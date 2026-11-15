# The underworld monsters: concepts

These are three design directions each for the post-game myth monsters of the Katabasis and the Odyssey:
- **Bouldyphus #131:** Sisyphus.
- **Elegull #132 and Seirenade #133:** the Sirens.
- **Stygiad #134:** the Styx.

Read the species YAMLs (`design/dex/species/sisyphus.yaml`, `siren.yaml`, `styx.yaml`) alongside this. All of these species are in the legendary tier of `design/dex/SPRITES.md`.

Each concept is a 64×64 battle front facing left, at about 70% finish: about 70% of a finished sprite, at most 15 colors, every channel a multiple of 8, transparent background.

The rule every direction keeps is **cohesion**. The boulder, the lyre and the oath-water are anatomy, never props. Faces are Pokémon faces: a beak and eyes, or a mask with big simple eyes. None has a human nose, lips or brows.

The comparison sheet is `sheets/underworld.png`. Each species is a row of its three concepts at 3x with 1x thumbnails, and official sprites sit alongside: golurk, regirock, spiritomb, giratina, mismagius, chandelure, lunala, articuno, yveltal, froslass, cofagrigus and necrozma.

## Bouldyphus #131 (Rock/Ghost)

The three directions are the three ways a ghost can belong to its stone: the stone is on it, the stone is it, or it is inside the stone. All three share one face and one pattern:
- **The face:** one wide gold eye, one eye screwed shut with effort, and a wide grin that says it still thinks it got the better deal.
- **The pattern:** cracks in the stone that run at right angles into a meander, with the glow showing through, so the boulder and the ghost light up together.
- **The hands:** stone fists or hands, so the rock runs through the limbs too.

### A: The Burden (`bouldyphus_a.png`)

The boulder has grown into its back, and its shadow-flesh swells up round the stone's base where they've fused. A meander groove circles the boulder's girth, glowing violet. Two stubs of the same stone break through its brow, its forearms end in stone fists, and its legs are a wisp trailing downhill as it hauls itself up the slope on its knuckles. Glow: violet (184,112,248).

### B: The Rolling Stone (`bouldyphus_b.png`)

Sisyphus has become the stone. Its whole body is the boulder, cracked open into a vast jagged grin and one burning eye, with a meander diadem: the crown of Corinth worn down into the rock. Smoke arms pour out of cracks in its flanks to drag it uphill. Beneath it, one ghost-tail curls back down the slope, the way the stone always rolls back. This ties to its Rock Head, Rollout and Head Smash. Glow: ghost-fire green (104,224,144).

### C: The Shade in the Stone (`bouldyphus_c.png`)

The trickster king is bound inside his boulder. His shade rises out of a split in its crown to the waist, wearing a circlet of stone horns, and drags the stone uphill on one huge arm while the other clutches its side. Death's chain, the one he once bound Thanatos with, is wound round the boulder. Gold, the life he stole, leaks from meander cracks and wells up in the split. Glow: gold (232,168,48).

### Pick: B

- It is the most cohesive. There is no seam between creature and stone, because the boulder *is* the creature, and its arms and tail come out of the stone's own cracks.
- It has the strongest silhouette at 1x: a round stone with a grin.
- It carries the brief's expression, and it ties straight to its moves.

**C is the runner-up for story.** The bound king and Thanatos's chain give it the richest myth, but at 1x it reads as a genie rising from a pot.

**A is closest to the brief's pushing ghost.** The fused collar and shared meander help, but the boulder can still read as a ball carried on its back, which is the thing the user flagged.

## Elegull #132 and Seirenade #133 (Ghost, then Ghost/Flying)

Each direction is drawn for both stages, so one pick sets the whole line. In each, the chick carries the final's face, its tear marks and a first hint of the lyre.

### A: The Lyrebird (`elegull_a.png`, `seirenade_a.png`)

The singer, with the lyre grown from a real lyrebird's tail.
- **Elegull A:** a round downy fledgling on a broken grave stele. It has a heart-shaped owl face-disk, big downcast lilac eyes and Aegean tears, and two short tail feathers already curling.
- **Seirenade A:** the grown swan-necked siren on a sea rock among bones, head thrown back and gold beak open in song, near wing open in a beckoning sweep. Two lyrate tail feathers grow from her rump and turn from white to gold as they curve into the lyre's arms, strung with three lilac filament feathers.

Glow: lilac (176,136,240).

### B: The Living Lyre (`elegull_b.png`, `seirenade_b.png`)

The mourner whose grief opens into song.
- **Elegull B:** a teardrop chick with its wings drawn over its head like a mourning veil. Only its wet sea-foam eyes and beak show, and the wingtips curl up behind it into a tiny lyre.
- **Seirenade B:** the veil has opened, and the siren's whole silhouette is the instrument. Her raised wings are the lyre's arms, and a gold yoke joins the wingtips over her head. Three sea-foam strings run down to a tortoise-shell soundbox on her breast; the first lyre was a tortoise shell. She has a bird face: a pale face plate, big glossy eyes and a small open gold beak. Her body tapers into a ghost wisp.

Glow: sea-foam aqua (112,224,208).

### C: The False Beacon (`elegull_c.png`, `seirenade_c.png`)

The wrecker. Frigatebird anatomy carries both the lure and the lyre.
- **Elegull C:** a dark downy chick on a bleached bone, with a pale deflated throat pouch that glows faintly when it cries.
- **Seirenade C:** on huge angular wings, her inflated throat sac blazes like a false lighthouse luring ships onto the rocks. Her forked tail streams back and curves into a gold lyre strung with the same ember light.

Glow: ember (232,88,56) with a hot core.

### Pick: B

- It is the most cohesive: the wings *are* the lyre, nothing is attached.
- It has the strongest 1x silhouette, a Lunala-class frame.
- It gives the clearest growth from chick to final: the veil of grief opens into the instrument.

**C is the runner-up for drama and a new reading of the myth.** Its lyre still has a straight crossbar that should curve in the render pass.

**A is closest to the brief** and is now properly anatomical. Its strings are faint at 1x, so the lyre reads more as a curling tail there.

## Stygiad #134 (Ice/Ghost)

Each direction makes the oath-water part of her rather than a jug she holds. All three have ice-mask faces in Froslass's lineage, and fins or sleeves of ice for arms.

### A: The Oath-Vessel (`stygiad_a.png`)

The vessel as body. Her torso is a polished gold hydria, with a meander on the shoulder and a black Styx wave on the belly. Its handles are the roots of her fin-arms: one raised as a broad wing-fin, one cupped open below. A masked ice spirit with a frozen-wave crest rises from the jar's mouth. A long thread of black water arcs from the lip and ends in a glowing drop. Below the jar's foot the water freezes into an icicle waterfall that dissolves into violet mist. Glow: ice-cyan (56,192,224).

### B: The Ninefold River (`stygiad_b.png`)

The river as body. The Styx winds nine times around the underworld, and she is one great S of river filling the frame. A crust of ice plates covers her lit flank, the black river flows underneath, and gold oath-rings bind her. Floe fins run along the curves, and her tail ends in a delta. Her Lugia- or Milotic-like head has a black-figure eye mask, closed frost lids glowing violet, and three long crest-fins streaming back like the current. Glow: ghost-violet (168,120,240).

### C: The Libation (`stygiad_c.png`)

The oath as a crown. She is a Froslass-lineage spirit with a hood of frozen ripples, temple crest-fins, a pale mask with closed frost lids, and a black-figure oath mark. Behind her rises a gold halo shaped like a libation phiale, the dish oaths were sealed with: its boss sits like a crown jewel, and a single thread of black water hangs frozen from its rim. One sleeve-fin is raised straight up in the oath, with a teal seal of light at its tip. Her gown is a frozen fall of black water breaking into icicles and mist. Glow: Styx teal (104,232,192).

### Pick: C

- It has the most legendary silhouette and contrast: a gold dish-crown over a pale spirit and a black gown.
- The oath gesture and the frozen thread tell the myth at a glance.

**B is a strong runner-up.** It is the most dragon-like, the "Lugia" option, but its silhouette sits close to Rayquaza's and it no longer reads as a naiad.

**A is the most literal and charming,** but it keeps some "spirit in a lamp" feel.

## Notes for the render pass

- **Edges and rows.** Several concepts touch row 61–62 or a side column: Bouldyphus B's fingers, Seirenade A's wing, and the perches and mist. Keep feet on rows 58–61 and hovering bodies on rows 50–56 in the final.
- **Not drawn yet:**
  - frame 2
  - the back, follower and icon views
  - the shiny palettes
- **Briefs to update.** Whichever directions win, the YAML art briefs should change with them. In particular:
  - Seirenade's "woman's serene face" becomes a bird face.
  - Stygiad's held golden jug becomes anatomy.
  - Bouldyphus's "boulder bigger than itself" becomes A, B or C's relationship to the stone.
- **Open weaknesses, by species:**
  - Bouldyphus: the ghost bodies' shading is still code-drafted and flat.
  - Seirenade: B's head is small for its frame.
  - Elegull: B still has the older pale-oval face rather than Seirenade B's face plate.
  - Stygiad: C's upper body is busy where its fins, spikes, raised arm and phiale overlap, and at 1x the phiale can read as a sun headdress.
- **Scripts.** The generator scripts are in `/private/tmp/concepts_underworld/` and may be cleared:
  - `kit.py` holds the shared helpers.
  - The sprites themselves are drawn by `bould_a.py` … `bould_c.py`, `siren_*.py` (with `siren_kit.py`) and `styx_*.py` (with `styx_kit.py`).
  - `sheet.py` builds the comparison sheet.
  - Start the final renders from the PNGs, not the scripts.
