#!/usr/bin/env bash
# Test-only EWRAM gallery; requires the selected ROM's matching ELF and map.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS gTrainerPicInfo"
OUT="${AKTI_ART_OUT:-build/akti_art}"
engine_prepare AKTI_ART "$OUT" tools/ichor/tests/akti_art_consts.c tools/ichor/tests/akti_art_setup.s
engine_run AKTI_ART "$OUT" tools/ichor/tests/akti_art.lua 30000 120
