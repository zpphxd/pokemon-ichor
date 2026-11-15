#!/usr/bin/env bash
# The Dionysia check: plays Act II's beats 32-34 in Thyrsa's theater headlessly.
#
#   tools/ichor/tests/act2_dionysia.sh [rom]     (default: pokeemerald.gba; run make first)
#
# From a save just after the Three-Act Play (the Mask Laurel won, Act I done, a
# level-100 test Pokémon; act2_dionysia_setup.s, assembled into spare EWRAM, so
# nothing in the ROM is patched), in through the theater's top gate:
#   beat 32  the workers, the first step down, the whole play, Silenos's call,
#            Thespis backstage, a wrong entrance (no mask), then the comic, tragic
#            and satyr entrances, the trance breaking, the actor's battle, the
#            inky handprint and the program;
#   beat 33  out through the skene and back in: Kleon on the stage's edge, his
#            third battle, and the empty theater;
#   beat 34  Silenos's riddle (one wrong answer, then right) and his fight: the
#            Girdle of Herakles and Daedalus's page III.
# Checks VAR_ICHOR_DIONYSIA, the flags and the trainer flags after each beat.
# Screenshots of every message box land in build/test_act2_dionysia/shots/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_act2_dionysia
engine_prepare DIONYSIA "$OUT" tools/ichor/tests/act2_dionysia_consts.c tools/ichor/tests/act2_dionysia_setup.s
# The theater's scripts by name, so the test finds people and things on the map
# as built (slice_symbols.sh only lists the slice's maps).
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^ThyrsaTheater[A-Za-z0-9_]*_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/theater_scripts.lua"
engine_run DIONYSIA "$OUT" tools/ichor/tests/act2_dionysia.lua 400000 1800
