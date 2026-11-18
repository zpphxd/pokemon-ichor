#!/usr/bin/env bash
# The Nursery of Nysa and the Great Deigma, played from a Quickstart:
# leave two Pokémon, see them roam the glade, find Eggs (Hera doubles the
# chance), take the Egg and a Pokémon back; buy from the stalls, see the
# curio stall hold its stock for a day and change it the next, sell coins.
#
#   tools/ichor/tests/nysa_deigma.sh [rom]     (default: pokeemerald.gba)
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_nysa_deigma
# Hera's hooks in the day care (design/SYSTEMS.md §3, Queen's Care)
grep -q "Ichor_ModifyEggChance" src/daycare.c && grep -q "Ichor_ExtraEggCycles" src/daycare.c \
  || { echo "NYSA FAIL: Hera's day-care hooks are gone from src/daycare.c"; exit 1; }
engine_prepare NYSA "$OUT" tools/ichor/tests/nysa_deigma_consts.c tools/ichor/tests/nysa_deigma_setup.s
{
  echo "return {"
  arm-none-eabi-nm "${ROM%.gba}.elf" | awk '$3 ~ /^(CB2_PokeStorage|gPlayerPartyCount)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "  SCRIPTS = {"
  arm-none-eabi-nm "${ROM%.gba}.elf" | awk '$3 ~ /^Route7_[A-Za-z0-9_]*_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ { print "    " $3 " = 0x" $1 "," }'
  echo "  },"
  echo "}"
} > "$OUT/extra_symbols.lua"
engine_run NYSA "$OUT" tools/ichor/tests/nysa_deigma.lua 200000 900
