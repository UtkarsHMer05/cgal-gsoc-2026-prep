# Proof-of-concept CMakeLists.txt
# NOTE: This is for REFERENCE ONLY - not meant to be built in prep repo
# Actual implementation will be in cgal-python-bindings during GSoC

cmake_minimum_required(VERSION 3.15)
project(cgal_named_params_poc CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include directory
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

# Mock test executable (demonstrates pattern without CGAL/nanobind)
add_executable(mock_test src/mock_test.cpp)

# Compile options
if(MSVC)
  target_compile_options(mock_test PRIVATE /W4)
else()
  target_compile_options(mock_test PRIVATE -Wall -Wextra -Wpedantic)
endif()

message(STATUS "")
message(STATUS "========================================")
message(STATUS "CGAL Named Parameters - Proof of Concept")
message(STATUS "========================================")
message(STATUS "")
message(STATUS "This is a REFERENCE implementation.")
message(STATUS "Shows operator pattern without full CGAL.")
message(STATUS "")
message(STATUS "NOTE: Not meant to be built in prep repo!")
message(STATUS "Actual implementation during GSoC Weeks 7-8")
message(STATUS "in cgal-python-bindings repository.")
message(STATUS "")
message(STATUS "========================================")
