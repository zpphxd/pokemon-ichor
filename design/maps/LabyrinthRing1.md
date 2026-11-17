# Ring I, the Threshold (`MAP_LABYRINTH_RING1`)

Built by `tools/ichor/maps/labyrinth_ring1.py` on `labyrinth_lib.py`; tileset `labyrinth` on `oikos`; 42×34 (9.5 screens), dark. Story: SCRIPT.md beat III-3F, LABYRINTH.md §6 Ring I, LABYRINTH_MAZE.md.

## Brief

- **Sentence:** the house's front rooms, a maze of gypsum corridors around the threshold hearth, where the old cave already breaks through on two sides and the fire has to be carried by hand.
- **Land:** the palace's Grand Staircase comes down into the threshold hall at the top middle. A karst cleft runs down the east side (the limestone the house was cut into, still raw); an older cave pocket opens in the south-west where the builders broke through and gave up.
- **Settlement logic:** the masonry is the house's oldest part, built first at the stair and pushed outward until it met the cave. The braziers stand at the ends of passages because that is where Daedalus wanted you to stop: each is a step of a relay from the hearth to the gate.
- **Reveal:** B1's light shows a seam in the wall south of it: a painted door that was never stone. Through it, the fresco hall and its brazier, which every other way round is too far for the fire.
- **Signature:** the threshold hearth, the house's oldest fire, and the red Minoan columns standing in the long corridors.

Real-world models: Knossos's ground-floor corridors and the Corridor of the Procession (gypsum slabs in red plaster, red columns tapering down, horns-and-niche shrines like the Shrine of the Double Axes); the Cretan karst caves (Skotino, the Idaean Cave) for the cleft and the pocket.

## The maze (LABYRINTH_MAZE.md §2)

The relay's spine is laid by hand (`SPINE`); the rest is a braided maze grown around it (seed 99), then measured. Graph, nodes every 4 cells (`#` a chamber, `J` a junction, `D` a dead end):

```text
D D D +-#-#-+-+-D D          row 0: the threshold hall (#) at the stair
| | | | | |       |
J-J-J-J-#-#-J-J-+-J
|     |   | | |   |
+ D-+ + +-J-J J-D +
|   | | |   | |   |
+ #-# J-J-+-J-J-J-J          the fresco hall (#), behind the painted door
| | | |       | | |
D #-# J-J-J-+-J J-J
  |   | | |   | | |
+-J D-J-+ +-J-J-J +
| |         |   | |
J-J-J-J-+-+-#-# J-J          the gate room (#): G and the stair down
| | | |     | | | |
D +-+ D D-+-#-# +-+
```

| Rule | Needed | Ring I |
|---|---|---|
| Junctions | 3 per screen (28) | 35 (3.7 per screen) |
| Loops | 3 | 15 |
| Dead ends, each holding something | 4 | 12 (below) |
| Longest straight run | 8 | every long run carries a column, niche or formation (`break_runs`); two short stretches left plain |
| Corridor width | 1–2 | 2, with 1-wide pinches at columns and lamps |
| Chambers 4×4+ | about 1 per 2 screens | 3 (the hall, the fresco hall, the gate room) |
| Long wrong turns | 2 | the west comb (four dead-end teeth off one corridor) and the south-east loop that circles the gate room without entering it |

**Dead ends and what each holds:** B1 (2,0), B2 (8,2), B4 (0,7), B5 (3,7) braziers; the thread lesson's Hyper Potion (8,0); Xenodike and TM Rock Tomb (0,0); a clay goddess's niche and a hidden Bronze Obol (1,0); the fresco nook behind the painted door (1,2); the hidden anchor and a Hyper Potion behind the fresco hall (0,4); an Ether (2,5); the bull fresco and a hidden Revive (4,7); the hole down to Ring II (9,0).

## The relay (measured on the final grid, steps)

| Hop | Steps | Rule |
|---|---|---|
| hearth → B1 | 11 | the easy first hop |
| hearth or B1 → B2 | 18 | |
| B3 from any earlier fire, door shut | 53 | past Hero's 30: the door is needed |
| B1 → B3 through the door | 16 | |
| B3 → B4 | 17 | B4 from H/B1/B2 is 33 |
| B4 → B5, the short way | 16 | through the draught, which snuffs the flame |
| B4 → B5, safe | 22 | fits Spartan's 26 |
| B5 → G | 18 | |

Every needed hop fits Spartan's 26. The fire lasts 36/30/26 steps (Mortal/Hero/Spartan) via `Ichor_GetStepGlassLimit`.

## Render passes

1. First render (pure generator, rectangular cave regions): the cave was two hard rectangles with a straight seam into the masonry, corridors ran 20+ cells bare, and nothing told one stretch from another. Fixed: the cave became node-level regions with rock eaten back at random (`cave_grid`), so its passages bulge and wander.
2. `img/maps/labyrinth_ring1_pass2.png`: readable, but 14 straight runs over 8 cells. Fixed: `break_runs` puts a red Minoan column on one lane of long north-south corridors, carved niches (plain, a goddess's shrine, a lamp gone out) in the faces of long east-west ones, and stalagmites or boulders in the cave.
3. `img/maps/labyrinth_ring1.png` (final), `_views.png` at 15×10: every screen has a brazier, the hearth, a column run, a niche shrine or the cave cleft. Left: no level change (the house is one floor; the cave's ledges are the next pass), and one 18-cell straight wall edge on the hall's north side, which is the stair's wall.

## Audits

`map_audit.py`: the two warp FAILs are the stair down naming Ring II's warp 0, which lands with Ring II. `map_style_audit.py`: 36% flat, 0% barren, 18-cell straight edge, no height.

## Test

`tools/ichor/tests/labyrinth_upper.sh`: arrival on the threshold ring, a wrong turn down the side passage and the thread winding back, then the whole relay (hearth, B1, the door, B2, back to B1, B3, B4, B5 round the draught, G), the stair opening, Akakallis.
