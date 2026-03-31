# Docstring Header Files — April 1, 2026

## What This Folder Is

This folder documents the **docstring header generation session** completed on April 1, 2026 (3 AM IST). It is a direct continuation of the docstring automation research from the March 25 session (50/50 AOS2 proof-of-concept).

## Context

Efi's Email 20 (March 25, 2026):
> "I don't have anything in particular, but you surely can start with how to automate a bit of the docstring creation."

Efi's Email 3 (January 7, 2026):
> "I think moving the docstring to a variable is a good idea."

Instead of continuing to write docstrings inline inside `.cpp` binding files (which "shadows the code itself" per Efi), this session generates **separate C++ header files** — one per package — containing all docstring constants.

---

## What Was Done

Created a new directory in the official repo:

```
src/libs/cgalpy/lib/docstrings/
```

Generated 5 header files:

| File | Size | Package |
|---|---|---|
| `polygon_2_docstrings.h` | 3.6K | Polygon_2 |
| `alpha_shape_2_docstrings.h` | 1.5K | Alpha Shapes 2D |
| `boolean_set_operations_2_docstrings.h` | 1.3K | Boolean Set Operations 2D |
| `envelope_2_docstrings.h` | 2.0K | Envelope 2D |
| `visibility_2_docstrings.h` | 1.1K | Visibility 2D |

---

## What Is NOT Done Yet

- [ ] Headers not yet `#include`'d in the binding `.cpp` files
- [ ] `.def()` calls not yet updated to reference DOC constants
- [ ] Build has not been re-run since header generation
- [ ] No new Bitbucket commit (still at `ebea4e79`, Feb 27)

---

## How the Headers Work

Each header follows a simple, consistent pattern:

```cpp
// In polygon_2_docstrings.h:
#pragma once

const char* IS_SIMPLE_DOC = R"pbdoc(
Returns true if the polygon is simple (non-self-intersecting).
)pbdoc";
```

Then in the binding file, after adding the `#include`:

```cpp
#include "docstrings/polygon_2_docstrings.h"

// Each .def() gets the constant as its last argument:
.def("is_simple", &Polygon_2::is_simple, IS_SIMPLE_DOC)
```

---

## Files In This Folder

| File | Purpose |
|---|---|
| `README.md` | This file — overview |
| `implementation.md` | Full technical breakdown: naming conventions, source of each docstring |
| `wiring-guide.md` | Step-by-step instructions to include headers in `.cpp` files |
| `polygon_2_docstrings.h` | Header file (mirrors what lives in the repo) |
| `alpha_shape_2_docstrings.h` | Header file |
| `boolean_set_operations_2_docstrings.h` | Header file |
| `envelope_2_docstrings.h` | Header file |
| `visibility_2_docstrings.h` | Header file |

---

## Relationship to Approach A vs B (Phase 3, Jan 11, 2026)

| Approach | Description | Status |
|---|---|---|
| A | External variables at top of same `.cpp` file | Validated Jan 2026 — 85% readability |
| B | Separate `.h` header files per package | **This session** — 95% readability |
| C | Doxygen auto-generation | Proof-of-concept only (March 25) |

This session implements **Approach B** for 5 packages.