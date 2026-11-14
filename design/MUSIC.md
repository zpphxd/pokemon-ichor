# Pokémon Ichor: the score

This is the score's thematic map. It names every leitmotif, gives its notes and mode, lists where it already plays and where it will, and sets out how it changes from act to act. It works alongside:

- `design/STORY.md`: §1 "The motifs", the set pieces in §6, and "The music plan in one table";
- `design/LABYRINTH.md` §9, the Labyrinth's cues;
- `tools/ichor/music/README.md`, the pipeline, and the songs themselves in `songs.py`, `songs_engine.py` and `songs_act1.py`.

When a new cue quotes a motif, take the notes from here. If a cue needs a motif to do something this file doesn't cover, add the transformation here first.

## How to read the notation

Notes are written as the song files write them, so you can paste a line into a part:

- `D5` is a pitch (C4 is middle C), and `:n` is its length in eighth notes;
- `|` is a bar line and `r` is a rest;
- `F#5` and `Bb4` are accidentals.

Mode names follow `songs.py`. The church name comes first and the Greek name, where it differs, follows in brackets. The two systems give the same scales different names: D Dorian (church) is the Greek Phrygian, for example.

## The score in one page

D is home. Elaia, the title and the lullaby all sit on D, so the game starts there, and that is where the lullaby resolves at the very end. The modes carry meaning:

| Mode | What it means in Ichor | Heard in |
|---|---|---|
| **Dorian** (Greek Phrygian) | Home, the way things are: fated, but warm | Elaia, the title, the lullaby, the trireme |
| **Lydian** (Greek Hypolydian) | A question, hope, a thread you spin yourself. The raised fourth reaches upward and won't settle. | Daphne, the Akademia, the Asclepeion, Hermes, the ending |
| **Ionian** (Greek Lydian) | The world going about its day | Akti, Emporion, Eleusa, the victories |
| **Mixolydian** (Greek Hypophrygian) | Roads and travel, its flat seventh pointing on to the next place | Route 1, the mainland road, the Agora |
| **Phrygian** (Greek Dorian) | The sacred and the grieving, and Sparta: the semitone above the tonic | Hestia's hymn, the Mysteries, Kleon, Kronos |
| **Locrian** (Greek Mixolydian) | The Titans: a tonic whose fifth is a tritone, so it can never rest | Team Titan, the admins |

Four rules hold the score together:

1. **The lullaby never resolves until Elpis finishes it** (STORY III-12). Its last bar is written down here and nowhere is it played before then.
2. **Timbres are reserved.** The glockenspiel (`ichor` slot 10) is Elpis's music box and nothing else. The tick (slot 115) is the box's escapement and the Frozen Hour's only sound. Neither may appear in any other cue.
3. **Mom's countermelody is withheld until the Kastalian spring** (STORY §6.10). After that, Elaia's theme always carries it.
4. **The three Fates' voices sound together only at the Loom**, and again on the Stair once all three are roused.

## The leitmotifs

| # | Motif | Shape | Mode | First heard |
|---|---|---|---|---|
| 1 | **The Thread** | 5-1-2-3, rising: A-D-E-F | D Dorian | The intro's spindle; Elaia; the title |
| 2 | **Elpis's lullaby** | 3-2-1-5, falling (the Thread reversed), 8 bars, stops on 5 | D Dorian | Act II, Elpis's room |
| 3 | **Mom's countersong** | Three rising steps, "come back up the hill" | D Dorian | Act III, the Kastalian spring |
| 4 | **Daphne's Question** | 5-1-2-3, then the raised 4th, hanging | Lydian | The Akademia |
| 5 | **Kleos**, Kleon's motif | 1-♭2-1-♭7-1, then down to 5 | E Phrygian | The rival battle |
| 6 | **The Sickle**, the Titans' motif | 1-♭5-4: a tritone leap and a falling step | B Locrian | Team Titan's battle |
| 7 | **The Loom**, the Fates' theme | Three voices: spindle, rod and shears | D Dorian, on the lullaby's chords | The intro (the spindle); the Loom (all three) |
| 8 | **The Ring of Hours**, the Lord of Time | A seven-note ring, D-E♭-F-E♭-D-C♯-D, through changing meters | D Phrygian | The Loom |

They are one family. The Thread is the seed:
- the lullaby is the Thread run backwards;
- Daphne's Question is the Thread asked in Lydian;
- Mom's countersong climbs the Thread's last three steps;
- the Labyrinth's crane dance winds the same three steps back and forth;
- the Ring of Hours is the lullaby's first three notes made Phrygian and closed into a circle.

The Sickle and the Ring share the Phrygian semitone grind, the sound of time being stopped.

---

### 1. The Thread (*nēma*)

**What it is.** The call that opens the game. A rising fourth and two steps, 5-1-2-3, as a spindle twists fibre upward into thread. It is the hero's motif and the world's: everyone in Aethos has a thread, and this is what one sounds like.

**Notation.** The call, and the spindle figure the lyre spins it into, rising root, fifth, octave, ninth and tenth:

```text
call (D Dorian):       A4:2 D5:1 E5:1 F5:4
spun (the intro):      D4:1 A4:1 D5:1 E5:1 F5:4
```

**Where it plays now.**
- **The boot intro** (`mus_ichor_intro` A, `THREAD`): the Spinner's spindle, the lyre's rising figure over a chorus that climbs a step every two bars.
- **The title** (`mus_ichor_title`): the spindle in the intro, then the main theme, which opens with the call (`THEME`: A4 D5 E5 F5).
- **Elaia** (`mus_ichor_elaia` A): the lyre's tune opens with it (`A4:2 D5:1 E5:2 F5:1`).
- **Route 1**: the syrinx hook opens D-G-A-B, the call in G.
- **The Temple of Hestia**: the chorus sings it in Greek Dorian, A-D-E♭-F, with the semitone of the sacred.
- **The fanfares**: the item, key-item and starter fanfares and the title's salpinx (B) open with the call in major.
- **The mainland road** (`mus_ichor_road` C): a far-off salpinx plays C-F-G-A twice, as if from the next valley. **At night** (`mus_ichor_road_night` A2) a horn plays it in Dorian, C-F-G-A♭.
- **Daphne's revelation** (`mus_ichor_revelation` A): the lyre plays A-D-E and stops before its third, twice. There is no thread.

**How it changes.**

| When | Form |
|---|---|
| Prologue | Dorian and whole: the world as fated. |
| Act I, the revelation | Broken off before the third: the hero has none. Daphne's Question supplies the third, in Lydian. |
| Act II, the Dionysia | Iapetos's tragedy (STORY §6.3) runs on the Sickle, but when the actor in the petasos enters, the chorus sings the Thread in Phrygian: the hero's story retold as a lie. |
| Act III, the Icarus Shaft and the end of the Stair | The main theme in **D Lydian**, rising: `A4:2 D5:1 E5:1 F#5:4 \| G#5:2 F#5:1 E5:1 C#5:4 \| …`. The thread the hero spins is gold, and this is how it sounds. |
| The resolution | Elpis's last note, A rising to D, is the Thread's first interval (see 2). |
| The credits | The main theme in Lydian, then Elaia's theme with Mom's countersong under it. |

> **For the director.** STORY's music plan calls the main theme and Elaia's theme "Lydian". Both are built in D Dorian (D Greek Phrygian), and MUSIC.md keeps that: they stay Dorian until the end, and the main theme turns Lydian only at the Icarus Shaft, the end of the Stair and the credits. I suggest STORY's table say "Dorian, turning Lydian at the end" for the main theme, and "Dorian" for Elaia.

---

### 2. Elpis's lullaby (*nanourisma*)

**What it is.** The score's heart (STORY §6.14). It is a hummable eight-bar tune in 3/4 that Elpis hums, that Daedalus's music box plays, and that is Phaedon's theme. It is the Thread run backwards: the Thread climbs A-D-E-F and the lullaby falls F-E-D-A. Both of its phrases stop on A, the half cadence. Its eighth bar would come home to D, and **no version plays that bar until Elpis finishes the song** at the resolution. Every other version stops on A, because Elpis always falls asleep first.

**Notation.** D Dorian, 3/4. The chords are Dm | G | Dm | Am | F | C | G Am | (Dm).

```text
1-4  F5:2 E5:1 D5:1 A4:2 | B4:2 D5:1 E5:1 D5:2 | F5:2 E5:1 D5:1 A4:2 | C5:2 B4:1 G4:1 A4:2
5-7  F5:2 A5:2 G5:1 F5:1 | E5:2 G5:1 E5:1 C5:2 | D5:2 B4:1 C5:1 A4:2
8    D5:6        (withheld: A rises to D, the Thread's first step)
```

- B natural over the G chord in bar 2 is the Dorian colour: hope inside the minor.
- The peak, A5 in bar 5, is her wish to see the sea.
- The code has bars 1-7 as `LB_TUNE` and bar 8 as `LB_LAST` in `songs_act1.py`.

**The twelve chimes** on the Stair (STORY §6.13) are its first twelve notes, on tubular bells: F E D A, B D E D, F E D A.

**Built now.**
- **`MUS_ICHOR_ELPIS_LULLABY` (627), the hum.** For Elpis's room in Astyra (Act II), ♩=72.
  - She hums it over a lyre rocking the cradle.
  - The hum stops on the half cadence and bar 8 is the lyre alone, rocking on A.
  - Then her father's lyre takes the tune, and she joins drowsily for the last phrase, a third under, and falls asleep again.
- **`MUS_ICHOR_ELPIS_LULLABY_BOX` (628), the music box.** For Daedalus's workshop, Elpis's shelf and the whole Frozen Hour, ♩=60.
  - The comb plays the tune an octave up over its own lower teeth.
  - The escapement ticks once a second: tick, tock, tock.
  - In bar 8 the comb is silent and only the ticking goes on: the box is missing its last bar.

**How it changes.**

| When | Arrangement |
|---|---|
| Act II, Elpis's room (II-8) | The hum (627). The player hears it here first, so the Labyrinth's version lands as something already known. |
| Act II, the Asclepeion | Phaedon's theme: the hum's lyre verse alone, for the healer. |
| Act III, Daedalus's workshop | The music box (628), the prototype. |
| Act III, the unmasking (LABYRINTH Scene J) | **Phaedon's theme in minor**: D Aeolian, with B♭ for B in bars 2, 4 and 7, chords Dm \| Gm \| Dm \| Am \| F \| C \| Gm Am. Strings and a low lyre under his speech. |
| Act III, the Loom | The box's tick starts again, slower, when the gray spreads. |
| The Frozen Hour | The music box (628), alone. Each Fate's voice from the Loom joins it for the rest of her sanctuary (see 7). |
| The Stair, Kronos's theme | **Phrygian and enormous**: E♭ for E and B♭ for B, ♩=56, full ensemble with chorus and horns, and the Sickle's grind D-E♭ in the bass. Still stopping on A. |
| The Moment | The tick stops on the frame you seize it: the first silence of the Frozen Hour. |
| The resolution (III-12) | Elpis hums all eight bars, alone, and **bar 8 sounds for the first time**. A rises to D. Then 120 frames of silence. |

---

### 3. Mom's countersong

**What it is.** Melitta's theme is Elaia's harmony, not a melody of its own. It is the countermelody to Elaia's lyre tune, written for it note against note, so the players hear the home tune all game and never this line under it (STORY §6.10). Its motto is three rising steps, F-G-A, "Come back up the hill". It climbs the Thread's last three notes, as her line in the slice does: "Wherever you end up, come back up the hill."

**Notation.** D Dorian, 6/8, under Elaia's A section (`E_LYRE_A`, chords Dm | Dm C | G | Dm | F | C | G | Am). It is for a woman's hum (`ichor` slot 53, or the chorus) and the lyre:

```text
F4:3 G4:2 A4:1 | A4:3 G4:3 | G4:2 A4:1 B4:2 C5:1 | A4:3 F4:1 G4:1 A4:1 |
A4:3 C5:3 | C5:2 B4:1 G4:3 | B4:1 A4:1 G4:1 D4:3 | E4:3 A4:1 B4:1 C5:1
```

Against Elaia's lyre it moves in sixths, thirds and open fifths, with no dissonance on a strong beat (checked note by note). The motto climbs in bars 1, 3, 4 and 8.

**How it changes.**

| When | Form |
|---|---|
| The slice and Acts I-II | Withheld. Mom's scenes use Elaia's theme without it. |
| Act I, the harbor (I-2) | Still withheld. Elaia's theme on a solo lyre as the boat leaves; the motto's three steps, F-G-A, end the cue on the aulos, and nothing more. |
| Act II, Kydippe's letter at Kaldera | Elaia's theme "very slowly on one lyre" (§6.7), still without it. |
| **Act III, the Kastalian spring** | **The first time it sounds**: lyre (Elaia's tune) and a woman's hum (this line), nothing else. |
| The Frozen Hour, Mom at the top of the stair | The music box only, by rule. |
| After Delphoi | Elaia's theme always carries it, as a variant of `mus_ichor_elaia` with the aulos or hum on this line, for the director to assign when the post-Delphoi maps land. |
| The credits | Under the main theme in the second half (§6.15). |

---

### 4. Daphne's Question

**What it is.** Daphne's whole philosophy in five notes: the Thread's call, but in Lydian, with a major third and then the raised fourth, which reaches up and won't settle. "A guess is only a question that's gotten too confident." She is the laurel, Daphne, who fled a god and became a tree. In the revelation the Question is played on the syrinx, since Syrinx was the other nymph who fled a god and became a plant.

**Notation.**

```text
the Akademia (G Lydian):     D5:2 G5:1 A5:1 B5:2 G5:2 | C#6:2 B5:1 A5:1 E5:4
the revelation (D Lydian):   A4:2 D5:1 E5:1 F#5:4 | G#5:6 r:2
```

Note that the revelation's form, A-D-E-F♯-G♯, is the main theme's head in Lydian, the form the Thread takes at the end (see 1). Daphne's question is the ending, asked early.

**Where it plays now.**
- **The Akademia** (`mus_ichor_akademia` A): the lyre's tune. It opens with the Question and its second bar leans on C♯, the raised fourth.
- **Daphne's revelation** (`MUS_ICHOR_REVELATION`, 637): see "Act I's music" below.

**How it changes.**

| When | Form |
|---|---|
| Prologue, the Akademia | Bright and curious: the lyre in G Lydian over open fifths. |
| Act I, the revelation | It gives the Thread the third it was missing, then hangs on G♯. |
| Act II, the Library in Astyra | Daphne unwriting her book. The Question in minor (Dorian, G♯ lowered to G) on a solo syrinx: being wrong, painfully. |
| The Frozen Hour, Elpis's room | The music box only, by rule. Daphne is frozen with the olive story open in her lap. |
| The epilogue, "Which came first?" / "WE'LL SEE" | The Question rises to its G♯ and, for the first time, goes on to A. The question gets no answer; it just keeps going. |

---

### 5. Kleos, Kleon's motif

**What it is.** *Kleos* is glory. It is a turn around the tonic that leans on the Phrygian semitone, then drops a fourth and lands on the long last beat of the 9/8: a boy in a hurry to be remembered. Plato called the Dorian the Spartan mode, and Kleon's is the Greek Dorian (church Phrygian).

**Notation.** E Phrygian, 9/8 as 2+2+2+3:

```text
E5:1 F5:1 E5:1 D5:1 E5:2 B4:3
```

**Where it plays now.**
- **The rival battle** (`mus_ichor_battle_rival` A): the aulos opens with it, over a string ostinato on the same semitone.
- **Encounter: Kleon** (`mus_ichor_encounter_rival`): it is quoted at once.
- **The trireme** (`MUS_ICHOR_TRIREME` B): Kleon at ease on deck. The turn is in G Dorian with its semitone opened into a whole tone, G-A-G-F-G-D: the same gesture without the edge.

**How it changes.**

| When | Form |
|---|---|
| Prologue and Act I | Driving, 9/8, the aulos doubled by a square. |
| Act I, the crossing | Relaxed: whole tones, 6/8, a shipmate's song. |
| Act I, the Eleusa double battle | The rival battle's arrangement, as in the slice. Kleon is on your side, so no change is needed. |
| Act II, Arkadia's new moon (§6.4) | "A single lyre plays Kleon's rival motif in minor." It is slowed to 3/4 and loses its 9/8 drive. The semitone stays, and the final drop to B never comes: it stops on E. |
| Act II, the Akropolis | As a Titan agent his battle theme takes the Sickle's tritone: E-F-E-D-E-B♭, the fall to a diminished fifth instead of a fourth. |
| Act III, Lakonia (§6.9) | "A frame drum alone in a slow 7/8": Kleos's rhythm, 2+2+3, with no notes. |
| The Frozen Hour, Kleon breaks free | The first sound after the music box: Kleos on a single aulos, in time, over the box. |
| The Stair, carrying Hyperion down | **In major**, E-F♯-E-D♯-E-B. No one will sing about it, so it has no words and no drums. |
| The epilogue footrace | Back to 9/8, light and quick: second place, to a Wooloo. |

---

### 6. The Sickle, the Titans' motif

**What it is.** The Titans' call is a tritone leap, B up to F, the fifth that the Locrian mode has instead of a true fifth, falling a step to E. Under it the tuba and bass grind a semitone, B-B-C-B. It has the curve of a harvest blade and the sound of something that can never rest, which is the doctrine: stop every thread.

**Notation.** B Locrian (Greek Mixolydian), 9/8 as 3+2+2+2:

```text
call:  B4:3 F5:4 E5:2
grind: B1:3 B1:2 C2:2 B1:2
```

**Where it plays now.**
- **Team Titan** (`mus_ichor_titan` A): the salpinx opens with it.
- **Encounter: Titanborn** (`mus_ichor_encounter_titan`): the call, answered by silence and war drums.
- **The Titan victory** (`mus_ichor_victory_titan`): the call once more, then its B becomes the bright dominant of E.
- **The admin battle** (`MUS_ICHOR_BATTLE_ADMIN`, 636): a fourth higher, E-B♭-A, in 7/8, and at the end of C as harmony, B♭ to E.

**How it changes.**

| When | Form |
|---|---|
| Prologue (grunts) | 9/8, salpinx and war drums. |
| Act I, the admins | A fourth higher and in 7/8, a gait the grunts can't march to. |
| Act II, the Kronia grounds (STORY II-1) | The feast: the call with its tritone softened to a fifth, as a major-key round dance in 7/8 on lyre and aulos with a tambourine. The Titans' public face, and the most welcoming music in Act II (`MUS_ICHOR_KRONIA`, `design/phase3/SCRIPT.md` Part 9). |
| Act II, Iapetos's tragedy (§6.3) | "Slowed into a Phrygian processional": the call on a chorus of aulos at ♩=60, with the tritone softened to a fifth. The lie sounds reasonable. |
| Act II, the Akropolis climb | The grunts' 9/8. |
| Act III, the Titan wing of the Labyrinth | The grunts' theme with the drums cut to a heartbeat (LABYRINTH §9). |
| The Stair, Kronos's theme | The grind sits under the lullaby: D-E♭, in the bass. |
| After the climax | The Titan victory's turn, the call resolving into a major key, is the doctrine undone. |

---

### 7. The Loom, the Fates' theme

**What it is.** Three voices for three women (STORY §6.11):
- Nemira the Spinner is a lyre;
- Lotira the Measurer is an aulos;
- Thanira the Cutter is a frame drum.

They are written in counterpoint to the lullaby, on its harmony and in its meter. That is what lets each Fate's voice join the music box in the Frozen Hour, and it is why the Loom and Elpis's song sound like one cloth.

**Notation.** D Dorian, 3/4, on the lullaby's chords:

```text
Nemira, the spindle (lyre): the Thread spun, root-fifth-octave-ninth-tenth, every bar
  D4:1 A4:1 D5:1 E5:1 F5:2 | G3:1 D4:1 G4:1 A4:1 B4:2 | D4:1 A4:1 D5:1 E5:1 F5:2 | A3:1 E4:1 A4:1 B4:1 C5:2 |
  F3:1 C4:1 F4:1 G4:1 A4:2 | C4:1 G4:1 C5:1 D5:1 E5:2 | G3:1 D4:1 G4:1 B4:1 A4:2 | C5:1 B4:1 A4:1 E4:1 A3:2
Lotira, the rod (aulos): one note a bar, down a tetrachord and back, measuring
  A4:6 | G4:6 | F4:6 | E4:6 | F4:6 | G4:6 | A4:6 | r:6
Thanira, the shears (frame drum): one stroke a bar
  dum:6 | dum:6 | dum:6 | dum:6 | dum:6 | dum:6 | dum:6 | tek:0.5_ ×12 (a trembling roll; no stroke)
```

Bar 8, the lullaby's missing bar, is the hero's bar, and all three Fates falter in it as the intro shows them (STORY §2):
- the spindle turns backwards, because Nemira unspun you;
- the rod rests, because Lotira found nothing to measure;
- the shears tremble open and don't close, because Thanira couldn't cut.

Against the lullaby the rod moves mostly in sixths, thirds and octaves.

**Where it plays now.** The boot intro's spindle (`mus_ichor_intro` A, the lyre) is Nemira's voice, in 4/4. Nothing else yet.

**How it changes.**

| When | Form |
|---|---|
| Prologue, the boot intro | Nemira alone: the spindle. |
| Act III, the Loom | **All three for the first time**, with no lullaby on top: the cloth itself. When the gray spreads, every voice stops on a single beat. Silence, then the tick. |
| The Frozen Hour | Each roused Fate's voice joins the music box for the rest of her sanctuary: Thanira at Kaldera's forge, Lotira at the Pool of Mnemosyne, Nemira at the old olive in Elaia. Build these as three variants of 628 that add one track each. |
| The Stair, once all three are roused | All three with the music box. Then the Lord of Time's battle. |
| The resolution | The Fates come down with their hands free: the three voices once more, and in bar 8 the shears are put down for good (no roll, no stroke) while the spindle turns forwards. |

---

### 8. The Ring of Hours, the Lord of Time

**What it is.** Kronos devours: he ate his children so that nothing after him could happen. His motif is the lullaby's head, F-E-D, swallowed into Phrygian, F-E♭-D, and closed into a ring that turns around D and never leaves it. STORY asks for a battle that "switches meter every phrase, from 7/8 to 9/8 to 5/8 and back, as if time can't settle". The ring is seven notes long, so it fills a bar of 7/8, overruns a bar of 9/8 and is cut short by a bar of 5/8. It never lands on the same beat twice.

**Notation.** D Phrygian with the raised seventh (C♯):

```text
the ring:            D3:1 Eb3:1 F3:1 Eb3:1 D3:1 C#3:1 D3:1
across the meters:   7/8 | 9/8 | 5/8 | 9/8, the ring running on through the bar lines
```

Above it the brass play the Sickle on D (D-A♭-G), its tritone grinding against the ring, and the chorus holds the lullaby's A, its half cadence, which never resolves.

**How it changes.**

| When | Form |
|---|---|
| Act III, the Loom (it rises) | The ring alone, low, on the tuba, under the Fates' last bar. |
| The Frozen Hour | Never heard. Only the box plays. |
| The Stair, its battle | The ring through the changing meters, full ensemble. |
| The Moment | The ring stops mid-turn, and the tick stops with it. |
| The post-game rematch | The battle, unchanged. Time hasn't learned anything. |

---

## Two supporting motifs

### Demeter's motif: grief and return

Written for the Mysteries and for Eleusa. Above ground, in the wheat, it is Kore come home. Below, in the Telesterion, it is her mother's grief. It has three parts:
- a sigh around the tonic, her daughter's name;
- a climb that searches and finds nothing;
- the falling tetrachord D-C-B♭-A, the lament.

```text
grief (A Phrygian, 4/4):   A4:2 Bb4:2 A4:4 | C5:2 D5:2 E5:2 F5:1 E5:1 | E5:2 F5:2 E5:4 | D5:2 C5:2 Bb4:2 A4:2
return (A Ionian, 2/4):    A4:2 B4:2 | A4:4 | C#5:2 D5:2 | E5:2 F#5:1 E5:1 | E5:2 F#5:2 | E5:4 | D5:2 C#5:2 | B4:2 A4:2
```

- **Now:** grief in `MUS_ICHOR_TEMPLE_DEMETER` B (the aulos, twice, the second a fifth higher); return in `MUS_ICHOR_ELEUSA` A and A2 (the aulos).
- **Later:**
  - Demeter's myth-quest at the Maiden's Well (SYSTEMS §10): grief on a solo aulos, then, when Iambe's joke lands, the return.
  - The post-game Underworld: grief on a lyre for Persephone, in Hades's house.
- **The ending:** Chloe's secret, "What's reaped grows again", is the return form. At the end of the Mysteries' A2 the chord turns major, a promise the loop doesn't keep yet.

### The Labyrinth's crane dance (approved in LABYRINTH §9)

`D E F G E F G E A`, the motif of the Labyrinth's music and Ariadne's dance. It is the Thread's last three steps, D-E-F, wound back and forth: Ariadne's thread through the rings.

---

## Act I's music (Phase 2)

These are new in `tools/ichor/music/songs_act1.py`. Map music isn't assigned; the director does that when the maps land.

| ID | Song | For | Motifs |
|---|---|---|---|
| 627 | `MUS_ICHOR_ELPIS_LULLABY` | Elpis's room (Act II) | The lullaby, hummed |
| 628 | `MUS_ICHOR_ELPIS_LULLABY_BOX` | The workshop; the Frozen Hour | The lullaby, the music box |
| 629 | `MUS_ICHOR_TRIREME` | The crossing on the *Euploia* | Kleos (relaxed) in B |
| 630 | `MUS_ICHOR_ROAD` | Act I's mainland routes | The Thread, on a distant salpinx |
| 631 | `MUS_ICHOR_ROAD_NIGHT` | The same roads at night | The Thread, in Dorian, on a far horn |
| 632 | `MUS_ICHOR_EMPORION` | Emporion City | — (the city's own) |
| 633 | `MUS_ICHOR_TEMPLE_HERMES` | The Herald's Run | — (the lyre and syrinx trading, as in the *Hymn to Hermes*) |
| 634 | `MUS_ICHOR_ELEUSA` | Eleusa Village | Demeter's motif, return |
| 635 | `MUS_ICHOR_TEMPLE_DEMETER` | The Telesterion and the Mysteries | Demeter's motif, grief |
| 636 | `MUS_ICHOR_BATTLE_ADMIN` | Hyperion at Eleusa; Iapetos's and Rhea's first battles | The Sickle |
| 637 | `MUS_ICHOR_REVELATION` | Daphne's revelation (I-7) | The Thread meets Daphne's Question |
| 638 | `MUS_ICHOR_HOLLOW` | Hecate's Hollow; any cave or wood | — (reusable) |

The **night road** needs no map work. `sNightMusicTable` in `src/overworld.c` maps 630 to 631, so any map that plays the road plays its night form after dark. The switch happens on a map change, as with any night music. A map can still name its own `night_music` in `map.json`.

**The revelation**, cue by cue against §7.1:
- The intro is the one sustained aulos note the bible asks for. It plays under "She didn't see one at all."
- A is the Thread trying and failing, under "Not you." and "That part isn't mine to tell."
- B is Daphne's part: the Question, the climb in tenths under "they put it in the sky", and the triangle's stars for the Star Chart.
- It loops for as long as the dialogue runs.

**The admin battle** keeps its tenth track free for each admin's own top layer, so it doesn't need re-orchestrating later:
- Hyperion: forge hammers (anvil hits), from Kaldera on;
- Iapetos: a chorus of aulos doubling the strings;
- Rhea: a slow 7/8 Lakonian frame drum, half time against the 2+2+3.

Each is a copy of 636 with the one extra track.

## Themes still to write

| Theme | Brief | Source |
|---|---|---|
| Alethea | Played once, alone, on a lyre, after the ostracism. Truth that isn't believed: a plain diatonic tune that repeats its first phrase as if insisting. | STORY §6.5 |
| The Fates at the Loom | The three voices above as a cue of their own. | §7 here |
| Phaedon's theme in minor | The lullaby in D Aeolian. | §2 here |
| Kronos | The lullaby in Phrygian, enormous. | §2 here |
| The Lord of Time | The Ring of Hours. | §8 here |
| The Archon | Mixolydian, stately, kithara and drum; it stops on "Gods help you". | STORY §6.15 |
| Iapetos's tragedy and the satyr play | The Sickle as a processional; a fast 9/8 aulos romp. | STORY §6.3 |
| The Hierophant battle | Not yet scored. | INVENTORY §8 |

## What the engine taught us

These came up while building Act I, and they apply to every cue.

- **A sine bass must not double a DirectSound note in unison.** The wave channel and the DirectSound mixer drift in phase from pass to pass, so a unison beats differently each time. The trireme's bass sat on the kithara's roots and its loop passes differed by up to 4 dB. Keep the bass an octave under any DirectSound instrument's lowest notes.
- **Harp tails count.** `compose.py --check` counts gated notes only, but the harp (slot 46) rings for about a second after each note. A harp arpeggio of six notes a bar holds four or five mixer channels by itself. Over other voices it forces steals, and those land differently from pass to pass. For a sparkle over a busy texture, use a square wave.
- **A music box is near-silence by design.** 628 measures about 2 dB under its counterpart, and its seam reading is digital silence: bar 8 is the tick alone. Both are deliberate.
