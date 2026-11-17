#!/usr/bin/env bash
# The voyage's transitions check: every map change around Aigina's inn on the
# voyage night, recorded frame by frame.
#
#   tools/ichor/tests/voyage_transitions.sh [rom]      (default: pokeemerald.gba, built first)
#
# Quickstarts a new game, sets the voyage night (off the Euploia at Aigina) and
# warps into the inn (all from voyage_transitions.lua, nothing patched in the
# ROM), then plays:
#   1. out of the inn by its mat onto the street, and back in by the door;
#   2. Endeis, the night by the fire and the warp to the deck;
#   3. beat 10C on deck and the Euploia making Emporion's quay.
# Each leg's frames land in build/test_voyage_transitions/<leg>/ with a
# frames.csv. The run fails on a warp seen un-faded, anyone popping more than
# a tile with the screen lit, a wrong arrival tile or facing, a crash or a
# timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_voyage_transitions
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "VOYAGE FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "$OUT"
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

# The Lua-capable headless runner (built by smoke_test.sh's rule).
RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "VOYAGE FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# Constants and offsets from the game's headers, and addresses from the ELF,
# written as a Lua table the test loads.
LUA="$OUT/symbols.lua"
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$OUT/consts.s" tools/ichor/tests/voyage_transitions_consts.c \
  || { echo "VOYAGE FAIL: could not compile voyage_transitions_consts.c"; exit 1; }
{
  echo "return {"
  # A zero constant is emitted as .space rather than .word.
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "$OUT/consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gMain|gSaveBlock1Ptr|gSaveBlock2Ptr|gMapHeader|gObjectEvents|gPlayerAvatar|gTasks|CB2_Overworld|ScrCmd_createmon|sGlobalScriptContextStatus|sLockFieldControls|sFieldMessageBoxMode|Task_HandleScrollingMultichoiceInput)$/ \
    { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$LUA"

VOYAGE_OUT="$OUT/" VOYAGE_SYMBOLS="$LUA" "$TIMEOUT" 900 "$RUNNER" \
  --script tools/ichor/tests/voyage_transitions.lua --frames 60000 \
  --until "VOYAGE done" "$ROM" > "$OUT/run.log" 2>&1
code=$?
grep -o "VOYAGE \(ok\|FAIL\|jump\|the\|Emporion\|recording\).*" "$OUT/run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$OUT/run.log"; then
  echo "VOYAGE FAIL: crash-like errors in $OUT/run.log"; exit 1
fi
if grep -q "VOYAGE FAIL" "$OUT/run.log" || ! grep -q "VOYAGE done" "$OUT/run.log"; then
  echo "VOYAGE FAIL: see $OUT/run.log (runner exit $code)"; exit 1
fi
echo "VOYAGE PASS: frames in $OUT/"
