#!/usr/bin/env bash
# Aigina's interior check (the Aphaia Road, Mount Oros, the Temple of Aphaia):
#
#   tools/ichor/tests/aigina_interior.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts a new game, opens Act II's Aigina stop, and walks the detour on foot
# from Aigina Town's gate: up the road to the fork, up Mount Oros and back, up the
# steps to the temple, and home down the east terraces. On the way it picks up
# every item, reads every sign and altar, talks to the placeholder people and
# anoints the herm (aigina_interior.lua has the route). Screenshots land in
# build/test_aigina_interior/; the run fails on any failed check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_aigina_interior
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "AIGINA FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png
. tools/ichor/tests/harness.sh
harness_prepare || exit 1

# Constants and offsets from the game's headers, and addresses from the ELF,
# written as a Lua table the test loads.
LUA="$OUT/symbols.lua"
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$OUT/consts.s" tools/ichor/tests/aigina_interior_consts.c \
  || { echo "AIGINA FAIL: could not compile aigina_interior_consts.c"; exit 1; }
{
  echo "return {"
  # A zero constant is emitted as .space rather than .word.
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "$OUT/consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gMain|gSaveBlock1Ptr|gSaveBlock2Ptr|gObjectEvents|gPlayerAvatar|gBackupMapLayout|gParties|gPartiesCount|CB2_Overworld|CB2_LoadMap|sGlobalScriptContextStatus|sLockFieldControls)$/ \
    { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$LUA"

AIGINA_OUT="$OUT/" AIGINA_SYMBOLS="$LUA" "$TIMEOUT" 900 "$RUNNER" \
  --script tools/ichor/tests/aigina_interior.lua --frames 80000 --until "AIGINA done" "$ROM" > "$OUT/run.log" 2>&1
code=$?
harness_result AIGINA "$OUT/run.log" "$code" || exit 1
grep -o "AIGINA \(ok\|FAIL\|PASS\).*" "$OUT/run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$OUT/run.log"; then
  echo "AIGINA FAIL: crash-like errors in $OUT/run.log"; exit 1
fi
if grep -q "AIGINA FAIL" "$OUT/run.log" || ! grep -q "AIGINA PASS" "$OUT/run.log"; then
  echo "AIGINA FAIL: see $OUT/run.log (runner exit $code)"; exit 1
fi
echo "AIGINA PASS: $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
