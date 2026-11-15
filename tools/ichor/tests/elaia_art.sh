#!/usr/bin/env bash
# Load Elaia's Pokemon views through the ROM's real sprite/palette functions.
# Test-only EWRAM fixture; no code or data is patched into the ROM.
# ELAIA_ART_OUT selects output; ELAIA_ART_BASELINE=1 accounts for the preserved
# before-redraw Smoliv's single front frame only. Normal validation stays strict.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT="${ELAIA_ART_OUT:-build/elaia_art}"
engine_prepare ART "$OUT" tools/ichor/tests/elaia_art_consts.c tools/ichor/tests/elaia_art_setup.s
engine_run ART "$OUT" tools/ichor/tests/elaia_art.lua 30000 120
