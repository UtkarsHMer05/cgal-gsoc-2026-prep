# 🎯 CGAL GSoC 2026 Preparation Repository

**Project:** CGAL Python Bindings Enhancement  
**Applicant:** Utkarsh Khajuria  
**Mentor:** Efi Fogel  
**Preparation Period:** December 20-27, 2025

---

## 📌 Current Status

### ✅ FIRST PR SUBMITTED - December 27, 2025, 12:51 AM IST

Opened first contribution PR to CGAL Python bindings: **"Add docstrings for Arrangement_2 insertion methods"**

- **PR Status:** Awaiting review from Efi Fogel
- **What Changed:** Docstrings + named parameters for 6 core insertion methods
- **Lines Changed:** Clean, focused diff (avoided formatting explosion)

🔗 **PR Link:** [Bitbucket PR #1](https://bitbucket.org/taucgl/cgal-python-bindings/pull-requests/)  
📝 **Proposal Link:** [Google Docs - Commenting Access](https://docs.google.com/document/d/1XL1RYG9U-9OJlXU0i78VNDTHCz3OLBPHnfQPgQmCfz4/edit?usp=sharing)

---

## 🚀 Why This Project?

I stumbled into CGAL when I needed 2D arrangement algorithms for a personal project. The C++ API was beautiful—elegant template metaprogramming, trait classes, policy-based design. But when I tried the Python bindings, I hit a wall.

No docstrings. Generic `arg0`, `arg1` parameter names. Comments like `//! \todo Why the f... reference_internal doesn't work?` on line 857.

That's when it clicked: **great architecture means nothing if users can't figure out how to use it.**

I'm not here just for a summer internship. I want to make CGAL's Python bindings actually usable for people who need computational geometry but don't want to read C++ source code.

---

## 📚 Phase 1: My Preparation Journey (50+ Hours, Dec 20-24)

### Day 1: Environment Setup (December 20, 2025)

**What I did:**
- Built CGAL from source on my MacBook Air M1
- Wrestled with Qt6, Boost, and CORE dependencies
- Configured CMake with Python bindings enabled
- Compiled and verified installation with test programs

**What I learned:**
- CGAL's build system is complex but well-documented
- Dependencies matter—wrong Boost version breaks everything
- Building from source gives me full control for debugging

**Time spent:** ~8 hours (most of it debugging Qt6 linking issues)

**Evidence:** Successfully compiled CGAL examples in `/examples/Arrangement_2/`

---

### Day 2: Mastering 2D Arrangements (December 21, 2025)

**What I did:**
- Studied DCEL (Doubly-Connected Edge List) data structure
- Built and ran 3 C++ examples:
  - `incremental_insertion.cpp` - Basic curve insertion
  - `point_location.cpp` - Finding faces containing points
  - `edge_insertion.cpp` - Advanced insertion patterns
- Wrote 600+ lines of architecture analysis

**What I learned:**

**DCEL Structure:**
- Vertices store geometric points
- Halfedges are directed edges with twin pointers
- Faces represent regions bounded by edges
- Everything links bidirectionally

**Traits Classes:**
- `Arr_segment_traits_2` for line segments
- `Arr_circle_segment_traits_2` for circular arcs
- Traits define how curves behave (intersections, comparisons)

**Insertion Methods (15+ different ones!):**
- `insert_in_face_interior()` - For isolated points
- `insert_from_left_vertex()` - Connect to existing vertex
- `insert_at_vertices()` - Connect two existing vertices
- `insert()` - General insertion with automatic splitting

**Why This Matters:**  
Understanding the C++ architecture helps me write better Python documentation. I know *WHY* each method exists and *WHEN* to use it.

**Time spent:** ~12 hours

**Evidence:** Detailed analysis document covering template structure, type system, and use cases

---

### Day 3: Exploring Python Bindings Repository (December 22, 2025)

**What I did:**
- Cloned `cgal-python-bindings` from Bitbucket
- Analyzed binding code in `src/libs/cgalpy/lib/`
- Studied 50+ bound methods in Arrangement_2
- Found 70+ Python examples in `/examples/` directory

**What I discovered:**

**The Good:**
- 2D/3D Arrangements: ~80% complete
- 13+ geometry types supported
- Examples exist for most features
- Pythonic iteration works well

**The Gaps:**
- 90% of methods have NO docstrings
- Most show `arg0`, `arg1`, `arg2` instead of parameter names
- No IDE autocomplete (missing `.pyi` type stubs)
- Some functions commented out (lifetime management issues)

**Specific Finding - Line 857:**

Found frustrated TODO comment in `arrangement_on_surface_2_bindings.cpp`:

```cpp
//! \todo Why the f... reference_internal doesn't work?
m.def("insert", &aos2::insert_cv_with_history, ref);
```

Currently using bare `ref` policy as workaround—dangerous for memory management.

**Time spent:** ~10 hours (reading code, testing examples)

**Evidence:**

```bash
# Verified this myself:
grep -n "todo" arrangement_on_surface_2_bindings.cpp
# Line 857: //! \todo Why the f... reference_internal doesn't work?
```

---

### Day 4: Learning Nanobind (December 23-24, 2025)

**What I did:**
- Read nanobind documentation cover-to-cover
- Discovered CGAL uses nanobind with migration alias: `namespace py = nanobind;`
- Studied return value policies and lifetime management
- Analyzed the line 857 bug in detail

**What I learned:**

**Return Value Policies:**
- `reference_internal` - Most common, keeps parent alive
- `copy` - Makes independent copy
- `take_ownership` - Python owns the object
- `reference` - Bare reference (dangerous without lifetime management)

**Lifetime Management:**
- `keep_alive<0, 1>` - Keep argument 1 alive while return value exists
- `keep_alive<1, 2>` - Keep argument 2 alive while argument 1 exists
- Critical for iterators and handles

**The Line 857 Problem:**

`insert_cv_with_history` returns a handle to curve history, but `reference_internal` doesn't work. Why?

**My Hypothesis:**
- Returned object might not be owned directly by `self` (the Arrangement)
- Could be multi-owner scenario (Arrangement + Curve_history)
- Might need custom `keep_alive` chains

**Time spent:** ~12 hours

**Evidence:** Line 857 verified in actual source code, not just documentation

📖 **Detailed Nanobind Learning Notes:** See `NANOBIND_DEEP_DIVE.md`

---

### Day 5: Writing the Proposal (December 24, 2025)

**What I did:**
- Read successful GSoC proposals from past years
- Studied Tarun's winning proposals (Red Hen Lab, caMicroscope)
- Drafted comprehensive proposal with 2-week timeline
- Created architecture diagrams showing binding layers
- Verified all technical claims before submission
- Restructured timeline from 3-week to 2-week increments per Efi's request

**Proposal Structure:**
- **Summary** - Problem statement and my approach
- **Personal Background** - Why this matters to me
- **Preparation Work** - What I've done (this repo!)
- **Project Understanding** - Gaps I identified
- **Proposed Work** - 12 weeks, 2-week increments
- **Timeline** - Detailed week-by-week breakdown
- **Why I'm Qualified** - Skills match + demonstrated preparation

**Timeline (2-Week Increments):**
- **Weeks 1-2:** Documentation foundation (15-20 Arrangement_2 insertion methods)
- **Weeks 3-4:** More docs (15-20 query/traversal methods)
- **Weeks 5-6:** Named parameters Phase 1 (15-20 Arrangement functions)
- **Weeks 7-8:** Named parameters Phase 2 (Triangulation + Vertex docs)
- **Weeks 9-10:** Handle classes (Halfedge, Face documentation)
- **Weeks 11-12:** Line 857 bug fix + final polish

**Time spent:** ~8 hours (writing + revising)

**Submitted:** December 24, 2025, 11:57 PM IST

---

## 🔥 Phase 2: First Contribution (Dec 26-27, 2025)

### From Theory to Practice: The 12-Hour Sprint

After submitting my proposal, I didn't wait around. I wanted to prove I could actually contribute, not just write about it.

---

### Night 1: Building cgalpy with Arrangements (Dec 25-26, 12 hours)

**The Challenge:**  
Build the Python bindings from source with arrangement support and run actual tests.

**What Happened:**

**Hour 1-3: Initial Build Attempts**
- Cloned `cgal-python-bindings`
- Tried building with GCC → failed (Qt6 macro issues on macOS)
- Switched to Apple Clang → success
- Key CMake flag: `-DCGALPY_ARRANGEMENT_ON_SURFACE_2_BINDINGS=ON`

**Hour 4-6: Finding the Bindings**
- Build succeeded but where are the modules?
- Discovered: `build/src/libs/cgalpy/CGALPY.cpython-312-darwin.so`
- Import path: `from CGALPY.Aos2 import Arrangement_2`
- Submodules: `Aos2` (arrangements), `Ker` (kernel types)

**Hour 7-12: Testing Everything**

Wrote `test_methods.py` and ran experiments on three methods:

---

#### Test 1: `insert_in_face_interior(point, face)`

```python
arr = Arrangement_2()
unbounded = arr.unbounded_face()

# Test basic insertion
v = arr.insert_in_face_interior(Point_2(5, 5), unbounded)
print(v.is_isolated())  # True
print(v.degree())       # 0

# DISCOVERY: No validation!
v1 = arr.insert_in_face_interior(Point_2(5, 5), unbounded)
v2 = arr.insert_in_face_interior(Point_2(5, 5), unbounded)  # SAME POINT
print(arr.number_of_vertices())  # 2 - both created!
```

**Surprise:** The method happily creates duplicate vertices at the same coordinates. No error, no warning. This creates invalid topology!

---

#### Test 2: `insert_from_left_vertex(curve, vertex)`

```python
v_left = arr.insert_in_face_interior(Point_2(0, 0), unbounded)
seg = Segment_2(Point_2(0, 0), Point_2(3, 3))
he = arr.insert_from_left_vertex(seg, v_left)

print(he.source().point())  # 0 0 (left - input vertex)
print(he.target().point())  # 3 3 (right - newly created)
print(v_left.degree())      # 1 (was 0, now has edge)
```

**Result:** Halfedge points left→right as expected. Intuitive naming!

---

#### Test 3: `insert_from_right_vertex(curve, vertex)` - The Confusing One

```python
v_right = arr.insert_in_face_interior(Point_2(10, 10), unbounded)
seg = Segment_2(Point_2(7, 7), Point_2(10, 10))
he = arr.insert_from_right_vertex(seg, v_right)

# WAIT, WHAT?
print(he.source().point())  # 10 10 (RIGHT vertex - the input!)
print(he.target().point())  # 7 7  (LEFT vertex - newly created!)

# The halfedge points RIGHT→LEFT, not left→right!
# Need to use he.twin() for left→right direction
```

**Big Discovery:** `insert_from_right_vertex` returns a halfedge that goes right→left, which is counter-intuitive from the name. The `source()` is the input right vertex, and `target()` is the newly created left vertex.

This is consistent API design (both methods return halfedges where source = input vertex), but it trips people up.

**Time Spent:** 12 hours straight (midnight to noon)

**Outcome:**
- ✅ cgalpy built and working
- ✅ Three methods thoroughly tested
- ✅ Two critical behaviors discovered that need documentation

---

### Day 6: Writing Research Docs (Dec 26, afternoon)

Based on the testing discoveries, I wrote three detailed research markdown files:

#### 1. `method1-insert_in_face_interior-POINT-research.md`
- **What it does:** Creates isolated vertex at point
- **DCEL changes:** +1 vertex (degree 0), no edges
- **CRITICAL:** No precondition validation—can create duplicates
- **When to use:** First step in incremental construction

#### 2. `method2-insert_from_left_vertex-VERTEX-research.md`
- **What it does:** Insert curve from existing left endpoint
- **Returns:** Halfedge pointing left→right
- **DCEL changes:** +1 vertex at right, +2 halfedges, +1 edge
- Intuitive naming matches behavior

#### 3. `method3-insert_from_right_vertex-VERTEX-research.md`
- **What it does:** Insert curve to existing right endpoint
- **Returns:** Halfedge pointing right→left (counter-intuitive!)
- Must use `he.twin()` for left→right
- Detailed comparison table with left variant

**Each research doc included:**
- Binding location (line numbers)
- Current state (no docs, no param names)
- Test results with actual Python code
- Preconditions and validation status
- DCEL topology changes
- Common mistakes to warn about

**Time Spent:** 4 hours

---

### Day 7: The Formatting Disaster (Dec 26, evening)

**The Problem:**

I wrote beautiful NumPy-style docstrings for all six methods and edited `arrangement_on_surface_2_bindings.cpp`. Hit Cmd+S to save.

VS Code's formatter rewrote the entire file.

**Result:** +1306 / -823 lines changed on Bitbucket, even though I only touched 6 methods.

**The Fix:**

1. Reset to clean master

```bash
git checkout master
git reset --hard
git pull origin master
```

2. Disable auto-format in VS Code
   - Set `"editor.formatOnSave": false` in settings.json
   - Disabled C/C++ extension's format-on-save
   - Disabled Clang-Format extension

3. Create fresh branch and re-apply changes

```bash
git checkout -b aos2-docstrings-new
# Edit ONLY the 6 insertion methods
# No formatter running this time
git diff  # Clean, focused diff
```

4. Rebuild and test

```bash
cmake --build . --target CGALPY -j8
python3
>>> from CGALPY.Aos2 import Arrangement_2
>>> help(Arrangement_2.insert_from_left_vertex)
# Docstrings appear correctly!
```

**Time Spent:** 3 hours (frustrating, but learned proper git hygiene)

---

### Day 7: PR Submission (Dec 27, 12:51 AM)

**What I Changed:**

Updated bindings for six methods in `src/libs/cgalpy/lib/arrangement_on_surface_2_bindings.cpp`:

1. `insert_from_left_vertex(curve, vertex)`
2. `insert_from_left_vertex(curve, halfedge)`
3. `insert_from_right_vertex(curve, vertex)`
4. `insert_from_right_vertex(curve, halfedge)`
5. `insert_in_face_interior(curve, face)`
6. `insert_in_face_interior(point, face)`

**For Each Method:**

**Named Parameters**
- Added `py::arg("curve")`, `py::arg("vertex")`, `py::arg("halfedge")`, `py::arg("point")`, `py::arg("face")`
- Python now shows `insert_from_left_vertex(curve, vertex)` instead of `(*args, **kwargs)`

**NumPy-Style Docstrings**
- One-line summary in plain language
- Explanation of DCEL changes (which vertices/halfedges/edges created)
- Preconditions with explicit "not validated" warnings
- Halfedge direction documentation (especially for right→left case)
- Runnable examples derived from my REPL tests
- Cross-references to related methods

**Key Behaviors Documented**
- `insert_in_face_interior(point, face)`: Explicitly warns that no validation happens—can create duplicate vertices
- `insert_from_right_vertex(curve, vertex)`: Multiple warnings about right→left orientation and need for `he.twin()`
- `insert_from_left_vertex(curve, vertex)`: Documents left→right orientation and incremental construction pattern

**PR Description:**

- **Title:** "Add docstrings for Arrangement_2 insertion methods"
- **Summary:**
  - Small, focused change to 6 core insertion methods
  - Makes them discoverable from Python without reading C++ source
  - Based on combination of C++ docs + actual REPL experiments
  - Captures confusing behaviors so future users don't rediscover them

**Testing:**
- Built on macOS Apple Silicon M2
- Ran all examples from docstrings in fresh Python session
- Verified `help()` output matches docstrings
- Confirmed examples run without errors

**Committed:** Dec 27, 2025, 12:45 AM IST  
**Pushed:** Dec 27, 2025, 12:48 AM IST  
**PR Opened:** Dec 27, 2025, 12:51 AM IST

---

### Email to Efi (Dec 27, 12:58 AM)

Sent update email with:
- Brief intro: first small documentation contribution
- Summary of what changed and why
- PR link
- Key behaviors highlighted (no validation, halfedge direction)
- Invitation for feedback on docstring style

**Status:** Awaiting reply

---

## 🎯 Key Findings from My Preparation

### Gap #1: Documentation (CRITICAL) - NOW ADDRESSING

- 90% of methods missing docstrings
- ✅ **Started fixing:** 6 core insertion methods now documented
- Example: `insert_from_left_vertex` now has parameter descriptions, examples, and DCEL explanation
- Users no longer forced to read C++ source for these methods

### Gap #2: Named Parameters (MAJOR) - PARTIAL FIX

- Efi mentioned: "only 2-3 instances implemented, hundreds needed"
- ✅ **Fixed for 6 methods:** Now show `(curve, vertex)` instead of `(*args, **kwargs)`
- **Remaining:** ~40-50 arrangement methods still need parameter names

### Gap #3: Resource Deallocation (TECHNICAL) - DOCUMENTED FOR LATER

- Line 857 TODO: `reference_internal` doesn't work for `insert_cv_with_history`
- Using dangerous bare `reference` as workaround
- Potential memory leaks in long-running applications
- 📋 **Planned for Weeks 11-12:** Investigation + fix

### Gap #4: Type Stubs

- Only one `.pyi` file exists (`Arr_segment_traits_2.pyi`)
- No IDE autocomplete for other traits
- Poor developer experience in VS Code, PyCharm
- 📋 **Future work:** Generate stubs from docstrings

---

## 💻 Technical Skills I'm Bringing

### C++ Template Programming
- CodeChef rating: 1611
- Understand traits classes, policy-based design, SFINAE
- Read and analyzed 4,000+ lines of CGAL template code
- Comfortable with template metaprogramming

### Python API Design
- Built production systems: Layers (sentiment analysis), CaseEvo (e-commerce)
- Designed APIs for 1,000+ daily users
- Experience with NumPy, SciPy—know what Pythonic APIs feel like

### Binding Libraries
- Deep dive into nanobind: return policies, keep_alive, kwargs
- Understand C++/Python interop challenges
- Found and analyzed real bugs in CGAL bindings
- ✅ **Proven:** Built cgalpy from source and submitted working PR

### Git & Open Source Workflow
- ✅ **Learned the hard way:** Auto-formatter disaster → clean git history
- Proper branching, focused commits, minimal diffs
- PR description written for reviewers, not just myself

---

## 📝 Next Steps

### Immediate (Dec 27-31):
- [x] Build cgalpy with arrangements
- [x] Test insertion methods
- [x] Submit first documentation PR
- [ ] Respond to Efi's feedback on PR
- [ ] Make any requested changes
- [ ] Document lessons learned from first review

### January 2026:
- [ ] Continue docstring work (next 6-10 methods)
- [ ] Submit PR #2 with similar scope
- [ ] Start named parameters audit for remaining methods
- [ ] Engage with CGAL community discussions

### February 2026 (Pre-GSoC):
- [ ] Have 3-4 quality PRs merged
- [ ] Begin line 857 investigation (if approved as direction)
- [ ] Update proposal based on learnings
- [ ] Prepare for GSoC applications opening

### Long-term (Post-GSoC Decision):
- Continue contributing regardless of selection
- Help other Python users through documentation
- Work toward maintaining Python bindings long-term

---

## 🔗 Important Links

### CGAL Resources:
- **Python Bindings Repo:** https://bitbucket.org/taucgl/cgal-python-bindings
- **CGAL Documentation:** https://doc.cgal.org/latest/
- **Nanobind Docs:** https://nanobind.readthedocs.io/

### My Links:
- **GitHub:** https://github.com/UtkarsHMer05
- **LinkedIn:** https://linkedin.com/in/utkarshkhajuria05
- **Email:** utkarshkhajuria55@gmail.com

### GSoC 2026:
- **CGAL Project Page:** [TBD - Not yet published]
- **My Proposal:** [Google Docs Link](https://docs.google.com/document/d/1XL1RYG9U-9OJlXU0i78VNDTHCz3OLBPHnfQPgQmCfz4/edit?usp=sharing)
- **First PR:** [Bitbucket PR #1](https://bitbucket.org/taucgl/cgal-python-bindings/pull-requests/)

---

## 🤔 Why I'm Doing This

I'm not here for a line on my resume. I genuinely want to make CGAL's Python bindings better.

Computational geometry is powerful. CGAL's algorithms are elegant. But the barrier to entry is too high for Python developers who just want to solve geometry problems.

I want to fix that. Whether GSoC accepts me or not, I plan to keep contributing. This is the kind of work that matters—making advanced algorithms accessible to more people.

**Update (Dec 27):** Already proven this commitment—submitted first PR within 3 days of proposal. Not waiting for GSoC decisions to contribute.

---

## 📊 Time Investment Breakdown

| Phase | Activity | Hours | Details |
|-------|----------|-------|---------|
| **Phase 1** | Environment Setup | ~8h | Building CGAL, dependencies, testing |
| | 2D Arrangements Study | ~12h | DCEL, traits, examples, analysis |
| | Python Bindings Analysis | ~10h | Code reading, gap identification |
| | Nanobind Learning | ~12h | Policies, lifetime management, line 857 |
| | Proposal Writing | ~8h | Research, writing, diagrams, revision |
| **Phase 2** | cgalpy Build & Testing | ~12h | Arrangements enabled, method testing, discoveries |
| | Research Documentation | ~4h | Three detailed method analyses |
| | Docstring Writing | ~6h | NumPy-style docs for 6 methods |
| | Git & PR Workflow | ~3h | Formatting fix, clean branch, submission |
| **Total** | | **~75h** | Documented work from Dec 20-27 |

---

## 🎓 What I've Learned So Far

### Technical:
- CGAL's template architecture is brilliant but complex
- Nanobind lifetime management is tricky but critical
- Python bindings require deep understanding of both languages
- Good documentation needs examples, not just API references
- ✅ **New:** Building from source reveals behavior docs don't mention
- ✅ **New:** Testing finds surprises (no validation, halfedge directions)

### Process:
- Read the actual code, don't just skim docs
- Verify claims before making them (learned this with line 857!)
- Quality over quantity matters in open source
- Mentors appreciate thorough preparation
- ✅ **New:** Auto-formatters can destroy PRs—disable them
- ✅ **New:** Small, focused PRs are easier to review than massive ones

### Personal:
- I love this kind of deep technical work
- Finding real bugs is incredibly satisfying
- I'm ready for the challenge of GSoC
- This is the kind of project I want to commit to long-term
- ✅ **New:** Going from "I want to contribute" to "I actually contributed" feels great

---

## 💪 Closing Thoughts

This README isn't AI-generated. It's my actual journey over 7 days in December 2025.

I started knowing nothing about CGAL. Now I can:
- Build it from source
- Understand its architecture
- Find bugs in its bindings
- Propose concrete improvements
- ✅ Write production-quality documentation
- ✅ Submit PRs that pass review (hopefully!)

That's what 75+ hours of genuine effort looks like.

Whether or not GSoC works out, I'm proud of this work. And I'm excited to keep going.

**Computational geometry deserves better Python support. Let's build it.**

---

**Last Updated:** December 27, 2025, 12:58 AM IST  
**Status:** First PR submitted, awaiting mentor review  
**Next Milestone:** Incorporate feedback, submit PR #2 (target: early January)

---

**Utkarsh Khajuria**  
Third-year CS student, VIT Chennai  
CGAL Python bindings contributor (not just hoping—doing it!)
