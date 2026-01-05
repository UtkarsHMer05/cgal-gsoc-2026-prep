#!/usr/bin/env python3
"""Test #7: Iterator invalidation"""
import sys
sys.path.insert(0, '/Users/utkarshkhajuria/cgal-python-bindings/build/src/libs/cgalpy')
from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Segment_2, Point_2

print("=" * 60)
print("Test #7: Iterator invalidation")
print("=" * 60)

try:
    arr = Arrangement_2()
    unbounded = arr.unbounded_face()
    
    for i in range(3):
        v = arr.insert_in_face_interior(Point_2(i, i), unbounded)
    
    print(f"Created {arr.number_of_vertices()} vertices")
    print("Iterating and deleting...")
    
    deleted = 0
    for v in arr.vertices():
        if v.is_isolated():
            print(f"  Deleting vertex at {v.point()}")
            arr.remove_isolated_vertex(v)
            deleted += 1
    
    print(f"\nDeleted: {deleted}, Remaining: {arr.number_of_vertices()}")
    
    if arr.number_of_vertices() == 0:
        print("✅ All deleted successfully")
    else:
        print("⚠️  Some vertices remain (iterator may be affected)")
except Exception as e:
    print(f"❌ CRASH: {type(e).__name__}: {e}")
