# The player's battle pics: Theo and Ianthe

The Unwoven replace Brendan and May in every battle, on the trainer card and in the intro's
boy-or-girl choice. The files keep Brendan's and May's names, so every code path that reads
`TRAINER_PIC_BRENDAN` or `TRAINER_PIC_MAY` works with no engine edits.

The four production PNGs are the canonical native sources, pinned by
`tools/ichor/art/player_sources.json`. They are image-model-led artwork,
resampled/indexed for the GBA, with retained-model-pixel animation assembly;
they are **not hand-authored native grids**. Theo's front preserves the approved
64x64 anchor's index geometry exactly; its disclosed palette adaptation truncates
channels to BGR555. Ianthe and the companion views have coordinator implementation
clearance, not separate user artistic acceptance.

The complete 24-PNG/186-frame player checkpoint, frozen image/crop/export replay,
read-only shared palettes and retained-vehicle contracts are documented in
[SPRITES_player_ow.md](SPRITES_player_ow.md). The historical battle painter remains
available to other named-cast drawing helpers; its `--write` command is rejected.
Old previews and all rejected pilots remain preserved, not silently replaced.

```bash
python3 tools/ichor/art/player_sources.py --check --rom pokeemerald.gba
bash tools/ichor/tests/player_battle.sh
```

## Files

| File | Theo | Ianthe |
|---|---|---|
| Front pic, 64×64 | `graphics/trainers/front_pics/brendan.png` | `graphics/trainers/front_pics/may.png` |
| Back pic, 64×256, 4 frames | `graphics/trainers/back_pics/brendan.png` | `graphics/trainers/back_pics/may.png` |
| Palette, shared by front and back | `graphics/trainers/palettes/brendan.pal` | `graphics/trainers/palettes/may.pal` |

## The look

This is the shared spec, so the overworld sprites match it.

- A sun-gold straw petasos: a low crown, a wide brim and a brown band.
- An Aegean-blue chlamys pinned with a gold fibula at the right shoulder. It drapes across the chest, covers the left arm and flares out behind.
- A cream chiton, belted, with connected cloth shading.
- Brown sandals laced up the shin.
- A terracotta satchel with a brown flap and a gold button, on a strap across the body.
- Theo has short black hair.
- Ianthe has dark-brown hair in a low braid with a gold tie. The braid falls over her shoulder in front and down her back behind.
- Expressive three-quarter faces and asymmetric, readable poses.

## Back frames

From behind, facing right, cropped at the waist. The throwing arm is the near (left) arm. It comes out from under the chlamys.

| Frame | Shows | Played |
|---|---|---|
| 0 | Held grip beside the near-left side of the body | `sAnimCmd_Hoenn`: 0, 1, 2, 0, 3 |
| 1 | Wind-up: ball raised high, in front of the brim | |
| 2 | Near-left cross-body release, open hand toward the opponent | |
| 3 | Rest, empty-handed, arm under the cloak | The battle intro (`sAnim_GeneralFrame3`) |

The corrected windup keeps each character's hold head/torso registered and uses
their own complete held grip/orb. The near-left arm stays the throwing arm in
every frame. All four frames remain 64x64 in a vertical 64x256 atlas.

`sAnimCmd_Point_HGSS` also reads the sources in order 3, 0, 2, 2, 3.
The real-loader fixture covers both fronts and all three native back animations:
idle, Hoenn throw (24/9/24/9/50), and pointing (9/9/24/24/50). It checks exact
source pixels, full OBJ VRAM, all sixteen live palette words and finite ends:
160 checks and 24 captures. These are forced engine fixtures, not a natural
battle playthrough or controller-eligibility claim.

## Palette

Each character has a trainer-local sixteen-color palette, shared by that
character's front/back only. Index 0 is transparent and all channels are BGR555
precise. The local `.pal` files and embedded PNG palettes are checked together,
including the compiled `gTrainerPalette_Brendan`/`May` arrays. These are not the
shared overworld palettes; no folk, peer-game, ball or other named-cast palette
is rewritten. The old ASCII painter's role ordering is historical, not the
current local palette contract.

## Historical game checks

`design/phase1/img/sprites_player_battle_ingame.png` shows:
- the trainer card for both characters
- the debug battle intro (frame 3)
- the "Go!" throw (frame 0, then the release as the player slides off).

**How to reproduce.**
1. Quickstart.
2. Write `playerGender` through `gSaveBlock2Ptr`.
3. Open START, then the player's name.
4. Hold R and press START, then pick Party…, then Start Debug Battle.

## Historical previews

- `design/phase1/img/sprites_player_battle.png`: Kleon, Theo, Ianthe and Ione at 3×, on a battle backdrop.
- `design/phase1/img/sprites_player_battle_back.png`: back frames 0–3. Theo is on top, Ianthe below.
- `design/phase1/img/sprites_player_battle_ingame.png`: in-game screenshots at 2×.

The current intro choice still loads these same front sources. Current smoke
and full real-loader captures accompany the source checkpoint; the image files
listed above retain their original historical content.

## Still open

- Separate user acceptance, parent-owned map-marker/credits surfaces and the
  broader character rollout are not closed by this player-source checkpoint.
