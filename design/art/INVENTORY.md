# Ichor art inventory

The checklist that makes the total conversion true: every player-facing asset group and system in the ROM, with its status. It is the "inventory" that `design/ART_PLAN.md` §6 promises. Nothing should stay Hoenn by accident.

## Character quality restart, 2026-11-16

The user approved the new **actual 64x64 Theo preview** and directed the same
method across character sprites. The approved PNG, generated source and
unchanged earlier illustration are preserved in `design/art/img/theo_approved_*`;
the authoring and review rules are in `design/ART_PLAN.md` under "Approved
character direction". The old native-pilot v3 remains rejected. Historical
acceptances below do not establish compliance with this new benchmark.

The first ownership partition covers all **40 existing custom NPC sheets**,
**20 Theo/Ianthe player-state sheets**, **20 custom trainer fronts**,
**four custom four-frame battle-back sheets**, and **Daphne's intro portrait**:
85 production PNG surfaces, not 85 completed redesigns. The approved Theo
reference is not counted as integrated production art.

| Human group | Assigned surfaces | Current new-style status |
|---|---|---|
| Players | Theo/Ianthe fronts and backs; all ten existing state sheets each | Image-model-led redesign in progress; Theo front preview is the approved style anchor, not complete player coverage |
| Named cast | 18 custom walker sheets, eight fronts, Kleon/Alethea backs, Daphne intro | Image-model-led redesign in progress; includes Kleon's seasick/tablet poses and the extra Sam/Apollo/Cami frames |
| Classes and townsfolk | 22 custom walker sheets and ten custom fronts | Source-backed image-model-led adoption verified: all 199 field states, healer bow, 66 right mirrors and ten fronts; shared palettes and bindings preserved |
| Active imported class fallbacks | Exekias/Potter, Myrrhine/Initiate F, Pheidippos/Runner | Three parent-owned image-model-led native fronts now replace the active picture bindings; original Hiker, Psychic F and Running Triathlete M sources remain byte-identical |
| Supplemental players | Two region-map markers and two seven-frame credits rider sheets | Parent-owned identity/source review in progress, separate from the core 24 player surfaces; credits' opposite-gender companion reuses the first four frames of the same seven-frame source |
| Legacy players | 22 RS/FRLG PNGs and their existing compiled aliases | Preserve accepted identities/provenance; not a new character redesign |
| Other imported people/fronts/backs and duplicate screen art | Hoenn/FRLG/cut assets, map markers, intro/credits/naming and other human appearances outside the custom set | Coverage review remains open; do not silently count unchanged or unassigned art as complete |

The Sacred Way replacements add three fronts beyond the first 85-surface
partition (88 surfaces before supplemental markers/credits). Their immutable
model source and export recipe are in `design/art/characters/route4/` and
`tools/ichor/art/export_route4_characters.py`. These are sampled/quantized
image-model outputs, not hand-authored native drawings or separately
user-approved character designs. Native source reproduction and accent
retention pass; the real loader gallery passes 68 checks/18 captures including
these three fronts. Build and smoke pass (9 captures); linked ROM usage is
23,094,568 bytes / 68.83%. The 22-source/208-frame legacy-player set and
36 compiled link frames remain unchanged. This bounded parent checkpoint
does not complete the other character groups or establish gameplay coverage.

The next bounded checkpoint adopts the 32 class/townsfolk sources from
`tools/ichor/art/sources/human_classes/`; reproduce them with
`python3 tools/ichor/art/human_classes.py --write`. The class-specific legacy
guard rejects those 32 production paths before writing, without blocking
unrelated assets. The combined parent build passes 79 targeted regressions,
smoke's nine captures, and `tools/ichor/tests/human_classes.sh`: 1,971 engine
checks and 275 complete, unobscured rendered-state comparisons. Linked ROM
usage is 23,096,488 bytes / 68.83%; the accepted legacy-player sources and
compiled aliases still pass. This brings adopted new-style character
surfaces to 35, leaving the 24 core player, 29 named-cast and four supplemental
surfaces in progress. These checks and parent implementation clearance do
not imply separate user artistic acceptance or completion of any town.

This character-only continuation does not restart Pokemon, prop, field-effect,
tileset, UI or ball-art generation. Town-by-town production landing still
requires complete compatible native sources, visual review, build and smoke
evidence. The full character and global sprite requests remain open until the
remaining groups are reconciled.

**Compiled-map coverage check:** at the concurrent `8b70e8ef98` boundary,
`data/maps/map_groups.json` registers 51 Aethos maps and 26 retained engine
maps. All directly placed human graphics on those 51 Aethos maps use the
custom character set above. The only variable graphics placement is Kleon
on the *Euploia*, whose script selects the existing normal, seasick and
tablet sheets; these are all assigned. Other non-species placements are
items, cuttable trees, breakable rocks and pushable boulders, not missing
human sheets. The 26 retained engine maps still contain imported people;
this is not evidence that they are reachable through Aethos or redrawn.
The normal credits routine loads the two seven-frame
`graphics/intro/scene_2/{brendan,may}_credits.png` sources for the player and
the opposite-gender companion. The companion loads only their first four
frames, not the separate normal `brendan.png`/`may.png` intro sources
(`src/intro_credits_graphics.c`, credits sheet tables). Those two normal
intro graphics and their sheet tables are discarded by the linker at the
`55d1d1b940` boundary; preserve their original sources rather than claiming
four active rider replacements. Together with the two region-map markers,
the four active supplemental surfaces bring the assigned character scope
to 92, not 94. Their review remains open. Credits' separate bicycle shares
each rider's palette, so rider adoption must preserve every palette word
used by the unchanged bicycle.

## Source provenance coverage, 2026-11-15

`sprite_audit.py provenance --reference <commit> --output <json>` accounts for
every current graphics PNG/palette against a pinned local Git revision. It
records the resolved commit, each working-file SHA-256, canonical Git blob
identity, reference-only paths and mutually exclusive source relations.
Palette comparison normalizes CRLF through the repository's text convention;
it does not rewrite palettes or weaken the byte-exact working-file hashes.
Invalid references, empty reference graphics sets and symlinked sources fail.

At the combined `5ca37db184` boundary, comparison with expansion 1.17.2
(`79dd436920845ebc145577649de624f65298c209`) accounts for all **20,149** current
sources: **18,172 reference-identical**, **467 source-different** and **1,510
current-only**. The reference also contains **25 reference-only** paths.
These figures are not redraw or completion percentages. In particular, an
unchanged expansion import is not automatically original Gen 3 artwork,
artistically accepted, or verified against its runtime palette/table binding.
Source differences can also be PNG container changes rather than new pixels.
Native comparisons and the bounded acceptance ledger below remain the
artistic and runtime evidence.

## Image-model-led named human cast candidate

This supersedes only the named human surfaces listed below, not the historical
artistic-acceptance claims for unrelated groups. The user authorized the new
image-model-led Theo direction, not the rejected native v3 pilots. These are
**candidate implementations pending artistic review**, not user acceptance or
whole-town completion. Source/renderer passes alone do not change that status.

| Owned group | Exact candidate coverage | Retained contracts / limits |
|---|---|---|
| Named cast walkers | `aiakides`, `alethea`, `apollo`, `cami`, `demeter`, `endeis`, `kedalion`, `kerykos`, `kleon`, `kleon_seasick`, `kleon_tablet`, `mom`, `pheidon`, `professor_daphne`, `pronomos`, `sam`, `hierophant_ione`, `titan_grunt`: 18 sheets, 170 frames | 16x32 frames; Sam/Apollo 12, Cami 11, all others nine. Existing graphics IDs, frame order, shared cast/folk/theoxenia palettes and aliases retained |
| Named portraits | Alethea, Cami, Ione, Kerykos, Kleon, Daphne, Sam, Titan grunt: eight 64x64 PNGs | Six existing trainer bindings; Sam/Cami remain unused dialogue busts, not newly enabled interfaces |
| Named companion backs | Kleon and Alethea: two 64x256 sheets, eight total frames | Model-pixel limb assembly; fixed head/costume/satchel anchors and existing near-left hold/windup/release contacts. Existing Hoenn throw tables unchanged |
| Daphne intro duplicate | `graphics/birch_speech/birch.png`: one 64x64 PNG | Exact pixels and palette duplicate Daphne's new front |

Total: **29 surfaces / 187 source frames**. Forty-nine selected image-model
RGBA crops and their hash manifest are under
`tools/ichor/art/base/named_cast/`; `model_cast.py` is the complete deterministic
conversion/assembly recipe. This is larger model artwork trimmed, sampled
nearest-neighbor and palette-reduced, with mechanical source-pixel animation
assembly; it is **not hand-authored native art**. Complete actual 1x/4x review
cards and unchanged pre-write PNG/ROM evidence are preserved in session files
under `named-cast-model`. Mouth/face and small ball detail can be lost during
64px reduction and remain visible review limitations.

Palette reduction uses median-cut plus k-means refinement. Extra weighting
is limited to genuinely tiny saturated hues and neutral lights (at most 3%
opaque coverage), never broad red/terracotta robes. Ione's cream veil and
Kleon's linen have native review evidence; Alethea's sampled/final blue
headband and the existing model-red orb caps/light halves have explicit
regressions. Kerykos retains the established
dark felt petasos, porphyry/burgundy cloak, gray beard, scrolls and kerykeion;
the old source docstring's blue-cloak wording was stale. Fixed shared palette
files and all unowned readers are retained.

Cami's unused front bust has a bounded follow-up: its existing model wheat is
relocated from hair to shawl fringe, with adjacent model hair restoring the
old location. The original source, face/figure anchors, Cami walker and every
other native output remain unchanged. Tiny source-yellow weighting preserves
the relocated wheat; it does not alter shared palettes or enable a bust UI.

The named-cast portion of the shared `save_indexed` guard blocks exactly its
29 migrated paths and names `python3 tools/ichor/art/model_cast.py --write`;
the 32 class/townsfolk paths remain separately protected. Neither guard
blocks a folder or silently falls back to the old painter. The named
source-frame ROM gallery uses actual graphics IDs, image-table slots, palettes and native OBJ
copies in test RAM, not natural battles or dialogue. Sam/Cami's two unrouted
portraits have native/source evidence only; Daphne's duplicate is also checked
through source reproduction and the introduction.

**Isolated candidate checkpoint verification:** 34 scoped source regressions,
helper compilation, `make -j$(sysctl -n hw.ncpu)` and
`tools/ichor/smoke_test.sh` pass (nine smoke captures). ROM usage is
23,038,304 of 33,554,432 bytes (68.66%). Both matching before/current named
galleries pass 996 checks / 238 captures, including every complete OBJ frame,
all 16 ROM/unfaded/hardware palette words and east mirrors. The independent
PNG encoder matches all 184 unmirrored frame/palette dumps on each ROM.
Every pixel outside the subject's native 16x32 or 64x64 image bounds is
identical across all 238 screenshot pairs. Route 1 passes with 48 captures,
the temple trial with 31, and the actual strum/rise controller check with
18 checks / six captures. Across 21,269 protected tracked asset/source paths,
exactly the 29 owned production PNGs differ; shared palettes, players, balls
and held Pokemon remain unchanged. Complete old/new native cards, unchanged
model sources and genuine paired engine captures remain outside Git in the
session evidence. These passes do not grant artistic approval.

Player states, generic folk/class portraits, balls, terrain, UI and unrelated
surfaces are outside this human batch. **All 24 unfinished owned Pokemon remain
held**; the preserved crab/Ketos prototypes and older material-polish evidence
are not upgraded to calibrated-redesign acceptance.

## Elaia redraw checkpoint, 2026-11-15

This checkpoint is **not a declaration that every Elaia-visible sprite is
finished**. It is based on `main` at `a22be3c8a9`; the historical Greek/Hoenn
counts below describe the earlier total-conversion pass, not approval of the
new higher-quality art direction.

| Elaia/opening group | This checkpoint | Remaining gate or scope |
|---|---|---|
| Theo/Ianthe fronts, Kleon, Daphne and Alethea portraits | New native poses/faces/folds in the existing painters; Daphne intro and trainer portrait regenerate together | Intro/player-choice/Kleon captures and native checks pass; later portrait contexts remain unexercised |
| Theo/Ianthe and Alethea animated battle backs | Profile/eye detail, matched palettes; all four throw frames retained and distinct | Opening player throw captured; native checks cover all sheets, not later tutorial/throw contexts |
| Player walking, running, fishing, relic raise and surfing | All ten sheets regenerated from the shared native hats/faces; no opaque palette-role changes | Both genders' walk/run captures pass; fishing, surfing and relic tables now have labeled engine-state captures, not proof of early-game controller eligibility |
| Player underwater | Both 128x32 sheets redrawn with wide bent arms, splayed kicking knees and a leaning profile; shared Theo/Ianthe identity parts and `player_underwater.pal` preserved | Pose/source/native checks and forced real-ROM state/bob/VRAM coverage pass; fourth source frame remains unused by the standard image table, and Dive eligibility/controller is not exercised |
| Player bikes | Four native Theo/Ianthe rider sheets, 72 source frames; private painter preserves retained bicycle contact planes/raised parts and exact player palettes | Artistically accepted at scoped source checkpoint `36f4207c6c`; independent combined renderer fixtures pass 7,481 checks/736 captures. Retired bike availability/controllers, items, tracks and shop art are unchanged |
| Player watering and decorating | Four native sheets replace recolored Brendan/May with Theo/Ianthe's established faces/clothing, a handled clay watering jug and crouched decorating pose | Source/native checks and matching 242-check/34-capture engine fixtures pass; gameplay availability/controllers/shared palettes unchanged; these unused systems are not enabled |
| Legacy RS/FRLG player variants | Accepted retain-as-authentic: 22 PNGs / 208 source frames match original Gen 3 art and hardware palette roles; offline private manifest/checker preserves provenance and all source/index/dimension/palette hashes | Required compiled 36-frame link atlases and three palette arrays checked by ELF symbol resolution; running/orphan/FRLG-gated partitions retained. No redraw, Red/Leaf identity conversion, live-link or controller claim |
| Kleon, Daphne, Alethea walkers | Native hair/headband/eye details; nine existing engine frames each | Native checks and current Elaia/Akademia captures pass |
| Halia, Korinna, Philon, Gylippos, woman, man/scribe, harvester, kid, shepherd, fisher, Kydippe and Melitta | Twelve shared sheets get native shoulder/waist/hem construction and Kydippe's shawl folds; costumes, props, frame indices and folk/cast palette budgets preserved | Native checks and current opening/interior captures pass; this is a polish pass, not twelve wholly new character concepts |
| Nine regional starter stages, Eripip and Galekit | Matched native battle/icon/follower/footprint pass, tracked in `design/dex/SPRITES.md`; native and rollout checks pass | Native artistic review accepted; current opening battles cover the first stages, the engine gallery covers every stage |
| Daphne's introductory Smoliv | Matched native olive-baby views and reproducible source; two-frame animation metadata updated without changing species/story/stats | Native checks, final rebuilt introduction and engine gallery pass |
| Ground item jar | New hand-painted handled/clay jar, still 16x16 on the existing folk palette | Current in-game pickup capture |
| Three starter kraters and their rocking views | Native contour/rim/clay highlight polish; existing starter palettes, motifs and engine frame order preserved | Current selection/rocking capture |
| Ripples, normal/landing splashes and ledge dust | Five native contact sheets replace inherited Emerald pixel shapes; unchanged dimensions/frame counts | Current in-game contact/landing capture |
| Grass/reed rustle and landing variants, sandal prints, field emotes, shadows, warp arrow and follower emotions | Fifteen native field sheets and the 23-frame follower-emotion sheet redrawn from reproducible indexed sources; shared/ball palettes untouched | Source/native checks and matched engine captures pass; tall-grass steps use actual Route 1 terrain, reeds use a labeled RAM fixture, other effects use labeled API fixtures |
| Dolphin surf mount | Three native views redrawn with a visible snout, saffron flank, cream belly, flippers and flukes; accepted rider sheets and both player palettes unchanged | Matched forced real-ROM paired mount/rider evidence covers four directions, step/get-on/off poses, native bobbing, palette and VRAM binding; not full Surf controller eligibility |
| Outdoor aethos/kalliste and interior oikos/oikia/civic terrain/furniture | Existing Greek tiles retained; no layout, collision, tileset palettes or tile budget changed | Separate terrain/environment pass if required for visual consistency |
| Door and water tile animations | Existing artwork retained | Separate environment-animation review |
| Opening/menu/battle UI, ordinary item icons and the bakery trade scene | Existing artwork retained | Full-rollout shared-screen/item/trade scope; no claim these sprites were all redrawn |
| Battle/Bag/follower balls | No edits by this batch | Separate Greek-god-ball owner |
| Ione and Titan grunt | No edits | Akti/Route 1 batch |

**Artist checkpoint verification:** native helper compilation and
`make -j$(sysctl -n hw.ncpu)` pass using an isolated Arm GNU 15.3.Rel1,
libpng and Poryscript toolchain. After the Smoliv pass the ROM uses
23,027,752 bytes of 33,554,432 (68.63%), leaving 10,526,680 bytes.
`tools/ichor/smoke_test.sh` passes (9 captures), and
`tools/ichor/tests/elaia_opening.sh` passes for Nebrel, Kynder and Hipling.
Both genders complete `player_ow_walk.lua`. Forty human/object sheets match
their source arrays, indexed palettes, transparency, BGR555 precision and
unique intended motion; the starter krater/tondo sheets pass their native
checks too. The eleven regional Pokemon pass the coordinator's native
rollout gate; Smoliv passes its separate source/ROM/native-conversion check.
`tools/ichor/tests/elaia_art.sh` renders real ROM front/back/normal/shiny
views for all twelve Pokemon, including both front frames, in a test-only
engine gallery: 96 checks and 48 captures. The preserved before-redraw ROM
passes 92 checks and 46 captures with `ELAIA_ART_BASELINE=1`; that option only
accounts for its single-frame Smoliv and does not relax the default gate.
The gallery does not replace real opening/battle coverage.

Pylakyon's final native refinement separates the S-curved serpent tail/head
from its flank in both fronts, back, icons and all follower directions.
Palette and footprint bytes are unchanged; the three diagonal mastiff heads,
arched lunge and sleeping flame-head progression remain intact. Final
native and real-engine before/after captures are retained with this handoff.

**Follow-on effects/state checkpoint:** `check_elaia_effects.py` checks all
16 sheets against native source pixels, exact dimensions, 4bpp indexed PNGs,
transparent index 0, BGR555 colors and distinct intended motion pairs.
`elaia_effects.sh` passes 538 checks and 229 captures against both the
preserved post-Pokemon integration baseline (`9ae5aff4af`) and the new ROM.
Its actual-input grass route does not change production terrain. It labels
forced owner-attached emotes, emotion indices on the actual Nebrel follower,
four shadow templates (including the unused overworld XL template), warp-arrow blinks,
sandal prints, landing effects and the single RAM reed tile separately.
The field and follower shard share one source outline.

Both players' twelve fishing animations, four surf facings, four surf-step
animations, four get-on/off poses and five-frame relic raise use real graphics
IDs, image/animation tables, dynamically allocated palette tags and matching
ROM palette bytes. These are forced state-table fixtures with an idle callback,
not claims that the fishing/surf/relic controllers were played normally in
early Elaia. Build and original smoke pass; ROM usage remains 23,027,752 bytes
(68.63%). The coordinator's native PNG gate passes all 16 changed sheets.

The old missing-toolchain failure is resolved. Retained groups above,
unexercised controllers and final artistic approval remain explicit;
this is not a finished-every-sprite town declaration. The human/opening-object
checkpoint was landed on `main` as `dfb7974fbc`, and Pokemon as `9ae5aff4af`;
the follow-on effects checkpoint does not require reapplying either
equivalent feature-branch commit.

**Bounded mount/underwater follow-on:** based on `main` at `8fce8d4ed6`,
only `surf_blob.png` and the two `underwater.png` sheets are changed.
`check_elaia_water.py` verifies three source-exact indexed 4bpp sheets and
eleven distinct source frames, transparent index 0, BGR555 palette colors,
shared mount color roles and unchanged accepted rider source arrays. The
underwater palette file is retained byte-for-byte; embedded PNG palettes
use its already-truncated hardware colors.

`elaia_water.sh` passes 13,448 assertions and 320 captures against both the
preserved partial-Akti `2d1a23993f` ROM and this checkpoint's ROM. Its 64
forced state cases cover both genders' four surf directions in seated,
stepping and controller-held get-on/off poses, plus underwater's four
facings and four standard movement speeds. Native callbacks, palette tags
and live bytes, relative-frame/image-table aliases, OBJ VRAM, mount anchors
and shared bob offsets are checked. The hidden native underwater bob helper
tracks the swimmer; it does not render a surface dolphin underwater.
All 320 matched captures and complete 1x/4x comparisons are retained in
session artifacts. These are Route 1 renderer fixtures, not natural
surfing/diving play or early relic eligibility. No map, controller, frame
table, accepted rider, shared palette or ball asset is changed. Helper
compilation, `make`, smoke (9 captures), native checks and the three-image
rollout gate pass. ROM usage is 23,040,960 bytes (68.67%).

Terrain/furniture, door/water tile animations, UI/item/trade, bikes and other
unused/global groups remain open. Watering/decorating landed separately as
`4133f17748`, not part of this three-sheet checkpoint. Artistic approval and
serial main integration remain the coordinator's gate.

**Underwater pose refinement:** the coordinator accepted the dolphin but
held `f786a9ad25` because the initial underwater silhouettes still read as
upright standing figures. A follow-up redraw changes only the two underwater
PNGs: raised returning forearms/wide elbows, bent splayed front/back kicks,
and a leaning profile with folded knees and feet. The source checker now
also measures visible arm/knee spread and the profile knee-to-ankle bend.
The accepted dolphin, riders, palettes, tables and bob/controller wiring
remain unchanged. The landed watering/decorating checkpoint was merged at
the clean boundary; those four PNGs are unchanged by this refinement.

The original submitted ROM, current-main `4133f17748` ROM and refined ROM
each pass the same 13,448-assertion/320-capture water fixture. Two independent
complete 1x/4x comparison sets separate the pose-only refinement from the
full current-main water rollout. Older comparisons and ROMs remain preserved.
Helper/build, 9-capture smoke, three-sheet native gate, retained-effect and
unused-player source checks, and 22 audit/unused-player regressions pass.
ROM usage remains 23,040,960 bytes (68.67%). The refined native swimming
poses and retained dolphin are artistically accepted; independent integration
remains the coordinator's gate, not a full-town completion claim.

**Bounded retained-bike follow-on:** based on canonical `main` at
`7d17b62e9a`, only the four player `mach_bike.png`/`acro_bike.png` graphics
change. `player_bikes.py` is a private painter/checker, using read-only
accepted identity parts and explicit retained bicycle layers. All 72
source frames, atlas sizes, relative-frame tables, player/rival aliases,
animations, callbacks and palette files are retained. Ordinary pedaling
and moving-wheelie knee phases remain distinct.

The exact baseline and new ROM each pass 7,481 assertions and 736 captures
across 240 graphics/animation cases, including every ordered source phase,
hardware east mirror, full native OBJ VRAM transfers, all live palette
words/tags and finite/loop contracts. Complete 1x/4x native and real-ROM
comparisons require identical anchors and unchanged pixels outside the
forced bike sprite. These are idle-callback renderer fixtures in the
bedroom, **not controller gameplay**; the observer's Quickstart identity
is fixed only in test RAM. Helper/build, 26 source/audit regressions and
smoke (9 captures) pass.
ROM usage is 23,039,520 bytes (68.66%).

This checkpoint does not enable bikes, allocate a Greek replacement
vehicle, change the retirement policy, or redraw bike items/tracks/shop
tiles. Accepted water/watering/decorating/healing and ball-owned assets
are untouched. Terrain/furniture, other door/water animations, UI/item/
trade and other retained/global groups remain open; there is no whole-town
or global completion claim. Artistic approval and serial landing remain
the coordinator's gate.

**Coordinator retained-bike integration verification:** accepted source
`36f4207c6c` is integrated after nine-species main `4d0a21d8fe`, without
reapplying its clean-boundary merge or earlier water/effect equivalents.
Only the four assigned production PNGs change. All four private input
atlases match the exact pre-redraw sources; the 72 contact planes, identity
faces, frame counts and pedal distinctions pass their regressions.
Helpers, build, original smoke (nine inspected captures), 37 combined
source regressions and all four native image gates pass.

Both genuine post-nine/current ROMs pass 7,481 assertions and 736 captures
across all 240 player/rival animation cases. Every phase's complete 512-byte
OBJ transfer, dynamic palette, mirror, finite ending and loop cycle is
verified. All paired anchors match, with no changed pixels outside the
forced rider bounds. All four complete native cards and all 240 matched
engine case boards were inspected. These remain test-only bedroom renderer
fixtures, not bicycle-controller gameplay or eligibility proof.

All four complete compiled atlases match actual ROM bytes. Compared with
the nine-species baseline, exactly 9,166 bytes change inside those four
atlas ranges; every other byte of the padded ROM and the complete linker
map is identical. The retained healing, water, unused-player and
nine-species fixtures pass 7/37, 13,448/320, 242/34 and 192/43
checks/captures respectively. ROM use remains 23,039,552 bytes (68.66%);
the distributed GBA is padded to 33,554,432 bytes. GBA SHA256:
`5f796528804400cbd9c4253500f56db8ff211961cf6f0e915b0ca4e4dcde9153`.
Matching ROM/ELF/map, source snapshots, logs and all raw paired captures
are preserved in `player-bikes-integrated`. Original graphics-source
reconciliation reports 222 changed, no added/removed and 19,927 unchanged,
not a completion percentage. This accepts four retained rider sheets only;
bike policy, items/tracks/shop and the full sprite rollout remain open.

**Coordinator water integration verification:** source `f786a9ad25` and
accepted pose follow-up `4011f16e92` are applied without the housekeeping
merge or earlier Elaia equivalents. The combined snapshot retains the
accepted Akti portraits/Nemean family and four unused-player sheets.
Helpers, build, 9-capture smoke, three source/native image checks, retained
16-effect and unused-player source checks, and 22 audit/player regressions
pass. The actual post-portrait main ROM `bc616c533d...` and current ROM each
pass 13,448 checks with 320 captures. Complete matching boards are inspected;
the first mistaken positional-ROM invocation was discarded rather than
presented as before evidence. The new water/unused-player wrappers now honor
both a positional ROM and the existing `ROM` environment selector. Matching
ELFs and the corrected baseline command are retained with the captures.

ROM use is 23,039,520 bytes (68.66%), SHA256
`97f0cdc84363a24438c52d36728514447c2a51cfb6c3da07337a20d1102aff2b`.
The coordinator's `elaia-water-integrated` package preserves matching
GBA/ELF/map, authoritative `before`/`after` runs and complete 1x/4x
comparisons. Paths labeled `discarded` are not baseline evidence.
Source reconciliation reports 178 changed, no added/removed and 19,971
unchanged image/palette sources. Shared palettes, riders, unused-player
art and protected balls remain unchanged. Surf/Dive eligibility and
natural controller play are not claimed; all retained global groups remain
open.

**Coordinator integration verification:** Pokemon source checkpoint
`f247d1e645` was applied as `9ae5aff4af` on top of the landed human checkpoint
`dfb7974fbc`. The integrated `make -j$(sysctl -n hw.ncpu)` and original smoke
test pass; the ROM uses 23,041,920 bytes (68.67%), leaving 10,512,512 bytes.
The eleven-species native/import checks, separate Smoliv check, 96-check
real-engine gallery, all three full opening runs and 19 sprite-audit
regressions pass. Final introduction, Kleon/player portraits, starter battle
and Pylakyon gallery captures were visually inspected. Source reconciliation
against the original 20,149-image/palette baseline reports 112 changed
sources, no additions or removals and 20,037 unchanged sources. These are
coverage counts, not a declaration that the unchanged sprites are finished;
the ball owner's assets remain untouched.

**Coordinator effects integration verification:** source checkpoint
`b5ca00aa58` was applied alone as `70ff39b430`, retaining the earlier
coordinator ledger and both already-landed equivalent checkpoints.
`make -f make_tools.mk`, `make -j$(sysctl -n hw.ncpu)`, original smoke
(9 captures), all 16 source-exact/native PNG checks and 19 sprite-audit
regressions pass. Both the preserved post-Pokemon baseline and the combined
ROM pass `bash tools/ichor/tests/elaia_effects.sh` (538 checks / 229 captures
each). The integrated ROM uses 23,041,920 bytes (68.67%), leaving
10,512,512 bytes. Native effect/emotion artwork and rebuilt follower,
arrow, relic-state and introductory Smoliv captures were visually reviewed;
the bounded effect artwork is accepted. Fishing/surf/relic fixtures remain
rendering evidence, not controller/mount eligibility approval. The transient
white follower in the grass-step capture also exists in the baseline and
is not attributed to this redraw. Full source reconciliation now reports
129 changed, no added/removed and 20,020 unchanged image/palette sources.
All retained groups above remain in scope; neither these counts nor this
checkpoint declare every town sprite finished.

- **Audited against:** the remnants branch, which is `main` at `25526ae5dc` plus that pass's fixes (`design/phase1/UI_remnants.md`), with a clean `make` (devkitARM 16.1, Emerald build). Each row was checked by looking: in game for the screens (the slice playthrough, its side checks and gallery, and a screen harness), and in the repo for the rest.
- **Sizes** were measured at `c82f1634f7` from the linker map, `pokeemerald.map`, and `nm -S` on `pokeemerald.elf`, and have not been re-measured; only the ROM total below is current. Unsized assembly labels are sized by the gap to the next symbol. KiB means 1024 bytes. Sizes are good to a few percent, and the groupings are by symbol name and source file.
- **Update rule:** when a batch merges, flip its rows from **In progress (batch)** to **Greek** and fix the counts in the summary.
- **What a row means.** A row is an asset group or system. When the slice's part of a group is Greek and the rest waits on later maps (the item icons, the songs), the row says so in its notes and its phase.

## Legend

| Status | Meaning |
|---|---|
| **Greek** | Redrawn, rewritten or recomposed for Aethos, and in the repo. |
| **In progress (batch)** | A batch running in parallel owns it. Today that is only the main menu's backdrop (QA P6). |
| **Hoenn** | Still Emerald's. It must be replaced or rewritten. |
| **Cut** | A Hoenn-only system or asset to remove, with no replacement. Systems on ART_PLAN's cut list are marked "per ART_PLAN"; the rest are flagged for the director. |
| **Keep** | Generic, and fine as it is (the battle animations, move SFX and so on). |
| **New** | Nothing exists in the ROM yet and nothing Hoenn is in its place. It has to be built (relics, the Scroll of Deeds, the Aethos cast). This sixth status is not in the brief; it stops "not started" from being counted as "Hoenn". |

**Phase** is the roadmap phase in `design/PITCH.md` §8: **1** is the Kalliste slice, **2** Act I (Emporion, Eleusa), **3** Act II (Thyrsa, Arkadia, Astyra, Kaldera), **4** Act III through the Pantheon (1.0), **5** post-game, and **6** the polish sweep. **Batch** means a running batch owns the row. **Dex** means it waits for `design/dex/`. **Director** means it needs a decision.

## Summary

**226 rows** across 11 areas. Counts by status (a row is an asset group or system, so these are not file counts):

| Status | Rows |
|---|---|
| Greek | 87 |
| In progress (batch) | 1 |
| Hoenn | 42 |
| Cut | 47 |
| Keep | 32 |
| New | 17 |

| Area | Greek | In progress | Hoenn | Cut | Keep | New | Rows |
|---|---|---|---|---|---|---|---|
| 1. Overworld | 13 | 0 | 7 | 4 | 2 | 3 | 29 |
| 2. People | 11 | 0 | 4 | 5 | 0 | 5 | 25 |
| 3. Pokémon | 0 | 0 | 1 | 0 | 5 | 3 | 9 |
| 4. Battles | 5 | 0 | 2 | 2 | 5 | 0 | 14 |
| 5. Screens | 26 | 1 | 5 | 3 | 1 | 3 | 39 |
| 6. Items | 3 | 0 | 4 | 5 | 2 | 3 | 17 |
| 7. Text | 11 | 0 | 7 | 1 | 1 | 0 | 20 |
| 8. Audio | 7 | 0 | 6 | 4 | 3 | 0 | 20 |
| 9. Data | 3 | 0 | 2 | 5 | 2 | 0 | 12 |
| 10. Cuts | 0 | 0 | 1 | 17 | 2 | 0 | 20 |
| 11. Overlooked | 8 | 0 | 3 | 1 | 9 | 0 | 21 |

Two rows are new since the first count: the `agros` and `akti` tilesets, and the follower's balls.

Greek now covers everything the slice shows except the few items below: all 15 slice maps and their tilesets, the cast, townsfolk and classes, the boot sequence, title and speech, every everyday screen (bag, party, summary, Agora, popups, codex, Pithos, naming, options, trainer card, region map, klepsydra, starter table, evolution, berry tag, the Augur's Eye), the battle interface, backgrounds and transitions, the field effects, doors and ground jars, the slice's item icons, 36 songs, and the system text. The 42 Hoenn rows are almost all Hoenn's own maps, people, music and text, which go as Aethos's maps replace them in Phases 2-5.

**ROM now:** 25,648,568 bytes of the 33,554,432-byte limit (76.44 %, from `make`). That leaves 7,905,864 bytes (7.54 MiB) free.

**ROM the cuts would free** (measured at `c82f1634f7`):
- **ART_PLAN's list, with the Hoenn Frontier engine kept: 2.15 MiB (2,250,486 bytes).** That is contests, the Berry Blender, Pokéblocks, secret bases, Mirage Island, the PokéNav, e-Reader and Mystery Gift, the minigames, the link-only features, the Frontier maps and art, and FRLG data.
- **2.48 MiB (2,599,873 bytes) if the Frontier engine goes too.** The Olympiad needs it, so I recommend keeping it.
- **About 0.58 MiB more** if the director also approves the proposed cuts that are not on ART_PLAN's list (Mauville Old Man, TV, Easy Chat and mail, Safari Zone, transport, Apprentice, gym puzzles).
- **The cuts are small next to the dex.** Pokémon cries (9.4 MB) and species art and data (5.9 MB) were 57 % of the ROM. FRLG maps and tilesets are not built into the Emerald ROM at all, so cutting FRLG frees only 365 KiB.

**What a slice player can still see that is Hoenn**, ranked by how much a player would notice. Existing species art is left out, because the dex team owns it.

| # | What the player sees | Where | Owner | Rows |
|---|---|---|---|---|
| 1 | **The trade scene.** Kimon's Finizen trade in Glykera's bakery plays Emerald's trade art. | `graphics/trade/`, `src/trade.c` | UI | §5 |
| 2 | **The main menu's lavender backdrop** behind NEW GAME and CONTINUE (QA P6). | `src/main_menu.c`, `graphics/interface/main_menu_*.pal` | UI, in progress | §5 |
| 3 | **The codex's AETHOS counts** still count Hoenn's regional dex: SEEN AETHOS 3 for Geodude, Nosepass and Machop (QA m7). | `src/pokedex.c` | Dex team | §3 |
| 4 | **Emerald's item icons on held items.** Wild Pokémon in the slice may hold a Pretty Feather, Everstone, Light Clay, Metal Coat, Moon Stone, Luminous Moss, Dragon Scale or Poison Barb. | `graphics/items/icons/` | Items | §6 |
| 5 | **The berry pictures** on Bag > Berries > CHECK TAG: Emerald's Oran and Sitrus, on the new clay label. | `graphics/berries/` | Items, with the berry decision | §1, §5 |
| 6 | **The summary's RIBBON box** on the skills page, for a system Aethos hasn't decided on. | `src/pokemon_summary_screen.c` | Director | §11 |
| 7 | **Small expansion leftovers on the Augur's Eye:** the "R TO REGISTER!" line and the no-data "X". | `src/dexnav.c`, `graphics/dexnav/no_data.png` | Text, UI | §5 |
| 8 | **The save-failed screen's clock icon**, if a save ever fails. | `graphics/misc/clock_small.png` | UI | §5 |

---

## 1. Overworld

### Route 1 / Akti native redraw coverage

The second town-scoped polish pass covers **KallisteRoute1,
KallisteRoute1_KronionHill, AktiTown**, and all six implemented Akti interiors:
**TempleOfHestia, Asclepeion, Agora, FishersHouse, DiversHouse and
GoatherdsHouse**. The older **Greek** labels below record conversion, not approval
of this new native-art pass.

Map objects, all encounter periods and the referenced trainer parties establish
20 directly used species. Their complete evolution families contain 43 species.
Elaia owns the polished **Eripip** and **Galekit**, not their later stages.

| Coverage | Native redraw status |
|---|---|
| Halcyling, Galenyon | New matched native battle fronts, backs, six follower frames and two menu-icon frames implemented from `tools/dex/sprites/lines/halcyon.py` and its six hand-finished art grids. Existing normal/shiny color identities, palette files and bird footprints retained deliberately. Artistically accepted at checkpoint scope; final whole-town matched in-game review still pending. |
| Nemecub, Nemeleon | Native lion-family battle fronts/back grids, two icon frames and all six follower frames implemented in `lines/nemean.py` and six art grids. Animal muzzles, cub forelock/paws/tufted tail and mature mane/claws/armor retained. Normal palettes, exact shared icon palette3 and paw footprints retained; Nemeleon's blue-black shiny mane matches the ink-dark identity in `design/dex/species/nemean.yaml` in both battle/follower palettes. Scoped generation, native conversion/source checks and matching real-engine normal/shiny/front0/front1/back views pass. Artistically accepted at checkpoint scope. |
| Ione, Titan Grunt | Native three-quarter portraits and all nine walker states redrawn in `sprites_trainers.py` and `sprites_npc.py`. Their existing portrait and shared cast palettes retained unchanged; palette-correct native comparisons and genuine ROM portraits verified. Artistically accepted at checkpoint scope, not whole-town approval. |
| Eopeep, Alekrow, Hoplektor; Harpeck, Harpelle; Epopoi, Lophops, Basilops | Complete native two-front/back grids, two icon frames and six follower states implemented in the three family painters and 24 art grids. Independently authored miniatures preserve the rooster shields/crests, harpy leaf/plumes and hoopoe fans/barred wings without scaled battle-view drafts. Normal/shiny and exact engine-selected icon palettes, all bird footprints and Hoplektor's follower scale retained. Source/native/ROM-loader checks pass; complete normal/shiny cards artistically accepted at scoped checkpoint `b2e32f2997`, not whole-town acceptance. |
| Gelasable | Complete native two-front/back grids and eight miniature states implemented in `lines/weasel.py` and three hand-finished grids. Lower sinuous mustelid, turned laughing muzzle, dark collar/three gold torches and curled dark-tipped tail preserved. Normal/shiny colors and exact icon palette5 retained. Four-toe footprint pixels, colors and 1-bit depth retained; its PNG container was re-encoded, not kept byte-identical. Galekit's existing source/output remains protected. Complete native cards artistically accepted at scoped checkpoint `b2e32f2997`; source/native and matching real-engine views pass technical checks. |
| Kerazap, Kerastorm | Complete two-front/back hand-finished grids, two native icon states and six independently authored follower states implemented in `lines/amalthea.py`. Smaller goat faces, connected cloud ruffs/tails, slimmer prancing legs, whole sparkling horn buds and the mature long-left/broken-right cornucopia horns preserved. Fruit includes olive grapes, a fig with one pink accent and terracotta pomegranate; normal/shiny identities, all palette-file bytes, exact icon selectors 5/3 and hoof-footprint bytes retained. Eripip's source and all 18 design/ROM assets remain protected. Complete native cards artistically accepted at scoped source `ddcd3fb3d9`; independent combined source/ROM verification passes, not whole-town acceptance. |
| Karkipool, Karkitox; Ketofry, Kynoketos; Melibee, Melisseer; Onotis, Midonos; Ergant, Hoplomex; Narthip, Promethex; Elaleaf, Elapling, Hierolive; Spalunk, Plouteras; Kampillar, Nymveil, Psychora; Pebblith, Cairnolith, Laolith; Narkeray; Chelonet, Chelyra | These 26 owned species still await this batch's native polish; existing sprites retained, not claimed redrawn. This includes species used only by the local trainers. |
| Theo, Ianthe, Kleon, Alethea, Melitta; shared folk already polished in Elaia; pickups and starter kraters; Elaia's contact/shared effects | Elaia's human/opening-object checkpoint `dfb7974fbc`, twelve-species checkpoint `9ae5aff4af` and shared-effects checkpoint `70ff39b430` are integrated. All 16 effects/emotion sheets and the emote palette are preserved. Main `90d53010aa` also supplies accepted dolphin/underwater, unused watering/decorating, retained bicycle rider sheets and the deterministic healing fixture. None is redrawn by the goat checkpoint; further supported-player-state ownership stays outside this batch. |
| Kronion tablet | Markings and lighting refined at native 16x16 resolution, preserving the cast palette and wiring. Captured during the Route 1 review's real cutscene drop, not an ordinary summit visit. Artistically accepted at checkpoint scope. |
| Two upturned-boat halves | Direct native 32x16 drawing split into matched halves, replacing tileset extraction. Restrained plank seam and keel clusters use the existing cast palette. Native and real harbor evidence artistically accepted at checkpoint scope. |
| Sailor and Diver walkers | Eight-row native directional heads, longer cloth bodies, distinct strides and all nine engine frames implemented in `sprites_folk.py`. Costumes and folk palette preserved; Sailor's shoulder rope matches the existing portrait identity. Palette-correct complete sheets and real harbor before/after captured against the exact post-Elaia ROM. Artistically accepted at checkpoint scope. |
| Healer and Kid F walkers | Native eight-row directional heads, folded chiton and child-sized saffron tunic with complete strides. Healer's tenth bow frame retains closed eyes, head dip, hand over heart and planted serpent rod. All 19 states reproduce, and the preview now includes the full tenth frame. Both real heal paths hold the bow for exactly 32 frames and restore player control. Existing palette, costumes and animation wiring preserved; artistically accepted at checkpoint scope. |
| Augur and Acolyte M/F walkers | Native directional heads, longer indigo/linen robes, distinct strides and all 27 states implemented. Gold band/feather, sparse bird hem, planted staff, saffron cloth, soot/ash, tongs/coal and attached raised lamp preserved. Cast palette unchanged and verified in the ROM. Complete colored sheets and matched Route 1/Temple captures pass technical checks; artistically accepted at checkpoint scope. |
| Goatherd, Hoplite and Merchant walkers | Native directional heads, longer bodies and all 27 states implemented. Gray curls/beard, syrinx, goat-hair mantle, bell/thongs; raised Corinthian helmet, crimson crest/chiton, linen corselet, bronze greaves, spear/lambda shield; bald/full beard, blue/gold himation over linen and purse retained. Both shared palettes unchanged and verified in the ROM. Complete native sheets and actual placed/counter-occluded captures artistically accepted at checkpoint scope. Pilgrim is absent from these nine maps and belongs to the voyage/Aegina batch. |
| Shepherd, Harvester, Goatherd, Hoplite, Augur and Acolyte M/F portraits | All seven native 64x64 poses, directional faces, hands and equipment refined in `sprites_classes.py`; embedded palettes and class identities retained. Source/palette reproduction, connected lamp/arm and actual ROM-loader palette checks pass. Complete colored native and matching engine views preserved; artistically accepted at checkpoint scope. Merchant, Sailor and Pilgrim portraits are not used by those local trainers and belong to the voyage/Aegina batch. |
| Local healing effects | Both registered 24x16 relief states and the neutral 8x8 healing orb are refined with connected lighting and an unflashed blue lower waterline. Three source/format regressions and both real heal paths pass; live palettes, all eight relief commands, cleanup, exact 32-frame bows and restored movement verified. Artistically accepted at scoped checkpoint `975b2d610f`. Only these three sheets were regenerated; shared effects, palettes and Elaia's dolphin source remain unchanged. |
| Tiles, animated metatiles, battle backgrounds, UI, weather and move animations | Retained explicitly; not part of a native creature/character/object sprite redraw claim. Temple braziers and hearth-trial changes are metatiles, not object sprites. |

The town batch is **not complete**. Full shared regeneration and final ROM
evidence must follow integration of Elaia's landed polish so its assets are not
reverted. Greek god ball art has separate ownership and is excluded here.

The walker checkpoints preserve the other 12 folk sheets from the landed
Elaia base; all 22 arrays reproduce their checked-in PNGs. Native image checks,
helper compilation, `make -j$(sysctl -n hw.ncpu)` and smoke pass. The matching
gallery passes at all seventeen cameras across the nine maps, checking both
map identity and the overworld callback. The healer's talk
and whiteout regressions pass against both exact before and current ROMs.
`python3 -m unittest discover -s tools/ichor/tests -p test_folk_sprites.py`
checks source reproduction, complete distinct states, the planted rod and
uncropped tenth-frame preview. The walker ROM used 23,040,960 bytes (68.67%).
All local walkers are implemented and accepted at checkpoint scope.
The seven portraits and Nemean family are artistically accepted at scoped
checkpoint `1a111f80fc`, and local healing at `975b2d610f`.
The eight bird species and Gelasable are artistically accepted at scoped
checkpoint `b2e32f2997`, and Kerazap/Kerastorm at scoped source
`ddcd3fb3d9`; the remaining 26 owned species are not finished.

The seven-portrait/Nemean checkpoint passes six human-source regressions,
seven portrait native audits, both species native/import checks, helpers,
build and smoke. Both exact matching engine galleries pass 37 checks and
15 captures, including all 16 real portrait palette colors. Its ROM uses
23,039,520 bytes (68.66%); no production test fixture or new palette bank
was added.

The local healing refinement passes helpers, build, smoke, nine combined
human/healing source regressions and all three native image checks. Both
exact before/current talk and whiteout runs pass six script checks and
capture 16 relief pulse states each. All 16 accepted shared effect sheets
still pass their source-exact checker. Its ROM uses 23,039,232 bytes (68.66%).

The subsequent nine-species checkpoint passes helpers, build, smoke (nine
captures), nine native audits, source/import checks and 11 combined sprite
regressions. The eight birds reproduce all 72 indexed image/palette files
byte-exactly and pass 40 native tile round-trips, 32 LZ round-trips and 32
palette checks. Gelasable's hand-finished grids and all imported views
reproduce; Galekit's retained five image assets and palettes also reproduce.
Only those nine species' framing, grounding, shadow and Pokedex comparison
geometry was recalculated through `tools/dex/rom/gen.py::pics`; gameplay
fields and other species' metadata were not changed. A regression checks
all derived fields against the authoritative generator.

Both exact healing-base/current engine galleries pass 120 checks and 43
captures, including all normal/shiny front0/front1/back views, identical
front/back palette words, distinct shiny palettes and the seven retained
portrait loader views. These are actual engine-loader captures, not nine
natural battle playthroughs or follower-playthrough approval. Complete
native comparison cards show both icon frames, all normal/shiny follower
states and deliberately retained footprints. The ROM uses 23,039,552 bytes
(68.66%), leaving 10,514,880 bytes. All 16 shared effect sheets still pass
source-exact protection; this checkpoint does not regenerate shared player,
ball, human or dolphin assets.
The actual Route 1/Kronion story and Temple trial also pass with
`SPRITE_REVIEW=1` (81 and 39 captures respectively), preserving the tablet
drop, road reopening, class battles, Ione's portrait and Hearth Laurel flow.

At the child's clean `b2e32f2997` boundary, landed main `7d17b62e9a` is integrated
without amending the nine-species checkpoint or reapplying equivalent
Elaia/Akti commits. Both exact new-main/current creature galleries pass
120 checks / 43 captures. Their unoccluded central player regions are
pixel-identical; the old healing-base comparisons remain preserved separately.
All 33 source regressions, helpers, build, smoke, the pinned seven-check
healing fixture, retained 13,448-check / 320-capture water fixture and
242-check / 34-capture unused-player fixture pass. The accepted water,
unused-player and healing sources/assets match landed main exactly.
The combined ROM remains 23,039,552 bytes (68.66%); no new shared art
was authored during this boundary merge.

The following two-species storm-goat checkpoint passes helpers, build, smoke
(nine captures), all 34 source regressions, both species audits and native
gbagfx conversions. Native miniatures are scale-independent indexed drawings,
not resized battle fronts; all eight miniature states and the six hand-finished
battle grids reproduce. All Eripip code before the Kerazap section is
AST-identical to the prior source, and its 18 palette/image hashes are unchanged.
Only the goats' framing, grounding, shadow and Pokedex comparison geometry
was recalculated through `gen.pics`; gameplay and other species metadata
remain unchanged.

Both exact integrated `a334d7efb4` baseline/current loader galleries pass
43 checks / 15 captures, covering the four normal/shiny/front0/front1/back
states per goat plus seven retained portraits. All seven portrait screenshots
and the eight unoccluded player/room crops are pixel-identical between runs.
These are real engine-loader views, not natural goat battle or follower
playthroughs. Complete native before/current cards also show both icons,
all normal/shiny follower states and retained prints. The current ROM uses
23,038,528 bytes (68.66%), leaving 10,515,904 bytes. Shared human, player,
field-effect and ball assets were not regenerated. Technical completion of
these two species alone does not establish artistic or whole-town acceptance.

The effects integration also passes helper compilation, build, smoke, the
four folk regressions and `tools/ichor/art/check_elaia_effects.py`. Both
fourteen-camera galleries pass against the exact new main ROM and the
combined Akti ROM. The earlier post-Elaia Pokemon baseline and comparisons
remain preserved separately; no equivalent Elaia child commits were reapplied.

**Coordinator partial Akti walker integration verification:** accepted source snapshot
`2d1a23993f` includes the earlier accepted Ione/Titan, Halcyling/Galenyon,
tablet/boat and ten shared-walker checkpoints. Its existing merge of effects
main `840dbefb86` permits a fast-forward without reapplying Elaia equivalents.
The combined `make -f make_tools.mk`, `make -j$(sysctl -n hw.ncpu)` and original
smoke (9 captures) pass. Four folk regressions verify all 22 source arrays;
19 sprite-audit regressions, 13 regional species checks and all 23 changed
non-icon native PNG checks pass. The two changed icons pass the species-aware
shared-palette gate instead of the stricter generic BGR555 image gate.
The eleven retained Elaia species and both Halcyon species pass source-exact
view/import and native conversion checks. All landed field-effect/emotion
assets, their painters, shared palettes and protected ball paths are unchanged
from effects main. Both exact post-effects baseline and current ROM pass the
17-camera gallery (34 checks each) with map and overworld callback assertions.
The current Route 1 sprite review (81 captures) and Temple trial sprite review
(39 captures) pass; actual portraits, harbor, hill/market and smoke views were
inspected. The ROM uses 23,040,960 bytes (68.67%); SHA256 is
`127fc563fc314a7f96ffa451068452ff76d9113e0c7bf115a143f54d96fce055`.
Matching GBA/ELF/map and before/current captures are preserved as a partial
Akti checkpoint, not the eventual completed-town baseline. Original source
reconciliation reports 154 changed, no added/removed and 19,995 unchanged
image/palette sources. At that snapshot, seven local portraits, healing effects
and 39 owned species remained pending; subsequent acceptance above covers the
portraits and two Nemean species. Retained global groups remain in scope.

**Coordinator portrait/Nemean integration verification:** source `1a111f80fc`
is integrated through its clean `6798daf781` boundary, without reapplying the
earlier town/effects equivalents. The combined snapshot also preserves the four
unused-player sheets landed in `4133f17748`. Helpers, build and original smoke
(9 captures) pass; six human-source regressions and three unused-player
regressions pass. All 15 accepted regional species pass native checks; the
four Halcyon/Nemean species additionally match their generated views, all nine
design/game imports and exact source normal/shiny colors. All seven portraits
pass native/palette reproduction checks. Both matching before/current ROM
loader galleries pass 37 checks and 15 captures; the current unused-player
fixture still passes 242 checks and 34 captures. Route 1 and Temple sprite
reviews pass with 81 and 39 captures respectively; actual trainer portraits,
normal/shiny loader views and smoke are inspected. Loader galleries are
test-only, and these Quickstart-based scene checks are not a natural-save
playthrough. Shared effects, palettes, icon palettes, player sheets and
protected follower-ball paths remain unchanged from `4133f17748`.

ROM use is 23,039,520 bytes (68.66%), SHA256
`bc616c533d3737db3800fe0a20e0ffd07be3120e0704c4453ef9114a1db2da2f`.
Matching GBA/ELF/map, logs and paired captures are preserved in the
coordinator's `akti-classes-nemean-integrated` evidence package. Original source
reconciliation reports 175 changed, no added/removed and 19,974 unchanged
image/palette sources, not a completion percentage. The 37 owned species,
local healing and retained terrain/UI/global groups remain pending.

**Coordinator local healing integration verification:** accepted source
`975b2d610f` is integrated after water checkpoint `c6b66c5daa`, preserving
the landed dolphin/underwater and four unused-player sheets. Only the two
24x16 relief PNGs and neutral 8x8 orb change; every shared palette, other
human/effect sheet and ball-owned asset remains unchanged. Helpers, build,
original smoke (9 inspected captures), 31 human/healing/player/audit source
regressions, three healing image gates and retained water/effect/player
source gates pass.

The exact water-baseline and combined ROM each pass seven script checks and
37 captures, including all eight relief commands on both heal paths, live
palette equality, unflashed waterlines, cleanup, exact 32-frame bows and
restored player movement. Quickstart's random name/gender is pinned to Theo
in test RAM before the clinic warp: only the 16 pulse screenshots differ;
the other 21 paired screenshots are pixel-identical. Initial unmatched-player
runs are preserved as discarded evidence, not comparison proof. These are
Quickstart-assisted talk and forced-whiteout checks, not an unassisted
natural-save playthrough. The retained water and unused-player fixtures pass
13,448 checks/320 captures and 242 checks/34 captures respectively.

ROM use is 23,039,520 bytes (68.66%), SHA256
`55f7314b9a3862c216e7089a60d2c29fd9d23ed7b035556a2de84b550cbf147d`.
Matching ROM/ELF/map, logs, all raw captures and complete native/engine
comparisons are preserved in `akti-healing-integrated`. Original-source
reconciliation reports 181 changed, no added/removed and 19,968 unchanged
image/palette sources. This accepts local healing only; the 37 owned species
and remaining terrain/UI/global groups are not complete.

**Coordinator nine-species integration verification:** accepted source
`b2e32f2997` is integrated after healing main `7d17b62e9a`, without applying
the child's housekeeping merge. The eight birds and Gelasable receive
37 changed game PNGs and matching design imports. All palettes and footprint
pixels remain unchanged; Gelasable's footprint container alone is re-encoded.
Galekit, non-Gelasable family functions, shared players/humans/effects and
ball-owned assets remain protected. Only the nine species' derived sprite
geometry changes; all other metadata and gameplay fields are identical.

Helpers, build, original smoke (nine inspected captures), 33 combined source
regressions and nine species-aware native gates pass. All 81 compiled
front/back/icon/follower/footprint and normal/shiny palette assets match their
exact build bytes in the actual ROM. Both matching post-healing/current
engine galleries pass 192 checks and 43 captures, now comparing all 2,048
OBJ VRAM bytes for every front0/front1/back state as well as live palette
words. All seven retained portrait pairs are pixel-identical. These are
engine-loader fixtures, not nine natural battle or follower playthroughs.
Complete native and engine comparison boards were inspected.

Current Route 1 and Temple sprite reviews pass with 81 and 39 captures;
the retained healing, water and unused-player fixtures pass 7/37,
13,448/320 and 242/34 checks/captures respectively. Their assisted/forced
setup does not prove natural progression or controller eligibility.
ROM use is 23,039,552 bytes (68.66%), SHA256
`a334d7efb43f6516a0da42ed22a7900cb2fd76ae017a4fef6631d99c62e7e57e`.
Matching GBA/ELF/map, sources, logs and complete paired captures are preserved
in `akti-nine-integrated`. Original-source reconciliation reports 218 changed,
no added/removed and 19,931 unchanged image/palette sources, not a completion
percentage. The remaining 28 owned species and retained global groups are
still unfinished; this is not whole-town acceptance.

**Coordinator storm-goat integration verification:** accepted source
`ddcd3fb3d9` is integrated after retained-bike main `90d53010aa`, without
the child's boundary merges. Exactly eight game PNGs and their design
imports change. Both goats' palette/hoof bytes and all 18 Eripip assets are
unchanged; the Eripip painter prefix is AST-identical. Only Kerazap and
Kerastorm's derived sprite geometry changes, with no other metadata or
gameplay changes. All shared player/human/effect/ball assets are retained.

Helpers, build, original smoke (nine inspected captures), 38 combined source
regressions and both species-aware native audits pass. All 99 compiled
surface/palette assets across the eleven-species union match actual ROM
bytes. Both genuine post-bike/current engine-loader galleries pass 230
checks and 51 captures, including complete 2,048-byte front0/front1/back
OBJ transfers and live normal/shiny palettes. Only the eight goat captures
differ; all 43 retained full screenshots, including seven portraits, are
pixel-identical. Complete native cards and all paired engine boards were
inspected. These are renderer fixtures, not natural goat battles or follower
playthroughs.

Retained healing, water, unused-player and bicycle fixtures pass 7/37,
13,448/320, 242/34 and 7,481/736 checks/captures respectively.
ROM use is 23,038,528 bytes (68.66%), leaving 10,515,904 bytes; the GBA
file is padded to 32 MiB. GBA SHA256:
`871bf0ab2265c1eca4f702dddd0540c895f0569bc5be92a7cd630ee070500dec`.
Matching ROM/ELF/map, source snapshot, logs and complete paired captures
are preserved in `akti-goats-integrated`. Original graphics-source
reconciliation reports 230 changed, no added/removed and 19,919 unchanged,
not a completion percentage. The remaining 26 owned species and all
unaccepted global groups still require work; this is scoped acceptance only.

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Outdoor primary tileset `aethos` | `data/tilesets/primary/aethos/`, `porytiles/tilesets/gTileset_Aethos/`, `tools/ichor/art/aethos_*.py`, `design/phase1/TILES_aethos.md` | Greek | 1 | Replaces `general`: olives, cypress, limestone, Aegean, Asclepeion and Agora exteriors. Elaia, Route 1, Kronion Hill and Akti use it. 18 free tile slots. |
| Interior primary tileset `oikos` | `data/tilesets/primary/oikos/`, `design/phase1/TILES_oikos.md` | Greek | 1 | Replaces `building`: terracotta floors, klinai, amphorae. The TV becomes Mom's loom and the PC becomes the Pithos. Every slice interior uses it. |
| Secondary tilesets `kalliste`, `temple_hestia` | `data/tilesets/secondary/kalliste/`, `.../temple_hestia/`, `design/phase1/TILES_kalliste.md`, `TILES_temple.md` | Greek | 1 | Cycladic village, harbor, Kronion ruins and the Hestia temple interior. |
| Secondary tilesets `oikia`, `civic` | `data/tilesets/secondary/oikia/`, `.../civic/`, `design/phase1/TILES_oikia.md`, `TILES_civic.md` | Greek | 1 | Houses, the Asclepeion, the Agora and the Akademia. 48 civic tile slots are left. |
| Secondary tilesets `agros`, `akti` | `data/tilesets/secondary/agros/`, `.../akti/`, `tools/ichor/art/agros_*.py`, `akti_*.py`, `design/phase1/TILES_agros.md`, `TILES_akti.md` | Greek | 1 | Route 1's and Kronion Hill's countryside, and Akti's harbor. |
| Wiring the Greek tilesets into the slice maps | `data/layouts/layouts.json`, `data/maps/ElaiaVillage*`, `KallisteRoute1*`, `AktiTown*` | Greek | 1 | All 15 slice layouts are on Greek tilesets: aethos with kalliste, agros or akti outdoors, and oikos with oikia, civic or temple_hestia indoors. |
| Biome secondary tilesets to come | New `data/tilesets/secondary/*` | New | 2–5 | About 15: Astyra, Thyrsa vineyards and theater, Eleusa wheat and Mystery sanctum, Arkadia cypress forest, Kaldera caldera, Kythera coves, Knossa Labyrinth, Lakonia, Delphoi, Olympus, Underworld and Elysium, Atlantis (ART_PLAN §1). |
| Temple interiors for Hermes through Zeus, trireme decks, the Pithos room | New secondaries | New | 2–5 | The Hestia interior is the pattern. Table of orders and materials: ART_PLAN §1. |
| Hoenn secondary tilesets | `data/tilesets/secondary/*` (67 Hoenn folders, plus 62 FRLG folders that are not built) | Hoenn | 2–5 | Retired biome by biome as the Aethos maps replace Hoenn's. The Hoenn tilesets total about 428 KiB in the ROM. Frontier, Secret Base, Mirage Tower, Contest and Cable Club tilesets go with their systems (§10). |
| Hoenn primaries `general`, `building`, `secret_base` | `data/tilesets/primary/` | Hoenn | 2–5 | `aethos` and `oikos` replace the first two once every layout moves. `secret_base` is cut. `building_frlg` and `general_frlg` are not built. |
| Aethos tile animations | `include/porytiles_generated/tilesets/aethos/`, `src/tileset_anims.c` | Greek | 1 | Water, surf, waterfalls and anemones, at General's slots. |
| Hoenn tile animations | `src/tileset_anims.c` (25 `InitTilesetAnim_*` for Hoenn tilesets), `data/tilesets/secondary/*/anim/` | Hoenn | 2–5 | Dewford, Slateport, Mauville, Lavaridge steam, Pacifidlog bridges, Sootopolis, Underwater, Cave and the rest. About 116 KiB. |
| Door animations | `graphics/door_anims/` (85 sheets), `src/field_door.c` (25 KiB) | Greek | 1 | The five aethos doors open with Greek sheets (`graphics/door_anims/ichor_*.png`, `tools/ichor/art/doors.py`, `design/phase1/ITEMS.md`), and on an Ichor map no Hoenn door can play (`src/field_door.c`). The 85 Hoenn sheets stay for Hoenn maps and go with them. Kalliste's, akti's and civic's doors are non-animated by design. |
| Terrain contact effects | `graphics/field_effects/pics/`: `short_grass`, `tall_grass`, `long_grass`, `jump_*`, `cut_grass`, `sand_footprints`, `deep_sand_footprints`, `ripple`, `splash`, `water_surfacing`, `bubbles`, `ash*`, `bike_tire_tracks` and others | Greek | 1 | Tall grass (barley), long grass (reeds), sandal footprints, ripples, splashes and ledge dust are redrawn over the aethos tiles (`field_effects.py`, `design/phase1/FIELD_EFFECTS.md`). Ash, bubbles, deep sand and bike tracks are out of the slice's reach and take the new palettes. `bike_tire_tracks` is cut with bikes. |
| Shadows, emotes and sparkles | `graphics/field_effects/pics/shadow_*`, `emotion_*`, `emote_x`, `sparkle`, `shiny_sparkle`, `small_sparkle`, `graphics/misc/emotes.png` | Greek | 1 | The "!", "?", "!!", "X" and heart emotes are pottery shards (`FIELD_EFFECTS.md`), and so are the follower's eleven emotions (`graphics/misc/emotes.png`, `follower_icons.py`, `design/phase1/UI_remnants.md`). Shadows and sparkles are generic shapes. |
| Weather | `graphics/weather/` (9 files plus `drought*`), `src/field_weather*.c` | Keep | 6 | Rain, snow, fog, ash, sandstorm, drought, bubbles and clouds are generic. The Frozen Hour palette drain is an engine job. `sDroughtWeatherColors` is 49 KiB. |
| Asclepeion healing machine and monitor | `graphics/field_effects/pics/pokecenter_monitor.png`, `pokeball_glow.png`, `src/field_effect.c` | Greek | 1 | The rod-of-Asclepius relief lights gold and the healed balls float in the spring (`FIELD_EFFECTS.md`). Nurse text is §7. |
| Mart and Asclepeion light sprites | `graphics/object_events/pics/misc/poke_center_light.png`, `mart_light.png`, `light.png` | Hoenn | 2–5 | Window lights outside the doors. No slice map places one. Greek: oil lamps. |
| Berry trees | `graphics/object_events/pics/berry_trees/` (47 sheets), `graphics/berries/` (67 pics), `src/berry.c` | Hoenn | 2 | The bible says nothing about berries, and the slice already gifts an Oran Berry and a Sitrus Berry. Proposal: keep the system and restyle the trees and fruit as Greek fruit and herbs. Needs a director decision. |
| Cut, Rock Smash and Strength objects | `graphics/object_events/pics/misc/cuttable_tree.png`, `breakable_rock.png`, `pushable_boulder.png` | Hoenn | 2 | Field powers become relics (Labrys, Bronze Hammer, Girdle of Herakles). Greek: a thorn thicket or olive sapling, a marble rubble pile, a column drum. |
| Signs, statues and props | `graphics/object_events/pics/misc/sign.png`, `wooden_sign.png`, `gym_sign.png`, `statue.png`, `clipboard.png`, `birchs_bag.png`, `moving_box.png`, `town_map.png`, `pokedex.png`, `fossil*.png`, `old_amber.png`, `truck.png` | Hoenn | 2–5 | No slice map places any of them: the slice's signs are tiles, and its field objects are Ichor's (the Titanborn's tablet, the upturned boats). A temple stele for the gym sign comes first when a map needs one. `birchs_bag` and `truck` belong to Hoenn's opening and can go. |
| Item-ball pickups on the ground | `graphics/object_events/pics/misc/ichor_item_jar.png`, `tools/ichor/art/items.py` (Emerald's `ball_*.png` served it before) | Greek | 1 | A sealed clay jar: `OBJ_EVENT_GFX_ITEM_BALL` draws `ichor_item_jar.png` (`design/phase1/ITEMS.md`). Hoenn maps' item balls are jars too. |
| The follower's balls | `graphics/object_events/pics/misc/ball_*.png` (28), `tools/ichor/art/follower_icons.py` | Greek | 1 | At doors the follower goes into the party menu's black-figure ball. The other 27 balls keep their colors as painted caps (`design/phase1/UI_remnants.md`). The Poké Ball loads the townsfolk palette. |
| Event Pokémon sprites | `graphics/object_events/pics/pokemon_old/` (63) | Keep | Dex | Static overworld Pokémon (Azumarill, Kyogre and so on). Followers make most of them redundant. |
| Trireme and sailing sequence | `graphics/object_events/pics/misc/ss_tidal.png`, `graphics/ss_anne/` (wake, smoke), `src/ss_anne.c`, `src/seagallop.c` | New | 1–2 | The slice ends at the trireme in Akti's harbor, which the akti tiles paint at the quay. The bible replaces ferries with triremes. The moving trireme sprite and the crossing scene still need art. |
| Cable car | `graphics/cable_car/` (4), `src/cable_car.c` | Cut | 6 | Mt. Chimney only. Proposed in §10. |
| SS Tidal and ferries | `graphics/seagallop/`, `graphics/ss_anne/`, `mr_briney_boat.png`, `ss_tidal.png` | Cut | 6 | Replaced by triremes. Proposed in §10. |
| Secret-base decorations | `graphics/object_events/pics/dolls/` (41), `cushions/` (10), `graphics/decorations/` (43) | Cut | 6 | Per ART_PLAN (§10). |
| Hoenn gym puzzle mechanics | `src/rotating_gate.c` (16 KiB), Fortree and Mossdeep gym tiles and scripts | Cut | 6 | Used by Fortree Gym and Trick House 6 only. The Hearth trial is Ichor's own puzzle. Proposed in §10. |

## 2. People

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Theo and Ianthe: walking, running (Talaria wings), fishing (Old Rod), field-move (relic raise) | `graphics/object_events/pics/people/brendan/`, `.../may/`, `tools/ichor/art/sprites_player_ow.py`, `design/phase1/SPRITES_player_ow.md` | Greek | 1 | 4 of the 10 sheets each, and the surfing sheet below. The folders keep Brendan's and May's names and palettes (`brendan.pal`, `may.pal`), which also color the rival and link-player sprites. |
| Theo and Ianthe: surfing | `.../brendan/surfing.png`, `.../may/surfing.png` | Greek | 1 | Theo and Ianthe ride a Minoan dolphin (`surf_poses.py`, `surf_blob.png`, `FIELD_EFFECTS.md`). Poseidon's Conch, the relic that grants it, does not exist yet (§6). |
| Theo and Ianthe: underwater (Dive) | `.../underwater.png`, `tools/ichor/art/player_underwater.py` | Greek art / late state | 5 | Native swimming bodies landed at `c6b66c5daa`; all four source frames and the existing three-frame engine aliases/palette retained. Forced renderer evidence is not Atlantis traversal or Nereid Pearl eligibility. |
| Mach Bike and Acro Bike | `.../mach_bike.png`, `.../acro_bike.png`, `graphics/field_effects/pics/bike_tire_tracks.png`, `bike_shop` tileset | Native rider art / retired system | 6 | Four retained rider sheets have a bounded native checkpoint with unchanged engine contracts; no bikes enabled. Retirement policy, bike key items, tire tracks and shop maps/tiles remain untouched and outside this art checkpoint. |
| Watering and decorating poses | `.../watering.png`, `.../decorating.png` | Greek art / unused | 6 | Four native Theo/Ianthe sheets implemented at `4133f17748`; systems remain unavailable. Earlier retirement proposal is still tied to the berry/secret-base decisions, not enacted by this art checkpoint. |
| Ruby/Sapphire and FRLG player sheets | `.../people/ruby_sapphire_brendan/`, `ruby_sapphire_may/`, `rs_brendan.png`, `rs_may.png`, `leaf/`, `red/` | Cut | 6 | Never used by Aethos. |
| Player battle back pics | `graphics/trainers/back_pics/brendan.png`, `may.png`, `graphics/trainers/palettes/brendan.pal`, `may.pal`, `design/phase1/SPRITES_player.md` | Greek | 1 | Theo and Ianthe with throw animation. |
| Player front pics | `graphics/trainers/front_pics/brendan.png`, `may.png` | Greek | 1 | The boy-or-girl choice, the trainer card and the Birch speech use them. Ianthe's side of the choice was not captured in-game. |
| Other back pics | `graphics/trainers/back_pics/`: `brendan_rs`, `may_rs`, `red`, `leaf`, `steven`, `wally`, `old_man`, `pokedude`, `none` | Hoenn | 6 | 9 of 11 files are Hoenn, Kanto or tutorial characters. About 70 KiB of the 86 KiB of back pics. Alethea's new back pic (`alethea.png`) leads the catch tutorial in Wally's place, so `wally` and `old_man` are unused by Aethos. |
| Daphne, Alethea, Kleon, Ione, Titan grunt overworld sprites | `graphics/object_events/pics/people/ichor/`, `design/phase1/SPRITES_npc.md` | Greek | 1 | Shared palette `ichor_cast.pal`. |
| Kleon, Ione, Titan grunt, Daphne portraits | `graphics/trainers/front_pics/kleon.png`, `hierophant_ione.png`, `titan_grunt.png`, `professor_daphne.png`, `design/phase1/SPRITES.md` | Greek | 1 | Polish pass 1 done. Still open: 3/4 turns, more folds, Kleon's swagger pose, Ione unchanged. |
| Daphne in the new-game speech | `graphics/birch_speech/birch.png` | Greek | 1 | Same file as Birch's, so no code change. The text, Smoliv, the laurel-grove stage and the music are Ichor's too (§5, §7, §8). |
| Alethea portrait and back pic | none | New | 3 | Her back pic is drawn (`sprites_alethea_back.py`) and leads the catch tutorial. Her front portrait is not; she fights beside you in Act II's double battle. |
| The Twelve's Hierophants (2–8), the four Pantheon seats and the Archon | New `front_pics/`, `people/` | New | 2–5 | Ione is done. Names are in PITCH §3. |
| Team Titan admins (Hyperion, Iapetos, Rhea), Kronos and Phaedon, Elpis, Kallisto's hunt, the Fates | New | New | 3–4 | Phaedon is the healer behind the mask: his walker and portrait must read as the same man. |
| Townsfolk walkers (22) | `include/constants/event_objects.h:444-465` (aliases `OBJ_EVENT_GFX_ICHOR_*`), `graphics/object_events/pics/people/` | Greek | 1 | Drawn (`sprites_folk.py`, `design/phase1/SPRITES_folk.md`). Every person on the slice's maps is an Ichor sprite. |
| More civilians to reach about 40 types | New `people/` | New | 2–5 | Potters, philosophers, olive farmers, oracles, athletes and so on (ART_PLAN §2). |
| Hoenn and FRLG NPC walker sheets | `graphics/object_events/pics/people/*.png` (about 230 sheets including subfolders), 393 `OBJ_EVENT_GFX_*` ids | Hoenn | 2–5 | Retired as the Hoenn maps go. Keep the sheets of generic types (the shared poses) as palette bases only if useful. |
| Hoenn story characters and teams | `.../people/team_aqua/`, `team_magma/`, `gym_leaders/`, `elite_four/`, `frontier_brains/`, `steven.png`, `wally.png`, `wallace.png`, `prof_birch.png`, `scott.png` and similar | Cut | 6 | No counterpart in Aethos. Team Titan, the Hierophants and the Pantheon replace them. |
| Aethos trainer classes | `include/constants/trainers.h` (Lakonian, Shepherd, Harvester, Goatherd, Hoplite, Augur, Titanborn, Acolyte, Hierophant), `src/battle_main.c` `gTrainerClasses` | Greek | 1 | 9 classes. The bible wants about 25. |
| Aethos trainer-class portraits | `graphics/trainers/front_pics/shepherd.png`, `harvester.png`, `goatherd.png`, `hoplite.png`, `augur.png`, `acolyte_m.png`, `acolyte_f.png`, `design/phase1/SPRITES_classes.md` | Greek | 1 | 7 class portraits, plus the 4 cast portraits above, make 11 new pic ids. Front pics only. |
| Remaining Aethos classes and portraits (about 16) | New | New | 2–5 | Fisher, sailor, potter, hunter, philosopher, athlete, oracle, bronzesmith and the rest, as each biome needs them. |
| Hoenn trainer classes and pics | `include/constants/trainers.h` (66 Hoenn classes, 2 unused), `graphics/trainers/front_pics/`, `src/data/graphics/trainers.h` | Hoenn | 2–5 | 66 classes and 85 pic ids (83 untouched; Brendan and May were redrawn as Theo and Ianthe). All 158 front pics together are about 105 KiB. Aqua, Magma, Frontier, Contest and Battle Girl classes go with their systems. Suggested replacements from the nine class designs (the bible does not assign them): Hierophant for Leader, Titanborn for Aqua and Magma, Lakonian for Rival, Hoplite for Black Belt and Battle Girl, Augur for Psychic, Hex Maniac and Expert, Shepherd for Camper, Bug Catcher and Youngster, Harvester for Picnicker, Lass and Aroma Lady, Goatherd for Hiker and Ruin Maniac, Acolyte for the temple-room trainers. |
| FRLG trainer classes and pics | `include/constants/trainers.h` (50 `_FRLG` classes), `graphics/trainers/front_pics/*_frlg.png` (62), `back_pics/` | Cut | 6 | FRLG data is not otherwise built, but 62 pics are about 43 KiB of ROM. Per ART_PLAN. |
| Trainer-sighting music table | `src/data/trainer_approach_music.h` | Greek | 1 | Every jingle the slice's classes reach is Ichor's: the male, female, intense, suspicious, hiker, rival and Titan slots play `mus_ichor_encounter_*` (§8). Hoenn classes keep their Hoenn slots. |

## 3. Pokémon

The Aethos regional dex of about 150 species is designed separately in `design/dex/` (not in this worktree). How it mixes with the existing nine generations is still open (`PITCH.md` §4). So these rows say what each group costs and what depends on the decision. The existing species are generation 1 to 9 art, not Hoenn's alone.

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Existing species front, back, icon, footprint and palettes | `graphics/pokemon/` (1,029 folders), `src/data/pokemon/`, `src/pokemon.o` | Keep | Dex | 1,571 species and form entries. About 5.9 MB of ROM (22 %), about 3.7 KiB per form. The slice's starters and Route 1 mons use this art. Not Hoenn-specific. |
| New Aethos species (about 150): sprites, icons, footprints, palettes, shiny palettes, follower sprites | `graphics/pokemon/<species>/` | New | 2–5 | Gen 3 pic format. Done by biome as the story reaches them. |
| Cries | `sound/direct_sound_samples/cries/`, `sound/cry_tables.inc` | Keep | Dex | About 1,160 sampled cries: 9.4 MB, 35 % of the ROM, about 8 KiB each. The biggest single block in the ROM. Cries for removed species are the largest ROM lever (§10). |
| New Aethos cries | `sound/direct_sound_samples/cries/` | New | 2–5 | One per new species. |
| Follower and overworld Pokémon sprites | `graphics/pokemon/*/overworld*.png` | Keep | Dex | Followers are on (`e3dd2df4c2`). New species need theirs. |
| Pokédex entry text | `src/data/pokemon/species_info/` (descriptions) | Keep | Dex | New species need entries in Daphne's voice ("every myth is a memory of a Pokémon"). |
| Hoenn dex mode and Hoenn dex ordering | `src/pokedex.c` (`DEX_MODE_HOENN`, "HOENN DEX"), `src/data/` order tables | Hoenn | 1 | The codex lists by national number and the mode is named AETHOS DEX, but its AETHOS counts still walk Hoenn's regional order (QA m7). The dex team is building the Aethos order. |
| Fusion, Dynamax and Tera forms and art | species info, `graphics/battle_interface/*_indicator.png` | Keep | Dex | The bible turns Z-Moves, Dynamax and Tera off. Their art costs ROM but is harmless. |
| Apotheosis (Mega Evolution) trigger and Ichor Stones | `graphics/battle_interface/mega_trigger.png`, `mega_indicator.png`, 92 Mega Stone items | New | 4 | The trigger is painted as the Omphalos (§4). The 92 stones and the Apotheosis wording wait for Phase 4 (`design/TERMS.md`). All classic and Z-A Megas are in the species data. |

## 4. Battles

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Greek battle backgrounds: grass, sand, water, building (also gym, leader, plain, frontier) | `graphics/battle_environment/{tall_grass,sand,water,building,plain}/`, `src/data/battle_environment.h`, `design/phase1/BATTLE_BG.md` | Greek | 1 | 8 environments: the olive grove, Akti's shore, the open Aegean and the Doric temple hall with its leader, gym and plain variants. `KYOGRE` uses the water tiles in a storm palette. |
| Other Greek backgrounds still needed | `graphics/battle_environment/{cave,rock,long_grass,pond_water,underwater}/` | Hoenn | 2–5 | Cave, mountain, long grass, pond and underwater are still Emerald's. Needs: cypress forest, caldera, Labyrinth, Underworld, Atlantis, Olympus. |
| Elite Four, Champion and Pantheon halls | `graphics/battle_environment/stadium/`, `sky/`, `src/data/battle_environment.h` (Sidney, Phoebe, Glacia, Drake, Champion) | Hoenn | 4 | The Pantheon needs five Olympus halls. |
| Team Aqua, Team Magma, Groudon, Kyogre and Rayquaza backgrounds | same | Cut | 6 | No Aethos equivalent. The Primordials may need one scene each in Phase 5. |
| Expansion extra backgrounds (puddle, marsh, swamp, snow, ice, volcano, space and so on) | `src/data/battle_environment.h` | Keep | 6 | They reuse base tiles. |
| Healthboxes, HP and EXP bars, status and ball indicators | `graphics/battle_interface/` (71 files), `src/battle_interface.c` | Greek | 1 | Terracotta plaques, ink-drawn tubes and little kraters for the party balls (`design/phase1/UI_battle.md`). The type indicators beside the healthbox are generic (Keep). |
| Battle text box and action and move menus | `graphics/battle_interface/textbox*`, `move_info_window_*`, `src/battle_message.c` | Greek | 1 | The dialogue box itself, with ink-pointer menus on parchment (`UI_battle.md`). Wording is §7. |
| Battle transitions | `graphics/battle_transitions/` (23 files), `src/battle_transition.c`, `src/battle_transition_frontier.c` | Greek | 1 | Bands of a turning pot for wild battles and a black-figure face-off for trainers (`UI_battle.md`). The Aqua, Magma, Regi, legendary, Elite Four mugshot and Frontier set pieces are Hoenn's art, and no slice battle plays them. |
| Poké Ball sprites and capture sequence | `graphics/balls/` (29), `src/pokeball.c` | Keep | — | The director ruled that Poké Balls keep their name and look (`design/phase1/ITEMS.md`). The party menu, the battle tokens and the follower's balls paint them black-figure. |
| Throw, shake, open and move animations | `graphics/battle_anims/` (476 files), `data/battle_anim_scripts.s` | Keep | — | ART_PLAN keeps these. About 306 KiB of art plus 243 KiB of scripts. |
| Type and status icons | `graphics/types/` (28), `graphics/interface/status_icons.png`, `src/data/types_info.h` | Keep | 6 | Generic. Contest category icons in `graphics/types/` go with contests. |
| Mid-battle trainer slide tables | `src/trainer_slide.c` (`sTrainerSlides` 275 KiB, `sFrontierTrainerSlides` 94 KiB) | Keep | 6 | A feature to keep, but both tables are empty arrays sized by trainer count × 3 difficulties. About 369 KiB of ROM is zeros. 94 KiB is counted in the Frontier row (§10); the other 275 KiB is in no cut total. It shrinks when the Hoenn trainer ids go. |
| Frontier battle UI (Dome tourney tree, Factory, Arena, Palace and so on) | `src/battle_dome.c`, `battle_factory_screen.c`, `battle_arena.c`, `battle_palace.c`, `graphics/battle_frontier/` | Cut | 5 | Per ART_PLAN, except the engine that the Olympiad reuses (§10). |
| Apotheosis trigger button and flash | `graphics/battle_interface/mega_trigger.png` | Greek | 4 | The Omphalos, Delphi's netted stone: dim marble until pressed, then lit with golden ichor (`UI_battle.md`). The gimmick's wording waits for Phase 4. |

## 5. Screens

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Boot copyright screen | `graphics/intro/copyright.png`, `copyright.bin`, `src/intro.c` | Greek | 1 | Black gloss between meander rules: it credits Pokémon's makers and calls Ichor a fan-made game (`design/phase1/INTRO.md`). |
| Expansion "powered by" credit | `graphics/expansion_intro/`, `src/expansion_intro.c`, `EXPANSION_INTRO` in `include/config/general.h` | Greek | 1 | Restyled: "POWERED BY" over a gilded PRET × RHH, between meander rules (`INTRO.md`). It keeps the upstream attribution. |
| Game Freak logo and drops | `graphics/intro/scene_1/` (`drops_logo.png`, `logo.pal`, `sparkle.png`), `src/intro.c` | Greek | 1 | Replaced by the studio mark: a drop of ichor that blooms into ΙΧΩΡ (`INTRO.md`). |
| Latios, Latias, Flygon, Brendan and May intro | `graphics/intro/scene_2/` (bicycle, houses, `latias.png`, `latios.png`, `flygon.png`, `manectric.png`, `volbeat.png`) | Greek | 1 | Replaced by the black-figure frieze of Aethos that Clotho's thread runs along (`INTRO.md`). The bible maps Latias and Latios to the Dioskouroi (PITCH §4), so their art can return in a Greek scene later. |
| Legendary trio sequence | `graphics/intro/scene_3/`, `src/intro.c` | Greek | 1 | Replaced by the Fates' loom, where Atropos stops at the golden thread (`INTRO.md`). |
| Title screen: the Fates amphora | `graphics/title_screen/`, `src/title_screen.c`, `tools/ichor/art/title_screen.py`, `design/phase1/TITLE.md` | Greek | 1 | The music is Ichor's (§8), and the expansion's Quickstart badge is hidden (`QUICKSTART_HUD`). |
| Main menu (New Game, Continue, Options) and Continue panel | `src/main_menu.c`, `graphics/interface/main_menu_*.pal` | In progress (batch) | 1 | The Continue panel says LAURELS and the windows use the Greek frames. Another agent is repainting the lavender backdrop (QA P6). |
| Birch speech scene | `graphics/birch_speech/`, `src/main_menu.c` (about lines 1270–1830), `data/text/birch_speech.inc` | Greek | 1 | Daphne in the Akademia's laurel grove at dawn, with Smoliv, her own words and `MUS_ICHOR_NEW_GAME` (`design/phase1/UI_world.md`). The labels keep Birch's names so `main_menu.c` needs no logic changes. |
| Start menu | `src/start_menu.c`, `src/strings.c:427-433,874-884` | Greek | 1 | POKéDEX, AUGURY, POKéMON, BAG, the player's name, SAVE, OPTION and EXIT on the pottery frame. POKéNAV is defined but never shown. |
| Starter selection | `graphics/starter_choose/` (5), `src/starter_choose.c` | Greek | 1 | Three kraters on Daphne's table (`UI_world.md`). The flow is Emerald's, per ruling 11. |
| Naming screen | `graphics/naming_screen/` (16), `src/naming_screen.c` | Greek | 1 | A writing tablet and a wax keyboard (`design/phase1/UI_codex.md`). Defaults are THEO and IANTHE. |
| Options menu | `src/option_menu.c`, `graphics/text_window/1–20.png` | Greek | 1 | Twenty pottery frame choices (`text_window`). |
| Dialogue box, name box, signpost, menu frames | `graphics/text_window/` (24 files), `tools/ichor/art/ui_frames.py` | Greek | 1 | Terracotta, black-figure, with a meander border. |
| Bag screen | `graphics/bag/`, `src/item_menu.c` | Greek | 1 | The traveler's satchel (`design/phase1/UI_menus.md`). The Pyramid bag goes with the Frontier. |
| Party menu | `graphics/party_menu/`, `src/party_menu.c` | Greek | 1 | Clay plaques on terracotta (`UI_menus.md`). Its prompts are in sentence case (QA P3). |
| Summary screen | `graphics/summary_screen/`, `src/pokemon_summary_screen.c` | Greek | 1 | Papyrus unrolled from a scroll rod (`UI_menus.md`). The contest page is hidden. The skills page's RIBBON box is §11. |
| Shop | `graphics/shop/`, `src/shop.c` | Greek | 1 | The Agora's market stall (`UI_menus.md`). |
| Map-name popups | `graphics/map_popup/` (14), `src/map_name_popup.c` | Greek | 1 | Steles and plaques (`UI_menus.md`). |
| Pokédex | `graphics/pokedex/` (28), `src/pokedex.c`, `src/pokedex_area_screen.c` | Greek | 1 | A bronze-cornered codex (`UI_codex.md`). The area glow is gold hatching and the unknown Pokémon a clay roundel (`UI_remnants.md`). The HGSS dex is off. |
| Region map and Fly map | `graphics/pokedex/region_map*.png` (Hoenn, Kanto and Sevii maps), `src/region_map.c`, `src/field_region_map.c`, `src/data/region_map/` | Greek | 1 | A black-figure map of Aethos on all three screens (`UI_world.md`, `design/AETHOS_MAP.md`). The Kanto and Sevii maps are FRLG leftovers and never show. |
| Pithos storage screen | `graphics/pokemon_storage/` (92 files, 30 box wallpapers), `src/pokemon_storage_system.c` | Greek | 1 | Sixteen painted jars, named in the wallpaper menu (`UI_codex.md`). |
| Trainer card | `graphics/trainer_card/` (`badges.png`, bronze, copper, silver, gold, `bg.bin`), `src/trainer_card.c` | Greek | 1 | A kylix with a wreath of Laurels (`UI_world.md`). |
| Evolution scene | `graphics/evolution_scene/`, `src/evolution_scene.c` | Greek | 1 | A black-figure radiance (`UI_world.md`) with gold sparks (`UI_remnants.md`). |
| Trade scene | `graphics/trade/` (11), `src/trade.c` | Hoenn | 1 | Kimon's Finizen trade in Glykera's bakery plays it, so the slice shows Emerald's trade art. The GBA and cable art is link-only. |
| Hall of Fame | `src/hall_of_fame.c`, `graphics/misc/hall_of_fame.png`, `graphics/field_effects/pics/hof_monitor*` | Hoenn | 4 | The Pantheon's laurel hall. Its strings already say HALL OF HEROES (§7); the art is Emerald's. |
| Credits | `src/credits.c`, `src/data/credits.h` (57 staff pages), `graphics/credits/`, `graphics/intro/scene_2/*_credits.png` | Hoenn | 4 | Emerald's Game Freak staff roll and the bike scenery. See §11. |
| Dex diploma | `graphics/diploma/` (Hoenn and National palettes), `src/diploma.c` | Hoenn | 4 | Signed PROF. DAPHNE now (§7). The art is Emerald's. |
| Wall clock | `graphics/wallclock/`, `src/wallclock.c` | Greek | 1 | The klepsydra (`UI_world.md`). |
| DexNav (the Augur's Eye) | `graphics/dexnav/` (9), `src/dexnav.c`, `include/config/dexnav.h` | Greek | 1 | An augur's tablet (`design/phase1/UI_remnants.md`, QA P5). The register line still reads the expansion's "R TO REGISTER!". |
| Scroll of Deeds (quest log) | `src/ichor_deeds.c`, `data/scripts/ichor_deeds.pory`, start-menu DEEDS | Greek | 3 | Playable text pages on the shared pottery frame: Act I receipts, amphora leads, herms, Stylus hints and calendar. No separate scroll illustration or key-item icon. Later-chapter pages remain. |
| Star Chart screen | `src/ichor_star_chart.c`, key-item Bag USE | Greek | 3 | Original parchment and 24 line patterns on three BG layers, with gold palette twinkling. Unplaced patches stay empty. Outdoor seats and reward scenes remain; the Bag item icon is still the upstream Town Map stand-in. |
| Difficulty select and the Oath of the Styx | not in the ROM as screens | New | 1 | The bible's four difficulties and the Nuzlocke oath need a new-game screen. `include/constants/difficulty.h` exists. |
| Laurel case | not in the ROM | New | 1 | ART_PLAN §5. Could share the trainer card's laurel art. |
| Save prompt and save info panel | `src/start_menu.c`, `src/strings.c:957` (`gText_SavingBadges`), `data/text/save.inc` | Greek | 1 | PLAYER, LAURELS and TIME on the pottery frame, with the place in the dialogue red. |
| Reset-clock and save-error screens | `graphics/reset_rtc_screen/`, `src/reset_rtc_screen.c`, `src/main_menu.c:259-262` | Keep | 6 | Generic text on the pottery frames. The save-failed screen stands on the Akademia art of the starter table; its small clock icon (`graphics/misc/clock_small.png`) is Emerald's. See §11. |
| Easy Chat and Mail | `graphics/easy_chat/` (9), `graphics/mail/` (12 mail designs), `src/easy_chat.c` | Hoenn | Keep | Kept for now ("where safe"): mail items and the Frontier still use them. 45 KiB. |
| Berry tag and berry check | `graphics/bag/berry_tag*`, `check_berry*`, `src/berry_tag_screen.c` | Greek | 1 | A clay label tied with twine (`ui_berry_tag.py`, `UI_remnants.md`). The berry pictures (`graphics/berries/`) are still Emerald's fruit, with the berry decision (§1). |
| Pokémon Jump, Berry Crush, Dodrio picking, slot machine and roulette screens | `graphics/pokemon_jump/`, `berry_crush/`, `dodrio_berry_picking/`, `slot_machine/`, `roulette/` | Cut | 6 | Per ART_PLAN, as minigames (§10). |
| Contest, Berry Blender, Pokéblock, PokéNav, Union Room, Mystery Gift, Wonder Card and secret-base screens | `graphics/contest/`, `berry_blender/`, `pokeblock/`, `pokenav/`, `union_room_chat/`, `wonder_card/`, `wonder_news/`, `link/`, `wireless_status_screen/` | Cut | 6 | Per ART_PLAN (§10). |
| Link and Frontier screens: Frontier Pass, Trainer Hill, picture frames | `graphics/frontier_pass/`, `graphics/picture_frame/` | Cut | 5 | See §10. |

## 6. Items

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Item icons, 874 items | `graphics/items/icons/` (619 PNGs), `graphics/items/icon_palettes/`, `src/data/items.h` | Hoenn | 2–5 | All Emerald and expansion icons except the slice's 34, which are Greek (row below; `items.py`, `design/phase1/ITEMS.md`). About 115 KiB. Restyle phase by phase. Items wild Pokémon may hold in the slice (Pretty Feather, Everstone and others) keep Emerald's. |
| Medicines and battle items | `graphics/items/icons/` | Greek | 1 | The slice's: clay flasks, herb bundles tied with colored wool, amphoriskoi of nectar and incense cones (`ITEMS.md`). The rest go with the row above. |
| Poké Balls and their cases | 28 ball items, `graphics/items/icons/*_ball.png`, `graphics/balls/` | Keep | — | Director's ruling: the name and look stay (`ITEMS.md`). See §4. |
| Berries | 68 berry items, `graphics/berries/` | Hoenn | 2 | Oran and Sitrus are a fig and a quince (`ITEMS.md`); the other 66 are Emerald's. See §1. 15 berry descriptions end with "{POKEBLOCK} ingredient". |
| TMs and HMs | 108 items (100 TMs, 8 HMs), `graphics/items/icons/tm.png`, `hm.png`, `tm_case.png` | Greek | 1 | Every TM is a sealed papyrus scroll and every HM a wax tablet, in the type's color (`ITEMS.md`). The eight HMs become relics (next row). |
| Field-power relics | none (`ITEM_TALARIA`, `ITEM_LABRYS` and the rest do not exist) | New | 1–3 | Talaria (run), Daedalus's Wings (Fly), Poseidon's Conch (Surf), Bronze Hammer (Rock Smash), Labrys (Cut), Girdle of Herakles (Strength), Hecate's Torch (Flash), Nereid Pearl (Dive): 0 of 8 exist. The player's field-move pose already raises a relic. Waterfall has no relic in PITCH §5. The slice needs only the Talaria, which Mom gives you in beat 1. |
| Omphalos (Mega key stone) | `ITEM_MEGA_RING` (key item "Mega Ring") | New | 4 | Rename and redraw. |
| Ichor Stones (Mega Stones) | 92 Mega Stone items | Hoenn | 4 | Redraw as one shared icon family with per-stone glints. |
| Laurels (badges) | `graphics/trainer_card/badges.png`, item/flag `FLAG_BADGE01_GET…08` | Greek | 1 | The trainer card's wreath gilds a leaf with its god's emblem for each Laurel (`UI_world.md`). The Hearth Laurel is the slice's reward. |
| Augur's Eye, Scroll of Deeds, Laurel case | key items | New | 1–3 | Icons for the Talaria, the Augur's Eye, the codex and the Hearth Laurel are drawn but not wired, because the slice keeps them as flags (`ITEMS.md`). The Scroll of Deeds and the Laurel case have no item yet. |
| Hoenn and Kanto key items | `src/data/items.h` (about 37: S.S. Ticket, Devon Parts, Go-Goggles, Devon Scope, Basement Key, Scanner, Storage Key, four Room Keys, Meteorite, Magma Emblem, Contest Pass, Letter, Eon, Mystic and Aurora Tickets, Old Sea Map, Parcel, Secret Key, Bike Voucher, Gold Teeth, Card Key, Lift Key, Silph Scope, Tri-Pass, Rainbow Pass, Tea, Ruby, Sapphire, Wailmer Pail, Poké Flute, Soot Sack, Teachy TV, Fame Checker) | Cut | 6 | No place in Aethos. |
| Bikes | Bike, Mach Bike, Acro Bike, Bike Voucher | Cut | 6 | See §2. |
| Contest items | 5 Contest Scarves, {POKEBLOCK} Case, Contest Pass | Cut | 6 | Per ART_PLAN (§10). |
| Items for gimmicks the bible turns off | 35 Z-Crystals, Z-Power Ring, Dynamax Band, Dynamax Candy, Max Mushrooms, Max Honey, Tera Orb, 19 Tera Shards | Cut | 6 | PITCH §5: only Apotheosis stays. Proposed. |
| Names that say Hoenn or Kanto | "Poké Ball", "Poké Doll", "Poké Toy", "Poké Radar", "Poké Flute", "Pokéshi Doll", "Devon", "S.S." | Hoenn | 6 | The bible's "Pokémon" is kept, so "Poké Ball" may stay. Decide the ball family name once (§4). |
| Mail items (12 designs) | `graphics/mail/` | Cut | 6 | With Easy Chat. |
| Fossils, Apricorns, shards, other generic items | `graphics/items/icons/` | Keep | 6 | Names and icons are generic. Restyle opportunistically. |

## 7. Text

Counts are matching lines or strings from `grep`, so they are not exhaustive.

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| New-game speech | `data/text/birch_speech.inc` (3 Birch blocks), `src/strings.c:46`, `src/main_menu.c` | Greek | 1 | Daphne's speech ("every myth is a memory of a Pokémon"). The labels keep Birch's names. |
| Starter-choice strings | `src/strings.c:63-64` | Greek | 1 | "Three Pokémon. Three kraters." and "Will this Pokémon be your partner?" |
| Whiteout and rescue messages | `src/field_screen_effect.c:64,66,1471` | Greek | 1 | "hurried to the Asclepeion" and "hurried back home". No PROF. BIRCH remains. |
| Asclepeion nurse text | `data/text/pkmn_center_nurse.inc` (10 strings), `data/scripts/pkmn_center_nurse*.inc` | Greek | 1 | The healer speaks Ichor's lines (ruling 6); the Hoenn copies stay for Hoenn's centers. |
| Pithos (PC) strings | `data/text/pc.inc`, `data/scripts/pc.inc` ("SOMEONE'S PC", "LANETTE'S PC") | Greek | 1 | The Pithos and its jars (ruling 6). |
| Start and main menu labels | `src/strings.c:427-433,874-884`, `src/main_menu.c:277` | Greek | 1 | AUGURY, LAURELS, POKéDEX. POKéNAV is defined but never shown. |
| Pokédex dex-mode titles | `src/pokedex.c:1184`, `src/strings.c:904,909` | Greek | 1 | AETHOS DEX and NATIONAL DEX. The counts behind AETHOS are §3. |
| Pokédex rating | `data/text/pokedex_rating.inc` (about 25 rating blocks), `src/strings.c:53` | Greek | 4 | Daphne gives the rating; no HOENN or BIRCH remains. |
| Hall of Fame and diploma text | `src/strings.c:57,63,906`, `src/hall_of_fame.c` | Greek | 4 | "ARCHON OF AETHOS!", HALL OF HEROES, and the diploma signed PROF. DAPHNE. |
| Battle messages that name Hoenn people | `src/battle_message.c` (`STRINGID_DONTLEAVEBIRCH`, `gText_WhatWillWallyDo`, `gText_BattleWallyName`, the Wally catch tutorial, the champion lines at `:1524-1527`) | Greek | 1 | Daphne and Alethea stand in for Birch and Wally. No other battle line names a Hoenn person; the Battle Arena referee's lines go with the Frontier (§11). |
| Trainer class names | `src/battle_main.c` `gTrainerClasses` | Hoenn | 2–5 | 9 Aethos names are in. 116 Hoenn and FRLG names remain, including "ELITE FOUR", "CHAMPION" and "LEADER". |
| Place names and landmarks | `src/data/region_map/region_map_sections.json` (241 map sections; 32 are Aethos's), `src/landmark.c` (27), `src/data/heal_locations.json` (44) | Hoenn | 2–5 | Kalliste's three sections and 29 more Aethos sections are in (`UI_world.md`), so the popups, the Fly map and the summary's "Met at" name ELAIA VILLAGE, ROUTE 1 and AKTI TOWN. Hoenn's 209 sections and 27 landmarks stay with Hoenn's maps. |
| Hoenn words in strings: HOENN, BIRCH, POKéNAV, POKéMON CENTER, MART, GYM, LEAGUE | the files in the rows above, plus `data/text/*.inc` and `src/data/*.h` | Hoenn | 1–5 | The count below is matching string lines (FRLG left out). System text and shared scripts: HOENN 14, BIRCH 4, POKéNAV 41, POKéMON CENTER 14, GYM 105, LEAGUE 24, down from 20, 10, 41, 19, 105 and 27; what is left serves Hoenn's systems and cut ones, and the slice's 269 messages show none. Hoenn map scripts: HOENN 42, BIRCH 45, POKéNAV 53, POKéMON CENTER 8, MART 13, GYM 169, LEAGUE 43. The map scripts go with the maps. "POKé MART" never appears as a string. |
| Trainer dialogue | `data/text/trainers.inc` (2,507 string lines, about 855 Hoenn trainers) | Hoenn | 2–5 | Mentions GYM BADGES, LEAGUE and CHAMPION. The 14 Ichor trainers' text is in `SCRIPT.md`. |
| Hoenn map-script dialogue | `data/maps/*/scripts.inc` (about 520 non-FRLG folders, 15,700 string lines) | Hoenn | 2–5 | Hoenn counts: 42 "HOENN", 45 "BIRCH", 53 "POKéNAV", 169 "GYM", 43 "LEAGUE", 63 "TEAM AQUA", 65 "TEAM MAGMA", 53 "CONTEST", 8 "POKéMON CENTER". Goes away with the maps. |
| Slice dialogue | `design/phase1/SCRIPT.md`, `data/maps/{ElaiaVillage*,KallisteRoute1*,AktiTown*}/scripts.pory` | Greek | 1 | The maps and scripts batch, in Poryscript. The slice's 269 messages show no Hoenn word (QA). |
| Story, tutor and lottery text | `data/text/move_tutors.inc` (Mossdeep, Sootopolis gyms), `apprentice.inc`, `mauville_man.inc`, `lottery_corner.inc`, `tv.inc`, `match_call.inc` (69 lines), `fame_checker_frlg.inc` | Cut | 6 | Most go with their systems (§10). Move-tutor text needs a rewrite if tutors stay. |
| Berry descriptions that mention Pokéblocks | `src/data/items.h` (15 berries, "{POKEBLOCK} ingredient") | Hoenn | 2 | Goes with the Pokéblock cut. |
| Item descriptions | `src/data/items.h` | Hoenn | 2 | Mostly generic. A few mention Contests, Devon Corp and Poké Flute. |
| Shared strings that say Pokémon | `src/strings.c`, `src/battle_message.c` and the party and summary screens | Keep | 6 | The title is "Pokémon Ichor", so "POKéMON" and the `{PKMN}` glyph stay. Decide once and record it (§11). |

## 8. Audio

Songs by use. Counts are from `include/constants/songs.h` and sizes are from the map (KiB of ROM). The ROM holds about 220 songs.

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Ichor songs: Elaia, Route 1, Akti, Hestia temple, Asclepeion, Titan, trainer, wild and rival battle themes, trainer victory | `sound/songs/midi/mus_ichor_*.mid` (10, 16 KiB), `sound/voicegroups/` Ichor voicegroup, `tools/ichor/music/` | Greek | 1 | 36 songs, among them every slice town, route, building and battle theme, the encounter jingles, the fanfares, the title and the intro. Registered at the end of `song_table.inc`, with 27 Emerald slots repointed. |
| Slice fanfares and the rest of the slice's songs | `include/constants/songs.h` | Greek | 1 | Every song and fanfare the slice plays is Ichor's: caught, victories, level up, heal, badge, item, evolved, TM and evolution, the title, the intro and the speech. |
| Title theme | `MUS_TITLE` in `src/title_screen.c:671` | Greek | 1 | `MUS_TITLE` plays `mus_ichor_title`. |
| Intro tracks | `MUS_INTRO`, `MUS_INTRO_BATTLE` in `src/intro.c:1208,1731` | Greek | 1 | `MUS_INTRO` plays `mus_ichor_intro`. `MUS_INTRO_BATTLE` belonged to the legendary scene, which is gone. |
| New-game speech music | `src/main_menu.c:1291` (`PlayBGM`) | Greek | 1 | `MUS_ICHOR_NEW_GAME`. |
| Towns and cities | 13 songs, 49 KiB: Littleroot, Oldale, Petalburg, Rustboro, Dewford, Slateport, Verdanturf, Fallarbor, Fortree, Lilycove, Sootopolis, Ever Grande (plus a test track) | Hoenn | 2–5 | One theme per Aethos town as it arrives. |
| Routes, woods and travel | 17 songs, 56 KiB: Routes 101, 104, 110, 113, 118, 119, 120, 122, Petalburg Woods, cycling, surf, sailing, underwater, desert, two GSC leftovers, Follow Me | Hoenn | 2–5 | Cycling is cut with bikes. |
| Dungeons and set pieces | 12 songs, 39 KiB: Mt. Chimney, Mt. Pyre (and exterior), Cave of Origin, Abandoned Ship, Sealed Chamber, Aqua/Magma hideout, Victory Road, abnormal weather, Groudon weather, Awaken Legend, Rayquaza appears | Hoenn | 3–5 | Keep the shape of a few (cave, victory road) as Aethos dungeons. |
| Buildings and indoor | 8 songs, 20 KiB: Pokémon Center, Mart, Gym, Birch Lab, Pokémon School, two museums, Help | Hoenn | 2–5 | The slice plays Ichor's Asclepeion, temple, Agora and Akademia themes; its houses play their town's. These Hoenn songs serve Hoenn's maps. |
| Battle themes | 14 songs, 45 KiB: wild, trainer, gym leader, rival, Aqua/Magma, champion, Elite Four, Kyogre/Groudon, Rayquaza, Regi, Mew, Frontier Brain, legend beast, intro battle | Hoenn | 2–4 | The Ichor wild, trainer and rival themes exist. Still needed: Hierophant, Titan admins, Pantheon, Archon, Kronos and Dialga. |
| Trainer-sighting jingles | 17 songs, 39 KiB (`MUS_ENCOUNTER_*`) | Greek | 1 | The slots the slice's classes reach play `mus_ichor_encounter_*` (§2). The Hoenn jingles stay for Hoenn's classes. |
| Fanfares and jingles | 18 songs, 24 KiB: caught, victory (wild, trainer, leader, league, Aqua/Magma, road), level up, heal, badge, item, evolved, TM, evolution (and intro), move deleted, berry, "too bad" | Greek | 1 | Every fanfare the slice plays is Ichor's. The berry, move-deleted, "too bad" and league jingles are Emerald's, and the slice never plays them. |
| Title, credits, Hall of Fame | 6 songs, 32 KiB: title, intro, credits, end, Hall of Fame, HoF room | Hoenn | 4 | The title and intro are Ichor's (rows above). The credits, end and Hall of Fame songs come with Act III. |
| FRLG songs | 75 songs, 239 KiB (`mus_rg_*`) | Cut | 6 | Per ART_PLAN. Built into the ROM. |
| Songs of cut systems | 31 songs, 94 KiB: contests, link contests, Frontier, Game Corner, slots, roulette, Trick House, Safari Zone, Cable Car, match call | Cut | 6 | Counted in §10. |
| Sound effects (269) | `sound/songs/midi/se_*.mid` (31 KiB total), `include/constants/songs.h` | Keep | — | 227 are generic: 130 move effects and about 97 UI, battle and field sounds (menu, door, ball, level up, faint, ledge, dex and so on). |
| Hoenn-specific sound effects | `SE_POKENAV_*` (4), `SE_CONTEST_*` (8), `SE_BERRY_BLENDER` (1), `SE_ROULETTE_*` (2), `SE_PIKE_*` (2), `SE_ARENA_*` (2), `SE_TRUCK_*` (4), `SE_BALLOON_*` (3), `SE_RG_*` (15), `SE_SUDOWOODO_SHAKE` (1) | Cut | 6 | 42 effects that go with their systems. Under 5 KiB. |
| Instruments, voicegroups and mixing | `sound/direct_sound_samples/` (107 samples, 754 KiB), `sound/voicegroups/` (183 files, 249 KiB) | Keep | 1 | The shared engine. The Ichor voicegroup (`ichor.inc`) maps Greek roles (lyre, kithara, aulos, frame drum) onto existing Emerald samples, so there are no new sampled instruments yet. |
| Cries | `sound/direct_sound_samples/cries/` | Keep | Dex | See §3. |
| Mauville Old Man phonemes | `sound/songs/midi/ph_*.mid` (51), `sound/direct_sound_samples/phonemes/`, `src/bard_music.c` | Cut | 6 | 162 KiB. Proposed (§10). |

## 9. Data

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Hoenn maps | `data/maps/`, `data/layouts/` | Cut | 2–5 | Removed by hoenn-cut batch 2 with their layouts, scripts, encounter tables, heal locations and the tilesets only they used. What's left is the Ichor maps and, until batch 3, the Battle Frontier and Trainer Hill maps. `include/constants/maps_removed_stub.h` keeps the removed names compiling for upstream code. |
| Ichor maps | `data/maps/{ElaiaVillage*,KallisteRoute1*,AktiTown*}`, `data/ichor_maps.inc` | Greek | 1 | 15 maps: Elaia and its four interiors, Route 1, Kronion Hill, Akti and its six interiors, all on Greek tilesets, with Poryscript scripts. |
| FRLG maps, tilesets and scripts | `*_Frlg` maps, `*_frlg` tilesets and scripts | Cut | 6 | Removed by hoenn-cut batch 2. They were never in the Emerald ROM. A few FRLG tileset animation frames stay, because `src/tileset_anims.c` names them. On upstream merges, resolve modify/delete conflicts on these paths with `git rm`. |
| Hoenn trainers | `src/data/trainers.party`, `include/constants/opponents.h`, `src/data/battle_partners.party` (2) | Cut | 2–5 | Removed by hoenn-cut batch 1: 847 Hoenn trainers gone, Ichor's 14 renumbered 1–14, and the seven Frontier Brains kept at 15–21 for the Frontier engine. `gTrainers` fell from 132 KiB to 3.4 KiB and now grows only with real trainers. Id ranges per session are in `tools/ichor/claim_ranges.md`. `PARTNER_STEVEN` is still there. FRLG's 624 trainers in `trainers_frlg.party` are not built. |
| Trainer-slide tables | `src/trainer_slide.c` | Keep | 6 | 187 KiB of mostly empty pointers: `sTrainerSlides` (156 KiB, (`MAX_TRAINERS_COUNT` 1,536 + partners) × 26 slides) and `sFrontierTrainerSlides` (30 KiB). Ichor keeps one difficulty's slides for every difficulty, a third of upstream's size. A sparse table would free most of the rest. |
| Hoenn wild encounter tables | `src/data/wild_encounters.json` | Cut | 2–5 | Removed by hoenn-cut batch 2: 388 Hoenn and FRLG headers. |
| Heal locations | `src/data/heal_locations.json` | Greek | 1 | Elaia and Akti, plus the Battle Frontier's until batch 3. |
| Fly destinations and region sections | `src/data/region_map/` (241 sections) | Greek | 1 | The Aethos map's sections, with Elaia and Akti as fly targets (`UI_world.md`). Hoenn's sections stay until their maps go. Hoenn's sections 0–85 are now free `MAPSEC_OIKOUMENE_*` slots (hoenn-cut batch 2; see `tools/ichor/claim_ranges.md`). |
| Flags and vars | `include/constants/flags.h`, `vars.h` | Keep | — | Hoenn-cut batch 2 freed 700 flags and 95 vars. The per-session ranges are in `tools/ichor/claim_ranges.md`. |
| Mart stock, tutors, in-game trades, apprentices, lottery | `data/scripts/`, map scripts | Hoenn | 2–5 | Rebuilt per Aethos location. |
| Move tutors and Frontier rewards | `data/text/move_tutors.inc`, `data/scripts/move_tutors.inc` | Hoenn | 3 | Needs Aethos tutors and, in Phase 5, Olympiad prizes. |
| Hoenn contest and Frontier data tables | `src/data/contest_*.h`, `src/data/battle_frontier/`, `data/contest_ai_scripts.s` | Cut | 5 | Counted in §10. The Frontier engine is kept; its tables are replaced by Olympiad data. |

## 10. Hoenn-only systems to cut

The first block is ART_PLAN's cut list, plus FRLG data, the PokéNav, Mirage Island, the minigames and the link and e-Reader pieces named in the brief. Each is sized as its code, text, graphics, music, SFX, maps and tilesets, from the map. The totals count only things that are in the ROM now.

| System | Where | ROM (KiB) | Status | Phase | Notes |
|---|---|---|---|---|---|
| Contests | `src/contest*.c`, `contest_ai.c`, `picture_frame`, `graphics/contest/`, `graphics/picture_frame/`, `data/contest_ai_scripts.s`, `include/config/contest.h`, `ContestHall*` maps, `gTileset_Contest`, 8 contest songs | 201.3 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_CONTESTS` in `include/config/ichor.h`). About 21 KiB stays: the summary screen still reads the contest move data and the category icons; guarding that waits for the menus restyle. |
| Berry Blender | `src/berry_blender.c`, `graphics/berry_blender/`, `data/text/blend_master.inc`, `SE_BERRY_BLENDER` | 38.5 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_CONTESTS`). |
| Pokéblocks | `src/pokeblock*.c`, `use_pokeblock.c`, `graphics/pokeblock/` | 31.3 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_CONTESTS`). The Safari Zone's feeder now places nothing. |
| Secret bases and decorations | `src/secret_base.c`, `decoration*.c`, `graphics/decorations/`, `data/tilesets/*/secret_base*`, `SecretBase_*` maps, `data/text/secret_base_trainers.inc` | 123.4 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_SECRET_BASES`). The bedroom PC's DECORATION option closes the PC. About 11 KiB stays, because the Frontier exchange corner names decorations. |
| Mirage Island and Mirage Tower | `src/mirage_tower.c`, `MirageTower_*` maps, `gTileset_MirageTower`, `Route111_NoMirageTower`, `Route130_MirageIsland` layouts, `graphics/misc/mirage_tower*` | 43.6 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_MIRAGE_TOWER`). |
| PokéNav and Match Call | `src/pokenav*.c` (14 files), `src/match_call.c`, `graphics/pokenav/` (64), `data/text/match_call.inc`, `SE_POKENAV_*` | 137.3 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_POKENAV`). |
| e-Reader and Mystery Gift | `src/mystery_gift*.c`, `mevent*.c`, `ereader*.c`, `data/multiboot_ereader.s`, `graphics/wonder_card/`, `wonder_news/`, `MysteryEventsHouse` | 61.0 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_MYSTERY_GIFT`, `ICHOR_CUT_MULTIBOOT`). The main menu's Mystery Gift entries go back to the menu. |
| Minigames: slots, roulette, Pokémon Jump, Berry Crush, Dodrio picking, lottery corner, Game Corners, Trick House | `src/slot_machine.c`, `roulette.c`, `pokemon_jump.c`, `berry_crush.c`, `dodrio_berry_picking.c`, `lottery_corner.c`, `minigame_countdown.c`, matching `graphics/` and maps | 235.3 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_MINIGAMES`). |
| Link-only features: Union Room, link trade and battle, Cable Club, record mixing, Colosseum multiboot, rfu library, Berry-fix multiboot | `src/union_room*.c`, `link*.c`, `librfu*.c`, `AgbRfu_LinkManager.c`, `cable_club.c`, `record_mixing.c`, `data/multiboot_pokemon_colosseum.s` (164 KiB), `data/multiboot_berry_glitch_fix.s` (15 KiB), `BattleColosseum_*`, `UnionRoom`, `TradeCenter`, `CableClub` maps and tilesets | 419.9 | Cut | 6 | Union Room, Cable Club, record mixing and the Colosseum and Berry-fix multiboot programs are cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_LINK`, `ICHOR_CUT_MULTIBOOT`). The RFU library and link-battle core stay, because main.c, battles and the overworld call into them. `trade.c` stays for in-game trades. |
| Hoenn Battle Frontier: maps, art, trainers, text | `BattleFrontier_*` maps (Tower, Dome, Palace, Pike, Pyramid, Arena, Factory, lounge), `BattlePyramidSquare*`, three Battle Tents, `TrainerHill_*`, twelve Frontier and Trainer Hill tilesets, `graphics/battle_frontier/`, `frontier_pass/`, `door_anims/battle_*`, `sFrontierTrainerSlides`, `data/text/battle_tent.inc` | 540.6 | Cut | 5 | Maps cut by hoenn-cut batch 3. Kept: the Battle Pyramid floor, top and squares (the Labyrinth's engine builds floors from them), the Pike rooms and the Trainer Hill floors, whose layouts the engine loads. The art the engine no longer reaches drops out of the ROM by itself (the build now uses -ffunction-sections). |
| FRLG data in the ROM | 75 FRLG songs (239 KiB), two FRLG Japanese fonts (64 KiB), 62 FRLG trainer pics (43 KiB), Kanto and Sevii region-map art, `hall_of_fame_frlg.c`, `voicegroup_frlg_*` | 365.4 | Cut | 6 | Per ART_PLAN, but FRLG maps are not in the ROM, so this is the whole ROM saving. The repo cleanup is in §9. |
| **Total, ART_PLAN's list (Frontier engine kept)** | | **2,197.7** | | | **2.15 MiB (2.25 MB)** |
| Hoenn Battle Frontier engine and data tables | `src/battle_tower.c` (`gBattleFrontierMons` 32 KiB, `gBattleFrontierTrainers` 16 KiB), `battle_dome.c`, `battle_pike.c`, `battle_pyramid.c`, `battle_arena.c`, `battle_factory*.c`, `battle_palace.c`, `battle_tent.c`, `trainer_hill.c`, `trainer_tower*.c`, `frontier_util.c`, Frontier songs | 341.2 | Keep | 5 | Keep: the Olympiad needs the facilities' rules. Replace the Hoenn trainer and Pokémon tables. Removing the engine too adds 341 KiB. |
| **Total if the Frontier engine also goes** | | **2,538.9** | | | **2.48 MiB (2.60 MB)** |

Additional Hoenn-only systems. They are **not** on ART_PLAN's list, so they are not in the totals above. I propose cutting them, and the director decides.

| System | Where | ROM (KiB) | Status | Phase | Notes |
|---|---|---|---|---|---|
| Mauville Old Man: bard, storyteller, hipster, Giddy, trader | `src/mauville_old_man.c`, `bard_music.c` (162 KiB of phoneme data), `sound/direct_sound_samples/phonemes/`, `ph_*.mid` | 283.8 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_MAUVILLE_MAN`). Not approved in the brief, but its maps were gone and the bard is an Easy Chat feature. Set the switch to 0 to restore it. |
| TV shows, Battle TV and Pokémon News | `src/tv.c`, `battle_tv.c`, `data/text/tv.inc` (2,193 string lines), `pokemon_news.inc` | 76.6 | Cut | 6 | Cut from the ROM by hoenn-cut batch 3 (`ICHOR_CUT_TV`). |
| Easy Chat and Mail | `src/easy_chat.c`, `data/text/`, `graphics/easy_chat/`, `graphics/mail/`, 12 mail items | 59.1 | Keep | 6 | Kept for now ("where safe"): mail items and the Frontier still use them. 45 KiB. |
| Safari Zone | `src/safari_zone.c`, `battle_controller_safari.c`, `healthbox_safari.png`, Safari maps | 40.9 | Cut | 6 | |
| Cable car and SS Tidal and ferries | `src/cable_car.c`, `ss_anne.c`, `seagallop.c`, graphics | 44.9 | Cut | 6 | Triremes replace ferries. |
| Apprentice, Lilycove Lady, wall-clock set screen, mass outbreaks | `src/apprentice.c`, `lilycove_lady.c`, `wallclock.c`, `mass_outbreak.c` | 68.2 | Cut | 6 | The Lilycove Lady is counted under Contests, not here. The wall clock stays: `wallclock.c` now runs the klepsydra (§5). |
| Hoenn gym puzzle mechanics | `src/rotating_gate.c` | 16.0 | Cut | 6 | Fortree Gym and Trick House 6 only. |
| **Subtotal of the proposals** | | **about 590** | | | **0.58 MiB** |
| Hoenn legendary set pieces | `src/rayquaza_scene.c`, `graphics/rayquaza_scene/` (25), Regi puzzle and Braille, Deoxys rock, weather-trio songs, Cave of Origin and Sealed Chamber songs | 335.6 | Hoenn | 5 | Not a cut. PITCH §6.6 reuses Groudon, Kyogre and Rayquaza as the Primordials (Gaia, Oceanus, Ouranos), so re-theme their scenes. |

**Where the ROM goes** (26,878,048 bytes used; the rest of the 33,554,432-byte limit is 6,676,384 bytes, or 6.37 MiB, free):

| Block | ROM | Share | What it means |
|---|---|---|---|
| Pokémon cries | 9.37 MB | 34.9 % | About 1,160 samples, 8 KiB each. Cuts depend on the dex. |
| Pokémon species data and art | 5.87 MB | 21.8 % | 1,571 entries, about 3.7 KiB each. |
| Hoenn map scripts, layouts and text | 1.07 MB | 4.0 % | Frees as Aethos maps replace Hoenn. The cut systems' maps are in their own rows. |
| Instruments, voicegroups, tables | 0.85 MB | 3.2 % | Shared engine. |
| Battle animations (art and scripts) | 0.80 MB | 3.0 % | Kept. |
| Overworld object graphics | 0.63 MB | 2.4 % | People, objects and field sprites. Mostly Hoenn and FRLG sheets, retired with the maps. |
| Tilesets (Hoenn 428 KiB, Greek 73 KiB) and animations (118 KiB) | 0.63 MB | 2.3 % | |
| Fonts | 0.37 MB | 1.4 % | Plus 64 KiB of FRLG fonts in the FRLG cut. Includes about 75 KiB of Japanese glyph tables (§11). |
| Hoenn music not on a cut list | 0.30 MB | 1.1 % | Replace as Ichor songs arrive. |
| Everything on ART_PLAN's cut list | 2.25 MB | 8.4 % | The first total above. |
| Engine code, other UI, text, the Frontier engine, the proposed cuts and the rest | about 4.7 MB | 17.5 % | |

The cuts matter less than the dex. The Hoenn-only systems on ART_PLAN's list free about 2.2 MB. The cries and species art together are 15 MB, so how many existing species stay decides the ROM budget far more than any system cut does.

## 11. Possibly overlooked

A total conversion tends to miss these. Each is checked in the repo.

| Item | Where | Status | Phase | Notes |
|---|---|---|---|---|
| Game Freak copyright and logo | `graphics/intro/copyright.png`, `graphics/intro/scene_1/`, `graphics/credits/the_end_copyright.png`, `src/strings.c:906` (diploma "GAME FREAK"), `graphics/intro/` | Greek | 1 | The copyright card credits Pokémon's makers and calls Ichor a fan-made game; the Game Freak logo is gone (`INTRO.md`). The diploma is signed PROF. DAPHNE. The credits' "the end" copyright waits with the credits. |
| Credits roll | `src/data/credits.h` (57 pages of Game Freak staff), `src/credits.c`, `graphics/credits/` | Hoenn | 4 | Needs Ichor's own credits plus upstream attribution (pokeemerald, expansion, tools, fonts, music sources). |
| ROM header title and game code | `Makefile` (`TITLE ?= POKEMONICHOR`, `GAME_CODE ?= BPEE`, `MAKER_CODE := 01`), `src/rom_header_gf.c:102` (`"pokemon emerald version"`), `src/rom_header_rhh.c` | Greek | 1 | The cartridge title is POKEMONICHOR (`Makefile`). The game code stays `BPEE`, because emulators pick the save type from it. The GF header's internal name in `src/rom_header_gf.c` still reads "pokemon emerald version"; only link and save tools read it. |
| Default player and rival names | `src/main_menu.c:481,485` ("THEO", "IANTHE") | Greek | 1 | Done. The rival is Kleon by script, and there is no rival-naming step (`sText_RivalsName` is used only by the FRLG Oak speech). Check the in-game-trade nicknames, egg OT strings and the debug menu's Brendan and May follower entries. |
| Save-error and corruption screens | `src/main_menu.c:259-262`, `src/strings.c:568` | Keep | 6 | Plain text. Only the "POKéMON" word and the menu frame show. Worth a proofread. |
| Clock reset screen | `src/reset_rtc_screen.c`, `graphics/reset_rtc_screen/` | Keep | 6 | Generic. "The internal battery has run dry". |
| Battle-message wording | `src/battle_message.c` | Greek | 1 | Swept: no line the game can reach says FOE, ELITE FOUR, CHAMPION, LEADER, Birch or Wally. The Battle Arena referee's three lines go with the Frontier. Trainer-class openers are generic. |
| `{PKMN}` glyph and the "POKé" glyphs | `charmap.txt:55` (`PKMN`), `graphics/fonts/latin_*.png` | Keep | Director | The font draws "PK" and "MN" as small caps in 2 tiles. The party menu no longer prints them (QA P3); Frontier and link text still does. Fine if the game keeps "Pokémon". Record the decision (§7). |
| The font | `graphics/fonts/` (23 files), `src/fonts.c` (422 KiB) | Keep | Director | Gen 3's six Latin variants plus 5 Japanese ones. Greek letters appear on the title as paint, not as glyphs. A Greek-style font is optional. |
| Japanese font tables | `src/fonts.c` (`gFont*Japanese*`), `src/text.c` (`sFontBoldJapaneseGlyphs`), `graphics/fonts/japanese_*.png` | Cut | 6 | About 75 KiB beyond FRLG's 64 KiB (counted in §10). An English-only build can drop them, but it needs careful engine work. Not in any total. |
| Ribbons | `src/pokemon_summary_screen.c` (ribbon count on the skills page), `graphics/pokenav/ribbons/`, `src/data/` ribbon names | Hoenn | 4 | The summary's skills page shows a RIBBON box. Champion, Cool, Beauty, Winning, Effort, Marine and so on. Re-theme as Laurels or cut with contests. |
| Summary "Trainer memo" and "Met at" lines | `src/pokemon_summary_screen.c`, `src/strings.c` | Greek | 1 | "Calm nature, met at Lv5, ELAIA VILLAGE." Hoenn places only show for Hoenn's maps. |
| Move-tutor, PC and trade-scene text | `data/text/move_tutors.inc`, `data/text/pc.inc`, `data/text/ingame_trade_frlg.inc` | Hoenn | 2 | The Pithos strings are Ichor's (§7). Tutor and trade text are not. |
| Pocket names | `src/strings.c:145` ("POKé BALLS" and others) | Keep | — | ITEMS, POKé BALLS, TMs & HMs, BERRIES and KEY ITEMS, on the satchel's parchment label. TERMS.md keeps Poké Ball and TM. |
| Pokémon type names and move names | `src/data/types_info.h`, `src/data/moves_info.h` | Keep | — | Generic. |
| Pokémon Center and Mart words in the follower messages | `src/follower_helper.c:26,132-140` | Greek | 1 | The follower's lines say "Your Pokémon", look up at Mount Olympus, and notice the Agora's shelves (`UI_remnants.md`). |
| Dev tools | `src/debug.c` (28 KiB), `graphics/quickstart/`, `include/config/quickstart.h`, `include/config/debug.h` | Keep | 6 | Disable for the release patch. Quickstart is off in release builds, and its title badge is hidden (`QUICKSTART_HUD`). |
| Hoenn flags and vars in names | `include/constants/flags.h`, `vars.h` | Keep | — | Internal names only. |
| Unused graphics | `graphics/unused/` (11 PNGs: old battle UI, a Bulbasaur and a Charizard) | Keep | 6 | Not built into the ROM. Delete when tidying. |
| Pokémon Center jingle at the heal tray, the Pokémon Center fainting sequence | `graphics/field_effects/`, `MUS_HEAL` | Greek | 1 | `MUS_HEAL` plays `mus_ichor_heal` over the Asclepeion's spring (§1, §8). |
| The brand "Pokémon Ichor" on the title | `graphics/title_screen/` | Greek | 1 | Done. |
