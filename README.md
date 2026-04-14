# CGAL GSoC 2026 — Python Bindings Enhancement (Preparation Repository)

> **Student:** Utkarsh Khajuria · VIT Chennai · `utkarshkhajuria55@gmail.com`
> **Mentor:** Efi Fogel · `efifogel@gmail.com`
> **Program:** Google Summer of Code 2026 · CGAL · 350 h / 12 weeks
> **Official repo:** https://bitbucket.org/taucgl/cgal-python-bindings
> **Branch:** `feature/named-params-operators-poc`
> **Latest upstream commit:** `ebea4e79` (Feb 27, 2026)

---

## What this repo is

This repository documents every hour of pre‑GSoC preparation work done
between December 20, 2025 and the start of GSoC coding (May 2026).
It is **not** the binding code itself — that lives on Bitbucket.
Everything here is research notes, scripts, progress logs, and reference
material that drove the actual code changes.

**160+ hours | 24 emails with mentor | 7 crashes found | 8‑kernel CI pipeline**

---

## Repository structure

```text
cgal-gsoc-2026-prep/
├── phase1-foundation/          Dec 20–24 2025  Environment, DCEL study, nanobind mastery
├── phase2-contributions/       Dec 25–29 2025  PRs, crash discovery (7 crashes, 10 corruptions)
├── phase3-research/            Jan 5–11 2026   Docstring approaches A/B/C, PMP build, Named Params
├── phase4-ci-infrastructure/   Feb 5–8  2026   Manual build fix, 8‑kernel CI pipeline
├── phase5-safety-framework/    Feb 19–27 2026  Framework built → refactored per Efi's direction
├── weeks1-2-parameter-naming/  Mar 4–11 2026   nb::arg() on all AOS2 methods
├── week3-4-docstrings/         Mar 13 – Apr 7  Inline docs, automation POC, header generation
└── phase6-docstring-headers/   Apr 7–15 2026   5‑package header wiring + automation coverage
```

Key subfolders and files:

- `week3-4-docstrings/`
  - `docstring-headers/` — initial copies of the 5 `.h` files
  - `docstring_extractor.py`, `docstring_extractor_v2.py` — AOS2 extractor scripts
  - `verification_test.py` — runtime `__doc__` spot‑check script
  - `march13-vertex-halfedge-face-complete.md` — vertex/halfedge/face inline docs
  - `march24-aos2-bindings-complete.md` — AOS2 main bindings inline docs
  - `march25-automation-research.md` — AOS2 automation POC (50/50) + email thread
  - `april1-docstring-headers-generated.md` — 5 external header files created
  - `april7-polygon2-wiring.md` — 10 missing Polygon_2 constants identified + text
  - `progress-notes.md` — cumulative progress log (all sessions)

- `phase6-docstring-headers/`
  - `README.md` — human‑level overview of the header‑based docstring phase
  - `01-design-overview.md` — why headers, how they integrate
  - `02-polygon_2-implementation.md` — full story of Polygon_2 docs + 10 missing constants
  - `03-alpha-shape-bso-env-vis-implementation.md` — As2/Bso2/Env2/Vis2 wiring
  - `04-automation-and-coverage.md` — 73/73 coverage across 5 packages
  - `05-open-questions-and-next-steps.md` — what's blocked on Efi and the plan while waiting

---

## Key technical achievements (pre‑GSoC)

| Deliverable | Status | When |
| --- | --- | --- |
| Dev environment (macOS M2, CGAL, nanobind) | ✅ Complete | Dec 20 |
| DCEL mastery + 15 insertion methods tested | ✅ Complete | Dec 21 |
| Line 857 bug discovered (`rv_policy` on free fn) | ✅ Complete | Dec 23 |
| 7 crash scenarios documented with repro | ✅ Complete | Dec 28 – Jan 6 |
| Proposal v3 (Efi's 9‑section spec) | ✅ Complete | Jan 11 |
| Named Parameters property map bridge problem | ✅ Complete | Jan 17 |
| 8‑kernel CI pipeline (GSoC Weeks 11–12) | ✅ Complete | Feb 8 |
| 7‑flag CMake safety architecture | ✅ Complete | Feb 27 |
| nb::arg() on all AOS2 methods (GSoC Weeks 1–2) | ✅ Complete | Mar 11 |
| Docstrings: vertex / halfedge / face (108 total) | ✅ Complete | Mar 13 + 24 |
| Docstring extractor — 50/50 on AOS2 | ✅ Complete | Mar 25 |
| 5 external docstring header files generated | ✅ Complete | Apr 1 |
| 10 missing Polygon_2 constants identified + text | ✅ Complete | Apr 7 |
| 5‑package header wiring + 119 `.def()` sites wired | ✅ Complete | Apr 7–15 |
| 73/73 docstring coverage for 5 packages | ✅ Complete | Apr 7–15 |

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
| --- | --- | --- |
| 1–2 | Make proposal concise, separate Task A/B | Dec 30–31 |
| 3 | CI + package analysis required | Jan 7 |
| 7–8 | Build results + CI clarifications | Feb 5 |
| 11 | 5‑point framework refactor direction | Feb 23 |
| 17–18 | Weeks 3–4 complete + Landmarks correction | Mar 24 |
| 20 | "automate docstring creation" | Mar 25 |
| 22 | 50/50 AOS2 automation POC results sent | Mar 25 |
| 23 | Docstring automation follow‑up (Q5) | Mar 25 — **no reply yet** |
| 24–25 | Docstring header + 5‑package wiring status, LaTeX/manual overrides questions | Apr 7 — **no reply yet** |

---

## Current blockers

- **Emails 23 + 24/25** — awaiting Efi's reply on:
  - how aggressive the automation should be,
  - policy for manual docstrings,
  - how to handle LaTeX/Doxygen markup,
  - whether to extend docstrings to more packages vs start Triangulation_2 / Convex_hull_2 now.
- CGAL C++ patches for the 7 crash scenarios — need fork location and workflow confirmation (Q3).
- New packages (Triangulation_2, Convex_hull_2, etc.) intentionally not implemented yet to avoid diverging from mentor's priorities.

All local binding changes are still unpushed beyond `ebea4e79` (Feb 27).

---

## Absolute DO NOTs

- Use lowercase `cgalpy` in imports — it is `CGALPY`.
- Re‑add `HandleRegistry` or `cgalpy_error_handler.h`.
- Suggest keep_alive‑based "fixes" for line 857 without Efi's explicit direction.
- Commit or open PRs to the official repo without mentor confirmation.
- Say "dynamically builds parameter chains" when describing Named Parameters.
- Put docstring headers anywhere other than `src/libs/cgalpy/lib/docstrings/`.
- Describe `Curve_halfedges` as "unregistered" — it is registered via `py::class_`.

---

## Project Context

| | |
| --- | --- |
| Project | CGAL Python Bindings Enhancement |
| Binding Library | nanobind (C++17) |
| Main Repository | https://bitbucket.org/taucgl/cgal-python-bindings |
| Working Branch | `feature/named-params-operators-poc` |
| CGAL Documentation | https://doc.cgal.org |

### Core problem

The CGAL Python bindings exist but are incomplete:

- Most methods lack documentation.
- Parameters appear as `arg0`, `arg1`, `arg2` instead of meaningful names.
- Several methods can still crash Python if misused.
- CGAL's Named Parameters pattern is not applied uniformly.
- No systematic precondition validation in C++.
- CI infrastructure was dormant until this work.

---

## Work Summary

*(You can keep your existing per‑phase sections largely as‑is; only small wording changes are needed where they reference total hours or "header generation only". The new `phase6-docstring-headers` folder already contains detailed Markdown for the header wiring + coverage work.)*

---

## GSoC Timeline Status

| Weeks | Task | Status |
| --- | --- | --- |
| 1–2 | Parameter Names | Complete (pre‑GSoC, Mar 4–11) |
| 3–4 | Docstrings (AOS2 + vertex/halfedge/face) | Complete (pre‑GSoC, Mar 13–24) |
| 3–4+ | Docstring automation POC (AOS2) | Complete (Mar 25, 50/50) |
| 3–4+ | Docstring header files (5 pkgs) | Generated (Apr 1) |
| 3–4++ | Header wiring + 5‑package coverage | Complete locally (Apr 7–15) |
| 5–6 | Safety and Preconditions | 7 CMake flags done, CGAL patch pending |
| 7–8 | Named Parameters | Architecture studied, property‑map bridge identified |
| 9–10 | New Package Expansion | Planned (Triangulation_2 / Shape recognition) |
| 11–12 | CI and Testing | Complete (pre‑GSoC, Feb 8) |

---

## References

- CGAL Python Bindings: https://bitbucket.org/taucgl/cgal-python-bindings
- CGAL Checks: https://doc.cgal.org/latest/Manual/devman_checks.html
- CGAL Documentation: https://doc.cgal.org
- Nanobind: https://nanobind.readthedocs.io
- GitHub: https://github.com/UtkarsHMer05
- Email: utkarshkhajuria55@gmail.com

---

## License

This repository documents preparation work for Google Summer of Code 2026.  
The CGAL library is licensed under GPL/LGPL. Binding code follows the same
licensing as the official CGAL Python bindings repository.

---

## Acknowledgments

Thanks to Efi Fogel for detailed mentorship through more than twenty emails.
The feedback at every stage made the preparation genuinely useful, not just
checkbox work. Thanks also to the CGAL community and the nanobind authors.

---

Last updated: April 15, 2026  
Repository: https://github.com/UtkarsHMer05/cgal-gsoc-2026-prep  
Status: Weeks 1–2 complete · Weeks 3–4 complete · Automation POC 50/50 ·  
5 header files generated · 5‑package wiring + 73/73 coverage · Awaiting Emails 23, 24, 25.