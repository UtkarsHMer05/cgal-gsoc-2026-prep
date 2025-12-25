# Research: insert_in_face_interior (Point Version)

**Date:** Dec 26, 2025, 12:31 AM IST  
**Status:** Tested and working ✅  
**Time invested:** ~2 hours (testing + analysis)

## Binding Location

**File:** `arrangement_on_surface_2_bindings.cpp`  
**Line:** 748

```cpp
.def("insert_in_face_interior",
     &aos2::insert_pnt_in_face_interior,
     ri)
```

## Current State (Before My PR)

- ❌ **No docstring** - completely undocumented
- ❌ **No parameter names** - shows `(*args, **kwargs)` in Python
- ❌ **No type hints** - users have no idea what to pass
- ❌ **No examples** - must read C++ source to understand

**Signature currently shows:**

```python
import inspect
inspect.signature(arr.insert_in_face_interior)
# (*args, **kwargs)
```

This is exactly what Efi was complaining about!

## What This Method Does

Creates a **new isolated vertex** at a given point location inside a specified face.

### Key Characteristics:
- The vertex starts with **degree 0** (no incident edges)
- The vertex is **isolated** (`is_isolated()` returns `True`)
- The face's isolated vertices list gets updated to include this new vertex
- This is typically the **first step** in building an arrangement incrementally

### When to Use:
- Starting a new arrangement from scratch (first vertex)
- Adding isolated points before connecting them with curves
- Incremental construction workflows

## Parameters

### Parameter 1: `point` (Point_2)
- **Type:** Point_2 (from CGALPY.Ker)
- **Purpose:** The 2D coordinates where the new vertex will be created
- **Constraint:** Must lie **strictly inside** the face (not on boundary)
- **Not validated!** ⚠️ See "Critical Discovery" below

### Parameter 2: `face` (Face handle)
- **Type:** Face (handle from Arrangement_2)
- **Purpose:** The face that will contain this isolated vertex
- **Common usage:** `arr.unbounded_face()` for initial insertions
- **Update:** Face's isolated vertices list is modified to include new vertex

## Return Value

**Type:** Vertex handle

**Properties of returned vertex:**
- `is_isolated()` → `True`
- `degree()` → `0`
- `point()` → the input point
- Has no incident halfedges yet

**Lifetime:** Valid as long as the arrangement exists (nanobind `reference_internal` policy)

## Preconditions (From C++ Documentation)

The C++ docs say:
1. The point must lie **inside** the face (not on its boundary)
2. No existing vertex should be at this point location

### ⚠️ CRITICAL DISCOVERY: NO VALIDATION!

I tested this extensively tonight. **The method does NOT check preconditions!**

**Test that proves it:**

```python
v1 = arr.insert_in_face_interior(Point_2(5, 5), unbounded)
v2 = arr.insert_in_face_interior(Point_2(5, 5), unbounded)  # SAME POINT!

print(arr.number_of_vertices())  # Output: 2 (both created!)
```

Both vertices get created at the exact same location. No error, no warning. This creates an invalid arrangement topology!

**Implication:** Users MUST validate their input before calling this method. The docstring needs a big warning about this.

## DCEL Topology Changes

**Before calling:**
- Face has N isolated vertices

**After calling:**
- Face has N+1 isolated vertices
- +1 Vertex (isolated, degree 0)
- +0 Halfedges
- +0 Edges
- +0 Faces

**Complexity:** O(1) constant time

## Test Results (Dec 26, 12:31 AM)

```python
from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Point_2

arr = Arrangement_2()
unbounded = arr.unbounded_face()

# Test 1: Basic insertion
v = arr.insert_in_face_interior(Point_2(5, 5), unbounded)
print(v.point())       # Output: 5 5 ✅
print(v.is_isolated()) # Output: True ✅
print(v.degree())      # Output: 0 ✅
```

**Result:** ✅ Works perfectly for valid input

**Test 2: Duplicate points (precondition violation)**

```python
v1 = arr.insert_in_face_interior(Point_2(5, 5), unbounded)
v2 = arr.insert_in_face_interior(Point_2(5, 5), unbounded)

print(v1.point() == v2.point())  # True - SAME LOCATION!
print(arr.number_of_vertices())   # 2 - BOTH EXIST!
```

**Result:** ⚠️ No validation - user must be careful!

## Related Methods

- `insert_from_left_vertex()` - Connect a curve FROM this vertex (left endpoint)
- `insert_from_right_vertex()` - Connect a curve TO this vertex (right endpoint)
- `remove_isolated_vertex()` - Delete this vertex (only works if still isolated)
- `number_of_isolated_vertices()` - Count isolated vertices in arrangement

## Common Mistakes to Warn About

1. **Assuming validation happens** - It doesn't! Check your preconditions.
2. **Inserting duplicate points** - Creates invalid topology silently
3. **Wrong face parameter** - Passing a bounded face when point is outside it
4. **Trying to remove non-isolated vertex** - Must use `remove_edge` first

## Nanobind Details

**Current binding:**

```cpp
.def("insert_in_face_interior",
     &aos2::insert_pnt_in_face_interior,
     ri)  // 'ri' = reference_internal policy
```

**What I need to add:**

```cpp
.def("insert_in_face_interior",
     &aos2::insert_pnt_in_face_interior,
     nb::arg("point"),   // ← Add parameter name!
     nb::arg("face"),    // ← Add parameter name!
     ri,
     R"pbdoc(
         [My docstring goes here]
     )pbdoc")
```

**Return policy:** `reference_internal` means the returned Vertex handle keeps the parent Arrangement alive. This is correct - if the Arrangement gets destroyed, the Vertex handle would dangle.

## Links to C++ Documentation

- [CGAL Arrangement_2 Reference](https://doc.cgal.org/latest/Arrangement_on_surface_2/classCGAL_1_1Arrangement__2.html)
- Search for "insert_in_face_interior" in C++ docs

## My Understanding Level

**Confidence:** 90% ✅

I tested this thoroughly, read the C++ source, and understand:
- What it does
- When to use it
- The preconditions (and lack of validation!)
- DCEL topology changes
- Nanobind lifetime semantics

**Remaining questions:**
- Should I mention face's "isolated vertices list" data structure in docstring?
- How much detail about DCEL internals is appropriate for Python users?

## Next Steps for Docstring

1. Write one-line summary: "Insert an isolated vertex at a point in face interior"
2. Extended description: Explain DCEL changes, when to use
3. **Prominent warning** about no precondition validation
4. Parameter docs with constraints clearly stated
5. Return value docs with lifetime semantics
6. Example from my test code (proven to work!)
7. Cross-references to related insertion methods
8. Notes section: preconditions, complexity, common mistakes

---

**Notes to self:**
- This was the easiest of the 3 methods to understand
- The "no validation" discovery is CRITICAL for the docstring
- Need to balance detail vs simplicity - don't overwhelm beginners
- The example must be runnable - I already tested it!