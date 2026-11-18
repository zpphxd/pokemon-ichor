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
- **Built (2026-11-18, `tools/ichor/maps/sacredway.py`):** Route 15 (the Rheitoi, the Aigaleo pass, the shrine court's drum seal), Daphni (the sanctuary of Apollo Daphnaios, the lookout, three rooms) and Route 16 (the Kephisos, the Kerameikos, the Akademia, the climb and the first sight of the Akropolis). Hooks: `design/maps/Route15_MysteryRoad.md`, `Daphni.md`, `Route16_CapitalPass.md`; the walk is `tools/ichor/tests/sacredway.sh`.

### The whole world: hidden parts and return gates
- **Planned (2026-11-17):** `design/WORLD_EXPLORATION.md` plans every region's return gates, cave back sections and what pays behind them (story, stronger Pokémon, leads), proposes Pan's Crook as the climbing relic, and gives a build order.

### The Oikoumene and the post-game epics, at the new bar
- **Planned (2026-11-17):** `design/OIKOUMENE_GUIDE.md` is the build-ready guide for the ten lands and the epics: the bar every land passes, where every other generation lives, each land's maps, stops, roads, puzzles, gates, species and story, the art and ROM, a build order (the Troad first), and proposals P-1 to P-11 for the user.

## Queued (user, 2026-11-17): start when the Act III helpers free up

### The road north from Lakonia: Route 26, Lake Stymphalia, Route 27
- Lakonia's north road is roped off with a cadet for now; the player leaves by Wings. Build the walkable road to today's standard (a cave or climb, the Stymphalian marshes with their birds, a midpoint rest with a herm). It needs its own flag and trainer range (claim_ranges.md).
- **Built (2026-11-18, `tools/ichor/maps/stymphalia.py`):** Route 26, Lake Stymphalia, Route 27 and the Skiritai cave, opened by III-5J as the story's road to Arkadia (the Wings still work). 31 trainers, Akanthis's rest and the lake's travel herm, two route herms, the bronze flock's first-crossing scene, and nine relics in use. Finds and hooks: `design/maps/Route26_Skiritis.md`, `LakeStymphalia.md`, `Route27_ArkadianHills.md`; the walk is `tools/ichor/tests/stymphalia.sh`. Still open: the deep reeds' rainy Lernip roll, Ares's gully (theoxenia E4), the scytale reading, the Karyai berry trees.

### The Ascent of Olympus: Ichor's Victory Road (user, 2026-11-17)
- **Awesome:** a long climb from the foothills to the clouds, over many floors with mixed terrain: caves, cliff ledges and switchbacks, an ice band, and a stretch above the cloud line.
- **Somewhat difficult:** strong trainer pairs on narrow paths you can't avoid, tougher wilds, puzzles that use every relic held, limited healing with one midpoint shrine, and a gatekeeper battle before the Pantheon.
- **Lots to find:** rare items, TMs, evolution stones, top held items, artifacts and amphora sherds, and an Olympian story fragment at each floor's shrine.
- **Post-game hooks everywhere:** sealed doors, boulders, falls and Pan's Crook cliffs toward the post-game peaks (Pegaunos above the clouds, the Moment's shrine), and side paths you can see but can't reach until after the credits.
- **Ice Pokémon as you climb (user):** the wild tables turn colder floor by floor. Niflake and Kryopuff in the snowline caves, Chionyad (the snow nymph) and Borapteryx (Boreas's wind) on the ice band, Krystolos in the crystal caves, Pagoshard (no wild home yet) on the glacier, and Stygiad in the coldest dark. Their evolved forms near the peak, with an Ice trainer or two among the gatekeepers.
- **Puzzles (user):** boulder-on-switch Strength puzzles (Girdle drums onto pressure plates, plates that must all be covered, drums as stepping stones), with a safe reset, as in the Labyrinth.
- **Built with:** the Elite Four (Pantheon) and Archon upgrade: new halls, teams rebalanced for team-wide EXP, a short scene before each battle.
- **Then:** the user plays the whole game themselves (user, 2026-11-18) and reports where it's too easy or slow; balance changes come from their notes.
- **Built (2026-11-17/18, origin `ascent-wip`):** seven Ascent floors (1F, 2F, the Icefall with ice sliding, the Deep, the Crystal Vault, the Glacier, 3F above the cloud) and the summit rebuilt on gTileset_Chion; trainer pairs at every chokepoint and the gatekeeper Polydamas; the cook's camp as the one midpoint heal and herm; Girdle seals in the Icefall and at the Gate of the Winds (with reset levers); every relic used (Sickle, Hammer, Girdle, Torch, Conch, Labrys, and the Horn's meltwater fall, the Wings' updraft, the Thread's crevasse and the Helm's watch-post); the Ice Pokémon floor by floor; hymn fragments I–V at the floors' shrines; the Pantheon's pre-battle scenes and the League's teams at 59–75. Each map's finds and post-game hooks are in `design/maps/Ascent_*.md`, `Olympus_Summit.md` and `Olympus_Pantheon.md`; the walk is `tools/ichor/tests/ascent.sh`. Still open: the balance playthrough above, and LEAGUE.md's art list.

## Queued next (user, 2026-11-18)

### Labyrinth identity pass
- Rings I–IV read as the same grey brick with red markers. Give each ring its own colour and fresco motif per LABYRINTH_MAZE §2 (bulls, dolphins, lilies, griffins, octopus and argonauts, double axes, stars), with floor and wall variants and one big landmark per screen.
- The treasure cellars are plain boxes; make each a small treasure room worth the climb (Minoan pithoi, gilded frescoes, an altar, a fallen explorer's cache).

### The architecture pass across the world (after Astyra lands)
- Once Astyra's STYLE.md "Architecture: Gen 3 craft and Greek forms" section and the shared column kit are in and approved, apply them to every city and temple in waves of two or three helpers: Emporion, Thyrsa, Eleusa (and the Telesterion), Arkadia, Delphoi (with AWE_PASS item 7), Knossa, Lakonia, Kythera's towns, the eight Laurel temples, and the ruins (with the ruins kit, AWE_PASS item 6). Same layouts and story; better facades, columns, platforms, rooflines, landmarks and ruins.
- Check every city's render against the new rules first, and fix the worst ones first.

### The awe pass
- Build from design/AWE_PASS.md's top 10 (colossi, grand temples, city improvements, the ruins kit) once the user picks.

## Done

### Day care: the Nursery of Nysa (Route 7, outside Thyrsa)
- The nymphs of Nysa raised Dionysus. A standard day care (levels, eggs); Hera's blessing already doubles egg finding (SYSTEMS).
- **Built (2026-11-18):** the farmhouse and its glade on Route 7, Makris and Aristaios, the deposited Pokémon roaming the glade (`src/ichor_nursery.c`), Hera's doubling kept; `design/maps/NurseryOfNysa.md`, `tools/ichor/tests/nysa_deigma.sh`. Proposed Day Care term: the Kourotrophion (TERMS).

### Grand bazaar: the Great Deigma (Emporion)
- A covered market of many stalls: foreign traders (Phoenician, Egyptian, Scythian), stones, TMs, berries, a daily rare stall and a coin exchange for Obols and Staters. A reason to sail back.
- **Built (2026-11-18):** behind the stoa's east door: nine stalls (Hiram of Sidon, Amasis of Naukratis, Skyles the Scythian, stones, techniques, berries, the daily curio stall, spices, pots), Phormion's trapeza for coins, stock that grows after the 4th and 7th Laurels; `design/maps/GreatDeigma.md`. Still open: walkers drawn for the three foreign traders (they use the shared sailor, acolyte and harvester sprites).

### Wild Pokémon distribution pass
- **Problem found:** Act II adds only 10 new species; Galenyon, Cairnolith, Pebblith, Kerazap, Gelasable and Galekit fill 40–57 maps each; about 18 regular lines can't be caught wild in the story (Chalkip, Elegull, Elektear, Erosie, Hymnet, Kalliglyph, Kerdovix, Skylaps, Sepidart, Sporadon, Ophidrop, Pagoshard, Lebetron, Bouldyphus, Enigmaw, Aetling and more); Nebrel, a starter, is wild on Routes 7–9.
- **Plan:** a species-by-area table first, then apply it: one or two signature species per area, Act II gets its own new species, each evolution line gets a catch point before its evolution level, the filler thins out, starters leave the wild, rares go to night, fishing, rock smash and hidden spots.
- **Built (2026-11-18):** design/DISTRIBUTION.md, applied by tools/ichor/wild_plan.py through every builder (tools/ichor/maps/plan_hook.py) and checked by tools/ichor/distribution.py in the smoke test. Act II now introduces 26 lines (12 before); no starter is wild; all 17 missing or late lines have a catch point before the League.

### Safari Zone: the Erymanthian Preserve (beside Arkadia)
- Artemis's hunting park on Mount Erymanthos. Entry fee, Pan Balls (the renamed Safari Ball), a step count, rare and missing species by time of day; ties to the boar Labor in the post-game. Pairs with the distribution pass.
- **Built (2026-11-18):** tools/ichor/maps/erymanthos.py: the keeper's lodge on Arkadia's west road, the Oakwood, the High Meadow, the River, the Cold Cave and the post-game Boar's Thicket (FLAG_ICHOR_ERYMANTHIAN_BOAR, for Labor 4 to set). ¥500, 30 Pan Balls, 500 steps, barley and stones (include/config/ichor.h); design/maps/ErymanthosPreserve.md; tools/ichor/tests/preserve.sh.

### Labyrinth hookups (built 2026-11-18)
- The Turning (tools/ichor/maps/labyrinth_turning.py, design/maps/Labyrinth_System.md), Scene L at dawn in the workshop,
  Klytios in Ring VII after a Ring IV fight, Scene J's bull-leaps (fixed and tested), the remains, Kronos, Gigas and
  tablet art. Still open: Labyrinth music cues (LABYRINTH §11).

### Herm fast travel, made clear and early (user, 2026-11-17)
- A great herm stands right at each town's entrance, easy to spot, with a sign that names it a travel stop.
- A town's herm registers the first time you use its Asclepeion or touch the herm. No Olive Oil needed (anointing can stay as a Favor rite).
- Travel works from the start: touch any herm and pick a registered town. Daedalus's Wings later let you fly from anywhere.
- **Built (2026-11-17):** 19 towns' entrance herms and plaques (tools/ichor/maps/town_herms.py), healer and touch registration, the travel menu from any herm (SYSTEMS §4, ENGINE_API §4), the rule in MAP_DESIGN §2 and its audit (tools/ichor/herm_audit.py), and tools/ichor/tests/town_herms.sh.
