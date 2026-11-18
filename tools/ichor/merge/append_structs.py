#!/usr/bin/env python3
"""Rebuild a C file of top-level definitions from one ref and append the named
definitions taken from another ref (for registries two branches both appended to).

    python3 tools/ichor/merge/append_structs.py FILE BASE_REF OURS_REF NAME [NAME ...]

Each NAME is a symbol; its whole definition (from the line that defines it to
the closing "};") is copied from OURS_REF onto the end of BASE_REF's file.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
path, base, ours, names = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]


def show(ref):
    return subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout


out = show(base)
src = show(ours)
for n in names:
    m = (re.search(rf"^[^\n]*\b{re.escape(n)}\b[^\n]*=[^\n]*;\n", src, re.M)
         or re.search(rf"^[^\n]*\b{re.escape(n)}\b[^\n]*=[^\n]*\n.*?^\}};\n", src, re.S | re.M))
    if not m:
        sys.exit(f"{n}: not found in {ours}")
    if re.search(rf"\b{re.escape(n)}\b\s*(\[\])?\s*=", out):
        continue
    out = out.rstrip("\n") + "\n\n" + m.group(0)
(ROOT / path).write_text(out)
print(f"{path}: rebuilt from {base} with {len(names)} definitions from {ours}")
