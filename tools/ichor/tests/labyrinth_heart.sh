#!/usr/bin/env bash
# The heart (Rings V-VII): walks Ring V to
# the Starry Chamber through the relics, the seal, the dials, the mirrors and the dance.
# Output in build/test_labyrinth_heart/
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_labyrinth_heart
engine_prepare LABHEART "$OUT" tools/ichor/tests/labyrinth_heart_consts.c tools/ichor/tests/labyrinth_heart_setup.s
{
    echo "return {"
    arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Labyrinth|KnossaPalace_GrandStaircase).*EventScript_/ { print "  " $3 " = 0x" $1 "," }'
    echo "}"
} > "$OUT/labyrinth_scripts.lua"
engine_run LABHEART "$OUT" tools/ichor/tests/labyrinth_heart.lua 300000 1200
