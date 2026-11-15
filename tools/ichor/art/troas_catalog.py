"""Write design/oikoumene/TILES_troas.md from the built structures.

troas_build.py runs this after a build, so the ids always match the compiled
tileset.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "design/oikoumene/TILES_troas.md"

INTRO = """\
# Troas tileset catalog

`gTileset_Troas` is the Troad's outdoor secondary: the wheat-gold plain, the Skamander's
reeds and banks, Ida's pines, heroes' burial mounds, the fast blue Hellespont, Sestos's
harbor and Hero's tower, and Ilion's great sloping walls of pale limestone (OIKOUMENE.md
§4.1, §7). Pair it with the `aethos` primary, which supplies grass, paths, sand, the sea,
cliffs, olives, cypresses and stone pines, the Asclepeion and the Agora.

**This file is generated.** `tools/ichor/art/troas_build.py` draws the tileset, compiles it
and rewrites this catalog. The art is in `troas_land.py`, `troas_sea.py`, `troas_walls.py`
and `troas_town.py`; the palette plan and painters are in `troas_lib.py`.

![Every troas structure on its ground](img/troas_pieces.png)

## Palettes (slots 6-12)

| Group | Holds |
|---|---|
| wood | Akti's wood group, slot for slot: the Euploia, the landing stage, the Skaian Gate's leaves, hay, dye vats, the chariot, wool |
| marble | Akti's marble group: the temple of Athena, Priam's megaron, the great herm, Hero's lamp, Helle's gilded ram |
| stone | Akti's stone group: Ilion's walls, gates and towers, Hero's tower, the quay, Helle's rock, the current's foam, troughs, springs, the mason's blocks |
| plaster | Trojan houses: ochre lime plaster, packed-clay flat roofs, timber |
| plaster2 | the same with whitewash, slot for slot (`house_kit_white` costs no tiles) |
| field | wheat, reeds, river banks, field flowers |
| grove | Ida's pines, the oak, the elm, the burial mound |

## How to use it

- Ids below are metatile ids (secondary metatiles start at `0x200`). Map builders place
  structures by key and part name from `build/troas/catalog.json`.
- Walk codes: `X` impassable, `.` passable, `D` a door (`MB_NON_ANIMATED_DOOR`, warp here).
- Cells marked *on grass / sand / sea* borrow aethos's ground metatile under their art, so
  they sit seamlessly on aethos's ground and the sea under them animates.
- **Seams.** Troas pieces may not stand in a seam's aethos-only strip (MAP_DESIGN §5)
  unless the neighbour also uses troas.
- **Door tiles.** Door animations overwrite tiles 504-511; the tileset stays under 504.
"""


def grid(rows):
    return "\n".join("    " + " ".join(f"{v:03X}" if isinstance(v, int) else v for v in r) for r in rows)


def main(used, structs, sections):
    lines = [INTRO, f"**Tile budget.** {used} of 504 tiles are used.\n"]
    for _, key, title, blurb in sections:
        lines.append(f"## {title}\n\n{blurb}\n")
        for s in structs:
            if s.section != key:
                continue
            lines.append(f"### {s.title}\n")
            lines.append(f"`{s.key}`, {s.w} wide by {s.h} tall. {s.notes}\n")
            grounds = sorted({g for g in s.ground.values() if g != "none"})
            if grounds:
                lines.append(f"Borrowed ground: {', '.join(grounds)}.\n")
            lines.append("```")
            lines.append(grid(s.ids))
            lines.append("")
            lines.append(grid([list(r) for r in s.walk]))
            lines.append("```")
            names = getattr(s, "names", {})
            if names:
                lines.append("Parts: " + ", ".join(f"`{n}` {s.ids[cy][cx]:03X}"
                                                   for n, (cx, cy) in names.items()) + "\n")
            beh = {mb for mb in s.behaviors.values()}
            if beh:
                lines.append("Behaviors: " + ", ".join(sorted(beh)) + "\n")
    OUT.write_text("\n".join(lines) + "\n")
    print(OUT)
