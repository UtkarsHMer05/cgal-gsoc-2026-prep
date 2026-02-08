#!/usr/bin/env python3
"""Test #9: Split edge then access original halfedge"""
import sys
sys.path.insert(0, '/Users/utkarshkhajuria/cgal-python-bindings/build/src/libs/cgalpy')
from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Segment_2, Point_2

print("=" * 60)
print("Test #9: Split edge then access original halfedge")
print("=" * 60)

try:
    arr = Arrangement_2()
    unbounded = arr.unbounded_face()
    v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
    seg = Segment_2(Point_2(0, 0), Point_2(10, 10))
    he_original = arr.insert_from_left_vertex(seg, v1)
    
    print(f"Created edge: {he_original.source().point()} to {he_original.target().point()}")
    
    # Split the edge
    seg1 = Segment_2(Point_2(0, 0), Point_2(5, 5))
    seg2 = Segment_2(Point_2(5, 5), Point_2(10, 10))
    he_new = arr.split_edge(he_original, seg1, seg2)
    print(f"Edge split successfully")
    
    # Try to access original halfedge
    print("Attempting to access original halfedge after split...")
    curve = he_original.curve()
    print(f"⚠️  Original halfedge still accessible: {curve.source()} to {curve.target()}")
    
except Exception as e:
    print(f"❌ CRASH: {type(e).__name__}: {e}")
