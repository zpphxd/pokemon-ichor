#!/usr/bin/env bash
# Thyrsa's and Eleutherai's interiors, in the game:
#
#   tools/ichor/tests/thyrsa_rooms.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Runs tools/ichor/tests/thyrsa_rooms.lua in the Lua headless runner: a tour of the
# thirteen rooms and their services. Screenshots land in build/test_thyrsa_rooms/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
OUT=build/test_thyrsa_rooms
[ -f "$ROM" ] || { echo "ROOMS FAIL: $ROM missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png
TIMEOUT=$(command -v gtimeout || command -v timeout)

RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "ROOMS FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

ROOMS_OUT="$OUT/" "$TIMEOUT" 600 "$RUNNER" --script tools/ichor/tests/thyrsa_rooms.lua \
  --frames 40000 --until "ROOMS done" "$ROM" > "$OUT/run.log" 2>&1
code=$?
grep -o "ROOMS \(ok\|FAIL\|PASS\).*" "$OUT/run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$OUT/run.log"; then
  echo "ROOMS FAIL: crash-like errors in $OUT/run.log"; exit 1
fi
if grep -q "ROOMS FAIL" "$OUT/run.log" || ! grep -q "ROOMS PASS" "$OUT/run.log"; then
  echo "ROOMS FAIL: see $OUT/run.log (runner exit $code)"; exit 1
fi
echo "ROOMS PASS: $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
