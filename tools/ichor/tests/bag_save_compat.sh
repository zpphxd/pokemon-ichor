#!/usr/bin/env bash
# Old saves keep their items across the big-Bag layout change (src/item.c,
# Ichor_MigrateBagLayout):
#
#   tools/ichor/tests/bag_save_compat.sh OLD_ROM [REAL_SAVE]
#
#   OLD_ROM    a ROM built before the change (its .elf beside it), e.g. from
#              `git worktree add /tmp/old <commit before the big Bag> && make`
#   REAL_SAVE  optional: a real battery save. Only a copy is ever opened.
#
# 1. The old ROM starts a new game, puts items in every pocket and the PC, and
#    saves. The new ROM CONTINUEs that save: every pocket, the PC, the dex flags
#    and the moved blocks must match, then still match after a save and reset.
# 2. With REAL_SAVE, the old ROM reads a copy and the new ROM migrates another.
# Output in build/test_bag_save/. An old ROM without its .map gets a stub one.
set -u
cd "$(dirname "$0")/../../.."
OLD_ROM="${1:?usage: bag_save_compat.sh OLD_ROM [REAL_SAVE]}"
REAL="${2:-}"
NEW_ROM=pokeemerald.gba
OUT=build/test_bag_save
mkdir -p "$OUT"
. tools/ichor/tests/engine_build.sh

# slice_symbols.sh reads the linker map for two battle and script statics these
# runs never use. An old ROM kept without its map gets a stub that covers them.
if [ ! -f "${OLD_ROM%.gba}.map" ]; then
  mkdir -p "$OUT/oldrom"
  cp "$OLD_ROM" "$OUT/oldrom/old.gba" && cp "${OLD_ROM%.gba}.elf" "$OUT/oldrom/old.elf" || exit 1
  printf ' .text 0x08000000 0x02000000 src/battle_controller_player.o\n .text 0x08000000 0x02000000 src/scrcmd.o\n' > "$OUT/oldrom/old.map"
  OLD_ROM="$OUT/oldrom/old.gba"
fi

# run TAG ROM MODE SAVE LAYOUT
run() {
  local tag="$1" rom="$2" mode="$3" save="$4" layout="$5" out="$OUT/$1"
  ROM="$rom"; ELF="${rom%.gba}.elf"
  engine_prepare BAGSAVE "$out" tools/ichor/tests/bag_overflow_consts.c tools/ichor/tests/bag_overflow_setup.s
  BAG_MODE="$mode" SAVE_IN="$save" LAYOUT="$layout" engine_run BAGSAVE "$out" tools/ichor/tests/bag_save.lua 30000 600 >/dev/null \
    || { echo "BAGSAVE FAIL: $tag run, see $out/run.log"; exit 1; }
  grep -o "BAGSAVE DUMP.*" "$out/run.log" | sed 's/^BAGSAVE DUMP //' > "$out/dump.txt"
}

# compare NAME A_FILE A_TAG B_FILE B_TAG
compare() {
  if diff <(sed -n "s/^$3 //p" "$2") <(sed -n "s/^$5 //p" "$4") > "$OUT/$1.diff"; then
    echo "BAGSAVE ok $1"
  else
    echo "BAGSAVE FAIL: $1"; cat "$OUT/$1.diff"; exit 1
  fi
}

check() {
  local name="$1" old="$2" new="$3"
  [ "$(grep -c . "$old/dump.txt")" -ge 9 ] || { echo "BAGSAVE FAIL: $name: the old ROM printed no dump"; exit 1; }
  compare "$name: the migrated save matches the old one" "$old/dump.txt" before "$new/dump.txt" migrated
  compare "$name: and still matches after a save and CONTINUE" "$old/dump.txt" before "$new/dump.txt" resaved
  grep "^before" "$old/dump.txt" | grep -v " $" | sed 's/^/BAGSAVE   /'
}

# 1. A save made by the old ROM.
/usr/bin/python3 -c "open('$OUT/synthetic.sav', 'wb').write(b'\xff' * 131072)"
run old_make "$OLD_ROM" make "$OUT/synthetic.sav" old
cp "$OUT/synthetic.sav" "$OUT/synthetic_new.sav"
run new_synthetic "$NEW_ROM" resave "$OUT/synthetic_new.sav" new
check synthetic "$OUT/old_make" "$OUT/new_synthetic"

# 2. A copy of a real save.
if [ -n "$REAL" ]; then
  cp "$REAL" "$OUT/real_old.sav"
  cp "$REAL" "$OUT/real_new.sav"
  run old_real "$OLD_ROM" dump "$OUT/real_old.sav" old
  run new_real "$NEW_ROM" resave "$OUT/real_new.sav" new
  check "real save" "$OUT/old_real" "$OUT/new_real"
fi
echo "BAGSAVE PASS"
