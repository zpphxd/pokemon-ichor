# Egypt's towns: Naukratis, Pharos, the Delta Reeds, Memphis (batch 1, egypt-towns)

Built by code: `tools/ichor/maps/naukratis.py`, `pharos.py`, `delta_reeds.py`, `memphis.py`
(shared code in `egypt_lib.py`), on `aethos` + `kemet` (`tools/ichor/art/kemet_*.py`,
catalog in `TILES_kemet.md`). Each builder writes its layout and map.json and checks it.

## The tileset

`gTileset_Kemet`: 491 of 504 tiles, 424 metatiles; the seven palette groups (nile, reed,
stone, paint, brick, hellas, goods) are full. Sheet rows 53-63 are free for batch 2, but
only about 13 tiles are: batch 2's Pyramid Field may need a sister tileset (as Emporion
and Isthmos split). Houses are a kit of parts (roofs and their furniture, whitewashed and
bare-brick walls, doors), so every household is a recipe.

## Seams

| Edge | Joins | Open cells |
|---|---|---|
| Pharos north | Route 34 (world-postgame), not yet connected: ICHOR_STUB_AETHOS | row 0 water at x 2-33 (sea rocks in the corner columns); rows 0-5 aethos-only. **Pharos is 36 wide**, for Route 34's offset |
| Pharos south / Naukratis north | each other, offset 0 | water at x 5-30 |
| Naukratis south / Delta Reeds north | offset 2 / -2 | Naukratis x 16-18 = Delta x 14-16 |
| Delta Reeds south / Memphis north | offset -4 / 4 | Delta x 14-16 = Memphis x 18-20 |
| Delta Reeds east | the Papyrus Shallows Nursery (map `PapyrusShallows`, batch 2) | rows 23-25 at x 31, fenced shut at x 29 (keeper, sign) |
| Memphis south | the Nile and the Pyramid Field (batch 2), not connected | x 0-39 open; rows 30-35 aethos-only |

## Landing tiles, doors, ids, flags

- Wings landing: Naukratis (13,14), Memphis (13,10), outside each Asclepeion.
- Doors, warp ids 0-6 (Naukratis: Asclepeion (13,13), Agora (20,13), field station (3,17),
  egg-ovens (7,21), incense (13,21), potter (22,22), net-loft (3,12)); 0-4 (Memphis:
  Asclepeion (13,9), Agora (24,9), Apis keepers (4,9), scribe (4,20), embalmer (10,20)).
  The pylon of Proteus (32,20) is solid, with a guard: ICHOR_STUB_HALL.
- Trainers 700-708 (Delta Reeds), 709-713 (Pharos), 935-936 (Memphis's desert road).
- Bank flags 0x404-0x40F (item balls, two gifts); vanilla 0x4C8-0x4CF (eight hidden items).

## ICHOR_STUB_HIDDEN

Hidden items the standard wants but no vanilla flag is left for:
- Naukratis (26,20), the Hellenion's court: Stardust.
- Memphis (16,22), under the sphinx's paw: Stardust.

## Stand-ins

| Who | Intended | Stand-in |
|---|---|---|
| Egyptian men / women | `_EGYPTIAN_M` / `_EGYPTIAN_F` | `MERCHANT`, `MAN` / `YOUTH_F`, `WOMAN`, `ELDER_F` |
| Nile boatmen | `_NILE_BOATMAN` | `SAILOR`, `FISHER`, `HARVESTER`; class Sailor / Fisherman / Swimmer F |
| Priests of the Sun | `_SUN_PRIEST` | `AUGUR`, `PRIESTESS`; class Augur |
| Scribe of Thoth | `_SCRIBE` | `ACOLYTE_M`; class Psychic |
| Embalmers | `_EMBALMER` | `ELDER_M`, `ELDER_F`; class Hex Maniac |
| Phoenician traders | — | `MERCHANT`, `HOPLITE`; class Expert |
| Proteus, Helen | `_PROTEUS`, `_HELEN` | not placed (batch 2's hall) |

Every party carries an `ICHOR_STUB_CLASS` comment. Intended song: *The Black Land*
(ICHOR_STUB_MUSIC: `MUS_ICHOR_EMPORION` in the towns, `MUS_ICHOR_ROAD` on Pharos and the
Delta Reeds).

## Render-and-critique passes

**Naukratis.** Pass 1: structure right (quay, one stair, Asclepeion and Agora facing the
square, the Hellenion); the south half was empty and the quay rendered as backdrop (a stale
tileset). Pass 2: map cut to 34 rows, canal with a shaduf, clay pit, papyrus edges; quay
fixed. Still to do: the quay is a wide blank; it wants goods and people.

**Pharos.** Pass 1: the island was small and its edges are aethos's shallow-water ring, so
items stood in the surf. Pass 2: bigger island, a south cove, a sandbar on the north strip,
the herd on the north beach, corners matched to Naukratis's basin.

**The Delta Reeds.** Pass 1: the canal let walkers and surfers skip the narrows. Pass 2:
three pools instead, thickets everywhere between; three forced bands (3, 4, 4 deep), three
narrows that can't be skirted, 31% optional reeds, every dead end pays.

**Memphis.** Pass 1 only: walls, gates, pylon, sphinx, households, herd pen. Not yet
critiqued.

## Stopped at

Paused by the coordinator on 2026-11-14 (usage limit; the main story first).

**Done**
- `kemet` drawn, compiled (491/504 tiles) and registered.
- All four maps built by code, passing their builders' checks; Delta Reeds proves its
  bands and sight lines.
- Scripts for all four maps (signs, people, Alethea's quay scene, Nausikles, two gifts,
  the rest point, 16 trainers); trainers 700-713 and 935-936 with parties; wild tables for
  the Delta Reeds (Morning/Day/Evening/Night land, surf, fishing), Pharos (the same) and
  Naukratis (surf, fishing); flags claimed.

**Partial**
- Render-and-critique: two passes on three maps, one on Memphis (three wanted each).
- `map_audit.py`: last run before the wild tables and trainers went in. Open there: rooms'
  warps and residents (the egypt-rooms agent's maps); two town hidden items (no flags, see
  ICHOR_STUB_HIDDEN). Augur's Eye hidden slots not added (adding the `hidden_mons` field
  redefines `NUM_HIDDEN_MONS_ENCOUNTER_SLOTS` in the template; needs the lead's call).
- Art polish: the sphinx's head, the thicket's regularity.

**Not started**
- `tools/ichor/tests/egypt_towns.sh` and `.lua`.
- Text measurement with `text_width.py`.
- 2x renders in `design/oikoumene/img/` (renders so far are in the scratchpad only).
- The smoke test.

**make:** green at the WIP commit (exit 0; ROM 22,367,656 B of 32 MB, 66.66%). Smoke and slice tests not run.
