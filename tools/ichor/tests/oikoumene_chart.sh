#!/usr/bin/env bash
# The Oikoumene chart check (design/oikoumene/BUILD.md §5, "The chart"), in game.
#
#   tools/ichor/tests/oikoumene_chart.sh [rom]     (default: pokeemerald.gba; run make first)
#
# On Oikoumene ground: the region is the Oikoumene's (its chart, its popups, its
# battle music) and the chart's state follows you round. Daedalus's Wings: the Fly
# map shows the Oikoumene chart; the crossing targets stay hidden until you've
# arrived; AETHOS lands at Akti; THE OIKOUMENE, on the Aethos chart, lands at the
# last Oikoumene port. The Nurseries' month and table offset are test/ichor_nursery.c's
# (make check TESTS=test/ichor_nursery.c). Output in build/test_oikoumene_chart/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_oikoumene_chart
engine_prepare CHART "$OUT" tools/ichor/tests/oikoumene_chart_consts.c tools/ichor/tests/oikoumene_chart_setup.s
# region_map.c's statics this check reads
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(sFlyDestIconSpriteTemplate|sFlyMap)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/chart_symbols.lua"
engine_run CHART "$OUT" tools/ichor/tests/oikoumene_chart.lua 120000 900
