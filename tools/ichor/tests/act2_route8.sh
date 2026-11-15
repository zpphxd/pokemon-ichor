#!/usr/bin/env bash
# Route 8, the Kopais shore (Act II beat 35A; the kopais agent's, batch 2):
#
#   tools/ichor/tests/act2_route8.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts, gives a test team, the Girdle of Herakles, Olive Oil and Fresh Water
# (nothing patched in the ROM), and warps onto the road at Route 8's east edge. Then
# plays the road west as a player: Alethea's five notes, the five trainers, the
# eel-smoker's rest, the dike and its jetty, the great herm, the decoy traveler, the
# Treasury of Minyas behind its column drum, the Sphinx's ledge and the goat path's
# ledges, the hidden items, and out through the west edge to Lebadeia. Screenshots
# land in build/test_route8/shots/; the run fails on any failed check, a crash or a
# timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_route8/
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "ROUTE8 FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "${OUT}shots" && rm -f "${OUT}"shots/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "ROUTE8 FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# The slice's symbol table, then Route 8's constants and scripts on top of it.
tools/ichor/tests/slice_symbols.sh "$ELF" "${OUT}base.lua" || { echo "ROUTE8 FAIL: slice symbols"; exit 1; }
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "${OUT}consts.s" tools/ichor/tests/act2_route8_consts.c \
  || { echo "ROUTE8 FAIL: could not compile act2_route8_consts.c"; exit 1; }
{
  echo "return {"
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "${OUT}consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 == "gSaveBlock3Ptr" { print "  " $3 " = 0x" $1 "," }'
  echo "  SCRIPTS = {"
  arm-none-eabi-nm "$ELF" | awk '($3 ~ /^Route8_Kopais_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/) || $3 == "EventScript_StrengthBoulder" { print "    " $3 " = 0x" $1 "," }'
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

"$TIMEOUT" 1200 "$RUNNER" --script tools/ichor/tests/act2_route8.lua --frames 300000 \
  --until "ROUTE8 done" "$ROM" > "${OUT}run.log" 2>&1
code=$?
grep -o "ROUTE8 \(ok\|FAIL\|NOTE\|BUG\).*" "${OUT}run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "${OUT}run.log"; then
  echo "ROUTE8 FAIL: crash-like errors in ${OUT}run.log"; exit 1
fi
if grep -q "ROUTE8 \(FAIL\|BUG\)" "${OUT}run.log" || ! grep -q "ROUTE8 done" "${OUT}run.log"; then
  echo "ROUTE8 FAIL: see ${OUT}run.log (runner exit $code)"; exit 1
fi
echo "ROUTE8 PASS: $(ls "${OUT}"shots/*.png | wc -l | tr -d ' ') screenshots in ${OUT}shots/"
