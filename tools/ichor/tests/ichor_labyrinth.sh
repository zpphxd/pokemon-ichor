#!/usr/bin/env bash
# The Labyrinth's engine check (design/LABYRINTH.md §5), in game.
#
#   tools/ichor/tests/ichor_labyrinth.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Route 1 stands in for a ring: Ariadne's Thread laid, wound, tied off, wound
# in, warned low, redrawn after a map load and followed back (RETURN TO); the
# Helm of Darkness against a trainer in the dark and in light; Asterion seeing,
# charging, breaking a cracked wall, knocking the player down, listening,
# missing a helmed player and resting; a dial turned with the Labrys.
# Output in build/test_ichor_labyrinth/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_ichor_labyrinth
engine_prepare LABYRINTH "$OUT" tools/ichor/tests/ichor_labyrinth_consts.c tools/ichor/tests/ichor_labyrinth_setup.s
engine_run LABYRINTH "$OUT" tools/ichor/tests/ichor_labyrinth.lua 120000 1200
