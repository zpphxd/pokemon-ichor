#!/usr/bin/env bash
# Kythera's road (design/phase4/SCRIPT.md beats III-1D to III-1H), played in game:
#
#   tools/ichor/tests/act3_kythera_road.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Quickstarts with Skandeia's state (Alethea rejoined, VAR_ICHOR_ACT3 2) and a
# level-100 team, warps to the Foam Road at Skandeia's gate (act3_kythera_road_setup.s;
# nothing in the ROM is patched) and walks: the Foam Road, Alethea's dig, the
# spring, Paphia's jetty and temple door, the Laurel, the Neraida falls and
# Krenaia's Horn. Output in build/test_act3_kythera_road/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_act3_kythera_road
engine_prepare ROAD "$OUT" tools/ichor/tests/act3_kythera_road_consts.c tools/ichor/tests/act3_kythera_road_setup.s
arm-none-eabi-nm "$OUT/setup.elf" | awk '$3 ~ /^Road_/ { print $3, $1 }' > "$OUT/setup.syms"
# The road's event scripts, by name (slice_symbols.sh lists only the slice's).
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^Kythera(FoamRoad|SpringOfKallirhoe|Paphia|NeraidaFalls)_EventScript_[A-Za-z0-9_]+$/ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/kythera_scripts.lua"
engine_run ROAD "$OUT" tools/ichor/tests/act3_kythera_road.lua 200000 1200
