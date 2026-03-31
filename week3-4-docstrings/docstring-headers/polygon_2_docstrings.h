#pragma once

/*
 * polygon_2_docstrings.h
 * Docstring constants for polygon_2_bindings.cpp
 * Part of: src/libs/cgalpy/lib/docstrings/
 */

const char* __INIT___DOC = R"pbdoc(
Constructs a polygon.

If a range of points is provided, the polygon is initialized with those
points as vertices in the given order.
)pbdoc";

const char* IS_SIMPLE_DOC = R"pbdoc(
Returns true if the polygon is simple.

A polygon is simple if its boundary does not self-intersect.
)pbdoc";

const char* IS_CONVEX_DOC = R"pbdoc(
Returns true if the polygon is convex.
)pbdoc";

const char* ORIENTATION_DOC = R"pbdoc(
Returns the orientation of the polygon.

Returns CLOCKWISE, COUNTERCLOCKWISE, or COLLINEAR.
The polygon must be simple.
)pbdoc";

const char* ORIENTED_SIDE_DOC = R"pbdoc(
Returns on which side of the polygon boundary a query point lies.

Returns ON_POSITIVE_SIDE, ON_NEGATIVE_SIDE, or ON_ORIENTED_BOUNDARY.
The polygon must be simple.
)pbdoc";

const char* BOUNDED_SIDE_DOC = R"pbdoc(
Returns whether a query point is inside, outside, or on the boundary.

Returns ON_BOUNDED_SIDE, ON_UNBOUNDED_SIDE, or ON_BOUNDARY.
The polygon must be simple.
)pbdoc";

const char* BBOX_DOC = R"pbdoc(
Returns the bounding box of the polygon.
)pbdoc";

const char* AREA_DOC = R"pbdoc(
Returns the signed area of the polygon.

The area is positive if the vertices are in counterclockwise order,
and negative if they are in clockwise order.
)pbdoc";

const char* LEFT_VERTEX_DOC = R"pbdoc(
Returns an iterator to the leftmost vertex of the polygon.
)pbdoc";

const char* RIGHT_VERTEX_DOC = R"pbdoc(
Returns an iterator to the rightmost vertex of the polygon.
)pbdoc";

const char* TOP_VERTEX_DOC = R"pbdoc(
Returns an iterator to the topmost vertex of the polygon.
)pbdoc";

const char* BOTTOM_VERTEX_DOC = R"pbdoc(
Returns an iterator to the bottommost vertex of the polygon.
)pbdoc";

const char* CONTAINER_DOC = R"pbdoc(
Returns a reference to the internal vertex container of the polygon.
)pbdoc";

const char* SIZE_DOC = R"pbdoc(
Returns the number of vertices of the polygon.
)pbdoc";

const char* IS_EMPTY_DOC = R"pbdoc(
Returns true if the polygon has no vertices.
)pbdoc";

const char* CLEAR_DOC = R"pbdoc(
Removes all vertices from the polygon.
)pbdoc";

const char* PUSH_BACK_DOC = R"pbdoc(
Appends a vertex to the polygon.

Inserts the point p at the end of the vertex sequence.
)pbdoc";

const char* VERTEX_DOC = R"pbdoc(
Returns a const reference to the vertex at position i.
)pbdoc";

const char* REVERSE_ORIENTATION_DOC = R"pbdoc(
Reverses the orientation of the polygon by reversing the order of its vertices.
)pbdoc";

const char* EDGES_DOC = R"pbdoc(
Returns an iterator range over the edges of the polygon.
)pbdoc";

const char* VERTICES_DOC = R"pbdoc(
Returns an iterator range over the vertices of the polygon.
)pbdoc";

const char* DRAW_DOC = R"pbdoc(
Opens a CGAL viewer window and draws the polygon.
)pbdoc";
