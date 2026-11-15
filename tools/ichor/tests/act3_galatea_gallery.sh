#!/usr/bin/env bash
# Galatea's Gallery, the Temple of Aphrodite's rite (design/phase4/SCRIPT.md Part 5):
#
#   tools/ichor/tests/act3_galatea_gallery.sh [rom]   (default: pokeemerald.gba; run make first)
#
# In the temple itself (MAP_KYTHERA_TEMPLE_OF_APHRODITE), with two level-100 test
# Pokémon given by a test-only script (nothing in the ROM is patched), the player
# walks the routes tools/ichor/maps/kythera_temple.py checked against its model of
# the statues (act3_galatea_routes.lua), and the game must agree with the model:
#   - the pronaos: turning back toward S1 gets you touched and sent to the door;
#     walking up facing M0 takes you through to the gallery;
#   - the gallery: up the west aisle and along the north aisle, Rhodanthe at the
#     door, every statue where the model says;
#   - the rose court: up the east lane, P2 turned to face down it (and still turned
#     after the temple is left and entered again), along the north walk to the dais;
#     Galatea steps down, the battle, the Foam Laurel, VAR_ICHOR_ACT3 = 3, Cygnus,
#     the falls hint; afterwards the statues stand still.
# Output in build/test_galatea_gallery/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_galatea_gallery
engine_prepare GALLERY "$OUT" tools/ichor/tests/act3_galatea_gallery_consts.c tools/ichor/tests/act3_galatea_gallery_setup.s
# The temple's event scripts, by name (slice_symbols.sh lists only the slice's).
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^KytheraTempleOfAphrodite_EventScript_[A-Za-z0-9_]+$/ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/temple_scripts.lua"
engine_run GALLERY "$OUT" tools/ichor/tests/act3_galatea_gallery.lua 90000 900
