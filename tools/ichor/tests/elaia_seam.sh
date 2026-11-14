#!/usr/bin/env bash
# The Route 1 / Elaia seam, seen in game from both sides (see elaia_seam.lua).
#
#   tools/ichor/tests/elaia_seam.sh [rom]      (default: pokeemerald.gba, built first)
#
# Screenshots land in build/elaia_seam/. tools/ichor/maps/elaia.py separately
# fails if Elaia's rows nearest the seam use anything but aethos metatiles.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
OUT=build/elaia_seam
[ -f "$ROM" ] && [ -f "${ROM%.gba}.elf" ] || { echo "SEAM FAIL: $ROM or its .elf missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png
TIMEOUT=$(command -v gtimeout || command -v timeout)
RUNNER=build/tools/ichor-mgba-headless
[ -x "$RUNNER" ] || { echo "SEAM FAIL: run tools/ichor/smoke_test.sh once to build $RUNNER"; exit 1; }
tools/ichor/tests/elaia_symbols.sh "${ROM%.gba}.elf" "$OUT/symbols.lua" || { echo "SEAM FAIL: no symbols"; exit 1; }
SEAM_OUT="$OUT/" SEAM_SYMBOLS="$OUT/symbols.lua" "$TIMEOUT" 120 "$RUNNER" --script tools/ichor/tests/elaia_seam.lua \
  --frames 20000 --until "SEAM done" "$ROM" > "$OUT/run.log" 2>&1
grep -o "SEAM \(ok\|FAIL\|shot\).*" "$OUT/run.log"
if grep -q "SEAM FAIL" "$OUT/run.log" || ! grep -q "SEAM done" "$OUT/run.log"; then
  echo "SEAM FAIL: see $OUT/run.log"; exit 1
fi
echo "SEAM PASS: $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
