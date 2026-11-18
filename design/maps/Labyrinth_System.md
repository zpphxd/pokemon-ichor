# The Labyrinth as one cave system

The connection diagram LABYRINTH_MAZE.md §3 asks for: every ring, stair, drop, climb, shortcut and the stream, and the warp ids each side promises the other. **Keep it current.** Labyrinth I (Rings I–IV, the workshop, Minos's tomb; tileset `labyrinth`, the workshop on `daidaleion`) and Labyrinth II (Rings V–VII, the forge, the chambers, the Icarus Shaft; tileset `mychos`) both edit it.

```text
                    PALACE: the Grand Staircase (Knossa above ground)
                               | stair             ^ Daedalus's lift (after scene D)
                               v                   |
   +---------------- RING I, the Threshold -------------------+
   |  hall/hearth --- maze --- fresco door --- gate room      |
   |  east cleft (cave) ... HOLE (9,0) ......................+-----+ drop
   |  cleft anchor  <------------------------- flowstone climb |     |
   +-----------------------------+-----------------------------+     |
                                 | stair (G lit)                     |
   +---------------- RING II, the Runner's Ring --------------+     |
   |  sun gate | moon gate --- Long Hall (scene C) --- heralds |<----+ the grotto
   |  Moon Room ... SUNKEN FLOOR ............................+-----+ drop
   |  ~ the trickle in the cleft (the stream begins) ~         |     |
   +-----------------------------+-----------------------------+     |
                                 | stair                             |
   +---------------- RING III, the Mysteries -----------------+     |
   |  webs (front way) | glow-marks (back way, doused)        |<----+ the web pocket
   |  ~~ the stream, surfable, north to south ~~               |
   |  front door --+   back door --+    HOLE in the webs ......+-----+ drop
   +---------------|---------------|---------------------------+     |
                   v               v                                 |
            DAEDALUS'S WORKSHOP (heal, Pithos, lift up)              |
                   | stair                                           |
   +---------------v-- RING IV, the Masks ---------------------+     |
   |  barracks, mess hall, posts --- Enkelados's checkpoint    |<----+ the Titans' dig
   |  the Titans' dig (cave) ~~ the stream ~~ CHUTE ...........+-----+ surf drop
   +-----------------------------+-----------------------------+     |
                                 | stair                             |
   +---------------- RING V, the Hunt (Labyrinth II) ----------+     |
   |  gallery --- Asterion's loop --- the LAKE (skylight pools)|<----+
   |  %1 ---> MINOS'S TOMB (the Helm)                          |
   +-----------------------------------------------------------+
           ... Ring VI (the forge; the stream falls past it), Ring VII, the heart
```

## The seams (warp ids)

Warp ids are each map's `warp_events` index. "Arrival" warps sit on a floor or a bronze ring: they are only landing spots (landing on a ring ties the thread, LABYRINTH §5.1).

| From | Cell | Goes to | Status |
|---|---|---|---|
| Grand Staircase | its stair-foot trigger | Ring I warp 0 (arrival on the threshold ring, (21,2)) | built |
| Ring I warps 1-2 | the stair up (21-22,1) | `MAP_KNOSSA_PALACE_GRAND_STAIRCASE` warp 1 (its dark doorway) | built |
| Ring I warp 3 | arrival on the gate ring (30,26) | — | Ring II's stair up lands here |
| Ring I warps 4-5 | the stair down (30-31,25), grated until G burns | Ring II warp 0 | |
| Ring I warp 6 | arrival on the cleft ring (38,6) | — | Ring II's flowstone climb lands here |
| Ring I hole (38,3) | coord event | Ring II warp 3 (the grotto) | one way |
| Ring II warp 0 | arrival on its entrance ring | — | |
| Ring II warps 1-2 | the stair up | Ring I warp 3 | |
| Ring II warp 3 | arrival in the grotto | — | from Ring I's hole |
| Ring II flowstone climb | coord event in the grotto | Ring I warp 6 | |
| Ring II warps 4-5 | the stair down | Ring III warp 0 | |
| Ring II warp 6 | arrival by its stair down | — | Ring III's stair up lands here |
| Ring II sunken floor | coord event in the Moon Room | Ring III warp 3 (the web pocket) | one way |
| Ring III warp 0 | arrival on its entrance ring | — | |
| Ring III warps 1-2 | the stair up | Ring II warp 6 | |
| Ring III warp 3 | arrival in the sealed web pocket | — | burn out from inside |
| Ring III warps 4 / 5 | the front door (30,37) / the back door (50,13) | Workshop warps 0 / 1 | the front door is sealed until its three floor plates are covered |
| Ring III warps 6 / 7 | arrivals outside each door | — | the workshop's doors land here |
| Ring III hole | coord event in the webs | Ring IV warp 3 (the Titans' dig) | one way |
| Workshop warps 0 / 1 | front door / back door | Ring III's arrivals | |
| Workshop warps 2-3 | the stair down | Ring IV warp 0 | |
| Workshop lift (20,2) | script, after scene D | Grand Staircase warp 1 | built; the staircase's lift down lands on workshop warp 5 (20,3) |
| Workshop warp 4 | arrival below the stair (6,3) | — | Ring IV's stair up lands here |
| Ring IV warps 4-5 | the stair down at Enkelados's checkpoint | Ring V warp 0 | built |
| Ring IV warp 6 | arrival by its stair down | — | Ring V's warps 0, 3 and 7 land here |
| Ring IV stream chute | coord event on the water | Ring V warp 2 | built |
| Ring V warps 1, 4 (Labyrinth II) | the stair into the tomb (44-45,13) | Minos's tomb warp 0 | built |
| Minos's tomb warps 0-1 | the threshold (7-8,10) | Ring V warp 1 | built (the tomb is Labyrinth I's) |

## Shared ids

- **Thread anchor names:** Labyrinth I uses `THREAD_ANCHOR_*` 10-29 (`include/constants/ichor.h`); Labyrinth II, please take 30 and up.
- **Braziers:** Labyrinth I uses `FLAG_ICHOR_BRAZIERS_START + 0x30`-`0x3F`.
- **Map section:** the rings show `MAPSEC_WATER_LABYRINTH`, renamed "LABYRINTH" (the FRLG section, unused by Ichor).
- **Map group:** `gMapGroup_Labyrinth`; add Labyrinth II's maps to it.
- **Tilesets:** `labyrinth` and `mychos` share the house (rows 0-12) and the rings' floor (rows 36-38) at the same metatile ids. `labyrinth` keeps its cave at rows 13-35; Rings I-IV, the tomb. `daidaleion` holds the workshop and **the Icarus Shaft** (the `dawn/` set), so Labyrinth II's `MAP_LABYRINTH_ICARUS_SHAFT` should use `gTileset_Daidaleion`.
- **The thread's floors:** the engine now takes eight (`MAX_FLOORS`), so a ring can register its slabs, cave earth, gravel, beams and plates together.

## The stream

A trickle in Ring II's cleft, a surfable stream across Ring III, a channel through Ring IV's dig that ends in a chute down to Ring V's lake, then falls past Ring VI's forge. Downstream is always a way deeper. The upper rings' water tables are in `tools/ichor/maps/labyrinth_encounters.py`.

## Relics in every ring (LABYRINTH_MAZE.md, the user's "HM stuff")

"Must" means on the only way on (a bridge of the ring's maze graph, or the only door); the rest sit on side loops and dead ends. Field obstacles hide on temp flags, so they come back when the map reloads, as in Emerald.

| Ring | Must use | Optional | Combination |
|---|---|---|---|
| I | **Hecate's Torch** (the dark; carry the hearth fire to six braziers), **Ariadne's Thread** (the tie lesson at A1), **Bronze Hammer** (the roof-fall across the gate room's only arch) | Demeter's Sickle (roots in the cleft's side passage); the Labrys on the way back up (the stewards' treasury seal) | the fire relay: carry the Torch's fire past the draught, and the fresco door that only B1's light shows |
| II | **Torch** (the dark), **Thread**, **Bronze Hammer** (the stair room's fallen ceiling), **Girdle of Herakles** (Daedalus's floor seal on whichever gate the hour opens: one drum by day, two by night) | Sickle (roots choking the grotto), the Labrys on the way back (the runners' shrine) | the herald plates and the floor seal: the grate only rises with the drum in place, then you run |
| III | **Torch** (pitch dark; burn the webs on the front way), **Girdle** (three drums onto three plates unseal the workshop's front door), **Bronze Hammer** (the stair room's way out); the back way needs **Poseidon's Conch** | Conch (the Big Pearl's islet), the glow trail with the Torch doused | the back way: douse the Torch to read Daedalus's glow-marks, then Surf the stream to the back door |
| Workshop | — (the hub) | the lift (after scene D) | — |
| IV | **the Labrys** (bronze chains across the checkpoint's only door), **Girdle** (three drums onto three plates raise the stair's grate; the third drum must cross the second's path first), **Bronze Hammer** (the Titans' cave-in by the stair) | the Titan helmet (the disguise), Sickle (dig roots), Conch (the stream to the chute, the way down to Ring V's lake) | the checkpoint: cut the chains, answer or fight Enkelados, then the floor seal |
| V-VII | Labyrinth II's (the Helm, the dials, the Horn at the forge falls) | — | — |

**Hooks for later** (post-game relics; each guards a stronger Pokémon and an item):
- Ring I: a labrys seal (open on the return from Ring III) on the stewards' treasury: a forgotten bronze Kolossette Lv 52, a Gold Stater.
- Ring II: a labrys seal on the runners' shrine: a Taurivet of the palace herd Lv 52, a Silver Owl.
- Ring III: a Three-Flamed Torch thornweb over the spiders' mother-nest was planned; this seed's maze left no free dead end for it, so it is still to place.
- Ring IV: a Hephaestus's Hammer great boulder sealing the Titans' deepest dig: Geogrip Lv 56, a Nugget.
- **Pan's Crook:** the relic isn't built yet (no item or climb behavior). The cave flowstone faces in Ring II's grotto and Ring IV's dig are where its handholds go; Ring II's grotto already climbs to Ring I by script.

## Daedalus's floor seals (Strength puzzles)

Column drums (the expansion's Strength boulder) onto bronze plates (the herald plate's metatile). The check runs from coord events on the room's cells after a push (one step after the last push); FLAG_TEMP_4/5 hold the open state, so leaving the map puts the drums back and shuts the way; each room has a reset lever (a double-axe handle on the wall) that does the same at once.

| Ring | Seal | Difficulty |
|---|---|---|
| II | the sun room: 1 drum, 1 plate; the Moon Room: 2 drums, 2 plates | teaches the idea |
| III | the workshop's front door: 3 drums, 3 plates, pushed down, down and up | a short plan |
| IV | the checkpoint's stair: 3 drums, 3 plates; the long push crosses another drum's lane, so the order matters | order matters |

Not built: plates that reset when stepped off, pits filled with blocks, drums pushed into the stream as stepping stones (Gen 3 boulders can't enter water without engine work).

## The lost (the tribute, and explorers since)

Read as signs; darker as you go down. Some hint that the Titans goaded Asterion (LABYRINTH §8: a frightened bull driven into a monster).

| Ring | Where | What |
|---|---|---|
| I | (10,21) | a tally of days scratched in the plaster, stopping at nine |
| I | (2,17) | "SEVEN TURNED LEFT. I TURNED RIGHT." in an Athenian hand |
| I | (36,9) | a burned-out torch snapped in two |
| II | (44,9) | a sandal by the trickle, its strap cut |
| II | (22,21) | in the Long Hall: "IT RAN AT THE FIRE, NOT AT US." |
| III | (6,5) | bones under old web, a girl's bronze pin |
| III | (20,25) | "THE BRONZE MEN DROVE IT AT US WITH FIRE. IT DID NOT WANT TO." |
| III | (40,30) | an explorer's satchel, every line of the map crossed out |
| IV | (5,30) | a snapped Titan spear and claw marks |
| IV | (30,13) | chalked by the barracks: "DRIVE IT WITH THE TORCHES. IT HATES THE TORCHES." |
| IV | (20,37) | bones, an Astyran owl shield and a pack |

No new art: the remains are read from walls and floor (the tileset has no bones piece; see the report).

## Awe moments

- **Ring I:** the threshold hall, the house's oldest fire under the stair from the palace.
- **Ring II:** the Long Hall, where the dark at the far end lifts its head and the wall beside you bursts.
- **Ring III:** the stream canyon down the east side, two screens of black water in a raw cave cut, crossed only by Surf.
- **Workshop:** Daedalus's vaulted hall of bronze automata under the grey light of the Icarus Shaft.
- **Ring IV:** the Titans' mess hall under sickle banners, and the dig where the stream roars over the lip into Ring V.

## Vertical treasure

Built: Ring I's hole down to Ring II's grotto and its flowstone climb back; Ring II's sunken floor into Ring III's web pocket; Ring III's hole into Ring IV's dig; Ring IV's chute into Ring V's lake. Not yet: in-ring stairs and ladders to lofts and cellars (`labyrinth_extras.cellar` is written but not placed).
