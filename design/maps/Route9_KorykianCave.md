# The Korykian Cave (`Route9_KorykianCave`)

Built by `tools/ichor/maps/gulf.py` (the `CAVE` plan in `gulf_plans.py`), with `gTileset_CaveDark`'s kit and autotiler as Hecate's Hollow is. 34x26, one floor, dark (`requires_flash`). Its mouth (15-16, 25) warps to Route 9's cave door (29, 8).

## Brief

- **Sentence:** Pan's and the nymphs' great cave high on Parnassos: one huge hall of stalagmites, a still pool, and the nymphs' own grotto behind a curtain of thorn.
- **Reveal:** the brazier. With the Torch lit, the whole hall shows at once.
- **Signature:** Pan's niche of reed pipes and loaded knucklebones.

## What's in it

- **The mouth** in daylight, the name stele.
- **The great hall:** Pan's niche on the north face (the gold bee for Hesychia's errand), the nymphs' altar stone, columns and stalagmites, Tityros (goatherd). The bronze brazier (21, 6) lights the cave for good: flag `FLAG_ICHOR_BRAZIERS_START + 0x2C` (world-act2's block). Coord triggers at rows 20/21 (x 12-17) enter and leave the lit zone.
- **The drum passage** east: a column drum (28, 12) pushed four times with the Girdle rolls into the bay (32, 12); the east grotto beyond holds Korykia (beekeeper) and a Hard Stone.
- **The side chamber** behind a cobweb (5, 16-17; the Torch): a Moon Stone.
- **The pool** (still water: surf and fishing tables) with its islet.

Trainers 2 (new ids 848, 849). Items 5 + 2 hidden. Wild 28-32: land (morning and night), surf, fishing.

## Hooks for later

| Gate | Relic | Where | Behind it |
|---|---|---|---|
| The still pool | Poseidon's Conch | the islet (4-5, 10-11) | a Pearl |
| The thornweb | the Three-Flamed Torch | (17, 4-5) | the nymphs' inner grotto (14-18, 1-3): Leftovers, and room for a Pan or nymph scene (the syrinx) |
| The column drum | the Girdle (now) | (28, 12) | the east grotto, Korykia, a Hard Stone |
| The cobweb | Hecate's Torch (now) | (5, 16-17) | a Moon Stone |

The thornweb uses the cobweb metatile and an invisible object running `EventScript_IchorThornweb`; a thornweb piece is still to draw.

## Render passes

`img/korykian_cave_pass1.png`, `_pass2.png`, `_after.png`, `_after_views.png`. Pass 1's walls were straight runs from the plan; pass 2 broke the hall's north and east walls; pass 3 moved a bump that hid Pan's niche.
