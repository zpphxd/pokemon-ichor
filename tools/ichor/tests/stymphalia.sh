#!/usr/bin/env bash
# The road north from Lakonia, walked (tools/ichor/maps/stymphalia.py):
#
#   tools/ichor/tests/stymphalia.sh [rom]     (default: pokeemerald.gba; run make first)
#
# From Lakonia's north road after III-5J, up Route 26 past its checkpoints, across
# Lake Stymphalia (the flock, Akanthis's rest and herm), a save and CONTINUE on the
# causeway, then Route 27 over the hills and into Arkadia. Output in build/test_stymphalia/.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_stymphalia
engine_prepare STYMPHALIA "$OUT" tools/ichor/tests/stymphalia_consts.c tools/ichor/tests/stymphalia_setup.s
{
    echo "return {"
    arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Lakonia|Route26_Skiritis|LakeStymphalia|Route27_ArkadianHills|Arkadia)_EventScript_/ { print "  " $3 " = 0x" $1 "," }'
    echo "}"
} > "$OUT/stymphalia_scripts.lua"
engine_run STYMPHALIA "$OUT" tools/ichor/tests/stymphalia.lua 400000 2000
