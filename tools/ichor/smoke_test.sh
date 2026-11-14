#!/usr/bin/env bash
# Boot pokeemerald.gba headlessly, run the title flow, and save screenshots.
# Usage: tools/ichor/smoke_test.sh [rom]   (default: pokeemerald.gba)
# Exit code is non-zero if the ROM is missing, the run times out, or mGBA
# logs a crash-like error.
set -u
cd "$(dirname "$0")/../.."
ROM="${1:-pokeemerald.gba}"
[ -f "$ROM" ] || { echo "SMOKE FAIL: $ROM not found (run make first)"; exit 1; }
mkdir -p build/smoke && rm -f build/smoke/*.png
LOG=build/smoke/mgba.log
TIMEOUT=$(command -v gtimeout || command -v timeout)

# The bundled tools/mgba runner has no Lua engine, so build our own against
# Homebrew's libmgba (see tools/ichor/mgba_headless.c).
RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba 2>/dev/null) || { echo "SMOKE FAIL: needs Homebrew mgba (brew install mgba)"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || { echo "SMOKE FAIL: could not build $RUNNER"; exit 1; }
fi

"$TIMEOUT" 120 "$RUNNER" --script tools/ichor/smoke_test.lua --frames 6000 "$ROM" >"$LOG" 2>&1
code=$?
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$LOG"; then
  echo "SMOKE FAIL: crash-like errors in $LOG"; grep -iE "$CRASH" "$LOG" | head -5; exit 1
fi
shots=$(ls build/smoke/*.png 2>/dev/null | wc -l | tr -d ' ')
grep -q "SMOKE done" "$LOG" || { echo "SMOKE FAIL: script did not finish (exit $code). See $LOG"; exit 1; }
echo "SMOKE PASS: $shots screenshots in build/smoke/"
