#pragma once

/*
 * boolean_set_operations_2_docstrings.h
 * Docstring constants for boolean_set_operations_2_bindings.cpp
 * Part of: src/libs/cgalpy/lib/docstrings/
 */

const char* DO_INTERSECT_DOC = R"pbdoc(
Returns true if the interiors of two polygons or polygon sets intersect.
)pbdoc";

const char* INTERSECTION_DOC = R"pbdoc(
Computes the intersection of two polygons or polygon sets.

The result is stored in the output polygon set passed as the last argument.
)pbdoc";

const char* JOIN_DOC = R"pbdoc(
Computes the union of two polygons or polygon sets.

The result is stored in the output polygon set passed as the last argument.
)pbdoc";

const char* DIFFERENCE_DOC = R"pbdoc(
Computes the difference of two polygons or polygon sets (first minus second).

The result is stored in the output polygon set passed as the last argument.
)pbdoc";

const char* SYMMETRIC_DIFFERENCE_DOC = R"pbdoc(
Computes the symmetric difference of two polygons or polygon sets.

Returns the set of points that belong to exactly one of the two input sets.
)pbdoc";

const char* COMPLEMENT_DOC = R"pbdoc(
Computes the complement of a polygon set with respect to the plane.

The result is a polygon set representing all points NOT in the input set.
)pbdoc";

const char* IS_VALID_DOC = R"pbdoc(
Returns true if the polygon with holes or polygon set is valid.

A polygon with holes is valid if its outer boundary is a simple polygon
and all holes are simple polygons contained within the outer boundary.
)pbdoc";
