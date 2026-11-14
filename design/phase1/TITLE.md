# Title screen: the Fates amphora

The bible's title screen is "a painted amphora". The screen is the belly of a black-figure **panel amphora**.

- The neck and foot are black gloss.
- A reserved clay panel is framed above and below by a meander, the pottery UI's Greek key drawn at twice the size.
- In the panel the three Fates handle a white thread. **Clotho** spins it from her distaff and drop spindle. **Lachesis** lays it along a marked rod. **Atropos**, veiled, closes her spring shears on it.
- Each Fate has a painted name label, as on the François Vase: ΚΛΩΘΩ, ΛΑΧΕΣΙΣ, ΑΤΡΟΠΟΣ.
- One **golden thread** drifts free past all three, never spun and never cut. That thread is the player.
- **ICHOR** is a gilded V-cut inscription in Greek lapidary capitals. POKÉMON, PRESS · START and "A FAN WORK · 2026" match it.

Screenshots: `img/title_1_glint.png` through `img/title_5_drift.png`. They are in-game captures; the dev-only Quickstart HUD is hidden in them.

## Layers

Emerald's layers and effects are reused, so the file names are still Emerald's.

| Layer | Files in `graphics/title_screen/` | Holds | Palette | Effect |
|---|---|---|---|---|
| BG0 | `rayquaza.png`, `rayquaza.bin` | The painted panel: gloss, bands, Fates, labels, white thread (179 tiles) | BG 13, inside `pokemon_logo.pal` | Static |
| BG1 | `clouds.png`, `clouds.bin` | The golden thread, a 2 px cord that wraps every 256 px | BG 14, `rayquaza_and_clouds.pal` | Drifts right at 1 px per 8 frames; the scanline wave ripples it; color 15 pulses; alpha 12/8 makes it glow |
| BG2 | `pokemon_logo.png`, `pokemon_logo.bin` (unchanged identity map) | ICHOR, 8bpp affine | BG 0 (index 0 is the backdrop) | Shine sweeps; slides up 32 px |
| OBJ | `emerald_version.png` | POKÉMON, as the two version-banner sprites | OBJ 0 | Slides down and fades in |
| OBJ | `press_start.png` | Row 0: PRESS · START (blinks). Row 1: the fan-work line | Own | As in Emerald |
| OBJ window | `logo_shine.png` (unchanged) | Shine shape | n/a | Lightens BG2 under it |

`pokemon_logo.pal` holds all 224 colors the build loads for BG2. The logo uses only row 0, so row 13 carries the painting's palette.

## Sequence

1. **Fade in from white.** ICHOR is alone on black gloss and glints as the shine crosses it.
2. **Double shine.** The backdrop warms from the gloss to terracotta clay (184,88,48), with a white-gold peak where Emerald flashed green. It is a glimpse of the pot.
3. **POKÉMON** slides down and fades in while ICHOR rises 32 px to meet it.
4. **The amphora appears**, with PRESS · START blinking on the black foot. The thread drifts, ripples and glints.

## Changes to `src/title_screen.c`

Every change is marked `// Ichor:`.

- Banner, PRESS START and fan-line positions are constants. The banner is centered and rests at y 16.
- The shine flash colors: a clay ramp, a white-gold peak, and the backdrop restored to the gloss ink instead of `RGB_BLACK`.
- BG1 blending is `BLDALPHA(12, 8)` (was 6/15) so the thread glows.
- Phase 3 drifts BG1 sideways (`gBattle_BG1_X`) instead of scrolling it up.
- `UpdateLegendaryMarkingColor` pulses the thread's glint between ichor gold and white gold.

## Regenerating

```bash
python3 tools/ichor/art/title_screen.py --preview   # writes graphics/title_screen/*, previews in build/title_preview/
make -j$(sysctl -n hw.ncpu)
python3 tools/ichor/art/title_screen.py --capture   # in-game shots into design/phase1/img/
```

- The figures are character grids in `tools/ichor/art/title_fates.py`.
- The letters are in `title_lettering.py`. ICHOR's V-cut is shaded by hand there.
- Budgets:
  - BG0 must stay at 512 tiles or fewer, or it overwrites BG1's tiles.
  - BG1 must stay at 128 tiles or fewer, or it reaches the tilemaps at screen base 26.
  - The generator asserts both.

## Not done

- The boot copyright screen and the intro (Game Freak logo, Latios and Latias) are still Emerald's. They belong to the intro task.
