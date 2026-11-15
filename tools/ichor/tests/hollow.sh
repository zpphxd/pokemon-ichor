#!/usr/bin/env bash
# Hecate's Hollow, played with key presses:
#
#   tools/ichor/tests/hollow.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Quickstarts, gives a level-100 lead, warps to the east mouth and walks the cave:
# the old woman; the dark road at a tile and a half of light and its three barks;
# each fork's side way (an Escape Rope, the Bronze Obol and Phaino, Stardust); the
# Hekataion (beat 18: refused, then the offering and Hecate's Torch, the spring,
# the altar, the niche's Honey); the webs, Hekabe and her Barley Cake, both braziers
# and their lit halls, the web chamber (the Silk Scarf; Raknit once the Arachne
# amphora is set), Kallias, Battos, the Ether and the Revive; the shortcut's web,
# its ledge and the Dusk Ball; a wild Pokemon from the Hollow's table; the hounds
# after dark; and out of the west mouth.
# Output in build/test_hollow/ (screenshots in shots/); see hollow.lua.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_hollow
engine_prepare HOLLOW "$OUT" tools/ichor/tests/hollow_consts.c ""
# The Hollow's scripts by name, and the few addresses the walk reads besides.
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gPartiesCount|gLocalTime)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "  SCRIPTS = {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^HecatesHollow_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ { print "    " $3 " = 0x" $1 "," }'
  echo "  },"
  echo "}"
} > "$OUT/hollow_symbols.lua"
engine_run HOLLOW "$OUT" tools/ichor/tests/hollow.lua 600000 1800
