#!/usr/bin/env bash
# Fixture enrollment and storage; actual loss, recovery, title and CONTINUE.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS gPartiesCount gPokemonStoragePtr sOathAftermathNotice CB2_OathEndScreen CB2_InitTitleScreen"
OUT=build/test_oath_recovery
engine_prepare RECOVERY "$OUT" tools/ichor/tests/oath_capture_consts.c tools/ichor/tests/oath_capture_setup.s
engine_run RECOVERY "$OUT" tools/ichor/tests/oath_recovery.lua 120000 600
