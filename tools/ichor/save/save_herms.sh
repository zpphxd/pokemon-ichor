#!/usr/bin/env bash
# Read a battery save headlessly, and with HERMS=ids register travel herms and save in game:
#   tools/ichor/save/save_herms.sh COPY.sav       (always work on a copy, never OpenEmu's own file)
set -u
cd "$(dirname "$0")/../../.."
ROM=pokeemerald.gba
. tools/ichor/tests/engine_build.sh
OUT=build/save_herms
engine_prepare SAVEHERMS "$OUT" tools/ichor/save/save_herms_consts.c tools/ichor/save/save_herms_setup.s
SAVE_IN="$1" HERMS="${HERMS:-}" FLAGS="${FLAGS:-}" engine_run SAVEHERMS "$OUT" tools/ichor/save/save_herms.lua 20000 300
grep -E "BEFORE|SET|SETFLAG|AFTER" "$OUT/run.log"
