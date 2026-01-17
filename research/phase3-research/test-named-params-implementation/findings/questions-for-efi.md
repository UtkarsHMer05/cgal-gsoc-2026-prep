# ❓ Questions for Efi — Named Parameters Implementation

**Date:** January 17, 2026  
**Context:** Preparation for GSoC 2026 Weeks 7-8 (Named Parameters task)  
**Purpose:** Technical clarifications after studying the architecture

---

## 📋 Table of Contents

- [Summary of Analysis](#-summary-of-analysis-completed)
- [Section 1: Migration Strategy](#-section-1-migration-from-switch-based-to-operator-based)
- [Section 2: Operator Priorities](#-section-2-operator-implementation-priorities)
- [Section 3: Multi-Parameter Functions](#-section-3-multi-parameter-functions)
- [Section 4: Property Maps](#-section-4-property-map-binding-strategy)
- [Section 5: Testing](#-section-5-testing-strategy)
- [Section 6: Documentation](#-section-6-documentation-requirements)
- [Section 7: Performance](#-section-7-performance-and-edge-cases)
- [Section 8: Integration](#-section-8-integration-with-existing-code)
- [Section 9: Scope](#-section-9-scope-clarification-for-weeks-7-8)
- [Section 10: Final Questions](#-section-10-final-questions)
- [Summary](#-summary-of-key-questions)

---

## ✅ Summary of Analysis Completed

Over the past 2 hours, I've analyzed:
- ✅ `export_pmp_normal_computation.cpp` (138 lines)
- ✅ `named_parameter_applicator.hpp` (42 lines)
- ✅ `Named_parameter_wrapper.hpp` (40 lines)
- ✅ `Named_parameter_geom_traits.hpp` (32 lines)
- ✅ `pmp_np_parser.hpp` (118 lines - switch-based legacy system)

**Key Discovery:** You've built a sophisticated operator-based system using variadic templates that recursively processes Python dict items and builds CGAL parameter chains. The architecture is elegant and fully reusable.

I have specific questions to ensure I implement Weeks 7-8 correctly.

---

## 📦 Section 1: Migration from Switch-Based to Operator-Based

### Question 1.1: Migration Status

I noticed `pmp_np_parser.hpp` has ~20 parameters commented out:

```cpp
// case internal::Hash("vertex_point_map"):
// case internal::Hash("vertex_normal_map"):
// ... (18+ more)
```

**Are these commented out because:**
- **A)** You're migrating from switch-based → operator-based system?
- **B)** They're not yet implemented and waiting for GSoC?
- **C)** They have issues that need resolution?

> **My assumption:** You're migrating to the operator-based system, and Weeks 7-8 involves creating 15-20 operator structs to replace the commented switch cases.
>
> **Is this correct?**

### Question 1.2: Which System Should GSoC Use?

Should I focus Weeks 7-8 on:
- **Option A:** Creating operator structs (`Named_parameter_*.hpp` files)
- **Option B:** Uncommenting switch cases and fixing them
- **Option C:** Hybrid approach (both systems coexist)

> **My understanding:** Option A (operators) is the future, but want to confirm.

---

## 🎯 Section 2: Operator Implementation Priorities

### Question 2.1: Priority Order

Based on frequency in CGAL PMP functions, I identified this priority order:

**Tier 1 (Critical - 5 operators):**
1. `vertex_point_map` — Used in ~30 functions
2. `vertex_normal_map` — Used in ~15 functions
3. `face_index_map` — Used in ~20 functions
4. `vertex_index_map` — Used in ~12 functions
5. `geom_traits` — Already done ✅

**Tier 2 (High - 5 operators):**
6. `edge_is_constrained_map`
7. `vertex_is_constrained_map`
8. `halfedge_index_map`
9. `edge_index_map`
10. `face_patch_map`

**Tier 3 (Medium - 5 operators):**
11. `vertex_mean_curvature_map`
12. `point_to_vertex_map`
13. `vertex_incident_patches_map`
14. `allow_move_functor` — Already done ✅
15. `vertex_principal_curvatures_and_directions` — Already done ✅

> **Does this priority align with your usage patterns? Should I reorder based on which PMP functions we want to expose first?**

### Question 2.2: Target Number

Your email mentioned *"Not trivial - 2 weeks allocation"* for Named Parameters.

**How many operators should I realistically implement in Weeks 7-8?**

My estimate:
- **15-20 operators** (5-7 per week)
- Each operator = ~30 lines of code + tests
- Total: 450-600 lines of new code

> **Is this scope reasonable, or should I adjust?**

---

## 🔢 Section 3: Multi-Parameter Functions

### Question 3.1: Extension Method Clarification

Your email stated:
> "Some functions accept MORE than one NamedParameter argument. I have already devised a method to extend the solution."

I understand the basic case:

```cpp
// Single parameter type - works now
compute_face_normals(mesh, fnormals, 
                     {"geom_traits": kernel})

// Calls: PMP::compute_face_normals(mesh, fnormals, 
//                                   params.geom_traits(kernel))
```

But for multi-parameter functions like:

```cpp
// Function signature might be:
// PMP::isotropic_remeshing(mesh, 
//                          CGAL::parameters::edge_is_constrained_map(ecm)
//                                            .vertex_point_map(vpm)
//                                            .vertex_is_constrained_map(vcm))
```

**Question:** Does the current `named_parameter_applicator` already handle this by chaining operators?

My hypothesis:

```cpp
// Python call
isotropic_remeshing(mesh, {
    "edge_is_constrained_map": ecm,
    "vertex_point_map": vpm,
    "vertex_is_constrained_map": vcm
})

// The applicator processes ALL three dict items and chains:
// np.edge_is_constrained_map(ecm)
//   .vertex_point_map(vpm)
//   .vertex_is_constrained_map(vcm)
```

> **Is this the "extension method" you mentioned, or is there something more complex I'm missing?**

### Question 3.2: Example Function

Could you point me to a specific CGAL PMP function that uses multiple Named Parameters?

I want to study it to ensure I understand the pattern correctly before implementing.

Examples I found in CGAL docs:
- `isotropic_remeshing()` — 7+ parameters
- `smooth_mesh()` — 5+ parameters
- `fair_mesh()` — 4+ parameters

> **Which one would be a good reference implementation?**

---

## 🗺️ Section 4: Property Map Binding Strategy

### Question 4.1: Property Map Creation

For parameters like `vertex_point_map`, users need property map objects.

**Should I bind property map creation functions first?** For example:

```python
# Option A: Bind property map getters
vpm = mesh.points()  # Returns Property_map<Vd, Point_3>
PMP.compute_normals(mesh, vnormals, {"vertex_point_map": vpm})

# Option B: Users pass None, we use default
PMP.compute_normals(mesh, vnormals, {})  # Uses mesh default

# Option C: Automatic - we get it internally
# (Not exposed to Python at all)
```

> **Which approach do you prefer? My guess is Option A (explicit), but want to confirm.**

### Question 4.2: Type Casting Challenge

Property maps have complex template types:

```cpp
// Surface_mesh
using Vpm = Surface_mesh::Property_map<Vd, Point_3>;

// Polyhedron_3  
using Vpm = boost::property_map<Polyhedron, vertex_point_tag>::type;
```

In the operator struct, should I:
- **Option A:** Use generic `py::cast<>` and let nanobind handle it?
- **Option B:** Template-specialize operators for each mesh type?
- **Option C:** Something else?

Current `geom_traits` operator uses Option A:

```cpp
return np.geom_traits(py::cast<const Kernel&>(value));
```

> **Should I follow this pattern for all operators?**

---

## 🧪 Section 5: Testing Strategy

### Question 5.1: Test Scope

For each operator I implement, should tests cover:

| Level | Description | Include in Weeks 7-8? |
|-------|-------------|----------------------|
| 1 | Operator in isolation (pass valid property map) | ✅ |
| 2 | Operator in function binding (call actual PMP function) | ✅ |
| 3 | Multiple operators together (parameter chaining) | ✅ |
| 4 | Error cases (wrong type, None, invalid map) | ⏳ Defer to Weeks 11-12? |

> **Which levels are essential for Weeks 7-8?**

### Question 5.2: Existing Tests

I see `test_binding.py` and test scripts in the repo.

**Are there existing tests for Named Parameters I should follow as a template?** Or should I create a new test structure?

My plan:

```python
# File: test_named_parameters.py

def test_vertex_point_map():
    mesh = create_test_mesh()
    vpm = mesh.points()
    # Test that parameter is accepted
    result = PMP.some_function(mesh, {"vertex_point_map": vpm})
    assert result is not None

def test_multiple_parameters():
    # Test parameter chaining
    result = PMP.function(mesh, {
        "vertex_point_map": vpm,
        "vertex_normal_map": vnm,
        "geom_traits": kernel
    })
    # Verify all parameters applied
```

> **Does this structure work for you?**

---

## 📖 Section 6: Documentation Requirements

### Question 6.1: Docstring for Named Parameters

When binding functions with Named Parameters, should docstrings:

**Option A:** List all possible parameters

```python
"""
compute_face_normals(mesh, fnormals, np={})

Parameters
----------
mesh : PolygonMesh
fnormals : Face_normal_map
np : dict, optional
    Named parameters:
    - "geom_traits": Kernel
    - "vertex_point_map": Property_map
    - ... (list all 15-20)
"""
```

**Option B:** Generic parameter dict

```python
"""
compute_face_normals(mesh, fnormals, np={})

Parameters
----------
np : dict, optional
    CGAL Named Parameters. See documentation.
"""
```

**Option C:** Link to external documentation

```python
"""
See CGAL PMP documentation for supported Named Parameters:
https://doc.cgal.org/latest/Polygon_mesh_processing/
"""
```

> **Which approach aligns with your vision?**

### Question 6.2: Contributor Guide

**Should I create a contributor guide for future operator implementations?**

Template:

```markdown
# Adding a New Named Parameter Operator

## Step 1: Create operator struct
File: Named_parameter_PARAM_NAME.hpp

## Step 2: Add to CMakeLists.txt

## Step 3: Test with existing function

## Step 4: Document in operator registry
```

> **Would this be valuable, or is it obvious from the pattern?**

---

## ⚡ Section 7: Performance and Edge Cases

### Question 7.1: Performance Impact

The operator-based system has O(n × m) complexity:
- n = number of dict items
- m = number of registered operators

For typical usage (n=3-5, m=20), this is ~60-100 comparisons.

> **Is this acceptable, or should I optimize?**

Potential optimizations:
- Use hash map instead of linear search
- Sort operators by frequency
- Early exit after match

> **My assumption:** Current performance is fine, no optimization needed in Weeks 7-8.

### Question 7.2: Error Handling

What should happen when:

**Case A: Unknown parameter in dict**

```python
PMP.function(mesh, {"unknown_param": value})
```

- Option 1: Silently ignore (current behavior)
- Option 2: Warning message
- Option 3: Raise exception

**Case B: Wrong type for parameter**

```python
PMP.function(mesh, {"geom_traits": "not_a_kernel"})  # String instead of Kernel
```

- Option 1: `py::cast` throws exception (current)
- Option 2: Custom error message

**Case C: Missing required parameter**

```python
# If some parameters are required but not provided
```

- Option 1: CGAL handles it (current)
- Option 2: Validate in Python

> **What's your preference for Weeks 7-8? My plan is Option 1 for all (keep current behavior), defer better error handling to Weeks 5-6 (safety).**

---

## 🔗 Section 8: Integration with Existing Code

### Question 8.1: Backwards Compatibility

Some PMP functions already bound might use the old switch-based parser.

**Should I:**
- **Option A:** Migrate all existing functions to operators in Weeks 7-8
- **Option B:** Only new functions use operators, old ones stay as-is
- **Option C:** Gradual migration (start with most-used functions)

> **My assumption:** Option C — Migrate high-priority functions first.

### Question 8.2: Repository During GSoC

Your email mentioned:
> "Eventually, you will be working in one specific repo., which I'll provide."

**Will this be:**
- A new branch in the main Bitbucket repo?
- A separate staging repo?
- Direct commits to main?

> Just want to clarify workflow for when GSoC starts. For now, all my research stays in my GitHub prep repo.

---

## 📐 Section 9: Scope Clarification for Weeks 7-8

### Question 9.1: Deliverables Checklist

Based on the proposal timeline, Weeks 7-8 deliverables are:

My understanding:
- [ ] 15-20 operator structs implemented (`Named_parameter_*.hpp` files)
- [ ] Bind 5-7 new PMP functions using these operators
- [ ] Test suite for parameter handling
- [ ] Documentation for each operator
- [ ] Contributor guide for future operators

> **Is this the complete scope, or am I missing something?**

### Question 9.2: Which PMP Functions to Bind?

**Which specific PMP functions should I prioritize for binding in Weeks 7-8?**

My shortlist (based on doc frequency + complexity):
1. `compute_vertex_normals()` — Already has binding, extend with operators
2. `smooth_shape()` — Multiple parameters
3. `fair()` — Multiple parameters
4. `isotropic_remeshing()` — Complex, 7+ parameters (maybe Week 8)
5. 3-4 simpler functions for testing

> **Does this list make sense?**

---

## 🤔 Section 10: Final Questions

### Question 10.1: Anything I'm Missing?

After studying the architecture for 2 hours, is there any aspect of Named Parameters I haven't considered?

**Potential blind spots:**
- Property map lifetime management?
- Thread safety (probably not relevant)?
- Python GIL handling?
- Memory ownership issues?

### Question 10.2: Early Implementation

**Would it be valuable for me to implement 1-2 operators NOW (before GSoC acceptance) as proof-of-concept?**

**Pros:**
- Demonstrates I can execute
- Validates my understanding
- Shows initiative

**Cons:**
- Might be premature
- Could create merge conflicts later
- Should wait for GSoC acceptance

> **Your preference?** My current plan is to wait until GSoC starts (May), just document deeply now.

---

## 📋 Summary of Key Questions

### Critical (need for Week 7-8 planning):

1. Which 15-20 operators to prioritize?
2. Is multi-parameter handling already solved by chaining?
3. Property map binding strategy (explicit vs automatic)?
4. Which PMP functions to bind first?

### Important (affect implementation approach):

5. Migration strategy (switch-based → operator-based)?
6. Testing levels required?
7. Error handling approach?

### Nice to have (can decide during GSoC):

8. Docstring format for Named Parameters?
9. Contributor guide needed?
10. Early proof-of-concept valuable?

---

## 📝 Closing Notes

| Metric | Value |
|--------|-------|
| Time invested | 2+ hours analyzing architecture |
| Confidence level | High — I understand the pattern and can execute in Weeks 7-8 |
| Blockers | None — just need answers to prioritize correctly |

**Next steps after your response:**
1. Finalize implementation plan for Weeks 7-8
2. Create detailed task breakdown (Day 1-14)
3. Prepare workspace and tooling
4. Document operator creation workflow

Thank you for the excellent architecture you've built. The template system is elegant and I'm excited to complete the operator implementations during GSoC.

---

**End of Questions Document**  
*Ready for Jan 23 email (after receiving your feedback)*