#pragma once

// polygon_2_docstrings.h
// ======================
// Docstring constants for CGALPY.Pol2.Polygon_2 Python bindings.
// Source: https://doc.cgal.org/latest/Polygon/classCGAL_1_1Polygon__2.html
// #include "docstrings/polygon_2_docstrings.h"

const char *__INIT___DOC = R"pbdoc(
Constructs a polygon from a range of points.

Parameters
----------
points : iterable of Point_2
    The vertices in order. The polygon is not automatically closed.
)pbdoc";

const char *IS_SIMPLE_DOC = R"pbdoc(
Returns true if the polygon is simple.

A polygon is simple if its boundary does not self-intersect.
)pbdoc";

const char *IS_CONVEX_DOC = R"pbdoc(
Returns true if the polygon is convex.

A polygon is convex if all interior angles are at most 180 degrees.
The polygon must be simple.
)pbdoc";

const char *ORIENTATION_DOC = R"pbdoc(
Returns the orientation of the polygon.

Returns CGAL::COUNTERCLOCKWISE, CGAL::CLOCKWISE, or CGAL::COLLINEAR.
)pbdoc";

const char *ORIENTED_SIDE_DOC = R"pbdoc(
Returns the oriented side of the polygon on which a point lies.

Returns CGAL::ON_POSITIVE_SIDE, CGAL::ON_NEGATIVE_SIDE, or
CGAL::ON_ORIENTED_BOUNDARY. The polygon must be simple.
)pbdoc";

const char *BOUNDED_SIDE_DOC = R"pbdoc(
Returns whether a point lies inside, outside, or on the boundary.

Returns CGAL::ON_BOUNDED_SIDE, CGAL::ON_UNBOUNDED_SIDE, or
CGAL::ON_BOUNDARY. The polygon must be simple.
)pbdoc";

const char *BBOX_DOC = R"pbdoc(
Returns the bounding box of the polygon.

Returns a Bbox_2 enclosing all vertices.
)pbdoc";

const char *AREA_DOC = R"pbdoc(
Returns the signed area of the polygon.

Positive for counterclockwise orientation, negative for clockwise.
)pbdoc";

const char *LEFT_VERTEX_DOC = R"pbdoc(
Returns an iterator to the leftmost vertex.

If multiple vertices share the minimum x-coordinate, the bottommost
among them is returned.
)pbdoc";

const char *RIGHT_VERTEX_DOC = R"pbdoc(
Returns an iterator to the rightmost vertex.

If multiple vertices share the maximum x-coordinate, the topmost
among them is returned.
)pbdoc";

const char *TOP_VERTEX_DOC = R"pbdoc(
Returns an iterator to the topmost vertex.

If multiple vertices share the maximum y-coordinate, the rightmost
among them is returned.
)pbdoc";

const char *BOTTOM_VERTEX_DOC = R"pbdoc(
Returns an iterator to the bottommost vertex.

If multiple vertices share the minimum y-coordinate, the leftmost
among them is returned.
)pbdoc";

const char *CONTAINER_DOC = R"pbdoc(
Returns a reference to the internal vertex container.
)pbdoc";

const char *SIZE_DOC = R"pbdoc(
Returns the number of vertices in the polygon.
)pbdoc";

const char *IS_EMPTY_DOC = R"pbdoc(
Returns true if the polygon has no vertices.
)pbdoc";

const char *CLEAR_DOC = R"pbdoc(
Removes all vertices from the polygon.

After this call, is_empty() returns true.
)pbdoc";

const char *PUSH_BACK_DOC = R"pbdoc(
Appends a vertex to the polygon.

Parameters
----------
p : Point_2
    The point to append as the new last vertex.
)pbdoc";

const char *VERTEX_DOC = R"pbdoc(
Returns a const reference to the vertex at position i.

Parameters
----------
i : int
    Zero-based index in the range [0, size()).
)pbdoc";

const char *REVERSE_ORIENTATION_DOC = R"pbdoc(
Reverses the orientation of the polygon in place.

A CCW polygon becomes CW and vice versa.
)pbdoc";

const char *EDGES_DOC = R"pbdoc(
Returns an iterator range over the edges of the polygon.

Each edge is a Segment_2. The last edge connects the last vertex to
the first vertex.
)pbdoc";

const char *VERTICES_DOC = R"pbdoc(
Returns an iterator range over the vertices of the polygon.
)pbdoc";

const char *DRAW_DOC = R"pbdoc(
Opens a CGAL Qt viewer window and draws the polygon.

Requires CGAL built with Qt6 support. Blocks until the window is closed.
)pbdoc";

// ── 10 constants added April 7, 2026
// ──────────────────────────────────────────

const char *IS_COUNTERCLOCKWISE_ORIENTED_DOC = R"pbdoc(
Returns true if the polygon is counterclockwise oriented.

Equivalent to ``orientation() == CGAL::COUNTERCLOCKWISE``.
)pbdoc";

const char *IS_CLOCKWISE_ORIENTED_DOC = R"pbdoc(
Returns true if the polygon is clockwise oriented.

Equivalent to ``orientation() == CGAL::CLOCKWISE``.
)pbdoc";

const char *IS_COLLINEAR_ORIENTED_DOC = R"pbdoc(
Returns true if the polygon is collinear oriented.

Equivalent to ``orientation() == CGAL::COLLINEAR``. This is the case
when all vertices are collinear.
)pbdoc";

const char *HAS_ON_POSITIVE_SIDE_DOC = R"pbdoc(
Returns true if the point q is on the positive side of the polygon.

The positive side is the left side of a counterclockwise-oriented polygon.
Equivalent to ``oriented_side(q) == CGAL::ON_POSITIVE_SIDE``.
)pbdoc";

const char *HAS_ON_NEGATIVE_SIDE_DOC = R"pbdoc(
Returns true if the point q is on the negative side of the polygon.

The negative side is the right side of a counterclockwise-oriented polygon.
Equivalent to ``oriented_side(q) == CGAL::ON_NEGATIVE_SIDE``.
)pbdoc";

const char *HAS_ON_BOUNDARY_DOC = R"pbdoc(
Returns true if the point q lies on the boundary of the polygon.

Equivalent to ``bounded_side(q) == CGAL::ON_BOUNDARY``.
)pbdoc";

const char *HAS_ON_BOUNDED_SIDE_DOC = R"pbdoc(
Returns true if the point q lies in the bounded region of the polygon.

Equivalent to ``bounded_side(q) == CGAL::ON_BOUNDED_SIDE``.
The polygon must be simple for this to be well-defined.
)pbdoc";

const char *HAS_ON_UNBOUNDED_SIDE_DOC = R"pbdoc(
Returns true if the point q lies in the unbounded region of the polygon.

Equivalent to ``bounded_side(q) == CGAL::ON_UNBOUNDED_SIDE``.
The polygon must be simple for this to be well-defined.
)pbdoc";

const char *VERTEX_MUTABLE_DOC = R"pbdoc(
Returns a mutable reference to the vertex at position i.

Unlike ``vertex()``, this non-const overload allows in-place modification.
)pbdoc";

const char *EDGE_DOC = R"pbdoc(
Returns the edge at position i as a Segment_2.

The edge connects vertex i to vertex (i+1) % size().
)pbdoc";