#!/usr/bin/env bash
# Route 4, the Isthmus road, played with key presses:
#
#   tools/ichor/tests/route4.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Quickstarts with the Herald Laurel and the Bronze Hammer, a level-100 lead and a
# Repel, warps to Emporion inside the Isthmus Gate and walks north across the seam
# onto Route 4. Then the whole road: every trainer fought (Exekias, Myrrhine, Laas,
# Menalkas, Pheidippos, Kapelos), every item and hidden item picked up that Act I
# allows, every person and sign read, the woods clearing's rubble broken, a wild
# Pokemon met in the tall grass, the great herm cleansed and anointed, beat 17's two
# scenes (the slide, the procession), the terrace lips jumped, and the Hollow's mouth
# entered. The orchard (Sickle) and the family tomb (Girdle) are checked shut, then
# opened with the relics. Output in build/test_route4/ (screenshots in shots/).
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_route4
engine_prepare ROUTE4 "$OUT" tools/ichor/tests/route4_consts.c ""
# Route 4's scripts and the obstacle scripts by name, and the addresses the walk reads.
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gPartiesCount|gBattleMons|gSaveBlock1Ptr|gBagPosition|Task_BagMenu_HandleInput)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "  SCRIPTS = {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^Route4_Isthmus_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ { print "    " $3 " = 0x" $1 "," }'
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^EventScript_(RockSmash|CutTree|StrengthBoulder)$/ { print "    " $3 " = 0x" $1 "," }'
  echo "  },"
  echo "}"
} > "$OUT/route4_symbols.lua"
engine_run ROUTE4 "$OUT" tools/ichor/tests/route4.lua 400000 1500
