# April 7, 2026 — Polygon_2 Wiring Session

**Session time:** ~3 AM IST  
**Goal:** Finish wiring `polygon_2_docstrings.h` into `polygon_2_bindings.cpp`  
**Outcome:** 10 missing constants identified + docstring text determined. Heredoc append pending.

---

## What Was Discovered

A grep of `polygon_2_bindings.cpp` showed that the `.cpp` file **already has DOC
constants wired on every `.def()` call** — this means Wiring Step B (editing the
`.cpp`) is already done for this file. The only remaining work is Step A: making
sure the header file defines all the constants the `.cpp` references.

```bash
grep -n '.def(' src/libs/cgalpy/lib/polygon_2_bindings.cpp
```

### The Problem: 10 Missing Constants

The generated `polygon_2_docstrings.h` (created April 1) had **22 constants**.
The `.cpp` references **32 constants**. The 10 that were missing would cause
`undeclared identifier` build errors:

| Constant | `.cpp` Line |
|---|---|
| `IS_COUNTERCLOCKWISE_ORIENTED_DOC` | 61 |
| `IS_CLOCKWISE_ORIENTED_DOC` | 62 |
| `IS_COLLINEAR_ORIENTED_DOC` | 63 |
| `HAS_ON_POSITIVE_SIDE_DOC` | 64 |
| `HAS_ON_NEGATIVE_SIDE_DOC` | 65 |
| `HAS_ON_BOUNDARY_DOC` | 66 |
| `HAS_ON_BOUNDED_SIDE_DOC` | 67 |
| `HAS_ON_UNBOUNDED_SIDE_DOC` | 68 |
| `VERTEX_MUTABLE_DOC` | 84 |
| `EDGE_DOC` | 87 |

---

## Full `.def()` Map (polygon_2_bindings.cpp)

```
Line 51:  .def(py::init<>())                         — no doc (default ctor)
Line 52:  .def(py::init<const Pgn&>())               — no doc (copy ctor)
Line 53:  .def("__init__", ...)            __INIT___DOC
Line 54:  .def("push_back", ...)           PUSH_BACK_DOC
Line 55:  .def("is_simple", ...)           IS_SIMPLE_DOC
Line 56:  .def("is_convex", ...)           IS_CONVEX_DOC
Line 57:  .def("orientation", ...)         ORIENTATION_DOC
Line 58:  .def("oriented_side", ...)       ORIENTED_SIDE_DOC
Line 59:  .def("bounded_side", ...)        BOUNDED_SIDE_DOC
Line 60:  .def("is_empty", ...)            IS_EMPTY_DOC
Line 61:  .def("is_counterclockwise_oriented", ...)  IS_COUNTERCLOCKWISE_ORIENTED_DOC  ← WAS MISSING
Line 62:  .def("is_clockwise_oriented", ...)         IS_CLOCKWISE_ORIENTED_DOC         ← WAS MISSING
Line 63:  .def("is_collinear_oriented", ...)         IS_COLLINEAR_ORIENTED_DOC         ← WAS MISSING
Line 64:  .def("has_on_positive_side", ...)          HAS_ON_POSITIVE_SIDE_DOC          ← WAS MISSING
Line 65:  .def("has_on_negative_side", ...)          HAS_ON_NEGATIVE_SIDE_DOC          ← WAS MISSING
Line 66:  .def("has_on_boundary", ...)               HAS_ON_BOUNDARY_DOC               ← WAS MISSING
Line 67:  .def("has_on_bounded_side", ...)           HAS_ON_BOUNDED_SIDE_DOC           ← WAS MISSING
Line 68:  .def("has_on_unbounded_side", ...)         HAS_ON_UNBOUNDED_SIDE_DOC         ← WAS MISSING
Line 69:  .def("size", ...)                SIZE_DOC
Line 70:  .def("area", ...)                AREA_DOC
Line 71:  .def("bbox", ...)                BBOX_DOC
Line 72:  .def("__getitem__", ...)         — lambda (handled separately)
Line 74:  .def("left_vertex", ...)         LEFT_VERTEX_DOC
Line 75:  .def("right_vertex", ...)        RIGHT_VERTEX_DOC
Line 76:  .def("top_vertex", ...)          TOP_VERTEX_DOC
Line 77:  .def("bottom_vertex", ...)       BOTTOM_VERTEX_DOC
Line 84:  .def("vertex_mutable", ...)      VERTEX_MUTABLE_DOC                          ← WAS MISSING
Line 85:  .def("vertex", ...)              VERTEX_DOC
Line 87:  .def("edge", ...)                EDGE_DOC                                    ← WAS MISSING
Line 88:  .def("clear", ...)               CLEAR_DOC
Line 89:  .def("reverse_orientation", ...) REVERSE_ORIENTATION_DOC
Line 90:  .def(py::self == py::self)       — no doc (operator)
Line 91:  .def(py::self != py::self)       — no doc (operator)
Line 96:  pgn_c.def("edges", ...)          — lambda (edges iterator)
Line 102: pgn_c.def("vertices", ...)       — lambda (vertices iterator)
Line 115: m.def("draw", ...)               DRAW_DOC
```

---

## The Fix — Append to polygon_2_docstrings.h

Run from the repo root:

```bash
cat >> src/libs/cgalpy/lib/docstrings/polygon_2_docstrings.h << 'HEREDOC'

const char* IS_COUNTERCLOCKWISE_ORIENTED_DOC = R"pbdoc(
Returns true if the polygon is counterclockwise oriented.

Equivalent to ``orientation() == CGAL::COUNTERCLOCKWISE``.
)pbdoc";

const char* IS_CLOCKWISE_ORIENTED_DOC = R"pbdoc(
Returns true if the polygon is clockwise oriented.

Equivalent to ``orientation() == CGAL::CLOCKWISE``.
)pbdoc";

const char* IS_COLLINEAR_ORIENTED_DOC = R"pbdoc(
Returns true if the polygon is collinear oriented.

Equivalent to ``orientation() == CGAL::COLLINEAR``. This is the case
when all vertices are collinear.
)pbdoc";

const char* HAS_ON_POSITIVE_SIDE_DOC = R"pbdoc(
Returns true if the point ``q`` is on the positive side of the polygon.

The positive side is the left side of a counterclockwise-oriented polygon.
Equivalent to ``oriented_side(q) == CGAL::ON_POSITIVE_SIDE``.
)pbdoc";

const char* HAS_ON_NEGATIVE_SIDE_DOC = R"pbdoc(
Returns true if the point ``q`` is on the negative side of the polygon.

The negative side is the right side of a counterclockwise-oriented polygon.
Equivalent to ``oriented_side(q) == CGAL::ON_NEGATIVE_SIDE``.
)pbdoc";

const char* HAS_ON_BOUNDARY_DOC = R"pbdoc(
Returns true if the point ``q`` lies on the boundary of the polygon.

Equivalent to ``bounded_side(q) == CGAL::ON_BOUNDARY``.
)pbdoc";

const char* HAS_ON_BOUNDED_SIDE_DOC = R"pbdoc(
Returns true if the point ``q`` lies in the bounded region of the polygon.

Equivalent to ``bounded_side(q) == CGAL::ON_BOUNDED_SIDE``.
The polygon must be simple for this to be well-defined.
)pbdoc";

const char* HAS_ON_UNBOUNDED_SIDE_DOC = R"pbdoc(
Returns true if the point ``q`` lies in the unbounded region of the polygon.

Equivalent to ``bounded_side(q) == CGAL::ON_UNBOUNDED_SIDE``.
The polygon must be simple for this to be well-defined.
)pbdoc";

const char* VERTEX_MUTABLE_DOC = R"pbdoc(
Returns a mutable reference to the vertex at position ``i``.

Unlike ``vertex()``, this overload returns a non-const reference that
allows the vertex coordinates to be modified in place.
)pbdoc";

const char* EDGE_DOC = R"pbdoc(
Returns the edge of the polygon at position ``i`` as a Segment_2.

The edge connects vertex ``i`` to vertex ``(i+1) % size()``.
)pbdoc";
HEREDOC
```

---

## After Appending — Build & Verify

### 1. Build

```bash
cd build-manual
export CC=/usr/bin/clang && export CXX=/usr/bin/clang++
make CGALPY -j4
```

Expected output: `[100%] Built target CGALPY` — zero errors.

### 2. Verify __doc__ for spot-check constants

```bash
python3 -c "import CGALPY; print(CGALPY.Pol2.Polygon_2.is_counterclockwise_oriented.__doc__)"
python3 -c "import CGALPY; print(CGALPY.Pol2.Polygon_2.edge.__doc__)"
python3 -c "import CGALPY; print(CGALPY.Pol2.Polygon_2.vertex_mutable.__doc__)"
python3 -c "import CGALPY; print(CGALPY.Pol2.Polygon_2.has_on_bounded_side.__doc__)"
```

---

## Status After This Session

| Step | Status |
|---|---|
| 10 missing constants identified | ✅ Done |
| Docstring text determined for all 10 | ✅ Done (this session) |
| `polygon_2_docstrings.h` updated (prep repo copy) | ✅ Done |
| Heredoc append run on actual machine | ❌ **TODO** — do this first next session |
| `make CGALPY -j4` run after append | ❌ **TODO** |
| Runtime `__doc__` spot-check (3 methods) | ❌ **TODO** |
| `#include "docstrings/polygon_2_docstrings.h"` in `.cpp` | ✅ Already present (grep confirmed) |

---

## Next Files to Wire (after polygon_2 build passes)

1. `alpha_shape_2_bindings.cpp` — grep `.def()` calls, compare vs `alpha_shape_2_docstrings.h`
2. `boolean_set_operations_2_bindings.cpp` — same
3. `envelope_2_bindings.cpp` — same
4. `visibility_2_bindings.cpp` — same

Use same pattern: grep → compare → append missing → build → verify.
