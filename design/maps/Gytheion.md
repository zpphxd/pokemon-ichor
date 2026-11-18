# Gytheion

- **Sentence:** Sparta's purple harbor: a hamlet round a small bay under a wooded hill, its theater cut into the slope and a causeway out to Kranai.
- **Land:** the wooded spur of Larysion on the west and north, Taygetos's last dark spur dropping into the sea as the north-east headland, a shingle beach on the south-west, the bay open east to the Lakonian Gulf and Route 24.
- **Settlement logic:** the quay where the boats come in, the Asclepeion in the theater's stage-building facing it, the one stall beside it; the dyers on the beach downwind, their murex heaps behind the works; the two houses on the slope above the quay; the shrine on the islet the causeway reaches.
- **Reveal:** stepping off the Euploia at dusk, the purple steps and the fisherman bailing with a bronze helmet, the theater's curve above.
- **Signature:** purple: stained quay steps, pebbles, vats and the dyers' heaps of crushed murex.

Builder: `tools/ichor/maps/lakonia_gytheion.py` (via `lakonia_maps.py`). Renders: `design/phase4/img/maps/gytheion*.png`; passes in `design/phase4/img/maps/lakonia_passes/gytheion_pass{1,2,3}.png`.

Passes: (1) the plaza was a flat slab and the beach noisy with pebbles; (2) the plaza narrowed with a grass bank, olives and anemones down to the beach, the road bent past the houses, Kranai rounded, pebbles halved; (3) the bank drops to the beach by a terrace ledge, the patient and the theater's hidden item moved where they can be reached, the Proteus islet added, the town herm at the berth.

**Entrance herm:** (23,13) beside the Euploia's berth; `Gytheion_EventScript_TownHerm` calls `EventScript_IchorAnointHerm` (the travel system hooks in on merge).

**Gates and hooks:**
- The Proteus islet off the headland, by Surf (Conch): a ruined shrine with the Old Man of the Sea's lead toward Pharos (WORLD_EXPLORATION D1, the Haligeron/Proteus lead into the Oikoumene), a Mystic Water and a hidden Pearl String.
- Route 24 (the strait off Malea) would join the east edge; it isn't built, so the bay's east edge is sea border.
