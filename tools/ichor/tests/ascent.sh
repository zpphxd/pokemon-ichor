#!/usr/bin/env bash
# The Ascent of Olympus (design/LEAGUE.md, design/maps/Ascent_*.md): with eight
# Laurels and an assisted team, ride the muleteer from Astyra and climb the
# whole critical path on foot: the slopes, the cloud ledges and the camp (its
# heal and its herm), the Leuke snowfield (its stair pair, the Mirror Tarn),
# the Icefall's slide hall, its pair and drum seal, the Glacier outdoors (the
# narrows pair; the frozen lake: a dead end and its reset, then the answer; the
# Gate of the Winds: a wrong push and the lever, then all three drums; the Wings'
# eyrie; the Thread's descent to the Vault and back), Boreas's ridge (Nephele,
# the spine's pair, the Bellows of Boreas: the Hammer's rubble, a push and the
# lever, then both drums), 3F (the cloud break, the stair pairs, the camera up
# the Propylaia's facade, the gatekeeper, the watch-post under the Helm), and in
# through the bronze doors to the guard. Every post-game gate on the way is read
# and stays shut. Every slide and push is the builder's proven answer
# (tools/ichor/tests/ascent_plans.lua, oros_plans.lua), played in the game.
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
cp tools/ichor/tests/oros_plans.lua "$OUT/oros_plans.lua"
engine_run ASCENT "$OUT" tools/ichor/tests/ascent.lua 1200000 3600
