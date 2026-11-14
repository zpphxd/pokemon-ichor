#!/usr/bin/env bash
# The Euploia check: plays beat 10 and beat 10C on the trireme's deck and hold.
#
#   tools/ichor/tests/trireme.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Assembles tools/ichor/tests/trireme_setup.s (test-only event scripts, never in
# the ROM) against the ELF's symbols, then runs trireme.lua in the Lua headless
# runner: a new game with beat 9B's flags, up the gangway (the deck's warp 0),
# casting off, a tour of the deck and its people, the hold and back, the items,
# then the whole set piece from Nausikles (the calm, the split reed, Kleon's
# stroke, the klepsydra running backward, the nest, two snatcher battles, the
# hatching, the chick on the hat, the night leg) to Aigina's quay; then beat 10C
# and the ferry. The stub trainers (Phormion, Lykon, Alethea) are never fought.
# Screenshots land in build/test_trireme/; the run fails on any failed check, a
# crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_trireme
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "TRIREME FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

# The Lua-capable headless runner (built by smoke_test.sh's rule).
RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "TRIREME FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# The setup blob: assembled with the game's macros, linked into spare EWRAM past
# the linker's last EWRAM symbol (near 0x02037480), ROM symbols from the ELF.
BLOB_ADDR=0x0203F000
ASM=tools/ichor/tests/trireme_setup.s
tools/preproc/preproc -s "$ASM" charmap.txt \
  | arm-none-eabi-cpp -iquote include -Wno-trigraphs -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -I include - \
  | tools/preproc/preproc -ie "$ASM" charmap.txt \
  | arm-none-eabi-as -mcpu=arm7tdmi -march=armv4t -meabi=5 --defsym MODERN=1 --defsym EMERALD=1 -o "$OUT/setup.o" \
  || { echo "TRIREME FAIL: could not assemble $ASM"; exit 1; }
arm-none-eabi-ld -Ttext=$BLOB_ADDR --just-symbols="$ELF" -o "$OUT/setup.elf" "$OUT/setup.o" \
  && arm-none-eabi-objcopy -O binary -j .text "$OUT/setup.elf" "$OUT/setup.bin" \
  || { echo "TRIREME FAIL: could not link the setup blob"; exit 1; }
arm-none-eabi-nm "$OUT/setup.elf" | awk '$3 ~ /^TriremeTest_.*Header$/ { print $3, $1 }' > "$OUT/setup.syms"

# Constants and offsets from the game's headers, and addresses from the ELF,
# written as a Lua table the test loads.
LUA="$OUT/symbols.lua"
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$OUT/consts.s" tools/ichor/tests/trireme_consts.c \
  || { echo "TRIREME FAIL: could not compile trireme_consts.c"; exit 1; }
{
  echo "return {"
  # A zero constant is emitted as .space rather than .word.
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "$OUT/consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gMain|gSaveBlock1Ptr|gSaveBlock2Ptr|gMapHeader|gObjectEvents|gPlayerAvatar|gBattleOutcome|gSpecialVar_0x8008|gSpecialVar_0x8009|gPlayerPartyCountPtr|CB2_Overworld|BattleMainCB2|sGlobalScriptContextStatus|sLockFieldControls)$/ \
    { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$LUA"

TRIREME_OUT="$OUT/" TRIREME_BLOB_ADDR=$BLOB_ADDR "$TIMEOUT" 1200 "$RUNNER" \
  --script tools/ichor/tests/trireme.lua --frames 160000 --until "TRIREME done" "$ROM" > "$OUT/run.log" 2>&1
code=$?
grep -o "TRIREME \(ok\|FAIL\).*" "$OUT/run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$OUT/run.log"; then
  echo "TRIREME FAIL: crash-like errors in $OUT/run.log"; exit 1
fi
if grep -q "TRIREME FAIL" "$OUT/run.log" || ! grep -q "TRIREME done" "$OUT/run.log"; then
  echo "TRIREME FAIL: see $OUT/run.log (runner exit $code)"; exit 1
fi
echo "TRIREME PASS: $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
