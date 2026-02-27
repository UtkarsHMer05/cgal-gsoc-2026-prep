# Phase 5.2: Framework Refactored per Mentor Direction (Feb 27, 2026)

## Efi's Feedback (Email, Feb 23, 2026)
1. Stay close to CGAL, create Pythonizing API
2. CGAL already has a check system — read devman_checks.html
3. One binding flag per CGAL flag
4. Handle invalidation fix belongs in CGAL C++, not Python bindings
5. Open a parallel CGAL branch for upstream fixes

## Key Technical Finding
CGAL checks throw exceptions by default. -DNDEBUG sets CGAL_NDEBUG which
compiles out all check macros. Fix = control which macros survive compilation.
Not: redirect abort().

## Changes Made (commit: ebea4e79)

### CMakeLists.txt
Replaced CGALPY_ENABLE_PRECONDITIONS with 7 granular flags:

| Binding Flag             | CGAL Definition          | Default |
|--------------------------|--------------------------|---------|
| CGALPY_NO_PRECONDITIONS  | CGAL_NO_PRECONDITIONS    | OFF     |
| CGALPY_NO_POSTCONDITIONS | CGAL_NO_POSTCONDITIONS   | OFF     |
| CGALPY_NO_ASSERTIONS     | CGAL_NO_ASSERTIONS       | OFF     |
| CGALPY_NO_WARNINGS       | CGAL_NO_WARNINGS         | OFF     |
| CGALPY_NDEBUG            | CGAL_NDEBUG              | OFF     |
| CGALPY_CHECK_EXPENSIVE   | CGAL_CHECK_EXPENSIVE     | OFF     |
| CGALPY_CHECK_EXACTNESS   | CGAL_CHECK_EXACTNESS     | OFF     |

### Deleted Files
- src/libs/cgalpy/include/cgalpy_error_handler.h (CGAL throws natively)
- src/libs/cgalpy/include/handle_registry.h (fix belongs in CGAL C++)

### Removed from arrangement_on_surface_2_bindings.cpp
- #include "handle_registry.h"
- All check_alive(), mark_dead(), mark_alive() calls (25 lines)

## Build Verification
Clean build. Basic sanity test passed:
  Vertices: 3, Edges: 2, Faces: 1 — correct geometry.

## Awaiting Efi
- CGAL fork/branch location for upstream precondition patches
- Build config enabling CGALPY_AOS2_WITH_HISTORY (for line 857 repro)
- Final default values for CGALPY_NO_* flags
