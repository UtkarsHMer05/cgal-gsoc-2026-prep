import cgalpy

arr = cgalpy.Arrangement_2()

p1 = cgalpy.Point_2(0, 0)
p2 = cgalpy.Point_2(1, 0)
p3 = cgalpy.Point_2(0, 1)

seg1 = cgalpy.Segment_2(p1, p2)
seg2 = cgalpy.Segment_2(p1, p3)

cgalpy.insert(arr, seg1)
cgalpy.insert(arr, seg2)

print(f"Vertices: {arr.number_of_vertices()}")   # 3
print(f"Edges: {arr.number_of_edges()}")          # 2
print(f"Faces: {arr.number_of_faces()}")          # 2 (1 bounded + 1 unbounded)
