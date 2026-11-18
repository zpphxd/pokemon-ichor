#!/usr/bin/env python3
"""Give every removable field gate (a cut tree, rubble, a Labrys seal, a web)
its own saved flag, so it stays gone once cleared.

A gate object with flag 0 is only hidden until it scrolls out of view; then
the engine respawns it, so the tree "grows back" a few steps later.

  /usr/bin/python3 tools/ichor/maps/gate_flags.py           fix: claim and set flags
  /usr/bin/python3 tools/ichor/maps/gate_flags.py --check   list flagless gates, exit 1 if any

Run it after any map generator that places gates. Flags come from bankflag
offsets 0x5D0-0x5FF (tools/ichor/claim_ranges.md); reruns reuse the same names.
Run by tools/ichor/smoke_test.sh with --check.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GATES = {"EventScript_CutTree", "EventScript_RockSmash", "EventScript_IchorRubble",
         "EventScript_IchorThicket", "EventScript_IchorLabrysSeal", "EventScript_IchorCobweb",
         "EventScript_IchorThornweb", "EventScript_IchorColumnDrum"}


def is_gate(o):
    s = o.get("script", "")
    return s in GATES or s.endswith("_EventScript_Chains")


def flagless():
    for p in sorted((ROOT / "data/maps").glob("*/map.json")):
        d = json.loads(p.read_text())
        for o in d.get("object_events", []):
            if is_gate(o) and o.get("flag", "0") in ("0", "", None):
                yield p, o


def name_for(mapname, o):
    kind = {"EventScript_CutTree": "TREE", "EventScript_RockSmash": "RUBBLE",
            "EventScript_IchorLabrysSeal": "SEAL"}.get(o["script"], "GATE")
    m = re.sub(r"[^A-Z0-9]", "", mapname.upper())
    return f"FLAG_ICHOR_CLEARED_{m}_{kind}_{o['x']}_{o['y']}"


def main():
    hits = list(flagless())
    if "--check" in sys.argv:
        for p, o in hits:
            print(f"gate_flags: {p.parent.name} ({o['x']},{o['y']}) {o['script']} has no flag")
        print(f"gate_flags: {len(hits)} flagless gates")
        sys.exit(1 if hits else 0)
    flags_h = (ROOT / "include/constants/flags.h").read_text()
    for p, o in hits:
        name = name_for(p.parent.name, o)
        if not re.search(rf"#define\s+{name}\b", flags_h):
            subprocess.run([sys.executable, str(ROOT / "tools/ichor/claim.py"), "--range", "0x5D0-0x5FF",
                            "bankflag", name, f"{p.parent.name}: the {o['script']} gate at ({o['x']},{o['y']}) stays cleared"],
                           check=True, cwd=ROOT)
            flags_h = (ROOT / "include/constants/flags.h").read_text()
        text = p.read_text()
        d = json.loads(text)
        for q in d["object_events"]:
            if q.get("x") == o["x"] and q.get("y") == o["y"] and q.get("script") == o["script"]:
                q["flag"] = name
        p.write_text(json.dumps(d, indent=2) + "\n")
        print(f"gate_flags: {p.parent.name} ({o['x']},{o['y']}) -> {name}")


if __name__ == "__main__":
    main()
