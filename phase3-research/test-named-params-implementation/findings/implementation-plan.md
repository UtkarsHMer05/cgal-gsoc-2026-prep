# 📋 Named Parameters Implementation Plan — GSoC Weeks 7-8

**Duration:** 14 days (June 15-28, 2026)  
**Estimated Hours:** 80-90 hours (6-7 hours/day)  
**Complexity:** 🔴 HIGH (Efi allocated 2 weeks)  
**Goal:** Implement 15-20 Named Parameter operators and bind 5-7 PMP functions

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Week 7: Core Operators](#-week-7-core-operators-days-1-7)
- [Week 8: Advanced Functions](#-week-8-advanced-functions--polish-days-8-14)
- [Metrics & Success Indicators](#-metrics--success-indicators)
- [Risk Management](#-risk-management)
- [Templates & Testing](#-operator-implementation-template)

---

## 🎯 Overview

### The Challenge

Bridge CGAL's compile-time Named Parameters with Python's runtime dictionaries using Efi's operator-based template system.

### Success Criteria

| Criteria | Target | Status |
|----------|--------|--------|
| Operator structs implemented | 15-20 | ⏳ |
| PMP functions bound | 5-7 | ⏳ |
| Test coverage | 80%+ | ⏳ |
| Documentation complete | ✓ | ⏳ |
| Contributor guide written | ✓ | ⏳ |

---

## 📅 Week 7: Core Operators (Days 1-7)

### Day 1 (June 15) — Infrastructure Setup
**Time:** 6 hours  
**Goal:** Prepare workspace and implement first operator as template

#### Morning (3 hours)
- [ ] Create branch: `feature/named-parameters-operators`
- [ ] Set up file structure:
  ```
  include/CGALPY/
  ├── operators/
  │   ├── Named_parameter_vertex_point_map.hpp
  │   ├── Named_parameter_vertex_normal_map.hpp
  │   └── ... (15-20 files)
  └── operator_registry.hpp
  ```
- [ ] Update CMakeLists.txt to include operator files
- [ ] Study existing `Named_parameter_geom_traits.hpp` as reference

#### Afternoon (3 hours)
- [ ] Implement **Operator #1:** `Named_parameter_vertex_point_map`
  - Write operator struct (~30 lines)
  - Add inline documentation
  - Identify correct type casting approach
- [ ] Create simple test binding to verify it works
- [ ] Document any issues or questions
- [ ] **Commit:** `Add vertex_point_map operator (template)`

**Deliverable:** First working operator + clean file structure

---

### Day 2 (June 16) — High-Priority Operators (Batch 1)
**Time:** 7 hours  
**Goal:** Implement 4 critical operators

#### Morning (4 hours)
- [ ] **Operator #2:** `Named_parameter_vertex_normal_map`
- [ ] **Operator #3:** `Named_parameter_face_index_map`
- [ ] **Operator #4:** `Named_parameter_vertex_index_map`

**Each operator (~60 min):**
1. Create `.hpp` file
2. Write struct with `m_name` and `operator()`
3. Add docstring comments
4. Quick compile check

#### Afternoon (3 hours)
- [ ] **Operator #5:** `Named_parameter_edge_is_constrained_map`
- [ ] Create test file: `test_operators_batch1.py`
- [ ] Test each operator with simple PMP function
- [ ] Document operator registry (which operator for which parameter)
- [ ] **Commit:** `Add 4 high-priority operators`

**Deliverable:** 5 operators total (including Day 1)

---

### Day 3 (June 17) — High-Priority Operators (Batch 2)
**Time:** 7 hours  
**Goal:** Complete remaining high-priority operators

#### Morning (4 hours)
- [ ] **Operator #6:** `Named_parameter_vertex_is_constrained_map`
- [ ] **Operator #7:** `Named_parameter_halfedge_index_map`
- [ ] **Operator #8:** `Named_parameter_edge_index_map`
- [ ] **Operator #9:** `Named_parameter_face_patch_map`

#### Afternoon (3 hours)
- [ ] **Operator #10:** `Named_parameter_point_to_vertex_map`
- [ ] Test all 10 operators together (parameter chaining)
- [ ] Fix any compilation issues
- [ ] Update documentation
- [ ] **Commit:** `Complete 10 core operators`

**Deliverable:** 10 operators implemented and tested

---

### Day 4 (June 18) — First Function Binding
**Time:** 6 hours  
**Goal:** Bind `compute_vertex_normals()` with operators

#### Morning (3 hours)
- [ ] Study current `compute_vertex_normals()` binding
- [ ] Migrate from switch-based to operator-based
- [ ] Create function-specific wrapper struct
- [ ] Register 3-4 relevant operators

#### Afternoon (3 hours)
- [ ] Test Python binding:
  ```python
  mesh = create_test_mesh()
  vnormals = mesh.add_property_map("v:normals")
  PMP.compute_vertex_normals(mesh, vnormals, {
      "vertex_point_map": mesh.points(),
      "geom_traits": kernel
  })
  ```
- [ ] Verify parameter chaining works
- [ ] Write comprehensive test cases
- [ ] **Commit:** `Migrate compute_vertex_normals to operators`

**Deliverable:** First complete function binding with Named Parameters

---

### Day 5 (June 19) — Medium-Priority Operators
**Time:** 7 hours  
**Goal:** Implement remaining operators

#### Morning (4 hours)
- [ ] **Operator #11:** `Named_parameter_vertex_mean_curvature_map`
- [ ] **Operator #12:** `Named_parameter_vertex_incident_patches_map`
- [ ] **Operator #13:** `Named_parameter_face_normal_map`
- [ ] **Operator #14:** `Named_parameter_do_project` (boolean parameter)

#### Afternoon (3 hours)
- [ ] **Operator #15:** `Named_parameter_number_of_iterations` (int parameter)
- [ ] **Operator #16:** `Named_parameter_use_safety_constraints` (boolean)
- [ ] Test non-map parameters (booleans, ints)
- [ ] **Commit:** `Add medium-priority operators`

**Deliverable:** 16 operators total

---

### Day 6 (June 20) — Second Function Binding
**Time:** 7 hours  
**Goal:** Bind `smooth_shape()` with multiple parameters

#### Morning (3 hours)
- [ ] Study `smooth_shape()` signature:
  ```cpp
  smooth_shape(mesh, time, 
               parameters::vertex_point_map(vpm)
                         .edge_is_constrained_map(ecm)
                         .number_of_iterations(100))
  ```
- [ ] Create binding with 5+ operators
- [ ] Test parameter chaining

#### Afternoon (4 hours)
- [ ] Write Python test:
  ```python
  PMP.smooth_shape(mesh, 0.01, {
      "vertex_point_map": vpm,
      "edge_is_constrained_map": ecm,
      "number_of_iterations": 50
  })
  ```
- [ ] Test all parameter combinations
- [ ] Handle missing/optional parameters
- [ ] Document parameter requirements
- [ ] **Commit:** `Add smooth_shape with multi-parameter support`

**Deliverable:** Second function binding with complex parameters

---

### Day 7 (June 21) — Week 7 Review & Documentation
**Time:** 6 hours  
**Goal:** Consolidate Week 7 work

#### Morning (3 hours)
- [ ] Code review of all 16 operators
- [ ] Ensure consistent style and documentation
- [ ] Fix any TODO comments
- [ ] Run full test suite

#### Afternoon (3 hours)
- [ ] Write operator registry documentation:
  - Which operator for which parameter
  - Type requirements for each
  - Common usage patterns
- [ ] Create troubleshooting guide
- [ ] Update proposal with actual progress
- [ ] Prepare Week 8 task list
- [ ] **Commit:** `Week 7 complete - 16 operators + 2 functions`

### 📊 Week 7 Checkpoint

| Metric | Target | Actual |
|--------|--------|--------|
| Operators | 16/20 (80%) | ⏳ |
| Functions | 2/7 (29%) | ⏳ |
| On track? | YES | ⏳ |

---

## 📅 Week 8: Advanced Functions & Polish (Days 8-14)

### Day 8 (June 22) — Remaining Operators + Function #3
**Time:** 7 hours  
**Goal:** Complete operator set, bind third function

#### Morning (3 hours)
- [ ] **Operator #17:** `Named_parameter_visitor` (complex type)
- [ ] **Operator #18:** `Named_parameter_density_control_factor` (double)
- [ ] **Operator #19:** `Named_parameter_protect_constraints` (boolean)
- [ ] **Operator #20:** `Named_parameter_relaxation_steps` (int)

#### Afternoon (4 hours)
- [ ] Bind `fair()` function with operators
- [ ] Test with various parameter combinations
- [ ] **Commit:** `Complete 20 operators + fair() binding`

**Deliverable:** 20 operators complete, 3 functions bound

---

### Day 9 (June 23) — Functions #4 and #5
**Time:** 7 hours  
**Goal:** Bind two simpler PMP functions

#### Morning (3.5 hours)
- [ ] **Function #4:** `triangulate_faces()`
  - Simpler signature (2-3 parameters)
  - Good for testing basic operators

#### Afternoon (3.5 hours)
- [ ] **Function #5:** `refine_mesh()`
  - Medium complexity
  - Test edge case handling
- [ ] **Commit:** `Add triangulate_faces and refine_mesh`

**Deliverable:** 5 functions bound

---

### Day 10 (June 24) — Complex Function: isotropic_remeshing()
**Time:** 7 hours  
**Goal:** Bind most complex function (7+ parameters)

#### Morning (4 hours)
- [ ] Study `isotropic_remeshing()` signature
- [ ] Identify all 7+ Named Parameters needed
- [ ] Create comprehensive wrapper
- [ ] Handle parameter validation

#### Afternoon (3 hours)
- [ ] Test with minimal parameters (defaults)
- [ ] Test with all parameters specified
- [ ] Test parameter conflicts/incompatibilities
- [ ] Document parameter dependencies
- [ ] **Commit:** `Add isotropic_remeshing - most complex binding`

**Deliverable:** 6 functions bound, including most complex one

---

### Day 11 (June 25) — Function #7 + Error Handling
**Time:** 6 hours  
**Goal:** Complete function quota, improve robustness

#### Morning (3 hours)
- [ ] **Function #7:** Choose based on utility
  - Options: `lloyd_optimize()`, `angle_and_area_smoothing()`, `extrude_mesh()`
  - Pick one with different parameter pattern

#### Afternoon (3 hours)
- [ ] Add basic error handling:
  - Invalid parameter types
  - Missing required parameters
  - Helpful error messages
- [ ] Test error cases for all 7 functions
- [ ] **Commit:** `Complete 7 functions + error handling`

**Deliverable:** 7 functions bound with error handling

---

### Day 12 (June 26) — Comprehensive Testing
**Time:** 7 hours  
**Goal:** Test all combinations and edge cases

#### Morning (4 hours)
- [ ] Create test matrix:
  - Each operator × 2-3 functions = 30-40 tests
  - Parameter chaining (2-param, 3-param, 5-param)
  - Type validation tests
  - Default parameter tests

#### Afternoon (3 hours)
- [ ] Run full test suite
- [ ] Fix any failures
- [ ] Measure test coverage (aim for 80%+)
- [ ] Document test results
- [ ] **Commit:** `Comprehensive test suite for Named Parameters`

**Deliverable:** 80%+ test coverage

---

### Day 13 (June 27) — Documentation & Contributor Guide
**Time:** 7 hours  
**Goal:** Complete documentation for future developers

#### Morning (4 hours)
- [ ] Write contributor guide:
  ```markdown
  # Adding a New Named Parameter Operator
  
  ## Step 1: Create operator file
  ## Step 2: Implement operator struct
  ## Step 3: Register with applicator
  ## Step 4: Test with existing function
  ## Step 5: Document in registry
  ```
- [ ] Document each operator:
  - Parameter name (Python dict key)
  - Expected type
  - Common use cases
  - Example usage

#### Afternoon (3 hours)
- [ ] Create visual diagrams:
  - Parameter flow (Python → C++)
  - Operator chaining visualization
  - Error handling flowchart
- [ ] Write troubleshooting guide
- [ ] **Commit:** `Complete Named Parameters documentation`

**Deliverable:** Full documentation package

---

### Day 14 (June 28) — Final Review & Integration
**Time:** 6 hours  
**Goal:** Polish and prepare for merge

#### Morning (3 hours)
- [ ] Code review entire implementation
- [ ] Ensure consistent naming conventions
- [ ] Remove debug code and TODOs
- [ ] Update CHANGELOG
- [ ] Verify all commits have good messages

#### Afternoon (3 hours)
- [ ] Create pull request with detailed description
- [ ] Write summary for Weeks 7-8 report:
  - What was implemented
  - Challenges encountered
  - Lessons learned
  - Future improvements
- [ ] Update Wiki with progress
- [ ] Prepare demo for Efi
- [ ] **Commit:** `Weeks 7-8 complete - Named Parameters system`

**Deliverable:** Complete, polished implementation ready for review

---

## 📊 Metrics & Success Indicators

### Code Metrics

| Metric | Target |
|--------|--------|
| Operators Implemented | 20/20 (100%) |
| Functions Bound | 7/7 (100%) |
| Lines of Code | 600-800 (operators + bindings + tests) |
| Test Coverage | 80%+ |
| Documentation | 2000+ lines (guides + API docs) |

### Quality Metrics

| Metric | Target |
|--------|--------|
| Compilation | Clean (no warnings) |
| Tests | All passing |
| Style | Consistent with CGAL codebase |
| Performance | No measurable overhead vs direct calls |

### Time Tracking

| Week | Hours |
|------|-------|
| Week 7 | 46 hours (operators + 2 functions) |
| Week 8 | 40 hours (5 functions + polish) |
| **Total** | **86 hours** (within 90-hour estimate) |

---

## ⚠️ Risk Management

### Potential Blockers

| Risk | Probability | Impact | Mitigation | Fallback |
|------|-------------|--------|------------|----------|
| Type casting complexity | MEDIUM | HIGH | Study existing operators first, ask Efi if stuck | Implement simpler operators first, defer complex ones |
| Property map binding issues | HIGH | MEDIUM | Work with Efi on property map strategy first | Use explicit property map parameters instead |
| Parameter chaining bugs | MEDIUM | MEDIUM | Extensive testing on Day 12 | Simplify applicator if complex chaining fails |
| Time overrun | LOW | HIGH | Prioritize critical operators, defer nice-to-haves | Complete 15 operators + 5 functions minimum |

---

## 🔧 Operator Implementation Template

### File Structure

```cpp
// Named_parameter_PARAM_NAME.hpp

#ifndef CGALPY_NAMED_PARAMETER_PARAM_NAME_HPP
#define CGALPY_NAMED_PARAMETER_PARAM_NAME_HPP

#include <string>
#include <nanobind/nanobind.h>
// Include CGAL types if needed

namespace py = nanobind;

namespace CGALPY {

/*! Operator for PARAM_NAME Named Parameter
 *
 * Python usage: {"param_name": value}
 * 
 * Type: Description of expected type
 * Used in: List of functions using this parameter
 */
struct Named_parameter_PARAM_NAME {
  const std::string m_name = "param_name";
  
  template <typename NamedParameters, typename Value>
  auto operator()(NamedParameters& np, Value& value) const {
    // Type casting
    auto cpp_value = py::cast<CppType>(value);
    
    // Chain parameter
    return np.param_name(cpp_value);
  }
};

}

#endif
```

### Time per Operator

| Type | Time |
|------|------|
| Simple (boolean, int) | 30-40 minutes |
| Medium (property maps) | 45-60 minutes |
| Complex (functors, visitors) | 60-90 minutes |

---

## 🧪 Testing Strategy

### Test Levels

**Level 1: Operator Unit Tests**
```python
def test_vertex_point_map_operator():
    mesh = Surface_mesh()
    vpm = mesh.points()
    result = PMP.function(mesh, {"vertex_point_map": vpm})
    assert result is not None
```

**Level 2: Parameter Chaining Tests**
```python
def test_multiple_parameters():
    result = PMP.function(mesh, {
        "vertex_point_map": vpm,
        "vertex_normal_map": vnm,
        "geom_traits": kernel
    })
    # Verify all parameters applied
```

**Level 3: Function Integration Tests**
```python
def test_smooth_shape_with_params():
    mesh = load_mesh("cube.off")
    PMP.smooth_shape(mesh, 0.01, {
        "vertex_point_map": mesh.points(),
        "edge_is_constrained_map": ecm,
        "number_of_iterations": 100
    })
    # Verify mesh was smoothed
```

**Level 4: Error Handling Tests**
```python
def test_invalid_parameter_type():
    with pytest.raises(TypeError):
        PMP.function(mesh, {"vertex_point_map": "not_a_map"})
```

---

## ✅ Success Definition

Weeks 7-8 considered **successful** if:

- ✅ 15-20 operators implemented and tested
- ✅ 5-7 PMP functions bound with Named Parameters
- ✅ 80%+ test coverage
- ✅ Complete documentation
- ✅ Code ready for merge
- ✅ Zero breaking changes to existing code
- ✅ Efi approves implementation approach

**Ideal outcome:**
- All 20 operators done
- All 7 functions bound
- Comprehensive tests
- Excellent documentation
- Clean, maintainable code

---

**End of Implementation Plan**  
**Status:** Ready for execution (GSoC Weeks 7-8)  
**Next Review:** June 21, 2026 (end of Week 7)