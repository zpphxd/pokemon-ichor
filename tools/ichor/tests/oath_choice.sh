#!/usr/bin/env bash
# Actual opening choice: default decline, confirmation, old saves and persistence.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS gPartiesCount gPokemonStoragePtr Task_HandleMultichoiceInput Task_HandleYesNoInput Task_SetClock_HandleInput Task_SetClock_HandleConfirmInput"
OUT=build/test_oath_choice
engine_prepare CHOICE "$OUT" tools/ichor/tests/oath_capture_consts.c tools/ichor/tests/oath_capture_setup.s
engine_run CHOICE "$OUT" tools/ichor/tests/oath_choice.lua 120000 600
