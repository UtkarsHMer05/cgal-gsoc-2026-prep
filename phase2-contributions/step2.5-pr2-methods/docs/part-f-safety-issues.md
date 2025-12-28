# Part F: Critical Safety Issues

**Comprehensive list of everything that can go wrong, organized by severity**

---

## The Core Problem

CGAL was written in C++ for C++ programmers. The design philosophy is explicitly documented:

> "The specialized insertion functions are provided for additional flexibility. They do not check their preconditions, in order to achieve maximal efficiency." — CGAL Manual

This makes perfect sense in C++:
- C++ programmers are trained to read documentation thoroughly
- Undefined behavior is an accepted concept
- Performance is often critical
- The type system catches some errors at compile-time

In Python, this creates severe problems:
- Python programmers expect **exceptions** when something goes wrong
- Segmentation faults are considered **unacceptable**
- Dynamic typing makes mistakes easier
- No compile-time safety net

---

## Category 1: Python Interpreter Crashes (5 Scenarios)

These scenarios will **kill your Python interpreter entirely**. Not catchable exceptions—the process just dies with a segmentation fault (SIGSEGV) or bus error (SIGBUS). Your work is lost.

### Crash #1: `remove_isolated_vertex()` on Non-Isolated Vertex

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
he = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(5, 5)), v1, v2)

print(f"v1.is_isolated() = {v1.is_isolated()}")  # False
print(f"v1.degree() = {v1.degree()}")            # 1

arr.remove_isolated_vertex(v1)  # v1 is NOT isolated!

# OUTPUT:
# zsh: bus error  python test.py
```

**Why it crashes**: The method directly accesses DCEL structures assuming the vertex is isolated. When it's not, it accesses invalid memory.

**Prevention**: ALWAYS check `v.is_isolated()` before calling.

---

### Crash #2: `remove_edge()` Called Twice on Same Handle

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
he = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(5, 5)), v1, v2)

arr.remove_edge(he)  # First removal - OK
arr.remove_edge(he)  # Second removal - he is now INVALID

# OUTPUT:
# zsh: segmentation fault  python test.py
```

**Why it crashes**: After first removal, `he` points to freed memory. Second removal tries to access/modify freed memory.

**Prevention**: Set handles to `None` after removal; never reuse.

---

### Crash #3: `merge_edge()` on Non-Adjacent Edges

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
v3 = arr.insert_in_face_interior(Point_2(10, 0), arr.unbounded_face())
v4 = arr.insert_in_face_interior(Point_2(15, 5), arr.unbounded_face())

he1 = arr.insert_at_vertices(seg1, v1, v2)
he2 = arr.insert_at_vertices(seg2, v3, v4)  # NOT adjacent to he1!

merged_curve = Segment_2(Point_2(0, 0), Point_2(15, 5))
arr.merge_edge(he1, he2, merged_curve)

# OUTPUT:
# zsh: segmentation fault  python test.py
```

**Why it crashes**: The method assumes edges share a vertex. When they don't, it follows invalid pointers.

**Prevention**: Verify `he1.target() == he2.source()` before calling.

---

### Crash #4: Accessing Deleted Vertex After `merge_edge()`

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
v3 = arr.insert_in_face_interior(Point_2(10, 10), arr.unbounded_face())

he1 = arr.insert_at_vertices(seg1, v1, v2)
he2 = arr.insert_at_vertices(seg2, v2, v3)

merged_curve = Segment_2(Point_2(0, 0), Point_2(10, 10))
arr.merge_edge(he1, he2, merged_curve)  # v2 is DELETED

v2.point()  # Accessing deleted vertex

# OUTPUT:
# zsh: segmentation fault  python test.py
```

**Why it crashes**: After merge, v2's memory is freed. Accessing it reads freed memory.

**Prevention**: Discard handles to shared vertex after merge.

---

### Crash #5: Accessing Deleted Halfedge After `remove_edge()`

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
he = arr.insert_at_vertices(seg, v1, v2)

arr.remove_edge(he)  # he is now DELETED

he.source()  # Accessing deleted halfedge

# OUTPUT:
# zsh: segmentation fault  python test.py
```

**Why it crashes**: Halfedge memory is freed immediately on removal.

**Prevention**: Never access halfedge handle after removal.

---

## Category 2: Silent Data Corruption (10+ Scenarios)

These scenarios create invalid arrangements without any error message. The corruption is silent—you won't know until later operations fail mysteriously.

### Corruption #1: Duplicate Points

```python
v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
v2 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)  # SAME POINT!

print(arr.number_of_vertices())  # 2 - BOTH created
# ⚠️ Two vertices at identical coordinates - violates DCEL invariant
```

---

### Corruption #2: Mismatched Curve Endpoints (Insertion)

```python
v_left = arr.insert_in_face_interior(Point_2(10, 10), unbounded)
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))  # Starts at (0,0), not (10,10)!

he = arr.insert_from_left_vertex(seg, v_left)
# ⚠️ Edge created with vertex at (10,10) but curve claiming (0,0) start
```

---

### Corruption #3: Overlapping Segments

```python
seg1 = Segment_2(Point_2(0, 0), Point_2(5, 5))
he1 = arr.insert_in_face_interior(seg1, unbounded)

seg2 = Segment_2(Point_2(2, 2), Point_2(7, 7))  # OVERLAPS seg1!
he2 = arr.insert_in_face_interior(seg2, unbounded)
# ⚠️ Overlapping edges in plane - violates arrangement properties
```

---

### Corruption #4: Duplicate Edges

```python
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he1 = arr.insert_at_vertices(seg, v1, v2)  # First edge
he2 = arr.insert_at_vertices(seg, v1, v2)  # DUPLICATE!

print(arr.number_of_edges())  # 2 - both created
# ⚠️ Two edges between same vertices - corrupts DCEL twins
```

---

### Corruption #5: Non-Isolated Vertices in `insert_at_vertices`

```python
# After creating edge v1-v2:
print(v1.is_isolated())  # False

# Use v1 again:
he2 = arr.insert_at_vertices(seg2, v1, v3)
# ⚠️ Method may not handle non-isolated vertices correctly
```

---

### Corruption #6: Wrong Split Point

```python
# Original edge: (0,0) → (10,10)
bad_c1 = Segment_2(Point_2(0, 0), Point_2(3, 3))  # Wrong midpoint
bad_c2 = Segment_2(Point_2(3, 3), Point_2(10, 10))

arr.split_edge(he, bad_c1, bad_c2)
# ⚠️ Creates vertex at wrong position relative to original geometry
```

---

### Corruption #7: Degenerate Split at Endpoint

```python
# Try to "split" at endpoint with zero-length segment:
c1 = Segment_2(Point_2(0, 0), Point_2(0, 0))  # Zero-length!
c2 = Segment_2(Point_2(0, 0), Point_2(10, 10))

arr.split_edge(he, c1, c2)
# ⚠️ Creates duplicate vertex at endpoint
```

---

### Corruption #8: Wrong Merged Curve

```python
# Edges: (0,0)→(5,5) and (5,5)→(10,10)
wrong_curve = Segment_2(Point_2(0, 0), Point_2(8, 8))  # Wrong endpoint!

arr.merge_edge(he1, he2, wrong_curve)
# ⚠️ Merged edge geometry doesn't match vertex positions
```

---

### Corruption #9: Vertex Position ≠ Curve Endpoint

```python
arr.modify_vertex(v1, Point_2(5, 0))  # Move vertex

# But edge curve still says original position!
print(he.curve())  # Still shows old (0,0) endpoint
# ⚠️ Vertex position doesn't match curve endpoint
```

---

### Corruption #10: Curve Doesn't Match Vertices

```python
bad_curve = Segment_2(Point_2(0, 0), Point_2(5, 5))  # Wrong endpoint
arr.modify_edge(he, bad_curve)

# Curve says (0,0)→(5,5) but edge connects different vertices
# ⚠️ Geometric inconsistency
```

---

## Category 3: Dangling Handle Problem

### The Root Cause

Python handles use `reference_internal` lifetime policy in nanobind. This means:
- Handle stays alive as long as arrangement exists
- Python GC doesn't know when DCEL elements are deleted
- Handles can become invalid while still being valid Python objects

### Example of the Problem

```python
arr = Arrangement_2()  # Arrangement created
v1 = arr.insert_in_face_interior(Point_2(0, 0), face)  # v1 handle created
he = arr.insert_at_vertices(seg, v1, v2)  # he handle created
arr.remove_edge(he)  # DCEL elements deleted

# At this point:
# - arr is still alive
# - v1, he are still valid Python objects (GC hasn't collected them)
# - BUT v1, he point to FREED MEMORY

v1.degree()  # Returns garbage or crashes
he.source()  # Crashes immediately
```

### Why Python GC Can't Help

```
Python's Perspective:
  arr exists → keeps v1, he alive
  v1 exists → valid Python object
  he exists → valid Python object
  
Reality:
  arr exists ✓
  v1's underlying C++ Vertex → FREED
  he's underlying C++ Halfedge → FREED
  
GC sees valid objects → doesn't collect
But objects point to freed memory → undefined behavior
```

### Required Pattern

```python
he = arr.insert_at_vertices(seg, v1, v2)
face = arr.remove_edge(he)

# MUST discard handles:
he = None
v1 = None
v2 = None

# Now you can't accidentally use them
# Python raises NameError instead of crashing
```

---

## Category 4: Missing API Features

### Missing #1: `remove_edge` Optional Parameters

**C++ API**:
```cpp
Face_handle remove_edge(Halfedge_handle e, 
                        bool remove_source = true, 
                        bool remove_target = true);
```

**Python API**:
```python
face = arr.remove_edge(halfedge)  # No optional parameters!
```

**Impact**: Cannot control vertex removal. Vertices are always auto-deleted when they become isolated.

---

### Missing #2: Face Iterators

**C++ API**:
```cpp
Ccb_halfedge_circulator holes_begin();
Ccb_halfedge_circulator holes_end();
Isolated_vertex_iterator isolated_vertices_begin();
Isolated_vertex_iterator isolated_vertices_end();
```

**Python API**: Methods not bound.

**Impact**: Cannot iterate over holes or isolated vertices within a specific face.

---

## Summary Table

| Issue | Type | Can Try/Catch? | Debugging Difficulty |
|-------|------|----------------|---------------------|
| Non-isolated vertex removal | 🔴 CRASH | ❌ No | Easy (clear cause) |
| Double edge removal | 🔴 CRASH | ❌ No | Medium |
| Non-adjacent merge | 🔴 CRASH | ❌ No | Medium |
| Deleted vertex access | 🔴 CRASH | ❌ No | Hard (delayed) |
| Deleted halfedge access | 🔴 CRASH | ❌ No | Hard (delayed) |
| Duplicate points | ⚠️ CORRUPT | N/A | Very Hard |
| Mismatched endpoints | ⚠️ CORRUPT | N/A | Very Hard |
| Overlapping segments | ⚠️ CORRUPT | N/A | Very Hard |
| Wrong split/merge | ⚠️ CORRUPT | N/A | Very Hard |
| Vertex/curve mismatch | ⚠️ CORRUPT | N/A | Very Hard |

---

**Previous**: [← Part E - Query Methods](./part-e-query-methods.md)  
**Next**: [Part G - Patterns and Design Philosophy →](./part-g-patterns.md)
