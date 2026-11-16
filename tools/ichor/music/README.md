# Ichor music

The songs are original. Their notes are plain text in three files:
- `songs.py`: the slice's map, battle and victory themes;
- `songs_engine.py`: fanfares, encounter themes, the other victories, evolution, the title, the intro and the new-game speech;
- `songs_act1.py`: Act I (Phase 2) and Elpis's lullaby.

The leitmotifs they share, and how each changes through the game, are mapped in `design/MUSIC.md`. Quote a motif from there. `compose.py` turns the songs into `sound/songs/midi/mus_ichor_*.mid`. `make` then converts those with `mid2agb`, using the flags in `midi.cfg`. The `.mid` files are committed and reproducible.

```bash
python3 tools/ichor/music/compose.py            # rewrite the .mid files after editing songs.py
python3 tools/ichor/music/compose.py --check    # bar lengths, ranges, mode, voicegroup slots, loop safety, staleness
python3 tools/ichor/music/compose.py --summary  # form, timing and ranges
python3 tools/ichor/music/preview.py            # after make: GBA-accurate WAVs in build/ichor_music/
```

`--check` fails on any of these:
- a bar that doesn't fill its meter
- a note outside its instrument's range, or outside the mode
- a program or drum key that is empty in the voicegroup
- a note that crosses the loop start or hangs past the loop end
- two tracks overlapping on one PSG channel
- a PSG note below C2, where m4a clamps the pitch
- a stale `.mid`
- a song whose `gSongTable` slot (its `song_id`) doesn't play it
- a fanfare that doesn't fit its `sFanfares` duration in `src/sound.c` (it must last at least as long as the song and at most 30 frames more)

It also warns when a loop isn't a whole number of frames. m4a advances `tempo / 150` ticks a frame, so the loop's ticks × 150 ÷ tempo should come out whole. Otherwise each pass starts at a different sub-frame phase, and the passes drift apart slightly in onsets and DirectSound channel steals. Pick a nearby even tempo that divides evenly.

`preview.py` patches a copy of the ROM so the title screen plays the song, then records the mGBA mix. It forces the song onto the BGM player, since fanfares normally use SE2 and the title screen watches BGM. It also silences the attract-mode intro, so the first sound after START is the song's first note. The intro itself is recorded from boot.

It prints loudness and clipped samples, and for a song that replaces a vanilla one, that song's level (`ref`, measured before its slot was repointed). A one-shot (a fanfare, the title, the intro) is measured over its own length only. For loops it also compares the second pass with the first, in two ways:
- **pass match** correlates their envelopes. It reads low on flat, sustained textures such as the temple hymn.
- **worst 1s** is the largest level difference between the passes over any one-second window. A hung or dropped note shows up as several dB, while a clean loop stays near 1 dB.

It also reports **seam low**: the quietest 100 ms within half a second of the loop point, relative to the song. A gap at the seam shows up here.

Name other songs on the command line to render them too, such as `MUS_POKE_CENTER` or `MUS_VS_WILD`. `NAME:seconds` measures a one-shot reference over that span, such as `MUS_RG_OBTAIN_KEY_ITEM:4.1`.

When you balance volumes, keep the PSG in mind:
- PSG levels are coarse. The wave channel has only four output levels (`gCgb3Vol`: 25, 50, 75 and 100%).
- A small change to `-V` or to a wave track's volume can therefore jump the bass by 6 dB and swamp the tune.
- Re-run `preview.py` after any volume change and compare the result with the reference songs.
- Current levels are within about 1 dB of the Emerald song each one replaces, as `preview.py` prints them. The exceptions are deliberate:
  - the new-game speech sits under the Route 122 theme it replaces;
  - the key-item and starter fanfares have no Emerald counterpart. The key-item fanfare sits beside the item fanfare, and the starter's fanfare a little above it;
  - the music box (628) sits about 2 dB under Sealed Chamber, because the Frozen Hour is near-silence. Its seam reads as digital silence, since bar 8 is the tick alone.
- Songs with no vanilla slot name an Emerald counterpart in `ref` to match. For example, the trireme matches `MUS_SAILING` and the admin battle matches `MUS_VS_AQUA_MAGMA_LEADER`.
- To change `-V` without moving a wave or square track, scale that track's volume the other way. Its envelope goal is about `velocity × volume × (V / 127) / 1024`, rounded down to one of 16 steps, and the wave channel turns those 16 into its four. Steps 2–5 give 25%, 6–9 give 50%, 10–13 give 75% and 14–15 give 100%.

Two things make loop passes differ, and `--check` can't see either:
- **A sine bass in unison with a DirectSound note.** The wave channel and the mixer drift in phase from pass to pass, so the unison beats differently each time, by up to 4 dB in `worst 1s`. Keep the bass an octave under the lowest notes of the kithara and other DirectSound parts.
- **Harp tails.** `--check` counts gated notes only, but the harp (46) rings for about a second after each one. A six-note-a-bar harp arpeggio holds four or five mixer channels by itself. Over a busy texture it forces steals, and those land differently from pass to pass. Give a sparkle like that to a square wave instead.

The previews run at the GBA's 59.73 frames a second, so a loop measures about 0.5% longer than its nominal length. The trireme's 57.60 s reads as 57.90 s.

## Auditioning in-game

The songs are in the debug menu's sound test. This needs a non-release build, which is the default.
1. In the overworld, hold **R** and press **START**. Choose **Sound… → Music…**.
2. Press **→** twice to move the cursor to the hundreds digit, then press **↑** three times. The list stops at its last song, 638 `MUS_ICHOR_HOLLOW`.
3. Press **←** twice to return to the ones digit. Each **↓** steps back one song, down to 610 `MUS_ICHOR_ELAIA`. Act I's songs are 627 to 638.
4. Songs that replace a vanilla one play under the vanilla name, for example 368 `MUS_HEAL` or 413 `MUS_TITLE`.
5. **A** plays, **START** stops, **B** leaves the menu with the song still playing.

## Replacing vanilla songs in place

Map themes get their own `MUS_ICHOR_*` ID, and the director assigns them in `map.json`. Music the engine or the shared scripts trigger keeps its vanilla ID instead. Its line in `sound/song_table.inc` points at the Ichor song (marked `@ Ichor: was mus_…`), so no C, script or `map.json` caller changes. Unreferenced vanilla songs are then dropped by the linker, and the `MUS_RG_*` (FRLG) slots stay as they were.

| Vanilla slot | Now plays |
|---|---|
| `MUS_LEVEL_UP`, `MUS_OBTAIN_ITEM`, `MUS_OBTAIN_TMHM`, `MUS_HEAL`, `MUS_OBTAIN_BADGE`, `MUS_EVOLVED` (also the "Gotcha!" jingle) | the `mus_ichor_` fanfare of the same name; the badge is the Laurel |
| `MUS_EVOLUTION_INTRO`, `MUS_EVOLUTION`, `MUS_CAUGHT` | `mus_ichor_evolution_intro`, `mus_ichor_evolution`, `mus_ichor_caught` |
| `MUS_VICTORY_WILD`, `MUS_VICTORY_GYM_LEADER`, `MUS_VICTORY_AQUA_MAGMA` | `mus_ichor_victory_wild`, `_laurel` (Hierophants), `_titan` (Titanborn) |
| `MUS_ENCOUNTER_MALE`, `_FEMALE`, `_INTENSE`, `_SUSPICIOUS`, `_HIKER` | the `mus_ichor_encounter_` theme of the same name |
| `MUS_ENCOUNTER_BRENDAN`, `_MAY` / `_MAGMA` | `mus_ichor_encounter_rival` / `mus_ichor_encounter_titan` (the same songs as the new IDs) |
| `MUS_TITLE`, `MUS_INTRO` | `mus_ichor_title`, `mus_ichor_intro` |

New IDs:
- 620 `MUS_ICHOR_ENCOUNTER_RIVAL`: trainers with `Music: Rival`, `TRAINER_ENCOUNTER_MUSIC_RIVAL`
- 621 `MUS_ICHOR_ENCOUNTER_TITAN`: `Music: Titan`
- 622 `MUS_ICHOR_OBTAIN_KEY_ITEM`: a fanfare. `Std_ObtainItem` plays it for every key item.
- 623 `MUS_ICHOR_OBTAIN_MON`: a fanfare for receiving a Pokémon, the starter
- 624 `MUS_ICHOR_NEW_GAME`: Daphne's speech, from `main_menu.c`
- 625 `MUS_ICHOR_AGORA` and 626 `MUS_ICHOR_AKADEMIA`: map themes
- 627 `MUS_ICHOR_ELPIS_LULLABY` (the hum) and 628 `MUS_ICHOR_ELPIS_LULLABY_BOX` (the music box): Elpis's lullaby, for Act II and III scenes
- 629–638, Act I:
  - 629 `MUS_ICHOR_TRIREME`
  - 630 `MUS_ICHOR_ROAD` and 631 `MUS_ICHOR_ROAD_NIGHT`
  - 632 `MUS_ICHOR_EMPORION`
  - 633 `MUS_ICHOR_TEMPLE_HERMES`
  - 634 `MUS_ICHOR_ELEUSA`
  - 635 `MUS_ICHOR_TEMPLE_DEMETER`
  - 636 `MUS_ICHOR_BATTLE_ADMIN`
  - 637 `MUS_ICHOR_REVELATION`
  - 638 `MUS_ICHOR_HOLLOW`

  Map themes are assigned in each map's `map.json`. Daphne's revelation starts
  637 at “She didn't see one at all”: its intro is one sustained aulos D4, then
  the score loops while the dialogue continues. It is not saved as a map-music
  override, so the Chart fanfare resumes it and the exit restores Eleusa's theme.
  `tools/ichor/tests/sanctum.sh` checks both scene branches, the opening D4 and
  music restoration. `sNightMusicTable` in `src/overworld.c` maps 630 to 631,
  so a map that plays the road plays its night form after dark.

A new fanfare needs an `sFanfares` entry (`src/sound.c`, with a `FANFARE_*` constant in `include/constants/sound.h`), or `playfanfare` falls back to the level-up fanfare. Use `compose.py --summary` for its length in frames. Fanfares keep vanilla's player (SE2) and priority.

## The pieces

| Song | Mode, meter, tempo | Form (bars) | Voices (voicegroup) |
|---|---|---|---|
| `MUS_ICHOR_ELAIA` (610) | D Dorian, 6/8, ♩=100 | intro 2, then a loop of A 8, A2 8, B 8, C 4, A3 8. Loop 64.8 s. | `rg_credits`: lyre = harp, kithara = low harp arpeggios, aulos = oboe, string pad, sine-wave bass, frame drum (Indian drum dum, conga tek, tambourine) |
| `MUS_ICHOR_ROUTE1` (611) | G Mixolydian, 7/8 kalamatianos 3+2+2, ♩=150 | intro 2, then a loop of A 8, A2 8, B 8, C 8, A3 8. Loop 56.0 s. | `rg_sevii_route`: syrinx = flute, aulos = accordion, salpinx = trumpet, kithara = nylon guitar, lyre = harp, wave bass, square, conga and taiko drums, noise shaker |
| `MUS_ICHOR_BATTLE_RIVAL` (612) | E Phrygian with a Phrygian-dominant E chord (G♯) in B, 9/8 aksak 2+2+2+3, ♩=180 | intro 2, then a loop of A 8, A2 8, B 8, C 8. Loop 48.0 s. | `rg_credits`: aulos = oboe doubled by a square, strings ostinato, salpinx = trumpet, horn stabs, wave bass, square arpeggio, kit with taiko and congas |
| `MUS_ICHOR_AKTI` (613) | C Greek Lydian (Ionian), B♭ synemmenon in B, 4/4 island syrtos 3+1+2+2, ♩=128 | intro 2, then a loop of A 8, A2 8, B 8, C 8. Loop 60.0 s. | `ichor`: syrinx = flute, aulos = oboe, kithara = nylon guitar, lyre = harp, sine bass, square, frame drum, krotala, shaker |
| `MUS_ICHOR_TEMPLE` (614) | D Greek Dorian (church Phrygian), chromatic genus in B, 5/4 hymn 3+2, ♩=80 | intro 2, then a loop of A 8, B 8, A2 8. Loop 90.0 s. | `ichor`: chorus = choir, aulos = oboe, lyre = harp, low strings, sine bass, temple bell (intro), frame-drum hearth pulse, noise embers |
| `MUS_ICHOR_ASCLEPEION` (615) | F Hypolydian (church Lydian), 3/4, ♩=90 | intro 1, then a loop of A 8, B 8. Loop 32.0 s. | `ichor`: lyre = harp, kithara = nylon guitar, syrinx = flute, soft strings, sine bass, triangle |
| `MUS_ICHOR_TITAN` (616) | B Greek Mixolydian (church Locrian), centre moves to E in B, 9/8 aksak 3+2+2+2, ♩=162 | intro 2, then a loop of A 8, A2 8, B 8, C 8. Loop 53.3 s. | `ichor`: salpinx = trumpet doubled by a square, horns, chorus, tuba and wave-bass riff, strings ostinato, timpani, square arpeggio, taiko and snare |
| `MUS_ICHOR_BATTLE_TRAINER` (617) | A Greek Phrygian (church Dorian), chromatic genus in B and C, 7/8 kalamatianos 3+2+2, ♩=180 | intro 2, then a loop of A 8, A2 8, B 8, C 8, A3 8. Loop 46.7 s. | `ichor`: aulos = oboe doubled by a square, second aulos = accordion, syrinx, salpinx, kithara, strings ostinato, wave bass, frame drum and taiko, shaker |
| `MUS_ICHOR_BATTLE_WILD` (618) | C Hypodorian (Aeolian), chromatic genus C–A–A♭–G throughout, 5/8 2+3, ♩=180 | intro 2, then a loop of A 8, A2 8, B 8, B2 8, C 8, A3 8. Loop 40.0 s. | `ichor`: syrinx = flute (Pan's pipes), aulos = oboe, kithara, string stabs, wave bass, square, frame drum and krotala, shaker |
| `MUS_ICHOR_VICTORY_TRAINER` (619) | D Greek Lydian (Ionian), C♮ (♭VII) in the fanfare and B, 4/4, ♩=144 | fanfare 3, then a loop of A 8, B 8. Loop 26.7 s. | `ichor`: salpinx fanfare with horn, square and timpani roll, harp sweep; then syrinx, lyre, kithara, sine bass, frame drum and krotala |
| `MUS_ICHOR_AGORA` (625) | D Hypophrygian (Mixolydian), 2/4 ballos, ♩=144 | intro 1, then a loop of A 16, B 16, A2 16. Loop 40.0 s. | aulos tune, syrinx answer, both in thirds in A2; kithara off-beats, sine bass, frame drum and krotala |
| `MUS_ICHOR_AKADEMIA` (626) | G Hypolydian (Lydian), 4/4, ♩=100 | intro 1, then a loop of A 8, B 8. Loop 38.4 s. | lyre tune, syrinx in B, kithara in open fifths, pizzicato bass, triangle |
| `MUS_ICHOR_ENCOUNTER_RIVAL` (620) | E Greek Dorian (Phrygian), 9/8 2+2+2+3, ♩=160 | intro 1, loop 8. Loop 13.5 s. | aulos with a square (Kleon's battle motif), kithara, wave bass, frame drum |
| `MUS_ICHOR_ENCOUNTER_TITAN` (621) | B Greek Mixolydian (Locrian), 9/8 3+2+2+2, ♩=144 | intro 1, loop 8. Loop 15.0 s. | the Titan battle's tritone call, tuba and wave-bass riff, strings, war drums |
| `MUS_ICHOR_OBTAIN_KEY_ITEM` (622) | C Greek Lydian, 3/4, ♩=150 | 2 bars, 2.40 s (144 frames; sFanfares 160, the item fanfare's pacing) | salpinx call, horns, lyre, timpani |
| `MUS_ICHOR_OBTAIN_MON` (623) | F Greek Lydian, 4/4, ♩=132 | 2 bars, 3.64 s (218 frames; sFanfares 230) | syrinx call with the aulos a third under, lyre, frame drum |
| `MUS_ICHOR_NEW_GAME` (624) | B♭ Greek Lydian, 4/4, ♩=96 | intro 1, then a loop of A 8, B 8. Loop 40.0 s. | syrinx, lyre, kithara, strings, sine bass, triangle |
| `mus_ichor_title` (in `MUS_TITLE`) | D Greek Phrygian (Dorian, Elaia's home mode), 4/4, ♩=112 | one-shot: intro 4, A 8, B 8, C 8, coda 4 (68.6 s); the title then returns to the intro, as in Emerald | chorus and aulos theme, salpinx and horns, lyre thread, kithara, strings, timpani, drums |
| `mus_ichor_intro` (in `MUS_INTRO`) | D Greek Phrygian, 4/4, ♩=140 | one-shot: A 10, B 10, C 3 (39.4 s), cut to the scene timers in `src/intro.c` | lyre thread and rising chorus; the title theme at a gallop; salpinx and horns |
| `mus_ichor_victory_wild`, `_laurel`, `_titan` | G Greek Lydian 4/4 ♩=144; F Greek Lydian 4/4 ♩=144 (E♭ fanfare); B Mixolydian fanfare into E Greek Lydian 4/4 ♩=144 | loops 13.3 s, 40.0 s, 13.3 s | syrinx and lyre; salpinx, syrinx and chorus processional; the Titan call turned into the dominant of E |
| `mus_ichor_caught`, `_evolution` | C Greek Lydian 6/8 ♩=144; D Hypodorian (Aeolian) with E♭, 4/4 ♩=120 | loops 15.0 s, 16.0 s | syrinx and lyre in thirds; harp ostinato under a chorus climbing a step a bar |
| `mus_ichor_encounter_male`, `_female`, `_intense`, `_suspicious`, `_hiker` | C Hypophrygian 4/4 ♩=144; B♭ Hypolydian 3/4 ♩=120; A Greek Dorian 2/4 pyrrhic ♩=160; D chromatic genus 4/4 ♩=120; A Hypophrygian 6/8 ♩=144 | loops 13.3, 12.0, 12.0, 16.0, 15.0 s | aulos hasapiko; syrinx over harp; salpinx and war drums; pizzicato, aulos and ison drone; syrinx over a tsabouna drone with goat bells |
| fanfares in `MUS_LEVEL_UP`, `_OBTAIN_ITEM`, `_OBTAIN_TMHM`, `_HEAL`, `_OBTAIN_BADGE`, `_EVOLVED`, `_EVOLUTION_INTRO` | D Hypolydian; G, D, A Greek Lydian; A Greek Phrygian; F Hypolydian; C (fifths) | 1.20, 2.40, 3.20, 2.40, 5.45, 3.64, 1.00 s, each inside its vanilla sFanfares duration | built on the slice's call, 5-1-2-3 |
| `MUS_ICHOR_ELPIS_LULLABY` (627) | D Dorian (Greek Phrygian), 3/4, ♩=72 | intro 1, then a loop of A 8, A2 8. Loop 40.0 s. | hum (53) over the lyre rocking the cradle; the father's lyre in A2 with the hum a third under; strings, sine bass. Each verse stops on the half cadence. |
| `MUS_ICHOR_ELPIS_LULLABY_BOX` (628) | D Dorian, 3/4, ♩=60 | intro 1 (ticks), then a loop of A 8. Loop 24.0 s. | music box (10, the comb and its lower teeth), the escapement's tick (115) once a second. Bar 8 is the tick alone. |
| `MUS_ICHOR_TRIREME` (629) | G Dorian (Greek Phrygian), 6/8, ♩=100, a rowing stroke a bar | intro 2, then a loop of A 8, A2 8, B 8, C 8. Loop 57.6 s. | syrinx sea tune, aulos in thirds and the trieraules's stroke call, rowers' chorus, square glint, kithara swell, sine bass, frame drum, sea wind (122) |
| `MUS_ICHOR_ROAD` (630) | F Mixolydian (Greek Hypophrygian), 3/4 tsamikos 3+1+2, ♩=120 | intro 2, then a loop of A 8, A2 8, B 8, C 8, A3 8. Loop 60.0 s. | aulos lead, horn echoes, syrinx in B, a distant salpinx Thread call and string drone in C, kithara, sine bass, square, frame drum, shaker |
| `MUS_ICHOR_ROAD_NIGHT` (631) | F Dorian, 3/4, ♩=90 | intro 1, then a loop of A 8, B 8, A2 8. Loop 48.0 s. | the road's tune with A flattened: syrinx, aulos in B, a far horn, lyre, sine bass, soft drum, crickets (127) |
| `MUS_ICHOR_EMPORION` (632) | B♭ Greek Lydian (Ionian), D Hijaz in B, 4/4 3+3+2, ♩=120 | intro 2 (fanfare), then a loop of A 8, A2 8, B 8, C 8. Loop 64.0 s. | aulos market tune, syrinx descant, horn stabs, an eastern-quarter aulos over maqsum, then strings, horns, salpinx and timpani for the harbor; kithara, sine bass, frame drum, shaker |
| `MUS_ICHOR_TEMPLE_HERMES` (633) | D Hypolydian (Lydian), D Mixolydian in B, 6/8, ♩=180 | intro 1, then a loop of A 8, A2 8, B 8, C 8, A3 8. Loop 40.0 s. | syrinx and lyre trading the tune, staccato aulos in B, the race as a hocket in C, pizzicato, square ostinato, krotala, taiko |
| `MUS_ICHOR_ELEUSA` (634) | A Greek Lydian (Ionian), A Mixolydian in B, 2/4 syrtos 2+1+1, ♩=100 | intro 2, then a loop of A 16, B 16, A2 16. Loop 57.6 s. | syrinx tune, aulos with Demeter's motif in major; a reaping song in B (aulos call, chorus answer, tsabouna drone, krotala); lyre, kithara, sine bass, frame drum |
| `MUS_ICHOR_TEMPLE_DEMETER` (635) | A Greek Dorian (Phrygian), 4/4, ♩=72 | intro 2, then a loop of A 8, B 8, A2 8. Loop 80.0 s. | mystai's hymn (chorus), Demeter's grief motif on the aulos, lyre, a low A pedal, bell (intro), heartbeat frame drum, torch embers. A2 ends on A major. |
| `MUS_ICHOR_BATTLE_ADMIN` (636) | E Greek Mixolydian (Locrian), centre on A in B, 7/8 2+2+3, ♩=168 | intro 2, then a loop of A 8, A2 8, B 8, C 8, A3 8. Loop 50.0 s. | the Sickle on the salpinx with a square, horns in thirds, chorus chant, strings ostinato, tuba and wave-bass grind, timpani, war drums; a tenth track left free for each admin's layer |
| `MUS_ICHOR_REVELATION` (637) | D Dorian, D Lydian in B, 4/4, ♩=72 | intro 2, then a loop of A 8, B 8. Loop 53.3 s. | one sustained aulos D; the lyre's broken Thread; Daphne's Question on the syrinx, joined by the lyre in tenths; strings, sine bass, triangle stars |
| `MUS_ICHOR_HOLLOW` (638) | E Hypodorian (Aeolian), chromatic genus in B, 4/4, ♩=96 | intro 1, then a loop of A 8, B 8, A2 8. Loop 60.0 s. | low aulos with a syrinx echo, harp drips, pizzicato walk, sine ison, soft frame drum; Hecate's chromatic syrinx in B |

The Greek octave species carry different names from the church modes on the same notes. `songs.py` maps them, and the table gives both for the newer songs.

The songs from 613 on share the `ichor` voicegroup (`sound/voicegroups/ichor.inc`), so the score has one palette. Act I added four slots:
- 10, the music box (the glockenspiel), kept for Elpis's box alone;
- 53, the hum (a single voice);
- 115, the box's tick, on the noise channel;
- 122, sea wind, on the noise channel.

Its slots are GM-numbered, so the `.mid` files also sound right in a DAW. Its drums come from Emerald drumset 1:
- Indian drum and congas = frame drum
- hyoushigi = krotala
- atarigane = kymbala
- ohtsuzumi, triangle and taiko are also available.

- **Elaia.**
  - A: the lyre tune over rolling kithara arpeggios.
  - A2: the aulos adds a slow counter-line.
  - B: the aulos takes the tune through F, C and G. G major is the Dorian colour.
  - C: a four-bar festival dance in which lyre and aulos trade calls.
  - A3: everything together. The last bar turns from Dm to G, a plagal Dorian cadence, back to the top.
- **Route 1.**
  - The guitar plays the laouto "boom-chick-chick" on 1, 4 and 6, and the drum plays dum-tek-tek.
  - A: the hook is a sequence on G, F and C. F major (♭VII) is the Mixolydian colour.
  - A2: the accordion doubles the hook a third below.
  - B: the accordion tune, with harp arpeggios.
  - C: salpinx fanfares answered by the flute, over taiko.
  - A3: tutti. It cadences F to G and loops.
- **Rival battle.**
  - A and A2: the oboe tune leans on the F–E semitone over a string ostinato. A2 adds horn stabs and ends on E major.
  - B: the trumpet in A minor, falling through the Hijaz tetrachord (A–G♯–F–E).
  - C: long wailing aulos notes over taiko. It closes with F to Em (♭II–i) and drops straight back into the loop.
- **Akti.**
  - A: the syrinx hook walks down in sequence (G–E, F–D, E–C) over the kithara's syrtos strum.
  - A2: the aulos doubles the hook in parallel thirds, island-band style.
  - B: B♭ replaces B (the synemmenon tetrachord). The harbor turns toward F for eight bars, with lyre arpeggios and flute gull calls.
  - C: the quay festival. The pipes trade calls over krotala, and the last bar (G) falls back to the opening C.
- **Temple of Hestia.**
  - A: the chorus sings Elaia's opening lyre motif, recast in Greek Dorian (A–D–E♭–F), since the hearth is the home's heart.
  - The frame drum keeps a hearth pulse on 1 and 4 throughout.
  - B: the aulos falls through the chromatic genus (G–E–E♭–D) over a slow chorus descant and noise-channel embers.
  - A2: the aulos takes the hymn while the chorus sings under it. Each phrase closes E♭→Dm.
- **Asclepeion.**
  - A: the lyre tune (Apollo's healing instrument) leans on the raised fourth over the G major chord.
  - B: the syrinx answers over soft strings and harp, and ends with E rising to the loop's F.
- **Team Titan.**
  - A: the salpinx opens with a tritone leap (B–F) over a tuba and bass riff grinding B–C.
  - A2: horns double the salpinx an octave down.
  - B: horn calls centred on E, answered by trumpets.
  - C: the Titans' chant, with chorus and horns in long tones over pounding taiko. It ends on B, where the loop restarts.
- **Trainer battle.**
  - A: the aulos kalamatianos tune, Dorian F♯ in the D major chord.
  - B: an E drone (the Byzantine ison) with the salpinx climbing and falling through E–F–F♯–A.
  - C: syrinx and aulos run in thirds.
  - A3: a second pipe (accordion) joins a third below, as on a real double aulos. The loop closes G→Am.
- **Wild battle.**
  - A: Pan's syrinx runs a sequence down C, B♭, A♭, G, ending each phrase on the chromatic C–A–A♭–G.
  - B: the aulos leads, and B2 adds a flute descant.
  - C: a hocket between the pipes over krotala and string stabs. Every section ends on G, which the loop's C answers.
- **Trainer victory.**
  - The fanfare: D, then a lift through C major (♭VII), then a held D with a harp sweep and a timpani roll.
  - The loop is a hasapiko-like dance for the syrinx. In B the trumpet answers over lyre arpeggios, and the loop ends A→D.
