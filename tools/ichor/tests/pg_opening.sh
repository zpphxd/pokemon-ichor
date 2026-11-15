#!/usr/bin/env bash
# The post-game's opening on Kalliste (design/postgame/BUILD.md, batch 1, the akti row), in game.
#
#   tools/ichor/tests/pg_opening.sh [rom]     (default: pokeemerald.gba; run make first)
#
# With FLAG_ICHOR_POSTGAME clear, nothing of the post-game appears in Elaia or Akti.
# With it set: Kleon at Elaia's well, the heralds, the Euploia given on Akti's quay and
# its gangplank, Lampon's fire, Diktys's boat, Glaukias, and Phaedon's heal.
# Output in build/test_pg_opening/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_pg_opening
engine_prepare PGOPEN "$OUT" tools/ichor/tests/pg_opening_consts.c tools/ichor/tests/pg_opening_setup.s
engine_run PGOPEN "$OUT" tools/ichor/tests/pg_opening.lua 120000 900
