# Hecate's Hollow: the map

Batch 3's cave (design/phase2/BUILD.md): the pass under Mount Aigaleos where the
Sacred Way runs from Route 4 (the Isthmus) to Route 5 (the Skironian cliffs). It holds
beat 18 and Part 5's "Three Roads" (design/phase2/SCRIPT.md), built from
`gTileset_CaveDark` (TILES_cave_dark.md) on aethos.

| | Builder | Size | Tilesets |
|---|---|---|---|
| `MAP_HECATES_HOLLOW` | `tools/ichor/maps/hecates_hollow.py` | 48×40, dark | aethos + cave_dark |

The builder writes the layout, `map.json`'s events and a generated block in
`scripts.pory`, then checks the result; run it after any change, with `--render DIR`
for the review images and `--ascii` for the grid. The check is
`tools/ichor/tests/hollow.sh`.

| Image | Shows |
|---|---|
| [`img/hecates_hollow.png`](img/hecates_hollow.png) | The cave at 2x as the player first finds it: webs whole, braziers and torches cold, its people and items |
| [`img/hecates_hollow_lit.png`](img/hecates_hollow_lit.png) | Cleared: the webs burnt, both braziers and the Hekataion's torches lit, the hounds at night |
| [`img/hecates_hollow_dark.png`](img/hecates_hollow_dark.png) | Without the Torch: the daylight at both mouths, the skylight's faint pool in the Hekataion, and a tile and a half of light at stops along the dark road |
| [`img/hecates_hollow_dark_torch.png`](img/hecates_hollow_dark_torch.png) | With the Torch and the first brazier lit: the lit halls, and three and a half tiles of light down the road west, the shortcut and back through the forks |
| [`img/hecates_hollow_ingame.png`](img/hecates_hollow_ingame.png) | In game, from `hollow.sh` |

## The plan

```text
            web chamber                 THE HEKATAION                 the shortcut
            (Silk Scarf,                (the pillar, its spring,      (web C, a ledge,
             Raknit)                     Hecate's supper niche)        the Dusk Ball)
               | web B        web A         |            east road ------+
      brazier 1 + Hekabe  <---- west road --+                            |
      (her sight cuts                       |  fork 3: ahead             |
       the waist)                   loops <-+-> loops (Stardust)         |
               |                            |                            |
      hall 2: brazier 2,          fork 2: right --> ...                  |
      Ether, Battos                 |  left: dead end (Bronze Obol,      |
   <-- WEST MOUTH                   |        Phaino, an eaten supper)    |
      Kallias's pocket            fork 1: left                           |
      (Revive)                      |  right: loop (Escape Rope)         |
                                    +---- the corridor in ---- EAST MOUTH (the old woman)
```

- **The east mouth** (bottom right): daylight from Route 4 on three rows, the old woman
  at the edge of the light with her covered dish, the name stone, the corridor west
  into the dark, and the foot of the shortcut tunnel (a dead end under a ledge, with a
  Dusk Ball as the lure).
- **The dark road** (the middle): a tile and a half of light. At each fork a trigger
  on the approach barks once a visit until the Torch: left, right, straight ahead
  (SCRIPT.md beat 18). The player always heads north at a fork, so "left" is the
  screen's left. Fork 1's right is a loop round a pillar (a hidden Escape Rope on it);
  fork 2's left is a dead end with the Bronze Obol, Phaino lost in the dark and a
  niche whose supper someone ate; fork 3's left and right are narrow loops that come
  back down to its approach (Stardust on the left one). Hecate's chalk marks each
  junction with her triangle and an arrow the right way, faint, for whoever looks.
- **The Hekataion** (top centre): the round chamber where the three roads meet, lit
  faintly from above (a 3-tile pool of light before the Torch). The three-faced pillar
  stands in the skylight; its front is the altar (beat 18, then Hecate's altar menu),
  its sides the spring (the midpoint rest). Hecate's wheel is chalked on the north
  wall beside her supper niche (a hidden Honey). Three roads leave it: south (the dark
  road), west and east, each of the last two behind a cobweb that only fire clears.
- **The road west** (left): web A, then Hekabe's hall in two lobes joined by a
  one-tile waist that her sight covers, the first brazier by her; web B off the hall's
  west lobe into the web chamber (the Silk Scarf; Raknit after the Arachne amphora);
  down to hall 2 with the second brazier and the Ether; Kallias in the dark of a side
  pocket (the Revive); the west mouth's daylight, where Battos minds his goats.
- **The shortcut** (right): from the Hekataion east, web C, a long tunnel down past the
  spring seeping from its wall, a one-way ledge, and out at the east mouth. MAP_DESIGN
  §3's "shortcut out once cleared": a returning player crosses the cave by the lit
  halls, the Hekataion and this tunnel, never the dark forks.

**Teach, test, combine** (MAP_DESIGN §3): fork 1 is a plain T with one bark; fork 2
tempts with a dead end that pays; fork 3's loops cost time. The webs are met before the
fire that burns them (the Hekataion's west and east roads), then the Torch combines
light, webs, braziers and trainers in the second half.

**Readable darkness** (SYSTEMS.md §2): the first screen is daylight; rim-lit walls in
the dark; the chalk, the bones, a niche, a fallen slab and the fork rooms are the
landmarks along the dark road, none more than a dozen tiles apart; Hekabe, the only
mandatory trainer, stands by a brazier inside the Torch's reach.

## Light

`VAR_TEMP_2` is the region the player stands in; the builder writes a trigger on every
edge cell for each neighbouring region, and ON_TRANSITION finds the region from the
arrival cell.

| Region | Id | Light |
|---|---|---|
| the dark | 0 | the Torch's own: flash 7 without it, 3 with it (the engine) |
| the east mouth's daylight | 1 | lit (`HH_LIT`) |
| the Hekataion | 2 | flash 4 before the Torch (the skylight), lit after |
| Hekabe's hall | 3 | lit once brazier 1 (`FLAG_ICHOR_BRAZIERS_START + 0x14`) burns |
| hall 2 | 4 | lit once brazier 2 (`+ 0x15`) burns |
| the west mouth's daylight | 5 | lit |

**Lit is flash 1, not 0** (`ICHOR_STUB_DARKNESS`). In game the engine's flash 0 never
lets the dark come back: `AnimateFlash` to 0 ends with `ScanlineEffect_Stop`, and a
map loaded at flash 0 never starts the scanline effect, so the window that draws the
dark stays fully open until the next map load (found by `hollow.sh`'s first run: the
cave entered from its daylit mouth was fully lit throughout). Until the engine
restarts the effect when the light shrinks, every lit place here is flash 1 (four and a
half tiles), the braziers are lit with `VAR_0x8005 = FALSE` and the map sets its own
flash after, and `HH_LIT` is the one constant to change back. The Telesterion's lit
quarters (`temple_demeter`) have the same problem.

## People, items and flags

| Who | Where | Notes |
|---|---|---|
| OLD WOMAN | (40, 33), the edge of the east daylight | beat 18's warning once (`FLAG_ICHOR_MET_HOLLOW_CRONE`), then the dog; after the Torch, two new lines |
| PILGRIM PHAINO (102) | (16, 23), fork 2's dead end | optional, in the dark, sight 2; Onotis 18, Galekit 19 |
| PILGRIM HEKABE (100) | (6, 14), by brazier 1 | mandatory: sight 3 east covers the waist; Galekit 19, Gelasable 20; then a Barley Cake (`FLAG_ICHOR_GOT_HEKABE_SUPPER`) |
| INITIATE KALLIAS (101) | (8, 34), Kallias's pocket | optional, sight 2 up the pocket's mouth; Pebblith 20, Onotis 20; an Acolyte until the initiate is drawn (`ICHOR_STUB_SPRITE`) |
| GOATHERD BATTOS (103) | (3, 25), the west mouth's daylight | optional, faces out of the cave; Pebblith 19, Kerazap 20 |
| the black hounds | (24, 9), (23, 7), (27, 7) | after 20:00: two fade into the rock as the player enters the Hekataion; the third is Lykopup, Lv 20 (`FLAG_ICHOR_HECATES_HOUND`) |
| Raknit | (7, 4), the web chamber | once the Arachne amphora is done (`FLAG_ICHOR_AMPHORAE_START + 2`, `ICHOR_STUB_AMPHORA`): Lv 20, its hidden ability (`FLAG_ICHOR_HOLLOW_RAKNIT`) |

Phaino and Battos are this map's own (SCRIPT.md names only Hekabe and Kallias); both
are optional and stand on side ways, so the bible's two remain the cave's story.

| Item | How | Where | Flag |
|---|---|---|---|
| Escape Rope | hidden | fork 1's loop (35, 29) | `FLAG_ICHOR_HIDDEN_HOLLOW_ESCAPE_ROPE` (0x2B0) |
| Bronze Obol (Relic Copper) | visible | fork 2's dead end (14, 22) | `FLAG_ICHOR_ITEM_HOLLOW_BRONZE_OBOL` |
| Stardust | hidden | fork 3's left loop (19, 18) | `FLAG_ICHOR_HIDDEN_HOLLOW_STARDUST` (0x2B2) |
| Honey | hidden | Hecate's supper niche (27, 2) | `FLAG_ICHOR_HIDDEN_HOLLOW_HONEY` (0x2B1) |
| Hecate's Torch | beat 18 | the Hekataion | `FLAG_ICHOR_GOT_HECATES_TORCH` (the engine's) |
| Barley Cake | Hekabe, after her battle | | `FLAG_ICHOR_GOT_HEKABE_SUPPER` |
| Silk Scarf | visible | the web chamber (4, 5) | `FLAG_ICHOR_ITEM_HOLLOW_SILK_SCARF` |
| Ether | visible | by brazier 2 (8, 23) | `FLAG_ICHOR_ITEM_HOLLOW_ETHER` |
| Revive | visible | Kallias's pocket (12, 35) | `FLAG_ICHOR_ITEM_HOLLOW_REVIVE` |
| Dusk Ball | visible | the shortcut, at the ledge's foot (40, 18) | `FLAG_ICHOR_ITEM_HOLLOW_DUSK_BALL` |
| Hard Stone | hidden | the shortcut tunnel (38, 22) | `FLAG_ICHOR_HIDDEN_HOLLOW_HARD_STONE` (0x2B3) |

The webs' hide flags: `FLAG_ICHOR_HIDE_HOLLOW_WEB_WEST`, `_CHAMBER`, `_SHORTCUT`. Each
web is two invisible objects (its two cells) running `EventScript_IchorCobweb`; the
map's ON_FRAME swaps in the torn web once one burns.

## Wild Pokémon

Land rate 10 on the cave floor (MB_CAVE); lit floor has none. Levels 17–20, BALANCE.md's
Eleusa band and SCRIPT.md Part 4's Hollow band. The ruling on early evolved forms drops
Cairnolith (it evolves at 25) and keeps Gelasable (at 20) to level 20 only.

| Slot | Rate | `_Morning` (4–10) | `_Day` (10–18) | `_Night` (18–4) |
|---|---|---|---|---|
| 0 | 20% | Pebblith 17–19 | Pebblith 17–19 | Galekit 17–19 |
| 1 | 20% | Spalunk 17–19 | Chelonet 17–19 | Pebblith 17–19 |
| 2 | 10% | Ergant 17–19 | Spalunk 17–19 | Galekit 18–20 |
| 3 | 10% | Galekit 17–19 | Pebblith 18–20 | Spalunk 17–19 |
| 4 | 10% | Pebblith 18–20 | Spalunk 18–20 | Pebblith 18–20 |
| 5 | 10% | Chelonet 18–20 | Ergant 17–19 | Ergant 17–19 |
| 6 | 5% | Spalunk 19–20 | Chelonet 19–20 | Gelasable 20 |
| 7 | 5% | Ergant 19–20 | Galekit 17–19 | Galekit 19–20 |
| 8 | 4% | Galekit 19–20 | Pebblith 19–20 | Spalunk 19–20 |
| 9 | 4% | Pebblith 20 | Spalunk 19–20 | Pebblith 19–20 |
| 10 | 1% | Gelasable 20 | Chelonet 20 | Gelasable 20 |
| 11 | 1% | Chelonet 20 | Galekit 20 | Galekit 20 |

Statics: Lykopup Lv 20 at night, Raknit Lv 20 in the web chamber (BUILD.md's rulings).

## Render-and-critique passes
