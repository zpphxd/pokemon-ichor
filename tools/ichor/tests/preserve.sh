#!/usr/bin/env bash
# The Erymanthian Preserve, Ichor's Safari Zone (tools/ichor/maps/erymanthos.py):
#
#   tools/ichor/tests/preserve.sh [rom]     (default: pokeemerald.gba; run make first)
#
# From Arkadia's west road into the keeper's lodge, pay the fee, hunt in the Oakwood (a
# wild battle with barley and Pan Balls), spend the last steps, hear the bell and be walked
# back to the lodge. Output in build/test_preserve/.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_preserve
engine_prepare PRESERVE "$OUT" tools/ichor/tests/preserve_consts.c tools/ichor/tests/preserve_setup.s
{
    echo "return {"
    echo "  SCRIPTS = {"
    arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Arkadia|ErymanthosPreserve_[A-Za-z]+)_EventScript_/ { print "    " $3 " = 0x" $1 "," }'
    echo "  },"
    arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gNumSafariBalls|gSafariZoneStepCounter|gActionSelectionCursor)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
    # the Safari controller's action menu: a static name the player's controller uses too,
    # so take the one beside SafariHandleChooseAction (the same file's code)
    near=$(( 16#$(arm-none-eabi-nm "$ELF" | awk '$3 == "SafariHandleChooseAction" { print $1 }') ))
    arm-none-eabi-nm "$ELF" | awk '$3 == "HandleInputChooseAction" { print $1 }' | while read -r a; do
        d=$(( 16#$a - near )); echo "${d#-} $a"
    done | sort -n | head -1 | awk '{ print "  SafariChooseAction = 0x" $2 "," }'
    echo "}"
} > "$OUT/preserve_syms.lua"
engine_run PRESERVE "$OUT" tools/ichor/tests/preserve.lua 200000 900
