# The Oikoumene's music: batch 1 cue sheet

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
