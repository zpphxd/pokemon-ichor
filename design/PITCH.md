# Pokémon Ichor — Pitch

> *In the age of heroes, every life is a thread spun by the Fates and read by the Oracle. Except yours.*

**Working title:** Pokémon Ichor. In Greek myth, ichor is the golden blood of the gods. The alternate title is Pokémon Laurel. Both names are unclaimed as of 2026-11-13.

**Basics**

| | |
|---|---|
| Base | pokeemerald-expansion 1.17.2 (the Emerald decompilation) |
| Pokémon | A new **Aethos regional dex** of about 150 species drawn from Greek myth (decided 2026-11-14, being designed in `design/dex/`). How it mixes with the existing 9 generations is open. |
| Format | Distributed only as a `.bps` patch |
| Benchmark | Pokémon Glazed |

**Logline:** You are the only person in Aethos whose fate was never written. A cult that worships Kronos wants to use you to stop time forever, and you are the only one who can stop it.

---

## 1. The world: the Aethos region

Aethos is a sun-bleached archipelago and mainland in the age of heroes. It has no modern technology. Every familiar system is re-skinned to fit the era.

| Standard system | In Aethos |
|---|---|
| Pokémon Center | **Asclepeion**, a healing temple of Asclepius |
| Poké Mart | **Agora** stall |
| PC storage | **Pithos** storage. The pithos was the great storage jar, and "Pandora's box" was really a pithos. |
| Gyms | **Temples** |
| Gym Leaders | **Hierophants** (high priests) |
| Badges | **Laurel leaves** woven into a victory crown |
| Ferries | **Triremes** |
| Elite Four | **the Pantheon** on Mount Olympus |
| Champion | **the Archon** |

### Places

| Place | Inspired by | Role |
|---|---|---|
| **Elaia Village** (Kalliste Isle) | olive-grove island | Hometown. Home of the Akademia grove and Professor Daphne. |
| **Akti Town** | fishing harbor | Temple of Hestia (1) |
| **Emporion City** | trading port | The great Agora. Temple of Hermes (2). |
| **Eleusa Village** | Eleusis | Wheat fields and an underground Mystery sanctum. Temple of Demeter (3). |
| **Thyrsa City** | Theater of Dionysus | Vineyards and a vast amphitheater. Temple of Dionysus (4). |
| **Arkadia** | mountain wilderness | Moonlit cypress forests and the Pool of Mnemosyne. Temple of Artemis (5). |
| **Astyra** | Athens | Capital: Akropolis, Library, Lyceum, Archon's Stoa. No temple; it is where the story turns. |
| **Kaldera** (Thera Isle) | Santorini volcano | Black-sand caldera forge. Temple of Hephaestus (6). |
| **Kythera Isle** | Cyprus / Paphos | Sea-foam beaches and the Spring of Kallirhoe. Temple of Aphrodite (7). |
| **Knossa Isle** | Crete / Knossos | The Labyrinth and Daedalus's workshop |
| **Lakonia** | Sparta | The rival's hometown, the battle school, and Lake Stymphalia |
| **Delphoi** | Delphi | The Oracle, the Omphalos, and the Loom of Fate. Temple of Apollo (8). |
| **The Ascent → Olympus** | Mount Olympus | Victory Road climbs through the clouds to the Pantheon |
| **Cape Tainaron** | the Underworld gate | Post-game |
| **Olympia** | site of the Games | Post-game: the Olympiad |
| **Atlantis** | the sunken city | Post-game |

---

## 2. The story

**Theme:** fate versus free will, and hubris and its cost. The full story, with character bibles, the beat sheet, the foreshadowing map and key scenes, is `design/STORY.md`, approved by the user on 2026-11-14. This section is its summary.

### Cast

- **You, "the Unwoven."** Default names are Theo and Ianthe. You wear a traveler's petasos hat and cloak. On the night you were born, the Loom stopped and the Oracle of Delphoi went blind for one hour; she has never been able to see your thread. The truth: the Spinner unspun your one-hour thread at your mother's plea. The thread you spin yourself is gold.
- **Mom (Melitta).** A former *melissa*, a bee-priestess of Delphoi. She learned her unborn child's thread was one hour long and begged the Fates, then fled to Kalliste and gave birth under the old olive in Elaia's square. She tells you everything at Delphoi, and hands you the honey jar labelled NOT FOR {PLAYER} for the Fates.
- **Professor Daphne.** A philosopher-naturalist at the Akademia grove who believes "every myth is a memory of a Pokémon." Pokémon professors are named after trees, and Daphne is the laurel. She knows why you have no thread. Her banned book on the Harpe became the Titans' map, and Phaedon was her friend.
- **Alethea.** Daphne's apprentice and your friend. Her name means *truth*. She keeps the Pokédex and digs into ruins. Her Klotheia reading was Cassandra's curse: she would never be believed. Ostracized in Astyra on a forgery, she unmasks the forger and becomes Keeper of Records.
- **Kleon.** Your rival, raised in the Lakonian battle school. His name comes from *kleos* (glory). A prophecy said he would die young and glorious, so he races toward it. He is Rhea's son. His arc runs from hubris to a fall to redemption: he breaks his own thread by will, and carries his blind enemy down the crumbling Stair where no one will ever see.
- **Team Titan.** The Titanborn wear bronze Corinthian helmets under a sickle emblem. They preach freedom from the tyranny of prophecy, and seek it through stasis instead of change.
  - **Hyperion** (Fire/Rock): a champion going blind, promised an endless noon.
  - **Iapetos** (Dark/Psychic): Team Titan's real architect. In public he is **Keeper Lykophron**, the Archon's Keeper of Records, once the priest who set the Pythia's words in verse. He forges fates to write the world's last draft, and every line he writes ends in a little hook.
  - **Rhea** (Ground): Kleon's mother. She buried two children to prophecy and misread the third's. At Knossa she disobeys Kronos and leaves the threshold open, the first crack in Team Titan, and on Crete she saves her last child from Kronos, as in her myth.
- **Kronos.** The masked leader. He is really **Phaedon**, a gentle healer at the capital's Asclepeion. His daughter **Elpis** (*Hope*, the last thing left in Pandora's jar) is fated, he believes, to die young. Her oracle was forged by Iapetos: the true one said her thread ends "the day the hours stop". By fleeing the forgery, Phaedon sets out to stop the hours, the one thing that could end her thread. He wants to seize the Loom and wake the Lord of Time to freeze the world in a golden age where no thread is ever cut.
- **Archon Aristeides the Just.** The Champion. He believes fixed fate keeps the peace. The one thing he ever chose freely was sparing you as a baby, under the law of xenia. He lied about it, was blackmailed for it, and keeps **Medon's Knot**, which could make all fate fixed again. **Medon**, son of Kodros, was the first Archon, who chained the Fates.
- **The Labyrinth's cast** (`design/LABYRINTH.md`, approved 2026-11-14):
  - **Daedalus**: the maker beneath Knossa, haunted by Icarus and by his apprentice. Out of sympathy for a grieving father he timed the Harpe's forging for Kronos, and now repents.
  - **Ariadne**: priestess of the Mistress of the Labyrinth and Asterion's half-sister. She is later the Endless Labyrinth's Brain.
  - **Asterion**: the Minotaur, a Pokémon goaded into a monster, whom you free. He is **Asterlorn** (Aethos dex #98, Fighting/Dark): only one exists, chained at the Labyrinth's heart.
  - **Minos**: Knossa's dead king, a tomb in the main story and a judge of the dead after it.
- **Legendaries** come from the Aethos dex (`design/STORY.md` §2 has the casting table):
  - **The Lord of Time** (the dex's Kronolith) replaces Dialga.
  - **The three Fates** (the Spinner, the Measurer and the Cutter) replace the lake trio.
  - **The Moment** (the dex's Kairazor, Kairos) is the moment you seize to restart time.

### Act I — The Unwoven (Laurels 1–3)

1. At the Klotheia, the coming-of-age festival, Halia can't read your thread. You receive your first Pokémon and fight your first battle with Kleon.
2. Team Titan grunts are caught digging at hilltop ruins for a fragment of the **Harpe**, the adamant sickle the Titan Kronos once wielded.
3. You cross to the mainland by trireme.
4. In Eleusa's underground Mystery sanctum the Titans steal the first fragment.
5. Daphne tells you what you are. There is a Loom where the three Fates weave every life, and yours isn't on it. *Why* waits for your mother, at Delphoi.

### Act II — Hubris (Laurels 4–6)

1. At the Dionysia festival in Thyrsa, Iapetos stages a tragedy, *The Unwoven*, that puts your own origin on stage and entrances the whole amphitheater. The satyr play breaks it.
2. In Arkadia, Kleon loses badly to the Huntress Kallisto. Iapetos offers to rewrite Kleon's fate into one of victory. Kleon accepts and joins the Titans. His hubris is wanting to own his fate. The forged prophecy reads: "Kleon of Lakonia shall slay the starry bull beneath the house of the double axe, and his glory shall never die."
3. **Astyra:** you meet a kind healer, Phaedon, who tends your Pokémon at the Asclepeion, and his sick daughter Elpis. She owns a clay bull she calls Starry, and Phaedon's theme is the lullaby she hums.
4. **The ostracism:** in Astyra, Alethea is ostracized on a forgery.
5. **The midpoint:** Team Titan storms the Akropolis for the second fragment. You fight up the Akropolis beside Alethea in a double battle, then face Kleon, now a Titan agent, who tells you they want *you*.
6. At Kaldera's forge you learn the Harpe can cut what the Fates have woven. Only someone with no thread can hold it without being unmade, which means you.
7. **The low point:** at Kaldera, Mom has vanished.

### Act III — The Loom (Laurels 7–8, climax, League)

1. **Kythera.** You win the seventh laurel.
2. **Knossa.** Ariadne gives you her thread. You descend Daedalus's seven-ringed Labyrinth, where Team Titan has its headquarters, and meet Daedalus, who gives you the Labrys. You win the Helm of Darkness from King Minos's tomb, beat Hyperion at the forge, and find Iapetos's draft of Kleon's prophecy. At the heart, under Daedalus's stars, Kronos completes the Harpe. You free the Minotaur, Asterion, instead of fighting him, and stop Kleon from killing him. Kronos removes his mask by choice: he is Phaedon, and he asks you to carry the Harpe at the Loom. Rhea turns the house to trap you but leaves the threshold open, and you escape along your own thread. The full design is in `design/LABYRINTH.md`.
3. **Lakonia.** Rhea unmasks for her son. Kleon learns two things: Iapetos forged his new prophecy, and his old one was misread, because *kleos* never meant death.
4. **Delphoi.** You win the eighth laurel from the Pythia. Mom tells you everything. Kronos opens the Omphalos.
5. **The Loom.** The three Fates are chained there, and have been since the first Archon, Medon, bound them to make destiny unchangeable. They ask to be freed, knowing the cost: "We let you go once. Will you let us go?" You cut them free because it is right. Kronos seizes their power, and **the Lord of Time awakens**.
6. **The Frozen Hour.** All of Aethos stops. The palette drains to gray and every person is frozen mid-step. Only you can move. You travel the frozen world to the three sanctuaries to rouse the Fates.
   - Mom stands frozen at the top of the stair, waiting.
   - The herms you anointed in Act I turn their heads to guide you.
   - Phaedon sits at Elpis's bedside and reads the true oracle, in Alethea's handwriting.
   - Kleon breaks free of the stillness by sheer will.
7. **The Stair of Hours.** You and Kleon fight Kronos and Hyperion in a multi battle, and Kleon carries the blind Hyperion down. You beat the Lord of Time, and still the world won't move. It restarts only when you seize **the Moment** as it runs down the falling sickle, not knowing whether Elpis will wake.
8. **Resolution.** Time flows again and the Fates stay free. Prophecy ends, and every person weaves their own thread. Elpis wakes: "Then my thread isn't finished yet." Phaedon is exiled to Kalliste as a suppliant at Hestia's hearth, healing small wounds at Akti.
9. **The Ascent → the Pantheon → the Archon.** The Archon keeps Medon's Knot, and the League is the fight over whether fate returns. You win it, take the Archon's title, and the two of you untie the Knot together. Credits.
10. **The epilogue: the next Klotheia.** Daphne asks her first question again, and you can answer "WE'LL SEE". The third krater goes to Elpis: "Someone always comes late." The post-game begins here.

---

## 3. The Twelve: temples and the Pantheon

The 8 temples and 4 Pantheon seats are the **Twelve Olympians**. Hestia is counted as one, and the Archon serves Zeus. **Hades** is not an Olympian, so he waits in the post-game.

| # | Olympian | Type | Hierophant | Home |
|---|---|---|---|---|
| 1 | Hestia | Normal | Ione, the Hearthkeeper | Akti Town |
| 2 | Hermes | Flying | Kerykos, the Herald | Emporion City |
| 3 | Demeter | Grass | Chloe, the Mystagogue | Eleusa Village |
| 4 | Dionysus | Poison | Thespis, the Masked Player | Thyrsa City |
| 5 | Artemis | Dark | Kallisto, the Moonlit Huntress | Arkadia |
| 6 | Hephaestus | Steel | Talos, the Bronzesmith (Daedalus's apprentice Perdix as a boy; he gives you Daedalus's Wings) | Kaldera |
| 7 | Aphrodite | Fairy | Galatea, the Living Marble | Kythera Isle |
| 8 | Apollo | Fire | Phemonoe, the Pythia | Delphoi |
| P | Ares | Fighting | Brasidas, the Polemarch | Olympus |
| P | Poseidon | Water | Themistokles, the Admiral | Olympus |
| P | Athena | Psychic | Hypatia, the Philosopher | Olympus |
| P | Hera | Dragon | Olympias, the Serpent Queen | Olympus |
| C | Zeus | Electric / mixed | Archon Aristeides the Just | Olympus |

Hera is the Dragon seat because in myth she raised the Hydra and set Ladon to guard the golden apples. Team Titan uses earth-born types (Rock, Ground, Steel), because the Titans were children of Gaia.

---

## 4. Pokémon: every generation, chosen for the myths

> **Superseded in part (2026-11-14).** The user chose to design a ~150-species Aethos regional dex of new Pokémon. The mappings below stand until `design/dex/` replaces them; see `design/dex/DECISIONS.md`.

- **Starters: the Python, the Typhon and the Trident.** The three come from three different generations, and none is among Lazarus's nine starters.
  - **Snivy** (Gen 5): Serperior is the great serpent of Delphoi that Apollo slew.
  - **Cyndaquil** (Gen 2): Typhlosion is named for Typhon, father of monsters. Its ancient Hisuian form (Fire/Ghost) suits the era.
  - **Piplup** (Gen 4): Empoleon carries Poseidon's trident on its crest.
  - **Theoxenia: gods in disguise** (user, 2026-11-14; replaces the earlier "Sanctuary of Firsts"). Later in the game, gods walk Aethos disguised as strangers. They test your kindness, then reveal themselves and give you a starter as a guest-gift. Details are in `design/SYSTEMS.md` §10.
    - **Core tier:** Demeter gives Snivy after Laurel 5, Hephaestus gives Cyndaquil (which evolves into Hisuian Typhlosion) after Laurel 6, and Poseidon gives Piplup after Laurel 7.
    - **Extended tier:** 13 more visits through the late game and post-game give the other starter lines. It ends with Zeus and Hermes at Mom's door in a storm.
    - Lazarus's nine starters are offered nowhere.
    - No vanilla species is cut from the ROM. The user wants every Pokémon obtainable eventually, so the gift species are there anyway.
- **Aethos Dex:** about 400 species from Gen 1–9, placed by theme. All **1,025** species can be caught by the end of the post-game. Glazed stops at Gen 6.
- **Ancient era, ancient forms.** Hisuian forms live in Aethos naturally, because the setting is ancient. Ancient Paradox Pokémon (Great Tusk, Flutter Mane, Roaring Moon and the rest) appear in post-climax **Time Fractures**, where the Golden Age leaks through.

### Myths, cast with Pokémon

| Myth | Pokémon |
|---|---|
| The three Fates (Moirai) | the Aethos dex's three Fates: the Spinner, the Measurer and the Cutter |
| Kronos, the Lord of Time | Kronolith (Aethos dex) |
| Kairos, the Moment | Kairazor (Aethos dex) |
| The Titans of Tartarus | Regigigas and the Regis |
| Hades and the Underworld | Giratina |
| Zeus's thunder-eagle | Zapdos |
| The Phoenix | Ho-Oh |
| The Dioskouroi twins | Latias and Latios |
| Nike, goddess of victory | Victini |
| Artemis's Golden Hind | Xerneas |
| Hephaestus's golden automaton | Magearna |
| The forge beneath the volcano | Heatran |
| Orpheus's song / the Muses | Meloetta |
| Eros and Aphrodite | Enamorus |
| Hypnos and Nyx (sleep and night) | Cresselia and Darkrai |
| The evils escaped from Pandora's jar | the Treasures of Ruin |
| Comedy and tragedy masks of the Dionysia | Ogerpon |
| The Lernaean Hydra | Hydreigon |
| Ladon and the golden apples | Hydrapple |
| Cerberus | Mega Houndoom |
| Asterion, the Minotaur | Asterlorn (Aethos dex #98, Fighting/Dark) |
| The Stymphalian birds | Skarmory and Corviknight |
| Polyphemus the Cyclops | Dusclops and Dusknoir |
| Circe's swine | Lechonk and Oinkologne |
| The Lotus-Eaters | Lotad and Ludicolo |
| The Sirens (bird-women) | Altaria |
| Scylla | Grapploct |
| The Golden Fleece | Mega Ampharos |
| Typhon | Hisuian Typhlosion |
| The Prime Mover | Arceus |

---

## 5. Systems

- **Apotheosis (Mega Evolution).** The key stone is the **Omphalos**, and Mega Stones are **Ichor Stones**. All classic and Legends Z-A Megas are included. It is the one battle gimmick; Z-Moves, Dynamax and Tera are off.
- **Difficulty.**
  - **Mortal**: easy.
  - **Hero**: standard.
  - **Spartan**: level caps, set mode, no items in battle, smart AI, and competitive boss teams.
  - **Oath of the Styx**: an optional Nuzlocke ruleset you swear to at the start.
  - **Current selection policy:** confirm Mortal, Hero or Spartan when setting
    the bedroom water clock. The choice is fixed for that save; existing saves
    stay Hero. Act I's modes are integrated; natural-level mode balance still
    needs approval. New games then offer the Oath separately, defaulting to
    NO and requiring a second confirmation to swear. Both answers are final
    for the opening; existing saves are not prompted or retroactively enrolled.
    The Oath has saved one-chance-per-named-area receipts independently of
    difficulty, and version-6 Urn foundations that preserve fallen Pokemon
    and grow only into empty Pithos jars without changing save sizes.
    Native wild-battle entry and ball-use guards now enforce the area chance
    on sworn saves; ordinary runs remain unrestricted.
    Real player fainting now records permanent falls, and HP healing, revival
    items and Revival Blessing respect them. The Urn now has view-only storage,
    and captures and deposits skip its jars. Non-defeat battle teardown now
    transfers fallen partners when a usable survivor remains, with party
    compaction and an acknowledged field notice.
    Capacity refusal preserves the fallen source and explains the problem.
    Retained fallen partners are restricted to view-only party actions;
    freeing a jar retries burial automatically on leaving storage.
    Total-party loss now recovers a living stored partner before ordinary
    whiteout healing. Exhaustion and blocked full-party/full-Urn recovery
    return to title without overwriting the last manual save, and saved
    failed states cannot enter the field.
    Field-poison cleanup waits for all party messages before burial and uses
    the same recovery path for total-party loss; modern one-HP survival
    never counts as a fall. Charon's later release scene and the Riverside
    shades remain Underworld chapter work, not delivered opening features.
- **No HM slaves.** Field powers come from relics. Relics are key items you use straight from the field; no Pokémon ever learns a field move. The user approved this mapping on 2026-11-14. Each relic's myth-quest and upgrades are in `design/SYSTEMS.md` §1–3.

  | Field power | Relic | Arrives |
  |---|---|---|
  | Running shoes | Talaria (winged sandals) | Act I |
  | Rock Smash | Bronze Hammer | Act I |
  | Flash, plus light, braziers and burning brambles | Hecate's Torch | Act I |
  | Cut | Demeter's Sickle | Act I, Eleusa |
  | Strength | Girdle of Herakles | Act II, Laurel 4 |
  | Surf | Poseidon's Conch | Act II, Astyra |
  | Fly | Daedalus's Wings, from Talos | Act II, Laurel 6 |
  | Waterfall | Horn of Achelous | Act III |
  | Escape and path-marking (the Labyrinth) | Ariadne's Thread | Act III, Knossa |
  | Dials, seals and chains (the Labyrinth's tool) | Labrys | Act III, Knossa |
  | Stealth past sight lines | Helm of Darkness | Act III, Knossa |
  | Dive | Nereid Pearl | Post-game |
  | Sailing and fog | Aeolus's Bag of Winds | Post-game |

  Two tools also come into play: **Alethea's Trowel**, for digging, and the **Star Chart**.
- **Rites.** Altars and roadside shrines to all 15 gods, about 60 in all. Praying is free. Offerings earn a god's **Favor** (0–100) and a blessing that lasts a set number of steps. Each god gives gifts at Favor 30, 60 and 100. Specified in `design/SYSTEMS.md`.
- **The living world** (`design/SYSTEMS.md`):
  - **Herm waystones:** you anoint them in Act I, and they become fast-travel points in Act II.
  - **Excavation** with Alethea's Trowel: amphorae that tell myths, ostraka, and evidence of Iapetos's forgeries.
  - **A daily augury**, built on the mass-outbreak engine.
  - **Festivals** on a 36-day Aethos year.
  - **The Katasterismoi:** a star chart of 24 constellations.
  - **Knucklebones** in the tavern.
  - **Xenia** (hospitality to strangers) and theoxenia (gods in disguise; see §4).
  - **"Know thyself"**: the Oracle's judge of your Pokémon.
- **Berries** stay, redrawn as Aegean fruits, and double as first-fruits offerings at the altars.
- **Design principle:** the main path never needs a time of day, a date, luck or a grind.

- **Modern features.**
  - Followers.
  - A day and night cycle with time-of-day encounters.
  - **The Augur's Eye** (DexNav).
  - **The Scroll of Deeds**, a quest log.
  - Run indoors, reusable TMs, and an EV/IV viewer.
  - Mints, and a move relearner in the party menu.
  - Pithos access from the menu, and an auto-repel prompt.
  - Fast text and battle options. Glazed has no speed-up.

---

## 6. Post-game: bigger than the main story

1. **The Twelve Labors.** A chain of side quests, each a myth retold with Pokémon:
   - the Nemean Lion (Pyroar)
   - the Hydra (Hydreigon)
   - the Golden Hind (Xerneas)
   - the Erymanthian Boar (Mamoswine)
   - the Augean Stables (Garbodor)
   - the Stymphalian Birds (Corviknight)
   - the Cretan Bull (Tauros), Asterion's sire. Asterion helps.
   - the Mares of Diomedes (Mudsdale)
   - Hippolyta's War-Belt (renamed so it doesn't clash with the Girdle of Herakles relic)
   - the Cattle of Geryon
   - the Apples of the Hesperides (Hydrapple)
   - Cerberus (Mega Houndoom)
2. **Katabasis: the Underworld.**
   - Pay Charon an obol to cross the Styx, home of Basculegion, the souls of the drowned.
   - Pass Cerberus.
   - Walk the Asphodel Meadows and Elysium.
   - Free the Titans in Tartarus: Regigigas and the Regis.
   - Face Hades and Persephone, then Giratina.
3. **The Olympiad.** The Battle Frontier, held at Olympia.
   - Its Frontier Brains are heroes: Achilles, Atalanta, Odysseus and Hippolyta.
   - **The Endless Labyrinth** at Knossa runs on the Battle Pyramid engine. Ariadne is its Brain, with Asterion as her ace. Asterion may join you after her gold symbol.
   - The Arena of Champions hosts rematches with every Hierophant.
4. **The Odyssey.** A voyage across the wine-dark sea:
   - Polyphemus's island
   - Circe's island
   - the Sirens' rocks
   - Scylla and Charybdis
   - the Lotus-Eaters
   - Aeolus's bag of winds (Tornadus)
   - It ends with a homecoming to Elaia.
5. **Atlantis.** A sunken marble city with Manaphy, Kyogre and Lugia.
6. **The Primordials and the Prime Mover.** Groudon (Gaia), Kyogre (Oceanus) and Rayquaza (Ouranos), then Arceus on Olympus's true summit.

---

## 7. Art and music direction

> **Total conversion (user, 2026-11-14).** Every asset on screen is redrawn Greek-myth inspired: houses, landscape, temples and columns, people, Pokémon, battles and every menu. Nothing stays Hoenn. The plan is in `design/ART_PLAN.md`.

- **A world painted on pottery.**
  - Menus and text boxes use terracotta-and-black Greek key borders.
  - Battle intros are black-figure silhouettes.
  - The title screen is a painted amphora.
  - The trainer card is a kylix (a drinking cup).
- **The overworld** keeps the Gen 3 16×16 style in a Mediterranean palette: Aegean blue, marble white, olive, terracotta and sun-gold.
- **Biomes:**
  - olive groves and vineyards
  - Cycladic villages and marble cities
  - wheat plains and cypress forests
  - a volcanic caldera and sea-foam coves
  - the Labyrinth
  - snowy Olympus above the clouds
  - the gray Underworld and golden Elysium
  - sunken Atlantis
- **Music.** Composed in the original Greek modes (Dorian, Phrygian, Lydian and Mixolydian), voiced as lyre, kithara, aulos and frame drum.
  - Battle themes use Greek folk meters: 7/8 (kalamatianos) and 9/8 (zeibekiko).
  - The Frozen Hour is near-silence and a ticking music box.

---

## 8. How we build it

### Team: one director, specialist agents

| Role | Owns |
|---|---|
| Creative Director (main session) | Vision, story bible, final review of all work |
| Narrative | Script and dialogue in Poryscript |
| World and level | Maps in Porymap, routes, puzzles, encounters |
| Engine | Expansion config, C features (difficulty, quest log, Apotheosis, relics) |
| Balance | Regional dex, trainer teams, level curve |
| Pixel art | Tilesets via Porytiles, trainer and overworld sprites, UI |
| Music | MIDI in Greek modes, then mid2agb and voicegroups |
| QA | `make check`, scripted mGBA smoke runs, bug list |

### Stack

| Area | Tools |
|---|---|
| Engine | pokeemerald-expansion 1.17.2 |
| Compiler | devkitARM |
| Maps | Porymap 6.3 |
| Scripting | Poryscript 3.6 |
| Tilesets | Porytiles 2.0 |
| Art | Aseprite or Pixelorama |
| Testing | mGBA 0.10.5 with Lua and printf logging |
| Patching | Flips (`.bps`) |
| Version control | git, for the design docs and the game fork |

### Roadmap

Every phase ends in a playable patch.

| Phase | Deliverable |
|---|---|
| **0. Foundation** | Toolchain installed, expansion forked, first clean build, ROM size measured, features configured (followers, day/night, Megas, DexNav, caps), Porytiles pipeline, automated smoke test, renamed title screen |
| **1. Vertical slice** | Kalliste Isle: Elaia, Route 1, Akti Town and the Temple of Hestia. First Greek tileset, pottery UI, the main cast's sprites, 3 songs, starters, the rival battle and Laurel 1. About an hour of play. **You playtest and approve the look before we scale.** |
| **2. Act I** | Emporion and Eleusa, Laurels 2–3 |
| **3. Act II** | Thyrsa, Arkadia, Astyra and Kaldera, Laurels 4–6 |
| **4. Act III** | Kythera, Knossa, Lakonia, Delphoi, the Frozen Hour and Olympus. The story is complete (**0.9**, approved OIKOUMENE PG-1). |
| **5. Post-game** | Labors, Katabasis, five-facility Olympiad, Odyssey, Atlantis, the Prime Mover, and all ten Oikoumene lands with their full Periodos halls. This is the **1.0 core** (OIKOUMENE PG-1, PG-4, PG-21, PG-33). |
| **6. Polish and release** | Balance, typo sweep, outside beta testers, release patch |

### Current implementation and acceptance

Use this table for current milestone status, rather than historical batch headers.
Engine support, reachable content, automated coverage and player approval are separate
gates. Counts of maps, species or songs are not a completion percentage.

| Goal | Implemented / playable | Remaining acceptance or implementation |
|---|---|---|
| Foundation | ROM builds; opening smoke and save/reload exercised; native emulator setup verified | Keep build commands reproducible on the current local toolchain; measure budgets after changes |
| Kalliste slice | Opening, starter selection, rival, Kronion Hill, Hestia and Laurel 1 | Current natural-level balance and human look/fun approval |
| Act I mainland | Voyage, Aegina, Emporion/Hermes, Routes 4–5, Hollow, Eleusa/Demeter, sanctum theft, Kleon's departure, Daphne's revelation with the real Star Chart, and the north-road Sickle gate | Complete return visits and side-system integrations, closing scene assets and player approval |
| Regional dex | 152 species records and expected sprite assets present | Chapter-appropriate obtainability, evolution timing, battle balance and final visual review |
| Shared systems | Save banks, relics/fire, rites/Favor, herms, excavation, world helpers, Act I difficulty/caps, starting Oath/capture/falls/Urn/recovery, Scroll of Deeds, portable Star Chart, Frozen Hour and parts of the Labyrinth | Remaining callers/tutorials; natural-level difficulty balance, later Oath story scenes, later quest pages, outdoor sky/rewards and missing dungeon mechanics |
| Act II | Story and system designs | Connected Thyrsa → Arkadia → Astyra → Kaldera chapters; Laurels 4–6 |
| Act III / 0.9 | Story and dungeon designs; supporting engines partly built | Kythera → Knossa → Lakonia → Delphoi → Loom/Frozen Hour → League and epilogue |
| Core post-game / 1.0 | Approved scope and dependency designs | Sailing, epics, facilities, ten lands/halls, all-species obtainability and twelve Kleos laurels |
| Release | Pipelines and some early regression coverage | Full-game natural-level runs, total-conversion audit, save safety, budgets and human acceptance |

The setup run exercised the opening through the Emporion gate continuously, and
separate area checks through the Mystery sanctum. Its assisted battles are progression
evidence, **not** natural-level balance evidence. Historical QA and art inventories
remain evidence of those revisions, not current open-issue counts.

The Hollow night-hound failure was a signed-offset error in the test clock setup,
not an established encounter bug. The corrected harness checks that the cave
actually loads at noon and 22:00; its complete 73-check walk passes.
Philoxenos and Metaneira now use the engine's forward-only rest menu; world tests
exercise actual NPC conversations, dusk, cancel, late-night behavior and the real
Wine reward.
Emporion Harbor now grants real Oil and the Trowel, invokes prayer/Favor and
fixed/daily excavation, consumes Oil for Daedalus's first page, and recovers the
missing tool on legacy saves. The Dolphin uses real best-of-five knucklebones
with cautious/bold opponents and actual Oil/Wine prizes. Myrtale awards a real
Fling scroll; a full TM pocket preserves the won prize for collection without
another match, including recovery of old placeholder wins. Reserved TM51–53
now teach Fling, Bulldoze and Round with species-specific eligibility; the
scroll stall sells the latter two without changing item IDs or save layout.
The offerings stall sells Oil, Barley Cake, Wine and Frankincense at their
specified prices. Pasion buys all three coins at the market's blessed price
plus 20%; cancellation and the money cap cannot consume an unpaid coin.
The Hephaisteion garden uses its own daily excavation index, distinct from
the harbor's ship sheds.
Emporion's crossroads herm now consumes Oil, grants its one-time Favor and
registers a Wings landing without counting toward the 23-route reward; legacy
anointing flags migrate without another charge. Halitherses reads the saved
daily omen, not a fresh random rumor. His optional blessing cannot be refreshed
by repeat conversations or map reentry. Reachable Act I omens include actual
Kerazap, Melibee and Stachyss outbreaks and Eleusa's sun weather. Its rare
Korantha visitor is a real level-22 encounter: capture or defeat consumes the
day's visit, while escape or loss leaves it available. An off-day legacy save
cannot reveal it; reentry cannot respawn a caught visitor. Later chapter omen
callers remain unfinished. An expired visitor cannot start a battle after a day
change in the wheat. Midnight rollover now refreshes live visitor objects and
Eleusa's sun/normal weather without reentry. It waits through active scripts,
fades and the Frozen Hour, and new arrivals do not overlap the player.
Emporion's marked-jar Pithound omen is also integrated: Halitherses names the
westernmost stoa jar, which holds a real level-16 visitor only on its omen day.
Capture/defeat consumes that visit; escape/loss keeps it available. The other
five jars retain their ordinary random encounters.
The Isthmus hill-spur Nemecub omen is integrated at level 18 after the rockslide
is cleared, with its approved rumor, real capture/defeat, loss/escape retry and
same-day persistence. The Halai Harpelle visitor belongs to later geography.
The Isthmus kilns and spur now have independent daily Arachne excavation.
The family tomb's fixed Arachne find is wired behind its existing Girdle gate;
natural acquisition of that relic still belongs to Act II.
Sanctum B1F's fixed Persephone sherd is also real excavation, with Trowel
requirement, repeat protection and saved-game persistence. Collecting sherds
does not itself restore an amphora or unlock its completed-amphora rewards.
The B3F cave-in exposes a real, Trowel-required fixed find for Daedalus's page II.
Its page ownership and consumed dig state survive saving and CONTINUE.
Eleusa's field shrine invokes Demeter's real prayer/offerings/Favor menu. Its
west and east digs have independent daily indices and actual Act I finds,
including Persephone sherds, rather than turned-earth placeholder messages.
Hermes's and Demeter's great temple altars now use real rites, including
daily prayer and doubled offering Favor. Kerykos awards Hermes's +15 Laurel
Favor once and teaches U-turn at Favor 30; cancellation leaves the lesson
available. Dynamic rite lessons are registered with the generated tutor lists
and still respect each species' learnset.
Mom's return-home dialogue now follows the crossing, ending and letter state.
All three Emporion day-runners and Eleusa's north herald can send the post-ending
letter. Mom answers with exactly three Honey, once, with an atomic full-Bag
refusal and saved pending/claimed state. The reserved story jar and her healing
offer are unchanged.
Halia and Gylippos acknowledge the revelation and Kleon's departure on return.
Daphne describes packing before the Mysteries and no longer appears at the home
Akademia after that night. Euboulos replaces missing Charcoal after the Hearth
Trial until the forge is relit, without duplicating an owned piece; a full Bag
can be retried. The original opening and home whiteout/healing remain playable
for all three starters.
Returning with the Trowel opens three independent daily Kalliste digs: Kronion
Hill's pried-up slabs, Route 1's bee terraces and Akti's beach. They give real
Act I loot and Kronos sherds, retain consumed/pending state through saves, and
renew at midnight without map reentry. A full Bag leaves an item in the ground
for retry; a four-piece collection keeps other loot available. Four collected
sherds are not a restored amphora until the player explicitly assembles them
at the Akademia's shelf. The shelf remains usable while Daphne is away, with
her written notes, all twelve distinct 64x64 black-figure paintings, saved
restoration flags and repeat reading. Hephaestus's and Paris's restorations
grant their gods five Favor once. All twelve restored amphorae reveal Daphne's
last written lecture and one Ability Patch, with a saved full-Bag retry.
The three Act I leads are playable after actual restoration: Kronion's altar
offers Cairnolith Lv20 at night (Sand Force, Hard Stone), the Hollow's web
chamber offers Raknit Lv20 (Defiant), and Eleusa's meadow offers Persenyx Lv22
at dusk. Escape, declined approach and whiteout preserve the encounters;
victory/capture claim independent saved flags. Raknit and Persenyx disappear
immediately when claimed, rather than requiring reentry. Dusk arrivals/expiry
refresh safely on the live field, deferring during scripts, the Frozen Hour
and occupied arrival tiles. The existing Korantha omen is now in reachable
wheat outside the sealed Rharian field; the sacred fence remains intact.
The start menu's DEEDS entry now opens the Scroll of Deeds, on the existing
pottery frame without replacing the trainer card. Its Act I pages follow
saved story receipts, including the Mysteries, Kleon's departure, the
revelation, the letter home and Mom's pending gift. Daedalus's pages and
anointed herms have collection counts. Amphora pages distinguish collected
sherds, explicit restoration, recorded later-region clues and the three
completed Act I encounters. Athena's Stylus adds hints to open quests.
The calendar page uses the existing 36-day Attic year, including the
festival-free storm month; it does not claim that all festival events exist.
Other amphora world callers and later-chapter quest pages remain unfinished.
The Star Chart now opens from the key-item Bag as a parchment sky, with
24 distinct star-and-line patterns, a twinkling palette, directional
navigation and a clean return to the same Bag pocket. Unplaced myths stay
blank, including the final Unwoven patch. Saved constellation flags record
the known Conch, Laurel 4/5/7/8, Favor-30 Artemis/Hera and seven-page gates.
Legacy progress is recovered when the chart opens; reading cannot invent
the remaining myths. Outdoor stargazing seats, milestone rewards and the
remaining story/post-game constellation callers are not yet integrated.
The sanctum now continues through Kleon's departure and Daphne's revelation,
with both dialogue branches, one real Star Chart, and independent saved Act I
completion flags instead of a fourth-Laurel alias. Full key-item pockets cannot
skip the Sickle or complete the revelation without its reward; both can be
retried after making room. The closing run exercises both branches, restored
braziers, repeat entry and save/CONTINUE. The north vines require the Sickle;
Alethea leaves after the player passes them, and the herald blocks the next
chapter until it exists. Gate and companion state persist across saves.
The revelation now displays an original clay-tablet close-up while Daphne
reads its back, then closes on a centered pottery-framed Act I title card
that waits for A or B. Both dialogue branches retain their speaker names,
release the scene windows and restore borrowed palettes before returning
outside. The Chart has its own rolled-sky Bag icon instead of borrowing the
Town Map. This is not final scene-art or human acceptance: lamp staging
and dedicated music remain unfinished.

**Continuation order.** Close and approve Act I first. Integrate shared systems at
their first story use, then build connected Act II and Act III chapters. For post-game
implementation, follow approved PG-2: sailing → Olympia → Katabasis → Labors →
Odyssey → Atlantis → summit, with Oikoumene lands alongside, near lands first.
This is a build order, not a new forced player quest order. Keep the deferred Astral
type/species expansion separate from the required 24-constellation collectible chart.

**Every chapter's gate.** Build and opening smoke pass; relevant Lua and continuous
progression checks pass; loss/reentry/save recovery works; encounters and teams follow
BALANCE.md; visible scenes and measured text are reviewed; map render/critique passes
follow phase2/BUILD.md. Obtain human approval before scaling. Run expansion engine
tests for shared-engine changes and release gates. Preserve the installed player's
ROM/save; a save-incompatible change needs explicit approval.

---

## 9. Against the competition

| | Glazed | Lazarus | **Ichor** |
|---|---|---|---|
| Engine | 2012 binary hack | Emerald | Modern decomp, expansion 1.17 |
| Pokémon | Gen 1–6 | 400+ (Gen 1–9) | **Gen 1–9, all 1,025 catchable** |
| Setting | Tunod, Johto, Rankor | Modern Greece-flavored Ilios, with Pokémon Centers | **Ancient era**: no modern tech, with myth as the story's spine |
| Gyms | Standard | The Muses | **The Twelve Olympians**; Hades waits in the post-game |
| Art | Gen 3 | GBC style | Gen 3 full color, with a pottery-painted UI |
| Post-game | Johto, legendary hunts, World Championship | Wakewater Isle | **Six arcs**, including a Battle Frontier |
| QoL | No speed-up, dated | Modern | Full 2026 suite |

Sources: `research/RESEARCH.md` and `research/LAZARUS.md`.

---

## 10. Risks and open decisions

1. **Lazarus.** A Greek-themed Emerald hack already shipped. We differentiate through the ancient-era setting, a story built on fate, Olympian temples, the full National Dex, the pottery art direction and the post-game.
   - We avoid what it already uses: Muse gym leaders, a Chimera team, Mega-as-weapon plots, its nine starters, and Greek-prefixed custom forms.
   - See `research/LAZARUS.md`.
2. **AI-content bans.** Resolved 2026-11-14: Ichor is a private project for the user and won't be released, so PokéCommunity's and Eevee Expo's bans on AI-made art and writing don't apply.
3. **Art quality is the bottleneck.** Mitigations:
   - Plan palettes first.
   - Use the Porytiles pipeline.
   - Use credited free resources.
   - Approve the look at the Phase 1 gate before building more.
4. **Legal.** Non-commercial, patch only, players bring their own Emerald ROM, never distribute a ROM.
5. **ROM space.** The cartridge limit is 32 MB. We measure it in Phase 0, and art and music are budgeted against it.
6. **Playtesting.** We automate crash and flow tests. Whether it is fun and well-balanced needs a human player.
7. **The install needs your password once.** The devkitPro installer runs `sudo`.
