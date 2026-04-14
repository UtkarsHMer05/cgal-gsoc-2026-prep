# Open Questions and Next Steps

## What is done

As of mid-April 2026, the state of the docstring work is:

- Five packages (Polygon_2, Alpha_shapes_2, Boolean_set_operations_2,
  Envelope_2, Visibility_2) have dedicated docstring headers.[file:21]
- All relevant binding `.cpp` files include those headers and pass the
  correct `*_DOC` constants to each `.def()` call.
- The Polygon_2 header now contains all 32 constants that the binding
  expects, including the 10 that were missing in my earlier snapshot.[file:21]
- The extractor script provides 73/73 coverage across those packages, with
  a small number of intentional manual overrides.
- Runtime checks confirm that the Python `__doc__` strings look reasonable
  and match what I expect from the C++ documentation.

## Open questions for my mentor

I am explicitly waiting for feedback from Efi on:

1. **Manual docstrings**  
   Is it acceptable to keep my manually written texts for functions that
   have no direct CGAL header comments yet, or should these be left blank
   until CGAL provides official wording?

2. **LaTeX/Doxygen markup**  
   Should I:
   - strip the markup,
   - normalise it into something more Python-friendly,
   - or keep the raw Doxygen-style strings for now?

3. **Next priority: more docstrings vs new packages**  
   Should I spend additional time extending the docstring system to other
   existing bindings (e.g. Minkowski_sum_2, Polygon_with_holes_2,
   Polygon_partitioning), or shift focus to the “Weeks 5–6” plan from my
   proposal (Triangulation_2 and Convex_hull_2 bindings)?[file:21]

## My plan while waiting

Until I get clear answers, my self-imposed constraints are:

- Do **not** change the extractor behaviour or markup handling further.
- Keep the five-packages docstring system stable and well-documented.
- Use new time mainly for **read-only reconnaissance**:
  - mapping the Triangulation_2 and Convex_hull_2 APIs,
  - listing which methods would be most valuable to expose in Python,
  - and preparing small tables that I can share once Efi confirms the
    direction.[file:21]

This way, I keep making progress on understanding the codebase and planning
the next concrete steps, without making large design decisions that my
mentor might want to adjust.