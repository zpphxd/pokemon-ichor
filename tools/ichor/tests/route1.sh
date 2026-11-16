#!/usr/bin/env bash
# Route 1 and Kronion Hill check:
#
#   tools/ichor/tests/route1.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Assembles tools/ichor/tests/route1_setup.s (test-only event scripts, never in
# the ROM) against the ELF's symbols, then runs route1.lua in the Lua headless
# runner: a starter and beat 4's flags, Route 1 and a battle with Tityros, a
# screenshot tour of the route, the flock blocking the road, the Kronion Hill
# summit scene played out, the road open again, and a hop off the goat path's
# last lip with a walk back out past the beaten Agis. Screenshots land in
# build/test_route1/; the run fails on any failed check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_route1
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "ROUTE1 FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png
. tools/ichor/tests/harness.sh
harness_prepare || exit 1

# The setup blob: assembled with the game's macros, linked into spare EWRAM past
# the linker's last EWRAM symbol (near 0x02037480), ROM symbols from the ELF.
BLOB_ADDR=0x0203F000
ASM=tools/ichor/tests/route1_setup.s
harness_assemble "$ASM" "$OUT/setup.o" \
  || { echo "ROUTE1 FAIL: could not assemble $ASM"; exit 1; }
arm-none-eabi-ld -Ttext=$BLOB_ADDR --just-symbols="$ELF" -o "$OUT/setup.elf" "$OUT/setup.o" \
  && arm-none-eabi-objcopy -O binary -j .text "$OUT/setup.elf" "$OUT/setup.bin" \
  || { echo "ROUTE1 FAIL: could not link the setup blob"; exit 1; }
arm-none-eabi-nm "$OUT/setup.elf" | awk '$3 ~ /^Route1Test_.*Header$/ { print $3, $1 }' > "$OUT/setup.syms"

# Constants and offsets from the game's headers, and addresses from the ELF,
# written as a Lua table the test loads.
LUA="$OUT/symbols.lua"
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$OUT/consts.s" tools/ichor/tests/route1_consts.c \
  || { echo "ROUTE1 FAIL: could not compile route1_consts.c"; exit 1; }
{
  echo "return {"
  # A zero constant is emitted as .space rather than .word.
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "$OUT/consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gMain|gSaveBlock1Ptr|gSaveBlock2Ptr|gMapHeader|gObjectEvents|gPlayerAvatar|gBattleOutcome|gSpecialVar_0x8008|gSpecialVar_0x8009|CB2_Overworld|BattleMainCB2|sGlobalScriptContextStatus|sLockFieldControls)$/ \
    { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$LUA"

ROUTE1_OUT="$OUT/" ROUTE1_BLOB_ADDR=$BLOB_ADDR "$TIMEOUT" 900 "$RUNNER" \
  --script tools/ichor/tests/route1.lua --frames 120000 --until "ROUTE1 done" "$ROM" > "$OUT/run.log" 2>&1
code=$?
harness_result ROUTE1 "$OUT/run.log" "$code" || exit 1
grep -o "ROUTE1 \(ok\|FAIL\).*" "$OUT/run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$OUT/run.log"; then
  echo "ROUTE1 FAIL: crash-like errors in $OUT/run.log"; exit 1
fi
if grep -q "ROUTE1 FAIL" "$OUT/run.log" || ! grep -q "ROUTE1 done" "$OUT/run.log"; then
  echo "ROUTE1 FAIL: see $OUT/run.log (runner exit $code)"; exit 1
fi
echo "ROUTE1 PASS: $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
