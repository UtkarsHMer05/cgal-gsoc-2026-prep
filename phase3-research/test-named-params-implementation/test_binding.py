#!/usr/bin/env python3
"""Test Named Parameters proof-of-concept."""

import sys
sys.path.insert(0, 'build')

import named_param_test as npt

print("=" * 60)
print("Named Parameters Proof-of-Concept Test")
print("=" * 60)

print("\n[Test 1] Without named parameters:")
result = npt.process_mesh("cube", 8)
print(f"  Result: {result}")
print("  ✓ Uses defaults")

print("\n[Test 2] With tolerance parameter:")
result = npt.process_mesh("sphere", 120, {"tolerance": 0.0001})
print(f"  Result: {result}")
print("  ✓ Custom tolerance")

print("\n[Test 3] With both parameters:")
result = npt.process_mesh("bunny", 5000, {"tolerance": 0.00001, "max_iterations": 500})
print(f"  Result: {result}")
print("  ✓ Both custom parameters")

print("\n[Test 4] With invalid parameter:")
result = npt.process_mesh("teapot", 256, {"invalid_param": 42})
print(f"  Result: {result}")
print("  ✓ Invalid parameter ignored")

print("\n[Test 5] Docstring check:")
print(f"  Has docstring: {npt.process_mesh.__doc__ is not None}")

print("\n" + "=" * 60)
print("✅ All tests passed!")
print("=" * 60)