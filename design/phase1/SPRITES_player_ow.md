# Theo and Ianthe: overworld sprites

Theo and Ianthe replace Brendan and May in the overworld. They share one design, which matches the battle back pics:
- a wide-brimmed straw **petasos** in sun-gold, with a brown cord at the crown
- an Aegean-blue **chlamys**, pinned with a gold brooch at the right shoulder
- a cream **chiton**, belted
- brown sandals and a small terracotta satchel at the left hip.

Theo has short black hair. Ianthe has dark-brown hair to the jaw and a low braid tied with terracotta. The braid shows down her back and behind her neck in the side view.

## Sheets

The source is `tools/ichor/art/sprites_player_ow.py`. Every frame is built from hand-edited ASCII parts: a petasos, a face per facing and per character, and a body per pose. The parts use role letters (skin, chlamys, chiton and so on), so one body serves both characters.

```
python3 tools/ichor/art/sprites_player_ow.py --write            # all sheets and both palettes
python3 tools/ichor/art/sprites_player_ow.py --write --sheets walking
python3 tools/ichor/art/sprites_player_ow.py --preview design/phase1/img/sprites_player_ow.png
```

## Review images

| Image | Shows |
|---|---|
| `design/phase1/img/sprites_player_ow.png` | Every sheet for both characters at 4x |
| `design/phase1/img/sprites_player_ow_ingame_theo.png` | Theo in the bedroom at 3x: walking and running in all four directions, mid-step |
| `design/phase1/img/sprites_player_ow_ingame_ianthe.png` | The same for Ianthe |
| `design/phase1/img/sprites_player_ow_rom.png` | Every player frame decoded from the built ROM with the new palettes, with the mirrored east-facing frames |

| Sheet | Size | Frames | Status |
|---|---|---|---|
| `walking.png` | 144×32 | 9 of 16×32: down, up, left standing, then 2 steps each for down, up, left. Walk steps bob down 1 px. Right is the left frames mirrored. | Done |
| `running.png` | 144×32 | Same order as walking. Crouched 1 px, strides 2 px; fists pumping, the chlamys flaring, and a little cream wing at each heel for the Talaria (the bible's running-shoes relic). | Done |
| `fishing.png` | 384×32 | 12 of 32×32, figure centered: 0–3 west (Old Rod over the shoulder, raised, cast, out), 4–7 north, 8–11 south. A bite alternates 2/3, 6/7 or 10/11; east mirrors west. The rod is cane-brown with a straw highlight and a terracotta float. | Done |
| `field_move.png` | 160×32 | 5 of 32×32, facing south: reach into the satchel (0–1), hold the relic at the chest (2), lift it (3), raise it overhead, glinting (4). Aethos has no HM Pokémon; field powers come from relics (bible §8), so the player raises a golden relic instead of a ball. | Done |

Both folders are `graphics/object_events/pics/people/brendan/` (Theo) and `.../may/` (Ianthe). The bike, watering, decorating, underwater and surfing sheets are untouched; Aethos has no bikes or watering cans, and surfing (on a dolphin) is a later batch.

## Palettes: how the roles were remapped

`graphics/object_events/palettes/brendan.pal` and `may.pal` are shared with every player sheet (bike, surf, fishing, watering and so on), the rival Brendan and May sprites and the link-player sprites. `may.pal` also colors the trainer "!" and "?" emotes, which use indices 14 and 15. So each index keeps its Emerald role and is recolored by role, and the untouched sheets still draw sensibly.

The two palettes never had the same roles. The brief's suggested mapping (navy at 5–8) holds for Brendan but not for May, so each palette is remapped on its own terms:

| Index | `brendan.pal` role | Theo | `may.pal` role | Ianthe |
|---|---|---|---|---|
| 1–3 | skin | skin (248,208,168) (232,160,112) (184,112,72) | skin | same |
| 4 | skin outline | warm brown (104,56,40): skin outline, sandals, hat cord | skin outline | same |
| 5 | navy, light | chlamys highlight (112,168,224) | gray (bandana knot) | chlamys (48,104,176) |
| 6 | navy | chlamys (48,104,176) | dark slate (shorts) | chlamys shade (24,56,120) |
| 7 | navy, dark | chlamys shade (24,56,120) | hair brown | hair (128,80,48) |
| 8 | navy, darkest (hair) | black hair's sheen (48,48,64) | hair dark brown | hair shade (72,40,32) |
| 9 | light gray | chiton shade (216,192,144) | light gray | same |
| 10–11 | green (hat band) | straw (240,192,64) (200,144,40) | green (bandana) | same |
| 12–13 | red | terracotta satchel (224,136,88) (184,88,48) | red | same |
| 14 | white | chiton cream (248,240,208) | white | same; the "!" emote's fill turns cream |
| 15 | black | ink (32,24,24) | black | same |

Only Theo has a chlamys highlight; Ianthe's chlamys uses two shades because `may.pal` has two free slots for it.

## Side effects on the untouched sheets

These still use Brendan's and May's art, so they now draw in the new colors:
- **Brendan's bike, surf, watering, decorating and underwater sheets:** the white beanie turns cream, the navy clothes Aegean blue, the green band straw-gold, the red trim terracotta.
- **May's:** the green bandana turns straw-gold, the brown hair stays brown, the gray knot and dark shorts turn Aegean blue.
- **Rival Brendan and May** (`OBJ_EVENT_GFX_RIVAL_*`) and the **link players** take the same colors. Ichor's rival is Kleon, so the rivals should not appear in the slice.
- **The "!" and "?" emotes** above trainers use `may.pal` 14 and 15: cream with ink, nearly as before.
- **Reflections** are filtered from the live palette by the engine, so they follow automatically.

## Checking

`tools/ichor/tests/player_ow_walk.lua` Quickstarts a new game, forces the gender (`WALK_GENDER=0` Theo, `1` Ianthe), gives the running shoes, then walks 2 tiles each way in the bedroom and runs the same way holding B, taking a screenshot every 2 frames:

```
mkdir -p build/walk_test/theo
WALK_GENDER=0 WALK_OUT=build/walk_test/theo/ build/tools/ichor-mgba-headless \
    --script tools/ichor/tests/player_ow_walk.lua --frames 4200 --until "WALK done" pokeemerald.gba
python3 tools/ichor/art/sprites_player_ow_review.py shots build/walk_test/theo out.png --title Theo
```

The `shots` review crops the player at 3x into one row per move.

Fishing and the field move can't be reached from the bedroom (they need water and an Old Rod, or a field-move target), so they are checked from the ROM instead:

```
python3 tools/ichor/art/sprites_player_ow_review.py rom out.png
```

This decodes every player frame and both palettes from `pokeemerald.gba` at the symbols the engine loads (`gObjectEventPic_BrendanFishing` and so on), with the mirrored east-facing frames. It proves the build's tiling and colors, but not the animation timing in play.
