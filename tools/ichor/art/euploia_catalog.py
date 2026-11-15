"""Write the generated part of design/postgame/TILES_euploia.md: the palette
groups, the tile budget, every named piece with its ids and walk grid, and the
cells each setmetatile variant changes. Everything outside the markers is
written by hand (the keepsake table, the render-and-critique passes) and kept
as it is. Ported from world-act1's trireme_catalog.py."""
from __future__ import annotations

from euploia_lib import C, GROUPS, ROOT

DOC = ROOT / "design/postgame/TILES_euploia.md"
START, END = "<!-- generated: euploia_build.py -->", "<!-- end generated -->"

GROUP_USE = {
    "wood": "Deck planks, bulwarks, the hull's side, the mast, the stern timbers, the helm, the "
            "benches, the gangplank, bronze shields, the eye and the wale",
    "water": "Where the ship meets the sea: waterline foam, shadow on the water, the ram, the "
             "steering oar's blade",
    "sail": "The linen sail, its yard, lifts, sheets and red head band; the chart table and "
            "Odysseus's Periplous on it",
    "cargo": "Amphorae, the water jar, coiled rope, the Pithos, the mess's bowls and table, "
             "Kydon's goods and awning, Diktys's nets, Iaso's chest, the sea chests",
    "shrine": "Poseidon's altar and trident; the trophy shelf and its seven keepsakes",
    "hold": "Below deck's dark timber, its floor and lamp, the bunk with its fleece and "
            "blanket, the rug",
    "hearth": "Hestia's fire: the hearth, its clay hood, pot and flames; the ladder and the "
              "daylight down the hatch",
}

SKELETON = f"""# Euploia tileset catalog

`gTileset_Euploia` is the *Euploia* refitted for the post-game: her deck and her
quarters below, a secondary on the `aethos` primary for `MAP_EUPLOIA_DECK` and
`MAP_EUPLOIA_BELOW`.

{START}
{END}
"""


def hexid(i):
    return f"0x{i:03X}"


def grid_block(ids, walk):
    w = max(len(r) for r in ids)
    lines = []
    for r, wr in zip(ids, walk):
        lines.append(" ".join(hexid(i) for i in r).ljust(w * 6) + "  " + " ".join(wr))
    return "```text\n" + "\n".join(lines) + "\n```"


def generated(data, used):
    out = []
    out.append("""**This section is generated** by `tools/ichor/art/euploia_build.py`, which draws the
tileset (`euploia_deck.py`, `euploia_below.py`), compiles it and rewrites the catalog
between these markers. Everything outside the markers is written by hand.

![The deck](img/euploia_deck.png)

![Below deck](img/euploia_below.png)

## How it works

**Scenes, not structures** (as world-act1's trireme). The ship is drawn as two whole
pictures, the deck (24×12 cells) and below deck (20×10), each in three layers. The build
slices them into 16×16 cells and keeps one metatile per distinct cell, so the maps are
the scenes cell for cell (`build/euploia/catalog.json`, `scenes`).
`tools/ichor/maps/euploia.py` writes the layouts from there and places events by the
named pieces below, never by raw id.

**Variants.** Below deck is also drawn in eight other states. Only the cells that differ
from the plain scene become metatiles, and the catalog lists them as `(x, y, id)` for
`setmetatile`: `hearth_cold` (Lampon not aboard) and `keepsake_<name>` (each keepsake on
its spot). `tools/ichor/maps/euploia.py` writes them into below deck's `scripts.pory` as
small scripts, between generated markers.

**Borrowed sea.** Every deck cell on the water points its bottom layer at aethos's open
sea (`0x170`), so the sea round the hull animates with aethos's water and costs no tiles.
Open water with nothing on it is `0x170` itself. Rebuild the ship whenever aethos is
repainted.

**Mirrored hull.** The hull is symmetric about the ship's middle, so the bow's curves are
the stern's tiles flipped. The ram, eye and stem, and the aphlaston and steering oars, are
drawn after the mirror and are their own.

**Walk codes.** In the grids below: `X` solid; `.` walkable; `~` open sea (solid); `w`
the hatch and the ladder (`MB_LADDER`: the warps); `c` the stall's counter (`MB_COUNTER`).
""")
    out.append("## Palettes\n")
    out.append("Seven groups, one per secondary palette (6-12). Every 8×8 tile draws from one group.\n")
    out.append("| Group | Colors | Use |\n|---|---|---|")
    for g, names in GROUPS.items():
        cols = ", ".join(f"`{n}` {C[n]}" for n in names)
        out.append(f"| {g} | {len(names)}: {cols} | {GROUP_USE[g]} |")
    out.append("")
    out.append(f"## Tile budget\n\n**{used} of 504 tiles**, {data['metatiles']} metatiles "
               f"(of 512). The door animations own tiles 504-511, so the build fails past 504. "
               f"Neither map has a door. Tiles within four pixels of another are redrawn as that "
               f"one before Porytiles dedups them.\n")
    out.append("## Pieces\n")
    for p in data["pieces"]:
        out.append(f"### {p['title']}\n")
        out.append(f"`{p['key']}`, {p['scene']} ({p['x']}, {p['y']}), {p['w']} wide by {p['h']} tall. "
                   f"{p['notes']}\n")
        out.append(grid_block(p["ids"], p["walk"]))
        out.append("")
    out.append("## Variants\n")
    out.append("| Variant | Cells | (x, y) → metatile |\n|---|---|---|")
    for name, cells in data["variants"].items():
        body = ", ".join(f"({x},{y})→{hexid(i)}" for x, y, i in cells)
        out.append(f"| `{name}` | {len(cells)} | {body} |")
    out.append("")
    return "\n".join(out)


def write(data, used):
    text = DOC.read_text() if DOC.exists() else SKELETON
    if START not in text:
        text = SKELETON + text
    a, b = text.index(START), text.index(END)
    text = text[:a + len(START)] + "\n" + generated(data, used) + "\n" + text[b:]
    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(text)
    print(DOC)
