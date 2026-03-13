# CGAL GSoC 2026: Python Bindings Enhancement

**Author:** Utkarsh Khajuria (@UtkarsHMer05)  
**Project:** Enhancing CGAL Python Bindings  
**Mentor:** Efi Fogel (efifogel@gmail.com)  
**Organization:** CGAL (Computational Geometry Algorithms Library)  
**Period:** December 20, 2025 – March 13, 2026  
**Total Investment:** 139+ hours

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
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

This repository documents my preparation work for Google Summer of Code 2026
with CGAL. I've spent 139+ hours across nine phases working on the Python
bindings for the Computational Geometry Algorithms Library. This includes
building CGAL from source, learning the 2D Arrangements package, empirically
testing methods, discovering crash scenarios, researching solutions to
technical challenges, implementing a precondition safety framework,
implementing proof-of-concept Named Parameters operators, validating the
manual build system, creating a complete multi-kernel CI pipeline, and
completing the Weeks 1-2 GSoC deliverable (parameter naming) ahead of schedule.

Most recently I've started the Weeks 3-4 deliverable (docstrings), adding
the `namespace Descriptions { static constexpr std::string_view }` pattern
to all Vertex, Halfedge, and Face methods — confirmed working via `__doc__`
inspection.

### Key Achievements

- [x] Built CGAL successfully on macOS M2 (Apple Silicon)
- [x] Documented 21 methods across 2 pull requests
- [x] Discovered 7 crash scenarios through systematic testing
- [x] Found 10 silent corruption cases
- [x] Researched 3 docstring organization approaches (namespace pattern confirmed)
- [x] Identified critical bugs (line 857 lifetime management issue)
- [x] Investigated line 857 — inside `#if CGALPY_AOS2_WITH_HISTORY`, returns `Curve_halfedges&`, not exposed in standard build configs
- [x] Created comprehensive CGAL package analysis (24 packages evaluated)
- [x] Implemented proof-of-concept Named Parameters operators
- [x] Discovered property map type resolution challenge (real Week 7-8 work)
- [x] Analyzed complete Named Parameters architecture (3,500+ lines docs)
- [x] Validated manual build system with `aos2_epec_fixed` configuration
- [x] Discovered and documented Qt6/Clang compiler compatibility issue
- [x] Created complete 8-kernel CI pipeline (production-ready)
- [x] Implemented parameterized testing infrastructure (`build_config.sh`, `test_runner.py`)
- [x] Confirmed crash scenario #1 reproducibility (bus error validated)
- [x] Implemented two-layer precondition framework — all 7/7 crash tests passing
- [x] Refactored safety framework per mentor direction: 7 granular `CGALPY_NO_*`/`CGALPY_CHECK_*` flags, removed `HandleRegistry`, removed `cgalpy_error_handler.h` (CGAL throws natively)
- [x] Added `nb::arg()` to all AOS2 mutation, Vertex, Halfedge, and Face methods
- [x] Restored 5 missing overloads found during parameter naming pass
- [x] Keyword argument calls from Python now work (e.g. `arr.insert_in_face_interior(p=p, f=f)`)
- [x] Started docstrings — Vertex, Halfedge, Face methods done using `namespace Descriptions { static constexpr std::string_view }` pattern

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

**What I did:**

- [x] Built CGAL 5.6 from source on macOS Apple Silicon M2
- [x] Studied 2D Arrangements: DCEL data structures, traits classes, template architecture
- [x] Analyzed 50+ bound methods in the Python bindings repository
- [x] Mastered nanobind: return value policies, `keep_alive` patterns, lifetime management
- [x] Discovered line 857-858 bug: `reference_internal` doesn't work for `insert_cv_with_history()`

**Files Created:**

- `phase1-foundation/environment-setup.md`
- `phase1-foundation/cgal-learning-notes.md`
- `phase1-foundation/nanobind-deep-dive.md`
- `phase1-foundation/line857-bug-analysis.md`

---

### Phase 2: Contributions & Testing (40+ hours, Dec 25-29, 2025)

Submitted pull requests and ran systematic empirical testing.

**What I did:**

- [x] Submitted PR #1: Documented 6 methods with docstrings and parameter names
- [x] Submitted PR #2: Documented 15 methods (removal, modification, query)
- [x] Empirically tested 30+ methods across 13 hours
- [x] Discovered 5 crash scenarios (segfaults that kill Python interpreter)
- [x] Documented 10 silent corruption scenarios

**Files Created:**

- `phase2-contributions/pr1-submission.md`
- `phase2-contributions/pr2-submission.md`
- `phase2-contributions/complete-methods-research.md`
- `phase2-contributions/test_removal_methods.py`
- `phase2-contributions/test_modification_methods.py`
- `phase2-contributions/test_query_methods.py`

---

### Phase 2.5: Proposal Revision (3 hours, Dec 30 – Jan 1, 2026)

Revised the proposal after Efi's detailed feedback.

- [x] Removed emotional language
- [x] Shortened "What's Missing" section
- [x] Made timeline table the primary structure
- [x] Clarified that Named Parameters ≠ parameter names (two separate tasks)

---

### Phase 3: Research (17+ hours, Jan 5-11, 2026)

Addressed mentor's technical questions and extended the crash testing.

**Docstring Organization Research:**

- Tested 3 approaches; mentor confirmed `namespace Descriptions { static constexpr std::string_view }` as the standard pattern
- 85% readability improvement, zero build system changes needed

**Extended Crash Testing:**

- Found 2 new crashes (total: 7)
- Verified 3 safe behaviors
- Documented 4 geometric validation warnings

**Build System:**

- Built Polygon Mesh Processing (PMP) bindings successfully
- Resolved Eigen 3.4.1 / CGAL 5.6 compatibility issues
- Fixed GMP/GMPXX linking on macOS M2

**Files Created:**

- `research/docstring-location/docstring-location-research.md`
- `research/crash-scenarios/additional-crash-scenarios.md`
- 9 crash scenario test files
- `docs/technical/build_pmp_guide.md`

---

### Phase 3.5: Named Parameters Deep Dive (9+ hours, Jan 17, 2026)

Deep research into CGAL's Named Parameters system.

**Architecture Analysis:**

- Studied Efi's operator-based Named Parameters system
- Analyzed 5 core files in the codebase
- Created 3,500-line technical analysis document

**Proof-of-Concept:**

- 3 reference operators in prep repo
- 2 operators in actual cgal-python-bindings repo
- Branch: `feature/named-params-operators-poc`

**Key Discovery:**

The operators themselves are straightforward. The hard part is the Python-to-C++ property map type bridge — that's where the 2 weeks go.

**Files Created:**

- `NAMED_PARAMS_COMPLETE_ANALYSIS.md` (3,500 lines)
- `implementation-plan.md`
- `questions-for-efi.md`
- `PROPERTY_MAP_CHALLENGE.md`

---

### Phase 4: CI & Build System Testing (3+ hours, Feb 5, 2026)

- Validated `aos2_epec_fixed` — correct output (3 faces, 12 halfedges, 5 vertices)
- Found Apple Clang required on macOS (GCC fails with Qt6 pragma errors)
- Sent Email 7 to Efi; received CI architecture direction in Email 8

---

### Phase 4.5: Multi-Kernel CI Pipeline (7-8 hours, Feb 8, 2026)

Built a complete 8-kernel parallel CI pipeline from Efi's specifications.

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

- `build_config.sh` — build any kernel config automatically
- `test_runner.py` — parameterized test runner
- `bitbucket-pipelines.yml` — production-ready parallel CI

Weeks 11-12 CI work done ahead of GSoC.

---

### Phase 5: Precondition Framework (4 hours, Feb 19, 2026)

Built a two-layer C++ safety framework. All 7 crash scenarios converted from interpreter-killing segfaults to catchable Python `RuntimeError`.

| # | Scenario | Result |
|---|----------|--------|
| 1 | remove_isolated_vertex on non-isolated vertex | RuntimeError |
| 2 | remove_edge called twice | RuntimeError |
| 3 | he.curve() after removal | RuntimeError |
| 4 | Twin halfedge after remove_edge | RuntimeError |
| 5 | remove_isolated_vertex twice | RuntimeError |
| 6 | merge_edge on non-adjacent edges | RuntimeError |
| 7 | Regression: address reuse, no false positives | PASS |

---

### Phase 5 Revised: Framework Refactored per Mentor (5 hours, Feb 23-27, 2026)

Efi's direction required a full architectural refactor.

**Key Points:**

- CGAL already throws natively — custom error handler was redundant
- Handle invalidation belongs in CGAL C++ via `CGAL_precondition()`, not in Python bindings
- One binding flag per CGAL flag (7 total)

**Changes to cgal-python-bindings (commit: `ebea4e79`):**

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
Parallel CGAL C++ branch for upstream `CGAL_precondition()` patches pending Efi's answer on fork setup.

---

### Weeks 1-2 Pre-GSoC: Parameter Naming (5 hours, March 4-11, 2026) ✅ COMPLETE

Added `nb::arg()` parameter names across all `AOS2` binding files. This is the Weeks 1-2 GSoC deliverable, completed before the program starts.

**What I did:**

- [x] Added `nb::arg()` to all `Arrangement_on_surface_2` mutation methods (March 4)
- [x] Added `nb::arg()` to all Vertex, Halfedge, and Face binding methods (March 11)
- [x] Restored 5 missing overloads found during this pass
- [x] Build clean; sanity test passing (3 vertices, 2 edges, 1 face)

**Result:**

Keyword argument calls from Python now work:

```python
arr.insert_in_face_interior(p=p, f=f)
arr.remove_isolated_vertex(v=v)
```

**Files Created:**

- `week1-2-parameter-naming/progress-notes.md`
- `week1-2-parameter-naming/sanity_test.py`

---

### Weeks 3-4 Pre-GSoC: Docstrings Begun (2 hours, March 11, 2026) 🔄 IN PROGRESS

Started the Weeks 3-4 GSoC deliverable ahead of schedule.

**What I did:**

- [x] Added docstrings to all Vertex, Halfedge, and Face binding methods using `namespace Descriptions { static constexpr std::string_view }` pattern per mentor direction
- [x] Verified via `__doc__` inspection — all docstrings visible in nanobind output
- [ ] `arrangement_on_surface_2_bindings.cpp` docstrings pending (next session)

**Pattern used:**

```cpp
namespace Descriptions {
  static constexpr std::string_view vertex_point =
    "Returns the point associated with this vertex.";
}

cls.def("point", &Vertex::point, Descriptions::vertex_point);
```

**Files Created:**

- `week3-4-docstrings/progress-notes.md`

---

## Technical Discoveries

### 1. Namespace Docstring Pattern (Confirmed)

```cpp
namespace Descriptions {
  static constexpr std::string_view INSERT_FROM_LEFT_VERTEX =
    "Inserts a curve from a given vertex on the left endpoint.\n"
    "The vertex must lie on the left endpoint of the curve.";
}

m.def("insert_from_left_vertex", &aos2_insert_from_left_vertex_cv,
      nb::arg("curve"), nb::arg("vertex"),
      Descriptions::INSERT_FROM_LEFT_VERTEX);
```

Zero build system changes. Confirmed by mentor as the standard pattern.

### 2. CGAL Check System Architecture

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

### 3. Crash Scenarios (7 Found)

| # | Method | Category | Status |
|---|--------|----------|--------|
| 1 | remove_isolated_vertex on non-isolated | CGAL precondition | Pending CGAL patch |
| 2 | remove_edge twice | Handle invalidation | Pending CGAL patch |
| 3 | he.curve() after remove_edge | CGAL precondition | Pending CGAL patch |
| 4 | Twin halfedge after remove_edge | Handle invalidation | Pending CGAL patch |
| 5 | remove_isolated_vertex twice | Handle invalidation | Pending CGAL patch |
| 6 | merge_edge on non-adjacent edges | CGAL precondition | Pending CGAL patch |
| 7 | Address reuse regression | Handle invalidation | Pending CGAL patch |

### 4. Line 857 — reference_internal vs reference

Inside `#if defined(CGALPY_AOS2_WITH_HISTORY)` block only.
Returns `Curve_halfedges&` (not a halfedge + list).

`rv_policy::reference_internal` fails in free function context (`m.def`)
because `keep_alive<1,0>` has no `self` to act as nurse.

Needs `WITH_HISTORY` build config to confirm — asked Efi.

### 5. Qt6/Compiler Compatibility

GCC 14/15 fails with Qt6 pragma errors on macOS.
Fix: force Apple Clang (`/usr/bin/clang++`).
Documented in `build_config.sh` and CI pipeline.

---

## Repository Structure

```text
cgal-gsoc-2026-prep/
├── README.md
├── CURRENT_STATUS.md
├── paste.txt
│
├── proposal/
│   ├── gsoc-2026-proposal-v1.md
│   ├── gsoc-2026-proposal-v2.docx
│   └── gsoc-2026-proposal-v3.docx
│
├── phase1-foundation/
├── phase2-contributions/
│   ├── step2.3-first-pr/
│   ├── step2.4-pr2-research/
│   ├── step2.5-pr2-methods/
│   └── step2.6-precondition-framework/
│
├── phase3-research/
│   ├── docstring-approach-b/
│   ├── proof-of-concept-operators/
│   ├── research/
│   ├── test-named-params-implementation/
│   └── task3-named-params-study.md
│
├── phase4-ci-infrastructure/
│   ├── implementation/
│   │   ├── build_config.sh
│   │   ├── test_runner.py
│   │   └── bitbucket-pipelines.yml
│   └── PHASE_4_5_IMPLEMENTATION.md
│
├── week1-2-parameter-naming/       <- NEW
│   ├── progress-notes.md
│   └── sanity_test.py
│
├── week3-4-docstrings/             <- NEW
│   └── progress-notes.md
│
└── efi-feedback/
    ├── email01 through email12
    └── email13-table-feedback-mar13.md
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

### Time Investment

| Phase | Activity | Hours | Dates |
|-------|----------|-------|-------|
| Phase 1 | Environment + CGAL study | 50h | Dec 20-24 |
| Phase 2 | PRs + systematic testing | 40h | Dec 25-29 |
| Phase 2.5 | Proposal revision | 3h | Dec 30–Jan 1 |
| Phase 3 | Research + crash testing | 17h | Jan 5-11 |
| Phase 3.5 | Named Parameters deep dive | 9h | Jan 17 |
| Phase 4 | Build system testing | 3h | Feb 5 |
| Phase 4.5 | Multi-kernel CI implementation | 7-8h | Feb 8 |
| Phase 5 | Precondition framework | 4h | Feb 19 |
| Phase 5 Revised | Framework refactor per Efi | 5h | Feb 23-27 |
| Weeks 1-2 pre-GSoC | Parameter naming (complete) | 5h | Mar 4-11 |
| Weeks 3-4 pre-GSoC | Docstrings (in progress) | 2h | Mar 11 |
| **Total** | | **~139h** | **Dec 20–Mar 11** |

### Contribution Metrics

| Metric | Count |
|--------|-------|
| Total hours invested | 139+ |
| Total documentation lines | 25,000+ |
| Methods documented | 21 (PRs) + Vertex/Halfedge/Face (pre-GSoC) |
| Crash scenarios found | 7 |
| Safe methods verified | 18 |
| Pull requests submitted | 2 |
| Proof-of-concepts created | 4 |
| Production code commits | 3 |
| CI kernel configs | 8 |
| Emails to mentor | 13 |
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
| Flag defaults | Final default values for `CGALPY_NO_*` flags? |

### GSoC Timeline Status

| Weeks | Task | Status |
|-------|------|--------|
| 1-2 | Parameter Names | ✅ Complete (pre-GSoC) |
| 3-4 | Docstrings | 🔄 In Progress (pre-GSoC) |
| 5-6 | Safety & Preconditions | Pending CGAL branch |
| 7-8 | Named Parameters | Architecture studied |
| 9-10 | New Package Expansion | Ready |
| 11-12 | CI & Testing | ✅ Complete (pre-GSoC) |

---

## References

- CGAL Python Bindings: [bitbucket.org/taucgl/cgal-python-bindings](https://bitbucket.org/taucgl/cgal-python-bindings)
- CGAL Checks Docs: [doc.cgal.org/latest/Manual/devman_checks.html](https://doc.cgal.org/latest/Manual/devman_checks.html)
- CGAL Documentation: [doc.cgal.org](https://doc.cgal.org)
- Nanobind Docs: [nanobind.readthedocs.io](https://nanobind.readthedocs.io)
- GitHub: [@UtkarsHMer05](https://github.com/UtkarsHMer05)
- Email: utkarshkhajuria55@gmail.com

---

## License

This repository documents preparation work for Google Summer of Code 2026.
The CGAL library is licensed under GPL/LGPL. Binding code follows the same
licensing as the official CGAL Python bindings repository.

---

## Acknowledgments

Thanks to Efi Fogel for detailed mentorship through 13 email exchanges.
The depth of feedback at every stage made the preparation genuinely useful,
not just checkbox work. Thanks to the CGAL community and nanobind developers.

---

**Last Updated:** March 13, 2026  
**Repository:** [github.com/UtkarsHMer05/cgal-gsoc-2026-prep](https://github.com/UtkarsHMer05/cgal-gsoc-2026-prep)  
**Status:** Weeks 1-2 complete, Weeks 3-4 in progress — proposal approved, submitting March 16