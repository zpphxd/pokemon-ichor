#!/usr/bin/env bash
# Boot pokeemerald.gba headlessly, play the opening (Daphne's speech, then
# Quickstart after a reset), and save screenshots.
# Usage: tools/ichor/smoke_test.sh [rom]   (default: pokeemerald.gba; its .elf must sit beside it)
# Exit code is non-zero if the ROM is missing, a check fails, the run times out,
# or mGBA logs a crash-like error.
set -u
cd "$(dirname "$0")/../.."
ROM="${1:-pokeemerald.gba}"
[ -f "$ROM" ] || { echo "SMOKE FAIL: $ROM not found (run make first)"; exit 1; }
mkdir -p build/smoke && rm -f build/smoke/*.png
LOG=build/smoke/mgba.log
. tools/ichor/tests/harness.sh
harness_prepare || exit 1

# Elaia's rows nearest the Route 1 seam must stay aethos-only (design/MAP_DESIGN.md).
/usr/bin/python3 tools/ichor/maps/elaia.py --verify >/dev/null \
  || { echo "SMOKE FAIL: Elaia's seam rows (tools/ichor/maps/elaia.py --verify)"; exit 1; }

# Addresses and constants the Lua reads the game's state with.
tools/ichor/tests/elaia_symbols.sh "${ROM%.gba}.elf" build/smoke/symbols.lua \
  || { echo "SMOKE FAIL: could not read symbols from ${ROM%.gba}.elf"; exit 1; }

"$TIMEOUT" 120 "$RUNNER" --script tools/ichor/smoke_test.lua --frames 12000 --until "SMOKE done" "$ROM" >"$LOG" 2>&1
code=$?
harness_result SMOKE "$LOG" "$code" || exit 1
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$LOG"; then
  echo "SMOKE FAIL: crash-like errors in $LOG"; grep -iE "$CRASH" "$LOG" | head -5; exit 1
fi
shots=$(ls build/smoke/*.png 2>/dev/null | wc -l | tr -d ' ')
grep -q "SMOKE done" "$LOG" || { echo "SMOKE FAIL: script did not finish (exit $code). See $LOG"; exit 1; }
if grep -q "SMOKE FAIL" "$LOG"; then grep -o "SMOKE FAIL.*" "$LOG"; exit 1; fi
echo "SMOKE PASS: $shots screenshots in build/smoke/"
