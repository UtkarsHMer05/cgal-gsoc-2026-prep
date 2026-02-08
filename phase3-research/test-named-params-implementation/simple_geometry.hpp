#pragma once

#include <vector>
#include <string>
#include <optional>

namespace SimpleGeometry {

// Simulates CGAL's Named Parameters pattern
namespace parameters {
    struct Default_named_parameters {};
    
    inline Default_named_parameters default_values() {
        return Default_named_parameters{};
    }
    
    template<typename T>
    struct With_tolerance {
        T tolerance_value;
        
        template<typename U>
        struct With_max_iterations {
            T tolerance_value;
            U max_iter_value;
        };
        
        template<typename U>
        With_max_iterations<U> max_iterations(U value) const {
            return {tolerance_value, value};
        }
    };
    
    template<typename T>
    With_tolerance<T> tolerance(T value) {
        return {value};
    }
}

// Simple function that accepts Named Parameters
// Simulates compute_face_normals pattern
template<typename NamedParameters = parameters::Default_named_parameters>
std::string process_mesh(
    const std::string& mesh_name,
    int vertex_count,
    const NamedParameters& np = parameters::default_values()
) {
    // Extract parameters with defaults
    double tol = 0.001;  // default
    int max_iter = 100;  // default
    
    // In real CGAL code, these would be extracted from np
    // For demo, we'll show the pattern
    
    return "Processed mesh '" + mesh_name + 
           "' with " + std::to_string(vertex_count) + " vertices";
}

} // namespace SimpleGeometry
