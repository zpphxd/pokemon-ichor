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

Ichor's own banks, saved in IchorSave (include/ichor_save.h), are claimed the
same way and leave the vanilla flags alone:

  python3 tools/ichor/claim.py bankflag  FLAG_ICHOR_MET_KERYKOS "met the Herald in Emporion"
  python3 tools/ichor/claim.py dailyflag FLAG_DAILY_ICHOR_ARES_BOUT "fought Ares's war-acolyte today"
  python3 tools/ichor/claim.py bankvar   VAR_ICHOR_HERALD_RUN "Herald's Run progress"

Each bank claim takes the next free id in the bank's general range and adds its
line between the bank's "adds lines here" and "end" markers. --range works for
them too: LO-HI is then an offset into the bank's general range.
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


def claim_bank(kind, claims, lo=None, hi=None):
    path, prefix, base, capacity, marker = BANKS[kind]
    text = path.read_text()
    lines = text.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith(f"// {marker}: claim.py"))
    end = next(i for i, l in enumerate(lines) if l == f"// {marker}: end")
    used = re.compile(rf"^#define \w+\s+\({base} \+ (0x[0-9A-Fa-f]+)\)")
    taken = [int(m.group(1), 16) for l in lines[start + 1:end] if (m := used.match(l))]
    lo = 0 if lo is None else lo
    hi = capacity - 1 if hi is None else min(hi, capacity - 1)
    for name, _ in claims:
        if not name.startswith(prefix):
            raise SystemExit(f"{name}: {kind} names start with {prefix}")
        if re.search(rf"\b{name}\b", text):
            raise SystemExit(f"{name} is already defined")
    free = [o for o in range(lo, hi + 1) if o not in taken]
    if len(free) < len(claims):
        raise SystemExit(f"only {len(free)} free {kind}s left in 0x{lo:03X}-0x{hi:03X}")
    for (name, comment), off in zip(claims, free):
        line = f"#define {name.ljust(39)} ({base} + 0x{off:03X}) // Ichor: {comment}"
        print(f"{name} = {base} + 0x{off:03X}")
        # keep the lines sorted by offset, so separate ranges merge as separate hunks
        at = next((i for i in range(start + 1, end) if (m := used.match(lines[i])) and int(m.group(1), 16) > off), end)
        lines[at:at] = [line]
        end += 1
    path.write_text("\n".join(lines))


def main():
    args = sys.argv[1:]
    lo, hi = None, None
    if args[:1] == ["--range"]:
        if len(args) < 2:
            raise SystemExit(__doc__)
        lo, hi = (int(x, 16) for x in args[1].split("-"))
        args = args[2:]
    if len(args) < 3 or args[0] not in {**KINDS, **BANKS} or len(args[1:]) % 2:
        raise SystemExit(__doc__)
    claims = list(zip(args[1::2], args[2::2]))
    if args[0] in BANKS:
        return claim_bank(args[0], claims, lo, hi)
    path, prefix, base_allowed = KINDS[args[0]]
    allowed = base_allowed if lo is None else (lambda v: base_allowed(v) and lo <= v <= hi)
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
