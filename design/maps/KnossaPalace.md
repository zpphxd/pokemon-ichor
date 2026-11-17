# The Palace of Minos (`MAP_KNOSSA_PALACE`, 60×50) and its rooms

Built by `tools/ichor/maps/knossa_palace.py` (`gTileset_PalaceMinos`, aethos primary) and `tools/ichor/maps/knossa_rooms.py` (`gTileset_PalaceRooms`). Scripts: SCRIPT.md III-3C, III-3D, III-3E, III-3O, III-3P's landing; LABYRINTH.md §3, §8 Scenes A, B, K, L, §10.

**Real-world model.** Knossos on the Kephala hill: the North Entrance passage with its painted charging-bull relief, the North Pillar Hall, the long Central Court running north–south, the Throne Room on the court's west side with its gypsum throne and griffins, the West Magazines' rows of pithoi behind it, the West Court with its *kouloures* (stone-lined pits), the Theatral Area's broad steps at the north-west, the Grand Staircase and light wells of the east wing, the Queen's Megaron with its dolphin fresco, the South Propylon and the "Prince of the Lilies" relief; red columns tapering downward under black capitals; horns of consecration on the roof lines.

## The brief

- **Sentence:** a many-storied ruin on its hill, entered through one narrow passage that opens on the whole Central Court at once.
- **Land:** the hill's top is the palace's paving; its north edge meets the road on a ramp, its south falls away in a limestone face; grass takes the palace back at its edges and in the West Court.
- **Settlement logic:** storerooms (the magazines) behind the state rooms (the throne) on the west; the residential wing with its staircase and light wells on the east; the court as the centre of everything, with the bull-leaping lane down its length and the herd's pen beside it; the Theatral Area where the road arrives.
- **Reveal:** you come down the road, fight through the North Entrance's passage between the charging bull and the leapers, and the colonnaded court, the painted lane and the Gentle Bull are all in front of you.
- **Signature:** the bull-leaping lane and its painted line, with Sarpedon and the Gentle Bull.

| Pass | Render | What changed |
|---|---|---|
| 1 | `design/phase4/img/maps/knossa_palace_pass1_1x.png` | Wings, court, lane, pen, magazines, West Court, Theatral Area, South Propylon. Critique: wings eight rows deep read as stacked shelves; endless uniform paving; 38-cell straight edges down both flanks; no height. |
| 2 | `knossa_palace_pass2.png`, `_1x`, `_events`, `_views` | Wings rebuilt as two stepped storeys of three-to-four rows; light wells between them; grass through the ruin with paving edges; cypress and rubble along the flanks; the south face stepped; porticoes of columns down both sides of the court; the hill top raised a level (ramps join it). |
| 3 | `knossa_palace_pass3*` | The lane's line as a sign facing north (the leap's start), final audit. |

## Hand-offs (for the Labyrinth chapters)

- **Down:** the Grand Staircase's stair foot is a trigger at (2,3) in `MAP_KNOSSA_PALACE_GRAND_STAIRCASE`. Once the Labyrinth I chapter's `MAP_LABYRINTH_RING1` exists, `KnossaPalace_GrandStaircase_EventScript_ToRing1` should warp there (it needs the Thread). Before dawn after the raid (`FLAG_ICHOR_ARIADNE_WOKE_YOU`), the same foot is Daedalus's lift: `_ToWorkshop` should warp to `MAP_LABYRINTH_WORKSHOP` for Scene L.
- **Back up after the Turning:** warp to `MAP_KNOSSA_PALACE` (29,16) at night with `VAR_ICHOR_KNOSSA` = 18. Kleon waits at (29,14) for Scene K; Alethea runs in; the night passes in the Queen's Megaron; Ariadne wakes you.
- **The Icarus Shaft:** warp to `MAP_KNOSSA_PALACE` (30,23) with `VAR_ICHOR_KNOSSA` = 19. The landing plays here (Ariadne asleep against Asterion) and sets `VAR_ICHOR_ACT3` = 6; Asterion can be caught (Lv 50); Alethea sends her gull and goes down to the quay for III-4.

## The rooms

Every room is its own shape and furniture (MAP_DESIGN §2). The `palace_rooms` tables are counters (`MB_COUNTER`) so healer and stallkeeper serve across them.

| Room | Size | Brief | Final render |
|---|---|---|---|
| Throne Room | 13×9 | The gypsum throne between its griffins, the council benches, the lustral basin; Ariadne beside the throne, not on it. | `knossa_room_throne_room_pass2_1x.png` |
| West Magazines | 15×11 | Aisles of pithoi taller than you; the Titans' camp among them (bedrolls, brazier, shovels); the password-trail talk. | `knossa_room_west_magazines_pass1_1x.png` |
| Queen's Megaron | 12×10 | The dolphin fresco, the saffron gatherer, bath, loom and bed; Alethea reading the plaster; the night after the raid. | `knossa_room_queens_megaron_pass1_1x.png` |
| Grand Staircase | 11×10 | A flight down under its balustrade into the dark, a light well beside it whose shaft drops past dressed gypsum into raw rock (LABYRINTH_MAZE §1); Ariadne and the Thread. | `knossa_room_grand_staircase_pass1_1x.png` |
| Amnisos Asclepeion | 13×10 | A hall lit from above: the sunken pool where the Panacoil coils, the healer's basin, salve niches, the painted Pithos. | `knossa_room_asclepeion_pass1_1x.png` |
| Amnisos Agora | 12×8 | Anthousa's saffron hall in Minoan red: oil pithoi, the loom-weight scale, crates of thyme. | `knossa_room_agora_pass1_1x.png` |
| Kydon's honey house | 9×8 | The back wall is the hillside: hive-tube niches in the rock, the wax press, the gulls' perch. | `knossa_room_kydons_house_pass1_1x.png` |
| The Double Axe | 14×8 | Long bench under half-flaked dolphins, the rack of horns, the gypsum knucklebones table. | `knossa_room_tavern_pass1_1x.png` |
| Aithon's house | 12×9 | Lustral basin, guest couches, a ship on the wall, a table set for more than live here. | `knossa_room_xenia_house_pass1_1x.png` |
| The old leaper's house | 11×8 | Bronze bulls on a shelf, the splint on its peg, the loom and the sleeping Gelasable. | `knossa_room_leapers_house_pass1_1x.png` |
| Polypos's hut | 8×7 | Octopus pots stacked by the door, the bean pot always on the fire. | `knossa_room_fishers_hut_pass1_1x.png` |
| Bombylia's hut (Bull Road) | 9×7 | A round hut over a spring basin, skeps on shelves, the cot. | `knossa_room_bull_road_hut_pass1_1x.png` |
