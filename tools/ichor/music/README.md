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

`preview.py` patches a copy of the ROM so the title screen plays the song, then records the mGBA mix. It prints loudness next to three Emerald reference songs. It also scores how closely the second pass of the loop matches the first.

## Auditioning in-game

The songs are in the debug menu's sound test. This needs a non-release build, which is the default.
1. In the overworld, hold **R** and press **START**. Choose **Sound… → Music…**.
2. Press **→** twice to move the cursor to the hundreds digit, then press **↑** three times. The list stops at its last song, 612 `MUS_ICHOR_BATTLE_RIVAL`.
3. Press **←** twice to return to the ones digit. Press **↓** for 611 `MUS_ICHOR_ROUTE1`, then again for 610 `MUS_ICHOR_ELAIA`.
4. **A** plays, **START** stops, **B** leaves the menu with the song still playing.

## The pieces

| Song | Mode, meter, tempo | Form (bars) | Voices (voicegroup) |
|---|---|---|---|
| `MUS_ICHOR_ELAIA` (610) | D Dorian, 6/8, ♩=100 | intro 2, then a loop of A 8, A2 8, B 8, C 4, A3 8. Loop 64.8 s. | `rg_credits`: lyre = harp, kithara = low harp arpeggios, aulos = oboe, string pad, sine-wave bass, frame drum (Indian drum dum, conga tek, tambourine) |
| `MUS_ICHOR_ROUTE1` (611) | G Mixolydian, 7/8 kalamatianos 3+2+2, ♩=150 | intro 2, then a loop of A 8, A2 8, B 8, C 8, A3 8. Loop 56.0 s. | `rg_sevii_route`: syrinx = flute, aulos = accordion, salpinx = trumpet, kithara = nylon guitar, lyre = harp, wave bass, square, conga and taiko drums, noise shaker |
| `MUS_ICHOR_BATTLE_RIVAL` (612) | E Phrygian with a Phrygian-dominant E chord (G♯) in B, 9/8 aksak 2+2+2+3, ♩=180 | intro 2, then a loop of A 8, A2 8, B 8, C 8. Loop 48.0 s. | `rg_credits`: aulos = oboe doubled by a square, strings ostinato, salpinx = trumpet, horn stabs, wave bass, square arpeggio, kit with taiko and congas |

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
