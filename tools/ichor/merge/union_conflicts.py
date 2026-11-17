#!/usr/bin/env python3
"""Resolve git conflict blocks by keeping both sides (upstream's first, then ours).

For shared append-only registries (tileset headers, labels, includes) where two
builders each added a block at the same spot.

    python3 tools/ichor/merge/union_conflicts.py FILE [...]
"""
import re
import sys
from pathlib import Path

PAT = re.compile(r"^<<<<<<< [^\n]*\n(.*?)^=======\n(.*?)^>>>>>>> [^\n]*\n", re.S | re.M)

for f in sys.argv[1:]:
    p = Path(f)
    t = p.read_text()
    n = len(PAT.findall(t))
    p.write_text(PAT.sub(lambda m: m.group(1) + m.group(2), t))
    print(f"{f}: {n} block(s) unioned")
