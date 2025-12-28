# Part A: Introduction and Research Methodology

**CGAL Arrangement_2 Python Bindings - Deep Empirical Analysis of 25+ Methods**

---

**Author**: Utkarsh Khajuria  
**Institution**: VIT Chennai (3rd Year CS)  
**Project**: CGAL GSoC 2026 - Enhancing Python Bindings  
**Research Period**: December 27-28, 2025  
**Total Research Time**: ~10 hours  
**Methods Tested**: 25+ methods across 4 categories  
**Test Code Written**: ~800 lines  
**Test Files**: 3 comprehensive test suites  
**Python Version**: 3.12.7  
**Platform**: macOS (Apple Silicon M1)  
**CGAL Version**: Development build from source  

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Research Methodology](#research-methodology)
3. [Part B: Specialized Insertion Methods](./part-b-insertion-methods.md)
4. [Part C: Removal Methods](./part-c-removal-methods.md)
5. [Part D: Modification Methods](./part-d-modification-methods.md)
6. [Part E: Query and Traversal Methods](./part-e-query-methods.md)
7. [Part F: Critical Safety Issues](./part-f-safety-issues.md)
8. [Part G: Patterns and Design Philosophy](./part-g-patterns.md)
9. [Part H: Recommendations](./part-h-recommendations.md)
10. [Appendix A: Complete Test Results](./appendix-a-test-results.md)
11. [Appendix B: Research Statistics](./appendix-b-statistics.md)

---

## Executive Summary

This document presents the results of hands-on empirical research on 25+ `Arrangement_2` methods in CGAL's Python bindings. Instead of trusting documentation blindly, I wrote test code, broke things on purpose, and documented exactly what happens in the real world.

### The Big Discovery: Zero Validation by Design

Here's what I didn't expect—**ALL specialized methods** (insertion, removal, modification) perform **ZERO precondition validation**. This isn't a bug. It's how CGAL was designed for maximum performance in C++. But in Python, this creates severe problems:

1. Python developers expect exceptions when something goes wrong, not silent corruption or crashes
2. Segmentation faults are completely unacceptable in Python (in C++, they're almost expected for undefined behavior)
3. There's no compile-time type checking to catch mistakes early
4. Dynamic typing makes it way too easy to pass wrong arguments

### Safety Impact Summary

| Method Category | Methods Tested | Validation Level | Crash Risk | Corruption Risk | Python Safety Rating |
|----------------|----------------|------------------|------------|-----------------|---------------------|
| **Insertion** | 4 methods | ❌ None | Low | 🔴 High | 🔴 Unsafe |
| **Removal** | 2 methods | ❌ None | 🔴 SEGFAULT | 🔴 High | 🔴 Dangerous |
| **Modification** | 4 methods | ❌ None | 🔴 SEGFAULT | 🔴 High | 🔴 Dangerous |
| **Query/Traversal** | 15+ methods | N/A (read-only) | ✅ None | ✅ None | ✅ Safe |

### Key Discoveries

These are the things that surprised me during testing:

1. **Discovery #1-2**: Insertion methods happily accept duplicate points at the same coordinates, mismatched curve endpoints, and overlapping segments—no complaints, no errors, just silent corruption

2. **Discovery #3-4**: The Python bindings are missing optional parameters that exist in C++ (like the `remove_edge` control flags for keeping vertices)

3. **Discovery #5**: Calling `remove_isolated_vertex()` on a vertex that has edges = instant Python crash (bus error). Not an exception—the interpreter just dies

4. **Discovery #6-8**: After you remove something, the old Python handles still "work" but they return garbage data from freed memory, or just crash when you try to use them

5. **Discovery #9-10**: Modification methods accept geometrically impossible inputs without blinking—you can set a curve that doesn't match the vertex positions

6. **Discovery #11-12**: Using handles after their underlying DCEL elements have been deleted causes immediate SEGFAULT

7. **Discovery #13**: Query methods are uniformly safe (read-only, well-behaved)—the only category where nothing bad can happen

### Research Impact

This research has documented:
- **12 major safety issues** that need prominent documentation in docstrings
- **5 scenarios** that crash the Python interpreter (SEGFAULT/bus error, not catchable)
- **10+ scenarios** that silently corrupt your arrangement data structure
- **2 missing API features** compared to the C++ version
- **0 crashes in query methods** (baseline for comparison—proves the problem is with modification methods)

---

## Research Methodology

### Approach: Break Things First, Document After

I didn't just read the CGAL manual and copy it into docstrings. That's how bad documentation gets written. Instead, I adopted a **test-driven documentation** approach:

1. **Hypothesis Formation**: Read the CGAL C++ docs, form expectations about what should happen
2. **Test Design**: Create minimal reproducible test cases that verify the documented behavior
3. **Boundary Testing**: Test edge cases and precondition violations—what happens at the limits?
4. **Failure Analysis**: Intentionally violate every precondition to discover what validation exists (spoiler: none)
5. **Documentation**: Record what actually happens, not what should happen according to docs

### Test Environment Setup

```python
import sys
sys.path.insert(0, '/Users/utkarshkhajuria/cgal-python-bindings/build/src/libs/cgalpy')

from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Segment_2, Point_2
```

**Build Configuration**:
- **Compiler**: Apple Clang 16.0.0
- **nanobind**: Latest version via conda
- **Build flags**: `-DCGALPY_ARRANGEMENT_ON_SURFACE_2_BINDINGS=ON`
- **Python**: 3.12.7
- **macOS**: Sonoma on Apple Silicon M1

### Testing Philosophy

> "If a method has a precondition in the C++ docs, I test what happens when you violate it. If it crashes, I document the crash. If it silently accepts bad input, I document the corruption. Only empirical testing reveals the truth about how software actually behaves."

This might sound paranoid, but it's exactly how I found every issue documented in this research. Documentation often describes intended behavior, but implementation doesn't always match intention.

### Why This Matters

The CGAL C++ documentation is excellent—but it's written for C++ programmers who expect:
- To read and understand preconditions thoroughly
- Undefined behavior when preconditions are violated
- Compile-time type checking to catch some errors
- Manual memory management awareness

Python programmers have different expectations:
- Exceptions should be raised for invalid input
- Crashes (segfaults) should never happen—the interpreter should catch errors
- Duck typing means fewer compile-time checks, so runtime validation matters more
- Garbage collection should handle memory, not dangling references

This mismatch is why empirical testing is essential.

---

## Document Organization

This research is split into multiple files for easier reading and navigation:

| File | Content | What You'll Learn |
|------|---------|-------------------|
| [Part A](./part-a-introduction.md) | Introduction & Methodology | Research approach, executive summary |
| [Part B](./part-b-insertion-methods.md) | Specialized Insertion Methods | 4 methods, all accept invalid input |
| [Part C](./part-c-removal-methods.md) | Removal Methods | 2 methods, instant crashes possible |
| [Part D](./part-d-modification-methods.md) | Modification Methods | 4 methods, geometric inconsistency |
| [Part E](./part-e-query-methods.md) | Query & Traversal Methods | 15+ methods, all safe! |
| [Part F](./part-f-safety-issues.md) | Critical Safety Issues | All crash/corruption scenarios |
| [Part G](./part-g-patterns.md) | Patterns & Design Philosophy | Why CGAL is designed this way |
| [Part H](./part-h-recommendations.md) | Recommendations | For users, maintainers, GSoC contributors |
| [Appendix A](./appendix-a-test-results.md) | Complete Test Output | Full terminal output from all tests |
| [Appendix B](./appendix-b-statistics.md) | Research Statistics | Time logs, code counts, timeline |

---

**Next**: [Part B - Specialized Insertion Methods →](./part-b-insertion-methods.md)
