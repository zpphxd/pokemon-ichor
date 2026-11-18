# Lake Stymphalia

Built by `tools/ichor/maps/stymphalia.py`. Renders: `img/stymphalia_pass1.png`, `_pass2`, `_after` (with `_after_views`, `_after_walk`). The tileset's own concept renders are in `design/phase4/img/stymphalia_*.png`.

## Brief

- **Sentence:** a wide marsh under bare hills, ringed by reed beds where bronze-feathered birds roost, crossed by an old stone causeway and then by boardwalks threading three reed islets.
- **Identity:** the birds. The first time you step onto the causeway's middle, the camera pans north, the flock lifts out of the roost and turns the marsh the color of a shield, circles once and settles, every bronze head turned toward you (`FLAG_ICHOR_STYMPHALIA_FLOCK_ROSE`). The flock stays perched along the roost after that.
- **Rest stop:** Akanthis's stilt hut by the causeway. She heals the party and registers the lake's travel herm (`TOWN_HERM_STYMPHALIA`, its herm and plaque on the south shore by the causeway's foot), and tells the deep reeds' rumor once (`FLAG_ICHOR_HEARD_LERNIP_RUMOR`).

Tilesets: aethos and gTileset_Stymphalia (42x36, 10.1 screens). Same tileset as both routes: no seam strips.

## The walk, south shore to west shore

| Stretch | Terrain | Trainers | Grass |
|---|---|---|---|
| The south shore | sand bank, long reeds, the sign, the herm | Halia | the bank |
| The causeway | old paving on piles; islet 1 off it | Kyknos (easy, in view, on islet 1's boardwalk) | islet 1 (optional) |
| Akanthis's hut | the stilt hut and its porch | | |
| The long boardwalk | one plank wide | **Borboros** (sitting at its edge) | |
| Islet 2 | reed grass, wall to wall | | band 1 (4 deep) right behind him |
| The west boardwalk | one plank wide | **Tenagos** (in a notch) | |
| Islet 3 | reed grass | Donax (cutting reeds, facing away) | band 2 |
| The west shore | grass, a sand bank, the bank's step (a ledge) | Skirites | |

Side areas: the north stub to the roost (a hidden Metal Coat at its end), the nests' walk with Melampous and the reeds that choke the nests' gap (the Sickle), the side boardwalk east to the deep reeds (Ornithe, a Full Heal, a hidden Razor Claw), the far rock (a Shell Bell, the Conch), the reed wall in the south-east (Limnaia beside it).

Finds: Net Ball, Shell Bell, Sharp Beak, Max Repel, Full Heal; hidden Big Pearl (under the hut), Razor Claw (the deep reeds' end), Metal Coat (the roost's foot), Heart Scale (an old egg in the nests), Super Repel (the causeway's foot).

Wild (all four times): Belornis, Galenyon, Gelasable, Chelonet, Kerazap, Karkitox, Harpelle (day), Sophowl and Kalyptor (night), Cairnolith (night), and **Chalkip at dawn and dusk** (the dex's rare spot, at 46), 46-50. Surf and rods everywhere: Karkitox and Galenyon, the first stages on the Old and Good Rods.

## Hooks for later

| Gate | Where | Relic or event | Behind it |
|---|---|---|---|
| **The north roost** (Labor 6) | the roost's front, (16-27, 4); the sign at (21, 4) from the stub's end | LABORS's Labor 6 (the krotala, post-game) | A reed-bed entrance opens here onto the Stymphalian Reeds (LABORS: 40x40, seven roosts). The flock already lives on it |
| **The reed wall that grows back** (Labor 2) | (30, 27-32), the sign at (30, 30) | LABORS's Labor 2 (the Springs of Lerna); the Sickle cuts it and it regrows | Eight pools in a ring round a ninth, drawn behind the wall and never reached (exempt cells); the Lerna arena goes here |
| **The fog bank** (WORLD_EXPLORATION D5) | the north-east reeds, the sign at (39, 4) from the water | Aeolus's Bag (post-game) | A lone Belornis at Lv 72 that won't leave, before the Labor |
| **The deep reeds' Lernip** (D4) | the deep reeds, east (34-40, 11-19) | rain (SCRIPT Part 4's weather omen) | Lernip at 28-30 in the rain. Akanthis already tells the rumor and sets `FLAG_ICHOR_HEARD_LERNIP_RUMOR`; the rain omen, the ripple object and the roll (`FLAG_ICHOR_CAUGHT_LERNIP`, `FLAG_DAILY_ICHOR_LERNIP_ROLLED`) are still to build |
| The nests' reeds | (7, 7) | Demeter's Sickle (held now) | A Sharp Beak and a hidden Heart Scale; Chalkip's dawn table is the lake's |
| The far rock | (29-30, 6-7) | Poseidon's Conch (held now) | A Shell Bell |
| Akanthis's door | (23, 27) | none yet | Proposal: her hut as a room (nets, a fire, the lime-pots) once the Lernip hunt lands |
