#!/usr/bin/env python3
"""Write design/phase4/TILES_<tileset>.md for the Lakonia-family secondaries
from build/<dir>/catalog.json and the compiled metatile attributes.

lakonia_build.py runs this after each build, so the ids, behaviors and layer
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

from kythera_catalog import LAYER, cell_table, grid  # noqa: E402

FAMILY = """\
## The Lakonia family

SCRIPT.md's front matter planned one `lakonia` secondary for all six maps.
Their pieces come to far more than one secondary's 504 tiles (the town alone,
with its ring, stoa, houses and the Taygetos wall, fills most of one), so the
art is split by map, as the Kythera family is. Every one pairs with the
`aethos` primary and is built by `tools/ichor/art/lakonia_build.py` from shared
painters, so a piece two of them carry (the Eurotas, the plane tree, the house
kit, the Taygetos rock) is drawn once and looks the same in both.

| Tileset | Symbol | Maps | Catalog |
|---|---|---|---|
| `gytheion` | `gTileset_Gytheion` | Gytheion; Route 24, the strait off Malea | [`TILES_gytheion.md`](TILES_gytheion.md) |
| `eurotas` | `gTileset_Eurotas` | Route 25, up the Eurotas | [`TILES_eurotas.md`](TILES_eurotas.md) |
| `lakonia` | `gTileset_Lakonia` | Lakonia | [`TILES_lakonia.md`](TILES_lakonia.md) |
| `stymphalia` | `gTileset_Stymphalia` | Route 26, Lake Stymphalia, Route 27 | [`TILES_stymphalia.md`](TILES_stymphalia.md) |

**Seams.** With the split, MAP_DESIGN §5's seam rule applies wherever neighbours
use different secondaries: the strip nearest the seam, on both maps, uses only
`aethos` metatiles (grass, path, olives, cypresses, pines, aethos sea).

| Seam | Tilesets | Rule |
|---|---|---|
| Route 24's west end ↔ Gytheion's harbor mouth | gytheion / gytheion | exempt |
| Route 24's east end ↔ Skandeia's north bay | gytheion / skandeia | 8 columns, both maps (open sea: aethos's anyway) |
| Gytheion's north gap ↔ Route 25's south end | gytheion / eurotas | 6 rows, both maps |
| Route 25's west end ↔ Lakonia's east edge | eurotas / lakonia | 8 columns, both maps: keep the Eurotas, its bridge and the plane trees 9 or more columns in from the seam |
| Lakonia's north gap ↔ Route 26's south end | lakonia / stymphalia | 6 rows, both maps |
| Route 26 ↔ Lake Stymphalia ↔ Route 27 | stymphalia / stymphalia | exempt |
| Route 27's west end ↔ Arkadia (Act II) | stymphalia / Act II's | 8 columns, both maps |

The strips cost little: the gaps and roads are aethos path and grass anyway,
and aethos olives, cypresses and stone pines plant the edges.
"""

CONVENTIONS = """\
## How to use it

**Ids.** Each grid lists metatile ids as Porymap shows them, row by row. Each section
starts on a fixed row of the sheet ({starts}). Structures are placed first-fit in build
order, so appending a new one never moves an old one. Map builders should place pieces
by key and name, never by raw id: `tools/ichor/maps/lakonia_tiles.py` holds every
Lakonia-family catalog as a Python dict (`mid('{name}', 'house', 'door')`, and
`blob_key(mask, x, y)` for the soft-edged pieces), and `build/{dir}/catalog.json` is
the same as JSON.

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
| `C` | A sea current: `MB_WESTWARD_CURRENT`, surfable. |
| `J` | Ledge: `MB_JUMP_SOUTH`. |

**Soft-edged pieces** (`yard`, `sands`, `river`, `reeds`, `marsh`, `marsh_reeds`,
`curtain`, `scree`...) are drawn as all 47 blob shapes and named by shape key: `1|`
then the cell's N NE E SE S SW W NW neighbours (1 = in the region; a diagonal counts
only when both its sides do). `blob_key(mask, x, y)` in `lakonia_tiles.py` computes it.
Each 8x8 quadrant depends only on its own two sides and corner, so a whole set costs
about a dozen tiles.

**Borrowed ground.** Cells marked *grass*, *path*, *sand*, *sea* or *shallow* draw
no ground of their own: after Porytiles compiles, the build points their bottom-layer
tiles at aethos's grass (`0x001`), limestone path (`0x1D9`), sand (`0x124`), animated
sea (`0x170`) or animated turquoise shallows (`0x0D1`). They meet aethos ground exactly
and cost no tiles. Rebuild whenever aethos is repainted. A borrowed cell's own art is
in one layer: the middle (`COVERED`, under the player) or the top (`SPLIT`, over him).

**Fresh water** is Lakonia's own: the Eurotas's slow green water and Stymphalia's black
water are animated textures in the bottom layer of every water cell (the same few
tiles under all of them), with banks, reeds, planks and stone on the middle layer.

**Animations.** {anims}

**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player),
`COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).

**Palettes.** Every 8x8 tile, in every animation frame, draws from one of seven color
groups, one per secondary palette (`lakonia_lib.GROUPS`), passed to Porytiles as packing
hints:

| Group | Use |
|---|---|
{groups}

**Tile budget.** {used} of 504 tiles ({meta} metatiles). The door animations copy their
frames into tiles 504-511 (`DOOR_TILE_START_SIZE1`, `src/field_door.c`), so the build
fails past 504. Static tiles within two pixels of one another are merged.
{labels}"""

GROUP_USE = {
    "red": "Lakonian red and bronze: cloaks, shields, doors, awnings, the bronze gods",
    "stone": "Plain stone, plaster and clay roofs: houses, the stoa, stelai, bridges, the causeway",
    "veg": "Plane, holm-oak, oak, walnut, willow; bark; the Sown Field",
    "vegb": "Trees with Route 25's flowers: hyacinths and oleander",
    "river": "The Eurotas: green water, its banks, reeds and pink oleander",
    "mount": "Taygetos and the Skiritis: dark rock, scree, black pine; Malea's foam",
    "purple": "Gytheion's murex purple: stains, shell heaps, lead vats, on the quay's limestone",
    "marsh": "Stymphalia: black water, its reeds and mud, bronze feathers",
    "wood": "Timber and thatch: boardwalks, the stilt hut, racks, the barracks' roof, posts",
    "yard": "Beaten sand: the agoge's yard, the ring, the wrestling sands, their stone",
    "foam": "Kythera's foam group: the surf on Gytheion's shingle and Elaphonisos's sand",
    "terra": "Kythera's timber and terracotta: the fishing boats",
    "deep": "The drowned town under Route 24's turquoise shallows",
}

ANIM_TEXT = {
    "eurotas": "`eurotas`: the river's slow ripples drifting (3 frames)",
    "marsh": "`marsh`: the black water, barely moving (3 frames, slow)",
    "glint": "`glint`: bronze feathers catching the light in the roosting reeds (3 frames, mostly still)",
    "flame": "`flame`: fire in an altar, a hearth or a herm-shrine's lamp (3 frames)",
    "current": "`current`: the Malea current's streaks running west (4 frames)",
    "steam": "`steam`: the dye vats steaming (3 frames)",
    "surf": "`surf`: Kythera's surf, washing up and back on the shingle (3 frames)",
}

SECTION_TITLES = {
    "town": "Town", "yard": "Yards and the ring", "land": "The land", "water": "Fresh water",
    "harbor": "The harbor", "coast": "The coast", "sea": "The strait", "route": "The road",
    "marsh": "Lake Stymphalia", "hills": "The hills",
}


def main(name, sp, used, meta):
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
             "the sheet. Borrowed sea and shallows keep aethos's own animations."
             ) if anim_names else "None of its own; the borrowed sea and shallows animate."
    labels = ""
    want = sp.get("labels", [])
    if want:
        items = ", ".join(f"`METATILE_{sp['label']}_{lab}`" for _, its in want for _, lab in its)
        labels = ("\n**Scripted swaps.** The build writes the ids scripts swap to the "
                  f"`{sp['symbol']}` block at the end of `include/constants/metatile_labels.h`: "
                  f"{items}.\n")
    grows = "\n".join(f"| {g} | {GROUP_USE.get(g, g)} |" for g in sp["groups"])
    out = [f"# {name} tileset catalog\n",
           f"`{sp['symbol']}` is {sp['title']} (Act III, Lakonia; SCRIPT.md Part 10). It serves "
           f"{sp['maps']}. Pair it with the `aethos` primary, which supplies the open grass, "
           "paths, sand, sea, olives, cypresses and stone pines.\n",
           "**This file is generated.** `tools/ichor/art/lakonia_build.py " + name + "` paints "
           "the tileset, compiles it, registers it and rewrites this catalog. The art is in "
           "`tools/ichor/art/lakonia_*.py` (the plane tree is Kythera's), the palette plan, "
           "the water and the soft-edge autotiles in `lakonia_lib.py`.\n"]
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
    if name == "lakonia":
        out.append(FAMILY)
    else:
        out.append("It is one of the Lakonia family of secondaries; see "
                   "[`TILES_lakonia.md`](TILES_lakonia.md) for why the art is split and which "
                   "seams then need aethos-only strips.\n")
    if sp.get("undrawn"):
        out.append("**Not drawn yet.** " + sp["undrawn"] + "\n")
    out.append(CONVENTIONS.format(starts=starts, name=name, dir=d, anims=anims, used=used,
                                  meta=meta, labels=labels, groups=grows))
    for sec, _ in sp["sections"]:
        out.append(f"## {SECTION_TITLES.get(sec, sec.title())}\n")
        for s in structs:
            if s["section"] != sec:
                continue
            out.append(f"### {s['title']}\n")
            out.append(f"`{s['key']}`, {s['w']} wide by {s['h']} tall. {s['notes']}\n")
            blob = [n for n in s["names"] if n.startswith("1|")]
            if len(blob) >= 40:
                rows = ["| Shape key | Id |", "|---|---|"]
                for nm in sorted(blob):
                    cx, cy = s["names"][nm]
                    rows.append(f"| `{nm}` | 0x{s['ids'][cy][cx]:03X} |")
                out.append("Shape keys (`blob_key`) and their ids:\n")
                out.append("\n".join(rows) + "\n")
                beh = s["behaviors"].get("0,0", "MB_NORMAL")
                out.append(f"Every shape cell: walk `{s['walk'][0][0]}`, `{beh}`.\n")
                extra = [n for n in s["names"] if not n.startswith("1|")]
                if extra:
                    rows = ["| Id | Piece | Walk | Behavior | Layer |", "|---|---|---|---|---|"]
                    for nm in extra:
                        cx, cy = s["names"][nm]
                        i = s["ids"][cy][cx]
                        a = int(attrs[i - 0x200]) if attrs is not None else 0
                        rows.append(f"| 0x{i:03X} | `{nm}` | `{s['walk'][cy][cx]}` | "
                                    f"`{s['behaviors'].get(f'{cx},{cy}', 'MB_NORMAL')}` | "
                                    f"{LAYER.get(a >> 12, a >> 12)} |")
                    out.append("Extra cells:\n")
                    out.append("\n".join(rows) + "\n")
                continue
            out.append(grid(s["ids"], s["walk"]) + "\n")
            out.append(cell_table(s, attrs) + "\n")
        if sec == "town" and cat.get("fronts"):
            out.append("### House fronts\n")
            out.append("Every house is a home (MAP_DESIGN.md §2), so each front has a door. These "
                       "are arrangements of the `house` kit's parts and cost no metatiles of their "
                       "own; mix the parts for more (`front(tileset, key)` in `lakonia_tiles.py` "
                       "returns the ids). Walk: every house cell is `X` except its door (`D`).\n")
            for k, f in cat["fronts"].items():
                walk = [["D" if r.startswith("door") else "X" for r in row] for row in f["rows"]]
                out.append(f"**{f['title']}** (`{k}`): {f['who']}.\n")
                out.append(grid(f["ids"], ["".join(w) for w in walk]) + "\n")
    doc = DOCS / sp["doc"]
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("\n".join(out))
    print(doc.relative_to(ROOT))


if __name__ == "__main__":
    import lakonia_build as B
    for n in sys.argv[1:] or ["lakonia"]:
        main(n, B.spec(n), "?", "?")
