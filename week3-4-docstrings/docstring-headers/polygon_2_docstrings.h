#pragma once

// ============================================================================
// polygon_2_docstrings.h
// CGAL Python Bindings — Polygon_2 docstring constants
// Generated: April 1, 2026 (initial 22 constants)
// Updated:   April 7, 2026 (10 missing constants appended — total: 32)
//
// Source: CGAL official Polygon_2 reference
//   https://doc.cgal.org/latest/Polygon/classCGAL_1_1Polygon__2.html
//   ~/cgal/Polygon/doc/Polygon/CGAL/
//
// Usage in polygon_2_bindings.cpp:
//   #include "docstrings/polygon_2_docstrings.h"
//   ...
//   .def("is_simple", &Pgn::is_simple, IS_SIMPLE_DOC)
// ============================================================================

// ----------------------------------------------------------------------------
// Constructor
// ----------------------------------------------------------------------------

const char *__INIT___DOC = R"pbdoc(
Construct a Polygon_2 from an optional sequence of Point_2 vertices.

Parameters
----------
points : iterable of Point_2, optional
    The vertices of the polygon in order. If omitted, an empty polygon
    is created. The polygon is not automatically closed; the last
    edge is implicitly from the last vertex back to the first.
)pbdoc";

// ----------------------------------------------------------------------------
// Predicates
// ----------------------------------------------------------------------------

const char *IS_SIMPLE_DOC = R"pbdoc(
Returns true if the polygon is simple.

A polygon is simple if its boundary does not self-intersect (edges only
share endpoints at consecutive vertices, not elsewhere).
)pbdoc";

const char *IS_CONVEX_DOC = R"pbdoc(
Returns true if the polygon is convex.

A polygon is convex if for every pair of points inside the polygon, the
line segment connecting them lies entirely inside the polygon. Requires
the polygon to be simple.
)pbdoc";

const char *ORIENTATION_DOC = R"pbdoc(
Returns the orientation of the polygon.

Returns
-------
CGAL.Orientation
    ``CGAL::COUNTERCLOCKWISE``, ``CGAL::CLOCKWISE``, or ``CGAL::COLLINEAR``.
    Collinear is returned when all vertices are collinear.
)pbdoc";

const char *ORIENTED_SIDE_DOC = R"pbdoc(
Returns the oriented side of the polygon on which a point lies.

Parameters
----------
q : Point_2
    The query point.

Returns
-------
CGAL.Oriented_side
    ``CGAL::ON_POSITIVE_SIDE``, ``CGAL::ON_NEGATIVE_SIDE``, or
    ``CGAL::ON_ORIENTED_BOUNDARY``.
)pbdoc";

const char *BOUNDED_SIDE_DOC = R"pbdoc(
Returns the region of the polygon in which a point lies.

Parameters
----------
q : Point_2
    The query point.

Returns
-------
CGAL.Bounded_side
    ``CGAL::ON_BOUNDED_SIDE``, ``CGAL::ON_BOUNDARY``, or
    ``CGAL::ON_UNBOUNDED_SIDE``. The polygon must be simple.
)pbdoc";

const char *IS_EMPTY_DOC = R"pbdoc(
Returns true if the polygon has no vertices.
)pbdoc";

// ----------------------------------------------------------------------------
// Orientation predicates (the 10 that were MISSING — added April 7, 2026)
// ----------------------------------------------------------------------------

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
Returns true if the point ``q`` is on the positive side of the polygon.

The positive side is the left side of a counterclockwise-oriented polygon.
Equivalent to ``oriented_side(q) == CGAL::ON_POSITIVE_SIDE``.
)pbdoc";

const char *HAS_ON_NEGATIVE_SIDE_DOC = R"pbdoc(
Returns true if the point ``q`` is on the negative side of the polygon.

The negative side is the right side of a counterclockwise-oriented polygon.
Equivalent to ``oriented_side(q) == CGAL::ON_NEGATIVE_SIDE``.
)pbdoc";

const char *HAS_ON_BOUNDARY_DOC = R"pbdoc(
Returns true if the point ``q`` lies on the boundary of the polygon.

Equivalent to ``bounded_side(q) == CGAL::ON_BOUNDARY``.
)pbdoc";

const char *HAS_ON_BOUNDED_SIDE_DOC = R"pbdoc(
Returns true if the point ``q`` lies in the bounded region of the polygon.

Equivalent to ``bounded_side(q) == CGAL::ON_BOUNDED_SIDE``.
The polygon must be simple for this to be well-defined.
)pbdoc";

const char *HAS_ON_UNBOUNDED_SIDE_DOC = R"pbdoc(
Returns true if the point ``q`` lies in the unbounded region of the polygon.

Equivalent to ``bounded_side(q) == CGAL::ON_UNBOUNDED_SIDE``.
The polygon must be simple for this to be well-defined.
)pbdoc";

const char *VERTEX_MUTABLE_DOC = R"pbdoc(
Returns a mutable reference to the vertex at position ``i``.

Unlike ``vertex()``, this overload returns a non-const reference that
allows the vertex coordinates to be modified in place.
)pbdoc";

const char *EDGE_DOC = R"pbdoc(
Returns the edge of the polygon at position ``i`` as a Segment_2.

The edge connects vertex ``i`` to vertex ``(i+1) % size()``.
)pbdoc";

// ----------------------------------------------------------------------------
// Accessors
// ----------------------------------------------------------------------------

const char *SIZE_DOC = R"pbdoc(
Returns the number of vertices of the polygon.
)pbdoc";

const char *AREA_DOC = R"pbdoc(
Returns the signed area of the polygon.

The area is positive for a counterclockwise-oriented polygon and negative
for a clockwise-oriented polygon. Uses the shoelace formula.
)pbdoc";

const char *BBOX_DOC = R"pbdoc(
Returns the bounding box of the polygon.

Returns
-------
CGAL.Bbox_2
    The smallest axis-aligned bounding box that contains all vertices.
)pbdoc";

const char *LEFT_VERTEX_DOC = R"pbdoc(
Returns an iterator to the leftmost vertex of the polygon.

If multiple vertices share the minimum x-coordinate, the bottommost
among them is returned.
)pbdoc";

const char *RIGHT_VERTEX_DOC = R"pbdoc(
Returns an iterator to the rightmost vertex of the polygon.

If multiple vertices share the maximum x-coordinate, the topmost
among them is returned.
)pbdoc";

const char *TOP_VERTEX_DOC = R"pbdoc(
Returns an iterator to the topmost vertex of the polygon.

If multiple vertices share the maximum y-coordinate, the rightmost
among them is returned.
)pbdoc";

const char *BOTTOM_VERTEX_DOC = R"pbdoc(
Returns an iterator to the bottommost vertex of the polygon.

If multiple vertices share the minimum y-coordinate, the leftmost
among them is returned.
)pbdoc";

const char *VERTEX_DOC = R"pbdoc(
Returns a const reference to the vertex at position ``i``.

Parameters
----------
i : int
    Zero-based index of the vertex. Must satisfy ``0 <= i < size()``.
)pbdoc";

const char *CONTAINER_DOC = R"pbdoc(
Returns a reference to the internal container holding the polygon vertices.

The container is a sequence of Point_2 objects stored in order.
)pbdoc";

// ----------------------------------------------------------------------------
// Modifiers
// ----------------------------------------------------------------------------

const char *PUSH_BACK_DOC = R"pbdoc(
Appends a vertex to the polygon.

Parameters
----------
p : Point_2
    The point to append as the new last vertex.
)pbdoc";

const char *CLEAR_DOC = R"pbdoc(
Removes all vertices from the polygon.

After this call ``is_empty()`` returns true.
)pbdoc";

const char *REVERSE_ORIENTATION_DOC = R"pbdoc(
Reverses the orientation of the polygon.

Reverses the order of the vertices in place. A counterclockwise polygon
becomes clockwise and vice versa.
)pbdoc";

// ----------------------------------------------------------------------------
// Iterators
// ----------------------------------------------------------------------------

const char *VERTICES_DOC = R"pbdoc(
Returns an iterator range over the vertices of the polygon.

Yields
------
Point_2
    Each vertex of the polygon in order.
)pbdoc";

const char *EDGES_DOC = R"pbdoc(
Returns an iterator range over the edges of the polygon.

Yields
------
Segment_2
    Each directed edge of the polygon in order. The last edge connects
    the last vertex back to the first vertex.
)pbdoc";

// ----------------------------------------------------------------------------
// Drawing
// ----------------------------------------------------------------------------

const char *DRAW_DOC = R"pbdoc(
Opens a CGAL viewer window and draws the polygon.

Requires CGAL to be compiled with Qt6 support. This call blocks until the
viewer window is closed.
)pbdoc";
