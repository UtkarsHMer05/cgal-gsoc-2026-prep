# CGAL Python Bindings — CI/CD Infrastructure Enhancement Plan

**Author:** Utkarsh Khajuria  
**Date:** February 4, 2026  
**GSoC Timeline:** Weeks 11–12  
**Status:** Research Phase Complete

---

## Overview

This document lays out a comprehensive strategy to resurrect and enhance the Continuous Integration infrastructure for the CGAL Python bindings project. The initiative stems from a direct request by mentor Efi Fogel (January 7, 2026), aiming to transform an existing release-only pipeline into a robust, contributor-friendly CI system.

### Where We Stand Today

The repository currently contains a `bitbucket-pipelines.yml` file (867 bytes, last updated Jan 30, 2025). Its sole purpose? **Release automation**—building wheels and publishing to PyPI. There's no automated testing on commits, no multi-version checks, and no crash scenario validation.

### What We're Building

| Goal | Description |
|------|-------------|
| **Build on Every Commit** | Catch issues before they reach the main branch |
| **Multi-Python Testing** | Validate across Python 3.9, 3.11, and 3.12 |
| **Crash Prevention** | Automated testing for segfault scenarios |
| **Fast Feedback Loop** | Contributors get results in under 30 minutes |
| **GitHub-Ready** | Seamless migration path when the repo moves |

**Timeline:** 12 days (Weeks 11–12 of GSoC), organized into three progressive stages.

---

## Current State Analysis

### The Existing Pipeline

Here's what the current `bitbucket-pipelines.yml` actually does:

```yaml
pipelines:
  tags:
    '*':
      - step: Build wheels with cibuildwheel
      - step: Publish to PyPI
```

**Trigger:** Only on git tags (e.g., `v1.0.10`)

**Capabilities:**
- Uses cibuildwheel for cross-platform wheel builds
- Uploads to TestPyPI via Twine
- Requires `TWINE_USERNAME` and `TWINE_PASSWORD` environment variables

**What's Missing:**
- No builds on commits or PRs
- No automated test execution
- No multi-version verification
- No crash scenario detection

### Test Infrastructure Audit

**Location:** `src/python_scripts/cgalpy_examples/`

| Test Script | Purpose |
|-------------|---------|
| `test_pmp.py` | Polygon Mesh Processing |
| `test_stubs.py` | Stub generation |
| `test_sms.py` | Surface mesh simplification |
| `test_property_map.py` | Property map functionality |
| `test_boost_utils_sm.py` | Boost utilities (Surface_mesh) |
| `test_boost_utils_polyhedron.py` | Boost utilities (Polyhedron) |
| `move_release_to_test.py` | Release verification |

> **Note:** These are manual example scripts—not pytest-based. Running `pytest tests/` currently does nothing because the framework doesn't exist yet.

**From My Phase 2 Research (Dec 2025):**
- 7 crash scenario tests (segfault prevention)
- 10 silent corruption tests (geometric validation)
- 15 safe method verification tests
- Precondition exception handling tests

All of these need to be integrated into a proper test suite.

### Build System Deep Dive

The build stack is modern but complex:

| Component | Version/Spec |
|-----------|--------------|
| Build Backend | scikit-build-core |
| Binding Tool | nanobind (2.3.0–2.10.2) |
| Package Manager | Conan 2.0+ |
| Build System | CMake 3.29.6+ |
| C++ Standard | C++17 |
| Python Support | 3.8–3.13 |

**Conan-Managed Dependencies:**
- CGAL 5.0+
- GMP (GNU Multiple Precision)
- MPFR (Multiple Precision Floating-Point)
- Eigen 3.4+
- Boost

The complexity comes from cross-platform profile detection—over 200 lines of CMake handle compiler detection (GCC/Clang/MSVC/AppleClang) and architecture variations (x86_64/ARM64).

### The Docker Problem

The current `Dockerfile` (566 bytes, Dec 17, 2024) looks like this:

```dockerfile
FROM ubuntu:22.04
RUN apt install -y python3 python3-pip
COPY . /usr/src/cgal-python-bindings
RUN pip3 install -v .
```

**This will not work.** It's missing:
- CGAL system dependencies (GMP, MPFR, Eigen, Boost)
- CMake
- A C++ compiler (g++/clang)
- Any test execution

We'll fix this in Stage 3.

---

## The Three-Stage Enhancement Plan

### Stage 1: Basic CI Pipeline (Days 1–4)

**Objective:** Get automated builds running on every commit.

#### Pipeline Configuration

```yaml
image: python:3.11

definitions:
  caches:
    conan: ~/.conan2

pipelines:
  # NEW: Triggers on every push
  default:
    - step:
        name: Build & Test (Python 3.11, Linux)
        image: ubuntu:22.04
        caches:
          - pip
          - conan
        max-time: 30
        script:
          # System dependencies
          - apt-get update
          - apt-get install -y cmake g++ python3 python3-pip git
          
          # Conan setup
          - python3 -m pip install --upgrade pip
          - pip3 install conan>=2.0.0
          - conan profile detect --exist-ok
          
          # Python build tools
          - pip3 install scikit-build-core nanobind pytest
          
          # Build the bindings
          - python3 -m pip install -e . -v
          
          # Run existing tests
          - echo "Running example test scripts..."
          - cd src/python_scripts
          - python3 move_release_to_test.py || echo "Test completed"
          
          # Smoke test
          - python3 -c "import CGALPY; print('Import successful!')"

  # PRESERVED: Release pipeline (unchanged)
  tags:
    '*':
      - step:
          name: Build wheels with cibuildwheel
          # ... (existing release configuration)
```

#### What This Gets Us

- Builds trigger on every push (not just releases)
- Ubuntu 22.04 base (matches cibuildwheel's manylinux_2_28)
- Proper Conan dependency resolution
- Pip and Conan caching for faster subsequent builds
- 30-minute timeout to catch hanging builds
- Complete isolation from the release pipeline

#### Expected Build Time: 15–20 minutes

| Phase | Duration |
|-------|----------|
| Conan dependency download | 5–7 min (cached: ~30 sec) |
| CGAL compilation | 10–15 min |
| Test execution | ~1 min |

#### Technical Hurdles

**Conan Profile Detection**  
The CMakeLists.txt handles this automatically for local builds (lines 99–147), but CI needs to replicate the same logic. Solution: `conan profile detect --exist-ok` handles auto-detection on Ubuntu 22.04.

**Build Performance**  
CGAL is not a fast compile. The Conan cache is critical—it cuts repeated build times by 5–7 minutes.

**System Dependencies**  
Rather than installing system packages (`libcgal-dev`, etc.), we let Conan manage everything. This keeps the CI environment consistent and reproducible.

---

### Stage 2: Multi-Python Matrix (Days 5–8)

**Objective:** Verify compatibility across Python 3.9, 3.11, and 3.12.

#### Matrix Configuration

```yaml
pipelines:
  default:
    - parallel:
        - step:
            name: Python 3.9 - Build & Test
            image: python:3.9-slim
            script:
              # (identical build steps)
        
        - step:
            name: Python 3.11 - Build & Test (Primary)
            image: python:3.11-slim
            script:
              # (identical build steps)
        
        - step:
            name: Python 3.12 - Build & Test
            image: python:3.12-slim
            script:
              # (identical build steps)
```

#### Version Selection Rationale

| Version | Status | Decision |
|---------|--------|----------|
| Python 3.8 | EOL October 2024 | Skip |
| Python 3.9 | Oldest actively used | **Include** |
| Python 3.10 | Covered by adjacent versions | Skip |
| Python 3.11 | Primary development target | **Include** |
| Python 3.12 | Latest stable | **Include** |
| Python 3.13 | Too new (Oct 2024 release) | Skip |

Three versions covers roughly 80% of the Python user base, based on PyPI download statistics.

#### Benefits

- **Parallel execution:** All three builds run simultaneously
- **Slim images:** Faster container pulls
- **Version-specific bugs caught early:** Especially nanobind 3.9/3.12 edge cases

#### Expected Total Time: ~20–25 minutes (parallel)

---

### Stage 3: Crash Tests & Preconditions (Days 9–12)

**Objective:** Integrate the crash scenario tests from my Phase 2 research.

#### New Test Directory Structure

```
tests/
├── __init__.py
├── conftest.py                    # pytest fixtures and markers
├── test_crash_scenarios.py        # 7 segfault prevention tests
├── test_geometric_validation.py   # 10 silent corruption tests
├── test_safe_methods.py           # 15 verified safe method tests
└── test_preconditions.py          # Exception handling validation
```

#### Sample Crash Scenario Test

```python
"""
Crash scenario tests discovered during Phase 2 research (Dec 2025)
Tests precondition validation and handle invalidation safety
"""
import pytest
from CGALPY.Aos2 import Arrangement_2
from CGALPY.Ker import Point_2, Segment_2


class TestCrashScenarios:
    """Tests for methods that previously caused segmentation faults"""
    
    def test_remove_isolated_vertex_on_non_isolated(self):
        """
        Crash Scenario 1: remove_isolated_vertex() on a vertex with edges
        
        Expected: RuntimeError with descriptive message
        Previous: Bus error (killed Python interpreter)
        """
        arr = Arrangement_2()
        unbounded = arr.unbounded_face()
        v = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
        seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
        he = arr.insert_from_left_vertex(seg, v)
        
        assert v.degree() == 1  # Vertex now has an edge
        
        with pytest.raises(RuntimeError, match="not isolated|degree > 0"):
            arr.remove_isolated_vertex(v)
    
    def test_remove_edge_called_twice(self):
        """
        Crash Scenario 2: Calling remove_edge() on an already-removed halfedge
        
        Expected: RuntimeError (handle invalidated)
        Previous: Segmentation fault
        """
        arr = Arrangement_2()
        unbounded = arr.unbounded_face()
        v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
        seg = Segment_2(Point_2(0, 0), Point_2(5, 5))
        he = arr.insert_from_left_vertex(seg, v1)
        
        arr.remove_edge(he)  # First removal succeeds
        
        with pytest.raises(RuntimeError, match="invalidated|deleted|invalid handle"):
            arr.remove_edge(he)  # Second removal must fail gracefully
    
    def test_merge_edge_on_non_adjacent_edges(self):
        """
        Crash Scenario 3: merge_edge() on edges that don't share a vertex
        
        Expected: ValueError (edges must be adjacent)
        Previous: Segmentation fault
        """
        arr = Arrangement_2()
        unbounded = arr.unbounded_face()
        
        # Create two separate, non-adjacent edges
        v1 = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
        v2 = arr.insert_in_face_interior(Point_2(10, 10), unbounded)
        
        seg1 = Segment_2(Point_2(0, 0), Point_2(5, 0))
        seg2 = Segment_2(Point_2(10, 10), Point_2(15, 10))
        
        he1 = arr.insert_from_left_vertex(seg1, v1)
        he2 = arr.insert_from_left_vertex(seg2, v2)
        
        merged_seg = Segment_2(Point_2(0, 0), Point_2(15, 10))
        
        with pytest.raises(ValueError, match="not adjacent|do not share vertex"):
            arr.merge_edge(he1, he2, merged_seg)
```

#### pytest Configuration

```python
# tests/conftest.py
"""pytest configuration for CGAL Python bindings"""
import pytest


@pytest.fixture(scope="session")
def cgalpy_module():
    """Import and verify CGALPY is available"""
    try:
        import CGALPY
        return CGALPY
    except ImportError as e:
        pytest.fail(f"Failed to import CGALPY: {e}")


@pytest.fixture
def fresh_arrangement():
    """Provides a fresh Arrangement_2 for each test"""
    from CGALPY.Aos2 import Arrangement_2
    return Arrangement_2()


def pytest_configure(config):
    """Register custom test markers"""
    config.addinivalue_line("markers", "crash: tests for crash scenario prevention")
    config.addinivalue_line("markers", "corruption: tests for silent corruption detection")
    config.addinivalue_line("markers", "precondition: tests for precondition validation")
```

#### CI Integration

```yaml
pipelines:
  default:
    - parallel:
        - step:
            name: Python 3.11 - Full Test Suite
            image: python:3.11-slim
            script:
              # ... (build steps)
              
              # Run the pytest suite
              - pytest tests/ -v --tb=short --maxfail=5
              
              # Generate coverage (Python 3.11 only)
              - pytest tests/ --cov=CGALPY --cov-report=term
              
              - echo "All tests passed without crashes!"
```

#### Test Coverage Targets

| Category | Count | Purpose |
|----------|-------|---------|
| Crash Prevention | 7 | Segfault scenarios |
| Geometric Validation | 10 | Silent corruption |
| Safe Methods | 15 | Regression protection |
| **Total** | **32+** | |

---

## Fixed Dockerfile

Here's the Dockerfile we actually need:

```dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    git \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Python tooling
RUN python3 -m pip install --upgrade pip && \
    pip3 install conan>=2.0.0 scikit-build-core nanobind pytest pytest-cov

WORKDIR /usr/src/cgal-python-bindings
COPY . .

# Conan profile and build
RUN conan profile detect --exist-ok
RUN python3 -m pip install -e . -v

# Default: run tests
CMD ["pytest", "tests/", "-v"]
```

This Dockerfile can:
- Actually build the bindings (novel concept)
- Run the pytest suite
- Match the CI environment exactly (useful for local debugging)

---

## GitHub Actions Migration Path

Efi mentioned considering a move from Bitbucket to GitHub. Here's the equivalent workflow, ready to go when that happens.

### Workflow File

```yaml
# .github/workflows/ci.yml
name: CI Build & Test

on:
  push:
    branches: [master, develop, 'feature/*']
  pull_request:
    branches: [master]

jobs:
  test:
    name: Python ${{ matrix.python-version }} on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.9', '3.11', '3.12']
        os: [ubuntu-22.04]
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      
      - name: Install Conan
        run: |
          pip install conan>=2.0.0
          conan profile detect --exist-ok
      
      - name: Install build dependencies
        run: pip install scikit-build-core nanobind pytest pytest-cov
      
      - name: Build bindings
        run: pip install -e . -v
      
      - name: Run tests
        run: pytest tests/ -v --tb=short --maxfail=5
      
      - name: Upload coverage
        if: matrix.python-version == '3.11'
        uses: codecov/codecov-action@v3

  release:
    name: Build and publish wheels
    if: startsWith(github.ref, 'refs/tags/v')
    needs: test
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Build wheels
        uses: pypa/cibuildwheel@v2.16
      
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

### Migration Checklist

When the repository moves to GitHub:

- [ ] Copy `.github/workflows/ci.yml` to the repository
- [ ] Add `PYPI_API_TOKEN` to repository secrets
- [ ] Push and verify the workflow runs
- [ ] Add GitHub Actions badge to README
- [ ] Disable Bitbucket Pipelines
- [ ] Test a tag push for release workflow

**Estimated migration time:** ~2 hours (mostly waiting for CI)

---

## Project Timeline

### Week 11 (Days 1–7)

| Day | Task | Deliverable |
|-----|------|-------------|
| 1 | Analyze existing CI, write this plan | This document |
| 2–3 | Implement Stage 1 pipeline | Updated `bitbucket-pipelines.yml` |
| 4 | Local testing and debugging | Working basic CI |
| 5 | Implement Stage 2 (multi-Python) | Parallel matrix builds |
| 6–7 | Test Stage 2, optimize caching | Verified multi-version support |

### Week 12 (Days 8–14)

| Day | Task | Deliverable |
|-----|------|-------------|
| 8 | Create pytest infrastructure | `tests/` directory structure |
| 9 | Write crash scenario tests | `test_crash_scenarios.py` (7 tests) |
| 10 | Write geometric validation tests | `test_geometric_validation.py` (10 tests) |
| 11 | Integrate tests into CI | Stage 3 pipeline update |
| 12 | Create GitHub Actions workflow | `.github/workflows/ci.yml` |
| 13 | Update Dockerfile, documentation | Enhanced Dockerfile, README updates |
| 14 | Final testing, PR submission | Complete CI enhancement PR |

**Total estimated effort:** 12 days (~40 hours)

---

## Success Metrics

### Stage 1

- CI runs on every push to any branch
- Builds complete in under 20 minutes
- Failures produce clear, actionable error messages

### Stage 2

- Three Python versions tested (3.9, 3.11, 3.12)
- Parallel builds keep total time under 25 minutes
- Version-specific issues caught automatically

### Stage 3

- 32+ pytest tests passing
- Zero segfaults in the test suite
- Coverage report generated (target: >80% for tested modules)
- GitHub Actions workflow ready for deployment

### Overall

- CI pipeline fully functional and documented
- Tests prevent regression of previously fixed bugs
- Contributors receive feedback in under 30 minutes
- GitHub migration achievable in under 2 hours

---

## Risk Assessment

### Conan Build Failures in CI

**Likelihood:** Medium | **Impact:** High

Conan profile detection can be finicky in containerized environments.

**Mitigations:**
- Test Conan installation locally first
- Implement aggressive caching
- Fallback plan: Install dependencies via system packages (`libcgal-dev`) if Conan fails

### Build Time Exceeds 30 Minutes

**Likelihood:** Low (with caching) | **Impact:** Medium

**Mitigations:**
- Aggressive caching (pip, Conan, CMake build directory)
- Use slim Python images (saves 2–3 minutes)
- If needed: Split build and test into separate pipeline steps

### pytest Tests Require Precondition Implementation

**Likelihood:** High | **Impact:** Medium

Many crash tests expect specific exception types that haven't been implemented yet.

**Mitigations:**
- Use `pytest.skip()` markers initially
- Tests serve as documentation for expected behavior (Weeks 5–6 implementation)
- Stage 3 focuses on infrastructure, not test count

### Bitbucket Pipelines Resource Limits

**Likelihood:** Low | **Impact:** Low

**Mitigations:**
- Free tier allows 10 parallel builds
- Our 3-version matrix is well within limits
- Fallback: Sequential execution if needed

---

## Future Enhancements

These are **out of scope** for GSoC but worth noting:

| Enhancement | Effort | Requires |
|-------------|--------|----------|
| Cross-platform CI (macOS + Windows) | +1 week | Platform-specific Conan handling |
| Coverage tracking (codecov.io) | +2 days | Coverage badge in README |
| Performance regression testing | +1 week | Benchmark suite |
| Automated documentation builds | +3 days | Sphinx integration |
| Nightly builds against CGAL master | +2 days | Scheduled pipeline |

---

## References

### Documentation

- [Bitbucket Pipelines](https://support.atlassian.com/bitbucket-cloud/docs/get-started-with-bitbucket-pipelines/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [cibuildwheel](https://cibuildwheel.readthedocs.io/)
- [pytest](https://docs.pytest.org/)
- [Conan 2.0](https://docs.conan.io/2.0/)

### Related Work

- Phase 2 crash scenario research (December 25–29, 2025)
- Master Prompt v14.0 (116+ hours of documentation)
- GSoC Proposal timeline (Weeks 11–12)

---

## Contact

**Author:** Utkarsh Khajuria — [utkarshkhajuria55@gmail.com](mailto:utkarshkhajuria55@gmail.com)  
**Mentor:** Efi Fogel — [efifogel@gmail.com](mailto:efifogel@gmail.com)
