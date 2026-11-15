#!/usr/bin/env bash
# The road west's nine interiors, in the game (Act II batch 2, the rooms2 agent):
#
#   tools/ichor/tests/act2_westrooms.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts, gives a Halcyling and a Lophops, and tours all nine rooms with their
# people in place, playing what each one offers: the pilgrims' hall's heal and its
# respawn after a whiteout; Herkyna's goose home and her Mystic Water; Agamedes's
# loose stone; the inn's heal and respawn, Pylades's fig and Focus Sash; the stall's
# shop; the muleteer's trade; Thyia's laurel; Tisamenos's bird; Helike's bell; the two
# hidden items. Screenshots land in build/test_westrooms/shots/; the run fails on any
# failed check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_westrooms/
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "WEST FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "${OUT}shots" && rm -f "${OUT}"shots/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "WEST FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# The slice's symbols (slice_lib.lua's needs), then this test's constants and the
# rooms' event scripts, by name, merged into one table.
tools/ichor/tests/slice_symbols.sh "$ELF" "${OUT}slice_symbols.lua" || { echo "WEST FAIL: no symbols"; exit 1; }
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "${OUT}consts.s" tools/ichor/tests/act2_westrooms_consts.c \
  || { echo "WEST FAIL: could not compile act2_westrooms_consts.c"; exit 1; }
{
  echo "local S = dofile(\"${OUT}slice_symbols.lua\")"
  echo "local X = {"
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "${OUT}consts.s"
  echo "}"
  echo "for k, v in pairs(X) do S[k] = v end"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Lebadeia|Kirrha|Aigion)_[A-Za-z]+_EventScript_[A-Za-z0-9_]+$/ { print "S.SCRIPTS." $3 " = 0x" $1 }'
  arm-none-eabi-nm "$ELF" | awk '$3 == "SetCB2WhiteOut" || $3 == "ScrCmd_createmon" || $3 == "CB2_PokeStorage" { print "S." $3 " = S." $3 " or 0x" $1 }'
  echo "return S"
} > "${OUT}symbols.lua"

WEST_OUT="$OUT" ${TIMEOUT:+$TIMEOUT 1500} "$RUNNER" --script tools/ichor/tests/act2_westrooms.lua \
  --frames 400000 --until "WEST done" "$ROM" > "${OUT}run.log" 2>&1
code=$?
grep -o "WEST \(ok\|FAIL\|BUG\|NOTE\).*" "${OUT}run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "${OUT}run.log"; then
  echo "WEST FAIL: crash-like errors in ${OUT}run.log"; exit 1
fi
if grep -q "WEST FAIL\|WEST BUG" "${OUT}run.log" || ! grep -q "WEST done" "${OUT}run.log"; then
  echo "WEST FAIL: see ${OUT}run.log (runner exit $code)"; exit 1
fi
echo "WEST PASS: $(ls "${OUT}"shots/*.png | wc -l | tr -d ' ') screenshots in ${OUT}shots/"
