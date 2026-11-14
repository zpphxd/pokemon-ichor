#!/usr/bin/env python3
"""Claim unused Emerald flags or vars under Ichor names (see CLAUDE.md).

  python3 tools/ichor/claim.py flag FLAG_ICHOR_GOT_STARTER "chose a starter at the Akademia" ...
  python3 tools/ichor/claim.py var  VAR_ICHOR_HEARTH_TRIAL "Hearth Trial progress"

Arguments come in NAME COMMENT pairs. Each claim renames the lowest free
FLAG_UNUSED_0x… / VAR_UNUSED_0x… line in include/constants/{flags,vars}.h,
keeping its value and column alignment. Flags are only taken from 0x20–0x4FF,
the ordinary saved event flags (below the trainer flags, above the temp flags).

Ichor's own banks, saved in IchorSave (include/ichor_save.h), are claimed the
same way and leave the vanilla flags alone:

  python3 tools/ichor/claim.py bankflag  FLAG_ICHOR_MET_KERYKOS "met the Herald in Emporion"
  python3 tools/ichor/claim.py dailyflag FLAG_DAILY_ICHOR_ARES_BOUT "fought Ares's war-acolyte today"
  python3 tools/ichor/claim.py bankvar   VAR_ICHOR_HERALD_RUN "Herald's Run progress"

Each bank claim takes the next free id in the bank's general range and adds its
line between the bank's "adds lines here" and "end" markers.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KINDS = {
    "flag": (ROOT / "include/constants/flags.h", "FLAG", lambda v: 0x20 <= v < 0x500),
    "var": (ROOT / "include/constants/vars.h", "VAR", lambda v: True),
}

# bank kind: (header, name prefix, base macro, capacity, marker text)
BANKS = {
    "bankflag": (ROOT / "include/constants/flags.h", "FLAG_ICHOR_", "FLAG_ICHOR_GENERAL_START", 0x500,
                 "Ichor bank flags"),
    "dailyflag": (ROOT / "include/constants/flags.h", "FLAG_DAILY_ICHOR_", "FLAG_DAILY_ICHOR_GENERAL_START", 0x70,
                  "Ichor daily bank flags"),
    "bankvar": (ROOT / "include/constants/vars.h", "VAR_ICHOR_", "ICHOR_VARS_START", 32, "Ichor bank vars"),
}


def claim_bank(kind, claims):
    path, prefix, base, capacity, marker = BANKS[kind]
    text = path.read_text()
    lines = text.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith(f"// {marker}: claim.py"))
    end = next(i for i, l in enumerate(lines) if l == f"// {marker}: end")
    used = re.compile(rf"^#define \w+\s+\({base} \+ (0x[0-9A-Fa-f]+)\)")
    taken = [int(m.group(1), 16) for l in lines[start + 1:end] if (m := used.match(l))]
    nxt = max(taken) + 1 if taken else 0
    for name, _ in claims:
        if not name.startswith(prefix):
            raise SystemExit(f"{name}: {kind} names start with {prefix}")
        if re.search(rf"\b{name}\b", text):
            raise SystemExit(f"{name} is already defined")
    if nxt + len(claims) > capacity:
        raise SystemExit(f"only {capacity - nxt} free {kind}s left")
    new = []
    for (name, comment), off in zip(claims, range(nxt, nxt + len(claims))):
        new.append(f"#define {name.ljust(39)} ({base} + 0x{off:03X}) // Ichor: {comment}")
        print(f"{name} = {base} + 0x{off:03X}")
    lines[end:end] = new
    path.write_text("\n".join(lines))


def main():
    if len(sys.argv) < 4 or sys.argv[1] not in {**KINDS, **BANKS} or len(sys.argv[2:]) % 2:
        raise SystemExit(__doc__)
    claims = list(zip(sys.argv[2::2], sys.argv[3::2]))
    if sys.argv[1] in BANKS:
        return claim_bank(sys.argv[1], claims)
    path, prefix, allowed = KINDS[sys.argv[1]]
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
