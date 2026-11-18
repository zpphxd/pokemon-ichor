#!/usr/bin/env bash
# Travel herms check (design/SYSTEMS.md §4), in game.
#
#   tools/ichor/tests/town_herms.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Rests at Akti's Asclepeion (registers Akti), touches Emporion's entrance herm
# (registers Emporion), travels Emporion -> Akti and Akti -> Emporion through
# the herms' travel menu, and checks that a town never registered is neither
# offered nor reachable. Output in build/test_town_herms/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_town_herms
engine_prepare TOWNHERMS "$OUT" tools/ichor/tests/town_herms_consts.c tools/ichor/tests/town_herms_setup.s
engine_run TOWNHERMS "$OUT" tools/ichor/tests/town_herms.lua 60000 600
