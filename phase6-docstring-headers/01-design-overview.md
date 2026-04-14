# Design Overview: Moving CGALPY Docstrings Into Header Files

## Background

Earlier phases (Weeks 3–4) added **inline** docstrings directly inside the
binding `.cpp` files for AOS2 (arrangement on surface 2). This worked, but
the code became hard to read: long `R"pbdoc(...)"` blocks broke up chains of
`.def()` calls and made diffs noisy.[file:21]

At the same time, my mentor Efi had already hinted that “moving the docstring
to a variable is a good idea” and wanted the Python API to stay close to the
C++ CGAL documentation.[file:21]

## High‑level approach

I decided to introduce a small, consistent pattern:

- For each package that has bindings, create a dedicated header in
  `src/libs/cgalpy/lib/docstrings/`.
- Inside that header, define one `const char*` per method, named in a simple
  way: `METHOD_NAME_DOC` (e.g. `IS_SIMPLE_DOC`, `ORIENTATION_DOC`).
- In the binding `.cpp` file, add a single `#include "docstrings/…_docstrings.h"`
  and then pass the appropriate `*_DOC` constant as the last argument to
  each `.def()` call.

Example pattern:

```cpp
#pragma once

const char* IS_SIMPLE_DOC = R"pbdoc(
Returns true if the polygon is simple (no self-intersections).
)pbdoc";
```

and in the binding:

```cpp
#include "docstrings/polygon_2_docstrings.h"

nb::class_<Polygon_2>(m, "Polygon_2", __INIT___DOC)
  .def("is_simple", &Polygon_2::is_simple, IS_SIMPLE_DOC);
```

## Benefits

This design buys me several things:

- Binding code is **visually clean**: the behaviour is visible in `.cpp`,
  the text lives elsewhere.
- The docstrings are **centralised** and can be regenerated or edited
  without touching binding logic.
- It matches CGAL’s philosophy of keeping Python very close to C++:
  most strings are adapted directly from the official CGAL headers
  under `~/cgal/<Package>/doc/<Package>/CGAL/`.[file:21]

## Packages covered

In this phase I created headers for five packages:

- `polygon_2_docstrings.h`
- `alpha_shape_2_docstrings.h`
- `boolean_set_operations_2_docstrings.h`
- `envelope_2_docstrings.h`
- `visibility_2_docstrings.h`[file:21]

AOS2 remains inline for now; I treat it as a separate later migration task.