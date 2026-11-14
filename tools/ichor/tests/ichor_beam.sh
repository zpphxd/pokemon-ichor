#!/usr/bin/env bash
# The beam trace (engine need E9, src/ichor_beam.c):
#
#   tools/ichor/tests/ichor_beam.sh [rom]     (default: pokeemerald.gba; run make first)
#
# In the Akti Agora, with its three objects rebuilt as a source mirror, a
# mirror and a target (act3_lib.lua; nothing in the ROM is patched), the check
# traces the beam, turns the mirror with turnobject, traces again, and checks
# VAR_RESULT and the beam metatiles in the live map grid, the old path put
# back each time. Output in build/test_ichor_beam/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_ichor_beam
engine_prepare BEAM "$OUT" tools/ichor/tests/act3_consts.c tools/ichor/tests/act3_setup.s
arm-none-eabi-nm "$OUT/setup.elf" | awk '$3 ~ /^Act3Test_/ { print $3, $1 }' > "$OUT/setup.syms"
engine_run BEAM "$OUT" tools/ichor/tests/ichor_beam.lua 40000 600
