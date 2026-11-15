# Act II, batch 1: sprites

Trainer portraits, trainer classes, overworld walkers, poses and field objects for beats 26–34 (the Kithairon crossing and Thyrsa). They're drawn in the slice's house style (`design/phase1/SPRITES_classes.md`, `SPRITES_npc.md`, `SPRITES_folk.md`), and every name below is the one BUILD.md fixed.

| Source | Rebuild | Preview |
|---|---|---|
| `tools/ichor/art/sprites_act2_classes.py` (portraits) | `python3 tools/ichor/art/sprites_act2_classes.py --write` | `--preview DIR`: the 3× sheet, 6× singles, pixel grids |
| `tools/ichor/art/sprites_act2.py` (walkers, poses, objects, the wine palette) | `python3 tools/ichor/art/sprites_act2.py --write` | `--preview DIR` for the 4× sheet; `--grids DIR` for 8× pixel grids |

`--write` with no name also rewrites the contact sheets:

- `img/sprites_batch1.png`: every walker, pose and object at 2×, after six of the slice's walkers (Kleon, Alethea, the Goatherd, the Harvester, Elder F, Acolyte M) for scale.
- `img/portraits_batch1.png`: the six portraits at 2× on the grass battle background, after five of the slice's.

In-game captures: `img/sprites_batch1_ingame.png` (the walkers in the Quickstart bedroom, turned down, left, up and right) and `img/portraits_batch1_ingame.png` (the six battle intros).

## For party files

| Trainers | `Class:` | `Pic:` |
|---|---|---|
| Euia, Bromia, Lenaia | `Maenad` | `Maenad` |
| Komos | `Satyr` | `Satyr` |
| Hegelochos, Mynniskos, Thettalos, Theodoros | `Actor` | `Actor` |
| Ikarios, Oinopion | `Vintner` | `Vintner` |
| Thespis | `Hierophant` (unchanged) | `Hierophant Thespis` |
| Silenos | `Satyr` | `Silenos` |

`tools/ichor/act2/fold_parties.py` can drop its stand-ins for these four classes and six pics.

## Trainer classes

| Constant | Shown as | Money | Who |
|---|---|---|---|
| `TRAINER_CLASS_MAENAD` | MAENAD | 5 | Kithairon's bacchants, Thyrsa's vineyard dancers |
| `TRAINER_CLASS_SATYR` | SATYR | 5 | the satyr play's chorus men, and Silenos |
| `TRAINER_CLASS_ACTOR` | ACTOR | 7 | Dionysus's acolytes, the city's players |
| `TRAINER_CLASS_VINTNER` | VINTNER | 6 | Thyrsa's vineyards, the Eleutherai terraces |

- **Money:** Act I's road classes pay 4–6 and its acolytes 5. Act II's trainers are a step stronger, so these pay a step more; actors and vintners own their trade. BALANCE.md sets no payouts, so adjust freely.
- **Balls:** all four throw the default ball.
- **In the box:** all four names were checked in battle ("You are challenged by MAENAD EUIA!" and the rest).

## Trainer pics

Each is a 64×64, 16-color front pic, its palette embedded in the PNG.

| Constant | `Pic:` | Look | File |
|---|---|---|---|
| `TRAINER_PIC_MAENAD` | `Maenad` | Mid-whirl: loose dark hair crowned with ivy and streaming out behind her, mouth open on the cry. A spotted fawnskin is knotted over her left shoulder, a hoof hanging, on a saffron chiton whose hem swings wide, with an ivy girdle. She's barefoot with one foot kicked back, the thyrsus (a fennel staff wound with ivy, a pine cone at its head) held high in her near hand and her far arm flung out. | `graphics/trainers/front_pics/maenad.png` |
| `TRAINER_PIC_SATYR` | `Satyr` | A comic chorus man with a pale snub-nosed satyr mask pushed up on his dark curls, goat ears and horn stubs on it. Under it, a wide toothy grin and a beard. Bare chest, shaggy goat-hair breeches down to black hooves, a tail curling up behind. A wineskin is tucked under his far arm and his near fist is up: "Euoi!" | `graphics/trainers/front_pics/satyr.png` |
| `TRAINER_PIC_ACTOR` | `Actor` | A tragic actor declaiming: dark curls under a gold fillet, a short beard, mouth open on a line, his near hand flung up to the gods in a long sleeve. A long-sleeved wine-red robe, gold collar and hem, white dots on the skirt, thick-soled tragic boots. His white tragic mask, mouth agape, hangs from his far hand. | `graphics/trainers/front_pics/actor.png` |
| `TRAINER_PIC_VINTNER` | `Vintner` | A sun-browned vineyard man in a wine-red headscarf with a short beard and a grin. An undyed exomis off his near shoulder, belted with a cord. His legs are stained purple to the knee from the treading floor, with a ragged edge and a few splashes higher up. A wicker basket heaped with black grapes (and a vine leaf) rides on his far shoulder, and his near hand holds a pruning hook up. | `graphics/trainers/front_pics/vintner.png` |
| `TRAINER_PIC_HIEROPHANT_THESPIS` | `Hierophant Thespis` | Tall and theatrical, one arm flung wide with the palm up, the other hand on his breast. A long grape-purple robe trailed with ivy, a gold band and hem, tragic boots. His face is his oldest Prosomime: a white mask split down the middle, its near half laughing and its far half weeping with a tear, violet haze in the eye holes. Gray-streaked hair and a gray beard frame it, under an ivy crown, with lilac ribbons behind. | `graphics/trainers/front_pics/hierophant_thespis.png` |
| `TRAINER_PIC_SILENOS` | `Silenos` | Bald, round and very old: pointed satyr's ears, a merry squint, a red nose, and a white beard spilling onto a great bare belly. A goatskin over his far shoulder, a linen loincloth, short legs in sandals. The wineskin he never puts down is hugged under his near arm, dribbling, and his far hand waves you over: "Sit!" | `graphics/trainers/front_pics/silenos.png` |

## Walkers

All sheets are in `graphics/object_events/pics/people/ichor/`. Each is 144×32: nine 16×32 frames in the slice's layout, with feet on row 30 and the 1 px step bob. They all use `sAnimTable_Standard`.

| Constant | Sheet | Palette | Look | Used in |
|---|---|---|---|---|
| `OBJ_EVENT_GFX_ICHOR_MAENAD` | `maenad.png` | folk | Loose dark hair crowned with ivy, falling past her shoulders. A spotted fawnskin on a saffron chiton to mid-calf, an ivy girdle, bare feet, and a tall thyrsus with a pine-cone head. | Kithairon (Euia, Bromia) |
| `OBJ_EVENT_GFX_ICHOR_MAENAD_THYRSA` | `maenad_thyrsa.png` | wine | The same maenad in the city's colors: a wine-red chiton shaded grape. | Thyrsa (Lenaia, the vineyard dancers) |
| `OBJ_EVENT_GFX_ICHOR_SATYR` | `satyr.png` | folk | The satyr mask (horn stubs, goat ears, red snub nose) pushed up on dark curls, a grin and a beard, a bare chest, goat-hair breeches to black hooves, a tail, a wineskin under his left arm. | Komos, the satyr play |
| `OBJ_EVENT_GFX_ICHOR_SILENOS` | `silenos.png` | folk | Bald, round, red-nosed, pointed ears, a long white beard over a bare belly, a goatskin over his left shoulder, a linen loincloth, the wineskin. | the parodos and the prop room |
| `OBJ_EVENT_GFX_ICHOR_MANTO` | `manto.png` | folk | Tiny (two rows shorter than the elder woman), white hair in a knot, white eyes in a face tipped up to the sky, a dark blue-black robe, a black cornel staff. | the Kadmeia's wall walk, her house |
| `OBJ_EVENT_GFX_ICHOR_KRONIST` | `kronist.png` | folk | A plain undyed tunic, a gold sickle pin at the shoulder, and a smiling clay half-mask (ochre, with upturned painted eyes) over his eyes. | the Kronia's greeter and readers |
| `OBJ_EVENT_GFX_ICHOR_HERALD` | `herald.png` | folk | A runner's short linen chiton girt high with red, a red fillet, an ox-horn on a cord across his chest, and the red-and-white barrier pole held upright on his shoulder. | Route 6 (beat 26), the orchestra (beat 32) |
| `OBJ_EVENT_GFX_ICHOR_VINTNER` | `vintner.png` | wine | A wine-red headscarf, a short beard, an undyed exomis off the right shoulder, legs and feet stained grape to the knee, a basket of black grapes on his left shoulder, a pruning hook. | Ikarios, Oinopion; Staphylos |
| `OBJ_EVENT_GFX_ICHOR_ACTOR` | `actor.png` | wine | Dark curls under a gold fillet, a beard, a long wine-red robe banded in gold with white dots, thick tragic soles (a row taller than the townsfolk), his right hand raised and his white mask in his left. | the temple's actors, Hegelochos, Polos |
| `OBJ_EVENT_GFX_ICHOR_THESPIS` | `thespis.png` | wine | Tall on tragic soles, a grape-purple robe trailed with ivy and hemmed in gold, gray-streaked hair under an ivy crown, and the **tragic** mask (slanted brows, mouth turned down, violet eye holes). From behind: the mask's lilac ribbons. | the temple (beat 31), the skene |
| `OBJ_EVENT_GFX_ICHOR_THESPIS_COMIC` | `thespis_comic.png` | wine | The same, in the **comic** mask (arched brows, an open grin with a red tongue). Its back frames are identical to the tragic sheet's. | the temple (beat 31) |
| `OBJ_EVENT_GFX_ICHOR_CHORUS_LEADER` | `chorus_leader.png` | cast | A long white chorus robe one row longer than the townsfolk's, black hair, a white tragic mask, and his right hand black with ink to the wrist (it shows facing down and up). The same sheet serves region B2's masked Iapetos. | the Dionysia |
| `OBJ_EVENT_GFX_ICHOR_BEE_WOMAN` | `bee_woman.png` | cast | A long pale veil over a white woman's mask, a honey-colored robe, a honeycomb hem on robe and veil, and a clay honey jar held before her. | the Dionysia |
| `OBJ_EVENT_GFX_ICHOR_FATE_SPINNER` | `fate_spinner.png` | cast | Black-figure: a glossy black robe with incised linen folds and a meander hem, a white mask under black hair with a linen fillet, a distaff with its wool, and a spindle hanging. | the Dionysia |
| `OBJ_EVENT_GFX_ICHOR_FATE_MEASURER` | `fate_measurer.png` | cast | The same costume incised in bronze, with a notched measuring rod. | the Dionysia |
| `OBJ_EVENT_GFX_ICHOR_FATE_CUTTER` | `fate_cutter.png` | cast | The same costume incised in crimson, with open shears held at her breast. | the Dionysia |
| `OBJ_EVENT_GFX_ICHOR_GOLD_MASK_KING` | `gold_mask_king.png` | cast | A tall actor in a crimson robe hemmed in bronze, a gold crown, and a smooth gold mask with closed eyes framed by black hair. | the Dionysia |
| `OBJ_EVENT_GFX_ICHOR_UNWOVEN_ACTOR` | `unwoven_actor.png` | cast | Borboros as the cursed child, the player's look a size too big: a wide straw petasos (the full frame's width), a blank pale mask, an Aegean-blue chlamys pinned with gold over a cream chiton, a terracotta satchel, sandals, a bronze sickle. A row taller and a pixel broader than anyone else. | the Dionysia |

### Facing and placement

- **Mirrored props.** Props held in one hand swap sides facing right, as on every Gen 3 NPC: the thyrsus, the pole, the hook, the staffs, the distaff, the rod, the sickle, the actor's mask.
- **Face these down** where they stand still: the Vintner (the grapes and the hook show), the Kronists (the half-mask), the bee-woman (the jar), the Fates (the masks and tools), the king (the mask). From behind, the Fates are black hair and robes, and the king is black hair under a crown.
- **Thespis and the actor** stand a row taller on their soles, and **the Unwoven** two, by design.
- **Staff carriers** (the Maenad, Manto, the herald, the Spinner, the Measurer) hold still on the staff side when they walk, as the slice's do.

## Poses

These are sheets of their own, nine 16×32 frames played by `sAnimTable_Standard`, like world-act1's Kleon poses (Phase 2). The facing picks the pose's direction (right is left mirrored). `walk_in_place_*` loops stand → A → stand → B, and here the A and B frames are the pose's own small motion. None of them should walk. Put the object on the right tile with the facing you want, or swap its graphics where it stands (below).

| Constant | Face down | Face left / right | Face up | Walking in place |
|---|---|---|---|---|
| `OBJ_EVENT_GFX_ICHOR_KLEON_SEATED` | on the stage's edge, the petasos actor's hat in his lap | seated in profile, hands on his knees, legs hanging: the front row, turned to the player | his back, the chlamys spread on the bench: the front row, watching the stage | down: he turns the hat (crown up, then edge-on) |
| `OBJ_EVENT_GFX_ICHOR_KLEON_FEAST` | at the Kronia's bench, a loaf in each fist at his chest | in profile, a loaf in his hand | his back, seated | down: a bite from one loaf, then the other; left: a loaf to his mouth |
| `OBJ_EVENT_GFX_ICHOR_ALETHEA_KNEEL` | kneeling at the dig, trowel in her right hand at the ground | kneeling in profile, leaning to the trowel | kneeling, from behind (the soles of her feet show) | down and left: the trowel rises and strikes |
| `OBJ_EVENT_GFX_ICHOR_ALETHEA_SEATED` | seated, holding the program up to show it | seated in profile, the program open in her lap | seated, from behind: watching the stage, or across the Kronia's table | down: she waves the program; left: she lifts it to read |
| `OBJ_EVENT_GFX_ICHOR_GOLD_MASK_KING_KNEEL` | on his knees, his face in his hands, the robe pooled round him | the same, in profile | kneeling, from behind | down: his shoulders heave |

**Which pose for which scene:**

| Scene | Object | Facing |
|---|---|---|
| Beat 29, the long tables | `KLEON_FEAST` | down toward the table, so walking in place makes him eat |
| Beat 29, Alethea opposite him | `ALETHEA_SEATED` | up, across the table |
| Beat 30, the Kadmeia dig | `ALETHEA_KNEEL` | as the dig lies; walk in place to dig |
| Beat 32, the front row | `KLEON_SEATED` | up to the stage. Turn him right (or left) to face the player; hold 60 frames; turn back. |
| Beat 32, Alethea in her seat | `ALETHEA_SEATED` | up to the stage, left or right to read beside the player, down to hold the program up |
| Beat 32, scene four | `GOLD_MASK_KING`, then `GOLD_MASK_KING_KNEEL` | He walks out of the palace door standing, then swaps to the kneeling sheet where he stops. |
| Beat 33, the empty theater | `KLEON_SEATED` | down; walk in place slowly to turn the hat. When he gets up, swap to `KLEON`. |

**Swapping a look mid-scene.** Use the slice's methods: give the object `OBJ_EVENT_GFX_VAR_n` in `map.json`, set `VAR_OBJ_GFX_ID_n` in `ON_TRANSITION`, then to swap in place: `copyobjectxytoperm`, `setvar VAR_OBJ_GFX_ID_n, <new>`, `removeobject`, `addobject`. Or use two objects on one tile with hide flags. world-act1's `design/phase2/SPRITES.md` (on its branch) walks through both.

**Thespis's masks (beat 31).** He stands on the roof's edge in `THESPIS` facing down, then turns up. While his back is turned, swap his graphics to `THESPIS_COMIC`, which looks identical from behind, then turn him down: the mask has changed. After the laurel he can stay comic by the altar ("Today I'm both").

## Field objects

| Constant | Sheet | Size | Palette | Look | Use |
|---|---|---|---|---|---|
| `OBJ_EVENT_GFX_ICHOR_WOODEN_IMAGE` | `misc/ichor/wooden_image.png` | 16×32, one frame, inanimate | wine | An old xoanon on a pale stone base: a post of weathered wood, carved arms worn almost away, and a face rubbed smooth into something round-muzzled, black-nosed, grinning and dog-like, with locks of hair hanging like soft ears. | inside the Temple of Dionysus's door |
| `OBJ_EVENT_GFX_ICHOR_WOODEN_IMAGE_GARLAND` | `misc/ichor/wooden_image_garland.png` | 16×32, inanimate | wine | The same, wearing Oinoe's ivy garland round its neck. | after her errand (swap objects) |
| `OBJ_EVENT_GFX_ICHOR_MASK` | `misc/ichor/mask.png` | 16×16, nine frames | wine | A Prosomime adrift as a mask, in its dex colors: marble white, wine-red lips and cheek, violet haze below, lilac ribbons. Face down, it is split, comic half grinning and tragic half weeping. Face up shows its hollow purple back; face left, its profile. | beat 32: the masks lift off and drift into the skene |
| `OBJ_EVENT_GFX_ICHOR_CROWS` | `misc/ichor/crows.png` | 32×32, nine frames | folk | Five crows on a tilted ring, wings up, level and down. | the Elektran Gate at dusk (Manto's errand) |

- **The mask** uses `sAnimTable_Standard`. Its walk frames bob a pixel, so `walk_slow_*` drifts it and `walk_in_place_*` makes it hover. It has no tracks.
- **The crows** use `sAnimTable_Standard` too. Each frame turns the ring a little and moves the wings, so `walk_in_place_*` wheels them over one spot and `walk_fast_down` carries them off south. They're a 32×32 sprite (like the vanilla 32×32 people), so place them a tile or two above the camp.
- **The wooden image** is drawn only in colors the folk and wine palettes share. It reads the same under either tag; it is registered under wine because the temple's actors already load it.

## Thyrsa's townsfolk (optional palette variants)

The wine palette is the folk palette index for index (below). So any folk walker shown under the wine tag is a Thyrsa version with no new pixels. These six read well and are registered, each reusing its folk sheet's pic table:

| Constant | Made from | Reads as | Suggested for |
|---|---|---|---|
| `OBJ_EVENT_GFX_ICHOR_MOM_THYRSA` | Mom | a matron in a wine-red peplos and linen apron | Chthonia; any Thyrsa mother |
| `OBJ_EVENT_GFX_ICHOR_WOMAN_THYRSA` | Woman | a purple peplos under an ochre himation and a linen kerchief | Eudora; the city's women |
| `OBJ_EVENT_GFX_ICHOR_YOUTH_F_THYRSA` | Youth F | a lilac chiton, a braid with a wine ribbon | Erigone, Staphylos's daughter; the city's girls |
| `OBJ_EVENT_GFX_ICHOR_KID_M_THYRSA` | Kid M | a wine-red tunic | the city's boys |
| `OBJ_EVENT_GFX_ICHOR_MERCHANT_THYRSA` | Merchant | a purple chiton under an apron | Euthykles the mask-maker; the Agora |
| `OBJ_EVENT_GFX_ICHOR_HARVESTER_THYRSA` | Harvester | a wine-red headscarf over the olive dress | the vineyard women |

Others from Part 10's list fit existing sheets as they stand: Staphylos → `VINTNER`, Polos (an old tragic actor) → `ACTOR`, Pindaros (the poet) → `ELDER_M`, Lysidike → `WOMAN`, her twins Amphis and Zetes → `KID_M`, Opsimos and Peneleos (the watch-house) → `MAN` and `HOPLITE`. Hippias's sleeping frame and Erigone's stained legs aren't drawn.

## Palette plan

Every new walker and object uses one of three tags, so a map shows at most three Ichor OBJ palette slots:

| Tag | Palette | New sheets |
|---|---|---|
| `OBJ_EVENT_PAL_TAG_ICHOR_FOLK` (0x1135) | the slice's `ichor_folk.pal`, unchanged | Maenad, Satyr, Silenos, Manto, Kronist, herald, crows |
| `OBJ_EVENT_PAL_TAG_ICHOR_CAST` (0x1134) | the slice's `ichor_cast.pal`, unchanged | the Dionysia's players (chorus leader, bee-woman, the three Fates, the king and his kneeling sheet, the Unwoven) and Kleon's and Alethea's poses |
| `OBJ_EVENT_PAL_TAG_ICHOR_WINE` (0x1136, **new**) | `graphics/object_events/palettes/ichor_wine.pal` | the Vintner, the city maenad, the Actor, Thespis (both masks), the wooden image, the floating mask, the six Thyrsa townsfolk |

**Why a new tag.** The Vintner's stained legs and black grapes, the city maenad's wine-red, and Thespis's purple robe need wine and grape, and neither slice palette has them. SCRIPT.md wanted the Vintner to "share the Harvester's palette family", so the wine palette is the folk palette with four colors changed and every role in its place:

| # | Char | Folk | Wine |
|---|---|---|---|
| 3 | `u` | terra 184 72 48 | **wine** 160 40 72 |
| 11 | `n` | blue_d 24 56 120 | **grape_d** 56 32 80 |
| 12 | `B` | blue 48 104 176 | **grape** 112 56 136 |
| 13 | `a` | sky 112 168 224 | **lilac** 184 136 208 |

The other eleven (ink, brown, ochre, gold, both skins, both linens, gray, both olives) are identical. To change a wine color, edit `_WINE_SWAP` in `sprites_act2.py` and rerun `--write`.

**Why the Dionysia's players are cast.** The Unwoven needs the player's own Aegean blue, straw gold and cream, and the king needs crimson and gold. The Fates need ink with linen, bronze and crimson incisions, and the chorus leader and bee-woman need white and honey. The cast palette holds all of that. Kleon and Alethea sit in the same theater in the same palette.

**Measured in game.** Thirteen walkers from all three families stood in the bedroom with the player. The live `sSpritePaletteTags` read `1200 1100 1135 1136 1134 FFFF…`: the weather, the player, folk, wine and cast, **5 of 16 slots**.

| Map | Ichor tags expected |
|---|---|
| Route 6, Kithairon, the Kronia | folk (Maenads, Satyrs, Kronists, herald) and cast (Kleon, Alethea, grunts) |
| Thyrsa City | folk, wine (Vintners, the city Maenad, actors, Thyrsa townsfolk), cast (Kleon, Alethea) |
| The temple | wine (actors, Thespis, the image), plus folk if Lasos is a folk walker |
| The theater (beat 32) | cast (the players, Kleon, Alethea), folk (the herald), wine (the floating masks) |

## Deviations from SCRIPT.md

- **The three Fates** are three sheets in one palette, not "three palettes of one sheet". Their tools differ (distaff, rod, shears), so they need their own pixels anyway, and one shared palette saves the stage two OBJ slots. Each still has her own color: her incisions and fillet are linen, bronze or crimson.
- **Kleon's seated pose** is two sheets: `KLEON_SEATED` for the theater and `KLEON_FEAST` for the Kronia's tables. Both scenes face him down, and a loaf in each hand and a hat in the lap can't share a frame.
- **Alethea's poses** are two sheets: `ALETHEA_KNEEL` (the trowel) and `ALETHEA_SEATED` (the program). "Holding it up" is drawn seated, facing down. When she comes down from the seats after the play, she walks on her own sheet and the picture window shows the program.
- **The gold-masked king** is two sheets: he walks out standing, then kneels (`GOLD_MASK_KING_KNEEL`).
- **Thespis** is two sheets (the tragic and the comic mask) rather than one sheet with extra frames, because the engine picks frames by facing. The swap is invisible from behind. He **stands** on the roof's edge: a seated Thespis isn't drawn.
- **The herald** "reuses the runner", but the runner walker doesn't exist yet (world-act1 hasn't drawn its RUNNER class). So the herald is drawn new in a runner's look, and a runner walker could start from him. His barrier pole is carried upright on his shoulder.
- **The city maenad** (Part 3: "one palette for the city (wine-red)") is a second sheet, `MAENAD_THYRSA`. The saffron chiton is gold in both palettes, so a palette swap alone couldn't turn it wine-red.
- **Manto** has her own small robe body, two rows shorter than the elder woman's, because she's tiny.
- **Silenos** is drawn standing; beat 34 seats him on a costume chest. The chest is the scenes agent's tile.

## Critique passes

**Walkers**

1. **First draft** (all at 4×, next to Birch and the slice's walkers).
   - The Satyr's mask was a big white slab over his face that read as an owl's head.
   - The Kronist's half-mask was a red band with slits, a blindfold.
   - Silenos was an old man in a gray tunic, not round and half-naked.
   - The Maenad's thyrsus had a pine cone one pixel wide.
   - The Vintner's grape basket sat beside his ear like an earmuff.
   - The bee-woman's back was a featureless tan slab.
   - The Fates' incised hair lines read as eyes, so from behind each had a black face.
   - The king's gold mask read as yellow skin.
   - On the poses, Kleon's loaves at his shoulders read as pom-poms, and the king's hands vanished into his gold mask.
2. **Redraw.**
   - The Satyr's mask got horn stubs and goat ears.
   - The Kronist's mask turned ochre clay with painted upturned eyes.
   - Silenos got a bare belly with the goatskin over one shoulder, and his merry squint.
   - The pine cone is 4 px with scales.
   - The basket sits on the Vintner's shoulder with its wicker showing.
   - The veil has folds and a honeycomb border.
   - The Fates' backs are plain black hair under the fillet.
   - The king's mask is framed by black hair and shaded bronze.
   - Kleon holds his loaves at his chest and bites each in turn.
   - The king's hands are peach with ink fingers, his crimson sleeves rising to them.
3. **In game.** The Quickstart bedroom held thirteen at a time, turned through four directions, with walk-in-place running the poses.
   - The wooden image was dark brown on a brown floor, a muddy silhouette. It is now weathered gray-tan wood with a warm mid-tone and a pale rubbed muzzle.
   - Manto's staff stood a pixel clear of her hand; it now touches it.
   - The king's sob duplicated his crown's points; it now drops him a pixel.
   - Everything else read in game as it did at 4×. The Thespis masks read tragic and comic at 1×.

**Portraits**

1. **First draft.**
   - The Actor's and Thespis's heads floated on long necks above their shoulders.
   - Thespis's mask was a bare white oval with no head round it, so it read as a floating mask.
   - Silenos's belly was hidden behind his goatskin and wineskin.
   - The Vintner's purple shins had a straight top edge and read as boots.
2. **Redraw.**
   - Both heads are seated on the shoulders.
   - Thespis's mask is narrower, framed by gray hair and a gray beard under his ivy crown, with a tear on the tragic half.
   - Silenos's belly is a broad round dome with a crease, the goatskin narrowed, the wineskin moved out under his arm.
   - The Vintner's stain has a ragged top edge and splashes above the knee.
3. **Fixes and in game.**
   - Silenos's brows made a frown, so his eyes became upturned merry arcs.
   - His head was pulled down so the beard spills onto the belly.
   - All six were checked in their battle intros. The class and name fit the box in each, and each pic reads on the platform at 1×.

## In-game checks

Both checks patch the emulator's in-memory ROM from a Lua script (mGBA's `emu.memory.cart0`), so no map or party file changes.

- **Walkers.** The script points the Quickstart bedroom's `MapEvents` at templates written into free ROM, so the new sheets spawn there, walking in place. It turns them down, left, up and right, screenshots each, and logs `sSpritePaletteTags`. The result is `img/sprites_batch1_ingame.png`.
- **Portraits.** The script gives six Act II trainers their new class and pic in every difficulty's `gTrainers` row (Euia, Komos, Hegelochos, Ikarios, Thespis and Silenos). A test-only blob in spare EWRAM (the `route1.sh` technique) then battles each one. The result is `img/portraits_batch1_ingame.png`.

The harness was throwaway and isn't committed: a consts file, an assembled blob and the Lua. It could become `tools/ichor/tests/act2_sprites.sh` if the session wants one. The two `_ingame.png` captures are its output; `--write` doesn't regenerate them.

`make` is green and `tools/ichor/smoke_test.sh` passes. The ROM is 25,643,524 B (76.42%), 64,864 B more than the batch's start (mostly the 28 uncompressed walker sheets at 2,304 B each).

## Still open

- **Not drawn yet:** a seated Thespis, a seated Silenos on his chest, Hippias's sleeping frame, Erigone's and Staphylos's stained legs on townsfolk bodies, and a runner walker for the RUNNER class.
- **Part 10's other art:** the battle backgrounds, item icons, the Mask Laurel icon and the map-name steles aren't this batch's.
- **Two tones per material:** as in the slice, materials have two tones plus the outline.
- **Not opened in Porymap:** the entries follow the slice's format exactly, so they should display.
