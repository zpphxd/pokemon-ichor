#!/usr/bin/env bash
# Egypt's rooms check: Naukratis's and Memphis's twelve interiors
# (tools/ichor/maps/egypt_rooms.py, design/oikoumene/ROOMS_egypt.md).
#
#   tools/ichor/tests/egypt_rooms.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Quickstarts a new game, gives a party (two Pidgey, a Smeargle, a Machamp) and
# a Helix Fossil (egypt_rooms_setup.s, assembled into spare EWRAM), then walks
# into every room by its door mat and plays it with key presses:
#   - each room's door mat (warp 0) leads to its town's warp with the room's
#     number (MAP_NAUKRATIS 0-6, MAP_MEMPHIS 0-4), read from the map header;
#   - every person is talked to and every sign read;
#   - each gift is taken once, and only once: Ipy's Super Rod, Merit's linen,
#     Khay's Reaper Cloth, Amenemope's Twisted Spoon after his riddles;
#   - Lykos's trade (the Smeargle for POIKILOS the Kecleon);
#   - Daphne wakes the Helix Fossil, and rates the Pokédex;
#   - two Pokémon go into the egg-ovens and the day care holds them both;
#   - the Apis puzzle: a wrong bull, then the true one, and the Tauros given.
# Screenshots land in build/test_egypt_rooms/shots/; the run fails on any
# failed check, a crash or a timeout. It never warps to a town (their door
# warps are another agent's) and never takes a door mat.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_egypt_rooms
engine_prepare EGYPT "$OUT" tools/ichor/tests/egypt_rooms_consts.c tools/ichor/tests/egypt_rooms_setup.s
# The rooms' scripts, by name, so the check finds people and signs by what they run.
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Naukratis|Memphis)_[A-Za-z]+_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/egypt_scripts.lua"
engine_run EGYPT "$OUT" tools/ichor/tests/egypt_rooms.lua 300000 1500
