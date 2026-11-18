#!/usr/bin/env bash
# Fishing at water the fishing audit opened, in game:
#
#   tools/ichor/tests/fishing.sh [rom] [out] [spots]
#
#   rom    default pokeemerald.gba (its .elf must sit beside it)
#   out    default build/test_fishing
#   spots  default "route8 kirrha neraida route12" (see fishing.lua)
#
# First runs tools/ichor/fishing_audit.py. Then, for each spot, a fresh run of
# fishing.lua: quickstart, the Old Rod on SELECT, a warp to the shore, and casts
# until something bites and its battle starts. Screenshots: <spot>_0_shore.png,
# _1_bite.png, _2_hooked.png, _3_battle.png. Nothing in the ROM is patched.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
OUT="${2:-build/test_fishing}"
SPOTS="${3:-route8 kirrha neraida route12}"
ELF="${ROM%.gba}.elf"
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "FISH FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "$OUT" && rm -f "$OUT"/*.png

/usr/bin/python3 tools/ichor/fishing_audit.py || { echo "FISH FAIL: tools/ichor/fishing_audit.py"; exit 1; }

export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)
RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "FISH FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
  -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$OUT/consts.s" tools/ichor/tests/fishing_consts.c \
  || { echo "FISH FAIL: could not compile fishing_consts.c"; exit 1; }
LUA="$OUT/symbols.lua"
{
  echo "return {"
  awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
       n && /\.word/  { print "  " n " = " $2 ","; n = "" }
       n && /\.short/ { print "  " n " = " $2 ","; n = "" }' "$OUT/consts.s"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gSaveBlock1Ptr|gSaveBlock2Ptr|gTasks|Task_Fishing|gIsFishingEncounter)$/ \
    && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$LUA"

fail=0
for spot in $SPOTS; do
  log="$OUT/$spot.log"
  FISH_OUT="$OUT/" FISH_SYMBOLS="$LUA" FISH_SPOT="$spot" "$TIMEOUT" 600 "$RUNNER" \
    --script tools/ichor/tests/fishing.lua --frames 40000 --until "finished" "$ROM" > "$log" 2>&1
  grep -o "FISH $spot \(ok\|PASS\|FAIL\).*" "$log"
  CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
  if grep -qiE "$CRASH" "$log"; then echo "FISH FAIL: crash-like errors in $log"; fail=1; fi
  if ! grep -q "FISH $spot PASS" "$log"; then echo "FISH FAIL: $spot (see $log)"; fail=1; fi
done
[ $fail = 0 ] && echo "FISH PASS: $(ls "$OUT"/*.png | wc -l | tr -d ' ') screenshots in $OUT/"
exit $fail
