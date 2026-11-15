#!/bin/bash
# Act II's integration check: build, then every test that touches Act II or what it
# builds on, the batch audits and map_audit on Act II's outdoor maps. One line per test.
#   tools/ichor/act2/check_all.sh [LOGDIR]
cd "$(dirname "$0")/../../.."
export DEVKITPRO=${DEVKITPRO:-/opt/devkitpro} DEVKITARM=${DEVKITARM:-/opt/devkitpro/devkitARM}
LOG=${1:-build/act2_check}; mkdir -p "$LOG"
make -j"$(sysctl -n hw.ncpu)" > "$LOG/make.log" 2>&1; echo "MAKE EXIT $?"
grep "ROM:" "$LOG/make.log" | tail -1
[ -f pokeemerald.gba ] || exit 1
run() { n=$1; shift; out=$("$@" 2>&1 | tail -1); echo "$n: $out"; }
run smoke tools/ichor/smoke_test.sh
for t in slice_playthrough temple_hermes emporion eleusa trireme ichor_herms \
         kithairon thyrsa_city thyrsa_rooms act2_dionysia act2_temple theoxenia_sprites temple_trial act2_batch1 \
         act2_westrooms act2_trophonios act2_route8 act2_parnassos act2_harbors \
         act2_arkrooms act2_heights act2_arkadia act2_artemis; do
  [ -x tools/ichor/tests/$t.sh ] && run $t tools/ichor/tests/$t.sh
done
python3 tools/ichor/act2/audit_batch1.py 2>&1 | tail -1
python3 tools/ichor/map_audit.py MtKithairon Route6_EleutheraiRoad Route7_KroniaGrounds ThyrsaCity \
  Route8_Kopais Route9_Schiste Lebadeia TrophoniosCave_B1F TrophoniosCave_B2F Kirrha GulfFerry_Deck Aigion \
  Route11_KrathisGorge StyxFalls Route12_CypressRoad Route12_CaveOfMaia Arkadia Arkadia_CypressWood \
  PoolOfMnemosyne Arkadia_TempleOfArtemis 2>&1 | grep -E "^\S|FAIL" | tail -40
