# Eleusa Village and the Temple of Demeter: the maps

Batch 4's places (design/phase2/BUILD.md): the village of the Mysteries and its
Telesterion, built from `gTileset_Eleusa` and `gTileset_TempleDemeter`
(TILES_eleusa.md, TILES_temple_demeter.md), with their everyday people, signs, items
and the Lesser Mysteries' layout. The story scenes (beats 20–25) come in the next batch.

| | Builder | Size | Tilesets |
|---|---|---|---|
| `MAP_ELEUSA_VILLAGE` | `tools/ichor/maps/eleusa.py` | 50×40 | aethos + eleusa |
| `MAP_ELEUSA_VILLAGE_TEMPLE_OF_DEMETER` | `tools/ichor/maps/temple_demeter.py` | 27×27, dark | oikos + temple_demeter |

Both builders write the layout, `map.json`'s events and a generated block in
`scripts.pory`, then check the result; run them after any change, with
`--render DIR` for the review images. The check: `tools/ichor/tests/eleusa.sh`.

| Image | Shows |
|---|---|
| [`img/eleusa_village.png`](img/eleusa_village.png) | The village at 2x, with its people and items |
| [`img/eleusa_village_walk.png`](img/eleusa_village_walk.png) | Collision (red), the wheat and meadow's tall grass (green), people (yellow), warps (cyan), signs (white ×) and hidden items (pink ×) |
| [`img/eleusa_views.png`](img/eleusa_views.png) | Fifteen GBA-screen views along the walk, with the border past the edges |
| [`img/temple_demeter.png`](img/temple_demeter.png) | The Telesterion at 2x, every light cold, as the player first finds it |
| [`img/temple_demeter_map_lit.png`](img/temple_demeter_map_lit.png) | The same with all four season braziers lit |
| [`img/temple_demeter_map_dark.png`](img/temple_demeter_map_dark.png) | As the Torch shows it: Autumn and Winter lit, the player at Spring's foot |
| [`img/temple_demeter_map_events.png`](img/temple_demeter_map_events.png) | The pit triggers (blue), the lit-zone rings (gold in, white out), bg events and warps |
| [`img/wheat_rustle.png`](img/wheat_rustle.png) | The wheat rustle's five frames over the wheat, at 6x |
| [`img/eleusa_ingame.png`](img/eleusa_ingame.png) | In game, from `eleusa.sh`: the gate and its name popup, Krokis, the wheat rustle, a wild Pokémon from the wheat, the dark hall, a lit quarter, the shut Ploutonion, Summer lit |

## Eleusa Village

**The plan.** The Sacred Way comes in from Route 5 on the west (rows 24–27) and runs
as a paved street through the village. Krokis keeps the gate with the village stele;
the Asclepeion and the Agora face the street just inside it. The well-yard opens north
of the street: the Maiden's Well (the Kallichoron) with its worn bench and a
pomegranate standing in for the dry fig, the house of Keleos, and the Propylaia's steps.
Through the gate is the walled court of the sanctuary: procession torches on the axis,
the Telesterion at the far end (the crown), the Ploutonion's crag and bronze gate in
the rock beside it, the sanctuary's grain jars and a shrine of Demeter, cypress hedges
outside the walls. West of the sanctuary is Sitokles's granary yard (oven, jars,
winnowing, a reaped plot with stooks) under the north-west wheat. South of the street
lie the fields: the big wheat field round the threshing floor (Eubouleus, the Super
Potion), a reaped strip with stooks and the reaper's basket, Demeter's field shrine,
Euphorion's porch house on the lane to the fields, Dysaules's long farmhouse facing the
fenced Rharian field, and the poppy meadow with its beehives (the Awakening, the Honey).
The Eleutherai road leaves north on the east side; the road of the Mysteries east is
shut by a hoplite in a gate.

**Identity:** wheat and dark doors. Gold fields on three sides, and the only dark
openings in the village are the Telesterion's door and the Ploutonion's cave.

### Pass 1

First layout, rendered and walked in 15×10 views.
- The edge forest was solid olives on a grid: straight walls of one tree on three sides.
- The well-yard and the court were paved wall to wall. With the three-row street that made a six-row slab desert below the Propylaia, and an empty court.
- The checker found pockets: grass above the Ploutonion's crag, the strip between the Propylaia and the west wall, cells behind the house of Keleos.
- The Rharian field, the threshing floor and the meadow read well. So did the Asclepeion and the Agora seen from the gate.
- The north road was a four-column path between two walls of olives, with nothing on it.
- The east gate was a hoplite alone on a wide road.

### Pass 2

- **Forest.** The forest is now mixed: edge blocks stay olives, so they run on into the border's olives, and inner blocks mix olives, stone pines and cypress pairs. The forest's face steps in and out on the west.
- **Well-yard.** The plaza shrank to the Propylaia's front. The well stands on grass with its bench, so the street, the yard and the sanctuary read as three places.
- **Court.** It gained a pomegranate in a bed cut into the paving, a grain shrine, sheaves, and the jars along the south wall.
- **Pockets.** The Ploutonion moved up against the hillside. Jars, a pomegranate and a cypress fill the pockets.
- **North road.** It is now a two-column road with grass verges, cypresses, a boulder and anemones.
- **East gate.** A dry-stone wall crosses the road with the hoplite standing in its gap.
- **Sanctuary.** Cypress hedges now stand outside its west and east walls. Pomegranates line the north-east grove's foot.

### Pass 3

- The Sacred Way reads as a procession route now: cold procession torches line its south verge, and the night of the Mysteries can light them (`METATILE_Eleusa_TorchPost_Lit`).
- The north-west field gained sheaves at its margin and poppies. The granary yard gained a reaped plot with stooks, so the big grass gap left of the granary is gone.
- The checker passes: the seams are open exactly at x 0 rows 24–27, y 0 columns 44–47 and x 49 rows 24–27. There are no Eleusa metatiles in the seam strips, every warp is on a door and reachable, every person can be talked to with everyone in place, every sign is readable, and no walkable cell is cut off.
- Looked at in game (the check's screenshots): the street at the gate, the wheat rustle in gold, the hall in the dark.

**Still wanted from the art side.**
- A dry fig: the well's tree is a pomegranate for now.
- Straw beehives: aethos's tan boulder stands in, as in Elaia.
- A sturdier sanctuary wall. The dry-stone walls read thin next to the Propylaia. The court wall would suit the farms, but not the precinct.
- A door animation for the eleusa doors. They are `MB_NON_ANIMATED_DOOR`, so the player steps in and the screen fades.

## The Temple of Demeter (the Telesterion)

**The plan** (SCRIPT.md Part 5).
- **The hall.** One square hall under the frieze of the Descent of Persephone. Rock-cut tiers run the width of the north wall, with the Mystagogue's dais and Demeter's great altar before them. A forest of columns stands six by six, with a clear aisle from the stair to the Anaktoron in the middle. Chloe's throne and the holy things stand by its door.
- **Autumn,** front left, near the stair. Kallidike stands with her lamp beside it to teach.
- **Winter,** back left, across the columns. Eumolpos stands with his lamp between two columns on the straight line.
- **Spring,** back right, below the tiers. Melissa stands on the tiers above it, facing the wall.
- **Summer,** front right. Its quarter is floored with grain pits. Hecate's chalk marks the one way through, a winding path: in, up, across, down and in from the side. A pit drops you onto the tiers by Spring.

**Lights.**
- Each brazier lights its quarter for good (a lit zone), its column torch, and, in the back quarters, two wall sconces.
- Only the next brazier's seed is set down.
- A brazier lit out of turn refuses: "The year isn't there yet."
- The fourth lights the Anaktoron's doorway, and Chloe is there.
- After the Harvest Laurel the pits are boarded over.

### Pass 1

First layout, rendered cold, lit and dark.
- The trail reads: four corner braziers, the Anaktoron central, the stair at the bottom.
- The Summer pits ran into the bottom wall, so the room's corner vanished into black.

### Pass 2

- The front row is now a walk along the wall (y 25), so the hall keeps its corner. The pit field is still enclosed: the only way to Summer is the chalk.
- The checker confirms the walk:
  - every open cell is reachable from the stair;
  - Autumn, Winter and Spring are reachable without touching a pit;
  - Summer is reachable along the chalk only;
  - every setmetatile lands on its own piece.

### Pass 3

- The Anaktoron's door got the gilt threshold under Chloe's feet.
- The back quarters' wall sconces now light with their brazier, so a lit quarter shows on the north wall too.
- The dark render shows what the player sees: a lit quarter is a landmark from anywhere in the hall.

**Still wanted from the art side.**
- **A grain-pit metatile.** It needs a stone lip, and a boarded-over twin for after the Laurel. The pits use the `void` black for now, which by torchlight reads as a hole but has no rim.
- A pomegranate-red seed and the chalk show only once dousing exists (the engine's glow palettes).

## The wheat rustle

Eleusa's wheat is `MB_TALL_GRASS`. `tools/ichor/art/field_effects_wheat.py` cuts the slice's tall-grass frames from the wheat's own interior metatile, in the wheat's five golds. Over gold, the thrown grain flies as pale chaff and dark husks so it still reads.

`FldEff_TallGrass` (`src/field_effect_helpers.c`) picks the wheat frames and `FLDEFF_PAL_TAG_WHEAT` on any map whose secondary tileset is `gTileset_Eleusa`. It now loads its palette itself, so the script line in `data/field_effect_scripts.s` became a plain `callnative`. Elsewhere the effect is unchanged: general_1, not fog-blended.

Landing in wheat from a ledge would still show the green jump effect. Eleusa has no ledges into wheat.
