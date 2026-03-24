# March 13 — Docstrings for Vertex, Halfedge, and Face Bindings

Date: March 13, 2026

Files edited:
- `src/libs/cgalpy/lib/arr_vertex_bindings.cpp`
- `src/libs/cgalpy/lib/arr_halfedge_bindings.cpp`
- `src/libs/cgalpy/lib/arr_face_bindings.cpp`

Methods documented: 51 total (13 + 14 + 24)
Build result: clean, zero errors


---


## Docstring placement pattern

Confirmed by studying `export_pol3_bgl.cpp`, `export_tri2.cpp`, and `export_tri3.cpp`.

```cpp
// The docstring goes after py::arg() calls, before ri or py::keep_alive.

.def("method_name", &Class::fn,
     py::arg("x"),
     "Docstring text here.",
     ri)

// For iterators (no ri, uses keep_alive instead):
.def("incident_halfedges", &vtx::incident_halfedges,
     "Docstring here.",
     py::keep_alive<0, 1>())

// For simple methods (no args, no lifetime management):
.def("is_isolated", &Vertex::is_isolated,
     "Docstring here.")
```

A few things worth noting:
- `py::` is an alias for `nanobind::` (set via `namespace py = nanobind;` at line 94 of the aos2 bindings)
- Only inline string literals are used for docstrings — no `R"(...)"`, no external header files
- `ri` is a shorthand: `constexpr auto ri(py::rv_policy::reference_internal);`


---


## arr_vertex_bindings.cpp

13 methods documented:

```cpp
.def("point", &Vertex::point,
     "Obtains the geometric point associated with this vertex.", ri)

.def("degree", &Vertex::degree,
     "Obtains the number of edges incident to this vertex.")

.def("is_isolated", &Vertex::is_isolated,
     "Determines whether this vertex is isolated (has no incident edges).")

.def("incident_halfedges", &vtx::incident_halfedges,
     "Obtains a circulator over the halfedges incident to this vertex.",
     py::keep_alive<0, 1>())

.def("data", &Vertex::data,
     "Obtains a reference to the data object associated with this vertex.", ri)

.def("set_data", &Vertex::set_data, py::arg("data"),
     "Sets the data object associated with this vertex.")

.def("is_at_open_boundary", &Vertex::is_at_open_boundary,
     "Determines whether this vertex lies on an open boundary of the parameter space.")

.def("parameter_space_in_x", &Vertex::parameter_space_in_x,
     "Returns the placement of the vertex in the x-direction "
     "(interior, left boundary, or right boundary).")

.def("parameter_space_in_y", &Vertex::parameter_space_in_y,
     "Returns the placement of the vertex in the y-direction "
     "(interior, bottom boundary, or top boundary).")
```


---


## arr_halfedge_bindings.cpp

14 methods documented:

```cpp
.def("curve", &Halfedge::curve,
     "Obtains the x-monotone curve associated with this halfedge.", ri)

.def("source", &Halfedge::source,
     "Obtains a handle to the source vertex of this halfedge.", ri)

.def("target", &Halfedge::target,
     "Obtains a handle to the target vertex of this halfedge.", ri)

.def("twin", &Halfedge::twin,
     "Obtains a handle to the twin halfedge (same edge, opposite direction).", ri)

.def("next", &Halfedge::next,
     "Obtains a handle to the next halfedge in the connected component of the boundary.", ri)

.def("prev", &Halfedge::prev,
     "Obtains a handle to the previous halfedge in the connected component of the boundary.", ri)

.def("face", &Halfedge::face,
     "Obtains a handle to the face to the left of this halfedge.", ri)

.def("direction", &Halfedge::direction,
     "Obtains the direction of this halfedge (ARR_LEFT_TO_RIGHT or ARR_RIGHT_TO_LEFT).")

.def("data", &Halfedge::data,
     "Obtains a reference to the data object associated with this halfedge.", ri)

.def("set_data", &Halfedge::set_data, py::arg("data"),
     "Sets the data object associated with this halfedge.")

// Envelope methods (inside #ifdef CGALPY_AOS2_WITH_ENVELOPE):
.def("set_decision", &Halfedge::set_decision, py::arg("cr"),
     "Sets the decision attribute for this halfedge (envelope computation).")

.def("set_env_data", &Halfedge::set_env_data, py::arg("data"),
     "Sets the envelope data for this halfedge.")

.def("add_env_data", &Halfedge::add_env_data, py::arg("data"),
     "Adds to the envelope data for this halfedge.")
```


---


## arr_face_bindings.cpp

### Face_base methods (8):

```cpp
.def("is_unbounded", &Face_base::is_unbounded,
     "Determines whether this face is unbounded.")

.def("outer_ccb", &fb::outer_ccb,
     "Obtains a circulator over the halfedges forming the outer boundary of this face.",
     py::keep_alive<0, 1>())

.def("number_of_outer_ccbs", &Face_base::number_of_outer_ccbs,
     "Obtains the number of outer connected components of this face's boundary.")

.def("holes", &fb::holes,
     "Obtains a range over circulators of the holes (inner connected components) of this face.",
     py::keep_alive<0, 1>())

.def("number_of_holes", &Face_base::number_of_holes,
     "Obtains the number of holes (inner connected components) of this face.")

.def("isolated_vertices", &fb::isolated_vertices,
     "Obtains a range over handles of the isolated vertices in this face.",
     py::keep_alive<0, 1>())

.def("number_of_isolated_vertices", &Face_base::number_of_isolated_vertices,
     "Obtains the number of isolated vertices in this face.")
```

### Face methods (16 including envelope):

```cpp
.def("data", &Face::data,
     "Obtains a reference to the data object associated with this face.", ri)

.def("set_data", &Face::set_data, py::arg("data"),
     "Sets the data object associated with this face.")

.def("assign", &Face::assign, py::arg("f"),
     "Assigns all attributes of another face to this face.")

// Envelope methods (inside #ifdef CGALPY_AOS2_WITH_ENVELOPE):
.def("set_is_env_set", &Face::set_is_env_set, py::arg("b"),
     "Sets whether the envelope data for this face has been computed.")

.def("set_decision", &Face::set_decision, py::arg("cr"),
     "Sets the decision attribute for this face (envelope computation).")

.def("set_decision", &Face::set_decision2, py::arg("d"),
     "Sets the decision attribute using a Decision enum value.")

.def("set_env_data", &Face::set_env_data, py::arg("data"),
     "Sets the envelope data for this face.")

.def("add_env_data", &Face::add_env_data, py::arg("data"),
     "Adds to the envelope data for this face.")
```


---


## Build and verification

```
make CGALPY -j4   # Clean, 0 errors
```

Quick sanity check in the Python REPL:

```python
import CGALPY as cgalpy
arr = cgalpy.Aos2.Arrangement_2()
v = arr.insert_in_face_interior(
    cgalpy.Ker.Point_2(0, 0),
    list(arr.faces())
)
print(v.point())          # Point_2(0, 0)
print(v.is_isolated())    # True
print(v.degree())         # 0
print(v.point.__doc__)    # 'Obtains the geometric point associated with this vertex.'
```

Build output:

```
[ 59%] Building CXX object .../arrangement_on_surface_2_bindings.cpp.o
[ 61%] Linking CXX shared module CGALPY.cpython-312-darwin.so
[100%] Built target CGALPY
```

Incremental build only — the changed file recompiled in about 30 seconds.

Verification result: 25/25 class methods have docstrings, 9/9 free function names verified.

Sample confirmed output:

```
is_empty      -> "Determines whether the arrangement is empty (contains only the
                  unbounded face, with no vertices or edges)."
vertices      -> "Obtains a range over handles of the arrangement vertices."
remove_edge   -> "Removes the edge e from the arrangement."
```


---


## Cumulative state after March 24

| File                                     | Methods documented | Date     |
|------------------------------------------|--------------------|----------|
| `arr_vertex_bindings.cpp`                | 13                 | March 13 |
| `arr_halfedge_bindings.cpp`              | 14                 | March 13 |
| `arr_face_bindings.cpp`                  | 24                 | March 13 |
| `arrangement_on_surface_2_bindings.cpp`  | 57                 | March 24 |
| **Total**                                | **108**            |          |

Total diff ready for Bitbucket: +492 insertions across 5 files.
Latest Bitbucket commit: `ebea4e79` (Feb 27). Changes not yet pushed upstream — waiting on Efi's replies to Q1 and Q3.