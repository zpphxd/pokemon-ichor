#!/usr/bin/env bash
# The post-game's first sprites: the Euploia (sail full and slack) rows in all
# four headings, the eleven new walkers walk in all four, each from its own
# graphics id and in its own palette, and the six trainer pics are registered.
#
#   tools/ichor/tests/pg_sprites.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Test scripts come from pg_sprites_setup.s, assembled into spare EWRAM;
# nothing in the ROM is patched. Output and screenshots in build/test_pg_sprites/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_pg_sprites
engine_prepare PGSPR "$OUT" tools/ichor/tests/pg_sprites_consts.c tools/ichor/tests/pg_sprites_setup.s
# gTrainerPicInfo is not in the shared symbol lists
arm-none-eabi-nm "$ELF" | awk '$3 == "gTrainerPicInfo" { print "  gTrainerPicInfo = 0x" $1 "," }' > "$OUT/extra.lua"
{ echo "return {"; cat "$OUT/extra.lua"; echo "}"; } > "$OUT/pg_symbols.lua"
engine_run PGSPR "$OUT" tools/ichor/tests/pg_sprites.lua 40000 400
