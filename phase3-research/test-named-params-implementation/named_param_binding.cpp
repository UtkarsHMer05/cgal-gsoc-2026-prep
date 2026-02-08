#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>

#include "simple_geometry.hpp"

namespace nb = nanobind;
namespace SG = SimpleGeometry;

// Python-facing function with dict parameter
std::string process_mesh_py(const std::string &mesh_name, int vertex_count,
                            const nb::dict &params = nb::dict()) {
  // Start with defaults
  auto np = SG::parameters::default_values();

  // Parse and apply parameters
  if (params.contains("tolerance") && params.contains("max_iterations")) {
    // Both parameters provided
    double tol = nb::cast<double>(params["tolerance"]);
    int max_iter = nb::cast<int>(params["max_iterations"]);
    auto np_full = SG::parameters::tolerance(tol).max_iterations(max_iter);
    return SG::process_mesh(mesh_name, vertex_count, np_full);
  } else if (params.contains("tolerance")) {
    // Only tolerance provided
    double tol = nb::cast<double>(params["tolerance"]);
    auto np_tol = SG::parameters::tolerance(tol);
    return SG::process_mesh(mesh_name, vertex_count, np_tol);
  } else {
    // No parameters, use defaults
    return SG::process_mesh(mesh_name, vertex_count, np);
  }
}

NB_MODULE(named_param_test, m) {
  m.doc() = "Test module demonstrating CGAL Named Parameters pattern";

  m.def("process_mesh", &process_mesh_py, nb::arg("mesh_name"),
        nb::arg("vertex_count"), nb::arg("np") = nb::dict(),
        R"pbdoc(
Process a mesh with optional named parameters.

Parameters
----------
mesh_name : str
    Name of the mesh
vertex_count : int
    Number of vertices
np : dict, optional
    Named parameters. Accepts:
    - 'tolerance' : float (default: 0.001)
    - 'max_iterations' : int (default: 100)

Returns
-------
str
    Processing result message

Examples
--------
>>> result = process_mesh("cube", 8)
>>> result = process_mesh("cube", 8, {"tolerance": 0.0001})
          )pbdoc");
}