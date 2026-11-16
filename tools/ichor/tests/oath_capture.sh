#!/usr/bin/env bash
# Fixture enrollment; native battles, captures, permanent falls and sealed storage.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS gPartiesCount gBagPosition gBattleResults Task_BagMenu_HandleInput Task_HandleChooseMonInput Task_ReturnToChooseMonAfterText CB2_BagMenuRun sOathCatchDenied sOathAftermathNotice gPokemonStoragePtr Task_PCMainMenu Task_PokeStorageMain Task_OnSelectedMon Task_DepositMenu sMonSummaryScreen sAutoActionOn sIsMonBeingMoved CB2_PssChangePokemonNickname"
OUT=build/test_oath_capture
engine_prepare OATH "$OUT" tools/ichor/tests/oath_capture_consts.c tools/ichor/tests/oath_capture_setup.s
engine_run OATH "$OUT" tools/ichor/tests/oath_capture.lua 150000 600
