# 🔧 Named Parameters Study — CGAL Python Bindings Pattern

**Date:** January 11, 2026  
**Author:** Utkarsh Khajuria  
**Context:** GSoC 2026 - Understanding Efi's Named Parameters Implementation

---

## 📋 Executive Summary

CGAL's C++ Named Parameters system allows optional, compile-time type-safe parameter specification. Efi has implemented a sophisticated pattern in the Python bindings that translates Python dictionaries to C++ compile-time parameter chains.

This study documents the pattern so I can replicate it across 15-20 other functions in Weeks 7-8 of GSoC.

**Status:** ✅ Pattern understood | Ready for implementation

---

## 🎓 C++ CGAL Named Parameters (Background)

### How It Works in C++

CGAL functions accept optional named parameters using a chainable compile-time pattern:

```cpp
// C++ usage
CGAL::Polygon_mesh_processing::compute_face_normals(
    mesh,
    face_normals,
    CGAL::parameters::vertex_point_map(vpm)
                     .geom_traits(gt)
);
```

**Key characteristics:**
- **Compile-time type safety:** Each parameter type is encoded in the template chain
- **Chainable:** Use `.parameter_name(value)` to add parameters
- **Optional:** Start with `default_values()` and add only what you need
- **Type deduction:** Compiler deduces the full type at compile time

---

### Named Parameters in CGAL Documentation

From `compute_face_normals` C++ signature:

```cpp
template<typename PolygonMesh, typename Face_normal_map, 
         typename NamedParameters = parameters::Default_named_parameters>
void compute_face_normals(
    const PolygonMesh& pmesh,
    Face_normal_map face_normals,
    const NamedParameters& np = parameters::default_values()
)
```

**Optional Named Parameters accepted:**
- `vertex_point_map` — custom point property map
- `geom_traits` — custom geometric traits class

---

## 🐍 Python Binding Implementation (Efi's Solution)

**File Location:** `lib/export_pmp_normal_computation.cpp` (lines 35-60)

### The Wrapper Pattern

#### Step 1: Wrapper Class Template

```cpp
template <typename T, typename... Args>
struct Compute_face_normals_wrapper {
  static void call(T np, Args&&... args)
  { 
    PMP::compute_face_normals(
        std::forward<Args>(args)..., 
        std::forward<T>(np)
    ); 
  }
};
```

**Purpose:** Defers the actual C++ function call until the named parameter type `T` is fully constructed.

---

#### Step 2: Python-Facing Function

```cpp
template <typename PolygonMesh, typename FaceNormalMap>
void compute_face_normals(
    const PolygonMesh& mesh, 
    FaceNormalMap face_normals, 
    const py::dict& params = py::dict()  // ← Python dict!
) {
  using Pm = PolygonMesh;
  using Fn_map = FaceNormalMap;

  // Start with CGAL defaults
  auto np = CGAL::parameters::default_values();
  
  // Geometry traits handler
  CGALPY::Named_parameter_geom_traits op;
  
  // Create wrapper with mesh and face_normals
  CGALPY::Named_parameter_wrapper<
      Compute_face_normals_wrapper, 
      const Pm&, 
      const Fn_map&
  > wrapper(mesh, face_normals);
  
  // Apply parameters from Python dict
  CGALPY::named_parameter_applicator(wrapper, np, params, op);
}
```

---

#### Step 3: The Applicator Magic

`named_parameter_applicator()` (defined in `CGALPY/named_parameter_applicator.hpp`):

1. Iterates through keys in the Python `params` dict
2. For each key, looks up the corresponding CGAL named parameter
3. Extracts the value from the dict and casts to correct C++ type
4. Chains the parameter onto `np` using `.parameter_name(value)`
5. Once all parameters are applied, calls `wrapper.call(np, ...)`

---

### Python Usage (Result)

```python
from cgalpy import compute_face_normals

# Simple usage - no named parameters
compute_face_normals(mesh, face_normals)

# With named parameters as dict
compute_face_normals(
    mesh, 
    face_normals, 
    {"vertex_point_map": custom_vpm, "geom_traits": custom_traits}
)
```

**What happens under the hood:**
1. Python dict `{"vertex_point_map": custom_vpm}` passed to C++
2. `named_parameter_applicator` extracts `"vertex_point_map"` key
3. Constructs `np.vertex_point_map(custom_vpm)` in C++
4. Final call: `PMP::compute_face_normals(mesh, face_normals, np)`

---

## 🤔 Why This Is Non-Trivial

### Challenge 1: Compile-Time Types from Runtime Values

- **C++ named parameters:** Types computed at compile time
- **Python dict:** Values known only at runtime
- **Solution:** Template metaprogramming + wrapper pattern defers instantiation

### Challenge 2: Multiple Parameter Chains

Some functions accept multiple named parameters:

```cpp
// C++ - multiple parameters chained
CGAL::parameters::vertex_normal_map(nm)
                 .edge_is_constrained_map(ecm)
                 .visitor(my_visitor)
```

Each `.parameter_name()` call *changes the type* of the parameter chain. The applicator must handle arbitrary chains.

### Challenge 3: Type Safety Preservation

Python dict keys are strings, values are `py::object`. The binding must:
- Validate that parameter names are valid
- Cast Python objects to correct C++ types
- Maintain type safety without runtime overhead

### Challenge 4: Default Parameter Handling

Some parameters have defaults in CGAL. The binding must:
- Start with `default_values()`
- Override only parameters provided in Python dict
- Preserve all other defaults

---

## 🔩 Pattern Components (Infrastructure)

### 1. `Named_parameter_wrapper<FuncWrapper, Args...>`

**Purpose:** Stores the arguments to pass to the wrapped function.

```cpp
Named_parameter_wrapper<
    Compute_face_normals_wrapper, 
    const Pm&, 
    const Fn_map&
> wrapper(mesh, face_normals);
```

### 2. `Named_parameter_geom_traits`

**Purpose:** Handles special case of `geom_traits` parameter which is very common.

### 3. `named_parameter_applicator()`

**Purpose:** Core engine that parses Python dict and builds C++ parameter chain.

```cpp
template <typename Wrapper, typename NP, typename GeomTraitsOp>
void named_parameter_applicator(
    Wrapper& wrapper,       // Holds function args
    NP& np,                 // CGAL named params (modified)
    const py::dict& params, // Python dict
    GeomTraitsOp& op        // Geom traits handler
);
```

### 4. Helper Headers

- `CGALPY/Named_parameter_wrapper.hpp`
- `CGALPY/named_parameter_applicator.hpp`
- `CGALPY/Named_parameter_geom_traits.hpp`

---

## 📋 Candidate Functions for Named Parameters (GSoC Weeks 7-8)

### Priority 1: Polygon Mesh Processing (PMP) — 8 functions

| Function | Parameters | Complexity |
|----------|-----------|------------|
| `triangulate_faces` | `visitor`, `face_index_map` | Medium (visitor callbacks) |
| `fair` | `weight_calculator`, `fairing_continuity` | Medium |
| `smooth_shape` | `number_of_iterations`, `time`, `use_safety_constraints` | Low (simple types) |
| `isotropic_remeshing` | `number_of_iterations`, `edge_is_constrained_map`, `visitor` | High (multiple + visitor) |
| `extrude_mesh` | `maximum_offset` | Low |
| `split_long_edges` | `edge_is_constrained_map` | Low |
| `collapse_short_edges` | `edge_is_constrained_map` | Low |
| `detect_features` | `dihedral_angle` | Low |

### Priority 2: 2D Arrangements (AOS2) — 7 functions

| Function | Parameters | Complexity |
|----------|-----------|------------|
| `overlay` | `overlay_traits`, `vertex_color_map`, `edge_color_map` | High (complex traits) |
| `zone` | `output_iterator` | Medium |
| `vertical_decomposition` | `output_vertical_walls` | Medium |
| `insert_curve` (batch) | `curve_traits`, `split_at_intersections` | Medium |
| `remove_curve` (batch) | `visitor` | Medium |
| `locate_point` | `point_location_strategy` | Medium |
| `insert_point_in_face` | `point_location_hint` | Low |

---

## ✅ Implementation Checklist (Per Function)

For each function to be wrapped with Named Parameters:

### Step 1: Read C++ Documentation (30 min)
- [ ] Identify CGAL C++ signature
- [ ] List all accepted named parameters
- [ ] Note parameter types and defaults
- [ ] Check for special cases (visitors, traits)

### Step 2: Create Wrapper Class (15 min)

```cpp
template <typename T, typename... Args>
struct My_function_wrapper {
  static void call(T np, Args&&... args)
  { CGAL::my_function(std::forward<Args>(args)..., std::forward<T>(np)); }
};
```

### Step 3: Write Python-Facing Function (30 min)

```cpp
template <typename Arg1, typename Arg2>
void my_function(Arg1 arg1, Arg2 arg2, const py::dict& params = py::dict()) {
  auto np = CGAL::parameters::default_values();
  CGALPY::Named_parameter_geom_traits op;
  CGALPY::Named_parameter_wrapper<My_function_wrapper, Arg1, Arg2> wrapper(arg1, arg2);
  CGALPY::named_parameter_applicator(wrapper, np, params, op);
}
```

### Step 4: Bind to Python Module (5 min)

```cpp
m.def("my_function", &pmp::my_function<Pm, Arg2>,
      py::arg("arg1"), py::arg("arg2"),
      py::arg("np") = py::dict());
```

### Step 5: Test in Python (20 min)

```python
# Test 1: No parameters
result = my_function(arg1, arg2)

# Test 2: With parameters
result = my_function(arg1, arg2, {"param_name": value})

# Test 3: Invalid parameter name (should error gracefully)
result = my_function(arg1, arg2, {"invalid_param": value})
```

### Step 6: Document (10 min)
- [ ] Add docstring with parameter descriptions
- [ ] List accepted named parameters
- [ ] Provide example usage

**Total per function:** ~2 hours

---

## ❓ Open Questions for Efi

1. **Parameter validation:** Should `named_parameter_applicator` throw Python exceptions for unknown parameter names, or silently ignore them?

2. **Multi-parameter functions:** For functions that accept 5+ named parameters (like `isotropic_remeshing`), should we prioritize the most commonly used parameters first?

3. **Visitor callbacks:** Some CGAL functions accept visitor objects as named parameters. What's the best way to expose these to Python? (Visitors are typically classes with methods called during algorithm execution.)

4. **Performance:** Does the wrapper + applicator pattern introduce measurable overhead compared to direct binding? Should we profile?

5. **Documentation generation:** Can the applicator infrastructure auto-generate a list of accepted named parameters for `help()` output?

6. **Type hints:** Python 3.9+ supports `TypedDict`. Should we create type hint stubs like:
   ```python
   class ComputeFaceNormalsParams(TypedDict, total=False):
       vertex_point_map: VertexPointMap
       geom_traits: GeomTraits
   ```

---

## 📝 Next Steps (Post-Study)

### 1. Create Test Prototype (2 hours)
- Pick one simple function (`split_long_edges`)
- Implement full wrapper pattern
- Test in Python
- Document any issues

### 2. Batch Implementation (Weeks 7-8 of GSoC)
- Implement 15 functions from candidate list
- 2 hours per function = 30 hours
- 10 hours buffer for complex cases

### 3. Contributor Documentation (Week 8)
- Write `NAMED_PARAMETERS_PATTERN.md` guide
- Include this study as reference
- Add to `CONTRIBUTING.md`

---

## 🔗 References

- **Implementation:** `lib/export_pmp_normal_computation.cpp`
- **CGAL C++ Docs:** https://doc.cgal.org/latest/Polygon_mesh_processing/group__PMP__normal__grp.html
- **Nanobind Docs:** https://nanobind.readthedocs.io/
- **CGAL Named Parameters Guide:** https://doc.cgal.org/latest/BGL/group__bgl__namedparameters.html

---

**Document Status:** ✅ Complete  
**Ready for GSoC Weeks 7-8 Implementation:** Yes  
**Estimated Effort:** 40 hours (15 functions × 2h + 10h documentation)
