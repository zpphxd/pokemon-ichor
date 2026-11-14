#!/usr/bin/env python3
"""Claim unused Emerald flags or vars under Ichor names (see CLAUDE.md).

  python3 tools/ichor/claim.py flag FLAG_ICHOR_GOT_STARTER "chose a starter at the Akademia" ...
  python3 tools/ichor/claim.py var  VAR_ICHOR_HEARTH_TRIAL "Hearth Trial progress"

Arguments come in NAME COMMENT pairs. Each claim renames the lowest free
FLAG_UNUSED_0x… / VAR_UNUSED_0x… line in include/constants/{flags,vars}.h,
keeping its value and column alignment. Flags are only taken from 0x20–0x4FF,
the ordinary saved event flags (below the trainer flags, above the temp flags).

Parallel build sessions each claim from their own range, so their claims
never collide when the director merges them. Pass --range LO-HI (hex) first:

  python3 tools/ichor/claim.py --range 0x200-0x2FF flag FLAG_ICHOR_... "..."

Ranges are assigned in tools/ichor/claim_ranges.md.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KINDS = {
    "flag": (ROOT / "include/constants/flags.h", "FLAG", lambda v: 0x20 <= v < 0x500),
    "var": (ROOT / "include/constants/vars.h", "VAR", lambda v: True),
}


def main():
    args = sys.argv[1:]
    lo, hi = None, None
    if args[:1] == ["--range"]:
        if len(args) < 2:
            raise SystemExit(__doc__)
        lo, hi = (int(x, 16) for x in args[1].split("-"))
        args = args[2:]
    if len(args) < 3 or args[0] not in KINDS or len(args[1:]) % 2:
        raise SystemExit(__doc__)
    path, prefix, base_allowed = KINDS[args[0]]
    allowed = base_allowed if lo is None else (lambda v: base_allowed(v) and lo <= v <= hi)
    claims = list(zip(args[1::2], args[2::2]))
    text = path.read_text()
    for name, _ in claims:
        if not name.startswith(f"{prefix}_ICHOR_"):
            raise SystemExit(f"{name}: Ichor names start with {prefix}_ICHOR_")
        if re.search(rf"\b{name}\b", text):
            raise SystemExit(f"{name} is already defined")

    lines = text.split("\n")
    pattern = re.compile(rf"^#define ({prefix}_UNUSED_0x[0-9A-Fa-f]+)(\s+)(0x[0-9A-Fa-f]+)\b.*$")
    free = [i for i, line in enumerate(lines)
            if (m := pattern.match(line)) and allowed(int(m.group(3), 16))]
    if len(free) < len(claims):
        raise SystemExit(f"only {len(free)} free {prefix.lower()}s left")
    for (name, comment), i in zip(claims, free):
        m = pattern.match(lines[i])
        width = len(m.group(1)) + len(m.group(2))
        lines[i] = f"#define {name.ljust(width - 1)} {m.group(3)} // Ichor: {comment}"
        print(f"{name} = {m.group(3)}")
    path.write_text("\n".join(lines))


if __name__ == "__main__":
    main()
