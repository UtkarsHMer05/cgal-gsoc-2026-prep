# April 7, 2026 — Polygon_2 Header Wiring Audit

> Session: ~3 AM IST | Duration: ~1 hour

## Context

`polygon_2_bindings.cpp` already has DOC constants wired on every `.def()` call —
confirmed via `grep -n '.def(' src/libs/cgalpy/lib/polygon_2_bindings.cpp`.

**Problem:** `polygon_2_docstrings.h` is missing 10 constants the `.cpp` references.
A build attempt would fail with `undeclared identifier` on all 10.

---

## Full .def() audit from grep output

```
Line 51:  .def(py::init<>())                        — bare ctor, no doc needed
Line 52:  .def(py::init<const Pgn&>())              — copy ctor, no doc needed
Line 53:  _INIT__DOC                                ✅ exists in header
Line 54:  PUSH_BACK_DOC                             ✅ exists
Line 55:  IS_SIMPLE_DOC                             ✅ exists
Line 56:  IS_CONVEX_DOC                             ✅ exists
Line 57:  ORIENTATION_DOC                           ✅ exists
Line 58:  ORIENTED_SIDE_DOC                         ✅ exists
Line 59:  BOUNDED_SIDE_DOC                          ✅ exists
Line 60:  IS_EMPTY_DOC                              ✅ exists
Line 61:  IS_COUNTERCLOCKWISE_ORIENTED_DOC          ❌ MISSING
Line 62:  IS_CLOCKWISE_ORIENTED_DOC                 ❌ MISSING
Line 63:  IS_COLLINEAR_ORIENTED_DOC                 ❌ MISSING
Line 64:  HAS_ON_POSITIVE_SIDE_DOC                  ❌ MISSING
Line 65:  HAS_ON_NEGATIVE_SIDE_DOC                  ❌ MISSING
Line 66:  HAS_ON_BOUNDARY_DOC                       ❌ MISSING
Line 67:  HAS_ON_BOUNDED_SIDE_DOC                   ❌ MISSING
Line 68:  HAS_ON_UNBOUNDED_SIDE_DOC                 ❌ MISSING
Line 69:  SIZE_DOC                                  ✅ exists
Line 70:  AREA_DOC                                  ✅ exists
Line 71:  BBOX_DOC                                  ✅ exists
Line 72:  _getitem_ lambda                          — no separate DOC constant needed
Line 74:  LEFT_VERTEX_DOC                           ✅ exists
Line 75:  RIGHT_VERTEX_DOC                          ✅ exists
Line 76:  TOP_VERTEX_DOC                            ✅ exists
Line 77:  BOTTOM_VERTEX_DOC                         ✅ exists
Line 84:  VERTEX_MUTABLE_DOC                        ❌ MISSING
Line 85:  VERTEX_DOC                                ✅ exists
Line 87:  EDGE_DOC                                  ❌ MISSING
Line 88:  CLEAR_DOC                                 ✅ exists
Line 89:  REVERSE_ORIENTATION_DOC                   ✅ exists
Line 90:  py::self == py::self                      — operator, no doc
Line 91:  py::self != py::self                      — operator, no doc
Line 96:  edges iterator lambda                     — no constant needed
Line 102: vertices iterator lambda                  — no constant needed
Line 115: DRAW_DOC                                  ✅ exists
```

**22 already exist. 10 are missing.**

---

## Fix command — run from repo root

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
Returns true if the point q is on the positive side of the polygon.

The positive side is the left side of a counterclockwise-oriented polygon.
Equivalent to ``oriented_side(q) == CGAL::ON_POSITIVE_SIDE``.
)pbdoc";

const char* HAS_ON_NEGATIVE_SIDE_DOC = R"pbdoc(
Returns true if the point q is on the negative side of the polygon.

The negative side is the right side of a counterclockwise-oriented polygon.
Equivalent to ``oriented_side(q) == CGAL::ON_NEGATIVE_SIDE``.
)pbdoc";

const char* HAS_ON_BOUNDARY_DOC = R"pbdoc(
Returns true if the point q lies on the boundary of the polygon.

Equivalent to ``bounded_side(q) == CGAL::ON_BOUNDARY``.
)pbdoc";

const char* HAS_ON_BOUNDED_SIDE_DOC = R"pbdoc(
Returns true if the point q lies in the bounded region of the polygon.

Equivalent to ``bounded_side(q) == CGAL::ON_BOUNDED_SIDE``.
The polygon must be simple for this to be well-defined.
)pbdoc";

const char* HAS_ON_UNBOUNDED_SIDE_DOC = R"pbdoc(
Returns true if the point q lies in the unbounded region of the polygon.

Equivalent to ``bounded_side(q) == CGAL::ON_UNBOUNDED_SIDE``.
The polygon must be simple for this to be well-defined.
)pbdoc";

const char* VERTEX_MUTABLE_DOC = R"pbdoc(
Returns a mutable reference to the vertex at position i.

Unlike ``vertex()``, this non-const overload allows the vertex
coordinates to be modified in place.
)pbdoc";

const char* EDGE_DOC = R"pbdoc(
Returns the edge at position i as a Segment_2.

The edge connects vertex i to vertex (i+1) % size().
)pbdoc";
HEREDOC
```

## Verify after appending

```bash
cd build-manual
export CC=/usr/bin/clang && export CXX=/usr/bin/clang++
make CGALPY -j4

PYTHONPATH=src/libs/cgalpy python3 -c "
import CGALPY
print(CGALPY.Pol2.Polygon_2.is_counterclockwise_oriented.__doc__)
print(CGALPY.Pol2.Polygon_2.edge.__doc__)
print(CGALPY.Pol2.Polygon_2.vertex_mutable.__doc__)
print(CGALPY.Pol2.Polygon_2.has_on_bounded_side.__doc__)
"
```

---

## Source

All text from CGAL Polygon_2 reference:
https://doc.cgal.org/latest/Polygon/classCGAL_1_1Polygon__2.html

`VERTEX_MUTABLE_DOC` and `EDGE_DOC` are manually written (no dedicated
`/*!` entries in CGAL doc headers) but match CGAL API semantics exactly.

---

## Status

- [x] All 10 missing constants identified
- [x] Exact docstring text written for all 10
- [ ] NOT yet appended to the header on disk
- [ ] Build NOT yet run
- [ ] Other 4 packages not yet audited 