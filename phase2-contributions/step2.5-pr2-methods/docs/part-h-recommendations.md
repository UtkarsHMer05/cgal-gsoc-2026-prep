# Part H: Recommendations

**Concrete advice for Python users, maintainers, and GSoC contributors**

---

## For Python Binding Users

### Priority 1: Use Safe Methods by Default

```python
# ✓ RECOMMENDED: Use high-level insert()
from CGALPY.Aos2 import Arrangement_2, insert
from CGALPY.Ker import Segment_2, Point_2

arr = Arrangement_2()
seg = Segment_2(Point_2(0, 0), Point_2(10, 10))
result = insert(arr, seg)  # Handles all topological scenarios safely

# ✗ AVOID: Specialized methods unless you know what you're doing
he = arr.insert_in_face_interior(seg, face)  # No validation!
```

### Priority 2: Always Validate Before Dangerous Operations

```python
# ✓ CORRECT: Check preconditions manually
if vertex.is_isolated():
    arr.remove_isolated_vertex(vertex)
else:
    print(f"Error: Vertex is not isolated (degree={vertex.degree()})")

# ✗ WRONG: Assume preconditions hold
arr.remove_isolated_vertex(vertex)  # May crash!
```

### Priority 3: Never Reuse Handles After Modification

```python
# ✓ CORRECT: Discard handles after removal
v1 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
v2 = arr.insert_in_face_interior(Point_2(5, 5), arr.unbounded_face())
he = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(5, 5)), v1, v2)

arr.remove_edge(he)

# Discard all handles that may have been invalidated:
he = None
v1 = None
v2 = None

# ✗ WRONG: Reuse handles after modification
arr.remove_edge(he)
print(he.source())  # CRASH - he is invalid!
```

### Priority 4: Use Query Methods to Verify State

```python
# ✓ RECOMMENDED: Validate arrangement after batch operations
arr = build_arrangement_from_file(filename)

if not arr.is_valid():
    print("ERROR: Arrangement is invalid!")
    print(f"  Vertices: {arr.number_of_vertices()}")
    print(f"  Edges: {arr.number_of_edges()}")
    print(f"  Faces: {arr.number_of_faces()}")
    # Debug the construction process

# Also check expected counts:
assert arr.number_of_vertices() == expected_v
assert arr.number_of_edges() == expected_e
```

### Priority 5: Understand try/except Limitations

```python
# ⚠️ NOTE: This does NOT catch segmentation faults!
# But it can catch other exceptions

try:
    he = arr.insert_at_vertices(seg, v1, v2)
except Exception as e:
    print(f"Insertion failed: {e}")
    # Handle error

# 🔴 This CANNOT catch crashes:
try:
    arr.remove_isolated_vertex(non_isolated_vertex)
except Exception as e:  # Never reaches here - process crashes first
    print("This will never execute")
```

---

## For CGAL Python Bindings Maintainers

### Short-Term Improvements (Can Do in Weeks)

#### 1. Add Prominent Safety Warnings to Docstrings

```python
"""
🔴 CRITICAL WARNING: This method performs NO validation.
Calling with invalid input WILL crash Python or corrupt the arrangement.

Preconditions (YOU must verify before calling):
- vertex.is_isolated() MUST be True
- vertex MUST currently exist in this arrangement

For safe alternatives, use the high-level insert() function.
"""
```

#### 2. Document Handle Lifetime Issues

```python
"""
⚠️ Handle Lifetime: After this operation, handles to deleted elements 
become INVALID. Accessing them causes undefined behavior (crashes or 
stale data). Do NOT reuse handles to removed elements.

Pattern:
    arr.remove_edge(he)
    he = None  # Prevent accidental use
"""
```

#### 3. Complete Missing API Bindings

```cpp
// Add optional parameters to remove_edge:
m.def("remove_edge",
      [](Aos2& arr, Halfedge_handle he, bool rem_src, bool rem_tgt) {
          return arr.remove_edge(he, rem_src, rem_tgt);
      },
      nb::arg("halfedge"),
      nb::arg("remove_source") = true,
      nb::arg("remove_target") = true,
      "Removes edge with control over vertex removal");

// Add face iterators:
// holes_begin(), isolated_vertices_begin(), etc.
```

### Medium-Term Improvements (Months of Work)

#### 4. Add Python-Specific Safety Wrappers (Optional Mode)

```python
# Proposed API enhancement
arr = Arrangement_2(validate=True)  # Enable runtime checks

# Now these would throw Python exceptions instead of crashing:
v = # ... non-isolated vertex ...
arr.remove_isolated_vertex(v)  # Raises ValueError instead of crash
```

#### 5. Improve Error Messages

```python
# Current: Cryptic nanobind type error
TypeError: remove_edge(): incompatible function arguments...

# Proposed: Clear Python-friendly message
TypeError: remove_edge() expected 1 argument (halfedge), got 3.
Note: Optional parameters remove_source and remove_target are not
available in Python bindings. See documentation for workarounds.
```

#### 6. Add Handle Validity Checking (Challenging)

```python
# Proposed: Detect invalid handles
arr.remove_edge(he)

if he.is_valid():  # New method
    print(he.source())
else:
    print("Handle is invalid - element was deleted")
```

### Long-Term Improvements (Major Effort)

#### 7. Dual-Mode API: Safe vs Performance

```python
from CGALPY.Aos2 import Arrangement_2_Safe, Arrangement_2_Fast

# Safe mode: All preconditions validated, exceptions instead of crashes
arr_safe = Arrangement_2_Safe()
arr_safe.remove_isolated_vertex(v)  # Raises ValueError if not isolated

# Fast mode: Current behavior, for experts
arr_fast = Arrangement_2_Fast()
arr_fast.remove_isolated_vertex(v)  # No checks, crashes if wrong
```

#### 8. Safe Defaults with Opt-Out

```python
# Default: Validation enabled
arr = Arrangement_2()

# Opt-out for performance-critical code
with arr.unsafe_mode():
    # Validation disabled in this block
    for i in range(1000000):
        arr.insert_at_vertices(segs[i], v1[i], v2[i])
```

---

## For GSoC Candidates and Contributors

### Documentation Priorities

#### 1. Write Comprehensive Docstrings

Every method should have:
- One-line summary
- Parameter descriptions with types
- Return value description
- Preconditions section with ⚠️ NOT VALIDATED warnings
- DCEL changes section
- Example code
- Cross-references to related methods
- "Danger Zone" section for unsafe methods

#### 2. Create Safety Guide

Write a document: **"CGAL Arrangements: Python Safety Guide"**
- Compare C++ vs Python safety expectations
- List all crash scenarios with examples
- Provide defensive coding patterns
- Explain handle lifetime issues

#### 3. Add Usage Examples

- Safe patterns (high-level API)
- Unsafe patterns (specialized methods with validation)
- Common mistakes to avoid
- Debugging invalid arrangements

### Code Improvements

#### 4. Parameter Name Binding

```cpp
// From:
m.def("remove_edge", &aos2::remove_edge)

// To:
m.def("remove_edge", &aos2::remove_edge,
      nb::arg("halfedge"),
      R"doc(
      Removes edge from arrangement.
      
      Parameters
      ----------
      halfedge : Halfedge
          Handle to the edge to remove.
      
      Returns
      -------
      Face
          The merged face.
      )doc");
```

#### 5. Validation Helper Functions

Create Python helper module:

```python
# cgal_helpers.py

def safe_remove_isolated_vertex(arr, vertex):
    """Remove isolated vertex with validation.
    
    Raises
    ------
    ValueError
        If vertex is not isolated.
    """
    if not vertex.is_isolated():
        raise ValueError(
            f"Vertex at {vertex.point()} is not isolated "
            f"(degree = {vertex.degree()})"
        )
    arr.remove_isolated_vertex(vertex)


def safe_insert_at_vertices(arr, curve, v1, v2):
    """Insert edge connecting two vertices with validation.
    
    Raises
    ------
    ValueError
        If preconditions are not met.
    """
    if curve.source() != v1.point():
        raise ValueError(
            f"Curve source {curve.source()} doesn't match v1 at {v1.point()}"
        )
    if curve.target() != v2.point():
        raise ValueError(
            f"Curve target {curve.target()} doesn't match v2 at {v2.point()}"
        )
    return arr.insert_at_vertices(curve, v1, v2)
```

### Testing

#### 6. Comprehensive Test Suite

```python
def test_precondition_violations():
    """Verify that precondition violations have documented behavior."""
    arr = Arrangement_2()
    v = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
    
    # Document that this creates duplicate:
    v2 = arr.insert_in_face_interior(Point_2(0, 0), arr.unbounded_face())
    assert arr.number_of_vertices() == 2  # Both created (documented behavior)
    

def test_validation_with_is_valid():
    """Verify is_valid() catches corruption."""
    arr = Arrangement_2()
    # ... create corrupt arrangement using specialized methods ...
    # Note: This may be hard to test without causing crashes
```

#### 7. Crash Scenario Documentation

Create `CRASH_SCENARIOS.md`:

```markdown
# Known Crash Scenarios

## Scenario 1: remove_isolated_vertex on non-isolated vertex
- **Cause**: Calling without checking is_isolated()
- **Symptom**: Bus error (SIGBUS)
- **Prevention**: Always check is_isolated() first
- **Test file**: test_removal_methods.py

## Scenario 2: ...
```

---

## Quick Reference Card

| Scenario | Safe Approach | Dangerous Approach |
|----------|---------------|-------------------|
| Insert segment | `insert(arr, seg)` | `insert_in_face_interior(seg, face)` |
| Remove vertex | Check `is_isolated()` first | Just call `remove_isolated_vertex()` |
| After removal | Set handles to `None` | Reuse handles |
| Batch construction | Validate with `is_valid()` | Trust your code |
| Learning CGAL | Query methods only | All methods |

---

## Summary

### For Users:
1. Use `insert()` by default
2. Always validate before removal
3. Discard handles after modification
4. Use `is_valid()` to check state

### For Maintainers:
1. Add safety warnings to docstrings
2. Bind missing optional parameters
3. Consider validation mode
4. Improve error messages

### For Contributors:
1. Document everything
2. Create helper functions
3. Write comprehensive tests
4. Focus on safety for Python users

---

**Previous**: [← Part G - Patterns and Design Philosophy](./part-g-patterns.md)  
**Next**: [Appendix A - Complete Test Results →](./appendix-a-test-results.md)
