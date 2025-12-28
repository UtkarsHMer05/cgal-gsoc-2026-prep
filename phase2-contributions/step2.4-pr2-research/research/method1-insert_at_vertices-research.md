# Research: insert_at_vertices Method

**Date:** Dec 27, 2025  
**Status:** 🔍 Research in progress  
**Time Started:** [your time]

---

## Binding Location

**File:** `arrangement_on_surface_2_bindings.cpp`  
**Lines:** [find them - search for "insert_at_vertices"]

**Current state:**
.definsertatvertices, aos2::insertatvertices1, ri
.definsertatvertices, aos2::insertatvertices2, ri
.definsertatvertices, aos2::insertatvertices3, ri
.definsertatvertices, aos2::insertatvertices4, ri

text

**Issues:**
- ❌ No docstrings
- ❌ No py::arg() names
- ❌ Shows as (*args, **kwargs)

---

## What I Think It Does (BEFORE testing)

[Write YOUR expectation here - what do you think this method does based on the name?]

---

## C++ Documentation Research

**CGAL Manual URL:** https://doc.cgal.org/latest/Arrangement_on_surface_2/classArrangement__2.html#a...

[Go read the official C++ docs and summarize in YOUR words:]

**Summary:**
- 

**Preconditions:**
- 

**Postconditions:**
- 

**Complexity:**
- 

---

## C++ Source Code Analysis

**File:** `CGAL/Arrangement_2.h`

[Optional - if you want to dig deeper, read the C++ implementation]

---

## Python Testing Session

**Date/Time:** [when you run tests]

### Test 1: Basic Usage - Connect Two Existing Vertices

from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Segment_2, Point_2

arr = Arrangement_2()
unbounded = arr.unbounded_face()

Create two isolated vertices
v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
v2 = arr.insert_in_face_interior(Point_2(5, 5), unbounded)

print(f"Before: v1.degree() = {v1.degree()}, v2.degree() = {v2.degree()}")

Connect them with insert_at_vertices
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr.insert_at_vertices(seg, v1, v2)

print(f"After: v1.degree() = {v1.degree()}, v2.degree() = {v2.degree()}")
print(f"Halfedge source: {he.source().point()}")
print(f"Halfedge target: {he.target().point()}")

text

**Results:**
- Before degrees: [fill in]
- After degrees: [fill in]
- Halfedge direction: [source → target]
- Number of edges created: [check arr.number_of_edges()]

**Surprises/Discoveries:**
- [What surprised you?]

---

### Test 2: [Design another test - maybe closing a triangle?]

[You design and run this]

---

## Key Discoveries

**Halfedge Direction:**
- Returns halfedge pointing from [v1 or v2?] to [v1 or v2?]

**DCEL Topology Changes:**
- Vertices added: [0 - both already exist]
- Halfedges added: [2 - twins]
- Edges added: [1]
- Face changes: [might split face?]

**Precondition Validation:**
- Does it check if v1 is at left endpoint? [test this]
- Does it check if curve endpoints match vertices? [test this]

**Degree Updates:**
- v1 degree: [increases by 1]
- v2 degree: [increases by 1]

---

## Comparison with Similar Methods

How does this differ from:
- `insert_from_left_vertex`: [you already know this one!]
- `insert_from_right_vertex`: [you already know this one!]

**Key difference:**
- insert_from_*_vertex: Creates ONE new vertex
- insert_at_vertices: Creates ZERO new vertices (both exist)

---

## Tricky Parts / Gotchas

[Things users might mess up:]
1. 
2. 
3. 

---

## Docstring Outline (Draft)

**One-liner:**
"Connect two existing vertices with a curve."

**Key points to emphasize:**
- Both endpoints must already exist
- Returns halfedge pointing v1 → v2
- Updates degrees of both vertices
- May split a face if curve crosses it

**Example ideas:**
- Basic: Connect two isolated vertices
- Advanced: Complete a triangle (3 vertices → 3 edges)

---

## Questions to Ask in Docstring

- What if v1 and v2 are same vertex? (self-loop)
- What if there's already an edge between them?
- What if curve endpoints don't match vertex positions?

---

## Time Log

- Research started: [time]
- C++ docs read: [time]  
- Testing done: [time]
- Total time: [calculate]