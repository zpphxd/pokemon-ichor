#!/usr/bin/env python3
"""Claim unused Emerald flags or vars under Ichor names (see CLAUDE.md).

  python3 tools/ichor/claim.py flag FLAG_ICHOR_GOT_STARTER "chose a starter at the Akademia" ...
  python3 tools/ichor/claim.py var  VAR_ICHOR_HEARTH_TRIAL "Hearth Trial progress"

Arguments come in NAME COMMENT pairs. Each claim renames the lowest free
FLAG_UNUSED_0x… / VAR_UNUSED_0x… line in include/constants/{flags,vars}.h,
keeping its value and column alignment. Flags are only taken from 0x20–0x4FF,
the ordinary saved event flags (below the trainer flags, above the temp flags).
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
    if len(sys.argv) < 4 or sys.argv[1] not in KINDS or len(sys.argv[2:]) % 2:
        raise SystemExit(__doc__)
    path, prefix, allowed = KINDS[sys.argv[1]]
    claims = list(zip(sys.argv[2::2], sys.argv[3::2]))
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
