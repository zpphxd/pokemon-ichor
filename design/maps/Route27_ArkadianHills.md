# Route 27, the Arkadian hills, and the Skiritai cave

Built by `tools/ichor/maps/stymphalia.py`. Renders: `img/route27_pass1.png`, `_pass2`, `_after` (with `_after_views`, `_after_walk`); `img/skiritai_cave_pass1.png`, `_after`.

## Brief

- **Sentence:** west from the lake and up over the old Lakonian-Arkadian border: a valley between rock walls, a ravine with one bridge, the Karyai spring under walnuts, and a pass through the pines into Arkadia's south road.
- **Signature:** the Karyai spring, where the maidens danced for Artemis, as the road's last rest; and the watchtower on the lookout spur, from which "you can see the lake, the road, and all of Lakonia. No walls."
- **Relics:** this is the road's relic map. Almost everything the player holds opens something here.

Tilesets: aethos and gTileset_Stymphalia (44x36, 10.6 screens); the cave is cave_dark (30x20, dark). The six rows at Arkadia's seam keep to aethos (Arkadia's bottom six already do). Arkadia's south road, which ended against limestone with the Karneia hoplite on it, now opens onto this route; the hoplite steps aside once III-5J is done (`FLAG_ICHOR_LAKONIA_PARTED`), so nobody walks into Lakonia ahead of the story.

## The walk, east to north

| Stretch | Terrain | Trainers | Grass |
|---|---|---|---|
| From the lake | the valley floor, Tityos's goats, the east sign | Tityos (easy, in view), Kore | |
| The hollow | between the cliff and the ridge | | band 1 (3 deep, wall to wall) |
| The narrows | a crag on the north side | **Lochagos** (in his niche) | |
| The ravine bridge | the ravine, one plank bridge | **Othryades** (at the far landing) | band 2 (4 deep) right behind him |
| The Karyai spring | walnuts, the spring (heals), the great herm, the fork sign | Karyatis | the verges |
| The top of the pass | two rock walls and the gap | **Sthenelaidas** (in his niche) | band 3 in the pines (3 deep) |
| Arkadia's pines (aethos strip) | stone pines and cypresses, the north sign | Kynegos | |

Side areas: the west meadow (Agria, Phoros, a Hyper Potion), the lookout spur (Skopos, the drum yard and the watchtower), the cut stair up the cliff to the high ledge (Anabates, TM Aerial Ace), the Skiritai cave and the scouts' terrace it climbs to (an Ultra Ball, a hidden Elixir; its wall drops back to the valley), the Titans' cache in the ridge.

## The relics

| Relic | Where | What it does |
|---|---|---|
| Girdle of Herakles | the drum yard, (27-38, 12-15) | Two column drums onto two grooved sills (`R27_DRUMS`, `R27_PLATES`) drop the old plank over the lookout's chasm (`FLAG_ICHOR_R27_LOOKOUT_PLANK`). The scouts' post at (27, 12) resets it. `check_seal()` proves it solvable (7 pushes) on every build |
| Daedalus's Wings | the updraft, (39, 13) | Rides across the cleft to the pinnacle's nest: a Rare Candy |
| Horn of Achelous | the cascade, (2, 10-12) | Climbs the spring's overflow to the basin above: a Mystic Water |
| Ariadne's Thread | the anchor ring, (8, 24) | Down to a ledge in the ravine: a Nugget |
| Helm of Darkness | the Titans' cache, (33-38, 31-32) | The watchman's eye sends you back at its door (35, 31) unless the Helm is on: a Full Restore and a hidden Rare Bone |
| Hecate's Torch | the Skiritai cave | The cave is dark; its brazier (`FLAG_ICHOR_BRAZIERS_START + 0x60`) lights it for good |
| Bronze Hammer | the cave's gallery, rubble at (14, 10) | A Hard Stone, a hidden Star Piece by the bones, a Max Ether in the crawl |
| Labrys | the scouts' store, chains at (6, 5) | TM Rest and a hidden Dusk Stone |

The watchtower's own TM is Steel Wing (SCRIPT named Stone Edge, which isn't one of Ichor's 61 TMs).

Finds on the route: TM Steel Wing, Rare Candy, Mystic Water, Nugget, TM Aerial Ace, Full Restore, Ultra Ball, Hyper Potion; hidden Big Nugget (the tower's foot), Revive (the walnut nearest the spring), Rare Bone (the cache), Elixir (the terrace), Stardust (the pines). In the cave: TM Rest, Hard Stone, Max Ether, Super Potion; hidden Dusk Stone, Star Piece, Ether. Cave trainers: Krypte on the climb, Arktos at the climb's top.

Wild (all four times): Cairnolith, Kerazap, Chelonet, Hyphantis, Gelasable, Nemeleon, Harpelle, Chelyra, Enigmaw by day; Lykanax and Kaprodon at dusk and night, 48-50. The cave: Cairnolith, Plouteras, Hyphantis, Kalyptor, Chelonet, Enigmaw, Sophowl, 48-50, with Rock Smash and its pool's rods.

## Hooks for later

| Gate | Where | Relic or event | Behind it |
|---|---|---|---|
| Ares's gully | the ridge, sign at (20, 31) | theoxenia E4 (SCRIPT Part 1), not built | The ambush double battle (Aulax and Gaieos with Ares's veteran beside you) on the lower road |
| The Titans' lower road | (3-43, 33-34) | none; never reached | The columns march west in place until the climax. Proposal: the same post-game way down as Route 26's |
| The watchtower's door | (42, 8) | none yet | Proposal: the Skiritai's last scout, a post-game rematch |
| The scytale | Othryades | `FLAG_ICHOR_GOT_SCYTALE_STRAP` (SCRIPT Part 3) | His after-battle scytale reading ("THIRD PLANE TREE. DIG.") is not wired yet: Gylippos's strap and the dig need the Lakonia builder's flags |
| Karyai's berry trees | the spring | none | SCRIPT's two berry trees under the walnuts need berry-tree ids; not placed |
