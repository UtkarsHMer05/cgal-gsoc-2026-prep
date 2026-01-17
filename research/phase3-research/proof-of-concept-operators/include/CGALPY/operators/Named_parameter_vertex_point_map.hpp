// Copyright (c) 2026 Utkarsh Khajuria
// Proof-of-concept for GSoC 2026 - CGAL Python Bindings
// Based on Efi Fogel's Named Parameters architecture

#ifndef CGALPY_NAMED_PARAMETER_VERTEX_POINT_MAP_HPP
#define CGALPY_NAMED_PARAMETER_VERTEX_POINT_MAP_HPP

#include <string>

// For actual implementation:
// #include <nanobind/nanobind.h>
// #include <boost/graph/graph_traits.hpp>
// #include "CGALPY/polygon_mesh_processing_types.hpp"

namespace CGALPY {

/*! Operator for vertex_point_map Named Parameter (Pattern 2: Property Map)
 *
 * Python usage:
 *   vpm = mesh.points()
 *   PMP.function(mesh, {"vertex_point_map": vpm})
 *
 * Type: Property_map<Vertex_descriptor, Point_3>
 * Pattern: Property Map (most common PMP parameter)
 * Used in: ~30 PMP functions (smooth_shape, fair, isotropic_remeshing, etc.)
 *
 * Example:
 * ```python
 * mesh = Surface_mesh()
 * vpm = mesh.points()  # Get default property map
 *
 * PMP.smooth_shape(mesh, 0.01, {
 *     "vertex_point_map": vpm,
 *     "geom_traits": kernel
 * })
 * ```
 *
 * Type Details:
 * - Surface_mesh: Surface_mesh::Property_map<Vertex_index, Point_3>
 * - Polyhedron_3: boost::property_map<Polyhedron, vertex_point_tag>::type
 *
 * Complexity: MEDIUM - Generic property map handling
 * Implementation time: 40-50 minutes
 */
struct Named_parameter_vertex_point_map {
  const std::string m_name = "vertex_point_map";

  template <typename NamedParameters, typename Value>
  auto operator()(NamedParameters &np, Value &value) const {
    // For actual implementation with nanobind:
    // Property map type is resolved by nanobind automatically
    // No explicit casting needed - nanobind handles it
    // return np.vertex_point_map(value);

    // For proof-of-concept (mock):
    // Assume value is already correct property map type
    return np.vertex_point_map(value);
  }
};

} // namespace CGALPY

#endif // CGALPY_NAMED_PARAMETER_VERTEX_POINT_MAP_HPP
