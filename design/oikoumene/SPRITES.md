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
