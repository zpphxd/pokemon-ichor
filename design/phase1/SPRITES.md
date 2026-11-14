# Phase 1 cast sprites

Sources live in `tools/ichor/art/sprites_*.py`. Rebuild the PNGs with
`python3 tools/ichor/art/sprites_trainers.py --write`, and preview with `--preview DIR`.

## Trainer pics (tier 1)

| Constant | Party-file name | What it is | File |
|---|---|---|---|
| `TRAINER_PIC_KLEON` | `Pic: Kleon` | Rival from Lakonia: crimson cloak, bronze armband | `graphics/trainers/front_pics/kleon.png` |
| `TRAINER_PIC_HIEROPHANT_IONE` | `Pic: Hierophant Ione` | Hestia's Hierophant: veil, bronze oil lamp | `graphics/trainers/front_pics/hierophant_ione.png` |
| `TRAINER_PIC_TITAN_GRUNT` | `Pic: Titan Grunt` | Titanborn grunt: Corinthian helmet, sickle emblem | `graphics/trainers/front_pics/titan_grunt.png` |
| `TRAINER_PIC_PROFESSOR_DAPHNE` | `Pic: Professor Daphne` | Professor Daphne: laurel wreath, himation, scroll | `graphics/trainers/front_pics/professor_daphne.png` |

The new pics are front-only (no back pic). Hoenn trainer pics are untouched.

## Alethea's back pic (catch tutorial)

| Constant | What it is | File |
|---|---|---|
| `TRAINER_PIC_ALETHEA` | Alethea from behind, throwing: blue headband, ponytail, sun-gold chiton, a satchel of scrolls on her left hip | `graphics/trainers/back_pics/alethea.png` (64×256, 4 frames) |

- **Source:** `tools/ichor/art/sprites_alethea_back.py` (`--write`, `--preview DIR`, `--grids DIR`).
- **Style:** it borrows the arm path, hands and ball from `sprites_player.py`, so the throw matches Theo's and Ianthe's frame for frame. The frames are the same as theirs: 0 holding the ball, 1 wind-up, 2 release, 3 rest. They play through `sBackAnims_Hoenn`.
- **Palette:** her own, embedded in the PNG.
- **No front pic yet.** The entry points its front pic at `gTrainerFrontPic_None`, so don't use it in a party file. When her front pic is drawn:
  - Add it to this same entry.
  - Give it the back pic's palette.
- **The catch tutorial uses it:** `battle_controller_wally.c` and `reshow_battle_screen.c` draw `TRAINER_PIC_ALETHEA` where they drew `TRAINER_PIC_WALLY`. Wally's own pics are unchanged.
- **Previews:**
  - `img/sprites_alethea_back.png` shows her four frames, with Ianthe's below.
  - `img/sprites_alethea_back_ingame.png` shows the tutorial in game, started through the debug menu's Wally Tutorial script: the intro, the "Go!" throw and the recall.

## Replaced assets

| Asset | Now shows | Why |
|---|---|---|
| `graphics/birch_speech/birch.png` | Professor Daphne | The new-game intro portrait. Same file, so no code changes. |

Preview: `design/phase1/img/sprites_trainers.png` (Brendan for scale, then Kleon, Ione, grunt, Daphne).

## Tier 1 polish, pass 1

- Titan grunt: lower Corinthian helmet with a swept-back crest, a T-shaped face opening with red eyes, a low crouch, a bronze shoulder guard, a sickle in the near hand and the far fist cocked.
- Daphne: index finger raised as if mid-lecture, with the end of the scroll unrolled.
- Kleon: a wider cloak flare and extra cloak folds.
- Still open: full 3/4 turns with weight shift for all four, more cloth folds, and Kleon's swagger pose. Ione is unchanged.
