#!/usr/bin/env bash
# Put a new Ichor build into OpenEmu without losing the save.
#
#   tools/ichor/openemu_update.sh [rom]     (default: pokeemerald.gba)
#
# OpenEmu's GBA core (mGBA) names a game's battery save after the ROM file:
# the library copy Game Library/roms/Game Boy Advance/ichor_latest.zip saves
# to mGBA/Battery Saves/ichor_latest.sav. Re-importing a new build makes a new
# game entry with an empty save, so instead this script overwrites the library
# copy in place (same file name, same entry) and the old save loads with it.
#
# It backs the save up first (mGBA/Battery Saves/ichor_backups/), and stops if
# a game is running, because OpenEmu writes the save back when a game closes.
# Use the game's own SAVE, not OpenEmu save states: a state is a snapshot of
# one build's memory and will not load into another.
set -euo pipefail
cd "$(dirname "$0")/../.."
ROM="${1:-pokeemerald.gba}"
OE="$HOME/Library/Application Support/OpenEmu"
LIB="$OE/Game Library/roms/Game Boy Advance/ichor_latest.zip"
SAVE="$OE/mGBA/Battery Saves/ichor_latest.sav"
BACKUPS="$OE/mGBA/Battery Saves/ichor_backups"

[ -f "$ROM" ] || { echo "No $ROM (run make first)."; exit 1; }
[ -f "$LIB" ] || { echo "No $LIB: import playtest/ichor_latest.zip into OpenEmu once, then rerun."; exit 1; }
if pgrep -f "OpenEmuHelperApp" >/dev/null 2>&1; then
  echo "A game is running in OpenEmu. Save in game, close the game window, then rerun."; exit 1
fi

if [ -f "$SAVE" ]; then
  mkdir -p "$BACKUPS"
  stamp=$(date +%Y%m%d-%H%M%S)
  cp -p "$SAVE" "$BACKUPS/ichor_latest_$stamp.sav"
  echo "Save backed up: $BACKUPS/ichor_latest_$stamp.sav"
fi

tmp=$(mktemp -d)
cp "$ROM" "$tmp/ichor_latest.gba"
(cd "$tmp" && zip -q ichor_latest.zip ichor_latest.gba)
cp "$tmp/ichor_latest.zip" "$LIB"
rm -rf "$tmp"

# OpenEmu doesn't run the zip: it unpacks it once into a temp cache keyed by
# the ROM's original checksum and reuses that copy on every launch. Overwrite
# every cached ichor_latest.gba so the next launch runs this build.
CACHE="${TMPDIR:-/tmp}/org.openemu.OpenEmu"
n=0
for f in "$CACHE"/*/ichor_latest.gba; do
  [ -f "$f" ] || continue
  cp "$ROM" "$f"; n=$((n + 1))
done
echo "Refreshed $n cached copies OpenEmu launches from."
echo "OpenEmu's Ichor now runs this build ($(git rev-parse --short HEAD)). Launch it from the library as usual."
