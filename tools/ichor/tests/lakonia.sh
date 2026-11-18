#!/usr/bin/env bash
# Lakonia's chapter, played through (design/phase4/SCRIPT.md III-5A to III-5J):
#
#   tools/ichor/tests/lakonia.sh [rom]     (default: pokeemerald.gba; run make first)
#
# From boarding at Amnisos for Gytheion (Knossa's hand-off) to the goat paths
# on Lakonia's north road. Output in build/test_lakonia/.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_lakonia
engine_prepare LAKONIA "$OUT" tools/ichor/tests/lakonia_consts.c tools/ichor/tests/lakonia_setup.s
{
    echo "return {"
    arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Gytheion|Route25|Lakonia|TriremeDeck).*EventScript_|^BerryTreeScript$/ { print "  " $3 " = 0x" $1 "," }'
    echo "}"
} > "$OUT/lakonia_scripts.lua"
engine_run LAKONIA "$OUT" tools/ichor/tests/lakonia.lua 400000 2000
