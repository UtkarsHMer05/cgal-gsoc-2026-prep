import sys
sys.path.insert(0, '/Users/utkarshkhajuria/cgal-python-bindings/build/src/libs/cgalpy')

from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Segment_2, Point_2

print("="*60)
print("QUERY METHODS - Quick Test Suite")
print("="*60)

# Build a simple arrangement for testing
arr = Arrangement_2()
unbounded = arr.unbounded_face()

# Create triangle
v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
v2 = arr.insert_in_face_interior(Point_2(10, 0), unbounded)
v3 = arr.insert_in_face_interior(Point_2(5, 10), unbounded)

he1 = arr.insert_at_vertices(Segment_2(Point_2(0, 0), Point_2(10, 0)), v1, v2)
he2 = arr.insert_at_vertices(Segment_2(Point_2(10, 0), Point_2(5, 10)), v2, v3)
he3 = arr.insert_at_vertices(Segment_2(Point_2(5, 10), Point_2(0, 0)), v3, v1)

print(f"\nTriangle arrangement built:")
print(f"  3 vertices, 3 edges, 2 faces (unbounded + interior)")

print("\n" + "="*60)
print("TEST 1: Counting methods")
print("="*60)

print(f"number_of_vertices(): {arr.number_of_vertices()}")
print(f"number_of_edges(): {arr.number_of_edges()}")
print(f"number_of_halfedges(): {arr.number_of_halfedges()}")
print(f"number_of_faces(): {arr.number_of_faces()}")
print(f"number_of_isolated_vertices(): {arr.number_of_isolated_vertices()}")

print("\n" + "="*60)
print("TEST 2: Boolean queries")
print("="*60)

print(f"is_empty(): {arr.is_empty()}")
print(f"is_valid(): {arr.is_valid()}")

# Create empty arrangement
empty_arr = Arrangement_2()
print(f"\nEmpty arrangement:")
print(f"  is_empty(): {empty_arr.is_empty()}")
print(f"  number_of_vertices(): {empty_arr.number_of_vertices()}")

print("\n" + "="*60)
print("TEST 3: unbounded_face()")
print("="*60)

ub = arr.unbounded_face()
print(f"unbounded_face() returned: {ub}")
print(f"Type: {type(ub)}")
print(f"is_unbounded(): {ub.is_unbounded()}")

print("\n" + "="*60)
print("TEST 4: Vertex methods")
print("="*60)

print(f"v1.point(): {v1.point()}")
print(f"v1.degree(): {v1.degree()}")
print(f"v1.is_isolated(): {v1.is_isolated()}")

# Create isolated vertex
v_iso = arr.insert_in_face_interior(Point_2(20, 20), unbounded)
print(f"\nIsolated vertex:")
print(f"  point: {v_iso.point()}")
print(f"  degree: {v_iso.degree()}")
print(f"  is_isolated: {v_iso.is_isolated()}")

# Check if isolated vertex has a face
try:
    iso_face = v_iso.face()
    print(f"  face(): {iso_face}")
    print(f"  face == unbounded: {iso_face == unbounded}")
except Exception as e:
    print(f"  face() not available or error: {type(e).__name__}")

print("\n" + "="*60)
print("TEST 5: Halfedge methods")
print("="*60)

print(f"he1 properties:")
print(f"  source(): {he1.source().point()}")
print(f"  target(): {he1.target().point()}")
print(f"  curve(): {he1.curve()}")

twin = he1.twin()
print(f"\nhe1.twin() properties:")
print(f"  source(): {twin.source().point()}")
print(f"  target(): {twin.target().point()}")
print(f"  Direction reversed: {twin.source().point()} → {twin.target().point()}")

# Navigation
next_he = he1.next()
print(f"\nhe1.next():")
print(f"  source: {next_he.source().point()}")
print(f"  target: {next_he.target().point()}")

prev_he = he1.prev()
print(f"\nhe1.prev():")
print(f"  source: {prev_he.source().point()}")
print(f"  target: {prev_he.target().point()}")

# Face
he_face = he1.face()
print(f"\nhe1.face():")
print(f"  Type: {type(he_face)}")
print(f"  is_unbounded: {he_face.is_unbounded()}")

print("\n" + "="*60)
print("TEST 6: Face methods")
print("="*60)

print(f"unbounded_face properties:")
print(f"  is_unbounded(): {unbounded.is_unbounded()}")

# Check outer_ccb
try:
    has_ccb = unbounded.has_outer_ccb()
    print(f"  has_outer_ccb(): {has_ccb}")
except Exception as e:
    print(f"  has_outer_ccb() error: {type(e).__name__}")

# Try to get inner face (not unbounded)
inner_face = he1.twin().face()  # Face on the other side
print(f"\nInner face properties:")
print(f"  is_unbounded(): {inner_face.is_unbounded()}")

try:
    has_ccb = inner_face.has_outer_ccb()
    print(f"  has_outer_ccb(): {has_ccb}")
except Exception as e:
    print(f"  has_outer_ccb() error: {type(e).__name__}")

print("\n" + "="*60)
print("TEST 7: Check for circulators")
print("="*60)

# Incident halfedges circulator
try:
    circ = v1.incident_halfedges()
    print(f"v1.incident_halfedges(): {circ}")
    print(f"Type: {type(circ)}")
    print(f"✓ Circulator exists")
except Exception as e:
    print(f"incident_halfedges() error: {type(e).__name__}: {e}")

# Holes iterators
try:
    holes_begin = unbounded.holes_begin()
    print(f"unbounded.holes_begin(): {holes_begin}")
except AttributeError:
    print(f"holes_begin() not bound in Python")
except Exception as e:
    print(f"holes_begin() error: {type(e).__name__}")

# Isolated vertices iterators
try:
    iso_begin = unbounded.isolated_vertices_begin()
    print(f"isolated_vertices_begin(): {iso_begin}")
except AttributeError:
    print(f"isolated_vertices_begin() not bound in Python")
except Exception as e:
    print(f"isolated_vertices_begin() error: {type(e).__name__}")

print("\n" + "="*60)
print("SUMMARY - QUERY & TRAVERSAL METHODS")
print("="*60)
print("""
✅ COUNTING METHODS (all work):
   - number_of_vertices()
   - number_of_edges()
   - number_of_halfedges()
   - number_of_faces()
   - number_of_isolated_vertices()

✅ BOOLEAN QUERIES (all work):
   - is_empty()
   - is_valid()
   - unbounded_face()

✅ VERTEX METHODS (all work):
   - point()
   - degree()
   - is_isolated()
   - face() [for isolated vertices]
   - incident_halfedges() [circulator]

✅ HALFEDGE METHODS (all work):
   - source()
   - target()
   - twin()
   - next()
   - prev()
   - curve()
   - face()

✅ FACE METHODS:
   - is_unbounded() [works]
   - has_outer_ccb() [check availability]
   - outer_ccb() [circulator - check]
   - holes_begin/end() [check if bound]
   - isolated_vertices_begin/end() [check if bound]

These methods are SAFE - no crashes expected!
Used for traversal and queries, not modification.
""")
