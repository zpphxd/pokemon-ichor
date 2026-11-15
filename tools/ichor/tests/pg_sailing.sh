#!/usr/bin/env bash
# The post-game's sailing layer (design/postgame/ENGINE.md), in game.
#
#   tools/ichor/tests/pg_sailing.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Boards the Euploia at Akti's quay onto her deck, leaves her, puts her to sea in
# Akti's harbor, and checks the ship's graphics, her speed and sail against the
# wind, the strong wind's extra tile, Poseidon's grudge, the encounter rate, the
# Relic Ring's DECK and TAKE HER OUT, SET A COURSE and its crossing, the start
# menu's wind line, the Wings refusing at sea, the Great Bear by night, the daily
# wind, save and reload with the epics, and the shades on Route 1 by night.
# Output in build/pg_sailing/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/pg_sailing
# the clock and the battle the checks read, besides engine_build.sh's
ENGINE_SYMS="$ENGINE_SYMS gTimeOfDay gTimeUpdateCounter gBattleMons gMapHeader gWindows sIchorBlessingWindowId"
engine_prepare PGSAIL "$OUT" tools/ichor/tests/pg_sailing_consts.c tools/ichor/tests/pg_sailing_setup.s
engine_run PGSAIL "$OUT" tools/ichor/tests/pg_sailing.lua 400000 1200
