// Arrangement bindings with inline docstrings - OLD APPROACH
// This shows how the docstrings "screen" the binding code

#include <nanobind/nanobind.h>

namespace nb = nanobind;

class Arrangement_2 {
public:
  int insert_from_left_vertex() { return 42; }
  int number_of_vertices() const { return 10; }
};

NB_MODULE(arrangement_inline, m) {
  m.doc() = "Arrangement_2 bindings - Inline docstrings (old approach)";

  nb::class_<Arrangement_2>(m, "Arrangement_2")

      // Notice how LONG and HARD TO READ this section becomes!
      .def("insert_from_left_vertex", &Arrangement_2::insert_from_left_vertex,
           R"pbdoc(
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
             )pbdoc")

      .def("number_of_vertices", &Arrangement_2::number_of_vertices,
           R"pbdoc(
Get the number of vertices in the arrangement.

Returns
-------
int
    The total number of vertices.

Examples
--------
>>> count = arr.number_of_vertices()
>>> print(f"Arrangement has {count} vertices")
             )pbdoc");

  // Imagine 40 more methods like this...
  // The binding section becomes unreadable!
}
