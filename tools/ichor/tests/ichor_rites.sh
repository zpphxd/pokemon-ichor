#!/usr/bin/env bash
# Rites check: altars, Favor, blessings and gifts (design/SYSTEMS.md §3), in game.
#
#   tools/ichor/tests/ichor_rites.sh [rom]     (default: pokeemerald.gba; run make first)
#
# Prays and makes offerings at altars run as a map would run them, reads the
# start menu's blessing panel, takes gifts I (a lesson, through the party
# menu), II and III, replaces one god's blessing with another's, walks a
# blessing down to its fading line, heals with Hestia's Hearthfire from the
# Relic Ring, offers Demeter a pomegranate, and cleanses a desecrated altar.
# The rules behind the numbers are also unit-tested in test/ichor_rites.c
# (make check). Output in build/test_ichor_rites/.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_ichor_rites
engine_prepare RITES "$OUT" tools/ichor/tests/ichor_rites_consts.c tools/ichor/tests/ichor_rites_setup.s
engine_run RITES "$OUT" tools/ichor/tests/ichor_rites.lua 120000 900
