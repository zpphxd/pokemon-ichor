#!/bin/sh
# Rebuild Mount Olympus end to end (design/maps/Ascent_*.md): the two outdoor
# tilesets, every Ascent floor, 3F and its facade, the Propylaia, the summit, the
# wild tables, the travel herms. Pass a directory to also write review renders.
#   sh tools/ichor/maps/olympus_all.sh [RENDER_DIR]
set -e
cd "$(dirname "$0")/../../.."
export PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"
PY=/usr/bin/python3
R=${1:+--render $1}
$PY tools/ichor/art/oros_build.py
$PY tools/ichor/maps/ascent.py $R
$PY tools/ichor/maps/ascent_snow.py $R
$PY tools/ichor/maps/oros_maps.py $R
$PY tools/ichor/maps/propylon.py $R
$PY tools/ichor/maps/olympus.py --only Propylaia $R
(cd tools/ichor/maps && $PY league_encounters.py)
$PY tools/ichor/maps/town_herms.py
$PY tools/ichor/maps/ascent_eggs.py
