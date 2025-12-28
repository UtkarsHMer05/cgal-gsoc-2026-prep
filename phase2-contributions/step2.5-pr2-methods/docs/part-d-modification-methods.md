# Part D: Modification Methods

**Research Date**: December 28, 2025  
**Time Invested**: ~3 hours  
**Methods Tested**: 4 methods  
**Test File**: `test_modification_methods.py` (~350 lines)

---

## Overview

Modification methods let you change existing arrangement elements in-place without full delete/reinsert cycles. They're all bound in Python (good news!), but they share the same "zero validation" philosophy as everything else (not so good).

These methods are particularly tricky because they can create **geometric inconsistencies**—where the DCEL topology is technically valid but the geometry is wrong (vertex positions don't match curve endpoints).

---

## Method 1: `split_edge(halfedge, curve1, curve2)`

### C++ Signature

```cpp
Halfedge_handle split_edge(Halfedge_handle e, 
                           const X_monotone_curve_2& c1, 
                           const X_monotone_curve_2& c2)
```

### What It Does

Splits an existing edge into two edges at some interior point. You provide:
- The halfedge to split
- `curve1`: segment from original source to split point
- `curve2`: segment from split point to original target

The two curves should geometrically add up to the original curve.

### Python Signature

```python
halfedge = arr.split_edge(he, curve1, curve2)
```

### DCEL Changes

```
Before                  After
------                  -----
Vertices: N      →      Vertices: N + 1 (at split point, degree 2)
Edges: E         →      Edges: E + 1 (now 2 edges instead of 1)
Halfedges: H     →      Halfedges: H + 2 (now 4 instead of 2)
Original edge    →      Becomes first segment
                        Second segment is new
```

### What It Returns

Halfedge of the **first segment** (source → split_point).

### Preconditions (from C++ docs)

1. ✅ `curve1.target()` must equal `curve2.source()` (the split point)
2. ✅ `curve1.source()` must equal original `e.source().point()`
3. ✅ `curve2.target()` must equal original `e.target().point()`
4. ✅ Split point must be in interior of original curve (not at endpoints)

### Validation Status: ❌ **NONE**

### Test Results: Basic Split

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(10, 10), arr.unbounded_face())
he = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(10, 10)), v1, v2)

print(f"Before split:")
print(f"  Vertices: {arr.number_of_vertices()}")  # 2
print(f"  Edges: {arr.number_of_edges()}")        # 1
print(f"  Halfedge: {he.source().point()} → {he.target().point()}")

# Split at midpoint (5, 5)
c1 = Segment_2(Point_2(0, 0), Point_2(5, 5))
c2 = Segment_2(Point_2(5, 5), Point_2(10, 10))

he_new = arr.split_edge(he, c1, c2)

print(f"\nAfter split:")
print(f"  Vertices: {arr.number_of_vertices()}")  # 3
print(f"  Edges: {arr.number_of_edges()}")        # 2
print(f"  Returned halfedge: {he_new.source().point()} → {he_new.target().point()}")
# Returns: 0 0 → 5 5 (first segment)

new_vertex = he_new.target()
print(f"  New vertex at: {new_vertex.point()}")    # 5 5
print(f"  New vertex degree: {new_vertex.degree()}")  # 2

# ✓ Works correctly for valid input
```

### ⚠️ Test Results: Mismatched Curves (Wrong Split Point)

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(10, 10), arr.unbounded_face())
he = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(10, 10)), v1, v2)

# Try split with curves that don't match the midpoint
bad_c1 = Segment_2(Point_2(0, 0), Point_2(3, 3))   # Ends at (3,3)
bad_c2 = Segment_2(Point_2(3, 3), Point_2(10, 10))  # Starts at (3,3)

print(f"Original edge: {he.source().point()} → {he.target().point()}")
print(f"Trying to split with: (0,0)→(3,3) + (3,3)→(10,10)")
print(f"  (Original midpoint was (5,5), not (3,3))")

arr.split_edge(he, bad_c1, bad_c2)

print(f"Vertices after split: {arr.number_of_vertices()}")  # 3

# ⚠️ Result: NO ERROR - accepts curves even if they don't represent
# the actual geometric midpoint of the original edge
# Creates vertex at (3,3) based on your curves, not the real geometry
```

**Impact**: The split happens at whatever point your curves say, regardless of whether it's geometrically correct. If you make a mistake calculating the split point, you get an arrangement that's topologically valid but geometrically wrong.

### ⚠️ Test Results: Degenerate Split at Endpoint

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(10, 10), arr.unbounded_face())
he = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(10, 10)), v1, v2)

# Try to "split" at the source endpoint (not a real split)
c1 = Segment_2(Point_2(0, 0), Point_2(0, 0))   # Zero-length segment!
c2 = Segment_2(Point_2(0, 0), Point_2(10, 10))  # Full original edge

print(f"Trying to split at endpoint (0,0) with zero-length first segment")
arr.split_edge(he, c1, c2)

print(f"Vertices: {arr.number_of_vertices()}")  # 3 ← created vertex at (0,0)!

# ⚠️ Result: NO VALIDATION - allows split at endpoint
# Creates a DUPLICATE vertex at the same location as v1
# Now you have two vertices at (0,0)
# DCEL invariant violated, topology corrupted
```

### ⚠️ Test Results: Handle Behavior After Split

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(10, 10), arr.unbounded_face())
he_original = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(10, 10)), v1, v2)

print(f"Original halfedge: {he_original.source().point()} → {he_original.target().point()}")
# 0 0 → 10 10

c1 = Segment_2(Point_2(0, 0), Point_2(5, 5))
c2 = Segment_2(Point_2(5, 5), Point_2(10, 10))
he_new = arr.split_edge(he_original, c1, c2)

print(f"New halfedge: {he_new.source().point()} → {he_new.target().point()}")
# 0 0 → 5 5

# Try to access original halfedge after split:
print(f"\nAccessing original halfedge after split:")
orig_source = he_original.source().point()
orig_target = he_original.target().point()
print(f"  Original halfedge: {orig_source} → {orig_target}")
# Shows: 0 0 → 5 5 (modified to first segment!)

# ⚠️ Result: Old handle was REUSED for first segment
# This is implementation-dependent behavior
# Sometimes the handle is reused, sometimes it's invalidated
# You cannot rely on this behavior
```

---

## Method 2: `merge_edge(he1, he2, merged_curve)`

### C++ Signature

```cpp
Halfedge_handle merge_edge(Halfedge_handle e1, 
                           Halfedge_handle e2, 
                           const X_monotone_curve_2& c)
```

### What It Does

Opposite of split—combines two edges that share a common vertex into one edge. The shared vertex must have degree exactly 2 (only these two edges touch it). After merging, the shared vertex is removed.

### Python Signature

```python
halfedge = arr.merge_edge(he1, he2, merged_curve)
```

### DCEL Changes

```
Before                  After
------                  -----
Vertices: N      →      Vertices: N - 1 (shared vertex removed)
Edges: E         →      Edges: E - 1 (two edges become one)
Halfedges: H     →      Halfedges: H - 2 (four halfedges become two)
```

### What It Returns

Halfedge of the merged edge.

### Preconditions (from C++ docs)

1. ✅ `he1.target()` must equal `he2.source()` (edges share a vertex)
2. ✅ Shared vertex must have degree exactly 2 (only these two edges)
3. ✅ `merged_curve` must represent the geometric union of the two curves

### Validation Status: ❌ **NONE**

### Test Results: Successful Merge

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
v3 = arr.insert_in_face_interior(Point_2(10, 10), arr.unbounded_face())

he1 = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(5, 5)), v1, v2)
he2 = arr.insert_at_vertices(Segment_2(Point_2(5, 5), Point_2(10, 10)), v2, v3)

print(f"Before merge:")
print(f"  Edge 1: {he1.source().point()} → {he1.target().point()}")
print(f"  Edge 2: {he2.source().point()} → {he2.target().point()}")
print(f"  Shared vertex v2: {v2.point()}, degree {v2.degree()}")
print(f"  Vertices: {arr.number_of_vertices()}")  # 3
print(f"  Edges: {arr.number_of_edges()}")        # 2

merged_curve = Segment_2(Point_2(0, 0), Point_2(10, 10))
he_merged = arr.merge_edge(he1, he2, merged_curve)

print(f"\nAfter merge:")
print(f"  Merged halfedge: {he_merged.source().point()} → {he_merged.target().point()}")
print(f"  Vertices: {arr.number_of_vertices()}")  # 2 (v2 removed)
print(f"  Edges: {arr.number_of_edges()}")        # 1

# ✓ Merge succeeded, shared vertex deleted
```

### 🔴 CRASH: Non-Adjacent Edges = SEGFAULT

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
v3 = arr.insert_in_face_interior(Point_2(10, 0), arr.unbounded_face())
v4 = arr.insert_in_face_interior(Point_2(15, 5), arr.unbounded_face())

# Two edges that DON'T share a vertex
he1 = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(5, 5)), v1, v2)
he2 = arr.insert_at_vertices(Segment_2(Point_2(10, 0), Point_2(15, 5)), v3, v4)

print(f"Edge 1: {he1.source().point()} → {he1.target().point()}")
print(f"Edge 2: {he2.source().point()} → {he2.target().point()}")
print(f"Edges share vertex? NO - they are completely separate")

merged = Segment_2(Point_2(0, 0), Point_2(15, 5))
arr.merge_edge(he1, he2, merged)

# OUTPUT:
# zsh: segmentation fault  python test_modification_methods.py
```

**This crashes Python instantly.** No validation, no exception—just death.

### ⚠️ Test Results: Wrong Merged Curve

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
v3 = arr.insert_in_face_interior(Point_2(10, 10), arr.unbounded_face())

he1 = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(5, 5)), v1, v2)
he2 = arr.insert_at_vertices(Segment_2(Point_2(5, 5), Point_2(10, 10)), v2, v3)

# Give it a WRONG merged curve
wrong_curve = Segment_2(Point_2(0, 0), Point_2(8, 8))  # Doesn't reach v3!

print(f"Edge 1: (0,0) → (5,5)")
print(f"Edge 2: (5,5) → (10,10)")
print(f"Giving wrong merged curve: (0,0) → (8,8)")

he_merged = arr.merge_edge(he1, he2, wrong_curve)
print(f"Vertices: {arr.number_of_vertices()}")  # 2

# ⚠️ Result: NO VALIDATION - accepts wrong curve
# Creates edge with curve that doesn't match vertex positions
# Edge connects (0,0)→(10,10) but curve says (0,0)→(8,8)
# Geometric inconsistency
```

### 🔴 CRASH: Accessing Deleted Vertex After Merge

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
v3 = arr.insert_in_face_interior(Point_2(10, 10), arr.unbounded_face())

he1 = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(5, 5)), v1, v2)
he2 = arr.insert_at_vertices(Segment_2(Point_2(5, 5), Point_2(10, 10)), v2, v3)

merged_curve = Segment_2(Point_2(0, 0), Point_2(10, 10))
he_merged = arr.merge_edge(he1, he2, merged_curve)

print(f"After merge: {arr.number_of_vertices()} vertices")  # 2 (v2 was deleted)

# Try to access the DELETED shared vertex v2
print(f"Accessing deleted vertex v2:")
v2_point = v2.point()  # This line CRASHES!

# OUTPUT:
# zsh: segmentation fault  python test_modification_methods.py
```

**Analysis**: Unlike `remove_edge()` where deleted vertices sometimes return stale data, `merge_edge()` immediately frees the vertex memory, causing instant crash on any access.

---

## Method 3: `modify_vertex(vertex, new_point)`

### C++ Signature

```cpp
void modify_vertex(Vertex_handle v, const Point_2& p)
```

### What It Does

Changes the point associated with vertex `v` to `new_point`. But here's the critical catch—**it does NOT update incident edge curves automatically**. You must manually update all incident curves using `modify_edge()`.

### Python Signature

```python
arr.modify_vertex(vertex, new_point)
```

No return value.

### DCEL Changes

```
Before                  After
------                  -----
Vertex v's point: P  →  Vertex v's point: new_point
Topology: unchanged  →  Topology: unchanged
Edge curves: unchanged → Edge curves: UNCHANGED (inconsistency!)
```

### Preconditions (from C++ docs)

1. ✅ New point must not create conflicts with other vertices
2. ✅ New point should maintain topological correctness
3. (In practice, nothing is checked)

### Validation Status: ❌ **NONE**

### ⚠️ Test Results: Creates Geometric Inconsistency

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(10, 10), arr.unbounded_face())
he = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(10, 10)), v1, v2)

print(f"Before modification:")
print(f"  v1.point() = {v1.point()}")    # 0 0
print(f"  v1.degree() = {v1.degree()}")  # 1
print(f"  Edge curve: {he.curve()}")     # 0 0 10 10

# Move v1 to a different location
new_point = Point_2(5, 0)
arr.modify_vertex(v1, new_point)

print(f"\nAfter modify_vertex:")
print(f"  v1.point() = {v1.point()}")  # 5 0 ← MOVED
print(f"  Edge curve: {he.curve()}")   # 0 0 10 10 ← UNCHANGED!

# ⚠️ Result: GEOMETRIC INCONSISTENCY
# Vertex is now at (5,0) but edge curve still says it starts at (0,0)
# The arrangement is now geometrically INVALID
# Point location queries will give wrong answers
# Intersections will be computed incorrectly
```

### Required Follow-Up (What You Must Do)

```python
# To maintain consistency after modify_vertex:
arr.modify_vertex(v1, new_point)
new_curve = Segment_2(new_point, v2.point())
arr.modify_edge(he, new_curve)

# Now vertex position and curve endpoints match again
```

**User Impact**: Forgetting to update curves leads to arrangements where vertex positions don't match curve endpoints. This breaks all geometric queries and algorithms. The arrangement will look correct when traversing topology but give wrong answers for anything involving geometry.

---

## Method 4: `modify_edge(halfedge, new_curve)`

### C++ Signature

```cpp
void modify_edge(Halfedge_handle e, const X_monotone_curve_2& c)
```

### What It Does

Changes the curve associated with edge `e` to `new_curve`. But again—**it does NOT verify** that the new curve endpoints match the vertex positions.

### Python Signature

```python
arr.modify_edge(halfedge, new_curve)
```

No return value.

### DCEL Changes

```
Before                  After
------                  -----
Edge curve: old_curve → Edge curve: new_curve
Topology: unchanged   → Topology: unchanged
Vertex positions: unchanged → Vertex positions: UNCHANGED
```

### Preconditions (from C++ docs)

1. ✅ `new_curve.source()` should equal `e.source().point()`
2. ✅ `new_curve.target()` should equal `e.target().point()`
3. ✅ New curve interior should not intersect other edges

### Validation Status: ❌ **NONE**

### ⚠️ Test Results: Curve Doesn't Match Vertices

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(10, 10), arr.unbounded_face())
he = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(10, 10)), v1, v2)

print(f"Original curve: {he.curve()}")                    # 0 0 10 10
print(f"Vertices: {v1.point()} and {v2.point()}")        # (0,0) and (10,10)

# Try to change to a curve that doesn't match vertices:
bad_curve = Segment_2(Point_2(0, 0), Point_2(5, 5))  # Doesn't reach v2!

print(f"\nTrying to set curve to: (0,0) → (5,5)")
print(f"But vertex v2 is at: {v2.point()}")  # 10 10

arr.modify_edge(he, bad_curve)
print(f"Modified curve: {he.curve()}")  # 0 0 5 5

# ⚠️ Result: NO VALIDATION - accepts curve that doesn't match vertices!
# Edge connects (0,0)→(10,10) but curve says (0,0)→(5,5)
# Geometric inconsistency - this breaks everything
```

**User Impact**: Arrangements can have edges where the curve geometry doesn't match the vertex positions. This causes incorrect results in geometric queries and makes the arrangement unusable for any real computation.

---

## Summary

| Method | Crash Risk | Corruption Risk | Main Danger |
|--------|------------|-----------------|-------------|
| `split_edge` | Low | 🔴 High | Accepts wrong split points, creates duplicate vertices |
| `merge_edge` | 🔴 **SEGFAULT** | 🔴 High | Crashes on non-adjacent edges, crashes accessing deleted vertex |
| `modify_vertex` | Low | 🔴 High | Creates vertex↔curve inconsistency (vertex position ≠ curve endpoint) |
| `modify_edge` | Low | 🔴 High | Accepts curves that don't match vertex positions |

**Common Pattern**: All modification methods trust the user completely. No validation means:
- Easy to create invalid arrangements
- Debugging is extremely difficult (corruption is silent)
- Geometric queries give wrong answers
- Python users expect better safety

---

**Previous**: [← Part C - Removal Methods](./part-c-removal-methods.md)  
**Next**: [Part E - Query Methods →](./part-e-query-methods.md)
