# Battle backgrounds

The slice's battle backgrounds are redrawn as Greek scenes. Each one is generated from a script in `tools/ichor/art/`, so edit the script and rerun it rather than touching the PNGs.

## What each environment is now

| Environment | When the game uses it | Scene | Script |
|---|---|---|---|
| `GRASS` | Tall grass (Route 1) | **Olive grove and meadow.** An old olive frames the screen; past the meadow, young olives line the coast, with the Aegean and a far island carrying a small Doric temple. The platforms are turf rings on an earth bank. The intro sweep is tall grass with red anemones. | `battle_bg_grass.py` |
| `SAND` | Sand tiles (Akti's beach) | **Akti's shore.** Surf breaking on a pale beach, a far islet with a white shrine under a blue dome, a fishing boat, an amphora half buried in the sand. The platforms are sand mounds. The intro sweep is a breaking wave. | `battle_bg_sand.py` |
| `WATER` | Fishing or surfing on ocean water | **The open Aegean.** A high sun with a road of glitter on the sea, and a trireme on the horizon. The platforms are rings of lighter water edged in foam. The intro sweep is a wave curling like the Greek wave scroll. | `battle_bg_water.py` |
| `BUILDING` | Every indoor map, including the Temple of Hestia | **A Doric temple hall.** Fluted columns under a triglyph frieze, a painted meander on the wall, bronze braziers, votive shields with Hestia's flame, and a polished floor. The platforms are marble discs with a bronze inlay. The intro sweep is streaks of firelight. | `battle_bg_building.py` |
| `GYM` | Maps with `MAP_BATTLE_SCENE_GYM` | The temple hall, cooler, with an Aegean-blue frieze | `battle_bg_building.py` |
| `LEADER` | Leader-class trainers, so the Hierophants | The temple hall with the hearth blazing: amber walls and gold light | `battle_bg_building.py` |
| `PLAIN` | Paths and open ground in towns and on routes | **The colonnade in the open air**, with sky and far green hills between the columns and a sunny limestone terrace. See *Plains* below. | `battle_bg_building.py` |
| `FRONTIER` | Link battles | The temple hall by moonlight | `battle_bg_building.py` |
| `KYOGRE` | Hoenn only | The open-sea tiles in a storm palette, so its colors still fit them | `battle_bg_water.py` |

Still Hoenn: `LONG_GRASS`, `POND` (pond water, for example if Akti's harbor uses pond-water tiles), `MOUNTAIN`, `CAVE`, `UNDERWATER`, the Rayquaza sky, and the stadium backgrounds of the Elite Four and the teams.

## Plains

The engine's table (`src/data/battle_environment.h`) draws `PLAIN` with the **building** tiles and only swaps the palette. So with art changes alone, plains get the temple's colonnade, recolored as open air.

To make plains use the olive grove instead, the director can change one line: in the `[BATTLE_ENVIRONMENT_PLAIN]` entry, set `.background = ENVIRONMENT_BACKGROUND(TallGrass),`. Then run `python3 tools/ichor/art/battle_bg_grass.py --plain-grove`, which writes `plain/palette.pal` for the grove, with trodden-earth platforms in place of turf. I didn't make that edit, because it is battle data outside the art files.

## Format and limits

Every replaced background keeps the engine's format.
- `tiles.png` holds at most 256 4bpp tiles.
- `map.bin` is 64×32 tiles: two 32×32 screen blocks.
- The palette is 48 colors, loaded to BG palettes 2–4. Each 8×8 tile uses one 16-color sub-palette.
- The entry overlay (`anim_tiles.png` and `anim_map.bin`) is a 32×32 map; color 0 is transparent.

Current tile counts:

| Background | Scene tiles | Entry tiles |
|---|---|---|
| Grass | 252 | 146 |
| Sand | 192 | 62 |
| Water | 215 | 42 |
| Building | 138 | 52 |

These constraints shape how the scenes are drawn:
- **The left 240×112 is what the player sees.** The battle text box covers BG3 from y = 112 down.
- **Each scene is a 256-pixel strip that wraps.** During the intro slide, the top half of the screen scrolls in from x = 240 and the bottom half from x = −240, so the whole 512-pixel width shows and has to join up. After a catch, the game shows x = 256–495. So the scenery repeats every 256 px. The left screen block gets the platforms; the right block is bare scenery.
- **Rows 240–255 repeat the top color,** because a screen shake can show them above row 0.
- **The platforms sit where the battlers stand.** The far platform is centered at (176, 69) and the near one at (64, 109), both 124 × 26 px plus a 2–5 px bank. Their texture follows the platform, not the screen, so the two share tiles.
- **The building streaks may only use BG palette 4, colors 1–5.** The Hoenn stadium palettes reuse that overlay, as in vanilla. Every building palette keeps its streak colors in those slots.
- **Palette variants share one layout.** `Pal.variant()` changes colors by name. The plains palette fades the wall, frieze and shields into the sky by giving them sky colors.

Colors come from the master palette families in `PLAN.md`, all multiples of 8.

## Tools

- **`battle_bg_lib.py`** is the shared toolkit. It paints on a canvas of named colors, then tile-izes: it picks a sub-palette for each tile, dedupes with flips, writes the files, and reports any tile that mixes sub-palettes.
- **`battle_bg_<scene>.py`** draws one scene and its variants. Pass `--preview DIR` to see the raw canvas.
- **`battle_bg_mockup.py`** renders the built files as the GBA would. Each mock-up has three parts: a 240×160 battle with a pic on each platform and the real text box, an intro-slide frame, and the whole map. Output goes to `design/phase1/img/battle_bg_<name>.png` at 3×.
- **`battle_bg_check.py`** shows each background in the real ROM, headlessly. It boots Quickstart, opens the debug menu (hold R, press START), and picks *Party > Start Debug Battle*. While the battle loads, it writes the environment id to `gBattleEnvironment`; debug battles never recompute it. Screenshots go to `build/battle_bg/<env>/`. The sheet `design/phase1/img/battle_bg_<env>_ingame.png` puts the slide, the trainers and the action menu side by side at 3×. Run `make` and `tools/ichor/smoke_test.sh` first.

## Images

| Environment | Mock-up | In-game |
|---|---|---|
| Grass | `img/battle_bg_grass.png` | `img/battle_bg_grass_ingame.png` |
| Sand | `img/battle_bg_sand.png` | `img/battle_bg_sand_ingame.png` |
| Water | `img/battle_bg_water.png` | `img/battle_bg_water_ingame.png` |
| Building | `img/battle_bg_building.png` | `img/battle_bg_building_ingame.png` |
| Gym | `img/battle_bg_gym.png` | `img/battle_bg_gym_ingame.png` |
| Leader | `img/battle_bg_leader.png` | `img/battle_bg_leader_ingame.png` |
| Plains | `img/battle_bg_plain.png` | `img/battle_bg_plain_ingame.png` |
| Frontier | `img/battle_bg_frontier.png` | none (link battles only) |

These shots were taken before the battle interface pass, so their text box and HP boxes are still vanilla. The game's are pottery now (`UI_battle.md`, `img/ui_battle_compare.png`).
