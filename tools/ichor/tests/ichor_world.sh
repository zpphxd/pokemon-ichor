#!/usr/bin/env bash
# The world's small systems (design/ENGINE_API.md §7), in game.
#
#   tools/ichor/tests/ichor_world.sh [rom]     (default: pokeemerald.gba; run make first)
#
# On Route 1: the xenia rest's menu offers only the hours still ahead, and
# resting until dusk moves the clock to 19:00 and the tint to evening; after
# 20:30 there is no menu. Two knucklebones matches through the menus, the
# second against Mom, on her record. A god in disguise. The party level check.
# The DAY/NIGHT TINT option at 22:00, through a save and CONTINUE. Output in build/test_ichor_world/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_ichor_world
engine_prepare WORLD "$OUT" tools/ichor/tests/ichor_world_consts.c tools/ichor/tests/ichor_world_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(EmporionCity_PhiloxenosHouse_EventScript_Philoxenos|EleusaVillage_HouseOfKeleos_EventScript_Metaneira)$/ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/host_symbols.lua"
engine_run WORLD "$OUT" tools/ichor/tests/ichor_world.lua 140000 900
