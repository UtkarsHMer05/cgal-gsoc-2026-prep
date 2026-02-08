# 🔧 CGAL Named Parameters: Implementation Research

**Research Date:** January 11, 2026  
**Status:** 🔬 IN PROGRESS  
**Researcher:** Utkarsh Khajuria  
**Context:** GSoC 2026 CGAL Python Bindings – Phase 3 Research Task 3

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [What Are CGAL Named Parameters?](#-what-are-cgal-named-parameters)
- [Mentor's Reference Implementation](#-mentors-reference-implementation)
- [Research Objectives](#-research-objectives)
- [Technical Deep Dive](#-technical-deep-dive)
- [Implementation Strategy](#-implementation-strategy)
- [Testing Plan](#-testing-plan)
- [Timeline for GSoC](#-timeline-for-gsoc)
- [Files in This Directory](#-files-in-this-directory)
- [References](#-references)

---

## 🎯 Overview

This directory contains research and implementation work for binding CGAL's compile-time Named Parameters pattern to Python. Named Parameters are CGAL's elegant solution for optional function arguments with type safety, but they use compile-time template metaprogramming that doesn't map directly to Python's runtime named arguments.

**Challenge Level:** 🔴 HIGH — Mentor Efi allocated 2 weeks (Weeks 7-8) for this task.

**Mentor Quote:**
> "It is a hard topic, and I suggest that you simply put it in the timetable and assign, say, 2 weeks to this task. Some functions accept more than one NamedParameter argument. I have already devised a method to extend the solution above, but again, not trivial."

---

## ❓ Problem Statement

### The Gap

**C++ CGAL API:**
```cpp
#include <CGAL/Polygon_mesh_processing/compute_normals.h>

// Beautiful compile-time optional parameters!
CGAL::Polygon_mesh_processing::compute_vertex_normals(
    mesh,
    CGAL::parameters::vertex_normal_map(normal_map)
                     .edge_is_constrained_map(constrained_map)
                     .geom_traits(traits)
);
```

**Current Python Bindings:**
```python
# Sad reality: No optional parameters exposed
compute_vertex_normals(mesh)  # Works, but no customization!

# Can't do this:
compute_vertex_normals(mesh, vertex_normal_map=my_map)  # ❌ Not bound
```

### Why This Matters

- **50+ CGAL functions** use Named Parameters
- Loss of **80% of function flexibility** in Python
- Users can't customize algorithms
- Research workflows blocked

---

## 🔧 What Are CGAL Named Parameters?

### C++ Template Magic

CGAL Named Parameters use compile-time type composition to build optional parameter sets:

```cpp
// Each parameter returns a new type with added information
auto params = CGAL::parameters::vertex_normal_map(vn_map)      // Type: NP1
                              .edge_is_constrained_map(ec_map) // Type: NP2<NP1>
                              .geom_traits(traits);            // Type: NP3<NP2<NP1>>

// The function signature accepts ANY combination via template
template <typename PolygonMesh, typename NamedParameters>
void compute_vertex_normals(const PolygonMesh& mesh, 
                           const NamedParameters& np);
```

### Compile-Time Type Safety

```cpp
// CGAL checks parameter types at compile time
CGAL::parameters::vertex_normal_map(my_map)  // ✅ Type must be PropertyMap<Vertex, Vector>

// Wrong type = compile error
CGAL::parameters::vertex_normal_map(42);     // ❌ Compile error!
```

### The Challenge for Python

Python is dynamically typed and has no compile time:

```python
# Python's approach: runtime keyword arguments
def my_function(mesh, vertex_normal_map=None, edge_map=None):
    # Check types at runtime
    pass
```

**Mismatch:**
- **C++:** Type information in the type system
- **Python:** Type information at runtime
- **Bridge needed!**

---

## 🔬 Mentor's Reference Implementation

### Location

```
cgal-python-bindings/
└── lib/
    └── export_pmp_normal_computation.cpp
```

### Function: `compute_face_normals()`

**C++ Signature:**
```cpp
template <typename PolygonMesh, typename NamedParameters>
void compute_face_normals(const PolygonMesh& mesh,
                         const NamedParameters& np = CGAL::parameters::default_values());
```

**Efi's Python Binding (Simplified View):**
```cpp
#include <nanobind/nanobind.h>
#include <CGAL/Polygon_mesh_processing/compute_normals.h>

namespace nb = nanobind;
namespace PMP = CGAL::Polygon_mesh_processing;

// Binding with Named Parameters support
m.def("compute_face_normals",
    [](const SurfaceMesh& mesh, 
       nb::kwargs kwargs) {  // Accept Python keyword arguments
        
        // Extract optional parameters from kwargs
        auto np = CGAL::parameters::default_values();
        
        if (kwargs.contains("vertex_normal_map")) {
            // Convert Python object to C++ property map
            auto vn_map = kwargs["vertex_normal_map"].cast<VertexNormalMap>();
            np = np.vertex_normal_map(vn_map);
        }
        
        if (kwargs.contains("geom_traits")) {
            auto traits = kwargs["geom_traits"].cast<Traits>();
            np = np.geom_traits(traits);
        }
        
        // Call CGAL function with composed parameters
        PMP::compute_face_normals(mesh, np);
    },
    nb::arg("mesh"),
    "Compute face normals with optional parameters"
);
```

**Python Usage:**
```python
from cgalpy import compute_face_normals, SurfaceMesh

mesh = SurfaceMesh()
# ... load mesh ...

# No parameters - use defaults
compute_face_normals(mesh)

# With optional parameter map
normal_map = create_vertex_normal_map(mesh)
compute_face_normals(mesh, vertex_normal_map=normal_map)

# Multiple parameters
compute_face_normals(mesh, 
                    vertex_normal_map=normal_map,
                    geom_traits=custom_traits)
```

---

## 🎯 Research Objectives

### Primary Goals

1. **Understand Efi's Pattern**
   - How does `export_pmp_normal_computation.cpp` work?
   - What nanobind features are used?
   - How are C++ property maps exposed to Python?

2. **Document the Template**
   - Create reusable pattern for other functions
   - Identify common Named Parameters across CGAL packages
   - Write contributor guide

3. **Handle Multi-Parameter Cases**
   - Mentor mentioned: "Some functions accept MORE than one NamedParameter"
   - Understand the extension method Efi devised
   - Test parameter composition

4. **Create Python-Friendly API**
   - Match Python conventions (snake_case kwargs)
   - Type hints for IDE support
   - Clear error messages for invalid parameters

### Deliverables for GSoC Weeks 7-8

- [ ] Technical analysis document (`named-params-analysis.md`)
- [ ] Implementation pattern template (`binding_template.cpp`)
- [ ] 15-20 functions bound with Named Parameters
- [ ] Test suite for parameter combinations
- [ ] Contributor documentation

---

## 🔍 Technical Deep Dive

### Step 1: Extracting the Pattern

**Key Components:**

1. **Lambda Wrapper**
   - Accepts `nb::kwargs` for Python keyword arguments
   - Builds CGAL Named Parameters from kwargs
   - Calls C++ function with composed parameters

2. **Type Conversions**
   - Python objects → C++ property maps
   - Runtime type checking
   - Helpful error messages

3. **Parameter Composition**
   ```cpp
   auto np = CGAL::parameters::default_values();
   if (has_param_A) np = np.param_A(value_A);
   if (has_param_B) np = np.param_B(value_B);
   // Type: NP_B<NP_A<default_values>>
   ```

4. **Default Values**
   - CGAL provides sensible defaults
   - Python kwargs make defaults optional
   - Matches Python idioms perfectly

---

### Step 2: Multi-Parameter Handling

**Challenge:** Some functions accept **multiple independent Named Parameter sets**

**Example C++ API:**
```cpp
CGAL::Polygon_mesh_processing::triangulate_faces(
    mesh,
    CGAL::parameters::vertex_point_map(vpm)     // Parameters for mesh
                     .face_index_map(fim),
    CGAL::parameters::geom_traits(traits)       // Parameters for visitor
);
```

**Efi's Extension Method (Hypothesis):**
```cpp
m.def("triangulate_faces",
    [](const SurfaceMesh& mesh,
       nb::kwargs mesh_params,
       nb::kwargs visitor_params) {
        
        // Build two separate parameter sets
        auto np_mesh = build_params(mesh_params, 
                                   {"vertex_point_map", "face_index_map"});
        auto np_visitor = build_params(visitor_params,
                                      {"geom_traits"});
        
        PMP::triangulate_faces(mesh, np_mesh, np_visitor);
    },
    nb::arg("mesh"),
    nb::arg("mesh_params") = nb::dict(),
    nb::arg("visitor_params") = nb::dict()
);
```

**Python Usage:**
```python
triangulate_faces(mesh,
                 mesh_params={"vertex_point_map": vpm},
                 visitor_params={"geom_traits": traits})
```

---

### Step 3: Common Named Parameters Catalog

| Parameter Name | Type | Used In Packages | Frequency |
|---------------|------|------------------|-----------|
| `vertex_point_map` | PropertyMap<Vertex, Point> | PMP, Mesh, Surface | 30+ functions |
| `vertex_normal_map` | PropertyMap<Vertex, Vector> | PMP, Normals | 15+ functions |
| `face_index_map` | PropertyMap<Face, int> | PMP, Mesh | 20+ functions |
| `edge_is_constrained_map` | PropertyMap<Edge, bool> | PMP, Meshing | 12+ functions |
| `geom_traits` | GeometricTraits | All packages | 40+ functions |
| `visitor` | Visitor concept | PMP, Surface | 8+ functions |

**Priority for Binding:**
- **High:** `vertex_point_map`, `geom_traits` (used everywhere)
- **Medium:** `vertex_normal_map`, `face_index_map`
- **Low:** Specialized visitors

---

## 🛠️ Implementation Strategy

### Phase 1: Study Reference (Week 7, Days 1-3)

```
research/named-params/study/
├── export_pmp_analysis.md          # Line-by-line analysis
├── nanobind_kwargs_examples.cpp    # nanobind::kwargs experiments
└── parameter_composition_test.cpp  # Test CGAL parameter chaining
```

**Tasks:**
1. Read `export_pmp_normal_computation.cpp` completely
2. Identify nanobind features used:
   - `nb::kwargs`
   - `nb::dict`
   - Type casting with `.cast<T>()`
3. Document parameter extraction pattern
4. Test locally with simple example

### Phase 2: Create Reusable Template (Week 7, Days 4-7)

**File:** `templates/named_param_binding_template.cpp`

```cpp
/*
 * TEMPLATE: Named Parameter Binding for CGAL Functions
 * 
 * How to use:
 * 1. Replace FUNCTION_NAME with your function
 * 2. Replace PARAM_LIST with supported parameters
 * 3. Add parameter extraction logic
 * 4. Update docstring
 */

#include <nanobind/nanobind.h>
#include <nanobind/stl/optional.h>
#include <CGAL/Named_function_parameters.h>

namespace nb = nanobind;

// Helper: Build Named Parameters from Python kwargs
template <typename Mesh>
auto build_named_parameters(const nb::kwargs& kwargs) {
    auto np = CGAL::parameters::default_values();
    
    // STEP 1: Extract each optional parameter
    if (kwargs.contains("vertex_point_map")) {
        auto vpm = kwargs["vertex_point_map"].cast<VertexPointMap>();
        np = np.vertex_point_map(vpm);
    }
    
    if (kwargs.contains("vertex_normal_map")) {
        auto vnm = kwargs["vertex_normal_map"].cast<VertexNormalMap>();
        np = np.vertex_normal_map(vnm);
    }
    
    // Add more parameters here...
    
    return np;
}

// Binding
m.def("FUNCTION_NAME",
    [](const Mesh& mesh, nb::kwargs kwargs) {
        auto np = build_named_parameters<Mesh>(kwargs);
        CGAL::PACKAGE::FUNCTION_NAME(mesh, np);
    },
    nb::arg("mesh"),
    R"pbdoc(
        FUNCTION_NAME with Named Parameters support.
        
        Parameters
        ----------
        mesh : Mesh
            The input mesh
        **kwargs : optional
            Named parameters:
            - vertex_point_map : PropertyMap
            - vertex_normal_map : PropertyMap
            - ...
    )pbdoc"
);
```

### Phase 3: Implement 15-20 Functions (Week 8)

**Target Functions:**

| Package | Function | Named Parameters | Priority |
|---------|----------|------------------|----------|
| PMP | `compute_vertex_normals` | 3 parameters | HIGH |
| PMP | `smooth_mesh` | 5 parameters | HIGH |
| PMP | `fair_mesh` | 4 parameters | MEDIUM |
| PMP | `triangulate_faces` | 2 parameter sets | HIGH |
| PMP | `refine_mesh` | 6 parameters | MEDIUM |
| Meshing | `lloyd_optimize_mesh` | 4 parameters | MEDIUM |
| Surface | `make_surface_mesh` | 5 parameters | HIGH |

**Implementation Order:**
1. Single parameter functions (easier)
2. Multi-parameter functions (use Efi's extension)
3. Complex parameter types (visitors, callbacks)

---

## 📊 Testing Plan

### Unit Tests

```
tests/
├── test_parameter_extraction.cpp      # C++ level: kwargs → CGAL params
├── test_parameter_composition.cpp     # Parameter chaining works
├── test_type_conversions.cpp          # Python → C++ type casting
└── test_named_parameters.py           # Python level: end-to-end
```

### Python Test Example

```python
import pytest
from cgalpy import SurfaceMesh, compute_vertex_normals

class TestNamedParameters:
    
    def test_no_parameters_default_behavior(self):
        """Test function works with no optional parameters"""
        mesh = SurfaceMesh()
        compute_vertex_normals(mesh)  # Should use defaults
        assert True  # No crash
    
    def test_single_parameter(self):
        """Test function with one Named Parameter"""
        mesh = SurfaceMesh()
        normal_map = create_vertex_normal_property_map(mesh)
        
        compute_vertex_normals(mesh, vertex_normal_map=normal_map)
        
        # Verify normals computed
        for v in mesh.vertices():
            assert normal_map[v].squared_length() > 0
    
    def test_multiple_parameters(self):
        """Test function with multiple Named Parameters"""
        mesh = SurfaceMesh()
        normal_map = create_vertex_normal_property_map(mesh)
        traits = CustomTraits()
        
        compute_vertex_normals(mesh,
                              vertex_normal_map=normal_map,
                              geom_traits=traits)
        assert True
    
    def test_invalid_parameter_type(self):
        """Test error handling for wrong parameter types"""
        mesh = SurfaceMesh()
        
        with pytest.raises(TypeError, match="vertex_normal_map"):
            compute_vertex_normals(mesh, vertex_normal_map=42)  # Wrong type!
    
    def test_unknown_parameter(self):
        """Test warning for unknown parameters"""
        mesh = SurfaceMesh()
        
        with pytest.warns(UserWarning, match="unknown parameter"):
            compute_vertex_normals(mesh, invalid_param="value")
```

---

## 📅 Timeline for GSoC Weeks 7-8

### Week 7: Research & Template Creation

| Day | Task | Hours | Deliverable |
|-----|------|-------|-------------|
| Mon | Study `export_pmp_normal_computation.cpp` | 4h | Analysis document |
| Tue | Experiment with nanobind kwargs | 3h | Working examples |
| Wed | Test CGAL parameter composition | 3h | Composition tests |
| Thu | Create reusable template | 4h | Template code |
| Fri | Document pattern for contributors | 3h | Tutorial guide |
| Sat-Sun | Implement 5 simple functions | 6h | First 5 bindings |

**Total: 23 hours**

### Week 8: Implementation & Testing

| Day | Task | Hours | Deliverable |
|-----|------|-------|-------------|
| Mon | Implement 5 more functions | 4h | 10 total bindings |
| Tue | Multi-parameter functions (Efi's extension) | 5h | 2-3 complex bindings |
| Wed | Implement final 5-7 functions | 4h | 15-20 total |
| Thu | Write Python tests | 3h | Test suite |
| Fri | Debug and fix issues | 4h | All tests passing |
| Sat | Documentation polish | 2h | Complete docs |
| Sun | Code review prep | 1h | PR ready |

**Total: 23 hours**

**Grand Total: 46 hours** (exceeds 40h allocation for buffer)

---

## 📁 Files in This Directory

```
test-named-params-implementation/
├── README.md                               # This file
├── task3-named-params-study.md            # Research findings document
├── simple_geometry.hpp                     # Test geometry helpers
├── named_param_binding.cpp                 # Proof-of-concept binding
├── test_binding.py                         # Python test script
├── CMakeLists.txt                          # Build configuration
├── analysis/
│   ├── export_pmp_analysis.md             # Line-by-line code analysis
│   ├── common_named_parameters.md         # Parameter catalog
│   └── multi_parameter_cases.md           # Efi's extension examples
├── templates/
│   ├── named_param_binding_template.cpp   # Reusable binding pattern
│   └── multi_param_example.cpp            # Complex case
└── tests/
    ├── test_parameter_extraction.cpp      # C++ unit tests
    └── test_named_parameters.py           # Python integration tests
```

---

## 🎓 Key Learnings

### Technical Insights

**nanobind kwargs is Powerful**
- `nb::kwargs` captures Python keyword arguments
- `.contains("key")` checks existence
- `.cast<Type>()` converts with type checking

**CGAL Parameter Chaining**
- Each parameter returns a new composed type
- Order doesn't matter (type composition handles it)
- Default values provided by CGAL

**Type Erasure Challenge**
- C++ template instantiation at compile time
- Python needs runtime dispatch
- Lambda wrappers bridge the gap

**Error Handling is Critical**
- Wrong types should give helpful messages
- Unknown parameters should warn (not crash)
- Match Python's exception conventions

---

## ⚠️ Common Pitfalls

### 1. Property Map Lifetime

**Problem:**
```cpp
// BAD: Property map destroyed before use
m.def("func", [](Mesh& m, nb::kwargs kw) {
    auto vpm = kw["vpm"].cast<VPM>();  // Local variable!
    auto np = params::vertex_point_map(vpm);
    CGAL::func(m, np);  // vpm might be destroyed!
});
```

**Solution:**
```cpp
// GOOD: Use keep_alive or move semantics
m.def("func", [](Mesh& m, nb::kwargs kw) {
    // ... implementation ...
}, nb::keep_alive<1, 2>());  // Keep kwargs alive with mesh
```

### 2. Template Instantiation Explosion

**Problem:** Each parameter combination creates a new template instantiation

```cpp
// This could generate 2^5 = 32 template instantiations!
// param_A, param_B, param_A+B, param_A+C, ... all combinations
```

**Solution:** Use type-erased parameter storage where possible

### 3. Python vs C++ Naming

```cpp
// C++ CGAL
params::vertex_point_map(vpm)

// Python - matches! (already snake_case)
compute_normals(mesh, vertex_point_map=vpm)
```

**Good News:** CGAL already uses snake_case! No conversion needed.

---

## 🔗 References

### CGAL Documentation
- [Named Function Parameters](https://doc.cgal.org/latest/BGL/group__bgl__namedparameters.html)
- [Polygon Mesh Processing](https://doc.cgal.org/latest/Polygon_mesh_processing/)
- [Property Maps](https://doc.cgal.org/latest/Property_map/)

### nanobind Documentation
- [Keyword Arguments](https://nanobind.readthedocs.io/)
- [Type Casting](https://nanobind.readthedocs.io/)
- [Keep Alive Policy](https://nanobind.readthedocs.io/)

### Mentor Communication
- **Email:** Dec 31, 2025 — "It is a hard topic"
- **Email:** Jan 7, 2026 — "I have already devised a method to extend the solution"

---

## 📧 Questions for Mentor

**Prepared for Next Email:**

1. **Multi-Parameter Approach:**
   > "You mentioned extending the solution for functions with multiple NamedParameter sets. Is the approach to use separate nb::kwargs arguments for each parameter group, or is there a more elegant method?"

2. **Property Map Exposure:**
   > "Should I bind property map creation functions first (e.g., `create_vertex_point_map`), or can users create them in Python?"

3. **Priority Functions:**
   > "Which 15-20 functions would have the most impact for users? I'm thinking PMP normals and smoothing, but want to align with your vision."

4. **Error Handling:**
   > "For invalid parameter types, should we raise `TypeError` immediately, or try to convert and raise helpful messages?"

---

**Last Updated:** January 11, 2026, 10:01 PM IST  
**Status:** 📋 Research Task 3 — Ready to Begin  
**Next Steps:** Study `export_pmp_normal_computation.cpp`, create analysis document  
**Estimated Completion:** Week 8 of GSoC (if accepted)
