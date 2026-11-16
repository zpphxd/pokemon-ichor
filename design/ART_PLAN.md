# Ichor art plan: a total conversion

**The user's direction, 2026-11-14:**
- "also the houses and the lanscape etc every sprie needs to be greek myth inspired. we dont want to leave anything really unchanged"
- "temples, columns etc"

**What this means.** Everything the player sees is redrawn for Aethos, apart from Emerald's code. That covers the world, the people, the Pokémon (the new dex, in `design/dex/`), battles and every menu. Nothing on screen should read as Hoenn.

**How we keep it achievable.**
- We redraw what *Aethos* uses. Hoenn's 530 maps get **replaced** by Aethos maps rather than repainted.
- Hoenn-only systems and their art are cut: contests, the Berry Blender, Pokéblocks, secret bases, the Hoenn Battle Frontier facilities, and FRLG data. Cutting them also frees ROM for our art; about 6 MB is free today.
- Each phase redraws the assets that phase needs, and the Phase 1 slice sets the look for everything after it.

## 1. The world: tilesets

**Temples and columns everywhere.** Architecture is the region's signature. Every town has a sacred building, and each Olympian's temple has its own order, materials and symbols:

| Temple | Look |
|---|---|
| Hestia | Doric, with hearth bronze |
| Hermes | Ionic, with a winged frieze |
| Demeter | Wheat-gold, with an underground megaron |
| Dionysus | Ivy-wrapped, with a theater skene |
| Artemis | Moonlit cypress grove |
| Hephaestus | Black basalt forge |
| Aphrodite | Sea-foam marble |
| Apollo | Gold, with the omphalos |
| The Pantheon | Parthenon scale |

| Tileset | Use | Contents |
|---|---|---|
| `aethos` (primary) | Every outdoor map | Olive trees and cypress, sun-bleached grass, limestone paths, dry-stone walls, the sea, steles, and the Asclepeion and Agora exteriors |
| `building` (primary) | Every interior | A Greek repaint: terracotta and marble floors, frescoed walls, amphorae, looms, klinai (couches), oil lamps, braziers, chests, columns |
| `kalliste` | Island villages (Phase 1) | Cycladic houses, a blue-domed shrine, the festival square, the Temple of Hestia facade, the harbor, Kronion Hill's ruins |
| One secondary per biome, as the phases reach it | | Marble city and Akropolis (Astyra); vineyards and theater (Thyrsa); wheat plains and the Mystery sanctum (Eleusa); cypress forest (Arkadia); volcanic caldera (Kaldera); sea-foam coves (Kythera); the Labyrinth (Knossa); Lakonia; Delphoi; Olympus above the clouds; the gray Underworld and golden Elysium; sunken Atlantis |
| One temple interior per Olympian | | As in the table above |
| Interiors | | Houses, Asclepeion, Agora, Akademia, the Pithos room, trireme decks |

Door animations, field effects (grass rustle, water splash, footprints) and the world map get matching art.

## 2. People

- **The player, Theo and Ianthe:** every state, not just walking and running.
  - Surfing on a dolphin-back or a small boat.
  - Fishing, field moves and the battle back pics.
- **The cast:** Daphne, Alethea, Kleon, the Twelve's Hierophants, the Archon, the Team Titan admins and grunts, Phaedon and Elpis.
- **Civilians:** about 40 overworld types for a living Greek world. These include fishers, olive farmers, shepherds, potters, merchants, philosophers, hoplites, priestesses, oracles, children, elders, sailors and athletes.
- **Trainer classes:** about 25 Aethos classes, each with a front portrait and an overworld sprite, replacing the 117 Hoenn classes for everything Aethos uses.

## 3. Pokémon

The ~150-species Aethos dex, in `design/dex/`. Each species gets Gen 3 front and back pics, normal and shiny palettes, a menu icon, a footprint and a follower sprite.

## 4. Battles

- **Battle backgrounds** for each Aethos terrain: olive grove, beach, marble temple, cave, sea, volcanic, Underworld.
- **The battle interface:** HP boxes and the move menu, in pottery style.
- **Trainer intros:** black-figure silhouette transitions, as the bible's §7 describes.
- Battle animations stay as they are.

## 5. Screens and UI

Done so far: the dialogue box and menu frames.

Still to do:
- **Title screen:** a painted amphora.
- **Intro:** Daphne.
- **Main menu.**
- **Bag:** a traveler's satchel.
- **Party menu.**
- **Summary:** a scroll.
- **Pokédex:** a codex.
- **Pithos storage:** jars.
- **Trainer card:** a kylix.
- **The Aethos region map.**
- **Naming screen.**
- **Shop:** the Agora.
- **Evolution scene.**
- **Map-name popups:** carved steles.
- **The Augur's Eye:** DexNav.
- **Laurel case:** the badges.

**Items:**
- Story items and relics get new icons: the Talaria, Daedalus's Wings, Poseidon's Conch, Ichor Stones, laurels.
- Common items are restyled phase by phase as Aethos uses them: medicines as clay flasks and herb bundles, ball cases and so on.

## 6. How it's made

- **One style guide.** The master palette, Gen 3 readability, top-left light, outlines on objects but not on terrain. It's in `design/phase1/PLAN.md`, to be promoted to `design/STYLE.md` once the slice is approved.
- **Shared toolkits** in `tools/ichor/art/`:
  - existing pixel-by-pixel ASCII painters for legacy assets; these are not the
    artistic authoring method for the approved character redraw below
  - the map renderer
  - Porytiles for tilesets.
- **Narrow batches.** One specialist agent per asset group, in its own worktree, committing as it goes.
- **Director review.** Each batch is checked in renders and in-game screenshots before it merges.
- **An inventory,** `design/art/INVENTORY.md`, tracking every asset group with its status (Hoenn, in progress, Greek) so nothing is left unchanged by accident.
- **Town-by-town native redraws.** The approved redraw direction is translated to native GBA pixels, not shipped as high-resolution concept art. Shared sprites are updated with their first town; backs, icons, follower views, palettes and supported animation states must stay consistent. Capture a source baseline with `python3 tools/ichor/sprite_audit.py inventory --output build/sprite_inventory.json`; this includes unplaced and National Dex assets, not just the Aethos dex. Check each regional batch with `python3 tools/ichor/sprite_audit.py check --pokemon Nebrel Kynder Hipling` (replace the names with the batch's species), and trainer portraits with `--image graphics/trainers/front_pics/kleon.png`. The gate checks native dimensions, indexed colors, palettes, nonempty frames and design-to-ROM copies, and reports static frame pairs for visual review. A changed hash or a passing gate is not artistic approval: inspect native-size comparisons and in-game screenshots, then run the build and smoke test before landing each town's commits on `main`.
- **Coverage evidence.** Run `python3 tools/ichor/sprite_audit.py changes --baseline build/sprite_inventory.json --output build/sprite_changes.json` after a batch to list added, removed and changed sources, plus the unchanged count. Reconcile this with the town's asset ledger; the report tracks source coverage, not redraw quality or artistic approval.

### Concept fidelity gate

The approved starter and trainer concepts set the bar for silhouettes,
proportions, expression, pose and coherent material shading, not merely a few
new highlights. Before extending a redraw recipe to a whole batch, review a
native pilot beside both the original production sprite and its approved
concept. Show the real indexed source at 1x and integer nearest-neighbor zoom;
label the concept as an illustration, never as an implemented ROM sprite.
Do not resample an illustration and call it authored native pixel art.

Preserve the character/species identity and gameplay contracts, not poor
geometry simply because an old painter reproduces it. Use expressive faces,
deliberate silhouettes, selective outlines and readable shading clusters.
Species- or portrait-local palette proposals may improve the approved color
identity within the design bible and native budget; shared palette edits need
separate ownership and review. Every affected normal/shiny and companion view
must remain consistent before an implementation lands.

Classify outputs honestly: a small material touch-up is **polish**, unchanged
verified original artwork is **retained**, and a successful native redesign is
a **redraw**. Neither regeneration nor compiled-pixel/renderer checks promote
polish into an approved redesign. A front-only pilot does not close backs,
icons, followers, animation states, a town or the global inventory.

### Approved character direction, 2026-11-16

The user approved the new Theo preview: "Okay this is a great improvement over
what was previously. Go ahead and do this for all character sprites."
This supersedes the rejected polygon/ASCII native pilots as the human-character
style benchmark, not as evidence that the full sprite rollout is complete.
Pokemon, environments, effects and items are not authorized by this
character-only continuation.

The exact approved result is
`design/art/img/theo_approved_64.png` (64x64, indexed, transparent index 0,
14 visible colors; SHA-256
`eab2845d3ffcd20adee2d63978e504747a37a959625bde9fb1f0b6f1ca20cd7f`).
`theo_approved_generated.png` beside it preserves the new image-model output;
`theo_approved_illustration.png` is the unchanged earlier illustration crop.
These are design references, not production imports. The model returned a
1254x1254 image, not an exact native pixel grid. The approved preview trims
transparent margins, fits within 60x60 using nearest-neighbor sampling, centers
the result on 64x64, thresholds alpha at 128 and reduces to at most 15 opaque
colors without dithering, weighting red accents to retain the capture ball.
Call this image-generated and resampled, not hand-authored native pixel art.
Hardware color conversion, palette bindings and companion views still need
verification before integration.

- Use reference-guided image generation for artistic creation, with the
  character's approved design and this Theo style benchmark. Do not substitute
  a code-writing model's polygons, ASCII body parts or cosmetic changes to
  locked old silhouettes. The generated source and the actual native export
  must both be retained.
- Design for the final pixel grid: silhouette first, readable limb gaps,
  expressive faces, purposeful connected shading clusters and selective
  outlines. Simplify minor decoration before sacrificing identity or anatomy.
  Adapt eye, hand and prop proportions when necessary for small-scale clarity.
- Judge native-size results before integer nearest-neighbor enlargements.
  Review against the intended background as well as a neutral surface.
  A large illustration or an attractive enlarged image cannot stand in for
  the actual final sprite. Palette or dimension checks are not artistic gates.
- Preserve the correct size for each role: trainer fronts use 64x64, while
  walkers, rider poses and other states keep their engine-specific dimensions.
  Keep all frame counts, ordering, anchors and action semantics; do not make a
  walking sheet by repeating a standing image.
- Treat the accepted PNG/palette as the artistic source of truth. Deterministic
  tools may arrange, index, convert, encode and validate it, but must not
  silently replace its anatomy with an older painter's output. Preserve
  pre-redraw sources and make source-backed rebuilding explicit.
- Plan front/back/state colors together. Shared palette changes require
  coordinating every reader; a locally attractive palette is not sufficient.
  Original RS/FRLG player identities remain in their accepted preservation
  scope rather than being converted into Theo or Ianthe.

## 7. Order

| Phase | Art |
|---|---|
| **Phase 1 slice** | Kalliste outdoors and the Temple of Hestia; the Greek `building` repaint for the slice's interiors; Theo and Ianthe (all states); the slice's cast and civilians; slice trainer classes; grass, beach and temple battle backgrounds; the battle UI; title, intro, bag, party, summary and Pokédex screens |
| **Phases 2–5** | Each biome's tilesets, temple, people and screens as the story reaches them |
| **Phase 6** | An inventory sweep to make sure nothing Hoenn remains on screen |
