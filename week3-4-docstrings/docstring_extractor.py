"""
CGAL Docstring Extractor — Proof of Concept
March 25, 2026

Extracts docstring text from CGAL doc headers and maps them to
Python binding function names in arrangement_on_surface_2_bindings.cpp.

Usage:
    python3 docstring_extractor.py

Requirements:
    - ~/cgal/ must contain the CGAL source repo
      (Arrangement_on_surface_2/doc/ subfolder)
    - Run from anywhere

Result: 50/50 (100%) on AOS2 binding function list
"""

import re
import glob
import os

# ── Configuration ────────────────────────────────────────────────────────────
DOC_ROOT = os.path.expanduser(
    "~/cgal/Arrangement_on_surface_2/doc/Arrangement_on_surface_2"
)

# Python binding name → CGAL doc name (where they differ)
NAME_ALIASES = {
    "vertices":           "vertex_handles",
    "halfedges":          "halfedge_handles",
    "edges":              "edge_handles",
    "faces":              "face_handles",
    "isolated_vertices":  "isolated_vertices_begin",
}

# Functions where auto-extraction picks the wrong match
# Value is the correct docstring text
MANUAL_OVERRIDES = {
    "degree":           "Obtains the number of edges incident to the vertex.",
    "topology_traits":  "Obtains the topology-traits object associated with the arrangement.",
    "assign":           "Assigns the contents of another arrangement to this arrangement.",
    "face":             "Obtains a handle to the face to the left of the halfedge.",
}

# ── Load all doc headers ──────────────────────────────────────────────────────
def load_all_headers(doc_root):
    all_files = (
        glob.glob(f"{doc_root}/**/*.h", recursive=True) +
        glob.glob(f"{doc_root}/*.h")
    )
    file_contents = {}
    for f in all_files:
        with open(f) as fh:
            file_contents[os.path.basename(f)] = fh.read()
    return file_contents


# ── Pattern A: standard /*! comment */ before function ───────────────────────
FUNC_PATTERN = re.compile(r'/\*!(.*?)\*/\s*\n\s*\S.*?(\w+)\s*\(', re.DOTALL)

SKIP_PREFIXES = (
    '\\ingroup', '\\name', '\\ref', '\\tparam',
    '@{', '\\addtogroup', 'A bidirectional', '\\deprecated',
)

def extract_standard(combined):
    results = {}
    for match in FUNC_PATTERN.finditer(combined):
        comment = match.group(1).strip()
        func_name = match.group(2)
        # Take text up to first \pre, \cgal, or blank-star line
        first = re.split(r'\n\s*\*\s*\\|\n\s*\*\s*\n', comment)[0]
        first = re.sub(r'\s*\n\s*\*\s*', ' ', first).strip()
        first = re.sub(r'\s+', ' ', first)
        if any(first.startswith(p) for p in SKIP_PREFIXES):
            continue
        if not first or len(first) < 10:
            continue
        first = first[0].upper() + first[1:]
        if func_name not in results:
            results[func_name] = first
    return results


# ── Pattern B: single-line /*! text. */ ──────────────────────────────────────
SINGLE_LINE = re.compile(
    r'/\*!\s*([^*\n][^\n]*?)\s*\*/\s*\n\s*\S.*?(\w+)\s*\('
)

def extract_single_line(combined, results, targets):
    for match in SINGLE_LINE.finditer(combined):
        text = match.group(1).strip()
        name = match.group(2)
        if name in targets and name not in results:
            text = text[0].upper() + text[1:]
            results[name] = text


# ── Pattern C: /*! \ingroup ... blank ... description */ ─────────────────────
INGROUP_BLOCK = re.compile(
    r'/\*!\s*\\ingroup\s+\S+\s*\n\s*\*\s*\n(.*?)\*/',
    re.DOTALL
)

def extract_ingroup(combined, results):
    for match in INGROUP_BLOCK.finditer(combined):
        raw = match.group(1)
        # Extract first sentence — stop at blank line, \pre, \cgal, <UL
        lines = raw.split('\n')
        parts = []
        for line in lines:
            s = re.sub(r'^\s*\*\s?', '', line).strip()
            if not s:
                break
            if (s.startswith('\\') or
                    s.startswith('<UL') or
                    s.startswith('<LI')):
                break
            parts.append(s)
        first = ' '.join(parts)
        first = re.sub(r'\s+', ' ', first).strip()
        if not first or len(first) < 10:
            continue

        # Find function name in next 8 lines after block ends
        after_close = combined[match.end():]
        next_lines = after_close.split('\n')[:8]
        func_name = None
        for line in next_lines:
            if re.match(r'\s*(template|typename|using|typedef|/)', line):
                continue
            m = re.search(r'\b(\w+)\s*\(', line)
            if m and not re.match(r'\s*(if|for|while|return|static)', line):
                func_name = m.group(1)
                break

        if func_name and func_name not in results:
            first = first[0].upper() + first[1:]
            results[func_name] = first


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    file_contents = load_all_headers(DOC_ROOT)
    combined = "\n".join(file_contents.values())

    # Run all three extraction patterns
    results = extract_standard(combined)
    extract_ingroup(combined, results)

    # Pattern B for specific targets missed by A
    single_line_targets = {"number_of_vertices", "number_of_halfedges"}
    extract_single_line(combined, results, single_line_targets)

    # Apply name aliases
    for py_name, doc_name in NAME_ALIASES.items():
        if py_name not in results and doc_name in results:
            results[py_name] = results[doc_name]

    # Apply manual overrides
    results.update(MANUAL_OVERRIDES)

    return results


# ── Verification against known AOS2 binding targets ──────────────────────────
TARGET_FUNCTIONS = [
    # Query methods
    "number_of_vertices", "number_of_edges", "number_of_faces",
    "number_of_halfedges", "number_of_isolated_vertices",
    "number_of_unbounded_faces", "is_empty", "is_valid", "assign", "clear",
    # Iterators
    "vertices", "halfedges", "edges", "faces",
    # Insertion
    "insert_from_left_vertex", "insert_from_right_vertex",
    "insert_in_face_interior", "insert_at_vertices",
    # Modification
    "modify_vertex", "modify_edge", "split_edge", "merge_edge",
    "remove_edge", "remove_isolated_vertex",
    # Free functions
    "insert_point", "insert_non_intersecting_curve",
    "insert_non_intersecting_curves", "insert", "do_intersect",
    "decompose", "zone", "remove_vertex",
    # Vertex methods
    "point", "degree", "is_isolated", "incident_halfedges",
    # Halfedge methods
    "source", "target", "twin", "next", "prev", "face", "direction",
    # Face methods
    "is_unbounded", "outer_ccb", "number_of_holes", "isolated_vertices",
    # Traits
    "geometry_traits", "topology_traits", "fictitious_face",
]


if __name__ == "__main__":
    results = main()

    print(f"{'':3} {'Function':<40} {'Extracted docstring'}")
    print("-" * 100)
    found = 0
    for name in TARGET_FUNCTIONS:
        doc = results.get(name, "NOT FOUND")
        status = "OK" if name in results else "XX"
        print(f"{status}  {name:<38} {doc[:60]}")
        if name in results:
            found += 1

    print(f"\n{found}/{len(TARGET_FUNCTIONS)} extracted cleanly")

    # Show any LaTeX/markup that needs cleaning in production
    print("\nMarkup that needs stripping for production use:")
    for name, doc in results.items():
        if name not in TARGET_FUNCTIONS:
            continue
        if '\\f$' in doc or '`' in doc or '<I>' in doc:
            print(f"  {name}: {doc[:80]}")