#pragma once

// alpha_shape_2_docstrings.h
// ==========================
// Docstring constants for CGALPY.As2 Alpha_shape_2 bindings.
// Source: https://doc.cgal.org/latest/Alpha_shapes_2/
// #include "docstrings/alpha_shape_2_docstrings.h"

const char *ALPHA_DOC = R"pbdoc(
Returns the current alpha value used to filter the alpha shape.

The alpha value determines which simplices are classified as
INTERIOR, REGULAR, SINGULAR, or EXTERIOR.
)pbdoc";

const char *SET_ALPHA_DOC = R"pbdoc(
Sets the alpha value used to filter the alpha shape.

Parameters
----------
alpha : float
    The new alpha value. Must be non-negative.
)pbdoc";

const char *ALPHA_COUNT_DOC = R"pbdoc(
Returns the number of alpha values in the sorted alpha spectrum.

The spectrum contains all critical alpha values at which the
topology of the alpha shape changes.
)pbdoc";

const char *GET_NTH_ALPHA_DOC = R"pbdoc(
Returns the nth alpha value from the sorted alpha spectrum.

Parameters
----------
n : int
    Zero-based index into the sorted sequence of critical values.
)pbdoc";

const char *FIND_OPTIMAL_ALPHA_DOC = R"pbdoc(
Returns the smallest alpha for which all points are in the same
connected component of the alpha complex.

Parameters
----------
nb_components : int
    The desired number of connected components (default 1).
)pbdoc";

const char *CLASSIFY_DOC = R"pbdoc(
Classifies a simplex under the current alpha value.

Returns one of: EXTERIOR, SINGULAR, REGULAR, or INTERIOR.

Parameters
----------
simplex : Vertex_handle | Edge | Face_handle
    The simplex to classify.
)pbdoc";

const char *NUMBER_OF_SOLID_COMPONENTS_DOC = R"pbdoc(
Returns the number of solid connected components of the alpha shape.

A solid component consists of interior faces connected by regular edges.
)pbdoc";

const char *ALPHA_SHAPE_VERTICES_DOC = R"pbdoc(
Returns an iterator range over the vertices of the alpha shape.

Only REGULAR and SINGULAR vertices are included.
)pbdoc";

const char *ALPHA_SHAPE_EDGES_DOC = R"pbdoc(
Returns an iterator range over the edges of the alpha shape.

Only REGULAR and SINGULAR edges are included.
)pbdoc";

const char *MAKE_ALPHA_SHAPE_DOC = R"pbdoc(
Constructs the alpha shape from a range of input points.

Parameters
----------
points : iterable of Point_2
    The input point set. Duplicate points are ignored.
alpha : float, optional
    Initial alpha value (default 0).
)pbdoc";