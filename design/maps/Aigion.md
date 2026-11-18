# Aigion (`Aigion`)

Built by `tools/ichor/maps/gulf.py`; the Homarion's room by `gulf_rooms.py` on `gTileset_Domos`. 28x32, aethos + skiron. South: Route 11 (x 13-16, offset 0). The trireme lands at (16, 5) on the quay.

## Brief

- **Sentence:** the Gulf landing under Achaea's hills: a fishermen's beach, and on a terrace above it the Homarion, where Agamemnon gathered the kings before Troy.
- **Land:** the bay north, with the drowned city of Helike under it; a wide beach; a terrace walled and stepped above the town; olives south toward the pass.
- **Settlement logic:** the fishers camp on the beach by the quay; the sanctuary sits raised, its altar outside in front; the road south runs straight to the gorge.
- **Reveal:** stepping off the trireme, the Homarion's roof above the beach.
- **Signature:** the oath altar of the Achaean league, and Helike's stones showing through the water.

## People and places

- **Outdoor healer** (19, 14): `HEAL_LOCATION_AIGION` and the respawn are (19, 15). Merchant, guide, captain at the quay's end (15, 4); a whiteout from Route 11 lands here with a walk back to the captain.
- **The fishers' camp:** tents, fire, baskets, firewood, an upturned boat. The fisher gives Dive Balls "for when you can follow the fish down" to Helike.
- **The Homarion** (door 6, 22 → `Aigion_Homarion`): Agesandros the priest (after Laurel 5: King's Rock); Kleobis, an old league oarsman (gift: Shell Bell). The oath altar (8, 23-24) stands outside on the terrace; Zeus's oak by the road.
- Items: a Full Heal in the lane under the terrace, a Star Piece on Helike's islet; hidden Net Ball in a tent and Smoke Ball behind the Homarion. Water: surf and fishing.

## Hooks for later

| Gate | Relic | Where | Behind it |
|---|---|---|---|
| Helike's islet | Poseidon's Conch | (3-5, 5-6) | a Star Piece |
| Drowned Helike | the Nereid Pearl (Dive, post-game) | the bay's stones (sea boulders at (3,3) (6,4) (1,6) (8,6) ...) | a dive site: a drowned town for the post-game (needs dive water and an underwater map) |
| The Homarion's barred doors | the Labrys (seals) or a league story beat | the adyton doors in the room (1-2, 0-1) | the league's oath tablets and treasury: a post-game quest |
| The priest | Laurel 5 | the Homarion | a King's Rock on the return |

## Render passes

`img/aigion_before.png`, `_pass1.png`, `_pass2.png`, `_after.png` with `_after_walk.png` and `_after_views.png`; the room is `img/aigion_homarion.png`.
- Pass 1: boulder rows from half olive blocks, tall grass in town, the oath altar cut the terrace's west strip off, an empty bay.
- Pass 2: whole olive blocks, no grass, the altar moved east, more of Helike's stones and two surf rocks, an upturned boat.
- Pass 3: edges closed to the map border, the item moved to the empty lane west of the steps.
