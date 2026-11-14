#!/usr/bin/env python3
"""Validate the Aethos dex plan and build its review outputs.

Reads design/dex/plan.yaml. Assigns dex numbers in file order, checks the
structure, and writes:
  design/dex/PLAN.md   the plan as Markdown tables (committed)
  --json PATH          the same data as JSON, for the review page
  --html PATH          the review page (template: tools/dex/plan_page.html)

Exit status is 1 if any check fails.
"""
import argparse
import collections
import json
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
PLAN = ROOT / "design/dex/plan.yaml"
PLAN_MD = ROOT / "design/dex/PLAN.md"
TEMPLATE = ROOT / "tools/dex/plan_page.html"

TYPES = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting",
         "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost",
         "Dragon", "Dark", "Steel", "Fairy"]
TARGET_TOTAL = 151

# method -> (table label, required keys)
METHODS = {
    "level": ("Level", ["level"]),
    "level_day": ("Level, daytime", ["level"]),
    "level_night": ("Level, night", ["level"]),
    "level_female": ("Level, females only", ["level"]),
    "stone": ("Evolution stone", ["item"]),
    "trade": ("Trade", []),
    "trade_item": ("Trade holding an item", ["item"]),
    "friendship": ("Friendship", []),
    "friendship_day": ("Friendship, daytime", []),
    "held_item": ("Level up holding an item", ["item"]),
    "location": ("Level up at a place", ["place"]),
    "move": ("Level up knowing a move", ["move"]),
}


def describe(evo):
    m = evo["method"]
    if m == "level":
        return f"Lv {evo['level']}"
    if m == "level_day":
        return f"Lv {evo['level']} (day)"
    if m == "level_night":
        return f"Lv {evo['level']} (night)"
    if m == "level_female":
        return f"Lv {evo['level']} (♀ only)"
    if m == "stone":
        return evo["item"]
    if m == "trade":
        return "Trade"
    if m == "trade_item":
        return f"Trade holding {evo['item']}"
    if m == "friendship":
        return "Friendship"
    if m == "friendship_day":
        return "Friendship (day)"
    if m == "held_item":
        gate = f" (Lv {evo['level']}+)" if evo.get("level") else ""
        return f"Level up holding {evo['item']}{gate}"
    if m == "location":
        return f"Level up at {evo['place']}"
    if m == "move":
        return f"Level up knowing {evo['move']}"
    return m


def load():
    return yaml.safe_load(PLAN.read_text())


def build(data):
    """Return (species list, errors)."""
    errors = []
    species = []
    seen_ids = set()
    dex = 0
    section = None
    for line in data["lines"]:
        section = line.get("section", section)
        line["section"] = section
        lid = line.get("id")
        if not section:
            errors.append(f"{lid}: no section before it")
        if not lid or lid in seen_ids:
            errors.append(f"line id missing or duplicated: {lid!r}")
        seen_ids.add(lid)
        for key in ("roles", "myth", "design", "habitat", "members"):
            if not line.get(key):
                errors.append(f"{lid}: missing {key}")
        members = line.get("members", [])
        first = dex + 1
        for i, mem in enumerate(members):
            dex += 1
            types = mem.get("types", [])
            if not 1 <= len(types) <= 2 or len(set(types)) != len(types):
                errors.append(f"#{dex} {mem.get('concept')}: needs 1-2 distinct types, got {types}")
            for t in types:
                if t not in TYPES:
                    errors.append(f"#{dex}: unknown type {t!r}")
            evos = mem.get("evo") or []
            if isinstance(evos, dict):
                evos = [evos]
            targets = []
            for evo in evos:
                method = evo.get("method")
                if method not in METHODS:
                    errors.append(f"#{dex}: unknown evolution method {method!r}")
                    continue
                for key in METHODS[method][1]:
                    if key not in evo:
                        errors.append(f"#{dex}: {method} needs {key}")
                to = evo.get("to", i + 1)
                if not i < to < len(members):
                    errors.append(f"#{dex}: evolves into member {to}, which is not later in the line")
                else:
                    targets.append(to)
            species.append({
                "dex": dex,
                "line": lid,
                "index": i,
                "concept": mem["concept"],
                "types": types,
                "baby": bool(mem.get("baby")),
                "evos": evos,
                "targets": targets,
                "first": first,
            })
        # Every member after the first must be reachable from an earlier one,
        # unless the "line" is a group of separate species (the Moirai).
        reach = set(range(len(members))) if line.get("group") else {0}
        for s in species[first - 1:]:
            if s["index"] in reach:
                reach.update(s["targets"])
        for s in species[first - 1:]:
            if s["index"] not in reach:
                errors.append(f"#{s['dex']} {s['concept']}: no earlier member evolves into it")
        line["first_dex"] = first
        line["last_dex"] = dex
    if dex != TARGET_TOTAL:
        errors.append(f"the dex has {dex} species, not {TARGET_TOTAL}")
    names = collections.Counter(s["concept"] for s in species)
    for name, n in names.items():
        if n > 1:
            errors.append(f"concept label used {n} times: {name}")
    return species, errors


def stats(data, species):
    by_type = {t: {"mono": 0, "dual": 0} for t in TYPES}
    for s in species:
        kind = "mono" if len(s["types"]) == 1 else "dual"
        for t in s["types"]:
            by_type[t][kind] += 1
    methods = collections.OrderedDict((m, []) for m in METHODS)
    for s in species:
        for evo in s["evos"]:
            methods[evo["method"]].append(f"#{s['dex']} {s['concept']}")
    shapes = collections.Counter()
    for line in data["lines"]:
        n = len(line["members"])
        if line.get("group"):
            shapes["single"] += n
            continue
        branch = any(isinstance(m.get("evo"), list) for m in line["members"])
        shapes["branching" if branch else {1: "single", 2: "two-stage", 3: "three-stage"}.get(n, f"{n}-stage")] += 1
    roles = collections.Counter(r for line in data["lines"] for r in line["roles"])
    combos = collections.Counter("/".join(s["types"]) for s in species if len(s["types"]) == 2)
    return {
        "by_type": by_type,
        "methods": methods,
        "shapes": dict(shapes),
        "roles": dict(roles),
        "dual": sum(1 for s in species if len(s["types"]) == 2),
        "repeated_combos": {k: v for k, v in combos.items() if v > 1},
    }


def evolves_text(s, species_by_line):
    parts = []
    line = species_by_line[s["line"]]
    for evo in s["evos"]:
        to = evo.get("to", s["index"] + 1)
        parts.append(f"→ {line[to]['concept']}: {describe(evo)}")
    return "; ".join(parts)


def markdown(data, species, st):
    by_line = collections.defaultdict(list)
    for s in species:
        by_line[s["line"]].append(s)
    lines_by_id = {l["id"]: l for l in data["lines"]}
    out = []
    w = out.append
    w("# Aethos regional dex: Gate 1 plan")
    w("")
    w("Generated by `tools/dex/plan.py` from `design/dex/plan.yaml`. Edit the YAML, not this file.")
    w("")
    w("The labels below are working concepts, not names. Names, stats, abilities, moves and Pokédex entries come at Gate 2, after this plan is approved.")
    w("")
    w("## At a glance")
    w("")
    sh = st["shapes"]
    w(f"- **{len(species)} species**: {sh.get('three-stage', 0)} three-stage lines, "
      f"{sh.get('two-stage', 0)} two-stage lines, {sh.get('branching', 0)} branching line "
      f"and {sh.get('single', 0)} single-stage species.")
    w(f"- **{st['dual']} dual-type** and **{len(species) - st['dual']} single-type** species.")
    babies = [s["concept"] for s in species if s["baby"]]
    w(f"- **Babies:** {', '.join(babies)}.")
    w("- **Targets for Gate 2:** starters about 310 / 405 / 530 BST; the pseudo-legendary 300 / 420 / 600; "
      "Kronos and Kairos about 680; the Moirai about 580 each; Pegasus about 580; the mythicals 600.")
    w("- **Names:** the engine allows 12 characters (`POKEMON_NAME_LENGTH`); we aim for Gen 3's 10. Categories fit in 12.")
    w(f"- **ROM:** front, back, shiny, icon, footprint and follower sprites for {len(species)} species come to roughly 1.2–1.5 MB "
      "if they reuse existing cries, about a quarter of today's headroom.")
    w("- **Moves:** the plan needs no new moves. Any signature move proposed at Gate 2 is flagged as a cost.")
    w("")
    w("## Decisions for you")
    w("")
    for d in data["decisions"]:
        w(f"**{d['id']}. {d['title']}.** {d['detail']}")
        w("")
        w(f"*Recommendation:* {d['recommend']}")
        w("")
        w(f"*Answer:* {d.get('answer', 'open')}")
        w("")
    w("## Type spread")
    w("")
    w("A species counts once for each of its types.")
    w("")
    w("| Type | Total | Single-type | Part of a dual type |")
    w("|---|---:|---:|---:|")
    for t in TYPES:
        b = st["by_type"][t]
        w(f"| {t} | {b['mono'] + b['dual']} | {b['mono']} | {b['dual']} |")
    w("")
    if st["repeated_combos"]:
        w("Dual types used more than once: " + ", ".join(f"{k} ×{v}" for k, v in sorted(st["repeated_combos"].items())) + ".")
        w("")
    w("## Evolution methods")
    w("")
    w("| Method | Count | Who |")
    w("|---|---:|---|")
    for m, who in st["methods"].items():
        if who:
            w(f"| {METHODS[m][0]} | {len(who)} | {', '.join(who)} |")
    w("")
    w(f"## All {len(species)} slots")
    w("")
    w("| # | Concept | Types | Evolves | Line | Role |")
    w("|---:|---|---|---|---|---|")
    for s in species:
        line = lines_by_id[s["line"]]
        n = len(line["members"])
        pos = "single" if n == 1 or line.get("group") else f"{s['index'] + 1} of {n}"
        role = ", ".join(line["roles"])
        w(f"| {s['dex']:03d} | {s['concept']}{' (baby)' if s['baby'] else ''} | {' / '.join(s['types'])} | "
          f"{evolves_text(s, by_line)} | {line['id']} ({pos}) | {role} |")
    w("")
    w("## The lines: myth, design and habitat")
    w("")
    section = None
    for line in data["lines"]:
        if line["section"] != section:
            section = line["section"]
            w(f"### {section}")
            w("")
        mem = by_line[line["id"]]
        rng = f"#{line['first_dex']:03d}" if line["first_dex"] == line["last_dex"] else f"#{line['first_dex']:03d}–{line['last_dex']:03d}"
        chain = " → ".join(f"{s['concept']} ({'/'.join(s['types'])})" for s in mem)
        w(f"#### {rng} {chain}")
        w("")
        w(f"- **Role:** {', '.join(line['roles'])}")
        w(f"- **Myth:** {line['myth']}")
        w(f"- **Design:** {line['design']}")
        w(f"- **Lives in:** {line['habitat']}")
        if line.get("notes"):
            w(f"- **Notes:** {line['notes']}")
        w("")
    return "\n".join(out)


def to_json(data, species, st):
    by_line = collections.defaultdict(list)
    for s in species:
        by_line[s["line"]].append(s)
    lines = []
    for line in data["lines"]:
        lines.append({
            "id": line["id"],
            "section": line["section"],
            "roles": line["roles"],
            "myth": line["myth"],
            "design": line["design"],
            "habitat": line["habitat"],
            "notes": line.get("notes", ""),
            "members": [{
                "dex": s["dex"],
                "concept": s["concept"],
                "types": s["types"],
                "baby": s["baby"],
                "evolves": evolves_text(s, by_line),
            } for s in by_line[line["id"]]],
        })
    return {
        "lines": lines,
        "decisions": data["decisions"],
        "types": TYPES,
        "typeSpread": st["by_type"],
        "methods": [{"label": METHODS[m][0], "who": who} for m, who in st["methods"].items() if who],
        "shapes": st["shapes"],
        "dual": st["dual"],
        "total": len(species),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", type=pathlib.Path, help="also write the plan as JSON")
    ap.add_argument("--html", type=pathlib.Path, help="also write the review page")
    ap.add_argument("--check", action="store_true", help="only validate; write nothing")
    args = ap.parse_args()

    data = load()
    species, errors = build(data)
    st = stats(data, species)
    for e in errors:
        print("error:", e, file=sys.stderr)

    print(f"{len(species)} species, {len(data['lines'])} lines, {st['dual']} dual-type")
    print("types: " + ", ".join(f"{t} {b['mono'] + b['dual']}" for t, b in st["by_type"].items()))
    print("shapes: " + ", ".join(f"{k} {v}" for k, v in sorted(st["shapes"].items())))
    if errors:
        return 1
    if args.check:
        return 0
    PLAN_MD.write_text(markdown(data, species, st) + "\n")
    payload = to_json(data, species, st)
    if args.json:
        args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=1))
    if args.html:
        page = TEMPLATE.read_text().replace("/*PLAN_DATA*/null", json.dumps(payload, ensure_ascii=False))
        args.html.write_text(page)
    print("wrote", PLAN_MD.relative_to(ROOT), *(p for p in (args.json, args.html) if p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
