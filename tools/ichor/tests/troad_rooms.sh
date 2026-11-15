#!/usr/bin/env bash
# The Troad's rooms check: every interior of Sestos and Ilion, in game.
#
#   tools/ichor/tests/troad_rooms.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Quickstarts a new game, gives a Pelipper, a Mewtwo and three dye berries, sets
# the Gate Emblem and the chisel's find (as Hektor's hall and the Walls of
# Laomedon will), then warps into each room through its door mat and plays it:
#   - the door mat is warp 0, and sends to its town's warp with the room's number;
#   - every household is talked to; every gift is taken once, and a second talk
#     gives nothing more; both trades are done (Kymon's, Idaios's);
#   - Hero's windy stair: a draught puts the flame out, the next climb lights the
#     lamp; Odysseus's Xenion and his battle, then Odysseus at the temple.
# Output, with a screenshot of every room and message, in build/test_troad_rooms/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_troad_rooms
engine_prepare TROAD "$OUT" tools/ichor/tests/troad_rooms_consts.c tools/ichor/tests/troad_rooms_setup.s

# The rooms' scripts by name (slice_symbols.sh knows only the slice's), and the
# few engine addresses this check needs besides engine_build.sh's.
{
  echo "return {"
  echo "  SCRIPTS = {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Sestos|Ilion)_[A-Za-z0-9]+_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ { print "    " $3 " = 0x" $1 "," }'
  echo "  },"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(CB2_PokeStorage|sHoursOverride)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/troad_symbols.lua"

engine_run TROAD "$OUT" tools/ichor/tests/troad_rooms.lua 400000 1500
