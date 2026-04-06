# CURRENT STATUS — CGAL GSoC 2026 Python Bindings

**Last updated:** April 7, 2026 (~3 AM IST)  
**Master Prompt version:** v24.0  
**Total investment:** ~155 hours  
**Latest Bitbucket commit:** `ebea4e79` (Feb 27, 2026 — unchanged)  
**Selection probability:** 85–90%

---

## Phase Status

| Phase | Status | Hours | Dates |
|---|---|---|---|
| Phase 1 Foundation | ✅ COMPLETE | 50h | Dec 20–24, 2025 |
| Phase 2 Contributions | ✅ COMPLETE | 40h | Dec 25–29, 2025 |
| Phase 2.5 Proposal Revision | ✅ COMPLETE | 3h | Dec 30–Jan 1, 2026 |
| Phase 3 Research | ✅ COMPLETE | 17h | Jan 5–11, 2026 |
| Phase 3.5 Named Params Dive | ✅ COMPLETE | 9h | Jan 17, 2026 |
| Phase 4 CI Build Testing | ✅ COMPLETE | 3h | Feb 5, 2026 |
| Phase 4.5 Multi-Kernel CI | ✅ COMPLETE | 8h | Feb 8, 2026 |
| Phase 5 Precondition FW | ✅ COMPLETE (superseded) | 4h | Feb 19, 2026 |
| Phase 5R Framework Refactor | ✅ COMPLETE | 5h | Feb 23–27, 2026 |
| Weeks 1–2 Parameter Naming | ✅ COMPLETE | 5h | March 4–11, 2026 |
| Weeks 3–4 Docstrings | ✅ COMPLETE | 8h | March 13 + March 24, 2026 |
| Docstring Automation Research | ✅ COMPLETE | 3h | March 25, 2026 |
| Docstring Header Generation | ✅ COMPLETE | 3h | April 1, 2026 |
| **Docstring Header Wiring (Pol2)** | **🔄 IN PROGRESS** | **1h** | **April 7, 2026** |

---

## Immediate Next Actions (Priority Order)

### 🔴 DO FIRST — Next Coding Session

**Step 1: Append 10 constants to `polygon_2_docstrings.h`**
```bash
# From repo root (cgal-python-bindings/)
cat >> src/libs/cgalpy/lib/docstrings/polygon_2_docstrings.h << 'HEREDOC'
# ... paste the 10 constants from april7-polygon2-wiring.md ...
HEREDOC
```

**Step 2: Build**
```bash
cd build-manual
export CC=/usr/bin/clang && export CXX=/usr/bin/clang++
make CGALPY -j4
```

**Step 3: Spot-check `__doc__`**
```bash
python3 -c "import CGALPY; print(CGALPY.Pol2.Polygon_2.is_counterclockwise_oriented.__doc__)"
python3 -c "import CGALPY; print(CGALPY.Pol2.Polygon_2.edge.__doc__)"
python3 -c "import CGALPY; print(CGALPY.Pol2.Polygon_2.vertex_mutable.__doc__)"
```

### 🟡 After polygon_2 Passes — Wire Remaining 4 Files

For each file, run the grep-compare-append-build-verify cycle:

```bash
# Step A: grep the .cpp to see what DOC constants it uses
grep -n 'DOC' src/libs/cgalpy/lib/alpha_shape_2_bindings.cpp

# Step B: compare vs the existing .h
cat src/libs/cgalpy/lib/docstrings/alpha_shape_2_docstrings.h | grep "^const char"

# Step C: append missing constants, build, verify
```

Files to wire:
- [ ] `alpha_shape_2_bindings.cpp` + `alpha_shape_2_docstrings.h`
- [ ] `boolean_set_operations_2_bindings.cpp` + `boolean_set_operations_2_docstrings.h`
- [ ] `envelope_2_bindings.cpp` + `envelope_2_docstrings.h`
- [ ] `visibility_2_bindings.cpp` + `visibility_2_docstrings.h`

---

## Task 1 — Wire Docstring Headers (Master Checklist)

### polygon_2_bindings.cpp
- [x] `.def()` calls already wired (DOC constants already present in `.cpp`)
- [x] 10 missing constants identified
- [x] Docstring text determined for all 10
- [ ] Heredoc append run on actual machine  ← **DO FIRST**
- [ ] `make CGALPY -j4` build passes
- [ ] 3 spot-check `__doc__` strings verified at runtime

### alpha_shape_2_bindings.cpp
- [ ] grep `.def()` calls — check if DOC constants already wired or need adding
- [ ] Compare vs `alpha_shape_2_docstrings.h`
- [ ] Append any missing constants
- [ ] Build + runtime verify

### boolean_set_operations_2_bindings.cpp
- [ ] Same check-and-wire sequence
- [ ] Build + runtime verify

### envelope_2_bindings.cpp
- [ ] Same check-and-wire sequence
- [ ] Build + runtime verify

### visibility_2_bindings.cpp
- [ ] Same check-and-wire sequence
- [ ] Build + runtime verify

### Final verification — all 5 packages
- [ ] `python3 -c "import CGALPY; help(CGALPY.Pol2.Polygon_2)"`
- [ ] `python3 -c "import CGALPY; help(CGALPY.As2.Alpha_shape_2)"`
- [ ] `python3 -c "import CGALPY; help(CGALPY.Bso2)"`
- [ ] `python3 -c "import CGALPY; help(CGALPY.Env2)"`
- [ ] `python3 -c "import CGALPY; help(CGALPY.Vis2)"`

---

## Task 2 — Extend Automation Script

Blocked on Task 1 completion and Efi reply to Email 23.

## Task 3 — AOS2 Docstring Header Migration

AOS2 currently has inline docstrings in `arrangement_on_surface_2_bindings.cpp`.  
Will migrate to external header format after all 5 packages are wired.

---

## Local File State (not yet committed)

```
modified:  src/libs/cgalpy/lib/arrangement_on_surface_2_bindings.cpp  (+105 lines)
modified:  src/libs/cgalpy/lib/arr_face_bindings.cpp                   (+101 lines)
modified:  src/libs/cgalpy/lib/arr_halfedge_bindings.cpp               (+54 lines)
modified:  src/libs/cgalpy/lib/arr_vertex_bindings.cpp                 (+50 lines)
modified:  bitbucket-pipelines.yml                                      (+270 lines)
staged:    CMakeLists.txt (7 granular CGAL check flags)
new file:  cmake/PrintCGALPYFlags.cmake
new dir:   src/libs/cgalpy/lib/docstrings/
new file:  src/libs/cgalpy/lib/docstrings/polygon_2_docstrings.h       ← needs 10 constants appended
new file:  src/libs/cgalpy/lib/docstrings/alpha_shape_2_docstrings.h
new file:  src/libs/cgalpy/lib/docstrings/boolean_set_operations_2_docstrings.h
new file:  src/libs/cgalpy/lib/docstrings/envelope_2_docstrings.h
new file:  src/libs/cgalpy/lib/docstrings/visibility_2_docstrings.h
Latest Bitbucket commit: ebea4e79 Feb 27 — UNCHANGED
```

---

## Open Questions for Efi

| Q# | Topic | Email | Status |
|---|---|---|---|
| Q1 | `CGALPY_AOS2_WITH_HISTORY` build config | Email 13, Feb 27 | ⏳ AWAITING |
| Q2 | `Curve_halfedges` fix approach | Email 13, Feb 27 | ⏳ AWAITING |
| Q3 | CGAL fork location (taucgl vs personal) | Email 12, Feb 24 | ⏳ AWAITING |
| Q4 | help-flags target vs `cmake -LH` | Email 15, Mar 9 | ⏳ AWAITING |
| Q5 | Automation: clean up + run on all files | Email 22, Mar 25 | ⏳ AWAITING |

Email 23 — **STILL AWAITING** Efi reply (no new emails since March 25)

---

## Key Numbers

| Metric | Value |
|---|---|
| Total Hours | ~155 |
| Methods with `py::arg` | All AOS2 + vertex/halfedge/face |
| Methods with docs | 108 (57 aos2 + 13 vertex + 14 halfedge + 24 face) |
| Docstring headers | 5 new files (pol2, as2, bso2, env2, vis2) |
| Missing constants (pol2) | 10 identified (text determined Apr 7) |
| Automation POC | 50/50 (100%) on AOS2 function list |
| Crashes Found | 7 (pending CGAL C++ upstream fix) |
| CI Configs | 8 kernels |
| Emails to Efi | 22 sent |
| Latest Bitbucket | ebea4e79 Feb 27 |
| Selection Estimate | 85–90% |

---

## Absolute DO NOTs

- ❌ Use `CGALPY_ENABLE_PRECONDITIONS` — DELETED, never reference it
- ❌ Re-add `HandleRegistry` — Efi said fix in CGAL C++
- ❌ Suggest `keep_alive` fix for line 857
- ❌ Use lowercase `cgalpy` in import — it's `CGALPY` (capital)
- ❌ Say "dynamically builds parameter chains" — this is wrong
- ❌ Say `Curve_halfedges` is unregistered — it IS registered
- ❌ Mention colors/visual design to Efi
- ❌ Commit without Efi's confirmation
- ❌ Add DOC constants that contradict CGAL's official doc language
- ❌ Put docstring headers anywhere other than `src/libs/cgalpy/lib/docstrings/`
- ❌ Open, prepare, or mention any PR — Efi said not to focus on PRs until he explicitly says so
- ❌ Reference PR #1 or PR #2 in any future email to Efi
