#!/bin/bash
# Real picture loaders and back animation tables, not a battle playthrough.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROM="${1:-${ROM:-pokeemerald.gba}}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS gTrainerPalette_Brendan gTrainerPalette_May
gTrainerBackPic_Brendan gTrainerBackPic_May"
engine_prepare PLAYER_BATTLE build/player_battle \
  tools/ichor/tests/player_battle_consts.c tools/ichor/tests/player_battle_setup.s
if [ "$(wc -c < build/player_battle/setup.bin)" -gt 4096 ]; then
  echo "PLAYER_BATTLE FAIL: fixture exceeds reserved EWRAM"
  exit 1
fi
engine_run PLAYER_BATTLE build/player_battle tools/ichor/tests/player_battle.lua 12000 300
python3 tools/ichor/tests/player_battle_render.py
