# Email to Efi Fogel - February 4, 2026

**Date:** February 4, 2026, 9:52 PM IST  
**From:** Utkarsh Khajuria (utkarshkhajuria55@gmail.com)  
**To:** Efi Fogel (efifogel@gmail.com)  
**Subject:** CI Infrastructure Research Complete - Build Testing & Platform Issues  
**Status:** SENT

---

## Email Content

Hi Efi,

I've completed the CI infrastructure research and hands-on build testing we discussed for Weeks 11-12. I discovered some critical platform-specific challenges that will affect CI design.

### **Research Completed:**

1. **Current CI Analysis:**
   - Analyzed `bitbucket-pipelines.yml` (867 bytes) - currently release-only (wheel building + PyPI publish)
   - No automated testing on commits/PRs
   - Missing: build verification, test suite execution, multi-Python coverage

2. **Build System Testing:**
   - Tested full Conan-based build process locally (simulating CI environment)
   - Documented dependency chain: CGAL 6.0.1, Boost 1.83.0, GMP 6.3.0, MPFR 4.2.1, Eigen 3.4.0
   - Build logs captured (15,000+ lines with detailed error diagnostics)

3. **Test Infrastructure Audit:**
   - Found test scripts in `src/python_scripts/` (test_pmp.py, move_release_to_test.py, etc.)
   - Currently manual execution scripts, not pytest-based automated tests
   - Need pytest framework integration for CI

### **Key Findings & CI Challenges:**

**Challenge 1: Conan Compiler Detection Issue**
During build testing, I discovered a critical platform-specific bug:

Conan Profile Detected:
compiler=gcc
compiler.libcxx=libstdc++11

Expected for macOS:
compiler=apple-clang
compiler.libcxx=libc++

text

**Result:** GMP 6.3.0 build failed with:
configure: error: C++ compiler not available

text

**Root cause:** Conan's `conan profile detect` picked up Homebrew GCC instead of Apple Clang, causing SDK path incompatibility.

**CI Implication:** Auto-detection is unreliable. CI pipelines need **explicit compiler configuration**, especially for cross-platform testing (Linux/macOS/Windows).

**Challenge 2: Build Time**
- Boost 1.83.0 builds from source: ~10 minutes (122.9MB download + compilation)
- Total build time estimate: 15-20 minutes minimum
- **CI Implication:** Need 25-30 minute pipeline timeout + aggressive caching strategy

**Challenge 3: Dependency Strategy Choice**
- **Option A:** Conan (portable, version-controlled, but slow + profile management complexity)
- **Option B:** System packages (`apt install libcgal-dev`, fast but version risk)
- Current setup uses Conan; CI needs consistent approach

### **Questions for CI Design:**

**Q1: Compiler Configuration Strategy**
Given the Conan profile detection issue, for CI should we:
- Define explicit Conan profiles per platform (Linux/macOS) in repo?
- Or use CMake's compiler detection and bypass Conan's auto-detection?

**Q2: Dependency Management Approach**
For CI builds on Ubuntu (manylinux_2_28):
- Continue with Conan (consistency but 20-min builds, requires caching)?
- Or use system packages (5-min builds, simpler setup)?

**Q3: Test Framework Migration**
The existing test scripts in `src/python_scripts/` need pytest conversion for automated CI. Should this be:
- Part of Weeks 11-12 CI work (higher priority)?
- Or deferred to post-GSoC (keep current manual tests)?

**Q4: Build Matrix Scope**
For multi-Python testing:
- **Conservative:** Python 3.9, 3.11, 3.12 (3 versions, ~25 min parallel)
- **Comprehensive:** Python 3.8-3.13 (6 versions, ~45 min parallel)

**Q5: Crash Scenario Tests Integration**
The 7 crash scenarios I documented in December - should these be:
- Integrated during Weeks 11-12 as pytest tests?
- Or wait until Weeks 5-6 after precondition implementation?

### **Proposed CI Enhancement Plan:**

I've drafted a complete 12-day implementation plan with 3 stages:
- **Stage 1 (Days 1-4):** Basic pipeline - automated build + test on every commit
- **Stage 2 (Days 5-8):** Multi-Python matrix with explicit compiler configs
- **Stage 3 (Days 9-12):** pytest infrastructure + crash tests + documentation

I also prepared a GitHub Actions equivalent workflow (migration-ready if repo moves from Bitbucket).

### **Documentation Ready:**

I've created a comprehensive CI Enhancement Plan document (~8,000 words) covering:
- Current state analysis
- Three-stage implementation plan
- Platform-specific challenges (like the Conan profile issue)
- Enhanced Dockerfile
- GitHub Actions migration guide
- Timeline breakdown (12 days, ~40 hours)
- Risk mitigation strategies

### **Next Steps:**

Your guidance on the questions above will help me finalize the technical approach. Once I have your input, I can:
1. Fix the local Conan profile and complete build testing
2. Update the proposal with specific CI technical details
3. Prepare concrete implementation code for Weeks 11-12

The hands-on testing revealed platform-specific challenges that the current pipeline doesn't address. The compiler detection issue alone could cause silent CI failures across different environments.

Best regards,  
Utkarsh

---

## Expected Response Timeline

- **Sent:** Feb 4, 9:52 PM IST = 4:22 PM UTC = 6:22 PM Israel time
- **Efi's timezone:** Israel (UTC+2)
- **Expected response:** Within 24-48 hours (by Feb 6, evening IST)
- **Follow-up if needed:** Not before Feb 7 (72 hours minimum)

---
