#!/usr/bin/env bash
# Native statue/mirror behavior for Galatea's Gallery; no player save is used.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_ichor_statues
engine_prepare STATUES "$OUT" tools/ichor/tests/statues_consts.c tools/ichor/tests/statues_setup.s
arm-none-eabi-nm "$OUT/setup.elf" | awk '$3 ~ /^Act3Test_/ { print $3, $1 }' > "$OUT/setup.syms"
engine_run STATUES "$OUT" tools/ichor/tests/ichor_statues.lua 40000 600
