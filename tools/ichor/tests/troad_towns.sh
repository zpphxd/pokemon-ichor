#!/usr/bin/env bash
# The Troad's towns and lane: Sestos, the Hellespont and Ilion.
#
#   tools/ichor/tests/troad_towns.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Assembles tools/ichor/tests/troad_towns_setup.s (test-only event scripts, never
# in the ROM) against the ELF's symbols, writes the maps' doors, signs, hidden
# items and people from their map.json (troad_towns.py), then runs
# troad_towns.lua in the Lua headless runner: land at Sestos and play Alethea's
# quay scene once; walk every door in Sestos and Ilion into its room; read every
# sign and take every hidden item on all three maps; talk to the townsfolk;
# fight Kotys on the Hellespont's strip; take the beach elder's gift; ride the
# current; surf east to the Bosporus seam and back; and sail home with Nausikles.
# Screenshots land in build/test_troad_towns/; the run fails on any failed
# check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_troad_towns
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "TROAD FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

# The Lua-capable headless runner (built by smoke_test.sh's rule).
RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "TROAD FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# The maps' doors, signs, hidden items and people, and the constants they name.
/usr/bin/python3 tools/ichor/tests/troad_towns.py "$OUT" > /dev/null \
  || { echo "TROAD FAIL: could not write the maps' data"; exit 1; }

# The setup blob: assembled with the game's macros, linked into spare EWRAM past
# the linker's last EWRAM symbol, ROM symbols from the ELF.
BLOB_ADDR=0x0203F000
ASM=tools/ichor/tests/troad_towns_setup.s
tools/preproc/preproc -s "$ASM" charmap.txt \
  | arm-none-eabi-cpp -iquote include -Wno-trigraphs -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -I include - \
  | tools/preproc/preproc -ie "$ASM" charmap.txt \
  | arm-none-eabi-as -mcpu=arm7tdmi -march=armv4t -meabi=5 --defsym MODERN=1 --defsym EMERALD=1 -o "$OUT/setup.o" \
  || { echo "TROAD FAIL: could not assemble $ASM"; exit 1; }
arm-none-eabi-ld -Ttext=$BLOB_ADDR --just-symbols="$ELF" -o "$OUT/setup.elf" "$OUT/setup.o" \
  && arm-none-eabi-objcopy -O binary -j .text "$OUT/setup.elf" "$OUT/setup.bin" \
  || { echo "TROAD FAIL: could not link the setup blob"; exit 1; }
arm-none-eabi-nm "$OUT/setup.elf" | awk '$3 ~ /^TroadTest_.*Header$/ { print $3, $1 }' > "$OUT/setup.syms"

# Constants and offsets from the game's headers, and addresses from the ELF.
LUA="$OUT/symbols.lua"
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$OUT/consts.s" "$OUT/consts.c" \
  || { echo "TROAD FAIL: could not compile the constants"; exit 1; }
{
  echo "return {"
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "$OUT/consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gMain|gSaveBlock1Ptr|gSaveBlock2Ptr|gSaveBlock3Ptr|gMapHeader|gObjectEvents|gPlayerAvatar|gBattleOutcome|gSpecialVar_0x8008|gSpecialVar_0x8009|CB2_Overworld|BattleMainCB2|sGlobalScriptContextStatus|sLockFieldControls)$/ \
    { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$LUA"

TROAD_OUT="$OUT/" TROAD_BLOB_ADDR=$BLOB_ADDR "$TIMEOUT" 1500 "$RUNNER" \
  --script tools/ichor/tests/troad_towns.lua --frames 300000 --until "TROAD done" "$ROM" > "$OUT/run.log" 2>&1
code=$?
grep -o "TROAD \(ok\|FAIL\).*" "$OUT/run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$OUT/run.log"; then
  echo "TROAD FAIL: crash-like errors in $OUT/run.log"; exit 1
fi
if grep -q "TROAD FAIL" "$OUT/run.log" || ! grep -q "TROAD done" "$OUT/run.log"; then
  echo "TROAD FAIL: see $OUT/run.log (runner exit $code)"; exit 1
fi
echo "TROAD PASS: $(grep -c 'TROAD ok' "$OUT/run.log") checks, $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
