# Pokémon Ichor: the master story

- **Owner:** Story lead. **Status:** a proposal for the user's approval, written 2026-11-14.
- **What this is:** the spine every script hangs on. It decides who everyone is, what they want, what they're hiding, and when each secret comes out. `design/phase1/SCRIPT.md` (built), `design/phase2/SCRIPT.md` (in progress), `design/LABYRINTH.md` (approved) and the post-game epics (LABORS, UNDERWORLD, ODYSSEY, POSTGAME, in progress) all implement pieces of it.
- **Sources:** `design/PITCH.md` (the bible), `design/LABYRINTH.md`, `design/SYSTEMS.md`, `design/phase1/SCRIPT.md`, `design/phase1/INTRO.md`, `design/MAP_DESIGN.md`, `design/TERMS.md`, `design/research/LAZARUS.md`, and the Aethos dex on branch `claude/aethos-dex-a7c73a`.
- **Where this disagrees with the bible,** the change is listed in §8 and waits for approval. Nothing here changes a game file.

**Status markers,** used through the beat sheet and the foreshadowing map:

| Marker | Meaning |
|---|---|
| **[BUILT]** | In the Phase 1 slice or the boot intro, as shipped. Canon. |
| **[PHASE2]** | Belongs to `design/phase2/SCRIPT.md`. This file says what the beat must accomplish; that file writes it. |
| **[LABYRINTH]** | Approved in `design/LABYRINTH.md`. |
| **[SYSTEMS]** | Specified in `design/SYSTEMS.md`. |
| **[NEW]** | New in this file. |
| **[POSTGAME]** | Belongs to the post-game epics. This file says what each must accomplish. |

**Species** come from the Aethos dex (`design/dex/species/*.yaml` on the dex branch).
- **Aethos species only before the League.** Under dex decision D5 (a), only Aethos species appear before the League, so every team below uses them.
- **Legendaries by role first.** Their names and designs are in review: the user is choosing between three concepts each for the time pair (`design/dex/concepts/time.md`). Staging here never depends on a concept.
- **Replacements.** The story's legendaries are cast from the dex and replace the bible's picks:

  | The bible's pick | The dex's legendary |
  |---|---|
  | Dialga | **the Lord of Time** (Kronolith, #146) |
  | The lake trio | **the three Fates** (Nemira, Lotira and Thanira, #143–145) |
  | (new) | **the Moment** (Kairazor, #147) gains a story role at the climax |

  - The full casting table is in §2.
  - Dex decisions D2 and D3 are still open; §8 asks the user to confirm them.

---

## Contents

1. Logline, themes and the rules of fate
2. Character bibles
3. The beat sheet
4. The foreshadowing map
5. Team Titan
6. Set pieces
7. Draft scenes
8. Proposed changes and decisions

---

# 1. Logline, themes and the rules of fate

## The logline

Every life in Aethos is a thread on the Fates' Loom, and the Oracle reads them all, except yours. Thirteen years ago your mother begged the Fates to unspin your thread, because it was one hour long. Now a gentle healer in a golden mask needs the one person fate can't hold. You alone can carry the sickle that cuts the Fates free, and he means to use it to stop time before his little girl's thread runs out. *Ichor* asks what a life is worth when nobody can tell you how it ends.

## The argument the story makes

**A life is a thread still being spun, not a story waiting to be finished.**

Both of the game's great powers offer certainty, and grief made both of them.
- **The Archon's office** fixes every ending. A thousand years ago a grieving son chained the Fates so that no prophecy could ever be wrong again. His heirs call the result peace.
- **Kronos** abolishes every ending. A grieving father means to stop the Loom, so that no thread is ever cut and his daughter never dies.

The game answers both. Love that won't allow change becomes a tomb. A better story is not the truth. Hope exists only where the ending is unknown, which is why the last thing left in Pandora's jar is a little girl called Elpis.

**The title.** Ichor is the golden blood of the gods. The gods aren't on the Loom: they have ichor instead of threads, because they never end and never change. Kronos wants to give the whole world ichor, and what he gets is a world of statues. Your own thread looks gold too, the color of ichor. Yet it is entirely mortal and entirely free. The Spinner explains it in the Frozen Hour: gold is "what a thread looks like when nobody's decided it yet."

## How each act tests it

| Act | The question | Who answers it, and how |
|---|---|---|
| **I. The Unwoven** (Laurels 1–3) | Can you begin without knowing how you end? | Everyone on Kalliste lives by their reading. Korinna is right half the time, Philon has a knot near the start, and Kleon is racing toward his death. The hero sets out with no reading at all and learns at Eleusa that this makes them the Titans' quarry. |
| **II. Hubris** (Laurels 4–6) | Is a better story worth more than the truth? | Kleon takes a forged fate because it flatters him. Astyra votes its truth-teller into exile on forged evidence. The Titans sell the public a golden age. In Act II, hubris means trying to own your fate: writing yourself a better one. |
| **III. The Loom** (Laurels 7–8, the climax) | Would you stop the world to keep someone you love? | Four parents answer, each differently. Daedalus built a cage for a grieving father. Rhea stood still while fate took two children, then moved to save the third. Phaedon stops the world. Melitta gave her child freedom instead of safety. The hero lets the world stop, then starts it again without knowing whether the girl will live. |
| **The League** | Would you take certainty back if it were offered? | The Archon keeps the last knot of the Fates' chains, and the whole frightened world wants it tied again. You win it, and the two of you untie it together. |
| **Post-game** | What do you do with an unwritten life? | The Labors are glory you earn, not glory you're promised. The Underworld is death without a schedule. The Odyssey is the long way home. |

## The rules of fate

These rules hold everywhere. Every script follows them, and the twists depend on them.

1. **Threads.** Every mortal life is a thread on the Loom of Fate, in a cavern under the Omphalos at Delphoi.
   - The **Spinner** spins it at birth.
   - The **Measurer** marks its length with a red knot.
   - The **Cutter** cuts at the knot.
   - This is the boot intro, exactly [BUILT].
2. **The chains.** A thousand years ago **Medon**, the first Archon, chained the three Fates to the Loom with adamant. Since then they can't stop working, and they can't move a knot. Every knot is fixed, so every true reading comes true.
   - Aethos calls this "the Archon's peace".
   - The public believes the Fates fix destiny willingly. Only Archons, a few scholars and the Titans know about the chains.
3. **Readings.** The Pythia reads threads through the Loom. Local seers such as Halia read them at coming of age.
   - A reading arrives as words, and words can be misread (Kleon's) or forged (Iapetos's). **The thread is always right; the words often aren't.**
   - This is how a world with fixed fate still holds surprises, lies and tragedies.
4. **The Harpe.** Kronos's adamant sickle is the one blade that can cut what the Fates have woven, chains included.
   - Anyone with a thread who holds it is unmade.
   - Medon broke it into three and hid the pieces: at Eleusa, on the Akropolis and in the Telchines' forge at Kaldera.
5. **The gods have no threads.** They have ichor. They can't change fate either; even Zeus answers to the Loom. That is why they test mortals in disguise (theoxenia) instead of fixing things themselves.
6. **The Unwoven.**
   - Once in a thousand years, the chained Spinner did the one thing her chains didn't forbid: she took a thread back before it was woven in. It was the unborn child of Melitta, a bee-priestess of Delphoi, and it had been measured at one hour.
   - On the night the child was born, far away on Kalliste, the Spinner held her spindle still for that hour. The Loom stopped, and the Pythia went blind. The child was born with no thread from the Fates.
   - Since then the child has been spinning their own thread, and it is gold. No one can read it, measure it or cut it. No fate protects it either: the Unwoven could die any day, or live to a hundred.
7. **The Lord of Time** (Kronolith).
   - The Titan of Time sleeps in the deep below the Loom, under the Omphalos, which is the stone he once swallowed in place of his son.
   - With the Fates' power loose and his Harpe in hand, he can stop the Loom. That stops every thread, and so every life. This is the Frozen Hour.
   - Three kinds of being can move in it:
     - **Those outside the Loom:** the Unwoven, and the gods.
     - **Those who stood in the Lord of Time's shadow when it fell:** Phaedon and Hyperion, at the Loom.
     - **Anyone who breaks their own thread:** Kleon.
8. **The cloth runs out.**
   - The Loom has known for a year that every thread in Aethos ends on the same row, the hour the Lord of Time will stop it.
   - Under the chains, that end is fated for everyone the Loom can see. The Loom can't see the Unwoven.
   - The slice's dread is the cloth running out: halcyon days come early, the tide runs backward, birds flee Kronion Hill, seers' eyes are "tired", and the Pythia says only "soon".
9. **After.**
   - Beating the Lord of Time doesn't restart the world. Stopped time waits for a moment, and the Fates have never chosen one: every moment they ever saw was already woven.
   - **The Moment** (Kairos, the Pokémon Kairazor) runs ahead of every thread. Only someone nobody can see coming can catch it, and that is the Unwoven.
   - When the Unwoven seizes it, time goes on past the last row of the old cloth. Nothing beyond that row was ever woven.
   - The freed Fates still spin, measure and cut, but no knot is tied in advance. **Prophecy is over; death isn't.** Every life is now like the hero's.
10. **Medon's Knot.**
    - The Archon keeps a fist-sized knot of black adamant thread in a bronze box. It is Medon's insurance: tied into the Loom, it would fix every knot again, with no chains needed.
    - Whoever beats the Archon on Olympus keeps the box. That is what the League is for.

## The backstory, in order

So every writer agrees on when things happened. The hero is thirteen. Kleon is about the same age.

| When | What happened |
|---|---|
| A thousand years ago | An oracle says a king's death will save Astyra, and **King Kodros** walks into the enemy's spears in a peasant's cloak. His son **Medon** becomes the first Archon.<br>Medon chains the Fates to the Loom, breaks the Harpe into three, hides the pieces, and keeps one knot in a box. |
| Before the story | Rhea (Lampito) buries two children as their readings said. Her third, Kleon, is read "glorious while young", and she hears death. |
| Fifteen years ago | **Daphne**, a young scholar in the Library of Delphoi, finds Medon's record and writes *On the Sickle*. It is banned, and she flees to Kalliste. |
| Thirteen years ago | **Melitta**, a pregnant melissa, is told her baby's thread is one hour long. The Spinner agrees to unspin it, and Melitta flees to Daphne on Kalliste.<br>Months later the baby is born under the old olive in Elaia, and Kydippe delivers it. At that hour the Spinner holds still, the Loom stops, and the Pythia goes blind.<br>**Iapetos**, the prophetes on duty, hears the blind Pythia say only "I can't see." He writes it up as the Unwoven Prophecy. |
| Twelve years ago | **Aristeides**, then the old Archon's envoy, finds Melitta and her baby. She feeds him, and he files a report that they drowned.<br>The report goes back to Delphoi, and Iapetos reads it and knows it is a lie. |
| Seven years ago | **Phaedon** brings his newborn Elpis to Delphoi. The Pythia: "Her thread ends the day the hours stop." Iapetos writes down "Short is her thread. The shears are near."<br>Phaedon writes to his old friend Daphne, and she sends him her book. |
| About six years ago | Kleon goes to the battle school. Rhea, begging at Delphoi for a better reading, meets Iapetos. |
| Five years ago | Iapetos uses Aristeides's lie to become the Archon's Keeper of Records. Elpis's mother dies of a fever that her husband, the best healer in Astyra, can't cure. |
| Two winters ago | A man in a gold mask visits Daedalus [LABYRINTH]. Team Titan forms: Hyperion's crews, Rhea's tunnels, Iapetos's readings. |
| A year ago | The cloth begins to run out, and every thread ends on the same row. The Pythia starts answering in single words. |
| This spring | The halcyon days come early, and the tide runs backward. Iapetos sits in Elaia's square as a scribe, and his grunts dig Kronion Hill. The Klotheia. |

## The motifs

The same images recur so that hindsight has something to hold.

| Motif | Where it runs |
|---|---|
| **Thread, knots, weaving and unweaving** | The intro, the Klotheia, Mom's loom, Ariadne's Thread, the Loom, Medon's Knot. Penelope unweaving in the post-game Odyssey. |
| **Honey and bees** | Mom's hives, the jar labelled NOT FOR {PLAYER}, Komatas fed by bees, the melissai of Delphoi, Melisseer the Delphic bee, the Mistress of the Labyrinth's honey. Bees fed the hidden child in the Cretan cave. |
| **The olive** | Elaia means "olive". The golden thread rises from the old olive's roots, Halia reads threads under it, and Mom gave birth under it. Athena's olive on the Akropolis grew back after it was burned. |
| **Two sickles** | The Harpe cuts and Demeter's Sickle reaps. "They came for a sickle. They didn't know there were two." |
| **Stones** | The swaddled stone Rhea gave Kronos, the Omphalos, Rhea's cairn Pokémon, Kronion Hill. |
| **The hour** | The klepsydra, sundials, the Stair of Hours, "the day the hours stop". |
| **Masks** | Kronos's gold mask, Iapetos's tragic mask, Rhea's closed helmet, the Dionysia's masks. Every major unmasking is a choice. |
| **Handwriting** | Iapetos's little hook against Alethea's signature. The lie is signed with a hook; the truth with a name. |
| **The lullaby** | Elpis hums it, it is Phaedon's theme, and Daedalus's music box plays it. The Frozen Hour ticks to it. It never resolves until Elpis finishes it in the last act (§6, music). |

---

# 2. Character bibles

Each bible gives the same parts: role, what they want, what they fear, their secret, their arc beat by beat, their team, their look, and three lines in their voice. Teams are Aethos species with level targets for Balance. A team marked "ace" lists its strongest Pokémon last, as the trainer data will.

## The hero, "the Unwoven"

- **Role.** The player. The default names are Theo and Ianthe. They are thirteen, Melitta's only child, raised in Elaia on Kalliste. A silent protagonist: their voice is their choices.
- **Wants.** At first, a partner and the open road. Then to stop the Titans, then to find Mom, and at last to keep the world moving.
- **Fears.** Never spoken, but the story presses on two:
  - that being Unwoven makes them a tool, as the Titans, the Fates and the Archon each want to use them;
  - that their freedom is a fluke someone else paid for.
- **Secret** (they don't know it):
  - Their thread was measured at one hour.
  - Their mother begged the chained Spinner, who unspun it.
  - They were born under the old olive in Elaia's square at the hour the Loom stood still. The thread they've had since is their own, and it's gold.
- **Arc.**
  1. [BUILT] The Klotheia. Halia's spindle stops on them. They get a partner and beat (or lose to) Kleon.
  2. [PHASE2] At Eleusa, Daphne tells them what they are, but not why. "That part's your mother's to tell." The Titans have a word for them: Unwoven.
  3. [NEW] At the Dionysia they watch an actor play them on stage, carrying a sickle to the Loom. The Titans have written them into their gospel.
  4. [NEW] On the Akropolis, Kleon tells them the Titans don't really want the fragments. They want the hero. Every step after the Titans brings the Titans' plan closer. That is the midpoint.
  5. [NEW] At Kaldera they learn why: only someone with no thread can hold the Harpe. In the same hour, a letter says Mom is gone. This is the low point.
  6. [LABYRINTH] At Knossa they free Asterion. The kind healer unmasks and asks them to carry the sickle.
  7. [NEW] At Delphoi, Mom tells them everything and hands them the honey jar.
  8. [NEW] At the Loom they cut the Fates free, knowing exactly what Phaedon will do with it, because the Fates ask and because nothing else will save anyone.
  9. [NEW] They walk the Frozen Hour alone. They wake the Fates, show a father the truth about his daughter, and go home.
  10. [NEW] They climb the Stair of Hours and beat the Lord of Time. Then they seize the Moment as it runs past and wake the world, without knowing whether Elpis will wake with it.
  11. [NEW] On Olympus they win Medon's Knot, the power to make fate certain again, and untie it with the man who lost it to them.
  12. [NEW] At the next Klotheia, Daphne asks her old question again, and the hero has a new answer: **WE'LL SEE.**
- **Team.** The player's own. The story gives them nothing forced, beyond what Mom and the gods give them (SYSTEMS §10).
- **Look.**
  - [BUILT] A traveler's petasos and cloak.
  - In the Frozen Hour, theirs is the only colored sprite on screen until Kleon wakes.
  - Optional: after the Frozen Hour they wear the cloak Mom finished, honey-gold. This is a palette swap, decision S13.
- **Voice.** Their three defining choices:
  - At the Loom: **"Cut the chains?" YES.**
  - On Olympus: **"Untie Medon's Knot?" YES.**
  - At the epilogue: **"Which came first? …WE'LL SEE."**

## Mom (Melitta)

- **Role.** The hero's mother, a beekeeper of Elaia. She was once a **melissa**, one of the bee-priestesses who served the Pythia at Delphoi. The Pythia herself was called "the Delphic Bee". The melissai were the only mortals who went down to the Loom: they carried honey to the chained Fates, because nobody else would feed them.
- **Wants.** For her child to live. Not long, not safe, just freely. And never to go back to Delphoi.
- **Fears.**
  - That the Archon's law will find them.
  - That she chose wrong. She gave her child no fate, which means no promise either.
- **Secret.**
  1. Thirteen years ago, pregnant, she carried honey down to the Loom. The Measurer measured her baby: **one hour.**
  2. She begged. The Spinner said she couldn't change what she'd spun, but she could take it back.
  3. Melitta fled to the edge of the map, where her friend Daphne had already hidden. She gave birth in the dark under the old olive in Elaia's square. Kydippe the midwife heard her and came out in her nightdress.
  4. At that hour the Spinner held still, the Loom stopped, and the Pythia went blind.
  5. Melitta has lied about it ever since. Her "pilgrim" story in the slice is a deflection: "Or the night before. Or the week after."
  6. The honey jar labelled NOT FOR {PLAYER} is the last of her Delphic honey, kept for the three who let her child go.
  7. The smaller secret, for comedy: she has never lost at knucklebones because her Melisseer hums the throws. Its kind hums what will happen tomorrow (dex #48).
- **Arc.**
  1. [BUILT] Festival morning. The Talaria. The pilgrim lie. The half-woven cloak: "you'll need it someday." The jar.
  2. [PHASE2] At the harbor she sees you off.
     - She doesn't cross the water.
     - She says one line she means more than you know: "Wherever you end up, come back up the hill. That's all."
  3. [NEW] Act II, off-screen.
     - Iapetos has worked out who she is, and he sends Titanborn to Elaia to bring the melissa to Delphoi as leverage.
     - Her bee hums it the day before. She's gone by midnight, with the honey jar.
     - Kydippe's letter reaches you at Kaldera: the low point.
  4. [NEW] Act III, Delphoi. She hid in the one place no one would look for a runaway bee: the hive.
     - The Pythia, her old sister-melissa, has sheltered her.
     - At the Kastalian spring she tells you the truth and gives you the jar. "Come back up. Every time."
  5. [NEW] In the Frozen Hour she stands frozen at the top of the Omphalos stair, hands clasped, waiting.
  6. [NEW] When time restarts, she's the first face you see. "You came back up."
  7. [NEW] Epilogue: the next Klotheia, as it began. "Did you fill your water clock?"
  8. [SYSTEMS] In the post-game, the theoxenia finale: Zeus and Hermes at her door in a storm.
- **Team.** Melisseer (her bee) as a follower in her scenes. She doesn't battle. If the post-game ever wants a Mom battle, it should be knucklebones.
- **Look.**
  - At home: a beekeeper's straw hat with the veil pushed back, an apron, honey-stained hands.
  - At Delphoi: a pale-gold melissa's veil with a honeycomb hem. The player has never seen it.
- **Voice.**
  - "Stubborn. You get that from me." [BUILT]
  - "I'm sorry I lied. I'm not sorry I did it."
  - "Come back up. You hear me? Every time."

## Professor Daphne

- **Role.** The philosopher-naturalist of the Akademia grove. "Every myth is a memory of a Pokémon." She is the hero's mentor, and Melitta's oldest friend.
- **Wants.** To understand, and to be wrong in interesting ways. "A guess is only a question that's gotten too confident" [BUILT].
- **Fears.** Being right about something terrible. Her whole philosophy is a flight from certainty: a Pythia is never wrong, and Daphne prizes being wrong.
- **Secret.** She has two.
  1. **She knows why you have no thread.**
     - Fifteen years ago she was a young scholar in the Library of Delphoi, where she found the record of Medon's chains.
     - She wrote a book about the Harpe, *On the Sickle*. The Archon's office banned it.
     - She fled to Kalliste and rooted herself in its grove. In myth Daphne fled Apollo and became the laurel: rooted, unchanging.
     - Two years later Melitta came to her, pregnant and terrified. Daphne gave her the island and kept her secret for thirteen years.
  2. **Her book is the Titans' map.**
     - The list on the Kronion Hill tablet is her book's chapters, in order.
     - She sent the manuscript years ago to her dearest friend from her student days in Astyra: a young healer named Phaedon. His newborn daughter had been read as doomed, and he wanted to know whether any story had ever changed a fate. She told him one had.
     - That is why she "went very quiet" over the tablet [BUILT]. The tablet's back held something worse (§3, Act I).
- **Arc.**
  1. [BUILT] The intro speech, the starters, "Which came first?"
  2. [BUILT] The tablet: "I have a guess."
  3. [PHASE2] At Eleusa she crosses the sea for the first time in thirteen years, seasick and in new sandals that pinch. She tells you what you are but not why. She confesses about the book, reads the tablet's back aloud ("Bring word of the Unwoven") and gives you the Star Chart. "I've been a tree on that island for thirteen years."
  4. [NEW] Act II, Astyra. She works in the Library to unwrite her book. She is close with Phaedon and Elpis, and the player sees how much she loves them: "Still being wrong?" "Constantly."
  5. [NEW] At Kaldera she has come to see the forge she once wrote about. She's there when Kydippe's letter arrives. "She's done this before. Find her."
  6. [NEW] Act III, after Knossa. Alethea writes to her that Kronos is Phaedon. Daphne's letter back: "I know. I'm staying with Elpis. Someone should. She thinks her papa's gone to buy her a real bull."
  7. [NEW] In the Frozen Hour she sits frozen at Elpis's bedside, the olive story open in her lap.
  8. [NEW] At the resolution she is the one who heard Elpis finish the song.
  9. [NEW] Epilogue: she gives the third krater to the one who came late, Elpis, then asks her question one more time.
- **Team.** Hierolive (the sacred olive, the dex's suggested intro Pokémon) as her ace, with Sophowl and Chelyra. She battles only if the post-game wants it.
- **Look.**
  - A laurel-green chiton, a bark-brown shawl and a laurel sprig in her hair. Ink on her fingers.
  - Barefoot in the grove [suggested]. From Eleusa on she wears new sandals.
- **Voice.**
  - "A guess is only a question that's gotten too confident." [BUILT]
  - "They're digging where I told them to dig."
  - "I've been a tree on that island for thirteen years. I think it's time I walked."

## Alethea

- **Role.** Daphne's apprentice, the hero's friend, the Pokédex's builder and an excavator. Her name means *truth*.
- **Wants.** The truth, dug up and believed. To be taken seriously by people who see a girl from a tiny island.
- **Fears.** That truth doesn't matter: that people will always choose the better story.
- **Secret.**
  - Her own Klotheia reading, three years ago, wasn't "exhausting" [BUILT: that was her joke]. Halia told her: **"You'll tell the truth all your life, and they'll call you a liar."** It is Cassandra's curse.
  - Her tic, "Truthfully, …", isn't a habit. She labels the truth in advance because she expects not to be believed.
  - And for one act she keeps a secret against her own nature. She saw the back of the Kronion tablet, and Daphne asked her to wait.
- **Arc.**
  1. [BUILT] The grunts, the tablet, the Augur's Eye, "Truthfully, but badly."
  2. [PHASE2] At Emporion she gives you the Trowel. She notices a little hook under the Archon's seal on a public notice, and says one line about it.
  3. [PHASE2] At Eleusa: "I wanted to tell you. Truthfully, I nearly did. Twice."
  4. [NEW] At Thyrsa the Dionysia's program is signed with the same little hook. She starts a list.
  5. [NEW] In Arkadia she tells Kleon his new prophecy is forged. He doesn't believe her. "People don't. I'm used to it. Truthfully, I'm not."
  6. [NEW] Astyra.
     - She takes her evidence to the Archon's Stoa. The Keeper of Records answers with forged "proof" that she faked it, and calls an ostracism.
     - The city votes her into exile. She is the midpoint's truth-loses beat.
     - That night, outside the walls, she tells you her real reading.
     - Then the Akropolis: "The Akropolis is above the city. Technically." At its gate she names the forger: the Archon's own Keeper.
  7. [NEW] Act III. She is exiled only from Astyra, so she meets you at Kythera and reads Knossa's frescoes above ground [LABYRINTH].
  8. [NEW] At Lakonia she reads the scraped wax of Elpis's tablet. Under the forgery is the Pythia's real line: *"Her thread ends the day the hours stop."* She writes it underneath in her own hand and signs it.
  9. [NEW] In the Frozen Hour she stands frozen at the top of the Omphalos stair beside Mom, holding up a lamp. In Elpis's room, it is her handwriting that tells Phaedon the truth.
  10. [NEW] After the climax she prosecutes Iapetos. The city votes again, and the ostraka come out of the urn with his name. Her exile is lifted, and the new Archon makes her Keeper of Records.
  11. [NEW] Epilogue: she is writing it all down. "Kleon asked me to leave him out of it. I said no." And her last line, the last line of the game: "…I'm writing that down."
- **Team.**
  - **Skylaps**, the storm-hound, is her ace. It is Laelaps, the hound fated to catch everything it chases, and it was seeded in the slice as Hisuian Growlithe.
  - **Iapetos's ace is Kerdovix,** the vixen fated never to be caught (seeded as Nickit). Truth and the liar are the myth's own unsolvable chase. Zeus ended it by turning both to stone, and the Frozen Hour does the same.
  - The rest of her team: Plouteras (a digger), Sophowl (an owl) and Narkeray (the torpedo ray, the philosopher who numbs you with questions). Akropolis partner levels are about 34–36.
- **Look.** Dusty knees and rolled sleeves. Two trowels on her belt ("three"), a satchel of tablets, an oil lamp, and her hair tied back with a cord.
- **Voice.**
  - "A riddle. I hate riddles. They're just lies wearing hats." [BUILT]
  - "They believed the better story."
  - "Truthfully? I hope they revise it. Then they'll have to read it first."

## Kleon

- **Role.** The rival, raised in the Lakonian battle school. His name comes from *kleos*, glory.
- **Wants.** To be remembered.
- **Fears.**
  - That he's ordinary. Without the prophecy he's nobody, and the prophecy is the only thing that made him special.
  - Underneath that, he is terrified of dying. He just won't let it show.
- **Secret.**
  - He doesn't know it, but **his mother is Rhea**, the Titan admin.
  - He was born early and small. When the Lakonian elders came to look at the baby, his mother had her Kourodin dance in the yard and clash their shields, so nobody would hear him cough. It is Rhea's myth, in which the Kouretes hid infant Zeus's cries from Kronos. It is also why he has spent his life proving he isn't weak.
  - His prophecy was never about death. His mother misread it.
- **Arc.**
  1. [BUILT] He grabs the starter that beats yours and battles you in front of the festival. "Glory first. The dying part can wait." He loses to Ione and vows to win tomorrow.
  2. [PHASE2] Your shipmate on the crossing, warm and loud. "My mother writes every week. Two lines. Lakonian."
  3. [PHASE2] At Eleusa he fights beside you once, a double battle against Titanborn. It is the bookend to the Stair of Hours.
  4. [NEW] At the Dionysia he sits in the audience. The Titans wrote *you* a play. Everyone has a story about you.
  5. [NEW] In Arkadia, Kallisto beats him six to nothing under the new moon without once looking at him. Her prophecy had been forged to make her merciless that night. Iapetos steps out of the cypresses with "a better thread", and Kleon takes it and goes with him.
  6. [NEW] On the Akropolis he battles you as a Titan agent, his helmet pushed back ("Heroes don't hide their faces"). He loses, and tells you the truth anyway: they want you. "Don't make it a thing."
  7. [LABYRINTH] Knossa.
     - He hunts Asterion and gets flattened in Ring V.
     - At the heart he tries to kill the freed bull. You stop him and beat him.
     - The tablet in Iapetos's hand sends him home.
  8. [NEW] Lakonia.
     - His mother comes home and takes off the helmet.
     - His real prophecy was *"glorious while young, and his glory will not die."* There was never any death in it.
     - He melts the forgery in the hearth, gives the real tablet back to his mother ("Keep it. I don't need it. You do") and battles you clean: no fate either way, for the first time.
     - His mother gives him her Kourodin.
  9. [NEW] At Delphoi he holds the Omphalos gate beside his mother and is frozen there, mid-swing.
  10. [NEW] In the Frozen Hour he breaks his own thread by will: "I pulled. It hurt. I pulled anyway." He is the first person to become Unwoven by choice.
  11. [NEW] On the Stair of Hours he fights beside you against Kronos and Hyperion. Then the stair begins to crumble and the blind Hyperion can't find the edge. The song is up the stair, and Kleon carries his enemy down it, where no one will ever see. "Nobody's going to sing about this. …Good."
  12. [NEW] Epilogue: second in the Klotheia footrace, to a Wooloo. His mother says "Good."
  13. [POSTGAME] The Labors: glory earned, not fated. "Herakles had twelve. Let's see about us."
- **Team.** He always leads with the starter that beats yours.

  | When | Team (levels are targets) |
  |---|---|
  | Akropolis | Starter, stage 2 (39); Alekrow (36); Hoplomex (36); Cairnolith (37), a Titan gift ("It's from Kronion Hill. Like you.") |
  | Knossa | Starter, final stage (54); Hoplektor (52); Dorydrake (52); Nemeleon (51); Laolith (51). This replaces LABYRINTH's placeholder species, as D5 (a) requires. |
  | Lakonia | Starter, final stage (57); Hoplektor; Dorydrake; Nemeleon; Hoplomex; **Kourodin**, his mother's (56) |
  | Stair partner | Starter, final stage; Hoplektor; Kourodin |
- **Look.** A Lakonian red cloak and bronze greaves a size too big. Short hair. As a Titan agent he wears the bronze helmet pushed back on his head like a cap; he never pulls it down.
- **Voice.**
  - "So I'm in a hurry. Glory first. The dying part can wait." [BUILT]
  - "Everybody's telling me the truth! I'd like a better one!"
  - "Nobody's going to sing about this. …Good. Go on. I've got him."

## Phaedon, who is Kronos

- **Role.** The healer of Astyra's Asclepeion, and the masked master of Team Titan.
- **Wants.** That no thread is ever cut. Above all, that his daughter's isn't.
- **Fears.** The knot. The one wound he can't close. And uncertainty, which is worse to him than death: he can't bear not to know.
- **Secret.**
  - He is Kronos [LABYRINTH: he unmasks by choice at Knossa].
  - There is a deeper secret, which he doesn't know: **his daughter's oracle was forged.**
    - Seven years ago he took his newborn to Delphoi.
    - The Pythia said: *"Her thread ends the day the hours stop."*
    - The prophetes who put her words into verse was Iapetos. He wrote down instead: *"Short is her thread. The shears are near."*
  - Iapetos needed a sincere man with steady hands and a grief to build a movement on, and he made one.
  - Phaedon set out to stop the hours so his daughter would never die. Stopping the hours is the only thing that could ever end her thread.
- **Arc.**
  1. [NEW, with LABYRINTH seed 9] Astyra, Act II.
     - He is the nurse of the Asclepeion, and every heal in the city is his. "Easy now. There. Every hurt closes, if you let it."
     - At his hearth: "I've stopped asking."
     - He is warm with Daphne. His daughter has a clay bull and hums a lullaby that never ends.
  2. [NEW] On the night of the Akropolis raid he's at the Asclepeion treating the wounded, Titans and guards alike. In hindsight, he was mending his own soldiers.
  3. [LABYRINTH] At Knossa he completes the Harpe under Daedalus's stars. He calls the bull "Starry".
     - He unmasks to ask you to carry the sickle.
     - [NEW] If you show him the sealed tablet from the archive, he won't look: "Iapetos said you'd bring me a tablet. He said Daphne's girl forged one."
  4. [NEW] At Delphoi he descends to the Loom.
     - He predicted everything. You come down. You see the Fates. You cut them free because you're kind.
     - Then he speaks to the Lord of Time, and the world stops.
  5. [NEW] In the Frozen Hour he doesn't go to the top of the stair. He goes to his daughter.
     - You find him on the floor beside her frozen bed, holding her hand. "It's not a garden. I thought it'd be a garden."
     - You show him the tablet, and this time he reads it.
     - He understands that he made her prophecy true. He believes waking the world will leave her dead. "This way she's here. Humming."
  6. [NEW] On the Stair of Hours he fights you anyway, beside Hyperion. Then he stands aside, because the Lord of Time never listened to him either: "It just wanted the same thing I did." "I'll stand here and hope you lose."
  7. [NEW] At the resolution, his daughter wakes and finishes the song.
     - He tells her no one can read anyone's thread any more, that he doesn't know how long she has.
     - She says: **"Then my thread isn't finished yet."**
  8. [NEW] His sentence. He asks for nothing. Ione the Hearthkeeper asks for him: in myth, a suppliant at Hestia's hearth can't be harmed. He is exiled to Kalliste, to heal at Akti's Asclepeion under Ione's roof for the rest of his life. Every heal in Akti in the post-game is his. "Easy now. There."
  9. [NEW] His punishment and his mercy are the same thing: an ordinary life, with an unknown end, watching his daughter. "Every morning I look at her and I don't know. It's unbearable. It's wonderful."
- **Team.** Earth-born, as Team Titan's are, apart from one exception that gives the man away. He battles only once, on the Stair (§7.8).

  | Pokémon | What it says about him |
  |---|---|
  | **Kolossard** | Talos the bronze giant, whose whole life ran in one vein stoppered with a nail |
  | **Bouldyphus** | Sisyphus, the man who chained Death so that nobody died |
  | **Panacoil** (his ace) | The healer serpent of Asclepius, whose kind once raised the dead and was punished for it (dex #76). His own partner, the one that healed your Pokémon in Astyra. |

  - Levels about 60 for the multi battle.
- **Look.**
  - As Phaedon: a plain white healer's chiton, a gray-streaked beard, kind tired eyes, and a clay bull on his belt.
  - As Kronos: a smooth gold mask with serene closed eyes, a black cloak and a sickle clasp.
- **Voice.**
  - "Easy now. There. Every hurt closes, if you let it."
  - "I'm sorry. I'd rather you saw my face for this part." [LABYRINTH]
  - "Go. I won't stand in your way. I'll stand here and hope you lose."

## Elpis

- **Role.** Phaedon's daughter, about seven. She is often sick: tired all the time, with a cough. Her name means *Hope*, the last thing left in Pandora's jar.
- **Wants.** To meet the real Starry. To see the sea. To get to the end of her song: she always falls asleep before the last line.
- **Fears.** That Papa is sad because of her.
- **Secret.**
  - She knows her prophecy, in a child's paraphrase: "I'll go when the hours stop. Papa says hours don't stop. So I'll never go."
  - She has been comforting him, not the other way round.
  - She has a bronze music box on her shelf, labelled "From Papa's friend under the island". It plays her lullaby, and it is Daedalus's work. In the Frozen Hour its spring keeps running when nothing else does, and it is the ticking you hear.
- **Arc.**
  1. [LABYRINTH seed 8, NEW lines] Astyra: Starry, the lullaby, "Papa's going to make him better."
  2. [NEW] After the Akropolis raid: "Papa says the Titans are sad people."
  3. [NEW] Act III, before Knossa: worse, in bed, with Daphne reading to her.
  4. [NEW] In the Frozen Hour, frozen mid-hum while her music box ticks.
  5. [NEW] At the resolution: "Papa! You missed it. I got to the end." Then her line.
  6. [NEW] Epilogue: she comes to the Klotheia from Akti, too young and too late, and gets the third krater anyway. Halia can't read her thread. "Isn't that grand?"
- **Team.** None yet. An Ophidrop, the temple snakelet from her father's garden, sleeps on her bed. In the epilogue she gets the third starter.
- **Look.** Small and pale in a shawl too big for her, holding a clay bull.
- **Voice.**
  - "This is Starry. Papa brought him from an island." [LABYRINTH]
  - "I'll go when the hours stop. Papa says hours don't stop."
  - "Then my thread isn't finished yet."

## Hyperion

- **Role.** A Titan admin, the Hand. He runs the dig crews and the forge, and he is Fire and Rock. Hyperion was the Titan of watchfulness and light, father of the sun, the moon and the dawn.
- **Wants.** To stay in the light. And to keep his crews fed: they're dockhands, quarrymen and orphans he pulled off Emporion's docks, and he calls them his kids.
- **Fears.** The dark. Losing.
- **Secret.**
  - **He's going blind.** His prophecy said *"You'll end your days in the dark."*
  - He was a champion pankratiast, unbeaten. He fights at noon, by the glare of his fire Pokémon, because he can barely see anything else.
  - Phaedon promised him the golden age would be one endless noon.
  - Iapetos sharpened his oracle. The original, which the player can dig up as an optional prophecy fragment, reads: *"You'll end your days in the dark, and be glad of it."*
- **Arc.**
  1. [BUILT] Off-screen. "Hyperion's going to roast us." / "He'll roast us literally."
  2. [PHASE2] At Eleusa he leads the theft from the dark sanctum. It is the first admin battle. He squints at the player: "Can't see a thing in here. Who builds a temple with no windows?"
  3. [NEW] At Kaldera, his home island, he takes the third fragment from the Telchines' sea-cave forge.
     - He sets off the caldera and fights you in the glare of the eruption.
     - He's brash and funny, and protective of his grunts: "Petros! Behind me!"
  4. [LABYRINTH] At Knossa he guards the forge in Ring VI. "You're late, Unwoven."
  5. [NEW] He stands in the Lord of Time's shadow at the Loom, so the Frozen Hour doesn't freeze him.
     - On the Stair of Hours he realizes the eternal hour has no light in it: it's gray. "He said noon forever. It's not noon. It's not anything."
     - He fights anyway, because he gave his word.
  6. [NEW] After the multi battle he can't find the stair's edge, and Kleon carries him down. "Who's got me?" "Nobody. Walk."
  7. [NEW] When time restarts, the sun comes up over Delphoi. Hyperion turns his face to it. "There it is."
  8. [NEW] His sentence, at Talos's request: "Send him to my forge. He knows fire. He'll learn the rest." In the epilogue he is nearly blind and working iron by feel and by the sound of the hammer, with Petros and Amathos on the bellows. Glad of it.
- **Team.** Light and fire, around a buried giant: his ace is the thing he fears.

  | When | Team (levels are targets) |
  |---|---|
  | Eleusa | Kapnub (22); Kaminoo (22); Pebblith (23) |
  | Kaldera | Taurivet; Laolith; Pyrapod; **Gigantomb** (ace, about 44) |
  | Knossa | Taurivet; Laolith; Pyrapod; Hymnaria; Gigantomb (50–53). This replaces LABYRINTH's placeholder species. |
  | Stair, multi | Taurivet; Hymnaria; Gigantomb |

  - Gigantomb is the giant buried under an island, breathing smoke (dex #84, "Admin Hyperion's ace").
  - He has no Apotheosis [LABYRINTH].
- **Look.** Huge and bare-armed, with burn scars and a sun-disc breastplate. His Corinthian helmet is pushed back like a crown. He always squints; by Act III his eyes are clouded.
- **Voice.**
  - "I roasted them for it. Mostly not literally." [LABYRINTH]
  - "Can't see a thing in here. Who builds a temple with no windows?"
  - "There it is." (the dawn)

## Iapetos, who is Keeper Lykophron

- **Role.** A Titan admin, the Voice: recruitment, readings and the archive.
  - In public he is **Lykophron, Keeper of Records** to the Archon. The historical Lykophron wrote an obscure poem that was all Cassandra's prophecy.
  - Before that he was a **prophetes at Delphoi**, one of the priests who turned the Pythia's raw words into verse.
  - In myth, Iapetos fathered Prometheus and Epimetheus: forethought and afterthought, the one who writes before and the one who rewrites after.
- **Wants.** **To write the last draft of the world.**
  - He learned at Delphoi that what the faithful heard was his writing, not the god's.
  - In a world where nothing changes, the last version written stays forever.
  - He doesn't care which side wins, only that he's the author.
- **Fears.** Being revised. Being caught. The truth, which is a draft he didn't write.
- **Secret.** Almost everything. He is Team Titan's real architect.
  1. He was the prophetes on duty in the blind hour. The Pythia said only "I can't see." He wrote it into the **Unwoven Prophecy**, a forgery that became Team Titan's gospel: a child born without a thread shall carry the sickle to the Loom.
  2. He read the Archon's envoy's report that a runaway melissa had drowned. He knew a forgery when he saw one. He held that lie over Aristeides and used it to get his post.
  3. He forged Elpis's oracle to make Phaedon. He forged Kallisto's to break Kleon, and Kleon's to recruit him. He sharpened Hyperion's.
  4. He sat at the Klotheia as a traveling scribe and watched Halia's spindle stop (proposed slice seed, §8.2).
  5. He forged the Archon's seal to stand the guard down the night of the Akropolis raid.
- **Arc.**
  1. [proposed slice seed] The Klotheia's traveling scribe: "May I tell you something true? You're going to be in my book."
  2. [PHASE2] Emporion. His hook sits under the Archon's owl on a public notice.
  3. [NEW] Thyrsa, the Dionysia. He stages *The Unwoven* with masks stolen from Thespis, and the whole amphitheater is entranced. You see yourself on stage. The satyr play breaks it.
  4. [NEW] Arkadia, in a white tragic mask: "Here's a better thread." Kleon goes with him.
  5. [NEW] Astyra, bare-faced, as Keeper Lykophron, he prosecutes Alethea. His tic gives him away to anyone listening: "May I tell the Assembly something true?" The city votes her out.
  6. [NEW] The Akropolis gate: his forged order, with the hook under the seal.
  7. [LABYRINTH] The Knossa archive: shelves of "Revised." prophecies, and his draft of Kleon's ("Better. He'll run straight at it.").
     - [NEW] Add one sealed tablet to the shelves: **"ELPIS, DAUGHTER OF PHAEDON. Revised."**
  8. [NEW] Lakonia. He comes for the deserter Rhea and finds her son beside her. He battles you and slips away: "Every draft has a next draft."
  9. [NEW] The Frozen Hour. He planned to be at the Loom, but Lakonia delayed him, and he is frozen at his desk in the Stoa. His stylus stopped two letters before the end of his own name, on the "Decree of the Golden Age": *"…its Keeper shall be Iape-"* You take the tablet.
  10. [NEW] After the climax he turns his coat at once: forged records show him the Archon's loyal man all along.
      - Alethea tries him before the Assembly, with the frozen decree, the archive tablets and every fragment you dug up. The ostraka come out with his name, in hundreds of hands.
      - His parting shot: "Ask your Just Archon about Kalliste." It sets up the League.
  11. [POSTGAME] Suggested for the Odyssey: in exile, he writes songs for the Sirens. "Come closer. May I tell you something true?"
- **Team.** Dark and Psychic, with a liar's story in every slot. Lakonia levels are about 55.

  | Pokémon | What it says about him |
  |---|---|
  | **Prosomime** | The theater mask, his tool at the Dionysia (dex #63) |
  | **Hyphantis** | Arachne, who wove the gods' crimes into a tapestry |
  | **Pithound** | The cynic in a jar who searched for an honest man and never found one |
  | **Enigmaw** | The riddling sphinx, whose words kill |
  | **Kerdovix** (ace) | The vixen fated never to be caught |
- **Look.**
  - As Keeper: neat and thin, with a trimmed beard and the Keeper's blue-bordered himation. A wax tablet hangs on a cord and a stylus sits behind his ear.
  - As Titan: a white tragic mask.
  - In both looks his right hand is ink-dark. That is the visual tell, and the sprite artist should keep it.
- **Voice.**
  - "May I tell you something true?"
  - "Here's a better thread."
  - "Every draft has a next draft."

## Rhea, who is Lampito

- **Role.** A Titan admin, the Ground: logistics, tunnels, and keeping the Labyrinth's chain. Her real name is Lampito, a Lakonian woman. **Kleon's mother.**
- **Wants.** That her last child's thread isn't cut.
- **Fears.** Standing still again.
- **Secret.**
  1. She had three children. The first two were read at birth: each would die before their mother. Both did, one of fever and one in war, and each death proved that fate can't be fought. "I stood still and let it" [LABYRINTH].
  2. The third was Kleon. She hid his cough from the elders with clashing shields and gave him to the battle school at seven.
  3. When the Oracle's verse for him came, she heard death in it, because she'd buried two. The verse said *glorious while young.*
  4. At Delphoi, begging for a better reading, she met a prophetes who said he knew a man who wanted to stop the cutting. That was Iapetos.
  5. She never told Kleon. She wears a closed Corinthian helmet and speaks the way Lakonians do: very little.
  6. When Iapetos recruited her own son and pointed him at a monster, she began to hate him.
- **Arc.**
  1. [NEW] The Akropolis.
     - She leads the raid up the old spring stair. Her Pokémon tear out Athena's sacred olive by the roots to reach the second fragment. She battles you and wins the fragment anyway.
     - She watches her son lose. When a grunt shoves him: "Leave the boy." / KLEON: "Who asked you?" / RHEA: "…No one."
  2. [LABYRINTH] Knossa. She holds Asterion's chain at the heart. Her son bursts in to kill the bull.
     - Ordered to seal the house with everyone inside, she leaves the threshold open: "I won't stand still and seal someone else's in a hole." She can't say *mine*.
     - In myth, on Crete, Rhea saved her last child from Kronos. Here she does it again.
     - [NEW stage direction] She looks at Kleon a long time before she pulls the lever.
  3. [NEW] Lakonia.
     - She deserts and comes home, and finds her son waiting to ask Iapetos questions. She takes off the helmet.
     - "I read it wrong. I'd buried two. I heard what I was afraid of."
     - She gives him her Kourodin: "It hid you once."
  4. [NEW] Delphoi. She fights beside you at the Omphalos gate against Titan Gigas, her first battle on your side. She is frozen with her arms out in front of her son.
  5. [NEW] After the climax she surrenders to the Archon's guard herself. Her sentence is house arrest in Lakonia, which she treats as a promotion.
  6. [NEW] Epilogue: she comes to the Klotheia with Gylippos to watch her son run. "Second. Good." / "Next year, first. Or not. We'll see."
- **Team.** Ground, and every slot tells her story.

  | Pokémon | What it says about her |
  |---|---|
  | **Cairnolith** | A cairn is a grave-heap, and she carries it for the two she buried. It is also the swaddled stone Rhea gave Kronos. |
  | **Geogrip** | Antaeus, a son who was strong only while he touched his mother |
  | **Plouteras** | The blind god of wealth, Demeter's child |
  | **Kourodin** (ace) | The shield-dancers who hid a baby's cry from Kronos. It lives in the Lakonian battle school (dex #104), a fair clue to where she comes from. |

  - Akropolis levels are about 40.
  - At the Delphoi partner battle she has Laolith, Geogrip and Kourodin, about 58.
- **Look.** A full bronze Corinthian helmet with the sickle on its cheek-pieces, never off until Lakonia. A Lakonian red-brown cloak, and a long chain wrapped around her forearm. Unmasked: gray-haired and square-jawed, with Kleon's eyebrows.
- **Voice.**
  - "Leave the boy."
  - "A prophecy took my children. I let it. I stood still and let it." [LABYRINTH]
  - "Second. Good."

## The Archon, Aristeides the Just

- **Role.** The Champion, servant of Zeus, keeper of the Archon's peace, and keeper of the box.
- **Wants.** Peace. Order. A world where nobody is to blame for anything, because it was written.
- **Fears.** Chaos. And his own responsibility: the one act of his life he can't blame on fate.
- **Secret.**
  1. Twelve years ago the old Archon sent him to find a runaway melissa. He found a beekeeper on Kalliste and a baby who never cried. She didn't ask his name. She sat him down and fed him bread and the good honey.
  2. You don't harm the house that feeds you. That law of Zeus Xenios is older than Archons. He went home and wrote that she had drowned, with her child. It was his first lie, and he wrote it badly.
  3. Iapetos read the report and has held it over him ever since. That is how the Keeper got his post, and how the Titans found the hero. It is also why a girl was voted out of his city and he said nothing.
  4. He keeps **Medon's Knot.**
- **Arc.**
  1. [PHASE2, light] Act I: the Archon is a name in proclamations, the man of the Archon's peace.
  2. [NEW] Act II, Astyra. Every seer says every thread ends on the same day, and his proclamation is: "If it is written, meet it with dignity." He looks a determinist villain, and that is deliberate misdirection.
     - He presides over Alethea's ostracism: "The people have voted. It is written."
     - He looks at the player too long. "You're from Kalliste." "…Hm."
     - The night of the raid, the guard stands down on an order bearing his seal. He doesn't deny it.
  3. [NEW] At Delphoi he arrives at the sanctuary gate with his guard as the Omphalos opens, too late again, and is frozen mid-stride.
  4. [NEW] After the climax the world is frightened: no oracles, merchants hoarding grain, Lakonia sharpening spears.
     - He takes the box to Olympus, as the law says, to answer any challenger before he carries the Knot to Delphoi at the new moon.
     - Iapetos's parting shot makes the player want to ask him about Kalliste.
  5. [NEW] Olympus. He tells the whole story. He fights you with everything he has, because a just man doesn't go easy.
     - Beaten, he gives you the box and the office: "Gods help you."
     - The Knot won't come undone for one pair of hands. "It took a grieving man a whole night to tie that. It'll take two to undo it. I'll hold. You pull."
  6. [NEW] Afterward he goes home to his father Lysimachos, who collects ostraka with his son's name on them [SYSTEMS]. "He'll be pleased. He was always sick of hearing me called the Just."
- **Team.** Zeus's: law, and hubris punished.

  | Pokémon | What it says about him |
  |---|---|
  | **Lebetron** | Salmoneus, the king who faked Zeus's thunder and was struck down |
  | **Elektear** | The Heliades, who wept amber when Zeus struck their brother Phaethon from the sun-chariot |
  | **Kerastorm** | Amalthea, whose hide became the aegis |
  | **Krystolos** | The everlasting ice: what never changes |
  | **Sepivolt** | A thunderbolt fossil from the first Archon's age |
  | **Aetarch** (ace) | The eagle of Zeus (dex #122, "the Archon's ace") |

  - Levels about 66–70, with Apotheosis on Spartan if Balance wants it.
- **Look.** A white beard and a plain, undyed cloak; Aristides was famously poor. An olive wreath, a staff, and a small bronze box under his arm.
- **Voice.**
  - "If it is written, meet it with dignity."
  - "You don't harm the house that feeds you. That's older than Archons."
  - "I spared one free child, and the world stopped. What happens when everyone is free?"

## The Fates: Nemira, Lotira and Thanira

- **Role.** The three Moirai, chained at the Loom for a thousand years.
  - **Nemira** is the Spinner, Klotho: birth.
  - **Lotira** is the Measurer, Lachesis: life.
  - **Thanira** is the Cutter, Atropos: death.
- **Wants.** To be free. Then, to their own surprise, not to know.
- **Fears.** Thanira fears her own shears. She has loved every life she cut, and known each ending before it began.
- **Secret.**
  - **They let you go.**
    - Nemira unspun you.
    - Lotira found nothing to measure.
    - Thanira held her shears open on your thread and couldn't close them. That is the boot intro's hesitation, exactly [BUILT].
  - They have watched you since. The olives came in silver on your Klotheia: "That was us. Looking."
  - And they know what the chained Loom knows: every thread ends on the same row.
- **Arc.**
  1. [BUILT] The intro.
  2. [BUILT] The slice's silver olives.
  3. [LABYRINTH] Phaedon's "Three old women, in chains."
  4. [NEW] The Loom: they taste Melitta's honey, tell you the truth and ask. "We let you go once, little one. Will you let us go?"
  5. [NEW] The Frozen Hour.
     - They flee as three sparks to three sanctuaries: Thanira to Kaldera's forge, Lotira to the Pool of Mnemosyne, Nemira to the old olive in Elaia.
     - Each is gray and faint. Each takes your hand, the only warm thing left in the world.
     - Each rouses and opens four hours of the Stair.
  6. [NEW] On the Stair, with the Lord of Time beaten and the world still stopped, they tell you what's missing. "It needs a moment. We never saw one coming in our lives." The Moment comes, and you take it.
  7. [NEW] At the resolution they come down out of the brightening sky, hands free. "Everything after this, nobody wove." They keep the broken Harpe, one piece each.
  8. [SYSTEMS, dex] Afterward each waits at her sanctuary to be caught at level 50.
     - LOTIRA: "We can measure from anywhere. We'd like to see more than one cave."
- **Team.** They are Pokémon (dex #143–145). In scenes their name boxes read SPINNER, MEASURER and CUTTER (decision S10). The species names appear in battle.
- **Look.** As drawn for the dex: floating black-figure maidens bound by thread. Nemira holds a distaff, Lotira a measuring rod, Thanira shears, in a solid black chiton.
- **Voice.** They finish each other's thoughts.
  - "We let you go once, little one. Will you let us go?"
  - "We've never not known before." / "…It's horrible. I think I like it."
  - "It's what a thread looks like when nobody's decided it yet."

## The Lord of Time (Kronolith, dex #146)

- **Who it is.** A Pokémon, not a person, and it never speaks. It is endless, devouring time: Kronos, who ate his children so that nothing after him could happen. Patient, enormous and certain to win.
  - All three concepts in review give it the Harpe and a stopped hourglass: a Titan, a devourer, or an ouroboros coiled into a clock dial. The story needs only those two things, plus a large overworld object.
- **Where it sleeps.** Under the Omphalos, the stone it once swallowed. Phaedon calls it "Lord of Time" and believes he commands it. He doesn't. It simply wants what he wants: nothing ending.
- **The Loom.** It rises with the Harpe and lays the blade across the warp, and the Frozen Hour spreads from it.
- **The Stair.** After the multi battle it waits at the top, static at level 60, one only, as the dex has it.
  - Caught or beaten, it lets go of the Harpe. **But stopped time doesn't start again by itself.**
  - If it faints, it sinks back into the deep and can be battled again after the credits.

## The Moment (Kairazor, dex #147)

- **Who it is.** Kairos: the fleeting right moment. Lysippos's statue showed him on tiptoe on a razor's edge, long hair in front and bald behind. Seize him as he comes, or he's gone. He is the Lord of Time's counterpart, the chosen instant against endless hours.
- **Its role in the climax** [NEW]. The time pair gives the climax its shape: the villain's frozen eternity against the hero's seized moment.
  1. When the Lord of Time falls, the world still won't move. Endless time has been beaten, but nobody has chosen the next moment.
  2. The Fates can't: they never could see it coming.
  3. Then the Moment comes. It runs along the edge of the Harpe as the blade falls down the Stair.
  4. The Unwoven, the one person nobody ever saw coming either, grabs it by the forelock. That is when time starts again.
  5. It slips free at once ("there's nothing behind to hold") and flies off into the first dawn, toward Olympia.
- **It is not catchable in the story.** As the dex has it, the Moment waits at the altar of Kairos at Olympia's stadium after the League, as a post-game legendary. That keeps dex D3 and gives it a reason to be there. "You seized it once. Try twice."
- **Seeds.**
  - Astyra's Agora has a statue of Kairos, and the Titans have scratched a sickle across its face (II-6).
  - The Kronists: "No more moments. Only the hour."
  - The bull-leap at Knossa teaches the timing [LABYRINTH].
- **Mechanic.** The bull-leap's timing special, reused (`Ichor_BullLeap`, LABYRINTH §3):
  - a painted line on the stair;
  - press A as the Moment's forelock crosses it;
  - fail forward: it wheels and comes again, and the window widens each time.

## Medon, the first Archon

- A memory, seen in the Pool of Mnemosyne in the Frozen Hour, and a shade in the post-game Underworld.
- His father, King Kodros, heard an oracle that a king's death would save the city. Kodros put on a peasant's cloak and walked into the enemy's spears.
- Medon, grieving, could not bear that the oracle might have been wrong and his father dead for nothing. So he chained the Fates so that no oracle would ever be wrong again. He cried the whole time.
- The institution's original sin is grief that made itself a law.
- [POSTGAME] In the Underworld, Kodros's shade tells him: "It wasn't the oracle. I chose."

## Casting the legendaries and the myth Pokémon

Roles come first and dex names second, because names and designs may change in review.
- Before the League only Aethos species appear (D5 (a)).
- Every vanilla pick the bible made stays obtainable in the post-game national dex. It just isn't the story's.

| Story role | Cast from the dex | Replaces the bible's pick (PITCH §4) | Story use |
|---|---|---|---|
| **The Lord of Time** | Kronolith #146 (Ground/Psychic) | Dialga | Wakes at the Loom; the Frozen Hour; the Stair's last battle, static Lv 60 |
| **The three Fates** | Nemira (Spinner), Lotira (Measurer), Thanira (Cutter), #143–145 | Uxie, Mesprit, Azelf | Chained at the Loom; roused in the Frozen Hour; caught after (Lv 50) |
| **The Moment** | Kairazor #147 (Flying/Psychic) | — (new, dex D3) | Seized on the Stair to restart time; post-game legendary at Olympia |
| **The brothers' colossi** | Olympanax, Pontanax, Nekranax, #149–151 (dex D4) | Zapdos as Zeus's bird is now Aetarch, the Archon's ace; the colossi are new | Post-game. The Lord of Time gives back the three bronze lots at the Omphalos, and Kronos returns what he swallowed. Each lot unseals one colossus: on Olympus, in Atlantis, below. |
| **The title mythical** | Ichorin #152 | — | Post-game, at the Pool of Mnemosyne |
| **Zeus's thunder-horse** | Pegaunos #148 | — | Post-game, on Olympus |
| **Asterion, the Minotaur** | Asterlorn #98 | Paldean Tauros | Knossa [LABYRINTH], recorded by the dex team |
| **The healer serpent** | Panacoil #76 | — | Phaedon's partner; the Asclepeion nurse (the Chansey role) |
| **The Delphic bee** | Melisseer #48 | — | Mom's bee, which hums tomorrow |
| **Laelaps and the Teumessian fox** | Skylaps #68, Kerdovix #69 | Hisuian Growlithe, Nickit (slice placeholders) | Alethea's ace against Iapetos's |
| **The Cyclops, Sirens, Scylla, Charybdis, Proteus, Argos** | Polyphant, Seirenade, Hexylla, Trybdis, Haligeron, Nostail | Dusclops, Altaria, Grapploct and others | [POSTGAME] the Odyssey |
| **The Hydra, Ladon, the Stymphalian birds, the Nemean lion, the boar** | Lernathan, Melodrakon, Belornis, Nemeleon, Kaprodon | Hydreigon, Hydrapple, Corviknight, Pyroar, Mamoswine | [POSTGAME] the Labors (dex D6) |
| **Cerberus** | The Fire starter's final stage, Pylakyon (dex D6) | Mega Houndoom | [POSTGAME] the twelfth Labor |
| **The old starters** | Snivy, Cyndaquil, Piplup and 15 more, as guest-gifts | — | [SYSTEMS §10] theoxenia, unchanged |

## The Twelve: the Hierophants and the Pantheon

| # | Hierophant | One line | Story role |
|---|---|---|---|
| 1 | **Ione**, the Hearthkeeper (Normal), Akti | "A hearth isn't the fire, you know. It's what you come back to." [BUILT] | Halia's friend. At the end she takes Phaedon in as a suppliant at Hestia's hearth: "Send him to me. I feed everyone either way." |
| 2 | **Kerykos**, the Herald (Flying), Emporion | "Hermes remembers everyone who passes. Anoint his herms, and when you're lost, he'll point." | Teaches rites and herms [SYSTEMS]. He is the voice of the Archon's proclamations, the doomsday decree and the rebinding decree. That line pays off in the Frozen Hour, when the herms turn their heads. |
| 3 | **Chloe**, the Mystagogue (Grass), Eleusa | "What's reaped grows again. That's the whole secret. Don't tell anyone." | The Mysteries' keeper. Robbed of the first fragment, she hands over the other sickle [SYSTEMS]. Her secret of the Mysteries is the game's ending in one sentence. |
| 4 | **Thespis**, the Masked Player (Poison), Thyrsa | "A tragedy with no satyr play after it is just a funeral." | Iapetos steals his masks for *The Unwoven*. He helps you break the trance with the play the tragedy left out. |
| 5 | **Kallisto**, the Moonlit Huntress (Dark), Arkadia | "I fought the new moon, as I was told. I didn't see his face." | Her prophecy was revised to make her merciless on the night Kleon came: "KALLISTO OF ARKADIA. Revised." [LABYRINTH archive]. [POSTGAME] She apologizes to Kleon during the Golden Hind. |
| 6 | **Talos**, the Bronzesmith (Steel), Kaldera | "It cuts what's woven. Anyone woven who holds it comes apart. You're not woven." | He was Perdix [LABYRINTH] and gives you the Wings. He tells you the Harpe's secret, loses the third fragment to Hyperion, and takes Hyperion into his forge at the end. |
| 7 | **Galatea**, the Living Marble (Fairy), Kythera | "I was perfect once. Marble. Then someone loved me, and I cracked." | Kythera's theme voice. Of love: "Love that won't let a thing change isn't love. It's a pool." Phaedon, in hindsight. She drops the Knossa hint [LABYRINTH]. |
| 8 | **Phemonoe**, the Pythia (Fire), Delphoi | "…I can't see you." [SYSTEMS] | Melitta's elder sister among the melissai, and the Pythia of the blind hour. She guessed the truth and has said nothing for thirteen years. She has answered in single words for a year, because there's less future to see every day. After your laurel, her first sentence in months is "Melitta." After the climax she laughs, and offers "Know thyself" [SYSTEMS]. |
| P | **Brasidas**, the Polemarch (Fighting) | "Lakonians never asked how long. Only how well. Show me well." | Kleon's hero. Courage without a known end. |
| P | **Themistokles**, the Admiral (Water) | "I had him exiled once. Best thing I ever did for him. Nobody's too good to be wrong." | The Archon's old rival. The historical Themistokles engineered Aristides' ostracism. Change, and rivals who need each other. |
| P | **Hypatia**, the Philosopher (Psychic) | "No one wrote you. So who are you? Answer in battle. It's quicker." | The theme's question asked aloud, just before the Archon. |
| P | **Olympias**, the Serpent Queen (Dragon) | "I told my son a god was his father. He believed me, and he conquered the world. Was I lying?" | Hera's seat. A mother who wrote her son a fate, as foil to Rhea and Melitta. |
| C | **Aristeides**, the Archon | See above. | The League's thematic climax. |

## Daedalus, Ariadne and Asterion

Approved in `design/LABYRINTH.md` §8; this file only links them to the spine.

- **Daedalus** is a father who outlived his son.
  - He built Kronos his collar and his hour, because a grieving father told him no father would ever bury a child again. Then he repented and gave you the Labrys.
  - [NEW] He also built Elpis's music box, which is why its tune is the workshop's tune and the Frozen Hour's.
- **Ariadne** is Asterion's half-sister and the Mistress's priestess.
  - She let the Titans in because their master swore he could mend anything. She gives you the thread so someone will witness what they're doing. It is the game's theme, held in your hand.
  - [POSTGAME] She is the Brain of the Endless Labyrinth.
- **Asterion** is the Minotaur, the Pokémon Asterlorn (dex #98). He never speaks.
  - Starry to Kronos, and the real bull Elpis wants to meet.
  - He is first a terror, then a tool, then an ally: nobody is fated to be what they're made into.
  - [NEW] Elpis asks you at the resolution: "Is he still sad?"
  - [POSTGAME] Phaedon can't travel, so the player can bring Elpis to Knossa.

## The supporting cast that carries story

| Who | What they carry |
|---|---|
| **Halia**, Kalliste's priestess | She read the hero's thread and saw nothing.<br>[PHASE2] Her second look: "Forty years, and I've never once seen nothing."<br>[NEW] Her gull carries Kydippe's letter in Act II. Frozen under her canopy in the Frozen Hour, spindle in hand. At the epilogue she reads threads anyway and can't see one: "It seems everyone's thread is their own business now." |
| **Kydippe**, the midwife | Delivered the hero under the old olive. "You didn't cry. You just looked around, like you'd lost something." [BUILT]<br>[NEW] Her letter at Kaldera: "The helmets came at dawn. Your mother was gone by midnight. She knew. I don't know how." |
| **Gylippos**, the Lakonian elder | "Fewer words." [BUILT]. He chaperones the Lakonian delegation and knows whose son Kleon is. At the epilogue he brings Rhea to the festival. |
| **Lysimachos**, the Archon's father | Collects ostraka [SYSTEMS]. At the end, his son comes home no longer "the Just". |
| **Petros and Amathos**, the slice's grunts | The first Titanborn you meet. In the epilogue they work Hyperion's bellows at Kaldera. "He roasts us. Not literally. Mostly." |
| **Kydon**, the Knossan honey-seller | [LABYRINTH seed 3] Thyme honey, and the bull that bellows under the palace. |

---

# 3. The beat sheet

Each beat gives the place, what happens and who's there, the reveal or turn, its foreshadowing link (→ means "pays off in", ← means "paid off from") and its status. Level targets are for Balance.

## Prologue: the slice, Kalliste [BUILT]

| # | Where | What happens | Reveal or turn | Link | Status |
|---|---|---|---|---|---|
| P1 | Boot intro | The Spinner spins white thread. A golden thread rises unspun from the third olive's roots in Elaia's grove. The Measurer finds nothing to measure, and the Cutter's shears open on it and tremble. | — | → the Spinner at the old olive (Frozen Hour); → Medon's Knot unties to gold | BUILT |
| P2 | Daphne's grove | "Every myth is a memory of a Pokémon." "Which came first?" | — | → epilogue: "WE'LL SEE" | BUILT |
| P3 | Player's house | Mom, the Talaria, the pilgrim story ("Or the night before. Or the week after."). The cloak: "someday". The jar: NOT FOR {PLAYER}. | Mom is lying. | → Delphoi spring | BUILT |
| P4 | The square | Halia's spindle stops. "It seems your thread is your own business." | — | → Eleusa; → epilogue | BUILT |
| P4a | The square | **Proposed seed.** A traveling scribe writes down every reading: "May I tell you something true? You're going to be in my book." His tablet's lines end in little hooks. | — | → the Emporion notice, the play program, the Akropolis order, the trial | NEW (§8.2) |
| P5 | Akademia | The starters. Kleon grabs the one that beats yours. "The last krater stays with me. Someone always comes late." | — | → epilogue (Elpis) | BUILT |
| P6 | The square | Kleon's battle. "Die young. And glorious." | — | → Lakonia | BUILT |
| P7 | Kronion Hill | Titanborn Petros and Amathos dig the shrine. The tablet's list has "Kalliste" scratched out and "where the grain goes underground". **Proposed LABYRINTH seed L8:** "Last, the house of the double axe." | — | → Eleusa (the list is Daphne's book; the back of the tablet) | BUILT + L8 |
| P8 | Kydippe's house | "You didn't cry. You just looked around, like you'd lost something." | — | → Delphoi (the lost hour) | BUILT |
| P9 | Akti | Ione and the Hearth Laurel. "She didn't say how it would go. That isn't like her." The Pythia answers in one word, "soon". The tide has been running backward. | The cloth is running out. | → the Loom ("we've known for a year") | BUILT |
| P10 | The quay | Halcyon days, early this year. Kleon's race. The ribbon hangs still. | — | → Phase 2 | BUILT |

## Act I: The Unwoven (Laurels 1–3)

**What `design/phase2/SCRIPT.md` must accomplish.** That team writes these beats. This file fixes only their story content.

1. **Halia's second look.** Before you sail, Halia reads you again by lamplight.
   - She still sees nothing, and must not say "no thread". Her line target is "Forty years, and I've never once seen nothing."
   - She sends a gull to Daphne. It is off-screen, and pays off at Eleusa.
2. **Mom at the harbor.** She sees you off and doesn't cross the water. "Wherever you end up, come back up the hill."
3. **The crossing.** Kleon is your shipmate; he won his laurel overnight.
   - Seed: "My mother writes every week. Two lines. Lakonian."
   - At night the tide runs the wrong way, and a Titan trireme passes with no lights.
   - A sailor: "The Pythia only says *soon* now."
4. **Emporion.**
   - **Titans, public face 1.** Dock crews are hired by "a big man who pays in silver and shouts". That's Hyperion, off-screen.
   - **The hook, first sighting.** A public notice in the Agora carries the Archon's owl seal. Alethea: "Odd. There's a little hook under the owl." No explanation.
   - Kerykos teaches herms: "when you're lost, he'll point."
   - The Trowel, and the Labyrinth seeds (Kydon, Number Nine, page I).
5. **Eleusa.**
   - The Titans rob the Mystery sanctum. Hyperion leads, and this is your first admin battle. Seed: he squints and complains about the dark.
   - Kleon fights beside you in one double battle against Titanborn. It is the bookend to the Stair of Hours.
   - The first fragment is gone. Chloe: "They came for a sickle. They didn't know there were two."
6. **Daphne's revelation** (§7.1 is the master text). It must deliver:
   - Daphne's first crossing in thirteen years;
   - **what** you are (not on the Loom), but **not why** ("your mother's to tell");
   - her confession about the book;
   - the tablet's back, "Bring word of the Unwoven", the Titans' word for you;
   - Alethea's held secret;
   - the Star Chart.
7. **Phase 2 must not:**
   - say why the hero has no thread;
   - reveal Phaedon, or name Iapetos;
   - hint that Kleon's mother is a Titan;
   - give away the third krater. It waits for the epilogue: decision S9.

| # | Where | What happens | Reveal or turn | Link | Status |
|---|---|---|---|---|---|
| I-1 | Elaia | Halia's second look; her gull to Daphne | Halia is frightened. | ← P4, → I-7 | PHASE2 |
| I-2 | Akti quay | The winds turn. Mom sees you off. The *Euploia* sails with Kleon aboard. | — | ← P10 | PHASE2 |
| I-3 | The crossing | Kleon's mother's letters. The wrong tide. A dark Titan ship. | — | → Lakonia; ← P9 | PHASE2 |
| I-4 | Emporion | Herald Laurel (Kerykos), the rites tutorial, herms, the Trowel, the Cold Forge, the hook under the seal, Hyperion's hiring | The Titans pay. Someone in the Archon's own office signs with a hook. | → Thyrsa, the Akropolis, the trial | PHASE2 |
| I-5 | Hecate's Hollow | Hecate's Torch | — | [SYSTEMS] | PHASE2 |
| I-6 | Eleusa sanctum | Harvest Laurel (Chloe). The Titans' theft. Hyperion, about Lv 22. Kleon partners for a double battle. Demeter's Sickle. | First fragment lost. Hyperion can't see in the dark. | → Kaldera, the Stair | PHASE2 |
| I-7 | Eleusa Telesterion | **The Unwoven reveal** (§7.1). Daphne, Alethea, the tablet's back. The Star Chart. | You're not on the Loom. The Titans know about you. Daphne's book is their map. | → Delphoi (why), the Dionysia (the play) | PHASE2, master text here |

## Act II: Hubris (Laurels 4–6)

**The act's spine.** Every beat makes the Titans more seductive and the truth less believed, until the hero learns they are the Titans' key and loses everyone who kept them steady.
- **Midpoint:** "They want you" (II-11).
- **Low point:** Mom is gone (II-14).

| # | Where | What happens | Reveal or turn | Link | Status |
|---|---|---|---|---|---|
| II-1 | Road to Thyrsa | Demeter's Sickle clears the vines. **The Kronia grounds:** a Titan feast camp outside the city. Free bread; masters serve slaves at long tables; masked Kronists give free "true readings" and everyone hears a better fate. "May your thread never be cut." | Titans, public face 2: a movement, not a gang | → §5 | NEW |
| II-2 | Thyrsa | Mask Laurel (Thespis) and the Girdle of Herakles (Silenos) [SYSTEMS] | — | — | NEW + SYSTEMS |
| II-3 | Thyrsa amphitheater | **The Dionysia: *The Unwoven*** (set piece, §6.3). Iapetos stages a tragedy with Thespis's stolen Prosomime masks, and the whole theater falls into a trance. An actor in a petasos carries a sickle to a loom. A "bee-woman" steals a thread from three old women and the gods curse her child. You break the trance with the satyr play the tragedy left out, the Mask trial's verb, used for real. The program is signed with a little hook. Kleon is in the audience. | The Titans know who you are, and where you came from. Your origin has an author, and it isn't the truth. | ← I-4 hook; → Delphoi (the real story); → II-11 | NEW |
| II-4 | Arkadia | The Pool of Mnemosyne, as lore only. Kallisto beats Kleon six to nothing under the new moon. **Kleon joins the Titans** (§7.2). Then your Moon Laurel. Kallisto, after: "I fought the new moon, as I was told." | Kleon chooses the better story. Alethea isn't believed. | → Knossa archive (Kallisto "Revised."); → Lakonia | NEW |
| II-5 | Eleusa, optional | Demeter's theoxenia (Snivy) | — | [SYSTEMS] | SYSTEMS |
| II-6 | Astyra Agora | A Kronist preacher on a cart: "Ask any seer. Every thread ends on the same day. They won't tell you why. We will." Townsfolk confirm it. The herald reads the Archon's proclamation: "If it is written, meet it with dignity." A statue of King Kodros: "He walked into the spears for his city. The Oracle asked it." A statue of Kairos, a runner on a razor, long hair in front and bald behind. Its plinth reads "Seize him as he comes." Someone has scratched a sickle across his face, and a Kronist says, "No more moments. Only the hour." | The world has a countdown, and the Titans own it. The Archon is a fatalist. The Titans hate the Moment. | → the Loom ("the end of the cloth"); → Pool of Mnemosyne (Medon); → the Stair (the Moment) | NEW |
| II-7 | Astyra Asclepeion | Phaedon heals your team. "Easy now. There. Every hurt closes, if you let it." At his hearth: "I've stopped asking." | — | → Knossa unmasking; → epilogue (Akti) | NEW + LABYRINTH seed 9 |
| II-8 | Phaedon's house | Elpis, Starry, the lullaby that stops before the end. "I'll go when the hours stop. Papa says hours don't stop." A music box on her shelf, "From Papa's friend under the island". Daphne visits: "Still being wrong?" / "Constantly. You?" / "Never, lately." | — | → Knossa (Starry; Daedalus's box); → Frozen Hour; → resolution | NEW + LABYRINTH seed 8 |
| II-9 | Astyra Library | Daphne unwriting her book. Page V, the Perdix plaque [LABYRINTH]. Amphora #7, Pandora's jar [SYSTEMS]. | — | — | NEW + LABYRINTH |
| II-10 | The Archon's Stoa | **The Ostracism** (set piece, §6.5). Alethea brings her hooked evidence. Keeper Lykophron answers ("May I tell the Assembly something true?") with forged proof that she faked it, and calls an ostracism. The urn is counted, and Alethea is exiled. She sees the little hook on her own exile decree. The Archon: "The people have voted. It is written." Then, to the player: "You're from Kalliste." "…Hm." | Truth loses. The forger is inside the Archon's house. The Archon is compromised (misread as villainy). | ← I-4, II-3; → Akropolis gate; → trial; → Olympus | NEW |
| II-11 | Outside the walls, night, then the Akropolis | Alethea's confession of her reading. **The Akropolis raid** (§7.3): the guard stands down on a forged order; double battles up the Sacred Way with Alethea; Kleon as a Titan agent; Rhea uproots Athena's olive and takes the second fragment. Kleon: "They want you." Phaedon at the Asclepeion afterward, mending everyone. | **Midpoint.** The Titans need the hero to carry the sickle. Every step after them helps them. Iapetos is the Keeper. | → Kaldera; → Knossa; ← Arkadia; the olive → resolution (new shoot) | NEW |
| II-12 | The salt well | Poseidon's Conch [SYSTEMS]. Alethea leaves: "Everywhere's outside the walls if you walk far enough." | — | → Kythera (she rejoins) | SYSTEMS + NEW |
| II-13 | Kaldera | Forge Laurel (Talos). In the Telchines' sea-cave forge, Talos tells you the Harpe's secret: "Anyone woven who holds it comes apart. You're not woven." **Hyperion's eruption** (§6.7): he takes the third fragment in the caldera's glare. The Wings, and every anointed herm goes live. | The Titans have all three pieces. Only you can hold the whole. | → Knossa; → the Loom | NEW + SYSTEMS |
| II-14 | Kaldera harbor | **The low point.** A gull from Halia carries Kydippe's letter: "The helmets came at dawn. Your mother was gone by midnight. She knew. I don't know how." The beehives are left open; the jar is gone. Daphne: "She's done this before. Find her." | Mom is missing. Kleon is gone, Alethea exiled, all three pieces taken. | → Delphoi | NEW |
| II-15 | Kaldera road, optional | Hephaestus's theoxenia (Cyndaquil) | — | [SYSTEMS] | SYSTEMS |

## Act III: The Loom (Laurels 7–8 and the climax)

| # | Where | What happens | Reveal or turn | Link | Status |
|---|---|---|---|---|---|
| III-1 | Kythera | Foam Laurel (Galatea). Titan ships are requisitioned for Knossa. The bad guests at a host's table [SYSTEMS]. Alethea rejoins: her exile covers Astyra only. The Spring of Kallirhoe, where Narcissus bends over his own reflection forever. Galatea: "Love that won't let a thing change isn't love. It's a pool." The Horn of Achelous. Hermes's theoxenia on the road teaches the tells: "Look at my feet. No shadow." [SYSTEMS E1] | — | → Frozen Hour (a shadowless figure); Phaedon in hindsight | NEW + SYSTEMS |
| III-2 | Off Astyra, optional | Poseidon's theoxenia (Piplup) | — | [SYSTEMS] | SYSTEMS |
| III-3 | Knossa | **The Labyrinth**, as approved, plus three small additions (§8.3):<br>1. In the Ring VI archive, a sealed tablet "ELPIS, DAUGHTER OF PHAEDON. Revised." (you take it).<br>2. At the unmasking, the "Iapetos said you'd bring a tablet" exchange.<br>3. Rhea looks at Kleon before the lever. | Kronos is Phaedon. Iapetos revised his daughter's fate, and the player knows something Phaedon doesn't. | ← II-7, II-8; → Lakonia; → Frozen Hour | LABYRINTH + NEW |
| III-4 | Astyra, letter | Daphne: "I know. I'm staying with Elpis." | — | → Frozen Hour (Daphne at the bedside) | NEW |
| III-5 | Lakonia | **The helmet comes off** (§6.9). Kleon at home; Rhea returns a deserter and unmasks for her son. His real prophecy: "glorious while young, and his glory will not die." Kleon melts the forgery and gives the real tablet back. Iapetos comes for Rhea with Gigas, battles you (about Lv 55) and slips away: "Every draft has a next draft." **Alethea reads Elpis's tablet:** *"Her thread ends the day the hours stop."* She writes it underneath and signs it. Rhea gives Kleon her Kourodin. Kleon's clean rival battle at the battle-school ring (about Lv 57). Hestia's and Ares's theoxenia are nearby [SYSTEMS E2, E4]. | Rhea is Kleon's mother. Kleos never meant death. Phaedon is about to end his own daughter's thread. | ← P6, II-4; → Delphoi, Frozen Hour | NEW |
| III-6 | Delphoi | The Kastalian falls. Titan musters on the slopes. Phemonoe's trial (beams) and the **Sun Laurel**. Then, her first sentence in months: "Melitta." / "Someone's waiting for you. At the spring." | — | — | NEW |
| III-7 | The Kastalian spring | **Mom's payoff** (§7.5). The truth, the jar, the knucklebones confession. "Come back up. Every time." | Why you have no thread, and who chose it. | ← P3, P8, II-3, II-14 | NEW |
| III-8 | The Omphalos, night | The last muster storms the sanctuary. Partner battle: you and Rhea against two Gigas (about Lv 58). Kleon holds the gate. Hyperion burns the Omphalos's net of wool and the stone cracks open. Phaedon goes down with the case. The Archon arrives at the gate, too late again. Mom and Alethea at the top of the stair. | — | → the Loom | NEW |
| III-9 | The Loom | **The Loom** (§7.6). The Fates in chains; every thread ends on the same row. Phaedon won't read the tablet. The honey. "We let you go once." You cut. The Lord of Time rises with the Harpe, and the world drains to gray. | The end of the cloth is tonight. The Fates have a plan: you. | ← P1, P9; → Frozen Hour | NEW |
| III-10 | The Frozen Hour | **The walk** (§7.7). You climb into a frozen Delphoi. The herms turn their heads. The Cutter at Kaldera; the Measurer at the Pool and the memory of Medon; Astyra (Iapetos at his desk, Elpis's room, Phaedon reads the truth); the Spinner under the old olive at home. Kleon breaks his own thread. | Phaedon made the prophecy true. Medon's grief made the chains. The golden thread is yours. | ← nearly everything | NEW |
| III-11 | The Stair of Hours | **The Stair** (§7.8). The multi battle, you and Kleon against Phaedon and Hyperion. Kleon carries Hyperion down. The Lord of Time. The world still won't move, until the Moment runs down the falling Harpe's edge and you seize it. The twelve chimes, and time restarts at dawn. The Moment flies off toward Olympia. | Endless time is beaten, and a chosen moment starts the world. Prophecy is over. | ← I-6 bookend; ← II-6 (the Kairos statue); ← Knossa (the bull-leap's timing); → post-game Olympia | NEW |
| III-12 | Delphoi, then Astyra | Mom: "You came back up." Rhea surrenders. **Elpis's line** (§7.9). Ophiuchus is placed [SYSTEMS]. | Hope | ← II-8 | NEW |

## The League: the Archon

| # | Where | What happens | Reveal or turn | Link | Status |
|---|---|---|---|---|---|
| L-1 | Astyra | The morning after. Joy and terror. The Pythia laughs in her temple. Merchants hoard grain; Lakonia sharpens spears. Kerykos reads the Archon's decree: at the new moon the Archon will carry Medon's Knot to Delphoi, and "fate will be made safe again". Until then he sits on Olympus, as the law says, to answer any challenger. | The fight now is whether fate comes back. | → Olympus | NEW |
| L-2 | The Stoa | **The trial of Iapetos.** Alethea presents the frozen decree, the archive tablets, Kleon's and Elpis's, and every prophecy fragment you found. With all 8, she reads the pattern aloud and the vote is unanimous. The ostraka come out "LYKOPHRON… LYKOPHRON…". Her exile is lifted. His parting shot: "Ask your Just Archon about Kalliste." | The forger is exiled by the same tool he used. | ← II-10; → Olympus | NEW |
| L-3 | Akti | Phaedon's sentence: a suppliant at Hestia's hearth, at Ione's request. Hyperion's: Talos's forge. Rhea's: her own house. | Mercy as a sentence | → epilogue | NEW |
| L-4 | The Akropolis | A green shoot a cubit long on the stump of Athena's olive | — | ← II-11 | NEW |
| L-5 | Delphoi | "Know thyself" opens [SYSTEMS §11]. The Fates wait at their sanctuaries. Dionysus's theoxenia on the crossing [SYSTEMS E5]. | — | — | SYSTEMS |
| L-6 | The Ascent | Victory Road through the clouds. Ex-Titanborn on the road, lost without their master. "In the golden age, did we still get to eat? Nobody ever answered that." | — | — | NEW |
| L-7 | The Pantheon | Brasidas, Themistokles, Hypatia and Olympias, each asking the theme's question (§2, the Twelve) | — | — | NEW |
| L-8 | Olympus summit | **The Archon** (§7.10). The confession of xenia and the lie; the battle; Medon's Knot untied by two pairs of hands. The golden thread blows away south. | The Archon spared you. Iapetos's leverage. The last chain is gone. | ← II-10, the Pool memory, the theoxenia finale | NEW |
| L-9 | Hall of Heroes, credits | The credits reuse the boot intro's frieze, scrolling the other way: the golden thread runs home across the pot, past Olympus, the temple and the sea, to the olive in Elaia. The Star Chart fills its last empty patch with your shape: **The Unwoven** [SYSTEMS §8 #24]. THE END. | — | ← P1 | NEW |
| L-10 | Elaia | **The epilogue** (§7.11). You wake on the next Klotheia. | — | ← P2, P4, P5 | NEW |

## The post-game spine [POSTGAME]

Another designer is writing these epics. This is what each must accomplish, so they hang on the same spine.

**Continuity everyone uses after the credits:**

| Who | Where |
|---|---|
| The player | Archon of Aethos (decision S7) |
| Alethea | Keeper of Records, in Astyra |
| Phaedon and Elpis | Akti, under Ione's roof |
| Hyperion | Talos's forge at Kaldera |
| Rhea | At home in Lakonia, with Kleon visiting |
| Aristeides | At home in Astyra with Lysimachos |
| Iapetos | Exiled for ten years, place unknown |
| The Fates | At their sanctuaries |
| The Lord of Time (Kronolith) | In the party, or in the deep under the Omphalos |
| Asterion | At Knossa with Ariadne |

**Every post-game epic:**
- no one reads the future;
- augurs read the weather [SYSTEMS §6];
- the Pythia does "Know thyself".

| Epic | What it must accomplish | Hooks this story leaves it |
|---|---|---|
| **LABORS** | Glory earned, not fated: Kleon's kleos, made real. | Kleon proposes them: "Herakles had twelve. Let's see about us." He's your partner for some.<br>Kallisto apologizes to him during the Golden Hind.<br>Asterion helps with the Cretan Bull [LABYRINTH L4].<br>Hyperion and his ex-grunts clean the Augean Stables by feel ("I don't need eyes for this. I need a shovel.").<br>The Nemean Lion (Nemeleon) is the first Labor, and Kleon fights it. |
| **UNDERWORLD** | Death without a schedule: still real, still rightful. It must not turn into a resurrection story. | **Medon's shade, and his father Kodros.** Kodros tells his son the oracle didn't kill him: "It wasn't the oracle. I chose." That closes the institution's original sin.<br>Minos asks for the Helm back [SYSTEMS].<br>Charon takes the Elaia well-coin.<br>Thanira can guide you down.<br>Optional: Phaedon asks you to carry a message to Elpis's mother's shade: "Tell her Elpis finished the song." |
| **ODYSSEY** | The long way home. Achilles's choice resolved: Kleon chose glory, and the hero chooses the homecoming. | **Penelope unweaves her loom at night,** the Unwoven motif one last time. Mom is the Penelope figure.<br>Iapetos is suggested on the Sirens' rocks, writing them better songs. You plug your ears with wax melted from his own tablets.<br>It ends at Elaia: Nostail, the faithful hound, waits there, then Zeus and Hermes knock in the storm [SYSTEMS finale]. |
| **POSTGAME** | The world learning to live with an open future. | **The Moment** (Kairazor) at Olympia's altar of Kairos (dex D3). The player seized it once on the Stair, and it got away. Now it appears in the first minute of each hour, per the dex. "You seized it once. Try twice."<br>**The colossi:** bring the Lord of Time to the Omphalos, it gives back three bronze lots, and Kronos returns what he swallowed (dex D4).<br>**Ichorin** at the Pool of Mnemosyne.<br>**Time Fractures** of Paradox Pokémon, where the old cloth's frayed edge leaks the Golden Age. They open after the League, under D5 (a).<br>The Endless Labyrinth [LABYRINTH]. |

---

# 4. The foreshadowing map

Every mystery is seeded at least twice before it pays off, and each seed reads one way the first time and another in hindsight. Quoted lines marked [BUILT] are in the game now. Lines marked [proposed] are the small slice additions in §8.2.

## The big three

| Twist | Seeds | Reminders | Payoff |
|---|---|---|---|
| **1. Why the hero has no thread: Mom chose it.** | **[BUILT]** Halia's spindle stops: "your thread is your own business".<br>**[BUILT]** Mom's pilgrim story hedges too much: "Or the night before. Or the week after. You know pilgrims."<br>**[BUILT]** Kydippe: "I delivered you… You just looked around, like you'd lost something."<br>**[BUILT]** The beehives; "Honey for sale. Ask Melitta."; the jar labelled NOT FOR {PLAYER}.<br>**[BUILT]** Komatas, fed by bees as a boy.<br>**[BUILT]** The half-woven cloak: "She's said *someday* a lot lately."<br>**[BUILT]** The intro's golden thread, rising from an olive in Elaia. | Daphne: "That part's your mother's to tell" (I-7).<br>The Dionysia's bee-woman who "stole a thread" (II-3): a lying version of the truth.<br>Kydippe's letter: "She knew. I don't know how" (II-14).<br>Melisseer's dex entry: it hums what will happen tomorrow.<br>The Pythia: "I can't see you" (III-6). | **Delphoi** (III-7). The melissa, the one hour, the Spinner, the olive, the jar. The knucklebones confession lets the scene breathe. |
| **2. Phaedon made his daughter's prophecy come true.** | **[NEW]** Elpis: "I'll go when the hours stop. Papa says hours don't stop" (II-8).<br>**[NEW]** The Kronist preacher: "Every thread ends on the same day" (II-6).<br>**[LABYRINTH]** The catechism: "What does the sickle reap? The hours."<br>**[BUILT]** The tablet: "*Kalliste* is scratched out", Daphne's book in Iapetos's hands. | The archive's sealed tablet, "ELPIS, DAUGHTER OF PHAEDON. Revised." (III-3).<br>Phaedon: "Iapetos said you'd bring me a tablet" (III-3, III-9).<br>Alethea reads the scraped wax at Lakonia (III-5). | **The Frozen Hour,** in Elpis's room (III-10). Phaedon reads it while the music box ticks. Then the Stair, and Elpis's line. |
| **3. The Archon spared you, and his one lie let the Titans find you.** | **[SYSTEMS]** Lysimachos's ostrakon: "ARISTEIDES. Sick of hearing him called the Just."<br>**[SYSTEMS]** The xenia law: hosts feed strangers first and ask their names after.<br>**[NEW]** The Archon, at the ostracism: "You're from Kalliste." "…Hm." (II-10)<br>**[NEW]** The Archon's seal on the Titans' standing-down order, which he never denies (II-11). | The Archon arrives too late at Delphoi (III-8).<br>Iapetos at the trial: "Ask your Just Archon about Kalliste" (L-2).<br>**[SYSTEMS]** The theoxenia finale's "Your only honey, on a night like this, for strangers". It is Mom's habit, and in hindsight the reason you're alive. | **Olympus** (L-8). "She didn't ask my name. She sat me down." |

## Every other mystery and twist

| Mystery or twist | Seeded | Reminders | Pays off |
|---|---|---|---|
| The Titans know about you | [proposed] The Klotheia's scribe: "You're going to be in my book."<br>[BUILT] Daphne "went very quiet" over the tablet. | The play *The Unwoven* (II-3).<br>Ariadne: "So you're the one the Titans whisper about" [LABYRINTH]. | The tablet's back, read at Eleusa (I-7). Kleon: "They want you" (II-11). |
| Why they want you | [BUILT] Kronion Hill's "Kalliste" | The play's actor carries a sickle (II-3) | Talos at Kaldera: "You're not woven" (II-13) |
| Iapetos is the Keeper of Records | [PHASE2] The little hook under the owl seal in Emporion (I-4)<br>[proposed] The scribe's hooked tablet | The play's program (II-3).<br>"May I tell you something true?" from the masked man (II-4) and from the Keeper (II-10). The ink-dark right hand in both sprites. | Alethea at the Akropolis gate (II-11) and at the trial (L-2) |
| Kronos is Phaedon | [LABYRINTH] Daedalus: "Healer's hands, that one"<br>[NEW] "Every hurt closes, if you let it" (II-7)<br>[LABYRINTH] Starry; "Papa's going to make him better"<br>[NEW] The music box "From Papa's friend under the island" | Phaedon at the Asclepeion on the raid night, mending Titans (II-11).<br>The Elpis tablet in the archive (III-3). | The unmasking (III-3) |
| Rhea is Kleon's mother | [BUILT] "When I was born, the Oracle told my mother something."<br>[PHASE2] "My mother writes every week. Two lines. Lakonian." | Rhea's laconic speech (Lakonians "speak little" [BUILT]).<br>Her Kourodin, a Lakonian battle-school species.<br>"Leave the boy." / "Who asked you?" / "…No one." (II-11).<br>"Someone else's" (Knossa), and her long look at him. | Lakonia (III-5) |
| Kleon's prophecy was misread | [BUILT] "Die young. And glorious." Agis: "He'll catch it, too. That's what worries me." | Kleon: "Where's the glorious part? When does that start?" (II-4) | Lakonia: "glorious while young, and his glory will not die" |
| Kallisto's fate was revised to break Kleon | [NEW] "I fought the new moon, as I was told. I didn't see his face." (II-4) | The archive: "KALLISTO OF ARKADIA. Revised." [LABYRINTH] | [POSTGAME] Her apology to Kleon |
| The Fates are chained | [BUILT] The intro loom<br>[dex] Nemira's entry: "For ages its hands were chained." | Daphne knows of the Loom (I-7).<br>Phaedon: "Three old women, in chains" [LABYRINTH]. | The Loom (III-9) |
| Medon, the original sin | [NEW] The statue of King Kodros in Astyra: "The Oracle asked it." (II-6) | The Archon "keeps a box" (L-8) | The Pool of Mnemosyne memory (III-10); [POSTGAME] the Underworld |
| Every thread ends on the same day | [BUILT] The Pythia's "soon".<br>[BUILT] Halia: "My eyes are tired today."<br>[BUILT] The tide running backward, the early halcyon days, the wrong birds, the humming hill. | The Kronist preacher, the Archon's fatalism (II-6).<br>"Golden age soon. No more clocks." [LABYRINTH] | The Loom: "Every thread ends tonight. We've known for a year." (III-9) |
| Hyperion is going blind | [PHASE2] "Who builds a temple with no windows?" (I-6) | He fights in the eruption's glare (II-13).<br>The optional prophecy fragment: "You'll end your days in the dark…" | The Stair: "It's not noon. It's not anything." The dawn: "There it is." The epilogue forge: "…and be glad of it." |
| Daphne's book is the Titans' map | [BUILT] She "went very quiet" over the tablet; "I have a guess." | — | Eleusa (I-7). At Knossa, add: "Daphne's book told me where" (§8.3). |
| The golden thread and the olive | [BUILT] The intro; the old olive; Halia reads under it.<br>[BUILT] The silver olives: "silver olives mean something's watching." | The Akropolis olive torn up, and the story that it grew back once (II-11).<br>Daphne reads Elpis the olive story (Frozen Hour). | The Spinner under the old olive: "That was us. Looking." (III-10). The shoot on the stump (L-4). The Knot unties to gold (L-8). |
| The honey jar | [BUILT] NOT FOR {PLAYER} | Ring VI's shrine takes honey [LABYRINTH] | Mom gives it at Delphoi (III-7). The Fates taste it: "Melitta's." (III-9). [SYSTEMS finale] A new jar, same label: "Habit." |
| The traveling cloak | [BUILT] "Mom says you'll need it someday." | The empty house after the low point (II-14) | Frozen Hour: finished on the loom, with a note pinned to it: "Someday. -M." |
| Starry and Asterion | [LABYRINTH] Elpis's clay bull | Kronos: "Easy, Starry." [LABYRINTH] | Elpis: "Is he still sad?" (III-12). [POSTGAME] She meets him. |
| The music box | [LABYRINTH] The workshop box ticks | The same box and tune in Elpis's room (II-8) | The Frozen Hour's tick is Elpis's box, still running (III-10). The lullaby finally resolves (III-12). |
| Alethea's curse | [BUILT] "She said I'm *exhausting*." "Truthfully, but badly." The tic itself. | "He didn't believe me. People don't." (II-4) | Her confession (II-11). The trial's vote (L-2). The epilogue. |
| Kronion Hill's hum | [BUILT] Amaryllis; the altar "warm, like a sleeping animal"; the pit "still feels like something's looking up" | [SYSTEMS] Amphora #1, Kronos swallows the stone | After the climax: "The hill's stopped humming. The sheep are fine." |
| "Someone always comes late" | [BUILT] The third krater | — | Elpis, at the epilogue |
| "Which came first?" | [BUILT] Daphne's first question | — | The epilogue: WE'LL SEE |
| Mom's 212 wins | [BUILT] "Record against Mom: 0 wins, 212 losses." | Melisseer hums tomorrow (dex) | Delphoi: "I cheated. The bee hums the throws. All of them." |
| The herms | [SYSTEMS] Anointed on faith in Act I, they become Fly points in Act II | Kerykos: "when you're lost, he'll point" | Frozen Hour: every anointed herm's head turns toward the next sanctuary |
| The Moment restarts the world | [NEW] The defaced Kairos statue in Astyra: "Seize him as he comes." (II-6)<br>[NEW] The Kronists: "No more moments. Only the hour." | The bull-leap at Knossa, timing the A press on a painted line [LABYRINTH].<br>The Fates at the Loom: the only thread that doesn't end tonight is yours. | The Stair: the Fates, "It needs a moment"; the Moment on the falling Harpe's edge; you take it. Post-game: the altar of Kairos at Olympia. |
| Gods have no threads | [SYSTEMS] Theoxenia: the gods have no shadows. Hermes: "We're about. More than you'd think." | — | Frozen Hour, optional: one shadowless figure moving on a distant rooftop. Hermes, watching. |

## Excavation feeds the story

The 8 prophecy fragments are lead tablets [SYSTEMS §5]. Each shows a visible prophecy with an older one scraped away beneath it, and the hook. Each is a small story of one person Iapetos used.

| # | Whose | The forgery | The original, as Alethea reads it | Where it lands |
|---|---|---|---|---|
| 1 | A quarryman of Emporion | "The quarry closes. You'll starve." | "The quarry closes. You'll find other work." | Petros's father. The first grunts were hired off this lie. |
| 2 | The harbor-master of Emporion | "Close the port to the Archon's ships." | "Keep the port open." | The archive's "Revised." line [LABYRINTH] |
| 3 | A soldier of Thyrsa | "You'll die in the next war." | "You'll come home from the next war." | Grunt archetype 5 (§5) |
| 4 | A bride of Eleusa | "Your husband will leave you." | "Your husband will be late." | A comic one |
| 5 | Kallisto of Arkadia | "Show no mercy at the new moon." | "Show mercy at the new moon." | Kleon's loss |
| 6 | A farmer of Kalliste | "Your olives will fail." | "Your olives will come in silver." | The silver olives [BUILT] |
| 7 | **Hyperion** | "You'll end your days in the dark." | "You'll end your days in the dark, and be glad of it." | His epilogue. With this one found, Alethea reads it to him at Talos's forge. |
| 8 | **A widow of Lakonia** | "Your last child will die young." | "Your last child will be glorious young." | Rhea's. This is not a forgery but her own misreading: the lead is unchanged and only her fear changed the words. Alethea: "Nobody scraped this one. She just read it wrong." |

- The main-path proof is the Knossa archive: Kleon's draft and Elpis's sealed tablet. The fragments are optional.
- With all 8, Alethea gets an extra line at Lakonia [SYSTEMS] and reads the full pattern at the trial (L-2), and the vote becomes unanimous.
- **Amphora #1** (Kronos swallows the stone) gives Alethea her answer to the Kronist preachers: "Your golden age had a menu. He ate his children."

---

# 5. Team Titan

## The doctrine

The **Titanborn** believe:

1. **Prophecy is a chain.** The Archon's priests read your thread and tell you what you'll be. They call it peace; it's a cage.
2. **There was a Golden Age.** Before the cutting, under Kronos, no one aged and no one died, and at the Kronia feast masters served their slaves.
3. **The Fates were made to cut.** This half-truth is the one that recruits: the Archons forced them.
4. **Kronos will return.** The cutting will stop, no thread will be cut again, and the feast will never end.
5. **The sign.** Every thread in Aethos ends on the same day. The priests won't tell you why, and the Titans will: it is Kronos's day, and on that day death ends.

**The pitch is seductive because it mirrors the hero's goal:**
- Free us from the tyranny of prophecy.
- Nobody told what they'll be.
- No more knots.

The catch is buried in the gospel itself. Stopping the cutting means stopping the Loom, and stopping the Loom stops everything. The Titans want freedom from fate through stasis; the hero wants it through change. Neither side says so aloud until the Frozen Hour proves it.

**The rite.** Titanborn greet each other with a blessing that sounds kind:
- "May your thread never be cut."
- The answer is "Nor yours."

The catechism, which the Ring IV checkpoint uses [LABYRINTH]:
- "What does the sickle reap?" "The hours."
- "Who stands at the heart?" "The master."
- "Which way do we turn?" "Backward."

## Hierarchy

| Rank | Who | Look |
|---|---|---|
| **Kronos**, the master | Phaedon, masked | The gold mask and a black cloak |
| **The Three**, the admins, who take Titans' names | **Hyperion**, the Hand: crews, digs and the forge.<br>**Iapetos**, the Voice: readings, recruitment, the archive and the plays.<br>**Rhea**, the Ground: tunnels, logistics, the Labyrinth and the chain. | The admins' looks are in §2 |
| **The empty chairs** | Kronos's council hall in the Labyrinth has twelve chairs, one for each Titan, and nine are empty, "for the worthy". It is lore in the Ring IV barracks: a recruiting promise nobody ever got. | — |
| **The Gigas**, the elite guard | Named for the Giants: Enkelados, Porphyrion, Mimas, Alkyoneus, Klytios [LABYRINTH] | Bigger helmets, bronze-scaled cuirasses |
| **The Titanborn**, the grunts | Named with earth-words: Petros, Amathos [BUILT]; Lithos, Koniortos, Sideros, Chalkos, Pelos [LABYRINTH] | A bronze Corinthian helmet with the sickle on the cheek-pieces, an earth-brown chiton and a sickle clasp. Off duty, the helmet is pushed back. |
| **The Kronists**, public preachers | Unarmed and friendly. They give out free bread and free "true readings" (Iapetos's forgeries) in every Agora from Act II on. | Plain clothes and a sickle pin |
| **Sympathizers** | The crowds at the Kronia | — |

## What Aethos sees, act by act

| When | The public face | The player's experience |
|---|---|---|
| **Act I** | **The diggers.** Cranks with shovels in bronze helmets, a nuisance. In Emporion they hire dockhands for silver. | Comic grunts (Petros and Amathos [BUILT]) and a theft at Eleusa that makes them criminals |
| **Act II** | **A movement.** The Kronia camp outside Thyrsa feeds anyone. Kronists stand in every Agora. The Dionysia's tragedy makes their gospel the most talked-about story in Aethos. When seers start finding that every thread ends on the same day, the Titans are the only ones with an answer. Recruits pour in. | Grunts with real reasons (below). The Archon's fatalism makes the Titans look like the side that's doing something. |
| **Act III** | **An army.** The Labyrinth headquarters, the Knossa garrison, the last muster on Delphoi's slopes. Doubt creeps into the ranks. | Grunts asking questions their admins can't answer |
| **The Frozen Hour** | **Statues.** The faithful were promised they'd live forever in the feast. They froze like everyone else. | Frozen Titanborn mid-step on the Stair of Hours, following their master up |
| **After** | **Broken faith.** The Titanborn wake from the Frozen Hour knowing they were stone, so the promise was a lie. Most give themselves up. | Ex-grunts across Aethos with new lives, rebuilding, apologizing or lost |

## Why ordinary people join

1. **Grief.** Their children have been read as doomed.
2. **Poverty.** The rich go to Delphoi and learn when to sell; the poor get a village seer who says they'll stay poor.
3. **Fear.** The same-day sign.
4. **The feast.** At the Kronia, the master pours the wine.
5. **Weariness.** Old soldiers have known their death for forty years.
6. **Flattery.** A free true reading that says you'll be a hero.
7. **Belonging.** A helmet, a crew and a big man who shouts but pays.

## Grunt archetypes

Each is a trainer type with a motive. Every grunt in the game should be one of these, so no grunt is "evil for evil's sake". The levels follow the act.

| # | Who | Sample line |
|---|---|---|
| 1 | **The dig-crew laborer** (Petros) | "The Oracle said the quarry'd close. It closed. Hyperion handed me a shovel and a wage. You got a better offer?" |
| 2 | **The true believer** (Amathos) | "The earth remembers, child. My grandmother remembered the golden age. Her grandmother told her." |
| 3 | **The grieving parent** | "My thread ends on the same day as my baby's. Either we all die that day, or nobody ever dies again. I know what I'm betting on." |
| 4 | **The resentful poor** | "The rich get readings at Delphoi and plan around them. I got told I'd be poor. I'd like a turn being surprised." |
| 5 | **The soldier who wants out** | "Seer said I'd die in a war. Titans don't go to wars. Titans stop them." |
| 6 | **The servant at the feast** | "At the Kronia my master poured my wine. One day a year. Kronos says every day." |
| 7 | **The old veteran** | "I've known how I die since I was sixteen. Forty years of knowing. I'm tired of knowing." |
| 8 | **The kid** | "My friends joined. The helmets are cool. …Is that not a reason?" |
| 9 | **The flattered** | "They read me my true thread. Free! It said I'd be a hero. So here I am. Being one." |
| 10 | **The doubter** (Act III only) | "In the golden age, do we still get to eat? I've asked three times. Nobody answers." |
| 11 | **The quiet one** (Delphoi only) | "I came for my mother. She's sick. …If it works, is she sick forever?" |

## Bases

| Where | What | Who |
|---|---|---|
| Kronion Hill dig [BUILT] | A hilltop pit | Petros, Amathos |
| Emporion warehouses | The hiring hall, crates of shovels and helmets | Hyperion's crew bosses |
| The Eleusa sanctum raid | A break-in, not a base | Hyperion |
| **The Kronia grounds**, outside Thyrsa | A permanent feast camp: long tables, a bread oven, a stage for Kronists. Optional battles with grunts at the tables, who are happy to battle "for fun, it's a feast!" | Kronists, Titanborn |
| Astyra: the Agora stall and the old spring stair | A preachers' stall in daylight, the tunnel by night | Kronists, then Rhea |
| Kaldera's shore camp | Hyperion's forge-shore camp under the caldera | Hyperion |
| **The Labyrinth** [LABYRINTH] | The headquarters: barracks, the council of empty chairs, the archive, the forge | All |
| Delphoi's slopes | The last muster, tents among the laurels | All |
| **Desecrated altars** [SYSTEMS §3] | About 12 roadside altars scratched with sickles, each guarded. "The gods won't save you from your thread. We will." | Titanborn |

## How it ends

- **Kronos** falls on the Stair, and his sickle breaks into three in the Fates' hands.
- **The faith** dies in the frozen streets. Every Titanborn wakes knowing they stood frozen too.
- **The Three:**
  - Hyperion goes to Talos's forge, and takes his crews with him.
  - Rhea goes home under guard.
  - Iapetos is ostracized by the votes he once used.
- **The helmets.** Talos melts them down into bells for every Asclepeion in Aethos (optional flavor). In the post-game, every Asclepeion heal ends with a bronze bell's chime: "Rung from a Titan's helmet," the healer says, if asked.
- **The Kronia** stays on the calendar [SYSTEMS §7]. After the climax it is a real festival again, one day a year when masters pour the wine. The Time Fractures ride on it.

---

# 6. Set pieces

The fifteen moments people will remember, in story order.

Staging is in the GBA's terms:
- **Objects.** Only 16 object events can be live at once (`OBJECT_EVENTS_COUNT` in `include/constants/global.h`), so crowds are drawn into the metatiles.
- **Palettes.** Tints use the existing `TintPalette_GrayScale` and `TintPalette_SepiaTone` (`src/palette.c`) and the day-and-night tint (`OW_ENABLE_DNS`).
- **Shakes and pans.** Screen shakes are `special ShakeCamera`. Camera pans use the camera object, as Emerald's cutscenes do.
- **Partner battles** use `setmultitrainerbattle` (`asm/macros/event.inc`).

## The four that carry the game

If the team can only polish four, these are they.

1. **The Frozen Hour walk** (§6.12)
2. **Mom at the spring** (§6.10)
3. **The Stair of Hours, with Kleon's choice** (§6.13)
4. **Elpis's line** (§6.14)

The rest exist to make those four land.

---

### 6.1 The stopped spindle [BUILT]

**Why it sticks.** The game's first mystery is told by a sound stopping.

**Staging.** As built:
- The chime plays, slows and cuts off.
- 60 frames of silence.
- The player turns left, right and up, twice.

**Music.** The festival theme drops out under the reading.

### 6.2 The robbed Mysteries, and what you are (Eleusa) [PHASE2]

**Why it sticks.** The Mysteries were the ancient world's great secret about death and return, and in their wrecked hall, by one lamp, you learn your own.

**Staging.**
- The Telesterion is dark (SYSTEMS §2), with one lit zone, a lamp on the steps.
- Overturned brazier metatiles and Titan bootprints.
- Daphne tilts the clay tablet to the lamp. Show a close-up of the tablet as a picture window, the way the expansion shows a Pokémon picture in a box, with the back's scratches rising in raking light.
- The Star Chart's item-get icon.

**Music.** Chloe's Mysteries theme, then near-silence: one sustained aulos note under Daphne.

### 6.3 The Dionysia: *The Unwoven* (Thyrsa)

**Why it sticks.** You sit in the audience and watch yourself on stage, cast as the villain's savior, and the story of your own birth told as a lie. Then you break a whole city's trance with a joke.

**Staging.**
1. The amphitheater map. The audience is drawn into the seating metatiles. A slow purple palette pulse on the audience tiles shows the trance; the expansion's palette animation can cycle one palette.
2. **Five objects on stage:**
   - an actor in a petasos;
   - a "bee-woman" in a veil;
   - three masked Fates in black-figure costume;
   - Iapetos's chorus leader in the tragic mask.
3. The play is told in four short scenes, in the chorus's verse, each line one box:
   - the blind hour;
   - the stolen thread;
   - the cursed child;
   - the child carrying a sickle to the Loom while a gold-masked king weeps.
4. Kleon sits in the front row as a fixed object. His sprite turns to look at you during scene three.
5. **The break.**
   - Thespis, backstage, hands you the satyr mask: "A tragedy with no satyr play after it is just a funeral."
   - You walk onto the stage (camera follows) and run the Mask trial's verb live: three doors, three masks, the right entrance in the right mask.
   - Each correct step plays a laugh SE from one block of seats, and that block's palette pulse stops.
   - The last laugh ripples up the tiers and the trance palette drains.
6. **After.** Alethea holds up the program, a close-up picture window: the playwright's name is blank, signed with a little hook.

**Music.** Iapetos's tragedy is the Titan theme slowed into a Phrygian processional. The satyr play is a fast 9/8 aulos romp. The trance cuts when the first laugh lands.

### 6.4 Kleon's new moon (Arkadia)

**Why it sticks.** The rival breaks, in the dark, and the person who catches him is the wrong one.

**Staging.**
- A night map at the new moon: the DNS night tint, with the moon gone from the sky layer.
- Kleon sits on a stump with five Poké Ball objects (one small sprite) beside him, none twitching.
- Iapetos steps out of the cypress line: an object fades in at the tree line through a blend.
- The wax tablet's item close-up. Kleon walks into the trees and hides.

**Music.** Arkadia's night theme with the drums pulled out. Then a single lyre plays Kleon's rival motif in minor as he leaves.

### 6.5 The Ostracism (Astyra)

**Why it sticks.** Democracy, used as a weapon against the one person telling the truth, and everyone you've met in the city votes.

**Staging.**
1. The Agora in daylight. Citizens are drawn into the metatiles around a great urn; six named NPCs stand as objects.
2. One by one the named NPCs walk to the urn and drop a shard. Each drop is a clay-clink SE.
3. **The count.** A wooden board, as a sign window, ticks up in three updates:
   - "ALETHEA, 1,204"
   - "ALETHEA, 3,977"
   - "ALETHEA, 6,000+. Others: 389."
   - 6,000 was the real quorum.
4. The Keeper reads the decree.
5. **Close-up of the decree.** The Archon's owl seal, and under it a little hook.
6. Alethea doesn't speak for 90 frames. Then: "They believed the better story."

**Music.** A dry frame-drum pulse for the vote. Silence for the decree. Then Alethea's theme, played once, alone, on a lyre.

### 6.6 The Akropolis at night

**Why it sticks.** The midpoint: a double battle climb up the most famous hill in the world, beside a friend who has just been exiled. Your rival waits at the top, telling you the terrible truth. Then a sacred tree comes down in the dark.

**Staging.**
1. **The Propylaia.** The guard captain's object steps aside: the forged order.
2. **The Sacred Way.**
   - Alethea joins as your partner, with `setmultitrainerbattle` against Titanborn pairs.
   - The DNS night tint. Torches as lit-zone metatiles.
   - The Titan chant as text from offscreen.
3. **The Parthenon steps.** Kleon, helmet pushed back.
4. **The Old Temple's court.**
   - Athena's olive is a 2×3-metatile tree.
   - Ground Pokémon objects dig at its roots, and `special ShakeCamera` shakes for 30 frames.
   - The tree's metatiles swap to a falling frame, then to a fallen trunk.
   - A gold glint item-icon is pulled from the split.
5. **Rhea.** Her helmet makes her a faceless sprite. She drops into the split, and it fills with rubble metatiles.

**Music.** The Titan theme in 9/8 zeibekiko for the climb. Kleon's rival theme. Rhea's admin battle theme. After the olive falls, wind SE only.

### 6.7 Kaldera erupts, and the letter

**Why it sticks.** The biggest spectacle of Act II, followed straight away by the smallest, worst news: a letter from home.

**Staging.**
1. The caldera map. WEATHER_VOLCANIC_ASH, with a red tint over the BG palettes.
2. Lava flows are animated metatiles. Shakes every 60 frames.
3. Hyperion fights in the glare: the screen briefly flashes white before his ace comes out (fade to white and back in 8 frames).
4. After he's gone, the ash stops. A gull object flies in from the sea edge and lands. A letter item-icon.
5. Kydippe's letter is a sign window in her voice.
6. The camera holds on the player looking out to sea for 90 frames.

**Music.** Hyperion's battle theme, the admin theme with a forge-hammer percussion layer. Then, for the letter, Elaia's home theme played very slowly on one lyre.

### 6.8 The heart of the Labyrinth: the unmasking [LABYRINTH]

As approved in LABYRINTH.md §6 and §8, Scene J, with three small additions (§8.3).

**Why it sticks.** Three bull-leaps over a frightened animal. A rival you have to stop. And the kind man who healed your Pokémon, taking off a gold mask.

**Music.** As approved. Phaedon's theme is Elpis's lullaby in minor (see the music plan below).

### 6.9 The helmet comes off (Lakonia)

**Why it sticks.** The second unmasking, mirrored. Phaedon unmasked to ask for help; Rhea unmasks to ask her son's forgiveness, in the kitchen of the house he grew up in.

**Staging.**
- A small Lakonian house interior: a hearth, a loom, two dead children's grave-stelai painted on the wall as metatiles.
- Rhea's sprite swaps from helmeted to bare-headed in one frame. The helmet is set on the table as a placed object.
- Kleon's sprite doesn't move for 120 frames.
- The lead tablet of his prophecy: an item close-up, unchanged, no hook.
- He melts the wax forgery in the hearth: the item's icon over the fire, a hiss SE, and it's gone.

**Music.** No track, just the hearth crackle. When Kleon speaks again, a frame drum alone in a slow 7/8, the Lakonian march with everything else taken out.

### 6.10 Mom at the Kastalian spring (Delphoi)

**Why it sticks.** Everything she said in the slice turns over at once. The woman who never left the island is standing at Delphoi in a veil you've never seen, and she tells you she chose you over a promise.

**Staging.**
- Dusk at the spring: the DNS evening tint, the spring's waterfall animating.
- Mom is a new sprite: the melissa's veil, the same palette family as her slice sprite.
- Her Melisseer follows her as a small object with a humming emote.
- The honey jar's item-get: the same jar as the 1F shelf's text, NOT FOR {PLAYER}.
- One beat of pure staging: she reaches out and straightens the player's petasos, a short movement script, before she says goodbye.

**Music.** Elaia's home theme, but in the arrangement it was written for: lyre and a woman's hum. It is the first time we hear the home theme's countermelody. The players will have heard the melody all game and never the harmony.

### 6.11 The Loom

**Why it sticks.** The game's whole cosmology in one picture: three old women chained to the machine that writes every life. You do what the villain wants, because it's right, and you know it.

**Staging.**
1. **The Loom map** is one screen tall and two wide.
   - The two posts and the beam are metatiles.
   - The warp threads are animated BG metatiles, swaying.
   - The red knots are drawn into the thread metatiles.
   - At the bottom row every thread ends: the "last row" is a visible line where the cloth stops and the dark begins.
2. The three Fates are object events with their dex art's overworld sprites. Their chains are metatiles from wrist to post.
3. The chasm below is black.
4. **The cut.** A three-stroke cutscene:
   - each stroke flashes white for 4 frames;
   - a bell SE;
   - that Fate's chain metatiles swap to broken ends.
5. **The Lord of Time rises** as a large object, like Emerald's legendaries in their cutscenes. The whole screen shakes as it lifts.
6. **The gray spreads.** `TintPalette_GrayScale` is applied palette by palette, outward from the Loom:
   - the BG palettes nearest first, then the rest;
   - one palette every 6 frames;
   - the player's palette is excluded.
7. **The sparks.** Three spark objects shoot up off the top of the screen.

**Music.** **The Fates' theme** is three voices: Nemira a lyre, Lotira an aulos, Thanira a frame drum. At the Loom all three play together for the first time. When the gray spreads, every instrument stops on a single beat. Silence. Then the tick.

### 6.12 The Frozen Hour

**Why it sticks.**
- The whole world you've walked through is stopped mid-breath, and you walk through it alone.
- Your mother is frozen waiting at the top of a stair. Your rival is frozen mid-swing.
- In a bedroom in Astyra, a father sits holding his frozen daughter's hand. He can't remember how her song ends.

**Staging.**
1. **The gray.** Every map is grayscaled, except the player's palette and later Kleon's, Phaedon's and Hyperion's. The day-and-night tint is suspended.
2. **The frozen world.**
   - Every NPC is a frozen object: movement type none, no idle animation, the walk frame mid-step.
   - **Wild encounters are off.**
   - Frozen motion is placed by hand:
     - birds as static objects in flight poses;
     - sparks hanging over Talos's anvil;
     - a wave curled and stopped at Akti, drawn as metatiles;
     - the Kastalian falls drawn as still water, with the animation suspended.
3. **Sound.**
   - The only BGM is **the music box**: Elpis's lullaby, ticked out slowly on a comb, missing its last bar.
   - Footstep SE for the player only.
   - No other SE in the world, until Kleon wakes.
4. **The herms.**
   - Every anointed herm's head metatile swaps to a variant facing the next unvisited sanctuary.
   - Talk to one: "The herm's stone face has turned. It's looking toward Kaldera."
   - Un-anointed herms stay as they are. Your faith in Act I pays off a second time.
5. **Travel.** Daedalus's Wings work; the herms are live.
   - The three sanctuaries can be woken in any order. Astyra is required, and the Measurer points to it.
   - Recommended order, nudged by the herms: Kaldera, Arkadia, Astyra, Elaia. Home last.
6. **Memory.** At the Pool of Mnemosyne, the memory of Medon plays in `TintPalette_SepiaTone`. Gray is the frozen present; sepia is memory. The two never mix.
7. **The music box's source.** In Elpis's room the box sits on her shelf, a small object with a 2-frame tick animation: the only animated object in the frozen world.
8. **A god, optional.** On one Astyra rooftop, a shadowless figure moves at the edge of the screen and is gone. Players who learned Hermes's tells will know.

**Music.** The music box only. When each Fate wakes, her voice from the Fates' theme joins the music box for the rest of that sanctuary.

### 6.13 The Stair of Hours

**Why it sticks.**
- The climax is fought beside the rival you started with, against the healer and his blind lieutenant, on a staircase made of stopped time.
- The rival chooses a deed nobody will ever see over the moment everyone will sing about.
- Then you beat endless time, and the world still doesn't move. It starts again only when you choose a moment, without knowing what it will bring. The time pair is the climax's shape: the villain's frozen eternity against the hero's seized moment.

**Staging.**
1. **The Stair.**
   - A vertical map, twelve landings spiraling up from the Omphalos into a gray sky.
   - Each landing has a sundial metatile with its shadow frozen.
   - Each landing is gated until its Fate is roused, four landings per Fate.
   - Frozen Titanborn climb the lower landings as static objects.
2. **The twelfth landing.**
   - Phaedon and Hyperion.
   - The Lord of Time is a large object above, filling the sky. The Harpe is part of its sprite in every concept under review.
3. **The multi battle,** with `setmultitrainerbattle`: you and Kleon against Phaedon and Hyperion.
4. **The crumble.**
   - Below the twelfth landing, the steps swap to empty sky, row by row, using `setmetatile` and `DrawWholeMapView`, with a shake per row.
   - Kleon's and Hyperion's objects walk down through the crumbling rows: a scripted movement just ahead of the swap.
   - The camera stays at the top and looks down. You watch them get smaller.
5. **The Lord of Time.** A static battle, `setwildbattle` with its own battle music.
6. **The Moment.**
   - After the battle, nothing moves. The music box ticks on.
   - The three Fates' sparks settle on the landing: "It needs a moment."
   - The Harpe slips from the Lord of Time's grip and tips over the edge. A bright small object, the Moment, comes running along its blade.
   - A painted line on the landing's paving. Press A as the forelock crosses it: the bull-leap timing special.
   - **Fail forward.**
     - A miss and the Moment is past, gone off-screen in a streak.
     - It wheels round and comes again, with the window wider each pass, as at Knossa.
   - **Success.**
     - A one-frame white flash and a sound like a breath drawn in.
     - The Moment's object pulls free, leaving a gold feather-glint, and streaks off toward the sky's east edge.
     - The chimes begin.
7. **The twelve chimes.**
   - The Harpe is a small spinning object. It falls past you down the stair, one landing per chime.
   - **Each chime restores one twelfth of the color.** Blend each palette from its grayscale copy toward the original by one twelfth per chime. A small new special does this; the expansion's blend routines are the model.
   - On the twelfth chime the sundial's shadow metatile shifts one step. The DNS tint resumes at dawn.
8. **Sound returns,** one layer at a time:
   - wind;
   - birds;
   - the sea far below;
   - the main Ichor theme.

**Music.**
- **Kronos's theme** for the multi battle: Elpis's lullaby slowed and made enormous, in Phrygian, for full ensemble.
- **The Lord of Time's battle theme** switches meter every phrase, from 7/8 to 9/8 to 5/8 and back, as if time can't settle.
- **The Moment** has no theme. The music box's tick simply stops on the frame you seize it: the first silence in the Frozen Hour.
- The twelve chimes are tuned to the lullaby's first twelve notes.
- Then the main Ichor theme, Lydian, rising, as at the Icarus Shaft [LABYRINTH].

### 6.14 "Then my thread isn't finished yet" (Astyra)

**Why it sticks.** The smallest scene in the climax and the one it's all for. A seven-year-old says one sentence and the whole game's argument is complete.

**Staging.**
- Elpis's room by morning light, the DNS morning tint.
- The city's noise comes in through the window as SE: a dog, a herald, people talking at once.
- Elpis sits up in bed.
- Phaedon's object kneels: a custom kneeling frame, or the face-down frame.
- Hold 120 frames on her line, with no music.
- Then Ophiuchus is placed: the Star Chart's chime and a one-line system message.

**Music.** Elpis hums the lullaby and, for the first time in the game, **finishes it.** The melody resolves to its tonic. Every other version of it in the game, the hum, Phaedon's theme, the music box and Kronos's theme, stops on the half cadence. This is the composer's most important brief (see below).

### 6.15 Medon's Knot (Olympus), and the credits

**Why it sticks.**
- The League's last battle is about the theme, not the title.
- The Archon tells you the one thing he ever chose freely was letting you live.
- Then two people who disagree untie the world's last chain together, and it turns to gold in their hands.

**Staging.**
1. The summit is above the clouds: a clouds weather layer below the map edge, and an altar.
2. **The box.**
   - It is a small object on the altar.
   - The Knot's item close-up shows a black fist of thread with one red strand.
3. **Untying.**
   - Six "pull" beats. Each is a YES-to-continue box with a rope-creak SE.
   - The Knot's icon swaps through three looser frames, then to a single gold thread.
4. **The thread blows away.** A small gold thread object drifts on a sine path off the screen's south edge.
5. **The credits** reuse the boot intro's frieze (`design/phase1/INTRO.md`), scrolled the other way.
   - The golden thread runs home across the turning pot: past Olympus, the temple and the sea, to the third olive in Elaia, where it sinks into the roots.
   - Then the Star Chart's last patch fills with the player's shape: **The Unwoven** [SYSTEMS §8 #24].

**Music.**
- **The Archon's theme** is Mixolydian, stately, on kithara and drum. It stops when he says "Gods help you."
- Untying the knot has no music: rope and wind.
- **The credits** play the main Ichor theme and, under it in the second half, Elaia's home theme with its countermelody from the spring scene.

---

## The music plan in one table

One melody carries the story's heart, and the score withholds its resolution until the right moment.

| Theme | What it is | Where it plays | The rule |
|---|---|---|---|
| **The lullaby** | Dorian, a simple eight-bar tune Elpis hums | Elpis's hum (Astyra); **Phaedon's theme**, in minor at the unmasking [LABYRINTH]; **the music box** (Elpis's shelf, Daedalus's workshop, the whole Frozen Hour); **Kronos's theme** (the Stair, enormous); the twelve chimes | **It never resolves.** Every version stops on the half cadence (Elpis always falls asleep first) until she finishes it at the resolution. |
| **The Labyrinth motif** | D E F G E F G E A, the crane dance [LABYRINTH] | Knossa | As approved |
| **Elaia, home** | Dorian, lyre (see MUSIC.md) | Elaia, Mom's scenes | The countermelody is withheld until the Kastalian spring. Afterward the town theme always has it. |
| **The Fates** | Three voices: lyre (Nemira), aulos (Lotira), frame drum (Thanira) | The intro's loom (already scored); the Loom; one voice per sanctuary in the Frozen Hour | All three play together only at the Loom, and on the Stair once all three are roused. |
| **Team Titan** | 9/8 zeibekiko, heavy (`mus_ichor_titan` exists) | Grunts, bases | Slowed into a processional for Iapetos's play |
| **The admins** | A shared battle theme, each with its own top layer | Hyperion (forge hammers), Iapetos (a chorus of aulos), Rhea (a slow 7/8 Lakonian frame drum) | Needed (INVENTORY §8) |
| **The Frozen Hour** | The music box, nothing else | The Frozen Hour | No other track may play |
| **The Lord of Time** | Meter changes every phrase | The Stair, the post-game rematch | — |
| **The Moment** | Silence: the tick stops | The instant you seize it on the Stair; at Olympia in the post-game, a fast bright phrase that's over before it starts | Never more than two bars |
| **The Archon** | Mixolydian, kithara and drum | Olympus | Stops on "Gods help you" |
| **The main Ichor theme** | Dorian, turning Lydian at the end (see MUSIC.md) | The title, the Icarus Shaft [LABYRINTH], the end of the Stair, the credits | — |

---

# 7. Draft scenes

These are written in `design/phase1/SCRIPT.md`'s format.
- **Boxes.** Each line is one text box. `NAME:` opens a speaker's turn. `[brackets]` are stage directions. Choices are `?? YES/NO` with `> YES:` branches. `{PLAYER}` is the player's name.
- **Characters.** The Gen 3 charmap has no em dash and no straight double quote, so dialogue uses `…`, `-` and “ ” only.
- **Length.** Lines are short enough for Poryscript's `format()` to wrap into the box.
- **Order.** The scenes are in story order. Where a scene belongs to another document, its header says so.

## 7.1 The Unwoven reveal

- **Where:** Eleusa, the Telesterion, after the theft and the Harvest Laurel.
- **Owner:** `design/phase2/SCRIPT.md` implements it; this is the master text.
- **Needs:** Laurel 3 and the theft. **Gives:** the Star Chart.

[The Telesterion after the theft. Braziers kicked over, bootprints in the ash. One lamp burns on the steps. Daphne sits beside it, a little green, in new sandals. Alethea stands below her.]
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
[She tilts the tablet to the lamp. Faint scratches stand up out of the clay.]
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
DAPHNE: Then take this. When people were sure of a story, they put it in the sky.

{PLAYER} received the Star Chart!

DAPHNE: You're not in the sky yet. Neither am I.

DAPHNE: I've been a tree on that island for thirteen years. Rooted.

DAPHNE: I think it's time I walked somewhere.

DAPHNE: Astyra. The Library. I'm going to try to unwrite a book.

ALETHEA: And I'm coming with you, {PLAYER}. Obviously. I brought two trowels.

ALETHEA: …Three.
```

## 7.2 Kleon joins the Titans

- **Where:** Arkadia, the cypress wood below Kallisto's temple, at the new moon.
- **Needs:** arriving in Arkadia, before the player's own Moon Laurel.
- **Who:** Kleon, Alethea, Iapetos in his Titan mask.

[Night. No moon. Kleon sits on a stump. His Poké Balls are lined up beside him, and none of them twitch.]
```text
KLEON: Don't. Whatever you're going to say. Don't.

KLEON: …She didn't even look at me. Kallisto. The whole match.

KLEON: She looked at the sky. And she won anyway. Six to nothing.

KLEON: Six to nothing.

KLEON: You know what her acolytes said? “Poor thing. He's fated.”

KLEON: Like it already happened. Like I'm a story they've heard.

KLEON: “Die young and glorious.” Well. I'm young.

KLEON: Where's the glorious part? When does that start?

ALETHEA: Kleon, she's beaten everyone this month. She's-

KLEON: She beat everyone. She crushed me. There's a difference.
```
[A twig snaps. A figure steps out of the cypresses in a white theater mask, the sad one. The fingers of his right hand are stained with ink.]
```text
???: Six to nothing. I watched. It was very hard to watch.

KLEON: Who are you?

???: A writer, of a sort. I write down what people are.

IAPETOS: The Titans call me Iapetos. You can call me whatever helps.

ALETHEA: {PLAYER}. That's a Titan.

IAPETOS: And you're Daphne's girl. The one who digs. Hello.

IAPETOS: Kleon. May I tell you something true?

IAPETOS: The thread they read you was a poor one. Badly made.

IAPETOS: “Young and glorious,” and nothing after. No deed. No place.

IAPETOS: That's not a fate. That's a shrug.

IAPETOS: Kallisto's fate is better written. That's why she won.

KLEON: …What's that supposed to mean?

IAPETOS: It means threads can be read again. Better. By someone careful.
```
[He holds out a wax tablet.]
```text
IAPETOS: Here's a better thread.

IAPETOS: “Kleon of Lakonia shall slay the starry bull…

…beneath the house of the double axe, and his glory shall never die.”
```
[Hold 60 frames.]
```text
KLEON: Never die.

IAPETOS: Never.

ALETHEA: That's forged. Kleon, look at the wax. It's soft. He wrote it tonight.

ALETHEA: Threads are read at Delphoi. Not by men in masks in the woods.

KLEON: And what did Delphoi read for me? “Die young.” Thanks, Delphoi.

ALETHEA: I'm telling you the truth.

KLEON: Everybody's telling me the truth! I'd like a better one!
```
[Pause. Kleon turns to the player.]
```text
KLEON: Everyone's got a story about you. Even the Titans. They wrote you a play.

KLEON: I just want one that's mine.
```
[He takes the tablet.]
```text
IAPETOS: There. That wasn't hard. May your thread never be cut.

KLEON: …Nor yours?

IAPETOS: Good. You'll pick it up.
```
[Iapetos steps back into the dark. Kleon gathers his Poké Balls.]
```text
KLEON: Don't follow me. I mean it this time.

KLEON: Next time we fight, it's written that I win.
```
[He goes into the trees after the mask. Hide Kleon.]
```text
ALETHEA: …He didn't believe me.

ALETHEA: People don't. I'm used to it.

ALETHEA: Truthfully, I'm not.
```

## 7.3 The Akropolis

- **Where:** Astyra, the night after the ostracism.
- **Needs:** II-10 done. **Gives:** the midpoint. The second fragment is lost.
- **Who:** Alethea, the guard captain, Titanborn, Kleon, Rhea.

**Prelude: outside the walls, at dusk.** [Alethea sits on her satchel by the road. The city gate is shut behind her.]
```text
ALETHEA: Ten years. That's how long an ostracism lasts.

ALETHEA: I'll be old. Truthfully, very old.

ALETHEA: Can I tell you something? About my Klotheia?

ALETHEA: I said Halia called me exhausting. She did. That wasn't the reading.

ALETHEA: She said, “You'll tell the truth all your life…

…and they'll call you a liar.”

ALETHEA: So I say “truthfully.” Every time. In case it helps.

ALETHEA: It doesn't. But I like to have it on the record.

ALETHEA: …The Titans are going up the Akropolis tonight. I heard the Keeper's men.

ALETHEA: Come on.
```

**The Propylaia.** [Four of the Archon's guards stand aside from the open gate, spears grounded.]
```text
CAPTAIN: Stand aside, kid. Orders. Sealed by the Archon.

CAPTAIN: Nobody goes up or down tonight.

CAPTAIN: Funny thing. Somebody's up there. Hear them?
```
[Far above, stone cracks. A chant, from offscreen: “What does the sickle reap? The hours.”]
```text
ALETHEA: Let me see that seal.
```
[The captain holds out the order. Alethea holds it to her lamp.]
```text
ALETHEA: That's the Archon's owl. Pressed right. Perfect.

ALETHEA: And under it, in the wax… a little hook.

ALETHEA: The same hook as my exile decree. The same as the play.

ALETHEA: {PLAYER}, the Archon didn't seal this. His Keeper of Records did.

CAPTAIN: The Keeper? He's the Archon's right hand.

ALETHEA: He's the Archon's right hand. And the Titans' left.

CAPTAIN: …You're the girl they voted out this morning.

ALETHEA: I'm exiled from the city. The Akropolis is above the city.

ALETHEA: Technically.

CAPTAIN: I didn't see you. Either of you. Go.
```

**The Sacred Way.** [Titanborn hold the ramp in pairs.]
```text
ALETHEA: They're in twos. So are we. {PLAYER}, with me.
```
[Alethea joins as your partner. Two double battles up the ramp: Lithos and Koniortos, then Sideros and Chalkos. Their lines:]
```text
LITHOS: Golden age soon! Then nobody gets voted out of anything.

KONIORTOS: You'll thank us when you never grow old.

SIDEROS: My thread ends the same day as my little brother's. Think about that.

CHALKOS: Shift's nearly over. Can we hurry this up?
```

**The Parthenon steps.** [Kleon stands on the top step. A bronze Titan helmet sits pushed back on his head like a cap.]
```text
KLEON: Took you long enough.

KLEON: Like the helmet? I don't wear it down. Heroes don't hide their faces.

ALETHEA: Kleon, they're tearing up the Akropolis.

KLEON: They're digging. You dig. Everyone digs.

KLEON: I've got a real thread now. It's written. I win.

KLEON: Let's find out.
```
[Battle `TRAINER_ICHOR_KLEON_AKROPOLIS`. His defeat line:]
```text
KLEON: …That's not- it's written. It's WRITTEN.
```
[After the battle:]
```text
KLEON: It says the bull. It doesn't say you. That's all. You're not in it.

KLEON: You're not in anything, are you? That's the whole point of you.

KLEON: They don't want the pieces. Not really. Iapetos told me.

KLEON: They want you. You're the only one who can carry it.

KLEON: Every step you take after them, you're bringing it closer.

KLEON: …I thought you should know. That's all. Don't make it a thing.
```
[A roar from the Old Temple. The ground shakes. Kleon runs into the dark.]

**The Old Temple's court.** [Athena's sacred olive leans over a split in the rock. Titanborn with shovels. Ground Pokémon tear at its roots. A woman in a full bronze helmet holds a lamp: Rhea.]
```text
RHEA: Keep digging.

TITANBORN: The roots, Rhea. It's Athena's tree. They say it grew back once-

RHEA: Not this time. Dig.
```
[A long crack. The olive tips and falls across the court. Something gold is pulled out from under its roots.]
```text
RHEA: There. Second piece.
```
[Rhea turns. The helmet hides everything but her eyes.]
```text
RHEA: You. The Unwoven.

RHEA: Go home.

ALETHEA: We're not going anywhere.

RHEA: Then don't. Fine.
```
[Battle `TRAINER_ICHOR_RHEA_AKROPOLIS`. Her defeat line:]
```text
RHEA: Hm. Good.
```
[After the battle:]
```text
RHEA: Strong. Doesn't matter. The piece goes.
```
[The Titanborn drop into the split: the old spring stair. Kleon reappears at the edge of the court. A grunt shoves him toward the stair.]
```text
TITANBORN: Move it, Lakonian!

RHEA: Leave the boy.

KLEON: Who asked you?

RHEA: …No one.
```
[Rhea goes down last. A rumble, and the split fills with rubble. Silence. Wind. Alethea kneels by the stump.]
```text
ALETHEA: The Persians burned this tree, long ago.

ALETHEA: The next morning there was a green shoot on the stump. A cubit long.

ALETHEA: Everyone in Astyra knows that story.

ALETHEA: …Truthfully? I don't think it'll do it twice.
```
[Fade. Pays off at L-4: a green shoot on the stump, the morning after the Frozen Hour.]

## 7.4 Phaedon's unmasking: the changes to LABYRINTH.md

`design/LABYRINTH.md` §8 Scene J is approved and stands word for word. Cross-checked against this file, it already matches every rule here:
- Phaedon's motive as he believes it;
- his prediction about the Loom;
- "Three old women, in chains";
- "Starry";
- Rhea's "someone else's".

This story adds four small things, marked **NEW**.

**1. Scene H, the archive.** After "{PLAYER} took the wax tablet.":
```text
On the bottom shelf, one tablet is sealed shut with a blob of wax.

“ELPIS, DAUGHTER OF PHAEDON. Revised.”

The seal is pressed with a little hook.

{PLAYER} took the sealed tablet.
```
[Main path: taking it is automatic, so Lakonia and the Frozen Hour can count on it.]

**2. Scene J, after** "PHAEDON: Daedalus understood. He buried a son.":
```text
PHAEDON: Daphne's book told me where the pieces lay. She sent it to me herself.

PHAEDON: She thought she was helping a friend with a sick child. She was.
```

**3. Scene J, after the YES/NO to** "Will you carry it for me?" **and before** "PHAEDON: Rhea. Turn the house.":
?? Show Phaedon the sealed tablet? YES/NO
```text
> YES:
PHAEDON: Iapetos said you'd bring me something. A tablet.

PHAEDON: He said Daphne's girl would forge one. To stop me.

PHAEDON: I'm not going to read it. I'm sorry. I can't afford to.

> NO:
PHAEDON: Whatever's in your bag, keep it. I've made up my mind.
```

**4. Scene J's stage direction** before Rhea's lines becomes:

[Rhea stands at the great lever. She looks at Kleon for a long time. Then at Ariadne, with her brother's head in her lap.]

## 7.5 Mom's payoff

- **Where:** Delphoi. The Pythia's temple, then the Kastalian spring at dusk.
- **Needs:** the Sun Laurel. **Gives:** Melitta's Honey (key item).

[The Pythia's temple, after the battle. Phemonoe sits on her tripod.]
```text
PYTHIA: …

PYTHIA: Melitta.
```
[Hold 60 frames. It is the first time anyone has heard her say more than one word in a year.]
```text
PYTHIA: Someone's waiting for you. At the spring.

PYTHIA: She's been waiting thirteen years.
```
[The Kastalian spring at dusk. Water falls from the cleft in the rock. A woman in a pale-gold veil with a honeycomb hem stands at the pool. A bee hums at her shoulder.]
```text
MOM: There you are. You look thin. Have you been eating?

MOM: …Don't look at me like that. I know. I know.

MOM: Sit. My knees aren't what they were when I lived here.

MOM: I said a pilgrim told me about the blind hour.

MOM: There wasn't any pilgrim.

MOM: I was here. I was a bee, once. A melissa.

MOM: We carried honey down to the Loom. For the three of them.

MOM: Nobody else would. A thousand years in chains, and nobody fed them.

MOM: When I was carrying you, I took the honey down like always.

MOM: The middle one measured your thread. She didn't mean to. It's what her hands do.

MOM: One hour. You'd have had one hour.
```
[Hold 90 frames. Only the spring.]
```text
MOM: I begged. I'm not proud of it. I begged three old women in chains.

MOM: The Spinner said she couldn't change what she'd spun.

MOM: But she could take it back. Unspin it. As if it had never been.

MOM: No thread. No hour. No knot. No promise of anything, ever.

MOM: Nobody would see what you'd be. Not the Pythia. Not even them.

MOM: I said yes before she'd finished asking.

MOM: I ran that same night. As far as a boat would go. To Daphne.

MOM: And one night, under the old olive in the square, you came.

MOM: Kydippe heard me. She came out in her nightdress and knelt in the dirt.

MOM: Far away, the Spinner held her hands still for an hour.

MOM: And the Oracle went blind.

MOM: You didn't cry. You looked around like you'd lost something.

MOM: You had. An hour. I traded it for everything else.

MOM: So that's what you are. You're the thing I chose.

MOM: I'm sorry I lied. I'm not sorry I did it.
```
?? Multichoice: WHY DIDN'T YOU TELL ME? / I KNOW.
```text
> WHY DIDN'T YOU TELL ME?:
MOM: Because you'd have wondered every day if it was worth it.

MOM: I wanted you to just live. Not prove anything.

> I KNOW.:
MOM: …Of course you do. You've got Daphne's nose for things. And my chin.
```
```text
MOM: The helmets came to Elaia. My bee hummed it the day before.

MOM: I'd packed by supper. Where do you hide a runaway bee?

MOM: In the hive. Phemonoe took me in. She always was the brave one.

MOM: Oh. And one more thing, while I'm confessing.

MOM: The knucklebones. I cheated. The bee hums the throws.

MOM: All two hundred and twelve.

MOM: …Well. You had to find out sometime.
```
[She takes the jar from her bag: the one from the shelf at home.]
```text
MOM: Here. You can have it now.

{PLAYER} received Melitta's Honey!

The label still says “NOT FOR {PLAYER}.”

MOM: It was never for you. It was for them. The last of the Delphoi honey.

MOM: You're going down there tonight, aren't you.
```
?? YES/NO
```text
> YES:
MOM: Stubborn. You get that from me.

> NO:
MOM: Liar. Good. You'll need that.
```
```text
MOM: Then take it to them. Tell them Melitta says thank you.

MOM: Tell them it was worth it. Every day.
```
[She reaches out and straightens the player's petasos.]
```text
MOM: And come back up. You hear me? That's all I'll ask.

MOM: Every time. Come back up.
```

## 7.6 The Loom

- **Where:** the cavern under the Omphalos, Delphoi, at night.
- **Needs:** III-8 (the Omphalos opened). **Gives:** the Frozen Hour.
- **Who:** Phaedon, Hyperion, the three Fates, the Lord of Time.

[A long stair down. Far off, a music box ticks. The cavern opens, and the Loom fills the screen: two posts, a beam and threads beyond counting. Every thread is white with a red knot. They all stop on the same row near the floor, and below that row there is only dark.]
```text
The Loom. Every life in Aethos hangs here.

Every thread ends on the same row. There's no cloth below it.
```
[Three figures stand at the Loom, chained at the wrists to the posts and the beam. Their hands never stop moving. Phaedon kneels by a lined case. Hyperion stands at the chasm's edge, squinting into the dark.]
```text
PHAEDON: You came down. Of course you did.

PHAEDON: Your mother's up there. I can tell by your face.
```
?? Show Phaedon the sealed tablet? YES/NO
```text
> YES:
PHAEDON: I told you at Knossa. I won't read it. Not now. Not here.

PHAEDON: If it says what Iapetos warned me it would, I'd stop.

PHAEDON: And then she dies. So no.
```
```text
PHAEDON: Look at them. That's all I'll ask. Look.
```
[The camera pans along the Loom to the three Fates.]
```text
SPINNER: …Someone's come.

MEASURER: Someone with nothing to measure.

CUTTER: Someone I can't cut.

SPINNER: Oh. Oh, it's you.

SPINNER: You've grown. We never get to see them grow. Only the thread.
```
?? Give them Melitta's Honey? YES/NO
```text
> NO:
The honey jar is heavy in your bag.
```
[NO asks again.]
```text
> YES:
You hold up the jar. The Spinner reaches as far as her chain allows.

SPINNER: Thyme. Kalliste thyme.

MEASURER: Melitta's.

CUTTER: She always brought too much. We never said.

SPINNER: She says thank you? Tell her we're the ones who say that.

SPINNER: Tell her it was worth it. Every day.
```
```text
PHAEDON: A thousand years. The first Archon chained them here.

PHAEDON: So no thread would ever change. So every oracle would come true.

PHAEDON: They tie the knots. They can't stop. They can't choose.

PHAEDON: I'm asking you to cut them free. That's all I've ever asked.
```
[He opens the case. The Harpe lies on red cloth, gold and black.]
```text
PHAEDON: It doesn't like anyone with a thread. It'll like you.
```
?? Take the Harpe? YES/NO
```text
> NO:
PHAEDON: I know. I said no too, the first time.
```
[NO asks again.]
```text
> YES:
{PLAYER} lifted the Harpe. It's light. It hums.

MEASURER: Listen to us before you listen to him.

MEASURER: Every thread on this Loom ends tonight. Every one.

MEASURER: We've known for a year. The tides knew. The birds knew.

CUTTER: His. Hers, at the top of the stair. The little girl's, in the city.

SPINNER: We tied it so. We couldn't help it. The chains don't let us help it.

MEASURER: Cut us free, and he'll take what we are. The world will stop.

MEASURER: Leave us, and it stops anyway. Tonight. In chains.

SPINNER: The only thread that doesn't end tonight is yours.

SPINNER: Because it isn't ours. We let it go.

CUTTER: Cut us free. Then, after, come and find us. Wake us.

CUTTER: You'll be the only one who can.

SPINNER: Will it work? We don't know.

MEASURER: We've never not known before.

CUTTER: …It's horrible. I think I like it.

SPINNER: We let you go once, little one. Will you let us go?
```
?? Cut the chains? YES/NO
```text
> NO:
SPINNER: …Take your time. We have until the end of the cloth.
```
[NO asks again.]
```text
> YES:
```
[Three strokes. Each chain parts with a sound like a bell. For the first time in a thousand years, three pairs of hands stop moving.]
```text
SPINNER: Oh. My hands.

MEASURER: They're still.

CUTTER: …
```
[Phaedon stands.]
```text
PHAEDON: Thank you. I mean that. I'll always mean that.

PHAEDON: Lord of Time. Your sickle's here.
```
[The Harpe tears itself out of the player's hands and flies down into the chasm. Darkness. A sound like a mountain breathing.]
```text
HYPERION: It's coming up! Back from the edge, Unwoven!
```
[The Lord of Time rises out of the chasm. The whole screen shakes. Its eyes find the Loom.]
```text
PHAEDON: Stop the cutting. Stop all of it. Let nothing end.
```
[It lays the Harpe across the warp. Every thread stops swaying. The music box's tick stops, then starts again, slower. Color drains from the Loom outward until the whole screen is gray, except for the player.]
```text
CUTTER: Go! Sisters, go!
```
[Three sparks, white, gray and black, leap from the Fates and shoot up through the ceiling. The Fates' figures fade. The Lord of Time rises through the rock above, and gray sky shows through. A stair of pale stone unfolds upward behind it. Phaedon and Hyperion step onto it.]
```text
PHAEDON: Come up when you're ready. I'll tell you all of it then.
```
[They climb out of sight.]
```text
The Loom is still. Every thread hangs where it stopped.

Somewhere very far off, a music box is ticking.

You can move. You seem to be the only one.
```

## 7.7 The Frozen Hour

- **Where:** all of Aethos, gray.
- **Owner:** this sequence is the Frozen Hour's script. Order is free, but Astyra is required, and every anointed herm points to the next place you haven't been.
- **Rules:** no wild encounters, no music but the music box (§6.12).

**At Delphoi, climbing out.** [The Omphalos court. Gray. Nothing moves.]
```text
The sky is the color of ash. Nothing moves anywhere.
```
| Interact with | Text |
|---|---|
| Mom, at the top of the stair, hands clasped | "She's warm. She doesn't move." / "She was waiting for you to come back up." |
| Alethea, lamp raised | "The lamp's flame has stopped mid-flicker. It gives no light at all." |
| Rhea, arms spread | "Rhea stands between the stair and the Titans. Between them and her son." |
| Kleon, mid-swing | "Kleon's mouth is open on a shout." |
| The Archon, at the gate | "The Archon, mid-stride at the gate. Late. He looks as if he knew he would be." |
| The Stair, before any Fate is roused | "The first step won't take your weight. The hour is holding its breath." |
| An anointed herm | "The herm's stone face has turned. It's looking toward Kaldera." (The text names whichever place it points to.) |
| A bird in the air, anywhere | "A bird hangs in the air, wings up. You could touch it." |

**Kaldera's forge: the Cutter.** [Talos frozen at the anvil, hammer raised. Sparks hang in the air like small stars. On the cold anvil sits a gray figure with shears in her lap.]
```text
CUTTER: You found me. Good. I wasn't sure anyone could.

CUTTER: I've cut every thread in Aethos. Every one, for a thousand years.

CUTTER: I always knew when. Before they were born, I knew.

CUTTER: Do you know what it's like? To love someone you've already cut?

CUTTER: …Now I don't know anything. My hands are empty.

CUTTER: It's the most frightening thing that's ever happened to me.

CUTTER: Help me up.
```
[The player takes her hand. A little color comes into her: black, then terracotta.]
```text
CUTTER: Warm. Of course you're warm. You're the only thing still going.

CUTTER: Four hours of the stair are mine. They'll take your weight now.

CUTTER: Go and get my sisters.
```
[Her spark flies toward Delphoi. Four landings open. The herms re-point.]

**The Pool of Mnemosyne: the Measurer.** [Arkadia's cypress wood, gray. The pool is the only thing in the world that moves: its surface ripples.]
```text
MEASURER: The pool remembers. Even now. Memory doesn't need time to move.

MEASURER: Look in. I'll show you who chained us.
```
[The pool's picture, in sepia: a young man in a white cloak at the Loom, hammering a black chain onto a post. Three figures stand at the warp with their backs to him.]
```text
MEDON: The Oracle said a king's death would save the city.

MEDON: So my father put on a peasant's cloak and walked into the spears.

MEDON: If oracles can be wrong, he died for nothing.

MEDON: So they won't be. Not ever again. Not for anyone.

MEDON: Hold still. Please. I'm sorry. Hold still.
```
[The sepia fades. Gray again.]
```text
MEASURER: Medon. The first Archon. He cried the whole time he worked.

MEASURER: He made every knot tight, so his father's would mean something.

MEASURER: Grief is a very strong smith.

MEASURER: He kept one last knot. Archons have kept it ever since. In a box.

MEASURER: Remember that, after.

MEASURER: And go to the city before you go home. The healer is there.

MEASURER: He isn't at the top of the stair. He's with her.

MEASURER: Your hand, please.
```
[The player takes her hand.]
```text
MEASURER: Four more hours. That's eight. The last four are my little sister's.
```

**Astyra.** [Gray streets. A herald stopped mid-shout. Lysimachos frozen over a basket of ostraka. A Kronist frozen on his cart with his mouth open.]

| Interact with | Text |
|---|---|
| The Kairos statue | "The runner on the razor. Someone scratched a sickle over his face." / "In the gray, the scratch is the only thing that looks new." |
| Lysimachos | "He's holding up a shard. It says ARISTEIDES." |

[The Stoa. Keeper Lykophron sits frozen at his desk, stylus raised.]
```text
A wax tablet lies under his hand.

“DECREE OF THE GOLDEN AGE. In the first hour without end…

…by the will of Kronos, its Keeper shall be Iape-”

The stylus stopped two letters short of his own name.
```
?? Take the tablet? YES/NO
```text
> YES:
{PLAYER} took the unfinished decree.

> NO:
You leave him to it. He isn't going anywhere.
```
[Optional. The trial (L-2) uses it if you have it, and stands without it.]

[Phaedon's house. Elpis's room. Elpis frozen in bed, mouth open on a note, the clay bull in her arms. Daphne frozen in the chair, a book open in her lap. On the shelf a small bronze music box ticks: the only moving thing in the room. On the floor by the bed sits Phaedon, in color, holding Elpis's hand. He doesn't look up.]

| Interact with | Text |
|---|---|
| The music box | "It's ticking. It's the tune you've heard everywhere since the world stopped." / "A scratched label: From Papa's friend under the island." |
```text
PHAEDON: She was humming when it stopped.

PHAEDON: I've been sitting here trying to remember how it ends.

PHAEDON: Seven years, every night. She never gets to the end.

PHAEDON: She always falls asleep first.

PHAEDON: Daphne was reading to her. The olive on the Akropolis. The one that grew back.

PHAEDON: I read her the rest. I don't know if she can hear me.

PHAEDON: It isn't a garden. I thought it would be a garden.

PHAEDON: I thought she'd play in it. Forever. Never tired.

PHAEDON: She isn't tired. She isn't anything.
```
?? Show him the sealed tablet? YES/NO
```text
> NO:
Phaedon doesn't look up.
```
[NO asks again on the next talk.]
```text
> YES:
```
[Phaedon takes it. He looks at the seal for a long time. He breaks it.]
```text
PHAEDON: “ELPIS, DAUGHTER OF PHAEDON. Revised.”

PHAEDON: “Short is her thread. The shears are near.”

PHAEDON: That's it. That's what they gave me.

PHAEDON: And underneath, in different writing…

PHAEDON: “Scraped from the wax. The Pythia's words, as she spoke them:”

PHAEDON: “Her thread ends the day the hours stop.”

PHAEDON: “Truthfully. Alethea.”
```
[Hold 90 frames. The music box ticks.]
```text
PHAEDON: The day the hours stop.

PHAEDON: Not young. Not soon. The day the hours stop.

PHAEDON: That's never. It was always never. Unless someone…
```
[He looks at the gray window.]
```text
PHAEDON: …I stopped them.

PHAEDON: He handed me a short thread, and I went and made it true.

PHAEDON: Her thread's ended. Tonight. I ended it.
```
[He stands, slowly, still holding her hand.]
```text
PHAEDON: Do you understand? If you wake the world, it's already cut.

PHAEDON: She won't wake with it. She can't. Her thread is done.

PHAEDON: This way she's here. Humming. I can hold her hand.

PHAEDON: I'm sorry. I'll be at the top of the stair.

PHAEDON: Please don't come up.
```
[He lets go of her hand, very carefully, and leaves.]
```text
Elpis's mouth is open on a note. You don't know which one.
```

**Elaia: home.** [Gray. Halia frozen under her canopy, spindle mid-turn. The kid's Wooloo stopped mid-chew on a garland. The player's house is empty, the hearth cold.]

| Interact with | Text |
|---|---|
| Mom's loom | "The traveling cloak is finished. It's folded on the stool." / "A note is pinned to it: Someday. -M." Then ?? Put it on? If YES: "{PLAYER} put on Melitta's cloak." (Cosmetic: decision S13.) |
| The honey shelf | "There's a clean ring where the jar sat. No dust. It wasn't gone long." |
| The knucklebones | "Record against Mom: 0 wins, 212 losses." / "Now you know why." |
| Halia | "Her spindle is mid-turn. She's frowning at it, the way she frowned at you." |

[The square. Among the roots of the old olive sits a gray figure with a distaff.]
```text
SPINNER: There you are. Back where you started.

SPINNER: This is where your thread came up. Out of the dark, like a root.

SPINNER: We didn't spin it. You did. You've been spinning it all along.

SPINNER: Look. It's gold. We don't spin gold. Nobody does.

SPINNER: It's what a thread looks like when nobody's decided it yet.

SPINNER: The olives came in silver on your festival day. That was us. Looking.

SPINNER: We wanted to see you on your day. We never get to see anyone's day.

SPINNER: And Halia. She tried so hard to read you. Tell her it wasn't her eyes.

SPINNER: Give me your hand. That's all twelve hours. We'll all come.
```
[The player takes her hand. Her spark flies toward Delphoi. All twelve landings open.]

**Delphoi again: Kleon wakes.** [It needs all three Fates roused and Elpis's room seen, because Phaedon goes to the top of the stair only after that scene. The player walks back through the frozen court. As the player passes Kleon, his eyes move.]

[A crack, like ice. Color runs into Kleon from his fist, then everywhere.]
```text
KLEON: -ow. OW. What-

KLEON: Why's everyone… why is everything gray?

KLEON: I heard you. Walking. Everything else stopped, and I could hear you walking.

KLEON: I had a thread. I could feel it. Like a leash. Stopped tight.

KLEON: I pulled. It hurt. I pulled anyway.
```
[He opens his fist. A short gray thread lies across his palm, snapped.]
```text
KLEON: …I think I broke it.

KLEON: So I'm like you now. No prophecy. Nothing written.

KLEON: I'll die when I die. Huh.

KLEON: That's either the worst thing that's ever happened to me, or the best.
```
[He looks at Rhea, frozen with her arms spread in front of him.]
```text
KLEON: She was standing in front of me. When it stopped. Look at her.

KLEON: …Mother.

KLEON: Right. Where's the fight? Up there? Good. Let's go up.
```

## 7.8 The Stair of Hours

- **Where:** the Stair, from the Omphalos into the sky.
- **Needs:** all twelve landings open, and Kleon awake. **Gives:** time restarts.
- **Who:** Kleon (partner), Phaedon, Hyperion, the Lord of Time, the Fates, the Moment.

[The climb. On the lower landings, frozen Titanborn stand mid-step, following their master up.]
```text
KLEON: They followed him up. He told them they'd live forever up here.

KLEON: Look at them.
```

[The twelfth landing. A sundial cut into the stone, its shadow stopped at the top of the hour. Phaedon stands beside it, and Hyperion beside him, squinting. Above them the Lord of Time fills the sky, the Harpe in its grip.]
```text
HYPERION: Is that them? I can't… it's all the same gray.

HYPERION: He said noon forever. He said I'd never lose the light.

HYPERION: It's not noon. It's not anything.

PHAEDON: I asked you not to come up.

KLEON: Yeah. We're bad at that.

PHAEDON: Kleon. You broke your own thread. I can see it. That must have hurt.

PHAEDON: You'd have made a fine healer. You never had patience for endings either.

PHAEDON: {PLAYER}. If you beat me, the world wakes. You know what that means for her.

PHAEDON: Please. Let me keep her. Like this.
```
?? YES/NO
```text
> YES:
PHAEDON: …You don't mean it. Kind people say yes first.

KLEON: Then they think. Sorry, healer.

> NO:
PHAEDON: No. I wouldn't either. Not for someone else's.
```
```text
PHAEDON: Hyperion. One more fight. Then you can rest.

HYPERION: Roast them, my lord?

PHAEDON: Gently.
```
[Multi battle with `setmultitrainerbattle`: the player and Kleon against Phaedon and Hyperion. Their defeat lines:]
```text
PHAEDON: There. Every hurt closes, if you let it.

HYPERION: Hot… no. Not hot. Cold. Everything's cold.
```
[After the battle, Hyperion sits down hard on the steps. Below the twelfth landing the stair begins to fall away, hour by hour, into the gray.]
```text
KLEON: The stair's going! Big man, it's going!

HYPERION: Where's the edge? I can't find the edge.

HYPERION: Go on, then. Leave me. I'd leave me.
```
[Kleon looks up at the Lord of Time. Then at the player. Then at Hyperion.]
```text
KLEON: That's where the song is. Up there. With you.

KLEON: Nobody's going to sing about this.

KLEON: …Good. Go on. I've got him.
```
[Kleon hauls Hyperion's arm over his shoulders and starts down the crumbling stair.]
```text
HYPERION: Who's that? Who's got me?

KLEON: Nobody. Walk.
```
[The camera stays at the top and watches them grow small. Phaedon doesn't move.]
```text
PHAEDON: I can't stop it now either. Did you know? It doesn't listen to me.

PHAEDON: It never did. It just wanted what I wanted. Nothing ending.

PHAEDON: Go. I won't stand in your way.

PHAEDON: I'll stand here and hope you lose.
```
[The player steps up into the Lord of Time's shadow. A static battle at Lv 60, catchable.]

[After it is caught or beaten:]
```text
The Lord of Time is still. The sky is still gray.

Nothing moves. Far below, the music box ticks on.
```
[Three faint sparks settle on the landing: the Fates, their hands free.]
```text
CUTTER: It's beaten. It isn't over.

MEASURER: Stopped time won't start by itself. It needs a moment.

SPINNER: Somebody has to choose one. We never have.

SPINNER: Every moment we ever saw was already woven.

CUTTER: Take one, and the world moves. We don't know what it brings.

MEASURER: Not for the girl in the city. Not for anyone.

SPINNER: There. Look.
```
[The Harpe slips from the Lord of Time's grip and tips over the landing's edge. Something small and bright comes running along its blade on tiptoe, toward you.]
```text
Something is running down the edge of the falling sickle.

Long hair in front. Nothing behind.
```
?? Take the moment? YES/NO
```text
> NO:
It's past you. Gone.
```
[NO: it wheels round in the sky and comes back along the blade, and the question is asked again.]
```text
> YES:
```
[The timing: a painted line on the paving. Press A as the forelock crosses it.]
```text
> Too early:
Too soon! It sidesteps you.

> Too late:
Too late. It's past.
```
[After a miss it comes round again, the window wider each time.]
```text
> Clean:
```
[One white frame. A sound like a breath drawn in. The music box stops ticking.]
```text
You have it by the forelock.
```
[It twists free at once, as it always does, and streaks away east into the gray.]
```text
There's nothing behind to hold. It's gone.
```
[The Harpe strikes the eleventh landing. A chime, and a twelfth of the color comes back. Then a chime on every landing below, all the way down: sky, stone, the sea far below, gold on the Omphalos. On the twelfth chime, the sundial's shadow moves. Wind. Birds. The sea. The three Fates stand on the landing, solid now, in color.]
```text
CUTTER: There. That's the end of the old cloth.

MEASURER: Everything after this, nobody wove.

SPINNER: Not us. Not anyone. It's all like yours now.
```
[Far below at the stair's foot, the Harpe lies in three pieces again.]
```text
CUTTER: We'll keep those. One each. So no one ever holds it whole again.
```
[Phaedon falls to his knees beside the sundial.]
```text
PHAEDON: Elpis.
```
[Fade to white.]

## 7.9 Elpis's line

- **Where:** Delphoi at dawn, then Astyra, Phaedon's house.
- **Gives:** Ophiuchus placed [SYSTEMS §8 #17].

[Delphoi. Dawn. Color, and noise everywhere at once. Mom's hands unclasp.]
```text
MOM: {PLAYER}!

MOM: You came back up.
```
[She holds the player. Hold 60 frames.]
```text
MOM: Don't say anything. You'll ruin it.
```
[At the stair's foot, Kleon sets Hyperion down on the Omphalos step. The sun comes up over the mountain. Hyperion turns his face to it.]
```text
HYPERION: …There it is.
```
[Rhea walks to the Archon's guard and holds out her wrists.]
```text
RHEA: Rhea. Lampito. Either name. I'm done.

KLEON: Mother-

RHEA: Good fight. Eat something.
```
[Phaedon comes down the last steps. He looks at no one.]
```text
PHAEDON: Take me to her. Please. Before they take me anywhere else.
```
[The Archon nods. Two guards go with him. Fade to Astyra. Morning comes in through the window with the city's noise: a dog, a herald, everyone talking at once. Daphne is in the chair, her book on the floor. Elpis sits up in bed with her clay bull. Phaedon stops in the doorway.]
```text
ELPIS: Papa! You missed it. I got to the end.

ELPIS: Of the song. All the way to the end. Listen.
```
[She hums the lullaby, all the way through, and for the first time it resolves.]
```text
DAPHNE: She did. I heard it. I'd never heard the end before.
```
[Phaedon kneels by the bed.]
```text
PHAEDON: Little one. Listen. The Oracle. What it said about you.

PHAEDON: It's gone. All of it. Nobody can read anybody now.

PHAEDON: Not the Pythia. Not me. I don't know how long you have.

PHAEDON: I don't know. I don't know anything.
```
[Elpis thinks about it.]
```text
ELPIS: Then my thread isn't finished yet.
```
[Hold 120 frames, with no music. Phaedon puts his face down on the blanket.]
```text
ELPIS: Papa? Are you sad or happy?

PHAEDON: I don't know that either.

ELPIS: {PLAYER}. This is Starry. Papa says there's a real one.

ELPIS: Is he still sad?
```
?? YES/NO
```text
> YES:
ELPIS: Then we should go and see him.

> NO:
ELPIS: Good. I'd like to meet him.

A new star has appeared in your Star Chart: Ophiuchus, the healer.
```

## 7.10 The Archon

- **Where:** the summit of Olympus, after the four Pantheon seats.
- **Gives:** Medon's Knot untied, the Hall of Heroes, the credits.

[A great altar under an open sky, above the clouds. Aristeides stands beside it in a plain undyed cloak. On the altar sits a small bronze box.]
```text
ARISTEIDES: You climbed. Everyone said you would. I didn't need an oracle.

ARISTEIDES: I've been Archon for twenty years. Do you know what the job is?

ARISTEIDES: Keeping a box.
```
[He opens it. Inside lies a fist-sized knot of black thread, with one red strand through it.]
```text
ARISTEIDES: Medon's Knot. The last of the chain. The one that holds the rest.

ARISTEIDES: Tie it on the Loom, and every knot goes tight again.

ARISTEIDES: Every oracle comes true. No chains needed.

ARISTEIDES: A thousand years of peace. Kings who stepped down when they were told.

ARISTEIDES: Wars nobody fought, because everyone knew who'd win.

ARISTEIDES: And now? Lakonia sharpens spears. Emporion hoards grain.

ARISTEIDES: The Pythia sits in her temple and laughs. Have you heard her laugh?

ARISTEIDES: People are frightened, child. I'm frightened.

ARISTEIDES: That forger told you to ask me about Kalliste. So ask.
```
?? Multichoice: WHAT HAPPENED? / I THINK I KNOW.
```text
> I THINK I KNOW.:
ARISTEIDES: Then you can tell me if I get it wrong.
```
```text
ARISTEIDES: Twelve years ago, the old Archon sent me to find a runaway bee.

ARISTEIDES: A melissa who left Delphoi before the night the Oracle went blind.

ARISTEIDES: I found a beekeeper on Kalliste. And a baby who never cried.

ARISTEIDES: I knocked. She didn't ask my name. She sat me down.

ARISTEIDES: Bread. Honey. The good honey.

ARISTEIDES: You don't harm the house that feeds you. That's older than Archons.

ARISTEIDES: So I went home and wrote that she'd drowned. Both of you.

ARISTEIDES: My first lie. I wrote it very badly.

ARISTEIDES: The Keeper read it. A forger knows a forgery.

ARISTEIDES: He's held it over me ever since. That's how he got his post.

ARISTEIDES: That's how they found you. That's why a girl was voted out of my city.

ARISTEIDES: Everything else in my life was written. That wasn't.

ARISTEIDES: The one thing I ever chose. And look what it did.

ARISTEIDES: I spared one free child, and the world stopped.

ARISTEIDES: What happens when everyone is free?
```
[He closes the box.]
```text
ARISTEIDES: The law of Olympus is simple. Whoever beats the Archon keeps the box.

ARISTEIDES: If I win, I carry this to Delphoi and tie it at the new moon.

ARISTEIDES: If you win… it's yours. And so is the fear.

ARISTEIDES: I won't go easy. A just man doesn't.
```
[Battle `TRAINER_ICHOR_ARISTEIDES`. His defeat line:]
```text
ARISTEIDES: …Unwritten. All of it. Even this.
```
[After the battle, Aristeides sits on the altar step and holds out the box.]
```text
ARISTEIDES: It's yours. The box. The knot. The office. The fear.

ARISTEIDES: Archon of Aethos. Gods help you.

{PLAYER} received Medon's Knot.

It's cold and heavy. Heavier than it should be.
```
?? Untie Medon's Knot? YES/NO
```text
> NO:
The knot sits in your palm. It isn't going anywhere.
```
[NO asks again.]
```text
> YES:
```
[The player pulls at the red strand. It doesn't move.]
```text
It's tied tight. Tighter than anything you've ever held.

ARISTEIDES: It took a grieving man a whole night to tie that.

ARISTEIDES: It'll take two to undo it. Here. I'll hold. You pull.
```
[Six pulls. Each is a YES-to-continue box with a rope-creak SE.]
```text
The red strand slides a little.

…A little more.

The black loops loosen, one by one.
```
[The knot's icon steps through three looser frames. Then it is only thread, and it isn't black. It's gold.]
```text
It isn't black anymore. It's gold.
```
[A wind off the summit lifts the thread out of their hands. It drifts away over the clouds, south, toward the sea.]
```text
ARISTEIDES: …There it goes.

ARISTEIDES: I'm going home. My father collects my name on broken pots.

ARISTEIDES: He'll be pleased. He was always sick of hearing me called the Just.
```
[The Hall of Heroes. Then the credits (§6.15).]

## 7.11 The epilogue

- **Where:** Elaia, the morning after the credits: the next Klotheia.
- **Gives:** the post-game.

[Fade in. The player's room, morning. The klepsydra drips.]
```text
MOM: [offscreen] {PLAYER}! Did you fill your water clock?

MOM: [offscreen] Festival day! You can't be late on festival day!
```
[Downstairs. Mom at the hearth.]
```text
MOM: There you are. Archon of Aethos, and you still sleep like a stone.

MOM: Let me look at you. …Hm. You'll do.

MOM: Halia's in the square. She says she's reading threads anyway.

MOM: “Tradition,” she says. She can't see a single one. She's never been happier.

MOM: Oh. And there's a man from Akti in my kitchen. And his little girl.

MOM: He brought me a jar of honey. Bad honey. I've told him so.
```
[Phaedon stands by the hearth holding a jar. Elpis sits on a stool, swinging her legs.]
```text
PHAEDON: Good morning. Your mother is very honest about honey.

PHAEDON: Ione lets me come to the festival. One day a year. With a guard.

PHAEDON: The guard's at the door. He's asleep. Ione fed him.

ELPIS: I'm having my thread read! Papa says nobody can read it. That's the fun part.
```
[The square, hung with garlands. Halia under her canopy. A line of youths: Korinna's little brother, a girl from Akti, and Elpis at the end.]
```text
HALIA: Next! Hold out your hand.

HALIA: …Nothing. Not a scrap. Same as all morning.

HALIA: Well. It seems your thread is your own business.

HALIA: Next!
```
[Elpis steps up.]
```text
HALIA: And who's this? A little one. Hold out your hand, little one.

HALIA: …Nothing at all. Isn't that grand?

ELPIS: Is that bad?

HALIA: Every thread has knots, child. You'll pull through. Next!
```
[The footrace finish line. Kleon, out of breath.]
```text
KLEON: Second! I came SECOND. To a Wooloo.

KLEON: …It was a really fast Wooloo.

GYLIPPOS: Kleon.

KLEON: Fewer words. I know, Elder. I know.
```
[Rhea stands beside Gylippos with no helmet, watching her son.]
```text
RHEA: Second. Good.

KLEON: Good? GOOD?

RHEA: Next year, first. Or not. We'll see.
```
[The Akademia. Daphne and Alethea. The third krater sits on the table.]
```text
DAPHNE: There you are! Come in. Mind the scrolls. They still bite.

DAPHNE: Elpis! You came. There's someone here who's waited a whole year.

DAPHNE: I told everyone. Someone always comes late.
```
[Elpis looks into the krater. The last starter looks back.]
```text
ELPIS: Hello. I'm Elpis. I don't know how long I've got. Do you?
```
[The starter climbs out into her arms.]
```text
ALETHEA: I'm writing it all down. The Loom. The Stair. All of it.

ALETHEA: Truthfully. Every word. It's going to be very long.

ALETHEA: Kleon asked me to leave him out of it. I said no.

DAPHNE: {PLAYER}. Before anything else, a question. Humor me.

DAPHNE: Which came first? The Pokémon, or the story?
```
?? Multichoice: THE POKéMON / THE STORY / WE'LL SEE
```text
> THE POKéMON:
DAPHNE: Still my answer too. I'd still love to be wrong.

> THE STORY:
DAPHNE: Still a heretic! Wonderful.

> WE'LL SEE:
DAPHNE: …Ha! Oh, that's the best one yet.
```
```text
DAPHNE: Alethea, write that down.

ALETHEA: …I'm writing that down.
```
[Fade out. The player is free. The post-game begins.]

---

# 8. Proposed changes and decisions

Everything here is small, and nothing is applied until the user approves it.

## 8.1 Changes to PITCH.md

| § | Change |
|---|---|
| §2, the cast | **The hero:** add "The Spinner unspun their one-hour thread at their mother's plea; the thread they spin themselves is gold."<br>**Mom (Melitta):** a new entry, "a former melissa of Delphoi, who begged the Fates for her child and fled".<br>**Daphne:** "knows why the hero has no thread; her banned book on the Harpe is the Titans' map; Phaedon was her friend".<br>**Alethea:** "her reading said she'd never be believed; becomes Keeper of Records".<br>**Kleon:** "Rhea's son".<br>**The admins:** replace the one-word lines with §2's one-sentence summaries: Hyperion, going blind, wants an endless noon; Iapetos, the Archon's Keeper of Records and former Delphic prophetes, wants to write the last draft of the world; Rhea, Kleon's mother, buried two children to prophecy.<br>**Kronos:** add "his daughter's oracle was forged by Iapetos; the true one said her thread ends the day the hours stop".<br>**The Archon:** add "spared the infant hero under the law of xenia; keeps Medon's Knot".<br>**Add:** Medon, the first Archon, son of Kodros. |
| §2, Act I step 5 | "…and yours isn't on it. *Why* waits for your mother, at Delphoi." |
| §2, Act II | **Step 1:** Iapetos's tragedy is *The Unwoven*; it puts the hero's own origin on stage, and the satyr play breaks it.<br>**New step:** the ostracism of Alethea, in Astyra.<br>**Step 4:** the Akropolis is the midpoint, where Kleon tells you they want *you*.<br>**New last step:** Kaldera is the low point, where Mom has vanished. |
| §2, Act III | **Step 3:** Lakonia: Rhea unmasks for her son.<br>**Step 4:** Delphoi: Mom tells you everything.<br>**Step 5:** the Loom: the Fates ask to be freed, knowing the cost.<br>**Step 6:** the Frozen Hour: Phaedon at Elpis's bedside reads the true oracle; Kleon breaks his own thread.<br>**Step 7:** the Stair: Kleon carries Hyperion down; after the Lord of Time, **the Moment** must be seized to restart time.<br>**Step 9:** the League: the Archon keeps Medon's Knot, and you untie it together.<br>**Add:** the epilogue, the next Klotheia. |
| §2, Dialga | Becomes **the Lord of Time** (the dex's Kronolith) throughout, if dex D2 is approved. |
| §4, myth table | The Fates become the three Moirai of the Aethos dex; Kronos becomes the Lord of Time. **Add** Kairos, the Moment (the dex's Kairazor). The rest of the dex casting is §2's table here. |
| §6 | One line per epic, from §3's post-game spine. Add: Medon and Kodros in the Underworld; Penelope in the Odyssey; the Moment at Olympia. |
| TERMS.md | **Resolve the flag** "the bible never says the title passes to the player": it does (decision S7). |

## 8.2 Changes to the slice, `design/phase1/SCRIPT.md`

The slice already carries almost every seed this story needs. Two small additions are proposed, both optional.

1. **The traveling scribe**, in Elaia's square during beats 2–4.
   - It is Iapetos, unrecognizable, and the first sighting of the hook.
   - It costs one object event, three lines, one sign object and one hide flag (`FLAG_ICHOR_HIDE_SCRIBE`, set after beat 4).

   ```text
   > before FLAG_ICHOR_THREAD_READ:
   SCRIBE: Don't mind me. I collect fortunes. For a book.

   > after FLAG_ICHOR_THREAD_READ:
   SCRIBE: Yours stopped her spindle. In forty years, she says. Never once.

   SCRIBE: May I tell you something true? You're going to be in my book.

   [Object: the scribe's stool]
   A wax tablet on a stool. Neat writing. Every line ends in a little hook.
   ```
2. **LABYRINTH's L8**, the tablet's last line, as already proposed: "Last, the house of the double axe." / "That's not a riddle. That's just rude."

Kleon's mother's letters and Mom's harbor line are in Phase 2, not the slice. No built line changes.

## 8.3 Changes to LABYRINTH.md and SYSTEMS.md

| Doc | Change |
|---|---|
| LABYRINTH §8 | The four additions in §7.4: the Elpis tablet in Scene H; Daphne's book lines in Scene J; the tablet exchange in Scene J; Rhea's look at Kleon. |
| LABYRINTH §9, trainers | Recast Kleon and Hyperion at Knossa with Aethos species (§2), as D5 (a) requires. |
| LABYRINTH §9, music | **Unify two cues.** The workshop's ticking music box, Phaedon's theme and the Frozen Hour's music box become **one melody, Elpis's lullaby**. Daedalus built Elpis's box, and the workshop's is his prototype. |
| SYSTEMS §10, the finale | Mom gives the jar away at Delphoi, so in the post-game she takes down "the new jar, labelled NOT FOR {PLAYER} again. MOM: Habit." |
| SYSTEMS §5, prophecy fragments | Use §4's table of the eight tablets. |
| SYSTEMS §9, knucklebones (optional) | Until Delphoi, Mom's throws lean lucky (the bee). After, they're fair, and she says "I gave the bee the day off." |

## 8.4 What the story asks of the engine and art

This is not a plan, only a list for the director. Each item uses an existing system.

1. **The Frozen Hour gray.** `TintPalette_GrayScale` over every BG and OBJ palette except the player's and the three movers'. The DNS tint is suspended.
2. **The twelve-step color return** on the Stair: a small special that blends from the grayscale copy back to the true palettes in twelve steps.
3. **Sepia memory** at the Pool: `TintPalette_SepiaTone`.
4. **The frozen-world state:** NPCs as static mid-step frames. No wild encounters, and one BGM.
5. **Herm head variants:** one metatile per facing, for the Frozen Hour.
6. **The Moment's grab:** `Ichor_BullLeap` reused, with the bull swapped for the Moment.
7. **Large objects** for the Lord of Time, at the Loom and on the Stair. Their size depends on the concept the user picks.
8. **The credits frieze,** reused from the intro and scrolled the other way.
9. **New sprites:**
   - Mom in her melissa veil, Rhea unhelmeted, Phaedon kneeling.
   - Iapetos's two looks, with the ink-dark hand.
   - Daphne in sandals.
   - Hyperion with clouded eyes, as a palette tweak.

## 8.5 The Lazarus check

Nothing here touches the avoid-list.
- There are no Muses, and the villains aren't Chimera.
- There is no Mega-as-weapon plot; Apotheosis stays a battle mechanic.
- Rayquaza isn't central, and Lazarus's nine starters appear nowhere.
- There are no prefixed custom forms.
- The new names are clear of Lazarus's: Medon, Kodros, Lampito, Lykophron and the Kronists.
- **One flag:** the three Fates are a Greek-named legendary trio. The avoid-list's item is a *beast* trio, Lazarus's Raikou-style set, and the Fates were already a trio in the bible, so this doesn't clash.

## 8.6 Decisions for the user

> **Approved by the user, 2026-11-14:** S1 (Mom begged the Fates), S3 (Elpis's forged oracle), S2/S4/S5 (Rhea as Kleon's mother, Iapetos as the Keeper, the Archon's secret and Medon's Knot), and every other decision as recommended. PITCH.md §2 and §4 have been updated to match.

Each decision has a recommendation. The ones marked **★** carry the most weight in the story.

| # | Decision | Recommendation | Alternative |
|---|---|---|---|
| **S1 ★** | **Why the hero has no thread** | **Mom begged; the Spinner unspun a one-hour thread; Mom fled and gave birth under the old olive.** It is fair to every built line: the pilgrim hedge, Kydippe, the jar, the intro's golden thread. And it makes Mom the mirror of the villain: she broke fate for one child, by giving freedom, not by stopping time. | (b) The Fates spun you blank as a key to free themselves. It's colder, and it makes your freedom someone's plan. (c) Never explain it. |
| **S2 ★** | **Rhea is Kleon's mother** | **Yes.** On Crete, Rhea saves her last child from Kronos: it is her myth, literally. It doubles the weight of her mercy at Knossa, and it puts the misread prophecy in her mouth at Lakonia. | An unrelated grieving mother |
| **S3 ★** | **Elpis's oracle was forged; the true one says her thread ends "the day the hours stop", and Phaedon makes it true** | **Yes.** It is the game's central irony, Oedipus's and Kronos's at once: you make the prophecy true by fleeing it. It gives the Frozen Hour its heart, and Elpis's line its force. | Her oracle was real. Simpler, but the climax loses its turn. |
| **S4 ★** | **Iapetos is Keeper Lykophron, inside the Archon's house; Alethea is ostracized on his forgery and identifies him by his hook** | **Yes.** It is Alethea's arc and the forger's natural nemesis, and it gives the Archon's office its rot. | Iapetos only ever as a masked Titan |
| **S5 ★** | **The Archon spared you under xenia, lied, and was blackmailed for it; Medon's Knot makes the League the fight over whether fate returns** | **Yes.** The League becomes the thematic climax, and the theoxenia system pays off in the main story. | The Archon as an honest believer with no secret |
| S6 | **Daphne's secrets:** she knows why, her book was the map, and Phaedon was her friend | **Yes** | The mentor with no secret |
| S7 | **The Archon's title passes to the player** | **Yes.** It is Pokémon convention, and your first act is untying the Knot. It resolves TERMS.md's flag. | You refuse the title |
| S8 | **Phaedon's sentence:** exile to Kalliste as a suppliant at Hestia's hearth, healing at Akti | **Yes.** His punishment and his mercy are the same: an ordinary life with an unknown end. | Prison in Astyra. Not recommended: death, which would let him off. |
| S9 | **The third krater goes to Elpis at the epilogue:** "Someone always comes late." | **Yes.** Phase 2 had this open. | A Phase 2 gift |
| S10 | **The Fates' name boxes:** SPINNER, MEASURER, CUTTER | **Yes.** Their roles read better than coined names in a scene, and they survive any rename in review. | The species names |
| S11 ★ | **The Moment restarts time on the Stair, and is caught only in the post-game at Olympia** | **Yes**, if dex D3 is approved. It is the time pair's thematic shape: endless time beaten, then a moment chosen. | The Lord of Time's defeat alone restarts time, and the Moment stays purely post-game |
| S12 | **Kleon's redemption deed:** carrying the blind Hyperion down the crumbling Stair, where no one will see | **Yes** | He holds Hyperion off while you climb |
| S13 | **Optional polish:** Melitta's cloak as a palette swap after the Frozen Hour; a shadowless Hermes glimpsed in the Frozen Hour; Titan helmets melted into Asclepeion bells | **Yes to the cloak and Hermes** if cheap; the bells are optional | Cut all three |
| S14 | **The epilogue is the next Klotheia,** after the credits, and the post-game starts from it | **Yes.** The game begins and ends on the same festival. | Wake at home as in Emerald |
| S15 | **The slice seed:** the traveling scribe (§8.2) | **Yes.** Three lines. | Leave the slice untouched |
| S16 | **The Harpe's fate:** the Fates keep a piece each | **Yes** | Talos reforges it into a reaping sickle |
| S17 | **Hyperion is going blind,** and his true oracle says "and be glad of it" | **Yes** | Hyperion as pure muscle |
| S18 | **Alethea's Klotheia reading was Cassandra's curse,** and her "Truthfully" is why | **Yes** | Keep "exhausting" as the whole reading |
| S19 | **Dex D2:** the Lord of Time and the three Fates replace Dialga and the lake trio | **Yes.** The story is written for it. | Keep Dialga and the trio |
| S20 | **The time pair's design** (dex concepts A–C) | The story needs only these traits: the Lord of Time has the Harpe and a stopped hourglass, and is large enough to fill the sky; the Moment has a razor's edge and a forelock with nothing behind. **Any concept works.** | — |

