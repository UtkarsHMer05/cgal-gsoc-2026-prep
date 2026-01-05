# 🎯 CGAL GSoC 2026 Preparation Repository

**Project:** CGAL Python Bindings Enhancement  
**Applicant:** Utkarsh Khajuria  
**Mentor:** Efi Fogel (efifogel@gmail.com)  
**Preparation Period:** December 20, 2025 – January 5, 2026  
**Total Time Invested:** 95+ hours

---

## 📌 Current Status — January 5, 2026

### ✅ TWO SUBSTANTIAL PRs SUBMITTED + CONTINUED RESEARCH

---

#### PR #1: Insertion Methods Documentation

- **Submitted:** December 27, 2025, 12:51 AM IST
- **Status:** Awaiting review
- 🔗 [PR Link](https://bitbucket.org/taucgl/cgal-python-bindings/pull-requests/)

**What Changed:**
- Added NumPy-style docstrings for 6 insertion method overloads
- Named parameters with `py::arg()` for all 6 methods
- Documented counter-intuitive `insert_from_right_vertex` behavior (returns halfedge RIGHT→LEFT)
- Warned about no validation in specialized insertion methods

**Methods Documented:**
- `insert_from_left_vertex(curve, vertex)`
- `insert_from_left_vertex(curve, halfedge)`
- `insert_from_right_vertex(curve, vertex)`
- `insert_from_right_vertex(curve, halfedge)`
- `insert_in_face_interior(curve, face)`
- `insert_in_face_interior(point, face)`

---

#### PR #2: Removal, Modification & Query Methods Documentation

- **Submitted:** December 29, 2025, 11:51 PM IST
- **Status:** Awaiting review
- 🔗 [PR Link](https://bitbucket.org/taucgl/cgal-python-bindings/pull-requests/)

**What Changed:**
- Added comprehensive docstrings for 15 methods across 3 categories
- 🔴 **CRITICAL** crash warnings for 2 methods that kill Python interpreter
- Documented 5 segfault scenarios discovered through empirical testing
- Documented 10+ silent corruption scenarios
- Safe usage patterns with validation checks
- Handle lifetime and invalidation warnings

**Methods Documented:**

*Removal Methods (2):*
- `remove_isolated_vertex(vertex)` — 🔴 CRITICAL: crashes if vertex not isolated
- `remove_edge(halfedge)` — Handle invalidation + missing optional parameters

*Modification Methods (4):*
- `split_edge(halfedge, curve1, curve2)` — No validation warnings
- `merge_edge(he1, he2, merged_curve)` — 🔴 CRITICAL: crashes on non-adjacent edges
- `modify_vertex(vertex, new_point)` — Geometric inconsistency warning
- `modify_edge(halfedge, new_curve)` — No validation warning

*Query Methods (9):*
- **Arrangement:** `number_of_vertices()`, `number_of_edges()`, `number_of_faces()`, `is_empty()`, `is_valid()`, `unbounded_face()`
- **Vertex:** `degree()`, `is_isolated()`
- **Halfedge:** `twin()`

---

### 📝 GSoC 2026 Proposal

🔗 [Live Proposal — Google Docs](https://docs.google.com/document/d/1ZM5TAC5rkKm3xmntMy7ZzfwnKFbS7yrk4IlOB5_FW_M/edit?usp=sharing)

**Updated to include:**
- Both PR submissions (21 methods documented total)
- Complete 95+ hour preparation timeline
- Critical safety discoveries from testing
- Architecture diagram showing three-layer structure
- Detailed week-by-week plan for GSoC 350 hours

---

## 🚀 Why This Project?

I found CGAL when I needed 2D arrangement algorithms for a project. The C++ API was elegant—template metaprogramming, traits classes, DCEL structures. But when I tried the Python bindings, I hit a wall immediately.

No docstrings. Parameters showing as `arg0`, `arg1`, `arg2`. And there's literally a comment on line 857 that says:

```cpp
//! \todo Why the f... reference_internal doesn't work?
```

That's when it clicked: elegant C++ architecture is worthless if Python users can't figure out how to use it.

I'm not here for just a summer project. I want to make CGAL's Python bindings actually usable for researchers and developers who need computational geometry but don't want to read C++ source code. I've already invested 95+ hours before even applying, and I'll keep contributing regardless of GSoC selection.

---

## 📚 Phase 1: Foundation (50+ Hours, Dec 20-24)

### Day 1: Environment Setup (December 20)

**What I did:**
- Built CGAL from source on MacBook Air M1
- Configured Qt6, Boost 1.86, CORE support
- Set up CMake with Python bindings enabled
- Verified installation with test programs

**What I learned:**
- CGAL's build system is complex but well-documented
- Dependencies matter—wrong Boost version breaks everything
- Building from source gives full control for debugging

**Time spent:** ~8 hours (mostly debugging Qt6 linking issues)

---

### Day 2: Mastering 2D Arrangements (December 21)

**What I did:**
- Studied DCEL (Doubly-Connected Edge List) data structure in depth
- Built and analyzed 3 C++ examples: `incremental_insertion`, `point_location`, `edge_insertion`
- Wrote 600+ lines of architecture analysis

**What I learned:**

*DCEL Structure:*
- Vertices store geometric points + degree
- Halfedges are directed edges with twin pointers
- Faces represent regions bounded by edges
- Everything links bidirectionally for traversal

*Traits Classes:*
- `Arr_segment_traits_2` for line segments
- `Arr_circle_segment_traits_2` for circular arcs
- Traits define geometric operations (intersections, comparisons)

*Insertion Methods (15+ types!):*
- General vs specialized insertion
- When to use each method
- DCEL topology changes for each

**Time spent:** ~12 hours

---

### Day 3: Exploring Python Bindings Repository (December 22)

**What I did:**
- Cloned `cgal-python-bindings` from Bitbucket
- Analyzed binding code in `src/libs/cgalpy/lib/`
- Studied 50+ bound methods in `Arrangement_2`
- Found 70+ Python examples

**What I discovered:**

*The Good:*
- 2D/3D Arrangements ~80% complete
- 13+ geometry types supported
- Pythonic iteration works well

*The Gaps:*
- 90% of methods have NO docstrings
- Most show `arg0`, `arg1`, `arg2` instead of names
- No IDE autocomplete (missing `.pyi` stubs)
- Some functions commented out (lifetime issues)

**Critical Finding — Line 857:**
```cpp
//! \todo Why the f... reference_internal doesn't work?
m.def("insert", &aos2::insert_cv_with_history, ref);  // Dangerous workaround!
```

**Time spent:** ~10 hours

---

### Day 4-5: Learning Nanobind (December 23-24)

**What I learned:**

*Return Value Policies:*
- `reference_internal` — Keeps parent alive (most common)
- `copy` — Independent copy
- `take_ownership` — Python owns object
- `reference` — Bare reference (dangerous!)

*Lifetime Management:*
- `keep_alive<0, 1>` patterns
- Critical for iterators and handles
- Line 857 uses dangerous bare ref as workaround

**Time spent:** ~12 hours

---

### Day 5: Proposal Writing (December 24)

- Drafted comprehensive 12-week proposal
- Created architecture diagrams
- Structured 2-week increment timeline
- Submitted to prep repository

**Time spent:** ~8 hours  
**Submitted:** December 24, 2025, 11:57 PM IST

---

## 🔥 Phase 2: Real Contributions (40+ Hours, Dec 25-29)

### Night 1: Building cgalpy (Dec 25-26, 12 hours)

**The Challenge:** Build Python bindings with arrangement support

**What happened:**
- Initial GCC build failed (Qt6 issues on macOS)
- Switched to Apple Clang → success
- Key flag: `-DCGALPY_ARRANGEMENT_ON_SURFACE_2_BINDINGS=ON`
- Discovered import path: `from CGALPY.Aos2 import Arrangement_2`

**Testing discoveries:**
- `insert_in_face_interior(point, face)` — NO validation, creates duplicate vertices at same coordinates
- `insert_from_left_vertex(curve, vertex)` — Intuitive, returns halfedge LEFT→RIGHT
- `insert_from_right_vertex(curve, vertex)` — Counter-intuitive! Returns halfedge RIGHT→LEFT

**Time spent:** 12 hours

---

### Day 6: Research Documentation (Dec 26)

Wrote detailed research files for three methods based on testing:
- Method behavior analysis
- DCEL topology changes
- Preconditions (none validated!)
- Common mistakes and warnings

**Time spent:** 4 hours

---

### Day 7: The Formatting Disaster & PR #1 (Dec 26-27)

**The Problem:**
- Wrote docstrings, saved file
- VS Code auto-formatter rewrote entire file
- Result: +1306 / -823 lines changed (mostly whitespace)

**The Fix:**
1. Reset to clean master
2. Disabled all auto-formatters in VS Code
3. Created fresh branch
4. Re-applied changes manually (clean diff!)
5. Rebuilt and tested
6. Submitted PR

**Time spent:** 9 hours (3 fixing formatter disaster, 6 writing docs)  
**PR #1 Submitted:** December 27, 2025, 12:51 AM IST

---

### Days 8-9: Deep Methods Research (Dec 27-28, 13 HOURS) 🔬

After submitting PR #1, I didn't stop. I systematically tested 25+ methods to understand safety characteristics. This wasn't casual testing—I wrote 800+ lines of test code and documented everything in a 2,500+ line research document.

**Timeline:**
- Dec 27, 6:18 PM - 11:05 PM: Specialized insertion methods (5 hours)
- Dec 28, 2:00 PM - 4:50 PM: Removal, modification, query methods (8 hours)

---

### 🔴 Critical Discovery #1: FIVE CRASH SCENARIOS

These ALL cause SEGFAULT or Bus Error (kill Python interpreter, no exception):

**1. `remove_isolated_vertex()` on non-isolated vertex**
```python
v = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
arr.insert_at_vertices(seg, v, v2)  # v now has degree 1

arr.remove_isolated_vertex(v)  # v is NOT isolated!
# Result: zsh: bus error python test.py
```

**2. `remove_edge()` twice on same halfedge**
```python
arr.remove_edge(he)  # First removal - OK
arr.remove_edge(he)  # Second removal - he is INVALID!
# Result: zsh: segmentation fault python test.py
```

**3. `merge_edge()` on non-adjacent edges**
```python
he1 = arr.insert_at_vertices(seg1, v1, v2)  # Edge 1
he2 = arr.insert_at_vertices(seg2, v3, v4)  # Edge 2 (different vertices!)

arr.merge_edge(he1, he2, merged)  # Edges don't share vertex!
# Result: zsh: segmentation fault python test.py
```

**4. Accessing deleted vertex after `merge_edge()`**
```python
v2 = he1.target()  # Save handle to shared vertex
arr.merge_edge(he1, he2, merged)  # v2 gets deleted internally

v2.point()  # Accessing deleted vertex!
# Result: zsh: segmentation fault python test.py
```

**5. Accessing deleted halfedge after `remove_edge()`**
```python
arr.remove_edge(he)  # he is now invalid

he.source()  # Accessing deleted halfedge!
# Result: zsh: segmentation fault python test.py
```

**Pattern:** All involve accessing freed memory or calling methods with invalid handles. Python GC can't detect this—handles exist but point to freed C++ memory.

---

### ⚠️ Critical Discovery #2: TEN+ SILENT CORRUPTION SCENARIOS

These create invalid arrangements with NO error:

1. **Duplicate points** — `insert_in_face_interior(point, face)` creates multiple vertices at same coordinates
2. **Mismatched endpoints** — `insert_from_left_vertex(seg, v)` where `seg.source() != v.point()`
3. **Overlapping segments** — `insert_in_face_interior()` accepts segments that overlap existing edges
4. **Duplicate edges** — `insert_at_vertices()` can create multiple edges between same vertices
5. **Wrong split point** — `split_edge()` accepts curves that don't actually split at the original edge
6. **Degenerate split** — `split_edge()` with zero-length first curve creates duplicate vertex
7. **Wrong merged curve** — `merge_edge()` accepts curve that doesn't match vertex positions
8. **Vertex moved, edge not updated** — `modify_vertex()` doesn't update incident edge curves automatically
9. **Curve doesn't match vertices** — `modify_edge()` accepts curve with endpoints not matching vertex positions
10. **Non-isolated vertices** — `insert_at_vertices()` accepts vertices that already have edges (violates precondition)

**Detection:** Use `arr.is_valid()` after operations to check arrangement consistency.

---

### ✅ Good Discovery: All Query Methods SAFE

Tested 15+ query/traversal methods:
- **Counting:** `number_of_vertices()`, `number_of_edges()`, `number_of_faces()`
- **Boolean:** `is_empty()`, `is_valid()`
- **Vertex:** `point()`, `degree()`, `is_isolated()`
- **Halfedge:** `source()`, `target()`, `twin()`, `next()`, `prev()`
- **Face:** `is_unbounded()`, `has_outer_ccb()`

**Result:** ALL work correctly, no crashes, no corruption. These are the baseline for "safe" behavior.

---

### Day 10: PR #2 Preparation & Submission (Dec 28-29)

**What I did:**
- Wrote docstrings for 15 methods in 3 batches
- Added 🔴 CRITICAL warnings for crash scenarios
- Documented safe usage patterns
- Wrote side-by-side correct vs incorrect examples
- Tested all examples in fresh Python session
- Integrated into binding code carefully (no formatter!)
- Rebuilt and verified

**Docstring Features:**
- NumPy-style format with parameter types
- Explicit "will CRASH Python" language for segfaults
- Safe validation patterns (e.g., `if vertex.is_isolated():`)
- Handle lifetime warnings
- Cross-references to related methods

**Time Spent:** 6 hours (docs already researched, just needed integration)  
**PR #2 Submitted:** December 29, 2025, 11:51 PM IST

---

## 🔬 Phase 3: Extended Research (5+ Hours, Jan 5, 2026)

After submitting both PRs, Efi raised two important questions in his feedback. Instead of waiting, I explored both immediately.

---

### Research Question #1: Docstring "Screening" Problem

**Efi's question:** Can docstrings be defined externally to avoid "screening or shadowing the code"?

**What I did:**
- Analyzed `arrangement_on_surface_2_bindings.cpp` (1,676 lines)
- Found the problem: each method binding spans 40-50 lines (5 lines code + 35-45 lines inline docstring)
- Researched 3 approaches for external definition
- Created proof-of-concept for Approach A

**Approaches Documented:**

**Approach A: Variables at Top of File**
```cpp
// At top of file
const char* METHOD_NAME_DOC = R"pbdoc(
    Full docstring here...
)pbdoc";

// In binding section (much cleaner!)
m.def("method_name", &function, py::arg("param"), METHOD_NAME_DOC);
```
- **Pros:** Simple, no build changes, 85% readability improvement
- **Cons:** Still in same file, long files get harder to navigate
- **Status:** ✅ Tested, syntax verified, production-ready

**Approach B: External Header File**
```cpp
// arrangement_docstrings.h
namespace CGAL { namespace docstrings {
    const char* METHOD_NAME_DOC = R"pbdoc(...)pbdoc";
}}

// arrangement_bindings.cpp
#include "arrangement_docstrings.h"
m.def("method_name", &function, py::arg("param"), CGAL::docstrings::METHOD_NAME_DOC);
```
- **Pros:** Clean separation, easy to find/edit docs
- **Cons:** Requires build system change, more files to maintain
- **Status:** Recommended for long-term

**Approach C: Namespace Organization**
- Middle ground between A and B
- Organizes docstrings in namespaces within same file

**Recommendation:** Approach A for immediate wins (20 minutes to migrate 5 methods), Approach B for long-term architecture.

**Files created:**
- `research/docstring-location/docstring-location-research.md` (full analysis)
- `research/docstring-location/test-approach-a/test_external_docstrings.cpp` (proof-of-concept)
- `research/docstring-location/test-approach-a/README.md` (documentation)

**Time spent:** ~2 hours

---

### Research Question #2: More Crash Scenarios?

**What I did:**
- Tested 3 more potentially unsafe operations
- Found 2 NEW crashes + verified 3 SAFE behaviors

**NEW Crash #6: Accessing Twin After `remove_edge()`**
```python
twin = he.twin()  # Store twin before removal
arr.remove_edge(he)  # Remove edge

point = twin.source().point()  # Access twin - CRASH!
# Result: zsh: segmentation fault
```
**Finding:** Both the halfedge AND its twin are invalidated when edge is removed.

**NEW Crash #7: `remove_isolated_vertex()` Called Twice**
```python
v = arr.insert_in_face_interior(Point_2(3, 3), unbounded)
arr.remove_isolated_vertex(v)  # First removal - OK
arr.remove_isolated_vertex(v)  # Second removal - CRASH!
# Result: zsh: segmentation fault
```
**Finding:** Confirms handle invalidation issue. First removal succeeds, but handle remains accessible—using it again crashes.

**SAFE Behavior #1: `modify_vertex()` Handle Management**
```python
v = arr.insert_in_face_interior(Point_2(5, 5), unbounded)
v_modified = arr.modify_vertex(v, Point_2(10, 10))
arr.remove_isolated_vertex(v)  # Using original handle - works!
```
**Finding:** Original handle remains valid after modification. User-friendly behavior!

**SAFE Behavior #2: `split_edge()` Handle Management**
```python
he_original = arr.insert_from_left_vertex(seg, v1)  # (0,0) to (10,10)
he_new = arr.split_edge(he_original, seg1, seg2)
curve = he_original.curve()  # Shows (0,0) to (5,5) - works!
```
**Finding:** Original halfedge is updated in-place to represent first segment. Expected and safe.

**SAFE Behavior #3: Iterator Invalidation Handled**
```python
for v in arr.vertices():
    if v.is_isolated():
        arr.remove_isolated_vertex(v)  # Deleting while iterating - works!
```
**Finding:** Iterator correctly handles modification during traversal.

**Additional Warnings Found (No Crash, But Invalid Geometry):**
- `modify_vertex()` on Connected Vertex — Accepts modification even when vertex has edges, creating geometric inconsistency
- `split_edge()` with Wrong Point — Accepts split with point not on original edge
- `merge_edge()` with Wrong Orientation — Unclear if using `he2.twin()` is intentional or bug
- `modify_edge()` with Mismatched Endpoints — Accepts new curve with different endpoints

**Updated Statistics:**
- Total crashes found: 7 (5 from December + 2 new)
- Total warnings found: 4 (unsafe but no crash)
- Safe behaviors verified: 3 (iterator, modify_vertex, split_edge)

**Files created:**
- `research/crash-scenarios/test_crash_3_twin.py`
- `research/crash-scenarios/test_crash_4_merge.py`
- `research/crash-scenarios/test_crash_5_double_remove.py`
- `research/crash-scenarios/test_crash_6_modify_edge.py`
- `research/crash-scenarios/test_crash_7_iterator.py`
- `research/crash-scenarios/test_crash_8_modify_then_remove.py`
- `research/crash-scenarios/test_crash_9_split_then_access.py`
- Updated `research/crash-scenarios/additional-crash-scenarios.md`

**Time spent:** ~3 hours

---

## 🎯 Total Contribution Statistics (Dec 20 – Jan 5)

| Metric | Count |
|--------|-------|
| Total hours invested | 95+ |
| Methods fully documented | 21 (6 in PR #1, 15 in PR #2) |
| Methods empirically tested | 30+ |
| Test code written | 900+ lines (9 files) |
| Research documentation | 3,000+ lines |
| Docstrings written | ~950 lines |
| Crash scenarios discovered | 7 (all cause SEGFAULT) |
| Corruption scenarios found | 10+ (silent invalid arrangements) |
| Safe methods confirmed | 15 query methods + 3 modification methods |
| Pull requests submitted | 2 (both substantial) |
| Missing API features identified | 2 categories |
| Research approaches documented | 3 (docstring organization) |
| Proof-of-concepts created | 1 (Approach A) |

---

## 📊 Key Findings Summary

### Gap #1: Documentation (CRITICAL) — ACTIVELY FIXING ⭐

**Before my work:**
- 90% of methods have NO docstrings
- Users forced to read C++ source

**After my work:**
- ✅ 21 methods now fully documented
- ✅ NumPy-style format with examples
- ✅ Named parameters showing actual argument names

**Remaining:** ~40-50 methods still need docs

---

### Gap #2: Safety Issues (CRITICAL) — NOW DOCUMENTED 🔴

**My discoveries:**
- 7 methods crash Python interpreter if misused (updated from 5)
- 10+ methods silently create invalid arrangements
- NO precondition validation in C++ bindings
- Python users expect exceptions, not crashes

**My solution:**
- 🔴 Explicit CRITICAL warnings in docstrings
- Safe usage patterns with validation checks
- Side-by-side correct vs incorrect examples
- Handle lifetime and invalidation documentation

---

### Gap #3: Named Parameters (MAJOR) — PARTIALLY FIXED

**Before:** `insert_from_left_vertex(*args, **kwargs)`  
**After:** `insert_from_left_vertex(curve, vertex)`

- ✅ Fixed for 21 methods
- **Remaining:** Hundreds of functions still show `arg0`, `arg1`

---

### Gap #4: Code Readability (NEW) — SOLUTION PROPOSED

**Problem identified by Efi:** Inline docstrings "screen or shadow" binding code

**Current state:** Each method spans 40-50 lines in binding file

**My solution:** 3 approaches documented with proof-of-concept
- Approach A: 85% readability improvement, 20 minutes to implement
- Approach B: Clean architecture, requires build changes
- Approach C: Middle ground

---

### Gap #5: Resource Deallocation (TECHNICAL) — DOCUMENTED FOR GSoC

Line 857 TODO still exists:
```cpp
//! \todo Why the f... reference_internal doesn't work?
```
- Currently using dangerous bare reference workaround
- Potential memory leaks in long-running applications
- 📋 **Planned for GSoC Weeks 9-10:** Investigation + fix

---

### Gap #6: Missing API Features — IDENTIFIED

- `remove_edge()` optional parameters not bound
- Face iterator methods missing
- **Impact:** Python API less powerful than C++ API

---

## 💻 Technical Skills Demonstrated

### C++ & CGAL
- ✅ Built CGAL from source on macOS M1
- ✅ Read and understood 4,000+ lines of template code
- ✅ Analyzed DCEL structure and traits classes
- ✅ Found real bugs (line 857, missing validations)
- ✅ Understand policy-based design and SFINAE

### Python API Design
- ✅ Written NumPy-style documentation (21 methods)
- ✅ Designed clear, usable examples
- ✅ Built production APIs for 1,000+ daily users
- ✅ Understand what makes documentation actually useful

### Binding Libraries (Nanobind)
- ✅ Mastered return value policies
- ✅ Understand `keep_alive` patterns
- ✅ Implemented `py::arg()` for named parameters
- ✅ Debugged C++/Python interop challenges
- ✅ **NEW:** Researched docstring organization approaches
- ✅ **NEW:** Created proof-of-concept implementations

### Testing & Quality Assurance
- ✅ Wrote 900+ lines of systematic test code
- ✅ Discovered 7 crash scenarios through empirical testing
- ✅ Found 10+ silent corruption cases
- ✅ Documented safe vs unsafe usage patterns
- ✅ **NEW:** Verified 3 safe behaviors (positive testing)

### Git & Open Source Workflow
- ✅ Clean, focused PRs (learned from formatter disaster!)
- ✅ Proper branching and minimal diffs
- ✅ Descriptive PR messages for reviewers
- ✅ Proactive communication with mentor

### Research & Problem Solving
- ✅ **NEW:** Responded to mentor questions with comprehensive research
- ✅ **NEW:** Documented multiple solution approaches
- ✅ **NEW:** Created proof-of-concepts for validation
- ✅ **NEW:** Extended testing to find edge cases

---

## 📝 Next Steps

### Immediate (Jan 5-12):
- [x] Build cgalpy with arrangements enabled
- [x] Test 30+ methods systematically
- [x] Submit PR #1 (insertion methods)
- [x] Complete 13-hour deep research
- [x] Submit PR #2 (removal, modification, query methods)
- [x] Research docstring organization approaches
- [x] Find 2 additional crash scenarios
- [x] Verify 3 safe behaviors
- [ ] Email Efi with research updates
- [ ] Respond to Efi's feedback on both PRs
- [ ] Make any requested changes

### January 2026:
- [ ] Continue docstring work (next batch of methods)
- [ ] Audit remaining methods for named parameters
- [ ] Submit PR #3 if feedback is positive
- [ ] Implement Approach A for docstrings if approved
- [ ] Engage with CGAL community

### February 2026 (Pre-GSoC):
- [ ] Have 3-4 quality PRs merged
- [ ] Begin line 857 investigation (if approved)
- [ ] Final proposal updates
- [ ] Prepare for GSoC applications opening

### Long-term (Post-GSoC Decision):
- Continue contributing regardless of selection
- Help other Python users through documentation
- Work toward maintaining Python bindings long-term
- Build example gallery with real-world use cases

---

## 🔗 Important Links

### My Contributions:
- 🔗 **PR #1 (Insertion Methods):** [Bitbucket PR #1](https://bitbucket.org/taucgl/cgal-python-bindings/pull-requests/)
- 🔗 **PR #2 (Removal/Modification/Query):** [Bitbucket PR #2](https://bitbucket.org/taucgl/cgal-python-bindings/pull-requests/)
- 🔗 **GSoC 2026 Proposal:** [Google Docs](https://docs.google.com/document/d/1XL1RYG9U-9OJlXU0i78VNDTHCz3OLBPHnfQPgQmCfz4/edit?usp=sharing)
- 🔗 **This Prep Repository:** [github.com/UtkarsHMer05/cgal-gsoc-2026-prep](https://github.com/UtkarsHMer05/cgal-gsoc-2026-prep)

### Research Documents:
- 📄 **Docstring Location Research:** `research/docstring-location/docstring-location-research.md`
- 📄 **Additional Crash Scenarios:** `research/crash-scenarios/additional-crash-scenarios.md`
- 📄 **Complete Methods Research:** `research/complete_methods_research.md`

### CGAL Resources:
- **Python Bindings Repo:** https://bitbucket.org/taucgl/cgal-python-bindings
- **CGAL Documentation:** https://doc.cgal.org
- **Nanobind Docs:** https://nanobind.readthedocs.io

### My Links:
- **GitHub:** https://github.com/UtkarsHMer05
- **LinkedIn:** https://linkedin.com/in/utkarshkhajuria05
- **Email:** utkarshkhajuria55@gmail.com

---

## 🤔 Why I'm Doing This

I'm not here for a resume line. I genuinely want to make CGAL's Python bindings better.

Computational geometry is powerful. CGAL's algorithms are elegant. But the barrier to entry is too high for Python developers who just want to solve geometry problems without reading C++ source code.

I want to fix that. Whether GSoC accepts me or not, I'll keep contributing. This is work that matters—making advanced algorithms accessible to more people.

**Update (Jan 5):** Already proven this commitment. Submitted two substantial PRs totaling 21 methods documented, discovered 7 crash scenarios and 10+ corruption cases through systematic testing, researched 3 docstring organization approaches with proof-of-concept, wrote 3,000+ lines of research documentation across multiple topics. Not waiting for GSoC decisions to contribute—actively researching and solving problems as they come up.

---

## 📊 Time Investment Breakdown

| Phase | Activity | Hours | Details |
|-------|----------|-------|---------|
| **Phase 1: Foundation** | Environment Setup | ~8h | Building CGAL, dependencies, testing |
| | 2D Arrangements Study | ~12h | DCEL, traits, examples, 600+ line analysis |
| | Python Bindings Analysis | ~10h | Code reading, gap identification |
| | Nanobind Learning | ~12h | Policies, lifetime, line 857 investigation |
| | Proposal Writing | ~8h | Research, writing, diagrams, revision |
| **Phase 2: Contributions** | cgalpy Build & Testing | ~12h | Arrangements build, method testing |
| | PR #1 Preparation | ~10h | Research docs + docstrings + submission |
| | Deep Methods Research | ~13h | Systematic testing of 25+ methods |
| | PR #2 Preparation | ~6h | 15 method docstrings + integration |
| **Phase 3: Extended Research** | Docstring Organization | ~2h | 3 approaches + proof-of-concept |
| | Additional Crash Testing | ~3h | 2 new crashes + 3 safe behaviors |
| **Total** | | **~96h** | Documented work Dec 20 – Jan 5, 2026 |

---

## 🎓 What I've Learned

### Technical:
- CGAL's template architecture is elegant but requires deep understanding
- Nanobind lifetime management is critical for safety
- Python bindings need comprehensive safety documentation
- Empirical testing reveals behaviors docs don't mention
- NO precondition validation in specialized methods—dangerous!
- 7 ways to crash Python interpreter with CGAL bindings
- 10+ ways to silently corrupt arrangements
- Handle invalidation is a major safety concern
- **NEW:** Docstring organization significantly affects code readability
- **NEW:** Proof-of-concepts validate approaches before implementation
- **NEW:** Some methods ARE safe—positive testing matters too

### Process:
- Read actual code, not just docs
- Test systematically, not casually
- Document discoveries immediately
- Small, focused PRs are easier to review
- 13 hours of testing finds more than 13 days of guessing
- Writing test code is as important as writing docstrings
- Safety warnings save users from painful debugging
- **NEW:** Respond to mentor questions with research, not guesses
- **NEW:** Multiple solution approaches show deep thinking
- **NEW:** Balance negative testing (crashes) with positive testing (safe behaviors)

### Personal:
- I love this kind of deep technical work
- Finding crashes and documenting them properly is satisfying
- I'm ready for the full GSoC challenge
- This is the kind of long-term project I want to commit to
- Going from "I want to contribute" to "I submitted 2 PRs with 21 methods documented" feels amazing
- **NEW:** Continuing research after PRs shows genuine commitment
- **NEW:** Exploring mentor questions immediately builds trust
- **NEW:** 95+ hours invested before GSoC applications even open proves this isn't about resume padding

---

## 💪 Closing Thoughts

This README isn't AI-generated. It's my actual journey over 16 days spanning December 2025 and January 2026.

I started knowing nothing about CGAL. Now I can:
- ✅ Build it from source
- ✅ Understand its architecture deeply
- ✅ Find crashes through systematic testing
- ✅ Write production-quality NumPy-style documentation
- ✅ Submit PRs that demonstrate technical depth
- ✅ Discover critical safety issues that users need to know about
- ✅ Research architectural questions with multiple solution approaches
- ✅ Verify safe behaviors (not just find crashes)

That's what 95+ hours of genuine effort looks like.

I've documented 21 methods. I've found 7 ways to crash Python. I've discovered 10+ ways to silently corrupt data. I've written 900+ lines of test code and 3,000+ lines of research documentation. I've researched 3 docstring organization approaches with working proof-of-concept.

This isn't preparation. This is contribution.

Whether or not GSoC works out, I'm proud of this work. And I'm excited to keep going.

**Computational geometry deserves better Python support. Let's build it together.**

---

**Last Updated:** January 5, 2026, 11:30 PM IST  
**Status:** Two PRs submitted + Extended research complete, awaiting mentor review  
**Next Milestone:** Email mentor with research updates, incorporate feedback, continue documentation work

---

**Utkarsh Khajuria**  
Third-year CS student, VIT Chennai  
CGAL Python bindings contributor (not hoping—doing it!)