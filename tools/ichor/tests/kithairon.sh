#!/usr/bin/env bash
# The Kithairon crossing check (Act II beats 26-29):
#
#   tools/ichor/tests/kithairon.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts, gives a test Pokémon and Demeter's Sickle (the relic stub), warps
# to Route 6 below the vines, and plays north with key presses: the vines, the
# herald, the road's trainers, Eleutherai's plinth, the maenads' dancing floor,
# Phorbas's fold, the Kronia's greeter, Kleon at the tables and the reader; then
# Antiope's cave. Screenshots land in build/test_kithairon/shots/; the run fails
# on any failed check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_kithairon/
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "KITH FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "${OUT}shots" && rm -f "${OUT}"shots/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "KITH FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# The slice's symbols (slice_lib.lua's needs), then this test's constants and the
# crossing's event scripts, by name, merged into one table.
tools/ichor/tests/slice_symbols.sh "$ELF" "${OUT}slice_symbols.lua" || { echo "KITH FAIL: no symbols"; exit 1; }
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "${OUT}consts.s" tools/ichor/tests/kithairon_consts.c \
  || { echo "KITH FAIL: could not compile kithairon_consts.c"; exit 1; }
{
  echo "local S = dofile(\"${OUT}slice_symbols.lua\")"
  echo "local X = {"
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "${OUT}consts.s"
  echo "}"
  echo "for k, v in pairs(X) do S[k] = v end"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Route6_EleutheraiRoad|Route6_AntiopesCave|Eleutherai|MtKithairon|Route7_KroniaGrounds)_EventScript_[A-Za-z0-9_]+$/ { print "S.SCRIPTS." $3 " = 0x" $1 }'
  echo "return S"
} > "${OUT}symbols.lua"

KITH_OUT="$OUT" ${TIMEOUT:+$TIMEOUT 1500} "$RUNNER" --script tools/ichor/tests/kithairon.lua \
  --frames 400000 --until "KITH done" "$ROM" > "${OUT}run.log" 2>&1
code=$?
grep -o "KITH \(ok\|FAIL\|BUG\|NOTE\).*" "${OUT}run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "${OUT}run.log"; then
  echo "KITH FAIL: crash-like errors in ${OUT}run.log"; exit 1
fi
if grep -q "KITH FAIL\|KITH BUG" "${OUT}run.log" || ! grep -q "KITH done" "${OUT}run.log"; then
  echo "KITH FAIL: see ${OUT}run.log (runner exit $code)"; exit 1
fi
echo "KITH PASS: $(ls "${OUT}"shots/*.png | wc -l | tr -d ' ') screenshots in ${OUT}shots/"
