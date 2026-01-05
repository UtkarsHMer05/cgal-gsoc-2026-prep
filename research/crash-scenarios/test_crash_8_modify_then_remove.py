#!/usr/bin/env python3
"""Test #8: Modify isolated vertex then remove it"""
import sys
sys.path.insert(0, '/Users/utkarshkhajuria/cgal-python-bindings/build/src/libs/cgalpy')
from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Segment_2, Point_2

print("=" * 60)
print("Test #8: Modify isolated vertex location then remove")
print("=" * 60)

try:
    arr = Arrangement_2()
    unbounded = arr.unbounded_face()
    v = arr.insert_in_face_interior(Point_2(5, 5), unbounded)
    print(f"Created isolated vertex at {v.point()}")
    
    # Modify the vertex
    v_modified = arr.modify_vertex(v, Point_2(10, 10))
    print(f"Modified vertex to {v_modified.point()}")
    
    # Try to remove using old handle
    print("Attempting to remove using original handle...")
    arr.remove_isolated_vertex(v)
    print("✅ Removal succeeded")
    
except Exception as e:
    print(f"❌ CRASH: {type(e).__name__}: {e}")
