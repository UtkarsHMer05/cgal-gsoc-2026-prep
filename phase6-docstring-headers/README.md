# Phase 6 — Docstring Headers and Automation

This folder documents the work I did **after** the inline AOS2 docstrings
(Weeks 3–4) to move CGALPY documentation into separate C++ header files and
to partially automate docstring extraction from CGAL’s own headers.

It explains, in human language:

- Why I introduced dedicated `docstrings/*.h` headers for five packages
  (Polygon_2, Alpha_shapes_2, Boolean_set_operations_2, Envelope_2,
  Visibility_2).
- How I wired those headers into the existing nanobind bindings.
- How the extraction script works, what coverage it achieves, and where I
  still use manual text.
- What is currently blocked on mentor feedback and what I plan to do next
  (Triangulation_2 / Convex_hull_2, AOS2 migration).