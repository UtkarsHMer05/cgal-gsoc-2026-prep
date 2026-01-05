# 🔬 Additional Crash Scenarios Discovery
**Date:** January 5-6, 2026  
**Author:** Utkarsh Khajuria  
**Goal:** Find more safety issues beyond the 5 crashes I discovered in December

---

## 🎯 What I Was Looking For

After submitting PR #2 in December, I had documented 5 crash scenarios. But I had a nagging feeling there were more lurking in the API. So I spent a few hours systematically testing edge cases I hadn't covered yet.

**Spoiler:** I found 2 more crashes and 4 "silent corruption" warnings.

---

## 📋 Previously Known Crashes (December 2025)

From my Phase 2 testing (Dec 27-28), I already knew about these 5 ways to crash Python:

1. **`remove_isolated_vertex()`** on a vertex that has edges → Bus error
2. **`remove_edge()`** called twice on same halfedge → Segfault
3. **`merge_edge()`** on non-adjacent edges → Segfault
4. **Accessing deleted vertex** after `merge_edge()` → Segfault
5. **Accessing deleted halfedge** after `remove_edge()` → Segfault

All of these are now documented in my PR #2 docstrings with big red warnings.

---

## 🔥 New Findings (January 2026)

### ❌ Crash #6: Accessing Twin After `remove_edge()`

**The scenario:** You remove an edge, but you had stored a reference to its twin beforehand. Then you try to access that twin.

**What happens:** Segmentation fault. Python dies.

```python
arr = Arrangement_2()
unbounded = arr.unbounded_face()
v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
seg1 = Segment_2(Point_2(0, 0), Point_2(5, 5))
he1 = arr.insert_from_left_vertex(seg1, v1)

twin = he1.twin()  # Store the twin BEFORE removal
arr.remove_edge(he1)  # Remove the edge

# Now try to use the twin...
point = twin.source().point()  # 💥 SEGFAULT
```

**Output:**
```
Stored twin halfedge before removal
Edge removed successfully
Attempting to access invalidated twin handle...
zsh: segmentation fault  python test_crash_3_twin.py
```

**Why this matters:** It's not obvious that when you delete an edge, you're also invalidating the twin handle. Users might think "I only deleted `he1`, but I still have `twin` right?" Nope. Both are gone.

**Fix needed:** Raise `RuntimeError: "Handle is invalidated - edge was removed"`

---

### ❌ Crash #7: `remove_isolated_vertex()` Called Twice

**The scenario:** You remove an isolated vertex. Then you accidentally call remove on the same handle again (maybe in a loop, or a logic bug).

**What happens:** Segmentation fault.

```python
arr = Arrangement_2()
unbounded = arr.unbounded_face()
v = arr.insert_in_face_interior(Point_2(3, 3), unbounded)

arr.remove_isolated_vertex(v)  # First removal - works fine
arr.remove_isolated_vertex(v)  # Second removal - 💥 CRASH
```

**Output:**
```
Created isolated vertex: 3 3
First removal: SUCCESS
Attempting second removal on same handle...
zsh: segmentation fault  python test_crash_5_double_remove.py
```

**Why this matters:** This is basically the same underlying issue as Crash #6 - handles don't know they've been invalidated. A Python user would expect a nice `ValueError` or `RuntimeError`, not a kernel kill.

**Fix needed:** Raise `RuntimeError: "Handle is invalidated - vertex was already removed"`

---

## ⚠️ Safety Warnings (No Crash, But Creates Invalid Arrangements)

These don't kill your Python process, but they silently break your arrangement. Arguably even worse in some ways - at least a crash is obvious.

---

### ⚠️ Warning #1: `modify_vertex()` on Connected Vertex

**The issue:** You can move a vertex to any location, even if it has edges connected to it. The vertex moves, but the edge curves don't update. Result: geometric nonsense.

```python
arr = Arrangement_2()
v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
seg1 = Segment_2(Point_2(0, 0), Point_2(5, 5))
he1 = arr.insert_from_left_vertex(seg1, v1)

# v1 has degree 1 - it has an edge!
v_modified = arr.modify_vertex(v1, Point_2(100, 100))  # Succeeds...

# Now vertex is at (100, 100), but edge curve still claims it goes from (0, 0) to (5, 5)
# 🤷 Arrangement is geometrically invalid
```

**Should probably:** Raise `ValueError: "Cannot modify vertex with connected edges to arbitrary location"`

---

### ⚠️ Warning #2: `split_edge()` with Wrong Point

**The issue:** You can split an edge at a point that's not actually on the edge. No validation.

```python
# Edge goes from (0,0) to (5,5) - it's the line y=x
# Try to split at (3, 5) which is NOT on that line!

wrong_seg1 = Segment_2(Point_2(0, 0), Point_2(3, 5))  # Off the line
wrong_seg2 = Segment_2(Point_2(3, 5), Point_2(5, 5))

he_new = arr.split_edge(he1, wrong_seg1, wrong_seg2)  # Succeeds...
```

**Result:** No crash, but the arrangement topology is now broken. `is_valid()` would probably return false.

**Should probably:** Raise `ValueError: "Split curves do not lie on original edge"`

---

### ⚠️ Warning #3: `merge_edge()` with Wrong Orientation

**The issue:** You can merge two edges even if you pass the twin of the second edge (wrong direction). It... works? I'm not sure if this is intentional flexibility or a bug.

```python
# he1: (0,0) -> (5,5)
# he2: (5,5) -> (10,10)

merged_curve = Segment_2(Point_2(0, 0), Point_2(10, 10))
he_merged = arr.merge_edge(he1, he2.twin(), merged_curve)  # Succeeds...

# he2.twin() goes (10,10) -> (5,5), which is the "wrong" direction
```

**Question for Efi:** Is this intentional? Should it be allowed, or should we validate that halfedges are consecutive in the same direction?

---

### ⚠️ Warning #4: `modify_edge()` with Mismatched Endpoints

**The issue:** You can modify an edge's curve to have different endpoints than the actual vertices. The method happily accepts it.

```python
# Original edge: (0,0) to (5,5)
# New curve: (0,0) to (7,7) - the target doesn't match the vertex!

wrong_curve = Segment_2(Point_2(0, 0), Point_2(7, 7))
he_modified = arr.modify_edge(he1, wrong_curve)  # Succeeds...
```

**Result:** Vertex stays at (5,5), but edge curve claims to go to (7,7). Geometric inconsistency.

**Should probably:** Raise `ValueError: "New curve endpoints must match edge vertices"`

---

## ✅ Good News: Some Things Are Safe!

### Iterator Invalidation Handled Correctly

I was worried this would crash, but it doesn't:

```python
for v in arr.vertices():
    if v.is_isolated():
        arr.remove_isolated_vertex(v)
```

**Result:** All 3 vertices deleted successfully, no crash. The iterator handles modification correctly.

This is actually really nice - it means you can safely delete while iterating. Not all C++ iterators behave this way.

---

## 🧪 Testing Methodology

**What I tested:**
- ✅ Vertex operations (`modify_vertex`, `remove_isolated_vertex`)
- ✅ Edge operations (`split_edge`, `merge_edge`, `modify_edge`)
- ✅ Halfedge operations (`remove_edge`, accessing twins)
- ✅ Handle lifetime (using invalidated handles)
- ✅ Iterator invalidation (deleting while iterating)

**How I tested:**
- Systematic violation of documented preconditions
- Edge cases (handle reuse, wrong parameters)
- Sequence errors (wrong order of operations)
- Handle misuse (using invalidated handles after deletion)

---

## 🔍 Patterns I've Identified

### Pattern 1: Handle Invalidation Not Enforced

**Methods affected:** `remove_edge()`, `remove_isolated_vertex()`  
**Issue:** Handles remain accessible after deletion, causing segfaults when reused  
**Solution:** Implement handle validity tracking or wrapper objects

### Pattern 2: Geometric Validation Missing

**Methods affected:** `modify_vertex()`, `split_edge()`, `modify_edge()`  
**Issue:** Accept geometrically invalid parameters without any checks  
**Solution:** Add precondition checks for geometric consistency

### Pattern 3: Parameter Validation Missing

**Methods affected:** `merge_edge()`  
**Issue:** Unclear if certain parameter combinations are intentional or bugs  
**Solution:** Clarify intended behavior with Efi, then add validation if needed

---

## 📊 Statistics

| Category | Count |
|----------|-------|
| Total crashes found | 7 (5 from December + 2 new) |
| Total warnings found | 4 (unsafe but no crash) |
| Safe behaviors verified | 1 (iterator invalidation) |
| Methods requiring precondition checks | 8 |
| Safe methods confirmed | 15+ (all query methods) |

---

## 🛠️ Precondition Framework Proposal

Based on everything I've found, here's what needs to be fixed:

| Method | Precondition | Check Required | Exception | Priority |
|--------|--------------|----------------|-----------|----------|
| `remove_isolated_vertex()` | Vertex must be isolated | `if not v.is_isolated()` | RuntimeError | 🔴 HIGH |
| `remove_isolated_vertex()` | Handle must be valid | Internal validation | RuntimeError | 🔴 HIGH |
| `remove_edge()` | Handle must be valid | Internal validation | RuntimeError | 🔴 HIGH |
| `remove_edge()` | Twin also invalidated | Track both handles | RuntimeError | 🔴 HIGH |
| `merge_edge()` | Edges must be adjacent | Check connectivity | ValueError | 🔴 HIGH |
| `merge_edge()` | Same direction? | Clarify behavior | ValueError | 🟡 MEDIUM |
| `modify_vertex()` | Point maintains edges | Geometric check | ValueError | 🟡 MEDIUM |
| `split_edge()` | Point on edge | Geometric check | ValueError | 🟡 MEDIUM |
| `modify_edge()` | Endpoints match | Vertex comparison | ValueError | 🟡 MEDIUM |

---

## ❓ Questions for Efi

1. **Handle invalidation:** Should we implement automatic handle invalidation tracking in the Python wrapper, or just document that users must manage handles themselves?

2. **Geometric validation:** Should precondition checks validate geometry (more expensive, but safer), or trust the user (current behavior, faster)?

3. **`merge_edge()` orientation:** Is merging with `he2.twin()` intentional flexibility, or a bug?

4. **Exception types:** What's the right exception hierarchy?
   - `RuntimeError` for handle/state issues?
   - `ValueError` for parameter validation?
   - Or custom classes like `InvalidHandleError`, `GeometryError`?

5. **Performance trade-off:** Should we always check preconditions (safer), or provide a flag to disable checks for performance-critical code?

6. **Priority:** Which crashes should I tackle first in Weeks 5-6?

---

## 📝 Next Steps (Weeks 5-6)

- **Week 5:** Implement precondition framework for HIGH priority items (handle invalidation crashes)
- **Week 6:** Add geometric validation for MEDIUM priority items
- **Testing:** Add unit tests for all precondition checks
- **Documentation:** Update docstrings with preconditions and exceptions raised

---

## 📁 Test Files Created

- `test_crash_3_twin.py` - Twin access after removal
- `test_crash_4_merge.py` - Merge with wrong orientation
- `test_crash_5_double_remove.py` - Double removal crash
- `test_crash_6_modify_edge.py` - Modify edge with wrong endpoints
- `test_crash_7_iterator.py` - Iterator invalidation (safe!)
- `test_additional_crashes.py` - All tests combined

---

*Research Completed: January 5, 2026, 10:58 PM IST*  
*Total new issues found: 2 crashes + 4 warnings*

The pattern is clear: CGAL trusts that the C++ user knows what they're doing. But Python users expect safety nets. That's the gap I'm here to fix.