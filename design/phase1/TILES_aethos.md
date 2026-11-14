# aethos: the outdoor primary tileset

`gTileset_Aethos` is Aethos's outdoor world. It replaces vanilla `gTileset_General` and keeps every one of General's 512 metatile ids, behaviors and layer types. Any layout built on General therefore means the same thing on aethos: the same tree is a tree, the same ledge jumps the same way.

The art is redrawn from scratch: olives, cypresses and stone pines; sun-bleached grass and wild barley; limestone paths and dry-stone terraces; the Aegean; and marble buildings.

## Images (`design/phase1/img/`)

| File | What |
|---|---|
| `aethos_route101.png` | `LAYOUT_ROUTE101`, `--primary aethos`, 2× |
| `aethos_littleroot.png` | `LAYOUT_LITTLEROOT_TOWN`, `--primary aethos --secondary petalburg`, 2×. A raw render with no remap: Petalburg's references into the primary are pinned (see Porytiles below). The houses are Petalburg's own art. |
| `aethos_village.png` | A mock village block built only from aethos metatiles, 2×. Throwaway block data, not a map. |
| `aethos_coast.png` | Part of `LAYOUT_ROUTE109`, 2×. Slateport's own references into the primary are remapped for the preview (`aethos_review.py --remap`). The umbrellas and chairs are Slateport's. |
| `aethos_sheet.png` | The numbered metatile sheet, 2×. |
| `aethos_anims.png` | Every animation, key frame first. |

Regenerate the tileset with `/usr/bin/python3 tools/ichor/art/paint_aethos.py`, then the images with `tools/ichor/art/aethos_images.py`.

## Metatile ids for map builders

Collision lives in the map data, as before. Behaviors are General's: tall grass is `MB_TALL_GRASS`, ledges keep their jump direction, and doors are `MB_ANIMATED_DOOR`.

### Ground

| Id | Element |
|---|---|
| `001` | Grass |
| `002` | Grass under a ledge or cliff lip (a thin shadow line on top) |
| `01C` | Grass in deep shade |
| `00D` | **Tall grass** (wild encounters): barley tufts with gold seed heads |
| `015` | Long grass: reeds |
| `004` | Red anemones (animated) |
| `000` | Void (the night-sea backdrop) |

**Limestone path patch.** `1D0` `1D1` `1D2` / `1D8` `1D9` `1DA` / `1E0` `1E1` `1E2`, laid out as TL T TR / L C R / BL B BR. `1D9` is the open path.

**Tilled earth.** `103` `104` `105` / `10B` `10C` `10D` / `113` `114` `115`, in the same layout.
- `10C`, `14C`, `12E` and `12F` are `MB_BERRY_TREE_SOIL`.
- `14B` `14C` `14D` is a plot's top edge: corner, edge, corner.

**Volcanic ash.** `100` `101` `102` / `108` `109` `10A` / `110` `111` `112`.

### Trees

The **olive** is 2×2, and its crown pokes 3 px into the row above on the top layer, so the player walks behind it.

| Part | Ids |
|---|---|
| Top half | `1D4` `1D5` (`1D6` `1D7` are identical) |
| Bottom half, nothing below | `1E4` `1E5` (`1E6` `1E7` identical) |
| Bottom half, with the crown tip of an olive below it | `1DC` `1DD` (`1DE` `1DF`, `1F2` `1F3` identical) |
| Crown tip in the row above, over grass | `1CE` `1CF` |
| … over tall grass | `1C6` `1C7` |
| … over ledge grass | `1E8` `1E9` |
| … over ash | `1EA` `1EB` |
| … over rock | `1EE` `1EF`, `1F0` `1F1` |
| … over the sea | `1F6` `1F7` |
| … over a pond | `1FE` `1FF` |
| Olive top half on the top layer, over ledge grass | `1FC` `1FD` |

**Stacking.** For a column of olives, use top, then bottom-with-tip, then top, and end with a plain bottom (`1E4` `1E5`).
- Above the first olive, put a tip metatile (`1CE` `1CF`), or the crown is cut flat.
- Below a bottom-with-tip, the next olive must start.

The **cypress spire** is 1×2. Its top half is on the top layer.

| Part | Ids |
|---|---|
| Top half, over grass | `00E`, `00F`, `0C6`, `0C7` (identical) |
| … over ledge grass, tall grass, pond, sea, rock or a white kerb | `01D`, `025`, `02D`, `035` / `193`, `0CE`, `040` |
| Bottom half | `016`, `017` (identical) |
| Cypress top over an olive bottom | `1EC` `1ED` |
| Cypress bottom under an olive tip | `1F4` `1F5` |

The **stone pine** (General's secret-base tree) is 2×2.
- Top: `01E` `01F` (`02E` `02F` identical).
- Bottom: `026` `027`.
- `036` `037` are the same with a dark hollow between the roots, the secret-base "open" spot.

### Edges and props

**Ledges** are dry-stone terrace lips. The ground under them comes from the family.

| Ledge | S | W | E | SW | SE | S, left end | S, right end | Inner corner |
|---|---|---|---|---|---|---|---|---|
| on grass | `087` | `085` | `086` | `08D` | `08E` | `0D5` | `0D6` | `06E` |
| on rock floor | `08F` | `095` | `096` | `09D` | `09E` | `0DD` | `0DE` | |
| on sand | `097` | `0A5` | `0A6` | `0AD` | `0AE` | `0E5` | `0E6` | |

More W/E lips: `0FE`/`0FF` and `106`/`107` (grass), `10E`/`10F` and `116`/`117` (rock), `11E`/`11F` and `126`/`127` (sand).

A step-shaped ledge, as in Route 101: `0D5 087 … 08E` on the lower row, and `06E 087 … 0D6` on the row above it.

**Dry-stone walls** (General's metal fence).

| Wall | Ids |
|---|---|
| West–east, middle layer | `148` left end, `149` run, `14A` right end; `134` run |
| West–east, top layer (walk behind it) | `138` left end, `13A` right end |
| North–south, middle layer | `132` (west side of the tile), `133` (east side) |
| North–south, top layer | `139`, `140` (west side); `141`, `142` (east side) |

Set walls impassable in the collision data.

**Signs and markers.**
- `003`: a marble stele with a pediment and a gold finial. Use it for town and route signs (bg events, as before).
- `01B`: a roadside herm, a stone pillar with a bearded head (General's trainer-tips board).
- `130` (top layer) over `131`: a bronze tripod on a marble plinth (General's gym sign).

**Rocks and other props.**
- Boulders: `0E0` on grass, `0E1` on rock, `0E2` on sand.
- Sea boulders with a foam ring: `0C5`, `0CD`, `18C` and `194` (middle layer), and `0BD` (top layer).
- Marble steps: `0AF`, `0CF`.
- Pebble mosaic threshold: `024` (`MB_SOUTH_ARROW_WARP`, the exit mat).
- Anemone troughs: `005`, `006`, `007`.
- General has no cut-tree metatile: cuttable trees are object events, outside this tileset.

### Coast and water

| Ids | Element |
|---|---|
| `170` | Open sea, calm water (animated) |
| `14E`, `14F` | Rough and deep water (currents, dive spots) |
| `147`, `156` | Interior deep water |
| `11B` `11C` `11D` / `123` `124` `125` / `12B` `12C` `12D` | A sand island or beach in the sea, laid out TL T TR / L C R / BL B BR. Its edges animate the surf. `124` is plain sand. |
| `150`–`16F`, `172`–`17F` | Sea stacks and reefs: pale gray stone in the sea, at General's ids |
| `0B3`, `0BB`, `0BC`; `04C`, `0B9`, `0C1`, `054` | Waterfall: falling water, the lip, and the plunge pool |
| `0B0`–`0DA` | Ponds, at General's ids |

Shallows (turquoise over sand), rocky shores and pond edges keep General's ids.

### Buildings

All doors are `MB_ANIMATED_DOOR` at General's ids, so existing warps work.

**Asclepeion** (Pokémon Center, 4×4). Door `061`, plaque with the rod of Asclepius `062`.

```
048 049 04A 04B
050 051 052 053
058 059 05A 05B
060 061 062 063
```

**Agora** (Mart, 4×4). Door `041`, pinax sign `042`. The middle of the roof repeats `029`, and `02A` is unused, as in General.

```
028 029 029 02B
030 031 032 033
038 039 03A 03B
060 041 042 043
```

**Shared corner.** Both buildings share the corner `060`, as General's did: an anta, the shaded wall, and the first column.

**Farmhouse** (General's route house, 3×4). Door `021`. `00B`, `00C`, `013` and `014` are plain whitewashed wall pieces.

```
008 009 00A
010 011 012
018 019 01A
020 021 022
```

**Palaestra** (General's gym, 6×5). Door `1CD`, porch pediment `1C5`. `1AB` and `1B3` repeat, as in General.

```
1AA 1AB 1AB 1AB 1AB 1AC
1B2 1B3 1B3 1B3 1B3 1B4
1B8 1B9 1BA 1B3 1BB 1BC
1C0 1C1 1C2 1C5 1C3 1C4
1C8 1C9 1CA 1CD 1CB 1CC
```

**Theater door** `1DB` (General's contest-hall door), under a gold mask.

### Not redrawn, only retextured

These kept General's shapes and were rebuilt from General's materials in aethos's palettes and textures:
- the mountain cliff set (`068`–`0FF` and the rock walls) in warm limestone with strata
- the bike rails and bridges (`0EC`–`0FD`)
- the muddy slope (`0E8`–`0EB`)
- the bumpy slope (`1F8`, `1F9`)
- the secret-base cave spots (`1A0`–`1B1`)
- the cave mouths (`09F`, `0A7`)
- the white kerbs (`03D`–`067`)
- the gym roof's leftover corner (`1D3`)

They no longer read as Hoenn, but the cliffs in particular deserve a hand-drawn pass before Kronion Hill's terraces are built.

## Porytiles rules for this tileset

Hoenn secondaries point into the primary by **tile index** and **palette slot**. The slice maps still pair with Petalburg, so aethos is built to keep Petalburg working.

**Locked palettes.** `porytiles/tilesets/gTileset_Aethos/config.yaml` locks palettes and patches tiles. The six palettes are written by `aethos_bin.py` and Porytiles never changes them.

| Palette | Family | Holds |
|---|---|---|
| 0 | marble | buildings |
| 1 | plaza | marble and clay on grass |
| 2 | grove | olives, cypresses, pines, trunks, grass |
| 3 | earth | limestone, ledges, cliffs, paths, soil |
| 4 | meadow | tall grass, anemones |
| 5 | sea | the Aegean, surf, sand |

- Petalburg's own tiles use palette 2's slots 2–4 and 14–15 and palette 5's slots 11–13. Those slots hold the aethos versions of General's greens and sand.
- Every palette keeps General's slot *roles* where it can, so other Hoenn art that borrows them shows a recolor, not noise.
- Palette 0's color 0 is the backdrop, a night-sea navy.

**Pinned tiles.** The 62 tile indices Petalburg uses are seeded into `tiles.png` before compiling, each holding the aethos art for what General had there. Patch mode keeps them and fills the free slots with the rest.

**Animations.** They sit at General's offsets (water 432, surf 464, rocky surf 480, waterfall 496, anemones 508). Every animated reference in aethos matches General's slot.

**Verification.** The build checks that the pins survived. It then runs a compile with checksum verification on and fails if that changes anything. kalliste and temple_hestia compile against it cleanly.
- No layout uses them yet, so pair them by hand: `porytiles compile-tileset gTileset_Kalliste --primary-pairing-mode manual --primary-pairing-partners gTileset_Aethos`.

**Budget.** 18 free tile slots remain in the primary. New Greek pieces belong in secondaries, which have their own 512.

**Don't hand-edit `porytiles_src` or `porytiles_bin`.** Change the painters in `tools/ichor/art/aethos_*.py` and rerun `paint_aethos.py`.
- `aethos_palcheck.py` explains palette trouble.
- `aethos_review.py --remap` previews aethos under any other Hoenn secondary, which still points at General's tile numbers.

## What map builders and other streams must know

- **Use aethos with a Greek secondary** (kalliste, temple_hestia).
  - Petalburg works as a stopgap: no stray tiles. But its own houses, door mats and the Pokémon Center roof corners `282` and `283` are still Hoenn art.
  - Any other Hoenn secondary renders wrong on aethos, because only Petalburg is pinned.
- **Door animations are still Hoenn.**
  - `graphics/door_anims/general.png`, `poke_center.png` and `poke_mart.png` play over `021`, `061` and `041`. They are drawn in General's palette slots, now aethos colors, so the opening frames show a recolored Hoenn door.
  - They need redrawing to match the Asclepeion, Agora and farmhouse doors.
- **Field effects are outside the tileset** and still Hoenn: the tall-grass rustle, the ripples, sand footprints.
- **Not yet seen in-game.** No map uses aethos yet, so it was checked in renders. The ROM builds, and every animated metatile points at its animation slot.
