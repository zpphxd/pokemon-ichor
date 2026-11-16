#!/usr/bin/env bash
# Restore the three Act I amphorae, then play their actual encounter leads.
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
ENGINE_SYMS="$ENGINE_SYMS gBattleMons gPartiesCount gBagPosition Task_BagMenu_HandleInput HecatesHollow_EventScript_Raknit"
OUT=build/test_amphora_leads
engine_prepare LEADS "$OUT" tools/ichor/tests/amphora_leads_consts.c tools/ichor/tests/amphora_leads_setup.s
engine_run LEADS "$OUT" tools/ichor/tests/amphora_leads.lua 300000 1200
