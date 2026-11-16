#!/usr/bin/env bash
# Genuine NEW GAME -> Kleon -> Alethea -> Mom, all three starters and difficulties.
# This is prologue coverage, not Kalliste/Act I balance approval.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
OUT="${SLICE_OUT:-build/slice-natural-opening/}"
OUT="${OUT%/}/"
if [ -n "${SLICE_FROM:-}" ] || [ "${SLICE_WORKAROUNDS:-0}" != 0 ]; then
  echo "NATURAL OPENING FAIL: cannot resume fixtures or use workarounds"
  exit 1
fi

fails=0
for difficulty in mortal hero spartan; do
  for starter in 0 1 2; do
    dir="$OUT$difficulty-$starter/"
    mkdir -p "$dir"
    if SLICE_NATURAL=1 SLICE_DIFFICULTY="$difficulty" SLICE_STARTER="$starter" \
       SLICE_STOP_AFTER=04_elaia_after SLICE_OUT="$dir" \
       tools/ichor/tests/slice_playthrough.sh "$ROM" > "${dir}summary.log" 2>&1; then
      echo "NATURAL OPENING PASS: $difficulty starter $starter (partial through 04_elaia_after)"
    else
      echo "NATURAL OPENING FAIL: $difficulty starter $starter; see ${dir}summary.log"
      tail -12 "${dir}summary.log"
      fails=$((fails + 1))
    fi
  done
done
if [ "$fails" -eq 0 ]; then
  echo "NATURAL OPENING PASS: all 9 prologues; full natural-level chapter balance remains open"
fi
exit "$fails"
