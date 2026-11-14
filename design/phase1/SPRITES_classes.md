# Phase 1 trainer-class portraits

Battle portraits (trainer front pics) for the slice's trainer classes. Each is a 64×64, 16-color Gen 3 front pic in a 3/4 view toward the player's side, lit from the top left. The palette is embedded in the PNG.

Sources live in `tools/ichor/art/sprites_classes.py`:
- Rebuild the PNGs and the preview sheet with `python3 tools/ichor/art/sprites_classes.py --write`.
- Preview with `--preview DIR`, which writes the 3× sheet, 6× singles and pixel grids.

## Catalog

| Constant | Party-file name | Look | File |
|---|---|---|---|
| `TRAINER_PIC_SHEPHERD` | `Pic: Shepherd` | Felt pilos cap, sheepskin mantle knotted at the chest over a blue tunic, crook; waving | `graphics/trainers/front_pics/shepherd.png` |

The pics are front-only (no back pic). Trainer parties and class definitions are not changed here: to use a pic, set its `Pic:` line in `src/data/trainers.party`.

Preview: `design/phase1/img/sprites_classes.png`. The top row shows Brendan and the cast for scale (Kleon, Ione, the Titan grunt, Daphne); the classes are below, on the grass battle background, at 3×.
