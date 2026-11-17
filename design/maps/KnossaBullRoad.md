# The Bull Road (`MAP_KNOSSA_BULL_ROAD`, 30×50), the vineyard terraces (`_VINEYARD`, 20×16) and the Bronze Heel (`MAP_KNOSSA_BRONZE_HEEL`, 30×20)

Built by `tools/ichor/maps/knossa_bull_road.py` on `gTileset_BullRoad` (aethos primary). Scripts: SCRIPT.md III-3B, Part 2–4. Encounters: `tools/ichor/maps/knossa_encounters.py`.

**Real-world model.** The Minoan road from Amnisos up the Kairatos valley to Knossos: low hills of olive terraces and vines, phrygana and thyme on the dry slopes, the herds of the palace (the Knossos tablets count thousands of sheep and plough-oxen), a cutting through the limestone where the valley narrows. The Bronze Heel is Talos's shore: Talos, the bronze guardian who ran round Crete three times a day, had one vein from neck to ankle stopped with a bronze nail.

## The Bull Road brief

- **Sentence:** a country road climbing south through terraces and a limestone cutting, where the palace herd crosses the meadow.
- **Land:** terraces step up southward, their brows facing north (you hop down them on the way back to Amnisos); the valley pinches to a three-wide cutting between limestone blocks, then opens into a meadow, then an old olive grove, then the palace's hill.
- **Settlement logic:** terraces and skeps where the beekeepers work, a great herm at the only fork (east to the shore), the herder's meadow where the road widens and the cattle cross, a beekeeper's corbelled hut (a *mitato*) on its spring by the grove, the priestess holding the last narrow approach.
- **Reveal:** the cutting opens on the meadow and the herd all at once; the labrys door is seen in the east cliff on the way, shut until the Labrys.
- **Signature:** the herd crossing and Milon's scratched line, where the player first leaps a bull.

Rhythm (MAP_DESIGN §1): sign, calm terraces and Kerinthe (easy, in plain view), forced band 1 (3 deep, between olive woods), the fork and herm (Telemos), the cutting and Euphemos with forced band 2 (4 deep) right behind him, the meadow (Boukolion, Kybiste, Theoris, Krokale; Milon; the herd), Bombylia's hut (rest point), forced band 3 (3 deep, Elais), Phaistia at the narrow approach, the two Titanborn at the south end. Forced grass north to south: 10 cells.

| Pass | Render | What changed |
|---|---|---|
| 1 | `design/phase4/img/maps/knossa_bull_road_pass1_1x.png` | The rhythm laid out: groves, three bands, the cutting, the meadow, the hut, the approach. Critique: rectangular grass, long straight lips on the cutting, a bare east terrace. |
| 2 | `knossa_bull_road_pass2_1x.png`, `_views.png` | Vine patches on the east terrace, Milon's line as a sign, the fossil-free brow on the Heel; a dead end found. |
| 3 | `knossa_bull_road_pass3.png`, `_1x`, `_events`, `_views` | The Ultra Ball moved to the east terrace's dead end; the Max Ether under the grove's edge where you can face it; audit clean of FAILs. |

## The vineyard terraces brief

- **Sentence:** three terraces of vines stepping up to a sealed jar, the Bull Road's optional grass with a rarer table.
- **Land / logic:** dry-stone terrace walls with steps cut into them; vines in every band; the vintner's sign at the gap from the meadow.
- **Reveal / signature:** the sealed jar (PP Up) sits on the top terrace in view from the gap; you reach it by walking the vines. Korantha and Persenyx grow here and nowhere else on the island.
- Connection: left of the Bull Road at offset 23. Passes: `knossa_vineyard_pass1_1x.png` to `_pass3`.

## The Bronze Heel brief

- **Sentence:** a shore spur where a giant's bronze foot stands alone on the beach.
- **Land / logic:** the headland's beach grass, a low cliff with one way down, sand, tide pools and a spit of rocks out to the point.
- **Reveal:** the foot comes into view as you round the cliff; Alethea is kneeling by it on the first visit.
- **Signature:** Talos's foot with its bronze nail; the fossil ledge (a skull and a dart: dig one, the tide takes the other).
- Connection: right of the Bull Road at offset 11. Classed `ichor_kind: dungeon` (a side area), as Kronion Hill is. Passes: `knossa_bronze_heel_pass1_1x.png` to `_pass3`.
