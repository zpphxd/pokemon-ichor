#!/usr/bin/env bash
# The Hearth Trial check: plays the Temple of Hestia from the door to the Hearth Laurel.
#
#   tools/ichor/tests/temple_trial.sh [rom]      (default: pokeemerald.gba, built first)
#
# Quickstarts a new game, gives a test team and warps into the temple (all from
# temple_trial.lua, nothing patched in the ROM), then plays the trial: the hymn,
# the torch going out at the door, a wrong brazier, the three acolytes, the right
# order, the last flame home, Ione and her rewards, and a re-entry with the room
# still solved. Screenshots land in build/temple_trial/; the run fails on any
# failed check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/temple_trial
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "TEMPLE FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

# The Lua-capable headless runner (built by smoke_test.sh's rule).
RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "TEMPLE FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# Constants and offsets from the game's headers, and addresses from the ELF,
# written as a Lua table the test loads.
LUA="$OUT/symbols.lua"
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$OUT/consts.s" tools/ichor/tests/temple_trial_consts.c \
  || { echo "TEMPLE FAIL: could not compile temple_trial_consts.c"; exit 1; }
{
  echo "return {"
  # A zero constant is emitted as .space rather than .word.
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "$OUT/consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gMain|gSaveBlock1Ptr|gSaveBlock2Ptr|gMapHeader|gObjectEvents|gPlayerAvatar|gBackupMapLayout|gBattleOutcome|CB2_Overworld|BattleMainCB2|ScrCmd_createmon|sGlobalScriptContextStatus|sLockFieldControls)$/ \
    { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$LUA"

"$TIMEOUT" 600 "$RUNNER" --script tools/ichor/tests/temple_trial.lua --frames 120000 \
  --until "TEMPLE done" "$ROM" > "$OUT/run.log" 2>&1
code=$?
grep -o "TEMPLE \(ok\|FAIL\).*" "$OUT/run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$OUT/run.log"; then
  echo "TEMPLE FAIL: crash-like errors in $OUT/run.log"; exit 1
fi
if grep -q "TEMPLE FAIL" "$OUT/run.log" || ! grep -q "TEMPLE done" "$OUT/run.log"; then
  echo "TEMPLE FAIL: see $OUT/run.log (runner exit $code)"; exit 1
fi
echo "TEMPLE PASS: $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
