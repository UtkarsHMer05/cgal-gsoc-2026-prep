# Current Status — Feb 27, 2026

## Phase 5 Revised (Feb 27, 2026) — Per Efi's Feedback

### Changes made to cgal-python-bindings (branch: feature/named-params-operators-poc)

1. CMakeLists.txt — replaced CGALPY_ENABLE_PRECONDITIONS with 7 granular flags:
   CGALPY_NO_PRECONDITIONS, CGALPY_NO_POSTCONDITIONS, CGALPY_NO_ASSERTIONS,
   CGALPY_NO_WARNINGS, CGALPY_NDEBUG, CGALPY_CHECK_EXPENSIVE, CGALPY_CHECK_EXACTNESS
   Each maps 1:1 to the corresponding CGAL_* compile definition.
   Defaults TBD with Efi.

2. Removed cgalpy_error_handler.h — CGAL 6.x already throws exceptions
   natively. The -DNDEBUG stripping approach was wrong; controlling which
   macros survive compilation is the correct fix.

3. Removed HandleRegistry (handle_registry.h + all bindings references) —
   Python-side tracking was wrong architecture. Fix belongs in CGAL C++
   via CGAL_precondition() in removal methods.

### Awaiting Efi
- Fork/branch location for CGAL-level precondition patches
- WITH_HISTORY build config for line 857 investigation
- Default values for CGALPY_NO_* flags

### Line 857 Investigation Results
- insert_cv_with_history is inside #if CGALPY_AOS2_WITH_HISTORY
- Also requires CGALPY_AOS2_CONSOLIDATED_CURVE_DATA
- Returns Curve_halfedges& (not halfedge + EdgeList as originally thought)
- Hypothesis: reference_internal fails because Curve_halfedges returned
  by ref is not a nanobind-managed object, so keep_alive nurse tracking
  silently fails. reference "works" by making no lifetime contract at all.
- Cannot confirm without WITH_HISTORY build config — asked Efi.

### Emails Sent
- Email 11: Confirmed checks understanding + 7-flag mapping (Feb 23)
- Email 12: Line 857 investigation results + 2 questions (Feb 27)
