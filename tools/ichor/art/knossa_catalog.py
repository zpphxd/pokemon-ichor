#!/usr/bin/env python3
"""Write design/phase4/TILES_<tileset>.md for the Knossa secondaries from
build/<dir>/catalog.json and the compiled metatile attributes.

knossa_build.py runs this after each build, so the ids, behaviors and layer
types in the documents always match the compiled tilesets.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "design/phase4"
sys.path.insert(0, str(Path(__file__).resolve().parent))

LAYER = {0: "NORMAL", 1: "COVERED", 2: "SPLIT"}

FAMILY = """\
## The Knossa family

LABYRINTH.md §11 planned one `knossa` secondary for Amnisos, the Bull Road and the
palace. Their pieces come to far more than one secondary's 504 tiles (the palace's
frescoes alone would fill half of one), so the art is split by map, as the Kythera
family is. All are built by `tools/ichor/art/knossa_build.py` from shared painters, so a
piece two of them carry (the limestone cliff, the surf, the hives) is drawn once and
looks the same in both. The labyrinth tileset (`TILES_labyrinth.md`) is the Labyrinth's
own and is not part of this family, but the palace's Minoan red, ochre, gypsum and fresco
blue are its colors exactly, so the Grand Staircase meets Ring I in one palette.

| Tileset | Symbol | Primary | Maps | Catalog |
|---|---|---|---|---|
| `amnisos` | `gTileset_Amnisos` | aethos | Amnisos | [`TILES_amnisos.md`](TILES_amnisos.md) |
| `bull_road` | `gTileset_BullRoad` | aethos | the Bull Road, the vineyard terraces, the Bronze Heel | [`TILES_bull_road.md`](TILES_bull_road.md) |
| `palace_minos` | `gTileset_PalaceMinos` | aethos | the Palace of Minos above ground | [`TILES_palace_minos.md`](TILES_palace_minos.md) |
| `palace_rooms` | `gTileset_PalaceRooms` | oikos (any) | the Throne Room, the West Magazines, the Queen's Megaron, the Grand Staircase | [`TILES_palace_rooms.md`](TILES_palace_rooms.md) |
| `ida` | `gTileset_Ida` | aethos | the Ida path, the cradle shrine, the Idaean Cave, the Cave of Eileithyia | [`TILES_ida.md`](TILES_ida.md) |

**Seams between them** (MAP_DESIGN §5). With the split, the seam rule applies wherever
neighbours use different secondaries:

{seams}
Gates, lanes and the sea are aethos's anyway, so the strips cost little: plant aethos
olives, cypresses, grass, path and ledges there.
"""

CONVENTIONS = """\
## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet ({starts}). Structures are placed first-fit in build
order, so appending a new one never moves an old one. Map builders should place pieces
by key and name, never by raw id: `tools/ichor/maps/knossa_tiles.py` holds every Knossa
catalog as a Python dict (`mid('{name}', '{example}', ...)`, `place(...)`, `front(...)`),
and `build/{dir}/catalog.json` is the same as JSON.

**Walk codes** (the grid beside each structure, and the cell tables):

| Code | Meaning |
|---|---|
| `X` | Impassable: set collision 1. |
| `.` | Passable. |
| `T` | Passable, drawn over the player, who walks behind it. |
| `G` | Tall grass: `MB_TALL_GRASS`, wild encounters. Passable. |
| `D` | Door: `MB_NON_ANIMATED_DOOR`. Put the warp here. |
| `W` | Sea: `MB_OCEAN_WATER`, surfable (collision 0). |
| `P` | Fresh water: `MB_POND_WATER`, surfable. |
| `J` | Ledge: `MB_JUMP_SOUTH`. |
| `S` | Sand: `MB_SAND`. |

{ground}
**Animations.** {anims}

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player),
`COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of these color
groups, one per secondary palette (`knossa_lib.GROUPS`), passed to Porytiles as packing
hints:

| Group | Use |
|---|---|
{groups}

**Tile budget.** {used} of 504 tiles ({meta} metatiles). The door animations copy their
frames into tiles 504-511 (`DOOR_TILE_START_SIZE1`, `src/field_door.c`), so the build
fails past 504. Static tiles within two pixels of one another are merged.
{labels}"""

GROUND = """**Borrowed ground.** Cells marked *grass*, *path*, *sand*, *sea* or *shallow* draw no
ground of their own: after Porytiles compiles, the build points their bottom-layer tiles
at aethos's grass (`0x001`), limestone path (`0x1D9`), sand (`0x124`), animated sea
(`0x170`) or animated turquoise shallows (`0x0D1`). They meet aethos ground exactly and
cost no tiles. Rebuild whenever aethos is repainted; the build checks every borrowed
entry. A borrowed cell's own art is in one layer: the middle (`COVERED`, under the
player) or the top (`SPLIT`, over the player).
"""

GROUND_SELF = """**Its own ground.** It borrows nothing: every bottom layer is opaque and every tile
is its own, so it works on any primary (it is drawn for `oikos`, as the labyrinth is).
"""

GROUP_USE = {
    "minoan": "Minoan red, ochre, gypsum, black and terracotta (labyrinth_art's): red columns, "
              "black capitals, horns of consecration, labrys marks, pithoi, the houses, the hives",
    "fresco": "Fresco blue, white, saffron and skin (labyrinth_art's): dolphins, lilies, "
              "bull-leapers, the lily prince, saffron gatherers, blue monkeys, griffins",
    "stone": "Cretan limestone on aethos grass: cliffs, terrace and town walls, the goat path",
    "foam": "Kythera's surf, foam lace, wet rock and quay edges",
    "green": "Vines and grapes, holm oak, phrygana and thyme, on aethos grass",
    "bronze": "Bronze and verdigris (Talos's foot, the Kouretes' shields, door fittings), and "
              "the marble herm",
    "terra": "Kythera's timber and terracotta: boats, the triremes, nets, trellis posts",
    "cave": "The caves' dark limestone, the worn floor, the polished birth-stone",
    "titan": "Titan slate and gold, timber and canvas: the West Magazines' camp",
}

ANIM_TEXT = {
    "surf": "`surf`: the foam on the shore and round rocks, washing up and back (3 frames, "
            "ping-pong; Kythera's)",
    "bees": "`bees`: bees flying at the hives' mouths (3 frames)",
}


def grid(ids, walk):
    lines = []
    for row, wr in zip(ids, walk):
        cells = " ".join(f"0x{i:03X}" if i is not None else "  -  " for i in row)
        lines.append(f"{cells}   {' '.join(wr)}")
    head = "ids".ljust(len(lines[0]) - len(walk[0]) * 2 + 1) + "   walk"
    return "```text\n" + head + "\n" + "\n".join(lines) + "\n```"


def cell_table(s, attrs):
    names = {}
    for n, (x, y) in s["names"].items():
        names.setdefault((x, y), []).append(n)
    rows = ["| Id | Piece | Walk | Behavior | Layer | Ground |", "|---|---|---|---|---|---|"]
    for y in range(s["h"]):
        for x in range(s["w"]):
            i = s["ids"][y][x]
            a = int(attrs[i - 0x200]) if attrs is not None else 0
            beh = s["behaviors"].get(f"{x},{y}", "MB_NORMAL")
            nm = ", ".join(f"`{n}`" for n in names.get((x, y), [])) or f"({x}, {y})"
            gr = s["ground"].get(f"{x},{y}", "")
            rows.append(f"| 0x{i:03X} | {nm} | `{s['walk'][y][x]}` | `{beh}` | "
                        f"{LAYER.get(a >> 12, a >> 12)} | {gr} |")
    return "\n".join(rows)


SECTION_TITLES = {
    "harbor": "The harbor", "town": "Town", "coast": "The coast", "land": "The land",
    "road": "The Bull Road", "vineyard": "The vineyard", "heel": "The Bronze Heel",
    "court": "The court", "walls": "Walls and columns", "fresco": "Frescoes and reliefs",
    "rooms": "The rooms", "cave": "The caves", "ida": "Mount Ida",
}


def main(name, sp, used, meta):
    import knossa_specs
    d = sp["dir"]
    cat = json.loads((ROOT / f"build/{d}/catalog.json").read_text())
    attrs_p = ROOT / f"data/tilesets/secondary/{d}/porytiles_bin/metatile_attributes.bin"
    attrs = np.fromfile(attrs_p, "<u2") if attrs_p.exists() else None
    structs = cat["structures"]
    starts = ", ".join(f"{n} at 0x{0x200 + r * 8:03X}" for n, r in sp["rows"].items())
    anim_names = sorted({a for s in structs for a in s["anims"]})
    sfx = sp["symbol"].replace("gTileset_", "")
    anims = ("Porytiles animations in this tileset, driven by "
             f"`InitTilesetAnim_PorytilesManaged_{sfx}` "
             f"(`include/porytiles_generated/tilesets/{d}/generated_anim_code.h`): "
             + "; ".join(ANIM_TEXT.get(a, f"`{a}`") for a in anim_names) + ". Every 8x8 tile "
             "that changes between frames is an animated tile; frame 0 is the key drawn in "
             "the sheet." + (" The sea and shallows under them are aethos's own animations."
                             if sp.get("primary", "aethos") == "aethos" else "")
             ) if anim_names else "None of its own" + (
                 "; the borrowed sea and shallows animate." if sp.get("primary", "aethos") == "aethos"
                 else ".")
    labels = ""
    want = sp.get("labels", [])
    if want:
        items = ", ".join(f"`METATILE_{sp['label']}_{lab}`" for _, its in want for _, lab in its)
        labels = ("\n**Scripted swaps.** The build writes the ids scripts swap to the "
                  f"`{sp['symbol']}` block at the end of `include/constants/metatile_labels.h`: "
                  f"{items}.\n")
    groups = "\n".join(f"| {g} | {GROUP_USE.get(g, g)} |" for g in sp["groups"])
    first = structs[0]
    example = f"{first['key']}', '{sorted(first['names'])[0]}" if first["names"] else first["key"]
    out = []
    out.append(f"# {name} tileset catalog\n")
    prim = sp.get("primary", "aethos")
    out.append(f"`{sp['symbol']}` is {sp['title']} (Act III, Knossa; LABYRINTH.md §2-§3, §11; "
               f"SCRIPT.md Part 10). It serves {sp['maps']}. Pair it with the `{prim}` primary"
               + (", which supplies the open grass, paths, sand, sea, olives, cypresses, "
                  "ledges and the Asclepeion and Agora fronts.\n" if prim == "aethos" else ".\n"))
    out.append("**This file is generated.** `tools/ichor/art/knossa_build.py " + name + "` paints "
               "the tileset, compiles it, registers it and rewrites this catalog. The art is in "
               "`tools/ichor/art/knossa_*.py`, the palette plan in `knossa_lib.py`, what each "
               "tileset holds in `knossa_specs.py`; `knossa_scene.py` renders the mock scenes.\n")
    imgs = ["| Image | Shows |", "|---|---|"]
    for f, what in sp.get("images", []):
        imgs.append(f"| [`img/{f}`](img/{f}) | {what} |")
    imgs.append(f"| [`img/{d}_pieces.png`](img/{d}_pieces.png) | Every structure on its ground |")
    imgs.append(f"| [`img/{d}_sheet.png`](img/{d}_sheet.png) | The numbered metatile sheet, "
                "rendered from the compiled tileset |")
    out.append("\n".join(imgs) + "\n")
    if sp.get("images"):
        f0 = sp["images"][0][0]
        out.append(f"![{sp['images'][0][1]}](img/{f0})\n")
    if name == "amnisos":
        out.append(FAMILY.format(seams=knossa_specs.SEAMS))
    else:
        out.append("It is one of the Knossa family of secondaries; see "
                   "[`TILES_amnisos.md`](TILES_amnisos.md) for why the art is split and which "
                   "seams then need aethos-only strips.\n")
    if sp.get("intro"):
        out.append(sp["intro"] + "\n")
    out.append(CONVENTIONS.format(starts=starts, name=name, dir=d, anims=anims, used=used,
                                  meta=meta, labels=labels, groups=groups, example=example,
                                  ground=GROUND if prim == "aethos" else GROUND_SELF))
    for sec, _ in sp["sections"]:
        out.append(f"## {SECTION_TITLES.get(sec, sec.title())}\n")
        for s in structs:
            if s["section"] != sec:
                continue
            out.append(f"### {s['title']}\n")
            out.append(f"`{s['key']}`, {s['w']} wide by {s['h']} tall. {s['notes']}\n")
            out.append(grid(s["ids"], s["walk"]) + "\n")
            out.append(cell_table(s, attrs) + "\n")
        fr = [(k, f) for k, f in cat.get("fronts", {}).items()
              if any(st["key"] == f["kit"] and st["section"] == sec for st in structs)]
        if fr:
            out.append("### House fronts\n")
            out.append("Every house is a home (MAP_DESIGN.md §2), so each front has a door. These "
                       "are arrangements of the kit's parts and cost no metatiles of their own; "
                       "mix the parts for more (`knossa_tiles.front()`). Walk: every house cell "
                       "is `X` except its door (`D`) and a ladder or stair.\n")
            for k, f in fr:
                walk = [["D" if r and r.startswith("door") else
                         ("." if r and ("ladder" in r or "steps" in r) else "X")
                         for r in row] for row in f["rows"]]
                out.append(f"**{f['title']}** (`{k}`): {f['who']}.\n")
                out.append(grid(f["ids"], ["".join(w) for w in walk]) + "\n")
    doc = DOCS / sp["doc"]
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("\n".join(out))
    print(doc.relative_to(ROOT))


if __name__ == "__main__":
    import knossa_build as B
    for n in sys.argv[1:] or ["amnisos"]:
        main(n, B.spec(n), "?", "?")
