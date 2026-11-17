#!/usr/bin/env bash
# Lakonia's fifteen rooms (Gytheion's five, Lakonia's ten): each loads and draws,
# and each household's event plays, with key presses.
#
#   tools/ichor/tests/lakonia_rooms.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts, gives a lead, then warps into each room just inside its mat (the
# outdoor maps are the chapter builder's), and plays it:
#   Gytheion: the healer heals and sets the respawn; Porphyris takes three Shoal
#   Shells for the King's Rock; Lysandros offers his trade (declined); Timaia's
#   fig cake, then Leftovers once it's delivered; Klymene's Shiny Stone after the
#   climax.
#   Lakonia: the healer twice ("Fight better."); the Agora's signs; Lampito's
#   hearth cold, then lit once Rhea is unmasked; Gylippos's strap; Chilon's quiz
#   answered wrong (no glasses); the black broth's TM Bulk Up; Archidamos's Focus
#   Sash after Kleon's ring; Hipposthenes's Choice Band for a Geogrip; Orthia's
#   cheese game, won by walking behind the watchers; Lichas's table and bed.
# Output in build/test_lakonia_rooms/ (screenshots in shots/).
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_lakonia_rooms
engine_prepare LAKONIA_ROOMS "$OUT" tools/ichor/tests/lakonia_rooms_consts.c ""
# the rooms' scripts by name, for L.npc and L.sign
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Gytheion_|Lakonia_|LakoniaLampito_|LakoniaOrthia_)[A-Za-z_]*EventScript_[A-Za-z0-9_]*$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/lakonia_rooms_symbols.lua"
engine_run LAKONIA_ROOMS "$OUT" tools/ichor/tests/lakonia_rooms.lua 400000 1500
