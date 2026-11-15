#!/usr/bin/env bash
# The Frozen Hour check (design/phase4/SCRIPT.md Part 11, E1-E6), in game.
#
#   tools/ichor/tests/ichor_frozen.sh [rom]     (default: pokeemerald.gba; run make first)
#
# On Route 1: a person caught mid-stride; the hour entered by loading the map
# with its flag set (gray palettes, the player in color, the flock frozen, the
# music box, no wild battles in tall grass, a trainer who doesn't see you,
# releaseall not thawing anyone); one Kerazap unfrozen with its color running
# back in; a sepia memory; the twelve steps of color back; then the gray
# spreading from a point. Output in build/test_ichor_frozen/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_ichor_frozen
engine_prepare FROZEN "$OUT" tools/ichor/tests/ichor_frozen_consts.c tools/ichor/tests/ichor_frozen_setup.s
engine_run FROZEN "$OUT" tools/ichor/tests/ichor_frozen.lua 90000 900
