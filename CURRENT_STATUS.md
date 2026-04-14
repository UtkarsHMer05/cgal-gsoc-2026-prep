# CURRENT STATUS — CGAL GSoC 2026 Python Bindings

**Last updated:** April 15, 2026 (~4:40 AM IST)  
**Master Prompt version:** v25.0 (includes April 7–15 session)  
**Total investment:** ~160+ hours  
**Latest Bitbucket commit:** `ebea4e79` (Feb 27, 2026 — unchanged)  
**Selection probability:** 85–90%

---

## Phase Status

| Phase | Status | Hours | Dates |
| --- | --- | --- | --- |
| Phase 1 Foundation | ✅ COMPLETE | 50h | Dec 20–24, 2025 |
| Phase 2 Contributions | ✅ COMPLETE | 40h | Dec 25–29, 2025 |
| Phase 2.5 Proposal Revision | ✅ COMPLETE | 3h | Dec 30–Jan 1, 2026 |
| Phase 3 Research | ✅ COMPLETE | 17h | Jan 5–11, 2026 |
| Phase 3.5 Named Params Dive | ✅ COMPLETE | 9h | Jan 17, 2026 |
| Phase 4 CI Build Testing | ✅ COMPLETE | 3h | Feb 5, 2026 |
| Phase 4.5 Multi‑Kernel CI | ✅ COMPLETE | 8h | Feb 8, 2026 |
| Phase 5 Precondition FW | ✅ COMPLETE (superseded) | 4h | Feb 19, 2026 |
| Phase 5R Framework Refactor | ✅ COMPLETE | 5h | Feb 23–27, 2026 |
| Weeks 1–2 Parameter Naming | ✅ COMPLETE | 5h | Mar 4–11, 2026 |
| Weeks 3–4 Docstrings (inline) | ✅ COMPLETE | 8h | Mar 13 + Mar 24, 2026 |
| Docstring Automation Research (AOS2) | ✅ COMPLETE | 3h | Mar 25, 2026 |
| Docstring Header Generation (5 pkgs) | ✅ COMPLETE | 3h | Apr 1, 2026 |
| Docstring Header Wiring (Pol2 + As2/Bso2/Env2/Vis2) | ✅ COMPLETE LOCALLY | ~3h | Apr 7–15, 2026 |

---

## Immediate Next Actions (Priority Order)

### 🔴 While waiting for Efi — keep repo consistent and stable

These tasks do **not** need new mentor decisions and are safe to finish/verify:

1. **Confirm `polygon_2_docstrings.h` is fully patched.**  
   - Ensure all 10 previously missing constants are present at the end of the file:  
     `IS_COUNTERCLOCKWISE_ORIENTED_DOC`, `IS_CLOCKWISE_ORIENTED_DOC`,
     `IS_COLLINEAR_ORIENTED_DOC`, `HAS_ON_POSITIVE_SIDE_DOC`,
     `HAS_ON_NEGATIVE_SIDE_DOC`, `HAS_ON_BOUNDARY_DOC`,
     `HAS_ON_BOUNDED_SIDE_DOC`, `HAS_ON_UNBOUNDED_SIDE_DOC`,
     `VERTEX_MUTABLE_DOC`, `EDGE_DOC`.  
   - Confirm a clean build succeeds and the constants resolve at compile time.

2. **Re‑run a clean build + runtime spot checks for all 5 packages.**

```bash
cd build-manual
export CC=/usr/bin/clang && export CXX=/usr/bin/clang++
make CGALPY -j4
```

Then:

```bash
python3 - << 'PY'
import CGALPY as C
for obj in [
    C.Pol2.Polygon_2.is_counterclockwise_oriented,
    C.Pol2.Polygon_2.edge,
    C.Pol2.Polygon_2.vertex_mutable,
]:
    print(obj.__name__, ":\n", obj.__doc__, "\n")

for mod in [C.As2.Alpha_shape_2, C.Bso2, C.Env2, C.Vis2]:
    help(mod)
PY
```

3. **Do not change the extractor or LaTeX/markup handling** until Efi replies
   to the April 7 questions (manual overrides + markup policy).

4. **Use spare time only for read‑only reconnaissance of Triangulation_2 /
   Convex_hull_2** (API mapping, method tables) — no big binding changes until
   mentor confirms Weeks 5–6 direction.

---

## Task 1 — Five‑Package Docstring Header Wiring (Master Checklist)

### polygon_2_bindings.cpp + polygon_2_docstrings.h

- [x] `.def()` calls wired to DOC constants in `polygon_2_bindings.cpp`.
- [x] 10 missing constants identified.
- [x] Docstring text determined for all 10 (see `april7-polygon2-wiring.md`).
- [x] 10 constants appended to `polygon_2_docstrings.h`.
- [x] `make CGALPY -j4` passes after header update.
- [x] Spot‑checks:

```bash
python3 - << 'PY'
import CGALPY as C
print(C.Pol2.Polygon_2.is_counterclockwise_oriented.__doc__)
print(C.Pol2.Polygon_2.has_on_bounded_side.__doc__)
print(C.Pol2.Polygon_2.edge.__doc__)
PY
```

### alpha_shape_2_bindings.cpp + alpha_shape_2_docstrings.h

- [x] `#include "docstrings/alpha_shape_2_docstrings.h"` added.
- [x] All `.def()` calls pass the appropriate `*_DOC` constant.
- [x] `make CGALPY -j4` passes.
- [x] Runtime `help(CGALPY.As2.Alpha_shape_2)` shows docstrings.

### boolean_set_operations_2_bindings.cpp + boolean_set_operations_2_docstrings.h

- [x] `#include "docstrings/boolean_set_operations_2_docstrings.h"` added.
- [x] `.def()` calls wired to `DO_INTERSECT_DOC`, `INTERSECTION_DOC`, `JOIN_DOC`,
      `DIFFERENCE_DOC`, `SYMMETRIC_DIFFERENCE_DOC`, `COMPLEMENT_DOC`,
      `IS_VALID_DOC`.
- [x] Build passes.
- [x] `help(CGALPY.Bso2)` shows the expected text.

### envelope_2_bindings.cpp + envelope_2_docstrings.h

- [x] `#include "docstrings/envelope_2_docstrings.h"` added.
- [x] All relevant `.def()` calls wired to `LOWER_ENVELOPE_*_DOC`,
      `UPPER_ENVELOPE_*_DOC`, `MINIMIZATION_DIAGRAM_DOC`,
      `MAXIMIZATION_DIAGRAM_DOC`, `DIAGRAM_VERTEX/EDGE/FACE_DOC`.
- [x] Build passes; `help(CGALPY.Env2)` looks correct.

### visibility_2_bindings.cpp + visibility_2_docstrings.h

- [x] `#include "docstrings/visibility_2_docstrings.h"` added.
- [x] `.def()` calls wired to `COMPUTE_VISIBILITY_DOC`,
      `COMPUTE_VISIBILITY_HALFEDGE_DOC`, `IS_ATTACHED_DOC`,
      `ATTACH_DOC`, `DETACH_DOC`.
- [x] Build passes; `help(CGALPY.Vis2)` looks correct.

### Final verification — all 5 packages

- [x] `python3 -c "import CGALPY; help(CGALPY.Pol2.Polygon_2)"`
- [x] `python3 -c "import CGALPY; help(CGALPY.As2.Alpha_shape_2)"`
- [x] `python3 -c "import CGALPY; help(CGALPY.Bso2)"`
- [x] `python3 -c "import CGALPY; help(CGALPY.Env2)"`
- [x] `python3 -c "import CGALPY; help(CGALPY.Vis2)"`

Result: **119 `.def()` call sites** across these five packages now take
a `*_DOC` constant, and 15 representative `__doc__` values were spot‑checked
successfully.

---

## Task 2 — Extend Automation Script

**Status:** Paused, waiting for mentor guidance.

You already have an extractor that:

- Achieves 50/50 (100%) coverage for the AOS2 target list.  
- Achieves 73/73 coverage across Polygon_2, Alpha_shapes_2, Boolean_set_operations_2, Envelope_2, Visibility_2 using a combination of extracted and manual docstrings.[file:21]

Pending Efi’s reply to Q5 / Emails 23–25, you are deliberately **not**
generalising it further to new packages (Minkowski_sum_2, Polygon_with_holes_2, etc.) or changing LaTeX handling.

---

## Task 3 — AOS2 Docstring Header Migration (Future)

- AOS2 currently uses inline docstrings inside
  `arrangement_on_surface_2_bindings.cpp` (Weeks 3–4 work).  
- Migrating AOS2 to a header file (Approach B) is a **future refactor**
  after the five current header‑based packages have been fully validated
  and after Efi confirms he likes this pattern.

---

## Local File State (not yet committed)

```text
modified:  src/libs/cgalpy/lib/arrangement_on_surface_2_bindings.cpp  (+105 lines)
modified:  src/libs/cgalpy/lib/arr_face_bindings.cpp                   (+101 lines)
modified:  src/libs/cgalpy/lib/arr_halfedge_bindings.cpp               (+54 lines)
modified:  src/libs/cgalpy/lib/arr_vertex_bindings.cpp                 (+50 lines)
modified:  bitbucket-pipelines.yml                                     (+270 lines)
staged:    CMakeLists.txt (7 granular CGALPY_* check flags)
new file:  cmake/PrintCGALPYFlags.cmake
new dir:   src/libs/cgalpy/lib/docstrings/
new file:  src/libs/cgalpy/lib/docstrings/polygon_2_docstrings.h
new file:  src/libs/cgalpy/lib/docstrings/alpha_shape_2_docstrings.h
new file:  src/libs/cgalpy/lib/docstrings/boolean_set_operations_2_docstrings.h
new file:  src/libs/cgalpy/lib/docstrings/envelope_2_docstrings.h
new file:  src/libs/cgalpy/lib/docstrings/visibility_2_docstrings.h

Latest Bitbucket commit: ebea4e79 (Feb 27) — UNCHANGED
```

All header and binding changes described above are still local only; per
Efi’s instruction, no PRs or pushes yet.

---

## Open Questions for Efi

| Q# | Topic | Email | Status |
| --- | --- | --- | --- |
| Q1 | `CGALPY_AOS2_WITH_HISTORY` build config | Email 13 (Feb 27) | ⏳ AWAITING |
| Q2 | `Curve_halfedges` fix approach | Email 13 (Feb 27) | ⏳ AWAITING |
| Q3 | CGAL fork location (taucgl vs personal) | Email 12 (Feb 24) | ⏳ AWAITING |
| Q4 | `help-flags` target vs `cmake -LH` | Email 15 (Mar 9) | ⏳ AWAITING |
| Q5 | Automation: clean up script + run on more files | Email 22 (Mar 25) | ⏳ AWAITING |
| Q6 | Manual docstrings policy (8 functions) | Email 24 (Apr 7) | ⏳ AWAITING |
| Q7 | LaTeX/Doxygen markup policy in Python docs | Email 24 (Apr 7) | ⏳ AWAITING |
| Q8 | Priority: more docstrings vs Triangulation_2 / Convex_hull_2 | Email 24/25 (Apr 7) | ⏳ AWAITING |

No replies yet after Email 22 (Mar 25) and the April 7 status + addendum emails.

---

## Key Numbers

| Metric | Value |
| --- | --- |
| Total Hours | ~160+ |
| Methods with `py::arg` | All AOS2 + vertex/halfedge/face |
| Methods with inline docs (AOS2 core) | 108 (57 AOS2 + 13 vertex + 14 halfedge + 24 face) |
| Docstring headers | 5 files (pol2, as2, bso2, env2, vis2) |
| Docstring constants in those headers | 70+ (including the 10 extra Polygon_2 ones) |
| Automation POC | 50/50 (100%) on AOS2 target list |
| 5‑package coverage | 73/73 methods documented (extracted or manual) |
| Crashes found | 7 (pending CGAL C++ patches) |
| CI configs | 8 kernels |
| Emails to Efi | 24–25 sent (depending whether addendum counted separately) |
| Latest Bitbucket | `ebea4e79` (Feb 27) |
| Selection estimate | 85–90% |

---

## Absolute DO NOTs

- ❌ Use `CGALPY_ENABLE_PRECONDITIONS` — it was deleted; never reference it.
- ❌ Re‑add `HandleRegistry` or `cgalpy_error_handler.h` — Efi wants fixes in CGAL C++.
- ❌ Suggest a `keep_alive`‑based “fix” for line 857 without explicit mentor direction.
- ❌ Use lowercase `cgalpy` in imports — the module name is `CGALPY`.
- ❌ Say “dynamically builds parameter chains” when describing Named Parameters.
- ❌ Claim `Curve_halfedges` is unregistered — it **is** registered via `py::class_<Ch, Cv>`.
- ❌ Talk about colours/visual design in emails to Efi.
- ❌ Commit or push to Bitbucket without Efi’s confirmation.
- ❌ Add DOC constants that contradict official CGAL documentation wording.
- ❌ Put docstring headers anywhere other than `src/libs/cgalpy/lib/docstrings/`.
- ❌ Open, prepare, or mention any PR (including PR #1 / #2) in future emails until Efi explicitly asks for PRs.
