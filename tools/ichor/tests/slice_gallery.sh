#!/usr/bin/env bash
# The look-review gallery: play the slice, tour the menus, and assemble contact
# sheets of its best moments into design/phase1/img/gallery/.
#
#   tools/ichor/tests/slice_gallery.sh [rom]       (default: pokeemerald.gba; run make first)
#
# Env: GALLERY_SKIP_RUN=1  reuse the screenshots of the last playthrough and side checks
#      GALLERY_ALL=<dir>   also write every screenshot, in order, as sheets there (for QA)
#
# Runs tools/ichor/tests/slice_playthrough.sh with SLICE_WORKAROUNDS=1, so a known
# softlock doesn't cut the gallery short (the playthrough's own verdict is printed
# but doesn't stop the gallery), then the side checks' "menus" tour, then
# slice_gallery.py, which picks a frame per beat, per map, per battle and per menu
# by the names the playthrough gives its screenshots:
#   01_opening  02_elaia_morning  03_halia  04_akademia  05_kleon  06_route1
#   07_kronion_hill  08_akti  09_temple  10_ending  11_battles  12_menus  13_maps
# (a section with more than 15 frames is split evenly: 08_akti_01.png, 08_akti_02.png, ...).
set -u
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
if [ -z "${GALLERY_SKIP_RUN:-}" ]; then
  SLICE_WORKAROUNDS=1 tools/ichor/tests/slice_playthrough.sh "$ROM" | tail -3
  CHECKS_ONLY=menus tools/ichor/tests/slice_sidechecks.sh "$ROM" | tail -2
fi
python3 tools/ichor/tests/slice_gallery.py ${GALLERY_ALL:+--all "$GALLERY_ALL"} || exit 1
echo "GALLERY: $(ls design/phase1/img/gallery/*.png | wc -l | tr -d ' ') sheets in design/phase1/img/gallery/"
