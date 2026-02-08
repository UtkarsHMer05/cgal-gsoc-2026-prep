// Proof-of-concept test demonstrating Named Parameters operator pattern
// This compiles WITHOUT full CGAL/nanobind - uses mocks to show the pattern

#include <functional>
#include <iostream>
#include <map>
#include <string>
#include <tuple>
#include <utility>

// ============================================================================
// MOCK IMPLEMENTATIONS (Replace with real nanobind/CGAL in actual code)
// ============================================================================

// Mock nanobind dict
using MockDict = std::map<std::string, int>; // Simplified - just int values

// Mock CGAL parameters
namespace CGAL {
namespace parameters {

struct MockParameters {
  std::string chain; // For visualization

  MockParameters() : chain("default_values()") {}

  MockParameters verbose(bool v) {
    MockParameters result = *this;
    result.chain += ".verbose(" + std::string(v ? "true" : "false") + ")";
    std::cout << "  → Chained: " << result.chain << std::endl;
    return result;
  }

  MockParameters vertex_point_map(int vpm) {
    MockParameters result = *this;
    result.chain += ".vertex_point_map(vpm_" + std::to_string(vpm) + ")";
    std::cout << "  → Chained: " << result.chain << std::endl;
    return result;
  }

  MockParameters geom_traits(int kernel) {
    MockParameters result = *this;
    result.chain += ".geom_traits(kernel_" + std::to_string(kernel) + ")";
    std::cout << "  → Chained: " << result.chain << std::endl;
    return result;
  }

  void print_final() const {
    std::cout << "\n✓ Final parameter chain:\n  " << chain << std::endl;
  }
};

MockParameters default_values() {
  std::cout << "Starting with: CGAL::parameters::default_values()" << std::endl;
  return MockParameters();
}

} // namespace parameters
} // namespace CGAL

// ============================================================================
// INCLUDE OUR OPERATORS
// ============================================================================

#include "../include/CGALPY/operators/Named_parameter_geom_traits.hpp"
#include "../include/CGALPY/operators/Named_parameter_verbose.hpp"
#include "../include/CGALPY/operators/Named_parameter_vertex_point_map.hpp"

// ============================================================================
// APPLICATOR IMPLEMENTATION (Simplified version of Efi's)
// ============================================================================

namespace CGALPY {

// Base case: No more operators
template <typename Wrapper, typename NamedParameter>
auto named_parameter_applicator(Wrapper &wrapper, NamedParameter &np,
                                const MockDict &params) {
  std::cout << "\n→ Base case reached: All operators processed" << std::endl;
  return wrapper(np);
}

// Recursive case: Try operators
template <typename Wrapper, typename NamedParameter, typename NamedParameterOp,
          typename... NamedParameterOps>
auto named_parameter_applicator(Wrapper &wrapper, NamedParameter &np,
                                const MockDict &params, NamedParameterOp op,
                                NamedParameterOps... ops) {
  std::cout << "\n→ Trying operator: " << op.m_name << std::endl;

  for (const auto &item : params) {
    const std::string &key = item.first;
    std::cout << "  Checking dict key: \"" << key << "\" against \""
              << op.m_name << "\"";

    if (key == op.m_name) {
      std::cout << " ✓ MATCH!" << std::endl;
      auto np_new = op(np, item.second);
      std::cout << "  Recursing with updated parameter chain..." << std::endl;
      return named_parameter_applicator(wrapper, np_new, params, ops...);
    } else {
      std::cout << " ✗" << std::endl;
    }
  }

  std::cout << "  No match for \"" << op.m_name << "\", trying next operator..."
            << std::endl;
  return named_parameter_applicator(wrapper, np, params, ops...);
}

} // namespace CGALPY

// ============================================================================
// MOCK WRAPPER (Simulates Named_parameter_wrapper)
// ============================================================================

struct MockWrapper {
  std::string function_name;

  MockWrapper(const std::string &name) : function_name(name) {}

  template <typename NP> void operator()(NP &np) {
    std::cout << "\n→ MockWrapper called for function: " << function_name
              << std::endl;
    np.print_final();
  }
};

// ============================================================================
// TEST FUNCTIONS
// ============================================================================

void test_single_operator() {
  std::cout << "\n" << std::string(70, '=') << std::endl;
  std::cout << "TEST 1: Single Operator (verbose)" << std::endl;
  std::cout << std::string(70, '=') << std::endl;

  MockDict params = {{"verbose", 1}}; // 1 = true
  auto np = CGAL::parameters::default_values();
  CGALPY::Named_parameter_verbose op;
  MockWrapper wrapper("compute_face_normals");

  CGALPY::named_parameter_applicator(wrapper, np, params, op);
}

void test_multiple_operators() {
  std::cout << "\n" << std::string(70, '=') << std::endl;
  std::cout << "TEST 2: Multiple Operators (vertex_point_map + geom_traits)"
            << std::endl;
  std::cout << std::string(70, '=') << std::endl;

  MockDict params = {{"vertex_point_map", 42}, {"geom_traits", 99}};

  auto np = CGAL::parameters::default_values();
  CGALPY::Named_parameter_vertex_point_map op1;
  CGALPY::Named_parameter_geom_traits op2;
  MockWrapper wrapper("smooth_shape");

  CGALPY::named_parameter_applicator(wrapper, np, params, op1, op2);
}

void test_all_three_operators() {
  std::cout << "\n" << std::string(70, '=') << std::endl;
  std::cout << "TEST 3: All Three Operators (Full Chain)" << std::endl;
  std::cout << std::string(70, '=') << std::endl;

  MockDict params = {
      {"vertex_point_map", 123}, {"geom_traits", 456}, {"verbose", 1}};

  auto np = CGAL::parameters::default_values();
  CGALPY::Named_parameter_vertex_point_map op1;
  CGALPY::Named_parameter_geom_traits op2;
  CGALPY::Named_parameter_verbose op3;
  MockWrapper wrapper("isotropic_remeshing");

  CGALPY::named_parameter_applicator(wrapper, np, params, op1, op2, op3);
}

void test_unknown_parameter() {
  std::cout << "\n" << std::string(70, '=') << std::endl;
  std::cout << "TEST 4: Unknown Parameter (Should Skip)" << std::endl;
  std::cout << std::string(70, '=') << std::endl;

  MockDict params = {{"vertex_point_map", 111},
                     {"unknown_param", 999}, // Should be ignored
                     {"verbose", 1}};

  auto np = CGAL::parameters::default_values();
  CGALPY::Named_parameter_vertex_point_map op1;
  CGALPY::Named_parameter_verbose op2;
  // No operator for "unknown_param"
  MockWrapper wrapper("test_function");

  CGALPY::named_parameter_applicator(wrapper, np, params, op1, op2);
}

// ============================================================================
// MAIN
// ============================================================================

int main() {
  std::cout << "\n" << std::string(70, '#') << std::endl;
  std::cout << "# CGAL Named Parameters Operators - Proof of Concept"
            << std::endl;
  std::cout << "# Demonstrates Efi Fogel's operator-based pattern" << std::endl;
  std::cout << std::string(70, '#') << std::endl;

  test_single_operator();
  test_multiple_operators();
  test_all_three_operators();
  test_unknown_parameter();

  std::cout << "\n" << std::string(70, '#') << std::endl;
  std::cout << "# All Tests Complete!" << std::endl;
  std::cout << "#" << std::endl;
  std::cout << "# This demonstrates:" << std::endl;
  std::cout << "#   1. Operator pattern with m_name matching" << std::endl;
  std::cout << "#   2. Parameter chaining (compile-time in real CGAL)"
            << std::endl;
  std::cout << "#   3. Variadic template recursion" << std::endl;
  std::cout << "#   4. Unknown parameters silently ignored" << std::endl;
  std::cout << std::string(70, '#') << std::endl;
  std::cout << std::endl;

  return 0;
}
