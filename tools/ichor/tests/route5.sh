#!/usr/bin/env bash
# Route 5, the Skironian cliffs, played with key presses:
#
#   tools/ichor/tests/route5.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Quickstarts, gives a level-100 lead, the Bronze Hammer, olive oil, the Old Rod
# and an Onotis, and comes out of Hecate's Hollow's west mouth. Then it walks the
# road to Eleusa: a wild Pokemon from the band (checked against the route's
# table), every trainer, item and hidden item, the signs and set pieces,
# Aphrodite's altar, the rubble, the Good Rod, the inn (rest and the trade), the
# great herm, and over the seam into Eleusa and back.
# Output in build/test_route5/ (screenshots in shots/); see route5.lua.
# ROUTE5_FROM=inn starts at the inn's door (the inn, the herm and the seam only).
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_route5
engine_prepare ROUTE5 "$OUT" tools/ichor/tests/route5_consts.c tools/ichor/tests/route5_setup.s
# Route 5's and the inn's scripts by name (slice_symbols.sh lists only the
# slice's maps), the engine scripts the road runs, and a few addresses.
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gPartiesCount|CB2_PokeStorage)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "  SCRIPTS = {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^Route5_(SkironianCliffs|RestHouse)_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ { print "    " $3 " = 0x" $1 "," }'
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^EventScript_(StrengthBoulder|CutTree|RockSmash|IchorAltar_Aphrodite|IchorGreatHerm)$/ && !seen[$3]++ { print "    " $3 " = 0x" $1 "," }'
  echo "  },"
  echo "}"
} > "$OUT/route5_symbols.lua"
engine_run ROUTE5 "$OUT" tools/ichor/tests/route5.lua 500000 3600
