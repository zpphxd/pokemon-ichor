#!/usr/bin/env bash
# Write the Lua table of constants, struct offsets and addresses that the opening
# test and the smoke test load.
#
#   tools/ichor/tests/elaia_symbols.sh pokeemerald.elf build/elaia_opening/symbols.lua
#
# Constants come from compiling elaia_opening_consts.c against the game's headers;
# addresses come from the ELF's symbol table (static symbols included).
set -u
cd "$(dirname "$0")/../../.."
ELF="$1"
LUA="$2"
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:$PATH"
mkdir -p "$(dirname "$LUA")"
ASM="${LUA%.lua}.s"
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$ASM" tools/ichor/tests/elaia_opening_consts.c \
  || { echo "could not compile elaia_opening_consts.c"; exit 1; }
{
  echo "return {"
  # A zero constant is emitted as .space rather than .word.
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "$ASM"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gMain|gSaveBlock1Ptr|gSaveBlock2Ptr|gObjectEvents|gPlayerAvatar|gBackupMapLayout|gBattleOutcome|gBattleMons|gParties|gTasks|CB2_Overworld|BattleMainCB2|CB2_MainMenu|CB2_NamingScreen|CB2_StarterChoose|CB2_WallClock|Task_NewGameBirchSpeech_ChooseGender|Task_HandleTruckSequence|sGlobalScriptContextStatus|sLockFieldControls|sCurrentMapMusic|gMapHeader|SetCB2WhiteOut)$/ \
    { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$LUA"
