# Phase 1 script: Kalliste Isle, new game to the Hearth Laurel

Owner: Narrative. Source of truth for scene dialogue, NPCs, trainers, encounters, the hearth trial and item placement in the slice. Map and script agents implement from this file. Where it conflicts with `design/PITCH.md`, the bible wins; see Open questions.

## How to read this file

**Dialogue blocks.**
- Each line is one text box (about 2 lines of 36 characters). A blank line separates boxes.
- `NAME:` opens a speaker's turn. Use the expansion's name box (`include/config/name_box.h`) for named speakers. Unlabelled lines are system or sign text.
- `[brackets]` are stage directions. They are never shown.
- `{PLAYER}` is the player's name. `{STR_VAR_1}` is a species name set by the script.
- Choices are shown as `?? YES/NO` (or a multichoice), followed by `> YES:` and `> NO:` branches.
- The Gen 3 charmap has no em dash and no straight double quote. Dialogue uses `…`, `-` and “ ” only.

**Flags and vars.** Names here are descriptive. The engine team claims the numbers in `include/constants/flags.h` and `vars.h`. Vanilla flags are used where they already do the job: `FLAG_SYS_POKEMON_GET`, `FLAG_SYS_POKEDEX_GET`, `FLAG_SYS_B_DASH`, `FLAG_RECEIVED_RUNNING_SHOES`, `FLAG_BADGE01_GET` and `VAR_STARTER_MON` (0 Snivy, 1 Cyndaquil, 2 Piplup, the order in `src/starter_choose.c`). Trainer-defeated flags are automatic. A full flag and var list is at the end.

**Maps.** The names are the ones already scaffolded: `MAP_ELAIA_VILLAGE`, `MAP_ELAIA_VILLAGE_PLAYERS_HOUSE_1F/2F`, `MAP_ELAIA_VILLAGE_NEIGHBORS_HOUSE`, `MAP_ELAIA_VILLAGE_AKADEMIA`, `MAP_KALLISTE_ROUTE1`, `MAP_AKTI_TOWN`, `MAP_AKTI_TOWN_ASCLEPEION`, `MAP_AKTI_TOWN_AGORA`, `MAP_AKTI_TOWN_FISHERS_HOUSE` and `MAP_AKTI_TOWN_TEMPLE_OF_HESTIA`. I recommend one new map: the summit of Kronion Hill as `MAP_KALLISTE_ROUTE1_KRONION_HILL` (see Open questions).

## The slice in one paragraph

It is the morning of the **Klotheia**, Kalliste's coming-of-age festival, named for Klotho the Spinner. Your mother Melitta sends you to the square, where the old priestess **Halia** reads each youth's thread. Hers is a festival ritual everyone trusts. When she reads yours, her spindle stops turning, and she covers it with a joke. At the Akademia, Professor Daphne gives you the Python, the Typhon or the Trident. Kleon of Lakonia barges in, grabs the starter that beats yours, and battles you in front of the whole festival. On the road north, a flock of Wooloo refuses to move because "the ground is humming" on Kronion Hill. At the summit, two Titanborn are digging the old shrine for a piece of the Harpe. You and Alethea run them off. They drop a tablet that points to "where the grain goes underground". In the harbor of Akti you light Hestia's braziers in the order of her hymn and give the last flame back to the hearth. Then you beat Ione the Hearthkeeper for the Hearth Laurel. The trireme to the mainland can't sail: it is halcyon days, the sea is glassy, and the tide has been running backward at night. You wait for the winds to turn, and Kleon is going to be your shipmate.

The dread under the festival shows in these places, each kept to one line:
- Halia's stopped spindle.
- Mom's half-memory of the Oracle's blind hour.
- Silver olives.
- The Augur's "wrong" birds.
- The hum on Kronion Hill.
- The tide running backward.
- The Pythia answering in single words.

---

# Part 1. Scenes, beats 0–8

## Beat 0. Professor Daphne's new-game speech

This replaces `data/text/birch_speech.inc`, string by string, so `src/main_menu.c` needs no logic changes. Swap the intro species `SPECIES_LOTAD` for **`SPECIES_SMOLIV`** in both places in `main_menu.c` (lines ~1371 and ~1871). Myth link: someone once saw a Smoliv and told the story of Athena giving a city its first olive tree. That is the thesis of the whole game in one Pokémon.

For the gender screen, the two sprites are Theo and Ianthe. The menu can keep BOY/GIRL or be relabelled THEO/IANTHE; that is the engine team's call. Name entry already defaults to Theo/Ianthe (commit 73b2d57).

`gText_Birch_Welcome`
```text
DAPHNE: Ah, there you are. Sit, sit. The grass is dry today.

Welcome to Aethos. Land of heroes, of olive groves, and of Pokémon.

I'm Daphne. People call me a professor. I prefer “curious.”
```

`gText_Birch_Pokemon` (Smoliv pops out)
```text
DAPHNE: This is a Pokémon. Say hello, Smoliv.
```

`gText_Birch_MainSpeech`
```text
DAPHNE: Aethos is full of creatures like this one.

We farm with them. We fish with them. Some of us fight beside them.

And we tell stories about them. We always have.

A serpent so huge a god had to slay it. A giant breathing fire.

A trident that could split the sea in two.

I think every myth is a memory of a Pokémon.

Someone saw one, once, and simply couldn't stop talking about it.

I study those memories. It's mostly walking. Some digging.

And a great deal of being wrong, which is the best part.
```

`gText_Birch_AndYouAre`
```text
DAPHNE: Now. Who's this standing in my grove?
```

`gText_Birch_BoyOrGirl`
```text
DAPHNE: Which of these two is you?
```

`gText_Birch_WhatsYourName`
```text
DAPHNE: And what do they call you?
```

`gText_Birch_SoItsPlayer` (yes/no confirm)
```text
DAPHNE: {PLAYER}. Have I got that right?
```

`gText_Birch_YourePlayer`
```text
DAPHNE: {PLAYER} of Elaia! Melitta's child. I should have guessed.

You have her chin. The stubborn one.
```

`gText_Birch_AreYouReady`
```text
DAPHNE: Today is the Klotheia, when Kalliste's youths come of age.

Your thread gets read. You get a partner. Then the road opens up.

Come find me at the Akademia. I'd like you to meet someone.

Three someones, actually.
```
[Fade to white. The player wakes in `MAP_ELAIA_VILLAGE_PLAYERS_HOUSE_2F` at (5,5), as already wired in `src/new_game.c`.]

---

## Beat 1. The player's house, festival morning

### 1A. Player's room (2F)

[The player starts by the bed. Nothing auto-plays. The furniture re-skins are listed in the NPC roster below.]

**Stair gate.** A coord event sits on the tile in front of the stairs while `FLAG_ICHOR_SET_WATER_CLOCK` is unset.
```text
MOM: [offscreen] {PLAYER}! Did you fill your water clock?

MOM: [offscreen] Festival day! You can't be late on festival day!
```
[The player steps back one tile.]

**Water clock.** This is a bg event on the wall clock. It runs vanilla `special StartWallClock`.
```text
Your klepsydra. Water drips from the top bowl to the bottom one.

It's run dry. Better fill it and set the hour.
```
[Clock UI. On exit, set `FLAG_ICHOR_SET_WATER_CLOCK`.]
```text
Drip… drip… drip. Good as new.
```

### 1B. Downstairs with Mom (1F)

[Trigger: arriving on 1F from the stairs with `FLAG_ICHOR_SET_WATER_CLOCK` set and `FLAG_ICHOR_TALKED_TO_MOM` unset. Mom stands at the hearth. She shows "!", walks up to the player and stops facing them.]
```text
MOM: There you are! Festival morning, and you slept like a stone.

MOM: Let me look at you. …Hm. You'll do.

MOM: Today's the Klotheia. Every youth on Kalliste comes of age today.

MOM: First, old Halia reads your thread. She's in the square.

MOM: Then Daphne gives you a partner at the Akademia. A Pokémon!

MOM: Oh! Before I forget. These are for you.
```
[Give the Talaria. Set `FLAG_SYS_B_DASH` and `FLAG_RECEIVED_RUNNING_SHOES`. Item-get fanfare.]
```text
{PLAYER} received the Talaria!

MOM: New sandals for a new road. The cobbler stitched wings on them.

MOM: He says they're for luck. Hold the B Button and you'll see.

MOM: …

MOM: I remember the night you came, you know. Like it was last week.

MOM: A pilgrim passed through that spring. He swore something odd.

MOM: That the Oracle at Delphoi went blind for an hour that night.

MOM: Or the night before. Or the week after. You know pilgrims.

MOM: Anyway! Go. Halia hates waiting, and Daphne hates it worse.
```
[Mom walks back to the hearth. Set `FLAG_ICHOR_TALKED_TO_MOM`.]

Mom's later lines and her heal offer are in the NPC roster.

---

## Beat 2. The festival square: Halia reads the threads

**Setup.** Halia sits under a striped canopy at the foot of the old olive tree, in the middle of the square. In front of her stand two youths in line: Korinna in front, then Philon. While `FLAG_ICHOR_THREAD_READ` is unset, a row of coord triggers runs across the square's southern and western approaches, two tiles from the line.

[Halia looks up. A "!" appears over her.]
```text
HALIA: You! Melitta's child. Don't dawdle, get in line.
```
[The player walks to the tile behind Philon and faces up. Halia lifts her spindle. Play a soft chime (SE_SHINY or similar) while it turns.]
```text
HALIA: Korinna. Hold out your hand.

HALIA: …Long and bright. You'll argue with everyone.

HALIA: And you'll be right about half the time.

KORINNA: Only half?

HALIA: Half is a great deal, child. Next!
```
[Korinna walks 3 tiles west and stops facing the garland tree. Philon steps up 1 tile.]
```text
HALIA: Philon. Your hand.

HALIA: …A strong thread. A knot near the start.

PHILON: Is that bad? Is the start now? It feels like now.

HALIA: Every thread has knots. You'll pull through. Next!
```
[Philon walks 3 tiles east. The player steps up 1 tile. The spindle chime plays, slows, and cuts off. Hold for 60 frames with no text.]
```text
HALIA: Hold out your hand, {PLAYER}.

HALIA: …

HALIA: Hm.

HALIA: The light's poor under this canopy. Turn around.
```
[The player turns left, then right, then up.]
```text
HALIA: …Again.
```
[The player turns left, right, up again.]
```text
HALIA: …Well. It seems your thread is your own business.

HALIA: Nervous?
```
?? YES/NO
```text
> YES:
HALIA: Good. Only fools aren't, and fools fall off cliffs.

> NO:
HALIA: Liar. Good. You'll need that.
```
```text
HALIA: Go on, the Akademia. Daphne's been pacing since dawn.

HALIA: And {PLAYER}… come see me after the festival.

HALIA: My eyes are tired today. I'd like another look.
```
[Set `FLAG_ICHOR_THREAD_READ`. This also clears the note on the Akademia door; see beat 3.]

**Design note.** Halia never says "blank" or "empty". Two clues stand: the spindle stops, and "your thread is your own business", which reads one way now and another after Act I step 5. Don't add more.

---

## Beat 3. The Akademia: Daphne, Alethea and the three

**Door gate.** While `FLAG_ICHOR_THREAD_READ` is unset, a coord event on the Akademia door tile shows this and steps the player back:
```text
A note is pinned to the door:

“Thread first. Then Pokémon. Halia's rule, not mine. -D.”
```

**Inside.** Daphne stands behind the long table at the top of the room. On the table are three painted kraters (wide clay bowls), one starter in each. Alethea is cataloguing scrolls at the shelves on the right.

[Trigger: the first step inside with `FLAG_ICHOR_GOT_STARTER` unset. Alethea turns, shows "!" and walks 2 tiles toward the player.]
```text
ALETHEA: There you are! Halia took ages, didn't she?

ALETHEA: Mine took three minutes. She said I'm “exhausting.”

ALETHEA: Professor! {PLAYER}'s here.
```
[Alethea returns to the shelves. Daphne turns around. The player walks up until they are 2 tiles below the table.]
```text
DAPHNE: {PLAYER}! Come in. Mind the scrolls, they bite.

DAPHNE: Before anything else, a question. Humor me.

DAPHNE: Which came first? The Pokémon, or the story?
```
?? Multichoice: THE POKéMON / THE STORY
```text
> THE POKéMON:
DAPHNE: That's my answer too. I'd love to be wrong, though.

> THE STORY:
DAPHNE: Ha! A heretic. Wonderful. Alethea, write that down.

ALETHEA: I am not writing that down.
```
```text
DAPHNE: Now. Every year a few youths go home with a partner.

DAPHNE: These three came to me this spring. They chose to come.

DAPHNE: I think they've been waiting for someone. Have a look.
```

**Choosing.** The engine team picks the method.
- **Option A (recommended):** `special ChooseStarter` (the starter-select screen). Repaint the bag as three kraters later.
- **Option B:** FRLG-style. Interact with each krater and get a yes/no.

For Option B, the krater texts are:
```text
SNIVY: A Grass Pokémon. It looks at you as if you owe it money.

CYNDAQUIL: A Fire Pokémon. Its back crackles when it sneezes.

PIPLUP: A Water Pokémon. It is trying very hard to stand up straight.

Will you take {STR_VAR_1}?
```
After either method, Daphne says the line for your choice:
```text
> VAR_STARTER_MON == 0 (Snivy):
DAPHNE: Snivy. Grown, it's the great serpent that guarded Delphoi.

DAPHNE: Apollo himself had to shoot it. Don't tell it. It's vain enough.

> == 1 (Cyndaquil):
DAPHNE: Cyndaquil. Raise it well and it becomes Typhon's fire.

DAPHNE: Father of monsters, the old poets said. Raise it kindly.

> == 2 (Piplup):
DAPHNE: Piplup. One day it'll wear a trident on its brow, like the sea-god.

DAPHNE: For now it mostly falls over. With great dignity.
```
[Vanilla nickname prompt. Set `FLAG_ICHOR_GOT_STARTER` and `FLAG_SYS_POKEMON_GET`. Hide the chosen krater: `FLAG_ICHOR_HIDE_KRATER_<SPECIES>`.]
```text
DAPHNE: And take this. It's a Pokédex.

DAPHNE: Every Pokémon you meet, it remembers. Better than I do.
```
[Give the Pokédex and set `FLAG_SYS_POKEDEX_GET`.]
```text
{PLAYER} received the Pokédex!

ALETHEA: I built most of it. She argued with all of it.

DAPHNE: That's called collaboration.
```

### Kleon arrives

[Door SE. Kleon walks in from the door, 4 tiles up, and stops one tile left of the player, facing the table. Play Kleon's encounter music.]
```text
KLEON: Professor Daphne! Kleon of Lakonia. Here for the games.

KLEON: Your herald said visitors could have a partner too.

DAPHNE: My herald said visitors could ask.

KLEON: I'm asking.
```
[Kleon turns to face the player. Short pause.]
```text
> VAR_STARTER_MON == 0:
KLEON: A Snivy? Then I want the fire one. Fire eats grass for breakfast.

> == 1:
KLEON: Fire, huh? Then the little sea-bird's mine.

Water puts out fire.

> == 2:
KLEON: The bird? Then I'll take the snake. Roots drink the sea dry.
```
[Kleon steps to the table. The krater he takes disappears. Hide flag as above.]
```text
KLEON: Thanks, Professor! You won't regret this. Well. You might.

KLEON: You. {PLAYER}, right? Outside. The square.

KLEON: Everyone should see this.
```
[Kleon walks out. Set `FLAG_ICHOR_KLEON_TOOK_STARTER`.]
```text
DAPHNE: …Well. At least he asked.

ALETHEA: He did not ask.

DAPHNE: Go on, {PLAYER}. A battle is only a question, louder.

DAPHNE: The last krater stays with me. Someone always comes late.
```

---

## Beat 4. Elaia: the first battle with Kleon

**Setup.** This needs `FLAG_ICHOR_KLEON_TOOK_STARTER` set and `FLAG_ICHOR_KLEON_BATTLE_1_DONE` unset. Kleon stands in the open middle of the square, south of Halia's canopy. A loose ring of watchers stands around him: Korinna, Philon, the festival-goers and Elder Gylippos. A coord trigger sits on the row just north of the Akademia door.

[Kleon faces the player. The watchers turn to face the player.]
```text
KLEON: There you are! Everyone, watch this.

KLEON: I'm Kleon. Lakonian. Raised in the battle school.

KLEON: When I was born, the Oracle told my mother something.

KLEON: That I'd die young. And glorious.

KLEON: So I'm in a hurry. Glory first. The dying part can wait.

KLEON: Battle me?
```
?? YES/NO
```text
> YES:
KLEON: Ha! Good.

> NO:
KLEON: That wasn't really a question.
```
[Set the no-whiteout flag (`B_FLAG_NO_WHITEOUT` → `FLAG_ICHOR_NO_WHITEOUT`). Start `trainerbattle_no_intro` with the trainer chosen by `VAR_STARTER_MON`: 0 → `TRAINER_ICHOR_KLEON_ELAIA_CYNDAQUIL`, 1 → `TRAINER_ICHOR_KLEON_ELAIA_PIPLUP`, 2 → `TRAINER_ICHOR_KLEON_ELAIA_SNIVY`. Afterwards, clear the no-whiteout flag and branch on `specialvar VAR_RESULT, GetBattleOutcome`.]

Defeat text (the in-battle line when Kleon loses):
```text
KLEON: Wait, what? Do-over! Lakonians get do-overs! …No, we don't.
```
```text
> Player won (set FLAG_ICHOR_WON_KLEON_1):
KLEON: Huh. …Lucky.

KLEON: No. Fair. You beat me. Remember it. It won't happen twice.

> Player lost:
KLEON: Ha! See? Glory. It follows me around like a hungry Wooloo.

KLEON: Don't make that face. You'll get me next time. Probably not.
```
```text
KLEON: I'm off to Akti. The Hearthkeeper has a laurel with my name on it.

GYLIPPOS: Kleon.

KLEON: Yes, Elder?

GYLIPPOS: Fewer words.

KLEON: …Right. Bye!
```
[Kleon runs north and off the map at the Route 1 exit. Hide him: `FLAG_ICHOR_HIDE_KLEON_ELAIA`. The watchers return to their posts. Alethea comes out of the Akademia door, walks up and faces the player.]
```text
ALETHEA: I watched from the window. Here, let me see them.
```
[Run `special HealPlayerParty` with the heal jingle.]
```text
Alethea tended to your Pokémon.

ALETHEA: And take these. You'll want to catch a few friends.
```
[Give `ITEM_POKE_BALL` ×5 and set `FLAG_ICHOR_GOT_POKEBALLS`.]
```text
{PLAYER} received 5 Poké Balls!

ALETHEA: Weaken a wild one first, then throw. Not at Kleon. I checked.

ALETHEA: I'm heading up Kronion Hill, to the old shrine.

ALETHEA: Something's been digging up there at night. Big holes.

ALETHEA: The road to Akti runs right past it. Come find me?
```
[Alethea walks north and off the map. Set `FLAG_ICHOR_KLEON_BATTLE_1_DONE` and `FLAG_ICHOR_HIDE_ALETHEA_ELAIA`. The old shepherd at the north exit steps aside.]

---

## Beat 5. Route 1 and Kronion Hill

**Road block.** Amaryllis's flock blocks the Akti road: 3–4 Wooloo object events across the road, just north of the spur up to Kronion Hill. While `FLAG_ICHOR_RUINS_CLEARED` is unset, talking to any of them gives:
```text
WOOLOO: Baaa. [It plants its hooves and does not move.]
```
Amaryllis's lines are in the roster. The spur to the hill is open. Polyeidos the Augur watches it from a rise, and his line covers the whole spur (trainer, roster below).

### The summit cutscene

**Setup.** Alethea stands at the lip of a fresh dig pit in front of the broken altar. The two Titanborn, Petros and Amathos, stand inside the pit with shovels, facing the altar. A coord trigger is placed 4 tiles from the pit as the player tops the stair. The scene needs `FLAG_ICHOR_RUINS_CLEARED` unset.

[A low rumble SE. Shake the screen for about 30 frames. Then Alethea turns.]
```text
ALETHEA: {PLAYER}! Good timing. Did you feel that?

ALETHEA: These two have been digging up the shrine all morning.
```
[The grunts turn around. Their bronze helmets catch the light.]
```text
PETROS: Dig site's closed, kid. Titanborn business.

AMATHOS: We're only taking back what belongs to our lord.

ALETHEA: Nothing here belongs to you. That stone's ancient.

PETROS: Yeah. That's the point.

ALETHEA: I'm a scholar, not a brawler. {PLAYER}, help?
```
[Petros climbs out of the pit and walks up to the player. Battle 1, `TRAINER_ICHOR_GRUNT_RUINS_PETROS`, with `trainerbattle_no_intro`. His defeat and post lines are in the trainer section. Then Amathos climbs out. Battle 2, `TRAINER_ICHOR_GRUNT_RUINS_AMATHOS`.]
```text
AMATHOS: Fine. FINE. There's nothing down there anyway.

PETROS: Nosepass hasn't twitched once. I told you it was wrong hill.

AMATHOS: Stop talking about the Nosepass.

PETROS: Hyperion's going to roast us.

AMATHOS: He'll roast us literally. Move!
```
[Both run down the far side and off the map. A clay tablet object appears where Amathos stood: `FLAG_ICHOR_HIDE_TITAN_TABLET` is cleared. Alethea walks to it, faces down and "picks it up". Hide the tablet. Set `FLAG_ICHOR_FOUND_TITAN_TABLET`.]
```text
ALETHEA: They dropped this. A clay tablet. Sickle stamped on top.

ALETHEA: It's a list of places. “Kalliste” is scratched out.

ALETHEA: Then: “The fragment of the Harpe lies…

…where the grain goes underground.”

ALETHEA: A riddle. I hate riddles. They're just lies wearing hats.

ALETHEA: …And at the bottom: “Last, the house of the double axe.”

ALETHEA: That's not a riddle. That's just rude.

ALETHEA: The Harpe… that's Kronos's sickle. From the old stories.

ALETHEA: The one he used to overthrow his own father.

ALETHEA: Why would anyone dig for a story?

ALETHEA: …Unless it isn't one.
```
[Pause. Alethea shakes it off.]
```text
ALETHEA: Here. Take my old Augur's Eye. I built a better one.
```
[Set `FLAG_ICHOR_DEXNAV_GET`, which already exists. The Augur's Eye now shows in the start menu.]
```text
{PLAYER} received the Augur's Eye!

ALETHEA: Augurs read birds. This reads grass. Want the short version?
```
?? YES/NO
```text
> YES:
ALETHEA: Open it from your menu. Pick a Pokémon you've already seen.

ALETHEA: It'll show you where one's hiding. Creep up slowly.

ALETHEA: Pokémon hate being stared at. So do I, for the record.

> NO:
ALETHEA: Good. I'd have explained it badly. Truthfully, but badly.
```
```text
ALETHEA: I'm taking this tablet to Daphne. You go on to Akti.

ALETHEA: The Hearthkeeper's waiting. I'll catch up. I'm fast.

ALETHEA: That's a lie, actually. I'm slow. But I'll catch up.
```
[Alethea walks down the stair and off the map. Set `FLAG_ICHOR_RUINS_CLEARED` and `FLAG_ICHOR_HIDE_ALETHEA_RUINS`. Hide the grunts. With them gone, the pit's floor shows cut steps going down into the dark (the dark stair, a relic gate for Hecate's Torch; no text). On Route 1, the flock's hide flag `FLAG_ICHOR_HIDE_ROUTE1_FLOCK` is set on the map transition, so the road is open.]

---

## Beat 6. Arriving in Akti

**Setup.** This plays once, on the first step into Akti from the south road. It sets the fly/visited flag and `FLAG_ICHOR_ARRIVED_AKTI`. Diktys the net-mender sits on an upturned boat near the south gate. He gets up, walks 2 tiles to the player and faces them.
```text
DIKTYS: A traveler! From the festival, by the look of those sandals.

DIKTYS: Welcome to Akti. Here's the whole town in one breath:

DIKTYS: Asclepeion on your left, for tired Pokémon.

DIKTYS: Temple of Hestia on your right, for tired challengers.

DIKTYS: Agora up the hill. And the sea straight ahead. Can't miss it.

DIKTYS: I tried once. Fell right in.
```
[Diktys walks back to his boat. Run `setrespawn HEAL_LOCATION_AKTI_TOWN` at the Asclepeion's first heal, not here.]

---

## Beat 7. The Temple of Hestia

See Part 4 for the full trial. Scene text for the entry, the acolytes and Ione is here and in the trainer section.

**Entry.** The temple guide Euboulos stands just inside the door. This is the gym-guide re-skin.
```text
EUBOULOS: Welcome, guest. In Hestia's house, every stranger is a guest.

EUBOULOS: The Hearthkeeper will see you once the house is warm.

EUBOULOS: Read the hymn on the stele. Then carry the fire as it says.

EUBOULOS: Lampon keeps the great hearth. Prove yourself to him first.
```
After `FLAG_BADGE01_GET`:
```text
EUBOULOS: The house is warm, and so are you. Hestia keep you, guest.
```

**Ione's scene.** This needs `FLAG_ICHOR_HEARTH_TRIAL_DONE`. Ione stands on the dais behind the inner hearth, facing down. Talk to her.
```text
IONE: Come in, come in. Sit by the fire. You look half frozen.

IONE: You carried the flame well. The house is warm because of you.

IONE: I'm Ione. I keep this hearth, as my mother did, and hers.

IONE: Have you eaten? No? Afterward, then. I feed everyone either way.

IONE: A hearth isn't the fire, you know. It's what you come back to.

IONE: Every house has a guard, a hungry mouth, and a flame.

IONE: Let me show you mine.
```
[Battle `TRAINER_ICHOR_IONE_1`. Her defeat text:]
```text
IONE: There. Warm all the way through.
```
[After the battle:]
```text
IONE: Well fought. Hestia doesn't hand out her fire to just anyone.

IONE: Take this. The Hearth Laurel. The first leaf of your crown.
```
[Set `FLAG_BADGE01_GET`. Badge fanfare.]
```text
{PLAYER} received the Hearth Laurel from Ione!

IONE: And this. Facade. A hearth burns hotter when it's fed.

IONE: Hurt, burned or poisoned, it hits twice as hard. Hardship is fuel.
```
[Give `ITEM_TM42` (Facade) and set `FLAG_ICHOR_GOT_TM_FACADE`.]
```text
{PLAYER} received TM42, Facade!

IONE: Halia sent word that you'd come. Her gull beat you by an hour.

IONE: She said you'd come. She didn't say how it would go.

IONE: That isn't like her. Halia always says how it'll go.

IONE: Ah, but you won. So it went well. Now, eat something.
```
After the laurel (repeat talk):
```text
IONE: The trireme sails for the mainland when the winds turn.

IONE: Kerykos keeps the temple at Emporion. He'll talk your ear off.

IONE: Come back whenever you're cold. The door doesn't lock.
```

**Design note on the myth.** Kronos swallowed Hestia first and gave her up last, which is why she takes the first and last of every offering. It lives in the hymn and the trial and is never explained. Only Aithra says it aloud, once, as a half-joke (see the trainers).

---

## Beat 8. The harbor: when the winds turn

**Part 1.** This needs `FLAG_BADGE01_GET` set and `FLAG_ICHOR_SLICE_COMPLETE` unset. A coord trigger sits on the tile outside the temple door. Alethea runs in from the south road and stops in front of the player. Clear `FLAG_ICHOR_HIDE_ALETHEA_AKTI`.
```text
ALETHEA: {PLAYER}! You did it! Let me see the laurel.

ALETHEA: …It smells like woodsmoke. And soup?

ALETHEA: I showed Daphne the tablet. She went very quiet.

ALETHEA: She thinks “where the grain goes underground” means Eleusa.

ALETHEA: On the mainland. Where they keep the Mysteries.

ALETHEA: So, truthfully? We need a ship. Come on, the quay!
```
[Alethea walks to the quay, about 8 tiles north. The player is released and follows. A second coord trigger on the quay plays Part 2. Captain Nausikles stands at the trireme's gangplank. Kleon and a Lakonian rower stand beside him.]
```text
ALETHEA: Captain! Two for the mainland. Emporion, please.

NAUSIKLES: Gladly. The Euploia sails the moment the winds turn.

ALETHEA: And when will that be?

NAUSIKLES: Ha! It's halcyon days, girl. The kingfishers are nesting.

NAUSIKLES: Aeolus keeps the sea flat as a plate until they're done.

NAUSIKLES: A few days. A week. Ask the birds, not me.

NAUSIKLES: Strange year, though. They nested early.

NAUSIKLES: And the tide's been running backward at night. Never seen it.
```
[Kleon turns to face the player.]
```text
KLEON: A week?! I'll have beaten Ione three times by then.

KLEON: …You've got the laurel. Already.

KLEON: Of course you do.

KLEON: Fine. I'll win mine tomorrow. Then we race to the mainland.

KLEON: First to the next laurel wins. Deal?
```
?? YES/NO
```text
> YES:
KLEON: Ha! Deal. Try to keep up, shipmate.

> NO:
KLEON: Too bad. It's a deal anyway. Lakonians don't take “no.”
```
[Kleon walks off toward the Asclepeion. The player turns to face the sea, north. Hold for 60 frames.]
```text
The ribbon on the trireme's mast hangs perfectly still.

Across the flat water, the mainland waits.
```
[Set `FLAG_ICHOR_SLICE_COMPLETE`. For the playtest build: fade to black, then show the line below, then return to the overworld so the player can keep catching and fishing.]
```text
Thank you for playing the Kalliste preview of Pokémon Ichor.
```

---

# Part 2. NPC rosters

Lines are listed by condition, earliest first. A later condition replaces earlier lines. Unnamed NPCs are fine as roles. Overworld palette families are a Sprites decision; the suggested sprites are vanilla placeholders.

## Elaia Village (outdoors)

Layout reference, from the scaffold: the player's house door is at (5,8), upper left; Kydippe's house at (14,8), upper right; the Akademia at (7,16), south; the Route 1 exit is north. The festival square is the open middle, with the old olive tree and Halia's canopy at its center. Map builders should add a stone well on the square's east side and Melitta's beehives behind the player's house.

| NPC | Where | Role |
|---|---|---|
| Halia | under the canopy by the old olive | island priestess, reads threads |
| Korinna | in line by the canopy (beat 2), then by the garland tree | youth, sharp-tongued |
| Philon | in line (beat 2), then east of the canopy | youth, nervous, Kydippe's grandson |
| Olive farmer | by the olive press, east | old farmer |
| Festival-goer (woman) | by the garlanded tree, west | Oracle gossip |
| Festival-goer (man) | by the footrace finish line, south of the square | race gossip |
| Gylippos | west edge of the square | Lakonian elder |
| Kid with Wooloo | near the well | comic |
| Old shepherd | north exit | gate |
| Kleon, Alethea | beat 4 only | — |
| Glykera, Kimon | at home, in the house west of the square | see "Glykera's house" below |
| Traveling scribe | at the square's west edge by the altar, at his stool; from the morning through beat 4 | a visitor who collects fortunes (secretly Iapetos, `design/STORY.md` §8.2) |

**Halia**
```text
> after FLAG_ICHOR_THREAD_READ:
HALIA: Come back after the festival. My eyes are tired today.

> after FLAG_ICHOR_GOT_STARTER:
HALIA: Daphne found you a partner? Good.

HALIA: Whatever's on your thread, you won't walk it alone.
```

**Korinna**
```text
> before FLAG_ICHOR_THREAD_READ:
KORINNA: I'm next. I'm not nervous. Why would I be nervous. Stop looking.

> after:
KORINNA: Right half the time! I'm choosing to hear that as a compliment.

KORINNA: What did she say about yours? …She said nothing? Huh.
```

**Philon**
```text
> before FLAG_ICHOR_THREAD_READ:
PHILON: Grandma says Halia's never wrong. That's the scary part.

> after FLAG_ICHOR_THREAD_READ, before FLAG_ICHOR_GOT_STARTER:
PHILON: A knot near the start. Is the start today? It feels like today.

> after FLAG_ICHOR_GOT_STARTER:
PHILON: Daphne gave me a Wooloo. It sat on me. I think that means yes.
```

**Olive farmer**
```text
OLIVE FARMER: Best harvest in years. Every tree came in silver.

OLIVE FARMER: My father used to say silver olives mean something's watching.

OLIVE FARMER: He also said that about clouds. And goats.
```

**Festival-goer (woman)**
```text
FESTIVAL-GOER: My sister sailed all the way to Delphoi to ask the Oracle.

FESTIVAL-GOER: “Will my baby be a boy?” The Oracle said, “Yes and no.”

FESTIVAL-GOER: Twins. One of each. The Oracle's never wrong. Just rude.
```

**Festival-goer (man)**
```text
> before FLAG_ICHOR_KLEON_BATTLE_1_DONE:
FESTIVAL-GOER: The Lakonian boy won the footrace by three lengths.

FESTIVAL-GOER: Then he challenged the finish line to a rematch.

> after:
FESTIVAL-GOER: Best match of the festival! Better than the footrace.
```

**Gylippos (Lakonian elder)**
```text
> before FLAG_ICHOR_KLEON_BATTLE_1_DONE:
GYLIPPOS: Lakonians speak little.

GYLIPPOS: …

GYLIPPOS: That was the conversation.

> after:
GYLIPPOS: The boy talks enough for all of Lakonia. Someone must.
```

**Traveling scribe.** He is Iapetos, unrecognizable: the first sighting of his hook (`design/STORY.md` §8.2). He stands at his stool by the altar from the morning until the end of beat 4, then slips away with the festival crowd: set `FLAG_ICHOR_HIDE_SCRIBE`, and the stool goes too. Name box: SCRIBE.
```text
> before FLAG_ICHOR_THREAD_READ:
SCRIBE: Don't mind me. I collect fortunes. For a book.

> after FLAG_ICHOR_THREAD_READ:
SCRIBE: Yours stopped her spindle. In forty years, she says. Never once.

SCRIBE: May I tell you something true? You're going to be in my book.

[Object: the scribe's stool, while he is there]
A wax tablet on a stool. Neat writing. Every line ends in a little hook.
```

**Kid with Wooloo** (with a Wooloo object event beside them)
```text
KID: My Wooloo ate the festival garland. Don't tell Halia.

WOOLOO: Baa! [It has a flower behind its ear.]
```

**Old shepherd (north exit gate).** While `FLAG_ICHOR_GOT_STARTER` is unset, a coord trigger on the exit row runs this, and the player steps back:
```text
OLD SHEPHERD: Whoa there. The grass is thick with Pokémon today.

OLD SHEPHERD: Nobody walks that road without a partner. Go see Daphne.
```
After the starter he stands beside the road:
```text
OLD SHEPHERD: Off you go, then. Mind the tall grass. And the goats.
```

**Signs**
```text
[Village sign, south of the square]
ELAIA VILLAGE
Where the olives grow silver.

[Player's house]
{PLAYER}'s house. Honey for sale. Ask Melitta.

[Kydippe's house]
KYDIPPE, MIDWIFE. Knock loudly. Louder than that.

[Akademia]
THE AKADEMIA
Professor Daphne's grove. Questions welcome. Answers not promised.

[Festival banner, by the canopy]
THE KLOTHEIA
Today Kalliste's youths come of age. Threads read under the old olive.

[Herm at the north exit, a road-pillar of Hermes]
A herm stands by the road.
North: Route 1, Akti Town.

[The honey-cake stall in the square]
Glykera's honey cakes, still warm. She's run home to bake another batch.
```

**Hidden items and objects.** See Part 5.

## Player's house 2F (the player's room)

| Object | Re-skins | Text |
|---|---|---|
| Wall clock | klepsydra (water clock) | Beat 1A. Afterwards: "Drip… drip… The water says it's still today." |
| PC | wooden chest, item storage | "Your kibotos. Spare gear and keepsakes go in here." Then the vanilla item-storage menu, which starts with a Potion. |
| GameCube / TV | knucklebones set | "Your knucklebones. Record against Mom: 0 wins, 212 losses." |
| Window | — | "Bees drift past. Down in the square, someone's tuning a lyre." |
| Bookshelf | — | "Scrolls about heroes. You've drawn mustaches on all of them." |

## Player's house 1F

**Mom (Melitta),** by the hearth.
```text
> after FLAG_ICHOR_TALKED_TO_MOM, before FLAG_ICHOR_THREAD_READ:
MOM: The square! Halia's under the old olive. Go, go.

> after FLAG_ICHOR_THREAD_READ, before FLAG_ICHOR_GOT_STARTER:
MOM: What did Halia say? …Nothing much? Hm. She's getting old.

MOM: Daphne's waiting. Don't make me walk you there.

> after FLAG_ICHOR_GOT_STARTER, before FLAG_ICHOR_KLEON_BATTLE_1_DONE:
MOM: Let me see! Oh, look at it. Does it eat honey? Everything eats honey.

> after FLAG_ICHOR_KLEON_BATTLE_1_DONE:
MOM: I heard about the Lakonian boy. The whole village heard.
```
Then, whenever `FLAG_ICHOR_GOT_STARTER` is set:
```text
MOM: You look worn out. Sit. Eat something?
```
?? YES/NO
```text
> YES: [special HealPlayerParty and the heal jingle]
MOM: Bread, honey, and a nap. Works on Pokémon and children both.

> NO:
MOM: Stubborn. You get that from me.
```

| Object | Text |
|---|---|
| TV, re-skinned as Mom's loom | "A half-woven traveling cloak. Mom says you'll need it someday." / "She's said “someday” a lot lately." |
| Hearth | "The family hearth, banked low. Mom says a cold hearth is bad luck." |
| Shelf | "Jars of honey, sealed with wax. One is labelled “NOT FOR {PLAYER}.”" |

## Kydippe's house (`MAP_ELAIA_VILLAGE_NEIGHBORS_HOUSE`)

**Kydippe** (old midwife), in her chair by the window. Her Chansey wanders the room.
```text
KYDIPPE: Melitta's child! Come here. I delivered you, you know.

KYDIPPE: You didn't cry. You just looked around, like you'd lost something.

KYDIPPE: Here. For the road. Don't tell Philon, he'll want some.
```
[Give `ITEM_ORAN_BERRY` ×2 once. Set `FLAG_ICHOR_GOT_KYDIPPE_ORAN`.]
```text
> after the gift:
KYDIPPE: Every child I've delivered walks that road one day. Go well.
```
**Chansey** (Pokémon object event)
```text
CHANSEY: Chaaan! [It pats your head. Professionally.]
```

## Glykera's house (`MAP_ELAIA_VILLAGE_BAKERS_HOUSE`)

Every house is a home (`design/MAP_DESIGN.md` §2). This is the house west of the square. **Glykera** bakes the Klotheia's honey cakes, and the stall in the square is hers; she is Korinna's mother. Her father **Kimon** pulled an oar on the war triremes for forty years and keeps the corner by the window. His Finizen, **Arion**, swam beside his ship the whole way.

What happens:
- **A swap.** Glykera has run out of honey. The comb hidden in Melitta's hives (Part 6) buys two of her honey cakes (Old Gateau ×2).
- **A trade, after beat 4.** Once the player has Poké Balls, Kimon trades Arion for a Wooloo from Route 1.
- **A return gift, after the Hearth Laurel.** Kimon gives the pearls he dived for as a boy (Pearl String).
- **Lore.** Kimon's halcyon days ("the sea goes flat as oil… no sail moves a ship then") set up beat 8.

The room is L-shaped: the bakery runs deep on the left, with the honey shelf, the oven (the kitchen hearth), the flour basket, the grain pithos, the kneading table and the mortar. Kimon's nook is a shallower bay on the right, with the model trireme, his oars and a blue rug.

**Glykera**, at her oven
```text
> FLAG_ICHOR_GOT_GLYKERA_CAKES unset, no Honey in the bag:
GLYKERA: Mind the tray! …Oh, it's you. Melitta's child. The whole island wants honey cakes today.

GLYKERA: And I've run out of honey. On festival day! Your mother promised me a jar.

GLYKERA: Her hives are behind your house. Bring me a comb and I'll make it worth your while.

> unset, with Honey:
GLYKERA: Is that honey? Melitta's honey? Oh, you darling. Give it here.
```
[Take one `ITEM_HONEY`.]
```text
GLYKERA: There. The last tray is saved, and so is the festival.

GLYKERA: Take two from the first batch. They're still warm.
```
[Give `ITEM_OLD_GATEAU` ×2. Set `FLAG_ICHOR_GOT_GLYKERA_CAKES`.]
```text
GLYKERA: Honey and barley. They mend whatever ails you, or your Pokémon.

> after the cakes, before FLAG_ICHOR_THREAD_READ:
GLYKERA: Korinna's been at the square since dawn. She says she isn't nervous.

GLYKERA: She's been sick twice.

> after FLAG_ICHOR_THREAD_READ:
GLYKERA: Right about half the time, Halia told my Korinna.

GLYKERA: She's choosing to hear it as a compliment. She gets that from her grandfather.

> after FLAG_ICHOR_KLEON_BATTLE_1_DONE:
GLYKERA: That Lakonian boy bought eleven cakes and ate twelve. I'm still working out how.
```

**Kimon**, by his chair under the window
```text
> before FLAG_ICHOR_GOT_POKEBALLS:
KIMON: Forty years on the rowing benches. Top bench, the thranites. Best view of the sky.

KIMON: Up there you learn the sea. When the halcyons nest, it goes flat as oil.

KIMON: Days with no wind at all. No sail moves a ship then. Only oars.

KIMON: My knees are done with oars. Arion isn't done with the sea. He sulks in his ball all day.

KIMON: Come back when you've some Poké Balls of your own. I've a thought about Arion.

> after FLAG_ICHOR_GOT_POKEBALLS:
KIMON: Arion's my Finizen. He swam beside my ship from Kalliste to Athens and back, twenty years.

KIMON: He's wasted on an old man by a fire. Bring me a Wooloo, something warm for my feet,

KIMON: and Arion goes to sea with you. Deal?
```
?? YES/NO, then choose a Pokémon (the expansion's party-and-storage picker)
```text
> NO, or nothing chosen:
KIMON: Think on it. Wooloo graze all along the road north.

> not a Wooloo:
KIMON: That's no Wooloo. My feet know the difference.

> a Wooloo: [the in-game trade `INGAME_TRADE_ICHOR_ARION`: Finizen "ARION", OT KIMON, holding an Oran Berry. Set FLAG_ICHOR_DID_KIMON_TRADE.]
KIMON: Mind this one, Arion. Stubborn chin. Runs in the family.

> after the trade:
KIMON: The Wooloo's asleep on my feet already.

KIMON: Best trade I ever made, and I once swapped a helmet for a goat.

> FLAG_BADGE01_GET set, FLAG_ICHOR_GOT_KIMON_PEARLS unset (comes first):
KIMON: A laurel! From the Hearthkeeper herself?

KIMON: In my day the winner got a cup of wine and a slap on the back.

KIMON: Here. I brought these up off the sea floor when I was your age.

KIMON: Sell them for your passage, or keep them for luck. I never decided.
```
[Give `ITEM_PEARL_STRING`. Set `FLAG_ICHOR_GOT_KIMON_PEARLS`.]
```text
> after the trade and the Hearth Laurel:
KIMON: Halcyon days down at Akti, they tell me. Sea like oil, and no wind.

KIMON: Told you. Only oars move a ship then.
```

| Object | Text |
|---|---|
| The oven | "Glykera's oven. The tray inside smells of honey and toasted barley." |
| Honey shelf | Before the cakes: "Jars of honey, every one of them scraped clean. On festival day." After: "Jars of honey. One is full again, sealed with Melitta's wax." |
| Grain pithos | "A pithos of barley flour, half empty. Someone has written “FESTIVAL” on the lid." |
| Model trireme | "A model trireme with three banks of tiny oars." / "Someone has painted KIMON on the top bench." |
| Kimon's window | "Between the olive trees, a sliver of sea. It hardly moves." |

## Akademia (`MAP_ELAIA_VILLAGE_AKADEMIA`)

**Daphne**
```text
> after FLAG_ICHOR_KLEON_BATTLE_1_DONE, before FLAG_ICHOR_RUINS_CLEARED:
DAPHNE: Alethea went up Kronion Hill. She said “digging” and ran.

DAPHNE: That girl runs toward holes. I've always admired that.

> after FLAG_ICHOR_RUINS_CLEARED:
DAPHNE: Alethea sent me a rubbing of that tablet. Interesting.

DAPHNE: “Where the grain goes underground.” I have a guess.

DAPHNE: But a guess is only a question that's gotten too confident.
```
**Alethea** (before beat 4 only)
```text
ALETHEA: Don't touch that scroll. Or that one. Actually, don't touch scrolls.
```

| Object | Text |
|---|---|
| The third krater (stays) | "The last starter peers out of its krater. It looks hopeful." |
| Wall map | "A painted map of Aethos. Kalliste is a tiny green dot." / "Someone has drawn an arrow at it labelled “YOU ARE HERE.”" |
| Bookshelf | "“Every myth is a memory of a Pokémon” is carved over the shelf." |

## Route 1 (`MAP_KALLISTE_ROUTE1`)

The road runs north from Elaia through olive groves and terraced hillside to Akti. The Kronion Hill spur branches off to the east about two-thirds of the way up. Trainer placement, south to north: Tityros (at the meadow wall's only gap, the first and easy one), Phyllis (optional, on her grove lane), Komatas (optional, on the bee terraces), Polyeidos (on the spur, guarding the way to the hill), Agis (holding the pass just north of the flock's wall gap). Three bands of tall grass cross the road and can't be walked around: just out of Elaia, in the grove narrows, and on the cove shore before the climb to Akti (tools/ichor/maps/route1.py proves it).

| NPC | Where | Role |
|---|---|---|
| Amaryllis | behind her flock, north of the spur | shepherdess, road block |
| Olive farmer (Route 1) | under the big olive, mid-route | gives a Sitrus Berry |
| Carter | by a cart and a Mudbray, south grove | gives Moomoo Milk |
| Youth on a wall | dry-stone wall near the herm | comic |

**Amaryllis**
```text
> before FLAG_ICHOR_RUINS_CLEARED:
AMARYLLIS: They won't budge. Not one of them. Not since sunrise.

AMARYLLIS: The ground's been humming up on Kronion Hill. Feel it?

AMARYLLIS: Sheep know things. Mostly about grass. But they know things.

> after:
AMARYLLIS: They're moving! The humming stopped and they just… went.

AMARYLLIS: Whatever you did up there, the flock thanks you. Baa.
```

**Olive farmer (Route 1)**
```text
OLIVE FARMER: I'd give you oil, but you can't carry oil. Take a berry.
```
[Give `ITEM_SITRUS_BERRY` once and set `FLAG_ICHOR_GOT_ROUTE1_SITRUS`.]
```text
OLIVE FARMER: Pick the olives, rest in the shade. That's the whole secret.
```

**Carter** (Mudbray object beside her)
```text
CARTER: Thirsty? Here, my last bottle. Fresh this morning.
```
[Give `ITEM_MOOMOO_MILK` once and set `FLAG_ICHOR_GOT_MOOMOO_MILK`.]
```text
CARTER: It's goat's milk. The bottle says Moomoo. Don't ask me why.

MUDBRAY: Hrrrnk! [It is carrying everything the carter owns.]
```

**Youth on a wall**
```text
YOUTH: No partner for me. Daphne said “next year.”

YOUTH: She said that last year too. I'm starting to see a pattern.
```

**Signs**
```text
[Herm, south end]
A herm of Hermes marks the road.
North: Akti Town. South: Elaia Village.

[Herm, at the spur fork]
East: Kronion Hill. North: Akti Town.

[Herm, north end]
North: Akti Town. Mind the nets.
```

## Kronion Hill (summit of the ruins)

A hilltop sanctuary of tumbled Doric drums around a broken altar. The dig pit sits in front of the altar.

| Object | Text |
|---|---|
| Stele at the top of the stair | "KRONION HILL. An old shrine, older than the olives." / "Someone has scratched a sickle into the stone. Recently." |
| Broken altar | "A cracked altar. The stone is warm, like a sleeping animal." |
| Dig pit, after it is cleared | The pit's floor now shows cut stone steps going down into the dark: Hecate's Torch's second gate, to the Kronion crypt (SYSTEMS.md, relic gates; D10). "Stone steps go down into the dark. You can't see a thing." / "…It still feels like something's looking up." |

Post-scene NPCs: none. The grunts and Alethea are hidden.

## Akti Town (`MAP_AKTI_TOWN`)

Layout reference, from the scaffold: you enter from the south road. The Asclepeion door is at (6,16), lower left; the Temple of Hestia at (15,16), lower right; the Fisher's house at (5,7), upper left; the Agora at (14,6), upper right. The quay runs along the north shore, with the trireme *Euploia* moored there. A strip of beach and tide rocks lies to the northeast.

| NPC | Where | Role |
|---|---|---|
| Diktys | upturned boat near the south gate | net-mender, greeter (beat 6) |
| Captain Nausikles | at the trireme's gangplank | trireme captain |
| Kleon | on the quay (until beat 8) | rival |
| Lakonian rower | on the quay beside Kleon | waiting for wind |
| Hydna | on the tide rocks, NE | sponge diver, gives Mystic Water |
| Fishwife | at a fish stall on the quay | comic |
| Old woman | on the temple steps | temple lore |
| Pilgrim | by the Asclepeion | Oracle gossip, dread |
| Kid on the pier | end of the pier | comic |
| Alethea | beat 8 | — |

**Diktys** (after beat 6)
```text
DIKTYS: Mending nets. Mending boats. Mostly mending my pride.

DIKTYS: My grandfather pulled a whole chest out of the sea once.

DIKTYS: Had a woman and a baby in it. Or so he said. He drank.
```

**Captain Nausikles**
```text
> before FLAG_BADGE01_GET:
NAUSIKLES: The mainland? Not without a laurel, young one.

NAUSIKLES: Emporion won't let you off the dock without one.

NAUSIKLES: Besides. We sail when the winds turn, and they haven't.

> after FLAG_ICHOR_SLICE_COMPLETE:
NAUSIKLES: Still flat. Still waiting. Go catch something, I'll shout.
```

**Kleon on the quay**
```text
> before FLAG_BADGE01_GET:
KLEON: Don't ask how it went with Ione.

KLEON: …Fine. She beat me. Then she fed me soup.

KLEON: Soup! I've never been so insulted in my life.

KLEON: Tomorrow I'll beat her. Then I'll eat the soup. Out of respect.
```
Kleon is hidden after beat 8 (`FLAG_ICHOR_HIDE_KLEON_AKTI`). He went off to train.

**Lakonian rower**
```text
LAKONIAN ROWER: Wind.

LAKONIAN ROWER: …None.

LAKONIAN ROWER: That was a whole Lakonian weather report.
```

**Hydna (sponge diver)**
```text
HYDNA: I dive for sponges. Holding my breath is the easy part.

HYDNA: Found this on the seabed yesterday. Bad luck to keep sea-gifts.
```
[Give `ITEM_MYSTIC_WATER` once and set `FLAG_ICHOR_GOT_MYSTIC_WATER`.]
```text
HYDNA: Give it to your Water Pokémon. The sea likes to be shared.

> after the gift:
HYDNA: The water's been strange at night. Too still. Even for halcyon days.
```

**Fishwife**
```text
FISHWIFE: Octopus! Fresh octopus! Still arguing!
```

**Old woman on the temple steps**
```text
OLD WOMAN: Ione keeps the fire. Her mother kept it. Her mother's mother.

OLD WOMAN: It hasn't gone out in three hundred years.

OLD WOMAN: Well. Once. But we don't talk about that.
```

**Pilgrim** (dread)
```text
PILGRIM: I'm just back from Delphoi. Long way to go for so little.

PILGRIM: The Pythia used to give whole verses. Riddles, rhymes.

PILGRIM: Now it's one word. Sometimes only “soon.”
```

**Kid on the pier**
```text
KID: When I grow up I'm going to be a Hierophant. Of fish.

KID: There's no temple for fish. That's why it's a good idea.
```

**Signs**
```text
[Town sign]
AKTI TOWN
Harbor of Kalliste. Mind the nets.

[Temple]
TEMPLE OF HESTIA
Hierophant: Ione, the Hearthkeeper. All guests welcome. All guests fed.

[Asclepeion]
ASCLEPEION
Rest for Pokémon and the weary, by the grace of Asclepius.

[Agora]
AGORA
Fair goods at fair prices. Mostly fair.

[Quay]
THE QUAY
Trireme to the mainland sails when the winds turn.

[Fisher's house]
GLAUKOS. Gone fishing. (Not really. Knock.)
```

## Akti Asclepeion (Pokémon Center re-skin)

**Healer.** These are the nurse strings, re-skinned. Ship them as Ichor-only copies under new labels, called from an Ichor nurse script, so Hoenn's centers don't change (see Open questions).

| Vanilla string | Ichor text |
|---|---|
| `gText_WouldYouLikeToRestYourPkmn` | "Welcome to the Asclepeion." / "We tend tired Pokémon by the sacred spring." / "Shall we tend yours?" |
| `gText_IllTakeYourPkmn` | "Rest them here a moment." |
| `gText_RestoredPkmnToFullHealth` | "There. Whole and well, by Asclepius's grace." |
| `gText_WeHopeToSeeYouAgain` | "Go in health." |

**Pithos (PC).** A great clay storage jar against the back wall, sealed with wax.
```text
A great clay pithos, taller than you. Its wax seal glows faintly.

{PLAYER} lifted the lid of the Pithos.
```
[Then the vanilla storage menu. Shared string re-skins: "Accessed SOMEONE'S PC" → "The Pithos of Akti opened." "POKéMON Storage System opened" → "Pokémon rest safely inside the jar."]

| NPC | Where | Lines |
|---|---|---|
| Fisher with a bandaged hand | bench by the door | "Krabby. Don't ask." / "…It was a big Krabby." |
| Woman by the Pithos | beside the jar | "Go on, open it. Everyone flinches the first time." / "Old stories. A jar, a girl, all the evils of the world. This one's just Pokémon." |
| Old man | by the statue | "My grandmother swore Asclepius once raised a man from the dead." / "Zeus struck him down for it. So now his healers stick to Pokémon. Safer." |
| Statue (object) | back wall | "Asclepius, with a snake coiled round his staff. It looks well fed." |

## Akti Agora (Mart re-skin)

**Demeas,** at the stall.
```text
DEMEAS: Welcome to the Agora! Buying? Selling? Haggling?

Please don't haggle.
```
[Mart UI. Then:]
```text
DEMEAS: Come again! Bring Lakonians, they pay double. In iron.
```

**Stock.** Expansion pokemart lists.
- Before `FLAG_BADGE01_GET`: Poké Ball, Potion, Antidote, Paralyze Heal, Awakening.
- After: add Super Potion, Repel and Escape Rope.

| NPC | Lines |
|---|---|
| Customer (man) | "Prices go up when the Lakonians are in town." / "They pay in iron bars. Iron bars! What am I supposed to do, build a gate?" |
| Customer (girl) | "What are Poké Balls made of? Nobody knows. My dad says “trade secrets.”" / "I think he doesn't know either." |

## Akti Fisher's house (`MAP_AKTI_TOWN_FISHERS_HOUSE`)

**Glaukos** (old fisher), by the window.
```text
GLAUKOS: Ah, a visitor. Do you fish?
```
?? YES/NO
```text
> YES:
GLAUKOS: Liar. You've got sandal tan, not net tan. Take this anyway.

> NO:
GLAUKOS: Not yet, you mean. Take this. Everyone fishes eventually.
```
[Give `ITEM_OLD_ROD` once and set `FLAG_ICHOR_GOT_OLD_ROD`.]
```text
{PLAYER} received an Old Rod!

GLAUKOS: Face the water, use the rod, wait for the tug. Then pull!

> after the gift:
GLAUKOS: I ate a strange seaweed once, as a lad. Felt immortal for a week.

GLAUKOS: Then I didn't. Don't eat strange seaweed.
```
**Glaukos's grandson**
```text
GRANDSON: Grandpa says he used to be a sea-god.

Grandpa says a lot of things.
```

## Temple of Hestia (`MAP_AKTI_TOWN_TEMPLE_OF_HESTIA`)

Euboulos (guide), the three acolytes and Ione are covered in beat 7, Part 3 and Part 4. One more NPC:

**Kanthos, the temple donkey** (Mudbray object, tied by the side door)
```text
EUBOULOS: [if you talk to Kanthos] Mind Kanthos. He brays at anyone sneaking about.

EUBOULOS: Once saved the goddess's dignity that way, they say. Good donkey.

KANTHOS: HRRRNK!
```

---

# Part 3. Trainers

Format: the `src/data/trainers.party` syntax. The Pic and Music values are vanilla placeholders until the Sprites stream delivers Kleon, Ione and the Titanborn. Moves are listed only where they differ from the defaults. Route trainers: IVs 0, AI Check Bad Move. Class names are at most 12 characters (`TrainerClass.name[13]`). New classes needed: LAKONIAN, SHEPHERD, HARVESTER, GOATHERD, HOPLITE, AUGUR, TITANBORN, ACOLYTE and HIEROPHANT.

## Kleon, first battle (Elaia square), level 5

At level 5, none of the starters has a STAB move yet: Snivy knows Tackle and Leer, Cyndaquil Tackle and Leer, Piplup Pound and Growl. So the fight is fair, and the type advantage is a lesson rather than a wall.

```
=== TRAINER_ICHOR_KLEON_ELAIA_CYNDAQUIL ===
Name: KLEON
Class: Lakonian
Pic: Brendan
Gender: Male
Music: Male
Double Battle: No
AI: Basic Trainer

Cyndaquil
Level: 5
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe
```
`TRAINER_ICHOR_KLEON_ELAIA_PIPLUP` (Piplup Lv5) and `TRAINER_ICHOR_KLEON_ELAIA_SNIVY` (Snivy Lv5) are the same entry with the species changed.

| Your starter | Kleon takes | Why it beats yours |
|---|---|---|
| Snivy | Cyndaquil | Fire beats Grass |
| Cyndaquil | Piplup | Water beats Fire |
| Piplup | Snivy | Grass beats Water |

His lines are in beat 4. Defeat text: "Wait, what? Do-over! Lakonians get do-overs! …No, we don't."

## Route 1 trainers, levels 3–7

**1. SHEPHERD Tityros.** In the first meadow, beside two grazing Wooloo.
```text
Before: TITYROS: You've got a partner? Let's see if it can herd!
Defeat: TITYROS: Scattered my flock! It'll take all afternoon to round them up.
After:  TITYROS: Sheep are easy. Stand still, look like grass.
```
```
=== TRAINER_ICHOR_TITYROS ===
Name: TITYROS
Class: Shepherd
Pic: Camper
Gender: Male
Music: Male
AI: Check Bad Move

Wooloo
Level: 3
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe

Mareep
Level: 4
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe
```

**2. HARVESTER Phyllis.** On a ladder in the first olive grove. Her sight line runs along the grove path.
```text
Before: PHYLLIS: Festival day and I'm still picking. Battle me, I need a break.
Defeat: PHYLLIS: That's fair. My Smoliv were up since dawn too.
After:  PHYLLIS: Every olive tree on Kalliste came from one cutting. Or so Gran says.
```
```
=== TRAINER_ICHOR_PHYLLIS ===
Name: PHYLLIS
Class: Harvester
Pic: Picnicker
Gender: Female
Music: Female
AI: Check Bad Move

Smoliv
Level: 4
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe

Smoliv
Level: 5
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe
```

**3. GOATHERD Komatas.** On the terraced hillside, by the beehive boxes.
```text
Before: KOMATAS: My goats climb anything. Let's see you climb this battle!
Defeat: KOMATAS: Ha! Good. The bees liked you. That's rare.
After:  KOMATAS: Got locked in a cedar chest once, as a boy.
After:  KOMATAS: Bees fed me honey till I got out.
```
```
=== TRAINER_ICHOR_KOMATAS ===
Name: KOMATAS
Class: Goatherd
Pic: Hiker
Gender: Male
Music: Hiker
AI: Check Bad Move

Skiddo
Level: 5
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe

Combee
Level: 5
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe
```

**4. HOPLITE Agis.** A Lakonian youth of the delegation, drilling in the pass just north of the flock's wall gap. He can only be met once the flock has moved.
```text
Before: AGIS: A Lakonian brings one spear to a fight. One is enough.
Defeat: AGIS: …Two spears next time.
After:  AGIS: Kleon? He's been racing his prophecy since he could walk.
After:  AGIS: He'll catch it, too. That's what worries me.
```
```
=== TRAINER_ICHOR_AGIS ===
Name: AGIS
Class: Hoplite
Pic: Black Belt
Gender: Male
Music: Intense
AI: Check Bad Move

Machop
Level: 7
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe
```

**5. AUGUR Polyeidos.** On a rise above the spur to Kronion Hill, staring at the sky. His line covers the whole spur.
```text
Before: POLYEIDOS: The birds are wrong today. Let me see if you're wrong too.
Defeat: POLYEIDOS: You're not wrong. The birds still are.
After:  POLYEIDOS: They're all flying away from the hill. Every one. Since dawn.
```
```
=== TRAINER_ICHOR_POLYEIDOS ===
Name: POLYEIDOS
Class: Augur
Pic: Bird Keeper
Gender: Male
Music: Suspicious
AI: Check Bad Move

Pidove
Level: 6
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe

Murkrow
Level: 7
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe
```

## Titanborn grunts (Kronion Hill), levels 8–9

These are earth-born types. Both grunts are scripted (`trainerbattle_no_intro`). Snivy and Piplup have the edge here. Cyndaquil players are pushed to use their Route 1 catches: Smoliv, Skiddo and Mudbray. That is deliberate.

**TITANBORN Petros** (display name GRUNT)
```text
Before: PETROS: [in the beat 5 scene]
Defeat: PETROS: Hrk! Amathos, your turn. I'm on break.
```
```
=== TRAINER_ICHOR_GRUNT_RUINS_PETROS ===
Name: GRUNT
Class: Titanborn
Pic: Magma Grunt M
Gender: Male
Music: Magma
AI: Check Bad Move

Geodude
Level: 8
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe
- Tackle
- Defense Curl
- Rock Throw

Drilbur
Level: 9
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe
```

**TITANBORN Amathos** (display name GRUNT)
```text
Before: AMATHOS: Useless. Watch how it's done.
Defeat: AMATHOS: The earth remembers, child. It remembers everything.
```
```
=== TRAINER_ICHOR_GRUNT_RUINS_AMATHOS ===
Name: GRUNT
Class: Titanborn
Pic: Magma Grunt F
Gender: Female
Music: Magma
AI: Check Bad Move

Nosepass
Level: 8
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe
- Tackle
- Harden
- Rock Throw

Silicobra
Level: 9
IVs: 0 HP / 0 Atk / 0 Def / 0 SpA / 0 SpD / 0 Spe
- Sand Attack
- Wrap
```
Silicobra's default Minimize is dropped on purpose: no evasion stacking in the slice.

## Temple acolytes, levels 10–11

Acolytes use IVs 6 and AI Basic Trainer. Lampon guards the great hearth and must be beaten before you can take the flame (see Part 4). Pyrrha and Aithra have sight lines but can be avoided.

**ACOLYTE Lampon.** Standing beside the great hearth in the center of the hall.
```text
Before: LAMPON: Nobody touches the hearth until they've faced its keeper!
Defeat: LAMPON: Fine. Fine! Carry the flame. Carefully. CAREFULLY.
After:  LAMPON: Read the hymn by the door. Twice. I had to read it nine times.
```
```
=== TRAINER_ICHOR_LAMPON ===
Name: LAMPON
Class: Acolyte
Pic: Psychic M
Gender: Male
Music: Male
AI: Basic Trainer

Minccino
Level: 10
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Fletchling
Level: 10
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**ACOLYTE Pyrrha.** On the left side of the hall, between the Table and Loom braziers.
```text
Before: PYRRHA: Ooh, a challenger! I've been itching for a fight all week!
Defeat: PYRRHA: Burned out. Ugh. That never happens to me.
After:  PYRRHA: Hestia gets the first cup and the last one. Always. Remember the last.
```
```
=== TRAINER_ICHOR_PYRRHA ===
Name: PYRRHA
Class: Acolyte
Pic: Psychic F
Gender: Female
Music: Female
AI: Basic Trainer

Tandemaus
Level: 10
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Growlithe
Level: 11
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

**ACOLYTE Aithra.** On the right side of the hall by the Bed brazier, yawning.
```text
Before: AITHRA: I keep the night watch. I haven't slept since spring. Battle?
Defeat: AITHRA: Counting Wooloo doesn't help. I've tried. Thousands.
After:  AITHRA: Old Kronos swallowed Hestia first and coughed her up last.
After:  AITHRA: Patient lady.
After:  AITHRA: The bed's always last before home. Everyone ends up in bed. Eventually.
```
```
=== TRAINER_ICHOR_AITHRA ===
Name: AITHRA
Class: Acolyte
Pic: Lass
Gender: Female
Music: Female
AI: Basic Trainer

Wooloo
Level: 10
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe

Hoothoot
Level: 11
IVs: 6 HP / 6 Atk / 6 Def / 6 SpA / 6 SpD / 6 Spe
```

## Hierophant Ione, the Hearthkeeper, levels 12–14 (Hero difficulty)

Her team is a guard, a hungry mouth and a flame. It is modelled on Roxanne's strength (12/12/15, two Potions).

The matchups:
- Piplup has the edge on her Litleo ace.
- Snivy is at a disadvantage and is pointed to Mudbray's Double Kick (Lv8) and Timburr from the hill.
- Cyndaquil is neutral, and Quilava arrives at 14.

```
=== TRAINER_ICHOR_IONE_1 ===
Name: IONE
Class: Hierophant
Pic: Leader Flannery
Gender: Female
Music: Female
Items: Potion / Potion
AI: Basic Trainer

Lillipup
Level: 12
Ability: Vital Spirit
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Tackle
- Leer
- Work Up
- Bite

Munchlax @ Oran Berry
Level: 13
Ability: Thick Fat
IVs: 12 HP / 12 Atk / 12 Def / 12 SpA / 12 SpD / 12 Spe
- Tackle
- Lick
- Defense Curl
- Recycle

Litleo @ Sitrus Berry
Level: 14
Ability: Unnerve
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
- Ember
- Headbutt
- Work Up
- Leer
```
- Lillipup leads deliberately, so it never gets a doubled Retaliate.
- Munchlax plus Recycle eats the Oran Berry twice: "the feast's leftovers". It is a lesson, not a wall.
- Litleo's Unnerve stops the player's berries for the ace fight only.
- Spartan difficulty needs its own team from Balance.

Her dialogue is in beat 7. Defeat text: "There. Warm all the way through."

## Every species in the slice, with its myth or setting link

| Species (Gen) | Where | Link |
|---|---|---|
| Snivy (5) | starter | Serperior is the Python of Delphoi, slain by Apollo |
| Cyndaquil (2) | starter | Typhlosion is Typhon, father of monsters |
| Piplup (4) | starter | Empoleon wears Poseidon's trident |
| Smoliv (9) | intro, Route 1, Phyllis | Athena's gift of the first olive tree; Elaia means "olive" |
| Wooloo (8) | Route 1, Tityros, Aithra | Island sheep; counting sheep on the night watch |
| Mareep (2) | Route 1, Tityros | Its line ends in Ampharos, the Golden Fleece |
| Skiddo (6) | Route 1, hill, Komatas | Amalthea, the goat that nursed infant Zeus |
| Combee (4) | Route 1, Komatas | Melissa and the bees that fed Zeus honey; Komatas fed by bees |
| Pidove (5) | Route 1, Polyeidos | Doves sacred to Aphrodite; augury birds |
| Nincada (3) | Route 1 | Tithonus, given eternal life without youth, shrivelled to a cicada; Shedinja is the husk |
| Ekans (1) | Route 1 | The guardian house-snake (oikouros ophis) of Greek homes |
| Mudbray (7) | Route 1, hill, Kanthos | The donkey sacred to Hestia, whose bray saved her |
| Tandemaus (9) | Route 1, Pyrrha | Apollo Smintheus, the mouse-lord |
| Ponyta (1) | Route 1 (rare) | The sun-horses of Helios's chariot |
| Hoothoot (2) | Route 1 night, Aithra | Athena's owl, the night watch |
| Spinarak (2) | Route 1 night, hill | Arachne the weaver, turned spider; thread motif |
| Murkrow (2) | Route 1 night, Polyeidos | Apollo's white crow, turned black for bad news |
| Cleffa (2) | Route 1 night (rare) | Selene's moon-child |
| Nickit (8) | Route 1 night (rare) | The Teumessian fox, fated never to be caught |
| Roggenrola (5) | hill | The stones Deucalion and Pyrrha threw, which became people |
| Baltoy (3) | hill | Cycladic clay idols, Kalliste's own past |
| Timburr (5) | hill | The beam-carriers who raised the old temples |
| Diglett (1) | hill | The Spartoi, men sown from the earth |
| Rockruff (7) | hill | Stone guard-dogs of the sanctuary |
| Bronzor (4) | hill | Bronze votive mirrors buried in shrines |
| Growlithe, Hisuian form (1/8) | hill (rare) | Laelaps, the hound fated to catch everything, turned to stone with the fox |
| Geodude (1) | Petros | Earth-born stone; Gaia's children |
| Drilbur (5) | Petros | The Titanborn dig crew |
| Nosepass (3) | Amathos | Magnes the shepherd's lodestone, used as a fragment-finder |
| Silicobra (8) | Amathos | The Gigantes, earth-born with serpent legs |
| Machop (1) | Agis | Pankration and Herakles's strength; Lakonian wrestling |
| Minccino (5) | Lampon | Sweeps the hearth ash at dawn (setting) |
| Fletchling (6) | Lampon | A spark with wings, carrying fire (setting) |
| Growlithe (1) | Pyrrha | Temple guard-dog (setting) |
| Lillipup (5) | Ione | The hound that sleeps by the hearth and guards the door |
| Munchlax (4) | Ione | Hestia takes the first and last share of the feast; Munchlax takes the rest |
| Litleo (6) | Ione | A walking hearth-flame; a lion cub before any Nemean Lion |
| Chansey (1) | Kydippe | The midwife's helper (setting) |
| Magikarp (1) | fishing | Gyarados as Cetus, the sea monster Perseus slew |
| Horsea (1) | fishing | The hippocampi drawing Poseidon's chariot |
| Krabby (1) | fishing | Karkinos, the crab Hera sent against Herakles |
| Finizen (9) | fishing | Arion's dolphin; the pirates Dionysus turned to dolphins |
| Corsola (2) | fishing | Coral born from Medusa's blood on seaweed |
| Wailmer (3) | fishing | The ketos, the great whale-beast |
| Seadra, Kingler (1) | super rod | Grown hippocampus and Karkinos |
| Dhelmise (7) | super rod (rare) | Anchors of a thousand wrecks on the wine-dark sea |
| Tentacool (1), Wingull (3), Pelipper (3), Mantyke (4) | surfing (later) | Harbor life (setting) |

---

# Part 4. Wild encounters

These are in `src/data/wild_encounters.json` terms. Land slot rates are fixed by the group's `fields`: 20/20/10/10/10/10/5/5/4/4/1/1.

**Day and night split.** `OW_TIME_OF_DAY_ENCOUNTERS` is `FALSE` today, so the engine team must set it `TRUE` in `include/config/overworld.h`. With `OW_TIME_OF_DAY_FALLBACK` = `TIME_MORNING` and the fallback enabled, define only `_Morning` (used for morning, day and evening) and `_Night`. Every other area at night (fishing, water) falls back to `_Morning` per area. Night is 20:00–06:00 under GEN_LATEST.

## Route 1 tall grass

`"map": "MAP_KALLISTE_ROUTE1"`, `"base_label": "gKallisteRoute1_Morning"`, land `encounter_rate: 20`

| Slot | Rate | Species | Levels |
|---|---|---|---|
| 0 | 20% | Smoliv | 3–5 |
| 1 | 20% | Wooloo | 3–5 |
| 2 | 10% | Pidove | 3–5 |
| 3 | 10% | Skiddo | 3–5 |
| 4 | 10% | Combee | 3–5 |
| 5 | 10% | Mareep | 4–6 |
| 6 | 5% | Nincada | 4–6 |
| 7 | 5% | Ekans | 4–6 |
| 8 | 4% | Mudbray | 4–6 |
| 9 | 4% | Tandemaus | 4–6 |
| 10 | 1% | Ponyta | 5–5 |
| 11 | 1% | Mareep | 6–6 |

`"base_label": "gKallisteRoute1_Night"`, land `encounter_rate: 20`

| Slot | Rate | Species | Levels |
|---|---|---|---|
| 0 | 20% | Hoothoot | 3–5 |
| 1 | 20% | Wooloo | 3–5 |
| 2 | 10% | Spinarak | 3–5 |
| 3 | 10% | Smoliv | 3–5 |
| 4 | 10% | Murkrow | 4–6 |
| 5 | 10% | Tandemaus | 3–5 |
| 6 | 5% | Nincada | 4–6 |
| 7 | 5% | Ekans | 4–6 |
| 8 | 4% | Mudbray | 4–6 |
| 9 | 4% | Skiddo | 4–6 |
| 10 | 1% | Cleffa | 5–5 |
| 11 | 1% | Nickit | 5–5 |

Example JSON shape (slots 0–1 shown; the rest follow the same pattern):
```json
{
  "map": "MAP_KALLISTE_ROUTE1",
  "base_label": "gKallisteRoute1_Night",
  "land_mons": {
    "encounter_rate": 20,
    "mons": [
      { "min_level": 3, "max_level": 5, "species": "SPECIES_HOOTHOOT" },
      { "min_level": 3, "max_level": 5, "species": "SPECIES_WOOLOO" }
    ]
  }
}
```

## Kronion Hill (the ruins summit)

This needs the summit to be its own map: `MAP_KALLISTE_ROUTE1_KRONION_HILL`, base label `gKallisteRoute1KronionHill_Morning`, a single table at all hours, land `encounter_rate: 15`. The grass is patchy, among the column drums.

| Slot | Rate | Species | Levels |
|---|---|---|---|
| 0 | 20% | Roggenrola | 5–7 |
| 1 | 20% | Skiddo | 5–7 |
| 2 | 10% | Baltoy | 5–7 |
| 3 | 10% | Timburr | 5–7 |
| 4 | 10% | Diglett | 5–7 |
| 5 | 10% | Smoliv | 5–7 |
| 6 | 5% | Rockruff | 6–7 |
| 7 | 5% | Spinarak | 5–7 |
| 8 | 4% | Bronzor | 6–7 |
| 9 | 4% | Mudbray | 6–7 |
| 10 | 1% | Growlithe (`SPECIES_GROWLITHE_HISUI`) | 6–6 |
| 11 | 1% | Growlithe (`SPECIES_GROWLITHE_HISUI`) | 7–7 |

**If the hill stays on the Route 1 map**, put these in Route 1's `_Morning` slots 8–11 instead: Timburr 4%, Roggenrola 4%, Baltoy 1%, Hisuian Growlithe 1%. Drop Mudbray and Tandemaus to night only. This keeps Fighting and Rock options for Snivy and Cyndaquil players before Ione.

## Akti fishing

`"map": "MAP_AKTI_TOWN"`, `"base_label": "gAktiTown_Morning"`, fishing `encounter_rate: 30`. Only the Old Rod can be obtained in the slice. The Good and Super Rod slots are filled now so the table is ready later.

| Slot | Rod | Rate | Species | Levels |
|---|---|---|---|---|
| 0 | Old | 70% | Magikarp | 5–10 |
| 1 | Old | 30% | Horsea | 5–10 |
| 2 | Good | 60% | Krabby | 10–20 |
| 3 | Good | 20% | Finizen | 10–20 |
| 4 | Good | 20% | Corsola | 10–20 |
| 5 | Super | 40% | Wailmer | 20–30 |
| 6 | Super | 40% | Seadra | 25–30 |
| 7 | Super | 15% | Corsola | 25–30 |
| 8 | Super | 4% | Kingler | 28–32 |
| 9 | Super | 1% | Dhelmise | 30–35 |

**Water (surfing),** for when Poseidon's Conch arrives in a later phase. `water_mons`, `encounter_rate: 4`, slots 60/30/5/4/1: Tentacool 5–30, Wingull 10–30, Finizen 15–30, Pelipper 25–30, Mantyke 20–30.

---

# Part 5. The Hearth Trial (Temple of Hestia)

## What the player sees

The temple is one long hall, entered from the south. In the middle burns the **great hearth**: a round stone hearth with a fire that never goes out, guarded by Lampon. Four cold bronze **braziers** stand around the hall. Each has a small carved plaque:
- the **Door** (a carved doorway),
- the **Table** (a loaf of bread),
- the **Loom** (a spindle),
- the **Bed** (a couch).

**Place the braziers so that their spatial order does not match the hymn**, so the player has to read. Suggested placement:
- Bed: front right.
- Loom: front left.
- Door: back right.
- Table: back left.

At the north end, on a raised dais, Ione stands behind a second small hearth, the **inner hearth**. Two cold braziers flank the dais steps and block them (a collision or metatile gate).

A stone **stele** stands just inside the entrance. It holds the hymn.
```text
HYMN OF THE HEARTH

Hestia, first and last of every feast.

From your fire, carry fire.

First to the door, that greets the stranger.

Then to the table, where the bread is shared.

Then to the loom, where the cloak is woven.

Then to the bed, where the house lies sleeping.

And bring the last flame home to you.
```

## What the player does

1. Beat Lampon at the great hearth. Until then, interacting with the hearth gives: "LAMPON: Hands off! Face me first."
2. Interact with the great hearth.
   ```text
   The great hearth of Hestia. It has never once gone out.

   Take a flame from the hearth?
   ```
   ?? YES/NO. YES sets `VAR_ICHOR_HEARTH_TRIAL` = 1.
   ```text
   {PLAYER} lit a torch from the hearth. Walk carefully.
   ```
3. Interact with a brazier while holding the flame (var ≥ 1 and < 5). Each brazier shows its plaque first:
   ```text
   A bronze brazier. Its plaque shows a loaf of bread.

   Light it?
   ```
   - **Correct next brazier** (Door when var = 1, Table at 2, Loom at 3, Bed at 4): play the fire SE, swap the brazier metatile to lit, and add 1 to the var.
     ```text
     The brazier catches with a soft WHUMPF.
     ```
   - **Wrong brazier:** set the var to 0, set all four braziers back to unlit and play a fizzle SE.
     ```text
     The flame gutters and dies. All the braziers go dark.

     Somewhere, an acolyte sighs.
     ```
   - **Interacting with no flame** gives only the plaque line.
4. After the Bed (var = 5), return to the **great hearth**.
   ```text
   Give the last flame back to the hearth?
   ```
   YES sets the var to 6 and `FLAG_ICHOR_HEARTH_TRIAL_DONE`. Play a flare SE and briefly flash the screen white.
   ```text
   The hearth roars up, gold and tall. Every brazier in the hall answers.

   The braziers by the dais flare. The way to the Hearthkeeper is open.

   Something tumbles out of the ashes at your feet.
   ```
   Give `ITEM_CHARCOAL` and set `FLAG_ICHOR_GOT_CHARCOAL`.
   ```text
   {PLAYER} found a piece of Charcoal from Hestia's hearth!
   ```
   If the player lights all four braziers but walks to the dais without returning the flame, the dais braziers stay cold. Talking to Euboulos then gives: "EUBOULOS: You took the first flame. Hestia is owed the last."
5. **Leaving while holding the flame** (var 1–5, stepping on the exit warp row): a coord trigger fires.
   ```text
   The torch sputters out in the sea wind. Hestia keeps her fire at home.
   ```
   Reset the var to 0 and the braziers to unlit.

## Placement and gates

- **Lampon** is on the tile south of the great hearth, facing south. He is mandatory: the hearth checks his trainer flag.
- **Pyrrha** is in the left aisle, with a sight line of 3 facing east, crossing the route to the Loom and Table braziers.
- **Aithra** is in the right aisle beside the Bed brazier, facing west, sight line 2. Both are avoidable with careful pathing.
- **Ione** is on the dais, facing south. Talking to her before the trial is done isn't possible, because the dais gate blocks her.

## State

| Name | Values |
|---|---|
| `VAR_ICHOR_HEARTH_TRIAL` | 0 no flame · 1 carrying · 2 Door lit · 3 Table lit · 4 Loom lit · 5 Bed lit · 6 complete |
| `FLAG_ICHOR_HEARTH_TRIAL_DONE` | set at 6, permanent |
| `FLAG_ICHOR_GOT_CHARCOAL` | the trial reward |

The map's `ON_LOAD` script draws the brazier metatiles from the var. `ON_TRANSITION` resets the var to 0 if it is between 1 and 5. Once the trial is done, all braziers and the dais are drawn lit.

---

# Part 6. Items and rewards by map

Flag naming: visible item balls use `FLAG_ITEM_ICHOR_<MAP>_<ITEM>`, hidden items use `FLAG_HIDDEN_ITEM_ICHOR_<MAP>_<ITEM>`, and gifts use the flags named in the scenes.

| Map | Item | How | Where |
|---|---|---|---|
| Player's house 2F | Potion | chest (item storage) | starts inside, as in vanilla |
| Player's house 1F | Talaria | gift, Mom (beat 1) | — |
| Elaia | Potion | visible | beside the olive press |
| Elaia | Honey | hidden | at Mom's beehives behind the house; Glykera swaps her honey cakes for it |
| Elaia | Relic Copper | hidden | in the well ("a coin someone wished on") |
| Elaia, Kydippe's house | Oran Berry ×2 | gift | — |
| Elaia, Glykera's house | Old Gateau ×2 (honey cakes) | swap, for the Honey from Melitta's hives | — |
| Elaia, Glykera's house | Finizen "Arion" | in-game trade with Kimon, for a Wooloo; after beat 4 | — |
| Elaia, Glykera's house | Pearl String | gift, Kimon; after the Hearth Laurel | — |
| Akademia | starter, Pokédex | gift, Daphne | — |
| Elaia | Poké Ball ×5 | gift, Alethea (beat 4) | — |
| Route 1 | Poké Ball | visible | on the grove's west walk, above the lip down to the meadow |
| Route 1 | Miracle Seed | visible | deep in Phyllis's olive grove, past her lane |
| Route 1 | Potion | visible | on the cove beach, past the shore grass |
| Route 1 | Oran Berry | hidden | under the big olive |
| Route 1 | Repel | hidden | in the corner of the walled patch by the carter |
| Route 1 | Antidote | hidden | in the grass near the Ekans patch |
| Route 1 | Sitrus Berry | gift, olive farmer | — |
| Route 1 | Moomoo Milk | gift, carter | — |
| Kronion Hill | Escape Rope | visible | at the dig pit; the grunts left it behind |
| Kronion Hill | Hard Stone | hidden | in the rubble by the column drums |
| Kronion Hill | Stardust | hidden | behind the broken altar |
| Kronion Hill | Augur's Eye | gift, Alethea (`FLAG_ICHOR_DEXNAV_GET`) | — |
| Akti | Potion | visible | among the crates on the quay |
| Akti | Paralyze Heal | visible | by the fish stall |
| Akti | Super Potion | hidden | behind Diktys's drying nets |
| Akti | Pearl | hidden | on the tide rocks |
| Akti | Heart Scale | hidden | on the beach sand |
| Akti | Mystic Water | gift, Hydna | — |
| Akti, Fisher's house | Old Rod | gift, Glaukos | — |
| Temple | Charcoal | trial reward | — |
| Temple | Hearth Laurel (badge 1), TM42 Facade | Ione | — |

There is one type booster per starter: Miracle Seed, Charcoal and Mystic Water.

---

# Part 7. Names introduced

All names are Greek-rooted and clear of the Lazarus avoid-list.

| Name | Who or what | Root |
|---|---|---|
| Melitta | the player's mother, a beekeeper | "bee" |
| Halia | the island priestess | "of the sea" |
| the Klotheia | the coming-of-age festival | Klotho, the Spinner |
| Korinna, Philon | youths at the reading | classical names |
| Kydippe | the midwife next door | classical name |
| Glykera | the honey-cake baker, Korinna's mother | "sweet one" |
| Kimon | her father, a retired trireme oarsman | the Athenian admiral Cimon |
| Arion | Kimon's Finizen | the poet a dolphin carried ashore |
| Gylippos | Lakonian elder | Spartan name |
| Amaryllis | the shepherdess with the flock | Theocritus |
| Tityros | Shepherd | Theocritus |
| Phyllis | Harvester | "leafy"; turned into a tree in myth |
| Komatas | Goatherd | Theocritus's goatherd, fed by bees |
| Agis | Hoplite | Spartan kings' name |
| Polyeidos | Augur | the seer Polyidus |
| Petros, Amathos | Titanborn grunts | "rock", "sand" |
| Lampon, Pyrrha, Aithra | acolytes | "lamp", "flame-colored", "bright sky" |
| Euboulos | temple guide | "good counsel" |
| Kanthos | temple donkey (a Mudbray) | "pack-ass" |
| Diktys | net-mender | the net-fisher who found Perseus |
| Demeas | Agora stallkeeper | New Comedy name |
| Glaukos | old fisher | the fisherman who became a sea-god |
| Hydna | sponge diver | the famous ancient diver |
| Nausikles | trireme captain | "ship-glory" |
| the Euploia | the trireme | "fair sailing" |
| Kronion Hill | the hilltop ruins | the Hill of Kronos at Olympia |
| Talaria, klepsydra, kibotos, krater | re-skinned objects | — |

---

# Part 8. Flags and vars

Engine: claim these as `FLAG_ICHOR_*` and `VAR_ICHOR_*`.

**Story**
- `FLAG_ICHOR_SET_WATER_CLOCK`
- `FLAG_ICHOR_TALKED_TO_MOM`
- `FLAG_ICHOR_THREAD_READ`
- `FLAG_ICHOR_GOT_STARTER`
- `FLAG_ICHOR_KLEON_TOOK_STARTER`
- `FLAG_ICHOR_KLEON_BATTLE_1_DONE`
- `FLAG_ICHOR_WON_KLEON_1`
- `FLAG_ICHOR_GOT_POKEBALLS`
- `FLAG_ICHOR_RUINS_CLEARED`
- `FLAG_ICHOR_FOUND_TITAN_TABLET`
- `FLAG_ICHOR_ARRIVED_AKTI`, plus a visited/fly flag for Akti
- `FLAG_ICHOR_HEARTH_TRIAL_DONE`
- `FLAG_ICHOR_GOT_CHARCOAL`
- `FLAG_ICHOR_GOT_TM_FACADE`
- `FLAG_ICHOR_SLICE_COMPLETE`

**Gifts**
- `FLAG_ICHOR_GOT_KYDIPPE_ORAN`
- `FLAG_ICHOR_GOT_GLYKERA_CAKES`
- `FLAG_ICHOR_DID_KIMON_TRADE`
- `FLAG_ICHOR_GOT_KIMON_PEARLS`
- `FLAG_ICHOR_GOT_ROUTE1_SITRUS`
- `FLAG_ICHOR_GOT_MOOMOO_MILK`
- `FLAG_ICHOR_GOT_MYSTIC_WATER`
- `FLAG_ICHOR_GOT_OLD_ROD`

**Object hide flags**
- `FLAG_ICHOR_HIDE_KRATER_SNIVY`, `_CYNDAQUIL`, `_PIPLUP`
- `FLAG_ICHOR_HIDE_KLEON_ELAIA`
- `FLAG_ICHOR_HIDE_ALETHEA_AKADEMIA`
- `FLAG_ICHOR_HIDE_ALETHEA_ELAIA`
- `FLAG_ICHOR_HIDE_SCRIBE` (set at the end of beat 4)
- `FLAG_ICHOR_HIDE_ALETHEA_RUINS`
- `FLAG_ICHOR_HIDE_RUINS_GRUNTS`
- `FLAG_ICHOR_HIDE_TITAN_TABLET`
- `FLAG_ICHOR_HIDE_ROUTE1_FLOCK`
- `FLAG_ICHOR_HIDE_KLEON_AKTI`
- `FLAG_ICHOR_HIDE_ALETHEA_AKTI`

**Battle**
- `FLAG_ICHOR_NO_WHITEOUT`, assigned to `B_FLAG_NO_WHITEOUT` in `include/config/battle.h`

**Vars**
- `VAR_ICHOR_HEARTH_TRIAL`
- Vanilla `VAR_STARTER_MON`

**Vanilla flags used**
- `FLAG_SYS_POKEMON_GET`
- `FLAG_SYS_POKEDEX_GET`
- `FLAG_SYS_B_DASH`
- `FLAG_RECEIVED_RUNNING_SHOES`
- `FLAG_BADGE01_GET`
- `FLAG_ICHOR_DEXNAV_GET` (already claimed)

---

# Open questions

1. **Kronion Hill as its own map.** The plan puts the ruins on the Route 1 map. I recommend a small summit map (`MAP_KALLISTE_ROUTE1_KRONION_HILL`) for three reasons: its own encounter table, an isolated cutscene, and a clean hide-flag scope. A fallback merge is given in Part 4.
2. **Time-of-day encounters** need `OW_TIME_OF_DAY_ENCOUNTERS TRUE`. This is a config change for the engine team.
3. **No-whiteout for Kleon.** `B_FLAG_NO_WHITEOUT` is 0 and needs a claimed flag. The alternative is vanilla whiteout to home on a loss. I wrote both outcomes as continuing.
4. **Elaia vs Lazarus's Professor Elia.** The bible's village name is one letter off Lazarus's professor. It's probably fine, but the director should decide.
5. **Currency.** The bible doesn't re-skin money. I avoided naming coins, apart from Lakonian iron bars as a joke.
6. **Shared strings.** The Asclepeion and Pithos re-skins should be Ichor-only copies, so Hoenn centers stay vanilla during the slice. Global replacement is fine once Hoenn is cut.
7. **The Augur's Eye arrives in the slice,** from Alethea at the ruins. It isn't in the plan, but the flag already exists and it shows off a modern feature in the playtest. Cut it if unwanted.
8. **Kleon lost to Ione** and plans to win "tomorrow". This keeps him likable and seeds his fall, but it means he leaves Kalliste one laurel behind until Phase 2 resolves it.
9. **The third starter** stays with Daphne ("someone always comes late"). It could be a later gift or the Sanctuary of Firsts. No promise is made in the text.
10. **TM numbering.** Facade is vanilla TM42. If Balance rebuilds the TM list, keep Facade as the Hearth Laurel TM.
11. **Starter selection UI vs table.** Both are written. The kraters need a hide flag per species either way.
12. **Litleo and the Nemean Lion.** Ione's Litleo is a cub. The Labors keep Pyroar as the Lion. If the director wants Pyroar's line kept clear until the post-game, swap Litleo for Fletchinder (Fire/Flying), which changes the matchups.

## Director's rulings on the open questions (2026-11-14)

1. Kronion Hill gets its own map, `KallisteRoute1_KronionHill`.
2. Turn on `OW_TIME_OF_DAY_ENCOUNTERS`, so night tables apply.
3. Claim a flag for `B_FLAG_NO_WHITEOUT`. Losing to Kleon continues the story.
4. Keep the name Elaia; the bible fixes it. Never pair it with a professor.
5. The currency stays unnamed for now.
6. The Asclepeion and Pithos get Ichor-only copies of their text. Hoenn's text stays as it is.
7. The Augur's Eye can arrive in the slice.
8. Kleon leaves Kalliste a laurel behind you: he loses to Ione and vows to win "tomorrow", as written.
9. The third starter stays with Daphne. Its fate is decided in Phase 2.
10. Facade stays as TM42.
11. Keep the vanilla starter select screen for the slice.
12. Ione keeps Litleo. Pyroar is the Nemean Lion of the post-game, so meeting its line early pays that off later.
