# Route 16, the capital pass

Daphni to Astyra's gate, rebuilt (2026-11-18) from the 48x24 placeholder
`nemea.roads()` wrote for astyra.py. `tools/ichor/maps/sacredway.py` owns it.

| | |
|---|---|
| Size, tilesets | 72x36, Aethos + Skiron (was Kalliste) |
| Levels | wild 34-36 (wild_plan.py's Route 16 tables: Sophowl, Ophidrop), trainers 36-38 |
| Story | Down to the Kephisos, through the potters' graves and past Plato's grove, up the hill to the Dipylon, and the first sight of the Akropolis |

Renders: `design/maps/img/route16_before.png`, `route16_pass1.png`, `route16_pass2.png`,
`route16_after.png`, `route16_after_walk.png`, `route16_after_views.png`.

## Seams

- Daphni's east road (rows 16-19) meets ours at offset 0. Our 8 west columns are aethos only.
- Our gate road, rows 10-13, meets Astyra's west road (its rows 32-35) at offset -22, unchanged; our 8
  east columns are aethos only (Astyra keeps gTileset_Kalliste; seam_audit passes).

## The road

1. **Daphni's foot.** The west sign, Nikias and Timarete over the road (both DOWN 4), the oak wood's
   meadow above the road (an Ultra Ball jar), the vine-dresser's olives below (Hyper Potion, hidden Honey).
2. **The Kephisos.** The river, north to south, crossed on stepping stones; band 1 on the far bank (hidden
   Super Repel). Fishable and surfable; an islet downstream (the Conch).
3. **The Kerameikos.** The tomb street north of the road: grave plots behind a low wall, stelai, lekythoi,
   a sarcophagus, the city's mound. Exekias the potter (the potters' quarter buries its own). Three plots
   open three ways: a fallen drum in a gap (the Girdle: hidden Nugget), rubble in a gap (the Hammer: hidden
   Star Piece), and a family tomb behind a double-axe seal (the Labrys: a Comet Shard). Kleobis tells his
   namesake's story.
4. **The Akademia.** Diotima at the road's narrow; south of it, a thicket (the Sickle) into Athena's olives
   where Aristokles (Plato) teaches: a question, no answer, Wise Glasses. Speusippos, his nephew, battles
   instead of studying; a Leaf Stone jar.
5. **The climb.** The scarp stair with Ariston at its head, band 2 straight after him, Straton on the
   terrace, the great herm. The **lookout**: stepping past the herm the first time, the camera rises over
   the walls to the rock of the Akropolis and the goddess's house on it (FLAG_ICHOR_R16_AKROPOLIS_SEEN);
   the stone seat repeats the view in words.
6. **The Nymphs' shrine** up a Pan's Crook face above the terrace: niches, the Ether jar, hidden Pretty
   Feather. The ledge drops back down to the ditch for the quick way home.
7. **The ditch and the fallen span** (A8): Menexenos on ditch duty, the old border road's broken pier, and
   across the gap a far pier with TM38 Fire Blast (Daedalus's Wings; scripted glide both ways).
8. **The gate road.** Alethea's roadside spot after the ostracism (her confession, unchanged:
   Astyra_EventScript_PlaceRoadAlethea from the map's transition script), Eubios the augur in his nook by
   the gate (optional; the astyra.sh whiteout check battles him), hidden Revive under the walls, the east
   sign, Astyra.

Forced grass: 8 Daphni to Astyra, 5 back (the ledge skips band 2). On the only road: Nikias, Timarete,
Diotima, Ariston, Straton (10 trainers). Items: 7 jars, 6 hidden. Wild: Sophowl and Ophidrop
(wild_plan.py), the Kephisos's pond table (water_tables.pond(35)), a rock-smash table.

## Relic gates you can open now

| Where | Gate | Relic | Behind it |
|---|---|---|---|
| (33,5) | fallen drum in a plot gap | Girdle of Herakles | hidden Nugget |
| (40,5) | rubble in a plot gap | Bronze Hammer | hidden Star Piece |
| (35,20) | thicket | Demeter's Sickle | the Akademia's grove: Aristokles's Wise Glasses, Speusippos, Leaf Stone |
| (48,6-8) | the Nymphs' face | Pan's Crook | the shrine: Ether, hidden Pretty Feather |

## Hooks for later

| Where | Gate | Relic (later) | What waits |
|---|---|---|---|
| The family tomb (29,5) | a double-axe bronze seal | the Labrys | a Comet Shard; Knossian work in an Astyran grave, a lead toward Act III |
| The fallen span (59,19) | the gap to the far pier | Daedalus's Wings | TM38 Fire Blast (A8 asks for the Winged Talaria; the Wings are the relic that glides) |
| The Kephisos islet | open water | Poseidon's Conch (from Astyra's salt well, just ahead) | a Big Pearl |
| The Akademia | Prometheus's altar, the torch race | Hecate's Torch | Aristokles describes the torch race from the grove to the city: a timed relay is unbuilt |
| The lookout | the Akropolis seen from outside | — | after the raid, a second scene could show the uprooted olive from here |
