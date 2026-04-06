#pragma once

// visibility_2_docstrings.h
// =========================
// Docstring constants for CGALPY.Vis2 bindings.
// Source: https://doc.cgal.org/latest/Visibility_2/
// #include "docstrings/visibility_2_docstrings.h"

const char *COMPUTE_VISIBILITY_DOC = R"pbdoc(
Computes the visibility region from a query point inside a face.

Returns an arrangement whose single bounded face represents the
region visible from the query point.
)pbdoc";

const char *COMPUTE_VISIBILITY_HALFEDGE_DOC = R"pbdoc(
Computes the visibility region from a point on a halfedge boundary.

Used for boundary queries (point lies on an edge, not in a face interior).
Returns an arrangement representing the visible region.
)pbdoc";

const char *IS_ATTACHED_DOC = R"pbdoc(
Returns true if the visibility object is attached to an arrangement.

When attached, compute_visibility() can be called.
)pbdoc";

const char *ATTACH_DOC = R"pbdoc(
Attaches the visibility object to the given arrangement.

Must be called before compute_visibility(). The arrangement must remain
valid for the lifetime of this attachment.
)pbdoc";

const char *DETACH_DOC = R"pbdoc(
Detaches the visibility object from its current arrangement.

After detaching, is_attached() returns false.
)pbdoc";