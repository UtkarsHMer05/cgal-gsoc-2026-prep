# Weeks 1-2: Parameter Naming — nb::arg()

**Date:** March 4, 2026  
**File:** `src/libs/cgalpy/lib/arrangement_on_surface_2_bindings.cpp`  
**Branch:** `feature/named-params-operators-poc`  

## What Was Done

Added `py::arg("name")` to every `.def()` call in `export_aos()`.
Enables keyword argument calls from Python, e.g.:
  arr.insert_in_face_interior(p=p4, f=f)

## Methods Updated

| Method | Args Added |
|---|---|
| insert_from_left_vertex (v) | xcv, v |
| insert_from_left_vertex (h) | xcv, h |
| insert_from_right_vertex (v) | xcv, v |
| insert_from_right_vertex (h) | xcv, h |
| insert_in_face_interior (xcv) | xcv, f |
| insert_in_face_interior (point) | p, f |
| insert_at_vertices (v1,v2) | xcv, v1, v2 |
| insert_at_vertices (h1,v2) | xcv, h1, v2 |
| insert_at_vertices (h1,h2) | xcv, h1, h2 |
| modify_vertex | v, p |
| remove_isolated_vertex | v |
| modify_edge | e, xcv |
| split_edge | e, c1, c2 |
| merge_edge | e1, e2, xcv |
| remove_edge | e |

## Also Restored 5 Missing Overloads
- insert_from_left_vertex2
- insert_from_right_vertex2
- insert_pnt_in_face_interior
- insert_at_vertices3
- insert_at_vertices4

## Test Verification
```python
v = arr.insert_in_face_interior(p=p4, f=f)
# Output: Vertices: 4, Edges: 2, Faces: 1 ✅