# Ascent_3F, above the cloud line

Builder: `tools/ichor/maps/propylon.py` (aethos + gTileset_Propylon, 44×62). The Chion build (`ascent_summit.py`) was retired on 2026-11-18.

- **Sentence:** out of the cloud, the old road becomes a processional stair that climbs three terraces to the Pantheon's propylaia, with nothing round it but sky and a sea of cloud.
- **Land:** the mountain's last shoulder: three walled terraces, a stair cut through each wall, the cloud sea on every side.
- **Settlement logic:** sacred ground, so the road is built: paving, tripods of every Archon, braziers at the platform; the Archon's guard holds the stairs, and keeps a watch-post on the stores.
- **Reveal:** at the top of the second stair the propylaia comes into view whole (the camera scene).
- **Signature:** the processional stair and the propylaia above the cloud.

## What's here

- **Awe:** the cloud-break scene at the arrival, and the first sight of the Pantheon at the second stair.
- **Trainer pairs** at each stair's foot (Sthenelos and Hippias; Melite and Korinna on the processional way), Gorgo on terrace 2, and **the gatekeeper, Polydamas** (67–69, Mortal/Spartan variants), who steps aside once beaten. Wild 60–64, the evolved Ice forms commonest.
- **New relic puzzle (2026-11-18): the Helm of Darkness.** A walled watch-post off terrace 3 has one way in; its watchman sends back anyone he can see. Under the Helm he looks through you. Its stores hold a **Choice Band** and a **Weakness Policy**.
- Finds: PP Up, Full Heal, Rare Candy, hidden Comet Shard and Star Piece. The travel herm by the propylaia (`town_herms.py`, Olympus).
- **Shrine:** Zeus Ombrios, fragment V of the hymn.

## Hooks for later

- **The four sockets** before a barred stair into the summit cone ("STAND STILL"): the Prime Mover's four keys (Arceus, POSTGAME §3.3).
- **The cloud bank that never clears** on terrace 2's east end: something whinnies inside; Aeolus's Bag of Winds moves it, toward Pegaunos's cloud meadows (D11, OIKOUMENE_GUIDE §15).

## Renders

- Before: `img/ascent_3f_before.png`. After: `img/ascent_3f_after.png`.
- Pass 1 cut the watch-post into terrace 3's west wall; pass 2 stepped the terrace edge with the post's pillars and moved the crystal that stood in the way; pass 3 checked the watchman's one cell of approach sits off the processional way, clear of the trainers' sight.

## Plan (2026-11-18 rework, outdoor on gTileset_Oros)

Rebuilt as snow terraces above the cloud, stepped by real cliffs with stairs cut into them, ending at the **grand entrance**: the Propylaia's columned marble facade on the cliff top, three screens wide.

- **The arrival:** up from Boreas's ridge (`Ascent_WindRidge`), the cloud-break scene as before.
- **Puzzle (the last, stealth):** the Helm of Darkness's watch-post: the watchman sends back anyone he can see; under the Helm he looks through you. Its stores hold the Choice Band and Weakness Policy.
- **The grand entrance:** the last stairway climbs the cliff with cloud on both sides, onto the plateau where the facade fills the screen: a pediment with Zeus and the eagle in gold, a red-and-gold frieze, a colonnade, bronze doors, two great braziers, and the statues of the Twelve, six a side. The first time you reach the foot of the last stair the camera climbs the facade to the pediment and back (`FLAG_ICHOR_SEEN_PANTHEON`).
- **Trainers:** both stair pairs, Gorgo, and the gatekeeper Polydamas, as before.
- **Post-game gates:** the four sockets (Arceus), the cloud bank (Pegaunos, D11), as before.
- **Easter eggs:** **the champion's statue**, an empty plinth among the Twelve whose inscription changes after the credits (it gets your name); **Aphrodite's dove and a scallop shell** at the lustral basin by the doors; **a laurel sprig** on the Hestia statue's plinth, the one Laurel left as an offering.

## Built (2026-11-18)

- **gTileset_Propylon**: the terraces, the facade and the processional way. The facade spans all 44 cells of the map's top: a 1-in-4 pediment (Zeus, the bolt, the eagle, the gods either side in gold on blue), a painted frieze (blue triglyphs, red metopes, gold rosettes), twenty Ionic columns from the shared kit (`tools/ichor/art/columns.py`, its `snow` variant) six cells tall with their capitals and shafts on the top layer (you walk behind them along the porch) and their shadows across the porch and the steps, the bronze doors four cells wide, three marble steps.
- **The statues of the Twelve** before it, six a side, are 32x64 objects drawn to the user's reference (`tools/ichor/art/statues.py`, `img/olympus_statues.png`): painted marble, teal plinths, each god's attribute. The empty champion's plinth gets your name after the credits.
- **The processional way:** broad marble stairs four wide, lit braziers at every stair's top and foot, lit tripods and the kit's columns along the way.
- **The facade's first sight:** at the top of the second stair the camera climbs the facade to the pediment, pans along it and comes back (`FLAG_ICHOR_SEEN_PANTHEON`); `ascent.sh` checks it.
- **Seams:** 3F is joined to Boreas's ridge (gTileset_Oros) by a connection; the two tilesets share their common terrain's metatile ids and the seam rows use only those (`seam_check`).
- **Herm and heal:** the herm stands by the processional way below the doors (19,16), its landing (20,16); `HEAL_LOCATION_OLYMPUS_PROPYLAIA` lands at (20,17).
- Renders: before `img/ascent_3f_before.png` (the walled terraces on Chion), after `img/ascent_3f_after.png`, screens `img/ascent_3f_after_screens.png`. Pass 1: a 21-wide facade with fat columns read as a hall; the user asked for the whole width, so pass 2 drew it wall to wall with taller columns; pass 3 rebuilt the colonnade on the shared kit at its standard pitch, moved the statues to objects (the reference's quality, no tiles), and lined the stairs with braziers.
