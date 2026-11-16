#!/usr/bin/env bash
# Actual Kalliste dig interactions, Bag retry, save recovery and midnight renewal.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_kalliste_digs
engine_prepare DIGS "$OUT" tools/ichor/tests/kalliste_digs_consts.c tools/ichor/tests/kalliste_digs_setup.s
engine_run DIGS "$OUT" tools/ichor/tests/kalliste_digs.lua 160000 900
