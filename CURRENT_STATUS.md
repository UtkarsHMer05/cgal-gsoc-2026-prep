# CURRENT STATUS — April 7, 2026

> Last updated: April 7, 2026 ~3 AM IST
> Total investment: **~155 hours** (Dec 20, 2025 – Apr 7, 2026)

---

## Phase completion

| Phase | Description | Hours | Dates | Status |
|---|---|---|---|---|
| Phase 1 | Foundation — env setup, DCEL, nanobind | 50h | Dec 20-24 | ✅ Complete |
| Phase 2 | Contributions — PRs, crash discovery | 40h | Dec 25-29 | ✅ Complete |
| Phase 2.5 | Proposal revision | 3h | Dec 30 – Jan 1 | ✅ Complete |
| Phase 3 | Research — docstring approaches, PMP | 17h | Jan 5-11 | ✅ Complete |
| Phase 3.5 | Named Parameters deep dive | 9h | Jan 17 | ✅ Complete |
| Phase 4 | CI build testing (Qt6/Clang fix) | 3h | Feb 5 | ✅ Complete |
| Phase 4.5 | 8-kernel CI pipeline | 8h | Feb 8 | ✅ Complete |
| Phase 5 | Precondition framework (superseded) | 4h | Feb 19 | ✅ Superseded |
| Phase 5R | Framework refactor per Efi | 5h | Feb 23-27 | ✅ Complete |
| Weeks 1-2 | Parameter naming (nb::arg) | 5h | Mar 4-11 | ✅ Complete |
| Weeks 3-4 | Docstrings — vertex/halfedge/face/AOS2 | 8h | Mar 13+24 | ✅ Complete |
| Automation | Docstring extractor POC (50/50 AOS2) | 3h | Mar 25 | ✅ Complete |
| Header gen | 5 external docstring headers created | 3h | Apr 1 | ✅ Complete |
| Wiring | polygon_2: 10 missing constants found | 1h | Apr 7 | 🔄 In progress |

---

## GSoC deliverables (pre-GSoC status)

| Week | Deliverable | Status |
|---|---|---|
| 1-2 | Parameter names (nb::arg) | ✅ Done — Mar 11 |
| 3-4 | Docstrings — all AOS2 files | ✅ Done — Mar 24 |
| 3-4+ | Docstring extractor 50/50 POC | ✅ Done — Mar 25 |
| 3-4+ | External header files (5 packages) | ✅ Done — Apr 1 |
| 3-4+ | Polygon_2 header wiring | 🔄 In progress — Apr 7 |
| 5-6 | Safety / preconditions | 🟡 Partial — 7 CMake flags done, CGAL patch pending |
| 7-8 | Named Parameters | 🔍 Researched — property map bridge identified |
| 9-10 | New package | ❌ Not started |
| 11-12 | CI testing | ✅ Done — Feb 8 |

---

## PRIORITY 1 — Append 10 missing constants to polygon_2_docstrings.h

The `.cpp` references these but the header is missing them:

```
IS_COUNTERCLOCKWISE_ORIENTED_DOC   IS_CLOCKWISE_ORIENTED_DOC
IS_COLLINEAR_ORIENTED_DOC          HAS_ON_POSITIVE_SIDE_DOC
HAS_ON_NEGATIVE_SIDE_DOC           HAS_ON_BOUNDARY_DOC
HAS_ON_BOUNDED_SIDE_DOC            HAS_ON_UNBOUNDED_SIDE_DOC
VERTEX_MUTABLE_DOC                 EDGE_DOC
```

See `week3-4-docstrings/april7-polygon2-wiring.md` for the exact heredoc command.

## PRIORITY 2 — Audit + wire remaining 4 packages

For each: `alpha_shape_2`, `boolean_set_operations_2`, `envelope_2`, `visibility_2`
1. `grep -n '.def(' src/libs/cgalpy/lib/<pkg>_bindings.cpp`
2. Verify every referenced DOC constant exists in the header
3. `make CGALPY -j4` → runtime spot-check

## PRIORITY 3 — Await Email 23 from Efi before any git push

---

## Local file state (not yet committed)

```
modified:  src/libs/cgalpy/lib/arrangement_on_surface_2_bindings.cpp  (+105 lines)
modified:  src/libs/cgalpy/lib/arr_face_bindings.cpp                  (+101 lines)
modified:  src/libs/cgalpy/lib/arr_halfedge_bindings.cpp              (+54 lines)
modified:  src/libs/cgalpy/lib/arr_vertex_bindings.cpp                (+50 lines)
modified:  bitbucket-pipelines.yml                                    (+270 lines)
staged:    CMakeLists.txt                                             (7 CGAL flags)
new file:  cmake/PrintCGALPYFlags.cmake
new dir:   src/libs/cgalpy/lib/docstrings/
new file:  src/libs/cgalpy/lib/docstrings/polygon_2_docstrings.h     ← needs 10 appended
new file:  src/libs/cgalpy/lib/docstrings/alpha_shape_2_docstrings.h
new file:  src/libs/cgalpy/lib/docstrings/boolean_set_operations_2_docstrings.h
new file:  src/libs/cgalpy/lib/docstrings/envelope_2_docstrings.h
new file:  src/libs/cgalpy/lib/docstrings/visibility_2_docstrings.h
```

**Latest Bitbucket commit: `ebea4e79` Feb 27 — UNCHANGED**

---

## Open questions for Efi

| # | Question | Email | Status |
|---|---|---|---|
| Q1 | CGALPY_AOS2_WITH_HISTORY build config | Email 13 Feb 27 | ⏳ Awaiting |
| Q2 | Curve_halfedges fix approach | Email 13 Feb 27 | ⏳ Awaiting |
| Q3 | CGAL fork location (taucgl vs personal) | Email 12 Feb 24 | ⏳ Awaiting |
| Q4 | help-flags target vs cmake -LH | Email 15 Mar 9 | ⏳ Awaiting |
| Q5 | Automation: clean up + run on all files | Email 22 Mar 25 | ⏳ Awaiting |

---

## Key numbers

| Metric | Value |
|---|---|
| Total hours | ~155 |
| Methods with docstrings | 108 (57 AOS2 + 13 vertex + 14 halfedge + 24 face) |
| Docstring headers generated | 5 |
| Missing constants found Apr 7 | 10 (polygon_2) |
| Automation POC coverage | 50/50 (100%) AOS2 |
| Crashes documented | 7 |
| CI kernel configurations | 8 |
| Emails to Efi | 22 sent |
| Selection estimate | 85-90% |