#!/usr/bin/env bash
# Kythera ported from claude/world-act3-4e546d onto main: the voyage from
# Kaldera by Melos to Skandeia, every door of Melos, Skandeia, Paphia, the
# spring and the falls both ways, every land seam both ways, the rooms' gifts,
# and the Temple of Aphrodite through to the Foam Laurel (FLAG_BADGE07_GET),
# on an assisted team. The sea seams (Skandeia to Routes 22 and 23, Route 22 to
# Melos) are map_audit.py's EDGE check's.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_kythera_town
engine_prepare KYTHERATOWN "$OUT" tools/ichor/tests/kythera_town_consts.c tools/ichor/tests/kythera_town_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Kythera|Melos|Kaldera|TriremeEuploia_DeckSouth)[A-Za-z0-9_]*$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/kythera_town_symbols.lua"
engine_run KYTHERATOWN "$OUT" tools/ichor/tests/kythera_town.lua 900000 4500
