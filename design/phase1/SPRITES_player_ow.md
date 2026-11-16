# Theo and Ianthe: overworld sprites

Theo and Ianthe replace Brendan and May in the overworld. They share one design, which matches the battle back pics:
- a wide-brimmed straw **petasos** in sun-gold, with a brown cord at the crown
- an Aegean-blue **chlamys**, pinned with a gold brooch at the right shoulder
- a cream **chiton**, belted
- brown sandals and a small terracotta satchel at the left hip.

Theo has short black hair. Ianthe has dark-brown hair to the jaw and a low braid tied with terracotta. The braid shows down her back and behind her neck in the side view.

## Current image-model source checkpoint

The **24 production PNGs / 186 source frames** are the sole canonical native
build inputs, pinned by `tools/ichor/art/player_sources.json`. No duplicate native
master tree or byte-copy `--write` producer is needed. The fronts, four-frame
backs, and all ten existing state atlases per character are image-model-led,
with deterministic cropping, registration, indexing and selected-model-pixel
limb assembly. They are not the rejected ASCII/native-grid pilots.

| Per character | Dimensions | Source frames |
|---|---|---|
| Battle front / back | 64x64 / 64x256 | 1 / 4 |
| Walking / running | 144x32 each | 9 / 9 |
| Field move / fishing | 160x32 / 384x32 | 5 / 12 |
| Surfing / underwater | 192x32 / 128x32 | 6 / 4 |
| Mach / Acro bike | 288x32 / 864x32 | 9 / 27 |
| Watering / decorating | 192x32 / 16x32 | 6 / 1 |

Source-frame counts, ordering, palette bindings, east mirrors, relative-frame
tables, controllers and availability remain unchanged. Walk/run phases alternate;
north Acro views show the rear of the head/cape; fishing shafts stay continuous
and distinct from fine line; Theo's north-watering jug stays on its held side.
Ground registration restores Theo bike source3 and Ianthe watering source1 by
one unclipped pixel; source images/evidence from before those shifts remain frozen.
Underwater source3 stays a dormant spare; the engine still aliases only 0/1/2.

The four bike atlases preserve **every original contact-plane and complete
`VEHICLE_EXTRAS` rectangle**, including transparent pixels and the 24 recorded
original skin-fragment instances. Explicit selections remove the model's own
vehicle geometry above those planes; six retained-model forearms register the
wheelie grips without changing head/torso pixels. The exact original bases and
selection/registration recipe are frozen with the image-source bundle. Actual
canonical PNGs, not the historical `legacy_frames()`, are checked against these
invariants. Bikes remain retired.

The three overworld palettes (`brendan`, `may`, `player_underwater`) are
byte-identical and read-only. Underwater PNGs embed the existing palette's
hardware-truncated display colors. Theo's cape avoids palette index7 so the
May-palette `LinkBrendan` alias stays compatible. Only the two trainer-local
front/back palettes change; other cast, balls and authentic RS/FRLG identities
remain untouched.

The portable frozen **`portable-player-sources-v3.zip`** accompanies the batch
evidence: 76 hashed generated-image/original-registration/recipe inputs, no live
model or repository dependency. Its SHA256 is
`285e4602c9b7151855d6a3fb47ca39869945b2a463a3331e106c68a53fbbb687`
(34,655,256 bytes). It independently reconstructs all 24 native PNGs and two
local palettes byte-identically, including retained-bike assembly. Pillow/NumPy
are the existing sprite-tool dependencies; no network is used. Local PAL text
uses the repository's required CRLF so hashes also survive a fresh Git checkout.
The verified replay environment is Python 3.9.6, Pillow 11.3.0, NumPy 2.0.2 and
zlib 1.2.12; frozen output hashes explicitly detect codec/export differences.

```bash
# In the extracted portable bundle; OUTPUT must not already exist:
python3 replay.py --output /absolute/path/to/new-replay

# Read-only canonical, independent replay and ELF-resolved ROM checks:
python3 tools/ichor/art/player_sources.py --check --rom pokeemerald.gba
python3 tools/ichor/art/player_sources.py --check --replay-dir /absolute/path/to/new-replay/native
python3 tools/ichor/art/player_sources.py --check --source-bundle /path/to/portable-player-sources-v3.zip
python3 tools/ichor/art/player_bikes.py --check
python3 tools/ichor/art/player_unused.py --check
python3 tools/ichor/art/check_elaia_water.py
```

The ROM check resolves 27 required image/palette arrays from the matching ELF,
including concatenated walk/run atlases and compressed trainer fronts. Missing
symbols, wrong sizes, out-of-ROM ranges and differing bytes fail explicitly.
Legacy repaint commands below **must fail**, leaving all canonical PNGs/PALs
unchanged. The parent-installed shared `sprites_lib.save_indexed` guard also
rejects all 24 player PNG paths without weakening the class/named guards.

```bash
python3 tools/ichor/art/sprites_player.py --write
python3 tools/ichor/art/sprites_player_ow.py --write
python3 tools/ichor/art/player_bikes.py --write
python3 tools/ichor/art/player_unused.py --write
python3 tools/ichor/art/player_underwater.py --write
python3 tools/ichor/art/surf_poses.py --write
```

Current forced-renderer fixtures cover real loaders/tables, frame transfers,
palettes and mirrors, not natural access to dormant systems:

```bash
bash tools/ichor/tests/player_battle.sh   # 160 checks / 24 captures
bash tools/ichor/tests/player_bikes.sh    # 7,481 / 736
bash tools/ichor/tests/player_unused.sh   # 242 / 34
bash tools/ichor/tests/elaia_water.sh     # 13,448 / 320
bash tools/ichor/tests/elaia_effects.sh   # 538 / 229
```

The parent-installed `player_battle_render.py` gate additionally requires all
24 captured trainer states to display every opaque native pixel unobscured,
using the source's RGB5-expanded colors and the shared rendered-pixel matcher.

The 736 paired bike captures keep identical OAM anchors and rendered lower
contact planes. All opaque original vehicle/extras pixels match their expected
hardware colors; source/VRAM checks also preserve original transparent pixels.
Unlike the earlier four-bike-only fixture, unrelated-screen comparison excludes
the stationary player's explicitly changed 16x32 OBJ as well as the tested bike.
Prior production did not preserve every transparent extras pixel, so the exact
original bases, not that older compositor, define the full extras contract.

Both genders also have natural player-controller walk/run captures in the
bedroom (fixture-selected gender/running shoes), plus the nine-capture smoke.
The isolated player-child build used 23,038,656 ROM bytes (68.66%). Full 1x/integer-zoom source
and actual-ROM comparisons accompany the handoff; old cards/pilots are immutable.
Coordinator implementation clearance is not separate user artistic acceptance,
runtime/controller eligibility, or whole-character/town completion. The marker
pair and two seven-frame credits sources are explicitly parent-owned: four
surfaces, not six. Credits' opposite-gender companion reuses the first four
frames of those same sources; the separate normal-intro sheets are link-discarded
and retained, not two additional active replacements.

## Historical source and review checkpoints

The sections below record earlier artwork and evidence. Their old `--write`
commands are historical and now reject protected paths; ASCII helpers remain
for other named-cast painters, not current player anatomy. The authentic legacy
retention partition/checker remains current and unchanged.

## Historical review images

| Image | Shows |
|---|---|
| `design/phase1/img/sprites_player_ow.png` | Every sheet for both characters at 4x |
| `design/phase1/img/sprites_player_ow_ingame_theo.png` | Theo in the bedroom at 3x: walking and running in all four directions, mid-step |
| `design/phase1/img/sprites_player_ow_ingame_ianthe.png` | The same for Ianthe |
| `design/phase1/img/sprites_player_ow_rom.png` | Every player frame decoded from the built ROM with the new palettes, with the mirrored east-facing frames |

| Sheet | Size | Frames | Status |
|---|---|---|---|
| `walking.png` | 144×32 | 9 of 16×32: down, up, left standing, then 2 steps each for down, up, left. Walk steps bob down 1 px. Right is the left frames mirrored. | Done |
| `running.png` | 144×32 | Same order as walking. Crouched 1 px, strides 2 px; fists pumping, the chlamys flaring, and a little cream wing at each heel for the Talaria (the bible's running-shoes relic). | Done |
| `fishing.png` | 384×32 | 12 of 32×32, figure centered: 0–3 west (Old Rod over the shoulder, raised, cast, out), 4–7 north, 8–11 south. A bite alternates 2/3, 6/7 or 10/11; east mirrors west. The rod is cane-brown with a straw highlight and a terracotta float. | Done |
| `field_move.png` | 160×32 | 5 of 32×32, facing south: reach into the satchel (0–1), hold the relic at the chest (2), lift it (3), raise it overhead, glinting (4). Aethos has no HM Pokémon; field powers come from relics (bible §8), so the player raises a golden relic instead of a ball. | Done |

Both folders are `graphics/object_events/pics/people/brendan/` (Theo) and
`.../may/` (Ianthe). Surfing is implemented by `surf_poses.py --write`:
192x32, six 32x32 sitting/hopping frames, sharing this file's hats and faces.
Walking, running, fishing, field-move and surfing sheets were regenerated in
the 2026-11-15 Elaia native pass with a cleaner petasos contour and eye glints.
All their motion frames are distinct and match their source arrays.

Bike sheets have a separate native rider checkpoint below; their systems
remain retired. Watering/decorating art landed
separately at `4133f17748`; these unused systems were not enabled. Underwater
now has an Ichor-native follow-on in its existing `player_underwater.pal`,
described below.
The current ROM builds and passes smoke and all three Elaia opening runs.
Both genders have new in-game walk/run captures from `player_ow_walk.lua`.
The earlier in-game images below show the previous artwork.

`bash tools/ichor/tests/elaia_effects.sh` now covers both genders' twelve
fishing animations (including finite hooked-rod loops), four surf facings,
four surf-step animations, four get-on/off poses and the five-frame relic
raise. It spawns the actual graphics ID, uses the engine's image/animation
tables, and verifies the dynamically allocated palette tag and live palette
bytes against the matching ROM source. Every finite selected animation
reaches its real end; looping states are checked through one cycle.
The complete field/state run passes 538 checks with 229 captures against the
post-Pokemon baseline and new ROM.

These captures are explicitly **forced engine-state evidence**: an idle NPC
callback prevents normal NPC behavior from overriding the selected player
animation. They are not proof that early Elaia gameplay permits fishing or
late relics, nor do isolated rider states exercise the surf mount/controller.
Bikes remain outside this checkpoint.

## Unused watering and decorating artwork

`tools/ichor/art/player_unused.py --write --check` replaces only the four
existing watering/decorating PNGs with Theo/Ianthe's established native
petasos, faces, chlamys, chiton and sandals. The watering vessel is a small
handled clay jug with two pouring phases in each facing; source order remains
down 0/1, up 2/3, left 4/5. The unchanged engine image tables expose those six
32x32 frames through their nine standard entries and mirror the east-facing
views. Decorating keeps its single 16x32 frame, now a crouched player holding
a small clay vessel. Shared palette bytes, controllers and availability are
unchanged; this artwork does not enable either unused system.

`bash tools/ichor/tests/player_unused.sh` exercises the actual graphics IDs,
animation/image tables, all sixteen live palette words, hardware mirroring
and complete OBJ VRAM frame transfers. Supply another ROM as the first
argument or through `ROM`, with its matching ELF beside it.
Both exact before and current ROMs
pass 242 checks with 34 captures each. These are labeled test-only fixtures,
not ordinary gameplay or proof of controller eligibility. Three source
regressions, four native PNG checks, helper/build and original smoke pass.
Complete palette-correct 1x/4x comparisons and matching ROM/ELF/map packages
are preserved in the coordinator's session artifacts.

## Retained bicycle rider follow-on

`python3 tools/ichor/art/player_bikes.py --write --check` writes exactly
the four existing `mach_bike.png`/`acro_bike.png` sheets. The private painter
uses the accepted Theo/Ianthe hats, faces and role maps read-only, with
authored gripping bodies, bent knees and alternating pedal phases. Private
base atlases preserve the bicycles, contact planes and raised-wheel/
handlebar parts; new riders may occlude parts behind them. This is not a
recolor of Brendan/May bodies or a new Greek vehicle.

Each Mach atlas remains 288x32 with nine 32x32 source frames; each Acro atlas
remains 864x32 with 27, for 72 source frames total. The player palettes are
unchanged, including all sixteen hardware color roles. PNGs are indexed
4bpp with transparent index 0 and exact BGR555 display colors.
`test_player_bikes.py` checks source reproduction, every retained bicycle
contact plane, accepted faces and distinct ordinary/wheelie pedal phases.

The original engine contracts are retained: the single relative-frame
image table transfers 512 bytes per source frame; Mach uses 20 standard
animations, Acro 40 standard/hop/standing-wheelie/moving-wheelie animations.
The four retained rival graphics IDs alias the same atlases. No source frame
is unused by these tables. East mirrors west in hardware; no vertical flip
is introduced. All production tables, callbacks, anchors and eligibility
code remain unchanged.

`bash tools/ichor/tests/player_bikes.sh [ROM.gba]` exercises all eight real
player/rival graphics IDs in a test-only NPC fixture. The exact paired
`7d17b62e9a` baseline and new ROM each pass 7,481 checks with 736 captures:
240 graphics/animation cases, every ordered phase, all source frames, all
live palette words/tags, full OBJ VRAM transfers, mirrors, finite ends and
loop cycles. The fixture holds the NPC callback idle; it does **not**
exercise bike controllers or prove bikes available in Aethos.
The walking observer's randomized Quickstart identity is fixed only in the
fixture so full-screen before/after backgrounds match.

For complete 1x/4x native and engine comparisons, pass `--preview DIR`,
`--engine-before BEFORE_RUN` and `--engine-after AFTER_RUN` to the painter.
The comparison gate requires all 736 paired phases and matching OAM
anchors, and rejects any difference outside the forced bike sprite.
Helper/build, 26 source/audit regressions and nine-capture smoke pass;
ROM usage is 23,039,520 bytes
(68.66%). Artistic approval and serial main integration remain the
coordinator's gate. Bike items, tire tracks, shop tiles and the retirement
policy are untouched; other global/town groups remain open.

The coordinator subsequently accepted source `36f4207c6c` and independently
integrated it after nine-species main `4d0a21d8fe`. Both matching combined
ROMs pass the same 7,481-check/736-capture fixture and complete comparison
gate; all native cards, all 240 case boards and smoke captures were inspected.
The four compiled atlases match ROM bytes, and every byte outside their
ranges remains identical to the baseline. Combined source regressions
pass 37 tests. Healing, water, spare-player and nine-species fixtures still
pass; use remains 23,039,552 bytes (68.66%), with the GBA padded to 32 MiB.
This is scoped rider-art acceptance, not restored bicycle gameplay or
whole-town/global completion.

## Genuine legacy player variants: retained, not redrawn

The coordinator accepted the read-only inventory of 22 existing legacy
PNGs, 208 source frames, against original Gen 3 decompilation art. These are
genuine Ruby/Sapphire and FireRed/LeafGreen identities, not additional
Theo/Ianthe costumes. No artwork or palette correction was needed.

`tools/ichor/art/legacy_players.json` pins each complete PNG byte hash,
row-major index hash, dimensions/frame layout and hardware palette hash.
Shared dimension hashes encode two little-endian uint32 values; palette
hashes encode sixteen little-endian BGR555 words. The recorded original
revisions are expansion 1.17.2 (`79dd436920...`), pret/pokeemerald
(`9103e529c2...`) and pret/pokefirered (`ce6406d8c2...`). The original full
inventory and 44 complete 1x/4x reference cards remain immutable in session
artifacts. Provenance is recorded locally; no network is used by the gate.

| Partition | PNGs / source frames | Current binding |
|---|---|---|
| `ruby_sapphire_{brendan,may}/walking.png`, `red.png`, `leaf.png` | 4 / 36 | Compiled link walkers, nine 16x32 frames each, relative 256-byte image tables and Standard20 animations; east mirrors west |
| `ruby_sapphire_{brendan,may}/running.png` | 2 / 18 | Declared but no image-table consumer; linker-GC absent |
| `rs_brendan.png`, `rs_may.png` | 2 / 18 | Original FRLG RS representations, no Ichor declaration/table/ID; not aliases of the compiled RS walkers |
| `red/`, `leaf/` playable-state families | 14 / 136 | `IS_FRLG=0`; native sources retained but player-state symbols absent |

The RS link walkers use their separate `ruby_sapphire_brendan.pal`/
`ruby_sapphire_may.pal` (tags `0x1122`/`0x1123`); Red/Leaf link walkers use
`red_leaf.pal` (`0x111D`). Orphan RS bitmaps use the **original FRLG
`NPC_WHITE` role order**, not the RS-link palette: the hypothetical
wrong-palette preview was not a production defect. Dormant FRLG player
states use `player_frlg.pal` through both `PLAYER_RED` and `PLAYER_GREEN`.
None of these are the accepted Theo/Ianthe player palettes.

Dormant normal states alias their running source frames from `*_surf_run`;
surf states also use `*_surf_run` rather than the separate 32x32 `*_surf`
bitmaps. Field-move and VS Seeker states share `*_item`. The manifest
retains these aliases, spare source frames and finite/loop contracts.
The naming-screen rival only borrows a RedNormal template: it substitutes
its own sheet/palette/animations and is not a direct legacy PNG alias.

```
python3 tools/ichor/art/check_legacy_players.py --rom pokeemerald.gba
python3 tools/ichor/art/check_legacy_players.py --rom /path/to/snapshot.gba --elf /path/to/snapshot.elf
python3 -m unittest tools/ichor/tests/test_legacy_players.py
```

The read-only checker preserves all 22 source files and five hardware
palettes. It uses `arm-none-eabi-nm` on the selected matching ELF to resolve
the four required link arrays and three palette arrays, checks exact
sizes/ROM bounds, and compares all 36 compiled frames and all sixteen
palette words. Missing required symbols are **failures**, never skipped.
GC-absent/orphan/FRLG symbols must remain absent. No asset addresses are
hardcoded; only the architectural GBA ROM base is used to locate the
ELF-resolved arrays in the selected ROM.

These are offline source/compiled-array checks, not live link gameplay or
controller eligibility. Link/contest retirement and peer-game identity
selection remain unchanged. This persistence checkpoint has no art,
palette, frame-table, callback or gameplay edits; helper/build and smoke
pass and the complete padded ROM is byte-identical before/after.

## Native underwater follow-on

`python3 tools/ichor/art/player_underwater.py --write` writes only the two
128x32 underwater sheets. Native swimming bodies, wide bent elbows/raised
forearms and splayed kicking knees replace the upstream player/black-blob shapes.
The profile leans from head to hips with folded knees and returning feet.
The existing petasos,
faces, Theo's short hair and Ianthe's braid are shared identity sources.
The underwater palette file is unchanged. Role indices retain skin,
blue clothing, straw, satchel and outline meanings; PNG palettes use the
same truncated BGR555 values the ROM loads.

All four source frames (south, north, west, spare east) are redrawn and
distinct. The existing engine image table aliases nine logical slots onto
the first three source frames; the fourth remains unused, not falsely
claimed as an additional live facing. East mirrors the west frame in game.
Underwater movement has no newly added stroke frames: the original aliases
and engine hFlips/bob helper are retained.

`bash tools/ichor/tests/elaia_water.sh` covers both players' four facings
and four standard movement speeds, together with paired dolphin/rider
states. Another ROM can be supplied as the first argument or through `ROM`,
with its matching ELF beside it. The partial-Akti baseline and new ROM each pass 13,448 assertions
and 320 captures across 64 state cases. Actual graphics IDs, dynamic
palette tags/live bytes, native image aliases and OBJ VRAM are checked.
The real hidden underwater helper bobs the swimmer; an idle NPC callback
holds the requested state table. The 1x/4x native and complete matched
engine galleries are retained as session artifacts.

This is **forced actual-ROM rendering on Route 1**, not underwater-map
gameplay or proof that the post-game Nereid Pearl is available early.
Build, smoke and the three-sheet source/native gates pass. Accepted walking,
surf rider and other player sheets and all palette files remain unchanged.
The coordinator held the initial `f786a9ad25` underwater submission because
its near-straight limbs read as standing. The pose refinement above leaves
the accepted dolphin untouched and adds measurable native arm/knee spread
and profile knee-to-ankle bend gates. The preserved submitted ROM, landed
`4133f17748` main baseline and refined ROM each pass the identical 320-capture
fixture. Complete 1x/4x comparisons are preserved separately for the
pose-only refinement and full current-main rollout; no older evidence is
overwritten. The safe-boundary merge includes the separate watering/decorating
art, which this refinement does not change.
The refined native poses are artistically accepted; independent main
integration remains the coordinator's gate.

## Palettes: how the roles were remapped

`graphics/object_events/palettes/brendan.pal` and `may.pal` are shared with every player sheet (bike, surf, fishing, watering and so on), the rival Brendan and May sprites and the link-player sprites. `may.pal` also colors the trainer "!" and "?" emotes, which use indices 14 and 15. So each index keeps its Emerald role and is recolored by role, and the untouched sheets still draw sensibly.

The two palettes never had the same roles. The brief's suggested mapping (navy at 5–8) holds for Brendan but not for May, so each palette is remapped on its own terms:

| Index | `brendan.pal` role | Theo | `may.pal` role | Ianthe |
|---|---|---|---|---|
| 1–3 | skin | skin (248,208,168) (232,160,112) (184,112,72) | skin | same |
| 4 | skin outline | warm brown (104,56,40): skin outline, sandals, hat cord | skin outline | same |
| 5 | navy, light | chlamys highlight (112,168,224) | gray (bandana knot) | chlamys (48,104,176) |
| 6 | navy | chlamys (48,104,176) | dark slate (shorts) | chlamys shade (24,56,120) |
| 7 | navy, dark | chlamys shade (24,56,120) | hair brown | hair (128,80,48) |
| 8 | navy, darkest (hair) | black hair's sheen (48,48,64) | hair dark brown | hair shade (72,40,32) |
| 9 | light gray | chiton shade (216,192,144) | light gray | same |
| 10–11 | green (hat band) | straw (240,192,64) (200,144,40) | green (bandana) | same |
| 12–13 | red | terracotta satchel (224,136,88) (184,88,48) | red | same |
| 14 | white | chiton cream (248,240,208) | white | same; the "!" emote's fill turns cream |
| 15 | black | ink (32,24,24) | black | same |

Only Theo has a chlamys highlight; Ianthe's chlamys uses two shades because `may.pal` has two free slots for it.

## Side effects on the untouched sheets

The retained bicycle checkpoint replaces the stock player bodies rather
than relying on the original beanie/bandana recolor. Remaining shared uses:
- **Rival Brendan and May** (`OBJ_EVENT_GFX_RIVAL_*`) and the **link players** take the same colors. Ichor's rival is Kleon, so the rivals should not appear in the slice.
- **The "!" and "?" emotes** above trainers use `may.pal` 14 and 15: cream with ink, nearly as before.
- **Reflections** are filtered from the live palette by the engine, so they follow automatically.

## Checking

`tools/ichor/tests/player_ow_walk.lua` Quickstarts a new game, forces the gender (`WALK_GENDER=0` Theo, `1` Ianthe), gives the running shoes, then walks 2 tiles each way in the bedroom and runs the same way holding B, taking a screenshot every 2 frames:

```
mkdir -p build/walk_test/theo
WALK_GENDER=0 WALK_OUT=build/walk_test/theo/ build/tools/ichor-mgba-headless \
    --script tools/ichor/tests/player_ow_walk.lua --frames 4200 --until "WALK done" pokeemerald.gba
python3 tools/ichor/art/sprites_player_ow_review.py shots build/walk_test/theo out.png --title Theo
```

The `shots` review crops the player at 3x into one row per move.

Fishing and the field move can't be reached from the bedroom (they need water and an Old Rod, or a field-move target), so they are checked from the ROM instead:

```
python3 tools/ichor/art/sprites_player_ow_review.py rom out.png
```

This decodes every player frame and both palettes from `pokeemerald.gba` at the symbols the engine loads (`gObjectEventPic_BrendanFishing` and so on), with the mirrored east-facing frames. It proves the build's tiling and colors, but not the animation timing in play.
