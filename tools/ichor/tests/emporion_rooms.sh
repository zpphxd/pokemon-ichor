#!/usr/bin/env bash
# Emporion's interiors check: every room's event, played from a Quickstart.
#
#   tools/ichor/tests/emporion_rooms.sh [rom]      (default: pokeemerald.gba, built first)
#
# Quickstarts a new game, gives a party (a Swampert to win with, an Onotis to
# trade, and the Harpeck, Chelonet and Stachyss Euphronios paints) and the
# arrival flag, then warps into each room through its door (all from
# emporion_rooms.lua, nothing patched in the ROM) and plays it with key presses:
#   1. the Asclepeion: the healer across the counter, the Panacoil, the Pithos;
#   2. the Deigma: beat 12 (the forty lamps, the notice), then Thaletas's trade
#      of the Narkeray SOCRATES for the Onotis;
#   3. the Hephaisteion: beat 13 with Akti's Charcoal, the forge lit, the Bronze
#      Hammer, and the forge still lit on re-entry;
#   4. the Dolphin: knucklebones with Myrtale until her first loss, then
#      Strepsiades;
#   5. Philoxenos's house: the table heals, and a story for the Herald Laurel;
#   6. the widow's house: the Sea Incense;
#   7. Euphronios's workshop: three paintings and their pay;
#   8. the hiring hall: the crew boss's battle and Rocky Helmet, then the hall
#      empty after Act I and the ledger left open;
#   9. the runners' house: the Quick Claw, then the letter home after Act I.
# Screenshots land in build/emporion_rooms/; the run fails on any failed check,
# a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/emporion_rooms
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "EMPORION FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

# The Lua-capable headless runner (built by smoke_test.sh's rule).
RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "EMPORION FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# Constants and offsets from the game's headers, and addresses from the ELF
# (static symbols included), written as a Lua table the test loads.
LUA="$OUT/symbols.lua"
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$OUT/consts.s" tools/ichor/tests/emporion_rooms_consts.c \
  || { echo "EMPORION FAIL: could not compile emporion_rooms_consts.c"; exit 1; }
{
  echo "return {"
  # A zero constant is emitted as .space rather than .word.
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "$OUT/consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gMain|gSaveBlock1Ptr|gSaveBlock2Ptr|gSaveBlock3Ptr|gMapHeader|gObjectEvents|gPlayerAvatar|gParties|gTasks|gBackupMapLayout|CB2_Overworld|CB2_PokeStorage|ScrCmd_createmon|sGlobalScriptContextStatus|sLockFieldControls|sFieldMessageBoxMode|Task_HandleScrollingMultichoiceInput)$/ \
    { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$LUA"

"$TIMEOUT" 1500 "$RUNNER" --script tools/ichor/tests/emporion_rooms.lua --frames 400000 \
  --until "EMPORION done" "$ROM" > "$OUT/run.log" 2>&1
code=$?
grep -o "EMPORION \(ok\|FAIL\).*" "$OUT/run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$OUT/run.log"; then
  echo "EMPORION FAIL: crash-like errors in $OUT/run.log"; exit 1
fi
if grep -q "EMPORION FAIL" "$OUT/run.log" || ! grep -q "EMPORION done" "$OUT/run.log"; then
  echo "EMPORION FAIL: see $OUT/run.log (runner exit $code)"; exit 1
fi
echo "EMPORION PASS: $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
