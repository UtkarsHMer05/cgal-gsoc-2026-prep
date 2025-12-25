"""
Testing the 3 methods we'll document for first PR.
Author: Utkarsh Khajuria
Date: Dec 26, 2025
Purpose: Understand actual behavior before writing docstrings
"""

import sys
sys.path.insert(0, '/Users/utkarshkhajuria/cgal-python-bindings/build/src/libs/cgalpy')

from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Segment_2, Point_2
import inspect

print("="*70)
print("CGAL Python Bindings - Method Testing for First PR")
print("Testing 3 methods: insert_in_face_interior, insert_from_left_vertex,")
print("                   insert_from_right_vertex")
print("="*70)

# Create arrangement
print("\nInitializing arrangement...")
arr = Arrangement_2()
unbounded = arr.unbounded_face()
print(f"✓ Created arrangement with {arr.number_of_faces()} face (unbounded)")

# ============================================================================
# Test 1: insert_in_face_interior - POINT overload (Line 748)
# ============================================================================
print("\n" + "="*70)
print("TEST 1: insert_in_face_interior (point version)")
print("="*70)

# Check current signature
print("\n[1.1] Current Python signature:")
try:
    sig = inspect.signature(arr.insert_in_face_interior)
    print(f"      {sig}")
    print("      ^ Notice: No parameter names (arg0, arg1)")
except Exception as e:
    print(f"      ERROR: {e}")

# Test basic usage
print("\n[1.2] Basic usage: Insert point (5, 5) into unbounded face")
try:
    v = arr.insert_in_face_interior(Point_2(5, 5), unbounded)
    print(f"      ✓ Success!")
    print(f"      Created vertex at: {v.point()}")
    print(f"      Is isolated? {v.is_isolated()}")
    print(f"      Degree: {v.degree()}")
except Exception as e:
    print(f"      ✗ FAILED: {e}")

# Test edge case: duplicate point
print("\n[1.3] Edge case: Trying to insert at same location (5, 5) again")
try:
    v_dup = arr.insert_in_face_interior(Point_2(5, 5), unbounded)
    print(f"      ⚠ WARNING: Allowed duplicate! Created at {v_dup.point()}")
    print(f"      Total vertices now: {arr.number_of_vertices()}")
except Exception as e:
    print(f"      ✓ Correctly rejected: {type(e).__name__}: {e}")

# ============================================================================
# Test 2: insert_from_left_vertex - VERTEX overload (Line 743)
# ============================================================================
print("\n" + "="*70)
print("TEST 2: insert_from_left_vertex (vertex version)")
print("="*70)

# Check signature
print("\n[2.1] Current Python signature:")
try:
    sig = inspect.signature(arr.insert_from_left_vertex)
    print(f"      {sig}")
except Exception as e:
    print(f"      ERROR: {e}")

# Create left endpoint vertex
print("\n[2.2] Setup: Create vertex at (0, 0) for left endpoint")
try:
    v_left = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
    print(f"      ✓ Created v_left at {v_left.point()}")
    print(f"      Degree before insertion: {v_left.degree()}")
except Exception as e:
    print(f"      ✗ FAILED: {e}")

# Insert curve from left vertex
print("\n[2.3] Insert segment from (0,0) to (3,3)")
try:
    seg = Segment_2(Point_2(0, 0), Point_2(3, 3))
    he = arr.insert_from_left_vertex(seg, v_left)
    print(f"      ✓ Success!")
    print(f"      Halfedge source: {he.source().point()}")
    print(f"      Halfedge target: {he.target().point()}")
    print(f"      v_left degree after: {v_left.degree()}")
    print(f"      Twin exists? {he.twin() is not None}")
    print(f"      Target vertex is isolated? {he.target().is_isolated()}")
except Exception as e:
    print(f"      ✗ FAILED: {e}")

# ============================================================================
# Test 3: insert_from_right_vertex - VERTEX overload (Line 745)
# ============================================================================
print("\n" + "="*70)
print("TEST 3: insert_from_right_vertex (vertex version)")
print("="*70)

# Check signature
print("\n[3.1] Current Python signature:")
try:
    sig = inspect.signature(arr.insert_from_right_vertex)
    print(f"      {sig}")
except Exception as e:
    print(f"      ERROR: {e}")

# Create right endpoint vertex
print("\n[3.2] Setup: Create vertex at (10, 10) for right endpoint")
try:
    v_right = arr.insert_in_face_interior(Point_2(10, 10), unbounded)
    print(f"      ✓ Created v_right at {v_right.point()}")
    print(f"      Degree before insertion: {v_right.degree()}")
except Exception as e:
    print(f"      ✗ FAILED: {e}")

# Insert curve ending at right vertex
print("\n[3.3] Insert segment from (7,7) to (10,10)")
try:
    seg2 = Segment_2(Point_2(7, 7), Point_2(10, 10))
    he2 = arr.insert_from_right_vertex(seg2, v_right)
    print(f"      ✓ Success!")
    print(f"      Halfedge source: {he2.source().point()}")
    print(f"      Halfedge target: {he2.target().point()}")
    print(f"      v_right degree after: {v_right.degree()}")
    print(f"      Twin exists? {he2.twin() is not None}")
    print(f"      Source vertex is isolated? {he2.source().is_isolated()}")
except Exception as e:
    print(f"      ✗ FAILED: {e}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"\nArrangement statistics:")
print(f"  Vertices: {arr.number_of_vertices()}")
print(f"  Halfedges: {arr.number_of_halfedges()}")
print(f"  Edges: {arr.number_of_edges()}")
print(f"  Faces: {arr.number_of_faces()}")

print("\n✓ Testing complete!")
print("\nKey observations for docstrings:")
print("  1. insert_in_face_interior creates isolated vertices (degree 0)")
print("  2. insert_from_left_vertex extends FROM existing vertex")
print("  3. insert_from_right_vertex extends TO existing vertex")
print("  4. Both create halfedge pairs (twins)")
print("  5. Vertex degrees update when curves connect")
