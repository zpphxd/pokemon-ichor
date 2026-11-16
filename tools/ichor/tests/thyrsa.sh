#!/usr/bin/env bash
# Assisted native chapter fixture, not a natural-level balance acceptance run.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_thyrsa
engine_prepare THYRSA "$OUT" tools/ichor/tests/thyrsa_consts.c tools/ichor/tests/thyrsa_setup.s
{
  echo "return {"
  arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Route6_|MtKithairon_|Route7_|ThyrsaCity)[A-Za-z0-9_]*$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
  echo "}"
} > "$OUT/thyrsa_symbols.lua"
engine_run THYRSA "$OUT" tools/ichor/tests/thyrsa.lua 350000 1500
