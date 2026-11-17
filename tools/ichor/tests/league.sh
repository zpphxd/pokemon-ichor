#!/usr/bin/env bash
# The League (design/LEAGUE.md): with eight Laurels and an assisted team, ride
# the muleteer from Astyra to the Ascent, climb its three floors (the camp's cook
# heals), pass the Propylaia's guard, lose once to Brasidas (the whiteout resets
# the Pantheon), then beat the four seats in order and the Archon, untie Medon's
# Knot, enter the Hall of Heroes, reach the Hall of Fame screen and the credits,
# and CONTINUE into the Elaia epilogue.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_league
engine_prepare LEAGUE "$OUT" tools/ichor/tests/league_consts.c tools/ichor/tests/league_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Ascent_|Olympus_|Astyra_EventScript_Muleteer|ElaiaVillage_PlayersHouse_2F_)[A-Za-z0-9_]*$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/league_symbols.lua"
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(CB2_HallOfFame|CB2_DoHallOfFameScreen|CB2_IchorCredits|CB2_StartIchorCredits|HealPlayerParty)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/league_callbacks.lua"
engine_run LEAGUE "$OUT" tools/ichor/tests/league.lua 900000 3600
