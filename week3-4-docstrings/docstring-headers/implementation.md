# Docstring Header Generation — Full Technical Implementation

## Session Details

| Field | Value |
|---|---|
| Date | April 1, 2026, ~3 AM IST |
| Duration | ~3 hours |
| Repo | cgal-python-bindings (branch: `feature/named-params-operators-poc`) |
| Trigger | Continuation of v22.0 automation research (50/50 AOS2 POC) |
| Status | Headers generated — not yet wired into `.cpp` files |

---

## The Problem Being Solved

The existing binding files have docstrings either:

1. **Missing entirely** — most methods in pol2, as2, bso2, env2, vis2
2. **Inline in `.def()`** — long strings buried inside binding logic (AOS2 pattern)

Inline strings cause the "shadowing" problem Efi described:
> "After I added some docstrings, I felt that they screen or shadow the code itself."

The solution: move all docstrings to a `const char*` variable in a dedicated header file, then reference the variable name from `.def()`.

---

## Directory Created In The Official Repo

```
src/libs/cgalpy/lib/docstrings/
├── alpha_shape_2_docstrings.h              (1.5K)
├── boolean_set_operations_2_docstrings.h   (1.3K)
├── envelope_2_docstrings.h                 (2.0K)
├── polygon_2_docstrings.h                  (3.6K)
└── visibility_2_docstrings.h               (1.1K)
```

This directory is **new** — it did not exist in the repo before this session.

---

## Header File Structure (Universal Pattern)

Every header uses this exact structure:

```cpp
#pragma once

const char* METHOD_NAME_DOC = R"pbdoc(
One or two sentence description.
May include parameter context if the method takes non-obvious arguments.
)pbdoc";

const char* ANOTHER_METHOD_DOC = R"pbdoc(
...
)pbdoc";
```

---

## Naming Convention for Constants

| Python binding name | Constant name |
|---|---|
| `is_simple` | `IS_SIMPLE_DOC` |
| `orientation` | `ORIENTATION_DOC` |
| `__init__` | `__INIT___DOC` |
| `reverse_orientation` | `REVERSE_ORIENTATION_DOC` |
| `push_back` | `PUSH_BACK_DOC` |
| `get_nth_alpha` | `GET_NTH_ALPHA_DOC` |

Rule: `UPPERCASE_SNAKE_CASE` + `_DOC` suffix, matching the Python method name.

---

## Source of Each Docstring

Docstrings were written by cross-referencing:

- The binding `.cpp` file — to enumerate all `.def()` calls
- CGAL doc headers at `~/cgal/<Package>/doc/<Package>/CGAL/*.h`, using the three comment patterns identified in the March 25 session:

```
Pattern 1 (class method, single-line):
  /*! Returns true if the polygon is simple. */
  bool is_simple() const;

Pattern 2 (class method, multi-line):
  /*! Computes the orientation of the polygon.
   *  Returns CLOCKWISE, COUNTERCLOCKWISE, or COLLINEAR.
   */
  Orientation orientation() const;

Pattern 3 (free function, \ingroup):
  /*! \ingroup PkgPolygon2Functions
   *
   *  Computes the area of a polygon.
   */
  FT polygon_area(...);
```

- `doc.cgal.org` — for methods not in local doc headers (e.g., `draw()`)

---

## Per-File Breakdown

### `polygon_2_docstrings.h` — 3.6K, 22 constants

| Constant | Method | Source |
|---|---|---|
| `__INIT___DOC` | `__init__` | Manual |
| `IS_SIMPLE_DOC` | `is_simple` | CGAL Polygon.h |
| `IS_CONVEX_DOC` | `is_convex` | CGAL Polygon.h |
| `ORIENTATION_DOC` | `orientation` | CGAL Polygon.h |
| `ORIENTED_SIDE_DOC` | `oriented_side` | CGAL Polygon.h |
| `BOUNDED_SIDE_DOC` | `bounded_side` | CGAL Polygon.h |
| `BBOX_DOC` | `bbox` | CGAL Polygon.h |
| `AREA_DOC` | `area` | CGAL Polygon.h |
| `LEFT_VERTEX_DOC` | `left_vertex` | CGAL Polygon.h |
| `RIGHT_VERTEX_DOC` | `right_vertex` | CGAL Polygon.h |
| `TOP_VERTEX_DOC` | `top_vertex` | CGAL Polygon.h |
| `BOTTOM_VERTEX_DOC` | `bottom_vertex` | CGAL Polygon.h |
| `CONTAINER_DOC` | `container` | Manual |
| `SIZE_DOC` | `size` | Manual |
| `IS_EMPTY_DOC` | `is_empty` | Manual |
| `CLEAR_DOC` | `clear` | Manual |
| `PUSH_BACK_DOC` | `push_back` | CGAL Polygon.h |
| `VERTEX_DOC` | `vertex` | CGAL Polygon.h |
| `REVERSE_ORIENTATION_DOC` | `reverse_orientation` | CGAL Polygon.h |
| `EDGES_DOC` | `edges` | CGAL Polygon.h |
| `VERTICES_DOC` | `vertices` | CGAL Polygon.h |
| `DRAW_DOC` | `draw` | Manual (no CGAL doc entry) |

### `alpha_shape_2_docstrings.h` — 1.5K, 10 constants

| Constant | Method |
|---|---|
| `ALPHA_DOC` | `alpha` |
| `SET_ALPHA_DOC` | `set_alpha` |
| `ALPHA_COUNT_DOC` | `alpha_count` |
| `GET_NTH_ALPHA_DOC` | `get_nth_alpha` |
| `FIND_OPTIMAL_ALPHA_DOC` | `find_optimal_alpha` |
| `CLASSIFY_DOC` | `classify` |
| `NUMBER_OF_SOLID_COMPONENTS_DOC` | `number_of_solid_components` |
| `ALPHA_SHAPE_VERTICES_DOC` | `alpha_shape_vertices` |
| `ALPHA_SHAPE_EDGES_DOC` | `alpha_shape_edges` |
| `MAKE_ALPHA_SHAPE_DOC` | `make_alpha_shape` |

### `boolean_set_operations_2_docstrings.h` — 1.3K, 7 constants

| Constant | Method |
|---|---|
| `DO_INTERSECT_DOC` | `do_intersect` |
| `INTERSECTION_DOC` | `intersection` |
| `JOIN_DOC` | `join` |
| `DIFFERENCE_DOC` | `difference` |
| `SYMMETRIC_DIFFERENCE_DOC` | `symmetric_difference` |
| `COMPLEMENT_DOC` | `complement` |
| `IS_VALID_DOC` | `is_valid` |

### `envelope_2_docstrings.h` — 2.0K, 9 constants

| Constant | Method |
|---|---|
| `LOWER_ENVELOPE_X_MONOTONE_DOC` | `lower_envelope_x_monotone_2` |
| `UPPER_ENVELOPE_X_MONOTONE_DOC` | `upper_envelope_x_monotone_2` |
| `LOWER_ENVELOPE_DOC` | `lower_envelope_2` |
| `UPPER_ENVELOPE_DOC` | `upper_envelope_2` |
| `MINIMIZATION_DIAGRAM_DOC` | `Minimization_diagram_2` |
| `MAXIMIZATION_DIAGRAM_DOC` | `Maximization_diagram_2` |
| `DIAGRAM_VERTEX_DOC` | diagram vertex accessor |
| `DIAGRAM_EDGE_DOC` | diagram edge accessor |
| `DIAGRAM_FACE_DOC` | diagram face accessor |

### `visibility_2_docstrings.h` — 1.1K, 5 constants

| Constant | Method |
|---|---|
| `COMPUTE_VISIBILITY_DOC` | `compute_visibility` (interior) |
| `COMPUTE_VISIBILITY_HALFEDGE_DOC` | `compute_visibility` (halfedge) |
| `IS_ATTACHED_DOC` | `is_attached` |
| `ATTACH_DOC` | `attach` |
| `DETACH_DOC` | `detach` |

---

## What Changes In The Binding `.cpp` Files

Before (no docstring):

```cpp
.def("is_simple", &Polygon_2::is_simple)
```

After:

```cpp
.def("is_simple", &Polygon_2::is_simple, IS_SIMPLE_DOC)
```

Before (with `nb::arg`, no docstring):

```cpp
.def("vertex", &Polygon_2::vertex, nb::arg("i"))
```

After:

```cpp
.def("vertex", &Polygon_2::vertex, nb::arg("i"), VERTEX_DOC)
```

---

## Why NOT AOS2 In This Session

`arrangement_on_surface_2_bindings.cpp` already has 57 inline docstrings added in the March 13 + March 24 sessions. Migrating those to a header file is a separate refactoring task. The header-file approach was applied only to packages that had zero docstrings: pol2, as2, bso2, env2, vis2.

---

## Known Limitations

- **`draw()`** — no CGAL doc header entry; written manually
- **Overloaded functions** — all overloads share one DOC constant (first-match)
- **LaTeX markup** (`\f$...\f$`) stripped manually when writing constants
- **Backtick markup** (`` `c` ``) stripped manually

---

## Commit Plan (awaiting Email 23 from Efi)

```bash
git add src/libs/cgalpy/lib/docstrings/
git add src/libs/cgalpy/lib/polygon_2_bindings.cpp
git add src/libs/cgalpy/lib/alpha_shape_2_bindings.cpp
git add src/libs/cgalpy/lib/boolean_set_operations_2_bindings.cpp
git add src/libs/cgalpy/lib/envelope_2_bindings.cpp
git add src/libs/cgalpy/lib/visibility_2_bindings.cpp
git commit -m "docs: add docstring header files for pol2, as2, bso2, env2, vis2"
```