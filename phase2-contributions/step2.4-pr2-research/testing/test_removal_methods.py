import sys
sys.path.insert(0, '/Users/utkarshkhajuria/cgal-python-bindings/build/src/libs/cgalpy')

from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Segment_2, Point_2

print("="*60)
print("TEST 1: remove_edge - Basic removal")
print("="*60)

arr = Arrangement_2()
unbounded = arr.unbounded_face()

v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
v2 = arr.insert_in_face_interior(Point_2(5, 5), unbounded)
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr.insert_at_vertices(seg, v1, v2)

print(f"Before removal:")
print(f"  Edges: {arr.number_of_edges()}")
print(f"  Vertices: {arr.number_of_vertices()}")
print(f"  v1.degree() = {v1.degree()}")
print(f"  v2.degree() = {v2.degree()}")

# Remove the edge
returned_face = arr.remove_edge(he)

print(f"\nAfter removal:")
print(f"  Edges: {arr.number_of_edges()}")
print(f"  Vertices: {arr.number_of_vertices()}")
print(f"  Returned face: {returned_face}")
print(f"  Returned face == unbounded? {returned_face == unbounded}")

# DANGER: Try to access deleted vertex
print(f"\n⚠️ DANGLING HANDLE TEST:")
try:
    degree = v1.degree()
    print(f"  v1.degree() = {degree}  ← HANDLE STILL ACCESSIBLE!")
    print(f"  ⚠️ This is UNDEFINED BEHAVIOR - data is garbage!")
except Exception as e:
    print(f"  ✓ Exception raised: {type(e).__name__}")


print("\n" + "="*60)
print("TEST 2: remove_edge with optional parameters")
print("="*60)

arr2 = Arrangement_2()
v1 = arr2.insert_in_face_interior(Point_2(0, 0), arr2.unbounded_face())
v2 = arr2.insert_in_face_interior(Point_2(5, 5), arr2.unbounded_face())
he = arr2.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(5, 5)), v1, v2)

print(f"Before removal: {arr2.number_of_vertices()} vertices")

try:
    arr2.remove_edge(he, False, False)
    print(f"After removal: {arr2.number_of_vertices()} vertices")
    print(f"  ✓ Parameters exist to control vertex removal!")
except TypeError as e:
    print(f"  ⚠️ MISSING FEATURE: Optional parameters not bound!")
    print(f"  Error: {e}")
    print(f"  C++ docs show remove_edge(e, remove_src, remove_tgt) but Python only has remove_edge(e)")
    

print("\n" + "="*60)
print("TEST 3: remove_isolated_vertex - SAFE case")
print("="*60)

arr3 = Arrangement_2()
v = arr3.insert_in_face_interior(Point_2(0, 0), arr3.unbounded_face())

print(f"Before removal:")
print(f"  Vertices: {arr3.number_of_vertices()}")
print(f"  v.is_isolated() = {v.is_isolated()}")

arr3.remove_isolated_vertex(v)

print(f"After removal:")
print(f"  Vertices: {arr3.number_of_vertices()}")
print(f"  ✓ Safe removal of isolated vertex succeeded")


print("\n" + "="*60)
print("TEST 4: remove_isolated_vertex - Check validation")
print("="*60)

arr4 = Arrangement_2()
v1 = arr4.insert_in_face_interior(Point_2(0, 0), arr4.unbounded_face())
v2 = arr4.insert_in_face_interior(Point_2(5, 5), arr4.unbounded_face())
he = arr4.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(5, 5)), v1, v2)

print(f"v1.is_isolated() = {v1.is_isolated()}")
print(f"v1.degree() = {v1.degree()}")
print(f"\n⚠️ CRASH TEST SKIPPED - Would cause bus error!")
print(f"Documented behavior: NO VALIDATION - calling remove_isolated_vertex()")
print(f"on a connected vertex CRASHES Python interpreter with bus error")


print("\n" + "="*60)
print("TEST 5: remove_edge - Return value analysis")
print("="*60)

arr5 = Arrangement_2()
unbounded = arr5.unbounded_face()

# Create a triangle to see face merging
v1 = arr5.insert_in_face_interior(Point_2(0, 0), unbounded)
v2 = arr5.insert_in_face_interior(Point_2(10, 0), unbounded)
v3 = arr5.insert_in_face_interior(Point_2(5, 10), unbounded)

he1 = arr5.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(10, 0)), v1, v2)
he2 = arr5.insert_at_vertices(Segment_2(Point_2(10, 0), Point_2(5, 10)), v2, v3)
he3 = arr5.insert_at_vertices(Segment_2(Point_2(5, 10), Point_2(0, 0)), v3, v1)

print(f"Triangle arrangement:")
print(f"  Vertices: {arr5.number_of_vertices()}")
print(f"  Edges: {arr5.number_of_edges()}")
print(f"  Faces: {arr5.number_of_faces()}")

# Remove one edge
returned_face = arr5.remove_edge(he1)
print(f"\nAfter removing bottom edge:")
print(f"  Vertices: {arr5.number_of_vertices()}")
print(f"  Edges: {arr5.number_of_edges()}")
print(f"  Faces: {arr5.number_of_faces()}")
print(f"  Returned face is unbounded? {returned_face == unbounded}")


print("\n" + "="*60)
print("TEST 6: Multiple removals - handle invalidation")
print("="*60)

arr6 = Arrangement_2()
v1 = arr6.insert_in_face_interior(Point_2(0, 0), arr6.unbounded_face())
v2 = arr6.insert_in_face_interior(Point_2(5, 5), arr6.unbounded_face())
he = arr6.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(5, 5)), v1, v2)

print(f"Before removal: {arr6.number_of_edges()} edges")

arr6.remove_edge(he)
print(f"After first removal: {arr6.number_of_edges()} edges")

# Try to remove the SAME edge again
print(f"\nTrying to remove the SAME halfedge again:")
try:
    arr6.remove_edge(he)  # he is now INVALID
    print(f"  ⚠️ Allowed removal of deleted edge - undefined behavior!")
except Exception as e:
    print(f"  ✓ Exception raised: {type(e).__name__}")

print("\n" + "="*60)
print("SUMMARY OF REMOVAL METHOD FINDINGS")
print("="*60)
print("""
CRITICAL SAFETY ISSUES DISCOVERED:

1. remove_edge(halfedge):
   ✓ Works and returns merged Face
   ⚠️ ALWAYS removes isolated vertices (no control in Python)
   ⚠️ C++ optional parameters NOT bound in Python
   ⚠️ Handles remain accessible after removal (undefined behavior)
   
2. remove_isolated_vertex(vertex):
   ✓ Works for isolated vertices
   🔴 NO VALIDATION - crashes Python if vertex not isolated
   🔴 Bus error (SEGFAULT) instead of exception
   ⚠️ Extremely dangerous for Python users

3. Handle Lifetime Issues:
   🔴 Deleted vertex handles still "work" but contain garbage
   🔴 No way to detect if a handle is invalid
   🔴 Calling methods on invalid handles causes crashes or corruption
   
RECOMMENDATIONS FOR DOCSTRINGS:
- Warn users about automatic vertex removal
- Emphasize handle invalidation after removal
- Document that remove_isolated_vertex() REQUIRES manual validation
- Example code must show v.is_isolated() check BEFORE removal
- Mention missing API (optional parameters) as limitation
""")
