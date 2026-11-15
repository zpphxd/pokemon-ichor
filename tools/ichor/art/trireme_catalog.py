"""Write the generated part of design/phase2/TILES_trireme.md: the palette
groups, the tile budget, every named piece with its ids and walk grid, and the
cells each setmetatile variant changes. Everything outside the markers is
written by hand (the render-and-critique passes) and kept as it is."""
from __future__ import annotations

from trireme_lib import C, GROUPS, ROOT

DOC = ROOT / "design/phase2/TILES_trireme.md"
START, END = "<!-- generated: trireme_build.py -->", "<!-- end generated -->"

GROUP_USE = {
    "wood": "Deck planks, bulwarks, the hull's side, the mast, the stern timbers, bronze shields, the eye and the wale",
    "water": "Where the ship meets the sea: waterline foam, shadow on the water, oar blades, the ram, the steering oar's blade",
    "sail": "The linen sail, its yard, lifts, sheets and red head band",
    "cargo": "Amphorae, crates, sacks, the stowed oars, the water jar, coiled rope",
    "bronze": "The klepsydra's bronze bowls and water; the far coast's haze, walls and town",
    "hold": "The hold's dark timber, the rowers and their cushions, the daylight in the ports",
    "stores": "The hold's ladder and light, its jars, pithos, lamp and rope",
}

SKELETON = f"""# Trireme tileset catalog

`gTileset_Trireme` is the *Euploia*'s deck and hold, a secondary on the `aethos`
primary for `MAP_TRIREME_EUPLOIA_DECK` and `MAP_TRIREME_EUPLOIA_HOLD`.

{START}
{END}

## Render-and-critique passes
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
    out.append("""**This section is generated** by `tools/ichor/art/trireme_build.py`, which draws the tileset
(`trireme_deck.py`, `trireme_hold.py`), compiles it and rewrites the catalog between these
markers. The passes below the markers are written by hand.

![The deck](img/trireme_deck.png)

## How it works

**Scenes, not structures.** The ship is drawn as two whole pictures, the deck (24×16 cells)
and the hold (18×9), each in three layers. The build slices them into 16×16 cells and keeps
one metatile per distinct cell, so the maps are the scenes cell for cell
(`build/trireme/catalog.json`, `scenes`). `tools/ichor/maps/trireme.py` writes the layouts
from there and places events by the named pieces below, never by raw id.

**Variants.** The deck is also drawn in five other states. Only the cells that differ from the
plain deck become metatiles, and the catalog lists them as `(x, y, id)` for `setmetatile`:
`sail_sag` (the halcyon calm), `sail_fill` (casting off; the wind coming back), `oars_out`
(the port bank rowing), `klepsydra_up` (the water clock running backward) and `coast` (the
mainland ahead of the bow, beat 10C). `tools/ichor/maps/trireme.py` writes them into the
deck's `scripts.pory` as small scripts (`TriremeDeck_EventScript_SailSag` and the rest),
between generated markers.

**Borrowed sea.** Every cell on the water points its bottom layer at aethos's open sea
(`0x170`), so the sea round the hull animates with aethos's water and costs no tiles. Open
water with nothing on it is `0x170` itself. Rebuild the trireme whenever aethos is repainted.

**Mirrored hull.** The hull is symmetric about the ship's middle, so the stern's curves are the
bow's tiles flipped. The ram, eye and stem, and the aphlaston and steering oars, are drawn
after the mirror and are their own.

**Walk codes.** In the grids below: `X` solid; `.` walkable; `~` open sea (solid); `f` sea you
fish into from the deck (`MB_OCEAN_WATER`, walkable collision at water elevation, so only the
rod and a surfer's single step reach it); `w` the hatch and the ladder (`MB_LADDER`: the warps).
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
               f"Neither map has a door, but the rule holds for every secondary. Tiles within four "
               f"pixels of another are redrawn as that one before Porytiles dedups them.\n")
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
