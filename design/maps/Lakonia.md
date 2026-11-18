# Lakonia

- **Sentence:** Sparta as Thucydides saw it: villages run together on the valley floor with no wall anywhere, the battle school under the mountain as its crown.
- **Land:** Taygetos a sheer dark wall down the west, a spur of it over the agoge; the Eurotas down the east with marshy banks; the far bank rises to the Menelaion's ridge; the valley floor is flat but for the agoge's terrace.
- **Settlement logic:** the road from Gytheion crosses the one bridge, with the Asclepeion and the Agora at its head and Artemis Orthia on the marshy bank beside it; the agora in the middle (the Persian Stoa, the chained Enyalios, the Lesche's porch, the mess hall); the agoge, its yard and ring under the rock; the palaestra and its sands by the training fields; plain houses round beaten yards at the west end against the mountain, Lampito's among them with its burial plot (Spartans buried their dead in town); olive groves across the river.
- **Reveal:** coming over the bridge the stoa's captive Persians and the bronze war god in chains, and no wall in any direction.
- **Signature:** the battle-school ring, and a cadet running across every screen.

Builder: `tools/ichor/maps/lakonia_town.py`. Renders: `design/phase4/img/maps/lakonia*.png`; passes in `lakonia_passes/lakonia_pass{1,2}.png` and the current render.

Passes: (1) a sparse layout; (2) palaestra and sands, the bridge row, Orthia's door made reachable, the Lesche as an open porch, the north road roped; (3) the agoge lifted a terrace above the village (ledges), the far bank's olive groves, a village yard and well south of the agora, gardens in the west, a rubble cleft, boulders breaking the rock wall's run, the town herm.

Doors (the rooms' contract): 0 Asclepeion, 1 Agora, 2 Lampito, 3 Gylippos, 4 syssition, 5 agoge, 6 palaestra, 7 Orthia, 8 Chilon, 9 Lichas.

**Entrance herm:** (37,35) at the bridge's west end; `Lakonia_EventScript_TownHerm`.

**Gates and hooks:**
- The Mani road south (Route 31 to Cape Tainaron): roped, post-game (UNDERWORLD).
- The north road (Route 26, Lake Stymphalia, Route 27 to Arkadia): roped with a cadet on guard until those maps exist; Route 26 is not built. The north strip is not yet aethos-only; whoever builds Route 26 agrees it.
- The Menelaion across the river (Conch): a Rare Candy and a hidden Star Piece.
- The cleft behind the agoge's yard (Bronze Hammer): a Focus Band.
- Prophecy fragment 8 in the burial plot (fixed dig index 0x30, from III-5E on).
