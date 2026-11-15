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

# Act II, batch 2: the road west

The Fowler class and the people of beats 35–37: Route 8 (the Kopais), Lebadeia and Trophonios's cave, Route 9, Kirrha, the Gulf ferry and Aigion. They follow batch 1's house style and SCRIPT.md Part 10's sprite list, and every name is the one BUILD.md's batch 2 block fixed. `include/constants/ichor_gfx_stubs_act2.h`'s batch 2 aliases are deleted, so the maps' names now resolve to the real art.

| Source | Rebuild | Preview |
|---|---|---|
| `tools/ichor/art/sprites_act2_b2_classes.py` (the two Fowler portraits) | `python3 tools/ichor/art/sprites_act2_b2_classes.py --write` | `--preview DIR`: the 3× sheet, 6× singles, pixel grids |
| `tools/ichor/art/sprites_act2_b2.py` (walkers, poses, the note, the extras) | `python3 tools/ichor/art/sprites_act2_b2.py --write` | `--preview DIR` for the 4× sheet; `--grids DIR` for 8× pixel grids |

`--write` with no name also rewrites the contact sheets:

- `img/sprites_batch2.png`: every walker, pose and object at 2×, after seven of the walkers they're drawn to match (the slice's fisher, sailor, elder, goatherd, hoplite and Alethea, and batch 1's Kronist).
- `img/portraits_batch2.png`: the two Fowlers at 2× on the grass battle background, after five earlier portraits (Shepherd, Harvester, Goatherd, Vintner, Maenad).

In-game captures: `img/sprites_batch2_ingame.png` (all 23 sheets in the Quickstart bedroom, turned down, left, up and right) and `img/portraits_batch2_ingame.png` (both Fowler battle intros).

## For party files

| Trainers | `Class:` | `Pic:` |
|---|---|---|
| Gorgidas (Route 8) | `Fowler` | `Fowler M` |
| Timoxena (Route 8) | `Fowler` | `Fowler F` |

The staged `design/phase3/parties/kopais.party` already says this. `tools/ichor/act2/fold_parties.py` folds a class or pic to a stand-in only when `trainers.h` lacks it, so rerunning it now writes the real ones.

## Trainer class

| Constant | Shown as | Money | Who |
|---|---|---|---|
| `TRAINER_CLASS_FOWLER` | FOWLER | 5 | the Kopais's bird-catchers |

- **Money:** 5, the same as batch 1's Maenads and Satyrs. Fowlers are poor marsh folk, so they pay like the mountain's bacchants rather than the vintners and actors.
- **Ball:** the default.
- **In the box:** checked in battle: "You are challenged by FOWLER GORGIDAS!" and "FOWLER TIMOXENA!" both fit.

## Trainer pics

Each is a 64×64, 16-color front pic with its palette embedded in the PNG. The two have their own palettes, which is Part 3's "one male and one female palette".

| Constant | `Pic:` | Look | File |
|---|---|---|---|
| `TRAINER_PIC_FOWLER_M` | `Fowler M` | A lean, clean-shaven man under a broad straw hat with a peaked crown and a terracotta band. He wears a short undyed tunic belted in terracotta, with bare legs and sandals. A folded net hangs over his far shoulder and down his back, with his far hand on its fold. His near hand holds a green reed decoy-pipe to his lips. A wicker quail cage, a speckled quail inside, hangs from his belt at the near hip. | `graphics/trainers/front_pics/fowler_m.png` |
| `TRAINER_PIC_FOWLER_F` | `Fowler F` | The same hat with a sky-blue band. Long dark hair falls behind her, and a braid tied in blue lies over her near shoulder. Her paler linen tunic reaches the knee, with a sky-blue girdle. The net is over her far shoulder and the pipe at her lips. Her far hand holds the quail's cage up to show you: Timoxena's decoy. | `graphics/trainers/front_pics/fowler_f.png` |

## Walkers

All sheets are in `graphics/object_events/pics/people/ichor/`. Each is 144×32 (nine 16×32 frames in the slice's layout, feet on row 30, the 1 px step bob) and uses `sAnimTable_Standard`.

| Constant | Sheet | Palette | Look | Used in |
|---|---|---|---|---|
| `OBJ_EVENT_GFX_ICHOR_FOWLER` | `fowler.png` | folk | The peaked straw hat across the whole frame with a terracotta band, short dark hair and no beard. An undyed tunic with a terracotta belt, the folded net over his left shoulder (down his back from behind), the decoy-pipe at the corner of his mouth, and the wicker cage hanging from his right hand. | Route 8 (Gorgidas) |
| `OBJ_EVENT_GFX_ICHOR_FOWLER_F` | `fowler_f.png` | folk | The same hat with a sky-blue band, hair past her jaw and a long braid down her back over the net, and a paler linen tunic to mid-calf with a sky-blue girdle. The same pipe, net and cage. | Route 8 (Timoxena) |
| `OBJ_EVENT_GFX_ICHOR_SAON` | `saon.png` | folk | Bald under a terracotta fillet, gray brows, a white fringe and a long white beard, a white robe to the floor with a terracotta girdle. He holds a wax tablet at his chest in both hands (a wooden frame, dark wax, a scratched line); from the side it is a plank. | Lebadeia (the grille; beat 35C) |
| `OBJ_EVENT_GFX_ICHOR_TROPHONIAN_PRIEST` | `trophonian_priest.png` | folk | Dark hair streaked gray and a short gray beard under the same fillet, the same white robe, and a lit clay lamp held out before him for the descent. | Lebadeia (by the chair; beat 35C) |
| `OBJ_EVENT_GFX_ICHOR_AGAMEDES` | `agamedes.png` | folk | Dark curls under a terracotta sweatband, a short beard with stone dust in it, a terracotta exomis under a dusty linen apron, and hands and forearms gray with stone dust. A wooden mallet is held up beside his shoulder. | the mason's house |
| `OBJ_EVENT_GFX_ICHOR_PANOPEUS` | `panopeus.png` | folk | The sailor's bare chest, linen kilt and blue sash, under a tall blue felt pilos with a terracotta band (the captain's hat; the fisher's is brown), and a full black beard going gray. | Kirrha's and Aigion's quays, the ferry (beat 37B) |
| `OBJ_EVENT_GFX_ICHOR_TEMPLE_GUARD` | `temple_guard.png` | cast | The Hoplite with a white horsehair crest, a white cloak (two edges from the front, the whole back from behind), a blue chiton under the linen corselet, bronze greaves, a spear, and a white shield rimmed in bronze with Apollo's green laurel wreath. | Kirrha's pilgrims' gate (beat 37A) |
| `OBJ_EVENT_GFX_ICHOR_HERKYNA` | `herkyna.png` | folk | A girl of nine (the child's body): dark hair loose to her shoulders with a white flower over one ear, a sky-blue tunic, barefoot. | Herkyna's house |
| `OBJ_EVENT_GFX_ICHOR_XENODIKE` | `xenodike.png` | folk | Dark hair in a knot, a linen chiton to mid-calf, a terracotta traveling cloak pinned at the right shoulder, and a sky-blue cloth bundle under her left arm. | Route 9's lookout, Kirrha's inn |
| `OBJ_EVENT_GFX_ICHOR_THYIA` | `thyia.png` | folk | White hair drawn back into a bun on the crown, a kind old face with smiling eyes and rosy cheeks, a blue peplos, a linen apron, and a twig besom in her right hand with its bristles on the floor. | the old sweeper's house |
| `OBJ_EVENT_GFX_ICHOR_TISAMENOS` | `tisamenos.png` | folk | The elder walker with a full head of white hair (Elder M is bald) and a long white beard, a sea-blue himation, and the walking staff. | the old Achaean's house |
| `OBJ_EVENT_GFX_ICHOR_HELIKE` | `helike.png` | folk | A terracotta kerchief over dark hair worn long in a braid, the goatherd's shaggy goat-hair cloak over an undyed dress to mid-calf, a bronze bell at her belt, and a crook. | the goatherd's house |

### Facing and placement

- **The Fowlers** read best facing down or sideways, where the pipe and cage show. From behind, the net is the read (and her braid).
- **Saon** faces down to show the tablet; the priest faces down to show the lamp.
- **The temple guards** are the Hoplite's frames, so as with Agis the side view is all shield: white with the laurel.
- **Thyia, Tisamenos and Helike** carry a broom, staff or crook in the right hand. As with the slice's staff carriers, the hand holds still when they walk, and the prop swaps sides facing right.
- **Agamedes's mallet** swaps sides facing right too.
- **Shadows:** every batch 2 walker keeps its shadow (`SHADOW_SIZE_M`), so any of them can stand in for a decoy (SYSTEMS.md §10's tell).

## Poses

Pose sheets are nine 16×32 frames in the standard order, played by `sAnimTable_Standard`, as in batch 1: the facing picks the pose, and `walk_in_place_*` plays its small motion. None of them should walk.

| Constant | Palette | Face down | Face left / right | Face up | Walking in place |
|---|---|---|---|---|---|
| `OBJ_EVENT_GFX_ICHOR_PILGRIM_BLANKET` | folk | sitting on the step, wrapped in a terracotta blanket to the chin, hands holding it shut, the white chiton's hem and bare feet below | in profile, knees up under the blanket | the blanket over the back | down or left: a shiver, the head ducking into the blanket |
| `OBJ_EVENT_GFX_ICHOR_PILGRIM_BLANKET_2` | folk | the same, gray-haired, in a blue blanket | | | |
| `OBJ_EVENT_GFX_ICHOR_PILGRIM_BLANKET_3` | folk | the same, auburn-haired, in an olive blanket | | | |
| `OBJ_EVENT_GFX_ICHOR_ALETHEA_RIM` | cast | seated on the rim, a wax tablet on her knees, the satchel open beside her with a scroll showing, stylus in hand | in profile, writing on the tablet on her knee | from behind (`ALETHEA_SEATED`'s back) | down: the stylus lifts and scratches; left: she writes |

- **The pilgrims** sit on the steps facing down, so walking in place makes them shiver ("Everyone's cold after"). The three swaps are three sheets: one palette can only swap colors by using different indices.
- **Alethea at the springs (beat 35B)** sits on the bright spring's rim in `ALETHEA_RIM`, facing down and walking in place to write. When she "stands and waves", swap her to `ALETHEA` (two objects with hide flags, or a `VAR_OBJ_GFX_ID_n` respawn, as batch 1's recipe).

## Field object

| Constant | Sheet | Size | Palette | Look | Use |
|---|---|---|---|---|---|
| `OBJ_EVENT_GFX_ICHOR_ALETHEA_NOTE` | `misc/ichor/alethea_note.png` | 16×32, one frame, inanimate | folk | A green reed with a brown plume stuck in a tuft of mud, with a slip of wax tablet tied to it: a wooden frame, dark wax, Alethea's scratched lines. | Route 8, five times (beat 35A) |

It is 16×32 rather than the slice's 16×16 tablet because a reed taller than a tile reads as a reed among the Kopais's reeds. It uses `sAnimTable_Inanimate`; don't `turnobject` it.

## Part 10's other folk (extras)

These are the slice's townsfolk recolored inside the folk palette, so a road-west map still loads only the folk tag. Each is its own sheet. Only the muleteer's staff is new pixels.

| Constant | Made from | Reads as | For |
|---|---|---|---|
| `OBJ_EVENT_GFX_ICHOR_STROPHIOS` | Merchant | the apron and purse over a terracotta chiton | Strophios, Kirrha's innkeeper |
| `OBJ_EVENT_GFX_ICHOR_PYLADES` | batch 1's herald's head on the tunic body | a clean-shaven youth under a terracotta fillet, a sky-blue chiton | Pylades |
| `OBJ_EVENT_GFX_ICHOR_MULETEER` | Man, plus the elder's staff | the bearded man in an undyed exomis with a walking staff | Kirrha's muleteer |
| `OBJ_EVENT_GFX_ICHOR_EEL_SMOKER` | Man | the bearded man in a smoke-gray exomis | Route 8's eel-smokers |
| `OBJ_EVENT_GFX_ICHOR_ELDER_M_STONE` | Elder M | the bald elder in a terracotta himation | the old man on Route 9's boundary stone |
| `OBJ_EVENT_GFX_ICHOR_ELDER_M_LETHE` | Elder M | the bald elder in an ochre himation | the old man who drank from Lethe |

Others from Part 10 already fit sheets that exist:
- Herkyna's grandmother: `ELDER_F`.
- Lebadeia's cake-seller and child: `WOMAN` and `KID_M`.
- The decoys (Route 8's traveler, Kirrha's beggar): `MAN` or any walker above, all with shadows.
- The Kronist on the crate: `KRONIST`.

## Palette plan

**No new tag.** Every sheet uses the slice's folk or cast palette, unchanged:

| Tag | Sheets |
|---|---|
| `OBJ_EVENT_PAL_TAG_ICHOR_FOLK` (0x1135) | both Fowlers, Saon, the priest, the three pilgrims, Agamedes, Panopeus, Herkyna, Xenodike, Thyia, Tisamenos, Helike, the note, and the six extras |
| `OBJ_EVENT_PAL_TAG_ICHOR_CAST` (0x1134) | the temple guard (the Hoplite's palette) and Alethea on the rim (her own) |

**Measured in game:** all 23 sheets at once in the Quickstart bedroom. The live `sSpritePaletteTags` read `1200 1100 1135 1134 FFFF…` (the weather, the player, folk and cast), **4 of 16 slots**. A road-west map loads folk, plus cast where Alethea, Kleon, a grunt or the temple guards stand.

## Deviations from SCRIPT.md

- **The Fowlers' hat** has a peaked crown, the tholia of Boeotia's Tanagra figurines (the Kopais is in Boeotia). Part 3 says it "shares the fisher's straw hat", but the slice's fisher wears a brown felt pilos. The only straw hat in the game is the player's domed petasos, and in battle the Fowler stood opposite the player's back pic in nearly the same hat. The peak keeps them apart.
- **The Fowler F walker** wears her tunic to mid-calf, not short, so she reads as a woman at 16×32. Her portrait's tunic stops at the knee.
- **"One male and one female palette"** became two pics and two walkers, each pic with its own palette.
- **The priest** isn't white-haired like Saon: Part 10 calls them all elders, but at 16×32 a second white head would read as a second Saon. He is graying and carries a lamp.
- **The pilgrims** are "three palette swaps of the initiate/pilgrim body", but no such body exists in this tree, so they are drawn new: one seated, wrapped body, recolored three ways.
- **Agamedes** is "the potter walker with a mallet", but no potter walker exists on this branch (world-act1's POTTER isn't merged), so he is drawn new on the tunic body. His mallet is held up beside his shoulder: hanging at his side, it read as a box on the floor.
- **The temple guard** is the Hoplite's pixels recolored in the cast palette. A palette swap inside one palette means new indices, so it is its own sheet.
- **Xenodike** sits on the lookout's bench in beat 36, but she is drawn as a walker because she walks down off the map. Stand her on the bench tile facing down.
- **Thyia:** the old sweeper's house's lines call her PHEMONIS while the house table calls her Thyia. The sheet is `THYIA`, the name the stub fixed. The world session should settle her name.
- **Not drawn:** the reed-boat boy (he sits in a reed-boat object, which is a new object, not a swap) and the Pokémon objects (follower sprites).

## Critique passes

**Walkers**

1. **First draft** (4× next to the slice's fisher, sailor, elder, goatherd and hoplite).
   - Fowler F was the man in a different belt. The face was the same, her braid was two pixels, and the tunic was the same color.
   - The quail cage hung at the feet and read as a yellow box on the ground.
   - Saon's fillet ribbons ran down the back of his bald head as a red stripe, a mohawk.
   - The priest's gray hair under the fillet read as a steel helmet.
   - Agamedes's stone-gray hands were linen-pale and read as white gloves. His mallet hung at his feet like a box.
   - Thyia's hair was a white cloud twice the size of her face, and the three blank rows above her head lifted it further.
   - Tisamenos's white hair had gray speckles and read as a sheep's fleece.
   - Helike's kerchief covered her head down to the brows: a red helmet.
2. **Redraw.**
   - Fowler F has a sky-blue hatband and girdle, a paler linen tunic, hair past her jaw, and a braid down her back over the net.
   - The cage is a domed wicker cage with gold ribs, held by its loop in the hand at the hip.
   - Saon's back is a white fringe under the fillet, with the knot only.
   - The priest is dark-haired going gray.
   - Agamedes's hands are solid stone gray, and his mallet is a wooden head held up beside his shoulder.
   - Thyia has a small bun on the crown, a face as large as anyone's, and no blank rows.
   - Tisamenos's hair has linen strands instead of speckles.
   - Helike's kerchief sits on the crown, with her hair showing at the brow and sides.
3. **In game** (all 23 sheets in the bedroom, turned through four facings; then the Fowler battles).
   - All four facings show the right frames, right is left mirrored, and both palettes load by tag.
   - At 1× every walker reads as itself: the hats, the white priests, the guard's laurel shield, the note's slip on its reed.
   - Opposite the player in battle, the Fowler's domed hat was the player's own. Both the portraits and the walkers now have the peaked crown (the tholia, above).
   - The note's sheet turns to garbage if `turnvobject` is run on it; it is inanimate, as above.

**Portraits**

1. **First draft.**
   - The hat brim sat over the brows, so the eyes vanished under it and the face was a blank.
   - The hair was ink-dark and merged with the outline.
   - The cage's dark interior with two quail pixels read as a jack-o'-lantern.
   - Fowler F differed from M only in the band color.
2. **Redraw.**
   - The hat is raised three rows so the brows and eyes sit under the brim's shadow, and the hair is a warmer brown.
   - Fowler F has long hair behind, a braid over her near shoulder, and a knee-length tunic. She holds the cage up in her far hand to show you the decoy quail.
   - The cage is three gold ribs over the wicker's shadowed back wall, with a plump speckled quail visible between them.
3. **In game.**
   - Both battle intros were checked. Their VS silhouettes read as broad-hatted figures, and the class and name fit the box.
   - The peaked crown (above) went in after this pass, and the walkers took it too.

## In-game check

The check was throwaway and isn't committed: an assembled blob, a consts file, the Lua and a shell runner. It changes no map or party.

- **Walkers.** After Quickstart, a test-only event script, assembled with the game's macros, is copied into spare EWRAM (0x0203F000) and run as the bedroom's `ON_FRAME` script. It creates the 23 sheets as virtual objects (`createvobject`), then turns them west, north and east with 60 frames between (`turnvobject`). The Lua screenshots each facing and logs `sSpritePaletteTags`.
- **Portraits.** The Lua writes `TRAINER_CLASS_FOWLER` and `TRAINER_PIC_FOWLER_M` / `_F` into Gorgidas's and Timoxena's `gTrainers` rows (every difficulty) in the emulator's ROM (`emu.memory.cart0`). The blob then gives a Pokémon and runs `trainerbattle_no_intro` against each. The intros are screenshotted every 30 frames.

`make` is green and `tools/ichor/smoke_test.sh` passes. The ROM is 22,553,452 B (67.21%), 53,440 B more than the batch's start: 22 uncompressed sheets at 2,304 B each, the note and the two portraits.

## Still open (batch 2)

- **Not drawn:** the reed-boat boy in his reed-boat object.
- **Part 10's other art:** the marsh and mountain-road battle backgrounds, item icons and the map-name steles aren't this batch's.
- **Two tones per material:** as in the slice.
- **Not opened in Porymap:** the entries follow the slice's format exactly.
