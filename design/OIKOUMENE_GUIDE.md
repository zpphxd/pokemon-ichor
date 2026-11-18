# The Oikoumene: the builder's guide

- **Owner:** World design. **Status:** a build-ready guide, written 2026-11-17. It changes no game file. Where it changes an approved decision it says so, marked **PROPOSAL**, and §8 collects them for the user.
- **What this is:** the second region, the ten lands beyond Aethos, and the post-game epics, designed to the standards the user set on 2026-11-17. A map builder can open any land's section and build it.
- **What it sits on.** `design/OIKOUMENE.md` stays the record of the region's approved shape (its §13 decisions), its chart, its engine plan and its people. `design/oikoumene/PERIODOS.md` owns the ten halls. `design/oikoumene/COVERAGE.md` owns where every species lives. `LEGENDS.md` owns every legendary quest. `LABORS.md`, `UNDERWORLD.md`, `ODYSSEY.md` and `POSTGAME.md` own the epics. This guide raises all of it to one bar and turns it into maps.
- **Where this guide and OIKOUMENE.md differ,** this guide is the newer plan for *how the lands are built* (routes, stops, puzzles, gates, art, order). OIKOUMENE.md still wins on *what is approved* until the user takes §8's proposals.

---

## Contents

1. The vision, and the bar every land must pass
2. The world: getting there, the connection diagram, the level curve, the unlock order, and where every other generation lives (§2.7)
3. The ten lands
   - 3.1 Thrace and the Troad
   - 3.2 Lydia and Phrygia
   - 3.3 The Black Sea
   - 3.4 Scythia and Hyperborea
   - 3.5 Egypt and the Nile
   - 3.6 Aithiopia and the Sunrise
   - 3.7 Libya
   - 3.8 The Far West
   - 3.9 The Western Sea
   - 3.10 The Ring of Okeanos
4. The epics at the same bar
5. Shared kit: the plate puzzle, herms, outcamps, the remains of the lost, map names
6. Art and ROM
7. Build order
8. Proposals that change approved decisions
9. Every type a home: the biome matrix
10. Etna: the Fire crown
11. The post-game League: the circuit, the Four of Oeta and Herakles
12. The Twelve Labors, one by one
13. The full Odyssey
14. The additions in the build order and the budget (and proposals P-12 to P-19)
15. The legendary register: all 136 legends, a third in Aethos and two thirds in the Oikoumene, with their quests (and P-20)

---

## 1. The vision, and the bar every land must pass

**The vision.** The user's words for the whole game: *"this game should feel grand and amazing, like a new world of Pokémon that has never been explored."* The main story is Greece, which the player comes to know road by road. The Oikoumene is the rest of the world as the Greeks imagined it, and the player arrives knowing nothing. Every land should feel like stepping off a boat into a country nobody at home has seen: its own light, its own stone, its own gods at the roadside, its own animals in the grass, and people with their own idea of what the world is. Herodotus walked this world asking questions and wrote down what he saw next to what he was told. The player does the same, for Alethea's chart. The routes are long and they climb; caves open under them; the old stories lie on the ground as wrecks, graves and abandoned camps; and once in each land the screen stops and simply shows you something enormous.

### The bar: a checklist every land passes before it ships

A land isn't done until its builder can tick every line, with the map and tile coordinates that prove it, in the land's `design/maps/<Land>.md`.

**Places**
- [ ] **No bare stops.** Every town, village, camp and landing has a temple, shrine or outcamp that can carry a quest, in the land's own idiom (an ibis shrine in Egypt, a felt tent-shrine on the steppe).
- [ ] **Every house is enterable,** with a unique interior, someone inside, and a gift, trade or quest (MAP_DESIGN §2). No barred doors.
- [ ] **An entrance herm in every town and village,** big and easy to spot, with a sign that names it a travel stop (§5.2). Each land has its own herm form.
- [ ] **Healing within one screen of every town entrance,** and at every outcamp.

**Roads**
- [ ] **Long, engaging routes:** each land's great road is 5–7 screens (75–105 tiles along its main line), with at least three kinds of terrain, one cave or covered stretch, one climb (a stair, a cliff road or a Crook face), and a **midpoint rest** (an outcamp, §5.3).
- [ ] **Forced grass:** two or three bands across each great road's main line (MAP_DESIGN §1), the later ones right after a trainer.
- [ ] **Trainers on chokepoints you can't walk around:** at least four mandatory trainers on each great road, with sight lines covering a narrow point's full width. The first trainer is easy and in plain view.
- [ ] **Ledges drop toward the land's port,** so the way back is fast.

**Gates and puzzles**
- [ ] **Heavy relic use:** at least six relic gates per land, at least four the player can open on arrival and at least two **for later** (a relic or key from another epic or land, §2.6). Every closed gate shows what's behind it.
- [ ] **A boulder-on-switch puzzle:** at least one drum-on-plate puzzle per land, and two or more in its main dungeon (§5.1), taught, tested and combined.
- [ ] **Stairs and ladders to treasure:** at least two per land: a tower stair, a well ladder, a cliff stair or a shaft, each ending at something worth the climb.

**Story in the land**
- [ ] **Environmental storytelling:** at least three "remains of the lost" per land (§5.4): a wreck, a grave, an abandoned camp, a last message. Each has a readable object and most pay something.
- [ ] **A main thread, at least three side quests,** and lore that points at the next place.

**Pokémon**
- [ ] **Signature Pokémon:** three to five species the player first meets here, placed where they make sense, named in the land's NPC talk.
- [ ] **Rarer, stronger Pokémon behind gates:** every "for later" gate and most "now" gates open onto a table or a static above the land's band (up to +4, WORLD_EXPLORATION §4).
- [ ] **Every COVERAGE area of the land is on a built map.**

**Wonder**
- [ ] **Awe moments:** at least two per land. One is a **vista** (the camera stops on something enormous, §5.5); one is a **set piece** (something happens: a river rises, a statue sings, the sun comes up out of the sea).
- [ ] **A first view:** the first screen after landing shows the land's signature landmark, or points at it.

**Craft**
- [ ] MAP_DESIGN §7's "great" checklist, three render-and-critique passes, and `tools/ichor/map_audit.py` clean.
- [ ] `make` green, `tools/ichor/smoke_test.sh` passing, and the ROM line noted in the land's doc.

---

## 2. The world

### 2.1 Getting there

The approved shape stands (OIKOUMENE §2, PG-6 to PG-8): no single key opens the Oikoumene. The ship opens the near lands, the epics carry you to their own places, and Aeolus's Bag opens the rim.

| Way in | When | First landing | Notes |
|---|---|---|---|
| **The *Euploia*, east** past Samothrake (Aethos Route 20) | From the post-game's start | **Sestos**, the Troad | Labor 8 sails the same way to Thrace |
| **The *Euploia*, east** through the Bosporus | From the start | **Salmydessos**, then Aia; Themiskyra by Labor 9 | |
| **The *Euploia*, south** past Knossa (Route 34) | From the start | **Naukratis**, Egypt | The Oikoumene's hub |
| **The *Euploia*, south-west** from Kaldera, the colonists' road | From the start | **Apollonia**, Kyrene's harbor | **PROPOSAL P-2**: Libya's coast by sea. Thera (Kaldera) founded Kyrene (Herodotus 4.150–158) |
| **West round Cape Maleia** | When you start the Odyssey | The wine-dark sea | One way until home (ODYSSEY) |
| **Helios's cup** | Labor 10 | The Strait of the Pillars, Erytheia | Then the Garden and Atlas's Ridge (Labor 11) |
| **Aeolus's Bag** | After the Odyssey | The fog banks round Okeanos | Cimmerian fog, ocean fog past the Pillars, Aithiopia's dawn fog |
| **Helios's cup, by night** | After Labor 10 | Every Okeanos shore | The only way to the Isles of the Blessed (PG-17) |

**Arriving is a scene, every time.** The first landing in each land plays a short arrival: the ship comes in, the camera pans over the first view (§1, "a first view"), Alethea says one line about what the old maps claimed was here, and the port's fisher hands over the Super Rod or a Big Pearl (OIKOUMENE §2).

```text
ALETHEA: Hecataeus drew a man with his face in his chest here.

ALETHEA: …That's a fisherman with a basket. Write it down.
```

### 2.2 The connection diagram

Lands meet only at harbors, passes and sea lanes, never at a walking seam (OIKOUMENE §4), so each land keeps its own secondary tileset. Double lines are sea lanes; single lines walk; `[gate]` is what opens the link.

```text
                                   THE RING OF OKEANOS (wild 75-80)
           Cimmerian Shore . Land of Dreams . Gates of the Sun . Selvage . Isles of the Blessed
               ^ [Bag]                 ^ [Bag]                       ^ [Bag]          ^ [cup, night]
               |                       |                             |                |
   SCYTHIA <-[flame]-> HYPERBOREA      |                             |                |
   (70-80)   Rhipaean Pass             |                             |                |
      ^                                |                             |                |
      || [Conch] Leuke=>Olbia          |                             |                |
      ||                               |                             |                |
   THE BLACK SEA (64-72) <=Bosporus=> THE TROAD (60-66) -- Royal Road -- LYDIA (63-70)
   Salmydessos, Aia, Leuke,            Sestos, Ilion,                    Sardis, Gordion,
   Chalybia; Themiskyra*,              Chryse; Thrace*                   Miletos, Hypaipa
   the Caucasus*                           ^
                                           || the Euploia, east
                                           ||
   THE FAR WEST (70-78) <==cup==>    ===== AETHOS ===== the Euploia, south ====> EGYPT (60-67)
   Gadeira, Tartessos,      (Labor 10)   (Olympia: Olympiad,     ||             Naukratis, Memphis,
   the Atarantes; Pillars*,              Labors; Tainaron:       ||             Heliopolis, Thebes,
   Erytheia*, Garden*, Ridge*            Katabasis; Atlantis     || Kaldera     Elephantine
      ^                                  past the Pillars;       ||  => Kyrene      |        |
      || after the Odyssey               Olympus: Primordials,   ||  [P-2]     [ravens]  [Horn: cataracts]
      ||                                 the Prime Mover)        vv             |        v
   THE WESTERN SEA (70-82) <==Maleia, one way==               LIBYA (63-70) <---+   AITHIOPIA (70-76)
   ODYSSEY's islands; Kroton,                                  Apollonia, Kyrene,     Meroe, the Gate
   Cumae, Elea, Ogygia                                         Ammonion, Tritonis     of Dawn --[Bag]--> Okeanos

   * = an epic's map on this chart (LABORS, ODYSSEY). Levels are wild bands.
```

### 2.3 The level curve

`BALANCE.md`'s Oikoumene row (wild 60–80, trainers 70–85, the strongest to 90–100) and OIKOUMENE §9 stand. This guide adds the shape inside each land: **every land climbs as you go deeper**, so its port is the gentlest place and its far end, its dungeon and its "for later" gates are the hardest. No map's band is wider than 5.

| Land | Port and first road (wild) | Deep road, dungeon (wild) | Behind "for later" gates | Route trainers | Hall trainers | Champion | Other bosses |
|---|---|---|---|---|---|---|---|
| Troad | 60–63 | 63–66 | 66–70 | 70–74 | 73–74 | Hektor 74–76 | Gargaros's Zapdos (LEGENDS) |
| Egypt | 60–63 | 63–67 | 67–70 | 70–74 | 73–74 | Proteus 74–76; Helen 74–76 | The flooded pyramid's keeper 75 |
| Lydia | 63–66 | 66–70 | 70–73 | 72–76 | 75–76 | Croesus 75–77 | Tantalus's shade 76 |
| Libya | 63–66 | 66–70 | 70–73 | 72–76 | 75–76 | Kyrene 75–77 | The Psylli's chief 76 |
| Black Sea | 64–68 | 68–72 | 72–75 | 74–78 | 77–78 | Medea 76–78 | Aietes's bulls 76; the serpent 77 |
| Aithiopia | 70–73 | 73–76 | 76–79 | 76–80 | 79–80 | Memnon 78–80 | The Ketos 79 |
| Far West | 70–74 | 74–78 | 78–80 | 78–82 | 81–82 | Arganthonios 80–82 | Atlas's sky-stone keeper 80 |
| Scythia, Hyperborea | 70–74 | 75–80 | 78–80 | 76–82 | 81–82 | Abaris 80–82 | Boreas's hall 81 |
| Western Sea (towns) | 74–76 | 75–77 | 77–80 | 76–80 | 81–82 | Milo 80–82 | The buried giant 80 |
| Okeanos | 75–78 | 77–80 | 80 | 80–85 | 83–84 | Rhadamanthys 82–84 | The Selvage's keeper 84 |
| Etna (§10) | 76–78 | 78–80 | 80 | 77–79 | — | — | Volcanion 80 |
| Mount Oeta (§11) | 82–85 | — | — | 85–88 | — | The Four 88–91; **Herakles 93–96, rematch 100** (P-13) | Primordials 88, Arceus 95 (POSTGAME) |

**Spartan** caps at each land's champion ace; **Mortal** bosses are −3 (BALANCE.md).

### 2.4 The unlock order

POSTGAME §2's route stays the spine. The lands slot round it so the player always has an open land at the right level. Nothing here is a new hard gate.

| Step | Epics | Lands open and in level | What gates the next step |
|---|---|---|---|
| 1 | The epilogue; Olympia; Labors pairs 1–3 (70–73) | **Troad and Egypt** (60–67) by ship. Both first ports teach the Oikoumene: Alethea's blank chart, the herm network, the first Emblem | Nothing: open play |
| 2 | **The Katabasis** (72–80): gives the Helm of Hades | **Lydia** overland from Ilion; **Libya** by sea (P-2) | — |
| 3 | Labors pairs 4–5 (73–77): Thrace, Themiskyra, Erytheia; Helios's cup | **The Black Sea** (64–72) | Labor 10's Pillars and the ship open Atlantis |
| 4 | **Atlantis** (76–80): gives the Nereid Pearl. Labors pair 6 and the **Kotinos** | **Aithiopia** (Horn, the cataracts) and **the Far West** (the cup) | — |
| 5 | **The Odyssey** (74–81): gives Aeolus's Bag and the Mirror of Truth | **The Western Sea's towns**; **Scythia and Hyperborea** (Conch, then a carried flame) | The Bag opens the rim |
| 6 | | **Okeanos and the Isles of the Blessed** (75–80) | Ten Emblems and the Kotinos |
| 7 | **Herakles at the Pillars** (no battle: he finishes the chart and sends you to Oeta, §11.3) | Every "for later" gate is now open; Etna's pyre-brand | The Primordials (88) and **the Prime Mover** (95), as wanted |
| 8 | **Mount Oeta:** the Four of Oeta (88–91), then **Herakles** (93–96), the last battle | — | The end; his rematch on Olympus at 100 |

### 2.5 Moving around

- **The *Euploia*** sails every lane both ways (ODYSSEY §2), except the Odyssey's voyage until you're home.
- **Herms.** Every town's entrance herm registers on first touch or first heal (the queued herm change in IDEAS.md). Touching any herm lists the registered herms **on that chart**, plus one cross-chart entry: AETHOS on the Oikoumene's herms and THE OIKOUMENE on Aethos's. This is OIKOUMENE §2's crossing target, reached from a herm as well as from the Wings. **Daedalus's Wings** fly to the same list from anywhere.
- **Helios's cup** runs the rim at night after Labor 10 (PG-17).
- **Lanes inside a land** (the Nile, the Hellespont, the Pontic coast) are sea maps you surf or sail.

### 2.6 "Now" gates and "for later" gates

When the player first lands anywhere in the Oikoumene, every main-game relic is in hand: the Hammer, Torch, Sickle, Girdle, Pan's Crook (WORLD_EXPLORATION Q1; if it isn't approved, its faces become Wings eyries), the Conch, Wings, Horn, Thread, Labrys and Helm. So "now" gates use those, and the Favor upgrades for players who have them.

"For later" gates use what the player earns **in the post-game, after a land usually opens**. One vocabulary, from WORLD_EXPLORATION §3, extended:

| Later key | From | Its obstacle | Typical prize |
|---|---|---|---|
| **Helm of Hades** | The Katabasis | A shadow door, open only at night, now by day | Tombs, the dead's back roads |
| **Nereid Pearl** | Atlantis | Deep water with columns or a wreck showing through | Drowned harbors, sunken temples |
| **Aeolus's Bag** | The Odyssey | A fog bank | The rim; islets in the fog |
| **The Mirror of Truth** | The Odyssey (Alethea makes it) | A mural or statue that shows its true face only in the mirror, and an illusion wall | Hidden doors; the Gorgons' Isle |
| **Prometheus's Ember** | Labor 11 | A cold altar or furnace no ordinary flame lights | Forges, beacons, frozen doors |
| **Abaris's Arrow** (PROPOSAL P-3) | The North's round temple, after Abaris's Emblem | An **arrow-stone**: a stone with a bow cut in it, facing a matching stone across a chasm | High ledges and islands in every land |
| **A land's own key** | That land's main thread | Named in each land's section | Mostly inside the land; a few reach other lands |

**Abaris's Arrow** (P-3). Abaris "carried the arrow round the whole earth" (Herodotus 4.36), and later writers had him ride it. After his hall, he gives you the arrow. Face an arrow-stone and press A: you fly in a straight line to its partner stone, over anything. It reuses the hall's arrow flight (OIKOUMENE §13, "The golden arrow": one `applymovement` that ignores collision), so its engine cost is a field prompt and a stone object. Because the North opens late, arrow-stones are the Oikoumene's main "for later" gate: every land has one or two, visible from the road, from the first visit.

### 2.7 Every generation: where the other thousand live

**The direction (user, 2026-11-17):** *"obviously all the other gens come in post-game."* All nine generations are already compiled into the ROM through the expansion, and PITCH's 1.0 acceptance lists all-species obtainability. This section is the plan for where they live, how each land themes them, how rare they are, and how they keep from turning the Oikoumene into a rerun of old regions.

**The source.** `design/oikoumene/COVERAGE.md`, generated by `coverage.py`, already gives all 1,025 National Dex species one home each (OIKOUMENE §8). The counts below are tallied from its species table. This guide doesn't move any home; it sets the rules for how the homes appear on the maps above, and adds each land's Aethos homeland lines on top.

#### Where every species comes from

| Source | Species | Notes |
|---|---:|---|
| The ten lands' encounter areas (wild, Augur's Eye, fishing, rock smash, surf) | 406 | Each in its land's areas, at the land's bands (§2.3) |
| The Nurseries (one per land but Okeanos) and breeding | 247 | First stages at Lv 10–20, turning by the Aethos month (PG-16); Naukratis's egg-ovens breed everything |
| Evolving a caught Pokémon | 178 | The Xenion handles trade evolutions (PG-14); stones are sold at Gadeira and found behind gates |
| Legendary, mythical, Ultra Beast, Paradox | 125 | `LEGENDS.md`, hosted by the lands and the epics |
| Theoxenia guest-gift lines (SYSTEMS §10) | 54 | 18 starter lines from Gens 1–5 and 8, given in Aethos (below) |
| Fossils, revived by Daphne at Naukratis | 15 | Dug in each land with Alethea's Trowel; the Galar halves on the Arimaspian heights |
| **All National Dex species** | **1,025** | Plus the 152 Aethos species, all obtainable in the main game and the post-game |

#### Per land: how many, and which families

"Homes" counts every species whose COVERAGE home is the land, by any method (wild, Nursery, evolution, trade, fossil). The **target** is the land's share of all-species obtainability: a land isn't done until every species homed in it can be obtained in a 1.0 save.

| Land | Homes (target) | Gen 1 / 2 / 3 / 4 / 5 / 6 / 7 / 8 / 9 | The families, themed to the land |
|---|---:|---|---|
| **Egypt** | 109 | 16 / 11 / 9 / 11 / 23 / 5 / 9 / 9 / 16 | **Tombs and sun:** Sigilyph, Cofagrigus and Runerigus, Unown, Claydol, Marowak, Greavard (the jackal-dogs of the necropolis), Rellor and Rabsca (the scarab rolling the sun). **The Nile:** Krookodile and Skeledirge (Moeris's sacred crocodiles), Hippowdon, Whiscash, Seismitoad, Eelektrik, Stunfisk. **The cats of Bubastis:** Persian, Purugly, Liepard, Meowstic, Perrserker. **Pharos:** Dewgong, Primarina, Pyukumuku, Wugtrio, Ditto. **Elephantine:** Donphan, Copperajah |
| **Troad** | 100 | 14 / 6 / 20 / 13 / 12 / 8 / 5 / 10 / 12 | **Hoplites and horses:** Falinks, Rapidash, Mudsdale, Gurdurr, Medicham, Bisharp and Kingambit, Doublade, Sirfetch'd. **Ida's birds:** Braviary, Staraptor, Swellow, Noctowl. **Apollo Smintheus's mice:** Pikachu, Plusle and Minun, Pachirisu, Dedenne, Togedemaru, Morpeko, Tandemaus, Pawmot. **The plain:** Sawsbuck, Gogoat, Dubwool, Lokix |
| **Black Sea** | 92 | 17 / 11 / 10 / 7 / 20 / 10 / 7 / 3 / 7 | **The dragons of Colchis:** Haxorus, Druddigon, Hydreigon, Drampa, Kommo-o, Dragonite, Salamence, Tyranitar. **The Fleece and the forges:** Ampharos, Rotom, Magnezone, Klinklang, Aggron, Torkoal, Coalossal, Tinkaton, Revavroom. **The coast:** Clawitzer, Mantine, Gastrodon, Wishiwashi, Kilowattrel, Noivern, Vivillon. **The Phasis:** Unfezant, Ledian, Yanma, Ninjask |
| **Libya** | 89 | 14 / 6 / 16 / 7 / 16 / 6 / 0 / 6 / 18 | **The Sand Sea:** Flygon, Garchomp, Sandaconda, Sandslash, Gligar, Cacturne, Maractus, Drapion, Mandibuzz, Orthworm. **Salt and glass:** Garganacl, Klawf, Glimmora, Darmanitan. **Antaeus's Ring:** Hariyama, Throh, Sawk, the Hitmons, Scrafty, Hawlucha. **Kyrene and the oases:** Arboliva, Eldegoss, Exeggutor, Dodrio, Delphox (Fennekin's line among the fennec foxes, PG-5), Espathra, Helioptile |
| **Far West** | 85 | 10 / 6 / 12 / 9 / 19 / 5 / 11 / 10 / 3 | **Silver and iron:** Excadrill, Ferrothorn, Duraludon, Boldore, Crustle, Golurk. **Atlas's peaks:** Skarmory, Corviknight, Lycanroc (Orthos's kind). **The Strait and the Atlantic:** Crawdaunt, Barbaracle, Panpour. **The Garden (LABORS):** Applin, Breloom, Cherrim, Lurantis, Steenee, Decidueye (Rowlet's line, wild only). **Erytheia:** Heracross, Bouffalant |
| **Aithiopia** | 84 | 16 / 10 / 6 / 5 / 10 / 12 / 11 / 3 / 11 | **The savannah of the Table of the Sun:** Zebstrika, Girafarig, Kangaskhan, Rhydon, Pyroar. **The long-lived:** Chansey and Blissey, Audino, Granbull. **The Mountains of the Moon:** Tropius, Toucannon, Passimian and Oranguru, Slaking, Galvantula, Vikavolt, Shiinotic, Sliggoo. **The cranes and the Pygmies:** Flamigo, Bombirdier. **Dawn:** Volcarona, Talonflame, Solrock, Xatu, Electabuzz |
| **Western Sea** | 83 | 16 / 9 / 21 / 5 / 1 / 3 / 7 / 17 / 4 | **The volcanoes:** Magmar, Magcargo, Salazzle, Centiskorch, Turtonator. **Avernus's ghosts:** Spiritomb, Banette, Sinistea, Dusclops. **The wine-dark sea (ODYSSEY):** Sharpedo, Golisopod, Barraskewda, Palafin, Araquanid, Qwilfish. **The islands:** Altaria (the Sirens'), Tauros and Miltank (the Sun's cattle), Toxicroak and Oinkologne (Circe's), Feebas and Azumarill (Ogygia) |
| **North** | 78 | 1 / 10 / 9 / 10 / 20 / 7 / 2 / 10 / 9 | **The steppe:** Cyclizar, Stantler and Wyrdeer, Stoutland, Diggersby, Dunsparce, Absol. **The feathers (snow):** Beartic, Abomasnow, Piloswine, Delibird, Cetitan's line, Sneasel and Sneasler. **The Cave of Boreas:** Avalugg, Glalie, Vanilluxe, Cryogonal, Baxcalibur. **Hyperborea's meadow:** Stonjourner, Swanna, Frosmoth, Jumpluff, Chimecho, Eiscue. **The gold-guardians:** the four Galar fossils |
| **Okeanos** | 67 | 16 / 8 / 7 / 9 / 5 / 9 / 6 / 3 / 4 | **The river-ocean:** Lapras, Wailord, Dondozo, Tatsugiri, Gyarados, Lanturn, Relicanth, Veluza. **The Cimmerian mist:** Haunter, Misdreavus, Drifblim, Jellicent, Zoroark, Dragapult. **Sleep:** Snorlax, Hypno, Komala. **The Isles of the Blessed:** Floette, Comfey, Spritzee, Ribombee, Bellossom, Gardevoir, Sylveon. **The Selvage:** Minior, Beheeyem, Metagross, Porygon2 |
| **Lydia** | 59 | 17 / 8 / 6 / 8 / 8 / 1 / 3 / 4 / 4 | **Gold and bronze:** Gimmighoul and Gholdengo, Klefki, Mawile, Bronzong, Seaking. **Tmolus and the vines:** Beedrill, Venomoth, Spinda, Oricorio. **The weavers:** Spidops, Ariados. **The moon on Latmos:** Clefairy, Lunatone, Munna, Hatterene |
| **LEGENDS** (lands and epics) | 125 | 5 / 6 / 10 / 14 / 13 / 6 / 27 / 12 / 32 | Placed by `LEGENDS.md`; each land's "hosts" line in OIKOUMENE §4 |
| **Theoxenia** (Aethos) | 54 | 9 / 9 / 9 / 9 / 9 / 0 / 0 / 9 / 0 | Below |
| **Total** | **1,025** | | |

#### The epics and the facilities

| Where | What it hosts | Rule |
|---|---|---|
| **The Labors' far lands** (Thrace, Themiskyra, the Caucasus, Erytheia, the Garden) | The homes COVERAGE already gives them (E3, E7, W1, W5, W7): Mienshao, Chesnaught (wild only, PG-5), Druddigon, Heracross, Applin and the rest | Their own tables stand; homes are added, never removed (OIKOUMENE §8, rule 2) |
| **The Labors in Aethos, the Katabasis, Atlantis** | Aethos species first (POSTGAME §3.2: Atlantis is Aethos-only), plus shares from neighboring lands' families by type: Ghost shares below Tainaron at night, Water shares in the Labors' marshes | Shares only, no homes, so the Aethos epics stay Aethos |
| **The Odyssey's sea and islands** | The Western Sea's homes (H1–H6, H10) | ODYSSEY's tables plus COVERAGE's homes |
| **The Olympiad** | The Battle Factory's rentals draw from every generation; Victini and Kairazor | No homes: rentals aren't catches |
| **Naukratis's egg-ovens** | Every breedable species; the nine incense babies with the Arabian merchant's incenses | The safety net for the 247 Nursery species |
| **Daphne's field station** | The 15 fossils | One dig site per land (§5.4's kit) |
| **In-game trades** | About 20 households across the lands (§3) | Early access to a far land's species, never the only source |

#### Rarity and levels

Gen 3 gives each land table 12 slots at 20/20/10/10/10/10/5/5/4/4/1/1 percent. The lands fill them by one rule, so every area feels like its own place:

| Slots | Share | What goes there |
|---|---:|---|
| 1–2 (common) | 40% | **The area's signature:** the land's homeland Aethos line (below) in its home area, and the land's most on-theme new family. **At most one** of the two is a Gen 1–2 family, so no area opens like an old region |
| 3–6 (uncommon) | 40% | The area's other homes |
| 7–10 (rare) | 18% | Shares from neighboring areas, and the second homeland line |
| 11–12 (very rare) | 2% | The area's showpiece: a fully evolved line above the band (+2), or a night or weather visitor |
| **Augur's Eye** (3 hidden slots) | — | Pseudo-legendaries, Eeveelutions, Lucario and the like: hands-off, chain-huntable (OIKOUMENE §8) |
| **Behind gates** | — | The land's "for later" tables at +3 to +4, and statics at up to +4 (WORLD_EXPLORATION §4) |
| **Nurseries** | — | First stages, Lv 10–20, by month |

- **Levels:** each area takes its land's band from §2.3, never wider than 5. Evolved forms appear at their natural stage (BALANCE.md's ruling); a line that evolves by stone, trade or friendship appears at the stage before.
- **First impressions:** the first grass a player walks into in each land rolls its signature on a common slot. The first wild Pokémon in Egypt is a Hippowdon or the land's homeland Enigmaw, not a Diglett.

#### Each land's homeland Aethos lines

**The direction:** keep each land's signature Aethos species prominent, so the Oikoumene feels like a new world, not a rerun. Aethos's dex already holds lines whose myths come from these lands. In the Oikoumene they're the **homeland lines**: wild at the land's levels, on common slots in one home area and rare elsewhere in the land, named in its NPCs' talk ("Ours are bigger"). They join the tables as additions; no COVERAGE home moves. This was P-4 as a proposal; the user's direction makes it the plan, and §8 keeps it listed only because it changes OIKOUMENE §0's rule that the Aethos species stay in Aethos.

| Land | Homeland lines (Aethos dex) | Why | Where |
|---|---|---|---|
| Troad | Hoplomex (#22), Kourodin (#104) | Achilles's Myrmidons; the Kouretes of Ida's caves | The Achaean camp; the Ida Road and its grotto |
| Lydia | Midonos (#41), Hyphantis (#71), Dakrock (#129), Plouteras (#58) | Midas; Arachne of Hypaipa; Niobe on Sipylos; Ploutos's wealth underground | Gordion; Tmolus's far slope; the weeping rock in rain; the Thousand Hills and the Chasm |
| Black Sea | Taurivet (#82), Dorydrake (#112), Pythoros (#115), Promethex (#88), Pithound (#46) | Aietes's bulls; the sown men; the Fleece's serpent; Prometheus's fennel; Diogenes of Sinope | The Field of Ares; the Grove; the Caucasus; Sinope |
| North | Borapteryx (#126), Chionyad (#124), Hymnaria (#119), Krystolos (#128) | Boreas; Chione, his daughter; Apollo's swans; the ice | The Cave of Boreas; the Feather Wastes; the Meadow; the Rhipaean ice |
| Egypt | Enigmaw (#80), Ophidrop and Panacoil (#75–76) | The sphinx; the uraeus cobras of the tombs | The Pyramid Field; the Valley of Tombs at night |
| Aithiopia | Kynoketos (#32), Oinopard (#62), Thyrsivy (#60), Elektear (#120) | The Ketos at Andromeda's rock; Dionysus's leopard and ivy on Nysa; Helios's daughters at the Gate of Dawn | The Okeanos shore; Mount Nysa; the Gate of Dawn |
| Libya | Geogrip (#113), Stachypter (#51) | Antaeus; the grain of Kyrene | Antaeus's Ring; the Silphium Plateau |
| Far West | Laolith (#25), Melodrakon (#139, LABORS's Garden) | The earth-born giants of the Atlas peaks; Ladon | The Atlas Range; the Garden |
| Western Sea | Gigantomb (#84), Chelyra (#45), Ikaroth (#100) | The giants under the Phlegraean Fields; Zeno's tortoise; Icarus, missing from Daedalus's doors at Cumae | The Fields; Elea; Cumae |
| Okeanos | Amnoze (#72), Kalyptor (#78) | Endymion, asleep for ever; the shades at the Cimmerian pit | The Cave of Sleep; the Cimmerian shore |

The three starter lines (Hipling's, Kynder's, Nebrel's) stay out of every Oikoumene table (WORLD_EXPLORATION Q6). Unique story Pokémon (Aetarch as Zeus's eagle, Asterlorn, the Fates, the colossi) never appear wild.

#### The theoxenia guest-gifts

SYSTEMS §10's guest-gifts are 18 starter lines from Gens 1–5 and 8 (54 species), given by gods in disguise in Aethos. They stay exactly that:
- **Gift only.** No Oikoumene table, Nursery or trade carries them, so each stays a god's gift.
- **Breeding is the second copy.** Naukratis's egg-ovens hatch them, so a player who wants a second Bulbasaur can have one.
- **The other three generations' starters** (Gens 6, 7 and 9) are Lazarus's nine, and live **only wild** in the Oikoumene (PG-5): Froakie's line in the delta, Litten's among Bubastis's cats, Popplio's among Proteus's seals, Fennekin's among Libya's fennecs, Rowlet's in the Garden, Chespin's on the Thermodon, Sprigatito's on Nysa, Fuecoco's in Moeris, Quaxly's in the delta.
- **A post-game thank-you.** A guest who gave you a starter in Aethos turns up once in the Oikoumene, in the land that suits their god (Hermes at a crossroads herm, Hestia at a far hearth, Persephone in the Isles' meadows), and asks how the Pokémon is doing. If it's in your party, they give its Ichor Stone or a Mint. It's the guest-gift's echo, not a new gift.

#### Keeping the count honest

- `coverage.py` stays the single source. When a land's maps are built, its builder runs `coverage.py`'s check against the land's real encounter files and lists any species still unobtainable in the land's `design/maps/<Land>.md`.
- A land's 1.0 is done when every species in its "Homes" count is obtainable in a 1.0 save, including the ones whose stretch-tier map hasn't been built (their tables ride on a 1.0 map, as each land's map table says).
- **The 1.0 check:** 1,025 National Dex species plus 152 Aethos species, every one obtainable in one save, with no link cable.

---

## 3. The ten lands

**How to read a land.** Each section has the same parts, in the order a builder needs them:
1. **Identity:** the myth or culture, the palette and terrain, the signature landmark, and the awe moments (★).
2. **Maps:** every map with its size, encounter area (COVERAGE's code, so the wild tables plug straight in), level band and tier: **1.0** or **S** (stretch, OIKOUMENE §13). When a stretch map's area has no 1.0 map, the line says which 1.0 map carries its table.
3. **Stops:** each town, village and outcamp with its temple, shrine or outcamp, its herm, its hall and its services. OIKOUMENE §4's households stand; this guide adds the ones its new stops need.
4. **Roads and dungeons:** each map's beats in walking order, the way `tools/ichor/maps/kithairon.py`'s docstring reads, then a checks line.
5. **Pokémon:** signature species, rarer ones behind gates, homeland echoes (P-4) and gaps.
6. **Story:** the land's question (its main thread), side quests and lore.
7. **Returns and links:** gates for later, and threads to other lands.
8. **Bosses.**

**Every land's main thread is a question for the chart.** Alethea's Periodos (OIKOUMENE §5) asks the player to see for themselves. Each land poses one question that the old maps and songs answer wrongly. The player gathers three pieces of evidence round the land (a witness, a place and an object), the hall's champion gives the last, and Alethea writes the answer into the land's panel when the Emblem is set. The questions give each land a spine without a villain, and they play the theme: the truth against the better story.

### 3.1 Thrace and the Troad

> **The fate undone.** Every night for years Cassandra saw Troy burn. Last month she stopped. Troy is still standing, and she's not sure it ever burned at all.

**Identity.**
- **Myth:** the *Iliad*, seen from the Trojan side and told wrong by everyone. Troy stands; the war was "a summer"; the heroes are alive and have heard songs about their own deaths (PG-10).
- **Palette and terrain:** wheat gold and dry-grass green on the plain, the Skamander's blue and its tall reeds, pale limestone walls, Ida's dark pine and white springs, the Hellespont fast and deep blue. Bronze glints everywhere: armor in the river, nails in the beached hulls.
- **Signature landmark:** Ilion's walls, sloping, pale and two screens tall, with the Skaian Gate and the great oak before it.
- ★ **Vista, "The Walls":** the Skamander Plain's road tops a rise between two burial mounds, and the camera pans slowly up Ilion's walls to the tower over the Skaian Gate. It is the first wall in the game taller than the screen.
- ★ **Set piece, "The river rises":** at the plain's middle ford the Skamander, angry at the armor choking his reeds, rises in a wave across the screen: the current tiles flip, the ford floods and a scripted wave sweeps east. It starts the river god's quest.
- ★ **Vista, "Zeus's seat":** from Gargaros's summit at dusk the whole plain lies below: Ilion small and gold, the Hellespont, the ribs of the Achaean camp, and on the far horizon a gray island with a peak, Samothrake, where Poseidon sat to watch the war (*Iliad* 13.10–14). Aethos is out there.

**Maps.** Wild 60–66; behind later gates 66–70.

| Map | Kind | Size | Area | Levels | Tier |
|---|---|---|---|---|---|
| `Sestos` | Port town | 40×32 | — | — | 1.0 |
| `Troad_Hellespont` | Sea lane, with the Elaious headland | 28×72 | T1 | 60–62 | 1.0 |
| `Troad_SkamanderPlain` | The great road | 96×36 | T2 | 61–64 | 1.0 |
| `Troad_TombOfIlos` | Crypt under a mound, 2 floors | 24×20 each | T2 (cave slots) | 63–65 | 1.0 |
| `Ilion` | City, with the Skaian Gate hall (PERIODOS §4.1) | 52×44 | — | — | 1.0 |
| `Troad_WallsOfLaomedon` | The land's dungeon, 3 floors | 32×28 each | T6 | 63–66 | 1.0 (2 floors); S (the 3rd) |
| `Chryse` | Village and the Smintheion grounds | 40×30 | T7 | 61–63 | 1.0 |
| `Troad_IdaRoad` | The climb | 36×96 | T3 | 62–65 | 1.0 |
| `Troad_Gargaros` | Peak dungeon, 3 floors and the summit | 28×28 each | T4 | 63–66 | 1.0 |
| `Troad_HebrosShore` | Route beside LABORS's Bistonian Plain | 60×24 | T5 | 62–66 | S. At 1.0, T5's table rides on the Elaious shore |

**Stops.**

| Stop | Temple, shrine or outcamp | Herm | Hall | Services |
|---|---|---|---|---|
| **Sestos** | **Hero's tower**, a lighthouse and a shrine of Aphrodite, whose priestess Hero was | A bronze-capped herm at the head of the quay | — | Asclepeion, Agora, the Super Rod |
| **Elaious** (a landing on the Hellespont lane) | **The shrine of Protesilaos** among its elms | A weathered herm on the jetty | — | A healer in the shrine |
| **The Achaean camp** (outcamp, the plain's midpoint) | **An altar to Apollo** of stacked oars, which the veterans built to say sorry | A herm carved from a steering oar | — | An old army surgeon heals |
| **Ilion** | **The temple of Athena** with the Palladion | A herm inside the Dardanian Gate (Hermes led Priam to Achilles, *Iliad* 24) | **The Skaian Gate:** Prince Hektor | Asclepeion, Agora, Odysseus's guest-room |
| **Chryse** | **The Smintheion**, Apollo's temple of mice | A herm with a mouse at its foot, as Apollo Smintheus's statue had (Strabo 13.1.48) | — | A healer in the temple |
| **The shepherds' fold** (outcamp, the Ida Road's midpoint) | **A rock shrine of the Mother of Ida** | A pine-trunk herm | — | The xenia host's hut: a heal and a bed |
| **Gargaros summit** | **Zeus's altar** | An eyrie: a sighting stone at the peak's foot makes it a Wings landing | — | — |

**New households** (OIKOUMENE §4.1's stand):
- **Elaious, the elm-keeper.** She waters the elms on Protesilaos's mound, which wither when they grow tall enough to see Troy (Pliny 16.238). Bring her a cutting from Ida's springs and plant it in the hollow below the mound. Next visit it has grown and hasn't withered. Reward: a Miracle Seed, and "It can't see Troy from there. Maybe it doesn't want to."
- **The Achaean camp, the carpenter's hut.** Epeios's apprentice, still here. He was building a wooden horse "for a trick" when everyone went home. Quest below.
- **The Achaean camp, the veteran's tent.** A Myrmidon who swears it was ten years. In-game trade: his Hoplomex (P-4) for your Gurdurr.
- **Chryse, the trapper.** He used to trap mice and now feeds them, because the god's back. Daily: a Leppa Berry, or a Light Clay once.
- **The shepherds' fold, the judge's widow.** Her husband once judged a beauty contest on this meadow, between three women who wouldn't give their names. She keeps the prize, a golden apple with a bite out of it. Lore, and a Lum Berry daily.

**Roads and dungeons.**

**The Hellespont** (28×72, north to south). *A fast strait between two shores.* The current runs east two tiles a step; surf across it on a diagonal. Helle's rock stands mid-channel, where the ram's rider fell (its mooring stone starts the Argo's Road, §3.3). The Elaious headland on the west shore has the jetty and herm, the elms on Protesilaos's mound, the shrine, and a sand cove whose grass carries T5's table at 1.0. A whirlpool shields a cove with a sealed jar (Triton's Conch). Halfway down, a darker patch with a mast-top showing is **a drowned Achaean trireme** (the Pearl, later).

**The Skamander Plain** (96×36, west to east; the great road). *From the beach where the Greeks landed, across the river plain, to the walls.*
1. **The beach and the Achaean camp.** Beached hulls rotted to their ribs, cold hearths, a tent line. The camp is the **outcamp** (surgeon, oar herm, three tents). The **half-built wooden horse** stands on its sledge, one flank planked, with a ladder up into its belly (stairs to treasure: a Big Nugget, and ODYSSEUS WAS HERE scratched inside, which he denies). The first trainer, a Trojan hoplite, patrols the dune path in plain view.
2. **Band 1** in the beach grass between the camp and the river marsh, walled by dunes and the sea.
3. **The marsh.** The Skamander's mouth, reeds taller than the player. Two Sickle reed walls open side pockets (a Mystic Water; the grass with Farfetch'd's hidden slot). Current tiles push you downstream along the river's edge. **A hoplite pair** holds the plank bridge over the main channel: the first chokepoint.
4. **The middle ford** and "the river rises" (★). Before the river god's quest the ford floods on a timer; after it, the ford stays low. A charioteer waits on the far bank in the only gap through a thorn fence.
5. **The mounds.** Three great burial mounds of heroes the songs disagree about. **Band 2** runs between them, right after the charioteer. The Tomb of Ilos's mouth is in the largest mound (the Torch). A grave stele carries a dented helmet and a name no song mentions (remains, §5.4: reading it the first time gives a Pythian Laurel).
6. **The wheat.** Standing wheat walled by field walls (**band 3**), a threshing floor where a farmer battles you, and the great oak.
7. **The rise and the walls** (★ "The Walls"), the Skaian approach, and the east edge into Ilion.
- **Checks:** bands 3; mandatory trainers 5 (the hoplite pair, the charioteer, the farmer, the gate guard); rest: the Achaean camp; climb: the horse's ladder and the mound stair; cave: the Tomb of Ilos; ledges drop west toward the beach.

**The Tomb of Ilos** (2 floors, dark). *The founder's tomb under his mound* (*Iliad* 11.166). Floor 1: a ramp down, a brazier that lights the floor for good, two side niches behind cobwebs (the Torch), and **the Oikoumene's first plate puzzle**: one drum, one bronze plate, a grille that opens (the teach, §5.1). Floor 2: the burial chamber, Ilos's bronze bed, a shaft ladder up to a capstone on the mound's top (a one-way shortcut out), and a **shadow door** (the Helm of Hades, later) to the king's inner room. Wild: Doublade and Phantump from T2's and T6's shares.

**Ilion** (52×44). *Priam's city on its hill.* The Dardanian Gate and its herm face the plain road; the Asclepeion and Agora are within one screen of it. Streets climb in terraces, and a drum-blocked stair (the Girdle) shortcuts the climb. The citadel holds Priam's palace, the temple of Athena and the Skaian Gate's tower (the hall). A **tower stair** inside the walls climbs to the wall walk: a smaller view over the plain, and a Choice Scarf where the watchmen sat. Households: OIKOUMENE §4.1.

**The Walls of Laomedon** (the land's dungeon). *The undercroft of the walls Poseidon and Apollo built and were never paid for* (*Iliad* 21.441–457): a building site abandoned mid-course, with scaffolds, cranes, stacks of drums, and the builders' tally marks on the walls.
- **Floor 1, teach and test.** The gods' masons' marks are bronze plates in the floor. Push drums onto them to "set the courses"; each set course raises a stone lift one level. Three plates, three drums, one lift. A reset lever by the stair undoes a bad push (§5.1).
- **Floor 2, combine.** A flooded gallery. Two plates hold a sluice shut so the water drains and drums can be rolled across the floor; pull the lever to flood it again and surf to an island with the last drum. Rubble (the Hammer) and bronze chains (the Labrys) close side passages. Gurdurr laborers in the dark, Bisharp in the Augur's Eye.
- **Floor 3 (S).** The wage room: the two gods' tablets of what Laomedon owed them, and Stakataka's chamber (LEGENDS).
- **Rest:** a masons' spring on floor 2. **Payoff:** Hard Stone, a TM and Stakataka's lead. **Remains:** the tally walls, and a mason's forgotten lunch, a loaf gone hard as the stone.

**Chryse and the Smintheion** (40×30). *A temple village of mice.* Electric mice in all the grass, the census minigame in the temple (OIKOUMENE §4.1), and the trapper's house. It sits at the Ida Road's foot, the second way onto the mountain.

**The Ida Road** (36×96, south to north; a climb). *Up "many-fountained Ida" from Chryse to Zeus's peak.*
1. Chryse's pasture, a shepherd in plain view, **band 1** in the hill grass between thorn fences.
2. **The first switchback** up a limestone scarp: a cut stair with a hoplite of Ida at its head (a chokepoint).
3. **The springs:** three falls down the mountain face. One has a cave mouth at its top (the Horn): the Idaean grotto, with a Water Stone and Ganymede's lost cup (lore). A rubble pocket (the Hammer) hides Hard Stone.
4. **The shepherds' fold** (outcamp, the midpoint rest): the Mother's rock shrine, the xenia host, the judge's widow and the pine herm.
5. **The pinewood:** **band 2** under the pines, walled by trunks, right after a woodcutter's sight line.
6. **The Crook face:** handholds up to Ganymede's spring, where Zeus's eagle stooped. A ledge pool with a Pretty Feather and a Braviary static (Lv 68).
7. **The high meadow:** **band 3**, the treeline, the eyrie's sighting stone and the mouth of Gargaros.
- **Checks:** bands 3; mandatory trainers 4; rest: the fold; climb: two stairs and a Crook face; cave: the grotto; ledges drop south.

**Gargaros Peak** (3 floors and the summit). Wind ledges push you a tile when you step off cover; eagle nests in the dead ends hold items; on floor 2 a drum-on-plate stair (two plates lower a rope bridge). The summit has Zeus's altar and the vista (★). Zapdos waits there on LEGENDS's terms.

**Pokémon.**
- **Signature:** Falinks (the plain's hoplite file), Rapidash (Troy "of the fine horses"), Apollo's mice at Chryse (Pikachu, Togedemaru, Dedenne, Pachirisu, Tandemaus), Braviary (Ida's eagles), Gurdurr (the wall-builders).
- **Rare behind gates:** Farfetch'd in the Sickle reed pocket (Augur's Eye); Bisharp in the Walls (Augur's Eye); the Braviary static at Ganymede's spring (the Crook, Lv 68); Relicanth and a Dhelmise static in the drowned trireme (the Pearl, Lv 70); Stakataka and Zapdos (LEGENDS).
- **Homeland lines (§2.7):** Hoplomex, Achilles's Myrmidons, common at the Achaean camp (Lv 64); Kourodin, the Kouretes, in the Idaean grotto and on the Ida Road.
- **Gaps:** none.

**Story.**
- **The land's question: "Was there a war?"** Alethea needs one true line for the panel. **A witness:** Priam ("A summer. Mostly arguing."). **A place:** the camp's hulls, which rotted for longer than a summer. **An object:** the Skamander's armor, which the river kept; the river god counts nine days of real fighting. Hektor's hall gives the last: he shows you the wall where his song says he died, and there's no mark on it. Alethea writes: *"There was a war. It was smaller than the song and longer than the Trojans say. Everyone who ought to be alive is."*
- **Side quests:** **the river god's armor** (clear five sets of bronze from the reeds and pools, using the Sickle, the Conch and one drum; reward: the ford stays low, a Mystic Water, and "Somebody finally tidied up."); **the horse** (bring the apprentice three straight pines from the Ida Road, cut with the Sickle; he finishes the horse, turns it into a boat and sails home: "Ten years late. Or a summer." Reward: a Bright Powder, and the ladder stays); **the elm cutting**; and OIKOUMENE's Hero's lamp, the mason's chisel, the peplos and the mouse census.
- **Lore:** the elms that won't look at Troy; the dented helmet with an unsung name; Ganymede's cup; the judge's widow's apple; the tally marks.

**Returns and links.**
- **For later:** the drowned trireme (the Pearl); the Tomb of Ilos's inner room (the Helm of Hades: Ilos's bronze scepter and a lead toward Deoxys's four marks in LEGENDS); the Mirror of Truth in Athena's temple, where a painted frieze of Troy burning shows the city standing (lore and a Reaper Cloth); an arrow-stone on Gargaros pointing at an islet in the Hellespont (Abaris's Arrow: a Skarmory static, Lv 70, and a Star Piece).
- **Links:** the Hellespont runs on to the Bosporus and the Black Sea; the Royal Road runs east to Lydia; LABORS's Thrace is across the water. **Memnon visits Troy** after Aithiopia's Emblem (§3.6): he and Hektor meet at the Skaian Gate, two men who've heard their own deaths sung. **Helen's phantom** (§3.5): the Mirror shows a woman on the Skaian tower who isn't there. **Achilles's tent** at the camp is empty, with a sign: GONE TO SEE MOTHER (Leuke, §3.3).

**Bosses.** Prince Hektor at the Skaian Gate (PERIODOS §4.1, 74–76). Odysseus at Ilion (76–78, optional). The Achaean veteran (72, a daily rematch). Zapdos and Stakataka (LEGENDS).

### 3.2 Lydia and Phrygia

> **The fate undone.** The oracle told Croesus that if he crossed the Halys a great empire would fall. He's still deciding whether to ask whose.

**Identity.**
- **Myth:** the first coins and the richest king (Herodotus 1.6–94); Midas and his touch, washed off in the Pactolus; his ears and the whispering reeds; the Gordian Knot; Niobe weeping on Sipylos; Tantalus's punishment; Arachne of Hypaipa; Gyges's ring.
- **Palette and terrain:** electrum gold and Lydian purple; green river flats and vine terraces; the Pactolus's glittering sand; gray Sipylos and its weeping rock; in Phrygia, pale tufa cliffs carved with house-fronts for the Mother, and great grass-covered tomb mounds.
- **Signature landmark:** Sardis's acropolis, a broken tooth of rock over the city, and the plain of the royal mounds behind it, the Thousand Hills, with Alyattes's tomb, which Herodotus ranked after only Egypt's and Babylon's works (1.93).
- ★ **Vista, "The gold river":** from Tmolus's vine terraces at sunset, the Pactolus valley glitters below, Sardis's acropolis black against it, and the Thousand Hills roll away east.
- ★ **Set piece, "Inside the mound":** at Gordion you tunnel into the great tumulus and break through into the timber chamber: a king's bed, bronze cauldrons, the funeral feast still on the table, untouched for centuries. The music stops. It is the tomb of Gordias, Midas's father (P-7). Midas himself is alive and upstairs in Gordion, in a very large hat.
- ★ **Set piece, "The weeping rock":** on Sipylos, when it rains, the cliff's face runs with water like tears, and the Niobe stone becomes a woman's shape for as long as the rain lasts.

**Maps.** Wild 63–70; behind later gates 70–73.

| Map | Kind | Size | Area | Levels | Tier |
|---|---|---|---|---|---|
| `Lydia_RoyalRoad` | The great road, from Ilion's east gate to Sardis, over Sipylos | 104×32 | L1, L5 | 63–66 | 1.0 |
| `Lydia_TantalusPalace` | Sunken palace under Sipylos's lake, 2 floors (a 3rd behind the Pearl) | 30×26 each | L8 | 66–68 | 1.0 |
| `Sardis` | City, with Croesus's treasury hall (PERIODOS §4.2) and the Thousand Hills | 56×44 | — | — | 1.0 |
| `Lydia_ChasmOfGyges` | Earthquake chasm among the mounds, 2 floors (3rd S) | 28×28 each | L7 | 66–68 | 1.0 |
| `Lydia_Tmolus` | The climb: the Pactolus gorge, the vine terraces, and Hypaipa on the far slope | 40×88 | L2, L3, L6 (night) | 64–68 | 1.0 |
| `Gordion` | Phrygian town, with the Midas valley's rock-cut shrines on its west approach | 48×40 | L1 (east) | 65–68 | 1.0 |
| `Gordion_Tumulus` | The great mound: a tunnel and the timber chamber | 20×24 | — | — | 1.0 |
| `Miletos` | Port town (Hecataeus, Thales) | 44×36 | — | — | S. At 1.0 Hecataeus stays at Sardis's guest-house |
| `Lydia_Maeander`, `Lydia_Latmos` | River route; moon mountain | 60×30; 36×40 | L4, L6 | 64–68 | S. At 1.0 L4's surfers fish and swim the Pactolus; L6 is Tmolus's night table |

**Stops.**

| Stop | Temple, shrine or outcamp | Herm | Hall | Services |
|---|---|---|---|---|
| **The post-station** (outcamp, the Royal Road's midpoint) | **A shrine of Hermes of the Road** with couriers' votive sandals | A Lydian waystone: a stele with a crouching lion, the stamp on Croesus's coins | — | The station-master heals; fresh horses (a Rapidash ride back to Ilion, once a day) |
| **Sardis** | **The temple of Artemis of Sardis**, huge, unfinished, its columns still in scaffolding | A lion stele inside the city gate | **Croesus's treasury:** King Croesus | Asclepeion, Agora, the mint, the dicing-house |
| **Hypaipa** (a hamlet on Tmolus) | **The temple of the Persian Artemis**, where a fire burns that the priests say lights itself | A lion stele by the weavers' well | — | A healer in the temple |
| **The vintners' terrace** (outcamp, Tmolus's midpoint) | **Dionysus's vine shrine**: Tmolus was his mountain | A vine-wrapped post herm | — | Heal; a press where the vintner gives a daily berry |
| **Gordion** | **The temple of Zeus the King**, with Gordias's ox-cart and the Knot | A Phrygian herm: a niche of the Mother cut into the rock beside the gate | — | Asclepeion, Agora |

**New households:**
- **The post-station, the courier.** Herodotus's relay: "neither snow nor rain" (8.98). Race him from the station to Sardis's gate along the Royal Road in his time; reward: a Quick Powder, then a daily rematch for a Rare Candy. The station also keeps the **last relay** (remains, below).
- **Sardis, the helmet-dropper.** A soldier on the acropolis wall who keeps dropping his helmet down the cliff and climbing down after it. Watch where he climbs: this is how Sardis fell, in Herodotus (1.84). Follow his path up the "unclimbable" side for a secret stair to the summit lookout: a Big Nugget and the best view of the Thousand Hills.
- **Gordion, King Midas.** Very old, very rich, very hatted. He wants the reeds on Tmolus cut before the king walks by (OIKOUMENE's barber quest), and he'll trade his Midonos (P-4) for anything you caught on Tmolus, "anything that isn't gold."
- **Hypaipa, the spinner.** Arachne's niece, who weaves a map of Lydia into a cloth and gets it wrong on purpose so you'll correct it: three errors, three corrections (a Thread Spool, a Silk Scarf, a Hyphantis gift egg, P-4).

**Roads and dungeons.**

**The Royal Road** (104×32, west to east; the great road). *From Troy's hinterland over Sipylos's shoulder and down the Hermos valley to Sardis.*
1. **Ilion's east gate** and a pass warp into the Lydian hills. A Lydian courier in plain view (the first trainer).
2. **Band 1** in the olive-and-grass hills, walled by dry-stone terraces.
3. **Sipylos.** The road climbs the mountain's flank on a cliff road (a cut stair). The **weeping rock** stands across a gorge (★ in rain). Below it, **Tantalus's lake**, black and still, with the sunken palace's roof under the water and its mouth at the shore. A hoplite pair holds the cliff road's narrowest point (a chokepoint).
4. **The fourteen mounds** below the rock, small and grassed: Niobe's children, buried by the gods after nine days (*Iliad* 24.602–617). A sign, and nothing to take: the remains of the lost don't always pay (§5.4).
5. **The post-station** (outcamp, the midpoint).
6. **The Hermos valley:** **band 2** in the river meadow, right after a charioteer at the bridge; a Sickle reed pocket on the river bank (a hidden Gimmighoul coin pile, 5 coins).
7. **The vineyard slope:** **band 3** between vine rows (the Sickle cuts one row for a shortcut back west), a Lydian musician on the only path through.
8. **Sardis's west gate.**
- **Checks:** bands 3; mandatory trainers 5; rest: the post-station; climb: Sipylos's cliff road; cave: Tantalus's palace; ledges drop west.

**Tantalus's Sunken Palace** (2 floors). *A palace laid for a feast that never ends.* The tables are set with fruit turned to stone; water pours in from the lake and drains away the moment you reach it.
- **Floor 1:** the moving-tile fruit (OIKOUMENE §4.2) and **the plate puzzle**: three drums on three plates seal the drains, so the hall stays flooded and you can surf to the fruit table's island (a Sitrus Berry pile and Lickitung, the land's oddest home).
- **Floor 2:** combine: the plates also hold a portcullis; seal two drains and leave the third open to drop the water just enough to walk the lower hall and reach the stair.
- **Later:** a third floor under deep water (the Pearl): Tantalus's own hall, his shade (a Lv 76 battle, Ghost), and the Sitrus tree he can never reach. "Take one. Please. I'll watch."

**Sardis** (56×44). The lower city of mud-brick and the Pactolus running through the agora with gold in its sand; the temple of Artemis; Croesus's palace on the slope; the acropolis rock above; and east of the walls, the Thousand Hills with Alyattes's great mound. Asclepeion and Agora at the west gate. The **Chasm of Gyges** opens in the mound field: a crack in the earth with a ladder down.

**The Chasm of Gyges** (2 floors; the land's dungeon). *The shepherd Gyges found a chasm after an earthquake, and in it a hollow bronze horse, and in the horse a giant's body with a gold ring* (Plato, *Republic* 2.359d–360b).
- **Floor 1:** a cracked cave of tumbled mound-earth, dark (the Torch), rubble (the Hammer), and bronze chains across a side gallery (the Labrys) to a niche with a Metal Coat. Klefki and Bronzong.
- **Floor 2:** the bronze horse, huge, on its side. Its belly has four doors, one per leg, each held shut by a plate. **The plate puzzle:** four plates, three drums, and the fourth weight is you: stand on the last plate and the door opens only while you stand there, so you must place the drums so that the door you need is the one you can reach from it. Inside: the giant's bones and an empty finger bone. The ring is gone, or it's there and you can't see it (the Mirror, later).
- **Later (floor 3, S):** Hoopa's chamber (LEGENDS).

**Mount Tmolus** (40×88, north to south; the climb). *Up the Pactolus gorge from Sardis, over the vine terraces, down to Hypaipa.*
1. **The Pactolus gorge:** gold-panners in the shallows (the panning minigame, OIKOUMENE §4.2), a ford, fishing water with Seaking (the "gold in the water"), and **band 1** on the gravel bars.
2. **A waterfall stair:** the Pactolus falls off a ledge; the Horn climbs it to a cave behind the fall with a Gold Bottle Cap.
3. **The vine terraces:** cut stairs between terraces, a vintner pair holding the stair (a chokepoint), **band 2** in the long grass between the vines.
4. **The vintners' terrace** (outcamp, the midpoint).
5. **The contest meadow** where Apollo and Pan played and Midas voted wrong. The reed bed whispers. A Crook face up to the summit cairn (a Moon Stone by night, and Clefairy).
6. **The far slope:** **band 3** in the pinewood after a Phrygian piper, then **Hypaipa**.
- **Checks:** bands 3; mandatory trainers 4; rest: the vintners' terrace; climb: the waterfall (Horn), the terrace stairs and a Crook face; cave: the fall's cave; ledges drop north toward Sardis.

**Gordion** (48×40). *The Phrygian capital on its mound.* The west approach runs through the Midas valley: tufa cliffs carved with house-fronts for the Mother, one inscribed MIDAS. A rock-cut stair climbs the largest face to a high niche with a Shiny Stone (stairs to treasure). The town: the temple of Zeus the King with the ox-cart and the Knot, Midas's house, the barber's, the wheelwright's, the piper's (OIKOUMENE §4.2), and the great tumulus on the plain outside.

**The Tumulus** (one map). A tunnel cut through the mound's fill (the Hammer twice and a Thread anchor ring at a shaft), ending at a timber wall. Break through (★ "Inside the mound"). The chamber: the bed, nine bronze cauldrons, the feast. Read the bed: "A king lies here who tied a knot." Take nothing, and Alethea writes it down; take the one cauldron that's loose and it holds an Amulet Coin.

**Pokémon.**
- **Signature:** Gimmighoul (its coin piles in the mounds and the river), Klefki (the treasury's keys), Bronzong (Lydian bronze), Seaking (the Pactolus's gold fish), Spidops (Hypaipa's weavers' pest), Clefairy and Lunatone (Tmolus at night).
- **Rare behind gates:** Gimmighoul (roaming) in the Chasm (Augur's Eye); Hatterene on Tmolus's summit at night (the Crook, Lv 70); Tantalus's shade (the Pearl, Lv 76); Hoopa (LEGENDS).
- **Homeland echoes (P-4):** Dakrock (Niobe's line) at the weeping rock in rain; Midonos (Midas's line) as Midas's trade; Hyphantis (Arachne's line) as the Hypaipa gift egg.
- **Gaps:** none.

**Story.**
- **The land's question: "Did Midas really turn things to gold?"** **A witness:** Midas, who won't take his hat off and won't talk about his hands. **A place:** the Pactolus, where he washed the touch away, and the gold in its sand. **An object:** the barber's reeds, which whisper the secret. Croesus's hall gives the last: weighed in his balance, the river's gold and the gold of Midas's old cup are the same metal. Alethea writes: *"Midas turned things to gold, and washed it into the Pactolus, and the river's been paying ever since. About the ears, we didn't look."*
- **Side quests:** **the last relay** (below); **the helmet path**; the spinner's map; the courier race; and OIKOUMENE's mint, panners, barber, wheelwright, piper, weaving school and dyer.
- **The last relay** (remains). In the post-station's back room, a courier's satchel and a sealed tablet that never arrived. The station-master: "He came in, sat down, and didn't get up. We never knew who it was for." Carry it to Gordion. It's for Midas, from his barber, and it says one word: SORRY. Reward: Midas laughs for the first time in years and gives you an Ability Patch.
- **Lore:** Niobe's fourteen mounds; Tantalus's stone feast; the empty finger bone; the inscribed MIDAS facade; Alyattes's mound, built by "the market people, the craftsmen and the girls" (Herodotus 1.93).

**Returns and links.**
- **For later:** Tantalus's third floor (the Pearl); the giant's ring (the Mirror of Truth shows it on the empty finger: take it and the bones settle; reward: a Bright Powder and a lead for Hoopa's quest in LEGENDS); the Thousand Hills' largest mound, Alyattes's, opens as a shadow door (the Helm of Hades: a two-room tomb with gold-leaf Gimmighoul, a Gimmighoul static, Lv 72); an arrow-stone on Tmolus's cairn pointing at Latmos's peak (Abaris's Arrow; S: Endymion's cave early).
- **Links:** the Royal Road from Ilion; Hecataeus checks the chart (OIKOUMENE §5); Solon (OIKOUMENE §4.2) asks after Kroton's Milo (§3.9), the man he'd call happy; **the Halys**: the Royal Road's east end is a ford with a sign, beyond which the chart is blank. Croesus stands at it some evenings. "I could cross it. I could ask whose empire." He never does; it's the Oikoumene's one deliberate non-gate.

**Bosses.** King Croesus in his treasury (PERIODOS §4.2, 75–77). Tantalus's shade (76, later). The courier (74, daily).

### 3.3 The Black Sea: Colchis, the Amazons and the White Isle

> **The fate undone.** Achilles was offered a short glorious life or a long forgotten one. The offer's off. He's visiting his mother to talk it over.

**Identity.**
- **Myth:** the *Argonautica*: the Clashing Rocks, Phineus and the Harpies, Aietes's bronze palace, Medea, the bulls and the sown men, the Fleece and its serpent; the Chalybes' iron; Achilles's White Isle; LABORS's Amazons and Prometheus.
- **Palette and terrain:** a dark green sea under low cloud, gray headlands, Colchian log towers in wet forest, the Phasis's tall reeds and its pheasants, bronze everywhere in Aia, the Caucasus white along the east, Leuke's bone-white rock and seabirds.
- **Signature landmark:** Aia's bronze palace and its four fountains of milk, wine, oil and water (*Argonautica* 3.215–231).
- ★ **Set piece, "The Clashing Rocks"** (P-1 moves it into 1.0): arriving through the Bosporus, the two cliffs twitch; Phineus hands you the dove; you sail the side channel behind it (OIKOUMENE §4.3).
- ★ **Vista, "The Fleece in the dark":** the Grove of Ares at night is black under the oaks, but far ahead a gold glow lights the canopy from below. Each floor the glow is brighter, until the last opens on the oak and the Fleece blazing on it, the serpent wrapped round the trunk.
- ★ **Set piece, "The sown field":** on the Field of Ares, the armed men rise out of the furrows in rows across the whole screen (OIKOUMENE §4.3, step 3).
- ★ **Vista, "The White Isle":** Leuke at dawn: seabirds sweeping the temple steps with wet wings (Arrian, *Periplus* 21).

**Maps.** Wild 64–72; behind later gates 72–75. LABORS's Themiskyra, the Thermodon Road and the Caucasus Crag sit inside it.

| Map | Kind | Size | Area | Levels | Tier |
|---|---|---|---|---|---|
| `Pontos_Bosporus` | Sea lane, with the Clashing Rocks and the side channel | 32×64 | E1 | 67–69 | 1.0 |
| `Salmydessos` | Port village on the Thracian shore | 36×28 | — | — | 1.0 |
| `Pontos_PonticCoast` | Sea lane of headlands, with landings at Sinope and Chalybia | 96×40 | E2 | 68–70 | 1.0 |
| `Chalybia` | Iron village and its forges, at a landing | 44×36 | E8 | 69–71 | 1.0 |
| `Aia` | City at the Phasis mouth, with Medea's hall (PERIODOS §4.3) | 52×44 | — | — | 1.0 |
| `Pontos_Phasis` | The great road: upriver to the Field of Ares | 100×36 | E4, E5 | 69–72 | 1.0 |
| `Pontos_GroveOfAres` | The Fleece's wood, 3 floors | 32×32 each | E6 | 70–72 | 1.0 |
| `Leuke` | The White Isle | 32×28 | E9 | 70–72 | 1.0 |
| `Pontos_CaucasusCaves` | Under LABORS's crag, 3 floors | 28×28 each | E7 | 68–72 | S. At 1.0, E7 is LABORS's crag table |
| `Pontos_IsleOfAres` | Ares's island and its birds: Flying's crown (§9) | 36×30 | — | 72–75 | 1.0 under P-18 (Yveltal, LEGENDS) |
| `Aia_GardenOfHecate` | Medea's poison garden: Poison's crown (§9) | 40×36 | E10 (new) | 70–72 | 1.0 under P-18 |

**Stops.**

| Stop | Temple, shrine or outcamp | Herm | Hall | Services |
|---|---|---|---|---|
| **Salmydessos** | **A shrine of Boreas**, whose sons drove the Harpies off Phineus's table | A Thracian herm with a horseman carved on it | — | Asclepeion, Agora, the Super Rod |
| **Sinope** (a landing on the coast lane) | **A shrine of Autolykos**, the city's founder | A herm by an empty storage jar on the beach (Diogenes was born here, P-4) | — | A healer |
| **Chalybia** | **The forge-shrine of Hephaestus**, a furnace that's never let go out | A herm of black iron, the only iron herm in the world | — | Healer; the ironmaster's shop (every Steel item) |
| **Aia** | **The temple of Helios**, Aietes's father; and **Hecate's shrine** under the palace | A bronze herm with a bull's head | **Aietes's bronze palace:** Medea | Asclepeion, Agora |
| **The Argonauts' backwater** (outcamp, the Phasis's midpoint) | **An altar the Argonauts left**, with a carved ship on it | A herm made from a broken oar with a name burned into it | — | A Colchian fisher-healer; a bed in his log tower |
| **Leuke** | **The temple of Achilles**, which the birds sweep | A white marble herm | — | The temple keeper heals |

**New households:**
- **Sinope, the jar-keeper.** An old woman who rents out the empty jar on the beach. "A philosopher lived in it once. He left for somewhere warmer." Gift: a Pithound (P-4), "it keeps sitting in the jar."
- **The backwater, the fisher in his log tower.** Colchians lived in timber towers (Vitruvius 2.1.4). A ladder inside climbs four floors to a lookout with a Dragon Scale (stairs to treasure). He remembers the night the Argo hid in these reeds.
- **Aia, the bull-keeper.** He tends Aietes's bronze bulls and is scared of them. In-game trade after the Fleece: his Taurivet (P-4) for your Tauros.
- **Chalybia, the bellows-boy.** Asks you to fire the three cold furnaces (the plate puzzle below). Reward: Meltan's lead (LEGENDS) and a Metal Alloy.

**Roads and dungeons.**

**The Bosporus** (32×64). The strait's current runs north into the Black Sea. Phineus's house at Salmydessos is at the north end. The Clashing Rocks stand open on the main channel; their **side channel** to the west is the timing passage with the dove (OIKOUMENE §4.3): a hidden cove behind it with a sealed jar and an Ichor Stone. A whirlpool (Triton's Conch) shields a second cove.

**The Pontic Coast** (96×40). *A long coast of headlands and Greek colonies.* Three landings (Sinope, Chalybia, and LABORS's Thermodon mouth), Mariandynian cliffs with a cave in a sea cliff (Conch; the **Acherusian cave**, where the Greeks said Herakles dragged Kerberos up, *Argonautica* 2.353–356: a one-room shrine with a Spell Tag and a link to Labor 12), whirlpools, and Argonaut trainers on rafts.

**Chalybia and the forges** (44×36). *Iron country: slag heaps, black earth, furnaces.* The village, then the forge yard: **the plate puzzle.** Three furnaces, each fed by bellows that work only when an ore cart stands on its plate; carts are drums in the Chalybes' iron skin (§5.1). Rails split and join, so carts have to be routed in order. Fire all three and the ironmaster's vault opens (a Metal Alloy, Meltan's lead). Rock Smash slag piles hold Coalossal.

**Aia** (52×44). The bronze palace's four fountains in its forecourt; the Helios temple on the acropolis; the harbor at the Phasis mouth with Argonaut ships' moorings, all empty but one; the palace workshop where Rotom changes form. A **palace stair** climbs to the roof cistern that feeds the fountains: four taps, and turning them in the order milk, wine, oil, water gives a Sweet Apple, a Berry Juice, a Shell Bell and a Mystic Water, once each.

**The Phasis** (100×36, west to east; the great road). *Upriver from Aia through the reeds to the Field of Ares.*
1. **Aia's river gate**, an Argonaut veteran in plain view, then **band 1** in the reed meadow, walled by river and forest.
2. **The pheasant reeds:** Sickle reed walls with pockets (a Sharp Beak; a nest of Unfezant), current tiles along the banks, a Colchian archer pair holding a log bridge (a chokepoint).
3. **The backwater** (outcamp, the midpoint): the Argonauts' altar, the oar herm, the fisher's log tower, the Argo's mooring stone (the Argo's Road, below).
4. **The wet forest:** **band 2** in the undergrowth after a sorceress's sight line; a Crook face up a gorge wall to a ledge with a Dragon Fang and a rare Druddigon.
5. **The plough-field:** the **Field of Ares**, its long furrows, the bronze bulls' stall, the Fleece tasks (OIKOUMENE §4.3), and **band 3** in the field's margin. Rusted helmets lie in the furrows, the sown men's from Jason's day (remains).
6. **The Grove's mouth** at the forest edge.
- **Checks:** bands 3; mandatory trainers 5; rest: the backwater; climb: the log tower and a Crook face; cave: the Grove; ledges drop west.

**The Grove of Ares** (3 floors; the land's dungeon). Dark oak wood under a roof of branches, mapped as a cave (the Torch lights braziers; the Fleece's glow is the landmark ahead).
- **Floor 1, teach:** the serpent's shed skins block paths; burn them (the Torch). A single drum-on-plate (a fallen oak drum) raises a root-gate.
- **Floor 2, test:** two plates and two drums in a ring of oaks, but every push also wakes a sleeping Dragonair-shaped shadow in the grass (a sight line that resets you to the floor's start if it sees you): the Helm of Darkness hides you while you push.
- **Floor 3, combine:** the stealth stage at the oak (OIKOUMENE §4.3, step 4), with Medea's juniper charm; then the Fleece.
- **Rest:** a spring of Hecate on floor 2. **Payoff:** the Ampharosite and Aries (PG-25). **Boss:** the serpent, a static Pythoros (P-4, Lv 77) if you're seen; it won't wake if you aren't.

**Leuke** (32×28). The temple, the birds, the temple keeper; Achilles and Thetis on the steps (OIKOUMENE §6). A temple stair down into a sea cave with the Nesting Cliffs (the Nursery). A Pearl patch off the north shore (later).

**Pokémon.**
- **Signature:** Ampharos (the Fleece's kind), the dragons of Colchis (Haxorus, Drampa, Kommo-o as the sown men), Unfezant (the Phasis's pheasants: the bird is named for the river), Rotom (Hephaestus's works in Aia), Tinkaton and Klinklang (the Chalybes' forges).
- **Rare behind gates:** Dragonite in the Grove (Augur's Eye); Druddigon on the gorge ledge (the Crook); Tyranitar, Salamence and Hydreigon at the Caucasus (Augur's Eye); Yveltal (LEGENDS, S).
- **Homeland echoes (P-4):** Taurivet (Aietes's bronze bulls, the Khalkotauros line); Dorydrake (the Spartoi, the sown men) rare on the Field of Ares at night; Pythoros (the Fleece's serpent, a static); Pithound at Sinope.
- **Gaps:** none.

**Story.**
- **The land's question: "Was the Golden Fleece real?"** **A witness:** Phrixos's sons, who tell how their father rode the ram. **A place:** the Field of Ares, whose furrows are still there. **An object:** the Fleece, which is an Ampharos's wool. Medea's hall gives the last: she's been sitting under it for years and is bored of it. Alethea writes: *"The Fleece is real. It's wool. The ram was an Ampharos."*
- **Side quests:** the Golden Fleece (OIKOUMENE §4.3, in 1.0 under P-1); the Clashing Rocks; the three furnaces; Aia's four taps; the jar on Sinope's beach; **Achilles at Leuke** (OIKOUMENE §6).
- **The Argo's Road** (P-8), a cross-land quest that starts here. The Argonauts left mooring stones wherever they put in, each carved with the ship. Take a rubbing of each with Alethea's Trowel: Helle's rock (the Hellespont), Phineus's jetty (the Bosporus), the backwater (the Phasis), the shore of Lake Tritonis (Libya, §3.7), Kaldera's Argo mooring (Aethos), and two of ODYSSEY's islands the Argo passed on its way home (Aiaia and Scheria). Seven rubbings, and the shipwright at Kaldera fits the *Euploia* with a beam of Dodona oak like the Argo's, which "spoke" (*Argonautica* 1.524–527). It reads the wind aloud and makes headwinds half as slow (an ODYSSEY §2 upgrade, for its designer to agree).
- **Lore:** the rusted helmets in the furrows; the shed skins; the empty moorings at Aia; the oar with a name burned in it (TIPHYS, the Argo's helmsman, who never reached Colchis: a lie, or an honor).

**Returns and links.**
- **For later:** the Pearl patch off Leuke (a drowned temple of Achilles, Thetis's gift: a Mystic Water and a Lapras static, Lv 74); a Prometheus's Ember altar in Chalybia's cold fourth furnace (Labor 11: a TM and the ironmaster's best gift, a Life Orb); an arrow-stone on the Phasis gorge pointing at the Isle of Ares (Abaris's Arrow; S); the Bag's fog nowhere: the Black Sea is the one land the rim never touches.
- **Links:** the Bosporus from the Troad; LABORS's Themiskyra and the Caucasus on this coast; the sea lane from Leuke to Olbia (the Conch) to Scythia (§3.4); the Argo's Road to Libya and Aethos.

**Bosses.** Medea in Aietes's palace (PERIODOS §4.3, 76–78). Aietes's bronze bulls (a double, 76). The serpent (77, avoidable). Achilles at Leuke (80–82).

### 3.4 Scythia and Hyperborea

> **The fate undone.** The Hyperboreans lived exactly a thousand years, then garlanded themselves and leapt into the sea, content (Pliny 4.89). Now nobody knows when. They're throwing parties about it.

**Identity.**
- **Myth:** Herodotus's fourth book: the nomads in wagons, mare's milk, burial mounds and stone idols, snow the Scythians call "feathers" (4.31), the one-eyed Arimaspians and the gold-guardians, the riddle-gifts the Scythians sent an invading king (4.131); then, past the North Wind, the Hyperboreans, Apollo's people, and Abaris with his golden arrow.
- **Palette and terrain:** straw grass to every edge under a huge sky, felt brown and wagon red, kurgan green; then the white of the feathers and the blue of the Rhipaean ice; then, through the Cave of Boreas, spring green and gold.
- **Signature landmark:** the steppe itself, no trees at all, with kurgans and a stone idol on the skyline; and beyond the ice, the round temple of Apollo among swans.
- ★ **Set piece, "The herd":** on the Steppe Road, a wild herd of Cyclizar thunders across the screen in front of you, twenty sprites in a scripted gallop, and the grass flattens behind them.
- ★ **Set piece, "Through the North Wind":** the Cave of Boreas's last floor is a gale you walk straight into. The screen whites out; then the cave mouth opens on warm green meadow under a sun that doesn't set, and the warmest music in the game starts. The palette change is the moment. This is the Oikoumene's biggest reveal.
- ★ **Vista, "The round temple":** across the Hyperborean meadow, the temple on its rise with swans wheeling round it.

**Maps.** Wild 70–80; behind later gates 78–80.

| Map | Kind | Size | Area | Levels | Tier |
|---|---|---|---|---|---|
| `Olbia` | Port town on the Borysthenes | 44×36 | — | — | 1.0 |
| `Scythia_SteppeRoad` | The great road, with the Wagon Camp as its outcamp | 104×40 | S1, S2 (marsh end) | 70–72 | 1.0 |
| `Scythia_Kurgan` | The chieftain's mound, 2 floors | 24×24 each | S1 (cave slots) | 72–74 | 1.0 |
| `Scythia_ArimaspianHeights` | Mining heights and fossil beds | 48×56 | S4 | 73–75 | 1.0 |
| `Scythia_FeatherWastes` | Snow route ending at the Rhipaean ice walls | 40×90 | S3, S5 | 73–77 | 1.0 |
| `Hyperborea_CaveOfBoreas` | The North Wind's house, 4 floors | 32×32 each | S6 | 76–78 | 1.0 |
| `Abaris` | The Hyperborean village and meadow, with the round temple hall (PERIODOS §4.4) | 56×48 | S7 | 77–80 | 1.0 |
| `Scythia_Maeotis`, the moving camp | Lake route; the camp moving by weekday | — | S2 | 70–72 | S |

**Stops.**

| Stop | Temple, shrine or outcamp | Herm | Hall | Services |
|---|---|---|---|---|
| **Olbia** | **The temple of Apollo the Healer**, the colony's god | A Greek herm on the quay, wrapped in felt against the wind | — | Asclepeion, Agora, the Super Rod |
| **The Wagon Camp** (outcamp, the Steppe Road's midpoint; it moves at S) | **A felt shrine of Tabiti**, the Scythian hearth goddess (Herodotus 4.59): a fire in a wagon | A stone *baba* idol (OIKOUMENE §4) | — | The healer's wagon; the mare-milker |
| **The miners' hut** (outcamp on the Arimaspian Heights) | **A gold-guardians' bone shrine** the Arimaspians keep "to be safe" | A cairn with a gold nugget on top that nobody steals | — | Heal |
| **The last hut** (the Feather Wastes' foot) | **A shrine of Boreas**, a wind-bell on a post | A *baba* idol in snow | — | Heal; a hearth to light your carried flame |
| **Abaris** | **The round temple of Apollo** (Diodorus 2.47) | A golden arrow stuck in a stone | **The round temple:** Abaris | A healer; the swan-keeper's shop |

**New households:**
- **The Wagon Camp, the riddle wagon.** A Scythian elder with a bird, a mouse, a frog and five arrows in a basket: the gifts the Scythians once sent a king who invaded (4.131). Explain them (fly like birds, hide like mice, leap into lakes like frogs, or be shot). Choose right and she gives you the five arrows: a Scope Lens, and the arrows go on the riddle-wagon's wall with your name.
- **Olbia, Anacharsis's house** (OIKOUMENE §4.4) adds the riddle's other half: he asks you what the Scythians meant, and laughs at whatever you say.
- **The miners' hut, the one-eyed foreman.** An Arimaspian, who squints. He has two eyes. He trades his Carbink for your Sableye, and asks you not to tell the Greeks about his other eye.
- **Abaris, the leaping cliff's gardener.** The cliff where Hyperboreans used to leap is a garden now, planted by the thousand-year couple. She gives a daily Lansat or Starf Berry.

**Roads and dungeons.**

**The Steppe Road** (104×40, west to east; the great road). *From Olbia's farms onto the open steppe.*
1. **Olbia's farms:** wheat and a Scythian archer in plain view; **band 1** in the wheat, walled by field banks.
2. **The open steppe:** no trees, only grass and low kurgans. The herd set piece (★). Kurgans are the walls here: the road threads between them, and the archer pair on the saddle between two mounds is the chokepoint.
3. **The Wagon Camp** (outcamp, the midpoint).
4. **The kurgan field:** the chieftain's mound with its shaft (the Kurgan, below), a stone idol in the grass, **band 2** right after a horse racer.
5. **The marsh end** at Lake Maeotis's edge (S2's table): reeds (the Sickle), a ford, and **band 3**, then the road north to the Heights.
- **Checks:** bands 3; mandatory trainers 4; rest: the Wagon Camp; climb: the kurgan shaft; cave: the Kurgan; ledges: the steppe's few rises drop west toward Olbia.

**The Kurgan** (2 floors). *A chieftain's burial mound.* A shaft ladder down from the mound's top (stairs to treasure). Floor 1: the horses' chamber, horses buried with their harness, frozen in the permafrost and perfect (remains, §5.4; the Pazyryk burials, lore only). A drum-on-plate pair opens the timber door. Floor 2: the chieftain's chamber, the gold pectoral (a Gold Bottle Cap) and a ghost table (Banette, the land's Ghost share).

**The Arimaspian Heights** (48×56). *Gold mines in the hills, and the bones the guardians left.* Rock Smash fossil beds (the four Galar fossil halves, OIKOUMENE §8), mine adits with ladders between levels (one ladder up to a gold seam with a Nugget pile), gold-digging Durant and their Heatmor (Herodotus's gold-digging ants), the miners' hut outcamp, and a Crook face to a ledge where the "griffin" skeleton lies: a Protoceratops-like skull that Alethea measures twice (Adrienne Mayor's reading; the chart notes it, OIKOUMENE §5). Never call it a griffin in a name (LAZARUS's avoid-list): the NPCs say "the gold-guardians."

**The Feather Wastes** (40×90, south to north). *Into the snow.* Blizzard weather; snowdrifts that slow you (deep-snow tiles); a frozen river to cross on ice (sliding is Aithiopia's hall verb, so these are short, safe slides of two or three tiles); **bands 1 and 2** in snow grass after two sight lines; the last hut and its hearth; and the **Rhipaean ice walls**, which a flame carried up from Olbia's hearth melts (OIKOUMENE §2; Prometheus's Ember works too, and never goes out). Beyond the walls, the Cave of Boreas's mouth.

**The Cave of Boreas** (4 floors; the land's dungeon). *The North Wind's house: wind-current floors* (OIKOUMENE §4.4).
- **Floor 1, teach:** wind currents push you along corridors. One vent in the floor blows a current; push an ice drum (a drum in the land's skin, §5.1) onto it and the current stops.
- **Floor 2, test:** three vents, two drums: choose which current to stop, because the one you leave carries you to the stair.
- **Floor 3, combine:** drums on vent plates also block the currents that would otherwise blow a drum off its plate. A hall of Boreas with frozen bronze statues of the winds and a frozen spring (rest; Prometheus's Ember thaws it for a Never-Melt Ice, later).
- **Floor 4:** the gale (★ "Through the North Wind"), Kyurem and Glastrier's chambers (LEGENDS) off to the sides.

**Abaris and the Meadow** (56×48). The village of round huts, the round temple (the hall), the swans' lake, the leaping cliff turned garden, the maidens' house (Calyrex's quest, LEGENDS), and a temple roof reached by a ladder inside the temple's dome scaffold, where Apollo's lyre hangs (lore and a Sitrus pile). The Hyperborean Nursery isn't here: the North's young are on the steppe (OIKOUMENE §8).

**Pokémon.**
- **Signature:** Cyclizar (the steppe's horses), Stantler and Wyrdeer, Stonjourner (the Hyperboreans' walking round temple), Swanna, Frosmoth, Avalugg, Cetoddle, Beartic.
- **Rare behind gates:** Absol on the steppe (Augur's Eye); Baxcalibur in the Cave of Boreas (Augur's Eye); Glaceon in the meadow (Augur's Eye); the fossils; Kyurem, Glastrier, Calyrex, Articuno (LEGENDS).
- **Homeland lines (§2.7):** Borapteryx, common in the Cave of Boreas; Chionyad, rare in the Feather Wastes; Hymnaria, on the swans' lake; Krystolos at the ice walls.
- **Gaps:** none. No griffin species, ever (LAZARUS).

**Story.**
- **The land's question: "What's beyond the North Wind?"** **A witness:** Anacharsis: "Nobody's been. We say 'feathers' and stop." **A place:** the Rhipaean ice. **An object:** a swan's feather, found on the snow, that is warm. Abaris's hall gives the last. Alethea writes: *"Beyond the North Wind it's spring. It stays spring."*
- **Side quests:** the riddle wagon; the miners' secret eye; the gold-guardians' bones; the leaping cliff's garden; and OIKOUMENE's Anacharsis, mare-milker, fur trader, schoolmaster, archer chief, barrow-keeper, racer, thousand-year couple, maidens and swan-keeper.
- **Lore:** the frozen horses; the stone idols, each a little different, all facing east; a felt saddle cloth with a gold stag; the warm feather.

**Returns and links.**
- **For later:** Prometheus's Ember thaws the frozen spring in the Cave and the hall of the winds' bronze statues (a Never-Melt Ice and a Borapteryx static, Lv 80); the Helm of Hades opens the Kurgan's sealed second chamber by day (a ghost chieftain's battle, Lv 79, then the Scythian bow, a Wide Lens); and **Abaris's Arrow is won here**: once you have it, the Hyperborean meadow's own arrow-stone flies you to an islet on the swans' lake (a Lapras static, Lv 78).
- **Links:** the sea lane from Leuke (§3.3); the Wagon Camp's racers mention Kyrene's chariots (§3.7); the Hyperborean maidens' offerings went to Delos (Herodotus 4.33), and the swan-keeper asks if anyone in Aethos still remembers them.

**Bosses.** Abaris in the round temple (PERIODOS §4.4, 80–82). The ghost chieftain (79, later). The Wagon Camp's archer chief (78).

### 3.5 Egypt and the Nile

> **The fate undone.** The Phoenix comes to Heliopolis every five hundred years, on schedule. The schedule's gone. The priests keep the altar swept anyway.

**Identity.**
- **Myth:** Herodotus's second book, which Egypt fills: the Nile and its flood, the pyramids, Proteus of Memphis and Helen, the singing colossus, the sacred animals, the Phoenix, the labyrinth by Lake Moeris.
- **Palette and terrain:** black mud and green papyrus taller than the player, white limestone, gold desert edge; tombs inside in ochre, malachite and lapis. Two worlds a few steps apart: the green strip and the desert.
- **Signature landmark:** the three pyramids on the plateau's edge, seen across the river.
- ★ **Vista, "The pyramids from the river":** on the Nile lane, the west bank opens and three pyramids stand on the desert's edge, each a set piece many tiles wide. The camera stops.
- ★ **Set piece, "The Nile rises":** the Nilometer's keeper at Elephantine reads the flood (OIKOUMENE §4.5). In two of the Aethos year's twelve months, the Delta Reeds switch to their **flood layout**: the canals spill, new water opens to surf, gnat-towers stand in a lake, and the table changes. The first time, it's a scene: the water rises across the screen.
- ★ **Set piece, "The singing stone":** at Hekatompylos at dawn, the colossus of Memnon sings (OIKOUMENE §4.5).

**Maps.** Wild 60–67; behind later gates 67–70.

| Map | Kind | Size | Area | Levels | Tier |
|---|---|---|---|---|---|
| `Naukratis` | Port town and the Oikoumene's hub | 52×44 | — | — | 1.0 |
| `Egypt_DeltaReeds` | The great road: Pharos's beach to Memphis, with a flood layout | 104×40 | Y1, Y7 | 60–63 | 1.0 |
| `Memphis` | City, with Proteus's precinct hall (PERIODOS §4.5) and Heliopolis's sun temple as its north quarter | 60×48 | — | — | 1.0 |
| `Egypt_PyramidField` | Desert route on the plateau, ending at Lake Moeris | 56×56 | Y3, Y5 | 62–65 | 1.0 |
| `Egypt_GreatPyramid` | The land's dungeon, 3 floors (a 4th S) | 32×32 each | Y4, Y8 | 63–67 | 1.0 |
| `Egypt_Nile` | River lane, Memphis to Hekatompylos | 24×100 | Y2 | 61–63 | 1.0 |
| `Hekatompylos` | Thebes of the hundred gates, the river, and the west bank's Valley of Tombs | 64×48 | Y6 | 64–66 | 1.0 |
| `Elephantine` | Island village and the First Cataract | 40×36 | Y9 | 65–67 | 1.0 |
| `Egypt_LabyrinthOfMoeris` | Herodotus's labyrinth | — | Y8 | 65–67 | S. At 1.0 Y8 rides on the Great Pyramid's upper floors |

**Stops.**

| Stop | Temple, shrine or outcamp | Herm | Hall | Services |
|---|---|---|---|---|
| **Naukratis** | **The Hellenion**, the Greek traders' shared temple | An ibis-headed pillar of Thoth (OIKOUMENE §4) at the quay | — | Asclepeion, Agora, Daphne's field station, the egg-ovens, the incense merchant, the Super Rod |
| **The gnat-tower village** (outcamp, the Delta Reeds' midpoint) | **A shrine of Wadjet**, the cobra of the delta, on a reed island | An ibis pillar | — | A healer who sleeps up a tower; nets (Herodotus 2.95) |
| **Memphis** | **The temple of Ptah**, the city's god, and the temple of the Stranger | An ibis pillar at the river gate | **The precinct of Proteus:** Pharaoh Proteus; Helen as his guest | Asclepeion, Agora |
| **The Moeris landing** (the Pyramid Field's far end) | **The crocodile shrine of Sobek** with its earringed crocodiles (Herodotus 2.69) | An ibis pillar | — | A healer; the lake ferry |
| **Hekatompylos** | **The great temple of Amun**, its hypostyle hall | An ibis pillar at the east-bank landing | — | Asclepeion, Agora |
| **Elephantine** | **The temple of Khnum**, the potter god of the cataract | An ibis pillar by the Nilometer | — | A healer |

**New households:**
- **The gnat-tower village, the tower family.** Three generations who sleep up a tower above the gnats. A ladder inside climbs to the sleeping platform (stairs to treasure: a Silk Scarf and a view across the reeds). In flood months, the tower's base is underwater, and their boat takes you to a reed island with a Mystic Water.
- **Memphis, the sun-boat keeper.** By the pyramids, a king's ship was buried in a pit, taken apart (the Khufu ship, lore). Dig its planks out of the Pyramid Field with the Trowel (six dig spots); he reassembles it. Reward: the boat sails you once a day from Memphis to Hekatompylos and back, and a Sun Stone.
- **Hekatompylos, the tomb painter's widow.** Her husband died with his last tomb half-painted, grid lines still showing (remains). Choose colors for the rest of the scene (the tomb-painters' minigame, OIKOUMENE §4.5) and she gives his brushes: a Smeargle that knows Sketch twice.
- **Elephantine, the Nilometer's keeper** (OIKOUMENE §4.5) now also runs the flood: he tells you which months the river rises.

**Roads and dungeons.**

**The Delta Reeds** (104×40, west to east; the great road). *From Pharos's beach through the papyrus to the apex of the delta at Memphis.*
1. **Pharos's beach:** the seal-herd on the island across a channel (the Conch; Ditto among them, Popplio's line wild), a Nile boatman in plain view, **band 1** in the dune grass.
2. **The papyrus maze:** papyrus walls the player can't see over, with Sickle cuts as shortcuts; a hippo pool (Hippowdon) and a fisher pair on the only causeway (a chokepoint).
3. **The gnat-tower village** (outcamp, the midpoint).
4. **The canals:** **band 2** on a reed island after a scribe's riddle-battle, a lock gate on a canal (a drum-on-plate puzzle opens it: §5.1), an egret rookery.
5. **The fields:** black earth, irrigation shadufs, **band 3** in a flax field, a farmer on the field dike, and Memphis's white walls.
- **Flood months:** the same map with the canals overflowing: new surf lanes, the gnat-towers in a lake, a flood table of water species, and two islands that are only reachable then (a Big Pearl, and a Barboach-and-Whiscash fishing hole).
- **Checks:** bands 3; mandatory trainers 5; rest: the gnat-tower village; climb: the towers; cave: none, but the canal lock's underpass is covered; ledges: dike edges drop west.

**Memphis** (60×48). The white walls, the temple of Ptah and the Apis stall, Proteus's precinct with the Tyrians' Camp and the temple of the Stranger, and Heliopolis's sun temple and obelisks in the north quarter (the sun-priest, the Phoenix's altar; LEGENDS). A temple pylon has a stair inside to its roof (stairs to treasure: a Choice Specs where the priests watched the sky). Households: OIKOUMENE §4.5.

**The Pyramid Field** (56×56). *The plateau of the pyramids, west of the river.* The vista from the edge (★ "The pyramids" is the river's; this map has the climb up the causeway). Dunes, a scarab rolling the sun across the sand (a moving Rabsca object you can follow to a hidden Revive), the **Great Sphinx**, half buried, with an Enigmaw static at its paws (Lv 66, the homeland line's showpiece), the sun-boat's pits (dig spots), and the causeway south to Lake Moeris and its crocodile shrine.

**The Great Pyramid** (3 floors; the land's dungeon). *Herodotus says the Nile was led into a chamber under it* (2.124).
- **Floor 1, teach:** the descending passage and the first **portcullis slab**: a granite block (a drum in the land's skin) onto a plate raises it.
- **Floor 2, test:** the Grand Gallery, a long ramp, with three portcullises and two blocks; ladders up the air shafts to side chambers (stairs to treasure: a Rare Candy, a Twisted Spoon).
- **Floor 3, combine:** the flooded chamber. Plates also work the Nile channel's sluice: drain it to roll a block, flood it to surf to the island with the king's sarcophagus. Unown in the walls (the scribe's riddles, OIKOUMENE §4.5, point to them).
- **Floor 4 (S):** the Labyrinth of Moeris's twelve courts, or Y8's table on floor 2 at 1.0.
- **Rest:** a well on floor 2. **Boss:** the pyramid's keeper (a Cofagrigus-led tomb guardian, Lv 75). **Payoff:** a TM and Unown's chambers.

**The Nile** (24×100). A river lane: boats, crocodiles basking on sandbars, hippos, papyrus banks, and the pyramid vista (★). A Pearl patch at a sunken temple's columns (later).

**Hekatompylos and the Valley of Tombs** (64×48). East bank: the city's gates, the temple of Amun, the colossus (★ at dawn). The river between, with a ferry. West bank: the Valley of Tombs at night, painted tomb doors in a cliff, jackals, a workers' village left empty when the tomb was done (remains). One tomb is open (a single room, the painter's widow's half-finished wall). One is a **shadow door** (the Helm of Hades, later).

**Elephantine** (40×36). The island, the Nilometer stair down to the river (stairs to treasure: a Damp Rock on the lowest mark), the temple of Khnum, and the cataract's foot, where the Horn climbs the rapids into Aithiopia.

**Pokémon.**
- **Signature:** Hippowdon, Krookodile and Skeledirge (Moeris's crocodiles), Sigilyph, Cofagrigus, Unown, Rabsca (the scarab), Persian and Purugly (Bubastis's cats).
- **Rare behind gates:** Lucario and Mabosstiff in the Pyramid (Augur's Eye); Houndstone in the Valley (Augur's Eye); Espeon on the pyramid's upper floor (Augur's Eye); flood-month islands (Whiscash, Barboach); Ho-Oh, Reshiram, Zygarde, Buzzwole and Kartana (§15; Uxie moves to Lebadeia under P-20).
- **Homeland lines (§2.7):** Enigmaw at the Sphinx (static, Lv 66) and wild on the Pyramid Field; Ophidrop and Panacoil, the uraeus cobras, in the Valley of Tombs at night.
- **Gaps:** **the sacred ibis** of Thoth. No species is an ibis; the herms carry the bird. A new species is optional (§8, P-11); nothing waits on it.

**Story.**
- **The land's question: "Was Helen at Troy?"** Herodotus asked it first (2.113–120). **A witness:** Helen herself. **A place:** the temple of the Stranger, where she's sat for years. **An object:** the treasure Paris took from Sparta, which Proteus kept in his storehouse. Proteus's hall gives the last. Alethea writes: *"Helen sat out the war in Memphis. Troy got a phantom."*
- **Side quests:** the sun-boat; the flood islands; the painter's widow; the tower family; and OIKOUMENE's egg-ovens, the true Apis, the scribe's riddles, the embalmer, the obelisk tutor, the thief's family, the colossus, the ivory-carver.
- **Lore:** the workers' village; the half-painted tomb; the empty Phoenix altar, swept; the sun-boat planks.

**Returns and links.**
- **For later:** the Valley's shadow door (the Helm of Hades: a king's tomb with a sealed sarcophagus room and a Spiritomb static, Lv 70); the sunken temple in the Nile (the Pearl: a Relicanth and a Prism Scale); the Mirror of Truth on the temple of the Stranger's wall, which shows the phantom (a link to the Troad's phantom on the Skaian tower); an arrow-stone on the Great Pyramid's top (reached by its outer stair) pointing at a second pyramid's capstone (Abaris's Arrow: a Sigilyph static, Lv 70, and a Star Piece).
- **Links:** Naukratis is the hub: Daphne's fossils from every land come here. **Helen and Menelaus** (§3.10): Menelaus waits on the Isles; carry a letter (she writes "Not yet. Nobody knows when, now."). The cataract to Aithiopia; the ravens' road to Libya; the Nile's sources at the Mountains of the Moon (§3.6).

**Bosses.** Pharaoh Proteus (PERIODOS §4.5, 74–76). Helen (74–76, optional). The pyramid's keeper (75).

### 3.6 Aithiopia and the Sunrise

> **The fate undone.** Memnon, son of the Dawn, has heard the song in which he dies at Troy. He has never been to Troy. He's thinking of going, just to see.

**Identity.**
- **Myth:** the "blameless" Aithiopians, with whom the gods feast (*Iliad* 1.423); Herodotus's long-lived Aithiopians, their gold fetters, their Table of the Sun and their unbent bow (3.17–25); Memnon and his mother Eos; the Pygmies and the cranes; the sun rising out of Okeanos; Andromeda, daughter of the Aithiopian king Kepheus, chained for the sea monster.
- **Palette and terrain:** red earth, acacia and baobab, savannah gold, steep small pyramids, jungle green in the Mountains of the Moon, and at the east edge Okeanos turning pink.
- **Signature landmark:** the pyramids of Meroë, dozens of them in rows on a ridge, steeper and smaller than Egypt's.
- ★ **Set piece, "The sunrise":** on the stable roof at the Gate of Dawn before first light, Eos opens the gates, and Helios's chariot rises out of Okeanos: the map's palette sweeps from violet to gold, tile row by tile row, as the music climbs. The Oikoumene's most beautiful moment.
- ★ **Vista, "Meroë's pyramids":** the road tops the ridge and the rows of pyramids fill the screen.
- ★ **Set piece, "The cranes":** at the Pygmy Marshes the sky darkens with cranes (shadow sprites sweep across), and you hold the reed line with the Pygmies, three battles in a row (OIKOUMENE §4.6).

**Maps.** Wild 70–76; behind later gates 76–79.

| Map | Kind | Size | Area | Levels | Tier |
|---|---|---|---|---|---|
| `Aithiopia_Cataracts` | River lane up the cataracts from Elephantine (the Horn) | 24×80 | A1 | 70–72 | 1.0 |
| `Meroe` | City, with Memnon's bath-court hall (PERIODOS §4.6) | 52×44 | — | — | 1.0 |
| `Aithiopia_TableOfTheSun` | The great road: savannah, with the Fountain of the Long-Lived as its outcamp | 104×40 | A2, A3 | 71–74 | 1.0 |
| `Aithiopia_Nysa` | Mountain climb to Dionysus's nursery | 36×80 | A4 | 72–74 | 1.0 |
| `Aithiopia_CaveOfNysa` | The land's dungeon, 2 floors (3rd S) | 30×30 each | A4 (cave slots) | 73–75 | 1.0 |
| `Aithiopia_MountainsOfTheMoon` | Jungle route with the Pygmy Marshes at its east end | 96×44 | A5, A6 | 72–75 | 1.0 |
| `Aithiopia_GateOfDawn` | Eos's palace, Helios's stables and the Okeanos shore with Andromeda's rock | 56×40 | A7 | 74–76 | 1.0 |

**Stops.**

| Stop | Temple, shrine or outcamp | Herm | Hall | Services |
|---|---|---|---|---|
| **The cataract landing** (top of the cataracts) | **A shrine of the Nile**, river votives on a rock | A lion-headed pillar of Apedemak, Meroë's god | — | A healer |
| **Meroë** | **The Lion Temple** of Apedemak | A lion-headed pillar at the gate | **The bath-court:** King Memnon | Asclepeion, the fetter-smith's reversed-price shop, Agora |
| **The Fountain of the Long-Lived** (outcamp, the Table's midpoint) | **The elders' spring shrine**, violet-scented (Herodotus 3.23) | A lion pillar | — | The elders heal you; a bath that fully restores PP |
| **The nymphs' hut** (outcamp on Nysa) | **Dionysus's cradle shrine** | A pillar wrapped in ivy | — | Heal; the nymph's daily Berry Juice |
| **The Pygmy village** (the Mountains of the Moon's east end) | **A crane-feather shrine** to their dead | A short pillar, Pygmy-height, which the player has to crouch to read | — | A healer |
| **The Gate of Dawn** | **Eos's palace** and **Helios's stables** | A golden pillar | — | A healer; Lampetie's daily Sun Stone |

**New households:**
- **The cataract landing, the spies' camp** (remains). Herodotus's Fish-Eaters, spies for a Persian king, brought gifts the Aithiopian king refused: a purple cloak, a gold necklace, myrrh and palm wine (3.20–22). Their camp is abandoned on a rock above the falls, the gifts still in their baskets. Return each to the right person in Meroë (a cloak to the dyer, myrrh to the priest, and so on) for a Choice item each time it's refused again.
- **Meroë, the bow-keeper.** Keeps the unbent bow the king sent back. Draw it (the archers' minigame, OIKOUMENE §4.6) at full strength and she gives you a Power Anklet.
- **The Pygmy village, the shieldmaker.** Makes crane-feather shields and needs feathers: Flamigo drops them after battle. Ten feathers: a Razor Claw and a Pygmy-size shield for your room.

**Roads and dungeons.**

**The Cataracts** (24×80). The Horn climbs six cataracts, each a waterfall with an eddy at its foot; rocks and rapids between them push you; a Pearl patch at a drowned shrine (later).

**The Table of the Sun** (104×40, west to east; the great road). *Savannah from the river to Meroë and on toward the dawn.*
1. **The riverside:** baobabs, a herder in plain view, **band 1** in long savannah grass between thorn bushes.
2. **The Table** itself: a meadow where cooked meat appears every night (Herodotus 3.18). By day it's a meadow with tables; by night it's laid out and wild Pokémon come to eat (a night-only table with rarer visitors, Kangaskhan on the very rare slot).
3. **A hollow baobab:** a ladder inside to its crown (stairs to treasure: a Leftovers in an old nest).
4. **The Fountain of the Long-Lived** (outcamp, the midpoint).
5. **The grassland:** **band 2** after an Ethiopian archer pair on the only gap through an acacia line (a chokepoint); Zebstrika herds.
6. **The ridge and Meroë's pyramids** (★); **band 3** at the ridge foot after a Pygmy warrior; the city gate.
- **Checks:** bands 3; mandatory trainers 5; rest: the Fountain; climb: the baobab and the ridge stair; cave: a dry riverbank cave with Rhydon (Rock Smash pocket); ledges drop west.

**Mount Nysa** (36×80, a climb). Dionysus's nursery mountain: ivy walls (Dionysus's Thyrsus if the player has it, SYSTEMS §3; otherwise the Sickle), vine-wrapped switchbacks, the nymphs' hut outcamp, Oinopard in the trees, and the cave mouth.

**The Cave of Nysa** (2 floors; the land's dungeon). *Where the nymphs hid the infant Dionysus.* Floor 1: a wine spring that flows when you set three amphorae (drums in the land's skin, §5.1) on their plates by the press; the spring fills a basin you can surf to a ledge. Floor 2: the cradle grotto, ivy curtains, a Crook face up to a crystal niche where Diancie's crown-stone was found, now empty: a note says it went home to Ariadne (Diancie moves to Kalliste, P-20; the niche holds a Shiny Stone). Rest: a spring of water on floor 1. Payoff: a TM and a Thyrsivy static (Lv 75).

**The Mountains of the Moon** (96×44). Jungle, rain every day (Sliggoo evolves here), vine bridges, a waterfall with a cave behind (the Horn), the Nile's sources ("between two mountains," a priest's tall tale, Herodotus 2.28), and at the east end the Pygmy Marshes and their village, where the cranes' battle (★) plays.

**The Gate of Dawn** (56×40). Eos's palace, Tithonus (Genesect, LEGENDS), Helios's stables and their roof (★ "The sunrise", reached by a ladder in the hayloft), and the Okeanos shore. **Andromeda's rock** stands in the surf: broken chains on a black rock, and a Kynoketos static in the water below it (Lv 79, "the Ketos": a boss battle). The dawn fog off the shore parts with Aeolus's Bag, onto Okeanos (§2.1).

**Pokémon.**
- **Signature:** Zebstrika, Girafarig, Tropius, Toucannon, Passimian and Oranguru, Chansey and Audino (the long-lived), Flamigo and Bombirdier (the cranes), Volcarona.
- **Rare behind gates:** Kecleon and Sliggoo in the jungle (Augur's Eye); Flareon at the Gate (Augur's Eye); Kangaskhan at the Table by night; the Ketos (a static); Solgaleo, Genesect, Zarude, Landorus, Virizion, Ting-Lu, Guzzlord and Pheromosa (§15).
- **Homeland lines (§2.7):** Kynoketos at Andromeda's rock; Oinopard and Thyrsivy on Nysa; Elektear at the Gate of Dawn.
- **Gaps:** none.

**Story.**
- **The land's question: "Where does the sun rise?"** **A witness:** Lampetie, who grooms the horses. **A place:** the stable roof. **An object:** a Sun Stone, still warm. Memnon's hall gives the last. Alethea writes: *"The sun rises out of the sea east of Meroë. We watched it come up."*
- **Side quests:** the spies' gifts; the unbent bow; the crane feathers; **Memnon visits Troy** (after the Emblem: escort him by ship to Sestos and up to the Skaian Gate, §3.1; reward: Memnon's sword, a Black Belt, and a line between two men who've heard their own deaths sung: "Did you die?" "Not yet." "Me neither."); and OIKOUMENE's fetter-smith, elders, archers and crane-wardens.
- **Lore:** Andromeda's broken chains; the spies' camp; the pyramids' chapels with a king's name on each and one chapel with none.

**Returns and links.**
- **For later:** the Bag's dawn fog onto Okeanos; the drowned shrine in the cataracts (the Pearl: a Bruxish static and a Mystic Water); an arrow-stone on Meroë's ridge pointing at the biggest pyramid's top (Abaris's Arrow: the king's capstone room, a Gold Bottle Cap); Prometheus's Ember lights Helios's cold spare torch in the stable, and Lampetie lets you ride a horse along the shore once a day (a Rapidash run, cosmetic).
- **Links:** Elephantine (§3.5); Troy (Memnon); Okeanos (the dawn fog); Helios's cup ties this shore to LABORS's Labor 10 and ODYSSEY's Thrinakia (Lampetie complains about both).

**Bosses.** King Memnon (PERIODOS §4.6, 78–80). The Ketos (79). The Pygmy chief after the cranes (77).

### 3.7 Libya

> **The fate undone.** Zeus Ammon's oracle in the oasis answered kings for a thousand years. It has nothing to say, and its priests have taken up reading the weather.

**Identity.**
- **Myth:** Herodotus's Libya (4.168–199): Kyrene, founded from Thera; silphium; the oasis of Ammon and its Spring of the Sun; the salt hills; the Garamantes; the Psylli, who marched against the south wind; Antaeus; and the Argonauts, who carried their ship across the desert to Lake Tritonis (*Argonautica* 4.1381–1392).
- **Palette and terrain:** Kyrene's green plateau and white limestone; the Sand Sea's gold dunes; salt-white ridges; date-palm green at the oases; the yellow desert glass.
- **Signature landmark:** the oasis of Ammon, green in the gold, with the oracle's temple on its rock.
- ★ **Vista, "The oasis":** following the ravens over the last dune, the camera lifts over Ammonion: the palms, the oracle's rock, the Spring of the Sun steaming.
- ★ **Set piece, "The south wind":** in the Sand Sea a sandstorm comes up; the screen browns, the dunes shift (the maze's daily layout changes on the spot), and when it clears a new dune shows a line of spear tips: the Psylli, who marched against the wind and were buried by it (Herodotus 4.173).
- ★ **Vista, "The glass":** the Glass Crater's floor, yellow glass glittering in animated light.

**Maps.** Wild 63–70; behind later gates 70–73.

| Map | Kind | Size | Area | Levels | Tier |
|---|---|---|---|---|---|
| `Kyrene` | Town on its plateau, with the harbor (Apollonia) below and the hippodrome hall (PERIODOS §4.7) | 56×52 | — | — | 1.0 |
| `Libya_SilphiumPlateau` | Route from Kyrene to the desert's edge, with Antaeus's Ring | 80×36 | B1, B8 | 64–67 | 1.0 |
| `Libya_SandSea` | The great road: a dune maze in three daily layouts, with the salt ridge | 3 × 80×60 | B2, B5 | 66–68 | 1.0 |
| `Libya_GaramantesTunnels` | Underground channels, 2 floors (3rd S) | 32×28 each | B6 | 67–69 | 1.0 |
| `Ammonion` | The oasis town | 48×44 | — | — | 1.0 |
| `Libya_GlassCrater` | Crater dungeon, 2 floors (3rd S) | 28×28 each | B7 | 68–70 | 1.0 |
| `Libya_Tritonis` | Lake Tritonis, its village and the Syrtis shore | 72×44 | B3, B4 | 65–67 | 1.0 |

**Stops.**

| Stop | Temple, shrine or outcamp | Herm | Hall | Services |
|---|---|---|---|---|
| **Kyrene** | **Apollo's sanctuary and spring** | A ram-horned cairn of Ammon at the harbor stair's head | **The hippodrome:** Kyrene | Asclepeion, Agora, the Super Rod at the harbor |
| **Antaeus's Ring** (outcamp, the plateau's midpoint) | **Antaeus's tomb mound**, a shrine to the wrestler | A ram cairn | — | A wrestlers' healer |
| **The salt well** (outcamp in the Sand Sea, at the salt ridge) | **A spring shrine**, one of Herodotus's springs "every ten days' journey" (4.181) | A ram cairn | — | Heal; water for the road |
| **Ammonion** | **The oracle of Zeus Ammon** on its rock | A ram cairn at the palm gate | — | Asclepeion, Agora, the raven-keeper |
| **Tritonis** | **Triton's lakeshore shrine** | A ram cairn on the shore | — | A healer |

**New households:**
- **Antaeus's Ring, the grandson.** Antaeus drew his strength from the earth. His grandson does too, and won't battle you unless you stand on sand. Win the Ring's gauntlet and he gives his Geogrip (§2.7).
- **The salt well, the salt-cutter.** Herodotus's Libyans built houses of salt blocks (4.185). His salt house is the outcamp's one building. Trade him your Garganacl for his "salt-cured" Klawf, and he gives a daily Hard Stone, "salt from the deep seam."
- **Tritonis, Mopsos's grave-tender.** The Argonauts' seer died here of a snakebite (*Argonautica* 4.1502–1536), and the Psylli's snake-charmer tends his grave (remains). Her snake-charmer trade (OIKOUMENE §4.7) gives Black Sludge.

**Roads and dungeons.**

**The Silphium Plateau** (80×36). Kyrene's last fields of silphium (the berry-planting puzzle, OIKOUMENE §4.7), fennec dens in the stones (Delphox's line, PG-5), **two bands**, a charioteer pair on the plateau road (a chokepoint), Antaeus's Ring (a gauntlet of Fighting trainers, the midpoint outcamp), and the escarpment's cut stair down to the desert.

**The Sand Sea** (three 80×60 layouts; the great road). *Cambyses lost an army here (Herodotus 3.26). The dunes move.*
1. **Layouts:** three dune layouts, one per day in rotation (OIKOUMENE §10's Medium item). The raven-keeper's ravens (a key item from Ammonion; from Kyrene's side, the first crossing has a raven sent to meet you) perch on the right dune crests; follow them.
2. **Every layout** keeps the same anchors so the player can learn the land: the salt ridge (B5, the salt well outcamp), the Garamantes' tunnel mouth, the buried Psylli's spear line (after the storm ★), and the oasis's edge.
3. **Bands:** each layout has two forced bands in the dune grass, and its mandatory trainers stand on the ridges the ravens lead over: Garamantian drivers, whose chariots block the crest.
4. **Remains:** half-buried bronze and bones of an army that walked into a sandstorm: a Persian helmet, a standard; and the spear tips. A shadow door in a buried fort (later).
- **Checks:** bands 2 per layout; mandatory trainers 4 per layout; rest: the salt well; climb: dune crests are one-way slides down (ledges) toward Kyrene, and a cut stair up the salt ridge; cave: the tunnels.

**The Garamantes' Tunnels** (2 floors). *The underground channels that carried water to the oases.* Floor 1: water in narrow channels you surf; a well shaft with a ladder up to the desert (a shortcut and a jar). Floor 2: **the plate puzzle**: three sluices, each held open by a drum on its plate (drums in the land's skin, §5.1), route water to three dry channels; fill the right two and the third dries so you can walk it. Toedscruel in the dark; the backward-grazing cattle's painted wall (Herodotus 4.183, lore).

**Ammonion** (48×44). The oasis's palms, the oracle's rock with a stair to the top (stairs to treasure: the oracle's empty seat and a Lagging Tail the priests left behind, "Someone always comes late"), the Spring of the Sun (warm at midnight, cold at noon: drink it at midnight for a full heal and a daily Heat Rock), the raven-keeper, the date-farmer (OIKOUMENE §4.7), and the Nursery of the oasis gardens.

**The Glass Crater** (2 floors). Yellow glass underfoot (★), glass rubble (the Hammer), heat that drains your party a little each step on floor 2 unless you walk in shade (a shade puzzle: the Helm of Darkness doesn't help here; the Atarantes' trick does, §3.8). Eternatus's chamber at S (LEGENDS).

**Lake Tritonis and the Syrtis shore** (72×44). The lake, its village and Triton's shrine; **the Argo's keel grooves** across the sand from the Syrtis shore to the lake (remains: walk them, twelve days' carrying in fifty steps); Mopsos's grave; the shoals where the Argo ran aground; wild lotus on the shore; and the Argo's mooring stone (the Argo's Road, §3.3).

**Pokémon.**
- **Signature:** Flygon, Sandaconda, Garganacl (the salt hills), Mandibuzz, Cacturne, Hariyama and Throh and Sawk (Antaeus's Ring), Delphox (the fennecs).
- **Rare behind gates:** Garchomp, Jolteon and Orthworm in the Sand Sea (Augur's Eye); Glimmora in the crater; Eternatus, Thundurus, Terrakion, Mesprit (LEGENDS).
- **Homeland lines (§2.7):** Geogrip at Antaeus's Ring; Stachypter in Kyrene's grain fields.
- **Gaps:** **silphium**, Kyrene's lost plant and its coin emblem, has no Pokémon. Optional (P-11); the silphium field uses Arboliva and Eldegoss meanwhile.

**Story.**
- **The land's question: "Did the Argonauts carry their ship across Libya?"** **A witness:** Triton's devotee. **A place:** Mopsos's grave. **An object:** the keel grooves. Kyrene's hall gives the last: her chariots race on the same track the Argonauts' shoulders wore. Alethea writes: *"They carried it twelve days. The grooves are still there."*
- **Side quests:** the silphium field; the Ring's gauntlet; the salt house; Mopsos's grave; the Spring of the Sun at midnight; the Argo's Road stone; and OIKOUMENE's charioteer, Ammon's priests, raven-keeper, date-farmer and Triton's clod of earth.
- **Lore:** the buried army; the spear line; the backward cattle; the salt houses.

**Returns and links.**
- **For later:** the buried fort's shadow door (the Helm of Hades: a Persian officer's tent under the sand, a Sandaconda static, Lv 72, and a lead toward Xurkitree in LEGENDS); Lake Tritonis's deep middle (the Pearl: Triton's clod of earth's twin, a Drednaw static, Lv 72); an arrow-stone on the salt ridge pointing at a dune-locked oasis (Abaris's Arrow: a palm grove with a Tropius and a Leaf Stone).
- **Links:** Kyrene's harbor by sea from Kaldera (P-2); the ravens' road to Egypt; the Argo's Road; Atlas's range is visible on Libya's western horizon (§3.8).

**Bosses.** Kyrene in the hippodrome (PERIODOS §4.7, 75–77). The Ring's gauntlet (74–76). The Psylli's chief, a shade on the spear dune at night (76, optional).

### 3.8 The Far West: Atlas, Tartessos and the Pillars

> **The fate undone.** Atlas holds up the sky for ever. He'd like to know if "for ever" still means anything.

**Identity.**
- **Myth:** the west where the sun sets: Herakles's Pillars (LABORS); Phoenician Gadeira and its tides, which amazed Greeks used to a sea without them; Tartessos's silver and King Arganthonios, who lived 120 years (Herodotus 1.163); Kolaios of Samos, blown past the Pillars to Tartessos and home rich (4.152); the Atlas range, "the pillar of heaven," and the Atarantes with no names (4.184).
- **Palette and terrain:** sunset red on everything, silver and slate in the mines, deep green scrub, then the Atlas's cold blue heights. LABORS's far-west tileset is the land's.
- **Signature landmark:** the Atlas Range, where the sky's underside sags low enough to touch.
- ★ **Vista, "Under the sky":** the Atlas Range's summit floor has a ceiling of stars just over the player's head (a top-layer star field over the walkable ground), at noon. Jirachi waits under it (LEGENDS).
- ★ **Set piece, "The tide":** at Gadeira the sea goes out (a tide layout swap by the clock), and a causeway appears to an islet with the temple of Kronos; the well in the Herakleion rises as the tide falls (Strabo 3.5.7).
- ★ **Set piece, "The sky sags":** in the Atlas Range, a floor where the sky's underside presses down; prop it with drums on the pillar sockets (§5.1) and it lifts enough to pass.

**Maps.** Wild 70–78; behind later gates 78–80. LABORS's Strait of the Pillars, Erytheia, the Garden and Atlas's Ridge sit inside it.

| Map | Kind | Size | Area | Levels | Tier |
|---|---|---|---|---|---|
| `FarWest_StraitWaters` | Sea lane through the Pillars (LABORS's map sits on it) | 32×64 | W1 | 70–72 | 1.0 |
| `Gadeira` | Port island town, with a tide layout | 48×44 | — | — | 1.0 |
| `FarWest_AtlanticShore` | Tide-flat route, Gadeira to Tartessos | 96×36 | W2 | 72–74 | 1.0 |
| `Tartessos` | Silver town, with the mine-gallery hall (PERIODOS §4.8) | 52×44 | — | — | 1.0 |
| `FarWest_SilverMines` | Mines, 2 floors (3rd S) | 32×32 each | W6 | 73–75 | 1.0 |
| `FarWest_AtlasFoothills` | The great road: from the Strait's south shore up to the range, with the Atarantes' village | 40×104 | W3 | 74–76 | 1.0 |
| `FarWest_AtlasRange` | Peak dungeon, 3 floors and the summit (5 floors S) | 32×32 each | W4 | 75–78 | 1.0 |

**Stops.**

| Stop | Temple, shrine or outcamp | Herm | Hall | Services |
|---|---|---|---|---|
| **Gadeira** | **The Herakleion** with its two bronze pillars; the **temple of Kronos** on the tidal islet | A Phoenician standing stone of Melqart (Herakles's Phoenician twin) at the quay | — | Asclepeion, the Phoenician traders' market (OIKOUMENE §4.8), the Super Rod |
| **The salt pans** (outcamp, the Atlantic Shore's midpoint) | **A shrine of the Tide**, a stone that's dry at low water and drowned at high | A standing stone | — | Heal; the tide table |
| **Tartessos** | **The temple of the silver**, with a lamp that's never let go out | A standing stone wrapped in silver wire | **The royal gallery:** King Arganthonios | Asclepeion, Agora |
| **The Atarantes** (outcamp, the Foothills' midpoint) | **The cursing cliff**, where they curse the sun at noon (Herodotus 4.184): their shrine, of a kind | A standing stone with every name scratched off | — | Heal in the shade |
| **The sky camp** (the Range's floor 2, a dungeon rest) | **A shrine to Atlas**, with offerings of sweat-salt | — (a cave camp) | — | Heal |

**New households:**
- **Gadeira, Kolaios's descendant.** Kolaios of Samos made a fortune here and gave a tenth to Hera as a bronze krater on three kneeling figures (Herodotus 4.152). His great-grandson keeps the krater's twin and tells the story. Once you've made any rite at a Hera altar in Aethos (SYSTEMS §3), he gives you the twin as a decoration, and a Lucky Egg.
- **Tartessos, the lost miners' families.** A gallery collapsed with its crew inside (remains). Find their three lamps in the mines and bring them back. Reward: a Metal Alloy, a Life Orb, and the families' song.
- **The Atarantes, the nameless child.** Asks you to give her a name, then gives it back: "We don't keep them." She gives you a Shed Shell and the name's in the trainer card's notes.

**Roads and dungeons.**

**The Strait Waters** (32×64). The current through LABORS's Pillars, NE PLUS ULTRA on both headlands, a whirlpool cove (Triton's Conch), and the ocean fog west of the Pillars (the Bag, onto Okeanos).

**The Atlantic Shore** (96×36). *Tide flats under the sunset.* A tide layout by the clock: at low tide the flats open (a shorter path, tide pools with the Gadeira Nursery's young, and Barbaracle on the rocks); at high tide you surf. **Two bands** in the dune grass, a Phoenician trader pair on the causeway (a chokepoint), the salt-pans outcamp, **Kolaios's wreck** at the tide line (a sealed jar at low tide; remains), and Tartessos's silver gate.

**The Silver Mines** (2 floors). Ore carts on rails: **the plate puzzle**: carts (drums in the mine's skin, §5.1) pushed onto hoist plates lift cages to the next gallery. Ladders down shafts (stairs to treasure: a Metal Coat at the bottom of the deepest), the collapsed gallery with the lamps, Excadrill and Ferrothorn and Duraludon.

**The Atlas Foothills** (40×104, north to south; the great road). *From the Strait's south shore up into the range.*
1. **The shore:** scrub and red earth, a silver miner in plain view (he's walked over from Tartessos), **band 1** in the scrub.
2. **The gorge:** a river gorge walled by red cliffs, a waterfall with a cave at its top (the Horn; a Waterfall-climb cave with a Choice Band), a Crook face to a ledge, **band 2** after a Garamantian driver who came the long way.
3. **The Atarantes** (outcamp, the midpoint): cliff dwellings with ladders between them (stairs to treasure: the highest dwelling has a Heat Rock), and the cursing cliff.
4. **The switchbacks:** cut stairs up the foothills with a pair of Atarantes on the narrowest (they battle with blank names), **band 3** in the high grass, Atlas's grunting audible from below (LABORS's Atlas's Ridge is next door), and the range's mouth.
- **Checks:** bands 3; mandatory trainers 4; rest: the Atarantes; climb: the switchbacks, ladders and a Crook face; cave: the waterfall cave; ledges drop north toward the shore.

**The Atlas Range** (3 floors and the summit; the land's dungeon). Wind and cold; the sky sagging (★): floor 2's pillar sockets are plates, and drums on them prop the ceiling up a tile row so you can pass under; floor 3 combines them with the wind (a drum on a socket also blocks a gust); the sky camp is the rest; the summit under the stars (★); Moltres at sunset on the summit's ledge (LEGENDS).

**Pokémon.**
- **Signature:** Excadrill, Corviknight and Skarmory, Duraludon, Golurk, Lycanroc (Orthos's kind), Barbaracle (the Pillars' rock), Crawdaunt.
- **Rare behind gates:** a Corviknight static at the Range's eyrie (the Wings); Archaludon's line's showpiece (a Duraludon very rare at 78 on the summit); Jirachi and Moltres (LEGENDS).
- **Homeland lines (§2.7):** Laolith, the earth-born, common on the Atlas Range; Melodrakon in LABORS's Garden.
- **Gaps:** none.

**Story.**
- **The land's question: "Does Atlas really hold up the sky?"** **A witness:** Atlas (LABORS's Ridge, after Labor 11). **A place:** the Atarantes' "pillar of heaven." **An object:** the sky's underside, which you've touched. Arganthonios's hall gives the last. Alethea writes: *"Atlas holds up the sky. He'd like a word about it."*
- **Side quests:** the tide temple; Kolaios's krater; the lost miners; the nameless child; Atalanta at the Garden (OIKOUMENE §6); and OIKOUMENE's priest, traders, tide-well, silver-runner, miners and tin-trader.
- **Lore:** the scratched-off names; Kolaios's wreck; Atlas's sweat-salt; the Herakleion's two pillars, which aren't the real ones (LABORS's are).

**Returns and links.**
- **For later:** the ocean fog past the Pillars (the Bag, onto Okeanos); the temple of Kronos's sunken half (the Pearl at high tide: a Relicanth and the temple's bronze sickle, lore for the main story's Harpe); an arrow-stone at the Atarantes pointing at Atlas's shoulder (Abaris's Arrow: a ledge where Atlas's sweat dries into salt crystals, a Comet Shard).
- **Links:** LABORS's Pillars, Erytheia, Garden and Ridge; Herakles at the Pillars, the Periodos's end (OIKOUMENE §5); after the Odyssey, the sea lane east to the Western Sea; Libya's horizon.

**Bosses.** King Arganthonios (PERIODOS §4.8, 80–82; Rock under P-12). Herakles meets you at the Pillars but fights at Oeta (§11.3, P-13). The sky camp's keeper, an Atlas priest (80).

### 3.9 The Western Sea: Magna Graecia

> **The fate undone.** The Sibyl of Cumae asked Apollo for as many years as there are grains in a fistful of sand, and forgot to ask for youth. She has no prophecies to give now, and asks visitors what they'd do with all that time.

**Identity.**
- **Myth:** the Greek colonies of the west: Kroton and Milo and Pythagoras, Elea and its philosophers, Cumae and its Sibyl, the Phlegraean Fields where the Giants fell, Lake Avernus, and Calypso's Ogygia; around them, ODYSSEY's wine-dark sea.
- **Palette and terrain:** bright blue sea, tufa yellow, sulfur, black volcanic sand, Doric temples bigger than any in Aethos.
- **Signature landmark:** Cumae's acropolis, with the temple of Apollo above the Sibyl's cave.
- ★ **Vista, "The buried giants":** across the Phlegraean Fields, rock spires stand up like fingers and a huge face lies in the hillside with steam coming from its mouth; at night the vents glow red.
- ★ **Set piece, "The hundred mouths":** in the Sibyl's cave, a hundred openings in the rock answer you in a hundred voices (Virgil, *Aeneid* 6.42–44).
- ★ **Set piece, "Daedalus's doors":** the temple of Apollo at Cumae has gold doors Daedalus made after he flew from Crete, carved with his whole story, and a blank panel: he tried twice to carve his son and couldn't (*Aeneid* 6.14–33). For a player who met Daedalus at Knossa and Icarus in the Underworld, the quietest moment in the post-game.

**Maps.** ODYSSEY's sea runs wild 70–78. This file's towns and places, open after the voyage: wild 74–77, behind later gates 77–80.

| Map | Kind | Size | Area | Levels | Tier |
|---|---|---|---|---|---|
| `Kroton` | Port town, with Milo's palaestra hall (PERIODOS §4.9) | 52×44 | — | — | 1.0 |
| `Elea` | Village on a coast path | 40×32 | — | — | 1.0 |
| `Cumae` | Town on its acropolis, with the temple and the Sibyl's cave | 52×48 | — | — | 1.0 |
| `WesternSea_SibylsCave` | The cave of a hundred mouths, 1 floor | 32×24 | H8 (cave slots) | 75–77 | 1.0 |
| `WesternSea_PhlegraeanFields` | The great road: Cumae's gate across the burning fields to Lake Avernus | 104×40 | H7, H8 | 74–77 | 1.0 |
| `WesternSea_GiantsThroat` | Vent caves under the fields, 2 floors | 30×30 each | H7 (cave slots) | 75–77 | 1.0 |
| `Ogygia` | Calypso's island and the Nursery | 36×32 | H9 | 75–77 | 1.0 |
| `WesternSea_Sybaris` | The drowned city (the Pearl) | 40×40 | — | 77–80 | S |
| `Katane`, `Etna_*` | Sicily's volcano: the Fire crown, five maps | §10 | H11 (new) | 76–80 | 1.0 under P-15 |

**Stops.**

| Stop | Temple, shrine or outcamp | Herm | Hall | Services |
|---|---|---|---|---|
| **Kroton** | **The temple of Hera Lakinia** on its cape | A Greek herm on the quay | **The palaestra:** Milo of Kroton | Asclepeion, the doctors' house, Agora, the Super Rod |
| **Elea** | **A shrine of Athena** on the acropolis, very still | A herm that, Zeno insists, never arrives at the gate | — | Healer |
| **Cumae** | **The temple of Apollo** with Daedalus's doors, and the Sibyl's cave | A herm at the lower town's gate | — | Asclepeion, Agora |
| **The sulfur camp** (outcamp, the Fields' midpoint) | **Hephaestus's vent shrine** | A herm of black tufa | — | The sulfur-gatherers heal |
| **Ogygia** | **Calypso's cave**, a shrine of the nymph | A vine-wrapped herm | — | Calypso heals; a bed |

**New households:**
- **Kroton, the split oak.** Milo, in story, died with his hands trapped in a split tree. Here a sign by a split oak in Kroton's grove reads MILO, DON'T. His trainer is told off by it daily. Lore, and a daily Protein if you read it to Milo.
- **Cumae, the door-keeper.** Polishes Daedalus's doors and has never noticed the blank panel. Show him (the Mirror of Truth, later, shows a faint figure in it: Icarus, falling, which Daedalus did carve and then covered). Reward: Ikaroth (§2.7) comes to the temple steps.
- **Ogygia, Calypso.** Quiet, unhurried, glad of company and glad when it leaves. The Seal Caves are hers. Gift: a Mystic Water, and the line "Everyone leaves. I like that they can, now."

**Roads and dungeons.**

**The Phlegraean Fields** (104×40, west to east; the great road). *From Cumae's gate across the burning fields to Lake Avernus.*
1. **Cumae's east gate**, a sulfur-gatherer in plain view, **band 1** in scorched grass between lava ridges.
2. **The fingers:** rock spires and the giant's face (★); steam vents that push you; a vent-plug puzzle (drums on vent plates, §5.1) shuts two vents to reach a ledge with a Fire Stone and the Giants' Throat's side entrance.
3. **The sulfur camp** (outcamp, the midpoint).
4. **The crater:** **band 2** on the crater floor after a sorceress from Colchis on holiday; a hot pool; a Crook face up the crater rim (a Gigantomb static, Lv 77, the homeland showpiece).
5. **Avernus:** the "birdless" lake (birds fly over it), the boatman, ghosts at night (H8), **band 3** in the reeds after an Argonaut on the shore path, and a cave mouth in the lakeside cliff with a **shadow door** (the Helm of Hades, later: the Avernus door, P-9).
- **Checks:** bands 3; mandatory trainers 4; rest: the sulfur camp; climb: the crater rim; cave: the Throat; ledges drop west toward Cumae.

**The Giants' Throat** (2 floors). *Vents under the fields, down into the giant's chest.* Floor 1: steam currents push you; drums on vent plates redirect them. Floor 2: the giant's hand, a cavern of finger-bones, with Turtonator in the rock and the buried Giant's last breath: a Gigantomb boss (Lv 80) if you wake him by plugging the last vent. Rest: a cold spring on floor 1.

**The Sibyl's Cave** (1 floor). A long trapezoid gallery with a hundred side openings; the Sibyl in her jar at the end (OIKOUMENE §4.9); the voices set piece (★); a shaft ladder up to the temple of Apollo's back room (stairs to treasure: a TM and a Pythian Laurel).

**Kroton, Elea, Ogygia** (towns): Kroton's palaestra and Pythagoras's school (the anvils, OIKOUMENE §4.9), the temple of Hera on its cape with one column standing; Elea's philosophers (Zeno's tortoise, Terapagos's lead in LEGENDS; a Chelyra wild on the coast path, §2.7); Ogygia's caves and vines.

**Pokémon.**
- **Signature:** Magmar, Magcargo, Salazzle, Centiskorch and Turtonator (the fields), Spiritomb, Sinistea and Banette (Avernus at night), Azumarill and Feebas (Ogygia).
- **Rare behind gates:** Feebas (fishing, Ogygia); Turtonator (rock smash, the Throat); the Sybaris table (S, the Pearl); Terapagos and Kubfu (LEGENDS). Volcanion moves to Etna (§10, P-15). Under P-15 the Fields keep Salazzle, Centiskorch and the Poison shares, and Etna takes Magmar's, Slugma's and Turtonator's lines.
- **Homeland lines (§2.7):** Gigantomb in the Fields and the Throat; Chelyra at Elea; Ikaroth at Cumae.
- **Gaps:** none.

**Story.**
- **The land's question: "Is Avernus a door to the dead?"** **A witness:** the Avernus boatman. **A place:** the lake, which birds fly over quite happily. **An object:** an obol on the shore, worn smooth. Milo's hall gives the last: he went looking for the door as a boy and found a cave. Alethea writes: *"Avernus is a lake. Birds fly over it. There is a door, but it isn't where they said."* (The door is the shadow door in the cliff, P-9.)
- **Side quests:** Daedalus's doors; the split oak; Calypso; the vent puzzles; and OIKOUMENE's Pythagoras, the doctors, the Sibyl, the sulfur-gatherers, Zeno and Parmenides.
- **Lore:** the blank panel; MILO, DON'T; the giant's face; the drowned city off the coast.

**Returns and links.**
- **For later:** the Avernus door (the Helm of Hades) opens a back road into UNDERWORLD's Plain of Lethe (P-9, for UNDERWORLD's designer), where a shade who missed the ferry waits; **the drowned city of Sybaris** (the Pearl; S): the luxury city drowned under a diverted river, its famous dancing horses' stables (lore) and a Milotic static; the Mirror on Daedalus's doors; an arrow-stone on Kroton's cape pointing at a sea stack (Abaris's Arrow: a Hawlucha nest).
- **Links:** ODYSSEY's islands (H1–H6, H10) and its free sailing; Daedalus and Icarus (LABYRINTH, UNDERWORLD); Solon's question about Milo (§3.2).

**Bosses.** Milo of Kroton (PERIODOS §4.9, 80–82). The buried giant (80). ODYSSEY's bosses on its own islands.

### 3.10 The Ring of Okeanos

> **The fate undone.** On the Isles of the Blessed, Kronos's golden age goes on for the heroes whose stories are finished (Hesiod, *Works and Days* 167–173). It is the golden age Phaedon wanted, and it exists: only for the finished.

**Identity.**
- **Myth:** the edge of the Greek world: the river-ocean Okeanos flowing round everything; the Cimmerians in their mist, where Odysseus called the dead; the Land of Dreams with its gates of horn and ivory; the Gates of the Sun; the Gorgons and the Graiai; the Isles of the Blessed; and, this game's addition, **the Selvage**, where the cloth of the world ends.
- **Palette and terrain:** three faces of the rim: Cimmerian gray-violet mist and dusk; the Isles' gold meadows red with roses; the Selvage's white water falling into black.
- **Signature landmark:** the Selvage.
- ★ **Vista, "The edge":** at the end of the Selvage road the ground stops. Okeanos pours over the world's rim in a long white fall, and below it is black with stars. The camera pans out over the edge and holds. The single grandest image in the game.
- ★ **Set piece, "Sunset at the Gates":** at dusk, Helios's cup sails up the river and in through one of the twelve bronze doors of the Gates of the Sun; the door closes, and night falls on the map.
- ★ **Vista, "The Isles":** landing at dawn on gold meadows red with roses, retired heroes walking in them.

**Maps.** Wild 75–80; the hardest trainers outside the halls (80–85).

| Map | Kind | Size | Area | Levels | Tier |
|---|---|---|---|---|---|
| `Okeanos_River` | The river-ocean lane, in two arcs (north and south) | 2 × 32×100 | O1 | 75–78 | 1.0 |
| `Okeanos_CimmerianShore` | The great road: mist route with the Cimmerian village and Odysseus's pit | 100×36 | O2 | 76–78 | 1.0 |
| `Okeanos_CaveOfSleep` | 2 floors | 30×28 each | O3 | 77–79 | 1.0 |
| `Okeanos_GatesOfTheSun` | Sanctuary with twelve bronze doors | 44×32 | — | — | 1.0 |
| `Okeanos_Springs` | Tethys's house, where every river rises (the rim's outcamp) | 32×28 | — | — | 1.0 |
| `Okeanos_Graiai` | The gray sisters' cave, 1 floor | 28×24 | O6 | 77–79 | 1.0 |
| `Okeanos_GorgonsIsle` | Mirror-walked island (LEGENDS) | 40×40 | O5 | 78–80 | 1.0 |
| `Okeanos_Selvage` | The world's edge road | 100×32 | O7 | 78–80 | 1.0 |
| `Okeanos_IslesHarbor`, `Okeanos_IslesMeadow` | Two of the four Isles: the town with the tower of Kronos hall (PERIODOS §4.10), and the meadow | 48×40 each | O4 | 78–80 | 1.0 (the other two isles S) |
| `Okeanos_LandOfDreams` | Sanctuary | 32×32 | — | — | S (PG-26's fallback only) |

**Stops.**

| Stop | Temple, shrine or outcamp | Herm | Hall | Services |
|---|---|---|---|---|
| **The Cimmerian village** | **The shade-callers' pit shrine**, at Odysseus's trench | A herm of Hermes the guide of souls, the only lit thing in the mist | — | A healer by lamplight |
| **The Springs of Okeanos** (the rim's outcamp) | **Tethys's house** | A herm of driftwood | — | Tethys heals; a bed; a Mystic Water |
| **The Gates of the Sun** | **The twelve doors** themselves | A golden herm | — | Helios's cup docks here at night |
| **The Selvage camp** (outcamp, the Selvage's midpoint) | **A shrine of Ananke**, Necessity, with nothing in it: "she left" | A herm made of a ship's broken mast | — | Heal |
| **The Isles' harbor town** | **The tower of Kronos** | A golden herm | **The tower:** Rhadamanthys | Asclepeion, Agora, the retired heroes |

**New households:**
- **The Cimmerian village, the lamp-seller** and **the shade-caller** (OIKOUMENE §4.10). Add **the boy who's never seen the sun**: take him on Helios's cup one night to the Gate of Dawn (§3.6) for the sunrise. He gives you his only possession, a Bright Powder he thought was "sun dust."
- **The Selvage camp, the last ship's captain.** Sailed to the edge on purpose, to see. Stayed. "There's nothing to go back for that I can't see from here." Trades his Wailord for your Lapras; gives a Big Pearl.
- **The Isles, Achilles's empty house,** reserved, with a sign. Peleus waits in the next one (OIKOUMENE §4.10).

**Roads and dungeons.**

**The Cimmerian Shore** (100×36, west to east; the great road). *Perpetual dusk.* Mist weather with a short sight radius; the shade-callers on the paths (mandatory, Ghost and Dark), **three bands** in gray grass, Odysseus's trench still damp (remains, and the night table's heart), the village, the Cave of Sleep's mouth, the Land of Dreams' white rock (S), and the Graiai's cave in a sea cliff.

**The Cave of Sleep** (2 floors). Ovid's cave (OIKOUMENE §4.10): talk too loud and the sleepers wake into battles. A drum-on-plate puzzle with a rule: pushing a drum makes noise and wakes the nearest sleeper, so you order your pushes to wake the ones you can afford to fight. Snorlax, Hypno, Komala; Amnoze, the homeland line, everywhere asleep.

**The Gates of the Sun** (44×32). Twelve bronze doors, one per hour of the night. **The plate puzzle:** twelve hour-plates and four sun-disc drums; set them on the hours Helios names and the thirteenth door, the one not on the dial, opens (Dialga, LEGENDS). The dusk set piece (★).

**The Selvage** (100×32). The world's edge: the ground thins to a lip of rock, wrecks of ships that sailed off the edge hang on it (remains: three wrecks, three captains' logs, each a line long), Ultra Beasts come through the frayed sky (LEGENDS), the Selvage camp at the midpoint, **three bands** of pale grass, four mandatory Blessed Heroes on the narrowest lip, and the edge (★).

**The Isles of the Blessed** (two maps at 1.0). The harbor town and the tower of Kronos; the meadow isle with the Tapus' groves (LEGENDS), roses, and the retired heroes' houses: Kadmos and Harmonia, Peleus, Menelaus (OIKOUMENE §4.10), Achilles's empty one.

**Pokémon.**
- **Signature:** Lapras, Wailord and Dondozo (the river-ocean), Haunter, Misdreavus and Drifblim (the mist), Snorlax and Komala (sleep), Floette, Comfey and Spritzee (the Isles), Minior (the Selvage).
- **Rare behind gates:** Dragapult, Umbreon and Mimikyu in the mist (Augur's Eye); Sylveon, Gardevoir, Togetic and Leafeon on the Isles (Augur's Eye); Metagross and Porygon2 at the Selvage (Augur's Eye); Dialga, Palkia, the Tapus, Mewtwo and the Ultra Beasts (LEGENDS).
- **Homeland lines (§2.7):** Amnoze in the Cave of Sleep; Kalyptor on the Cimmerian shore at night.
- **Gaps:** none.

**Story.**
- **The land's question: "Is the world round, with a river round it?"** Herodotus laughed at maps that said so (4.36). **A witness:** Tethys, at the Springs. **A place:** the Selvage. **An object:** Helios's cup, which sails the ring every night. Rhadamanthys's hall gives the last. Alethea writes: *"Herodotus laughed at this. He was wrong. Okeanos runs round the world, and the world has an edge. We stood on it."*
- **Side quests:** the boy and the sunrise; the last captain; the Graiai's eye; the Gorgons' Isle by the Mirror; Menelaus's letter from Helen (§3.5); the Cave of Sleep's sleepers; and OIKOUMENE's lamp-seller, shade-caller, Kadmos and Harmonia, Peleus.
- **Lore:** the captains' logs; Odysseus's trench; the empty shrine of Necessity; Achilles's reserved house.

**Returns and links.** Okeanos is the end of the Oikoumene, so its gates look back: every land's "for later" gate is open by now, and Rhadamanthys's last line points to the Pillars, where Herakles waits (OIKOUMENE §5). The Selvage's camp sells nothing and asks nothing; it is the place to stand and look.

**Bosses.** Rhadamanthys (PERIODOS §4.10, 82–84). The Selvage's keeper, a Blessed Hero at the edge (84). Herakles next.

---

## 4. The epics at the same bar

The epics keep their own docs, maps, tables and levels (PG-7). This section holds each one to the §1 bar and lists what it needs to pass. Items marked **for the epic's designer** are additions that doc's owner should agree to; none changes an approved decision.

### 4.1 The Twelve Labors (`LABORS.md`)

- **Shape:** six pairs of two Labors, set by Olympias at the Heraion; 28 maps; bosses 70–79, Olympias 80; the Kotinos as the prize. Each Labor has one verb (corner, cauterize, track, lure, divert, flush, leap and ride, feed, unmask, herd, endure, escort).
- **Awe already there:** the Pillars set up at sunset (Labor 10); the sky on your shoulders (Labor 11); Kerberos dragged up into the light (Labor 12); twelve metopes going up on the Temple of Zeus.
- **To pass the bar (for LABORS's designer):**
  - **Herms and outcamps.** Herms at Abdera, Themiskyra and Erytheia's landing, each in its land's form (a Thracian horseman herm, an Amazon's spear-post, a red-stone cairn). An outcamp at the midpoint of each route-like map: Nemea Glen (the lion-hunters' shelter), Erymanthos Slopes (a boar-hunters' hut), the Bistonian Plain (a Thracian shepherd's tent), the Thermodon Road (an Amazon waystation), Erytheia (Eurytion's empty hut).
  - **Plates.** Labor 5's two rivers turned through Augeas's farm are the Labors' natural plate puzzle: drums on sluice plates divert the Alpheios and the Peneios channel by channel (it keeps LABORS's "turn two rivers" verb; the plates are how). Labor 4's snowfield can hold one drum-and-plate gate to the boar's lair.
  - **Stairs to treasure.** Paionios's scaffold on the Temple of Zeus: a ladder that gains a rung with each metope, ending at the roof after twelve with a Gold Bottle Cap and the view over the Altis.
  - **Remains.** At Nemea Glen, the lion's earlier hunters' graves (Route 14's stele already points at them); in Diomedes's stable, the bronze mangers and what the mares were fed (told, not shown); on Erytheia, the herdsman Eurytion's and the dog Orthos's cairns, which Geryon tends.
  - **Signature species:** the Labors' cast (Nemeleon, Lernathan, Kaprodon, Belornis, the Bull from the Sea) stays Aethos's; the far lands' homes from COVERAGE (E3, E7, W1, W5, W7) give the trip abroad its new animals.
- **Links:** the Labors open Thrace, Themiskyra, the Caucasus and the far west on the Oikoumene's chart; the Kotinos opens Herakles at the Pillars (PG-24) and Ouranos (POSTGAME §3.3).

### 4.2 The Katabasis (`UNDERWORLD.md`)

- **Shape:** 27 maps from the Mani Road down through Charon, the Styx, Kerberos, the Meadows of Asphodel, the Crossroads, Lethe and Mnemosyne, the House of Hades, Tartarus and the Chasm; the Cutter as your guide; bosses 72–80.
- **Awe already there:** the Styx crossing; the nine-day fall into Tartarus; Giratina's upside-down Chasm; Elysium's gold; "don't look back" on the Ascent.
- **To pass the bar (for UNDERWORLD's designer):**
  - **Herms.** A herm of Hermes the guide of souls at Tainaron and on the Acheron Bank. Below the Styx, herms register but only list Tainaron: the dead don't fly.
  - **The Mani Road** (30×70) is the epic's great road: lengthen it to the §1 standard with its roadside shrine of Poseidon as the outcamp and two Crook faces up the tower villages (P4 in WORLD_EXPLORATION).
  - **Plates.** **Sisyphus's Hill** becomes the Underworld's signature plate puzzle: his boulder (a drum in raw-rock skin, the one place a raw boulder rolls) slides back a tile for every step you don't push it, and the plate is on the summit. Get it there and it stays. Sisyphus sits down on it. "It stayed up. Now what do I do?" Tartarus's relics exam keeps its design.
  - **Stairs to treasure.** The Danaids' jar in the Meadows: a ladder down inside the leaking jar to its cracked bottom (a Big Pearl, and the leak's cause).
  - **Remains.** The unburied on the Acheron bank (already there); add Orpheus's lyre-peg on the Ascent, where he turned round.
  - **Back doors (P-9).** Three other doors of the dead in the Oikoumene, each a shadow door for the Helm of Hades: Avernus (§3.9) into the Plain of Lethe; the Acherusian cave on the Black Sea (§3.3) onto the Ascent of Tainaron, the way Herakles came up with Kerberos; and Odysseus's trench on the Cimmerian Shore (§3.10), a one-room view down into the Meadows. They make the Underworld part of the wider world.
- **Signature species:** Obolorn's line, Charonaut, Stygiad, Basculegion; the Oikoumene's Ghost families appear only as shares, at night.

### 4.3 The Odyssey (`ODYSSEY.md`)

- **Shape:** the one-way voyage from Cape Maleia to Elaia: eleven steps, 27 maps, bosses 74–81; gives Aeolus's Bag, the Mirror of Truth and the true Periplous.
- **Awe already there:** the storm off Maleia; the Cyclops's eye opening; the bag opened within sight of home; the Sirens; Argos at the gate.
- **To pass the bar (for ODYSSEY's designer):**
  - **Herms.** Each island's landing has a herm in the island's own style (a driftwood herm on the Lotus Isle, a bronze one on Aiolia's wall). During the voyage they register but don't take you home: the Wings already don't (ODYSSEY §4).
  - **Plates.** The Cyclops's cave: the great door-stone stays the Cyclops's to move, but the cave's sheep-pens are a drum-on-plate puzzle to separate the rams you'll ride out under. Scylla's cave: two plates hold back the tide long enough to reach the inner ledge.
  - **Stairs to treasure.** The *Euploia*'s mast ladder to the crow's nest, usable at sea: from the top you spot islets and sealed jars that don't show from the deck.
  - **Remains.** Elpenor's oar planted on his tomb on Aiaia (*Odyssey* 12.15); the Sirens' meadow and its bones (12.45–46), told, not drawn; the Sun's cattle's hides on Thrinakia, which crawl (12.395).
  - **The Argo's Road** (P-8) passes Aiaia and Scheria.
- **Signature species:** Polyphant, Seirenade, Hexylla, Trybdis and Haligeron (Aethos's), and the Western Sea's homes (H1–H6, H10).

### 4.4 Atlantis (`POSTGAME.md` §3.2)

- **Shape:** beyond the Pillars; the Nereids and the Nereid Pearl; three drowned rings on a breath counter; Poseidon's temple and Pontanax; Manaphy's nursery; the abyss and Lugia; the edge of the world and Kyogre. About 12 maps, bosses 76–80.
- **Awe already there:** the first dive, and the rings seen from above through clear water; the abyss.
- **To pass the bar (for POSTGAME's designer):**
  - **Herms and rests.** A shell herm in each air dome, registered for the return dive; the air domes are the rests.
  - **Plates.** Plato's rings were joined by canals and tunnels (*Critias* 115d–e). The rings' water gates are a plate puzzle that combines with breath: drums on plates open the next ring's tunnel, but every push costs breath, so you plan pushes between air pockets.
  - **Stairs to treasure.** The orichalcum pillar in the citadel has a spiral stair to an air pocket at its top, where the kings' oath is cut (a lore text and an Ability Patch).
  - **Remains.** The ring of the kings' bull-hunt round the pillar (*Critias* 119d–120c); gold statues of the kings and their wives round the temple (116e), green now; the racecourse's sunken chariots.
- **Signature species:** Aethos's sea lines (POSTGAME §3.2's list), with Telkanvil, the Telchines, at the forges.

### 4.5 The Olympiad (`POSTGAME.md` §3.1)

- **Shape:** Olympia's Altis as the post-game's hub; five facilities and five Brains; the Arena of Champions in the Echo Stoa; the Moment and Victini.
- **Awe:** the stadium's vaulted tunnel opening on the full stadium and its crowd; Phidias's empty throne in the Temple of Zeus ("It stood up and walked to Olympus").
- **To pass the bar (for POSTGAME's designer):**
  - **The Sacred Way** (30×64) is the hub's road in: lengthen it to the §1 standard (a great road of about 90 tiles), with the **Alpheios ford** as the outcamp (WORLD_EXPLORATION's P7, the Horn's cascade) and a herm at Olympia's gate.
  - **Remains.** **The suitors' mound:** Oinomaos killed thirteen suitors who raced him for his daughter, and they were buried together at Olympia (Pausanias 6.21.9–11). Their mound by the hippodrome has thirteen grave markers, and Pelops's chariot wheel.
  - **Stairs to treasure.** The Nike's pillar has a ladder for the cleaners (a Pythian Laurel at the top, before Victini comes down).
- **Species:** no wild homes (rentals aren't catches, §2.7). Olympia is where every generation is *seen* first in battle.

### 4.6 The Primordials and the Prime Mover (`POSTGAME.md` §3.3)

- **Shape:** Gaia under Delphoi through the Korykian cave, Oceanus at the edge of the world under Atlantis, Ouranos above Olympus's clouds (all Lv 88); then the four keys and Arceus on the summit (Lv 95), reached by standing still.
- **Awe already there:** Ouranos coming down to look at the one who held the sickle; the summit where walking gets you nowhere.
- **To pass the bar (for POSTGAME's designer):**
  - **The summit path** is the game's last great road: a climb above the clouds from Pegaunos's cloud meadows (the outcamp: a meadow of thunder-horses, a spring) to the summit's foot. Its terrain changes as you climb: cloud meadow, marble ruins of the Giants' war, bare light.
  - **The last herm.** At the summit's foot, a plain herm of Hermes. It's the only herm that lists every herm on both charts.
  - **Plates.** The four keys set into the stone at the summit's foot are four key-plates; set all four and the stone opens (POSTGAME's design, given the plate's look so it reads as part of the same vocabulary).
  - **Remains.** On the slope, the debris of the war against the Giants: a giant's spear the length of a ship, a broken throne.
  - **Gaia's way in** uses the Korykian cave's back section on Route 9 (WORLD_EXPLORATION D8), so the last epic returns to a place the player first saw in Act II.

---

## 5. Shared kit

Pieces every land uses. Build each once.

### 5.1 The plate puzzle (boulder on switch)

- **The look.** A **bronze plate**: a one-tile disc set in the floor, with a meander rim, dull when empty and bright when pressed. One metatile in two states, drawn for each land's floor palette.
- **The drum.** The Girdle's obstacle stays a fluted column drum on its side (WORLD_EXPLORATION §3, row 5). In the Oikoumene it takes **each land's skin with the same silhouette** (P-5): a granite block in Egypt, an ore cart in the mines, an ice drum in the Cave of Boreas, an oak log in the Grove, an amphora on Nysa. The silhouette is what the player reads, so it never changes.
- **Teach, test, combine.** Every dungeon follows MAP_DESIGN §3: one drum on one plate, in a room with nothing else; then several plates and an order to find; then plates combined with another mechanic (water level, wind, breath, noise, a timed gate).
- **Reset.** A **reset lever** by each puzzle room's entrance puts every drum back. Leaving the map resets them too. A solved puzzle stays solved: its flag swaps in the solved layout, and its drums are hidden.
- **Engine.** A small special, `Ichor_CheckPlates`, compares the map's plate list with its drums' positions after each Girdle push and runs the map's script when the set of pressed plates changes (`setmetatile` and `special DrawWholeMapView`). Kaldera's dials already read a pushed drum's position (ENGINE_API §6's "parking at the plate"), so this generalizes built code. **Low.**

### 5.2 Herms, one per town entrance

- **Placement:** within three tiles of the town's main entrance, on the path, 1×2 tiles with a sign beside it: "Herm of <Town>. Touch to travel."
- **Registration and travel:** IDEAS.md's queued change (first touch or first heal registers it; travel from any herm). In the Oikoumene the list is per chart, plus the cross-chart entry (§2.5).
- **Forms by land:** the Troad and the Greek colonies, a Greek herm (the colony's own touch: mouse, felt, oar); Lydia, a lion stele; Phrygia, a rock-cut niche of the Mother; the Black Sea, a bronze bull-head post; Scythia, a stone *baba*; Hyperborea, a golden arrow in a stone; Egypt, an ibis-headed pillar of Thoth; Aithiopia, a lion-headed pillar of Apedemak; Libya, a ram-horned cairn of Ammon; the Far West, a Phoenician standing stone; Okeanos, driftwood, a mast, or gold. Each is one 1×2 metatile pair in the land's tileset.

### 5.3 Outcamps

- **What one is:** the midpoint rest on every great road, and the shrine-carrying stop where there's no town. It always has a healer, a herm, a shrine or altar, and one household or tent with a gift, trade or quest. Some add a bed or a shop.
- **Footprint:** about 12×10 tiles, built from the land's tents, huts or a single building. Each outcamp's household is unique (MAP_DESIGN §2), but the tents and huts are shared pieces in the land's tileset.

### 5.4 The remains of the lost

- **Kinds:** a wreck, a grave or mound, an abandoned camp, a last message.
- **Each has:** an object you can read (a stele, a log, a tablet, a helmet), one or two lines that tell a small story without explaining it, and usually something: an item, a quest start, a dig spot for the Trowel, or a note on Alethea's chart. **Some pay nothing,** on purpose (Niobe's fourteen mounds), so the player reads them for their own sake.
- **Tone:** quiet. No bodies on screen; bones only where myth puts them and only as shapes.

### 5.5 Vistas, set pieces and changing maps

- **Vistas:** the camera leaves the player and pans to the landmark (the vanilla camera object, `SpawnCameraObject` and `applymovement` on `OBJ_EVENT_ID_CAMERA`, as Emerald's Sootopolis scenes use), holds two seconds, and returns. Once per save, then a sign lets the player replay it.
- **Big set-piece tiles:** walls, pyramids, the giant's face, the Selvage's fall. Each is a block of unique metatiles in the land's tileset, counted in §6.
- **Maps that change:** the Nile flood (by month), Gadeira's and the Atlantic Shore's tides (by time of day), the Sand Sea (by day). All use layout swaps on load (`setmaplayoutindex` in an `ON_LOAD` script, keyed to a var, `Ichor_GetMonth()` or the clock). **Low** each.

### 5.6 Names, sections and budgets

- **Map names:** `<Land>_<Place>` for routes and dungeons (`Troad_SkamanderPlain`), the town's own name for towns (`Ilion`), and the hall names PERIODOS gives.
- **Sections:** outcamps and dungeon floors share their parent map's section, so the ~75 sections OIKOUMENE §10 counted still hold (the Hoenn block gives ~87).
- **Trainers:** PG-38 gives the Oikoumene 300 ids. The halls, champions, rematches and Herakles take 63. That leaves **about 23 per land** for routes and dungeons. Each land's section above stays inside that: 12–15 on its roads, 4–6 in its dungeons, 2–3 rematch households.

---

## 6. Art and ROM

### 6.1 The ROM today

`make` on this branch, 2026-11-17: **ROM 24,157,072 B of 32 MiB, 71.99%.** That leaves **9.0 MiB** (9,397,360 B) for everything still to come: the rest of the main game, the post-game epics, the Oikoumene and the music.

### 6.2 What each land needs

OIKOUMENE §7's tilesets stand: one land secondary each (7 palettes; the shared primary stays Aethos's 6), six interior secondaries, and the shared steppe and far-west sets with LABORS. This guide adds the set pieces its awe moments and kit need. Every new piece follows `design/STYLE.md`'s process.

| Land | Tileset (OIKOUMENE §7) | New set pieces for this guide | Plate floor, drum skin, herm |
|---|---|---|---|
| Troad | `troas` | Ilion's two-screen wall and the Skaian tower; beached hull ribs; the half-built horse (4×4); burial mounds; the elms; the river-wave overlay | Limestone plate; marble drum; Greek herm |
| Lydia | `lydia` | Sardis's acropolis rock; the Thousand Hills' great mound; the weeping rock (rain state); Phrygian rock-cut facades; the timber tomb chamber | Plate on tufa; bronze-banded drum; lion stele, Mother's niche |
| Black Sea | `pontos` | The Clashing Rocks (two states); the bronze palace and four fountains; the Fleece's oak and glow; Colchian log towers; furrows | Plate on dark earth; oak log; bull-head post |
| North | steppe (shared) + `hyperborea` | Kurgans and stone idols; wagons; ice walls (melted state); the round temple; the gale whiteout | Plate on frozen earth; ice drum; *baba*, golden arrow |
| Egypt | `kemet` | Three pyramids (each about 8×6); the Sphinx; the colossus; gnat-towers; obelisks; a flood layout's water edges | Plate on sandstone; granite block; ibis pillar |
| Aithiopia | `aithiopia` | Meroë's pyramid rows; baobab (with ladder); the stable roof; the sunrise palette ramp; Andromeda's rock and chains | Plate on red earth; amphora; lion pillar |
| Libya | `libye` | Dune crests (three layouts); the oracle's rock; the salt house; spear tips in sand; keel grooves; desert glass (animated) | Plate in a channel; stone sluice drum; ram cairn |
| Far West | far west (shared) | The sagging-sky ceiling and the star field; tide flats (two states); cliff dwellings; ore carts and rails | Plate on slate; ore cart; Phoenician stone |
| Western Sea | `magna_graecia` | The giant's face and finger spires; vents (glow at night); Daedalus's doors with the blank panel; the Sibyl's hundred mouths | Plate on tufa; tufa drum; Greek herm |
| Okeanos | `okeanos` | The Selvage's fall into stars (animated); twelve bronze doors; mist overlays; the Isles' rose meadows | Plate on wet rock; sun-disc drum; driftwood and gold herms |
| Shared | — | The bronze plate (two states), the reset lever, one tent and one hut per land for outcamps | — |

### 6.3 The estimate

The 1.0 Oikoumene in this guide has about **61 outdoor maps and 42 dungeon floors** (OIKOUMENE §13's 1.0 had about 45 outdoor maps), and its great roads are about 100 tiles long instead of 60. The halls (PERIODOS) are unchanged.

| Item | OIKOUMENE §13, 1.0 | This guide, 1.0 | Why it grew |
|---|---:|---:|---|
| Map layouts, events, connections | ~210 KiB | ~330 KiB | More and longer maps; flood, tide and dune layouts |
| Tilesets: land secondaries, interiors, set pieces | ~170 KiB | ~240 KiB | §6.2's set pieces, plates and herm forms |
| The chart | ~35 KiB | ~35 KiB | — |
| Encounter tables, Nurseries, homeland lines | ~90 KiB | ~95 KiB | Homeland lines are slots in existing tables |
| Trainers outside the halls (~230) | ~65 KiB | ~60 KiB | Capped at PG-38's ids |
| Trainer and NPC sprites | ~100 KiB | ~120 KiB | Outcamp and household people |
| Scripts and text | ~280 KiB | ~420 KiB | Land questions, remains, ~30 more households |
| Music, 15–18 tracks | ~150 KiB | ~150 KiB | — |
| Code (plates, vistas, layout swaps, arrow-stones) | ~15 KiB | ~25 KiB | §5's specials |
| The ten halls | ~260 KiB | ~260 KiB | — |
| **Total** | **~1.35 MiB** | **~1.7 MiB** | |
| **Full (all stretch)** | ~1.85 MiB | ~2.3 MiB | |

- **With the epics** (POSTGAME §7's ~2.0 MiB, plus about 0.1 MiB for §4's additions) and LEGENDS's ~0.3 MiB, the whole post-game at 1.0 is about **4.1 MiB of the 9.0 MiB free.** That leaves about 4.9 MiB for the rest of the main game and its music.
- **Levers if it runs short,** in order: the one-arrangement hall music (PG-41, saves ~35 KiB); stretch maps stay stretch; flood and tide states drop to one layout each (~40 KiB); then POSTGAME §7's levers (Hoenn's remaining maps and tilesets, shared Mega cries).
- **Every land's builder** notes `make`'s ROM line before and after, in the land's doc.

---

## 7. Build order

### 7.1 First, the shared kit (one chunk, two helpers)

Nothing in the lands should start until these exist, because every land uses them:
1. **Engine helper:** `Ichor_CheckPlates` and the reset lever (§5.1); the vista camera wrapper (§5.5); layout swaps by month, clock and day; the arrow-stone field prompt (P-3, can wait until the North). The prerequisites OIKOUMENE §10 already names, done by the engine and hoenn-cut sessions: the Hoenn section audit, the chart slot (PG-11), and the trainer-id raise (PG-38).
2. **Art helper:** the bronze plate and lever, and the herm-and-sign pattern; then the Troad's `troas` tileset first.

### 7.2 Then the lands, most payoff first

| # | Build | Why here | Opens with |
|---|---|---|---|
| 1 | **The Troad** | The Oikoumene's vertical slice: the first eastern landing, closest to the main game's look (Greek stone, so the least new art per map), the richest cast (Hektor, Priam, Cassandra, Odysseus), and it proves every line of the §1 bar. Build it, play it, and fix the bar before the other nine copy it | The ship east |
| 2 | **Egypt** | The hub (Daphne's fossils, the egg-ovens, the incenses) and the land that most says "new world." The other southern lands hang off it | The ship south |
| 3 | **Lydia** | Overland from Ilion, at the next band; reuses the Troad's road and hall patterns | The Royal Road |
| 4 | **The Black Sea** | The Fleece, the Clashing Rocks and Achilles; it also places LABORS's Themiskyra and Caucasus in a living land | The Bosporus |
| 5 | **Libya** | The Sand Sea's day-layouts and the Argo's Road; a second southern land at 63–70 | The ship from Kaldera (P-2), or the ravens |
| 6 | **Aithiopia** | The sunrise: the land's set piece is the post-game's prettiest moment | The cataracts |
| 7 | **The Far West** | Builds on LABORS's far-west tileset and maps; ends at Herakles | Helios's cup, Labor 10 |
| 8 | **The Western Sea's towns** | Needs ODYSSEY's sea built first | After the Odyssey |
| 9 | **Scythia and Hyperborea** | The biggest single reveal (through the North Wind), and Abaris's Arrow, which opens every land's "for later" arrow-stones | The Conch lane from Leuke |
| 10 | **Okeanos** | The end; needs the Bag and the cup | The fog |

**The epics** stay on PG-2's order (the sailing layer, Olympia, the Katabasis, the Labors, the Odyssey, Atlantis, the summit), alongside: the Troad and Egypt can be built as soon as the *Euploia* sails, which ODYSSEY's sailing layer provides.

### 7.3 Builder-sized chunks: three helpers per land

Every land splits the same way, so three helpers can work at once without touching each other's files. Each owns its maps' builder script under `tools/ichor/maps/` and its section of `design/maps/<Land>.md`.

| Helper | Owns | Done when |
|---|---|---|
| **A, art** | The land's secondary tileset, its interior set, its set pieces (§6.2), its herm, plate floor and drum skin, its outcamp tents or huts | Tiles compile with Porytiles; a test map shows every set piece; STYLE.md's review gate passes |
| **B, towns** | The port or hub town, the other towns and villages, every interior, every household's script, the hall's map and puzzle (PERIODOS) | Every house is enterable with its gift, trade or quest; herms register; the hall is beatable |
| **C, roads** | The great road, the other routes and lanes, the dungeons and their plate puzzles, the wild tables (from COVERAGE and §2.7), the trainers | The §1 checklist's road, gate, puzzle and Pokémon lines tick; `map_audit.py` is clean; every COVERAGE area of the land is on a map |

- **Order inside a land:** A starts first and hands B and C a working palette and a placeholder catalog by its first day; B and C build on placeholders until A's final tiles land, then re-render.
- **Integration** (the land question, the arrival scene, the remains' chart notes, the cross-land links) is B's last step, with C's maps in place.
- **Each land ends** with three render-and-critique passes on every map (MAP_DESIGN §7), a play-through at the land's band, `make` green, `smoke_test.sh` passing, the renders sent to the user (memory: show map images), and the ROM line recorded.
- **Smaller lands** (Lydia, the Western Sea's towns) can run with two helpers: A, and B and C together.

---

## 8. Proposals that change approved decisions

The first two change decisions in OIKOUMENE §13 and need the user. P-12 to P-19, from the later directions (the gym circuit, Herakles, Etna, the full Odyssey, the biomes), are in §14; P-12 and P-13 also change approved decisions. The rest are additions that need a yes from the user or an epic's designer, but don't overturn anything approved.

| # | Proposal | Changes | Recommendation |
|---|---|---|---|
| **P-1 ★** | **What "core size" means at 1.0.** PG-4 approved all ten lands "at core size, about 45 outdoor maps." The user's new bar (long routes with caves and climbs, a rest at each midpoint, a shrine at every stop, two awe moments per land) doesn't fit in 45 short maps. This guide's 1.0 is about **61 outdoor maps and 42 dungeon floors**, with longer roads, and it moves the Golden Fleece's full quest, the Clashing Rocks' side channel, Chryse and the Smintheion, and the Walls of Laomedon's first two floors from stretch into 1.0. About +0.35 MiB (§6.3) | **PG-4** | Yes. The grand-new-world direction is the user's own, and 9.0 MiB is free |
| **P-2 ★** | **Libya's coast by sea from Kaldera** (Thera founded Kyrene, Herodotus 4.150–158), so Libya opens with the ship like the other near lands; the Sand Sea still gates the oasis. (Miletos gets a lane at stretch.) | **PG-8**'s list of ship-opened lands | Yes. It gives the second step of §2.4 a southern choice, and it's the colonists' real road |
| P-3 | **Abaris's Arrow**, a key item from the North's round temple: fly from one arrow-stone to its partner. Every land gets one or two arrow-stones as its main "for later" gate. It reuses the hall's arrow flight | New key item; SYSTEMS §1's list | Yes |
| P-4 | **Homeland Aethos lines** wild in the Oikoumene (§2.7). The user's direction asks for it ("keep each land's signature Aethos species prominent"); it's listed because it changes OIKOUMENE §0 and §8's rule that the 152 Aethos species stay in Aethos | OIKOUMENE §0, §8; COVERAGE's tables gain slots | Yes, as the user directed. The dex team checks each line's levels against its evolution levels |
| P-5 | **Drum skins per land with one silhouette, and the bronze plate as an obstacle** in the gate vocabulary | WORLD_EXPLORATION §3, row 5 | Yes |
| P-6 | **Every Oikoumene stop has a temple, shrine or outcamp and an entrance herm in its land's form** (§5.2–5.3) | Extends OIKOUMENE §4's route herms | Yes |
| P-7 | **Gordion's great mound is Gordias's, not Midas's.** OIKOUMENE §4.2 calls it "Midas's great tomb mound" while Midas's barber's quest has Midas alive. Archaeology now gives Tumulus MM to Gordias, Midas's father | OIKOUMENE §4.2's wording | Yes |
| P-8 | **The Argo's Road:** seven mooring-stone rubbings across the Troad, the Black Sea, Libya, Aethos and two of ODYSSEY's islands, rewarded with a Dodona-oak beam for the *Euploia* that halves headwinds | ODYSSEY §2's upgrades (for its designer) | Yes |
| P-9 | **Three back doors of the dead** (Avernus, the Acherusian cave, Odysseus's trench), shadow doors for the Helm of Hades into UNDERWORLD's maps | UNDERWORLD's map list (for its designer) | Yes; one small map each on UNDERWORLD's tilesets |
| P-10 | **Every land's main thread is a question for Alethea's chart** (§3's intro), answered at its hall | Adds a beat to PERIODOS §2's panels | Yes |
| P-11 | **Two optional new species** for gaps no existing Pokémon fills: the **sacred ibis** of Thoth (Egypt) and **silphium** (Libya). Nothing waits on them; the herms and the silphium field have stand-ins | The dex team's list | Optional; only if the dex team has room after the Aethos 152 are finished |

**Lazarus check.** No Muses, no Chimera, no weaponized Mega, no "Gryphon"-, "Medusa"-, "Aegis"- or "Titan"-prefixed forms: the Arimaspians' gold-guardians are bones and are never called griffins, and the Gorgons stay "the Gorgons." New place names (Elaious, Sinope, Apollonia, Hypaipa, Gadeira, Tartessos, Meroë, Cumae, Elea) are all historical and clear of Lazarus's list (Acrisia, Jusmail, Kalami, Pythios, Sofos, Myrrini, Marmaro, Palati, Kaptara, Port Pello, Areios, Pentepetal, Ahiyawa, Wakewater). Lazarus's nine starters stay wild only (PG-5). The Four of Oeta (§11) are Herakles's own people from myth, not Muses, and no hall or seat is a Lazarus gym.

---

## 9. Every type a home: the biome matrix

**The direction (user, 2026-11-17):** every one of the 18 types has at least one signature biome somewhere in the post-game, built and themed, with caves and the Underworld covered explicitly.

**How to read it.** "Signature biome" is the place a player would name if asked where that type lives. Every row has at least one **built 1.0 map** (land, epic or Aethos post-game). "Cave" is the type's underground home. "Leader" is the post-game hall, seat or boss who fights with it (§11). The right-hand column says whether the row was already covered or needed a new biome.

| Type | Signature biomes (where) | Cave | Underworld | Leader (§11) | Status |
|---|---|---|---|---|---|
| **Normal** | The steppe (§3.4); the Skamander plain's wheat (§3.1); the Table of the Sun's savannah (§3.6) | The Kurgan | — | Herakles's lion (Nemeleon) | Covered |
| **Fire** | **Etna** (§10, the crown); the Phlegraean Fields (§3.9); the Gate of Dawn's sun stables (§3.6) | Etna's forge and magma chambers | Pyriphlegethon, the river of fire, on the Plain of Lethe's edge (UNDERWORLD) | Memnon (hall) | **Gap filled: a climbable volcano** |
| **Water** | The river-ocean Okeanos (§3.10); the Nile and its flood (§3.5); the wine-dark sea (ODYSSEY); Atlantis's rings | The Garamantes' tunnels; Atlantis's air domes | The Styx (Charonaut, Basculegion) | Deianeira (seat) | Covered |
| **Grass** | The Mountains of the Moon's jungle (§3.6); the delta's papyrus (§3.5); the Garden of the Hesperides (LABORS); the Isles' rose meadows (§3.10) | The Cave of Nysa's ivy grotto | Asphodel's meadows (Persenyx) | Herakles's club (Hierolive) | Covered |
| **Electric** | **Gargaros's storm crown** (§3.1): the peak's summit in a standing thunderstorm, Zeus's lookout; Chryse's mice; the Sand Sea's lightning storms (§3.7) | The Chalybes' charged ore seams | — | Croesus, "electrum" (hall) | **Gap filled:** Chryse was a village; Gargaros's summit gets a storm state as Electric's crown |
| **Ice** | Hyperborea's glaciers and the Feather Wastes (§3.4); the Atlas peaks (§3.8) | **The Cave of Boreas**, the North Wind's house | The Styx's cold (Stygiad) | Abaris (hall) | Covered |
| **Fighting** | Antaeus's Ring (§3.7); Kroton's palaestra (§3.9); the Achaean camp (§3.1); Themiskyra (LABORS) | The Walls of Laomedon's builders | — | Milo (hall) | Covered |
| **Poison** | **The Garden of Hecate** at Aia (new, below); Circe's Aiaia (ODYSSEY); the Springs of Lerna (LABORS) | The Grove of Ares's serpent floor | The Plain of Lethe's bog | Medea (hall) | **Gap filled:** Colchis had a Poison champion but no Poison place |
| **Ground** | The Sand Sea and the salt ridge (§3.7); the Pyramid Field (§3.5); the Thousand Hills (§3.2) | The Chasm of Gyges | Tartarus's floor | Kyrene (hall) | Covered |
| **Flying** | **The Isle of Ares** (§3.3, moved to 1.0), with the birds that shoot their feathers; Leuke's nesting cliffs; Gargaros's eyries; Lake Stymphalia (LABORS) | The eagle-nest galleries of Gargaros | — | Philoktetes (seat) | **Gap filled:** Flying had cliffs, not a crown |
| **Psychic** | Egypt's temples and the Great Pyramid (§3.5); the Cave of Sleep and the Land of Dreams (§3.10) | The Great Pyramid | The Lake of Mnemosyne | Proteus (hall) | Covered |
| **Bug** | The Mountains of the Moon (§3.6); the Arimaspian ant-mines (§3.4); Tmolus's vines (§3.2) | The ant galleries of the Arimaspian Heights | — | Herakles's beetle (Heracross) | Covered (thin; the jungle carries it) |
| **Rock** | The Atlas Range (§3.8); Sipylos (§3.2); the Arimaspian Heights (§3.4) | The Silver Mines of Tartessos | Tartarus's bronze-and-stone cells | Arganthonios (hall) | Covered |
| **Ghost** | **The Underworld:** the Styx shore, Asphodel, the Chasm (UNDERWORLD); the Cimmerian mist (§3.10); the Valley of Tombs (§3.5); Avernus (§3.9) | The Tomb of Ilos; the Kurgan | All of it | The Shade of Herakles (seat) | Covered |
| **Dragon** | **The Grove of Ares**, the Fleece's oak wood (§3.3); **Ladon's garden** in the far west (LABORS); the Caucasus; the Sand Sea's sand dragons | The Caucasus caves | Giratina's Chasm | Iolaus (seat) | Covered |
| **Dark** | Tartarus and the Katabasis (UNDERWORLD); the Cimmerian night (§3.10); the Valley of Tombs by night | The Cave of the Graiai | Tartarus | Medea's Hecate shrine; Herakles's Lernathan line on its Dark-Fairy rivals | Covered |
| **Steel** | **The Chalybes' forges** (§3.3); the Silver Mines (§3.8); Sardis's treasury (§3.2) | The Walls of Laomedon; the Silver Mines | The Bronze Gates of Tartarus | Hektor (hall) | Covered |
| **Fairy** | The Isles of the Blessed (§3.10); the Hyperborean meadow (§3.4); Mount Nysa's nymphs (§3.6) | The Cave of Nysa | Elysium | Rhadamanthys (hall) | Covered |

**The three new biomes, and Etna:**
- **The Garden of Hecate** (Black Sea, 1.0, 40×36, off Aia's palace). Medea's herb garden under the palace's back wall, where she grew the drugs of the *Argonautica* and the flower that sprang from Prometheus's blood (3.844–866). Poison flowers in beds, a black-water pool, Hecate's shrine at its heart, and a poison-mist hedge maze that the Torch's flame burns back for a few steps at a time. **Wild (new COVERAGE area E10):** Roserade, Toxicroak, Amoonguss, Vileplume as shares, Ophidrop and Panacoil as homeland lines, and Glimmora at night. It's the Poison hall's land made visible. Two plates under two herb-presses open the garden's locked inner bed (a Black Sludge and a Toxic Orb).
- **The Isle of Ares** (Black Sea, moved from stretch to 1.0, 36×30). *The birds of Ares shoot their feathers like arrows* (*Argonautica* 2.1030–1089). The Argonauts held their shields over their heads and banged them to drive the birds off; here, falling-feather shadows mark tiles that knock you back, and you cross under a carried shield (the Girdle's drum, rolled, as cover). Flying's crown: Skarmory, Braviary, Kilowattrel, and Belornis as a share from the Labors; Yveltal's lead (LEGENDS).
- **Gargaros's storm crown** (Troad, part of the existing peak map). The summit stands in a thunderstorm by day: lightning strikes marked tiles in a pattern, and lightning rods (drums in bronze) pushed onto plates draw the strikes away from the path. Electric's crown: Electivire, Manectric, Boltund and Emolga, with Zapdos's lead (LEGENDS).
- **Etna** (§10) is Fire's crown and the post-game's volcano.

**Caves at a glance.** Every land has at least one cave or underground dungeon, and they don't repeat a type: the Tomb of Ilos (Ghost), the Walls of Laomedon (Steel and Fighting), the Chasm of Gyges (Ground and Steel), Tantalus's palace (Water), the Grove of Ares (Dragon), the Kurgan (Normal and Ghost), the Cave of Boreas (Ice), the Great Pyramid (Psychic), the Cave of Nysa (Grass and Fairy), the Garamantes' tunnels (Water and Ground), the Glass Crater (Rock and Fire), the Silver Mines (Rock and Steel), the Atlas Range (Rock and Ice), Etna (Fire and Ground), the Giants' Throat (Fire and Rock), the Sibyl's cave (Ghost and Psychic), the Cave of Sleep (Psychic and Normal), and the Graiai's cave (Dark).

---

## 10. Etna: the Fire crown

**The direction (user, 2026-11-17):** "a volcano for sure": a real, climbable, active volcano as a major set piece and dungeon.

**Identity.**
- **Myth:** Etna is the highest, angriest mountain the Greeks knew. Hephaestus's forge is under it, with the Cyclopes (Brontes, Steropes and Arges, who forged Zeus's thunderbolts: not Polyphemus's kind) at the anvils. **Typhon**, the storm-giant Zeus beat last of all, lies pinned beneath it, and the eruptions are his breathing (Pindar, *Pythian* 1.15–28; Aeschylus, *Prometheus Bound* 351–372). The philosopher Empedokles jumped into the crater, and the mountain threw back one of his bronze sandals (Diogenes Laertius 8.69). At Katane below, two brothers carried their parents out of a lava flow, and the lava parted round them: the Field of the Pious.
- **Where:** Sicily, in the Western Sea (§3.9). Its port is **Katane**, a landing on the Western Sea's lanes; it opens with the Western Sea, after the Odyssey.
- **Palette and terrain:** black lava fields and gray ash; chestnut woods on the lower slopes (Etna's hundred-horse chestnut); orange lava rivers; snow on the summit above the fire; the forge's bronze and red light.
- ★ **Set piece, "The eruption":** when you wake the forge (below), Etna erupts. The screen shakes, the sky goes red, and lava pours down the lower slopes. The map changes for good: the old road through the chestnut wood is buried, a new black lava field hardens over it with a direct path up, and a cave that was under the flow opens.
- ★ **Vista, "The crater":** from the summit rim, the camera pans out over the crater: a lake of glowing lava a long way down, steam, Empedokles's sandal on a ledge, and, if you look long enough, a vast shape in the rock below the lava, breathing.

**Maps** (Western Sea; new COVERAGE area **H11**, which takes over Magmar's, Slugma's and Turtonator's lines from the Phlegraean Fields, P-15).

| Map | Kind | Size | Levels | Tier |
|---|---|---|---|---|
| `Katane` | Port town at the mountain's foot | 44×36 | — | 1.0 |
| `Etna_Slopes` | The great road: the climb, in pre- and post-eruption layouts | 40×104 | 76–78 | 1.0 |
| `Etna_Forge` | Hephaestus's forge, 3 floors | 32×32 each | 77–79 | 1.0 |
| `Etna_MagmaChambers` | Rising-magma dungeon, 2 floors | 30×30 each | 78–80 | 1.0 |
| `Etna_Crater` | The summit rim | 40×32 | 78–80 | 1.0 |

**Stops.**

| Stop | Temple, shrine or outcamp | Herm | Services |
|---|---|---|---|
| **Katane** | **The shrine of the Pious Brothers**, two statues carrying their parents | A Greek herm with soot in its cracks | Asclepeion, Agora, the Super Rod |
| **The chestnut hut** (outcamp, the Slopes' midpoint) | **A shrine of Hephaestus** at a vent | A herm of black basalt | The charcoal-burner heals |
| **The snow hut** (below the crater) | **Empedokles's altar**, with one bronze sandal on it (a copy: the real one is on the crater ledge) | A basalt herm | A heal; snow-melt water |

**The Slopes** (40×104, south to north; the great road).
1. **Katane's lava field:** old black flows with orchards growing on them, a Sicel shepherd in plain view, **band 1** in the ash grass.
2. **The Field of the Pious:** a strip of green between two old lava tongues, where the lava parted (remains, lore, and a Revive).
3. **The chestnut wood:** huge chestnut trees, the hundred-horse chestnut in a clearing, **band 2** after a charcoal-burner pair on the wood's only path (a chokepoint).
4. **The chestnut hut** (outcamp, the midpoint).
5. **The lava rivers:** live flows cross the slope. **The lava puzzle:** basalt drums (the land's skin, §5.1) pushed into a flow's channel mouth divert it into a side channel, cooling the old bed into a crossing. Three flows, three drums; one flow can only be diverted after another is.
6. **The ash cone:** a cut stair up a cinder slope, **band 3** in the high scrub after a Cyclops's apprentice smith, the snow hut, and the forge's gate in the mountain's side.
- **After the eruption:** steps 3–5 change. The chestnut wood's lower half is under new lava (a sign: the hundred-horse chestnut survived, alone in the black), a hardened lava field gives a straight road from Katane to the hut, and the **lava tube** under the old flow opens: a one-room cave with Heatmor, a Fire Stone and a Magmarizer.
- **Checks:** bands 3; mandatory trainers 4; rest: the chestnut hut; climb: the ash-cone stair and a Crook face to a fumarole ledge (a Charcoal pile); cave: the lava tube; ledges drop south.

**Hephaestus's Forge** (3 floors).
- **Floor 1, teach:** bellows plates. A drum on a plate pumps a furnace; a lit furnace melts a bronze grille.
- **Floor 2, test:** the anvils. Three Cyclopes are working (trainers: Brontes, Steropes and Arges, with Fire, Electric and Steel teams; each is a checkpoint you can't walk round). Plates pump three furnaces, but each furnace's heat closes a different door. Choose the order.
- **Floor 3, combine:** the great furnace, where the thunderbolts were forged. Pumping it **wakes the mountain**: this is the eruption's trigger. You have to run the floor's last stretch as lava floods in behind you (a timed escape; fail forward to the floor's start).
- **Rest:** a cooling trough on floor 2. **Payoff:** the **pyre-brand** (below), and Hephaestus's tripods: a Mantipod gift (§2.7's homeland line), and Hephaestus Favor +10.

**The Magma Chambers** (2 floors, after the eruption). *Rising magma.* Each floor fills from the bottom: every ten steps the magma rises a row (layout swaps by the step hook, §5.5). Climb stairs and ladders ahead of it, push drums into vents to hold it back a row, and grab what's on the low ledges before it's gone. Fail forward: the magma carries you back to the floor's start. At the bottom of floor 2, below the magma line on a second visit, **Typhon's hand**: a rock formation of enormous fingers, warm and moving very slowly.

**The Crater** (40×32). The rim walk, snow and steam; the vista (★); Empedokles's real sandal on a ledge (a Crook face down; take it and the mountain coughs: a Heat Rock); and the climb down to the Typhon chamber.

**Pokémon.**
- **Signature:** Magmar and Magmortar, Magcargo, Turtonator, Torkoal, Coalossal (a share from the Black Sea), Camerupt (a share from Libya), Heatmor in the lava tube.
- **Homeland lines (§2.7):** Pyrapod and Mantipod (Hephaestus's tripods, *Iliad* 18.373), Kolossard (Talos, Hephaestus's bronze man), and Gigantomb (the giants under Sicily).
- **Rare:** Magmortar very rare on the crater rim (80); a Gigantomb static in the magma chambers (80).
- **The legendary lead (P-15):** **Volcanion**, which LEGENDS casts as "the giant under the burning fields," moves from the Phlegraean Fields to Etna's Typhon chamber, as Typhon's breath: steam and fire together (Lv 80, LEGENDS's quest moved, not rewritten). The chamber also gives a lead to **Gaia** (Groudon, POSTGAME §3.3): Typhon was her son, and the priest says his mother is under Delphoi.
- **Gap:** Typhon himself. The dex has no Typhon. An optional new legendary (P-11's list) could be the shape in the rock; nothing waits on it.

**The tie-in: the pyre-brand.** The forge's payoff is a **pyre-brand**, a coal from Hephaestus's own fire that never goes out. It's the fire that lights Herakles's pyre on Mount Oeta (§11.3): the post-game's final boss can't be finished without the volcano. (It works anywhere Prometheus's Ember works, so players who did Labor 11 aren't punished.)

**Bosses.** The three Cyclopes (78, 78, 79); the forge's keeper, a bronze Kolossard (80, totem-boosted); Volcanion (80, LEGENDS).

---

## 11. The post-game League: the circuit, the Four of Oeta and Herakles

**The direction (user, 2026-11-17):** the post-game has its own gyms, its own Elite Four and a final boss, Herakles, "the greatest hero, deified after his Labors."

### 11.1 The circuit: the Periodos halls, each with a type

The Oikoumene already has ten champions in ten halls, with Emblems (PG-33, PERIODOS). Adding eight more gyms on top would give the post-game two parallel circuits. So **the Periodos is the gym circuit** (PROPOSAL P-12): each hall keeps its leader, venue, puzzle verb (PG-35) and Emblem, and now has **one type**, all ten different. The teams below replace PERIODOS's mixed teams; no species repeats across the ten halls, the Four of Oeta and Herakles, and Lazarus's starters stay off them (PG-5).

| # | Land | Leader | Type | Venue and verb | Lv | Team (ace last) |
|---|---|---|---|---|---|---|
| 1 | Troad | Prince Hektor | **Steel** (bronze and the wall) | The Skaian Gate: the song and the wall | 74–76 | Lucario, Excadrill, Bronzong, Kingambit, Metagross, **Aegislash** |
| 2 | Egypt | Pharaoh Proteus | **Psychic** (priests and shapes) | The precinct: catch the right shape | 74–76 | Sigilyph, Indeedee, Reuniclus, Gothitelle, Hatterene, **Alakazam** |
| 3 | Lydia | King Croesus | **Electric** (electrum, the first coins' metal) | The treasury: weigh | 75–77 | Pawmot, Luxray, Bellibolt, Rotom (Wash), Electivire, **Magnezone** |
| 4 | Libya | Kyrene | **Ground** (the Sand Sea, the chariots) | The hippodrome: drive | 75–77 | Sandaconda, Hippowdon, Krookodile, Gliscor, Flygon, **Garchomp** |
| 5 | Black Sea | Medea | **Poison** (her drugs, the Garden of Hecate) | Aietes's palace: make it young | 76–78 | Toxicroak, Roserade, Revavroom, Dragalge, Nidoqueen, **Gengar** |
| 6 | Aithiopia | King Memnon | **Fire** (the dawn) | The bath-court: slide | 78–80 | Talonflame, Pyroar, Arcanine, Torkoal, Magmortar, **Volcarona** |
| 7 | Far West | King Arganthonios | **Rock** (the silver mines) | The royal gallery: fire and vinegar | 80–82 | Crustle, Barbaracle, Lycanroc, Gigalith, Rhyperior, **Tyranitar** |
| 8 | North | Abaris | **Ice** (beyond the North Wind) | The round temple: the arrow | 80–82 | Frosmoth, Alolan Ninetales, Cetitan, Glaceon, Avalugg, **Baxcalibur** |
| 9 | Western Sea | Milo of Kroton | **Fighting** (the palaestra) | The palaestra: leap | 80–82 | Throh, Grapploct, Bewear, Hawlucha, Machamp, **Paldean Tauros (Combat)** |
| 10 | Okeanos | Rhadamanthys | **Fairy** (the Isles of the Blessed) | The tower of Kronos: petteia | 82–84 | Granbull, Clefable, Tinkaton, Azumarill, Togekiss, **Florges** |

- **Order.** The circuit is open, like the lands; the levels steer it (§2.3), so the usual order is the table's.
- **Hall trainers** take their hall's type. Helen's optional battle in Memphis keeps her team (Altaria, Espeon, Sylveon, Gardevoir, Milotic).
- **Coverage.** Ten types have a hall; Water, Flying, Dragon and Ghost have a seat on Oeta; Normal, Grass and Bug are Herakles's (his lion, his club and his beetle). **Dark** is the one type without a leader: it lives in the Underworld and the Graiai's cave (§9), the post-game's villains' ground rather than its heroes'.
- **What changes:** PERIODOS's ten teams, and its §8 note that the halls "aren't type-themed." The puzzles, venues, prizes and Emblems don't change. Ten Emblems plus the Kotinos still open the end (PG-24).

### 11.2 The Four of Oeta: the post-game Elite Four

The main story's Elite Four is the Pantheon on Olympus: four seats of the Twelve, gods' representatives (LEAGUE.md). The post-game's is different in kind: **four people from Herakles's own life,** who keep the mountain where he died. Mount Oeta stands above Trachis, near Thermopylai on the Aethos chart (AETHOS_MAP), where Herakles had his pyre built and went up to Olympus from its smoke (Sophocles, *Women of Trachis*; Apollodorus 2.7.7).

**The venue.** `Trachis`, a town at the foot (herm, Asclepeion, the Herakleia's heralds), and **the Ascent of Oeta**, the post-game's victory road: a long climb (two maps, 40×100 each) with oak forest, cliff stairs, Crook faces, a midpoint shrine of Herakles as its only heal, mandatory trainer pairs on the narrow paths (Blessed Heroes, Argonaut veterans), and four seats on four terraces, each a small hall of its own. The pyre's summit is at the top. Like the Pantheon (LEAGUE.md), the four seats lock behind you, and a whiteout sends you back to Trachis.

| Seat | Who | Type | Venue on the mountain | Lv | Team (ace last) |
|---|---|---|---|---|---|
| 1 | **Deianeira**, Herakles's wife, whom he won by wrestling the river god Achelous | **Water** | The ford of the Spercheios at the mountain's foot, where the centaur Nessos carried her and she kept his blood | 88–90 | Barraskewda, Kingdra, Toxapex, Gyarados, Dondozo, **Palafin** (its Hero Form, the hero's turn) |
| 2 | **Philoktetes**, who lit the pyre when no one else would, and got Herakles's bow | **Flying** | The bow ledge: a cliff terrace with the birds he lived on, ten years alone on Lemnos | 88–90 | Staraptor, Braviary, Skarmory, Kilowattrel, Crobat, **Salamence** |
| 3 | **Iolaus**, his nephew and charioteer, who burned the Hydra's stumps | **Dragon** | The charioteer's terrace, with braziers he keeps lit "in case of heads" | 89–91 | Noivern, Haxorus, Goodra, Kommo-o, Dragapult, **Dragonite** |
| 4 | **The Shade of Herakles**, the image that stays in Asphodel while the hero is on Olympus (*Odyssey* 11.601–627; UNDERWORLD scene 9) | **Ghost** | The smoke ledge, where the pyre's smoke still hangs | 89–91 | Mismagius, Chandelure, Ceruledge, Dusknoir, Spiritomb, **Golurk** ("what was left": a body of clay) |

- **Why these four:** each holds a piece of the hero that a song never shows: his wife's grief, his friend's loneliness, his nephew's help (the help that made a Labor "not count"), and the part of him that stayed dead. Herakles's last line makes the point: you met everything he left behind before you met him.
- **The Shade's seat** pays off UNDERWORLD's scene: the shade who counted your Labors comes up the mountain to see the end. "I came to see him go. I never have."
- **Rematches:** weekly, at +5 levels, with new aces.

### 11.3 Herakles's arc and the final battle

**The arc across the post-game.** Herakles appears in every epic, and is never met in person until the end.

| Where | What the player sees | Owner |
|---|---|---|
| The epilogue and Olympia | Kleon's "Herakles had twelve"; the wild olive he planted; Paionios carving eleven Herakleses | LABORS |
| The Labors | Each Labor is his, done again; his monsters, met and mostly caught; the Kotinos cut from his tree | LABORS |
| The Katabasis | His shade in Asphodel, counting your Labors: "Twelve? Then I can stop counting." | UNDERWORLD |
| The Periodos | His Pillars at the edge of the world; his Phoenician twin's temple at Gadeira; his footprints all round the Oikoumene | §3.8 |
| **The Pillars** | With ten Emblems and the Kotinos, he's there, on the northern Pillar, as PG-23 has it. He doesn't fight. He scratches out NE and leaves PLUS ULTRA, finishes Alethea's chart, and says: "Not here. Come where it ended for me." | §11.3, P-13 |
| **Etna** | The pyre-brand, Hephaestus's coal | §10 |
| **Mount Oeta** | The Four, then him | §11.2 |
| **Olympus** | His seat, beside Hebe: rematches | §11.3 |

**At the pyre.** The summit of Oeta is a ring of oak logs stacked for a pyre that burned once. Herakles stands in it, a god now, unhurt, in the lion skin.

```text
HERAKLES: They built this for me. I'd done twelve, and then a hundred more.

HERAKLES: A song said I'd die by a dead man's hand. I did. It's still a good song.

HERAKLES: You did my twelve with nobody telling you to. And a few hundred more.

HERAKLES: Nobody wrote you a pyre. Let's see what you're for instead.
```

**The battle: Herakles, the greatest hero.** The hardest trainer in the game: his conquered monsters, now his companions, and the one Pokémon that bears his name, which rises to Apotheosis, Ichor's Mega, the way he did.

| Species | Lv | Ability | Item | Moves | Why |
|---|---|---|---|---|---|
| Nemeleon | 94 | Fur Coat | Leftovers | Crush Claw, Bulk Up, Double-Edge, Noble Roar | The Nemean lion, his cloak (Labor 1) |
| Lernathan | 94 | Regenerator | Black Sludge | Coil, Gunk Shot, Outrage, Recover | The Hydra, whose venom tipped his arrows (Labor 2) |
| Belornis | 93 | Iron Barbs | Rocky Helmet | Brave Bird, Iron Head, Spikes, Roost | The Stymphalian flock (Labor 6) |
| Kaprodon | 93 | Reckless | Choice Band | Head Smash, Earthquake, Night Slash, Double-Edge | The Erymanthian boar (Labor 4) |
| Hierolive | 95 | Regenerator | Olive Club (LABORS §4) | Wood Hammer, Drain Punch, Swords Dance, Horn Leech | His wild-olive club |
| Heracross (Apotheosis: Mega Heracross) | 96 | Skill Link as Mega | Heracronite | Pin Missile, Rock Blast, Close Combat, Swords Dance | His name's beetle; Apotheosis is his story |

- **Spartan:** competitive sets and EVs, smart AI, the cap at his ace (BALANCE.md).
- **After:** he steps out of the pyre and hands the player the pyre-brand to light it. It burns. He goes up in the smoke, as in the myth, and the camera follows him into the clouds to Olympus, where Hebe pours him a cup. The credits' second roll: the Periodos map, the Labors' metopes, the Odyssey's true chart, one after another. Reward: the trainer card's last stamp, the Periodos as a wall map at home (OIKOUMENE §5), and the War Horn's upgrade.
- **Rematch:** at **his seat on Olympus**, above the Pantheon, once a week, at Lv **100**: the top of BALANCE.md's curve.

### 11.4 Levels and order

| Content | Wild | Trainers | Boss |
|---|---|---|---|
| The ten halls | — | 73–83 | 74–84 |
| Etna | 76–80 | 77–79 | 80 |
| The Ascent of Oeta | 82–85 | 85–88 | — |
| The Four of Oeta | — | — | 88–91 |
| The Primordials | — | — | 88 |
| The Prime Mover | — | — | 95 (a catch) |
| **Herakles** | — | — | **93–96; rematch 100** |

**The order:** the ten Emblems and the Kotinos → the Pillars → Etna (if not done) → the Primordials and the Prime Mover, as wanted → **Oeta: the Four, then Herakles, last.** The Prime Mover stays the last legendary; Herakles is the last battle. This replaces OIKOUMENE §6's Herakles at the Pillars at 86–88 with a rematch at 92 (P-13).

---

## 12. The Twelve Labors, one by one

**The user confirms:** all twelve. `LABORS.md` designs every one in full; this is the builder's summary, with the guide's additions (§4.1) and how each builds to Herakles (§11). Levels are LABORS's; bosses come from the dex casting (STORY §2; LABORS §5). The Heraion's trophy niches fill one per Labor.

| # | Labor | Where | The challenge (its verb) | Boss (casting) | Reward | Levels | Toward Herakles |
|---|---|---|---|---|---|---|---|
| 1 | **The Nemean Lion** | Nemea's sealed den (the built hook: the great boulder and the high mouth, `design/maps/Nemea.md`) | **Corner it:** seal one of the den's two mouths with a drum; inside, no Bag works | Nemeleon, 70 (with a lioness, 68), Kleon beside you | The Lion's Hide; Leo; TM Swords Dance | Wild 55–62; boss 70 | His lion leads his team |
| 2 | **The Lernaean Hydra** | The Springs of Lerna, Lakonia | **Cauterize it:** carry fire to each pool's brazier before the stump regrows | Trilerna heads 66–68; Lernathan, the golden head, 71; Hera's crab Karkitox, 70 | Lernathan (a victory catch); Hydra; it "doesn't count" | Wild 55–62; boss 71 | His second |
| 3 | **The Ceryneian Hind** | All Aethos, ending at the Ladon ford, Arkadia | **Track it** for days, without harming it | Xerneas, 72 | Xerneas, by its choice; Kallisto's apology to Kleon | Wild 57–64; boss 72 | The Labor he did by patience |
| 4 | **The Erymanthian Boar** | Erymanthos's slopes and snowfield, beside **the Erymanthian Preserve** (IDEAS's safari): after the Labor the fallen oaks clear from the High Meadow's gap and the Preserve's Boar's Thicket opens, with Kaprodon in its table (FLAG_ICHOR_ERYMANTHIAN_BOAR; design/maps/ErymanthosPreserve.md) | **Lure it** into deep snow | Kaprodon, 72 | Kaprodon (a victory catch); Atalanta's Net | Wild 57–64; boss 72 | His boar |
| 5 | **The Augean Stables** | Augeas's farm in Elis, by Olympia | **Turn two rivers** through the yard: drums on sluice plates (§4.1) | The Muck: Garbodor ×2 (70), then a giant Garbodor (73) | A stable door-pin; it "doesn't count" | Wild 60–66; boss 73 | Hyperion shovels; Herakles founded the Games after it |
| 6 | **The Stymphalian Birds** | The Stymphalian Reeds on **Lake Stymphalia**, on the road north from Lakonia (IDEAS's Routes 26–27): the Labor's map *is* the lake's marsh, built once for both | **Flush them** with Athena's rattles, then fight them in the air | Belornis, 72, and the Bronze Flock (Belornis 70, Corviknight 70) | Belornis (a victory catch); a bronze feather | Wild 60–66; boss 72 | His birds |
| 7 | **The Cretan Bull** | Knossa's shore, then the sea crossing | **Leap it, then ride it** across the sea, with Asterion's help | The Bull from the Sea: Paldean Tauros (Aqua), 73 | A hank of sea-white hair | Wild 62–67; boss 73 | — |
| 8 | **The Mares of Diomedes** | Abdera and the Bistonian Plain, Thrace (Oikoumene) | **Feed them** the right food, stall by stall | King Diomedes: Mudsdale, Borapteryx, Lykanax, Kaprodon, Taurivet (72–73) | Podarge (Mudsdale, 72); a bronze bit | Wild 62–67; boss 73 | — |
| 9 | **Hippolyta's War-Belt** (LABORS keeps "War-Belt": the Girdle of Herakles is already the Strength relic, SYSTEMS D2) | Themiskyra and the Thermodon, Black Sea | **Find the disguised goddess** stirring the camp | Queen Hippolyta: Hoplektor, Kourodin, Dorydrake, Lykanax, Hisuian Braviary (75) | The War-Belt; Hippolyta to the Olympiad | Wild 64–69; boss 75 | — |
| 10 | **The Cattle of Geryon** | Helios's cup to the Strait of the Pillars and Erytheia, the Far West | **Sail the sun's cup, set up the Pillars, then herd the cattle home** | Orthros (Dikyon, 74); Eurytion's team (73–75); Geryon (Hydreigon, 77) | Hydreigon (a victory catch); the Pillars stand; the cup | Wild 64–69; boss 77 | His Pillars, where you meet him (§11.3) |
| 11 | **The Apples of the Hesperides** | The Caucasus crag, the Garden, Atlas's Ridge | **Endure:** free Prometheus from Zeus's eagle, then hold up the sky while Atlas fetches the apples | Zeus's eagle (Aetarch, 76); Ladon (Melodrakon, 78), Kleon beside you; the Hesperides | A golden apple; Melodrakon (a victory catch); Prometheus's Ember; Draco | Wild 65–70; bosses 76–78 | Atlas's question (§3.8) |
| 12 | **Kerberos** | The Underworld, up the Ascent of Tainaron | **Escort him** up into the light without letting him look up | Kerberos: Pylakyon, 79 (Hades's: not catchable) | A three-headed collar; Hades and Hera Favor | Wild 65–70; boss 79 | The Shade sees you bring him up |
| — | **The Kotinos** | The Altis at Olympia | Olympias, at full strength | Olympias: Kynoketos, Pythoros, Hisuian Goodra, Melodrakon, Mega Altaria, Lernathan (77–80) | The Kotinos; Hercules; the Olive Club | — | The Olive Club powers Herakles's Hierolive; the Kotinos opens the Pillars |

**What the guide adds (for LABORS's designer):** §4.1's outcamps, herms, plates, the scaffold ladder and the remains; the shared Lake Stymphalia map (P-19); the Preserve's opening after Labor 4 (P-19); and the arc's end at Oeta (§11).

---

## 13. The full Odyssey

**The user confirms:** the full Odyssey, every major episode, as a sailing quest chain. `ODYSSEY.md` designs eleven steps; Homer has four more that this guide adds (**P-16**, for ODYSSEY's designer). The voyage stays one way until home (O1), at the Oikoumene's levels.

| # | Episode | Where on the chart | The test and its mechanic | Boss (casting) | Prize | Lv | Status |
|---|---|---|---|---|---|---|---|
| 0 | **The Kikones** | Ismaros, on the Thracian coast by the Hebros shore (§3.1) | **Know when to leave.** Odysseus's men lingered on the beach and lost men when the Kikones came back at dawn (*Odyssey* 9.39–61). A night raid map with a clock: get Maron's wine-jar from Apollo's priest and be back aboard before dawn, or fight the dawn wave | The Kikones' horsemen: a double battle at dawn, Mudsdale and Rapidash (73) | **Maron's wine** (9.196–211), which gives a second way out of the Cyclops's cave | 72–74 | **New**, before Maleia |
| 1 | The storm off Maleia | Off the Aethos chart | A scripted passage | — | — | — | ODYSSEY |
| 2 | The Lotus-Eaters | The Lotus Isle | Temptation to stay: lead the dazed crew back | — | The Lotus Fruit | 71–73 | ODYSSEY |
| 3 | The Cyclops's cave | Cyclops Isle | Stealth: move only while the eye is shut; leave under a ram. **New:** pour Maron's wine and the eye stays shut longer | The great Polyphant (74), if spotted | The Ram's fleece | 71–74 | ODYSSEY, plus the wine |
| 4 | Aeolus's isle | Aiolia | Trust: the bag of winds, opened within sight of home | Aeolus (optional), **Tornadus** (75) | **Aeolus's Bag** | 74–75 | ODYSSEY |
| 5 | **The Laestrygonians** | Telepylos, a harbor with a narrow mouth between cliffs (10.80–132) | **Moor outside.** Every ship that moors in the harbor is sunk by giants throwing rocks from the cliffs. Moor in the bay and the *Euploia* is safe; go in, and you escape under falling boulders (shadows on the water), dodging out of the harbor mouth | King Antiphates's giants: a trainer pair with Gigantomb and Laolith (76), on the cliff path | A Big Nugget from the abandoned wrecks inside | 75–77 | **New**, between Aiolia and Aiaia |
| 6 | Circe's island | Aiaia | Transformation: become a pig, a wolf or a lion to find your crew | **Circe** (76–78) | Mints; Circe's cup; Elpenor's oar (§4.3) | 72–78 | ODYSSEY |
| 7 | **The descent to the dead** | The Cimmerian Shore, Okeanos (§3.10), reached through fog with the Bag, as Circe directs | **Ask the dead the way.** Dig Odysseus's trench with the Trowel; the shades come. **Tiresias's shade can't prophesy,** because prophecy has ended: "I can't tell you anything. Nobody can now. Go home." Elpenor asks for his oar tomb. If the player did the Katabasis, Tiresias knows them. | — (a scene) | The way home; Elpenor's quest; the first sight of the rim, which fogs again until after the voyage | 77 | **New**; links the Katabasis (UNDERWORLD's Tiresias) and Okeanos |
| 8 | The Sirens | The Sirens' rocks | Desire: wax, the mast, or the bard; Iapetos writes their songs | Iapetos (76–78); two **Seirenade** (76) by one way | A Siren's feather | 73–78 | ODYSSEY |
| 9 | Scylla and Charybdis | The Strait | Loss: choose which | **Hexylla** or **Trybdis** (77) | Scylla's tooth or a fig branch | 73–77 | ODYSSEY |
| 10 | Helios's cattle | Thrinakia | Hunger: feed the crew without touching the cattle | — | A Sun Stone; Helios's favor | 73–75 | ODYSSEY (optional) |
| 11 | **Calypso's Ogygia** | Ogygia (§3.9), in the Outer Sea | **Refuse for ever.** Calypso offers to make you deathless and keep you. Hermes comes (a theoxenia tell: the stranger who knows your name) to say you may go. Build a raft from Ogygia's trees (the Sickle and the Hammer, four parts), and sail it, alone, to Scheria. Poseidon's storm wrecks it; a white bird drops a veil (Leukothea, ODYSSEY's Lugia cameo) | — (a choice; staying gives a false ending, as the Lotus does, and loads the last save) | Calypso's gift: a Mystic Water, and "Everyone leaves. I like that they can, now." | 79 | **New**; replaces the empty stretch of the Outer Sea. **Proteus's islet** (Haligeron, theoxenia E13) stays on the way |
| 12 | The Phaeacians | Scheria (Kerkyra) | Rest: the bard sings your voyage | The Phaeacian games (optional, 75–77) | The Phaeacian keel | 75–77 | ODYSSEY |
| 13 | **The homecoming and the suitors** | **Kalliste: the mist beach, then Elaia** | The beggar's disguise; **Nostail**, Argos, knows you first; the twelve axes (twelve suitors, no healing); your mother's question | Twelve suitors (74–81), the last two as a double with Kleon | Melitta's Cloak, lined; Argos joins you | 74–81 | ODYSSEY, approved (O3, O4) |

**Ithaca.** The user's brief names the homecoming to Ithaca and the suitors. In Ichor that homecoming is already built into the approved story: **the player's home island plays Ithaca**, Mom plays Penelope, and the suitors sit in her house (STORY §3; ODYSSEY §1, O3, O4). This guide keeps it (P-17) and adds **Ithaka itself** as an optional visit after the voyage (it's on the Aethos chart's Route 33, AETHOS_MAP): Odysseus's own house, the real loom, Penelope, and the olive-tree bed. Penelope asks how your mother did the loom trick. "Better than me, by the sound of it." Reward: Penelope's shuttle, a decoration, and the Odysseus rematch moves to his own hall.

**The Odyssey's monsters, all placed:** Polyphant (the Cyclops), Seirenade (the Sirens), Hexylla (Scylla), Trybdis (Charybdis), Haligeron (Proteus, on his islet), Nostail (Argos); plus the guide's Gigantomb and Laolith for the Laestrygonians.

---

## 14. The additions in the build order and the budget

**Build order (§7.2), extended:**
- **Etna** builds with the Western Sea's towns (step 8), as its own three-helper chunk: art (the `etna` lava set: flows, cooled flows, chestnut trees, the forge, the crater, the magma rise states), roads (the Slopes in two layouts, the lava-tube cave), and dungeons (the forge, the magma chambers, the crater).
- **The Garden of Hecate and the Isle of Ares** join the Black Sea (step 4); **Gargaros's storm state** joins the Troad (step 1).
- **The retyped halls** (P-12) change only PERIODOS's party data: whoever builds each hall builds its typed team.
- **Mount Oeta** (Trachis, the Ascent of Oeta, four seats, the pyre) comes **last**, after Okeanos (step 11), with two helpers: maps and seats, then scenes and parties. Its trainers need ids from the shared reserve (820–863, PG-38): the Four, Herakles, their rematches and the Ascent's trainers are about 22.
- **The Labors and the Odyssey** stay on PG-2's epic order. The Odyssey's four new episodes (P-16) are one chunk for ODYSSEY's builder: Ismaros, Telepylos, the Nekyia's trench (on the Cimmerian Shore's map, built early in a fogged state) and Ogygia's raft quest (on §3.9's Ogygia map, built early too).

**Levels:** §11.4 replaces §2.3's Herakles row: the Four 88–91, Herakles 93–96, his rematch 100.

**ROM:**

| Addition | 1.0 |
|---|---:|
| Etna: five maps, the `etna` set, the eruption and magma states, the Cyclopes | ~170 KiB |
| The Garden of Hecate, the Isle of Ares at 1.0, Gargaros's storm state | ~60 KiB |
| Mount Oeta: Trachis, two climb maps, four seats, the pyre; five new trainer sprites and portraits; the ascension scene | ~180 KiB |
| The Odyssey's four episodes (maps, scripts, the raft) | ~150 KiB |
| The retyped halls | ~0 |
| The Labors in full | already in LABORS's estimate |
| **Total added** | **~0.55 MiB** |

With §6.3's ~4.1 MiB, the whole post-game at 1.0 is about **4.7 MiB of the 9.0 MiB free**, leaving about 4.3 MiB for the rest of the main game and its music.

**New proposals** (they join §8's table):

| # | Proposal | Changes | Recommendation |
|---|---|---|---|
| **P-12 ★** | **The Periodos is the post-game gym circuit,** each hall with one type, all ten different, with new teams (§11.1) | PERIODOS's teams and its §8 note; PG-33 stands otherwise | Yes |
| **P-13 ★** | **Herakles's final battle moves to Mount Oeta's pyre,** after the Four of Oeta, at 93–96 with a rematch at 100 on his seat on Olympus. He still meets you at the Pillars with the ten Emblems and the Kotinos, and finishes the chart there, but doesn't fight | **PG-23** (Herakles at the Pillars as the capstone fight), OIKOUMENE §6's 86–88 and rematch 92 (which was kept under Arceus) | Yes. It makes him the final boss the user asked for, and Oeta is where his myth ends |
| P-14 | **The Four of Oeta,** a post-game Elite Four (Deianeira, Philoktetes, Iolaus, the Shade of Herakles), and Trachis and the Ascent of Oeta as new Aethos post-game maps | AETHOS_MAP's unbuilt Thermopylai area; LEAGUE's Pantheon unchanged | Yes |
| P-15 | **Etna** as a new Western Sea dungeon and the Fire crown; **Volcanion's quest moves** from the Phlegraean Fields to Etna's Typhon chamber; a new COVERAGE area H11 takes the Magmar, Slugma and Turtonator lines; the pyre-brand ties it to Herakles | LEGENDS §4.12's place; `coverage.py`'s overrides | Yes |
| P-16 | **The Odyssey's four missing episodes:** the Kikones (with Maron's wine), the Laestrygonians, the descent to the dead at the Cimmerian Shore, and Calypso's Ogygia | ODYSSEY's step list and maps (for its designer); OIKOUMENE §4.9's note that the route skips Ogygia | Yes |
| P-17 | **Ithaca:** keep the approved homecoming at Elaia (Kalliste plays Ithaca, Mom plays Penelope), and add Ithaka as an optional visit after the voyage | Nothing approved; adds one map on Route 33 | Yes |
| P-18 | **Three new biomes** so every type has a crown: the Garden of Hecate (Poison), the Isle of Ares moved to 1.0 (Flying), Gargaros's storm summit (Electric) | OIKOUMENE §13's stretch list (the Isle of Ares); COVERAGE gains E10 | Yes |
| P-19 | **Shared places with the Labors:** Labor 6's Stymphalian Reeds are Lake Stymphalia's marsh on Routes 26–27 (IDEAS), and Labor 4's slopes open the Erymanthian Preserve's high meadow | LABORS's maps 6, 7 and 10 (for its designer) | Yes |

---

## 15. The legendary register

**The direction (user, 2026-11-17):** "post-game needs all the legendaries, and small quests for each," with "some in the original region, others in the new."

**What this is.** One table of every legendary and mythical in Ichor: the 125 National Dex legends, mythicals, Ultra Beasts and Paradox Pokémon, and the Aethos dex's own 11. Each row gives its region, where it lives (for Aethos, the WORLD_EXPLORATION return gate that leads to it), its quest, its level, what it needs, and the legends it links to.

**Where the quests live.** `design/LEGENDS.md` already gives most legends a quest of three to six steps: someone who asks, a clue trail, a task or puzzle, a trigger, and a staged encounter, with no two quests built the same way (LEGENDS §0). Those rows point to it. Some legends had no quest of their own (the epics' Primordials and Titans, the story's own legends), and this guide moves or extends a few. Those get their quests in §15.2.

**The split (user: "some in the original region, others in the new"):**

| Region | Legends | Share |
|---|---:|---:|
| **Aethos**, behind the return gates and in the Aethos epics (the Katabasis, Atlantis, Olympia, Olympus, the Labors) | **53** | 39% |
| **The Oikoumene**, in the ten lands and the Odyssey's sea | **83** | 61% |
| **All** | **136** | |

That's roughly the third and two thirds the user asked for. Going home pays: Aethos's return gates now lead to the Primordials, the Titans, the colossi, Pegaunos, Ichorin, Heatran, the Golden Paradox Pokémon, Uxie under Lebadeia and Diancie on Kalliste.

**Every land has legends** (Oikoumene rows by land): Troad 9, Black Sea 9, Egypt 9, North 8, Aithiopia 8, Libya 8, Lydia 6, Western Sea 4 with Tornadus, Far West 2, and Okeanos 16. The wanderers, Latios and the evolutions cross land lines.

**The headline legend for each big set piece:**

| Set piece | Headline | With it |
|---|---|---|
| **Etna** (§10) | Volcanion, in Typhon's chamber | Gaia's lead (Groudon) |
| **The Underworld** | Giratina, in the Chasm | The five Titans and Regigigas; Cresselia and Darkrai |
| **The Selvage** | Palkia | The Ultra Beasts; the Iron Paradox Pokémon |
| **Hyperborea** | Calyrex, at the round temple | Kyurem and Glastrier in the Cave of Boreas |
| **Atlantis** | Lugia, in the abyss | Kyogre at the world's edge; Manaphy |
| **Olympus's summit** | Arceus | Rayquaza, Pegaunos, Olympanax |
| **The Gates of the Sun** | Dialga | — |
| **The Isles of the Blessed** | Koraidon | The Tapus, Shaymin, Keldeo |
| **Heliopolis** | Ho-Oh | The three Golden beasts |
| **The Gate of Dawn** | Solgaleo | Genesect, Pheromosa |
| **The Atlas Range** | Jirachi | Moltres |
| **Leuke** | Zacian and Zamazenta | Achilles |

**The user's examples, checked against what's approved:**
- *Groudon or Kyogre in Okeanos's world-river:* Kyogre is Oceanus, at the edge of the world below Atlantis (POSTGAME §3.3), the same river seen from the Aethos side of the disc (OIKOUMENE §1). Kept.
- *Heatran in Etna's crater, or "Etna-class fire under Kaldera":* the second, the user's later example, is already LEGENDS's (S2). Heatran stays under Kaldera, and Etna's headline is Volcanion (P-15).
- *The Regis as Daedalus's or Talos's automata:* the user settled the Regis as Tartarus's freed Titans (UNDERWORLD, K3), so they stay. The automata roles go to Type: Null (Daedalus's statue that runs away), Magearna (Hephaestus's golden handmaid) and Genesect (Tithonus in his armor).
- *Ho-Oh as the phoenix at Heliopolis:* kept (LEGENDS §3.2).
- *Lugia in the Clashing Rocks' deep:* Lugia stays in Atlantis (PITCH §6, POSTGAME §3.2). A **sighting** is added: in the Clashing Rocks' side channel (§3.3), a white shape passes under the boat, and Phineus says it's going west. It's the first clue in Lugia's quest (§15.2).
- *The Swords of Justice with the Argonauts:* LEGENDS casts them as the Hours (Good Order, Justice, Peace) and Keldeo as Astraea. Kept. The Argo's Road (P-8) passes two of their homes, and each mooring stone's rubbing names the Hour of that land.

### 15.1 The register

Grouped into chains: trios, pairs and families come together, and each row says which legends it links to. **Bold** gate ids are this guide's moves (P-20).

#### The Primordials and the Prime Mover

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 383 | Groudon | **Aethos** | D8, the Korykian cave's inner grotto | §15.2 *Gaia's Navel* | 88 | The Katabasis | The Primordials; Arceus; Typhon's lead at Etna (§10) |
| 382 | Kyogre | **Aethos** | Atlantis (P2), below the abyss | §15.2 *The River That Runs in a Circle* | 88 | Atlantis | The Primordials; Lugia; Arceus |
| 384 | Rayquaza | **Aethos** | D11, above the cloud meadows | §15.2 *The One Who Held the Sickle* | 88 | The Kotinos | The Primordials; Pegaunos; Arceus |
| 493 | Arceus | **Aethos** | Olympus's true summit (§4.6) | §15.2 *Stand Still* | 95 | The four keys, the three Primordials | All three Primordials; the four epics' keys |

#### The sea of Atlantis

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 249 | Lugia | **Aethos** | Atlantis (P2), the abyss; first seen in ODYSSEY's storm | §15.2 *The White Bird* | 80 | Atlantis | Kyogre; Manaphy |
| 490 | Manaphy | **Aethos** | Atlantis's coral nursery (P2) | §15.2 *The Prince's Egg* | — | Atlantis | Phione; Lugia |
| 489 | Phione | **Aethos** | Breed Manaphy with the Ditto of Pharos (§3.5) | §15.2 (by breeding) | — | — | Manaphy |

#### The Underworld (headline: Giratina)

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 487 | Giratina | **Aethos** | The Chasm, below Tartarus | §15.2 *Upside Down* | 80 | The Katabasis | Dialga and Palkia; Arceus |
| 377 | Regirock | **Aethos** | P5 Tainaron or I13 Eleusa's Ploutonion; Tartarus's five cells | §15.2 *The Relics' Exam* | 75 | The Katabasis | The five Titans; Regigigas |
| 378 | Regice | **Aethos** | P5 Tainaron or I13 Eleusa's Ploutonion; Tartarus's five cells | §15.2 *The Relics' Exam* | 75 | The Katabasis | The five Titans; Regigigas |
| 379 | Registeel | **Aethos** | P5 Tainaron or I13 Eleusa's Ploutonion; Tartarus's five cells | §15.2 *The Relics' Exam* | 75 | The Katabasis | The five Titans; Regigigas |
| 894 | Regieleki | **Aethos** | P5 Tainaron or I13 Eleusa's Ploutonion; Tartarus's five cells | §15.2 *The Relics' Exam* | 75 | The Katabasis | The five Titans; Regigigas |
| 895 | Regidrago | **Aethos** | P5 Tainaron or I13 Eleusa's Ploutonion; Tartarus's five cells | §15.2 *The Relics' Exam* | 75 | The Katabasis | The five Titans; Regigigas |
| 486 | Regigigas | **Aethos** | Tartarus's inner gate | §15.2 *The Keeper of the Gate* | 80 | All five Titans | All five Titans; Briareus |
| 488 | Cresselia | **Aethos** | The House of Night (PG-26) | §15.2 *Horn and Ivory* | 78 | The Katabasis | Each other; the Land of Dreams (§3.10) |
| 491 | Darkrai | **Aethos** | The House of Night (PG-26) | §15.2 *Horn and Ivory* | 78 | The Katabasis | Each other; the Land of Dreams (§3.10) |

#### Olympia, Olympus and the story's own

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 494 | Victini | **Aethos** | Olympia, the Nike's pillar | §15.2 *Nike Comes Down* | 80 | All five Olympiad gold symbols | Kairazor |
| 147 | Kairazor | **Aethos** | Olympia's altar of Kairos | §15.2 *Try Twice* | 78 | — | Kronolith; Celebi |
| 148 | Pegaunos | **Aethos** | D11, above the Ascent's clouds | §15.2 *The Bridle* | 80 | — | Bellerophon's chain (I2, I3, T9, D11); Rayquaza |
| 149 | Olympanax | **Aethos** | D12, the Ascent's storm terrace | §15.2 *The Three Lots* | 80 | — | Pontanax, Nekranax: the three lots |
| 150 | Pontanax | **Aethos** | K6, G1, A5, G2, then Atlantis's temple | §15.2 *The Three Lots* | 80 | — | The three lots; Kyogre |
| 151 | Nekranax | **Aethos** | I13, then the vault beneath Hades's hall | §15.2 *The Three Lots* | 80 | — | The three lots; Giratina |
| 152 | Ichorin | **Aethos** | G12, the Pool of Mnemosyne's floor | §15.2 *The First Myth* | 70 | — | Uxie (memory); the Katabasis |
| 146 | Kronolith | **Aethos** | The deep under the Omphalos | §15.2 *Give It Back* | 60 | — | Kairazor; Dialga; the three lots |
| 143–145 | Nemira, Lotira, Thanira | **Aethos** | The three Fates' sanctuaries | §15.2 *Three Sanctuaries* | 60 | — | Kronolith; the Cutter guides the Katabasis |
| 98 | Asterlorn | **Aethos** | Knossa, after Ariadne's gold symbol | LABYRINTH §10 | 60 | — | Type: Null; Labor 7's bull |
| 716 | Xerneas | **Aethos** | All Aethos, ending at the Ladon ford, Arkadia | LABORS Labor 3 (§12) | 72 | The Labors | Yveltal; Zygarde |

#### The Eagles of the Edges

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 144 | Articuno | Oikoumene | North: the Feather Wastes | LEGENDS §3.1 | 75 | Ship | Zapdos, Moltres |
| 145 | Zapdos | Oikoumene | Troad: Gargaros's storm crown (§9) | LEGENDS §3.1 | 75 | Ship | Articuno, Moltres |
| 146 | Moltres | Oikoumene | Far West: the Atlas Range at sunset | LEGENDS §3.1 | 75 | Labor 10, or the Odyssey | Articuno, Zapdos |

#### The Three Shares and the Phoenix

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 243 | Raikou | Oikoumene | Egypt, Libya, Aithiopia (omens) | LEGENDS §3.2 | 72 | Ship | Entei, Suicune, then Ho-Oh; Raging Bolt |
| 244 | Entei | Oikoumene | Troad, Lydia, Black Sea (omens) | LEGENDS §3.2 | 72 | Ship | Raikou, Suicune, then Ho-Oh; Gouging Fire |
| 245 | Suicune | Oikoumene | Thrace, the North, the West (omens) | LEGENDS §3.2 | 72 | Ship | Raikou, Entei, then Ho-Oh; Walking Wake |
| 250 | Ho-Oh | Oikoumene | Egypt: Heliopolis | LEGENDS §3.2 | 78 | The three wanderers | The three wanderers; the Golden beasts |

#### The Charioteer, then Time and Room

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 480 | Uxie | **Aethos** | **T7**, Lebadeia's oracle descent (moved, P-20) | §15.2 *Lethe, Then Mnemosyne* | 70 | Ship | Mesprit, Azelf; Ichorin; Dialga, Palkia |
| 481 | Mesprit | Oikoumene | Libya: Lake Tritonis | LEGENDS §3.3 | 70 | Ship | Uxie, Azelf |
| 482 | Azelf | Oikoumene | North: Lake Maeotis (at 1.0, the Steppe Road's marsh end) | LEGENDS §3.3 | 70 | Ship | Uxie, Mesprit |
| 483 | Dialga | Oikoumene | Okeanos: the Gates of the Sun | LEGENDS §3.5 | 80 | The Charioteer | Palkia; Giratina; Kronolith |
| 484 | Palkia | Oikoumene | Okeanos: the Selvage (its headline) | LEGENDS §3.5 | 80 | The Charioteer | Dialga; Giratina; the Ultra Beasts |

#### The Twin Lights

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 380 | Latias | **Aethos** | D1, Lakonia's Kranai islet; then the sea lanes, even days | LEGENDS §3.4 | 72 | Ship | Latios; Gemini |
| 381 | Latios | Oikoumene | The Oikoumene's sea lanes, odd days | LEGENDS §3.4 | 72 | Ship | Latias; Gemini |

#### The Hours of Justice

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 638 | Cobalion | Oikoumene | Lydia: Sardis, with Solon | LEGENDS §3.7 | 74 | Ship | Terrakion, Virizion, then Keldeo; Iron Crown |
| 639 | Terrakion | Oikoumene | Libya: Ammonion | LEGENDS §3.7 | 74 | Ship | Cobalion, Virizion, then Keldeo; Iron Boulder |
| 640 | Virizion | Oikoumene | Aithiopia: Meroë | LEGENDS §3.7 | 74 | Ship | Cobalion, Terrakion, then Keldeo; Iron Leaves |
| 647 | Keldeo | Oikoumene | Okeanos: the Isles of the Blessed | LEGENDS §3.7 | 75 | The three Hours | The three Hours |

#### Life, death and the first clay

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 717 | Yveltal | Oikoumene | Black Sea: the Isle of Ares (1.0 under P-18) | LEGENDS §3.8 | 80 | `LABORS.md` Labors 6 and 9 | Xerneas; Zygarde |
| 151 | Mew | Oikoumene | Black Sea: the Caucasus (at 1.0, a cave room off LABORS's crag) | LEGENDS §3.8 | 75 | `LABORS.md` Labor 11 (Prometheus freed) | Mewtwo; Prometheus (Labor 11) |
| 150 | Mewtwo | Oikoumene | Okeanos: the Gorgons' Isle | LEGENDS §4.2 | 90 | The Cave of the Graiai; ODYSSEY's Mirror of Truth | Mew; the Graiai; the Mirror of Truth |
| 718 | Zygarde | Oikoumene | Egypt: Abydos (Memphis at 1.0); cells in every land | LEGENDS §4.9 | 78 | Ship | Xerneas, Yveltal |

#### What came out of the Bag

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 641 | Tornadus | Oikoumene | The wine-dark sea (ODYSSEY) | ODYSSEY §6.4 (§13) | 75 | The Odyssey | Thundurus, Landorus, Enamorus |
| 642 | Thundurus | Oikoumene | Libya: the Sand Sea's storms | LEGENDS §3.9 | 76 | The Odyssey (Aiolia) | Tornadus, then Landorus, then Enamorus |
| 645 | Landorus | Oikoumene | Aithiopia: the Table of the Sun | LEGENDS §3.9 | 76 | Thundurus | Thundurus, then Enamorus |
| 905 | Enamorus | **Aethos** | S10, Kythera's spring of Kallirhoe | LEGENDS §3.9 | 76 | Landorus | Landorus; Kythera's sea caves (S7, S21) |

#### The Truth and the Glory

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 643 | Reshiram | Oikoumene | Egypt: Memphis, with Alethea | LEGENDS §3.10 | 80 | Ship; Alethea | Zekrom; Kyurem |
| 644 | Zekrom | Oikoumene | Troad: the Skaian Gate, with Kleon | LEGENDS §3.10 | 80 | Ship; Kleon | Reshiram; Kyurem |
| 646 | Kyurem | Oikoumene | North: the Cave of Boreas (Hyperborea's headline, with Calyrex) | LEGENDS §3.10 | 82 | Reshiram or Zekrom | Reshiram or Zekrom |

#### The Keepers of the Isles

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 785 | Tapu Koko | Oikoumene | Okeanos: the Isles of the Blessed | LEGENDS §3.11 | 76 | The Isles | The four Tapus; Shaymin |
| 786 | Tapu Lele | Oikoumene | Okeanos: the Isles of the Blessed | LEGENDS §3.11 | 76 | The Isles | The four Tapus; Shaymin |
| 787 | Tapu Bulu | Oikoumene | Okeanos: the Isles of the Blessed | LEGENDS §3.11 | 76 | The Isles | The four Tapus; Shaymin |
| 788 | Tapu Fini | Oikoumene | Okeanos: the Isles of the Blessed | LEGENDS §3.11 | 76 | The Isles | The four Tapus; Shaymin |

#### Hyperion's children

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 789 | Cosmog | **Aethos** | Kaldera, from Hyperion (by S2) | LEGENDS §3.12 | 42 (gift) | League | Solgaleo, Lunala, Necrozma |
| 790 | Cosmoem | **Aethos** | Evolve Cosmog | LEGENDS §3.12 | — | — | — |
| 791 | Solgaleo | Oikoumene | Aithiopia: the Gate of Dawn (its headline) | LEGENDS §3.12 | 80 | Cosmog | Lunala; Necrozma |
| 792 | Lunala | Oikoumene | Lydia: Mount Latmos (at 1.0, Tmolus's summit by night) | LEGENDS §3.12 | 80 | Cosmog | Solgaleo; Necrozma |
| 800 | Necrozma | Oikoumene | Lydia: the Halys ford | LEGENDS §3.12 | 85 | Solgaleo and Lunala | Solgaleo and Lunala |

#### The Shield With the World on It

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 888 | Zacian | Oikoumene | Black Sea: Leuke, with Achilles | LEGENDS §3.13 | 85 | Ship; Achilles | Each other; Achilles's choice |
| 889 | Zamazenta | Oikoumene | Black Sea: Leuke, with Achilles | LEGENDS §3.13 | 85 | Ship; Achilles | Each other; Achilles's choice |

#### The Straw Offerings (Hyperborea's headline)

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 898 | Calyrex | Oikoumene | North: the round temple, Hyperborea | LEGENDS §3.14 | 80 | Ship | Glastrier, Spectrier |
| 896 | Glastrier | Oikoumene | North: the Cave of Boreas | LEGENDS §3.14 | 78 | Calyrex's quest | Calyrex |
| 897 | Spectrier | Oikoumene | Okeanos: the Cimmerian Shore | LEGENDS §3.14 | 78 | Calyrex's quest | Calyrex |

#### What Stayed in the Jar

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 1001 | Wo-Chien | Oikoumene | North: the Steppe Road | LEGENDS §3.15 | 78 | Ship; Elpis | The four Treasures; Elpis |
| 1002 | Chien-Pao | Oikoumene | Lydia: Sardis's treasury | LEGENDS §3.15 | 78 | Ship; Elpis | The four Treasures; Elpis |
| 1003 | Ting-Lu | Oikoumene | Aithiopia: the Fountain of the Long-Lived | LEGENDS §3.15 | 78 | Ship; Elpis | The four Treasures; Elpis |
| 1004 | Chi-Yu | Oikoumene | Troad: Ilion | LEGENDS §3.15 | 78 | Ship; Elpis | The four Treasures; Elpis |

#### The Satyr Play Nobody Wrote

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 1017 | Ogerpon | **Aethos** | T2, Thyrsa: Silenos's cellar and the vineyards | LEGENDS §7.6 | 76 | League | The Thyrsa five |
| 1014 | Okidogi | **Aethos** | T2, Thyrsa: Silenos's cellar and the vineyards | LEGENDS §7.6 | 74 | League; the Anthesteria | The Thyrsa five |
| 1015 | Munkidori | **Aethos** | T2, Thyrsa: Silenos's cellar and the vineyards | LEGENDS §7.6 | 74 | League | The Thyrsa five |
| 1016 | Fezandipiti | **Aethos** | T2, Thyrsa: Silenos's cellar and the vineyards | LEGENDS §7.6 | 74 | League | The Thyrsa five |
| 1025 | Pecharunt | **Aethos** | T2, Thyrsa: Silenos's cellar and the vineyards | LEGENDS §7.6 | 78 | League; the Anthesteria | The Thyrsa five |

#### Fire, forges and makers

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 485 | Heatran | **Aethos** | **S2**, Kaldera's vent boulder: the fire under the forge | LEGENDS §7.2 | 72 | League | Volcanion (Etna); Magearna |
| 721 | Volcanion | Oikoumene | Western Sea: **Etna's** Typhon chamber (moved, P-15; the Fire crown's headline) | LEGENDS §4.12, moved (§10) | 80 | Odyssey | Heatran; Groudon (Gaia, Typhon's mother) |
| 801 | Magearna | **Aethos** | Kaldera's forge (S2), with a Lemnos lead (S14) | LEGENDS §7.4 | 75 | Hephaestus Favor 100 | Heatran; Hephaestus Favor |
| 772 | Type: Null | **Aethos** | Knossa, Daedalus's workshop; its memories in the Minoan vaults (C1, C3, C6, S1, S6, D3, A13) | LEGENDS §7.3 | 70 (gift) | League | Silvally; Asterlorn |
| 773 | Silvally | **Aethos** | Evolve Type: Null | LEGENDS §7.3 | — | — | Type: Null |
| 808 | Meltan | Oikoumene | Black Sea: the Chalybes' forges | LEGENDS §4.14 | 70 | Ship | Melmetal; Miraidon |
| 809 | Melmetal | Oikoumene | Black Sea: the great furnace | LEGENDS §4.14 | 80 | 40 Meltan's iron | Meltan |
| 649 | Genesect | Oikoumene | Aithiopia: Eos's palace | LEGENDS §4.8 | 75 | Ship | Solgaleo; Memnon |
| 807 | Zeraora | Oikoumene | Lydia: Miletos (at 1.0, Thales lodges at Sardis) | LEGENDS §4.13 | 75 | Ship | Necrozma (the eclipse) |

#### Sky, stars and fallen things

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 385 | Jirachi | Oikoumene | Far West: the Atlas Range's summit | LEGENDS §4.3 | 75 | All 24 constellations (SYSTEMS §8) | All 24 constellations |
| 386 | Deoxys | Oikoumene | Troad: Ilion's temple of Athena | LEGENDS §4.4 | 78 | Ship | The Palladion; the Tomb of Ilos (§3.1) |
| 719 | Diancie | **Aethos** | **K9**, Ariadne's door on Kalliste (moved, P-20): Naxos is where Dionysus crowned her | §15.2 *The Crown's Last Stone*, moved | 74 | Corona Borealis (LABYRINTH) | Corona Borealis; Asterlorn |
| 890 | Eternatus | Oikoumene | Libya: the Glass Crater | LEGENDS §4.15 | 92 | Eight Periodos panels | Eight Periodos panels |
| 720 | Hoopa | Oikoumene | Lydia: the Chasm of Gyges | LEGENDS §4.11 | 76 | Ship | The Mirror of Truth (§3.2) |

#### Singles of the lands

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 492 | Shaymin | Oikoumene | Okeanos: the Isles, at the Pyanopsia | LEGENDS §4.5 | 70 | The Isles | The Tapus |
| 648 | Meloetta | Oikoumene | Troad: the Hebros's mouth (the Elaious shore at 1.0); its lead starts at Arkadia's G8 | LEGENDS §4.7 | 72 | Orpheus amphora (SYSTEMS §5); Lyre of Apollo | Orpheus (UNDERWORLD) |
| 802 | Marshadow | **Aethos** | Elaia, then **G11**, Lykaion's shadowless precinct (P-20) | LEGENDS §7.5, extended (§15.2) | 75 | The theoxenia finale | The theoxenia finale |
| 251 | Celebi | **Aethos** | Akti, the fractures, then **T6**, the Kopais mist (P-20) | LEGENDS §7.1, extended (§15.2) | 70 | Five fractures visited | Kairazor; the Time Fractures |
| 891 | Kubfu | Oikoumene | Western Sea: Kroton, from Milo | LEGENDS §4.16 | 70 (gift) | Odyssey | Urshifu |
| 892 | Urshifu | Oikoumene | Evolve Kubfu | LEGENDS §4.16 | — | — | Kubfu |
| 893 | Zarude | Oikoumene | Aithiopia: the Mountains of the Moon | LEGENDS §4.17 | 76 | Ship | Dionysus (Nysa) |
| 1024 | Terapagos | Oikoumene | Western Sea: Elea | LEGENDS §4.18 | 90 | Odyssey | Achilles |

#### The Time Fractures

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 984 | Great Tusk | **Aethos** | K1, Kronion Hill: its fracture | LEGENDS §5 | 66–70 | League | The Golden Age; Koraidon |
| 989 | Sandy Shocks | **Aethos** | K1, Kronion Hill: its fracture | LEGENDS §5 | 66–70 | League | The Golden Age; Koraidon |
| 985 | Scream Tail | **Aethos** | I12, Eleusa: its fracture | LEGENDS §5 | 66–70 | League | The Golden Age; Koraidon |
| 986 | Brute Bonnet | **Aethos** | I12, Eleusa: its fracture | LEGENDS §5 | 66–70 | League | The Golden Age; Koraidon |
| 987 | Flutter Mane | **Aethos** | D7, Delphoi: its fracture | LEGENDS §5 | 66–70 | League | The Golden Age; Koraidon |
| 988 | Slither Wing | **Aethos** | S3, Kaldera's burnt islet: its fracture | LEGENDS §5 | 66–70 | League | The Golden Age; Koraidon |
| 1005 | Roaring Moon | **Aethos** | D3, Lakonia on Taygetos: its fracture | LEGENDS §5 | 66–70 | League | The Golden Age; Koraidon |
| 1009 | Walking Wake | Oikoumene | Egypt: Heliopolis's fracture | LEGENDS §5 | 74–78 | Ho-Oh | Its wanderer; Ho-Oh; Koraidon |
| 1020 | Gouging Fire | Oikoumene | Egypt: Heliopolis's fracture | LEGENDS §5 | 74–78 | Ho-Oh | Its wanderer; Ho-Oh; Koraidon |
| 1021 | Raging Bolt | Oikoumene | Egypt: Heliopolis's fracture | LEGENDS §5 | 74–78 | Ho-Oh | Its wanderer; Ho-Oh; Koraidon |
| 990 | Iron Treads | Oikoumene | Black Sea: the Chalybes: its fracture | LEGENDS §5 | 74–78 | Ship | The Iron Age; Miraidon |
| 992 | Iron Hands | Oikoumene | Black Sea: the Chalybes: its fracture | LEGENDS §5 | 74–78 | Ship | The Iron Age; Miraidon |
| 991 | Iron Bundle | Oikoumene | North: the Cave of Boreas: its fracture | LEGENDS §5 | 74–78 | Ship | The Iron Age; Miraidon |
| 993 | Iron Jugulis | Oikoumene | Libya: the Glass Crater: its fracture | LEGENDS §5 | 74–78 | Ship | The Iron Age; Miraidon |
| 994 | Iron Moth | Oikoumene | Libya: the Glass Crater: its fracture | LEGENDS §5 | 74–78 | Ship | The Iron Age; Miraidon |
| 995 | Iron Thorns | Oikoumene | Troad: the Walls of Laomedon: its fracture | LEGENDS §5 | 74–78 | Ship | The Iron Age; Miraidon |
| 1006 | Iron Valiant | Oikoumene | Troad: the Walls of Laomedon: its fracture | LEGENDS §5 | 74–78 | Ship | The Iron Age; Miraidon |
| 1010 | Iron Leaves | Oikoumene | Okeanos: the Selvage: its fracture | LEGENDS §5 | 74–78 | Keldeo | The Iron Age; Miraidon |
| 1022 | Iron Boulder | Oikoumene | Okeanos: the Selvage: its fracture | LEGENDS §5 | 74–78 | Keldeo | The Iron Age; Miraidon |
| 1023 | Iron Crown | Oikoumene | Okeanos: the Selvage: its fracture | LEGENDS §5 | 74–78 | Keldeo | The Iron Age; Miraidon |
| 1007 | Koraidon | Oikoumene | Okeanos: the Isles of the Blessed | LEGENDS §5 | 85 | All eleven fractures | All eleven fractures; Miraidon |
| 1008 | Miraidon | Oikoumene | Black Sea: the great furnace | LEGENDS §5 | 85 | All eleven fractures | All eleven fractures; Koraidon |

#### Beyond the Selvage

| # | Pokémon | Region | Where (for Aethos, the return gate) | Quest | Lv | Needs | Links |
|---:|---|---|---|---|---|---|---|
| 793 | Nihilego | Oikoumene | Okeanos: the Selvage, north | LEGENDS §6 | 74 | Lotira | The Peratai; Palkia; Lotira |
| 794 | Buzzwole | Oikoumene | Egypt: the Delta Reeds | LEGENDS §6 | 74 | Lotira | The Peratai; Palkia; Lotira |
| 795 | Pheromosa | Oikoumene | Aithiopia: the Gate of Dawn | LEGENDS §6 | 74 | Lotira | The Peratai; Palkia; Lotira |
| 796 | Xurkitree | Oikoumene | Libya: the Sand Sea | LEGENDS §6 | 74 | Lotira | The Peratai; Palkia; Lotira |
| 797 | Celesteela | Oikoumene | North: the Hyperborean Meadow | LEGENDS §6 | 76 | Lotira | The Peratai; Palkia; Lotira |
| 798 | Kartana | Oikoumene | Egypt: the Great Pyramid (Y8 at 1.0) | LEGENDS §6 | 74 | Lotira | The Peratai; Palkia; Lotira |
| 799 | Guzzlord | Oikoumene | Aithiopia: the Table of the Sun | LEGENDS §6 | 78 | Lotira | The Peratai; Palkia; Lotira |
| 803 | Poipole | Oikoumene | Okeanos: the Selvage | LEGENDS §6 | 70 (gift) | Lotira | The Peratai; Palkia; Lotira |
| 804 | Naganadel | Oikoumene | Evolve Poipole | LEGENDS §6 | — | — | The Peratai; Palkia; Lotira |
| 805 | Stakataka | Oikoumene | Troad: the Walls of Laomedon | LEGENDS §6 | 76 | Lotira | The Peratai; Palkia; Lotira |
| 806 | Blacephalon | Oikoumene | Libya: the salt ridge | LEGENDS §6 | 76 | Lotira | The Peratai; Palkia; Lotira |

### 15.2 The quests this guide adds

Each follows LEGENDS §0: a clue trail, a person, an omen or a relic, and a payoff scene. Encounters follow the epic doc where one owns the map. Where an epic already stages the battle, the quest wraps it in steps without changing it.

**The Primordials and the Prime Mover**
- **Groudon, *Gaia's Navel*** (D8; Lv 88; after the Katabasis). 1. After Tartarus is emptied, the Pythia's tripod at Delphoi starts to sweat. "The ground's warm. It hasn't been warm since Apollo came." 2. Pan's caves quest's last cave (D8, the Korykian cave) has an inner grotto behind a Crook face that was cold before; now it steams. 3. Descend three rooms where the floor's heat rises a step at a time (the Etna kit's rising-heat state, §10). 4. At the bottom, the first oracle's stone, Gaia's before Apollo's. The sun comes out underground, and Groudon rises.
- **Kyogre, *The River That Runs in a Circle*** (Atlantis; Lv 88; after Atlantis). 1. After Pontanax, Daphne notices the current in the abyss runs one way, round. 2. Follow it with the Pearl past three markers that the Nereids left. 3. Rain falls from nowhere, under the sea. 4. Oceanus, the world-river, rises at the edge.
- **Rayquaza, *The One Who Held the Sickle*** (D11 and above; Lv 88; the Kotinos). 1. With the Kotinos, the Ascent's cloud bank (D11) parts onto Pegaunos's meadows. 2. A thunder-horse herder there has seen a long green shape in the storm above, "looking for someone." 3. Carry the Harpe's empty sheath (a story item kept since the climax) to the meadow's highest stone. 4. Ouranos comes down to look at the one who held the blade that first cut Earth from Sky (POSTGAME §3.3's scene).
- **Arceus, *Stand Still*** (the summit; Lv 95; the four keys and the three Primordials). 1. Set the four keys into their plates at the summit's foot (§4.6). 2. The last herm. 3. The summit, where walking takes you back (POSTGAME §3.3). 4. Stop, and the summit brings you.

**The sea of Atlantis**
- **Lugia, *The White Bird*** (Atlantis's abyss; Lv 80). 1. A white shape under the Clashing Rocks (§3.3): "Going west," says Phineus. 2. In ODYSSEY's storm a white bird drops a veil (the Leukothea cameo, and Calypso's raft, §13). 3. Daphne connects the two: "The same bird. Ino became a sea-goddess." 4. In Atlantis's abyss, follow the veil's glow down. Leukothea waits at the bottom.
- **Manaphy, *The Prince's Egg*** (Atlantis's nursery; an egg). 1. A Nereid asks you to find the coral garden's missing egg. 2. Three sea-currents lead three ways; only one carries warm water (follow the bubbles). 3. The egg, in a ring of Luvdisc. Daphne hatches it on the *Euploia*. **Phione** comes from breeding Manaphy with Pharos's Ditto (§3.5).

**The Underworld**
- **The five Titans, *The Relics' Exam*** (Tartarus; Lv 75; after the Katabasis's descent). UNDERWORLD §4.10's five cells are each a relic test: Krios's cell needs the Hammer, Koios's the Torch, Iapetos's the Labrys, Hyperion's the Girdle, Menoitios's the Thread. Free each Titan and its Regi joins the fight (Regirock, Regice, Registeel, Regieleki, Regidrago). The new clue trail: in the Meadows, Tiresias names "five who never got a trial", and the five cells' names are cut into the Bronze Gates.
- **Regigigas, *The Keeper of the Gate*** (Tartarus's inner gate; Lv 80; all five Titans). 1. With five cells open, the inner gate's five locks glow. 2. Briareus, the hundred-handed gaoler, asks if his work is done. 3. Battle him, or answer that it is. 4. The keeper of the gate wakes, slowly, as the Regis' king.
- **Giratina, *Upside Down*** (the Chasm; Lv 80). 1. Below the inner gate, the Chasm's floor is its ceiling (UNDERWORLD §4.11). 2. The Cutter tells you to walk where you can't. 3. Three gravity flips, each opened by a Titan you freed, who holds the rock while you cross. 4. Tartaros, the first pit, upside down.
- **Cresselia and Darkrai, *Horn and Ivory*** (the House of Night; Lv 78; PG-26). 1. On the Cimmerian Shore (§3.10), the Land of Dreams' gates of horn and ivory are shut. 2. A dreamer in the Cave of Sleep says the dreams have gone to Night's house, below. 3. In the Katabasis, the House of Night's door opens only to someone asleep: rest at the Asphodel cypress, then walk in. 4. Two dreams: the true one (horn) and the false one (ivory). Choose which to battle first; the other waits a night.

**Olympia, Olympus and the story's own**
- **Victini, *Nike Comes Down*** (Olympia; Lv 80; the five gold symbols). POSTGAME §3.1's catch, with a trail: each gold symbol makes the Nike on her pillar turn one notch toward the stadium, and Paionios notices. On the fifth, she steps down.
- **Kairazor, *Try Twice*** (Olympia's altar of Kairos; Lv 78). POSTGAME §3.1's timing catch. The trail: the altar's priest hands you the forelock's single hair from the Stair of Hours, which you've carried since the climax.
- **Pegaunos, *The Bridle*** (D11; Lv 80). Bellerophon's chain, WORLD_EXPLORATION §7: Peirene's spring (I2), Akrokorinthos (I3), Hippokrene (T9) and the cloud meadows (D11). Each spring gives a piece of Athena's golden bridle; the whole bridle calms the thunder-horse.
- **The colossi, *The Three Lots*** (Olympanax D12, Pontanax K6 to G2 to Atlantis, Nekranax I13 to Hades's vault; Lv 80). 1. Bring Kronolith to the Omphalos; it gives back three bronze lots (POSTGAME §3.4). 2. Phidias's empty throne: "It stood up and walked to Olympus." 3. Each lot opens its seal: thunderbolt on Olympus's storm terrace, trident in Atlantis's temple, bident under Hades's hall. 4. Each colossus wakes when its lot is set.
- **Ichorin, *The First Myth*** (G12; Lv 70). 1. In the Katabasis, fill a hoof cup (G6's quest) at the Lake of Mnemosyne. 2. Pour it into the Pool of Mnemosyne in Arkadia. 3. The pool's floor shows stars by day (G12); dive with the Pearl. 4. Ichorin, the first story, at the bottom.
- **Kronolith, *Give It Back*** (the deep under the Omphalos; Lv 60, rematch scaling). 1. The Pythia asks you to bring back what the Lord of Time swallowed. 2. The deep under the Omphalos, a dial of twelve hours. 3. Set the dial to the hour you seized the Moment. 4. Kronolith gives back the three lots, then fights or joins.
- **The Fates, *Three Sanctuaries*** (Lv 60). Each Fate waits at her sanctuary after the climax (STORY §2). The trail: Halia's spindle-whorl (K3's old grove) spins toward the nearest one. Nemira asks for wool, Lotira for a measure (a Nilometer reading from Elephantine, §3.5), Thanira for nothing. Thanira also guides the Katabasis.

**Moved or extended by this guide (P-20)**
- **Uxie, *Lethe, Then Mnemosyne*** (T7, Lebadeia's Trophoneion; Lv 70). 1. Lebadeia's oracle descent opens with the Thread (T7). 2. Drink from Lethe, then Mnemosyne, the springs beside the temple (`design/maps/Lebadeia.md`): the screen blanks, then remembers. 3. Go down feet first. At the bottom, the votive tablets of everyone who came back changed. 4. Uxie, Reason, the charioteer of Plato's soul, sits among them. The Charioteer quest (LEGENDS §3.3) begins here, then sends you to Mesprit at Lake Tritonis and Azelf at Lake Maeotis. It used to start at Lake Moeris, which keeps its crocodiles.
- **Diancie, *The Crown's Last Stone*** (K9, Ariadne's door on Kalliste; Lv 74; the Corona Borealis). LEGENDS §4.10's quest, moved from Mount Nysa: Naxos (Kalliste) is where Dionysus gave Ariadne her crown. 1. Ariadne visits Kalliste after Knossa (WORLD_EXPLORATION Q3). 2. The crown is missing one stone. 3. The Labrys opens the door under the Portara. 4. Diancie, the last stone, in the room behind it.
- **Marshadow, *The Shadow Hermes Left*** (Elaia, then G11; Lv 75). LEGENDS §7.5, with one step added: the shadow left at Elaia after the theoxenia finale runs. Follow it across Aethos by its omens (a shadow with no one to cast it) to Lykaion's shadowless precinct (G11, the Helm), where no one casts a shadow. It's there, being one.
- **Celebi, *The Thirteenth Hour*** (Akti, the fractures, then T6; Lv 70). LEGENDS §7.1, with its last step moved to the Kopais marsh's fog bank (T6, the Bag), "where the reed people live outside time."
- **Volcanion, *Steam and Stone*** (Etna; Lv 80). LEGENDS §4.12's quest, moved to Etna's Typhon chamber (§10).

### 15.3 What it costs and when it's built

- **Build:** each legend is built with the map that hosts it. A land's builder does its legends, and an epic's builder does the epic's. The Aethos ones go in with WORLD_EXPLORATION §8's return packs (Kalliste, Lebadeia, Arkadia, the Ascent).
- **ROM:** LEGENDS's estimate (~0.3 MiB) covers its quests; §15.2's added and moved quests are scripts and a few objects, about 40 KiB. The post-game total stays about 4.7 MiB of 9.0 free.
- **The 100%:** LEGENDS §10's checklist stands; this register is its index.

| # | Proposal | Changes | Recommendation |
|---|---|---|---|
| P-20 | **Legends behind Aethos's return gates:** Uxie moves to Lebadeia's oracle descent (T7); Diancie to Ariadne's door on Kalliste (K9); Marshadow's quest ends at Lykaion (G11); Celebi's at the Kopais fog (T6). At 1.0, the stretch homes of Mew, Lunala, Zeraora, Azelf, Zygarde and Meloetta ride on 1.0 maps (each row says where). The Aethos/Oikoumene split becomes 53/83 | LEGENDS §3.3, §4.10, §7.1, §7.5 (places only) | Yes, as the user directed |
