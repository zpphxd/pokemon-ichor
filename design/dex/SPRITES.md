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

## Evolutions must feel grand

The user's words: "we just want to make sure these look amazing. and evolutions are truly grand and powerful etc".

- **Final stages are the payoff.**
  - Use the full size class the brief gives: a large final fills about 56–64 px of the frame.
  - Strike a commanding pose: rearing, wings spread, roaring, weight thrown forward, or towering.
  - Scale up the signature feature so it dominates the silhouette.
  - Render more than the earlier stages: extra highlight tones, metal or gem glints, and effects such as flame, lightning, spray or aura where the type allows.
  - The back view conveys bulk and power, not just a shoulder.
- **Middle stages show the growth.** Each feature from stage one gets bigger, sharper and more elaborate, so the line reads as one creature maturing toward that final form.
- **Compare finals at 3x** with blaziken, sceptile, swampert, salamence, metagross, garchomp, gyarados and staraptor. Ours should hold the frame the way they do.

## The legendary tier

The user's words: "all legendaries and mythical olympians constilations etc need to be fucking awesome. powerful. mysterical. the best pokemon ever designed".

**Who is in it:**
- The legendaries and mythicals: the Moirai (Nemira, Lotira, Thanira), Kronolith, Kairazor, Pegaunos, the colossi (Olympanax, Pontanax, Nekranax) and Ichorin.
- The Astral constellation Pokémon, when they come.
- The same standard applies to the pseudo-legendary's final stage (Lernathan) and the post-game myth monsters (Hexylla, Trybdis, Melodrakon, Haligeron, Nostail, Stygiad, Seirenade, Bouldyphus).

**How they're made:**
1. **Concepts first.** Each species gets three distinct design concepts: different silhouettes, poses and readings of the myth, not three colorways. The user picks one.
2. **One artist per species.** The chosen concept is rendered as its own job, with as many passes as it takes.

**The bar:**
- **Cohesion.** The user rejected a whole round of concepts: "they all feel disjointed". Those were props bolted onto a body: an hourglass in a chest, gears on the shoulders, a falcon whose body was a sand glass. A legendary is one creature whose motifs grow out of its anatomy, the way Dialga's time-crest, chest gem and plates are its body, or Lugia's fins and dorsal plates are. Use flowing, unified silhouettes, and give paired or trio legendaries a shared design language. The user's touchstone: "lugia meets dialga".
- **Size:** fill the frame, about 60–64 px. The silhouette must be unmistakable at 1x.
- **Presence:** a sense of power and mystery. Use otherworldly effects that belong to the myth: auras, glowing runes or meanders, celestial motifs, threads of fate, ichor-gold light, sea spray, storm, shadow.
- **Palette:** all 15 colors used deliberately, with a signature glow color.
- **Iconography:** Greek in every case (black-figure patterns, bronze, marble, laurel, the god's attributes), made into something new rather than a costume.
- **Back view:** imposing, never just a shoulder.
- **Comparison:** check at 3x against the most iconic legendaries: lugia, ho_oh, rayquaza, dialga, palkia, giratina, arceus, groudon, kyogre, regigigas, zacian, solgaleo, lunala, necrozma and eternatus. Ours must hold their own.

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

## Common misses from the first round

Reviews of the starters kept finding the same gaps. Check for each one before you call a sprite done.

- **Flat shading.** Two or three tones lit edge to edge read as a sticker.
  - Use 4 tones on the main material, plus a highlight where it fits: wet sheen, metal glint or silver leaf.
  - Model the anatomy: shoulder and chest planes, the underside of the neck in shadow, the barrel of the ribs, the haunch.
  - Add a lit rim along the top edges and cast shadows under heads, arms and capes.
- **Back views as one big mass.**
  - Draw them at about 1.2× the front's scale, not larger.
  - Model the back: spine, shoulder blades, muscle.
  - Keep the head in a readable right-facing profile at a sensible size: no giraffe necks.
- **Stamped detail.** Repeated identical leaves, feathers or scales look mechanical. Vary size and angle, overlap them with depth, and make the back layers darker.
- **Human-looking faces.** The user flagged a "messed up" face, and reviews caught the same thing twice more: a nymph with a realistic nose and lips, a lion whose face read as a man's, a laughing weasel with human eyebrows and a human grin. Faces must be Pokémon faces:
  - **Animals:** animal anatomy. A protruding muzzle or beak, a nose pad, eyes set on the sides of the head, an animal mouth.
  - **Humanoids:** stylized like Gardevoir. Big simple eyes with a shine, little or no nose or mouth.
  - **Nobody:** no drawn human eyebrows, lips or rows of teeth.
  - **Check at 1x and 2x,** not just zoomed in: that's where an uncanny face shows.
- **Boxy shapes.** Heads and bodies built from straight-edged polygons look like carved wooden toys, however well they're shaded.
  - Build creatures from curves: a round skull, a muzzle that tapers along a curved top line, round chests, haunches and paws.
  - No straight edge longer than 2–3 px on a face.
  - The parts renderer's blobs, lenses, limbs and drops along bezier paths give organic forms. Nebrel is the example.
- **Shapes that read as something else.** A cape of stacked ovals reads as wings. A symmetric frontal pose reads stiff. Use 3/4 view and asymmetric, weighted poses.
- **Lazy frame 2.** A 1 px lift alone is too little. Move something with character too: a mane or fin flick, ears perking, a mouth opening, flames flickering, leaves swaying. `paint.shift(..., mask=...)` moves a shaped region.
- **Weak follower views.** The `up` view must be a creature seen from behind, not a totem or a cocoon. The `down` view must read as the creature's face and body, not a helmet.
- **Icons that change color.** After the build quantizes to the shared icon palettes, look at the icon. If a green went gray, set `Mon(..., icon_pal=N)`. Simplify the draft's small-size shapes (`if not p.big`) so icons aren't noisy.
- **Lost work.** Scratch scripts in /tmp vanish. The art `.txt` files and the line's `.py` file are the deliverables. If a generator script matters, paste the key data into the `.py` file instead.

## Checks

The build fails on errors (a missing view, a palette over 15 colors, a bad footprint, a stray character in an art file). It also warns when a sprite touches the frame edge or declares a color it never draws. Clear every warning.

### Elaia native redraw pass (2026-11-15)

This pass covers **Nebrel, Kladoe, Daphnyad, Kynder, Dikyon, Pylakyon,
Hipling, Thalamare, Seismare, Eripip and Galekit**. The approved concept sheets
are references only: no concept image is resized, quantized or used as a battle
sprite input. The five line modules draw the native views; all 33 editable
battle grids have localized hand-painted highlight/shadow refinements.

The fire line retains the Ember Dreams progression and Pylakyon's locked
diagonal, differently angled mastiff heads, lunging arched back and
serpent-faced S-tail. The water line has a split caudal fan on Hipling's
supporting coil and a foam-crested blue wave on Seismare. Galekit's battle
back now includes its ears, mask, muzzle and stolen olive. Party icons keep
the ROM's existing shared-palette selectors, and every down/up/side pair has
distinct native pixels. Existing hoof, paw and root footprints remain valid.

Rebuild only this batch, then validate and copy it with the existing ROM
importer's `copy_sprites` operation:

```bash
python3 tools/dex/sprites/build.py Nebrel Kladoe Daphnyad Kynder Dikyon Pylakyon Hipling Thalamare Seismare Eripip Galekit --preview build/elaia-sprite-review --sheet build/elaia-sprite-review.png
python3 tools/dex/sprites/check_elaia.py --import-rom --report build/elaia-sprite-validation.json
```

`check_elaia.py` checks the 64×128 fronts, 64×64 backs, 32×64 icons,
192×32 followers and 16×16 footprints; indexed PNG bit depth, transparent
index 0, BGR555-ready battle/shiny palettes, exact shared icon palettes and
ROM selectors, unique motion pairs, editable-grid dimensions, localized
hand finishing, reproducible rendered pixels and byte-identical ROM imports.
The commands pass with no species errors or warnings. Pillow's API deprecation
notices are separate from the sprite checks.

These are technical checks, **not user art approval or a completed-town
claim**. Smoliv, displayed in the shared opening, has a separate native pass
below rather than a custom dex entry. ROM build and emulator smoke evidence
are the coordinator's separate responsibility.

### Smoliv shared-opening dependency

Smoliv remains Smoliv: a small, anxious olive baby with a rounded seed body,
three green leaves, a waxy green-gold fruit, tiny feet and no arms or horns.
Its shiny darkens the olive to purple-black without recoloring the green body
or leaves. Frame 2 winks and tilts the olive/rosette; the follower alternates
its feet and sways its leaves in each direction.

Editable sources are `tools/dex/sprites/lines/smoliv.py` and
`tools/dex/sprites/art/smoliv_front0.txt`, `_front1.txt`, `_back0.txt`.
The line deliberately does not export `MONS`, so this vanilla opening asset
does not enter the Aethos YAML/dex generator. The standalone driver is:

```bash
python3 tools/dex/sprites/smoliv.py --native-check --preview build/smoliv-review --report build/smoliv-check.json
```

It builds only `design/dex/sprites/smoliv/` and copies its nine files into
`graphics/pokemon/smoliv/`. The two-frame `anim_front.png` maps to the
upstream registration's `front.png` (64×128). The only species-info edit
selects the existing two-frame animation table; species identity, stats,
types, story and YAML are unchanged. Icon palette 1 and the existing
32×32 six-frame follower registration are preserved.

The scoped command passes with no errors or warnings: native editable-grid
coverage, rendered/indexed-file reproducibility, transparent index 0,
shared icon palette/ROM selector identity, battle and follower normal/shiny
palette equality, distinct battle/icon/walk pairs and exact ROM copies.
`--native-check` also uses the real `gbagfx` helper: front 4096 bytes, back
2048, icon 1024, follower 3072, footprint 32, and each palette 32 bytes.
Both converted palettes match the exact little-endian BGR555 words.

### Pylakyon serpent-tail separation refinement

Pylakyon's bronze serpent now has two opposed bends outside the flank,
transparent space inside the lower coil, a black edge and a pale-lit,
ghost-eyed serpent head. The back and both down/up/side follower pairs use
the same tail construction; both shared-palette icon frames match it.
Normal/shiny palette entries, icon selector 3, footprint, three mastiff
heads and the arched lunge are retained. Only the tail-side silhouette and
adjacent material shading were changed in the three battle art grids.

```bash
python3 tools/dex/sprites/build.py Pylakyon --preview build/pylakyon-refinement/review --grid
python3 tools/dex/sprites/check_elaia.py Pylakyon --import-rom --native-check --report build/pylakyon-refinement/validation.json
```

The checker accepts optional species names; without names it still checks
the original eleven. `--native-check` validates real `gbagfx` output sizes
and both exact BGR555 palettes. The Pylakyon-only commands pass with no
errors or warnings, unchanged palettes/footprint and distinct paired
front/icon/follower motion. Visual evidence includes native normal/shiny
views rather than treating palette validity as visual approval.
