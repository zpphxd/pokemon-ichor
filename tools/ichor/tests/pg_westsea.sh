#!/usr/bin/env bash
# Route 33, the western sea (post-game batch 1, design/postgame/BUILD.md), in game.
#
#   tools/ichor/tests/pg_westsea.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Onto Route 33 surfing at Tainaron's landing; Pontia's line across the reef
# fence's north gap; the westward current carrying you to the loose rock, the
# rock without the bronze ram, with it but not aboard, and aboard (then the
# current runs on through the fence); the fog bank's weather and its shut way
# through; an amphora and a hidden item; the Echinades' whirlpool without a
# Conch, with Poseidon's alone and with Triton's; Kymon's tow home; ashore at
# Halia's jetty and into her hut, where she rests your Pokémon. Output in
# build/test_pg_westsea/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_pg_westsea
engine_prepare WESTSEA "$OUT" tools/ichor/tests/pg_westsea_consts.c tools/ichor/tests/pg_westsea_setup.s
engine_run WESTSEA "$OUT" tools/ichor/tests/pg_westsea.lua 120000 900
