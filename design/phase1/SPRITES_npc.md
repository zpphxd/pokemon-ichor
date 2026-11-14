# Ichor overworld NPCs

Walking sprites for Ichor's people, as new object-event graphics IDs. The trainer portraits are in `SPRITES.md`.

- **Source:** `tools/ichor/art/sprites_npc.py`. Every frame is ASCII art in that file, one character per pixel.
- **Rebuild the PNGs and the palette:** `python3 tools/ichor/art/sprites_npc.py --write`
- **Preview:** `python3 tools/ichor/art/sprites_npc.py --preview DIR` writes the 4× sheet and 8× pixel grids for editing.

## Catalog

| Constant | Sheet | Look |
|---|---|---|
| `OBJ_EVENT_GFX_ICHOR_KLEON` | `ichor/kleon.png` | Short-cropped dark hair, linen exomis, a crimson chlamys behind, and a bronze armband on his right arm |
| `OBJ_EVENT_GFX_ICHOR_PROFESSOR_DAPHNE` | `ichor/professor_daphne.png` | Chestnut bun under a laurel wreath, and a floor-length Aegean-blue chiton with a white himation over her left shoulder. She carries a scroll in the crook of her left arm. |
| `OBJ_EVENT_GFX_ICHOR_ALETHEA` | `ichor/alethea.png` | Dark ponytail tied under a blue headband, and a sun-gold chiton to the knee. She has a leather satchel of scrolls on her left hip and a small trowel in her right hand. |
| `OBJ_EVENT_GFX_ICHOR_HIEROPHANT_IONE` | `ichor/hierophant_ione.png` | Cream veil to the waist, and a terracotta robe with a gold hem. She holds a lit bronze oil lamp in both hands. |
| `OBJ_EVENT_GFX_ICHOR_TITAN_GRUNT` | `ichor/titan_grunt.png` | Bronze Corinthian helmet with a crimson crest and a T-shaped face opening with red eyes. Slate tunic with a bronze sickle emblem, bronze shoulder guards and greaves. |

- **Sheet location:** sheets are in `graphics/object_events/pics/people/ichor/`.
- **Palette:** all five use the palette tag `OBJ_EVENT_PAL_TAG_ICHOR_CAST`.
- **Alethea's colors:** she has no portrait yet, so her colors are new. The sun-gold comes from the master palette, and the blue headband ties her to Daphne's Akademia.

Previews:
- `img/sprites_npc_sheets.png`: every frame at 4×. Vanilla Birch is in the first row for scale.
- `img/sprites_npc_ingame.png`: three moments of the five wandering in the player's room, at 3×.

## The shared cast palette

**Palette file:** `graphics/object_events/palettes/ichor_cast.pal`, loaded as `gObjectEventPal_IchorCast`.

**How it was built:** the ramps come from the trainer portraits and were merged so that each slot serves several characters.

**Fixed order:** the order is fixed. Each sheet's PNG embeds this exact palette, so changing a color means editing `CAST_COLORS` and re-running `--write`.

| # | Char | Name | RGB | Used for |
|---|---|---|---|---|
| 0 | `.` | transparent | 112 192 160 | Never drawn |
| 1 | `k` | ink | 32 24 24 | Outlines and eyes |
| 2 | `b` | brown | 88 48 32 | Kleon's and Alethea's hair; leather, sandals and the satchel |
| 3 | `r` | red_d | 120 32 40 | Shadow for the cloak, robe and crest |
| 4 | `u` | umber | 168 88 48 | Ione's robe, Daphne's hair and bronze shadow |
| 5 | `c` | crimson | 216 64 56 | Kleon's cloak, the helmet crest and the lamp flame |
| 6 | `s` | skin_d | 224 152 104 | Skin shadow and the terracotta highlight |
| 7 | `S` | skin_l | 248 208 168 | Skin |
| 8 | `o` | bronze | 216 160 64 | Bronze, the gold hem and Alethea's chiton |
| 9 | `O` | bronze_l | 248 216 112 | Bronze highlight, the sickle emblem and the lamp |
| 10 | `l` | linen_d | 200 176 144 | Shadow for linen, veil and parchment |
| 11 | `L` | linen_l | 248 240 216 | Kleon's tunic, Ione's veil, Daphne's himation and scrolls |
| 12 | `n` | blue_d | 24 56 120 | Aegean-blue shadow |
| 13 | `B` | blue | 48 104 176 | Daphne's chiton and Alethea's headband |
| 14 | `t` | slate | 72 64 96 | Titanborn tunic |
| 15 | `g` | leaf | 120 144 56 | Laurel |

## Sheet format

- **Layout:** each sheet is 144×32 pixels: nine 16×32 frames side by side, as in every Emerald NPC (compare `prof_birch.png`). Right-facing frames are the left frames flipped in game.

  | Frame | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
  |---|---|---|---|---|---|---|---|---|---|
  | Pose | face down | face up | face left | walk down A | walk down B | walk up A | walk up B | walk left A | walk left B |

- **Color format:** 4bpp indexed PNG with color 0 transparent.
- **Proportions:** standing figures have their feet on row 30.
- **Step bob:** walk frames drop the head and body 1 px, as the Gen 3 step bob does, so the stepping foot lands on row 31.
- **How a character is drawn in `sprites_npc.py`:**
  - Each direction has a `top` block (the head) and three body blocks: `stand` and two `walk` blocks.
  - `build_sheet` places them.
  - A walk block written as `"mirror"` is the other walk block flipped. Use it only for symmetric characters.

## How a later batch adds an NPC

Keep every addition inside the marked **`// Ichor object events`** blocks. They sit at the end of each table, so Hoenn entries stay untouched and upstream merges stay clean.

### 1. Draw the sheet

- **If the character fits the cast palette** above, add it to `CAST` in `sprites_npc.py`.
- **Otherwise,** create `tools/ichor/art/sprites_npc_<batch>.py`:
  - Import `Palette`, `build_sheet` and `save_indexed`.
  - Define its own 15 colors, with one palette per family (shepherds, priestesses and so on).
  - Write `graphics/object_events/palettes/ichor_<batch>.pal` with `Palette.write_jasc`.
- **Either way,** write the sheet to `graphics/object_events/pics/people/ichor/<name>.png`.

### 2. A new palette only: claim a tag

These steps apply only when the batch has its own palette.

1. In `include/constants/event_objects.h`, add the next free tag at the end of the Ichor palette-tag block:

   ```c
   #define OBJ_EVENT_PAL_TAG_ICHOR_<BATCH>  0x1135
   ```

   Ichor owns 0x1134–0x114F.
2. In `src/data/object_events/object_event_graphics.h`, in the Ichor block, add:

   ```c
   const u16 gObjectEventPal_Ichor<Batch>[] = INCGFX_U16("graphics/object_events/palettes/ichor_<batch>.pal", ".gbapal");
   ```

3. In `src/event_object_movement.c`, in the Ichor block of `sObjectEventSpritePalettes`, add:

   ```c
   {gObjectEventPal_Ichor<Batch>, OBJ_EVENT_PAL_TAG_ICHOR_<BATCH>},
   ```

   Every tag the game loads must appear in this table.

### 3. Register the graphics ID

Add one entry to each of these five files, always inside its Ichor block:

| File | Add |
|---|---|
| `include/constants/event_objects.h` | `OBJ_EVENT_GFX_ICHOR_<NAME>,` at the end of the Ichor block, before `NUM_OBJ_EVENT_GFX` |
| `src/data/object_events/object_event_graphics.h` | `const u32 gObjectEventPic_Ichor<Name>[] = INCGFX_U32("graphics/object_events/pics/people/ichor/<name>.png", ".4bpp", "-mwidth 2 -mheight 4");` |
| `src/data/object_events/object_event_pic_tables.h` | `static const struct SpriteFrameImage sPicTable_Ichor<Name>[] = { overworld_ascending_frames(gObjectEventPic_Ichor<Name>, 2, 4), };` |
| `src/data/object_events/object_event_graphics_info.h` | A copy of `gObjectEventGraphicsInfo_IchorKleon`, renamed, with its own `.images` and the right `.paletteTag` |
| `src/data/object_events/object_event_graphics_info_pointers.h` | An `extern` line in the Ichor extern block, and `[OBJ_EVENT_GFX_ICHOR_<NAME>] = &gObjectEventGraphicsInfo_Ichor<Name>,` in the table |

- **No makefile rule needed.** `INCGFX_U32` converts the PNG at build time, so `spritesheet_rules.mk` needs no rule.
- **`paletteSlot` is not read by the engine.** Overworld palettes load by tag into any free OBJ slot. Leave it as `PALSLOT_NPC_SPECIAL`.

### 4. Mind the palette budget

- Each distinct palette tag on screen takes one of the 16 OBJ palette slots. It takes a second slot when it casts a water reflection.
- The player, followers, field effects and the UI share those same slots.
- So group NPCs into palette families, and keep the number of different Ichor tags on one map small.

### 5. Verify in game

1. **Place the NPCs.** Temporarily add the new NPCs to `data/maps/ElaiaVillage_PlayersHouse_2F/map.json`, the room Quickstart starts in. Give them `MOVEMENT_TYPE_WANDER_AROUND` and a range of 1.
2. **Build.**
3. **Capture screenshots** with a Lua script on `build/tools/ichor-mgba-headless`. This one presses START on frame 500 and SELECT on frame 1020, as the smoke test does, then screenshots every 12 frames from frame 2300:

   ```lua
   local K = C.GBA_KEY
   local held, releaseAt, n = nil, 0, 0
   callbacks:add("frame", function()
     local f = emu:currentFrame()
     if held and f >= releaseAt then emu:clearKey(held); held = nil end
     if f == 500 then emu:addKey(K.START); held = K.START; releaseAt = f + 6 end
     if f == 1020 then emu:addKey(K.SELECT); held = K.SELECT; releaseAt = f + 6 end
     if f >= 2300 and f < 3740 and (f - 2300) % 12 == 0 then
       n = n + 1; emu:screenshot(string.format("build/npc_check/shot_%03d.png", n))
     end
     if f == 3750 then console:log("SMOKE done at frame " .. f) end
   end)
   ```

   Run it with:

   ```bash
   build/tools/ichor-mgba-headless --script build/npc_check/npc_check.lua --frames 4000 --until "SMOKE done" pokeemerald.gba
   ```

4. **Check the screenshots** at 3×.
5. **Revert the map:** `git checkout -- data/maps/ElaiaVillage_PlayersHouse_2F/map.json`.
6. **Rebuild, then run `tools/ichor/smoke_test.sh`.**

## Field objects

Small props that scripts show and hide, drawn 16×16 in the cast palette so they cost no extra OBJ palette slot.

- **Source:** `tools/ichor/art/sprites_objects.py`. Rebuild with `--write`; `--preview DIR` shows each object on grass and on a pale slab at 4×.
- **Sheets:** `graphics/object_events/pics/misc/ichor/<name>.png`, one 16×16 frame.
- **Registration:** the same five files as a walker, but set up like the vanilla Fossil: `INCGFX_U32(..., ".4bpp")` with no `-mwidth`/`-mheight`, `obj_frame_tiles` in the pic table, and a 16×16, `.inanimate = TRUE`, `sAnimTable_Inanimate` graphics info.

| Constant | Sheet | Look | Used |
|---|---|---|---|
| `OBJ_EVENT_GFX_ICHOR_TABLET` | `misc/ichor/tablet.png` | An unfired clay tablet lying face up, a sickle pressed into one corner and a scratched list of places, one line struck through. The bottom right corner is chipped. | Kronion Hill, beat 5: the Titanborn drop it fleeing the summit |

## Still open

- **Shading:** the sheets use two tones per material plus the outline. Vanilla NPCs often use three, so a polish pass could add mid-tones. That would need a freed palette slot or a second cast palette.
- **Mirrored props:** right-facing frames are mirrored, as for every Gen 3 NPC. So Kleon's armband and Daphne's scroll swap arms when the character faces right.
- **Not tested in Porymap:** the sheets have not been opened in Porymap yet. The entries follow the vanilla format exactly, so they should display.
