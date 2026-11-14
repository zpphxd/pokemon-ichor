# Ichor music

The songs are original. Their notes are plain text in `songs.py`, and `compose.py` turns them into `sound/songs/midi/mus_ichor_*.mid`. `make` then converts those with `mid2agb`, using the flags in `midi.cfg`. The `.mid` files are committed and reproducible.

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

It also warns when a loop isn't a whole number of frames. m4a advances `tempo / 150` ticks a frame, so the loop's ticks × 150 ÷ tempo should come out whole. Otherwise each pass starts at a different sub-frame phase, and the passes drift apart slightly in onsets and DirectSound channel steals. Pick a nearby even tempo that divides evenly.

`preview.py` patches a copy of the ROM so the title screen plays the song, then records the mGBA mix. It prints loudness and clipped samples next to three Emerald reference songs. It also compares the second pass of the loop with the first, in two ways:
- **pass match** correlates their envelopes. It reads low on flat, sustained textures such as the temple hymn.
- **worst 1s** is the largest level difference between the passes over any one-second window. A hung or dropped note shows up as several dB, while a clean loop stays near 1 dB.

Name other songs on the command line to render them too, such as `MUS_POKE_CENTER` or `MUS_VS_WILD`.

When you balance volumes, keep the PSG in mind:
- PSG levels are coarse. The wave channel has only four output levels (`gCgb3Vol`: 25, 50, 75 and 100%).
- A small change to `-V` or to a wave track's volume can therefore jump the bass by 6 dB and swamp the tune.
- Re-run `preview.py` after any volume change and compare the result with the reference songs.
- Current levels are within about 1 dB of the Emerald song each one replaces: Littleroot, Route 101, the Pokémon Center, the trainer, wild, rival and Aqua/Magma battles, and the trainer victory.

## Auditioning in-game

The songs are in the debug menu's sound test. This needs a non-release build, which is the default.
1. In the overworld, hold **R** and press **START**. Choose **Sound… → Music…**.
2. Press **→** twice to move the cursor to the hundreds digit, then press **↑** three times. The list stops at its last song, 619 `MUS_ICHOR_VICTORY_TRAINER`.
3. Press **←** twice to return to the ones digit. Each **↓** steps back one song, down to 610 `MUS_ICHOR_ELAIA`.
4. **A** plays, **START** stops, **B** leaves the menu with the song still playing.

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

The Greek octave species carry different names from the church modes on the same notes. `songs.py` maps them, and the table gives both for the newer songs.

The seven songs from 613 on share the `ichor` voicegroup (`sound/voicegroups/ichor.inc`), so the slice has one palette. Its slots are GM-numbered, so the `.mid` files also sound right in a DAW. Its drums come from Emerald drumset 1:
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
