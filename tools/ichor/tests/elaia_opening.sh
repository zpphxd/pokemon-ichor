#!/usr/bin/env bash
# The opening check: plays a new game from Daphne's speech to the road north,
# once per starter.
#
#   tools/ichor/tests/elaia_opening.sh [rom]      (default: pokeemerald.gba, built first)
#
# Each run starts a real NEW GAME (no Quickstart): Daphne's speech, Theo, the
# naming screen, waking on 2F, the water clock, Mom and the Talaria, Halia's
# reading, the Akademia and the starter, Kleon taking his, the battle in the
# square, Alethea's heal and Poke Balls, and the walk north onto Route 1.
#   run 1: Nebrel,  Kleon on 1 HP:  a win  (Kleon takes Kynder)
#   run 2: Kynder,  played straight: either outcome (Kleon takes Hipling)
#   run 3: Hipling, the player on 1 HP: a loss (Kleon takes Nebrel), and the story goes on
# Screenshots land in build/elaia_opening/<starter>/; the run fails on any failed
# check, a crash or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT=build/elaia_opening
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "ELAIA FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
mkdir -p "$OUT"
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)

# The Lua-capable headless runner (built by smoke_test.sh's rule).
RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "ELAIA FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

tools/ichor/tests/elaia_symbols.sh "$ELF" "$OUT/symbols.lua" || { echo "ELAIA FAIL: no symbols"; exit 1; }

fails=0
for run in "0 win nebrel" "1 any kynder" "2 lose hipling"; do
  set -- $run
  dir="$OUT/$3"
  mkdir -p "$dir" && rm -f "$dir"/*.png
  ELAIA_STARTER=$1 ELAIA_OUTCOME=$2 ELAIA_OUT="$dir/" ELAIA_SYMBOLS="$OUT/symbols.lua" \
    "$TIMEOUT" 600 "$RUNNER" --script tools/ichor/tests/elaia_opening.lua --frames 150000 \
    --until "ELAIA done" "$ROM" > "$dir/run.log" 2>&1
  code=$?
  grep -o "ELAIA \(ok\|FAIL\|note\).*" "$dir/run.log" | sed "s/^/[$3] /"
  CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
  if grep -qiE "$CRASH" "$dir/run.log"; then
    echo "ELAIA FAIL [$3]: crash-like errors in $dir/run.log"; fails=1
  elif grep -q "ELAIA FAIL" "$dir/run.log" || ! grep -q "ELAIA done" "$dir/run.log"; then
    echo "ELAIA FAIL [$3]: see $dir/run.log (runner exit $code)"; fails=1
  else
    echo "ELAIA PASS [$3]: $(ls "$dir"/*.png | wc -l | tr -d ' ') screenshots in $dir/"
  fi
done
exit $fails
