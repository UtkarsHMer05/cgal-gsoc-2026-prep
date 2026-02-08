cmake_minimum_required(VERSION 3.15)
project(named_param_test)

set(CMAKE_CXX_STANDARD 17)

# Find Python
find_package(Python COMPONENTS Interpreter Development REQUIRED)

# Fetch nanobind
include(FetchContent)
FetchContent_Declare(
    nanobind
    GIT_REPOSITORY https://github.com/wjakob/nanobind.git
    GIT_TAG v2.0.0
)
FetchContent_MakeAvailable(nanobind)

# Create the extension module
nanobind_add_module(named_param_test named_param_binding.cpp)
