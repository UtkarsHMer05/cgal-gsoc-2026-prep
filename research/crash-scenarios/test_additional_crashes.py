#!/usr/bin/env python3
"""
Additional Crash Scenario Testing
Goal: Find more safety issues in CGAL Python bindings
Date: January 5-6, 2026
"""

import sys
sys.path.insert(0, '/Users/utkarshkhajuria/cgal-python-bindings/build/src/libs/cgalpy')

try:
    from CGALPY.Aos2 import Arrangement_2
    from CGALPY.Ker import Segment_2, Point_2
    print("✅ CGAL modules imported successfully\n")
except ImportError as e:
    print(f"❌ ERROR: Cannot import CGAL modules: {e}")
    sys.exit(1)

def setup_basic_arrangement():
    """Create a simple arrangement for testing"""
    arr = Arrangement_2()
    unbounded = arr.unbounded_face()
    
    v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
    seg1 = Segment_2(Point_2(0, 0), Point_2(5, 5))
    he1 = arr.insert_from_left_vertex(seg1, v1)
    
    v2 = he1.target()
    seg2 = Segment_2(Point_2(5, 5), Point_2(10, 10))
    he2 = arr.insert_from_left_vertex(seg2, v2)
    
    return arr, v1, v2, he1, he2

def test_modify_vertex_with_connected_edges():
    """Test: What happens if we modify a vertex that has edges?"""
    print("=" * 60)
    print("Test #1: modify_vertex on vertex with edges")
    print("=" * 60)
    try:
        arr, v1, v2, he1, he2 = setup_basic_arrangement()
        
        print(f"v1 degree: {v1.degree()}")
        print(f"v1 is_isolated: {v1.is_isolated()}")
        print(f"v1 current position: {v1.point()}")
        
        new_point = Point_2(100, 100)
        print(f"\nAttempting to modify vertex to {new_point}...")
        
        v_modified = arr.modify_vertex(v1, new_point)
        
        print(f"✅ SUCCESS: Vertex modified to {v_modified.point()}")
        print(f"⚠️  Edge curve endpoints: {he1.curve().source()} to {he1.curve().target()}")
        print("⚠️  WARNING: Arrangement is now geometrically inconsistent\n")
        return "WARNING"
        
    except Exception as e:
        print(f"❌ CRASH: {type(e).__name__}: {e}\n")
        return "CRASH"

def test_split_edge_with_wrong_point():
    """Test: split_edge with point not on the edge"""
    print("=" * 60)
    print("Test #2: split_edge with wrong point")
    print("=" * 60)
    try:
        arr, v1, v2, he1, he2 = setup_basic_arrangement()
        
        print(f"Original edge: {he1.source().point()} to {he1.target().point()}")
        
        wrong_seg1 = Segment_2(Point_2(0, 0), Point_2(3, 5))
        wrong_seg2 = Segment_2(Point_2(3, 5), Point_2(5, 5))
        
        print(f"Splitting at wrong point: (3, 5) - NOT on the line y=x")
        
        he_new = arr.split_edge(he1, wrong_seg1, wrong_seg2)
        
        print(f"✅ Split succeeded without validation!")
        print(f"⚠️  WARNING: Accepted geometrically invalid split\n")
        return "WARNING"
        
    except Exception as e:
        print(f"❌ CRASH: {type(e).__name__}: {e}\n")
        return "CRASH"

def test_remove_edge_then_access_twin():
    """Test: Access twin() after remove_edge()"""
    print("=" * 60)
    print("Test #3: Access twin after remove_edge")
    print("=" * 60)
    try:
        arr, v1, v2, he1, he2 = setup_basic_arrangement()
        
        twin = he1.twin()
        print(f"Stored twin halfedge before removal")
        
        print(f"\nRemoving edge...")
        arr.remove_edge(he1)
        print("Edge removed successfully")
        
        print(f"\nAttempting to access invalidated twin handle...")
        point = twin.source().point()
        
        print(f"⚠️  WARNING: Accessed invalidated handle, got: {point}\n")
        return "WARNING"
        
    except Exception as e:
        print(f"❌ CRASH: {type(e).__name__}: {e}\n")
        return "CRASH"

def test_merge_edge_non_consecutive():
    """Test: merge_edge with edges that share vertex but wrong order"""
    print("=" * 60)
    print("Test #4: merge_edge with wrong halfedge orientation")
    print("=" * 60)
    try:
        arr, v1, v2, he1, he2 = setup_basic_arrangement()
        
        print(f"he1: {he1.source().point()} -> {he1.target().point()}")
        print(f"he2: {he2.source().point()} -> {he2.target().point()}")
        
        merged_curve = Segment_2(Point_2(0, 0), Point_2(10, 10))
        
        print(f"\nAttempting to merge he1 with he2.twin()...")
        he_merged = arr.merge_edge(he1, he2.twin(), merged_curve)
        
        print(f"✅ Merge succeeded\n")
        return "WARNING"
        
    except Exception as e:
        print(f"❌ CRASH: {type(e).__name__}: {e}\n")
        return "CRASH"

def test_remove_isolated_vertex_twice():
    """Test: remove_isolated_vertex called twice on same vertex"""
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
        
        print("Attempting second removal...")
        arr.remove_isolated_vertex(v)
        
        print("⚠️  WARNING: Second removal succeeded\n")
        return "WARNING"
        
    except Exception as e:
        print(f"❌ CRASH: {type(e).__name__}: {e}\n")
        return "CRASH"

def test_modify_edge_wrong_endpoints():
    """Test: modify_edge with curve that doesn't match vertices"""
    print("=" * 60)
    print("Test #6: modify_edge with mismatched endpoints")
    print("=" * 60)
    try:
        arr, v1, v2, he1, he2 = setup_basic_arrangement()
        
        print(f"Original edge: {he1.source().point()} to {he1.target().point()}")
        
        wrong_curve = Segment_2(Point_2(0, 0), Point_2(7, 7))
        
        print(f"New curve: {wrong_curve.source()} to {wrong_curve.target()}")
        print(f"⚠️  Target mismatch: curve ends at (7,7) but vertex is at (5,5)")
        
        he_modified = arr.modify_edge(he1, wrong_curve)
        
        print(f"✅ Modified without validation!\n")
        return "WARNING"
        
    except Exception as e:
        print(f"❌ CRASH: {type(e).__name__}: {e}\n")
        return "CRASH"

def test_iterator_invalidation():
    """Test: Delete vertices while iterating"""
    print("=" * 60)
    print("Test #7: Iterator invalidation")
    print("=" * 60)
    try:
        arr = Arrangement_2()
        unbounded = arr.unbounded_face()
        
        vertices = []
        for i in range(3):
            v = arr.insert_in_face_interior(Point_2(i, i), unbounded)
            vertices.append(v)
        
        print(f"Created {arr.number_of_vertices()} isolated vertices")
        print(f"Iterating and deleting...")
        
        deleted_count = 0
        for v in arr.vertices():
            if v.is_isolated():
                print(f"  Deleting vertex at {v.point()}")
                arr.remove_isolated_vertex(v)
                deleted_count += 1
        
        print(f"\n✅ Completed")
        print(f"Deleted: {deleted_count}, Remaining: {arr.number_of_vertices()}\n")
        
        if arr.number_of_vertices() > 0:
            return "WARNING"
        else:
            return "SAFE"
        
    except Exception as e:
        print(f"❌ CRASH: {type(e).__name__}: {e}\n")
        return "CRASH"

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  CGAL Python Bindings - Crash Scenario Testing")
    print("=" * 60 + "\n")
    
    results = {}
    
    results["Test 1: modify_vertex on connected vertex"] = test_modify_vertex_with_connected_edges()
    results["Test 2: split_edge with wrong point"] = test_split_edge_with_wrong_point()
    results["Test 3: Access twin after remove_edge"] = test_remove_edge_then_access_twin()
    results["Test 4: merge_edge wrong orientation"] = test_merge_edge_non_consecutive()
    results["Test 5: remove_isolated_vertex twice"] = test_remove_isolated_vertex_twice()
    results["Test 6: modify_edge wrong endpoints"] = test_modify_edge_wrong_endpoints()
    results["Test 7: Iterator invalidation"] = test_iterator_invalidation()
    
    print("\n" + "=" * 60)
    print("  SUMMARY OF RESULTS")
    print("=" * 60 + "\n")
    
    crash_count = 0
    warning_count = 0
    safe_count = 0
    
    for test_name, result in results.items():
        symbol = "❌" if result == "CRASH" else "⚠️ " if result == "WARNING" else "✅"
        print(f"{symbol} {test_name}: {result}")
        
        if result == "CRASH":
            crash_count += 1
        elif result == "WARNING":
            warning_count += 1
        else:
            safe_count += 1
    
    print("\n" + "-" * 60)
    print(f"Total Tests: {len(results)}")
    print(f"Crashes: {crash_count}")
    print(f"Warnings (unsafe but no crash): {warning_count}")
    print(f"Safe: {safe_count}")
    print("-" * 60 + "\n")
