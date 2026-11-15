#!/usr/bin/env bash
# The Black Sea's rooms check: Salmydessos's two and Aia's five (batch 1).
#
#   tools/ichor/tests/pontos_rooms.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Quickstarts, gives a Pidgeot, a Liepard and a Rotom, warps into each room by its
# door mat and plays it with key presses: every person and readable thing,
# Phineus's dove and Argos's Heat Rock taken once, Ixos's and Byssa's trades, the
# healer, the stall and the Pithos, the Rotom through all five works of the
# palace workshop and back out, and each room's mat back to its town's warp.
# Test scripts come from pontos_rooms_setup.s, assembled into spare EWRAM.
# Output in build/test_pontos_rooms/ (screenshots in shots/).
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_pontos_rooms
engine_prepare PONTOS "$OUT" tools/ichor/tests/pontos_rooms_consts.c tools/ichor/tests/pontos_rooms_setup.s
# the rooms' scripts by name (slice_symbols.sh lists only the slice's), and the
# two screens the trades and the works open
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(CB2_PokeStorage|CB2_UpdatePartyMenu)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "  SCRIPTS = {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Salmydessos|Aia)_[A-Za-z]+_EventScript_[A-Za-z0-9_]+$/ && !seen[$3]++ { print "    " $3 " = 0x" $1 "," }'
  echo "  },"
  echo "}"
} > "$OUT/pontos_scripts.lua"
engine_run PONTOS "$OUT" tools/ichor/tests/pontos_rooms.lua 200000 1500
