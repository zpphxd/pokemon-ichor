# Kynder, Dikyon and Pylakyon: concepts

Three line-wide directions for the Fire starter (see `design/dex/species/cerberus.yaml`). Each direction is drawn for all three stages, so a pick sets the look of the whole line. Each sprite is a 64×64 battle front facing left, at about 70% finish. All three directions keep the parts that already work: the bronze collar with its black-figure meander band, flames that cool from gold to Aegean blue on Pylakyon, Pylakyon's serpent tail, and one more head waking at each stage. They differ in what the extra heads are made of.

All three share one Kynder head: a round skull, short ears with soft points, a short cream muzzle with a nose pad, a cream cheek running back under a big eye with a two-pixel shine, and a panting tongue. The shared body is a squat pup with oversized paws. The comparison sheet is `sheets/cerberus.png`. It puts each direction in a row at 3x and 1x, then the committed sprites, then growlithe, arcanine and houndoom.

## A: Ember Dreams

The heads that are still asleep are flames. Kynder's two sleeping heads are the two biggest tufts of its fire ruff, each shaped like a little dozing hound's head with closed eyes and a nose. As the line grows, the dreams wake into flesh one at a time. This is the most literal reading of the brief and the classic three-headed silhouette.

- **Kynder** (`kynder_a.png`): a sitting pup. Two dreaming flame faces curl up out of its ruff behind its head.
- **Dikyon** (`dikyon_a.png`): a lean hound mid-stride. The second head has woken and snaps back over its shoulder at the trail. The third is still a dreaming flame face on the shoulder between the two necks.
- **Pylakyon** (`pylakyon_a.png`): three terracotta mastiff heads on a bronze gorget. A fire mane blazes up around the base of the necks and cools to blue at the tips. A banded bronze serpent tail curls up behind.

## B: Ghostfire Kin

The extra heads are ghosts. They start as will-o'-wisps and condense a little more at each stage, so the Ghost typing grows into the body before Pylakyon gains it. This direction shows the Fire/Ghost type best, and its final has the most unusual silhouette.

- **Kynder** (`kynder_b.png`): a standing pup. Two sleeping wisp-puppies rise off its ruff on stems of flame.
- **Dikyon** (`dikyon_b.png`): the second head is half-materialized. Its face is flesh, but the back of its skull is still burning. It snaps upward above the first head, and the third wisp drifts along its back.
- **Pylakyon** (`pylakyon_b.png`): the middle head is flesh. The outer two are Aegean-blue ghost-fire mastiffs with gold eyes and bone-pale muzzles, held up on necks of blue flame that run into the mane.

## C: Black-Figure Kin (my own idea)

The extra heads are black-figure painting come alive. On an Attic vase, figures are black glaze and every detail is scratched through to the orange clay. Here, a black-figure mantle spreads from the collar's meander band over the pup's shoulders, and the extra heads grow out of it as glossy black hounds with terracotta incisions. The black-against-terracotta contrast also fixes the original problem, because three heads in one color merge into a lump at Gen 3 size.

- **Kynder** (`kynder_c.png`): a sitting pup with black-figure socks. Two little black heads sleep curled on its mantle, their closed eyes and ears scratched in terracotta.
- **Dikyon** (`dikyon_c.png`): the second head has woken as a black-figure hound and barks back at the trail, which makes the dex line about barking "at its own shadow" literal. The third still sleeps on the black saddle, and the legs fade to black glaze.
- **Pylakyon** (`pylakyon_c.png`): a terracotta middle head stares ahead between two black-figure heads with incised jaws and ghost-blue eyes. The black saddle and serpent tail carry incised terracotta lines, the legs fade to black glaze, and the fire mane cools from gold to blue.

## Artist's pick

**C is the strongest.** Its three heads stay separate at 1x, so the heads don't clutter. It is the most Greek of the three, because the meander on the collar becomes the creature's own markings. It reads as one creature: the black figure starts on the collar, spreads to the mantle and then becomes the heads. Its shiny also works, since an ash-marble coat with blue fire still frames the black heads.

**B is the runner-up**, and its Kynder is the most lovable of the three: the wisp-puppies are the cutest take on the sleeping heads. Its Pylakyon is the boldest final. The risk is that floating ghost heads come across as attached rather than grown, so the render pass should keep the flame necks.

**A is the safe, brief-faithful choice.** Its Kynder works well, but its Pylakyon brings back the original problem: three heads in one color crowd the top of the frame.

## Notes for the render pass

- **Sizes.**
  - Kynder is about 43×41 including its flames. That is larger than the brief's 32×36, so the final can trim the body, but it should keep the big head.
  - Dikyon is about 56×49 and could lose a few pixels to stay clearly between the other two.
  - Pylakyon fills 62×60 and stays clear of every frame edge.
- **Shared heads.**
  - The middle Pylakyon head and the Dikyon hound head are shared across the three directions.
  - The directions differ in how those heads are recolored: ghost-fire in B, black-figure in C.
  - Every face is a hand-drawn pixel template, not a rendered shape.
- **Not done yet.**
  - Frame 2 and the back, follower and icon views aren't drawn.
  - The bodies still need fur texture and the finer muscle work that arcanine has.
- **Generator scripts.** The scripts are in `/private/tmp/concepts_cerberus/` and may be cleared:
  - `kit.py` and `parts.py` hold the shared helpers.
  - `asc.py` holds the hand-drawn heads.
  - The sprites themselves are drawn by `a.py`, `a_dik.py`, `a_pyl.py`, `b*.py` and `c*.py`.
  - `build_all.py --write` writes the files.
  - Start the final render from the PNGs, not from these scripts.
