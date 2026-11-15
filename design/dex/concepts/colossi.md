# The colossi: concepts

There are three trio-wide directions for Olympanax (#149, Electric, Zeus), Pontanax (#150, Water, Poseidon) and Nekranax (#151, Ghost, Hades). They belong to the legendary tier (see "The legendary tier" in `design/dex/SPRITES.md`).

- **What each concept is.** A 64×64 battle front facing left, at about 70% finish.
- **The rules every direction keeps.**
  - The brothers have no faces, only their lot's emblem in glowing points: a bolt in electric yellow, a trident in sea-foam aqua and a bident in ghost violet.
  - Each one's attribute is part of its anatomy, never a prop it holds.
  - The three share one design language, the way the Regis or Dialga, Palkia and Giratina do.
- **What to pick.** Choose one direction for the whole trio; each colossus then gets its own render pass.

The comparison sheet, with reference legendaries alongside, is `/private/tmp/concepts_colossi/sheet.png`.

## A: The Risen Statues

The three cult statues come alive, and their regalia has grown into them. Each is a monumental humanoid in its own sacred material: gold and ivory, sea-green bronze and black basalt. Each is posed for its domain: Zeus stands under the sky, Poseidon strides out of the surf and Hades never left his seat.

- **Olympanax A** (`olympanax_a.png`): Phidias's gold-and-ivory Zeus on its feet.
  - The eagle from its scepter has become two folded gold wings rising from its back like a mantle.
  - A thunderbolt strikes down into its raised open palm.
  - It has a blank ivory face with a seven-point bolt, a gold beard and an olive wreath.
- **Pontanax A** (`pontanax_a.png`): the Artemision bronze lunging out of a breaking wave.
  - Its raised forearm runs into a bronze shaft, and its hand is the trident: three barbed tines.
  - Its other details are a plate face with a trident glyph, a beard of weed, and barnacles and coral.
- **Nekranax A** (`nekranax_a.png`): the brother who kept his throne, fused to it.
  - Its basalt mantle and the throne are one mass, and the throne's corners sweep up into the bident's two gold-tipped tines.
  - Under the crestless Helm of Darkness, the bident glows in the T of the visor. It is hunched, with its hands on its knees and its legs gone to smoke.

## B: The Elemental Titans

The Cyclopes forged the three gifts together, so the brothers wear one war-gear: the same Corinthian helm and muscled cuirass. Inside that gear, each body is its domain.

- **How the gear is shared.** The visor's T holds the emblem, and the helm's crest is the element.
- **How each one strikes.** One limb turns into the weapon:
  - Zeus's forearm is the thunderbolt.
  - Poseidon's hand is a trident of water.
  - Hades's gauntlets end in bident talons.
- **How the three sit in the frame.** Their heights read sky, sea and underworld: Zeus floats high on a storm funnel, Poseidon rises out of a curling wave, and Hades sags low into a ghost-tail of shadow.

- **Olympanax B** (`olympanax_b.png`): a thunderhead with eagle wings of storm cloud.
  - Its gold helm wears a Corinthian crest of living lightning.
  - Its near forearm becomes a forking bolt that strikes the ground.
- **Pontanax B** (`pontanax_b.png`): the sea in verdigris armor, with a dorsal-fin crest.
  - Its lower body is a wave that curls up behind it and breaks over its head.
  - Its raised arm turns into a trident of water.
- **Nekranax B** (`nekranax_b.png`): a hulking black war-shell.
  - Shadow pours up out of the helm like a crest.
  - Its giant gauntlets end in twin gold bident talons.
  - Below the belt it dissolves into shadow tongues.

## C: The Temple Golems

The brothers are their temples walking, which makes them the Regis of Greek architecture: each colossus is one of the three orders.

- **What the architecture does.** Columns are the limbs, the capital or roof is the head, and a Regi-style face of glowing points sits where a temple keeps its god.
- **Where each attribute goes.** It is the akroterion, the sculpture on the temple's crown.

- **Olympanax C** (`olympanax_c.png`): Corinthian, after the Temple of Olympian Zeus.
  - Its gable is the head: a seven-point bolt glows in the tympanum and a gold eagle akroterion spreads on the peak.
  - Lightning crackles inside the cella between its columns, and its arms are fluted Corinthian columns.
- **Pontanax C** (`pontanax_c.png`): Ionic, a drowned temple, sea-green and crusted with barnacles.
  - The two great volutes are its shoulders, their eyes glowing.
  - The trident glyph glows across the capital, and three stone tines grow up out of the abacus as its crown.
- **Nekranax C** (`nekranax_c.png`): Doric, a Mycenaean beehive tomb.
  - The dome is its helm, and its doorway with the relieving triangle above it is the helm's T. The bident glows in the dark of the door.
  - Two gold bident horns sweep out of the dome's crown, Mycenaean gold is set in the masonry and smoke pools at its feet.

## Artist's pick

**C, the Temple Golems.**
- It is the most cohesive and the most unmistakable at 1x, and the most purely Regi.
- The three orders give the brothers one shared language and three distinct silhouettes: a gable, scrolls and a dome.
- No other hack has walking temples, and they work in the overworld, where the colossi wait in their sanctuaries.

**B is the runner-up** for drama. It has the strongest trio rhyme: one helm and three elements. Its risk is the feedback on the other legendaries: armor over an element can still read as assembled.

**A is the most faithful** to the current briefs and the bible's "statue that stood up". It reads more as three humanoid gods than as Pokémon.

## Notes for the render pass

- **Briefs that change if C or B wins.** The species YAMLs' art briefs (thrones, a scepter eagle, a held trident and bident) describe the old statue idea. Update them with whichever direction wins.
- **Faces.** The face glyphs are placeholders at concept finish. Check the final dot counts against the briefs: seven for the bolt.
- **Polish still owed:**
  - Shading on the big statue and cloud masses is code-drafted and needs a hand pass, especially Olympanax A's robe, Pontanax B's cuirass and Nekranax A's cloak.
  - Several sprites reach rows 61–62. Keep the feet on rows 58–61 in the final pass.
