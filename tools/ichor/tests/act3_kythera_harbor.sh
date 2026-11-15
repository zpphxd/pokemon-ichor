#!/usr/bin/env bash
# Act III's opening voyage, played in game (design/phase4/SCRIPT.md, beats
# III-1A to III-1C2):
#
#   tools/ichor/tests/act3_kythera_harbor.sh [rom]   (default: pokeemerald.gba; run make first)
#
# From Act II's end state (VAR_ICHOR_ACT3 = 0) on the Euploia's southern deck:
# the boarding, Route 22 by night (the lookout's fleet, SAILOR Eudoros, sleep),
# Melos (Nausikles's arrival, Kentrios on the stair, the rooted statue's rite,
# TITANBORN Theion, the obsidian seam), Cape Malea, Skandeia (Molybdos and the
# requisition, the Kronist, Alethea on the main street, the bad guests at
# Axylos's table, the Asclepeion's respawn), then III-1I's sailing for Knossa.
# Battles are won with two level-100 Metagross. Every beat is screenshotted;
# VAR_ICHOR_ACT3 and the beat flags are checked as they change.
# Output in build/test_act3_kythera_harbor/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_act3_kythera_harbor
engine_prepare HARBOR "$OUT" tools/ichor/tests/act3_kythera_harbor_consts.c tools/ichor/tests/act3_kythera_harbor_setup.s
# slice_symbols.sh names only the slice maps' scripts; add this voyage's maps'.
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(TriremeEuploia_DeckSouth|Melos|KytheraSkandeia|Route22_[A-Za-z]+|Route23_[A-Za-z]+)_EventScript_[A-Za-z0-9_]+$/ && $3 !~ /_[0-9]+$/ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/act3_scripts.lua"
engine_run HARBOR "$OUT" tools/ichor/tests/act3_kythera_harbor.lua 200000 1200
