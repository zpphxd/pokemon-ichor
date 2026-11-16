#!/usr/bin/env bash
# Real shelf menus, restoration, all twelve paintings and the collection reward.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS sAmphoraWindowIdPlusOne gWindows"
OUT=build/test_amphorae
engine_prepare AMPHORAE "$OUT" tools/ichor/tests/amphorae_consts.c tools/ichor/tests/amphorae_setup.s
engine_run AMPHORAE "$OUT" tools/ichor/tests/amphorae.lua 200000 900
