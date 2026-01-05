#!/usr/bin/env python3
"""Test #6: modify_edge with wrong endpoints"""
import sys
sys.path.insert(0, '/Users/utkarshkhajuria/cgal-python-bindings/build/src/libs/cgalpy')
from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Segment_2, Point_2

print("=" * 60)
print("Test #6: modify_edge with mismatched endpoints")
print("=" * 60)

try:
    arr = Arrangement_2()
    unbounded = arr.unbounded_face()
    v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
    seg1 = Segment_2(Point_2(0, 0), Point_2(5, 5))
    he1 = arr.insert_from_left_vertex(seg1, v1)
    
    print(f"Original edge: {he1.source().point()} to {he1.target().point()}")
    
    wrong_curve = Segment_2(Point_2(0, 0), Point_2(7, 7))
    print(f"New curve: {wrong_curve.source()} to {wrong_curve.target()}")
    print("⚠️  Target mismatch: curve ends at (7,7) but vertex is at (5,5)")
    
    he_modified = arr.modify_edge(he1, wrong_curve)
    print("✅ Modified without validation (arrangement now inconsistent)")
except Exception as e:
    print(f"❌ CRASH: {type(e).__name__}: {e}")
