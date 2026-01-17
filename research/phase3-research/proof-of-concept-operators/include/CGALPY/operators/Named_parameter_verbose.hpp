// Copyright (c) 2026 Utkarsh Khajuria
// Proof-of-concept for GSoC 2026 - CGAL Python Bindings
// Based on Efi Fogel's Named Parameters architecture

#ifndef CGALPY_NAMED_PARAMETER_VERBOSE_HPP
#define CGALPY_NAMED_PARAMETER_VERBOSE_HPP

#include <string>

// For actual implementation:
// #include <nanobind/nanobind.h>
// namespace py = nanobind;

namespace CGALPY {

/*! Operator for verbose Named Parameter (Pattern 1: Simple Value)
 *
 * Python usage:
 *   PMP.function(mesh, {"verbose": True})
 *
 * Type: bool
 * Pattern: Simple Value (boolean flag)
 * Used in: Most PMP functions for debug output
 *
 * Example:
 * ```python
 * PMP.smooth_shape(mesh, 0.01, {
 *     "verbose": True,
 *     "geom_traits": kernel
 * })
 * ```
 *
 * Complexity: LOW - Direct boolean casting
 * Implementation time: 20-30 minutes
 */
struct Named_parameter_verbose {
  const std::string m_name = "verbose";

  template <typename NamedParameters, typename Value>
  auto operator()(NamedParameters &np, Value &value) const {
    // For actual implementation with nanobind:
    // return np.verbose(py::cast<bool>(value));

    // For proof-of-concept (mock):
    // Assume value can be cast to bool
    bool verbose_val = static_cast<bool>(value);
    return np.verbose(verbose_val);
  }
};

} // namespace CGALPY

#endif // CGALPY_NAMED_PARAMETER_VERBOSE_HPP
