# Aethos dex sprites

How the dex's Pokémon are drawn, and the bar they must clear. The user's words are the bar: "make sure they are as detailed and designed well as any normal pokemon. spend time". The exemplar is **Nebrel** (`tools/dex/sprites/lines/laurel.py` and `tools/dex/sprites/art/nebrel_*.txt`). Read both before drawing anything.

## What each species gets

The build writes each species in the expansion's own layout under `design/dex/sprites/<name>/`, so a folder can later be copied into `graphics/pokemon/<name>/` as it is.

| File | Size | What it is |
|---|---|---|
| `anim_front.png` | 64×128 | Two 64×64 battle frames, facing left |
| `back.png` | 64×64 | Battle back |
| `normal.pal`, `shiny.pal` | 16 colors | JASC. Color 0 is transparent. The shiny is a palette swap only. |
| `icon.png` | 32×64 | Two party-icon frames in one of the six shared icon palettes. `index.json` records which. |
| `footprint.png` | 16×16 | 1 bit |
| `overworld.png` | 192×32 | Follower frames: down ×2, up ×2, side ×2 |
| `overworld_normal.pal`, `overworld_shiny.pal` | | The same as the battle palettes |

## How a sprite is made

Every species is drawn twice over:

1. **A code draft** of every view, in `tools/dex/sprites/lines/<line>.py`. Shapes go through a parts renderer that adds the outline, interior lines, volume shading lit from the upper left, and cast shadow. The icon and the follower frames come from this draft, because at 32 px a clean drawn shape beats hand pixels.
2. **Hand-finished battle sprites**, in `tools/dex/sprites/art/<name>_front0.txt`, `_front1.txt` and `_back0.txt`. The draft is dumped as a grid of palette indices and then finished pixel by pixel, the way a Gen 3 artist cleans up a sketch. When an art file exists, the build uses it instead of the draft.

Commands:

```bash
python3 tools/dex/sprites/build.py Nebrel --preview /tmp/spr --grid --no-write   # review card and pixel grids
python3 tools/dex/sprites/build.py Nebrel --dump front 0 --start-art             # start a hand-finished file from the draft
python3 tools/dex/sprites/build.py Nebrel --dump back 0                          # print the current art with coordinates
python3 tools/dex/sprites/build.py                                               # build every species and write the files
```

Edit art files with `tools/dex/sprites/paint.py`: `paint` writes runs of pixels at exact coordinates, `clear` empties a box, `retone` reshades one color ramp across a region, and `shift` copies frame 1 into frame 2 with a part moved. Its docstring has examples.

## The bar

Put the review card next to official sprites of a similar creature (`graphics/pokemon/<species>/anim_front.png`, for example deerling, eevee, treecko, growlithe or ponyta) and keep working until ours holds up beside them.

- **Silhouette first.** It should read at a glance: clear head, limbs and signature feature, with negative space between the legs. First stages use young proportions: a big head and big eyes.
- **Faces are hand-painted.**
  - Eyes are large and dark with a white shine. Some also get an iris color or a colored glint, for example Nebrel's sun-gold.
  - Every face gets a nose or beak and a mouth line.
  - Never leave an eye touching the outline.
- **Outline.**
  - A 1 px black-figure ink outline (`ink`, 32,24,24) runs around the silhouette.
  - Lines inside the silhouette use the darkest shade of the local color.
  - No doubled outline pixels or stair-step clumps.
- **Shading.**
  - Light comes from the upper left.
  - Each material gets 3–4 tones in clean clusters: highlight on the upper-left planes, midtone, shadow on the lower right and underside.
  - No stray single pixels, no stripes, no pillow shading.
- **Detail.**
  - Add the texture the brief calls for: fur tufts, spot patterns, leaf midribs, feather rows, scales, cracks, flame tongues, metal glints.
  - Every species is Greek-myth inspired, so its myth detail must be visible in the sprite, as the art brief says.
- **Palette.**
  - At most 15 colors plus transparent, each channel a multiple of 8.
  - Start from the master families in `mon_lib.C` (Aegean blue, marble, olive, cypress, terracotta, sun-gold, limestone, ink) and the extended ones for the types they don't cover.
  - Draw every color you declare.
  - The shiny follows the entry's `shiny` line and changes colors only.

## Each view

- **Front** (`front`, phases 0 and 1).
  - 3/4 view facing left, sized as the art brief says.
  - Feet on rows 58–61, roughly centered. Floating species hover with their lowest point around rows 50–56.
  - Frame 2 (phase 1) is a small pose change, for example the head lifted 1 px, ears perked, the mouth open or a wing raised. Make it with `shift` from frame 1, then touch it up.
- **Back** (`back`).
  - An over-the-shoulder close view, about 1.2× the front's scale.
  - The head is turned right into profile so the face still shows.
  - The body is cropped by the bottom of the frame, with no outline along that edge.
- **Down** (`down`). The follower walking toward the camera: symmetric, both eyes showing, with phases 0 and 1 as walk steps. Draw it at the front's scale; the build shrinks it.
- **Up** (`up`). The follower walking away: the whole body from behind. It isn't the battle back.
- **Side** (`side`, optional). Defaults to the front draft. Draw it when the walk needs its own leg swap.
- **Icon** (`icon`, optional). Defaults to the front draft.
- **Footprint.** A preset in `mon_lib.FOOTPRINTS` (hoof, paw, bigpaw, claw, bird, webbed, hand, fin, root, coil, blank) or 16 custom rows. Species with no feet use `blank`, as Gen 3 does.

## Checks

The build fails on errors (a missing view, a palette over 15 colors, a bad footprint, a stray character in an art file). It also warns when a sprite touches the frame edge or declares a color it never draws. Clear every warning.
