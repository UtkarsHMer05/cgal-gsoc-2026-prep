# Polygon_2 Docstring Implementation

## Why Polygon_2 mattered

`Polygon_2` is one of the most user-facing pieces of CGALPY. It has a
reasonable but non-trivial set of methods: orientation queries, point
location (bounded / unbounded / boundary), vertex access, container access,
and some viewer integration (`draw`).[file:21]

It was the first package where I wanted the full “header-based docstring”
story to be correct end-to-end.

## Building `polygon_2_docstrings.h`

I created `src/libs/cgalpy/lib/docstrings/polygon_2_docstrings.h` and
initially populated it with 22 docstring constants. These covered things
like:

- Construction: `__INIT___DOC`
- Basic predicates: `IS_SIMPLE_DOC`, `IS_CONVEX_DOC`, `ORIENTATION_DOC`
- Side and containment: `ORIENTED_SIDE_DOC`, `BOUNDED_SIDE_DOC`
- Size and geometry: `SIZE_DOC`, `AREA_DOC`, `BBOX_DOC`
- Extreme vertices: `LEFT_VERTEX_DOC`, `RIGHT_VERTEX_DOC`,
  `TOP_VERTEX_DOC`, `BOTTOM_VERTEX_DOC`
- Container access and mutations: `CONTAINER_DOC`, `PUSH_BACK_DOC`,
  `CLEAR_DOC`, `VERTEX_DOC`
- Iterators and viewer: `VERTICES_DOC`, `EDGES_DOC`, `DRAW_DOC`[file:21]

All of these were short, human-readable summaries adapted from the CGAL
Polygon_2 documentation in `~/cgal/Polygon/doc/Polygon/CGAL/`.[file:21]

## Discovering the “10 missing constants” issue

While preparing a summary of this work, I noticed something subtle:

- `polygon_2_bindings.cpp` already referenced **32** docstring constants
  in its `.def()` calls.
- `polygon_2_docstrings.h` only defined **22** of them.[file:21]

The missing ten were exactly the more advanced predicates and helpers:

- `IS_COUNTERCLOCKWISE_ORIENTED_DOC`
- `IS_CLOCKWISE_ORIENTED_DOC`
- `IS_COLLINEAR_ORIENTED_DOC`
- `HAS_ON_POSITIVE_SIDE_DOC`
- `HAS_ON_NEGATIVE_SIDE_DOC`
- `HAS_ON_BOUNDARY_DOC`
- `HAS_ON_BOUNDED_SIDE_DOC`
- `HAS_ON_UNBOUNDED_SIDE_DOC`
- `VERTEX_MUTABLE_DOC`
- `EDGE_DOC`[file:21]

This meant that a clean build from scratch would have failed with
“undeclared identifier” errors for those constants.

## Fixing it properly

I went back to the CGAL Polygon_2 documentation and wrote precise
descriptions for each of the missing methods. Section 4 of my master
prompt contains the exact `R"pbdoc(...)"` texts that I use.[file:21]

I then appended these ten `const char*` definitions at the end of
`polygon_2_docstrings.h`, so that the header now exposes all **32**
constants referenced by the binding code.

After that:

1. `polygon_2_bindings.cpp` includes the header.
2. Every `.def()` for Polygon_2 passes the appropriate `*_DOC`.
3. A rebuild of CGALPY succeeds.
4. Runtime spot checks like

   ```python
   import CGALPY
   help(CGALPY.Pol2.Polygon_2.is_simple)
   help(CGALPY.Pol2.Polygon_2.has_on_bounded_side)
   ```

   show the expected text, including the newly added predicates.[file:21]

## Takeaway

Polygon_2 ended up as the “reference implementation” of this header-based
docstring pattern:

- It demonstrates the naming convention for constants.
- It shows how to keep bindings and headers in sync.
- It forced me to think through what happens when the header is incomplete
  even though the binding already expects documentation.