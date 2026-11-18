#!/usr/bin/env python3
"""Where each Aethos Pokémon lives: the species data and the wild tables, side by side.

  tools/ichor/distribution.py            the audit: exit 1 on a problem
  tools/ichor/distribution.py --report   every area in story order, with its species
  tools/ichor/distribution.py --json OLD.json --report   the same for another copy of the tables

The audit fails when
  STARTER   a starter line (Nebrel, Kindlepup, Hippofoal and their evolutions) is wild,
  HELD      a legendary, mythical, fossil or post-game line is wild in the main story
            (post-game maps, the Erymanthian Preserve's sealed thicket and the
            Oikoumene are outside the story and aren't checked),
  NOCATCH   a regular Aethos line has no wild catch point before the League (the Ascent,
            the League's Victory Road, counts), or its first stage is only ever wild at or
            past the level it evolves at (a baby line starts at its second stage),
  FOREIGN   a non-Aethos species is wild in a main-story area,
  UNPLACED  an Ichor map has wild tables but no place in STORY_ORDER,
  EARLY     a wild evolved form appears below the level it evolves at (BALANCE's
            "no early evolved forms in the wild").

The story order of the areas is STORY_ORDER below; design/DISTRIBUTION.md is the plan
these tables follow. Lines with a story reason not to be wild (a gift, a static, a
revival) are in NOT_WILD with that reason; a held line the user placed on purpose is in
HELD_OK. Python 3 stdlib plus PyYAML (macOS's
/usr/bin/python3 has it).
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
FAMILIES = ROOT / "src/data/pokemon/species_info/aethos_families.h"
ENCOUNTERS = ROOT / "src/data/wild_encounters.json"
PLAN = ROOT / "design/dex/plan.yaml"
SPECIES_DIR = ROOT / "design/dex/species"

# (stage, act, maps) in the order the story walks them. A map's place in this list is
# its story position; "League" and "Post" stages are after the League.
STORY_ORDER = [
    ("Kalliste", "I", ["MAP_KALLISTE_ROUTE1", "MAP_KALLISTE_ROUTE1_KRONION_HILL", "MAP_AKTI_TOWN",
                       "MAP_TRIREME_EUPLOIA_DECK"]),
    ("Emporion", "I", ["MAP_AEGINA_TOWN", "MAP_AEGINA_APHAIA_ROAD", "MAP_AEGINA_TEMPLE_OF_APHAIA",
                       "MAP_AEGINA_MOUNT_OROS", "MAP_EMPORION_HARBOR", "MAP_ROUTE4_ISTHMUS",
                       "MAP_HECATES_HOLLOW", "MAP_ROUTE5_SKIRONIAN_CLIFFS"]),
    ("Eleusa", "I", ["MAP_ELEUSA_VILLAGE", "MAP_ELEUSA_SANCTUM_B1F", "MAP_ELEUSA_SANCTUM_B2F",
                     "MAP_ELEUSA_SANCTUM_B3F"]),
    ("Thyrsa", "II", ["MAP_ROUTE6_ELEUTHERAI_ROAD", "MAP_MT_KITHAIRON", "MAP_THYRSA_CITY",
                      "MAP_ROUTE7_KRONIA_GROUNDS"]),
    ("Arkadia", "II", ["MAP_ROUTE8_KOPAIS_ROAD", "MAP_KOPAIS_KATAVOTHRES", "MAP_LEBADEIA",
                       "MAP_ROUTE9_PARNASSOS_CROSSROADS", "MAP_ROUTE9_KORYKIAN_CAVE", "MAP_KIRRHA",
                       "MAP_GULF_TRIREME", "MAP_AIGION", "MAP_ROUTE11_DRUM_PASS",
                       "MAP_ROUTE12_CYPRESS_ROAD", "MAP_ARKADIA_CYPRESS_WOOD", "MAP_ARKADIA",
                       "MAP_ERYMANTHOS_PRESERVE_OAKWOOD", "MAP_ERYMANTHOS_PRESERVE_MEADOW",
                       "MAP_ERYMANTHOS_PRESERVE_RIVER", "MAP_ERYMANTHOS_PRESERVE_CAVE"]),
    ("Astyra", "II", ["MAP_ROUTE13_HIGHLAND_ROAD", "MAP_NEMEA", "MAP_ROUTE14_NEMEA_ROAD",
                      "MAP_ROUTE14_TRETOS", "MAP_ROUTE15_MYSTERY_ROAD", "MAP_ROUTE16_CAPITAL_PASS",
                      "MAP_SALT_WELL_B1F", "MAP_SALT_WELL_B2F", "MAP_ASTYRA_HARBOR"]),
    ("Kaldera", "II", ["MAP_KALDERA", "MAP_KALDERA_TELCHINES_FORGE"]),
    ("Kythera", "III", ["MAP_KYTHERA_SKANDEIA", "MAP_KYTHERA_FOAM_ROAD", "MAP_KYTHERA_SPRING_OF_KALLIRHOE",
                        "MAP_KYTHERA_ECHO_CAVES", "MAP_KYTHERA_PAPHIA", "MAP_KYTHERA_NERAIDA_FALLS"]),
    ("Knossa", "III", ["MAP_KNOSSA_AMNISOS", "MAP_KNOSSA_BULL_ROAD", "MAP_KNOSSA_BULL_ROAD_VINEYARD",
                       "MAP_KNOSSA_BRONZE_HEEL", "MAP_LABYRINTH_RING1", "MAP_LABYRINTH_RING2",
                       "MAP_LABYRINTH_RING3", "MAP_LABYRINTH_RING4", "MAP_LABYRINTH_RING5",
                       "MAP_LABYRINTH_RING6", "MAP_LABYRINTH_RING7", "MAP_LABYRINTH_CELLARS",
                       "MAP_LABYRINTH_MINOS_TOMB"]),
    ("Lakonia", "III", ["MAP_GYTHEION", "MAP_ROUTE25_EUROTAS", "MAP_LAKONIA", "MAP_ROUTE26_SKIRITIS",
                        "MAP_LAKE_STYMPHALIA", "MAP_ROUTE27_ARKADIAN_HILLS", "MAP_ROUTE27_SKIRITAI_CAVE"]),
    ("Delphoi", "III", ["MAP_ROUTE28_SACRED_OLIVES", "MAP_ROUTE28_KASTALIAN_GORGE", "MAP_DELPHOI"]),
    ("League", "III", ["MAP_ASCENT_1F", "MAP_ASCENT_2F", "MAP_ASCENT_ICEFALL", "MAP_ASCENT_ICEFALL_DEEP",
                       "MAP_ASCENT_CRYSTAL_VAULT", "MAP_ASCENT_GLACIER", "MAP_ASCENT_3F"]),
    ("Post", "Post", ["MAP_ERYMANTHOS_PRESERVE_THICKET"]),
]
STORY_STAGES = [s for s, a, m in STORY_ORDER if a in ("I", "II", "III") and s != "League"]

# Lines held out of the wild on purpose, by plan.yaml section or role.
HELD_SECTIONS = {"Starters", "Post-game", "Legendaries and mythicals"}
HELD_ROLES = {"fossil", "legendary", "mythical", "box legendary", "legendary trio"}

# Regular lines with a story reason not to be wild: line id -> why.
NOT_WILD = {
    "minotaur": "the Labyrinth's heart holds the one Minotaur, a story static",
    "echo": "met only beside Narcissus at the Echo Caves' scripted pool (a static)",
}

# Held lines with a placement the user asked for: line id -> (maps, why).
HELD_OK = {
    "styx": (("MAP_ASCENT_ICEFALL_DEEP", "MAP_ASCENT_CRYSTAL_VAULT"),
             "the user's Ascent (IDEAS, 2026-11-17): Stygiad in the coldest dark, and nowhere else"),
}

# Lines whose first wild stage arriving after its evolution level is accepted: id -> why.
LATE_OK = {}

TIMES = ("Morning", "Day", "Evening", "Night")
METHODS = ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons")


def species():
    """name -> {const, line, section, roles, evos: [(to, level|None, method)], prev}."""
    text = FAMILIES.read_text()
    out = {}
    for m in re.finditer(r"\[SPECIES_(\w+)\] =\s*\{(.*?)\n    \},", text, re.S):
        const, body = m.group(1), m.group(2) + "\n"
        name = re.search(r'\.speciesName = _\("([^"]+)"\)', body).group(1)
        evos = []
        em = re.search(r"\.evolutions = EVOLUTION\((.*?)\),\n", body, re.S)
        if em:
            for e in re.finditer(r"\{(EVO_\w+), (\w+), SPECIES_(\w+)", em.group(1)):
                lvl = int(e.group(2)) if e.group(1) == "EVO_LEVEL" and e.group(2).isdigit() else None
                evos.append((e.group(3), lvl or None, e.group(1)))
        out[const] = {"const": const, "name": name, "evos": evos, "prev": None}
    for c, s in out.items():
        for to, _, _ in s["evos"]:
            out[to]["prev"] = c
    plan = yaml.safe_load(PLAN.read_text())
    sec = None
    meta = {}
    for ln in plan["lines"]:
        sec = ln.get("section", sec)
        meta[ln["id"]] = (sec, set(ln.get("roles") or []))
    byname = {s["name"]: c for c, s in out.items()}
    for f in sorted(SPECIES_DIR.glob("*.yaml")):
        d = yaml.safe_load(f.read_text())
        sec, roles = meta[d["line"]]
        for sp in d["species"]:
            c = byname[sp["name"]]
            out[c].update(line=d["line"], section=sec, roles=roles, dex=sp["dex"],
                          habitat=sp.get("habitat", ""))
    return out


def lines(sp):
    """line id -> member consts in evolution order (branches after their base)."""
    by = defaultdict(list)
    for c, s in sorted(sp.items(), key=lambda kv: kv[1]["dex"]):
        by[s["line"]].append(c)
    return dict(by)


def held(s):
    return s["section"] in HELD_SECTIONS or bool(s["roles"] & HELD_ROLES)


def is_starter(s):
    return s["section"] == "Starters"


def evo_level(sp, c):
    """The level a wild c can first be met at in its evolved form: its previous stage's
    level threshold (None if it evolves by stone, trade, friendship or place)."""
    p = sp[c]["prev"]
    if not p:
        return 0
    for to, lvl, _ in sp[p]["evos"]:
        if to == c:
            return lvl
    return None


def map_positions():
    pos = {}
    i = 0
    for stage, act, maps in STORY_ORDER:
        for m in maps:
            pos[m] = (i, stage, act)
            i += 1
    return pos


def tables():
    """[(map, time, method, [mons])] for every Ichor wild table."""
    d = json.loads(ENCOUNTERS.read_text())
    out = []
    for e in d["wild_encounter_groups"][0]["encounters"]:
        time = e["base_label"].rsplit("_", 1)[-1]
        time = time if time in TIMES else "Morning"
        for meth in METHODS:
            if meth in e:
                out.append((e["map"], time, meth, e[meth]["mons"]))
    return out


def occurrences(sp):
    """const -> [(pos, map, time, method, min, max)] over the story-ordered maps."""
    pos = map_positions()
    occ = defaultdict(list)
    for m, time, meth, mons in tables():
        p = pos.get(m)
        for mon in mons:
            c = mon["species"].removeprefix("SPECIES_")
            occ[c].append((p[0] if p else None, m, time, meth, mon["min_level"], mon["max_level"]))
    return occ


def audit():
    sp = species()
    occ = occurrences(sp)
    pos = map_positions()
    # The main story runs to the Pantheon: the Ascent (the League stage) is its Victory
    # Road, so a catch there is still before the League's battles.
    post = min(p for p, st, a in pos.values() if a == "Post")
    problems = []
    for m in sorted({t[0] for t in tables()} - set(pos)):
        problems.append(f"UNPLACED {m} has wild tables but no place in STORY_ORDER (tools/ichor/distribution.py)")
    for c, hits in occ.items():
        story_hits = [h for h in hits if h[0] is not None and h[0] < post]
        if not story_hits:
            continue
        s = sp.get(c)
        if s is None:
            for h in story_hits:
                problems.append(f"FOREIGN  {c} is wild on {h[1]} ({h[2]} {h[3]}); the story is Aethos-only")
            continue
        maps = sorted({h[1] for h in story_hits})
        if is_starter(s):
            problems.append(f"STARTER  {s['name']} is wild on {', '.join(maps)}")
        elif held(s):
            ok = HELD_OK.get(s["line"], ((), ""))[0]
            bad = [m for m in maps if m not in ok]
            if bad:
                problems.append(f"HELD     {s['name']} ({s['section']}) is wild on {', '.join(bad)}")
        lvl = evo_level(sp, c)
        for h in story_hits:
            if lvl and h[4] < lvl:
                problems.append(f"EARLY    {s['name']} at Lv{h[4]} on {h[1]} ({h[2]} {h[3]}); "
                                f"it evolves from {sp[s['prev']]['name']} at {lvl}")
    for lid, members in lines(sp).items():
        s0 = sp[members[0]]
        if held(s0) or lid in NOT_WILD:
            continue
        # a baby hatches from eggs; the line's wild life starts at its second stage
        base = members[1] if "baby" in s0["roles"] and len(members) > 1 else members[0]
        lvl = next((l for _, l, _ in sp[base]["evos"] if l), None)
        hits = sorted(h for h in occ.get(base, []) if h[0] is not None and h[0] < post)
        good = [h for h in hits if not lvl or h[4] < lvl]
        if good or lid in LATE_OK:
            continue
        if hits:
            h = hits[0]
            problems.append(f"NOCATCH  {sp[base]['name']} is only wild at Lv{h[4]}+ (first on {h[1]}), "
                            f"past the level {lvl} it evolves at")
        else:
            problems.append(f"NOCATCH  {sp[base]['name']} (the {s0['name']} line) has no wild catch point "
                            f"before the League")
    return problems


def summary(sp=None):
    """Per act: new species, new lines (a line's first wild catch), and the land tables'
    most widespread species (maps whose land tables hold it)."""
    sp = sp or species()
    pos = map_positions()
    first_seen, first_line = {}, {}
    land = defaultdict(set)
    rows = sorted(((pos[m][0], m, meth, mons) for m, t, meth, mons in tables() if m in pos), key=lambda r: r[:3])
    for p, m, meth, mons in rows:
        st, act = pos[m][1], pos[m][2]
        for mon in mons:
            c = mon["species"].removeprefix("SPECIES_")
            first_seen.setdefault(c, act)
            if c in sp:
                first_line.setdefault(sp[c]["line"], act)
            if meth == "land_mons":
                land[c].add(m)
    acts = {a: (sum(1 for v in first_seen.values() if v == a), sum(1 for v in first_line.values() if v == a))
            for a in ("I", "II", "III", "Post")}
    wide = sorted(((len(v), sp[c]["name"] if c in sp else c) for c, v in land.items()), reverse=True)[:8]
    return acts, wide


def markdown():
    """The species-by-area tables of design/DISTRIBUTION.md, from the json. Each cell lists
    a table's species, commonest first; a species is bold where it is first met."""
    sp = species()
    pos = map_positions()
    per = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    rates = {"land_mons": [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1], "water_mons": [60, 30, 5, 4, 1],
             "rock_smash_mons": [60, 30, 5, 4, 1], "fishing_mons": [70, 30, 60, 20, 20, 40, 40, 15, 4, 1]}
    times_seen = defaultdict(set)
    for m, t, meth, mons in tables():
        if m not in pos:
            continue
        col = {"land_mons": "night" if t == "Night" else "day", "water_mons": "water",
               "fishing_mons": "fish", "rock_smash_mons": "rock"}[meth]
        if col in ("day", "night"):
            times_seen[(m, col)].add(t)
        for mon, r in zip(mons, rates[meth]):
            per[m][col][mon["species"].removeprefix("SPECIES_")] += r
    seen = set()
    out = []
    for stage, act, maps in STORY_ORDER:
        out.append(f"\n### {stage} (Act {act})\n")
        out.append("| Map | Land by day | Land at night | Water and rods | Rock Smash |")
        out.append("|---|---|---|---|---|")
        for m in maps:
            if m not in per:
                continue
            cells, bolded = [], set()
            for col in ("day", "night", "water+fish", "rock"):
                tally = defaultdict(float)
                for k in col.split("+"):
                    n = max(1, len(times_seen.get((m, k), ())) or 1)
                    for c, v in per[m][k].items():
                        tally[c] += v / n
                parts = []
                for c, v in sorted(tally.items(), key=lambda kv: -kv[1]):
                    name = sp[c]["name"] if c in sp else c
                    if c not in seen and c not in bolded and m in pos and pos[m][2] != "Post":
                        name = f"**{name}**"
                        bolded.add(c)
                    parts.append(name)
                cells.append(", ".join(parts) or "")
            for col in ("day", "night", "water", "fish", "rock"):
                seen.update(per[m][col])
            out.append(f"| {m.removeprefix('MAP_')} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def report():
    print(markdown())
    acts, wide = summary()
    print()
    for a, (ns, nl) in acts.items():
        print(f"Act {a}: {ns} new species, {nl} new lines")
    print("Widest in the land tables (maps):", ", ".join(f"{n} {k}" for k, n in wide))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--report", action="store_true", help="the species-by-area tables and the act counts")
    ap.add_argument("--json", type=Path, help="read this wild_encounters.json instead (e.g. an old one)")
    args = ap.parse_args()
    global ENCOUNTERS
    if args.json:
        ENCOUNTERS = args.json
    if args.report:
        report()
        return 0
    probs = audit()
    for p in probs:
        print(p)
    if probs:
        print(f"distribution: {len(probs)} problem(s); see design/DISTRIBUTION.md")
        return 1
    print("distribution: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
