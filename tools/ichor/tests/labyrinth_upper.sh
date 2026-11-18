#!/usr/bin/env bash
# The Labyrinth's upper rings (design/LABYRINTH.md, LABYRINTH_MAZE.md): walks
# Ring I's flame relay end to end, with a wrong turn and the thread winding
# back, through to the stair down. Output in build/test_labyrinth_upper/.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_labyrinth_upper
engine_prepare LABUPPER "$OUT" tools/ichor/tests/labyrinth_upper_consts.c tools/ichor/tests/labyrinth_upper_setup.s
{
    echo "return {"
    arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Labyrinth|KnossaPalace_GrandStaircase).*EventScript_/ { print "  " $3 " = 0x" $1 "," }'
    echo "}"
} > "$OUT/labyrinth_scripts.lua"
engine_run LABUPPER "$OUT" tools/ichor/tests/labyrinth_upper.lua 180000 1200
