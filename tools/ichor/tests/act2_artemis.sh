#!/usr/bin/env bash
# The Hunt for the Hind check: plays the Temple of Artemis from the door to the Moon Laurel.
#
#   tools/ichor/tests/act2_artemis.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts a new game, gives a test team and the first four laurels and walks in at the
# temple's door (act2_artemis_setup.s, assembled into spare EWRAM: nothing in the ROM is
# patched), then plays design/phase3/SCRIPT.md beat 44 and Part 5 with key presses:
# Phylonoe's welcome and her answers, the great altar, Stage I (three walks back from the
# hound, then Phylonoe's direct hint, then past the hound behind the great myrtle, Kyrene),
# Stage II (a walk back to the second arch; past the turning hound and the stele's hound;
# Anthia, her gate and her bench's feather; the shortcut to the third arch), Stage III (the
# hind's three touches, each stage's hounds read live, Sagitta and the stair's hedge,
# Prokris), Kallisto's scene and battle, the Moon Laurel and her gifts, and a re-entry with
# the garden solved and its hounds asleep.
#
# The hounds are crossed the way a player crosses them: the test watches each one, learns
# where it is in its patrol (tools/ichor/maps/temple_artemis.py --lua writes the patrols),
# and only steps where no hound will be looking. Screenshots land in
# build/test_act2_artemis/shots/; the run fails on any failed check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_act2_artemis
engine_prepare ARTEMIS "$OUT" tools/ichor/tests/act2_artemis_consts.c tools/ichor/tests/act2_artemis_setup.s
/usr/bin/python3 tools/ichor/maps/temple_artemis.py --lua "$OUT/hunt.lua" || { echo "ARTEMIS FAIL: the hunt's patrols"; exit 1; }
# The temple's event scripts by name: slice_lib finds people and signs by the script they run.
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Arkadia_TempleOfArtemis_EventScript_[A-Za-z0-9_]+|EventScript_IchorTempleAltar_Artemis)$/ && $3 !~ /_[0-9]+$/ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/temple_scripts.lua"
engine_run ARTEMIS "$OUT" tools/ichor/tests/act2_artemis.lua 700000 2400
