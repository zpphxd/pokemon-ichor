#!/usr/bin/env bash
# Theoxenia sprites check: Sam, Apollo, Cami and Demeter load from their
# graphics IDs, and both new animations play to their end: the lyre strum
# (sAnimTable_IchorLyre) and Cami rising from her bench (sAnimTable_IchorCami).
#
#   tools/ichor/tests/theoxenia_sprites.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Test scripts come from theoxenia_sprites_setup.s, assembled into spare EWRAM;
# nothing in the ROM is patched. Output in build/test_theoxenia/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_theoxenia
engine_prepare THEOX "$OUT" tools/ichor/tests/theoxenia_sprites_consts.c tools/ichor/tests/theoxenia_sprites_setup.s
# gSprites is not in the shared symbol lists
arm-none-eabi-nm "$ELF" | awk '$3 == "gSprites" { print "return { gSprites = 0x" $1 " }"; exit }' > "$OUT/theox_symbols.lua"
engine_run THEOX "$OUT" tools/ichor/tests/theoxenia_sprites.lua 20000 300
