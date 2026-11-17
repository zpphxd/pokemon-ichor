#!/usr/bin/env bash
# The bull-leap timing special (engine need E7, src/ichor_bull_leap.c):
#
#   tools/ichor/tests/ichor_bull_leap.sh [rom]     (default: pokeemerald.gba; run make first)
#
# In the Akti Agora, a bull (an object rebuilt from the map's first template,
# act3_lib.lua; nothing in the ROM is patched) charges nine tiles at the player
# while the check presses A at fixed frames of the special, and checks
# VAR_RESULT for early, clean and late. Output in build/test_ichor_bull_leap/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_ichor_bull_leap
engine_prepare LEAP "$OUT" tools/ichor/tests/act3_consts.c tools/ichor/tests/act3_setup.s
arm-none-eabi-nm "$OUT/setup.elf" | awk '$3 ~ /^Act3Test_/ { print $3, $1 }' > "$OUT/setup.syms"
engine_run LEAP "$OUT" tools/ichor/tests/ichor_bull_leap.lua 40000 600
