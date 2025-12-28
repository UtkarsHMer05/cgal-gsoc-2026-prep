# Specialized Insertion Methods - Complete Research

**Date:** December 27, 2025  
**Status:** ✅ Tested and documented  
**Methods Covered:** 4 low-level insertion functions  
**Test Suite:** 7 comprehensive tests

---

## 🚨 CRITICAL WARNING: These Are Low-Level, Unsafe Methods

All 4 specialized insertion methods perform **ZERO VALIDATION**. They're designed for maximum performance when you can guarantee correctness yourself. Using them incorrectly creates **CORRUPT ARRANGEMENTS** with **UNDEFINED BEHAVIOR**.

I learned this the hard way during testing—there are no friendly error messages, no exceptions thrown, nothing. You just end up with an arrangement that looks fine but has broken topology under the hood.

---

## Method 1: `insert_in_face_interior(curve, face)`

### Purpose

Insert an x-monotone curve whose endpoints do NOT correspond to existing vertices, creating a new "island" (hole) inside a face.

### Signature

```python
halfedge = arr.insert_in_face_interior(curve, face)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `curve` | X-monotone curve (e.g., `Segment_2`) | The curve to insert |
| `face` | Face handle | The face where the curve lies entirely |

### Returns

Halfedge directed **LEFT → RIGHT** (matches segment direction)

- `halfedge.source()` = left endpoint
- `halfedge.target()` = right endpoint

### Effects

| Before | After |
|--------|-------|
| Vertices: N | Vertices: N + 2 |
| Edges: E | Edges: E + 1 |
| Faces: F | Faces: F (same) |

### PRECONDITIONS ⚠️ (NOT CHECKED!)

- ✅ `curve` lies entirely inside `face`
- ✅ `curve` endpoints don't coincide with existing vertices
- ✅ `curve` interior is disjoint from all existing edges
- ✅ No overlaps with existing curves

### Test Results

```python
# ✅ CORRECT usage
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr.insert_in_face_interior(seg, unbounded_face)
# Result: Creates 2 new vertices, 1 edge

# ❌ WRONG - Overlapping segment (NOT DETECTED!)
seg2 = Segment_2(Point_2(2, 2), Point_2(7, 7))  # Overlaps first!
he2 = arr.insert_in_face_interior(seg2, unbounded_face)
# ⚠️ Creates INVALID arrangement - no error thrown!
```

---

## Method 2: `insert_from_left_vertex(curve, v_left)`

### Purpose

Insert a curve from an existing vertex corresponding to the curve's LEFT endpoint, creating one new vertex at the right end.

### Signature

```python
halfedge = arr.insert_from_left_vertex(curve, v_left)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `curve` | X-monotone curve | The curve to insert |
| `v_left` | Vertex handle | Existing vertex at curve's LEFT endpoint |

### Returns

Halfedge directed **FROM v_left → new vertex**

- `halfedge.source()` = `v_left`
- `halfedge.target()` = newly created vertex

### Effects

| Before | After |
|--------|-------|
| Vertices: N | Vertices: N + 1 |
| Edges: E | Edges: E + 1 |
| `v_left.degree()`: D | `v_left.degree()`: D + 1 |

### PRECONDITIONS ⚠️ (NOT CHECKED!)

- ✅ `curve.source() == v_left.point()` (left endpoint matches)
- ✅ `curve.target()` doesn't coincide with existing vertex
- ✅ `curve` interior is disjoint from all existing edges

### Test Results

```python
# ✅ CORRECT usage
v_left = arr.insert_in_face_interior(Point_2(0, 0), face)
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr.insert_from_left_vertex(seg, v_left)
# Result: he.source() = (0,0), he.target() = (5,5)

# ❌ WRONG - Mismatched left endpoint (NOT DETECTED!)
v_wrong = arr.insert_in_face_interior(Point_2(10, 10), face)
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))  # Doesn't start at v_wrong!
he = arr.insert_from_left_vertex(seg, v_wrong)
# ⚠️ Creates INVALID arrangement - no error thrown!
```

---

## Method 3: `insert_from_right_vertex(curve, v_right)`

### Purpose

Insert a curve from an existing vertex corresponding to the curve's RIGHT endpoint, creating one new vertex at the left end.

### Signature

```python
halfedge = arr.insert_from_right_vertex(curve, v_right)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `curve` | X-monotone curve | The curve to insert |
| `v_right` | Vertex handle | Existing vertex at curve's RIGHT endpoint |

### Returns

Halfedge directed **FROM v_right → new vertex** ⚠️ **REVERSED from segment direction!**

- `halfedge.source()` = `v_right`
- `halfedge.target()` = newly created vertex

### Effects

| Before | After |
|--------|-------|
| Vertices: N | Vertices: N + 1 |
| Edges: E | Edges: E + 1 |
| `v_right.degree()`: D | `v_right.degree()`: D + 1 |

### PRECONDITIONS ⚠️ (NOT CHECKED!)

- ✅ `curve.target() == v_right.point()` (right endpoint matches)
- ✅ `curve.source()` doesn't coincide with existing vertex
- ✅ `curve` interior is disjoint from all existing edges

### 🔥 CRITICAL: Return Value is REVERSED!

This tripped me up during testing. The halfedge comes back pointing the opposite way from what you might expect:

```python
# Example demonstrating the reversal:
v_right = arr.insert_in_face_interior(Point_2(5, 5), face)
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))  # LEFT→RIGHT
he = arr.insert_from_right_vertex(seg, v_right)

# Segment direction:  (0,0) → (5,5)
# Halfedge direction: (5,5) → (0,0)  ← REVERSED!
```

### Test Results

```python
# ✅ CORRECT usage
v_right = arr.insert_in_face_interior(Point_2(5, 5), face)
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr.insert_from_right_vertex(seg, v_right)
# Result: he.source() = (5,5), he.target() = (0,0) ← REVERSED!

# ❌ WRONG - Mismatched right endpoint (NOT DETECTED!)
v_wrong = arr.insert_in_face_interior(Point_2(10, 10), face)
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))  # Doesn't end at v_wrong!
he = arr.insert_from_right_vertex(seg, v_wrong)
# ⚠️ Creates INVALID arrangement - no error thrown!
```

---

## Method 4: `insert_at_vertices(curve, v1, v2)`

### Purpose

Connect two existing vertices with a curve, creating no new vertices. This is useful when you already have both endpoints and just need to draw the edge between them.

### Signature

```python
halfedge = arr.insert_at_vertices(curve, v1, v2)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `curve` | X-monotone curve | The curve connecting the vertices |
| `v1` | Vertex handle | Existing vertex (LEFT endpoint) |
| `v2` | Vertex handle | Existing vertex (RIGHT endpoint) |

### Returns

Halfedge directed **v1 → v2** (first parameter to second)

- `halfedge.source()` = `v1`
- `halfedge.target()` = `v2`

### Effects

| Before | After |
|--------|-------|
| Vertices: N | Vertices: N (unchanged) |
| Edges: E | Edges: E + 1 |
| `v1.degree()`: D1 | `v1.degree()`: D1 + 1 |
| `v2.degree()`: D2 | `v2.degree()`: D2 + 1 |
| `v1.is_isolated()`: ? | `v1.is_isolated()`: False |
| `v2.is_isolated()`: ? | `v2.is_isolated()`: False |

### PRECONDITIONS ⚠️ (NOT CHECKED!)

- ✅ `curve.source() == v1.point()` (left endpoint matches v1)
- ✅ `curve.target() == v2.point()` (right endpoint matches v2)
- ✅ No edge already exists between v1 and v2
- ✅ `curve` interior is disjoint from all existing edges

### Test Results

```python
# ✅ CORRECT usage
v1 = arr.insert_in_face_interior(Point_2(0, 0), face)
v2 = arr.insert_in_face_interior(Point_2(5, 5), face)
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))  # Matches exactly!
he = arr.insert_at_vertices(seg, v1, v2)
# Result: he.source() = (0,0), he.target() = (5,5)

# ❌ WRONG - Mismatched endpoints (NOT DETECTED!)
v1 = arr.insert_in_face_interior(Point_2(0, 0), face)
v2 = arr.insert_in_face_interior(Point_2(5, 5), face)
seg = Segment_2(Point_2(0, 0), Point_2(10, 10))  # Goes beyond v2!
he = arr.insert_at_vertices(seg, v1, v2)
# ⚠️ Creates INVALID arrangement - no error thrown!

# ❌ WRONG - Duplicate edge (NOT DETECTED!)
he1 = arr.insert_at_vertices(seg, v1, v2)  # First insertion
he2 = arr.insert_at_vertices(seg, v1, v2)  # DUPLICATE!
# ⚠️ Corrupts DCEL structure - no error thrown!
```

---

## 📊 Comparison Table

| Method | New Vertices | New Edges | Return Direction | Validation |
|--------|--------------|-----------|------------------|------------|
| `insert_in_face_interior` | +2 | +1 | LEFT → RIGHT | ❌ None |
| `insert_from_left_vertex` | +1 | +1 | v_left → new | ❌ None |
| `insert_from_right_vertex` | +1 | +1 | v_right → new ⚠️ | ❌ None |
| `insert_at_vertices` | 0 | +1 | v1 → v2 | ❌ None |

---

## ✅ When to Use These Methods

### Safe Use Cases:

- **Batch construction** - Building arrangement from pre-validated data
- **File I/O** - Loading arrangements from trusted sources
- **Performance-critical** - When validation overhead is prohibitive
- **Algorithmic construction** - When you've already computed all intersections yourself

### ❌ When NOT to Use:

- **User input** - Always use high-level `insert()` functions instead
- **Interactive editing** - Risk of corruption is too high
- **Uncertain topology** - Let CGAL handle the complexity for you
- **Learning/prototyping** - Stick with safe methods until you're confident

---

## 🛡️ Safe Alternative: High-Level Insertion

If you're not sure whether you need the performance of specialized methods, use the free function `insert()` instead. It handles all the validation automatically:

```python
from CGAL.Arrangement_2 import insert

# Safe - handles all validation automatically
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
insert(arr, seg)  # Automatically finds location, handles intersections

# Or with a point location strategy for better performance
from CGAL.Arrangement_2 import Arr_naive_point_location
pl = Arr_naive_point_location(arr)
insert(arr, seg, pl)
```

---

## 🎓 Key Takeaways

1. **All 4 methods are UNSAFE** - zero validation, period
2. **Return value pattern:** Always returns halfedge FROM the "source" vertex
3. **`insert_from_right_vertex` is REVERSED** - this catches people off guard
4. **Use high-level `insert()` unless you have a compelling reason not to**
5. **If you must use specialized methods:** Validate everything yourself before calling!

---

**Empirically tested:** December 27, 2025  
**CGAL Version:** Latest Python bindings  
**Test suite:** 7 comprehensive tests covering all edge cases
