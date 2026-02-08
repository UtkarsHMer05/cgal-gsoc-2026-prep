#!/usr/bin/env python3
"""Test #4: merge_edge with wrong orientation"""
import sys
sys.path.insert(0, '/Users/utkarshkhajuria/cgal-python-bindings/build/src/libs/cgalpy')
from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Segment_2, Point_2

print("=" * 60)
print("Test #4: merge_edge with wrong orientation")
print("=" * 60)

try:
    arr = Arrangement_2()
    unbounded = arr.unbounded_face()
    v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
    seg1 = Segment_2(Point_2(0, 0), Point_2(5, 5))
    he1 = arr.insert_from_left_vertex(seg1, v1)
    
    v2 = he1.target()
    seg2 = Segment_2(Point_2(5, 5), Point_2(10, 10))
    he2 = arr.insert_from_left_vertex(seg2, v2)
    
    print(f"he1: {he1.source().point()} -> {he1.target().point()}")
    print(f"he2: {he2.source().point()} -> {he2.target().point()}")
    
    merged_curve = Segment_2(Point_2(0, 0), Point_2(10, 10))
    print("Attempting to merge he1 with he2.twin()...")
    
    he_merged = arr.merge_edge(he1, he2.twin(), merged_curve)
    print("✅ Merge succeeded (WARNING: accepted wrong orientation)")
except Exception as e:
    print(f"❌ CRASH: {type(e).__name__}: {e}")
