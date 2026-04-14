# Docstring Extraction and Coverage

## From manual typing to automation

For AOS2 I originally wrote many docstrings manually. Later I realised that
CGAL already maintains high-quality documentation in its own header files,
and it would be better if my Python docstrings stayed as close as possible
to those.

This led to a small extraction script (`docstring_extractor.py` /
`docstring_extractor_v2.py`) that walks the CGAL headers and pulls out the
comments that sit immediately above the function declarations.[file:21]

## Patterns in the CGAL headers

CGAL uses a Doxygen style based on `/*! ... */` comments. During the AOS2
work I discovered three main patterns:

1. Single-line comments.
2. Multi-line comments.
3. `\\ingroup` blocks for free functions.[file:21]

I also learned that the Homebrew-installed headers under
`/opt/homebrew/include/CGAL/` contain **no comments at all**, so the
extractor must work on a local CGAL clone under `~/cgal/`.[file:21]

## Extending beyond AOS2

The first proof-of-concept was for AOS2: I achieved 50/50 coverage for the
set of functions I cared about, with a mixture of pure extraction,
an alias table for iterator names, and a few manual overrides.[file:21]

In this phase I generalised the same idea to the five packages that now
have dedicated docstring headers:

- Polygon_2
- Alpha_shapes_2
- Boolean_set_operations_2
- Envelope_2
- Visibility_2[file:21]

For each package I:

- Enumerated the bound methods.
- Mapped them to either a directly extractable header comment or a manual
  description.
- Measured coverage as “number of methods that have a reasonable docstring”
  / “total number of bound methods.”

The result is:

- Polygon_2: 31/31
- Alpha_shapes_2: 16/16
- Boolean_set_operations_2: 8/8
- Envelope_2: 13/13
- Visibility_2: 5/5

Total: **73/73** methods covered.[file:21]

## Manual overrides

Not every method has a ready-made comment in the CGAL headers. In those
cases I wrote short, neutral descriptions myself. Examples include:

- `draw` for Polygon_2 (viewer integration).
- Some Envelope_2 helpers that are thin wrappers around more general
  functions.
- A few constructors where the header comment isn’t directly usable.[file:21]

In total there are about eight of these “manual” docstrings. In my email
to Efi I asked explicitly whether it is acceptable to keep them as-is or
whether he prefers that I leave them blank until CGAL itself provides
official comments.

## LaTeX/Doxygen markup

Some of the extracted comments include LaTeX/Doxygen fragments such as
`\f$...\f$` and `\cgalBigO{}`. I have not yet changed these; they appear
in Python exactly as they appear in the C++ comments.[file:21]

In the same email I outlined the options:

- Strip markup completely and show plain text.
- Normalise it into simpler notation that still communicates the idea.
- Leave it as-is and possibly handle it later with a post-processor.

I am currently waiting for guidance before touching this.