# Route 26, the Skiritis

Built by `tools/ichor/maps/stymphalia.py` (with Lake Stymphalia, Route 27 and the Skiritai cave). Renders: `img/lakonia_north_before.png` (Lakonia's roped north road) and `img/lakonia_north_after.png`; `img/route26_pass1.png`, `_pass2`, `_after` (with `_after_views`, `_after_walk`). The walk is `tools/ichor/tests/stymphalia.sh`.

## Brief

- **Sentence:** north past the battle school's grounds: the running track by the upper Eurotas, the practice field, the Platanistas in its moat, the fork with the great herm, then up into the Skiritis between two rock walls, with the Titan columns marching on the road below the east ridge.
- **Story:** the road opens after III-5J (`FLAG_ICHOR_LAKONIA_PARTED`): Rhea sends the player "by the road, make noise". The cadet who held Lakonia's north gap steps aside. The Wings still work, so this is the story's road (AETHOS_MAP Act III 6-7), the long way on purpose.
- **Signature:** the Platanistas: two bridges, Herakles's and Lykourgos's, onto an island of plane trees where the boys fight to throw each other in.

Tilesets: aethos and gTileset_Stymphalia (32x48, 10.2 screens). The six rows at Lakonia's seam keep to aethos, and Lakonia's top six rows keep to aethos over its x 15-35, which is all the camera can see from this side (`lakonia_town.py`, `NORTH_STRIP`).

## The walk, south to north

| Stretch | Terrain | Trainers | Grass |
|---|---|---|---|
| Lakonia's north road (aethos strip) | a sunken road between stone pines, the south sign | | |
| The running track | the oval track, turning posts, the starting sill | Anaxilas (easy, in view), Dromas | infield long grass |
| The practice field | open field between the moat and the woods | | band 1 (4 deep, wall to wall) |
| Herakles's bridge and the Platanistas | moat, plank bridge, island of planes, wrestling sands | **Anaxandros** (on the landing), Palaistes | island long grass |
| The fork | Lykourgos's statue, the great herm, the fork sign | Phrynon | |
| The Skiritis | two rock walls and the gap | **Dienekes** (in his niche, sight across the gap) | band 2 (4 deep) right behind him |
| The last rise | the scouts' meadow, the ridge's edge, reeds over the lake | Aipolos | the meadow |

Side areas: the west terrace (a ledged slope that hops home to the track: Kryptis, a Hyper Potion at its foot, a thicket pocket), the Phoibaion behind its cracked rock (Argeios the deserter, Honey on the altar step, a Pearl in the brook), the moat's islet (a Big Pearl, the Conch).

Set pieces: the wrestling cadets (one gives the team's Muscle Band), the Titan columns walking in place on the lower road (hidden after the climax), the columns sign on the ridge's edge.

Finds: Honey, Rare Candy, Big Pearl, Ultra Ball, Hyper Potion; hidden Star Piece (the biggest plane), Pearl (the brook), PP Up (the starting sill), Escape Rope (Dienekes's rock), Revive (behind the herm).

Wild (all four times): Hoplomex, Cairnolith, Kerazap, Dorydrake, Gelasable, Chelonet, Hoplektor, Nemeleon (dusk), Harpelle (day), Kalyptor (night), 47-49. Surf and rods in the moat and the river. Rock Smash at the Phoibaion.

## Hooks for later

| Gate | Where | Relic | Behind it |
|---|---|---|---|
| The Phoibaion's rock | (18, 15) | Bronze Hammer (held now) | The altar pocket: Honey, the deserter, a hidden Pearl |
| The terrace thicket | (1, 25) | Demeter's Sickle (held now) | A Rare Candy |
| The moat's islet | (7, 29) | Poseidon's Conch (held now) | A Big Pearl |
| The Titans' lower road | (27-29, 0-16), past the ridge | none; it's never reached | The columns march north until the climax; after it, the empty road and "a helmet full of rain" (the columns sign). Proposal: a post-game way down onto it for the Titanborn remnants' rematches |
| The Platanistas at dawn | the island | time of day (proposal) | SCRIPT's dawn fight between the two teams as a morning-only scene with a prize |
