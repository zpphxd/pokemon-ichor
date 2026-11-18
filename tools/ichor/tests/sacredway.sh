#!/usr/bin/env bash
# The Sacred Way, walked (tools/ichor/maps/sacredway.py):
#
#   tools/ichor/tests/sacredway.sh [rom]     (default: pokeemerald.gba; run make first)
#
# From Eleusa's east gate after the Moon Laurel over Route 15 (the causeway, the pass,
# the shrine court's drum seal), into Daphni (the healer and its travel herm, the prayer
# laurel and the priestess), a save and CONTINUE on the old save's cell (9,10), then
# Route 16 (the lookout's first sight of the Akropolis) to Astyra's gate.
# Output in build/test_sacredway/.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_sacredway
engine_prepare SACREDWAY "$OUT" tools/ichor/tests/sacredway_consts.c tools/ichor/tests/sacredway_setup.s
{
    echo "return {"
    arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Route15_MysteryRoad|Daphni|Daphni_Sanctuary|Route16_CapitalPass)_EventScript_/ { print "  " $3 " = 0x" $1 "," }'
    echo "}"
} > "$OUT/sacredway_scripts.lua"
engine_run SACREDWAY "$OUT" tools/ichor/tests/sacredway.lua 400000 2000
