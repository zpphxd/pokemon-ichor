#!/usr/bin/env bash
# The never-full Bag (src/item.c, Ichor_AddBagOrPithosItem): with a pocket full,
# an item ball, a gift, a hidden item and a shop purchase land in the Pithos and
# say so; only a full Pithos as well refuses. Output in build/test_bag_overflow/.
#
#   tools/ichor/tests/bag_overflow.sh [rom]     (default: pokeemerald.gba; run make first)
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_bag_overflow
engine_prepare BAG "$OUT" tools/ichor/tests/bag_overflow_consts.c tools/ichor/tests/bag_overflow_setup.s
engine_run BAG "$OUT" tools/ichor/tests/bag_overflow.lua 40000 600
