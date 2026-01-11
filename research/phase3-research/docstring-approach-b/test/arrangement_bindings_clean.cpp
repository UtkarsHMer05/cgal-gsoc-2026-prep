// Arrangement bindings with Approach B - External Header Docstrings
// This demonstrates how clean the binding code becomes

#include "../include/arrangement_docstrings.hpp"
#include <nanobind/nanobind.h>

namespace nb = nanobind;

// Simulated Arrangement_2 class for demonstration
class Arrangement_2 {
public:
  int insert_from_left_vertex() { return 42; }
  int insert_from_right_vertex() { return 43; }
  int insert_at_vertices() { return 44; }
  int remove_edge() { return 45; }
  int remove_isolated_vertex() { return 46; }
  int split_edge() { return 47; }
  int number_of_vertices() const { return 10; }
  int number_of_edges() const { return 15; }
  int number_of_faces() const { return 5; }
};

NB_MODULE(arrangement_clean, m) {
  m.doc() = "Arrangement_2 bindings - Approach B demonstration";

  nb::class_<Arrangement_2>(m, "Arrangement_2")

      // INSERTION METHODS - Notice how clean this section is!
      .def("insert_from_left_vertex", &Arrangement_2::insert_from_left_vertex,
           CGAL::docstrings::INSERT_FROM_LEFT_VERTEX)

      .def("insert_from_right_vertex", &Arrangement_2::insert_from_right_vertex,
           CGAL::docstrings::INSERT_FROM_RIGHT_VERTEX)

      .def("insert_at_vertices", &Arrangement_2::insert_at_vertices,
           CGAL::docstrings::INSERT_AT_VERTICES)

      // MODIFICATION METHODS
      .def("remove_edge", &Arrangement_2::remove_edge,
           CGAL::docstrings::REMOVE_EDGE)

      .def("remove_isolated_vertex", &Arrangement_2::remove_isolated_vertex,
           CGAL::docstrings::REMOVE_ISOLATED_VERTEX)

      .def("split_edge", &Arrangement_2::split_edge,
           CGAL::docstrings::SPLIT_EDGE)

      // QUERY METHODS
      .def("number_of_vertices", &Arrangement_2::number_of_vertices,
           CGAL::docstrings::NUMBER_OF_VERTICES)

      .def("number_of_edges", &Arrangement_2::number_of_edges,
           CGAL::docstrings::NUMBER_OF_EDGES)

      .def("number_of_faces", &Arrangement_2::number_of_faces,
           CGAL::docstrings::NUMBER_OF_FACES);
}
