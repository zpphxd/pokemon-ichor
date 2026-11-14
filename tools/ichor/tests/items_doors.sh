#!/usr/bin/env bash
# Item icons, the ground jar and door animations, in game:
#
#   tools/ichor/tests/items_doors.sh [rom] [out] [mode]
#
#   rom   default pokeemerald.gba (its .elf must sit beside it)
#   out   default build/test_items_doors
#   mode  all (default), or doors: only the door walks, for comparing an older ROM
#
# Compiles items_doors_consts.c with the game's headers into a Lua table, then
# runs items_doors.lua in the Lua headless runner. It walks through every
# animated door on the slice's maps (and the aethos doors no map uses yet,
# written into Akti's grid), photographs the ground jars where the maps put
# them, fills the bag with the slice's items and pages through every pocket,
# and opens the Agora's buy list. Nothing in the ROM is patched.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
OUT="${2:-build/test_items_doors}"
MODE="${3:-all}"
ELF="${ROM%.gba}.elf"
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "ITEMS FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "ITEMS FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$OUT/consts.s" tools/ichor/tests/items_doors_consts.c \
  || { echo "ITEMS FAIL: could not compile items_doors_consts.c"; exit 1; }
LUA="$OUT/symbols.lua"
{
  echo "return {"
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.short/ { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "$OUT/consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gMain|gSaveBlock1Ptr|gSaveBlock2Ptr|gBackupMapLayout|CB2_LoadMap|CB2_Overworld)$/ \
    { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$LUA"

ITEMS_OUT="$OUT/" ITEMS_SYMBOLS="$LUA" ITEMS_MODE="$MODE" "$TIMEOUT" 900 "$RUNNER" \
  --script tools/ichor/tests/items_doors.lua --frames 60000 --until "ITEMS done" "$ROM" > "$OUT/run.log" 2>&1
code=$?
grep -o "ITEMS \(ok\|FAIL\).*" "$OUT/run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$OUT/run.log"; then
  echo "ITEMS FAIL: crash-like errors in $OUT/run.log"; exit 1
fi
if grep -q "ITEMS FAIL" "$OUT/run.log" || ! grep -q "ITEMS done" "$OUT/run.log"; then
  echo "ITEMS FAIL: see $OUT/run.log (runner exit $code)"; exit 1
fi
echo "ITEMS PASS: $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
