#!/usr/bin/env bash
# Knossa above ground, played through (design/phase4/SCRIPT.md III-3A to III-4):
#
#   tools/ichor/tests/knossa.sh [rom]     (default: pokeemerald.gba; run make first)
#
# From Kythera's departure to boarding for Gytheion; the Labyrinth's two hand-offs
# (out through the threshold at night, the Icarus Shaft at dawn) are stood in for
# by test headers. Output in build/test_knossa/.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_knossa
engine_prepare KNOSSA "$OUT" tools/ichor/tests/knossa_consts.c tools/ichor/tests/knossa_setup.s
{
    echo "return {"
    arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Knossa|KytheraSkandeia).*EventScript_|^BerryTreeScript$/ { print "  " $3 " = 0x" $1 "," }'
    echo "}"
} > "$OUT/knossa_scripts.lua"
engine_run KNOSSA "$OUT" tools/ichor/tests/knossa.lua 300000 2000
