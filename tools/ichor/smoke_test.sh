#!/usr/bin/env bash
# Boot pokeemerald.gba headlessly, play the opening (Daphne's speech, then
# Quickstart after a reset), and save screenshots.
# Usage: tools/ichor/smoke_test.sh [rom]   (default: pokeemerald.gba; its .elf must sit beside it)
# Exit code is non-zero if the ROM is missing, a check fails, the run times out,
# or mGBA logs a crash-like error.
set -u
cd "$(dirname "$0")/../.."
ROM="${1:-pokeemerald.gba}"
[ -f "$ROM" ] || { echo "SMOKE FAIL: $ROM not found (run make first)"; exit 1; }
mkdir -p build/smoke && rm -f build/smoke/*.png
LOG=build/smoke/mgba.log
TIMEOUT=$(command -v gtimeout || command -v timeout)

# The bundled tools/mgba runner has no Lua engine, so build our own against
# Homebrew's libmgba (see tools/ichor/mgba_headless.c).
RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba 2>/dev/null) || { echo "SMOKE FAIL: needs Homebrew mgba (brew install mgba)"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || { echo "SMOKE FAIL: could not build $RUNNER"; exit 1; }
fi

# Elaia's rows nearest the Route 1 seam must stay aethos-only (design/MAP_DESIGN.md).
/usr/bin/python3 tools/ichor/maps/elaia.py --verify >/dev/null \
  || { echo "SMOKE FAIL: Elaia's seam rows (tools/ichor/maps/elaia.py --verify)"; exit 1; }

# A connected neighbour draws with the current map's tilesets: every seam cell the
# camera shows across a connection must look the same under both (MAP_DESIGN.md §5).
/usr/bin/python3 tools/ichor/seam_audit.py \
  || { echo "SMOKE FAIL: seam cells that draw wrong across a connection (tools/ichor/seam_audit.py)"; exit 1; }

# No blocked cell that looks like the open ground beside it, no object without graphics.
/usr/bin/python3 tools/ichor/wall_audit.py \
  || { echo "SMOKE FAIL: invisible walls (tools/ichor/wall_audit.py)"; exit 1; }

# Open water beside reachable land must take a rod, and a map with it needs a fishing table.
/usr/bin/python3 tools/ichor/fishing_audit.py \
  || { echo "SMOKE FAIL: unfishable water (tools/ichor/fishing_audit.py)"; exit 1; }

# Every town with a healer has a travel herm by its entrance (design/MAP_DESIGN.md §7).
/usr/bin/python3 tools/ichor/herm_audit.py \
  || { echo "SMOKE FAIL: a town without its travel herm (tools/ichor/herm_audit.py)"; exit 1; }

# Nobody stands inside a wall or a tree, or under a crown or a capital's top layer.
/usr/bin/python3 tools/ichor/object_audit.py \
  || { echo "SMOKE FAIL: an object inside solid ground or under top-layer art (tools/ichor/object_audit.py)"; exit 1; }

# No starter in the wild, every regular line catchable before the League, the tables as
# planned (design/DISTRIBUTION.md).
/usr/bin/python3 tools/ichor/distribution.py \
  || { echo "SMOKE FAIL: the wild distribution (tools/ichor/distribution.py)"; exit 1; }
/usr/bin/python3 tools/ichor/wild_plan.py --check \
  || { echo "SMOKE FAIL: wild_encounters.json strays from tools/ichor/wild_plan.py"; exit 1; }

# Addresses and constants the Lua reads the game's state with.
tools/ichor/tests/elaia_symbols.sh "${ROM%.gba}.elf" build/smoke/symbols.lua \
  || { echo "SMOKE FAIL: could not read symbols from ${ROM%.gba}.elf"; exit 1; }

"$TIMEOUT" 120 "$RUNNER" --script tools/ichor/smoke_test.lua --frames 12000 --until "SMOKE done" "$ROM" >"$LOG" 2>&1
code=$?
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "$LOG"; then
  echo "SMOKE FAIL: crash-like errors in $LOG"; grep -iE "$CRASH" "$LOG" | head -5; exit 1
fi
shots=$(ls build/smoke/*.png 2>/dev/null | wc -l | tr -d ' ')
grep -q "SMOKE done" "$LOG" || { echo "SMOKE FAIL: script did not finish (exit $code). See $LOG"; exit 1; }
if grep -q "SMOKE FAIL" "$LOG"; then grep -o "SMOKE FAIL.*" "$LOG"; exit 1; fi
echo "SMOKE PASS: $shots screenshots in build/smoke/"
