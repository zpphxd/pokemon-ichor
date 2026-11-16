#!/bin/bash
# Forced renderer fixtures, not retired-bike gameplay/controller eligibility.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROM="${1:-${ROM:-pokeemerald.gba}}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS gObjectEventPal_Brendan gObjectEventPal_May
gObjectEventPic_BrendanMachBike gObjectEventPic_BrendanAcroBike
gObjectEventPic_MayMachBike gObjectEventPic_MayAcroBike"
engine_prepare PLAYER_BIKES build/player_bikes \
  tools/ichor/tests/player_bikes_consts.c tools/ichor/tests/player_bikes_setup.s
if [ "$(wc -c < build/player_bikes/setup.bin)" -gt 4096 ]; then
  echo "PLAYER_BIKES FAIL: fixture exceeds the reserved EWRAM page"
  exit 1
fi
engine_run PLAYER_BIKES build/player_bikes tools/ichor/tests/player_bikes.lua 40000 600
