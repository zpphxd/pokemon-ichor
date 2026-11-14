#!/usr/bin/env bash
# Boot pokeemerald.gba headlessly and capture the UI (start menu, dialogue box,
# YES/NO box, options, name box, sign) with tools/ichor/ui_check.lua.
# Usage: tools/ichor/ui_check.sh [rom]   (default: pokeemerald.gba)
# Screenshots go to build/ui_check/. Builds the runner via smoke_test.sh's
# rules, so run tools/ichor/smoke_test.sh once first on a fresh checkout.
set -u
cd "$(dirname "$0")/../.."
ROM="${1:-pokeemerald.gba}"
RUNNER=build/tools/ichor-mgba-headless
[ -f "$ROM" ] || { echo "UI CHECK FAIL: $ROM not found (run make first)"; exit 1; }
[ -x "$RUNNER" ] || { echo "UI CHECK FAIL: $RUNNER missing (run tools/ichor/smoke_test.sh once)"; exit 1; }
mkdir -p build/ui_check && rm -f build/ui_check/*.png
LOG=build/ui_check/mgba.log
TIMEOUT=$(command -v gtimeout || command -v timeout)
# Addresses the Lua pokes to force a name box and a sign frame.
sym() { awk -v s="$1" '$2 == s && $1 ~ /^0x/ { print $1; exit }' pokeemerald.map; }
export UI_SPEAKER_NAME=$(sym gSpeakerName) UI_SPEAKER_TABLE=$(sym gSpeakerNamesTable) UI_MSG_IS_SIGNPOST=$(sym gMsgIsSignPost)
"$TIMEOUT" 120 "$RUNNER" --script tools/ichor/ui_check.lua --frames 6000 --until "UI done" "$ROM" >"$LOG" 2>&1
grep -q "UI done" "$LOG" || { echo "UI CHECK FAIL: script did not finish. See $LOG"; exit 1; }
echo "UI CHECK: $(ls build/ui_check/*.png | wc -l | tr -d ' ') screenshots in build/ui_check/"
