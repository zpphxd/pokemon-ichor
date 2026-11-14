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

## Replaced assets

| Asset | Now shows | Why |
|---|---|---|
| `graphics/birch_speech/birch.png` | Professor Daphne | The new-game intro portrait. Same file, so no code changes. |

Preview: `design/phase1/img/sprites_trainers.png` (Brendan for scale, then Kleon, Ione, grunt, Daphne).
