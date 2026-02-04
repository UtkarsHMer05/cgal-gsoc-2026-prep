# Conan Profile Detection Issue — Technical Analysis

**Date:** February 4, 2026  
**Platform:** macOS 14.x (Sonoma), Apple Silicon M2  
**Conan Version:** 2.25.2

---

## The Short Version

Conan's `conan profile detect` command picked up Homebrew's GCC instead of Apple Clang on my Mac. This caused GMP to fail during configuration because GCC doesn't know how to navigate macOS SDK paths. It's a known quirk, and there are straightforward fixes—but it's worth documenting since it'll affect CI design.

---

## What Happened

### What Conan Detected

```bash
$ conan profile detect --exist-ok
```

```
detect_api: CC and CXX: /opt/homebrew/bin/gcc-14, /opt/homebrew/bin/g++-14
detect_api: Found gcc 15
detect_api: gcc>=5, using the major as version

Detected profile:
[settings]
arch=armv8
build_type=Release
compiler=gcc
compiler.cppstd=gnu17
compiler.libcxx=libstdc++11
compiler.version=15
os=Macos
```

### What It Should Have Detected

```
[settings]
arch=armv8
build_type=Release
compiler=apple-clang
compiler.cppstd=17
compiler.libcxx=libc++
compiler.version=15
os=Macos
```

The key differences: `compiler=apple-clang` instead of `gcc`, and `libc++` instead of `libstdc++11`.

---

## Why This Happened

### My Environment

```bash
$ which gcc
/opt/homebrew/bin/gcc  # Homebrew-installed GCC 14

$ which clang
/usr/bin/clang  # Apple Clang (Xcode Command Line Tools)

$ clang --version
Apple clang version 15.0.0 (clang-1500.3.9.4)
Target: arm64-apple-darwin23.6.0
```

### Conan's Detection Logic

1. Conan first checks if `CC` and `CXX` environment variables are set (they weren't)
2. Falls back to scanning the `PATH` for compilers
3. Homebrew's `/opt/homebrew/bin` appears in my PATH
4. GCC gets found first → gets selected as the default

### Why GCC + macOS Doesn't Work

macOS SDK paths live in deep Xcode directories:
```
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/...
```

Apple Clang has built-in knowledge of these paths. GCC doesn't. When GMP's configure script tries to compile a test program using GCC, it can't link against macOS system libraries—even though GCC itself runs fine.

---

## The Actual Build Failure

### GMP 6.3.0 Configuration Error

Here's how the failure cascaded:

```
conan install .
├─ gmp/6.3.0: Sources downloaded
├─ gmp/6.3.0: Building from source
└─ gmp/6.3.0: ./configure --prefix=... --enable-cxx
    └─ FAILED: C++ compiler not available
```

### From the config.log

```
configure:5247: checking for C++ compiler version
configure:5256: /opt/homebrew/bin/g++-14 --version
configure:5267: $? = 0
configure:5274: /opt/homebrew/bin/g++-14 -v
configure:5277: $? = 0
configure:5284: /opt/homebrew/bin/g++-14 -V
g++-14: error: unrecognized command line option '-V'
configure:5295: $? = 1
configure:5302: checking whether the C++ compiler works
configure:5344: result: no
configure:5349: error: C++ compiler not available
```

The `-V` flag error is a red herring—the real problem is that when configure tries to compile and link a test program, GCC can't find the macOS system libraries.

---

## How This Affects CI

### Ubuntu CI — Not Affected

On Ubuntu 22.04:

```bash
$ which gcc
/usr/bin/gcc  # System GCC

$ gcc --version
gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
```

Auto-detection works correctly here. GCC is the right choice on Linux.

### macOS CI — Affected

On macOS runners (GitHub Actions or Bitbucket):

```bash
$ which gcc
/usr/local/bin/gcc  # Could be Homebrew GCC
```

If Homebrew GCC is present on the runner, we'll hit the same bug.

### Windows CI — Different Issues

Detection usually works (`compiler=msvc`), but there are edge cases with MinGW and Clang-CL that we'd need to handle separately.

---

## Possible Solutions

### Option A: Commit Explicit Profiles to the Repo

Create platform-specific profiles:

```
conan-profiles/
├── linux-gcc.profile
├── macos-clang.profile
└── windows-msvc.profile
```

Use them in CI:

```bash
conan install . --profile=conan-profiles/macos-clang.profile
```

| Pros | Cons |
|------|------|
| Deterministic | Requires maintenance |
| Version-controlled | Must update for new compiler versions |
| Explicitly cross-platform | |

### Option B: Set Environment Variables Before Detection

```bash
export CC=/usr/bin/clang
export CXX=/usr/bin/clang++
conan profile detect --exist-ok
```

| Pros | Cons |
|------|------|
| Simple | Must document for contributors |
| No profile files needed | Easy to forget in CI scripts |

### Option C: Manual Profile Edit

Detect first, then fix:

```bash
conan profile detect --exist-ok
nano ~/.conan2/profiles/default
# Change compiler=gcc → compiler=apple-clang
# Change compiler.libcxx=libstdc++11 → compiler.libcxx=libc++
```

| Pros | Cons |
|------|------|
| Works immediately | Not automatable |
| | Error-prone |

### Option D: Let CMake Handle It

The existing `CMakeLists.txt` (lines 99–241) already has platform-specific Conan integration. We could modify it to explicitly pass compiler settings:

```cmake
set(COMPILER_SETTING -s compiler=apple-clang)
set(LIBCXX_SETTING -s compiler.libcxx=libc++)
```

| Pros | Cons |
|------|------|
| Leverages CMake's superior detection | More complex CMakeLists.txt |
| Already platform-aware | |

---

## My Recommendation for CI (Weeks 11–12)

### For Linux CI (Primary Target)

Just use auto-detection—it works correctly on Ubuntu:

```yaml
script:
  - conan profile detect --exist-ok
  - python3 -m pip install -e . -v
```

### For macOS CI (If Added Later)

Use Option B (environment variables):

```yaml
script:
  - export CC=/usr/bin/clang
  - export CXX=/usr/bin/clang++
  - conan profile detect --exist-ok
  - python3 -m pip install -e . -v
```

### For Local Development

Document the workaround in the README:

```markdown
### macOS Users: Fixing the Conan Profile

If you have Homebrew GCC installed, Conan may detect the wrong compiler. Check with:

```bash
conan profile show
```

If you see `compiler=gcc`, edit the profile:

```bash
nano ~/.conan2/profiles/default
```

Change:
- `compiler=gcc` → `compiler=apple-clang`
- `compiler.libcxx=libstdc++11` → `compiler.libcxx=libc++`
```

---

## CI Sanity Check

Worth adding this to the pipeline as a verification step:

```yaml
- step:
    name: Verify Conan Profile
    script:
      - conan profile show
      - |
        if [ "$(uname)" = "Darwin" ]; then
          # On macOS, must be apple-clang
          conan profile show | grep "compiler=apple-clang" || exit 1
        elif [ "$(uname)" = "Linux" ]; then
          # On Linux, gcc or clang both OK
          conan profile show | grep -E "compiler=(gcc|clang)" || exit 1
        fi
```

---

## Wrapping Up

This is a known limitation of Conan's auto-detection on macOS when Homebrew compilers are present. The fix is straightforward for CI (use explicit configuration), but it does affect local development workflows—especially for anyone who has both Homebrew GCC and Xcode installed.

**For GSoC Weeks 11–12, the plan is:**

1. Use auto-detection on Linux CI (it works)
2. Document the macOS workaround in the README
3. Add a profile verification step to CI
4. Consider explicit profiles later if we add cross-platform CI