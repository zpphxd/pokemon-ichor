# Ichor style guide: sprites and maps

This guide sets the visual standard for every Pokémon, character, tile and map in Ichor, and the process that gets us there. Read it before any art or map work.

- `design/ART_PLAN.md` covers what gets drawn.
- `design/MAP_DESIGN.md` covers how maps play.
- This file covers **how everything looks** and **how it is made**.

The bar is the target sheets in `design/art/img/style/target_*.webp`: the starter lines and the first five trainer portraits, which the user approved on 2026-11-16. Every sprite should look as if it belongs on those sheets. Every map should look as polished as those sprites.

![The method on Kynder](art/img/style/kynder_pipeline.png)

*Left: Kynder in the game before this guide. Middle: the old method, a plain resize and color reduction. Right: the method below. All three are real 64×64, 15-color sprites.*

---

## 1. Why the old sprites fall short

These are the problems we found by measuring the current sprites against the targets.

1. **Concepts drawn too big for the frame.** The target concepts are pixel art at about 4 screen pixels per game pixel. At that scale the basic forms come out around 62×65 game pixels. The evolutions come out 87–104 px across, against a 64×64 frame. Every resize to fit throws away 20–60% of the pixels, and eyes, spots and fin edges go first. *Detail is lost at the resize, not in the drawing.*
2. **Nearest-neighbor resizing of an illustration.** Image-model "pixel art" is not on a true grid: its pixels vary in size and have soft edges. Nearest-neighbor sampling lands on those edges, which produces broken outlines, noise and a halo in the background color.
3. **Keying the background by color distance.** The concepts sit on a cream backdrop. Removing it by "pixels close to the backdrop color" also removes cream muzzles, bellies and eye whites, punching holes in the face.
4. **Plain k-means palettes.** Fifteen colors chosen by clustering get spent on near-duplicate mid-tones. The two-pixel eye shine and the dark pupil get merged away, and the face goes dead.
5. **Sprites that don't fill the frame.** The old Kynder used about 40% of its 64×64 frame. Gen 3 fronts fill most of theirs.

The fix is the pipeline in §3. Its tool is `tools/ichor/art/concept_to_native.py`.

![Concept beside native sprite](art/img/style/concept_vs_native.png)

---

## 2. The shared look

These rules apply to everything: Pokémon, people, tiles, UI.

**Light and form**
- Light comes from the **top left**. Highlights go up and left; shadows go down and right. Cast shadows fall down and right by about one tile in maps, and sit at the feet in sprites.
- Shade with **clusters**, not single pixels. Every shading shape is at least 2 px wide. Don't pillow-shade, where an outline follows the edge all the way round. Shade to the form.
- **Hue-shift the ramps.** Shadows shift toward violet or blue and lose saturation. Highlights shift toward yellow. A ramp that is just a darker and lighter copy of one hue looks muddy.

**Outlines**
- Use a **selective outline**: the darkest ink (near `(32,24,24)`) on the shadow side, the dark of each material's own ramp on the lit side, and none inside lit areas. Interior lines are a step lighter than the silhouette line.
- **Objects get outlines, terrain doesn't.** Trees, rocks, signs and buildings take a 1 px outline on their silhouette. Grass, paths, sand and water read through value and texture alone.
- **Never anti-alias against transparency.** Any color between the sprite and a backdrop it can't know about becomes a halo on some other background.

**Color**
- Every RGB channel is a **multiple of 8**, so colors convert to GBA BGR555 exactly.
- Color 0 is transparent. Use flat magenta `(248,0,248)` so it can never be confused with a real color.
- Build from the master palette families in `design/phase1/PLAN.md` (Aegean blue, marble, olive, cypress, terracotta, sun-gold, limestone, black-figure ink). New families should be hue-shifted ramps of 3–5 steps.

**Dither**
- Dither only for textures such as stone, bark and fur grain, never for gradients. Ordered dither, two colors, no more than 1 px in 4.

---

## 3. Sprites

### 3.1 Formats and budgets

Every sprite type has a fixed size and color budget.

| Surface | File(s) | Size | Colors | Notes |
|---|---|---|---|---|
| Pokémon front | `graphics/pokemon/<sp>/anim_front.png` | 64×128: two 64×64 frames | 15 + transparent | Frame 2 is the idle/attack pose. It must keep the palette and stay on the same base line |
| Pokémon back | `back.png` | 64×64 | Same palette as the front | Seen from behind, low and to the left; can crop at the bottom edge |
| Shiny | `shiny.pal` | — | Same index order as `normal.pal` | Swap whole ramps, never single indices |
| Party icon | `icon.png` | 32×64: two 32×32 frames | One of the **shared icon palettes** (`iconPalIndex`) | Design within that shared palette. No private colors |
| Follower / overworld | `overworld.png` + `overworld_*.pal` | Keep the existing frame strip (e.g. 192×32) | 15 | Four directions, readable at walker scale |
| Footprint | `footprint.png` | 16×16 | 1-bit | |
| Trainer front | `graphics/trainers/front_pics/<name>.png` | 64×64 | 15 | Three-quarter view, feet near the bottom |
| Trainer back | `graphics/trainers/back_pics/<name>.png` | 64×256: four frames | 15 | Keep each frame's anchor and throw contact |
| Walker (NPC/player) | `graphics/object_events/pics/people/ichor/<name>.png` | 16×32 frames (e.g. 144×32 for nine) | Shared walker palette | Keep the frame count, order and feet position |

**How big the subject is in the frame** is the size ladder, and it is what makes a basic read as young and a final as grown. Emerald's benchmark: basics about 41 px at their largest dimension, middles about 52, finals about 61; small birds smaller still (Taillow 43×30, Natu 25). `mon_from_concept.py` (`ladder_size`) sets every species' size from its place in its line, its dex `height_m` (which picks the spot inside the band, 0.2 m low to 2.0 m high) and its build:

| Place in line | Largest dimension | Examples |
|---|---|---|
| Basic of three | 34–46 px | Nebrel 40, Kynder 39, Hipling 40 |
| Basic of two | 36–50 px | Eripip, Glyphlet |
| Middle of three | 46–56 px | Kladoe 54, Dikyon 53, Thalamare 55 |
| Final | 54–63 px | Daphnyad, Pylakyon, Seismare |
| Single stage | 44–62 px | by height |
| Legendary (base stat total 600+) | 63 px | Olympian-tier species |
| Flying basic or middle | 4 px less than the above | Epopoi 30, Aetling 39 |
| Back | front + 35% of the gap to 63 | Mudkip 41 front, 53 back |
| Trainer portrait | 56–62 px tall | All fronts |

Each evolution should grow about 1.7× in area, as Emerald's do. A concept larger than its target is reduced once, straight from its own grid to the target; a smaller one is never enlarged. Party icons are reduced from the full-frame conversion, so a small battle sprite keeps a detailed icon. Override a species with `"size"` in `species.json` only with a reason in its `"note"`.

Keep 1–2 px of clear space at the frame edges. Front sprites stand on a shared base line, 1–2 px above the bottom edge.

### 3.2 The concept: draw for the grid

A concept is the start of a sprite, not the sprite. It must be made **at native scale** so nothing needs shrinking.

- **Size.** Ask for the subject to fit a **64×64 grid at exactly 8 screen pixels per game pixel**, a 512×512 image. Basics should take up only part of that grid, following the size table in §3.1. If a concept comes out bigger than the frame at its own scale, **regenerate it**; don't shrink it. The converter refuses an oversized subject when you pass `--pitch`.
- **Background.** Ask for a flat, untextured background color that appears nowhere in the subject. Magenta or pure green both work. Never use cream, white or gray.
- **Palette.** Ask for at most 15 colors, with a dark outline and top-left light.
- **Pose.** Front sprites face **left** or three-quarter left, toward the player's side of the screen. Back sprites face away, toward the upper right. Trainers stand three-quarter on with one hand in action: holding a ball, a prop or a gesture.
- **Identity first.** Each species' description in `design/dex/species/` and its earlier concepts in `design/dex/concepts/` decide its silhouette, colors and signature feature. The concept must keep them.

**The whole dex is pre-written.** `design/dex/CONCEPT_PROMPTS.md` has a front and a back prompt for every species, generated by `tools/dex/concept_prompts.py` from `design/dex/species/`. It applies the stage sizes above; rerun the script after a species changes.

**Prompt template.** For a new species, fill in the bracketed parts:

> Gen 3 Pokémon battle sprite, true pixel art on a 64×64 grid, each pixel exactly 8×8 screen pixels (512×512 image), max 15 colors, 1-pixel dark selective outline, light from top left, hue-shifted shading, cluster shading with no noise, no anti-aliasing, flat #F800F8 background. Facing left, three-quarter view. [Species: one-line identity from design/dex/species/<sp>.md, main colors, signature feature]. Subject about [N] pixels tall for a [basic / middle / final] stage.

### 3.3 The converter

```bash
python3 tools/ichor/art/concept_to_native.py concept.png draft.png --pitch 8      # true-grid concept
python3 tools/ichor/art/concept_to_native.py concept.png draft.png --fit 58       # legacy concept, smallest possible resize
```

The converter does five things:
1. It removes the background by **flood fill from the border**, so interior colors that match the backdrop stay in.
2. It samples the **median of each cell's center** at the concept's own pitch.
3. It quantizes to **15 GBA-exact colors**, reserving slots for the lightest and darkest few pixels so eye shines and pupils survive.
4. It strips blur halos and removes orphan pixels and specks.
5. It closes a **selective outline**: ink on the shadow side, the local ramp's dark on the lit side.

Use `--pitch` whenever the concept was made to the template in §3.2. Use `--fit` only for older concepts, and expect to hand-fix more.

**A whole species, in the game.** `tools/ichor/art/mon_from_concept.py` builds every file a species needs from `tools/ichor/art/concepts/mon/<name>.png`:
- the two-frame front, with the species' hand-fix list and a breathing bob for frame 2
- the palettes, with the shiny carried over from the old designed scheme
- the follower, moved onto the new palette
- the icon, in its shared icon palette
- the back, from `<name>_back.png` when one exists. Until it does, an interim back is made from the mirrored front, set low and cropped, with the face painted out.

Then `python3 tools/dex/rom/gen.py` copies the files into `graphics/pokemon/` and re-measures the battle coordinates. **The `concept-sprites` skill** (`.claude/skills/concept-sprites/SKILL.md`) runs the whole path for a folder of returned concepts: ingest and checks, previews, the hand-fix pass (fixes live in `tools/ichor/art/concepts/mon/species.json`), writing into the game, verification and landing. True-grid concepts that already use 15 colors or fewer convert losslessly. A concept PNG in that folder protects the species from the old painter (`tools/dex/sprites/build.py`); `tools/dex/sprites/check_elaia.py` then checks it against this builder instead.

### 3.4 The hand-fix pass (required)

The converter gets the silhouette, proportions and palette right. **People** make a sprite feel alive. Every draft gets this pass at 1× and 4× before review. As a coding agent, record it as a short, explicit list of pixel edits in the species' build script, so it can be replayed.

**Eyes**
- At least 2×2 dark pixels with a 1 px shine on the upper-left.
- Both eyes are visible on a three-quarter face.
- A single-pixel eye is never acceptable.

**Mouth and expression**
- A 1–2 px mouth line or an open-mouth shape.
- The expression matches the species' personality in its dex entry.

**Silhouette**
- Limbs have gaps between them, so no blob reads as one mass.
- The signature feature (flames, leaves, fins, horns) breaks the outline and is readable at 1×.

**Palette and color**
- Merge near-duplicate colors.
- Turn the freed slots into a clean 3–4 step ramp per material: fur, flame, leaf, metal.
- Check that the shiny palette swaps whole ramps.

**Cleanup**
- Remove noise inside flat areas: every cluster at least 2 px.
- Fix outline breaks. The silhouette is closed, with no doubled lines at the corners.

**Frame 2 and companion views**
- Draw frame 2 from frame 1 by moving parts (breath, flame flicker, raised head), not by redrawing.
- The back, icon and follower use the same ramps and the same signature feature.

### 3.5 Review gate

A sprite is ready to land only when all of these hold:

1. **Contact sheet.** For every species in the batch, the current sprite and the new one sit side by side at 1× and 3× on the grass battle backdrop. `design/art/img/style/starters_current_vs_draft.png` shows the layout.
2. **In-game screenshot.** The front and back appear in a real battle, and the icon in the party menu.
3. **Checks pass.** `python3 tools/ichor/sprite_audit.py check --pokemon <names>` passes, along with the build and `tools/ichor/smoke_test.sh`.
4. **Director's look-pass.** Checklist:
   - Does it match the target sheets?
   - Does the face read at 1×?
   - Is the signature feature clear?
   - Does it fill its size class?
   - Is the evolution line consistent?
5. **Labelled honestly.** Record whether the sprite is a redraw, a polish or retained, as `ART_PLAN.md`'s concept fidelity gate requires. A passing audit is not artistic approval.

Batches go **by evolution line**, never by single sprites: all stages, then backs, icons, followers and shinies, landed together.

### 3.6 Walking characters: Gen 3 construction, Greek costume

The people who walk around the world must stand beside Emerald's townsfolk as equals: the same proportions, the same clean construction, with a Greek twist in the costume. On 2026-11-16 we measured Emerald's walkers against ours, at native size:
- **Height and width.** Emerald's adults stand about 20 px tall and use the full 16 px width. Ours stood about 25 px tall and 13 wide: realistic figures, too thin and too tall.
- **Heads.** Emerald's heads are about half the body. Ours were small.
- **Outlines and shading.** Ours had broken outlines, speckled shading, and often single-pixel eyes or none.
- **The exception.** Theo and Ianthe, the approved player sprites, already have the right build. They are the reference for everyone.

**The build:**

| Part | Gen 3 measure (16x32 frame) |
|---|---|
| Body | Adults 19–22 px tall, children 15–18, elders 18–20 (a slight stoop). **Feet on the bottom row.** |
| Head | About half the height: 10–12 px tall, 12–14 px wide. A bold hair or hat shape is the character's identity. |
| Face (front view) | Two eyes, each 1x2 dark px, 2–3 px apart, set low in the face; skin in two tones. Side view: one eye, plus the nose's step in the outline. Back view: hair or headwear only. |
| Torso and legs | 8–10 px together, short and sturdy: arms 2 px wide, feet 2–3 px each. |
| Outline | One continuous 1 px ink outline around the silhouette, with no breaks or doubled corners. Interior lines are a step lighter than the ink. |
| Shading | Two tones per material (three for hair at most), lit from the top left, as flat shapes. **No texture noise.** |
| Silhouette | Every class can be told apart by its silhouette alone: hat, helmet, veil, beard or prop. |

**The sheet.** 9 frames of 16x32 in the engine's order:
- frames 1–3: standing, facing down, up and left
- frames 4–5: walking down
- frames 6–7: walking up
- frames 8–9: walking left

The right-facing frames are the left ones mirrored, so nothing may be one-sided by accident.
- **Walk frames:** alternate the legs and swing the arms, with the head held level.
- **Special sheets** (kneeling, holding up a tablet, seasick) keep their own frame counts.

**Palette.** Walkers share family palettes, such as `ichor_cast.pal` for the named cast (the slot table is in `design/phase1/SPRITES_npc.md`) and `ichor_folk.pal` for townsfolk and classes. Design inside the family's 15 colors. A new family palette costs one of the OBJ palette slots, so it needs the director's approval.

**The Greek costume vocabulary.** Use real clothes, chosen for who the person is:

| Who | What they wear |
|---|---|
| Men, workers | A belted **chiton** to the knee, or an **exomis** (one shoulder bare) for laborers. Adult men are usually **bearded**. |
| Older or important men | A **himation** (a large mantle) draped over one shoulder, and a staff. |
| Women | A **peplos** (with a folded overfold at the chest) or a long chiton, a himation or **veil** over the head outdoors, and hair in a bun or tied with a fillet. |
| Travelers, messengers, hunters | A short **chlamys** cloak pinned at one shoulder, a wide-brimmed **petasos** hat, and laced sandals. |
| Fishermen, sailors, craftsmen | A conical felt **pilos** cap and an exomis. |
| Soldiers | A Corinthian helmet with a crest, a round **hoplon** shield, greaves and a spear. |
| Priests and priestesses | White or saffron robes, a fillet or wreath, and the god's object: a lamp for Hestia, a torch for Demeter, ivy and a thyrsos for Dionysus. |
| Festival people and victors | Wreaths: olive, laurel or ivy. |

**Props tell the job:** an amphora on the shoulder, a fishing net, a lyre, a distaff and spindle, a scroll, a shepherd's crook, a basket of olives.

**Never:** trousers, buttons, modern shoes, realistic proportions, or tiny heads.

**Concepts and conversion.** Walker concepts come from `design/art/WALKER_PROMPTS.md`, as one 3x3 sheet per character:
- **Rows:** facing down, up and left.
- **Columns:** standing, step A, step B.
- **Frames:** each 16x32 on a true pixel grid, drawn at 8x.

**The walkers are hand-drawn** in `tools/ichor/art/walker_paint.py` and `walker_parts.py`: one shared Gen 3 body (face, tunic or robe, child and seated builds) with layered hair, beards, headwear, clothes, capes and props, a tinted outline added round the silhouette, and thin props drawn last without one. Each character is a short spec of parts and palette roles; `python3 tools/ichor/art/walker_paint.py --write` rebuilds every sheet, and `--preview` shows old beside new with Theo and an Emerald townsperson. For a concept sheet instead, `tools/ichor/art/walker_from_concept.py` checks a sheet, reads each frame on its grid, sets the feet on the bottom row, maps the colors into the family palette, and writes the 144x32 strip in engine order. Review every walker at 1x on a real map beside Theo and an Emerald townsperson, before and after.

---

## 4. Maps

The maps must look as finished as the sprites. `MAP_DESIGN.md` decides where things go for play; this section decides how they look.

### 4.1 What's wrong today

We rendered the current maps with `tools/ichor/render_map.py` and compared them. These are the issues, worst first.

1. **Placeholder maps on main.** The Thyrsa and Arkadia that landed on main are stand-ins: one ring of trees, open grass and rectangular paths. The `world-act2` branch has the real ones: a walled city with an acropolis temple, an agora, market stalls and farm plots; a cypress forest with a temple on a raised plinth and a waterfall pool. **Restore the branch versions** before polishing anything. See `art/img/style/thyrsa_main_vs_branch.png` and `arkadia_main_vs_branch.png`.
2. **Forests in a grid.** Trees sit in rows and columns, one by one. Gen 3 forests are **interlocking canopy masses**: overlapping tree blocks forming a solid wall with a ragged, staggered edge and an occasional lone tree in front.
3. **Flat ground.** Most grass is one metatile repeated. The eye needs a base, a variant and an accent.
4. **Flower confetti.** Red flowers are spread evenly across Akti, Thyrsa and Route 1. Flowers belong in **beds**: by doors, along walls, around shrines and in meadows, in clumps of 3–7.
5. **Rectangular paths.** Paths are straight bars with square corners. Real paths have **desire lines**: they curve, widen at junctions and doors, narrow between obstacles, and wear into the grass at the edges.
6. **No height.** Almost everything is flat. Gen 3 maps use cliffs, ledges, terraces, stairs and raised plinths to make depth and frame each screen.

### 4.2 Composition rules

The play screen is **15×10 metatiles**. Judge every rule at that size.

**One landmark per screen**
- Every 15×10 window holds one thing you'd remember: a temple, a big tree, a statue, a ruin, a waterfall or a distinctive house.
- It sits off-center, with open ground in front of it.

**Masses and space**
- Trees, cliffs and buildings form **large masses** with open clearings between them.
- About 60% of a screen should be one simple ground surface and 40% detail. Never spread detail evenly.

**Edges**
- Every boundary is staggered: tree walls, cliffs and coastlines.
- No straight run longer than 6 metatiles without a step, a notch or a lone object in front.

**Ground variety**
- The base ground metatile makes up 70–85% of an open area.
- Two or three variants (tufts, pebbles, worn patches) make up 10–25%, in clusters.
- Accents (flowers, a stray stone) make up 2–5%, in clumps.
- One flat metatile covering more than 90% of an open area is a fail.

**Paths**
- Paths join doors, gates and route exits along the line a person would walk.
- At least 2 metatiles wide on routes and 3+ on town main streets.
- Use worn-edge transition tiles where path meets grass, never a hard square edge.

**Height**
- Every town and route has at least one level change: a ledge, terrace, stair, cliff or plinth.
- Sacred buildings sit **raised**, with steps leading up to them.

**Story in props**
- Props come in believable groups:
  - amphorae beside a storeroom
  - nets and boats on a beach
  - a well with a bucket
  - a shrine with offerings
  - fences around a field that has a farmer
- No orphaned single props in open grass.

**Contrast**
- The player must always tell walkable from blocked at a glance.
- Walkable ground is lighter and lower in contrast. Blockers are darker, outlined and higher in contrast.

### 4.3 Tile art rules

**Size, palettes and limits**
- Tiles are 8×8 and metatiles 16×16, with two layers.
- A primary tileset has 6 palettes and a secondary has 7. Plan the palette families first (`CLAUDE.md`). Every 8×8 tile uses one palette of 16 colors.
- A secondary tileset may use at most 504 tiles. Keep 496–511 free on maps with wide doors.

**Ground textures**
- Ground tiles **tile seamlessly in all four directions**.
- Spread texture marks evenly but irregularly, so no single tile's pattern repeats in a visible grid when it is laid out 4×4.
- Build grass from 3 values. Shading clusters are no smaller than 2 px; avoid single-pixel salt-and-pepper.

**Shadows and edges**
- Buildings and big trees cast a soft, 1–2-value-darker shadow down and right onto the ground. Use a shadow metatile; don't bake one ground color into the object.
- Edge and transition sets are complete: straight edges, outer corners and inner corners for every pair of ground types that meet. If a corner is missing, get it drawn rather than covering it with a prop (`MAP_DESIGN.md`).
- Trees have **at least two silhouettes per species** (olive, cypress), plus interlocking **canopy wall** pieces: top edge, bottom edge, left/right edge and fill.

**Water**
- Water has a lit edge on the far shore, foam where it meets sand, and a 2–4 frame animation.

### 4.4 Process for a map upgrade

1. **Render the map as it is** with `tools/ichor/render_map.py LAYOUT_<NAME> -o build/render/<name>_before.png`.
2. **Critique every 15×10 screen** against §4.2 and write down the findings.
3. **Fix the tiles first.** Missing corners, canopy-wall pieces, ground variants and transitions get drawn into the tileset (§4.3) before any layout change.
4. **Re-lay the map.** Restructure the masses, then paths and height, then landmarks, then props.
5. **Re-render** and compare before and after. Do at least **three critique passes**.
6. **Check it.** `python3 tools/ichor/map_audit.py` and the map's test pass, and you walk the map in the game. `python3 tools/ichor/map_style_audit.py <Map>` measures this section's rules: flat ground, barren screens, long straight edges, no height, and too few distinct tiles. It orders maps worst first; use it to find where to look, then judge the render.

For a new biome, start with a **beauty shot**: a 240×160 mock-up of one typical screen at native resolution, drawn to these rules and approved before the tileset is cut. It does for a tileset what the concept does for a sprite.

### 4.5 The Greek land: build from the ground up

Every map is designed by two people at once: a ROM-hack mapper who makes places worth exploring, and someone who knows how a Greek landscape and city actually work. A map that is correct for play but could be anywhere has failed. **Design from the landform outward:** the land first, then the water, then where people would put roads, fields, walls and temples because of that land.

**The land.**
- **Limestone everywhere.** Pale gray-white rock, karst, scree slopes, cliffs that drop straight into the sea, caves and sinkholes. Mountains are steep and bare above the trees, and they come right down to the coast. Flat land is precious: small coastal plains, upland basins, river valleys.
- **Water is scarce and therefore sacred.** Streams are seasonal (*cheimarroi*): dry beds of white stones most of the year, flowing after rain. Springs are holy places with a fountain house, a nymph's shrine or a temple. Wherever a map has water, give it a reason and a structure.
- **Vegetation by height:**
  - Coast: sand and shingle, tamarisk, Aleppo pine, reeds at river mouths.
  - Lowland: olive groves on terraces, vineyards, wheat and barley, with a stone threshing floor (*aloni*) beside the fields.
  - Hillside: *maquis* and *phrygana* (kermes oak, mastic, broom, thyme in low mounds), with cypress around shrines and graves.
  - Mountain: fir and black pine, then bare rock and summer-burnt grass.
- **Terraces are the signature of a lived-in hillside.** Dry-stone retaining walls (*pezoules*) step the slope into strips of olives or vines, with steps built into the wall. In Gen 3 terms these are ledges, stairs and wall tiles, and they give every farmed slope its height.
- **Light.** High sun, bleached ground, short dark shadows, a deep blue sea. Keep land colors warm and dry, and the sea saturated.

**The polis.** A Greek town is not a grid of houses around a square. It has parts, and each part has a place in the land:
- **Akropolis:** the defensible high rock, holding the oldest temple, treasuries and the last refuge. Visible from everywhere in town, and reached by one ramp or stair through a gateway (*propylon*).
- **Asty:** the lower town on the slopes below. Houses are **courtyard houses**: blank walls and one door onto the street, life inside around a court. Lanes are narrow, follow the contours, and turn to steps where it's steep.
- **Agora:** the open civic heart on the flattest ground. It's lined by **stoas** (long colonnaded halls, one side open) and holds altars, herms, a fountain house, the council house and market stalls. Keep it open; the stoas frame it.
- **Walls** follow the ridges and contours, not straight lines. They have towers at corners and gates where the roads come in. Gates are a big moment: a towered opening, often angled so attackers expose their unshielded side.
- **Outside the walls:**
  - the **necropolis**, lining the roads out of each gate with grave stelai, tombs and cypress
  - the gymnasium and palaestra, near water and shade
  - the stadium, set in a natural hollow
  - the theater, cut into a hillside, facing a view
  - farmsteads with a stone tower, and shepherd huts on the hills
- **Sanctuaries** sit in a walled precinct (*temenos*), entered through a propylon. The **temple faces east**, and its **altar stands outside in front of it**, because the rites happen at the altar, not inside. Around them are votive offerings, treasuries and a sacred grove or spring.
- **Harbors** have a mole or breakwater, ship sheds (long sloping roofed slips), warehouses, a market stoa and a harbor shrine.

**Two kinds of town.** **Old hill towns grow organically:** stepped lanes, irregular blocks, and buildings fitted to the rock (Elaia, Thyrsa's Kadmeia, Delphoi). **Planned cities use the Hippodamian grid:** straight streets at right angles, blocks of equal size, and the agora as one or two blocks left open (Emporion, Astyra's harbor quarter, colonies). Choose deliberately for each town, and never mix the two at random.

**Architecture.**
- **Orders.** Doric is sturdy, with no base and plain capitals; it belongs to the mainland and the older temples. Ionic is slender, with volute capitals; it belongs to the islands and the east, and suits richer, later buildings. Corinthian is rare and late; save it for one showpiece at most.
- **Materials.** Marble or limestone for sacred and civic buildings. Houses are mudbrick and timber on stone footings, with terracotta tile roofs. Island villages are whitewashed stone cubes with flat roofs; Ichor's blue domes are an accepted design-bible choice for island shrines only.
- **Detail that says Greek:**
  - antefixes along a roof edge, acroteria on gable peaks, a pediment
  - herms at crossroads and stelai beside roads
  - amphorae, pithoi (storage jars) half-sunk in courtyards
  - a *louterion* basin at a sanctuary gate
  - painted stoa walls, bronze tripods, olive-oil lamps
- **Avoid anachronisms:** no Roman arches, vaults or domes on secular buildings, no glass windows, no chimneys, no fences of planks (use dry-stone walls or wattle).

### 4.6 What makes a map incredible

1. **One idea per map, said clearly.** Before placing a tile, write the map's sentence: "a switchback road up a gorge to a cliff-hung sanctuary", or "a harbor town under its akropolis". Every choice serves that sentence.
2. **Approach and reveal.** Hide the best thing, then show it. Approach a temple from below, through a propylon or around a bend, so it appears whole in one screen. Let the player see the next town, peak or tower from far off (a landmark visible across the map) before they can reach it.
3. **Compression and release.** Alternate narrow and open: a tight gorge or lane opens onto a plain, an agora or the sea. Never give the same width for a whole map.
4. **Roads obey the land.** Paths follow contours, switch back up slopes, cross streams at fords or a single bridge, and squeeze through passes. A road that runs straight over a mountain is a placeholder.
5. **Height you can feel.** Use at least two levels per map:
   - terraces, a raised akropolis or plinth
   - cliffs with a cast shadow
   - stairs cut into rock
   - ledges that make the return trip a shortcut
6. **Loops and secrets.** A shortcut that opens back to the start, a hidden item behind a column or in an olive press, a nook only reachable from a ledge above, a cave mouth behind a waterfall. Reward curiosity at every dead end (`MAP_DESIGN.md`).
7. **People in their place.** Put townsfolk where their life happens: the potter at the kiln, the farmer at the threshing floor, the priestess at the altar, the old men in the stoa's shade.
8. **Each place has a signature motif no other map uses.** For example:
   - Thyrsa's vineyards and theater cut into the hill
   - Emporion's ship sheds
   - Eleusa's forest of columns in the Telesterion
   - the diolkos ship-track across the Isthmus
9. **Read it at 15×10.** Every screen should be a good picture on its own: a landmark, a frame, a path through.

**The map brief.** Every new or rebuilt map starts with this five-line brief, recorded in its map-design doc:
- **Sentence:** the one idea.
- **Land:** the ridges, the water, how it slopes.
- **Settlement logic:** why things are where they are.
- **Reveal:** the moment the player sees the best thing.
- **Signature:** the one motif no other map has.

### 4.7 Places: what each one is

These are the real-world models the design bible names, and the features each map should draw on. Use them as references, not copies.

| Place | Model | Build it around |
|---|---|---|
| Elaia, Kalliste | Cycladic hill village | Whitewashed cubes stepping down a slope, stepped lanes, the old olive in the square, a threshing floor, terraces, a dovecote |
| Akti Town | Island harbor town | Mole and breakwater, ship sheds, fish market by the water, the Temple of Hestia on a rise above the harbor |
| Aegina | Aegina: Aphaia, Mt Oros | Pine-wooded ridge, with the Doric temple looking out to sea; a conical peak with a summit altar |
| Emporion City | Piraeus | Hippodamian grid, harbor stoas, ship sheds, herms at the crossroads, the Long Walls heading inland |
| Route 4, Isthmus | Isthmus of Corinth | The **diolkos**, a paved ship-track hauling boats across, plus the Isthmian sanctuary |
| Route 5 | Skironian Rocks | A cliff road high above the sea; Skiron's rock at the drop |
| Eleusa | Eleusis | The Rharian wheat plain, the Kallichoron well, the Telesterion's forest of columns, the start of the Sacred Way |
| Kithairon, Route 6 | Mt Kithairon, Eleutherai | Fir slopes, and a walled fort with square towers guarding the pass |
| Thyrsa | Thebes | The Kadmeia citadel on its hill, gates in the walls, the Dirce spring, vineyards on the plain, the theater in a hillside |
| Route 8, Kopais | Lake Kopais | A marsh lake of reeds, Mycenaean dikes and the island fortress of Gla |
| Lebadeia | Trophonios's oracle | A gorge with the Herkyna spring and the oracle's cave |
| Route 9 | The Schiste | The three-way crossroads in a narrow valley where Oedipus met Laius: a split road and a lone tomb |
| Kirrha | Delphi's port | A sea of olive trees on the plain below the mountains |
| Arkadia, Route 12 | Arcadia, Bassae, Lykaion | Remote pastoral uplands, a lone temple high on a mountain, cypress, shepherds' folds |
| Styx Falls | Mavroneri, Mt Chelmos | A thin waterfall down a black cliff in a high bowl |
| Nemea | Nemea | The Temple of Zeus on a valley floor, a stadium entered by a vaulted tunnel, the lion's cave in the hills |
| Daphni, Route 15 | The Sacred Way | The road from Eleusa to the capital through a pass, with roadside shrines and tombs |
| Astyra | Athens | The Akropolis rock with its Propylaia and Parthenon, the Areopagus, the agora with its stoas below, the Kerameikos with potters and graves at the Dipylon gate, the Pnyx, the Lyceum outside the walls, the harbor at Phaleron |
| Kaldera | Santorini | Caldera cliffs with white towns on the rim, black-sand beaches, and a buried Bronze Age town in the ash |
| Kythera | Paphos | The sea-foam rock where Aphrodite rose, her sanctuary, rose-gardens |
| Knossa | Knossos | A many-storied palace: light wells, red columns that taper downward, horns of consecration, frescoed corridors that become the Labyrinth |
| Lakonia | Sparta | Unwalled villages, the reedy Eurotas river, the wall of Taygetos behind, and the sanctuary of Artemis Orthia: austere, not grand |
| Delphoi | Delphi | A terraced sanctuary on a steep slope: the Sacred Way zigzagging up past treasuries, the temple on its terrace, the theater above, the stadium at the top, the Castalian spring in the ravine, the shining Phaedriades cliffs, and the olive sea far below |

---

## 5. Order of work

1. **System in place:** this guide and the converter. Done 2026-11-16.
2. **Restore the real Act II maps** (Thyrsa, Arkadia) from `world-act2` over the placeholders.
3. **Pokémon, one evolution line at a time**:
   - starters first, from the approved targets
   - then the dex in the order the story reaches each species
   - each line through §3.2–§3.5.
4. **Characters** through the same gate. Samuel's image-model portraits already match the trainer targets closely; the hand-fix pass on faces is what remains.
5. **Maps, town by town** in story order through §4.4: Kalliste first, since it sets the look.
