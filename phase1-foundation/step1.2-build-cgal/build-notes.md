# Step 1.2: Build CGAL from Source

**Status**: ✅ Complete  
**Date**: December 2024  
**Duration**: ~1 day  

---

## 📥 1. Clone CGAL Repository

    cd ~
    git clone https://github.com/CGAL/cgal.git
    cd cgal


**Result**: CGAL source code cloned successfully

---

## 📂 2. Understand Directory Structure

    cgal/
    ├── Installation/ # Build and install scripts
    ├── examples/ # Example programs by package
    │ ├── Arrangement_on_surface_2/
    │ ├── Triangulation_2/
    │ └── ...
    ├── demo/ # Qt-based interactive demos
    ├── include/CGAL/ # Header-only library
    └── CMakeLists.txt # Main build configuration


**Key Insight**: CGAL is mostly header-only — templates compiled when you use them!

---

## ⚙️ 3. Configure CMake Build

    cd cgal
    mkdir build
    cd build
    
    Configure with all options
    cmake ..
    -DCMAKE_BUILD_TYPE=Release
    -DWITH_CGAL_Qt6=ON
    -DWITH_CGAL_Core=ON
    -DCMAKE_INSTALL_PREFIX=/usr/local


**Output Example:**
-- Found GMP: /opt/homebrew/lib/libgmp.dylib
-- Found MPFR: /opt/homebrew/lib/libmpfr.dylib
-- Found Boost: /opt/homebrew/lib/cmake/Boost-1.82.0
-- Found Qt6: /opt/homebrew/opt/qt@6
-- Configuring done
-- Generating done


**Result**: ✅ All dependencies detected, build configured

---

## 🔨 4. Build CGAL

Build (parallel jobs for speed)
cmake --build . -j8


This compiles examples and demos and takes ~10–15 minutes.

**Result**: ✅ CGAL built successfully

---

## 📦 5. Install CGAL

sudo cmake --install .


**Installed to:** `/usr/local/include/CGAL/`

Set environment variable:

echo 'export CGAL_DIR=/usr/local' >> ~/.zshrc # or ~/.bashrc
source ~/.zshrc


**Result**: ✅ CGAL installed system-wide

---

## ✅ 6. Verify Installation

**Test Program**: `test_cgal.cpp`

    #include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
    #include <CGAL/point_generators_2.h>
    #include <CGAL/algorithm.h>
    
    #include <iostream>
    #include <vector>
    
    typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
    typedef K::Point_2 Point;
    
    int main() {
      std::vector<Point> points;
      CGAL::Random_points_in_square_2<Point> gen(1.0);

    for (int i = 0; i < 10; ++i) {
        points.push_back(*gen++);
    }

    std::cout << "Generated " << points.size() << " random points" << std::endl;
    std::cout << "First point: " << points[0] << std::endl;
    std::cout << "CGAL installation verified!" << std::endl;

    return 0;
    }



**Compile & Run:**

    g++ -std=c++17 test_cgal.cpp -o test_cgal
    -I/usr/local/include
    -L/usr/local/lib
    -lgmp -lmpfr
    
    ./test_cgal


**Expected Output:**

      Generated 10 random points
      First point: 0.435... 0.782...
      CGAL installation verified!


**Result**: ✅ CGAL working correctly!

---

## 🎯 Configuration Summary

    | Setting | Value | Status |
    |----------|--------|--------|
    | Build Type | Release | ✅ |
    | Qt6 Support | Enabled | ✅ |
    | CORE Support | Enabled | ✅ |
    | Install Location | /usr/local | ✅ |
    | Examples Built | Yes | ✅ |

---

## 💡 Key Learnings

- **Header-only library** — Most CGAL components are templates compiled at use time.  
- **CMake detection** — Properly configured environment variables are critical.  
- **Parallel builds** — Using `-j8` significantly speeds up compilation.  
- **Examples directory** — A gold mine for learning CGAL usage patterns.  

---

## 🔗 Next Steps

Now that CGAL is built, you can:

1. Navigate to `examples/Arrangement_on_surface_2/`  
2. Build and run specific examples  
3. Start learning the 2D Arrangements package 
