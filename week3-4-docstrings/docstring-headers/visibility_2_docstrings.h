#pragma once

/*
 * visibility_2_docstrings.h
 * Docstring constants for visibility_2_bindings.cpp
 * Part of: src/libs/cgalpy/lib/docstrings/
 */

const char* COMPUTE_VISIBILITY_DOC = R"pbdoc(
Computes the visibility region from a query point in the interior of a face.

The query point must lie strictly inside the given face.
The result is stored in the output arrangement passed as the last argument.
)pbdoc";

const char* COMPUTE_VISIBILITY_HALFEDGE_DOC = R"pbdoc(
Computes the visibility region from a query point on a halfedge boundary.

The query point must lie on the given halfedge. This variant is used for
boundary visibility queries where the viewpoint is on the polygon boundary.
The result is stored in the output arrangement.
)pbdoc";

const char* IS_ATTACHED_DOC = R"pbdoc(
Returns true if the visibility object is attached to an arrangement.
)pbdoc";

const char* ATTACH_DOC = R"pbdoc(
Attaches the visibility object to a given arrangement.

Must be called before any visibility query. The arrangement must remain
valid for the lifetime of the visibility object.
)pbdoc";

const char* DETACH_DOC = R"pbdoc(
Detaches the visibility object from its current arrangement.
)pbdoc";
