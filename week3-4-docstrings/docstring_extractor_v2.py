#!/usr/bin/env python3
"""
docstring_extractor_v2.py
=========================
Final proof-of-concept docstring extractor.
Result: 50/50 (100%) coverage on AOS2 binding function list.

Usage:
    python3 docstring_extractor_v2.py

Requires:
    - CGAL source at ~/cgal/
    - Binding file at ~/cgal-python-bindings/src/libs/cgalpy/lib/
"""

import re
import os
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

CGAL_DOC_DIR = Path.home() / "cgal" / "Arrangement_on_surface_2" / \
               "doc" / "Arrangement_on_surface_2" / "CGAL"

BINDING_FILE = Path.home() / "cgal-python-bindings" / "src" / "libs" / \
               "cgalpy" / "lib" / "arrangement_on_surface_2_bindings.cpp"

# Iterator name mismatch map: binding name → doc header name
ALIAS_MAP = {
    "vertices":          "vertex_handles",
    "halfedges":         "halfedge_handles",
    "edges":             "edge_handles",
    "faces":             "face_handles",
    "isolated_vertices": "isolated_vertices_begin",
}

# Known wrong-match cases — override with correct manual text
MANUAL_OVERRIDES = {
    "degree": (
        "Returns the degree (number of incident halfedges) of the vertex."
    ),
    "topology_traits": (
        "Returns the topology traits object associated with the arrangement."
    ),
    "assign": (
        "Assigns the content of another arrangement to this arrangement."
    ),
    "face": (
        "Returns a handle to the face incident to this halfedge "
        "(the face to its left)."
    ),
}

# ── Regex patterns ─────────────────────────────────────────────────────────────

# Pattern 1+2: class methods (skips \ingroup and \name openers)
RE_CLASS = re.compile(
    r'/\*!((?:(?!\bingroup\b|\bname\b).)*?)\*/\s*\n\s*\S[^\n]*?(\w+)\s*\(',
    re.DOTALL
)

# Single-line (catches methods under \name section headers)
RE_SINGLE = re.compile(
    r'/\*!\s+([^\n]+?)\s+\*/\s*\n\s*\S[^\n]*?(\w+)\s*\('
)

# ingroup free-function blocks
RE_INGROUP = re.compile(
    r'/\*!\s*\\ingroup\s+\w+\s*\n'
    r'\s*\*\s*\n'
    r'((?:\s*\*[^\n]*\n)*?)'
    r'\s*\*/',
    re.DOTALL
)


def clean(text: str) -> str:
    """Strip comment markers, directives, and extra whitespace."""
    lines = [re.sub(r'^\s*\*\s?', '', l) for l in text.strip().splitlines()]
    lines = [l for l in lines
             if not re.match(r'\\(pre|cgal|param|return|tparam)', l.strip())]
    result = ' '.join(' '.join(lines).split())
    result = re.sub(r'\\f\$[^\\]+\\f\$', '<math>', result)  # strip LaTeX
    result = re.sub(r'`([^`]+)`', r'\1', result)            # strip backticks
    return result


def load_docs(doc_dir: Path) -> dict:
    docs = {}
    for h in sorted(doc_dir.rglob("*.h")):
        text = h.read_text(errors="replace")

        for m in RE_CLASS.finditer(text):
            name = m.group(2)
            if name not in docs:
                docs[name] = clean(m.group(1))

        for m in RE_SINGLE.finditer(text):
            name = m.group(2)
            if name not in docs:
                docs[name] = clean(m.group(1))

        for m in RE_INGROUP.finditer(text):
            desc = clean(m.group(1))
            if not desc:
                continue
            tail = text[m.end():m.end() + 600]
            fn = None
            for line in tail.splitlines()[:8]:
                line = line.strip()
                if not line:
                    continue
                if re.match(r'(template|typename|class|//|#|using|\w+_handle\b)', line):
                    continue
                hit = re.search(r'(\w+)\s*\(', line)
                if hit:
                    fn = hit.group(1)
                    break
            if fn and fn not in docs:
                docs[fn] = desc

    return docs


def load_binding_names(binding_file: Path) -> list:
    text = binding_file.read_text(errors="replace")
    raw = re.findall(r'\.def\(\s*"([^"]+)"', text)
    seen, out = set(), []
    for n in raw:
        if n not in seen and not n.startswith("__"):
            seen.add(n); out.append(n)
    return out


def run():
    print(f"Loading docs from:\n  {CGAL_DOC_DIR}\n")
    docs = load_docs(CGAL_DOC_DIR)
    print(f"  {len(docs)} docstrings extracted\n")

    print(f"Loading bindings from:\n  {BINDING_FILE}\n")
    names = load_binding_names(BINDING_FILE)
    print(f"  {len(names)} unique binding names\n")

    matched, unmatched = [], []
    for name in names:
        lookup = ALIAS_MAP.get(name, name)
        if name in MANUAL_OVERRIDES:
            matched.append((name, f"[MANUAL] {MANUAL_OVERRIDES[name]}"))
        elif lookup in docs:
            matched.append((name, docs[lookup]))
        else:
            unmatched.append(name)

    print("=" * 60)
    print(f"RESULTS: {len(matched)}/{len(names)}  "
          f"({100*len(matched)//len(names)}%)")
    print("=" * 60)

    if unmatched:
        print(f"\nUNMATCHED ({len(unmatched)}):")
        for n in unmatched:
            print(f"  - {n}")

    print("\nMATCHED SAMPLE (first 10):")
    for name, doc in matched[:10]:
        print(f"  {name:35s}  {doc[:75]}")

    return docs, matched, unmatched


if __name__ == "__main__":
    run()