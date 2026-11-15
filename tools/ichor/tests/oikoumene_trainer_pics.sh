#!/usr/bin/env bash
# The Oikoumene's batch-1 trainer classes: one battle per new class, from the
# intro screen. For each class it checks the class label in gTrainerClasses,
# that the intro line names the trainer with that label, and that the opponent's
# front pic loaded (its palette is in OBJ palette RAM). One screenshot per class.
#
#   tools/ichor/tests/oikoumene_trainer_pics.sh [rom]   (default: pokeemerald.gba; run make first)
#
# The test trainer is an existing slice trainer whose class, pic and name are
# rewritten in the emulator's copy of the ROM for each battle; nothing in the
# ROM file or the shipped data changes. Output in build/test_oik_trainers/,
# with a contact sheet of the intros at build/test_oik_trainers/intros.png.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_oik_trainers
engine_prepare OIKTR "$OUT" tools/ichor/tests/oikoumene_trainer_pics.c tools/ichor/tests/oikoumene_trainer_pics.s
# addresses the shared symbol lists don't have
arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gTrainers|gTrainerClasses|gDisplayedStringBattle)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }' \
  | { echo "return {"; cat; echo "}"; } > "$OUT/oik_symbols.lua"
# what each pic should look like: its palette, from the PNG (a Python with Pillow:
# engine_build.sh puts Homebrew's first on PATH, which may not have it)
PY=
for p in /usr/bin/python3 python3; do "$p" -c "import PIL" 2>/dev/null && { PY=$p; break; }; done
[ -n "$PY" ] || { echo "OIKTR FAIL: needs a python3 with Pillow"; exit 1; }
"$PY" tools/ichor/tests/oikoumene_trainer_pics.py expect "$OUT/expect.lua" || exit 1
engine_run OIKTR "$OUT" tools/ichor/tests/oikoumene_trainer_pics.lua 60000 600
"$PY" tools/ichor/tests/oikoumene_trainer_pics.py sheet "$OUT"
