# The Labyrinth's heart: Rings V–VII, the Starry Chamber, the Icarus Shaft

Built by `tools/ichor/maps/labyrinth_heart.py` (layouts, events, generated ON_LOAD) with
`heart_lib.py`, `heart_extras.py` and the `mychos`/`astra` tilesets (`tools/ichor/art/mychos_build.py`).
Rerun `/usr/bin/python3 tools/ichor/maps/labyrinth_heart.py` after any change; it prints
LABYRINTH_MAZE §2's counts and writes the per-ring extras log to `build/<Map>_extras.md`.

## Briefs

**Ring V, the Hunt** (`LabyrinthRing5`, 56×48, mychos, dark)
- **Sentence:** an underground lake in a cavern older than the palace, a paved ring road round it, and a bull walking the road.
- **Model:** the Minoan palace's deep basements broken into karst (Skotino's lake chamber), the processional road of the Royal Road.
- **Logic:** the Titans' grated gallery looks down on the water and never goes down; caves wrap the road; the dark south is reached only across his road.
- **Reveal:** from the gallery, four shafts of daylight lying on the black water.
- **Signature:** Asterion's loop (his 16×16 patrol), the corner spurs into cracked walls.

**Ring VI, the Forge** (`LabyrinthRing6`, 48×48, mychos, firelit)
- **Sentence:** Team Titan's headquarters, a built maze of swinging bars round a magma cavern where the house's stream falls.
- **Model:** a bronze foundry in the rock (Kaldera's Telchines forge), the Knossos magazines, Daedalus's automata.
- **Logic:** the dials' hall in the middle, archive east, vault north-east, forge west, barracks and sealed landing south.
- **Reveal:** the forge cavern: the furnace, Hyperion's anvil, the magma lake, the falls.
- **Signature:** the three-dial combination lock.

**Ring VII, the Choros** (`LabyrinthRing7`, 32×32, astra, starlit)
- **Sentence:** Ariadne's dancing floor under a natural dome set with crystal stars, in a braided cave.
- **Model:** Homer's *choros* at Knossos (Iliad 18.590), the Theatral Area's paving, Delos's crane dance.
- **Logic:** stair in from the north, the dome in the middle, the mirrors west of the floor, the teaching mirror north-east.
- **Reveal:** the beam lights the floor and the fresco of the whole dance at once.
- **Signature:** the crane dance (E5 spiralling to C3).

**The Starry Chamber** (`LabyrinthStarryChamber`, 20×20, astra) — a round cave whose rock is crystal stars, a marble floor round the star-clock and the black lustral basin, the pillar of horns, the anvil. Scene J.

**The Icarus Shaft** (`LabyrinthIcarusShaft`, 10×40, astra) — a natural chimney with Daedalus's cut footholds, crystal ledges, sky at the top. Scene L's flight; ends in the palace court (`MAP_KNOSSA_PALACE` 31,23), `FLAG_ICHOR_ICARUS_FLIGHT`, `VAR_ICHOR_KNOSSA` 19, `VAR_ICHOR_ACT3` 6.

## Maze counts (LABYRINTH_MAZE §2, from the builder)

| Ring | Junctions / screen | Loops | Dead ends | Longest straight run |
|---|---|---|---|---|
| V | 3.0 | 7 | 23 (rewarded, niches, refuges) | 7 |
| VI | 3.6 | 21 | 23 | 8 |
| VII | 3.8 | 5 | 8 | 7 |

Graph: each ring is fixed architecture plus a braided lattice maze (`maze()`), short stubs pruned and
the rest braided into loops (`prune`, `braid_dead_ends`); long runs get alcoves (`break_long_runs`).

## Relics, puzzles, treasure, the lost (the user's 2026-11-17 direction)

| Ring | Must use | Optional | Seal / combination | Treasure down | Remains |
|---|---|---|---|---|---|
| V | Labrys chains on all three ways down from the gallery; Hammer rubble on both crossings south (or lure Asterion through %2) | Surf the lake to the island (Hammer the fallen block there); the Helm's stealth in the dark south | Daedalus's floor seal: two drums onto two plates (Girdle), reset lever; luring Asterion's charge from a pool through %1-%3 | stair to a Titan cache (TM Shadow Ball); hole to a sump (Relic Gold) | 4: the tribute token, the spear caked with bull hair, the goad and Hyperion's order to keep him hurting, the explorer who meant to try the bell |
| VI | the Labrys dials (teaching dial, then the B A B forge combination); Hecate's Torch on two webs across the forge corridor | Waterfall up the falls past the forge (PP Up); Hammer slag | the three-dial combination lock | stair (Relic Crown); hole (PP Max) | 3: the Kaldera smith's note about the "mule's" adamant collar, a grunt's letter home, a toppled automaton |
| VII | Labrys chains and Torch webs across the stair to the dome | the Girdle drum on the fresco corridor | the three mirrors and the crane dance | stair (Relic Statue); hole (TM Psychic) | 3: a tribute girl's sandal, THESE- cut in the rock, a Titan's note about the dark floor |

Awe: the lake cavern from the gallery (a scripted look, the first time), the forge cavern (Scene G), the dome (Scene I), the star-ceilinged chamber (Scene J).

## Seams (see Labyrinth_System.md)

Ring V warps: 0/3 stair up ↔ Ring IV warp 6; 1/4 the tomb stair ↔ tomb warp 0; 2 arrival in the lake (Ring IV's chute); 5/6 down to Ring VI 0/1; 7 rope up to Ring IV 6; 8 rope down to Ring VI 4; the sinkhole (45,44) drops to Ring VI's east caves. Ring VI 2/3 → Ring VII 0/1. Ring VII's dance stair (16,18) → Starry Chamber 0.

## Known gaps

- Ring V has no trainers by design (LABYRINTH §4: Asterion is its checkpoint) and Ring VII's Gigas are a scripted double, so `map_audit.py` reports "trainers in the whole dungeon" for both.
- The Turning is built (Labyrinth_System.md, The Turning). Rings VII and VI's sealed halls are few: their loops leave few
  dead-end pockets, and Ring VII's escape (the dome to the stair) is too short for a breakthrough.
- Scene J's bull-leaps now run on the west lane below the basin, (4,12) to the line at (8,12); the old lane started
  the bull eight rows off, outside the object window, so the special found no bull and every leap was late.
- The Starry Chamber's way in lands at the stair's foot (warp 3), and the stair out is a trigger: landing on the
  north-arrow stair in the south wall sent a player who walked north straight back up.
- Ring VII's double battle now starts (`BattleSetup_StartMultiBattle`, as at Delphoi): `setmultitrainerbattle` alone
  only set it up. Ariadne fights with `TRAINER_PIC_ARIADNE_PARTNER` (a back-pic stand-in, like Rhea's at Delphoi).
