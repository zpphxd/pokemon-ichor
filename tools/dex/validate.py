#!/usr/bin/env python3
"""Check the Aethos dex's full species entries (Gate 2).

Reads design/dex/plan.yaml and every design/dex/species/*.yaml, then checks
each entry against the plan, design/dex/SCHEMA.md and the expansion's own
tables of species, moves and abilities.

  python3 tools/dex/validate.py                 check every entry written so far
  python3 tools/dex/validate.py --lines a,b     check only these lines
  python3 tools/dex/validate.py --complete      also require all 151 entries

Exit status is 1 if any error is found. Warnings don't fail the run.
"""
import argparse
import collections
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/dex"))
import plan as planlib  # noqa: E402

SPECIES_DIR = ROOT / "design/dex/species"
TYPES = set(planlib.TYPES)
STATS = ["hp", "atk", "def", "spa", "spd", "spe"]
EGG_GROUPS = {"Monster", "Water 1", "Water 2", "Water 3", "Bug", "Flying", "Field", "Fairy", "Grass",
              "Human-Like", "Mineral", "Amorphous", "Dragon", "Ditto", "Undiscovered"}
GROWTH = {"Erratic", "Fast", "Medium Fast", "Medium Slow", "Slow", "Fluctuating"}
FEMALE_PCTS = {0, 12.5, 25, 50, 75, 87.5, 100}
NAME_MAX, NAME_AIM, CATEGORY_MAX, DEX_LINE_MAX = 12, 10, 12, 42
DEX_CHARS = re.compile(r"^[A-Za-z0-9 .,'!?\-:;()é…]*$")
FORBIDDEN_ROOTS = ["aegis", "gryphon", "griffin", "medusa", "titan", "chimera"]
CAST = ["daphne", "alethea", "kleon", "phaedon", "elpis", "aristeides", "hyperion", "iapetos", "rhea",
        "kronos", "ione", "kerykos", "chloe", "thespis", "kallisto", "talos", "galatea", "phemonoe",
        "brasidas", "themistokles", "hypatia", "olympias", "melitta", "halia"]
# Well-known fan-made species to keep clear of (Smogon CAP, Pokémon Uranium).
FAN_NAMES = ["Syclant", "Revenankh", "Pyroak", "Fidgit", "Stratagem", "Arghonaut", "Kitsunoh", "Cyclohm",
             "Colossoil", "Krilowatt", "Voodoom", "Tomohawk", "Necturna", "Mollux", "Aurumoth", "Malaconda",
             "Cawmodore", "Volkraken", "Plasmanta", "Naviathan", "Crucibelle", "Kerfluffle", "Pajantom",
             "Jumbao", "Caribolt", "Smokomodo", "Snaelstrom", "Equilibra", "Astrolotl", "Miasmaw", "Chromera",
             "Venomicon", "Saharaja", "Hemogoblin", "Cresceidon", "Chuggalong", "Shox", "Ramnarok",
             "Orchynx", "Rozorchid", "Raptorch", "Archilles", "Eletux", "Electruxo", "Nucleon", "Hazma", "Urayne"]

# BST bands, (low, high), by role and stage index. See SCHEMA.md.
BANDS = {
    "starter": [(309, 318), (405, 405), (525, 535)],
    "route bird": [(245, 260), (340, 360), (480, 500)],
    "fast bug": [(195, 210), (205, 225), (395, 420)],
    "common mammal": [(240, 265), (400, 430)],
    "three": [(280, 330), (380, 430), (480, 535)],
    "two": [(250, 340), (420, 510)],
    "mascot": [(180, 250), (300, 330), (480, 495)],
    "baby two": [(180, 250), (420, 510)],
    "magikarp": [(190, 210), (520, 545)],
    "fossil": [(340, 380), (480, 525)],
    "single": [(380, 510)],
    "pseudo": [(300, 300), (420, 420), (600, 600)],
    "legendary trio": [(570, 590)],
    "box legendary": [(670, 690)],
    "legendary": [(570, 590)],
    "mythical": [(600, 600)],
    "champion ace": [(320, 345), (520, 540)],
}


def read_enum(path, prefix, stop):
    names = []
    for raw in path.read_text().splitlines():
        if raw.strip().startswith(stop):
            break
        m = re.match(rf"\s*({prefix}\w+)\b", raw)
        if m:
            names.append(m.group(1))
    return set(names)


def display_names(path, prefix, allowed):
    text = path.read_text()
    out = {}
    for const, name in re.findall(rf"\[({prefix}\w+)\]\s*=\s*\{{\s*\.name\s*=\s*(?:COMPOUND_STRING|_)\(\"([^\"]+)\"\)", text):
        if const in allowed:
            out[name] = const
    return out


def engine_tables():
    moves_enum = read_enum(ROOT / "include/constants/moves.h", "MOVE_", "MOVES_COUNT =") - {"MOVE_NONE"}
    abil_enum = read_enum(ROOT / "include/constants/abilities.h", "ABILITY_", "ABILITIES_COUNT =") - {"ABILITY_NONE"}
    moves = display_names(ROOT / "src/data/moves_info.h", "MOVE_", moves_enum)
    abilities = display_names(ROOT / "src/data/abilities.h", "ABILITY_", abil_enum)
    species = set()
    for f in (ROOT / "src/data/pokemon/species_info").glob("*.h"):
        species.update(re.findall(r'\.speciesName = _\("([^"]+)"\)', f.read_text()))
    return moves, abilities, species


def distance(a, b):
    a, b = a.lower(), b.lower()
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def band_key(line, index):
    roles = set(line["roles"])
    n = len(line["members"])
    for r in ("pseudo", "legendary trio", "box legendary", "mythical", "legendary", "starter",
              "route bird", "common mammal", "fossil", "champion ace"):
        if r in roles:
            return r
    if "mascot" in roles:
        return "mascot"
    if "Magikarp role" in roles:
        return "magikarp"
    if "early bug" in roles and n == 3:
        return "fast bug"
    if "baby" in roles and n == 2:
        return "baby two"
    if n == 1:
        return "single"
    if any(isinstance(m.get("evo"), list) for m in line["members"]):
        return "two"           # the branching seed: both branches are final stages
    return "three" if n == 3 else "two"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lines", help="comma-separated line ids to check")
    ap.add_argument("--complete", action="store_true", help="require every entry in the plan")
    args = ap.parse_args()

    data = planlib.load()
    plan_species, plan_errors = planlib.build(data)
    if plan_errors:
        print("plan.yaml has errors; run tools/dex/plan.py first", file=sys.stderr)
        return 1
    lines = {l["id"]: l for l in data["lines"]}
    by_dex = {s["dex"]: s for s in plan_species}
    # The real pre-evolution of each species, so branches compare with their seed.
    pre_of = {}
    for s in plan_species:
        for t in s["targets"]:
            pre_of[s["first"] + t] = s["dex"]
    moves, abilities, existing = engine_tables()
    move_lc = {k.lower(): k for k in moves}
    abil_lc = {k.lower(): k for k in abilities}

    errors, warnings = [], []
    err = lambda where, msg: errors.append(f"{where}: {msg}")
    warn = lambda where, msg: warnings.append(f"{where}: {msg}")

    wanted = set(args.lines.split(",")) if args.lines else None
    entries = {}
    for path in sorted(SPECIES_DIR.glob("*.yaml")):
        try:
            doc = yaml.safe_load(path.read_text())
        except yaml.YAMLError as e:
            err(path.name, f"YAML does not parse: {e}")
            continue
        lid = doc.get("line")
        if lid not in lines:
            err(path.name, f"unknown line {lid!r}")
            continue
        if path.stem != lid:
            err(path.name, f"file should be named {lid}.yaml")
        for sp in doc.get("species") or []:
            d = sp.get("dex")
            if d in entries:
                err(path.name, f"#{d} is written twice")
            entries[d] = (lid, sp)

    # Names are checked across every file, even when only some lines are selected.
    seen_names = collections.defaultdict(list)
    for d, (lid, sp) in entries.items():
        if sp.get("name"):
            seen_names[sp["name"].lower()].append(d)

    for d in sorted(entries):
        lid, sp = entries[d]
        if wanted and lid not in wanted:
            continue
        line = lines[lid]
        where = f"#{d:03d} {sp.get('name') or sp.get('concept')}"
        p = by_dex.get(d)
        if not p or p["line"] != lid:
            err(where, f"plan has no #{d} in line {lid}")
            continue
        idx = p["index"]
        prev = by_dex.get(pre_of[d]) if d in pre_of else None

        # identity
        if sp.get("concept") != p["concept"]:
            err(where, f"concept should be {p['concept']!r}")
        if sp.get("types") != p["types"]:
            err(where, f"types {sp.get('types')} differ from the plan's {p['types']}")
        for key in ("etymology", "myth", "expression", "art", "shiny", "habitat", "signature"):
            if not str(sp.get(key) or "").strip():
                err(where, f"missing {key}")

        # name
        name = sp.get("name") or ""
        if not re.fullmatch(r"[A-Z][a-z]+", name):
            err(where, f"name {name!r} must be one capitalized word of letters")
        if len(name) > NAME_MAX:
            err(where, f"name is {len(name)} characters; the engine allows {NAME_MAX}")
        elif len(name) > NAME_AIM:
            warn(where, f"name is {len(name)} characters; aim for {NAME_AIM}")
        if len(seen_names[name.lower()]) > 1:
            err(where, f"name {name} is also used by #{', #'.join(str(x) for x in seen_names[name.lower()] if x != d)}")
        lname = name.lower()
        for ex in existing:
            if ex.lower() == lname:
                err(where, f"{name} is an existing Pokémon")
            elif abs(len(ex) - len(name)) <= 2 and len(name) >= 5 and distance(ex, name) <= 2:
                warn(where, f"{name} is close to the existing Pokémon {ex}")
        for fan in FAN_NAMES:
            if distance(fan, name) <= 2:
                warn(where, f"{name} is close to the fan-made {fan}")
        for od, (_, osp) in entries.items():
            other = osp.get("name") or ""
            if od != d and other and other.lower() != lname and len(name) >= 5 and distance(other, name) <= 2:
                warn(where, f"{name} is close to #{od:03d} {other} in this dex")
        for root in FORBIDDEN_ROOTS:
            if root in lname:
                err(where, f"{name} uses the avoided root {root!r}")
        for c in CAST:
            if lname == c or (len(c) >= 5 and lname.startswith(c)):
                err(where, f"{name} reuses the cast or myth name {c.title()}")

        # category
        cat = sp.get("category") or ""
        if not cat or len(cat) > CATEGORY_MAX or not re.fullmatch(r"[A-Za-z][A-Za-z \-]*", cat):
            err(where, f"category {cat!r} must be 1-{CATEGORY_MAX} letters, spaces or hyphens")

        # abilities
        abil = sp.get("abilities") or []
        hidden = sp.get("hidden_ability")
        if not 1 <= len(abil) <= 2:
            err(where, "needs 1 or 2 regular abilities")
        for a in abil + ([hidden] if hidden else []):
            if a.lower() not in abil_lc:
                err(where, f"ability {a!r} is not in the expansion")
            elif a not in abilities:
                err(where, f"ability {a!r} should be written {abil_lc[a.lower()]!r}")
        if hidden and hidden in abil:
            err(where, "hidden ability repeats a regular one")
        if len(set(abil)) != len(abil):
            err(where, "regular abilities repeat")

        # stats
        bs = sp.get("base_stats") or {}
        if sorted(bs) != sorted(STATS) or not all(isinstance(bs[k], int) and 1 <= bs[k] <= 255 for k in bs):
            err(where, f"base_stats needs integer {', '.join(STATS)} in 1-255")
            bst = 0
        else:
            bst = sum(bs.values())
            key = band_key(line, idx)
            band = BANDS[key]
            stage = 0 if line.get("group") else min(idx, len(band) - 1)
            if key == "two" and any(isinstance(m.get("evo"), list) for m in line["members"]):
                stage = 0 if idx == 0 else 1
            lo, hi = band[stage]
            if not lo <= bst <= hi:
                err(where, f"BST {bst} is outside the {key} band {lo}-{hi} for this stage")
        sp["_bst"] = bst

        ev = sp.get("ev_yield") or {}
        if not ev or not set(ev) <= set(STATS) or not all(isinstance(v, int) and v > 0 for v in ev.values()):
            err(where, "ev_yield needs positive integers on stat keys")
            ev_total = 0
        else:
            ev_total = sum(ev.values())
            if not 1 <= ev_total <= 3:
                err(where, f"EV yield totals {ev_total}; it must be 1-3")
        sp["_ev"] = ev_total

        for key, lo, hi in (("exp_yield", 20, 400), ("catch_rate", 3, 255), ("egg_cycles", 5, 120)):
            v = sp.get(key)
            if not isinstance(v, int) or not lo <= v <= hi:
                err(where, f"{key} must be an integer {lo}-{hi}")
        fr = sp.get("base_friendship", 50)
        if not isinstance(fr, int) or not 0 <= fr <= 255:
            err(where, "base_friendship must be 0-255")
        g = sp.get("gender") or {}
        if g.get("genderless") is True:
            pass
        elif g.get("female_pct") not in FEMALE_PCTS:
            err(where, f"gender needs female_pct in {sorted(FEMALE_PCTS)} or genderless: true")
        eg = sp.get("egg_groups") or []
        if not 1 <= len(eg) <= 2 or any(e not in EGG_GROUPS for e in eg):
            err(where, f"egg_groups {eg} must be 1-2 of {sorted(EGG_GROUPS)}")
        if ("Undiscovered" in eg) and len(eg) > 1:
            err(where, "Undiscovered can't share with another egg group")
        roles = set(line["roles"])
        if (p["baby"] or roles & {"legendary trio", "box legendary", "legendary", "mythical"}) and eg != ["Undiscovered"]:
            err(where, "babies, legendaries and mythicals use the Undiscovered egg group")
        if sp.get("growth_rate") not in GROWTH:
            err(where, f"growth_rate must be one of {sorted(GROWTH)}")
        for key in ("height_m", "weight_kg"):
            v = sp.get(key)
            if not isinstance(v, (int, float)) or v <= 0:
                err(where, f"{key} must be positive")

        # evolution consistency with the previous stage
        if prev and prev["dex"] in entries:
            _, psp = entries[prev["dex"]]
            if "_bst" in psp and psp["_bst"] and bst and bst <= psp["_bst"]:
                err(where, f"BST {bst} doesn't rise from #{prev['dex']}'s {psp['_bst']}")
            if psp.get("_ev") and ev_total and ev_total < psp["_ev"]:
                err(where, "EV yield falls from the previous stage")
            if psp.get("growth_rate") != sp.get("growth_rate"):
                err(where, "growth_rate differs from the previous stage")

        # Pokédex text
        dex = sp.get("dex_entry") or []
        if not isinstance(dex, list) or not 3 <= len(dex) <= 4:
            err(where, "dex_entry must be a list of 3-4 lines")
        else:
            for i, t in enumerate(dex, 1):
                if len(t) > DEX_LINE_MAX:
                    err(where, f"dex line {i} is {len(t)} characters (max {DEX_LINE_MAX})")
                if not DEX_CHARS.match(t):
                    bad = sorted(set(ch for ch in t if not DEX_CHARS.match(ch)))
                    err(where, f"dex line {i} uses characters the Gen 3 charmap lacks: {''.join(bad)!r}")

        # moves
        ls = sp.get("learnset") or {}
        lvl = ls.get("level_up") or []
        teach = ls.get("teachable") or []
        egg = ls.get("egg") or []
        last = -1
        names_lv = []
        for entry in lvl:
            if not (isinstance(entry, list) and len(entry) == 2 and isinstance(entry[0], int)):
                err(where, f"level_up entry {entry!r} must be [level, move]")
                continue
            lv, mv = entry
            if not 0 <= lv <= 100:
                err(where, f"level {lv} out of range")
            if lv < last:
                err(where, f"level_up is out of order at {mv} (level {lv})")
            last = lv
            names_lv.append(mv)
        for kind, lst in (("level_up", names_lv), ("teachable", teach), ("egg", egg)):
            for mv in lst:
                if not isinstance(mv, str) or mv.lower() not in move_lc:
                    err(where, f"{kind} move {mv!r} is not in the expansion")
                elif mv not in moves:
                    err(where, f"{kind} move {mv!r} should be written {move_lc[mv.lower()]!r}")
            dupes = [m for m, n in collections.Counter(lst).items() if n > 1]
            if dupes and kind != "level_up":
                err(where, f"{kind} repeats {', '.join(dupes)}")
        first_stage = idx == 0 or line.get("group") or p["baby"]
        limited = "Magikarp role" in roles and idx == 0      # the fry is meant to know almost nothing
        breeds = eg != ["Undiscovered"]
        want_lv = (10, 26) if first_stage and len(line["members"]) > 1 else (14, 26)
        if not limited and not want_lv[0] <= len(lvl) <= want_lv[1]:
            warn(where, f"{len(lvl)} level-up moves; aim for {want_lv[0]}-{want_lv[1]}")
        if not lvl or lvl[0][0] > 1:
            err(where, "level_up must start with a level 0 or level 1 move")
        if idx > 0 and not line.get("group") and not any(e[0] == 0 for e in lvl if isinstance(e, list)):
            warn(where, "no evolution move (level 0)")
        if len(teach) < 20 and not limited:
            warn(where, f"only {len(teach)} teachable moves")
        if first_stage and breeds and not (4 <= len(egg) <= 10) and (len(line["members"]) > 1 or egg):
            warn(where, f"{len(egg)} egg moves; aim for 4-10 on a first stage")
        if not first_stage and egg:
            err(where, "egg moves belong on the first stage only")
        if prev and prev["dex"] in entries:
            ptea = set((entries[prev["dex"]][1].get("learnset") or {}).get("teachable") or [])
            missing = ptea - set(teach)
            if missing:
                warn(where, f"drops teachable moves its pre-evolution has: {', '.join(sorted(missing))}")
        if not isinstance(sp.get("new_move", None), (type(None), dict)):
            err(where, "new_move must be null or a mapping")

    # coverage
    total_written = len(entries)
    if args.complete and total_written != planlib.TARGET_TOTAL:
        missing = sorted(set(by_dex) - set(entries))
        errors.append(f"dex: {total_written} of {planlib.TARGET_TOTAL} entries written; missing #{', #'.join(map(str, missing))}")

    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("error:", e)
    shown = [d for d in entries if not wanted or entries[d][0] in wanted]
    print(f"{len(shown)} entries checked, {len(errors)} errors, {len(warnings)} warnings "
          f"({total_written} of {planlib.TARGET_TOTAL} written)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
