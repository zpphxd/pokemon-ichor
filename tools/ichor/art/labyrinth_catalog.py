#!/usr/bin/env python3
"""Write design/phase4/TILES_labyrinth.md and TILES_mychos.md from
build/<tileset>/catalog.json.

labyrinth_build.py runs this after each build, so every id in the catalogs
matches the compiled tilesets.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from emporion_catalog import structure  # noqa: E402

PALETTES = [
    ("stone", "Dark stone with thread red", "The masonry of every map (a cool grey limestone "
     "that warms toward the light), the rings' darker slabs, Ariadne's thread (three reds), "
     "lamp-warm and dawn-cool light on stone (the skylight pools), and the latent glow paint"),
    ("minoan", "Minoan red", "Red columns, ochre, gypsum, black capitals, terracotta, horns "
     "of consecration, Minos's tomb and bier, the Mistress's shrine"),
    ("fresco", "Fresco blue", "The dance frescoes, and the Icarus Shaft's dawn sky"),
    ("bronze", "Bronze and Titan", "Automata, grates, dials, anchor rings, the labrys seal, "
     "helmets, shields, the vault's gold; the Titans' slate (their banners) and gold"),
    ("fire", "Forge fire", "Flames, embers, molten bronze, iron (the anvils), clay (the "
     "furnace, the hearth), oak in firelight (bellows, tub). Its three bronze shades are "
     "bronze's own, so a brazier's bowl can share a tile with its flame"),
    ("night", "Starry night", "Ring VII's starlit marble, the beam by night, the dancing floor, "
     "the Starry Chamber's black basin, its stars and the star-clock's gold and lapis"),
    ("timber", "Timber and papyrus", "Benches, tables, bunks, shelves, wax tablets, scrolls"),
]

SPLIT = """\
**Two tilesets.** LABYRINTH.md §11 planned one `labyrinth` secondary; with the rings, the
rooms and the heart drawn it needs about 800 tiles, so it is split by map, as Emporion was
with Isthmos. Both draw **the house and the rings' floor at the same metatile ids** (rows
0-12 and 36-38 of the sheet), so a ring's walls, floor, thread twins, anchor rings and
stairs are the same numbers whichever it uses.

| Tileset | Maps |
|---|---|
| `labyrinth` (`gTileset_Labyrinth`) | Ring I (the Threshold), Ring II (the Runner's Ring), Ring III (the Mysteries), Daedalus's workshop, Ring V (the Hunt), Minos's tomb, the Icarus Shaft |
| `mychos` (`gTileset_Mychos`, "the innermost part of a house") | Ring IV (the Masks: the Titans' barracks and mess hall), Ring VI (the Forge: the forge, the Hall of Dials), the archive, the vault, the Mistress's shrine, Ring VII (the Choros), the Starry Chamber |

Both pair with `oikos` (any interior primary works: they use only their own tiles and
palettes 6-12, and every bottom layer is opaque).
"""

THREAD = """\
## The rings' floor and Ariadne's thread

**The floor.** The rings are "the same stone in the dark": the workshop's gypsum slabs one
shade down, in the same running bond. **Lay `thread` `dark_l` where x + y is even and
`dark_r` where odd** (`labyrinth_tiles.floor(x, y)`). Ring VII and the Starry Chamber are
starlit marble, `marble` (mychos), one square slab a cell, with no parity.

**The twins.** Each floor is followed by its ten thread twins, in the engine's order
(ENGINE_API.md §6, `src/ichor_labyrinth.c` SHAPE_*): `h`, `v`, `ne`, `nw`, `se`, `sw`,
`cap_n`, `cap_s`, `cap_w`, `cap_e` (corners by the two sides they join, caps by the one). So
a ring's ON_LOAD registers each floor with its first twin right after it:

{thread_table}

The thread is drawn as an overlay in the middle layer, a twisted two-ply red cord a little
up and left of the cell's middle with its shadow down and right, so every floor's twins
share the same ten thread tiles (the skylight pools' and the marble's cost no thread tiles
of their own). In the glow set the thread shows faintly.

**Every walkable cell of a threaded ring must be a registered floor or a bronze ring.** The
engine lays thread only onto registered floors and anchors; step onto anything else (the
workshop's slabs, dust, a decorated slab) and the thread waits at its end until the player
comes back to it. So every passage a piece opens (a gate, a seal, a dial's wall, a breach)
opens onto plain ring floor for its parity, and decorations stand on cells that block.
Stairs, doorways and the dancing floor are deliberate thread stops.

**Anchors.** `anchor` (house) is a bronze ring lying in its socket: register its cell with
`Ichor_AddThreadAnchor`. Thread is never drawn over it. `anchor_odd` on the odd parity.
"""

BEHAVIORS = """\
## Collision and behaviors

The walk grids below give the collision to paint (`X` blocks, `.` passes, `D` is a door).
Behaviors other than `MB_NORMAL`:

| Behavior | On |
|---|---|
{behavior_rows}

Braziers, the hearth, dials, seals, gates, the bell, the lift, the heal bed and the shrine
are scripts on their cells (bg events); the beam is `Ichor_TraceBeam` (mychos).
"""

VARIANTS = """\
**Variant sets** (in `porytiles_bin/`, written by the build; load over palettes 6-12):

| Set | Tileset | When | What it does |
|---|---|---|---|
| `glow/` | both | The torch doused (SYSTEMS.md §2) | Black but for the glow paint (the latent `lg`: by torchlight the wall tops' dark stone, doused a pale aqua), the flames, and Ariadne's thread, faint ("your own thread shows faintly when doused"). Daedalus's glow-marks (`glow`, labyrinth) are painted on the wall tops. `gTilesetPalettes_LabyrinthGlow`, `gTilesetPalettes_MychosGlow`. |
| `dawn/` | labyrinth | Scene L: the workshop's dawn, and the Icarus Shaft | Every color dimmed and cooled toward a grey morning but the dawn light (`ld0`, `ld1`) and the first light (`lw1`): the room goes dim and blue and the open shaft blazes. `gTilesetPalettes_LabyrinthDawn`. |

None is wired into the engine yet: world-act3 loads them (one `LoadPalette` over 6-12).
"""

ANIMS = """\
**Animations** (Porytiles, one step every 16 frames; `InitTilesetAnim_PorytilesManaged_*`
in `src/tileset_anims.c`):

| Tileset | Animation | Frames | On |
|---|---|---|---|
| labyrinth | `flame` | 3 | the lit braziers' and the threshold hearth's flames |
| mychos | `flame` | 3 | the Titans' oil lamps |
| mychos | `forge` | 3 | the furnace's mouth |
| mychos | `stars` | 4 (a 16-step twinkle) | the Starry Chamber's water: the star-clock's stars reflected, brightening and fading |
"""


def thread_table(data):
    rows = ["| Floor | Tileset | Metatile | First twin | Behavior |", "|---|---|---|---|---|"]
    for ts, d in data.items():
        for s in d:
            for name, mid in (s.get("runs") or {}).items():
                beh = "MB_ICHOR_LIGHT_POOL" if name.startswith(("sun", "moon")) else "MB_NORMAL"
                rows.append(f"| `{s['key']}` `{name}` | {ts} | 0x{mid:03X} | 0x{mid + 1:03X} | {beh} |")
    return "\n".join(rows)


def behavior_rows(data):
    """One row per behavior: where it is, as runs of consecutive ids per piece."""
    seen = {}
    for ts, d in data.items():
        for s in d:
            ids = []
            for c, mb in (s.get("behaviors") or {}).items():
                if mb == "MB_NORMAL":
                    continue
                x, y = map(int, c.split(","))
                seen.setdefault(mb, {}).setdefault(f"{ts} `{s['key']}`", []).append(s["ids"][y][x])
    rows = []
    for mb, pieces in sorted(seen.items()):
        parts = []
        for piece, ids in pieces.items():
            ids = sorted(ids)
            runs, start, prev = [], ids[0], ids[0]
            for v in ids[1:] + [None]:
                if v is not None and v == prev + 1:
                    prev = v
                    continue
                runs.append(f"0x{start:03X}" if start == prev else f"0x{start:03X}-0x{prev:03X}")
                if v is not None:
                    start = prev = v
            parts.append(f"{piece} {', '.join(runs)}")
        rows.append(f"| `{mb}` | " + "; ".join(parts) + " |")
    return "\n".join(rows)


def section_list(A, tileset):
    out = []
    for row, key, title, blurb in A.SECTIONS[tileset]:
        out.append((key, title, blurb, row))
        for sub, (parent, stitle, sblurb) in A.SUBSECTIONS.items():
            if parent == key and tileset == "labyrinth":
                out.append((sub, stitle, sblurb, None))
    return out


def catalog(A, tileset, data, budget, sections_counts):
    out = []
    by_key = {s["key"]: s for s in data}
    by_sec = {}
    for s in data:
        by_sec.setdefault(s["section"], []).append(s)
    out.append("## Catalog\n")
    out.append("Each grid lists metatile ids as Porymap shows them, with the collision beside "
               "it. Each section starts on a fixed row of the sheet, so adding to one never "
               "renumbers another: " + ", ".join(
                   f"{key} at 0x{0x200 + row * 8:03X}" for row, key, *_ in A.SECTIONS[tileset])
               + ". `build/" + tileset + "/catalog.json` and `tools/ichor/maps/labyrinth_tiles.py` "
               "name every part (`names`), so a map builder can place pieces by key and name, "
               "never by raw id. Odd twins are listed with their even twin.\n")
    for key, title, blurb, row in section_list(A, tileset):
        out.append(f"### {title}\n\n{blurb}\n")
        for s in by_sec.get(key, []):
            if s["key"].endswith("_odd"):
                twin, r0 = s.get("twin_of") or [s["key"][:-4], 0]
                rows = ("" if s["h"] == len(by_key[twin]["ids"]) else
                        f" of row{'s' if s['h'] > 1 else ''} "
                        + "-".join(str(r) for r in sorted({r0, r0 + s["h"] - 1})))
                out.append(f"`{s['key']}`: the odd twin{rows}, ids "
                           + "; ".join(" ".join(f"0x{v:03X}" for v in r) for r in s["ids"])
                           + ".\n")
                continue
            block = structure(s)
            block[0] = block[0].replace("### ", "#### ")
            beh = {mb for mb in (s.get("behaviors") or {}).values()
                   if mb not in ("MB_NORMAL", "MB_NON_ANIMATED_DOOR", "MB_COUNTER")}
            if beh:
                cells = []
                for c, mb in sorted(s["behaviors"].items()):
                    x, y = map(int, c.split(","))
                    if mb in beh:
                        cells.append(f"0x{s['ids'][y][x]:03X}")
                if len(cells) > 6:
                    block.append(f"Behavior: {', '.join(sorted(beh))} on every cell.\n")
                else:
                    block.append(f"Behavior: {', '.join(sorted(beh))} on {', '.join(cells)}.\n")
            if s.get("anims"):
                block.append(f"Animated: {', '.join(s['anims'])}.\n")
            out += block
    return out


LAB_INTRO = """\
# Labyrinth tilesets: `labyrinth` and `mychos`

Daedalus's Labyrinth under Knossa (LABYRINTH.md §4-§11). This file is the `labyrinth`
tileset's catalog and the plan for both; `TILES_mychos.md` is its sister's catalog.

- **The house**: the workshop's slab floor, the vaulted arcade, and now the rings' corridor
  walls as an autotile, the bronze anchor rings and the stairs from ring to ring.
- **The rings' floor**: the slabs in the dark with Ariadne's thread, 20 twins.
- **Daedalus's workshop** (scenes D and L), unchanged.
- **The outer rings**: Ring I's braziers and threshold hearth, Ring II's sun and moon gates
  and Asterion's cracked walls, Ring III's webs and glow-marks, Ring V's skylight pools,
  niches and the fresco of the dance's steps 4-6; labrys seals and doorways.
- **Minos's tomb** (scene F) and **the Icarus Shaft** (scene L).

![A ring corridor: the thread laid from an anchor, a brazier lit](img/labyrinth_scene_ring.png)

![The same in the dark: the torch's radius, the brazier's lit zone](img/labyrinth_scene_ring_dark.png)

![The same doused: the glow set](img/labyrinth_scene_ring_doused.png)

| Image | Shows |
|---|---|
| `img/labyrinth_scene_ring.png` | One 15 x 10 screen of a ring: corridors walled with the autotile, the thread laid from a bronze anchor ring to the player, a brazier lit in its alcove, the stair down, a cracked face, webs, glow-marks (by torchlight, the stone) |
| `img/labyrinth_scene_ring_dark.png` | The same as the player sees it: the torch's 3.5-tile radius (flash level 3) and the brazier's zone, lit for good |
| `img/labyrinth_scene_ring_doused.png` | The same with the torch doused (the `glow/` set): the flames, the thread faintly, Daedalus's labrys signs |
| `img/labyrinth_scene_hunt.png`, `_hunt_night.png` | Ring V by day and by night: the loop's corridor, a skylight pool across it (sun, then moon) with the thread through it, niches and the niche shrine, a cracked wall, the fresco of steps 4-6 in a bay |
| `img/labyrinth_scene_tomb.png` | Minos's tomb (scene F): the bier and the cap on it, the inscription, labrys stands, painted pillars, jars, dust and old footprints |
| `img/labyrinth_scene_shaft.png` | The top of the Icarus Shaft with the `dawn/` set (scene L): the courses brightening to the lip and the morning sky |
| `img/labyrinth_scene_workshop.png`, `_dawn.png` | Daedalus's workshop, scenes D and L (the first batch) |
| `img/labyrinth_scene_*_pass1.png`, `_pass2` | The earlier render-and-critique passes; the unsuffixed images are the last |
| `img/labyrinth_pieces.png`, `img/labyrinth_sheet.png` | Every structure as drawn; every metatile with its id, from the compiled tileset, on `oikos` |
| `img/labyrinth_scene_forge.png`, `_choros.png`, `_starry.png` | The sister tileset's scenes (TILES_mychos.md) |

{split}
## How it is made

- `tools/ichor/art/labyrinth_art.py` holds the palette plan, the house's masonry and the
  sheet's sections for both tilesets; `labyrinth_kit.py` the rings' house kit (walls,
  floors, thread, anchors, stairs); `labyrinth_workshop.py` the workshop;
  `labyrinth_rings.py` the outer rings' fixtures and the fresco painter; `labyrinth_deep.py`
  the tomb and the shaft; `mychos_titans.py` and `mychos_heart.py` the sister's.
- `tools/ichor/art/labyrinth_build.py [labyrinth|mychos|all]` draws, compiles (Porytiles,
  in a scratch project against an empty stand-in primary), registers the tilesets and their
  animations in `src/`, writes the variant palette sets, verifies, and rewrites these files
  and `tools/ichor/maps/labyrinth_tiles.py`. `labyrinth_scene.py` renders the mock scenes.
- Run both with `/usr/bin/python3`.

**Layers.** Floors and walls fill the bottom layer; objects stand in the middle layer over
them, so a piece on the floor costs its object tiles once and its odd twin nothing.
Nothing is drawn over sprites.

**Floor parity.** The slabs are two cells long, in a running bond: `slab_l` / `dark_l`
where x + y is even, `slab_r` / `dark_r` where odd. So every piece standing on a slab floor
comes as **twins**, `<key>` for a top-left cell where x + y is even and `<key>_odd` where
odd; they share every object tile. Where only some rows of a piece show floor, `<key>_odd`
holds just those rows; the catalog says which. `labyrinth_tiles.piece()` picks the twin.

**Walls.** `walls` (house) is an autotile. Every wall cell is a *top* (the masonry's dark
top, rim-lit where it meets a corridor: a dark seam, a lit edge, a bevel) or a *face* (the
wall seen from the south, one row tall: a coping over two courses of ashlar). A face is a
wall cell with floor south of it. Paint a wall/floor grid and let
`labyrinth_tiles.autotile(grid)` choose each cell: tops are named by the sides that meet
floor and their inner corners, faces by their two ends (`o` open, `c` continuing, `i`
meeting a wall that turns down beside them). Walls one cell thick work either way. Rooms
can still take the arcade's three-row north wall (the archive, the forge, the frescoes).

{thread}
{behaviors}
## Palettes

LABYRINTH.md §11's seven palettes, the same in both tilesets: six slots plus timber and
papyrus, with glow as a palette *variant* set (as planned in the first batch). Every 8x8
tile draws from one group (`labyrinth_art.GROUPS`), all colors multiples of 8.

| Group | §11 name | For |
|---|---|---|
{palette_rows}

{variants}
{anims}
## Tile budget

| Tileset | Tiles used | Of 504 | Left |
|---|---|---|---|
{budget_rows}

The door animations own tiles 504-511, and the build fails past 504. By section (distinct
tiles a section adds, before Porytiles packs palettes; animated tiles counted once):

| Tileset | Section | Tiles |
|---|---|---|
{section_rows}

How they keep to it:
- The thread is an overlay: ten tiles serve every floor's twins.
- Every piece on a slab floor stands in the middle layer, so its odd twin costs nothing
  (the first plan's warm halos round braziers and lamps doubled every twin, and went).
- Patterns repeat on the 8 px grid (the archive's pigeonholes, the inscription's signs, the
  shaft's courses, the grates), and symmetric pieces (the beam, the dancing floor's squares,
  the star-clock's ring, the stairs) are stored once and flipped.
- Cracks, glow-marks and dust are overlay tiles shared by every wall or floor they're on.
- Any tile within two pixels of another is redrawn as that tile.

**Metatiles.** A secondary holds 512: labyrinth uses {lab_meta}, mychos {my_meta}.

## Notes for the ring builders (world-act3)

- **Registering a ring.** In ON_LOAD: `Ichor_AddThreadFloor` for `dark_l` and `dark_r`
  (and Ring V's pool pair, or Ring VII's `marble`), `Ichor_AddThreadAnchor` for each
  `anchor`, `Ichor_AddCrackedWall` for each `cracked` cell with its parity's floor as the
  broken metatile, then draw broken walls and their `breach_l` / `breach_r` edges by flag,
  dials, gates, then `Ichor_DrawThread` last.
- **Ring V's pools.** By day the pools' cells are `pools` `sun_l` / `sun_r`, by night
  `moon_l` / `moon_r` (gettimeofday in ON_LOAD); register whichever pair is down (four
  floors is the engine's limit). Every pool cell and its twins carry `MB_ICHOR_LIGHT_POOL`.
- **Two engine notes.** (1) Thread drawn over a wall the Turning or a dial put on a
  committed tile uses the *first* registered floor's twins whatever the cell's parity, so a
  forced-open cell on an odd cell shows a slab's left half beside another left half: a
  one-line fix in `DrawThreadTile` would pick `dark_r` on odd cells. (2) The beam's
  metatiles (mychos) aren't registered floors, so the thread stops at a lit beam in Ring
  VII's antechamber until the player steps back; the antechamber can stay unthreaded.
- **Darkness.** Rims mark every wall in the torch's radius; every brazier, the hearth, the
  pools and the lamps are landmarks. A lit brazier's zone is a lit zone (SYSTEMS.md §2).
  The GBA's flash window shows one circle, so on a dark ("cave") map a skylight pool
  outside the torch's radius is black like the rest: for Ring V's pools to read as light
  from across the dark (LABYRINTH.md §5.2), make each pool's surround a lit zone, as the
  mock `hunt_night` shows it, or give the ring a lit header with the darkness in its art.

## Weak spots and open questions

- **No sprites yet** for Daedalus, Hyperion, Kronos, Rhea, Asterion, the mirrors or the
  crystal: the scenes stage around them. The mirrors are objects
  (`MOVEMENT_TYPE_ICHOR_MIRROR*`); the tiles give their bases and the beam's corners.
- **The corridor walls are one row tall**, lower than the workshop's three-row arcade:
  readable mazes at the cost of height. Big rooms can use the arcade.
- **Ring floors are uniform**: a threaded ring can't scatter decorated slabs on its walkable
  cells (they'd stop the thread), so its landmarks are the blocking pieces.
- **The Icarus Shaft** is a stylised side view of its back wall, five light levels from the
  grate to the sky; load the `dawn/` set there.
- **Small things at 1x**: the glow-marks, the dance's symbols in the frescoes and the
  inscription's signs are a few pixels; the object text carries them.
- **The budget**: both tilesets have about a dozen tiles left. A third secondary (the
  heart alone) is the release valve.

## Ring by ring

| Ring | Pieces |
|---|---|
| All | `walls` (autotile), `thread` `dark_l` / `dark_r`, `anchor`, `stairs`, `doorways` (jambs, the labrys seal, a grate) |
| I, the Threshold (labyrinth) | `hearth` (the threshold hearth), `brazier` (B1-B5 and the gate brazier G, cold and lit), `doorways` for the fresco door |
| II, the Runner's Ring (labyrinth) | `doorways` `sun` and `moon` (the gates), `grate` (the Long Hall's lattice), `cracked` (scene C's breach), the bronze plates are the floor (scripts) |
| III, the Mysteries (labyrinth) | `webs` (anchors either side of the web objects), `glow` (Daedalus's trail), `brazier` |
| The workshop (labyrinth) | its own section (scenes D and L) |
| IV, the Masks (mychos) | `bunk`, `helmets` (the disguise), `armory`, `mess_table`, `banners`, `lamp_stand` (the sentry posts), `grates`, `fresco_iv` (steps 1-3) |
| V, the Hunt (labyrinth) | `pools` (four skylight pools, sun and moon), `niche` (back, shrine), `cracked` (%1, %2, %3), `fresco_v` (steps 4-6) |
| Minos's tomb (labyrinth) | `tomb_pillar`, `tomb_bier` (the Helm on it; `head_empty`), `tomb_inscription`, `tomb_goods` (labrys stand, jar, dust) |
| VI, the Forge (mychos) | `forge`, `anvil` (Hyperion's), `forge_kit` (bellows, tub, runnels, mold, slag), `dials` (dials A and B, swinging walls, the reset lever), `archive`, `archive_desk`, `vault`, `shrine`, `fresco_vi` (steps 7-9) |
| VII, the Choros (mychos) | `marble`, `beam` (sun and star, mirror bases), `dance` (the 5 x 5 floor and its stair), `fresco_faded` and `fresco_iv`/`_v`/`_vi` (the whole dance) |
| The Starry Chamber (mychos) | `marble`, `basin` (the lustral pool, twinkling), `clock` (the star-clock's ring), `horns`, `star_anvil` |
| The Icarus Shaft (labyrinth) | `icarus` |
"""

MY_INTRO = """\
# Labyrinth tileset: `mychos`

`gTileset_Mychos` ("the innermost part of a house") is the Labyrinth's sister tileset: the
Titan wing (Rings IV and VI, the archive, the vault, the Mistress's shrine), Ring VII (the
Choros) and the Starry Chamber. Its house and floor sections are `labyrinth`'s, at the same
ids. **The plan for both, the thread, the walls, palettes, budget and notes for the ring
builders are in [TILES_labyrinth.md](TILES_labyrinth.md).**

![Ring VI's forge: the furnace, Hyperion's anvil](img/labyrinth_scene_forge.png)

![Ring VII: the mirrors' beam and the dancing floor, four steps danced](img/labyrinth_scene_choros.png)

![The Starry Chamber: the black basin under the star-clock](img/labyrinth_scene_starry.png)

| Image | Shows |
|---|---|
| `img/labyrinth_scene_forge.png` | Ring VI's forge (scene G), one screen: the furnace roaring in its wall between sickle banners, Hyperion's anvil, the bellows, the quench tub, a runnel of bronze into its mold, slag, a grate, the Titans' lamps |
| `img/labyrinth_scene_choros.png` | Ring VII (scene I, §5.7): the fresco of the whole dance along the north wall, the starlight beam from the shaft by three mirror bases to the floor's edge, the dancing floor revealed, E5-E2 danced |
| `img/labyrinth_scene_starry.png` | The Starry Chamber (scene J): the lustral basin full of the star-clock's stars (they twinkle in game), its gold-and-lapis ring, the anvil with the three fragments, the pillar of horns, the stair down from the Choros |
| `img/labyrinth_scene_*_pass1.png`, `_pass2` | The earlier passes |
| `img/mychos_pieces.png`, `img/mychos_sheet.png` | Every structure as drawn; every metatile with its id, from the compiled tileset |

"""


def main(tileset="labyrinth", tiles_used=None, structs=None):
    sys.path.insert(0, str(ROOT / "tools/ichor/art"))
    import labyrinth_art as A
    data = {}
    for ts in ("labyrinth", "mychos"):
        p = ROOT / f"build/{ts}/catalog.json"
        if p.exists():
            data[ts] = json.loads(p.read_text())
    budget = {}
    bp = ROOT / "build/labyrinth_budget.json"
    if bp.exists():
        budget = json.loads(bp.read_text())
    if tiles_used is not None:
        budget[tileset] = budget.get(tileset, {})
        budget[tileset]["used"] = tiles_used
    if structs is not None:
        budget.setdefault(tileset, {})["sections"] = section_counts(structs)
    bp.parent.mkdir(parents=True, exist_ok=True)
    bp.write_text(json.dumps(budget, indent=1))
    group_name = {g: (name, use) for g, name, use in PALETTES}
    palette_rows = "\n".join(f"| {g} | {group_name[g][0]} | {group_name[g][1]} |"
                             for g in A.GROUPS)
    budget_rows = "\n".join(f"| {ts} | {b.get('used', '?')} | 504 | "
                            f"{504 - b['used'] if 'used' in b else '?'} |"
                            for ts, b in budget.items())
    section_rows = "\n".join(f"| {ts} | {sec} | {n} |" for ts, b in budget.items()
                             for sec, n in b.get("sections", {}).items())
    meta = {ts: sum(len(s["ids"]) * len(s["ids"][0]) for s in d) for ts, d in data.items()}
    lab = LAB_INTRO.format(split=SPLIT, thread=THREAD.format(thread_table=thread_table(data)),
                           behaviors=BEHAVIORS.format(behavior_rows=behavior_rows(data)),
                           palette_rows=palette_rows, variants=VARIANTS, anims=ANIMS,
                           budget_rows=budget_rows, section_rows=section_rows,
                           lab_meta=meta.get("labyrinth", "?"), my_meta=meta.get("mychos", "?"))
    docs = {}
    if "labyrinth" in data:
        docs["labyrinth"] = [lab] + catalog(A, "labyrinth", data["labyrinth"], budget, None)
    if "mychos" in data:
        docs["mychos"] = [MY_INTRO] + catalog(A, "mychos", data["mychos"], budget, None)
    for ts, out in docs.items():
        doc = ROOT / f"design/phase4/TILES_{ts}.md"
        doc.write_text("\n".join(out).rstrip() + "\n")
        print(doc)


def section_counts(structs):
    """Distinct tiles each section adds, in build order (static, then animated keys)."""
    import labyrinth_build as LB
    seen, out = set(), {}
    for s in structs:
        occ = set(LB.static_tiles([s]))
        anim = {k.tobytes() for k, _ in
                (t for tiles in LB.collect_anims([s]).values() for t in tiles)}
        new = (occ | anim) - seen
        seen |= occ | anim
        out[s.section] = out.get(s.section, 0) + len(new)
    return out


if __name__ == "__main__":
    main(*(sys.argv[1:2] or ["labyrinth"]))
