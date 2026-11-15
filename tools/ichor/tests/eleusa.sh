#!/usr/bin/env bash
# Eleusa Village and the Temple of Demeter, played with key presses:
#
#   tools/ichor/tests/eleusa.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Quickstarts, gives a level-100 lead, warps to Eleusa's west gate and walks the
# village: talks to every person, reads every sign, picks up every item and
# hidden item, enters every door and comes back out, checks the Ploutonion is shut
# until the sanctum opens, walks through the wheat (the gold rustle, and a wild
# Pokemon from Eleusa's table), then plays the Lesser Mysteries' braziers in the
# dark Telesterion: out of turn, in turn, the pits and the chalk path, Chloe.
# Output in build/test_eleusa/ (screenshots in shots/); see eleusa.lua.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_eleusa
engine_prepare ELEUSA "$OUT" tools/ichor/tests/eleusa_consts.c ""
# Eleusa's scripts by name (slice_symbols.sh lists only the slice's maps), and the
# few addresses the walk reads besides.
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gPartiesCount|sSpritePaletteTags)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "  SCRIPTS = {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^EleusaVillage[A-Za-z0-9_]*_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ { print "    " $3 " = 0x" $1 "," }'
  echo "  },"
  echo "}"
} > "$OUT/eleusa_symbols.lua"
engine_run ELEUSA "$OUT" tools/ichor/tests/eleusa.lua 400000 1500
