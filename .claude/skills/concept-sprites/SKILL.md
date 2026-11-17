---
name: concept-sprites
description: Turn approved Pokémon concept art into real in-game Ichor sprites (front with animation frame, back, shiny, follower and party icon), check them, put them in the ROM and land them. Use when the user hands over a folder of concept PNGs from the concept prompt page (files like 004_kynder_front.png / 004_kynder_back.png), or asks to turn concepts into sprites, ingest concept art, or redo a species' sprites from its concept.
---

# Concept art → in-game sprites

The method behind this is `design/STYLE.md` §3. Read §3.1 (budgets and sizes) and §3.4 (the hand-fix pass) before starting. The tools:
- `tools/ichor/art/mon_from_concept.py` builds the species.
- `tools/ichor/art/concept_to_native.py` is the converter it uses.
- `tools/dex/rom/gen.py` puts the files in the ROM.

The prompts that produce the concepts are in `design/dex/CONCEPT_PROMPTS.md` and on the prompt page.

**Arguments:** the folder of concept PNGs, and optionally the species to limit the run to.

## Setup

```bash
export DEVKITPRO=/opt/devkitpro DEVKITARM=/opt/devkitpro/devkitARM PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"
PY=/usr/bin/python3            # has Pillow and numpy
REVIEW=build/concept_review    # review images; not committed
git fetch origin && git merge --ff-only origin/main   # start from the latest main
```

## 1. Ingest the folder

Dry-run first, then file:

```bash
$PY tools/ichor/art/mon_from_concept.py ingest "<folder>" --dry-run
$PY tools/ichor/art/mon_from_concept.py ingest "<folder>"
```

- Ingest checks every file before copying anything:
  - the species exists, and the number matches it
  - the background is flat
  - the subject fits the 64×64 frame at the concept's own scale
- It files fronts as `tools/ichor/art/concepts/mon/<name>.png` and backs as `<name>_back.png`. Its last line lists the species ingested; use that list below.
- **Report every `SKIPPED` line to the user.** Each means a regenerate: wrong number, busy background, or a subject too big for the frame. Never shrink a concept to make it fit; that's what loses detail.
- A file flagged "not on a 64-grid" is still usable, but expect more hand-fixing.
- Work **one evolution line at a time**, so a line's stages land together.

## 2. Build previews

```bash
$PY tools/ichor/art/mon_from_concept.py <names...> --preview $REVIEW --grid $REVIEW --sheet $REVIEW/sheet.png
```

- **Preview mode writes nothing into the game.** It produces:
  - one card per species: front, frame 2, shiny, back, icon
  - a numbered 10× grid of frame 1, with the palette printed
  - `sheet.png`, the old sprites beside the new set
- Settings come from `tools/ichor/art/concepts/mon/species.json`. A species with no entry gets stage defaults. True-grid concepts from the prompt page (512×512) are read at their exact pitch and are lossless when they already use 15 colors or fewer.

## 3. Review and hand-fix (required)

Look at every card and `sheet.png` yourself, at 1× and zoomed. A sprite passes only if:
- **Face:**
  - Each visible eye is at least 2×2 dark pixels with a 1 px shine at its upper-left.
  - The mouth or expression matches the species' `expression` in `design/dex/species/*.yaml`.
- **Silhouette:**
  - The signature feature (flames, leaves, fins, horns) reads at 1×.
  - Limbs have gaps between them.
  - No blobs.
- **Cleanliness:** no single-pixel noise in flat areas, no outline breaks, no halo.
- **Size:** it fills its stage's size (STYLE.md §3.1), and evolutions grow from stage to stage.
- **Shiny:** matches the species' `shiny:` line in its dex file.
- **Back:**
  - With a back concept: it shows the same colors and features from behind.
  - Without one: it's the interim mirrored front, and you **tell the user that back is interim**.

**Fixing:** add entries to the species in `species.json`, then rebuild the previews and look again.
- `"fixes": [[x, y, [r, g, b]], ...]` sets pixels, using the grid's coordinates. A color snaps to the nearest palette entry; `null` clears the pixel.
- `"pivot"` sets the row that frame 2 bends at, as a fraction of the height. Use 0.4–0.55.
- `"fit"` sets the size, but only for concepts that aren't on the grid.
- Add a `"note"` saying why each fix exists.
- Repeat until every card passes. **If a concept can't pass without redrawing large areas, stop and ask the user for a new concept** rather than painting one in.

## 4. Write into the game

```bash
$PY tools/ichor/art/mon_from_concept.py <names...> --sheet $REVIEW/sheet.png
$PY tools/dex/rom/gen.py
```

`gen.py` copies the sprites into `graphics/pokemon/` and re-measures battle coordinates and shadows. Check that `git diff --stat -- src` shows changes **only** for these species' entries in `src/data/pokemon/species_info/aethos_families.h`.

## 5. Verify

```bash
$PY tools/ichor/sprite_audit.py check --pokemon <Names...>    # capitalized species names
$PY tools/dex/sprites/check_elaia.py                          # if any are Elaia species (starters, Eripip, Galekit)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 $PY -m pytest -q tools/ichor/tests/test_sprite_audit.py tools/ichor/tests/test_akti_species_sprites.py
make -j$(sysctl -n hw.ncpu) && tools/ichor/smoke_test.sh
```

- Every command must pass.
- If a species appears in a scripted test (`grep -ril <name> tools/ichor/tests/*.lua`), run that suite and look at its battle screenshots.
- Check `make`'s ROM usage line too; Pokémon sprites cost little, but report it.

## 6. Land it

- Commit **per evolution line**:
  - the concepts and `species.json`
  - `design/dex/sprites/<name>/` and `graphics/pokemon/<name>/`
  - `aethos_families.h`

  Use the format from `CLAUDE.md`, e.g. `feat(art): build the <line> line from its approved concepts`, and give the reason in the body.
- `git fetch origin && git rebase origin/main`, rebuild with `make` and `smoke_test.sh` if anything came in, then `git push origin main`.
- Package a playtest ROM for the user:

  ```bash
  cp pokeemerald.gba playtest/ichor_latest.gba && (cd playtest && rm -f ichor_latest.zip && zip -q ichor_latest.zip ichor_latest.gba)
  ```

## 7. Report

Send the user `$REVIEW/sheet.png` and a battle screenshot. Tell them:
- which lines landed
- which files were skipped and why
- which backs are still interim
- any concept you asked to have regenerated

## Rules

- **Concepts are the artistic source of truth.** Never paint a species from scratch here, and never fall back to the old ASCII painter (`tools/dex/sprites/build.py`). It now skips any species with a concept, and `check_elaia.py` checks those against this builder instead.
- **Never shrink a concept to fit.** Ask for a regenerate.
- **Don't edit shared icon palettes** (`graphics/pokemon/icon_palettes/`) or another species' files.
- **Never commit** ROMs, saves, or the `build/` review images.
