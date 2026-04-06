#pragma once

// envelope_2_docstrings.h
// =======================
// Docstring constants for CGALPY.Env2 bindings.
// Source: https://doc.cgal.org/latest/Envelope_2/
// #include "docstrings/envelope_2_docstrings.h"

const char *LOWER_ENVELOPE_X_MONOTONE_DOC = R"pbdoc(
Constructs the lower envelope of a set of x-monotone curves.

The lower envelope is the pointwise minimum over the x-axis.
Returns an Envelope_diagram_1 (minimization diagram).
)pbdoc";

const char *UPPER_ENVELOPE_X_MONOTONE_DOC = R"pbdoc(
Constructs the upper envelope of a set of x-monotone curves.

The upper envelope is the pointwise maximum over the x-axis.
Returns an Envelope_diagram_1 (maximization diagram).
)pbdoc";

const char *LOWER_ENVELOPE_DOC = R"pbdoc(
Constructs the lower envelope of a set of curves.

Curves are decomposed into x-monotone subcurves internally.
Returns an Envelope_diagram_1.
)pbdoc";

const char *UPPER_ENVELOPE_DOC = R"pbdoc(
Constructs the upper envelope of a set of curves.

Curves are decomposed into x-monotone subcurves internally.
Returns an Envelope_diagram_1.
)pbdoc";

const char *MINIMIZATION_DIAGRAM_DOC = R"pbdoc(
Returns the minimization diagram (lower envelope) of the input curves.
)pbdoc";

const char *MAXIMIZATION_DIAGRAM_DOC = R"pbdoc(
Returns the maximization diagram (upper envelope) of the input curves.
)pbdoc";

const char *DIAGRAM_VERTEX_DOC = R"pbdoc(
Accesses a vertex in the envelope diagram.

A diagram vertex is an x-coordinate where the active curve set changes.
)pbdoc";

const char *DIAGRAM_EDGE_DOC = R"pbdoc(
Accesses an edge in the envelope diagram.

A diagram edge is an x-interval where one or more curves form the envelope.
)pbdoc";

const char *DIAGRAM_FACE_DOC = R"pbdoc(
Accesses a face in the 1D envelope diagram.

Faces are the open intervals between consecutive diagram vertices.
)pbdoc";