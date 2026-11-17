#!/bin/bash
# Move animations must not darken the top of the battle screen (BG palettes,
# blend and window registers) for ordinary contact, special and status moves.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROM="${1:-${ROM:-pokeemerald.gba}}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS gAnimScriptActive gBattleAnimAttacker gAnimMoveIndex sGpuRegBuffer gBattleEnvironment"
OUT=build/test_battle_anim_light
engine_prepare ANIMLIGHT "$OUT" tools/ichor/tests/battle_anim_light_consts.c tools/ichor/tests/battle_anim_light_setup.s
engine_run ANIMLIGHT "$OUT" tools/ichor/tests/battle_anim_light.lua 40000 300
