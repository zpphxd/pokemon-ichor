# Ideas to come back to

Things the user wants built later. Nothing here is scheduled; each entry says what the idea is and when it might land. Add new ideas at the bottom of their section, and move an entry to "Done" with the commit when it's built.

## Places

### Lebadeia: a temple rest stop
- **Now:** a bare outdoor hamlet between Route 8 and Route 9, with an outdoor healer, a merchant and one sign (no buildings).
- **Idea (user, 2026-11-17):** a temple stands here as a rest stop for travelers.
- **Later:** a side quest, perhaps in the post-game. Trophonios's oracle cave (AETHOS_MAP.md's proposal: an optional dark cave for the Torch, entered feet first) fits it.
- **Built (2026-11-17, tools/ichor/maps/kopais.py):** the Trophoneion, Lebadeia's temple, rest-house and Asclepeion, with the honey-baker's house and the springs of Lethe and Mnemosyne. The oracle's descent is sealed (the roped stair inside, the grilled mouth outside); the side quest's hooks are in design/maps/Lebadeia.md under "Hooks for later".

### Every route: a design and complexity pass
- **Idea (user, 2026-11-17):** improve all the routes, both how they look and how complex they are to explore.
- **The model:** Route 6 and Mt. Kithairon's rebuild (tools/ichor/maps/kithairon.py): trainers on chokepoints you can't walk around, forced grass, ledges and one-way shortcuts, terrain that reads (climbs, cliffs, water), optional branches with rewards, and three render → critique → fix passes.
- **Also for each route:** fuller time-of-day wild tables, fishable water with a fishing table, relic gates that invite a return, and a landmark per screen.
- **Relics and terrain (user, 2026-11-17):** use the relics (our HMs) much more, with gates the player can open now as well as ones for later, and vary the terrain so each route is a different place: marsh, scree, rivers and fords, terraces, forest, beaches, grottos.
- **First up when it lands:** Route 7 (Kronia Grounds) and Routes 8–9 around Lebadeia, which the user asked about; then Routes 1, 4 and 5, and every route after.
- **In progress (2026-11-17):** Routes 7, 8, 9, 11, 13 and 14, with the bare stops (Lebadeia, Kirrha, Aigion, Nemea) each getting a temple, shrine or outcamp that can carry a later quest. Routes 1, 4, 5 and the rest are still to come.

### The whole world: hidden parts and return gates
- **Planned (2026-11-17):** `design/WORLD_EXPLORATION.md` plans every region's return gates, cave back sections and what pays behind them (story, stronger Pokémon, leads), proposes Pan's Crook as the climbing relic, and gives a build order.

## Queued (user, 2026-11-17): start when the Act III helpers free up

### First: herm fast travel, made clear and early (user, 2026-11-17)
- A great herm stands right at each town's entrance, easy to spot, with a sign that names it a travel stop.
- A town's herm registers the first time you use its Asclepeion or touch the herm. No Olive Oil needed (anointing can stay as a Favor rite).
- Travel works from the start: touch any herm and pick a registered town. Daedalus's Wings later let you fly from anywhere (SYSTEMS §4 and §1 need updating).

### The road north from Lakonia: Route 26, Lake Stymphalia, Route 27
- Lakonia's north road is roped off with a cadet for now; the player leaves by Wings. Build the walkable road to today's standard (a cave or climb, the Stymphalian marshes with their birds, a midpoint rest with a herm). It needs its own flag and trainer range (claim_ranges.md).

### Wild Pokémon distribution pass
- **Problem found:** Act II adds only 10 new species; Galenyon, Cairnolith, Pebblith, Kerazap, Gelasable and Galekit fill 40–57 maps each; about 18 regular lines can't be caught wild in the story (Chalkip, Elegull, Elektear, Erosie, Hymnet, Kalliglyph, Kerdovix, Skylaps, Sepidart, Sporadon, Ophidrop, Pagoshard, Lebetron, Bouldyphus, Enigmaw, Aetling and more); Nebrel, a starter, is wild on Routes 7–9.
- **Plan:** a species-by-area table first, then apply it: one or two signature species per area, Act II gets its own new species, each evolution line gets a catch point before its evolution level, the filler thins out, starters leave the wild, rares go to night, fishing, rock smash and hidden spots.

### Day care: the Nursery of Nysa (Route 7, outside Thyrsa)
- The nymphs of Nysa raised Dionysus. A standard day care (levels, eggs); Hera's blessing already doubles egg finding (SYSTEMS).

### Safari Zone: the Erymanthian Preserve (beside Arkadia)
- Artemis's hunting park on Mount Erymanthos. Entry fee, Pan Balls (the renamed Safari Ball), a step count, rare and missing species by time of day; ties to the boar Labor in the post-game. Pairs with the distribution pass.

### Grand bazaar: the Great Deigma (Emporion)
- A covered market of many stalls: foreign traders (Phoenician, Egyptian, Scythian), stones, TMs, berries, a daily rare stall and a coin exchange for Obols and Staters. A reason to sail back.

### The Ascent of Olympus: Ichor's Victory Road (user, 2026-11-17)
- **Awesome:** a long climb from the foothills to the clouds, over many floors with mixed terrain: caves, cliff ledges and switchbacks, an ice band, and a stretch above the cloud line.
- **Somewhat difficult:** strong trainer pairs on narrow paths you can't avoid, tougher wilds, puzzles that use every relic held, limited healing with one midpoint shrine, and a gatekeeper battle before the Pantheon.
- **Lots to find:** rare items, TMs, evolution stones, top held items, artifacts and amphora sherds, and an Olympian story fragment at each floor's shrine.
- **Post-game hooks everywhere:** sealed doors, boulders, falls and Pan's Crook cliffs toward the post-game peaks (Pegaunos above the clouds, the Moment's shrine), and side paths you can see but can't reach until after the credits.
- **Puzzles (user):** boulder-on-switch Strength puzzles (Girdle drums onto pressure plates, plates that must all be covered, drums as stepping stones), with a safe reset, as in the Labyrinth.
- **Built with:** the Elite Four (Pantheon) and Archon upgrade: new halls, teams rebalanced for team-wide EXP, a short scene before each battle.
- **Then:** a natural-level balance playthrough of the whole game (party level at each Laurel), raising trainers and bosses where the player is too far ahead.

## Done
