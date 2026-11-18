# Ring III, the Mysteries (`MAP_LABYRINTH_RING3`)

Built by `tools/ichor/maps/labyrinth_ring3.py` (seed 3); tileset `labyrinth` on `oikos`; 54×46 (16.6 screens), pitch dark. SCRIPT.md beat III-3H, LABYRINTH.md §6 Ring III, LABYRINTH_MAZE.md.

## Brief

- **Sentence:** the house's dark heart before the workshop: webbed corridors on the way everyone takes, and Daedalus's own way marked in paint that only shows in the dark.
- **Land:** the masonry maze fills the west and middle; the east is a raw cave cut where the stream runs north to south in a channel; old cave in the south-west.
- **Settlement logic:** Daedalus lived down here and marked his own route to his back door with glow-paint labrys signs; the front way grew webs because nobody uses it but the Titans.
- **Reveal:** douse the torch and the black screen fills with faint aqua double axes leading east, to water.
- **Signature:** the glow trail (the `glow/` palette set over `labyrinth`, `src/data/ichor_glow.h`).

Models: the Knossos labyrinth of Cretan legend as a working Minoan basement; Skotino's dark galleries; the karst streams under Psiloritis.

## The maze

| Rule | Needed | Ring III |
|---|---|---|
| Junctions | 50 (3/screen) | 59 (3.6/screen) |
| Loops | 3 | 28 |
| Dead ends that pay | 4 | 9: the Max Ether, the Star Piece by the trail's spur, a hidden Revive, the hole down to Ring IV, anchors, the web pocket's Rare Bone, No. 7's room (TM Shadow Ball), the Big Pearl islet (Surf) |
| Chambers | ~1 per 2 screens | 4: entry, No. 7's room, the front room, the back room |
| Long wrong turns | 2 | the north-west webbed loop; the south-west cave |

## Relics and puzzles

Must: Torch (dark, webs on the front way), Bronze Hammer (the stair room's way out), Girdle (three drums onto three plates unseal the workshop's front door). The back way: douse the Torch for the glow trail, then Surf (Conch) across the stream, which has no ford. See `Labyrinth_System.md`.

## Hooks for later

A Three-Flamed Torch thornweb over the spiders' mother-nest (Hyphantis Lv 55) is planned; the current seed left no free dead end, so it is not placed.

## Passes

1. First render: the channel was a ford and the back way walked; the glow trail looked like any route. Fixed: the ford went (the back way is now Surf), glow-marks only at turns and branches.
2. Rubble, the floor seal, remains, a second hidden item for the dungeon minimum.
3. Final `img/maps/labyrinth_ring3.png`, `_views.png`. Map audit: no FAIL. Style: 37% flat, longest edge 18 (WARN).
