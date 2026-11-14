#!/usr/bin/env bash
# Aegina's homes check: the inn's night scene, Pheidon's trade and Aiakides's Black Belt.
#
#   tools/ichor/tests/aegina_homes.sh [rom]      (default: pokeemerald.gba, built first)
#
# Quickstarts a new game, gives a Karkipool and sets the voyage night's arrival
# flag, then warps into each room (all from aegina_homes.lua, nothing patched in
# the ROM) and plays it with key presses:
#   1. the inn: Endeis, "Ready for bed?", the night by the fire (the second
#      answer to Kleon), Kleon up the ladder, the heal and the warp to the deck;
#      then a later visit, where Endeis heals;
#   2. the mint: Pheidon's trade, the Karkipool for Stater, and the Karkipool
#      on guard afterwards;
#   3. Aiakides's house: his story without an Ergant, then the Black Belt with one.
# Screenshots land in build/aegina_homes/; the run fails on any failed check, a
# crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/aegina_homes
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "AEGINA FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

# The Lua-capable headless runner (built by smoke_test.sh's rule).
RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "AEGINA FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# Constants and offsets from the game's headers, and addresses from the ELF
# (static symbols included), written as a Lua table the test loads.
LUA="$OUT/symbols.lua"
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$OUT/consts.s" tools/ichor/tests/aegina_homes_consts.c \
  || { echo "AEGINA FAIL: could not compile aegina_homes_consts.c"; exit 1; }
{
  echo "return {"
  # A zero constant is emitted as .space rather than .word.
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "$OUT/consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gMain|gSaveBlock1Ptr|gSaveBlock2Ptr|gMapHeader|gObjectEvents|gPlayerAvatar|gParties|gTasks|CB2_Overworld|CB2_PokeStorage|ScrCmd_createmon|sGlobalScriptContextStatus|sLockFieldControls|sFieldMessageBoxMode|sHoursOverride|sCurrentMapMusic|Task_HandleScrollingMultichoiceInput)$/ \
    { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$LUA"

"$TIMEOUT" 900 "$RUNNER" --script tools/ichor/tests/aegina_homes.lua --frames 200000 \
  --until "AEGINA done" "$ROM" > "$OUT/run.log" 2>&1
code=$?
grep -o "AEGINA \(ok\|FAIL\).*" "$OUT/run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$OUT/run.log"; then
  echo "AEGINA FAIL: crash-like errors in $OUT/run.log"; exit 1
fi
if grep -q "AEGINA FAIL" "$OUT/run.log" || ! grep -q "AEGINA done" "$OUT/run.log"; then
  echo "AEGINA FAIL: see $OUT/run.log (runner exit $code)"; exit 1
fi
echo "AEGINA PASS: $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
