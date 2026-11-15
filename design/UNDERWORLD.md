# Katabasis: the Underworld

- **Owner:** Quest and level design.
- **Status:** a proposal for the user's approval. Nothing here is built yet.
- **Spine:** `design/STORY.md` §3, "The post-game spine": the Underworld is **death without a schedule, still real, still rightful. It must not turn into a resurrection story.** Where this file and STORY.md disagree, STORY.md wins.
- **Umbrella:** `design/POSTGAME.md` (order, levels, save struct, scope).
- **Companions:** `design/LABORS.md` (Labor 12, Kerberos, starts here), `design/SYSTEMS.md` (relics, fire, rites, theoxenia E11 and E12, the Bronze Obol), `design/LABYRINTH.md` (the Helm, Minos, Icarus and Daedalus, the Thread), `design/phase1/SCRIPT.md` (the Elaia well-coin).
- **Species** come from the Aethos dex. The post-game may also use existing species (dex D5). Substitutions are flagged in §7.

---

## 0. The hook

Spring hasn't come.

When the Lord of Time woke at the Frozen Hour, his brothers in Tartarus felt it, and they have been throwing themselves at the bronze gates ever since. Hades, afraid of what's under his house, barred every door of the Underworld. Nothing goes in. Nothing comes out. Persephone stayed below with him, so she never came up, so the fields of Eleusa are still gray. And the dead who can't get in drift along the roads of Aethos at night, small gray shades with their hands held out.

Hades shut every door to every thread. You don't have one.

So you go down, and the Cutter goes with you: the Fate who cut every one of these threads, and who has never once seen where they went. You pass Charon, who can't tell if you're living or dead, and the three-headed dog. In a gray meadow you meet the first Archon, who has stood by the river of forgetting for a thousand years because he can't bear to ask his father one question. You cross a plain that forgets the path behind you, to a lake that remembers. You face the King and Queen below. Then you go further down, into Tartarus, where the Titans have been chained since the world was young and have lost their voices, and write on their walls instead. You can put them back. Or you can let them go.

Then you climb back up into the light with the Queen of the dead walking behind you, because spring can't start until she's in the sun. Don't look back.

### Pillars

1. **A world in reverse.** Above, the one figure without a shadow is a god in disguise (SYSTEMS §10). Below, nobody has a shadow except the living. The shades notice yours. Gold and Aegean blue are gone from the palette, and the music has no heartbeat.
2. **Death without a schedule** (STORY §3). Prophecy is over; death isn't (STORY §1, rule 9). The dead are still dead, and that is still right. What's new is that nobody knew when. The Cutter, who always knew, comes to see what that means.
3. **The last fixed threads are punishments.** What's left of "for ever" is down here: Titans chained for ever, Sisyphus pushing for ever, and Medon waiting for ever at the river. The Katabasis asks whether those should end too, and lets you answer.
4. **Gently. Nobody comes back.** The shades are people with one small unfinished thing, and you can help with it. Nobody is brought back to life. The emotional peak is a father telling his son "It wasn't the oracle. I chose."
5. **The relics' final exam.** The Labyrinth tested each temple's verb (LABYRINTH §0). Tartarus's five cells test the relics.
6. **Fail forward.** No step can be lost for good. Turn around on the stair and you climb it again.

### At a glance

| | |
|---|---|
| Where in the story | Post-game. Opens after the epilogue's Klotheia (POSTGAME §1). Recommended after Labor pair 2. |
| Length | About 4 hours |
| Levels | `design/BALANCE.md`'s Aethos post-game row: wild 60–70, shade trainers 68–74, bosses 72–80 (Kerberos 72, Minos 74–76, Hades and Persephone 78–80, the Titans 75, Briareus 80, Giratina 80). |
| Maps | 27, plus one stretch (§3) |
| Guide | **The Cutter** (Thanira, dex #145), for the whole descent (STORY §3: "Thanira can guide you down"). |
| Bosses | Kerberos (optional), Minos, Hades and Persephone, five Titans, Briareus, Giratina |
| Relics used | Hecate's Torch, the Helm of Darkness, the Bronze Hammer, the Labrys, the Girdle, Ariadne's Thread, and Prometheus's Ember if Labor 11 is done |
| Unlocks | Labor 12; theoxenia E12 (Persephone in spring); Hades's altar (SYSTEMS §3); Ichorin's lead; the Nekranax vault; spring at Eleusa; three messages carried home (§4.14) |

---

## 1. The frame

### Why the doors are shut

The climax (STORY §3, Act III; PITCH Act III) freed the Fates and woke the Lord of Time. Two consequences land below.
- **The Titans felt their brother wake.** The Lord of Time's brothers Krios, Koios, Iapetos, Hyperion and Menoitios have been in Tartarus since the war of the Titans, guarded by the hundred-handed Briareus. At the Frozen Hour they threw themselves at the bronze gates, and they haven't stopped. (The Team Titan admins took the names Hyperion and Iapetos; these are the Titans the names belong to.)
- **Hades barred the Underworld,** above and below. No shade can cross the Styx, and no one can leave.
  - **Persephone** stayed with him, so spring never came. In Eleusa, Chloe's fields are gray and the Mystery sanctum is cold.
  - **The unferried dead** wait on the near bank, then wander up the roads. After the epilogue, small shades (Obolorn) appear in every route's night table across Aethos.

### Why the player goes

- **Chloe asks.** Demeter's Hierophant, the Mystagogue of Eleusa, knows the way down: the Mysteries were about Persephone's return. "What's reaped grows again" is their whole secret (STORY §2, the Twelve), and this year it hasn't. She gives you an initiate's gold leaf, the instructions the dead are buried with.
- **The door opens for you.** At Cape Tainaron the gate has a lock for every thread. You don't have one. It is the same reason only you could hold the Harpe.
- **You're the Archon** (STORY decision S7). The Underworld's doors are shut on every city in Aethos, and the dead are on the roads. People expect the Archon to do something. Chloe says so, drily.

### Who goes with you: the Cutter

After the climax the three Fates went to their sanctuaries (STORY §2, the Fates): **Thanira, the Cutter,** to Kaldera's forge. She is there to be caught at Lv 50, or already in your party.

She has cut every thread in Aethos for a thousand years, knowing each ending before it began, and she has loved every one (STORY: "Thanira fears her own shears. She has loved every life she cut"). She has never seen where any of them went.

- **How she joins.** When you first reach Cape Tainaron, she is waiting at the gate. If she's in your party, she comes out of her ball at the gate instead.
  ```text
  CUTTER: I cut every one of them. I'd like to see where they went.
  ```
- **How she travels.** As a scripted escort behind you (SYSTEMS §10's escort rule), using her follower sprite. If she's your party's lead, she simply is your follower.
- **Her name box** reads CUTTER (STORY decision S10). She speaks seldom and short, as the Fates do.
- **Her arc below.** The shades recognize her. Some thank her; one tells her she came too soon; most don't mind at all. At the bottom of Tartarus she meets the one thing in the world older than threads. On the stair she stays below for a while: "I owe them each a visit."

**Phaedon stays at Akti.** He is a suppliant at Hestia's hearth, exiled to Kalliste for life (STORY §2, decision S8), and he can't travel. Before you go down, he asks you to carry a message to Elpis's mother (§4.12; STORY §3's optional hook): "Tell her Elpis finished the song."

### The cast below

| Who | What | Voice |
|---|---|---|
| **The Cutter** | Thanira, the Fate who cuts; your guide | Short, careful, her shears always closed |
| **Charon** | The ferryman | Bored, exact, not unkind. Speaks in short sentences. |
| **Kerberos** | The gatehound, a Pylakyon older than the dead | Three heads, three moods |
| **The Judges:** Minos, Rhadamanthys, Aiakos | They sort the dead at the crossroads (Plato, *Gorgias* 524a) | Minos dry, Rhadamanthys stern, Aiakos fond |
| **Hades** | King below | Tired, proud, frightened of what's under his house, funny in spite of himself |
| **Persephone** | Queen below; Kore above | Warm, sharp, the only one who can make Hades laugh |
| **Medon** | The first Archon, who chained the Fates (STORY §2) | Formal, exhausted, a thousand years of not asking |
| **Kodros** | Medon's father, the king who walked into the spears (STORY §1, the backstory) | Plain-spoken. A king in a peasant's cloak. |
| **Theano** | Elpis's mother, dead five years of a fever Phaedon couldn't cure (STORY §1). The name is this file's proposal; STORY doesn't name her. | Practical, teasing, the wisest person in the room |
| **Agis and Kyniska** | Lampito's (Rhea's) two elder children, Kleon's brother and sister: one died in war, one of fever (STORY §2, Rhea) | A soldier, and a small girl who asks a lot of questions |
| **Icarus** | Daedalus's son | A boy, still, and still curious |
| **Tiresias** | The blind seer, out of work since prophecy ended | Relieved |
| **The image of Herakles** | Homer's phantom of Herakles (*Odyssey* 11.601): the hero is on Olympus, his shade is here | Counting |
| **Ajax** | Sulking | — |
| **Orpheus** | In Elysium, with his lyre | Gentle, rueful |
| **The Titans** | Five Regis, voiceless; they write on their walls | In carved capitals |
| **Briareus** | The hundred-handed jailer, Regigigas | Silent |
| **Tartaros** | The pit itself, Giratina | — |

---

## 2. The world below: rules and look

### Shadows

- **Only the living cast shadows below:** you and your Pokémon. Every shade, god and judge has none, and neither does the Cutter: "I never had a thread either."
- **Shades notice.** One line in about a third of shade conversations: "You've got a shadow. I'd forgotten what that looked like."
- **Engine:** shadows come from the expansion's object shadow system (`OW_OBJECT_VANILLA_SHADOWS` is FALSE in `include/config/overworld.h`). The check at `src/event_object_movement.c` line 10388 already asks `CurrentMapHasShadows()`. Add an Underworld map flag that keeps shadows only for the player and the follower. This is the inverse of SYSTEMS §10's per-object opt-out, and it shares that code. Low.

### Palette

| Region | Palette | Accent |
|---|---|---|
| Tainaron's cave | Basalt, wet slate | Torchlight |
| The Acheron and the Styx | Black water, cold teal, reed gray | Charon's lantern, a single amber |
| The Meadows of Asphodel | Ash violet, bone, pale lavender | The asphodel's cream flowers |
| Lethe | Fog white on gray | None |
| The Lake of Mnemosyne | Silver-blue | A thin moon-white |
| The House of Hades | Black basalt, dark bronze | Pomegranate red |
| Tartarus | Bronze and soot | Ember red, the Phlegethon's fire |
| The Chasm | Nothing: black and a violet that shouldn't exist | — |
| **Elysium** | **Gold.** A low sun that never sets, warm grass | The first warm color since the cape |

- **No sun-gold, no Aegean blue, until Elysium.** When Elysium's gold comes up after hours of cold color, it should feel like breathing out.
- **This must not look like the Frozen Hour.** The Frozen Hour is total gray and silence with a ticking music box (PITCH §7). The Underworld keeps its hues, but shifts them cold, and it has sound.
- **Engine:** the overworld's day/night tint (`OW_ENABLE_DNS`, `src/overworld.c`) gets one more fixed tint for maps flagged Underworld, and the time of day is ignored there. The tilesets' own palettes do most of the work. Low.

### Sound and music

- **No frame drum anywhere above Tartarus.** The dead have no heartbeat. The Underworld's themes are aulos, lyre and low strings.
- **The Styx has no music.** Only the pole in the water, and Charon breathing.
- **Tartarus** has a drum again: a bronze anvil struck in 9/8, the Titans' theme (§9).
- **Orpheus's lament** is the Katabasis's leitmotif. It is introduced at the cape, played by Orpheus in Elysium, and carried up the Ascent.

### Services

| Service | Below | Notes |
|---|---|---|
| Heal | **Springs,** at each rest point (the Acheron bank, the Meadows' cypress, the House of Hades's garden, Tartarus's fire-ledge, Elysium). The Underworld's rivers heal the living. | A spring is a bg event that runs the heal script, with one line: "The water is very cold. Your Pokémon look better for it." |
| Pithos | **The Danaids' jar,** in the Meadows | A working Pithos with a hole in it. "Your Pokémon are perfectly safe. The jar's only leaking water. Mostly." The Danaids were punished to carry water in leaky jars for ever. |
| Agora | None | Bring what you need. Charon warns you at the bank. |
| Wings | **Off** below | "There's no sky to fly in." The way out is up. |
| Rest (time) | Off | The Underworld has no hours. Its encounter tables have no day or night split. |

## 3. Map list

| # | Map | Size | Notes |
|---|---|---|---|
| 1 | The Mani Road | 30×70 | A new route from Lakonia south to the cape. Two forced grass bands; mourners and pilgrims as trainers; a roadside shrine of Poseidon as a rest point. |
| 2 | Cape Tainaron | 36×30 | The headland: Poseidon's old temple, the cave mouth, the bronze gate of locks, a xenia host, dig spots (with Bronze Obols in their table) |
| 3 | The Descent, upper | 30×40 | Dark (the Torch). Kalyptor country. |
| 4 | The Descent, lower | 30×40 | Darker, with a lit brazier as a landmark |
| 5 | The Acheron Bank | 30×24 | Charon's landing; the unburied; the first spring |
| 6 | The Styx | 20×70 | The crossing, on Charon's boat |
| 7 | The Gate | 24×20 | Kerberos |
| 8 | The Meadows of Asphodel | 60×50 | The hub: shades, the Danaids' jar, the cypress rest |
| 9 | The Riverside of the Oath | 24×20 | Only on an Oath of the Styx run (§5) |
| 10 | The Crossroads of Judgment | 24×20 | The three roads and the three Judges |
| 11 | The Plain of Lethe | 40×40 | Fog that forgets your path |
| 12 | The Lake of Mnemosyne | 20×16 | The guards and the password |
| 13 | The House of Hades | 30×24 | The hall and its garden |
| 14 | The Vault beneath the Hall | 16×16 | Post-Katabasis: Nekranax (dex D4) |
| 15 | The Bronze Gates | 20×20 | The way down into Tartarus |
| 16 | The Fall | — | A scripted cutscene, no map: nine days falling |
| 17 | Tartarus | 40×40 | The round hall, five cells and the inner gate |
| 18–22 | The five cells | 16×16 to 24×20 each | Krios, Koios, Iapetos, Hyperion, Menoitios |
| 23 | Sisyphus's Hill | 20×30 | A side room |
| 24 | The Chasm | 30×30 | Giratina, upside down |
| 25 | Elysium | 50×40 | Gold |
| 26 | Elysium's Shore | 30×20 | Looks out across the water to the Isles of the Blessed (`OIKOUMENE.md`, PG-40) |
| 27 | The Ascent of Tainaron | 20×60 | The Orpheus moment. Shared with Labor 12. |
| (28) | The House of Night | 24×20 | Stretch: Cresselia and Darkrai |

```text
  THE SHAPE OF THE UNDERWORLD (not to scale)

   [Mani Road] -> [Cape Tainaron] ............................ [Ascent's top]
                       |                                             ^
                 [Descent, upper]                                    |
                 [Descent, lower]                           [Ascent of Tainaron]
                       |                                             ^
                 [Acheron Bank] ==== the Styx ==== [The Gate]        |
                                                       |             |
                                         [Meadows of Asphodel]       |
                                          |     |      |             |
                         [Riverside of the Oath] |  [Danaids' jar]   |
                                                |                    |
                                [Crossroads of Judgment] ----> [ELYSIUM] -- [Isles]
                                    |                  (opens at the end)
                           [Plain of Lethe]
                                    |
                           [Lake of Mnemosyne]
                                    |
                           [House of Hades] -- [Vault] (post)
                                    |
                           [Bronze Gates] -> (the Fall) -> [TARTARUS]
                                                            /  |  |  |  \
                                                     five cells   [Sisyphus's Hill]
                                                               |
                                                         [inner gate: Briareus]
                                                               |
                                                          [THE CHASM]
```

---

## 4. The descent, step by step

### 4.1 Eleusa: the gray fields

**Trigger.** After the epilogue (STORY §7.11), Eleusa's map uses a gray-wheat variant, and its wild table loses its Grass types except Persenyx at night.

**Steps.**
1. Chloe stands in the dead field, holding a single gray ear of wheat.
2. She explains in four lines (scene 1), and gives you the **Gold Leaf**, an initiate's tablet.
3. The Scroll of Deeds gains "Katabasis". Tainaron is marked on the region map.

**The Gold Leaf** (key item). Real initiates of the Mysteries were buried with thin gold tablets telling them what to do below. The leaf's text, shown from the Bag:
```text
On the left you'll find a spring, and a white cypress beside it.

Don't go near that spring. Go on, to the Lake of Memory.

Cold water flows there. Guards stand before it.

Say: "I am a child of Earth and starry Sky."
```
It tells you exactly how to beat the Plain of Lethe (§4.8), and that's the point. Anyone who reads it is ahead.

### 4.2 The Mani Road and Cape Tainaron

**The Mani Road** (30×70) runs south from Lakonia along a dry peninsula of towers and stone walls.
- Two forced grass bands: thornscrub, then the cliff path. Mourners and pilgrims stand on it as trainers, going to the cape "to leave something for the ones who can't cross".
- A shrine of Poseidon halfway is a rest point. Dig spots along the walls.
- **Lampito's house** is on the way, in Lakonia. Rhea is under house arrest there (STORY §2). Visit her before you go down and she says one thing, which matters later (scene 2).

**Cape Tainaron** (36×30):
- **The temple of Poseidon** stands on the point, as the real one did, with the cave mouth beneath it.
- **The gate** is bronze. A lock for every thread is cast into it, thousands of tiny keyholes.
- **Shades** gather on the cape at night: wild Obolorn, plus a few to talk to.
- **The Cutter** waits at the gate (§1).
- **A xenia host,** an old woman who keeps a lamp in her window for the dead. She feeds you and lets you rest to night.
- **Dig spots** whose table includes Bronze Obols (a proposed SYSTEMS §5 change, §14 below), for players who've spent the Elaia well-coin.

**Steps.**
1. **At Akti first** (optional but signposted): Phaedon's message (scene 2).
2. **The cape.** The Cutter at the gate (scene 2).
3. You touch the gate. Nothing for a moment, then every lock turns at once.

### 4.3 The Descent

Two dark cave floors (Hecate's Torch). The torch's radius is the same as above (SYSTEMS §2), but nothing glows here except what you light.
- **Upper:** a switchback down past old votive niches. Two shade trainers.
- **Lower:** one great brazier you light as a landmark. From the brazier's light you see the Acheron's reeds below, and hear the water.
- **Wild:** Kalyptor, Obolorn, Golbat, Sableye, Sinistea, Dusclops.

### 4.4 The Acheron Bank: Charon

**The unburied.** A crowd of small shades (Obolorn) stands in the reeds with their palms open. The unburied wait a hundred years on this bank (Virgil, *Aeneid* 6).

**Charon's fare: the Elaia well-coin** (STORY §3: "Charon takes the Elaia well-coin").
- **The coin.** The slice hides a Relic Copper in Elaia's well, "a coin someone wished on" (SCRIPT.md). SYSTEMS §5 renames it the Bronze Obol. It is the fare Charon wants: "A wished-on coin. Those carry further down here."
- **If you did theoxenia E11,** you already gave that coin to a ragged shade by a river, and the shade was Hades. Charon waves you on. "The master told me. You paid an old man's fare once. That was your coin. Get in."
- **If you sold it,** any Bronze Obol will do. "Coin's a coin."
- **No obol at all?** Charon waits. Dig one at the cape, or ask the unburied: one of them, a small one, has been saving a coin for a hundred years and gives it to you. "I couldn't pay for me. Maybe for you."
- **The Cutter** crosses free. Charon knows her: "You. You've sent me more fares than anyone."

**Paying for the unburied** (optional). You can give Charon more obols, one per shade. Each shade you pay for crosses with you. Up to five.
- In the Meadows, each one finds you once, to say thank you, with a small gift: a Spell Tag, a Cleanse Tag, a Reaper Cloth, a Revive and a Pearl.
- Each gives Hades +1 Favor (SYSTEMS §3's post-game row).
- It is real money (obols are sell-only treasure), spent on strangers, which is the theoxenia moral again, played rather than said.

**Rest point:** a cold spring on the bank. Every rest point below is a spring: the Underworld has rivers, and its water heals the living.

### 4.5 The Styx: the crossing, and the Oath

**The crossing** is a scripted ride in Charon's boat across a long, misty strip of black water (20×70), with no control. Wild encounters only if you fish.
- **The fishing table:** Stygiad, Kalyptor, Charonaut (rare), Ketofry and Kynoketos.
- **The oath.** Halfway over, a pale Stygiad rises beside the boat and looks at you.
  - **On an Oath of the Styx run** (PITCH §5's Nuzlocke): Charon speaks of it (scene 4), and offers to let it go.
    - **KEEP IT:** "Good. Most don't."
    - **LET IT GO:** the Oath's rules switch off for the rest of the game. "The river doesn't mind. Oaths end. That's what makes them oaths."
    - Either way, the Stygiad follows the boat to the far bank and can be caught there. It is the Oath's emblem in the dex.
  - **Not on the Oath:** Charon says one thing about oaths and goes back to poling.

### 4.6 The Gate: Kerberos

At the far bank, under a gate of black stone, lies the great gatehound: a Pylakyon older than the dead. His three heads take turns sleeping, and none of them is sleeping now.

**Three heads, three ways past.** Each head can be dealt with in one way of its own, or left awake.

| Head | Its manner | What puts it out | Myth |
|---|---|---|---|
| **The hungry head** (left) | Drools, watches your bag | A **Barley Cake and Honey**, offered together: a honey cake. Both are SYSTEMS §3 offerings. | The Sibyl's honey-cake (*Aeneid* 6.420) |
| **The listening head** (middle) | Ears forward, twitching at every sound | **A song.** A party Pokémon that knows **Sing** or **Grass Whistle**, or the **Lyre of Apollo** (Apollo's gift II, SYSTEMS §3) | Orpheus |
| **The watchful head** (right) | Never blinks | **It can't see you.** Wear the **Helm of Darkness** (LABYRINTH) and walk past on its side. | Hades's own helm, at Hades's own gate |

- **All three out:** you walk past without a fight. Kerberos snores in three keys.
- **Any awake:** he stands. Battle. He gets +1 to a stat for each head still awake: hungry +1 Attack, listening +1 Speed, watchful +1 Sp. Def (`settotemboost`). Win, and he lies down and lets you through.
- **No lock:** you can leave and come back with what you need.
- **The Cutter's line** when the dog wakes: "He's never let anyone past who wasn't dead."

**Boss (optional): Kerberos.**

| Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|
| Pylakyon | 72 | Strong Jaw | — | Fire Fang, Thunder Fang, Ice Fang, Crunch |

He isn't catchable. Labor 12 brings him up later at Lv 80 (LABORS §3).

### 4.7 The Meadows of Asphodel

The hub. A gray-violet plain of pale flowers under no sky, full of drifting shades who mostly don't remember why they're waiting. The rest point is a spring under a black cypress. The Danaids' jar (the Pithos) stands by a well that the Danaids keep filling.

```text
  THE MEADOWS OF ASPHODEL (60x50)
 +--------------------------------------------------------------+
 |  [from the Gate]                                             |
 |   .  .  ,,,,,,,  .  .  .  .  .  .  ,,,,,,,,  .  .  .  .      |  ,, = asphodel (encounters)
 |   .  ,,,,,,,,,,,,  .  [AGIS and KYNISKA]  ,,,,,,,,,  .  .     |
 |   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   |
 |  [Danaids' well + jar]   .  .  [CYPRESS: spring]  .  [Ajax]   |
 |   .  ,,,,,,,,,,  .  .  .  .  .  .  .  .  ,,,,,,,,,,  .  .    |
 |   [Tiresias]  .  .  [image of Herakles]  .  .  [ICARUS, cliff edge]
 |   .  .  ,,,,,,,,,,,,,,,,,,,  .  .  .  .  .  .  .  .  .  .    |
 |  [to the Riverside of the Oath] (Oath runs only)              |
 |  ~ ~ ~ LETHE's bank ~ ~ ~ [MEDON, standing]  [to the Crossroads] -->
 +--------------------------------------------------------------+
```

**The asphodel** is the meadow's tall grass: you can't avoid it on the way from the Gate to the Crossroads. Six shade trainers stand in it, optional except for one at the crossroads path. They are trainers who died long ago, in gray palette swaps of ordinary trainer classes ("SHADE of a hoplite").

**The shades you meet.** Each has one small thing, and none of it is a fetch quest except Icarus's single delivery.

| Shade | Where | Wants | Gives | Condition |
|---|---|---|---|---|
| **Medon,** the first Archon | Standing on Lethe's bank, where he has stood for a thousand years, neither drinking nor leaving | To know whether the oracle killed his father. He has never dared ask. | His story, and a question for the Archon who untied his Knot (scene 6). He follows you once Elysium opens (§4.12). | Always |
| **Agis and Kyniska,** Kleon's elder brother and sister | Sitting together in the asphodel | To hear about their little brother, whom they never met | Their message for their mother (scene 7) | Always. Their lines change with how many Labors Kleon has done. |
| **Icarus** | At the meadow's cliff edge, where the gray ends in dark air | To know his father is all right | **Icarus's Feather**, for Daedalus | Always. His lines change if you flew the Icarus Shaft (LABYRINTH `FLAG_ICHOR_ICARUS_FLIGHT`). |
| **Tiresias** | Leaning on a staff by a dry stream | Nothing. He's resting. | A line about a city that sank in a day: a seed for Atlantis (POSTGAME §3) | Always |
| **The image of Herakles** | Standing with a bow, counting | To know how many | Counts your Labors aloud. With all twelve: "Then I can stop counting." | Always |
| **Ajax** | Turned away | — | Silence. If you have Odysseus's Periplous (ODYSSEY §1), he turns further away. | Always |
| **The Cutter's dead** | Scattered | — | Shades who recognize the Cutter. "Oh. It's you." Most are kind about it. | Always |
| **The unburied you paid for** | They find you | — | Small gifts (§4.4) | Per obol |
| **Your fallen** | The Riverside of the Oath | To say goodbye | — | Oath runs only (§5) |

**Why Medon is still here.** A thousand years ago an oracle said a king's death would save Astyra, and King Kodros walked into the enemy's spears in a peasant's cloak. Medon couldn't bear that the oracle might have been wrong and his father dead for nothing, so he chained the Fates so no oracle could ever be wrong again (STORY §2). Below, he could have asked his father. He never has, because he's afraid of the answer. He won't drink from Lethe, because forgetting would be worse. He won't go to Elysium, because his father is there.

The player is the Archon who untied Medon's Knot. That is the scene.

### 4.7a The Crossroads of Judgment

A meadow where three roads part (Plato's *Gorgias*): to the Meadows, behind you; to Tartarus, down; to Elysium, which is closed, its gate of gold leaves tied shut. Three judges sit on three stones.

**The judgment.** They judge each soul by its thread. You have none.
1. **"Next."** At first they simply wave you through, puzzled.
2. **Then they judge your deeds instead,** from the save file. Each Judge picks lines from what you've done (§5, "the judgment"). It is the Scroll of Deeds read aloud by people who don't flatter.
3. **Minos asks for the Helm** (STORY §3; SYSTEMS §16.5). "That's from my tomb, I believe. I'll hold it while you're here." He takes the Helm of Darkness. Hades returns it at the end (§4.12).
4. **Minos's test.** Minos, Knossa's dead king, wants to see what someone with no thread fights like. Battle.
5. **Two questions answered.**
   - **Phaedon's message.** You ask where Elpis's mother went. Aiakos: "Theano, wife of Phaedon. The gold fields. She asked after the girl. Often." The gate is shut, so the message waits.
   - **The Cutter asks** the Judges whether anyone she cut is angry with her. Rhadamanthys: "Some. Not many. You never cut early. You only seemed to." The Cutter doesn't answer.

**Boss: Minos, King of Knossa, Judge of the Dead.**

| Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|
| Kolossard | 74 | Clear Body | Leftovers | Heavy Slam, Earthquake, Stealth Rock, Stone Edge |
| Melisseer | 74 | Forewarn | Focus Sash | Quiver Dance, Bug Buzz, Psychic, Defend Order |
| Panacoil | 74 | Regenerator | Black Sludge | Heal Pulse, Toxic, Sludge Bomb, Wish |
| Taurivet | 75 | Flash Fire | Charcoal | Flare Blitz, Heavy Slam, Shift Gear, Earthquake |
| Mantipod | 75 | Magic Bounce | — | Mystical Fire, Psychic, Calm Mind, Will-O-Wisp |
| Asterlorn | 76 | Guts | Flame Orb | Close Combat, Lash Out, Bulk Up, Thrash |

These are Minoan things: Talos's bronze, the Minoan bee, the snake goddess, a bull, an oracle's tripod, and the Minotaur's own kind. His Asterlorn isn't Asterion, who is upstairs with Ariadne.

### 4.8 The Plain of Lethe and the Lake of Mnemosyne

**The Plain of Lethe** (40×40) lies on the left of the road to the House of Hades, exactly where the Gold Leaf says. It is white fog over gray ground, standing stones and a few white cypresses.

**The forgetting.**
- **Your path forgets you.** As you walk, the plain rearranges behind you. Standing stones you passed shift by a tile; the gap you came through closes and another opens. Go back the way you came and it isn't there.
- **The footprints vanish** three steps behind you.
- **Lethe itself** is the first spring you'll see, by the first white cypress, straight down the obvious path. The Leaf says don't. If you drink anyway:
  - "You can't remember the way. Or why you came. Something about a spring?"
  - You're back at the plain's edge. Your Scroll of Deeds shows the Katabasis page blank until you reach Mnemosyne, which gives it back ("You remember").
  - Nothing else is lost.
- **The true way** goes past Lethe's spring and on. The landmark is sound: a second spring, louder, colder, with flowing water you hear before you see.

```text
  THE PLAIN OF LETHE (40x40): fog, sketch of one solution
     c = white cypress   s = Lethe's spring   S = stones that shift behind you
     M = the way to Mnemosyne (sound gets louder)
 +---------------------------------------------+
 |  [from the Crossroads]                      |
 |    .  S  .  .  S  .  .  .  .  .  S  .  .    |
 |    .  .  .  c  s  <-- the obvious path ends here (Lethe)
 |    .  S  .  .  .  .  S  .  .  .  .  .  .    |
 |    .  .  .  .  .  S  .  .  .  S  .  .  .    |
 |    .  .  S  .  .  .  .  .  c  .  .  S  .    |  a second cypress: a decoy, no spring
 |    .  .  .  .  S  .  .  .  .  .  .  .  .    |
 |    .  S  .  .  .  .  .  .  S  .  .  M  -->  [LAKE OF MNEMOSYNE]
 +---------------------------------------------+
```

**The Lake of Mnemosyne** (20×16). Cold, clear water in a ring of silver stones. Two guards stand before it.
- **They ask:** "Who are you? Where are you from?" (scene 11)
  - **"A CHILD OF EARTH AND STARRY SKY"** is the Leaf's answer, and passes.
  - **"{PLAYER} OF ELAIA"** fails gently: "Names are for up there. Try again."
  - **"NOBODY'S. MY THREAD IS MY OWN."** appears only if you have no thread, which is to say always for the player, and only after you've read the Leaf once. The guards confer. "That isn't the answer." "It's a better one." It passes.
- **You drink.** "You remember." The Cutter touches the water and doesn't drink: "I remember all of them already."
- **Mnemosyne's Water,** a key item: a flask from the lake. Pour it into the Pool of Mnemosyne in Arkadia, its spring above ground (PITCH §1), and the pool remembers the first myth: **Ichorin's** encounter opens there (dex #152; POSTGAME §3).

**Engine.**
- **The shifting stones** are coord triggers that swap metatiles behind the player, like LABYRINTH's Turning (`src/ichor_thread.c`'s turned layouts). Low.
- **The vanishing footprints** reuse the sand-footprint field effect with a short timer.
- **The blank Scroll page** is one flag the Scroll's page reads.
- **The password** is a multichoice with a conditional fourth option, as theoxenia E5 has.

### 4.9 The House of Hades

A hall of black basalt with a throne of dark bronze. Inside its walls is a garden of pale pomegranate trees and white poplars, Persephone's. Hades sits. Persephone doesn't.

**Steps.**
1. **Hades explains** (scene 12): the Titans, the doors, his fear.
2. **Persephone** suggests finding out why they rattle. Hades says nobody goes into Tartarus. Persephone says nobody *with a thread*.
3. **Battle:** "Show me you can hold what's down there, if it gets out."
4. **The Key of Hades.** Greek art shows Hades holding a key. He gives it to you: the key to "the house under the house". "Find out what they want. Then make them stop."
5. **Rest:** a spring in the garden. Persephone offers you a pomegranate. The Cutter, quickly: "Don't eat anything down here." You can take it (a Pomeg Berry, "Persephone's", which Hades loves as an offering), not eat it.

**Boss: Hades and Persephone,** a two-trainer double battle (`trainerbattle_two_trainers`, `asm/macros/event.inc` line 816). Each brings three, so the royal couple fight side by side.

| Trainer | Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|---|
| Hades | Plouteras | 78 | Thick Fat | Leftovers | Earthquake, Body Slam, Stockpile, Recycle. Hades was Plouton, "the wealthy one". |
| Hades | Stygiad | 78 | Pressure | Never-Melt Ice | Freeze-Dry, Shadow Ball, Haze, Destiny Bond |
| Hades | **Pylakyon** (Kerberos) | 80 | Strong Jaw | — | Fire Fang, Thunder Fang, Ice Fang, Poltergeist. "You put my dog to sleep. I'll wake him." |
| Persephone | Korantha | 78 | Natural Cure | Miracle Seed | Petal Dance, Moonblast, Synthesis, Grassy Terrain |
| Persephone | Trevenant | 78 | Harvest | Sitrus Berry | Horn Leech, Poltergeist, Leech Seed, Will-O-Wisp |
| Persephone | **Persenyx** | 80 | Perish Body | Leftovers | Strength Sap, Shadow Ball, Leaf Storm, Mean Look |

- **Kerberos is Hades's ace either way.** If you fought him at the gate, Hades: "You've met. He liked you. He likes everyone he bites."
- **Persephone has both her forms,** the spring maiden and the queen below. That is the dex's branching Rhoaril line in one team.
- **On Spartan,** both gain 2 levels and Kerberos holds a Life Orb.
- **His full team** (six, Lv 82: the three above with Dusknoir, Charonaut and Bouldyphus) is his weekly rematch in the hall after the Katabasis.

### 4.10 Tartarus: the relics' exam

**The Bronze Gates.** The Key of Hades opens them. Behind is nothing but a drop.

**The Fall.** "A bronze anvil dropped from earth would fall nine days and nights before it reached Tartarus" (Hesiod, *Theogony* 724). A cutscene: nine flashes of dark and darker, a counter of days, your torch swinging. You land softly. The Cutter, who has never fallen before, lands on her back and lies there a moment.

**Tartarus** is a round bronze hall under a ceiling too high to see, ringed by five cells, with the inner gate at the far side and Briareus standing before it, motionless, a hundred hands folded. The Phlegethon, the river of fire, runs through a channel around the hall.

```text
  TARTARUS (40x40)
 +---------------------------------------------------+
 |                 [ INNER GATE ]                     |
 |                  B (Briareus)                      |
 |     [MENOITIOS]                    [HYPERION]      |
 |       cell 5   ~~~~ Phlegethon ~~~~   cell 4       |
 |              ~                    ~                |
 |  [KOIOS]    ~    (the round hall)   ~    [IAPETOS] |
 |   cell 2    ~       F (fire-ledge:  ~     cell 3   |
 |              ~        rest point)  ~               |
 |               ~~~~~~~~~~~~~~~~~~~~~                |
 |     [KRIOS]                      [SISYPHUS'S HILL] |
 |      cell 1        (landing)          side room    |
 +---------------------------------------------------+
```

**The five cells.** Each cell holds one Titan, chained in what Tartarus has made of him over the ages. Each is opened with one relic or verb. The walls inside are covered in carved words, the oldest worn smooth, the newest fresh: the Titans lost their voices down here, so they write (Prometheus warned you, LABORS §3, Labor 11).

| Cell | Titan | Became | The lock | Relic or verb | Regi |
|---|---|---|---|---|---|
| 1 | **Krios**, of the south and the ram | Stone | A cell walled in rubble, a maze of it | **Bronze Hammer** (Hephaestus's Hammer for the 2×2 blocks, if you have the upgrade; otherwise a longer way round) | **Regirock** |
| 2 | **Koios**, the pole of the north | Ice that never melts | The cell is ice from wall to wall | **Carry fire** from the Phlegethon to four braziers inside, 20 steps each (SYSTEMS §2). **Prometheus's Ember** (LABORS, Labor 11) never runs out and makes it trivial. | **Regice** |
| 3 | **Iapetos**, the piercer, Atlas's father | Iron | Bronze chains on gear dials | **The Labrys**: turn the dials (Daedalus's mechanism, LABYRINTH §5.5) and cleave the chains | **Registeel** |
| 4 | **Hyperion**, the Titan of light | Lightning | A cage of Zeus's bolts | **Bronze mirrors**: turn them to carry the bolts into a grounding pillar. Apollo's beam verb (SYSTEMS §12, `src/ichor_beam.c`). | **Regieleki** |
| 5 | **Menoitios**, "doomed strength", whom Zeus struck down into the dark | Dragon bone | **Erebus**: a darkness that eats light. The Torch doesn't work. | **Ariadne's Thread**: lay it as you go. It glows red in the dark, and it is the only thing you can see. Find the cell by retracing and branching. | **Regidrago** |

- **Each Titan** is a static encounter once its cell opens (Lv 75). Catch it, or beat it.
- **A beaten Titan** walks out of Tartarus into the world above, and waits in a place that suits him until you catch him: Krios on Kronion Hill, Koios in the Ascent's ice caves, Iapetos at Kaldera's forge, Hyperion on Delphoi's shining cliffs (the Phaedriades), Menoitios in Arkadia's darkest wood. Fail forward.
- **Sisyphus's Hill** is the side room (below).
- **The exam's order** is free. The fire-ledge in the middle, with its spring, is the rest point.

**The walls.** One wall per cell, read like a sign. These are drafts. Each line is one box; capitals because they're carved.

| Titan | Some of what's written |
|---|---|
| Krios | "I COUNTED THE DAYS. THEN THE YEARS. THEN SOMETHING LONGER." / "IS THE RAM STILL IN THE SKY?" |
| Koios | "NORTH IS UP. I HELD IT THERE ONCE." / "I WAS NOT ALWAYS COLD." |
| Iapetos | "ATLAS. PROMETHEUS. MENOITIOS. EPIMETHEUS. MY SONS." / "DOES ANYONE STILL HOLD THE SKY?" |
| Hyperion | "I WAS LIGHT. THEY MADE ME LIGHTNING." / "A MORTAL WEARS MY NAME, THEY SAY. IS HE BRIGHT?" |
| Menoitios | "I WAS TOO STRONG. THAT WAS THE CRIME." / "THE DARK HAS TEETH. I GREW SOME TOO." |

**Atlas's message.** If you did Labor 11, Iapetos's wall gives a choice after you read it.
- **"ATLAS SAYS HE'S STILL HOLDING IT."** The Titan's lights flicker, and as you watch, new words scratch themselves into the iron, one letter at a time: "GOOD BOY."
- It's the smallest scene in the Katabasis and possibly the best.

**Sisyphus's Hill** (20×30, a side room). A Bouldyphus pushes its boulder up a slope that loops: walk to the top and you're at the bottom.
- **Your own column drum** sits at the foot. Push it up (the Girdle), and at the top it rolls back down.
- **The trick, shown not said:** stop pushing. Watch. The Bouldyphus, grinning, stops too, and nudges its boulder *sideways* into an alcove at the second landing. A door opens.
- **Copy it** with your drum and the door opens for you: a hidden room with a Gold Stater, a Rare Bone, TM Stone Edge and a Reaper Cloth.
- **The Bouldyphus** can then be caught (Lv 74). "Nobody said up. They said push."

**Briareus.** When the fifth cell opens, the inscriptions on all five walls change at once, and every wall says the same two words: "OPEN IT." Briareus, the hundred-handed jailer, moves for the first time since the war of the Titans.

**Boss: Briareus.**

| Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|
| Regigigas | 80 | Slow Start | — | Crush Grip, Knock Off, Drain Punch, Protect |

Beaten or caught, he opens the inner gate. With nobody left to guard, he follows the Titans up (if beaten, he waits at sea off the Pillars, POSTGAME §3).

**Engine.**
- Every cell reuses a system already specified: Hammer obstacles (SYSTEMS §1), carried flames (§2), Labrys dials (LABYRINTH §5.5), the beam special (`src/ichor_beam.c`), and the Thread in darkness (LABYRINTH §5.1–5.2, with the Torch disabled by a map flag).
- The looping hill is a map whose north edge connects to its own south edge.
- **Low–Medium overall,** because it's mostly content on top of earlier systems.

### 4.11 The Chasm: Giratina

Beyond the inner gate is the bottom of everything: **Tartaros** itself, the pit, which Hesiod counts among the first beings, older than the gods. Empty of its prisoners for the first time since the beginning, it turns over to see who emptied it.

**The Chasm** (30×30) is upside down.
- **The D-pad's up and down are swapped** on this map, and the tiles are drawn hanging from the top of the screen.
- It's a short maze: three switchbacks and a bridge over nothing.
- A message on entry: "Up is down here. You'll get used to it." The Cutter: "I don't like it either."

**Boss: Tartaros.**

| Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|
| Giratina (Altered) | 80 | Pressure | — | Shadow Force, Dragon Claw, Aura Sphere, Earth Power |

- Catchable. With it, the **Griseous Core** ("the core of the pit"), which turns it to its Origin Forme.
- **Engine:** the input swap is one flag checked where the D-pad is read for walking, in `src/field_control_avatar.c`. Low.

### 4.12 Hades's verdict, and Elysium

Back in the hall (scene 13), Hades is angry, then isn't. The Titans have stopped rattling, because they've left. He opens the doors.
- **The dead** begin to cross. Above, the Obolorn leave the routes' night tables after the next daily reset.
- **The Helm** comes back from Minos, by Hades's hand.
- **The Hades altar** appears in his garden (SYSTEMS §3's Hades row). Hades Favor +15.
- **Labor 12's permission,** if Olympias has set it.
- **Elysium opens.** Persephone unties the gold leaves on the Crossroads' third gate.

**Elysium** (50×40) is gold. A low sun that never sets, warm grass, white poplars, a river that runs clear. The good dead live here, as much as they live. The rest point is a spring by a white poplar.

**Three things happen in Elysium.**

1. **Theano** sits under a poplar, rolling a bandage (scene 14). You give her Phaedon's message: "Elpis finished the song." She made the lullaby up, she says, as she went along, and never got to the end of it before Elpis fell asleep. She asks how it ends. You can't sing it; the music plays the resolved melody, the one Elpis finished (STORY §1, the motifs: "It never resolves until Elpis finishes it"). She gives you a reply to carry back.
2. **Medon and Kodros** (scene 15). Medon, who would never come here, follows you from Lethe's bank to the gate now that it's open, because you're the Archon and he wants to see what you do. At the gate a man in a peasant's cloak is waiting. **Kodros** says the line the whole institution was built to avoid hearing: **"It wasn't the oracle. I chose."** Medon, a thousand years late, goes in.
3. **Orpheus** plays by the river (scene 16). He teaches the Ascent without meaning to.

**Also here:**
- **Elysium's Shore** (30×20), looking out across the water to the Isles of the Blessed: gold sand, rare fishing, and a hidden Ichor Stone in a shell.
- **Wild:** the gentlest table in the game, and among its rarest (§6).

**Persephone's return.** Persephone walks with you to the Ascent's foot. Spring can't start until she's in the sun, and Hades, being Hades, sets a condition (scene 13): she follows you up, and **you mustn't look back** until she's out. "That's how it's done. Ask Orpheus. Actually, don't."

This is the Orpheus moment, and it is not a resurrection. Persephone is a goddess going up for the season, as she does every year. What's at stake is spring.

### 4.13 The Ascent of Tainaron: don't look back

**The Ascent** (20×60) is a long stair from Elysium's edge up through the rock to the cape. You go first. Persephone follows two tiles behind. The Cutter stays at the foot (scene 17). Your follower Pokémon goes into its ball for the climb (`B_FLAG_FOLLOWERS_DISABLED` is `FLAG_ICHOR_FOLLOWERS_DISABLED` in `include/config/overworld.h`), so nothing walks behind you but the Queen.

**The rule.** Hades said it once: don't look back. On this map, **facing south fails**: any press of Down, even a turn in place.

**The stair is built to tempt you.**

| Landing | What happens behind you | The trap |
|---|---|---|
| 1 | Persephone's footsteps, light, and her voice. She talks the whole way. | — |
| 2 | She stops to pick something. "Narcissus. Down here? I'll be one moment." | — |
| 3 | **The footsteps stop.** The music drops to one held note. "The footsteps behind you have stopped." | Orpheus's mistake. They haven't stopped. Wait, or walk on. |
| 4 | A switchback. The path goes west, then a dead end with a ledge that looks like it needs a step down. | It doesn't. A second path runs east along the wall. |
| 5 | **Hades's voice,** from far below: "Kore. Come back a moment. You forgot something." | It's a test. She doesn't go, and neither should you. |
| 6 | "Would you like a pomegranate seed? Just one. For the road." | Eating in the Underworld binds you below. Choose NO THANK YOU; YES is a fail too (you'd have to turn to take it). |
| 7 | Daylight ahead. A last flight. She's humming. | — |

**What she says behind you** (scene 18) moves from teasing, to the year she's spent below, to the thing she tells every mortal who's ever led her: that spring isn't a gift, it's a return, and returns are the point.

**Failure.** If you turn:
- Persephone is gone. "Behind you, the stair is empty."
- Hades's voice: "Again. Everyone gets one more try. He didn't." You're back at the foot. Her lines shorten on each retry, so the second climb isn't a chore.

**At the top.** Persephone steps past you into the sun. You can turn around now. Behind her, down the whole length of the stair, the cracks in the rock are green.

**Engine.**
- The facing check is a per-step callback on this map (like LABYRINTH's thread step callback in `src/field_tasks.c`), plus a check on turn-in-place input. It fails if the player's facing becomes `DIR_SOUTH`. Low.
- Persephone is a scripted escort two tiles behind (SYSTEMS §10's escorts). The footsteps are a sound effect that the script stops at landing 3.
- Landing 6 is a yes/no box with YES as a fail.

### 4.14 Spring, and three messages home

You come out on the cape at dawn, and the cape's dry grass has gone green overnight.

- **Eleusa is green.** The map's gray variant is gone, its Grass types return, and Korantha appears by day. Chloe gives you a sheaf of First Fruits and Demeter Favor +10. "What's reaped grows again. Told you. Don't tell anyone."
- **Persephone** is above for the season. Theoxenia E12 (SYSTEMS §10) can now happen: a pale girl picking narcissus at dusk.
- **The Cutter** returns to Kaldera's forge in her own time, or to your party (scene 17).
- **Three messages to carry,** each optional, each one scene:

| To | Where | From | What happens |
|---|---|---|---|
| **Phaedon** | Akti's Asclepeion | Theano | Her reply (scene 19). Elpis is there. |
| **Lampito (Rhea)** | Her house in Lakonia | Agis and Kyniska | Her children's message (scene 20). Kleon may be visiting. |
| **Daedalus** | His workshop, Knossa | Icarus | The feather (scene 8). The Wings learn the way to your ship. |

- **The Scroll of Deeds** marks the Katabasis done when you come out on the cape. The messages are their own lines on its page.

---

## 5. Mechanics in detail

### The judgment: reading the save

At the Crossroads, the Judges each pick one line from a list, by the first condition that's true. They are drafts, one box each.

| Judge | Condition | Line |
|---|---|---|
| Minos | Caught 300 or more species | "A collector. We get those. They keep counting down here too." |
| Minos | Caught fewer than 100 | "Travels light. Good. Nothing's heavier than a long list." |
| Minos | Otherwise | "Busy. Not cruel. Next." |
| Rhadamanthys | Cleansed 10 or more desecrated altars (SYSTEMS §3) | "You cleaned up after the Titans. Someone should have." |
| Rhadamanthys | Beat Kleon at every meeting | "You won every time. Did you ever let him win?" |
| Rhadamanthys | Otherwise | "No crimes worth the name. Disappointing." |
| Aiakos | Did theoxenia E11 or paid for an unburied shade | "You paid a stranger's fare. That gets talked about here." |
| Aiakos | Reached Chosen rank (Favor 100) with any god | "One of them loves you. That's rare, and dangerous." |
| Aiakos | On the Oath of the Styx, with fallen Pokémon | "You've sent some down ahead of you. They're waiting." |
| Aiakos | Otherwise | "Kind enough. Go on." |

**Engine:** pokedex counts, `IchorSave` fields and flags SYSTEMS already defines. Scripts only. Low.

### Your fallen: the Riverside of the Oath

**Only on an Oath of the Styx run.** The Oath is PITCH §5's optional Nuzlocke, and nobody has specified it yet. This feature needs one thing from whoever does:

> **Requirement for the Oath's spec:** when a Pokémon faints under the Oath, move it to a locked Pithos jar, **the Urn**, rather than releasing it. The Urn keeps species, nickname, level and met location.

Then the Riverside reads the Urn.
- **Up to six of your fallen** stand by the river as shades: their follower sprites (`OW_POKEMON_OBJECT_EVENTS`), with no shadow and the shade palette blend.
- **Talk to one:** its cry, softly. Then:
  ```text
  {STR_VAR_1} doesn't remember the battle.

  It remembers you.
  ```
  ?? SAY GOODBYE / STAY A WHILE
- **SAY GOODBYE:** it turns and walks toward Elysium's gate, and fades. Its Urn entry is marked "at rest" and can't be brought back: the Oath forbids it, and so does the myth.
- **STAY A WHILE:** you stand together. Nothing else happens. You can come back.
- **If more than six fell,** the six most recent come, and a line says "Others are further along. They're all right."
- **Engine:** an object per slot with a variable graphics id set from the Urn entry's species (`OBJ_EVENT_GFX_SPECIES`), and the nickname buffered. Low–Medium, once the Oath exists.

### Obols

| Use | Cost |
|---|---|
| Your fare | 1, or none after theoxenia E11 |
| Each unburied shade | 1, up to 5 |
| The Cutter | 0. Charon knows her. |

Bronze Obols are dig finds in Acts I and II (SYSTEMS §5: 18% and 12%), so most players arrive with several. Cape Tainaron's dig spots add them back for latecomers.

### Kerberos's heads

Each head's "out" state is a temp flag set on that map: `FLAG_TEMP_1` to `_3`. The battle reads them to build the totem boost.

### The don't-look-back rule

As §4.13. Two details:
- **Menus are fine.** Opening the start menu or the Bag doesn't turn you.
- **Bumping a wall doesn't count.** Only a facing change to south does.

---

## 6. Encounters

The Underworld ignores time of day. Levels follow BALANCE.md's Aethos post-game row (wild 55–70). The Underworld is in Aethos, so its tables use **Aethos species only**: every non-Aethos species lives in the Oikoumene (BALANCE.md; POSTGAME §4). That's a fair constraint here, because the Aethos dex already has a full underworld: the Obolorn line, Stygiad, Elegull, Persenyx, Bouldyphus, Echolali and the Cutter's kin.

| Map | Levels | Species |
|---|---|---|
| The Mani Road | 60–64 | Lykopup 15%, Lykanax 5%, Hoplomex 10%, Laolith 5%, Cairnolith 15%, Ergant 10%, Alekrow 10%, Basilops 5%, Obolorn 25% (night, until the doors open) |
| Cape Tainaron | 60–64 | Galenyon 20%, Halcyling 20%, Karkipool 20%, Dakrock 5%, Obolorn 25% (night), Kalyptor 10% (night) |
| The Descent | 62–66 | Kalyptor 25%, Obolorn 25%, Elegull 15%, Cairnolith 15%, Spalunk 10%, Prosomime 5%, Bouldyphus 5% |
| The Acheron Bank | 63–67 | Obolorn 40%, Kalyptor 30%, Elegull 20%, Stygiad 8%, Charonaut 2% |
| The Styx (fishing only) | 64–68 | Stygiad 35%, Kalyptor 25%, Ketofry 20%, Kynoketos 15%, Charonaut 5% |
| The Meadows of Asphodel | 64–68 | Elegull 20%, Kalyptor 15%, Obolorn 15%, Persenyx 10%, Amnoze 15%, Echolali 10%, Prosomime 10%, Seirenade 5% |
| The Plain of Lethe | 65–69 | Echolali 25%, Amnoze 20%, Prosomime 15%, Kalyptor 15%, Elegull 15%, Kerdovix 5%, Psychora 5% |
| The House of Hades's garden | 66–70 | Persenyx 25%, Rhoaril 20%, Korantha 10%, Plouteras 10%, Spalunk 15%, Narcibulb 10%, Ophidrop 10% |
| Tartarus | 66–70 | Bouldyphus 15%, Gigantomb 15%, Kapnub 20%, Cairnolith 15%, Laolith 10%, Kolossard 10%, Pyrapod 15% |
| Elysium | 66–70 | Psychora 15%, Himerow 15%, Korantha 10%, Hymnaria 10%, Kalliglyph 10%, Sophowl 10%, Kerastorm 10%, Melisseer 10%, Chionyad 5%, Aphrogene 5% |
| Elysium's Shore (fishing) | 66–70 | Aphrogene 25%, Narkeray 25%, Galenyon 20%, Kynoketos 15%, Aphrell 10%, Haligeron 5% |

The existing species the earlier draft used here (Basculegion, Dusknoir, Trevenant, Cofagrigus, Togekiss and others) belong to the Oikoumene's tables. Trainers' teams in the Underworld (Hades, Persephone, the shades) may still use existing species, as the post-game allows.

**Stretch, the House of Night:** Cresselia (Lv 78) and Darkrai (Lv 78), one each, in Nyx's house at Tartarus's edge, where Sleep and Death live with their mother (Hesiod, *Theogony* 744–757). The bible casts them as Hypnos and Nyx (PITCH §4).

---

## 7. Species casting and substitutions

| Bible | Ichor | Kind | Why |
|---|---|---|---|
| Basculegion, souls of the drowned (§6.2) | **Stygiad** (#134) | **Substitution** | The dex's Styx Pokémon is the Oath's emblem. Basculegion, a non-Aethos species, lives in the Oikoumene (BALANCE.md). |
| Cerberus (Mega Houndoom) | **Pylakyon** (#6), as Kerberos | **Substitution** | As LABORS §5. The Houndoominite comes from Labor 12. |
| The Regis, "the Titans of Tartarus" | The Regis, each named as a Titan: Krios, Koios, Iapetos, Hyperion, Menoitios, with Regigigas as **Briareus** | Kept, with new identities | Legendaries. Regigigas as their jailer fits its legend of pulling the others into place. |
| Giratina, "Hades and the Underworld" | Giratina as **Tartaros**, the primordial pit | Kept, refined | Hades is a character, so his Pokémon can't be him. Tartaros is a primordial (Hesiod), which links Giratina to the Primordials arc (POSTGAME §3). |
| Charon (no Pokémon named) | Charon is a person; the **Obolorn line** is the shades who'd like to be him | New | The dex's Charonaut is "Charon fused to his boat", so wild Charonaut are rare and Charon himself is human. |
| Cresselia and Darkrai (Hypnos and Nyx) | In the House of Night | Kept (stretch) | — |
| — | **Nekranax** (#151) in the vault beneath the hall | From the dex | Dex D4's suggestion, unsealed by the bident lot |
| — | **The Cutter** (Thanira, #145) as your guide | From the dex and STORY §3 | Not a battle. She travels as an escort, or from your party. |

---

## 8. Rewards

| Where | Reward |
|---|---|
| Eleusa | The Gold Leaf |
| Cape Tainaron | Hidden: a Spell Tag behind the temple; dig spots |
| The Descent | TM Shadow Ball, Max Revive, Reaper Cloth |
| Paying the unburied | Spell Tag, Cleanse Tag, Reaper Cloth, Revive, Pearl (one each), Hades +1 each |
| The Styx | Stygiad |
| The Meadows | Icarus's Feather; TM Hex; a hidden Dusk Stone by the Danaids' well |
| Minos | Prize money; TM Stealth Rock |
| The Lake | Mnemosyne's Water (Ichorin's lead) |
| Hades and Persephone | The Key of Hades; Persephone's pomegranate; TM Poltergeist |
| Tartarus | Five Titans; Briareus; Sisyphus's room (Gold Stater, Rare Bone, TM Stone Edge, Reaper Cloth); Bouldyphus |
| The Chasm | Giratina; the Griseous Core |
| The verdict | The Helm of Darkness back; Hades's altar; Hades Favor +15; Labor 12's permission |
| Elysium | The Isles' hidden Ichor Stone; the finished lullaby for the music player; Medon at rest |
| Spring | First Fruits ×5, Demeter Favor +10; Eleusa green; theoxenia E12 |
| Theano's reply, to Phaedon | Phaedon's scene; a Sacred Ash from the Asclepeion ("She'd want you to have it.") |
| Agis and Kyniska's message, to Lampito | Rhea's scene; her old Cairnolith's Everstone ("He never needed to grow. Neither did they.") |
| Icarus's Feather, to Daedalus | **The Wings learn the way to your ship:** Daedalus's Wings can land at your trireme's anchorage (ODYSSEY §2). Plus a short scene. |
| After | **The Vault beneath the Hall** opens with the bident lot (dex D4): Nekranax |

## 9. Music

| Cue | Use | Mode and feel |
|---|---|---|
| The Mani Road | Route | Dorian, a dry 7/8 with a bell on the off-beat. The last aboveground drum. |
| Cape Tainaron | The cape | **Orpheus's lament** introduced: a lyre alone, Hypodorian, slow |
| The Descent | Caves | A low aulos drone and water drips |
| The Styx | The crossing | **No music.** The pole, the water, Charon breathing. |
| The Gate | Kerberos | Three low notes in a cycle, one per head; each head that sleeps drops its note |
| The Meadows of Asphodel | Hub | Mixolydian, lyre and a soft string pad, no percussion, very slow |
| Shade battle | Wild and trainer battles below | The trainer theme, drumless, with a breathy aulos lead |
| The Crossroads | Judgment | Three stately chords, Dorian |
| The Plain of Lethe | Fog | Almost nothing; a melody that starts and forgets itself after four bars, then starts again |
| The Lake of Mnemosyne | Memory | The Ichor main theme, quiet, in Lydian: the first time it plays below |
| The House of Hades | Hall | Phrygian, a slow 5/4, dark kithara and a pomegranate-bright aulos |
| Hades and Persephone | Battle | A royal theme in 7/8 with two interlocking lines, his low and hers high |
| Tartarus | The Titans | **The drum returns:** a bronze anvil in 9/8 (zeibekiko), with low aulos and grinding strings |
| Titan battle | The five, and Briareus | The Regi idea re-voiced: anvil, drone and a five-note figure |
| The Chasm | Giratina | The Tartarus theme played backward (a stretch: reversed sequence data) |
| Elysium | Gold | Lydian, kithara and choir, the warmest music in the game |
| The Ascent | Don't look back | Orpheus's lament, building. It drops to one note at landing 3 and returns. |
| Spring | Eleusa, after | The Eleusa town theme with a new flute descant |

About **16 new tracks.**

---

## 10. Scenes

Dialogue in SCRIPT.md's format: one box per line, `[brackets]` are directions. The Fates' name boxes read CUTTER (STORY decision S10).

### Scene 1. Eleusa: the gray fields

[A field of wheat, every stalk gray. Chloe stands in the middle holding one ear.]
```text
CHLOE: It's past the Mysteries. She should have come up a month ago.

CHLOE: Every year she comes up, and every year it's spring. Not this year.

CHLOE: Hades has shut his doors. Nothing in, nothing out. Not even her.

CHLOE: You're the Archon now. People expect you to do something. I'm people.

CHLOE: And you've no thread. The doors are all locks. You're not a lock.

CHLOE: Here. We bury our initiates with these.

{PLAYER} received the Gold Leaf!

CHLOE: You're not dead. Take it anyway. Cape Tainaron. South of Lakonia.
```

### Scene 2. Before the descent

[Akti's Asclepeion. Phaedon heals your party, as he does every time now. Elpis is asleep on a cot behind the counter, her Ophidrop coiled at her feet.]
```text
PHAEDON: Easy now. There.

PHAEDON: Ione says you're going down to Tainaron. To the doors.

PHAEDON: I can't go. I can't leave the island. That's fair.

PHAEDON: If you see Elpis's mother… her name is Theano. Tell her one thing.

PHAEDON: Tell her Elpis finished the song.

PHAEDON: That's all. She'll know what it means.
```
[Lakonia, Lampito's house. Rhea sits on the step, unhelmeted, mending a sandal.]
```text
RHEA: Going under? Hm.

RHEA: Two of mine are down there. A boy and a girl.

RHEA: …If they ask. Only if they ask. Say their mother's well.

RHEA: Say she stopped standing still.
```
[Cape Tainaron, at night. Small gray shades crowd the bronze gate. Among them, floating a little above the rock, a figure in a solid black chiton holds a pair of closed shears. The Cutter.]
```text
CUTTER: Unwoven.

CUTTER: I cut every one of them. Every thread in Aethos, for a thousand years.

CUTTER: I knew each ending before it began. I loved every one.

CUTTER: I never once saw where they went.

CUTTER: I'd like to see where they went. Will you take me?
```
[If she's in your party, she comes out of her ball for this, and says the last line differently.]
```text
CUTTER: I'll walk. I've never walked anywhere.
```

### Scene 3. The Acheron: Charon

[A reed boat noses into the bank. A gaunt old man leans on a pole and looks at you, then down at your feet.]
```text
CHARON: Coin.

CHARON: …You've a shadow. And no thread. Can't tell if you're coming or going.

CHARON: That's a wished-on coin. From a well. Those carry further down here.

CHARON: Hand, not tongue. I'm not fussy.
```
[If theoxenia E11 is done.]
```text
CHARON: Oh. You. You paid an old man's fare by a river once.

CHARON: That was your coin. And the master. He told me. Get in.
```
[He sees the Cutter, and for the first time looks surprised.]
```text
CHARON: You.

CHARON: You've sent me more fares than anyone. Never come yourself.

CUTTER: No.

CHARON: …Get in. Both of you. Don't touch the water.

CHARON: Bring food if you've got it. Nobody sells anything down there.
```
[The unburied, crowding the reeds.]
```text
CHARON: Those? Nobody buried them. Nobody paid. A hundred years, they wait.

CHARON: I don't make the rules. I just row.
```
?? PAY FOR ONE / NOT NOW
```text
> PAY FOR ONE:
The little shade closes its hand around the coin. It doesn't let go.
```

### Scene 4. The Styx: the Oath

[Midstream. A pale shape rises beside the boat: a Stygiad, a girl of ice holding a jug of black water. She looks at you.]
```text
CHARON: This is the Styx. The gods swear on it. Break an oath on this water…

CHARON: …and even a god lies breathless for a year. I've seen it. Hilarious.
```
[If the player swore the Oath of the Styx.]
```text
CHARON: You swore on it too. At the start. I heard. Everybody down here heard.

CHARON: Some of yours came over already. You kept to it. Most don't.

CHARON: You can keep it. Or let it go. The river doesn't mind. Oaths end.
```
?? KEEP IT / LET IT GO
```text
> KEEP IT:
CHARON: Good.

> LET IT GO:
CHARON: Done. That's what makes it an oath, you know. That it can end.
```

### Scene 5. The Gate

[Under the black arch, a hound the size of a house lies across the road. Three heads lift, one after another.]
```text
CUTTER: The left one's looking at your bag. The middle one's listening.

CUTTER: The right one hasn't blinked since we arrived.

CUTTER: He's never let anyone past who wasn't dead. You're not anything.
```

### Scene 6. The Meadows: Medon

[Lethe's bank. Pale water. A tall shade in an old-fashioned purple-bordered robe stands very straight at the edge, as if waiting to be announced. He has been standing there for a thousand years.]
```text
MEDON: You're living. And you've no thread. And you carry yourself like…

MEDON: Oh. You're Archon. Of course you are. I can always tell.

MEDON: I was the first. Medon. Son of Kodros.

MEDON: My father walked into the spears because an oracle said a king must die.

MEDON: The city lived. I made sure no oracle could ever be wrong again.

MEDON: I chained them. The Fates. I cried the whole night. Did you know that?
```
[The Cutter, behind you, is very still. Medon doesn't look at her.]
```text
MEDON: There was a knot. In a box. Do you have it? Did you tie it?
```
?? WE UNTIED IT / IT'S GONE
```text
MEDON: …

MEDON: Untied. After a thousand years. By the Archon.

MEDON: Then I suppose I'll never know if it would have worked.

MEDON: My father's in the gold fields. Everyone says so. I haven't gone.

MEDON: If I go, I'll have to ask him. If the oracle was wrong, he died for nothing.

MEDON: I've stood here so I wouldn't have to know. It's very restful, not knowing.

CUTTER: No. It isn't.
```

### Scene 7. The Meadows: Agis and Kyniska

[In the asphodel, a young man in a Lakonian red cloak, a spear wound under his arm, sits with a small girl in a shawl. She is braiding asphodel stems.]
```text
KYNISKA: You've got a shadow! Agis, look. A shadow.

AGIS: I see it. Don't touch.

KYNISKA: Are you from Lakonia? Do you know our brother? He came after us.

KYNISKA: We never met him. Mama said he coughed.

AGIS: She hid it. With shields. She told me she'd do that if there was another.
```
?? HE'S FINE / HE'S DOING THE LABORS / HE CAME SECOND TO A WOOLOO
```text
> HE'S FINE:
KYNISKA: Fine's good. Fine's very good.

> HE'S DOING THE LABORS:
AGIS: Like Herakles? That idiot. Good.

> HE CAME SECOND TO A WOOLOO:
KYNISKA: Ha! A Wooloo! Agis, he's like you.

AGIS: I came second to a goat once. It was a fast goat.
```
[If the player visited Rhea first.]
```text
{PLAYER} gives them their mother's words.

AGIS: …She stopped standing still?

AGIS: Then tell her we're not waiting. Tell her we're fine here.

KYNISKA: Tell her the flowers are boring but the company's good.
```

### Scene 8. The Meadows: Icarus

[At the cliff edge, where the gray grass ends in dark air, a boy sits with his knees up, picking at a feather.]
```text
ICARUS: Are you from up there? Is it still bright?

ICARUS: I went up too far once. Then down too far. Now I'm here.

ICARUS: My father makes things. Daedalus. Do you know him?
```
[If the player flew the Icarus Shaft.]
```text
ICARUS: You flew? In his wings? And you came down? On your feet?

ICARUS: …He made them right, then. He always made them right.

ICARUS: It was me. I wanted to see the sun's face. You can't. It's just bright.

ICARUS: Give him this. He'll know which one it is.

{PLAYER} received Icarus's Feather!
```
[If not.]
```text
ICARUS: Does he still build things? Does he still laugh at his own jokes?

ICARUS: Give him this. Tell him I'm not cold.

{PLAYER} received Icarus's Feather!
```
[Later, at Daedalus's workshop on Knossa.]
```text
DAEDALUS: …

DAEDALUS: That's his. That's the one I glued crooked. He wouldn't let me fix it.

DAEDALUS: Wax still on it. Twelve years.

DAEDALUS: Give me your Wings a moment. I'll teach them where your ship is.

DAEDALUS: No reason. I just want something of mine to find its way home.
```

### Scene 9. The Meadows: Tiresias and the image of Herakles

[A blind old man leans on a staff by a dry stream.]
```text
TIRESIAS: Another visitor. The last one wanted to know the way home.

TIRESIAS: I used to see everything. Every road. Every end.

TIRESIAS: Now it's dark. Just dark. You've no idea how restful it is.

TIRESIAS: I still remember things. A city under the sea, that sank in a day.

TIRESIAS: That's not a prophecy. It's just a memory. I've only those now.
```
[A tall shade with a bow, standing perfectly still.]
```text
SHADE OF HERAKLES: I'm not him. He's on Olympus with the gods. I'm what was left.

SHADE OF HERAKLES: How many have you done? Labors. I can tell. You've the look.
```
[He counts on his fingers, aloud, to the number done.]
```text
SHADE OF HERAKLES: Twelve? …Then I can stop counting.
```

### Scene 10. The Crossroads: the Cutter's question

[After the judgment and Minos's battle. The Cutter floats up to the three stones.]
```text
CUTTER: Are they angry with me? The ones I cut?

RHADAMANTHYS: Some. Not many.

RHADAMANTHYS: You never cut early. You only ever seemed to.

AIAKOS: Most of them never thought about you at all. Is that worse?

CUTTER: …I don't know. I've never not known before.
```

### Scene 11. The Lake of Mnemosyne

[Cold, clear water in a ring of silver stones. Two guards in pale armor cross their spears.]
```text
GUARD: Who are you? Where are you from?
```
?? A CHILD OF EARTH AND STARRY SKY / {PLAYER} OF ELAIA / NOBODY'S. MY THREAD IS MY OWN.
```text
> A CHILD OF EARTH AND STARRY SKY:
GUARD: Drink.

> {PLAYER} OF ELAIA:
GUARD: Names are for up there. Try again.

> NOBODY'S. MY THREAD IS MY OWN.
GUARD: …

GUARD: That isn't the answer.

OTHER GUARD: It's a better one.

GUARD: Drink.
```
[You drink.]
```text
You remember.
```
[The Cutter touches the water with one finger, and doesn't drink.]
```text
CUTTER: I remember all of them already. That's the job.

CUTTER: A fisherman in Akti. A girl in Thyrsa who laughed at the end.

CUTTER: A king in a peasant's cloak, in the spears. I remember him best.
```

### Scene 12. The House of Hades

[A black basalt hall. A dark bronze throne. Hades sits, chin on fist. Persephone stands among pale pomegranate trees behind him, with a pruning knife.]
```text
HADES: A living one. In my hall. With no thread. And the Archon, I'm told.

HADES: You're the one who freed the Fates. I've been meaning to complain.

HADES: Since the Loom came loose, nothing down here sits still.

HADES: My uncles hit the gates the hour their brother woke. They haven't stopped.

HADES: So I shut every door. Nothing in. Nothing out.

PERSEPHONE: Including me. It's been a long winter up there, I hear.

HADES: I won't open them while those old men are rattling.

PERSEPHONE: Then let's find out why they rattle.

HADES: Nobody goes into Tartarus.

PERSEPHONE: Nobody with a thread.
```
[Hades looks at you for a long time.]
```text
HADES: …Show me you can hold what's down there. If it gets out.
```
[After the battle.]
```text
HADES: Hm.

HADES: Take this. The key to the house under the house.

{PLAYER} received the Key of Hades!

HADES: Find out what they want. Then make them stop.

PERSEPHONE: Pomegranate? They're very good this year. Nobody's eaten any.

CUTTER: Don't eat anything down here. I've cut the ones who did.

PERSEPHONE: She's no fun. Take it for later, then.
```

### Scene 13. The verdict

[The hall. Hades stands, which he never does. Persephone is trying not to smile.]
```text
HADES: You let them out.

HADES: All of them. Krios. Koios. Iapetos. Hyperion. Menoitios. Even Briareus.

HADES: They're walking up through the dark toward the sun. My prisoners.

HADES: Zeus put them there. For ever, he said.

PERSEPHONE: "For ever" was a prophecy, love. Those are over.

HADES: …

HADES: They stopped rattling.

PERSEPHONE: People do, when you open the door.

HADES: Fine. Open the doors. Let the dead in.

HADES: Minos says this is yours. It's mine. The Cyclopes made it for me.

HADES: Keep it. I never liked how I looked in it.
```
[If Olympias has set Labor 12.]
```text
HADES: And Hera's woman wants my dog. For a labor. Of course she does.

HADES: Fine. No weapons. Bring him back by evening. He gets fretful.
```
[Persephone, already in a traveling cloak.]
```text
HADES: And you'll be going up.

PERSEPHONE: It's spring, love. It's very late spring.

HADES: Then it's done the old way. She follows you up, Archon. You don't look back.

HADES: Not till she's in the sun. Turn round on the stair, and she's mine another year.

PERSEPHONE: He loves this part. Ask Orpheus. Actually, don't.
```

### Scene 14. Elysium: Theano

[Golden grass. A low sun that doesn't move. A woman sits under a white poplar, rolling a bandage. She looks up.]
```text
THEANO: Oh. You're the one with no thread. The whole of Elysium's been talking.

THEANO: Did Phaedon send you? He did, didn't he. He'd never come himself.

THEANO: He'd think it wasn't allowed. He's very good at not being allowed.
```
?? ELPIS FINISHED THE SONG
```text
THEANO: …

THEANO: She finished it?

THEANO: I made that song up as I went along. Every night a bit more.

THEANO: She always fell asleep before the end. So I never wrote one.

THEANO: How does it end? Can you…
```
[No words. The lullaby plays, all the way through, to the last note: the version Elpis finished. Theano listens with her eyes closed.]
```text
THEANO: Oh. That's better than mine would have been.

THEANO: Tell him… tell him to stop sitting so far away from her.

THEANO: He always sits too far away when he thinks he's done something.

THEANO: And tell him I'm not waiting. I'm busy. There's a lot of people here.
```

### Scene 15. Elysium's gate: Medon and Kodros

[The Crossroads' third gate, its gold leaves untied. Medon has followed you from the river, and stops a step short of it. On the other side, a broad old man in a coarse peasant's cloak stands up from a stone.]
```text
KODROS: Medon.

MEDON: Father.

MEDON: I have to ask. I've had a thousand years and I still have to ask.

MEDON: The oracle. Did it kill you? Was it true? Did you die because it said so?
```
[Kodros comes to the gate. He is shorter than his son.]
```text
KODROS: It wasn't the oracle. I chose.

KODROS: An oracle can say a king must die. It can't say which king. It can't walk.

KODROS: I put on the cloak myself. I walked out myself.

KODROS: You chained them for that? Oh, son.

MEDON: …I cried the whole night.

KODROS: I know. I heard. Come in. It's warm.
```
[Medon goes through the gate. He doesn't look back. Then he does, once, at you.]
```text
MEDON: Archon. Thank you for untying it.

MEDON: Don't tie anything. Whatever they ask you. Whatever you're afraid of.
```

### Scene 16. Elysium: Orpheus

[By the river, a young man plays a lyre for nobody. The grass leans toward him.]
```text
ORPHEUS: You're going up the stair. I can tell. Everyone looks at it like that.

ORPHEUS: I went up it once. She was right behind me. I couldn't hear her.

ORPHEUS: I was sure she'd gone. So I looked.

ORPHEUS: She hadn't. She was right there. And then she wasn't.

ORPHEUS: If the footsteps stop, they haven't stopped. Remember that.
```

### Scene 17. The stair's foot: the Cutter stays

[The bottom of the Ascent. Persephone waits a little way off. The Cutter turns her closed shears over in her hands.]
```text
CUTTER: I'll stay down here a while. I owe them each a visit.

CUTTER: I used to know when every one of them would come.

CUTTER: Now I won't. I'll cut, and I won't know it's the end until it is.

CUTTER: Like a person. That's what they kept telling me down here.

CUTTER: Go up. I'll come to the forge when I'm done. Or to you.
```

### Scene 18. The Ascent: what Persephone says behind you

Each line plays at a landing, from behind. No portrait; the name box only.
```text
PERSEPHONE: [landing 1] You're very quiet. Orpheus sang the whole way. It was a lot.

PERSEPHONE: [landing 2] Narcissus. Down here? I'll be one moment.

PERSEPHONE: [landing 3, the footsteps stop] …

PERSEPHONE: [after a pause] Sorry! Still here. It had a bee on it.

PERSEPHONE: [landing 5, after Hades's voice] He does that every year. I never go back.

PERSEPHONE: [landing 6] Would you like a pomegranate seed? Just one. For the road.

PERSEPHONE: [landing 7] People think spring is a present. It isn't. It's a return.

PERSEPHONE: You go down. You come back up. That's all it ever was. That's the secret.

PERSEPHONE: Your mother knows it. She's been saying it to you since you left.
```
[She steps past you into the light.]
```text
PERSEPHONE: There. You can turn round now, Archon.
```
[Behind her, all the way down the stair, the cracks in the rock are green.]

### Scene 19. Akti: Phaedon and Elpis

[The Asclepeion. Phaedon heals your party. Elpis sits on the counter with her clay bull and her starter from the Klotheia.]
```text
PHAEDON: Easy now. There.

PHAEDON: …Did you see her?
```
?? SHE SAYS STOP SITTING SO FAR AWAY
```text
PHAEDON: …

PHAEDON: That's her. That's exactly her.
```
[He gets up, goes round the counter, and sits down right next to Elpis. She leans on him without looking up.]
```text
ELPIS: Papa, you're squashing Starry.

PHAEDON: Sorry.

PHAEDON: She said she's busy. She said there's a lot of people there.

ELPIS: Mama was always busy. I remember that. And the well.
```

### Scene 20. Lakonia: Lampito

[Rhea's step. If Kleon is visiting, he's at the well with a bucket.]
```text
RHEA: Well?
```
?? THEY SAID THEY'RE NOT WAITING
```text
RHEA: …

RHEA: Not waiting.

RHEA: Good.
```
[She puts down the sandal she's been mending. She doesn't pick it up again for a while.]
```text
KLEON: [if there] Who's not waiting?

RHEA: Agis and Kyniska.

KLEON: …You never say their names.

RHEA: I'm saying them now. Sit down. Fewer words won't do for this one.
```

---

## 11. Art list

### Tilesets

- **`underworld`** (new secondary): the Descent's basalt; the Acheron's black water and gray reeds; the Gate; the Meadows' asphodel (tall grass), cypresses and the Danaids' well; the Crossroads' three gates; Lethe's standing stones and white cypresses (and their "shifted" twins); Mnemosyne's silver stones; Tartarus's bronze walls, the Phlegethon (animated fire channel), five cell interiors, inscription walls (carved-text metatiles, 4 variants), the bronze gates; the Chasm's upside-down tiles. Palettes: basalt, black water, asphodel violet, fog white, silver-blue, bronze and ember, chasm violet. That is 7, one more than a secondary normally carries, so the Chasm borrows the asphodel palette with an inverted ramp.
- **`elysium`** (new secondary): gold grass, white poplars, clear river, the Isles' gold sand and shells, the House of Hades's garden (pomegranate trees, white poplars, the throne hall). Palettes: gold grass, poplar white, river, pomegranate, basalt, sky-gold, spare.
- **Cape Tainaron** uses the aethos primary plus the Lakonia secondary, with the bronze gate of locks added (a 3×3).

### Sprites and portraits

| Who | Overworld | Portrait |
|---|---|---|
| Charon and his boat | 32×32 (in the boat) | 64×64 |
| Hades | 16×32 | 64×64 |
| Persephone | 16×32 | 64×64 |
| Minos, Rhadamanthys, Aiakos | 16×32 each | Minos only |
| Medon | 16×32, in an old purple-bordered robe | 64×64 |
| Kodros | 16×32, in a peasant's cloak | 64×64 |
| Agis and Kyniska | 16×32 each (Agis reuses the Lakonian class walker, recolored) | — |
| Icarus | 16×32 | — |
| Theano | 16×32 | 64×64 |
| Tiresias, Ajax, Orpheus, the image of Herakles | 16×32 each | Orpheus only |
| Mnemosyne's guards | 16×32 | — |
| Shade trainers | Existing class walkers and portraits, **shade palette** (a gray-violet blend) | Existing, palette-swapped |
| Kerberos at the gate | 64×64 (shared with Labor 12) | — |
| The Cutter (escort) | Her dex follower sprite (Thanira, #145) | — (a Pokémon; the name box only) |
| The Titans' shades | The Regis' follower sprites, shade palette | — |

### Objects and effects

- The bronze gate of locks (opening animation, 4 frames).
- The shade palette blend for object events (the same alpha-blend the Helm of Darkness uses on the player, LABYRINTH §5.4).
- The Fall: a full-screen falling sequence (palette flashes; reuse the screen-fade effects).
- Item icons: the Gold Leaf, the Key of Hades, Mnemosyne's Water, Icarus's Feather, the Griseous Core (the expansion's icon, recolored).

### Battle backgrounds

- **The Meadows** (gray-violet), **the Styx** (black water), **the hall** (basalt and pomegranate), **Tartarus** (bronze and fire), **the Chasm** (violet void), **Elysium** (gold). Six new.

### Pictures

- One full-screen picture, 240×160: the view up the Ascent into the light, shown as Persephone steps into the sun (scene 18). About 15 KiB.

---

## 12. ROM estimate

| Item | Size |
|---|---|
| 27 maps (layouts and events) | ~110 KiB |
| Two new tilesets and the cape's additions | ~50 KiB |
| Scripts and text (about 700 lines, plus the judgment tables) | ~85 KiB |
| Portraits (9) and overworld sprites (about 14 sheets) | ~35 KiB |
| Battle backgrounds (6) | ~40 KiB |
| Music (about 16 tracks) | ~55 KiB |
| The Ascent picture, item icons, effects | ~20 KiB |
| **Total** | **~395 KiB** |

---

## 13. Flags and vars

**Vars: one.**

| Var | Holds |
|---|---|
| `VAR_ICHOR_KATABASIS` | Story state 0–20: Eleusa asked, the cape, the Cutter joined, the gate open, the Styx crossed, Kerberos passed, the Meadows, judged, Lethe crossed, Mnemosyne drunk, the hall, the key, Tartarus entered, the Chasm, the verdict, Elysium, Medon at rest, the Ascent done, spring |

**Save data** (`IchorSave.epics`, POSTGAME §6):
- `titans` (u8): 6 bits, which cells are open, and which Titans are caught or out in the world.
- `shades` (u16): Medon, Agis and Kyniska, Icarus, Tiresias, the image of Herakles, Theano, and up to five unburied paid for.
- `oathAtRest` (u8): how many of the Urn's entries have said goodbye (the Urn itself holds the marks).

**Flags** (about 30, `FLAG_ICHOR_*`, from freed Hoenn story flags):

| Group | Flags |
|---|---|
| Items | `GOT_GOLD_LEAF`, `GOT_KEY_OF_HADES`, `GOT_MNEMOSYNE_WATER`, `GOT_ICARUS_FEATHER`, `GAVE_ICARUS_FEATHER`, `GOT_GRISEOUS_CORE` |
| Messages | `PHAEDON_MESSAGE` (asked), `THEANO_REPLY` (carried back), `RHEA_MESSAGE`, `AGIS_REPLY` |
| Story | `UNDERWORLD_DOORS_SHUT` (set after the epilogue, cleared at the verdict), `SPRING_RETURNED`, `OATH_LAID_DOWN`, `HELM_WITH_MINOS`, `HADES_ALTAR`, `ELYSIUM_OPEN`, `MEDON_AT_REST`, `CUTTER_GUIDE`, `ICHORIN_POOL` |
| Encounters | `KERBEROS_GATE_PASSED`, `STYGIAD_STYX`, `BRIAREUS`, `GIRATINA`, the five Titans' caught-or-roaming flags, `BOULDYPHUS`, `SISYPHUS_DOOR` |
| Hide flags | About 12: the Gate's sleeping heads, the shades, Theano, Kodros, the gray-wheat variant |

---

## 14. Proposed changes

**What changed when STORY.md was approved** (STORY.md wins; listed so the director can check):
1. **Phaedon no longer goes down.** STORY's sentence exiles him to Kalliste for life (decision S8). The **Cutter** guides you instead (STORY §3: "Thanira can guide you down"), and Phaedon sends a message (STORY §3's optional hook).
2. **The Orpheus moment** is now **Persephone's return**: she follows you up, and spring depends on it. The earlier draft had Phaedon leading his dead wife. That came too close to a resurrection story, which STORY §3 rules out, and it needed Phaedon to travel.
3. **Halia lives.** STORY's epilogue has her reading threads at the next Klotheia, so her shade scene and her death (the old decision K1) are gone.
4. **Medon and Kodros** are added (STORY §2 and §3): Medon at Lethe's bank, Kodros at Elysium's gate, and "It wasn't the oracle. I chose."
5. **Charon takes the Elaia well-coin** specifically (STORY §3).
6. **Agis and Kyniska,** Kleon's elder brother and sister, are new, from STORY's Rhea bible. Their names are this file's proposal.
7. **The Golden Bough** is cut: nobody living needs it now.
8. **You're the Archon** throughout (STORY decision S7).
9. **Levels and species** follow BALANCE.md: the Aethos post-game row (wild 60–70 here, bosses 72–80), and Aethos species only in the wild tables, because every non-Aethos species lives in the Oikoumene (§6).
10. **Legendaries placed here,** for LEGENDS.md to reconcile: Regirock, Regice, Registeel, Regieleki and Regidrago (Tartarus, Lv 75), Regigigas (Lv 80), Giratina (Lv 80, with the Griseous Core), Nekranax (the vault, with the bident lot), and, as a stretch, Cresselia and Darkrai (the House of Night, Lv 78). Ichorin's lead starts here (Mnemosyne's Water).

**To PITCH.md:**
1. **§6.2, Katabasis.** "Spring hasn't come: Hades has barred the Underworld since the Titans felt the Lord of Time wake. With Chloe's gold leaf, and the Cutter as your guide, you cross the Styx, pass Kerberos, and meet the shades: Medon, the first Archon, who learns from his father Kodros that it wasn't the oracle. You cross Lethe to Mnemosyne and face Hades and Persephone. In Tartarus you free the five Titans (the Regis) and their jailer Briareus (Regigigas), and meet Tartaros itself (Giratina). Elysium opens. You lead Persephone up the stair into spring, and don't look back."
2. **§4, the myth table.** "Hades and the Underworld: Giratina" becomes "Tartaros, the primordial pit: Giratina".

**To STORY.md** (small, for the story lead): name Elpis's mother **Theano**, and Kleon's elder siblings **Agis** and **Kyniska**.

**To SYSTEMS.md:**
1. **§5, the dig table:** add Bronze Obol at 10% to Cape Tainaron's post-game spots.
2. **§10, E11:** E11's shade takes the Elaia well-coin, and at Charon's landing the fare is already paid (§4.4).
3. **§16.5:** Minos holds the Helm during the Katabasis; Hades returns it; the Helm of Hades upgrade stays Hades's Favor-60 gift.

**For whoever specifies the Oath of the Styx:** fallen Pokémon go to a locked jar, the Urn (§5).

---

## Decisions for the user

> **Settled by the user, 2026-11-14.** Asked directly: the Oikoumene opens in stages (PG-6, PG-7, PG-8); the Orpheus moment is Persephone's return, and nobody returns from the dead (K4); the five Titans and Briareus are freed (K3); the suitors stay, comic, with Mom in control (O3); Argos lives and joins you (O4); the legend castings are approved as a set (PG-31); the House of Night is built for 1.0 (PG-26, overriding K8's stretch). **Every other decision below takes its recommendation** (the user: "Take the recommendations"). Any can still be changed later.

- **K1. The Cutter as your guide** (recommended, from STORY §3), traveling as a scripted escort, or from your party if you caught her.
- **K2. Theano,** the name proposed for Elpis's mother, and Phaedon's message to her and her reply.
- **K3. Freeing the Titans.** The Katabasis frees the five Titans and Briareus, as the bible says, and frames it as ending the last "for ever". Hades objects and comes round. The alternative is to seal them again, which the bible doesn't want.
- **K4. The Orpheus moment is Persephone's return** (recommended): spring follows you up the stair. Nobody returns from the dead in Ichor.
- **K5. Your fallen.** On an Oath of the Styx run, the Pokémon who fell appear as shades you can say goodbye to. It needs the Oath to keep them in an Urn jar instead of releasing them.
- **K6. Letting the Oath go** at the Styx: an option to end the Nuzlocke rules there (recommended), or keep it binding.
- **K7. Giratina as Tartaros,** the primordial pit, rather than as Hades.
- **K8. The House of Night** (Cresselia and Darkrai) is a stretch goal, not 1.0.
- **K9. Kleon's siblings,** Agis and Kyniska, in the Meadows, with a message home to Lampito.
