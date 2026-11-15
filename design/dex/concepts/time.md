# Kronolith and Kairazor: concepts

Three concepts per species for the legendary tier (see "The legendary tier" in `design/dex/SPRITES.md`). Each is a 64×64 battle front, facing left, at about 70% finish. The pair are counterparts: Kronolith is endless, devouring time, heavy and slow, in earth, bronze and violet; Kairazor is the decisive instant, sharp and bright, in marble, gold, Aegean blue and pink. Pick one per species, and that concept gets its own full render pass.

## Kronolith #146 (Ground/Psychic, Endless Time)

**A: Titan of the Golden Age** (`kronolith_a.png`)
The brief's colossus, pushed toward clockwork. A hunched Titan of cracked earth stands on fluted Doric-column legs. Its chest is a bronze-caged hourglass with the sand frozen mid-fall, and its shoulders turn on verdigris gear-wheels like the Antikythera mechanism's. A Corinthian helm with violet eye-light sits low between the shoulders over a stone beard. The Harpe rises from its fist as a crescent as tall as its body, and the gray pool of the Frozen Hour spreads at its feet. It's the closest to the bible and the one that most looks like the Titanborn's master.

**B: The Devourer** (`kronolith_b.png`)
Kronos who swallowed his children, as a roaring behemoth. It is a hunched slate beast whose skull is a bronze Corinthian helm. Its jaws gape on a maw of violet dark where stars and sand drain away, and its fangs are broken columns. The tail arcs over its back like a scorpion's and ends in the Harpe. It's the most menacing of the three and its low, horizontal beast silhouette is unlike the others, but it reads more as a Groudon-style monster than as a Greek one.

**C: Ouroboros of Ages** (`kronolith_c.png`)
Time as the Orphic serpent Chronos, coiled into a clock dial. Its black-figure glaze is incised with terracotta lines, twelve gold hour-fins ring the rim, and gold bands mark the quarters. Its tail tip grows into the Harpe and curls up toward its own open jaws: the instant before eternity eats itself. A bronze brow-plate and helm crest crown the head, and inside the ring an hourglass of frozen sand floats with grains hanging still in the air. It's unmistakable at 1x and the most mythic, but it strays furthest from the bible's Titan: it has no legs and no Corinthian face.

## Kairazor #147 (Flying/Psychic, Moment)

**A: Razor's Edge** (`kairazor_a.png`)
Lysippos's statue as a Pokémon. A slim marble runner stands on tiptoe on a floating silver razor whose edge glows pink. It leans into a dash with razor-feathered Aegean wings swept back and gold wings at its ankles. Its bare crown sweeps back to a smooth point with nothing to grab, while a gold forelock breaks forward over its brow like a wave, and it holds a tiny balance level on one palm. It's the closest to the brief and the most elegant, but the lightest of the three at 1x.

**B: The Hourglass Falcon** (`kairazor_b.png`)
Kairos as the fastest thing alive: a peregrine whose body is an hourglass. Its crystal chest drains glowing pink sand through a gold waist into the lower bulb. It lands on the razor's edge with its wings flared high, its crown bare and white, a gold forelock curling forward over the hooked beak, and a falcon's dark stripe under the eye. It's the simplest idea and the quickest to read, and its running sand answers Kronolith's frozen sand.

**C: The Tipping Scale** (`kairazor_c.png`)
The relief of Kairos weighing the balance on a razor, made into a seraph. Its body narrows into a hanging razor, and its wings spread as a balance beam caught at the instant it tips, with a pink spark of the moment weighing down one pan. A second pair of dusk-violet wings rises behind it against a gold clock dial. Its gold forelock falls like a veil over its face, and one pink eye shows past it. It's the most mysterious and the most legendary-feeling of the three, and its single dial answers Kronolith C's ring.

## Pairings

- **Kronolith C with Kairazor C:** the whole dial against a single tick on it. This is the strongest pair.
- **Kronolith A with Kairazor A:** the bible pair, a Titan and a runner.
- **Kronolith A with Kairazor B:** both have hourglass bodies, one frozen and one running. This works as a deliberate rhyme, but it repeats one motif across both legendaries.

## Artist's pick

- **Kronolith: C.** It has the most distinctive silhouette and the deepest reading of the myth, and the Harpe is part of its body. A is the safe, brief-faithful alternative.
- **Kairazor: C.** It is the most mysterious and pairs with Kronolith C. B is the most readable and the most lovable creature, and it's the runner-up.

## Notes for the render pass

- These are concept-finish fronts. Several touch a frame edge (the bible asks Kronolith to push against the box), and the floating ones sit lower than SPRITES.md's hover rows 50–56. Fix both in the final pass.
- The generator scripts are in `/private/tmp/concepts_time/` (`kron_a.py` … `kai_c.py`), which may be cleared. The final render should start from the PNG, not those scripts.
