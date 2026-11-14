#!/usr/bin/env bash
# Write the Lua table of constants, struct offsets and addresses that the slice
# playthrough and its side checks load (tools/ichor/tests/slice_lib.lua).
#
#   tools/ichor/tests/slice_symbols.sh pokeemerald.elf build/slice/symbols.lua
#
# Constants come from compiling slice_consts.c against the game's headers;
# addresses come from the ELF's symbol table (static symbols included).
set -u
cd "$(dirname "$0")/../../.."
ELF="$1"
LUA="$2"
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:$PATH"
mkdir -p "$(dirname "$LUA")"
ASM="${LUA%.lua}.s"
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$ASM" tools/ichor/tests/slice_consts.c \
  || { echo "could not compile slice_consts.c"; exit 1; }
SYMS="gMain gSaveBlock1Ptr gSaveBlock2Ptr gObjectEvents gPlayerAvatar gBackupMapLayout gBattleOutcome
gBattleMons gParties gTasks gMapHeader gBattleTypeFlags gStringVar4 gSpecialVar_Result gSpecialVar_0x8004
gSpecialVar_0x8008 gSpecialVar_0x8009 gMPlayInfo_BGM gSongTable gExperienceTables gSpeciesInfo
sSubstructOffsets sGlobalScriptContextStatus sGlobalScriptContext sLockFieldControls sCurrentMapMusic sFieldMessageBoxMode
sStartMenuCursorPos sNumStartMenuActions sCurrentStartMenuActions gPaletteFade
CB2_Overworld BattleMainCB2 CB2_MainMenu CB2_InitMainMenu CB2_NamingScreen CB2_StarterChoose CB2_WallClock
CB2_EvolutionSceneUpdate CB2_InitTitleScreen CB2_LoadMap CB2_ReturnToField
gBattlerControllerFuncs HandleInputChooseMove
Task_NewGameBirchSpeech_ChooseGender Task_HandleYesNoInput Task_HandleMultichoiceInput
Task_HandleScrollingMultichoiceInput Task_BuyMenu Task_ShopMenu Task_OptionMenuProcessInput
SetCB2WhiteOut SetHiddenNature ScrCmd_createmon"
PATTERN="^($(echo $SYMS | tr ' ' '|'))$"
{
  echo "return {"
  # A zero constant is emitted as .space rather than .word.
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "$ASM"
  # The first definition wins: a static name used in two files would be ambiguous.
  arm-none-eabi-nm "$ELF" | awk -v pat="$PATTERN" '$3 ~ pat && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  # Statics whose name several files use: take the one inside that file's .text
  # (its range from the linker map).
  for want in HandleInputChooseAction@battle_controller_player WaitForMovementFinish@scrcmd; do
    name=${want%@*}; obj=${want#*@}
    set -- $(awk -v o="src/$obj.o" '$1 == ".text" && $4 == o { print $2, $3; exit }' "${ELF%.elf}.map")
    lo=$(( $1 )); hi=$(( $1 + $2 ))
    arm-none-eabi-nm "$ELF" | awk -v n="$name" '$3 == n { print $1 }' | while read -r a; do
      v=$(( 16#$a ))
      [ $v -ge $lo ] && [ $v -lt $hi ] && echo "  $name = 0x$a,"
    done
  done
  # The slice's and Phase 2's maps' event scripts, by name: the tests find people, signs and
  # triggers on the live map by the script they run, never by coordinates.
  echo "  SCRIPTS = {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^((ElaiaVillage|KallisteRoute1|AktiTown|Trireme|Aegina|Emporion|Eleusa|Ichor)[A-Za-z0-9_]*_EventScript_[A-Za-z0-9_]+|Common_EventScript_FindItem)$/ && $3 !~ /_[0-9]+$/ { print "    " $3 " = 0x" $1 "," }'
  echo "  },"
  # Every song's header, by name: several song ids share one header (Ichor
  # re-pointed Hoenn's slots at its own songs), so tests compare headers.
  echo "  SONG_NAMES = {"
  arm-none-eabi-nm "$ELF" | awk '$2 ~ /^[dDrR]$/ && $3 ~ /^mus_[a-z0-9_]+$/ && $3 !~ /_[0-9]+$/ { print "    [0x" $1 "] = \"" $3 "\"," }'
  echo "  },"
  echo "}"
} > "$LUA"
for s in $SYMS HandleInputChooseAction WaitForMovementFinish; do
  grep -q "^  $s = " "$LUA" || { echo "slice_symbols: $s not found in $ELF"; exit 1; }
done
