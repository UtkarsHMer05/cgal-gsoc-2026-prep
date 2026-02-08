#pragma once

// External Docstring Header - Approach B
// Separates documentation from binding code for improved readability
// Date: January 11, 2026
// Author: Utkarsh Khajuria

namespace CGAL {
namespace docstrings {

// ============================================================
// ARRANGEMENT INSERTION METHODS
// ============================================================

constexpr const char *INSERT_FROM_LEFT_VERTEX = R"pbdoc(
Insert a curve from a vertex that corresponds to its left endpoint.

Parameters
----------
curve : Curve
    The curve to insert.
vertex : Vertex
    The source vertex (left endpoint of the curve).

Returns
-------
Halfedge
    A halfedge directed from the source vertex toward the target vertex.

Examples
--------
>>> arr = Arrangement_2()
>>> unbounded = arr.unbounded_face()
>>> v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
>>> seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
>>> he = arr.insert_from_left_vertex(seg, v1)
>>> print(f"Inserted edge from {he.source().point()} to {he.target().point()}")

Notes
-----
The vertex must already exist in the arrangement and must correspond
to the curve's left endpoint according to the traits class.
)pbdoc";

constexpr const char *INSERT_FROM_RIGHT_VERTEX = R"pbdoc(
Insert a curve from a vertex that corresponds to its right endpoint.

Parameters
----------
curve : Curve
    The curve to insert.
vertex : Vertex
    The source vertex (right endpoint of the curve).

Returns
-------
Halfedge
    A halfedge directed from the source vertex toward the target vertex.

Examples
--------
>>> v1 = arr.insert_in_face_interior(Point_2(5, 5), unbounded)
>>> seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
>>> he = arr.insert_from_right_vertex(seg, v1)

Notes
-----
The vertex must correspond to the curve's right endpoint.
The returned halfedge is directed from right to left along the curve.
)pbdoc";

constexpr const char *INSERT_AT_VERTICES = R"pbdoc(
Insert a curve between two existing vertices.

Parameters
----------
curve : Curve
    The curve to insert.
source : Vertex
    The source vertex.
target : Vertex
    The target vertex.

Returns
-------
Halfedge
    A halfedge directed from source to target.

Examples
--------
>>> v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
>>> v2 = arr.insert_in_face_interior(Point_2(5, 5), unbounded)
>>> seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
>>> he = arr.insert_at_vertices(seg, v1, v2)

Notes
-----
Both vertices must already exist in the arrangement.
The curve endpoints must match the vertex positions.
)pbdoc";

// ============================================================
// ARRANGEMENT MODIFICATION METHODS
// ============================================================

constexpr const char *REMOVE_EDGE = R"pbdoc(
Remove an edge from the arrangement.

Parameters
----------
halfedge : Halfedge
    A halfedge representing the edge to remove.
remove_source : bool, optional
    Whether to remove the source vertex if it becomes isolated (default: True).
remove_target : bool, optional
    Whether to remove the target vertex if it becomes isolated (default: True).

Returns
-------
Face
    The face that remains after edge removal.

Examples
--------
>>> he = arr.insert_from_left_vertex(seg, v1)
>>> face = arr.remove_edge(he)
>>> print(f"Edge removed, face has {face.number_of_outer_ccbs()} outer boundaries")

Warnings
--------
After calling this method, the halfedge handle becomes invalid.
Do not use it or its twin after removal.
)pbdoc";

constexpr const char *REMOVE_ISOLATED_VERTEX = R"pbdoc(
Remove an isolated vertex from the arrangement.

Parameters
----------
vertex : Vertex
    The isolated vertex to remove.

Returns
-------
Face
    The face that contained the vertex.

Examples
--------
>>> v = arr.insert_in_face_interior(Point_2(3, 3), unbounded)
>>> face = arr.remove_isolated_vertex(v)

Warnings
--------
The vertex must be isolated (degree 0). If the vertex has incident
edges, this method will cause a crash. Check with vertex.is_isolated()
before calling.

After removal, the vertex handle becomes invalid.
)pbdoc";

constexpr const char *SPLIT_EDGE = R"pbdoc(
Split an edge into two edges at a given point.

Parameters
----------
halfedge : Halfedge
    The halfedge representing the edge to split.
curve1 : Curve
    The first curve segment (from source to split point).
curve2 : Curve
    The second curve segment (from split point to target).

Returns
-------
Halfedge
    A halfedge representing the second curve segment.

Examples
--------
>>> he = arr.insert_from_left_vertex(seg, v1)
>>> seg1 = Segment_2(Point_2(0, 0), Point_2(2.5, 2.5))
>>> seg2 = Segment_2(Point_2(2.5, 2.5), Point_2(5, 5))
>>> he_new = arr.split_edge(he, seg1, seg2)

Notes
-----
The original halfedge is modified in place to represent the first segment.
A new halfedge is returned for the second segment.
The split point must lie on the original curve.
)pbdoc";

// ============================================================
// ARRANGEMENT QUERY METHODS
// ============================================================

constexpr const char *NUMBER_OF_VERTICES = R"pbdoc(
Get the number of vertices in the arrangement.

Returns
-------
int
    The total number of vertices.

Examples
--------
>>> count = arr.number_of_vertices()
>>> print(f"Arrangement has {count} vertices")
)pbdoc";

constexpr const char *NUMBER_OF_EDGES = R"pbdoc(
Get the number of edges in the arrangement.

Returns
-------
int
    The total number of edges (halfedge pairs).

Examples
--------
>>> count = arr.number_of_edges()
>>> print(f"Arrangement has {count} edges")
)pbdoc";

constexpr const char *NUMBER_OF_FACES = R"pbdoc(
Get the number of faces in the arrangement.

Returns
-------
int
    The total number of faces (including unbounded face).

Examples
--------
>>> count = arr.number_of_faces()
>>> print(f"Arrangement has {count} faces")

Notes
-----
Every arrangement has at least one face (the unbounded face).
)pbdoc";

} // namespace docstrings
} // namespace CGAL
