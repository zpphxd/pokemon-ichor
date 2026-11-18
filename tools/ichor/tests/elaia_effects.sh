#!/bin/bash
# Actual grass walk plus explicitly labeled engine field/state fixtures.
set -euo pipefail
cd "$(dirname "$0")/../../.."
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS UpdateTallGrassFieldEffect UpdateLongGrassFieldEffect
SpriteCB_TrainerIcons gFieldEffectObjectPic_Arrow gFieldEffectObjectPic_TallGrass
gFieldEffectObjectPic_LongGrass gFieldEffectObjectPic_SandFootprints gEmotes"
ENGINE_SYMS="$ENGINE_SYMS gObjectEventPal_Brendan gObjectEventPal_May"
engine_prepare ELAIA_EFFECTS build/elaia_effects \
  tools/ichor/tests/elaia_effects_consts.c tools/ichor/tests/elaia_effects_setup.s
if [ "$(wc -c < build/elaia_effects/setup.bin)" -gt 4096 ]; then
  echo "ELAIA_EFFECTS FAIL: fixture exceeds its reserved EWRAM page"
  exit 1
fi
engine_run ELAIA_EFFECTS build/elaia_effects tools/ichor/tests/elaia_effects.lua 60000 900
