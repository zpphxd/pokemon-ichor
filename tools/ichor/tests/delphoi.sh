#!/usr/bin/env bash
# Delphoi's chapter, walked: Kirrha to the Sacred Olives (III-6A), the gorge's
# muster and both falls (III-6B), the Pythia passing (III-6C), the Pythian Light
# and Laurel 8 (III-6D), Mom at the spring (III-7), the Omphalos at night (III-8)
# and the stair down toward the Loom. Assisted (a level-100 lead).
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_delphoi
engine_prepare DELPHOI "$OUT" tools/ichor/tests/delphoi_consts.c tools/ichor/tests/delphoi_setup.s
{
    echo "return {"
    arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Delphoi|Route28).*EventScript_/ { print "  " $3 " = 0x" $1 "," }'
    echo "}"
} > "$OUT/delphoi_scripts.lua"
engine_run DELPHOI "$OUT" tools/ichor/tests/delphoi.lua 400000 1800
