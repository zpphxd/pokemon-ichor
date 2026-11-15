#!/usr/bin/env bash
# The Three-Act Play check: plays the Temple of Dionysus from the door to the Mask Laurel.
#
#   tools/ichor/tests/act2_temple.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts a new game, gives a test team and the first three laurels and warps
# into the temple (act2_temple_setup.s, assembled into spare EWRAM: nothing in the ROM
# is patched), then plays design/phase3/SCRIPT.md beat 31 and Part 5 with key presses:
# Lasos's welcome, Act I (the program, a wrong entrance, Mynniskos, the comic mask, the
# ivy door), Act II (Thettalos, two entrances by cue), Act III (Theodoros waving the
# comic mask through and battling the tragic one, the audience's hint after two wrong
# entrances, the satyr by the goat door), the god-machine, Thespis's battle and his
# rewards, and a re-entry with the room still solved. Screenshots land in
# build/test_act2_temple/shots/; the run fails on any failed check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_act2_temple
engine_prepare TEMPLE "$OUT" tools/ichor/tests/act2_temple_consts.c tools/ichor/tests/act2_temple_setup.s
# The temple's event scripts by name: slice_lib finds people and signs by the script they run.
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^ThyrsaCity_TempleOfDionysus_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/temple_scripts.lua"
engine_run TEMPLE "$OUT" tools/ichor/tests/act2_temple.lua 400000 1800
