#!/usr/bin/env bash
# The playthrough: one continuous run from a fresh cartridge through the Phase 1
# slice and on into Phase 2 as far as it is built, with key presses only.
#
#   tools/ichor/tests/slice_playthrough.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Env: SLICE_STARTER 0 Snivy (default) / 1 Cyndaquil / 2 Piplup
#      SLICE_GENDER  theo (default) / ianthe
#      SLICE_OUT     output folder (default build/slice/)
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
# Elaia; Route 1's five trainers, items and gifts; the flock; Kronion Hill's
# summit scene and both grunts; Akti's arrival, the Asclepeion heal, a SAVE,
# a reset and CONTINUE; the Agora, the Fisher's house, the harbor's people and
# items; the Hearth Trial with all three acolytes; Ione, the Hearth Laurel and
# TM42; the harbor ending; and Akti after the end.
#
# THE ONE ASSIST: after the starter screen the starter's experience is set to
# level 100's (battle strength only; see the .lua header). Everything else is
# button presses.
#
# Checks at every beat: the map, the music actually playing (the BGM player's
# song, not just the map's), the story flags and vars, items landing in the bag
# once, each trainer beaten once and never again, battle music, and that the
# player always gets control back. Writes:
#   <out>shots/NNNN_<beat>_<name>.png   a screenshot per moment, in play order
#   <out>states/<beat>.ss               an mGBA save state at the start of each beat
#   <out>run.log                        the full log (TEXT lines hold every message)
#   <out>text.txt                       every message the run saw, decoded, with width checks
# Exit status is non-zero on any failed check, a crash, a stuck scene or a timeout.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
OUT="${SLICE_OUT:-build/slice/}"
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
SLICE_OUT="$OUT" SLICE_SYMBOLS="${OUT}symbols.lua" ${TIMEOUT:+$TIMEOUT 2400} "$RUNNER" \
  --script tools/ichor/tests/slice_playthrough.lua --frames 900000 --until "SLICE done" "$ROM" > "${OUT}run.log" 2>&1
code=$?
secs=$(( $(date +%s) - start ))

grep -o "SLICE \(ok\|FAIL\|BUG\|FINDING\|NOTE\|BEAT\|BATTLE\|note\).*" "${OUT}run.log"
python3 tools/ichor/tests/slice_text_report.py "${OUT}run.log" > "${OUT}text.txt" || true
grep -E "^(WIDE|SUMMARY)" "${OUT}text.txt"

fail=0
CRASH="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
if grep -qiE "$CRASH" "${OUT}run.log"; then
  echo "SLICE FAIL: crash-like errors in ${OUT}run.log"; grep -iE "$CRASH" "${OUT}run.log" | head -5; fail=1
fi
if grep -q "SLICE FAIL" "${OUT}run.log" || ! grep -q "SLICE done" "${OUT}run.log"; then
  echo "SLICE FAIL: see ${OUT}run.log (runner exit $code)"; fail=1
elif ! grep -q "SLICE PASS" "${OUT}run.log"; then
  echo "SLICE FAIL: the run stopped before the end (runner exit $code)"; fail=1
fi
# Phase 2 replaced the slice's farewell card; the run now ends where Act I's
# built content does (design/phase2/BUILD.md's batches).
if ! grep -q "Halia sent a gull" "${OUT}text.txt"; then
  echo "SLICE FAIL: the run never reached the end of the slice (Alethea's word from Halia)"; fail=1
fi
if [ $fail -eq 0 ]; then
  echo "SLICE PASS: $(ls "${OUT}"shots/*.png | wc -l | tr -d ' ') screenshots, $(grep -c ' BATTLE ' "${OUT}run.log") battles," \
       "$(grep -c ' NOTE ' "${OUT}run.log") notes, ${secs}s. Shots in ${OUT}shots/, save states in ${OUT}states/"
fi
exit $fail
