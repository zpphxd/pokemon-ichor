# Phase 2, batch 1: the people of the voyage and Aegina

Trainer portraits, trainer classes and overworld walkers for the *Euploia* and Aegina (BUILD.md batch 1). They are drawn in the slice's house style (`design/phase1/SPRITES*.md`), and the slice's palettes take every walker, so no new OBJ palette tag is needed.

**Current shared-class source override:** Merchant, Pilgrim and Ichor Sailor
fronts, plus the shared Merchant/Sailor/Pilgrim walkers, now come from the
authored native exports in `tools/ichor/art/sources/human_classes/`.
Reproduce the exact 32-asset class/townsfolk union with
`python3 tools/ichor/art/human_classes.py --write`, not an unfiltered legacy
phase-2 writer. Their indexed sources derive from image-model outputs and
native conversion, not new procedural shape recipes. Shared palettes,
graphics IDs, trainer bindings and all named-cast assets remain unchanged.
See `design/phase1/SPRITES_folk.md` for complete motion, provenance, engine
checks and acceptance scope. The older writer table below remains applicable
to its other profiles, not these authored overrides.

| Source | Rebuild | Preview |
|---|---|---|
| `tools/ichor/art/sprites_phase2_classes.py` (portraits) | `python3 tools/ichor/art/sprites_phase2_classes.py --write` | `--preview DIR`: the 3× contact sheet, a 6× row, 6× singles and pixel grids |
| `tools/ichor/art/sprites_phase2_walkers.py` (walkers) | `python3 tools/ichor/art/sprites_phase2_walkers.py --write` | `--preview DIR` for the 4× sheet; `--grids DIR` for 8× pixel grids |

`--write` with no name also rewrites the contact sheets in `img/`.

## Sacred Way portrait replacements, 2026-11-16

The existing Potter Exekias, Initiate Myrrhine and Runner Pheidippos now have
separate Greek portraits rather than Hiker, Psychic F and Running Triathlete M
placeholders. Their classes, parties, levels, dialogue and battle behavior are
unchanged. The three original Hoenn PNGs remain byte-identical.

| `Pic:` | Look | File |
|---|---|---|
| `Potter` | Bearded craftsman in linen and a clay-colored apron, raising his brush while holding a black-figure amphora | `graphics/trainers/front_pics/potter.png` |
| `Initiate F` | Myrtle-wreathed young woman in ivory and indigo, holding a scroll and gesturing excitedly | `graphics/trainers/front_pics/initiate_f.png` |
| `Runner` | Red-headbanded messenger in a short ochre chiton and red cloak, running with a tied message roll | `graphics/trainers/front_pics/runner.png` |

These are reference-guided image-model outputs using the approved Theo
direction, **not hand-authored native drawings**. The immutable 1536x1024 source
is `design/art/characters/route4/generated.png`; each production picture is an
actual indexed 64x64 export with transparent index 0 and at most 15 opaque
colors at GBA precision. Nearest-neighbor sampling retains the silhouette but
loses small facial and vase-painting detail.

`python3 tools/ichor/art/export_route4_characters.py --output DIR` reproduces
the native PNGs in `DIR/native`, a comparison board and a verification manifest.
It segments the source's existing alpha channel and does no anatomy drawing.
Tiny red/green accents receive extra palette weight only below 3% coverage:
weighting whole red/brown garments erased the Potter's linen in the rejected
first conversion. This exporter never writes production paths implicitly.
The older class painters do not own these three source-backed assets.

## For party files

| Trainer | `Class:` | `Pic:` |
|---|---|---|
| Alethea (`TRAINER_ICHOR_ALETHEA_DECK`) | `Scholar` | `Alethea` |
| Lykon, Sostratos | `Merchant` | `Merchant` |
| Euthymia | `Pilgrim` | `Pilgrim` |
| Phormion and every Ichor sailor | `Sailor` (the vanilla class, unchanged) | **`Ichor Sailor`** |

`design/phase2/trainers_batch1.party` still says `Pic: Sailor` for Phormion. Change it to `Pic: Ichor Sailor` when the parties move to `src/data/trainers.party`; `Pic: Sailor` is Hoenn's sailor, which stays untouched.

## Trainer pics

Each is a 64×64, 16-color front pic. The palette is embedded in the PNG, except Alethea's (below).

| Constant | `Pic:` | Look | File |
|---|---|---|---|
| `TRAINER_PIC_ALETHEA` | `Alethea` | Her walker and back pic from the front: a blue headband over a dark fringe, a ponytail swinging behind her left shoulder, a sun-gold chiton to the knee, bloused over a leather girdle and dusty at the hem. A satchel of scrolls sits on her left hip, its strap across her chest, and she holds a trowel up like a find. Eyes wide, grinning. | `graphics/trainers/front_pics/alethea.png` |
| `TRAINER_PIC_MERCHANT` | `Merchant` | A portly trader, balding, with a full brown beard and a pleased smile. A dyed Aegean-blue himation with a gold stripe is wrapped round his belly over a linen chiton. A fat purse hangs at his hip, and he holds a bronze balance out from his fist, the near pan dipping under two coins. The walker is the slice's merchant. | `graphics/trainers/front_pics/merchant.png` |
| `TRAINER_PIC_PILGRIM` | `Pilgrim` | A woman in a midnight-blue hooded cloak, open over a white chiton with a saffron cord. She has a staff in her far hand and, in the near one, Hecate's supper: a terracotta bowl under a linen cloth knotted with saffron. A wry smile. | `graphics/trainers/front_pics/pilgrim.png` |
| `TRAINER_PIC_ICHOR_SAILOR` | `Ichor Sailor` | A bare-chested oarsman, his tousled hair under a terracotta headband with tails, a short jaw beard and a grin. His undyed linen chiton is rolled down to a kilt with a blue sash, and a coil of rope runs over his far shoulder and across his chest, his thumb hooked under it. The walker is the slice's sailor. | `graphics/trainers/front_pics/ichor_sailor.png` |

- **Alethea's palette:** her front pic is drawn on her back pic's palette (`sprites_alethea_back.PAL`), and the entry points the front pic at `gTrainerBackPicPalette_Alethea`. Change her colors in `sprites_alethea_back.py` and rerun both scripts.
- **Her back pic:** unchanged. It still leads the catch tutorial.

Contact sheet: `img/sprites_classes.png`, at 3× on the grass battle background. The top row is the slice's Kleon, Daphne, Shepherd, Harvester and Hoplite for scale; the new four are below.

## Trainer classes

| Constant | `Class:` | Shown as | Money | Who |
|---|---|---|---|---|
| `TRAINER_CLASS_SCHOLAR` | `Scholar` | SCHOLAR | 8 | Alethea alone (SCRIPT.md open question 6) |
| `TRAINER_CLASS_MERCHANT` | `Merchant` | MERCHANT | 20 | traders on the road and aboard |
| `TRAINER_CLASS_PILGRIM` | `Pilgrim` | PILGRIM | 3 | devotees on the roads |

- **Money:** the money values are my guesses (merchants pay like gentlemen, pilgrims are poor). Adjust them with BALANCE.md if it sets payouts.
- **Balls:** all three throw the default ball.
- **Sailors:** they keep the vanilla `TRAINER_CLASS_SAILOR` (SAILOR, 8).

## Walkers

Every sheet is 144×32: nine 16×32 frames in the slice's layout, with feet on row 30 and the 1 px step bob. Every sheet uses `sAnimTable_Standard`.

| Constant | Sheet | Palette | Look | Made from |
|---|---|---|---|---|
| `OBJ_EVENT_GFX_ICHOR_PILGRIM` | `pilgrim.png` | folk | A midnight-blue hooded cloak over a white chiton with a saffron cord. A staff in her right hand, the covered dish (linen over terracotta, a saffron knot) held at her waist. From behind she's all cloak, with the staff showing. | new, on the slice's midi body; the hood frames the face as the priestess's veil does |
| `OBJ_EVENT_GFX_ICHOR_PRONOMOS` | `pronomos.png` | folk | The sailor with dark curls and no headband. The aulos slants from his lips to his left hip, one hand high on it and one low, and his hands stay on it when he walks. His sash is terracotta, not the rowers' blue. | the slice's sailor |
| `OBJ_EVENT_GFX_ICHOR_ENDEIS` | `endeis.png` | folk | Dark hair streaked gray under a terracotta kerchief, an ochre peplos, a linen apron, and a terracotta wine jug in her right hand. | the island woman, with Melitta's apron |
| `OBJ_EVENT_GFX_ICHOR_PHEIDON` | `pheidon.png` | folk | Dark curls going gray at the temples, a short beard, an undyed exomis under a terracotta leather apron, and the striking hammer in his right hand. | new, on the slice's tunic body |
| `OBJ_EVENT_GFX_ICHOR_AIAKIDES` | `aiakides.png` | folk | Close-cropped white hair, a short white beard and stern brows. A white chiton with a black belt (the one he gives away), a faded terracotta soldier's cloak, and a stick. | the old man's staff, on a soldier's tunic body |
| `OBJ_EVENT_GFX_ICHOR_KEDALION` | `kedalion.png` | folk | Batch 2, Emporion's Hephaisteion. A broad smith, bald on top with a black fringe and a great black beard, soot on his brow, a sooty gray exomis under a black leather apron, and his tongs. | Pheidon's tunic body, with his own head, apron and tongs; the bald dome and the black beard keep him apart from Pheidon and the slice's merchant |
| `OBJ_EVENT_GFX_ICHOR_KLEON_SEASICK` | `kleon_seasick.png` | cast | Kleon at the rail (see below) | Kleon |
| `OBJ_EVENT_GFX_ICHOR_KLEON_TABLET` | `kleon_tablet.png` | cast | Kleon reading his mother's wax tablet (see below) | Kleon |

### Existing walkers that already fit

- **Lookout and rowers:** use `OBJ_EVENT_GFX_ICHOR_SAILOR` as it is (SCRIPT.md Part 10, "Reuse the sailor").
- **Merchant trainers (Lykon, Sostratos):** use `OBJ_EVENT_GFX_ICHOR_MERCHANT`, the class walker.
- **Pheidon:** the merchant walker came close (balding, beard, apron, purse). It belongs to the Merchant class, though, and a moneyer at the anvil needed the leather apron and hammer, so he got his own sheet.
- **Aiakides:** `OBJ_EVENT_GFX_ICHOR_ELDER_M` reads as "old man" but not "soldier", hence the cloak, the stick and the belt.
- **Endeis:** `OBJ_EVENT_GFX_ICHOR_MOM` would have fit, but Melitta is the player's mother and shouldn't turn up keeping an inn.

### Facing and placement

- **Props in the right hand:** these swap sides facing right, as on every Gen 3 NPC. That covers Pronomos's pipes, Endeis's jug, Pheidon's hammer, the pilgrim's staff and Aiakides's stick.
- **Endeis and Pheidon:** stand them facing down behind a counter or anvil. The apron, jug and hammer all show from the front.
- **Pronomos:** reads best facing down or sideways. From behind he is a bare back and curls.
- **The pilgrim's dish:** shows facing down and sideways. From behind she's a hooded cloak with her staff.
- **Staff and stick carriers:** the pilgrim and Aiakides hold still on that side when they walk, as the slice's staff carriers do.

### Palette budget on the batch 1 maps

| Map | Ichor tags | Why |
|---|---|---|
| The deck | 2: cast and folk | Kleon and his poses and Alethea are cast; Pronomos, Nausikles (the sailor) and the merchants are folk |
| Aegina Town, its homes, the detour | folk (plus cast if Kleon or Alethea is on the quay) | Endeis, Pheidon, Aiakides and the pilgrim are folk |

## Kleon's poses

There are two sheets, each with nine frames in the standard layout. The facing chooses the pose's direction (right is left mirrored), and walking in place loops stand → frame A → stand → frame B. Neither sheet needs a special anim table or a new movement action.

| `OBJ_EVENT_GFX_ICHOR_KLEON_SEASICK` | What it shows |
|---|---|
| face up | From behind: leaning over a rail to the north, elbows out, his head hung between his shoulders |
| face left / right | Bent double over a rail at his side, head and hands over it |
| face down | Hunched toward the viewer, gray-green in the face, eyes screwed shut, both hands clutching his stomach |
| walking in place (any direction) | The heave: he sags a pixel lower and gulps. Facing down, one hand comes up over his mouth. |

| `OBJ_EVENT_GFX_ICHOR_KLEON_TABLET` | What it shows |
|---|---|
| face down | A small wax diptych open at his chest in both hands, head bowed to read |
| face left / right | The tablet held up in front of him, head bowed |
| face up | His back, with his hands in front of him |
| walking | He walks while he reads: the legs step, and the tablet stays put |

**The sitting pose** (on steps with his greaves off, SCRIPT.md Part 10) is for a later batch, at the Telesterion. It isn't drawn yet.

### How a script shows them

**1. A whole scene in one pose.** In `map.json`, give that Kleon object the pose's graphics id directly. Give it `MOVEMENT_TYPE_FACE_UP`, `_LEFT`, `_RIGHT` or `_DOWN`, pointing toward the rail. To make him heave, use:

```
movement Euploia_Movement_KleonHeave { walk_in_place_slow_up * 3 }   // _left/_right/_down to match his facing

applymovement(LOCALID_EUPLOIA_KLEON, Euploia_Movement_KleonHeave)
waitmovement(LOCALID_EUPLOIA_KLEON)
```

Talking to him with `faceplayer` turns him toward the player in the same pose. Facing down, he's clutching his stomach. Leave `faceplayer` out if he should stay bent over the rail while he talks ("Hrk.").

**2. Switching pose mid-scene.** This covers "Kleon pushes himself off the rail and walks to the hatch" and the night leg's tablet. Give the object `"graphics_id": "OBJ_EVENT_GFX_VAR_0"` (use any `VAR_OBJ_GFX_ID_n` the map doesn't already use), and set the var in `MAP_SCRIPT_ON_TRANSITION`, before objects spawn:

```
setvar(VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_ICHOR_KLEON_SEASICK)   // or _KLEON / _KLEON_TABLET by the scene's flags
```

To swap him where he stands:

```
copyobjectxytoperm(LOCALID_EUPLOIA_KLEON)                  // respawn here, not at his map.json tile
setvar(VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_ICHOR_KLEON)
removeobject(LOCALID_EUPLOIA_KLEON)
addobject(LOCALID_EUPLOIA_KLEON)
clearflag(FLAG_...)                                        // only if his object has a hide flag: removeobject sets it
applymovement(LOCALID_EUPLOIA_KLEON, Euploia_Movement_KleonToHatch)
```

**What the swap does in game:**
- **No `copyobjectxytoperm`:** the swap respawns him on his `map.json` tile, a visible jump.
- **After the swap:** he faces whatever his movement type says. Turn him with a `face_*` move if that matters.
- **A note on `addobject`:** it spawns from the template without checking the hide flag.
- **The engine side:** the graphics var is resolved at spawn (`event_object_movement.c`), which is why remove-then-add works.

**3. Two objects instead.** One object per look, on the same tile, each with its own hide flag, swapped with `removeobject` and `addobject`. This is the classic vanilla way. Use it if the map has no graphics var free.

Recipe 2 was run in game. On Akti's quay, Kleon starts seasick through `OBJ_EVENT_GFX_VAR_0`, heaves three times, swaps to his walker and walks off two tiles. He then swaps in place (with `copyobjectxytoperm`) to the tablet and walks back two tiles reading. The object's logged graphics id and position matched at every step. Strip: `img/sprites_kleon_poses_ingame.png`.

## In-game checks

The brief rules out editing maps and parties, and the permission system refused a temporary party edit. So both checks patch the emulator's in-memory copy of the ROM from a Lua script (mGBA's `emu.memory.cart0`), and no repo file changes.

- **Walkers:** `img/sprites_walkers_ingame.png`, from Akti Town at 3×.
  - Fourteen of Akti's object templates were repointed at the seven new walkers.
  - The top row walks in place, turned down, left, up and right.
  - The bottom row stands and rotates clockwise.
  - Every frame draws, in the right palette, beside the slice's townsfolk.
- **Portraits:** `img/sprites_classes_ingame.png`, at 2×.
  - Four slice trainers took the new class, pic and name for the run.
  - A test-only event script in spare EWRAM (the `route1.sh` technique) battled each one.
  - The intros read "You are challenged by SCHOLAR ALETHEA!", "MERCHANT LYKON", "PILGRIM EUTHYMIA" and "SAILOR PHORMION", each with its portrait on the platform. All four class names fit the box.
- **Kleon's poses:** recipe 2 above.

`make` is green and `tools/ichor/smoke_test.sh` passes. The ROM is 25,677,912 B (76.53%), 19,136 B more than before this batch.

## Critique passes

**Portraits**

1. **First draft.**
   - Every face read sleepy: the half-lid eye of the slice's classes looked drowsy without a hat or scarf over it.
   - Alethea's red mouth read as lipstick, and her trowel as a feather.
   - The merchant's belly was a white egg.
   - The pilgrim's lidded dish read as a burger.
   - The sailor's rope was an empty ring.
2. **Redraw.**
   - Brows went in, and the eyes now run two rows with a catchlight, as on the cast.
   - Alethea got a small open grin and a flat-bladed trowel.
   - The merchant's himation now wraps the belly, with its edge running from hip to shoulder.
   - The sailor's rope runs as a coil across his chest from his far shoulder, the loops showing behind it.
3. **Fixes.**
   - Alethea's trowel was floating above her fist, so it went into her hand, and her satchel got smaller.
   - The merchant's arm was lost behind the balance cords, so it reaches out further and the balance hangs clear of it.
   - The pilgrim's dish still read as a burger, so it became a cloth-covered bowl.

**Walkers**

1. **First draft.**
   - Pronomos's pipes made a gold V that read as a harness, and his strap read as a beard.
   - Pheidon was a brown blob, and his hammer didn't show.
   - Endeis's jug sat at her feet.
   - Seasick Kleon crouched facing down and cheered facing up (arms high).
   - The tablet read as a box at his belly.
2. **Redraw.**
   - Pronomos's pipes slant from his lips to his hip, with his hands on them.
   - Pheidon's apron is terracotta and his hammer has a pale head.
   - Endeis's jug is up in her hand.
   - Seasick Kleon facing down hunches green with his hands on his stomach (the heave brings a hand to his mouth), and from behind his elbows are out over the rail.
   - The tablet sits at his chest.
3. **Matching the portrait.** The pilgrim's dish now matches the portrait's cloth and knot. Checked in game.

## Original batch 1 open-items ledger

This is the historical batch 1 ledger, not the current completion matrix;
see `design/art/INVENTORY.md`. In particular, the three active Sacred Way
portrait fallbacks are now replaced as described above.

- **Phase 2's other classes:** Potter, Runner, Initiate, Jester, Beekeeper, Swineherd and the Titan Admin were not drawn at this checkpoint. Neither were Kerykos, Chloe, Hyperion, Daphne's sandals or the walkers for batch 2 and later. Eleusa's story borrowed the Goatherd pic for `TRAINER_CLASS_SWINEHERD`, the Acolyte F pic for Chloe, and pilgrims/youths for initiate walkers.
- **Kleon's back pic** is drawn (`tools/ichor/art/sprites_kleon_back.py`, his front pic's palette, Theo's throw): a battle partner slides in from behind, and he is one on the night of the Mysteries.
- **The initiate walker:** it can reuse the pilgrim's white midi chiton without the cloak.
- **Kleon's sitting pose:** it waits for the Telesterion's batch.
- **The test harness:** the runtime-patch scripts (Lua plus an assembled script blob) live outside the repo. They could become a `tools/ichor/tests/` check if the session wants one.
