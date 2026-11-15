"""Write design/postgame/TILES_<set>.md for a far-lands secondary: every
structure by key, its ids and walk codes, every named piece, the palette plan,
the animations and the budget. Called by farlands_build.py after a compile."""
from __future__ import annotations

import farlands_lib as F

ROOT = F.ROOT
DOCS = ROOT / "design/postgame"

GROUND_ID = {"grass": "0x001", "path": "0x1D9", "sand": "0x124", "sea": "0x170",
             "shallow": "0x0D1", "fall": "0x0B3"}

FAMILY = {
    "steppe": "the steppe family (`steppe`, `steppe_town`, `steppe_camp`)",
    "steppe_town": "the steppe family (`steppe`, `steppe_town`, `steppe_camp`)",
    "steppe_camp": "the steppe family (`steppe`, `steppe_town`, `steppe_camp`)",
    "far_west": "the far-west family (`far_west`, `hesperides`)",
    "hesperides": "the far-west family (`far_west`, `hesperides`)",
}


def grid(s):
    lines = []
    for y in range(s.h):
        ids = " ".join(f"{s.ids[y][x]:03X}" for x in range(s.w))
        lines.append(f"{ids}    {s.walk[y]}")
    return "```\n" + "\n".join(lines) + "\n```"


def names_table(s, blob=False):
    if not s.names:
        return ""
    rows = []
    for n, (x, y) in s.names.items():
        mb = s.behaviors.get((x, y), "")
        g = s.ground.get((x, y), "")
        rows.append((n, s.ids[y][x], s.walk[y][x], g, mb))
    if blob:
        out = ["| Shape key | Id |", "|---|---|"]
        for n, i, *_ in rows:
            out.append(f"| `{n}` | 0x{i:03X} |")
        return "\n".join(out)
    out = ["| Piece | Id | Walk | Ground | Behavior |", "|---|---|---|---|---|"]
    for n, i, w, g, mb in rows:
        out.append(f"| `{n}` | 0x{i:03X} | `{w}` | {g or 'drawn'} | {mb or '—'} |")
    return "\n".join(out)


def main(name, sp, sections, n_tiles, n_meta, groups):
    mod = sp["module"]
    structs = [s for _, ss in sections for s in ss]
    oik = [s.key for s in structs if s.oik]
    anims = sorted({a for s in structs for a in F.anim_tiles(s).values()})
    starts = ", ".join(f"{sec} at 0x{0x200 + sp['rows'][sec] * 8:03X}" for sec, _ in sections)
    L = []
    L.append(f"# {name} tileset catalog\n")
    L.append(f"`{sp['symbol']}` is {sp['title']}. {sp.get('intro', '')} Pair it with the `aethos` "
             "primary, which supplies the open grass, the limestone path, sand, the sea, olives and "
             "cypresses. It is one of " + FAMILY[name] + ".\n")
    L.append("**This file is generated.** `tools/ichor/art/farlands_build.py " + name + "` paints the "
             "tileset, compiles it, registers it and rewrites this catalog. The art is in "
             f"`tools/ichor/art/farlands_{name}.py` (with `farlands_ground.py` and `farlands_kits.py`); "
             "the palette groups are in that file's `GROUPS`, the borrowed ground in `farlands_lib.py`.\n")
    imgs = [(f"farlands_{sp['dir']}_pieces.png", "Every structure on its ground (`*` marks the "
             "Oikoumene's pieces)"),
            (f"farlands_{sp['dir']}_sheet.png", "The numbered metatile sheet, rendered from the "
             "compiled tileset")] + sp.get("images", [])
    L.append("| Image | Shows |\n|---|---|")
    for f, what in imgs:
        L.append(f"| [`img/{f}`](img/{f}) | {what} |")
    L.append("")
    for f, what in sp.get("images", [])[:1]:
        L.append(f"![{what}](img/{f})\n")
    if sp.get("why_split"):
        L.append("**Why a sister set.** " + sp["why_split"] + "\n")
    L.append("## How to use it\n")
    L.append("**Ids.** Each grid lists metatile ids as Porymap shows them, row by row, with the walk "
             f"codes beside them. Each section starts on a fixed row of the sheet ({starts}). "
             "Structures are placed first-fit in build order, so appending one never moves another. "
             "Place pieces by key and name, never by raw id: `tools/ichor/maps/farlands_tiles.py` holds "
             f"every far-lands catalog as a Python dict (`mid('{name}', key, piece)`, and "
             f"`soft('{name}', key, region, x, y)` for soft ground); `build/{sp['dir']}/catalog.json` "
             "is the same as JSON.\n")
    if oik:
        L.append("**The Oikoumene's pieces** (drawn for world-oikoumene's lands, OIKOUMENE.md; "
                 "`oikoumene_pieces('" + name + "')` lists them): " + ", ".join(f"`{k}`" for k in oik)
                 + ". The rest serve LABORS's maps first; both sessions may use anything here.\n")
    L.append("**Walk codes:**\n")
    L.append("| Code | Meaning |\n|---|---|")
    used_codes = {c for s in structs for row in s.walk for c in row}
    for c, m in F.WALK_CODES.items():
        if c in used_codes:
            L.append(f"| `{c}` | {m} |")
    L.append("")
    L.append("**Soft ground.** Grasses, roads, earth, mud and water come as 47 soft-edged shapes, "
             "keyed by a cell's neighbors (`farlands_lib.blob_key`, or `shape()` in "
             "`farlands_tiles.py`): `1|` then N NE E SE S SW W NW, 1 where the neighbor is in the "
             "region, a diagonal counting only when both its sides are. `1|11111111` is the full "
             "interior. Draw regions as irregular masks that follow the land (MAP_DESIGN 1: never "
             "plain rectangles); the shapes round every outer corner and wobble every edge.\n")
    L.append("**Borrowed ground.** Cells marked *grass*, *path*, *sand*, *sea*, *shallow* or *fall* "
             "draw no ground of their own: after Porytiles compiles, the build points their "
             "bottom-layer tiles at aethos's grass (`0x001`), limestone path (`0x1D9`), sand "
             "(`0x124`), animated sea (`0x170`), shallows (`0x0D1`) or waterfall (`0x0B3`). They meet "
             "aethos ground exactly and cost no tiles. A borrowed cell's art is in one layer: the "
             "middle (`COVERED`, under the player) or the top (`SPLIT`, over the player). Cells "
             "marked *drawn* paint their own ground, aethos's grass pixel for pixel where it shows.\n")
    L.append("**Seams.** MAP_DESIGN 5: the 6 rows (or 8 columns) nearest a connection to a map on a "
             "different secondary use only aethos metatiles. Everything here fades onto aethos "
             "ground, so a map can always end its soft regions before the strip: grass and earth "
             "shapes onto aethos grass, water onto aethos sea, roads through `road_join` onto "
             "aethos's limestone path patch (`1D0`-`1E2`).\n")
    if anims:
        L.append("**Animations.** Porytiles animations, driven by "
                 f"`InitTilesetAnim_PorytilesManaged_{sp['symbol'].replace('gTileset_', '')}` "
                 f"(`include/porytiles_generated/tilesets/{sp['dir']}/generated_anim_code.h`): "
                 + "; ".join(f"`{a}`: {sp.get('anim_notes', {}).get(a, '')}" for a in anims)
                 + ". Every 8x8 tile that changes between frames is an animated tile; frame 0 is the "
                 "key drawn in the sheet.\n")
    L.append("**Layer types** in the cell tables: `NORMAL` (bottom and middle under the player), "
             "`COVERED` (ground under the middle layer), `SPLIT` (ground under, art over the player).\n")
    L.append("**Palettes.** Every 8x8 tile, in every animation frame, draws from one of these color "
             "groups, one per secondary palette (6-12), passed to Porytiles as packing hints.\n")
    L.append("| Group | Use | Colors |\n|---|---|---|")
    for g, names in groups.items():
        use = sp.get("group_notes", {}).get(g, "")
        cols = " ".join(f"`{n}`" for n in names)
        L.append(f"| {g} | {use} | {cols} |")
    L.append("")
    L.append(f"**Tile budget.** {n_tiles} of {sp['limit']} tiles ({n_meta} metatiles). "
             + (f"The door animations copy their frames into tiles {sp['limit']}-511, so the build "
                "fails past " + str(sp['limit']) + ". " if sp['limit'] == 504 else
                f"Its maps use wide doors, whose animation frames copy over tiles 496-511 "
                "(`DOOR_TILE_START_SIZE2`, `src/field_door.c`), so the build fails past 496. ")
             + "Static tiles within two pixels of one another are merged.\n")
    if sp.get("labels"):
        labs = []
        by = {s.key: s for s in structs}
        for key, items in sp["labels"]:
            for piece, label in items:
                labs.append(f"`METATILE_{sp['label']}_{label}`")
        L.append(f"**Scripted swaps.** The build writes the ids scripts swap to the `{sp['symbol']}` "
                 "block at the end of `include/constants/metatile_labels.h`: " + ", ".join(labs) + ".\n")
    if sp.get("extra_doc"):
        L.append(sp["extra_doc"] + "\n")
    for sec, ss in sections:
        L.append(f"## {sp.get('section_titles', {}).get(sec, sec.capitalize())}\n")
        for s in ss:
            blob = len(s.names) >= 47 and "1|11111111" in s.names
            star = " *(Oikoumene)*" if s.oik else ""
            L.append(f"### {s.title}{star}\n")
            L.append(f"`{s.key}`, {s.w} wide by {s.h} tall. {s.notes}\n")
            if blob:
                L.append("Shape keys and their ids:\n")
                L.append(names_table(s, blob=True) + "\n")
            else:
                L.append(grid(s) + "\n")
                t = names_table(s)
                if t:
                    L.append(t + "\n")
    (DOCS / sp["doc"]).write_text("\n".join(L).rstrip() + "\n")
    print(f"design/postgame/{sp['doc']}")
