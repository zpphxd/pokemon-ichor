#!/usr/bin/env bash
# Herm waystones check (design/SYSTEMS.md §4), in game.
#
#   tools/ichor/tests/ichor_herms.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Route 1's great herm with no oil, anointed, and anointed again; Hermes's
# Favor; Daedalus's Wings flying from Akti back to the herm's landing tile; and
# the bonus for the last herm. Output in build/test_ichor_herms/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_ichor_herms
engine_prepare HERMS "$OUT" tools/ichor/tests/ichor_herms_consts.c tools/ichor/tests/ichor_herms_setup.s
engine_run HERMS "$OUT" tools/ichor/tests/ichor_herms.lua 60000 600
