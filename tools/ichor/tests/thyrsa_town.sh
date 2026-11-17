#!/usr/bin/env bash
# Thyrsa's ported city (claude/world-act2-0a92e7's layout on main): every door
# opens both ways and lands on walkable ground, both roads cross at the gates,
# and the houses' occupants hand over their gifts.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_thyrsa_town
engine_prepare THYRSATOWN "$OUT" tools/ichor/tests/thyrsa_town_consts.c tools/ichor/tests/thyrsa_town_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^ThyrsaCity[A-Za-z0-9_]*$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/thyrsa_town_symbols.lua"
engine_run THYRSATOWN "$OUT" tools/ichor/tests/thyrsa_town.lua 300000 1500
