#!/usr/bin/env bash
# Relics check: the key items that replace HMs (design/SYSTEMS.md §1, §2).
#
#   tools/ichor/tests/ichor_relics.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Every obstacle with and without its relic, the AUTO option, forbidden places,
# darkness and the Torch, the Relic Ring, the Wings' fly map, Surf, Waterfall
# and Dive, Aeolus's Bag, the bag and the option row. Test scripts come from
# ichor_relics_setup.s, assembled into spare EWRAM; the arena is built in RAM
# on Route 1. Output in build/test_ichor_relics/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_ichor_relics
engine_prepare RELICS "$OUT" tools/ichor/tests/ichor_relics_consts.c tools/ichor/tests/ichor_relics_setup.s
engine_run RELICS "$OUT" tools/ichor/tests/ichor_relics.lua 120000 900
