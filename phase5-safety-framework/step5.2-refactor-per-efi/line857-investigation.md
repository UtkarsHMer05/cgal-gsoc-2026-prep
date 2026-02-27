# Line 857 Investigation (Feb 27, 2026)

## Original Claim (Email sent to Efi)
Returns halfedge + EdgeList. reference_internal fails because list/tuple
can't be nurse in keep_alive. Fix: nb::keep_alive<0,1>().

## Efi's Response
"No, I don't think this is the problem. If keep_alive is necessary there,
it is necessary in many many other places."

## Actual Finding (from source investigation)

Location: arrangement_on_surface_2_bindings.cpp, inside:
  #if defined(CGALPY_AOS2_WITH_HISTORY)
  void export_aos_with_history(py::module_& m)

The todo:
  //! \todo Why the f... reference_internal doesn't work?
  m.def("insert", &aos2::insert_cv_with_history, ref)

The wrapper returns: Arrangement_on_surface_with_history_2::Curve_halfedges&
NOT a halfedge + list.

## Hypothesis
reference_internal uses return value as nurse in implicit keep_alive<0,1>.
Curve_halfedges returned by reference may not be tracked as a
nanobind-managed object, so keep_alive silently does nothing.
reference "works" by making no lifetime contract at all.

## Why Cannot Confirm
CGALPY_AOS2_WITH_HISTORY is not set in aos2_epec_fixed.cmake.
Also requires CGALPY_AOS2_CONSOLIDATED_CURVE_DATA.
Arrangement_on_surface_with_history_2 is not present in standard builds.

## Next Step
Asked Efi which build config enables WITH_HISTORY.
