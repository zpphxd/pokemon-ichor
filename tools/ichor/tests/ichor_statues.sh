#!/usr/bin/env bash
# Marble statues and bronze mirrors (engine need E8, src/ichor_statue.c):
#
#   tools/ichor/tests/ichor_statues.sh [rom]     (default: pokeemerald.gba; run make first)
#
# In the Akti Agora, with its three objects rebuilt as a statue, a mirror and a
# rooted statue (act3_lib.lua; nothing in the ROM is patched), the player walks
# and turns: a statue in a wall mirror stays, one behind the mirror's back
# steps nearer, one faced directly stays, a rooted one turns but never moves,
# a person blocks the view, and a statue that reaches the player runs its touch
# script. Output in build/test_ichor_statues/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_ichor_statues
engine_prepare STATUES "$OUT" tools/ichor/tests/act3_consts.c tools/ichor/tests/act3_setup.s
arm-none-eabi-nm "$OUT/setup.elf" | awk '$3 ~ /^Act3Test_/ { print $3, $1 }' > "$OUT/setup.syms"
engine_run STATUES "$OUT" tools/ichor/tests/ichor_statues.lua 40000 600
