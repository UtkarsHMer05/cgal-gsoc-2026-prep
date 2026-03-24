"""
Weeks 3-4 docstring verification test.

Checks that every bound method and free function in the Aos2 module
has a real docstring (not just a signature).

Run from the repo root:
    export PYTHONPATH=../../build-manual/src/libs/cgalpy
    python3 verification_test.py
"""

import sys

try:
    import CGALPY as cgalpy
except ModuleNotFoundError:
    print("ERROR: CGALPY not found.")
    print("Set: export PYTHONPATH=../../build-manual/src/libs/cgalpy")
    sys.exit(1)

arr = cgalpy.Aos2.Arrangement_2()


def get_doctext(obj, method_name):
    """Return (has_text, preview) for a given method's docstring."""
    fn = getattr(obj, method_name, None)
    if fn is None:
        return None, "NOT FOUND"

    doc = (fn.__doc__ or "").strip()
    lines = [l.strip() for l in doc.split("\n") if l.strip()]

    # Skip lines that are just the signature or overload boilerplate
    text = next(
        (l for l in lines
         if not l.startswith(method_name)
         and not l.startswith("Overloaded")
         and not l.startswith("1.")
         and not l.startswith("``")
         and not l.startswith("self")),
        None
    )
    return bool(text), (text[:72] if text else "SIGNATURE ONLY")


print("=" * 76)
print("Weeks 3-4 Docstring Verification")
print("=" * 76)

class_methods = [
    ("Query",        ["number_of_vertices", "number_of_edges", "number_of_faces",
                      "number_of_halfedges", "number_of_isolated_vertices",
                      "number_of_unbounded_faces", "is_empty", "is_valid",
                      "assign", "clear"]),
    ("Iterators",    ["vertices", "halfedges", "edges", "faces", "unbounded_faces"]),
    ("Insertion",    ["insert_from_left_vertex", "insert_from_right_vertex",
                      "insert_in_face_interior", "insert_at_vertices"]),
    ("Modification", ["modify_vertex", "modify_edge", "split_edge",
                      "merge_edge", "remove_edge", "remove_isolated_vertex"]),
]

passed = 0
total = 0

for section, methods in class_methods:
    print(f"\n  [{section}]")
    for m in methods:
        ok, text = get_doctext(arr, m)
        status = "OK" if ok else "XX"
        print(f"    {status}  {m:35s}  {text}")
        if ok:
            passed += 1
        total += 1

print(f"\n  Class methods: {passed}/{total}")

print("\n  [Free Functions -- cgalpy.Aos2]")
free_fns = [
    "insert_point", "insert_non_intersecting_curve",
    "insert_non_intersecting_curves", "insert",
    "do_intersect", "decompose", "zone",
    "remove_edge", "remove_vertex",
]

passed_free = 0

for fn_name in free_fns:
    ok, text = get_doctext(cgalpy.Aos2, fn_name)
    if ok is None:
        print(f"    XX  {fn_name:35s}  NOT FOUND IN MODULE")
        continue
    status = "OK" if ok else "XX"
    print(f"    {status}  {fn_name:35s}  {text}")
    if ok:
        passed_free += 1

print(f"\n  Free functions: {passed_free}/{len(free_fns)}")

print()
grand_total = passed + passed_free
grand_expected = total + len(free_fns)
print("=" * 76)
print(f"TOTAL: {grand_total}/{grand_expected} methods verified")
if grand_total == grand_expected:
    print("ALL DOCSTRINGS CONFIRMED LIVE")
print("=" * 76)