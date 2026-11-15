#!/usr/bin/env bash
# The Gulf crossing check (the harbors agent's, Act II batch 2: beat 37):
#
#   tools/ichor/tests/act2_harbors.sh [rom]      (default: pokeemerald.gba; run make first)
#
# Quickstarts, gives a test team and the flags of the road west so far, and warps onto
# Kirrha's north road where Route 9 comes in (nothing patched in the ROM). Then plays
# beat 37 as a player: Alethea's arrival above the harbor, the pilgrims' gate and its
# guards, the Kronist's reading, the beggar (a decoy), the harbor's people, signs and
# hidden things; Panopeus and the crossing (Route 10: Alethea at the stern, both
# trainers, the goats, the rail, the hidden scale); the landing at Aigion (beat 37C),
# the grove-keeper's heal, the altar of Zeus, the fisher and the drowned town; and the
# ferry back to Kirrha. Screenshots land in build/test_harbors/shots/; the run fails on
# any failed check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/test_harbors/
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "HARBORS FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "${OUT}shots" && rm -f "${OUT}"shots/*.png
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "HARBORS FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

# The slice's symbol table, then the crossing's constants and scripts on top of it.
tools/ichor/tests/slice_symbols.sh "$ELF" "${OUT}base.lua" || { echo "HARBORS FAIL: slice symbols"; exit 1; }
arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "${OUT}consts.s" tools/ichor/tests/act2_harbors_consts.c \
  || { echo "HARBORS FAIL: could not compile act2_harbors_consts.c"; exit 1; }
{
  echo "return {"
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.space/ { print "  " n " = 0,"; n = "" }' "${OUT}consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 == "gSaveBlock3Ptr" { print "  " $3 " = 0x" $1 "," }'
  echo "  SCRIPTS = {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Kirrha|GulfFerry_Deck|Aigion)_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ { print "    " $3 " = 0x" $1 "," }'
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

"$TIMEOUT" 1200 "$RUNNER" --script tools/ichor/tests/act2_harbors.lua --frames 260000 \
  --until "HARBORS done" "$ROM" > "${OUT}run.log" 2>&1
code=$?
grep -o "HARBORS \(ok\|FAIL\|NOTE\|BUG\).*" "${OUT}run.log"
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "${OUT}run.log"; then
  echo "HARBORS FAIL: crash-like errors in ${OUT}run.log"; exit 1
fi
if grep -q "HARBORS \(FAIL\|BUG\)" "${OUT}run.log" || ! grep -q "HARBORS done" "${OUT}run.log"; then
  echo "HARBORS FAIL: see ${OUT}run.log (runner exit $code)"; exit 1
fi
echo "HARBORS PASS: $(ls "${OUT}"shots/*.png | wc -l | tr -d ' ') screenshots in ${OUT}shots/"
