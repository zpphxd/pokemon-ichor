#!/usr/bin/env bash
# Let the actual field clock turn the day without leaving the visitor/weather map.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_omen_rollover
engine_prepare ROLLOVER "$OUT" tools/ichor/tests/omen_rollover_consts.c tools/ichor/tests/omen_rollover_setup.s
engine_run ROLLOVER "$OUT" tools/ichor/tests/omen_rollover.lua 120000 900
