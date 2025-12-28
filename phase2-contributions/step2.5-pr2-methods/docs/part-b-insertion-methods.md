# Part B: Specialized Insertion Methods

**Research Date**: December 27, 2025  
**Time Invested**: ~5 hours  
**Methods Tested**: 4 methods (6 overloads total)  
**Test File**: `test_insert_at_vertices.py` (250+ lines)

---

## Overview

These are the "power user" insertion methods. They skip all the safety checks that the general `insert()` function does, which makes them fast but dangerous. If you know exactly what you're doing and can guarantee your input is correct, they're great. If not, they'll silently corrupt your arrangement without any warning.

The C++ documentation explicitly states:

> "The specialized insertion functions are provided for additional flexibility. They do not check their preconditions, in order to achieve maximal efficiency." — CGAL Manual

In C++, this is acceptable—programmers are expected to validate input themselves. In Python, users expect exceptions for bad input, not silent corruption.

---

## Method 1: `insert_in_face_interior(curve, face)`

### C++ Signature

```cpp
Halfedge_handle insert_in_face_interior(const X_monotone_curve_2& c, Face_handle f)
```

### What It Does

Inserts an x-monotone curve that floats entirely inside a face—both endpoints become new vertices, and you get a new "island" edge in that face. Think of dropping a line segment into an empty canvas.

### Python Signature

```python
halfedge = arr.insert_in_face_interior(curve, face)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `curve` | X_monotone_curve_2 (e.g., Segment_2) | The curve to insert |
| `face` | Face handle | The face where the curve lies entirely |

### Returns

Halfedge directed **LEFT → RIGHT** (same direction as your segment).

- `halfedge.source()` = left endpoint of the curve
- `halfedge.target()` = right endpoint of the curve

### DCEL Changes

```
Before                  After
------                  -----
Vertices: N      →      Vertices: N + 2 (both degree 1, not isolated)
Edges: E         →      Edges: E + 1
Halfedges: H     →      Halfedges: H + 2 (twins of each other)
Faces: F         →      Faces: F + 1 (original face gets split)
```

### Preconditions (from C++ docs)

These are what the documentation says you MUST ensure before calling:

1. ✅ Curve must be x-monotone
2. ✅ Curve interior must be disjoint from all existing edges
3. ✅ Curve must lie entirely within face `f`
4. ✅ Curve endpoints must NOT coincide with existing vertices

### Validation Status: ❌ NONE

Does the method check ANY of these? **No.**

### Test Results

**Test 1: Basic correct usage**

```python
arr = Arrangement_2()
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr.insert_in_face_interior(seg, arr.unbounded_face())

print(f"Vertices: {arr.number_of_vertices()}")  # 2
print(f"Edges: {arr.number_of_edges()}")        # 1
print(f"Halfedge: {he.source().point()} → {he.target().point()}")  # 0 0 → 5 5
# ✓ Works correctly for valid input
```

**Test 2: Overlapping segments (violates precondition #2)**

```python
# First segment: fine
seg1 = Segment_2(Point_2(0, 0), Point_2(5, 5))
he1 = arr.insert_in_face_interior(seg1, arr.unbounded_face())

# Second segment: overlaps the first one!
seg2 = Segment_2(Point_2(2, 2), Point_2(7, 7))
he2 = arr.insert_in_face_interior(seg2, arr.unbounded_face())

# What happens?
print(f"Vertices: {arr.number_of_vertices()}")  # 4
print(f"Edges: {arr.number_of_edges()}")        # 2

# ⚠️ NO ERROR - creates invalid arrangement with overlapping edges
# Looks like it worked, but the topology is now garbage
# The DCEL structure is corrupted in ways that will cause problems later
```

### Returned Halfedge Direction

```python
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))  # LEFT → RIGHT
he = arr.insert_in_face_interior(seg, arr.unbounded_face())

print(f"source: {he.source().point()}")  # 0 0 (LEFT endpoint)
print(f"target: {he.target().point()}")  # 5 5 (RIGHT endpoint)

# ✓ Direction: LEFT → RIGHT (matches segment direction)
```

---

## Method 2: `insert_in_face_interior(point, face)`

### C++ Signature

```cpp
Vertex_handle insert_in_face_interior(const Point_2& p, Face_handle f)
```

### What It Does

Creates an isolated vertex (degree 0) at a point inside a face. This is how you start building arrangements incrementally—drop some points first, then connect them with edges later using `insert_at_vertices`.

### Python Signature

```python
vertex = arr.insert_in_face_interior(point, face)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `point` | Point_2 | Where to place the isolated vertex |
| `face` | Face handle | The face containing the point |

### Returns

Vertex handle for the newly created isolated vertex.

### DCEL Changes

```
Before                  After
------                  -----
Vertices: N      →      Vertices: N + 1 (degree 0, is_isolated() = True)
Edges: E         →      Edges: E (unchanged)
Halfedges: H     →      Halfedges: H (unchanged)
Faces: F         →      Faces: F (unchanged)
Face's isolated vertex count: I → I + 1
```

### Preconditions (from C++ docs)

1. ✅ Point must NOT coincide with existing vertices
2. ✅ Point must lie in interior of face `f` (not on boundary)

### Validation Status: ❌ NONE

### 🔴 CRITICAL TEST: Duplicate Points

This one really surprised me. The C++ docs clearly say the point shouldn't coincide with existing vertices. But watch what happens:

```python
unbounded = arr.unbounded_face()
v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
v2 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)  # SAME POINT!

print(f"Vertices created: {arr.number_of_vertices()}")  # 2
print(f"Same position? {v1.point() == v2.point()}")     # True
print(f"Same handle? {v1 == v2}")                       # False - DIFFERENT handles!
```

**Result**: You now have TWO vertices at the exact same coordinates. This violates the basic DCEL invariant that each position has exactly one vertex. The arrangement is structurally corrupt.

**Impact**: Silent corruption. Users can unknowingly create invalid arrangements that will cause bizarre bugs later when traversing or modifying the structure.

---

## Method 3: `insert_from_left_vertex(curve, vertex)`

### C++ Signature

```cpp
Halfedge_handle insert_from_left_vertex(const X_monotone_curve_2& c, Vertex_handle v)
```

### What It Does

Inserts a curve starting from an existing vertex. The vertex must be at the curve's LEFT endpoint, and a new vertex gets created at the RIGHT endpoint.

### Python Signature

```python
halfedge = arr.insert_from_left_vertex(curve, v_left)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `curve` | X_monotone_curve_2 | The curve to insert |
| `v_left` | Vertex handle | Existing vertex at curve's LEFT endpoint |

### Returns

Halfedge directed FROM the given vertex TO the newly created vertex.

- `halfedge.source()` = `v_left` (the vertex you passed)
- `halfedge.target()` = new vertex at right endpoint

### DCEL Changes

```
Before                  After
------                  -----
Vertices: N      →      Vertices: N + 1 (at right endpoint)
Edges: E         →      Edges: E + 1
Halfedges: H     →      Halfedges: H + 2
v_left.degree(): D →    v_left.degree(): D + 1
v_left.is_isolated(): ? → v_left.is_isolated(): False
Possible face split    →  (if v_left was on face boundary)
```

### Preconditions (from C++ docs)

1. ✅ `curve.source()` must equal `v_left.point()` (left endpoint matches)
2. ✅ `curve.target()` must NOT coincide with existing vertex
3. ✅ Curve interior must be disjoint from all existing edges

### Validation Status: ❌ NONE

### Test Results: Correct Usage

```python
v_left = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr.insert_from_left_vertex(seg, v_left)

print(f"source: {he.source().point()}")  # 0 0 (v_left - the vertex we gave it)
print(f"target: {he.target().point()}")  # 5 5 (new vertex created at right)
print(f"v_left.degree(): {v_left.degree()}")  # 1 (was 0)
print(f"v_left.is_isolated(): {v_left.is_isolated()}")  # False (was True)

# ✓ Direction: FROM v_left TO new vertex
# This is intuitive!
```

### ⚠️ Test Results: Mismatched Left Endpoint

This is where things get dangerous:

```python
# Create vertex at (10, 10)
v_left = arr.insert_in_face_interior(Point_2(10, 10), arr.unbounded_face())

# But segment starts at (0, 0) - doesn't match!
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))

he = arr.insert_from_left_vertex(seg, v_left)

print(f"Segment starts at: {seg.source()}")  # 0 0
print(f"But v_left is at: {v_left.point()}")  # 10 10
print(f"Halfedge source: {he.source().point()}")  # 10 10

# ⚠️ NO VALIDATION - creates edge from vertex at (10,10)
# using a curve that says it starts at (0,0)
# Geometry is now inconsistent with DCEL topology
```

**Impact**: The arrangement now has an edge where the vertex position doesn't match the curve endpoint. Geometric queries will return incorrect results.

---

## Method 4: `insert_from_right_vertex(curve, vertex)`

### C++ Signature

```cpp
Halfedge_handle insert_from_right_vertex(const X_monotone_curve_2& c, Vertex_handle v)
```

### What It Does

Insert curve TO an existing vertex at its RIGHT endpoint. Creates a new vertex at the LEFT endpoint.

### Python Signature

```python
halfedge = arr.insert_from_right_vertex(curve, v_right)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `curve` | X_monotone_curve_2 | The curve to insert |
| `v_right` | Vertex handle | Existing vertex at curve's RIGHT endpoint |

### Returns

Halfedge directed FROM the given vertex (v_right) TO the newly created vertex.

⚠️ **THE GOTCHA**: This means the halfedge points **RIGHT → LEFT**, which is the **OPPOSITE** of the curve direction!

### DCEL Changes

```
Before                  After
------                  -----
Vertices: N      →      Vertices: N + 1 (at LEFT endpoint)
Edges: E         →      Edges: E + 1
Halfedges: H     →      Halfedges: H + 2
v_right.degree(): D →   v_right.degree(): D + 1
v_right.is_isolated(): ? → v_right.is_isolated(): False
```

### Preconditions (from C++ docs)

1. ✅ `curve.target()` must equal `v_right.point()` (right endpoint matches)
2. ✅ `curve.source()` must NOT coincide with existing vertex
3. ✅ Curve interior disjoint from all edges

### Validation Status: ❌ NONE

### 🔥 CRITICAL: Return Value is REVERSED!

This one tripped me up for a while during testing:

```python
v_right = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))  # Points LEFT → RIGHT

he = arr.insert_from_right_vertex(seg, v_right)

print(f"Segment direction: {seg.source()} → {seg.target()}")
# Segment: 0 0 → 5 5 (LEFT → RIGHT)

print(f"Halfedge direction: {he.source().point()} → {he.target().point()}")
# Halfedge: 5 5 → 0 0 (RIGHT → LEFT)

# ⚠️ Direction REVERSED from segment!
# To get left→right, use: he.twin()
```

**Why does this happen?**

The method name means "insert FROM the right vertex"—so the returned halfedge starts AT that vertex. The pattern is that all methods return halfedges FROM the "source" vertex parameter. But when the vertex is on the RIGHT, that means the halfedge goes backward from the curve direction.

This is **internally consistent** with the API design, but **counter-intuitive** if you're thinking about segment direction.

### Test Results: Mismatched Right Endpoint

```python
v_right = arr.insert_in_face_interior(Point_2(10, 10), arr.unbounded_face())
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))  # Ends at (5,5), NOT (10,10)!

he = arr.insert_from_right_vertex(seg, v_right)

print(f"Segment ends at: {seg.target()}")    # 5 5
print(f"But v_right is at: {v_right.point()}")  # 10 10

# ⚠️ NO VALIDATION - creates edge with mismatched geometry
```

---

## Method 5: `insert_at_vertices(curve, v1, v2)`

### C++ Signature

```cpp
Halfedge_handle insert_at_vertices(const X_monotone_curve_2& c, Vertex_handle v1, Vertex_handle v2)
```

### What It Does

Connects two EXISTING vertices with a curve. No new vertices created—just a new edge between them. This is used to "draw the lines" after you've placed isolated vertices.

### Python Signature

```python
halfedge = arr.insert_at_vertices(curve, v1, v2)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `curve` | X_monotone_curve_2 | The curve connecting the vertices |
| `v1` | Vertex handle | Existing vertex (LEFT endpoint) |
| `v2` | Vertex handle | Existing vertex (RIGHT endpoint) |

### Returns

Halfedge directed v1 → v2 (first parameter to second).

### DCEL Changes

```
Before                  After
------                  -----
Vertices: N      →      Vertices: N (unchanged - uses existing)
Edges: E         →      Edges: E + 1
Halfedges: H     →      Halfedges: H + 2
v1.degree(): D1  →      v1.degree(): D1 + 1
v2.degree(): D2  →      v2.degree(): D2 + 1
v1.is_isolated(): ?  →  v1.is_isolated(): False
v2.is_isolated(): ?  →  v2.is_isolated(): False
Possible face split  →  (if edge crosses face)
```

### Preconditions (from C++ docs)

1. ✅ `v1.is_isolated()` must be True (historically)
2. ✅ `v2.is_isolated()` must be True (historically)
3. ✅ Curve endpoints must match vertex positions exactly
4. ✅ No edge already exists between v1 and v2
5. ✅ Curve interior disjoint from all edges

### Validation Status: ❌ NONE

### Test Results: Correct Usage

```python
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))

print(f"Before: v1.degree={v1.degree()}, v2.degree={v2.degree()}")  # 0, 0

he = arr.insert_at_vertices(seg, v1, v2)

print(f"After: v1.degree={v1.degree()}, v2.degree={v2.degree()}")  # 1, 1
print(f"Halfedge: {he.source().point()} → {he.target().point()}")  # 0 0 → 5 5

# ✓ Direction: v1 → v2
```

### ⚠️ Test Results: Mismatched Endpoints

```python
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())

# Segment goes to (10, 10) - doesn't match v2!
bad_seg = Segment_2(Point_2(0, 0), Point_2(10, 10))

he = arr.insert_at_vertices(bad_seg, v1, v2)

print(f"Segment ends at: {bad_seg.target()}")  # 10 10
print(f"But v2 is at: {v2.point()}")           # 5 5

# ⚠️ NO VALIDATION - creates edge with wrong geometry
# Edge connects (0,0)→(5,5) but curve says (0,0)→(10,10)
```

### ⚠️ Test Results: Duplicate Edges

```python
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he1 = arr.insert_at_vertices(seg, v1, v2)  # First edge
he2 = arr.insert_at_vertices(seg, v1, v2)  # DUPLICATE!

print(f"Edges: {arr.number_of_edges()}")  # 2

# ⚠️ Now you have two edges between the same vertices
# DCEL twin structure is corrupted
# Violates planar subdivision invariants
```

### ⚠️ Test Results: Non-Isolated Vertices

```python
# Create edge connecting v1 and v2
he1 = arr.insert_at_vertices(seg1, v1, v2)

# Now v1 and v2 are NOT isolated (degree 1)
print(f"v1.is_isolated() = {v1.is_isolated()}")  # False

# Try to insert another edge using non-isolated vertex
v3 = arr.insert_in_face_interior(Point_2(10, 0), arr.unbounded_face())
seg2 = Segment_2(Point_2(0, 0), Point_2(10, 0))
he2 = arr.insert_at_vertices(seg2, v1, v3)  # v1 NOT isolated!

# ⚠️ NO VALIDATION - method assumes isolated vertices
# May or may not work correctly depending on topology
```

---

## Halfedge Direction Pattern Summary

After testing all 4 methods, here's the consistent pattern:

| Method | Returned Halfedge Direction | Matches Curve Direction? | Notes |
|--------|---------------------------|-------------------------|-------|
| `insert_in_face_interior(curve, face)` | LEFT → RIGHT | ✅ Yes | Intuitive |
| `insert_from_left_vertex(curve, v)` | v_left → new_right | ✅ Yes | Intuitive |
| `insert_from_right_vertex(curve, v)` | v_right → new_left | ❌ **REVERSED** | Counter-intuitive! |
| `insert_at_vertices(curve, v1, v2)` | v1 → v2 | ✅ Yes | Intuitive |

**The Rule**: All methods return halfedge FROM the "source" vertex:
- For `insert_from_left_vertex`: source = v_left (matches curve)
- For `insert_from_right_vertex`: source = v_right (reversed from curve!)
- For `insert_at_vertices`: source = v1 (first parameter)

**User Impact**: `insert_from_right_vertex` is highly likely to confuse users who expect the returned halfedge to match the curve direction.

---

## When to Use Specialized Insertion Methods

### ✅ Valid Use Cases

1. **Batch construction from validated data** - You've verified all input beforehand
2. **Implementing geometric algorithms** - Sweep-line algorithms control topology
3. **Performance-critical code** - Thousands of insertions, validation overhead matters
4. **File I/O** - Loading from your own verified format

### ❌ Bad Use Cases

1. **User input** - Use `insert()` with automatic validation instead
2. **Interactive editing** - Too easy to violate preconditions
3. **Learning CGAL** - Too many ways to corrupt things silently
4. **Prototyping** - Use safe methods until you're confident

### Safe Alternative

Use the general `insert()` function:

```python
from CGALPY.Aos2 import insert

# Safe - handles all topological scenarios automatically
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
insert(arr, seg)  # Automatically finds location, handles intersections

# Or with point location strategy for better performance
from CGALPY.Aos2 import Arr_naive_point_location
pl = Arr_naive_point_location(arr)
insert(arr, seg, pl)
```

---

**Previous**: [← Part A - Introduction](./part-a-introduction.md)  
**Next**: [Part C - Removal Methods →](./part-c-removal-methods.md)
