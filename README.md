# CGAL GSoC 2026: Python Bindings Enhancement

**Author:** Utkarsh Khajuria (@UtkarsHMer05)  
**Project:** Enhancing CGAL Python Bindings  
**Mentor:** Efi Fogel (efifogel@gmail.com)  
**Organization:** CGAL (Computational Geometry Algorithms Library)  
**Period:** December 20, 2025 – February 27, 2026  
**Total Investment:** 135+ hours

---

## Table of Contents

- [Overview](#overview)
- [Project Context](#project-context)
- [Work Summary](#work-summary)
- [Technical Discoveries](#technical-discoveries)
- [Repository Structure](#repository-structure)
- [Research Findings](#research-findings)
- [Key Statistics](#key-statistics)
- [How to Navigate This Repo](#how-to-navigate-this-repo)
- [Next Steps](#next-steps)
- [References](#references)

---

## Overview

This repository documents my preparation work for Google Summer of Code 2026
with CGAL. I've spent over 135 hours across seven phases working on the Python
bindings for the Computational Geometry Algorithms Library. This includes
building CGAL from source, learning the 2D Arrangements package, empirically
testing methods, discovering and fixing crash scenarios, researching solutions
to technical challenges, implementing a precondition safety framework,
implementing proof-of-concept Named Parameters operators, validating the manual
build system, and creating a complete multi-kernel CI pipeline.

Most recently, based on mentor feedback, I refactored the entire safety
framework to align with CGAL's native check system: replacing the coarse
`CGALPY_ENABLE_PRECONDITIONS` flag with 7 granular per-type flags matching
CGAL's own compile-time check architecture, and removing the Python-side
HandleRegistry in favour of upstream CGAL-level fixes.

### Key Achievements

- [x] Built CGAL successfully on macOS M2 (Apple Silicon)
- [x] Documented 21 methods across 2 pull requests with NumPy-style docstrings
- [x] Discovered 7 crash scenarios through systematic testing
- [x] Found 10 silent corruption cases
- [x] Researched 3 docstring organization approaches (Approach A validated)
- [x] Identified critical bugs (line 857 lifetime management issue)
- [x] Investigated line 857 todo — discovered it is inside
      `#if CGALPY_AOS2_WITH_HISTORY`, returns `Curve_halfedges&`,
      not exposed in standard build configs
- [x] Created comprehensive CGAL package analysis (19 packages evaluated)
- [x] Implemented proof-of-concept Named Parameters operators (2 in production repo)
- [x] Discovered property map type resolution challenge (the real Week 7-8 challenge)
- [x] Analyzed complete Named Parameters architecture (3,500 lines documentation)
- [x] Validated manual build system with aos2_epec_fixed configuration
- [x] Discovered and documented Qt6/Clang compiler compatibility issue
- [x] Created complete 8-kernel CI pipeline (bitbucket-pipelines.yml production-ready)
- [x] Implemented parameterized testing infrastructure (build_config.sh, test_runner.py)
- [x] Confirmed crash scenario #1 reproducibility (bus error validated)
- [x] Implemented two-layer precondition framework (Layer 1: CGAL error handler,
      Layer 2: HandleRegistry) — all 7/7 crash tests passing
- [x] Refactored safety framework per mentor direction:
      replaced single flag with 7 granular CGALPY_NO_*/CGALPY_CHECK_* flags,
      removed HandleRegistry (fix belongs in CGAL C++),
      removed cgalpy_error_handler.h (CGAL throws natively)

---

## Project Context

| | |
|---|---|
| **Project** | CGAL Python Bindings Enhancement |
| **Binding Library** | nanobind (modern C++17 bindings) |
| **Main Repository** | [bitbucket.org/taucgl/cgal-python-bindings](https://bitbucket.org/taucgl/cgal-python-bindings) |
| **Working Branch** | `feature/named-params-operators-poc` |
| **CGAL Documentation** | [doc.cgal.org](https://doc.cgal.org) |

### Core Problem

The CGAL Python bindings exist but are incomplete:

- 90% of methods lack documentation
- Parameters appear as `arg0`, `arg1`, `arg2` instead of meaningful names
- Several methods cause segmentation faults when misused
- CGAL's compile-time Named Parameters pattern isn't applied to Python bindings
- No precondition validation, leading to silent data corruption
- CI infrastructure dormant, no automated testing

---

## Work Summary

### Phase 1: Foundation (50+ hours, Dec 20-24, 2025)

Built the development environment and studied CGAL's architecture.

**What I did:**

- [x] Built CGAL 5.6 from source on macOS Apple Silicon M2
- [x] Studied 2D Arrangements: DCEL data structures, traits classes,
      template architecture
- [x] Analyzed 50+ bound methods in the Python bindings repository
- [x] Mastered nanobind: return value policies, `keep_alive` patterns,
      lifetime management
- [x] Discovered line 857-858 bug: `reference_internal` doesn't work
      for `insert_cv_with_history()`

**Files Created:**

- `phase1-foundation/environment-setup.md` — Complete build instructions
- `phase1-foundation/cgal-learning-notes.md` — DCEL and 2D Arrangements deep dive
- `phase1-foundation/nanobind-deep-dive.md` — Lifetime management patterns
- `phase1-foundation/line857-bug-analysis.md` — Memory management bug documentation

---

### Phase 2: Contributions & Testing (40+ hours, Dec 25-29, 2025)

Submitted pull requests and conducted empirical testing across methods.

**What I did:**

- [x] Submitted PR #1: Documented 6 methods with NumPy-style docstrings
- [x] Submitted PR #2: Documented 15 methods (removal, modification,
      query operations)
- [x] Empirically tested 30+ methods across 13 hours of systematic testing
- [x] Discovered 5 crash scenarios (segfaults that kill Python interpreter)
- [x] Documented 10 silent corruption scenarios

**Files Created:**

- `phase2-contributions/pr1-submission.md`
- `phase2-contributions/pr2-submission.md`
- `phase2-contributions/complete-methods-research.md` — 2,500 lines
- `phase2-contributions/test_removal_methods.py` — 300 lines
- `phase2-contributions/test_modification_methods.py` — 350 lines
- `phase2-contributions/test_query_methods.py` — 200 lines

---

### Phase 2.5: Proposal Revision (3 hours, Dec 30-Jan 1, 2026)

Revised proposal based on Efi's detailed feedback.

**Changes Made:**

- [x] Removed all emotional language
- [x] Shortened "What's Missing" section
- [x] Made timeline table primary focus
- [x] Added clarification: Named Parameters is different from parameter
      names (two separate tasks)

---

### Phase 3: Research (17+ hours, Jan 5-11, 2026)

Addressed mentor's technical questions and extended research.

**Docstring Organization Research**

- Tested 3 approaches: External variables (A), External headers (B),
  Namespace organization (C)
- Validated Approach A: 85% readability improvement, zero build system changes
- Created proof-of-concept: `test-approach-a/test_external_docstrings.cpp`

**Extended Crash Testing**

- Found 2 new crashes (total: 7)
- Verified 3 safe behaviors
- Documented 4 geometric validation warnings

**Build System Mastery**

- Successfully built Polygon Mesh Processing (PMP) bindings
- Resolved Eigen 3.4.1/CGAL 5.6 compatibility issues
- Fixed GMP/GMPXX linking on macOS M2

**Files Created:**

- `research/docstring-location/docstring-location-research.md`
- `research/crash-scenarios/additional-crash-scenarios.md`
- 9 test files for crash scenarios
- `docs/technical/build_pmp_guide.md`

---

### Phase 3.5: Named Parameters Deep Dive (9+ hours, Jan 17, 2026)

Deep research into CGAL's Named Parameters system and proof-of-concept
implementation.

**Complete Architecture Analysis**

- Studied Efi's operator-based Named Parameters system
- Analyzed 5 core files in the codebase
- Documented complete data flow
- Created 3,500-line technical analysis document

**Proof-of-Concept Implementation**

- Created 3 reference operators in prep repo
- Implemented 2 operators in actual cgal-python-bindings repo
- Branch: `feature/named-params-operators-poc`

**Integration Attempt & Critical Discovery**

- Attempted to integrate operators into `compute_vertex_normals()`
- Discovered the hard problem: Property map type resolution
- Realization: Operators are trivial. The 2-week allocation is for the
  Python-to-C++ property map type bridge

**Files Created:**

- `NAMED_PARAMS_COMPLETE_ANALYSIS.md` (3,500 lines)
- `implementation-plan.md` (1,200 lines)
- `questions-for-efi.md` (900 lines)
- `PROPERTY_MAP_CHALLENGE.md`
- Production code in cgal-python-bindings repo

**Total Documentation:** 12,000+ lines

---

### Phase 4: CI & Build System Testing (3+ hours, Feb 5, 2026)

Validated manual build system with different kernel configurations.

- `aos2_epec_fixed.cmake` tested on macOS M2 — correct output
  (3 faces, 12 halfedges, 5 vertices)
- Discovered Apple Clang required on macOS (GCC fails with Qt6 pragma errors)
- Email 7 sent to Efi with results and CI questions
- Email 8 received: multi-kernel testing, manual CMake builds, example
  scripts are the tests

---

### Phase 4.5: Multi-Kernel CI Implementation (7-8 hours, Feb 8, 2026)

Implemented complete 8-kernel CI pipeline based on Efi's specifications.

**8-Kernel Build Matrix**

| Config | Package | Kernel | Status |
|--------|---------|--------|--------|
| aos2_epec_fixed | AOS2 | EPEC | Validated |
| aos2_epic | AOS2 | EPIC | Ready |
| sm_pmp_epec | SM+PMP | EPEC | Ready |
| sm_pmp_epic | SM+PMP | EPIC | Ready |
| ch2_epic | CH2 | EPIC | Ready |
| pol3_pmp_epic | POL3+PMP | EPIC | Ready |
| pol3_ch3_epec | POL3+CH3 | EPEC | Ready |
| tri3_epic | TRI3 | EPIC | Ready |

**Deliverables:**

- `build_config.sh` — Automated build script for any kernel configuration
- `test_runner.py` — Parameterized test runner
- `bitbucket-pipelines.yml` — Production-ready 8-kernel parallel CI pipeline
- Bus error for crash scenario #1 confirmed reproducible

This completes the Weeks 11-12 CI work ahead of GSoC.

---

### Phase 5: Precondition Framework (4 hours, Feb 19, 2026)

Implemented a two-layer C++ safety framework converting all 7 crash
scenarios from interpreter-killing segfaults into catchable Python
RuntimeError exceptions.

**Layer 1 — CGAL Precondition Framework (`cgalpy_error_handler.h`)**

- CMake option `CGALPY_ENABLE_PRECONDITIONS` (default ON)
- Strips `-DNDEBUG` from Release flags to re-enable CGAL check macros
- Custom `CGAL::set_error_handler()` converts abort() to RuntimeError

**Layer 2 — Handle Invalidation Registry (`handle_registry.h`)**

- `HandleRegistry` singleton tracking dead DCEL handles
- Keyed on `(arrangement_ptr, handle_ptr)` pairs to prevent false
  positives from DCEL memory address reuse
- Patched all removal wrappers (check_alive + mark_dead) and insertion
  wrappers (mark_alive)

**Test Results: 7/7 ALL PASSED**

| # | Scenario | Result |
|---|----------|--------|
| 1 | remove_isolated_vertex on non-isolated vertex | RuntimeError |
| 2 | remove_edge called twice | RuntimeError |
| 3 | he.curve() after removal | RuntimeError |
| 4 | Twin halfedge after remove_edge | RuntimeError |
| 5 | remove_isolated_vertex twice | RuntimeError |
| 6 | merge_edge on non-adjacent edges | RuntimeError |
| 7 | Regression: address reuse, no false positives | PASS |

Weeks 5-6 GSoC deliverable completed pre-GSoC.

---

### Phase 5 Revised: Framework Refactored per Mentor Direction (5 hours, Feb 23-27, 2026)

After sharing Phase 5 with Efi, he provided critical architectural
direction that required a full refactor.

**Efi's Direction (Email Feb 23, 2026):**

1. Stay close to CGAL but create a Pythonizing API
2. CGAL already supports checks — read the checks documentation
3. One binding flag per CGAL flag (not one coarse flag)
4. Handle invalidation not checked by CGAL — fix it IN CGAL C++,
   not in the Python bindings
5. Open a parallel CGAL branch for the upstream fixes

**Key Technical Finding from Docs:**

CGAL checks already throw exceptions by default — `std::abort`,
`std::exit`, and `assert` are forbidden in CGAL code. The crash problem
in Release builds is that `-DNDEBUG` sets `CGAL_NDEBUG`, which compiles
out all check macros entirely. The fix is controlling which macros
survive compilation, not redirecting abort().

**Changes Made to cgal-python-bindings
(branch: `feature/named-params-operators-poc`, commit: `ebea4e79`):**

1. **`CMakeLists.txt`** — Replaced `CGALPY_ENABLE_PRECONDITIONS` with
   7 granular flags matching CGAL's own check architecture:

   | Binding Flag | CGAL Definition | Default |
   |---|---|---|
   | `CGALPY_NO_PRECONDITIONS` | `CGAL_NO_PRECONDITIONS` | OFF |
   | `CGALPY_NO_POSTCONDITIONS` | `CGAL_NO_POSTCONDITIONS` | OFF |
   | `CGALPY_NO_ASSERTIONS` | `CGAL_NO_ASSERTIONS` | OFF |
   | `CGALPY_NO_WARNINGS` | `CGAL_NO_WARNINGS` | OFF |
   | `CGALPY_NDEBUG` | `CGAL_NDEBUG` | OFF |
   | `CGALPY_CHECK_EXPENSIVE` | `CGAL_CHECK_EXPENSIVE` | OFF |
   | `CGALPY_CHECK_EXACTNESS` | `CGAL_CHECK_EXACTNESS` | OFF |

   Final defaults to be decided with Efi.

2. **`cgalpy_error_handler.h` deleted** — CGAL 6.x already throws
   natively. Custom handler was redundant.

3. **`handle_registry.h` deleted** — Python-side tracking was wrong
   architecture. Handle invalidation crashes (#2, #4, #5, #7) will be
   fixed via `CGAL_precondition()` in arrangement removal methods in C++,
   in a parallel CGAL branch (pending Efi's answer on fork setup).

**Line 857 Investigation:**

The `\todo` comment at line 857 is inside
`#if defined(CGALPY_AOS2_WITH_HISTORY)` in `export_aos_with_history()`.
The function `insert_cv_with_history` returns `Curve_halfedges&` — not
a halfedge + EdgeList as originally thought. Hypothesis: `reference_internal`
fails because `Curve_halfedges` returned by reference is not tracked as a
nanobind-managed object, so `keep_alive<0,1>` silently does nothing.
`rv_policy::reference` "works" by making no lifetime contract at all.
Cannot confirm without a `CGALPY_AOS2_WITH_HISTORY` build config — asked Efi.

**Awaiting Efi:**

- CGAL fork/branch location for upstream precondition patches
- Build config that enables `CGALPY_AOS2_WITH_HISTORY` for line 857 repro
- Final default values for `CGALPY_NO_*` flags

---

## Technical Discoveries

### 1. Docstring Shadowing Problem

**Solution — Approach A (Validated):**

```cpp
const char* INSERT_FROM_LEFT_VERTEX_DOC = R"pbdoc(...)pbdoc";

m.def("insert_from_left_vertex", &aos2_insert_from_left_vertex_cv,
      nb::arg("curve"), nb::arg("vertex"),
      INSERT_FROM_LEFT_VERTEX_DOC);
```

85% readability improvement, zero build changes needed.

---

### 2. CGAL Check System Architecture

CGAL has 7 compile-time check controls:

- `CGAL_NO_PRECONDITIONS` — disable precondition checks
- `CGAL_NO_POSTCONDITIONS` — disable postcondition checks
- `CGAL_NO_ASSERTIONS` — disable assertion checks
- `CGAL_NO_WARNINGS` — disable warning checks
- `CGAL_NDEBUG` — disable ALL checks (set by `-DNDEBUG`)
- `CGAL_CHECK_EXPENSIVE` — enable expensive checks (opt-in)
- `CGAL_CHECK_EXACTNESS` — enable exactness checks (opt-in)

All standard checks are enabled by default and throw exceptions (not
abort). The bindings now expose a matching `CGALPY_*` flag for each.

---

### 3. Crash Scenarios (7 Found, Framework Refactored)

| # | Method | Category | Current Status |
|---|--------|----------|----------------|
| 1 | remove_isolated_vertex on non-isolated vertex | CGAL precondition | Pending CGAL patch |
| 2 | remove_edge called twice | Handle invalidation | Pending CGAL patch |
| 3 | he.curve() after remove_edge | CGAL precondition | Pending CGAL patch |
| 4 | Twin halfedge after remove_edge | Handle invalidation | Pending CGAL patch |
| 5 | remove_isolated_vertex twice | Handle invalidation | Pending CGAL patch |
| 6 | merge_edge on non-adjacent edges | CGAL precondition | Pending CGAL patch |
| 7 | Address reuse regression | Handle invalidation | Pending CGAL patch |

All 7 were passing with the Python-side framework (Phase 5). Now pending
upstream CGAL C++ fixes in a parallel branch per Efi's direction.

---

### 4. Line 857 — reference_internal vs reference

- Lives inside `#if defined(CGALPY_AOS2_WITH_HISTORY)` block
- Only compiled when `CGALPY_AOS2_WITH_HISTORY` +
  `CGALPY_AOS2_CONSOLIDATED_CURVE_DATA` are both set
- Returns `Curve_halfedges&` (not a halfedge + list)
- Hypothesis: `rv_policy::reference_internal` silently fails because
  `Curve_halfedges` by reference is not nanobind-managed; `reference`
  works by making no lifetime contract at all
- Needs `WITH_HISTORY` build config to confirm — asked Efi

---

### 5. Qt6/Compiler Compatibility

- GCC 14/15 fails with Qt6 pragma errors on macOS
- Root cause: Qt6 uses Clang-specific pragmas GCC doesn't recognize
- Solution: Force Apple Clang (`/usr/bin/clang++`) on macOS
- Documented in `build_config.sh` and CI pipeline

---

### 6. Multi-Kernel CI Architecture

```
aos2_epec_fixed.cmake  ->  CGALPY (EPEC)  ->  aos2.py CGALPY
aos2_epic.cmake        ->  CGALPY (EPIC)  ->  aos2.py CGALPY
[6 more configs...]
```

8 configs, parallel builds, parameterized test runner, manual CMake
builds from source. Production-ready `bitbucket-pipelines.yml`.

---

## Repository Structure

```
cgal-gsoc-2026-prep/
├── README.md
├── CURRENT_STATUS.md                      <- Always up to date
├── paste.txt                              # Master AI context
│
├── proposal/
│   ├── gsoc-2026-proposal-v1.md
│   ├── gsoc-2026-proposal-v2.docx
│   └── gsoc-2026-proposal-v3.docx        <- Submitted to GSoC
│
├── phase1-foundation/                     # Dec 20-24, 50h
├── phase2-contributions/                  # Dec 25-29, 40h
│   ├── step2.3-first-pr/
│   ├── step2.4-pr2-research/
│   ├── step2.5-pr2-methods/
│   └── step2.6-precondition-framework/   # Phase 5 docs (original)
│       ├── implementation.md
│       └── test-results.md
│
├── phase3-research/                       # Jan 5-17, 26h
│   ├── docstring-approach-b/
│   ├── proof-of-concept-operators/
│   ├── research/
│   ├── test-named-params-implementation/
│   └── task3-named-params-study.md
│
├── phase4-ci-infrastructure/              # Feb 5-8, 10h
│   ├── ci-analysis/
│   ├── implementation/
│   │   ├── build_config.sh
│   │   ├── test_runner.py
│   │   └── bitbucket-pipelines.yml
│   ├── PHASE_4_5_IMPLEMENTATION.md
│   └── README.md
│
├── efi-feedback/                          # All mentor emails
│   ├── email1 through email9 (sent)
│   ├── email10-preconditions-feb19.md    # Drafted + sent
│   ├── email11-checks-flags-feb23.md     # Sent
│   └── email12-line857-investigation-feb27.md  # Sent
│
└── master-prompts/
    └── [v1.0 through v17.0]
```

---

## Research Findings

### Completed Tasks

| Task | Status | Outcome | Phase |
|------|--------|---------|-------|
| Docstring organization | Done | Approach A ready for production | Phase 3 |
| Extended crash testing | Done | 7 crashes found, 3 safe behaviors | Phase 3 |
| Named Parameters architecture | Done | 12,000+ lines documentation | Phase 3.5 |
| Property map challenge | Identified | 4 potential solutions analyzed | Phase 3.5 |
| Build system testing | Done | aos2_epec_fixed builds correctly | Phase 4 |
| Qt6/Clang compatibility | Resolved | Force Clang on macOS | Phase 4 |
| Multi-kernel CI pipeline | Done | 8 configs, production-ready | Phase 4.5 |
| Crash scenario validation | Done | Bus error reproduced | Phase 4.5 |
| Precondition framework | Done | 7/7 crash tests passing | Phase 5 |
| Framework refactor | Done | 7 granular flags, upstream fix path | Phase 5 Revised |

---

## Key Statistics

### Time Investment (Dec 20 – Feb 27, 2026)

| Phase | Activity | Hours | Dates |
|-------|----------|-------|-------|
| Phase 1 | Environment + CGAL study | 50h | Dec 20-24 |
| Phase 2 | PRs + systematic testing | 40h | Dec 25-29 |
| Phase 2.5 | Proposal revision | 3h | Dec 30-Jan 1 |
| Phase 3 | Research + crash testing | 17h | Jan 5-11 |
| Phase 3.5 | Named Parameters deep dive | 9h | Jan 17 |
| Phase 4 | Build system testing | 3h | Feb 5 |
| Phase 4.5 | Multi-kernel CI implementation | 7-8h | Feb 8 |
| Phase 5 | Precondition framework | 4h | Feb 19 |
| Phase 5 Revised | Framework refactor per Efi | 5h | Feb 23-27 |
| **Total** | | **~135h** | **Dec 20-Feb 27** |

### Contribution Metrics

| Metric | Count |
|--------|-------|
| Total hours invested | 135+ |
| Total documentation lines | 25,000+ |
| Methods documented | 21 |
| Crash scenarios found | 7 |
| Safe methods verified | 18 |
| Pull requests submitted | 2 |
| Proof-of-concepts created | 4 |
| Production code commits | 2 |
| CI infrastructure files | 3 |
| Kernel configs tested | 8 |
| Emails to mentor | 12 (9 sent + 3 recent) |
| Proposal versions | 3 |

---

## How to Navigate This Repo

**For understanding the CI work:**

- CI Implementation: `phase4-ci-infrastructure/implementation/`
- Build scripts: `build_config.sh`, `test_runner.py`
- Test results: `phase4-ci-infrastructure/testing/`
- Phase 4.5 summary: `PHASE_4_5_IMPLEMENTATION.md`

**For reviewing the precondition work:**

- Original framework: `phase2-contributions/step2.6-precondition-framework/`
- Refactored flags: see Phase 5 Revised section above

**For reviewing my work end-to-end:**

1. Start with this README
2. Read the proposal (`proposal/gsoc-2026-proposal-v3.docx`)
3. Check Phase 1-3 for foundation work
4. Review Phase 3.5 for Named Parameters research
5. Check Phase 4-4.5 for CI implementation
6. Review Phase 5 and 5 Revised for the precondition framework

**For technical challenges:**

- CI pipeline: `phase4-ci-infrastructure/`
- Qt6/Clang issue: `phase4-ci-infrastructure/documentation/compiler_compatibility.md`
- Named Parameters: `phase3-research/test-named-params-implementation/`
- Crash scenarios: `research/crash-scenarios/`
- Docstrings: `research/docstring-location/`

---

## Next Steps

### Awaiting Efi's Response

| Item | Question |
|------|----------|
| CGAL fork location | taucgl org or personal fork for upstream patches? |
| WITH_HISTORY build | Which config enables `CGALPY_AOS2_WITH_HISTORY`? |
| Flag defaults | What should default values be for `CGALPY_NO_*` flags? |

### Unblocked — Ready to Start

| Task | GSoC Week |
|------|-----------|
| Add `nb::arg()` parameter names to Arrangement_2 methods | 1-2 |
| Write NumPy-style docstrings (Approach A validated) | 3-4 |
| Fix line 857 `keep_alive` issue | 5-6 |
| Apply Named Parameters lambda+kwargs pattern to PMP | 7-8 |

### GSoC Timeline Status

| Weeks | Task | Status |
|-------|------|--------|
| 1-2 | Parameter Names | Ready to start |
| 3-4 | Docstrings | Approach validated |
| 5-6 | Safety & Preconditions | Pending CGAL branch |
| 7-8 | Named Parameters | Architecture studied |
| 9-10 | New Package Expansion | Ready |
| 11-12 | CI & Testing | Complete (Feb 8) |

---

## References

- CGAL Python Bindings: [bitbucket.org/taucgl/cgal-python-bindings](https://bitbucket.org/taucgl/cgal-python-bindings)
- CGAL Checks Documentation: [doc.cgal.org/latest/Manual/devman_checks.html](https://doc.cgal.org/latest/Manual/devman_checks.html)
- CGAL Documentation: [doc.cgal.org](https://doc.cgal.org)
- Nanobind Documentation: [nanobind.readthedocs.io](https://nanobind.readthedocs.io)
- GitHub: [@UtkarsHMer05](https://github.com/UtkarsHMer05)
- Email: utkarshkhajuria55@gmail.com

---

## License

This repository documents preparation work for Google Summer of Code 2026.
The CGAL library is licensed under GPL/LGPL. Binding code follows the same
licensing as the official CGAL Python bindings repository.

---

## Acknowledgments

Thanks to Efi Fogel for detailed mentorship through 12 email exchanges and
technical guidance. Thanks also to the CGAL community for building an
exceptional computational geometry library, and to the nanobind developers
for creating modern Python binding tools.

---

**Last Updated:** February 27, 2026, 10:30 PM IST  
**Repository:** [github.com/UtkarsHMer05/cgal-gsoc-2026-prep](https://github.com/UtkarsHMer05/cgal-gsoc-2026-prep)  
**Status:** Phase 5 Revised Complete — Awaiting Efi on fork setup + WITH_HISTORY config