# 🔍 External Docstring Definition Research
**Date:** January 5, 2026  
**Author:** Utkarsh Khajuria  
**Context:** Efi's feedback on PR #1 - docstrings "screen or shadow" the actual binding code

---

## 🎯 The Problem

Efi raised a valid concern: my NumPy-style docstrings are comprehensive (which is good), but they're also *long*. When you're scrolling through the binding code trying to understand the C++ logic, you have to scroll past 30-40 lines of documentation text for each method.

That's frustrating when you just want to see what functions are bound and how.

So I started researching: **Can we move docstrings out of the binding definitions while keeping them attached to the methods?**

---

## 📊 Current State

**File:** `src/libs/cgalpy/lib/arrangement_on_surface_2_bindings.cpp`  
**Total lines:** 1,676  
**Methods with my docstrings:** 5 methods (lines 748, 834, 873, 971, 1008)

### What It Looks Like Now

```cpp
aosc.def("insert_from_left_vertex", aos2::insertfromleftvertex1, 
         py::arg("curve"), py::arg("vertex"), 
         ri, 
         R"pbdoc(
            Insert a curve starting from an existing vertex...
            
            Parameters
            ----------
            curve : X_monotone_curve_2
                The curve to insert...
            vertex : Vertex_handle
                The existing vertex...
            
            Returns
            -------
            Halfedge_handle
                A handle to the new halfedge...
            
            Examples
            --------
            >>> # Example code here...
            
            Notes
            -----
            - Important note 1
            - Important note 2
            
            See Also
            --------
            insert_from_right_vertex : For curves ending at vertices
         )pbdoc");
```

**The issue:** Each method definition spans 40-50 lines total. The actual binding logic is maybe 5-8 lines, buried in a sea of documentation.

When Efi (or anyone) wants to quickly scan what methods are bound and how, they have to scroll through pages of docstrings. That's the "screening/shadowing" problem.

---

## 💡 Three Approaches I Researched

I didn't just pick one approach blindly. I researched three different patterns that other projects use.

---

### 📁 Approach A: Variables at Top of File

**The idea:** Define all docstrings as `const char*` variables at the top of the file, then reference them in the `.def()` calls.

```cpp
// ===================================================================
// DOCSTRINGS SECTION (at top of file, before export_aos())
// ===================================================================

const char* INSERT_FROM_LEFT_VERTEX_DOC = R"pbdoc(
Insert a curve starting from an existing vertex...

Parameters
----------
curve : X_monotone_curve_2
    The curve to insert.
vertex : Vertex_handle
    The existing vertex where the curve starts.

[... full docstring ...]
)pbdoc";

const char* INSERT_FROM_RIGHT_VERTEX_DOC = R"pbdoc(
Insert a curve ending at an existing vertex...
[... full docstring ...]
)pbdoc";

// ... more docstrings ...

// ===================================================================
// BINDING SECTION (much cleaner now!)
// ===================================================================

aosc.def("insert_from_left_vertex", aos2::insertfromleftvertex1, 
         py::arg("curve"), py::arg("vertex"), 
         ri, 
         INSERT_FROM_LEFT_VERTEX_DOC);  // <-- Just a variable reference!

aosc.def("insert_from_right_vertex", aos2::insertfromrightvertex1, 
         py::arg("curve"), py::arg("vertex"), 
         ri, 
         INSERT_FROM_RIGHT_VERTEX_DOC);
```

**✅ Pros:**
- Simple to implement (just move text around)
- All docstrings in one clearly marked section
- Binding code becomes super readable (~6 lines instead of ~45 per method)
- Works with existing build system - no new files
- Easy to find and edit any docstring

**❌ Cons:**
- File is still large (just reorganized, not smaller)
- Need to scroll to top to edit docstrings
- Variable names must be unique across the entire file (not a big deal in practice)

**Readability improvement:** ~85-90% fewer lines in binding section

**My rating:** ⭐⭐⭐⭐ (4/5) - Good balance of simplicity and readability

---

### 📂 Approach B: External Header File

**The idea:** Create a separate header file just for docstrings. Include it in the binding file.

```cpp
// ===================================================================
// NEW FILE: src/libs/cgalpy/lib/arrangement_docstrings.h
// ===================================================================

#ifndef ARRANGEMENT_DOCSTRINGS_H
#define ARRANGEMENT_DOCSTRINGS_H

#define INSERT_FROM_LEFT_VERTEX_DOC R"pbdoc(
Insert a curve starting from an existing vertex...
[full docstring]
)pbdoc"

#define INSERT_FROM_RIGHT_VERTEX_DOC R"pbdoc(
Insert a curve ending at an existing vertex...
[full docstring]
)pbdoc"

// ... all other docstrings ...

#endif
```

```cpp
// ===================================================================
// In arrangement_on_surface_2_bindings.cpp
// ===================================================================

#include "arrangement_docstrings.h"

// Now the binding file is ONLY binding logic:
aosc.def("insert_from_left_vertex", aos2::insertfromleftvertex1, 
         py::arg("curve"), py::arg("vertex"), 
         ri, 
         INSERT_FROM_LEFT_VERTEX_DOC);
```

**✅ Pros:**
- Complete separation of concerns (docs vs bindings)
- Binding file stays focused on binding logic only
- One header can serve multiple binding files if needed
- Docstrings can be edited without touching binding code
- Documentation writers can work independently of binding developers
- Makes future auto-generation from Doxygen easier (structured format already exists)

**❌ Cons:**
- Requires adding a new file to build system
- Need to maintain a separate file
- Uses macros instead of `const char*` (slightly less type-safe)
- Need to open two files when working on both docs and bindings

**Readability improvement:** ~90% fewer lines in main binding file

**My rating:** ⭐⭐⭐⭐⭐ (5/5) - Best separation of concerns

---

### 🏷️ Approach C: Namespace Organization

**The idea:** Use a namespace to group all docstrings, keeping them in the same file but organized.

```cpp
// At top of file
namespace docstrings {
    constexpr const char* insert_from_left_vertex = R"pbdoc(
        Insert a curve starting from an existing vertex...
        [full docstring]
    )pbdoc";
    
    constexpr const char* insert_from_right_vertex = R"pbdoc(
        Insert a curve ending at an existing vertex...
        [full docstring]
    )pbdoc";
    
    // ... more docstrings ...
}

// In binding section:
aosc.def("insert_from_left_vertex", aos2::insertfromleftvertex1, 
         py::arg("curve"), py::arg("vertex"), 
         ri, 
         docstrings::insert_from_left_vertex);
```

**✅ Pros:**
- Clean namespacing prevents naming conflicts
- `constexpr` is more modern C++ than macros
- Still single file (simpler than header approach)
- Good organization

**❌ Cons:**
- Still in same file (file remains large)
- `docstrings::` prefix adds verbosity in binding code
- `constexpr` may have compiler compatibility requirements

**Readability improvement:** ~85% fewer lines in binding section

**My rating:** ⭐⭐⭐ (3/5) - Good, but not as clean as header approach

---

## 📋 Comparison Table

| Approach | Files Changed | Readability | Maintenance | Complexity | Score |
|----------|---------------|-------------|-------------|------------|-------|
| A: Variables at Top | 1 file | High | Easy | Low | 4/5 |
| B: External Header | 2 files (1 new) | Very High | Medium | Medium | 5/5 |
| C: Namespace | 1 file | High | Easy | Low | 3/5 |

---

## 🎯 My Recommendation

### Primary: Approach B (External Header)

For CGAL Python bindings, I think the external header approach is the best long-term choice:

1. **Scalability** - As more methods get documented (40+ remaining), the separation becomes more valuable
2. **Maintainability** - Documentation writers can work independently of binding developers
3. **Common Source Potential** - External headers make it easier to explore auto-generation from Doxygen later (we discussed this possibility)
4. **Industry Pattern** - Many large projects separate documentation from code this way

### Fallback: Approach A (Variables at Top)

If adding a new file creates build complexity or seems like overkill for now, Approach A is a solid compromise:

- Still solves the "screening/shadowing" problem
- Much simpler to implement (just move docstrings to top section)
- Can be transitioned to Approach B later if we decide it's worth it

### Not Recommended: Approach C

While namespace organization is elegant C++, it doesn't provide enough benefit over Approach A to justify the `docstrings::` verbosity everywhere.

---

## 📝 Next Steps (If Approved)

1. **Week 3-4 of GSoC:** Test chosen approach with 5-10 methods
2. **Verify:** Build succeeds, `help()` in Python shows docstrings correctly
3. **Apply:** Convert remaining 30-40 methods to new pattern
4. **Document:** Add pattern to contributing guide for other contributors

---

## ❓ Questions for Efi

1. **Preference:** Which approach aligns better with CGAL's coding style?
2. **Build System:** Any concerns with adding a new header file (Approach B)?
3. **Scope:** Should we apply this to all packages, or just `Arrangement_2` initially?
4. **Common Source:** Does this structure help with the Doxygen auto-generation idea we discussed?

---

## 📌 Status

**Research complete.** Awaiting mentor feedback before implementation.

This is a code organization question, not a functionality question - I want to make sure whatever pattern I use fits with CGAL's existing codebase style before I apply it to 40+ methods.

---

*Last Updated: January 5, 2026*  
*Time Spent: ~2 hours researching patterns and writing this doc*