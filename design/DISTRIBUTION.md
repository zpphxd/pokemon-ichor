# Ichor's wild Pokémon: the distribution plan

Where each Aethos Pokémon lives, area by area in story order. The user's north star is "a new world never explored": each place should feel like it has its own wildlife. This plan is the IDEAS.md "Wild Pokémon distribution pass" (2026-11-18). It pairs with the Erymanthian Preserve (§4).

- **The tables:** `src/data/wild_encounters.json`. Each map's builder writes its own tables. `tools/ichor/wild_plan.py` then applies this plan on top, and every builder calls it through `tools/ichor/maps/plan_hook.py` just before it writes, so a rerun keeps the plan. Stymphalia's maps carry their changes in `tools/ichor/maps/stymphalia.py`'s own `LAND` data.
- **The check:** `tools/ichor/distribution.py`, run by the smoke test together with `wild_plan.py --check`. It fails when:
  - a starter line is wild;
  - a legendary, mythical, fossil or post-game line is wild in the story (except where the user placed it: Stygiad, below);
  - a regular Aethos line has no wild catch point before the League, or its first stage is only ever wild at or past its evolution level (the Ascent counts as the League's Victory Road);
  - a non-Aethos species is wild in the story;
  - an evolved form is wild below the level it evolves at;
  - a map has wild tables but no place in the story order.
- **The tables below** are generated: `tools/ichor/distribution.py --report` prints them. Regenerate this file's §5 after changing any table.

## 1. Rules

1. **Signature species.** Every area has one or two species found mainly there (§3). The mainland's commons (the weasels, Pebblith and Cairnolith, the goats, Galenyon on land) are thinned to the places they belong: farms and Act I roads, caves and rubble, hills, and coasts.
2. **A catch point before evolution.** Every regular line can be caught as its first stage below the level it evolves at, somewhere before the League. For a baby line this means its second stage (the baby hatches from an egg). A line that evolves by stone, trade, friendship or place only needs its first stage wild.
3. **Late lines start early.** BALANCE.md's late-area rule says that from Astyra on, a line whose evolution level is below the area's band appears only as its evolved form. So a line whose home is late in the game (the Kouretes, the Spartoi, the Python, the swans, the Stymphalian birds) has its first stage placed in an Act II area that fits its myth, at Act II levels. Its home area keeps the grown form.
4. **No starters in the wild.** The three starter lines are given at the Akademia and return in the post-game (PITCH). Nebrel, Kladoe, Daphnyad and Seismare have all left the wild tables. Trainers keep them.
5. **Rares.** Rare species go:
   - at night: owls, wolves, the Teumessian vixen, Amnoze;
   - on the rods: Hymnet, Lernip;
   - under Rock Smash: Pithound in amphora rubble, Geogrip in the Tretos;
   - in the 1% slots;
   - behind gates: the Preserve's fee, the Conch's water, the post-game thicket.
6. **Levels.** Every table keeps BALANCE.md's band for its stage, at most five levels wide. A rare low-level first stage is the band's floor or one level under it. That is BALANCE's "rare lower-level spot", and it is used for Kaldera's Kaminoo and Pyrapod.
7. **Held back.** These stay out of the main story's wild tables:
   - legendaries and mythicals;
   - the post-game lines (the Sirens, Scylla and Charybdis, Proteus, Argos, Ladon, Sisyphus);
   - the fossils;
   - the story statics (Asterlorn, Echolali's pool).

   **Stygiad** is the one exception, at the user's own ask (IDEAS, the Ascent: "Stygiad in the coldest dark"). It now lives only in the Icefall Deep and the Crystal Vault.
8. **Aethos only.** The main story's wild tables hold Aethos species only (BALANCE, "Aethos's trainers use Aethos's Pokémon"). The other generations belong to the Oikoumene and the post-game.

## 2. Before and after

| | Before the pass | After |
|---|---|---|
| Act I: new species / new lines | 29 / 23 | 31 / 24 |
| **Act II: new species / new lines** | 28 / **12** | 44 / **26** |
| Act III: new species / new lines | 42 / 23 | 36 / 13 |
| Starter lines in the wild | 4 species on 11 maps | none |
| Regular lines with no catch point before the League, or only past their evolution level | 17 | none |
| Evolved forms wild below their evolution level | 38 slots | none |
| Widest in the land tables (maps) | Gelasable 29, Cairnolith 28, Kerazap 23, Harpelle 21, Galenyon 21 | Harpelle 20, Cairnolith 20, Lykanax 19, Melibee 18, Gelasable 18 |

"New lines" counts each evolution line at its first wild catch. Act III now has fewer new lines because their first stages moved into Act II (rule 3). Its areas keep the grown forms as their signatures, and Kythera and Knossa keep their own lines.

The "before" column is the tables before this pass and before the Stymphalia merge. Act II's after count includes the Preserve.

**Lines fixed** (none had a catch point before the League, or their first stage was only wild past its evolution level):

| Line | Its catch point now |
|---|---|
| Pithound | Rock Smash rubble on Routes 4 and 5 (Act I) |
| Skylaps | Route 12 and the Arkadian cypress wood (rare), the Preserve |
| Kerdovix | Mt Kithairon at dusk and night (1%), the Preserve at night |
| Glaukoin | Routes 13–15, Nemea and the Tretos at dusk, the Preserve's Oakwood at night |
| Ophidrop | Route 16 |
| Kaminoo | Kaldera at 32 (rare) |
| Kapnub | Kaldera's caldera floor |
| Kymbash | Route 11, the Drum Pass |
| Chalkip | Lake Kopais's reeds (Route 8), the Preserve's river |
| Sporadon | Route 7, the Kronia grounds |
| Pelython | The Korykian Cave |
| Pyrapod | Kaldera at 32–33 (rare) |
| Hymnet | Lake Kopais's water and rods, the Preserve's river |
| Aetling | Route 13, Route 16, the Preserve's High Meadow |
| Kryopuff | The Preserve's High Meadow and cave |
| Pagoshard | The Preserve's cold cave |
| Lebetron | The Ascent 1F |
| Lernip | The Preserve's river: the 1% surf and Super Rod slot, at 29 (BALANCE's "about level 30") |

Lake Stymphalia now exists, but at Lakonia's 46–50 band. Lernip's rain hunt stays a hook there (`FLAG_ICHOR_HEARD_LERNIP_RUMOR`), at Lakonia's levels.

Also new: Alekrow, the middle cockerel, in Eleusa's farmyards; Psychora at Aphaia's temple.

## 3. Signature species, area by area

| Area | Signature | Why |
|---|---|---|
| Route 1, Kronion Hill | Epopoi, Kampillar; Kerazap, Narthip | The hoopoe's road and the soul-butterflies; the hill's goat and fennel |
| Aegina's roads | Ergant (all three), Chelonet (Aphaia road), Psychora (the temple), Kerazap and Harpeck (Mount Oros) | The Myrmidons' island; its coins' turtle; the vanished nymph's temple; the goat crags and sea cliffs. Obolorn and Onotis at night, for the first coins |
| Route 4, Route 5 | Nemecub, Harpeck; Pithound under rubble | The golden cub; the cliffs' harpies; the jar-dog in broken amphorae |
| Hecate's Hollow | Gelasable, Obolorn at night | Galanthis, the weasel Hecate took in; the shades |
| Eleusa | Stachyss, Kaplet, Alekrow; Rhoaril in the sanctum | Demeter's wheat, the Mysteries' piglet, the farmyard cocks; the seed of Persephone |
| Route 6, Mt Kithairon | Ampelix, Botrykit; Kerdovix (rare, night) | Dionysus's vines and leopards; the Teumessian vixen that plagued Thebes |
| Thyrsa, Route 7 | Midonos; Sporadon | Midas's gold; the Spartoi, the men sown at Thebes |
| Route 8, Lake Kopais | Chalkip, Hymnet | The reed marsh's bronze chicks and cygnets |
| Kopais's katavothres | Raknit, Obolorn | Sinkholes into the dark |
| Route 9, the crossroads | Enigmaw (dusk and night), Eripip | The Sphinx on the road to Delphoi, where Oedipus met his father |
| The Korykian Cave | Pelython | The Python's young, in Parnassos's cave |
| Route 11, the Drum Pass | Kymbash | The Kouretes' cymbal-clashers among the column drums |
| Route 12, the cypress wood | Arkoby, Raknit, Lykopup; Skylaps (rare) | Kallisto's bears, Arachne's webs, Lykaon's wolves; Artemis's hound |
| **The Erymanthian Preserve** | Skylaps and Kerdovix, Glaukoin (night), Kryopuff, Aetling, Chalkip, Hymnet, Pagoshard, Lernip | §4 |
| Route 13 | Aetling, Glaukoin (dusk) | Eagle chicks over the uplands; Athena's owlets |
| Nemea, Route 14, the Tretos | Nemeleon; Geogrip (rare, Rock Smash in the Tretos) | The lion's country; Antaeus's wrestler, for Nemea's palaestra |
| Route 15, the Mystery Road | Korantha by day, Persenyx at night, Melisseer | Kore on the Eleusinian procession's road; Demeter's Melissai |
| Route 16, the capital pass | Sophowl, Ophidrop | Athena's owls on the road to Astyra; the Asklepian snakes |
| The Salt Well, Astyra's harbor | Narkeray, Karkitox, Kynoketos | Poseidon's salt spring (Seismare gone) |
| Kaldera | Taurivet, Kapnub; Kaminoo and Pyrapod (rare, young) | The bronze bulls, the Gigantes' young, the forge tripods |
| The Telchines' forge | Telpup, Telkanvil | The smith-spirits' pool |
| Kythera | Aphrell, Narcibulb, Glyphlet, Himerow; Echolali at night | Aphrodite's foam, Narcissus's spring, Galatea's marble, Eros |
| Knossa, the Bull Road | Taurivet, Ikaroth; Oinopard, Korantha (the vineyard); Kolossette (the Bronze Heel) | The bull's island, Talos's coast |
| The Labyrinth | Mitoclew, Kourodin, Gigantomb | Ariadne's thread, the Kouretes grown, the buried giants |
| Route 25, the Eurotas | Hymnaria, Stachypter, Belornis | Leda's swans on Sparta's river |
| Lakonia, Route 26 | Dorydrake, Hoplektor, Nemeleon | The Spartoi grown, the battle cocks, the hills' lions |
| Lake Stymphalia | Belornis, Hymnaria | The bronze-feathered birds |
| Route 27, the Arkadian hills | Chelyra, Starkos, Hyphantis, Enigmaw | Hermes's lyre-tortoise on Kyllene, Kallisto as the bear, Arachne |
| Delphoi, Route 28 | Pythoros, Hymnaria, Elektear, Mantipod; Hierolive (the Sacred Olives) | The Python, Apollo's swans, the Heliades' amber tears, the tripod |
| The Ascent | Floor by floor colder (the user's plan): Niflake and Kryopuff, Chionyad and Borapteryx, Krystolos, Pagoshard; Lebetron in the foothills; Stygiad in the Deep and the Vault | IDEAS, the Ascent |

## 4. The Erymanthian Preserve

Artemis's hunting park on Mount Erymanthos, beside Arkadia. It is Ichor's Safari Zone: upstream's engine, switched back on with `ICHOR_SAFARI_PRESERVE` in `include/config/ichor.h`. The maps are built by `tools/ichor/maps/erymanthos.py`. Their design and finds are in `design/maps/ErymanthosPreserve.md`.

- **The hunt.**
  - The keeper's lodge stands at the end of Arkadia's west road.
  - The fee is ¥500. It buys 30 Pan Balls and 500 steps.
  - FRLG's bait and rock return as barley and a stone, standing in for the cut Pokéblocks.
  - The start menu shows the steps and balls left.
  - The keeper's bell at the gate ends the hunt early.
- **Levels:** 28–32, at Arkadia's stage. The Thicket runs 58–62 (post-game).

| Area | By day | At night | Water and rods |
|---|---|---|---|
| The Oakwood | Kaplet, Arkoby, Skylaps, Raknit, Lophops, Eripip; Kerdovix and Kaprodon (rare) | Glaukoin, Lykopup, Amnoze, Kerdovix; Lykanax (rare) | — |
| The High Meadow | Eripip, Chelonet, Aetling, Kryopuff, Melibee; Kerazap and Skylaps (rare) | Amnoze, Kryopuff, Lykopup; Kerdovix, Glaukoin and Lykanax (rare) | — |
| The River | Chalkip, Hymnet, Melibee, Kaplet, Halcyling | Chalkip, Lykopup, Amnoze, Glaukoin; Kerdovix (rare) | Hymnet, Ketofry, Karkitox, Kynoketos; **Lernip** (1%) |
| The Cold Cave | Pagoshard, Spalunk, Pebblith, Raknit, Obolorn, Kryopuff | the same | Ketofry, Karkitox, Hymnet, Kynoketos |
| The Boar's Thicket (after Labor 4) | Kaprodon, Kaplet, Borapteryx, Lykanax, Krystolos, Chionyad, Starkos; Skylaps, Kerdovix | the same | — |

## 5. Species by area (generated)

Each cell lists a table's species, commonest first. A species is **bold** where it is first met in the story. "Water and rods" merges the surf table and the three rods.

### Kalliste (Act I)

| Map | Land by day | Land at night | Water and rods | Rock Smash |
|---|---|---|---|---|
| KALLISTE_ROUTE1 | **Epopoi**, **Kampillar**, **Ergant**, **Galekit**, **Elaleaf**, **Eopeep** | Galekit, Elaleaf, Ergant, **Pebblith**, Kampillar | **Ketofry**, **Karkipool**, **Halcyling**, **Narkeray** |  |
| KALLISTE_ROUTE1_KRONION_HILL | Pebblith, Ergant, Epopoi, Galekit, **Kerazap**, **Narthip** | Galekit, Pebblith, Ergant, Narthip, Kerazap |  |  |
| AKTI_TOWN |  |  | Ketofry, Karkipool, Halcyling, Narkeray |  |
| TRIREME_EUPLOIA_DECK |  |  | Narkeray, Ketofry, Karkipool, **Kynoketos** |  |

### Emporion (Act I)

| Map | Land by day | Land at night | Water and rods | Rock Smash |
|---|---|---|---|---|
| AEGINA_TOWN |  |  | Ketofry, Karkipool, Narkeray, Halcyling, Kynoketos, **Galenyon** |  |
| AEGINA_APHAIA_ROAD | Ergant, **Chelonet**, **Onotis**, Epopoi, Halcyling, Karkipool, Galekit, **Lophops** | Galekit, Ergant, Onotis, Chelonet, Karkipool, Pebblith, **Obolorn** | Narkeray, Galenyon, **Karkitox**, Kynoketos |  |
| AEGINA_TEMPLE_OF_APHAIA | **Psychora**, Ergant, Lophops, Epopoi, Galekit, Chelonet, Halcyling, Kerazap | Galekit, Ergant, Pebblith, Onotis, Obolorn, Chelonet | Narkeray, Galenyon, Karkitox, Kynoketos |  |
| AEGINA_MOUNT_OROS | Kerazap, Ergant, **Harpeck**, Epopoi, Lophops, Pebblith, Chelonet | Pebblith, Galekit, Kerazap, Ergant, Harpeck, Obolorn, Narthip | Kynoketos, Narkeray, Karkitox, Galenyon |  |
| EMPORION_HARBOR |  |  | Ketofry, Karkipool, Narkeray, Halcyling, Kynoketos, Galenyon |  |
| ROUTE4_ISTHMUS | Kerazap, Epopoi, Lophops, Onotis, Galekit, Chelonet, Ergant, Elaleaf, **Spalunk**, Harpeck, **Nemecub** | Galekit, Onotis, Pebblith, Chelonet, Spalunk, Kerazap, Ergant, Harpeck, Obolorn, Nemecub |  | Pebblith, Spalunk, **Pithound**, Chelonet |
| HECATES_HOLLOW | Pebblith, Spalunk, Chelonet, Ergant, Galekit, **Gelasable** | Galekit, Pebblith, Obolorn, Spalunk, Ergant, Gelasable |  |  |
| ROUTE5_SKIRONIAN_CLIFFS | Lophops, Kerazap, Harpeck, Chelonet, Onotis, Epopoi, Galekit, Ergant, Elaleaf, Pebblith, Nemecub | Galekit, Gelasable, Pebblith, Onotis, Kerazap, Chelonet, Spalunk, Ergant | Ketofry, Karkipool, Narkeray, Halcyling, Kynoketos, Galenyon | Pebblith, Spalunk, Pithound, Chelonet |

### Eleusa (Act I)

| Map | Land by day | Land at night | Water and rods | Rock Smash |
|---|---|---|---|---|
| ELEUSA_VILLAGE | **Stachyss**, **Melibee**, **Kaplet**, **Alekrow**, Spalunk, Elaleaf, **Rhoaril** | Kaplet, Galekit, Spalunk, Gelasable, Stachyss, Elaleaf, Rhoaril |  |  |
| ELEUSA_SANCTUM_B1F | Spalunk, Rhoaril, Kaplet, Galekit, Pebblith, Ergant, Gelasable |  |  |  |
| ELEUSA_SANCTUM_B2F | Rhoaril, Spalunk, Pebblith, Kaplet, Gelasable | Rhoaril, Spalunk, Pebblith, Kaplet, Gelasable, Galekit |  |  |
| ELEUSA_SANCTUM_B3F | Rhoaril, Spalunk, Pebblith, Kaplet, Gelasable | Rhoaril, Spalunk, Pebblith, Kaplet, Gelasable, Galekit |  |  |

### Thyrsa (Act II)

| Map | Land by day | Land at night | Water and rods | Rock Smash |
|---|---|---|---|---|
| ROUTE6_ELEUTHERAI_ROAD | **Ampelix**, Lophops, Onotis, Kerazap, **Botrykit**, Melibee, Gelasable, Galekit, Harpeck, Stachyss, Nemecub, **Lykopup**, **Prosomime** | Botrykit, Gelasable, Galekit, Lykopup, Ampelix, Onotis, Spalunk, Prosomime, Nemecub |  |  |
| MT_KITHAIRON | Pebblith, Kerazap, Ampelix, Harpeck, **Cairnolith**, Botrykit, Lophops, Melibee, Gelasable, Nemecub, Galekit, Lykopup, Prosomime, **Kerdovix** | Botrykit, Lykopup, Prosomime, Gelasable, Pebblith, Cairnolith, Galekit, Ampelix, Kerdovix |  |  |
| THYRSA_CITY | Ampelix, Onotis, Lophops, Melibee, Kerazap, Elaleaf, Spalunk, **Midonos** | Botrykit, Gelasable, Onotis, Ampelix, Galekit, Kaplet |  |  |
| ROUTE7_KRONIA_GROUNDS | Ampelix, Botrykit, Lophops, Onotis, **Sporadon**, Kerazap, Melibee, Stachyss, Prosomime, Galekit, Harpeck, Lykopup, Nemecub | Botrykit, Sporadon, Lykopup, Prosomime, Ampelix, Spalunk, Nemecub |  | Pebblith, Cairnolith, Spalunk, Chelonet |

### Arkadia (Act II)

| Map | Land by day | Land at night | Water and rods | Rock Smash |
|---|---|---|---|---|
| ROUTE8_KOPAIS_ROAD | **Chalkip**, Lophops, Melibee, Chelonet, Karkitox, Onotis, Spalunk, Ampelix, Gelasable, Kerazap, Prosomime, Lykopup, Stachyss, **Amnoze** | Lykopup, Chalkip, Gelasable, Karkitox, Prosomime, Spalunk, Chelonet, Amnoze | Ketofry, **Hymnet**, Karkitox, Galenyon |  |
| KOPAIS_KATAVOTHRES | Spalunk, Pebblith, **Raknit**, Cairnolith, Chelonet, Karkipool, Karkitox, Obolorn | Raknit, Spalunk, Obolorn, Cairnolith, Pebblith, Karkipool, Chelonet, Karkitox | Ketofry, Halcyling, Galenyon, Kynoketos | Pebblith, Cairnolith, Spalunk, Chelonet |
| LEBADEIA |  |  | Ketofry, Halcyling, Galenyon, Kynoketos |  |
| ROUTE9_PARNASSOS_CROSSROADS | Ampelix, **Eripip**, Lophops, **Harpelle**, Melibee, Onotis, Gelasable, Cairnolith, Midonos, Botrykit, Lykopup, Prosomime, Kerazap, **Enigmaw** | Gelasable, Lykopup, Prosomime, Botrykit, Raknit, Spalunk, Enigmaw, Ampelix, Galekit, Cairnolith, Midonos | Ketofry, Halcyling, Galenyon, Kynoketos | Pebblith, Spalunk, Cairnolith, Chelonet |
| ROUTE9_KORYKIAN_CAVE | **Pelython**, Pebblith, Cairnolith, Raknit, Gelasable, Melibee, **Arkoby**, **Melisseer** | Pelython, Raknit, Prosomime, Pebblith, Cairnolith, Lykopup, Arkoby | Ketofry, Halcyling, Galenyon, Kynoketos |  |
| KIRRHA |  |  | Ketofry, Narkeray, Karkipool, Halcyling, Kynoketos, Galenyon |  |
| GULF_TRIREME |  |  | Ketofry, Karkipool, Narkeray, Kynoketos |  |
| AIGION |  |  | Ketofry, Narkeray, Karkipool, Halcyling, Kynoketos, Galenyon |  |
| ROUTE11_DRUM_PASS | **Kymbash**, Eripip, Arkoby, Kerazap, Gelasable, Lophops, Melibee, Cairnolith, Lykopup, Botrykit, Onotis, Harpelle, Raknit, Prosomime, Midonos | Lykopup, Gelasable, Prosomime, Raknit, Kymbash, Spalunk, Botrykit, Arkoby, Cairnolith | Ketofry, Halcyling, Galenyon, Kynoketos | Pebblith, Spalunk, Cairnolith, Chelonet |
| ROUTE12_CYPRESS_ROAD | Raknit, Eripip, Arkoby, Ampelix, Kaplet, Lykopup, Melibee, Galekit, Prosomime, **Skylaps**, Amnoze | Lykopup, Raknit, Prosomime, Amnoze, Arkoby, Kaplet, Galekit, **Lykanax** | Ketofry, Halcyling, Galenyon, Kynoketos |  |
| ARKADIA_CYPRESS_WOOD | Arkoby, Raknit, Lophops, Kaplet, Skylaps | Lykopup, Raknit, Arkoby, Amnoze, **Kaprodon**, Lykanax |  |  |
| ARKADIA |  |  | Karkipool, Ketofry, Kynoketos |  |
| ERYMANTHOS_PRESERVE_OAKWOOD | Kaplet, Arkoby, Skylaps, Melibee, Raknit, Lophops, Eripip, Kerdovix, Kaprodon | **Glaukoin**, Lykopup, Amnoze, Kaplet, Raknit, Kerdovix, Arkoby, Lykanax |  |  |
| ERYMANTHOS_PRESERVE_MEADOW | Eripip, Chelonet, **Aetling**, **Kryopuff**, Melibee, Arkoby, Kerazap, Skylaps | Amnoze, Kryopuff, Lykopup, Chelonet, Arkoby, Kerdovix, Glaukoin, Lykanax |  |  |
| ERYMANTHOS_PRESERVE_RIVER | Chalkip, Melibee, Hymnet, Kaplet, Arkoby, Halcyling, Raknit, Skylaps | Lykopup, Chalkip, Amnoze, Raknit, Kaplet, Glaukoin, Kerdovix, Lykanax | Ketofry, Hymnet, Kynoketos, Karkitox, Karkipool, Galenyon, **Lernip** |  |
| ERYMANTHOS_PRESERVE_CAVE | **Pagoshard**, Spalunk, Obolorn, Pebblith, Raknit, Cairnolith, Kryopuff | Pagoshard, Spalunk, Obolorn, Pebblith, Raknit, Cairnolith, Kryopuff | Ketofry, Karkitox, Karkipool, Kynoketos, Hymnet |  |

### Astyra (Act II)

| Map | Land by day | Land at night | Water and rods | Rock Smash |
|---|---|---|---|---|
| ROUTE13_HIGHLAND_ROAD | **Elapling**, Arkoby, **Nemeleon**, Kerazap, Harpelle, Cairnolith, Melisseer, Aetling, Glaukoin, Lykanax, Prosomime | Lykanax, Harpelle, Prosomime, Cairnolith, Kerazap, Elapling, Nemeleon | Ketofry, Halcyling, Galenyon, Kynoketos | Cairnolith, Kerazap |
| NEMEA | Nemeleon, Melisseer, Elapling, Glaukoin, **Hoplomex**, Kerazap, Lykanax, Prosomime, **Geogrip** | Nemeleon, Lykanax, Glaukoin, Prosomime | Ketofry, Halcyling, Galenyon, Kynoketos |  |
| ROUTE14_NEMEA_ROAD | Elapling, Hoplomex, Kerazap, Melisseer, Nemeleon, Glaukoin, Lykanax, Prosomime | Lykanax, Glaukoin, Prosomime, Elapling, Hoplomex, Kerazap, Nemeleon | Ketofry, Halcyling, Galenyon, Kynoketos | Cairnolith, Kerazap, Hoplomex |
| ROUTE14_TRETOS | Cairnolith, Kerazap, Prosomime, Glaukoin, Lykanax, Hoplomex, Nemeleon | Prosomime, Lykanax, Cairnolith, Glaukoin, Kerazap, Hoplomex, Nemeleon | Ketofry, Halcyling, Galenyon, Kynoketos | Cairnolith, Kerazap, Hoplomex, Geogrip |
| ROUTE15_MYSTERY_ROAD | Galenyon, **Korantha**, Melisseer, **Thyrsivy**, Hoplomex, Nemeleon, Glaukoin | Lykanax, **Persenyx**, Melisseer, Thyrsivy, Hoplomex, Nemeleon | Ketofry, Narkeray, Karkipool, Halcyling, Kynoketos, Galenyon |  |
| ROUTE16_CAPITAL_PASS | **Sophowl**, Hoplomex, Thyrsivy, Cairnolith, Nemeleon, Elapling, **Ophidrop**, Aetling | Sophowl, Lykanax, Harpelle, Cairnolith, Thyrsivy, Nemeleon, Persenyx, Hoplomex, Ophidrop |  |  |
| SALT_WELL_B1F | Galenyon, Karkitox, Narkeray, Kynoketos |  | Galenyon, Narkeray, Karkitox, Kynoketos |  |
| SALT_WELL_B2F | Galenyon, Karkitox, Narkeray, Kynoketos |  | Galenyon, Narkeray, Karkitox, Kynoketos |  |
| ASTYRA_HARBOR |  |  | Galenyon, Narkeray, Karkitox, Kynoketos |  |

### Kaldera (Act II)

| Map | Land by day | Land at night | Water and rods | Rock Smash |
|---|---|---|---|---|
| KALDERA | **Taurivet**, **Laolith**, **Kapnub**, Narthip, **Kaminoo**, **Pyrapod** | Taurivet, Laolith, Kapnub, Narthip, Kaminoo, Pyrapod | Galenyon, Narkeray, Karkitox, Kynoketos |  |
| KALDERA_TELCHINES_FORGE | Taurivet, Laolith, Pyrapod, **Plouteras** | Taurivet, Laolith, Pyrapod, Plouteras | **Telpup**, Ketofry, **Telkanvil**, Karkitox |  |

### Kythera (Act III)

| Map | Land by day | Land at night | Water and rods | Rock Smash |
|---|---|---|---|---|
| KYTHERA_SKANDEIA |  |  | **Aphrell**, Narkeray, Galenyon, Ketofry, Kynoketos, Telkanvil |  |
| KYTHERA_FOAM_ROAD | Galenyon, **Himerow**, Aphrell, Psychora, **Glyphlet**, **Narcibulb**, **Chelyra**, Harpelle | **Echolali**, Glyphlet, Aphrell, Chelyra, Harpelle, Galenyon | Aphrell, Narkeray, Galenyon, Kynoketos, Telkanvil |  |
| KYTHERA_SPRING_OF_KALLIRHOE | Narcibulb, Psychora, Glyphlet, Aphrell, Himerow, Galenyon, **Narcisheen**, Echolali | Glyphlet, Echolali, Chelyra, Narcibulb, Harpelle, Narcisheen |  |  |
| KYTHERA_ECHO_CAVES | Cairnolith, Aphrell, Echolali, Galenyon, Glyphlet, Harpelle, Narcisheen |  | Aphrell, Narkeray, Galenyon, Kynoketos, Echolali, Telkanvil |  |
| KYTHERA_PAPHIA |  |  | Aphrell, Narkeray, Galenyon, Kynoketos, Telkanvil |  |
| KYTHERA_NERAIDA_FALLS | Himerow, Glyphlet, Narcibulb, Melisseer, Chelyra, Galenyon, Psychora, Harpelle | Narcibulb, Glyphlet, Harpelle, Chelyra, Echolali, Galenyon, Psychora | Ketofry, Galenyon, Aphrell, Kynoketos, Narcisheen |  |

### Knossa (Act III)

| Map | Land by day | Land at night | Water and rods | Rock Smash |
|---|---|---|---|---|
| KNOSSA_AMNISOS |  |  | Karkitox, Ketofry, Narkeray, Galenyon, Telkanvil, Kynoketos |  |
| KNOSSA_BULL_ROAD | Taurivet, Melibee, Onotis, **Kolossette**, Cairnolith, Melisseer, **Kolossard**, **Ikaroth** | Gelasable, Sophowl, Onotis, **Kalyptor**, Taurivet, Cairnolith, Amnoze, Midonos |  |  |
| KNOSSA_BULL_ROAD_VINEYARD | Thyrsivy, Onotis, Melisseer, Melibee, Gelasable, Midonos, Korantha, **Oinopard** | Oinopard, Gelasable, Thyrsivy, Sophowl, Onotis, Midonos, Kalyptor, Persenyx, Amnoze |  |  |
| KNOSSA_BRONZE_HEEL | Galenyon, Kolossette, Taurivet, Karkitox, Cairnolith, Onotis, Ikaroth, Kolossard, Telkanvil | Kolossette, Karkitox, Gelasable, Cairnolith, Kalyptor, Sophowl, Telkanvil | Ketofry, Karkitox, Narkeray, Galenyon, Telkanvil, Kynoketos |  |
| LABYRINTH_RING1 | **Mitoclew**, Cairnolith, Kalyptor, Kolossette, Plouteras, Kolossard, **Kourodin** |  |  | Cairnolith, Mitoclew, Kolossette, Geogrip |
| LABYRINTH_RING2 | Mitoclew, Kalyptor, Cairnolith, **Hyphantis**, Kolossette, Plouteras, Taurivet, Kolossard | Kalyptor, Mitoclew, Hyphantis, Cairnolith, Kolossette, Plouteras, Amnoze, Taurivet | Plouteras, Kalyptor, Mitoclew, Persenyx, Kolossette | Cairnolith, Mitoclew, Kolossette, Geogrip |
| LABYRINTH_RING3 | Hyphantis, Kalyptor, Persenyx, Mitoclew, Plouteras, Kolossette, Kolossard |  | Plouteras, Kalyptor, Mitoclew, Persenyx, Kolossette | Cairnolith, Mitoclew, Kolossette, Geogrip |
| LABYRINTH_RING4 | Cairnolith, Plouteras, Kolossette, Mitoclew, Kaprodon, Geogrip |  | Plouteras, Kalyptor, Mitoclew, Persenyx, Kolossette | Cairnolith, Mitoclew, Kolossette, Geogrip |
| LABYRINTH_RING5 | Kalyptor, Mitoclew, Lykanax, Hyphantis, Plouteras, Cairnolith, Kaprodon, Persenyx |  | Plouteras, Kalyptor, Mitoclew, Persenyx, Kolossette | Cairnolith, Mitoclew, Kolossette, Geogrip |
| LABYRINTH_RING6 | Kolossette, Taurivet, **Gigantomb**, Cairnolith, Kourodin, Kolossard |  | Plouteras, Kalyptor, Mitoclew, Persenyx, Kolossette | Cairnolith, Mitoclew, Kolossette, Geogrip |
| LABYRINTH_RING7 | Sophowl, Mitoclew, Psychora, Chelyra, Melisseer, **Kerastorm**, Amnoze | Sophowl, Mitoclew, Psychora, Amnoze, Chelyra, Kerastorm |  | Cairnolith, Mitoclew, Kolossette, Geogrip |
| LABYRINTH_CELLARS | Kalyptor, Mitoclew, Persenyx, Lykanax, Kolossard |  |  |  |
| LABYRINTH_MINOS_TOMB | Kalyptor, Mitoclew, Persenyx, Lykanax, Kolossard |  |  |  |

### Lakonia (Act III)

| Map | Land by day | Land at night | Water and rods | Rock Smash |
|---|---|---|---|---|
| GYTHEION |  |  | Narkeray, Ketofry, Galenyon, Karkipool, Kynoketos, Karkitox, Telkanvil |  |
| ROUTE25_EUROTAS | Hoplomex, **Belornis**, **Stachypter**, **Hymnaria**, **Dorydrake**, Galenyon, Onotis, Kaplet, Elapling, Nemeleon | Belornis, Dorydrake, Karkitox, Hymnaria, Kaplet, Kalyptor, Stachypter, Nemeleon | Ketofry, Karkitox, Hymnaria, Kynoketos, Karkipool | Cairnolith, Laolith, Geogrip |
| LAKONIA | Dorydrake, Hoplomex, Nemeleon, Belornis, **Hoplektor**, Cairnolith | Nemeleon, Dorydrake, Cairnolith, Hoplomex, Belornis | Ketofry, Karkitox, Kynoketos, Karkipool, Galenyon | Cairnolith, Laolith, Geogrip |
| ROUTE26_SKIRITIS | Hoplomex, Laolith, Nemeleon, Stachypter, Dorydrake, Chelonet, Hoplektor, Harpelle | Stachypter, Laolith, Dorydrake, Nemeleon, Hoplomex, Chelonet, Kalyptor | Karkitox, Ketofry, Karkipool, Galenyon, Halcyling, Chelonet, Kynoketos, Kalyptor | Cairnolith, Chelonet, Plouteras, Laolith |
| LAKE_STYMPHALIA | Hymnaria, Belornis, Galenyon, Chelonet, Karkitox, Chalkip, Harpelle | Karkitox, Hymnaria, Kalyptor, Chelonet, Sophowl, Belornis | Karkitox, Ketofry, Karkipool, Galenyon, Halcyling, Chelonet, Kynoketos, Kalyptor |  |
| ROUTE27_ARKADIAN_HILLS | Chelyra, Laolith, Hyphantis, **Starkos**, Lykanax, Chelonet, Nemeleon, Harpelle, Enigmaw, Kaprodon | Starkos, Lykanax, Laolith, Kaprodon, Hyphantis, Chelyra, Chelonet, Nemeleon | Karkitox, Ketofry, Karkipool, Galenyon, Halcyling, Chelonet, Kynoketos, Kalyptor |  |
| ROUTE27_SKIRITAI_CAVE | Laolith, Plouteras, Hyphantis, Kalyptor, Chelonet, Enigmaw, Sophowl | Kalyptor, Plouteras, Sophowl, Hyphantis, Laolith, Enigmaw, Chelonet | Karkitox, Ketofry, Karkipool, Galenyon, Halcyling, Kynoketos, Chelonet, Kalyptor | Cairnolith, Chelonet, Plouteras, Laolith |

### Delphoi (Act III)

| Map | Land by day | Land at night | Water and rods | Rock Smash |
|---|---|---|---|---|
| ROUTE28_SACRED_OLIVES | Melibee, Elapling, **Basilops**, Lykanax, **Hierolive**, Melisseer, **Elektear**, Sophowl, Harpelle, Enigmaw | Lykanax, Sophowl, Hierolive, Elapling, Elektear |  |  |
| ROUTE28_KASTALIAN_GORGE | Cairnolith, Melibee, **Pythoros**, Hymnaria, Melisseer, Basilops, Elektear, Gelasable, Harpelle, Sophowl, Enigmaw, Taurivet, Lykanax | Gelasable, Cairnolith, Sophowl, Elektear, Lykanax, Hymnaria, Pythoros | Ketofry, Karkitox, Hymnaria, Galenyon, Kynoketos, Karkipool, Elektear | Cairnolith, Enigmaw, Pythoros, Telkanvil |
| DELPHOI | Melibee, Melisseer, Hymnaria, Elektear, Cairnolith, Basilops, Harpelle, Sophowl, Gelasable, **Mantipod**, Enigmaw, Pythoros, Chelyra | Mantipod, Sophowl, Gelasable, Elektear, Cairnolith, Pyrapod | Ketofry, Karkitox, Hymnaria, Galenyon, Kynoketos, Karkipool, Elektear |  |

### League (Act III)

| Map | Land by day | Land at night | Water and rods | Rock Smash |
|---|---|---|---|---|
| ASCENT_1F | Lykanax, Nemeleon, Laolith, Basilops, Hoplektor, Kerastorm, **Lebetron** | Lykanax, Harpelle, Starkos, Kaprodon, Laolith, Nemeleon, Lebetron | Kynoketos, Galenyon, **Dakrock** |  |
| ASCENT_2F | **Borapteryx**, **Chionyad**, Laolith, Kolossard, Geogrip, Hoplektor, Kryopuff, **Niflake** | Borapteryx, Chionyad, Harpelle, Kolossard, Geogrip, Starkos, Niflake, Kryopuff | Kynoketos, Galenyon, Dakrock | Laolith, Kolossard, Geogrip |
| ASCENT_ICEFALL | Borapteryx, Chionyad, Kolossard, Laolith, **Krystolos**, Geogrip, Niflake, Kryopuff | Krystolos, Chionyad, Borapteryx, Kolossard, Harpelle, Niflake, Kryopuff | Kynoketos, Galenyon, Dakrock | Krystolos, Pagoshard, Laolith, Geogrip |
| ASCENT_ICEFALL_DEEP | **Stygiad**, Krystolos, Chionyad, Kolossard, Persenyx, Niflake, Kryopuff | Stygiad, Krystolos, Persenyx, Chionyad, Harpelle, Niflake, Kryopuff | Kynoketos, Galenyon, Stygiad, Dakrock |  |
| ASCENT_CRYSTAL_VAULT | Krystolos, Chionyad, Pagoshard, Stygiad, Niflake, Kryopuff | Krystolos, Stygiad, Pagoshard, Chionyad, Niflake, Kryopuff |  |  |
| ASCENT_GLACIER | Chionyad, Borapteryx, Pagoshard, Krystolos, Kerastorm, Kolossard, Kryopuff, Niflake | Krystolos, Borapteryx, Pagoshard, Chionyad, Harpelle, Kolossard, Niflake, Kryopuff | Kynoketos, Galenyon, Dakrock |  |
| ASCENT_3F | Borapteryx, Krystolos, Chionyad, Kerastorm, Hoplektor, **Aetarch** | Krystolos, Chionyad, Borapteryx, Harpelle, Starkos |  |  |

### Post (Act Post)

| Map | Land by day | Land at night | Water and rods | Rock Smash |
|---|---|---|---|---|
| ERYMANTHOS_PRESERVE_THICKET | Kaprodon, Kaplet, Borapteryx, Lykanax, Krystolos, Chionyad, Starkos, Skylaps, Kerdovix | Kaprodon, Kaplet, Borapteryx, Lykanax, Krystolos, Chionyad, Starkos, Skylaps, Kerdovix |  |  |

