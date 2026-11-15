# The Oikoumene: sprites

Batch 1's people, for `BUILD.md` §5's sprites row. The trainer pics and classes are below; the overworld sprites are the overworld agent's, under "Overworld".

## Trainer pics

Eleven new trainer classes, five champions' titles as classes, and four named pics: Prince Hektor, Pharaoh Proteus, Medea and Helen of Sparta. Each pic is a 64×64, 16-color Gen 3 front pic in the slice's hand (`design/phase1/SPRITES_classes.md`): a 3/4 view toward the player's side, lit from the top left, with ink outlines and a share of black-figure ornament. Color 0 is transparent and each palette is embedded in its PNG.

- **Source:** `tools/ichor/art/sprites_oikoumene_trainers.py`. `--write` rebuilds the PNGs and the review sheet; `--preview DIR` writes a 3× sheet, 6× singles and pixel grids.
- **Review sheet:** `design/oikoumene/img/trainers_batch1.png`, 2×, on the grass battle background, with five of the slice's pics on the top row for scale.
- **In battle:** `tools/ichor/tests/oikoumene_trainer_pics.sh` writes each class's intro screen and a contact sheet, `build/test_oik_trainers/intros.png`.

### For the lead: the constants

Parties written with a stand-in class carry `# ICHOR_STUB_CLASS: <name>`. Swap each for the `Class:` and `Pic:` lines below. `trainerproc` upper-cases the string and turns spaces into underscores, so each `Class:` string is exactly its constant's tail.

| Class | `Class:` | Constant | Label | Prize ×, ball | `Pic:` | Pic constant | Suggested `Music:` |
|---|---|---|---|---|---|---|---|
| Trojan Hoplite | `Trojan Hoplite` | `TRAINER_CLASS_TROJAN_HOPLITE` | HOPLITE | 10, Great | `Trojan Hoplite` | `TRAINER_PIC_TROJAN_HOPLITE` | Intense |
| Charioteer | `Charioteer` | `TRAINER_CLASS_CHARIOTEER` | CHARIOTEER | 12, Fast | `Charioteer` | `TRAINER_PIC_CHARIOTEER` | Cool |
| Shepherd of Ida | `Shepherd of Ida` | `TRAINER_CLASS_SHEPHERD_OF_IDA` | SHEPHERD | 5, Poké | `Shepherd of Ida` | `TRAINER_PIC_SHEPHERD_OF_IDA` | Male |
| Argonaut | `Argonaut` | `TRAINER_CLASS_ARGONAUT` | ARGONAUT | 12, Dive | `Argonaut` | `TRAINER_PIC_ARGONAUT` | Cool |
| Colchian Sorceress | `Colchian Sorceress` | `TRAINER_CLASS_COLCHIAN_SORCERESS` | SORCERESS | 10, Moon | `Colchian Sorceress` | `TRAINER_PIC_COLCHIAN_SORCERESS` | Suspicious |
| Chalybes Smith | `Chalybes Smith` | `TRAINER_CLASS_CHALYBES_SMITH` | SMITH | 10, Heavy | `Chalybes Smith` | `TRAINER_PIC_CHALYBES_SMITH` | Hiker |
| Priest of the Sun | `Priest of the Sun` | `TRAINER_CLASS_PRIEST_OF_THE_SUN` | SUN PRIEST | 12, Ultra | `Priest of the Sun` | `TRAINER_PIC_PRIEST_OF_THE_SUN` | Intense |
| Scribe of Thoth | `Scribe of Thoth` | `TRAINER_CLASS_SCRIBE_OF_THOTH` | SCRIBE | 10, Repeat | `Scribe of Thoth` | `TRAINER_PIC_SCRIBE_OF_THOTH` | Suspicious |
| Embalmer | `Embalmer` | `TRAINER_CLASS_EMBALMER` | EMBALMER | 10, Dusk | `Embalmer` | `TRAINER_PIC_EMBALMER` | Suspicious |
| Nile Boatman | `Nile Boatman` | `TRAINER_CLASS_NILE_BOATMAN` | BOATMAN | 8, Net | `Nile Boatman` | `TRAINER_PIC_NILE_BOATMAN` | Hiker |
| Phoenician Trader | `Phoenician Trader` | `TRAINER_CLASS_PHOENICIAN_TRADER` | TRADER | 20, Luxury | `Phoenician Trader` | `TRAINER_PIC_PHOENICIAN_TRADER` | Rich |
| Prince (Hektor) | `Prince` | `TRAINER_CLASS_PRINCE` | PRINCE | 30, Ultra | `Prince Hektor` | `TRAINER_PIC_PRINCE_HEKTOR` | Elite Four |
| Pharaoh (Proteus) | `Pharaoh` | `TRAINER_CLASS_PHARAOH` | PHARAOH | 30, Luxury | `Pharaoh Proteus` | `TRAINER_PIC_PHARAOH_PROTEUS` | Elite Four |
| Priestess (Medea) | `Priestess` | `TRAINER_CLASS_PRIESTESS` | PRIESTESS | 30, Moon | `Priestess Medea` | `TRAINER_PIC_PRIESTESS_MEDEA` | Elite Four |
| Queen (Helen) | `Queen` | `TRAINER_CLASS_QUEEN` | QUEEN | 30, Luxury | `Queen Helen` | `TRAINER_PIC_QUEEN_HELEN` | Elite Four |
| King (Croesus, Memnon, Arganthonios) | `King` | `TRAINER_CLASS_KING` | KING | 40, Luxury | none yet | each king's own, in his batch | Elite Four |

- **Shared labels** (PG-39): the Trojan Hoplite shows HOPLITE and the Shepherd of Ida shows SHEPHERD, like the slice's Aethos classes, but they are classes of their own with their own pics, prize money and balls.
- **Label widths** (`tools/ichor/text_width.py`): 24 px (KING) to 60 px (CHARIOTEER), the same as HIEROPHANT's 60. The intro line wraps itself at 208 px, so "You are challenged by CHARIOTEER KEBRIONES!" breaks onto two lines on its own.
- **Prize money** is `4 × the last Pokémon's level × the multiplier` (`GetTrainerMoneyToGive`). At Lv 74 a Hoplite pays ¥2,960, a Trader ¥5,920 and a champion ¥8,880–9,120; a king at Lv 77 pays ¥12,320. The slice's are 4–25.
- **Balls** follow the expansion's per-class balls (`B_TRAINER_CLASS_POKE_BALLS`). The Shepherd of Ida keeps the Poké Ball like the slice's classes.
- **Music, per class.** `GetBattleBGM` plays the Hierophants' theme, `MUS_ICHOR_BATTLE_RIVAL`, for the five titles, tagged `ICHOR_STUB_MUSIC` until the music agent's *Battle! Champion of the Periodos* has a song id; every other class falls through to the region's trainer theme (the chart agent's branch). The titles win with the Hierophants' victory fanfare (`HandleEndTurn_BattleWon`).
- **Encounter music** is per trainer (`Music:`), not per class; the last column is a suggestion from the Hoenn classes each one resembles.
- **Trainer slides.** `sTrainerSlides` (`src/trainer_slide.c`) is keyed by trainer id, not class, and is empty for every Ichor trainer, the slice's included. A champion's last-Pokémon line goes there, by trainer id, when its hall is built.
- **Battle background.** The titles don't take the Hierophants' hearth background (`battle_bg.c`): each hall has its own look, so they fight on their map's environment.
- **Portraits.** Ichor has no dialogue-portrait system: `setspeaker` shows a name box only, and the theoxenia's "portraits" are trainer front pics. Hektor's, Proteus's, Medea's and Helen's pics are their portraits.

### The pics

Each land's people are drawn the way Greek painters drew foreigners on their own pots (OIKOUMENE §7): Trojans as Greeks, with Phrygian caps and patterned sleeves for Paris's kind; Colchians in the patterned, long-sleeved dress of Medea on South Italian vases; Egyptians with shaved heads or wigs, kohl, white linen and broad collars, in the red-brown both the Egyptians and the Greeks painted Egyptian men. Every pic carries some black-figure: a figure or band painted in ink on clay, or clay on black.

| Pic | Look | Palette |
|---|---|---|
| Trojan Hoplite | A gate guard of Ilion: a bronze Attic helmet worn down with a tall blue crest on a stilt, a round shield braced toward you with Troy's horse painted on it in black-figure, a bronze cuirass and blue chiton, the spear grounded at his side. The Aethos Hoplite's mirror: shield left, spear upright, blue not crimson | Bronze, Trojan blue, clay |
| Charioteer | Kebriones's kind, after the Delphi charioteer: a long fluted white chiton girt high, crossed straps with a gold boss, a blue fillet with its ends flying, curls; both fists on the reins, which run off toward his team, and the goad up behind | White, blue, gold |
| Shepherd of Ida | Paris's kind as the vase painters dressed him: a red Phrygian cap with its peak falling forward and lappets at the cheeks, a saffron tunic and blue trousers in diamond-work and zigzags, a short throwing-crook, and a golden apple held up | Red, saffron, blue |
| Argonaut | A veteran of the Argo: a felt pilos, a gray-shot beard, an exomis off one shoulder with a black hem band and a running wave, a sea-green chlamys, a coil of rope, an oar upright with its blade high | Felt, oatmeal, sea green |
| Colchian Sorceress | One of Medea's acolytes: a purple veil drawn over her head with a gold band at the brow, a teal long-sleeved gown with gold dots and a black zigzag hem, a bronze pyxis of herbs and a green sprig smoking in her raised hand. Gold-lidded eyes | Teal, purple, lime, bronze |
| Chalybes Smith | Iron country: a felt cap, a black beard and a grin, a leather apron, soot; the hammer on his shoulder and a glowing bar of iron held out in the tongs, throwing sparks. Iron gray, not bronze | Leather, iron, white-hot |
| Priest of the Sun | A priest of Heliopolis: a shaved head, kohl, the leopard skin of his office over white linen, a broad collar, his palm raised to the sun's gold disk on its staff, and sun disks in clay on a black hem | Linen, leopard, gold, lapis |
| Scribe of Thoth | A short black wig, kohl, a broad collar and a white kilt; an open papyrus of riddles in hieroglyphs held out, a reed pen behind his ear, the scribe's palette with its red and black wells under his arm | Linen, papyrus, lapis, malachite |
| Embalmer | Anubis's black jackal mask pushed up on his head, ears high and snout forward, gold-banded; white linen, a roll of bandage unspooling between his hands, a file of recumbent jackals on the hem, and violet wisps drifting off | Linen, black, gold, violet |
| Nile Boatman | A blue-striped headcloth, kohl and a grin, a white kilt with a rope belt and a papyrus reed, a punting pole with its forked foot dripping, and the day's fish hung on the pole | Linen, blue, wood |
| Phoenician Trader | From the Tyrians' Camp: a robe of the reddish purple Tyre is named for, gold-belted, fringed over a black band of running spirals; a white conical cap, a curled black beard, gold in his ear, a bolt of striped linen on his hip, and a bronze balance held up for you, a coin in its pan | Tyrian purple, gold, white |
| Prince Hektor | Hektor of the shining helmet, as his son saw it (*Iliad* 6.466–473): the bronze helmet with cheek pieces raised and the nodding horsehair crest on a tall stilt, its tail down his back; a full beard, a royal blue cloak with a meander hem, a bronze cuirass, the great ringed bronze shield of Troy and a long spear | Bronze (4), royal blue, crest gray |
| Pharaoh Proteus | Egyptian royal dress as the Greeks drew it: the gold-and-lapis striped nemes with the cobra at the brow, a braided lapis beard, a broad collar of lapis, gold, carnelian and turquoise, the pleated kilt with its gold apron, the crook over his shoulder. Playful: he winks, grinning, and holds up Homer's lion as a gold mask on a stick | Gold, lapis, linen |
| Priestess Medea | Priestess of Hecate as the vase painters drew her: a tall gold diadem, long black hair, a purple gown with gold dots and a black hem band of gold meander; a bronze ladle of the brew that makes old things young, dripping green. Curious, and a little dangerous: one brow up, a small smile, her fingers at her chin | Purple, gold, black, green |
| Queen Helen | Helen of Sparta, who sat out the war in Memphis and never went home ("Sparta's cold"): golden hair in a knot with a lapis diadem, a white chiton under a Spartan crimson himation, an Egyptian broad collar and gold armlets. She holds up a bronze mirror: everyone wanted a copy of her | Gold hair, white, crimson, lapis |

### Render-and-critique passes

**Calibration (the Troad only).** Four pics drafted against the slice's Hoplite and Shepherd.
- A legend clash drew blue outlines round two faces ('b' meant both blue and the outline). All fifteen faces now start from one shared face patch (`FACE_M`, `FACE_F`, `FACE_BEARD`, `FACE_KOHL`) with hair and headgear drawn over it, so every face is in the slice's hand: 16 wide, eyes looking left, light from the top left.
- Troy's horse read as a dog. Redrawn as a black-figure protome: ears, an incised eye, a mane line in clay, the neck down to the chest.
- The Phrygian cap read as a hood. Redrawn with its peak falling forward over the brow.
- Hektor read as the Trojan Hoplite with a beard. He got the dark horsehair crest with a tail down his back, cheek pieces raised so his face shows, the ringed bronze shield and the spear on the other side.

**Pass 1, the full sheet.**
- *Silhouette.* Every pic has its own shape: the round clay shield, the white column with reins, the falling cap and apple, the oar, the hammer and sparks, the sun staff, the papyrus, the jackal, the slanting pole, the balance, the crest and great shield, the diadem and ladle, the nemes and lion mask, the mirror. Nothing reads as Hoenn.
- *Readability.* The Hoplite's left pupil merged into his cheek piece: face moved a pixel right inside the helmet. The Shepherd's cap hair sat over his brows and his lappets ate half his face: lappets thinned and the face moved. Mouths were dots: each now has a clean shape (a set line, a smile, or a grin with teeth). The sorceress's cone read as a fairy-tale witch's hat. The jackal mask read as a cat. The trader's fist floated off his balance. Medea's far hand floated at her shoulder.
- *Black-figure.* The Troad and Black Sea had ornament (the horse, meanders, diamond-work), but the Egyptians had none. Added black hem bands with clay motifs: sun disks for the priest, a file of recumbent jackals for the embalmer, running spirals for the trader.
- *Fixed:* all of the above; the sorceress got a soft cap, the jackal ears and a forward snout, the balance hangs from the trader's fist, Medea's fingers come to her chin; the reins got a sag, the Argonaut's rope a loop, the smith's apron its folds, Proteus's lion mask a mane of points, Helen a larger mirror.

**Pass 2, the full sheet at 1×, 2× and 3×.**
- *Silhouette.* All fifteen still separate at 1× on the battle background, the size a player sees them.
- *Readability.* Three pics were purple: the sorceress, Medea and the trader. The soft cap still read as a wizard's. The reins were too faint to see at 1×.
- *Black-figure.* The Argonaut had none, nor did the three men in kilts (pass 3).
- *Fixed:* the sorceress now wears a purple veil drawn over her head, with a gold band at the brow, over a teal gown with gold dots and a black zigzag hem, so she sits apart from Medea's purple and gold; the trader's purple is redder, the real Tyrian; the reins are two-strand lines with a sag; the Argonaut's hem got a black band with a clay running wave.

**Pass 3, the full sheet and in battle.**
- *Silhouette and readability.* The three purples now read as three people. Faces hold at 1×: kohl reads on all five Egyptians, the wink on Proteus, the smile on Helen. The champions read as grander than their lands' classes (Hektor's crest and shield fill the frame; Medea's diadem and hem; Proteus's nemes; Helen's gold).
- *Black-figure.* The scribe's, the boatman's and Proteus's kilts had none; each got a black hem band with a clay zigzag, or gold either side of Proteus's apron. Thirteen of fifteen now carry a black-figure band or figure. The Charioteer (after the plain Delphi bronze) and the Chalybes Smith carry their pattern in ink instead: crossed straps, soot.
- *Consistency with the slice.* Same ink, same outline rule (an outline color per figure, ink on metal and beards), same proportions (a 20 px head on a 61 px figure, feet on row 61), same light.
- *Left as they are:* the sorceress's gold-lidded eyes (eerie, which suits her); Helen's mirror reads as a bronze disk on a handle, which is what a Greek mirror is.
- *In battle* (`build/test_oik_trainers/intros.png`): all sixteen intros read on Ichor's temple battle background, with the pottery message box. The pics sit on the opponent's dais at the size the sheet shows at 1×. The game keeps the label and the name together with a non-breaking space, so a long pair moves to the second line whole: "You are challenged by / CHARIOTEER KEBRIONES!".

### Tests

`tools/ichor/tests/oikoumene_trainer_pics.sh` (with `.lua`, `.c`, `.s` and `.py`) runs one battle per new class on the headless runner:
- The stand-in is the slice's TITYROS. For each battle the test rewrites his class, pic and name in the emulator's copy of the ROM (the cart0 memory domain), so nothing in the ROM file or `trainers.party` changes. It checks first that it has found his entry: `gTrainers` is `[DIFFICULTY_COUNT][TRAINERS_COUNT]`, and the game reads the normal row.
- For each class it checks the label in `gTrainerClasses`; that the intro line reads "You are challenged by LABEL NAME!" (names from PERIODOS's halls where there are any: AGENOR, KEBRIONES, PARIS, KYTAIA, AKMON, MANETHO, IMOUTHES, THONIS, ITHOBAL); and that the pic's own palette, read from its PNG, is in OBJ palette RAM. It also takes a screenshot of the intro.
- KING has no pic yet, so its battle (KING PRIAM) uses Hektor's.

**Result** (2026-11-14): `OIKTR PASS: 82 checks, 16 screenshots`. `make` is green and `tools/ichor/smoke_test.sh` passes (9 screenshots).

**ROM:** 22,191,564 B before, 22,202,476 B after (66.14% → 66.17%), +10,912 B for fifteen pics and their tables.
## Overworld

Batch 1's walking sprites: the named people, townsfolk and trainer classes of the Troad, Egypt and the Black Sea (OIKOUMENE §4.1, §4.3, §4.5, §6). They are 27 standard 16×32 walkers with Ichor's nine frames, on sprites_folk.py's bodies, so they keep Aethos's proportions, outline and step bob. Foreigners look foreign, drawn by the same painter.

- **Source:** `tools/ichor/art/sprites_oikoumene_ow.py`. Every head, costume and prop is ASCII art in that file.
- **Rebuild the sheets and palettes:** `python3 tools/ichor/art/sprites_oikoumene_ow.py --write`
- **Review sheets:** `--preview DIR` writes each land at 4× on grass, `--sheet PNG` writes all 27 at 2× (`img/overworld_batch1.png`), and `--grids DIR` writes 8× pixel grids for editing.
- **Sheets:** `graphics/object_events/pics/people/ichor/oik/<name>.png`, registered in the five sprite tables' Ichor blocks (SPRITES_npc.md §"How a later batch adds an NPC").
- **Test:** `tools/ichor/tests/oikoumene_ow_sprites.sh` (below).

### Stopped at (2026-11-14, Oikoumene paused)

- **Done.**
  - All 27 walkers are drawn and written. The three land palettes are at tags 0x1146–0x1148.
  - Every id is registered in the five sprite tables and the palette table.
  - The headless check passes: 258 checks.
  - The stand-in table and the 2× sheet below are written.
  - Review passes 1 and 2 are written up below.
- **Partial.** Pass 3, the in-game look, is not done. The check's 21 screenshots of Akti are taken (`build/test_oikoumene_ow/shots/`) but haven't been reviewed or cropped into a design image.
- **Not started.** Nothing else was asked of this batch. The smoke and slice tests were not run at the last commit.
- **Make** is green at the last commit (ROM 22,255,180 B, 66.33%).

![All 27 at 2x](img/overworld_batch1.png)

### Stand-ins to swap

Map agents placed stand-ins tagged `ICHOR_STUB_SPRITE`. Swap each for its constant.

| Stand-in | Constant | Palette |
|---|---|---|
| Hero of Sestos, the lamp-keeper | `OBJ_EVENT_GFX_ICHOR_HERO_LAMPKEEPER` | Troad |
| King Priam | `OBJ_EVENT_GFX_ICHOR_PRIAM` | Troad |
| Cassandra | `OBJ_EVENT_GFX_ICHOR_CASSANDRA` | Troad |
| Prince Hektor | `OBJ_EVENT_GFX_ICHOR_HEKTOR` | Troad |
| Odysseus (Ilion's guest-room) | `OBJ_EVENT_GFX_ICHOR_ODYSSEUS` | Troad |
| A Trojan man; the ferryman, the horse-breeder, the mason | `OBJ_EVENT_GFX_ICHOR_TROJAN_M` | Troad |
| A Trojan woman; the peplos-weaver, the mason's wife | `OBJ_EVENT_GFX_ICHOR_TROJAN_F` | Troad |
| Trojan Hoplite (trainer); the Skaian Gate's guard | `OBJ_EVENT_GFX_ICHOR_TROJAN_HOPLITE` | Troad |
| Charioteer (trainer) | `OBJ_EVENT_GFX_ICHOR_CHARIOTEER` | Troad |
| Shepherd of Ida (trainer) | `OBJ_EVENT_GFX_ICHOR_SHEPHERD_IDA` | Troad |
| Pharaoh Proteus | `OBJ_EVENT_GFX_ICHOR_PROTEUS` | Egypt |
| Helen of Sparta | `OBJ_EVENT_GFX_ICHOR_HELEN` | Egypt |
| An Egyptian man; the Apis keepers, the precinct's guard | `OBJ_EVENT_GFX_ICHOR_EGYPTIAN_M` | Egypt |
| An Egyptian woman; the egg-oven keeper | `OBJ_EVENT_GFX_ICHOR_EGYPTIAN_F` | Egypt |
| Priest of the Sun (trainer); Heliopolis's sun-priest | `OBJ_EVENT_GFX_ICHOR_SUN_PRIEST` | Egypt |
| Scribe of Thoth (trainer); Memphis's scribe | `OBJ_EVENT_GFX_ICHOR_SCRIBE` | Egypt |
| Embalmer (trainer); Memphis's embalmer | `OBJ_EVENT_GFX_ICHOR_EMBALMER` | Egypt |
| Nile Boatman (trainer) | `OBJ_EVENT_GFX_ICHOR_NILE_BOATMAN` | Egypt |
| Phoenician Trader (trainer); the incense merchant | `OBJ_EVENT_GFX_ICHOR_PHOENICIAN` | Egypt |
| King Aietes | `OBJ_EVENT_GFX_ICHOR_AIETES` | Black Sea |
| Medea | `OBJ_EVENT_GFX_ICHOR_MEDEA` | Black Sea |
| Phineus | `OBJ_EVENT_GFX_ICHOR_PHINEUS` | Black Sea |
| A Colchian man; Phrixos's sons, the bird-catcher, the palace guard | `OBJ_EVENT_GFX_ICHOR_COLCHIAN_M` | Black Sea |
| A Colchian woman; the linen-weaver | `OBJ_EVENT_GFX_ICHOR_COLCHIAN_F` | Black Sea |
| Argonaut (trainer) | `OBJ_EVENT_GFX_ICHOR_ARGONAUT` | Black Sea |
| Colchian Sorceress (trainer) | `OBJ_EVENT_GFX_ICHOR_SORCERESS` | Black Sea |
| Chalybes Smith (trainer); the palace workshop's smith | `OBJ_EVENT_GFX_ICHOR_CHALYBES_SMITH` | Black Sea |

The households in the second column are suggestions, so that no house needs a sprite batch 1 doesn't have.

### Who they are

| Constant | Look |
|---|---|
| `HERO_LAMPKEEPER` | Golden hair blown out by the strait's wind, a night-blue peplos with a linen girdle, and a clay lamp cupped at her waist, lit |
| `PRIAM` | White hair and long beard under a gold band, a royal purple robe with a gold key hem, a gold-headed sceptre |
| `CASSANDRA` | Loose black hair with a purple sheen, a gold fillet, wide blue-lit eyes, a white peplos and a red himation |
| `HEKTOR` | A bronze helmet with cheek-pieces and a tall red horsehair crest, a bronze cuirass over royal purple, greaves, spear, and a purple shield with a gold boss |
| `ODYSSEUS` | A felt pilos, a dark beard, a white chiton and a blue chlamys pinned with a gold brooch |
| `TROJAN_M` | A red Phrygian cap with lappets, a wheat-gold tunic, blue sleeves and trousers: the Trojan as Greek painters drew him |
| `TROJAN_F` | A red veil with a gold border, a blue sleeved dress with a gold girdle and hem |
| `TROJAN_HOPLITE` | A bronze helmet with a short white crest, a linen corselet over river blue, greaves, spear and a blue shield |
| `CHARIOTEER` | The Delphi charioteer: short curls under a red fillet whose ends fly behind, a long white xystis with crossed red straps, a goad |
| `SHEPHERD_IDA` | Paris's trade: a purple Phrygian cap, a white fleece, a bronze-brown tunic and a crook |
| `PROTEUS` | The striped nemes with the uraeus, a false beard, a broad collar, bare chest, a white kilt with a gold apron, the striped crook |
| `HELEN` | Golden hair in a knot with a lapis ribbon, fair skin, a white peplos and a lapis himation: Greek dress among the Egyptians |
| `EGYPTIAN_M` | A black bob wig, kohl, a broad collar of malachite, gold and lapis, a bare chest and a white kilt |
| `EGYPTIAN_F` | Lighter-skinned, as the tomb painters drew women: a long black wig with a lapis band and a lotus, a collar, a white sheath dress |
| `SUN_PRIEST` | A shaved head, kohl, a leopard skin over a long white robe, and a staff crowned with the red sun disc |
| `SCRIBE` | A black wig with a reed pen behind the ear, a white shirt and mid-calf kilt with a lapis sash, a papyrus roll, his red-and-black palette |
| `EMBALMER` | Anpu's jackal mask, black with gold eyes and the striped headcloth behind, a long white robe, a roll of bandage linen |
| `NILE_BOATMAN` | A linen headcloth with a malachite band, a bare sun-darkened chest, a short kilt, bare feet, and a punting pole taller than him |
| `PHOENICIAN` | A tall purple cone of a cap, black curls and a curled beard, a robe of phoinix red (his name is the colour he sells), a jar on his hip |
| `AIETES` | Son of Helios: a crown of gold rays, black curls and beard, a long robe of gold and bronze, a wine-red cloak, a gold sceptre |
| `MEDEA` | The moon to her father's sun: a gold crescent on a night-purple veil, a long-sleeved wine-red robe with a gold girdle and hem, Hecate's torch |
| `PHINEUS` | Wild white hair and beard, eyes closed, a worn linen robe under a night-purple mantle, a staff, and the dove on his hand |
| `COLCHIAN_M` | Tight black curls and beard (Herodotus 2.104), a sea-green tunic with linen sleeves, a bronze belt, brown leggings |
| `COLCHIAN_F` | A veil of Colchian linen, bronze earrings, a sea-green dress with a wine-red sash and hem |
| `ARGONAUT` | A Greek veteran of the Argo's bench: brown curls and beard, a white exomis, a red chlamys, an oar blade-up |
| `SORCERESS` | A sea-green hood and mantle with gold eyes in its shadow, a night-purple dress, a bronze phial |
| `CHALYBES_SMITH` | A tan felt pilos, black curls and beard, a sooty linen exomis under a leather apron, an iron hammer |

### Palette families

One palette per land, shared by its townsfolk, its classes and its named people, so a land's map spends one OBJ palette slot on all of them. Each sheet's PNG embeds its palette; change a colour in the `*_COLORS` lists and re-run `--write`.

| Palette | Tag | File | Walkers | Colours |
|---|---|---|---|---|
| Troad | `OBJ_EVENT_PAL_TAG_ICHOR_TROAD` 0x1146 | `ichor_troad.pal` | the ten Troad walkers | ink, brown, two skins, linen, gray, bronze, gold, Trojan red (2), river blue (2), royal purple (2) |
| Egypt | `OBJ_EVENT_PAL_TAG_ICHOR_KEMET` 0x1147 | `ichor_kemet.pal` | the nine Egypt walkers, the Phoenician among them | ink, brown, three skins in one chain, linen, gold (2), lapis (2), malachite (2), carnelian, Tyrian purple |
| Black Sea | `OBJ_EVENT_PAL_TAG_ICHOR_PONTOS` 0x1148 | `ichor_pontos.pal` | the eight Black Sea walkers | ink, brown, three skins in one chain, linen, bronze, gold, iron, sea green (2), wine, flame, Hecate's night |

- **Skin chains.** Egypt's and the Black Sea's palettes hold three skin tones in a row, dark to light, so two ramps share a colour. Egyptian men use the darker pair and women and Helen the lighter, the way Egyptian painters told them apart. Colchians use the darker pair and the Greeks among them (the Argonaut, Phineus) the lighter.
- **Tags.** The Oikoumene's ten lands take 0x1146–0x114F, from the top of Ichor's 0x1134–0x114F, so they never collide with the Aethos sessions counting up from 0x1136 (main has 0x1136, Act II's branch 0x1137). Batches 3–5 take 0x1149 onwards, one per land.
- **Budget.** All of a land's people cost its maps one OBJ slot of sixteen, beside the player's, the follower's and the field effects'; Alethea's quay scene adds the cast palette for its length. The Phoenician Trader wanders (OIKOUMENE §6): placed outside Egypt he costs that map a second land slot.
- **Role letters.** The tool adds two role pairs to sprites_folk's bodies: A/Z for the arms (sleeves or skin) and G/J for the rest of the skin. Sleeves and a land's skin tone are a role mapping, not a redraw, and X/Y (shins) default to the skin, so trousers and greaves are roles too.

### Review passes

Passes 1 and 2 looked at the full sheets (every walk frame and facing) at 4× on grass and at 2× together. Pass 3 is to look at them in game on Akti's agora.

**Pass 1: first drafts, 4× sheets.**
- Hero's windblown hair read as comb teeth, and her lamp was too small to read as a lamp.
- Cassandra's back view was speckled with purple noise.
- Hektor's and the Trojan Hoplite's helmets, flat bronze, read as brown hair, and their faces looked small and lost.
- The Trojan woman's back view was a solid red blob.
- The Shepherd of Ida's gold cap read as blond hair.
- The Charioteer's goad and every spear shaft, dark wood beside the outline, vanished.
- The boatman's green headcloth read as green hair.
- Medea's pointed purple cap read as a party hat.
- The Colchian woman's sea-green veil was the Sorceress's hood again.
- The Argonaut's gold oar blade read as a torch.
- The Smith's brown cap melted into his black curls; his hammer was a gray block.

**Pass 2: fixes, 4× and 2× sheets.**
- Hero's hair now streams in one swept mass with two highlight strands, and the lamp has a three-row flame over a white girdle.
- Cassandra's hair falls in two wavy strands.
- The helmets are shaded lit-to-shade (gold, bronze, brown) with an ink brim over the face and shaded cheek-pieces, so they read as metal.
- The Trojan veil ends in a gold border at the shoulders.
- The Ida cap is royal purple: a prince's shepherd.
- Spear shafts and the goad are bronze-tan wood.
- The boatman wears a linen khat with a malachite band.
- Medea wears a night veil with a gold crescent at the brow: the moon to Aietes's sun-ray crown.
- The Colchian woman's veil is linen over a sea-green dress.
- The oar is wood.
- The Smith's pilos is tan felt and his hammer has a lit iron face.

**Between passes 2 and 3**, at 5× and 10×:
- Phineus's dove grew into a readable bird.
- The Scribe's papyrus roll turned papyrus-yellow, so it no longer vanishes against his white shirt.
- The Trojan woman's head was re-centred: it sat a pixel right, and her earring poked out of the outline.
- A sweep confirmed every other head is centred; Hero's is off-centre on purpose, her hair blown out by the wind.

**Pass 3: in game.** Not done yet. The test's 21 screenshots (`build/test_oikoumene_ow/shots/`) are the material for it.

### Test

`tools/ichor/tests/oikoumene_ow_sprites.sh` (Lua on `tools/ichor/mgba_headless.c`; test scripts assembled into spare EWRAM, nothing in the ROM patched):

1. A lead Pokémon, so a follower walks, then a warp to Akti beside the Agora, with Akti's own people and props removed.
2. For each land: every walker spawns from its graphics id in two rows round the player. The land's walkers must share one OBJ palette slot, holding exactly `ichor_<land>.pal`, which is neither the player's slot nor the follower's, and the player's and follower's colours must not change. All walk a square, two tiles each way, showing both walk frames of each direction (left 7/8, down 3/4, right 7/8 mirrored, up 5/6), and end where they began. Screenshots standing and mid-step each way.
3. Four of each land at once: three palettes in three different slots, none of them the player's or the follower's.

**Result, 2026-11-14: PASS**, 258 checks and 21 screenshots.
- Each land's walkers shared one slot: the Troad's and Egypt's were 2 and 3, and the Black Sea's was 2 again once the Troad's walkers had gone.
- With all three lands at once they took slots 2, 3 and 4, clear of the player and the follower.
- Every walker showed both walk frames in all four directions and finished the square where it began.

**ROM.** The batch adds 63,624 B (62.1 KiB), taking the ROM from about 22,191,556 B (66.14%) to 22,255,180 B (66.33% of 32 MB).

### Open

- **Odysseus is drawn here.** No `OBJ_EVENT_GFX_ICHOR_ODYSSEUS` existed on any branch. If the post-game session draws its own for the Olympiad, one of the two should go.
- **Trainer pics.** Hektor's, Proteus's, Medea's and Helen's portraits are being drawn alongside. The walkers' colours are listed above so the two can be matched; whichever changes, the other follows.
- **Mirrored props.** As for every Gen 3 NPC, the right-facing frames are the left ones flipped, so Hero's lamp, the spears and the staffs change hands facing right.
- **The rest of the Oikoumene's people** (Lydia, Libya, the North, Aithiopia, the Far West, the Western Sea and Okeanos; about 13 more for OIKOUMENE §7's 40) come with their batches, each with its land's palette in 0x1149 onwards.
