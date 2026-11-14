# Phase 2 script: Act I on the mainland, from the trireme to the unspun thread

Owner: Narrative. Source of truth for Phase 2's scene dialogue, NPCs, trainers, encounters, the two temple rites, the Mystery sanctum and item placement. Map and script agents implement from this file. It continues `design/phase1/SCRIPT.md` from beat 9. Where it conflicts with `design/PITCH.md`, the bible wins; where it touches `design/SYSTEMS.md` or `design/LABYRINTH.md`, those specs win on mechanics and this file supplies the words. Every deviation is listed in Open questions.

## How to read this file

Phase 1's conventions hold (SCRIPT.md, "How to read this file"). In short:
- Each line is one text box, about 2 lines of 36 characters. A blank line separates boxes. `NAME:` opens a speaker's turn.
- `[brackets]` are stage directions. `{PLAYER}` is the player's name and `{STR_VAR_1}` is set by the script.
- Choices are `?? YES/NO` or a multichoice, then `> YES:` and `> NO:` branches.
- The charmap has no em dash and no straight double quote. Dialogue uses `…`, `-` and “ ”.

Four more for Phase 2:
- **Species are the Aethos dex** (`design/dex/` on `claude/aethos-dex-a7c73a`), because the regional dex is Aethos-only until the League (dex decision D5). Constants are written `SPECIES_<NAME>` and will exist when the dex is implemented.
- **The starters are the Aethos three** (dex decision D1). `VAR_STARTER_MON` keeps the slice's order: 0 is Nebrel (Grass), 1 is Kynder (Fire), 2 is Hipling (Water). Kleon takes the one that beats yours, as in the slice, and Alethea has the third (beat 10).
- **"Per SYSTEMS.md"** marks a system that SYSTEMS.md specifies. The text here says what the player sees; the rules, numbers and engine notes are SYSTEMS.md's.
- **Maps** are named in the slice's style (`MAP_EMPORION_CITY_TEMPLE_OF_HERMES`). The mainland route ids are provisional until the geography agent's `design/AETHOS_MAP.md` lands (Open questions 1).

---

## Act I's second half in one paragraph

Before you sail, Halia reads your hand once more by lamplight, and is frightened by what she doesn't see. Your mother walks you down to Akti's quay and doesn't cross the water. The halcyon days end and the *Euploia* sails, with Alethea and the blind mole she dug up aboard, and Kleon green at the rail with his Hearth Laurel, won overnight. Mid-sea the calm comes back and the piper's reed splits; Kleon keeps the stroke with a Lakonian marching chant while you fight off the snatchers diving at the last halcyon nest. When the chicks hatch, the wind returns, but too late to make port. That night the tide runs the wrong way, a trireme with no lights slides past, and Kleon reads you his mother's two-line letter. The ship puts in at Aegina, and at the inn table Kleon admits what it's like when everyone already knows how your story ends. Emporion is the harbor of the world, and its herald is Kerykos, who talks your ear off, teaches you to pray at a herm and anoint it with oil, and turns out to be the Hierophant of Hermes. Alethea gives you a trowel, learns at the exchange hall that a big man who pays in silver bought shovels, rope and forty lamps, and notices a little hook under the Archon's seal on a public notice. Kleon wins the Herald Laurel first and wins the race he set, then loses to you at the Sacred Gate and admits he would like someone to tell him death isn't the end. On the Sacred Way you break the Titans' rockslide with the Bronze Hammer from Emporion's cold forge, so the procession of initiates can walk to the Mysteries. In Hecate's Hollow, in the pitch dark, you follow a dog's bark to the three-faced pillar and leave the goddess her supper; she gives you her Torch. The road goes on down Mount Aigaleos's pine slopes, past the rock where a king once watched his fleet lose, through the roadside hamlet of Thria, and across the salt streams where masked jesters insult every pilgrim. At Eleusa's gate a woman ties a saffron thread on every pilgrim's wrist, and yours keeps slipping off. Chloe, the silent Mystagogue, tests you in the dark Telesterion and shows you the secret: what's reaped grows again. On the night of the Mysteries, Titanborn burst up through the floor of the hall, and Kleon fights beside you for the first time. Under the granaries, Hyperion of the Titans squints into your torchlight while his diggers carry off the first fragment of the Harpe; he can't see a thing down there, and he loses to you anyway. Chloe gives you Demeter's own sickle, which the Titans tossed aside. Next morning, in the wrecked hall by one lamp, Daphne, seasick from her first crossing in thirteen years, tells you what you are: there is a Loom where the Fates weave every life, and you aren't on it. Why is your mother's to tell. Then she reads the back of the Titans' tablet. They have a word for you: the Unwoven.

**The dread,** one line each, building on the slice's list:
- Halia, after forty years of reading threads, has never once seen nothing.
- The tide runs the wrong way at night, and a Titan trireme passes with no lights.
- A sailor: the Pythia only says "soon" now.
- The Rharian field came up twice this year: up, then back down, then up.
- Krokis's saffron thread will not stay on your wrist.

**What Phase 2 must not do** (STORY.md §3, Act I): say why the hero has no thread; reveal Phaedon or name Iapetos; hint that Kleon's mother is a Titan; give away the third krater. This script keeps to all four.

---

## The route plan

Act I is a corridor (MAP_DESIGN §5), but a long one. The user wants the mainland to feel far: "it should feel like we are traveling farther". So every stretch is two or three routes with a waypoint between them, each route 2–5 screens long (MAP_DESIGN §1), and the crossing is a voyage with a night ashore. The geography agent and the director can reconcile these chains with `design/AETHOS_MAP.md`.

**The chains**
- **The voyage:** Akti Town → the *Euploia*, the open sea (the halcyon calm) → **Aegina Town**, a night ashore → the *Euploia*, the Saronic Gulf → Emporion City.
- **The Sacred Way, the main path:** Emporion City → Route 2, the Sacred Way → **Hecate's Hollow**, the pass under Mount Aigaleos → Route 3, the Pine Slopes → **Thria**, a hamlet and inn at the edge of the plain → Route 4, the Rheitoi → Eleusa Village.
- **The Halai Shore, optional:** Emporion City → Route 5, the Halai Beach → **Halai**, a salt hamlet → Route 6, the Halai Cliffs → the cape (a dead end).
- **Aegina, an optional detour** (proposed; Part 2): Aegina Town → the Aphaia Road → the Temple of Aphaia, with a spur up Mount Oros.
- **Onward, Act II:** Eleusa Village → the Eleutherai road (vines) → Thyrsa. Emporion City → the Long Walls Road (closed) → Astyra.

```
 [AKTI TOWN, Kalliste, the Cyclades]
        |   the Euploia: the open sea, the halcyon calm
 (AEGINA TOWN)  a night ashore ----- optional: the Aphaia Road -> Temple of Aphaia; Mount Oros
        |   the Euploia: the Saronic Gulf
 [EMPORION CITY] ----- the Long Walls Gate (closed) -----> [ASTYRA, Act II]
   |          \
   |           +-- R5 the Halai Beach -- (HALAI) -- R6 the Halai Cliffs -- the cape (dead end)
   |
 R2 the Sacred Way: kilns, tombs, the hill spur, the Titans' rockslide
   |
 [HECATE'S HOLLOW]: the cave under the pass of Mount Aigaleos
   |
 R3 the Pine Slopes: Xerxes's seat, the niches of Aphrodite, a thyme meadow
   |
 (THRIA): a hamlet and inn at the edge of the Thriasian plain
   |
 R4 the Rheitoi: the salt streams, the jesters' bridge, the first wheat
   |
 [ELEUSA VILLAGE] -- the Ploutonion --> the Mystery sanctum, B1F-B3F
   |
 the Eleutherai road (vines: Demeter's Sickle) --> [THYRSA, Act II]
```

**Connections, map by map.** Sizes are in tiles; a GBA screen is 15×10.

| # | Map | Size | Joins |
|---|---|---|---|
| 1 | `MAP_TRIREME_EUPLOIA_DECK` | 24×16 | Akti's quay, Aegina's quay and Emporion's quay, all by scripted warps (beats 9–10C). After the first voyage Nausikles runs a three-port ferry (Part 2). |
| 2 | `MAP_AEGINA_TOWN` | 30×24 | The quay. North edge: the Aphaia Road (optional; shut on the voyage night). |
| 3 | `MAP_EMPORION_CITY` | 50×40 | The quay. West edge, the Sacred Gate: Route 2 (opens with the Herald Laurel, beat 16). East edge, the Coast Gate: Route 5. North edge, the Long Walls Gate: closed (Open questions 14). |
| 4 | `MAP_ROUTE2_SACRED_WAY` | 70×24, about 5 screens | East edge: Emporion. West end: the Hollow's east mouth (a warp). North side: the hill spur, a dead end. |
| 5 | `MAP_HECATES_HOLLOW` | 40×30 | East mouth: Route 2. West mouth: Route 3. |
| 6 | `MAP_ROUTE3_PINE_SLOPES` | 50×30, about 3.5 screens | East end: the Hollow (a warp). West edge: Thria. |
| 7 | `MAP_THRIA` | 30×24 | East edge: Route 3. West edge: Route 4. |
| 8 | `MAP_ROUTE4_RHEITOI` | 55×24, about 4 screens | East edge: Thria. West edge: Eleusa (Krokis's gate). |
| 9 | `MAP_ELEUSA_VILLAGE` | 50×40 | East edge: Route 4. North edge: the Eleutherai road (Act II; vines until beat 23). The Ploutonion: the Mystery sanctum B1F → B2F → B3F, a dead end. |
| 10 | `MAP_ROUTE5_HALAI_BEACH` | 50×20, about 3.5 screens | West edge: Emporion's Coast Gate. East edge: Halai. |
| 11 | `MAP_HALAI` | 24×20 | West edge: Route 5. East edge: Route 6. |
| 12 | `MAP_ROUTE6_HALAI_CLIFFS` | 40×30, about 3 screens | West edge: Halai. The cape at the east end is a dead end. |

**Real geography behind it.**
- Emporion is Piraeus. Ships from the Cyclades rounded Cape Sounion and worked up the Saronic Gulf, and Aegina sits in that gulf a day's sail out: a natural last stop.
- The Sacred Way is the Hiera Hodos. It ran from Athens to Eleusis over Mount Aigaleos at the pass now called Daphni, which is where Hecate's Hollow sits.
- Aigaleos's west slopes were pine-covered. Xerxes watched the battle of Salamis from them (Herodotus 8.90), and a sanctuary of Aphrodite with votive niches cut in the rock stood beside the road.
- Below, the deme of Thria gave the Thriasian plain its name. Then came the Rheitoi, two salt streams sacred to Demeter and the Kore, and Eleusis.
- The Halai Shore is the coast south-east of Piraeus, where the deme of Halai worked salt.
- Thyrsa lies north of Eleusa on the road to Eleutherai, the home of Dionysus Eleuthereus. Astyra (Athens) is up the Long Walls from Emporion, as Athens was from Piraeus.

## Pacing and levels

About 3 hours on a first run, the top of the 2–3 hour brief, because the road is longer. Optional content (the Halai Shore and Aegina's interior) adds about 45 minutes.

| Stretch | Time | Wild levels | Trainer levels | Boss |
|---|---|---|---|---|
| The voyage, with the night on Aegina | 20 min | — | 13–14 | Two scripted snatchers, 14–15 |
| Emporion | 25 min | — | — | — |
| Temple of Hermes | 18 min | — | 16–18 | Kerykos 18 / 19 / 21 |
| The Sacred Gate | 5 min | — | — | Kleon 19 / 20 / 22 |
| Route 2 | 12 min | 17–20 | 18–21 | — |
| Hecate's Hollow | 12 min | 19–21 | 20–21 | — |
| Route 3 | 12 min | 20–22 | 20–22 | — |
| Thria | 5 min | — | — | — |
| Route 4 | 12 min | 20–22 | 21–23 | — |
| Eleusa | 12 min | 21–23 | 22–23 | — |
| Temple of Demeter | 18 min | — | 23–24 | Chloe 24 / 25 / 25 / 27 |
| The night of the Mysteries and the sanctum | 20 min | 22–25 | 23–25 | Kleon beside you vs two Titanborn; Hyperion 25 / 25 / 26 |
| The revelation | 5 min | — | — | — |
| *Optional:* Routes 5–6 and Halai | 25 min | 14–17 | 15–17 | — |
| *Optional:* Aegina's interior | 20 min | 18–21 | 19–21 | — |

The curve runs Ione's ace 14 → Kerykos's 21 → Chloe's 27 → Hyperion's 26 (STORY.md targets him at about 22; Open questions 24). Emerald runs 15 → 19 → 24 → 29 over the same badges; Ichor sits a level or two higher because Phase 2 has more road between temples.

---

# Part 1. Scenes, beats 9–25

## Beat 9A. Elaia: Halia's second look

Per STORY.md §3, Act I item 1.

**Phase 2 build change.** The slice ends with the line "Thank you for playing the Kalliste preview of Pokémon Ichor." Drop it. `FLAG_ICHOR_SLICE_COMPLETE` stays.

**The pointer.** After the slice's last scene, Alethea waits on Akti's quay:
```text
ALETHEA: Halia sent a gull. She wants to see you before we sail.

ALETHEA: Truthfully, she wrote “NOW.” In very big letters.
```
**Setup.** In Elaia, a coord trigger two tiles from Halia's canopy runs with `FLAG_ICHOR_SLICE_COMPLETE` set and `FLAG_ICHOR_HALIA_SECOND_LOOK` unset. Halia sits alone under the canopy. The festival garlands are down.
```text
HALIA: There you are. Sit. No, closer.

HALIA: I said the light was poor, at the festival. It wasn't the light.
```
[She lights a small clay lamp and holds it low over the player's hand. Lamp SE. Hold 60 frames. The spindle in her other hand doesn't turn.]
```text
HALIA: …

HALIA: Forty years I've read threads under this tree.

HALIA: Forty years, and I've never once seen nothing.

HALIA: Don't look at me like that. I don't know what it means.

HALIA: That's what frightens me.

HALIA: I've sent a gull to Daphne. She'll know what to make of it.

HALIA: Or she'll pretend to. She's very good at pretending to.

HALIA: Go on. Your mother's gone down to the harbor. The wind's turning.

HALIA: I can smell it.
```
[Set `FLAG_ICHOR_HALIA_SECOND_LOOK`. Hide Mom at home (`FLAG_ICHOR_HIDE_MOM_HOME`) and show her on Akti's quay (`FLAG_ICHOR_HIDE_MOM_AKTI` cleared).]

**Design note.** Halia never says "no thread" (STORY.md's rule). "Nothing" is as far as she goes, and it reads two ways until Daphne explains it at Eleusa.

## Beat 9B. Akti: the winds turn, and Mom

Per STORY.md §3, Act I item 2.

**Setup.** The next time the player enters `MAP_AKTI_TOWN` with `FLAG_ICHOR_HALIA_SECOND_LOOK` set and `FLAG_ICHOR_WINDS_TURNED` unset, an `ON_FRAME` script runs. Mom stands on the quay with a covered basket. The slice's Kleon stays hidden (`FLAG_ICHOR_HIDE_KLEON_AKTI`); this scene uses a second Kleon object by the temple door, shown only while `FLAG_ICHOR_WINDS_TURNED` is unset.

[A gull cries. The ribbon on the trireme's mast lifts and snaps out. Wind SE.]
```text
NAUSIKLES: [offscreen] WIND! Wind from the south!

NAUSIKLES: [offscreen] Everyone aboard who's coming aboard!
```
[Alethea runs up from the quay and stops in front of the player.]
```text
ALETHEA: {PLAYER}! Did you hear? The kingfishers are done nesting!

ALETHEA: The halcyon days are over. We're sailing!
```
[Kleon runs out of the Temple of Hestia, waving something green. He skids to a stop beside Alethea.]
```text
KLEON: WAIT! Wait for me! Look at this!

KLEON: The Hearth Laurel. I beat her. Last night. By lamplight.

KLEON: Ione got up specially. In her nightdress. Then she fed me soup.

KLEON: I ate the soup. Out of respect.

ALETHEA: Congratulations, Kleon. Truthfully.

KLEON: So we're even. One laurel each. The race starts now!
```
[Kleon and Alethea walk up the gangplank and are hidden. Mom walks over from the quay's edge.]
```text
MOM: There you are. I brought bread. And honey. Not from that jar.

MOM: Don't look at me like that. I'm not crying. It's the wind.

MOM: I'm not coming across. I don't cross water. You know that.

MOM: …

MOM: Wherever you end up, come back up the hill. That's all.
```
[Give `ITEM_HONEY` ×2. Set `FLAG_ICHOR_MOM_HARBOR`.]
```text
{PLAYER} received 2 Honey!

MOM: Go on. That Lakonian boy's already halfway up the mast.
```
[Mom walks back to the quay's edge and stays there, facing the sea. Set `FLAG_ICHOR_WINDS_TURNED`. The player is free to finish up in Akti. Nausikles stands at the gangplank. Talking to Mom again: "MOM: Go. Before I change my mind for you."]

**Design note.** "Come back up the hill" is the line Mom means more than the player knows (STORY.md §2). It returns at Delphoi as "Come back up. Every time."
```text
NAUSIKLES: All aboard for Emporion? Once we're out, we don't turn back.
```
?? YES/NO
```text
> YES:
NAUSIKLES: Good. Mind the oars. They don't mind you.

> NO:
NAUSIKLES: Don't be long. Wind's like a cat. It leaves when it likes.
```
[YES: fade out, warp to `MAP_TRIREME_EUPLOIA_DECK`. Set `FLAG_ICHOR_BOARDED_EUPLOIA`.]

---

## Beat 10. The crossing

**The map.** `MAP_TRIREME_EUPLOIA_DECK` is the trireme's open deck with the sea on every side: the bronze ram at the bow (west), the mast and sail amidships, the steering oars and the captain's klepsydra at the stern (east). A hatch leads down to `MAP_TRIREME_EUPLOIA_HOLD`, three banks of rowers. The player can fish from the rail (Part 4). The deck's trainers and NPCs are in Part 2 and Part 3.

[Fade in. The *Euploia* under full sail. Play `MUS_ICHOR_TRIREME`.]
```text
NAUSIKLES: Cast off! Oars in, lads! Let the wind do the work.
```
[The player is free on deck. Kleon leans over the starboard rail. Alethea stands by the mast with a Poké Ball held in both hands.]

**Alethea's partner.** Talking to Alethea the first time plays this. Her first Pokémon is a Spalunk, the blind mole (dex #057), whose line ends in Plouteras, a member of her STORY.md team. The third krater stays with Daphne until the epilogue (STORY.md decision S9).
```text
ALETHEA: Look! My first partner. A Spalunk.

ALETHEA: It was asleep in the bottom of the dig pit on Kronion Hill.

ALETHEA: It followed me home. It's blind. It doesn't care. It just digs.

ALETHEA: Daphne said I needed a partner. So I dug one up. Literally.

KLEON: [at the rail] A mole? You picked a mole?

KLEON: Hrk.

ALETHEA: {PLAYER}, would you battle me? Gently?

ALETHEA: I've never done it with my own Pokémon. Only with books.
```
?? YES/NO
```text
> YES:
ALETHEA: Thank you! Wait. Was I supposed to bow? Never mind!

> NO:
ALETHEA: That's all right. Ask me later. I'll be standing here, being nervous.
```
[YES: `trainerbattle_no_intro` with `TRAINER_ICHOR_ALETHEA_DECK`. Set `FLAG_ICHOR_BATTLED_ALETHEA_DECK` afterwards either way.]

Defeat text:
```text
ALETHEA: I lost, but correctly! I did every step!
```
After:
```text
ALETHEA: I'm going to get better. Slowly. But I'll get there.
```

**The set piece.** It starts when the player talks to Nausikles at the stern. Before that he says: "Aegina by dark, Emporion tomorrow, if the wind holds. Winds always hold. Until they don't." Then ask:
```text
NAUSIKLES: Want to take the steering oar a moment? Just hold it straight.
```
?? YES/NO. NO: "Ha. Wise." and nothing else. YES:

[The player faces east, holding the oar. Hold 30 frames. The sail sags. The wind SE stops. The sea goes flat as glass.]
```text
The sail sags. The wind is gone. The sea goes flat in every direction.

NAUSIKLES: …No. Not out here. We're past the islands.

NAUSIKLES: One nest still out. Has to be. Aeolus won't blow while one's sitting.

NAUSIKLES: OARS! Pronomos, the stroke!
```
[An aulos plays a steady two-note stroke. Rowing SE. The ship creeps forward over the glassy water.]
```text
NAUSIKLES: Pull! We'll row her to Aegina if we have to!

ALETHEA: Is that… normal?

NAUSIKLES: Nothing's been normal since spring, girl. Pull!
```
[A loud squawk: a split reed. The aulos stops. The oars clatter out of time.]
```text
PRONOMOS: [from the hatch] My reed! It split clean through!

PRONOMOS: I can't keep the stroke!
```
[Kleon pushes himself off the rail and walks to the hatch. He's still green.]
```text
KLEON: …Lakonians march to the aulos.

KLEON: Rowing's just marching. Sitting down.

KLEON: LEFT! And LEFT! And LEFT, RIGHT, LEFT!
```
[The rowers pick it up. The oars find the beat. `MUS_ICHOR_TRIREME` switches to its march variant.]
```text
KLEON: FORWARD, SONS OF LAKONIA!

KLEON: AND EVERYONE ELSE'S SONS! AND DAUGHTERS! LEFT!

ALETHEA: He's actually good at this.

ALETHEA: Don't ever tell him I said so.

LOOKOUT: [from the bow] Something in the water! Dead ahead!
```
[The player walks to the bow; Alethea follows. A nest of woven seaweed and feathers drifts across the glassy water straight at the bronze ram. Two Harpeck circle above it, then dive.]
```text
A floating nest, woven from seaweed and feathers.

It's drifting straight at the ram. Above it, two snatchers are diving.

NAUSIKLES: We can't turn! We'll lose the stroke!

ALETHEA: Then we keep them off it! {PLAYER}, the bow!
```
[Set `FLAG_ICHOR_NO_WHITEOUT` and the no-running flag. Scripted wild battle with `SPECIES_HARPECK` at Lv 14. Then:]
```text
The other one's diving!
```
[Scripted wild battle with `SPECIES_HARPECK` at Lv 15. Clear both flags. If the player lost either battle, Alethea's Spalunk drives the bird off instead and the scene continues.]
```text
ALETHEA: There's a third! Spalunk, go! Dig! …There's no dirt. Bite it!
```
[The Spalunk scrambles up the rail; a hit SE; a squawk fades into the distance.]
```text
ALETHEA: I did it! I mean, it did it. I mostly shouted.
```
[The nest bumps against the ram's bronze beak and stops. A Galenyon drops out of the sky and lands on the ram, wings spread over the nest. One by one, the eggs crack. A tiny peep SE, three times.]
```text
The eggs are hatching. One, two, three.
```
[Hold 30 frames. Then the sail fills with a crack. Wind SE. Music back to the sailing theme.]
```text
NAUSIKLES: WIND! Ha! The last of them's hatched!

NAUSIKLES: That's halcyon days. Flat sea till the chicks are out.

NAUSIKLES: Then Aeolus lets go.
```
[The Galenyon lifts two chicks onto its back and flies. The third hops onto the rail, then onto the player's petasos.]
```text
A halcyon chick has hopped onto your hat. It doesn't look like leaving.
```
?? Take it with you? YES/NO
```text
> YES:
{PLAYER} received a Halcyling!

> NO:
The chick ruffles up, offended, and flies after its family.
```
[YES: `givemon SPECIES_HALCYLING, 12` with Water Gun, Wing Attack, Quick Attack and Mist, then the vanilla nickname prompt. Set `FLAG_ICHOR_GOT_HALCYLING`. NO: nothing; Halcyling is common on every coast. Set `FLAG_ICHOR_SAVED_HALCYON_NEST` either way.]
```text
KLEON: [hoarse, from the hatch] Left… and… left… Are we there yet?

NAUSIKLES: Not even close, lad. That calm cost us half a day.

NAUSIKLES: We'll put in at Aegina for the night. Emporion in the morning.

KLEON: Aegina's land, right? Solid land?

NAUSIKLES: Solid as Lakonia.

KLEON: …Bless Aegina.
```

**The night leg** (per STORY.md §3, Act I item 3). [Fade to black, then in on the deck with a scripted night tint (the DNS night palette, forced for this scene whatever the clock says). Stars. The sail full. Kleon at the rail, no longer green, holding a small wax tablet. The player is placed beside him.]
```text
KLEON: {PLAYER}. Can't sleep either?

KLEON: Letter from my mother. Came on the gull boat before we sailed.

KLEON: My mother writes every week. Two lines. Lakonian.

KLEON: [reading] “Eat. Don't be stupid.”

KLEON: That's a long one, for her.
```
[A creak. The water along the hull hisses and runs forward, toward the bow. The ship slides back a tile, then steadies.]
```text
NAUSIKLES: There it goes again. The tide, running the wrong way.

NAUSIKLES: Third night this month. Never seen it in forty years at sea.
```
[A long dark shape slides past to starboard: a trireme with no lamps lit, its oars muffled in leather. For a moment the moon shows a sickle painted on its furled sail. Then it's gone.]
```text
SAILOR: No lights. No flag. Nobody rows at night without lights…

SAILOR: …unless they're ashamed of something.

SAILOR: Strange times. My cousin's just back from Delphoi.

SAILOR: The Pythia only says “soon” now. To everyone. About everything.

KLEON: Soon what?

SAILOR: That's what everyone asks.
```
[Lights on the water ahead: a harbor.]
```text
NAUSIKLES: Aegina. Bed, the lot of you.
```
[Fade out. Warp to `MAP_AEGINA_TOWN`, the quay, for beat 10B.]

**Design note.** The calm was the halcyons, and the player ended it. The wrong-way tide is not, and nobody explains it: it is the cloth running out (STORY.md §1, rule 8). Kleon's mother's two-line letters are STORY.md's seed for Lakonia; they must read as nothing more than a Lakonian mother.

---

## Beat 10B. Aegina: a night ashore

**Setup.** `MAP_AEGINA_TOWN` is a small island harbor town around a round port: the inn, the mint where the island strikes its turtle coins, a few houses, ant hills in the dry grass at the edge of town, and on the headland of Kolona a single standing column from an old temple. The *Euploia* ties up for the night. The road inland, to the Temple of Aphaia, is closed by a gate for the night. Play `MUS_ICHOR_AKTI` (island harbors share a theme). Aegina's households are in Part 2; the player may visit them before or after the inn.

[The player, Alethea and Kleon step onto the quay. Kleon kneels and pats the stones.]
```text
KLEON: Solid. Look at it. Not moving at all. Beautiful.

ALETHEA: Aegina! The first coins in the world were struck here. Turtles.

ALETHEA: I'm going to the mint. Don't wait for me. Truthfully, do wait for me.

KLEON: The ants here turned into soldiers. A whole army out of an anthill.

KLEON: I'm going to look at them. Professionally.

NAUSIKLES: The inn's paid for. Sleep there. We sail at first light.
```
[Alethea and Kleon walk off and are hidden. The player is free in town. The gate to the Aphaia Road:]
```text
GATEKEEPER: The temple road's shut after dark. The goddess likes her privacy.

GATEKEEPER: She's very good at it. That's sort of her whole thing.
```
**The night at the inn.** Talking to Endeis, the innkeeper, asks: "ENDEIS: Ready for bed? Your friends are by the fire." ?? YES/NO. YES: fade; the common room at night, a fire in the hearth. Kleon sits with his back to the wall, eating bread like it owes him money. Alethea has a scroll open. The player sits.
```text
ALETHEA: The mint stamps every coin with a sea turtle. Nobody knows why.

ALETHEA: Truthfully, I think somebody just liked turtles.

KLEON: I went to the anthills. They're just ants.

ALETHEA: What did you expect?

KLEON: I don't know. A salute.
```
[Pause. Kleon puts the bread down.]
```text
KLEON: {PLAYER}. Can I ask you something?

KLEON: At the festival. What did Halia say about yours? Your thread.
```
?? Multichoice: SHE SAID NOTHING / IT'S MY OWN BUSINESS
```text
> SHE SAID NOTHING:
KLEON: Nothing? Lucky.

> IT'S MY OWN BUSINESS:
KLEON: Ha! That's what she told you, isn't it? I heard.

KLEON: I'd give anything for an oracle to say that to me.
```
```text
KLEON: Mine, they never stopped talking about. Young and glorious.

KLEON: My teachers know it. The other boys know it. The cook knows it.

KLEON: When I win, they say, “Glorious.”

KLEON: When I lose, they look at me like I'm already gone.

ALETHEA: …That's awful, Kleon.

KLEON: It's fine! It's a good prophecy. Glorious is the good part.

KLEON: I'm going to bed. Lakonians sleep sitting up. In case of attack.
```
[Kleon leaves for the loft.]
```text
ALETHEA: He doesn't sleep sitting up. He snores. I checked.

ALETHEA: Daphne says a prophecy is a story somebody told too early.

ALETHEA: I'd like to find out what the real story is. Before it happens to him.

ALETHEA: Goodnight, {PLAYER}.
```
[Fade to black. Heal the party. Set `FLAG_ICHOR_AEGINA_NIGHT`. Warp to the deck for beat 10C.]

**Design note.** Kleon asks the question the player can't answer yet, and the second choice lets the player quote Halia back at him. It lands differently after beat 25.

## Beat 10C. The last leg

[Fade in on `MAP_TRIREME_EUPLOIA_DECK` under full sail, the Saronic Gulf calm and blue. The scene is scripted; the player can't walk. A coastline rises in the east: long walls running inland, and a forest of masts.]
```text
NAUSIKLES: There she is. Emporion. Harbor of the whole wide world.

NAUSIKLES: Hold on to your purse. With both hands.

ALETHEA: That's the mainland. It's bigger than I thought. It just keeps going.

KLEON: [at the bow, not green at all] All of that. And somewhere in it, the next laurel.
```
[Fade. Set `FLAG_ICHOR_CROSSING_DONE`. Warp to `MAP_EMPORION_CITY`, the quay, for beat 11.]

---

## Beat 11. Emporion: the herald on the quay

**Setup.** This plays once on arrival, while `FLAG_ICHOR_ARRIVED_EMPORION` is unset. Set the fly flag `FLAG_ICHOR_VISITED_EMPORION` at the start. The quay is crowded: stevedores, a customs man, amphorae stacked like firewood. Play `MUS_ICHOR_EMPORION`.

[The player, Alethea and Kleon step off the gangplank. Kleon stops, breathes in, and grins.]
```text
KLEON: Land! Glorious, solid land!

KLEON: …Where's the temple? Up there? With the wings on it?

KLEON: BYE!
```
[Kleon sprints north and off-screen. Hide him: `FLAG_ICHOR_HIDE_KLEON_QUAY`. A man in a winged hat, holding a herald's staff wound with two snakes, climbs onto a bollard and raps the staff on it.]
```text
KERYKOS: Hear ye! Hear ye! The Euploia, out of Akti, three days late!

KERYKOS: Blame the kingfishers! Everyone does!

KERYKOS: Welcome, welcome to Emporion, harbor of the whole wide world!

KERYKOS: Everything that floats comes here. And most of what sinks.
```
[He hops down and walks straight to the player.]
```text
KERYKOS: You! New face. I collect faces. Names, too. Who are you?

{PLAYER} told him.

KERYKOS: {PLAYER} of Elaia! Ione's gull said you'd come.

KERYKOS: Her gulls tell me everything.

KERYKOS: I'm Kerykos. Herald of Hermes. Keeper of his temple. Talker.

KERYKOS: Mostly talker.

KERYKOS: First rule of Emporion. Say hello to Hermes. This is his town.
```
[He walks the player 3 tiles to the herm at the head of the quay: a square pillar with a bearded head, hung with garlands.]

**The rites tutorial** (per SYSTEMS.md §3). This is the first altar the player can use. It opens the shared altar menu.
```text
KERYKOS: This is a herm. A pillar with Hermes's face. Every road has one.

KERYKOS: Talk to any altar and you can pray. Prayer's free. Hermes likes free.

KERYKOS: Go on. Try.
```
[The altar menu opens: PRAY / MAKE AN OFFERING / FAVOR / LEAVE. Anything but PRAY gets "KERYKOS: Pray first. Shopping later." and the menu again.]
```text
You pray to Hermes.

Your purse feels lighter. Then heavier. Then exactly the same.

KERYKOS: See? He noticed you. Gods like being noticed.

KERYKOS: Offer something he likes, and he'll do more than notice.

KERYKOS: Honey, for Hermes. He's sweet like that.
```
**Herm waystones** (per SYSTEMS.md §4).
```text
KERYKOS: Now. Out on the roads you'll find great herms. Old, hung with garlands.

KERYKOS: Hermes remembers everyone who passes.

KERYKOS: Anoint his herms, and when you're lost, he'll point.

KERYKOS: Travelers swear he carries them back to any herm he remembers.

KERYKOS: Do I believe it? I'm a herald. I believe everything until it's proven.

KERYKOS: Then I sell it.

KERYKOS: Here. Three flasks of oil. The first ones are free.

KERYKOS: That's how they get you.
```
[Give `ITEM_OLIVE_OIL` ×3. Set `FLAG_ICHOR_RITES_TUTORIAL`. Hermes Favor +1 from the prayer.]
```text
{PLAYER} received 3 Olive Oil!

KERYKOS: Come up to the temple when you want a laurel. Ask for the herald.

KERYKOS: You'll find me. I'll be talking.
```
[Kerykos hurries north and off-screen.]
```text
ALETHEA: He talks the way Kleon runs.

ALETHEA: Here, before I forget. I brought two trowels. I always bring two.

ALETHEA: Truthfully, I bring three.
```
[Give `ITEM_ALETHEAS_TROWEL`. Set `FLAG_ICHOR_GOT_TROWEL`.]
```text
{PLAYER} received Alethea's Trowel!
```
**Excavation** (per SYSTEMS.md §5). A fixed dig spot sits in the planter beside the herm: turned earth with a glint of pottery.
```text
ALETHEA: See that planter? Turned earth and a glint. That's a dig spot.

ALETHEA: Kneel, scrape, and see what Aethos buried. Go on.
```
[The player digs: the field-move pose, a dust puff, one second. A fixed find.]
```text
{PLAYER} dug up a Potsherd!

ALETHEA: A sherd! Painted, too. Find the other pieces and we'll have a whole jar.

ALETHEA: Every old jar has a story on it. Daphne says the myths hide there.

ALETHEA: Now. The Titans came through here first. Someone sold them something.

ALETHEA: Merchants show samples at the Deigma. I'll start there.
```
[Alethea walks east to the Deigma and is hidden from the quay. Set `FLAG_ICHOR_ARRIVED_EMPORION`. The player is free.]

---

## Beat 12. The Deigma: forty lamps

**Setup.** The first time the player enters `MAP_EMPORION_CITY_DEIGMA` after beat 11. Alethea stands at a sample table with Lampis, a lamp-seller. She waves the player over.
```text
ALETHEA: {PLAYER}! Listen to this. Tell them what you told me.

LAMPIS: Bronze-helmet folk. Came through four days back.

LAMPIS: Bought twenty shovels, a mile of rope, and forty lamps.

LAMPIS: Forty! I've never sold forty lamps to one person. Not even a priest.

LAMPIS: A big man paid. In silver. Shouting the whole time. Friendly shouting.

LAMPIS: He's been hiring dockhands off the quay all month. Silver a day.

LAMPIS: Then they asked the road to Eleusa. I said the Sacred Way's shut.

LAMPIS: They said they'd go round. Over the goat paths.

ALETHEA: Shovels. Rope. Forty lamps.

ALETHEA: You don't take forty lamps to a field. You take them underground.

ALETHEA: “Where the grain goes underground.” Under Eleusa. The Mysteries.

ALETHEA: I was right. Daphne was right. Truthfully, I wish we weren't.

ALETHEA: The Sacred Way's the fast road, and only heralds may walk it now.
```
[Alethea walks to the wall by the door, where a public notice is pinned: a wax-sealed sheet. The player follows.]

**The hook, first sighting** (per STORY.md §3, Act I item 4). The notice is also an object anyone can read afterward.
```text
A public notice, sealed with the Archon's owl:

“By order of the Archon. The Sacred Way is closed to all but heralds…

…for the Mysteries' truce. Obey, and be safe.”

ALETHEA: Odd. There's a little hook under the owl.

ALETHEA: …Never mind. Probably a clerk's habit.

ALETHEA: So you need Kerykos's laurel. I'll write to Daphne.

ALETHEA: Kerykos's runners carry letters faster than any ship. Somehow.
```
[Alethea walks out. Hide her in Emporion: `FLAG_ICHOR_HIDE_ALETHEA_EMPORION`. Set `FLAG_ICHOR_DEIGMA_CLUE`. She reappears at the rockslide on Route 2 (beat 17).]

**Design note.** The hook gets one line and no explanation, as STORY.md requires. It is the first of the forger's signatures the player will learn to recognize (STORY.md §4).

---

## Beat 13. The Cold Forge: the Bronze Hammer

Per SYSTEMS.md §1, relic quest 2. It can be done any time in Emporion. The Hephaisteion is a small Doric temple on the hill above the Agora, as Hephaestus's stands above the Agora of Athens. Its forge, inside `MAP_EMPORION_CITY_HEPHAISTEION`, is cold. Kedalion sits on the anvil, glaring at it.
```text
KEDALION: Cold. Cold as a fish. Forty years this forge has burned.

KEDALION: Then the calm came, and it went out. Like someone blew on it.

KEDALION: I've tried pine. Olive. Charcoal from three islands. Nothing takes.

KEDALION: A forge isn't lit from any old fire, see.

KEDALION: Only from a hearth that's never gone out.

KEDALION: When the old colonists sailed, they carried fire from home. Always.
```
> **If the player has `ITEM_CHARCOAL`:**
```text
KEDALION: …What's that smell? Woodsmoke. And… soup?

KEDALION: That's hearth-coal. That's from Hestia's own hearth! At Akti!

KEDALION: Spare me a sliver? Just a sliver. You keep the rest.
```
?? YES/NO
```text
> YES:
The forge catches with a roar. Sparks climb the smoke.

KEDALION: HA! Listen to her! Like she never went out!

KEDALION: My master would be pleased. He never says so. He just hammers louder.

KEDALION: Here. This hung over the forge for luck. Now it's yours. For luck.

> NO:
KEDALION: Keep it, then. I'll sit here and be cold. Like a fish.
```
[YES: fire SE, flash, swap the forge metatile to lit. Give `ITEM_BRONZE_HAMMER`, set `FLAG_ICHOR_FORGE_RELIT` and `FLAG_ICHOR_GOT_BRONZE_HAMMER`, Hephaestus Favor +5. The item is not consumed.]
```text
{PLAYER} received the Bronze Hammer!

KEDALION: Rocks. Rubble. Broken marble. Hit it where it's tired. It comes apart.

KEDALION: I once carried a blind giant on my shoulders all the way to the sunrise.

KEDALION: After that, a bit of rubble's nothing.
```
> **If the player has no Charcoal:**
```text
KEDALION: Got any fire from a hearth that's never gone out? No?

KEDALION: Akti's never has. Euboulos at the temple there might spare a coal.
```
Euboulos gives a Charcoal in Akti if asked (Part 2, Return to Kalliste). Once the forge is lit, the Agora's general stall stocks Charcoal (SYSTEMS.md).

After the quest:
```text
KEDALION: Hear that? That's a happy forge. Votives for the gods, if you want one.
```
[Kedalion sells `ITEM_BRONZE_VOTIVE` from then on (Part 6).]

---

## Beat 14. Kleon on the temple steps

**Setup.** The first time the player steps onto the Temple of Hermes's stair with `FLAG_ICHOR_KLEON_WON_HERALD` unset, Kleon comes out of the door, a second laurel leaf tied beside the first.
```text
KLEON: {PLAYER}! Sixty-one steps! Remember that number!

KLEON: Kerykos says it's the fastest run in nine years.

KLEON: And I beat him. First try. First try! Look at it!

KLEON: First to the next laurel. That was the deal. I WIN!

KLEON: …I don't know what I win. I never said.

KLEON: I win the winning. That's plenty.

KLEON: I'll wait at the Sacred Gate. Being ahead of you. See you there!
```
[Kleon runs down the steps and west. Set `FLAG_ICHOR_KLEON_WON_HERALD`. Clear `FLAG_ICHOR_HIDE_KLEON_SACRED_GATE`.]

**Design note.** Kleon wins the race he set, by his own rules, and it doesn't satisfy him. That is the whole point of beat 16.

---

## Beat 15. The Temple of Hermes

The Herald's Run is in Part 5. Kerykos's lines are here; the acolytes are in Part 3.

**Entry.** Angelos, the temple guide, stands inside the door. This is the gym-guide re-skin.
```text
ANGELOS: Welcome, traveler. In the house of Hermes, every road's a short one.

ANGELOS: If you know where it goes.

ANGELOS: The herald's been waiting since dawn. And talking since dawn.
```
Hint, after a failed run:
```text
ANGELOS: Stuck? The herms only point the way once they're oiled. They're vain.

ANGELOS: Like the herald. Don't tell him I said so. He'll tell everyone.
```
After `FLAG_BADGE02_GET`:
```text
ANGELOS: Delivered, and on time! Hermes keep your roads short.
```

**Kerykos, before the run.** He stands just inside, by the oil jar.
```text
KERYKOS: You came! Everyone comes. I knew you'd come. I wrote it down.

KERYKOS: Welcome to the house of Hermes. Herald of the gods. Guide of roads.

KERYKOS: Friend of merchants, travelers, shepherds, liars and thieves.

KERYKOS: Mostly the last two. Don't tell the merchants.

KERYKOS: Kleon of Lakonia came through this morning. Sixty-one steps!

KERYKOS: Then he ran into a pillar. Then he beat me. In that order.

KERYKOS: Here's the rite. A herald carries the god's word.

KERYKOS: Fast, and to the right door.

KERYKOS: Three sealed scrolls. Three herald-herms, somewhere in my stoa.

KERYKOS: Deliver them in the order they're written. A herald always does.

KERYKOS: And this is the step-glass. It runs dry in a hundred and twenty steps.

KERYKOS: The herms in there are vain. Oil their faces and they'll point.

KERYKOS: There's oil by the door. Free. Don't tell the merchants that either.

KERYKOS: Ready?
```
?? YES/NO
```text
> YES:
KERYKOS: Then run, herald!

> NO:
KERYKOS: Nobody's ever ready. That's what makes it a race.

KERYKOS: Come back when you're less ready.
```
[YES starts the run (Part 5). Kerykos walks off through a side door; he reappears on the dais.]

**Kerykos on the dais,** once all three scrolls are delivered.
```text
KERYKOS: There you are! I took the short way. There's always a short way.

KERYKOS: Don't tell the acolytes. They think I fly.

KERYKOS: Every scroll at the right door, in the right order. Hermes is pleased.

KERYKOS: I can tell. He's gone quiet. He's never quiet.

KERYKOS: Now let's see if you're as quick when Pokémon do the running!
```
[Battle `TRAINER_ICHOR_KERYKOS_1`. Hierophant battle music. Defeat text:]
```text
KERYKOS: Delivered! Signed, sealed, and soundly beaten!
```
[After the battle:]
```text
KERYKOS: Well run, and well fought! Here. The Herald Laurel.
```
[Set `FLAG_BADGE02_GET`. Badge fanfare. Hermes Favor +15.]
```text
{PLAYER} received the Herald Laurel from Kerykos!

KERYKOS: And Aerial Ace. It never misses. A herald's word always arrives.
```
[Give TM Aerial Ace (vanilla `ITEM_TM40`; Balance keeps the number or reassigns it). Set `FLAG_ICHOR_GOT_TM_AERIAL_ACE`.]
```text
{PLAYER} received TM40, Aerial Ace!

KERYKOS: A secret. My family's been heralds at Eleusa for twenty generations.

KERYKOS: The Kerykes. We call the holy silence at the Mysteries. Every year.

KERYKOS: I ran off to sea. My cousin Chloe hasn't spoken to me since.

KERYKOS: That's not a feud. That's just Chloe. She doesn't speak to anyone much.

KERYKOS: The Sacred Way's shut for the Mysteries' truce. Only heralds walk it.

KERYKOS: That laurel says you're one of mine. Show it at the Sacred Gate.

KERYKOS: I'll be at Eleusa for the Mysteries. Someone has to shout “Silence!”

KERYKOS: It's the one night a year I'm paid to tell people to be quiet.

KERYKOS: I'm terrible at it.
```
After the laurel (repeat talk):
```text
KERYKOS: Herms on every road! Oil them all. Hermes remembers.

KERYKOS: So do I. I have a list.
```
**Gift I** (per SYSTEMS.md §3), the first time the player talks to him at Hermes Favor 30 or more:
```text
KERYKOS: Hermes is pleased with you. He asked me to give you this.

KERYKOS: Well. He didn't ask. He looked at me. Here.
```
[Give TM U-turn. Set `FLAG_ICHOR_GIFT_HERMES_I`.]

---

## Beat 16. The Sacred Gate: Kleon's second battle

**Setup.** The Sacred Gate is a stone gateway in Emporion's west wall, with a hoplite on each side. Before `FLAG_BADGE02_GET`, a coord trigger across the gate runs the hoplite's line and steps the player back:
```text
HOPLITE: The Sacred Way's shut for the Mysteries' truce. Heralds only.

HOPLITE: Got a herald's laurel? No? Then you're a tourist. Go buy a lamp.
```
With `FLAG_BADGE02_GET` set and `FLAG_ICHOR_KLEON_BATTLE_2_DONE` unset, the trigger plays this instead. Kleon leans on the gatepost, tossing a Poké Ball.
```text
KLEON: Took you long enough. How many steps?

KLEON: …Doesn't matter. I won the race. That was the deal.

KLEON: So why does it feel like I haven't won anything?

KLEON: It's you. It's because you're still standing there.

KLEON: No crowd this time. No festival. Just us. Battle me. Properly.
```
[Set `FLAG_ICHOR_NO_WHITEOUT`. `trainerbattle_no_intro` with the trainer chosen by `VAR_STARTER_MON`: 0 → `TRAINER_ICHOR_KLEON_2_KYNDER`, 1 → `TRAINER_ICHOR_KLEON_2_HIPLING`, 2 → `TRAINER_ICHOR_KLEON_2_NEBREL`. Afterwards clear the flag and branch on `GetBattleOutcome`.]

Defeat text:
```text
KLEON: No. No, no, no. I was ahead!
```
```text
> Player won (set FLAG_ICHOR_WON_KLEON_2):
KLEON: Again. I lost again.

KLEON: You know what the Oracle told my mother. Young and glorious.

KLEON: The young part's going great.

> Player lost:
KLEON: Ha! There. That's what winning's supposed to feel like.

KLEON: …It doesn't, though. Not quite.
```
```text
KLEON: The Mysteries are at Eleusa. When the procession gets there.

KLEON: They say initiates stop being afraid of dying.

KLEON: I'm not afraid of it. Lakonians aren't.

KLEON: I'd just like to hear someone say it isn't the end. Out loud. Once.

KLEON: Don't look at me like that. Lakonians don't get sad. We get faster.
```
[Kleon runs through the gate and off the map. Set `FLAG_ICHOR_KLEON_BATTLE_2_DONE` and `FLAG_ICHOR_HIDE_KLEON_SACRED_GATE`. The hoplites step aside.]
```text
HOPLITE: A herald's laurel. Pass, herald.

HOPLITE: Mind the road past the tombs. Titans brought half a hill down on it.

HOPLITE: Old Kedalion at the Hephaisteion has a hammer. If he's in a mood.
```

---

## Beat 17. Route 2: the rockslide and the procession

**Setup.** Near the west end of Route 2, at the foot of Mount Aigaleos, a marble tomb monument lies toppled across the road in three heaps of rubble. On the near side, the procession of initiates is camped: men and women in white with myrtle crowns and bundles of myrtle branches, and a pack donkey. Alethea sits on a milestone. A coord trigger 4 tiles east of the rubble plays this once.
```text
ALETHEA: {PLAYER}! The Titans brought the hill down. On purpose.

ALETHEA: Look at the stone. Shovel marks.

ALETHEA: The procession's stuck. So am I. Truthfully, I'm enjoying the sit.

EUDEMOS: Every year since there was a year, the procession walks to Eleusa.

EUDEMOS: This year, a mountain sat down in the road.
```
**The rubble** is three marble-rubble obstacles (per SYSTEMS.md §1, relic prompts). Without the Hammer:
```text
Marble rubble from a toppled tomb. A good hammer would break it.
```
With it, on ASK:
```text
Marble rubble from a toppled tomb.

Break it with the Bronze Hammer?
```
[YES: the relic pose, a crack SE, the rubble is hidden. The third heap leaves a scroll behind: TM Rock Tomb (vanilla `ITEM_TM39`), `FLAG_ICHOR_ITEM_ROUTE2_TM_ROCK_TOMB`.]

When the third heap breaks:
```text
The road is clear!

INITIATES: Iakch', o Iakche! Iakch', o Iakche!

EUDEMOS: The road is open! Herald, take these. Barley cakes, for the goddess.

EUDEMOS: She'll know who cleared her road.
```
[Give `ITEM_BARLEY_CAKE` ×2. Set `FLAG_ICHOR_ROCKSLIDE_CLEARED` and `FLAG_ICHOR_GOT_PROCESSION_BARLEY`.]
```text
{PLAYER} received 2 Barley Cakes!

ALETHEA: We'll follow at procession speed. Which is very slow. On purpose.

ALETHEA: The road goes under the mountain from here. Through Hecate's Hollow.

ALETHEA: The procession lights it with torches. You haven't got a torch.

ALETHEA: …You're going anyway. Of course you are. Go on, then.
```
[Alethea stays at the camp until the procession moves on. On the next map load, hide the camp: `FLAG_ICHOR_HIDE_PROCESSION_ROUTE2`.]

---

## Beat 18. Hecate's Hollow: the Three Roads

Per SYSTEMS.md §1, relic quest 3, and §2 (fire and light). The layout is in Part 5.

**The mouth.** An old woman sits by the cave's east mouth with a covered dish at her feet.
```text
OLD WOMAN: No light? Then you're braver than you look. Or sillier.

OLD WOMAN: Three roads meet in there. In the dark, every one looks right.

OLD WOMAN: Listen for the dog. Hecate's dogs always know the way.

OLD WOMAN: I leave her supper at the crossroads every new moon. She never eats it.

OLD WOMAN: Somebody does.
```

**The dark.** Past the first six tiles of daylight, the cave is dark: flash level 7, a tile and a half of light. At each of the three forks, a coord trigger plays a bark SE panned toward the right branch and shows one line:
```text
Somewhere ahead, a dog barks. The barking comes from your left.
```
(Right, and then ahead, at the next two forks.)

**The Hekataion.** The third fork opens into a round chamber lit faintly from above. A pillar of three women stands back to back, each face looking down one road, each hand holding a cold bronze torch. A barley cake sits on the pillar's ledge.
```text
A pillar with three faces, looking down three roads. An altar of Hecate.

A barley cake sits on the ledge, as if someone left it for you.
```
**The offering tutorial** (per SYSTEMS.md §3). The altar menu opens. MAKE AN OFFERING shows only offerings, with the ledge's cake added for this scene.
```text
Leave Hecate her supper at the crossroads?
```
?? YES/NO
```text
> YES:
You set the barley cake on the altar.

> NO:
The torches stay cold. Somewhere, very close, a dog sighs.
```
[YES: a single bark, very close. Silence. Then the left face's torch catches, then the right's, then the middle's. Swap the three torch metatiles to lit. Set the room to flash level 0. Hecate Favor +10 for the myth-quest and +5 for the loved offering (a Barley Cake); Hestia +1, as for any offering.]
```text
The middle face's torch comes loose in your hand. It's warm.
```
[Give `ITEM_HECATES_TORCH`. Set `FLAG_ICHOR_GOT_HECATES_TORCH`.]
```text
{PLAYER} received Hecate's Torch!

Something brushes past your legs. Something warm, with a cold nose.

Then it's gone.
```
[From here the torch gives flash level 3, three and a half tiles. Two unlit bronze braziers stand on the way out west. Lighting one makes its zone fully lit for good, per SYSTEMS.md §2:]
```text
A cold bronze brazier.

Light it with Hecate's Torch?
```
```text
The brazier catches. Its light reaches every corner of the passage.
```
**At night** (optional, per SYSTEMS.md): after 20:00 the Hekataion has three black hounds sitting at the pillar's feet. Two fade into the walls when the player approaches. The third stays: a static `SPECIES_LYKOPUP` at Lv 22, catchable. `FLAG_ICHOR_HECATES_HOUND`.

---

## Beat 19. The long road down: Routes 3 and 4, Thria, the saffron thread

The road from the Hollow to Eleusa is three maps: Route 3 down the pine slopes, the hamlet of Thria, and Route 4 across the salt streams. Their trainers and households are in Parts 2 and 3. Each map has its moment:
- **Route 3:** Xerxes's seat, a rock throne with the whole bay below (Part 2).
- **Thria:** the inn, and three sisters who won't cast pebbles for you (Part 2).
- **Route 4:** the jesters' bridge and Krokis's gate, written here.

**The Rheitoi bridge.** Two masked jesters stand on the bridge over the salt streams, one at each rail, so both see the player at once and it becomes a double battle (vanilla Emerald's two-trainer spotting). This is the *gephyrismos*: at the Rheitoi bridge, masked jokers insulted the Mysteries' procession as it passed. Their lines are in Part 3.

**Krokis's gate.** At Eleusa's east gate, a coord trigger plays this once. Krokis sits on a stool with a basket of saffron-yellow thread.
```text
KROKIS: Welcome to Eleusa, traveler. Hold out your right hand.

KROKIS: My family's tied the saffron thread on pilgrims for a thousand years.

KROKIS: Right wrist, and the Kore keeps you safe below. There.
```
[She ties it. A soft SE. Hold 30 frames. The thread slides off the player's wrist and drops into the dust.]
```text
KROKIS: …Hm. Bad knot. Again.
```
[She ties it. It slides off.]
```text
KROKIS: That's never… Once more.
```
[She ties it. It slides off. She looks at it for a long while.]
```text
KROKIS: Well! It must be the damp. It's been very damp this year.

KROKIS: Go on in.

KROKIS: Go on.
```
[Set `FLAG_ICHOR_SAFFRON_THREAD`.]

**Design note.** This is the act's one new thread clue, and like Halia's spindle it is never explained on the spot. Alethea mentions it once, in beat 25.

---

## Beat 20. Eleusa

**Arrival.** The first step into `MAP_ELEUSA_VILLAGE` sets `FLAG_ICHOR_ARRIVED_ELEUSA` and the fly flag `FLAG_ICHOR_VISITED_ELEUSA`. Play `MUS_ICHOR_ELEUSA`. No greeter: Eleusa is a quiet place, and Krokis has already greeted you. The village's layout and roster are in Part 2.

**Kleon in the square,** before the trial:
```text
KLEON: I'm getting initiated. Tonight, when the procession gets here.

KLEON: Not because I'm scared of anything. Because it's educational.

KLEON: Educational and nothing else.
```

---

## Beat 21. The Temple of Demeter

The Lesser Mysteries are in Part 5. The scene text is here; the acolytes are in Part 3.

**Entry.** Doso, an old woman, sits on the step inside the door.
```text
DOSO: Welcome, child. Mind your feet. It's dark in the goddess's house.

DOSO: It's meant to be. The Kore went down into the dark, and stayed a while.

DOSO: Her mother searched for her by torchlight. You've a torch, I see.

DOSO: Follow the Kore's trail. Put your light out to see it.

DOSO: Light it again to see the walls.

DOSO: At each step of her trail, give the goddess a fire.

DOSO: Somewhere in here is the Mystagogue. You won't see her. She'll see you.
```
Talk to Doso again:
```text
DOSO: My name? Doso.

DOSO: It's a very common name. Around here.
```
After `FLAG_BADGE03_GET`:
```text
DOSO: You found the Kore. Most people walk straight past her.
```

**Chloe.** When the fourth brazier is lit, the Anaktoron's doorway at the center of the hall is lit from all four corners. Someone has been standing in it the whole time.
```text
CHLOE: …

CHLOE: You followed her down. And you brought her back up.
```
[She holds up a single ear of wheat. A small bronze blade flicks; the stalk parts without a sound.]
```text
CHLOE: One ear of grain, cut in silence.

CHLOE: What's reaped grows again. That's the whole secret.

CHLOE: Don't tell anyone.

CHLOE: I'm Chloe. I lead the initiates down. And I lead them back up.

CHLOE: Show me you can find your way back.
```
[Battle. If `GetTimeOfDay` returns night, `TRAINER_ICHOR_CHLOE_1_NIGHT`; otherwise `TRAINER_ICHOR_CHLOE_1_DAY`. Hierophant battle music. Defeat text:]
```text
CHLOE: …Good.
```
[After the battle:]
```text
CHLOE: Down, and back up. That's the whole of it.

CHLOE: The Harvest Laurel.
```
[Set `FLAG_BADGE03_GET`. Badge fanfare. Demeter Favor +15.]
```text
{PLAYER} received the Harvest Laurel from Chloe!

CHLOE: And Giga Drain. What you take, you keep.
```
[Give TM Giga Drain (vanilla `ITEM_TM19`). Set `FLAG_ICHOR_GOT_TM_GIGA_DRAIN`.]
```text
{PLAYER} received TM19, Giga Drain!
```
**Demeter's rite** (per SYSTEMS.md §3: the Hierophant teaches the rite, with one free loved offering).
```text
CHLOE: Bring the goddess barley. Here's one.

CHLOE: Never a pomegranate.

CHLOE: Don't ask.
```
[Give `ITEM_BARLEY_CAKE` ×1. Set `FLAG_ICHOR_CHLOE_RITE`.]

Talk again:
```text
CHLOE: My cousin talks. I don't.

CHLOE: Between us we make one normal person.
```
**Gift I,** at Demeter Favor 30 or more: "CHLOE: The goddess is pleased. Here." TM Leech Seed. `FLAG_ICHOR_GIFT_DEMETER_I`.

---

## Beat 22. The night of the Mysteries

**The procession arrives.** On leaving the Telesterion with `FLAG_BADGE03_GET` set, set `FLAG_ICHOR_PROCESSION_ARRIVED`. The square fills: initiates in white, Eudemos, Alethea, and Kerykos with his staff on the sanctuary steps. Kleon is among the initiates.

```text
ALETHEA: We made it! Very slowly. Every step of the way. On purpose.

ALETHEA: I sent word to Daphne with one of Kerykos's runners. She's coming.

ALETHEA: She hates boats. She'll arrive cross.

KERYKOS: {PLAYER}! A laurel from my cousin! Did she say anything? Anything at all?

KERYKOS: …“Good.” Ha! That's practically a speech, for Chloe.

KERYKOS: The Mysteries open when the doors close. Heal up first.

KERYKOS: Once those doors shut, they don't open till it's done.
```
[Talking to Kerykos again asks: "KERYKOS: Ready? Doors are closing." ?? YES/NO. YES: fade, warp into the Telesterion for the scene. NO: "KERYKOS: Don't be long. I hate waiting quietly. I hate it loudly too."]

**Inside the Telesterion.** Since the Lesser Mysteries were finished, the hall's four braziers burn, but every other light is out. The initiates fill the stepped seats along the walls, a sea of white in the dark. Chloe stands at the Anaktoron's door with a covered basket. Kerykos stands on the top step. The player and Alethea are placed at the front; Kleon sits two places along. Play `MUS_ICHOR_MYSTERIES`, then let it fall to a single held note.

[Kerykos raps his staff three times.]
```text
KERYKOS: EUPHEMEITE!

KERYKOS: Keep holy silence! Silence, all of you!

KERYKOS: …That includes me. Starting now.
```
[Total silence. Hold 90 frames, no text. Chloe lifts the cover from the basket. Then a low rumble, felt more than heard. Shake the screen for 30 frames. Dust sifts down from the roof beams.]
```text
A rumble comes up through the floor. You feel it in your teeth.

ALETHEA: The ground's humming. Like Kronion Hill.
```
[A crack SE. The flagstones in the Anaktoron's doorway heave up, and two Titanborn climb out of the hole with lamps and shovels, into the middle of the hall. The initiates scream.]
```text
GRUNT: …This isn't the granary.

GRUNT: It's full of people. Why is it full of people?

GRUNT: The big man said it'd be empty! “Holy night, nobody about!”

CHLOE: It's the Mysteries. Everybody is about.

GRUNT: Right. Plan two. Everybody stay calm, and nobody follow us!
```
[They kick over the nearest braziers. Swap them to the overturned metatiles; their lit zones go dark. Kleon vaults down the tiers and lands beside the player.]
```text
KLEON: Titans? Finally! Something I can hit!

KLEON: {PLAYER}! You take the loud one. I'll take the other loud one.
```
**Kleon beside you** (per STORY.md §3, Act I item 5: the one double battle with Kleon, the bookend to the Stair of Hours). [Set `FLAG_ICHOR_NO_WHITEOUT`. A multi battle with `setmultitrainerbattle`: the player and Kleon as partner (`PARTNER_ICHOR_KLEON_ELEUSA_<KYNDER|HIPLING|NEBREL>`, chosen as in beat 16) against `TRAINER_ICHOR_GRUNT_TELESTERION_PSAMMIS` and `TRAINER_ICHOR_GRUNT_TELESTERION_CHERSOS`. Clear the flag afterwards. Either outcome continues; on a loss, Kleon's line is "Ha! We'll call that a draw."]
```text
KLEON: Ha! Did you see that? Side by side! Like the old songs!

KLEON: …Don't tell anyone I said that.

GRUNT: Fine! FINE! You can't follow us anyway. Down's dark!
```
[The grunts drop back into the hole. Another rumble, from far below.]
```text
CHLOE: Below us. The granaries.

KERYKOS: EVERYONE STAY CALM. I AM BEING CALM. LOOK HOW CALM I AM.

KLEON: The initiates. Someone has to keep them out of that hole.

KLEON: Lakonians are good at narrow places. Go on. I've got the door.

CHLOE: You. Bring that torch. Alethea, too.

CHLOE: There's a stair under the Anaktoron. No one goes down it.

CHLOE: Not even me, except once a year. Tonight I'll make an exception.
```
[Set `FLAG_ICHOR_MYSTERIES_NIGHT`, `FLAG_ICHOR_TELESTERION_MULTI` and `FLAG_ICHOR_SANCTUM_OPEN`. Chloe, Alethea and the player walk into the Anaktoron and down; warp to `MAP_ELEUSA_MYSTERY_SANCTUM_B1F`. Kleon stays at the Anaktoron's door until beat 24.]

---

## Beat 23. The Mystery sanctum

The dungeon's layout and rules are in Part 5. Three scenes are written here.

### 23A. B1F, the granaries

[Arrival at the foot of the stair. Dark: flash level 3 with the torch. Down the hall, far off, small lamps bob between the grain pits: Titanborn, each carrying one of Lampis's lamps.]
```text
CHLOE: The granaries. Every first fruit in Aethos ends up down here.

CHLOE: “Where the grain goes underground.”

ALETHEA: The tablet. It meant here. It meant this exact room.

CHLOE: I'll hold the stair. Nobody comes up it while I'm standing on it.

CHLOE: I've held worse. I've held a harvest.
```
[Chloe stays at the stair: she heals the party if spoken to ("CHLOE: Hold still."). A grunt walks out of the dark toward them, lamp swinging.]
```text
GRUNT: Oi! The priestess! Get her!

ALETHEA: Oh no you don't. Spalunk, go!

ALETHEA: {PLAYER}, I've got this one. Mostly. Go on!
```
[Alethea and the grunt are moved behind a pillar; battle SEs play offscreen. Hide them after the player leaves the screen. The two B1F grunts in Part 3 are ahead.]

### 23B. B2F, the Hall of the Kore

[A long frescoed hall, the four panels of the Kore's story (Part 5). Halfway down, a stone basin of spring water: the midpoint rest. Coord trigger at the hall's head: a big voice echoes up from the far stair.]
```text
VOICE: [from below] EASY! EASY. It's older than your grandmother!

VOICE: [from below] Lift with your knees! Who taught you to lift?
```
[The basin heals the party: "The water's cold and tastes of iron. You feel rested." Konis waits at the hall's far end; Gaios in an alcove (Part 3).]

### 23C. B3F, the deepest granary: Hyperion

Per STORY.md §2 and §3: Hyperion leads the theft, and this is the first admin battle. He is going blind, and the dark is what he fears; the seed is that he squints and complains about it. Nothing he says names his blindness.

**Setup.** A round vault, the oldest granary, its wall cracked open where the Titans' tunnel broke through from the fields. A great bronze chest stands open in the middle. Two Kapnub smolder on the floor like coals: the only light besides the player's torch. Petros and Amathos, the slice's grunts, are levering a curved black shard as long as an arm out of the chest with a sling of rope. Over them stands a huge bare-armed man with burn scars, a sun-disc breastplate, and a Corinthian helmet pushed back like a crown, squinting. A bronze harvest sickle lies in the dust beside the chest. Play the admins' shared theme with Hyperion's layer of forge hammers (`MUS_ICHOR_ENCOUNTER_ADMIN`).

The sickle can be examined before the scene triggers:
```text
A bronze sickle in the dust. Someone decided it wasn't worth taking.
```
[Coord trigger 5 tiles from the chest.]
```text
HYPERION: Easy! It's older than your grandmother, Petros.

PETROS: It's cold, boss. It's like holding a winter.

HYPERION: Then hold it fast and get it up the tunnel. Both of you. Go!

AMATHOS: Boss. Boss! That's the kid. From the hill!

HYPERION: What? Where? Somebody bring a lamp.
```
[Petros and Amathos haul the shard into the tunnel and are hidden. Set `FLAG_ICHOR_FRAGMENT_STOLEN`. Hyperion turns toward the torchlight, squinting hard.]
```text
HYPERION: Step into the light. I can't see a thing in here.

HYPERION: Who builds a temple with no windows? Underground! Who does that?

HYPERION: …Ha! You're tiny. You ran those two off a hill?

HYPERION: Petros is still sulking about it. He sulks loud.

HYPERION: I'm Hyperion. I run the crews. I feed the crews. Those two are mine.

HYPERION: Nobody chases my kids. Want to try me instead?
```
[Battle `TRAINER_ICHOR_HYPERION_1`, with `MUS_ICHOR_BATTLE_ADMIN`. A normal battle: a loss whites out to Eleusa's Asclepeion. On the way back down, the trigger sees `FLAG_ICHOR_FRAGMENT_STOLEN` already set, so Petros, Amathos and the shard stay hidden and Hyperion starts at "Step into the light." Defeat text:]
```text
HYPERION: HA! Good! Somebody show me who just beat me!
```
[After the battle:]
```text
HYPERION: You fight like you're not scared of the dark. Lucky you.

HYPERION: Doesn't matter. The piece is halfway up the tunnel by now.

HYPERION: Nothing personal, kid. One day there'll be no more dark. For anyone.

HYPERION: You'll thank us.
```
[He backs into the tunnel. His Pebblith thumps the roof; a deep rumble; shake the screen for 60 frames. The tunnel caves in behind him. Hide Hyperion: `FLAG_ICHOR_HIDE_HYPERION_SANCTUM`. Swap the tunnel metatiles to collapsed. Footsteps: Chloe comes down the stair from B2F, with Alethea behind her.]
```text
ALETHEA: {PLAYER}! Are you hurt? Is anyone hurt? Was that the ceiling?

CHLOE: …The chest's empty.
```
[Chloe walks to the chest, then stoops and picks up the bronze sickle from the dust.]
```text
CHLOE: They threw this aside. They thought it was nothing.

CHLOE: Two blades were kept down here.

CHLOE: One cut a father down. One taught the world to reap.

CHLOE: When the old sickle was broken, the goddess asked for a piece of it.

CHLOE: She buried it under her grain. Where nothing's ever cut but wheat.

CHLOE: They came for a sickle. They didn't know there were two.
```
[She holds it out.]
```text
CHLOE: Take hers. It cuts what's grown across a path. Nothing else.

CHLOE: That's all she ever wanted it to cut.
```
[Give `ITEM_DEMETERS_SICKLE`. Set `FLAG_ICHOR_GOT_DEMETERS_SICKLE`. Demeter Favor +10 for the myth-quest. Relic fanfare.]
```text
{PLAYER} received Demeter's Sickle!

CHLOE: Go up. I'll stay a while. Somebody should, down here.
```
[Fade. Warp to the Telesterion's steps, outside, for beat 24.]

---

## Beat 24. Kleon goes to Thyrsa

[Outside the Telesterion. The initiates are coming out in twos and threes, whispering. Kleon sits on the steps with his greaves off. Alethea comes out behind the player.]
```text
KLEON: You're back. They got it anyway, didn't they. I can tell from your face.

KLEON: An old man held my hand the whole time I was on the door. An initiate.

KLEON: Shaking. He said the Mysteries promise you come back. Like the grain.

KLEON: I said, “Back from where?” He just patted my hand.

KLEON: I didn't ask what he meant. I didn't want to know. That's a first.

ALETHEA: Kleon…

KLEON: I'm going to Thyrsa. The Dionysia. All of Aethos will be in that theater.

KLEON: Somebody should give them something worth watching.

KLEON: And you were good tonight. Side by side. Don't tell anyone.
```
[Kleon stands, looks north toward the vine-choked road, and grins.]
```text
KLEON: Vines on the road? Lakonians don't need roads.
```
[He runs to the north edge, vaults the vines (a scripted jump over the vine metatiles) and is gone. Set `FLAG_ICHOR_KLEON_LEFT_FOR_THYRSA`.]
```text
ALETHEA: He's going to break his neck.

ALETHEA: Truthfully, he'll probably be fine. That's the annoying part.
```
[Fade to black. Text: "Morning." The Telesterion is dark at every hour, so the scene inside doesn't depend on the clock.]

---

## Beat 25. The Telesterion, by one lamp: what you are

**The master text is STORY.md §7.1.** This is that scene, staged for the engine. Its words are §7.1's except where noted; it must deliver what STORY.md §3 lists: Daphne's first crossing in thirteen years; **what** you are, not **why**; her confession about the book; the tablet's back and the Titans' word for you; Alethea's held secret; the Star Chart.

**Setup** (STORY.md §6.2). The next time the player enters the Telesterion with `FLAG_ICHOR_KLEON_LEFT_FOR_THYRSA` set. The hall is as the theft left it: braziers kicked over (the overturned metatiles), Titan bootprints in the ash, the Anaktoron's floor broken open. The hall is dark (SYSTEMS.md §2) except one lit zone: a single clay lamp on the steps. Daphne sits beside it, a little green, in new sandals. Alethea stands below her. Play Chloe's Mysteries theme (`MUS_ICHOR_MYSTERIES`), then let it fall to one sustained aulos note under Daphne. The hall is dark at every hour, so nothing here depends on the clock.
```text
ALETHEA: She came on the morning boat. She was sick the whole way.

DAPHNE: Thirteen years on one island. The sea and I aren't friends.

DAPHNE: New sandals, too. They pinch. Don't look at them.

DAPHNE: {PLAYER}. Sit. The steps are cold, but they're honest.

DAPHNE: Halia wrote to me. After the Klotheia, and again when you sailed.

DAPHNE: She looked at your thread four times. Once by lamplight.

DAPHNE: She didn't see a short thread. Or a long one. Or a knotted one.

DAPHNE: She didn't see one at all.
```
[Hold 60 frames. The lamp flickers.]
```text
DAPHNE: Here's what I know. I'll try to say it plainly. I'm out of practice.

DAPHNE: Under Delphoi there's a Loom. Three old women work it.

DAPHNE: One spins every life. One measures it. One cuts it.

DAPHNE: Everyone in Aethos is a thread on it. Korinna. Philon. Kleon.

DAPHNE: Me. Halia. Kanthos the donkey, probably.

DAPHNE: Not you.
```
?? Multichoice: WHY? / HOW DO YOU KNOW?
```text
> WHY?:
DAPHNE: That part isn't mine to tell. It's your mother's.

> HOW DO YOU KNOW?:
DAPHNE: Someone I trust told me. Before you could walk.
```
```text
DAPHNE: When you see your mother, ask her. She'll tell you.

DAPHNE: She's waited thirteen years to. She hoped she'd never have to.

DAPHNE: Now the part that is mine.
```
[Daphne takes out the clay tablet from Kronion Hill.]
```text
DAPHNE: Alethea read you the front of this. The list of places.

DAPHNE: That list is mine. It's my book. Chapter by chapter.

ALETHEA: She wrote a book about the Harpe. Years ago. Before me.

DAPHNE: Where the sickle broke. Where the pieces fell. Where they'd be joined.

DAPHNE: I was wrong about Kalliste. Thank the gods. I was right about Eleusa.

DAPHNE: They're digging where I told them to dig.

DAPHNE: …And then there's the back.
```
[She tilts the tablet to the lamp. Show the tablet's back as a picture window, the way the expansion shows a Pokémon picture in a box: faint scratches stand up out of the clay in the raking light.]
```text
DAPHNE: Hold a lamp low and old scratches stand up. I taught Alethea that.

ALETHEA: I saw it on the hill. I wanted to tell you.

ALETHEA: Truthfully, I nearly did. Twice.

DAPHNE: I asked her to wait until I was sure. That was wrong of me.

DAPHNE: It says: “At the Klotheia, watch the threads.”

DAPHNE: “Bring word of the Unwoven.”

DAPHNE: Unwoven. That's their word for you.

DAPHNE: They weren't on Kalliste for the hill. They were there for you.
```
[Hold 60 frames.]
```text
DAPHNE: You could go home. Nobody would blame you. I'd row you myself.

DAPHNE: Badly. But I'd row.
```
?? Go home? YES/NO
```text
> YES:
DAPHNE: …No. You won't. You've got her chin.

DAPHNE: Still. It was worth asking.

> NO:
DAPHNE: No. I didn't think so.
```
```text
DAPHNE: Then take this.

DAPHNE: When people were sure of a story, they put it in the sky.
```
[Give `ITEM_STAR_CHART` with the item-get icon. Set `FLAG_ICHOR_GOT_STAR_CHART`. The chart screen is a SYSTEMS.md §8 stretch; until it exists, the item's description carries the line.]
```text
{PLAYER} received the Star Chart!

DAPHNE: You're not in the sky yet. Neither am I.

DAPHNE: I've been a tree on that island for thirteen years. Rooted.

DAPHNE: I think it's time I walked somewhere.

DAPHNE: Astyra. The Library. I'm going to try to unwrite a book.

ALETHEA: And I'm coming with you, {PLAYER}. Obviously. I brought two trowels.

ALETHEA: …Three.
```
[Daphne picks up the lamp and stands, wincing at the sandals. The one added line, for the runners' letter (Part 2):]
```text
DAPHNE: And write to your mother. Not about this. Tell her you're eating.
```
[Daphne walks out. Set `FLAG_ICHOR_DAPHNE_REVELATION` and `FLAG_ICHOR_ACT1_COMPLETE`; hide Daphne in Eleusa. Alethea now travels with the player: she waits by the vines on the Eleutherai road ("ALETHEA: Ready when you are. Truthfully, I've been ready since breakfast.") and is hidden once the player passes them. Restore the Telesterion's braziers on the next map load.]

[Fade to black. A title card in the pottery frame:]
```text
END OF ACT I

THE UNWOVEN
```
[For the Phase 2 playtest build only, then:]
```text
Thank you for playing Act I of Pokémon Ichor.
```
[Return to the overworld outside the Telesterion. The player can cut the vines on the Eleutherai road, catch, dig and return to Kalliste. In the Phase 2 build the road beyond the vines ends at a herald's barrier: "HERALD: Thyrsa's preparing the Dionysia. The road opens when the play's ready."]

**Design notes.**
- Daphne says what, never why (STORY.md §3). The why is Mom's, at Delphoi in Act III.
- The Titans' knowledge of the player comes from the tablet's back, as STORY.md has it, and from nothing Hyperion says. Nobody in Phase 2 names Iapetos.
- The one line added to §7.1 is "And write to your mother", which sets up the runners' letter and Mom's honey on the next visit home.

---

# Part 2. NPC rosters

Lines are listed by condition, earliest first; a later condition replaces earlier lines. Unnamed NPCs are fine as roles. Walker sprites are in Part 10.

## The trireme *Euploia* (`MAP_TRIREME_EUPLOIA_DECK`, `MAP_TRIREME_EUPLOIA_HOLD`)

| NPC | Where | Role |
|---|---|---|
| Captain Nausikles | stern, by the steering oars | captain; starts the set piece; the ferry |
| Kleon | starboard rail | rival, seasick |
| Alethea | by the mast | friend; optional practice battle |
| Pronomos | the hatch, then the hold | the ship's piper (*trieraules*) |
| Lookout | bow | — |
| Phormion, Lykon | deck | trainers (Part 3) |
| Lakonian rower | hold | from the slice |
| Rowers (3) | hold | flavor |

**Kleon at the rail**
```text
KLEON: I'm fine. Lakonians never get seasick.

KLEON: Lakonians fight on land. That's why. We've got loads of land.

KLEON: Don't look at the water. I'm not looking at the water.

KLEON: Hrk.
```
**Pronomos**
```text
PRONOMOS: I'm the piper. When the wind drops, I play, and they row to it.

PRONOMOS: A trireme's a hundred and seventy men trying to agree. The aulos helps.

> after the set piece:
PRONOMOS: A Lakonian kept the stroke with his voice. A whole crossing.

PRONOMOS: I'm a little in love with him. Professionally.
```
**The Lakonian rower** (hold)
```text
LAKONIAN ROWER: Wind.

LAKONIAN ROWER: …Yes.

LAKONIAN ROWER: That was a happy Lakonian weather report.
```
**Rowers**
```text
ROWER: Row, rest, row, rest. Then Emporion. Then row back. It's a good life.

ROWER: My oar's called Iris. Don't laugh. She's never let me down.

ROWER: Top bench gets the breeze. Bottom bench gets the top bench's feet.
```
**The captain's klepsydra** (an object at the stern)
```text
The captain's water clock. Water drips from the top bowl to the bottom one.

> during the set piece only, if checked:
The water in the captain's klepsydra is dripping upward.
```
**Nausikles as the ferry.** After `FLAG_ICHOR_CROSSING_DONE`, the *Euploia* runs a three-port loop: Akti, Aegina and Emporion. Talking to Nausikles at any of the three quays asks:
```text
NAUSIKLES: Where to? Wind's fair, more or less.
```
?? Multichoice of the other two ports, plus STAY. A choice warps the player to the deck, where they can walk and fish. Talking to him again on deck: "NAUSIKLES: Ready to make port?" YES fades to the chosen quay. On a ferry trip the set-piece flags are already set, so only the ambient NPCs are on deck. Emporion to Akti stops at Aegina only if the player picks it.

## Aegina Town (`MAP_AEGINA_TOWN`)

**Layout.** About 30×24. A round harbor with a stone mole, fishing boats and the *Euploia*'s berth; the inn on the waterfront; the mint behind it; old Aiakides's house up a lane; ant hills in the dry grass at the edge of town; and on the headland, **Kolona**, a single standing column of an old temple, the landmark you see from the sea. The gate to the Aphaia Road is at the north edge. **Identity:** turtles and ants. The island's coins carry a sea turtle, and its people say they were ants once.

The voyage night is beat 10B. The gate is shut that night and opens on any later visit (by ferry).

| NPC | Where | Role |
|---|---|---|
| Gatekeeper | the north gate | the Aphaia Road |
| Fisherwoman | the mole | flavor |
| Kid with an Ergant | by the ant hills | flavor |
| Endeis, Pheidon, Aiakides | their houses | households (below) |

**Kolona** (an object)
```text
A single column, all that's left of an old temple. The headland's named for it.

Sailors steer by it. It's been standing here longer than anyone's been counting.
```
**Gatekeeper**
```text
> the voyage night:
GATEKEEPER: The temple road's shut after dark. The goddess likes her privacy.

GATEKEEPER: She's very good at it. That's sort of her whole thing.

> later visits:
GATEKEEPER: The road to Aphaia's temple. Up through the pines. Mind the ants.
```
**Fisherwoman**
```text
FISHERWOMAN: Aegina's halfway to everywhere. Kalliste, Emporion, the Isthmus.

FISHERWOMAN: Everybody stops here. Nobody stays. Suits me.
```
**Kid with an Ergant**
```text
KID: My Ergant's called Myrmidon. Everyone's Ergant here is called Myrmidon.

KID: It's confusing at the ant races.
```

| House | Who | Event | Opens |
|---|---|---|---|
| The inn | Endeis, the innkeeper | the voyage night; rest and heal | the voyage |
| The mint | Pheidon, the moneyer | trade a Karkipool for his Chelonet | the voyage |
| Aiakides's house | an old soldier | show him an Ergant for a Black Belt | the voyage; the Ergant lives up the Aphaia Road |

### The inn (`MAP_AEGINA_TOWN_INN`)

- **Who:** Endeis, the innkeeper, who has seen every sailor in the gulf at least twice.
- **The room:** an island inn built around a little courtyard with a rain cistern in the middle, a wooden gallery of guest rooms above it, a turtle mosaic on the courtyard floor, and the common room's hearth, where beat 10B's scene plays.
- **Events:** the voyage night (beat 10B), then the rest point on later visits.
```text
ENDEIS: Off the Euploia? Nausikles always runs late. Kingfishers, was it?

ENDEIS: Sit. Bread and fish. The fish is fresh. The bread is honest.

> later visits:
ENDEIS: Back again? Everyone comes back to Aegina. They just don't stay.

[heal the party]
```

### The mint (`MAP_AEGINA_TOWN_MINT`)

- **Who:** Pheidon, the moneyer, who strikes the island's turtle coins. Legend credited a King Pheidon with the first coins, struck on Aegina.
- **The room:** a stone strongroom with two anvils, coin dies hung on a rack, a small brazier for heating the silver blanks, scales, and a heavy chest with a turtle stamped on its lid. A slot in the door lets coins out and nothing in.
- **Event:** an in-game trade. His Chelonet keeps sitting on the stamps. `FLAG_ICHOR_TRADED_CHELONET`.
```text
PHEIDON: Every coin gets a turtle. That's the rule. Don't ask me whose.

PHEIDON: Problem is, this one keeps sitting on the stamps. Thinks it's the model.

PHEIDON: I need a guard for the strongbox. Something with claws.

PHEIDON: You wouldn't trade me a Karkipool?
```
?? Trade a Karkipool for his Chelonet? YES/NO. YES: in-game trade, Chelonet nicknamed **STATER**, Lv 18, with its hidden ability (Punk Rock), holding an Oran Berry. It learns Sing at 24 and then evolves into Chelyra, the lyre tortoise, as the dex specifies.
```text
> YES, after the trade:
PHEIDON: Stater's a good name for it. It's worth about as much.

PHEIDON: It hums when it's happy. Hums. A tortoise. Don't ask.

> NO:
PHEIDON: Then it's back on the stamps for you, old friend.
```

### Aiakides's house (`MAP_AEGINA_TOWN_AIAKIDES_HOUSE`)

- **Who:** Aiakides, an old soldier, who says his family were ants before they were people.
- **The room:** a small house with a bronze shield and spear on the wall, a shrine with a clay ant on it, and, in a big pot in the corner, a living anthill he feeds crumbs to.
- **Event:** a "show me" request. Bring him an Ergant (they live up the Aphaia Road) and he gives you his Black Belt. `FLAG_ICHOR_GOT_BLACK_BELT`.
```text
AIAKIDES: There was a plague here once. Emptied the island. Every house.

AIAKIDES: The old king sat under an oak and watched a line of ants climb it.

AIAKIDES: He asked Zeus for as many people as there were ants. He woke up to an army.

AIAKIDES: We fought at Troy, you know. Well. My great-great-great-grandfather did.

AIAKIDES: Find me an ant that remembers. An Ergant, from up the temple road.

> with an Ergant in the party:
AIAKIDES: There. See how it stands? Shoulders back. That's a soldier.

AIAKIDES: Here. My old belt. I won't need it. The ants do the fighting now.

{PLAYER} received a Black Belt!

> after:
AIAKIDES: Feed them crumbs, and they'll follow you anywhere. Ants and soldiers both.
```

## Aegina's interior: an optional detour (proposal)

The user wants islands to be side content to explore. Aegina is the island on the voyage, so its interior is offered as an optional Act I detour, reachable by ferry any time after the voyage. It is a proposal: it costs three small maps.

**The chain:** Aegina Town → the Aphaia Road → the Temple of Aphaia, with a spur up Mount Oros.

| Map | Size | What's there |
|---|---|---|
| `MAP_AEGINA_APHAIA_ROAD` | 40×24, about 3 screens | Pistachio and pine hills, the ant hills where Ergant live (the Myrmidon myth), a forced band through scrub, the great herm (`FLAG_ICHOR_HERM_AEGINA`), three trainers, and a fork to Mount Oros. |
| `MAP_AEGINA_TEMPLE_OF_APHAIA` | 24×20 | A Doric temple on a pine-crowned hilltop, its pediments carved with heroes; a priestess; an altar of Artemis; a fixed dig spot. |
| `MAP_AEGINA_MOUNT_OROS` | 16×16 | The island's peak and the altar of Zeus, where King Aiakos prayed for rain and ended a drought for all of Greece (Pausanias 2.29.7). A view to the mainland. |

**Why go:**
- **The ants.** Ergant (and a rare Hoplomex) live here, on the island of the Myrmidons. Aiakides's Black Belt is waiting.
- **Two altars before their temples.** Artemis at Aphaia (her loved offering is any feather) and Zeus on Oros (Wine), long before the player reaches Arkadia or Olympus.
- **A Knossa seed.** Aphaia was Britomartis of Crete, who fled King Minos for nine months, leapt into the sea, and vanished on Aegina: "the one who isn't seen".
- **Trainers** at levels 19–21 between Kerykos and the Sacred Way, and a few items (Part 6).

**The priestess of Aphaia**
```text
PRIESTESS: This is Aphaia's house. The one who isn't seen.

PRIESTESS: She was a huntress from Knossa. A king chased her for nine months.

PRIESTESS: She jumped into the sea. Fishermen caught her in a net.

PRIESTESS: Then she walked up this hill, and simply wasn't there anymore.

PRIESTESS: If you ever go to Knossa, don't ask about their old king. Just run.
```
**Mount Oros's altar of Zeus**
```text
An altar of Zeus on the island's peak. A cloud is sitting on the summit.

From here you can see Emporion's masts, and the mountains behind them.

And far out to sea, if you squint and lie a little, Kalliste.
```
**The trainers** (Part 3 conventions: IVs 6, Check Bad Move)

| Trainer | Where | Team | Lines |
|---|---|---|---|
| HOPLITE Myrmex | the ant hills | Ergant 19, Ergant 20 | "MYRMEX: My family were ants. I'm proud of it. Ants can lift fifty times their weight." / Defeat: "MYRMEX: I can lift about one of me." |
| MERCHANT Sostratos | the road's fork | Onotis 20, Chelonet 20 | "SOSTRATOS: Richest trader on Aegina! Ask anyone. Ask my donkey." / Defeat: "SOSTRATOS: Still rich. Slightly less." |
| PILGRIM Euthymia | the temple steps | Galekit 20, Kerazap 21 | "EUTHYMIA: I came to see a goddess nobody can see. It's going very well." / Defeat: "EUTHYMIA: That I saw." |

Sostratos is the real Aeginetan merchant Herodotus called the richest trader of his day (Herodotus 4.152).

**Layout.** Emporion is a planned port city on a grid, as Piraeus was. Five districts, south to north:
1. **The harbor.** The quay where the *Euploia* moors, the long shipsheds where triremes winter, Glykera's fish stall, the harbor wall with the augur, the customs post, and the quay herm. The **Asclepeion** stands at the head of the quay, the first building you see.
2. **The Deigma**, the exchange hall, on the harbor's east side.
3. **The Agora**, the region's great market: a wide square of stalls under striped awnings, the long stoa on its west side, the moneychanger's table, a row of empty pithoi, Kydon's honey stall, Number Nine on its plinth, a herm at the crossroads, and the tavern. The general stall faces the main street, so a tired player finds it at once.
4. **The Hephaisteion**, on the hill above the Agora's west side.
5. **The Temple of Hermes**, Ionic with a winged frieze, at the top of the main street on a raised terrace, framed by the street from the quay. It is the crown.

**Houses.** Four households and the Titans' hiring hall, each with its own door and its own room (Emporion interiors, below): Philoxenos's house and the widow's house in the grid streets east of the Agora, the runners' house beside the Sacred Gate, Euphronios's workshop in the potters' lane under the Hephaisteion's hill, and the hiring hall among the warehouses by the shipsheds. No other house has a door, so no other house is drawn as a house: the rest of the grid is walls, courtyards, shrines and trees.

**Exits.** The Sacred Gate in the west wall (Route 2), the Coast Gate in the east wall (Route 5), the Long Walls Gate north of the temple (closed), and the quay (the trireme). **Identity:** the market. Everything is for sale, the snatchers steal from it, and even the jars bark.

| NPC | Where | Role |
|---|---|---|
| Kerykos | quay (beat 11), then the temple | herald; Hierophant |
| Halitherses | harbor wall | the augur: the daily omen |
| Glykera | fish stall | Daedalus's page I |
| Customs man | quay | flavor |
| Kydon | Agora, honey stall | Labyrinth seed |
| Number Nine | Agora, a roped wooden statue | Labyrinth seed |
| Sykeas | Agora, fig stall | the snatcher errand |
| Pasion | Agora, moneychanger's table | buys treasure |
| Man with a lamp | the stoa | flavor |
| Stallkeepers (3) | Agora | the markets |
| Sailor | shipsheds | dread |
| Dockhand | by the warehouses | the Titans' hiring (STORY.md §3) |
| Metic | by the Deigma | flavor |
| Kid with a Harpeck feather | Agora | flavor |
| Mother and son | shipsheds | flavor |
| Hoplites (2 + 2) | Sacred Gate, Long Walls Gate | gates |

**Halitherses, the augur** (per SYSTEMS.md §6). He sits on the harbor wall with his face turned up to the gulls.
```text
> first talk:
HALITHERSES: I read birds. They're more honest than oracles.

HALITHERSES: Birds never want anything from you but bread.

HALITHERSES: Come by once a day. I'll tell you what the sky says.

> each talk after:
HALITHERSES: The gulls came in low this morning. Here's what they said.

[the day's omen line]

> once the day's omen is told:
HALITHERSES: That's today's. The sky doesn't repeat itself. Come back tomorrow.
```
Act I omen lines, filtered by progress (SYSTEMS.md §6 holds the weights and the engine):

| Kind | Line | What happens |
|---|---|---|
| Swarm | "Goats on every hill along the Sacred Way. Sparks in their wool." | Route 2: Kerazap is half the encounters |
| Swarm | "Kingfishers, a whole cloud of them, over the Halai Shore." | Route 5: Galenyon swarm |
| Swarm | "The bees are restless in Eleusa's meadows." | Eleusa: Melibee swarm |
| Swarm | "Snatchers over the Agora. Hold onto your figs." | Route 6: Harpeck swarm |
| Swarm | "The fields at Eleusa are crawling with wheat. With serpents, I mean." | Eleusa: Stachyss swarm |
| Visitor | "A golden cub was seen in the scrub above the tombs." | Route 2 hill spur: a static Nemecub, Lv 20 |
| Visitor | "A great snatcher is hunting the Halai cliffs." | Route 6: a static Harpelle, Lv 22 |
| Visitor | "Someone saw a flower-crowned girl walking in the wheat. Then she wasn't there." | Eleusa fields: a static Korantha, Lv 24 |
| Visitor | "A jar in the Agora barked at a priest." | Emporion: one marked pithos holds a Pithound, Lv 20 |
| Weather | "Rain on the Halai Shore by noon. The snatchers love it." | Routes 5 and 6: rain |
| Weather | "A cloud is sitting on Mount Oros. Aegina will have rain." | Aegina's interior (the detour): rain |
| Swarm | "Goats on the pine slopes. The pitch-gatherers are furious." | Route 3: Kerazap swarm |
| Weather | "Hard sun over Eleusa. Good day to be wheat." | Eleusa: drought (harsh sun) |
| Good sign | "Today, threes are lucky." | Knucklebones: the 3-face counts as a 4 |

**Glykera** (Daedalus's page I, per LABYRINTH.md §1)
```text
GLYKERA: Sardines! Tuna! Eels from the lake, fat as priests!

GLYKERA: Phew. Hot one.
```
[She fans herself with an old sheet covered in drawings.]
```text
That fan's an old sheet covered in drawings. Doors. Wheels. A bird with a man's legs.
```
[If the player has an Olive Oil and `FLAG_ICHOR_DAEDALUS_PAGE_1` is unset:] ?? Trade her an Olive Oil for it? YES/NO
```text
> YES:
GLYKERA: For oil? Done! It's only some old scribble. Came up in a net.

{PLAYER} received Daedalus's page I!

> NO:
GLYKERA: Suit yourself. It's a good fan.

> after the trade:
GLYKERA: Sardines! Tuna! Oil, if you've got more of it.
```
[Set `FLAG_ICHOR_DAEDALUS_PAGE_1`. The page reads, from the bag: "THE THRESHOLD. / The first fire hides a door. Look behind it. / Tie off at the bronze ring under the bull. -D." Its meaning (Ring I's fresco door and hidden anchor) is LABYRINTH.md's.]

**Customs man**
```text
CUSTOMS MAN: Two in every hundred. Of everything that comes off a ship.

CUSTOMS MAN: Even you. …I'm joking. Mostly. Move along.
```
**Kydon** (LABYRINTH.md seed 3; his lines are LABYRINTH.md's). His awning is painted with a bull-leaper.
```text
KYDON: Knossan honey. The bees drink thyme and fear.

KYDON: Fear? There's a thing under the palace that bellows at the new moon.

KYDON: The bees don't mind. I mind.
```
[Kydon is a stall: after his lines, the mart UI sells `ITEM_HONEY`, Hermes's loved offering, at Ichor's 300.]

**Number Nine** (LABYRINTH.md seed 4). A wooden statue of a young man, mid-stride, roped to its plinth like a goat.
```text
A wooden statue, roped to its plinth like a goat.

The plaque says: BY DAEDALUS. DO NOT UNTIE.
```
?? Untie it? YES/NO
```text
> YES:
You untie the rope.

The statue looks down at you. Then it steps off the plinth and walks away.

Nobody in the Agora seems surprised.

> NO:
The statue strains very slightly against its rope.
```
[YES: it walks off the map; hide it with `FLAG_ICHOR_NUMBER_NINE_UNTIED`. The empty plinth then reads: "An empty plinth. A cut rope. The plaque says: BY DAEDALUS. DO NOT UNTIE."]

**Sykeas, the fig-seller** (the snatcher errand). A Harpeck object perches on his awning.
```text
> before:
SYKEAS: Figs! Best figs in Emporion! Fewer every minute!

SYKEAS: That snatcher's had six. Six! It looks at me while it eats them.

> talk to the Harpeck: static battle, SPECIES_HARPECK Lv 15. Win, lose or catch, it's gone.

> after:
SYKEAS: You got it! Here. Figs. Real ones. And it dropped this.
```
[Give `ITEM_FIGY_BERRY` ×3 and `ITEM_PRETTY_FEATHER` once; `FLAG_ICHOR_GOT_SYKEAS_FIGS`.]
```text
SYKEAS: My grandfather says “fig-shower” used to mean a snitch.

SYKEAS: He never says why. He just gets a look.
```
**Pasion, the moneychanger.** He sits at a table (*trapeza*) with a set of scales.
```text
PASION: Old coins? I buy old coins. Fair weight, fair price.

PASION: A Bronze Obol! The ferryman's fare, they say. Put one in the mouth of the dead.

PASION: I'll give you a good price for it. The ferryman won't.
```
[Pasion is a sell-only shop for the three coins at +20% over the general stall (Part 6).]

**The man with a lamp.** He walks slowly up and down the stoa holding a lit lamp at noon.
```text
MAN WITH A LAMP: I'm looking for an honest man.

MAN WITH A LAMP: You'll do for now. Don't let it go to your head.
```
**The empty jars.** Six pithoi stand in a row by the stoa. Checking one runs a 1-in-4 roll:
```text
An empty storage jar. It smells, faintly, of dog.

> on a hit (a wild battle, SPECIES_PITHOUND, Lv 16–18):
Something in the jar growls. A scruffy face looks up at you, deeply unimpressed.
```
**The Sacred Gate hoplites** are in beat 16. **The Long Walls Gate hoplites:**
```text
HOPLITE: The Long Walls Road. Astyra's at the far end.

HOPLITE: The Archon's council is sitting. Nobody goes up till it rises.

HOPLITE: Could be a week. Could be a year. Councils, you know.
```
**Dockhand** (Titans, public face 1, per STORY.md §3)
```text
DOCKHAND: Half the quay's gone digging. A big man came hiring.

DOCKHAND: Pays in silver and shouts. Shouts nice, mind. Like a big uncle.

DOCKHAND: Gives you a bronze hat and a shovel. Doesn't say what for.
```
**Sailor at the shipsheds** (dread)
```text
SAILOR: Ship in from Delphoi this morning. Same news as always.

SAILOR: The Pythia only says “soon” now. Pilgrims queue a week for one word.

SAILOR: Soon what, they ask. She just looks at them.
```
**Metic** (a resident foreigner)
```text
METIC: Thirty years I've lived here. I still pay the stranger's tax.

METIC: In Emporion everyone's a stranger. That's why it works.
```
**Kid with a feather**
```text
KID: A snatcher stole my bread, so I stole its feather.

KID: Now we're even. It doesn't think so.
```
**Mother and son at the shipsheds**
```text
MOTHER: He wants to row when he's grown. Bottom bench, he says.

SON: The bottom bench is where the strong ones go!

MOTHER: It's where the feet go. He'll learn.
```
**Stallkeepers.** Each is a mart; stock is in Part 6.
```text
GENERAL STALLKEEPER: Potions, balls, rope and repel! Everything a hero forgets!

OFFERINGS STALLKEEPER: Oil, barley, wine, frankincense. Whatever your god's fussy about.

SCROLL STALLKEEPER: Techniques, written down. Teach your Pokémon. Use it again and again.
```
**Signs**
```text
[City sign, at the quay]
EMPORION CITY
Harbor of the whole wide world.

[Temple of Hermes]
TEMPLE OF HERMES
Hierophant: Kerykos, the Herald. Every road's a short one.

[Asclepeion]
ASCLEPEION
Rest for Pokémon and the weary, by the grace of Asclepius.

[Agora]
THE AGORA
Fair weights. Fair measures. Fair warning: mind your figs.

[The Deigma]
THE DEIGMA
Merchants' samples shown within. Look, but don't lick.

[The tavern]
THE DOLPHIN
Wine, bread, knucklebones. No wagers. (Some wagers.)

[Hephaisteion]
HEPHAISTEION
The smith's temple. Kedalion keeps the forge.

[Sacred Gate]
THE SACRED GATE
West: the Sacred Way to Eleusa. Heralds only during the truce.

[Coast Gate]
THE COAST GATE
East: Route 5, the Halai Beach.

[Long Walls Gate]
THE LONG WALLS GATE
North: the Long Walls Road to Astyra.
```

## Emporion interiors

Per MAP_DESIGN §2, every door in Emporion opens, someone is home, and something happens inside; no two rooms share a layout. Emporion has four households and four public buildings. Each entry gives who is there, the room's character for the map team, the dialogue, the event and its flags.

| Building | Who | Event | Opens |
|---|---|---|---|
| Asclepeion | the healer, patients | healing, the Pithos | arrival |
| The Deigma | Lampis, Thaletas, merchants | beat 12; a Pokémon trade | arrival |
| The Hephaisteion | Kedalion, his apprentice | the Bronze Hammer; votives | arrival |
| The Dolphin | Myrtale and two regulars | knucklebones | arrival |
| Philoxenos's house | the xenia host | heal and rest; Wine for every new laurel | arrival, and each laurel |
| The runners' house | the day-runners | Quick Claw; a letter home | arrival; after Act I |
| The widow's house | Penelopeia, a sailor's widow | Sea Incense | arrival |
| Euphronios's workshop | a vase-painter | "Show me a Pokémon": three rewards | arrival, then Eleusa |
| The hiring hall | a Titan crew boss | an optional battle for a Rocky Helmet; empty after Act I | arrival |

### Asclepeion (`MAP_EMPORION_CITY_ASCLEPEION`)

- **The room:** a harbor Asclepeion, long and bright, with a wide **sea window** behind the counter so the healer works with the harbor at her back. Ship's rope for the bell-pull, small bronze anchors hung as thank-offerings, and the statue of Asclepius by the window. The Pithos stands at the back in a niche.
- **Service:** the slice's Ichor nurse strings. A **Panacoil**, the healer serpent of every Asclepeion (dex #076), coils around the counter post: "PANACOIL: Hss. [It looks you over, very professionally.]"

| NPC | Lines |
|---|---|
| Sailor with a sunburn | "Fell asleep on deck in the halcyon calm." / "Three days. I'm the color of a boiled octopus." |
| Old woman by the statue | "My grandson went to the Mysteries last year." / "He won't tell me a thing. He just smiles now. Infuriating." |
| Young healer | "We get a lot of snatcher bites. They bite the hand that holds the bread." |

### The Deigma (`MAP_EMPORION_CITY_DEIGMA`)

- **The room:** a long colonnaded exchange hall, open on the harbor side, with trestle tables of merchants' samples: amphorae of oil, bolts of dyed wool, a single bronze helmet, a stuffed fish. A scribe's desk by the door. Beat 12 plays here.

| NPC | Role |
|---|---|
| Lampis | lamp-seller; beat 12 |
| Thaletas | the trader (Narkeray) |
| Wool merchant | flavor |
| Grain merchant | foreshadowing |

**Lampis** (after beat 12)
```text
LAMPIS: Forty lamps. I keep thinking about it.

LAMPIS: You'd need a lot of dark to want forty lamps.
```
**Thaletas, the trader** (an in-game trade)
```text
THALETAS: I hooked this on the crossing. Flat as a plate. Numbs my hands.

THALETAS: I'd trade it for anything with legs. An Onotis, say. I like a donkey.
```
?? Trade an Onotis for his Narkeray? YES/NO. YES: in-game trade, Narkeray nicknamed **SOCRATES**, Lv 18, holding a Shell Bell. `FLAG_ICHOR_TRADED_NARKERAY`.
```text
> after the trade:
THALETAS: “Socrates.” A man in Astyra named it. It does what Socrates does.

THALETAS: Touch it, and you can't think straight for an hour.
```
**Wool merchant**
```text
WOOL MERCHANT: Purple from Tyre. Saffron from Eleusa. Red from my own shins.

WOOL MERCHANT: I don't recommend the last one.
```
**Grain merchant**
```text
GRAIN MERCHANT: Every city sends Eleusa its first fruits. A share of every harvest.

GRAIN MERCHANT: All of it goes underground. Into their granaries.

GRAIN MERCHANT: Nobody knows what they do with it. Eat it, I assume. Slowly.
```

### Hephaisteion (`MAP_EMPORION_CITY_HEPHAISTEION`)

- **The room:** a forge built into the temple's courtyard under a smoke-black roof: the great forge with its bellows, an anvil on an oak stump, racks of tongs and hammers, a quenching trough, and the empty hook over the forge where the Bronze Hammer hung. Small bronze votives line a shelf by the door.
- **Event:** the Bronze Hammer (beat 13), then Kedalion's votive stall. `FLAG_ICHOR_FORGE_RELIT`, `FLAG_ICHOR_GOT_BRONZE_HAMMER`.

One more NPC:
```text
APPRENTICE: The forge went out and Master sat on the anvil for a week.

APPRENTICE: He said if he got off it, the cold would win.
```

### The Dolphin, a tavern (`MAP_EMPORION_CITY_TAVERN`)

- **The room:** a low-beamed harbor tavern with a dolphin mosaic on the floor, racks of wine amphorae on the back wall, a long bench under the window over the quay, and the knucklebones table in the corner, its wood worn pale where the bones land.
- **Event:** knucklebones, per SYSTEMS.md §9: two regulars and a champion. The match rules and the AI personalities are SYSTEMS.md's.

| NPC | Personality | Prize for a first win |
|---|---|---|
| Strepsiades | Cautious | Olive Oil ×2 |
| Stratyllis | Bold | Wine |
| Myrtale (champion) | Bold, and good | TM Fling, and a line on the trainer card |

```text
STREPSIADES: I only rethrow the ones. That's my system.

STREPSIADES: My son says it's not a system. My son owes me money.

STRATYLLIS: Aphrodite or nothing, dear. Aphrodite or nothing.

STRATYLLIS: Mostly it's nothing. But oh, when it's Aphrodite.

MYRTALE: Forty years at sea. Thirty-nine at this table. Sit.

MYRTALE: Throw.

> after the player first beats her:
MYRTALE: Huh. Thirty-nine years.

MYRTALE: Here. Fling. It's how you throw a thing so it counts.

> after:
MYRTALE: Come back any time. I like losing to people who'll come back.
```
[`FLAG_ICHOR_KNUCKLEBONES_EMPORION` marks the champion's first loss.]

### Philoxenos's house (`MAP_EMPORION_CITY_PHILOXENOS_HOUSE`)

- **Who:** Philoxenos, a retired grain-shipper who keeps the old law of hospitality, and his cook.
- **The room:** an *andron*, a dining room with seven couches set around the walls and a low table in the middle, a mosaic floor of a host greeting a traveler at a door, a hearth, and a guest bed behind a striped curtain.
- **Event:** the xenia host (per SYSTEMS.md §10): heal and rest. And a story for every laurel: each time the player arrives holding a laurel he hasn't heard about, he trades a story for Wine.

The first two lines are SYSTEMS.md's.
```text
PHILOXENOS: Sit. Eat first.

PHILOXENOS: Then tell me who you are. Not before.

[heal the party, with the heal jingle]

PHILOXENOS: Bread, olives, a little cheese. Your Pokémon had the cheese.

PHILOXENOS: Stay, if you like. Rest till you want to wake.
```
[The rest menu (per SYSTEMS.md): DAWN / NOON / DUSK / NIGHT, each shown only if that hour is still ahead today, plus NOT NOW.]

**A story for a laurel.** With a laurel he hasn't heard about (the Herald Laurel, then the Harvest Laurel, and every later one):
```text
PHILOXENOS: A new leaf on your crown! Sit. Tell me everything.

[Fade. Hold 60 frames.]

PHILOXENOS: Ha! And then the herald ran into a pillar? Wonderful.

PHILOXENOS: Here. Wine, for Zeus of Strangers. He likes a story with his cup.
```
[Give `ITEM_WINE` ×1 (an offering, SYSTEMS.md §3). Flags `FLAG_ICHOR_PHILOXENOS_LAUREL_2`, `_3`, one per laurel.]

**The Split Coin** (a token chain, per SYSTEMS.md §10; a stretch feature). On the first visit:
```text
PHILOXENOS: Take half this coin. My guest-friend in Eleusa has the other half.

PHILOXENOS: Metaneira, of the house of Keleos. Show it to her. She'll know.
```
[Give the key item `ITEM_HALF_COIN`. `FLAG_ICHOR_SPLIT_COIN_1`.]

### The runners' house (`MAP_EMPORION_CITY_RUNNERS_HOUSE`)

- **Who:** Kerykos's day-runners, the heralds who carry messages on foot: the chief runner, Dromokleia, and two young runners.
- **The room:** a barracks. Rows of straw pallets, sandals hung in pairs on pegs, a big water jar with a ladle, a wall where someone has scratched a map of every road in Aethos with the distances in stades, and a finishing ribbon nailed over the door.
- **Events:** a Quick Claw on the first visit; after Act I, a letter home (Daphne's "Write to your mother"), which Mom answers with a gift on the next visit to Elaia.
```text
DROMOKLEIA: Message to carry? We run anywhere. Ships for the sea, us for the rest.

DROMOKLEIA: Take this. Every runner wears one. For a head start.
```
[Give `ITEM_QUICK_CLAW` once; `FLAG_ICHOR_GOT_QUICK_CLAW`.]
```text
> after beat 12:
DROMOKLEIA: Your scholar friend's letter is on its way to Kalliste.

DROMOKLEIA: The sea part's a ship. I don't like to talk about the sea part.

RUNNER: Sixty-one steps, the Lakonian did the Herald's Run in.

RUNNER: I did it in sixty-three. In my dreams. Every night.

> after FLAG_ICHOR_ACT1_COMPLETE, the first time:
DROMOKLEIA: A letter for Kalliste? For your mother? Write it. We'll run it.

DROMOKLEIA: What does it say? …“I'm eating.” That's all?

DROMOKLEIA: Mothers like short letters. It means you're busy, not dead.
```
[Set `FLAG_ICHOR_WROTE_TO_MOM`. On the next visit to the player's house, Mom gives `ITEM_HONEY` ×3 (Part 2, Return to Kalliste). Any of Kerykos's runners takes the letter: there is one in Eleusa's square after the procession, too.]

- **Who:** Penelopeia, a sailor's widow, who weaves for a living.
- **The room:** a narrow upstairs room over a rope-maker's yard: a big upright loom with a half-finished shroud on it, a window on the sea with a stool in front of it, her husband's oar hung on the wall, and a little shrine of Poseidon with a dried starfish.
- **Event:** a gift, Sea Incense, and a seed for the post-game Odyssey.
```text
PENELOPEIA: My husband sailed past the Sirens' rocks. With wax in his ears.

PENELOPEIA: They say he took it out to listen.

PENELOPEIA: He always did want to hear the end of a song.

PENELOPEIA: Here. He kept this for luck. Luck should go somewhere.

> after:
PENELOPEIA: I weave all day. Some nights I unpick it. Don't ask me why.

PENELOPEIA: It feels like waiting is a thing you have to keep doing.
```
[Give `ITEM_SEA_INCENSE` once; `FLAG_ICHOR_GOT_WIDOWS_GIFT`.]

### Euphronios's workshop (`MAP_EMPORION_CITY_POTTERS_WORKSHOP`)

- **Who:** Euphronios, a vase-painter, and his apprentice. The real Euphronios was a master of red-figure painting, and signed his pots "Euphronios painted me".
- **The room:** a workshop with a potter's wheel by the door, a domed kiln at the back with its chimney through the roof, long shelves of cups and jars drying, pots of black slip, and on every surface the words EUPHRONIOS PAINTED ME. A half-painted cup on the wheel shows a creature nobody has drawn yet.
- **Event:** "Show me a Pokémon." He paints from life. Show him the species he asks for (in the party) and he pays you, three times. The third is gated by progress: its species lives at Eleusa.
```text
EUPHRONIOS: People think I invent the creatures on my cups. I don't.

EUPHRONIOS: I just look. Very hard. For a very long time.

EUPHRONIOS: Bring me a {STR_VAR_1}.

[the step's line from the table below]
```
| Step | He asks for | Reward | Flag |
|---|---|---|---|
| 1 | Harpeck ("I've never got the wings right.") | Super Potion ×2 | `FLAG_ICHOR_EUPHRONIOS_1` |
| 2 | Chelonet ("The shell. I always paint it flat.") | Great Ball ×3 | `FLAG_ICHOR_EUPHRONIOS_2` |
| 3 | Stachyss ("A snake made of wheat, they say. From Eleusa.") | Star Piece | `FLAG_ICHOR_EUPHRONIOS_3` |

```text
> when shown the species:
EUPHRONIOS: Hold still. No, the Pokémon. You can fidget.

[Fade. Hold 60 frames.]

EUPHRONIOS: There. Look at that. It's never been on a cup before.

EUPHRONIOS: Take this. Every painter pays his models.

> after the third:
EUPHRONIOS: My teacher said every myth started on a cup.

EUPHRONIOS: Somebody saw something, and painted it. Then everyone argued about it.
```
(The third reward line echoes Daphne's thesis from the slice, without naming her.)

### The hiring hall (`MAP_EMPORION_CITY_HIRING_HALL`)

- **Who:** a Titan crew boss, signing on dockhands. STORY.md §5 puts the Titans' Emporion base in the warehouses: "the hiring hall, crates of shovels and helmets".
- **The room:** a long warehouse by the shipsheds, stacked with crates of shovels and bronze helmets, a trestle table with a ledger and a bag of silver, and a rope-and-pulley hoist. A sickle is chalked small on one crate, almost hidden.
- **Event:** an optional battle with the crew boss for a Rocky Helmet. After Act I the hall stands empty. `FLAG_ICHOR_HIRING_HALL`.
```text
CREW BOSS: Strong back? Silver a day. Bring a shovel. Or don't. We've got crates.

CREW BOSS: What's the work? Digging. Where? Somewhere. Who for? A big man.

CREW BOSS: He shouts, but he pays. Better than the quarry ever did.

CREW BOSS: Too small to dig? Then fight. Beat me, and you can have a hat.
```
[`trainerbattle_single` with `TRAINER_ICHOR_GRUNT_EMPORION_CREW_BOSS` (Part 3).]
```text
> after the battle:
CREW BOSS: Ha. Fair. Here, then. A Titan hat. Hurts anyone who hits you.

{PLAYER} received a Rocky Helmet!

CREW BOSS: May your thread never be cut. That's what we say. Say “Nor yours.”

> after FLAG_ICHOR_ACT1_COMPLETE:
The hall is empty. The crates are gone. Someone left the ledger open.

The last page says: “ELEUSA. FORTY LAMPS. ALL PAID.”
```
(The blessing and its answer are STORY.md §5's Titanborn rite.)

### Temple of Hermes (`MAP_EMPORION_CITY_TEMPLE_OF_HERMES`)

The room is Part 5's switchback stoa. Angelos, Kerykos and the three acolytes are in beat 15, Part 3 and Part 5. Objects:

| Object | Text |
|---|---|
| The oil jar by the door | "A jar of temple oil, for the herms." Then, if the player holds fewer than 3 Olive Oil: "You fill a flask." Give 1, up to 3. Otherwise: "Your flasks are full." |
| The temple altar | Hermes's great altar (per SYSTEMS.md §3: offerings count double here). |
| The step-glass | Before the run: "A tall step-glass. The sand falls one grain for every step you take." |
| Frieze | "A frieze of running figures. Every one has wings on his heels." |

## The Halai Shore (optional): Route 5, Halai, Route 6

Open from arrival. A coastal journey in three maps, south-east from Emporion's Coast Gate: a long beach, a salt hamlet, then sea cliffs out to a cape. It's the place to train and catch before Kerykos, and its gates pay off as the player gains relics.

### Route 5, the Halai Beach (`MAP_ROUTE5_HALAI_BEACH`)

**Layout.** About 50×20. Sand and dune grass along a curving bay, fishing boats drawn up on the shore, tide pools at the waterline, and low cliffs on the inland side. Two forced bands: dune grass across the beach path near the gate (2 deep, walled by the cliff and the boats), and a longer band before Halai. The great herm stands by the first boats. At the east end, where the cliffs come down to the sand, is the crack that the hoofprints lead to (below).

**Rhythm:** the gate and the herm, Asphalion in plain view, grass, the tide pools (hidden items), Krison running laps, grass, and Halai's roofs ahead.

**The great herm** of Route 5 (per SYSTEMS.md §4): `FLAG_ICHOR_HERM_ROUTE5`.

**The backward hoofprints** (the Hermes amphora's lead, per SYSTEMS.md §5: "Hermes steals the cattle"). Once that amphora is complete, hoofprint metatiles appear on the beach (clear `FLAG_ICHOR_HIDE_HOOFPRINTS`), leading the wrong way along the sand to a crack in the cliff that wasn't marked before: the Grotto of the Twelve (`MAP_ROUTE5_GROTTO_OF_THE_TWELVE`).
```text
Hoofprints in the sand. Dozens. They all point back the way they came.

Someone walked a whole herd here backward, so nobody could follow.
```
**The Grotto of the Twelve.** In the Homeric Hymn, the baby Hermes hid Apollo's stolen cattle in a cave, roasted two, and cut the meat into twelve portions: the first sacrifice to the Twelve. The grotto holds a low stone altar with twelve hollows worn into it.
```text
A stone altar with twelve hollows, worn smooth.

Twelve shares. One for every god at the table.

Pray here?
```
?? YES/NO. YES, once: "You pray to all of them at once. Somewhere, twelve people turn their heads." Every one of the Twelve gains +2 Favor; Hestia, who takes the first share, gains +1 more. `FLAG_ICHOR_TWELVE_ALTAR_PRAYED`. A visible item: TM Thief, for the god of thieves.

**Signs**
```text
[West end]
ROUTE 5 · THE HALAI BEACH
West: Emporion City. East: Halai.
```

### Halai (`MAP_HALAI`)

**Layout.** A salt hamlet of three whitewashed huts on a spit of sand, about 24×20. Square salt pans flooded with seawater, white heaps raked up beside them, drying racks of fish and octopus, a stone spring under a tamarisk tree (the rest point), and the road on east to the cliffs. **Identity:** white salt, and the slowest work in Aethos.

**The spring.**
```text
A cold spring in a stone basin, under a tamarisk. You and your Pokémon drink.

You feel rested.
```
[Heal the party.]

**Outdoors**
```text
SALT-WORKER: Let the sea in. Let the sun take the water. Rake up what's left.

SALT-WORKER: It's the slowest job in Aethos. I love it.
```

Three households, each with a door, an occupant and an event:

| House | Who | Event | Opens |
|---|---|---|---|
| Aigialeus's hut | an old fisher | the Good Rod | arrival |
| Halmyris's hut | the salt-worker's grandmother | swap salt and shells for a Shell Bell | arrival |
| Sagene's hut | a net-maker and her daughter | show her a Narkeray for a Big Pearl; the hoofprint lore | arrival; the hoofprints after the Hermes amphora |

#### Aigialeus's hut (`MAP_HALAI_FISHERS_HUT`)

- **Who:** Aigialeus, an old fisher who learned the trade beside Glaukos of Akti.
- **The room:** a boat on trestles fills half the hut. Nets hang from the rafters, a bed is squeezed into the corner, and rods of every length lean by the door.
- **Event:** a gift, the Good Rod. `FLAG_ICHOR_GOT_GOOD_ROD`.
```text
AIGIALEUS: You fish? With that? That's an old rod.

AIGIALEUS: Glaukos's, by the look of it. Out of Akti.

AIGIALEUS: He and I learned on the same rock. He got the sea. I got the shore.

AIGIALEUS: Here. A proper rod. Glaukos would want you to have it.

AIGIALEUS: He'd never say so.
```
[Give `ITEM_GOOD_ROD` once. If the player has no Old Rod, the first two lines become "AIGIALEUS: You fish? No? Everyone fishes eventually. Here."]
```text
{PLAYER} received a Good Rod!

> after:
AIGIALEUS: There's rays out past the point. Flat as plates.

AIGIALEUS: Don't grab one. I did once. My hand's still thinking about it.
```

#### Halmyris's hut (`MAP_HALAI_SALT_HUT`)

- **Who:** Halmyris, the salt-worker's grandmother, who strings shells by the fire.
- **The room:** a low hut lined with salt jars in rows, a curtain of strung shells over the inner door that clicks when you pass, a salt rake by the hearth, and a half-strung shell bell on her lap.
- **Event:** an item swap. Bring her two Shoal Salt and two Shoal Shell (hidden on Routes 4–6 and in Halai), and she strings you a Shell Bell. `FLAG_ICHOR_GOT_SHELL_BELL`.
```text
HALMYRIS: Salt from the pans. Shells from the sea. A bell from both.

HALMYRIS: Bring me two of each and I'll string you one.

HALMYRIS: It rings when your Pokémon hits something. Heals it a little.

HALMYRIS: Don't ask me how. I'm old, I'm not a priestess.

> with two Shoal Salt and two Shoal Shell:
HALMYRIS: There we are. Salt and shell. Listen.

[A soft chime SE.]

{PLAYER} received a Shell Bell!

> after:
HALMYRIS: My grandson rakes salt all day and calls it love. I call it a bad back.
```

#### Sagene's hut (`MAP_HALAI_NET_HUT`)

- **Who:** Sagene, a net-maker, and her daughter Galene.
- **The room:** a net stretched on a frame across the whole room, so you walk around it; baskets of cork floats; shuttles on hooks; and Galene's corner, a shelf of shells and one dried starfish she has named.
- **Events:** a "show me" request, and the hoofprint lore after the Hermes amphora. `FLAG_ICHOR_SHOWED_SAGENE_RAY`.
```text
SAGENE: Mending nets. Always mending nets. The sea eats them.

SAGENE: The fishers say a ray out past the point numbs a man through his net.

SAGENE: I'd love to see one. Just to know what I'm knotting against.

> with a Narkeray in the party:
SAGENE: Is that one? Flat as a plate! Let me…

SAGENE: …Ow. Ow! My whole arm's asleep. Wonderful. Take this.

{PLAYER} received a Big Pearl!

GALENE: We get snatchers. They steal salt. What does a bird want with salt?

> GALENE, after the Hermes amphora is complete:
GALENE: Somebody walked a herd of cows backward down our beach.

GALENE: You can see the hoofprints. They all go the wrong way.
```
(A Narkeray comes from the Good Rod off the cape, Kymon's team aside, or Thaletas's trade in Emporion.)

**Signs**
```text
[Hamlet]
HALAI
Salt, fish, and more salt.
```

### Route 6, the Halai Cliffs (`MAP_ROUTE6_HALAI_CLIFFS`)

**Layout.** About 40×30. The road climbs from Halai onto sea cliffs where snatchers nest, then runs out along a cape to a ruined watchtower and a shrine of Poseidon. A forced band on the cliff path, at its narrowest. The cliff-top pasture is optional grass behind marble rubble (the Bronze Hammer).

**Rhythm:** the climb; grass at the narrow cliff path and Kymon across it; the pasture (optional); the watchtower; Naubolos at the cape; the shrine, the herm, the dark cave mouth, and the islet offshore.

**Relic gates you can see:**
- Marble rubble across the cliff-top path (the Bronze Hammer, Act I): the pasture beyond has its densest grass and a visible Magnet.
- A dark sea-cave at the cape's tip (Hecate's Torch, Act I): the Salt Grotto.
- An islet with an item ball, across open water (Poseidon's Conch, Act II).

**The cape's shrine of Poseidon** is a Poseidon altar (per SYSTEMS.md §3). Sea gifts are his loved offering.

**The great herm** of Route 6 stands at the start of the cape (per SYSTEMS.md §4): `FLAG_ICHOR_HERM_ROUTE6`.

**The Salt Grotto** (`MAP_ROUTE6_SALT_GROTTO`). Dark; the Torch is needed. One small cave: a tide pool chamber with two braziers to light, Karkipool and Pebblith, a Big Pearl (visible), a Star Piece (hidden), and a fixed dig spot (a sherd for the Hermes amphora).
```text
[cave mouth, without the Torch]
A sea cave, pitch black inside. Water slaps somewhere in the dark.

You'd want a light.
```

**Signs**
```text
[West end]
ROUTE 6 · THE HALAI CLIFFS
West: Halai. East: the cape.

[Cape]
The cape. Poseidon's shrine. Mind the cliff. The cliff won't mind you.
```

## Route 2, the Sacred Way (`MAP_ROUTE2_SACRED_WAY`)

**Layout.** About 70×24 tiles, west from the Sacred Gate to the foot of Mount Aigaleos. The road is the old Sacred Way, paved, lined with tombs: grave stelai carved with family scenes, marble lekythoi on plinths, a walled family plot, a burial mound. Near the gate are the potters' kilns. Halfway, a hill spur climbs north into scrub. At the west end, the Titans' rockslide and the procession's camp, then the cave mouth of Hecate's Hollow.

**Rhythm:** the kilns and Exekias (first trainer, in plain view); a forced grass band among the tombs (3 deep, walled by grave plots); Myrrhine across the road; the great herm, desecrated, with its guard; the spur fork; a second forced band; Pheidippos at the narrow cutting; the procession's camp (rest point: a healer); the rockslide; the cave.

**Ledges.** The road climbs toward the pass, so the terraces beside it have ledges that drop back east toward Emporion: a quick way home, and a loop past the walled grave plot.

**The hill spur** (optional): goat paths through scrub, optional grass, Menalkas, a visible Super Potion, and at the top a thorn thicket (Demeter's Sickle, end of Act I) closing off a laurel grove with a shrine of Apollo. Beyond the thicket: a laurel tree that gives one Laurel Sprig a day (per SYSTEMS.md §3), a visible Sun Stone, and Apollo's altar.

**Other relic gates you can see:** a column drum (the Girdle of Herakles, Act II) blocking the gate of a walled family tomb, with a visible item inside and a fixed dig spot.

| NPC | Where | Role |
|---|---|---|
| Kiln worker | the kilns | flavor |
| Mourner | at a grave stele | lore |
| Eudemos | procession camp | the procession's leader (beat 17) |
| Procession healer | camp | rest point |
| Initiates (3) | camp | flavor |
| Alethea | camp (beat 17) | — |
| Exekias, Myrrhine, Menalkas, Pheidippos, Kapelos, the herm's guard | along the road | trainers (Part 3) |

**Kiln worker**
```text
KILN WORKER: Clay from the river. Fire from the kiln. Black from the smoke.

KILN WORKER: We close the vents at the end, see. Starve the fire. That's what makes the black.
```
**Mourner** (by a stele of a seated woman holding a baby's hand)
```text
MOURNER: My grandmother's stone. See her? Holding my mother's hand.

MOURNER: The carver gave them the same face. He said families look alike, in the end.
```
**Procession healer** (until the rockslide clears)
```text
HEALER: A doctor walks with every procession. Hold still.

[heal the party]

HEALER: There. Walk slowly. We all do, this week.
```
**Initiates at the camp**
```text
INITIATE: I've waited my whole life to see the Mysteries.

INITIATE: I can wait a bit longer. Behind a rock. In the sun.

INITIATE: We carry myrtle and walk all the way. You're not supposed to ride.

INITIATE: The donkey rides. Well. The donkey carries. The donkey has it easy.

INITIATE: Afterward, you're not allowed to tell anyone what you saw.

INITIATE: I've already practiced not telling. I'm very good at it.
```
**The great herm,** desecrated (per SYSTEMS.md §3, desecrated altars, and §4). A sickle is scratched deep into Hermes's face. The Titanborn guard stands beside it (Part 3). Before the guard is beaten:
```text
A great herm, hung with old garlands. Someone has scratched a sickle into its face.
```
After the guard, the altar menu offers PRAY; the first prayer cleanses it (+3 Hermes Favor, `FLAG_ICHOR_ALTAR_CLEANSED_ROUTE2`):
```text
You pray to Hermes. The scratches seem shallower. Then they're gone.
```
Then it can be anointed (`FLAG_ICHOR_HERM_ROUTE2`).

**Signs**
```text
[East end]
ROUTE 2 · THE SACRED WAY
East: Emporion City. West: Mount Aigaleos and Eleusa.

[Spur fork]
North: the hill paths. West: the Sacred Way.

[By the tombs]
Walk softly. Everyone here was somebody's.

[West end]
HECATE'S HOLLOW. The road goes under the mountain.
```

## Hecate's Hollow (`MAP_HECATES_HOLLOW`)

The old woman at the mouth is in beat 18. Hekabe and Kallias, the two trainers past the Hekataion, are in Part 3. The layout is in Part 5.

**The web chamber** (the Arachne amphora's lead, per SYSTEMS.md §5). A side passage off the western half is curtained with cobwebs. Burn them with the Torch (per SYSTEMS.md §2: "Webs burn"):
```text
A thick curtain of cobweb, strung across the passage.

Burn it with Hecate's Torch?
```
Inside: a visible Silk Scarf. After the Arachne amphora is complete, a static `SPECIES_RAKNIT` with its hidden ability (Defiant) hangs from the ceiling at Lv 22: `FLAG_ICHOR_HOLLOW_RAKNIT`.

**Signs**
```text
[East mouth]
HECATE'S HOLLOW
Three roads meet beneath the mountain. Hecate keeps them all.

[West mouth]
West: Route 3, the Pine Slopes, and Thria.
```

## Route 3, the Pine Slopes (`MAP_ROUTE3_PINE_SLOPES`)

**Layout.** About 50×30. From the Hollow's west mouth the Sacred Way switchbacks down Mount Aigaleos's western flank through Aleppo pines, with the bay of Salamis glittering below on the left. On a rocky shoulder is **Xerxes's seat**, a rough throne cut in the rock. Halfway down, a rock face beside the road is cut with dozens of small niches: the **niches of Aphrodite**, a roadside shrine. A side path climbs to a **thyme meadow** with beehives. The great herm stands at the foot of the slope, where the road levels out toward Thria.

**Rhythm:** the Hollow's mouth and the first view (calm stretch); a forced band in a pine clearing (3 deep, walled by a rock fall and the drop); Kynegeiros at the narrow ledge below Xerxes's seat; the seat; a second forced band on the switchback; the niches and Myrto; the meadow (optional); the herm; Thria's roofs ahead.

**Ledges.** None on the main road: it descends toward the next town, and MAP_DESIGN §1 wants ledges to drop toward the previous one. Route 2's climb has them instead.

**Relic gates you can see:** a column drum (the Girdle of Herakles, Act II) across the path to a ruined watchtower, with a visible PP Up beyond; and a thorn thicket (Demeter's Sickle, end of Act I) closing a pine hollow with a visible Calcium.

| NPC | Where | Role |
|---|---|---|
| Pitch-gatherer | among the pines | flavor |
| Trygaios's piglet | the thyme meadow | Thria's errand (below) |
| Kynegeiros, Myrto, Aristaios | along the route | trainers (Part 3) |

**Xerxes's seat** (an object, and the route's set piece)
```text
A rough seat cut into the rock, looking out over the bay.

A king once sat here to watch his ships win a battle.

They didn't.
```
(Herodotus 8.90: Xerxes watched the battle of Salamis from Aigaleos. A hubris echo, unexplained.)

**The niches of Aphrodite** are an altar of Aphrodite (per SYSTEMS.md §3; Frankincense is her loved offering).
```text
A rock face cut with dozens of little niches.

Each holds a clay dove, or a lamp, or a name scratched small.
```
**Pitch-gatherer**
```text
PITCH-GATHERER: Pine resin. We seal the wine jars with it.

PITCH-GATHERER: Makes the wine taste of trees. People pay extra for that.

PITCH-GATHERER: People are strange.
```
**The great herm:** `FLAG_ICHOR_HERM_ROUTE3`.

**Signs**
```text
[East end]
ROUTE 3 · THE PINE SLOPES
East: Hecate's Hollow. West: Thria.

[Meadow path]
Thyme meadow. Bees at work. Walk softly, or be stung loudly.
```

## Thria (`MAP_THRIA`)

**Layout.** A roadside hamlet at the edge of the Thriasian plain, about 30×24: the Sacred Way runs straight through it between three buildings. The **Inn of the Plain**, with a donkey yard, on the north side of the road; the sisters' round house and Trygaios's farmhouse on the south; a well, a threshing floor and a peddler's cart in the middle. West, the plain opens out flat and gold. **Identity:** the last bed before Eleusa, and the first one after.

The real deme of Thria gave the plain its name. In myth the Thriai were three sisters who told the future with pebbles, and taught it to Apollo.

**The peddler** (an Agora stall on a cart, Thria's local look)
```text
PEDDLER: Potions, repels, barley for the goddess. Everything a pilgrim forgets.
```
[Mart: Potion, Super Potion, Antidote, Repel, Olive Oil, Barley Cake.]

| House | Who | Event | Opens |
|---|---|---|---|
| The Inn of the Plain | Xenokles, the innkeeper | rest and heal; trade an Onotis for his Gelasable | arrival |
| The sisters' house | three old sisters | trade Honey for an Everstone | arrival; a new line after beat 25 |
| Trygaios's farmhouse | a farmer | find his lost sow on Route 3 for Leftovers | arrival |

### The Inn of the Plain (`MAP_THRIA_INN`)

- **Who:** Xenokles, the innkeeper, and a stable boy.
- **The room:** a long, low common room with a hearth halfway down, benches and trestle tables, sleeping lofts up a ladder, wine jars in a row, and a stable door standing open on the donkey yard, where an Onotis eats hay.
- **Events:** the rest point (heal), and an in-game trade. `FLAG_ICHOR_TRADED_GELASABLE`.
```text
XENOKLES: The Inn of the Plain. Last bed before Eleusa. First bed after.

XENOKLES: Heralds sleep free this week. The Mysteries. Sit down, sit down.

[heal the party]

XENOKLES: My weasel keeps stealing the guests' sandals. Left foot only. Every one.

XENOKLES: What I need is a donkey for the stable. You wouldn't have an Onotis?
```
?? Trade an Onotis for his Gelasable? YES/NO. YES: in-game trade, Gelasable nicknamed **GALANTHIS**, Lv 21, with its hidden ability (Prankster), holding a Leppa Berry.
```text
> YES, after the trade:
XENOKLES: Galanthis, I called her. After the girl who laughed at a goddess.

XENOKLES: She laughs at me all day. You'll get on.

> NO:
XENOKLES: Fair enough. I'll just keep buying sandals.

STABLE BOY: A Lakonian came through two days ago. Ran into the doorpost.

STABLE BOY: Then he ran into the other doorpost. Then he slept in the hay.
```

### The sisters' house (`MAP_THRIA_SISTERS_HOUSE`)

- **Who:** three old sisters who cast pebbles to tell the future.
- **The room:** a round house with three stools around three clay bowls of white pebbles, honeycombs on a high shelf, bundles of laurel drying from the beams, and loom-weights strung up as a wind chime by the door.
- **Event:** an item swap: Honey for an Everstone, a pebble that "only ever says one thing". `FLAG_ICHOR_THRIAI_PEBBLE`.
```text
ELDEST SISTER: We cast pebbles. Three sisters, three bowls. We tell what's coming.

MIDDLE SISTER: Not for you, dear. We cast for a Lakonian boy, two days ago.

YOUNGEST SISTER: He asked if it would hurt. We said no.

YOUNGEST SISTER: It was the kindest pebble.

ELDEST SISTER: That was enough casting for one week.

MIDDLE SISTER: We'd take a little honey, though. We were bees, once. Long story.
```
?? Give them a Honey? YES/NO (if the player has one)
```text
> YES:
ELDEST SISTER: Ah. Thyme honey. Here. A pebble for a pebble's worth.

YOUNGEST SISTER: It only ever says one thing. “Not yet.”

{PLAYER} received an Everstone!

MIDDLE SISTER: Give it to a Pokémon that's growing up too fast.

> NO:
MIDDLE SISTER: Bees remember who brings honey. So do we.

> after FLAG_ICHOR_DAPHNE_REVELATION:
YOUNGEST SISTER: We tried to cast for you, after you'd passed. Just to see.

YOUNGEST SISTER: The pebbles wouldn't fall. They stayed in the bowl.

ELDEST SISTER: We put the bowl away. Some bowls you put away.
```

### Trygaios's farmhouse (`MAP_THRIA_FARMHOUSE`)

- **Who:** Trygaios, a farmer, whose prize sow has run off.
- **The room:** a farmhouse with an indoor pig-pen in one corner (empty, with a full trough), seed jars along the wall, a plough propped by the door, and a little shrine of Demeter hung with dried wheat.
- **Event:** a small quest. His Kaplet followed a bee up Route 3 into the thyme meadow. Find her there (an overworld Kaplet; talking to her sends her trotting home) and he gives Leftovers. `FLAG_ICHOR_FOUND_TRYGAIOS_SOW`, `FLAG_ICHOR_HIDE_TRYGAIOS_SOW`.
```text
TRYGAIOS: My sow's gone. Best sow on the plain. Prize-winner.

TRYGAIOS: She ran up the pine slopes after a bee. She loves bees. Bees don't love her.

> on Route 3, the Kaplet in the meadow:
KAPLET: Oink! [It has thyme stuck in its ears. It trots off downhill, toward Thria.]

> back at the farmhouse:
TRYGAIOS: She's home! Covered in thyme. She smells delicious.

TRYGAIOS: Don't tell her I said that.

TRYGAIOS: Here. From the inn's kitchen. It never runs out, somehow.

{PLAYER} received Leftovers!

> after:
TRYGAIOS: She's sulking. The bees told her off.
```

**Signs**
```text
[Hamlet]
THRIA
The Inn of the Plain. Eleusa: half a day's walk west.
```

## Route 4, the Rheitoi (`MAP_ROUTE4_RHEITOI`)

**Layout.** About 55×24, from Thria west across the edge of the Thriasian plain. Two salt streams, the Rheitoi, cross the route; the road crosses the larger on a stone bridge. Past the bridge the wheat begins, with a grain shrine of Demeter at the field's edge and a flower meadow off to the south. Eleusa's gate is at the west edge.

**Rhythm:** Thria behind you (a calm stretch, and the far-off Telesterion roof); a forced grass band; the bridge and the jesters (a mandatory double battle at the only crossing); the spring by the stream (rest point); the wheat (a forced band of tall wheat, 4 deep, walled by the stream and a field wall); the desecrated grain shrine and its guard; the great herm; Lityerses in the wheat; Krokis's gate.

**Relic gates you can see:** a reed islet in the larger stream with an item ball (Poseidon's Conch, Act II), and a thorn thicket closing an old orchard south of the road (Demeter's Sickle, end of Act I), with a visible item.

| NPC | Where | Role |
|---|---|---|
| Spring-keeper | the spring | rest point |
| Priest's boy | the stream bank | lore |
| Iambe, Thersites, Lityerses, Eunikos, the shrine's guard | along the route | trainers (Part 3) |
| Krokis | Eleusa's gate | beat 19 |

**The spring.** A spring wells up beside the smaller stream under a plane tree.
```text
SPRING-KEEPER: Fresh water, right beside the salt. The goddess's little joke.

SPRING-KEEPER: Drink. Rest your Pokémon.

[heal the party]
```
**Priest's boy**
```text
PRIEST'S BOY: The Rheitoi are the goddess's streams. Only priests may fish them.

PRIEST'S BOY: The fish don't know that. I tell them. They don't listen.
```
(The player may fish here anyway; nobody stops a herald.)

**The grain shrine,** desecrated. A little roofed shrine with a clay figure of Demeter holding wheat ears, a sickle scratched across her. Its guard is in Part 3. Cleansing it gives +3 Demeter Favor, `FLAG_ICHOR_ALTAR_CLEANSED_ROUTE4`.
```text
A shrine of Demeter, hung with wheat. A sickle is scratched across her face.
```
**The great herm** stands at the field's edge: `FLAG_ICHOR_HERM_ROUTE4`.

**Signs**
```text
[East end]
ROUTE 4 · THE RHEITOI
East: Thria. West: Eleusa Village.

[Bridge]
THE BRIDGE OF THE RHEITOI. Pilgrims, expect insults. It's tradition.

[Stream]
The Rheitoi. Sacred to Demeter and the Kore. Priests' fishing only.
```

## Eleusa Village (`MAP_ELEUSA_VILLAGE`)

**Layout.** Eleusa is a farming village on a low hill above wheat fields. Krokis's gate is on the east. The village center is the **well-yard**: the Maiden's Well under a dry fig tree, with a worn bench. Around it: the Asclepeion (visible from the gate), a small Agora stall, and the houses. North, up a ramp, the walled **sanctuary**: its gateway (the Propylaia), the **Telesterion** (the Temple of Demeter, a great square hall with a columned porch, wheat-gold, the crown of the village), and, cut into the rock under the Telesterion's terrace, the **Ploutonion**, a cave mouth behind a bronze gate. South and west of the village, the **fields**: wheat (tall grass with its own table, Part 4), threshing floors, a poppy-strewn meadow, and the fenced **Rharian field**, the first field ever sown. The Eleutherai road leaves the north edge, choked with vines.

**Identity:** wheat and dark. The fields are the most open grass in Act I, and the sanctuary keeps the only secrets.

| NPC | Where | Role |
|---|---|---|
| Krokis | east gate | the saffron thread (beat 19) |
| Dysaules | the Rharian field | farmer; dread |
| Eubouleus | the fields | swineherd; trainer (Part 3) |
| Kid with a piglet | by the threshing floor | a hint |
| Water-carrier | the well | flavor |
| Kerykos's runner | the square, after the procession | carries a letter home (Part 2, Emporion's runners' house) |
| Kleon | the square (beat 20) | rival |
| Initiates, Eudemos, Alethea, Kerykos | the square, after `FLAG_ICHOR_PROCESSION_ARRIVED` | beat 22 |
| Daphne, Alethea | the Telesterion (beat 25) | — |

**Dysaules** (dread)
```text
DYSAULES: The Rharian field. First ever sown, by the goddess's own hand.

DYSAULES: Every year we sow it by hand. Every year it comes up on the same day.

DYSAULES: This year it came up. Then it went back down. Then it came up again.

DYSAULES: I've stopped telling people. They look at me like I've been at the wine.

> after FLAG_ICHOR_ACT1_COMPLETE:
DYSAULES: It's growing the right way again. For now. I check it every hour.
```
**Kid with a piglet**
```text
KID: This is Kopros. He's a Kaplet. He's my best friend.

KID: He found a coin in the well once. Now he won't stop staring into it.

KAPLET: Oink. [It is staring into the well.]
```
(The hint points at the well's hidden Bronze Obol.)

**Water-carrier**
```text
WATER-CARRIER: The Maiden's Well. The girls of the house of Keleos drew water here.

WATER-CARRIER: An old woman sat on that bench, they say, and nobody knew who she was.

WATER-CARRIER: They took her in anyway. That was the important part.
```
**The well's bench** (an object; a seed for the Demeter theoxenia after Laurel 5, SYSTEMS.md §10)
```text
A stone bench by the well, worn smooth, as if somebody sits here a lot.
```
**Kleon** (beat 20, before the trial). After the trial and before the Mysteries:
```text
KLEON: You got Chloe's laurel? …I never found her. In the dark.

KLEON: I ran into eleven pillars. Doso counted.

KLEON: She says I went down fine. I just never came back up.

KLEON: Doesn't matter. I'll get it later. Nothing in the dark matters.
```
Kleon fails the Lesser Mysteries, not a battle: he can't do the patient half of the trial. He leaves Eleusa with two laurels (beat 24).

**Houses.** Four households, each with a door and its own room (Eleusa interiors, below): the house of Keleos on the well-yard, Dysaules's farmhouse facing the Rharian field, the granary-keeper's house by the sanctuary ramp, and Euphorion's house on the lane to the fields. No other house is drawn with a door.

**Signs**
```text
[Village sign, east gate]
ELEUSA VILLAGE
Where the grain goes down, and comes back up.

[Sanctuary gateway]
THE SANCTUARY OF DEMETER AND THE KORE
Initiates only beyond the Telesterion. Silence, please.

[Temple]
TEMPLE OF DEMETER (THE TELESTERION)
Hierophant: Chloe, the Mystagogue.

[Ploutonion gate]
THE PLOUTONION. Closed. Closed. CLOSED. (The last in a different hand.)

[Rharian field]
THE RHARIAN FIELD. The first furrow. Please don't walk on it. Please.

[North edge]
North: the Eleutherai road to Thyrsa.

[The vines, without the Sickle]
Vines across the road, thick as rope. A good blade would clear them.
```

## Eleusa interiors

Four households and three public buildings; no two rooms share a layout (MAP_DESIGN §2).

| Building | Who | Event | Opens |
|---|---|---|---|
| Asclepeion | the healer | healing, the Pithos | arrival |
| Agora stall | a farm wife | the market | arrival |
| The house of Keleos | Metaneira, the xenia host | heal and rest; the goddess's drink | arrival; the drink after Laurel 3 |
| Dysaules's farmhouse | Theano, the farmer's wife | TM Bullet Seed | arrival |
| The granary-keeper's house | Sitokles | the Amulet Coin, once the iron is gone | after the theft |
| Euphorion's house | the playwright | trade a Melibee for his Pithound | arrival; a new ending after Act I |
| Temple of Demeter | Chloe and her acolytes | Laurel 3 | arrival |

### Asclepeion (`MAP_ELEUSA_VILLAGE_ASCLEPEION`)

- **The room:** a country Asclepeion, low and wide, built around a courtyard **herb garden** (mint, poppy, fennel) that the counter looks out on. Sheaves are stacked in one corner, bundles of herbs dry from the beams, and the healer grinds remedies in a stone mortar between patients. The Pithos is an old grain jar, painted with poppies. A Panacoil coils around the herb-garden gate post.

| NPC | Lines |
|---|---|
| Pilgrim with blisters | "I walked from Emporion. Barefoot. For the goddess." / "The goddess did not ask me to walk barefoot. I've checked." |
| Farmer | "Bitten by a Kaplet. On the ankle. It wasn't even angry. It was hungry." |

### Agora stall (`MAP_ELEUSA_VILLAGE_AGORA`)

- **The room:** a farmhouse front room turned shop: sacks of barley stacked to the ceiling, a hanging scale, honey jars in a row, and a counter made of a door laid across two barrels.
```text
STALLKEEPER: Barley, oil, honey, potions. Eleusa grows everything except surprises.
```

### The house of Keleos (`MAP_ELEUSA_VILLAGE_HOUSE_OF_KELEOS`)

- **Who:** Metaneira, head of Eleusa's oldest family, and her youngest daughter. In the Homeric Hymn, Keleos's wife Metaneira took the disguised Demeter in as a nurse for her baby son.
- **The room:** the oldest house in the village. A great hearth in the middle with a wooden cradle beside it, a long table worn smooth, a loom in the corner, and three water jars by the door for the trip to the well.
- **Events:** Eleusa's xenia host (per SYSTEMS.md §10): heal and rest. After Laurel 3, the goddess's drink, a seed for her theoxenia at the well after Laurel 5 (SYSTEMS.md §10: water and a barley cake is the drink she loves). `FLAG_ICHOR_GOT_KYKEON`.
```text
METANEIRA: Sit. Eat first.

METANEIRA: My family has fed strangers at this table since there was a table.

METANEIRA: Once it was a goddess, and we didn't know.

METANEIRA: So now we feed everyone. Just in case.

[heal the party; the rest menu as Philoxenos's]

> after FLAG_BADGE03_GET, once:
METANEIRA: Chloe gave you her laurel? Then you should have this.

METANEIRA: The goddess's own drink. Barley, water, a little mint. We call it kykeon.

METANEIRA: Keep the makings with you. You never know who's thirsty.

{PLAYER} received 2 Fresh Water and 2 Barley Cakes!

> with ITEM_HALF_COIN (the Split Coin, link 2; stretch):
METANEIRA: Philoxenos's half! He's still alive? He still owes me a goat.

METANEIRA: Here. Take my half on to Arkadia. And this, for the road.
```
[The chain continues per SYSTEMS.md §10 (Emporion → Eleusa → Arkadia → Kaldera). Give `ITEM_BIG_PEARL` here. `FLAG_ICHOR_SPLIT_COIN_2`.]
```text
GIRL: My sister Kallidike's an acolyte. She practices being mysterious at dinner.

GIRL: She says “I can't tell you” about the salt.
```

### Dysaules's farmhouse (`MAP_ELEUSA_VILLAGE_FARMHOUSE`)

- **Who:** Theano, Dysaules's wife. Dysaules himself is out at the Rharian field, staring at it.
- **The room:** a farmhouse kitchen with a plough propped by the door, seed jars along one wall, a cat asleep on a sack, and a stool under the window that faces the Rharian field, worn into a Dysaules-shaped dip.
- **Event:** a gift, TM Bullet Seed. `FLAG_ICHOR_GOT_TM_BULLET_SEED`.
```text
THEANO: He's at the field again, isn't he. Staring at it.

THEANO: Here. A Grass technique. Take it, before he teaches it to the wheat.

{PLAYER} received TM09, Bullet Seed!

> after:
THEANO: Twenty years married. I've never seen him look at me the way he looks at that field.

THEANO: I've made my peace with it. The field's very handsome.
```

### The granary-keeper's house (`MAP_ELEUSA_VILLAGE_GRANARY_HOUSE`)

- **Who:** Sitokles, keeper of the sanctuary's granaries.
- **The room:** half house, half storeroom. Jars of seed-corn on every shelf, a tally board on the wall marking every city's first fruits, a painting of the Kore, and a trapdoor with a ladder down to a private grain pit.
- **Event:** lore, then a gift once the theft has happened: the Amulet Coin his family kept near the cold iron. `FLAG_ICHOR_GOT_AMULET_COIN`.
```text
> before FLAG_ICHOR_FRAGMENT_STOLEN:
SITOKLES: Every city in Aethos sends Eleusa a share of its harvest. I count it.

SITOKLES: My grandmother said there's cold iron under the grain.

SITOKLES: You never plant over cold iron, she said. You keep it.

> after FLAG_ICHOR_FRAGMENT_STOLEN, once:
SITOKLES: The iron's gone. I felt it go. Like a tooth.

SITOKLES: My family kept this beside it, for luck. To keep the luck in, I suppose.

SITOKLES: No sense keeping it now. Take it. Ploutos hands out luck blind anyway.

{PLAYER} received an Amulet Coin!

> after:
SITOKLES: The grain doesn't care. Grain never cares. That's what I love about it.
```
| Object | Text |
|---|---|
| The wall painting | "A painting of a girl picking flowers. Behind her, the ground splits open." |
| A jar of seed-corn | "Seed-corn, kept back from the harvest. Next year's field, asleep in a jar." |
| Hidden item | Under the bed: a Revive. |

### Euphorion's house (`MAP_ELEUSA_VILLAGE_POETS_HOUSE`)

- **Who:** Euphorion, a playwright writing for the Dionysia at Thyrsa, and his Pithound, which reviews his work. Aeschylus came from Eleusis, and his father was named Euphorion.
- **The room:** wax tablets on every surface, scraped and rewritten; masks of tragedy and comedy on the walls; a stage chalked on the floor with three doors drawn at the back; and a chorus of clay figurines lined up on the windowsill.
- **Events:** an in-game trade, and a seed for Thyrsa that changes after Act I. `FLAG_ICHOR_TRADED_PITHOUND`.
```text
EUPHORION: I'm writing a tragedy for the Dionysia. At Thyrsa.

EUPHORION: It's about a family where the father eats the children.

EUPHORION: Too much? My mother says it's too much.

EUPHORION: My Pithound says it's too much. He growls at every line.

EUPHORION: I need a gentler audience. Bees, say. Bees only sting at the end.
```
?? Trade a Melibee for his Pithound? YES/NO. YES: in-game trade, Pithound nicknamed **CRITIC**, Lv 23, with its hidden ability (Prankster), holding a Twisted Spoon.
```text
> YES, after the trade:
EUPHORION: Take Critic. He was right about everything. That's the problem.

> NO:
EUPHORION: Then I'll read it to the dog again. Pray for me.

> after FLAG_ICHOR_ACT1_COMPLETE:
EUPHORION: I'm changing the ending. Now the youngest is never eaten at all.

EUPHORION: The father swallows a stone instead. I don't know why. It felt right.
```
| Object | Text |
|---|---|
| Desk | "Wax tablets, scraped and rewritten. One says “TOO MUCH?” in big letters." |
| The chalked stage | "Three doors drawn on the floor. Someone has walked through the middle one so often the chalk is gone." |

### Temple of Demeter (`MAP_ELEUSA_VILLAGE_TEMPLE_OF_DEMETER`)

Doso, Chloe and the acolytes are in beat 21, Part 3 and Part 5. The temple altar is Demeter's great altar.

## The Mystery sanctum, after the theft

`MAP_ELEUSA_MYSTERY_SANCTUM_B1F` to `B3F` stay open after beat 23, with the grunts gone and every brazier the player lit still burning. Chloe's line at the Ploutonion gate:
```text
CHLOE: You've seen it now. You may as well come back.

CHLOE: Mind the pits. And the seeds. The seeds are alive.
```
The wild tables (Part 4) and Daedalus's page II (Part 6) are here. On B3F, the collapsed tunnel:
```text
The Titans' tunnel, caved in. Somewhere above, it comes out in a field.
```

## Return to Kalliste

The ferry runs from the first arrival in Emporion. Phase 2 adds these to the slice's maps.

**Mom** (1F), new conditions:
```text
> after FLAG_ICHOR_CROSSING_DONE, before FLAG_ICHOR_ACT1_COMPLETE:
MOM: A mainlander! Look at you. Did you eat? You didn't eat.

MOM: Halia came by. She looked tired. She wouldn't say why.

> after FLAG_ICHOR_ACT1_COMPLETE, with FLAG_ICHOR_WROTE_TO_MOM:
MOM: You wrote! “I'm eating.” That's the whole letter. “I'm eating.”

MOM: …Something's happened. Daphne's letter was three pages and said nothing.

MOM: Sit. You don't have to tell me. Sit anyway.

MOM: And take these. From the hives. Not from that jar.

MOM: That jar's spoken for.

{PLAYER} received 3 Honey!

> after FLAG_ICHOR_ACT1_COMPLETE, without the letter:
MOM: Daphne wrote. Three pages, and they said nothing. You didn't write at all.

MOM: Sit. You don't have to tell me. Sit anyway.
```
[The Honey is given once: `FLAG_ICHOR_GOT_MOMS_HONEY`. It is never from the jar labelled NOT FOR {PLAYER}: STORY.md keeps that jar for Delphoi, and LABYRINTH.md's Ring VI shrine.]

**Daphne** (the Akademia), before `FLAG_ICHOR_MYSTERIES_NIGHT`; she is gone after it:
```text
DAPHNE: Halia's gull. Then Alethea's letter. I'm packing.

DAPHNE: I hate packing. I hate boats more. I've bought sandals. Look at them.

DAPHNE: …Go on. I'll find you on the mainland. Probably green.
```
**Halia**
```text
> after FLAG_ICHOR_HALIA_SECOND_LOOK, before FLAG_ICHOR_DAPHNE_REVELATION:
HALIA: Back already? No. I won't look again. Four times is enough for anyone.

> after FLAG_ICHOR_DAPHNE_REVELATION:
HALIA: So Daphne told you. I'm glad it was her and not me.

HALIA: Your thread's your own business. I meant it more than I knew.
```
**Euboulos** (Akti temple), a Charcoal for anyone who lost theirs (SYSTEMS.md §1):
```text
EUBOULOS: Lost your coal from the hearth? Take another. Hestia doesn't count.
```
[Give `ITEM_CHARCOAL` if the player has none and `FLAG_ICHOR_FORGE_RELIT` is unset.]

**Gylippos** (Elaia), after `FLAG_ICHOR_KLEON_LEFT_FOR_THYRSA`:
```text
GYLIPPOS: The boy went north. To the theater.

GYLIPPOS: …

GYLIPPOS: He wants an audience. He'll get one.
```

**What the Phase 2 relics open on Kalliste** (MAP_DESIGN §1: every relic opens something already visited):

| Relic | Where | What's behind it |
|---|---|---|
| Alethea's Trowel | Kalliste dig spots: daily spots on Kronion Hill, Route 1's terraces and Akti's beach; fixed finds in the crypt and the grotto | The Kronos amphora's four sherds (SYSTEMS.md §5, amphora 1) |
| Bronze Hammer | Marble rubble in the side of Kronion Hill's dig pit | **The Kronion Crypt** (`MAP_KALLISTE_ROUTE1_KRONION_CRYPT`): a short stair down to a small rock-cut room. Pebblith and Cairnolith, a fixed dig (a Kronos sherd), a Hard Stone, and a carved relief. |
| Hecate's Torch | The dark sea cave behind Akti's tide rocks | **Akti's Sea Grotto** (`MAP_AKTI_TOWN_SEA_GROTTO`): Hydna's "too still" water. Two braziers, Karkipool and Halcyling, a Big Pearl, a fixed dig (a Kronos sherd), and a fisherman's shrine. |
| Demeter's Sickle | A thorn thicket off Route 1's olive terraces | **The old grove:** Elaia's oldest olives. Elapling at 4% (Part 4), a visible Leaf Stone (which evolves Elapling), and a hidden Oran Berry. |
| Olive Oil | Route 1's spur-fork herm, Kalliste's great herm | `FLAG_ICHOR_HERM_ROUTE1` (SYSTEMS.md §4) |

**The Kronion Crypt's relief**
```text
A relief carved into the rock. A woman hands a giant something wrapped in cloth.

The giant is opening his mouth very wide.

The bundle is the shape of a baby. It's carved like a stone.
```
**Akti's Sea Grotto's shrine**
```text
A tiny shrine of shells. Someone scratched a name: GLAUKOS.

Below it, in smaller letters: “The herb tasted of the sea. I'm sorry, Mother.”
```
(In myth Glaukos the fisherman ate a herb that made him immortal and leapt into the sea. The slice's old Glaukos ate a strange seaweed once and "felt immortal for a week".)

**The Kronos amphora's lead** (SYSTEMS.md §5, amphora 1). When it is complete, at night, the broken altar on Kronion Hill hums, and checking it starts a static `SPECIES_CAIRNOLITH` at Lv 24 with its hidden ability (Sand Force), holding a Hard Stone: `FLAG_ICHOR_KRONION_ALTAR_STONE`.

---

# Part 3. Trainers

Format: the `src/data/trainers.party` syntax, as in the slice. Moves are listed only where they differ from the default (the last four level-up moves in the dex learnset), and every listed move is in the species' dex learnset at or below that level. Species constants exist once the dex is implemented.

**Conventions for Phase 2.**
- Route trainers: IVs 6, AI Check Bad Move.
- Titanborn grunts: IVs 6, AI Check Bad Move.
- Acolytes: IVs 10, AI Basic Trainer.
- Kleon: IVs 10, his starter 16, AI Basic Trainer.
- Hierophants and Hyperion: IVs 15 (Kerykos) or 18 (Chloe, Hyperion), aces 25 or 27, AI Basic Trainer, two Super Potions.
- Spartan difficulty needs its own boss teams from Balance, as in the slice.

## New trainer classes

Class names fit `TrainerClass.name[13]`. Each class needs a front portrait and an overworld walker; the walkers can share palette families as noted.

| Class | Who | Portrait | Walker | Placeholder pic until drawn |
|---|---|---|---|---|
| SAILOR | trireme hands, harbor sailors | a bare-chested oarsman in a short chiton, rope over one shoulder | sailor (shared with the slice's townsfolk sailor) | Sailor |
| MERCHANT | traders on the road and aboard | a portly man in a dyed himation, a purse and a set of scales | new; shares the townsfolk merchant's palette | Gentleman |
| POTTER | the Sacred Gate's kilns | a potter with clay-gray arms and a half-painted black-figure cup | new | Hiker |
| RUNNER | heralds' day-runners, athletes | a lean runner in a short chiton, mid-stride, petasos on a cord | new | Triathlete (running) M |
| INITIATE | pilgrims walking to the Mysteries | a youth in white with a myrtle crown and a bundle of myrtle branches | new, white and green; also used for the procession NPCs | Psychic F / Psychic M |
| JESTER | the bridge mockers | a figure in a grotesque comic mask, pointing and laughing | new, one male and one female palette | Twins (as a pair) |
| PILGRIM | devotees on the roads | a cloaked traveler with a staff and a covered dish (Hecate's supper) | new; shares the initiate's body, dark cloak | Hex Maniac |
| FISHER | shore and stream fishers | a fisher with a rod over one shoulder and a basket | fisher (shared with the slice's townsfolk fisher) | Fisherman |
| BEEKEEPER | Eleusa's meadows | a veiled beekeeper with a smoking clay pot | new | Bug Catcher |
| SWINEHERD | Eleusa's fields | a farm boy with a staff and a piglet under one arm | new; shares the harvester's palette | Camper |
| TITAN ADMIN | Hyperion (and later Iapetos and Rhea) | see Hyperion, below | per admin | Magma Admin |

Cast portraits and walkers needed: **Kerykos** (Hierophant), **Chloe** (Hierophant), **Hyperion** (Titan Admin), and Daphne's walker in new sandals (STORY.md §8.4). Alethea's portrait, which INVENTORY marks for Act II, is needed now for her practice battle.

## The crossing

**Alethea, practice battle** (optional). Her one Pokémon is the Spalunk she dug up on Kronion Hill; the third krater stays with Daphne (STORY.md decision S9).
```text
Before: [beat 10]
Defeat: ALETHEA: I lost, but correctly! I did every step!
After:  ALETHEA: I'm going to get better. Slowly. But I'll get there.
```
```
=== TRAINER_ICHOR_ALETHEA_DECK ===
Name: ALETHEA
Class: Scholar
Pic: Alethea
Gender: Female
Music: Girl
AI: Check Bad Move

Spalunk
Level: 12
Ability: Pickup
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe
```
**SCHOLAR** is a twelfth class, for Alethea alone; or she can borrow PILGRIM. See Open questions 6.

**SAILOR Phormion.** Amidships, in plain view.
```text
Before: PHORMION: Sea legs? Let's see if your Pokémon have them!
Defeat: PHORMION: Sunk! In a flat calm, too.
After:  PHORMION: A trireme's fast because it's light. That's why there's no room for your bags.
```
```
=== TRAINER_ICHOR_PHORMION ===
Name: PHORMION
Class: Sailor
Pic: Sailor
Gender: Male
Music: Swimmer
AI: Check Bad Move

Halcyling
Level: 13
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
- Water Gun
- Wing Attack
- Quick Attack
- Mist

Karkipool
Level: 14
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**MERCHANT Lykon.** By the cargo at the bow, facing away. Optional.
```text
Before: LYKON: Everything's for sale. Even a battle. This one's free.
Defeat: LYKON: Free, and I still lost on the deal.
After:  LYKON: The Agora at Emporion! They sell things there nobody's invented yet.
```
```
=== TRAINER_ICHOR_LYKON ===
Name: LYKON
Class: Merchant
Pic: Merchant
Gender: Male
Music: Rich
AI: Check Bad Move

Onotis
Level: 13
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Galekit
Level: 14
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

## Routes 5 and 6, the Halai Shore (optional), levels 15–17

**1. FISHER Asphalion.** Route 5, on the beach path, in plain view. In Theocritus, the fisherman Asphalion dreams he hooked a fish of gold.
```text
Before: ASPHALION: I dreamed I caught a golden fish. You're not gold. Battle anyway.
Defeat: ASPHALION: Dreams lie. So do fish.
After:  ASPHALION: My partner says a dream you tell never comes true. So I tell them all.
```
```
=== TRAINER_ICHOR_ASPHALION ===
Name: ASPHALION
Class: Fisher
Pic: Fisherman
Gender: Male
Music: Swimmer
AI: Check Bad Move

Ketofry
Level: 15
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Ketofry
Level: 15
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Karkipool
Level: 16
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**2. RUNNER Krison.** Route 5, running laps on the sand before Halai; his sight line crosses the beach.
```text
Before: KRISON: Run on sand and you're fast on stone. Race? No? Battle, then!
Defeat: KRISON: Out-paced!
After:  KRISON: Emporion and back four times today. The fifth time I'm taking a donkey.
```
```
=== TRAINER_ICHOR_KRISON ===
Name: KRISON
Class: Runner
Pic: Runner
Gender: Male
Music: Cool
AI: Check Bad Move

Lophops
Level: 16
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Galekit
Level: 16
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**3. FISHER Kymon.** Route 6, on the cliff path at its narrowest point, so he is mandatory to reach the cape.
```text
Before: KYMON: Touch my ray, your hand goes numb. Touch my Pokémon… same thing.
Defeat: KYMON: Numb. Just numb all over.
After:  KYMON: There's a philosopher in Astyra who does that to people. Just by talking.
```
```
=== TRAINER_ICHOR_KYMON ===
Name: KYMON
Class: Fisher
Pic: Fisherman
Gender: Male
Music: Swimmer
AI: Check Bad Move

Karkipool
Level: 16
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Narkeray
Level: 17
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**4. SAILOR Naubolos.** Route 6, on the cape, facing the sea. Optional.
```text
Before: NAUBOLOS: Those cliffs are full of snatchers. They took my lunch. Then my hat.
Defeat: NAUBOLOS: Then my other lunch. And now this.
After:  NAUBOLOS: There's a cave at the end of the cape nobody goes in. It's dark. That's the reason.
```
```
=== TRAINER_ICHOR_NAUBOLOS ===
Name: NAUBOLOS
Class: Sailor
Pic: Sailor
Gender: Male
Music: Swimmer
AI: Check Bad Move

Halcyling
Level: 16
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
- Water Gun
- Wing Attack
- Aqua Jet
- Quick Attack

Harpeck
Level: 17
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

## Temple of Hermes acolytes, levels 16–18

Steps don't count while a battle runs (Part 5). Podarge and Euchidas stand at narrow points; Philonides faces away and is optional.

**ACOLYTE Podarge.** The lower stoa, across the way back from the first herm. In myth Podarge, "swift-foot", is a harpy.
```text
Before: PODARGE: A herald who stops to chat is a late herald! …Let's chat. With Pokémon.
Defeat: PODARGE: Delayed! Delivered late!
After:  PODARGE: Oil a herm and it'll point. It's vain. Every herm in here is vain.
```
```
=== TRAINER_ICHOR_PODARGE ===
Name: PODARGE
Class: Acolyte
Pic: Acolyte F
Gender: Female
Music: Female
AI: Basic Trainer

Harpeck
Level: 16
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe

Epopoi
Level: 16
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
```

**ACOLYTE Euchidas.** The middle stoa, at the colonnade's narrow point. The real Euchidas ran from Plataea to Delphi and back in one day to fetch pure fire, and dropped dead at the finish.
```text
Before: EUCHIDAS: My namesake ran to Delphoi and back in one day. Then he died. I'm aiming for the first part.
Defeat: EUCHIDAS: Still breathing. In my family, that's a win.
After:  EUCHIDAS: Wrong turnstile and you're back where you started. Hermes thinks that's funny.
```
```
=== TRAINER_ICHOR_EUCHIDAS ===
Name: EUCHIDAS
Class: Acolyte
Pic: Acolyte M
Gender: Male
Music: Male
AI: Basic Trainer

Lophops
Level: 17
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe

Halcyling
Level: 17
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Water Pulse
- Wing Attack
- Aqua Jet
- Quick Attack
```
(Euchidas's first line is two boxes in game: split after "one day.")

**ACOLYTE Philonides.** The upper gallery, facing the wall. Optional.
```text
Before: PHILONIDES: I carried letters for a king once. He never said thank you. Battle me, and say it.
Defeat: PHILONIDES: Thank you. …See? That wasn't hard.
After:  PHILONIDES: Kerykos takes the short way. Everyone knows. Nobody knows where it is.
```
```
=== TRAINER_ICHOR_PHILONIDES ===
Name: PHILONIDES
Class: Acolyte
Pic: Acolyte M
Gender: Male
Music: Male
AI: Basic Trainer

Harpeck
Level: 17
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe

Lophops
Level: 18
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
```

## Hierophant Kerykos, the Herald, levels 18–21 (Hero difficulty)

A messenger, a calm-weather bird and a thief: Hermes's three jobs. Modelled on Brawly's strength (16/16/19), a level or two up.

```
=== TRAINER_ICHOR_KERYKOS_1 ===
Name: KERYKOS
Class: Hierophant
Pic: Hierophant Kerykos
Gender: Male
Music: Male
Items: Super Potion / Super Potion
AI: Basic Trainer

Lophops
Level: 18
Ability: Keen Eye
IVs: 15 HP / 15 Atk / 15 Def / 15 SpA / 15 SpD / 15 Spe
- Pluck
- Echoed Voice
- Feather Dance
- Quick Attack

Halcyling @ Oran Berry
Level: 19
Ability: Cloud Nine
IVs: 15 HP / 15 Atk / 15 Def / 15 SpA / 15 SpD / 15 Spe
- Water Pulse
- Pluck
- Aqua Jet
- Mist

Harpelle @ Sitrus Berry
Level: 21
Ability: Pickpocket
IVs: 25 HP / 25 Atk / 25 Def / 25 SpA / 25 SpD / 25 Spe
- Pluck
- Thief
- Taunt
- Tailwind
```
- **Lophops** leads with Feather Dance, so the player learns that a herald softens you up first.
- **Halcyling's** Cloud Nine switches off weather. It matters little now, and teaches the ability for later.
- **Harpelle** is evolved five levels early (Harpeck becomes Harpelle at 26), like Whitney's Miltank: the herald's real job is theft. Tailwind is Hermes's own wind. Pickpocket steals the player's held item when Harpelle is hit by contact, and Thief steals it outright; Kerykos gives stolen items back after the battle ("KERYKOS: Oh, and this is yours. Professional habit.").
- **The matchups:**
  - Nebrel players are weak to Flying. Their answers are Pebblith from Kronion Hill, Kerazap from the Halai Shore (commonest on Route 6's cliffs), and Thaletas's traded Narkeray (Electric) in the Deigma.
  - Kynder is neutral. Hipling is neutral, and Bulldoze does nothing to Flying types; Hipling players lean on Water moves and the Halcyling gift.

Defeat text: "Delivered! Signed, sealed, and soundly beaten!"

## Kleon, second battle (the Sacred Gate), levels 19–22

He has caught his way across Kalliste and the mainland: a rooster from Elaia's farmyards ("It woke me up at dawn. So I caught it. Fair's fair."), a hoopoe off the Emporion road, and his starter, now in its middle stage.

```
=== TRAINER_ICHOR_KLEON_2_KYNDER ===
Name: KLEON
Class: Lakonian
Pic: Kleon
Gender: Male
Music: Rival
AI: Basic Trainer

Lophops
Level: 19
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Pluck
- Echoed Voice
- Quick Attack
- Sand Attack

Alekrow
Level: 20
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
- Low Sweep
- Wake-Up Slap
- Bulk Up
- Fury Attack

Dikyon
Level: 22
IVs: 16 HP / 16 Atk / 16 Def / 16 SpA / 16 SpD / 16 Spe
- Fire Fang
- Double Hit
- Flame Charge
- Thunder Fang
```
The other two entries change only the ace:
- `TRAINER_ICHOR_KLEON_2_HIPLING`: **Thalamare** Lv 22, Aqua Jet, Flip Turn, Bulldoze, Double Kick.
- `TRAINER_ICHOR_KLEON_2_NEBREL`: **Kladoe** Lv 22, Magical Leaf, Fairy Wind, Quick Attack, Synthesis.

| Your starter | Kleon's ace | Why |
|---|---|---|
| Nebrel (Kladoe by now) | Dikyon | Fire beats Grass |
| Kynder (Dikyon) | Thalamare | Water beats Fire |
| Hipling (Thalamare) | Kladoe | Grass beats Water |

Alekrow hits hard and fast; it is the fight's real test, and Kleon's personality in a Pokémon. His lines are in beat 16. Defeat text: "No. No, no, no. I was ahead!"

## Route 2 trainers, levels 18–21

**1. POTTER Exekias.** By the kilns outside the Sacred Gate, in plain view. Exekias was the great black-figure painter; his best-known cup shows Achilles and Ajax playing at dice.
```text
Before: EXEKIAS: Every pot I paint, somebody breaks. Let's see what you break.
Defeat: EXEKIAS: Cracked. It'll still hold water. Mostly.
After:  EXEKIAS: I painted two heroes playing knucklebones once. They're still playing.
After:  EXEKIAS: It's a very long game.
```
```
=== TRAINER_ICHOR_EXEKIAS ===
Name: EXEKIAS
Class: Potter
Pic: Potter
Gender: Male
Music: Hiker
AI: Check Bad Move

Chelonet
Level: 18
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Spalunk
Level: 18
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**2. INITIATE Myrrhine.** Among the tombs, facing the road; mandatory. One of the pilgrims who set out early. Her last line is the Greek proverb "a donkey carrying the Mysteries": the one who does the work while others get the honor.
```text
Before: MYRRHINE: I'm going to the Mysteries! I can't tell you about them. I don't know yet!
Defeat: MYRRHINE: Oh! That was a mystery too.
After:  MYRRHINE: My donkey carries all my things. He'll carry the Mysteries, too.
After:  MYRRHINE: And never know what they were. There's a saying about that.
```
```
=== TRAINER_ICHOR_MYRRHINE ===
Name: MYRRHINE
Class: Initiate
Pic: Initiate F
Gender: Female
Music: Female
AI: Check Bad Move

Epopoi
Level: 18
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Onotis
Level: 19
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**3. GRUNT Laas** (TITANBORN), guarding the desecrated great herm on a short side path. Optional, but the herm can't be cleansed or anointed until he's beaten.
```text
Before: LAAS: This herm's ours now. See the sickle? I did that. It took ages.
Defeat: LAAS: Fine! Pray at it! See if that ugly stone face cares!
```
[After the battle he runs off east; hide him.]
```
=== TRAINER_ICHOR_GRUNT_ROUTE2_LAAS ===
Name: GRUNT
Class: Titanborn
Pic: Titan Grunt
Gender: Male
Music: Titan
AI: Check Bad Move

Pebblith
Level: 20
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Ergant
Level: 20
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**4. GOATHERD Menalkas.** On the hill spur, among his goats. Optional. Menalkas is a herdsman in Theocritus.
```text
Before: MENALKAS: My goats give milk, sparks and opinions.
Defeat: MENALKAS: Shocking. Truly.
After:  MENALKAS: Titans went up my goat path four days back. My goats are still offended.
```
```
=== TRAINER_ICHOR_MENALKAS ===
Name: MENALKAS
Class: Goatherd
Pic: Goatherd
Gender: Male
Music: Hiker
AI: Check Bad Move

Kerazap
Level: 19
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Kerazap
Level: 20
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**5. RUNNER Pheidippos.** At the narrow cutting before the camp; mandatory. A day-runner with a message for Eleusa, stuck behind the rockslide.
```text
Before: PHEIDIPPOS: A message for Eleusa! No time! …There's always time for a battle.
Defeat: PHEIDIPPOS: Beaten, and still not delivered.
After:  PHEIDIPPOS: There's a rockslide ahead. I'm a runner, not a climber.
After:  PHEIDIPPOS: I'm just going to stand here. Fast.
```
```
=== TRAINER_ICHOR_PHEIDIPPOS ===
Name: PHEIDIPPOS
Class: Runner
Pic: Runner
Gender: Male
Music: Cool
AI: Check Bad Move

Galekit
Level: 19
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Lophops
Level: 20
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**6. MERCHANT Kapelos.** At the procession's camp, by his cart of myrtle crowns. Optional, facing away.
```text
Before: KAPELOS: Stuck behind a mountain with a thousand pilgrims. Battle? It's free.
Defeat: KAPELOS: Free and losing. Story of my week.
After:  KAPELOS: I sell myrtle crowns to initiates. They wear them one night. Wonderful business.
```
```
=== TRAINER_ICHOR_KAPELOS ===
Name: KAPELOS
Class: Merchant
Pic: Merchant
Gender: Male
Music: Rich
AI: Check Bad Move

Onotis
Level: 20
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Harpeck
Level: 21
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

## Hecate's Hollow trainers, levels 20–21

Both stand in the lit western half, past the Hekataion.

**PILGRIM Hekabe.** By the first brazier. In one myth, old Queen Hekabe of Troy became a black dog, Hecate's own.
```text
Before: HEKABE: Hecate's light is on you, I see. Let's see if it's earned.
Defeat: HEKABE: Earned.
After:  HEKABE: The weasel was a girl once. She laughed at a goddess.
After:  HEKABE: Hecate took her in anyway. Hecate takes everyone in.
```
```
=== TRAINER_ICHOR_HEKABE ===
Name: HEKABE
Class: Pilgrim
Pic: Pilgrim
Gender: Female
Music: Suspicious
AI: Check Bad Move

Galekit
Level: 20
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Gelasable
Level: 21
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**INITIATE Kallias.** Sitting in the dark of a side passage, so he sees you only once you're close. The Kallias family were the Mysteries' hereditary torch-bearers.
```text
Before: KALLIAS: My family carry the Mysteries' torches! I forgot mine. Battle me so I feel better.
Defeat: KALLIAS: I feel worse.
After:  KALLIAS: Don't tell my father. He's the Torchbearer. Officially. He has a hat.
```
```
=== TRAINER_ICHOR_KALLIAS ===
Name: KALLIAS
Class: Initiate
Pic: Initiate M
Gender: Male
Music: Male
AI: Check Bad Move

Pebblith
Level: 21
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Onotis
Level: 21
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

## Route 3 trainers, levels 20–22

**1. HOPLITE Kynegeiros.** On the narrow ledge path below Xerxes's seat, facing down the road; mandatory. The real Kynegeiros was the brother of Aeschylus, who at Marathon grabbed a Persian ship's stern with one hand and had it cut off.
```text
Before: KYNEGEIROS: A king sat up there once to watch my grandfather lose. He didn't.
Before: KYNEGEIROS: Draw!
Defeat: KYNEGEIROS: Beaten on the same hill as a king. Good company.
After:  KYNEGEIROS: My grandfather grabbed an enemy ship with one hand. They cut it off.
After:  KYNEGEIROS: So he grabbed it with the other. We're a grabby family.
```
```
=== TRAINER_ICHOR_KYNEGEIROS ===
Name: KYNEGEIROS
Class: Hoplite
Pic: Hoplite
Gender: Male
Music: Intense
AI: Check Bad Move

Eopeep
Level: 20
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Ergant
Level: 21
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**2. PILGRIM Myrto.** At the niches of Aphrodite, facing the rock. Optional.
```text
Before: MYRTO: I left a clay dove for Aphrodite. Now I'm leaving with a battle.
Defeat: MYRTO: She'll understand. She likes a fight, secretly.
After:  MYRTO: Every niche is somebody who wanted to be loved back.
After:  MYRTO: That's a lot of niches.
```
```
=== TRAINER_ICHOR_MYRTO ===
Name: MYRTO
Class: Pilgrim
Pic: Pilgrim
Gender: Female
Music: Female
AI: Check Bad Move

Kerazap
Level: 20
Ability: Cute Charm
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Elaleaf
Level: 21
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**3. BEEKEEPER Aristaios.** In the thyme meadow, among the hives. Optional. In myth Aristaios lost all his bees, and the sea-god Proteus told him how to win them back.
```text
Before: ARISTAIOS: Careful! The bees are nervous. So am I. We're nervous together.
Defeat: ARISTAIOS: Everyone, calm down. Me especially.
After:  ARISTAIOS: I lost all my bees once. A sea-god told me how to get them back.
After:  ARISTAIOS: Long story. There's a cow in it.
```
```
=== TRAINER_ICHOR_ARISTAIOS ===
Name: ARISTAIOS
Class: Beekeeper
Pic: Beekeeper
Gender: Male
Music: Suspicious
AI: Check Bad Move

Melibee
Level: 21
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Melibee
Level: 21
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Melibee
Level: 22
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

## Route 4 trainers, levels 21–23

**1–2. JESTERS Iambe and Thersites,** one at each rail of the Rheitoi bridge. Both see the player at once on the only crossing, so it is a double battle (vanilla Emerald's two-trainer spotting). In the Homeric Hymn, old Iambe made the grieving Demeter laugh. Thersites is the Iliad's mocker. If the player has only one Pokémon able to fight, they battle one after the other.
```text
Before: IAMBE: Halt, pilgrim! Nobody crosses my bridge without being insulted!
Before: THERSITES: Look at those sandals. Did a goat make them? Did a goat WEAR them?
Defeat: IAMBE: Ha! A pilgrim with a sense of humor. Rare.
Defeat: THERSITES: That's it. I'm insulting the next one twice.
After:  IAMBE: We mock every pilgrim at the bridge. It reminds the goddess how to laugh.
After:  IAMBE: She forgot, once.
After:  THERSITES: I was voted ugliest man in three cities. Undefeated.
```
```
=== TRAINER_ICHOR_IAMBE ===
Name: IAMBE
Class: Jester
Pic: Jester F
Gender: Female
Music: Twins
AI: Check Bad Move

Galekit
Level: 21
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Lophops
Level: 22
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

=== TRAINER_ICHOR_THERSITES ===
Name: THERSITES
Class: Jester
Pic: Jester M
Gender: Male
Music: Twins
AI: Check Bad Move

Harpeck
Level: 21
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Onotis
Level: 22
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**3. FISHER Eunikos.** On the stream bank below the bridge. Optional.
```text
Before: EUNIKOS: Only priests may fish the Rheitoi. I'm a priest. Today.
Defeat: EUNIKOS: The goddess is not impressed with me.
After:  EUNIKOS: I'm not really a priest. Don't tell anyone. The fish know.
```
```
=== TRAINER_ICHOR_EUNIKOS ===
Name: EUNIKOS
Class: Fisher
Pic: Fisherman
Gender: Male
Music: Swimmer
AI: Check Bad Move

Ketofry
Level: 21
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Ketofry
Level: 21
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Karkipool
Level: 22
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**4. GRUNT Chalix** (TITANBORN), at the desecrated grain shrine. Optional, but she guards the shrine.
```text
Before: CHALIX: Shrine's closed. Orders. A sickle on every one. My wrist hurts.
Defeat: CHALIX: Go on, pray at it. The gods won't save you from your thread.
After:  CHALIX: We will.
```
[She runs off west; hide her.]
```
=== TRAINER_ICHOR_GRUNT_ROUTE3_CHALIX ===
Name: GRUNT
Class: Titanborn
Pic: Titan Grunt
Gender: Female
Music: Titan
AI: Check Bad Move

Spalunk
Level: 22
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Pebblith
Level: 23
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**5. HARVESTER Lityerses.** In the wheat band, facing across it; mandatory, and the band continues behind him, so there is no healing between. In myth Lityerses challenged every traveler to a reaping contest, and the loser lost his head.
```text
Before: LITYERSES: I challenge every traveler to a reaping contest! …A battle will do.
Defeat: LITYERSES: Reaped.
After:  LITYERSES: My great-great-grandfather was much stricter about the contest.
After:  LITYERSES: We don't talk about him.
```
```
=== TRAINER_ICHOR_LITYERSES ===
Name: LITYERSES
Class: Harvester
Pic: Harvester
Gender: Male
Music: Intense
AI: Check Bad Move

Stachyss
Level: 22
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Kaplet
Level: 23
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

## Eleusa trainer, level 22–23

**SWINEHERD Eubouleus.** In the fields by the threshing floor. Optional. In the myth, when the earth opened for the Kore, the swineherd Eubouleus's pigs fell in with her.
```text
Before: EUBOULEUS: When the earth opened for the Kore, my ancestor's pigs fell in too.
Before: EUBOULEUS: Nobody writes songs about the pigs. Battle!
Defeat: EUBOULEUS: Down they go.
After:  EUBOULEUS: Every year the priestesses throw piglets in a pit for the festival.
After:  EUBOULEUS: Mine always climb back out. I've stopped arguing with them.
```
```
=== TRAINER_ICHOR_EUBOULEUS ===
Name: EUBOULEUS
Class: Swineherd
Pic: Swineherd
Gender: Male
Music: Hiker
AI: Check Bad Move

Kaplet
Level: 22
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Kaplet
Level: 23
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

## Temple of Demeter acolytes, levels 23–24

In the dark, each acolyte holds a small clay lamp, so each stands in a small pool of light: a landmark as well as a checkpoint (Part 5).

**ACOLYTE Kallidike.** Beside the Autumn brazier, teaching. In the Hymn, Kallidike was the daughter of Keleos who brought the disguised Demeter home from the well.
```text
Before: KALLIDIKE: Put your torch out. Yes, on purpose. The dark won't bite. I will, a little.
Defeat: KALLIDIKE: Ow. You bit back.
After:  KALLIDIKE: See the seed glowing? That's her trail. Light the brazier beside it.
```
```
=== TRAINER_ICHOR_KALLIDIKE ===
Name: KALLIDIKE
Class: Acolyte
Pic: Acolyte F
Gender: Female
Music: Female
AI: Basic Trainer

Elaleaf
Level: 23
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe

Melibee
Level: 23
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
```

**ACOLYTE Eumolpos.** Between two columns on the way to the Winter brazier; mandatory. The Eumolpidai, "sweet singers", were the family of the Hierophants of Eleusis.
```text
Before: EUMOLPOS: My family has sung the hymns here since the first harvest. Here's one. It's a battle.
Defeat: EUMOLPOS: The shortest hymn in history.
After:  EUMOLPOS: The trail goes cold in winter. So does the goddess. Keep walking.
```
```
=== TRAINER_ICHOR_EUMOLPOS ===
Name: EUMOLPOS
Class: Acolyte
Pic: Acolyte M
Gender: Male
Music: Male
AI: Basic Trainer

Spalunk
Level: 23
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe

Stachyss
Level: 24
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
```

**ACOLYTE Melissa.** On the tiers by the Spring brazier, facing the wall. Optional. Demeter's priestesses were called *melissai*, bees.
```text
Before: MELISSA: The goddess's priestesses are called bees. Buzz. That's a joke. We don't buzz.
Defeat: MELISSA: …Bzz.
After:  MELISSA: Bees don't sleep through winter. They huddle and wait. Like everyone here.
```
```
=== TRAINER_ICHOR_MELISSA ===
Name: MELISSA
Class: Acolyte
Pic: Acolyte F
Gender: Female
Music: Female
AI: Basic Trainer

Melibee
Level: 24
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe

Rhoaril
Level: 24
IVs: 10 HP / 10 Atk / 10 Def / 10 SpA / 10 SpD / 10 Spe
```

## Hierophant Chloe, the Mystagogue, levels 24–27 (Hero difficulty)

Her team is the turning year: the seed in the dark, the stalk, the tree, and what the seed becomes. Her ace depends on the clock: **Kore by day, Persephone by night**, the dex's branching evolution made into a boss. Modelled on Wattson's four (20/20/22/24), a few levels up.

```
=== TRAINER_ICHOR_CHLOE_1_DAY ===
Name: CHLOE
Class: Hierophant
Pic: Hierophant Chloe
Gender: Female
Music: Female
Items: Super Potion / Super Potion
AI: Basic Trainer

Rhoaril
Level: 24
Ability: Leaf Guard
IVs: 18 HP / 18 Atk / 18 Def / 18 SpA / 18 SpD / 18 Spe
- Magical Leaf
- Leech Seed
- Mega Drain
- Astonish

Stachyss
Level: 25
Ability: Shed Skin
IVs: 18 HP / 18 Atk / 18 Def / 18 SpA / 18 SpD / 18 Spe
- Seed Bomb
- Glare
- Coil
- Synthesis

Elapling @ Miracle Seed
Level: 25
Ability: Harvest
IVs: 18 HP / 18 Atk / 18 Def / 18 SpA / 18 SpD / 18 Spe
- Seed Bomb
- Rock Smash
- Bullet Seed
- Leech Seed

Korantha @ Sitrus Berry
Level: 27
Ability: Natural Cure
IVs: 27 HP / 27 Atk / 27 Def / 27 SpA / 27 SpD / 27 Spe
- Petal Dance
- Giga Drain
- Fairy Wind
- Leech Seed
```
`TRAINER_ICHOR_CHLOE_1_NIGHT` is the same entry with the ace changed:
```
Persenyx @ Sitrus Berry
Level: 27
Ability: Cursed Body
IVs: 27 HP / 27 Atk / 27 Def / 27 SpA / 27 SpD / 27 Spe
- Hex
- Giga Drain
- Leech Seed
- Magical Leaf
```
- **Rhoaril** leads, because the seed goes down first.
- **Stachyss's** Glare paralyzes, and it is the trial's lesson in battle form: the dark slows you down.
- **Elapling** is there because the olive is Kalliste's oldest tree, met again in the mainland's oldest field. It holds a Miracle Seed, so its Harvest ability is idle. Rock Smash is its answer to Halcyling.
- **The ace.** Korantha (Grass/Fairy) by day hits hard with Petal Dance. Persenyx (Grass/Ghost) by night is bulkier, slower and immune to Normal and Fighting, with Cursed Body. The battle-start check is `GetTimeOfDay() == TIME_NIGHT`.
- **The matchups:**
  - Kynder players have the edge.
  - Hipling players are weak to the whole team; the Halcyling gift, Harpeck, Lophops and Melibee are their answers.
  - Nebrel players are neutral, but Kladoe's Grass moves are resisted, so they lean on Fairy Wind, Quick Attack and their catches.
- A player who wants to face both forms can come back at the other hour for the post-game rematch (not in Phase 2).

Defeat text: "…Good."

## The Mystery sanctum: Titanborn grunts, levels 24–25

All are `GRUNT` / Titanborn / Titan Grunt / Music: Titan / Check Bad Move / IVs 6. Each carries a lamp, so each is a lit landmark in the dark (Part 5). Alethea fights a sixth, offscreen, in beat 23A.

**GRUNT Pelos** (B1F, mandatory, across the granary aisle)
```text
Before: PELOS: Forty lamps. Do you know what forty lamps cost? Rhea does. She made us sign for them.
Defeat: PELOS: I'm docking this from my own lamp.
```
```
=== TRAINER_ICHOR_GRUNT_SANCTUM_PELOS ===
Name: GRUNT
Class: Titanborn
Pic: Titan Grunt
Gender: Male
Music: Titan
AI: Check Bad Move

Spalunk
Level: 24
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Ergant
Level: 22
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**GRUNT Bolos** (B1F, optional, guarding a side pit with an item)
```text
Before: BOLOS: Hyperion sent us to the wrong hill on Kalliste. Rhea found the right one first try.
Defeat: BOLOS: Rhea brings snacks, too. Hyperion never brings snacks.
```
```
=== TRAINER_ICHOR_GRUNT_SANCTUM_BOLOS ===
Name: GRUNT
Class: Titanborn
Pic: Titan Grunt
Gender: Male
Music: Titan
AI: Check Bad Move

Pebblith
Level: 24
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Kaplet
Level: 25
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**GRUNT Konis** (B2F, mandatory, at the far end of the Hall of the Kore)
```text
Before: KONIS: You got past the lamps? Then you'll get past me. No. Wait. That's wrong.
Defeat: KONIS: That's what I meant, though.
```
```
=== TRAINER_ICHOR_GRUNT_SANCTUM_KONIS ===
Name: GRUNT
Class: Titanborn
Pic: Titan Grunt
Gender: Female
Music: Titan
AI: Check Bad Move

Spalunk
Level: 25
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Cairnolith
Level: 25
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**GRUNT Gaios** (B2F, optional, in a fresco alcove with an item)
```text
Before: GAIOS: The frescoes down here are a girl getting dragged under the earth. Cheerful.
Defeat: GAIOS: She comes back in the last picture. I checked. That's something.
```
```
=== TRAINER_ICHOR_GRUNT_SANCTUM_GAIOS ===
Name: GRUNT
Class: Titanborn
Pic: Titan Grunt
Gender: Male
Music: Titan
AI: Check Bad Move

Galekit
Level: 24
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Pebblith
Level: 24
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Hoplomex
Level: 25
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

## Rhea of the Titans, first battle, levels 25–28

**Why Rhea, and not Hyperion or Iapetos.**
- **Eleusa is her myth.** In the Homeric Hymn to Demeter, it is Rhea, Demeter's own mother, whom Zeus sends down to Eleusis to bring her grieving daughter home. A grieving mother sent to a grieving mother's town is the strongest first meeting any admin can have.
- **Her motive is Act I's theme.** The Mysteries promise that the daughter comes back every spring. Rhea, "a mother who lost her children to prophecy", doesn't believe it, and says so in the place built on it.
- **Ground is the digging type,** and the earth-born Titans dig. The slice's grunts failed on the wrong hill with a Nosepass; the competent one finds the fragment.
- **It sets up LABYRINTH.md's Rhea.** Her mercy at Knossa (LABYRINTH L5) is the first crack in Team Titan. A player who met her first as a mother rocking a stone will believe that crack.
- **The others are better saved.** Hyperion stays offscreen and feared ("Hyperion's going to roast us"), so his entrance can be the loud one; he already has the Ring VI forge fight and the finale. Iapetos is the bible's Act II schemer at Thyrsa, and Rhea's last line hands him to Phase 3.

**Her look.** A broad woman in her fifties: a bronze Corinthian helmet pushed back off gray-streaked hair, a heavy wool cloak dyed earth-brown, and the sickle emblem as a bronze brooch. She carries a stone swaddled like a baby in the crook of one arm, as the Titaness Rhea handed Kronos a swaddled stone instead of her last child. She never explains it. Her portrait holds the bundle; her walker carries it.

**Her team.** A patient tortoise that sings lullabies, a sacrificial piglet, a goat, and a cairn. The goat is Kerazap, the Amalthea line, the goat that nursed a child hidden from Kronos. Nobody points out the irony.

```
=== TRAINER_ICHOR_RHEA_1 ===
Name: RHEA
Class: Titan Admin
Pic: Admin Rhea
Gender: Female
Music: Titan
Items: Super Potion / Super Potion
AI: Basic Trainer

Chelonet
Level: 25
Ability: Sturdy
IVs: 18 HP / 18 Atk / 18 Def / 18 SpA / 18 SpD / 18 Spe
- Sing
- Bulldoze
- Round
- Withdraw

Kaplet
Level: 25
Ability: Thick Fat
IVs: 18 HP / 18 Atk / 18 Def / 18 SpA / 18 SpD / 18 Spe
- Dig
- Take Down
- Bulldoze
- Rest

Kerazap
Level: 26
Ability: Static
IVs: 18 HP / 18 Atk / 18 Def / 18 SpA / 18 SpD / 18 Spe
- Electro Ball
- Spark
- Thunder Wave
- Charm

Cairnolith @ Sitrus Berry
Level: 28
Ability: Sturdy
IVs: 27 HP / 27 Atk / 27 Def / 27 SpA / 27 SpD / 27 Spe
- Rock Slide
- Bulldoze
- Rock Blast
- Rock Polish
```
- **Chelonet** leads with Sing: a lullaby, then Bulldoze.
- **Kerazap** covers the Water and Flying answers to her Ground types.
- **Cairnolith** is a grave cairn. Rock Polish, then Rock Slide, is the fight's spike.
- **The matchups:**
  - Hipling (Thalamare by now) and Nebrel (Kladoe) players have the edge on three of the four.
  - Kynder players are weak to most of it. Their answers are the Halcyling gift (Water/Flying: immune to Ground, and Water hits Cairnolith four times over), Stachyss from Eleusa's fields, and Karkipool.

Defeat text: "Good. Someone taught you well. Go home and thank them."

## Every species in Phase 2, with its myth or setting link

All are from the Aethos dex; the myths are the dex's, in brief.

| Species | Where in Phase 2 | Link |
|---|---|---|
| Nebrel / Kladoe, Kynder / Dikyon, Hipling / Thalamare | starters; Kleon; Alethea | Daphne the laurel; Kerberos and Orthros; Poseidon's hippocampi |
| Epopoi / Lophops | routes; Kerykos; Kleon | Aristophanes's hoopoe, herald of the birds |
| Galekit / Gelasable | everywhere at night; Hekabe | Galanthis, the laughing servant Hecate took in |
| Elaleaf / Elapling | Eleusa's fields; Kalliste's old grove; Chloe | Athena's olive, which regrew overnight |
| Ergant / Hoplomex | the Hollow; grunts; Aegina's ant hills | the Myrmidons, ants made men, on their own island |
| Pebblith / Cairnolith | caves and mountain roads; Team Titan; Rhea | Deucalion's thrown stones that became people; a grave cairn |
| Kerazap | hill pastures; Menalkas; Rhea | Amalthea, the goat who hid a child from Kronos |
| Halcyling / Galenyon | the crossing (gift); coasts; Kerykos | Alcyone and the halcyon days |
| Ketofry / Kynoketos | fishing everywhere | the ketos, the sea-beast Perseus killed |
| Karkipool | tide pools; fishing | Karkinos, Hera's crab |
| Nemecub | rare, the scrub hills behind Emporion | the Nemean lion, Ione's ace |
| Eopeep / Alekrow | Kleon | Alectryon, the lookout turned rooster |
| Onotis | Emporion's outskirts; merchants; initiates | Midas's ears; "a donkey carrying the Mysteries" |
| Harpeck / Harpelle | Emporion's rooftops and cliffs; the crossing; Kerykos's ace | the Harpies, the snatchers; Hermes, god of thieves |
| Chelonet | the hills around Emporion; Exekias; Rhea | the tortoise Hermes made the first lyre from |
| Pithound | Emporion's empty jars | Diogenes in his jar |
| Melibee | Eleusa's meadows; Aristaios; acolytes | the Melissai, Demeter's bee-priestesses |
| Narkeray | the crossings (Good Rod); Kymon; the Deigma trade | the torpedo ray Meno compared to Socrates |
| Stachyss / Stachypter | Eleusa's wheat; Chloe | Triptolemus's serpent chariot |
| Rhoaril / Korantha / Persenyx | the sanctum; the fields; Chloe's ace | Persephone and the pomegranate |
| Kaplet | Eleusa's farms; Eubouleus; Rhea | Eubouleus's pigs; Demeter's piglets |
| Spalunk / Plouteras | fields and granaries; grunts | Ploutos, the blind wealth of the harvest |
| Lykopup (static) | Hecate's Hollow at night | Hecate's black hounds |
| Raknit (static) | the Hollow's web chamber | Arachne the weaver |
| Obolorn (rare) | Route 2's tombs at night | the unburied dead on the near bank |

---

# Part 4. Wild encounters

In `src/data/wild_encounters.json` terms, as in the slice. Land slots are 20/20/10/10/10/10/5/5/4/4/1/1. `OW_TIME_OF_DAY_ENCOUNTERS` is already TRUE, so each map defines `_Morning` (used for morning, day and evening) and, where it differs, `_Night`. Fishing and water fall back to `_Morning`.

**Deviations from the dex's habitats** are marked †, and listed in Open questions 16.

## Routes 5 and 6, the Halai Shore

Land `encounter_rate: 20`. Open before Laurel 2, so their levels sit just above the voyage's. Halai itself has no grass.

`MAP_ROUTE5_HALAI_BEACH`, the beach and dunes:

| Slot | Rate | `_Morning` | Levels | `_Night` | Levels |
|---|---|---|---|---|---|
| 0 | 20% | Halcyling | 14–16 | Galekit | 14–16 |
| 1 | 20% | Harpeck | 14–16 | Onotis | 14–16 |
| 2 | 10% | Onotis | 14–16 | Karkipool | 14–16 |
| 3 | 10% | Chelonet | 14–16 | Chelonet | 14–16 |
| 4 | 10% | Lophops | 15–17 | Gelasable | 15–17 |
| 5 | 10% | Karkipool | 14–16 | Galekit | 15–16 |
| 6 | 5% | Kerazap | 15–17 | Harpeck | 15–17 |
| 7 | 5% | Epopoi | 14–16 | Karkipool | 15–16 |
| 8 | 4% | Galekit | 15–17 | Onotis | 16–17 |
| 9 | 4% | Karkipool | 16–17 | Galekit | 16–17 |
| 10 | 1% | Galenyon | 17–17 | Gelasable | 17–17 |
| 11 | 1% | Nemecub | 16–16 | Nemecub | 16–16 |

`MAP_ROUTE6_HALAI_CLIFFS`, the cliffs and the pasture. The cliff-top pasture behind the rubble shares this table; its reasons to visit are a visible item and the densest grass on the route.

| Slot | Rate | `_Morning` | Levels | `_Night` | Levels |
|---|---|---|---|---|---|
| 0 | 20% | Harpeck | 15–17 | Galekit | 15–17 |
| 1 | 20% | Kerazap | 15–17 | Cairnolith | 15–17 |
| 2 | 10% | Halcyling | 15–17 | Kerazap | 15–17 |
| 3 | 10% | Chelonet | 15–17 | Pebblith † | 15–17 |
| 4 | 10% | Lophops | 15–17 | Chelonet | 15–17 |
| 5 | 10% | Pebblith † | 15–17 | Gelasable | 16–17 |
| 6 | 5% | Onotis | 15–17 | Harpeck | 16–17 |
| 7 | 5% | Cairnolith | 16–17 | Onotis | 15–17 |
| 8 | 4% | Galenyon | 16–17 | Galekit | 17–17 |
| 9 | 4% | Epopoi | 15–17 | Cairnolith | 17–17 |
| 10 | 1% | Harpelle | 18–18 | Nemecub | 17–17 |
| 11 | 1% | Nemecub | 17–17 | Gelasable | 17–17 |

## Route 2, the Sacred Way

`MAP_ROUTE2_SACRED_WAY`, land `encounter_rate: 20`.

| Slot | Rate | `_Morning` | Levels | `_Night` | Levels |
|---|---|---|---|---|---|
| 0 | 20% | Lophops | 17–19 | Galekit | 17–19 |
| 1 | 20% | Onotis | 17–19 | Onotis | 17–19 |
| 2 | 10% | Chelonet | 17–19 | Gelasable | 18–20 |
| 3 | 10% | Galekit | 17–19 | Chelonet | 17–19 |
| 4 | 10% | Kerazap | 18–20 | Cairnolith | 18–20 |
| 5 | 10% | Epopoi | 17–19 | Spalunk | 17–19 |
| 6 | 5% | Ergant | 17–19 | Pebblith | 17–19 |
| 7 | 5% | Elaleaf | 17–19 | Kerazap | 18–20 |
| 8 | 4% | Spalunk | 18–20 | Ergant | 18–20 |
| 9 | 4% | Harpeck | 18–20 | Galekit | 18–20 |
| 10 | 1% | Nemecub | 19–19 | Obolorn † | 19–19 |
| 11 | 1% | Nemecub | 20–20 | Nemecub | 19–19 |

## Hecate's Hollow

`MAP_HECATES_HOLLOW`, one table at all hours, land `encounter_rate: 10`. Encounters are on in the dark half too: being jumped by something you can't see is part of the place.

| Slot | Rate | Species | Levels |
|---|---|---|---|
| 0 | 20% | Pebblith | 19–21 |
| 1 | 20% | Spalunk | 19–21 |
| 2 | 10% | Galekit | 19–21 |
| 3 | 10% | Ergant | 19–21 |
| 4 | 10% | Cairnolith | 20–21 |
| 5 | 10% | Gelasable | 20–21 |
| 6 | 5% | Pebblith | 21–21 |
| 7 | 5% | Galekit | 21–21 |
| 8 | 4% | Chelonet | 20–21 |
| 9 | 4% | Spalunk | 21–21 |
| 10 | 1% | Cairnolith | 21–21 |
| 11 | 1% | Gelasable | 21–21 |

Statics: Lykopup † Lv 22 at the Hekataion at night (beat 18); Raknit † Lv 22 with Defiant in the web chamber, after the Arachne amphora (Part 2).

## Route 3, the Pine Slopes

`MAP_ROUTE3_PINE_SLOPES`, land `encounter_rate: 20`. Hill and mountain-road species, as the dex places them; Melibee belong to Aristaios, not the wild.

| Slot | Rate | `_Morning` | Levels | `_Night` | Levels |
|---|---|---|---|---|---|
| 0 | 20% | Lophops | 20–21 | Galekit | 20–21 |
| 1 | 20% | Kerazap | 20–21 | Gelasable | 20–21 |
| 2 | 10% | Chelonet | 20–21 | Cairnolith | 20–21 |
| 3 | 10% | Galekit | 20–21 | Kerazap | 20–21 |
| 4 | 10% | Onotis | 20–21 | Onotis | 20–21 |
| 5 | 10% | Epopoi | 20–21 | Chelonet | 20–21 |
| 6 | 5% | Elaleaf | 20–21 | Spalunk | 20–21 |
| 7 | 5% | Ergant | 20–21 | Pebblith | 20–21 |
| 8 | 4% | Cairnolith | 21–21 | Ergant | 21–21 |
| 9 | 4% | Spalunk | 21–21 | Galekit | 21–21 |
| 10 | 1% | Nemecub | 21–21 | Nemecub | 21–21 |
| 11 | 1% | Kerazap | 22–22 | Gelasable | 22–22 |

Thria has no grass.

## Route 4, the Rheitoi

`MAP_ROUTE4_RHEITOI`, land `encounter_rate: 20`.

| Slot | Rate | `_Morning` | Levels | `_Night` | Levels |
|---|---|---|---|---|---|
| 0 | 20% | Stachyss | 20–22 | Gelasable | 20–22 |
| 1 | 20% | Lophops | 20–22 | Galekit | 20–22 |
| 2 | 10% | Melibee | 20–22 | Kaplet | 20–22 |
| 3 | 10% | Kaplet | 20–22 | Spalunk | 20–22 |
| 4 | 10% | Spalunk | 20–22 | Stachyss | 20–22 |
| 5 | 10% | Onotis | 20–22 | Onotis | 20–22 |
| 6 | 5% | Elaleaf | 20–22 | Cairnolith | 21–22 |
| 7 | 5% | Halcyling | 20–22 | Elaleaf | 20–22 |
| 8 | 4% | Kerazap | 21–22 | Chelonet | 21–22 |
| 9 | 4% | Epopoi | 21–22 | Galekit | 22–22 |
| 10 | 1% | Galenyon | 22–22 | Gelasable | 22–22 |
| 11 | 1% | Stachyss | 22–22 | Kerazap | 22–22 |

## Eleusa Village, the fields

`MAP_ELEUSA_VILLAGE`, land `encounter_rate: 20`. Only the wheat and the meadow have grass; the village streets have none.

| Slot | Rate | `_Morning` | Levels | `_Night` | Levels |
|---|---|---|---|---|---|
| 0 | 20% | Stachyss | 21–23 | Gelasable | 21–23 |
| 1 | 20% | Melibee | 21–23 | Galekit | 21–23 |
| 2 | 10% | Kaplet | 21–23 | Kaplet | 21–23 |
| 3 | 10% | Spalunk | 21–23 | Spalunk | 21–23 |
| 4 | 10% | Elaleaf | 21–23 | Stachyss | 21–23 |
| 5 | 10% | Lophops | 21–23 | Elaleaf | 21–23 |
| 6 | 5% | Epopoi | 21–23 | Onotis | 21–23 |
| 7 | 5% | Gelasable | 22–23 | Kerazap | 22–23 |
| 8 | 4% | Kerazap | 22–23 | Spalunk | 23–23 |
| 9 | 4% | Onotis | 22–23 | Kaplet | 23–23 |
| 10 | 1% | Korantha | 23–23 | Gelasable | 23–23 |
| 11 | 1% | Stachypter | 23–23 | Galekit | 23–23 |

Static: Persenyx Lv 26 in the fields in the evening, after the Persephone amphora (SYSTEMS.md §5, amphora 2; `FLAG_ICHOR_ELEUSA_PERSENYX`).

## The Mystery sanctum

Land `encounter_rate: 10`. B1F is the granaries; B2F and B3F share the deeper table. At night, the deeper table's two 1% slots become Persenyx.

`MAP_ELEUSA_MYSTERY_SANCTUM_B1F`

| Slot | Rate | Species | Levels |
|---|---|---|---|
| 0 | 20% | Spalunk | 22–24 |
| 1 | 20% | Rhoaril | 22–24 |
| 2 | 10% | Kaplet | 22–24 |
| 3 | 10% | Galekit | 22–24 |
| 4 | 10% | Pebblith | 22–24 |
| 5 | 10% | Spalunk | 23–25 |
| 6 | 5% | Rhoaril | 24–25 |
| 7 | 5% | Ergant | 22–24 |
| 8 | 4% | Plouteras | 24–25 |
| 9 | 4% | Gelasable | 23–25 |
| 10 | 1% | Plouteras | 25–25 |
| 11 | 1% | Rhoaril | 25–25 |

`MAP_ELEUSA_MYSTERY_SANCTUM_B2F` and `_B3F`

| Slot | Rate | `_Morning` | Levels | `_Night` | Levels |
|---|---|---|---|---|---|
| 0 | 20% | Rhoaril | 23–25 | Rhoaril | 23–25 |
| 1 | 20% | Spalunk | 23–25 | Spalunk | 23–25 |
| 2 | 10% | Pebblith | 23–25 | Pebblith | 23–25 |
| 3 | 10% | Kaplet | 23–25 | Kaplet | 23–25 |
| 4 | 10% | Rhoaril | 24–25 | Rhoaril | 24–25 |
| 5 | 10% | Cairnolith | 24–25 | Cairnolith | 24–25 |
| 6 | 5% | Gelasable | 24–25 | Gelasable | 24–25 |
| 7 | 5% | Spalunk | 25–25 | Spalunk | 25–25 |
| 8 | 4% | Plouteras | 25–25 | Plouteras | 25–25 |
| 9 | 4% | Rhoaril | 25–25 | Rhoaril | 25–25 |
| 10 | 1% | Plouteras | 25–25 | Persenyx | 25–25 |
| 11 | 1% | Rhoaril | 25–25 | Persenyx | 25–25 |

## Fishing and water

Fishing `encounter_rate: 30`; water (`water_mons`) `encounter_rate: 4`, slots 60/30/5/4/1. The Good Rod comes from Aigialeus in Halai. The Super Rod and Poseidon's Conch come later; their slots are filled now so the tables are ready.

| Map | Old Rod (70 / 30) | Good Rod (60 / 20 / 20) | Super Rod (40 / 40 / 15 / 4 / 1) |
|---|---|---|---|
| `MAP_TRIREME_EUPLOIA_DECK` | Ketofry 10–15 / Karkipool 10–15 | Narkeray 15–25 / Ketofry 15–20 / Karkipool 15–20 | Kynoketos 25–30 / Narkeray 25–30 / Karkipool 25–30 / Kynoketos 30–35 / Narkeray 35 |
| `MAP_EMPORION_CITY` | Ketofry 5–10 / Karkipool 5–10 | Karkipool 10–20 / Ketofry 10–20 / Narkeray 15–20 | Kynoketos 25–30 / Narkeray 25–30 / Karkipool 25–30 / Kynoketos 30–35 / Narkeray 35 |
| `MAP_AEGINA_TOWN` | Ketofry 10–15 / Karkipool 10–15 | Karkipool 15–20 / Narkeray 15–20 / Ketofry 15–20 | as Emporion |
| `MAP_ROUTE5_HALAI_BEACH` | Ketofry 10–15 / Karkipool 10–15 | Karkipool 15–20 / Ketofry 15–20 / Narkeray 15–20 | as Emporion |
| `MAP_ROUTE6_HALAI_CLIFFS` (the cape: "rays past the point") | Ketofry 10–15 / Karkipool 10–15 | Narkeray 15–20 / Karkipool 15–20 / Ketofry 15–20 | as Emporion |
| `MAP_ROUTE4_RHEITOI` | Ketofry 15–20 / Karkipool 15–20 | Karkipool 20–25 / Ketofry 20–25 / Narkeray 20–25 | as Emporion |

| Map (water) | 60% | 30% | 5% | 4% | 1% |
|---|---|---|---|---|---|
| Emporion, Aegina, Routes 5–6 | Halcyling 20–30 | Ketofry 20–30 | Galenyon 25–30 | Narkeray 25–30 | Galenyon 30 |
| Route 4 | Halcyling 20–30 | Ketofry 20–30 | Karkipool 25–30 | Narkeray 25–30 | Galenyon 30 |

## Aegina's interior (the proposed detour)

`MAP_AEGINA_APHAIA_ROAD`, land `encounter_rate: 20`. The temple hilltop and Mount Oros share it.

| Slot | Rate | `_Morning` | Levels | `_Night` | Levels |
|---|---|---|---|---|---|
| 0 | 20% | Ergant † | 18–20 | Galekit | 18–20 |
| 1 | 20% | Epopoi | 18–20 | Ergant † | 18–20 |
| 2 | 10% | Chelonet | 18–20 | Gelasable | 19–20 |
| 3 | 10% | Lophops | 18–20 | Chelonet | 18–20 |
| 4 | 10% | Galekit | 18–20 | Onotis | 18–20 |
| 5 | 10% | Halcyling | 18–20 | Karkipool | 18–20 |
| 6 | 5% | Kerazap | 19–21 | Pebblith | 19–21 |
| 7 | 5% | Ergant † | 20–21 | Ergant † | 20–21 |
| 8 | 4% | Karkipool | 19–21 | Cairnolith | 20–21 |
| 9 | 4% | Onotis | 19–21 | Galekit | 20–21 |
| 10 | 1% | Hoplomex † | 21–21 | Hoplomex † | 21–21 |
| 11 | 1% | Galenyon | 21–21 | Gelasable | 21–21 |

## Kalliste, new in Phase 2

These maps open with the Phase 2 relics (Part 2, Return to Kalliste). The slice's own Kalliste tables still use vanilla species and need an Aethos pass under dex decision D5 (Open questions 18).

| Slot | Rate | Kronion Crypt (rate 10) | Levels | Akti Sea Grotto (rate 10) | Levels | Route 1 old grove (rate 20) | Levels |
|---|---|---|---|---|---|---|---|
| 0 | 20% | Pebblith | 18–20 | Pebblith | 20–22 | Elaleaf | 24–26 |
| 1 | 20% | Ergant | 18–20 | Karkipool | 20–22 | Epopoi | 24–26 |
| 2 | 10% | Galekit | 18–20 | Halcyling | 20–22 | Galekit | 24–26 |
| 3 | 10% | Pebblith | 20–22 | Galekit | 20–22 | Ergant | 24–26 |
| 4 | 10% | Cairnolith | 20–22 | Pebblith | 22–24 | Lophops | 25–27 |
| 5 | 10% | Ergant | 20–22 | Karkipool | 22–24 | Elaleaf | 26–27 |
| 6 | 5% | Galekit | 20–22 | Halcyling | 22–24 | Kerazap | 25–27 |
| 7 | 5% | Cairnolith | 22–22 | Cairnolith | 22–24 | Eopeep | 25–27 |
| 8 | 4% | Kerazap | 20–22 | Galenyon | 24–24 | Elapling | 26–27 |
| 9 | 4% | Pebblith | 22–22 | Cairnolith | 24–24 | Galekit | 27–27 |
| 10 | 1% | Kerazap | 22–22 | Galenyon | 24–24 | Elapling | 27–27 |
| 11 | 1% | Cairnolith | 22–22 | Karkipool | 24–24 | Psychora | 27–27 |

The old grove is its own small map, `MAP_KALLISTE_ROUTE1_OLD_GROVE`, so it can have this table. The Sea Grotto's pool fishes like Akti's.

---

# Part 5. The rites, the Hollow and the sanctum

## The Herald's Run (Temple of Hermes)

Per SYSTEMS.md §12, Hermes's verb: **race and route**. The rules here (the step-glass, the anointed herms, the one-way turnstiles, battles pausing the count, failure returning the scrolls) are SYSTEMS.md's; this section lays them out.

### What the player sees

One long hall, entered from the south: an Ionic **stoa** that folds back on itself three times, in three galleries one above the other, joined at alternate ends by short stairs. A frieze of winged runners runs along the walls. Bronze **turnstiles** (a four-armed gate on a post) stand in the galleries. Stone **herms** stand at every fork, their heads facing straight out at you. Three of them, the **herald-herms**, wear a bronze plaque each: a doorway, a sandal, a purse. Kerykos's **dais** is at the top, behind a closed bronze gate. By the door: the oil jar, the step-glass on its stand, and Angelos.

```text
  +---------------------------[ DAIS: KERYKOS ]----------------------------+
  |  [H3 purse] . . J4 . . (T5) . . . . . (dais gate) . . . [Philonides]  |  UPPER
  |       ^ loop: (T6) runs you back along the gallery to J4              |  gallery
  +----------------------------------------------------------------- . ---+
  |                                                                 stair  |
  |  . . J3 . (T3) . . . . [Euchidas] . . . . (T4) . . . . . [H2 sandal]   |  MIDDLE
  |  loop: (T3b) back to the stair foot                                   |  gallery
  +-stair-+---------------------------------------------------------------+
  |       |                                                                |
  |  . . . J2 . (T2a) . . (T2b) . . [door] . . J1 . (T1) . [Podarge] [H1] |  LOWER
  |          loop: (T2a) back to the door                      doorway     |  gallery
  +------------------------------[ entrance ]------------------------------+
   (T) one-way turnstile    J junction herm    H herald-herm
```

### What the player does

1. **Take the scrolls.** Kerykos's YES (beat 15) gives three sealed scrolls and starts the step-glass. The count shows in the start-menu info panel ("Step-glass: 120"), per SYSTEMS.md §2's display rule.
   ```text
   {PLAYER} took three sealed scrolls.

   The first is addressed “To Hermes of the Threshold.” The second, “Of the Road.”

   The third, “Of the Market.” The step-glass begins to run.
   ```
2. **Oil a junction herm** (J1 to J4). A herm's head faces south until oiled. Interacting:
   ```text
   A herm of Hermes. His stone eyes stare straight ahead.

   Oil his face?
   ```
   YES uses one Olive Oil (the oil jar by the door refills you to 3, free). The head turns, by `turnobject`, to face the branch that leads to the **next undelivered** herald-herm. After each delivery, every oiled herm in the hall turns again.
   ```text
   The oil runs down the stone. Slowly, the head turns.
   ```
   An oiled herm, checked again: "The herm is looking that way. Pointedly."
3. **Pass a turnstile.** Each turns one way only. From the wrong side: "The turnstile won't turn that way." The wrong-way turnstiles at forks lead into loops that come out back where they started, costing steps.
4. **Deliver a scroll** at the matching herald-herm, in order. The right one:
   ```text
   A herm with a bronze plaque: a doorway. “Hermes of the Threshold.”

   You slip the scroll into the niche at its foot. Somewhere, a bell rings once.
   ```
   The wrong one, or the right one out of order: "The plaque shows a sandal. This scroll isn't for this herm. Not yet."
5. **The dais.** When the third scroll is delivered, the dais gate swings open and Kerykos is already there (beat 15).
6. **Running dry.** At 30 steps left: "The step-glass is running low." At 0:
   ```text
   The last grain falls. The scrolls flap out of your hands and fly back to the door.

   KERYKOS: [from somewhere] Late! A herald is never late.

   KERYKOS: He's sometimes early, and blames the wind.
   ```
   Warp the player to the entrance. The scrolls are with Kerykos again; oiled herms **stay oiled**, so a second try is easier. No other penalty.
7. **Battles don't count.** The step hook ignores steps taken while a trainer walks up to you, and no steps pass in battle.

### The three legs: teach, test, master

| Leg | Teaches | Optimal steps | What's in it |
|---|---|---|---|
| Lower (to H1) | Oiled herms point; turnstiles turn one way | ~22 | J1 by the door points east once oiled. One turnstile (T1). H1 is in plain sight once you're past T1. Podarge stands across the way back from H1, so she must be fought. |
| Middle (to H2) | Reading the herms at a fork; the cost of a wrong loop | ~34 | Back west past the door: J2 at a fork of two turnstiles. T2a loops to the door (about 16 steps lost); T2b takes the stair. Then J3 at a three-way fork, and Euchidas at the colonnade's narrow point (mandatory). H2 at the east end. |
| Upper (to H3) | Everything at once, with the glass tight | ~28 | The stair by H2. J4 and two turnstiles: T5 the right one, T6 a loop. Philonides optional, facing the wall. H3 at the west end, then back east to the dais. |

The optimal route is about 84 steps with every junction herm oiled. The glass is 120 on Hero, 150 on Mortal and 100 on Spartan (SYSTEMS.md), so a Hero player can make one wrong loop and still finish; a Spartan player must read the herms.

### Placement and gates

- **Podarge:** lower gallery, between T1 and H1, facing west, sight 3. Mandatory.
- **Euchidas:** middle gallery at the colonnade, facing east, sight 4 across the only gap. Mandatory.
- **Philonides:** upper gallery, facing north at the wall. Optional.
- **Kerykos:** on the dais. The dais gate is a metatile gate, open at 3 deliveries.
- **The engine:** the Fortree Gym's rotating gates (`src/rotating_gate.c`) are Emerald's own Flying-temple turnstiles and may do this job with the arms placed to allow one direction. If not, each turnstile is a coord event that blocks entry from the wrong side and a two-frame metatile swap. Either way, Low.

### State

| Name | Values |
|---|---|
| `VAR_TEMP_1` | scrolls delivered, 0–3 (resets on leaving the map, which also returns the scrolls) |
| `VAR_TEMP_2` | steps left in the glass |
| `FLAG_ICHOR_HERMES_HERM_J1` … `_J4` | junction herm oiled (permanent) |
| `FLAG_ICHOR_HERALDS_RUN_DONE` | set at the third delivery, permanent |

The map's `ON_LOAD` turns oiled herms by `VAR_TEMP_1`. After `FLAG_BADGE02_GET`, every herm faces the dais, the gate stays open and the glass is gone from its stand: "The step-glass has been put away. Kerykos says you've nothing left to prove. Then he talks for ten minutes."

## The Lesser Mysteries (Temple of Demeter)

Per SYSTEMS.md §12, Demeter's verb: **dark and light**: the Torch, braziers and dousing (SYSTEMS.md §2). The rules (pitch dark, douse to see the glowing seeds, relight to see walls, a season's brazier at each seed, Chloe revealed by the fourth) are SYSTEMS.md's. Two refinements here: only the **next** seed glows, so the trail is followed rather than solved, and the last stretch adds grain pits.

### What the player sees

The **Telesterion**: one great square hall with a **forest of columns** (a grid of 7 by 6, as at Eleusis), stepped seats (tiers) climbing all four walls, and the **Anaktoron** in the middle, a small stone room with one door. It is pitch dark: flash level 3 with the torch. A cold bronze **brazier** stands in each corner, each with a plaque: a falling leaf (Autumn), a bare branch (Winter), a sprout (Spring), a sheaf (Summer). The acolytes each hold a small clay lamp, so each stands in a pool of light.

```text
  +--------------------------------------------------------------+
  | tiers  tiers  tiers  tiers  tiers  tiers  tiers  tiers  tiers |
  | [WINTER]   o    o    o    o    o    o    o        [SPRING]    |
  |  seed 2        o    o    o    o    o    o          seed 3     |
  | tiers   o    o    +------------+    o    o   [Melissa] tiers   |
  |         o    o    | ANAKTORON  |    o    o    . . . . .        |
  | tiers   o  [Eumolpos]   (Chloe)     o    o    . pits  .  tiers |
  |  seed 1        o    +----door----+  o    o    . . . . .        |
  | [AUTUMN]   o    o    o    o    o    o    o   seed 4 [SUMMER]  |
  |  [Kallidike]                [Doso]                             |
  +---------------------------[ entrance ]-------------------------+
     o column    seeds glow only while the torch is doused
```

### What the player does

1. **Douse the torch** from the Relic Ring (per SYSTEMS.md §1 and §2). The walls and columns vanish; only glow-paint shows. Here that is one **glowing pomegranate seed**, the next on the trail.
   ```text
   You douse the torch. The dark is total.

   …Except for one small red point of light, low down, not far away.
   ```
2. **Relight** to see the walls, and walk toward where the seed was. Alternate the two until you reach it.
3. **Light the season's brazier** beside the seed (the Torch on a brazier, per SYSTEMS.md §2). Its corner becomes a lit zone for good.
   ```text
   A cold bronze brazier. Its plaque shows a falling leaf.

   Light it with Hecate's Torch?

   The brazier catches. Its corner of the hall is suddenly, warmly gold.

   The seed at its foot is gone. Somewhere else in the dark, another has begun to glow.
   ```
   A brazier lit out of turn: "The brazier won't take. Its plaque shows a sprout. The year isn't there yet." Nothing resets.
4. **The fourth brazier** (Summer) lights the Anaktoron's doorway from all four corners, and Chloe is revealed (beat 21).

### The four seeds: teach, test, master

| Seed | Season | Teaches | The way there |
|---|---|---|---|
| 1 | Autumn, front left | Douse to see, relight to walk | Near the door. Kallidike stands at the brazier and teaches (she's mandatory: her sight line covers the first steps). The way is open. |
| 2 | Winter, back left | Navigating by memory | Across the column forest. Seen doused, it looks close; the columns make you go round. Eumolpos stands between two columns on the only straight line (mandatory). |
| 3 | Spring, back right | The tiers | Up on the tiers by the right wall, reached only by the steps at the hall's far end. Melissa is on the tiers, facing the wall (optional). |
| 4 | Summer, front right | Combining: douse **and** read the floor | The front-right quarter is floored with **grain pits** you can't see when doused. Hecate's chalk marks the safe stones, and the chalk glows only when doused, like the seed. Walk doused by the chalk, relight to check. A step into a pit drops you, unhurt, onto the tiers by the Spring brazier: "You slide down into a grain pit. Someone has helpfully left a ladder." |

The **safety valve** is Doso: talking to her after any two minutes in the hall offers "DOSO: Lost? Put your light out and look for the red. The goddess always leaves a trail." and, after a fall into a pit, "DOSO: The chalk marks the stones. Hecate's chalk. It only shows in the dark."

### State

| Name | Values |
|---|---|
| `IchorSave.litBraziers`, four bits | the Autumn, Winter, Spring and Summer braziers (per SYSTEMS.md §2) |
| `FLAG_ICHOR_LESSER_MYSTERIES_DONE` | set when the fourth is lit |

The next seed is derived from the bits: the first unlit brazier in season order. `ON_LOAD` draws lit braziers and zones and places the one glowing seed. Leaving the temple keeps every brazier lit. After `FLAG_BADGE03_GET`, the four braziers burn, the pits are boarded over, and the hall stays dark between them, as a temple of the Mysteries should.

**Engine notes.** The glow palette is SYSTEMS.md §2's douse (Low–Medium): the temple's tileset needs a glow copy in which only the seed, the chalk and the lamps show. The pit is a hole metatile that warps to the tiers.

## Hecate's Hollow: the Three Roads

Per SYSTEMS.md §1, relic quest 3. About 40×30.

```text
            WEST MOUTH (to Route 3)
                  |
         [brazier 2] . . [Kallias, side passage]
                  |
         [brazier 1] . . [Hekabe]       [WEB CHAMBER] (burn the webs)
                  |                          |
            ( HEKATAION: the three-faced pillar, the altar )   <- lit faintly from above
                  ^
   fork 3: ahead  |  (left and right loop back to fork 3)
                  |
   fork 2: right  +--- left: a dead end with a Bronze Obol (item ball)
                  |
   fork 1: left   +--- right: loops back to fork 1, past a hidden Escape Rope
                  |
           the dark begins
                  |
     daylight . . . . . . [old woman]
            EAST MOUTH (from Route 2)
```

- **The first half is dark** (flash level 7, 1.5 tiles) and is the only way through. The forks are simple, and the dog's bark is the guide (beat 18).
- **Every wrong branch pays or loops** (MAP_DESIGN §1): a dead end with an item, or a loop back to the fork.
- **The second half** (after the Torch) has two braziers to light, two trainers, and the web chamber. Lit braziers are landmarks for the walk back.
- **The midpoint rest** is the Hekataion itself: praying at Hecate's altar there gives her minor blessing (SYSTEMS.md §3), and a spring trickles down the pillar: "Cold water runs down the pillar's three faces. You feel rested." (heal).

## The Mystery sanctum

A three-floor story dungeon under the Telesterion. MAP_DESIGN §3: teach, test, combine; a midpoint rest; a payoff.

| Floor | Size | What it does |
|---|---|---|
| **B1F, the granaries** | 36×28 | **Teach.** A wide hall of round grain pits and great storage jars. Dark (the Torch's radius). Four braziers along the walls: each lit one makes its stretch a lit zone. The grunts' lamps are moving lights, so you can see them coming. Chloe holds the stair (and heals). Pelos stands across the main aisle; Bolos guards a side pit with a visible Hyper Potion. A fixed dig spot behind a jar: a Persephone sherd. |
| **B2F, the Hall of the Kore** | 20×40 | **Test.** A long frescoed hall: four painted panels of the Kore's story, read one by one. A chasm runs down the middle (impassable; its floor glows faintly red). The near half is a chalk path across pits, like the Summer seed: douse to see the chalk. Kleon and the iron-tasting spring (the midpoint rest) are halfway. Konis at the far end (mandatory). Gaios in a fresco alcove (optional) with TM Dig, which the Titans left behind. |
| **B3F, the deepest granary** | 18×18 | **Payoff.** A round vault, the Titans' tunnel, the bronze chest, Rhea (beat 23C). After the story: the collapsed tunnel, and Daedalus's page II in a fixed dig spot where the tunnel exposed the old foundations. |

**The four frescoes** (B2F, examined in order south to north):
```text
A girl picking flowers in a meadow. Behind her the ground is splitting open.

A chariot of black horses, going down. The girl's arms reach back.

A woman with a torch, searching. Beside her, a smaller figure with two torches.

The girl again, coming up a stair into the light. The flowers are open.
```
The third fresco's second figure is Hecate. A player who has met her will know.

**After the theft** the grunts are gone and every brazier the player lit still burns (Part 2).

---

# Part 6. Items and rewards by map

Flag naming follows the slice: visible items `FLAG_ICHOR_ITEM_<MAP>_<ITEM>`, hidden items `FLAG_ICHOR_HIDDEN_<MAP>_<ITEM>`, gifts as named in the scenes. TM numbers are vanilla where vanilla has the move; Balance assigns the rest. Dig spots follow SYSTEMS.md §5: daily spots use the Act I loot table, and fixed finds are listed here.

## The relics and tools of Phase 2

Phase 2 gives three relics and two tools, in SYSTEMS.md's order (the Talaria came in the slice).

| # | Relic or tool | From | Opens in Phase 2 | Opens back on Kalliste |
|---|---|---|---|---|
| tool | **Alethea's Trowel** | Alethea, Emporion's quay (beat 11) | Dig spots everywhere: Daedalus's page II, three amphorae's sherds | The Kronos amphora's sherds; fixed finds in the crypt and the grotto |
| 2 | **Bronze Hammer** | Kedalion, the Hephaisteion (beat 13) | The rockslide on Route 2 (main path); the cliff-top pasture on Route 6 | **The Kronion Crypt**, under the dig pit |
| 3 | **Hecate's Torch** | The Hekataion, Hecate's Hollow (beat 18) | The Hollow's second half and web chamber; the Lesser Mysteries and the sanctum (main path); the Salt Grotto | **Akti's Sea Grotto** |
| 4 | **Demeter's Sickle** | Chloe, the sanctum (beat 23) | The vines on the Eleutherai road to Thyrsa (Act II's main path); the laurel grove on Route 2's spur; the pine hollow on Route 3; the orchard on Route 4 | **The old grove** off Route 1 |
| tool | **The Star Chart** | Daphne (beat 25) | — (per SYSTEMS.md §8) | — |

## By map

| Map | Item | How | Where |
|---|---|---|---|
| Trireme, deck | Super Potion | visible | among the cargo at the bow |
| Trireme, deck | Heart Scale | hidden | in a coil of rope at the stern |
| Trireme, hold | Potion | visible | under the bottom bench |
| Trireme | Halcyling | gift (beat 10) | — |
| Aegina Town | Big Pearl | hidden | at the end of the mole |
| Aegina Town | Stardust | hidden | at the foot of Kolona's column |
| Aegina Town, the mint | Chelonet "STATER" | in-game trade for a Karkipool | — |
| Aegina Town, Aiakides's house | Black Belt | show him an Ergant | — |
| Aphaia Road (detour) | Silver Powder | visible | on the ant hills |
| Aphaia Road (detour) | Super Potion | visible | at the Oros fork |
| Temple of Aphaia (detour) | Pretty Feather ×2 | visible | on the temple steps (Artemis's offering) |
| Temple of Aphaia (detour) | Potsherd | fixed dig | the old foundations (Open questions 23: which amphora) |
| Mount Oros (detour) | Wine | visible | by Zeus's altar (his offering) |
| Emporion | Olive Oil ×3 | gift, Kerykos (beat 11) | — |
| Emporion | Alethea's Trowel | gift, Alethea (beat 11) | — |
| Emporion | Potsherd (Arachne amphora) | fixed dig | the planter by the quay herm |
| Emporion | Super Potion | visible | on the shipsheds' slipway |
| Emporion | X Speed | visible | at the end of the stoa |
| Emporion | Repel | visible | behind the Deigma |
| Emporion | Bronze Obol | hidden | in a crack in the harbor wall |
| Emporion | Heart Scale | hidden | on the quay steps |
| Emporion | Honey | hidden | under Kydon's awning |
| Emporion | Figy Berry ×3, Pretty Feather | gift, Sykeas | — |
| Emporion | Daedalus's page I | trade an Olive Oil, Glykera | — |
| Emporion, Deigma | Narkeray "SOCRATES" | in-game trade for an Onotis | — |
| Emporion, Hephaisteion | Bronze Hammer | quest, Kedalion (beat 13) | — |
| Emporion, runners' house | Quick Claw | gift | — |
| Emporion, widow's house | Sea Incense | gift | — |
| Emporion, tavern | TM Fling | Myrtale's first loss | — |
| Emporion, Philoxenos's house | Wine ×1 per new laurel | a story for a laurel | — |
| Emporion, Philoxenos's house | Half Coin | gift (stretch: the Split Coin) | — |
| Emporion, Euphronios's workshop | Super Potion ×2, Great Ball ×3, Star Piece | show him a Harpeck, a Chelonet, a Stachyss | — |
| Temple of Hermes | Herald Laurel (badge 2), TM40 Aerial Ace | Kerykos | — |
| Temple of Hermes | TM U-turn | Kerykos, Hermes Favor 30 | — |
| Route 5 | Potion | visible | on the beach path |
| Route 5 | Net Ball | visible | among the drawn-up boats |
| Route 5 | Shoal Shell | hidden | on the beach |
| Route 5 | Shoal Shell | hidden | under the last boat |
| Route 5 | Pearl | hidden | in a tide pool |
| Route 5, Grotto of the Twelve | TM Thief (vanilla `ITEM_TM46`) | visible | by the altar |
| Halai | Shoal Salt | hidden | in a heap at the salt pans |
| Halai | Shoal Salt | hidden | by the drying racks |
| Halai, Aigialeus's hut | Good Rod | gift | — |
| Halai, Halmyris's hut | Shell Bell | swap 2 Shoal Salt and 2 Shoal Shell | — |
| Halai, Sagene's hut | Big Pearl | show her a Narkeray | — |
| Route 6 | Super Potion | visible | halfway up the cliff path |
| Route 6 | Magnet | visible | the cliff-top pasture (behind the Hammer's rubble) |
| Route 6 | Thunder Stone | visible | on the islet (Poseidon's Conch, Act II) |
| Route 6 | Heart Scale | hidden | at the tip of the cape |
| Route 6, Salt Grotto | Big Pearl | visible | — |
| Route 6, Salt Grotto | Star Piece | hidden | behind the second brazier |
| Route 6, Salt Grotto | Potsherd (Hermes amphora) | fixed dig | — |
| Route 2 | Potion | visible | by the kilns |
| Route 2 | Repel | visible | in a walled grave plot, off the forced band |
| Route 2 | Super Potion | visible | up the hill spur |
| Route 2 | TM39 Rock Tomb | the rockslide's last heap | — |
| Route 2 | Barley Cake ×2 | gift, Eudemos (beat 17) | — |
| Route 2 | Revive | visible | inside the walled tomb (the Girdle, Act II) |
| Route 2 | Sun Stone | visible | in the laurel grove (Demeter's Sickle) |
| Route 2 | Laurel Sprig | the grove's laurel tree, once a day | — |
| Route 2 | Oran Berry | hidden | by a milestone |
| Route 2 | Ether | hidden | in the kiln's ash |
| Route 2 | Stardust | hidden | by the procession's campfire |
| Hecate's Hollow | Escape Rope | hidden | on fork 1's loop |
| Hecate's Hollow | Bronze Obol | visible | fork 2's dead end |
| Hecate's Hollow | Hecate's Torch | the Hekataion (beat 18) | — |
| Hecate's Hollow | Silk Scarf | visible | the web chamber |
| Hecate's Hollow | Ether | visible | by the second brazier |
| Route 3 | Super Potion | visible | in the first pine clearing |
| Route 3 | Great Ball | visible | beside Xerxes's seat |
| Route 3 | Super Repel | visible | at the end of the thyme meadow |
| Route 3 | PP Up | visible | at the ruined watchtower (the Girdle, Act II) |
| Route 3 | Calcium | visible | in the pine hollow (Demeter's Sickle) |
| Route 3 | Honey | hidden | under a beehive in the meadow |
| Route 3 | Pretty Feather | hidden | in a niche of Aphrodite's shrine |
| Thria | Potion | visible | behind the inn's stable |
| Thria | Oran Berry | hidden | by the well |
| Thria, the inn | Gelasable "GALANTHIS" | in-game trade for an Onotis | — |
| Thria, the sisters' house | Everstone | swap for a Honey | — |
| Thria, Trygaios's farmhouse | Leftovers | find his sow on Route 3 | — |
| Route 4 | Super Potion | visible | on the road out of Thria |
| Route 4 | Great Ball | visible | at the foot of the bridge |
| Route 4 | Big Pearl | visible | on the reed islet (Poseidon's Conch, Act II) |
| Route 4 | Sitrus Berry | visible | in the orchard (Demeter's Sickle); the orchard's fig tree is a berry tree (Figy) |
| Route 4 | Heart Scale | hidden | in the stream shallows |
| Route 4 | Shoal Salt | hidden | at the salt stream's edge |
| Route 4 | Revive | hidden | behind the grain shrine |
| Eleusa | Super Potion | visible | on the threshing floor |
| Eleusa | Awakening | visible | in the poppy meadow |
| Eleusa | Honey | hidden | by the beehives in the meadow |
| Eleusa | Pomeg Berry | hidden | under the fig by the well |
| Eleusa | Bronze Obol | hidden | in the Maiden's Well |
| Eleusa, farmhouse | TM09 Bullet Seed | gift, Theano | — |
| Eleusa, granary-keeper's house | Revive | hidden | under the bed |
| Eleusa, granary-keeper's house | Amulet Coin | gift, Sitokles, after the theft | — |
| Eleusa, house of Keleos | Fresh Water ×2, Barley Cake ×2 | gift, Metaneira, after Laurel 3 | — |
| Eleusa, house of Keleos | Big Pearl | the Split Coin, link 2 (stretch) | — |
| Eleusa, Euphorion's house | Pithound "CRITIC" | in-game trade for a Melibee | — |
| Elaia, player's house (return) | Honey ×3 | Mom, after the letter home | — |
| Temple of Demeter | Harvest Laurel (badge 3), TM19 Giga Drain, Barley Cake | Chloe | — |
| Temple of Demeter | TM Leech Seed | Chloe, Demeter Favor 30 | — |
| Sanctum B1F | Hyper Potion | visible | the side pit Bolos guards |
| Sanctum B1F | Potsherd (Persephone amphora) | fixed dig | behind a great jar |
| Sanctum B2F | TM28 Dig | visible | Gaios's alcove |
| Sanctum B2F | Super Potion | visible | by the second fresco |
| Sanctum B2F | Ether | hidden | in the basin's overflow |
| Sanctum B3F | Soft Sand | visible | at the tunnel's mouth |
| Sanctum B3F | Demeter's Sickle | gift, Chloe (beat 23) | — |
| Sanctum B3F | Daedalus's page II | fixed dig, after the theft | the exposed foundations |
| Eleusa, well | Star Chart | gift, Daphne (beat 25) | — |
| Kronion Crypt | Hard Stone | visible | — |
| Kronion Crypt | Potsherd (Kronos amphora) | fixed dig | — |
| Akti Sea Grotto | Big Pearl | visible | — |
| Akti Sea Grotto | Potsherd (Kronos amphora) | fixed dig | — |
| Route 1 old grove | Leaf Stone | visible | — |
| Route 1 old grove | Oran Berry | hidden | — |

**Daily dig spots** (per SYSTEMS.md §5), with the amphora their sherds belong to:
- Emporion 2 (the Hephaisteion's garden, the shipsheds' sand) and Route 2 2 (by the kilns, on the spur): Arachne.
- Routes 5 and 6, 3 (the beach ×2, the cape): Hermes.
- Route 4 2 (the shrine, the field edge) and Eleusa 2 (the fields): Persephone.
- Route 3 1 (the thyme meadow) and Aegina 1 (the Aphaia Road): see Open questions 23.
- Kalliste 3 (Kronion Hill, Route 1's terraces, Akti's beach): Kronos.

Each amphora needs four sherds from its own region's spots and fixed finds.

**Boosters.** Phase 2's held boosters are the Silk Scarf (Normal), Soft Sand (Ground), Magnet (Electric), Black Belt (Fighting) and Silver Powder (Bug), for the catches the player leans on.

## Shops

| Where | Stock |
|---|---|
| Emporion, general stall | Poké Ball, Potion, Super Potion, Antidote, Paralyze Heal, Awakening, Burn Heal, Repel, Escape Rope. After `FLAG_BADGE02_GET`: Great Ball, Ice Heal, Super Repel. After `FLAG_ICHOR_FORGE_RELIT`: Charcoal. |
| Emporion, offerings stall | Olive Oil 200, Barley Cake 150, Wine 300, Frankincense 500 (SYSTEMS.md §3 prices) |
| Emporion, scroll stall | TMs: Protect, Rest, Shock Wave, Bulldoze, Round (Balance sets prices) |
| Emporion, Kydon | Honey 300 |
| Emporion, Kedalion (after the forge) | Bronze Votive 400 |
| Emporion, Pasion | Buys Bronze Obol, Silver Owl and Gold Stater at +20% |
| Eleusa, stall | Great Ball, Super Potion, Antidote, Paralyze Heal, Awakening, Repel, Olive Oil, Barley Cake, Honey. After `FLAG_BADGE03_GET`: Revive, Full Heal. |
| Thria, the peddler's cart | Potion, Super Potion, Antidote, Repel, Olive Oil, Barley Cake |

New offering items needed by Phase 2: Olive Oil, Barley Cake, Wine, Frankincense, Bronze Votive (SYSTEMS.md §3). New key items: Alethea's Trowel, Bronze Hammer, Hecate's Torch, Demeter's Sickle, Star Chart, Daedalus's pages I and II, Half Coin, the three Hermes scrolls (temporary, removed at the end of the run).

---

# Part 7. Names introduced

All names are Greek-rooted and clear of the Lazarus avoid-list (no Muse names, no Lazarus places or cast).

| Name | Who or what | Root |
|---|---|---|
| Pronomos | the *Euploia*'s piper | a famous Theban aulos-player |
| Phormion | Sailor | an Athenian admiral |
| Lykon | Merchant | classical name |
| Kerykos | Hierophant of Hermes | *keryx*, herald; the Kerykes, a herald clan of Eleusis |
| Angelos | temple guide, Hermes | "messenger" |
| Podarge, Euchidas, Philonides | Hermes's acolytes | a harpy "swift-foot"; the runner who fetched Delphi's fire; Alexander's courier |
| Halitherses | the augur | the bird-reader of Odyssey 2 |
| Glykera | fish-seller | "sweet"; a New Comedy name |
| Lampis | lamp-seller | a rich Piraeus shipowner; it also sounds like lamps |
| Thaletas | trader | classical name |
| Kedalion | smith | Hephaestus's servant, who carried blind Orion |
| Sykeas | fig-seller | *sykon*, fig |
| Pasion | moneychanger | the famous banker of Piraeus |
| Philoxenos | Emporion's host | "friend of strangers" |
| Strepsiades, Stratyllis, Myrtale | the tavern | Aristophanes's old cheat; Aristophanes's old woman; classical name |
| Aigialeus | old fisher, Halai | "of the shore" |
| Halmyris | salt-worker's grandmother, Halai | "salty" |
| Sagene, Galene | net-maker and daughter, Halai | "drag-net"; "calm sea" |
| Asphalion, Kymon, Krison, Naubolos | Route 5 and 6 trainers | Theocritus's fisherman; "wave"; an Olympic runner; Homeric name |
| Dromokleia | chief runner, Emporion | "glory of the race" |
| Penelopeia | sailor's widow, Emporion | after Penelope, who wove and unwove |
| Euphronios | vase-painter, Emporion | the red-figure master |
| Endeis | innkeeper, Aegina | the wife of Aiakos, Aegina's first king |
| Pheidon | moneyer, Aegina | the king credited with the first coins |
| Aiakides | old soldier, Aegina | "descendant of Aiakos" |
| Myrmex, Sostratos, Euthymia | Aegina detour trainers | "ant"; the richest trader in Herodotus; "good cheer" |
| Kolona | Aegina's headland column | the real site, "column" |
| Aphaia, Mount Oros | the detour's temple and peak | the real sanctuary and summit |
| Kynegeiros | Hoplite, Route 3 | Aeschylus's brother, the hero who grabbed the ship |
| Myrto | Pilgrim, Route 3 | "myrtle", Aphrodite's plant |
| Xerxes's seat, the niches of Aphrodite | Route 3's landmarks | Herodotus 8.90; the real roadside sanctuary |
| Thria | the hamlet | the real deme of the Thriasian plain; the Thriai, pebble-seers |
| Xenokles | innkeeper, Thria | "glory of strangers" |
| Trygaios | farmer, Thria | Aristophanes's farmer in *Peace* |
| Theano | Dysaules's wife, Eleusa | classical name |
| Sitokles | granary-keeper, Eleusa | "grain-glory" |
| Exekias | Potter | the black-figure master |
| Myrrhine | Initiate | "myrtle" |
| Menalkas | Goatherd | Theocritus's herdsman |
| Pheidippos | Runner | after the herald Pheidippides |
| Kapelos | Merchant | "huckster" |
| Eudemos | the procession's leader | "good for the people" |
| Laas, Chalix, Pelos, Bolos, Konis, Gaios | Titanborn grunts | stone, gravel, clay, clod, dust, "of Gaia" |
| Hekabe | Pilgrim | Queen Hekabe, who became Hecate's dog |
| Kallias | Initiate | the Mysteries' torch-bearing family |
| Iambe, Thersites | Jesters | the Hymn's joker; the Iliad's mocker |
| Eunikos | Fisher | classical name |
| Lityerses | Harvester | the reaper who challenged travelers |
| Aristaios | Beekeeper | the hero of beekeeping |
| Krokis | thread-tyer | the Krokonidai, who tied the saffron thread |
| Dysaules | farmer | Triptolemus's father in one telling |
| Eubouleus | Swineherd | the swineherd whose pigs fell with the Kore |
| Euphorion | playwright | Aeschylus's father; Aeschylus was from Eleusis |
| Metaneira | Eleusa's host | the queen who took in the disguised Demeter |
| Doso | temple guide, Demeter | the name Demeter gave in disguise |
| Kallidike, Eumolpos, Melissa | Demeter's acolytes | Keleos's daughter; the Hierophants' clan; "bee" |
| Chloe | Hierophant of Demeter | "green shoot", an epithet of Demeter |
| Rhea | Titan Admin | the bible |
| the Deigma | Emporion's exchange hall | Piraeus's sample hall |
| the Sacred Way | Routes 2–4 | the Hiera Hodos |
| the Rheitoi | Route 4's salt streams | the real streams |
| Halai | the salt hamlet between Routes 5 and 6 | "salt works", an Attic deme |
| Hecate's Hollow, the Hekataion | the cave and its pillar | Hecate's three-faced crossroads pillar |
| the Telesterion, the Anaktoron, the Ploutonion | Eleusa's temple, its inner room, its cave | the real buildings at Eleusis |
| the Maiden's Well | Eleusa's well | the Parthenion of the Hymn |
| the Rharian field | Eleusa's first field | the real sacred field |
| Number Nine, Kydon | Labyrinth seeds | LABYRINTH.md |

---

# Part 8. Flags and vars

Engine: claim these as `FLAG_ICHOR_*`. Phase 2 needs **no new permanent vars**: puzzle state is in `VAR_TEMP_*` and `IchorSave` (SYSTEMS.md §14), and story state is in flags.

**Story**
- `FLAG_ICHOR_WINDS_TURNED`, `FLAG_ICHOR_BOARDED_EUPLOIA`, `FLAG_ICHOR_AEGINA_NIGHT`, `FLAG_ICHOR_CROSSING_DONE`
- `FLAG_ICHOR_SAVED_HALCYON_NEST`, `FLAG_ICHOR_GOT_HALCYLING`, `FLAG_ICHOR_BATTLED_ALETHEA_DECK`
- `FLAG_ICHOR_ARRIVED_EMPORION`, `FLAG_ICHOR_VISITED_EMPORION` (fly)
- `FLAG_ICHOR_RITES_TUTORIAL`, `FLAG_ICHOR_DEIGMA_CLUE`
- `FLAG_ICHOR_FORGE_RELIT`
- `FLAG_ICHOR_KLEON_WON_HERALD`
- `FLAG_ICHOR_HERALDS_RUN_DONE`, `FLAG_ICHOR_HERMES_HERM_J1` … `_J4`
- `FLAG_ICHOR_GOT_TM_AERIAL_ACE`
- `FLAG_ICHOR_KLEON_BATTLE_2_DONE`, `FLAG_ICHOR_WON_KLEON_2`
- `FLAG_ICHOR_ROCKSLIDE_CLEARED`, `FLAG_ICHOR_GOT_PROCESSION_BARLEY`
- `FLAG_ICHOR_SAFFRON_THREAD`
- `FLAG_ICHOR_ARRIVED_ELEUSA`, `FLAG_ICHOR_VISITED_ELEUSA` (fly)
- `FLAG_ICHOR_LESSER_MYSTERIES_DONE`, `FLAG_ICHOR_GOT_TM_GIGA_DRAIN`, `FLAG_ICHOR_CHLOE_RITE`
- `FLAG_ICHOR_PROCESSION_ARRIVED`, `FLAG_ICHOR_MYSTERIES_NIGHT`, `FLAG_ICHOR_SANCTUM_OPEN`
- `FLAG_ICHOR_FOUND_KLEON_SANCTUM`, `FLAG_ICHOR_HELPED_KLEON_SANCTUM`
- `FLAG_ICHOR_FRAGMENT_STOLEN`
- `FLAG_ICHOR_KLEON_LEFT_FOR_ARKADIA`
- `FLAG_ICHOR_DAPHNE_REVELATION`, `FLAG_ICHOR_ACT1_COMPLETE`

**Relics and tools** (per SYSTEMS.md §1: scripts read these, not the bag)
- `FLAG_ICHOR_GOT_TROWEL`, `FLAG_ICHOR_GOT_BRONZE_HAMMER`, `FLAG_ICHOR_GOT_HECATES_TORCH`, `FLAG_ICHOR_GOT_DEMETERS_SICKLE`, `FLAG_ICHOR_GOT_STAR_CHART`

**Systems** (named by SYSTEMS.md and LABYRINTH.md)
- Herms: `FLAG_ICHOR_HERM_ROUTE1` to `_ROUTE6`, and `_AEGINA` (the detour)
- Desecrated altars: `FLAG_ICHOR_ALTAR_CLEANSED_ROUTE2`, `_ROUTE4` (SYSTEMS.md numbers them; these are two of its ~12)
- Gifts I: `FLAG_ICHOR_GIFT_HERMES_I`, `FLAG_ICHOR_GIFT_DEMETER_I`
- Daily prayers: `FLAG_DAILY_ICHOR_PRAYED_HERMES`, `_HECATE`, `_DEMETER`, `_POSEIDON`, `_APOLLO`, `_APHRODITE`, and on the detour `_ARTEMIS` and `_ZEUS` (Phase 2's altars)
- Knucklebones: `FLAG_ICHOR_KNUCKLEBONES_EMPORION`
- Xenia (stretch): `FLAG_ICHOR_SPLIT_COIN_1`, `_2`
- Labyrinth seeds: `FLAG_ICHOR_DAEDALUS_PAGE_1`, `_2`, `FLAG_ICHOR_NUMBER_NINE_UNTIED`
- Amphora leads: `FLAG_ICHOR_HIDE_HOOFPRINTS`, `FLAG_ICHOR_TWELVE_ALTAR_PRAYED`, `FLAG_ICHOR_HOLLOW_RAKNIT`, `FLAG_ICHOR_ELEUSA_PERSENYX`, `FLAG_ICHOR_KRONION_ALTAR_STONE`
- Statics: `FLAG_ICHOR_HECATES_HOUND`

**Gifts**
- `FLAG_ICHOR_GOT_GOOD_ROD`, `FLAG_ICHOR_GOT_QUICK_CLAW`, `FLAG_ICHOR_GOT_WIDOWS_GIFT`, `FLAG_ICHOR_GOT_SYKEAS_FIGS`, `FLAG_ICHOR_GOT_TM_BULLET_SEED`
- Households: `FLAG_ICHOR_PHILOXENOS_LAUREL_2`, `_3`; `FLAG_ICHOR_WROTE_TO_MOM`, `FLAG_ICHOR_GOT_MOMS_HONEY`; `FLAG_ICHOR_EUPHRONIOS_1` to `_3`; `FLAG_ICHOR_GOT_SHELL_BELL`; `FLAG_ICHOR_SHOWED_SAGENE_RAY`; `FLAG_ICHOR_THRIAI_PEBBLE`; `FLAG_ICHOR_FOUND_TRYGAIOS_SOW`; `FLAG_ICHOR_GOT_KYKEON`; `FLAG_ICHOR_GOT_AMULET_COIN`; `FLAG_ICHOR_GOT_BLACK_BELT`
- In-game trades: `FLAG_ICHOR_TRADED_NARKERAY` (Emporion), `FLAG_ICHOR_TRADED_CHELONET` (Aegina), `FLAG_ICHOR_TRADED_GELASABLE` (Thria), `FLAG_ICHOR_TRADED_PITHOUND` (Eleusa). Four new entries in the in-game trade table (`src/data/trade.h`).

**Object hide flags**
- Kleon: `FLAG_ICHOR_HIDE_KLEON_QUAY`, `_SACRED_GATE`, `_TELESTERION`, `_ELEUSA`, `_SANCTUM`
- Alethea: `FLAG_ICHOR_HIDE_ALETHEA_EMPORION`, `_ROUTE2`, `_ELEUSA`, `_SANCTUM`
- Daphne: `FLAG_ICHOR_HIDE_DAPHNE_ELEUSA`
- Kerykos: `FLAG_ICHOR_HIDE_KERYKOS_QUAY`, `_ELEUSA`
- The crossing: `FLAG_ICHOR_HIDE_HALCYON_NEST`, `FLAG_ICHOR_HIDE_DECK_HARPECK`
- Emporion: `FLAG_ICHOR_HIDE_SYKEAS_HARPECK`, `FLAG_ICHOR_HIDE_NUMBER_NINE`
- Route 2: `FLAG_ICHOR_HIDE_ROCKSLIDE_1` … `_3`, `FLAG_ICHOR_HIDE_PROCESSION_ROUTE2`, `FLAG_ICHOR_HIDE_GRUNT_LAAS`
- Route 3: `FLAG_ICHOR_HIDE_TRYGAIOS_SOW`
- Route 4: `FLAG_ICHOR_HIDE_GRUNT_CHALIX`
- Eleusa: `FLAG_ICHOR_HIDE_PROCESSION_ELEUSA` (cleared by `FLAG_ICHOR_PROCESSION_ARRIVED`), `FLAG_ICHOR_HIDE_ELEUTHERAI_VINES`
- Sanctum: `FLAG_ICHOR_HIDE_SANCTUM_GRUNTS`, `FLAG_ICHOR_HIDE_RHEA_SANCTUM`, `FLAG_ICHOR_HIDE_FRAGMENT`, `FLAG_ICHOR_HIDE_BRONZE_SICKLE`, `FLAG_ICHOR_HIDE_CHLOE_SANCTUM`
- Kalliste: `FLAG_ICHOR_HIDE_KRONION_RUBBLE`, `FLAG_ICHOR_HIDE_ROUTE1_THICKET`

**Battle**
- `FLAG_ICHOR_NO_WHITEOUT` (the slice's) for the deck snatchers and Kleon's second battle.

**Temp vars**
- `VAR_TEMP_1`: the Herald's Run, scrolls delivered.
- `VAR_TEMP_2`: the Herald's Run, steps left.

**Save data** (SYSTEMS.md §14): `IchorSave.litBraziers` (the Hollow's 2, the Telesterion's 4, the sanctum's 4, Route 6's Salt Grotto's 2, Akti's grotto's 2: 14 indices), `.herms`, `.favor`, `.blessing`, `.digDaily`, `.sherds`.

**Vanilla flags used:** `FLAG_BADGE02_GET`, `FLAG_BADGE03_GET`, `FLAG_SYS_POKEDEX_GET`, `VAR_STARTER_MON`.

---

# Part 9. Music

Phase 1 has ten Ichor songs (`MUS_ICHOR_*`). Phase 2 needs these. Modes and meters follow PITCH §7.

| Cue | Where | Brief |
|---|---|---|
| `MUS_ICHOR_TRIREME` | the crossing; the ferry | A rowing song: aulos over a steady two-beat stroke, Lydian, bright. **A march variant** for Kleon's stroke: the same tune in Dorian, drum-led, with a chanted LEFT on the downbeat. |
| `MUS_ICHOR_EMPORION` | Emporion City | A market in 7/8 (kalamatianos): kithara, frame drum, a busy Mixolydian line that never quite sits still. |
| `MUS_ICHOR_HERALDS_RUN` | the Temple of Hermes during the run | Fast and light, a ticking ostinato like falling sand; it stops dead when the glass runs dry. |
| `MUS_ICHOR_BATTLE_HIEROPHANT` | Kerykos, Chloe, and every later Hierophant | INVENTORY §8 lists it as needed. Heavier than the trainer theme, in 9/8 (zeibekiko). |
| `MUS_ICHOR_SACRED_WAY` | Routes 2–4, Thria | A processional: slow aulos, hand drums, Dorian, with a far-off chant of "Iakche" in the second phrase. Thria uses it too: a hamlet on the road belongs to the road. |
| `MUS_ICHOR_HALAI` | Routes 5–6, Halai, Aegina's interior | Akti's theme reharmonized for open water and wind, so the coast sounds like home. Aegina Town itself plays `MUS_ICHOR_AKTI`. |
| `MUS_ICHOR_HEARTH_NIGHT` | the inn on Aegina (beat 10B) | Short and quiet: a solo lyre by a fire. It can return for later night-before scenes. |
| `MUS_ICHOR_DARK_CAVE` | Hecate's Hollow, the Salt Grotto, the Kalliste grottos | Near-silence: a low drone and drips. The bark is a sound effect, not music. |
| `MUS_ICHOR_ELEUSA` | Eleusa Village | Pastoral and slow, in Hypodorian: a reaping song with a lyre. |
| `MUS_ICHOR_MYSTERIES` | the Telesterion, the Mystery sanctum | Phrygian, dark: one long held note under faint struck bronze. In beat 22 it falls to the single held note. |
| `MUS_ICHOR_ENCOUNTER_ADMIN` | Rhea's entrance | Her lullaby: a simple cradle song in a minor mode, sung by a solo aulos, slightly out of time. |
| `MUS_ICHOR_BATTLE_ADMIN` | Rhea's battle, and later the other admins | The lullaby's tune turned into a battle theme in 9/8, heavy on low drums. |
| `MUS_ICHOR_LOOM` | Daphne's revelation | The Loom motif: a three-note figure on plucked kithara over a spindle's hum. The Frozen Hour's ticking music box (PITCH §7) should quote it. |

Sound effects needed: a dog's bark with left, right and center panning (the Hollow), a split reed, a herm's stone head turning, a turnstile, the step-glass's last grain, a peep (the chicks), a saffron thread slipping.

---

# Part 10. Art needs per map

Biome tilesets are secondary tilesets on the `aethos` primary (ART_PLAN §1), drawn at 128 px wide and compiled with Porytiles, with palettes planned first.

## Tilesets

| Tileset | Maps | Contents |
|---|---|---|
| `trireme` (interior) | the deck, the hold | Deck planks, the mast and furled or full sail, the bronze ram and the painted eye at the bow, the steering oars and the stern's curl, coils of rope, amphorae lashed down, the hatch; in the hold, three banks of benches with oars. Sea on all sides of the deck, animated. |
| `emporion` | Emporion City | A grid city in marble and limestone: two-story houses with tiled roofs, Ionic and Doric stoas, the Agora's striped awnings and stall counters, rows of pithoi, the moneychanger's table, the long shipsheds with their ramps, the harbor quay with bollards and many moored ships, the harbor wall, the Long Walls, city gates, the Hephaisteion's Doric exterior on its hill, the Temple of Hermes's Ionic facade with a winged frieze, herms. |
| `temple_hermes` | Temple of Hermes | Ionic columns, the winged-runner frieze, three galleries and stairs, bronze turnstiles (four frames), herms with plaques, the dais and its bronze gate, the oil jar and the step-glass. |
| `sacred_way` | Routes 2–4, Thria | The paved Sacred Way, roadside tombs (grave stelai, marble lekythoi, a walled family plot, a burial mound), potters' kilns, terrace ledges, hill scrub (thyme, low oak, rock), the toppled-tomb rubble, the procession's camp (tents, a cart, a cookfire). For Route 3: Aleppo pines in several shapes, switchbacks, the rock seat, the cliff of votive niches, beehives, a ruined watchtower. For Route 4: salt streams, reeds, the stone bridge, a plane tree and spring, a roofed grain shrine, the first wheat. For Thria: a long low inn with a donkey yard, a round house, a farmhouse, a peddler's cart. |
| `halai` | Routes 5–6, Halai | Dune grass and drawn-up fishing boats, tide pools, sea cliffs with snatcher nests, square salt pans and white salt heaps, drying racks, whitewashed huts, a tamarisk, a ruined watchtower, Poseidon's cape shrine. |
| `aegina` | Aegina Town and the detour | Built on `akti`'s harbor pieces plus: a round harbor mole, the Kolona column on its headland, the mint's strongroom front, ant hills, pistachio trees, the Temple of Aphaia's Doric front on a pine hill, Zeus's summit altar. |
| `cave_dark` | Hecate's Hollow, the Salt Grotto, Akti's Sea Grotto, the Kronion Crypt | Limestone cave, the three-faced Hekataion and its torches (lit and unlit), bronze braziers (lit and unlit, 2×2), cobweb curtains, a tide pool; a glow palette copy (SYSTEMS.md §2) for dousing. |
| `eleusa` | Eleusa Village, Route 4's west end | Wheat (tall grass, gold, with a sway animation), threshing floors, poppies, beehives, farmhouses of mud brick and stone, the Maiden's Well and its bench, the dry fig, the Rharian field's fence, the sanctuary wall and Propylaia, the Telesterion's exterior porch, the Ploutonion's rock face and bronze gate, the vine-choked north road. |
| `temple_demeter` | the Telesterion | A dark square hall: a grid of columns, stepped tiers on all four walls, the Anaktoron, four season braziers with plaques, grain pits and their boarded-over state, Hecate's chalk marks; glow palette with the seed, chalk and lamps. |
| `sanctum` | the Mystery sanctum B1F–B3F | Underground granaries: round grain pits, great storage jars, stone stairs, the Hall of the Kore's four fresco panels, the glowing chasm, the iron-tasting basin, the round vault, the bronze chest (open and closed), the Titans' tunnel (open and collapsed); glow palette. |

## Interiors

Every interior is unique (MAP_DESIGN §2): 23 rooms, each laid out for its owner from the room catalogs (`design/phase1/ROOMS_oikia.md`, `ROOMS_civic.md`) on the `building` primary. Each room's character is in its Part 2 entry. The pieces the catalogs probably lack, to be drawn:

| Room | New pieces |
|---|---|
| Emporion's Asclepeion | a wide sea window behind the counter, rope bell-pull, hanging bronze anchors |
| The Deigma | trestle sample tables, a stuffed fish, a scribe's desk |
| The Hephaisteion | forge with bellows (cold and lit), anvil on a stump, quenching trough, tongs rack |
| The Dolphin | dolphin floor mosaic, amphora racks, a worn knucklebones table |
| Philoxenos's house | seven dining couches round a low table, host-greeting mosaic, curtained guest bed |
| The runners' house | straw pallets, paired sandals on pegs, a scratched road map on the wall, finishing ribbon |
| The widow's house | upright loom with a half-finished shroud, oar on the wall, sea window with a stool |
| Euphronios's workshop | potter's wheel, domed kiln with chimney, shelves of drying cups, slip pots |
| Aegina's inn | courtyard cistern, wooden guest gallery, turtle mosaic |
| Aegina's mint | two anvils, coin dies, blank-heating brazier, turtle-stamped chest |
| Aiakides's house | shield and spear trophy, a clay-ant shrine, an anthill in a pot |
| The Inn of the Plain | long trestle hall, sleeping lofts and ladder, an open stable door with a donkey |
| The sisters' house | round room, three stools and three bowls of pebbles, honeycomb shelf, loom-weight chime |
| Trygaios's farmhouse | indoor pig-pen with trough, plough, a Demeter house-shrine |
| Aigialeus's hut | a boat on trestles indoors, nets from the rafters |
| Halmyris's hut | salt jars in rows, a clicking shell curtain, salt rake |
| Sagene's hut | a net stretched across the whole room on a frame, cork-float baskets |
| Eleusa's Asclepeion | courtyard herb garden, herb bundles from the beams, stone mortar, poppy-painted Pithos |
| Eleusa's Agora stall | barley sacks to the ceiling, hanging scale, door-on-barrels counter |
| The house of Keleos | great central hearth, a wooden cradle beside it, worn long table |
| Dysaules's farmhouse | seed jars, a sleeping cat on a sack, a worn stool at a field window |
| The granary-keeper's house | first-fruits tally board, Kore painting, trapdoor and ladder to a grain pit |
| Euphorion's house | wax tablets everywhere, mask wall, a stage chalked on the floor, clay chorus figurines |

## Sprites

| Sprite | Kind | Notes |
|---|---|---|
| Kerykos | portrait, walker | A round, cheerful man in middle age: winged petasos, herald's staff wound with two snakes, a traveling cloak with deep pockets. |
| Chloe | portrait, walker | A woman of about forty in a plain dark himation, a wheat-ear crown, a small bronze sickle at her belt. Still, unreadable. |
| Rhea | portrait, walker | See Part 3. The swaddled stone in the crook of her arm, in both. |
| Alethea | portrait (front) | Needed now for the practice battle; INVENTORY had it for Act II. |
| Kleon | walker frames | Leaning over a rail (seasick); sitting against a column (beaten). |
| The 12 new classes | portraits, walkers | Part 3's table. |
| Pronomos, the lookout, rowers | walkers | Reuse the sailor; Pronomos holds an aulos. |
| Kedalion | walker | A short, broad smith in a leather apron; his apprentice reuses a townsfolk youth. |
| Halitherses | walker | Reuse the augur. |
| Glykera, Kydon, Sykeas, Lampis, Thaletas, stallkeepers | walkers | Reuse the merchant and townsfolk; Kydon's awning carries the bull-leaper. |
| Pasion | walker | Seated at his table, with scales. |
| Man with a lamp | walker | A scruffy old man holding a lit lamp. |
| The procession | walkers | The initiate walker in a group of four or five, plus a pack donkey (Onotis's overworld sprite). |
| Old woman at the Hollow, Doso, Krokis, Metaneira | walkers | Reuse the elder women; Krokis holds a basket of yellow thread. |
| The household occupants: Dromokleia, Penelopeia, Euphronios, Endeis, Pheidon, Aiakides, Xenokles, the three sisters, Trygaios, Aigialeus, Halmyris, Sagene and Galene, Theano, Sitokles, Euphorion, the priestess of Aphaia | walkers | From the 22 townsfolk walkers by palette swap where they fit (runner, elder woman, potter, merchant, soldier, fisher, farmer, child, priestess). Euphronios needs clay-gray hands; the three sisters are one sheet in three palettes. |
| Trygaios's sow, the inn's donkey, Pheidon's tortoise, Aiakides's ants | objects | Kaplet, Onotis and Chelonet follower sprites; a small anthill object |
| Daphne | walker | Exists. |
| Number Nine | object | A wooden kouros, roped (still) and walking (four directions). |
| The herms | object | A herm with a head that faces four ways (the head turns, not the pillar), and a desecrated variant with the sickle scratched in. |
| The halcyon nest | object | A floating seaweed nest with eggs, then hatched, then empty. |
| The Harpe fragment | object | A curved black shard in a rope sling, carried by two grunts. |
| The bronze harvest sickle | object | On the floor, then in Chloe's hand. |
| The saffron thread | small effect | Three frames of a yellow thread falling from a wrist. |
| Pokémon objects | follower sprites | From the dex's own overworld sprites: Harpeck (on an awning; diving), Galenyon (wings spread on the ram), Halcyling ×3 (chicks), Lykopup ×3 (sitting), Kaplet (the kid's piglet), Onotis (the donkey). |

## Battle backgrounds

New: **deck** (planks and open sea), **cave** (dark limestone), **wheat field**, **temple interior, dark** (columns in gloom, for both temples and the sanctum). The slice's grass, beach and temple backgrounds cover the rest.

## Screens

- The **Herald Laurel** and **Harvest Laurel** icons for the laurel case.
- Item icons: the five offerings, the Trowel, the Hammer, the Torch, the Sickle, the Star Chart, the Potsherd, Daedalus's page, the Half Coin, the sealed scroll.
- The **END OF ACT I** card in the pottery frame.
- Map-name steles for every new map.

---

# Systems alignment

Where Phase 2 introduces a SYSTEMS.md or LABYRINTH.md feature, and what the player sees here.

| Feature | Spec | Where in Phase 2 | What the player sees |
|---|---|---|---|
| Rites: altars, prayer, offerings, Favor | SYSTEMS §3 | Kerykos on the quay (beat 11), the Hekataion (beat 18), every temple altar | The altar menu; one sign per god; the offering bag |
| Hierophants teach their god's rite | SYSTEMS §3 | Kerykos (Honey), Chloe (Barley Cake, never a pomegranate) | One line, one free loved offering |
| Desecrated altars | SYSTEMS §3 | Route 2's great herm, Route 4's grain shrine | A sickle scratched in; a Titanborn guard; a prayer cleanses it |
| Herm waystones | SYSTEMS §4 | Routes 1–6, and the Aphaia Road | Anoint with oil; "Somewhere, Hermes makes a note." |
| Relics 2–4 and the prompt | SYSTEMS §1 | Beats 13, 18, 23 | ASK prompts; text never mentions a Pokémon |
| Darkness, lit zones, douse, webs | SYSTEMS §2 | The Hollow, the Telesterion, the sanctum, the grottos | A tile and a half of light, then three and a half; braziers that stay lit; the glow world |
| Excavation | SYSTEMS §5 | The Trowel on the quay (beat 11); dig spots on every map | Turned earth with a glint; sherds; four amphorae's leads |
| The daily augury | SYSTEMS §6 | Halitherses on Emporion's harbor wall | One omen a day, filtered by progress (Part 2) |
| Knucklebones | SYSTEMS §9 | The Dolphin, Emporion | Two regulars and Myrtale |
| Xenia | SYSTEMS §10 | Philoxenos (Emporion), Metaneira (Eleusa); the inns on Aegina and at Thria heal but aren't xenia hosts | "Sit. Eat first." Heal and rest; the Split Coin (stretch) |
| Every house a home | MAP_DESIGN §2 | 15 households and 10 public buildings across Emporion, Aegina, Thria, Halai and Eleusa | A door, an occupant and an event in every one; 4 in-game trades, 3 item swaps, 3 "show me" requests, gifts, a quest, a minigame |
| Theoxenia seeds | SYSTEMS §10 | The Maiden's Well's worn bench; Doso | Nothing yet. Demeter comes after Laurel 5. |
| Temple trial verbs | SYSTEMS §12 | The Herald's Run, the Lesser Mysteries | Part 5 |
| Katasterismoi | SYSTEMS §8 | The Star Chart (beat 25) | A key item; the chart screen is a stretch |
| Labyrinth seeds 3, 4, 5; page II | LABYRINTH §1 | Kydon, Number Nine and Glykera in Emporion; the sanctum's foundations | Part 2 |

---

# Open questions

1. **Map ids and route numbers.** I numbered the mainland routes 2 to 6, continuing Kalliste's Route 1: Routes 2–4 are the Sacred Way's three legs and Routes 5–6 the Halai Shore's two. The geography agent's `AETHOS_MAP.md` may number or prefix them differently; the chains and the connection table in "The route plan" are the parts to reconcile.
2. **Waypoints.** Following the user's "it should feel like we are traveling farther", every stretch has one: Aegina on the voyage, Hecate's Hollow and the hamlet of Thria on the Sacred Way, and Halai on the Halai Shore. The bible fixes the towns; these are hamlets and a cave, so no new Asclepeions or temples. The procession's camp is a rest point on Route 2.
3. **The third starter goes to Alethea** (slice ruling 9 deferred it to Phase 2). It gives her a partner for the Act II double battle and makes the three young leads a triangle: Kleon beats you, you beat Alethea, Alethea beats Kleon.
4. **Kleon wins the race.** He takes the Herald Laurel first and wins the bet he set in the slice, then loses to you at the gate. The alternative is that he loses to Kerykos and you pull ahead. I chose the win because a hollow victory is the start of his hubris.
5. **Kleon fails the Lesser Mysteries** and leaves Eleusa with two laurels, straight for Arkadia's fifth temple. That fits Act II step 2 (he loses badly to Kallisto) but means Phase 3 meets him there out of laurel order.
6. **Alethea's trainer class.** She needs one for the practice battle. I proposed a twelfth class, SCHOLAR, for her alone. She could borrow PILGRIM instead.
7. **The Halcyling gift.** An Act I gift Pokémon from the crossing. It also covers the Kynder player's worst fight (Rhea). The alternative is a catchable static on the rail.
8. **Chloe's ace depends on the clock:** Korantha by day, Persenyx by night, as two trainer entries. It's the only place the main path reads the time, and it changes a team, not progress, so it keeps SYSTEMS.md's principle.
9. **The Titans learn about the player in Act I.** Rhea notices the shard go quiet and says "Iapetos will want to hear about you." This gives Iapetos a reason to seek you out at Thyrsa, and Daphne a reason to tell you now. If the director wants the Titans ignorant until Kaldera, cut her last three lines.
10. **The hum motif.** I read the slice's Amaryllis line ("The humming stopped and they just… went") as the hill going quiet when the player climbed it, and made the Harpe fragment do the same. It's a retcon of intent, not of text.
11. **The saffron thread.** Krokis's thread slipping off is a new clue in the slice's style, one line each time. Cut it if the director wants Halia's spindle to stand alone.
12. **Doso.** The Demeter temple guide shares the name Demeter used in disguise, as a seed for her theoxenia at the well after Laurel 5. It could mislead a myth-savvy player into thinking the guide is the goddess. She has a shadow, which SYSTEMS.md's tells say a god would not.
13. **Kerykos and Chloe are cousins** of Eleusa's herald clan, the Kerykes, and Kerykos calls the holy silence at the Mysteries. This is new backstory for two Hierophants.
14. **The Long Walls Road to Astyra** is closed by the Archon's council in Act I. Phase 3 has to decide what opens it, since Act II reaches Astyra third, after Thyrsa and Arkadia.
15. **Daphne foreshadows the Harpe.** She says it "could cut anything, even what the Fates had spun" and that she doesn't like it sitting beside a child with no thread. Kaldera's reveal (only the unwoven can hold it) stays for Act II. A stricter director could cut those four lines.
16. **Deviations from the dex** (†):
    - Lykopup as Hecate's hound at the Hollow at night. The dex has it in Arkadia only; SYSTEMS.md asked for a Dark-type hound here.
    - Raknit as the web chamber's static, for SYSTEMS.md's Arachne amphora lead. The dex has it in Arkadia and Astyra.
    - Obolorn at 1% on Route 2 at night, among the Sacred Way's tombs. The dex has it in Astyra's Kerameikos; the real Sacred Way began at the Kerameikos.
    - Pebblith on the Halai Shore's cliffs. The dex has it in Kalliste's caves.
    - Every other species is where the dex puts it. Ergant, Kerazap, Cairnolith and Gelasable use the dex's general "mainland" habitats.
17. **Deviations from SYSTEMS.md:**
    - The Lesser Mysteries show only the next seed, rather than all four, and add grain pits in the last quarter.
    - The story's Greater Mysteries are on story time (like the Act II Dionysia), not the calendar's Boedromion festival, which stays a stretch.
    - The temple oil jar refills Olive Oil to 3 for free, so the Herald's Run can't softlock a player who spent their oil.
    - Hecate's Hollow is on the main road (the Sacred Way runs under the pass), so the Torch quest is mandatory, as SYSTEMS.md's gating implies.
18. **The slice's Kalliste tables and starters** still use vanilla species. Under dex decisions D1 and D5 they need an Aethos pass before Phase 2 ships, or the player arrives on the mainland with a Snivy. That pass also rewrites the slice's six starter-specific lines.
19. **Rhea's lullaby and Phaedon's.** LABYRINTH.md makes Phaedon's theme the lullaby Elpis hums. Rhea's encounter theme is also a lullaby. They should be different songs, or the same song on purpose. If the same, it suggests the two grieving parents share something, and the music team should know.
20. **Laurel names.** I used TERMS.md's proposals, the Herald Laurel and the Harvest Laurel.
21. **TMs.** Aerial Ace for Kerykos and Giga Drain for Chloe follow vanilla's Flying and Grass gyms. Balance may rebuild the TM list.
22. **Kleon's second battle uses no-whiteout,** like the first, so both outcomes continue. Rhea's battle is a normal one.

## Decisions for the user

1. **Rhea as the first admin** (Part 3 gives the reasons), with Hyperion feared offscreen.
2. **Alethea gets the third starter** (Open questions 3).
3. **Kleon wins the Herald Laurel first, then fails the Mysteries and goes to Arkadia early** (4, 5).
4. **The Titans learn about you in Act I** (9).
5. **Chloe's ace changes between day and night** (8).
6. **The halcyon chick is a gift** (7).
7. **Two new Act I clues:** the saffron thread and the silent shard (10, 11).

