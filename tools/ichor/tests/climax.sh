#!/usr/bin/env bash
# The climax, played through (design/phase4/SCRIPT.md III-9 to III-12):
#
#   tools/ichor/tests/climax.sh [rom]     (default: pokeemerald.gba; run make first)
#
# From the Omphalos stair into the Loom to the League's L-1 in Astyra. Output and
# screenshots in build/test_climax/.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_climax
engine_prepare CLIMAX "$OUT" tools/ichor/tests/climax_consts.c tools/ichor/tests/climax_setup.s
{
    echo "return {"
    arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(TheLoom|StairOfHours|Climax|Kaldera_TelchinesForge|Arkadia|Astyra|ElaiaVillage).*EventScript_/ { print "  " $3 " = 0x" $1 "," }'
    echo "}"
} > "$OUT/climax_scripts.lua"
engine_run CLIMAX "$OUT" tools/ichor/tests/climax.lua 400000 2400
