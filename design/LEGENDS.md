# Legends: every legendary and mythical Pokémon

- **Owner:** World and quest design. **Status:** a proposal for the user's approval, written 2026-11-14. Nothing here changes a game file.
- **The brief, in the user's words:** "post game we will need events, caves etc that are for catching all the other legendaries from the other movies. each should have a tiny story tasks puzzles needed to catch them like always." And: "eventually you should be able to get every pokemon."
- **What this file owns:** every legendary, mythical, Ultra Beast and Paradox Pokémon that the main story and the post-game epics don't place: where it lives, its myth, its quest, its battle and what it unlocks. The master table (§2) lists all of them, the ones placed elsewhere included.
- **Companions:** `design/OIKOUMENE.md`, the second chart, where most of these live; `design/oikoumene/COVERAGE.md`, where every other species lives.
- **Sources:** `PITCH.md` §4 and §6, `STORY.md` (approved; §2's casting table and §3's post-game spine), `SYSTEMS.md` (approved: relics, rites, theoxenia, the star chart, festivals, omens), `LABYRINTH.md`, `BALANCE.md`, `MAP_DESIGN.md`, `research/LAZARUS.md`, the dex branch (`design/dex/`), and the engine as cited.
- **Overlap.** `LABORS.md`, `UNDERWORLD.md`, `ODYSSEY.md` and `POSTGAME.md` belong to another designer. Where they place a legendary, this file lists it as "placed by" that doc and doesn't redesign it. This revision is reconciled with `POSTGAME.md` §4: where the two disagreed, the epic won, and §8 lists every legend that moved. The decisions are consolidated with POSTGAME's P1–P11 in `OIKOUMENE.md` §13.

---

## Contents

0. The rules every legendary quest follows
1. Why legends walk the world now, and the two frayed edges
2. The master table
3. Trios, pairs and families
4. Single legends and mythicals
5. Time Fractures: the Paradox Pokémon
6. Beyond the Selvage: the Ultra Beasts
7. In Aethos's post-game
8. Placed elsewhere: notes for the other docs
9. Engine feasibility
10. The 100%: completing the Oikoumene Dex
11. Scope, ROM and decisions

---

## 0. The rules every legendary quest follows

1. **A tiny story, tasks and puzzles.** Every quest has three to six steps: someone who asks, a task or puzzle, a trigger, and a staged encounter. No legend is a sprite standing in a cave waiting.
2. **No two quests alike.** Across the file the verbs are spread on purpose: chases, riddles, escorts, offerings, timing, festival days, an ordering puzzle, alternate days, constellations, carried flames, mirrors, moral tests, deliveries, music, reasoning. §11 tallies them.
3. **Myth woven in, never lectured.** A character says one line about the myth, in their own voice, and the mechanic does the rest.
4. **One only.** Every legendary is a single static or gift. If it faints, it returns the next day at the same spot until caught (an Ichor convenience, so nobody softlocks a 100%).
5. **Levels follow `BALANCE.md`:** legendaries 70–80, the strongest 85–92. Arceus at Lv 95 (`POSTGAME.md` §3.3) stays the game's strongest battle, and nothing here passes it.
6. **Gates are post-game only.** No legend sits on the main path. Most need the Oikoumene, whose near lands open with the ship from the post-game's start; the Western Sea's wait for the Odyssey, and Okeanos's for Aeolus's Bag (OIKOUMENE §2). Some live in Aethos's post-game.
7. **Nothing requires luck.** Timed quests (hours, days, festivals) can be met by waiting, or by resting with a xenia host (SYSTEMS §10).
8. **The cast comes back.** Most quests are carried by someone the player already loves: Alethea, Kleon, Elpis, Hyperion, Daphne, Ariadne, Thespis, Hypatia, the Fates, Mom.

---

## 1. Why legends walk the world now, and the two frayed edges

**The world after fate.** Under Medon's chains every knot was fixed. Even legends kept to their appointed hours: the Phoenix every five hundred years, the wish-star every thousand. Now nothing is appointed (STORY §1, rule 9), and the old schedules have come loose. That is the reason, given in a line or two by whoever's nearby, for legends turning up in a cave or on a mountain.

**The two frayed edges of the cloth.** The Loom's cloth has two kinds of edge, as every weaver knows.

| Edge | In weaving | In Ichor | What comes through |
|---|---|---|---|
| **The ends** | Where the weaving starts and where it stops | **Time.** When the hero seized the Moment, time went on past the old cloth's last row (STORY §1, rule 9). The cut ends fray. | **Paradox Pokémon**, from the ages before and after (§5) |
| **The selvages** | The two side edges, where the weft turns back | **Space.** The Loom wove the whole world out to Okeanos. Past the rim is cloth that was never woven. | **Ultra Beasts**, from beyond the world's edge (§6) |

- **Paradox Pokémon come from Hesiod's ages.** Hesiod sang five races of men: Golden, Silver, Bronze, the Heroes, and the Iron race he lived in and dreaded (*Works and Days* 109–201). Ichor is set in the age of heroes, so the past is gold and the future is iron.
  - The ancient Paradox Pokémon are **the Golden Age**, the age of Kronos, when the earth bore fruit unbidden. Koraidon is its mount.
  - The future Paradox Pokémon are **the Age of Iron**. The game's own species names already say "Iron." Miraidon is its mount.
  - Because nothing is woven ahead any more, the Iron Age is a possible future, not a fated one. "It might not come. Nobody wove it."
- **Ultra Beasts are unwoven.** They come from past the selvage, where nothing was ever on the Loom. They have no threads, like the hero. That is why they feel wrong to everyone else, and why Lotira, the Measurer, notices them: "There's something out there we can't measure. Again. You're not the only one now."

---

## 2. The master table

Every legendary, mythical, Ultra Beast and Paradox Pokémon in the National Dex, plus the Aethos dex's own. "Placed by" names the doc that owns the encounter; where it's this one, the quest is in the section given.

**Gates:** *League* means the post-game; *Ship* means the Oikoumene's near lands, open with the trireme from the post-game's start; *Odyssey* means after the voyage (the Western Sea's towns, and Aeolus's Bag for Okeanos). Levels are the encounter's.

### The National Dex

| # | Pokémon | Cast as | Where | Quest | Placed by | Gate | Lv |
|---:|---|---|---|---|---|---|---|
| 144 | Articuno | The eagle of the north | The Feather Wastes, Scythia | The Eagles of the Edges (§3.1) | LEGENDS | Ship | 75 |
| 145 | Zapdos | The eagle of the east | Gargaros Peak, the Troad | The Eagles of the Edges | LEGENDS (PG-27) | Ship | 75 |
| 146 | Moltres | The eagle of the west | The Atlas Range, at sunset | The Eagles of the Edges | LEGENDS | Labor 10, or the Odyssey | 75 |
| 150 | Mewtwo | A thing made into a monster | The Gorgons' Isle, Okeanos | Look Only in the Mirror (§4.2) | LEGENDS | The Cave of the Graiai; ODYSSEY's Mirror of Truth | 90 |
| 151 | Mew | The first clay | The Caucasus caves, below LABORS's crag | The First Clay (§3.8) | LEGENDS | `LABORS.md` Labor 11 (Prometheus freed) | 75 |
| 243 | Raikou | The wanderer of Libya | Omens across Egypt, Libya, Aithiopia | The Three Shares of the Earth (§3.2) | LEGENDS | Ship | 72 |
| 244 | Entei | The wanderer of Asia | Omens across the Troad, Lydia, the Euxine | The Three Shares of the Earth | LEGENDS | Ship | 72 |
| 245 | Suicune | The wanderer of Europe | Omens across Thrace, Scythia, the West | The Three Shares of the Earth | LEGENDS | Ship | 72 |
| 249 | Lugia | Leukothea, the white sea-goddess | Atlantis's abyss | — | `POSTGAME.md` §3.2 | Atlantis | 80 |
| 250 | Ho-Oh | The Phoenix of Heliopolis | Heliopolis, Egypt | The Egg of Myrrh (§3.2) | LEGENDS | The three wanderers | 78 |
| 251 | Celebi | The Hour that stopped | Akti, then the Time Fractures | The Thirteenth Hour (§7.1) | LEGENDS | Five fractures visited | 70 |
| 377 | Regirock | A Titan in Tartarus | Tartarus's five cells | — | `UNDERWORLD.md` §4.10 | The Katabasis | 75 |
| 378 | Regice | A Titan in Tartarus | Tartarus's five cells | — | `UNDERWORLD.md` §4.10 | The Katabasis | 75 |
| 379 | Registeel | A Titan in Tartarus | Tartarus's five cells | — | `UNDERWORLD.md` §4.10 | The Katabasis | 75 |
| 380 | Latias | The Dioskouroi, the saviors of sailors | Lakonia, then the sea lanes, even days | The Twin Lights (§3.4) | LEGENDS | Ship | 72 |
| 381 | Latios | The Dioskouroi | The sea lanes, odd days | The Twin Lights | LEGENDS | Ship | 72 |
| 382 | Kyogre | Oceanus, the world-river | The edge of the world, below Atlantis | — | `POSTGAME.md` §3.3 | Atlantis | 88 |
| 383 | Groudon | Gaia, the Earth | Under Delphoi | — | `POSTGAME.md` §3.3 | The Katabasis | 88 |
| 384 | Rayquaza | Ouranos, the Sky | Above Olympus's clouds | — | `POSTGAME.md` §3.3 | The Kotinos | 88 |
| 385 | Jirachi | The wish-star that slept a thousand years | The Atlas Range's summit | The Thousand-Year Star (§4.3) | LEGENDS | All 24 constellations (SYSTEMS §8) | 75 |
| 386 | Deoxys | The things that fell from the sky | Ilion, the temple of Athena | The Things That Fell (§4.4) | LEGENDS | Ship | 78 |
| 480 | Uxie | Reason, the charioteer of the soul | Lake Moeris, Egypt | The Charioteer (§3.3) | LEGENDS | Ship | 70 |
| 481 | Mesprit | Desire, the dark horse | Lake Tritonis, Libya | The Charioteer | LEGENDS | Ship | 70 |
| 482 | Azelf | Spirit, the white horse | Lake Maeotis, Scythia | The Charioteer | LEGENDS | Ship | 70 |
| 483 | Dialga | Chronos: time that goes on, "a moving image of eternity" | The Gates of the Sun, Okeanos | Time and Room (§3.5) | LEGENDS | The Charioteer | 80 |
| 484 | Palkia | Chora: the room the world sits in | The Selvage, Okeanos | Time and Room | LEGENDS | The Charioteer | 80 |
| 485 | Heatran | The fire under the forge | Kaldera (Aethos) | The Forge Under the Forge (§7.2) | LEGENDS | League | 72 |
| 486 | Regigigas | Briareus's charge, the Titans' keeper | Tartarus's inner gate | — | `UNDERWORLD.md` §4.10 | All five Titans | 80 |
| 487 | Giratina | Tartaros, the primordial pit | The Chasm | — | `UNDERWORLD.md` §4.11 | The Katabasis | 80 |
| 488 | Cresselia | The true dream | The House of Night, Tartarus's edge | — | `UNDERWORLD.md` §6 (stretch; PG-26) | The Katabasis | 78 |
| 489 | Phione | — | Breed Manaphy with Ditto (Pharos) | — | `POSTGAME.md`, by breeding | — | — |
| 490 | Manaphy | The sea's prince | Atlantis's coral nursery, an egg | — | `POSTGAME.md` §3.2 (stretch) | Atlantis | — |
| 491 | Darkrai | The false dream | The House of Night, Tartarus's edge | — | `UNDERWORLD.md` §6 (stretch; PG-26) | The Katabasis | 78 |
| 492 | Shaymin | *Charis*, gratitude | The Isles of the Blessed, at the Pyanopsia | Thank-Offerings (§4.5) | LEGENDS | The Isles | 70 |
| 493 | Arceus | The Prime Mover | Olympus's true summit | — | `POSTGAME.md` §3.3 | The four keys, the three Primordials | 95 |
| 494 | Victini | Nike, victory | Olympia, the Nike's pillar | — | `POSTGAME.md` §3.1 | All five Olympiad gold symbols | 80 |
| 638 | Cobalion | Eunomia, Good Order | Sardis, with Solon | The Hours of Justice (§3.7) | LEGENDS | Ship | 74 |
| 639 | Terrakion | Dike, Justice | Ammonion, Libya | The Hours of Justice | LEGENDS | Ship | 74 |
| 640 | Virizion | Eirene, Peace | Meroë, Aithiopia | The Hours of Justice | LEGENDS | Ship | 74 |
| 641 | Tornadus | The storm wind let out of Aeolus's bag | The wine-dark sea | — | `ODYSSEY.md` §6.4 | The Odyssey | 75 |
| 642 | Thundurus | The storm that got out of the bag | The Great Sand Sea's storms | What Came Out of the Bag (§3.9) | LEGENDS | The Odyssey (Aiolia) | 76 |
| 643 | Reshiram | *Aletheia*, truth | Memphis, Egypt | The Truth and the Glory (§3.10) | LEGENDS | Ship; Alethea | 80 |
| 644 | Zekrom | *Kleos*, the glory that won't die | The Skaian Gate, Ilion | The Truth and the Glory | LEGENDS | Ship; Kleon | 80 |
| 645 | Landorus | The earth's own plenty | The Table of the Sun, Aithiopia | What Came Out of the Bag | LEGENDS | Thundurus | 76 |
| 646 | Kyurem | The hollow half | The Cave of Boreas | The Other Half (§3.10) | LEGENDS | Reshiram or Zekrom | 82 |
| 647 | Keldeo | Astraea, the last immortal to leave the earth | The Isles of the Blessed | The Hours of Justice | LEGENDS | The three Hours | 75 |
| 648 | Meloetta | Orpheus's song | The mouth of the Hebros, Thrace | The Singing Head (§4.7) | LEGENDS | Orpheus amphora (SYSTEMS §5); Lyre of Apollo | 72 |
| 649 | Genesect | Tithonus, in Memnon's armor | Eos's palace, the Gate of Dawn | The Man Who Couldn't Stop (§4.8) | LEGENDS | Ship | 75 |
| 716 | Xerneas | The Golden Hind | The Ladon ford, Arkadia | — | `LABORS.md` Labor 3 | The Labors | 72 |
| 717 | Yveltal | The dark bird of the Isle of Ares | The Isle of Ares, the Black Sea | The Isle of Ares (§3.8) | LEGENDS | `LABORS.md` Labors 6 and 9 | 80 |
| 718 | Zygarde | Osiris, scattered and gathered | Abydos; cells across the Oikoumene | Fourteen Pieces (§4.9) | LEGENDS | Ship | 78 |
| 719 | Diancie | The last stone of Ariadne's crown | Mount Nysa, Aithiopia | The Crown's Last Stone (§4.10) | LEGENDS | Corona Borealis (LABYRINTH) | 74 |
| 720 | Hoopa | The Ring of Gyges | The Chasm of Gyges, Lydia | The Ring of Gyges (§4.11) | LEGENDS | Ship | 76 |
| 721 | Volcanion | The Giant under the burning fields | The Phlegraean Fields | Steam and Stone (§4.12) | LEGENDS | Odyssey | 76 |
| 772 | Type: Null | Daedalus's statue that runs away | Daedalus's workshop, Knossa | The Statue That Runs Away (§7.3) | LEGENDS | League | 70 (gift) |
| 773 | Silvally | — | Evolve Type: Null (friendship) | The Statue That Runs Away | LEGENDS | — | — |
| 785 | Tapu Koko | Elektra, "amber-bright," an Okeanid | The Isles of the Blessed | The Keepers of the Isles (§3.11) | LEGENDS | The Isles | 76 |
| 786 | Tapu Lele | Metis, "wise counsel," an Okeanid | The Isles of the Blessed | The Keepers of the Isles | LEGENDS | The Isles | 76 |
| 787 | Tapu Bulu | Plouto, "plenty," an Okeanid | The Isles of the Blessed | The Keepers of the Isles | LEGENDS | The Isles | 76 |
| 788 | Tapu Fini | Amphirho, "flowing round," an Okeanid | The Isles of the Blessed | The Keepers of the Isles | LEGENDS | The Isles | 76 |
| 789 | Cosmog | A light only a blind man sees | Kaldera (Aethos), from Hyperion | Hyperion's Children (§3.12) | LEGENDS | League | 42 (gift) |
| 790 | Cosmoem | — | Evolve Cosmog, Lv 43 | Hyperion's Children | LEGENDS | — | — |
| 791 | Solgaleo | Helios, the sun | The Gate of Dawn | Hyperion's Children | LEGENDS | Cosmog | 80 |
| 792 | Lunala | Selene, the moon | Mount Latmos, Lydia | Hyperion's Children | LEGENDS | Cosmog | 80 |
| 793 | Nihilego | Pytheas's "sea-lung" at the top of the world | The Selvage, north | Beyond the Selvage (§6) | LEGENDS | Lotira | 74 |
| 794 | Buzzwole | What the gnat-towers were built against | The Delta Reeds, Egypt | Beyond the Selvage | LEGENDS | Lotira | 74 |
| 795 | Pheromosa | The Astomi, who live on scent | The Gate of Dawn | Beyond the Selvage | LEGENDS | Lotira | 74 |
| 796 | Xurkitree | The tree that grows lightning | The Great Sand Sea | Beyond the Selvage | LEGENDS | Lotira | 74 |
| 797 | Celesteela | The arrow that flies by itself | The Hyperborean Meadow | Beyond the Selvage | LEGENDS | Lotira | 76 |
| 798 | Kartana | The papyrus that cuts | The Labyrinth of Moeris | Beyond the Selvage | LEGENDS | Lotira | 74 |
| 799 | Guzzlord | The guest who ate the Table of the Sun | The Table of the Sun | Beyond the Selvage | LEGENDS | Lotira | 78 |
| 800 | Necrozma | The eclipse that eats the light | The Halys ford, Lydia | The Day Turned to Night (§3.12) | LEGENDS | Solgaleo and Lunala | 85 |
| 801 | Magearna | Hephaestus's golden handmaid | Kaldera's forge | The Golden Handmaid (§7.4) | `SYSTEMS.md` §3 gift III, staged here | Hephaestus Favor 100 | 75 |
| 802 | Marshadow | The shadow a god left behind | Your home, Elaia | The Shadow Hermes Left (§7.5) | LEGENDS | The theoxenia finale | 75 |
| 803 | Poipole | A beast from beyond that likes you | The Selvage | Beyond the Selvage | LEGENDS | Lotira | 70 (gift) |
| 804 | Naganadel | — | Evolve Poipole (knowing Dragon Pulse) | Beyond the Selvage | LEGENDS | — | — |
| 805 | Stakataka | A stretch of Troy's god-built wall that walks | The Walls of Laomedon | Beyond the Selvage | LEGENDS | Lotira | 76 |
| 806 | Blacephalon | The Blemmyes, the headless men | The Salt Ridge, Libya | Beyond the Selvage | LEGENDS | Lotira | 76 |
| 807 | Zeraora | The spark in Thales's amber | Miletos, Lydia | The Amber Spark (§4.13) | LEGENDS | Ship | 75 |
| 808 | Meltan | The first iron | The Chalybes' forges | The First Iron (§4.14) | LEGENDS | Ship | 70 |
| 809 | Melmetal | What the furnace pours | The Chalybes' great furnace | The First Iron | LEGENDS | 40 Meltan's iron | 80 |
| 888 | Zacian | The sword: a short life, and glory | Leuke, the White Isle | The Shield With the World on It (§3.13) | LEGENDS | Ship; Achilles | 85 |
| 889 | Zamazenta | The shield: a long life, and the whole world on it | Leuke | The Shield With the World on It | LEGENDS | Ship; Achilles | 85 |
| 890 | Eternatus | The day the sun fell | The Glass Crater, Libya | The Day the Sun Fell (§4.15) | LEGENDS | Eight Periodos panels | 92 |
| 891 | Kubfu | Milo's calf | Kroton | Milo's Calf (§4.16) | LEGENDS | Odyssey | 70 (gift) |
| 892 | Urshifu | — | Evolve Kubfu: the unlit tower or the strait | Milo's Calf | LEGENDS | — | — |
| 893 | Zarude | Dionysus's foster-nurses | The Mountains of the Moon | The Foster-Father (§4.17) | LEGENDS | Ship | 76 |
| 894 | Regieleki | A Titan in Tartarus | Tartarus's five cells | — | `UNDERWORLD.md` §4.10 | The Katabasis | 75 |
| 895 | Regidrago | A Titan in Tartarus | Tartarus's five cells | — | `UNDERWORLD.md` §4.10 | The Katabasis | 75 |
| 896 | Glastrier | The mares of Boreas | The Cave of Boreas | The Straw Offerings (§3.14) | LEGENDS | Calyrex's quest | 78 |
| 897 | Spectrier | The black horses of the dead | The Cimmerian Shore | The Straw Offerings | LEGENDS | Calyrex's quest | 78 |
| 898 | Calyrex | The forgotten king of the Hyperborean harvest | The round temple, Hyperborea | The Straw Offerings | LEGENDS | Ship | 80 |
| 905 | Enamorus | The love that changes things | The Spring of Kallirhoe, Kythera (Aethos) | What Came Out of the Bag | LEGENDS | Landorus | 76 |
| 984 | Great Tusk | The Golden Age | Kronion Hill's fracture | Time Fractures (§5) | LEGENDS | League | 66–70 |
| 985 | Scream Tail | The Golden Age | Eleusa's fracture | Time Fractures | LEGENDS | League | 66–70 |
| 986 | Brute Bonnet | The Golden Age | Eleusa's fracture | Time Fractures | LEGENDS | League | 66–70 |
| 987 | Flutter Mane | The Golden Age | Delphoi's fracture | Time Fractures | LEGENDS | League | 66–70 |
| 988 | Slither Wing | The Golden Age | Kaldera's fracture | Time Fractures | LEGENDS | League | 66–70 |
| 989 | Sandy Shocks | The Golden Age | Kronion Hill's fracture | Time Fractures | LEGENDS | League | 66–70 |
| 990 | Iron Treads | The Iron Age | The Chalybes' fracture | Time Fractures | LEGENDS | Ship | 74–78 |
| 991 | Iron Bundle | The Iron Age | The Cave of Boreas's fracture | Time Fractures | LEGENDS | Ship | 74–78 |
| 992 | Iron Hands | The Iron Age | The Chalybes' fracture | Time Fractures | LEGENDS | Ship | 74–78 |
| 993 | Iron Jugulis | The Iron Age | The Glass Crater's fracture | Time Fractures | LEGENDS | Ship | 74–78 |
| 994 | Iron Moth | The Iron Age | The Glass Crater's fracture | Time Fractures | LEGENDS | Ship | 74–78 |
| 995 | Iron Thorns | The Iron Age | The Walls of Laomedon's fracture | Time Fractures | LEGENDS | Ship | 74–78 |
| 1001 | Wo-Chien | Limos, Famine | The Steppe Road, Scythia | What Stayed in the Jar (§3.15) | LEGENDS | Ship; Elpis | 78 |
| 1002 | Chien-Pao | Phthonos, Envy | The treasury of Sardis | What Stayed in the Jar | LEGENDS | Ship; Elpis | 78 |
| 1003 | Ting-Lu | Geras, Old Age | The Fountain of the Long-Lived | What Stayed in the Jar | LEGENDS | Ship; Elpis | 78 |
| 1004 | Chi-Yu | Eris, Strife | Ilion | What Stayed in the Jar | LEGENDS | Ship; Elpis | 78 |
| 1005 | Roaring Moon | The Golden Age | Lakonia's fracture, on Taygetos | Time Fractures | LEGENDS | League | 66–70 |
| 1006 | Iron Valiant | The Iron Age | The Walls of Laomedon's fracture | Time Fractures | LEGENDS | Ship | 74–78 |
| 1007 | Koraidon | The Golden Age's mount | The Isles of the Blessed | The Two Mounts (§5) | LEGENDS | All eleven fractures | 85 |
| 1008 | Miraidon | The Iron Age's mount | The Chalybes' great furnace | The Two Mounts | LEGENDS | All eleven fractures | 85 |
| 1009 | Walking Wake | Suicune in the Golden Age | Heliopolis's fracture | Time Fractures | LEGENDS | Ho-Oh | 74–78 |
| 1010 | Iron Leaves | Virizion in the Iron Age | The Selvage's fracture | Time Fractures | LEGENDS | Keldeo | 74–78 |
| 1014 | Okidogi | One of three false heroes | Thyrsa's vineyards (Aethos) | The Satyr Play Nobody Wrote (§7.6) | LEGENDS | League; the Anthesteria | 74 |
| 1015 | Munkidori | One of three false heroes | Thyrsa's vineyards | The Satyr Play Nobody Wrote | LEGENDS | League | 74 |
| 1016 | Fezandipiti | One of three false heroes | Thyrsa's vineyards | The Satyr Play Nobody Wrote | LEGENDS | League | 74 |
| 1017 | Ogerpon | The Dionysia's masks: the satyr who was the hero | Thyrsa's vineyards | The Satyr Play Nobody Wrote | LEGENDS (PITCH §4's casting) | League | 76 |
| 1020 | Gouging Fire | Entei in the Golden Age | Heliopolis's fracture | Time Fractures | LEGENDS | Ho-Oh | 74–78 |
| 1021 | Raging Bolt | Raikou in the Golden Age | Heliopolis's fracture | Time Fractures | LEGENDS | Ho-Oh | 74–78 |
| 1022 | Iron Boulder | Terrakion in the Iron Age | The Selvage's fracture | Time Fractures | LEGENDS | Keldeo | 74–78 |
| 1023 | Iron Crown | Cobalion in the Iron Age | The Selvage's fracture | Time Fractures | LEGENDS | Keldeo | 74–78 |
| 1024 | Terapagos | Zeno's tortoise | Elea, the Western Sea | Achilles and the Tortoise (§4.18) | LEGENDS | Odyssey | 90 |
| 1025 | Pecharunt | Methe, the poisoned vintage | Thyrsa's wine-jars, at the Anthesteria | The Satyr Play Nobody Wrote | LEGENDS | League; the Anthesteria | 78 |

### The Aethos dex's own

| # | Pokémon | Cast as | Where | Placed by | Lv |
|---:|---|---|---|---|---|
| 98 | Asterlorn | Asterion, the Minotaur | Knossa; joins after Ariadne's gold symbol | `LABYRINTH.md` §10 | 60 |
| 143–145 | Nemira, Lotira, Thanira | The three Fates | Their three sanctuaries after the climax | `STORY.md` §2 and the dex | 60 (the dex team's level) |
| 146 | Kronolith | The Lord of Time | The Stair of Hours; rematch in the deep under the Omphalos | `STORY.md` | 60 |
| 147 | Kairazor | The Moment | Olympia's altar of Kairos | `POSTGAME.md` §3.1 | 78 |
| 148 | Pegaunos | Zeus's thunder-horse | Olympus's cloud meadows, after the Kotinos | `POSTGAME.md` §3.4 | 80 |
| 149–151 | Olympanax, Pontanax, Nekranax | The three brothers' colossi | Olympus's storm terrace, Atlantis's temple, the vault beneath Hades's hall | `POSTGAME.md` §3.4 (dex D4: the three lots) | 80 |
| 152 | Ichorin | The first myth | The Pool of Mnemosyne, with Mnemosyne's Water from the Katabasis | `POSTGAME.md` §3.4 | 70 (the dex team's level) |

### By where they live

| Home | Count |
|---|---:|
| **The Oikoumene**, quests in this file | **85** |
| **Aethos's post-game**, quests in this file | **20** |
| `SYSTEMS.md` (Magearna, staged here in §7.4) | 1 |
| `POSTGAME.md` (Lugia, Kyogre, Groudon, Rayquaza, Manaphy, Phione by breeding, Arceus, Victini) | 8 |
| `UNDERWORLD.md` (Regirock, Regice, Registeel, Regieleki, Regidrago, Regigigas, Giratina, and Cresselia and Darkrai in the House of Night) | 9 |
| `ODYSSEY.md` (Tornadus) | 1 |
| `LABORS.md` (Xerneas) | 1 |
| **All National Dex legends** | **125** |
| The Aethos dex's own, placed by STORY, LABYRINTH, POSTGAME and the dex | 11 |

- **The Oikoumene's 85** are the three birds, Mewtwo and Mew, the three wanderers and Ho-Oh, Latias and Latios (caught at sea there), Jirachi, Deoxys, the soul trio, Dialga and Palkia, Shaymin, the four Hours with Keldeo, Thundurus, Landorus, Reshiram, Zekrom, Kyurem, Meloetta, Genesect, Yveltal, Zygarde, Diancie, Hoopa, Volcanion, the four Tapus, Solgaleo, Lunala, Necrozma, the eleven Ultra Beasts (Naganadel included), Zeraora, Meltan, Melmetal, Zacian, Zamazenta, Eternatus, Kubfu and Urshifu, Zarude, Calyrex and both horses, the four Treasures, the ten Iron Paradox Pokémon, the three Golden beasts at Heliopolis, Koraidon, Miraidon and Terapagos.
- **Aethos's 20** are Celebi, Heatran, Type: Null and Silvally, Cosmog and Cosmoem (from Hyperion), Marshadow, Enamorus, the Thyrsa five (Ogerpon, the Loyal Three, Pecharunt), and the seven Golden Paradox Pokémon in Aethos's fractures.
- **Reconciled with POSTGAME §4.** Everything that file lists as "placed" is marked "placed by" its doc above. Its "proposed only" list (Ho-Oh, Heatran, Meloetta, Enamorus, Latias and Latios, the Treasures, Ogerpon, the Paradox Pokémon, the Ultra Beasts) is this file's, as it says. Two of this file's first-draft quests gave way: Victini is POSTGAME's Nike at Olympia, and Cresselia and Darkrai are UNDERWORLD's, in the House of Night.

---

## 3. Trios, pairs and families

### 3.1 Articuno, Zapdos and Moltres: The Eagles of the Edges

**The myth.** Zeus wanted to know where the middle of the world was. He let two eagles go from its two ends, and they met over Delphi (Pindar, fr. 54; Strabo 9.3.6). Two gold eagles stood on the Omphalos ever after.

**Ichor's telling.** There were three: one from the frozen north, one from the sunrise, one from the sunset. With prophecy over, the Omphalos is just a stone. The three eagles have gone home to the edges.

**Where and gate.** The Feather Wastes (north), Gargaros Peak (east, over Troy), the Atlas Range at sunset (west). Any order: the first two open with the ship, the third with Labor 10's cup or by sea after the Odyssey.

**The quest.**
1. **The empty perch.** At Delphoi, the Pythia shows you the Omphalos's two eagle sockets, and a third nobody remarked on. "There were three. Nobody counted. I counted." She gives you a gold feather that turns in your hand to point at the nearest edge.
2. **The north: the real feather.** Herodotus says the Scythians call snow feathers (4.31). On the Feather Wastes a blizzard of white feathers fills every screen. One feather per screen is gold and glints when you face it. Follow only those, screen to screen, to Articuno's eyrie. Follow a white one and the blizzard walks you back to the start of the screen.
3. **The east: the shepherd boy.** On Ida a shepherd boy named Ganymedes has gone up Gargaros to see the great eagle. His mother asks you to fetch him. You chase him up three floors of ledges; he's faster than you. At the top he is sitting quietly with Zapdos, which hasn't carried him off. "It just looked at me. I think it was lonely." Escort him down; Zapdos follows to the peak's lip and waits for you.
4. **The west: the hour.** At Atlas's shoulder the sun sets into Okeanos. Moltres rises out of the sunset only in the evening hour (19:00–20:00, `include/constants/rtc.h`). Arrive early and the Titan's voice rumbles: "Wait. It's always worth it." A xenia host at Gadeira can rest you till dusk.
5. **The three perches.** Catch all three and the gold feather settles. Back at Delphoi the Pythia lays it on the Omphalos.

```text
PYTHIA: Three eagles, to find the middle of the world.

PYTHIA: Now nobody's thread runs through here. So where's the middle?

PYTHIA: …Wherever you're standing, I suppose. Sit down. That's the navel now.
```

**Battles.** Each Lv 75, alone.
- Articuno: Freeze-Dry, Hurricane, Roost, Mind Reader. Snow falls on its screen.
- Zapdos: Thunder, Hurricane, Roost, Discharge. Rain on Gargaros's peak.
- Moltres: Fire Blast, Hurricane, Roost, Sky Attack. Harsh sunlight in the sunset.

**Reward.** The gold feather becomes the **Pythia's Feather**, a key item: the Pythia's "Know thyself" (SYSTEMS §11) costs one Pythian Laurel less per use.

**SYSTEMS change (decision PG-27).** SYSTEMS §3 makes Zapdos Zeus's gift III. STORY §2 already moved Zeus's eagle to the dex's **Aetarch**, the Archon's ace. So Zeus's gift III should be a unique Aetarch, the true eagle of Zeus, and Zapdos joins its trio here.

### 3.2 Raikou, Entei and Suicune, then Ho-Oh: The Three Shares of the Earth and The Egg of Myrrh

**The casting.** Herodotus divides the world into three, Europe, Asia and Libya, and finds it odd that three women's names were given to one earth (4.45). The three beasts are those three shares, each roaming its own: Raikou is Libya's thunderstorms, Entei Asia's volcanic heart, Suicune Europe's cold clean rivers. They were made, in Ichor's telling, from what was left of the last Phoenix's pyre.

**The Lazarus check.** Lazarus has a Greek-named legendary beast trio. Ichor's beasts keep their own names, aren't a story trio, and appear as wanderers in a side quest. Nothing here gives them Greek names.

**Where and how.** They don't roam in the engine's sense (`ROAMER_COUNT` is 1, `include/constants/global.h`). Each is a **wanderer** on the daily omen (SYSTEMS §6): the Oikoumene's "rare visitor" omen can name a spot in that beast's share of the world. "A beast with a crystal mane drank from the Hebros at dawn."

**The quest: The Three Shares of the Earth.**
1. **The sun-priest's worry.** At Heliopolis the priest keeps the Phoenix's altar swept. The bird comes every five hundred years (Herodotus 2.73). Nobody knows now if it's coming at all. "It always comes after the three have walked the world. Have you seen them?"
2. **Tracking.** Ask an augur in each share of the world. The omens name a spot for each beast on some days. The Augur's Eye shows "Something here is watching you" on the right map.
3. **The meeting.** Each beast stands at its spot and runs on sight. Approach with the Helm of Darkness on (SYSTEMS §1), or leave any offering at the nearest altar first (the beasts like being expected), and it stays.
4. **Battle and catch.** Lv 72 each.
   - Raikou: Thunder, Extrasensory, Calm Mind, Rain Dance.
   - Entei: Sacred Fire, Stone Edge, Extreme Speed, Calm Mind.
   - Suicune: Hydro Pump, Extrasensory, Calm Mind, Tailwind.

**The quest: The Egg of Myrrh.** Herodotus's Phoenix carries its dead father from Arabia in an egg it makes from myrrh: as heavy as it can carry, hollowed, the father put inside, and sealed (2.73).
1. **The myrrh.** Buy myrrh from Naukratis's Arabian incense merchant. Five measures. "That's a very heavy egg."
2. **The shaping.** The sun-priest shows you how: shape it, test whether you can lift it, hollow it. A short choice puzzle: too light and the priest shakes his head; too heavy and you can't lift it. The answer is "as heavy as you can carry," so you must try each size and pick the heaviest that lifts.
3. **The carry.** Carry the egg from Naukratis to Heliopolis. You can't run while carrying it (the "don't run" flag from Hephaestus's theoxenia, SYSTEMS §10), and setting it down in grass breaks it.
4. **The altar at sunrise.** With all three wanderers caught, lay the egg on the sun-altar in the morning hour, and Ho-Oh descends. The wanderers were its heralds; their omens stop once they are caught.

```text
SUN-PRIEST: Five hundred years, and we always knew the day.

SUN-PRIEST: This time nobody told us. It came anyway.

SUN-PRIEST: …I think it wanted to.
```

**Battle.** Ho-Oh, Lv 78: Sacred Fire, Brave Bird, Earthquake, Recover. Harsh sunlight.

**Follow-up.** A Time Fracture opens over Heliopolis's altar: the three beasts' Golden Age forms, Walking Wake, Gouging Fire and Raging Bolt (§5). **Reward:** the priest gives a Rainbow-feathered **Sacred Ash**.

### 3.3 Uxie, Mesprit and Azelf: The Charioteer

**The casting.** The main story gave the lake trio's role to the three Fates (STORY S19). Here they become something just as Greek: Plato's soul. In the *Phaedrus* (246a–254e) the soul is a charioteer driving two winged horses, a white one, spirited and honest, and a dark one, all appetite. Uxie is the charioteer, reason; Azelf the white horse, spirit and will; Mesprit the dark horse, desire and feeling.

**Who asks.** **Hypatia**, the Pantheon's Psychic seat, who asked you before the Archon: "No one wrote you. So who are you?" (STORY §2). She's travelling now. You meet her at Naukratis's library.

```text
HYPATIA: I asked who you were. You beat me instead. Very rude. Very fair.

HYPATIA: Plato said a soul is a driver and two horses. Let's see yours.
```

**The quest.**
1. **Reason, at Lake Moeris.** Uxie sits on the lake's island. It keeps its eyes shut; whoever meets its eyes forgets. Hypatia sets you a reasoning puzzle on the lake's causeway: three priests, one always lies, one always tells the truth, one is new and doesn't know. Ask two questions to find the boat that's safe. Get it right and Uxie opens its eyes, and you don't forget.
2. **Desire, at Lake Tritonis.** Mesprit flits round the lake and won't be caught; desire never is. The trick is to stop chasing. Sit on the shore bench and wait three turns of the day, and it comes to you.
3. **Spirit, at Lake Maeotis.** Azelf tests your nerve. Six wild battles across the marsh in a row, no healing between, with Amazon trainers watching. Flee or heal, and it's gone till tomorrow.
4. **The chariot.** With all three, Hypatia asks her question again.

```text
HYPATIA: So. Who are you?
```
?? I DON'T KNOW / A TRAINER / WE'LL SEE
```text
HYPATIA: Good. All three are good. Plato would hate that.
```

**Battles.** Each Lv 70. Uxie: Psychic, Yawn, Future Sight, Amnesia. Mesprit: Psychic, Charm, Healing Wish, Draining Kiss. Azelf: Psychic, Nasty Plot, Explosion, Dazzling Gleam.

**Reward.** Hypatia's **Lustrous Globe** and **Adamant Crystal** for what comes next (§3.5).

### 3.4 Latias and Latios: The Twin Lights

**The casting.** Kastor and Polydeukes, the Dioskouroi, twin sons of Leda, are the sailors' saviors: the two lights that sit on a ship's mast in a storm (Homeric *Hymn to the Dioskouroi*). When Kastor died, his brother shared his immortality with him, and the two spend alternate days among the gods and below (*Odyssey* 11.301–304; Pindar, *Nemean* 10). Latias and Latios are a pair that can never be in the same place on the same day.

**Who asks.** Kleon. The twins' shrine is at Therapne, outside Sparta.

```text
KLEON: They share one life between two. One's in the dark every other day.

KLEON: They take turns. Every day.

KLEON: …I could do that. If I had a brother.
```

**The quest.**
1. **Therapne.** At the shrine in Lakonia, an old sailor's votive says the lights come back to the twins' home "in a storm, at sea, one at a time." Kleon gives you his cloak-pin, a pair of stars.
2. **The days.** On even Aethos days Latias rides the masts, on odd days Latios (`gLocalTime.days` parity). The augurs name the sea lane. They ride only the Oikoumene's wide lanes, where a storm has room.
3. **The storm.** Sail the named lane in a storm. Weather omens bring rain to one lane a day (SYSTEMS §6), and the Mountains of the Moon's lane always rains. Two lights sit on the *Euploia*'s mast. Climb the rigging (a short scripted climb) and one comes down to the deck.
4. **The other day.** Catch one. Next day, catch the other.
5. **Home.** Bring both back to Therapne. Kleon puts the pin on the shrine. The **Gemini** constellation is placed (SYSTEMS §8, #15).

**Battles.** Lv 72 each, in rain. Latias: Mist Ball, Recover, Calm Mind, Draco Meteor. Latios: Luster Purge, Recover, Calm Mind, Draco Meteor.

**Reward.** The **Latiasite** and **Latiosite** Ichor Stones, and Gemini.

### 3.5 Dialga and Palkia: Time and Room

**The casting.** The main story's Lord of Time is Kronolith, the Titan who devours time (STORY §2). `POSTGAME.md` gives Hesiod's Chaos, the first Gap, to Arceus to fill (§3.3 there). So Dialga and Palkia come from the other great Greek account of the world's making, Plato's *Timaeus*, the same book Atlantis comes from (Daphne's arc, POSTGAME §3.2).
- **Dialga is Chronos,** time as Plato defines it: "a moving image of eternity" (*Timaeus* 37d). Not the devourer: plain time that goes on. The Orphic poets made Chronos and Kronos one god, and Ichor pulls them apart: one wanted everything to stop, the other just keeps going.
- **Palkia is Chora,** Plato's third kind: the receptacle, the room in which everything comes to be, "the nurse of becoming" (*Timaeus* 49a, 52a–b).

**Where.** Dialga waits at **the Gates of the Sun** on Okeanos's western shore, where the sun goes in at evening (*Odyssey* 24.12). Palkia waits at **the Selvage**, where Okeanos pours over the edge of the world.

**Gate.** The Charioteer (§3.3), for Hypatia's two items, and Aeolus's Bag for the rim.

**The quest.**
1. **Hypatia's book.** "Daphne's reading the *Timaeus* for Atlantis. She skipped the good part. Plato says what time is, and what room is. Let's go and look."
2. **The twelve doors.** At sunset the Gates of the Sun open. Inside are twelve bronze doors, one for each hour of the night, each with a sundial's shadow cut into its lintel at a different angle. Walk them in the order the hours fall, reading the shadows. A wrong door puts you back at the first hour; Hypatia: "Time goes one way. Try that."
3. **Morning.** At the twelfth door the night turns to morning, and Dialga is standing in it.
4. **The room.** At the Selvage, Okeanos falls into nothing. Walk the rim until the water stops falling: the place where there's nothing to fall into, because there's no room there yet. Hold the Lustrous Globe up, and Palkia makes room in front of you.

```text
HYPATIA: Kronos wanted time to stop. This one just goes on.

HYPATIA: It doesn't eat anything. It doesn't want anything. It's very restful.
```

**Battles.** Lv 80 each. Dialga: Roar of Time, Flash Cannon, Earth Power, Aura Sphere. Palkia: Spacial Rend, Hydro Pump, Earth Power, Aura Sphere. The Adamant Crystal and Lustrous Globe give their Origin forms.

**Hook.** Sinnoh's tradition is that Dialga, Palkia and Giratina come before Arceus. `POSTGAME.md`'s summit already needs four keys and the three Primordials (P4); this file doesn't add Dialga and Palkia to that gate, but the summit's priest can mention them.

### 3.6 Cresselia and Darkrai: placed by UNDERWORLD

`UNDERWORLD.md` places both in **the House of Night**, Nyx's house at Tartarus's edge, where Sleep and Death live with their mother (Hesiod, *Theogony* 744–766), at Lv 78, as a stretch goal (its §6 and K8). The bible casts them as Hypnos and Nyx (PITCH §4). This file's first-draft quest for them gives way.

**What this file offers UNDERWORLD, if wanted.** Two beats from the first draft fit the House of Night:
- **The lead:** a ferryman's daughter at Sestos has slept for nine days and dreams of drowning; Cresselia's feather wakes her, and her father's oar-token gets you past Night's door.
- **The false shore:** Penelope, talking to a beggar who is really Odysseus, tells of two gates of dreams, horn for true ones and ivory for false (*Odyssey* 19.560–567). Darkrai's half of the house could be the ivory side, where the shore lies and the way that looks blocked is the true one.

**The 1.0 gap.** As a stretch goal, the House of Night leaves Cresselia and Darkrai uncatchable in 1.0. Decision PG-26 (OIKOUMENE §13) recommends building it in 1.0; failing that, the two wait at this file's Land of Dreams on Okeanos (OIKOUMENE §4.10), which already has the gates.

### 3.7 Cobalion, Terrakion, Virizion and Keldeo: The Hours of Justice

**The casting.** The Horai, the Hours, were daughters of Zeus and Themis: **Eunomia** (Good Order), **Dike** (Justice) and **Eirene** (Peace) (Hesiod, *Theogony* 901–903). Cobalion is Eunomia, steel discipline; Terrakion is Dike, who strikes; Virizion is Eirene, who brings plenty. Keldeo is **Astraea**, the star-maiden of justice who lived among people in the Golden Age and was the last immortal to leave the earth when men turned to iron (Aratus, *Phaenomena* 96–136; Ovid, *Metamorphoses* 1.149–150). It became Virgo.

**The Iron Age link.** Hesiod says Justice will leave the earth in the age of iron. The Swords' Iron Paradox forms, Iron Crown, Iron Boulder and Iron Leaves, are what justice looks like when nobody believes in it any more (§5).

**The quest.**
1. **Eunomia, in Sardis.** Solon, the lawgiver who wrote a poem called *Eunomia*, is visiting Croesus and refusing to call him happy. "Call no man happy till he's dead. Or, now, till he's done. Which is never." He asks you to settle three disputes in Sardis's market by the law he gave Athens: hear both sides, then choose (three short dialogue cases). Fair rulings, and Cobalion stands at the market's lion fountain.
2. **Dike, at Ammonion.** The oracle's priests have no answers to give. A man accuses another of stealing water from the Spring of the Sun. Terrakion won't appear while anyone in the oasis is lying. Find the liar by the spring's own rule: it's warm at midnight and cold at noon (Herodotus 4.181), so the man who says he drew warm water at noon is lying.
3. **Eirene, in Meroë.** The blameless Ethiopians (*Iliad* 1.423) have no quarrels to settle. Eirene has nothing to do. She appears to whoever brings food to the Table of the Sun's poor without being asked: lay three berries on the meadow's empty end. Virizion grazes there next morning.
4. **Astraea, on the Isles of the Blessed.** With the three Hours caught, the Virgo stars dim over the Isles. Keldeo walks out of the Golden Age's meadow, where justice never left.

```text
RHADAMANTHYS: She left the earth when men got iron. She came here. It's quiet.

RHADAMANTHYS: You've brought her sisters. She'll want to go back and look.
```

**Battles.** Each of the three, Lv 74. Cobalion: Sacred Sword, Iron Head, Close Combat, Swords Dance. Terrakion: Sacred Sword, Stone Edge, Close Combat, Swords Dance. Virizion: Sacred Sword, Leaf Blade, Close Combat, Swords Dance. Keldeo, Lv 75: Secret Sword, Hydro Pump, Calm Mind, Air Slash. It takes its Resolute form when it knows Secret Sword.

**Follow-up.** A fracture opens at the Selvage: the Iron Crown, Iron Boulder and Iron Leaves (§5).

### 3.8 Yveltal and Mew: The Isle of Ares and The First Clay

**Yveltal: the dark bird of the Isle of Ares.**

**The casting.** Off the Black Sea's south coast lies the Isle of Ares, where the Argonauts met birds that shot their feathers like arrows. The crew roofed the ship with their shields and rowed past under them (*Argonautica* 2.1030–1089). Apollonius says these were the birds Herakles drove from Lake Stymphalia. Yveltal is the dark bird over that flock: death in war, Ares's own. Xerneas, `LABORS.md`'s Golden Hind (Labor 3), is its opposite.

**Gate.** `LABORS.md`'s Labor 6, which drives the Stymphalian flock away to here, and Labor 9, for Hippolyta's shields.

**The quest.**
1. **Where they went.** After Labor 6, Lake Stymphalia's fishermen say the flock flew east. At Themiskyra, an Amazon has a bronze feather stuck in her shield: "From the island. Nobody lands there."
2. **The shield-roof.** Hippolyta lends you six of her shield-maidens. On the Isle of Ares the feathers fall in volleys. Move only under the shields: the maidens walk in a formation you steer (a scripted escort), and stepping out from under them in a volley sends you back to the landing. Three volleys, then the shore's end.
3. **The summit.** The flock rises off the ridge, and something above it doesn't. Yveltal comes down.

```text
SHIELD-MAIDEN: The Argonauts held their shields up and rowed. They didn't look.

SHIELD-MAIDEN: Don't look either. Walk.
```

**Battle.** Lv 80: Oblivion Wing, Dark Pulse, Sucker Punch, Taunt.

**Mew: The First Clay.**

**The casting.** Prometheus shaped the first creatures from clay (Pausanias 10.4.4), before his brother Epimetheus handed out the claws, wings and shells and ran out before he reached people (Plato, *Protagoras* 320d–321c). Mew is the first one, made before the gifts, so it has a little of everything. In myth Prometheus is the son of Iapetos, Ichor's forger; his name means "forethought."

**Gate.** `LABORS.md`'s Labor 11: you break Prometheus's chains on the Caucasus Crag with the Labrys, drive off Zeus's eagle (an Aetarch), and he gives you an ember from the fire he stole.

**The quest.**
1. **Free, and talking.** After the Labor, Prometheus stays near his crag. He can walk now, badly.

```text
PROMETHEUS: I was chained for a secret about who'd be born. A prophecy.

PROMETHEUS: Nobody can know who'll be born now. My secret's worth nothing.

PROMETHEUS: So I'd like to see the first thing I ever made. It hid when they took the fire.
```

2. **The caves.** Below the crag, three floors of wind-cut caves lead down to his first workshop. The wind blows out ordinary flames (SYSTEMS §2), but not his ember.
3. **The fire-pit.** Carry the ember from the crag to the cold fire-pit at the bottom, and light it. Mew comes to the light, plays round the fire, and then battles you, curious.
4. **The ring.** Prometheus gives you a Fire Stone set in an iron ring with a chip of Caucasus rock in it, as he wore one in myth (Hyginus, *De Astronomia* 2.15).

**Battle.** Mew, Lv 75: Psychic, Aura Sphere, Transform, Soft-Boiled.

### 3.9 Thundurus, Landorus and Enamorus: What Came Out of the Bag

**The casting.** Aeolus's winds are Tornadus, and `ODYSSEY.md` owns them. On the Odyssey, a deckhand opens the bag in sight of home and every wind comes out at once (ODYSSEY §6.4). Tornadus is caught and brought back. One more doesn't come back: Thundurus, the thunder, which blows south to Libya. Landorus is the earth's plenty, which mends what storms break. Enamorus is the spring after, the love that changes things, the Eros Hesiod put among the first powers (*Theogony* 120).

```text
AEOLUS: The thunder went south. Not my problem. Not my wind, strictly.
```

**The quest.**
1. **Your crew's fault.** In Libya the date-palms are stripped, and Ammonion's priests say the storms came the week your ship was blown about. A camel-driver: "Somebody opened something they shouldn't have."
2. **Thundurus.** It rides the Great Sand Sea's thunderstorms. The ravens of Ammonion find it: follow them into the storm's eye. Lv 76: Wildbolt Storm, Hurricane, Nasty Plot, Grass Knot.
3. **Landorus.** At the Table of the Sun, the meadow that feeds the poor every night has been bare since the storms. Landorus is the earth's own generosity, and it won't come to someone empty-handed. Bring one berry from each of the Oikoumene's ten lands (the Periodos makes you walk them anyway) and lay them on the Table. Landorus comes up out of the ground. Lv 76: Sandsear Storm, Earth Power, Sludge Wave, Rock Slide.
4. **Enamorus.** Back in Aethos, at Kythera's Spring of Kallirhoe, where Narcissus stares at himself for ever (STORY III-1). Galatea: "Love that won't let a thing change isn't love. It's a pool." Bring the two Forces to the spring, and the water ripples for the first time in a thousand years. Narcissus looks up. Enamorus is what made him. Lv 76: Springtide Storm, Moonblast, Superpower, Calm Mind.
5. **The Mirror of Truth.** For their Therian forms, use ODYSSEY's Mirror of Truth, the Reveal Glass that Alethea makes from Aiolia's bronze to show Tornadus's true shape (ODYSSEY §6.4). It shows each Force its own.

### 3.10 Reshiram, Zekrom and Kyurem: The Truth and the Glory, and The Other Half

**The casting.** Unova's dragons are truth and ideals. Ichor already has a girl named Truth and a boy named Glory.
- **Reshiram** is *aletheia*, truth. The Greek word means "un-forgetting," *a-lethe*.
- **Zekrom** is *kleos*, glory that won't die: Kleon's real prophecy, "glorious while young, and his glory will not die" (STORY §2).
- **Kyurem** is what's left when a whole is split. Aristophanes tells in Plato's *Symposium* (189c–193d) that people were once double, and Zeus cut them in half, and each half searches for its other. Kyurem is the cold hollow where two halves used to be one.

**The quest: The Truth and the Glory.**
1. **Alethea in Egypt.** In Memphis, Helen of Sparta, the land's champion, tells Alethea the truth: the Helen on Troy's walls was a phantom made of cloud, and she sat here the whole war (Euripides, *Helen*; Stesichorus's *Palinode*). A thousand ships for a better story. Alethea writes it down, and Helen asks her not to: "They prefer the other version." Alethea: "Truthfully? I don't care what they prefer." In the temple of the Stranger Aphrodite, the **Truth-Stone** (the Light Stone) is warm. Alethea gives it to you.
2. **Kleon at Troy.** Kleon sails out to see Ilion, and to meet Hektor, who wants glory the way he did. They spar on the Skaian Gate's tower. Hektor: "I used to know how I'd die. It made the glory easy." Kleon: "It's not easy now. It's better." The **Glory-Stone** (the Dark Stone) cracks with light in Kleon's hand.
3. **Waking them.** Each stone wakes its dragon where it was given: Reshiram over Memphis at noon, Zekrom over the Skamander plain in a storm. Alethea and Kleon each watch you catch theirs.
4. **The cold half.** With either one caught, the Cave of Boreas's deepest floor freezes harder. Kyurem waits in the hollow. Alethea and Kleon both come; it's the first time the three of you have been in one place since the Akropolis. Kyurem won't fight until they stand on either side of it.

```text
KLEON: It looks like it's waiting for someone.

ALETHEA: Two someones.

KLEON: …Don't make it a thing.
```

5. **The Gordian Cord.** At Gordion, the knot that bound Gordias's cart is the expansion's DNA Splicers, renamed. Its priest: "Whoever undid it would rule Asia. Nobody rules anything now. Take it if you like." Untie it with two hands: hold the cart, and pull (a callback to Medon's Knot, STORY §6.15). It binds Kyurem to either dragon, and unties them again.

**Battles.** Reshiram, Lv 80: Blue Flare, Fusion Flare, Draco Meteor, Earth Power. Zekrom, Lv 80: Bolt Strike, Fusion Bolt, Outrage, Crunch. Kyurem, Lv 82: Glaciate, Scary Face, Dragon Pulse, Freeze-Dry.

### 3.11 The four Tapus: The Keepers of the Isles

**The casting.** The Tapus are island guardians, fickle and kind by turns, each with its own ground. Hesiod's Isles of the Blessed lie "beside deep-swirling Okeanos" (*Works and Days* 171), and Okeanos's daughters, the Okeanids, are the springs and waters of the world (*Theogony* 346–366). Four of them keep the four Isles:
- **Tapu Koko is Elektra,** "shining," the same root as *elektron*, amber;
- **Tapu Lele is Metis,** "wise counsel," whom Zeus married first;
- **Tapu Bulu is Plouto,** "plenty";
- **Tapu Fini is Amphirho,** "flowing round."

The first draft cast them as the Hesperides; `LABORS.md`'s eleventh Labor already gives the Garden's Hesperides as its own trainers, so the Tapus moved to the Isles.

**Gate.** The Isles of the Blessed: Helios's cup after Labor 10, and Rhadamanthys's question (OIKOUMENE §4.10).

**The quest.** The Isles have everything. The Okeanids are bored, and each tests whether a living visitor is worth the trouble.
1. **Elektra's race.** All light and showing off, she races you round her isle's shore from one standing stone to the next, and lightning strikes where she's been (Koko loves a fight). Catch her and she battles.
2. **Plouto's want.** Her isle has plenty of everything except things that run out. "Bring me something that ends." Any perishable from the living world will do: a loaf from Elaia's bakery, a cut flower, Moomoo Milk. She eats it slowly. "Oh. That's what it's for."
3. **Metis's riddle.** At dusk she asks: "What comes after this?" Every answer fails ("night," "morning," "nothing") except the one that admits you don't know. "Good. Neither do I. I've never said that before."
4. **Amphirho's spring.** Her spring runs round her isle, and it has silted up with gold. Carry seawater from Okeanos in a jar three times (carried, like a flame; it spills if you run) to wash it clear.
5. **The four gifts.** Each Okeanid, beaten and caught, leaves her isle's seed: the **Electric, Psychic, Grassy and Misty Seeds**, the terrains' own items (already in the expansion).

**Battles.** Each Lv 76, with its own terrain. Tapu Koko: Nature's Madness, Wild Charge, U-turn, Dazzling Gleam. Tapu Lele: Psychic, Moonblast, Calm Mind, Nature's Madness. Tapu Bulu: Wood Hammer, Horn Leech, Superpower, Bulk Up. Tapu Fini: Moonblast, Surf, Nature's Madness, Calm Mind.

### 3.12 Cosmog, Solgaleo, Lunala and Necrozma: Hyperion's Children, and The Day Turned to Night

**The casting.** In myth Hyperion, the Titan of watchfulness and light, fathered the Sun (Helios), the Moon (Selene) and the Dawn (Eos) (Hesiod, *Theogony* 371–374). Ichor's Hyperion is a man named for him: the Titan admin who went blind, whose true oracle said "You'll end your days in the dark, and be glad of it," and who works iron by feel at Talos's forge now (STORY §2).

**The quest: Hyperion's Children.**
1. **The light.** At Kaldera, Hyperion has seen something. He can't see anything, so he's sure.

```text
HYPERION: There's a light in the forge that isn't the fire. Little. Floaty.

HYPERION: Petros says there's nothing. Petros has eyes. I don't trust him.
```

   It's a Cosmog, a scrap of star-cloud, and it sits on his shoulder. Nobody else saw it until he did.
2. **His kid.** "My namesake had three kids. Sun, moon, morning. I never had any." Pause. "Well. I had the crews." He gives it to you (Lv 42) because it wants to go somewhere east, and he can't take it.
3. **East.** It evolves at 43 into Cosmoem and at 53 into its final form, by the hour: Solgaleo by day, Lunala at night (the expansion's own condition). Carry it to the Gate of Dawn, where the sun rises out of Okeanos.
   - If yours became Solgaleo, Lunala waits at Mount Latmos, where Selene visits sleeping Endymion, on any night. If yours became Lunala, Solgaleo waits on the Gate of Dawn's stable roof at sunrise. Each is Lv 80.
4. **Home.** Bring both back to Kaldera. Hyperion holds his hand out at the forge's door, and they both come and sit by him, one hot and one cold. "There they are."

**The quest: The Day Turned to Night.**
1. **Thales.** In Miletos, the philosopher Thales has done something no one did before him: he predicted an eclipse without an oracle (Herodotus 1.74). "I didn't foresee it. I counted."
2. **The date.** He names a day on the Aethos calendar. On it, at noon, at the Halys ford where the Lydians and the Medes once stopped a battle because the day turned to night, the sun goes out.
3. **The dark.** Everyone panics but Hyperion, whom you bring along. "Dark? I'm used to it. This way." The eclipse is a living thing eating the light: Necrozma. Hyperion talks you across the black ford by sound.
4. **The battle.** Necrozma, Lv 85: Photon Geyser, Prismatic Laser, Earth Power, Moonlight. Catch it and the sun comes back. Hyperion turns his face to it, the same line as the Stair of Hours (STORY III-11): "There it is."

**Reward.** Hyperion gives the **N-Solarizer** and **N-Lunarizer**, renamed the **Dawn-Bridle** and **Dusk-Bridle**, for Necrozma's fusions.

### 3.13 Zacian and Zamazenta: The Shield With the World on It

**The casting.** Thetis told her son he could have a short life and glory that never dies, or a long life and no glory (*Iliad* 9.410–416). She had Hephaestus make him armor, and on its shield the god put the whole world: the earth, sea and sky, two cities, the harvest, a dance, and the river Okeanos running round the rim (*Iliad* 18.478–608). The Oikoumene is that shield.
- **Zacian is the sword:** the short life, and glory.
- **Zamazenta is the shield:** the long life, with the whole world on it.

**Who.** Achilles, the Stadion's Brain at Olympia (`POSTGAME.md` §3.1), at Leuke, his mother's White Isle in the Black Sea (OIKOUMENE §6). The bards say his shade lives here after Troy; he's come while he's alive. Open once you've won his silver symbol.

**The quest.**
1. **The choice that's off.** Achilles has come to tell his mother he doesn't know which life he'll have. Prophecy's over. She's relieved, and frightened.

```text
THETIS: I gave him two lives to choose from. Now there's no choosing. Just living.

ACHILLES: I don't know what I'll do, Mother.

THETIS: Nobody does. I didn't know that was allowed.
```

2. **The rusted gifts.** Thetis keeps the sword and the shield Hephaestus made, rusted by the sea. Achilles won't take either: taking one is choosing. He asks you to carry both to the island's two cliffs, east and west, and see which wakes.
3. **The wolves.** Both wake. At the east cliff, under the sword, Zacian. At the west, under the shield, Zamazenta. You get to choose the order, and that's the only choice.
4. **The rim.** When you hold the shield up to the sea, its edge lines up with the horizon: the river running round the world. Achilles laughs. "I'll take the long way, then. Probably. We'll see."

**Battles.** Each Lv 85. Zacian: Behemoth Blade (Crowned), Play Rough, Close Combat, Swords Dance. Zamazenta: Behemoth Bash (Crowned), Body Press, Iron Defense, Crunch. Each starts in its Hero form and can be crowned with its rusted item.

**Reward.** The **Rusted Sword** and **Rusted Shield**, renamed **the Sword of Peleus** and **the Shield of Achilles**.

### 3.14 Calyrex, Glastrier and Spectrier: The Straw Offerings

**The casting.** Every year the Hyperboreans sent offerings wrapped in wheat straw to Apollo's Delos, handed on from people to people across Scythia, Greece and the islands, though no one along the way knew why (Herodotus 4.33). Calyrex is the king of that harvest, whom everyone has forgotten while still carrying his gifts. Glastrier is Boreas's mare: the North Wind sired horses that ran over the wheat without bending it (*Iliad* 20.221–229). Spectrier is a black horse of the dead.

**The quest.**
1. **The maidens' house.** In Abaris, the kin of the Hyperborean maidens who died carrying the offerings to Delos ask you to do the opposite: bring a straw bundle back up the chain, from Delos to here. "We send them south every year. We've never seen what comes back."
2. **The relay.** Delos is the island beside Aethos's Route 2 (`AETHOS_MAP.md`, `MAPSEC_DELOS`), so the relay starts at home. The priests there give you the old straw, and you carry it hand to hand: to Kalliste's Halia, to Olbia's Anacharsis, to the Wagon Camp, to the Arimaspian miners, to the Rhipaean pass. Each keeper adds something and tells you one line about why they never asked what was in it.
3. **The round temple.** The bundle, unwrapped at Apollo's round temple, is empty. Calyrex rises out of the straw: a king whose gift is that the bundle kept travelling. "Nobody remembers me. Everyone remembers to pass it on." It battles you, Lv 80.
4. **Its steed.** Calyrex asks for a horse it lost. Both can come: Glastrier waits at the Cave of Boreas's windiest floor, and Spectrier on the Cimmerian Shore, where the dead come to drink. Lure each with a carrot of its land, an Iceroot from the Hyperborean meadow or a Shaderoot of asphodel from the Cimmerian mist (new key items). Each is Lv 78.

**Battles.** Calyrex: Psyshock, Giga Drain, Leech Seed, Calm Mind. Glastrier: Glacial Lance, High Horsepower, Close Combat, Swords Dance. Spectrier: Astral Barrage, Shadow Ball, Nasty Plot, Hex.

**Reward.** The **Reins of Unity**, renamed **the Straw Reins**. In Sword and Shield you could keep only one horse; here you keep both, and the Reins join Calyrex to either.

### 3.15 Wo-Chien, Chien-Pao, Ting-Lu and Chi-Yu: What Stayed in the Jar

**The casting.** PITCH §4: the Treasures of Ruin are the evils that escaped Pandora's jar. Hesiod's jar held sickness, toil and countless others; only Hope stayed inside (*Works and Days* 90–104). Four of the evils are Ichor's:
- **Wo-Chien is Limos, Famine.** Ovid says Famine lives in icy Scythia, at the edge of the world, pulling up scraps of grass with her teeth (*Metamorphoses* 8.788–800).
- **Chien-Pao is Phthonos, Envy.** Solon told Croesus that the gods are envious (Herodotus 1.32).
- **Ting-Lu is Geras, Old Age.**
- **Chi-Yu is Eris, Strife,** who threw the golden apple at the wedding and started the road to Troy.

**Who asks.** Elpis, whose name is Hope, the one thing that stayed in the jar. SYSTEMS §5's seventh amphora, Pandora's jar, gives the lead.

```text
ELPIS: Papa says the jar had sad things in it. And hope stayed in.

ELPIS: So all the sad ones went out by themselves.

ELPIS: Can you find them? Somebody should say hello.
```

**The quest.**
1. **The lid.** Elpis gives you the jar's clay lid from Astyra's Library (her father brought it home for her). It hums near each evil.
2. **Four shrines.** Each evil was shut in a shrine at the edge of the world by the men of the Bronze Age, with eight bronze nails driven into its door. The nails are scattered across its land: in a tomb, a nest, a well, under a herm. Pull all eight and the shrine opens.
   - Wo-Chien's shrine: a stony field on the Steppe Road.
   - Chien-Pao's: the deepest vault of Croesus's treasury in Sardis.
   - Ting-Lu's: the Fountain of the Long-Lived's dry back spring, in Aithiopia. Old age waiting beside the cure for it.
   - Chi-Yu's: under the Skaian Gate in Ilion. Cassandra knows exactly which stone. She's not sure how she knows. "Habit."
3. **Saying hello.** Each evil, freed, battles you, Lv 78. Before it does, if Elpis's lid is in your bag, you get a line from her: what she'd say to it.

```text
(To Famine) You can have half my bread. I'm not very hungry. I never am.

(To Envy) I'm jealous of you. You've been everywhere.

(To Old Age) Papa says you're the one I want. He says it's a good one to get.

(To Strife) Do you want to play a game? You can win.
```

4. **Home.** Bring the lid back to Akti. Elpis puts it on her shelf next to Daedalus's music box. "They're not by themselves now. They've got you."

**Battles.** Wo-Chien: Ruination, Giga Drain, Leech Seed, Foul Play. Chien-Pao: Icicle Crash, Sucker Punch, Sacred Sword, Ruination. Ting-Lu: Earthquake, Ruination, Whirlwind, Throat Chop. Chi-Yu: Overheat, Dark Pulse, Ruination, Nasty Plot.

---

## 4. Single legends and mythicals

### 4.1 Celebi, Heatran, Type: Null, Magearna, Marshadow and the Thyrsa five

These live in Aethos and are in §7.

### 4.2 Mewtwo: Look Only in the Mirror

**The casting.** The Gorgon was a mortal girl, Ovid says, made into a monster by a goddess's anger, so that anyone who looked at her turned to stone (*Metamorphoses* 4.790–803). Mewtwo is a creature made into the strongest monster there is, angry at whoever made it. The Gorgons live beyond Okeanos (Hesiod, *Theogony* 274–275). The Lazarus check: Ichor never uses the name Medusa, and nothing here is called Aegis.

**Gate.** The Cave of the Graiai, and ODYSSEY's **Mirror of Truth**, the polished bronze Alethea makes from Aiolia's walls (ODYSSEY §6.4). Perseus looked at the Gorgon only in a polished shield; Alethea's mirror does the same job, and suits her: it shows a thing as it is.

**The quest.**
1. **The gray sisters.** The three Graiai share one eye and pass it hand to hand (Aeschylus, *Prometheus Bound* 794–797). Perseus stole it to make them talk. You don't: you sit and watch until you know their order, then catch the eye when it drops between the second and third sister and hand it back. Grateful, they tell you the way.
2. **The landing.** At the Gorgons' landing Alethea, if she's with you, holds up the mirror. "Don't look at the island. Look at it in this. Truthfully, that's how I look at most things."
3. **The mirror walk.** The Gorgons' Isle is walked looking only in the mirror. Your controls are mirrored left to right for the whole map, and the screen shows the reflection. Stone statues of earlier visitors mark the wrong turns. It is the game's strangest dungeon, and it's short.

```text
A stone hoplite, mid-stride. His hand is over his eyes.

Somebody's scratched on his shield: "I LOOKED."
```

4. **The center.** In the last chamber, Mewtwo waits with its back to you. Turn the mirror and it sees itself as it is, and that's what it can't stand. It battles you.

**Battle.** Mewtwo, Lv 90: Psystrike, Aura Sphere, Ice Beam, Recover. After Eternatus, it is the Oikoumene's hardest static.

**Reward.** Both **Mewtwonite** stones.

### 4.3 Jirachi: The Thousand-Year Star

**The casting.** Jirachi wakes for seven days every thousand years and grants wishes. Ichor's thousand years are Medon's: the Fates were chained a thousand years ago (STORY §1). Jirachi fell asleep the night Medon tied his first knot, because someone wished it. It wakes now because the wish is undone.

**Where.** The Atlas Range's highest summit. Atlas himself is alive on his ridge, holding up the sky, and is `LABORS.md`'s to write; this peak is the next one along, where the sky he holds hangs low enough that the stars almost touch the snow. Atlas, in myth, taught people the stars.

**Gate.** All 24 constellations placed on the Star Chart. SYSTEMS §8 promises "a star-born mythical" for completing the chart; this is it (decision PG-28).

**The quest.**
1. **The empty patch.** With the chart complete, a 25th light blinks in a corner of it that was never a constellation. Daphne: "That's not one of ours."
2. **The climb.** Up the Atlas Range past the snowline. On the way, Atlas calls across from his ridge: "Mind the low bit. That's where I keep the ones I like." At the summit, hanging just above the snow, something small is asleep in the sky.
3. **The seven days.** It wakes when you reach it and stays awake seven Aethos days. Visit on any of them.
4. **The wish.** On the first visit Jirachi offers a wish. The options are things you might want: a Pokémon, an item, a stronger team. Turn them all down and a last option appears.

```text
JIRACHI looks at you, waiting.
```
?? A RARE POKÉMON / A TREASURE / STRENGTH / NOTHING
```text
> NOTHING:
Jirachi looks puzzled. Then it laughs, and climbs down off the sky.
```

   Choose a gift and you get it, and Jirachi still battles you. Choose nothing and it joins without a battle, already caught, with a Cherish Ball and its "wish" ribbon.

**Battle** (if any). Lv 75: Doom Desire, Iron Head, Psychic, Wish.

**Follow-up.** The 25th light stays on the chart: **Atlas**, for the one who held up all the others.

### 4.4 Deoxys: The Things That Fell

**The casting.** The Greeks kept stones that had fallen from the sky. The Palladion at Troy fell when Ilos prayed for a sign, and the city couldn't fall while it stood (Apollodorus 3.12.3). The image of Artemis at Ephesos was "fallen from Zeus" (*diopetes*). The Mother of the Gods at Pessinus in Phrygia was a black stone that fell from heaven. Deoxys is what fell: four forms, four stones.

**The quest.**
1. **The Palladion.** In Ilion's temple of Athena, the Palladion's keeper says the image hums at night now. "It never did before. Before, we knew why it was here."
2. **The others.** Daphne at Naukratis, on hearing: "Every fallen stone in the world will be humming." Visit three more: the Mother's black stone in a Phrygian shrine on the Royal Road, the Artemis at Ephesos on the Maeander's mouth, and Ammon's navel-stone at the oasis.
3. **Each stone.** Touching each one with the Palladion's splinter (from its keeper) leaves a glowing mark on the Star Chart's sky. Four marks, joined, point at Ilion at midnight.
4. **The fall.** At midnight on Ilion's highest tower, Deoxys comes down in a column of light.

**Battle.** Lv 78, Normal form: Psycho Boost, Superpower, Extreme Speed, Recover.

**Form changes.** Touching any of the four stones changes its form: the Palladion Defense (it kept Troy), the black stone Attack, the Artemis Speed (the huntress), Ammon's Normal. The expansion's Meteorite item, renamed **Sky-Stone**, also cycles the forms anywhere.

### 4.5 Shaymin: Thank-Offerings

**The casting.** Shaymin carries gratitude. The Greek word is *charis*, which is also grace and favor: the Charites, the Graces, are where the word comes from. Its Sky form rides the west wind, Zephyros, who blows on the Isles of the Blessed for ever (*Odyssey* 4.567–568).

**Gate.** The Isles of the Blessed, and the Pyanopsia festival (SYSTEMS §7: its *eiresione*, an olive branch hung with wool and fruit, is a thank-offering every god likes).

**The quest.**
1. **Menelaus's garden.** On the Isles, Menelaus waits for Helen. His meadow has a patch of Gracidea that never flowers. "You can only pick it for someone. My wife says that. She'd know."
2. **Thank-yous.** Shaymin only comes to someone carrying gratitude. Collect a thank-you from five people you helped in the main game, each a small token:
   - Elpis, a drawing of Starry;
   - Petros and Amathos, a bent nail from Hyperion's forge;
   - Kydippe, the midwife, a thread from your swaddling;
   - Ione, a coal from Hestia's hearth;
   - Phaedon, a single dressing he rolled that morning.
3. **The eiresione.** Hang the five tokens on an olive branch with wool. On the Pyanopsia, carry it to the Isles and hang it on Menelaus's door.
4. **The flowers.** The Gracidea flowers. Shaymin comes out of it, looks at the branch for a long time, and battles you.

**Battle.** Lv 70: Seed Flare, Earth Power, Air Slash, Synthesis.

**Reward.** Menelaus gives you the **Gracidea**: "Give it to someone." Shaymin's Sky form returns to Land at night, as in the originals.

### 4.6 Victini: placed by POSTGAME

`POSTGAME.md` §3.1 places Victini as **Nike** on her pillar before Olympia's Temple of Zeus, where Paionios carved her: she comes down once you hold all five Olympiad gold symbols (Lv 80). This file's first-draft quest, Victini landing on your trireme's prow, gives way. One line of it survives as flavor, if POSTGAME wants it: after Nike comes down, the *Euploia*'s captain carves one for his prow anyway. "In case she gets bored."

### 4.7 Meloetta: The Singing Head

**The casting.** PITCH §4: Orpheus's song. When the maenads tore Orpheus apart, they threw his head and lyre into the Hebros, and the head kept singing as it floated out to sea, to Lesbos (Ovid, *Metamorphoses* 11.50–55). The lyre went up into the sky as Lyra. The Lazarus check: Ichor never calls Meloetta a Muse.

**Gate.** SYSTEMS §5's eighth amphora (Orpheus) leads to Arkadia's grove at night; SYSTEMS §3's Apollo gift II, the **Lyre of Apollo**, plays it back.

**The quest.**
1. **The lead.** In Arkadia's grove, at night, you hear a phrase of song from nowhere (SYSTEMS §5). Daphne: "That's from the Hebros. Thrace. It's a long way to hear a song."
2. **The river.** At the Hebros's mouth, the song comes over the water at dusk. Each evening it sings one phrase: four notes.
3. **The playback.** Answer it on the Lyre of Apollo: four notes, chosen from the Relic Ring's lyre menu (up, down, left, right). Each correct phrase brings the next, longer one. Five phrases, and the song is complete for the first time since it was torn off.
4. **The singer.** Meloetta stands on the water where the head drifted, and sings the whole thing, then battles you.
5. **Lyra.** The Lyra constellation is placed (SYSTEMS §8, #11).

**Battle.** Lv 72, Aria form: Relic Song, Psychic, Close Combat, Calm Mind. It changes to Pirouette form when it uses Relic Song, as the expansion already supports.

### 4.8 Genesect: The Man Who Couldn't Stop

**The casting.** Eos, the Dawn, asked Zeus to make her husband Tithonus immortal, and forgot to ask for youth. He grew older and older, and could never die, until he shrank and babbled and she turned him into a cicada (Homeric *Hymn to Aphrodite* 218–238). Her son Memnon wore armor Hephaestus made. Genesect is Tithonus the cicada, living in his son's god-made armor.

**Who asks.** Eos, at the Gate of Dawn, and Memnon, the land's champion.

**The quest.**
1. **The noise.** In Eos's palace something sings all day in an empty room, with a sound like a forge. Eos: "My husband. He sings. He's sung for a very long time."
2. **The armor.** Memnon's old suit of armor stands in the corner and moves when no one's in it. Tithonus has climbed inside.

```text
EOS: I asked for him to never die. I forgot the rest.

EOS: Your Cutter could do it now, they say. Nobody fixed his end. It's his.

EOS: He doesn't want to. He wants to see more dawns. I'm glad.
```

3. **The dawns.** Tithonus will only come out to watch the sunrise. Be in the room at dawn three days running, and on the third the armor walks out onto the terrace.
4. **The battle.** The armor battles you, the cicada singing inside it.

**Battle.** Lv 75: Techno Blast, U-turn, Flamethrower, Iron Head.

**Reward.** Memnon gives you the four **Drives**, renamed the four winds' **Dawn-Colors**: they paint the armor's song with fire, ice, water or lightning.

### 4.9 Zygarde: Fourteen Pieces

**The casting.** Zygarde is the order of a whole land, scattered in cells and gathered into a body. The Greeks' Egypt has the same story: Set cut Osiris into fourteen pieces and scattered them along the Nile, and Isis found each and put him back together (Plutarch, *On Isis and Osiris* 18). Herodotus says Osiris is the Egyptians' Dionysus (2.144).

**The quest.**
1. **The cedar chest.** Osiris's body once floated to Byblos in a chest. At Naukratis, a Phoenician trader sells an old cedar chest that ticks (the expansion's Zygarde Cube, renamed).
2. **The pieces.** Fourteen Zygarde cells hide across Egypt and the Oikoumene: one in each land's oldest place, and four along the Nile. The chest ticks faster near one. Some need a relic (a dark tomb, a flooded chamber, a thicket).
3. **Abydos.** At Osiris's tomb in Abydos, with ten pieces, Zygarde gathers into its 10% form and battles you. With all fourteen, its Complete form is available.

**Battle.** Lv 78, 50% form: Thousand Arrows, Thousand Waves, Dragon Dance, Extreme Speed.

**Form note.** The expansion's Zygarde forms depend on its Cube and abilities; collecting cells is new. The script counts the 14 and sets the form when you use the chest (§9).

### 4.10 Diancie: The Crown's Last Stone

**The casting.** When Dionysus married Ariadne he gave her a crown of gold and Indian gems that Hephaestus had made, and later set it in the sky as the Corona Borealis (Hyginus, *De Astronomia* 2.5). LABYRINTH places that constellation after the crane dance. Diancie is the crown's last stone, which fell to earth.

**Who asks.** Ariadne, at Knossa, between rounds of her Endless Labyrinth (LABYRINTH §10).

```text
ARIADNE: Look. Corona Borealis. Nine stars. There used to be ten.

ARIADNE: He said they came from the mountain where they raised him. Nysa.
```

**The quest.**
1. **Nysa.** Dionysus was raised on Mount Nysa, which Herodotus puts in Aithiopia (2.146).
2. **The gems.** On Nysa, Carbink live in the ivy walls (Dionysus's Thyrsus climbs them, SYSTEMS §3 gift II). Each carries a chip of the fallen stone. Battle six Carbink (wild, they're common here) and the chips draw together.
3. **The tenth star.** At the top, Diancie sits where the chips point, making a new stone out of nothing. It battles you.
4. **Ariadne.** Take it to Knossa. She holds it up to the night sky in the palace court, and the crown has ten stars.

**Battle.** Lv 74: Diamond Storm, Moonblast, Earth Power, Protect.

**Reward.** **Diancite**.

### 4.11 Hoopa: The Ring of Gyges

**The casting.** In Plato's *Republic* (2.359d–360b), a Lydian shepherd named Gyges goes into a chasm opened by an earthquake and finds a hollow bronze horse with a giant's body inside, wearing a gold ring. Turn the ring and you vanish. Gyges used it to murder the king and take Lydia. Plato's question: would anyone stay just if no one could see them? Hoopa is the ring: rings that open, things that vanish and appear, and its Prison Bottle is the bronze horse.

**The quest.**
1. **The chasm.** The Chasm of Gyges opened again in an earthquake the week the fog lifted. A shepherd won't go down: "My grandfather said the last man who did became king. I don't want to be king."
2. **The horse.** Three floors down, a hollow bronze horse. Inside, a ring-shaped bottle (the expansion's Prison Bottle).
3. **The test.** Take the bottle and Hoopa comes out and makes you invisible. Walk back up through Sardis's market: every stall is unguarded, every chest open, and no one can see you. The town has nineteen things you could take.
   - Take nothing, and walk back to the chasm. Hoopa reappears, delighted, and battles you.
   - Take anything, and Hoopa vanishes with the bottle. The stolen thing is in your bag with its owner's name on it; return it and try tomorrow.

```text
You are invisible. The goldsmith has stepped away from his table.

There are nine gold coins on it.
```

**Battle.** Lv 76, Confined form: Hyperspace Hole, Psychic, Shadow Ball, Nasty Plot.

**Reward.** The **Prison Bottle**, renamed **the Bronze Horse**, for its Unbound form.

### 4.12 Volcanion: Steam and Stone

**The casting.** In the war of the gods and the Giants, the Giants fell at the Phlegraean Fields, the burning plain near Cumae, and were buried under its volcanoes, still breathing steam (Strabo 5.4.6). Volcanion is a Giant under the fields: fire and water, and no love for anyone who comes poking.

**The quest.**
1. **The Sibyl's warning.** At Cumae: "Something under the fields is angry. It's been angry for a long time. I'd know."
2. **The vents.** The Fields are a vent puzzle. Fire vents and water vents alternate; walking past a fire vent while carrying water (the Atlantic jar of §3.11, or a well's) makes steam that clears the path; carrying a flame past a water vent does the same. Five vents, two carried things.
3. **The steam.** At the center, the last vent breathes the Giant out. Volcanion battles you without a word.

**Battle.** Lv 76: Steam Eruption, Earth Power, Sludge Bomb, Flame Charge.

### 4.13 Zeraora: The Amber Spark

**The casting.** The Greek for amber is *elektron*, and it gave the world the word electricity: Thales noticed that rubbed amber pulls straws to it (Diogenes Laertius 1.24). Zeraora is the spark that lived in Thales's amber.

**The quest.**
1. **Thales's amber.** In Miletos, Thales has a lump of Baltic amber from the north's amber road. He rubs it and it snaps. "Something's in there. Not a soul. I said everything has souls once. I was being dramatic."
2. **The rubbing.** He wants more amber to test. Collect five pieces: from Olbia's traders, the Arimaspian miners, Eridanos driftwood on the Steppe Road, Hyperborea's swan-keeper and a Heliad tree in Aethos (the dex's Elektear, whose tears are amber).
3. **The spark.** Rub all five together at Thales's table, at night, with no lamp. The spark jumps from the amber to the floor and is a cat. It runs out of the house. Chase it through Miletos's streets: it is faster than you and hides in metal (bronze doors, lamps, a statue). Thales calls out where it went.
4. **Cornered.** It turns at the harbor's end.

**Battle.** Lv 75: Plasma Fists, Close Combat, Knock Off, Bulk Up.

### 4.14 Meltan and Melmetal: The First Iron

**The casting.** The Chalybes were said to be the first people to work iron (Aeschylus, *Prometheus Bound* 714–715; *Argonautica* 2.1001–1007). Meltan are the first iron, crawling out of the ore. In the expansion Meltan doesn't evolve: Melmetal is its own encounter.

**The quest.**
1. **The pests.** Meltan swarm the Chalybes' forges, eating the iron. The ironmaster wants them gone. They're wild here, common in the forges (Lv 70).
2. **The iron.** Each Meltan you catch or beat drops iron filings. The ironmaster: "Bring me forty of them's worth and I'll pour you something."
3. **The furnace.** With 40 measures, he fills the great furnace. What pours out is alive.

**Battle.** Melmetal, Lv 80: Double Iron Bash, Thunder Punch, Ice Punch, Acid Armor.

### 4.15 Eternatus: The Day the Sun Fell

**The casting.** Phaethon begged his father Helios for one day with the sun's chariot, lost control, and burned the world. Ovid says that day dried Libya into a desert (*Metamorphoses* 2.237–238). There is a real yellow glass lying in the Libyan desert, made by a fall from the sky long ago. Eternatus is that day: the darkest one, when the sun came down.

**Gate.** The Glass Crater, and eight Periodos panels.

**The quest.**
1. **The glass.** At Kyrene, the champion Kyrene shows you a scarab of yellow glass. "It comes from the middle of the sand. Nobody goes there."
2. **The crater.** Through the Sand Sea with Ammon's ravens, to the Glass Crater. Three floors of glass that reflect your torchlight; the light radius jumps between reflections.
3. **The chariot.** At the bottom lie the burned spokes of a chariot wheel. Hyperion, if you've done Hyperion's Children, sent you with a message for his namesake's grandson: "Tell him it was a good try."
4. **The day.** Eternatus rises from the glass, and the screen goes red.

**Battle.** Lv 92, the strongest static in this file, under only Arceus: Dynamax Cannon, Sludge Bomb, Flamethrower, Recover. No Eternamax form: Dynamax is off (PITCH §5).

### 4.16 Kubfu and Urshifu: Milo's Calf

**The casting.** Milo of Kroton, six times Olympic wrestling champion, trained by carrying a calf on his shoulders every day until it was a bull (Quintilian 1.9.5). Kubfu is the calf.

**The quest.**
1. **Milo.** The Western Sea's champion (OIKOUMENE §6). After you beat him, he gives you a cub. Lv 70.

```text
MILO: Carry it. Every day. When you can't carry it any more, you're ready.
```

2. **The carrying.** Kubfu must be in your party and lead for 2,000 steps.
3. **The two schools.** Milo sends you to the Hellespont, where Leander swam to Hero every night by her lamp until the night it went out and he drowned.
   - **The unlit tower** (Dark): Hero's tower at Sestos, climbed in the dark with no torch, the night the lamp is out. Single Strike.
   - **The strait** (Water): swim the Hellespont by night, against the current, toward the lamp. Rapid Strike.
   - Each ends at a scroll: the expansion's Scroll of Darkness or Scroll of Waters, renamed **Hero's Lamp** and **Leander's Strait**. Kubfu evolves by reading one.
4. **Only one.** Kubfu takes one path. For the 100%, Urshifu's two forms are forms, not species; one is enough.

### 4.17 Zarude: The Foster-Father

**The casting.** Dionysus was raised by nymphs and by old Silenus on Mount Nysa (Homeric *Hymn* 26). Zarude is a troop of the jungle who once raised a lost child, and its Dada form is the foster-father.

**The quest.**
1. **The lost child.** In the Mountains of the Moon, a hunter's boy has been missing for a year and is seen with the monkeys. His mother asks you to find him.
2. **The troop.** Zarude's troop won't let you near. Bring them what the boy liked to eat (a Nanab: his mother tells you) and leave it at the vines' edge three days running.
3. **The boy.** On the third day he comes out, healthy and very dirty. He won't leave without his Dada. Zarude in its cape follows him out and stands between you and him.
4. **The battle.** It battles to see if you're kind. Win and the boy goes home, and Zarude comes with you, because it can visit.

**Battle.** Lv 76, Dada form: Jungle Healing, Power Whip, Darkest Lariat, U-turn.

### 4.18 Terapagos: Achilles and the Tortoise

**The casting.** Zeno of Elea proved that Achilles can never catch a tortoise. Each time he reaches where the tortoise was, it has moved a little on, so he never closes the gap (Aristotle, *Physics* 6.9). Terapagos is the tortoise at the bottom of that gap. Its Stellar form needs Terastallization, which is off in Ichor (PITCH §5), so only its Normal and Terastal forms appear.

**Who.** Zeno, at Elea; and Achilles, if you've met him at Leuke.

**The quest.**
1. **Zeno's bet.** "Nobody can catch it. I proved it." The tortoise sits at the end of Elea's beach.
2. **The chase.** Walk toward it and it moves exactly half the remaining distance away, every step, for ever. A scripted chase that can't be won by walking at it.
3. **The trick.** Stop chasing. Walk to where it's going instead. The tortoise's path bends toward the sea, and if you stand on the tide line ahead of it, it walks up to you.

```text
ZENO: That's cheating.

ZENO: …That's how everything moves, isn't it. I'll need a new proof.
```

4. **Achilles.** If he's met you, he comes to Elea to see it. "I could never catch it either. I didn't know you were allowed to wait."

**Battle.** Lv 90, Normal form, which turns Terastal on entry (Tera Shift): Tera Starstorm, Earth Power, Calm Mind, Rapid Spin. One of the three strongest statics.

---

## 5. Time Fractures: the Paradox Pokémon

**The explanation (§1).** When time went past the old cloth's last row, its cut ends frayed. Through the frayed ends leak the Golden Age behind and the Iron Age ahead. STORY §3 put the fractures in `POSTGAME.md`'s list; the director's brief for this file brings them here (decision PG-29).

**What a fracture is.**
- A shimmering tear on a map, visible some days and not others (rolled daily from `dailySeed`, SYSTEMS §6). The Kronia festival doubles them (SYSTEMS §7).
- Step in and you're in a small pocket map, one of a few reused layouts, tinted gold or iron-gray, with its own wild table: two or three Paradox species.
- **The Golden fractures** sit at Titan and Kronos sites in Aethos (STORY's "the old cloth's frayed edge leaks the Golden Age"). **The Iron fractures** sit in the Oikoumene's places of iron and edges.
- Paradox Pokémon are wild here, not one-only: they breed as normal and stay catchable.

| Fracture | Chart | Age | Species | Lv |
|---|---|---|---|---|
| Kronion Hill, Kalliste | Aethos | Gold | Great Tusk, Sandy Shocks | 66–70 |
| Eleusa's fields | Aethos | Gold | Brute Bonnet, Scream Tail | 66–70 |
| Delphoi, the Kastalian ravine | Aethos | Gold | Flutter Mane | 66–70 |
| Kaldera's rim | Aethos | Gold | Slither Wing | 66–70 |
| Taygetos, Lakonia | Aethos | Gold | Roaring Moon | 66–70 |
| Heliopolis's altar (after Ho-Oh) | Oikoumene | Gold | Walking Wake, Gouging Fire, Raging Bolt: the three wanderers as they were | 74–78 |
| The Chalybes' forges | Oikoumene | Iron | Iron Hands, Iron Treads | 74–78 |
| The Walls of Laomedon | Oikoumene | Iron | Iron Valiant, Iron Thorns | 74–78 |
| The Glass Crater | Oikoumene | Iron | Iron Moth, Iron Jugulis | 74–78 |
| The Cave of Boreas | Oikoumene | Iron | Iron Bundle | 74–78 |
| The Selvage (after Keldeo) | Oikoumene | Iron | Iron Leaves, Iron Boulder, Iron Crown: justice once nobody believes in it | 74–78 |

**The Two Mounts.** Visit all eleven fractures (§7.1's Celebi quest counts them) and the Fates send for you.

```text
LOTIRA: Eleven tears. We've measured them. They're getting no wider.

NEMIRA: But there's one thing on each side we can't measure.

THANIRA: Something big. Waiting at each end of the cloth.
```

- **Koraidon** waits on the Isles of the Blessed, in the golden meadow where Kronos's age never ended. Lv 85: Collision Course, Flare Blitz, Drain Punch, Swords Dance.
- **Miraidon** waits at the Chalybes' great furnace, in the place iron started. Lv 85: Electro Drift, Draco Meteor, Parabolic Charge, Calm Mind.
- Each runs: catch it on the third meeting, as each mount leads you further into its age's fracture first. Neither can be ridden: Ichor has no ride Pokémon in the overworld.

---

## 6. Beyond the Selvage: the Ultra Beasts

**The explanation (§1).** Beyond Okeanos is the cloth that was never woven. Things live there with no threads. They come through where the world's edge has frayed, and they turn up in the edge-lands, where Greek travellers always swore they'd seen marvels.

**The name.** People in the Oikoumene call them the **Peratai**, the "beyond-ones," from *peran*, across. The battle text can keep "Ultra Beast" or say "beast from beyond," the director's call (PG-30).

**Catching them.** The expansion's Beast Ball becomes **Hephaestus's Net**, the golden net that caught Ares and Aphrodite in bed and held them for every god to see (*Odyssey* 8.266–366). Anything caught in it stays caught. Daphne makes them at Naukratis from bronze wire you bring.

**The arc: Beyond the Selvage.**
1. **Lotira notices.** The Measurer, at her sanctuary or wherever you last saw her: "There's something out there we can't measure. Again. You're not the only one now."
2. **The rumors.** Each beast is a "marvel" that a Greek traveler reported from the edge of the world, and a townsperson in that land tells you about it. Follow the rumor; at the place a white tear in the air (different from the gold and iron fractures) shows where it came through.
3. **The catch.** Each is a one-only static that re-forms the next day if it faints.
4. **Poipole.** When seven are caught, a small one comes through at the Selvage and won't leave you alone. It's a gift, Lv 70. It evolves into Naganadel knowing Dragon Pulse.

| Beast | The marvel | Where | Lv |
|---|---|---|---|
| Nihilego | Pytheas of Massalia, sailing to the top of the world, found a "sea-lung" where sea, air and land were one jelly (Strabo 2.4.1) | The Selvage, north, past the Cimmerians | 74 |
| Buzzwole | Egyptians in the marshes sleep up towers or under nets because of the gnats (Herodotus 2.95). Here's what the towers were built against | The Delta Reeds | 74 |
| Pheromosa | The Astomi, a people with no mouths who live on the smell of flowers (Pliny 7.25) | The Gate of Dawn | 74 |
| Xurkitree | A tree in the desert that grows lightning instead of leaves | The Great Sand Sea, in storms | 74 |
| Celesteela | Abaris the Hyperborean carried a golden arrow round the whole world without eating (Herodotus 4.36); later writers had him ride it. The arrow flies by itself | The Hyperborean Meadow | 76 |
| Kartana | A scroll in the Labyrinth of Moeris that cuts whoever opens it | The Labyrinth of Moeris | 74 |
| Guzzlord | The Table of the Sun feeds everyone. Something has been eating all of it | The Table of the Sun, at night | 78 |
| Stakataka | Poseidon and Apollo built Troy's walls. One stretch of wall moves at night | The Walls of Laomedon | 76 |
| Blacephalon | The Blemmyes, men with no heads and faces in their chests (Herodotus 4.191) | The Salt Ridge | 76 |
| Poipole | A small one that likes you | The Selvage | 70 (gift) |

Necrozma came from beyond the selvage too, but its quest is the eclipse (§3.12).

---

## 7. In Aethos's post-game

### 7.1 Celebi: The Thirteenth Hour

**The casting.** The Horai, the Hours, were goddesses who kept the gates of heaven and the turning of time (*Iliad* 5.749–751). When the Lord of Time stopped the world, one Hour was trapped inside the stopped one. In the Frozen Hour, only one thing kept ticking: Daedalus's music box on Elpis's shelf (STORY §2). That was the Hour, hiding.

**Who.** Elpis, at Akti.

**The quest.**
1. **The box.** Elpis's music box, which played the Frozen Hour's lullaby, has started skipping a beat. "It goes tick, tick, tick… and then it doesn't. Like it's gone somewhere."
2. **Where it goes.** Every time a Time Fracture opens anywhere, the box misses a beat. The Hour is slipping out to look through them.
3. **Five fractures.** Visit five fractures. In each, you glimpse something small and green ahead of you, always one room ahead.
4. **Home.** After the fifth, the box stops entirely. Go to Akti. Elpis has wound it, and Celebi is sitting on top of it, listening to the end of the lullaby, which it never heard: the song stopped short in the Frozen Hour, and Elpis finished it at the resolution (STORY §6.14).

```text
ELPIS: It wanted to hear the end. Everybody always falls asleep first.

ELPIS: I didn't. I got to the end. Did you like it?
```

**Battle.** Lv 70: Leaf Storm, Psychic, Recover, Nasty Plot. If you'd rather not battle Elpis's guest, choose to let it go: it comes back the next day and joins without one.

### 7.2 Heatran: The Forge Under the Forge

**The casting.** PITCH §4: the forge beneath the volcano. Hephaestus's forge was under a volcano; something older than the smith keeps it hot.

**Who.** Talos, the sixth Hierophant, at Kaldera.

**The quest.**
1. **Warm in winter.** "My forge is warm on the coldest day of the year. I don't stoke it that much."
2. **Under the forge.** On Kaldera's caldera floor, a boulder only Hephaestus's Hammer can move (`POSTGAME.md` §3.4's suggestion, kept) hides a vent that runs under Talos's forge into lava tubes below the Telchines' sea-cave. Pitch dark, and too hot for Hecate's Torch: it gutters out.
3. **Hyperion.** Talos fetches Hyperion from the bellows. He can't see, and doesn't need to. He listens and calls the way: "Left. It breathes on the left." A walk through the dark with your torch doused (SYSTEMS §2) and a blind man's directions.
4. **The heart.** At the bottom, on the ceiling, upside down, Heatran.

**Battle.** Lv 72: Magma Storm, Earth Power, Flash Cannon, Stealth Rock.

**Reward.** Talos forges you a **Magma Stone**, which doesn't exist in the expansion: a held item that powers up Fire moves for Heatran only (a small new item; or drop it and give Charcoal, decision PG-32).

### 7.3 Type: Null and Silvally: The Statue That Runs Away

**The casting.** Socrates says Daedalus's statues were so lifelike that if they weren't tied down they'd run away (Plato, *Meno* 97d). Type: Null is one of Daedalus's beasts, kept in a mask and bindings so it won't. Its Memories are the Phaistos Disc, the real clay disc from Minoan Crete stamped with signs no one can read: here, seventeen of them.

**Who.** Daedalus, in his workshop under Knossa (LABYRINTH).

**The quest.**
1. **The bound one.** In the workshop's back room, a masked beast stands tied to a post. Daedalus: "I tied it so it wouldn't run off. Then I forgot how to untie it. Then I was afraid to."
2. **The gift.** He gives it to you, Lv 70, still masked. "It'll stay with someone who won't tie it."
3. **The bindings.** At full friendship it breaks its mask and becomes Silvally (the expansion's condition).
4. **The discs.** Seventeen Phaistos Discs, one per type, are scattered in the Minoan vaults (LABYRINTH §9) and the Oikoumene's ruins. Each changes Silvally's type.

### 7.4 Magearna: The Golden Handmaid

**The casting.** Hephaestus was served by handmaids made of gold who could move, speak and think (*Iliad* 18.417–420). PITCH §4 casts Magearna as his golden automaton.

**Placed by.** SYSTEMS §3 makes Magearna Hephaestus's gift III, at Favor 100. That stays. This file only stages it.

**Staging.**
1. **The tinker returns.** At Favor 100, the lame tinker from Hephaestus's theoxenia (SYSTEMS §10) knocks at Talos's forge.
2. **The handmaid.** He has brought a golden maid whose heart has stopped. "She was the last one I made before I went to sea. Her heart's a little wheel. It wants a reason to turn."
3. **The reason.** The heart turns for kindness: walk her round Kaldera, and at each house someone says hello to her. Seven hellos, and she moves.
4. **The gift.** Lv 75, with Fleur Cannon, Flash Cannon, Calm Mind and Protect.

### 7.5 Marshadow: The Shadow Hermes Left

**The casting.** The gods have no shadows when they walk in disguise: that's the first tell of theoxenia (SYSTEMS §10). Ichor asks where the shadows go. Marshadow is a god's shadow, left behind.

**Gate.** The theoxenia finale at Mom's table, Zeus and Hermes in the storm (SYSTEMS §10). If the user chooses the core tier only (SYSTEMS D8), the gate becomes Hermes's E1 visit instead.

**The quest.**
1. **The morning after.** The guests are gone. On the floor where Hermes sat, there's a shadow with nobody in it.

```text
MOM: {PLAYER}. Don't step on that.

MOM: …He's forgotten his shadow. Typical.
```

2. **It follows you.** For the rest of the day the shadow copies you, a step behind (the engine's copy-the-player movement, §9). It won't let you catch it while you can see it.
3. **The trick.** Hermes's own advice: "Always check the feet." Stand still in Elaia's square at noon, when you have almost no shadow. Your shadow and the stray one overlap, and it can't tell which is which.
4. **The battle.** It steps out of your shadow and fights.

**Battle.** Lv 75: Spectral Thief, Close Combat, Shadow Sneak, Bulk Up.

### 7.6 Ogerpon, Okidogi, Munkidori, Fezandipiti and Pecharunt: The Satyr Play Nobody Wrote

**The casting.** PITCH §4 makes Ogerpon the Dionysia's comedy and tragedy masks. In Kitakami, three "heroes" with a statue were really the villains, and the "ogre" was the hero. That's a satyr play: the story the tragedy leaves out. Thespis, the fourth Hierophant, broke Iapetos's trance at the Dionysia with one (STORY §6.3).
- **Ogerpon** is a satyr: the vineyard's guardian, slandered as a monster, who keeps four masks (its Teal, Wellspring, Hearthflame and Cornerstone forms).
- **Okidogi, Munkidori and Fezandipiti** are three "heroes" with a statue in Thyrsa's vineyards, honored for driving off "the monster."
- **Pecharunt** is **Methe**, Drunkenness, Dionysus's companion: a poisoned vintage that makes whoever drinks it obey.

**Gate.** The League. Two festivals finish it, a month apart in SYSTEMS §7's calendar: Pecharunt at the Anthesteria in Anthesterion, when the new wine jars are opened, and Ogerpon at the City Dionysia in Elaphebolion, where `POSTGAME.md` §3.4 suggested it.

**The quest.**
1. **The statue.** In Thyrsa's vineyards, three heroes in stone: a dog, an ape and a pheasant. Every year the town toasts them for saving the harvest from a monster. Thespis is bored of it.

```text
THESPIS: Three heroes, one monster, no jokes. It's a tragedy. Badly written.

THESPIS: Every tragedy needs a satyr play after it. Somebody left this one out.
```

2. **The monster.** At the vineyard's edge, a masked creature watches you, then runs. Follow it to its hollow: four masks on pegs, and the grapes it has been guarding all year.
3. **The heroes.** Three Pokémon who match the statue live in the vineyard's fine houses. Each battles you on sight, eyes glassy: Okidogi at the press, Munkidori in the drying-loft, Fezandipiti on the trellis roof. Lv 74 each. Beaten, each sobers up for a moment and says one thing about the wine.
4. **The jars.** At the Anthesteria, the jars are opened. One jar is opened by itself from inside. Pecharunt is the vintage. Lv 78.
5. **The play.** Thespis writes the real story, *The Satyr Who Was the Hero*, and stages it at the next City Dionysia. Ogerpon comes to watch, from the back, in its tragedy mask. When the audience laughs in the right place, it comes down to the orchestra and battles you as a bow. Lv 76.

**Battles.** Okidogi: Bitter Malice, Drain Punch, Crunch, Bulk Up. Munkidori: Sludge Bomb, Psychic, Fake Out, U-turn. Fezandipiti: Moonblast, Beat Up, Roost, Heat Wave. Pecharunt: Malignant Chain, Shadow Ball, Parting Shot, Recover. Ogerpon: Ivy Cudgel, Horn Leech, Knock Off, Spiky Shield.

**Reward.** The four masks (the expansion's mask items) for Ogerpon's forms. Its Tera forms need Terastallization and are off.

### 7.7 Quests that cross the two charts

Three quests elsewhere in this file touch Aethos: Latias and Latios start at Therapne in Lakonia and end at sea in the Oikoumene (§3.4); Calyrex's straw relay starts at Delos beside Route 2 (§3.14); and Enamorus, the end of the Forces arc, is caught at Kythera's spring in Aethos (§3.9).

---

## 8. Placed elsewhere: notes for the other docs

Reconciled with `POSTGAME.md` §4's list. Everything below is the other docs'; this file only notes how it fits.

| Pokémon | Owner | Notes |
|---|---|---|
| Lugia (Leukothea), Manaphy, and Phione by breeding with Ditto from Pharos | `POSTGAME.md` §3.2, Atlantis | Atlantis stays on the Aethos chart; the Pillars look out toward it (OIKOUMENE §4.8) |
| Kyogre (Oceanus), Groudon (Gaia), Rayquaza (Ouranos), Arceus | `POSTGAME.md` §3.3 | Arceus at Lv 95 stays the game's strongest battle; nothing here passes 92. Chaos, the Gap, is Arceus's to fill, which is why Palkia here is Plato's Chora instead (§3.5) |
| Kairazor, Pegaunos, the colossi, Ichorin | `POSTGAME.md` §3.1, §3.4 | The dex team set Ichorin at Lv 70 and the Fates at 60; POSTGAME §4's table still says Ichorin 80 and the Fates 50, and should follow the dex |
| Victini (Nike) | `POSTGAME.md` §3.1 | This file's first-draft quest gave way (§4.6) |
| Regirock, Regice, Registeel, Regieleki, Regidrago, Regigigas | `UNDERWORLD.md` §4.10 | Tartarus's five cells and Briareus's gate. Settled: the first draft's fallback for Regieleki and Regidrago is dropped |
| Giratina (Tartaros) | `UNDERWORLD.md` §4.11 | — |
| Cresselia, Darkrai | `UNDERWORLD.md` §6, the House of Night (stretch) | This file's first-draft quest gave way (§3.6). Decision PG-26 asks for the House of Night in 1.0; failing that, they wait at the Land of Dreams |
| Tornadus | `ODYSSEY.md` §6.4 | The Forces arc here starts from the same opened bag (§3.9) |
| Xerneas | `LABORS.md` Labor 3 | Yveltal's quest (§3.8) is its opposite and follows Labors 6 and 9 |
| Zapdos | Moved here from SYSTEMS §3's Zeus gift III | Zeus's gift III becomes a unique Aetarch, the eagle LABORS's Labor 11 already uses (PG-27) |
| Magearna | `SYSTEMS.md` §3, Hephaestus gift III | Staged in §7.4; the rule and the gate stay SYSTEMS's |

**POSTGAME §3.4's proposed homes,** which §4 hands to this file: kept are Heatran at Kaldera behind the Hammer boulder (§7.2), Enamorus at Kythera (§3.9), Latias and Latios from Lakonia (§3.4) and Ogerpon at Thyrsa's City Dionysia (§7.6). Moved to the Oikoumene, as §4 allows: Ho-Oh to Heliopolis, where Herodotus's phoenix brings its father in an egg of myrrh (2.73); Meloetta to the mouth of the Hebros, where Orpheus's head came singing down the river; the Treasures of Ruin to four places across the Oikoumene (§3.15); and the Paradox Pokémon and Ultra Beasts to the Time Fractures and the Selvage (§5, §6; PG-29).

**What this file now leans on from the epics,** so their authors know: LABORS's Labor 6 (where the Stymphalian flock goes), Labor 9 (Hippolyta's shield-maidens), Labor 10 (Helios's cup) and Labor 11 (Prometheus freed, his ember); ODYSSEY's Aiolia (the opened bag, the Mirror of Truth); POSTGAME's Olympia (Achilles, whose silver symbol opens Leuke, §3.13); and UNDERWORLD's House of Night, for which §3.6 offers two beats.

---

## 9. Engine feasibility

Every mechanic here uses something the expansion or an approved Ichor system already has, except where marked new.

| Mechanic | Used by | How | Effort |
|---|---|---|---|
| Statics that return until caught | All | A daily flag reset in `DoDailyEvents` (`src/clock.c`) per static | Low |
| Omen wanderers | The beasts, Latias and Latios | SYSTEMS §6's rare-visitor omen with hide flags. Avoids `ROAMER_COUNT`, which is 1 (`include/constants/global.h` line 110); raising it grows SaveBlock1 | Low |
| Alternate days | Latias and Latios | Parity of `gLocalTime.days` | Low |
| Time-of-day windows | Moltres, Dialga, Solgaleo, Genesect | `GetTimeOfDay()` (Gen 8+ hours, `include/constants/rtc.h`) | Low |
| Festival days | Shaymin, Pecharunt, Herakles's rematch | `Ichor_GetFestival` (SYSTEMS §7) | Low |
| Carried things | Mew (Prometheus's ember), Amphirho's spring and Volcanion (water), Ho-Oh (the egg) | SYSTEMS §2's carried-flame grammar, reused for a water jar and an egg; the "don't run" flag from SYSTEMS §10 | Low |
| Timing gates | The Clashing Rocks side channel (OIKOUMENE §2) | `Ichor_BullLeap` (LABYRINTH §3) | Low |
| Ordering puzzle | Dialga's twelve doors | Twelve door warps and one var that counts the hours walked in order; a wrong door warps you to the first | Low |
| Escort under a shield-roof | Yveltal | Scripted movement for the maidens, as SYSTEMS's escorts use (not the expansion's NPC followers, which cost SaveBlock3), plus a volley timer that checks whether you stand under them | Low–Medium |
| Follow-the-glint blizzard | Articuno | Scripted per screen; a wrong turn warps you back | Low |
| Mirrored controls | Mewtwo's isle, walked in the Mirror of Truth | A per-map flag that swaps left and right in `src/field_player_avatar.c`'s input handling, and a horizontally flipped camera view (or simply flipped map art) | Low–Medium (new) |
| The halving chase | Terapagos | Scripted object movement that halves the gap each step | Low |
| The shadow that copies you | Marshadow | `MOVEMENT_TYPE_COPY_PLAYER` (`include/constants/event_object_movement.h`) | Low |
| Invisibility and an unguarded town | Hoopa | `OW_FLAG_NO_TRAINER_SEE` (the Helm, SYSTEMS §1) plus per-stall item scripts that check a flag | Low |
| The eclipse | Necrozma | A scripted palette darken; the same tint tools as the Frozen Hour (STORY §8.4) | Low–Medium |
| Lyre playback | Meloetta | A `dynmultichoice` sequence from the Relic Ring (SYSTEMS §1) | Low |
| The cell count | Zygarde | 14 flags; the chest's use script sets the form. The expansion has `ITEM_ZYGARDE_CUBE`, but cell collection is new | Medium |
| Form-change items | Deoxys, Shaymin, the Forces, Kyurem, Necrozma, Hoopa, Calyrex, Zacian and Zamazenta, Dialga and Palkia, Silvally, Ogerpon, Urshifu | All exist: `ITEM_METEORITE`, `GRACIDEA`, `REVEAL_GLASS`, `DNA_SPLICERS`, `N_SOLARIZER`, `N_LUNARIZER`, `PRISON_BOTTLE`, `REINS_OF_UNITY`, `RUSTED_SWORD`, `RUSTED_SHIELD`, `ADAMANT_CRYSTAL`, `LUSTROUS_GLOBE`, the Memories, the masks, `SCROLL_OF_DARKNESS` and its pair (`include/constants/items.h`). Renames only; `REVEAL_GLASS` is ODYSSEY's Mirror of Truth | Low |
| Hephaestus's Net | The Ultra Beasts | `ITEM_BEAST_BALL`, renamed | Low |
| Cosmog's day and night | Solgaleo, Lunala | Already in the species data (`IF_NOT_TIME, TIME_NIGHT`, `gen_7_families.h` line 6353) | None |
| Kubfu's scrolls | Urshifu | `EVO_SCRIPT_TRIGGER` with the dark and water triggers, already in the data | None |
| Iceroot and Shaderoot | The horses | Two new key items | Low (new) |
| Magma Stone | Heatran | A new held item | Low (new, optional) |
| Fracture pockets | Paradox | A handful of reused pocket layouts with tinted palettes; warps from a daily-rolled tear object | Low–Medium |

**What doesn't work, honestly.**
- **Terapagos's Stellar form** and **Ogerpon's Tera forms** need Terastallization, which is off. They're forms, not species, so the National Dex is unaffected.
- **Eternatus's Eternamax form** was never obtainable in the originals and needs Dynamax.
- **Zygarde's cell collection** is new script work, the biggest single item here.

---

## 10. The 100%: completing the Oikoumene Dex

Every one of the 1,025 National Dex species (the **Oikoumene Dex**, if PG-13 is approved) can be caught in one save, with no link cable, no event distribution and no second game. The Aethos Dex's 152 are on top. `POSTGAME.md` §5 defines 100% as the **Kleos page's twelve laurels**; laurel 8 is the Aethos Dex and laurel 9 the Oikoumene Dex, and this section is how a player earns laurel 9. The ending itself, the Loom and Halia's spindle, is POSTGAME's.

### How the 1,025 add up

| Route to the dex | Species | Where it's specified |
|---|---:|---|
| Wild in the Oikoumene | 406 | `oikoumene/COVERAGE.md` |
| A Nursery, or breeding | 247 | `oikoumene/COVERAGE.md` |
| Evolving a caught Pokémon (the Xenion for trades) | 178 | `oikoumene/COVERAGE.md`, special handling |
| Legendary, mythical, Ultra Beast or Paradox | 125 | This file, §2, and the epics it names |
| A theoxenia guest-gift line | 54 | `SYSTEMS.md` §10 |
| A fossil | 15 | `oikoumene/COVERAGE.md` |
| **Total** | **1,025** | |

### The checklist a player follows

1. **Finish the story,** then sail: the near lands open with the ship, and the Odyssey gives Aeolus's Bag for the rim.
2. **Walk the ten lands** for the Periodos. Most wild species come on the way.
3. **Do the four epics.** The Labors, the Katabasis, the Odyssey and Atlantis place 19 of the 125 legends, and LEGENDS's quests lean on several of them.
4. **Breed and visit the Nurseries** for first stages. The egg-ovens at Naukratis, with Hera's blessing, halve the work.
5. **Use the Xenion** for trade evolutions, and the Oikoumene Agoras' evolution items.
6. **Dig** for fossils and have Daphne revive them.
7. **Accept every stranger's request** in Aethos, for the eighteen guest-gift lines.
8. **Do the legend quests.** The Scroll of Deeds lists each open lead.

### The rewards

Daphne keeps the count at Naukratis and at the Akademia. Her lines are drafts.

| Milestone | Reward |
|---|---|
| Aethos Dex, all 152 caught | Kleos laurel 8, and a diploma painted on a kylix (TERMS.md's trainer card art) |
| Oikoumene Dex, 250 caught | An Ability Patch |
| 500 caught | The **Oval Charm**, renamed **Hera's Pomegranate**: eggs come more often (`ITEM_OVAL_CHARM`) |
| 750 caught | Three Golden Pythian Laurels (SYSTEMS §11) |
| 1,000 caught | The **Catching Charm**, renamed **Artemis's Arrow** (`ITEM_CATCHING_CHARM`) |
| **All 1,025** | **Kleos laurel 9,** and **the Acorn of Dodona**, the Shiny Charm (SYSTEMS §3). If Zeus already gave it at Favor 60, Daphne gives the **Exp. Charm** instead, renamed **Apollo's Laurel** (`ITEM_EXP_CHARM`) |

**The shiny charm two ways.** SYSTEMS makes the Acorn of Dodona Zeus's gift II, earned by faith. The 100% gives it too, earned by knowing every creature. Either road gets there, which suits a game about choosing your own (PG-20).

**Daphne's last question.** POSTGAME gives Daphne her last lecture on Atlantis's deck. This is her last question, with all 1,025 caught (STORY §2, P2).

```text
DAPHNE: You've seen every one. All of them. In the whole world.

DAPHNE: So tell me. Which came first? The myth, or the Pokémon?
```
?? THE MYTH / THE POKÉMON / WE'LL SEE
```text
> THE MYTH / THE POKÉMON:
DAPHNE: Hm. A guess is only a question that's gotten too confident.

> WE'LL SEE:
DAPHNE: …Yes. I suppose we will.
```

---

## 11. Scope, ROM and decisions

### The verbs, tallied

So no two quests feel alike, here is what each asks of you.

| Verb | Quests |
|---|---|
| Chase or pursuit | Zapdos (the boy), Zeraora, Terapagos, Mesprit (by not chasing), Koraidon and Miraidon, Elektra's race |
| Riddle or reasoning | Uxie, Metis, Terrakion (the liar), Hypatia |
| Ordering puzzle | Dialga's twelve doors |
| Escort or relay | Zapdos's shepherd boy, Calyrex's straw, Magearna's walk, Yveltal's shield-roof |
| Offering or gift | Ho-Oh's egg, Landorus's ten berries, Virizion's berries, Shaymin's thank-yous, Plouto's thing that ends, the beasts' altars |
| Timing, hours and days | Moltres (dusk), Dialga (sunset), Genesect (three dawns), Latias and Latios (alternate days) |
| Festivals | Shaymin (Pyanopsia), Pecharunt (Anthesteria), Ogerpon (City Dionysia) |
| Constellations and the chart | Jirachi (all 24), Deoxys (four marks), Latias and Latios (Gemini), Meloetta (Lyra), Diancie (Corona Borealis) |
| Carried things | Mew (Prometheus's ember), Amphirho and Volcanion (water), Ho-Oh (the egg) |
| Navigation puzzles | Articuno's blizzard, Mewtwo's mirror, Heatran's dark, Palkia's edge |
| Moral tests | Hoopa (the ring), Jirachi (the wish), Cobalion (judgments) |
| Music | Meloetta |
| Endurance | Azelf's six battles |
| Collection | Zygarde's pieces, Melmetal's iron, the Treasures' nails, the Silvally discs |
| Theoxenia | Marshadow, Magearna |
| A friend carries it | Alethea (Reshiram, Kyurem, Mewtwo), Kleon (Zekrom, Latias, Kyurem), Elpis (Celebi, the Treasures), Hyperion (Cosmog, Necrozma, Heatran), Hypatia (the soul trio, Dialga, Palkia), Ariadne (Diancie), Thespis (Ogerpon), Achilles (Zacian, Zamazenta), Prometheus (Mew), Hippolyta's shield-maidens (Yveltal), Lotira (the Ultra Beasts), Mom (Marshadow) |

### Scope

| Tier | What |
|---|---|
| **1.0** | Every species obtainable, through the simplest version of its quest: the master table's placements, every battle, every form item, the Time Fractures with their tables, the Ultra Beasts as statics with rumors, Poipole, and the 100% rewards. Every quest keeps at least its first and last step |
| **Stretch** | Each quest's full step list: the blizzard, the mirror walk, the halving chase, the eclipse, the relay of straw, the invisible town, the lyre playback, the twelve doors, the shield-roof, Zygarde's fourteen pieces |
| **Later** | Rematch versions of the strongest legends; alternate dialogue when a friend is absent; a Scroll of Deeds page for every lead |

### ROM estimate

| Item | Size |
|---|---:|
| Scripts and text for about 55 quests | ~160 KiB |
| About 25 small new maps (sanctuaries, shrines, fracture pockets, the Gorgons' Isle, the Isle of Ares, the Caucasus caves) | ~70 KiB |
| Large overworld objects for the legends (about 40, 32×32 and up, sharing palettes) | ~60 KiB |
| New items and icons (Iceroot, Shaderoot, Magma Stone, the Pythia's Feather, renamed form items' icons) | ~5 KiB |
| Code (mirrored input, cell count, fracture rolls) | ~5 KiB |
| **Total** | **~300 KiB** |

All the species, their sprites and their cries are already in the ROM.

### Decisions for the user

This file's decisions are folded into the post-game's consolidated list in `OIKOUMENE.md` §13, alongside POSTGAME's P1–P11. The ones that are this file's:

| # | Decision | Recommendation | First draft's number |
|---|---|---|---|
| PG-20 | **The 100% reward:** the Acorn of Dodona by knowledge as well as by Zeus's Favor | Yes | D-L9 |
| **PG-26 ★** | **The House of Night in 1.0,** so Cresselia and Darkrai can be caught; else they wait at the Land of Dreams | Make it 1.0 | — |
| PG-27 | **Zapdos joins its trio here**, and Zeus's gift III (SYSTEMS §3) becomes a unique Aetarch | Yes: STORY already moved Zeus's eagle to Aetarch, and LABORS's Labor 11 uses one | D-L1 |
| PG-28 | **Jirachi is SYSTEMS §8's star-born reward** for all 24 constellations | Yes | D-L3 |
| **PG-29 ★** | **Time Fractures and the Ultra Beasts are this file's:** Golden fractures in Aethos, Iron fractures in the Oikoumene, after Hesiod's ages; the Ultra Beasts at the Selvage instead of POSTGAME's Sky Fractures | Yes | D-L4 |
| PG-30 | **The Ultra Beasts' name:** the Peratai, "the beyond-ones," in dialogue; the battle text keeps "Ultra Beast" | Yes | D-L5 |
| **PG-31 ★** | **The legend castings as a set:** Plato's soul for the lake trio; Chronos and Chora (Plato's *Timaeus*) for Dialga and Palkia; the Hours for the Swords; truth and glory for Unova's dragons; the Isles' four Okeanids for the Tapus; Hyperion's children for the sun and moon; the dark bird of Ares's island for Yveltal; Pandora's evils and Elpis for the Treasures | Yes | D-L8 |
| PG-32 | **Small items:** a Magma Stone for Heatran (optional; Charcoal is fine), and Jirachi joins without a battle if you wish for nothing | Optional; yes | D-L6, D-L10 |

**Settled since the first draft:** D-L2 (Regieleki and Regidrago are UNDERWORLD's) and D-L7 (the dex team set the Fates at Lv 60 and Ichorin at 70).

### The Lazarus check

- **No Muses.** Meloetta is Orpheus's song.
- **No Chimera.** Type: Null is Daedalus's runaway statue, never a chimera.
- **No Greek-named beast trio.** Raikou, Entei and Suicune keep their names and stay a side quest.
- **No prefixed forms:** no Aegis, Gryphon, Medusa or Titan anything. The Gorgons are never named Medusa; the gold-guardians are never called gryphons.
- **Rayquaza isn't central** and isn't here.
- **Mega Evolution is never a weapon.** The Ichor Stones here are rewards.
