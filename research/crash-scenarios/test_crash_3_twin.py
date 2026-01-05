#!/usr/bin/env python3
"""Test #3: Access twin after remove_edge"""
import sys
sys.path.insert(0, '/Users/utkarshkhajuria/cgal-python-bindings/build/src/libs/cgalpy')
from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Segment_2, Point_2

print("=" * 60)
print("Test #3: Access twin after remove_edge")
print("=" * 60)

try:
    arr = Arrangement_2()
    unbounded = arr.unbounded_face()
    v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
    seg1 = Segment_2(Point_2(0, 0), Point_2(5, 5))
    he1 = arr.insert_from_left_vertex(seg1, v1)
    
    twin = he1.twin()
    print("Stored twin halfedge before removal")
    
    arr.remove_edge(he1)
    print("Edge removed successfully")
    
    print("Attempting to access invalidated twin handle...")
    point = twin.source().point()
    
    print(f"⚠️  WARNING: Accessed invalidated handle: {point}")
except Exception as e:
    print(f"❌ CRASH: {type(e).__name__}: {e}")
