# Alpha Shapes, Boolean Set Ops, Envelope, and Visibility

After Polygon_2, I applied the same pattern to four more packages that
already had bindings.

## Files created

I added the following headers under
`src/libs/cgalpy/lib/docstrings/`:[file:21]

- `alpha_shape_2_docstrings.h`
- `boolean_set_operations_2_docstrings.h`
- `envelope_2_docstrings.h`
- `visibility_2_docstrings.h`

Each file uses the same simple structure:

```cpp
#pragma once

const char* METHOD_NAME_DOC = R"pbdoc(
Short, focused description adapted from CGAL docs.
)pbdoc";
```

## Alpha Shapes (As2)

For alpha shapes I documented methods such as:

- `ALPHA_DOC`, `SET_ALPHA_DOC`, `ALPHA_COUNT_DOC`,
  `GET_NTH_ALPHA_DOC`
- `FIND_OPTIMAL_ALPHA_DOC`
- `CLASSIFY_DOC` (INTERIOR / REGULAR / SINGULAR / EXTERIOR)
- `NUMBER_OF_SOLID_COMPONENTS_DOC`
- `ALPHA_SHAPE_VERTICES_DOC`, `ALPHA_SHAPE_EDGES_DOC`
- `MAKE_ALPHA_SHAPE_DOC`[file:21]

These texts are adapted from the Alpha_shapes_2 documentation and explain
in plain language what the alpha parameter means and how classification
works.

## Boolean Set Operations (Bso2)

For boolean set operations I focused on the core set-theoretic API:

- `DO_INTERSECT_DOC`
- `INTERSECTION_DOC`
- `JOIN_DOC`
- `DIFFERENCE_DOC`
- `SYMMETRIC_DIFFERENCE_DOC`
- `COMPLEMENT_DOC`
- `IS_VALID_DOC`[file:21]

The goal is that if someone knows basic set operations from math, they can
read these docstrings and immediately understand what the function does.

## Envelope_2 (Env2)

Envelope_2 is a bit more geometric. I documented:

- `LOWER_ENVELOPE_X_MONOTONE_DOC`
- `UPPER_ENVELOPE_X_MONOTONE_DOC`
- `LOWER_ENVELOPE_DOC`, `UPPER_ENVELOPE_DOC`
- `MINIMIZATION_DIAGRAM_DOC`, `MAXIMIZATION_DIAGRAM_DOC`
- `DIAGRAM_VERTEX_DOC`, `DIAGRAM_EDGE_DOC`, `DIAGRAM_FACE_DOC`[file:21]

Here the emphasis is on explaining “envelope” in intuitive language:
“piecewise-linear surface that bounds a set of functions from below/above”
and what a minimization/maximization diagram actually is.

## Visibility_2 (Vis2)

Visibility_2 is relatively small; I documented:

- `COMPUTE_VISIBILITY_DOC`
- `COMPUTE_VISIBILITY_HALFEDGE_DOC`
- `IS_ATTACHED_DOC`
- `ATTACH_DOC`
- `DETACH_DOC`[file:21]

These explain how to compute visibility polygons from a point or a point
on a boundary halfedge and how the visibility object attaches to an
arrangement.

## Wiring into the bindings

For each of these packages I:

1. Added an `#include "docstrings/<name>_docstrings.h"` at the top of the
   corresponding `*_bindings.cpp` file.
2. Updated each `.def()` call to pass the proper `*_DOC` constant as the
   last argument.
3. Rebuilt CGALPY.
4. Ran runtime checks such as:

   ```python
   import CGALPY
   help(CGALPY.As2.Alpha_shape_2)
   help(CGALPY.Bso2)
   help(CGALPY.Env2)
   help(CGALPY.Vis2)
   ```

   and spot-checked at least three methods per module.[file:21]

In total, across Polygon_2, Alpha_shapes_2, Boolean_set_operations_2,
Envelope_2, and Visibility_2, I wired **119 `.def()` call sites** to their
docstring constants and verified 15 representative `__doc__` values at
runtime.[file:21]