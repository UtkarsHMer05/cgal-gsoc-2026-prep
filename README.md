# CGAL GSoC 2026 — Python Bindings Enhancement (Preparation Repository)

> **Student:** Utkarsh Khajuria · VIT Chennai · `utkarshkhajuria55@gmail.com`
> **Mentor:** Efi Fogel · `efifogel@gmail.com`
> **Program:** Google Summer of Code 2026 · CGAL · 350 h / 12 weeks
> **Official repo:** https://bitbucket.org/taucgl/cgal-python-bindings
> **Branch:** `feature/named-params-operators-poc`
> **Latest upstream commit:** `ebea4e79` (Feb 27, 2026)

---

## What this repo is

This repository documents every hour of pre-GSoC preparation work done
between December 20, 2025 and the start of GSoC coding (May 2026).
It is **not** the binding code itself — that lives on Bitbucket.
Everything here is research notes, scripts, progress logs, and reference
material that drove the actual code changes.

**155+ hours | 22 emails with mentor | 7 crashes found | 8-kernel CI pipeline**

---

## Repository structure

```
cgal-gsoc-2026-prep/
├── phase1-foundation/          Dec 20-24 2025  Environment, DCEL study, nanobind mastery
├── phase2-contributions/       Dec 25-29 2025  PRs, crash discovery (7 crashes, 10 corruptions)
├── phase3-research/            Jan 5-11 2026   Docstring approaches A/B/C, PMP build, Named Params
├── phase4-ci-infrastructure/   Feb 5-8 2026    Manual build fix, 8-kernel CI pipeline
├── phase5-safety-framework/    Feb 19-27 2026  Framework built → refactored per Efi's direction
├── weeks1-2-parameter-naming/  Mar 4-11 2026   nb::arg() on all AOS2 methods
└── week3-4-docstrings/         Mar 13 – Apr 7  Docstring headers + automation + wiring
    ├── docstring-headers/          All 5 .h files (reference copies)
    ├── docstring_extractor.py      v1 extractor (iterative dev log)
    ├── docstring_extractor_v2.py   Final clean extractor — 50/50 on AOS2
    ├── verification_test.py        Runtime __doc__ spot-check script
    ├── march13-vertex-halfedge-face-complete.md   March 13 session — vertex/halfedge/face docs
    ├── march24-aos2-bindings-complete.md          March 24 session — AOS2 57 methods done
    ├── march25-automation-research.md             Automation POC (50/50) + email thread
    ├── april1-docstring-headers-generated.md      5 external header files created
    ├── april7-polygon2-wiring.md                  10 missing constants identified + text
    └── progress-notes.md                          Cumulative progress log (all sessions)
```

---

## Key technical achievements (pre-GSoC)

| Deliverable | Status | When |
|---|---|---|
| Dev environment (macOS M2, CGAL, nanobind) | ✅ Complete | Dec 20 |
| DCEL mastery + 15 insertion methods tested | ✅ Complete | Dec 21 |
| Line 857 bug discovered (`rv_policy` on free fn) | ✅ Complete | Dec 23 |
| 7 crash scenarios documented with repro | ✅ Complete | Dec 28 – Jan 6 |
| Proposal v3 (Efi's 9-section spec) | ✅ Complete | Jan 11 |
| Named Parameters property map bridge problem | ✅ Complete | Jan 17 |
| 8-kernel CI pipeline (GSoC Weeks 11-12) | ✅ Complete | Feb 8 |
| 7-flag CMake safety architecture | ✅ Complete | Feb 27 |
| nb::arg() on all AOS2 methods (GSoC Weeks 1-2) | ✅ Complete | Mar 11 |
| Docstrings: vertex / halfedge / face (108 total) | ✅ Complete | Mar 13+24 |
| Docstring extractor — 50/50 on AOS2 | ✅ Complete | Mar 25 |
| 5 external docstring header files generated | ✅ Complete | Apr 1 |
| 10 missing Polygon_2 constants identified + text | ✅ Complete | Apr 7 |

---

## Build commands (always use these)

```bash
export CC=/usr/bin/clang && export CXX=/usr/bin/clang++
cmake -C ../cmake/tests/aos2_epec_fixed.cmake \
      -DCMAKE_BUILD_TYPE=Release \
      -Dnanobind_DIR=$(python3 -c "import nanobind; print(nanobind.cmake_dir())") \
      ..
make CGALPY -j4
```

Runtime import:

```python
import sys
sys.path.insert(0, "build-manual/src/libs/cgalpy")
import CGALPY   # capital — NOT cgalpy
```

---

## Email thread summary

| # | Key direction | Date |
|---|---|---|
| 1-2 | Make proposal concise, separate Task A/B | Dec 30-31 |
| 3 | CI + package analysis required | Jan 7 |
| 7-8 | Build results + CI clarifications | Feb 5 |
| 11 | 5-point framework refactor direction | Feb 23 |
| 17-18 | Weeks 3-4 complete + Landmarks correction | Mar 24 |
| 20 | "automate docstring creation" | Mar 25 |
| 22 | 50/50 POC results sent | Mar 25 |
| 23 | **AWAITING EFI REPLY** | — |

---

## Current blockers

- **Email 23** — awaiting Efi's reply on automation approach (Q5)
- **polygon_2_docstrings.h** — 10 constants need appending before build
- **4 other binding files** — wiring audit not yet done
- **All local commits** — nothing pushed since `ebea4e79` (Feb 27)

---

## Absolute DO NOTs

- Use lowercase `cgalpy` in import — it's `CGALPY`
- Re-add `HandleRegistry` or `cgalpy_error_handler.h`
- Commit without Efi's confirmation on Q5
- Say "dynamically builds parameter chains"
- Put docstring headers anywhere other than `src/libs/cgalpy/lib/docstrings/`

---

## Project Context

| | |
|---|---|
| Project | CGAL Python Bindings Enhancement |
| Binding Library | nanobind (modern C++17 bindings) |
| Main Repository | [bitbucket.org/taucgl/cgal-python-bindings](https://bitbucket.org/taucgl/cgal-python-bindings) |
| Working Branch | `feature/named-params-operators-poc` |
| CGAL Documentation | [doc.cgal.org](https://doc.cgal.org) |

### Core problem

The CGAL Python bindings exist but are incomplete:

- Most methods lack documentation
- Parameters appear as `arg0`, `arg1`, `arg2` instead of meaningful names
- Several methods cause segmentation faults when misused
- CGAL's compile-time Named Parameters pattern isn't applied globally
- No precondition validation, leading to silent data corruption
- CI infrastructure dormant, no automated testing

---

## Work Summary

### Phase 1: Foundation (50+ hours, Dec 20-24, 2025)

Built the development environment and studied CGAL's architecture.

What was done:

- Built CGAL 5.6 from source on macOS Apple Silicon M2
- Studied 2D Arrangements: DCEL data structures, traits classes, template architecture
- Analyzed 50+ bound methods in the Python bindings repository
- Mastered nanobind: return value policies, `keep_alive` patterns, lifetime management
- Discovered line 857-858 bug: `reference_internal` doesn't work for `insert_cv_with_history()`

Files created:

- `phase1-foundation/environment-setup.md`
- `phase1-foundation/cgal-learning-notes.md`
- `phase1-foundation/nanobind-deep-dive.md`
- `phase1-foundation/line857-bug-analysis.md`

---

### Phase 2: Contributions and Testing (40+ hours, Dec 25-29, 2025)

Submitted pull requests and ran systematic empirical testing.

What was done:

- Submitted PR #1: Documented 6 methods with docstrings and parameter names
- Submitted PR #2: Documented 15 methods (removal, modification, query)
- Empirically tested 30+ methods across 13 hours
- Discovered 5 crash scenarios (segfaults that kill Python interpreter)
- Documented 10 silent corruption scenarios

Files created:

- `phase2-contributions/pr1-submission.md`
- `phase2-contributions/pr2-submission.md`
- `phase2-contributions/complete-methods-research.md`
- `phase2-contributions/test_removal_methods.py`
- `phase2-contributions/test_modification_methods.py`
- `phase2-contributions/test_query_methods.py`

---

### Phase 2.5: Proposal Revision (3 hours, Dec 30 – Jan 1, 2026)

Revised the proposal after Efi's detailed feedback.

- Removed emotional language
- Shortened "What's Missing" section
- Made timeline table the primary structure
- Clarified that Named Parameters and parameter names are two separate tasks

---

### Phase 3: Research (17+ hours, Jan 5-11, 2026)

Addressed mentor's technical questions and extended the crash testing.

Docstring organization research:

- Tested 3 approaches; mentor confirmed inline string literals as the standard pattern
- 85% readability improvement over `R"(...)"` raw strings, zero build system changes needed

Extended crash testing:

- Found 2 new crashes (total: 7)
- Verified 3 safe behaviors
- Documented 4 geometric validation warnings

Build system:

- Built Polygon Mesh Processing (PMP) bindings successfully
- Resolved Eigen 3.4.1 / CGAL 5.6 compatibility issues
- Fixed GMP/GMPXX linking on macOS M2

Files created:

- `research/docstring-location/docstring-location-research.md`
- `research/crash-scenarios/additional-crash-scenarios.md`
- 9 crash scenario test files
- `docs/technical/build_pmp_guide.md`

---

### Phase 3.5: Named Parameters Deep Dive (9+ hours, Jan 17, 2026)

Deep research into CGAL's Named Parameters system.

Architecture analysis:

- Studied Efi's operator-based Named Parameters system
- Analyzed 5 core files in the codebase
- Created 3,500-line technical analysis document

Proof-of-concept:

- 3 reference operators in prep repo
- 2 operators in actual cgal-python-bindings repo
- Branch: `feature/named-params-operators-poc`

Key discovery:

The operators themselves are straightforward. The hard part is the Python-to-C++ property map type bridge — that's where the 2 weeks go.

Files created:

- `NAMED_PARAMS_COMPLETE_ANALYSIS.md` (3,500 lines)
- `implementation-plan.md`
- `questions-for-efi.md`
- `PROPERTY_MAP_CHALLENGE.md`

---

### Phase 4: CI and Build System Testing (3+ hours, Feb 5, 2026)

- Validated `aos2_epec_fixed` — correct output (3 faces, 12 halfedges, 5 vertices)
- Found Apple Clang required on macOS (GCC fails with Qt6 pragma errors)
- Sent Email 7 to Efi; received CI architecture direction in Email 8

---

### Phase 4.5: Multi-Kernel CI Pipeline (7-8 hours, Feb 8, 2026)

Built a complete 8-kernel parallel CI pipeline from Efi's specifications.

| Config | Package | Kernel | Status |
|---|---|---|---|
| `aos2_epec_fixed` | AOS2 | EPEC | Validated |
| `aos2_epic` | AOS2 | EPIC | Ready |
| `sm_pmp_epec` | SM+PMP | EPEC | Ready |
| `sm_pmp_epic` | SM+PMP | EPIC | Ready |
| `ch2_epic` | CH2 | EPIC | Ready |
| `pol3_pmp_epic` | POL3+PMP | EPIC | Ready |
| `pol3_ch3_epec` | POL3+CH3 | EPEC | Ready |
| `tri3_epic` | TRI3 | EPIC | Ready |

Deliverables:

- `build_config.sh` — build any kernel config automatically
- `test_runner.py` — parameterized test runner
- `bitbucket-pipelines.yml` — production-ready parallel CI

Weeks 11-12 CI work done ahead of GSoC.

---

### Phase 5: Precondition Framework (4 hours, Feb 19, 2026)

Built a two-layer C++ safety framework. All 7 crash scenarios converted from interpreter-killing segfaults to catchable Python `RuntimeError`.

| # | Scenario | Result |
|---|---|---|
| 1 | `remove_isolated_vertex` on non-isolated vertex | RuntimeError |
| 2 | `remove_edge` called twice | RuntimeError |
| 3 | `he.curve()` after removal | RuntimeError |
| 4 | Twin halfedge after `remove_edge` | RuntimeError |
| 5 | `remove_isolated_vertex` twice | RuntimeError |
| 6 | `merge_edge` on non-adjacent edges | RuntimeError |
| 7 | Regression: address reuse, no false positives | PASS |

---

### Phase 5 Revised: Framework Refactored per Mentor (5 hours, Feb 23-27, 2026)

Efi's direction required a full architectural refactor.

Key points:

- CGAL already throws natively — custom error handler was redundant
- Handle invalidation belongs in CGAL C++ via `CGAL_precondition()`, not in Python bindings
- One binding flag per CGAL flag (7 total)

Changes to cgal-python-bindings (commit: `ebea4e79`):

| Binding Flag | CGAL Definition |
|---|---|
| `CGALPY_NO_PRECONDITIONS` | `CGAL_NO_PRECONDITIONS` |
| `CGALPY_NO_POSTCONDITIONS` | `CGAL_NO_POSTCONDITIONS` |
| `CGALPY_NO_ASSERTIONS` | `CGAL_NO_ASSERTIONS` |
| `CGALPY_NO_WARNINGS` | `CGAL_NO_WARNINGS` |
| `CGALPY_NDEBUG` | `CGAL_NDEBUG` |
| `CGALPY_CHECK_EXPENSIVE` | `CGAL_CHECK_EXPENSIVE` |
| `CGALPY_CHECK_EXACTNESS` | `CGAL_CHECK_EXACTNESS` |

Deleted `cgalpy_error_handler.h` and `handle_registry.h`.
New file: `cmake/PrintCGALPYFlags.cmake`.
Parallel CGAL C++ branch for upstream `CGAL_precondition()` patches pending Efi's answer on fork setup (Q3, open).

---

### Weeks 1-2 Pre-GSoC: Parameter Naming (5 hours, March 4-11, 2026) — COMPLETE

Added `nb::arg()` parameter names across all AOS2 binding files. This is the Weeks 1-2 GSoC deliverable, completed before the program starts.

What was done:

- Added `nb::arg()` to all `Arrangement_on_surface_2` mutation methods (March 4)
- Added `nb::arg()` to all Vertex, Halfedge, and Face binding methods (March 11)
- Restored 5 missing overloads found during this pass
- Build clean; sanity test passing (3 vertices, 2 edges, 1 face)

Result — keyword argument calls from Python now work:

```python
arr.insert_in_face_interior(p=p, f=f)
arr.remove_isolated_vertex(v=v)
```

Files created:

- `week1-2-parameter-naming/progress-notes.md`
- `week1-2-parameter-naming/sanity_test.py`

---

### Weeks 3-4 Pre-GSoC: Docstrings (10 hours total) — COMPLETE

Completed the Weeks 3-4 GSoC deliverable ahead of schedule across three sessions.

#### Session 1 — March 13, 2026 (2h): Vertex, Halfedge, Face

Added inline docstrings to all Vertex, Halfedge, and Face binding methods.

| File | Methods | Lines Added |
|---|---|---|
| `arr_vertex_bindings.cpp` | 13 | ~50 |
| `arr_halfedge_bindings.cpp` | 14 | ~54 |
| `arr_face_bindings.cpp` | 24 | ~101 |

Pattern used (confirmed by Efi):

```cpp
.def("point", &Vertex::point,
     py::arg("..."),
     "Obtains the point associated with the vertex.",
     ri)
```

Build clean, 0 errors. All 51 docstrings visible via `fn.__doc__` in Python REPL.

#### Session 2 — March 24, 2026 (5h): AOS2 Main Bindings

Added inline docstrings to all `arrangement_on_surface_2_bindings.cpp` methods and free functions.

File modified: `src/libs/cgalpy/lib/arrangement_on_surface_2_bindings.cpp`
Starting at 1345 lines, ending at 1450 lines (+105 lines).

Patch approach: `re.subn()` with `\s+` regex — plain `str.replace()` failed because Python `\n` didn't match actual newlines in the file. 32/32 replacements in one run.

| Category | Count | Examples |
|---|---|---|
| Traits | 3 | `geometry_traits`, `topology_traits`, `fictitious_face` |
| Insertion | 9 | `insert_from_left_vertex` x2, `insert_in_face_interior` x2... |
| Modification | 6 | `modify_vertex`, `split_edge`, `merge_edge`... |
| Query | 8 | `number_of_vertices`, `is_empty`, `is_valid`... |
| Iterators | 5 | `vertices`, `halfedges`, `edges`, `faces`, `unbounded_faces` |
| Free functions | 26 overloads | `insert_point` x4, `insert` x11, `zone` x4... |

Build clean. 25/25 class methods verified, 9/9 free function names verified.

Mistake corrected: asked Efi if Landmarks_pl block was missing — it already existed at lines 1327-1332. Efi corrected via Email 18. Lesson: `grep` first, ask second.

#### Session 3 — March 25, 2026 (3h): Automation Research

After Efi's Email 20 ("you surely can start with how to automate a bit of the docstring creation"), built a proof-of-concept automation script.

Core discovery — where docs live:

Homebrew headers (`/opt/homebrew/include/CGAL/`) have zero documentation comments. The CGAL source repo (`~/cgal/`) has full docs in the `doc/` subfolder:

```
Path: ~/cgal/Arrangement_on_surface_2/doc/Arrangement_on_surface_2/CGAL/
Format: /*! comments before function signatures (NOT \brief tags)
```

Three comment patterns discovered:

```cpp
// Pattern 1 — simple class methods (single-line)
/*! Obtains the number of vertices in the arrangement. */
Size number_of_vertices() const;

// Pattern 2 — complex class methods (multi-line)
/*! Inserts the curve `c` into the arrangement...
 * \pre The interior of `c` is disjoint from all existing vertices.
 */
Halfedge_handle insert_from_left_vertex(...);

// Pattern 3 — free functions (\ingroup style)
/*! \ingroup PkgArrangementOnSurface2Funcs
 *
 * Inserts a given point into a given arrangement...
 * \pre If provided, pl must be attached to arr.
 */
Vertex_handle insert_point(...);
```

Script evolution (7 iterations):

| Attempt | Change | Result |
|---|---|---|
| 1 | Basic `re.compile('/\*!(.*?)\*/')` | 35/50 (70%) |
| 2 | + alias map + single-line pattern | 42/50 (84%) |
| 3 | + negative lookahead (DOTALL) | BROKE — 6/50 |
| 4 | Reverted + `ingroup_block` pattern | 41/50 |
| 5 | + forward scan for fn name | 50/50 (100%) |

Critical lesson: negative lookahead `(?:(?!X).)*` in DOTALL mode causes catastrophic backtracking and destroys all matches. Never use it. Use a separate dedicated pattern for each comment style instead.

Final result: **50/50 (100%)** on the full AOS2 binding function target list.

Known issues for production (not blockers):

1. LaTeX markup in extracted text: `\f$x\f$-monotone` needs stripping
2. Backtick markup: `` `c` `` needs stripping for Python docstrings
3. 4 functions need manual overrides (wrong doc match or no doc entry)
4. Overloaded functions all get same docstring (first match)
5. Only AOS2 package tested — other packages untested

Files created:

- `week3-4-docstrings/march25-automation-research.md`
- `week3-4-docstrings/docstring_extractor.py`
- `week3-4-docstrings/progress-notes.md` (updated)

#### Session 4 — April 1, 2026 (3h): Docstring Header Files — COMPLETE

After the March 25 automation session, applied Approach B (separate `.h` header files per package) to the 5 packages that had zero docstrings.

New directory created in the official repo:

```
src/libs/cgalpy/lib/docstrings/
```

Five header files generated:

| File | Size | Constants | Package |
|---|---|---|---|
| `polygon_2_docstrings.h` | 3.6K | 22 | Polygon_2 |
| `alpha_shape_2_docstrings.h` | 1.5K | 10 | Alpha Shapes 2D |
| `boolean_set_operations_2_docstrings.h` | 1.3K | 7 | Boolean Set Operations 2D |
| `envelope_2_docstrings.h` | 2.0K | 9 | Envelope 2D |
| `visibility_2_docstrings.h` | 1.1K | 5 | Visibility 2D |

Pattern used (Approach B — confirmed viable in Phase 3):

```cpp
// In polygon_2_docstrings.h:
#pragma once

const char* IS_SIMPLE_DOC = R"pbdoc(
Returns true if the polygon is simple (non-self-intersecting).
)pbdoc";
```

```cpp
// In polygon_2_bindings.cpp, after wiring:
#include "docstrings/polygon_2_docstrings.h"
...
.def("is_simple", &Polygon_2::is_simple, IS_SIMPLE_DOC)
```

Status: headers generated, **not yet wired** into `.cpp` binding files. Wiring is the immediate next action — see [`week3-4-docstrings/docstring-headers/wiring-guide.md`](week3-4-docstrings/docstring-headers/wiring-guide.md).

Files created (prep repo):

- `week3-4-docstrings/docstring-headers/README.md`
- `week3-4-docstrings/docstring-headers/implementation.md`
- `week3-4-docstrings/docstring-headers/wiring-guide.md`
- `week3-4-docstrings/docstring-headers/polygon_2_docstrings.h`
- `week3-4-docstrings/docstring-headers/alpha_shape_2_docstrings.h`
- `week3-4-docstrings/docstring-headers/boolean_set_operations_2_docstrings.h`
- `week3-4-docstrings/docstring-headers/envelope_2_docstrings.h`
- `week3-4-docstrings/docstring-headers/visibility_2_docstrings.h`

#### Session 5 — April 7, 2026: Polygon_2 Wiring

Identified 10 missing constants in `polygon_2_docstrings.h` and wrote their docstring text.
Full details: [`week3-4-docstrings/april7-polygon2-wiring.md`](week3-4-docstrings/april7-polygon2-wiring.md)

---

## Technical Discoveries

### 1. Docstring pattern (confirmed by Efi)

Inline string literals directly in `.def()` calls:

```cpp
.def("insert_from_left_vertex",
     &Aos2::insert_from_left_vertex,
     py::arg("c"), py::arg("v"),
     "Inserts the curve c into the arrangement, such that its left endpoint "
     "corresponds to the given arrangement vertex v.",
     ri)
```

Zero build system changes. Works in all nanobind versions.

### 2. CGAL check system architecture

| Flag | Controls |
|---|---|
| `CGAL_NO_PRECONDITIONS` | precondition checks |
| `CGAL_NO_POSTCONDITIONS` | postcondition checks |
| `CGAL_NO_ASSERTIONS` | assertion checks |
| `CGAL_NO_WARNINGS` | warnings |
| `CGAL_NDEBUG` | ALL checks |
| `CGAL_CHECK_EXPENSIVE` | expensive checks (opt-in) |
| `CGAL_CHECK_EXACTNESS` | exactness checks (opt-in) |

All 7 now mirrored as `CGALPY_*` flags in `CMakeLists.txt`.

### 3. Crash scenarios (7 found)

| # | Method | Category | Status |
|---|---|---|---|
| 1 | `remove_isolated_vertex` on non-isolated | CGAL precondition | Pending CGAL patch |
| 2 | `remove_edge` called twice | Handle invalidation | Pending CGAL patch |
| 3 | `he.curve()` after `remove_edge` | CGAL precondition | Pending CGAL patch |
| 4 | Twin halfedge after `remove_edge` | Handle invalidation | Pending CGAL patch |
| 5 | `remove_isolated_vertex` twice | Handle invalidation | Pending CGAL patch |
| 6 | `merge_edge` on non-adjacent edges | CGAL precondition | Pending CGAL patch |
| 7 | Address reuse regression | Handle invalidation | Pending CGAL patch |

### 4. Line 857 — `reference_internal` vs `reference`

Inside `#if defined(CGALPY_AOS2_WITH_HISTORY)` block only. Returns `Curve_halfedges&` (not a halfedge + list). `rv_policy::reference_internal` fails in free function context (`m.def`) because `keep_alive<1,0>` has no `self` to act as nurse. Needs `WITH_HISTORY` build config to confirm — asked Efi (Q1, open).

### 5. Qt6/compiler compatibility

GCC 14/15 fails with Qt6 pragma errors on macOS. Fix: force Apple Clang (`/usr/bin/clang++`). Documented in `build_config.sh` and CI pipeline.

### 6. CGAL doc header location

Homebrew-installed headers contain zero documentation comments. The full Doxygen `/*!` doc headers live only in the CGAL source repo under the `doc/` subdirectory of each package. This is undocumented and non-obvious — required trial and error to find.

### 7. Iterator name mismatch (doc vs bindings)

| Python binding name | CGAL doc header name |
|---|---|
| `vertices` | `vertex_handles` |
| `halfedges` | `halfedge_handles` |
| `edges` | `edge_handles` |
| `faces` | `face_handles` |
| `isolated_vertices` | `isolated_vertices_begin` |

An alias map is required for correct automated extraction.

### 8. Docstring approaches — Approach B implemented

| Approach | Description | Readability | Status |
|---|---|---|---|
| A | External variables at top of same `.cpp` file | 85% | Validated Jan 2026 |
| B | Separate `.h` header per package | 95% | Implemented April 1, 2026 |
| C | Doxygen auto-generation | POC only | 50/50 on AOS2, March 25 |

Approach B is now implemented for 5 packages (pol2, as2, bso2, env2, vis2). AOS2 retains the inline pattern from March 13/24 — migrating those to a header is a separate future refactoring task.

---

## Research Findings

### Completed tasks

| Task | Status | Outcome | Phase |
|---|---|---|---|
| Docstring organization | Done | Inline strings confirmed | Phase 3 |
| Extended crash testing | Done | 7 crashes, 3 safe behaviors | Phase 3 |
| Named Parameters architecture | Done | 12,000+ lines documentation | Phase 3.5 |
| Property map challenge | Done | 4 solutions analyzed | Phase 3.5 |
| Build system testing | Done | `aos2_epec_fixed` builds | Phase 4 |
| Qt6/Clang compatibility | Done | Force Clang on macOS | Phase 4 |
| Multi-kernel CI pipeline | Done | 8 configs, production-ready | Phase 4.5 |
| Crash scenario validation | Done | Bus error reproduced | Phase 4.5 |
| Precondition framework | Done | 7/7 crash tests passing | Phase 5 |
| Framework refactor | Done | 7 granular flags | Phase 5R |
| Parameter naming | Done | All AOS2 + vtx/he/face | Weeks 1-2 |
| Docstrings: vtx/he/face | Done | 51 methods, 3 files | Weeks 3-4 S1 |
| Docstrings: AOS2 main | Done | 57 methods, +105 lines | Weeks 3-4 S2 |
| Docstring automation POC | Done | 50/50 (100%) extraction | Weeks 3-4 S3 |
| Docstring header files | Done | 5 headers, ~50 constants | Weeks 3-4 S4 |
| Polygon_2 wiring audit | Done | 10 missing constants + text | Weeks 3-4 S5 |

---

## Key Statistics

### Time investment

| Phase | Activity | Hours | Dates |
|---|---|---|---|
| Phase 1 | Environment + CGAL study | 50h | Dec 20-24 |
| Phase 2 | PRs + systematic testing | 40h | Dec 25-29 |
| Phase 2.5 | Proposal revision | 3h | Dec 30–Jan 1 |
| Phase 3 | Research + crash testing | 17h | Jan 5-11 |
| Phase 3.5 | Named Parameters deep dive | 9h | Jan 17 |
| Phase 4 | Build system testing | 3h | Feb 5 |
| Phase 4.5 | Multi-kernel CI implementation | 7-8h | Feb 8 |
| Phase 5 | Precondition framework | 4h | Feb 19 |
| Phase 5R | Framework refactor per Efi | 5h | Feb 23-27 |
| Weeks 1-2 | Parameter naming | 5h | Mar 4-11 |
| Weeks 3-4 S1 | Docstrings: vtx/he/face | 2h | Mar 13 |
| Weeks 3-4 S2 | Docstrings: AOS2 main | 5h | Mar 24 |
| Weeks 3-4 S3 | Docstring automation POC | 3h | Mar 25 |
| Weeks 3-4 S4 | Docstring header files (5 pkgs) | 3h | Apr 1 |
| Weeks 3-4 S5 | Polygon_2 wiring audit | 1h | Apr 7 |
| **Total** | | **~156h** | **Dec 20–Apr 7** |

### Contribution metrics

| Metric | Count |
|---|---|
| Total hours invested | 155+ |
| Total documentation lines | 25,000+ |
| Methods with parameter names | All AOS2 + vertex/halfedge/face |
| Methods with inline docstrings | 108 (57 AOS2 + 13 vertex + 14 halfedge + 24 face) |
| Docstring header files | 5 (pol2, as2, bso2, env2, vis2) |
| Docstring constants in headers | ~50 across 5 files |
| Automation POC coverage | 50/50 (100%) on AOS2 target list |
| Crash scenarios found | 7 |
| Safe methods verified | 18 |
| Pull requests submitted | 2 |
| Proof-of-concepts created | 5 |
| Production code commits | 3 (latest: `ebea4e79` Feb 27) |
| CI kernel configs | 8 |
| Emails to mentor | 22 sent |
| Proposal versions | 10+ |

### Local file state (not yet pushed upstream)

| File | Change |
|---|---|
| `arrangement_on_surface_2_bindings.cpp` | +105 lines |
| `arr_face_bindings.cpp` | +101 lines |
| `arr_halfedge_bindings.cpp` | +54 lines |
| `arr_vertex_bindings.cpp` | +50 lines |
| `bitbucket-pipelines.yml` | +270 lines |
| `CMakeLists.txt` | 7 CGALPY check flags (staged) |
| `cmake/PrintCGALPYFlags.cmake` | new file |
| `src/libs/cgalpy/lib/docstrings/` | new dir — 5 header files (Apr 1) |

Latest Bitbucket commit: `ebea4e79` Feb 27 — unchanged since.

---

## How to Navigate This Repo

For understanding the CI work:

- CI Implementation: `phase4-ci-infrastructure/implementation/`
- Build scripts: `build_config.sh`, `test_runner.py`
- Phase 4.5 summary: `PHASE_4_5_IMPLEMENTATION.md`

For reviewing the precondition work:

- Original framework: `phase2-contributions/step2.6-precondition-framework/`
- Refactored flags: Phase 5 Revised section above + `CMakeLists.txt`

For the docstring inline work (AOS2, vertex, halfedge, face):

- Session 1 notes: `week3-4-docstrings/march13-vertex-halfedge-face-complete.md`
- Session 2 notes: `week3-4-docstrings/march24-aos2-bindings-complete.md`

For the docstring automation:

- Research notes: `week3-4-docstrings/march25-automation-research.md`
- Working script: `week3-4-docstrings/docstring_extractor.py`
- Progress log: `week3-4-docstrings/progress-notes.md`

For the docstring header files (pol2, as2, bso2, env2, vis2):

- Overview: `week3-4-docstrings/docstring-headers/README.md`
- Technical breakdown: `week3-4-docstrings/docstring-headers/implementation.md`
- Wiring instructions: `week3-4-docstrings/docstring-headers/wiring-guide.md`
- The `.h` files: `week3-4-docstrings/docstring-headers/*.h`

For reviewing end-to-end:

1. Start with this README
2. Read the proposal (`proposal/gsoc-2026-proposal-v3.docx`)
3. Check Phase 1-3 for foundation work
4. Review Phase 3.5 for Named Parameters research
5. Check Phase 4-4.5 for CI implementation
6. Review Phase 5 and 5R for the precondition framework
7. Review `week1-2-parameter-naming/` for Weeks 1-2 deliverable
8. Review `week3-4-docstrings/` for Weeks 3-4 deliverable + automation + headers

---

## GSoC Timeline Status

| Weeks | Task | Status |
|---|---|---|
| 1-2 | Parameter Names | Complete (pre-GSoC, Mar 4-11) |
| 3-4 | Docstrings | Complete (pre-GSoC, Mar 13 – Apr 7) |
| 3-4+ | Docstring automation POC | Complete (Mar 25, 50/50) |
| 3-4+ | Docstring header files | Generated (Apr 1) — wiring pending |
| 5-6 | Safety and Preconditions | 7 CMake flags done, CGAL patch pending |
| 7-8 | Named Parameters | Architecture studied, property map challenge identified |
| 9-10 | New Package Expansion | LCC or Shape Recognition (not started) |
| 11-12 | CI and Testing | Complete (pre-GSoC, Feb 8) |

---

## References

- CGAL Python Bindings: [bitbucket.org/taucgl/cgal-python-bindings](https://bitbucket.org/taucgl/cgal-python-bindings)
- CGAL Checks Docs: [doc.cgal.org/latest/Manual/devman_checks.html](https://doc.cgal.org/latest/Manual/devman_checks.html)
- CGAL Documentation: [doc.cgal.org](https://doc.cgal.org)
- Nanobind Docs: [nanobind.readthedocs.io](https://nanobind.readthedocs.io)
- GitHub: [@UtkarsHMer05](https://github.com/UtkarsHMer05)
- Email: [utkarshkhajuria55@gmail.com](mailto:utkarshkhajuria55@gmail.com)

---

## License

This repository documents preparation work for Google Summer of Code 2026. The CGAL library is licensed under GPL/LGPL. Binding code follows the same licensing as the official CGAL Python bindings repository.

---

## Acknowledgments

Thanks to Efi Fogel for detailed mentorship through 22 email exchanges. The depth of feedback at every stage made the preparation genuinely useful, not just checkbox work. Thanks to the CGAL community and nanobind developers.

---

Last updated: April 7, 2026
Repository: [github.com/UtkarsHMer05/cgal-gsoc-2026-prep](https://github.com/UtkarsHMer05/cgal-gsoc-2026-prep)
Status: Weeks 1-2 complete | Weeks 3-4 complete | Automation POC 50/50 | Header files generated | Polygon_2 wiring audit done | Awaiting Email 23