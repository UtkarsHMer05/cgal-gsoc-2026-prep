# Current Status — cgal-gsoc-2026-prep

**Last updated:** April 1, 2026, 3:48 AM IST
**Total hours logged:** 156+
**Bitbucket commit:** `ebea4e79` (Feb 27, 2026) — unchanged

---

## GSoC Deliverables — Pre-GSoC Progress

| Week | Task | Status | Date Completed |
|---|---|---|---|
| Weeks 1-2 | Parameter Names (`nb::arg`) | Done (pre-GSoC) | March 4–11 |
| Weeks 3-4 | Docstrings — inline, AOS2/Vertex/HE/Face | Done (pre-GSoC) | March 13 + 24 |
| Weeks 3-4+ | Docstring Automation Research (50/50 AOS2) | Done (pre-GSoC) | March 25 |
| Weeks 3-4+ | Docstring Header Files (5 packages) | Done (pre-GSoC) | April 1 |
| Weeks 5-6 | Safety/Preconditions | Partial | 7 CMake flags done |
| Weeks 7-8 | Named Parameters | Researched | Property map bridge identified |
| Weeks 9-10 | New Package | Not started | LCC or Shape Recognition |
| Weeks 11-12 | CI Pipeline (8 kernels) | Done (pre-GSoC) | Feb 8 |

---

## Phase Completion Summary

| Phase | Description | Hours | Status |
|---|---|---|---|
| Phase 1 | Foundation (env, DCEL, nanobind) | 50h | Complete |
| Phase 2 | Contributions (PRs, crash discovery) | 40h | Complete |
| Phase 2.5 | Proposal Revision | 3h | Complete |
| Phase 3 | Research (Approach A/B, PMP build) | 17h | Complete |
| Phase 3.5 | Named Parameters Deep Dive | 9h | Complete |
| Phase 4 | CI Build Testing | 3h | Complete |
| Phase 4.5 | Multi-Kernel CI Pipeline | 8h | Complete |
| Phase 5 | Precondition Framework (superseded) | 4h | Complete |
| Phase 5R | Framework Refactor per Efi | 5h | Complete |
| Weeks 1-2 | Parameter Naming | 5h | Complete |
| Weeks 3-4 | Docstrings (inline) | 8h | Complete |
| Doc Automation | AOS2 50/50 POC Script | 3h | Complete |
| Doc Headers | 5 header files generated | 3h | Complete |
| **Total** | | **153h+** | |

---

## Local File State (Not Yet Committed)

```
modified:  src/libs/cgalpy/lib/arrangement_on_surface_2_bindings.cpp  (+105 lines)
modified:  src/libs/cgalpy/lib/arr_face_bindings.cpp                  (+101 lines)
modified:  src/libs/cgalpy/lib/arr_halfedge_bindings.cpp              (+54 lines)
modified:  src/libs/cgalpy/lib/arr_vertex_bindings.cpp                (+50 lines)
modified:  bitbucket-pipelines.yml                                    (+270 lines)
staged:    CMakeLists.txt                                             (7 check flags)
new file:  cmake/PrintCGALPYFlags.cmake
new dir:   src/libs/cgalpy/lib/docstrings/                           (new — April 1)
new file:  src/libs/cgalpy/lib/docstrings/polygon_2_docstrings.h
new file:  src/libs/cgalpy/lib/docstrings/alpha_shape_2_docstrings.h
new file:  src/libs/cgalpy/lib/docstrings/boolean_set_operations_2_docstrings.h
new file:  src/libs/cgalpy/lib/docstrings/envelope_2_docstrings.h
new file:  src/libs/cgalpy/lib/docstrings/visibility_2_docstrings.h
```

The headers are generated but **not yet wired** into the binding `.cpp` files.
See [`wiring-guide.md`](week3-4-docstrings/docstring-headers/wiring-guide.md) for the next steps.

---

## Open Questions for Efi

| # | Question | Email | Status |
|---|---|---|---|
| Q1 | `CGALPY_AOS2_WITH_HISTORY` build config | Email 13, Feb 27 | Awaiting |
| Q2 | `Curve_halfedges` fix approach | Email 13, Feb 27 | Awaiting |
| Q3 | CGAL fork location (taucgl vs personal) | Email 12, Feb 24 | Awaiting |
| Q4 | `help-flags` target vs `cmake -LH` | Email 15, Mar 9 | Awaiting |
| Q5 | Automation: clean up + run on all files | Email 22, Mar 25 | Awaiting |

Email 23 is still pending. No new emails since Email 22.

---

## Key Numbers

- **Total hours:** 156+
- **Methods with `nb::arg`:** all AOS2 + vertex/halfedge/face
- **Methods with inline docs:** 108 (AOS2: 57, vertex: 13, halfedge: 14, face: 24)
- **Docstring header files:** 5 (pol2, as2, bso2, env2, vis2)
- **Docstring constants total:** ~50 across 5 header files
- **Automation POC accuracy:** 50/50 (100%) on AOS2 function list
- **Crashes found:** 7 (pending CGAL C++ upstream fix)
- **CI configurations:** 8 kernels
- **Emails sent to Efi:** 22
- **Selection estimate:** 85–90%

---

## Immediate Next Actions

1. **Wire the headers** — add `#include` to the 5 binding `.cpp` files, then append DOC constants to each `.def()` call. See `wiring-guide.md` for the full walkthrough.
2. **Await Email 23** before committing anything to Bitbucket.
3. **Extend the automation script** — run the March 25 AOS2 extractor against `~/cgal/Polygon/doc/Polygon/CGAL/` to measure `Polygon_2` coverage.
