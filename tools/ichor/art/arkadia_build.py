#!/usr/bin/env python3
"""Draw, compile and catalog Arkadia's two secondaries.

  gTileset_Arkadia      the town (arkadia_town.py, arkadia_trees.py)
  gTileset_ArkadiaWood  the Cypress Wood and the Pool of Mnemosyne (arkadia_wood.py)

The pipeline is kithairon_build.py's, reused function for function, with
Arkadia's palette groups as Porytiles' packing hints:
1. Paint every structure, check each 8x8 tile draws from one group of its set,
   merge tiles within 2 px of each other.
2. The soft sets (canopy, rock) hold only the blob shapes the maps use:
   tools/ichor/maps/arkadia_plan.py lists them, so redraw after changing a plan.
3. Pack, write data/tilesets/secondary/<dir>/porytiles_src, compile in a scratch
   project, point every borrowed-ground cell at aethos's grass, verify, and fail
   past 504 tiles (door animations own 504-511).
4. Write build/arkadia/<dir>/catalog.json, the lamp metatile labels the dusk
   scene swaps, the sheets and design/phase3/TILES_arkadia.md (keeping its
   hand-written passes section).

Usage: /usr/bin/python3 tools/ichor/art/arkadia_build.py [--no-compile] [--only arkadia,arkadia_wood]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "maps"))
import arkadia_lib as L  # noqa: E402
import arkadia_plan  # noqa: E402
import arkadia_town  # noqa: E402
import arkadia_wood  # noqa: E402
import kithairon_build as KB  # noqa: E402

ROOT = L.ROOT
OUT = ROOT / "build/arkadia"
IMG = ROOT / "design/phase3/img"
DOC = ROOT / "design/phase3/TILES_arkadia.md"
PASSES_MARK = "<!-- passes: hand-written below this line; arkadia_build.py keeps it -->"
NEAR = 2

SETS = {
    "arkadia": {"symbol": "gTileset_Arkadia", "dir": "arkadia", "label": "Arkadia",
                "title": "Arkadia, the hunters' town", "groups": L.TOWN_GROUPS,
                "rgb": L.TOWN_RGB},
    "arkadia_wood": {"symbol": "gTileset_ArkadiaWood", "dir": "arkadia_wood",
                     "label": "ArkadiaWood", "title": "the Cypress Wood and the Pool of Mnemosyne",
                     "groups": L.WOOD_GROUPS, "rgb": L.WOOD_RGB},
}

# metatiles scripts swap: (set, structure, cell name, label)
LABELS = [
    ("arkadia", "lamptree", "ml", "LampUnlit_L"),
    ("arkadia", "lamptree", "mr", "LampUnlit_R"),
    ("arkadia", "lamps_lit", "L", "LampLit_L"),
    ("arkadia", "lamps_lit", "R", "LampLit_R"),
]

SECTION_TITLES = {
    "trees": "Cypresses, the lamp-trees and the canopy",
    "town": "Rock, terraces, houses and the town's buildings",
    "wood": "The Cypress Wood",
    "glade": "The Pool of Mnemosyne's glade",
}


def hints(groups):
    lines = ["  palettes:", "    packing:", "      hints_enabled: true", "      hints:"]
    for g, names in groups.items():
        lines.append(f"        - name: {g}")
        lines.append("          colors:")
        for n in names:
            r, gg, b = L.C[n]
            lines.append(f"            - [{r}, {gg}, {b}]")
    return "\n".join(lines) + "\n"


def painted(shapes):
    town = arkadia_town.build(shapes)
    wood = arkadia_wood.build(shapes)
    for ss in (town, wood):
        keys = [s.key for s in ss]
        dup = {k for k in keys if keys.count(k) > 1}
        assert not dup, dup
    return {"arkadia": town, "arkadia_wood": wood}


def sections(structs):
    order = []
    by = {}
    for s in structs:
        if s.section not in by:
            order.append(s.section)
            by[s.section] = []
        by[s.section].append(s)
    return [(sec, by[sec]) for sec in order]


def catalog(name, secs, ids):
    data = []
    for sec, structs in secs:
        for s in structs:
            data.append({
                "key": s.key, "title": s.title, "section": sec, "w": s.w, "h": s.h,
                "ids": ids[s.key], "walk": s.walk, "notes": s.notes,
                "names": {k: list(v) for k, v in s.names.items()},
                "behaviors": {f"{x},{y}": mb for (x, y), mb in s.behaviors.items() if mb},
                "ground": {f"{x},{y}": g for (x, y), g in getattr(s, "ground", {}).items()},
            })
    d = OUT / SETS[name]["dir"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "catalog.json").write_text(json.dumps({"symbol": SETS[name]["symbol"], "structures": data},
                                               indent=1))
    return data


LABEL_FILE = ROOT / "include/constants/metatile_labels.h"
LABEL_START = "// gTileset_Arkadia, gTileset_ArkadiaWood (Ichor: Arkadia), written by tools/ichor/art/arkadia_build.py"
LABEL_END = "// end gTileset_Arkadia"


def write_labels(all_ids):
    lines = [LABEL_START]
    for setname, key, cell, label in LABELS:
        ids, structs = all_ids[setname]
        s = next(x for x in structs if x.key == key)
        cx, cy = s.names[cell]
        lines.append(f"#define METATILE_{SETS[setname]['label']}_{label:<20} 0x{ids[key][cy][cx]:03X}")
    lines.append(LABEL_END)
    block = "\n".join(lines) + "\n"
    text = LABEL_FILE.read_text()
    if LABEL_START in text:
        a = text.index(LABEL_START)
        b = text.index(LABEL_END, a) + len(LABEL_END) + 1
        text = text[:a] + block + text[b:]
    else:
        end = text.rindex("#endif")
        text = text[:end] + block + "\n" + text[end:]
    LABEL_FILE.write_text(text)


def structure_md(s):
    out = [f"### {s['title']}\n", f"`{s['key']}`, {s['w']} wide by {s['h']} tall. {s['notes']}\n"]
    rows = [" ".join(f"0x{v:03X}" for v in r) for r in s["ids"]]
    out.append("```text")
    out.append("ids".ljust(len(rows[0])) + "   walk")
    for r, w in zip(rows, s["walk"]):
        out.append(r + "   " + " ".join(w))
    out.append("```\n")
    if s["names"] and not all(k.startswith("1|") for k in s["names"]):
        out.append("Parts: " + ", ".join(f"`{n}` 0x{s['ids'][y][x]:03X}" for n, (x, y) in s["names"].items())
                   + ".\n")
    return out


INTRO = """\
# Arkadia tileset catalog

Arkadia is a town in a forest, on a long slope among cypresses so tall the houses look like
toys between their trunks (SCRIPT.md Part 2). Two secondaries, both on the `aethos` primary:

- `gTileset_Arkadia` ({town_tiles} of 504 tiles): the town's cypresses in four shapes, the
  lamp-trees unlit and lit, the canopy at the town's edges, the grey rock (Kithairon's, so
  the climb from Route 12 matches) with its tall faces, terrace walls, the timber-and-stone
  house kit under weathered shingles, the Asclepeion against its outcrop, the Agora's stall
  round the great cypress, Hippothoos's hut and kiln, Krotos's byre and fence, the old
  racecourse, Iamos's wall, Pan's grotto, the temple stair, the Temple of Artemis and its
  precinct gate, and the Cypress Wood's gate.
- `gTileset_ArkadiaWood` ({wood_tiles} of 504 tiles): the Wood's floor in deep shade, its
  ferns (the tall grass), the canopy, the great trunks, the starlit clearing and its stump,
  the Tomb of Kallisto, Agapenor's kiln, and the Pool's glade: the canopy over grass, the
  black pool and its fixed stars, white poplars, asphodel (the glade's tall grass), the seat.

**This file is generated** above the passes section by `tools/ichor/art/arkadia_build.py`.
The art is in `arkadia_lib.py` (colors, groups, the cypress and canopy painters),
`arkadia_trees.py`, `arkadia_town.py` and `arkadia_wood.py`. The maps are built by
`tools/ichor/maps/arkadia.py` from the plans in `tools/ichor/maps/arkadia_plan.py`; the
soft sets hold only the outlines those plans use, so rebuild the tiles after changing one.

The sheets are [img/tiles_arkadia_sheet.png](img/tiles_arkadia_sheet.png) and
[img/tiles_arkadia_wood_sheet.png](img/tiles_arkadia_wood_sheet.png); every piece on its ground
is [img/arkadia_pieces.png](img/arkadia_pieces.png) and
[img/arkadia_wood_pieces.png](img/arkadia_wood_pieces.png).

**Why two sets.** One set's 504 tiles can't hold a town, a dark forest and a sacred pool. The
Wood is entered by a gate warp, so no seam joins the two; the Wood and the Pool share theirs, so
their seam needs no aethos-only strip.

**Collision.** `X` blocks, `.` walks, `T` walks and draws over the player, `G` tall grass
(`MB_TALL_GRASS`), `J` a ledge (`MB_JUMP_SOUTH`), `D` a door (`MB_NON_ANIMATED_DOOR`).

**Ground.** Pieces marked on grass leave their bottom layer to aethos's grass (`0x001`); the build
points it there, so rebuild after aethos is repainted.

**Palettes.** Every 8x8 tile draws from one group of its set:

| Set | Group | Use |
|---|---|---|
| Arkadia | tree | the cypresses, the canopy, the lamps and their glow, on grass |
| Arkadia | house | stone footings, dark timber, weathered shingles, daub, a lit window, a red door |
| Arkadia | rock | Kithairon's grey rock, moss, a cave's dark, a glint, the spring |
| Arkadia | sacred | the temple: marble, silver, the roof's terracotta, the night-blue frieze |
| Arkadia | town | the racecourse's earth, the awning, nets, fences, the kiln and its smoke |
| ArkadiaWood | forest | the floor in deep shade, the canopy, ferns, bark, starlight, embers |
| ArkadiaWood | tomb | the mound's earth and stones, the little shrine |
| ArkadiaWood | canopy | the canopy over grass, round the Pool |
| ArkadiaWood | glade | white poplars, asphodel, the seat |
| ArkadiaWood | pool | the black water, its stars, the kerb |
"""


def write_doc(used):
    datas = {n: json.loads((OUT / SETS[n]["dir"] / "catalog.json").read_text())["structures"]
             for n in SETS}
    out = [INTRO.format(town_tiles=used.get("arkadia", "?"), wood_tiles=used.get("arkadia_wood", "?"))]
    for n in SETS:
        out.append(f"## {SETS[n]['symbol']}\n")
        cur = None
        for s in datas[n]:
            if s["section"] != cur:
                cur = s["section"]
                out.append(f"### — {SECTION_TITLES.get(cur, cur)} —\n")
            out += structure_md(s)
    passes = ""
    if DOC.exists() and PASSES_MARK in DOC.read_text():
        passes = DOC.read_text().split(PASSES_MARK, 1)[1]
    DOC.write_text("\n".join(out).rstrip() + "\n\n" + PASSES_MARK + (passes or "\n"))
    print(DOC.relative_to(ROOT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--only", help="comma-separated: arkadia,arkadia_wood")
    args = ap.parse_args()
    shapes = arkadia_plan.shapes()
    pieces = painted(shapes)
    wanted = args.only.split(",") if args.only else list(SETS)
    all_ids, used = {}, {}
    IMG.mkdir(parents=True, exist_ok=True)
    for name in wanted:
        info = SETS[name]
        structs = pieces[name]
        validate = L.validate_town if name == "arkadia" else L.validate_wood
        probs = validate(structs)
        for p in probs:
            print("PROBLEM:", p)
        if probs:
            sys.exit(1)
        n0 = len(L.E.tiles_of(structs))
        L.E.merge_near_duplicates(structs, NEAR)
        print(f"{name}: {n0} -> {len(L.E.tiles_of(structs))} tiles before palette sharing")
        probs = validate(structs)
        for p in probs:
            print("PROBLEM:", p)
        if probs:
            sys.exit(1)
        secs = sections(structs)
        ids, rows = KB.pack(secs)
        print(f"{name}: {rows} sheet rows, {rows * 8} metatiles")
        all_ids[name] = (ids, structs)
        KB.write_sources(ROOT / f"data/tilesets/secondary/{info['dir']}/porytiles_src", secs, ids, rows)
        catalog(name, secs, ids)
        L.E.preview(structs, scale=2, cols=5).save(IMG / f"{info['dir']}_pieces.png")
        if args.no_compile:
            continue
        KB.palette_hints = lambda groups=info["groups"]: hints(groups)
        binp = KB.compile_set(info)
        patched = KB.borrow_ground(binp, secs, ids)
        used[name] = KB.verify(binp, rows, patched, name)
        out = IMG / f"tiles_{info['dir']}_sheet.png"
        KB.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet", info["symbol"],
                "--primary", "aethos", "--scale", "2", "-o", str(out)])
        print(out.relative_to(ROOT))
    if "arkadia" in all_ids:
        write_labels(all_ids)
    if not args.no_compile and len(used) == len(SETS):
        write_doc(used)


if __name__ == "__main__":
    main()
