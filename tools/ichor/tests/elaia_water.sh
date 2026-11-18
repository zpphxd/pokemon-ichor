#!/bin/bash
# Real ROM renderer coverage, not Surf/Dive controller eligibility.
set -euo pipefail
cd "$(dirname "$0")/../../.."
ROM="${1:-${ROM:-pokeemerald.gba}}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS gSpecialVar_0x8004 gObjectEventPal_Brendan gObjectEventPal_May
gObjectEventPal_PlayerUnderwater gObjectEventPic_BrendanUnderwater
gObjectEventPic_MayUnderwater gFieldEffectObjectPic_SurfBlob UpdateSurfBlobFieldEffect
SpriteCB_UnderwaterSurfBlob"
engine_prepare ELAIA_WATER build/elaia_water \
  tools/ichor/tests/elaia_water_consts.c tools/ichor/tests/elaia_water_setup.s
if [ "$(wc -c < build/elaia_water/setup.bin)" -gt 4096 ]; then
  echo "ELAIA_WATER FAIL: fixture exceeds its reserved EWRAM page"
  exit 1
fi
engine_run ELAIA_WATER build/elaia_water tools/ichor/tests/elaia_water.lua 40000 600
