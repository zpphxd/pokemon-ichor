# Route 13, Nemea, Route 14 and the Tretos

The return loop from Arkadia to Emporion, rebuilt (2026-11-17) from the bare
placeholder stops. `tools/ichor/maps/nemea.py` owns all four outdoor/cave maps
and the events of Nemea's two rooms; `tools/ichor/maps/nemea_rooms.py` lays out
the rooms on gTileset_Domos. Run `/usr/bin/python3 tools/ichor/maps/nemea.py
--render design/maps/img --stem-suffix _after` to rebuild and re-render.

| Map | Size | Tilesets | What it is |
|---|---|---|---|
| Route13_HighlandRoad | 56x28 | Aethos + Skiron | Down out of Arkadia: oak wood, the scarp and its stair, the valley road, a ford |
| Nemea | 44x36 | Aethos + Skiron | The Games' valley: palaestra, Zeus's ruined temple, stadium, outcamp, the lion's den |
| Nemea_Palaestra | 16x11 | Oikos + Domos | The Games' wrestling hall (a trainer and a gift) |
| Nemea_MolorchosHouse | 11x8 | Oikos + Domos | Molorchos's cottage (a small quest) |
| Route14_NemeaRoad | 80x26 | Aethos + Skiron | The Tretos road: valley, gorge stair, the limestone ridge, the ravine, the Isthmus plain |
| Route14_Tretos | 36x20 | Aethos + CaveDark | The pass under the ridge: dark, required, with relic gates now and later |

Renders: `design/maps/img/{route13,nemea,route14,tretos}_{pass1,pass2,after}.png`,
the `_before` images of the old maps (`route13_highland_road_before.png`,
`nemea_before.png`, `route14_nemea_road_before.png`), and `_after_walk.png`
(collision, grass, sight lines) and `_after_views.png` (15x10 views). Rooms:
`design/phase2/img/nemea_palaestra.png`, `nemea_molorchos.png`.

## Seams

- Arkadia's right edge (rows 22-25) meets Route 13's left (rows 10-13), offset -12, unchanged. Route 13's 8 west columns are aethos-only.
- Route 13 / Nemea / Route 14 share gTileset_Skiron, so their seams need no strip. Road rows 17-18 on both seams, offsets 0.
- Route 14's exit is its row 13 at x 79 (the 8 east columns are aethos olives), meeting Emporion's one-tile Nemea Gate at y 41: Route 14's right offset is -28 and Emporion's left offset is 28 (written by `emporion_connection()`). Emporion's hoplite and FLAG_ICHOR_ARKADIA_NORTH_OPEN are unchanged.
- Route 14's two cave mouths (29,7) and (49,8) are warps 0 and 1 to the Tretos's west (0,9) and east (35,9) arrow exits.

## The road, map by map

**Route 13.** Arkadia's cypresses and a sheep meadow; Polydoros the border hoplite in plain view; the oak wood with band 1 and Anthe over the road; the clearing and the great herm; the high meadow (beekeeper's gift, hives with hidden Honey, a jar); the hermit's cell behind rubble (the Hammer, Max Ether); the glade behind a thicket (the Sickle, Moon Stone); the rim that hops back down by a ledge; the scarp with its cut stair and rock-cut niches; Lykon at the stair foot, band 2, the ford over the brook (fishable) and Kallias; the lower wood with Pan's stele and Theano; Aglaon's south meadow. Forced grass 8. Mandatory: Anthe, Lykon, Kallias.

**Nemea.** The healer's tent (HEAL_LOCATION_NEMEA, respawn in front of her at (12,16)) and the merchant's cart on the road. North: the palaestra (enterable), Zeus's temple on a stepped platform with its fallen drums, column stumps and altar, Opheltes's mound, the Langia spring, the sweeper who tells the lion's story. East: the lion's den in a four-row cliff, lion grass before it. South: Molorchos's cottage (enterable) and his tilled plot, the stadium track with its stone seats, tunnel and turning posts, the athletes' outcamp (tents, cookfire, a runner and a discus thrower), and the river pool with its islet.

**Route 14.** The hills' sheep meadow (herdsman's gift), Ison and band 0, the gorge stair, Philomele and band 1 in the gorge, the herm, the west mouth. Below: the stream bed (fishable) with Neokles and a gully behind rubble (the Hammer, Hard Stone). The ridge is bare limestone with a pine terrace. East: Erato in the slot under the ridge, the ravine stream and ford, band 2 and Demades, the knoll (Klearchos, a jar, the honey) with a stair up and a one-cell ledge back down, the south meadow behind a thicket (the Sickle; Dorkon, an Ether), the pool's islet, Antikles at the olives, and the Isthmus plain. Forced grass 8 (Nemea to the mouth), 4 east of the ridge. Mandatory: Ison, Philomele, Demades, Antikles.

**The Tretos.** Dark (requires_flash; Hecate's Torch lights it). Rubble shuts the neck on the only road (the Hammer, persistent once broken). The chamber's brazier (FLAG_ICHOR_BRAZIERS_START + 0x2E) lights the whole cave for good once lit. Lysandra, Hecate's acolyte, keeps it. A cobweb over the bone room (the Torch: Dusk Ball, hidden Escape Rope). The pool's islet, the thornweb's deep room and the boulder tunnel are later gates (below). One floor: 4 jars, 2 hidden, 1 trainer, a ledge down to the east mouth.

## Relic gates you can open now

| Where | Gate | Relic | Behind it |
|---|---|---|---|
| Route 13 (23,5) | rubble | Bronze Hammer | the hermit's cell: Max Ether, the bee stele |
| Route 13 (46,5) | thicket | Demeter's Sickle | the glade: Moon Stone, long grass |
| Route 14 (9,22) | rubble | Bronze Hammer | the gully: Hard Stone, a grass pocket |
| Route 14 (64,15) | thicket | Demeter's Sickle | the south meadow: Ether, Dorkon |
| Route 14 (45,3) | column drum | Girdle of Herakles | a one-way shortcut west over the ridge top, back toward Nemea (push it north from (45,4); a ledge drops into the gorge) |
| Tretos (10,9) | rubble on the only road | Bronze Hammer | the way through |
| Tretos (14,3) | cobweb | Hecate's Torch | the bone room: Dusk Ball, Escape Rope |
| Tretos (17,4) | brazier | Hecate's Torch | the whole cave lit, for good |

## Hooks for later

Every closed thing here is visible from where the player stands, with a line that says what it wants.

| Where | Gate | Relic (later) | Reward behind it |
|---|---|---|---|
| Nemea (36,9) | great boulder over the lion's den's low mouth | Hephaestus's Hammer | the den itself: **Labor 1, the Nemean Lion** (post-game). Not built; the den map comes with the Labors. FLAG_ICHOR_NEMEA_LION_BOULDER |
| Nemea (40,7) | the den's high mouth, handholds up the cliff (sign at (40,8)) | the climbing relic | the den's upper chamber (Labor 1's second way in) |
| Nemea, the den | sealed until the Labors | story (Labor 1) | the lion; Molorchos's "thirty days" line pays off |
| Nemea (27-29,8-10) | the Langia spring's waterfall, "a hollow behind the fall" | Horn of Achelous | a grotto behind the fall (not built): an amphora or Opheltes's relic |
| Nemea (36,31) | the river pool's islet | Poseidon's Conch | Big Pearl (FLAG_ICHOR_ITEM_NEMEA_ISLET); the pool also gets a surf table now |
| Nemea (2,28-29) | the athletes' tunnel, bricked up, wings scratched on it | Winged Talaria (gap-jump/sprint upgrade) | the stadium race with the runner in the outcamp and Chionis in the palaestra (a minigame hook) |
| Route 13 (47,12) | the crag pocket above the scarp: **built**, Pan's Crook's face at (47,14-16) (Skiron `crook`) | Pan's Crook | PP Up (FLAG_ICHOR_ITEM_R13_CRAG) |
| Route 14 (11,5) | great boulder closing the gorge's north cleft | Hephaestus's Hammer | the lion hunters' stele and nook, with a hidden Super Repel (FLAG_ICHOR_HIDDEN_ITEM_R14_REPEL) FLAG_ICHOR_R14_GREAT_BOULDER |
| Route 14 (54-55,19-21) | the ravine pool's islet | Poseidon's Conch | Pearl (FLAG_ICHOR_ITEM_R14_ISLET) |
| Route 14, the stream bed | the stream "goes into the hill and never comes out" (Neokles) | Poseidon's Conch | surfable now-unreachable water; leads the eye to the Tretos's pool |
| Tretos (19,10) | the underground pool's islet | Poseidon's Conch | Big Pearl (FLAG_ICHOR_ITEM_TRETOS_POOL) |
| Tretos (22,15) | thornweb | the Three-Flamed Torch | the deep room: Protein (FLAG_ICHOR_ITEM_TRETOS_DEEP); room for a later trainer or amphora |
| Tretos (29,8) | great boulder over the north tunnel | Hephaestus's Hammer | the claw-marked tunnel toward the den (stele at (30,2)): the Tretos side of Labor 1, a future warp into the lion's den. FLAG_ICHOR_TRETOS_GREAT_BOULDER |

Climbing faces to tag for the climbing relic: Route 13's scarp at (47,14-16) under the crag pocket, and Nemea's den cliff at (40,5-8) under the high mouth.

## Missing pieces (STYLE.md)

- **A standing Doric column** (1x3, Skiron) for Nemea's three standing temple columns. Stele stumps stand in for now.
- **Vine rows on tilled soil** for a vineyard; Molorchos's plot is bare soil.
- **Handholds** cut in a cliff face (Skiron cliff variant) for the climbing gates; signs mark them for now.
- **A sand-backed rock** (rocks on sand show their grass corner), and **concave pool corners** for the aethos shore set (pool corners use straight edges).

## New ids

- Trainers 296-299 (top of Act II's block, so a parallel session taking the next free id can't collide): TRAINER_ICHOR_R14_ANTIKLES, _R14_DORKON, _TRETOS_LYSANDRA, _NEMEA_KLEITOMACHOS (shown as KLEITOS). Parties in `/* Nemea rebuild teams */` in `src/data/trainers.party`, levels 35-37.
- Bank flags from world-act2's 0x620-0x63F slice (second bank 0x120-0x13A); see `include/constants/flags.h`.
- Brazier index +0x2E (world-act2's +0x20-0x2F block).
- Wild: Route 13 30-32, Nemea 31-33, Route 14 31-33, the Tretos 32-34; pond surf/fishing tables (`water_tables.pond`) on all four, rock-smash tables on Route 13, Route 14 and the Tretos.
