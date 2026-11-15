#!/usr/bin/env bash
# Oikoumene overworld sprites check (batch 1: the Troad, Egypt, the Black Sea).
# Every new walker spawns on Akti from its graphics id, walks a square (left,
# down, right, up) showing its walk frames, and its land's palette loads intact
# into its own OBJ slot, clear of the player's and the follower's.
#
#   tools/ichor/tests/oikoumene_ow_sprites.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Test scripts come from oikoumene_ow_sprites_setup.s, assembled into spare
# EWRAM; nothing in the ROM is patched. Output in build/test_oikoumene_ow/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_oikoumene_ow
engine_prepare OIKOW "$OUT" tools/ichor/tests/oikoumene_ow_sprites_consts.c tools/ichor/tests/oikoumene_ow_sprites_setup.s
# special vars the shared symbol lists leave out
arm-none-eabi-nm "$ELF" | awk 'BEGIN { print "return {" }
  $3 ~ /^gSpecialVar_0x800[48]$/ { print "  " $3 " = 0x" $1 "," }
  END { print "}" }' > "$OUT/oikow_symbols.lua"
engine_run OIKOW "$OUT" tools/ichor/tests/oikoumene_ow_sprites.lua 40000 600
