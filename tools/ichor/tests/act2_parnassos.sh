#!/usr/bin/env bash
# Lebadeia and Route 9, the Split Road (the parnassos agent's, Act II batch 2):
#
#   tools/ichor/tests/act2_parnassos.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts, gives a test team, the Girdle and Act II's flags, and warps onto the
# road at Lebadeia's east gate (nothing patched in the ROM). Then plays beats 35B-36
# as a player: the arrival, Alethea at the springs, Saon and the grille, the hamlet;
# west onto the Split Road: Koretas, the bands, Onomarchos, the crossroads scene, the
# herm, Psephos and Apollo's shrine, the laurel; the north-west fork to the lookout
# (the scene, Xenodike, the fig, the Max Revive); the treasury's drums pushed into
# the gully with the Girdle and the ruin's finds; the terraces, Lykoreus, the road
# down to Kirrha; the omen's Enigmaw. Screenshots land in build/test_parnassos/shots/;
# the run fails on any failed check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_parnassos/
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "PARN FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "${OUT}shots" && rm -f "${OUT}"shots/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "PARN FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# The slice's symbol table, then this test's constants and the two maps' scripts.
tools/ichor/tests/slice_symbols.sh "$ELF" "${OUT}base.lua" || { echo "PARN FAIL: slice symbols"; exit 1; }
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "${OUT}consts.s" tools/ichor/tests/act2_parnassos_consts.c \
  || { echo "PARN FAIL: could not compile act2_parnassos_consts.c"; exit 1; }
{
  echo "return {"
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "${OUT}consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 == "gSaveBlock3Ptr" { print "  " $3 " = 0x" $1 "," }'
  echo "  SCRIPTS = {"
  arm-none-eabi-nm "$ELF" | awk '($3 ~ /^(Lebadeia|Route9_Schiste)_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/) || $3 == "EventScript_StrengthBoulder" { print "    " $3 " = 0x" $1 "," }'
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

"$TIMEOUT" 1500 "$RUNNER" --script tools/ichor/tests/act2_parnassos.lua --frames 400000 \
  --until "PARN done" "$ROM" > "${OUT}run.log" 2>&1
code=$?
grep -o "PARN \(ok\|FAIL\|NOTE\|BUG\).*" "${OUT}run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "${OUT}run.log"; then
  echo "PARN FAIL: crash-like errors in ${OUT}run.log"; exit 1
fi
if grep -q "PARN \(FAIL\|BUG\)" "${OUT}run.log" || ! grep -q "PARN done" "${OUT}run.log"; then
  echo "PARN FAIL: see ${OUT}run.log (runner exit $code)"; exit 1
fi
echo "PARN PASS: $(ls "${OUT}"shots/*.png | wc -l | tr -d ' ') screenshots in ${OUT}shots/"
