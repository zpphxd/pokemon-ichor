#!/usr/bin/env bash
# The catch mash (src/ichor_catch.c): real throws from the battle Bag. A mashed
# throw opens the "Tap A!" window, counts presses to the cap and rolls with the
# x1.3 rate; an untouched throw keeps the vanilla rate; a Master Ball skips it.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS gIchorCatchMash gBagPosition Task_BagMenu_HandleInput CB2_BagMenuRun"
OUT=build/test_catch_mash
engine_prepare MASH "$OUT" tools/ichor/tests/catch_mash_consts.c tools/ichor/tests/catch_mash_setup.s
engine_run MASH "$OUT" tools/ichor/tests/catch_mash.lua 40000 300
