#!/usr/bin/env bash
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS sStarChart CB2_StarChart gBagPosition gBagMenu gWindows sNumStartMenuActions sCurrentStartMenuActions sStartMenuCursorPos Task_BagMenu_HandleInput Task_ItemContext_SingleRow Task_ItemContext_MultipleRows"
OUT=build/test_star_chart
engine_prepare CHART "$OUT" tools/ichor/tests/star_chart_consts.c tools/ichor/tests/star_chart_setup.s
tools/gbagfx/gbagfx graphics/items/icons/star_chart.png "$OUT/icon.4bpp" || exit 1
tools/gbagfx/gbagfx graphics/items/icon_palettes/star_chart.pal "$OUT/icon.gbapal" || exit 1
engine_run CHART "$OUT" tools/ichor/tests/star_chart.lua 150000 900
