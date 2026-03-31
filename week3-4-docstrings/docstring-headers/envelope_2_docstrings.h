#pragma once

/*
 * envelope_2_docstrings.h
 * Docstring constants for envelope_2_bindings.cpp
 * Part of: src/libs/cgalpy/lib/docstrings/
 */

const char* LOWER_ENVELOPE_X_MONOTONE_DOC = R"pbdoc(
Constructs the lower envelope of a set of x-monotone curves.

The lower envelope is the lower boundary of the arrangement of curves.
The output is stored in a minimization diagram (a 1D arrangement).
)pbdoc";

const char* UPPER_ENVELOPE_X_MONOTONE_DOC = R"pbdoc(
Constructs the upper envelope of a set of x-monotone curves.

The upper envelope is the upper boundary of the arrangement of curves.
The output is stored in a maximization diagram (a 1D arrangement).
)pbdoc";

const char* LOWER_ENVELOPE_DOC = R"pbdoc(
Constructs the lower envelope of a set of curves.

Curves are decomposed into x-monotone sub-curves internally.
The output is stored in a minimization diagram.
)pbdoc";

const char* UPPER_ENVELOPE_DOC = R"pbdoc(
Constructs the upper envelope of a set of curves.

Curves are decomposed into x-monotone sub-curves internally.
The output is stored in a maximization diagram.
)pbdoc";

const char* MINIMIZATION_DIAGRAM_DOC = R"pbdoc(
Represents the lower envelope (minimization diagram) of a set of curves.

The minimization diagram is a 1D arrangement where each edge is associated
with the curves achieving the minimum y-value in that x-range.
)pbdoc";

const char* MAXIMIZATION_DIAGRAM_DOC = R"pbdoc(
Represents the upper envelope (maximization diagram) of a set of curves.

The maximization diagram is a 1D arrangement where each edge is associated
with the curves achieving the maximum y-value in that x-range.
)pbdoc";

const char* DIAGRAM_VERTEX_DOC = R"pbdoc(
Returns a handle to a vertex in the envelope diagram.

Diagram vertices correspond to x-coordinates where the envelope changes
its defining curve(s).
)pbdoc";

const char* DIAGRAM_EDGE_DOC = R"pbdoc(
Returns a handle to an edge in the envelope diagram.

Each edge is associated with one or more curves that define the envelope
over that x-interval.
)pbdoc";

const char* DIAGRAM_FACE_DOC = R"pbdoc(
Returns the single unbounded face of the envelope diagram.

The minimization or maximization diagram has exactly one face.
)pbdoc";
