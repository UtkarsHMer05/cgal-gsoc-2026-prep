// Proof-of-concept: External docstring variables
// Author: Utkarsh Khajuria
// Date: January 5, 2026

#include <nanobind/nanobind.h>

namespace nb = nanobind;

// ============================================================================
// DOCSTRINGS SECTION - Approach A (Variables at top)
// ============================================================================

const char* SIMPLE_FUNCTION_DOC = R"pbdoc(
A simple function to test external docstrings.

This demonstrates that docstrings can be defined as variables at the top
of the file, making the binding code much cleaner and easier to read.

Parameters
----------
x : int
    The input integer value

Returns
-------
int
    The input value multiplied by 2

Examples
--------
>>> simple_function(5)
10
>>> simple_function(-3)
-6

Notes
-----
This is a proof-of-concept for Approach A: defining docstrings as
const char* variables before the binding code.
)pbdoc";

const char* ADD_FUNCTION_DOC = R"pbdoc(
Add two integers together.

Parameters
----------
a : int
    First integer
b : int
    Second integer

Returns
-------
int
    Sum of a and b
)pbdoc";

// ============================================================================
// C++ FUNCTIONS (What we're binding)
// ============================================================================

int simple_function(int x) {
    return x * 2;
}

int add_function(int a, int b) {
    return a + b;
}

// ============================================================================
// BINDINGS (Notice how clean this section is!)
// ============================================================================

NB_MODULE(test_module, m) {
    m.doc() = "Test module for external docstring approach";
    
    // Look how clean these bindings are compared to inline docstrings!
    m.def("simple_function", 
          &simple_function, 
          nb::arg("x"),
          SIMPLE_FUNCTION_DOC);  // <-- Just one line!
    
    m.def("add_function",
          &add_function,
          nb::arg("a"),
          nb::arg("b"),
          ADD_FUNCTION_DOC);     // <-- Clean!
}
