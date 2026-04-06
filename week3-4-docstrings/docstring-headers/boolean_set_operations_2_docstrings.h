#pragma once

// boolean_set_operations_2_docstrings.h
// =====================================
// Docstring constants for CGALPY.Bso2 bindings.
// Source: https://doc.cgal.org/latest/Boolean_set_operations_2/
// #include "docstrings/boolean_set_operations_2_docstrings.h"

const char *DO_INTERSECT_DOC = R"pbdoc(
Returns true if two polygons or polygon sets have a non-empty intersection.

Parameters
----------
p : General_polygon_2 or General_polygon_set_2
q : General_polygon_2 or General_polygon_set_2
)pbdoc";

const char *INTERSECTION_DOC = R"pbdoc(
Computes the intersection of two polygons or polygon sets.

Returns a list of General_polygon_with_holes_2 objects whose union
equals the geometric intersection of the inputs.
)pbdoc";

const char *JOIN_DOC = R"pbdoc(
Computes the union of two polygons or polygon sets.

Returns a list of General_polygon_with_holes_2 objects whose union
equals the geometric union of the inputs.
)pbdoc";

const char *DIFFERENCE_DOC = R"pbdoc(
Computes the set-theoretic difference (p minus q) of two polygon sets.

Returns the region belonging to p but not to q.
)pbdoc";

const char *SYMMETRIC_DIFFERENCE_DOC = R"pbdoc(
Computes the symmetric difference of two polygons or polygon sets.

Returns the region belonging to exactly one of p or q.
)pbdoc";

const char *COMPLEMENT_DOC = R"pbdoc(
Computes the complement of a polygon set.

Returns a polygon set representing the entire plane minus the input region.
)pbdoc";

const char *IS_VALID_DOC = R"pbdoc(
Returns true if the polygon set is valid.

A set is valid if all its polygons are valid and they do not overlap.
)pbdoc";