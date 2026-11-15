# Phase 1 trainer-class portraits

Battle portraits (trainer front pics) for the slice's trainer classes. Each is a 64×64, 16-color Gen 3 front pic in a 3/4 view toward the player's side, lit from the top left. The palette is embedded in the PNG.

Sources live in `tools/ichor/art/sprites_classes.py`:
- Rebuild the PNGs and the preview sheet with `python3 tools/ichor/art/sprites_classes.py --write`.
- Preview with `--preview DIR`, which writes the 3× sheet, 6× singles and pixel grids.

## Native Akti checkpoint

All seven portraits now use smaller hand-drawn directional faces, cleaner
cloth/fleece clusters, selective outlines and lighter, attached hands/props.
Their full native 64x64 poses and existing embedded palettes are preserved.
The Shepherd waves beside his crook; the Harvester raises an olive sprig and
supports a smaller woven basket; the Goatherd holds bound reeds to his lips
under a gray beard and goat-hair mantle. The Hoplite retains his raised
Corinthian helmet, crimson crest, linen armor, bronze greaves and lambda shield.
The Augur points upward with his feather/fillet, white beard and two restrained
black-figure birds at the hem. Both acolytes keep soot and saffron; Lampon's
slim tongs clasp a glowing coal, and Pyrrha's raised lamp joins her hand/arm.

`python3 -m unittest discover -s tools/ichor/tests -p 'test_*sprites.py'`
checks all source pixels/palettes and the connected lamp/arm, alongside the
accepted walker/bow protections. `tools/ichor/tests/akti_art.sh` loads the
actual ROM portraits through `CreateTrainerPicSprite` and checks every color
against that ROM's trainer palette table. The EWRAM-only fixture also reviews
Nemecub/Nemeleon fronts, backs and normal/shiny palettes. Both matching
baseline/current runs pass 37 checks with 15 captures. These are genuine
engine-loader views, not a claim of seven completed trainer battle playthroughs.
Native checks, helper compilation, build and smoke pass; creative approval
and whole-town acceptance remain pending.

## Catalog

| Constant | Party-file name | Look | File |
|---|---|---|---|
| `TRAINER_PIC_SHEPHERD` | `Pic: Shepherd` | Felt pilos cap, sheepskin mantle knotted at the chest over a blue tunic, crook; waving | `graphics/trainers/front_pics/shepherd.png` |
| `TRAINER_PIC_HARVESTER` | `Pic: Harvester` | Sun-browned olive-picker: terracotta headscarf, linen apron over an olive-green dress, a wicker basket of black and green olives on her hip, an olive sprig held up | `graphics/trainers/front_pics/harvester.png` |
| `TRAINER_PIC_GOATHERD` | `Pic: Goatherd` | Wild graying curls and beard, a shaggy goat-hair cloak over a coarse undyed tunic, a syrinx at his lips, a bronze goat-bell on his rope belt, leg thongs. One bee buzzes nearby: Komatas is the goatherd the bees fed (Theocritus) | `graphics/trainers/front_pics/goatherd.png` |
| `TRAINER_PIC_HOPLITE` | `Pic: Hoplite` | Lakonian youth: Corinthian helmet pushed up with a crimson crest, a crimson hoplon with a bronze rim and a bronze lambda (Λ, Lakonia's mark), spear held low and ready, linen corselet, crimson chiton and cloak, bronze greaves. Shares Kleon's crimson and bronze | `graphics/trainers/front_pics/hoplite.png` |
| `TRAINER_PIC_AUGUR` | `Pic: Augur` | Bird-watching seer: white hair and beard, head tilted up, pointing at the sky; a gold fillet with a black crow feather, an indigo robe and himation with a black-figure frieze of birds in flight at the hem, a staff in his other hand | `graphics/trainers/front_pics/augur.png` |
| `TRAINER_PIC_ACOLYTE_M` | `Pic: Acolyte M` | Hestia's temple servant (Lampon): white chiton with a saffron himation and hem, bronze hearth tongs held out in both hands clasping a glowing coal, a smear of hearth ash on his cheek and hem, alarmed ("Carefully!") | `graphics/trainers/front_pics/acolyte_m.png` |
| `TRAINER_PIC_ACOLYTE_F` | `Pic: Acolyte F` | Hestia's temple servant (Pyrrha, Aithra): white peplos with a saffron girdle and hem, auburn hair in a bun tied with saffron, a clay oil lamp held high, the other fist on her hip, hearth ash on her nose and hem | `graphics/trainers/front_pics/acolyte_f.png` |

The pics are front-only (no back pic). Trainer parties and class definitions are not changed here: to use a pic, set its `Pic:` line in `src/data/trainers.party`.

Preview: `design/phase1/img/sprites_classes.png`. The top row shows Brendan and the cast for scale (Kleon, Ione, the Titan grunt, Daphne); the classes are below, on the grass battle background, at 3×.
