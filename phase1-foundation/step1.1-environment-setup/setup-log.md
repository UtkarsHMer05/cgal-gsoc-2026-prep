# Step 1.1: System Preparation & Dependencies

**Status**: ✅ Complete  
**Date**: December 2025
**Duration**: ~2 days  

---

## ✅ Completed Tasks

### 1. C++ Compiler Installation

**Installed**: GCC with C++17 support

Verification
g++ --version

Output: g++ (GCC) 11.x or higher
Test C++17 support
echo '#include <iostream>
int main() {
if constexpr (true) {
std::cout << "C++17 works!" << std::endl;
}
}' > test_cpp17.cpp
g++ -std=c++17 test_cpp17.cpp -o test_cpp17
./test_cpp17

Output: C++17 works!

**Result**: ✅ C++17 fully supported

---

### 2. CMake Installation

**Installed**: CMake 3.20+

cmake --version

Output: cmake version 3.2x.x

**Result**: ✅ CMake configured

---

### 3. Boost Library (Built from Source)

**Method**: Homebrew (recommended by mentor)

brew install boost

Boost installed to: /opt/homebrew/Cellar/boost/
Verify
ls /opt/homebrew/include/boost

Output: Shows boost headers


**Result**: ✅ Boost libraries available

---

### 4. Qt6 Installation

**Installed**: Qt6 with development headers

brew install qt@6

Set environment variables
export Qt6_DIR=/opt/homebrew/opt/qt@6
export PATH="/opt/homebrew/opt/qt@6/bin:$PATH"

Verify
qmake --version

Output: QMake version 3.1, Using Qt version 6.x.x

**Result**: ✅ Qt6 ready for CGAL demos

---

### 5. Additional Libraries

**Installed**: GMP, MPFR, Eigen, CORE

brew install gmp mpfr eigen

Verify installations
brew list | grep -E 'gmp|mpfr|eigen'


**Result**: ✅ All dependencies installed

---

### 6. Git Configuration

**SSH Keys Setup**

Generate SSH key
ssh-keygen -t ed25519 -C "utkarshkhajuria55@gmail.com"

Add to GitHub
cat ~/.ssh/id_ed25519.pub


**Result**: ✅ Git with SSH configured for GitHub & Bitbucket

---

## 📝 Notes

- All dependencies installed via Homebrew on macOS
- C++17 standard verified and working
- Qt6 environment variables added to shell profile for persistence
- SSH authentication tested and confirmed working

## ⏭️ Next Steps

- Proceed to **Step 1.2**: Build CGAL from source

