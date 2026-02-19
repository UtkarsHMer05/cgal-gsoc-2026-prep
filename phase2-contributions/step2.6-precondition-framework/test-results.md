# Step 2.6 -- Precondition Framework Test Results

Date: February 19, 2026
Test file: `tests/crash_scenarios/test_all_crashes.py`
Result: 7 out of 7 passed

---

## Full Test Output

```
======================================================================
CGAL Python Bindings - Crash Scenario Tests
Testing library: CGALPY

[1/7] Testing: remove_isolated_vertex on non-isolated vertex
PASS: RuntimeError raised ->
      precondition violation: (v->is_isolated())
      [/opt/homebrew/include/CGAL/Arrangement_2/
       Arrangement_on_surface_2_impl.h:1482]

[2/7] Testing: remove_edge called twice on same halfedge
PASS: RuntimeError raised ->
      Halfedge handle is no longer valid. The underlying object was
      removed from the arrangement. Do not use a handle after the
      element it refers to has been removed.

[3/7] Testing: Accessing halfedge.curve() after removal
PASS: RuntimeError raised ->
      precondition violation: (x.PTR != static_cast<Rep*>(0))
      [/opt/homebrew/include/CGAL/Handle.h:52]

[4/7] Testing: Accessing twin halfedge after edge removal
PASS: RuntimeError raised ->
      Halfedge handle is no longer valid. The underlying object was
      removed from the arrangement. Do not use a handle after the
      element it refers to has been removed.

[5/7] Testing: remove_isolated_vertex called twice
PASS: RuntimeError raised ->
      Vertex handle is no longer valid. The underlying object was
      removed from the arrangement. Do not use a handle after the
      element it refers to has been removed.

[6/7] Testing: merge_edge on non-adjacent edges
PASS: RuntimeError raised ->
      precondition violation: (false)
      -- The input edges do not share a common vertex.
      [/opt/homebrew/include/CGAL/Arrangement_2/
       Arrangement_on_surface_2_impl.h:1648]

[7/7] Testing: Basic ops still work after framework enabled (regression)
PASS: Basic ops + regression (no false positives)

======================================================================
CRASH SCENARIO TEST RESULTS
Passed: 7/7
Failed: 0/7
ALL TESTS PASSED
```

---

## Before vs After

| Test | Scenario | Before (no framework) | After (framework enabled) |
|------|----------|-----------------------|---------------------------|
| 1 | `remove_isolated_vertex` on non-isolated vertex | `zsh: bus error` | `RuntimeError: precondition violation: (v->is_isolated())` |
| 2 | `remove_edge` called twice on same halfedge | `zsh: segmentation fault` | `RuntimeError: Halfedge handle is no longer valid` |
| 3 | `he.curve()` after edge removal | `zsh: segmentation fault` | `RuntimeError: precondition violation: (x.PTR != 0)` |
| 4 | Accessing twin halfedge after edge removal | `zsh: segmentation fault` | `RuntimeError: Halfedge handle is no longer valid` |
| 5 | `remove_isolated_vertex` called twice | `zsh: segmentation fault` | `RuntimeError: Vertex handle is no longer valid` |
| 6 | `merge_edge` on non-adjacent edges | `zsh: segmentation fault` | `RuntimeError: precondition violation: (false)` |
| 7 | Regression -- normal ops after address reuse | n/a | PASS, no false positives |

---

## Crash Category Breakdown

### Category A -- CGAL Precondition Violations

These are caught by Layer 1 of the framework. By removing `-DNDEBUG` from the build and registering a custom error handler, CGAL's own internal precondition checks fire at runtime. The handler converts what would have been an `abort()` call into a `RuntimeError`.

| Crash | CGAL source file | Line |
|-------|------------------|------|
| 1, `remove_isolated_vertex` | `Arrangement_on_surface_2_impl.h` | 1482 |
| 3, `he.curve()` null pointer | `Handle.h` | 52 |
| 6, `merge_edge` non-adjacent | `Arrangement_on_surface_2_impl.h` | 1648 |

### Category B -- Handle Invalidation (Use-After-Free)

These are caught by Layer 2 of the framework. The `HandleRegistry` detects that a Python variable holds a pointer to a freed DCEL element and raises `RuntimeError` before any C++ dereference happens.

| Crash | Trigger | Handle type |
|-------|---------|-------------|
| 2, `remove_edge` twice | Second call on a dead halfedge | Halfedge |
| 4, twin after removal | Twin was captured before the edge was removed | Halfedge |
| 5, `remove_isolated_vertex` twice | Second call on a dead vertex | Vertex |

---

## Regression Safety (Test 7)

Test 7 specifically verifies that the framework does not produce false positives. The concern is address reuse: after removing a DCEL element, the allocator might hand out the same memory address for a newly inserted element. If the dead-handle set is not managed carefully, the new handle would be incorrectly flagged as dead.

The test does exactly this:

```python
arr = Arrangement_2()
v = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
he = arr.insert_from_left_vertex(Curve(Point_2(0,0), Point_2(5,5)), v)
arr.remove_edge(he)              # he and twin marked dead

# Fresh insert in the SAME arrangement -- DCEL may reuse freed addresses
v2 = arr.insert_in_face_interior(Point_2(1, 1), arr.unbounded_face())
he2 = arr.insert_from_left_vertex(Curve(Point_2(1,1), Point_2(6,6)), v2)
arr.remove_edge(he2)             # must NOT false-positive -- PASSES
```

This works because `mark_alive()` is called on every insertion, which clears any stale dead-set entry at a reused address before it can cause a false `RuntimeError`.

---

## Environment

```
OS:       macOS Darwin 25.2.0 (Apple Silicon M2)
Compiler: Apple Clang 17.0.0 (clang-1700.6.3.2)
Python:   3.12.12 (miniforge3)
CGAL:     from Homebrew (/opt/homebrew/include/CGAL)
Boost:    1.84.0
Build:    Release + CGALPY_ENABLE_PRECONDITIONS=ON
```

Note: GCC from Homebrew must not be used. It fails with Qt6 pragma errors on macOS. Always force `/usr/bin/clang++` (Apple Clang).
