#!/usr/bin/env bash
# Kythera's and Melos's trainers (design/phase4/SCRIPT.md Part 3, ids 320-347):
#
#   tools/ichor/tests/act3_trainers.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Reads the expected teams from SCRIPT.md, checks every trainer's entry in
# gTrainers against them, then fights Eudoros, Galatea and the bad guests'
# double battle (from Axylos's house's own scene) with two level-100 Metagross,
# checking each opponent's party as the battle starts. Output in
# build/test_act3_trainers/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_act3_trainers
engine_prepare TRAINERS "$OUT" tools/ichor/tests/act3_trainers_consts.c tools/ichor/tests/act3_trainers_setup.s
arm-none-eabi-nm "$OUT/setup.elf" | awk '$3 ~ /^Act3Trainers_/ { print $3, $1 }' > "$OUT/setup.syms"
# gTrainers isn't among engine_build.sh's symbols: the Lua loads it from here.
GT=$(arm-none-eabi-nm "$ELF" | awk '$3 == "gTrainers" { print $1; exit }')
[ -n "$GT" ] || { echo "TRAINERS FAIL: gTrainers not in $ELF"; exit 1; }
echo "return { gTrainers = 0x$GT }" > "$OUT/trainer_symbols.lua"
engine_run TRAINERS "$OUT" tools/ichor/tests/act3_trainers.lua 60000 600
