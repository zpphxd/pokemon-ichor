# Route 4, the Isthmus road: the map

Batch 3's first road (design/phase2/BUILD.md): out of Emporion's Isthmus Gate, across
the Isthmus to the mouth of Hecate's Hollow. It carries SCRIPT.md's "Route 2, the
Sacred Way" (its old name) and beat 17, on `gTileset_Skiron` (TILES_skiron.md).

| | Builder | Size | Tilesets |
|---|---|---|---|
| `MAP_ROUTE4_ISTHMUS` | `tools/ichor/maps/route4.py` | 60×32 (about 4.5 screens of road) | aethos + skiron |

The builder writes the layout, `map.json`'s events and the city's connection entry, and a
generated block in `scripts.pory` (each heap's cell, the cleared slide, the struck camp),
then checks the result; run it after any change, with `--render DIR` for the review
images. `tools/ichor/maps/route4_encounters.py` writes the wild tables. The check:
`tools/ichor/tests/route4.sh`.

| Image | Shows |
|---|---|
| [`img/route4.png`](img/route4.png) | The route at 2x, with its people, items and obstacles, before beat 17 |
| [`img/route4_after.png`](img/route4_after.png) | After beat 17: the slide gone from the road, the camp struck |
| [`img/route4_walk.png`](img/route4_walk.png) | Collision (red), tall grass (green), ledges (blue), people (yellow), trainers (orange) and their sight (orange squares), the warp (cyan), the trigger (magenta), signs (white ×), hidden items (pink ×) |
| [`img/route4_screens.png`](img/route4_screens.png) | Sixteen GBA-screen views along the walk, with the border and the city past the edges |
| [`img/route4_seam.png`](img/route4_seam.png) | The Isthmus Gate's seam from both sides, each drawn with the tilesets the game uses there |
| [`img/route4_ingame.png`](img/route4_ingame.png) | In game, from `route4.sh`: the gate, the kilns, the band, the herm, the slide's scene, the heaps, the procession's thanks, the struck camp |

## The plan

**The road.** It leaves the gate north as the aethos path (the six rows by the seam are
aethos only, and match the city's gate road at x = 7–9), turns into the old paving
outside the potters' quarter, and bends east between the family plots of the dead.
Past the hill spur it climbs the rise to the pass and runs along the cut bank to the
cutting, the procession's camp and the Titans' rockslide. The Hollow's mouth is a dark
door in the cut bank beyond the slide.

**Rhythm,** south to east: the gate's olive groves and the route sign; the kilns and
Exekias, in plain view, watching the road (first trainer, mandatory); the woods
clearing west of the road, its mouth choked with marble rubble (the Hammer's first
lesson, a Great Ball and a forgotten grave inside); the corner among the tombs; the
paving gone to grass between two walled plots (forced band 1, three deep); Myrrhine
across the road; the fork: the hill spur north (the goat path, Menalkas and his goats,
the herm's side path with its Titanborn guard, the Super Potion, the terrace orchard
behind its thicket); the rise (forced band 2); Pheidippos at the narrow cutting
(mandatory); the camp (healer, Eudemos, the initiates, Alethea on her milestone,
Kapelos); the slide; the Hollow.

**The lower terrace** is the loop. From the road among the tombs a gap leads down past
the old burial mound and the walled grave plot (the Repel, through its back gate), the
family tomb a fallen column drum has shut (the Girdle, Act II: a Revive and a dig spot
inside) and the east meadow with its scree nook (the Hard Stone). From the camp,
terrace lips drop south to it: one way, back toward the city.

**Relic gates you can see:** the woods clearing's rubble (the Hammer, now), the
rockslide (the Hammer, the main path), the orchard's thicket (Demeter's Sickle, end of
Act I: the Sun Stone shows on the terrace), the family tomb's drum (the Girdle, Act II:
the Revive shows through the gate).

**Every dead end pays:** the clearing (Great Ball), the kiln yard (Potion; the Ether in
the wasters' ash), the walled plot (Repel), the spur's top corner (Super Potion), the
orchard (Sun Stone), the herm's nook (the herm), the cookfire (Stardust), the milestone
(Oran Berry), the scree nook (Hard Stone), the tomb (Revive), the road's end (the
Hollow's name stone).

## Pass 1

First layout, rendered whole, in sixteen 15×10 views and as a walk map.
- The checker found the edges open over unreachable hilltop, a pine's crown that let the goat meadow out onto the hilltop, the camp walled in by its own tents and people, the walled plot's gate and the family tomb's drum shut in by grove olives, and Exekias and Myrrhine walkable round (the kiln yard opened onto the road south of Exekias; the verge under Myrrhine ran along the road).
- Fixed: the yard fenced on the road below Exekias (firewood, amphorae, a wasters' heap); Myrrhine's sight 4, down to the south verge; the meadow's east side shut; the grove olives moved off the gates; the camp re-laid with lanes between the tents.
- Looked at: the slide's white marble heaps read well, and the mouth reads as a cave in the bank. But every patch of tall grass was a rectangle, the edge woods were a grid of olives and stone pines in rows, the hilltop over the bank was flat grass with a few trees, and the camp's tents stood in a line.

## Pass 2

- Tall grass redrawn as staircases (row by row spans), so every patch has a ragged edge but uses only the shapes the tileset already has (the builder fails on a missing shape rather than rebuilding Skiron, which Route 5 shares).
- The camp laid in an arc round the cookfire: four tents, the cart with its donkey at the shafts, bedrolls, myrtle and baskets, the people at the fire.
- The hilltop planted as an Aleppo pine wood with kermes oak, thinning to scree and boulders above the slide.
- The terrace's own dead added: a sarcophagus by the track, a fallen drum, a leaning stele, a cypress pair.
- The cutting's scree made solid rocks (loose pebbles there looked walkable and weren't).
- Item balls drawn in the renders.
- Still wrong: the edge woods still read as an orchard grid.

## Pass 3

- The woods filler rewritten: only the two cells by the map's edge keep the border's 2×2 olive phase, so the woods run on into the border; inside, olives, stone pines and cypresses are placed staggered by noise, so the lines are mixed and never one tree in rows.
- The struck camp now leaves trampled ground: dry grass and stones where the tents stood, the fire's ring cold, Alethea's milestone by the road (it was flat grass).
- In game (`route4.sh`): see below.

## What still isn't ideal

- The heaps are the vanilla breakable-rock sprite (ENGINE_API §2's art note: the marble-rubble object art isn't drawn yet). Each stands on a marble-rubble cell, so the slide reads as rubble around them.
- The great herm is aethos's small roadside herm (0x01B); Skiron has no great herm and no desecrated look, so the sickle is in the text only.
- The Hollow's mouth is General's cave door, retextured, set in Skiron's grey cut bank: its brown frame is a shade warmer than the bank's strata.
- Potter, runner and initiate walkers and portraits aren't drawn: Exekias is the man, Pheidippos the youth, Myrrhine and the initiates the priestess and the youths; their battle portraits are SCRIPT.md's placeholders (Hiker, running Triathlete, Psychic).
- The Diolkos isn't on this road: it stays with Emporion's harbor (BUILD.md allowed either).
