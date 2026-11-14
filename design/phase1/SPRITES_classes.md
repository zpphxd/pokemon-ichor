# Phase 1 trainer-class portraits

Battle portraits (trainer front pics) for the slice's trainer classes. Each is a 64×64, 16-color Gen 3 front pic in a 3/4 view toward the player's side, lit from the top left. The palette is embedded in the PNG.

Sources live in `tools/ichor/art/sprites_classes.py`:
- Rebuild the PNGs and the preview sheet with `python3 tools/ichor/art/sprites_classes.py --write`.
- Preview with `--preview DIR`, which writes the 3× sheet, 6× singles and pixel grids.

## Catalog

| Constant | Party-file name | Look | File |
|---|---|---|---|
| `TRAINER_PIC_SHEPHERD` | `Pic: Shepherd` | Felt pilos cap, sheepskin mantle knotted at the chest over a blue tunic, crook; waving | `graphics/trainers/front_pics/shepherd.png` |
| `TRAINER_PIC_HARVESTER` | `Pic: Harvester` | Sun-browned olive-picker: terracotta headscarf, linen apron over an olive-green dress, a wicker basket of black and green olives on her hip, an olive sprig held up | `graphics/trainers/front_pics/harvester.png` |
| `TRAINER_PIC_GOATHERD` | `Pic: Goatherd` | Wild graying curls and beard, a shaggy goat-hair cloak over a coarse undyed tunic, a syrinx at his lips, a bronze goat-bell on his rope belt, leg thongs. One bee buzzes nearby: Komatas is the goatherd the bees fed (Theocritus) | `graphics/trainers/front_pics/goatherd.png` |
| `TRAINER_PIC_HOPLITE` | `Pic: Hoplite` | Lakonian youth: Corinthian helmet pushed up with a crimson crest, a crimson hoplon with a bronze rim and a bronze lambda (Λ, Lakonia's mark), spear held low and ready, linen corselet, crimson chiton and cloak, bronze greaves. Shares Kleon's crimson and bronze | `graphics/trainers/front_pics/hoplite.png` |
| `TRAINER_PIC_AUGUR` | `Pic: Augur` | Bird-watching seer: white hair and beard, head tilted up, pointing at the sky; a gold fillet with a black crow feather, an indigo robe and himation with a black-figure frieze of birds in flight at the hem, a staff in his other hand | `graphics/trainers/front_pics/augur.png` |

The pics are front-only (no back pic). Trainer parties and class definitions are not changed here: to use a pic, set its `Pic:` line in `src/data/trainers.party`.

Preview: `design/phase1/img/sprites_classes.png`. The top row shows Brendan and the cast for scale (Kleon, Ione, the Titan grunt, Daphne); the classes are below, on the grass battle background, at 3×.
