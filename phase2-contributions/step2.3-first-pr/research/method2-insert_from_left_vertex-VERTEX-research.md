# Research: insert_from_left_vertex (Vertex Version)

**Date:** Dec 26, 2025, 12:31 AM IST  
**Status:** Tested and working ✅  
**Time invested:** ~2 hours (testing + debugging direction semantics)

## Binding Location

**File:** `arrangement_on_surface_2_bindings.cpp`  
**Line:** 743

```cpp
.def("insert_from_left_vertex",
     &aos2::insert_cv_from_vertex</*LEFT*/ true>,
     ri)
```

Note the template parameter `<true>` - this is what makes it "left" vs "right"!

## Current State (Before My PR)

- ❌ **No docstring** - undocumented
- ❌ **No parameter names** - shows `(*args, **kwargs)`
- ❌ **No examples** - unclear how to use

**Current signature:**

```python
inspect.signature(arr.insert_from_left_vertex)
# (*args, **kwargs)
```

Users have no idea what to pass or in what order!

## What This Method Does

Inserts a new **x-monotone curve** (edge) into the arrangement, where one endpoint (the **left** one) is an **existing vertex**.

### Key Characteristics:
- Left endpoint of curve **must match** an existing vertex's location
- Creates a **new vertex** at the right endpoint
- Creates **2 halfedges** (twin pair) representing the new edge
- May **split the face** if curve divides it

### When to Use:
- Building arrangement incrementally from a starting vertex
- Extending an arrangement by adding edges from known points
- When you have the left endpoint but need to create the right endpoint

## Parameters

### Parameter 1: `curve` (X_monotone_curve_2)
- **Type:** X_monotone curve (e.g., Segment_2, Arc, etc.)
- **Purpose:** The curve to insert as a new edge
- **Constraint:** Left endpoint must coincide with `vertex` parameter
- **X-monotone:** Curve must be monotone in X direction (no vertical tangent changes)

### Parameter 2: `vertex` (Vertex handle)
- **Type:** Vertex handle (from Arrangement_2)
- **Purpose:** The existing vertex at the curve's **left endpoint**
- **Constraint:** Must be a valid vertex in the arrangement
- **Constraint:** Must be at the same location as curve's left endpoint

## Return Value

**Type:** Halfedge handle

**Direction:** The returned halfedge points **FROM left TO right**

**Properties:**
- `source()` → the input `vertex` (left endpoint)
- `target()` → the newly created vertex (right endpoint)
- `curve()` → the input curve
- `twin()` → the opposite halfedge (right→left direction)

**Lifetime:** Valid as long as arrangement exists (`reference_internal`)

## Preconditions

From C++ documentation:
1. The `vertex` must be at the **left endpoint** of the `curve`
2. The curve must be **disjoint** from existing edges (no intersections)
3. Curve must lie in a **single face** (won't split through multiple faces)

### Validation Status:
I didn't test precondition violations extensively, but I suspect (like `insert_in_face_interior`) that **validation is minimal or absent**. Users must ensure preconditions themselves!

## DCEL Topology Changes

**Before calling:**
- Left vertex exists (the input parameter)
- Face contains the curve region

**After calling:**
- +1 Vertex (at right endpoint of curve)
- +2 Halfedges (twin pair for new edge)
- +1 Edge (the curve)
- May split face (+1 face if curve subdivides)

**Degree update:**
- Left vertex: degree increases by 1
- Right vertex (new): starts with degree 1

**Complexity:** 
- O(1) if no face split
- O(n) if face split requires traversal

## Test Results (Dec 26, 12:31 AM)

```python
from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Segment_2, Point_2

arr = Arrangement_2()
unbounded = arr.unbounded_face()

# Step 1: Create isolated vertex at left endpoint
v_left = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
print(f"Initial degree: {v_left.degree()}")  # 0

# Step 2: Insert segment FROM this left vertex
seg = Segment_2(Point_2(0, 0), Point_2(3, 3))
he = arr.insert_from_left_vertex(seg, v_left)

# Verify halfedge direction
print(he.source().point())  # Output: 0 0 (left - input vertex) ✅
print(he.target().point())  # Output: 3 3 (right - newly created) ✅

# Verify degree update
print(v_left.degree())  # Output: 1 (was 0, now has edge) ✅

# Verify twin exists
print(he.twin() is not None)  # True ✅

# Verify right vertex is NOT isolated
print(he.target().is_isolated())  # False ✅
```

**Result:** ✅ Works exactly as expected!

## Key Discovery: Halfedge Direction

The returned halfedge has:
- **Source = left vertex** (the one we passed as parameter)
- **Target = right vertex** (newly created)

This makes sense because the method is "insert **FROM** left vertex", so the halfedge naturally points FROM that vertex.

**Intuitive naming!** 👍 (Unlike `insert_from_right_vertex` - see that research doc)

## Related Methods

- `insert_in_face_interior()` - Create the initial isolated vertex first
- `insert_from_right_vertex()` - Opposite: curve's right endpoint is existing
- `insert_at_vertices()` - Connect two existing vertices (both endpoints exist)
- `modify_edge()` - Change the curve of an existing edge
- `remove_edge()` - Delete this edge

## Common Mistakes to Warn About

1. **Wrong endpoint order** - Passing vertex at right endpoint instead of left
2. **Curve not x-monotone** - Some traits require pre-processing
3. **Curve intersects existing edges** - Creates invalid topology
4. **Trying to use non-existent vertex** - Must create isolated vertex first!

## Use Case Example

**Incremental construction pattern:**

```python
# Start with isolated point
v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)

# Extend from left
seg1 = Segment_2(Point_2(0, 0), Point_2(5, 0))
he1 = arr.insert_from_left_vertex(seg1, v1)

# Now extend from the newly created right vertex
v2 = he1.target()  # Right vertex from previous insertion
seg2 = Segment_2(Point_2(5, 0), Point_2(5, 5))
he2 = arr.insert_from_left_vertex(seg2, v2)

# Result: Connected path from (0,0) → (5,0) → (5,5)
```

This is a common workflow!

## Nanobind Details

**Current binding:**

```cpp
.def("insert_from_left_vertex",
     &aos2::insert_cv_from_vertex</*LEFT*/ true>,
     ri)
```

**What I need to add:**

```cpp
.def("insert_from_left_vertex",
     &aos2::insert_cv_from_vertex</*LEFT*/ true>,
     nb::arg("curve"),    // ← Add this!
     nb::arg("vertex"),   // ← Add this!
     ri,
     R"pbdoc(
         [Docstring here]
     )pbdoc")
```

**Template magic:** The C++ code uses a single templated function with a boolean parameter to implement both `insert_from_left_vertex` (true) and `insert_from_right_vertex` (false). Smart code reuse!

## Links

- [CGAL Arrangement_2 insert methods](https://doc.cgal.org/latest/Arrangement_on_surface_2/classCGAL_1_1Arrangement__2.html)

## My Understanding Level

**Confidence:** 95% ✅

This one was straightforward to understand. The naming is intuitive, the halfedge direction makes sense, and my test proves it works correctly.

**No surprises here!** (Unlike the next method...)

## Next Steps for Docstring

1. One-line: "Insert curve from existing left endpoint vertex"
2. Description: When to use, what gets created, DCEL changes
3. Parameter docs: emphasize left endpoint constraint
4. Return: Halfedge FROM left TO right (clear direction)
5. Example: My test code above (simplified)
6. See Also: Cross-reference to right_vertex variant and insert_at_vertices
7. Notes: Preconditions, no validation warning, incremental construction pattern

---

**Notes to self:**
- This method's naming is intuitive (unlike its sibling!)
- The incremental construction example is important to include
- Halfedge direction is clear: source=left (input), target=right (created)
- Need to explain the twin halfedge concept for users unfamiliar with DCEL.