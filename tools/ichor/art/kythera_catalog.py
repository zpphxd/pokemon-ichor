#!/usr/bin/env python3
"""Write design/phase4/TILES_<tileset>.md for the Kythera-family secondaries
from build/<dir>/catalog.json and the compiled metatile attributes.

kythera_build.py runs this after each build, so the ids, behaviors and layer
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
## The Kythera family

Kythera Isle and Melos need far more distinct pieces than one secondary's 504
tiles hold (the coast and harbor alone came to over 600), so the art is split
by map, the way Emerald gives each town its own secondary. Every one pairs with
the `aethos` primary and is built by `tools/ichor/art/kythera_build.py` from
shared painters, so a piece two of them carry (the surf, myrtle, the house kit)
is drawn once and looks the same in both.

| Tileset | Symbol | Maps | Catalog |
|---|---|---|---|
| `kythera` | `gTileset_Kythera` | the Foam Road, the Spring of Kallirhoe | [`TILES_kythera.md`](TILES_kythera.md) |
| `skandeia` | `gTileset_Skandeia` | Skandeia | [`TILES_skandeia.md`](TILES_skandeia.md) |
| `paphia` | `gTileset_Paphia` | Paphia | [`TILES_paphia.md`](TILES_paphia.md) |
| `neraida` | `gTileset_Neraida` | the Neraida falls | [`TILES_neraida.md`](TILES_neraida.md) |
| `melos` | `gTileset_Melos` | Melos; Routes 22 and 23 and Antikythera; Echo's sea caves | [`TILES_melos.md`](TILES_melos.md) |
| `temple_aphrodite` | `gTileset_TempleAphrodite` | the Temple of Aphrodite (Galatea's Gallery), on the `oikos` interior primary | [`TILES_temple_aphrodite.md`](TILES_temple_aphrodite.md) |

**Seams between them.** SCRIPT.md Part 2 assumed one `kythera` for every Kythera
map, which would have made their shared seams exempt from MAP_DESIGN §5. With the
split, the seam rule applies where neighbours use different secondaries:

| Seam | Tilesets | Rule |
|---|---|---|
| Skandeia's west gate ↔ the Foam Road's east end | skandeia / kythera | the 8 columns nearest the seam, on both maps, use only `aethos` |
| the Foam Road's west end ↔ Paphia's east gate | kythera / paphia | 8 columns, both maps |
| Paphia's north edge ↔ the Neraida falls | paphia / neraida | 6 rows, both maps |
| the Foam Road's stair ↔ the spring | kythera / kythera | exempt |
| the sea maps of Routes 22 and 23 ↔ Melos, Skandeia, Kaldera | sea | aethos sea only, as before |

Gates, lanes and sea are aethos's anyway, so the strips cost little: plant aethos
olives, cypresses, grass and path there.
"""

CONVENTIONS = """\
## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet ({starts}). Structures are placed first-fit in build
order, so appending a new one never moves an old one. Map builders should place pieces
by key and name, never by raw id: `tools/ichor/maps/kythera_tiles.py` holds every
Kythera-family catalog as a Python dict (`mid('{name}', 'surf', 'S')`), and
`build/{dir}/catalog.json` is the same as JSON.

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
| `F` | Waterfall: `MB_WATERFALL` (the Horn of Achelous climbs it). |
| `J` | Ledge: `MB_JUMP_SOUTH`. |

**Borrowed ground.** Cells marked *grass*, *path*, *sand*, *sea*, *shallow* or *fall*
draw no ground of their own: after Porytiles compiles, the build points their
bottom-layer tiles at aethos's grass (`0x001`), limestone path (`0x1D9`), sand
(`0x124`), animated sea (`0x170`), animated turquoise shallows (`0x0D1`) or animated
waterfall (`0x0B3`). They meet aethos ground exactly and cost no tiles. Rebuild
whenever aethos is repainted; the build checks every borrowed entry. A borrowed cell's
own art is in one layer: the middle (`COVERED`, under the player) or the top (`SPLIT`,
over the player).

**Animations.** {anims}

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player),
`COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of seven color
groups, one per secondary palette (`kythera_lib.GROUPS`), passed to Porytiles as packing
hints.

| Group | Use |
|---|---|
| foam | The surf, foam lace, shingle, white rock, Aphrodite's rock, reefs, quays, pumice |
| rose | Pink stone and rose marble: sea-cliffs, the quarry, temple and stair, kerbs, moss |
| green | Myrtle, sea-grass and thrift, roses, narcissus, plane, oleander, apple |
| cyc | Whitewashed houses, Aegean doors, rose-pink frames, pots, dovecotes, sea doors |
| terra | Timber and terracotta: boats, the trireme, slips, mill wheels, bridges, gear |
| bronze | Bronze mirrors, the harbor shrine's dove, the great herm, the Minoan vault door |
| melos | Melos's obsidian slope on its earth and grass |

**Tile budget.** {used} of 504 tiles ({meta} metatiles). The door animations copy their
frames into tiles 504-511 (`DOOR_TILE_START_SIZE1`, `src/field_door.c`), so the build
fails past 504. Static tiles within two pixels of one another are merged.
{labels}"""


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
    "coast": "The coast", "land": "The land", "water": "Fresh water", "town": "Town",
    "harbor": "The harbor", "melos": "Melos", "sea": "The open sea", "cave": "Echo's sea caves",
}


def main(name, sp, used, meta):
    d = sp["dir"]
    cat = json.loads((ROOT / f"build/{d}/catalog.json").read_text())
    attrs_p = ROOT / f"data/tilesets/secondary/{d}/porytiles_bin/metatile_attributes.bin"
    attrs = np.fromfile(attrs_p, "<u2") if attrs_p.exists() else None
    structs = cat["structures"]
    starts = ", ".join(f"{n} at 0x{0x200 + r * 8:03X}" for n, r in sp["rows"].items())
    anim_names = sorted({a for s in structs for a in s["anims"]})
    anim_text = {
        "surf": "`surf`: the foam on the shore, round rocks, at a fall's foot and over a weir, "
                "washing up and back (3 frames, ping-pong)",
        "wheel": "`wheel`: the mill's paddle wheel turning (4 frames)",
        "glint": "`glint`: light catching the obsidian now and then (3 frames, mostly still)",
    }
    anims = ("Porytiles animations in this tileset, driven by "
             f"`InitTilesetAnim_PorytilesManaged_{sp['symbol'].replace('gTileset_', '')}` "
             "(`include/porytiles_generated/tilesets/" + d + "/generated_anim_code.h`): "
             + "; ".join(anim_text.get(a, f"`{a}`") for a in anim_names) + ". Every 8x8 tile "
             "that changes between frames is an animated tile; frame 0 is the key drawn in "
             "the sheet. The sea, shallows and waterfall under them are aethos's own animations."
             ) if anim_names else "None of its own; the borrowed sea, shallows and waterfall animate."
    labels = ""
    want = sp.get("labels", [])
    if want:
        items = ", ".join(f"`METATILE_{sp['label']}_{lab}`" for _, its in want for _, lab in its)
        labels = ("\n**Scripted swaps.** The build writes the ids scripts swap to the "
                  f"`{sp['symbol']}` block at the end of `include/constants/metatile_labels.h`: "
                  f"{items}.\n")
    out = []
    title = sp["title"]
    out.append(f"# {name} tileset catalog\n")
    out.append(f"`{sp['symbol']}` is {title} (Act III, Kythera Isle; SCRIPT.md Part 10). Pair it "
               "with the `aethos` primary, which supplies the open grass, paths, sand, sea, "
               "olives and cypresses.\n")
    out.append("**This file is generated.** `tools/ichor/art/kythera_build.py " + name + "` paints "
               "the tileset, compiles it, registers it and rewrites this catalog. The art is in "
               "`tools/ichor/art/kythera_*.py` (and `melos_art.py`), the palette plan and the "
               "borrowed ground in `kythera_lib.py`.\n")
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
    if name == "kythera":
        out.append(FAMILY)
    else:
        out.append("It is one of the Kythera family of secondaries; see "
                   "[`TILES_kythera.md`](TILES_kythera.md) for why the art is split and which "
                   "seams then need aethos-only strips.\n")
    out.append(CONVENTIONS.format(starts=starts, name=name, dir=d, anims=anims, used=used,
                                  meta=meta, labels=labels))
    for sec, _ in sp["sections"]:
        out.append(f"## {SECTION_TITLES.get(sec, sec.title())}\n")
        for s in structs:
            if s["section"] != sec:
                continue
            out.append(f"### {s['title']}\n")
            out.append(f"`{s['key']}`, {s['w']} wide by {s['h']} tall. {s['notes']}\n")
            if s["key"] in ("seagrass", "shingle", "obsidian") and len(s["names"]) > 40:
                out.append("Shape keys (kythera_lib.blob_key) and their ids:\n")
                rows = ["| Shape key | Id |", "|---|---|"]
                for nm, (cx, cy) in sorted(s["names"].items()):
                    rows.append(f"| `{nm}` | 0x{s['ids'][cy][cx]:03X} |")
                out.append("\n".join(rows) + "\n")
                beh = s["behaviors"].get("0,0", "MB_NORMAL")
                out.append(f"Every cell: walk `{s['walk'][0][0]}`, `{beh}`.\n")
                continue
            out.append(grid(s["ids"], s["walk"]) + "\n")
            out.append(cell_table(s, attrs) + "\n")
        if sec == "town" and cat.get("fronts"):
            out.append("### House fronts\n")
            out.append("Every house is a home (MAP_DESIGN.md §2), so each front has a door. These "
                       "are arrangements of the `house` kit's parts and cost no metatiles of their "
                       "own; mix the parts for more. Walk: every house cell is `X` except its door "
                       "(`D`).\n")
            for k, f in cat["fronts"].items():
                walk = [["D" if r.startswith("door") else "X" for r in row] for row in f["rows"]]
                out.append(f"**{f['title']}** (`{k}`): {f['who']}.\n")
                out.append(grid(f["ids"], ["".join(w) for w in walk]) + "\n")
    doc = DOCS / sp["doc"]
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("\n".join(out))
    print(doc.relative_to(ROOT))


if __name__ == "__main__":
    import kythera_build as B
    for n in sys.argv[1:] or ["kythera"]:
        sp = B.spec(n)
        main(n, sp, "?", "?")
