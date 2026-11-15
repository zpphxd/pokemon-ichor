#!/usr/bin/env bash
# The Arkadian climb check: plays beats 38-40 from the top of Route 11 to Arkadia.
#
#   tools/ichor/tests/act2_heights.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts a new game, gives a test team, the Girdle of Herakles and the laurels
# Act II has given by beat 38, and warps to the top of Route 11 (act2_heights_setup.s,
# assembled into spare EWRAM: nothing in the ROM is patched). Then, with key presses:
# beat 38 (the muleteer's road shut; drum 1 over the edge, drum 2 into the gap and the
# Hard Stone, drum 3 to the cliff), the gorge (trainers, the great herm, Pelasgos's
# spring, the thirsty traveler), beat 39 at Styx Falls (Alethea at the Oath Stone, the
# oath, the black pool, the obol), Route 12 (the hawk spur's drum and the nest's page,
# the great herm), beat 40 in the Cave of Maia (the lyre's story, the priestess and
# the Chelyra), Basanos and the shrine of Artemis, and the road down into Arkadia;
# then back onto Route 11 to check the drums stay moved. Screenshots land in
# build/test_act2_heights/shots/; the run fails on any failed check, a crash or a
# timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_act2_heights
engine_prepare HEIGHTS "$OUT" tools/ichor/tests/act2_heights_consts.c tools/ichor/tests/act2_heights_setup.s
# The climb's event scripts by name: slice_lib finds people and signs by the script they run.
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Route11_KrathisGorge|StyxFalls|Route12_CypressRoad|Route12_CaveOfMaia)_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ { print "  " $3 " = 0x" $1 "," }'
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^EventScript_(StrengthBoulder|IchorGreatBoulder|IchorAltar_Hermes)$/ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/heights_scripts.lua"
engine_run HEIGHTS "$OUT" tools/ichor/tests/act2_heights.lua 600000 2400
