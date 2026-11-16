#!/usr/bin/env bash
# Check that the Aethos dex is in the ROM: every species' name, base stats,
# types, national dex number and front pic in gSpeciesInfo, the regional dex
# order and the starters (tools/ichor/tests/aethos_dex.lua).
# Usage: tools/ichor/aethos_dex_check.sh [rom]   (default: pokeemerald.gba)
# Builds the runner via smoke_test.sh's rules, so run that once on a fresh checkout.
set -u
cd "$(dirname "$0")/../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/harness.sh
[ -f "$ROM" ] || { echo "AETHOS FAIL: $ROM not found (run make first)"; exit 1; }
harness_prepare || exit 1
mkdir -p build/aethos_dex
export AETHOS_EXPECT=build/aethos_dex/expect.lua
python3 tools/dex/rom/gen.py --expect "$AETHOS_EXPECT" || exit 1
LOG=build/aethos_dex/mgba.log
"$TIMEOUT" 120 "$RUNNER" --script tools/ichor/tests/aethos_dex.lua --frames 600 --until "AETHOS done" "$ROM" >"$LOG" 2>&1
code=$?
harness_result AETHOS "$LOG" "$code" || exit 1
grep "AETHOS" "$LOG" | grep -v "AETHOS done"
grep -q "AETHOS PASS" "$LOG" || { echo "AETHOS CHECK FAIL. See $LOG"; exit 1; }
