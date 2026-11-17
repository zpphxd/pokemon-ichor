# Amnisos (`MAP_KNOSSA_AMNISOS`, 40×30)

Built by `tools/ichor/maps/knossa_amnisos.py` on `gTileset_Amnisos` (aethos primary). Scripts: SCRIPT.md beats III-3A and III-4, Part 2.

**Real-world model.** Amnisos was the harbor of Knossos, on the open north coast of Crete: a beach town under a limestone headland (Paliochora), a sanctuary of Zeus Thenatas, and the Cave of Eileithyia in the hill behind, where Odysseus says Idomeneus's fleet anchored. Its "Villa of the Lilies" had the finest lily frescoes on the island.

## The brief

- **Sentence:** a working harbor town that faces the sea and turns its back on the palace road: you step off the ship onto a quay full of Titan hulls and bees.
- **Land:** the headland's limestone bluff rises in the west with the birth goddess's cave in its south face; a stone quay and a curving mole hold the harbor; east of the mole the beach runs out to the open shore; the ground climbs gently south to the town wall and the olive country of the Bull Road.
- **Settlement logic:** what a port needs sits on the quay (the Asclepeion, the saffron hall, the harbor shrine with its morning honey); the tavern and the fisher's hut sit on the beach where the boats are drawn up; the houses line a street a step above the harbor, each with hives on its flat roof; the town wall closes the south with one gap for the road.
- **Reveal:** from the gangplank the four Titan ships are moored along the mole in plain view, sails furled and decks empty, while the town carries on beside them. The cave's carved mouth is seen across the harbor and reached last, up the goat path.
- **Signature:** bees: hives and skeps on every roof, the honey jar at the harbor shrine, Kydon's hive-tube wall, a girl with a Melibee at the ladder to the roofs.

## Passes

| Pass | Render | What changed |
|---|---|---|
| 1 | `design/phase4/img/maps/knossa_amnisos_pass1_1x.png` | Layout: headland, quay, jetty, mole with two Titan triremes, beach; Asclepeion and Agora on the quay; five houses; the town wall and the south gap. Critique: an 18-cell straight street, flat open grass, no height. |
| 2 | `knossa_amnisos_pass2_1x.png`, `_views.png` | A paved harbor plaza before the Asclepeion and Agora with a herm at its corner; flower beds by the doors and walls; the headland raised a level (elevation 4, the cave stair the join); boulders and anemones break the south lawn. |
| 3 | `knossa_amnisos_pass3.png`, `_1x`, `_events`, `_views` | Clear the mole's single-file walk (the bollards moved off it, the sailor off its root) so the veteran can be reached; final audit pass. |

At 15×10 every screen holds one landmark: the jetty and harbor shrine, the Titan ships on the mole, the cave mouth, the plaza's two civic fronts, the beach tavern and boats, the south gap with its sign.

## Events

- Doors (warp ids 0–6): Asclepeion (10,13), Agora (16,13), the Double Axe (26,13), Polypos's hut (34,12), Aithon's house (11,19), the old leaper's house (17,19), Kydon's honey house (24,19).
- South: a down connection to the Bull Road at offset 5 (the gap, x 18–21, meets the road's x 13–16). The 6 rows nearest the seam use only aethos metatiles.
- The arrival lands at (16,7), beside Nausikles's gangplank (17,6).
- Hidden: a Pearl at the jetty's end (14,2), a Bronze Obol behind the harbor shrine (15,8). Items: Max Repel on the headland (6,4), Hyper Potion on the leaper house's flat roof, up the ladder (16,17).
- Heal location `HEAL_LOCATION_KNOSSA_AMNISOS` in front of the Asclepeion (10,14).
- Water: surf and fishing tables (SCRIPT.md Part 4, "Fishing and water"); no land encounters in town.
