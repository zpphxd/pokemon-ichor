#!/usr/bin/env bash
# Actual letter runners and Mom's return visit, including atomic Honey and save recovery.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_return_home
engine_prepare HOME "$OUT" tools/ichor/tests/return_home_consts.c tools/ichor/tests/return_home_setup.s
engine_run HOME "$OUT" tools/ichor/tests/return_home.lua 120000 900
