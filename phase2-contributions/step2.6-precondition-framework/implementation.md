# Step 2.6 -- Precondition Framework Implementation

Date: February 19, 2026
Status: Complete
Time spent: roughly 4 hours
Branch: cgal-python-bindings (local build using Apple Clang)

---

## Background

During Phase 2 research (December 28, 2025) I found seven distinct crash scenarios in the Arrangement_2 Python bindings. Each of them kills the Python interpreter outright when triggered -- no exception, no traceback. The user just sees something like:

```
zsh: bus error       python3 test.py
zsh: segmentation fault  python3 test.py
```

After digging into the root causes, the crashes fell into two separate categories that each needed their own fix.

The first category is CGAL precondition violations. CGAL ships with `CGAL_precondition()` macros scattered throughout its C++ source. These macros validate inputs before operations proceed. The problem is that in Release builds, the standard `-DNDEBUG` flag compiles them out entirely, so when the Python bindings are built in Release mode, none of those checks ever run. When an invalid operation happens, CGAL ultimately calls `abort()`, which takes down the entire Python process.

The second category is handle invalidation, essentially use-after-free. When you call `remove_edge()` or `remove_isolated_vertex()`, the underlying C++ DCEL node gets freed. But on the Python side, the variable (say `he` or `v`) still holds a raw pointer to that now-freed memory. Any subsequent access through that variable dereferences freed memory and segfaults before CGAL even gets a chance to check anything.

---

## What Was Built

### Layer 1 -- CGAL Precondition Error Handler

New file: `src/libs/cgalpy/include/cgalpy_error_handler.h`
Modified: `src/libs/cgalpy/lib/export_module.cpp`
Modified: `src/libs/cgalpy/CMakeLists.txt`

The idea behind Layer 1 is straightforward. A new CMake option called `CGALPY_ENABLE_PRECONDITIONS` (defaulting to ON) controls whether the precondition macros stay active in the build. When the option is enabled, the build system strips `-DNDEBUG` from the Release and RelWithDebInfo compiler flags, which keeps the `CGAL_precondition()` macros compiled in.

On its own, re-enabling the macros is not enough. By default a precondition failure still calls `abort()`. So at Python module initialization time, a custom error handler is registered through `CGAL::set_error_handler()`. This handler throws a `std::runtime_error` with a descriptive message instead of aborting. nanobind then automatically translates that into a Python `RuntimeError`, which is exactly what a Python developer expects.

The error handler itself lives in `cgalpy_error_handler.h`:

```cpp
namespace CGALPy {

inline void precondition_handler(
    const char* type, const char* expr,
    const char* file, int line, const char* msg)
{
    std::string error_msg = std::string(type) + " violation: ("
                          + std::string(expr) + ")";
    if (msg && msg != '\0')
        error_msg += std::string(" -- ") + msg;
    error_msg += "  [" + std::string(file) + ":"
               + std::to_string(line) + "]";
    throw std::runtime_error(error_msg);
}

inline void register_error_handler() {
    CGAL::set_error_handler(CGALPy::precondition_handler);
}

} // namespace CGALPy
```

Registration happens as the very first thing in `export_module.cpp`:

```cpp
#include "cgalpy_error_handler.h"
...
MY_PYTHON_MODULE(CGALPY_MODULE_NAME, m) {
  m.attr("__path__") = XSTR(CGALPY_MODULE_NAME);

#ifdef CGALPY_PRECONDITIONS_ENABLED
  CGALPy::register_error_handler();   // registered here
#endif
  ...
}
```

The CMake block that makes this work is added right after `nanobind_add_module(...)`:

```cmake
option(CGALPY_ENABLE_PRECONDITIONS "Enable CGAL precondition checks" ON)
if(CGALPY_ENABLE_PRECONDITIONS)
    string(REPLACE "-DNDEBUG" "" CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE}")
    string(REPLACE "-DNDEBUG" "" CMAKE_CXX_FLAGS_RELWITHDEBINFO
           "${CMAKE_CXX_FLAGS_RELWITHDEBINFO}")
    target_compile_definitions(CGALPY PRIVATE CGALPY_PRECONDITIONS_ENABLED)
    message(STATUS "CGALPY: Precondition checks ENABLED (NDEBUG removed)")
else()
    message(STATUS "CGALPY: Precondition checks DISABLED")
endif()
```

---

### Layer 2 -- Handle Invalidation Registry

New file: `src/libs/cgalpy/include/handle_registry.h`
Modified: `src/libs/cgalpy/lib/arrangement_on_surface_2_bindings.cpp`

Layer 2 tackles the use-after-free crashes that Layer 1 cannot catch. A global singleton called `HandleRegistry` maintains a set of dead handle addresses. The set is keyed on `(arrangement_ptr, handle_ptr)` pairs -- not on the handle address alone. The reason for using pairs is explained further below.

The lifecycle works like this:

- Every removal wrapper calls `mark_dead()` before the actual C++ deletion happens.
- Every insertion wrapper calls `mark_alive()` on the returned handle, clearing any stale entry at a reused address.
- Every removal wrapper calls `check_alive()` as its very first line, before any dereference, raising `RuntimeError` if the handle is already dead.

The registry:

```cpp
namespace CGALPy {

class HandleRegistry {
public:
    using Key = std::pair<const void*, const void*>;

    static HandleRegistry& instance() {
        static HandleRegistry reg;
        return reg;
    }

    void mark_dead(const void* arr, const void* ptr) {
        dead_handles_.insert({arr, ptr});
    }

    void mark_alive(const void* arr, const void* ptr) {
        dead_handles_.erase({arr, ptr});
    }

    void check_alive(const void* arr, const void* ptr,
                     const char* handle_type) const {
        if (dead_handles_.count({arr, ptr})) {
            throw std::runtime_error(
                std::string(handle_type) + " handle is no longer valid. "
                "The underlying object was removed from the arrangement. "
                "Do not use a handle after the element it refers to has "
                "been removed."
            );
        }
    }

private:
    std::set<Key> dead_handles_;
    HandleRegistry() = default;
    HandleRegistry(const HandleRegistry&) = delete;
    HandleRegistry& operator=(const HandleRegistry&) = delete;
};

} // namespace CGALPy
```

---

### Patched Wrappers

Every wrapper in `arrangement_on_surface_2_bindings.cpp` that creates or destroys DCEL elements was patched.

**Removal wrappers** (call `check_alive` then `mark_dead`):

`remove_edge` (member function):

```cpp
Arrangement_on_surface_2::Face& remove_edge(
    Arrangement_on_surface_2& arr, Halfedge& e)
{
  CGALPy::HandleRegistry::instance().check_alive((void*)&arr, (void*)&e,
                                                  "Halfedge");
  auto twin_handle = e.twin();
  CGALPy::HandleRegistry::instance().mark_dead((void*)&arr, (void*)&e);
  CGALPy::HandleRegistry::instance().mark_dead((void*)&arr,
                                                (void*)&(*twin_handle));
  return *(arr.remove_edge(twin_handle));
}
```

`remove_edge_free` (free function) follows the same pattern with `aos` instead of `arr`.

`remove_isolated_vertex`:

```cpp
Arrangement_on_surface_2::Face& remove_isolated_vertex(
    Arrangement_on_surface_2& arr, Vertex& v)
{
  CGALPy::HandleRegistry::instance().check_alive((void*)&arr, (void*)&v,
                                                  "Vertex");
  CGALPy::HandleRegistry::instance().mark_dead((void*)&arr, (void*)&v);
  return *(arr.remove_isolated_vertex(Vertex_handle(&v)));
}
```

**Insertion wrappers** (call `mark_alive` on returned handles):

All six insert wrappers now call `mark_alive` on the returned handle. For halfedge-returning inserts, both the halfedge and its twin are marked alive. For vertex-returning inserts, just the vertex is marked.

Example from `insert_from_left_vertex1`:

```cpp
insert_from_left_vertex1(Arrangement_on_surface_2& arr,
                          X_monotone_curve_2& c, Vertex& v)
{
  Halfedge& result = *(arr.insert_from_left_vertex(c, Vertex_handle(&v)));
  auto& reg = CGALPy::HandleRegistry::instance();
  reg.mark_alive((void*)&arr, (void*)&result);
  reg.mark_alive((void*)&arr, (void*)&(*result.twin()));
  return result;
}
```

The full list of patched insert wrappers:

- `insert_from_left_vertex1` (takes Vertex)
- `insert_from_left_vertex2` (takes Halfedge)
- `insert_from_right_vertex1` (takes Vertex)
- `insert_from_right_vertex2` (takes Halfedge)
- `insert_xcv_in_face_interior` (returns Halfedge)
- `insert_pnt_in_face_interior` (returns Vertex)

---

### Why (arrangement_ptr, handle_ptr) Pairs Matter

This was a non-obvious bug I hit during testing. Consider what happens across consecutive test functions. In test 2:

```
arr = Arrangement_2()          # arr at address 0x...A
he = arr.insert_from_left_vertex(...)
arr.remove_edge(he)            # marks (0x...A, 0x...B) dead
# arr goes out of scope, DCEL freed, 0x...B returned to allocator
```

Then in test 3:

```
arr = Arrangement_2()          # NEW arr, might land at SAME address 0x...A
he1 = arr.insert_from_left_vertex(...)  # new halfedge, might land at 0x...B
arr.remove_edge(he1)           # If keyed by handle_ptr alone: (0x...B) is still in dead set!
                               # If keyed by (arr_ptr, handle_ptr): (0x...A, 0x...B) is fresh -- clean
```

Using just the handle pointer as the key caused test 7 (the regression test) to fail with a false positive. Switching to the `(arrangement_ptr, handle_ptr)` pair as the key fixed it completely.

---

## Build Instructions (macOS, Apple Silicon)

Always force Apple Clang. GCC from Homebrew fails with Qt6 pragma errors on macOS.

```bash
export CC=/usr/bin/clang
export CXX=/usr/bin/clang++

rm -rf build-manual && mkdir build-manual && cd build-manual

cmake -C ../cmake/tests/aos2_epec_fixed.cmake \
      -DCGALPY_ENABLE_PRECONDITIONS=ON \
      -DCMAKE_BUILD_TYPE=Release \
      -Dnanobind_DIR=$(python3 -c "import nanobind; print(nanobind.cmake_dir())") \
      ..

make CGALPY -j4
```

Look for this line in the cmake output to confirm Layer 1 is active:

```
-- CGALPY: Precondition checks ENABLED (NDEBUG removed)
```

---

## Files Changed in cgal-python-bindings

```
NEW:      src/libs/cgalpy/include/cgalpy_error_handler.h
NEW:      src/libs/cgalpy/include/handle_registry.h
MODIFIED: src/libs/cgalpy/lib/export_module.cpp
MODIFIED: src/libs/cgalpy/lib/arrangement_on_surface_2_bindings.cpp
MODIFIED: src/libs/cgalpy/CMakeLists.txt
MODIFIED: tests/crash_scenarios/test_all_crashes.py
```

---

## GSoC Proposal Alignment

This work directly completes the Weeks 5-6 deliverable from the proposal:

> "Crucial Safety Feature: Configure precondition failures to raise Python exceptions instead of crashing the interpreter."

> "Crash Mitigation: Address crash scenario #1 (remove_isolated_vertex on non-isolated vertex) as part of the new precondition framework."

All seven known crashes are now fixed, not just the first one. This was implemented pre-GSoC as part of preparation and is ready for Efi's review.