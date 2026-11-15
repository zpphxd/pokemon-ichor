#!/usr/bin/env python3
"""Resolve append-versus-append merge conflicts in the tileset tables.

When two branches each append a tileset to src/data/tilesets/{graphics,headers,
metatiles}.h, git sees one conflict whose two sides share a closing suffix
(the lines after the conflict, e.g. "    .callback = NULL,\n};"). Keep both:
ours, then the shared suffix, a blank line, then theirs.

  python3 tools/ichor/merge/union_tables.py FILE...
"""
import re
import sys

CONFLICT = re.compile(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n", re.S)


def suffix_after(text, end):
    """The lines after a conflict up to and including the next '};' line."""
    rest = text[end:]
    m = re.match(r"((?:(?!\};\n).*\n)*?\};\n)", rest)
    return m.group(1) if m else ""


def resolve(text):
    out, pos = [], 0
    for m in CONFLICT.finditer(text):
        ours, theirs = m.group(1), m.group(2)
        out.append(text[pos:m.start()])
        # only borrow the shared closing lines when ours leaves a struct open
        suffix = "" if ours.rstrip().endswith("};") else suffix_after(text, m.end())
        if suffix:
            out.append(ours + suffix + "\n" + theirs)
        else:                               # plain lines (metatiles.h): just both
            out.append(ours + ("\n" if ours and not ours.endswith("\n\n") else "") + theirs)
        pos = m.end()
    out.append(text[pos:])
    return "".join(out)


for path in sys.argv[1:]:
    with open(path) as f:
        text = f.read()
    new = resolve(text)
    if "<<<<<<<" in new:
        raise SystemExit(f"{path}: unresolved conflict left")
    with open(path, "w") as f:
        f.write(new)
    print(f"resolved {path}")
