import sys
sys.path.insert(0, '/Users/utkarshkhajuria/cgal-python-bindings/build/src/libs/cgalpy')

from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Segment_2, Point_2

print("="*60)
print("TEST 1: insert_at_vertices - Basic Usage")
print("="*60)

arr = Arrangement_2()
unbounded = arr.unbounded_face()

# Create two isolated vertices
v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
v2 = arr.insert_in_face_interior(Point_2(5, 5), unbounded)

print(f"Before connection:")
print(f"  v1.degree() = {v1.degree()}")
print(f"  v2.degree() = {v2.degree()}")
print(f"  v1.is_isolated() = {v1.is_isolated()}")
print(f"  v2.is_isolated() = {v2.is_isolated()}")
print(f"  arr.number_of_edges() = {arr.number_of_edges()}")

# Connect them
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr.insert_at_vertices(seg, v1, v2)

print(f"\nAfter connection:")
print(f"  v1.degree() = {v1.degree()}")
print(f"  v2.degree() = {v2.degree()}")
print(f"  v1.is_isolated() = {v1.is_isolated()}")
print(f"  v2.is_isolated() = {v2.is_isolated()}")
print(f"  arr.number_of_edges() = {arr.number_of_edges()}")

print(f"\nHalfedge properties:")
print(f"  he.source().point() = {he.source().point()}")
print(f"  he.target().point() = {he.target().point()}")
print(f"  he.twin() exists = {he.twin() is not None}")

print(f"\nArrangement stats:")
print(f"  Vertices: {arr.number_of_vertices()}")
print(f"  Halfedges: {arr.number_of_halfedges()}")
print(f"  Edges: {arr.number_of_edges()}")
print(f"  Faces: {arr.number_of_faces()}")

# TODO: Add more tests!
# Test 2: Close a triangle (3 vertices, 3 edges)
# Test 3: What if vertices don't match curve endpoints?

print("\n" + "="*60)
print("TEST 2: Mismatched endpoints - Does it validate?")
print("="*60)

arr2 = Arrangement_2()
unbounded2 = arr2.unbounded_face()

# Create vertices at (0, 0) and (5, 5)
v1 = arr2.insert_in_face_interior(Point_2(0, 0), unbounded2)
v2 = arr2.insert_in_face_interior(Point_2(5, 5), unbounded2)

# Try to connect them with a segment that has DIFFERENT endpoints!
bad_seg = Segment_2(Point_2(0, 0), Point_2(10, 10))  # Goes beyond v2!

try:
    he = arr2.insert_at_vertices(bad_seg, v1, v2)
    print("⚠️  NO VALIDATION! Method accepted mismatched segment")
    print(f"  Segment goes to {bad_seg.target()}")
    print(f"  But v2 is at {v2.point()}")
except Exception as e:
    print(f"✅ VALIDATION EXISTS: {e}")

print("\n" + "="*60)
print("TEST 3: Duplicate edges - What happens?")
print("="*60)

arr3 = Arrangement_2()
unbounded3 = arr3.unbounded_face()

v1 = arr3.insert_in_face_interior(Point_2(0, 0), unbounded3)
v2 = arr3.insert_in_face_interior(Point_2(5, 5), unbounded3)

# Insert first edge
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he1 = arr3.insert_at_vertices(seg, v1, v2)
print(f"After first insertion: {arr3.number_of_edges()} edges")

# Try to insert the SAME edge again!
try:
    he2 = arr3.insert_at_vertices(seg, v1, v2)
    print(f"⚠️  Allowed duplicate! Now {arr3.number_of_edges()} edges")
except Exception as e:
    print(f"✅ Prevented duplicate: {e}")


print("\n" + "="*60)
print("TEST 4: insert_in_face_interior - Creates new components")
print("="*60)

arr4 = Arrangement_2()
unbounded4 = arr4.unbounded_face()

# Insert a segment in the unbounded face
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr4.insert_in_face_interior(seg, unbounded4)

print(f"After insertion:")
print(f"  Vertices: {arr4.number_of_vertices()}")
print(f"  Edges: {arr4.number_of_edges()}")
print(f"  Halfedge direction: {he.source().point()} → {he.target().point()}")

# TEST: What if we insert overlapping segment?
try:
    bad_seg = Segment_2(Point_2(2, 2), Point_2(7, 7))  # Overlaps!
    he2 = arr4.insert_in_face_interior(bad_seg, unbounded4)
    print("⚠️  Accepted overlapping segment!")
except Exception as e:
    print(f"✅ Rejected overlap: {e}")

print("\n" + "="*60)
print("TEST 5: insert_from_left_vertex - Direction and validation")
print("="*60)

arr5 = Arrangement_2()
unbounded5 = arr5.unbounded_face()

# Create one vertex (left endpoint)
v_left = arr5.insert_in_face_interior(Point_2(0, 0), unbounded5)

# Insert segment from left vertex
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr5.insert_from_left_vertex(seg, v_left)

print(f"After insertion:")
print(f"  Vertices: {arr5.number_of_vertices()}")
print(f"  Edges: {arr5.number_of_edges()}")
print(f"  Returned halfedge: {he.source().point()} → {he.target().point()}")
print(f"  v_left.degree() = {v_left.degree()}")
print(f"  v_left.is_isolated() = {v_left.is_isolated()}")

# TEST: Mismatched left endpoint
print("\nTesting mismatched left endpoint:")
v_wrong = arr5.insert_in_face_interior(Point_2(10, 10), unbounded5)
bad_seg = Segment_2(Point_2(0, 0), Point_2(15, 15))  # Doesn't start at v_wrong!

try:
    he2 = arr5.insert_from_left_vertex(bad_seg, v_wrong)
    print("⚠️  NO VALIDATION! Accepted mismatched left endpoint")
    print(f"  Segment starts at {bad_seg.source()}")
    print(f"  But vertex is at {v_wrong.point()}")
except Exception as e:
    print(f"✅ Rejected: {e}")


print("\n" + "="*60)
print("TEST 6: insert_from_right_vertex - Direction and validation")
print("="*60)

arr6 = Arrangement_2()
unbounded6 = arr6.unbounded_face()

# Create one vertex (right endpoint)
v_right = arr6.insert_in_face_interior(Point_2(5, 5), unbounded6)

# Insert segment from right vertex
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr6.insert_from_right_vertex(seg, v_right)

print(f"After insertion:")
print(f"  Vertices: {arr6.number_of_vertices()}")
print(f"  Edges: {arr6.number_of_edges()}")
print(f"  Returned halfedge: {he.source().point()} → {he.target().point()}")
print(f"  v_right.degree() = {v_right.degree()}")
print(f"  v_right.is_isolated() = {v_right.is_isolated()}")

# TEST: Mismatched right endpoint
print("\nTesting mismatched right endpoint:")
v_wrong = arr6.insert_in_face_interior(Point_2(10, 10), unbounded6)
bad_seg = Segment_2(Point_2(0, 0), Point_2(5, 5))  # Doesn't end at v_wrong!

try:
    he2 = arr6.insert_from_right_vertex(bad_seg, v_wrong)
    print("⚠️  NO VALIDATION! Accepted mismatched right endpoint")
    print(f"  Segment ends at {bad_seg.target()}")
    print(f"  But vertex is at {v_wrong.point()}")
except Exception as e:
    print(f"✅ Rejected: {e}")


print("\n" + "="*60)
print("TEST 7: Direction patterns - Summary")
print("="*60)

# Fresh arrangement for each test
print("\n1. insert_in_face_interior:")
arr_test1 = Arrangement_2()
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr_test1.insert_in_face_interior(seg, arr_test1.unbounded_face())
print(f"   Segment: {seg.source()} → {seg.target()}")
print(f"   Returned halfedge: {he.source().point()} → {he.target().point()}")
print(f"   ✓ Direction: LEFT → RIGHT (matches segment)")

print("\n2. insert_from_left_vertex:")
arr_test2 = Arrangement_2()
v_left = arr_test2.insert_in_face_interior(Point_2(0, 0), arr_test2.unbounded_face())
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr_test2.insert_from_left_vertex(seg, v_left)
print(f"   Segment: {seg.source()} → {seg.target()}")
print(f"   Given vertex: {v_left.point()}")
print(f"   Returned halfedge: {he.source().point()} → {he.target().point()}")
print(f"   ✓ Direction: FROM given vertex (v_left → new)")

print("\n3. insert_from_right_vertex:")
arr_test3 = Arrangement_2()
v_right = arr_test3.insert_in_face_interior(Point_2(5, 5), arr_test3.unbounded_face())
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr_test3.insert_from_right_vertex(seg, v_right)
print(f"   Segment: {seg.source()} → {seg.target()}")
print(f"   Given vertex: {v_right.point()}")
print(f"   Returned halfedge: {he.source().point()} → {he.target().point()}")
print(f"   ⚠️  Direction: FROM given vertex (v_right → new) - REVERSED from segment!")

print("\n4. insert_at_vertices:")
arr_test4 = Arrangement_2()
v1 = arr_test4.insert_in_face_interior(Point_2(0, 0), arr_test4.unbounded_face())
v2 = arr_test4.insert_in_face_interior(Point_2(5, 5), arr_test4.unbounded_face())
seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
he = arr_test4.insert_at_vertices(seg, v1, v2)
print(f"   Segment: {seg.source()} → {seg.target()}")
print(f"   Given vertices: v1={v1.point()}, v2={v2.point()}")
print(f"   Returned halfedge: {he.source().point()} → {he.target().point()}")
print(f"   ✓ Direction: v1 → v2 (first param to second param)")

print("\n" + "="*60)
print("PATTERN SUMMARY:")
print("="*60)
print("All methods return halfedge FROM the 'source' vertex:")
print("  - insert_from_left_vertex:  FROM v_left")
print("  - insert_from_right_vertex: FROM v_right (reversed from segment!)")
print("  - insert_at_vertices:       FROM v1 (first parameter)")
print("  - insert_in_face_interior:  FROM left endpoint")
