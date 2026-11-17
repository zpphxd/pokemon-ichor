#!/usr/bin/env bash
# Themed Poke Balls thrown in a real wild battle, photographed through the throw,
# the wobble and the catch: tools/ichor/tests/ball_throw.sh [rom]
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS gBagPosition Task_BagMenu_HandleInput"
OUT=build/test_ball_throw
engine_prepare BALL "$OUT" tools/ichor/tests/ball_throw_consts.c tools/ichor/tests/ball_throw_setup.s
engine_run BALL "$OUT" tools/ichor/tests/ball_throw.lua 40000 600
