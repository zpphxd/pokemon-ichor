#!/usr/bin/env bash
set -euo pipefail

. tools/ichor/tests/engine_build.sh
OUT="${OUT:-build/test_asclepeion_healing}"
for path in "$ROM" "$ELF" "${ROM%.gba}.map"; do
    [ -f "$path" ] || { echo "HEAL FAIL: missing $path"; exit 1; }
done
[ -x "$RUNNER" ] || { echo "HEAL FAIL: build the Lua headless runner first"; exit 1; }
mkdir -p "$OUT/shots"
arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(gSprites|SpriteCB_PokecenterMonitor|SpriteCB_PokeballGlow|gFieldEffectObjectPalette0|gSpritePalette_PokeballGlow|gPlttBufferUnfaded|gPlttBufferFaded)$/ { print }' > "$OUT/healing.syms"
export BOW_OUT="$OUT/shots/" HEAL_SYMBOLS="$OUT/healing.syms" ICHOR_ROM_MAP="${ROM%.gba}.map"
engine_run BOW "$OUT" tools/ichor/tests/asclepeion_bow.lua 9000 120
echo "HEAL PASS: both paths cover eight relief commands, palettes, stable waterlines and cleanup"
