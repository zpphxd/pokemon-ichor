#!/usr/bin/env bash
# Excavation check (design/SYSTEMS.md §5, design/ENGINE_API.md §8), in game.
#
#   tools/ichor/tests/ichor_dig.sh [rom]     (default: pokeemerald.gba; run make first)
#
# On Route 1: a dig spot without the Trowel; with it, a daily spot's find, the
# spot dug out for the day, and the same find after a reload; fixed finds (an
# item, sherds, a prophecy tablet, a page, an ostrakon), each only once; a
# dig called from another script; a dig-spot object removed by its dig; and
# Hades's blessing doubling a find. Output in build/test_ichor_dig/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_ichor_dig
engine_prepare DIG "$OUT" tools/ichor/tests/ichor_dig_consts.c tools/ichor/tests/ichor_dig_setup.s
engine_run DIG "$OUT" tools/ichor/tests/ichor_dig.lua 80000 600
