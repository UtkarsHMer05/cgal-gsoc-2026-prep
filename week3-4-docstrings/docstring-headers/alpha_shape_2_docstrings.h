#pragma once

/*
 * alpha_shape_2_docstrings.h
 * Docstring constants for alpha_shape_2_bindings.cpp
 * Part of: src/libs/cgalpy/lib/docstrings/
 */

const char* ALPHA_DOC = R"pbdoc(
Returns the current alpha value used to filter the alpha shape.
)pbdoc";

const char* SET_ALPHA_DOC = R"pbdoc(
Sets the alpha value used to filter the alpha shape.

Changing the alpha value updates which simplices (vertices, edges, faces)
are classified as INTERIOR, REGULAR, SINGULAR, or EXTERIOR.
)pbdoc";

const char* ALPHA_COUNT_DOC = R"pbdoc(
Returns the number of different alpha values in the sorted alpha spectrum.

The spectrum contains one value per triangle circumradius in the triangulation.
)pbdoc";

const char* GET_NTH_ALPHA_DOC = R"pbdoc(
Returns the nth alpha value from the sorted alpha value spectrum.
)pbdoc";

const char* FIND_OPTIMAL_ALPHA_DOC = R"pbdoc(
Returns the smallest alpha value for which all input points are part of
the same connected component of the alpha shape.
)pbdoc";

const char* CLASSIFY_DOC = R"pbdoc(
Classifies a simplex (vertex, edge, or face) with respect to the alpha shape.

Returns one of EXTERIOR, SINGULAR, REGULAR, or INTERIOR depending on
whether the simplex lies outside, on the boundary (singular), on the
boundary (regular), or inside the alpha shape.
)pbdoc";

const char* NUMBER_OF_SOLID_COMPONENTS_DOC = R"pbdoc(
Returns the number of solid connected components of the alpha shape.

A solid component is a connected set of INTERIOR and REGULAR faces.
)pbdoc";

const char* ALPHA_SHAPE_VERTICES_DOC = R"pbdoc(
Returns an iterator range over the vertices of the alpha shape boundary.

Only vertices classified as REGULAR or SINGULAR are included.
)pbdoc";

const char* ALPHA_SHAPE_EDGES_DOC = R"pbdoc(
Returns an iterator range over the edges of the alpha shape boundary.

Only edges classified as REGULAR or SINGULAR are included.
)pbdoc";

const char* MAKE_ALPHA_SHAPE_DOC = R"pbdoc(
Constructs an alpha shape from a range of input points.

Returns the optimal alpha value used to build the shape.
)pbdoc";
