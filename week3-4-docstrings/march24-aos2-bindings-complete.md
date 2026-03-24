# March 24 — Docstrings for arrangement_on_surface_2_bindings.cpp

Date: March 24, 2026
File edited: `src/libs/cgalpy/lib/arrangement_on_surface_2_bindings.cpp`
Branch: `feature/named-params-operators-poc`
Base commit: `ebea4e79` (Feb 27 framework refactor)

Methods documented: 57 (25 class members + 32 free function overloads)
Lines added: +105 (file grew from 1345 to 1450 lines)
Build: clean, zero errors (Apple Clang 17, macOS M2)
Verification: 25/25 class methods confirmed, 9/9 free function names confirmed


---


## Why this file was saved for last

The three smaller binding files (vertex, halfedge, face) were done on March 13.
This file was the largest at 1345 lines and the most complex. It contains:
- Class method bindings for `Arrangement_on_surface_2`
- Class method bindings for `Arrangement_2` (subclass)
- Class method bindings for `Arrangement_with_history_2`
- Over 32 free function overloads (`insert`, `zone`, `decompose`, and so on)


---


## Key file facts discovered before editing

```cpp
// py:: is an alias for nanobind:: (line 94)
namespace py = nanobind;

// ri is defined at line 755 as:
constexpr auto ri(py::rv_policy::reference_internal);

// The class binding variable is aos_c (not aosc)
py::class_<Aos> aos_c(m, "Arrangement_on_surface_2");  // line 757

// Parameter naming uses py::arg() NOT nb::arg()
// (because py:: = nanobind::, so py::arg = nb::arg)
```

Placement pattern confirmed from `export_pol3_bgl.cpp`:
```cpp
// Docstring goes AFTER py::arg(...) calls, BEFORE ri or py::keep_alive
m.def("halfedges_around_target", &pol3::halfedges_around_target_v_iterator,
      py::arg("v"), py::arg("g"),
      "Obtain an iterator over all halfedges with vertex v as target",
      py::keep_alive<0, 1>());
```


---


## All code changes (before and after)

### 1. geometry_traits and topology_traits (lines 761-766)

Before:
```cpp
    .def("geometry_traits", &aos2::geometry_traits, ri)
    .def("topology_traits", &aos2::topology_traits, ri)
```

After:
```cpp
    .def("geometry_traits", &aos2::geometry_traits,
         "Obtains the geometry-traits object associated with the arrangement.",
         ri)
    .def("topology_traits", &aos2::topology_traits,
         "Obtains the topology-traits object associated with the arrangement.",
         ri)
```


### 2. fictitious_face (inside preprocessor guard, lines 770-772)

Before:
```cpp
    .def("fictitious_face", &aos2::fictitious_face, ri)
```

After:
```cpp
    .def("fictitious_face", &aos2::fictitious_face,
         "Obtains a handle to the fictitious face of the arrangement.",
         ri)
```

This remains inside the `#if ((CGALPY_AOS2_GEOMETRY_TRAITS == ...))` guard. The preprocessor block was not modified.


### 3. insert_from_left_vertex, two overloads (lines 774-784)

Before:
```cpp
    .def("insert_from_left_vertex", &aos2::insert_from_left_vertex1,
         py::arg("xcv"), py::arg("v"), ri)
    .def("insert_from_left_vertex", &aos2::insert_from_left_vertex2,
         py::arg("xcv"), py::arg("h"), ri)
```

After:
```cpp
    .def("insert_from_left_vertex", &aos2::insert_from_left_vertex1,
         py::arg("xcv"), py::arg("v"),
         "Inserts the curve xcv into the arrangement, such that its left endpoint "
         "corresponds to a given arrangement vertex.",
         ri)
    .def("insert_from_left_vertex", &aos2::insert_from_left_vertex2,
         py::arg("xcv"), py::arg("h"),
         "Inserts the curve xcv into the arrangement, such that its left endpoint "
         "corresponds to a given arrangement vertex. The given halfedge h is the "
         "predecessor halfedge in the circular list of halfedges around the vertex.",
         ri)
```

The first overload takes a `Vertex_handle`, the second takes a `Halfedge_handle` (predecessor).


### 4. insert_from_right_vertex, two overloads (lines 785-795)

Before:
```cpp
    .def("insert_from_right_vertex", &aos2::insert_from_right_vertex1,
         py::arg("xcv"), py::arg("v"), ri)
    .def("insert_from_right_vertex", &aos2::insert_from_right_vertex2,
         py::arg("xcv"), py::arg("h"), ri)
```

After:
```cpp
    .def("insert_from_right_vertex", &aos2::insert_from_right_vertex1,
         py::arg("xcv"), py::arg("v"),
         "Inserts the curve xcv into the arrangement, such that its right endpoint "
         "corresponds to a given arrangement vertex.",
         ri)
    .def("insert_from_right_vertex", &aos2::insert_from_right_vertex2,
         py::arg("xcv"), py::arg("h"),
         "Inserts the curve xcv into the arrangement, such that its right endpoint "
         "corresponds to a given arrangement vertex. The given halfedge h is the "
         "predecessor halfedge in the circular list of halfedges around the vertex.",
         ri)
```


### 5. insert_in_face_interior, two overloads (lines 796-806)

Before:
```cpp
    .def("insert_in_face_interior", &aos2::insert_xcv_in_face_interior,
         py::arg("xcv"), py::arg("f"), ri)
    .def("insert_in_face_interior", &aos2::insert_pnt_in_face_interior,
         py::arg("p"), py::arg("f"), ri)
```

After:
```cpp
    .def("insert_in_face_interior", &aos2::insert_xcv_in_face_interior,
         py::arg("xcv"), py::arg("f"),
         "Inserts the curve xcv, which lies entirely in the interior of the face f, "
         "into the arrangement. Returns a halfedge directed from the vertex "
         "corresponding to the left endpoint of xcv toward its right endpoint.",
         ri)
    .def("insert_in_face_interior", &aos2::insert_pnt_in_face_interior,
         py::arg("p"), py::arg("f"),
         "Inserts the point p into the arrangement as an isolated vertex in the "
         "interior of the face f and returns a handle for the newly created vertex.",
         ri)
```


### 6. insert_at_vertices, three overloads (lines 807-822)

Before:
```cpp
    .def("insert_at_vertices", &aos2::insert_at_vertices1,
         py::arg("xcv"), py::arg("v1"), py::arg("v2"), ri)
    .def("insert_at_vertices", &aos2::insert_at_vertices3,
         py::arg("xcv"), py::arg("h1"), py::arg("v2"), ri)
    .def("insert_at_vertices", &aos2::insert_at_vertices4,
         py::arg("xcv"), py::arg("h1"), py::arg("h2"), ri)
```

After:
```cpp
    .def("insert_at_vertices", &aos2::insert_at_vertices1,
         py::arg("xcv"), py::arg("v1"), py::arg("v2"),
         "Inserts the curve xcv into the arrangement, such that both its endpoints "
         "correspond to existing arrangement vertices given by v1 and v2.",
         ri)
    .def("insert_at_vertices", &aos2::insert_at_vertices3,
         py::arg("xcv"), py::arg("h1"), py::arg("v2"),
         "Inserts the curve xcv into the arrangement, such that both its endpoints "
         "correspond to existing arrangement vertices given by h1->target() and v2.",
         ri)
    .def("insert_at_vertices", &aos2::insert_at_vertices4,
         py::arg("xcv"), py::arg("h1"), py::arg("h2"),
         "Inserts the curve xcv into the arrangement, such that both its endpoints "
         "correspond to existing arrangement vertices given by h1->target() and "
         "h2->target().",
         ri)
```

Note: `insert_at_vertices2` is commented out in the original file and was left untouched.


### 7. modify_vertex, remove_isolated_vertex, modify_edge, split_edge, merge_edge, remove_edge (lines 823-850)

Before:
```cpp
    .def("modify_vertex", &aos2::modify_vertex,
         py::arg("v"), py::arg("p"), ri)
    .def("remove_isolated_vertex", &aos2::remove_isolated_vertex,
         py::arg("v"), ri)
    .def("modify_edge", &aos2::modify_edge,
         py::arg("e"), py::arg("xcv"), ri)
    .def("split_edge", &aos2::split_edge,
         py::arg("e"), py::arg("c1"), py::arg("c2"), ri)
    .def("merge_edge", &aos2::merge_edge,
         py::arg("e1"), py::arg("e2"), py::arg("xcv"), ri)
    .def("remove_edge", &aos2::remove_edge,
         py::arg("e"), ri)
```

After:
```cpp
    .def("modify_vertex", &aos2::modify_vertex,
         py::arg("v"), py::arg("p"),
         "Modifies the point associated with the vertex v.",
         ri)
    .def("remove_isolated_vertex", &aos2::remove_isolated_vertex,
         py::arg("v"),
         "Removes an isolated vertex v from the arrangement.",
         ri)
    .def("modify_edge", &aos2::modify_edge,
         py::arg("e"), py::arg("xcv"),
         "Modifies the x-monotone curve associated with the edge e.",
         ri)
    .def("split_edge", &aos2::split_edge,
         py::arg("e"), py::arg("c1"), py::arg("c2"),
         "Splits the edge e into two at the curves c1 and c2. Returns a handle for "
         "the halfedge directed from the source of e toward the new split vertex.",
         ri)
    .def("merge_edge", &aos2::merge_edge,
         py::arg("e1"), py::arg("e2"), py::arg("xcv"),
         "Merges the edges represented by e1 and e2 into a single edge associated "
         "with the merged curve xcv.",
         ri)
    .def("remove_edge", &aos2::remove_edge,
         py::arg("e"),
         "Removes the edge e from the arrangement.",
         ri)
```


### 8. Simple query methods: is_empty, is_valid, number_of_*, assign, clear

Before:
```cpp
    .def("is_empty", &Aos::is_empty)
    .def("is_valid", &Aos::is_valid)
    .def("number_of_edges", &Aos::number_of_edges)
    .def("number_of_faces", &Aos::number_of_faces)
    .def("number_of_halfedges", &Aos::number_of_halfedges)
    .def("number_of_isolated_vertices", &Aos::number_of_isolated_vertices)
    .def("number_of_unbounded_faces", &Aos::number_of_unbounded_faces)
    .def("number_of_vertices", &Aos::number_of_vertices)
    .def("assign", &Aos::assign)
    .def("clear", &Aos::clear)
```

After:
```cpp
    .def("is_empty", &Aos::is_empty,
         "Determines whether the arrangement is empty (contains only the unbounded "
         "face, with no vertices or edges).")
    .def("is_valid", &Aos::is_valid,
         "Determines whether the arrangement is valid.")
    .def("number_of_edges", &Aos::number_of_edges,
         "Obtains the number of edges in the arrangement.")
    .def("number_of_faces", &Aos::number_of_faces,
         "Obtains the number of faces in the arrangement.")
    .def("number_of_halfedges", &Aos::number_of_halfedges,
         "Obtains the number of halfedges in the arrangement.")
    .def("number_of_isolated_vertices", &Aos::number_of_isolated_vertices,
         "Obtains the total number of isolated vertices in the arrangement.")
    .def("number_of_unbounded_faces", &Aos::number_of_unbounded_faces,
         "Obtains the number of unbounded faces in the arrangement.")
    .def("number_of_vertices", &Aos::number_of_vertices,
         "Obtains the number of vertices in the arrangement.")
    .def("assign", &Aos::assign,
         "Assigns the contents of another arrangement.")
    .def("clear", &Aos::clear,
         "Clears the arrangement.")
```


### 9. Iterator methods: vertices, halfedges, edges, faces, unbounded_faces

Before:
```cpp
  aos_c.def("vertices", &aos2::vertices, py::keep_alive<0, 1>())
    .def("halfedges", &aos2::halfedges, py::keep_alive<0, 1>())
    .def("edges", &aos2::edges, py::keep_alive<0, 1>())
    .def("faces", &aos2::faces, py::keep_alive<0, 1>())
    .def("unbounded_faces", &aos2::unbounded_faces, py::keep_alive<0, 1>());
```

After:
```cpp
  aos_c.def("vertices", &aos2::vertices,
         "Obtains a range over handles of the arrangement vertices.",
         py::keep_alive<0, 1>())
    .def("halfedges", &aos2::halfedges,
         "Obtains a range over handles of the arrangement halfedges.",
         py::keep_alive<0, 1>())
    .def("edges", &aos2::edges,
         "Obtains a range over handles of the arrangement edges.",
         py::keep_alive<0, 1>())
    .def("faces", &aos2::faces,
         "Obtains a range over handles of the arrangement faces.",
         py::keep_alive<0, 1>())
    .def("unbounded_faces", &aos2::unbounded_faces,
         "Obtains a range over handles of the unbounded faces of the arrangement.",
         py::keep_alive<0, 1>());
```


### 10. Free functions: insert_point (4 overloads)

Before:
```cpp
  m.def("insert_point", &aos2::insert_point)
    .def("insert_point", &aos2::insert_point_pl<Naive_pl>)
    .def("insert_point", &aos2::insert_point_pl<Wal_pl>)
    .def("insert_point", &aos2::insert_point_pl<Trapezoid_pl>)
    ;
```

After:
```cpp
  m.def("insert_point", &aos2::insert_point,
         "Inserts the point p into the arrangement and returns a handle for the "
         "vertex associated with it.")
    .def("insert_point", &aos2::insert_point_pl<Naive_pl>,
         "Inserts the point p into the arrangement using a naive point-location "
         "strategy.")
    .def("insert_point", &aos2::insert_point_pl<Wal_pl>,
         "Inserts the point p into the arrangement using a walk-along-line "
         "point-location strategy.")
    .def("insert_point", &aos2::insert_point_pl<Trapezoid_pl>,
         "Inserts the point p into the arrangement using a trapezoidal "
         "point-location strategy.")
    ;
```


### 11. Free functions: insert_non_intersecting_curve / _curves (4 overloads)

Before:
```cpp
  m.def("insert_non_intersecting_curve", &aos2::insert_ni_cv)
    .def("insert_non_intersecting_curve", &aos2::insert_ni_xcv_pl<Aos, Naive_pl>)
    .def("insert_non_intersecting_curve", &aos2::insert_ni_xcv_pl<Aos, Wal_pl>)
    .def("insert_non_intersecting_curve", &aos2::insert_ni_xcv_pl<Aos, Trapezoid_pl>)
    .def("insert_non_intersecting_curves", &aos2::insert_ni_cvs)
    ;
```

After:
```cpp
  m.def("insert_non_intersecting_curve", &aos2::insert_ni_cv,
         "Inserts the given x-monotone curve into the arrangement, which is "
         "assumed to be interior-disjoint from all existing arrangement edges.")
    .def("insert_non_intersecting_curve", &aos2::insert_ni_xcv_pl<Aos, Naive_pl>,
         "Inserts the given x-monotone curve into the arrangement using a naive "
         "point-location strategy.")
    .def("insert_non_intersecting_curve", &aos2::insert_ni_xcv_pl<Aos, Wal_pl>,
         "Inserts the given x-monotone curve into the arrangement using a "
         "walk-along-line point-location strategy.")
    .def("insert_non_intersecting_curve", &aos2::insert_ni_xcv_pl<Aos, Trapezoid_pl>,
         "Inserts the given x-monotone curve into the arrangement using a "
         "trapezoidal point-location strategy.")
    .def("insert_non_intersecting_curves", &aos2::insert_ni_cvs,
         "Inserts a range of x-monotone curves into the arrangement, all assumed "
         "to be pairwise interior-disjoint.")
    ;
```


### 12. Free functions: insert (11 overloads)

Before:
```cpp
  m.def("insert", &aos2::insert_cv<Aos>)
    .def("insert", &aos2::insert_cv_pl<Aos, Naive_pl>)
    .def("insert", &aos2::insert_cv_pl<Aos, Wal_pl>)
    .def("insert", &aos2::insert_cv_pl<Aos, Trapezoid_pl>)
    .def("insert", &aos2::insert_xcv<Aos>)
    .def("insert", &aos2::insert_xcv_pl<Aos, Naive_pl>)
    .def("insert", &aos2::insert_xcv_pl<Aos, Wal_pl>)
    .def("insert", &aos2::insert_xcv_pl<Aos, Trapezoid_pl>)
    .def("insert", &aos2::insert_xcv_vertex<Aos>)
    .def("insert", &aos2::insert_xcv_halfedge<Aos>)
    .def("insert", &aos2::insert_xcv_face<Aos>)
    .def("insert", &aos2::insert_curves)
    ;
```

After:
```cpp
  m.def("insert", &aos2::insert_cv<Aos>,
         "Inserts the given curve into the arrangement, possibly splitting it into "
         "x-monotone subcurves.")
    .def("insert", &aos2::insert_cv_pl<Aos, Naive_pl>,
         "Inserts the given curve into the arrangement using a naive "
         "point-location strategy.")
    .def("insert", &aos2::insert_cv_pl<Aos, Wal_pl>,
         "Inserts the given curve into the arrangement using a walk-along-line "
         "point-location strategy.")
    .def("insert", &aos2::insert_cv_pl<Aos, Trapezoid_pl>,
         "Inserts the given curve into the arrangement using a trapezoidal "
         "point-location strategy.")
    .def("insert", &aos2::insert_xcv<Aos>,
         "Inserts the given x-monotone curve into the arrangement.")
    .def("insert", &aos2::insert_xcv_pl<Aos, Naive_pl>,
         "Inserts the given x-monotone curve into the arrangement using a naive "
         "point-location strategy.")
    .def("insert", &aos2::insert_xcv_pl<Aos, Wal_pl>,
         "Inserts the given x-monotone curve into the arrangement using a "
         "walk-along-line point-location strategy.")
    .def("insert", &aos2::insert_xcv_pl<Aos, Trapezoid_pl>,
         "Inserts the given x-monotone curve into the arrangement using a "
         "trapezoidal point-location strategy.")
    .def("insert", &aos2::insert_xcv_vertex<Aos>,
         "Inserts the given x-monotone curve into the arrangement, where one of its "
         "endpoints is associated with a given arrangement vertex.")
    .def("insert", &aos2::insert_xcv_halfedge<Aos>,
         "Inserts the given x-monotone curve into the arrangement, where one of its "
         "endpoints is associated with a given arrangement halfedge.")
    .def("insert", &aos2::insert_xcv_face<Aos>,
         "Inserts the given x-monotone curve into the arrangement, where one of its "
         "endpoints lies inside a given arrangement face.")
    .def("insert", &aos2::insert_curves,
         "Inserts a range of curves into the arrangement.")
    ;
```


### 13. Free functions: do_intersect (4 overloads)

Before:
```cpp
  m.def("do_intersect", static_cast<Do_intersect>(CGAL::do_intersect))
    .def("do_intersect", static_cast<Do_intersect_nv_pl>(CGAL::do_intersect))
    .def("do_intersect", static_cast<Do_intersect_wl_pl>(CGAL::do_intersect))
    .def("do_intersect", static_cast<Do_intersect_tr_pl>(CGAL::do_intersect))
    ;
```

After:
```cpp
  m.def("do_intersect", static_cast<Do_intersect>(CGAL::do_intersect),
         "Returns true if the given x-monotone curve intersects any of the edges "
         "of the arrangement.")
    .def("do_intersect", static_cast<Do_intersect_nv_pl>(CGAL::do_intersect),
         "Returns true if the given x-monotone curve intersects any of the edges "
         "of the arrangement, using a naive point-location strategy.")
    .def("do_intersect", static_cast<Do_intersect_wl_pl>(CGAL::do_intersect),
         "Returns true if the given x-monotone curve intersects any of the edges "
         "of the arrangement, using a walk-along-line point-location strategy.")
    .def("do_intersect", static_cast<Do_intersect_tr_pl>(CGAL::do_intersect),
         "Returns true if the given x-monotone curve intersects any of the edges "
         "of the arrangement, using a trapezoidal point-location strategy.")
    ;
```


### 14. decompose, zone, remove_edge (free), remove_vertex (free)

Before:
```cpp
  m.def("decompose", &aos2::decompose, ri, py::keep_alive<1, 0>());

  m.def("zone", &aos2::zone)
    .def("zone", &aos2::zone_pl<Naive_pl>)
    .def("zone", &aos2::zone_pl<Wal_pl>)
    .def("zone", &aos2::zone_pl<Trapezoid_pl>)

  m.def("remove_edge", &aos2::remove_edge_free);
  m.def("remove_vertex", &aos2::remove_vertex_free);
```

After:
```cpp
  m.def("decompose", &aos2::decompose,
         "Computes the vertical decomposition of the arrangement by adding vertical "
         "walls to the arrangement.",
         ri, py::keep_alive<1, 0>());

  m.def("zone", &aos2::zone,
         "Computes the zone of an x-monotone curve in the arrangement.")
    .def("zone", &aos2::zone_pl<Naive_pl>,
         "Computes the zone of an x-monotone curve in the arrangement using a "
         "naive point-location strategy.")
    .def("zone", &aos2::zone_pl<Wal_pl>,
         "Computes the zone of an x-monotone curve in the arrangement using a "
         "walk-along-line point-location strategy.")
    .def("zone", &aos2::zone_pl<Trapezoid_pl>,
         "Computes the zone of an x-monotone curve in the arrangement using a "
         "trapezoidal point-location strategy.")

  m.def("remove_edge", &aos2::remove_edge_free,
         "Removes the given edge from the arrangement.");
  m.def("remove_vertex", &aos2::remove_vertex_free,
         "Removes the given vertex from the arrangement.");
```


---


## How the patch was applied

The first attempt with plain `str.replace()` failed because `\n` in the Python string didn't match actual newlines in the file. Switched to `re.subn()` with `\s+` to handle whitespace flexibly. All 32 replacements applied cleanly in one run.

```python
pattern = r'(\.def\("insert_from_left_vertex",\s*&aos2::insert_from_left_vertex1,\s*py::arg\("xcv"\),\s*py::arg\("v"\)),\s*ri\)'
replacement = r'\1,\n         "Inserts the curve xcv...",\n         ri)'
new_content, count = re.subn(pattern, replacement, content, count=1)
```


---


## Build output

```
[ 59%] Building CXX object src/libs/cgalpy/CMakeFiles/CGALPY.dir/lib/arrangement_on_surface_2_bindings.cpp.o
[ 61%] Linking CXX shared module CGALPY.cpython-312-darwin.so
[100%] Built target CGALPY
```


---


## Verification output

```
OK number_of_vertices          number_of_vertices(self) -> int
OK number_of_edges             number_of_edges(self) -> int
OK number_of_faces             number_of_faces(self) -> int
OK number_of_halfedges         number_of_halfedges(self) -> int
OK number_of_isolated_vertices number_of_isolated_vertices(self) -> int
OK number_of_unbounded_faces   number_of_unbounded_faces(self) -> int
OK is_empty                    is_empty(self) -> bool
OK is_valid                    is_valid(self) -> bool
OK assign                      assign(self, arg: ...) -> None
OK clear                       clear(self) -> None
OK vertices                    vertices(self) -> object
OK halfedges                   halfedges(self) -> object
OK edges                       edges(self) -> object
OK faces                       faces(self) -> object
OK unbounded_faces             unbounded_faces(self) -> object
OK insert_from_left_vertex     insert_from_left_vertex(self, xcv: ...)
OK insert_from_right_vertex    insert_from_right_vertex(self, xcv: ...)
OK insert_in_face_interior     insert_in_face_interior(self, xcv: ...)
OK insert_at_vertices          insert_at_vertices(self, xcv: ...)
OK modify_vertex               modify_vertex(self, v: ...)
OK modify_edge                 modify_edge(self, e: ...)
OK split_edge                  split_edge(self, e: ...)
OK merge_edge                  merge_edge(self, e1: ...)
OK remove_edge                 remove_edge(self, e: ...)
OK remove_isolated_vertex      remove_isolated_vertex(self, v: ...)

25/25 methods have docstrings

Free functions:
OK insert_point                     Inserts the point p into the arrangement...
OK insert_non_intersecting_curve    Inserts the given x-monotone curve...
OK insert_non_intersecting_curves   Inserts a range of x-monotone curves...
OK insert                           Inserts the given curve...
OK do_intersect                     Returns true if the given x-monotone curve...
OK decompose                        Computes the vertical decomposition...
OK zone                             Computes the zone of an x-monotone curve...
OK remove_edge                      Removes the given edge from the arrangement.
OK remove_vertex                    Removes the given vertex from the arrangement.
```


---


## What was not changed

- `Arrangement_with_history_2` methods -- inside `#ifdef CGALPY_AOS2_WITH_HISTORY`, cannot build without the WITHHISTORY config (pending Efi reply to Q1)
- Observer callback methods -- out of scope for this task