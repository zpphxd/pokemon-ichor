# Field effects for the Kalliste slice

The overworld effects a slice playthrough shows, redrawn to sit on the aethos and civic tiles. Every file keeps Emerald's size, frame layout and animation, so no engine table changed.

**Sources:**
- `tools/ichor/art/field_effects.py`: every effect and the two shared effect palettes. Rebuild with `/usr/bin/python3 tools/ichor/art/field_effects.py --write`. `--preview DIR` writes the 6× art sheet.
- `tools/ichor/art/surf_poses.py`: Theo and Ianthe riding the dolphin. Rebuild with `/usr/bin/python3 tools/ichor/art/surf_poses.py --write`.

**Images (`img/`):**
- `field_effects_before_after.png`: each effect in game over aethos, Emerald's on the left and Ichor's on the right, at 3×.
- `field_effects.png`: every redrawn effect frame at 6×, over the tile it plays on.
- `surf_dolphin.png`: both riders on the dolphin in all six surfing frames, each in their own palette, as the game draws them.

## What changed

| Effect | Files | Palette | Now | Plays on |
|---|---|---|---|---|
| Tall-grass rustle | `tall_grass.png` | general_1 | Cut from aethos's barley metatile (`0x00D`), so the tuft over the player's feet matches the tile pixel for pixel. Each step bends the stalks apart and throws gold grain and chaff. | `MB_TALL_GRASS`, Route 1 |
| Landing in tall grass | `jump_tall_grass.png` | general_1 | Stalks and grain burst out from under the feet. | Ledges into barley |
| Long grass | `long_grass.png`, `jump_long_grass.png` | general_1 | Cut from aethos's reeds (`0x015`). They part around the player as they step in, then close. | `MB_LONG_GRASS` |
| Footprints | `sand_footprints.png` | general_0 | Sandal soles: smooth ovals with a strap dent, in the sand's own shades. | `MB_SAND`, the Akti beach |
| Ripples | `ripple.png` | general_1 | Emerald's rings, now in foam white and aethos turquoise. The outer ring fades into the puddle's own color. | `MB_PUDDLE`, `MB_POND_WATER` |
| Splashes | `splash.png`, `jump_small_splash.png`, `jump_big_splash.png` | general_0 | Emerald's droplets in aethos's foam and sea blues. | Puddles, shallows |
| Ledge-hop dust | `ground_impact_dust.png` | general_0 | Emerald's puffs, now in pale limestone dust. | Landing from a ledge |
| Emotes "!", "?", "!!", "X" | `emotion_exclamation.png`, `emotion_question.png`, `emotion_double_exclamation.png`, `emote_x.png` | may | Pottery shards with black-figure glyphs, after the pottery UI. A cream glaze chip on the top left and a broken edge on the top. | Trainers spotting you, scripted emotes |
| Heart emote | `emotion_heart.png` | npc_1 | The same shard, with a black-figure heart. | Scripted emotes |
| Warp arrow | `arrow.png` | the player's palette | Terracotta with an ink outline and a cream glint; it blinks to saffron. | Standing on an exit mat |
| Surf mount | `surf_blob.png` | the player's palette | A Minoan dolphin for Poseidon's Conch, after the Knossos fresco: an Aegean-blue back, a saffron stripe down the flank, a cream belly. Facing south, its head comes up between the rider's shins. Facing north, the tail flukes show. In profile, the snout, dorsal fin and raised tail show past the rider. | Surfing |
| Riders | `people/brendan/surfing.png`, `people/may/surfing.png` | brendan, may | Theo and Ianthe astride, in their petasos and chlamys, shins down the dolphin's flanks, plus a hop pose for mounting and dismounting. They replace Emerald's recolored Brendan and May. | Surfing |
| Heal: the "monitor" | `pokecenter_monitor/0.png`, `1.png` | general_0 | The Asclepeion's rod-of-Asclepius relief lighting up during the heal: the serpent white and gold, the rod gold, flickering bright and dim. The pixels are traced from the relief in `rooms/akti_asclepeion.bin` (map pixels x 112–135, y 8–23), so the glow lands on it. Before, a pale rectangle flashed beside the relief. | `FLDEFF_POKECENTER_HEAL` |
| Heal: the balls | `pokeball_glow.png` | pokeball_glow | Each ball floats in the spring with a ripple ring at its waterline. The ball keeps the slots the heal flashes (2, 3, 5, 6, 8); the ring uses the palette's untouched blues (12, 13). | The spring basin |

## Palettes

**Shared effect palettes.** `general_0.pal` and `general_1.pal` are shared by many effects, including ones the slice never shows, so each index keeps its Emerald role: greens stay greens, water stays water, sand stays sand. The untouched effects still draw sensibly.

| # | general_1 (grass, reeds, ripples) | general_0 (sand, splashes, dust, glow) |
|---|---|---|
| 1 | barley light (160,176,80) | limestone dust light (248,240,216) |
| 2 | barley mid (112,128,64) | limestone dust (232,216,176) |
| 3 | barley shade (72,88,48) | limestone dust shade (208,184,136) |
| 4 | barley dark (40,56,32) | foam white (248,248,240) |
| 5 | meadow grass (184,184,104) | water light (176,216,240) |
| 6 | puddle water (88,176,200) | water (112,168,224) |
| 7 | sea-sky water (112,168,224) | sea (80,136,200) |
| 8 | water light (176,216,240) | deep sea (48,104,176) |
| 9 | foam (248,240,216) | gold glow (240,192,64) |
| 10 | ash (Emerald's, kept) | ink (32,24,24) |
| 11 | ash light (Emerald's, kept) | sand (232,208,144) |
| 12 | barley grain gold (240,192,64) | sand print rim (216,192,128) |
| 13 | grain ochre (200,144,40) | sand print (200,168,104) |
| 14 | meadow shade (144,152,72) | sand print deep (176,144,96) |
| 15 | meadow light (208,200,128) | ochre glow shade (200,144,40) |

- **Tile colors.** The barley, reed, puddle and sand colors are the aethos tile colors exactly. The painter refuses to cut a tile frame if a tile color is missing from the effect palette.
- **The player's palette.** The surf mount and the warp arrow load the current player's palette: brendan.pal for Theo, may.pal for Ianthe (`FldEff_SurfBlob` and `CreateWarpArrowSprite` call `LoadPlayerObjectEventPalette`).
  - So they use only slots both palettes give the same meaning: straw 10–11, terracotta 12–13, cream 14 and ink 15.
  - The dolphin also uses the two blue slots, 5 and 6, as Emerald's blob did. It is a lighter blue under Theo and a deeper blue under Ianthe.
- **may.pal.** The "!" family always loads may.pal, and draws only in its terracotta, cream and ink.

## Testing

The check ran in the headless runner, over the real tiles, with temporary patches that were reverted before committing:
- **The lab.** `LAYOUT_KALLISTE_ROUTE1` was switched to `gTileset_Aethos` + `gTileset_Kalliste` and filled with a test lab: barley, reeds, sand, a puddle pool, a row of ledges landing on reeds, grass, barley and a puddle, the sea, and an exit mat with a warp.
- **The NPCs.** Five folk walkers stood in the lab for the emotes.
- **The start.** `src/new_game.c` started the game in the lab: on grass for the land route, and on the sea for the surf route, where spawning on water starts surfing.
- **The heal.** A third patch pointed `AktiTown_Asclepeion` at the civic room and gave the party three Pokémon.
- **The Lua driver.** It walks a waypoint route by reading the player's coordinates from `gObjectEvents`, so the route doesn't depend on frame counts. It jumps each ledge, triggers every emote on the NPCs by setting their held movement (`movementActionId` 0x56, 0x57, 0x9F, 0x58, 0x9E), and talks to the healer. It screenshots each effect.

## Left as they are

| Effect | Why |
|---|---|
| Jump and object shadows (`shadow_*.png`) | Neutral blended ovals in the weather palette. They read the same on any ground. |
| Bike tire tracks, follower tracks (slither, spot, bug), deep-sand footprints, sand pile | Not in the slice: Aethos has no bikes, and aethos has no `MB_DEEP_SAND`. They take the new sand colors through general_0. |
| Short grass (`short_grass.png`) | aethos has no `MB_SHORT_GRASS`. It now draws in barley and gold, and needs redrawing if a short-grass metatile is added. |
| Ash, hot springs, cave dust, bubbles and water surfacing (Dive), rock climb, secret power, sand pillar, Deoxys rock, record mix lights, spotlight, Hall of Fame monitors, field-move streaks, ORAS dowsing, Fly's bird, Cut grass, the tree/mountain/sand disguises, Hoenn's scripted sparkles, the shiny sparkle, unused grass and sand | Not reachable in the slice. The water and sand ones take the new colors. |
| Night lights on Center and Mart signs (`BallLight`, `PokeCenterLight`, `MartLight`) | They spawn only from light objects placed on a map, and no slice map places one. |
| The smiley (`graphics/misc/emoticons.png`) | FRLG's; no Emerald script plays it. The follower balls and emotes are done since (`follower_icons.py`, `UI_remnants.md`). |

## Found while testing: the truck intro still runs on a new game

`CB2_NewGame` in `src/overworld.c` still sets `gFieldCallback = ExecuteTruckSequence`. This is Emerald's moving-truck intro, and Quickstart uses the same path.
- **What it does.** On the first load it writes the truck's door and exit-light metatiles into cells (4,1), (4,2) and (4,3) of whatever map the game starts in. The ids are 0x20D–0x20F, then 0x208, 0x210 and 0x218. It also runs the truck's camera-shake task.
- **In the slice.** The start map is the player's bedroom, so those three cells show stray pieces of the bedroom's secondary tileset. It is the white "fridge" at the back wall in the smoke test's start screenshot. On any kalliste map they draw as Cycladic house pieces.
- **Suggested fix (engine).** Use `FieldCB_WarpExitFadeFromBlack`, as the FRLG branch already does.
- **Other art outside `graphics/field_effects/`.**
  - **Door animations.** They are still Hoenn. They live in `graphics/door_anims/` and belong to the tilesets (`TILES_aethos.md`).
  - **Berry trees.** They are object-event sprites; no slice map places one yet.
