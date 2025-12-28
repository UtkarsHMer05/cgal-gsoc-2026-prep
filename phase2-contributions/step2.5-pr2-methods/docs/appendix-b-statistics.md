# Appendix B: Research Statistics

**Detailed breakdown of time, code, and discoveries**

---

## Time Investment Breakdown

| Activity | Hours | Date | Notes |
|----------|-------|------|-------|
| **Insertion methods research** | 5 | Dec 27, 2025 | All 4 methods + overloads |
| **Removal methods research** | 2 | Dec 28, 2025 | Crash discoveries |
| **Modification methods research** | 3 | Dec 28, 2025 | Split, merge, modify |
| **Query methods research** | 1 | Dec 28, 2025 | Safe methods verification |
| **Documentation writing** | 2 | Dec 28, 2025 | This document |
| **Total** | **~13 hours** | Dec 27-28 | 2 days of work |

---

## Code Statistics

| Metric | Count |
|--------|-------|
| **Test files created** | 3 |
| **Total lines of test code** | ~800 |
| **Methods tested** | 25+ |
| **Individual test cases** | 30+ |
| **Python files** | 3 |

### Test File Breakdown

| File | Lines | Tests | Focus |
|------|-------|-------|-------|
| `test_insert_at_vertices.py` | ~250 | 7 | Insertion methods |
| `test_removal_methods.py` | ~300 | 6 | Removal + crashes |
| `test_modification_methods.py` | ~250 | 16 | Modification + query |

---

## Discovery Timeline

| Date | Time | Discovery |
|------|------|-----------|
| Dec 27 | 6:18 PM | Started insertion methods research |
| Dec 27 | 7:30 PM | **Discovery #1**: No validation in insertion methods |
| Dec 27 | 8:45 PM | **Discovery #2**: `insert_from_right_vertex` direction reversed |
| Dec 27 | 9:15 PM | **Discovery #3**: Duplicate points allowed |
| Dec 27 | 10:00 PM | **Discovery #4**: Overlapping segments accepted |
| Dec 27 | 11:05 PM | Completed insertion methods documentation |
| Dec 28 | 2:00 PM | Started removal methods research |
| Dec 28 | 4:28 PM | **Discovery #5**: `remove_isolated_vertex` crash on non-isolated |
| Dec 28 | 4:31 PM | **Discovery #6**: Missing optional parameters in Python |
| Dec 28 | 4:35 PM | **Discovery #7**: Dangling handles return stale data |
| Dec 28 | 4:40 PM | **Discovery #8**: Double removal crashes |
| Dec 28 | 4:46 PM | **Discovery #9**: `merge_edge` non-adjacent crash |
| Dec 28 | 4:48 PM | **Discovery #10**: Deleted vertex access crash |
| Dec 28 | 4:50 PM | **Discovery #11**: Query methods all safe |
| Dec 28 | 5:00 PM | **Discovery #12**: Wrong curves accepted in merge |
| Dec 28 | 5:05 PM | Began comprehensive documentation |

---

## Findings Summary

### Safety Issues Found

| Category | Count | Severity |
|----------|-------|----------|
| **Crash scenarios** | 5 | 🔴 Critical |
| **Corruption scenarios** | 10+ | ⚠️ High |
| **Missing API features** | 2 | 🟡 Medium |
| **Safe methods verified** | 15+ | ✅ Good |

### Crash Scenarios

| # | Method | Cause | Result |
|---|--------|-------|--------|
| 1 | `remove_isolated_vertex` | Non-isolated vertex | Bus error |
| 2 | `remove_edge` | Double call | Segfault |
| 3 | `merge_edge` | Non-adjacent edges | Segfault |
| 4 | vertex access | After merge | Segfault |
| 5 | halfedge access | After remove | Segfault |

### Corruption Scenarios

| # | Method | Cause | Effect |
|---|--------|-------|--------|
| 1 | `insert_in_face_interior` | Duplicate point | Multiple vertices at same location |
| 2 | `insert_from_left_vertex` | Mismatched endpoint | Geometry inconsistency |
| 3 | `insert_from_right_vertex` | Mismatched endpoint | Geometry inconsistency |
| 4 | `insert_at_vertices` | Mismatched endpoints | Geometry inconsistency |
| 5 | `insert_at_vertices` | Duplicate edge | DCEL corruption |
| 6 | `insert_in_face_interior` | Overlapping | Invalid topology |
| 7 | `split_edge` | Wrong split point | Wrong vertex position |
| 8 | `split_edge` | Endpoint split | Duplicate vertex |
| 9 | `merge_edge` | Wrong curve | Geometry inconsistency |
| 10 | `modify_vertex` | No curve update | Geometry inconsistency |
| 11 | `modify_edge` | Wrong curve | Geometry inconsistency |

---

## Methods Tested

### Insertion Methods (4 methods, 6 overloads)

| Method | Tested | Validation | Result |
|--------|--------|------------|--------|
| `insert_in_face_interior(curve, face)` | ✅ | ❌ None | Silent corruption |
| `insert_in_face_interior(point, face)` | ✅ | ❌ None | Allows duplicates |
| `insert_from_left_vertex(curve, v)` | ✅ | ❌ None | Accepts mismatch |
| `insert_from_right_vertex(curve, v)` | ✅ | ❌ None | Reversed + mismatch |
| `insert_at_vertices(curve, v1, v2)` | ✅ | ❌ None | Multiple issues |

### Removal Methods (2 methods)

| Method | Tested | Validation | Result |
|--------|--------|------------|--------|
| `remove_edge(he)` | ✅ | ❌ None | Crashes on double call |
| `remove_isolated_vertex(v)` | ✅ | ❌ None | Crashes on non-isolated |

### Modification Methods (4 methods)

| Method | Tested | Validation | Result |
|--------|--------|------------|--------|
| `split_edge(he, c1, c2)` | ✅ | ❌ None | Accepts wrong points |
| `merge_edge(he1, he2, c)` | ✅ | ❌ None | Crashes + wrong curves |
| `modify_vertex(v, p)` | ✅ | ❌ None | Geometry inconsistency |
| `modify_edge(he, c)` | ✅ | ❌ None | Geometry inconsistency |

### Query Methods (15+ methods)

| Method | Tested | Result |
|--------|--------|--------|
| `number_of_vertices()` | ✅ | ✅ Safe |
| `number_of_edges()` | ✅ | ✅ Safe |
| `number_of_halfedges()` | ✅ | ✅ Safe |
| `number_of_faces()` | ✅ | ✅ Safe |
| `number_of_isolated_vertices()` | ✅ | ✅ Safe |
| `is_empty()` | ✅ | ✅ Safe |
| `is_valid()` | ✅ | ✅ Safe |
| `unbounded_face()` | ✅ | ✅ Safe |
| `vertex.point()` | ✅ | ✅ Safe |
| `vertex.degree()` | ✅ | ✅ Safe |
| `vertex.is_isolated()` | ✅ | ✅ Safe |
| `halfedge.source()` | ✅ | ✅ Safe |
| `halfedge.target()` | ✅ | ✅ Safe |
| `halfedge.twin()` | ✅ | ✅ Safe |
| `halfedge.next()` | ✅ | ✅ Safe |
| `halfedge.prev()` | ✅ | ✅ Safe |
| `halfedge.curve()` | ✅ | ✅ Safe |
| `halfedge.face()` | ✅ | ✅ Safe |
| `face.is_unbounded()` | ✅ | ✅ Safe |
| `face.has_outer_ccb()` | ✅ | ✅ Safe |

---

## Documentation Statistics

| Metric | Count |
|--------|-------|
| **Total document lines** | ~2,500 |
| **Total word count** | ~15,000 |
| **Major sections** | 10 |
| **Appendices** | 2 |
| **Tables** | 15+ |
| **Code examples** | 50+ |

### Document Structure

| Part | Topic | Lines |
|------|-------|-------|
| A | Introduction & Methodology | ~200 |
| B | Insertion Methods | ~450 |
| C | Removal Methods | ~400 |
| D | Modification Methods | ~400 |
| E | Query Methods | ~300 |
| F | Safety Issues | ~350 |
| G | Patterns & Philosophy | ~250 |
| H | Recommendations | ~350 |
| Appendix A | Test Results | ~400 |
| Appendix B | Statistics | ~200 |

---

## Environment Details

| Component | Version/Details |
|-----------|-----------------|
| **Python** | 3.12.7 |
| **macOS** | Sonoma (Apple Silicon M1) |
| **Compiler** | Apple Clang 16.0.0 |
| **nanobind** | Latest via conda |
| **CGAL** | Development build from source |
| **Build flags** | `-DCGALPY_ARRANGEMENT_ON_SURFACE_2_BINDINGS=ON` |

---

## Conclusion

This research represents **~13 hours of systematic empirical testing** that revealed:

- **10 unsafe methods** (insertion + removal + modification)
- **15+ safe methods** (query/traversal only)
- **5 crash scenarios** (Python interpreter death)
- **10+ corruption scenarios** (silent data corruption)
- **2 missing API features** (compared to C++)
- **0 crashes in query methods** (safe baseline)

All findings have been documented with reproducible test cases.

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Created** | December 28, 2025, 5:05 PM IST |
| **Last Updated** | December 28, 2025 |
| **Author** | Utkarsh Khajuria |
| **Email** | utkarshkhajuria55@gmail.com |
| **GitHub** | https://github.com/UtkarsHMer05 |
| **License** | CC BY 4.0 (Attribution) |

---

## References

1. **CGAL 6.1 - 2D Arrangements: User Manual**  
   https://doc.cgal.org/latest/Arrangement_on_surface_2/index.html

2. **CGAL Arrangement_2 Class Reference**  
   https://doc.cgal.org/latest/Arrangement_on_surface_2/classCGAL_1_1Arrangement__2.html

3. **nanobind Documentation - Return Value Policies**  
   https://nanobind.readthedocs.io/en/latest/ownership.html

4. **CGAL Python Bindings Repository**  
   https://bitbucket.org/taucgl/cgal-python-bindings

5. **NumPy Documentation Style Guide**  
   https://numpydoc.readthedocs.io/en/latest/format.html

---

**Previous**: [← Appendix A - Test Results](./appendix-a-test-results.md)  
**Back to**: [Part A - Introduction](./part-a-introduction.md)

---

*This research was conducted independently as part of Google Summer of Code 2026 preparation for the CGAL project. All testing was performed genuinely by the author.*
