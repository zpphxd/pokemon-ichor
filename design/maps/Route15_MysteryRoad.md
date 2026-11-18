# Route 15, the road of the Mysteries

Eleusa's east gate to Daphni, rebuilt (2026-11-18) from the 48x24 placeholder
that `nemea.roads()` wrote for astyra.py. `tools/ichor/maps/sacredway.py` owns
this map, Daphni and Route 16 (and Daphni's rooms); nemea.py and astyra.py skip
them with commented exclusions. Rebuild and re-render:
`/usr/bin/python3 tools/ichor/maps/sacredway.py --render design/maps/img --stem-suffix _after`.

| | |
|---|---|
| Size, tilesets | 80x34, Aethos + Skiron (was Kalliste) |
| Levels | wild 32-34 (land), trainers 35-37 (BALANCE.md) |
| Story | The procession's road from Eleusis to the city, walked backwards: the Rheitoi, the Aigaleo pass, Aphrodite's rock shrine, Daphni's laurels ahead |

Renders: `design/maps/img/route15_before.png`, `route15_pass1.png`, `route15_pass2.png`,
`route15_after.png`, `route15_after_walk.png` (collision, grass, sight lines),
`route15_after_views.png` (15x10 views along the road).

## Seams

- Eleusa's east gate (its x 49, rows 24-27) meets our rows 10-13 at offset 14, unchanged; Eleusa's
  watch (the hoplite and the stood-aside watchman at (47,23)) is Eleusa's own. Our 8 west columns are aethos only.
- Our east road, rows 16-19, meets Daphni's west road at offset 0. Our 8 east columns are aethos only.

## The road

1. **Eleusa's gate and the Thriasian olives.** The west sign, Timon the watch in plain view (the first
   trainer, DOWN 4 across the gate road), two optional fields in the olives (the Hyper Potion jar, the
   Ultra Ball jar, hidden Honey in the south field's hive corner).
2. **The Rheitoi.** Two salt lakes with the causeway between them (fishable and surfable: surf and
   fishing tables). Hegeso watches the causeway and band 1 (4 deep) follows her with the lakes for walls.
   The priest-fishers' beach on the north lake (the priest's gift: a Dive Ball; hidden Revive). The
   jesters' broken bridge: a stub into the south lake, the span gone, Kerkops the jester shouting from
   the islet across the gap (A1).
3. **The Aigaleo pass.** A three-row scarp with a cut stair (Polemon at its head), the terrace road
   (band 2, then Phila), the great herm and the pilgrims' spring with its keeper (the midpoint rest:
   she heals), Aphrodite's niches in the rock (hidden Heart Scale), and the shrine court.
4. **The shrine court's seal.** Two column drums and two worn plates. With the Girdle, roll each drum
   onto its plate (4 pushes; solvable, checked by `check_seal()`); the court's stair opens down the
   scarp into Kore's hollow (TM22 Solar Beam: Kore returning to the light). The reset post rolls the
   drums back. FLAG_ICHOR_R15_SHRINE_STAIR.
5. **The ledge back down** from the terrace into the foot meadow (Theoxenos, who skipped the climb), and
   the old Aigaleo quarry below it, down a Pan's Crook face: Simmias the quarryman, a Hard Stone, hidden
   Star Piece in the spoil, the cut blocks.
6. **The east side.** The east stair down; a gully choked with fallen rock (the Hammer) to the Iakchos
   glade, where Lampon keeps the procession's cold torch-stand: light it with Hecate's Torch and the
   stand's cup gives up a Fire Stone (the Ether jar and hidden Super Repel in the glade). A thicket (the
   Sickle) over Demeter's wayside altar (Kallidike, a Big Root). Agis, band 3 straight after him,
   graves along the Sacred Way, Praxon above Daphni, the east sign.

Forced grass: 12 each way. On the only road: Timon, Hegeso, Polemon, Phila, Agis, Praxon (11 trainers,
5 optional). Items: 7 jars, 5 hidden. Wild: Korantha by day, Persenyx at night, Melisseer
(DISTRIBUTION.md), Glaukoin at dusk; the lakes' sea table (water_tables.sea(33)); a rock-smash table.

## Relic gates you can open now

| Where | Gate | Relic | Behind it |
|---|---|---|---|
| (49,9), (51,9) | two column drums onto two plates | Girdle of Herakles | the stair down to Kore's hollow: TM22 |
| (43,16-18) | the quarry face | Pan's Crook | the quarry: Simmias, Hard Stone, hidden Star Piece |
| (62,14) | fallen rock in the gully | Bronze Hammer | the Iakchos glade: Lampon, Ether, Super Repel |
| (65,4) | the cold torch-stand | Hecate's Torch | the flame relit; a Fire Stone |
| (58,19) | thicket | Demeter's Sickle | Demeter's altar: Kallidike, Big Root |

## Hooks for later

| Where | Gate | Relic (later) | What waits |
|---|---|---|---|
| The jesters' bridge (24,18) and the islet | the missing span, open water | Poseidon's Conch (soon: Astyra's salt well) | Kerkops the jester (a battle) and a Big Pearl. WORLD_EXPLORATION A1 asks for the Winged Talaria and an insult duel for Hermes Favor +5: the duel's script and the Talaria hop are still to build |
| The salt lakes | the goddesses' fish | the Conch, the Super Rod | the priest says only priests may fish them; a sacred-fish quest (a rare Rheitoi catch for the priest) |
| Kore's hollow | a dead end under the court | — | room for an Eleusinian side scene (the Mysteries' night, PITCH Act II) |
| The quarry | a cut face with no stair | — | the marble for the Akropolis: a hook for Astyra's rebuilding after the raid |
| Theoxeny | the spring and the herm | — | the pilgrims' spring is a natural theoxenia stop for Demeter (SYSTEMS) |
