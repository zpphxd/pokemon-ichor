# The player's battle pics: Theo and Ianthe

The Unwoven replace Brendan and May in every battle, on the trainer card and in the intro's
boy-or-girl choice. The files keep Brendan's and May's names, so every code path that reads
`TRAINER_PIC_BRENDAN` or `TRAINER_PIC_MAY` works with no engine edits.

Source: `tools/ichor/art/sprites_player.py`.

```bash
/usr/bin/python3 tools/ichor/art/sprites_player.py --write --preview design/phase1/img
/usr/bin/python3 tools/ichor/art/sprites_player.py --grids /tmp/grids   # pixel grids for edits
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
- A cream chiton, belted, with folds. It is knee length on Theo and three pixels longer on Ianthe.
- Brown sandals laced up the shin.
- A terracotta satchel with a brown flap and a gold button, on a strap across the body.
- Theo has short black hair.
- Ianthe has dark-brown hair in a low braid with a gold tie. The braid falls over her shoulder in front and down her back behind.
- **Front poses.**
  - Theo holds the ball out toward the opponent.
  - Ianthe raises it beside her shoulder.
  - Both face left in a 3/4 view, like the cast.

## Back frames

From behind, facing right, cropped at the waist. The throwing arm is the near (left) arm. It comes out from under the chlamys.

| Frame | Shows | Played |
|---|---|---|
| 0 | Holding the ball at shoulder height | `sAnimCmd_Hoenn`: 0, 1, 2, 0, 3 |
| 1 | Wind-up: ball raised high, in front of the brim | |
| 2 | Release: arm swung across, open hand toward the opponent. The leaning body shifts 2 px right. | |
| 3 | Rest, empty-handed, arm under the cloak | The battle intro (`sAnim_GeneralFrame3`) |

`sAnimCmd_Point_HGSS` (3, 0, 2, 2, 3) also reads correctly: hold, then the open hand.

## Palette

The index layout is the same for both characters. Only `hair_l` differs.

| # | Name | Theo | Ianthe | Use |
|---|---|---|---|---|
| 0 | transparent | 112 192 160 | same | |
| 1 | ink | 32 24 24 | same | Outlines; Theo's hair |
| 2–4 | skin_l, skin_m, skin_d | 248 208 168 · 224 160 112 · 168 104 72 | same | |
| 5 | brown | 96 56 40 | same | Leather: sandals, belt, strap, hat band; Ianthe's hair |
| 6 | hair_l | 72 72 104 | 152 96 64 | Hair sheen |
| 7–9 | blue_d, blue_m, blue_l | 24 56 120 · 48 104 176 · 112 168 224 | same | Chlamys (master Aegean blue) |
| 10–12 | gold_d, gold_m, gold_l | 152 96 32 · 208 152 48 · 240 200 88 | same | Petasos, fibula, braid tie |
| 13–14 | cream_d, cream_l | 200 176 136 · 248 240 216 | same | Chiton; the ball's white half |
| 15 | terra | 192 80 48 | same | Satchel; the ball's red half |

## Checked in game

`design/phase1/img/sprites_player_battle_ingame.png` shows:
- the trainer card for both characters
- the debug battle intro (frame 3)
- the "Go!" throw (frame 0, then the release as the player slides off).

**How to reproduce.**
1. Quickstart.
2. Write `playerGender` through `gSaveBlock2Ptr`.
3. Open START, then the player's name.
4. Hold R and press START, then pick Party…, then Start Debug Battle.

## Previews

- `design/phase1/img/sprites_player_battle.png`: Kleon, Theo, Ianthe and Ione at 3×, on a battle backdrop.
- `design/phase1/img/sprites_player_battle_back.png`: back frames 0–3. Theo is on top, Ianthe below.
- `design/phase1/img/sprites_player_battle_ingame.png`: in-game screenshots at 2×.

The intro's boy-or-girl choice uses the same front pics. Theo was checked there, including the fade-in; Ianthe's side of the choice was not captured.

## Still open

- The overworld sprites are drawn separately from this same spec. Compare the two once both land.
