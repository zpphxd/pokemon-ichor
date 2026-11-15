# The Periodos: the ten halls

- **Owner:** World and quest design. **Status:** written 2026-11-14 to carry out decision PG-33, which the user approved that day ("Yes, full gyms"). The open questions it raises are PG-34 to PG-41 in `OIKOUMENE.md` §13. Nothing here changes a game file.
- **What this is:** every one of the Periodos's ten champions (`OIKOUMENE.md` §5, §6) now keeps a full hall, with a puzzle, trainers, a prize and a scene. Egypt's champion is **Pharaoh Proteus of Memphis**, with Helen as his guest. Herakles at the Pillars stays the capstone, and he isn't a hall.
- **Where it fits:** `OIKOUMENE.md` owns the lands, their towns and the Periodos itself. This file owns the halls inside them. Its §4.1 to §4.10 follow the same order as OIKOUMENE's lands, so §4.5 is Egypt in both files.
- **Sources:** `OIKOUMENE.md`, `MAP_DESIGN.md` (§3 and §4), `SYSTEMS.md` (§1, §2 and §12, the Aethos temples' verbs), `ENGINE_API.md`, `BALANCE.md`, `TERMS.md`, `MUSIC.md`, `LABYRINTH.md`, `LABORS.md`, `UNDERWORLD.md`, `ODYSSEY.md`, `LEGENDS.md`, `research/LAZARUS.md`, and the ancient authors cited in each section.

---

## Contents

0. What a hall is
1. The prize: Emblems
2. Alethea's chart, and the end
3. The ten verbs, and why they're new
4. The halls
   - 4.1 Troad: Hektor at the Skaian Gate
   - 4.2 Lydia: Croesus's treasury
   - 4.3 The Black Sea: Medea in Aietes's palace
   - 4.4 Scythia and Hyperborea: Abaris's round temple
   - 4.5 Egypt: Pharaoh Proteus's precinct
   - 4.6 Aithiopia: Memnon's bath-court
   - 4.7 Libya: Kyrene's hippodrome
   - 4.8 The Far West: Arganthonios's gallery
   - 4.9 The Western Sea: Milo's palaestra
   - 4.10 Okeanos: Rhadamanthys at the tower of Kronos
5. The two Proteuses
6. Music
7. Budget: maps, trainers, flags and ROM
8. The Lazarus check

---

## 0. What a hall is

> *Herodotus went to see for himself. He asked the priests at Memphis, the Scythians at Olbia and the Libyans at the oases, and wrote down what each land said about itself.*

The Aethos temples are Greek: a god, a Hierophant and acolytes. The Oikoumene's lands aren't Greek, so their halls are each land's own seat of power, in its own idiom: a city gate, a king's treasury, a sorceress's palace, a pharaoh's precinct, a wrestling school. What they share is the shape `MAP_DESIGN.md` §3 and §4 ask of every trial.

- **One verb per hall,** from that land's myth or history. It is taught in the first room, tested in the middle and combined with a second mechanic at the end. The second mechanic is a relic the player already owns, an Aethos temple verb, or one more rule of the hall's own.
- **Three to five trainers,** from that land's classes (`OIKOUMENE.md` §6). At least one is optional, and the first is easy and in plain view.
- **A safety valve.** Someone in every hall explains the rule and, after a few failures, shows you. Failing never costs anything but the walk back to the start of that stage.
- **No time of day, no festival, no luck.**
- **A midpoint shortcut** opens once you've cleared the test stage, so a second attempt at the champion doesn't mean the whole hall again.
- **The champion waits at the climax of the architecture.** After the Emblem, the hall stays solved and its trainers stay beaten.
- **Every hall opens when you reach its land.** No hall needs another's Emblem.

**Levels.** Hall trainers sit at the top of their land's route-trainer band, just under the champion (`OIKOUMENE.md` §9, `BALANCE.md`). Champions keep their §6 levels. Hall trainers don't rematch; champions do, as §6 says.

---

## 1. The prize: Emblems

**The term is the Emblem** (decision PG-34). It's the Oikoumene's Laurel.

- **Where the word comes from.** The Greek *emblēma* is something set into something else: the inlaid picture at the centre of a mosaic floor, or a relief set into a silver cup. Alethea's chart has ten panels, and each champion's prize is the picture she sets into one.
- **It reads at once.** "Emblem" is an ordinary English word and needs no gloss, as "Laurel" doesn't.
- **What it looks like.** Each Emblem is a small black-figure roundel with its land's device, mostly taken from that land's own coins or seals. On the trainer card's Oikoumene page the ten sit round a disc, like the chart.
- **The avoid-list.** Nothing on Lazarus's list is close (`research/LAZARUS.md`). The word is kept apart from the Olympiad's Symbols (`POSTGAME.md` §3.1) and from xenia's *symbola* (`SYSTEMS.md` §10).
- **The halls** have no generic in-game label. Each keeps its own name: the Skaian Gate, the treasury of Croesus, the precinct of Proteus. In prose they are "halls".
- **The champions** fight under their own titles: PRINCE HEKTOR, KING CROESUS, PHARAOH PROTEUS. "Champion" stays a plain word in prose; the League's title is still the Archon (`TERMS.md`).

| # | Land | Hall | Champion, and title | Emblem | Device |
|---|---|---|---|---|---|
| 1 | Troad | The Skaian Gate | Hektor, PRINCE | Gate Emblem | The Skaian Gate |
| 2 | Lydia | The treasury of Croesus | Croesus, KING | Lion Emblem | The lion's head on Lydia's coins, the first ever struck (Herodotus 1.94) |
| 3 | Black Sea | Aietes's palace and Hecate's shrine | Medea, PRIESTESS | Fleece Emblem | The golden ram's fleece |
| 4 | North | The round temple of Apollo | Abaris, PRIEST | Arrow Emblem | Abaris's golden arrow |
| 5 | Egypt | The precinct of Proteus | Proteus, PHARAOH | Scarab Emblem | A scarab seal |
| 6 | Aithiopia | Memnon's bath-court | Memnon, KING | Dawn Emblem | The rising sun over Okeanos |
| 7 | Libya | The hippodrome of Kyrene | Kyrene, HUNTRESS | Silphium Emblem | The silphium of Kyrene's coins |
| 8 | Far West | The royal gallery of Tartessos | Arganthonios, KING | Silver Emblem | A silver ingot stamped with a ship |
| 9 | Western Sea | Milo's palaestra | Milo, ATHLETE | Tripod Emblem | The tripod of Kroton's coins |
| 10 | Okeanos | The tower of Kronos | Rhadamanthys, JUDGE | Rose Emblem | A rose from the Isles' meadows (Pindar, fr. 129) |

Labels are measured in `TERMS.md`.

**Each prize is three things:** the Emblem, a TM (TMs are reusable here; Balance numbers them), and one reward in the land's own flavor. The TMs are new to the game: none repeats a TM another doc already gives.

---

## 2. Alethea's chart, and the end

**The panels fill with Emblems.** This replaces `OIKOUMENE.md` §5's "beat the champion and visit the landmark".

- Alethea works from the chart table on the *Euploia* (`ODYSSEY.md` §2), so the Periodos and the Periplous end up on one table.
- When you win an Emblem, its panel on the region map fills at once. The next time you speak to Alethea she sets it in, and writes the panel's two lines: what's **TRUE** and what was only **TOLD**. Each hall's section below gives its pair.
- Landmarks you've visited add more notes, but they're never required.

```text
ALETHEA: An emblem. That's Troy, then. Hold still, I'm setting it in.

ALETHEA: TRUE: the wall is four men high. TOLD: Poseidon built it. Also true.
```

**The end.** With all ten Emblems and `LABORS.md`'s Kotinos, the Herakleion's priest at Gadeira sends you to the Pillars (`OIKOUMENE.md` §5). The script counts the Emblems with `Ichor_CountFlags` over their flags (§7).

```text
ALETHEA: Ten. Truthfully, I didn't think there were ten.
```

---

## 3. The ten verbs, and why they're new

Each hall's verb was checked against every puzzle the other docs already use: the eight Aethos temples (`SYSTEMS.md` §12), the Labyrinth's seven rings and the Choros (`LABYRINTH.md` §5–§6), the twelve Labors, the Katabasis, the Odyssey's islands, and `LEGENDS.md` §11's tally.

| Hall | The verb | Teach, test, combine | Closest existing puzzle, and how this differs | Engine |
|---|---|---|---|---|
| 4.1 Skaian Gate | **Step into the song and out again** | Two versions of the hall, the Wall and the Song; then a door opened from the Song's side, and Hestia's carried flame, which dies when you cross | The Labyrinth's dials and sun-and-moon gates move single walls. Here the whole hall has two versions you move between | Low |
| 4.2 Treasury | **Weigh** | Lifts that stop level only under the right load; sorting two golds on a hand-balance; balancing the lion | No other puzzle in the game weighs anything | Low |
| 4.3 Aietes's palace | **Make it young** | A ladle of brew turns a sleeping beast into its first stage for 12 steps; the bulls' fire lines, which only big beasts shield | Circe (ODYSSEY §6.5) changes the player's shape. Medea changes other creatures', for a while, and the timing is the puzzle | Low–Medium |
| 4.4 Round temple | **Fly the arrow** | Aim arrow-stones that fly you over chasms to a target; the swans, moving targets | Apollo's beams (SYSTEMS §12) are light; ODYSSEY's currents push you. Here you aim yourself | Low–Medium |
| 4.5 Precinct of Proteus | **Catch the right shape** | Ditto that take Homer's six shapes, one per step you take; hold one still; push one aside with the Girdle | Galatea's statues move when unwatched. Proteus's shapes cycle with your steps, and you plan by counting | Low–Medium |
| 4.6 Bath-court | **Slide** | Wet marble after the guest's bath; pools where nothing floats; gold blocks pushed as new stops | No hall or dungeon in the game uses sliding floors | Low; sliding blocks Low–Medium |
| 4.7 Hippodrome | **Drive** | A chariot that never stops or turns back; two strides between turns; other chariots and the left-hand rule at three posts | Labor 7's bull ride is free steering at sea. The chariot can't stop | Medium |
| 4.8 Royal gallery | **Heat, then quench or melt** | Crack an ore face with fire and vinegar, or melt it into a silver bridge; then choose which, three times over | Hestia's and Demeter's fires light things. Here fire changes rock, two ways, and you can't have both | Low |
| 4.9 Palaestra | **Leap** | Jump pits with jumping weights, one tile standing, two running; then carry Milo's calf across, which rules out running | The bull-leap is a timing test. This is a traversal verb you plan | Low–Medium |
| 4.10 Tower of Kronos | **Don't get taken** | A board game: stone dogs move as you move, and two on either side take you; then the trainers you beat become your pieces | Galatea's statues chase you. These follow fixed tracks, and a board rule decides | Low–Medium |

**Spread.** Four halls change how you move (the arrow, the slide, the chariot, the leap), two change other creatures (the brew, the shapes), one is a world of two layers, one is weighing, one is fire on rock and one is a board game.

**The combine stages** reach for different things. Troy adds Hestia's carried flame; Egypt and Aithiopia add the Girdle of Herakles, used two different ways; the Far West adds Hecate's Torch and the "don't run" rule; the Western Sea adds a carried calf. The other five add a rule of the hall's own: the lion's true weight, the bulls' fire, the moving swans, the other chariots, and trainers who join your side.

**Engine.** Every new piece is in `OIKOUMENE.md` §13's hall engine table. The chariot is the only Medium item, and it has a Low fallback. The set as a whole is decision PG-35.

---

## 4. The halls

### 4.1 Troad: Hektor at the Skaian Gate

> *The elders sat on the Skaian Gate, too old to fight, talking like cicadas in a tree* (*Iliad* 3.146–153). *There was a war, the Trojans say, but it was smaller and shorter than the songs* (`OIKOUMENE.md` §1).

**The hall.** The Skaian Gate, Ilion's western gate in the great sloping walls, and its tower. Two maps: **the Gate** (the barbican between the outer and inner gates, and the gate-house with its hearth; 30×20, four screens) and **the Tower** (the stair, the wall-walk and the top, where Priam watched the plain; 20×30, four screens). Each has a twin, **the Song**: the same place as the bards sing it, drawn in red-figure where the real one is black-figure. Four maps in all.

**The puzzle: the Song and the Wall.**
- **The rule.** Trojan bards sit on stools in the Wall. Sit by one and listen, and you're in the Song, on the same tile. STOP LISTENING, a Relic Ring entry that exists only in this hall, brings you back to the Wall on the same tile, unless the Wall has a wall there.
- **The two versions differ.** The Song is bigger than the truth: it has ten years of siege in it.
  - In the Song, the gates stand open for the routed army, as Priam ordered (*Iliad* 21.531–536). The tower is twice as tall and its stair is whole, but its landings are crowded with the song's heroes' shields.
  - In the Wall, the gates are barred, and the stair is broken: the war was a summer, and nobody ever needed the top.
- **A carried flame dies when you cross.** You can't carry a fire out of a song. (It's free: a carried flame lives in `VAR_TEMP`, which a map change clears; `SYSTEMS.md` §2.)
- **Teach: the gate-court.** The inner gate is barred. A bard by the outer gate says it plainly. Listen, walk through the Song's open gate, stop listening inside.
- **Test: the tower stair.** Four landings. The Wall's stair breaks off in two places and the Song's shields block two other landings, so neither version climbs the tower by itself. Bards sit only on some landings, so you have to plan where you'll be in the Song when you need it: going in needs a stool, coming out doesn't.
- **Combine: the beacon.** Besieged cities called for help with fire from their towers (*Iliad* 18.207–213). Light the beacon on the tower top with fire from the gate-house hearth, carried (20 steps). The stair takes too long and crosses into the Song, which puts the flame out. The Wall's short way is a ladder from the gate-house to the wall-walk, but its trapdoor is barred from above. So you climb the stair once without fire, unbar the trapdoor from the wall-walk, go down for the fire, and carry it up the ladder in time.
- **The safety valve.** The bards. Three failures and one sings you the way.
- **The shortcut.** That trapdoor and ladder, once unbarred.
- **After the Emblem.** The bards add a verse, and the Song's tower top now has Hektor standing on it, alive. They aren't sure it scans.

```text
BARD: Sit and listen. In the song, the gates are always open.

BARD: When you've had enough, stop listening. It's that easy.
```

```text
There's a wall there. A real one.
```

```text
The flame goes out. You can't carry a fire out of a song.
```

**Trainers** (Lv 72–74).

| Trainer | Class (label) | Where | Lv | Team | Line |
|---|---|---|---|---|---|
| Agenor | Trojan Hoplite (HOPLITE) | The gate-house door, Wall; mandatory, easy | 72 | Medicham, Doublade, Bisharp | "In the song I fight Achilles. Here I mind the gate." |
| Kebriones, Hektor's charioteer (*Iliad* 16.727–743) | Charioteer | The second landing, Song only; mandatory | 73 | Rapidash, Mudsdale, Braviary | "I'm Hektor's driver. In this verse I fall off. Mind the wheel." |
| Paris | Shepherd of Ida (SHEPHERD) | A side bastion, Wall; optional, facing away | 73 | Dubwool, Gogoat, Beautifly | "I did take her. Proteus took her off me in Egypt. And the treasure." (Herodotus 2.115) |
| Polydamas, who told Hektor to stay inside the walls (*Iliad* 18.249–283) | Trojan Hoplite | The tower-top door, Wall; mandatory | 74 | Primeape, Falinks, Bisharp | "I told him to stay behind the walls. He listens, now." |

**The champion: Prince Hektor** (Lv 74–76), on the tower top.

| Species | Lv | Note |
|---|---|---|
| Falinks | 74 | A phalanx |
| Rapidash | 74 | Troy of the fine horses |
| Conkeldurr | 75 | Mason of the walls |
| Lucario | 75 | |
| Kingambit | 75 | |
| **Aegislash** | **76** | **Ace.** The shield of Troy |

```text
HEKTOR: There's a song where I'm dragged round these walls.

HEKTOR: My sister saw it every night. Last month she stopped.

HEKTOR: Let's see what I do with that.
```
After the battle:
```text
HEKTOR: That's not in any song. Good.

HEKTOR: Tell your friend with the chart: the wall's this high. Not higher.
```

**The prize.** The **Gate Emblem**; **TM Body Press**, the defender's move; and a **Rocky Helmet**, the helmet whose crest frightened his son (*Iliad* 6.466–473).
```text
HEKTOR: My son cried at this helmet. Take it before he sees it again.
```
Alethea's panel: "TRUE: the wall is four men high. TOLD: Poseidon built it. Also true."

`LEGENDS.md` §3.10 has Kleon spar with Hektor on this tower. It happens here, after the Emblem.

**Look and sound.** The `troas` tileset, plus the gate-tower, bard stools, the washing troughs at the two springs (*Iliad* 22.147–156), the beacon and the broken stair. The Song is the same tiles with a second set of palettes (red-figure: figures in clay on black), which costs 224 bytes because two tilesets can share one set of tile graphics. The Wall plays the hall theme (§6); the Song plays the Troad's own *The Plain of Troy*, the march that never arrives.

---

### 4.2 Lydia: Croesus's treasury

> *Croesus sent Delphi a hundred and seventeen half-bricks of gold: four of refined gold, two and a half talents each, the rest of white gold, two talents each, and a lion of refined gold. When the temple burned, the lion fell, and three and a half talents of it melted away* (Herodotus 1.50).

**The hall.** The treasury cut into Sardis's acropolis rock below the palace: lamps, electrum and Lydian purple, lion reliefs. Two maps: **the Weighing Room and the Strongroom** (45×20, six screens) and **the Lion Vault**, with Croesus's counting-room above it (30×20, four screens).

**The puzzle: the Weighing.**
- **Two golds.** White gold (electrum) weighs 2 talents an ingot and refined gold 2½. In the lamplight they look the same.
- **Alcmaeon's boots.** Croesus once let the Athenian Alcmaeon take as much gold as he could carry, and Alcmaeon came in the widest boots he could find (Herodotus 6.125). The treasurer lends you a pair: they hold three ingots. Pick ingots up and put them down at their plinths.
- **The lifts.** A lift is a platform hung against a counterweight. Step on with your load. If it matches, the lift stops level with the gallery and you can step off. Too light and it rises to the ceiling; too heavy and it sinks into the pit. Either way you step back down and try again.
- **The hand-balance.** A small table balance compares two ingots.
- **Teach: the Weighing Room.** A 2-talent lift, and a shelf with one ingot of each gold.
- **Test: the Strongroom.** Nine ingots, two of them refined, and two lifts: 4½ talents (one of each) and 6 (three white). Sort them on the hand-balance.
- **Combine: the Lion Vault.** Croesus's lion is home from Delphi and sits on one pan of the great balance. Its plinth says ten talents, as the song does. It weighs six and a half, what the fire left. Carry two white and one refined onto the other pan, and the vault stair levels. The way in passes a 4-talent lift, so you can't arrive with the whole load: bring the two white through, then find the refined ingot among the vault's own on its hand-balance.
- **The safety valve.** The treasurer, who will weigh things for you if you ask twice.
- **The shortcut.** A stair from the 6-talent gallery back to the Weighing Room.
- **After the Emblem.** The lifts stay level, and the treasurer weighs whatever you bring him.

```text
TREASURER: Two kinds of gold, and down here they look the same. Weigh them.

TREASURER: Alcmaeon's boots. They hold three. He filled his hair too. Don't.
```
```text
TEN TALENTS OF REFINED GOLD, says the plinth. The lion's been in a fire since.
```

**Trainers** (Lv 74–76).

| Trainer | Class | Where | Lv | Team | Line |
|---|---|---|---|---|---|
| Manes | Panner | The Strongroom door; mandatory, easy | 74 | Floatzel, Bronzong, Mawile | "I carry the gold dust up from the river. Nobody weighs me on the way out." |
| Tylon | Panner | By the hand-balance; optional | 75 | Golduck, Forretress, Klefki | "The lion says ten talents. The lion's been in a fire. Think about it." |
| Sandanis, who told Croesus not to fight men in leather trousers (Herodotus 1.71) | Lydian Musician (MUSICIAN) | The 6-talent gallery; mandatory | 75 | Exploud, Oricorio, Kricketune | "Why fight someone who has nothing? Win, and you win nothing." |
| Hyagnis, father of Marsyas | Phrygian Piper (PIPER) | The counting-room stair; mandatory | 76 | Toxtricity, Clefable, Venomoth | "My son Marsyas played better than Apollo. Don't tell anyone I said so." |

**The champion: King Croesus** (Lv 75–77), in his counting-room.

| Species | Lv | Note |
|---|---|---|
| Klefki | 75 | The treasury keys |
| Torkoal | 75 | The tortoise Croesus boiled in a bronze pot to test the oracles (Herodotus 1.47–48) |
| Aggron | 76 | |
| Luxray | 76 | *Elektron* is the Greek for both amber and white gold: an electrum lion |
| Copperajah | 76 | |
| **Gholdengo** | **77** | **Ace.** Sardis's mint makes its coins |

```text
CROESUS: The oracle said a great empire would fall. I never asked whose.

CROESUS: I'm asking you.
```
After the battle:
```text
CROESUS: Solon said count no man happy till he's dead. I'm counting.

CROESUS: I'm fairly happy.
```

**The prize.** The **Lion Emblem**; **TM Flash Cannon**; and a **Gold Bottle Cap**.
```text
CROESUS: Alcmaeon took all he could carry. You took exactly enough. Here.
```
Alethea's panel: "TRUE: the lion weighs six and a half talents. TOLD: ten."

**Look and sound.** The `lydia` tileset and the Lydian house interior set, plus the lifts and counterweights, the hand-balance, ingot plinths, the great balance and the gold lion. The hall theme in its Lydian voicing.

---

### 4.3 The Black Sea: Medea in Aietes's palace

> *She stirred the brew with a long-dead branch of olive. It turned green, then put out leaves, then hung with olives. Where the froth spilled, the ground flowered* (Ovid, *Metamorphoses* 7.279–284, when Medea made old Aeson young).

**The hall.** Aietes's bronze palace at Aia: the court of Hephaestus's four fountains, of milk, wine, oil, and water that runs warm when the Pleiades set and icy when they rise (*Argonautica* 3.215–231); the bronze halls round it, where the heads of Hephaestus's bulls jut from the walls and breathe fire down the corridors; and below, Hecate's shrine, where Medea keeps her cauldron. Two maps: **the bronze halls** (40×30, eight screens) and **Hecate's stair and shrine** (20×15, two screens).

**The puzzle: Medea's Cauldron.**
- **The sleepers.** Aietes's beasts sleep across the doorways: a Dubwool of the golden ram's kin, a Mudsdale, a Snorlax, a Copperajah.
- **The brew.** A ladle of Medea's brew makes one young for 12 steps. It's a Wooloo, a Mudbray, a Munchlax or a Cufant, small enough to trot aside into its alcove. When the brew wears off it grows back and trots home. If you're in the doorway then, it nudges you back the way you came.
- **The ladle** holds three doses. Refill it at the cauldron, or from Medea's maid by the milk fountain.
- **The bulls.** A bull's head breathes fire down its corridor. A big beast standing in the line takes the fire without noticing; a young one can't. If the fire reaches you, you're back at the stage's door, smoking slightly.
- **Teach: the fountain court.** One Dubwool across the door to the halls.
- **Test: the bronze halls.** Two sleepers in doorways ten steps apart, three doses, and a bull's fire line across the corridor between them, shielded by the Copperajah standing in it. Shrink the sleepers, not the shield.
- **Combine: Hecate's stair.** The last doorway's sleeper is a Copperajah that also shields the landing beyond it. Shrink it and the door opens, but so does the fire line. Slip through, wait in the niche until it grows back, then cross under its shield.
- **The safety valve.** Chalkiope, Medea's sister, by the cauldron (*Argonautica* 3).
- **The shortcut.** A side door from the stair back into the fountain court.
- **After the Emblem.** The beasts sleep on, and Medea's maids keep the doorways clear.

```text
CHALKIOPE: My sister's brew makes old things young. For a little while.

CHALKIOPE: Twelve steps, then they grow back. Don't stand in the doorway.
```
```text
A ladle of the brew. The Dubwool is a Wooloo again, and indignant about it.
```
```text
The bronze bull breathes. You're back at the door, smoking slightly.
```

**Trainers** (Lv 75–77).

| Trainer | Class | Where | Lv | Team | Line |
|---|---|---|---|---|---|
| Akmon, "anvil", one of the first smiths | Chalybes Smith (SMITH) | The first hall; mandatory, easy | 75 | Magneton, Torkoal, Klinklang | "The bulls breathe fire down these halls. The big beasts don't feel it." |
| Kytaia, named for Medea's home town | Colchian Sorceress (SORCERESS) | A side hall; optional | 76 | Ninetales, Salazzle, Mismagius | "She made an old ram into a lamb once. It's never forgiven her." |
| Kelmis, "the smelter" | Chalybes Smith | The stair down; mandatory | 76 | Coalossal, Aggron, Tinkaton | "We smelted iron before anyone. Nobody sings about that." |
| Phasia, named for the river | Colchian Sorceress | The shrine door; mandatory | 77 | Galarian Slowking, Gengar, Drampa | "The princess is downstairs. She's been expecting you. She hates that." |

**The champion: Medea, Priestess of Hecate** (Lv 76–78), at the cauldron.

| Species | Lv | Note |
|---|---|---|
| Toxicroak | 76 | |
| Rotom (Heat) | 76 | From the palace workshop (`OIKOUMENE.md` §4.3) |
| Ampharos | 77 | The ram's kin |
| Dragalge | 77 | |
| Hatterene | 77 | |
| **Hydreigon** | **78** | **Ace.** The serpent that never sleeps |

```text
MEDEA: My father keeps a fleece, a dragon and a daughter. Two of us are bored.
```
After the battle:
```text
MEDEA: Nobody's sung this yet. I'd like to keep it that way a while.
```

**The prize.** The **Fleece Emblem**; **TM Trick Room** (old to young, last to first: it's the same trick); and a **Covert Cloak**, the charm that kept Jason safe from the bulls for a day (*Argonautica* 3.1042–1051).
```text
MEDEA: My charm against the bulls, sewn into a cloak. Jason never asked.
```
Alethea's panel: "TRUE: four fountains. TOLD: the princess is dangerous. Pending."

**Look and sound.** The `pontos` tileset and the Colchian bronze hall interior set, plus the four fountains, the bulls' heads and their fire lines, the alcoves, the cauldron and Hecate's three-faced pillar. The young and grown-up beasts are follower sprites, which exist for every species. The hall theme in its Black Sea voicing.

---

### 4.4 Scythia and Hyperborea: Abaris's round temple

> *I say nothing of the story of Abaris, said to be a Hyperborean, who carried the arrow round the whole earth, eating nothing* (Herodotus 4.36). *Later writers said he rode it over rivers and seas and places no one could cross* (Iamblichus, *Life of Pythagoras* 91, 136).

**The hall.** The round temple of Apollo on the Hyperborean headland. Diodorus calls it spherical, and says most of the island's people are kitharists who play in it (2.47). A ring of standing stones (the Stonjourner of the meadow, `COVERAGE.md`), a ring-ditch, chasms dropping to the sea where the thousand-year-old once leapt, and at the centre a pool where Apollo's swans circle. Two maps: **the outer rings** (45×30, nine screens) and **the swan pool and temple** (20×20, three screens).

**The puzzle: the Golden Arrow.**
- **Arrow-stones.** A golden arrow lies on a stone. Press A to turn it a quarter. Step on to ride it: it flies straight over chasms, water and walls until it meets a target (a laurel post or a gilded swan), and sets you down in front of it.
- **No target, no flight.** An arrow with nothing in line won't fly.
- **Teach: the first ring.** One stone, already aimed at a post across the ditch.
- **Test: the stone circle.** Turf islets between chasms. Turn the stones to chain flights; some posts are dead ends on islets with a stone home.
- **Combine: the swan pool.** The gilded swans circle the pool on eight posts round its rim, one place every time an arrow flies, as the swans flew round Delos when Apollo was born (Callimachus, *Hymn to Delos* 249–254). Aim at where the swan will be.
- **The safety valve.** A kitharist on the temple steps.
- **The shortcut.** A stone at the circle's gate that flies straight back to the entrance.
- **After the Emblem.** The stones stay aimed, and the swans keep circling for the view.

```text
The arrow won't fly. There's nothing in front of it to hit.
```

**Trainers** (Lv 79–81).

| Trainer | Class | Where | Lv | Team | Line |
|---|---|---|---|---|---|
| Opis, one of the first maidens to carry offerings to Delos (Herodotus 4.35) | Hyperborean Pilgrim (PILGRIM) | The first ring; mandatory, easy | 79 | Whimsicott, Chimecho, Eiscue | "We carried straw to Delos once. Nobody remembers why. We still do it." |
| Arge, Opis's companion | Hyperborean Pilgrim | An islet; optional | 80 | Glaceon, Jumpluff, Walrein | "The swans go round seven times. Count them, or don't. They don't." |
| Kolaxais, whose family took the gold that fell from the sky (Herodotus 4.5–7) | Scythian Archer (ARCHER) | The circle's gate; mandatory | 80 | Stoutland, Diggersby, Cyclizar | "A gold plough fell out of the sky on my family once. Watch the sky." |
| Laodike, who carried the offerings later (Herodotus 4.33) | Hyperborean Pilgrim | The temple door; mandatory | 81 | Cetitan, Vanilluxe, Sylveon | "Abaris rode that arrow round the world and never ate. He's eating now." |

**The champion: Abaris, Priest of Apollo** (Lv 80–82), at the temple's altar.

| Species | Lv | Note |
|---|---|---|
| Frosmoth | 80 | |
| Swanna | 80 | Apollo's swans |
| Alolan Ninetales | 81 | Replaces Jynx, which keeps its wild home |
| Stonjourner | 81 | The walking round temple |
| Avalugg | 81 | |
| **Baxcalibur** | **82** | **Ace** |

```text
ABARIS: We live a thousand years. Lived. Now? We'll see.

ABARIS: We've never said that before.
```
After the battle:
```text
ABARIS: Round the world on an arrow, and I never got lost. You'll be fine.
```

**The prize.** The **Arrow Emblem**; **TM Dazzling Gleam**, Apollo's light; and a **Moon Stone**. Diodorus says the moon looks very near from the island (2.47.5).
```text
ABARIS: The moon's very close here. Bits come off. Take this one.
```
Alethea's panel: "TRUE: the moon is very close. TOLD: they live a thousand years."

**Look and sound.** The `hyperborea` tileset (the meadow), plus arrow-stones in four facings, laurel posts, gilded swans, the ring of stones and chasm edges. The hall theme in its Hyperborean voicing, on Apollo's lyre.

---

### 4.5 Egypt: Pharaoh Proteus's precinct

> *In Memphis there is a precinct of Proteus, south of the temple of Hephaestus. Phoenicians of Tyre live round it, and the place is called the Tyrians' Camp. Inside is a temple of Aphrodite the Stranger. I think it is Helen's* (Herodotus 2.112, abridged). *Homer knew this story, Herodotus adds, but chose the other one because it suited an epic better* (2.116).

**Egypt's champion is now Pharaoh Proteus,** the king who held Helen through the whole Trojan War (Herodotus 2.112–120). **Helen stays, as his guest,** and battles you if you like (decision PG-36). §5 reconciles him with Homer's Old Man of the Sea.

**The hall.** The precinct of Proteus: a pylon gate with a frieze, a hypostyle court of papyrus columns, the Tyrians' Camp of Phoenician tents round the precinct wall, the pharaoh's throne under a canopy in the inner court, and at the back the temple of the Stranger Aphrodite. Three maps: **the pylon and hypostyle court** (30×20, four screens), **the Tyrians' Camp and the inner court** (30×20, four screens, open-air) and **the temple of the Stranger** (15×12, one screen).

**The puzzle: the Shapes.**
- **The shapes.** Proteus likes Homer's version of himself, so he had his Ditto trained to play it. Each takes Homer's six shapes in order, one per step you take: lion, serpent, leopard, boar, water, tree (*Odyssey* 4.456–458). The frieze over the pylon shows the order.
- **Which let you by.** Step over a Ditto while it's a **serpent**, lying flat. Walk through it while it's **water**. The other four block.
- **Hold fast.** Press A beside one and grip it: it stops changing. You can hold one at a time, and gripping another lets the first go.
- **It always works out.** Serpent and water sit three apart in the cycle, so pacing back and forth (two steps at a time) always brings one of them round, whichever side you stand on.
- **Teach: the pylon gate.** One Ditto in the gateway.
- **Test: the hypostyle court.** Three Ditto in a row of doorways, and every step changes all of them. A side aisle reaches the far one: hold it as water from there, then come back and pace the near ones round.
- **Combine: the Tyrians' Camp.** Add the Girdle of Herakles: a Ditto held as a **boar** is heavy enough to push, so you can shove it out of a doorway and leave it there, held. But you only have one grip, and every push is a step for the others.
- **The safety valve.** Eidothea, Proteus's daughter, who once told Menelaus how to catch the Old Man of the Sea (*Odyssey* 4.363–445).
- **The shortcut.** A side gate from the Camp back to the pylon.
- **After the Emblem.** The Ditto stop performing and loll about the court as Ditto.

```text
EIDOTHEA: Every step you take, my father's shapes change.

EIDOTHEA: Lion, serpent, leopard, boar, water, tree. Then round again.

EIDOTHEA: Step over the serpent. Walk through the water.

EIDOTHEA: Or grab one and hold on. Homer says that's the way. He's half right.
```

**Trainers** (Lv 72–74).

| Trainer | Class | Where | Lv | Team | Line |
|---|---|---|---|---|---|
| Thonis, warden of the Canopic mouth, who stopped Paris's ship (Herodotus 2.113–115) | Nile Boatman (BOATMAN) | Inside the pylon; mandatory, easy | 72 | Whiscash, Octillery, Eelektross | "I stopped Paris's ship at the Canopic mouth. Nobody sings about me." |
| Imouthes, the Greek name of Imhotep | Scribe of Thoth (SCRIBE) | A side aisle; optional | 73 | Claydol, Wobbuffet, Gothitelle | "I write things down. It's how the truth gets old enough to believe." |
| Manetho, the priest who wrote Egypt's history in Greek, partly to correct Herodotus | Priest of the Sun (SUN PRIEST) | The court's far door; mandatory | 73 | Camerupt, Meowstic, Houndoom | "Herodotus got half of Egypt right. I'm writing the other half." |
| Ithobal | Phoenician Trader (TRADER) | The inner court's gate; mandatory | 74 | Krookodile, Perrserker, Copperajah | "We're the Tyrians' Camp. We've been camping here a very long time." |

**The champion: Pharaoh Proteus** (Lv 74–76), on his throne in the inner court.

| Species | Lv | Note |
|---|---|---|
| Sigilyph | 74 | |
| Cofagrigus | 74 | |
| Hippowdon | 75 | |
| Mimikyu | 75 | A borrowed shape |
| Zoroark | 75 | Illusion: it comes out looking like his ace. A phantom of a shape-shifter |
| **Ditto** | **76** | **Ace.** Imposter and a Choice Scarf: his last shape is yours |

```text
PROTEUS: Homer says I turn into a lion if you grab me. I don't.

PROTEUS: But I liked it. So I had the shapes trained.
```
After the battle:
```text
PROTEUS: Menelaus held on to my seal-herd for an hour.

PROTEUS: He went home and called him a god.
```
If you've met the Old Man of the Sea (theoxenia E13, `SYSTEMS.md` §10):
```text
PROTEUS: You've met the other one? Out past the Bear? …Does he look like me?
```

**The prize.** The **Scarab Emblem**; **TM Substitute**, a copy that takes the blows, which the Trojans fought ten years for; and **a Ditto** with Imposter, for the egg-ovens at Naukratis.
```text
PROTEUS: Take one of the shapes. It'll be anything you like. Mostly you.
```
Alethea's panel: "TRUE: Proteus is a man. TOLD: he turns into a lion if you grab him."

**Helen, in the temple of the Stranger.** After the Scarab Emblem, Helen of Sparta will battle you in her temple: Herodotus guessed the "Stranger Aphrodite" was Helen, and here the stranger is her. `LEGENDS.md` §3.10's Truth-Stone is in this temple too.

| Species | Lv | Note |
|---|---|---|
| Altaria | 74 | The cloud the phantom was made of (Euripides, *Helen* 31–36) |
| Espeon | 75 | |
| Sylveon | 75 | |
| Gardevoir | 75 | |
| **Milotic** | **76** | **Ace** |

```text
HELEN: A thousand ships sailed for me. I wasn't there. They fought for a story.

HELEN: Everyone fought over me. Nobody's ever fought me. Go on.
```
After the battle, and her gift, a **Mirror Herb**:
```text
HELEN: Tell Menelaus I'll come. Eventually. Nobody knows when, now.

HELEN: Everyone wanted a copy of me. Here's one that's useful.
```
Menelaus is on the Isles of the Blessed, waiting for her (`OIKOUMENE.md` §4.10).

**Look and sound.** The `kemet` tileset and the Egyptian mud-brick interior set, plus the pylon and its frieze, papyrus columns, the Tyrians' tents and the Stranger's shrine. The six shapes are follower sprites: Pyroar for the lion, Seviper for the serpent, Liepard, Mamoswine for the boar, a puddle object for the water, and a palm for the tree. The hall theme in its Egyptian voicing; the temple of the Stranger plays *The Black Land*.

---

### 4.6 Aithiopia: Memnon's bath-court

> *They took the spies to a spring. Washing in it made the skin sleek, as if with oil, and it smelt of violets. The water was so light that nothing would float on it, not even wood* (Herodotus 3.23, abridged).

**The hall.** Memnon's palace at Meroë is built round the violet spring. Its bath-courts are black marble, kept wet by the spring's channels, with palm-fibre mats, pools of violet water, blocks of gold (gold is common here; bronze is the treasure, 3.23) and pillars of crystal like the ones the Ethiopians keep their dead in (3.24). Memnon's throne stands on a dais at the east end, facing the dawn. Two maps: **the bath-courts** (45×20, six screens) and **the dawn hall** (20×15, two screens).

**The puzzle: the Bath.**
- **The bath.** A Homeric host bathes a guest and rubs them with oil before anything else (*Odyssey* 3.464–468, 4.48–50). Memnon's servants bathe you in the violet spring, and now you're sleek as oil. On the wet marble you slide until something stops you: a mat, a wall, a pillar, a person.
- **Nothing floats.** Slide into a violet pool and you sink. The servants fish you out at the court's edge. Poseidon's Conch is no use on it.
- **The crystal pillars** stop you but don't block your view, so you can read a whole court at a glance.
- **Teach: the first court.** One long line to a mat.
- **Test: courts two and three.** Slide routes that cross a court mat by mat, with pools to miss.
- **Combine: the dawn hall.** Add the Girdle: push a gold block onto the marble and it slides too, until it hits something. Where you shove it from decides where it stops, and where it stops is your next mat.
- **The safety valve.** The bath-servant, who will lay a mat for you after three dunkings.
- **The shortcut.** A dry path of mats along the colonnade, laid once you clear the third court.
- **After the Emblem.** The mat path runs through every court.

```text
BATH-SERVANT: A guest is bathed first. Then the floors. Mind the floors.
```
```text
You're sleek as oil. On the wet marble you'll slide till something stops you.
```
```text
Nothing floats on the violet water. Not wood. Not you. The servants fish you out.
```

**Trainers** (Lv 77–79).

| Trainer | Class | Where | Lv | Team | Line |
|---|---|---|---|---|---|
| Amani | Ethiopian Archer (ARCHER) | The first court's mat; mandatory, easy | 77 | Electivire, Pyroar, Farigiraf | "Bronze is the treasure here. Gold we make chains of." |
| Oinoe, the Pygmy queen who was turned into a crane (Ovid, *Metamorphoses* 6.90–92; Antoninus Liberalis 16) | Pygmy Warrior (PYGMY) | A mat island; optional | 78 | Passimian, Pangoro, Bombirdier | "I was a crane once. Long story. I still don't like them." |
| Nastasen | Ethiopian Archer | The colonnade; mandatory | 78 | Toucannon, Electrode, Kangaskhan | "Our king draws a bow no Persian can bend. Want to try? Later." (Herodotus 3.21) |
| Ergamenes, named for the king who refused when the priests told him to die (Diodorus 3.6) | Ethiopian Archer | The dais stair; mandatory | 79 | Xatu, Arcanine, Slaking | "The priests used to tell our kings when to die. One king said no." |

**The champion: King Memnon, son of the Dawn** (Lv 78–80), on the dais.

| Species | Lv | Note |
|---|---|---|
| Zebstrika | 78 | |
| Solrock | 78 | |
| Talonflame | 79 | In the song, birds rose from his pyre (Ovid, *Metamorphoses* 13.600–619) |
| Rhyperior | 79 | |
| Magmortar | 79 | His armor was Hephaestus's work. Replaces Pyroar, which Kyrene and Herakles already field |
| **Volcarona** | **80** | **Ace.** The sun |

```text
MEMNON: There's a song where I die at Troy. I've never been to Troy.

MEMNON: Is it nice?
```
After the battle (Ovid has the dew be Dawn's tears for him, *Metamorphoses* 13.621–622):
```text
MEMNON: In that song my mother wept every morning. The dew, they said.

MEMNON: Now she just waters the garden.
```

**The prize.** The **Dawn Emblem**; **TM Heat Wave**; and an **Assault Vest**.
```text
MEMNON: Hephaestus made my armor. This was the lining.
```
Alethea's panel: "TRUE: nothing floats on the violet spring. TOLD: Memnon died at Troy."

**Look and sound.** The `aithiopia` tileset (the courts are open to the sky), plus wet black marble, palm mats, violet pools, gold blocks, crystal pillars and the dawn dais. The hall theme in its Aithiopian voicing.

---

### 4.7 Libya: Kyrene's hippodrome

> *Apollo snatched Kyrene from the windy glens of Pelion and carried her off in his golden chariot* (Pindar, *Pythian* 9.5–8). *The Greeks learned to yoke four horses from the Libyans* (Herodotus 4.189).

**The hall.** The hippodrome below Apollo's sanctuary at Kyrene, whose kings' chariots won at Delphi (Pindar, *Pythian* 4 and 5): the starting gates, the long sand track, the turning posts, the stables, the stands where her lions doze, and Kyrene's box above the finish. Two maps: **the practice ground** (30×20, four screens) and **the hippodrome** (60×20, eight screens).

**The puzzle: the Golden Chariot.**
- **The chariot.** Kyrene lends you Apollo's chariot. On the track the team runs by itself: you steer left or right, but you can't stop or turn back.
- **Two strides.** The team needs two tiles straight between turns, so there's no zigzagging.
- **Post on your left.** Round each post with it on your left, as Nestor told his son (*Iliad* 23.306–348). Round one the wrong way and the judges flag you back to the gates.
- **Spills.** Hit a rail, a post or the stands, and you're back at the gates with no harm done.
- **Stopping.** The chariot halts at the stables between laps and at the finish. You get down there, and that's where the trainers wait.
- **Teach: the practice ground.** A straight, one post, a straight to the finish.
- **Test: the first lap.** A track of posts and gaps where the two-stride rule picks the line.
- **Combine: the second lap.** Add other chariots: the hall's charioteers drive their own laps on fixed lines, and their teams cross yours, with three posts to round on the left. At Delphi forty chariots fell and Kyrene's driver brought his home whole (Pindar, *Pythian* 5.49–51).
- **The safety valve.** Kyrene's groom at the gates, who will drive a lap with you beside him.
- **The shortcut.** A stair from the middle stables up to the stands, past the first lap.
- **After the Emblem.** The chariot waits at the gates for practice laps, and the charioteer of Kyrene (`OIKOUMENE.md` §4.7) races your best time.

```text
KYRENE: Apollo carried me here in that chariot. I kept the chariot.

KYRENE: It won't stop or turn back. Two strides between turns.

KYRENE: Keep the post on your left.
```
```text
The team bolts into the rail. You pick yourself up at the gates.
```
```text
The judges wave a flag. Post on your LEFT. Back to the gates.
```

**Trainers** (Lv 74–76).

| Trainer | Class | Where | Lv | Team | Line |
|---|---|---|---|---|---|
| Battos, of the founder's line (Herodotus 4.155) | Charioteer | The practice ground's stable; mandatory, easy | 74 | Dodrio, Zangoose, Camerupt | "My ancestor stammered till he saw a lion. It's a family cure." |
| Adikran, a Libyan king who fought Kyrene once (Herodotus 4.159) | Garamantian Driver (DRIVER) | A side stable; optional | 75 | Sandslash, Garganacl, Krookodile | "The Greeks learned four horses from us. They still drive like Greeks." |
| Garamas | Garamantian Driver | The middle stables; mandatory | 75 | Sandaconda, Gliscor, Drapion | "We drive four horses across the desert. Sand's softer than posts." |
| Karrhotos, the driver who brought the king's chariot home whole (Pindar, *Pythian* 5) | Charioteer | The last stable; mandatory | 76 | Rapidash, Arcanine, Darmanitan | "Forty chariots fell at Delphi. I brought mine home whole. Like this." |

**The champion: Kyrene, the lion-wrestler** (Lv 75–77), in her box above the finish.

| Species | Lv | Note |
|---|---|---|
| Arbok | 75 | The Psylli's snakes |
| Hariyama | 75 | She wrestled without weapons (Pindar, *Pythian* 9.26–28) |
| Flygon | 76 | |
| Espathra | 76 | Libya's ostriches (Herodotus 4.192). Replaces Delphox: Lazarus's starter lines are wild-only (PG-5) |
| Garchomp | 76 | |
| **Pyroar** | **77** | **Ace.** The lion |

```text
KYRENE: Apollo saw me wrestle a lion and fell in love. Most people just clap.
```
After the battle:
```text
KYRENE: Fair race. The lion's sulking. He'll get over it.
```

**The prize.** The **Silphium Emblem**; **TM Flame Charge** (the sun's chariot gets faster as it burns); and two **Revival Herbs**, the last of the king's silphium, which was worth its weight in silver (Pliny, *Natural History* 19.38–40).
```text
KYRENE: The last of the silphium. It cures anything, they say. Except sheep.
```
Alethea's panel: "TRUE: the Libyans taught us four horses. TOLD: the lion started it."

**Look and sound.** The `libye` tileset, plus the sand track and rails, turning posts, starting gates, stables, stands and lion beds, and a chariot overworld sprite in four facings (one new sprite, like the *Euploia*'s). The hall theme in its Libyan voicing.

---

### 4.8 The Far West: Arganthonios's gallery

> *They break the rock with fire and vinegar* (Pliny, *Natural History* 33.71, of the mines of Spain). *Shepherds once set the forests alight, and the silver melted out of the earth and ran in streams* (Diodorus 5.35).

**The hall.** Under the silver palace of Tartessos runs the royal gallery of the mine. Arganthonios keeps a second throne at its end, because he likes to hear the mine at work. The galleries are silver-veined rock, with braziers on bronze stands, jars of vinegar, channels cut in the floor and moulds over the pits. Two maps: **the gallery** (60×20, eight screens) and **the silver throne room** (15×15, two screens).

**The puzzle: Fire and Vinegar.**
- **Heat.** Every ore face has two braziers before it. Light one with Hecate's Torch, and the face glows hot for 15 steps.
- **Quench** a hot face with vinegar and it cracks open: the face is a passage now.
- **Or melt it.** Light the other brazier while it's hot, and the vein runs out down its channel to the mould at the end, where it sets as a silver plank across the pit.
- **One or the other.** A face can be cracked or melted, not both.
- **The vinegar** is in jars by the big storage pithoi. Carry one at a time, and don't run with it or it spills (`SYSTEMS.md` §10's "don't run" rule).
- **Teach.** One face: heat it, fetch the vinegar, quench it, walk through.
- **Test.** One face and one pit: melt it for a bridge.
- **Combine.** Three faces, two pits and one wall. Choose which to crack and which to melt, and get the vinegar there inside 15 steps, walking.
- **The safety valve.** The overseer by the pithoi. Faces cool and set again when you leave the gallery, so nothing can be spoiled for good.
- **The shortcut.** The mine lift from the middle gallery up to the palace.
- **After the Emblem.** The cracked and melted faces stay as you left them.

```text
The face glows red. It'll stay hot for fifteen steps.
```
```text
The vinegar hisses. The rock cracks open.
```
```text
The vein melts. Silver runs down the channel and sets in the mould.
```

**Trainers** (Lv 79–81).

| Trainer | Class | Where | Lv | Team | Line |
|---|---|---|---|---|---|
| Argyris | Silver Miner (MINER), a new class (`OIKOUMENE.md` §6) | The gallery mouth; mandatory, easy | 79 | Ferrothorn, Crustle, Golurk | "Fire for a door. Fire twice for a bridge. Vinegar if you want the door." |
| Hanno, who sailed past the Pillars and down the coast of Libya (the *Periplus of Hanno*) | Phoenician Trader | By the pithoi; optional | 80 | Barbaracle, Lycanroc, Oranguru | "I sailed past the Pillars and down Libya. Saw hairy people. Wrote it down." |
| Molybdos, "lead" | Silver Miner | The second pit; mandatory | 80 | Probopass, Durant, Skarmory | "Don't run with the vinegar. We lose more jars that way than men." |
| Magon | Phoenician Trader | The throne-room stair; mandatory | 81 | Kingdra, Bouffalant, Lycanroc | "The king's downstairs. He likes to hear the mine. Says it sounds rich." |

**The champion: King Arganthonios of Tartessos** (Lv 80–82), who ruled eighty years and lived a hundred and twenty (Herodotus 1.163), on his silver throne. His name is two letters too long for a trainer name; see PG-39.

| Species | Lv | Note |
|---|---|---|
| Excadrill | 80 | |
| Steelix | 80 | The mine shafts |
| Corviknight | 81 | |
| Gigalith | 81 | |
| Tinkaton | 81 | Tin from the far north came through Tartessos. Replaces Copperajah, which Croesus fields |
| **Archaludon** | **82** | **Ace** |

```text
ARGANTHONIOS: A hundred and twenty. My physician says a hundred and fifty.

ARGANTHONIOS: Your lot put physicians out of business, I hear.
```
After the battle (he paid for the Phocaeans' city wall, Herodotus 1.163):
```text
ARGANTHONIOS: I paid for a wall for some Greeks once. Good wall. They left anyway.
```

**The prize.** The **Silver Emblem**; **TM Iron Defense**, the wall he paid for; and a **King's Rock**.
```text
ARGANTHONIOS: A king's rock. I have a mountain of them. Several.
```
Alethea's panel: "TRUE: the mountains ran with silver. TOLD: so did the anchors. True too." (Diodorus 5.35: the Phoenicians loaded so much that they cast their anchors in silver.)

**Look and sound.** The Silver Mines of Tartessos's cave set, plus ore faces in four states (cold, hot, cracked, melted), braziers on stands, vinegar jars and pithoi, floor channels, moulds and silver planks, and the silver throne. The hall theme in its Far West voicing.

---

### 4.9 The Western Sea: Milo's palaestra

> *Milo of Kroton carried a calf every day until it was a bull* (Quintilian 1.9.5). *Kroton sent one ship to Salamis, under Phayllus, three times a victor at Delphi* (Herodotus 8.47).

**The hall.** Milo's palaestra at Kroton shares a wall with Pythagoras's school; you can see the bean garden over it, and once, when the school's roof fell in, Milo held it up while everyone got out (Strabo 6.1.12). Colonnaded courts round dug sand pits (the *skamma*), racks of jumping weights, sandbags, and at the end the wrestling ground. Two maps: **the jumping courts** (45×20, six screens) and **the wrestling ground** (20×15, two screens).

**The puzzle: Phayllus's Leap.**
- **The weights.** Take a pair of *halteres*, the jumping weights, from the rack at the door. Swung forward as you jump, they carry you further, as Aristotle noticed (*Problemata* 5.8; *Progression of Animals* 705a). You hand them back when you leave.
- **Leaps.** With the weights you clear a one-tile pit from a standstill, and a two-tile pit after a run of at least two steps.
- **Falls.** A pit is soft. Fall in and you climb out at its near edge.
- **Teach: the first court.** One one-tile pit.
- **Test: the second court.** One- and two-tile pits, with run-up lanes and walls that cut some run-ups short.
- **Combine: the third court.** Milo asks you to carry his calf across. With a calf on your shoulders you can't run (`SYSTEMS.md` §10's "don't run" rule), so only the one-tile leaps are open to you. The one-tile way across starts behind a gate that unbars only from the far side, and only the two-tile leaps reach it. Put the calf down, go round by the long jumps, unbar the gate, then come back for the calf and carry it over.
- **The safety valve.** The palaestra's attendant, who will jump it in front of you.
- **The shortcut.** The street gate between the second and third courts.
- **After the Emblem.** The calf grazes in the third court, until it goes home with you (the prize, below).

```text
ATTENDANT: Swing the weights as you jump. One tile standing, two running.
```
```text
MILO: Carry my calf across for me. You can't run with a calf. Don't try.
```
```text
You can't take a running leap with a calf on your shoulders.
```

**Trainers** (Lv 78–80).

| Trainer | Class | Where | Lv | Team | Line |
|---|---|---|---|---|---|
| Philippos of Kroton, an Olympic victor whom Herodotus calls the handsomest Greek of his day (5.47) | Wrestler | The first court; mandatory, easy | 78 | Hitmonchan, Hitmontop, Sawk | "I was the handsomest Greek of my day. Herodotus says so. Look it up." |
| Astylos, whose house Kroton turned into a prison when he ran for Syracuse (Pausanias 6.13.1) | Wrestler | A pit island; optional | 79 | Lopunny, Scrafty, Passimian | "When I ran for Syracuse, Kroton made my house a prison. Fair, really." |
| Phayllus | Wrestler | The third court's gate; mandatory | 79 | Hitmonlee, Mienshao, Medicham | "They dug the pit fifty feet. I jumped fifty-five. Mind the far edge." |
| Myia, Pythagoras's daughter and Milo's wife (Iamblichus, *Life of Pythagoras* 267) | Wrestler | The wrestling ground's door; mandatory | 80 | Annihilape, Pangoro, Hariyama | "My husband carries bulls. My father won't let him eat beans. It's a full house." |

**The champion: Milo of Kroton** (Lv 80–82), in the wrestling ground.

| Species | Lv | Note |
|---|---|---|
| Throh | 80 | A grappler |
| Grapploct | 80 | Another |
| Bewear | 81 | |
| Hawlucha | 81 | |
| Machamp | 81 | |
| **Paldean Tauros (Combat Breed)** | **82** | **Ace.** The calf, grown into the bull |

The team drops Hariyama (Kyrene's) and Conkeldurr (Hektor's and Herakles's) for two grapplers.

```text
MILO: I carried a calf every day until it was a bull. Then I carried the bull.
```
After the battle (a man who won all four of the great games was a *periodonikes*, a victor of the circuit, and Milo was one):
```text
MILO: Win all four games and they call you a periodonikes. You want ten. Greedy.
```

**The prize.** The **Tripod Emblem**; **TM Drain Punch** (Milo ate a whole bull in a day, Athenaeus 10.412e–f); and **the calf**, the Kubfu of `LEGENDS.md` §4.16, whose quest starts here.
```text
MILO: I ate that bull, you know. In a day. This helps.

MILO: Carry it. Every day. When you can't carry it any more, you're ready.
```
Alethea's panel: "TRUE: Milo carried a bull. TOLD: he ate it in a day. He says true."

**Look and sound.** The `magna_graecia` tileset, plus sand pits and their edges, the weights rack, sandbags, the colonnade, the bean garden over the wall and the wrestling ground. The hall theme in its Magna Graecia voicing.

---

### 4.10 Okeanos: Rhadamanthys at the tower of Kronos

> *They travel the road of Zeus to the tower of Kronos, where the ocean breezes blow round the Isle of the Blessed and flowers of gold are blazing* (Pindar, *Olympian* 2.70–72). *Some delight in horses and wrestling, some in board games, some in the lyre* (Pindar, fr. 129).

**The hall.** The tower of Kronos on the largest of the Isles of the Blessed. Rhadamanthys sits there as judge, beside a seat that's empty: in Ichor, the Titan Kronos never came. Before the tower, the meadow is laid out as a board for *petteia*, the game the Blessed play. Its squares were called "cities" and its pieces "dogs" (Pollux 9.98). Two maps: **the board meadow** (30×30, six screens) and **the tower** (15×20, two screens). `UNDERWORLD.md`'s map 26, Elysium's shore, also carries the name "the Isles of the Blessed"; PG-40 proposes renaming it.

**The puzzle: Petteia.**
- **The board.** The meadow is a grid of gold and rose squares. Rhadamanthys's pieces, stone hounds, stand on it, each on a worn groove.
- **The dogs move as you move.** Every step you take, each dog takes one step along its groove, back and forth.
- **Taken.** If you end a step with a dog on either side of you in a straight line, you're taken, and set back at the board's edge.
- **Teach: the first rank.** Two dogs on one groove across the path.
- **Test: the middle ranks.** A full board. Read the grooves, and cross between dogs when the gap is safe.
- **Combine: the last ranks.** Add your own pieces. The board's trainers stand on squares and don't walk to you (speak to one to play), and once you've beaten one he plays on your side and stays where he stood. Trap a dog between you and one of your pieces and it's taken off the board. The last rank is a wall of dogs, so the order you beat the trainers in decides where your pieces are when you get there.
- **The safety valve.** A Blessed onlooker, who has watched a great many games.
- **The shortcut.** A path round the board's rim, open once you've crossed the middle ranks.
- **After the Emblem.** The dogs sit, and the Blessed go on playing.

```text
ONLOOKER: We've got all the time there is, so we play.

ONLOOKER: Don't end up between two dogs. That's the whole game.

ONLOOKER: Anyone you've beaten plays for you. That's how it works here.
```
```text
Two dogs, one on either side. You're taken. Back to the edge.
```
```text
A dog between you and Tellos. It's taken off the board.
```

**Trainers** (Lv 81–83). Herodotus's happy men are here. When Croesus asked Solon who was the happiest man alive, Solon named Tellos of Athens, then the brothers Kleobis and Biton, who yoked themselves to their mother's cart when the oxen were late (Herodotus 1.30–31). All three have finished stories, so they came to the Isles.

| Trainer | Class | Where | Lv | Team | Line |
|---|---|---|---|---|---|
| Tellos of Athens | Blessed Hero (BLESSED HERO) | The board's edge; mandatory, easy | 81 | Ribombee, Vaporeon, Gallade | "Solon called me the happiest man alive. Then I died. Still happy." |
| Kleobis and Biton | Blessed Hero, a double battle | Two squares side by side in the middle ranks; mandatory | 82 | Kleobis: Tauros, Comfey, Slowbro. Biton: Bouffalant, Sylveon, Dondozo | KLEOBIS: "We pulled our mother's cart to the temple. Forty-five stades." BITON: "Then we lay down and didn't get up. Best day we ever had." |
| Epimenides, the Cretan who slept fifty-seven years (Diogenes Laertius 1.109) | Dreamer | Asleep on a square in the last ranks; optional. Beaten, he's your best-placed piece | 82 | Hypno, Snorlax, Komala | "All Cretans are liars. I'm a Cretan. Work it out. I'll be asleep." |

After his battle, Tellos explains the combine:
```text
TELLOS: Beat me and I'm on your side. Get a dog between us and it's off the board.
```
If you hold the Lion Emblem, he adds: "Croesus? Is he still asking?"

**The champion: Rhadamanthys, Judge of the Blessed** (Lv 82–84), in the tower. His name is two letters too long for a trainer name; see PG-39.

| Species | Lv | Note |
|---|---|---|
| Togekiss | 82 | |
| Florges | 82 | The golden flowers |
| Lapras | 83 | The ferry over Okeanos |
| Houndstone | 83 | The dogs. Replaces Gardevoir, which Helen fields |
| Dragapult | 83 | |
| **Metagross** | **84** | **Ace** |

```text
RHADAMANTHYS: I judge the finished. You're not finished.

RHADAMANTHYS: This is irregular, and I'm enjoying it.
```
After the battle. Homer seats him in the Elysian plain (*Odyssey* 4.564) and Plato at the crossroads of the dead (*Gorgias* 524a), where `UNDERWORLD.md` §4.7a has him:
```text
RHADAMANTHYS: Homer seats me here. Plato puts me under the earth.

RHADAMANTHYS: I keep a bench in both.
```

**The prize.** The **Rose Emblem**; **TM Payback** (suffer what you did, and that's justice: "the justice of Rhadamanthys", Aristotle, *Nicomachean Ethics* 1132b); and an **Ability Patch**. Plato's judges see the soul bare, without its clothes (*Gorgias* 523c–e).
```text
RHADAMANTHYS: We judge by what's underneath. Here. See what's under yours.
```
Alethea's panel: "TRUE: the Isles are there. TOLD: only the finished land. You landed."

**Look and sound.** The `okeanos` tileset (the gold meadow and roses), plus board squares in gold and rose, grooves, stone hounds (Houndstone's follower sprite, greyed), white stones, and the tower with its two seats. The hall theme in its Okeanos voicing, with *The Blessed*'s resolved lullaby under it (`OIKOUMENE.md` §7).

---

## 5. The two Proteuses

`OIKOUMENE.md` already had a Proteus: Homer's Old Man of the Sea, with his seals and Ditto on Pharos (§4.5, and `COVERAGE.md`'s overrides). Egypt's champion is now Herodotus's Proteus. Both exist, and they share a name.

| | Proteus of Memphis | The Old Man of the Sea |
|---|---|---|
| Source | Herodotus 2.112–120 | *Odyssey* 4.351–570. Homer already calls him "Egyptian Proteus" (4.385) |
| What he is | A man, the pharaoh who kept Helen and Paris's treasure through the war, and sent Paris home | A sea-god who knows every depth of the sea, and changes shape when held |
| Where | His precinct at Memphis (§4.5) | The sandbar in the Outer Sea where `SYSTEMS.md` §10's theoxenia E13 meets you, and Lynkeus finds it (`ODYSSEY.md` §6.9) |
| His seals | A royal herd on Pharos, off the delta | His own, on the sandbar |
| His shapes | Trained Ditto, playing Homer's version | His own; E13's four battles, "Hold fast" |
| His Pokémon | His team (§4.5) | Haligeron (dex #137), whose kind lives in Atlantis's shallows (`POSTGAME.md` §3.2) |

**How they agree.** Menelaus really was becalmed off Pharos for twenty days (*Odyssey* 4.360). In Ichor he grabbed one of the pharaoh's seal-herders there, went home, and told it as a god. Herodotus's priests told it the other way. The pharaoh loves Homer's version and had his Ditto trained to play it. The god, out past the Bear, has heard about this and is annoyed.

**What changes elsewhere.** On Pharos (`OIKOUMENE.md` §4.5; `coverage.py`'s overrides), the seals are the pharaoh's herd and the Ditto are strays from his troupe. Popplio's line still lives among them, wild only (PG-5). SYSTEMS's E13 and ODYSSEY's islet are unchanged. This is decision PG-37.

---

## 6. Music

**One hall theme, *The Periodos*, in ten short arrangements** (decision PG-41). This fits `MUSIC.md`'s method, a few motifs transformed for each place, better than ten unrelated cues would, and it costs a third as much.

- **A: home.** Every hall opens on the Thread (MUSIC.md motif 1, 5-1-2-3 rising) in D Dorian, Elaia's mode: a processional for aulos, kithara and frame drum. "D is home", and in every hall your own thread arrives first.
- **B: the land.** Then the land's own music: the B section is in the land's mode and meter and quotes the first phrase of its land track (`OIKOUMENE.md` §7). For example, Lydian and too sweet at Sardis, a 9/8 rowing beat at Aia, Apollo's lyre in Mixolydian at Abaris's temple, harp and sistrum at Memphis.
- **Form.** Intro 1 bar, then a loop of A 8 and B 8, about 30 seconds, in the `ichor` voicegroup like every song from 613 on. At about 4 KiB each, ten arrangements cost about 40 KiB.
- **Battles** use `OIKOUMENE.md` §7's *Battle! Oikoumene Trainer* for hall trainers and *Battle! Champion of the Periodos* for the champions and Helen.
- **Exceptions:** the Song at the Skaian Gate plays the Troad's *The Plain of Troy*, and the temple of the Stranger plays *The Black Land*.
- **Fallback:** if ROM runs short, one arrangement serves all ten halls, at about 5 KiB.

`MUSIC.md`'s "Themes still to write" lists the cue.

---

## 7. Budget: maps, trainers, flags and ROM

### Maps

| Hall | Maps | Size |
|---|---|---|
| 4.1 The Skaian Gate | 4: the Gate and the Tower, each with its Song twin | 30×20 and 20×30, each twice |
| 4.2 The treasury | 2: the Weighing Room and Strongroom; the Lion Vault and counting-room | 45×20, 30×20 |
| 4.3 Aietes's palace | 2: the bronze halls; Hecate's stair and shrine | 40×30, 20×15 |
| 4.4 The round temple | 2: the outer rings; the swan pool and temple | 45×30, 20×20 |
| 4.5 The precinct of Proteus | 3: the pylon and hypostyle; the Tyrians' Camp and inner court; the temple of the Stranger | 30×20, 30×20, 15×12 |
| 4.6 The bath-court | 2: the bath-courts; the dawn hall | 45×20, 20×15 |
| 4.7 The hippodrome | 2: the practice ground; the hippodrome | 30×20, 60×20 |
| 4.8 The royal gallery | 2: the gallery; the silver throne room | 60×20, 15×15 |
| 4.9 The palaestra | 2: the jumping courts; the wrestling ground | 45×20, 20×15 |
| 4.10 The tower of Kronos | 2: the board meadow; the tower | 30×30, 15×20 |
| **Total** | **23 maps** | |

The halls are interiors and courts, so each shares its town's map section, and the Oikoumene still needs about 75 sections (`OIKOUMENE.md` §11). All ten halls are in 1.0, because the champions are.

### Trainers

| | Count | Ids |
|---|---:|---|
| Hall trainers, 4 per hall | 40 | New |
| Helen | 1 | New |
| The ten champions and their ten rematches | 20 | Already in `OIKOUMENE.md` §13's estimate |
| Herakles and his rematch | 2 | Already in the estimate |

- **41 new trainers.** `OIKOUMENE.md` §13's 1.0 estimate rises from about 280 to about 320.
- **The id range runs short, and did before this.** The Oikoumene's block is ids 680–819, which is **140** (`tools/ichor/claim_ranges.md`). That couldn't hold the earlier estimate of about 280 either. The halls themselves, with the champions, rematches and Herakles (63 ids), fit inside 140, leaving 77 for every route, dungeon and hero. Nothing has been claimed. This is decision PG-38.
- **Names and labels.** A trainer name holds 10 characters and a class label 12 (`TRAINER_NAME_LENGTH`, `struct TrainerClass`). Every hall trainer's name fits. ARGANTHONIOS and RHADAMANTHYS are 12, and several of §6's class names are longer than 12; the tables above give each class's short label. This is decision PG-39.
- **New classes.** One trainer class, Silver Miner, for the Far West, which had none of its own; it shares the label MINER with the Arimaspian Miner. Also the champions' titles: PRINCE, KING, PRIESTESS, PRIEST, PHARAOH, HUNTRESS, ATHLETE, JUDGE, and QUEEN for Helen. A class is a name and a prize-money value.

### Flags

The Oikoumene's bank flags are 0x3C0–0x47F, 192 in all (`tools/ichor/claim_ranges.md`). The halls need **30**, and none are claimed yet:

| Flags | Count | Note |
|---|---:|---|
| The ten Emblems | 10 | Claim them first and together, so they're contiguous and `Ichor_CountFlags` can count them for Herakles's gate and the trainer card |
| Prize given (TM and land reward) | 10 | |
| Midpoint shortcut open | 10 | |

- **No vars.** Every puzzle's state lives in `VAR_TEMP` for the length of a map, and each stage is one map.
- **Trainer flags** come with the trainer ids.
- **The range is tight overall.** 30 of 192 is fine for the halls, but the Oikoumene's hundred-odd households, its items and its quests will want most of the rest. Watch it as the lands are built.

### ROM

| Item | Size |
|---|---:|
| 23 hall maps (layouts and events) | ~45 KiB |
| Hall tiles and metatiles, added to the land and interior sets; the Song's palettes | ~60 KiB |
| Scripts and text for ten halls and Helen | ~85 KiB |
| Trainer data, 41 parties | ~10 KiB |
| Sprites: the chariot, Proteus's portrait and pic, the Silver Miner, Eidothea and Chalkiope | ~15 KiB |
| Ten hall arrangements | ~40 KiB |
| Code (`OIKOUMENE.md` §13's hall engine table) | ~6 KiB |
| **Total** | **~260 KiB** |

That takes the Oikoumene to about 1.35 MiB at 1.0 (`OIKOUMENE.md` §13).

---

## 8. The Lazarus check

- **No Muses.** Lazarus's gyms are the Muses'. None of these champions is a Muse or a singer, the halls aren't type-themed temples, and no puzzle asks you to play music or dance. (The Troad's Song is the story the bards tell, not a tune you play.)
- **Rhadamanthys** is not Lazarus's seventh leader, Rhadine. She's a different, minor figure, and the two names share only their first four letters.
- **No Lazarus starters on any team.** Kyrene's Delphox became Espathra, and nobody fields Primarina, Decidueye, Incineroar, Greninja, Chesnaught, Meowscarada, Skeledirge or Quaquaval.
- **No forbidden names.** No form or name is prefixed Aegis, Gryphon, Medusa or Titan. Libya's Gorgon story stays out of Kyrene's hall.
- **No Mega-as-weapon** and **no Chimera.**
- **Place names** are clear of Lazarus's. The nearest is its Palati ("palace"), against English descriptions such as Aietes's palace.
