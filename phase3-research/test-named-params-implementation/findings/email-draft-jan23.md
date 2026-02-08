# 📧 Email Draft for Efi — January 23, 2026

**Subject:** GSoC 2026 — Named Parameters Deep Dive + Implementation Attempt + Questions

---

Hi Efi,

Hope you're doing well! I wanted to share some significant progress I've made over the past week on understanding the Named Parameters architecture.

---

## 📌 What I've Accomplished

Over the last 6 days, I spent **~12 hours** deeply analyzing the Named Parameters implementation:

### 1. Complete Architecture Analysis

I studied the entire system:
- `export_pmp_normal_computation.cpp` — Your `compute_face_normals()` implementation
- `named_parameter_applicator.hpp` — The recursive variadic template processor
- `Named_parameter_wrapper.hpp` — The `std::apply`-based wrapper
- `Named_parameter_geom_traits.hpp` — Example operator pattern
- `pmp_np_parser.hpp` — The legacy switch-based system

**Key insight:** You've built a sophisticated operator-based system that recursively processes Python dict items and builds CGAL compile-time parameter chains. The architecture is elegant and fully reusable.

I documented the complete flow:

```
Python dict → named_parameter_applicator → Operator matching →
Parameter chaining → Named_parameter_wrapper → CGAL function call
```

### 2. Identified the Migration Pattern

I noticed `pmp_np_parser.hpp` has ~20 parameters commented out, which suggests you're migrating from the switch-based system to the operator-based system. This makes sense because:
- Operator system is more maintainable
- Easier to extend (just add new operator struct)
- Better separation of concerns
- Follows modern C++ template patterns

### 3. Multi-Parameter Question Answered (I think!)

For your note about "*some functions accept MORE than one NamedParameter*" — I believe the current `named_parameter_applicator` already handles this through variadic template recursion:

```cpp
// Each dict item processed in sequence
// Builds chain: np.param1(v1).param2(v2).param3(v3)
named_parameter_applicator(wrapper, np, params, op1, op2, op3, ...);
```

Is this the extension method you mentioned, or is there additional complexity I'm missing?

### 4. Created Detailed Implementation Plan

I broke down Weeks 7-8 into a 14-day plan:
- **Days 1-7:** Implement 16 core operators + bind 2 functions
- **Days 8-14:** Complete 20 operators + bind 5 more functions + documentation
- **Total:** 20 operators, 7 PMP functions, comprehensive tests

All documented with daily tasks, time estimates, and risk management.

---

## 🔬 Proof-of-Concept Implementation (NEW — Jan 17)

To validate my understanding, I implemented 2 operators in a feature branch:

| Detail | Value |
|--------|-------|
| **Branch** | `feature/named-params-operators-poc` |
| **Commit** | `eb5a9e39` (2 files, 60 lines) |

### Files Created

1. `Named_parameter_vertex_point_map.hpp` — Following your exact pattern
2. `Named_parameter_vertex_normal_map.hpp` — Following your exact pattern

Both operators are **structurally correct** — identical to your `Named_parameter_verbose.hpp` style.

### The Challenge I Discovered

When I attempted to integrate them into `compute_vertex_normals()`, I hit this compilation error:

```
error: no type named 'reference' in 'boost::property_traits<nanobind::handle>'
```

**This is exactly why you allocated 2 weeks for this task!**

### What This Taught Me

| Before | After |
|--------|-------|
| "Write 20 operators, bind 7 functions, done in 2 weeks" | Operators are easy (30 lines, 30 minutes each) |
| | **Property map type resolution is the actual challenge** |
| | `nanobind::handle` → `Property_map<Vd, Point_3>` requires sophisticated type bridge |
| | This is THE hard problem, not just "writing more operators" |

### The Type Resolution Problem

```cpp
// Python side
{"vertex_point_map": vpm}  // Python object (nanobind::handle)

// CGAL expects
Property_map<Vertex_index, Point_3>  // Compile-time type

// How to bridge?
```

**Four possible approaches I identified:**

| Option | Approach | Challenge |
|--------|----------|-----------|
| A | Explicit casting in operator | Mesh type unknown at operator level |
| B | Template specialization per mesh type | Explosion of combinations |
| C | Defer casting to wrapper | How to extract from compiled np chain? |
| D | Python-side property map binding first | Still need nanobind type recognition |

### Why This Discovery is VALUABLE

- ✅ Shows I can quickly identify the real technical challenge
- ✅ Demonstrates I won't waste time implementing wrong approach
- ✅ Proves I understand the depth of the problem
- ✅ Ready for intelligent discussion about solutions

I've documented the complete challenge analysis in:  
`cgal-gsoc-2026-prep/phase3-research/proof-of-concept-operators/PROPERTY_MAP_CHALLENGE.md`

---

## ⚠️ CRITICAL Question (Based on Implementation Attempt)

### Q0: Property Map Type Resolution Strategy ⭐ MOST IMPORTANT

When I tried integrating the operators, CGAL's `compute_vertex_normals()` fails because:
- It calls `get(vpmap, vertex)` internally
- Requires `boost::property_traits<VertexPointMap>::reference`
- `nanobind::handle` doesn't satisfy this

**Which approach should I use in Weeks 7-8?**

**Option A:** Explicit type casting in operators

```cpp
auto operator()(NamedParameters& np, Value& value) const {
  using Vpm = /* HOW TO DETERMINE? Surface_mesh or Polyhedron? */;
  return np.vertex_point_map(py::cast<Vpm>(value));
}
```

**Option B:** Template specialization per mesh

```cpp
template <typename Mesh>
struct Named_parameter_vertex_point_map { /* mesh-specific casting */ };
```

**Option C:** Python-side property map binding first

```python
vpm = mesh.points()  # Bind this first, returns proper Property_map
PMP.function(mesh, {"vertex_point_map": vpm})
```

**Option D:** Something else I haven't considered?

> **This is THE blocker for integration. The operators are trivial once this is solved.**

---

## ❓ Key Questions for Week 7-8 Planning

### Priority Questions:

**Q1: Operator Priority Order**

Based on frequency in PMP functions, I identified this priority:
1. `vertex_point_map` (used in ~30 functions)
2. `vertex_normal_map` (~15 functions)
3. `face_index_map` (~20 functions)
4. `vertex_index_map` (~12 functions)
5. `edge_is_constrained_map`

Does this align with your priorities, or should I adjust based on which functions you want exposed first?

**Q2: Property Map Strategy**

For property maps like `vertex_point_map`, should I:
- **Option A:** Bind property map creation functions first (e.g., `mesh.points()`)
- **Option B:** Let users pass `None`, use defaults internally
- **Option C:** Automatic — get property maps internally

My guess is Option A (explicit), but wanted to confirm.

**Q3: Which PMP Functions to Bind?**

For the 5-7 functions in Weeks 7-8, which should I prioritize? My shortlist:
1. `compute_vertex_normals()` — Extend existing binding
2. `smooth_shape()` — Multiple parameters
3. `fair()` — Multiple parameters
4. `triangulate_faces()` — Simpler, good for testing
5. `isotropic_remeshing()` — Most complex (7+ parameters)

**Q4: Testing Scope**

Should tests cover:
- **Level 1:** Operator in isolation ✓
- **Level 2:** Multiple operators (chaining) ✓
- **Level 3:** Full function integration ✓
- **Level 4:** Error cases (defer to Weeks 11-12?) ✓

### Technical Clarification:

**Q5: Example Multi-Parameter Function**

Could you point me to a specific CGAL PMP function that uses multiple Named Parameters? I want to ensure I understand the pattern correctly before implementing.

Options I found: `isotropic_remeshing()`, `smooth_mesh()`, `fair_mesh()`.

**Q6: Type Casting Approach**

Should I follow the `Named_parameter_geom_traits` pattern for all operators?

```cpp
return np.param_name(py::cast<CppType>(value));
```

Or do some require template specialization for different mesh types?

---

## 📂 Documentation Created

All my research is organized in the prep repository:
- `NAMED_PARAMS_COMPLETE_ANALYSIS.md` (3,500+ lines) — Complete architecture breakdown
- `implementation-plan.md` (1,200+ lines) — Day-by-day plan for Weeks 7-8
- `questions-for-efi.md` (900+ lines) — Comprehensive question list
- `PROPERTY_MAP_CHALLENGE.md` (NEW) — Type resolution problem analysis

**Repository:** https://github.com/UtkarsHMer05/cgal-gsoc-2026-prep/tree/main/phase3-research/test-named-params-implementation

---

## 💪 What This Demonstrates

This deep dive shows I can:
- ✅ Reverse-engineer complex C++ template systems
- ✅ Understand CGAL's architecture patterns
- ✅ Plan large-scale implementations systematically
- ✅ Document comprehensively for future contributors
- ✅ Ask specific, technical questions (not just "how do I do this?")
- ✅ **Quickly identify the real technical blockers** (NEW)
- ✅ **Attempt implementation to validate understanding** (NEW)

Ready to execute in Weeks 7-8 once GSoC starts.

---

## 🚀 Next Steps

If you have time to answer the 7 priority questions above (especially Q0!), it would help me finalize:
1. **Type resolution strategy for property maps** ⭐
2. Exact operator priority list (which 15-20)
3. Property map binding strategy
4. Target PMP functions for Weeks 7-8
5. Any architecture aspects I'm missing

No rush at all — I know January is busy. Just want to ensure my understanding is correct before GSoC selection.

In the meantime, I'm continuing to:
- Study more PMP functions for patterns
- Document common parameter combinations
- Prepare visual architecture diagrams

---

## 🔗 Links

**Updated Proposal:** https://docs.google.com/document/d/1ZM5TAC5rkKm3xmntMy7ZzfwnKFbS7yrk4IlOB5_FW_M/edit?usp=sharing

**Technical Research:** https://github.com/UtkarsHMer05/cgal-gsoc-2026-prep

---

Thanks for building such an elegant system. The template metaprogramming pattern you've created is exactly the kind of modern C++ architecture I want to learn more about during GSoC.

Best,  
**Utkarsh**

---

*P.S. If there's any specific PMP function or operator you'd like me to study in more detail before the GSoC announcement, let me know. I'm happy to do additional research to strengthen the proposal.*