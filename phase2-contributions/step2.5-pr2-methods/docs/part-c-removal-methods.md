# Part C: Removal Methods

**Research Date**: December 28, 2025  
**Time Invested**: ~2 hours  
**Methods Tested**: 2 methods  
**Test File**: `test_removal_methods.py` (~300 lines)

---

## Overview

Removal methods are where things get really dangerous. Unlike insertion (which at worst corrupts your data silently), removal can **crash your Python interpreter** with no warning. These aren't catchable exceptions—they're segmentation faults that kill your process, lose your data, and leave you wondering what happened.

---

## Method 1: `remove_edge(halfedge)`

### C++ Signature

```cpp
Face_handle remove_edge(Halfedge_handle e, 
                        bool remove_source = true, 
                        bool remove_target = true)
```

### Python Signature

```python
face = arr.remove_edge(halfedge)
```

⚠️ **CRITICAL ISSUE**: The Python binding does NOT expose the optional `remove_source` and `remove_target` parameters! You cannot control whether vertices get removed—they're always automatically deleted if they become isolated.

### What It Does

- Removes the edge (deletes the halfedge and its twin)
- Merges the two faces that were on either side of the edge
- **Automatically** removes source/target vertices IF they become isolated (degree 0)
- Returns the merged face handle

### Python Behavior (no optional parameters)

- Source vertex removed IF it becomes degree 0 after edge removal
- Target vertex removed IF it becomes degree 0 after edge removal
- No way to override this behavior in Python

### DCEL Changes

```
Before                  After
------                  -----
Vertices: N      →      Vertices: N - 0, -1, or -2 
                        (depends on what becomes isolated)
Edges: E         →      Edges: E - 1
Halfedges: H     →      Halfedges: H - 2
Faces: F         →      Faces: F - 1 (two merge into one)
```

### Preconditions (from C++ docs)

1. ✅ Halfedge must be a valid handle to an existing edge
2. ✅ Edge must currently exist in the arrangement

### Validation Status: ❌ **NONE**

### Test Results: Basic Removal with Auto-Delete

```python
arr = Arrangement_2()
unbounded = arr.unbounded_face()

v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
v2 = arr.insert_in_face_interior(Point_2(5, 5), unbounded)
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr.insert_at_vertices(seg, v1, v2)

print(f"Before removal:")
print(f"  Edges: {arr.number_of_edges()}")           # 1
print(f"  Vertices: {arr.number_of_vertices()}")     # 2
print(f"  v1.degree() = {v1.degree()}")              # 1
print(f"  v2.degree() = {v2.degree()}")              # 1

returned_face = arr.remove_edge(he)

print(f"\nAfter removal:")
print(f"  Edges: {arr.number_of_edges()}")           # 0
print(f"  Vertices: {arr.number_of_vertices()}")     # 0 ← BOTH REMOVED!
print(f"  Returned face == unbounded: {returned_face == unbounded}")  # True
```

**Analysis**: Both vertices had degree 1. After removing the only edge connecting them, both became isolated (degree 0), so they got auto-deleted. In C++, you could pass `remove_edge(he, false, false)` to keep them—but that option doesn't exist in Python.

### Test Results: Vertices NOT Removed (Still Have Edges)

```python
# Create a triangle
arr = Arrangement_2()
unbounded = arr.unbounded_face()

v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
v2 = arr.insert_in_face_interior(Point_2(10, 0), unbounded)
v3 = arr.insert_in_face_interior(Point_2(5, 10), unbounded)

he1 = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(10, 0)), v1, v2)
he2 = arr.insert_at_vertices(Segment_2(Point_2(10, 0), Point_2(5, 10)), v2, v3)
he3 = arr.insert_at_vertices(Segment_2(Point_2(5, 10), Point_2(0, 0)), v3, v1)

print(f"Triangle arrangement:")
print(f"  Vertices: {arr.number_of_vertices()}")  # 3
print(f"  Edges: {arr.number_of_edges()}")        # 3
print(f"  Faces: {arr.number_of_faces()}")        # 2

# Remove the bottom edge
returned_face = arr.remove_edge(he1)

print(f"\nAfter removing bottom edge:")
print(f"  Vertices: {arr.number_of_vertices()}")  # 3 ← ALL KEPT!
print(f"  Edges: {arr.number_of_edges()}")        # 2
print(f"  Faces: {arr.number_of_faces()}")        # 1
print(f"  Returned face is unbounded? {returned_face.is_unbounded()}")  # True
```

**Analysis**: After removing `he1`, v1 and v2 still have degree ≥ 1 (they're still connected to other edges in the triangle), so they were NOT removed. The automatic deletion only happens when vertices become completely isolated.

### 🔴 DANGER: Dangling Handle Access

Here's where it gets scary. After edges and vertices are deleted, the Python handles still exist but point to freed memory:

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
he = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(5, 5)), v1, v2)

# Remove edge (will auto-remove both isolated vertices)
arr.remove_edge(he)

print(f"Vertices in arrangement: {arr.number_of_vertices()}")  # 0

# Now try to access the "deleted" vertex:
print(f"⚠️ DANGLING HANDLE TEST:")
print(f"v1.degree() = {v1.degree()}")  # Returns 1 ← STALE DATA!

# ⚠️ Result: Handle still accessible, but returns OLD VALUE from before deletion
# This is UNDEFINED BEHAVIOR - accessing freed memory
# Python doesn't know the handle is invalid
```

**Impact**: The handle `v1` still exists as a Python object, but the underlying C++ vertex was deleted. Accessing it returns garbage data from freed memory. It might seem to work, but the data is meaningless. This is **undefined behavior** that leads to bugs that are nearly impossible to debug.

### 🔴 CRASH: Double Removal = SEGFAULT

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
he = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(5, 5)), v1, v2)

arr.remove_edge(he)  # First removal - succeeds
print(f"After first removal: {arr.number_of_edges()} edges")  # 0

arr.remove_edge(he)  # Second removal - he is now INVALID

# OUTPUT:
# zsh: segmentation fault  python test_removal_methods.py
```

**This crashes Python entirely.** Not an exception you can catch with try/except—the interpreter just dies. Your work is lost.

### Missing API Features (C++ vs Python)

```cpp
// C++ allows control over vertex removal:
arr.remove_edge(he, false, false);  // Keep both vertices even if they become isolated
arr.remove_edge(he, true, false);   // Only remove source if it becomes isolated
arr.remove_edge(he, false, true);   // Only remove target if it becomes isolated
```

```python
# Python only has:
arr.remove_edge(he)  # Always equivalent to C++ (true, true)
```

**Impact**: Python users cannot control vertex removal behavior. If you need to keep isolated vertices after edge removal, you must use workarounds (and there aren't good ones).

---

## Method 2: `remove_isolated_vertex(vertex)`

### C++ Signature

```cpp
void remove_isolated_vertex(Vertex_handle v)
```

### What It Does

Removes an isolated vertex from its face's isolated vertex list. The vertex must have degree 0 (no incident edges whatsoever).

### Python Signature

```python
arr.remove_isolated_vertex(vertex)
```

No return value.

### DCEL Changes

```
Before                  After
------                  -----
Vertices: N      →      Vertices: N - 1
Face's isolated vertex count: I → I - 1
```

### Preconditions (from C++ docs)

1. ✅ `vertex.is_isolated()` must be True
2. ✅ `vertex.degree()` must be 0

### Validation Status: ❌ **ABSOLUTELY NONE**

This is the **MOST DANGEROUS METHOD** in the entire Arrangement_2 API for Python users.

### Test Results: Safe Usage (Isolated Vertex)

```python
arr = Arrangement_2()
v = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())

print(f"Before removal:")
print(f"  Vertices: {arr.number_of_vertices()}")  # 1
print(f"  v.is_isolated() = {v.is_isolated()}")   # True

arr.remove_isolated_vertex(v)

print(f"After removal:")
print(f"  Vertices: {arr.number_of_vertices()}")  # 0

# ✓ Safe removal succeeded
```

### 🔴 CRITICAL TEST: Non-Isolated Vertex = INSTANT CRASH

This is not an exaggeration—this will kill your Python interpreter immediately:

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
he = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(5, 5)), v1, v2)

print(f"v1.is_isolated() = {v1.is_isolated()}")  # False
print(f"v1.degree() = {v1.degree()}")            # 1

print("About to call remove_isolated_vertex on non-isolated vertex...")
arr.remove_isolated_vertex(v1)  # v1 is NOT isolated!

# OUTPUT:
# zsh: bus error  python test_removal_methods.py
```

**Result**: INSTANT BUS ERROR (a type of segmentation fault). NOT a Python exception—crashes the entire interpreter. No try/except can catch this. Your work is gone.

**Analysis**: The method performs **ZERO validation**. It directly accesses internal DCEL structures assuming the vertex is isolated. When it's not, accessing non-existent data structures causes immediate memory access violation.

### Required Usage Pattern (100% Mandatory)

```python
# ✓ CORRECT - always check first
if vertex.is_isolated():
    arr.remove_isolated_vertex(vertex)
else:
    print("Error: Vertex has incident edges, cannot remove")

# ✗ WRONG - will crash if vertex has edges
arr.remove_isolated_vertex(vertex)  # DANGEROUS!
```

### Why This Violates Python Expectations

| Aspect | C++ Expectation | Python Expectation |
|--------|-----------------|-------------------|
| Invalid input | Undefined behavior (documented) | Exception raised |
| Crash on error | Acceptable (programmer's fault) | Unacceptable (interpreter should catch) |
| Precondition checking | Manual, before calling | Runtime, by the function |
| Memory access errors | Expected for bugs | Should never happen |

Python's safety contract says that even bad input should result in an exception, not a crash. This method violates that contract.

---

## Handle Lifetime Issues

Both removal methods create **dangling reference** problems that Python's garbage collector cannot solve.

### Problem 1: Deleted Vertex Handles

After `remove_edge()` removes vertices, the old Python handles still exist but point to freed memory:

```python
v1 = arr.insert_in_face_interior(Point_2(0, 0), face)
he = arr.insert_at_vertices(seg, v1, v2)
arr.remove_edge(he)  # v1 gets deleted (became isolated)

# v1 is now a dangling handle
v1.degree()  # Returns garbage or crashes
```

### Problem 2: Deleted Halfedge Handles

Accessing removed halfedges crashes immediately:

```python
he = arr.insert_at_vertices(seg, v1, v2)
arr.remove_edge(he)  # he is deleted

he.source()  # SEGFAULT - instant crash
```

### Problem 3: Python GC Cannot Help

Handles use `reference_internal` lifetime policy in nanobind—they remain alive as long as the arrangement exists. But the underlying DCEL elements can be deleted while the arrangement (and its handles) still exist.

```python
# This is the trap:
arr = Arrangement_2()  # Arrangement alive
v1 = arr.insert_in_face_interior(...)  # v1 handle created
he = arr.insert_at_vertices(...)  # he handle created
arr.remove_edge(he)  # DCEL elements deleted, but handles still exist

# arr is still alive, so Python keeps v1 and he alive
# But v1 and he point to freed memory
# GC has no idea the handles are invalid
```

### Best Practice: Discard Handles After Removal

```python
he = arr.insert_at_vertices(seg, v1, v2)
face = arr.remove_edge(he)

# MUST NOT use he, v1, or v2 after this point!
# Set to None to prevent accidents:
he = None
v1 = None
v2 = None

# Now if you try to use them, Python raises NameError
# instead of crashing or returning garbage
```

---

## Summary

| Method | Crash Risk | Main Danger |
|--------|------------|-------------|
| `remove_edge(he)` | 🔴 If called twice on same handle | Dangling handles return stale data or crash |
| `remove_isolated_vertex(v)` | 🔴 If vertex has edges | Instant crash with no exception |

**Golden rules**:
1. Always validate before removal (`is_isolated()` for vertices)
2. Never reuse handles after removal operations
3. Set handles to `None` after removal to prevent accidents

---

**Previous**: [← Part B - Insertion Methods](./part-b-insertion-methods.md)  
**Next**: [Part D - Modification Methods →](./part-d-modification-methods.md)
