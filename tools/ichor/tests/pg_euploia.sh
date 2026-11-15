#!/usr/bin/env bash
# The Euploia refitted (design/ODYSSEY.md §2, §3; design/postgame/BUILD.md batch 1),
# in game.
#
#   tools/ichor/tests/pg_euploia.sh [rom]     (default: pokeemerald.gba; run make first)
#
# With FLAG_ICHOR_POSTGAME and FLAG_ICHOR_GOT_EUPLOIA set: the deck and below deck
# with no crew and with all of them aboard; every service with and without its
# crew member (the hearth, the Pithos, the stall, the nets, Iaso, Phemios), the
# daily flags, the bunk healing and clearing Iaso's flag, Poseidon's altar, the
# hatch and the ladder both ways, the trophy shelf's keepsake scripts.
# Screenshots of both maps. Output in build/test_pg_euploia/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_pg_euploia
engine_prepare EUPLOIA "$OUT" tools/ichor/tests/pg_euploia_consts.c tools/ichor/tests/pg_euploia_setup.s
# the ship's own scripts, by name, for L.npc and L.sign
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^Euploia(Deck|Below)_EventScript_[A-Za-z0-9_]+$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/euploia_scripts.lua"
engine_run EUPLOIA "$OUT" tools/ichor/tests/pg_euploia.lua 120000 900
