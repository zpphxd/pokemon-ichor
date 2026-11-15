#!/usr/bin/env bash
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_difficulty
engine_prepare DIFFICULTY "$OUT" tools/ichor/tests/difficulty_consts.c tools/ichor/tests/difficulty_setup.s
arm-none-eabi-nm "$ELF" | awk '$3 == "gTrainers" { print "return { gTrainers = 0x" $1 " }"; exit }' > "$OUT/trainers.lua"
engine_run DIFFICULTY "$OUT" tools/ichor/tests/difficulty.lua 60000 240
