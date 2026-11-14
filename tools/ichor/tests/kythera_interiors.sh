#!/usr/bin/env bash
# Kythera's and Melos's interiors, toured in game:
#
#   tools/ichor/tests/kythera_interiors.sh [rom]   (default: pokeemerald.gba; run make first)
#
# Runs tools/ichor/tests/kythera_interiors.lua in the Lua headless runner.
# Screenshots land in build/test_kythera/; the run fails on a failed check, a
# crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
OUT=build/test_kythera
[ -f "$ROM" ] || { echo "KYTHERA FAIL: $ROM missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png
TIMEOUT=$(command -v gtimeout || command -v timeout)

RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "KYTHERA FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

KYTHERA_OUT="$OUT/" "$TIMEOUT" 600 "$RUNNER" \
  --script tools/ichor/tests/kythera_interiors.lua --frames 40000 --until "KYTHERA done" "$ROM" > "$OUT/run.log" 2>&1
code=$?
grep -o "KYTHERA \(ok\|FAIL\|PASS\).*" "$OUT/run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$OUT/run.log"; then
  echo "KYTHERA FAIL: crash-like errors in $OUT/run.log"; exit 1
fi
if grep -q "KYTHERA FAIL" "$OUT/run.log" || ! grep -q "KYTHERA done" "$OUT/run.log"; then
  echo "KYTHERA FAIL: see $OUT/run.log (runner exit $code)"; exit 1
fi
echo "KYTHERA PASS: $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
