#!/usr/bin/env python3
"""Test #5: remove_isolated_vertex twice"""
import sys
sys.path.insert(0, '/Users/utkarshkhajuria/cgal-python-bindings/build/src/libs/cgalpy')
from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Segment_2, Point_2

print("=" * 60)
print("Test #5: remove_isolated_vertex twice")
print("=" * 60)

try:
    arr = Arrangement_2()
    unbounded = arr.unbounded_face()
    v = arr.insert_in_face_interior(Point_2(3, 3), unbounded)
    print(f"Created isolated vertex: {v.point()}")
    
    arr.remove_isolated_vertex(v)
    print("First removal: SUCCESS")
    
    print("Attempting second removal on same handle...")
    arr.remove_isolated_vertex(v)
    print("⚠️  Second removal succeeded (handle should be invalid!)")
except Exception as e:
    print(f"❌ CRASH: {type(e).__name__}: {e}")
