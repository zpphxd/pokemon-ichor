#!/usr/bin/env bash
# The Oikoumene's batch-1 music (design/oikoumene/MUSIC_cues.md), in game.
#
#   tools/ichor/tests/oikoumene_music.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Each new song's slot and header; playbgm plays it, it keeps time, the game runs
# on, and it is still playing past the end of its first loop. Output in
# build/test_oikoumene_music/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_oikoumene_music
engine_prepare MUSIC "$OUT" tools/ichor/tests/oikoumene_music_consts.c tools/ichor/tests/oikoumene_music_setup.s

# A symbol engine_build.sh doesn't export, and each song's length from its source.
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 == "voicegroup_ichor" && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/music_symbols.lua"
python3 - "$OUT/song_lengths.lua" <<'EOF' || { echo "MUSIC FAIL: could not read the songs"; exit 1; }
import sys
sys.path.insert(0, 'tools/ichor/music')
import songs  # noqa: F401  (songs.py imports songs_oikoumene at its end)
from songs_oikoumene import OIKOUMENE_SONGS
with open(sys.argv[1], 'w') as f:
    f.write('return {\n')
    for s in OIKOUMENE_SONGS:
        f.write(f'  {s.song_id} = {{ ticks = {s.section_starts()[1]}, tempo = {s.tempo} }},\n')
    f.write('}\n')
EOF
engine_run MUSIC "$OUT" tools/ichor/tests/oikoumene_music.lua 45000 900
