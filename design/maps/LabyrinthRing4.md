# Ring IV, the Masks (`MAP_LABYRINTH_RING4`)

Built by `tools/ichor/maps/labyrinth_ring4.py` (seed 5); tileset `labyrinth` on `oikos`; 50×42 (14 screens), lit by the Titans' lamps (not a dark map). SCRIPT.md beat III-3I, LABYRINTH.md §6 Ring IV, LABYRINTH_MAZE.md.

## Brief

- **Sentence:** Team Titan's first quarters dug into the house: barracks, an armory, a mess hall where the passwords slip, four sentry posts in the maze, and a giant asking questions at the stair.
- **Land:** the Titan wing takes the masonry north and east; the west and south are the Titans' dig, raw cave where they broke into a spring, the stream running south to a lip that drops to Ring V's lake.
- **Settlement logic:** the Titans took the rooms nearest the way down and dug for water; the posts sit where their corridors meet.
- **Reveal:** the mess hall under the sickle banners, and the chute's roar from the dig.
- **Signature:** the Titan helmet: walk the posts as a recruit.

Models: the West Magazines of Knossos turned to a soldiers' barracks; Mycenaean guard rooms; Cretan karst springs.

## The maze

| Rule | Needed | Ring IV |
|---|---|---|
| Junctions | 42 | 39 (2.8/screen; slightly under) |
| Loops | 3 | 20 |
| Dead ends that pay | 4 | 7: the armory (Pelos, Hyper Potion), the barracks (Max Revive, hidden Ultra Ball), the dig's Iron, a hidden Nugget, the deep dig behind the great boulder, the remains |
| Chambers | ~1 per 2 screens | 5: entry, barracks, armory, mess hall, checkpoint |

## Relics and puzzles

Must: the Labrys (chains across the checkpoint's door), Bronze Hammer (the Titans' cave-in), Girdle (three drums, three plates; order matters). Optional: the helmet disguise against the four sentries (TRAINER_TYPE_ICHOR_SENTRY), Sickle roots in the dig, Surf down the stream to the chute (Ring V's lake). Enkelados's catechism: the hours, the master, backward; a wrong answer is one battle.

## Hooks for later

A Hephaestus's Hammer great boulder seals the Titans' deepest dig: Geogrip Lv 56, a Nugget.

## Passes

1. Draft (world-act3): a corridor with rooms, not a maze. Rebuilt on the maze generator with the rooms stamped.
2. A lamp blocked the checkpoint's door; a sentry stood on a column. Fixed (lamp moved, features never on people).
3. Final `img/maps/labyrinth_ring4.png`, `_views.png`. Map audit: no FAIL. Style: 38% flat, longest edge 15 (WARN).
