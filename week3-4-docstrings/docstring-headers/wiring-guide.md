# Wiring Guide — How To Include Docstring Headers In Binding Files

## Overview

The header files in `src/libs/cgalpy/lib/docstrings/` are generated but not yet included in the binding `.cpp` files. This guide walks through every step, in order.

---

## Step 0 — Verify a Clean Build First

Before touching anything, confirm the build is in a working state:

```bash
cd cgal-python-bindings/build-manual
make CGALPY -j4
python3 -c "import CGALPY; print('OK')"
```

---

## Step 1 — Add `#include` To Each Binding File

Add one line after the last existing `#include` in each file:

```cpp
// polygon_2_bindings.cpp
#include "docstrings/polygon_2_docstrings.h"

// alpha_shape_2_bindings.cpp
#include "docstrings/alpha_shape_2_docstrings.h"

// boolean_set_operations_2_bindings.cpp
#include "docstrings/boolean_set_operations_2_docstrings.h"

// envelope_2_bindings.cpp
#include "docstrings/envelope_2_docstrings.h"

// visibility_2_bindings.cpp
#include "docstrings/visibility_2_docstrings.h"
```

The relative path `"docstrings/..."` works because both the `.cpp` files and the `docstrings/` folder live under `src/libs/cgalpy/lib/`.

---

## Step 2 — Update `.def()` Calls

Find all `.def()` calls in each file and append the matching DOC constant as the last argument:

```bash
grep -n '.def(' src/libs/cgalpy/lib/polygon_2_bindings.cpp
```

### `polygon_2` — Full Mapping

| Method | Constant |
|---|---|
| `__init__` | `__INIT___DOC` |
| `is_simple` | `IS_SIMPLE_DOC` |
| `is_convex` | `IS_CONVEX_DOC` |
| `orientation` | `ORIENTATION_DOC` |
| `oriented_side` | `ORIENTED_SIDE_DOC` |
| `bounded_side` | `BOUNDED_SIDE_DOC` |
| `bbox` | `BBOX_DOC` |
| `area` | `AREA_DOC` |
| `left_vertex` | `LEFT_VERTEX_DOC` |
| `right_vertex` | `RIGHT_VERTEX_DOC` |
| `top_vertex` | `TOP_VERTEX_DOC` |
| `bottom_vertex` | `BOTTOM_VERTEX_DOC` |
| `container` | `CONTAINER_DOC` |
| `size` | `SIZE_DOC` |
| `is_empty` | `IS_EMPTY_DOC` |
| `clear` | `CLEAR_DOC` |
| `push_back` | `PUSH_BACK_DOC` |
| `vertex` | `VERTEX_DOC` |
| `reverse_orientation` | `REVERSE_ORIENTATION_DOC` |
| `edges` | `EDGES_DOC` |
| `vertices` | `VERTICES_DOC` |
| `draw` | `DRAW_DOC` |

### `alpha_shape_2` — Mapping

| Method | Constant |
|---|---|
| `alpha` | `ALPHA_DOC` |
| `set_alpha` | `SET_ALPHA_DOC` |
| `alpha_count` | `ALPHA_COUNT_DOC` |
| `get_nth_alpha` | `GET_NTH_ALPHA_DOC` |
| `find_optimal_alpha` | `FIND_OPTIMAL_ALPHA_DOC` |
| `classify` | `CLASSIFY_DOC` |
| `number_of_solid_components` | `NUMBER_OF_SOLID_COMPONENTS_DOC` |
| `alpha_shape_vertices` | `ALPHA_SHAPE_VERTICES_DOC` |
| `alpha_shape_edges` | `ALPHA_SHAPE_EDGES_DOC` |
| `make_alpha_shape` | `MAKE_ALPHA_SHAPE_DOC` |

### `boolean_set_operations_2` — Mapping

| Method | Constant |
|---|---|
| `do_intersect` | `DO_INTERSECT_DOC` |
| `intersection` | `INTERSECTION_DOC` |
| `join` | `JOIN_DOC` |
| `difference` | `DIFFERENCE_DOC` |
| `symmetric_difference` | `SYMMETRIC_DIFFERENCE_DOC` |
| `complement` | `COMPLEMENT_DOC` |
| `is_valid` | `IS_VALID_DOC` |

### `envelope_2` — Mapping

| Method | Constant |
|---|---|
| `lower_envelope_x_monotone_2` | `LOWER_ENVELOPE_X_MONOTONE_DOC` |
| `upper_envelope_x_monotone_2` | `UPPER_ENVELOPE_X_MONOTONE_DOC` |
| `lower_envelope_2` | `LOWER_ENVELOPE_DOC` |
| `upper_envelope_2` | `UPPER_ENVELOPE_DOC` |
| `Minimization_diagram_2` | `MINIMIZATION_DIAGRAM_DOC` |
| `Maximization_diagram_2` | `MAXIMIZATION_DIAGRAM_DOC` |
| diagram vertex | `DIAGRAM_VERTEX_DOC` |
| diagram edge | `DIAGRAM_EDGE_DOC` |
| diagram face | `DIAGRAM_FACE_DOC` |

### `visibility_2` — Mapping

| Method | Constant |
|---|---|
| `compute_visibility` (interior) | `COMPUTE_VISIBILITY_DOC` |
| `compute_visibility` (halfedge) | `COMPUTE_VISIBILITY_HALFEDGE_DOC` |
| `is_attached` | `IS_ATTACHED_DOC` |
| `attach` | `ATTACH_DOC` |
| `detach` | `DETACH_DOC` |

---

## Step 3 — Build After Each File

Build after wiring each individual file — don't batch them.

```bash
make CGALPY -j4
# Must be 0 errors before moving to the next file
```

---

## Step 4 — Verify Docstrings Appear In Python

```bash
export PYTHONPATH=build-manual/src/libs/cgalpy
python3 -c "import CGALPY; print(CGALPY.Pol2.Polygon_2.is_simple.__doc__)"
python3 -c "import CGALPY; print(CGALPY.Pol2.Polygon_2.orientation.__doc__)"
python3 -c "import CGALPY; help(CGALPY.As2)"
python3 -c "import CGALPY; help(CGALPY.Bso2)"
python3 -c "import CGALPY; help(CGALPY.Env2)"
python3 -c "import CGALPY; help(CGALPY.Vis2)"
```

---

## Step 5 — Regression Test

```bash
python3 tests/aos2.py
# Expected: Number of faces: 3, Number of halfedges: 12, Number of vertices: 5
```

---

## Step 6 — Commit (After Email 23 From Efi)

```bash
git add src/libs/cgalpy/lib/docstrings/
git add src/libs/cgalpy/lib/polygon_2_bindings.cpp
git add src/libs/cgalpy/lib/alpha_shape_2_bindings.cpp
git add src/libs/cgalpy/lib/boolean_set_operations_2_bindings.cpp
git add src/libs/cgalpy/lib/envelope_2_bindings.cpp
git add src/libs/cgalpy/lib/visibility_2_bindings.cpp
git commit -m "docs: add docstring header files for pol2, as2, bso2, env2, vis2

- New dir: src/libs/cgalpy/lib/docstrings/
- 5 header files, ~50 docstring constants total
- Separates docstrings from binding code (Approach B)
- Binding .cpp files reference constants instead of inline strings
- No functional changes; all method signatures unchanged"
```

---

## Troubleshooting

**"Cannot open include file: docstrings/polygon_2_docstrings.h"**

Add to `src/libs/cgalpy/CMakeLists.txt` if the include path isn't picked up:

```
target_include_directories(CGALPY PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/lib)
```

**Docstring shows as `None`**

The constant is in the wrong position. It must be the last positional argument, after all `nb::arg()` and `nb::keep_alive` calls.

**Build error: redefinition of constant**

Two headers define the same name (e.g., `IS_VALID_DOC`). Prefix with the package name: `BSO2_IS_VALID_DOC`, `AS2_IS_VALID_DOC`.