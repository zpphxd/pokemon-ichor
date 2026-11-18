# The Erymanthian Preserve

Artemis's hunting park on Mount Erymanthos, beside Arkadia. It is Ichor's Safari Zone (IDEAS, 2026-11-18).

- **Built by:** `tools/ichor/maps/erymanthos.py` (layouts, events, scripts, checks and renders; it also writes the lodge's hut into Arkadia's west road).
- **Wild tables:** `tools/ichor/wild_plan.py` (design/DISTRIBUTION.md §4).
- **Engine:** upstream's Safari Zone, with the switches in `include/config/ichor.h` (`ICHOR_SAFARI_PRESERVE`).
- **Test:** `tools/ichor/tests/preserve.sh`.

## The hunt

- **The lodge.** Arkadia's west road ends at a hunters' hut dug into the hill: Arkadia's charcoal-hut front, copied to (3,33). Its door, (5,35), leads into the lodge.
  - The room is the charcoal hut's, cleared of its coal and given a stool and a second stack of spear shafts.
  - Melanippe, Artemis's keeper, explains the rules ("caught, not beaten"), checks there is room in the party or the Pithos, and takes ¥500.
  - She hands over 30 Pan Balls (`ICHOR_SAFARI_BALLS`) and walks the player to the Oakwood's gate.
  - The hunt lasts 500 steps (`ICHOR_SAFARI_STEPS`).
- **In battle:** Ball, Barley, Stone, Run.
  - Barley makes the quarry slow to flee but harder to catch. A stone does the reverse.
  - These are FRLG's bait and rock, switched on by `ICHOR_SAFARI_BAIT_ROCK` in place of the cut Pokéblocks. Their lines read "tossed some barley" and "threw a stone".
- **The start menu** shows the steps and Pan Balls left. It offers Retire.
- **Ending the hunt.** Ring the bell at the gate, run out of Pan Balls, or spend the last step: "Ding-dong! The keeper's bell." Any of the three walks the player back to (5,5) in the lodge, where Melanippe says goodbye. The exits live in `data/scripts/safari_zone.inc`.
- **No herm.** The Preserve isn't a town and has no healer, so MAP_DESIGN §7's herm rule doesn't apply. Arkadia's herm is a minute's walk away.

## The maps (gTileset_Aethos + gTileset_Stymphalia; the cave on gTileset_CaveDark)

Every area is `"ichor_kind": "safari"`. map_audit judges a safari area on these:

- its grass, per screen as a route of its band;
- an item ball and a hidden item;
- a sign at each end;
- its wild tables.

It does not require trainers (a Safari battle can't fight them) or forced grass.

| Map | Size | What's there |
|---|---|---|
| **The Oakwood** | 40x34 | Holm oaks, walnuts and planes round glades. The gate's glade (the keeper's sign and bell, a huntress who explains barley and stones), the long glade the road climbs through, the crossroads and the clearing of long grass, Artemis's spring in the west glade, and the north-east and south-east glades. Roads out: north to the High Meadow (x 12–13), east to the River (rows 12–13) |
| **The High Meadow** | 40x30 | Long grass wall to wall above the trees. A ragged limestone band with a stair cut through it (x 12) and a ledge to hop back down. Scree, a goatherd, and the cold cave's mouth in a crag (31,8). In the top-left corner, a one-cell gap choked with fallen oaks (6,2) leads to the Thicket |
| **The River** | 32x34 | The Erymanthos swinging down the middle. A sand bar, stepping stones across at rows 22–23, the angler's stilt hut, a reedy backwater, and the far bank's long grass. Rods work from every bank; the Conch takes you onto the water |
| **The Cold Cave** | 26x18 | A seep cave: the first hall, the frost hall under a crack of daylight (a stele: "THE COLD KEEPS. SO DO WE."), and the seep's pool. Lit, so no Torch is needed |
| **The Boar's Thicket** | 26x22 | Post-game. Oaks rooted up round the boar's wallow of bare scree, and Atalanta's cairn ("ATALANTA WAS HERE. SO WAS THE BOAR. NOT FOR LONG.") |

## Finds

| Map | Items | Hidden |
|---|---|---|
| Oakwood | Big Mushroom (south-east glade), Tiny Mushroom (west pocket) | Moon Stone (by the spring), Ether (north-east glade) |
| High Meadow | Never-Melt Ice (east scree), Revive (lower meadow) | Stardust (the ledge), Ice Stone (west scree) |
| River | Mystic Water (far bank), Net Ball (west bank) | Pearl (sand bar), Heart Scale (west bank's south end) |
| Cold Cave | Ice Stone | Never-Melt Ice (frost hall), Escape Rope (rock pile) |
| Thicket | Big Root, Sitrus Berry | Rare Candy (the wallow), Ether (the cairn) |

## The post-game hook: Labor 4

The fallen oaks across the High Meadow's gap carry `FLAG_ICHOR_ERYMANTHIAN_BOAR`. It is a post-game bank flag, unset until Labor 4.

- **Setting it:** LABORS.md's Erymanthian Boar sets it when the boar is caught. Labor 4 isn't built yet, so nothing sets it today.
- **Until then:** the oaks are scored with tusks, and "something has to be done about whatever tore them up".
- **After:** the oaks are gone and the Thicket opens, with Kaprodon in its table at the post-game's 58–62.

OIKOUMENE_GUIDE §12's Labor 4 row now says the thicket opens, not the high meadow; the meadow is open from the first visit. The Labor's own maps, Erymanthos Slopes and the Snowfield, still lie beyond, as LABORS.md designs them.

## The story

The west road is where Kleon's recruitment scene waits (`Arkadia_EventScript_Recruitment`, the triggers at x 9). A player who walks to the lodge before that scene has played will see it first. The scene plays the same either way.

## Reviews

Three render passes, in `design/maps/img/preserve_*`:

1. **Pass 1** (`preserve_*_pass1.png`):
   - the painter's woods read as a park of loose bushes;
   - the glades were rectangles;
   - the meadow's crag was a dark slab and its band a ruled line;
   - the river's reeds were isolated dark squares and the ford ran onto the banks.
2. **Pass 2** (`_pass2`):
   - a holm-oak canopy laid on a staggered 2x2 lattice, with walnuts and planes among it;
   - the glades drawn as blobs;
   - the reeds moved into a backwater;
   - the river given smooth bends.
3. **After** (`_after`, `_after_views`, `_after_walk`):
   - a broader crag face round the cave mouth;
   - a ragged band with clefts;
   - stepping stones over the water only;
   - closed pockets fixed.

`preserve_arkadia_lodge_after.png` shows the hut on Arkadia's west road. Nothing is cut off on any map, and map_audit and map_style_audit report no FAILs.
