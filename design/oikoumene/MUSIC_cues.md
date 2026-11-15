# The Oikoumene's music: batch 1 cue sheet

## Stopped at (2026-11-14, Oikoumene paused)

`make` is green at commit d7993704fa (ROM 22,204,208 B, 66.17%; before the songs, 22,191,564 B). The rest of this file is a draft, with placeholders where the measurements would go.

**Done.**
- Ten songs in `tools/ichor/music/songs_oikoumene.py`, ids 639–648, wired into `songs.h` (with `END_MUS`), `song_table.inc`, `midi.cfg`, `charmap.txt` and the debug sound test. They are on the `ichor` voicegroup and pass `compose.py --check`, with no PSG note in unison with a DirectSound note. Each compiles to 0.5–2.1 KB, 12.7 KB in all.
  - 639 *The Wider World*, D Mixolydian, 6/8
  - 640 *The Plain of Troy*, E Dorian, 4/4 march
  - 641 *The Black Land*, A double harmonic, 2/4 malfuf
  - 642 *The Necropolis*, the same mode, 4/4, slow
  - 643 *The Black Sea*, G Phrygian, 9/8 (3+3+3)
  - 644 *Battle! Oikoumene Trainer*, B Aeolian, 7/8 at 200
  - 645 *Battle! Champion of the Periodos*, D Dorian, 9/8 zeibekiko
  - 646–648 *The Periodos* for the Troad, Egypt and the Black Sea
- `periodos()`: each later hall is one call.
- `tools/ichor/tests/oikoumene_music.*` passed (81 checks) on the first render. It checks every slot, header and voicegroup, that playbgm plays each song at its tempo, that the game keeps running, and that each song is still playing past its loop end.
- The smoke test passed on the first render.

**Partial.** Revision pass 1 is written in the source but not re-rendered:
- levels: five songs were 2–2.9 dB under their references, so -V went to 127, with the PSG tracks scaled back;
- seams: the Periodos gets a home-aulos "turn" into A, and Black Land's A2 gets a pickup;
- meter: the Black Sea's 3+3+3 wasn't felt and has been rewritten on the beats; the Oikoumene battle's B and C drums now sit on 3+2+2; the champion battle has an accented downbeat with a breath before it;
- Wider World B: a string pad was added.

Still to do:
- re-render with `preview.py` and the scratchpad meter analysis;
- revision pass 2;
- fill in sections 1–6;
- re-run the music test and the smoke test.

**Not started.** Choosing the Emerald references for the Black Land, Black Sea and battles (`MUS_ROUTE111` doesn't exist; use `MUS_ROUTE110` or `MUS_DESERT`).

**Open.**
- Song ids 639+ will collide with other branches that append songs (pg-b1-music); the lead renumbers at merge.
- Surfing on the lanes plays `MUS_SURF` over the map's music.
- Champion classes need cases in `GetBattleBGM` (§1, Battles).

- **Owner:** the music agent of world-oikoumene's batch 1 (`design/oikoumene/BUILD.md` §5).
- **What this is:** the songs batch 1 adds, the maps each one belongs to (so the lead can swap the map agents' stand-ins), how they were checked, and what changed in each revision pass.
- **Reads with:** `design/MUSIC.md` (the motifs), `design/OIKOUMENE.md` §7 (the music table), `design/oikoumene/PERIODOS.md` §6 (the hall theme), `tools/ichor/music/README.md` (the pipeline). The notes are in `tools/ichor/music/songs_oikoumene.py`.

## 1. The constants, and the maps they belong to

No `map.json` was touched. The map agents set stand-ins (`MUS_ICHOR_AKTI`, `_EMPORION`, `_TRIREME`, `_ROAD`); swap them for these.

PLACEHOLDER_TABLE

**Interiors.** Houses take their town's track, as the slice's do (Akti's houses play `MUS_ICHOR_AKTI`). Asclepeia keep `MUS_ICHOR_ASCLEPEION`, Agoras `MUS_ICHOR_AGORA`, and Ilion's temple of Athena keeps `MUS_ICHOR_TEMPLE` (Hestia's hymn) until a temple cue of its own exists.

**Night.** *The Necropolis* is paired map by map, with `"night_music": "MUS_ICHOR_NECROPOLIS"` in the outdoor maps' `map.json` (the table above marks them), and not in `sNightMusicTable` the way the road is. The table would also flip every Egyptian house, shop and field station that plays the town's track, and a funeral reed in Daphne's field station at night is wrong. Two engine facts decide this (`src/overworld.c`):
- `GetLocationMusic` takes a map's `night_music` at night, then `GetNightMusicFromTrack` runs `sNightMusicTable` over whatever came out, so a table pairing can't be undone by a map's own field.
- The switch happens on a map change, as with any night music; walking out of a house at night plays the night form.

Later Egyptian maps with a night form (the Pyramid Field, whose night is the Valley of Tombs, BUILD §1) take the same field.

**Battles.** The chart agent's branch in `GetBattleBGM` (`src/pokemon.c`) should return `MUS_ICHOR_BATTLE_OIKOUMENE` for Oikoumene trainers. The champions and Helen need a class case beside it: the champions' titles (PRINCE, KING, PRIESTESS, PRIEST, PHARAOH, HUNTRESS, ATHLETE, JUDGE, and QUEEN for Helen; PERIODOS §7) return `MUS_ICHOR_BATTLE_PERIODOS`. Neither is wired here: `src/pokemon.c` is the chart agent's.

**Victory.** No new jingle. *Battle! Oikoumene Trainer* ends every section on F♯ minor into B minor, and the existing trainer victory (`mus_ichor_victory_trainer`, D major) is B minor's relative major, so the cadence lands. The champions' classes can take the Laurel victory (`MUS_VICTORY_GYM_LEADER`) as the Hierophants do.

## 2. The songs

PLACEHOLDER_SONGS

## 3. The Periodos: how the other seven halls are added

PLACEHOLDER_PERIODOS

## 4. How they were checked

PLACEHOLDER_CHECKS

## 5. Revision passes

PLACEHOLDER_PASSES

## 6. Open questions

PLACEHOLDER_OPEN
