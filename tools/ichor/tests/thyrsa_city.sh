#!/usr/bin/env bash
# Thyrsa City check (the thyrsa agent's, Act II batch 1):
#
#   tools/ichor/tests/thyrsa_city.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts, gives a test team and Act II's flags, and warps onto the road below
# the Elektran Gate (nothing patched in the ROM). Then plays beat 30 as a player:
# the gatekeeper's welcome, a tour of the city with a screenshot per district, Manto
# on the Kadmeia wall, the festival guards at the Neistan Gate, the theater keeper;
# then, with the Dionysia over and the Girdle held, the drum pushed out of the
# Neistan Gate, Alethea going west, and the open road. Screenshots land in
# build/test_thyrsa/shots/; the run fails on any failed check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_thyrsa/
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "THYRSA FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "${OUT}shots" && rm -f "${OUT}"shots/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "THYRSA FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# The slice's symbol table, then Thyrsa's constants and scripts on top of it.
tools/ichor/tests/slice_symbols.sh "$ELF" "${OUT}base.lua" || { echo "THYRSA FAIL: slice symbols"; exit 1; }
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "${OUT}consts.s" tools/ichor/tests/thyrsa_city_consts.c \
  || { echo "THYRSA FAIL: could not compile thyrsa_city_consts.c"; exit 1; }
{
  echo "return {"
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "${OUT}consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 == "gSaveBlock3Ptr" { print "  " $3 " = 0x" $1 "," }'
  echo "  SCRIPTS = {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^ThyrsaCity_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ { print "    " $3 " = 0x" $1 "," }'
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

"$TIMEOUT" 900 "$RUNNER" --script tools/ichor/tests/thyrsa_city.lua --frames 200000 \
  --until "THYRSA done" "$ROM" > "${OUT}run.log" 2>&1
code=$?
grep -o "THYRSA \(ok\|FAIL\|NOTE\|BUG\).*" "${OUT}run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "${OUT}run.log"; then
  echo "THYRSA FAIL: crash-like errors in ${OUT}run.log"; exit 1
fi
if grep -q "THYRSA \(FAIL\|BUG\)" "${OUT}run.log" || ! grep -q "THYRSA done" "${OUT}run.log"; then
  echo "THYRSA FAIL: see ${OUT}run.log (runner exit $code)"; exit 1
fi
echo "THYRSA PASS: $(ls "${OUT}"shots/*.png | wc -l | tr -d ' ') screenshots in ${OUT}shots/"
