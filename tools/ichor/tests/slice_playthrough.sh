#!/usr/bin/env bash
# The playthrough: one continuous run from a fresh cartridge through the Phase 1
# slice and on through the actual roads and Hollow to Eleusa, with key presses only.
# Demeter and the sanctum still have separate fixtures, not continuous coverage.
#
#   tools/ichor/tests/slice_playthrough.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Env: SLICE_STARTER 0 Nebrel (default) / 1 Kynder / 2 Hipling
#      SLICE_GENDER  theo (default) / ianthe
#      SLICE_DIFFICULTY mortal / hero (default) / spartan, chosen at the water clock
#      SLICE_NATURAL=1  no strength assist; rejects memory writes, RAM scripts,
#                    SLICE_FROM and SLICE_WORKAROUNDS; the button-only team pilot
#                    measures its own strategy, not a balance verdict
#      SLICE_STOP_AFTER a beat name: explicitly partial coverage, never a full PASS
#      SLICE_OUT     output folder (default build/slice/; natural mode uses
#                    build/slice-natural/<difficulty>-<starter>/)
#      SLICE_FROM    a beat name (e.g. 07_temple): resume from the save state an
#                    earlier full run left at that beat, for fixing one beat fast
#      SLICE_WORKAROUNDS=1  release a softlocked waitmovement (logged as a BUG) and
#                    play on, to see past a known blocker; the run still fails
#
# What it plays (tools/ichor/tests/slice_playthrough.lua has the detail): the
# title, the OPTION menu (fast text, battle scene off, Set style), NEW GAME,
# Daphne's speech and naming; the bedroom, the water clock, Mom and the Talaria,
# Kydippe, the Akademia note and the shepherd's gate, Halia's reading, the
# Akademia and the starter, Kleon's battle, Alethea; every item and gift in
# Elaia; Route 1's six trainers, items and gifts; the flock; Kronion Hill's
# summit scene and both grunts, and its high pastures' three herders and items; Akti's arrival, the Asclepeion heal, a SAVE,
# a reset and CONTINUE; the Agora, the Fisher's house, the harbor's people and
# items; the Hearth Trial with all three acolytes; Ione, the Hearth Laurel and
# TM42; the harbor ending; and Akti after the end. Then Phase 2 as far as it is
# built: batch 1 (Halia's second look, the winds, the Euploia's crossing and
# Aigina) and batch 2, Emporion: beat 11 on the quay, the harbor and the city,
# every room (beat 12 in the Deigma, beat 13 at the forge), beat 14 on the temple
# stair, the Isthmus Gate shut, the Temple of Hermes (the Herald's Run, its three
# acolytes, Kerykos, the Herald Laurel and TM40), and beat 16, Kleon at the gate.
# Then the actual Isthmus slide and its Hammer rewards, Hecate's Torch, the
# western Hollow, cliff-road trainers and real healers, and Krokis's Eleusa arrival.
#
# THE ONE ASSIST (unless SLICE_NATURAL=1): after the starter screen the starter's
# experience is set to level 100's (battle strength only; see the .lua header).
# Everything else is button presses. PARTY lines record actual species, levels,
# experience and HP before and after each battle.
#
# Checks at every beat: the map, the music actually playing (the BGM player's
# song, not just the map's), the story flags and vars, items landing in the bag
# once, required trainer victories (both authored rival losses permit
# progression), battle music, and that the player always gets control back. Writes:
#   <out>shots/NNNN_<beat>_<name>.png   a screenshot per moment, in play order
#   <out>states/<beat>.ss               an mGBA save state at the start of each beat
#   <out>run.log                        the full log (TEXT lines hold every message)
#   <out>text.txt                       every message the run saw, decoded, with width checks
# Exit status is non-zero on any failed check, a crash, a stuck scene or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
NATURAL="${SLICE_NATURAL:-0}"
DIFFICULTY="${SLICE_DIFFICULTY:-hero}"
STARTER="${SLICE_STARTER:-0}"
case "$NATURAL" in 0|1) ;; *) echo "SLICE FAIL: SLICE_NATURAL must be 0 or 1"; exit 1 ;; esac
case "$DIFFICULTY" in mortal|hero|spartan) ;; *) echo "SLICE FAIL: unknown SLICE_DIFFICULTY"; exit 1 ;; esac
case "$STARTER" in 0|1|2) ;; *) echo "SLICE FAIL: SLICE_STARTER must be 0, 1 or 2"; exit 1 ;; esac
case "${SLICE_GENDER:-theo}" in theo|ianthe) ;; *) echo "SLICE FAIL: SLICE_GENDER must be theo or ianthe"; exit 1 ;; esac
if [ "$NATURAL" = 1 ] && { [ -n "${SLICE_FROM:-}" ] || [ "${SLICE_WORKAROUNDS:-0}" != 0 ]; }; then
  echo "SLICE FAIL: natural runs cannot resume save states or use workarounds"; exit 1
fi
beat_line() {
  awk -F '"' -v name="$1" '$1 == "beat(" && $2 == name { print NR; found = 1; exit }
                         END { if (!found) exit 1 }' tools/ichor/tests/slice_playthrough.lua
}
if [ -n "${SLICE_FROM:-}" ]; then
  first=$(beat_line "$SLICE_FROM") || { echo "SLICE FAIL: unknown beat $SLICE_FROM"; exit 1; }
fi
if [ -n "${SLICE_STOP_AFTER:-}" ]; then
  last=$(beat_line "$SLICE_STOP_AFTER") || { echo "SLICE FAIL: unknown beat $SLICE_STOP_AFTER"; exit 1; }
  if [ -n "${SLICE_FROM:-}" ] && [ "$first" -gt "$last" ]; then
    echo "SLICE FAIL: requested beat range is not in play order"; exit 1
  fi
fi
DEFAULT_OUT=build/slice/
if [ "$NATURAL" = 1 ]; then DEFAULT_OUT="build/slice-natural/$DIFFICULTY-$STARTER/"; fi
OUT="${SLICE_OUT:-$DEFAULT_OUT}"
OUT="${OUT%/}/"
[ -f "$ROM" ] && [ -f "$ELF" ] || { echo "SLICE FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)
mkdir -p "${OUT}shots" "${OUT}states"
# SLICE_FROM=<beat> resumes from that beat's save state (left by an earlier full run)
if [ -z "${SLICE_FROM:-}" ]; then rm -f "${OUT}"shots/*.png "${OUT}"states/*.ss; fi

# The Lua-capable headless runner (built by smoke_test.sh's rule).
RUNNER=build/tools/ichor-mgba-headless
SRC=tools/ichor/mgba_headless.c
if [ ! -x "$RUNNER" ] || [ "$SRC" -nt "$RUNNER" ]; then
  MGBA_PREFIX=$(brew --prefix mgba) || { echo "SLICE FAIL: needs Homebrew mgba"; exit 1; }
  mkdir -p build/tools
  cc -O2 -I"$MGBA_PREFIX/include" "$SRC" -L"$MGBA_PREFIX/lib" -lmgba -o "$RUNNER" || exit 1
fi

tools/ichor/tests/slice_symbols.sh "$ELF" "${OUT}symbols.lua" || { echo "SLICE FAIL: no symbols"; exit 1; }

start=$(date +%s)
SLICE_NATURAL="$NATURAL" SLICE_DIFFICULTY="$DIFFICULTY" SLICE_STARTER="$STARTER" \
SLICE_OUT="$OUT" SLICE_SYMBOLS="${OUT}symbols.lua" ${TIMEOUT:+$TIMEOUT 2400} "$RUNNER" \
  --script tools/ichor/tests/slice_playthrough.lua --frames 900000 --until "SLICE done" "$ROM" > "${OUT}run.log" 2>&1
code=$?
secs=$(( $(date +%s) - start ))

grep -o "SLICE \(ok\|FAIL\|BUG\|FINDING\|NOTE\|BEAT\|BATTLE\|PARTY\|PILOT\|REACHED\|note\).*" "${OUT}run.log"
report=0
python3 tools/ichor/tests/slice_text_report.py "${OUT}run.log" > "${OUT}text.txt" || report=$?
grep -E "^(WIDE|SUMMARY)" "${OUT}text.txt"

fail=0
if [ "$report" -ne 0 ]; then
  echo "SLICE FAIL: could not decode the playthrough text"; fail=1
fi
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "${OUT}run.log"; then
  echo "SLICE FAIL: crash-like errors in ${OUT}run.log"; grep -iE "$CRASH" "${OUT}run.log" | head -5; fail=1
fi
if [ "$code" -ne 0 ] || grep -q "SLICE FAIL" "${OUT}run.log" || ! grep -q "SLICE done" "${OUT}run.log"; then
  echo "SLICE FAIL: see ${OUT}run.log (runner exit $code)"; fail=1
elif [ -n "${SLICE_STOP_AFTER:-}" ]; then
  if ! grep -Fq "SLICE PARTIAL PASS $SLICE_STOP_AFTER" "${OUT}run.log" \
     || ! grep -Fq "SLICE REACHED $SLICE_STOP_AFTER" "${OUT}run.log"; then
    echo "SLICE FAIL: requested partial endpoint was not reached"; fail=1
  fi
elif ! grep -q "SLICE PASS" "${OUT}run.log"; then
  echo "SLICE FAIL: the run stopped before the end (runner exit $code)"; fail=1
fi
if [ -z "${SLICE_STOP_AFTER:-}" ] && ! grep -q "SLICE REACHED 20_eleusa_arrival" "${OUT}run.log"; then
  echo "SLICE FAIL: the run never reached Eleusa's actual arrival"; fail=1
fi
# These are the continuous harness's endpoints, not all of Act I's built content.
if [ -z "${SLICE_STOP_AFTER:-}" ] && ! grep -q "Halia sent a gull" "${OUT}text.txt"; then
  echo "SLICE FAIL: the run never reached the end of the slice (Alethea's word from Halia)"; fail=1
fi
# The end of batch 2: Kleon's second battle is over and the Isthmus Gate's
# hoplites let the herald through (beat 16).
if [ -z "${SLICE_STOP_AFTER:-}" ] && ! grep -q "Mind the road past the tombs" "${OUT}text.txt"; then
  echo "SLICE FAIL: the run never reached the end of batch 2 (the Isthmus Gate opening after beat 16)"; fail=1
fi
if [ $fail -eq 0 ]; then
  RESULT="SLICE PASS"
  if [ -n "${SLICE_STOP_AFTER:-}" ]; then RESULT="SLICE PARTIAL PASS through $SLICE_STOP_AFTER"; fi
  echo "$RESULT: $(ls "${OUT}"shots/*.png | wc -l | tr -d ' ') screenshots, $(grep -c ' BATTLE ' "${OUT}run.log") battles," \
       "$(grep -c ' NOTE ' "${OUT}run.log") notes, ${secs}s. Shots in ${OUT}shots/, save states in ${OUT}states/"
fi
exit $fail
