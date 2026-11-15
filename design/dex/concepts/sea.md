# The post-game sea monsters: concepts

There are three directions each for Hexylla (#135, Water/Dark, Scylla), Trybdis (#136, Water/Ground, Charybdis) and Haligeron (#137, Water, Proteus). All three belong to the legendary tier (see "The legendary tier" in `design/dex/SPRITES.md`).

- **What each concept is.** A 64×64 battle front facing left, at about 70% finish, with 15 colors in multiples of 8.
- **How Hexylla and Trybdis are lettered.** They face each other across one strait, so each letter is one shared design language. Hexylla A goes with Trybdis A, and so on. Each pair has one glow color, with identical values in both palettes.
- **How Haligeron is lettered.** Its directions stand alone.
- **The rules every direction keeps.**
  - Motifs grow out of the anatomy.
  - No human faces.
  - Every Hexylla direction solves the six-heads problem its own way.
  - Every Trybdis is a creature with eyes and a body, not a whirlpool graphic.
  - The figs, fangs and forms are body parts, never props.
- **The sheet.** `sheets/sea.png` shows each species as a row at 3x, with reference legendaries alongside.

## Hexylla #135

The heads are the same sea-hound in every direction: a tall pointed ear-fin, a long muzzle, open jaws with marble fangs and a glowing eye. They are hand-pixeled at four sizes. What changes between directions is the body they grow from.

- **A: Anthemion** (`hexylla_a.png`). A rearing indigo sea-serpent whose six necks spring from its shoulders and are webbed together into one violet palmette, the fan-shaped anthemion ornament of Greek temples, grown as a hood.
  - **How it solves six heads.** The web makes the necks one shape, so the 1x silhouette is a single crowned fan. Depth and value grade the heads from the large lit lead head down to a small dark one at the rim.
  - **The glow.** Magenta rays light the webbing like the ribs of the ornament.
  - **The myth.** Scylla as the strait's terrible display: six bites raised behind one lunge.
- **B: Cliff-Kraken** (`hexylla_b.png`). A vampire squid diving out of the cliff cave. Its mantle and fins point up-right and its six arms fan down-left, each ending in a hound head.
  - **How it solves six heads.** The heads sit at the tips of a cephalopod's arms, so they come from real anatomy and never cross. The near arms are slate with marble suckers; the far ones fade into the cave's violet dark.
  - **The glow.** Cyan photophores mark the mantle, and a ring-shaped eye watches from the collar.
  - **The myth.** Homer's Scylla, who never leaves her cave and reaches down for whatever passes.
- **C: The Sheer Rock** (`hexylla_c.png`). Homer's smooth, cloud-capped cliff made a creature: a giant barnacle crag whose six wall plates (one per head) open at the crown. Its cirri are six slate-teal hound necks arching out like a fountain.
  - **How it solves six heads.** The necks fan out radially from one crater, two of them turning right in front of the crag, with amber eyes catching light.
  - **What it adds.** Homer's dark cloud never leaves the peak, and anemone foam breaks at the foot.
  - **The myth.** The strait's geography itself is alive.

## Trybdis #136

Each Trybdis has a different maw: a tunnel of fangs (A), a vortex of arms (B) and the sea itself spiralling in (C).

- **A: The Frilled Maw** (`trybdis_a.png`). An indigo sea-serpent rearing out of its own coils in a frilled lizard's threat display.
  - **The maw.** Its head faces the viewer with the jaws thrown wide: a dark throat ringed with three rows of marble fangs, each row deeper and darker. That is the brief's whirlpool of teeth seen from the front.
  - **The pair link.** Behind the head a pinwheel frill spreads with magenta rays, the same palmette Hexylla A wears.
  - **The fig.** It grows from the tail tip at the right edge.
- **B: Ammonite Kraken** (`trybdis_b.png`). A colossal ammonite of terracotta stone (the Ground type), with a glowing cyan Greek key running round the whorl as its suture line.
  - **The maw.** From the aperture a great ringed eye looks out, and slate arms curl into a vortex round a fanged beak, with sea streaking in.
  - **The fig.** It is rooted on the shell's crest and leans out over the maw, where Odysseus would hang.
  - **The pair link.** It shares Hexylla B's arms, suckers and cyan light.
- **C: The Low Rock** (`trybdis_c.png`). Homer's lower rock with the fig tree, alive: a frogfish-stonefish islet of limestone with scowling amber eyes in bony turrets.
  - **The maw.** Its underbite gapes so wide that the sea spirals visibly into the throat.
  - **The rest of it.** Fan fins grip the seabed, and the gnarled fig grows from its back.
  - **The pair link.** Hexylla C's tall rock and this low one are the two rocks of Odyssey 12.

## Haligeron #137

Each Haligeron shows "can't hold one shape" differently: as markings (A), as camouflage (B) and as the body itself changing (C). All three keep the brief's sly half-open gold eye and the foam beard.

- **A: Elder of the Seals** (`haligeron_a.png`). A squat walrus elder sitting up on its flippers, the closest direction to the brief.
  - **The beard.** Ivory tusks hang over a foam beard that breaks into a wave at its tip.
  - **The markings.** The other shapes surface in its hide as sea-glass lines: a lion's ruff round the neck, serpent scales on the flank and a leaf in the tail flipper.
  - **The myth.** The herdsman napping among Poseidon's seals at noon.
- **B: The Mimic** (`haligeron_b.png`). Proteus as the mimic octopus, nature's real shapeshifter. Its bald dome and heavy-lidded gold eye are the old man's head, and its arms bunch beneath into a curling beard tipped with foam.
  - **The forms.** One arm is banded like a sea snake, leopard rosettes and a sea-glass wave of colour pass across the dome, and raised papillae fringe the face like a mane.
- **C: The Turning** (`haligeron_c.png`). A seal elder caught in the middle of a change, the moment Menelaus must hold through. Its hindquarters are already running water, rising behind it in a breaking crest.
  - **The forms.** Inside the water, glowing foam traces a serpent's coil, a lion's mane at the crest and a leaf in the spray.
  - **The 1x read.** It has the strongest silhouette of the three: a seal under a wave.

## Signature glows

| Concept | Glow |
|---|---|
| Hexylla A, Trybdis A | Magenta `224,88,224` / `248,184,248` |
| Hexylla B, Trybdis B | Cyan `48,200,216` / `176,248,240` |
| Hexylla C, Trybdis C | Amber `232,136,32` / `248,224,120` |
| Haligeron A, B | Sea-glass, with a gold eye |
| Haligeron C | Pale lime-gold foam in the water, with a gold eye |

## Artist's pick

**Pair A, Anthemion with the Frilled Maw.**
- It has the clearest shared language: one palmette, worn as six necks by Scylla and as the frill round the maw by Charybdis. It is Kyogre and Groudon's kind of rhyme.
- Hexylla A turns six heads into one emblem at 1x.
- Trybdis A is the strongest creature read of the three Trybdis: eyes, jaws and a body, with the whirlpool inside its mouth.

**Pair B is the runner-up** and the most original. The ammonite's glowing Greek-key suture is the single best detail on the sheet, and the diving squid is the most frightening Hexylla.

**Pair C is the most faithful** to Homer's two rocks, but it reads more as landscape than as legend.

**Haligeron C, The Turning.**
- Its shape-shifting is the body itself rather than a pattern on it.
- It has the strongest silhouette of the three.
- It stays a pinniped elder with the beard and the sly eye.
- B is the cleverer idea if the octopus doesn't crowd the dex alongside Sepivolt.

## Notes for the render pass

- **Brief deviations to confirm with the creative director:**
  - The Hexylla briefs give terracotta dog heads. Every direction colors the heads as part of the body instead, because a separate material read as bolted on.
  - Haligeron's brief says medium (about 46×44). These concepts fill about 60 px, per the legendary-tier rule.
  - Hexylla B has a seventh "face": the squid's eye on its collar.
  - Trybdis A's fig grows from the tail, not the rim.
- **Polish still owed:**
  - The hound heads are three hand templates stamped at depth. Vary their mouths and angles so they don't read as stamped detail.
  - Trybdis A and C and several others touch the frame edges. Keep the final sprites inside rows and columns 1–62.
  - The pinniped faces (Haligeron A and C) need a hand pass at 1x and 2x.
  - Each species still needs frame 2 and a back view.
- **Generator scripts.** They are in `/private/tmp/concepts_sea/`, which may be cleared:
  - `hex_a.py` … `hal_c.py`, one per concept
  - `tmpl.py`, the hand-pixeled hound heads
  - `hound.py`, the parametric head
  - `kit.py`
  - `sheet.py`

  The hound-head templates are the one piece worth keeping, so they are copied below. Start the final render from the PNGs.

## Appendix: the hound-head templates

These face left. The anchor is where the neck joins. Legend:

- `#` ink
- `0`–`4` skin, dark to light
- `p`/`P` pale jaw
- `f`/`F` ear-fin
- `a` mouth
- `r` gum
- `w` fang
- `e` eye
- `i` iris glow
- `s` shine
- `n` nose

`L`, anchor (16, 11):

```
..............#......
.............#4#..#..
.............#43##F#.
............#432#fF#.
............#4321#fF#
........####44321#f#.
......##4444333221f#.
....##4443###222110#.
..##44433#es#2211000#
.#4433333##i#221100F#
#n4333333322222110FF#
#4322222222211110ff#.
.##########p11100f#..
..#waaaawaa#p100f#...
..#aarrrraa#pp0f#....
...#w#aw#a#ppp0#.....
....#PPPPPPpp##......
.....########........
```

`M`, anchor (12, 7):

```
........#..#....
.......#4#.#f#..
.......#43##fF#.
.....###4321fF#.
...##443332110#.
..#43##e#22110#.
.#4433#is#2110F#
#43333322211100#
#3##w#ww##111ff#
.#aarraa#p11ff#.
..##w#wPPp00#f#.
....#####pp##...
.........##.....
```

`M2`, anchor (12, 7):

```
........#..#....
.......#4#.#f#..
.......#43##fF#.
.....###4321fF#.
...##443332110#.
..#43##e#22110#.
.#4433#is#2110F#
#43333322211100#
#3#w##w###111ff#
.#ppPPPPp011ff#.
..#########0f#..
...........##...
```

`S`, anchor (9, 6):

```
......#..#..
.....#4##f#.
....#43#fF#.
..##4332110#
.#43##e#210#
#4433is#110#
#33222211ff#
.#w#aar#0f#.
..#wPPp##...
...####.....
```

`XS`, anchor (7, 4):

```
.....#.#..
....#4#f#.
..##432f#.
.#43#i10#.
#432221f#.
.#w#ar0#..
..####....
```
