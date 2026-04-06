# April 1, 2026 — External Docstring Headers Generated

> Session: ~3 AM IST | Duration: ~3 hours

## What was done

Created `src/libs/cgalpy/lib/docstrings/` (did not exist before) and generated
five C++ header files — one per binding package.

## Why external headers (Approach B from Phase 3)

- Binding `.cpp` code stays clean — no string literals interrupting logic
- Docstrings are version-controlled separately from binding mechanics  
- Automation script can regenerate headers without touching `.cpp` files
- Directly implements Email 3 direction (Jan 7): "moving the docstring to a
  variable is a good idea"

## Files created

| File | Size | Constants |
|---|---|---|
| `polygon_2_docstrings.h` | 3.6K | 22 (10 more added Apr 7) |
| `alpha_shape_2_docstrings.h` | 1.5K | 10 |
| `boolean_set_operations_2_docstrings.h` | 1.3K | 7 |
| `envelope_2_docstrings.h` | 2.0K | 9 |
| `visibility_2_docstrings.h` | 1.1K | 5 |

## Header structure (identical pattern in all 5 files)

```cpp
#pragma once

const char* METHOD_NAME_DOC = R"pbdoc(
Description from CGAL documentation.
)pbdoc";
```

## Naming convention

Python binding name → UPPERCASE + `_DOC` suffix:
- `is_valid` → `IS_VALID_DOC`
- `__init__` → `__INIT___DOC`
- `reverse_orientation` → `REVERSE_ORIENTATION_DOC`

## Include pattern (to add to each .cpp)

```cpp
#include "docstrings/polygon_2_docstrings.h"
#include "docstrings/alpha_shape_2_docstrings.h"
#include "docstrings/boolean_set_operations_2_docstrings.h"
#include "docstrings/envelope_2_docstrings.h"
#include "docstrings/visibility_2_docstrings.h"
```

## .def() wiring pattern

```cpp
// BEFORE:
.def("is_simple", &Pgn::is_simple)

// AFTER:
.def("is_simple", &Pgn::is_simple, IS_SIMPLE_DOC)
```

## What was NOT done

- Headers NOT yet `#include`'d in any `.cpp` file
- `.def()` calls NOT yet updated with DOC constants
- Build NOT run since header generation
- AOS2 header NOT created (AOS2 keeps inline strings for now)
- NOT committed (latest: `ebea4e79` Feb 27)
