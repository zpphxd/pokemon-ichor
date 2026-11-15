#!/usr/bin/env bash
# Eleusa's story, beats 19-22, played with key presses:
#
#   tools/ichor/tests/temple_demeter.sh [rom]     (default: pokeemerald.gba; run make first)
#
# From a set-up save state (Quickstart, a level-100 lead, the Herald Laurel and the
# Torch, the player on Eleusa's west edge as if just in from Route 5), it walks in
# through Krokis's gate (the saffron thread), plays beat 20 (the arrival flags, the
# music, Kleon in the square), then the Temple of Demeter: Doso, the three acolytes,
# the four season braziers in the dark, a fall into a pit and the chalk path, and
# Chloe three ways from one state: lost (a whiteout, no Laurel), by night (Persenyx's
# team) and by day (Korantha's), each checked for the Harvest Laurel, Giga Drain, the
# barley cake, Demeter's Favor and the boarded pits. Then re-entry after the Laurel,
# the procession's arrival, Kerykos (NO, then YES), and the night of the Mysteries:
# the raid, the multi battle beside Kleon, and the stair down to the sanctum. Last,
# back up through the Ploutonion to the wrecked hall, Kleon at the door.
# Output in build/test_temple_demeter/ (screenshots in shots/); see temple_demeter.lua.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_temple_demeter
engine_prepare DEMETER "$OUT" tools/ichor/tests/temple_demeter_consts.c tools/ichor/tests/temple_demeter_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gPartiesCount|gBattleTypeFlags)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/demeter_symbols.lua"
engine_run DEMETER "$OUT" tools/ichor/tests/temple_demeter.lua 600000 2400
