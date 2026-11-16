#!/usr/bin/env bash
# Aegina Town check:
#
#   tools/ichor/tests/aegina_town.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts a new game and plays beat 10B's arrival on Aigina's quay at night
# (the scripted warp from the deck, as warp 0), then visits every person, sign,
# hidden item and door in town on the voyage night, and again after the crossing
# (the gate open, Nausikles the ferry). Screenshots land in build/test_aegina/; the
# run fails on any failed check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_aegina
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "AEGINA FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png
. tools/ichor/tests/harness.sh
harness_prepare || exit 1

# Constants and offsets from the game's headers, and addresses from the ELF,
# written as a Lua table the test loads.
LUA="$OUT/symbols.lua"
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$OUT/consts.s" tools/ichor/tests/aegina_town_consts.c \
  || { echo "AEGINA FAIL: could not compile aegina_town_consts.c"; exit 1; }
{
  echo "return {"
  # A zero constant is emitted as .space rather than .word.
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "$OUT/consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gObjectEvents|gPlayerAvatar|gBackupMapLayout|gTimeOfDay|sGlobalScriptContextStatus|sLockFieldControls)$/ \
    { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$LUA"

AEGINA_OUT="$OUT/" AEGINA_SYMBOLS="$LUA" "$TIMEOUT" 900 "$RUNNER" \
  --script tools/ichor/tests/aegina_town.lua --frames 60000 --until "AEGINA done" "$ROM" > "$OUT/run.log" 2>&1
code=$?
harness_result AEGINA "$OUT/run.log" "$code" || exit 1
grep -o "AEGINA \(ok\|FAIL\).*" "$OUT/run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$OUT/run.log"; then
  echo "AEGINA FAIL: crash-like errors in $OUT/run.log"; exit 1
fi
if grep -q "AEGINA FAIL" "$OUT/run.log" || ! grep -q "AEGINA done" "$OUT/run.log"; then
  echo "AEGINA FAIL: see $OUT/run.log (runner exit $code)"; exit 1
fi
echo "AEGINA PASS: $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
