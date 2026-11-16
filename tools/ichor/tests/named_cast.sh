#!/usr/bin/env bash
# Forced real image-table slots, not natural dialogue/battle/controller coverage.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS gTrainerPicInfo gObjectEventPal_IchorCast gObjectEventPal_IchorFolk gObjectEventPal_IchorTheoxenia"
OUT=build/named_cast
engine_prepare NAMED_CAST "$OUT" tools/ichor/tests/named_cast_consts.c tools/ichor/tests/named_cast_setup.s
engine_run NAMED_CAST "$OUT" tools/ichor/tests/named_cast.lua 30000 300
