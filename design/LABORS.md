# The Twelve Labors

- **Owner:** Quest and level design.
- **Status:** a proposal for the user's approval. Nothing here is built yet.
- **Spine:** `design/STORY.md` §3, "The post-game spine": the Labors are **glory earned, not fated: Kleon's kleos, made real.** Where this file and STORY.md disagree, STORY.md wins.
- **Umbrella:** `design/POSTGAME.md` sets where this sits in the post-game, the levels, the save struct and the scope tiers.
- **Companions:** `design/UNDERWORLD.md` (Labor 12 needs the Katabasis), `design/ODYSSEY.md` (Labors 8, 9 and 11 sail on the player's trireme), `design/SYSTEMS.md` (relics, fire, rites, star chart, theoxenia tells), `design/LABYRINTH.md` (Asterion, bull-leaping, Ariadne).
- **Species** come from the Aethos dex (`claude/aethos-dex-a7c73a:design/dex/`). The dex is Aethos-only until the League is beaten (dex D5), so the post-game may also use existing species. Every place this file departs from the bible's casting is listed in §5 and flagged.

---

## 0. The hook

At the next Klotheia, Kleon comes second in the footrace, to a Wooloo (STORY §7.11). That evening he finds you in the square with a scroll he's borrowed from the Akademia and hasn't read properly.

"Herakles had twelve. Let's see about us."

He was told all his life he'd be glorious while young, and he heard death in it. Now nobody's told him anything, and he wants glory he's actually earned. You're the Archon now. He'd like the Archon along. So the two of you go to Olympia, to the one member of the Pantheon who still sets labors the old way: Olympias, the Serpent Queen, Hera's seat.

Each Labor is a myth you play rather than read: a lion you must corner before Kleon can fight it; a hydra whose heads grow back unless you carry fire in time; a hind you follow for days; two rivers you turn with every relic you own while a blind man shovels; birds you scare into the sky and fight up there; a bull you leap and then ride across the sea. Around the world's edge, a queen whose camp a goddess is poisoning with rumor, a herd you drive home from the sunset, the sky itself on your shoulders, and finally the hound of Hades, dragged up into a daylight he hates.

Twelve metopes go up on the Temple of Zeus, one for each, carved by a sculptor who can't stop talking. The last one shows two figures, not one.

### Pillars

1. **Twelve mechanics, not twelve boss fights.** Every Labor has one verb nobody else uses: corner, cauterize, track, lure, divert, flush, leap and ride, feed, unmask, herd, endure, escort. The boss battle, when there is one, is the last beat, never the whole.
2. **The myth is the rule.** No weapon cuts the lion, so your Bag doesn't work in its cave. The Hydra's heads grow back, so a cleared pool refills unless it's burned. Herakles lifted the sky for Atlas, so you can't move while you hold it. Nobody explains any of this; the play does.
3. **Glory earned, not fated** (STORY §3). Herakles's name means "glory of Hera". Kleon's means "glory". He proposed the Labors and fights beside you in several (Labors 1, 2, 11 and the finale's crowning). Where he goes on alone, he keeps losing ground, because he keeps stopping to help people. That is the glory he earns, and it's shown, not told.
4. **Hera meddles, Olympias shrugs.** The goddess sent a crab at the Hydra fight, a rumor to the Amazons and a gadfly to Geryon's herd. In Ichor she does all three. Olympias, her priestess, neither apologizes nor explains.
5. **Fail forward.** No Labor can be failed for good. A lost battle, a missed flame or a bolted hind resets that step and nothing else (SYSTEMS's rule for theoxenia, and LABYRINTH's).

### At a glance

| | |
|---|---|
| Where in the story | Post-game. Kleon proposes the Labors at the epilogue's Klotheia (STORY §7.11); they open on your first visit to Olympia after it. See POSTGAME §2. |
| Structure | Six pairs, set one pair at a time. Either Labor of a pair can come first. |
| Length | About 7 hours: 20–40 minutes per Labor, plus the finale |
| Levels | `design/BALANCE.md`'s Aethos post-game row: wild 55–70, trainers 65–75, bosses 70–80. By pair, bosses run 70 (Pair 1) to 79 (Pair 6), and Olympias's ace is 80. |
| Maps | 28 new (§4 and §7), plus revisits to 9 main-game maps |
| New lands | Thrace, Themiskyra, the Caucasus crag, Erytheia and the far west. These are the edges of the known world, and they open the Oikoumene (POSTGAME §0). |
| Bosses | The Lion, the Hydra and the Crab, the Hind, the Boar, the Muck, the Bronze Flock, the Bull from the Sea, King Diomedes, Queen Hippolyta, Geryon, Zeus's Eagle, Ladon, Kerberos, and Olympias |
| Partner battles | Kleon fights beside you against the Lion (Labor 1), the Hydra and the Crab (Labor 2) and Ladon (Labor 11): the expansion's player-plus-partner multi battles (§11) |
| Hard gates | Labors 8 and 9 need the trireme (ODYSSEY §2). Labor 11 needs Labors 9 and 10. Labor 12 needs the Katabasis. |
| Prize | The **Kotinos**, Olympia's wild-olive crown, which Herakles planted (§4). It is one of the keys to Olympus's true summit (POSTGAME §3.3). |

---

## 1. The frame

### Who proposes them, and who sets them

**Kleon proposes them** (STORY §3: "Herakles had twelve. Let's see about us."). His arc in the main story ended with him breaking his own thread, carrying the blind Hyperion down the Stair where nobody would see, and coming second to a Wooloo (STORY §2, Kleon). What's left is the thing he always wanted: to be remembered, for something he chose.

**Olympias sets them.** Olympias, the Serpent Queen, holds Hera's seat of the Pantheon (PITCH §3; STORY §2, the Twelve). In myth Hera raised the Hydra and set Ladon to guard the golden apples, and Hera set Herakles's labors through her creature, King Eurystheus. Ichor drops the middleman: Hera's priestess sets them herself.
- **Who she is** (STORY §2): a mother who wrote her son a fate. "I told my son a god was his father. He believed me, and he conquered the world. Was I lying?" She is the foil to Rhea, who misread her son's fate, and to Melitta, who gave hers none.
- **Why she agrees.** She doesn't believe glory without a fate is possible. She sets the Labors to find out.
- **Her arc** follows Hera's: contempt, grudging respect, a crown. Hera made peace with Herakles in the end and gave him her daughter Hebe.
- **Where.** In the post-game she leaves Olympus for Olympia, where Hera's temple, the Heraion, is older than Zeus's. She sets the Labors from its doorway.

Why not an oracle: **prophecy has ended** (STORY §1, rule 9). In myth the Pythia sent Herakles to his labors. Here nobody can be sent; you have to choose.

**The Heraion** sits on the Altis's north side, under the Hill of Kronos, facing the great Temple of Zeus across the precinct (POSTGAME §3 sketches the Altis). Paionios's scaffold leans on the Temple of Zeus's east end, where the metopes go.

```text
  HERAION (interior, 24x14)
 +----------------------------------------------+
 |  [cult statue of Hera, seated]               |
 |        O  OLYMPIAS (stands, never sits)       |
 |   .  .  .  .  .  .  .  .  .  .  .  .  .  .   |
 |  [disc of Hera]      [trophy niches x12]     |
 |  (the oldest thing    1  2  3  4  5  6       |
 |   in Olympia)         7  8  9 10 11 12       |
 |   .  .  .  .  .  .  .  .  .  .  .  .  .  .   |
 |  (pithos, large)   K (Kleon, between Labors)  |
 |                                              |
 +---------------------[ door ]-----------------+
```
- **The trophy niches** fill as you dedicate each Labor's proof: the hide, the golden head's tooth, a golden antler tine, a tusk, a stable door-pin, a bronze feather, a hank of sea-white hair, a bronze bit, the War-Belt, a red heifer's bell, a golden apple, and a three-headed collar.
- **The pithos** is a giant storage jar. It matters at Labor 12.
- **Olympias's Pantheon line-up** is unchanged elsewhere. She is at Olympia only once the Labors open, and back on Olympus during Pantheon rematches.

### Ten that became twelve

In myth, Eurystheus set ten labors and then refused to count two: the Hydra, because Herakles's nephew Iolaus helped, and the Augean Stables, because Herakles asked to be paid. He added the Apples and Cerberus.

Ichor plays it straight.
- **Olympias sets ten.** The Scroll of Deeds lists ten.
- **Labor 2:** Kleon is your Iolaus. He holds the fire, and fights beside you. Olympias: "You had help. It doesn't count."
- **Labor 5:** Augeas pays you, whether you agree or not. Olympias: "You were paid. It doesn't count."
- **After Labor 10,** she sets the last two: "Ten done. Eight count. Two more." The Scroll grows two lines.
- **In the end all twelve count.** The metopes show twelve, and Olympias admits it in the finale.

A player who knows the myth sees it coming. One who doesn't gets a surprise that's fair, because the Scroll said *ten*.

### Kleon's part

Olympias sets the same twelve for both of you, "as a pair, since you insist". Kleon fights beside you in some and goes ahead alone in others, and wherever he goes alone he gets distracted helping someone: a shepherd's lost lamb in Nemea, Atalanta out of a snowdrift, the Amazons' wounded. He keeps a tally on a wax tablet of who's done more. By the end it says he's three behind, and he's prouder of the tablet than of anything he won.

| Labor | Kleon's moment | What it shows |
|---|---|---|
| 1 | Charges the lion through the wrong mouth of its cave, and it bolts out the other. Then, once you've cornered it, **he fights it beside you** (STORY §3: "the Nemean Lion is the first Labor, and Kleon fights it"). | Why you seal one mouth; and that he wanted to be the one |
| 2 | Holds the fire, and fights the golden head and the crab beside you. Your Iolaus. | He chooses to help, and it costs him the Labor |
| 3 | Kallisto, who beat him six to nothing under the new moon on a forged prophecy, **apologizes to him** at the ford (STORY §3). | The forged fates' last casualty, put right |
| 4 | Falls into a snowdrift. Atalanta pulls him out, laughing. | Humility |
| 5 | Arrives to find **Hyperion and his ex-grunts** already shoveling the stables by feel (STORY §3). Kleon carried Hyperion down the Stair; Hyperion doesn't know it was him. | A secret kindness that stays secret |
| 6 | Is afraid of birds. Admits it. | A Lakonian admitting fear |
| 7 | Apologizes to Asterion, whom he tried to kill | The scene the Labyrinth set up |
| 8 | Crews your trireme to Thrace | — |
| 9 | Hears the rumor and nearly starts the war. You stop him. | Hera's poison works on proud men |
| 10 | Herds badly. Very badly. | Comic relief before the last pair |
| 11 | Guards Ladon's sleep while you hold the sky, then fights Ladon beside you | Trust |
| 12 | Waits at the top of Tainaron with water for the hound | Kindness, at the end |

### Hera's hand

Three times the goddess interferes. Olympias's reaction is always one line, and never an apology.

| Labor | Hera's move (myth) | In Ichor |
|---|---|---|
| 2 | She sent the crab Karkinos to bite Herakles's foot | A giant Karkitox joins the Hydra's last fight, a multi battle with Kleon beside you |
| 9 | She went among the Amazons disguised, saying Herakles meant to carry off their queen | A disguised goddess stirs the camp. You find her by the theoxenia tells (SYSTEMS §10). |
| 10 | She sent a gadfly that scattered the cattle in Thrace | A Yanmega swarm scatters your herd mid-drive, and you round them up again |

---

## 2. Structure, tracking and pacing

### The six pairs

Olympias sets two Labors at a time. Finish both and she sets the next two. Either Labor of a pair can come first, so the player always has a choice.

| Pair | Labors | Lands | Levels | Needs |
|---|---|---|---|---|
| 1 | Nemean Lion, Lernaean Hydra | Emporion's hills; Lakonia | Wild 55–62; bosses 70–71 | The Girdle of Herakles; Hecate's Torch |
| 2 | Ceryneian Hind, Erymanthian Boar | All Aethos; Arkadia | Wild 57–64; bosses 71–72 | — |
| 3 | Augean Stables, Stymphalian Birds | Elis, by Olympia; Lakonia | Wild 60–66; bosses 72–73 | The Hammer, the Girdle, the Labrys, the Sickle and the Horn of Achelous |
| 4 | Cretan Bull, Mares of Diomedes | Knossa; Thrace | Wild 62–67; bosses 73–74 | The trireme for Thrace |
| 5 | Hippolyta's War-Belt, Cattle of Geryon | Themiskyra; Erytheia | Wild 64–69; bosses 75–77 | The trireme for Themiskyra |
| 6 | Apples of the Hesperides, Kerberos | The Caucasus and the far west; the Underworld | Wild 65–70; bosses 77–79; Olympias 80 | Labors 9 and 10; the Katabasis |

All relics except the two post-game ones (the Nereid Pearl and Aeolus's Bag) are from Acts I–III (SYSTEMS §1), so every one is in hand when the Labors open. None of the Labors needs the Pearl or the Bag.

### Tracking

Four views of the same progress. None of them is a new screen.

1. **The Scroll of Deeds** (PITCH §5): a "Labors" page listing each Labor, its land and its state ("Set", "Done", "Dedicated", "Doesn't count", "Counts"). It shows ten lines until Pair 5 is done, then twelve.
2. **The metopes.** Twelve carved panels go up on the Temple of Zeus at Olympia, as the real ones did (the temple's twelve metopes showed the twelve labors). After each Labor, **Paionios** the sculptor carves one. They are 12 object events above the temple porch, with hide flags. Read one and a short caption plays. Stretch goal: a 64×64 picture per metope, in the amphora painting window (SYSTEMS §5).
3. **The trophy niches** in the Heraion (§1).
4. **The star chart** (SYSTEMS §8): **Leo** (Labor 1), **Hydra** (Labor 2), **Draco** (Labor 11) and **Hercules** (all twelve). This file adds none. One proposed amendment is in §13: let Labor 2's crab also place **Cancer**.

### Pacing across the post-game

POSTGAME §2 has the recommended route. In short:
- Pairs 1–3 stay in Aethos and pay off the main game's places with new encounters. They make a good first week.
- Pair 4 starts the reach outward, Pair 5 hits the edges of the world, and Pair 6 waits for the Katabasis.
- The Katabasis fits between Pairs 3 and 4. The Odyssey, at the Oikoumene's higher levels, comes after the Kotinos (POSTGAME §2).

---

## 3. The Labors

Each Labor below has: the myth in one line; the play; its maps, with a sketch where the layout matters; the steps; the mechanic and its engine note; the boss; its wild Pokémon; the rewards; the music; and the key scene's draft lines.

Dialogue follows SCRIPT.md's format: one box per line, `[brackets]` are stage directions, `{PLAYER}` is the player's name, `?? A/B` is a choice.

### Scene 0. Elaia, then Olympia: "Let's see about us"

[The Klotheia, evening, after the epilogue (STORY §7.11). The square is emptying. Kleon sits on the edge of the well with a borrowed scroll, still out of breath from the footrace.]
```text
KLEON: Second. To a Wooloo. In front of my mother.

KLEON: She said "Good." I don't know what to do with "Good."

KLEON: I've been reading. Daphne lent me this. It's about Herakles.

KLEON: Nobody told him he'd be glorious. They told him to clean a stable.

KLEON: Herakles had twelve. Let's see about us.

KLEON: …You're Archon now. You probably have Archon things to do.

KLEON: Do them after. Olympia. The Serpent Queen still sets labors. Come on.
```
[Olympia, the Altis. First entry. Olympias stands at the top of the Heraion steps and doesn't come down.]
```text
OLYMPIAS: The new Archon. And the Lakonian who came second to a sheep.

KLEON: News travels.

OLYMPIAS: I make it my business. Labors, is it?

OLYMPIAS: I told my son a god was his father. He believed it, and it made him.

OLYMPIAS: Nobody's told you anything, boy. Nobody will now. Prophecy's over.

OLYMPIAS: I don't believe glory comes without a fate behind it. Show me.

OLYMPIAS: Here is the old list. Ten labors. The same ten, for both of you.

KLEON: Together.

OLYMPIAS: As a pair, since you insist. Two at a time.

OLYMPIAS: Start with the lion. And the Hydra.

OLYMPIAS: Mind the Hydra. I raised her. She was a sweet little thing.

KLEON: [to you, quietly] I'm keeping count. Of who does more. Just so you know.
```
[The Scroll of Deeds gains the Labors page. Labors 1 and 2 are set.]

---

### Labor 1. The Nemean Lion: *corner it*

> *A lion no weapon could wound. Herakles blocked one mouth of its cave and strangled it in the other* (Apollodorus 2.5.1).

**Play.** A great Nemeleon has been taking herds from the hills behind Emporion. Its cave has two mouths, and whenever anyone comes in one, it leaves by the other. Kleon proves this for you at once. You have to seal one mouth with a column drum, using the Girdle of Herakles, then drive the lion back into its den. Inside, no weapon works: your Bag won't open.

**Maps.**

| Map | Size | Notes |
|---|---|---|
| Nemea Glen | 30×56 | A new valley route between Emporion's hills and the Eleusa road. The entrance is a column-drum pass (Girdle), visible from the Act I road since Act I: a relic gate that invites a return (MAP_DESIGN §1). Forced grass in two bands; a shepherd's hut rest point. |
| The Lion's Den | 26×18 | The two-mouthed cave |

```text
  NEMEA GLEN (30x56), south to north
 +------------------------------------+
 |  [Lion's Den: WEST mouth]  ^^^^^   |  N
 |       (( den ))       [EAST mouth] |
 |  ::::::::  scrub  :::::::: ledges  |
 |  ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,  |  forced grass band 2 (3 deep)
 |   T3 (Herdsman, faces S)           |
 |  stele: "Here the lion drank."     |
 |       [shepherd's hut] (rest)  *   |  * hidden: Revive behind the trough
 |  ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,  |  forced grass band 1 (2 deep)
 |   T1 (Shepherd)        T2 (Goatherd, optional, faces E)
 |   o sealed jar (TM Crunch), up a side path past optional grass
 |  [column drum: GIRDLE]             |
 +------[ to the Eleusa road ]--------+  S
```

```text
  THE LION'S DEN (26x18)
 +--------------------------------------------+
 |  WEST MOUTH  W       bone heap      E  EAST MOUTH
 |   |  [drum slot]   . . . . . .   [drum slot]  |
 |   +---.  .  .  .   L (lion)  .  .  .  .---+   |
 |       .  pillar .  .  .  .  .  pillar  .      |
 |       .  .  .  .   [THE DEN]  .  .  .  .      |
 |       .  .  .  .   (inner, 8x6)  .  .  .      |
 +--------------------------------------------+
```

**Steps.**
1. **The Glen.** Two forced grass bands and three trainers. The shepherd's hut has a bed and a stew pot: a heal. The shepherd's lamb is missing. (Kleon finds it later.)
2. **The first try.** At the den, Kleon arrives from the east path. He charges in by the east mouth. The lion lopes out of the west mouth and away up the glen. Kleon comes out flat on his back.
3. **The lesson, shown.** The lion returns to the den after 30 steps. It always leaves by the mouth you didn't come in by.
4. **Seal a mouth.** Both mouths have a slot for a column drum. Two drums lie up the slope. Push one down a gully into a slot (the Girdle). Either mouth works.
5. **Corner it.** Enter by the open mouth. The lion retreats from you across the cave toward the sealed mouth, finds it blocked, and backs into the inner den.
6. **The fight, with Kleon.** Kleon comes in behind you: "My turn. Together." In the inner den the great lion and his lioness turn at bay. It's a **multi battle: you and Kleon against the two lions** (STORY §3: "Kleon fights it"). "No weapon could pierce it": nobody's Bag opens in this battle. The great lion has a totem boost.
7. **After.** Beaten, the lion yields. Throw a Poké Ball after the battle (a guaranteed victory catch), or leave it to the glen. The lioness stays with her cubs.
8. **The proof.** Its old shed hide lies on the bone heap. Take it to the Heraion.

**Mechanic: cornering.**
- **The lion's movement.** It moves away from the player when the player is within 4 tiles, along open floor, toward the mouth the player isn't nearest. With both mouths open it leaves the map and respawns in the den 30 steps later. With one sealed, it ends in the inner den.
- **The drums** reuse the Girdle's column drums (SYSTEMS §1).
- **Engine:**
  - A new movement type, **flee-from-player**, is the inverse of the follow logic in `src/event_object_movement.c`. Labor 10's cattle use the same type. Medium–Low.
  - The fight sets `B_VAR_NO_BAG_USE` to 2 for the battle (`include/config/battle.h`; it is 0 today, so point it at a new var, or reuse a free temp var) and uses `settotemboost` (`asm/macros/event.inc`, line 2205).
  - The victory catch uses `B_FLAG_VICTORY_CATCH_GUARANTEED` (also 0 today; give it an `FLAG_ICHOR_` flag).
  - **The partner battle** is the expansion's player-plus-AI-partner wild battle: `BattleSetup_StartMultiBattle` with `MULTI_BATTLE_2_VS_WILD` in `gSpecialVar_0x8005` (`src/battle_setup.c`, line 357), Kleon's party loaded by `FillPartnerParty`. Low.
  - **Fallback:** the lion walks a fixed path chosen by which slot holds a drum.

**Boss: the Lions of Nemea** (you and Kleon, each with your own party).

| Species | Lv | Ability | Item | Moves | Notes |
|---|---|---|---|---|---|
| Nemeleon (the great lion) | 70 | Fur Coat | — | Crush Claw, Noble Roar, Bulk Up, Double-Edge | Totem boost +1 Defense, +1 Speed. No Bag for either side. |
| Nemeleon (the lioness) | 68 | Unnerve | — | Crunch, Slash, Roar, Take Down | — |

**Kleon's partner team** for Pair 1 (Lv 68–70): his starter's final stage (the one that beats yours), Hoplektor, Nemeleon (his own, from Lakonia's hills, STORY §2) and Kourodin, his mother's.

**Wild Pokémon** (Nemea Glen, Lv 55–59). Aethos species only: under BALANCE.md every non-Aethos species lives in the Oikoumene (POSTGAME §4).

| Time | Species |
|---|---|
| Day | Nemecub 10%, Lophops 15%, Gelasable 15%, Cairnolith 15%, Kerazap 10%, Chelonet 10%, Spalunk 15%, Alekrow 10% |
| Night | Lykopup 25%, Gelasable 20%, Nemecub 15%, Cairnolith 15%, Arkoby 15%, Obolorn 10% |

**Trainers.** Shepherd Damon (Lv 65), Goatherd Lakon (Lv 66, optional), Herdsman Thyrsis (Lv 67).

**Rewards.**
- The Lion's Hide (trophy) → Hera Favor +5, Zeus Favor +5.
- **Leo** placed (SYSTEMS §8).
- Olympias, on dedication: TM Swords Dance.
- Glen items: TM Crunch, Revive (hidden), Max Ether, a fixed dig spot (Gold Stater).

**Music.** *The Labor*, a new route theme in Dorian 7/8 (kalamatianos), one variant per Pair (§8). *The Lion*, a battle cue that starts with a single frame-drum hit and a held aulos.

**Scene: the first try.**

[At the east mouth. Kleon jogs up the path behind you, sword-and-shield Hoplektor at his heels.]
```text
KLEON: Ha! Beat you to it. Stand back. I've read the story.

KLEON: He goes in. He grabs it. Done. How hard can it be?
```
[Kleon runs into the east mouth. A roar. The lion bounds out of the west mouth, shakes its mane and lopes uphill. Kleon staggers out of the east mouth and sits down hard.]
```text
KLEON: It went out the back.

KLEON: Caves shouldn't have backs.

KLEON: …There's a drum up there. Like the ones at Thyrsa.

KLEON: You've got the Girdle. I've got a headache. Seal it.

KLEON: But when it's cornered, I'm going in. Herakles went in. I'm going in.
```
[In the inner den, after the battle. Kleon sits against the wall, grinning, a long scratch down one arm.]
```text
KLEON: We did it. Both of us. I counted.

KLEON: Nobody wrote that. I'd have read it. I'd have hated it.
```
[Later, if you return after the Labor.]
```text
KLEON: Found the shepherd's lamb. It was in the den. Asleep on the lion.

KLEON: Don't put that on a metope.
```

---

### Labor 2. The Lernaean Hydra: *cauterize it*

> *For every head Herakles cut off, two grew. His nephew Iolaus burned each stump, and Herakles buried the immortal head under a rock. Hera sent a crab to bite his foot* (Apollodorus 2.5.2).

**Play.** South of Lake Stymphalia, the reeds give way to the Springs of Lerna: eight pools in a ring around a ninth, as the Hydra had eight mortal heads and one immortal. A head rises from a pool. Beat it, and you have to carry fire to that pool's brazier before the stump regrows, or two heads rise from the pools beside it. Kleon is your Iolaus: he keeps the fire burning in the rain and shouts the count. The near pools are easy. The far corners are out of reach from his fire, until you notice that a brazier you've already lit is a fire too. When all eight are burned, the immortal golden head rises from the centre, and Hera's crab comes out of the reeds to help it.

**Maps.**

| Map | Size | Notes |
|---|---|---|
| The Springs of Lerna | 40×36 | A new marsh south of the main game's Lake Stymphalia, through reed beds you cut with Demeter's Sickle. The pool grid is the arena. |

```text
  THE SPRINGS OF LERNA (arena, centre of the map)
       . = marsh path, ~ = water, B = brazier, R = column drum

        P1 ~ B1 . . . . . P2 ~ B2 . . . . . P3 ~ B3
         .                   .                   .
         .       (reeds)     .     (reeds)       .
        P4 ~ B4 . . . . . (( P9 )) . . . . . P5 ~ B5     P9 = the golden head's pool
         .                 [ F ]  R              .       F = Kleon's fire, R = column drum
         .                   .                   .
        P6 ~ B6 . . . . . P7 ~ B7 . . . . . P8 ~ B8
   Steps along the paths: F to P4, P5 or P7 is 6; F to P2 is 8 (round P9);
   F to a corner (P1, P3, P6, P8) is 12; an edge pool to its corners is 6.
```

**Rules.**
- **Carrying fire.** Light the Torch at Kleon's fire, F. In the marsh's rain the flame lasts **10 steps** on Hero (13 on Mortal, 8 on Spartan). This is SYSTEMS §2's carried-flame grammar, with the rain rule from theoxenia E2. Kleon shouts the count as you go: "Six! Five!"
- **A head.** A Trilerna rises from a pool when you come near. Beat it and the pool is "cut". Bring a flame to its brazier and the pool is burned for good.
- **Too slow.** If you walk 30 steps after cutting a head without burning its pool, its stump regrows and two new heads rise in the nearest unburned pools beside it. A pool that already has a head keeps it.
- **The trick.** A burned pool's brazier stays lit (SYSTEMS §2: braziers stay lit), and a lit brazier relights your torch. So the edge pools are reachable from F, and the corners are reachable from an edge brazier you've already lit. Nobody says this. Kleon only says "Every fire was a spark once," after your first failed corner.
- **No dead ends.** You can always relight at F or at any burned brazier. The worst case is more battles, never a lock.
- **The golden head.** Once P1–P8 are burned, the golden head rises from P9 and Karkitox bursts from the reeds. Kleon drops the torch and comes to stand beside you: a multi battle, you and Kleon against the golden head and the crab. Then push the column drum R onto P9 with the Girdle. The immortal head is buried, as in the myth.

**A clean solution (Hero).** Cut P4, burn from F (6). Cut P1, burn from B4 (6). Cut P6, burn from B4 (6). Cut P7, burn from F (6). Cut P5, burn from F (6). Cut P3 and P8 and burn each from B5 (6). Cut P2, burn from F (8). Other orders work. A player who goes for a corner first gets two extra heads and learns the rule.

**Engine.**
- The heads are objects with hide flags. The pool states are nine two-bit states in `IchorSave.epics.lernaPools` (§12, POSTGAME §6). The braziers use `IchorSave.litBraziers` (SYSTEMS §14).
- The carried flame is SYSTEMS §2's step counter in `VAR_TEMP_2` and `_3`.
- The final fight: `setwildbattle SPECIES_LERNATHAN, 70, ITEM_NONE, SPECIES_KARKITOX, 70` (`asm/macros/event.inc`, line 1632, which already takes a second species), started as a player-plus-partner battle (`MULTI_BATTLE_2_VS_WILD`, `src/battle_setup.c` line 357) with Kleon as the partner.
- **Low–Medium.** **Fallback:** a fixed five-pool version.

**Bosses.**

| Who | Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|---|
| Each head | Trilerna | 66–68 | Regenerator | — | Dragon Breath, Poison Fang, Scary Face, Dual Chop |
| The golden head | Lernathan | 71 | Regenerator | Black Sludge | Recover, Sludge Bomb, Dragon Rush, Coil |
| Hera's crab | Karkitox | 70 | Shell Armor | Rocky Helmet | Crabhammer, Cross Poison, Swords Dance, Protect |

The crab's job is to be a slow, hard-hitting nuisance that tempts you into wasting turns on it while the golden head Recovers.

**After.** Lernathan, the golden head, can be caught (a guaranteed victory catch, as Labor 1). It is the pseudo-legendary's final form at Lv 70. That is a strong post-game prize, and deliberately so: Olympias raised it, and she lets it go to whoever beat it.

**Wild Pokémon** (the Springs, Lv 58–62):

| Time | Species |
|---|---|
| Day | Karkipool 20%, Karkitox 10%, Lernip 5%, Ampelix 15%, Ophidrop 15%, Narcibulb 15%, Halcyling 20% |
| Rain (any time) | Lernip 15%, Trilerna 5%, and the rest as Day |

**Rewards.**
- The Golden Tooth (trophy) → Hera Favor +5.
- **Hydra** placed (SYSTEMS §8). Proposed: **Cancer** too, if not yet placed (§13).
- Olympias: "It doesn't count." No prize from her. Kleon gives you his share instead: an Ability Capsule.
- Marsh items: TM Sludge Bomb, Max Revive, Black Sludge (hidden, in the reeds).

**Music.** *The Labor* (Pair 1 variant). *The Hydra*, a battle cue in 9/8 (zeibekiko) with a two-note aulos figure that doubles every time the melody repeats.

**Scene: the discount.**

[The Heraion. You set the golden tooth in its niche. Olympias looks at it, then at Kleon, who is soot to the eyebrows.]
```text
OLYMPIAS: Who held the fire?

KLEON: I did. In the rain. For an hour.

OLYMPIAS: Then you had help, {PLAYER}. It doesn't count.

KLEON: What? It was a hydra! You said she was sweet!

OLYMPIAS: She is. And it doesn't count. Herakles had help too. Same rule.

KLEON: …Then don't count mine either. It was my fire. Not my Labor.

OLYMPIAS: Hm.

OLYMPIAS: Noted.
```

---

### Labor 3. The Ceryneian Hind: *track it, for days*

> *A hind with golden horns and bronze hooves, sacred to Artemis. Herakles followed it for a whole year rather than harm it, and caught it at last as it forded the river Ladon* (Apollodorus 2.5.3; Callimachus, *Hymn to Artemis* 98–109).

**Play.** This is a chase across real days and across all of Aethos. Each day the Hind is seen in one place. Find her, and she bolts, leaving golden hoofprints that lead toward where she'll be tomorrow. Four sightings, four days. On the fifth dawn she drinks at the Ladon ford in Arkadia, and that is the only place she can be caught. She flees at once unless you can stop her running.

This is not the Artemis temple trial (SYSTEMS §12), which is a stealth puzzle in one grove. This is a world-scale hunt.

**Maps.** One new map, **the Ladon Ford** (28×30), off Arkadia's cypress forest. The sightings use existing main-game maps.

| Day | Where she's seen | The omen that morning | What you find |
|---|---|---|---|
| 1 | Kallisto's grove, Arkadia, at dawn | Kallisto tells you herself | She bolts. Her prints lead east. |
| 2 | Thyrsa's vineyards, at noon | "A deer stripped a whole vine in Thyrsa. Golden, they say." | Prints lead to the Ascent |
| 3 | The Ascent's snowfields, at dusk | "Snow on the Ascent, and a gold deer in it." | She has gone where the north wind lives. Kleon, tracking alone, loses her in a minute and catches up with you at the ford. |
| 4 | Eleusa's fields, at night | "Something with gold feet in the wheat." | Prints lead west, to the river |
| 5 | The Ladon Ford, at dawn | — | She drinks. This is the catch. |

**Rules.**
- **One sighting per real day.** The daily event (`DoDailyEvents`, `src/clock.c`) advances `IchorSave.epics.laborStep[2]` only if the player found the previous day's sighting.
- **Missed a day?** She waits. Each sighting persists until found, then the next unlocks at the next daily reset. A player can take a week; nothing is lost.
- **Time of day.** Each sighting is only at its hour (dawn 6–10, noon 10–19, dusk 19–20, night 20–6). Optional content may use time (SYSTEMS principle 2). A xenia host's bed (SYSTEMS §10), the trireme's bunk (ODYSSEY §2) or Melitta's lined cloak (ODYSSEY §6.11) can move the clock forward.
- **The prints** are footprint metatiles, the same ones theoxenia E8 uses, laid as a trail across each map.
- **The catch.** At the ford she flees on her first turn, as roaming legendaries do, **unless she is trapped**: Mean Look, Block, Spider Web, Jaw Lock, Anchor Shot, Spirit Shackle, Thousand Waves, Arena Trap or Shadow Tag. Kallisto's hint: "Hounds don't catch her. Hounds corner her."
- **Don't harm her** is the myth, but Ichor doesn't punish it. If she faints, she is back at the ford the next dawn.

**Engine.**
- Sightings are hide flags set by the daily event. Prints are metatile swaps in each map's `ON_LOAD`.
- The ford battle is a small special, `Ichor_StartHindBattle`, modeled on the roamer setup in `src/battle_setup.c`, so the battle carries `BATTLE_TYPE_ROAMER` (`include/constants/battle.h`, line 111) and she flees as a roamer does.
- **Low–Medium.**

**Boss: the Hind.**

| Species | Lv | Ability | Item | Moves | Notes |
|---|---|---|---|---|---|
| Xerneas | 72 | Fairy Aura | — | Geomancy, Moonblast, Aromatherapy, Megahorn | Flees on turn 1 unless trapped. A legendary, so the bible's casting stays. |

**After the catch.** Kallisto, Artemis's Hierophant, is waiting on the far bank. In myth Artemis confronted Herakles, and let him go once he promised to bring the hind back.
- Kallisto asks you to open the ball and let the Hind choose. She steps out, looks up at the hills for a long moment, and comes back to stand beside you.
- The Hind is yours. Artemis Favor +10.

**Conflict with SYSTEMS, and the fix.** SYSTEMS §3 makes Artemis's gift III "the golden-horned deer". The myth gives both a place:
- Callimachus says Artemis found **five** golden-horned hinds. She caught four to draw her chariot, and the fifth ran away to Ceryneia.
- **This Labor's Hind is the fifth one,** Xerneas.
- **Artemis's gift III becomes one of the four chariot hinds,** a different species (suggested: Hisuian Wyrdeer, as an ancient-era deer). This is decision LB4, a one-line change to SYSTEMS §3.

**Wild Pokémon** (the Ladon Ford, Lv 58–62):

| Time | Species |
|---|---|
| Dawn and day | Skylaps 5%, Lykopup 20%, Raknit 15%, Hyphantis 10%, Arkoby 15%, Chelonet 15%, Glaukoin 20%; fishing: Narkeray, Ketofry |
| Night | Kerdovix 5%, Lykanax 15%, Starkos 10%, Amnoze 15%, Glaukoin 20%, Arkoby 20%, Obolorn 15% |

**Rewards.**
- A golden antler tine she shed (trophy) → Hera Favor +5.
- Xerneas.
- Olympias: TM Agility.
- Ford items: a Moon Stone, a Star Piece, and a hidden Leftovers under the ford stones.

**Music.** *The Hind*: a solo kithara theme in Lydian that plays only at sightings. It is fast and light, and stops dead when she bolts.

**Scene: the ford.**

[Dawn. Mist on the river. The Hind stands knee-deep, drinking. Kallisto sits on a stone on the far bank, bow across her knees, not drawn.]
```text
KALLISTO: Four days. Herakles took a year. You're quicker, or she's tired.

KALLISTO: She's never been caught. Hounds can't. Arrows won't.

KALLISTO: Hounds corner her. Think like a hound that doesn't bite.
```
[After the catch.]
```text
KALLISTO: Now open it. Here. In front of her river.

KALLISTO: My goddess caught four of them for her chariot. This one ran.

KALLISTO: If she runs now, she runs. Open it.
```
[The Hind steps out. She looks at the hills a long time. Then she walks back and stands at your side.]
```text
KALLISTO: …Huh.

KALLISTO: She's never chosen anyone. Look after her. She'll know if you don't.
```
[Kleon wades across the ford behind you, soaked to the knees. Kallisto stands up. He stops.]
```text
KALLISTO: Kleon of Lakonia.

KLEON: Hierophant.

KALLISTO: I fought you under the new moon. Six to nothing. I didn't look at you once.

KALLISTO: I'd been told to be merciless that night. A reading. It was revised.

KALLISTO: Your Keeper's little hook was on it. Alethea showed me.

KALLISTO: I'm sorry. I should have looked at you.

KLEON: …

KLEON: I'd have lost anyway. You're very good.

KALLISTO: Yes. But you'd have lost to me. Not to a forgery.

KALLISTO: Come to Arkadia at the full moon. I'll look the whole time.
```
This is STORY §3's hook ("Kallisto apologizes to him during the Golden Hind"). After the Labors, Kallisto's Arkadia temple offers Kleon's player a full-moon rematch with him as your partner, once.

---

### Labor 4. The Erymanthian Boar: *lure it into the snow*

> *Herakles drove the boar into deep snow on Mount Erymanthos, where it stuck, and caught it in a net* (Apollodorus 2.5.4).

**Play.** A huge Kaprodon has been tearing up Arkadia's upland farms. It charges anything it sees in a straight line, and stops only when it hits something. Above the tree line on Mount Erymanthos, the snow lies in deep drifts. Stand where its charge will end in a drift. Three drifts tire it out. Atalanta is up there too, hunting the same boar, as she hunted the Calydonian boar in her own story, and she'd rather work with you than race you.

**Maps.**

| Map | Size | Notes |
|---|---|---|
| Erymanthos Slopes | 30×60 | A new mountain route from Arkadia. Two forced grass bands (alpine meadow), then scree. A shepherd's summer hut (rest). |
| The Snowfield | 40×40 | The arena: open snow, rocks, three drift hollows |

```text
  THE SNOWFIELD (40x40)
       # = rock (the boar stops, stunned 1 turn)   D = deep drift   ^ = Atalanta
 +--------------------------------------------------------+
 |  # #        .  .  .  .  .  .  .         # #   [cairn]  |
 |     .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .     |
 |  .  D1 (hollow)  .  .  .  #  .  .  .  .  .  D2  .  .   |
 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .     |
 |  .  .  .  #  .  .  B (boar's wallow)  .  .  .  #  .    |
 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .     |
 |  ^ .  .  .  .  .  .  .  .  .  .  .  D3 (hollow)  .  .  |
 |  #  .  .  .  .  .  .  #  .  .  .  .  .  .  .  .  .  #  |
 +------------------[ down to the Slopes ]----------------+
```

**Rules.**
- **The charge.** The boar wanders until it sees you in a straight line within 7 tiles. It paws twice (a warning), then charges along that line until it hits something.
  - **Rock:** stunned for a moment, then it turns.
  - **You:** you are knocked back 3 tiles and take a wild battle with one of its piglets (Kaplet, Lv 62). Then it resets.
  - **A drift:** stuck for 6 seconds, then it struggles out, tired.
- **Three drifts.** After a charge ends in each of D1, D2 and D3 (in any order), it's exhausted. Talk to it to start the battle.
- **The trick** is standing so you are in line with the boar *and* a drift is between you, then stepping aside after the paw warning. Atalanta shows the first one, then lets you do the rest.
- **Kleon** falls into D2 at the start, and Atalanta pulls him out by the collar.

**Engine.**
- The charge reuses LABYRINTH's Asterion charge (`src/ichor_asterion.c`: sight, paw, charge, stun), without his hearing or patrols.
- The drifts are a new metatile behavior, `MB_ICHOR_DRIFT`, which the charge treats as a stop that sets a "stuck" state.
- **Medium,** and it depends on Asterion's AI being built. **Fallback:** three scripted charge lanes, one per drift, each triggered by standing on a marked rock.

**Boss: the Boar of Erymanthos.**

| Species | Lv | Ability | Item | Moves | Notes |
|---|---|---|---|---|---|
| Kaprodon | 72 | Thick Fat | — | Head Smash, Earthquake, Night Slash, Thrash | Starts with −1 Speed (tired) and +1 Attack (angry). A guaranteed victory catch. |

**Atalanta** (no battle here; you meet her again as a Frontier Brain, POSTGAME §3):
- She gives you the net she brought: an **Atalanta's Net** key item. In Labor 10, when the gadflies scatter the herd, cattle bolt only 3 tiles instead of all the way back to the pasture.
- She mentions Olympia: "They want me to run their apple course. I'll go, once this pig's done."

**Wild Pokémon.**

| Map | Levels | Species |
|---|---|---|
| Erymanthos Slopes | 59–63 | Kaplet 20%, Kaprodon 5%, Chelonet 10%, Niflake 15%, Kryopuff 15%, Spalunk 15%, Basilops 10%, Pagoshard 10% |
| The Snowfield | 60–64 | Kryopuff 20%, Niflake 20%, Pagoshard 20%, Kaplet 15%, Kaprodon 10%, Krystolos 5%, Chionyad 5%, Borapteryx 5% |

**Rewards.**
- A tusk (trophy) → Hera Favor +5, Artemis Favor +5.
- Kaprodon.
- Atalanta's Net.
- Olympias: TM Earthquake.
- Items: a Never-Melt Ice, Ice Stone, PP Up, and a hidden Max Revive in the summer hut's woodpile.

**Music.** *The Labor* (Pair 2). *The Boar*, a short sting that plays on each paw warning: two thumps.

**Scene: Atalanta.**

[The Snowfield's edge. A woman in a short hunting chiton crouches by a cairn, watching the boar's wallow. A Starkos sits beside her like a dog.]
```text
ATALANTA: Shh. Don't run at it. Everyone runs at it.

ATALANTA: Your friend ran at it. He's in that drift.

KLEON: [from the drift] I'm fine!

ATALANTA: He's not fine. Watch. It only runs straight.

ATALANTA: You get in line, let it see you, and let the snow do the rest.
```
[She steps into the boar's sight line with D1 between them. It paws twice and charges. She steps aside. The boar ploughs into the drift and sticks.]
```text
ATALANTA: See? Two more. I'll get your friend out.

ATALANTA: Then I'm going to Olympia. Apparently I'm a "Brain" now.

ATALANTA: I don't know what that means. I just run.
```

---

### Labor 5. The Augean Stables: *turn two rivers*

> *King Augeas's stables hadn't been cleaned in thirty years. Herakles turned the rivers Alpheios and Peneios through them and cleaned them in a day, having asked a tenth of the herd as his fee. So Eurystheus refused to count it* (Apollodorus 2.5.5).

**Play.** A short walk from Olympia, King Augeas's stable yard is so foul that a heap of Garbodor lives in it. Two rivers run past the farm in old channels that the farm has blocked, rerouted and forgotten over thirty years. Every relic you own opens part of the waterworks: the Hammer breaks a rock dam, the Girdle rolls column drums into side channels, the Labrys turns the old sluice dials, the Sickle cuts the reed beds that choke a channel, and the Horn of Achelous, blown at the confluence, makes the rivers rise. When both rivers reach the yard at once, the flood flushes it.

**Maps.**

| Map | Size | Notes |
|---|---|---|
| Augeas's Farm | 50×44 | A new map in Elis, joined to the road out of Olympia. The waterworks puzzle covers the whole map. Forced grass on the river meadows; farmhands as trainers. |
| The Stable Yard | 30×24 | The flooded finale and the Muck's lair |

```text
  AUGEAS'S FARM (50x44): the waterworks
     A = ALPHEIOS (from the east)   P = PENEIOS (from the north)
     h = rock dam (Hammer)  g = drum slot (Girdle)  s = sluice dial (Labrys)
     r = reed choke (Sickle)  H = confluence (Horn)  Y = stable yard

                    P (source)
                    |
              r ----+---- (old ditch, dry) ---- g
                    |                           |
       h ===========s1=====+                    |
       |                   |                    |
  A ---+---- s2 ---- r ----H---- g ---- s3 -----+---> to Y
  (src)       \            |
               +-- (leak to the pasture: ends in a pond, a dead end with a Big Pearl)
```

**Rules.**
- **The flow** traces from each source along channel tiles. It turns at sluice dials by their setting and stops at dams, drums, reed chokes and dry ditches.
- **Both** rivers must reach Y, then you blow the Horn at H. Both flows at once, with the Horn, is the flush.
- **Every relic matters once.** One of each obstacle stands on the true path. There are decoys: a second rock dam whose breaking only floods the pasture, and a drum slot that blocks the Peneios if filled.
- **Undo.** Everything can be undone (re-roll a drum, re-set a dial), except breaking a dam, and no dam break locks the puzzle.
- **A farmhand** who has worked these ditches all his life stands at the confluence. Ask him and he gives one hint per visit, in order.

**Engine.**
- The flow uses SYSTEMS §12's beam-trace special (`src/ichor_beam.c`), generalized: the "beam" is water, the "mirrors" are sluice dials, and the walker swaps channel metatiles from dry to wet along the path. Low–Medium.
- The relic obstacles are the existing obstacle scripts (SYSTEMS §1).
- Dials are var bits (`IchorSave.epics.laborStep[4]`).

**Boss: the Muck.** When the flood hits the yard, the Garbodor heap boils up.
1. A wild double: Garbodor and Garbodor (Lv 70).
2. Then the Muck itself: a giant Garbodor (Lv 73, totem boost +1 Defense and +1 Sp. Def; Stench, Black Sludge; Gunk Shot, Drain Punch, Toxic Spikes, Explosion).

**Augeas pays.** Before you start, Augeas offers a tenth of his herd if it's done in a day.
- **Say yes,** and he sends the herd's worth after you: Moomoo Milk ×10, a Lucky Egg and 20,000 money.
- **Say no,** and he sends it anyway: "A king doesn't take charity."
- Either way, Olympias: "You were paid. It doesn't count."

**Wild Pokémon** (Augeas's Farm, Lv 60–64). Garbodor and its kind appear only in the yard's scripted battles:

| Time | Species |
|---|---|
| Day | Onotis 15%, Midonos 5%, Spalunk 15%, Stachyss 15%, Kaplet 15%, Galekit 15%, Lophops 10%, Ampelix 10% |
| Fishing | Ketofry, Karkipool, Narcibulb (rare) |

**Rewards.**
- A stable door-pin (trophy) → Hera Favor +5, and Hestia Favor +5 ("a clean house").
- Augeas's payment.
- Olympias: nothing ("It doesn't count").
- Farm items: TM Gunk Shot, a Big Pearl (the pasture dead end), Black Sludge.
- **Pindar's line.** In Pindar, Herakles founded the Olympic Games after this Labor. Paionios mentions it at the metope: "He cleaned the stables, then he started the Games. Explains the smell at the opening ceremony."

**Music.** *The Labor* (Pair 3). *The Waterworks*: the farm theme gains a layer of running-water percussion for each flow that reaches the yard.

**Scene: Hyperion with a shovel** (STORY §3: "Hyperion and his ex-grunts clean the Augean Stables by feel").

[The stable yard, before the flood. A huge bare-armed man with clouded eyes stands knee-deep in muck, shoveling steadily, his face turned up to the sun. Petros and Amathos, the slice's two grunts, shovel beside him. Talos lent them out from the forge.]
```text
PETROS: Boss. It's the Archon.

HYPERION: Is it? Good. Grab a shovel, Archon. Or don't. Your choice now.

HYPERION: Talos says I'm to "learn the rest". This is the rest, apparently.

HYPERION: I don't need eyes for this. I need a shovel.

AMATHOS: He's faster than us. He just goes by the smell.

HYPERION: The farmhand says there's a smarter way. Rivers. Go and be smart.

HYPERION: We'll keep shoveling till it gets here. It's good, this. It's warm.
```
[Kleon arrives at the gate, sees who it is, and stops. He doesn't say anything. He picks up a spare shovel and starts on the far stall.]
```text
HYPERION: Who's that? New fellow?

KLEON: …Nobody. Shovel.

HYPERION: Hah. Fair.
```
[After the flood. All four of them are sitting on the stable roof, soaked, holding shovels.]
```text
HYPERION: …It got here. I heard it. Like the sea coming in.

KLEON: [quietly, to you] Don't tell him it was me on the Stair. He likes not knowing.
```

---

### Labor 6. The Stymphalian Birds: *flush them, then fight them in the air*

> *Birds with bronze feathers roosted in the marsh at Stymphalos, where no one could walk. Athena gave Herakles bronze rattles that Hephaestus had made. He shook them, the flock rose, and he shot them down* (Apollodorus 2.5.6).

**Play.** Lake Stymphalia's northern reed beds are a marsh you can't cross. Belornis roost in the reeds, and a flushed flock fires bronze feather-darts at the ground where you stand. Hypatia brings you Athena's **krotala**, bronze rattles. Shake them near a roost and that flock takes to the air. Work around the marsh's rocky islands, flushing every roost from a place the darts can't reach. When the last flock rises, the great bird leads them, and you fight it in the sky: only your fliers and floaters can follow.

**Maps.**

| Map | Size | Notes |
|---|---|---|
| Lake Stymphalia | existing | The main game's lake in Lakonia. A new reed-bed entrance appears on its north shore. |
| The Stymphalian Reeds | 40×40 | The marsh: unwalkable mud, rocky islets joined by boardwalks, seven roosts |

```text
  THE STYMPHALIAN REEDS (40x40)
     ~ = mud (impassable)  = = boardwalk  O = rock islet (safe from darts)
     R = roost (7)   x = dart zone when the nearest roost is flushed
 +----------------------------------------------------+
 |  ~ ~ R1 ~ ~ ~ ~ ~ ~ ~ R2 ~ ~ ~ ~ ~ ~ R3 ~ ~ ~ ~ ~  |
 |  ~ x x x ~ ~ O ~ ~ x x x ~ ~ ~ ~ x x x ~ ~ O ~ ~  |
 |  ~ ~ = = = = O = = = = = = = = = = = = = = O ~ ~  |
 |  ~ ~ = ~ ~ ~ ~ ~ ~ R4 ~ ~ ~ ~ ~ ~ R5 ~ ~ ~ = ~ ~  |
 |  ~ ~ O ~ ~ ~ ~ ~ x x x ~ ~ ~ ~ x x x ~ ~ ~ O ~ ~  |
 |  ~ ~ = = = = = = = = = = O = = = = = = = = = ~ ~  |
 |  ~ ~ ~ R6 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ R7 ~ ~ ~ ~  |
 |  ~ ~ ~ x x x ~ ~ ~ ~ ~ O ~ ~ ~ ~ ~ x x x ~ ~ ~ ~  |
 +-----------------[ to the lake shore ]--------------+
```

**Rules.**
- **The krotala** is a key item, used from the Relic Ring (SYSTEMS §1) or the Bag. Shaking it flushes every roost within **4 tiles**.
- **Darts.** A flushed flock circles for 20 seconds and rains darts on its dart zone (x). Standing in a dart zone while it's raining sends you back to the last islet you stood on and starts a wild battle against two Chalkip (Lv 68). Islets are always safe.
- **The order matters,** because some boardwalks run through dart zones. Flush R4 from the middle islet before you walk under it.
- **Kleon** won't go in. He holds the boardwalk's end, and admits why. (Scene below.)
- **The sky battle.** When the seventh roost is flushed, the flock leader comes down for you. It's a **Sky Battle**: only Flying-types and Pokémon with Levitate can take part (`B_FLAG_SKY_BATTLE`, which is in the expansion). If you have none, the leader lands and fights you on the ground: "Fine. Down here, then."

**Engine.**
- The krotala's field use is a radius check against roost objects. Dart zones are coord events with a timer flag. Low.
- `B_FLAG_SKY_BATTLE` and `B_VAR_SKY_BATTLE` are 0 in `include/config/battle.h` today; give them an `FLAG_ICHOR_` flag and a temp var. Low.

**Boss: the Bronze Flock.**

| Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|
| Belornis (the leader) | 72 | Iron Barbs | Sharp Beak | Brave Bird, Iron Head, Spikes, Roost |
| Belornis | 70 | Skill Link | — | Pin Missile, Drill Peck, Steel Wing, Agility |
| Corviknight | 70 | Pressure | Leftovers | Brave Bird, Body Press, Iron Defense, Roost |

The leader opens alone. The other two come in as it calls them: a 3-Pokémon wild gauntlet, one after another, with no healing between. Each is catchable, and the leader is a guaranteed victory catch.

**Wild Pokémon** (the Reeds, Lv 66–70; you meet them in the boardwalk's shallows only):

| Time | Species |
|---|---|
| Day | Chalkip 25%, Belornis 5%, Galenyon 15%, Halcyling 15%, Karkipool 20%, Narcibulb 10%, Ampelix 10% |
| Fishing | Lernip (rare, rain), Karkitox, Narkeray, Ketofry |

**Rewards.**
- A bronze feather (trophy) → Hera Favor +5, Athena Favor +5, Hephaestus Favor +5.
- The krotala, which stays useful: it flushes hidden flying Pokémon from tall grass on any map, once a day (a guaranteed Flying-type encounter).
- Olympias: TM Brave Bird.
- Items: Sharp Beak, Metal Coat, a hidden Gold Stater on R6's islet.

**Music.** *The Reeds*: no melody, only wind, a reed flute and the clatter of the krotala, which plays as a rhythm sound effect when you shake it. *Sky Battle*, an airy 7/8 battle theme.

**Scene: Hypatia and the krotala.** Hypatia holds Athena's seat in the Pantheon.

[The lake shore. Hypatia sits on a crate, reading. She doesn't look up.]
```text
HYPATIA: You'll want these. Bronze rattles. Krotala.

HYPATIA: Hephaestus made them. Athena handed them over. I'm the courier.

HYPATIA: Shake them near a roost and the birds go up.

HYPATIA: Then they come down. That's the part to think about.

HYPATIA: Stand on rock. Feathers don't go through rock. Mostly.
```
[Kleon, at the boardwalk's end.]
```text
KLEON: I'll… hold the end. Of the boardwalk. Someone should.

KLEON: …Fine. I don't like birds.

KLEON: A crow took my bread when I was six. In front of the whole school.

KLEON: Lakonians aren't afraid of anything. So I've been lying since I was six.

KLEON: Go on. I'll hold the end. It's a very important end.
```

---

### Labor 7. The Cretan Bull: *leap it, then ride it*

> *Poseidon sent King Minos a white bull from the sea. Herakles caught it on Crete and brought it to the mainland; some say he rode it across the sea. It was the Minotaur's sire* (Apollodorus 2.5.7; Pausanias 1.27.10).

**Play.** Asterion's father has come back out of the sea, and he is tearing up Knossa's shore. The Labyrinth's bull-leaping (LABYRINTH §3) is how Minoans met a bull. Here it's how you tire one: leap him three times on the beach while Asterion, who loves him, keeps him calm. Then ride him. The bull swims, and you cross the open sea on his back, from Amnisos to the mainland, fighting the currents. Kleon, who tried to kill Asterion at Knossa, has to ask Asterion for help.

**Maps.**

| Map | Size | Notes |
|---|---|---|
| The Bull's Shore | 36×24 | A new beach below the Bronze Heel (LABYRINTH §2). The leaping ground. |
| The Bull's Crossing | 20×90 | A new sea strip from Amnisos to the mainland: currents, rocks and one Poseidon shrine on a skerry (a rest point) |

**Steps.**
1. **Ariadne** sends word: "Our brother's father is back. Bring your sandals."
2. **Asterion** leads you down from the palace court (LABYRINTH §10) to the shore. He goes ahead and stands near the white bull, and the bull's charges get slower.
3. **Leap ×3.** It is the bull-leaping timing task (`src/ichor_bull_leap.c`), with a narrower window than the palace's: the white bull is faster.
   - **Asterion widens it** by 2 frames ("he's helping"), as in LABYRINTH §10.
   - **A miss** knocks you down; get up and go again. No battle.
4. **The battle.** The tired bull. A guaranteed victory catch, or not: the next step works either way, because Asterion's father won't be ridden by someone he hasn't tested.
5. **The ride.** Climb on his back. The bull swims north across the Bull's Crossing: the dolphin surf state (SYSTEMS §1, Poseidon's Conch) with a bull sprite and a faster speed.
   - Currents (`MB_*_CURRENT`) push you sideways, and rocks stop you.
   - Wild encounters are off. The danger is drifting onto the reefs, which sends you back to the last skerry.
6. **Landfall** at the mainland's harbor. Olympias is there, which surprises everyone.

**Engine.**
- Bull-leaping: LABYRINTH's `src/ichor_bull_leap.c`, with a per-encounter window parameter. Low.
- The ride: the surfing state with a bull graphics id. Currents are vanilla metatile behaviors (`MB_EASTWARD_CURRENT` and the rest, `include/constants/metatile_behaviors.h` lines 85–88). Low–Medium.

**Boss: the Bull from the Sea.**

| Species | Lv | Ability | Item | Moves | Notes |
|---|---|---|---|---|---|
| Paldean Tauros (Aqua Breed) | 73 | Cud Chew | — | Wave Crash, Close Combat, Bulk Up, Raging Bull | No Aethos species is Poseidon's white sea-bull; this is a deliberate exception (§5). His hide is described as "sea-foam white". |

**Wild Pokémon** (the Bull's Shore, Lv 62–66):

| Time | Species |
|---|---|
| Day | Karkipool 15%, Galenyon 15%, Telpup 15%, Kolossette 10%, Kolossard 5%, Aphrell 15%, Halcyling 15%, Dakrock 10% |

**Rewards.**
- A hank of sea-white hair (trophy) → Hera Favor +5, Poseidon Favor +10.
- The bull (if caught).
- Olympias: TM Close Combat.
- The skerry shrine on the crossing: a sea-gift offering point, and a Big Pearl.

**Music.** *Bull-leaping* (LABYRINTH §9). *The Crossing*: the Ichor main theme in Mixolydian, played on a galloping frame drum.

**Scene: Kleon and Asterion.**

[The palace court. Asterion lies in the sun. He lifts his head when Kleon comes in behind you, and his breathing changes.]
```text
KLEON: …He remembers me.

KLEON: Course he does. I came at him with fire. In his own house.

KLEON: I was going to be famous for killing him.
```
[Kleon walks forward and kneels about three tiles away. He puts his hands on the ground, palms up.]
```text
KLEON: I'm sorry. Nobody wrote that one for me. I'm saying it anyway.

KLEON: Your father's on the beach. He's in trouble. We need your help.
```
[A long pause. Asterion gets up, walks past Kleon, and bumps him with one horn, not hard. Then he heads for the shore path.]
```text
ARIADNE: That's yes. Or a threat. With him it's sometimes both.

KLEON: I'll take it.
```

---

### Labor 8. The Mares of Diomedes: *feed them*

> *King Diomedes of Thrace fed his mares on men. Herakles drove them off, fed the king to his own horses, and they grew calm* (Apollodorus 2.5.8).

**Play.** Across the northern sea in Thrace, King Diomedes starves his four mares to keep them savage, and turns them loose on travelers. You sail there on your own trireme (ODYSSEY §2). In his stable at night, each mare paces her stall. Each one is hungry for something different, and how she paces tells you what. Feed each the right fruit and she calms. Feed her the wrong one and she kicks the stall door down. When all four are calm, Diomedes comes for you, and his own mares chase him into the sea.

**Maps.** Thrace shares a new **steppe** tileset with Themiskyra (Labor 9).

| Map | Size | Notes |
|---|---|---|
| Abdera | 30×26 | A small Thracian port town: Asclepeion, Agora (Thracian goods), a xenia host, the Pithos. Its founding story is the myth's sad one, told on a stele. |
| The Bistonian Plain | 40×60 | A route of long grass and burial mounds. Two forced grass bands, Bistonian soldiers as trainers. |
| Diomedes's Stable | 24×16 | The night stable, four stalls |
| Diomedes's Yard | 30×20 | The finale, ending at the shore |

**Rules: the feeding.**
- Each mare has a fixed nature, and you read it from how she behaves. Feed her a berry of the flavor that nature likes. The Gen 3 rule is that each nature likes one flavor and dislikes another; Ichor uses the expansion's existing table, the one confusion berries read.
- The bag picker shows only berries (SYSTEMS §3's offering picker, filtered).

| Mare | Her stall | Nature | Likes | So feed her |
|---|---|---|---|---|
| **Podarge** ("swift-foot") | "Paces fast. Won't stand still a second." | Hasty | Sweet | Pecha, Mago or another sweet berry |
| **Xanthe** ("golden") | "Rears and kicks at the walls." | Adamant | Spicy | Cheri, Figy or another spicy berry |
| **Deine** ("terrible") | "Stands perfectly still, watching you." | Calm | Bitter | Rawst, Aguav or another bitter berry |
| **Melaina** ("black") | "Lies down. Gets up. Lies down." | Relaxed | Sour | Aspear, Iapapa or another sour berry |

- **A wrong feeding** makes that mare kick her door down: a wild battle with her (Mudsdale, Lv 72). Win, and she's back in her stall, still hungry.
- **A stablehand** you can wake gives one clue per mare: "Podarge was always the quick one. Liked honey cakes, back when she got any."
- **Diomedes's guards** patrol the yard, but the stable is the puzzle, not the yard. Their sight is short and there is plenty of cover.

**The finale.** When all four are calm, Diomedes storms in. Battle. When he loses, he whistles for his mares to kill you. They look at him for a long time. Then all four chase him out through the yard and into the surf. He's a strong swimmer. They're stronger. This is the myth's grim ending, made into something a Pokémon game can show.

**Engine.**
- The flavor test calls the existing nature-to-flavor relation in `src/pokemon.c` (the one berries' confusion effect uses), with the mare's fixed nature. Low.
- The stable is scripts and objects. Low.

**Boss: King Diomedes of the Bistones,** son of Ares.

| Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|
| Mudsdale | 73 | Stamina | Leftovers | High Horsepower, Heavy Slam, Rock Slide, Body Press |
| Borapteryx | 72 | Snow Warning | Never-Melt Ice | Blizzard, Hurricane, Freeze-Dry, Tailwind |
| Lykanax | 72 | Intimidate | — | Throat Chop, Close Combat, Sucker Punch, Jaw Lock |
| Kaprodon | 72 | Reckless | Choice Band | Head Smash, Earthquake, Night Slash, Double-Edge |
| Taurivet | 73 | Flash Fire | — | Flare Blitz, Heavy Slam, Shift Gear, Earthquake |
| Hisuian Arcanine | 74 | Rock Head | Charcoal | Head Smash, Flare Blitz, Extreme Speed, Wild Charge |

Boreas, the North Wind, lived in Thrace; that's why Diomedes keeps a Borapteryx.

**After.** The four mares come home with you on the trireme. Podarge, the lead mare, can join your party (Mudsdale, Lv 72, Hasty, Stamina, with Atalanta-fast Speed IVs). The other three go to Olympia, where Olympias "gives them to Hera" by putting them in the Hippodrome's stables.

**Wild Pokémon** (the Bistonian Plain, Lv 62–66). Thrace is outside Aethos, so existing species live here; reconcile with OIKOUMENE.md (POSTGAME §4).

| Time | Species |
|---|---|
| Day | Mudbray 20%, Mudsdale 5%, Hisuian Growlithe 10%, Kryopuff 15%, Lykopup 15%, Bouffalant 10%, Gogoat 15%, Braviary 10% |
| Night | Lykanax 15%, Hisuian Zorua 10%, Mightyena 20%, Noctowl 20%, Spiritomb 5% (burial mounds), Kalyptor 15%, Gelasable 15% |

**Rewards.**
- A bronze bit from Diomedes's bridle (trophy) → Hera Favor +5, Ares Favor +5 (Ares was Diomedes's father, and likes a fight).
- Podarge.
- Olympias: TM High Horsepower.
- Abdera opens as a port and a Wings landing point.

**Music.** *Thrace*: a new town and route theme in Phrygian 9/8, on a droning bagpipe-like aulos. *The Stable*, almost silent: hoof shuffles and breathing.

**Scene: the end of Diomedes.**

[The yard. Diomedes's last Pokémon falls. He puts two fingers in his mouth and whistles.]
```text
DIOMEDES: Podarge! Xanthe! Here! Eat!
```
[The four mares walk out of the stable. They stop. They look at you. Then they look at him.]
```text
DIOMEDES: …What are you looking at? Eat! I said eat!

DIOMEDES: I've kept you hungry for ten years for exactly this!
```
[Podarge lays her ears flat. The other three do the same. Diomedes takes one step back. Then he runs, and they go after him, through the gate and down the shingle and into the sea.]
```text
STABLEHAND: He's a strong swimmer.

STABLEHAND: They're stronger. They'll let him off at the point. Probably.

STABLEHAND: They've never had a full stomach before. Thank you.
```

---

### Labor 9. Hippolyta's War-Belt: *find the disguised goddess*

> *Queen Hippolyta of the Amazons was willing to give Herakles her war-belt. But Hera, disguised as an Amazon, told the camp he meant to carry off their queen, and the Amazons attacked* (Apollodorus 2.5.9).

**Naming.** SYSTEMS's decision D2 notes that the game already has a Girdle of Herakles (the Strength relic). This Labor's prize is **Hippolyta's War-Belt**, as SYSTEMS proposes. The Greek *zoster* is a soldier's belt, so "war-belt" is closer than "girdle" anyway.

**Play.** You sail east to Themiskyra on the river Thermodon. Hippolyta, Ares's daughter, receives you as a guest. She'll give you her belt if you beat her, honorably, at the next dawn. But by evening, someone in the camp is whispering that you've come to carry her off. One of the warriors isn't an Amazon. She's a goddess, and she has no shadow. Find her before the camp turns on you. Each wrong accusation, and each night that passes, makes the camp angrier.

This is theoxenia's tells used in reverse: for the first time, the disguised god is the one making trouble.

**Maps.**

| Map | Size | Notes |
|---|---|---|
| The Thermodon Road | 30×56 | A river route from the trireme's landing: long grass, Amazon scouts as trainers, two forced bands |
| Themiskyra | 44×40 | The Amazon camp-town: tents, a horse field, a practice yard, an Asclepeion tent, an Agora of Pontic goods |
| Hippolyta's Hall | 22×16 | A timber hall with Ares's spear set in the floor |

```text
  THEMISKYRA (44x40), the camp
 +------------------------------------------------+
 |  [horse field]  m  m        [HIPPOLYTA'S HALL]  |
 |     a1   a2          .   .   .     a3           |
 |  .  .  .  .  [cook fires]  .  .  .  .  .  a4    |
 |  [practice yard]   a5   .   .  [archery]  a6    |
 |    a7     .   .   .  [well]  .   .   .          |
 |  [Asclepeion tent]   a8    [Agora]    a9   a10  |
 |  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .    |
 |  [your guest tent]          [gate] --> Thermodon Road
 +------------------------------------------------+
   a1-a10: the ten warriors who can be accused. One is the goddess.
```

**Rules.**
- **The tells** are SYSTEMS §10's:
  1. **No shadow.** Every object casts one, except a disguised god.
  2. **Your follower bows** within 3 tiles of her.
  3. **A detail that doesn't fit.** She wears a peacock-eye brooch, Hera's bird, that no Amazon would.
  4. **The Augur's Eye** says "Something here is watching you."
- **The goddess moves.** She stands in a different one of the ten spots each in-game hour, so a player who stands still can't just wait for her.
- **The tension meter** (0–6), shown as campfire smoke rising over the hall:
  - +1 for each wrong accusation;
  - +1 for each in-game night that passes before you find her;
  - +1 if Kleon is left alone with the rumor (scene below).
  - At 6, the camp attacks: a gauntlet of six Amazon battles, back to back, with Hippolyta's healer patching you between them. Survive it, and Hippolyta calls them off. You can still find the goddess afterward. Fail forward.
- **Accusing.** Talk to a warrior and choose "YOU'RE NOT AN AMAZON." The wrong ones are insulted, and some challenge you to a battle.
- **Found her.** She stands, taller. She doesn't give her name, and doesn't have to.

**The scene that matters.** Kleon has crewed your trireme. He hears the rumor first, from a warrior at the well, and comes to you furious that Hippolyta means to trap you.
- **If you calm him** ("SHE'S A GUEST-FRIEND"), he cools.
- **If you agree with him,** tension +1, and he goes to shout at the hall. You find him being held back by two Amazons.
- **Either way,** this is Kleon at his old worst for one minute: Hera's rumor works on proud men. He's ashamed of it afterward.

**Engine.**
- The no-shadow per-object opt-out and the follower bow are already specified for theoxenia (SYSTEMS §10, Engine: `OW_OBJECT_VANILLA_SHADOWS`, `src/follower_helper.c`).
- The goddess's hourly position is a hide-flag set chosen in the map's `ON_LOAD` from the time of day.
- The tension meter is `IchorSave.epics.laborStep[8]`.
- **Low.**

**Boss: Queen Hippolyta,** at dawn, in the practice yard.

| Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|
| Hoplektor | 75 | Guts | Flame Orb | Close Combat, Brave Bird, No Retreat, Wide Guard |
| Kourodin | 75 | Punk Rock | Throat Spray | Boomburst, Iron Defense, Body Press, Sacred Sword |
| Dorydrake | 75 | Defiant | Life Orb | Dragon Dance, Outrage, Close Combat, Earthquake |
| Lykanax | 75 | Intimidate | — | Jaw Lock, Close Combat, Throat Chop, Sucker Punch |
| Hisuian Braviary | 75 | Sheer Force | Choice Specs | Esper Wing, Hurricane, Heat Wave, Psychic |
| Hisuian Decidueye | 77 | Scrappy | Expert Belt | Triple Arrows, Leaf Blade, Brave Bird, Swords Dance |

The Amazons were Ares's daughters and mounted archers. If the dex's decision D8 adds Shield Clash, Kourodin uses it instead of Boomburst.

**After.** Hippolyta gives you the War-Belt. Then she says she's going to Olympia: "If they're running games, someone should run them properly." She becomes the Olympiad's fifth Brain (POSTGAME §3).

**Wild Pokémon** (the Thermodon Road, Lv 64–68). Outside Aethos, as Thrace.

| Time | Species |
|---|---|
| Day | Rapidash 10%, Ponyta 15%, Hoplomex 15%, Basilops 15%, Braviary 10%, Hisuian Braviary 5%, Tauros 10%, Gogoat 20% |
| Fishing | Basculin, Hisuian Qwilfish, Kynoketos (rare) |

**Rewards.**
- **Hippolyta's War-Belt** (trophy) → Hera Favor +5, Ares Favor +10.
- Olympias: TM Bulk Up.
- Themiskyra's Agora sells the Expert Belt and the Muscle Band.
- Themiskyra opens as a port and Wings landing point. The Caucasus crag (Labor 11) is reachable from its harbor.

**Music.** *Themiskyra*: a horse-gait 5/8 on frame drums and a low aulos. *Tension*: as the meter climbs, the camp theme loses its melody, one instrument at a time.

**Scene: the unmasking.**

[You accuse the right warrior. She laughs, a low pleasant sound. Then she stands up straighter, and keeps standing up, and the camp goes quiet.]
```text
WARRIOR: Took you long enough. Your friend believed me in a minute.

WARRIOR: Proud men always do. That's what makes them fun.
```
[She looks at you, and the peacock brooch on her shoulder blinks.]
```text
???: My priestess sets you labors. I make them interesting.

???: Herakles never found me, you know. He just fought them all.

???: You looked. That's new.

???: Go on. Win your belt. I'll be watching. I'm always watching.
```
[She is gone. The camp's cook fires burn higher, and somebody, somewhere, laughs with relief.]
```text
HIPPOLYTA: …Was that who I think it was?

HIPPOLYTA: Never mind. Dawn. The practice yard. Bring your best.
```

---

### Labor 10. The Cattle of Geryon: *sail the sun's cup, then drive the herd home*

> *On Erytheia, the red island past the sunset, the three-bodied giant Geryon kept red cattle, guarded by the herdsman Eurytion and the two-headed dog Orthros. Herakles borrowed the Sun's golden cup to sail there, set up the Pillars at the strait on the way, and drove the herd home. Hera's gadfly scattered it in Thrace* (Apollodorus 2.5.10; Stesichorus's *Geryoneis* gives Geryon wings).

**Play.** The red island lies where the sun goes down, beyond any map. The only ship that goes there is the golden cup Helios rides home each night around the edge of the world. At sunset, at Aethos's western cape, you have to get him to lend it to you. On the way you set up the Pillars at the world's edge, two great columns, one on each side of a strait. On Erytheia you beat the two-headed hound and his herdsman, and then Geryon, who is all heads and wings. Then you drive twelve red cattle across the island to the cup. They move away from you, so herding is a matter of angles. Halfway there, Hera's gadflies scatter them.

**Maps.** A new **far west** tileset (red earth, sunset sky, low scrub) is shared with Labor 11's garden.

| Map | Size | Notes |
|---|---|---|
| The Western Cape | 24×20 | A new headland at Aethos's western end, past Kythera's road (POSTGAME §0). Where the cup docks at sunset. |
| The Ocean Stream | 16×80 | A scripted voyage in the cup, west along the edge of the world. No control except steering left or right around floating rocks of light. |
| The Strait of the Pillars | 30×30 | Two headlands. You push a pillar into place on each with the Girdle: a set piece. |
| Erytheia | 50×46 | The red island: Eurytion's hut, Orthros's den, the pasture, the cup's landing |
| Geryon's Pasture | 40×40 | The herding ground and Geryon's crag |

```text
  ERYTHEIA, the herding route (Erytheia + Geryon's Pasture, joined)
     C = a red cow (12)  G = the gate gully  P = the cup's landing  * = gadfly zone
 +--------------------------------------------------------------+
 |  [Geryon's crag]                                             |
 |    C  C     C           ######                               |
 |  C     C   C    C       ######  (rocks)          ~ ~ ~ ~ ~   |
 |      C   C    C            .  .  .  .  .  .  .  ~  P (cup) ~  |
 |   .  .  .  .  .  .  .  ****************  .  .  ~ ~ ~ ~ ~ ~    |
 |   .  .  .  .  .  .  .  * gadfly hollow *  .  .  .  .  .  .   |
 |   ######  .  .  .  .  .****************  .  .  .  ######     |
 |   ######  .  .  G (gully, 2 wide)  .  .  .  .  .  ######     |
 |  [Eurytion's hut]  [Orthros's den]                           |
 +--------------------------------------------------------------+
```

**Steps.**
1. **The cup.** At the Western Cape, at sunset (19:00–20:00), Helios's golden cup touches the shore. Helios, a broad, gold-skinned man at the rim, won't lend it: "Nobody rides the cup." There are three answers.
   - **"I'LL MAKE YOU."** As in the myth, where Herakles drew his bow on the Sun. Helios laughs, admires the nerve, and lends it.
   - **"PLEASE."** He says no. Ask again, and the third time he relents, sighing.
   - **"YOUR CATTLE SEND THEIR REGARDS."** This appears only if you spared his cattle on Thrinakia in the Odyssey (ODYSSEY §6.8). He lends it warmly, and gives you a Heat Rock.
2. **The Ocean Stream.** A night voyage around the edge of the world.
3. **The Pillars.** At the strait, the cup puts in. Two columns lie on the headlands. Push each upright into its socket (the Girdle, with a two-tile run-up). A set piece: when both stand, the sea between them glows, and beyond them a fog bank shows a dark shape on the horizon. That's a seed for Atlantis (POSTGAME §3).
4. **Orthros and Eurytion.** The two-headed hound guards the pasture's gate. Then his master.
5. **Geryon.** On his crag, three heads and six wings. Battle.
6. **The herd.** Twelve red cattle graze in the pasture. Drive them to the cup.
   - **Herding rule:** a cow steps 1 tile directly away from you when you come within 2 tiles of her, unless something blocks her; then she steps sideways.
   - **Twelve must reach the landing.** They funnel through the gully G.
   - **The gadflies.** When the first six are past G, a Yanmega swarm comes out of the hollow (*). Every cow still in the open bolts back to the pasture. Beat the swarm (a wild double, Yanmega and Yanmega) and herd again. With Atalanta's Net (Labor 4), the cattle bolt 3 tiles instead of back to the pasture.
7. **Home.** The cup carries you and the herd back to the Western Cape by dawn. The cattle go to Olympia.

**Engine.**
- The herding uses Labor 1's flee-from-player movement type, with a count trigger on the landing. Medium–Low.
- The cup ride is a scripted sea map with the player in a cup graphics id and forced forward movement, steering only left and right, like a current lane. Low–Medium.
- Helios's sunset docking: `gettimeofday` in the cape's `ON_LOAD`, as LABYRINTH's sun and moon gates do. Low.

**Bosses.**

| Who | Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|---|
| Orthros | Dikyon | 74 | Strong Jaw | — | Fire Fang, Thunder Fang, Double Hit, Crunch. A totem boost of +1 Speed: two heads, twice as quick. |
| Eurytion the herdsman | Taurivet 74, Kaminoo 73, Mudsdale 74, Hierolive 75 | — | — | — | A herdsman's team. Hierolive carries an olive club. |
| Geryon | Hydreigon | 77 | Levitate | — | Draco Meteor, Dark Pulse, Flamethrower, Earth Power. Totem boost +1 Sp. Atk, +1 Sp. Def, +1 Speed: three bodies. A guaranteed victory catch. |

Hydreigon was the bible's Hydra. The dex's Lernathan has that job now, which frees Hydreigon for Geryon, whom Stesichorus gave wings (§5).

**Wild Pokémon.**

| Map | Levels | Species |
|---|---|---|
| Erytheia | 65–69 | Kaminoo 20%, Taurivet 10%, Hymnet 15%, Hymnaria 5%, Torkoal 10%, Hippowdon 10%, Sandaconda 15%, Volcarona 5%, Larvesta 10% |
| Geryon's Pasture | 66–70 | Kaminoo 25%, Taurivet 10%, Yanmega 15%, Yanma 15%, Hisuian Electrode 10%, Heliolisk 15%, Dikyon 5%, Hydreigon (rare, 5%, only after Geryon) |

**Rewards.**
- A red heifer's bell (trophy) → Hera Favor +5, Hestia Favor +5 (the herd's home fire).
- Geryon (Hydreigon), if caught.
- Olympias: TM Draco Meteor.
- **The Pillars of Herakles stand.** The strait is now a place, and beyond it is the way to Atlantis (POSTGAME §3).
- The Western Cape becomes a Wings landing point.

**Music.** *The Ocean Stream*: the Ichor main theme in Lydian, very slow, on a high kithara with no percussion. *Erytheia*: a sunset theme in Mixolydian, 7/8. *Geryon*: a battle theme in three overlapping meters (a stretch: 9/8 over 6/8 over 3/4).

**Scene: Helios at the cape.**

[Sunset. A great golden bowl the size of a house rocks in the shallows, full of light. A man stands at its rim, polishing it with his sleeve.]
```text
HELIOS: No.

HELIOS: Whatever it is, no. Nobody rides the cup.

HELIOS: It's for the night run. West to east, round the edge, every night.

HELIOS: Do you know how long I've done that run? Neither do I.
```
?? I'LL MAKE YOU / PLEASE / (YOUR CATTLE SEND THEIR REGARDS)
```text
> I'LL MAKE YOU:
HELIOS: You'll what?

HELIOS: …Ha! Ha. The last one who said that drew a bow on me.

HELIOS: I liked him too. Get in. Don't touch the rim, it's hot.
```
```text
> YOUR CATTLE SEND THEIR REGARDS:
HELIOS: You're the one. On Thrinakia. Your crew was starving, and you fished.

HELIOS: Get in. And take this. It holds a whole summer, if you ask it nicely.

{PLAYER} received a Heat Rock!
```
**Scene: after ten.**

[The Heraion. Eight trophies in their niches. Two niches hold Olympias's own marks, a tiny carved "no".]
```text
OLYMPIAS: Ten done. Eight count.

OLYMPIAS: The Hydra, you had help. The stables, you were paid.

OLYMPIAS: So two more. The garden at the end of the world.

OLYMPIAS: And the dog at the bottom of it.

KLEON: [from the doorway] She's been planning this since the start.

OLYMPIAS: Since before you were born, Lakonian. Since before Herakles was.
```

---

### Labor 11. The Apples of the Hesperides: *hold up the sky*

> *On the way to the garden at the world's end, Herakles freed Prometheus from Zeus's eagle, and Prometheus told him the trick: let Atlas fetch the apples. Herakles held up the sky while Atlas went. Atlas came back and wanted to leave him holding it forever; Herakles asked him to take it for a moment while he fixed his cloak, and walked away* (Apollodorus 2.5.11).

**Play.** This is two journeys in one Labor.
- **East, to the Caucasus.** On a frozen crag above Themiskyra's sea, Prometheus hangs in chains while a huge Aetarch, Zeus's eagle, tears at him. Drive the eagle off and break the chains. Prometheus, the Titan who gave mortals fire, tells you how to get the apples: "Let my brother fetch them. And don't let him give you the sky to keep."
- **West, to the garden.** Past Erytheia, where it's always evening, the Hesperides tend a tree of golden apples, and the serpent Ladon sleeps around it. Atlas holds up the sky on the ridge above. He offers to fetch the apples if you'll hold the sky. While you hold it, you can't move, and the sky's weight comes down on you as falling stars, battle after battle. Then Atlas comes back with the apples, and tries to leave you holding it.

**Maps.**

| Map | Size | Notes |
|---|---|---|
| The Caucasus Crag | 30×44 | Reached by trireme from Themiskyra. Snow, wind, the chain-rock at the top. It reuses Olympus's snow and crag tiles. |
| The Garden of the Hesperides | 40×40 | Far west tileset in permanent dusk. The tree, Ladon's coils, three nymphs' bowers. |
| Atlas's Ridge | 30×30 | The ridge above the garden. Atlas, very large, under a sky that sags. |

```text
  THE GARDEN OF THE HESPERIDES (40x40): always evening
 +------------------------------------------------+
 |              [ up to ATLAS'S RIDGE ]            |
 |   .  .  .  .  .  .  .  /\  .  .  .  .  .  .    |
 |  [Aigle's bower]     ( TREE )    [Arethousa's]  |
 |   .  .  .  .  .  .  ~LADON~  .  .  .  .  .  .  |
 |   .  .  ,,,,,,,,  ~ coils  ~  ,,,,,,,,  .  .   |
 |   .  .  ,,,,,,,,  ~~~~~~~~~~  ,,,,,,,,  .  .   |  optional grass (Applin)
 |  [Hespere's bower]   .  .  .  .   [spring]  *   |  * hidden: a Lansat Berry by the spring
 |   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  |
 +---------------[ from Erytheia's west shore ]----+
```

**Steps.**
1. **The crag.** Climb through the wind. Gusts at marked tiles push you back 2 tiles unless you wait for the lull (a timing beat). At the top, the eagle. Battle.
2. **Prometheus.** Break his chains with the Labrys (it "cleaves bronze chains", SYSTEMS §1). He tells you the trick, and gives you an ember from the fire he stole.
3. **The garden.** The three Hesperides are trainers. Each fights you, then lets you past: "Father's on the ridge. He'll talk your ear off."
4. **Ladon** sleeps around the tree. You can fight him now (he is catchable after) or leave him asleep. In myth Herakles killed him; in Ichor he's Hera's, and Olympias wants him unhurt. Kleon stays by Ladon as you go up.
5. **Atlas.** He offers the deal.
6. **Holding the sky.** You take the sky. The player sprite holds a pose and can't move. Three falling stars land, one after another: three wild battles in a row.
   - **No Bag, no running:** as with Proteus's test (SYSTEMS §10, E13), fleeing ends the attempt, and you can retry.
   - **The stars** are Minior (Lv 76), then Solrock and Lunatone together (a wild double, Lv 76), then a Clefable (Lv 78). If the Astral type is implemented (dex DECISIONS, "Next"), the last star is an Astral Pokémon instead.
7. **Atlas comes back** with three golden apples, and says he'll take them to Olympias himself. "You keep holding."
8. **The trick.** A choice:
   - **"FIX MY CLOAK FIRST"** is the right answer. Atlas takes the sky back for a moment, and you step away with the apples.
   - **"NO"**: he shrugs, and another star falls (one more battle), and he asks again.
   - **"FINE"**: you hold it for another star, and he asks again.
   - **"YOU'RE TRICKING ME"**: "I am. Is it working?" One more star.
   - The right choice is always there. Prometheus's hint makes it findable.
9. **Atlas laughs.** "Prometheus told you. He always tells."

**Engine.**
- The crag's gusts are coord events on a timer. Low.
- Holding the sky: a "can't move" flag that freezes input (`ScriptContext` locks, as cutscenes do) while three `setwildbattle`s run in sequence, with `B_VAR_NO_BAG_USE`. Low.
- The eagle's fight uses `settotemboost`. Low.

**Bosses.**

| Who | Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|---|
| Zeus's eagle | Aetarch | 76 | Intimidate | — | Supercell Slam, Brave Bird, Roost, Hone Claws. Totem boost +1 Attack, +1 Speed. |
| Ladon | Melodrakon | 78 | Intimidate | Leftovers | Grav Apple, Moonblast, Dragon Tail, Recycle. A multi battle: Kleon fights beside you (`MULTI_BATTLE_2_VS_WILD`). Ladon is a single opponent, so the wild side is Ladon and one of the garden's Applin, Lv 70. A guaranteed victory catch. |

The three Hesperides are trainers of the evening:

| Hesperid | Team | Theme |
|---|---|---|
| Aigle ("radiance") | Psychora 74, Korantha 74, Himerow 74 | Evening light and Fairy |
| Arethousa ("the spring") | Narcisheen 74, Chionyad 74, Dipplin 74 | The garden's spring, and apples |
| Hespere ("evening") | Hymnaria 75, Kalliglyph 75, Hydrapple 75 | Dusk and gold |

**Wild Pokémon.**

| Map | Levels | Species |
|---|---|---|
| The Caucasus Crag | 66–70 | Aetling 15%, Aetarch 5%, Borapteryx 10%, Kryopuff 15%, Krystolos 10%, Mandibuzz 15%, Braviary 15%, Hisuian Avalugg 15% |
| The Garden | 66–70 | Applin 20%, Flapple 10%, Appletun 10%, Dipplin 10%, Korantha 15%, Psychora 15%, Comfey 10%, Melodrakon 5%, Hydrapple 5% |

**Rewards.**
- **A golden apple** (trophy) → Hera Favor +10, Aphrodite Favor +5 (SYSTEMS's Paris amphora seeded this tree, §5 amphora 11).
- **Draco** placed (SYSTEMS §8).
- **Prometheus's Ember**, a key item: Hecate's Torch can now light braziers that need "the first fire" (Labyrinth vaults, a few main-game secrets). It also counts as a carried flame that never dies.
- Ladon, if caught.
- Olympias: TM Moonblast.
- **Athena returns the apples.** In myth, the apples went back to the garden because they belonged there. Here Hypatia comes to the Heraion and takes the trophy apple back west: "They don't keep anywhere else." The niche keeps a golden apple's carved outline.

**Music.** *The Garden*: Lydian, slow, kithara and a soft choir pad, permanent dusk. *Atlas*: one low string under the garden theme, held for as long as you hold the sky.

**Scene: Prometheus.**

[The crag top. The eagle is gone. The Titan hangs in chains against the rock, very tall and very thin, smiling.]
```text
PROMETHEUS: Ah. Somebody who isn't a bird.

PROMETHEUS: Can you do the chains? Thank you. You'd think I'd be used to them.
```
[The Labrys rings on the bronze. The chains fall.]
```text
PROMETHEUS: You want the apples. Everyone who comes this way wants the apples.

PROMETHEUS: My brother Atlas holds the sky over the garden. He'll fetch them.

PROMETHEUS: He'll ask you to hold the sky. Do it. It's only heavy.

PROMETHEUS: But when he comes back, he won't want it again. Nobody would.

PROMETHEUS: So ask him to hold it one moment. While you fix your cloak.

PROMETHEUS: He'll fall for it. He always has. He's a good brother.

PROMETHEUS: We were punished in the open air, he and I. So we kept our voices.

PROMETHEUS: My brothers under the world didn't. If you go down there…

PROMETHEUS: …read their walls. They'll have been writing.
```
[He presses something warm into your hands.]
```text
PROMETHEUS: Here. The first fire. I took it from the gods in a fennel stalk.

PROMETHEUS: It's done more good than harm. Just. Keep it that way.

{PLAYER} received Prometheus's Ember!
```
That last exchange seeds the Katabasis: the imprisoned Titans have lost their voices and speak through inscriptions (UNDERWORLD §4.10).

**Scene: Atlas.**

[The ridge. A giant of a man stands with the sky across his shoulders, a dark blue weight full of stars that sags almost to his head.]
```text
ATLAS: Visitors! I don't get visitors. I get weather.

ATLAS: Apples? My girls grow them. Ladon guards them. I could fetch you some.

ATLAS: I'd need my hands, though. Somebody would have to hold this.

ATLAS: Just for a while. Just for a little while.
```
[Later, with the apples.]
```text
ATLAS: Got them! Three. Lovely.

ATLAS: You know, I'll take them to your priestess myself. I'd like the walk.

ATLAS: You stay. You're doing very well. You're a natural.
```
?? FIX MY CLOAK FIRST / NO / FINE / YOU'RE TRICKING ME
```text
> FIX MY CLOAK FIRST:
ATLAS: Your cloak? …Oh, go on. Give it here. One moment.
```
[He takes the sky back. You step out from under it, holding the apples.]
```text
ATLAS: …Ah.

ATLAS: Prometheus told you. He always tells.

ATLAS: Well. It was nice, having my hands for a bit. Thank you for that.

ATLAS: If you ever go under the world, my father's down there. Iapetos.

ATLAS: Tell him I'm still holding it. He'll want to know.
```
Atlas's message pays off in Tartarus, at Iapetos's cell (UNDERWORLD §4.10).

---

### Labor 12. Kerberos: *bring him up into the light*

> *Hades let Herakles take Cerberus to the upper world, if he could master the hound without weapons. Herakles dragged him up through Tainaron. The hound hated the light. When Eurystheus saw him, he hid in a jar* (Apollodorus 2.5.12).

**Needs:** the Katabasis is complete (UNDERWORLD). Hades gives his permission there, so this is the Underworld epic's encore.

**Play.** Kerberos, the great gatehound, is a Pylakyon older than the dead: the final form of the Kynder line, and if you started with Kynder, the great-great-grandfather of your own. Hades lets you take him up on one condition: no weapons. Your Bag doesn't open in the fight. Win, and he'll follow you, but he hates the sun. The long stair up to Tainaron has cracks where daylight falls in bright shafts, and he won't step into the light. Push column drums into the shafts to shade the way, and lead him up to the surface, where Kleon waits with water, and Olympias, for the first time, loses her composure.

**Maps.** No new maps. It uses the Katabasis's **Ascent of Tainaron** (UNDERWORLD §4.13) with a second set of objects (hide flags), and the cape. The same stair carries two ascents: Orpheus's, where you mustn't look back, and Herakles's, where the dog mustn't look up.

```text
  THE ASCENT OF TAINARON (20x60): the Kerberos layout
     | = stair edge  ### = light shaft (he won't enter)  R = column drum
 +--------------------+
 |    [ THE CAPE ]    |   N (daylight)
 |  .  .  ###  .  .   |
 |  .  R  ###  .  .   |   shaft 5: push R left into it
 |  .  .  .  .  ###   |
 |  ###  .  R  .  .   |   shafts 3-4: one drum, two shafts: choose the route
 |  .  .  .  .  .  .  |   (rest landing: a spring)
 |  .  ###  .  .  R   |
 |  .  ###  .  .  .   |   shaft 2
 |  R  .  .  ###  .   |   shaft 1: the teaching shaft, with a drum right beside it
 |  .  .  .  .  .  .  |
 |   [ from Hades ]   |   S (dark)
 +--------------------+
```

**Steps.**
1. **Hades's permission** (UNDERWORLD §4.12, at the verdict): "No weapons. Bring him back by evening. He gets fretful."
2. **The fight,** at the gate where you first passed him. No Bag for either side.
3. **The leash.** Kerberos follows you as a large escort (64×64), using scripted movement, as SYSTEMS §10 specifies for escorts.
4. **The stair.** Seven light shafts, five drums. He stops at the edge of any lit tile and whines. Push drums into the shafts to shade them.
   - Two shafts sit side by side with one drum between them, so you have to choose a route.
   - **No lock:** the drums can always be pulled back (the Girdle pulls as well as pushes in Ichor; SYSTEMS §1's drums).
5. **The top.** Daylight. Kerberos sits down in the cave mouth's shadow and won't go further. Kleon is there with a bucket of water. He's been waiting all day.
6. **Olympias.** She's come to the cape to see. She sees. She gets into the nearest large jar.
7. **Home.** Kerberos goes back down on his own, wagging all three tails. Hades sends a note.

**Engine.**
- `B_VAR_NO_BAG_USE`, as Labor 1. The escort is scripted movement with a large graphics id (`OW_LARGE_OW_SUPPORT` is TRUE in `include/config/overworld.h`).
- Light shafts are metatiles with a behavior the escort's step script checks. The drums are the Girdle's.
- **Low–Medium.**

**Boss: Kerberos.**

| Species | Lv | Ability | Item | Moves | Notes |
|---|---|---|---|---|---|
| Pylakyon | 79 | Strong Jaw (hidden) | — | Fire Fang, Thunder Fang, Ice Fang, Poltergeist | Totem boost +1 Attack, +1 Defense, +1 Sp. Def: three heads. Not catchable: he's Hades's. |

If your own party has a Pylakyon, it gets a special line before the battle: "{STR_VAR_1} lowers all three heads." If Kleon took the Kynder line (because it beat your starter), his gets that line at the top instead.

**Rewards.**
- **A three-headed collar** (trophy) → Hera Favor +10, Hades Favor +10.
- **Houndoominite** (an Ichor Stone), from Hades's note: "For your little dogs. They can look like him for a while." This keeps the bible's Mega Houndoom in the game.
- Olympias: TM Flare Blitz, from inside the jar.

**Music.** *The Ascent*: UNDERWORLD's Orpheus lament, rearranged. Its lyre line becomes a plodding, comic frame-drum walk. It gets brighter with every shaft you shade.

**Scene: the jar.**

[The cape, at the cave mouth. Kerberos lies in the shade, panting, three tongues out. Kleon pours water into a trough. Then footsteps on the path, and Olympias comes round the rock.]
```text
OLYMPIAS: Well? I came to see if you'd really…

OLYMPIAS: …

OLYMPIAS: That is a very large dog.
```
[Kerberos lifts one head and wags. Olympias walks, quite calmly, to a big storage pithos by the shrine wall, climbs in, and pulls the lid on.]
```text
KLEON: …Did she just…

OLYMPIAS: [from inside the jar] Take it back.

OLYMPIAS: [from inside the jar] Take it back, it counts, they all count, TAKE IT BACK.

KLEON: She said they all count.

KLEON: {PLAYER}. She said they ALL count.
```

---

## 4. The finale: the Kotinos

**Needs:** all twelve Labors dedicated.

**Where:** the Altis at Olympia, at noon.

**Steps.**
1. **Paionios** finishes the twelfth metope. He has done eleven Herakleses. The twelfth panel shows two figures and a dog, and he's very pleased with it.
2. **Olympias** waits at the Temple of Zeus. "One more labor. Me." She fights at full strength.
3. **The crown.** She cuts two sprigs from the sacred wild olive at the temple's back, the one Herakles brought from the far north to crown the first victors (Pindar, *Olympian* 3). She crowns you, and then Kleon.
4. **The roof.** Kleon shows Olympias his tally: by his count he's three behind. Then he climbs to the roof where Nike stands, and you go with him, and nobody stops either of you.
5. **The Hercules constellation** is placed.

**Boss: Olympias, the Serpent Queen.**

| Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|
| Kynoketos | 77 | Intimidate | Lum Berry | Dragon Dance, Waterfall, Outrage, Ice Fang |
| Pythoros | 77 | Sand Force | Soft Sand | Coil, Earthquake, Outrage, Stone Edge |
| Hisuian Goodra | 77 | Shell Armor | Leftovers | Heavy Slam, Draco Meteor, Thunderbolt, Acid Armor |
| Melodrakon | 78 | Intimidate | Sitrus Berry | Grav Apple, Moonblast, Dragon Tail, Ingrain |
| Altaria (Apotheosis: Mega Altaria) | 78 | Pixilate as Mega | Altarianite | Hyper Voice, Dragon Dance, Roost, Earthquake |
| Lernathan | 80 | Regenerator | Black Sludge | Coil, Gunk Shot, Outrage, Recover |

- On Spartan she also brings a Hydreigon at 79 and drops Kynoketos, with competitive sets (BALANCE.md's Spartan rule).
- The Pantheon's Hera seat team in the main story is Balance's call; this is the post-game version.

**Rewards.**
- **The Kotinos,** a key item. Olympia's wild-olive crown, cut from Herakles's tree.
  - It shows on the trainer card.
  - Olympias rematches you at the Heraion once a week, at the top of the Aethos post-game row (ace 80; BALANCE.md's rematch rule).
  - It is one of the four keys to Olympus's true summit (POSTGAME §3.3).
- **Hercules** placed (SYSTEMS §8).
- **The Olive Club,** a held item: Herakles cut his club from wild olive. It doubles Hierolive's Attack, as the Thick Club does for Marowak. Data only: a copy of `HOLD_EFFECT_THICK_CLUB` with a species check.
- Hera Favor +15 (the "seat" bonus in SYSTEMS §3, given for the Labors as a whole).
- Paionios gives you a small clay model of the twelfth metope for the player's room in Elaia.

**Scene: the crown.**

[The back of the Temple of Zeus. A gnarled, low wild olive with silver leaves. Olympias holds a bronze knife.]
```text
OLYMPIAS: Herakles brought this tree from the north. From past the north wind.

OLYMPIAS: He planted it here, and its leaves crowned every winner since.

OLYMPIAS: Not laurel. Olive. Laurel is for poets.

OLYMPIAS: Twelve. All twelve count. I knew they would. I just didn't say.
```
[She cuts a sprig, bends it into a ring, and sets it on your head.]
```text
OLYMPIAS: Hera made peace with Herakles in the end. Gave him her daughter.

OLYMPIAS: I don't have a daughter to spare. You'll have to make do with this.

OLYMPIAS: Archon. You'll be asked to write people's fates for them. Often. Don't.

OLYMPIAS: Kleon.
```
[Kleon, who has been standing back, looks up.]
```text
KLEON: I'm three labors behind. I don't…

OLYMPIAS: You're three behind because you stopped to pull a lamb out of a den.

OLYMPIAS: And a huntress out of a drift. And a stable boy out of a flood.

OLYMPIAS: I told my son a god was his father. It made him. I thought nothing else could.

OLYMPIAS: Nobody told you anything. And here you are, three behind, kneeling.

OLYMPIAS: Kneel properly. It's not for winning. It's for the other thing.
```
[She crowns him. Kleon stays on one knee a long moment, then stands.]
```text
KLEON: Kleos. It means being remembered. That's all. I looked it up.

KLEON: I always thought it meant dying young and loud.

KLEON: …Come on. Roof. Herakles never saw the view from up there. We will.
```

---

## 5. Species casting and substitutions

The dex's open decision D6 asks whether the Labors should use regional species where one exists. This file assumes **yes** (the dex's recommendation) and flags every change from the bible's list.

| Labor | Bible's pick | Ichor's pick | Kind | Why |
|---|---|---|---|---|
| 1. Lion | Pyroar | **Nemeleon** (#36) | **Substitution** | The dex's Nemean lion. Litleo and Pyroar stay in the glen as wild post-game species. |
| 2. Hydra | Hydreigon | **Lernathan** (#142) with **Karkitox** (#34) | **Substitution** | The dex's Hydra and Hera's crab. Hydreigon moves to Geryon. |
| 3. Hind | Xerneas | Xerneas | Kept | A legendary. |
| 4. Boar | Mamoswine | **Kaprodon** (#56) | **Substitution** | The dex's Calydonian boar (Dark/Ground). Mamoswine lives in the Oikoumene (POSTGAME §4). |
| 5. Stables | Garbodor | Garbodor | Kept: **deliberate exception** | No Aethos species fits a dung heap, and none should. |
| 6. Birds | Corviknight | **Belornis** (#110) | **Substitution** | The dex's Stymphalian bird. Corviknight stays as one of the flock. |
| 7. Bull | Tauros | **Paldean Tauros (Aqua Breed)** | Kept, refined: **deliberate exception** | No Aethos white sea-bull. The dex's own Minotaur (Asterlorn) frees Paldean Tauros, LABYRINTH's placeholder for Asterion, to play his sire. |
| 8. Mares | Mudsdale | Mudsdale | Kept: **deliberate exception** | Aethos's horses are Poseidon's sea-horses (the starter line). Thracian mares are something else. |
| 9. War-Belt | — | Hippolyta's team | New | Trainer battle |
| 10. Cattle | — | **Hydreigon** (Geryon), **Dikyon** (#5, Orthros), **Kaminoo and Taurivet** (#81–82, the red cattle) | New castings, flagged | Stesichorus's winged Geryon suits Hydreigon's three heads and six wings. Orthros is the Kynder line's middle stage, the two-headed hound, by the dex's own myth note. |
| 11. Apples | Hydrapple | **Melodrakon** (#139, Ladon) with **Aetarch** (#122, Zeus's eagle) | **Substitution** | The dex's Ladon. Hydrapple and the Applin family grow wild in the garden. |
| 12. Cerberus | Mega Houndoom | **Pylakyon** (#6) as Kerberos | **Substitution** | The dex's three-headed gatehound. The Houndoominite reward keeps Mega Houndoom in the game. |

**For the dex team:**
- Lernathan at Lv 70 (Labor 2) and Xerneas (Labor 3) are both early post-game prizes. That is deliberate, but it's Balance's call.
- Karkitox's and Kourodin's boss sets above use roles where their learnsets weren't checked. The dex validator should confirm them.

---

## 6. Cast

| Who | Role | Voice | Portrait | Overworld |
|---|---|---|---|---|
| **Olympias** | Hera's seat; sets the Labors | Commands, never asks. Dry. Proud of her creatures. Warmth she won't admit. | Exists (Pantheon) | Exists |
| **Kleon** | Proposes the Labors; your partner in Labors 1, 2 and 11; keeps a tally | Brash, then humbled, then funny about it | Exists | Exists |
| **Hyperion**, with Petros and Amathos | Labor 5, shoveling by feel (STORY §3) | Nearly blind, cheerful, "glad of it" | Exists (clouded-eyes palette, STORY §8.4) | Exists |
| **Paionios** | Sculptor of the metopes | Chatty, very proud of his work, slightly behind schedule | New | New (civilian) |
| **Atalanta** | Huntress; Labor 4; later a Brain | Quick, practical, unbothered | New (Brain) | New |
| **Kallisto** | Artemis's Hierophant; Labor 3 | As in the main game | Exists | Exists |
| **Hypatia** | Athena's seat; the courier, Labors 6 and 11 | Dry, scholarly | Exists | Exists |
| **Ariadne**, **Asterion** | Labor 7 | As LABYRINTH | Exist | Exist |
| **Augeas** | King of Elis | A hearty king who can't stand charity | New | New |
| **Diomedes** | King of the Bistones | Cruel, then ridiculous | New | New |
| **Hippolyta** | Queen of the Amazons; later a Brain | Formal, generous, fierce | New (Brain) | New |
| **The disguised goddess** | Labor 9 | Amused, never named | — | An Amazon warrior, no shadow |
| **Helios** | The Sun, with his cup | Bored, grand, secretly lonely | New | New |
| **Eurytion** | Geryon's herdsman | A grumpy herdsman | Class portrait | Class walker |
| **Prometheus** | The fire-giver | Gentle, wry, very tired | New | New, large |
| **Atlas** | Holds the sky | Cheerful, lonely, a bad liar | New | New, 64×64 |
| **The Hesperides** (Aigle, Arethousa, Hespere) | Trainers | Sleepy, evening-voiced | One shared portrait, palette swaps | One walker, palette swaps |
| **Hades** | Labor 12's permission | See UNDERWORLD | — | — |

---

## 7. Map list

| # | Map | Size | Labor | Tileset |
|---|---|---|---|---|
| 1 | The Heraion | 24×14 | Hub | Olympia (POSTGAME) |
| 2 | Nemea Glen | 30×56 | 1 | aethos + kalliste-style hills |
| 3 | The Lion's Den | 26×18 | 1 | cave |
| 4 | The Springs of Lerna | 40×36 | 2 | Lakonia marsh (main game) |
| 5 | The Ladon Ford | 28×30 | 3 | Arkadia (main game) |
| 6 | Erymanthos Slopes | 30×60 | 4 | Arkadia + Olympus snow |
| 7 | The Snowfield | 40×40 | 4 | Olympus snow |
| 8 | Augeas's Farm | 50×44 | 5 | Eleusa farm (main game) + water channels |
| 9 | The Stable Yard | 30×24 | 5 | Eleusa farm |
| 10 | The Stymphalian Reeds | 40×40 | 6 | Lakonia marsh |
| 11 | The Bull's Shore | 36×24 | 7 | knossa (LABYRINTH) |
| 12 | The Bull's Crossing | 20×90 | 7 | aethos sea |
| 13 | Abdera | 30×26 | 8 | **steppe** (new) |
| 14 | Abdera interiors (×3) | small | 8 | oikos, civic |
| 15 | The Bistonian Plain | 40×60 | 8 | steppe |
| 16 | Diomedes's Stable | 24×16 | 8 | steppe interior |
| 17 | Diomedes's Yard | 30×20 | 8 | steppe |
| 18 | The Thermodon Road | 30×56 | 9 | steppe |
| 19 | Themiskyra | 44×40 | 9 | steppe |
| 20 | Hippolyta's Hall | 22×16 | 9 | steppe interior |
| 21 | The Western Cape | 24×20 | 10 | aethos coast |
| 22 | The Ocean Stream | 16×80 | 10 | **far west** (new) |
| 23 | The Strait of the Pillars | 30×30 | 10 | far west |
| 24 | Erytheia | 50×46 | 10 | far west |
| 25 | Geryon's Pasture | 40×40 | 10 | far west |
| 26 | The Caucasus Crag | 30×44 | 11 | Olympus snow |
| 27 | The Garden of the Hesperides | 40×40 | 11 | far west |
| 28 | Atlas's Ridge | 30×30 | 11 | far west |

**MAP_DESIGN checks.** Every route-like map above (2, 6, 8, 15, 18, 24) has at least one forced grass band across the main path; its first trainer is easy and in plain view; it has a rest point; and every dead end holds an item. Nemea Glen's Girdle gate is visible from the Act I road, so the player has been looking at it for forty hours.

---

## 8. Music cues

| Cue | Use | Mode and feel |
|---|---|---|
| **The Labor** | Every Labor map that has no theme of its own | Dorian, 7/8 kalamatianos, aulos and frame drum. **Six variants, one per Pair,** each adding an instrument: by Pair 6 it is a full band. |
| The Heraion | Hub | Lydian, slow, a single kithara and a temple bell |
| Labor boss | Every Labor boss except those below | 9/8 zeibekiko; a variant of the Ichor trainer theme |
| The Hind | Sightings only | Lydian kithara solo. Stops when she bolts. |
| The Reeds / Sky Battle | Labor 6 | Wind and reed flute / an airy 7/8 |
| Thrace | Labor 8 maps | Phrygian 9/8 on a droning aulos |
| Themiskyra | Labor 9 maps | 5/8 horse gait; loses a voice per tension step |
| The Ocean Stream | Labor 10 | The main theme in Lydian, very slow, high kithara |
| Erytheia | Labor 10 maps | Mixolydian 7/8 at sunset |
| The Garden | Labor 11 | Lydian, dusk, choir pad |
| The Ascent (Kerberos) | Labor 12 | UNDERWORLD's lament as a comic walk |
| Olympias | Finale battle | The Pantheon theme, Hera's variant: a serpentine aulos line over 7/8 |
| The Kotinos | Crowning | The Ichor main theme, full, in Lydian |

About **13 new tracks** (the Labor theme's six variants share one sequence with instrument layers switched by var).

---

## 9. Art list

### Tilesets

- **`steppe`** (new secondary), for Thrace and Themiskyra: long grass, burial mounds, timber halls and stables, felt tents, horse fields, Pontic river banks. Palettes: steppe gold, river blue, timber, felt red, Thracian bronze, sky, spare.
- **`far_west`** (new secondary), for the Ocean Stream, the Pillars, Erytheia and the Garden: red earth, sunset sky, low scrub, the two Pillars (2×6 each), the golden-apple tree (4×4, animated fruit glint), Atlas's ridge, the cup's dock. Palettes: red earth, sunset, evening blue, gold, green, rock, spare.
- **Additions to existing tilesets:** water channels, sluice dials and rock dams for the Eleusa farm set; drift hollows for Olympus snow; light-shaft tiles for the Underworld stair (shared with UNDERWORLD).

### Sprites and portraits

| Who or what | Overworld | Portrait |
|---|---|---|
| Paionios | 16×32 | 64×64 |
| Atalanta | 16×32 | 64×64 (Brain) |
| Augeas, Diomedes | 16×32 | 64×64 each |
| Hippolyta | 16×32 | 64×64 (Brain) |
| Amazon warrior (class) | 16×32, 3 palettes | 64×64 |
| Bistonian soldier (class) | 16×32 | 64×64 |
| Hesperid (class) | 16×32, 3 palettes | 64×64 |
| Helios | 16×32, gold palette | 64×64 |
| Prometheus | 32×32 | 64×64 |
| Atlas | 64×64, with the sky (an animated star-field overlay) | 64×64 |
| The player holding the sky | 2 frames × 2 genders | — |
| The player in Helios's cup | 32×32 cup with the player in it | — |
| The player riding the white bull | 2 sheets (re-uses the dolphin surf frames' layout) | — |
| Kerberos | 64×64, from Pylakyon's follower sprite, scaled up and redrawn | — |

### Objects

- The lion's movement uses Nemeleon's follower sprite. The Hind, the Boar, the Mares, the cattle and Ladon use their species' follower sprites (`OW_POKEMON_OBJECT_EVENTS` is TRUE).
- Hydra heads: Trilerna's follower sprite rising from water (2 frames).
- Twelve metopes (each 32×32 on the temple facade), twelve trophy icons for the niches.
- The krotala, Atalanta's Net, Prometheus's Ember, the War-Belt, the Kotinos, the Olive Club: item icons (24×24).
- Dart-rain field effect (reuses the ash-fall effect, recolored bronze).

### Battle backgrounds

- **Marsh** (Lerna and Stymphalia), **Snowfield**, **Steppe**, **Sunset** (Erytheia and the Garden), **Sky** (the Sky Battle and holding the sky: a starry blue). Five new.

### Pictures (stretch)

- Twelve metope pictures at 64×64 in the amphora painting window (SYSTEMS §5): 24 KiB.

---

## 10. ROM estimate

Measured against LABYRINTH's ratios (§11 there: 29 maps ≈ 120 KiB of layouts and events; Greek tilesets ≈ 12–20 KiB each; songs ≈ 3.5 KiB each).

| Item | Size |
|---|---|
| 28 maps (layouts and events) | ~125 KiB |
| Two new tilesets (`steppe`, `far_west`) and additions | ~45 KiB |
| Scripts and text (12 Labors, the frame, about 900 lines of dialogue) | ~95 KiB |
| Portraits (10) and overworld sprites (about 16 sheets, including Atlas and Kerberos at 64×64) | ~45 KiB |
| Battle backgrounds (5) | ~35 KiB |
| Music (about 13 tracks) | ~45 KiB |
| Item icons, metopes, trophies, field effects | ~12 KiB |
| Metope pictures (stretch) | ~24 KiB |
| **Total** | **~400 KiB** (about 425 with the stretch pictures) |

That is roughly 6% of the ~6.3 MB left for all of Ichor's maps, tilesets, music and trainer art (POSTGAME §7 has the whole post-game's budget).

---

## 11. Engine summary

| Mechanic | Labors | Approach | Files | Effort | Fallback |
|---|---|---|---|---|---|
| Flee-from-player movement | 1, 10 | New movement type, the inverse of follow | `src/event_object_movement.c` | Medium–Low | Fixed paths |
| No Bag in battle | 1, 11, 12 | `B_VAR_NO_BAG_USE` set for the battle | `include/config/battle.h` | Low | — |
| Totem boosts | 1, 2 (none), 4, 5, 10, 11, 12 | `settotemboost` | `asm/macros/event.inc:2205` | Low | — |
| Victory catch | 1, 2, 4, 6, 10, 11 | `B_FLAG_VICTORY_CATCH_GUARANTEED` | `include/config/battle.h:378` | Low | Normal catch |
| Carried flame with rain | 2 | SYSTEMS §2 step counter | Scripts | Low | — |
| Wild double battles | 2, 5, 10 | `setwildbattle` with a second species | `asm/macros/event.inc:1632` | Low | — |
| Daily relocation | 3 | `DoDailyEvents`, hide flags, footprint metatiles | `src/clock.c`, map scripts | Low | — |
| Roamer-style flee | 3 | A special that starts a `BATTLE_TYPE_ROAMER` battle | `src/battle_setup.c` | Low–Medium | A normal wild battle |
| Charge AI and drifts | 4 | LABYRINTH's Asterion charge subset; `MB_ICHOR_DRIFT` | `src/ichor_asterion.c`, `src/metatile_behavior.c` | Medium | Scripted lanes |
| Water flow | 5 | SYSTEMS's beam-trace special, generalized | `src/ichor_beam.c` | Low–Medium | Fixed states per dial |
| Krotala radius | 6 | Key-item field use, radius check | `src/item_use.c`, scripts | Low | — |
| Sky Battle | 6 | `B_FLAG_SKY_BATTLE` | `include/config/battle.h:311` | Low | Ground battle |
| Partner battles | 1, 2, 11 | You and Kleon against wild Pokémon: `BattleSetup_StartMultiBattle` with `MULTI_BATTLE_2_VS_WILD` | `src/battle_setup.c:357` | Low | Solo battles |
| Bull-leap and bull ride | 7 | LABYRINTH's `ichor_bull_leap.c`; the surf state with a bull gfx | `src/ichor_bull_leap.c`, `src/field_player_avatar.c` | Low–Medium | — |
| Nature flavors | 8 | The existing nature-flavor relation | `src/pokemon.c` | Low | — |
| Theoxenia tells | 9 | SYSTEMS §10's no-shadow opt-out and follower bow | `src/follower_helper.c` | Low (once theoxenia exists) | Dialogue clues only |
| Cup ride | 10 | Scripted sea map, forced forward movement | Scripts | Low–Medium | A cutscene |
| Holding the sky | 11 | Input lock plus three scripted battles | Scripts | Low | — |
| Escort and light shafts | 12 | Scripted escort; a shaft behavior | Scripts, `src/metatile_behavior.c` | Low–Medium | Fixed path with drums |

**Risk: low overall.** The one Medium dependency is Labor 4 on Asterion's charge AI, and it has a fallback.

---

## 12. Flags and vars

**Vars: none.** Per-Labor state lives in `IchorSave.epics` (POSTGAME §6):

| Field | Holds |
|---|---|
| `laborsSet` (u16) | 12 bits: which Labors Olympias has set |
| `laborsDone` (u16) | 12 bits: done |
| `laborsDedicated` (u16) | 12 bits: trophy dedicated |
| `laborStep[12]` (u8 each) | Each Labor's internal state, one byte per Labor: the lion's sealed mouth, the Hind's day (3 bits), the boar's drifts (3 bits), the sluice dials, the roosts (7 bits), the mares (4 bits), the tension meter (3 bits), the herd count (4 bits), the sky's falling stars, the shaded shafts |
| `lernaPools` (u32) | Labor 2's nine pools, 2 bits each (untouched, head up, cut, burned), plus the moved-fire bit |

**Flags** (about 40, all `FLAG_ICHOR_*`; they come from the Hoenn story flags that free up as Hoenn's maps go, INVENTORY §9):

| Group | Flags |
|---|---|
| Story | `LABORS_OPEN`, `LABORS_TWELVE` (the last pair set), `KOTINOS`, `OLYMPIAS_JAR` |
| Per-Labor scenes | `L1_KLEON_TRY`, `L2_DISCOUNT`, `L3_KALLISTO`, `L4_ATALANTA`, `L5_PAID`, `L5_DISCOUNT`, `L6_KROTALA`, `L7_KLEON_SORRY`, `L8_DIOMEDES_SWIM`, `L9_GODDESS_FOUND`, `L10_CUP`, `L10_PILLARS`, `L11_PROMETHEUS`, `L11_ATLAS_TRICK`, `L12_PERMISSION` |
| Items | `GOT_KROTALA`, `GOT_ATALANTA_NET`, `GOT_PROMETHEUS_EMBER`, `GOT_OLIVE_CLUB` |
| Hide flags | About 16: the metopes (12, or one var bitfield if flags run short), Hind sightings (4) |
| Battle switches | One flag each for `B_FLAG_SKY_BATTLE` and `B_FLAG_VICTORY_CATCH_GUARANTEED`, and one var for `B_VAR_NO_BAG_USE`. They are shared with the rest of the game. |

Static-encounter "caught" flags are automatic in the boss scripts' battle results.

---

## 13. Proposed changes

**What changed when STORY.md and BALANCE.md landed** (they win; listed so the director can check):
1. **Kleon proposes the Labors** at the epilogue's Klotheia ("Herakles had twelve. Let's see about us."), and Olympias sets them for the two of you as a pair. The earlier draft had Olympias set a race. Kleon's tally of who's done more replaces the race.
2. **Kleon fights beside you** in multi battles: the Lions (Labor 1), the Hydra and the Crab (Labor 2) and Ladon (Labor 11). "The Nemean Lion is the first Labor, and Kleon fights it."
3. **Kallisto apologizes to Kleon** at the Ladon ford (Labor 3).
4. **Hyperion, Petros and Amathos** shovel the Augean Stables by feel (Labor 5), replacing Kleon's shovel scene.
5. **Olympias** speaks as STORY's Olympias: a mother who wrote her son a fate.
6. **You're the Archon** throughout (STORY decision S7).
7. **Levels** follow BALANCE.md's Aethos post-game row (bosses 70–80). Olympias's rematch is capped at that row.
8. **Wild tables on Aethos maps** use Aethos species only; existing species live in the Oikoumene. The far lands (Thrace, Themiskyra, the Caucasus, Erytheia and the Garden) keep existing species, and must be reconciled with OIKOUMENE.md (POSTGAME §4).

**To PITCH.md:**
1. **§6.1.** Replace the Labors list with §5's casting table, and add: "Kleon proposes them; Olympias, Hera's seat, sets them from the Heraion at Olympia, ten and then two more. Kleon fights beside you in several."
2. **§6.1, Labor 9.** The prize is **Hippolyta's War-Belt** (SYSTEMS D2).
3. **§6.1, the reward.** The Kotinos, the wild-olive crown, which is one of the keys to Olympus's summit.
4. **§2, Kleon's arc** gains its post-game end: "atonement in the Labors, crowned at Olympia."
5. **§6.3.** Hippolyta joins the Olympiad after Labor 9, and Atalanta after Labor 4.

**To SYSTEMS.md:**
1. **§3, Artemis's gift III** becomes one of the four chariot hinds (suggested: Hisuian Wyrdeer). Labor 3's Hind is Xerneas, the fifth (LB4).
2. **§8, Cancer** is placed by Hera Favor 30 *or* by beating Labor 2's crab, whichever comes first (LB6).

**To the dex (`design/dex/DECISIONS.md`):**
1. D6 answered as yes, per §5.
2. Note Lernathan's and Xerneas's early post-game availability for Balance.

---

## Decisions for the user

> **Settled by the user, 2026-11-14.** Asked directly: the Oikoumene opens in stages (PG-6, PG-7, PG-8); the Orpheus moment is Persephone's return, and nobody returns from the dead (K4); the five Titans and Briareus are freed (K3); the suitors stay, comic, with Mom in control (O3); Argos lives and joins you (O4); the legend castings are approved as a set (PG-31); the House of Night is built for 1.0 (PG-26, overriding K8's stretch). **Every other decision below takes its recommendation** (the user: "Take the recommendations"). Any can still be changed later.

- **LB1. Kleon proposes, Olympias sets** (recommended, from STORY §3): Olympias, Hera's seat, sets them from Olympia's Heraion for you and Kleon as a pair. The alternatives are an oracle (prophecy has ended, so it fits poorly) or Herakles himself (who would overshadow the player).
- **LB2. Ten that become twelve.** Olympias sets ten and discounts the Hydra and the Stables, as in the myth (recommended). Or set all twelve from the start.
- **LB3. Pairs.** Set two at a time, either order (recommended), or all at once, or strictly in order.
- **LB4. The Hind is Xerneas, and you keep her** after she chooses you. Artemis's gift III in SYSTEMS becomes a chariot hind of another species.
- **LB5. Strong prizes.** Lernathan at Lv 71 from Labor 2 and Xerneas from Labor 3 (recommended), or make the Labor bosses uncatchable and put their species in the wild later.
- **LB6. Cancer** may also be placed by Labor 2's crab.
- **LB7. The Kotinos** is one of the four keys to Olympus's summit (POSTGAME §3.3), so Arceus needs the Labors.
- **LB8. The Olive Club** for Hierolive: a tiny data-only signature item (recommended), or none.
- **LB10. The far lands.** Thrace, Themiskyra, the Caucasus, Erytheia and the Garden sit outside Aethos. Either they become the Oikoumene's eastern and western edges, visited early at the Aethos post-game row's levels through the Labors (recommended), or OIKOUMENE.md absorbs them and the Labors route there at its levels.
- **LB9. Scope.** All twelve with their full mechanics (recommended). The fallback set is in POSTGAME §8: if time runs short, Labors 4 and 10 use their fallbacks, and Labor 11 drops the Caucasus and starts at the garden (Atlas's trick needs no hint, just more tries).
