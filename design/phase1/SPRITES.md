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

The four cast entries above are front-only. The player front/back pics are in
`SPRITES_player.md`; Alethea's matched front/back pair is described below.

## Elaia native-art checkpoint (2026-11-15)

Theo, Ianthe and Kleon now have hand-painted smaller faces and asymmetric,
weighted stances, with flared cloth, bent knees and articulated sandals.
Daphne's portrait has a narrower face, layered himation folds and her existing
teaching/scroll gesture. Her painter now actually writes both
`professor_daphne.png` and `birch_speech/birch.png`, so the introduction cannot
retain a different portrait after regeneration. Alethea's front keeps the
blue headband, gold chiton, scroll satchel and trowel; the tutorial back and the
three Elaia cast walkers retain those same identities.

These are native indexed drawings, not resized concept-sheet extracts.
The two player palettes and cast/folk palettes keep their opaque index roles.
The player overworld transparent entry is now expressed at exact BGR555
precision; its value in the ROM is unchanged.

**Current verification:** native PNGs match their painters and preserve
dimensions, shared palettes and distinct motion frames. The restored native
toolchain builds the ROM; `smoke_test.sh` and all three `elaia_opening.sh`
runs pass. New captures include Daphne's introduction, the player choice,
Kleon's portrait/player throw and the Elaia walkers. Both genders also pass
the existing walk/run capture script. The images below remain historical;
director approval and coverage of later supported states are separate gates.

## Alethea's back pic (catch tutorial)

| Constant | What it is | File |
|---|---|---|
| `TRAINER_PIC_ALETHEA` | Alethea from behind, throwing: blue headband, ponytail, sun-gold chiton, a satchel of scrolls on her left hip | `graphics/trainers/back_pics/alethea.png` (64×256, 4 frames) |

- **Source:** `tools/ichor/art/sprites_alethea_back.py` (`--write`, `--preview DIR`, `--grids DIR`).
- **Style:** it borrows the arm path, hands and ball from `sprites_player.py`, so the throw matches Theo's and Ianthe's frame for frame. The frames are the same as theirs: 0 holding the ball, 1 wind-up, 2 release, 3 rest. They play through `sBackAnims_Hoenn`.
- **Palette:** her own, embedded in the PNG.
- **Front pic:** `graphics/trainers/front_pics/alethea.png`, drawn by
  `sprites_phase2_classes.py alethea --write`. It already uses the back pic's
  palette, `gTrainerBackPicPalette_Alethea`, in the same trainer entry.
- **The catch tutorial uses it:** `battle_controller_wally.c` and `reshow_battle_screen.c` draw `TRAINER_PIC_ALETHEA` where they drew `TRAINER_PIC_WALLY`. Wally's own pics are unchanged.
- **Previews:**
  - `img/sprites_alethea_back.png` shows her four frames, with Ianthe's below.
  - `img/sprites_alethea_back_ingame.png` shows the tutorial in game, started through the debug menu's Wally Tutorial script: the intro, the "Go!" throw and the recall.

## Replaced assets

| Asset | Now shows | Why |
|---|---|---|
| `graphics/birch_speech/birch.png` | Professor Daphne | The new-game intro portrait. Same file, so no code changes. |

Preview: `design/phase1/img/sprites_trainers.png` (Brendan for scale, then Kleon, Ione, grunt, Daphne).

## Historical tier 1 polish, pass 1

- Titan grunt: lower Corinthian helmet with a swept-back crest, a T-shaped face opening with red eyes, a low crouch, a bronze shoulder guard, a sickle in the near hand and the far fist cocked.
- Daphne: index finger raised as if mid-lecture, with the end of the scroll unrolled.
- Kleon: a wider cloak flare and extra cloak folds.
- Kleon's swagger and Daphne's folds have a newer native pass above. Ione and
  the Titan grunt now have the native Akti checkpoint below.

## Akti native-art checkpoint (2026-11-15)

Ione's smaller three-quarter face, offset veil and diagonal robe folds keep
the cream/terracotta costume and lit bronze lamp. The Titan Grunt keeps the
Corinthian helmet, crimson crest, slate tunic, sickle emblem and bronze
greaves, with a weighted crouch and a narrower turned helmet. Both have
matched nine-frame walkers in `sprites_npc.py`; no portrait, cast or folk
palette changes were needed.

`SPRITE_REVIEW=1 tools/ichor/tests/route1.sh` and
`SPRITE_REVIEW=1 tools/ichor/tests/temple_trial.sh` additionally capture the
real portrait/send-out sequence without changing its timing or input.
The Kronion tablet's native markings and the Akti boat's shallow hull are drawn
in `sprites_objects.py` and `akti_objects.py`. The boat's two halves share one
32x16 source and keep the cast palette; its renderer no longer samples tiles.

For matching prop shots and coverage of all nine local maps:

```sh
mkdir -p build/akti_sprites
build/tools/ichor-mgba-headless --script tools/ichor/tests/akti_sprites.lua \
  --frames 7000 --until "AKTI_SPRITES done" pokeemerald.gba
```

`SPRITE_OUT` selects an existing screenshot directory. This review test checks
each loaded map and records a fixed camera; it does not assert artistic quality
or replace the Route 1 and temple gameplay tests.

This is a validated implementation checkpoint, not director approval or
completion of every Route 1/Akti sprite. Exact coverage and retained assets
are recorded in `design/art/INVENTORY.md`.
