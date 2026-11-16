#!/usr/bin/env bash
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS sStarChart CB2_StarChart gBagPosition gWindows sNumStartMenuActions sCurrentStartMenuActions sStartMenuCursorPos Task_BagMenu_HandleInput Task_ItemContext_SingleRow Task_ItemContext_MultipleRows"
OUT=build/test_star_chart
engine_prepare CHART "$OUT" tools/ichor/tests/star_chart_consts.c tools/ichor/tests/star_chart_setup.s
engine_run CHART "$OUT" tools/ichor/tests/star_chart.lua 150000 900
