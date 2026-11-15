#!/usr/bin/env bash
# The interiors of Styx Falls and Arkadia (Act II batch 3, the rooms3 agent):
#
#   tools/ichor/tests/act2_arkrooms.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts, gives a team (a Gelasable first, for the trade), and tours all nine rooms
# with a screenshot each, playing their people and services with key presses: the inn's
# rest and Alethea's one visit, Gryllos, the Cleanse Tag, TM Bulldoze and the Everstone,
# the Asclepeion's heal and the respawn it sets, the Agora's stall, Nyktimos's welcome and
# Black Glasses, the race's finish both ways, Hippothoos's trade, and Krotos's kids. The
# outdoor maps aren't this agent's, so nothing here walks out of a door. Screenshots land
# in build/test_arkrooms/shots/; the run fails on any failed check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_arkrooms/
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "ARKROOMS FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "${OUT}shots" && rm -f "${OUT}"shots/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "ARKROOMS FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# The slice's symbol table, then the rooms' constants and scripts on top of it.
tools/ichor/tests/slice_symbols.sh "$ELF" "${OUT}base.lua" || { echo "ARKROOMS FAIL: slice symbols"; exit 1; }
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "${OUT}consts.s" tools/ichor/tests/act2_arkrooms_consts.c \
  || { echo "ARKROOMS FAIL: could not compile act2_arkrooms_consts.c"; exit 1; }
{
  echo "return {"
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "${OUT}consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 == "gSaveBlock3Ptr" || $3 == "Scrcmd_checkspecies" || $3 == "gPartiesCount" \
    { print "  " $3 " = 0x" $1 "," }'
  echo "  SCRIPTS = {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(StyxFalls|Arkadia)_[A-Za-z]+_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ \
    { print "    " $3 " = 0x" $1 "," }'
  echo "  },"
  echo "}"
} > "${OUT}extra.lua"
cat > "${OUT}symbols.lua" <<EOF
local S = dofile("${OUT}base.lua")
local X = dofile("${OUT}extra.lua")
for k, v in pairs(X) do
  if k == "SCRIPTS" then for a, b in pairs(v) do S.SCRIPTS[a] = b end else S[k] = v end
end
return S
EOF

"$TIMEOUT" 900 "$RUNNER" --script tools/ichor/tests/act2_arkrooms.lua --frames 200000 \
  --until "ARKROOMS done" "$ROM" > "${OUT}run.log" 2>&1
code=$?
grep -o "ARKROOMS \(ok\|FAIL\|NOTE\|BUG\).*" "${OUT}run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "${OUT}run.log"; then
  echo "ARKROOMS FAIL: crash-like errors in ${OUT}run.log"; exit 1
fi
if grep -q "ARKROOMS \(FAIL\|BUG\)" "${OUT}run.log" || ! grep -q "ARKROOMS done" "${OUT}run.log"; then
  echo "ARKROOMS FAIL: see ${OUT}run.log (runner exit $code)"; exit 1
fi
echo "ARKROOMS PASS: $(ls "${OUT}"shots/*.png | wc -l | tr -d ' ') screenshots in ${OUT}shots/"
