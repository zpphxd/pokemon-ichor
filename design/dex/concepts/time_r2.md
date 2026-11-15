# Kronolith and Kairazor: round 2 concepts

Round 1 (`time.md`) was rejected as disjointed: the concepts were props bolted onto bodies. This round develops the user's two leads. Kronolith is **the Devourer** (round 1's `kronolith_b`). Kairazor is **Lugia meets Dialga, with a Psychic twist**.

Each row below is a matched pair, designed together the way Dialga and Palkia are. Within a pair the two share a plate-and-line language, the same gem placement and the same violet time-glow ramp (`72,32,120` / `144,80,216` / `216,176,248`, identical in both palettes). The two species are opposites in mass and element. Kronolith is slate, bronze and starry void, heavy and low. Kairazor is marble, Aegean blue and gold, light and high.

All three pairs keep the traits fixed by the master story:
- Kronolith carries the Harpe and a stopped hourglass, each as part of its body.
- Kairazor has a razor's edge and a forelock with a bare, sleek head-back behind it.

Every Kronolith shares the same Devourer head:
- a Corinthian bronze helm grown into the skull, with a nose-guard down the snout and a flared nape
- a maw that opens onto stars
- fangs like broken marble columns

Each concept is a 64×64 battle front facing left, at about 70% finish. Compare them on `sheets/time_r2.png`.

## A: The Adamant pair

This pair is Dialga's architecture, worn by both species. Plates are traced with violet time-lines, and each species has a single gem on its chest. Kronolith's gem is a stopped hourglass, two triangles meeting at their points. Kairazor's is a diamond, the same two triangles meeting at their bases: the hourglass turned inside out into the instant. Bronze in Kronolith and gold in Kairazor sit in the same places, on the head and on the blade.

- **Kronolith A** (`kronolith_r2_a.png`) is the Devourer as a quadruped behemoth on Doric-column legs.
  - One dorsal line runs from the helm's crest down the spine of fins, up the raised tail and into the bronze Harpe, which hangs over its back with a white-hot violet edge.
  - The stopped hourglass glows between its chest plates, with sand frozen mid-fall. Time-lines run from it along the plate seams to the blade.
- **Kairazor A** (`kairazor_r2_a.png`) is the purest Lugia-meets-Dialga.
  - It hovers with Lugia's long neck and a raised wing-hand whose fingers are razors: gold cutting edges with Aegean tips.
  - Aegean plates sit on the neck, shoulder and back, carrying violet lines.
  - Its other marks: a diamond chest gem, a pink third eye, and a gold forelock springing from the brow and curling forward over a bare crown.
  - Its tail ends in two balance-pan fins on a gold beam.

## B: The Crescent pair

This pair repeats one curve, the sickle. In Kronolith it is a blade and in Kairazor it is flight. Every cutting edge glows the shared violet, and both stand upright, the Titan rearing and the bird on tiptoe. The gem sits mid-chest in both. In Kronolith it is the waist of the hourglass that the whole torso has become.

- **Kronolith B** (`kronolith_r2_b.png`) is the Devourer reared up as a Titan.
  - Its torso is the stopped hourglass: a broad chest, a pinched waist and broad hips. A slit of void runs between the rib plates, with sand heaped above, a frozen thread through the waist and a heap below.
  - Its near forearm ends in the Harpe, a sickle long enough to touch the ground.
  - Its far claw is raised, and its helm's crest is split into swept-back horns.
- **Kairazor B** (`kairazor_r2_b.png`) stands tall on tiptoe like Dialga.
  - One great sickle-moon wing is raised, with an Aegean leading edge and razor fingers.
  - Its tail sweeps down and forward under its feet and flattens into a razor, so it balances on its own blade's edge: Lysippos's statue as anatomy.
  - It has a crescent forelock and a round pink chest gem.

## C: The Coil pair

This pair turns time into loops. Kronolith's body holds two loops of void, the hourglass and the endless figure-eight at once. Kairazor's tail turns a single loop that holds light: the one moment. Both are serpentine, and the plates run along their spines.

- **Kronolith C** (`kronolith_r2_c.png`) is the Devourer as a serpent-dragon.
  - Its body coils into a figure-eight standing on end, with dorsal fins along the outside of the coils.
  - The loops are filled with starry void. Sand is heaped in the lower loop, and grains hang frozen falling through the waist.
  - The tail leaves the coil and drops into the Harpe on the right.
  - It's the most original silhouette, and the hourglass reads at 1x.
- **Kairazor C** (`kairazor_r2_c.png`) is the sky-serpent: Lugia's long body and wing-hand on a Rayquaza-length tail.
  - The tail turns one loop ringed with a halo of pink light, with the instant's spark at its heart, then ends in the balance fins.
  - It has a forward forelock, a bare head-back and Aegean dorsal plates.

## Artist's pick

**Pair A is the strongest.** Kronolith A is the most developed Devourer.
- Its maw, helm, hourglass core and Harpe are linked by one dorsal line and one set of time-lines, so nothing reads as attached.
- Kairazor A is closest to the user's "lugia meets dialga" read.
- The hourglass-and-diamond gem is the clearest shared mark of any pair.

**Pair C is the boldest idea**, and the one to choose if the coils-as-hourglass silhouette matters more than Dialga's stance. Kairazor C is the least finished of the three Kairazors.

**Pair B's Kronolith** gives the best "Titan" read for cutscenes, but Kairazor B's upright pose is the stiffest of the six.

Pairs can be mixed. Kronolith A goes well with Kairazor C, for example, since both have the balance-pan tail and the light-against-void idea.

## Notes for the render pass

- These are concept fronts.
  - Several touch a frame edge: the Harpe tips and Kronolith C's top fin and bottom coil.
  - The hovering Kairazors sit lower than SPRITES.md's hover rows 50–56.
  - Fix both in the final pass, and give each a frame 2 and a back view.
- The generator scripts are in `/private/tmp/concepts_time_r2/`, which may be cleared:
  - `kron_a.py` … `kai_c.py`
  - `head_dev.py`, the shared Devourer head
  - `sheet.py`
- The final render should start from these PNGs, not from the scripts.
