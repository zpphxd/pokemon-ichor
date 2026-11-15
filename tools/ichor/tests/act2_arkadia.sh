#!/usr/bin/env bash
# Arkadia, the Cypress Wood and the Pool of Mnemosyne (Act II beats 41-43, the arkadia
# agent):
#
#   tools/ichor/tests/act2_arkadia.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts, gives a test Pokémon, and arrives in Arkadia from Route 12's road: the dusk
# scene (beat 41) and its lamps; then the town's people, signs, a lost kid, the decoy and
# the hidden Revive, all with key presses; then through the Wood's gate, band 1 and Euadne
# to the stump clearing, where Kleon's new moon (beat 42) and the storm-hound (beat 43)
# play; on through band 2 and Lysippe to the Pool and Mnaseas; and back to Arkadia, where
# Alethea has gone and the temple's gate is open. Screenshots land in
# build/test_arkadia/shots/; the run fails on any failed check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_arkadia/
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "ARKADIA FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "${OUT}shots" && rm -f "${OUT}"shots/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "ARKADIA FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# The slice's symbol table, then the rooms' constants and scripts on top of it.
tools/ichor/tests/slice_symbols.sh "$ELF" "${OUT}base.lua" || { echo "ARKADIA FAIL: slice symbols"; exit 1; }
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "${OUT}consts.s" tools/ichor/tests/act2_arkadia_consts.c \
  || { echo "ARKADIA FAIL: could not compile act2_arkadia_consts.c"; exit 1; }
{
  echo "return {"
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "${OUT}consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 == "gSaveBlock3Ptr" || $3 == "Scrcmd_checkspecies" || $3 == "gPartiesCount" || $3 == "CB2_PokeStorage" \
    { print "  " $3 " = 0x" $1 "," }'
  echo "  SCRIPTS = {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Arkadia|Arkadia_CypressWood|PoolOfMnemosyne|Arkadia_[A-Za-z]+)_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ \
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

"$TIMEOUT" 1500 "$RUNNER" --script tools/ichor/tests/act2_arkadia.lua --frames 400000 \
  --until "ARKADIA done" "$ROM" > "${OUT}run.log" 2>&1
code=$?
grep -o "ARKADIA \(ok\|FAIL\|NOTE\|BUG\).*" "${OUT}run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "${OUT}run.log"; then
  echo "ARKADIA FAIL: crash-like errors in ${OUT}run.log"; exit 1
fi
if grep -q "ARKADIA \(FAIL\|BUG\)" "${OUT}run.log" || ! grep -q "ARKADIA done" "${OUT}run.log"; then
  echo "ARKADIA FAIL: see ${OUT}run.log (runner exit $code)"; exit 1
fi
echo "ARKADIA PASS: $(ls "${OUT}"shots/*.png | wc -l | tr -d ' ') screenshots in ${OUT}shots/"
