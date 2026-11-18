#!/usr/bin/env bash
# Travel herms check (design/SYSTEMS.md §4), in game.
#
#   tools/ichor/tests/town_herms.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Rests at Akti's Asclepeion (registers Akti), touches Emporion's entrance herm
# (registers Emporion), and marks Elaia and Eleusa known. Then, on the herms'
# travel map (the region map): only registered herms other than this town's are
# lit, and the cursor snaps between those and no others. It steers to Akti and
# travels there, landing on Akti's herm tile; B on Akti's map stays put; and it
# travels back to Emporion. A town never registered (Thyrsa) is neither lit,
# reachable, nor accepted by Ichor_TravelToTownHerm. Screenshots of the map are
# in build/test_town_herms/shots/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_town_herms
engine_prepare TOWNHERMS "$OUT" tools/ichor/tests/town_herms_consts.c tools/ichor/tests/town_herms_setup.s
engine_run TOWNHERMS "$OUT" tools/ichor/tests/town_herms.lua 60000 600
