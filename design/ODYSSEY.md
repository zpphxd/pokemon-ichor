# The Odyssey: the wine-dark sea

- **Owner:** Quest and level design.
- **Status:** a proposal for the user's approval. Nothing here is built yet.
- **Spine:** `design/STORY.md` §3, "The post-game spine": the Odyssey is **the long way home. Achilles's choice resolved: Kleon chose glory, and the hero chooses the homecoming.** Where this file and STORY.md disagree, STORY.md wins.
- **Umbrella:** `design/POSTGAME.md` (order, levels, save struct, scope).
- **Companions:** `design/SYSTEMS.md` (relics, including Aeolus's Bag; rites; xenia; theoxenia E1, E3, E13 and the finale at home), `design/LABORS.md` (Labors 8, 9, 10 and 11 use the ship), `design/UNDERWORLD.md` (Icarus's feather teaches the Wings to find the ship), `design/phase1/SCRIPT.md` (Mom, her loom and her honey jar; Nausikles and the *Euploia*; Glaukos; Amaryllis).
- **Species** come from the Aethos dex; the post-game may also use existing species (dex D5). Substitutions are flagged in §8.

---

## 0. The hook

The map used to stop at the sea's edge, because nobody was fated to sail past it. Now nobody is fated not to.

Captain Nausikles gives you the *Euploia*, the trireme that carried you off Kalliste at the start of everything. You fill her benches with people you met across Aethos, and sail west round Cape Maleia, where every old sailor says you forget your home. A storm takes you off the edge of the map.

You come to an island where nobody wants to leave, and you very nearly don't. You hide under a ram's belly to get out of a cave. A king of the winds gives you every wind in a bag and your own crew lets them out within sight of home. A witch turns your friends into pigs, and you have to become a pig to bring them back. You hear the Sirens, or you don't. In a narrow strait you choose what to lose. And then you come home, to a house full of strangers eating your mother's food, and an old dog by the gate who knows you first.

### Pillars

1. **The ship is home.** The *Euploia* has a bed, a hearth, a Pithos, a shop and a crew you know by name. For most of the voyage she is the only home you have.
2. **Sailing is a skill.** Wind, current, stars and fog decide how fast and where you go. A player who reads the wind gets there in half the time.
3. **Every island is one test.** Temptation, stealth, trust, transformation, desire, loss, hunger and kindness, each with its own mechanic.
4. **The crew are people.** You can lose some of them. You can always get them back.
5. **Truth and the story.** Odysseus gave you his chart, the Periplous, and it's mostly embellished. Alethea, whose name means *truth*, corrects it island by island. By the end you have the true chart, and Odysseus has to read it.
6. **Homecoming is the point.** Every mechanic on the way out pays off at the house in Elaia.

### At a glance

| | |
|---|---|
| Where in the story | Post-game. The ship and crew are available from the post-game's start; the voyage proper begins whenever you round Cape Maleia. Recommended after the Kotinos and Atlantis: it sits in BALANCE.md's Oikoumene row (POSTGAME §2). |
| Length | About 5 hours, plus crew recruitment (about 1 hour, optional beyond the required three) |
| Levels | `design/BALANCE.md`'s **Oikoumene** row, because the wine-dark sea lies outside Aethos: wild 70–78, trainers and bosses 74–81, Tornadus 75. Where the sea sits on the Oikoumene's map is for OIKOUMENE.md to reconcile (POSTGAME §4). |
| Maps | 27 new (§11), plus objects on Elaia and Akti |
| One way | Once you round Maleia, Daedalus's Wings don't work until you're home (§4). The ship carries everything you need. |
| Bosses | The great Polyphant (if spotted), Aeolus (optional), Tornadus, Circe, the Sirens (by one route), Hexylla and Trybdis, the Phaeacian games (optional), twelve suitors |
| Relic | **Aeolus's Bag** (SYSTEMS §1, relic 13): sail through fog banks |
| Unlocks | Free sailing on the wine-dark sea; Melitta's Cloak, lined; Argos; the true Periplous; with Labor 10, the route to Atlantis (POSTGAME §3); and the theoxenia finale's homecoming night (SYSTEMS §10) |

---

## 1. The frame

### Why the map got bigger

Before the climax, the known world ended at Aethos's western sea. Sailors turned back at Cape Maleia. That wasn't only fear: no thread ran past it.

After the Fates were freed, the fog to the west started to move. Fishermen at Akti see islands out there that weren't there before, or were always there and nobody was ever going to reach them. Alethea puts it best (scene 1): "The map stopped at Maleia because nobody was fated to go past it. Now nobody's fated not to."

This is the Odyssey's mythic license. These islands are the old story's islands, and Odysseus has been there. Now they're anyone's.

### Odysseus and his chart

**Odysseus** runs the Horse, the Olympiad's Factory facility, at Olympia (POSTGAME §3). He sailed this sea long ago and took ten years to get home. If you visit him before setting out, he gives you his sea-chart, **the Periplous of Odysseus**, a key item, and a briefing (scene 2).
- The Periplous marks every island, with his notes: "Cyclops. One-eyed giant. Asks your name. Say NOBODY."
- **Most of the notes are embellished.** Alethea checks each one against what's really there and writes "TRUTH:" under it. The Cyclops is a Polyphant, and it never asked anybody's name.
- **Without Odysseus's copy** you still get one: Nausikles has a copy. "Everyone has a copy. It's mostly wrong."
- **At the end** you bring the corrected chart back to Odysseus (§6.11).

### Who sails

| | |
|---|---|
| **The ship** | The *Euploia*, given by Captain Nausikles at Akti (scene 1) |
| **Required crew** | Nausikles (helmsman), Alethea (navigator and chronicler), the Lakonian oarsmen (twelve, lent by Kleon) |
| **Optional crew** | Seven more, recruited across Aethos (§3). Each brings a service, and each matters somewhere on the voyage. |

**Alethea's arc.** Alethea is Keeper of Records in Astyra now (STORY §3). She takes leave for the voyage: "The records have kept for a thousand years. They'll keep for a summer." She has kept the Pokédex and dug in ruins all game. Her tic is "Truthfully, …" (LABYRINTH §8). On the voyage she learns that the truth is sometimes stranger than the embellishment, and sometimes kinder. Her last line, at the homecoming, is about the dog.

### Glory or home

Achilles was offered two fates: a short life and undying glory at Troy, or a long one and a homecoming (*Iliad* 9.410–416). STORY §3 resolves it across the post-game: **Kleon chose glory** (the Labors), and **the hero chooses the homecoming.**
- **Achilles says so,** at the Stadion, before you sail (scene 2): "Your friend picked glory. Good for him. What'll you pick?" There's no menu. You answer by sailing.
- **The Sirens offer glory** (§6.6): to be sung forever, the undying song, *kleos aphthiton*, if you'll only come closer and stay.
- **The homecoming** is the answer: an old dog, a mother's question and a house.

### Mom is Penelope

STORY §3: "Penelope unweaves her loom at night, the Unwoven motif one last time. Mom is the Penelope figure." Melitta unspun her child's thread once to keep a fate off them (STORY §2). At the homecoming she unweaves again, every night, to keep a fate off herself (§6.11). The real Penelope, Odysseus's wife, comes to Elaia at the end and the two weavers compare notes (scene 16).

---

## 2. The trireme: home on the water

### The *Euploia*

The *Euploia* ("fair sailing", SCRIPT.md) has two maps. Both use the trireme deck tileset that ART_PLAN §1 already plans for the slice's crossing.

```text
  THE EUPLOIA: DECK (24x12), bow to the right
 +---------------------------------------------------------+
 |  [stern: Nausikles at the steering oars]                 |
 |   N   =  =  =  =  =  =  =  =  =  =  =  =  =  =   [bow]   |
 |   [chart table: Alethea]   (mast)   [Poseidon's altar]   |
 |   =  =  =  =  oarsmen's benches  =  =  =  =  =  =        |
 |   [hatch down]        [Lynkeus at the rail]   [ram]      |
 +---------------------------------------------------------+

  BELOW DECK (20x10)
 +--------------------------------------+
 |  [bunk]   [hearth: Lampon]  [mess]    |
 |  [Pithos: Kydon's hold] [Kydon's stall]|
 |  [trophy shelf]   [Phemios]  [Iaso]   |
 |  [Diktys's nets]  [ladder up]         |
 +--------------------------------------+
```

### Services aboard

| Station | Who | Service | Without them |
|---|---|---|---|
| **The bunk** | — | Rest to dawn, noon, dusk or night (forward only, never past midnight: SYSTEMS §10's xenia rule). Resting heals the party. | Always there |
| **The chart table** | Alethea | The Periplous: the sea map with Odysseus's notes and Alethea's corrections. The Odyssey page of the Scroll of Deeds. At night, she reads the stars (§4). | Required crew |
| **The steering oars** | Nausikles | Talk to him to hear the wind and the day's sea | Required crew |
| **The hearth** | Lampon | Once a day, Hestia's **Hearthfire** blessing (SYSTEMS §3: a stored full heal, usable anywhere outside battle) | No stored heal; the bunk still heals |
| **The Pithos** | Kydon | A working Pithos | No Pithos at sea |
| **The stall** | Kydon | Potions, balls, berries and offerings | No shop at sea |
| **Poseidon's altar** | — | Offerings at sea (SYSTEMS §3); the prayer to Krataiis before the Strait; lifting Poseidon's grudge | Always there |
| **The nets** | Diktys | Once a day, hauls something up: a Pearl, Big Pearl, Heart Scale, Shoal Salt, Shoal Shell, Star Piece or a water evolution stone | — |
| **The rail** | Lynkeus | Hidden items at sea glint; hidden islets show on the map; warns before Scylla strikes | — |
| **Phemios** | Phemios | Plays any song you've heard (a music player); the Sirens' third way (§6.6) | — |
| **Iaso** | Iaso | Cures status and revives fainted Pokémon, once per rest | — |
| **The run-through** | Christopher Nolan | The voyage so far, told backwards (§3) | — |
| **The trophy shelf** | — | One keepsake per island: a ram's fleece, a lotus, the bag's silver cord, a Siren's feather, Scylla's tooth, Circe's cup, a Phaeacian oar | — |

### Upgrades

| Upgrade | From | Effect |
|---|---|---|
| **The bronze ram** | Talos at Kaldera, for 3 Bronze Votives (before the voyage, optional) | Smash sea rocks and ice floes (sea obstacles); some hidden coves |
| **The new sail** | Aeolus, after Tornadus is back in the bag | Downwind speed up one more step |
| **The Phaeacian keel** | Scheria | The ship "knows the way": the Outer Sea's loop never catches you again (§4) |

### The ship as a place you return to

- **On land,** the ship waits at the island's landing. Walk onto the gangplank to board.
- **After the voyage,** Daedalus's Wings can land at the ship's anchorage, once Daedalus has seen Icarus's feather (UNDERWORLD §10, scene 7). Before that, she waits at Akti's quay.
- **The crew talk.** Every crew member has a new line after each island, and some have a line for each other. Kleon's oarsmen grumble in Lakonian (as in short sentences).

---

## 3. The crew

Recruit them before you round Maleia. Each is a short scene, two to ten minutes. None is required except the first three.

| Crew | Role | Recruited at | How | Matters at |
|---|---|---|---|---|
| **Nausikles** | Helmsman, first mate | Akti | He gives you the ship and comes along: "One more voyage. Then I'm done." | Required |
| **Alethea** | Navigator, chronicler | Akti | She's already aboard with a satchel of tracings. "Truthfully, you'd get lost." | Required; the Periplous; the stars |
| **The Lakonian oarsmen** (twelve) | Rowers | Lakonia, the battle school | Kleon lends them: "They row better than they fight. Don't tell them." | Required; Scylla; the Sirens |
| **Lampon** | Cook, keeper of the ship's hearth | Akti, the Temple of Hestia | Carry fire from Hestia's great hearth to the ship's hearth: a carried flame (SYSTEMS §2), 30 steps on Hero, through Akti's streets to the quay. Callback to the slice's Hearth Trial. | Hearthfire; the Lotus (he cooks something better than lotus); Thrinakia |
| **Diktys** | Carpenter, net-mender | Akti | Mend his boat with him: bring him a Big Root and a coil of rope from Emporion's Agora | Nets; repairs after Charybdis go faster |
| **Kydon** | Quartermaster | Emporion's Agora (LABYRINTH seed 3), or Amnisos | Buy one jar of Knossan honey. He decides he likes you. | Pithos and stall |
| **Phemios** | Bard | Thyrsa, the theater | Sit through his rehearsal and tell him the truth about it (three choices; honesty wins) | Music player; the Sirens' third way; the Lotus (his song wakes one crew member) |
| **Lynkeus** | Lookout | Astyra's harbor watchtower | Find three things in the harbor he can see and you can't: three hidden items he describes | Hidden islets; Scylla's warning; theoxenia E13's islet |
| **Iaso** | Healer | Astyra's Asclepeion | Phaedon recommends her if you've done the Katabasis; otherwise, help her with three patients | Status cures and revives aboard |
| **Glaukias** | Deckhand, Glaukos's grandson | Akti, the Fisher's house | He begs to come. Say yes. | **He opens the bag of winds** (§6.4). If he isn't aboard, an oarsman does. |
| **Christopher Nolan** | Dramatist (*didaskalos*), the man who wants it real | Lechaion, beside the Diolkos (Emporion's harbor) | Sail the *Euploia* into Lechaion and show him a real ship with a real crew (scene below) | The run-through; Scheria's song, backwards; the Strait |

**Christopher Nolan** (the user's request, 2026-11-14). A dramatist from the far north, staging the Odyssey and refusing to fake any of it. He is the voyage's other answer to the songs: Alethea corrects them with the truth, and he wants to *see* the truth, at full size, in order or not. The name box reads NOLAN (the full name is too wide for it); he says his full name when you meet.

[Lechaion, by the Diolkos. Haulers drag a ship across the Isthmus on its cradle. A man in a dark, neatly pinned cloak watches it without blinking.]
```text
NOLAN: Look at that. A real ship. Hauled over real land.

NOLAN: Anyone else would paint one. Painted ships look painted.

NOLAN: Christopher Nolan. I'm staging the Odyssey. All of it.

NOLAN: Not the songs. The songs are out of order, and half of them are fake.

NOLAN: I need a real ship. A real storm. A real whirlpool.
```
If the *Euploia* is moored in Lechaion:
```text
NOLAN: …That's your ship? With a crew? Going where he went?

NOLAN: Take me. I'll keep out of the way. Mostly.
```
?? YES/NO. YES: "NOLAN: Good. We start at the end and work back. Trust me." NO: "NOLAN: I'll wait. Waiting is most of the job." Ask again on the next visit.

- **The run-through** (his service aboard): talk to him for the voyage so far, told backwards, from the homecoming you haven't reached yet ("…and before that") back to Cape Maleia. It reads the same choice flags as Demodokos's song (§6.10), in reverse.
- **The crew talk.** With Phemios: "PHEMIOS: You can't have the Cyclops that small." / "NOLAN: He was that small. I measured." With Alethea, after the Cyclops: "ALETHEA: Truthfully, I like him."

**Glaukos himself** isn't crew. Poseidon's theoxenia line said "He fished too, before the sea kept him" (SYSTEMS §10). On the voyage, Glaukos turns up in the sea, changed, a sea-god now, half fish, delighted with himself (§6.5).

**The crew in the story.** Crew who are aboard take part in scenes: who gets turned into a pig, who's lost to the lotus, who the Sirens' song pulls at. The scripts pick from whoever is aboard, in a fixed priority order, so every combination plays.

---

## 4. Sailing

### The sea maps

The wine-dark sea is five large sea maps west of Aethos, plus the Outer Sea. Each is up to 80×80 (the engine's limit is `(w+15)×(h+14) ≤ 10240`, `MAX_MAP_DATA_SIZE` in `include/fieldmap.h`).

```text
  THE WINE-DARK SEA (schematic; west is left, Aethos is off the right edge)

            [AIOLIA] (floats: a new spot each day)
                 .                                   [CYCLOPS ISLE]
   ~~~ fog bank ~~~~~~~~~                                   .
   ~  [SIRENS' ROCKS]  ~       [AIAIA]                       .     [LOTUS ISLE]
   ~~~~~~~~~~~~~~~~~~~~~           .                          .         .
            |                       .                          .        .
   [THE STRAIT: Scylla | Charybdis]   . . . . . . . . . . . . . . . . . . [CAPE MALEIA] <== from Aethos
            |                                                        (the storm)
   [THRINAKIA] (optional)
            |
   ~~~~~~~ THE OUTER SEA (loops, unless you keep the Bear on your left) ~~~~~~~
            |
        [SCHERIA] ====== the Phaeacian ship, one night ======> [ELAIA's shore]
```

**The voyage's order** follows Homer's, roughly: the Lotus-Eaters, the Cyclops, Aiolia (where the bag is opened and the storm throws you west), Aiaia, the Sirens, the Strait, Thrinakia, the Outer Sea, Scheria, home. Fog banks keep the order: until you have Aeolus's Bag, the western half is closed.

### Wind

- **Each day has a wind:** a direction (8 points) and a strength (calm, fresh, strong). It is set at the daily reset from the daily seed (`DoDailyEvents`, `src/clock.c`), and by events: the bag, Poseidon's grudge, Thrinakia.
- **You can see it:** the ship sprite's sail fills toward the wind; the start-menu info panel shows "Wind: west, fresh"; Nausikles says it.

| Heading against the wind | Speed | Encounters |
|---|---|---|
| **Downwind** (the wind within 45° of behind you) | Fast: the running speed. With the new sail, faster. | Half rate |
| **Crosswind** | Normal | Normal |
| **Upwind** (the wind within 45° of ahead) | Normal: the oarsmen row | ×1.5 (rowing is loud) |
| **Calm** | Normal, rowing | Normal |
| **Strong wind** | As above, but a strong downwind pushes you one extra tile on the first step | — |

The difference between downwind and upwind is roughly half the voyage's sailing time. A player who waits a day for a better wind, or rests to night when the wind turns at the land breeze, is playing well.

**Engine.** The surf state chooses its step speed in `src/field_player_avatar.c`. Add a branch for sea maps: compare the facing to `IchorSave.epics.wind` and pick the fast or normal step. The encounter-rate change is a modifier beside the expansion's other rate modifiers in `src/wild_encounter.c`. **Low–Medium.**

### Currents

Strong sea lanes use Emerald's current tiles (`MB_EASTWARD_CURRENT` and its three siblings, `include/constants/metatile_behaviors.h` lines 85–88), as Routes 131–134 do. They are fast lanes if you go with them and walls if you don't. Charybdis's pull is a ring of currents (§6.7).

### Stars

- **At night on a sea map,** if Ursa Major is placed (SYSTEMS §8; it's placed at Laurel 5, so always by now), a small star sprite of the Great Bear hangs in the top of the screen, fixed to north.
- **"Keep the Bear on your left,"** which is what Calypso told Odysseus (*Odyssey* 5.276). Sailing with the Bear on your left takes you east.
- **The Outer Sea loops.** Its edges connect back to itself unless you sail out of its east edge **at night**, with the Bear on your left. By day there are no stars, and the sea goes round and round. Alethea says so the first time: "No stars, no east. Truthfully, I'd wait."
- **Engine:** the Outer Sea's map connections point to itself. A coord check on the east edge swaps in the real connection when it's night (`gettimeofday`) and the player is facing east. **Low.**

### Fog banks

Impassable fog walls close off the western sea. Fog weather (`WEATHER_FOG_HORIZONTAL`) plus invisible collision objects with a hide flag. **Aeolus's Bag** blows a bank away: use it from the Relic Ring facing the fog. It is Defog's field effect re-pointed to the relic (`OW_DEFOG_FIELD_MOVE` exists in `include/config/overworld.h`; SYSTEMS §1 already names it).

### Wings at sea

Daedalus's Wings don't work once you've rounded Maleia: "No herm out here. The sea has no roads." They return when you're home. This is the one place in the post-game that locks fast travel. It's announced before you go (scene 3), and the ship has everything you need. It's what makes the homecoming land.

### Poseidon's grudge

If you boast your name at the Cyclops's island (§6.3), Poseidon holds a grudge.
- **The wind** is always against your heading for one day, then strong and random.
- **It lifts** when you make a loved offering (a sea gift: Pearl, Big Pearl, Shoal Salt, Shoal Shell, Heart Scale) at the ship's altar of Poseidon, or at the next island's shrine.
- It's a nuisance, not a lock, and the game never explains it beyond Nausikles: "That's not weather. That's somebody."

### Wild Pokémon at sea

| Sea map | Levels | Surfing | Fishing |
|---|---|---|---|
| Maleia's waters | 70–73 | Galenyon 25%, Halcyling 15%, Wingull and Pelipper 25%, Mantine 15%, Tentacruel 20% | Ketofry, Kynoketos (rare), Narkeray, Remoraid and Octillery |
| The eastern wine-dark sea | 71–74 | Finizen 20%, Lapras 10%, Galenyon 20%, Cramorant 15%, Sharpedo 15%, Wailmer 20% | Kynoketos, Hisuian Qwilfish, Bruxish, Alomomola |
| The western wine-dark sea | 72–75 | Lapras 15%, Wailord 10%, Dhelmise 10%, Galenyon 20%, Seirenade 5% (near the rocks), Kingdra 10%, Mantine 15%, Palafin 15% | Relicanth, Lanturn, Milotic, Kynoketos |
| The Outer Sea | 74–76 | Wailord 20%, Lapras 15%, Dhelmise 15%, Haligeron 5%, Dragalge 15%, Jellicent 15%, Kingdra 15% | Relicanth, Gyarados, Milotic, Kynoketos |

At night, each table adds Lanturn and Chinchou, and Jellicent becomes common.

---

## 5. The voyage in one table

| # | Island | The test | The mechanic | Boss | Prize |
|---|---|---|---|---|---|
| 1 | Cape Maleia | — | The storm: a scripted passage | — | — |
| 2 | **The Lotus-Eaters** | Temptation to stay | Lead lotus-dazed crew back at a distance; refuse the lotus, or don't, and get a fake ending | — | The Lotus Fruit |
| 3 | **The Cyclops's island** | Stealth | Move only while the great eye is shut; leave clinging under a ram | The great Polyphant, only if spotted | The Ram's fleece |
| 4 | **Aiolia** | Trust | The bag of winds; the sight of home; the crew opens it | Aeolus (optional), then **Tornadus** at sea | **Aeolus's Bag** |
| 5 | **Aiaia** | Transformation | Become a pig, a wolf or a lion to find your crew among Circe's animals | **Circe** | Mints; Circe's cup |
| 6 | **The Sirens' rocks** | Desire | Iapetos writes their songs. Three ways: his wax and silence, the mast and the song, or the bard | Iapetos; the Sirens, by one way | A Siren's feather |
| 7 | **The Strait** | Loss | Choose Scylla or Charybdis | Hexylla or Trybdis | Scylla's tooth or a fig branch |
| 8 | Thrinakia (optional) | Hunger | Feed the crew without touching the Sun's cattle | — | A Sun Stone; Helios's favor (Labor 10) |
| 9 | The Outer Sea | Navigation | Keep the Bear on your left | — | — |
| 10 | **Scheria** | Rest | The kindest hosts; the bard sings your voyage | The Phaeacian games (optional) | The Phaeacian keel |
| 11 | **Elaia** | Home | The beggar's disguise; the twelve suitors; your mother's question | Twelve suitors | Melitta's Cloak, lined; Argos |

---

## 6. The voyage, step by step

### 6.1 Cape Maleia: off the edge of the map

**Before.** At Akti's quay, Nausikles asks if you're ready, and warns you about the Wings (scene 3). Saying yes starts the voyage.

**The storm.** Rounding Maleia, the sky goes dark in seconds. A scripted passage on the Maleia sea map: the screen shakes, rain (`WEATHER_DOWNPOUR`), currents throw the ship west whatever you press, and the crew shout. You wake in calm water with no land you know. The Periplous shows the first island: the Lotus-Eaters.

### 6.2 The Lotus-Eaters: the temptation to stay

> *Whoever ate the honey-sweet lotus wanted never to go home, only to stay among the Lotus-Eaters, eating lotus, forgetting the way back* (*Odyssey* 9.94–97).

**Play.** A gentle island of golden light where nothing happens. The Lotus-Eaters are kind, smiling people with Lotad and Ludicolo, who offer everyone fruit. Three of your crew eat it and lie down under the lotus trees, perfectly happy, and won't come back to the ship. You have to lead them, one at a time, while the islanders keep offering you a lotus too.

**The island stopped its clock.** On this map the time of day doesn't change and the day/night tint is fixed at a golden afternoon. Alethea notices (scene 4): "This is what Kronos wanted. Everyone happy. Nobody going anywhere." The Lotus isle is the villain's dream, small and sweet and harmless, and it is the most dangerous place on the voyage.

**Maps:** the Lotus Isle (40×40), a beach, a meadow of lotus trees and a village of hammocks.

**Rules.**
- **The dazed crew** are the first three aboard in this priority: Phemios, Kydon, Glaukias, Lynkeus, then oarsmen.
- **Leading.** A dazed crew member follows you while you're within 3 tiles. Get farther, and they drift back to their tree. Walk them back to the gangplank one at a time.
- **Lotus-Eaters** stand along the paths. Pass within 2 tiles and they offer a lotus: "Have one. You look tired."
  - **NO, THANK YOU:** they smile and let you by.
  - **YES:** you eat. Your speed drops to a stroll, and your dazed crew member, seeing you eat, sits down where they are. Five steps later it wears off.
- **The way round:** paths that keep 3 tiles from the offerers are longer. Lampon, if aboard, can be sent ashore with "something better than lotus": a stew that pulls one dazed crew member back on its own.
- **Phemios,** if aboard and not dazed, plays a sea song at the gangplank, and the first dazed crew member walks back to it unaided.

**The fake ending.** Accept a lotus three times in one visit, and the screen fades to gold.
```text
And {PLAYER} stayed on the island of the lotus, and was happy,

and nothing ever happened again.

THE END
```
A short credits roll follows: the crew's names, the island's name, nothing else. Then, faintly: "Somewhere very far away, a dog barked." You wake on the beach with Alethea shaking you (scene 4). No penalty. It's the game's only joke ending, and it's on the theme.

**Prize.**
- **The Lotus Fruit,** a consumable, given by a Lotus-Eater who's sorry to see you go. A Pokémon that eats it forgets all its training: its EVs reset to 0. Five more in the island's Agora-hut (500 money each, after the voyage).
- Lotus Isle items: a Leaf Stone, a Big Pearl, and a hidden Max Revive under a hammock.

**Engine.**
- The frozen clock is a map flag that the day/night tint and `gettimeofday` read (`OW_ENABLE_DNS`, `src/overworld.c`). Low.
- Leading at a distance is a scripted escort (SYSTEMS §10's escorts) with a distance check per step. Low.
- The fake ending is a script: a fade, scrolling text and a warp. Low.
- The Lotus Fruit is a new item whose effect clears EVs (`SetMonData` on the six EV fields). Low.

**Wild Pokémon** (the Lotus Isle, Lv 70–73): Lotad 20%, Lombre 15%, Ludicolo 10%, Psychora 15%, Comfey 10%, Amnoze 15%, Slakoth and Slaking 15%. Fishing: Lotad, Lombre, Basculin, Narcibulb.

### 6.3 The Cyclops's island: hide among the flock

> *Polyphemus shut them in his cave with a stone no wagon could shift. They blinded him, and in the morning they left clinging beneath his rams, while he felt each one's back at the door. Odysseus, safe on his ship, shouted his real name* (*Odyssey* 9).

**Play.** A cave full of cheese and milk, and your crew can't resist. Then the cave's owner comes home: not a one-eyed giant, but a **colossal, ancient Polyphant**, a shepherd-beast whose one great central socket looks just like an eye. It herds its flock of Amnoze and a huge old Dubwool ram inside, and rolls a boulder across the door, and you are now part of its flock. It isn't cruel. It collects strays. And it doesn't let them go.

**Truth and the story.** Odysseus's chart says "Cyclops. One-eyed giant. Asks your name. Say NOBODY." The dex's thesis is that the Cyclopes were dwarf-elephant skulls misread as giants (dex #105–106). Here the misreading is in front of you. Alethea, delighted: "Truthfully, I think he just didn't want to say he was out-herded by an elephant."

**Maps:** Cyclops Isle (40×40, a pasture and goat-cliffs) and the Cave (30×24).

```text
  THE CYCLOPS'S CAVE (30x24), at night
     P = the Polyphant (sleeping by the door)   O = the boulder
     s = Amnoze (sleeping sheep)   R = the great ram (Dubwool)
     c = your trapped crew (asleep in corners)   [] = cheese racks (cover)
 +-----------------------------------------------------+
 |  c   []  []        s   s     s        []  []    c    |
 |      s       s  s      R       s   s       s        |
 |  []      s          s      s         s       []     |
 |      s   []   s        s       s   []    s          |
 |  c         s      s        s       s          c     |
 |  []  []        s      s       s        []  []       |
 |                   P                                 |
 |                  [O] the door                        |
 +-----------------------------------------------------+
```

**Steps.**
1. **The cave.** Explore it with three crew members. The Polyphant returns; the boulder rolls shut. The Girdle can't move it: "Twenty wagons couldn't shift it." (Homer said twenty-two.)
2. **The wine.** Your crew brought a skin of strong Maronean wine (a Wine offering item, SYSTEMS §3; if you have none, the crew has one). Offer it to the Polyphant. It drinks, and lies down by the door.
3. **Night: the eye.** The Polyphant dozes, but its great socket glows when it stirs.
   - **The eye glows** every 8–12 seconds, for 3 seconds, with a rumble first. While it glows, anything moving in its line of sight is "a stray" and it gets up and herds you back to the middle of the cave, and the night restarts. (No battle; just the walk back.)
   - **Sheep are cover.** Standing next to a sleeping sheep, you're part of the flock and invisible to it.
   - **Wake your three crew** in the corners and tell each one which sheep to hide under at dawn.
4. **Dawn: the door.** The Polyphant rolls the boulder aside and sits in the doorway, letting its flock out one by one, nosing each one's back.
   - **Cling under a sheep:** walk into a sheep's side and choose HOLD ON. You disappear under it and move with it.
   - **The small sheep** (Amnoze) are too thin. It feels you, and puts you back inside.
   - **The great ram** (Dubwool) is the one it nuzzles last and longest, every time. You can watch it do this on the first dawn. Only the ram, and two big ewes, are big enough.
   - **Your crew** must each be under a big sheep too, or they're held back for the next dawn. (Rest in the cave to reach the next dawn.)
5. **The boast.** At the ship, as the oarsmen pull away, the crew urge you to shout your name to the island, "the way Odysseus did."
   - **{PLAYER}:** Poseidon's grudge (§4). The Polyphant, hearing, hurls a boulder into the sea beside the ship, and you take a wild battle with it on the beach-edge (the boss below).
   - **NOBODY:** the crew roars with laughter. Alethea: "Accurate." For the Unwoven, it's literally true.
   - **Say nothing:** Nausikles nods. "Wise."

**Mechanic: hide among the flock.**
- **The eye** is a non-battle sight object with an on/off cycle (SYSTEMS §12's non-battle sight, `src/trainer_see.c`), whose sight ignores the player when the player is adjacent to a sheep object.
- **Clinging** hides the player object and attaches it to the sheep's movement script.
- **The dawn exit** is a scripted procession.
- **Low–Medium.**

**Boss** (only if you boast, or are spotted three nights running and choose to fight): **the great Polyphant.**

| Species | Lv | Ability | Item | Moves | Notes |
|---|---|---|---|---|---|
| Polyphant | 74 | Rock Head | — | Rock Wrecker, Body Slam, Milk Drink, Block | Totem boost +1 Defense, +1 Attack. **Not catchable:** it's the island's shepherd (decision O2). |

**Prize.**
- **The Ram's fleece** (trophy).
- **The great ram** follows you to the ship and won't go back. He's a Dubwool, Lv 72, Bulletproof, with Cotton Guard. The crew name him (a multichoice: NOBODY, WOOLLY, or the player's choice).
- Cave items: Moomoo Milk ×6 ("the Cyclops's cheese, which is excellent"), a Rare Bone, a hidden Ichor Stone behind the cheese racks.

**Wild Pokémon** (Cyclops Isle, Lv 71–74): Amnoze 20%, Wooloo 15%, Dubwool 10%, Monophant 5%, Gogoat 15%, Galekit 15%, Cairnolith 10%, Mudsdale 10%.

### 6.4 Aiolia: the bag of winds

> *Aeolus, keeper of the winds, lived on a floating island walled in bronze. He gave Odysseus every wind tied in an ox-hide bag, all but the West Wind, which blew them home. In sight of Ithaca, while Odysseus slept, the crew opened the bag, thinking it held gold. The winds blew them all the way back. Aeolus sent them away: "The gods must hate you"* (*Odyssey* 10.1–75).

**Play.** A floating island ringed by a wall of bronze, which drifts to a new place on the sea each day. Aeolus, a booming, generous host, feasts you for a "month" (one scene) and gives you every wind in a silver-tied bag. The West Wind alone stays free, and it carries you east, fast. Within hours you see home: Elaia's coast, the old olive on the hill. Then a deckhand opens the bag.

**Maps:** Aiolia (36×30, the bronze-walled island with Aeolus's hall) and its hall (24×16).

**Steps.**
1. **Find Aiolia.** It floats. Each day it's in one of four places on the eastern wine-dark sea, and Lynkeus (if aboard) or the day's wind tells you where: "It's always upwind."
2. **The feast.** Aeolus's xenia (SYSTEMS §10): a heal, a bed and a feast scene. Optional: his friendly match (the boss below).
3. **The bag** (scene 5).
4. **The West Wind.** The wind is set to "west, strong" and the sea maps' fog lifts eastward. You sail east at full downwind speed.
5. **The sight of home.** On the eastern sea, a full-screen picture: Elaia's coast in the distance, small and bright (240×160). The crew go quiet. Alethea: "Truthfully, I didn't think we'd see it again."
6. **The bag is opened.** You're "asleep" at the chart table. Glaukias (or an oarsman) unties the silver cord because "nobody gets a bag like that for nothing" (scene 5).
7. **The storm.** Every wind at once. A scripted storm: currents throw you west across all four sea maps, back past Aiolia, into the fog. A white shape circles the mast in the storm, and the ship doesn't break. (A cameo for Atlantis's Lugia: Leukothea, the white sea-goddess who saved Odysseus's life with her veil in *Odyssey* 5. Alethea: "That was no bird.")
8. **Aiolia again.** You drift back to the floating island. Aeolus is cold: "The gods hate you. Go away."
9. **The escaped wind.** One wind didn't go back: the storm wind, **Tornadus**, now loose on the sea. Aeolus, grudging: "Bring him back and we'll talk."
10. **Chasing the storm** (below).
11. **Forgiveness.** With Tornadus caught (or beaten), Aeolus re-ties the bag with every wind but one inside, the new sail as a gift, and gives it to you to keep: **Aeolus's Bag**, the relic. "Don't let anyone touch the cord."

**Mechanic: chase the storm.**
- **Tornadus** is a storm cloud object on the sea maps (32×32, animated), which moves **with the day's wind**, two tiles for each step you take.
- **To catch it,** you need to get ahead of it and let it come to you: sail downwind of it while it's coming your way. Chasing it from behind, with the wind, you're the same speed and never close. Approaching it head-on into the wind, you're too slow.
- **It crosses maps.** When it leaves a sea map, it enters the next one in the wind's direction. Nausikles: "It goes where the wind goes. Get where the wind's going."
- **Touch the cloud** to start the battle. Tornadus doesn't flee (this is a sailing chase, not Labor 3's trap-the-runner).
- **If you beat it instead of catching it,** it reforms the next day.
- **Engine:** an object with a scripted movement each player step, along the wind vector, and a map-transfer when it leaves the map (as a roamer moves, `src/roamer.c`, but visible). Its position is 2 bytes in `IchorSave.epics`. **Medium–Low.**

**Bosses.**

| Who | Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|---|
| Aeolus (optional) | Galenyon (his daughter Alcyone's kingfisher) | 77 | Cloud Nine | — | Hurricane, Liquidation, Roost, Calm Mind |
| | Borapteryx | 76 | Wind Rider | Never-Melt Ice | Blizzard, Hurricane, Freeze-Dry, Tailwind |
| | Kerastorm | 76 | Static | — | Thunderbolt, Moonblast, Nasty Plot, Thunder Wave |
| | Pelipper | 76 | Drizzle | Damp Rock | Hurricane, Surf, Roost, Tailwind |
| | Whimsicott | 76 | Prankster | Light Clay | Tailwind, Moonblast, Encore, Leech Seed |
| | Cramorant | 77 | Gulp Missile | — | Surf, Brave Bird, Ice Beam, Hurricane |
| **Tornadus** | Tornadus (Incarnate) | 75 | Prankster | — | Hurricane, Heat Wave, Tailwind, Taunt |

- **The halcyon link.** In Ovid, Alcyone was Aeolus's daughter, and the halcyon days are her father calming the winds while she nests. The slice ends in halcyon days at Akti (SCRIPT, one paragraph). Aeolus, at the feast: "My girl's bird. She makes me calm the sea every winter. Seven days. You were stuck in it once, I hear. Sorry."

**Prize.**
- **Aeolus's Bag** (relic 13): sail the fog banks.
- **The new sail.**
- **Tornadus,** if caught. Alethea later makes the **Reveal Glass**, which she calls the Mirror of Truth, from Aiolia's bronze: it shows Tornadus's true shape (its Therian Forme). TERMS should decide the item's name.
- The bag's silver cord (trophy).

**Wild Pokémon** (Aiolia, Lv 72–75): Kryopuff 15%, Borapteryx 5%, Galenyon 15%, Whimsicott 15%, Swablu and Altaria 15%, Hisuian Braviary 10%, Drifblim 15%, Castform 10%.

### 6.5 Aiaia: Circe and the shapes

> *Circe turned Odysseus's men into swine. Hermes gave him the herb moly, so her cup couldn't change him. Wolves and mountain lions, men she had enchanted, prowled her house* (*Odyssey* 10.133–574).

**Play.** On a wooded island, smoke rises from a stone hall in a clearing, where wolves and lions lie about like dogs. Your crew go ahead to the hall, and only one comes running back: the rest are pigs. A young man with a golden wand and no shadow gives you a black-rooted, white-flowered herb on the path. Circe's cup can't change you now. She's impressed, after a fight, and offers a bargain: bring your crew to her and she'll turn them back, but they're mixed in among her other animals, and pigs only follow pigs. So she lets you drink from her three fountains.

**Maps:** Aiaia (44×40: woods, the clearing, the sty, the wolf run, the lion court and Circe's garden) and Circe's hall (24×18).

```text
  AIAIA (44x40), Circe's grounds
     F = a form fountain (pig / wolf / lion)   S = the restoring spring (by Circe's door)
     w = wolf pack (blocks unless you're a wolf)   l = lions (block unless you're a lion)
 +--------------------------------------------------+
 |  [CIRCE'S HALL]  S                     [lion court] |
 |      .  .  .  .  .  .  .  .  .  .  l  l  .  l      |
 |   [garden: mints]   F(lion)   .  .  .  .  .  .     |
 |   .  .  .  w  w  .  .  .  .  .  .  .  .  .  .     |
 |   .  [wolf run]  w  .  F(wolf)  .  .  .  .  .     |
 |   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .     |
 |   [THE STY: twelve pigs]   F(pig)   .  .  .  .    |
 |   .  .  .  .  .  .  .  .  .  .  .  [woods path] -->  the landing
 +--------------------------------------------------+
```

**Steps.**
1. **The warning.** One oarsman runs back to the ship: "Pigs! They're all pigs!" (scene 6).
2. **Hermes** (in disguise, no shadow) gives you **moly** on the woods path. If you did theoxenia E1, he says "Feet," and winks.
3. **Circe's hall.** She offers her cup. Moly: nothing happens. She draws her wand. Battle.
4. **The bargain.** Beaten, Circe offers to restore anyone you bring to her spring, and gives you her fountains.
5. **The forms.**

| Fountain | You become | You can | Animals react |
|---|---|---|---|
| Pig | A Kaplet | Squeeze through the sty's gaps; sniff out buried items (dig spots show) | Pigs follow you. Wolves and lions chase you off. |
| Wolf | A Lykopup | Howl: the wolf pack moves aside for 20 steps | Wolves let you through. Pigs scatter from you. |
| Lion | A Nemecub | Roar: the lions lie down for 20 steps | Lions let you through. Pigs scatter. |

   Drinking again at your own fountain turns you back. You can't battle or use the Bag in a form; wild encounters are off.
6. **Find your crew.** The sty holds twelve pigs. As a pig, talk to them. Your crew members still have their habits:
   - "This pig keeps sniffing toward the kitchen." (Lampon)
   - "This pig is humming. Badly." (Phemios)
   - "This pig is staring at the horizon." (Lynkeus)
   - "This pig is mending a net that isn't there." (Diktys)
   - "This pig is counting the other pigs." (Kydon)
   - "This pig is very sorry about something." (Glaukias)
   - Oarsmen: "This pig is doing push-ups."
   - Circe's other pigs just eat.
7. **Lead them out.** Pigs follow a pig, but the path to the spring runs past the wolf run and the lion court. So: lead the pigs as a pig to the edge, go back to a fountain, become a wolf, howl the pack aside, go back, become a pig again, and lead them through in the 20 steps you've got. The lion court is the same, with a roar.
8. **The spring.** Each crew member steps in a pig and steps out themselves, embarrassed.
9. **Circe's other animals.** If you bring her wolves and lions to the spring too (as a wolf or a lion, leading them), they're old sailors from other voyages. Each gives you one line and a small gift.

**Glaukos.** On the beach as you leave, a sea-god with a fish's tail and a green beard surfaces in the shallows. Glaukos, the old fisher of Akti, is a god now: he ate a strange seaweed again (SCRIPT: "I ate a strange seaweed once… felt immortal for a week"). "Didn't wear off this time!" He used to tell sailors their futures. "Now I just tell them the weather." He tells you the Sirens are next and how to pass them (scene 7).

**Mechanic: the forms.**
- The player's graphics switch to a species follower sprite (Kaplet, Lykopup, Nemecub; `OW_POKEMON_OBJECT_EVENTS` is TRUE). This generalizes LABYRINTH's disguise ("a new avatar graphics state behind a flag", §12 there). **Medium.**
- Pigs following: the follow movement on object events while the player is a pig. Wolves and lions: scripted blockers with timed hide flags. **Low–Medium.**
- **Fallback:** keep the mechanic and use the player's normal sprite with a small animal icon over their head.

**Boss: Circe,** daughter of Helios.

| Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|
| Kaprodon | 76 | Thick Fat | — | Head Smash, Earthquake, Night Slash, Thrash |
| Lykanax | 76 | Intimidate | — | Jaw Lock, Close Combat, Sucker Punch, Bulk Up |
| Nemeleon | 76 | Fur Coat | — | Crush Claw, Bulk Up, Double-Edge, Crunch |
| Oinopard | 76 | Poison Touch | — | Gunk Shot, Throat Chop, Sucker Punch, Hone Claws |
| Prosomime | 77 | Illusion | Focus Sash | Nasty Plot, Sludge Bomb, Psyshock, Trick Room |
| Galarian Slowking | 78 | Curious Medicine | Black Sludge | Eerie Spell, Sludge Bomb, Trick Room, Flamethrower |

Her swine, her wolf, her lion, Dionysus's panther, a mask, and a brewing king. Galarian Slowking is a vanilla pick: a witch's brew, and the post-game allows it.

**Prize.**
- **Mints.** Circe's garden sells every Mint after the voyage (PITCH §5 lists Mints): she's the herb-witch.
- **Circe's cup** (trophy).
- Moly (a key item; it only has a dex-entry joke: "Hermes says it's good in salads.").
- Aiaia items: a Big Root, a Mystic Water, a hidden Ichor Stone under the lion court's fountain.

**Wild Pokémon** (Aiaia, Lv 72–75): Kaplet 20%, Lykopup 15%, Nemecub 5%, Botrykit 15%, Prosomime 5%, Hisuian Zorua 10%, Galarian Slowpoke 10%, Morelull and Shiinotic 20%.

### 6.6 The Sirens' rocks: three ways past

> *Circe told Odysseus to stop his crew's ears with beeswax, and to have himself bound to the mast if he wanted to hear the Sirens. He heard them, begged to be untied, and the crew bound him tighter. The Argonauts passed them another way: Orpheus played louder* (*Odyssey* 12; Apollonius 4.891–919).

**Play.** A strait of white rocks in the western sea, littered with old timbers. Seirenade perch on the rocks with lyre-tails and women's voices. Their song pulls any ship that hears it onto the rocks.

On a skerry at the strait's mouth, someone has set up a writing desk under an awning. A neat, thin man with an ink-dark right hand sits at it, scratching at wax tablets, and the Sirens are singing what he writes. **Iapetos,** the forger, exiled for ten years to a place nobody knows (STORY §2 and §3), has found an audience that will sing anything he gives it.

**The skerry.** Land there first.
- Iapetos greets you as if he expected you: "May I tell you something true?" He's writing the Sirens better songs.
- Alethea, who was exiled on his forgery and then tried him and won, does the talking (scene 7a).
- He battles you, because a writer defends his drafts (the boss below).
- Beaten, he shrugs and goes back to writing. His stacks of wax tablets are left on the rocks. **Lampon melts them at the ship's hearth into earplugs** (STORY §3: "You plug your ears with wax melted from his own tablets"). Without Lampon aboard, Alethea melts them over the lamp.

**What the Sirens sing.** In Homer they promise knowledge: everything that happened at Troy. Iapetos's lyrics promise what he always sold: a better story. To the Unwoven they promise two things you've never had. A thread: "We know everyone's thread. We'll write you yours. A beautiful one." And glory: "Stay, and we'll sing you forever. Your friend chose glory. Choose it too." The temptation is to be given a fate, and a famous one. Achilles's choice, sung (§1).

**Maps:** the Sirens' Strait (40×50): a maze of rocks with Seirenade on them, a current that runs north through the middle, slack water at the sides, and Iapetos's skerry at the mouth.

There are three ways past, and you choose one when you approach.

**Way 1: wax and silence** (needs Iapetos's tablets, melted).
- Everyone, you included, stops their ears. Nobody can hear the song, and nobody can hear your orders either.
- **The oarsmen stop rowing.** The ship moves only with the wind and the current, so you can only steer. A sound-and-stealth passage through the maze with the sail alone.
- **The Sirens can't pull you,** but the rocks can still stop you. Read the current, wait for the wind, tack.
- **Prize:** the drift lanes hold floating items you can only reach without rowing (a Shell Bell, a Pearl String, a Big Nugget).

**Way 2: the mast** (always available).
- Your crew stop their ears with Iapetos's wax (or with cloth, if you haven't been to the skerry), and bind you to the mast. The ship rows itself through on a fixed course.
- **You hear the song.** A sequence of text boxes: the Sirens' verses, and after each, a choice: **UNTIE ME!** or **KEEP ROWING**. The cursor starts on UNTIE ME (`multichoicedefault`, `asm/macros/event.inc` line 954).
- **Choose UNTIE ME** and the crew, who can't hear you, see you struggle and bind you tighter (as in Homer). After three UNTIE MEs, two oarsmen sit on you. The ship goes through either way. It's a test of nothing except the player, and that's the point.
- **Prize:** you heard the song. The Siren's verses are recorded in the Periplous, and Alethea writes "TRUTH: they don't know anything. He writes it; they sing it beautifully." Plus a Siren's feather (trophy).

**Way 3: the bard** (needs Phemios).
- Phemios plays louder than the Sirens, as Orpheus did for the Argonauts. The crew row; the song can't reach them over his.
- **The Sirens come for him instead.** A wild double battle against two Seirenade (Lv 76). Win, and they fall silent.
- **Prize:** the Seirenade are catchable here (only by this way during the voyage; after it, they're on the rocks for anyone), and Phemios learns their tune for the music player.

**Engine.**
- Way 1: rowing off means only wind and current move the ship. On this map the surf step is refused unless the facing is downwind or the tile is a current (the same speed branch as §4). Sirens' rocks are collision. **Low–Medium.**
- Way 2: a scripted sequence of multichoices. **Low.**
- Way 3: `setwildbattle` with two species. **Low.**

**Boss: Iapetos, the Voice,** on his skerry. His team is STORY §2's, with the post-game's levels: a liar's story in every slot.

| Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|
| Prosomime | 76 | Illusion | Focus Sash | Nasty Plot, Sludge Bomb, Psyshock, Trick Room |
| Hyphantis | 76 | Frisk | — | First Impression, Sticky Web, Knock Off, Sucker Punch |
| Pithound | 76 | Unaware | Leftovers | Foul Play, Psyshock, Slack Off, Trick Room |
| Enigmaw | 77 | Analytic | Life Orb | Psychic, Close Combat, Air Slash, Calm Mind |
| Kerdovix (ace) | 78 | Prankster | — | Foul Play, Moonblast, Parting Shot, Fake Tears |

Iapetos isn't caught or punished again here: he's already exiled, and "Every draft has a next draft."

**Wild Pokémon** (the Sirens' Strait, fishing only, Lv 74–76): Elegull 30%, Seirenade 5% (after the voyage), Dhelmise 20%, Corsola (Galarian) 20%, Relicanth 15%, Mantine 10%.

### 6.7 The Strait: choose your loss

> *On one side, Scylla with six heads, who snatches six men from every ship. On the other, Charybdis, who swallows the sea three times a day. Circe told Odysseus to hug Scylla's side: better to lose six than all* (*Odyssey* 12.73–259).

**Play.** A narrow strait between a cliff and a whirlpool. On the left, a cave high in the cliff, where six long necks wait. On the right, the sea turns round and down. You have to steer one way or the other, and each takes something. If Christopher Nolan is aboard, he stands at the rail the whole way through: "NOLAN: Nobody paints this. Ever."

**Maps:** the Strait (30×60): Scylla's cliff on the west side, Charybdis's whirlpool (a ring of currents around a center) on the east side, and between them nothing safe.

**The choice.**

| Way | What you lose | For how long | How you get it back |
|---|---|---|---|
| **Scylla's side** | **Six oarsmen.** Each of her six heads takes one from the benches. Rowing upwind is no longer normal speed: it's slower (one step in two is refused). | Until you rescue them | **Scylla's cave** (below), any time, during or after the voyage |
| **Scylla's side, prepared** | Fewer. Circe's advice: pray to **Krataiis**, Scylla's mother, at the ship's altar before you go, and she'll strike only once (−3). **Lynkeus** sees the heads coming (−1). **Rowing hard** with the wind behind you (−1). The minimum is one. | As above | As above |
| **Charybdis's side** | **The ship and its hold.** Charybdis swallows the *Euploia*. The crew all swim clear; you cling to a fig tree above the whirlpool. The hold is gone: Kydon's stock, the ship's upgrades, the trophy shelf. | The ship: until Scheria rebuilds her. The hold: until you dive for it. | **Charybdis's Hoard** (below), a dive after the voyage, with the Nereid Pearl (POSTGAME §3) |

Neither is a mistake. Scylla is the cheaper loss if you're prepared, and Charybdis gives you more back in the end, much later. Circe tells you this in one line if you ask her (scene 6): "Six is better than all. Unless all is coming back."

**Scylla's side.**
- **The strike** is a scripted moment: six heads, one after another, each snatching one oarsman and one line of dialogue ("Agis!" "Doros!"). The names come from the oarsmen's roster (§3). Prepared strikes take fewer.
- **Scylla's cave** is a short climb up the cliff (a 20×30 dungeon) reachable from a ledge on the strait after you're through. Each rescued oarsman is in a niche. At the top: Hexylla, the six-headed snatcher, in a battle (boss below). The rescue can wait until after the voyage; the Strait is revisitable.

**Charybdis's side.**
- **The pull:** a ring of current tiles draws the ship to the center.
- **The fig tree:** as the ship spins past the rock, a prompt: "A fig tree hangs over the whirlpool!" Press A in the window (LABYRINTH's bull-leap timing task, `src/ichor_bull_leap.c`, reused with a wide window). You cling.
- **Miss it,** and you go down into the maw: a battle with Trybdis, the whirlpool maw (boss below). Then she spits you up anyway, as she spat up the keel.
- **Either way,** you ride the ship's keel when she spits it out, and drift. The current takes you (and the crew, swimming) to Scheria (§6.10). Thrinakia and the Outer Sea are skipped. (Thrinakia stays open after the voyage.)
- **Charybdis's Hoard** (after Atlantis gives you the Nereid Pearl): dive into the whirlpool's calm center at "slack water" (Charybdis swallows three times a day; between, she's still). Below is a cave of everything she's ever swallowed: your hold back, plus wrecks and treasure (a Big Nugget, two Comet Shards, a Kings Rock, an Ichor Stone and a Relicanth).

**Bosses.**

| Who | Species | Lv | Ability | Item | Moves | Notes |
|---|---|---|---|---|---|---|
| Scylla (her cave) | Hexylla | 77 | Strong Jaw | — | Psychic Fangs, Jaw Lock, Liquidation, Sucker Punch | Totem boost +1 Attack, +1 Speed. Catchable after. |
| Charybdis (the maw) | Trybdis | 77 | Arena Trap | — | Water Spout, Earth Power, Stockpile, Swallow | Totem boost +1 Defense, +1 Sp. Def. Catchable at the Hoard, after the voyage. |

**Prize.**
- Scylla's tooth (trophy), or a fig branch (trophy).
- The rescued oarsmen, each with a line, and one gives you a Razor Fang he pulled out of the cave wall.

**Wild Pokémon** (the Strait, fishing only, Lv 74–77): Hexylla 2% (only after her cave), Trybdis 2% (only after the Hoard), Dhelmise 20%, Bruxish 20%, Sharpedo 20%, Octillery 20%, Kingdra 16%.

### 6.8 Thrinakia: the Sun's cattle (optional)

> *On the island of the Sun, Odysseus's crew, starving and becalmed, killed Helios's cattle while he slept. Zeus wrecked the ship for it* (*Odyssey* 12.260–419).

**Play.** Only on Scylla's way (Charybdis's way skips past it). A golden meadow island where the Sun's cattle graze, a golden herd of Kaminoo and Taurivet. The wind dies. The crew are hungry, and the stores, short after Scylla, run out. The test is simple: feed your crew without touching the Sun's cattle, before one of them gives in.

**Rules.**
- **Hunger.** Each oarsman aboard needs one food. A hunger counter starts at 30 steps per food still needed (so 6 oarsmen give you about 180 steps).
- **Food:** any berry, a fish (each catch with a rod counts), Barley Cake, Moomoo Milk, honey, or Lampon's stew (one pot feeds four, if Lampon's aboard).
- **If the counter runs out,** one oarsman slips off and kills a calf. Helios is angry (scene 8): a bolt strikes the ship (no one's hurt), the hold is lost as at Charybdis, and the next Labor 10 meeting with Helios is cold.
- **If you feed them,** the wind comes back, and Helios, who was watching, leaves a Sun Stone on the ship's altar, and remembers (LABORS §3, Labor 10).

**Engine:** a step counter in `VAR_TEMP`, food counted from the Bag's items as you hand them over. **Low.**

**Wild Pokémon** (Thrinakia, Lv 73–76): Kaminoo 25%, Taurivet 5%, Hymnet 20%, Hymnaria 5%, Sunkern and Sunflora 20%, Heliolisk 15%, Volbeat 10%.

### 6.9 The Outer Sea

The last sea before Scheria (on Scylla's way). It loops by day; at night, keep the Bear on your left (§4). Lynkeus, if aboard, finds **Proteus's islet** here: a sandbar with seals, where theoxenia E13 (SYSTEMS §10) happens if the extended tier is chosen. This is the sea-god, the Old Man of the Sea. Egypt's Pharaoh Proteus, the Oikoumene's champion at Memphis, is his namesake, and the seals on Pharos are the pharaoh's (`oikoumene/PERIODOS.md` §5).

### 6.10 Scheria: the Phaeacians

> *The Phaeacians, kindest of hosts, took the shipwrecked Odysseus in, held games in his honor, and had their bard sing of Troy until he wept. Their ships sail by thought, and they carried him home in one night while he slept* (*Odyssey* 6–13).

**Play.** Whichever way you came, you end up on the beach of Scheria. On Charybdis's way, you wash up there, and Princess Nausikaa and her friends find you while playing ball (scene 9). On Scylla's way, you sail into a harbor full of the most beautiful ships you've ever seen. The Phaeacians feed you, lend you clothes, hold games, and ask who you are. Their blind bard sings a song. It's about you.

**Maps:** Scheria's shore (30×24), the town of the Phaeacians (40×40, with an Asclepeion, an Agora and the king's hall), and King Alkinoos's hall (24×18).

**Steps.**
1. **The beach** (scene 9).
2. **The town.** The Phaeacians are the voyage's xenia (SYSTEMS §10): every door feeds you.
3. **The games** (optional): three Phaeacian youths challenge you, as they did Odysseus. Euryalos insults you first, as he did in Homer ("You look like a merchant, not an athlete"). Battles.
4. **The bard.** **Demodokos**, blind, sings the voyage: your voyage, built from your choices (the table below). It's a recap, and it's the moment the voyage looks back at itself.
   - **If Christopher Nolan is aboard,** he stands up before the first verse: "NOLAN: Sing it backwards." / "DEMODOKOS: …Backwards?" / "NOLAN: Start at the homecoming. End at Maleia. Trust me." ?? YES/NO lets him. Backwards, Demodokos sings the same verses in reverse, and ends: "DEMODOKOS: …It's better backwards. I hate that."
5. **The ship.** If Charybdis took the *Euploia*, the Phaeacians have rebuilt her, better (the Phaeacian keel). If not, they add the keel anyway.
6. **The night crossing.** "Sleep. When you wake, you'll be home." You lie down on the deck (scene 10). Fade.

**The bard's song.** Demodokos's verses are picked from the flags, one per island:

| Island | If… | Verse (one box) |
|---|---|---|
| Lotus | You ate three times | "Thrice the lotus touched their lips, and thrice they woke, ashamed." |
| Lotus | You never ate | "The lotus held their friends, but not the one with no thread." |
| Cyclops | You shouted your name | "They told the beast their name. The sea god heard it too." |
| Cyclops | You shouted NOBODY | "'Nobody!' they cried, and the island laughed with them." |
| Aiolia | Always | "They saw their home, and slept, and woke to every wind at once." |
| Aiaia | Always | "They put on a pig's shape, and found their friends in the mud." |
| Sirens | Wax / mast / bard | "They heard nothing, and steered by the wind." / "They heard it all, and begged, and were bound." / "Their bard sang louder, and the rocks were quiet." |
| Strait | Scylla / Charybdis | "Six were taken from the benches. Six were brought back." (if rescued) / "The whirlpool took the ship. They held a fig tree and waited." |
| Thrinakia | Spared / killed | "They were hungry, and they fished, and the Sun was pleased." / "They were hungry. The Sun remembers." |

The song ends: "And now they're here, at Alkinoos's table, and they haven't said their name." Then Alkinoos asks it. You give it, or "NOBODY", and the hall laughs either way.

**Bosses** (the games, optional):

| Who | Team (Lv 75–77) | Theme |
|---|---|---|
| Laodamas, the king's son | Geogrip, Hoplektor, Laolith | Wrestling |
| Klytoneos, the runner | Gelasable, Galenyon, Skylaps | Speed |
| Euryalos, the rude one | Kourodin, Dorydrake, Kolossard | Discus |

**Prize.** The Phaeacian keel. Nausikaa's gift: a Choice Scarf, "for running home." Demodokos's song for the music player. A Phaeacian oar (trophy). Scheria becomes a port you can sail back to.

**Wild Pokémon** (Scheria's shore, Lv 73–76): Galenyon 20%, Aphrell 15%, Aphrogene 5%, Pelipper 15%, Wingull 15%, Corphish and Crawdaunt 15%, Hisuian Qwilfish 15%.

### 6.11 The homecoming: Elaia

> *Odysseus woke on Ithaca in a mist Athena sent, not knowing his own island. She disguised him as an old beggar. His swineherd fed him, not knowing him. His old dog Argos knew him at once, and died. His wife set the suitors a contest: string Odysseus's bow and shoot through twelve axes. Then she tested him with a question only he could answer* (*Odyssey* 13–23).

**Play.** You wake on a beach in a thick white mist and don't know where you are. A young shepherd who isn't one tells you: this is Kalliste. Home. And there's trouble. Word came back from the Maleia storm that the Archon was lost at sea, and a crowd of fine people moved into Elaia to court your mother. They've been eating her food for months. Mom is Penelope (STORY §3). She's been weaving at her loom upstairs, a bridal veil, she tells them, and she'll choose when it's finished. Every night she unpicks what she wove that day.

You go in disguised as an old beggar. Amaryllis, the shepherdess from the start of the game, feeds you without knowing you. Your family's old hound lies by the gate in the rain, and lifts his head when you come near. Then your mother announces a contest.

**Maps.** Elaia's existing maps (SCRIPT.md: the village, the player's house 1F and 2F, the square), with a **homecoming object set** behind hide flags: the suitors, their tents in the square, the mess in the house. Plus the Mist Beach (24×20), a new small cove south of Elaia.

**Steps.**
1. **The mist.** Fog weather, and the Elaia theme slowed and muffled. The landmarks are hidden (scene 11).
2. **Athena,** as a young shepherd with no shadow, lifts the mist a little and disguises you as a beggar (the player's graphics switch to a beggar sheet, LABYRINTH's disguise state again). If you did theoxenia E3, she mentions the loom: "I warned a weaver once. This one I'm helping."
3. **Amaryllis** (the Eumaios role): in her hut by the olive groves, she feeds the "beggar" (xenia) and tells you what's happened. She's been sneaking Mom extra cheese.
4. **Argos.** By your house's gate, in the rain, the old hound (scene 12). He knows you. He thumps his tail. You can't call him, because you're in disguise, and that's the hardest moment of the voyage.
5. **The suitors.** Twelve of them, lounging in the square and the house. Talking to them is how you learn who they are: they're social climbers who want to be "the Archon's stepfather". None is a villain; most are ridiculous. One, Amphinomos, is kind to the beggar.
6. **Mom's contest** (scene 13): "I'll marry whoever can win twelve battles in a row without resting, the way my child did on Olympus." The suitors laugh and choose an opponent they're sure of: the beggar.
7. **The twelve axes.** A gauntlet of twelve trainer battles in a row, no healing between (the Bag works; it's a fair fight). The last is a double battle against the two ringleaders together, and Kleon steps out of the crowd to stand beside you (scene 14): `setmultitrainerbattle` (`asm/macros/event.inc` line 2665).
8. **The disguise drops.** Athena's work falls away mid-sentence. The square goes quiet.
9. **Mom's question** (scene 15): she doesn't run to you. She asks which jar on the shelf is yours.
10. **The veil.** Mom takes the veil off the loom, unfinished, for good. With the thread she unpicked every night she lines your cloak, the honey-gold one she finished after the Frozen Hour (STORY decision S13).
11. **The storm night.** If the theoxenia extended tier's finale is ready (SYSTEMS §10: E1–E13 done), the knock comes tonight. Two travelers in the rain. Otherwise it waits for its own night.

**The twelve suitors.**

| # | Suitor | Who he is | Team (Lv) |
|---|---|---|---|
| 1 | Leodes | A soothsayer who won't accept that prophecy has ended. "I foresaw this." | Mantipod, Melisseer, Sophowl (74) |
| 2 | Ktesippos | Throws things at the beggar | Taurivet, Laolith, Kolossard (74) |
| 3 | Amphinomos | The decent one. He warns the beggar to leave before it gets ugly. | Hierolive, Chelyra, Nostail (75) |
| 4 | Agelaos | A Thyrsa actor who rehearses his proposal | Prosomime, Oinopard, Thyrsivy (75) |
| 5 | Elatos | An Emporion merchant | Midonos, Harpelle, Plouteras (75) |
| 6 | Peisandros | A Lakonian veteran who won't stop talking about the battle school | Hoplektor, Dorydrake, Hoplomex (76) |
| 7 | Eurydamas | Writes poems to Mom | Hymnaria, Himerow, Kalliglyph (76) |
| 8 | Amphimedon | Brought his own chair | Starkos, Lykanax, Kaprodon (77) |
| 9 | Polybos | Sells olive oil, very loudly | Elapling, Hierolive, Basilops (77) |
| 10 | Demoptolemos | Has a speech about destiny he can't stop giving | Sophowl, Kourodin, Enigmaw (78) |
| 11–12 | **Eurymachos and Antinoos** | The ringleaders, smooth and loud. A double battle; Kleon is your partner. | Below |

| Ringleader | Species | Lv | Ability | Item | Moves |
|---|---|---|---|---|---|
| Eurymachos | Aphrogene | 79 | Marvel Scale | Leftovers | Scald, Moonblast, Calm Mind, Life Dew |
| Eurymachos | Pythoros | 79 | Intimidate | — | Earthquake, Outrage, Coil, Stone Edge |
| Eurymachos | Harpelle | 80 | Pickpocket | — | Knock Off, Brave Bird, Sucker Punch, Tailwind |
| Antinoos | Kynoketos | 80 | Moxie | — | Dragon Dance, Waterfall, Outrage, Ice Fang |
| Antinoos | Gigantomb | 80 | Solid Rock | — | Eruption, Earth Power, Stealth Rock, Heat Crash |
| Antinoos | Kingambit | 81 | Supreme Overlord | Black Glasses | Kowtow Cleave, Sucker Punch, Iron Head, Swords Dance |

The ringleaders are three each (it's a multi battle); Kleon brings three of his Labors team.

**After.**
- **The suitors leave.** Amphinomos stops to apologize to Mom. Leodes leaves predicting he'll be back.
- **Argos** joins your party (scene 12): Nostail, Lv 70, with Healing Wish, Extreme Speed, Follow Me and Helping Hand. In the old story the dog dies on seeing his master. Ichor doesn't do that (decision O4). Alethea: "In the old story the dog dies. Truthfully, I like ours better."
- **Melitta's Cloak, lined** (scene 15).
- **The Wings** work again.

**Engine.** The homecoming object set is hide flags on Elaia's existing maps. The beggar disguise uses the same avatar state as Circe's forms. The gauntlet is twelve scripted trainer battles with no heal between; the multi battle is vanilla. **Low.**

### 6.12 After: the true Periplous and the oar

- **Odysseus** visits Elaia the next day (or, if you go to Olympia first, he's at the Horse). He reads Alethea's corrected Periplous (scene 16). "Hm. I may have embellished the Cyclops." He gives you **the true Periplous** (key item): the sea map with every island, hidden islet and dive spot marked, which works like Daedalus's Compass (LABYRINTH §9) for the sea.
- **The oar inland** (optional). In Homer, Tiresias told Odysseus that to make peace with Poseidon he must carry an oar inland until someone took it for a winnowing fan, and plant it there. Odysseus never did. "Prophecy's over. But I'd still like him off my back." He gives you the *Euploia*'s spare oar.
  - Carry it inland. Most people say "Nice oar."
  - A farmer in Eleusa's fields, who has never seen the sea, says "Nice winnowing fan."
  - Plant it in his field and make an offering to Poseidon. Poseidon Favor +15; Poseidon's grudge, if any, is lifted for good; and the farmer gets a sea gift he can't explain. You get a Mystic Water and the last line of the arc (scene 16).

---

## 7. Bosses at a glance

| Boss | Where | Lv | Catchable |
|---|---|---|---|
| The great Polyphant | Cyclops Isle (if spotted, or if you boast) | 74 | No |
| Aeolus | Aiolia (optional) | 76–77 | — |
| Tornadus | At sea | 75 | Yes |
| Circe | Aiaia | 76–78 | — |
| Iapetos | The Sirens' skerry | 76–78 | — |
| Two Seirenade | The Sirens (by the bard) | 76 | Yes |
| Hexylla | Scylla's cave | 77 | Yes |
| Trybdis | The maw, or the Hoard | 77 | At the Hoard |
| The Phaeacian games | Scheria (optional) | 75–77 | — |
| Twelve suitors | Elaia | 74–81 | — |

---

## 8. Species casting and substitutions

| Bible | Ichor | Kind | Why |
|---|---|---|---|
| Polyphemus (Dusclops and Dusknoir) | **Polyphant** (#106), the great one | **Substitution** | The dex's Cyclops line, and its thesis made literal. Dusclops and Dusknoir move to the Underworld's tables. |
| Circe's swine (Lechonk and Oinkologne) | **Kaplet** (#55) | **Substitution** | The dex's piglet, Demeter's sacrifice. Lechonk can live on Aiaia's mud wallows as a post-game extra if wanted. |
| The Lotus-Eaters (Lotad and Ludicolo) | Lotad, Lombre, Ludicolo | Kept: **deliberate exception** | No Aethos lotus species, and the Lotad line is the joke. |
| The Sirens (Altaria) | **Seirenade** (#133) | **Substitution** | The dex's Siren. Altaria lives on Aiolia, and Olympias uses Mega Altaria (LABORS §4). |
| Scylla (Grapploct) | **Hexylla** (#135) | **Substitution** | The dex's six-headed snatcher |
| Charybdis (none) | **Trybdis** (#136) | From the dex | The dex's whirlpool maw |
| Aeolus's bag (Tornadus) | Tornadus | Kept | A legendary |
| Argos (none in the bible's Odyssey) | **Nostail** (#138) | From the dex | The dex places him at Elaia's homecoming |
| — | Proteus (**Haligeron**, #137) | From the dex | Theoxenia E13's islet is in the Outer Sea |
| — | Leukothea (**Lugia**), a cameo | Seed | Lugia is caught in Atlantis (POSTGAME §3). The bible puts Lugia in Atlantis. |

---

## 9. Rewards

| Where | Reward |
|---|---|
| Recruiting | Each crew member's service (§3); Lampon's flame; Kydon's honey |
| Lotus Isle | The Lotus Fruit (EV reset), Leaf Stone, Big Pearl, Max Revive |
| Cyclops Isle | The great ram (Dubwool), Moomoo Milk ×6, Rare Bone, Ichor Stone |
| Aiolia | **Aeolus's Bag**, the new sail, Tornadus, the Reveal Glass |
| Aiaia | Mints (shop), moly, Big Root, Mystic Water, Ichor Stone |
| The Sirens | By way: drift-lane items / the song in the Periplous / Seirenade and the tune |
| The Strait | Scylla's cave: the six oarsmen, Razor Fang, Hexylla. Or the Hoard: the hold, Big Nugget, Comet Shard ×2, King's Rock, Ichor Stone, Relicanth, Trybdis. |
| Thrinakia | A Sun Stone; Helios's favor for Labor 10 |
| Scheria | The Phaeacian keel, Choice Scarf, Demodokos's song |
| Elaia | **Melitta's Cloak, lined** (key: rest anywhere outdoors to dawn, noon, dusk or night, forward only, never past midnight, from the Relic Ring), **Argos** (Nostail), prize money from twelve suitors |
| After | **The true Periplous**; the oar's peace (Poseidon Favor +15, Mystic Water) |
| Favor along the way | Poseidon +10 (rounding Maleia and back), Hermes +5 (moly), Athena +10 (the mist), Hestia +5 (the ship's hearth), Zeus +3 per host (xenia) |

---

## 10. Music

| Cue | Use | Mode and feel |
|---|---|---|
| **The *Euploia*** | Aboard, below deck | Mixolydian 7/8, with the trieraules's aulos keeping the stroke (triremes really had a piper for the rowers) |
| **The wine-dark sea: under sail** | Sea maps, downwind | The same tune, fast, kithara over a swelling drone |
| **The wine-dark sea: rowing** | Sea maps, upwind or calm | The same tune, steady, with the oar-stroke drum |
| **Night sea** | Sea maps at night | The tune in Lydian, sparse, high bells for stars |
| The storm | Maleia, the bag, chasing Tornadus | 9/8 zeibekiko, all instruments, crashing |
| **The Lotus Isle** | Lotus | Lydian, honeyed, and it **never resolves**: a loop with no cadence |
| The Cyclops's cave | Stealth | A slow two-note breathing in the bass; the melody only while the eye is shut |
| Aiolia | Island and feast | Bright Mixolydian, bronze bells and wind |
| **Aiaia** | Circe's grounds | Phrygian 5/8, a hypnotic aulos, a little too sweet |
| **The Sirens' song** | The strait | The most beautiful melody in the game: Lydian, a female choir pad and lyre. Way 1 hears it muffled; way 3 hears it fighting Phemios's sea song. |
| The Strait | Scylla and Charybdis | 9/8 tension, low strings, a whirlpool swirl in the drone |
| Thrinakia | The Sun's island | A golden pastoral, Dorian, slowing as the hunger counter falls |
| Scheria | The Phaeacians | A warm 7/8 dance, the most festive town theme in the game |
| Demodokos's song | The bard | A solo lyre setting of the Odyssey's main sea theme |
| **Home in the mist** | Elaia, homecoming | The Elaia theme slowed and muffled |
| The suitors | Elaia, occupied | The Elaia theme as a raucous party tune, slightly out of tune |
| The twelve axes | The gauntlet | A bowstring motif over the trainer battle theme |
| **Recognition** | Mom's question, after | The Elaia theme restored in full, warm, then the main Ichor theme |

About **17 new tracks** (the three sea variants share a sequence).

---

## 11. Map list

| # | Map | Size | Tileset |
|---|---|---|---|
| 1 | The *Euploia*, deck | 24×12 | trireme deck (ART_PLAN, planned) |
| 2 | The *Euploia*, below deck | 20×10 | trireme deck |
| 3 | Maleia's waters | 80×60 | aethos sea |
| 4 | The eastern wine-dark sea | 80×80 | **wine_sea** (new) |
| 5 | The western wine-dark sea | 80×80 | wine_sea |
| 6 | The Outer Sea | 60×60 | wine_sea |
| 7 | Lotus Isle | 40×40 | **isles_west** (new) |
| 8 | Lotus Isle hut | small | oikos |
| 9 | Cyclops Isle | 40×40 | isles_west |
| 10 | The Cyclops's cave | 30×24 | cave + isles_west |
| 11 | Aiolia | 36×30 | **isles_magic** (new) |
| 12 | Aeolus's hall | 24×16 | isles_magic |
| 13 | Aiaia | 44×40 | isles_magic |
| 14 | Circe's hall | 24×18 | isles_magic |
| 15 | The Sirens' Strait | 40×50 | isles_magic |
| 16 | The Strait | 30×60 | isles_magic |
| 17 | Scylla's cave | 20×30 | cave + isles_magic |
| 18 | Charybdis's Hoard | 24×24 | underwater (post-Atlantis) |
| 19 | Thrinakia | 36×36 | isles_west |
| 20 | Proteus's islet | 16×12 | isles_west |
| 21 | Scheria's shore | 30×24 | isles_west |
| 22 | The town of the Phaeacians | 40×40 | isles_west |
| 23 | Alkinoos's hall | 24×18 | isles_west |
| 24 | Scheria's interiors (×3) | small | oikos, civic |
| 25 | The Mist Beach | 24×20 | kalliste |
| 26 | Elaia (homecoming objects) | existing | — |
| 27 | Akti (crew recruitment objects) | existing | — |

**MAP_DESIGN checks.** Each island that plays like a route (Lotus, Cyclops, Aiaia, Thrinakia, Scheria's shore) has a forced grass band between its landing and its set piece, an easy first trainer in plain view where it has trainers (the Lotus-Eaters, Circe's handmaids, the Phaeacian youths), a rest point (the ship, always), and an item in every dead end. Sea maps put visible floating items in the lee of rocks, so reaching them is a sailing problem.

---

## 12. Art list

### Tilesets

- **`wine_sea`** (new secondary): deep-sea water in Homer's wine-dark (a purple-red ramp at dusk and night, through the DNS tint), wreck timbers, sea rocks, fog banks, the floating-island shadow.
- **`isles_west`** (new secondary): the Lotus Isle's golden meadows and lotus trees; the Cyclops Isle's goat-cliffs, pasture and cave mouth (with cheese racks and the boulder door); Thrinakia's golden meadows; Scheria's harbor, palace and gardens (Homer's Alkinoos's orchard, where fruit never fails).
- **`isles_magic`** (new secondary): Aiolia's bronze wall and hall; Aiaia's woods, sty, wolf run, lion court, three form fountains and the restoring spring; the Sirens' white rocks; the Strait's cliff with Scylla's cave mouth and Charybdis's whirlpool (an animated 4×4 ring).
- **Trireme deck** (planned by ART_PLAN §1 for the slice's crossing): add the bunk, hearth, stall, altar, trophy shelf and chart table.

### Sprites and portraits

| Who or what | Overworld | Portrait |
|---|---|---|
| **The *Euploia*** at sea | 64×64, 4 directions × 2 frames, with sail states (full, slack) | — |
| Phemios, Lynkeus, Christopher Nolan | 16×32 each (Nolan: a dark himation pinned neatly over a pale chiton) | — |
| Lampon, Diktys, Kydon, Glaukias, Iaso | Existing walkers | — |
| The Lakonian oarsmen | Existing Lakonian class walker | — |
| Aeolus | 16×32 | 64×64 |
| Circe | 16×32 | 64×64 |
| Hermes (disguised), Athena (shepherd) | Theoxenia's disguise sprites (SYSTEMS §10) | — |
| Glaukos the sea-god | 32×32, in the water | 64×64 |
| Nausikaa, Alkinoos, Demodokos | 16×32 each | Nausikaa only |
| Lotus-Eater (class), Phaeacian youth (class) | 16×32, palette variants | 64×64 each |
| Suitor (class) | 16×32, three palettes | 64×64 |
| Antinoos, Eurymachos | Suitor class palette variants | Their own 64×64 |
| Mom at her loom | A 2-frame pose | Exists |
| The player as a beggar | 2 sheets (one per gender) | — |
| The player as a pig, a wolf, a lion | **No new art:** Kaplet's, Lykopup's and Nemecub's follower sprites | — |
| The great Polyphant | Polyphant's follower sprite, at 64×64 | — |
| Tornadus's storm cloud | 32×32, animated | — |
| Leukothea's white bird | 32×32 silhouette | — |

### Objects and effects

- The bag of winds (24×24 item and an overworld object), moly, the Lotus Fruit, the Periplous and the true Periplous, the lined cloak, the Reveal Glass (the expansion's icon, restyled): item icons.
- Floating items at sea (a bobbing amphora), the fig tree over Charybdis, the six-necks strike (a scripted 32×64 effect), the eye glow.

### Battle backgrounds

- **The deck** (for battles at sea: a planked deck with the sea behind), **the Cyclops's cave**, **Aiaia's garden**, **the Strait**, **Scheria**, **Elaia at night**. Six new.

### Pictures

- **The sight of home** from the sea (240×160).
- **The fake ending's** gold card (240×160, mostly text on gold).

---

## 13. ROM estimate

| Item | Size |
|---|---|
| Sea maps (4, large) | ~60 KiB |
| 23 other maps (layouts and events) | ~90 KiB |
| Three new tilesets and the deck additions | ~60 KiB |
| Scripts and text (about 1,000 lines, the bard's song, the Sirens' verses, twelve suitors) | ~115 KiB |
| Portraits (10) and overworld sprites (about 18 sheets, including the 64×64 ship) | ~45 KiB |
| Battle backgrounds (6) | ~40 KiB |
| Music (about 17 tracks) | ~60 KiB |
| Pictures (2), item icons, effects | ~35 KiB |
| **Total** | **~505 KiB** |

---

## 14. Engine summary

| Mechanic | Approach | Files | Effort | Fallback |
|---|---|---|---|---|
| The ship at sea | The surf state with a 64×64 ship graphics id on sea maps | `src/field_player_avatar.c`; `OW_LARGE_OW_SUPPORT` | Low–Medium | The dolphin |
| Wind speed | A surf-speed branch reading `IchorSave.epics.wind` | `src/field_player_avatar.c`, `src/wild_encounter.c` | Low–Medium | Fixed speed, wind as flavor |
| Daily wind | `DoDailyEvents` | `src/clock.c` | Low | — |
| Currents | Vanilla current behaviors | `include/constants/metatile_behaviors.h` | Low | — |
| Stars and the Outer Sea loop | Self-connections, a night-and-facing edge check | Map scripts | Low | A guide NPC at night |
| Fog banks | Fog weather plus hide-flag collision; the Bag as Defog | `include/config/overworld.h` (`OW_DEFOG_FIELD_MOVE`) | Low | — |
| Wings off at sea | A flag the Wings' field use checks | `src/item_use.c` | Low | — |
| Frozen clock (Lotus) | A map flag the DNS tint and `gettimeofday` read | `src/overworld.c` | Low | Fixed tint only |
| Escort at a distance (Lotus) | Scripted escort with a distance check | Scripts | Low | — |
| The eye (Cyclops) | Non-battle sight with an on/off cycle, ignoring the flock | `src/trainer_see.c` | Low–Medium | Scripted waves |
| Clinging under a sheep | Hide the player and attach to the sheep's script | Scripts | Low | — |
| Tornadus's storm | A moving object along the wind; map transfer | Scripts, `src/roamer.c` pattern | Medium–Low | A static at a fixed spot |
| Forms (Circe), beggar (home) | A player graphics state using species or beggar sheets | `src/field_player_avatar.c` (LABYRINTH's disguise state) | Medium | Icon over the player |
| Pigs follow a pig | Follow movement on object events | `src/event_object_movement.c` | Low–Medium | Scripted lines |
| Sirens: wax | Rowing refused unless downwind or on a current | `src/field_player_avatar.c` | Low–Medium | Way 2 only |
| Sirens: mast | `multichoicedefault` | `asm/macros/event.inc:954` | Low | — |
| Charybdis's fig tree | LABYRINTH's timing task | `src/ichor_bull_leap.c` | Low | A yes/no |
| Hunger (Thrinakia) | A step counter and Bag checks | Scripts | Low | — |
| The bard's song | Flag-driven verse selection | Scripts | Low | — |
| The twelve axes | Twelve scripted battles; a multi battle | `asm/macros/event.inc:2665` | Low | — |
| Lotus Fruit | A new item that zeroes EVs | `src/data/items.h`, `src/item_use.c` | Low | — |

**Risk: low to medium.** The biggest single piece is the sailing layer (the ship sprite and the wind speed), which every sea map depends on. Build and playtest it first, with one sea map, before any island.

---

## 15. Flags and vars

**Vars: one.**

| Var | Holds |
|---|---|
| `VAR_ICHOR_ODYSSEY` | Story state 0–30: ship given, crew ready, Maleia rounded, each island's done-state, the bag opened, the bag won, the Strait passed, Scheria, home, the suitors gone, the cloak, the Periplous |

**Save data** (`IchorSave.epics`, POSTGAME §6):

| Field | Holds |
|---|---|
| `crew` (u16) | Recruited crew, one bit each (10) |
| `oarsmenTaken` (u8) | Scylla's toll, 0–6, and which were rescued (bits) |
| `wind` (u8) | Direction (3 bits), strength (2 bits), Poseidon's grudge (1 bit), becalmed (1 bit) |
| `storm` (u16) | Tornadus's sea map and position while loose |
| `voyage` (u16) | Choices: lotus count (2 bits), the boast (2 bits), the Sirens' way (2 bits), Scylla or Charybdis (1 bit), Thrinakia spared or not (2 bits), the hold lost (1 bit), the Hoard recovered (1 bit) |
| `shipUpgrades` (u8) | Ram, sail, keel |

**Flags** (about 35, `FLAG_ICHOR_*`, from freed Hoenn story flags):

| Group | Flags |
|---|---|
| Items | `GOT_PERIPLOUS`, `GOT_TRUE_PERIPLOUS`, `GOT_AEOLUS_BAG` (SYSTEMS's relic flag), `GOT_MOLY`, `GOT_CLOAK_LINING`, `GOT_REVEAL_GLASS`, `GOT_SPARE_OAR`, `OAR_PLANTED` |
| Story | `AT_SEA` (Wings off), `SAW_HOME`, `BAG_OPENED`, `LOTUS_FAKE_END`, `CIRCE_BARGAIN`, `GLAUKOS_GOD`, `NAUSIKAA`, `HOMECOMING`, `SUITORS_GONE`, `MOM_KNEW` |
| Encounters | `TORNADUS`, `GREAT_RAM`, `SEIRENADE_PAIR`, `HEXYLLA`, `TRYBDIS`, `ARGOS_JOINED` |
| Hide flags | About 20: the suitors (12), their tents, the dazed crew, the pigs, Aiolia's four positions (one var-picked set instead of flags if short) |

---

## 16. Scenes

Dialogue in SCRIPT.md's format: one box per line, `[brackets]` are directions, `{PLAYER}` is the player.

### Scene 1. Akti: the ship

[Akti's quay. The *Euploia* rides at her mooring. Nausikles sits on a bollard, coiling a rope he doesn't need to coil. Alethea stands on the deck with a satchel.]
```text
NAUSIKLES: There you are. The Archon. I carried you off this island once.

NAUSIKLES: You were seasick the whole way. Don't deny it.

NAUSIKLES: The fishermen say there are islands past Maleia now. New ones.

ALETHEA: Not new. Just reachable. The map stopped at Maleia for a reason.

ALETHEA: Nobody was fated to go past it. Now nobody's fated not to.

NAUSIKLES: I'm too old to sail off the edge of the world.

NAUSIKLES: So she's yours. The Euploia. I'll come as far as the edge.

NAUSIKLES: …And then a bit further, probably. One more voyage. Then I'm done.

ALETHEA: I'm coming too. Truthfully, you'd get lost.
```

### Scene 2. Olympia: Odysseus's briefing

[The Horse, at Olympia. A broad, gray-bearded man with clever eyes sits on an upturned crate, carving a small wooden horse.]
```text
ODYSSEUS: Going west? Past Maleia? I did that once. Took me ten years to get back.

ODYSSEUS: Here. My chart. Every island, and what's on it. I drew it myself.

{PLAYER} received the Periplous of Odysseus!

ODYSSEUS: The Cyclops will ask your name. Say "Nobody." Trust me.

ODYSSEUS: Don't eat the lotus. Don't trust the witch. Don't listen to the singing.

ODYSSEUS: And if a king gives you a bag, sleep with your hand on it.

ALETHEA: [later, reading it] "One-eyed giant, tall as a mountain." Hm.

ALETHEA: He also says he fought a sea-monster with a single oar. I'll be checking.
```
[Across the Altis, at the Stadion's tunnel, Achilles is stretching. He calls over.]
```text
ACHILLES: Going west? I was offered that once. Not west. The choice.

ACHILLES: Short life, and they sing about you forever. Or a long one, and home.

ACHILLES: Your friend Kleon picked glory. I watched him at the Heraion. Good for him.

ACHILLES: What'll you pick?

ACHILLES: …Don't tell me. Just sail. I'll know by which way you come back.
```

### Scene 3. Akti: ready?

```text
NAUSIKLES: Once we round Maleia, there's no going back the way we came.

NAUSIKLES: Your Wings won't find a herm out there. The sea has no roads.

NAUSIKLES: We'll have the bunk and the hearth. Whatever's in the hold. That's all.

NAUSIKLES: Ready?
```
?? CAST OFF / NOT YET

### Scene 4. The Lotus Isle

[A golden meadow. The light doesn't change. Alethea frowns at the sky.]
```text
ALETHEA: The sun hasn't moved since we landed. Not a hair.

ALETHEA: Everyone's happy. Nobody's going anywhere. Nothing ever changes.

ALETHEA: This is what Kronos wanted. Just smaller. And with fruit.

LOTUS-EATER: Have one. You look tired. Everyone looks tired when they arrive.

LOTUS-EATER: Nobody looks tired after.
```
[After the fake ending.]
```text
ALETHEA: {PLAYER}! Up. You ate it. Three times.

ALETHEA: You were lying in a hammock telling a Lotad about your feelings.

ALETHEA: Truthfully, I'm impressed. Let's go before you do it again.
```

### Scene 5. Aiolia: the bag

[Aeolus's hall, after the feast. A huge, laughing man with wind-blown hair holds up a bag of ox-hide, tied with a silver cord.]
```text
AEOLUS: Every wind there is, in here. Except the West. She'll take you home.

AEOLUS: Don't open it. Don't let anyone. It isn't gold, whatever it sounds like.

AEOLUS: My girl's bird calms the sea every winter. Seven days. Halcyon days.

AEOLUS: You were stuck in them once, I hear, on a quay. Sorry about that.
```
[At sea, the full-screen picture: a small bright coast far off, an olive on a hill.]
```text
ALETHEA: That's Kalliste. That's home.

ALETHEA: Truthfully, I didn't think we'd see it again.

NAUSIKLES: Get some sleep, {PLAYER}. We'll be in by dawn.
```
[The chart table. Glaukias creeps past and crouches by the bag.]
```text
GLAUKIAS: Nobody gets a bag like that for nothing.

GLAUKIAS: Just a peek. Just to see.
```
[He unties the cord. Every wind at once.]
```text
NAUSIKLES: GLAUKIAS!

GLAUKIAS: Sorry! Sorry, sorry, sorry!
```
[Later, at Aiolia again. Aeolus doesn't smile.]
```text
AEOLUS: You're back. With the bag open. Of course you are.

AEOLUS: The gods must hate you. Go away.

AEOLUS: …One wind didn't come back. The storm. He likes being loose.

AEOLUS: Bring him back, and we'll talk.
```

### Scene 6. Aiaia

[The landing. An oarsman stumbles out of the woods.]
```text
OARSMAN: Pigs! They're all pigs! She gave them wine and they turned into pigs!

OARSMAN: I didn't drink. I don't drink. I'm Lakonian.
```
[The woods path. A young man with a golden wand. There is no shadow under him.]
```text
YOUNG MAN: Going to the witch's? Eat this first. The root's bitter.

YOUNG MAN: It's called moly. Mortals can't dig it up. Lucky I'm not a mortal.

{PLAYER} received moly!
```
[Circe's hall. A tall woman with gold-bright eyes at a loom, singing. She stops.]
```text
CIRCE: A guest. Sit. Drink. Everyone drinks.
```
[You drink. Nothing happens. She looks at the cup, then at you.]
```text
CIRCE: …Hermes. It's always Hermes.
```
[After the battle.]
```text
CIRCE: Fine. I'll give them back. Bring them to my spring.

CIRCE: They're with my other pigs. And pigs only follow pigs.

CIRCE: Drink from my fountains. You'll see.

CIRCE: You're going past the Sirens next. Then the strait.

CIRCE: Hug Scylla's side. Six is better than all.

CIRCE: …Unless all is coming back. Then do what you like.
```

### Scene 7. Glaukos, the sea-god

[The shallows off Aiaia. A green-bearded man surfaces to the waist. Below the waist, he's a fish.]
```text
GLAUKOS: {PLAYER}! It's me! Glaukos! From Akti! I gave you a rod!

GLAUKOS: I ate the strange seaweed again. Didn't wear off this time!

GLAUKOS: I'm a god now. A little one. Mostly I tell sailors the weather.

GLAUKOS: Used to tell them their futures. Not allowed now. Prophecy's over.

GLAUKOS: Sirens next. Wax, the mast, or a good loud song. Pick one.

GLAUKOS: Is my grandson with you? Is he behaving?

GLAUKIAS: …

GLAUKOS: Ha! I'll take that as a no.
```

### Scene 7a. The Sirens' skerry: Iapetos

[A bare rock at the mouth of the strait. Under a sailcloth awning, a thin man in a faded blue-bordered himation sits at a driftwood desk, writing on a wax tablet. Stacks of tablets are weighted down with stones. Out on the rocks, the Sirens are singing his last verse. He doesn't look up.]
```text
IAPETOS: May I tell you something true?

IAPETOS: They'll sing anything. Anything at all. Do you know how rare that is?

IAPETOS: Ten years' exile, your Assembly said. Place unknown. Well. It's known now.
```
[He sees Alethea, and puts the stylus down.]
```text
ALETHEA: You're writing for them.

IAPETOS: I'm improving them. They used to sing about Troy. Dreadful. All facts.

IAPETOS: Now they sing people the thread they wish they had. They come so gladly.

ALETHEA: They come onto the rocks.

IAPETOS: Every story has a price, Keeper. You know that. You've read mine.

ALETHEA: I've read all of them. That's the job now. Truthfully, they're not that good.
```
[He laughs, for the first time, and stands.]
```text
IAPETOS: A critic. Then let's see you revise this.
```
[After the battle. He sits back down and picks up his stylus.]
```text
IAPETOS: Every draft has a next draft.

ALETHEA: These tablets. We'll take them.

IAPETOS: My drafts? Whatever for?

ALETHEA: Wax. For our ears.

IAPETOS: …That's almost witty. Take them. I'll write more.
```

### Scene 8. Thrinakia

[If the crew killed a calf. A tall shape of light stands over the meadow.]
```text
HELIOS: I see everything. That's the job. I saw that.

HELIOS: Hungry, were they. Hm.
```
[A bolt. The ship rocks. No one is hurt; the hold is gone.]

[If the crew were fed.]
```text
HELIOS: Your crew were starving, and you fished. And foraged. And waited.

HELIOS: Nobody waits. Take this. A little piece of the afternoon.

{PLAYER} received a Sun Stone!

HELIOS: I'll remember. I'm told I'm good at that.
```

### Scene 9. Scheria: Nausikaa

[Charybdis's way. A beach. You wake face-down in the sand. A ball bounces past your head. A girl in a white dress runs after it, and stops.]
```text
NAUSIKAA: Oh!

NAUSIKAA: Girls! There's a person! A sea-person! Don't scream!

NAUSIKAA: …They screamed. Sorry. Are you all right? You look half drowned.

NAUSIKAA: You're on Scheria. My father's the king. We like guests. Come up.
```

### Scene 10. The night crossing

[Alkinoos's harbor, at night. The *Euploia* sits low and sleek with the Phaeacian keel.]
```text
ALKINOOS: Our ships know the way to any home. You only have to sleep.

ALKINOOS: When you wake, you'll be there. You won't remember the crossing.

ALKINOOS: Nobody ever does. It's the best part.
```

### Scene 11. The mist

[A white beach. Fog everywhere. The music is a slowed, muffled Elaia theme.]
```text
{PLAYER} doesn't know this beach.

ALETHEA: Where are we? I can't see anything.
```
[A young shepherd with a crook comes out of the fog. No shadow.]
```text
SHEPHERD: Lost? This is Kalliste. That's Elaia, up the path.

SHEPHERD: There's trouble at your house. Strangers. Lots of them.

SHEPHERD: Word came you'd drowned off Maleia. So they came to court your mother.

SHEPHERD: Go in as nobody. It's what you're best at. Hold still.
```
[A flash. You're an old beggar in a torn cloak.]
```text
SHEPHERD: I warned a weaver once. This one I'm helping.
```

### Scene 12. Argos

[Your gate, in the rain. An old gray-muzzled hound lies in the mud by the wall. The suitors have put him out. He lifts his head as the beggar comes near.]
```text
The old hound lifts his head.

He looks at the beggar for a long time.

His tail thumps the mud. Once. Twice.

You can't call him. Not yet.
```
[After the recognition, by the hearth.]
```text
MOM: He knew you first, didn't he. Before any of us.

ALETHEA: In the old story the dog dies, when he sees his master.

ALETHEA: Truthfully, I like ours better.
```
[Argos gets up, stiffly, and comes to stand by you.]
```text
Argos wants to come with you.

{PLAYER} received Argos!
```

### Scene 13. Mom's contest

[The square. Twelve suitors lounging. Mom comes down from the house with a basket of wool and stands on the well's step.]
```text
MOM: Listen, all of you. I've decided.

MOM: My child won twelve battles in a row on Olympus. Without resting.

MOM: I'll marry whoever can do the same. Here. Today.

ANTINOOS: Twelve? Against whom?

MOM: Against whoever you like.
```
[The suitors look around. They see the beggar.]
```text
ANTINOOS: Him. The old beggar. One each. Then whoever's left gets the lady.

MOM: …Fine. The beggar it is.
```

### Scene 14. Kleon steps in

[The last battle. Antinoos and Eurymachos step up together.]
```text
ANTINOOS: Two at once. Rules are rules. We made them up just now.
```
[A figure pushes through the crowd, olive crown on his head if Labors are done.]
```text
KLEON: Two on one? In Elaia? In front of my rival's mother?

KLEON: I don't think so. I'll stand with the beggar.

KLEON: [quietly] I know those feet. Don't say anything. Fight.
```

### Scene 15. Mom's question

[The square, after. The disguise is gone. The village has gone silent. Mom doesn't run. She looks at you for a long time.]
```text
MOM: You look like my child.

MOM: People have looked like my child before. Mostly in the dark.

MOM: So. On the shelf at home there are jars of honey. Which one is yours?
```
?? THE BIG ONE / THE ONE BY THE HEARTH / THE ONE THAT SAYS NOT FOR {PLAYER}
```text
> THE BIG ONE / THE ONE BY THE HEARTH:
MOM: Hm. Try again. You never were quick in the morning.

> THE ONE THAT SAYS NOT FOR {PLAYER}:
MOM: …

MOM: That's the new jar. I labelled it out of habit. Only you would say it was yours.
```
[She puts down the basket. She doesn't say anything else for a while.]

[Later, upstairs. The loom. A pale-gold veil with a honeycomb hem, half woven, the same every morning for months.]
```text
MOM: I wove it every day. And every night I took out what I'd woven.

MOM: I said I'd choose when it was finished. It was never going to be.

MOM: I've done this before, you know. Unmade something, so nobody could decide it for me.

MOM: Last time it was you.
```
[She cuts the veil off the loom, unfinished. Morning. She holds out your cloak, the honey-gold one, heavier now.]
```text
MOM: I lined it. With everything I unpicked. Months of it.

{PLAYER} received Melitta's Cloak, lined!

MOM: Sleep in it anywhere. Under a tree. On a hill. Wherever you are.

MOM: You'll be warm. And you'll come back up. Every time.
```

### Scene 16. Odysseus reads the true chart

[The next day. Odysseus has come to Elaia, and Penelope with him: a tall, gray-haired woman who goes straight upstairs to look at Mom's loom. Through the window you can hear them.]
```text
PENELOPE: Every night?

MOM: Every night. For months.

PENELOPE: Three years, I did it. Then my maid told them.

MOM: Mine didn't. I haven't got a maid. I've got a bee.

PENELOPE: …Teach me the honeycomb hem.
```
[Outside, Odysseus sits on Amaryllis's wall with the corrected Periplous across his knees. Alethea stands over him.]
```text
ODYSSEUS: "TRUTH: the Cyclops is an elephant." Hm.

ODYSSEUS: "TRUTH: the Sirens don't know anything. They just sing it well."

ODYSSEUS: "TRUTH: the sea-monster was a crab. A normal-sized crab."

ALETHEA: You said it was as big as a ship.

ODYSSEUS: It was a very confident crab.

ODYSSEUS: …I may have embellished the Cyclops. Keep this one. It's better.

{PLAYER} received the true Periplous!

ODYSSEUS: One more thing. A blind man told me once to carry an oar inland.

ODYSSEUS: Until someone calls it a winnowing fan. Then Poseidon forgives you.

ODYSSEUS: I never did. Too busy being home. Prophecy's over, but still.

ODYSSEUS: I'd like him off my back. Would you?
```
[Later. A wheat field in Eleusa. A farmer squints at the oar on your shoulder.]
```text
FARMER: Nice winnowing fan. Where'd you get one that size?
```
[You plant it. You make the offering. Somewhere very far off, the sea goes quiet.]
```text
ODYSSEUS: [a letter, delivered by Hermes's herald at Olympia] He's off my back. I can tell.

ODYSSEUS: The fish are biting again. Thank you. And thank your crab-checker.
```

---

## 17. Proposed changes

**To PITCH.md:**
1. **§6.4.** Replace the island list with §5's table, and add: "Your own trireme, the *Euploia*, given by Nausikles, with a crew you recruit across Aethos. Sailing by wind, current and stars. The voyage is one way until you're home. It ends at Elaia with Mom's suitors, Argos the hound, and a question about a honey jar."
2. **§2, Alethea's arc:** "the chronicler of the voyage; truth against the embellished story."
3. **§6.3.** Odysseus gives the Periplous before the voyage and reads the true one after.

**To SCRIPT.md (the slice, the Narrative team's call):**
1. **The player's house:** add **Argos**, the family's old hound, asleep by the hearth. Interacting: "Argos, the old hound. He thumps his tail once and goes back to sleep." One object and one line. Without it, the homecoming's dog is a stranger. (Decision O7.)
2. **Mom's loom** line, already in the slice ("A half-woven traveling cloak. Mom says you'll need it someday."), is the seed. STORY finishes the cloak after the Frozen Hour (decision S13); the homecoming's new weaving is the veil, and its thread lines the cloak. No slice change needed.

**To SYSTEMS.md:**
1. **§1, relic 13:** Aeolus's Bag comes from Aeolus after Tornadus is recaptured (§6.4).
2. **§10, E13:** Proteus's islet is in the Outer Sea, and Lynkeus reveals it.

**To TERMS.md:** name the Reveal Glass (proposal: **Mirror of Truth**), Melitta's Cloak and the Periplous.

**What changed when STORY.md and BALANCE.md landed** (they win; listed so the director can check):
1. **Iapetos is on the Sirens' rocks,** writing their songs, and the wax for Way 1 is melted from his own tablets (STORY §3). It replaces Kydon's beeswax. Alethea faces him again.
2. **The Sirens sing glory and a better story,** and the voyage resolves Achilles's choice: Kleon chose glory, you choose home (§1).
3. **Mom is Penelope,** explicitly, and **the real Penelope** visits Elaia at the end (scene 16).
4. **The cloak** was finished after the Frozen Hour (STORY S13); Mom now weaves and unweaves a veil, and lines the cloak with it.
5. **The honey jar** in the recognition is the new one, "labelled out of habit" (STORY §8.3).
6. **Alethea** is Keeper of Records, on leave. **You're the Archon** throughout.
7. **Levels** follow BALANCE.md's Oikoumene row, since the wine-dark sea lies outside Aethos.
8. **Legendaries placed here,** for LEGENDS.md: Tornadus (at sea, Lv 75). Lugia appears only as a cameo; she's caught in Atlantis (POSTGAME §3.2).

---

## Decisions for the user

- **O1. One way.** Once you round Maleia, the Wings don't work until you're home (recommended: it's what makes the homecoming land). The alternative is free travel, which breaks the suitors' premise.
- **O2. The Cyclops is a Polyphant,** a Pokémon, not a talking giant: the dex's own thesis, with Odysseus's tale as the embellishment and "NOBODY" kept as the boast. It isn't catchable.
- **O3. The suitors** are comic social climbers courting Mom, because her child is the Archon. Check the tone: it's played for laughs, and Mom is in control throughout.
- **O4. Argos lives** and joins you, instead of dying as in Homer.
- **O5. Scylla takes oarsmen,** never named crew, and you can rescue them. Charybdis takes the ship's hold, recoverable much later.
- **O6. The fake ending** on the Lotus Isle, after three lotuses.
- **O7. The slice seed:** an old hound asleep by the hearth in the player's house, from the first minute of the game.
- **O8. Crew scope.** Ten crew (recommended), or the required three plus four (Lampon, Kydon, Phemios, Lynkeus), which keeps every island's choices and cuts three recruitment scenes.
- **O9. The Lotus Fruit** resets a Pokémon's EVs.
- **O10. Iapetos on the Sirens' rocks** (STORY §3's suggestion, adopted), with a battle and his melted tablets as the wax.
- **O11. The wine-dark sea is Oikoumene territory** at the Oikoumene's levels, to be placed on that map by OIKOUMENE.md (recommended), rather than a separate third map.
- **O12. Penelope's visit** to Elaia at the end: a short scene of two weavers.
