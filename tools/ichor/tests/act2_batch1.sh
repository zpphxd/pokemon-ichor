#!/usr/bin/env bash
# Act II batch 1's check (design/phase3/BUILD.md, Tests): beats 26-34, the Kithairon
# crossing and Thyrsa, as one batch.
#
#   tools/ichor/tests/act2_batch1.sh [rom]          the joins: audit and walk
#   tools/ichor/tests/act2_batch1.sh --all [rom]    and every agent's own test too
#
# 1. tools/ichor/act2/audit_batch1.py checks, from the map.json files, that every
#    warp and connection between the agents' maps joins up both ways, that the
#    Asclepeion's respawn stands at its door, and that every trainer has a party.
# 2. act2_batch1.lua walks those joins in the game: Route 6 north across every seam
#    to Thyrsa, in and out of every door, through the theater to the skene, and back
#    south. Screenshots land in build/test_act2_batch1/shots/.
# 3. With --all, the batch's own tests play the beats themselves: kithairon.sh
#    (26-29), thyrsa_city.sh (30), act2_temple.sh (31), thyrsa_rooms.sh (the
#    interiors) and act2_dionysia.sh (32-34).
set -u
cd "$(dirname "$0")/../../.."
ALL=0
[ "${1:-}" = "--all" ] && { ALL=1; shift; }
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_act2_batch1/
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "B1 FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
python3 tools/ichor/act2/audit_batch1.py | grep -v "^NOTE" || { echo "B1 FAIL: the audit failed"; exit 1; }
mkdir -p "${OUT}shots" && rm -f "${OUT}"shots/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "B1 FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# The slice's symbols (slice_lib.lua's needs), then this test's constants and the
# crossing's event scripts, by name, merged into one table.
tools/ichor/tests/slice_symbols.sh "$ELF" "${OUT}slice_symbols.lua" || { echo "B1 FAIL: no symbols"; exit 1; }
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "${OUT}consts.s" tools/ichor/tests/act2_batch1_consts.c \
  || { echo "B1 FAIL: could not compile act2_batch1_consts.c"; exit 1; }
{
  echo "local S = dofile(\"${OUT}slice_symbols.lua\")"
  echo "local X = {"
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "${OUT}consts.s"
  echo "}"
  echo "for k, v in pairs(X) do S[k] = v end"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Route6_EleutheraiRoad|Eleutherai|MtKithairon|Route7_KroniaGrounds|ThyrsaCity|ThyrsaTheater)_EventScript_[A-Za-z0-9_]+$/ { print "S.SCRIPTS." $3 " = 0x" $1 }'
  echo "return S"
} > "${OUT}symbols.lua"

B1_OUT="$OUT" ${TIMEOUT:+$TIMEOUT 1500} "$RUNNER" --script tools/ichor/tests/act2_batch1.lua \
  --frames 400000 --until "B1 done" "$ROM" > "${OUT}run.log" 2>&1
code=$?
grep -o "B1 \(ok\|FAIL\|BUG\|NOTE\).*" "${OUT}run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "${OUT}run.log"; then
  echo "B1 FAIL: crash-like errors in ${OUT}run.log"; exit 1
fi
if grep -q "B1 FAIL\|B1 BUG" "${OUT}run.log" || ! grep -q "B1 done" "${OUT}run.log"; then
  echo "B1 FAIL: see ${OUT}run.log (runner exit $code)"; exit 1
fi
echo "B1 PASS: $(ls "${OUT}"shots/*.png | wc -l | tr -d ' ') screenshots in ${OUT}shots/"
[ "$ALL" = 1 ] || exit 0
for t in kithairon thyrsa_city act2_temple thyrsa_rooms act2_dionysia; do
  tools/ichor/tests/$t.sh "$ROM" | tail -1
  [ "${PIPESTATUS[0]}" = 0 ] || { echo "B1 FAIL: $t.sh failed"; exit 1; }
done
echo "B1 PASS: the joins and all five of the batch's own tests"
