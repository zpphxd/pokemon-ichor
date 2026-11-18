# Ring II, the Runner's Ring (`MAP_LABYRINTH_RING2`)

Built by `tools/ichor/maps/labyrinth_ring2.py` (seed 9); tileset `labyrinth` on `oikos`; 54×42 (15.1 screens), dark. SCRIPT.md beat III-3G, LABYRINTH.md §6 Ring II and scene C, LABYRINTH_MAZE.md.

## Brief

- **Sentence:** the house's runners' quarter: a fork of carved gates that open by the hour, a maze that meets in the Long Hall where something huge is first seen, and a heralds' way of bronze plates and dropping grates that has to be run.
- **Land:** the stair from Ring I comes down in the north-west. The north-east is old cave, a grotto where the house's stream begins as a trickle down a cleft; the south runs out into cave again where the masonry gave up.
- **Settlement logic:** Daedalus timed the house: two doors share one corridor so one is always shut, and the heralds' plates were built to test a runner's legs. The grotto was never built on; a hole from Ring I's cleft drops into it, and its flowstone is a way back up.
- **Reveal:** the Long Hall: walking in, the dark at its far end lifts its head, and the wall beside you bursts (scene C).
- **Signature:** the heralds' way: three bronze plates engraved with a herald's staff, each raising a grate for a dozen steps.

Models: the Knossos palace's long west corridor and its magazines; the Cretan cave springs (the Idaean Cave's dripping chambers) for the grotto.

## The maze (LABYRINTH_MAZE.md §2)

```text
#-# D-J-D +-J-J-+ +-#-#-#     the entry (#), the comb above the fork, the grotto (#, east)
| |   |   | | | | | | | |
#-#-+-J-D +-+ + J-J #-#-#
              | | | |   |     sun gate below (2,1), moon gate below (4,1): shut in this sketch
+-+-J-J-J-#-# J-J J-J-J-J
|   | | | | | | | | | | |
+ #-# J-+ #-# + +-J-J-J-J     the TM room (#, west), the Moon Room (#)
| | | |     | |         |
+ #-# J-+-+-J-J +-+-D D +
| |   |       | |     | |
J-J-J-#-#-#-#-#-+     + +     the Long Hall (#); the heralds' way to its east
|   | | | | | |       | |
+ +-J #-#-#-#-#-+ D D-+ +
| | |           | |     |
J-+ J-J-D + +-+ + + +-+-+
|   | |     | | | | |
J-+-J-J-J-+ J-J-J D #-#-#     the stair room (#): Tephra and the stair down
|     | | | |   |   | | |
+-+-+-J-J-J-J-+-J-+-#-#-#
```

| Rule | Needed | Ring II |
|---|---|---|
| Junctions | 3 per screen (45) | 44 nodes of degree 3+ (2.9 per screen), more at the chambers' many doors |
| Loops | 3 | 23 |
| Dead ends with something | 4 | the comb's goddess shrine (2,0); the herald fresco and a hidden Bronze Obol (4,0); Sinopos and the Silver Owl (4,7); the Full Heal behind the cracked wall (5,7); the TM room (TM Shock Wave); the Moon Room (Moon Stone, hidden Stardust, the sunken floor); the grotto (Ultra Ball, the climb); a Max Repel |
| Straight runs | 8 | columns, niches and formations break every long run; walls notched every 16 at most |
| Chambers | ~1 per 2 screens | 6: entry, TM room, Moon Room, Long Hall, grotto, stair room |
| Long wrong turns | 2 | the west comb of the sun side; the south loop under the Long Hall |

## Puzzles

- **Sun and moon gates:** `gettimeofday` in DrawState opens the sun gate by day and the moon gate at night; each side reaches the Long Hall.
- **The heralds:** plates at (34,18), (46,22), (38,30); every cell of each run has a `RunStep` coord event (VAR_TEMP_3 = the run), the grate stays up for 14/12/10 steps (Mortal/Hero/Spartan, `Ichor_GetStepGlassLimit`), and a grate once passed stays up (FLAG_TEMP_1-3) so the walk back is free.
- **Scene C:** coord events across the Long Hall: the rumble, the shake, the cracked wall becomes rubble (`FLAG_ICHOR_R2_LONG_HALL`), LABYRINTH's two lines word for word. Asterion has no sprite yet, so he is heard and felt, not seen.
- **Drops and climbs:** Ring I's hole lands in the grotto (warp 3); the grotto's flowstone climbs to Ring I's cleft; the Moon Room's sunken floor drops into Ring III's web pocket.

## Passes

1. 24 crossings: the maze became a field of square pillars, too open to be a maze, and the fork's north band one big room (seen in the first render). Cut to 12 crossings, the fork made a short comb.
2. A 44-cell straight south wall (style FAIL). The cave took the south row, and `notch()` cuts a recess into any wall running over 16.
3. Final `img/maps/labyrinth_ring2.png`, `_views.png`. Style audit: 38% flat, 0% barren, longest edge 16 (WARN), no height. Map audit: only the stair down's Ring III warp, which lands with Ring III.

## Test

`labyrinth_upper.sh` walks Ring I's stair down, scene C, the three herald runs, Tephra, the climb up to Ring I and the hole back down.
