#!/usr/bin/env bash
# Side checks for the slice: the things one playthrough can't cover.
#
#   tools/ichor/tests/slice_sidechecks.sh [rom]     (run slice_playthrough.sh first: it leaves the save states;
#                                                   while a blocker stands, run it with SLICE_WORKAROUNDS=1)
#
# Env: CHECKS_ONLY  a comma-separated list of checks (default: all)
#      CHECKS_OUT   output folder (default build/slice_checks/)
#
# Each check loads a beat's save state from build/slice/states/ and plays one
# thing with key presses (tools/ichor/tests/slice_sidechecks.lua has the list):
#   well_twice               Elaia's well gives the Relic Copper once, and nobody vanishes
#   whiteout_*               whiting out in Elaia, on Route 1, on Kronion Hill, in Akti
#                            before and after the first heal, in the Temple, after the end
#   trial_flame_whiteout     the torch is reset when the player comes back in
#   reentry_*                no scene replays on leaving and re-entering a map
#   ending_after_leaving_akti  the ending still plays after a trip indoors mid-scene
#   lose_to_ione, lose_to_petros  losing a story battle, coming back and winning
#   menus                    every start-menu screen, screenshotted for the look review
# A known softlock is released here (and logged as a BUG) so later checks still run.
# Prints "CHECK RESULT <name>: clean | N finding(s)", "CHECK BUG ..." per finding and
# "CHECK FAIL <name>: ..." when a check could not finish. Exit status is non-zero on
# any finding or failure.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
OUT="${CHECKS_OUT:-build/slice_checks/}"
[ -f "$ROM" ] || { echo "CHECK FAIL: $ROM missing (run make first)"; exit 1; }
[ -f build/slice/states/08_after.ss ] && [ -f build/slice/symbols.lua ] \
  || { echo "CHECK FAIL: no save states through 08_after (run tools/ichor/tests/slice_playthrough.sh first; while a blocker stands, with SLICE_WORKAROUNDS=1)"; exit 1; }
TIMEOUT=$(command -v gtimeout || command -v timeout)
mkdir -p "${OUT}shots"
rm -f "${OUT}"shots/*.png
RUNNER=build/tools/ichor-mgba-headless
[ -x "$RUNNER" ] || { echo "CHECK FAIL: $RUNNER missing (run tools/ichor/smoke_test.sh once)"; exit 1; }

CHECKS_OUT="$OUT" ${TIMEOUT:+$TIMEOUT 2400} "$RUNNER" --script tools/ichor/tests/slice_sidechecks.lua \
  --frames 900000 --until "CHECK SUMMARY" "$ROM" > "${OUT}run.log" 2>&1
code=$?
grep -o "CHECK \(RESULT\|BUG\|FAIL\|SUMMARY\|NOTE\|note\).*" "${OUT}run.log"
python3 tools/ichor/tests/slice_text_report.py "${OUT}run.log" > "${OUT}text.txt" || true
grep -E "^(WIDE|TALL|HOENN|WORD\?|SUMMARY)" "${OUT}text.txt"
grep -q "CHECK SUMMARY" "${OUT}run.log" || { echo "CHECK FAIL: the checks did not finish (runner exit $code)"; exit 1; }
if grep -q "CHECK \(BUG\|FAIL\)" "${OUT}run.log"; then exit 1; fi
echo "CHECK PASS: every side check is clean"
