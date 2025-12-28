# Part G: Patterns and Design Philosophy

**Understanding why CGAL is designed this way, and what it means for Python users**

---

## CGAL's Design Philosophy

CGAL is a C++ library with decades of development. Its design reflects C++ priorities:

### Performance Over Safety

> "Computational geometry algorithms require high performance. Validation overhead can be prohibitive when processing millions of geometric elements. Expert users who can guarantee correctness should not pay the cost of runtime checks."

This is the core philosophy. Every precondition check adds CPU cycles. For users processing millions of segments, those cycles add up. So CGAL trusts the programmer.

### Trust the Programmer

In C++, developers are expected to:
- Read documentation thoroughly
- Understand and verify preconditions before calling functions
- Accept responsibility for undefined behavior if preconditions aren't met
- Use assertions during development, disable in production

This "trust the programmer" philosophy is standard in high-performance C++.

### Compile-Time vs Runtime Checks

C++'s type system catches many errors at compile-time:
- Template type mismatches
- const correctness violations
- API contract violations (to some extent)

This reduces the need for runtime checks because many errors simply don't compile.

---

## Why This Matters for Python

Python has fundamentally different expectations:

| Aspect | C++ Expectation | Python Expectation |
|--------|-----------------|-------------------|
| Invalid input | Undefined behavior | Exception raised |
| Crashes | Acceptable for bugs | Unacceptable |
| Precondition checking | Manual, by caller | Runtime, by function |
| Documentation reading | Required before use | Optional (discoverability) |
| Type safety | Compile-time | Runtime only |
| Memory errors | Programmer's fault | Should never happen |

### The Mismatch

When CGAL's C++ philosophy meets Python users:
- Python users don't expect to read 50 pages of DCEL theory before calling a method
- Python users expect `ValueError` when they mess up, not segfaults
- Python's duck typing means you can easily pass wrong types
- Python's REPL encourages experimentation—which breaks things in CGAL

---

## Method Classification System

Through testing, I identified three tiers of methods:

### Tier 1: Safe High-Level Operations

**Examples**: `insert(curve)`, all query methods

**Characteristics**:
- Full validation
- Automatic intersection handling
- Cannot corrupt arrangement
- Safe for beginners

**When to use**: Always, unless you have specific performance needs.

### Tier 2: Unsafe Low-Level Operations

**Examples**: `insert_in_face_interior`, `insert_at_vertices`, `split_edge`, `modify_vertex`, `modify_edge`

**Characteristics**:
- Zero validation
- Maximum performance
- Can silently corrupt data
- For experts who guarantee correctness

**When to use**: Batch construction from validated data, algorithm implementation.

### Tier 3: Dangerous Operations

**Examples**: `remove_edge`, `remove_isolated_vertex`, `merge_edge`

**Characteristics**:
- Zero validation
- Can crash Python interpreter
- Handle invalidation issues
- Highest risk

**When to use**: Only when you fully understand consequences and have validated input.

---

## The Performance vs Safety Tradeoff

### Why Specialized Methods Exist

Consider building an arrangement with 1 million segments:

**With `insert()` (safe, slow)**:
```python
for seg in million_segments:
    insert(arr, seg)  # Each call: locate point, find intersections, subdivide
# Time: O(n² log n) with sweep-line, O(n²) naive
```

**With specialized methods (unsafe, fast)**:
```python
# If you've pre-computed all intersections and topology:
for vertex_data in sorted_vertices:
    v = arr.insert_in_face_interior(vertex_data.point, vertex_data.face)
for edge_data in sorted_edges:
    arr.insert_at_vertices(edge_data.curve, edge_data.v1, edge_data.v2)
# Time: O(n) - linear!
```

The difference can be orders of magnitude for large datasets.

### When Performance Matters

1. **GIS applications** - Processing continental-scale maps
2. **CAD systems** - Complex mechanical designs with thousands of features
3. **Scientific simulations** - Mesh generation, visibility computation
4. **Real-time applications** - Game engines, robotics

### When Safety Matters More

1. **Interactive applications** - User input can't be trusted
2. **Research/prototyping** - Rapid iteration, mistakes likely
3. **Learning CGAL** - Experimentation is how you learn
4. **One-off scripts** - Debugging time > execution time

---

## Halfedge Direction Patterns

Understanding the consistent pattern helps predict behavior:

### The Rule

**All methods return halfedge FROM the "source" parameter**:

| Method | Source Parameter | Return Direction |
|--------|-----------------|------------------|
| `insert_from_left_vertex(curve, v)` | v (left vertex) | v → new |
| `insert_from_right_vertex(curve, v)` | v (right vertex) | v → new |
| `insert_at_vertices(curve, v1, v2)` | v1 (first param) | v1 → v2 |
| `insert_in_face_interior(curve, face)` | (implicit left) | left → right |

### Why `insert_from_right_vertex` is Confusing

```python
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))  # LEFT → RIGHT
he = arr.insert_from_right_vertex(seg, v_right)

# Segment direction:  (0,0) → (5,5)
# Halfedge direction: (5,5) → (0,0)  ← REVERSED!
```

The method returns halfedge FROM v_right (the source parameter), not matching the curve direction. This is **internally consistent** but **externally confusing**.

---

## Handle Lifetime Pattern

### nanobind's `reference_internal` Policy

```cpp
// In the bindings:
m.def("insert_in_face_interior", &aos2::insert_point,
      nb::rv_policy::reference_internal);
```

This means:
- Returned handle keeps parent (arrangement) alive
- Handle is valid as long as arrangement exists
- **But**: Handle can become invalid if DCEL element is deleted

### The Gap

```
What reference_internal guarantees:
  handle.parent → arrangement → stays alive

What reference_internal doesn't handle:
  arrangement.internal_element(handle) → can be deleted
  handle → now points to freed memory
```

### The Pattern for Safe Code

```python
# Create
v1 = arr.insert_in_face_interior(...)
he = arr.insert_at_vertices(...)

# Use
# ... do stuff with v1, he ...

# Modify (dangerous)
arr.remove_edge(he)

# Discard (REQUIRED)
he = None
v1 = None
v2 = None

# After this, attempting to use them raises NameError
# instead of crashing or returning garbage
```

---

## Why Validation Isn't Added to Python Bindings

You might wonder: why not add validation in the Python bindings themselves?

### Technical Challenges

1. **Performance**: Validation requires geometric predicates (point location, intersection detection). Adding these to every call eliminates the performance benefit.

2. **Consistency**: Adding validation to some methods but not others creates confusing API where some methods raise exceptions and others don't.

3. **Completeness**: Full validation requires duplicating CGAL's internal algorithms (zone computation, etc.) in Python, which is error-prone.

4. **Maintenance**: Two different behaviors (C++ fast, Python safe) doubles the testing burden.

### The Current Compromise

The bindings take the approach of thin wrappers:
- Expose C++ API directly
- Let users choose their safety level
- Document the dangers clearly (this is where GSoC work helps!)

### Possible Future Improvements

1. **Optional validation mode**: `arr = Arrangement_2(validate=True)`
2. **Wrapper functions**: `safe_insert_at_vertices()` that validates first
3. **Better error messages**: Check for common mistakes before calling C++
4. **Handle validity checking**: `he.is_valid()` method (challenging to implement)

---

## Implications for Python Users

### Accept the Trade-off

If you use specialized methods, you're trading safety for performance. Accept this explicitly.

### Validate Externally

```python
def safe_insert_at_vertices(arr, curve, v1, v2):
    """Insert edge with validation."""
    # Check preconditions
    if not v1.is_isolated():
        raise ValueError(f"v1 is not isolated (degree={v1.degree()})")
    if not v2.is_isolated():
        raise ValueError(f"v2 is not isolated (degree={v2.degree()})")
    if curve.source() != v1.point():
        raise ValueError(f"Curve source {curve.source()} != v1 {v1.point()}")
    if curve.target() != v2.point():
        raise ValueError(f"Curve target {curve.target()} != v2 {v2.point()}")
    
    # Now safe to call
    return arr.insert_at_vertices(curve, v1, v2)
```

### Use High-Level API by Default

```python
# Prefer this:
from CGALPY.Aos2 import insert
insert(arr, segment)  # Safe, handles everything

# Over this:
arr.insert_in_face_interior(segment, face)  # Dangerous
```

### Test Thoroughly

```python
# After batch construction:
assert arr.is_valid(), "Arrangement corrupted during construction"
assert arr.number_of_vertices() == expected_v, f"Wrong vertex count"
assert arr.number_of_edges() == expected_e, f"Wrong edge count"
```

---

**Previous**: [← Part F - Critical Safety Issues](./part-f-safety-issues.md)  
**Next**: [Part H - Recommendations →](./part-h-recommendations.md)
