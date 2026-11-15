#!/usr/bin/env bash
# Trophonios's cave check: plays the optional descent and the reading (SCRIPT.md Part 5,
# beats 35B-35C).
#
#   tools/ichor/tests/act2_trophonios.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts a new game, gives a test team, Act I's Torch and Hammer and one Honey,
# opens the grille (Saon's flag) and warps in through it (act2_trophonios_setup.s,
# assembled into spare EWRAM: nothing in the ROM is patched), then plays both floors
# with key presses: the lit upper chamber, the ladder, brazier 1, Herkyna's goose, the
# chalk hand lit and doused, the Bronze Obol, the rubble and the Max Repel, Philomelos;
# the spring, forks A-C and their pay, the web den, the snake and the honey, Melampos,
# the great boulder with and without Hephaestus's Hammer, brazier 2, the TM, the hole
# and the reading on the throne of Mnemosyne; then back down (the braziers lit, the
# snake gone) and out through the hole to Lebadeia. Screenshots land in
# build/test_act2_trophonios/shots/; the run fails on any failed check, a crash or a
# timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_act2_trophonios
engine_prepare TROPH "$OUT" tools/ichor/tests/act2_trophonios_consts.c tools/ichor/tests/act2_trophonios_setup.s
# The cave's event scripts by name: slice_lib finds people and signs by the script they run.
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^TrophoniosCave_B[12]F_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ { print "  " $3 " = 0x" $1 "," }'
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(EventScript_RockSmash|EventScript_IchorCobweb|EventScript_IchorGreatBoulder|Common_EventScript_FindItem)$/ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/troph_scripts.lua"
engine_run TROPH "$OUT" tools/ichor/tests/act2_trophonios.lua 400000 1800
