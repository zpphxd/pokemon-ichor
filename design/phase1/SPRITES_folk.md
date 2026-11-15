# Ichor townsfolk and trainer-class walkers

Overworld walking sprites for Kalliste's island people and the slice's trainer classes: 22 new object-event graphics IDs. The cast (Kleon, Daphne, Alethea, Ione, the Titanborn) is in `SPRITES_npc.md`; the battle portraits the class walkers match are in `SPRITES_classes.md`.

**2026-11-15 Elaia polish:** `mom`, `priestess`, `youth_m`, `youth_f`,
`man`, `woman`, `elder_m`, `elder_f`, `kid_m`, `fisher`, `harvester` and
`shepherd` now use the native `elaia_*` cloth bodies in the same source file.
They add shoulder/waist/hem folds without changing costumes, props, stature,
palette tags, or the nine-frame engine order. Kydippe also has shaded shawl
folds. The ten walkers outside that checkpoint were reserved for their own
town batches. All twelve generated arrays and distinct movement frames have
been checked. The rebuilt ROM passes smoke and the three Elaia opening runs,
with current village/interior captures of the shared folk. The earlier
screenshots below are historical; native checks do not replace director
review of every character and pose.

**Akti harbor checkpoint:** `sailor` and `diver` now use eight-row directional
heads and the longer native `akti_tunic` body with all nine distinct engine
frames. Terracotta headband, beard, blue sash and linen kilt remain on the
Sailor; the restrained shoulder rope agrees with his existing battle portrait.
Hydna retains her wet shoulder-length hair, blue wrap, bare feet and sponge
bag. The folk palette, anchors and animation order are unchanged. Rebuild only
these sheets with `python3 tools/ichor/art/sprites_folk.py sailor diver --write`.
All 22 folk arrays reproduce; the other 20 PNGs are unchanged. Native checks,
build and smoke pass, and `tools/ichor/tests/akti_sprites.lua` captures both
placed harbor walkers among eleven shots across nine maps. Complete colored
native comparisons and matching post-Elaia ROM captures are review evidence,
not artistic approval. This harbor checkpoint is now artistically accepted;
at that point, eight remaining Akti walkers still awaited polish.

**Asclepeion/Agora checkpoint:** `healer` has an eight-row head, longer folded
chiton and a thin brown rod with a two-tone green serpent. Her tenth frame
keeps the rod planted while her head dips, eyes close and hand rises over her
heart. `kid_f` keeps the child-sized height, saffron tunic, short pigtails and
terracotta ties with a smaller native head and complete strides. Both sheets
retain their folk palette and all nine walking states. The sheet preview now
uses the actual frame count, so the healer's bow is not omitted. All 22 sources
reproduce, the other 20 PNGs are unchanged from the preceding checkpoint, and
the two real heal paths hold the bow for exactly 32 frames before returning
control. Build, smoke and the scoped gallery pass. Six local walkers still
await polish; these two new sheets await artistic approval.

- **Source:** `tools/ichor/art/sprites_folk.py`. Every head, body and prop is ASCII art in that file, one character per pixel.
- **Rebuild the PNGs and the folk palette:** `python3 tools/ichor/art/sprites_folk.py --write`
- **Preview:** `python3 tools/ichor/art/sprites_folk.py --preview DIR` writes the 4× sheet; `--grids DIR` writes 8× pixel grids for editing.
- **Native regressions:** `python3 -m unittest discover -s tools/ichor/tests -p test_folk_sprites.py` checks reproduction, complete Akti states, the planted bow rod and the full tenth-frame preview.

Previews:
- `img/sprites_folk_sheets.png`: every frame of every walker at 4×, labelled with its sheet and palette. Each column starts with vanilla Birch for scale.
- `img/sprites_folk_ingame.png`: the in-game check at 3×. The top row shows the first test batch (twelve walkers, including Kleon) facing down, left, up and right. The bottom row shows the second batch (including Alethea).

## Catalog

All sheets are in `graphics/object_events/pics/people/ichor/`. The names match the aliases the map agents placed, so no map changes.

| Constant | Sheet | Palette | Look | Suggested for (SCRIPT.md Part 2) |
|---|---|---|---|---|
| `OBJ_EVENT_GFX_ICHOR_MOM` | `mom.png` | folk | Dark hair up in a bun tied with a honey-gold ribbon, a terracotta peplos, a linen apron | Melitta |
| `OBJ_EVENT_GFX_ICHOR_PRIESTESS` | `priestess.png` | folk | A saffron veil with a terracotta border over gray hair, falling in folds to a terracotta hem behind; a white peplos with a saffron girdle; a drop spindle hanging from her left hand, seen from front and back | Halia |
| `OBJ_EVENT_GFX_ICHOR_YOUTH_M` | `youth_m.png` | folk | The festival's olive wreath, its leaves sprigging out past his brown hair and tied behind with terracotta ribbons; a short linen chiton | Philon, the youth on the wall |
| `OBJ_EVENT_GFX_ICHOR_YOUTH_F` | `youth_f.png` | folk | A sky-blue chiton to mid-calf with a linen girdle, a long braid tied with a terracotta ribbon | Korinna |
| `OBJ_EVENT_GFX_ICHOR_MAN` | `man.png` | folk | Short dark hair and a full beard, an ochre exomis off the right shoulder, sandals | festival-goer, pilgrim, customer |
| `OBJ_EVENT_GFX_ICHOR_WOMAN` | `woman.png` | folk | A linen kerchief over brown hair, a blue peplos, an ochre himation over her left shoulder | festival-goer, fishwife, carter, woman by the Pithos |
| `OBJ_EVENT_GFX_ICHOR_ELDER_M` | `elder_m.png` | folk | Bald with a white fringe and a long white beard, an olive-wool himation to mid-calf, a walking staff in his right hand | olive farmers, old shepherd, Gylippos, old man by the statue |
| `OBJ_EVENT_GFX_ICHOR_ELDER_F` | `elder_f.png` | folk | A dark wool himation pushed back off parted gray hair, a kind face with smiling eyes and rosy cheeks, the himation wrapped round her with her hands folded. From behind: a gray bun under the hood's edge, the himation as a shawl, a linen chiton below | Kydippe, the old woman on the temple steps |
| `OBJ_EVENT_GFX_ICHOR_KID_M` | `kid_m.png` | folk | A mop of dark hair, a short terracotta tunic, barefoot. Child-sized: 16 rows tall. | kids, Glaukos's grandson |
| `OBJ_EVENT_GFX_ICHOR_KID_F` | `kid_f.png` | folk | Two short pigtails tied with terracotta, a short saffron tunic, barefoot. Child-sized. | kids, the customer girl |
| `OBJ_EVENT_GFX_ICHOR_FISHER` | `fisher.png` | folk | A brown felt pilos, a gray beard, a faded sea-blue tunic with a rope belt, a net over the shoulder | Diktys, Glaukos, the fisher with the bandaged hand |
| `OBJ_EVENT_GFX_ICHOR_SAILOR` | `sailor.png` | folk | Tousled hair under a terracotta headband with tails, a short jaw beard, bare-chested above an undyed linen kilt with a blue sash, a shoulder rope | the Lakonian rower, Nausikles |
| `OBJ_EVENT_GFX_ICHOR_DIVER` | `diver.png` | folk | Wet black hair to the shoulders with a blue sheen, a short sea-blue wrap tied with linen, barefoot, a net bag of sponges at her hip | Hydna |
| `OBJ_EVENT_GFX_ICHOR_HEALER` | `healer.png` | folk | Long brown hair to her shoulders under an olive-green fillet, a white chiton to the floor with a green sash, a gold serpent armlet, and the rod of Asclepius (a green serpent coiled on a staff) in her right hand | the Asclepeion healer |
| `OBJ_EVENT_GFX_ICHOR_MERCHANT` | `merchant.png` | folk | Balding, with a brown beard, a blue chiton with a leather belt, a linen apron, a coin purse | Demeas |
| `OBJ_EVENT_GFX_ICHOR_SHEPHERD` | `shepherd.png` | cast | A bronze felt pilos, a sheepskin mantle over a blue tunic, a crook in his right hand | Tityros |
| `OBJ_EVENT_GFX_ICHOR_HARVESTER` | `harvester.png` | folk | A terracotta headscarf knotted at the side, an olive-green dress, a linen apron, a wicker basket of olives on her left hip | Phyllis |
| `OBJ_EVENT_GFX_ICHOR_GOATHERD` | `goatherd.png` | folk | Wild graying curls and beard, a syrinx at his lips, a shaggy goat-hair cloak over an undyed tunic, a bronze bell on a rope belt, leg thongs | Komatas |
| `OBJ_EVENT_GFX_ICHOR_HOPLITE` | `hoplite.png` | cast | A Corinthian helmet pushed up with a crimson crest, a linen corselet over a crimson chiton, bronze greaves, a spear, a crimson hoplon with a bronze rim and the Lakonian lambda | Agis |
| `OBJ_EVENT_GFX_ICHOR_AUGUR` | `augur.png` | cast | White hair and beard, a gold fillet with a black crow feather, an indigo robe under a slate himation, a hem frieze of black birds on terracotta, a staff | Polyeidos |
| `OBJ_EVENT_GFX_ICHOR_ACOLYTE_M` | `acolyte_m.png` | cast | Close-cropped black hair, a smear of hearth soot across his cheek, a white chiton under a broad saffron himation that wraps his waist, a saffron hem, and bronze tongs holding a glowing coal at his side | Lampon, Euboulos |
| `OBJ_EVENT_GFX_ICHOR_ACOLYTE_F` | `acolyte_f.png` | cast | Auburn hair in a bun tied with saffron, a white peplos with a saffron girdle and hem, a clay oil lamp held up beside her head | Pyrrha, Aithra |

The class walkers take their clothes, colours and props from their portraits. Where the 16×32 frame forced a cut, the prop stayed and the pose went. The Shepherd doesn't wave, the Augur doesn't point at the sky, and Acolyte F's fist-on-hip is dropped.

## Palette plan

Every walker uses one of two palette tags, so a map needs at most **two Ichor OBJ palette slots**, however many of these walkers it shows:

| Tag | Palette | Walkers |
|---|---|---|
| `OBJ_EVENT_PAL_TAG_ICHOR_FOLK` (0x1135) | new `graphics/object_events/palettes/ichor_folk.pal` | the 15 townsfolk, the Harvester and the Goatherd |
| `OBJ_EVENT_PAL_TAG_ICHOR_CAST` (0x1134) | the existing `ichor_cast.pal` (`SPRITES_npc.md`), unchanged | the cast, the Shepherd, the Hoplite, the Augur and both Acolytes |

**Why the split.**
- **The cast palette:** five class portraits use the cast's fairer skin and its crimson, bronze, linen and blue. The Hoplite in particular "shares Kleon's crimson and bronze". So those five fit the cast palette without a new tag.
- **The folk palette:** the Harvester and the Goatherd are sun-browned in their portraits, and need olive, gray and wicker, which only the folk palette has.
- **One rule:** a walker never mixes palettes.
- **A dependency:** the five class sheets embed the cast palette, so changing `CAST_COLORS` means re-running both `sprites_npc.py --write` and `sprites_folk.py --write`.

**How the engine allocates.** Overworld palettes load by tag into any free slot of the 16 OBJ palettes (`LoadObjectEventPalette`, then `LoadSpritePalette`).
- Every sprite with the same tag shares one slot.
- A water reflection adds one filtered copy per tag, not per sprite (`LoadObjectRegularReflectionPalette`).
- When the slots run out in the overworld, the engine evicts generated wild overworld encounters first.

**Measured in game.** Twelve different walkers stood in one room with the player, from both palettes. The live `sSpritePaletteTags` read:

```
1200 1100 1135 1134 FFFF FFFF FFFF FFFF FFFF FFFF FFFF FFFF FFFF FFFF FFFF FFFF
```

That is the weather tag, the player, folk and cast: **4 of 16 slots, 12 free.**

| Map | Expected slots |
|---|---|
| The busiest map, Elaia's festival square | about 9: those 4, plus the follower Pokémon, the Wooloo object, the emote, and one or two field-effect palettes |
| Akti, the harbor | about 12: up to three more for reflections (player, folk, cast) |

Every slice map fits, with room for a third Ichor family later.

### The folk palette

**Palette file:** `graphics/object_events/palettes/ichor_folk.pal`, loaded as `gObjectEventPal_IchorFolk`. Its order is fixed and every folk PNG embeds it, so to change a colour, edit `FOLK_COLORS` and re-run `--write`. Its letters follow the cast palette's wherever the role matches.

| # | Char | Name | RGB | Used for |
|---|---|---|---|---|
| 0 | `.` | transparent | 112 192 160 | Never drawn |
| 1 | `k` | ink | 32 24 24 | Outlines, eyes, Hydna's wet hair |
| 2 | `b` | brown | 88 48 32 | Hair, sandals, leather, terracotta shadow, Kydippe's himation |
| 3 | `u` | terra | 184 72 48 | Mom's peplos, the boy's tunic, headscarves, ribbons, the veil border |
| 4 | `o` | ochre | 200 144 40 | Halia's veil, the man's exomis, the woman's himation, wicker |
| 5 | `O` | gold | 240 192 64 | Honey ribbon, girl's tunic, sponges, the bell, the armlet |
| 6 | `s` | skin_d | 192 120 72 | Sun-browned skin shadow (the Harvester and Goatherd portraits' ramp) |
| 7 | `S` | skin_l | 232 176 120 | Sun-browned skin |
| 8 | `l` | linen_d | 200 184 152 | Linen and wool shadow, net twine, the goatherd's tunic |
| 9 | `L` | linen_l | 248 240 216 | Linen, aprons, white hair and beards, kerchief |
| 10 | `y` | gray | 152 144 136 | Gray hair and beards, goat hair, net knots |
| 11 | `n` | blue_d | 24 56 120 | Aegean-blue shadow, sash, wet-hair sheen |
| 12 | `B` | blue | 48 104 176 | The woman's peplos, the merchant's chiton |
| 13 | `a` | sky | 112 168 224 | Korinna's chiton, the fisher's and Hydna's sea-blue |
| 14 | `v` | olive_d | 64 80 32 | Olive shadow, olives |
| 15 | `g` | olive | 120 136 56 | The elder's himation, the harvester's dress, the wreath, the healer's sash |

## How a walker is built

- **Layout:** each sheet uses the cast layout: 144×32, with nine 16×32 frames.

  | Frame | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
  |---|---|---|---|---|---|---|---|---|---|
  | Pose | face down | face up | face left | walk down A | walk down B | walk up A | walk up B | walk left A | walk left B |

- **The Healer's tenth frame:** her sheet is 160×32. Frame 9 is the bow (see "Special animations" below).
- **Feet and step bob:** feet stand on row 30. Walk frames drop 1 px, so the stepping foot lands on row 31.
- **Right-facing frames:** these are the left frames mirrored in game.
- **Body archetypes** (`TUNIC`, `MIDI`, `ROBE`, `KID`) draw the torso, arms and legs for all nine frames once, in role letters: `C` cloth, `Q` cloth shade, `T` belt, `F` feet, `X`/`Y` shins. A walker maps the roles to its palette. For example, the Hoplite maps the shins to bronze greaves, and the children map `F` to bare skin.
- **Walk cycles:**
  - Front and back walks lift one leg and swing that side's hand back.
  - Side walks stride with the near leg and then the far leg forward, and the near arm swings against the step.
- **Heads:** each walker draws its own head per direction, the same height in all three.
  - Walkers with a tall prop (the Shepherd's crook, the Hoplite's spear) start with three blank rows, so the prop clears the head.
  - Children's heads are 9 rows tall, over a 7-row body.
- **Overlays** paint costume and props over the composed figure, per direction and pose: `all`, `stand`, `walk`, `walk0` or `walk1`. `_` keeps the pixel underneath. `pole()` places staffs, spears, crooks and baskets.
- **Props held still:** walkers that hold a prop keep that hand still in the walk frame that would swing it away.

The registration follows `SPRITES_npc.md` step 3, inside the Ichor blocks of the five object-event tables. The new palette also has its own tag and entries in `object_event_graphics.h` and `sObjectEventSpritePalettes`.

## Notes for map placement

- **Mirrored props.** Right-facing frames are mirrored, so props held in one hand swap sides facing right. This affects the staffs, the crook, the spear, the shield, the basket, Halia's spindle and the lamp. Facing down or left shows them as drawn.
- **Halia** reads best facing **down**: the face, gray hair, veil border and spindle all show. From behind she is a plain saffron veil.
- **The Healer and the Merchant** are drawn for counters and stalls: face them **down**. The apron, purse, armlet and sash all show from the front.
- **Kydippe** reads best facing **down or left**, where her smile shows.
- **The Hoplite** is at his most Lakonian facing **left or right**: the side view is all shield, crimson with the lambda. Facing down, the shield is on his left arm and the spear in his right.
- **The Goatherd's syrinx** shows only facing down and sideways. From behind, his shaggy cloak is the read.
- **The Fisher's net** reads best from behind or the side, as a bundle on his back. From the front it is a mesh sash across the chest.
- **Hydna's sponge bag** hangs at her left hip and shows in every direction.
- **Children** are shorter by design, about the vanilla little boy's height. Face them down and they read as kids at a glance.
- **Shepherdess.** The Shepherd walker is male, after Tityros's portrait. For Amaryllis the shepherdess, `WOMAN` or `YOUTH_F` is the closer fit.
- **Wandering.** Every walker wanders and walks normally. The staff carriers (Elder M, the Healer, the Shepherd, the Augur) look best with `MOVEMENT_TYPE_FACE_*` or a short wander, since their staff hand doesn't swing.

## Special animations

A walker's anim table has to cover every movement a script gives it. `waitmovement` waits for the animation to end, so an anim the table lacks never ends, and the player is stuck.

- **The Healer bows.**
  - Both Asclepeion heals end with `Movement_PkmnCenterNurse_Bow`: talking to her (`Ichor_EventScript_AsclepeionHealer`) and the whiteout respawn (`EventScript_AfterWhiteOutHeal`).
  - That movement plays `ANIM_NURSE_BOW`, which only `sAnimTable_Nurse` has. It shows frame 9 for 32 ticks.
  - So the Healer uses `sAnimTable_Nurse`, and `sPicTable_IchorHealer` lists ten frames.
  - **The bow:**
    - The top of her head drops 1 px and her fillet 2 px.
    - Her eyes close and her neck is hidden.
    - Her left hand comes up over her heart, and the rod stays planted.
  - Behind the Asclepeion counter only the head shows, so the bow reads as the head dipping and the eyes closing.
  - Preview: `img/healer_bow.png` shows the stand and bow frames at 6×, then the talk-heal in game: restored, bow, bow, "Go in health."
- **Everyone else uses `sAnimTable_Standard`.** Checked against every slice script (Elaia, Akti and its interiors, Route 1, Kronion Hill) and the shared scripts they call. They use only these:
  - walks, at normal, fast and slow speed
  - faces, and the walk-in-place turns of the heal script
  - `jump_in_place_down`
  - emotes, which are field effects and not anims
  - The Agora merchant runs the plain `pokemart` flow, which has no movements.
  - Mom isn't placed on any map yet. The whiteout heal at home only walks her in place.
- **Moves that need a special table:**
  - `nurse_joy_bow` needs `sAnimTable_Nurse`.
  - `jump_special_*` and `spin_*` read `ANIM_GET_ON_OFF_POKEMON_*` and `ANIM_SPIN_*`, which `sAnimTable_Standard` doesn't have.
  - `rock_smash_break` and `cut_tree` play `ANIM_REMOVE_OBSTACLE`.
  - None of them is used on an Ichor walker today. A script that adds one needs the matching table.
- **Regression test:** `tools/ichor/tests/asclepeion_bow.lua`. It runs both heals and checks that the bow is held for 32 frames and that the player can walk away afterwards. With the healer back on `sAnimTable_Standard`, the walk-away checks fail in both paths.

## In-game check

The check runs in the Quickstart bedroom. Twelve walkers stand facing down, a Lua script turns them through all four directions while they walk in place, and the screenshots are cropped together.

1. **Place the walkers.** Temporarily set `data/maps/ElaiaVillage_PlayersHouse_2F/map.json`'s `object_events` to up to twelve walkers.
   - Give them `MOVEMENT_TYPE_WALK_IN_PLACE_DOWN`, elevation 3.
   - Put nine in row 6 (x 0–8) and the rest in row 4.
   - The room holds 16 object events, including the player and follower.
2. **Build.**
3. **Run the check.** Walk-in-place re-reads `ObjectEvent.facingDirection` every step, so a Lua frame callback can turn the walkers. The check:
   - Quickstarts at the smoke test's frames: START at 500, SELECT at 1020.
   - From frame 2400 writes `facingDirection` and `movementDirection` (offset 0x18 of each `gObjectEvents[i]`, 0x24 bytes apart) to 1, 3, 2 and 4: down, left, up, right. Each phase lasts 100 frames.
   - Screenshots every 2 frames.
   - Logs `sSpritePaletteTags`: 16 u16s at the address `arm-none-eabi-nm pokeemerald.elf | grep sSpritePaletteTags` gives, 0x03001830 in this build.
4. **Revert the map:** `git checkout -- data/maps/ElaiaVillage_PlayersHouse_2F/map.json`.
5. **Rebuild, then run `tools/ichor/smoke_test.sh`.**

## Still open

- **Two tones per material.** As with the cast, materials have two tones plus the outline. The folk palette is full, so mid-tones would need a third family.
- **Not opened in Porymap yet.** The entries follow the vanilla format and the cast entries, so they should display.
