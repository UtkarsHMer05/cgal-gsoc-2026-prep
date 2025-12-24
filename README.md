# 🎯 CGAL GSoC 2026 Preparation Repository

**Project:** CGAL Python Bindings Enhancement  
**Applicant:** Utkarsh Khajuria  
**Mentor:** Efi Fogel  
**Preparation Period:** December 20-24, 2025

---

## 📌 Current Status

**✅ PROPOSAL SUBMITTED - December 24, 2025, 11:57 PM IST**

Submitted draft proposal to Efi Fogel via Google Docs for review. Waiting for feedback and ready to iterate based on mentor guidance.

**Proposal Link:** [Google Docs - Commenting Access](https://docs.google.com/document/d/1SHbLyhFKKJ1zjSKpw7itQlySHZafjXdm2hMlN3naKo4/edit?usp=sharing)

---

## 🚀 Why This Project?

I stumbled into CGAL when I needed 2D arrangement algorithms for a personal project. The C++ API was beautiful—elegant template metaprogramming, trait classes, policy-based design. But when I tried the Python bindings, I hit a wall.

No docstrings. Generic `arg0, arg1` parameter names. Comments like `//! \todo Why the f... reference_internal doesn't work?` on line 857.

That's when it clicked: **great architecture means nothing if users can't figure out how to use it.**

I'm not here just for a summer internship. I want to make CGAL's Python bindings actually usable for people who need computational geometry but don't want to read C++ source code.

---

## 📚 My Preparation Journey (50+ Hours)

### **Day 1: Environment Setup (December 20, 2025)**

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

### **Day 2: Mastering 2D Arrangements (December 21, 2025)**

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
Understanding the C++ architecture helps me write better Python documentation. I know WHY each method exists and WHEN to use it.

**Time spent:** ~12 hours

**Evidence:** Detailed analysis document covering template structure, type system, and use cases

---

### **Day 3: Exploring Python Bindings Repository (December 22, 2025)**

**What I did:**
- Cloned `cgal-python-bindings` from Bitbucket
- Analyzed binding code in `src/libs/cgalpy/lib/`
- Studied 50+ bound methods in `Arrangement_2`
- Found 70+ Python examples in `/examples/` directory

**What I discovered:**

**The Good:**
- 2D/3D Arrangements: ~80% complete
- 13+ geometry types supported
- Examples exist for most features
- Pythonic iteration works well

**The Gaps:**
- **90% of methods have NO docstrings**
- Most show `arg0, arg1, arg2` instead of parameter names
- No IDE autocomplete (missing `.pyi` type stubs)
- Some functions commented out (lifetime management issues)

**Specific Finding - Line 857:**  

    Found frustrated TODO comment in `arrangement_on_surface_2_bindings.cpp`:
    
    //! \todo Why the f... reference_internal doesn't work?
    m.def("insert", &aos2::insert_cv_with_history, ref);


Currently using bare `ref` policy as workaround—dangerous for memory management.

**Time spent:** ~10 hours (reading code, testing examples)

**Evidence:**

    Verified this myself:
    grep -n "todo" arrangement_on_surface_2_bindings.cpp
    
    Line 857: //! \todo Why the f... reference_internal doesn't work?


---

### **Day 4: Learning Nanobind (December 23-24, 2025)**

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

**📖 Detailed Nanobind Learning Notes:** See [NANOBIND_DEEP_DIVE.md](./NANOBIND_DEEP_DIVE.md)

---

### **Day 5: Writing the Proposal (December 24, 2025)**

**What I did:**
- Read successful GSoC proposals from past years
- Studied Tarun's winning proposals (Red Hen Lab, caMicroscope)
- Drafted comprehensive proposal with 2-week timeline
- Created architecture diagrams showing binding layers
- Verified all technical claims before submission
- Restructured timeline from 3-week to 2-week increments per Efi's request

**Proposal Structure:**
1. **Summary** - Problem statement and my approach
2. **Personal Background** - Why this matters to me
3. **Preparation Work** - What I've done (this repo!)
4. **Project Understanding** - Gaps I identified
5. **Proposed Work** - 12 weeks, 2-week increments
6. **Timeline** - Detailed week-by-week breakdown
7. **Why I'm Qualified** - Skills match + demonstrated preparation

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

## 🎯 Key Findings from My Preparation

### **Gap #1: Documentation (CRITICAL)**
- 90% of methods missing docstrings
- Example: `insert_from_left_vertex` has ZERO parameter descriptions
- Users forced to read C++ source code
- High barrier to entry for Python developers

### **Gap #2: Named Parameters (MAJOR)**
- Efi mentioned: "only 2-3 instances implemented, hundreds needed"
- Most functions show `arg0, arg1, arg2`
- Python users expect keyword arguments
- Hard to remember parameter order

### **Gap #3: Resource Deallocation (TECHNICAL)**
- Line 857 TODO: `reference_internal` doesn't work for `insert_cv_with_history`
- Using dangerous bare reference as workaround
- Potential memory leaks in long-running applications
- Needs investigation of ownership chains

### **Gap #4: Type Stubs**
- Only one `.pyi` file exists (`Arr_segment_traits_2.pyi`)
- No IDE autocomplete for other traits
- Poor developer experience in VS Code, PyCharm

---

## 💻 Technical Skills I'm Bringing

### **C++ Template Programming**
- CodeChef rating: 1611
- Understand traits classes, policy-based design, SFINAE
- Read and analyzed 4,000+ lines of CGAL template code
- Comfortable with template metaprogramming

### **Python API Design**
- Built production systems: Layers (sentiment analysis), CaseEvo (e-commerce)
- Designed APIs for 1,000+ daily users
- Experience with NumPy, SciPy—know what Pythonic APIs feel like

### **Binding Libraries**
- Deep dive into nanobind: return policies, `keep_alive`, kwargs
- Understand C++/Python interop challenges
- Found and analyzed real bugs in CGAL bindings

---

## 📝 Next Steps (Post-Submission)

### **Immediate (Dec 26-31):**
- [ ] Start first documentation PR (2-3 simple methods)
- [ ] Continue studying nanobind lifetime patterns
- [ ] Document line 857 investigation approach
- [ ] Keep this repo updated with learning

### **January 2026:**
- [ ] Monitor email for Efi's feedback
- [ ] Iterate on proposal based on comments
- [ ] Submit small PRs to demonstrate coding style
- [ ] Join CGAL mailing list and engage with community

### **Long-term (Post-GSoC Decision):**
- Continue contributing regardless of selection
- Help other Python users through documentation
- Work toward maintaining Python bindings long-term

---

## 🔗 Important Links

**CGAL Resources:**
- Python Bindings Repo: https://bitbucket.org/taucgl/cgal-python-bindings
- CGAL Documentation: https://doc.cgal.org/latest/
- Nanobind Docs: https://nanobind.readthedocs.io/

**My Links:**
- GitHub: https://github.com/UtkarsHMer05
- LinkedIn: https://linkedin.com/in/utkarshkhajuria05
- Email: utkarshkhajuria55@gmail.com

**GSoC 2026:**
- CGAL Project Page: [TBD - Not yet published]
- My Proposal: https://docs.google.com/document/d/1SHbLyhFKKJ1zjSKpw7itQlySHZafjXdm2hMlN3naKo4/edit?usp=sharing

---

## 🤔 Why I'm Doing This

I'm not here for a line on my resume. I genuinely want to make CGAL's Python bindings better.

Computational geometry is powerful. CGAL's algorithms are elegant. But the barrier to entry is too high for Python developers who just want to solve geometry problems.

I want to fix that. Whether GSoC accepts me or not, I plan to keep contributing. This is the kind of work that matters—making advanced algorithms accessible to more people.

---

## 📊 Time Investment Breakdown

| Activity | Hours | Details |
|----------|-------|---------|
| Environment Setup | ~8h | Building CGAL, dependencies, testing |
| 2D Arrangements Study | ~12h | DCEL, traits, examples, analysis |
| Python Bindings Analysis | ~10h | Code reading, gap identification, examples |
| Nanobind Learning | ~12h | Policies, lifetime management, line 857 |
| Proposal Writing | ~8h | Research, writing, diagrams, revision |
| **Total** | **~50h** | **Documented preparation work** |

---

## 🎓 What I've Learned So Far

**Technical:**
- CGAL's template architecture is brilliant but complex
- Nanobind lifetime management is tricky but critical
- Python bindings require deep understanding of both languages
- Good documentation needs examples, not just API references

**Process:**
- Read the actual code, don't just skim docs
- Verify claims before making them (learned this with line 857!)
- Quality over quantity matters in open source
- Mentors appreciate thorough preparation

**Personal:**
- I love this kind of deep technical work
- Finding real bugs is incredibly satisfying
- I'm ready for the challenge of GSoC
- This is the kind of project I want to commit to long-term

---

## 💪 Closing Thoughts

This README isn't AI-generated. It's my actual journey over 5 days in December 2025.

I started knowing nothing about CGAL. Now I can:
- Build it from source
- Understand its architecture
- Find bugs in its bindings
- Propose concrete improvements

That's what 50+ hours of genuine curiosity looks like.

Whether or not GSoC works out, I'm proud of this work. And I'm excited to keep going.

Computational geometry deserves better Python support. Let's build it.

---

**Last Updated:** December 25, 2025, 12:09 AM IST  
**Status:** Proposal submitted, awaiting mentor feedback  
**Next Milestone:** First documentation PR (target: Dec 28-30)

---

**Utkarsh Khajuria**  
Third-year CS student, VIT Chennai  
Future CGAL Python bindings contributor (hopefully!)
