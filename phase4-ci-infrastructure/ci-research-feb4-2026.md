# CI/CD Infrastructure Research Log

**Date:** February 4, 2026  
**Time:** 8:00 PM – 10:00 PM IST  
**Duration:** 2 hours

---

## How the Evening Went

This is a timestamped log of my hands-on CI research session. The goal was to simulate what a CI build would actually look like—and I found some interesting problems along the way.

---

## Timeline

### 8:00 PM — Getting Started

Navigated to the cgal-python-bindings repo and verified the essentials were in place: `CMakeLists.txt`, `pyproject.toml`, the usual suspects.

### 8:05 PM — Installing Conan

```bash
python3 -m pip install "conan>=2.0.0"
```

Installed `conan-2.25.2` along with `fasteners-0.20` and `patch-ng-1.18.1`. No issues here.

### 8:06 PM — Profile Detection (Where Things Got Interesting)

```bash
conan profile detect --exist-ok
```

This is where I hit my first surprise. Conan detected the wrong compiler:

```
[settings]
arch=armv8
build_type=Release
compiler=gcc                 # ← WRONG (should be apple-clang)
compiler.cppstd=gnu17
compiler.libcxx=libstdc++11  # ← WRONG (should be libc++)
compiler.version=15
os=Macos
```

Conan found Homebrew's GCC (`/opt/homebrew/bin/gcc-14`) instead of Apple Clang. This is going to cause problems—and it did.

### 8:10 PM — Build Attempt

Started a full editable install to see exactly what would happen:

```bash
python3 -m pip install -e . -v 2>&1 | tee build-log.txt
```

**Environment:**
- Platform: macOS M2 (ARM64)
- Python: 3.12.12
- Working directory: `/Users/utkarshkhajuria/cgal-python-bindings`

### 8:12 PM — Watching Dependencies Download

| Package | Version | Status | Time |
|---------|---------|--------|------|
| CGAL | 6.0.1 | Downloaded | ~30 sec |
| Boost | 1.83.0 | Built from source | ~10 min |
| Eigen | 3.4.0 | Downloaded | ~10 sec |
| GMP | 6.3.0 | Built from source | **FAILED** |
| MPFR | 4.2.1 | Built from source | Never reached |
| m4 | 1.4.19 | Downloaded | ~5 sec |
| b2 | 5.4.2 | Downloaded | ~5 sec |

### 8:15 PM — Boost Takes Its Time

Boost started downloading (122.9 MB for `boost_1_83_0.tar.bz2`), then compiling:

```
toolset=clang-darwin
cxxstd=17
threading=multi
link=shared
variant=release
```

Interestingly, Boost picked up Apple Clang correctly (unlike the Conan profile). It compiled with `-stdlib=libc++` and used `-j8` for parallel builds. Build directory ended up at `/Users/utkarshkhajuria/.conan2/p/b/boost0d552ead9e44d/b/build-release`.

This took about 10 minutes—most of the build time right there.

### 8:25 PM — GMP Fails

And here's where it died:

```
configure: error: C++ compiler not available, see config.log for details
```

GMP's configure script trusted the Conan profile (which said GCC), tried to use it, and ran into macOS SDK path incompatibilities. The chain of failure:

```
gmp/6.3.0: Sources downloaded
gmp/6.3.0: Building from source
gmp/6.3.0: ./configure (FAILED)
```

Build stopped here. Never got to MPFR or the actual bindings.

### 8:30 PM — Figuring Out Why

Checked the profile:

```bash
cat ~/.conan2/profiles/default
```

Confirmed: `compiler=gcc` instead of `compiler=apple-clang`.

**Why did Boost work but GMP fail?** Different configuration mechanisms:
- Boost uses its own `user-config.jam` which explicitly specified the Apple Clang toolchain
- GMP's autoconf respects the Conan profile settings, which told it to use GCC
- GCC + macOS SDK paths = doesn't work

### 8:35 PM — Thinking About CI Implications

Some questions that came up:

- **Will this happen on Ubuntu?** Probably not—Ubuntu has real GCC, so the profile would be correct.
- **How do we handle cross-platform compiler selection?** Need explicit profiles per platform.
- **Should CI use Conan or just apt-get?** Trade-off between consistency and simplicity.

**Timing data I collected:**
- Conan dependency download: ~5 minutes
- Boost compilation: ~10 minutes
- Total before failure: ~15 minutes
- Estimated full build: 20–25 minutes

### 8:45 PM — Started Writing Documentation

Began the comprehensive CI enhancement plan. Covered:
- 3-stage implementation strategy
- Platform-specific challenges
- GitHub Actions migration path
- Risk mitigation
- Detailed timeline

Ended up at about 8,000 words.

### 9:20 PM — Drafted Email to Efi

Put together an email summarizing:
- Research findings
- 5 technical questions
- The Conan profile bug details
- Build time data

### 9:52 PM — Email Sent

Subject: *CI Infrastructure Research Complete - Build Testing & Platform Issues*  
Recipient: efifogel@gmail.com  
Status: Awaiting response

---

## Key Discoveries

### 1. Conan's Auto-Detection Can't Be Trusted

On my macOS system, it detected GCC when Apple Clang should have been used. This caused GMP to fail.

**CI implication:** We'll need explicit compiler profiles, not auto-detection.

### 2. Build Times Are Significant

- Boost alone: 10 minutes
- Full build estimate: 20–25 minutes

**CI implication:** Need a 30-minute timeout and aggressive caching.

### 3. Each Platform Has Its Quirks

| Platform | Compiler | Standard Library | Special Considerations |
|----------|----------|------------------|------------------------|
| macOS | Apple Clang | libc++ | SDK paths |
| Linux | GCC or Clang | libstdc++11 | Straightforward |
| Windows | MSVC | Different conventions | Haven't tested yet |

**CI implication:** Explicit profiles for each platform, probably checked into the repo.

### 4. No Real Test Infrastructure

The existing test scripts are manual—not pytest-based. There's no way to just run `pytest tests/` right now.

**CI implication:** Stage 3 needs to build out a proper pytest framework from scratch.

---

## Data Collected

### Build Log

- **Size:** 15,000+ lines
- **Location:** `build-log.txt`
- **Contains:** Full Conan dependency graph, Boost compilation output, GMP failure diagnostics, CMake configuration logs

### Conan Profile

- **Location:** `~/.conan2/profiles/default`
- **Issue:** Detected `compiler=gcc` instead of `compiler=apple-clang`
- **Fix needed:** Manual edit to specify Apple Clang and libc++

### Timing Data

| Phase | Fresh Build | With Cache |
|-------|-------------|------------|
| Conan install | 5–7 min | ~30 sec |
| Boost build | 10 min | Reused |
| GMP build (if fixed) | ~3 min | Reused |
| MPFR build | ~2 min | Reused |
| **Total** | **20–25 min** | **5–10 min** |

---

## The Questions I Asked Efi

### Q1: Compiler Configuration Strategy

Given the profile detection issue, should CI:
- Define explicit Conan profiles per platform (checked into the repo)?
- Use CMake compiler detection and bypass Conan auto-detection?
- Just document the required manual profile edits?

### Q2: Dependency Management

For Ubuntu CI, which approach?
- **Option A:** Conan (portable, consistent, but slow and needs profile management)
- **Option B:** System packages via `apt install libcgal-dev` (fast, simple, but version risk)

### Q3: Test Framework Timing

When should I convert the manual scripts to pytest?
- During Weeks 11–12 (the CI work)?
- Or defer to post-GSoC?

### Q4: Build Matrix Size

Test 3 Python versions (~25 min parallel) or go for full coverage with 6 versions (~45 min)?

### Q5: Crash Test Integration

The 7 crash scenarios from my Phase 2 research—integrate them now during Weeks 11–12, or wait until the precondition implementation in Weeks 5–6?

---

## What's Next

### Tonight (Done)

- Saved build log to prep repo
- Documented research findings
- Created phase4 directory structure
- Updated master prompt

### Tomorrow (If No Response)

- Optional: Compare how other projects (nanobind, other CGAL packages) handle CI
- Optional: Fix the Conan profile manually and retry the build
- No follow-up email—give it at least 48 hours

### When Efi Responds

- Address any questions or concerns
- Continue research based on guidance
- Refine the CI enhancement plan accordingly

---

## Files Generated Tonight

| File | Description |
|------|-------------|
| `ci-enhancement-plan.md` | 8,000-word implementation guide |
| `build-log.txt` | 15,000+ lines of diagnostic output |
| `email-to-efi-feb4.md` | Copy of the email I sent |
| `conan-profile-issue.md` | Deep dive on the compiler bug |
| This file | Complete research log |

---

## Session Summary

This research phase accomplished what I set out to do:

- Identified a critical CI blocker (the compiler detection issue)
- Gathered concrete timing data for CI pipeline design
- Created an actionable 12-day implementation plan
- Formulated specific technical questions for Efi
- Documented platform-specific challenges I'll face

**Total time invested in GSoC prep:** 118 hours (116 previous + 2 tonight)