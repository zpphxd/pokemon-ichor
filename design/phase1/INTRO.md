# Boot sequence: the pot turns

From power-on to the title, the player now sees one painted pot. Emerald's Game Freak logo, Latios and Latias, the bike ride and the legendary trio are gone.

The sequence:

1. An honest **copyright card**.
2. The upstream **"powered by" card**, restyled.
3. The **studio mark**: a drop of ichor falls through the dark and blooms into ΙΧΩΡ.
4. The **cinematic**. Clotho spins, and her thread runs along a black-figure frieze of Aethos as the pot turns under the light. The camera follows it to the Fates' loom. Lachesis measures the warp and Atropos cuts it, until the shears reach the golden thread and stop.
5. A white cut to the **amphora title**, where the three Fates stand painted.

Stills are in `img/intro_*.png`. Contact sheets, one frame per 30, are `img/intro_sheet_cards.png`, `_studio.png`, `_frieze.png` and `_loom.png`. The key frames are `img/intro_keys.png`, and the skip check is `img/intro_skip.png`.

## The story it tells

The color code is the title's. White thread is a mortal life: Clotho spins it, Lachesis measures it, and Atropos cuts it. The **golden thread** is the player's, which the bible says was never spun.

The brief suggested Clotho spin a golden thread. Instead she spins white, and the golden thread comes from somewhere else. **It rises, unspun, from the roots of an olive in Elaia's grove**, the player's home, on the first beat of the music's second section. From there it runs beside the white thread across the world.

At the loom, Lachesis ties a red knot on every thread to mark where it will be cut. The golden thread gets none: her rod finds nothing to measure. Atropos cuts three threads, one per beat, and their weighted ends drop away. Then she opens her shears on the golden thread and stops. She trembles, makes one attempt to close, and opens again. The screen cuts to white, and the title fades in from white, as it was built to.

## Scenes

| # | Scene | Still | What happens |
|---|---|---|---|
| 1 | Copyright | `intro_1_copyright.png` | Black gloss between two meander rules. The first line reads "POKÉMON © NINTENDO / CREATURES / GAME FREAK". A small gold drop sits under it, then "ICHOR IS A FAN-MADE GAME, NOT AFFILIATED WITH THEM." It fades in from the BIOS white, as Emerald's card did. |
| 2 | Powered by | `intro_2_powered_by.png` | "POWERED BY" over a gilded V-cut **PRET × RHH**, captioned POKEEMERALD and EXPANSION, between meander rules. The upstream egg and Porygon sprites are left out of the pottery look. |
| 3 | Studio mark | `intro_3_studio_bead.png` to `intro_5_studio_mark.png` | A bead of ichor gathers at the top of the dark, swells, lets go and falls. On landing, the mark's drop flares white and cools to gold. A ripple spreads to a ring of **twelve gold dots** (the Twelve), and **ΙΧΩΡ** (*ichor* in Greek capitals) gilds in below. |
| 4 | Clotho | `intro_6_clotho.png` | The frieze fades in on Clotho, the title's own figure, beside her wool basket and labeled ΚΛΩΘΩ. Her drop spindle turns, and the white thread runs from her hand to the edge of the frame. |
| 5 | The grove of Elaia | `intro_7_grove.png` | The pot begins to turn. Three gnarled olives stand here, with Athena's owl (**Noctowl**) on a bough and two grazing **Mareep** (the Golden Fleece's flock). The golden thread rises from the third olive's roots, a spark running ahead of it. |
| 6 | The sea | `intro_8_sea.png` | A trireme sails under a white sail, with its painted eye and its ram. **Finizen** leap around it, as the dolphins do on Exekias's cup, and they dive behind the painted waves. **Gyarados** rears from the waves as the *ketos*, the sea serpent of Greek vases. Labeled ΘΑΛΑΣΣΑ. |
| 7 | The temple of the Twelve | `intro_9_temple.png` | A Doric temple in side view with **twelve columns**, a triglyph frieze and palmette acroteria. **Xatu**, the bird that watches past and future, stands on the roof corner like an acroterion. The altar fire flickers. Labeled ΝΑΟΣ. |
| 8 | Olympus | `intro_10_olympus.png` | Cypresses mark the road up. Olympus's snowy peaks rise through a white cloud bank, with the Twelve's seat on the summit. **Zapdos**, Zeus's thunder-eagle, calls the lightning three times, and the clay flashes each time. Labeled ΟΛΥΜΠΟΣ. |
| 9 | The loom: measure | `intro_11_measure.png` | The Fates' warp-weighted loom: two posts and a beam, a woven meander band, and seven warp threads. Six are white and weighted by clay loom-weights. The golden one hangs free, swaying, and is not woven in. Lachesis's rod steps along the warp, held in her white hand at the end of a black-sleeved arm, and ties a red knot on each white thread. On the golden thread it pauses and finds nothing, and the thread glints. Labeled ΛΑΧΕΣΙΣ and ΑΤΡΟΠΟΣ. |
| 10 | The loom: cut | `intro_12_cut.png` | Atropos's spring shears come in from the right and cut three threads at their knots, one per beat. Each cut end drops with its weight. |
| 11 | The hesitation | `intro_13_hesitate.png` | The shears open wide on the golden thread and tremble. They half close once and open again, and the thread sways harder and glints. |
| 12 | Title | `intro_14_title.png` | A cut to white, then the amphora title as before. |

## Timing sheet

The **intro clock** `t` counts frames from the studio card. It is `gIntroFrameCounter`, and `MUS_INTRO` starts at `t = 0`.

- The GBA runs at 59.73 frames per second.
- `MUS_INTRO` is 4/4 at 140 bpm, so a beat is 25.6 frames and a bar is 102.4 frames.
- Every scene change sits on a bar line of the current track: bar 5, bar 8, section B at bar 11, and section C at bar 21.
- The cues are the `T_*` constants at the top of the movie section of `src/intro.c`.

**Before the intro clock** (boot frames, from power-on):

| Boot frame | Length | Card | Skip |
|---|---|---|---|
| 0 | about 175 | Copyright, then a fade to black | Not skippable, as in Emerald (it hosts the GameCube link check) |
| about 200 | about 255 | Powered by: fade in, hold for 208 frames, fade out | Any key skips to the studio card, as upstream |
| 459 | | The studio card starts (`t = 0`) | |

**The intro clock:**

| t | Seconds | Bar.beat | Length | Cue |
|---|---|---|---|---|
| 0 | 0.00 | 1.1 | 410 | **Studio card.** `MUS_INTRO` starts. Darkness. |
| 24 | 0.40 | 1.1 | 62 | A bead of ichor forms at the top and swells. |
| 86 | 1.44 | 1.4 | 26 | The drop lets go and falls. |
| 112 | 1.88 | 2.1 | 24 | It lands. The mark's drop flares and the ripple spreads. |
| 124 | 2.08 | | 12 | The ring of the Twelve kindles. |
| 140 | 2.34 | | 40 | ΙΧΩΡ gilds in, then glints and holds. |
| 300 | 5.02 | | 32 | Fade to black. Black until 410. |
| **410** | 6.86 | **5.1** | 307 | **Clotho.** Fade in from black over 32 frames. The spindle turns. |
| 466 | 7.80 | | 234 | Her white thread runs from her hand to the frame's edge, finishing at 700. |
| **717** | 12.00 | **8.1** | 1273 | **The pot turns.** The pan eases in over 150 frames and reaches full speed (1.07 px a frame) at 867, under the timpani roll from bar 9 (819). |
| 923 | 15.45 | | | The grove is centered: Noctowl, Mareep. |
| **1024** | 17.14 | **11.1, section B** | 60 | **The golden thread rises** from the third olive's roots: a spark at 1024, then it runs to the frame's edge by 1084. |
| 1181 | 19.77 | | | The trireme is centered. Finizen leap every 80 frames. |
| 1371 | 22.95 | | | The ketos (Gyarados) is centered. |
| 1595 | 26.70 | | | The temple of the Twelve is centered. Xatu is on the roof. |
| 1717 | 28.75 | | | The altar fire. |
| 1779 | 29.78 | | | The cypresses. |
| 1880 | 31.48 | | 110 | The pan eases out onto Olympus and comes to rest at 1990. |
| 1894, 1936, 1972 | 31.7, 32.4, 33.0 | | 10 each | Zapdos's lightning: bolts, and the clay flashes. |
| 2032 | 34.02 | | 16 | Fade to white. |
| **2048** | 34.29 | **21.1, section C** | 102 | **The loom.** Fade in from white over 16 frames. |
| 2061 + 12.8k, k = 0–6 | 34.5 | the off-beat of 21.1 to the off-beat of 21.4, on eighth notes | | Lachesis's rod stands at thread k. A knot is tied 2 frames later, except on k = 3, the golden thread, which only glints. |
| 2142 | 35.86 | | 12 | The rod withdraws. |
| 2150 | 36.00 | 22.1 | 26 | Atropos's shears come in from the right. |
| 2176, 2201.6, 2227.2 | 36.4, 36.9, 37.3 | 22.2, 22.3, 22.4 | 10 each | Three cuts, a beat apart. The blades close about 2 frames before the beat, and the cut end falls from the beat. |
| **2253** | 37.72 | **23.1 (the crash)** | 73 | **The hesitation.** The shears open wide on the golden thread and tremble. They half close at 2293 to 2303 and glint at 2273 and 2305. |
| 2326 | 38.94 | | 16 | The cut to white. |
| **2342** | 39.21 | 23.4 | | **Title.** `CB2_InitTitleScreen` fades in from white and starts `MUS_TITLE`. |

The current `mus_ichor_intro` (A 10 bars, B 10, C 3; 39.4 s, ends near t = 2355) fits this sheet as cut: section B starts the golden thread and section C starts the loom. **For a recut**, the moments a score can hit are:

- the drop landing at 112
- Clotho at 410
- the turn at 717
- the golden thread at 1024
- the lightning at 1894, 1936 and 1972
- the loom at 2048
- the rod's seven steps on eighth notes from 2061
- the three cuts on beats at 2176, 2201.6 and 2227.2
- the hesitation at 2253
- the white cut at 2326

`MUS_INTRO` remains the placeholder slot.

## How it is built

The frieze is a pot turning under a fixed light. The clay band and its lighting (BG3) stay still. The black-figure painting (BG2) scrolls across them, so the figures pass under the highlight as a turning pot's do. The meander bands scroll too, since they are painted on the pot.

| Scene | Layer | Holds | VRAM |
|---|---|---|---|
| Studio | BG0 | `studio_mark.png`: the drop, the ring of twelve, ΙΧΩΡ. 54 tiles, one palette whose three groups `intro.c` lights separately. | char 0, map 31 |
| | OBJ | `studio_drop.png` (6 frames, 16x32), `studio_ripple.png` (6 frames, 64x64) | |
| Frieze | BG2 | `frieze.png` (633 tiles): the 1464 px painting, streamed into a 64-column map a column at a time as the camera moves | char 0-1, map 24-25 |
| | BG3 | The lit clay band and the band rules, still (`clay.bin`) | char 2, map 26 |
| | BG1 | Clotho's white thread (`frieze_white.bin`), shown through WIN1 while it grows | char 2, map 28-29 |
| | BG0 | The golden thread (`frieze_gold.bin`), shown through WIN0 while it grows, blended 12/8 to glow as on the title. Color 15 pulses. | char 2, map 30-31 |
| | OBJ | The spindle (7 frames), Finizen (3 frames, priority 3 so they dive behind the painted waves), the altar flame (3 frames), lightning (2 frames), sparkles | |
| Loom | BG2 | `loom.png` (62 tiles): posts, beam, woven band, the warp and its weights, the labels | char 0, map 24 |
| | BG3 | The clay band | char 2, map 26 |
| | BG0 | The golden thread (`loom_gold.bin`), blended 12/8 and swayed per scanline (an HBlank DMA into BG0HOFS that grows toward its free end) | char 2, map 30 |
| | OBJ | Lachesis's rod, hand and arm (6 sprites); Atropos's shears and arm (4); the knots; the cut ends with their weights (32x64); a sparkle. All at priority 0, in front of the golden thread. | |

- **Palettes.** Everything uses the title's colors (`tools/ichor/art/intro_lib.py`): black gloss, the clay ramp, added white, added red, and the thread golds.
- **Fades.** Every fade and flash is computed per frame on the intro clock: the faded buffer is rebuilt from the loaded palettes, then blended. `gPaletteFade` is never busy during the movie, so a key skips at any frame.
- **Shared palette.** `credits.c`'s THE END screen loads `copyright.png`'s palette. Colors 9, 13 and 15, the ones its letters use, are kept as a mid, a light and the brightest color, so it now reads cream on black gloss.

## Pokémon in the frieze

All are existing species, cast for the myth each scene tells:

- **Noctowl:** Athena's owl, in Elaia's olives.
- **Mareep:** the Golden Fleece's flock.
- **Finizen:** Exekias's dolphins.
- **Gyarados:** the *ketos*.
- **Xatu:** the seer, on the temple.
- **Zapdos:** Zeus's eagle, as in bible §4.

None is on the Lazarus avoid-list. If the Aethos dex later replaces them, each is one grid or painter in `tools/ichor/art/intro_figures.py`.

## Files

| Path | What |
|---|---|
| `src/intro.c` | The movie. Emerald's copyright-screen code is kept as is; scenes 1-3 are replaced. |
| `src/expansion_intro.c` | The powered-by card, minus the sprite gag |
| `src/data/intro_ichor_layout.h` | Generated: art positions the code needs (Clotho's hand, the golden thread's origin, the loom's threads and knots and so on) |
| `src/data/graphics/intro_scene.h` | Now only the bike-ride art the credits use. Emerald's intro art and its files under `graphics/intro/scene_1`, `scene_3` and the scene 2 Volbeat, Torchic and Manectric are deleted. |
| `graphics/intro/*` | The art, all generated |
| `graphics/expansion_intro/{powered_by,rhh_credits}.*`, `credits.pal` | The restyled card, generated |
| `tools/ichor/art/intro_lib.py` | Palettes, fonts, V-cut shading, tile writers |
| `tools/ichor/art/intro_cards.py` | The copyright, powered-by and studio cards |
| `tools/ichor/art/intro_figures.py` | Every figure: grids, plus seeded painters for the olives, trireme, ketos, temple and Olympus |
| `tools/ichor/art/intro_screen.py` | Composes the frieze and the loom, writes everything, and previews |
| `tools/ichor/art/intro_capture.py` | Headless capture: the contact sheets, stills and skip check |

## Regenerating and checking

```bash
python3 tools/ichor/art/intro_screen.py --preview   # writes the art; previews in build/intro_preview/
make -j$(sysctl -n hw.ncpu)
python3 tools/ichor/art/intro_capture.py            # sheets, key frames and stills into design/phase1/img/
python3 tools/ichor/art/intro_capture.py --skip     # START in each scene; writes img/intro_skip.png
tools/ichor/smoke_test.sh
```

- The capture reads `gIntroFrameCounter`'s address from `pokeemerald.map`, so its key frames follow the intro clock even if the cards before it change length.
- **Budgets.** The generator asserts each one:
  - the frieze must fit 1024 BG tiles (it uses 633)
  - each scene's still layers must fit 512 tiles in char block 2 (112 and 75)
- **Skipping.** Any key during the studio card, the frieze or the loom goes straight to the title. Checked at t 61, 1238 and 2096; the title then plays through to the amphora. A key during the powered-by card skips to the studio card, as upstream does. The smoke test's START at boot frame 500 lands in the studio card (t 41), and its title shot at frame 1000 is unchanged.
- **ROM.** 26,903,960 B against 26,907,384 B for main at 218ac09a8a, so 3,424 B smaller. Emerald's intro art left more room than Ichor's took.

## Not done

- The copyright card can't be skipped (Emerald's behavior), and the powered-by card skips only to the studio card. Making one press skip everything would mean changing upstream's card logic.
- `MUS_INTRO` and `MUS_TITLE` are the music agent's. The sheet above is for them.
- `design/art/INVENTORY.md` (§5 boot rows, §11 Game Freak row) and `TITLE.md`'s "Not done" still describe the Hoenn intro. They are the director's to update.
