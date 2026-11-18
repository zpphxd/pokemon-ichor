# Ichor terms

The canonical Ichor word for every Pokémon-system term. Use it in scripts, system text, item and menu names. Where the bible (`PITCH.md`) or the Phase 1 script (`phase1/SCRIPT.md`) already decides, this file only repeats it. Rows marked **Flag** are new calls that the director has not ruled on yet.

`tools/ichor/text_width.py` measures any string against the game font, so every label below has been checked against its window.

## How to write them

- **Prose is sentence case.** Message boxes, battle text and descriptions write "Pokémon", "the Asclepeion", "your Bag", the way the slice scripts and the expansion's battle text already do. The old all-caps nouns ("POKéMON", "BAG", "PC") go when a line is rewritten.
- **Labels stay in capitals.** Menu entries, window headers and info-panel tags keep Gen 3's capitals ("LAURELS", "AUGURY", "SAVE"). On a pottery frame they read like an inscription.
- **People's names** are capitals in name boxes and trainer names (KLEON, DAPHNE) and mixed case in prose ("Daphne told me…"). The player's default names are THEO and IANTHE.
- **"Professor"** is spelled out in prose. In a label it is "PROF. DAPHNE".
- **Keep these as they are:** Pokémon, Poké Ball, TM, Pokérus, Egg, Trainer, Bag, HP, PP, money and the ¥ sign. "Poké Ball" stays both as the plain ball's item name and as the generic word for every ball (the POKé BALLS pocket, "Poké Ball" in battle text); the other balls take the names in [the Poké Balls](#the-poké-balls).

## The world and its people

| Hoenn term | Ichor term | Label | Source and notes |
|---|---|---|---|
| Hoenn | Aethos | AETHOS | PITCH §1 |
| Hoenn Dex | the Aethos Dex | AETHOS DEX | The regional dex mode. |
| National Dex | the National Dex | NATIONAL DEX | Not a Hoenn word, so it stays. **Flag:** "National" is anachronistic. *Oikoumene* ("the known world") would fit if the director wants a Greek name. |
| Prof. Birch | Professor Daphne | PROF. DAPHNE | PITCH §2. Female. |
| Brendan / May | Theo / Ianthe | THEO / IANTHE | Default player names (PITCH §2, `main_menu.c`). The `{RIVAL}` placeholder expands to the other hero's name, as in Emerald. Ichor's rival is Kleon, and scripts name him directly. |
| Wally (the catch-tutorial partner) | Alethea | ALETHEA | **Flag.** The engine's catch tutorial is the only place this shows. Alethea is Daphne's apprentice and the natural teacher. |
| Lanette, Bill (the PC's maker) | none | | The Pithos has no inventor. "Someone's PC" and "Lanette's PC" both become "the Pithos". |
| Mom | Mom (Melitta) | MOM | SCRIPT Part 7. Prose calls her Mom. |
| Dad's advice (wrong item use) | Mom's advice | | Emerald's Dad is a Gym Leader. Ichor has no father in the story, and Mom is the one who sends you out. |
| Team Aqua / Team Magma | Team Titan, the Titanborn | TEAM TITAN | PITCH §2. Archie and Maxie have no single counterpart: the admins are Hyperion, Iapetos and Rhea, under Kronos. |

## Places and services

| Hoenn term | Ichor term | Label | Source and notes |
|---|---|---|---|
| Pokémon Center | the Asclepeion | ASCLEPEION | PITCH §1. Its keeper is "the healer". "Scurried to a Pokémon Center" becomes "hurried to the Asclepeion". |
| Poké Mart | the Agora (a stall in it) | AGORA | PITCH §1. Its keeper is "the stallkeeper". |
| Gym | Temple | TEMPLE | PITCH §1 and §3. Gym trainers are acolytes. |
| Gym Leader | Hierophant | HIEROPHANT | PITCH §3. |
| Pokémon League | the Pantheon | PANTHEON | PITCH §1. On Mount Olympus. |
| Elite Four | the Pantheon (its four seats) | PANTHEON | PITCH §1 and §3. One member "holds a seat of the Pantheon". |
| Champion | the Archon | ARCHON | PITCH §1. Aristeides the Just. Beating him makes you Archon of Aethos (**Flag**: the bible never says the title passes to the player, but the Hall of Fame line now says so). |
| Gym, in the Oikoumene | a hall | | `oikoumene/PERIODOS.md` (decision PG-33). The Oikoumene's lands aren't Greek, so their halls aren't temples: each is its land's own seat, under its own name (the Skaian Gate, the treasury of Croesus, the precinct of Proteus). "Hall" is the word in prose; no label shows it. |
| Gym Leader, in the Oikoumene | the land's champion, under their own title | PRINCE, KING, PRIESTESS, PRIEST, PHARAOH, HUNTRESS, ATHLETE, JUDGE | `oikoumene/PERIODOS.md` §1. "Champion" is the plain English word here, in lower case; the League's title is still the Archon. Helen, who battles in Memphis, is QUEEN. Widths 24–54 px. |
| Hall of Fame | the Hall of Heroes | HALL OF HEROES | **Flag.** The bible has no name for it. "Heroes" in the Greek sense: people the age remembers. *Heroön* (a hero's shrine) is the scholarly option. |
| Battle Frontier | the Olympiad | OLYMPIAD | PITCH §6. A cut system for now; its text is left alone. |
| Ferry, S.S. Tidal | trireme | TRIREME | PITCH §1. The Phase 1 trireme is the *Euploia*. |
| Mach Bike, Bike | the Chariot | CHARIOT | The user's decision (2026-11-16). One chariot, pulled by a pony, with the Mach Bike's speed; the Acro Bike stays unused. Sold, not given: ¥10,000 from Alfred at Waltz Chariots, beside the Deigma in Emporion (`data/maps/EmporionCity_ChariotStore`). The item is still `ITEM_MACH_BIKE` in code. |
| Rydel's Cycles (the bike shop) | Waltz Chariots | WALTZ CHARIOTS | The user's names: the store and its owner, Alfred, a wheelwright from the far east who came in by sea. Both are the user's exceptions to CLAUDE.md's Greek-rooted naming rule. |

## Things you carry and use

| Hoenn term | Ichor term | Label | Source and notes |
|---|---|---|---|
| Badge | Laurel | LAURELS | PITCH §1. Laurel leaves woven into a victory crown. "Laurel" is capitalized when it is named ("the Hearth Laurel") and lower case otherwise ("your first laurel"). |
| The eight badge names | the eight Laurels, below | | Only the Hearth Laurel is in the script. The other seven are **Flag**. |
| Badge, in the Oikoumene | Emblem | EMBLEMS | `oikoumene/PERIODOS.md` §1 (decision PG-34). The Greek *emblēma* is a picture set into something, like the inlaid panel of a mosaic floor: each champion's Emblem is set into its land's panel of Alethea's chart. Capitalized when named ("the Scarab Emblem"), lower case otherwise. EMBLEMS is 42 px, the same as LAURELS. The ten names are below. |
| PC / Pokémon Storage System | the Pithos | PITHOS | PITCH §1. The great storage jar. |
| Box (in the PC) | Jar | JAR | **Flag.** The Pithos holds jars; the storage art is being redrawn as jars (INVENTORY §5). New games name them JAR1 to JAR14. |
| Item storage in the PC | your stored things | ITEM STORAGE | Shared by the Pithos and the kibotos (the wooden chest at home), so the wording names neither. |
| Pokédex | Pokédex | POKéDEX | SCRIPT beat 3: "It's a Pokédex." The art is a codex. |
| DexNav | the Augur's Eye | AUGURY | PITCH §5 and SCRIPT beat 5. The start menu has 48 px for a label and "AUGUR'S EYE" needs 60, so the menu reads AUGURY, the augur's craft. **Flag:** the alternative is widening the start menu two tiles, which is an engine edit. |
| Trainer Card | Trainer Card | TRAINER CARD | **Flag.** The art becomes a kylix (ART_PLAN §5), but "Kylix" alone doesn't tell a player what it is. Kept until the director decides. |
| PokéNav | none | | A cut system (INVENTORY §10). Its menu entry never shows, because its flag is never set. |
| Running Shoes | Talaria | | PITCH §5. Mom's gift. |
| HMs | relics | | PITCH §5. Cut becomes the Labrys, Fly Daedalus's Wings, Surf Poseidon's Conch, Strength the Girdle of Herakles, Rock Smash the Bronze Hammer, Flash Hecate's Torch, Dive the Nereid Pearl. **Not applied yet:** none of the relics exist, and the field prompts ("Would you like to SURF?") still describe the HM mechanic. They change when the relic system lands. |
| Mega Ring | the Omphalos | | PITCH §5. **Not applied yet**, with the next two rows: see the note below the table. |
| Mega Stones | Ichor Stones | | PITCH §5. Item names (`src/data/items.h`). |
| Mega Evolution | Apotheosis | | PITCH §5. Form names keep "Mega" (Mega Charizard X), so the battle line becomes "rose to Apotheosis as Mega Charizard X!". |
| Money, ¥ | money, ¥ | MONEY | Director's ruling 5: the currency stays unnamed. **Flag:** the ¥ glyph is the Pokédollar sign. The drachma is the obvious name if it ever gets one; the obol is already Charon's fee in the post-game. |
| Mystery Gift, Wonder Card, Wonder News | none | | A cut system (INVENTORY §10). Left alone. |
| Day Care | the Nursery of Nysa | NURSERY | **Decided** (user, 2026-11-18): "the Nursery of Nysa" is the name, in place text and system text alike ("the nursery" for short). The nymphs of Nysa nursed Dionysus. Its keepers are Makris and Aristaios (`design/maps/NurseryOfNysa.md`). |

**Apotheosis waits for one pass.** The two battle lines (`STRINGID_MEGAEVOREACTING`, `STRINGID_MEGAEVOEVOLVED` in `src/battle_message.c`) are asserted word for word by the expansion's tests (`test/battle/trainer_slides.c` and four more), and the bag would still say "Mega Ring". Rename the items, the two lines, the trigger art and those tests together, in Phase 4.

## The Poké Balls

The user's ruling (2026-11-17): every ball gets Ichor art and a Greek name, the Master Ball is **Daedalus Ball** and the Dive Ball is **Poseidon Ball**. Each ball is named "&lt;figure&gt; Ball" for the figure whose story matches what it does, so the name hints at the effect. **Only the names, descriptions and art change:** every catch rate, item constant (`ITEM_DIVE_BALL` and the rest) and ball id is upstream's. The plain **Poké Ball keeps its name**, because it is also the generic word (see above); it keeps its red-over-white look too, in terracotta and marble.

The art: `tools/ichor/art/balls.py` draws the battle sprites (`graphics/balls/`, closed, opening and open) and the bag icons (written through `items.py`); each cap carries its figure's mark, from `ball_motifs.py`. Each ball's `openFadeColor` in `src/battle_anim_throw.c` is its cap's light, so a Pokémon comes out of a Poseidon Ball sea-blue. Widths are the bag's narrow font; the bag allows 88 px and the shop about 76 before the price.

| Upstream | Ichor | Width | Why this figure |
|---|---|---|---|
| Poké Ball | **Poké Ball** | 41 | Kept: the generic word. |
| Great Ball | **Theseus Ball** | 56 | The hero who bound the bull of Marathon. A step up from a Poké Ball. |
| Ultra Ball | **Herakles Ball** | 60 | His labors brought beasts back alive. A step up from Theseus. |
| Master Ball | **Daedalus Ball** | 60 | User's name. Nothing finds its way out of Daedalus's work (LABYRINTH Scene D). |
| Premier Ball | **Xenia Ball** | 45 | *Xenia*, the guest-gift: the Agora throws one in for every ten balls. |
| Heal Ball | **Asclepius Ball** | 64 | The healer god: the catch is healed. |
| Net Ball | **Arachne Ball** | 56 | The weaver turned spider: good on Bug and Water types. |
| Nest Ball | **Alcyone Ball** | 55 | The halcyon's calm-sea nest: good on weaker Pokémon. |
| Dive Ball | **Poseidon Ball** | 60 | User's name. Good on Pokémon in the water. |
| Dusk Ball | **Nyx Ball** | 36 | Night herself: good at night and in caves. |
| Timer Ball | **Chronos Ball** | 56 | Time: stronger as the battle runs on. **Flag:** Chronos (time) and Kronos (the villain's Titan) were run together in antiquity; the spelling keeps them apart, but the director may prefer *Horai* (the Hours). |
| Quick Ball | **Hermes Ball** | 51 | The swiftest god: best on the first turn. |
| Repeat Ball | **Mnemosyne Ball** | 66 | Memory: good on species caught before. Her pool is in Arkadia. |
| Luxury Ball | **Plutus Ball** | 50 | Wealth: the Pokémon grows friendly quickly. |
| Level Ball | **Arete Ball** | 46 | Excellence: better when your Pokémon's level is higher. |
| Lure Ball | **Glaucus Ball** | 55 | The fisherman made a sea god: good on Pokémon hooked by a Rod. |
| Moon Ball | **Selene Ball** | 50 | The moon: good on Moon Stone evolvers. |
| Friend Ball | **Philia Ball** | 48 | Friendship: the catch starts out fond of you. |
| Love Ball | **Eros Ball** | 41 | Desire: good on the opposite gender. |
| Fast Ball | **Atalanta Ball** | 60 | The fastest runner: good on fast Pokémon. |
| Heavy Ball | **Atlas Ball** | 45 | He bears the sky: good on heavy Pokémon. |
| Dream Ball | **Hypnos Ball** | 51 | Sleep: good on sleeping Pokémon. |
| Safari Ball | **Pan Ball** | 36 | The god of the wild. The Erymanthian Preserve's ball (the Safari Zone). |
| Sport Ball | **Agon Ball** | 41 | The contest. A cut system's ball (Bug-Catching Contest). |
| Park Ball | **Elysium Ball** | 54 | The blessed meadow. A transfer ball, never found in Aethos. |
| Beast Ball | **Typhon Ball** | 51 | The father of monsters: for beasts from beyond, poor on the rest. |
| Cherish Ball | **Charis Ball** | 50 | Grace and gift: the event ball. |
| Strange Ball | **Aion Ball** | 40 | Eternity: the ball that "wandered through all time". |

None of the names touches the Lazarus avoid-list (`research/LAZARUS.md`). The Premier Ball's throw-in line now reads "Take a Xenia Ball too, as a guest-gift." The Safari Zone is back as the Erymanthian Preserve (design/maps/ErymanthosPreserve.md): its strings now say Pan Balls, the keeper's bell, barley and a stone.

## The eight Laurels

Each laurel is named for its god's domain, in one plain English word, so a player can guess where it came from. Only the first is in the script; the other seven are proposals for the director.

| # | Temple | Hierophant | Laurel |
|---|---|---|---|
| 1 | Hestia, Akti Town | Ione, the Hearthkeeper | **Hearth Laurel** (SCRIPT beat 7) |
| 2 | Hermes, Emporion City | Kerykos, the Herald | Herald Laurel |
| 3 | Demeter, Eleusa Village | Chloe, the Mystagogue | Harvest Laurel |
| 4 | Dionysus, Thyrsa City | Thespis, the Masked Player | Mask Laurel |
| 5 | Artemis, Arkadia | Kallisto, the Moonlit Huntress | Moon Laurel |
| 6 | Hephaestus, Kaldera | Talos, the Bronzesmith | Forge Laurel |
| 7 | Aphrodite, Kythera Isle | Galatea, the Living Marble | Foam Laurel (she was born from the sea foam) |
| 8 | Apollo, Delphoi | Phemonoe, the Pythia | Sun Laurel |

## The ten Emblems

The Oikoumene's prizes, one per hall of the Periodos (`oikoumene/PERIODOS.md`). Each is named, like the Laurels, in one plain English word for its land's device, mostly taken from that land's own coins or seals. The longest, SILPHIUM EMBLEM, is 87 px, and "{PLAYER} received the Silphium Emblem from Kyrene!" wraps onto two lines of the field message box.

| # | Land | Hall | Champion | Emblem |
|---|---|---|---|---|
| 1 | Troad | The Skaian Gate | Prince Hektor | **Gate Emblem** |
| 2 | Lydia | The treasury of Croesus | King Croesus | **Lion Emblem** |
| 3 | Black Sea | Aietes's palace | Medea, Priestess of Hecate | **Fleece Emblem** |
| 4 | North | The round temple of Apollo | Abaris, Priest of Apollo | **Arrow Emblem** |
| 5 | Egypt | The precinct of Proteus | Pharaoh Proteus | **Scarab Emblem** |
| 6 | Aithiopia | Memnon's bath-court | King Memnon | **Dawn Emblem** |
| 7 | Libya | The hippodrome of Kyrene | Kyrene, the lion-wrestler | **Silphium Emblem** |
| 8 | Far West | The royal gallery of Tartessos | King Arganthonios | **Silver Emblem** |
| 9 | Western Sea | Milo's palaestra | Milo of Kroton | **Tripod Emblem** |
| 10 | Okeanos | The tower of Kronos | Rhadamanthys, Judge of the Blessed | **Rose Emblem** |

**Names that don't fit** (decision PG-39). A trainer name holds 10 characters. ARGANTHONIOS and RHADAMANTHYS are 12, so their battle names are ARGANTHON (54 px) and RHADAMANTH (60 px), the old English form; their dialogue keeps the full names. A trainer class label holds 12 characters, so the Oikoumene's longer class names show short labels such as HOPLITE, SORCERESS, ARCHER and MINER.

## What this pass left alone

- **Systems being cut** (contests, secret bases, the Battle Frontier, Pokéblocks, the PokéNav, Mystery Gift, the minigames, link play): their text keeps its Hoenn words until the code goes.
- **Hoenn map scripts and trainer dialogue** (`data/maps/*/scripts.inc`, `data/text/trainers.inc`): they go with the maps.
- **Item, move, species and trainer-class names**: other passes own them.
