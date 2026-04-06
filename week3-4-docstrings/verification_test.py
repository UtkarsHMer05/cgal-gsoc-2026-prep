#!/usr/bin/env python3
"""
verification_test.py
====================
Runtime __doc__ spot-check for all 5 docstring packages.

Run from repo root after building:
    PYTHONPATH=build-manual/src/libs/cgalpy python3 \
        week3-4-docstrings/verification_test.py

Expected: all 15 checks pass.
"""

import sys

CHECKS = [
    # (dotted attribute path after CGALPY,  label)
    ("Pol2.Polygon_2.is_simple",                          "Pol2 — is_simple"),
    ("Pol2.Polygon_2.orientation",                        "Pol2 — orientation"),
    ("Pol2.Polygon_2.area",                               "Pol2 — area"),
    ("Pol2.Polygon_2.is_counterclockwise_oriented",       "Pol2 — is_counterclockwise_oriented"),
    ("Pol2.Polygon_2.edge",                               "Pol2 — edge"),
    ("As2.Alpha_shape_2.alpha",                           "As2 — alpha"),
    ("As2.Alpha_shape_2.classify",                        "As2 — classify"),
    ("Bso2.join",                                         "Bso2 — join"),
    ("Bso2.intersection",                                 "Bso2 — intersection"),
    ("Env2.lower_envelope_x_monotone_curves",             "Env2 — lower_envelope_x_monotone"),
    ("Vis2.Simple_polygon_visibility_2.attach",           "Vis2 — attach"),
    ("Vis2.Simple_polygon_visibility_2.compute_visibility","Vis2 — compute_visibility"),
    ("Aos2.Arrangement_2.number_of_vertices",             "AOS2 — number_of_vertices"),
    ("Aos2.Arrangement_2.insert_from_left_vertex",        "AOS2 — insert_from_left_vertex"),
    ("Aos2.Arrangement_2.clear",                          "AOS2 — clear"),
]


def main():
    try:
        import CGALPY
    except ImportError as e:
        print(f"ERROR: Cannot import CGALPY: {e}")
        print("Run with: PYTHONPATH=build-manual/src/libs/cgalpy python3 ...")
        sys.exit(1)

    print("=" * 60)
    print("CGALPY __doc__ verification — all 5 packages")
    print("=" * 60)

    passed = failed = 0
    prev_pkg = None

    for attr_path, label in CHECKS:
        pkg = label.split("—")[0].strip()
        if pkg != prev_pkg:
            print(f"\n--- {pkg} ---")
            prev_pkg = pkg

        try:
            obj = CGALPY
            for part in attr_path.split("."):
                obj = getattr(obj, part)
            doc = getattr(obj, "__doc__", None)
            if doc and len(doc.strip()) > 5:
                print(f"  [PASS] {label}")
                passed += 1
            else:
                print(f"  [FAIL] {label} — __doc__ empty or missing")
                failed += 1
        except AttributeError as e:
            print(f"  [FAIL] {label} — AttributeError: {e}")
            failed += 1

    print()
    print("=" * 60)
    print(f"TOTAL: {passed}/{passed+failed} passed")
    print("All checks PASSED ✅" if failed == 0 else f"{failed} FAILED ❌")
    print("=" * 60)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()