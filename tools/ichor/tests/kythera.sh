#!/usr/bin/env bash
# Connected, assisted chapter check. Starts after Kaldera; does not award Kythera receipts.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_kythera
engine_prepare KYTHERA "$OUT" tools/ichor/tests/kythera_consts.c tools/ichor/tests/kythera_setup.s
{
    echo "return {"
    arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Kythera|Kaldera|TriremeDeck).*EventScript_|^BerryTreeScript$/ { print "  " $3 " = 0x" $1 "," }'
    echo "}"
} > "$OUT/kythera_scripts.lua"
engine_run KYTHERA "$OUT" tools/ichor/tests/kythera.lua 180000 1200
