#!/usr/bin/env bash
# IchorSave check: the one block of Ichor state in SaveBlock3 (include/ichor_save.h).
#
#   tools/ichor/tests/ichor_save.sh [rom]     (default: pokeemerald.gba; run make first)
#
# A new game's defaults, scripts writing every bank (flags, daily flags, vars),
# a day turning over, a save and a CONTINUE, and an old save migrating. Test
# scripts come from ichor_save_setup.s, assembled into spare EWRAM; nothing in
# the ROM is patched. Output in build/test_ichor_save/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_ichor_save
engine_prepare SAVE "$OUT" tools/ichor/tests/ichor_save_consts.c tools/ichor/tests/ichor_save_setup.s
engine_run SAVE "$OUT" tools/ichor/tests/ichor_save.lua 40000 600
