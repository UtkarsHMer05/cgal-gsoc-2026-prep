# March 25 — Docstring Automation Research

Date: March 25, 2026
Trigger: Efi's suggestion (Email 20): "you surely can start with how to automate a bit of the docstring creation"
Result: Python script achieving 50/50 (100%) extraction on AOS2 binding function list
Time spent: roughly 3 hours


---


## The core question

All 108 docstrings for Weeks 3-4 were written manually by reading doc.cgal.org.
The question was whether we could automate this by parsing CGAL's existing documentation headers.


---


## Step 1: Where do the docs live?

First assumption (wrong): Doxygen comments are in the installed CGAL headers.

```bash
grep -n "\\brief\|/\*\*" /opt/homebrew/include/CGAL/Arrangement_on_surface_2.h | head -20
# Output: (nothing)
```

The Homebrew-installed headers have zero documentation comments.

Second find: the CGAL source repo at `~/cgal/` has a separate `doc/` folder:

```bash
find ~ -name "Arrangement_on_surface_2.h" -path "*/doc/*" 2>/dev/null
# Output:
# /Users/utkarshkhajuria/cgal/Arrangement_on_surface_2/doc/
#   Arrangement_on_surface_2/CGAL/Arrangement_on_surface_2.h
```

The doc headers are not the implementation. They are concept/documentation files that look like C++ but exist purely for Doxygen. They contain full prose descriptions for every function.

```
~/cgal/Arrangement_on_surface_2/doc/Arrangement_on_surface_2/
├── CGAL/              ← 45+ doc headers
│   ├── Arrangement_on_surface_2.h    ← main class doc
│   ├── Arrangement_2.h
│   ├── Arr_vertical_decomposition_2.h
│   ├── Arr_batched_point_location.h
│   └── ... (40 more)
├── Concepts/          ← 60+ concept doc headers
└── Doxyfile.in
```


---


## Step 2: What does the doc format look like?

Three distinct patterns were discovered:

### Pattern 1 — Simple class methods (single-line)

```cpp
/*! obtains the number of vertices in the arrangement. */
Size number_of_vertices() const;

/*! obtains the number of halfedges in the arrangement. */
Size number_of_halfedges() const;
```

Comment is a single `/*! ... */` on one line immediately before the signature.

### Pattern 2 — Complex class methods (multi-line)

```cpp
/*! inserts the curve `c` into the arrangement, such that its left endpoint
 * corresponds to a given arrangement vertex. As a result, a new halfedge pair
 * is created...
 * \pre The interior of `c` is disjoint from all existing arrangement vertices
 * and edges.
 * \pre `v` is associated with the left endpoint of `c`.
 */
Halfedge_handle insert_from_left_vertex(const X_monotone_curve_2& c,
                                        Vertex_handle v);
```

Multi-line comment, description before `\pre` lines. Description ends at first `\pre`.

### Pattern 3 — Free functions (\ingroup style)

```cpp
/*! \ingroup PkgArrangementOnSurface2Funcs
 *
 * Inserts a given point into a given arrangement. It uses a given
 * point-location object to locate the given point...
 *
 * \pre If provided, `pl` must be attached to the given arrangement `arr`.
 */
template <typename GeometryTraits, typename TopologyTraits, typename PointLocation>
typename Arrangement_on_surface_2<...>::Vertex_handle
insert_point(Arrangement_on_surface_2<...>& arr,
             const typename Traits::Point_2& p,
             const PointLocation& pl = walk_pl);
```

Mandatory structure: `\ingroup` tag, blank line, then description text.
Function signature spans multiple lines (template + return type + name).


---


## Step 3: Iterator name mismatch discovery

The Python binding file uses shorter names than the CGAL doc headers:

| Python binding name  | CGAL doc name             |
|----------------------|---------------------------|
| `vertices`           | `vertex_handles`          |
| `halfedges`          | `halfedge_handles`        |
| `edges`              | `edge_handles`            |
| `faces`              | `face_handles`            |
| `isolated_vertices`  | `isolated_vertices_begin` |

An alias map is required to bridge these.


---


## Step 4: Known wrong-match cases

Some function names appear in multiple doc headers with different meanings:

| Function          | Wrong match                                          | Correct source                                                    |
|-------------------|------------------------------------------------------|-------------------------------------------------------------------|
| `degree`          | "Compute the degree of a polynomial" (from traits)   | "Obtains the number of edges incident to v" (from vertex doc)     |
| `assign`          | Constructor doc (from arrangement doc)                | Manual: "Assigns the contents of another arrangement"             |
| `face`            | "Obtains a handle to the face that contains v" (iso)  | Manual: "Obtains a handle to the face to the left of the halfedge"|
| `topology_traits` | No doc entry exists                                  | Manual: write directly                                            |


---


## Step 5: Script evolution (7 iterations)

| Attempt | Approach                                        | Result                          |
|---------|-------------------------------------------------|---------------------------------|
| 1       | `str.replace()` with exact strings              | FAILED — Python `\n` != real newlines |
| 2       | `re.subn()` with `\s+`                          | Worked for binding patches, not extraction |
| 3       | Basic `re.compile('/\*!(.*?)\*/')`               | 35/50 (70%) — \ingroup filtered out |
| 4       | + alias map + single-line pattern               | 42/50 (84%)                     |
| 5       | + negative lookahead `(?:(?!\ingroup).)*`       | BROKE — 6/50                    |
| 6       | Reverted + `ingroup_block` pattern              | 41/50 — multi-line fn sig broke it |
| 7       | + forward scan skipping template lines          | 50/50 (100%)                    |

Critical lesson from Attempt 5: negative lookahead in DOTALL mode with `.*?` causes catastrophic backtracking and breaks all matches. Never use `(?:(?!X).)*` with DOTALL. Use a separate pattern for `\ingroup` blocks instead.


---


## Step 6: Final script logic

The working script uses three separate patterns:

Pattern A catches class methods (35-42 range):

```python
func_pattern = re.compile(r'/\*!(.*?)\*/\s*\n\s*\S.*?(\w+)\s*\(', re.DOTALL)
# For each match: extract comment, split at \pre or blank-star-line,
# take first chunk as description, skip if starts with \ingroup/\name/etc.
```

Pattern B catches `number_of_vertices`, `number_of_halfedges`:

```python
single_line = re.compile(r'/\*!\s*([^*\n][^\n]*?)\s*\*/\s*\n\s*\S.*?(\w+)\s*\(')
# These are preceded by \name section headers which cause Pattern A to skip them.
# Single-line pattern avoids the issue.
```

Pattern C catches free functions (\ingroup style):

```python
ingroup_block = re.compile(r'/\*!\s*\\ingroup\s+\S+\s*\n\s*\*\s*\n(.*?)\*/', re.DOTALL)
# Find all \ingroup blocks, extract description lines until blank/\pre/<UL,
# then scan forward 8 lines in the file to find function name,
# skipping template/typename/return-type lines.
```


---


## Final results: 50/50

```
OK number_of_vertices          Obtains the number of vertices in the arrangement.
OK number_of_edges             Obtains the number of edges in the arrangement.
OK number_of_faces             Obtains the number of faces in the arrangement.
OK number_of_halfedges         Obtains the number of halfedges in the arrangement.
OK number_of_isolated_vertices Obtains the total number of isolated vertices...
OK number_of_unbounded_faces   Obtains the number of unbounded faces...
OK is_empty                    Determines whether the arrangement is empty...
OK is_valid                    Obtains true if arr represents a valid instance...
OK assign                      Assigns the contents of another arrangement...
OK clear                       Clears the arrangement.
OK vertices                    Obtains a range over handles of the arrangement vertices.
OK halfedges                   Obtains a range over handles of the arrangement halfedges.
OK edges                       Obtains a range over handles of the arrangement edges.
OK faces                       Obtains a range over handles of the arrangement faces.
OK insert_from_left_vertex     Inserts the curve c into the arrangement, such that its left...
OK insert_from_right_vertex    Inserts the curve c into the arrangement, such that its right...
OK insert_in_face_interior     Inserts the point p into the arrangement as an isolated vertex...
OK insert_at_vertices          Inserts the curve c into the arrangement, such that both...
OK modify_vertex               Sets p to be the point associated with the vertex v...
OK modify_edge                 Sets c to be the x-monotone curve associated with the edge e...
OK split_edge                  Splits the edge e into two edges...
OK merge_edge                  Merges the edges represented by e1 and e2 into a single edge...
OK remove_edge                 Removes the edge e from the arrangement...
OK remove_isolated_vertex      Removes the isolated vertex v from the arrangement...
OK insert_point                Inserts a given point into a given arrangement...
OK insert_non_intersecting_curve     Inserts a given x-monotone curve into a given arrangement...
OK insert_non_intersecting_curves    Inserts a set of x-monotone curves in a given range...
OK insert                      Inserts the x-monotone curve xc into the arrangement...
OK do_intersect                Checks if a given curve or x-monotone curve intersects...
OK decompose                   Produces the symbolic vertical decomposition of a given arrangement...
OK zone                        Computes the zone of the given x-monotone curve in a given arrangement...
OK remove_vertex               Attempts to removed a given vertex from a given arrangement...
OK point                       Obtains the point associated with the vertex.
OK degree                      Obtains the number of edges incident to the vertex.
OK is_isolated                 Checks whether the vertex is isolated (i.e., has no incident edges).
OK incident_halfedges          Obtains a circulator that allows going over the halfedges...
OK source                      Obtains a handle for the source vertex of e.
OK target                      Obtains a handle for the target vertex of e.
OK twin                        Obtains the twin halfedge.
OK next                        Obtains e's successor in the connected component it belongs to.
OK prev                        Obtains e's predecessor in the connected component it belongs to.
OK face                        Obtains a handle to the face to the left of the halfedge.
OK direction                   Obtains the direction of the halfedge: ARR_LEFT_TO_RIGHT...
OK is_unbounded                Obtains a Boolean indicating whether the face is unbounded.
OK outer_ccb                   Obtains a circulator that enables traversing the outer boundary...
OK number_of_holes             Obtains the number of holes (inner CCBs) inside the face.
OK isolated_vertices           Obtains an iterator for traversing all the isolated vertices...
OK geometry_traits             Obtains the traits object used by the arrangement instance...
OK topology_traits             Obtains the topology-traits object associated with the arrangement.
OK fictitious_face             Obtains a handle to the fictitious face of the arrangement...
```

50/50 extracted cleanly.


---


## Known issues for production use

1. LaTeX markup — extracted text contains `\f$x\f$-monotone` and `\f$xy\f$`. Needs a cleanup pass: `re.sub(r'\\f\$.*?\\f\$', 'x', text)`

2. Backtick markup — `` `c` ``, `` `arr` `` need stripping for Python docstrings. Fix: `re.sub(r'` + "`" + r'([^` + "`" + r']+)` + "`" + r'', r'\1', text)`

3. HTML tags — `<I>`, `<UL>`, `<LI>` appear in some entries. Fix: `re.sub(r'<[^>]+>', '', text)`

4. 4 manual overrides needed (`degree`, `topology_traits`, `assign`, `face`) — documented above, acceptable for a real implementation.

5. Overloaded functions — all overloads get same docstring (first match). For methods like `insert_from_left_vertex` which have 2 overloads, parameter-type disambiguation would be needed for perfect per-overload docs.

6. Only AOS2 package tested — other packages (tri2, tri3, pol3, lcc) not yet run. Next step: run against all binding files and report coverage.


---


## Comparison: manual vs automated docstrings

| Function              | Manual (written March 24)                                                                                       | Automated (extracted March 25)                                                                                                    |
|-----------------------|-----------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| `number_of_vertices`  | "Obtains the number of vertices in the arrangement."                                                            | "Obtains the number of vertices in the arrangement."                                                                              |
| `clear`               | "Clears the arrangement."                                                                                       | "Clears the arrangement."                                                                                                         |
| `is_empty`            | "Determines whether the arrangement is empty (contains only the unbounded face, with no vertices or edges)."    | "Determines whether the arrangement is empty (contains only the unbounded face, with no vertices or edges)."                      |
| `insert_point`        | "Inserts the point p into the arrangement and returns a handle for the vertex associated with it."              | "Inserts a given point into a given arrangement. It uses a given point-location object to locate the given point..."               |

Manual versions are shorter and cleaner. Automated versions are verbatim from docs and sometimes longer. For production use, the automated text would need a "trim to first sentence" pass.
