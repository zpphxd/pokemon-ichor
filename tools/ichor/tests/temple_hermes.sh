#!/usr/bin/env bash
# The Herald's Run check: plays the Temple of Hermes from the door to the Herald Laurel.
#
#   tools/ichor/tests/temple_hermes.sh [rom]      (default: pokeemerald.gba, built first)
#
# Quickstarts a new game, gives a test team and warps into the temple (all from
# temple_hermes.lua, nothing patched in the ROM), then plays it with key presses:
# Angelos, the oil jar, Kerykos's rite, a wrong-way turnstile, oiling J1, a step-glass
# that runs dry (back to the door, J1 still oiled), Angelos's hint, then the whole run:
# T1 and Podarge, H1, back west, J2, the turnstile stair, J3, the colonnade's gap and
# Euchidas, H2, the east stair, J4, T5, H3 (the gate opens, the turnstiles turn round,
# every herm faces the dais), Philonides through the turned turnstiles, Kerykos, the
# Herald Laurel, TM40 and the Honey, his short way down, and a re-entry with the room
# still solved. Screenshots land in build/temple_hermes/; the run fails on any failed
# check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/temple_hermes
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "HERMES FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

# The Lua-capable headless runner (built by smoke_test.sh's rule).
RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "HERMES FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# Constants and offsets from the game's headers, and addresses from the ELF (static
# symbols included), written as a Lua table the test loads.
LUA="$OUT/symbols.lua"
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$OUT/consts.s" tools/ichor/tests/temple_hermes_consts.c \
  || { echo "HERMES FAIL: could not compile temple_hermes_consts.c"; exit 1; }
{
  echo "return {"
  # A zero constant is emitted as .space rather than .word.
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "$OUT/consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gMain|gSaveBlock1Ptr|gSaveBlock2Ptr|gSaveBlock3Ptr|gMapHeader|gObjectEvents|gPlayerAvatar|gBackupMapLayout|gBattleOutcome|CB2_Overworld|BattleMainCB2|ScrCmd_createmon|sGlobalScriptContextStatus|sLockFieldControls|sCurrentMapMusic|gMPlayInfo_BGM|gSongTable)$/ \
    { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$LUA"

"$TIMEOUT" 900 "$RUNNER" --script tools/ichor/tests/temple_hermes.lua --frames 200000 \
  --until "HERMES done" "$ROM" > "$OUT/run.log" 2>&1
code=$?
grep -o "HERMES \(ok\|FAIL\).*" "$OUT/run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$OUT/run.log"; then
  echo "HERMES FAIL: crash-like errors in $OUT/run.log"; exit 1
fi
if grep -q "HERMES FAIL" "$OUT/run.log" || ! grep -q "HERMES done" "$OUT/run.log"; then
  echo "HERMES FAIL: see $OUT/run.log (runner exit $code)"; exit 1
fi
echo "HERMES PASS: $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
