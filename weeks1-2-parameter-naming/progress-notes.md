# Weeks 1-2: Progress on Parameter Naming

**Status:** Complete  
**Time Spent:** ~5h  
**Dates:** March 4-11, 2026  
**Branch:** `feature/named-params-operators-poc`

## What I Did

* **March 4:** Went through `arrangement_on_surface_2_bindings.cpp` and added `nb::arg()` to every mutation method. There were a lot more methods than initially expected, so I had to be careful not to miss any overloads.
* **March 11:** Covered the `Vertex`, `Halfedge`, and `Face` binding files. In the process, I actually found 5 overloads that were altogether missing and went ahead and restored them!

## The Result

The Python bindings now successfully accept keyword arguments:

```python
arr.insert_in_face_interior(p=point, f=face)
arr.remove_isolated_vertex(v=vertex)
```

The build passes cleanly. Running a quick sanity test also gives the correct output:
> `3 vertices, 2 edges, 1 face after basic insertion.`

## Files Changed in `cgal-python-bindings`

* `src/libs/cgalpy/lib/arrangement_on_surface_2_bindings.cpp`
* `src/libs/cgalpy/lib/aos2_vertex_bindings.cpp`
* `src/libs/cgalpy/lib/aos2_halfedge_bindings.cpp`
* `src/libs/cgalpy/lib/aos2_face_bindings.cpp`