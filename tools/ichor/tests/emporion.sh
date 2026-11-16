#!/usr/bin/env bash
# Emporion's check: the city and its harbor district, beats 11, 14 and 16.
#
#   tools/ichor/tests/emporion.sh [rom]      (default: pokeemerald.gba, built first)
#
# Quickstarts a new game, gives a strong test Pokémon, and runs the end of beat
# 10C (Ichor_EventScript_EuploiaMakesEmporion), all from emporion.lua with
# nothing patched in the ROM. Then, with key presses:
#   1. beat 11 on the quay: Kleon's sprint, Kerykos and the herm (the altar menu
#      sends MAKE AN OFFERING back to PRAY), the oil, the Trowel, the dig;
#   2. the harbor: every person, sign, item and hidden item, the ferry's menu,
#      the hiring hall's door, and the deck's ferry to Emporion's berth;
#   3. up the harbor road into the city (the seam), every door in the city (each
#      warps to its registered interior), the Agora's people and stalls, Number
#      Nine, Sykeas's snatcher, the jars, the herm, the signs and items;
#   4. beat 14 on the temple stair, the Isthmus Gate before the Herald Laurel,
#      then beat 16, Kleon's second battle, after it; and back down to the quay.
# Screenshots land in build/emporion_test/; the run fails on any failed check, a
# crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/emporion_test
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "EMPORION FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png
. tools/ichor/tests/harness.sh
harness_prepare || exit 1

# Constants and offsets from the game's headers, and addresses from the ELF
# (static symbols included), written as a Lua table the test loads.
LUA="$OUT/symbols.lua"
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$OUT/consts.s" tools/ichor/tests/emporion_consts.c \
  || { echo "EMPORION FAIL: could not compile emporion_consts.c"; exit 1; }
{
  echo "return {"
  # A zero constant is emitted as .space rather than .word.
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "$OUT/consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gMain|gSaveBlock1Ptr|gSaveBlock2Ptr|gSaveBlock3Ptr|gMapHeader|gObjectEvents|gPlayerAvatar|gTasks|gBattleOutcome|CB2_Overworld|BattleMainCB2|ScrCmd_createmon|sGlobalScriptContextStatus|sLockFieldControls|sFieldMessageBoxMode|Task_HandleScrollingMultichoiceInput|Task_HandleMultichoiceInput|Task_HandleYesNoInput|Task_ShopMenu|Task_BuyMenu|Task_BuyHowManyDialogueHandleInput|Task_CallYesOrNoCallback|EmporionCity_Mart_Offerings|Ichor_EventScript_EuploiaMakesEmporion|Ichor_EventScript_FerryDeck)$/ \
    { print "  " $3 " = 0x" $1 "," }'
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(sDig|gRngValue|gParties|gPartiesCount|gBattleMons|gBattlerControllerFuncs|gBagPosition|Task_BagMenu_HandleInput|CB2_NamingScreen)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$LUA"
tools/ichor/tests/slice_symbols.sh "$ELF" "$OUT/battle_symbols.lua" \
  || { echo "EMPORION FAIL: could not resolve the player battle controller"; exit 1; }

/usr/bin/python3 tools/ichor/tests/emporion_grids.py > "$OUT/grids.lua" \
  || { echo "EMPORION FAIL: could not write the walk grids"; exit 1; }

"$TIMEOUT" 1500 "$RUNNER" --script tools/ichor/tests/emporion.lua --frames 400000 \
  --until "EMPORION done" "$ROM" > "$OUT/run.log" 2>&1
code=$?
harness_result EMPORION "$OUT/run.log" "$code" || exit 1
grep -o "EMPORION \(ok\|FAIL\).*" "$OUT/run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$OUT/run.log"; then
  echo "EMPORION FAIL: crash-like errors in $OUT/run.log"; exit 1
fi
if grep -q "EMPORION FAIL" "$OUT/run.log" || ! grep -q "EMPORION done" "$OUT/run.log"; then
  echo "EMPORION FAIL: see $OUT/run.log (runner exit $code)"; exit 1
fi
echo "EMPORION PASS: $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
