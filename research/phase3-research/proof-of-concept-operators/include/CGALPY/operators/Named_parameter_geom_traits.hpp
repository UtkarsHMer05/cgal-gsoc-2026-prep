// Copyright (c) 2026 Utkarsh Khajuria
// Proof-of-concept for GSoC 2026 - CGAL Python Bindings
// Based on Efi Fogel's Named Parameters architecture

#ifndef CGALPY_NAMED_PARAMETER_GEOM_TRAITS_HPP
#define CGALPY_NAMED_PARAMETER_GEOM_TRAITS_HPP

#include <string>

// For actual implementation:
// #include <nanobind/nanobind.h>
// #include "CGALPY/kernel_types.hpp"
// namespace py = nanobind;

namespace CGALPY {

/*! Operator for geom_traits Named Parameter (Pattern 3: Kernel/Traits)
 *
 * Python usage:
 *   from CGALPY.Ker import Kernel
 *   kernel = Kernel()
 *   PMP.function(mesh, {"geom_traits": kernel})
 *
 * Type: const Kernel&
 * Pattern: Kernel/Traits (geometry kernel parameter)
 * Used in: Many PMP functions requiring geometric operations
 *
 * Example:
 * ```python
 * from CGALPY.Ker import Kernel
 *
 * kernel = Kernel()
 * PMP.compute_face_normals(mesh, fnormals, {
 *     "geom_traits": kernel
 * })
 * ```
 *
 * Note: This operator already exists in cgal-python-bindings
 *       (include/CGALPY/Named_parameter_geom_traits.hpp)
 *       Reproduced here for completeness of proof-of-concept
 *
 * Complexity: MEDIUM - Explicit kernel type casting
 * Implementation time: 30-40 minutes
 */
struct Named_parameter_geom_traits {
  const std::string m_name = "geom_traits";

  template <typename NamedParameters, typename Value>
  auto operator()(NamedParameters &np, Value &value) const {
    // For actual implementation with nanobind:
    // return np.geom_traits(py::cast<const Kernel&>(value));

    // For proof-of-concept (mock):
    // Assume Kernel is a mock type
    // In real implementation, Kernel is from CGALPY/kernel_types.hpp
    return np.geom_traits(value);
  }
};

} // namespace CGALPY

#endif // CGALPY_NAMED_PARAMETER_GEOM_TRAITS_HPP
