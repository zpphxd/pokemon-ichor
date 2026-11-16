#!/usr/bin/env bash
# Real start-menu entry, journal navigation, scrolling and saved receipts.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS sNumStartMenuActions sCurrentStartMenuActions sStartMenuCursorPos sStartMenuItems StartMenuDeedsCallback StartMenuPlayerNameCallback CB2_TrainerCard gMenuCallback"
OUT=build/test_deeds
engine_prepare DEEDS "$OUT" tools/ichor/tests/deeds_consts.c tools/ichor/tests/deeds_setup.s
engine_run DEEDS "$OUT" tools/ichor/tests/deeds.lua 150000 900
