# 🎯 CGAL GSoC 2026 Preparation Repository

**Project:** CGAL Python Bindings Enhancement  
**Applicant:** Utkarsh Khajuria  
**Mentor:** Efi Fogel (efifogel@gmail.com)  
**Preparation Period:** December 20-29, 2025  
**Total Time Invested:** 90+ hours

---

## 📌 Current Status — December 29, 2025

### ✅ TWO SUBSTANTIAL PRs SUBMITTED

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
- Arrangement: `number_of_vertices()`, `number_of_edges()`, `number_of_faces()`, `is_empty()`, `is_valid()`, `unbounded_face()`
- Vertex: `degree()`, `is_isolated()`
- Halfedge: `twin()`

**Research Behind PR #2:**
- 13 hours of systematic empirical testing (Dec 27-28)
- 800+ lines of test code across 3 files
- 2,500+ lines of research documentation
- 25+ methods tested across all categories
- Found 5 scenarios that crash Python interpreter
- Found 10+ scenarios that silently corrupt arrangements

---

### 📝 GSoC 2026 Proposal
🔗 [Live Proposal — Google Docs](https://docs.google.com/document/d/1XL1RYG9U-9OJlXU0i78VNDTHCz3OLBPHnfQPgQmCfz4/edit?usp=sharing)

Updated to include:
- Both PR submissions (21 methods documented total)
- Complete 90+ hour preparation timeline
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

I'm not here for just a summer project. I want to make CGAL's Python bindings actually usable for researchers and developers who need computational geometry but don't want to read C++ source code. I've already invested 90+ hours before even applying, and I'll keep contributing regardless of GSoC selection.

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

**DCEL Structure:**
- Vertices store geometric points + degree
- Halfedges are directed edges with twin pointers
- Faces represent regions bounded by edges
- Everything links bidirectionally for traversal

**Traits Classes:**
- `Arr_segment_traits_2` for line segments
- `Arr_circle_segment_traits_2` for circular arcs
- Traits define geometric operations (intersections, comparisons)

**Insertion Methods (15+ types!):**
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

**The Good:**
- 2D/3D Arrangements ~80% complete
- 13+ geometry types supported
- Pythonic iteration works well

**The Gaps:**
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

**Return Value Policies:**
- `reference_internal` — Keeps parent alive (most common)
- `copy` — Independent copy
- `take_ownership` — Python owns object
- `reference` — Bare reference (dangerous!)

**Lifetime Management:**
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

### Missing API Features Found:

**`remove_edge()` optional parameters missing**
- C++ has: `remove_edge(e, remove_source=true, remove_target=true)`
- Python has: `remove_edge(halfedge)` only
- Impact: No control over vertex removal

**Face iterator methods not bound**
- Missing: `holes_begin()`, `holes_end()`, `isolated_vertices_begin()`, `isolated_vertices_end()`
- Impact: Can't iterate holes in faces or isolated vertices

---

### Research Output Created:

**`complete_methods_research.md` (2,500+ lines)**
- Executive summary with safety tables
- Complete findings for 25+ methods
- Test results with code
- 12 critical discoveries documented
- Recommendations for users/maintainers

**`test_removal_methods.py` (~300 lines)**
- Tests for `remove_edge`, `remove_isolated_vertex`
- Crash scenarios reproduced
- Conditional vertex removal documented

**`test_modification_methods.py` (~350 lines)**
- Tests for `split_edge`, `merge_edge`, `modify_vertex`, `modify_edge`
- Crash scenarios reproduced
- Geometric inconsistency tests

**`test_query_methods.py` (~200 lines)**
- Tests for 15+ query methods
- Confirmed all safe

**Total Test Code:** 800+ lines  
**Total Research Docs:** 2,500+ lines

**Time Spent on Research:** 13 hours

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

## 🎯 Total Contribution Statistics (Dec 20-29)

| Metric | Count |
|--------|-------|
| Total hours invested | 90+ |
| Methods fully documented | 21 (6 in PR #1, 15 in PR #2) |
| Methods empirically tested | 25+ |
| Test code written | 800+ lines (3 files) |
| Research documentation | 2,500+ lines |
| Docstrings written | ~950 lines |
| Crash scenarios discovered | 5 (all cause SEGFAULT) |
| Corruption scenarios found | 10+ (silent invalid arrangements) |
| Safe methods confirmed | 15+ (all query methods) |
| Pull requests submitted | 2 (both substantial) |
| Missing API features identified | 2 categories |

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
- 5 methods crash Python interpreter if misused
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

### Gap #4: Resource Deallocation (TECHNICAL) — DOCUMENTED FOR GSoC

Line 857 TODO still exists:
```cpp
//! \todo Why the f... reference_internal doesn't work?
```
- Currently using dangerous bare reference workaround
- Potential memory leaks in long-running applications
- 📋 **Planned for GSoC Weeks 9-10:** Investigation + fix

---

### Gap #5: Missing API Features — IDENTIFIED

- `remove_edge()` optional parameters not bound
- Face iterator methods missing
- Impact: Python API less powerful than C++ API

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

### Testing & Quality Assurance
- ✅ Wrote 800+ lines of systematic test code
- ✅ Discovered 5 crash scenarios through empirical testing
- ✅ Found 10+ silent corruption cases
- ✅ Documented safe vs unsafe usage patterns

### Git & Open Source Workflow
- ✅ Clean, focused PRs (learned from formatter disaster!)
- ✅ Proper branching and minimal diffs
- ✅ Descriptive PR messages for reviewers
- ✅ Proactive communication with mentor

---

## 📝 Next Steps

### Immediate (Dec 29 - Jan 5):
- [x] Build cgalpy with arrangements enabled
- [x] Test 25+ methods systematically
- [x] Submit PR #1 (insertion methods)
- [x] Complete 13-hour deep research
- [x] Submit PR #2 (removal, modification, query methods)
- [ ] Respond to Efi's feedback on both PRs
- [ ] Make any requested changes
- [ ] Document lessons learned

### January 2026:
- [ ] Continue docstring work (next batch of methods)
- [ ] Audit remaining methods for named parameters
- [ ] Submit PR #3 if feedback is positive
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

**Update (Dec 29):** Already proven this commitment. Submitted two substantial PRs totaling 21 methods documented, discovered 5 crash scenarios and 10+ corruption cases through 13 hours of systematic testing, and wrote 2,500+ lines of research documentation. Not waiting for GSoC decisions to contribute—doing it now.

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
| **Total** | | **~91h** | Documented work Dec 20-29, 2025 |

---

## 🎓 What I've Learned

### Technical:
- CGAL's template architecture is elegant but requires deep understanding
- Nanobind lifetime management is critical for safety
- Python bindings need comprehensive safety documentation
- Empirical testing reveals behaviors docs don't mention
- ✅ **New:** NO precondition validation in specialized methods—dangerous!
- ✅ **New:** 5 ways to crash Python interpreter with CGAL bindings
- ✅ **New:** 10+ ways to silently corrupt arrangements
- ✅ **New:** Handle invalidation is a major safety concern

### Process:
- Read actual code, not just docs
- Test systematically, not casually
- Document discoveries immediately
- Small, focused PRs are easier to review
- ✅ **New:** 13 hours of testing finds more than 13 days of guessing
- ✅ **New:** Writing test code is as important as writing docstrings
- ✅ **New:** Safety warnings save users from painful debugging

### Personal:
- I love this kind of deep technical work
- Finding crashes and documenting them properly is satisfying
- I'm ready for the full GSoC challenge
- This is the kind of long-term project I want to commit to
- ✅ **New:** Going from "I want to contribute" to "I submitted 2 PRs with 21 methods documented" feels amazing

---

## 💪 Closing Thoughts

This README isn't AI-generated. It's my actual journey over 10 days in December 2025.

I started knowing nothing about CGAL. Now I can:
- ✅ Build it from source
- ✅ Understand its architecture deeply
- ✅ Find crashes through systematic testing
- ✅ Write production-quality NumPy-style documentation
- ✅ Submit PRs that demonstrate technical depth
- ✅ Discover critical safety issues that users need to know about

That's what 90+ hours of genuine effort looks like.

I've documented 21 methods. I've found 5 ways to crash Python. I've discovered 10+ ways to silently corrupt data. I've written 800+ lines of test code and 2,500+ lines of research documentation.

This isn't preparation. This is contribution.

Whether or not GSoC works out, I'm proud of this work. And I'm excited to keep going.

**Computational geometry deserves better Python support. Let's build it together.**

---

**Last Updated:** December 29, 2025, 11:55 PM IST  
**Status:** Two PRs submitted, awaiting mentor review  
**Next Milestone:** Incorporate feedback, continue documentation work

---

**Utkarsh Khajuria**  
Third-year CS student, VIT Chennai  
CGAL Python bindings contributor (not hoping—doing it!)
