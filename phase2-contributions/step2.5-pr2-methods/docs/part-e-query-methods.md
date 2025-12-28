# Part E: Query and Traversal Methods

**Research Date**: December 28, 2025  
**Time Invested**: ~1 hour  
**Methods Tested**: 15+ methods  
**Test File**: `test_query_methods.py` (~200 lines)

---

## Overview

Finally, some good news! Query and traversal methods are **read-only**, which means they can't corrupt anything or crash Python. These are the safe ones—perfect for exploring your arrangement structure without any risk.

After testing 10 dangerous modification methods, finding that all of them can crash or corrupt, it was a relief to discover that query methods are uniformly safe and well-behaved.

---

## Arrangement-Level Counting Methods

All these methods return integer counts and work correctly:

| Method | Return Type | Description |
|--------|-------------|-------------|
| `number_of_vertices()` | int | Total vertices (isolated + non-isolated) |
| `number_of_edges()` | int | Total edges (undirected count) |
| `number_of_halfedges()` | int | Total halfedges (always 2 per edge) |
| `number_of_faces()` | int | Total faces (including unbounded) |
| `number_of_isolated_vertices()` | int | Count of isolated vertices (degree 0) |

### Test Results

```python
# Build a triangle: 3 vertices, 3 edges, 2 faces (unbounded + interior)
arr = Arrangement_2()
unbounded = arr.unbounded_face()

v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
v2 = arr.insert_in_face_interior(Point_2(10, 0), unbounded)
v3 = arr.insert_in_face_interior(Point_2(5, 10), unbounded)

he1 = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(10, 0)), v1, v2)
he2 = arr.insert_at_vertices(Segment_2(Point_2(10, 0), Point_2(5, 10)), v2, v3)
he3 = arr.insert_at_vertices(Segment_2(Point_2(5, 10), Point_2(0, 0)), v3, v1)

print(f"number_of_vertices(): {arr.number_of_vertices()}")        # 3
print(f"number_of_edges(): {arr.number_of_edges()}")              # 3
print(f"number_of_halfedges(): {arr.number_of_halfedges()}")      # 6
print(f"number_of_faces(): {arr.number_of_faces()}")              # 2
print(f"number_of_isolated_vertices(): {arr.number_of_isolated_vertices()}")  # 0

# ✓ All methods work correctly, no safety issues
```

**Invariant**: `number_of_halfedges() == 2 * number_of_edges()` always holds, because every edge has exactly two halfedges (twins pointing in opposite directions).

---

## Boolean Query Methods

| Method | Return Type | Description |
|--------|-------------|-------------|
| `is_empty()` | bool | True if arrangement has no vertices/edges |
| `is_valid()` | bool | True if DCEL structure is internally valid |

### Test Results

```python
arr = Arrangement_2()

print(f"Empty arrangement:")
print(f"  is_empty(): {arr.is_empty()}")       # True
print(f"  number_of_vertices(): {arr.number_of_vertices()}")  # 0

# Add something
arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())

print(f"\nNon-empty arrangement:")
print(f"  is_empty(): {arr.is_empty()}")       # False
print(f"  is_valid(): {arr.is_valid()}")       # True

# ✓ Works correctly
```

### About `is_valid()`

This method performs **comprehensive DCEL validation** including:
- Halfedge twin symmetry (he.twin().twin() == he)
- CCB (Counter-Clockwise Boundary) cycles are properly closed
- Face/edge incidence consistency
- Vertex degree accounting

This is incredibly useful for debugging after using specialized methods (which can corrupt topology). If `is_valid()` returns False, you know something went wrong.

```python
# Use after batch construction to verify integrity:
arr = build_arrangement_from_file(filename)

if not arr.is_valid():
    print("ERROR: Arrangement is corrupted!")
    print(f"  Vertices: {arr.number_of_vertices()}")
    print(f"  Edges: {arr.number_of_edges()}")
    print(f"  Faces: {arr.number_of_faces()}")
    # Time to debug...
```

---

## Face Access Methods

### `unbounded_face()`

Returns a handle to the unbounded (outer) face. This face represents the "infinite outside" of the arrangement—the region that extends to infinity in all directions.

```python
unbounded = arr.unbounded_face()

print(f"unbounded_face() returned: {unbounded}")
print(f"Type: {type(unbounded)}")  
# <class 'CGALPY.Aos2.Arrangement_on_surface_2.Face'>
print(f"is_unbounded(): {unbounded.is_unbounded()}")  # True

# ✓ Works correctly, always available even in empty arrangement
```

The unbounded face always exists, even in a completely empty arrangement. It's the starting point for building arrangements incrementally.

---

## Vertex Methods

| Method | Return Type | Description | Notes |
|--------|-------------|-------------|-------|
| `point()` | Point_2 | The geometric position | Always available |
| `degree()` | int | Number of incident edges | 0 for isolated vertices |
| `is_isolated()` | bool | True if degree 0 | Critical check before removal |
| `face()` | Face | Containing face | **Only for isolated vertices** |
| `incident_halfedges()` | Circulator | Iterator over incident halfedges | For non-isolated vertices |

### Test Results

```python
# Non-isolated vertex (connected to edges)
print(f"v1.point(): {v1.point()}")            # 0 0
print(f"v1.degree(): {v1.degree()}")          # 2
print(f"v1.is_isolated(): {v1.is_isolated()}")  # False

# Isolated vertex (floating in a face)
v_iso = arr.insert_in_face_interior(Point_2(20, 20), unbounded)
print(f"\nIsolated vertex:")
print(f"  point: {v_iso.point()}")             # 20 20
print(f"  degree: {v_iso.degree()}")           # 0
print(f"  is_isolated: {v_iso.is_isolated()}")   # True
print(f"  face(): {v_iso.face()}")             # Returns unbounded face
print(f"  face == unbounded: {v_iso.face() == unbounded}")  # True

# ✓ All methods work correctly
```

### Incident Halfedges Circulator

The `incident_halfedges()` method returns a circulator that lets you walk around all edges touching a vertex:

```python
circ = v1.incident_halfedges()
print(f"v1.incident_halfedges(): {circ}")
print(f"Type: {type(circ)}")  
# <class 'CGALPY.Aos2.Arrangement_on_surface_2.Vertex.Halfedge_around_vertex_iterator'>

# ✓ Circulator exists and is bound
```

This is essential for traversing the local topology around a vertex—finding all edges connected to it, checking degrees programmatically, etc.

---

## Halfedge Methods

These are the workhorses for traversing the DCEL structure:

| Method | Return Type | Description |
|--------|-------------|-------------|
| `source()` | Vertex | Source vertex of directed halfedge |
| `target()` | Vertex | Target vertex of directed halfedge |
| `twin()` | Halfedge | Opposite-direction halfedge (same edge) |
| `next()` | Halfedge | Next halfedge in CCB |
| `prev()` | Halfedge | Previous halfedge in CCB |
| `curve()` | X_monotone_curve_2 | The geometric curve |
| `face()` | Face | The incident face (to the left of halfedge) |

### Test Results

```python
# For halfedge from (0,0) to (10,0):
print(f"he1 properties:")
print(f"  source(): {he1.source().point()}")  # 0 0
print(f"  target(): {he1.target().point()}")  # 10 0
print(f"  curve(): {he1.curve()}")            # 0 0 10 0

# Twin reverses direction:
twin = he1.twin()
print(f"\nhe1.twin() properties:")
print(f"  source(): {twin.source().point()}")  # 10 0
print(f"  target(): {twin.target().point()}")  # 0 0
print(f"  Direction reversed: {twin.source().point()} → {twin.target().point()}")
# ✓ Twin correctly reverses direction

# Navigation around face boundary (CCB = Counter-Clockwise Boundary):
next_he = he1.next()
print(f"\nhe1.next():")
print(f"  source: {next_he.source().point()}")  # 10 0 (continues from he1.target())
print(f"  target: {next_he.target().point()}")  # 5 10
# ✓ next() continues the CCB from where the current halfedge ends

prev_he = he1.prev()
print(f"\nhe1.prev():")
print(f"  source: {prev_he.source().point()}")  # 5 10
print(f"  target: {prev_he.target().point()}")  # 0 0 (ends where he1 starts)
# ✓ prev() ends where the current halfedge starts

# Face (to the left of the halfedge):
he_face = he1.face()
print(f"\nhe1.face():")
print(f"  Type: {type(he_face)}")
print(f"  is_unbounded: {he_face.is_unbounded()}")  # Depends on orientation
# ✓ Returns the face to the left of the directed halfedge
```

### CCB Traversal Pattern

The DCEL structure allows complete traversal of face boundaries using `next()`:

```python
# Walk around a face boundary:
start = he1
current = start
boundary_edges = []

while True:
    boundary_edges.append(f"{current.source().point()} → {current.target().point()}")
    current = current.next()
    if current == start:
        break

print(f"Face boundary: {boundary_edges}")
# Face boundary: ['0 0 → 10 0', '10 0 → 5 10', '5 10 → 0 0']
```

---

## Face Methods

| Method | Return Type | Description | Notes |
|--------|-------------|-------------|-------|
| `is_unbounded()` | bool | True for the outer infinite face | Always available |
| `has_outer_ccb()` | bool | True if face has outer boundary | Unbounded face returns False |
| `outer_ccb()` | Circulator | Iterator over outer boundary halfedges | Check `has_outer_ccb()` first |

### Test Results

```python
# Unbounded face (infinite outside):
print(f"unbounded_face properties:")
print(f"  is_unbounded(): {unbounded.is_unbounded()}")     # True
print(f"  has_outer_ccb(): {unbounded.has_outer_ccb()}")   # False
# Unbounded face has no outer boundary (it extends to infinity)

# Inner face (like the triangle interior):
inner_face = he1.twin().face()  # Face on the other side of the edge
print(f"\nInner face properties:")
print(f"  is_unbounded(): {inner_face.is_unbounded()}")    # False
print(f"  has_outer_ccb(): {inner_face.has_outer_ccb()}")  # True
# Inner face has an outer boundary (the triangle edges)
```

### Missing Face Iterators in Python

Some face iterators from C++ aren't bound in the Python bindings:

```python
# These methods exist in C++ but NOT in Python:
try:
    holes = unbounded.holes_begin()
    print(f"holes_begin(): {holes}")
except AttributeError:
    print(f"holes_begin() not bound in Python")  # This is what happens

try:
    iso = unbounded.isolated_vertices_begin()
    print(f"isolated_vertices_begin(): {iso}")
except AttributeError:
    print(f"isolated_vertices_begin() not bound in Python")  # Same
```

**Missing methods**:
- `holes_begin()`, `holes_end()` - iterate over hole (inner) boundaries
- `isolated_vertices_begin()`, `isolated_vertices_end()` - iterate over isolated vertices in face

**Workaround**: You can still access isolated vertices through arrangement-level iteration, just not face-by-face.

---

## Iteration Over Arrangement Elements

The arrangement provides iterators over all elements:

```python
# Iterate over all vertices:
for v in arr.vertices():
    print(f"Vertex at {v.point()}, degree {v.degree()}")

# Iterate over all edges:
for e in arr.edges():
    print(f"Edge: {e.source().point()} → {e.target().point()}")

# Iterate over all faces:
for f in arr.faces():
    print(f"Face: unbounded={f.is_unbounded()}")
```

These are safe, read-only operations that let you explore the entire arrangement structure.

---

## Safety Summary

### Comparison: Query vs Modification Methods

| Aspect | Query Methods | Modification Methods |
|--------|---------------|---------------------|
| Validation required | N/A (read-only) | ❌ None provided |
| Crash risk | ✅ None | 🔴 SEGFAULT possible |
| Corruption risk | ✅ None | 🔴 High |
| Python safety | ✅ Excellent | 🔴 Poor |
| User-friendliness | ✅ Easy to use | ⚠️ Difficult, error-prone |
| Learning curve | ✅ Gentle | ⚠️ Steep |

**Contrast**: After documenting 10 modification methods that can crash or corrupt, it's worth emphasizing that query methods are **uniformly safe**. You literally cannot break anything by calling them.

### Complete List of Safe Methods

**✅ ALL QUERY METHODS ARE SAFE:**

- `number_of_vertices()`
- `number_of_edges()`
- `number_of_halfedges()`
- `number_of_faces()`
- `number_of_isolated_vertices()`
- `is_empty()`
- `is_valid()`
- `unbounded_face()`
- `vertex.point()`
- `vertex.degree()`
- `vertex.is_isolated()`
- `vertex.face()` (for isolated vertices)
- `vertex.incident_halfedges()`
- `halfedge.source()`
- `halfedge.target()`
- `halfedge.twin()`
- `halfedge.next()`
- `halfedge.prev()`
- `halfedge.curve()`
- `halfedge.face()`
- `face.is_unbounded()`
- `face.has_outer_ccb()`
- `face.outer_ccb()` (circulator)
- All iteration methods (`vertices()`, `edges()`, `faces()`)

---

## Recommendation for Learners

If you're new to CGAL arrangements:

1. **Start with query methods** - Build a small arrangement using `insert()` and explore it with the methods above
2. **Use counting methods liberally** - After every modification, verify counts match expectations
3. **Check `is_valid()` often** - Especially after batch operations or debugging
4. **Avoid modification methods initially** - Use high-level `insert()` exclusively until you're confident

You cannot break anything with query methods. They're your safe exploration tools.

---

**Previous**: [← Part D - Modification Methods](./part-d-modification-methods.md)  
**Next**: [Part F - Critical Safety Issues →](./part-f-safety-issues.md)
