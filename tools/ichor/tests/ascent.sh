#!/usr/bin/env bash
# The Ascent of Olympus (design/LEAGUE.md, design/maps/Ascent_*.md): with eight
# Laurels and an assisted team, ride the muleteer from Astyra and climb the
# whole critical path on foot: the slopes' pair, the cloud ledges' pair and the
# camp (its heal and its herm), the Icefall's slide hall and its pair, the drum
# seal, the Glacier's narrows pair, its frozen lake, the Gate of the Winds (a
# wrong push and the reset lever first, then all three drums), out of the cloud
# onto 3F (the awe scenes), both stair pairs, the gatekeeper, and in through
# the Propylaia to the guard. Every slide and push is the builder's proven
# answer (tools/ichor/tests/ascent_plans.lua), played in the game.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_ascent
engine_prepare ASCENT "$OUT" tools/ichor/tests/ascent_consts.c tools/ichor/tests/ascent_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Ascent_|Olympus_Propylaia_|Astyra_EventScript_Muleteer)[A-Za-z0-9_]*$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/ascent_symbols.lua"
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(HealPlayerParty)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/ascent_callbacks.lua"
cp tools/ichor/tests/ascent_plans.lua "$OUT/ascent_plans.lua"
engine_run ASCENT "$OUT" tools/ichor/tests/ascent.lua 1200000 3600
