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

---

# Act II, batch 3: sprites (Arkadia)

Portraits, classes, walkers, poses and field objects for beats 38–44 (SCRIPT.md Part 10's Arkadia list and Part 3's class table), drawn to batch 1's standard above. Every name is the one BUILD.md fixed, except the muleteer: batch 2 already drew `OBJ_EVENT_GFX_ICHOR_MULETEER` (Kirrha's), so Route 11's is `OBJ_EVENT_GFX_ICHOR_MULETEER_GOAD`.

| Source | Rebuild | Preview |
|---|---|---|
| `tools/ichor/art/sprites_act2_b3_classes.py` (portraits) | `python3 tools/ichor/art/sprites_act2_b3_classes.py --write` | `--preview DIR`: the 3× sheet, 6× singles, pixel grids |
| `tools/ichor/art/sprites_act2_b3.py` (walkers, poses, objects) | `python3 tools/ichor/art/sprites_act2_b3.py --write` | `--preview DIR` for the 4× sheet; `--grids DIR` for 8× pixel grids |

`--write` with no name rewrites the contact sheets too:

- `img/sprites_batch3.png`: every sheet at 2×, after four of the slice's walkers and two of batch 1's for scale.
- `img/portraits_batch3.png`: the three portraits at 2× on the grass battle background, after five earlier ones.

In-game captures (not regenerated by `--write`): `img/sprites_batch3_ingame.png` (the sheets in the Quickstart bedroom facing down, left, up and right; then Kallisto looking down from her seat with Kleon risen; then the hind and the hound mid-run) and `img/portraits_batch3_ingame.png` (the Huntress's and Kallisto's battle intros).

## For party files

| Trainers | `Class:` | `Pic:` |
|---|---|---|
| Euadne, Auge, Kyrene, Anthia, Prokris, and every huntress acolyte or forest hunter | `Huntress` | `Huntress` |
| Agapenor, Hippothoos and the kiln men | `Charcoaler` | `Charcoaler` |
| Kallisto | `Hierophant` (unchanged) | `Hierophant Kallisto` |

`tools/ichor/act2/fold_parties.py` picks the new class and pics up by itself: it only stands in for names `trainers.h` lacks. Re-fold the batch 3 parties after merging.

## Trainer classes

| Constant | Shown as | Money | Who |
|---|---|---|---|
| `TRAINER_CLASS_HUNTRESS` | HUNTRESS | 7 | Artemis's acolytes, Arkadia's forest hunters |
| `TRAINER_CLASS_CHARCOALER` | CHARCOALER | 6 | Arkadia's charcoal-burners |

- **Money:** huntresses are a temple's acolytes, a step above the road's classes; charcoal-burners pay like the vintners. BALANCE.md sets no payouts.
- **In the box:** "You are challenged by HUNTRESS EUADNE!" and "…by HIEROPHANT KALLISTO!" both fit (checked in battle).

## Trainer pics

| Constant | `Pic:` | Look | File |
|---|---|---|---|
| `TRAINER_PIC_HUNTRESS` | `Huntress` | A young woman in a short saffron chiton girt high under the breast with a red girdle, the hem at mid-thigh. A spotted fawnskin crosses from her near shoulder, pinned there with a silver crescent. Her dark hair is bound up in a knot with a strand loose. She wears laced fawn hunting boots. Her bow is held low in her near fist, the string slack. Her far hand reaches back to the red-and-white fletching of the arrows standing out of the quiver on her back. | `graphics/trainers/front_pics/huntress.png` |
| `TRAINER_PIC_CHARCOALER` | `Charcoaler` | A stocky man, broad in the shoulder, in a soot-gray tunic under a tan leather apron. He has a sooty felt cap pulled low, a short dark beard and a smudged face squinting against smoke. He is black to the elbows, with black fists. The long iron rake rests on his far shoulder, its tines hanging behind him. A turf kiln mound smokes at his back with a glowing vent and sparks in the smoke. | `graphics/trainers/front_pics/charcoaler.png` |
| `TRAINER_PIC_HIEROPHANT_KALLISTO` | `Hierophant Kallisto` | Tall and very still, her face lifted in profile to the sky. Her dark hair is drawn back into one long braid over her near shoulder, tied in silver. She wears a short silver-gray chiton banded in night blue, with a silver crescent at the shoulder and laced running boots. A dark bearskin hangs from her far shoulder, the bear's round-eared head resting on it. The bow she never draws is slung across her back, its upper limb and string rising over her shoulder. | `graphics/trainers/front_pics/hierophant_kallisto.png` |

## Walkers

All are 16×32 frames in `graphics/object_events/pics/people/ichor/`, in the slice's layout (feet on row 30, the 1 px step bob).

| Constant | Sheet | Palette | Look | Used in |
|---|---|---|---|---|
| `OBJ_EVENT_GFX_ICHOR_HUNTRESS` | `huntress.png` | folk | Hair bound up in a knot, a short saffron chiton, a pale spotted fawnskin across from the left shoulder, terra knee boots, the quiver on her back (fletching over the right shoulder), and the bow held low in her left hand. | the huntresses' cordon, the Cypress Wood (Euadne), the temple's acolytes |
| `OBJ_EVENT_GFX_ICHOR_CHARCOALER` | `charcoaler.png` | folk | A sooty gray felt cap, a short beard and a soot smudge, a gray tunic under a tan leather apron, arms black from the elbows, and the iron rake over his shoulder, its head behind him. | Agapenor, Hippothoos, the kiln men on Route 11 |
| `OBJ_EVENT_GFX_ICHOR_KALLISTO` | `kallisto.png` (11 frames) | theoxenia | A row taller than the townsfolk: dark hair with a braid over her right shoulder, a short gray chiton girt dark, the dark bearskin over her left shoulder pinned silver, and the bow's tips showing where it's slung across her back. Frames 9 and 10: seated on the rock, knees drawn up, arms round her shins, the bearskin spread behind her. In 9 her face is tipped up to the sky; in 10 she looks down at you. | the moonlit rock (beat 44) |
| `OBJ_EVENT_GFX_ICHOR_PHYLONOE` | `phylonoe.png` | folk | A girl of nine: a saffron robe to her ankles, auburn hair, and a little cap of brown fur with two round bear's ears. | the temple's porch |
| `OBJ_EVENT_GFX_ICHOR_MULETEER_GOAD` | `muleteer_goad.png` | folk | A lean mountain man in a peaked ochre felt pilos, a russet tunic under a shaggy gray goat-hair cape, wrapped shins, and a long cornel goad with an iron prick. | Route 11, Styx Falls |
| `OBJ_EVENT_GFX_ICHOR_LAMPLIGHTER` | `lamplighter.png` | folk | Dark curls, an olive tunic, a clay oil flask at his belt, and a long pole with a lit taper at its head. | Arkadia at dusk |
| `OBJ_EVENT_GFX_ICHOR_MNASEAS` | `mnaseas.png` | folk | The slice's elder man recolored: his himation in poplar white (linen shaded gray), the white hair and beard and staff unchanged. | the Pool of Mnemosyne |

- **Mirrored props**, as in batch 1: the bow, the goad, the rake and the taper swap hands facing right.
- **Kallisto never walks north.** Facing up she sits (below), so a walk north slides her seated. She climbs down off the rock walking down.

## Pose: Kleon on the stump

`OBJ_EVENT_GFX_ICHOR_KLEON_STUMP` (`kleon_stump.png`, 11 frames, cast) is beat 42's Kleon. He sits low with his elbows on his knees and doesn't look up. The facing picks the view, and walking in place he hangs his head a pixel lower.

| Face down | Face left / right | Face up | Frames 9–10 |
|---|---|---|---|
| his front: hunched, head bowed so his hair hides his eyes, hands clasped between his knees | profile, hunched, a forearm across his knee | his back, the crimson chlamys over hunched shoulders | 9: half up, hands on his knees, head lifting; 10: standing facing down, his ordinary look |

- **The stump is the map's.** His seat is about 5 px above the tile's bottom and nothing under him is drawn, so put him on a low stump metatile (a cut top about 12 px wide).
- **He gets up** with `applymovement` `nurse_joy_bow` (it plays `ANIM_ICHOR_STAND_UP`, frames 9 then 10), then swap him to `OBJ_EVENT_GFX_ICHOR_KLEON` to walk (batch 1's swap recipe, under Poses above).
- **Place him with `MOVEMENT_TYPE_NONE`** and turn him to his seat at load (`turnobject` in `ON_WARP_INTO_MAP_TABLE` or `ON_FRAME`). A `FACE_*` movement type re-faces him the frame his movement ends, which sits him back down before the swap.

## Field objects (32×32)

All are in `graphics/object_events/pics/misc/ichor/`. Like batch 1's crows, they're 32×32 sprites centered on their tile, 8 px over each side.

| Constant | Sheet | Palette | Look | Use |
|---|---|---|---|---|
| `OBJ_EVENT_GFX_ICHOR_KLEON_BALLS` | `kleon_balls.png` (3 drawings) | cast | Six Poké Balls in a row, 6 px above the tile's bottom (the stump's top), none twitching | Face down: the row is centered on its tile. Face left: it runs left from the tile's right edge. Face right (mirrored): it runs right from the tile's left edge. So put it on the tile beside Kleon and face it away from him. Hide it when he sweeps them up. |
| `OBJ_EVENT_GFX_ICHOR_TEMPLE_HOUND` | `temple_hound.png` (11 frames) | folk | A lean white sighthound with pricked ears (pink inside) in a bronze collar: deep chest, tucked belly, long legs, a long low tail. Walking, the legs stride, and facing down the head turns side to side. | the sight hounds H1–H7: trainer-type objects, standard facings |
| `OBJ_EVENT_GFX_ICHOR_TEMPLE_HOUND_SLEEP` | the same sheet, frames 9–10 | folk | The hound asleep, curled nose to tail on the path; walking in place lifts an ear ("One ear twitches") | the seven sleeping hounds after `FLAG_BADGE05_GET` (a name of my own, not in BUILD.md) |
| `OBJ_EVENT_GFX_ICHOR_GOLDEN_HIND` | `golden_hind.png` (12 frames) | theoxenia | A chestnut doe with a pale throat, belly and tail, and branched gold antlers. Frames: 0–2 head up, 3–8 the bolt (stretched out, then bounding), 9–11 grazing with her head at the grass. | the Hunt for the Hind's clearings A, B and C |

**The hind's animations** (`sAnimTable_IchorHind`). A standing object shows its normal-speed walk animation paused on a standing step (`FaceDirection` in `event_object_movement.c`). So her normal walks hold her grazing frames there.
- **Placed or turned, she grazes.**
- **Move her with `walk_fast_*` or faster.** Those keep her head up between the bolt frames, so she runs head up and stands alert where the run ends, until a `face_*` puts her head down again. A normal-speed walk would flash her grazing between strides.
- **`nurse_joy_bow` (`ANIM_ICHOR_STARTLE`) throws her head up** facing down, the moment you touch her. On a `FACE_*` movement type she lowers it again as soon as the movement ends.

## Kallisto on the rock (`sAnimTable_IchorKallisto`)

- **Facing up she sits** on the rock looking at the sky (frame 9), as Cami sits facing up.
- **`nurse_joy_bow` (`ANIM_ICHOR_LOOK_DOWN`)** has her look down at you (frame 10) and holds it.
- **Place her with `MOVEMENT_TYPE_NONE`** and `turnobject` her up at load. A `FACE_*` movement type re-faces her the frame the look-down ends: south, which is her standing walker.
- **Don't `faceplayer` her while she sits:** facing down she stands.
- **After the battle** the overworld respawns her standing facing down, so "she climbs down off the rock" is a walk south.

## Part 10's other folk

Most need no new pixels:

| Who | Sheet |
|---|---|
| Mnaseas | `MNASEAS` (new, above) |
| Horkia (in black) | `ELDER_F`: the slice's old woman already wears near-black |
| Klymene, Nyktimos's mother | `ELDER_F` |
| Parthenopaios (the runner) | batch 1's `HERALD` |
| Nyktimos, Aroanios (the innkeeper) | `MAN` |
| Hippothoos | `CHARCOALER` |
| Kepheus, Pelasgos, Krotos | `HARVESTER` or `MAN`, `SHEPHERD`, `GOATHERD` |
| The Cave of Maia's priestess | `PRIESTESS` |

## Palette plan

No new tag. Each sheet is in an existing family:

| Tag | Sheets |
|---|---|
| `OBJ_EVENT_PAL_TAG_ICHOR_FOLK` (0x1135) | Huntress, Charcoaler, Phylonoe, the muleteer, the lamplighter, Mnaseas, both hounds |
| `OBJ_EVENT_PAL_TAG_ICHOR_CAST` (0x1134) | Kleon on the stump and his balls (Kleon's own colors, beside Iapetos and Alethea, also cast) |
| `OBJ_EVENT_PAL_TAG_ICHOR_THEOXENIA` (0x1136) | Kallisto and the golden hind |

- **Why theoxenia for these two.** The hind's antlers want a true gold over chestnut, and folk's ochre and gold sit too close. Kallisto's silver-gray and dark bearskin read better in its linen grays and dark wool than in folk's warm gray. In the temple, that is two Ichor tags: folk for the hounds, huntresses and Phylonoe, and theoxenia for the hind and Kallisto.
- **Measured in game:** all twelve new graphics ids stood in the bedroom at once. `sSpritePaletteTags` read `1200 1110 1135 1136 1134 FFFF…`: the weather, the player, folk, theoxenia and cast, **5 of 16 slots**.

## Deviations from SCRIPT.md

- **The muleteer** is `MULETEER_GOAD`, since batch 2 owns `MULETEER`. His three mules (Onotis recolored) and the hoof-cup jars aren't drawn: Onotis's follower sprite doesn't exist yet.
- **The hounds** aren't "one palette family with Lykopup's follower" either: there is no Lykopup follower yet. They're drawn new in folk white and bronze. Their ears are pricked, after the Laconian hounds of Greek vase painting; folded ears read as a goat in the front view.
- **The sleeping hound** is a second graphics id over the same sheet (`TEMPLE_HOUND_SLEEP`), because Part 5 swaps sight hounds for sleeping ones anyway.
- **Kallisto's walker** follows Part 10: she sits facing up and stands otherwise. Her seat faces you with her face tipped up, not her back, so "she looks down at the player" is a change of face, not a turn. Her bow is slung, not held: "a bow she never draws".
- **Kleon's stump** isn't in his sprite. It is the map's, as batch 1 left benches to the map.
- **Kleon's balls** sit on the tile beside him, since an object can't share his tile; the facing trick puts them against his side.
- **The Iapetos fade-in** (a 16-frame blend) isn't done: it's an OBJ blend register effect for the scene script, not art. Batch 1's `CHORUS_LEADER` is the sheet it fades.
- **The lamplighter's variants** aren't drawn: the lamp-trees light as he passes, and one lamplighter covers the dusk scene.

## Critique passes

**Walkers and objects** (rendered at 4–6× next to Kleon, Youth F, the Harvester, Kid F, the maenad and the herald, then in game)

1. **First draft.**
   - The charcoaler's rake was a box on a pole that read as a hook, and his gray cap with a black band was a hoplite's helmet. His red leather apron hid the gray tunic, and his brown forearms read as sleeves.
   - Kallisto's bearskin was a dark slab down her whole left side, a shield. Her folk chiton was plain white, not silver-gray. Her seated frames were a skin-colored blob.
   - The muleteer's wide gold cone was an Asian straw hat, not a pilos. The lamplighter's linen cap was a turban, and his flask was sky blue.
   - Kleon's front pose had his forearms in a block across his chest, as if he were hugging a box.
   - The hound's front view was a round head with big round ears, a bear or a pig. Its side view had stubby legs and a beak, and its walk frames were the standing frame moved.
   - The hind's side antlers were a gold starburst. Her walk frames were copies, and she had no grazing front or back view.
   - The huntress's quiver feathers sat against her cheek like an earring.
2. **Redraw.**
   - The charcoaler's cap is a soft rounded felt and the rake head a comb with tines. The apron is tan, and his arms are ink from the elbow, with soot on his cheek.
   - Kallisto moved to the theoxenia palette: a linen-gray chiton, and a 4 px dark-wool bearskin with a silver pin. Her braid is over her right shoulder, the bow's tips show at her hip and shoulder, and she stands a row taller. Her seated frames have cloth-covered knees, arms round her shins, sandals, and the bearskin spread behind.
   - The pilos is a narrow brown-ochre felt cone. The lamplighter has bare dark curls, a clay flask and a 2 px flame.
   - Kleon's forearms come down from his knees to hands clasped between them. Walking in place he sags lower.
   - The hound is a sighthound: a narrow head, a long neck, a deep chest, a tucked belly and long legs. Its legs stride fore and aft, and facing down its head turns.
   - The hind's antlers are two beams with tines. She has a stretched bolt, and her grazing frames lower her head to the grass in front of her body.
3. **Third pass, before game.**
   - The hound's front view now read as a goat, from its sideways folded ears, so its ears are pricked in every view, pink inside. Its sleeping curl read as a white loaf, so it has a pricked ear, a haunch line and a curled tail.
   - The hind's second bolt frame read as kneeling. It is now a bound: forelegs tucked, hind legs pushing off.
   - The hind's grazing front frame hid her body, so she shows her back over the lowered head with her forelegs spread. Her grazing back frame got a rounded back.
   - Two 32×32 sheets had standing paws on row 31 or 29; all now stand on row 30, with walk frames a pixel lower as the walkers have them.
4. **In game.**
   - All twelve render in the right palettes and turn through four facings.
   - Kallisto sits facing up and looks down on the bow. Kleon rises to standing. The hind grazes when placed, bolts when run, and throws her head up on the bow. The hound trots, and the sleeping hound curls.
   - The first in-game run showed that a standing object shows its walk animation paused, not its face animation. So a grazing loop with head-lifts can never play, and the hind's grazing moved into her normal-speed walk table.
   - The same run showed that a `FACE_*` movement type undoes the look-down and the rise. That gives the `MOVEMENT_TYPE_NONE` recipe above.

**Portraits** (3× next to Kleon, the Harvester, the Maenad, the Vintner and Thespis)

1. **First draft.**
   - The huntress read at once.
   - The charcoaler's black cap brim and dark beard framed his face like a balaclava, and his kiln was a brown ball.
   - Kallisto had a bowl-cut fringe and a startled face. Her braid vanished against her arm, her bow dangled like a whip, the bear's head on her shoulder was a smudge, and her collar was a white blob.
2. **Redraw.**
   - Kallisto's face is in profile, lifted to the sky, with her hair drawn back. Her braid is 4 px wide with plaits and a silver tie, down her breast to the girdle. The bear's head has round ears, an eye and a snout. The bow's upper limb rises over her far shoulder with its string, and the crescent pin is a crescent.
   - The charcoaler's cap has a felt edge, not a black brim.
3. **Fixes.**
   - The bow's lower limb by Kallisto's hand read as a walking stick, so only the slung upper limb shows.
   - The charcoaler's sideburns are gone, so his face reads as a face. His kiln was clipped into a box by the frame's edge; it is now a dome behind him.
4. **In game.** The Huntress's and Kallisto's battle intros: both pics read on the platform at 1×, and both names fit the box.

## In-game checks

A throwaway harness on `tools/ichor/tests/engine_build.sh`, the theoxenia check's technique, not committed. It spawns all twelve objects round the Quickstart player from a test blob in spare EWRAM, turns them down, left, up and right, and walks them in place. It then plays the three `nurse_joy_bow` animations and runs the hind and the hound. Nine checks pass: the seat, the graze, each animation's end frame, the hind's run and return to grazing, and the palette tags.

For the battle intros, a frame callback writes `TRAINER_CLASS_HUNTRESS` and `TRAINER_PIC_HUNTRESS` into Euadne's `gTrainers` rows, and `TRAINER_PIC_HIEROPHANT_KALLISTO` into Kallisto's, in the emulator's ROM copy. `trainerbattle_no_intro` then fights each. No party file changes.

`make` is green and `tools/ichor/smoke_test.sh` passes. The ROM is 22,573,756 B (67.28%), 36,416 B more than the batch's start, mostly the sheets: the walkers at 2,304 B, the 32×32 sheets at 512 B a frame.

## Still open

- **Not drawn:** the three mules and the hoof-cup jars (waiting on Onotis's follower), Skylaps's and Kerdovix's objects (the dex's follower sprites), Alethea kneeling with Skylaps leaning on her, the lamplighter's variants, and the Iapetos fade.
- **The stump metatile and Kallisto's rock** are the arkadia and artemis agents'. The sprites assume a low flat stump and a flat rock top under her tile.
- **Not opened in Porymap:** the entries follow the slice's format exactly, so they should display.
