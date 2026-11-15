#!/bin/bash
# Forced unused-state rendering, not gameplay/controller eligibility.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROM="${1:-${ROM:-pokeemerald.gba}}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS gObjectEventPal_Brendan gObjectEventPal_May"
engine_prepare PLAYER_UNUSED build/player_unused \
  tools/ichor/tests/player_unused_consts.c tools/ichor/tests/player_unused_setup.s
if [ "$(wc -c < build/player_unused/setup.bin)" -gt 4096 ]; then
  echo "PLAYER_UNUSED FAIL: fixture exceeds the reserved EWRAM page"
  exit 1
fi
engine_run PLAYER_UNUSED build/player_unused tools/ichor/tests/player_unused.lua 15000 300
