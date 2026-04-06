# March 25, 2026 — Docstring Automation Research

> Trigger: Email 20 from Efi — "automate docstring creation"
> Duration: ~3 hours | Final result: **50/50 (100%)** on AOS2

## Key findings

### Where CGAL docs actually live

| Location | Comments? |
|---|---|
| `/opt/homebrew/include/CGAL/` | ❌ ZERO — stripped headers |
| `~/cgal/Arrangement_on_surface_2/doc/Arrangement_on_surface_2/CGAL/` | ✅ Full `/*!` comments |

### Three comment patterns found

**Pattern 1 — Single-line class method:**
```cpp
/*! obtains the number of vertices in the arrangement. */
Size number_of_vertices() const;
```

**Pattern 2 — Multi-line class method:**
```cpp
/*! inserts the curve `c` into the arrangement,
 * without intersecting existing curves.
 * \pre `c` is interior-disjoint from existing curves.
 */
Halfedge_handle insert_non_intersecting_curve(...);
```

**Pattern 3 — Free function (`\ingroup` style):**
```cpp
/*! \ingroup PkgArrangementOnSurface2Funcs
 *
 * Inserts a given point into the arrangement.
 */
Vertex_handle insert_point(...);
```

### Iterator alias map (5 entries needed)

| Binding name | Doc header name |
|---|---|
| `vertices` | `vertex_handles` |
| `halfedges` | `halfedge_handles` |
| `edges` | `edge_handles` |
| `faces` | `face_handles` |
| `isolated_vertices` | `isolated_vertices_begin` |

### Manual overrides (4 known wrong matches)

| Binding name | Problem | Fix |
|---|---|---|
| `degree` | Matched polynomial degree (wrong file) | Manual: "number of incident edges" |
| `topology_traits` | No doc entry exists | Manual: "topology traits object" |
| `assign` | Matched constructor doc | Manual: "assigns content of another arrangement" |
| `face` | Matched isolated vertex face | Manual: "face incident to this halfedge" |

## Script evolution

| Attempt | Score | What happened |
|---|---|---|
| 1 — plain string replace | FAILED | Python `\n` ≠ real newlines |
| 2 — `re.subn()` with `\s+` | 35/50 | `\ingroup` blocks filtered out entirely |
| 3 — added alias map | 42/50 | Single-line pattern still missed |
| 4 — negative lookahead | 6/50 | Too aggressive, broke everything |
| 5 — reverted + ingroup_block | 41/50 | Forward scan only 4 lines (too shallow) |
| **6 — 8-line forward scan** | **50/50 ✅** | Final version |

## Final script logic (see `docstring_extractor_v2.py`)

1. Load all `.h` files from `~/cgal/Arrangement_on_surface_2/doc/` recursively
2. **Pattern 1+2:** regex captures `/*! ... */` then the next function name; skips `\ingroup`/`\name` openers
3. **Single-line:** separate pattern catches methods under `\name` section headers
4. **ingroup_block:** scan forward 8 lines past `*/`, skip `template`/`typename`/return-type lines, take first `word(` match as function name
5. Apply alias map → apply manual overrides

**Result: 50/50 (100%) on all AOS2 binding function names**

## Known production issues (documented, not blockers)

1. LaTeX: `\f$x\f$`-monotone → needs stripping before use as Python docstring
2. Backtick markup: `` `c` `` → needs stripping
3. 4 functions need manual overrides (will always need manual overrides)
4. Script covers AOS2 only — other packages not yet measured
5. Overloaded functions get same docstring (first match) — needs parameter-type disambiguation

## Email thread

- Email 20 received Mar 25 — Efi: "automate docstring creation"
- Email 21 sent Mar 25 — confirmed direction, asked about target file
- Email 22 sent Mar 25 — 50/50 results + "should I clean up and run on all files?"
- **Email 23 — AWAITING Efi reply**
