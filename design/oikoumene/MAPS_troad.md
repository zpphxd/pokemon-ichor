# The Troad's towns and lane: Sestos, the Hellespont, Ilion

Batch 1's troad-towns work (BUILD.md §5): the `troas` outdoor tileset and three maps,
built by code. This file is the map team's notes: what each map is, its seams, doors,
landing tiles, flags, trainers, wild tables, stand-ins and stubs, the render-and-critique
passes, and the audit.

| Map | Builder | Size | Tilesets | Render |
|---|---|---|---|---|
| The Hellespont (`MAP_HELLESPONT`) | `tools/ichor/maps/hellespont.py` | 64 × 34 (14.5 screens) | aethos + troas | `img/hellespont.png` |
| Sestos (`MAP_SESTOS`) | `tools/ichor/maps/sestos.py` | 36 × 30 (7.2 screens) | aethos + troas | `img/sestos.png` |
| Ilion (`MAP_ILION`) | `tools/ichor/maps/ilion.py` | 48 × 42 (13.4 screens) | aethos + troas | `img/ilion.png` |

Each builder writes its layout (`data/layouts/<Map>/`), its size and tilesets in
`layouts.json`, and **its events in `map.json`**, so every coordinate comes from the same
code as the layout. Then it checks: warps on doors and reachable, every door metatile has a
warp, people and triggers on walkable ground, every sign and person readable past the
people standing still, the seams' strips aethos-only, the edges open exactly where recorded.
The shared code is `tools/ichor/maps/troad_lib.py`. Run a builder with `--render DIR` for the
2x render, a collision overlay with the events (`*_walk.png`) and a sheet of screen-sized
crops along the route.

The tileset is `gTileset_Troas` (`tools/ichor/art/troas_build.py`; catalog in
[TILES_troas.md](TILES_troas.md)).

---

## The tileset: `troas`

**476 of 504 tiles** (28 free for batch 2's Troad maps), 448 metatiles in the sheet, 142
cells on borrowed aethos ground (grass, sand, sea: the sea under every rock, ship and current
animates with aethos's water).

**Palette plan (slots 6-12)**, one group a palette, every 8×8 tile in one group:

| Slot group | Holds |
|---|---|
| wood | Akti's wood group slot for slot: the Euploia (Akti's own painter), the landing stage, the Skaian Gate's leaves, hay, dye vats, the chariot |
| marble | Akti's marble group: the temple of Athena, Priam's megaron, the great herm, Hero's lamp, Helle's gilded ram |
| stone | Akti's stone group: Ilion's sloping walls, towers and gates, Hero's tower, the quay, Helle's rock, the current's foam, springs, troughs, the mason's blocks |
| plaster | Trojan houses: ochre lime plaster, packed-clay flat roofs with beam ends, timber |
| plaster2 | the same in whitewash, slot for slot: each `pw` sorts into its `pl`'s slot (Porytiles orders a palette by value), so the white houses reuse the ochre houses' tiles |
| field | wheat gold, reed green, river earth, field flowers |
| grove | Ida's black pines, the valonia oak, Protesilaos's withered elm, the burial mound |

**What it holds**, by section: the plain (wheat as tall grass in 14 soft shapes, the same
wheat as an impassable town crop, the Skamander's banks in 14 shapes over aethos's sea,
reeds, a heroes' burial mound, Ida's pine, a young pine, the oak, the withered elm, flowers
and stones); the Hellespont (the eastward current, four pieces; Helle's rock; a timber
landing stage); Sestos's harbor (Akti's quay, the Euploia and her gangplank's foot, a
bollard); Ilion's walls (the great sloping wall west-east with an offset, north-south runs
and corners, a bastion tower, the open ramp gate, the Skaian Gate's outer face, Hero's
tower with its lamp); the town (the Trojan house kit in ochre and white, Priam's megaron,
the temple of Athena, a great herm, yard things, the twin springs).

**For batch 2:** the Skamander Plain has wheat, reeds, banks (water cells, `MB_OCEAN_WATER`,
elevation 1), mounds, pines and oaks; the Skaian Gate's outer face is the same piece Ilion
uses (its door cells are `MB_NON_ANIMATED_DOOR`, left impassable). The current is eastward
only; the Skamander's "current pushes you downstream" needs a southward set (about 6 tiles).
Tiles within 3 px of another are merged (`troas_build.py`), which is what leaves the 28.

---

## The Hellespont

The sea lane between Thrace (north) and the Troad (south). West to east:

- **The north shore** is COVERAGE's T5, the Hebros Shore's strip: barley, Protesilaos's
  mound at Elaious with its elms withered at the top, the timber landing for Abdera, a
  shore road with one forced band of barley (x 19-21, rocks on the beach under it) and
  Kotys over the narrows at x 24, and the road up to Sestos at x 30-33.
- **The current** fills the middle in staggered races, tapering at both ends, its edges
  ragged. Every fifth cell of a race is slack water, offset two a row, so a surfer crossing
  the strait drifts east one to four cells a row: *cross upstream of where you mean to land*
  (Glaukippos says so after his battle). Going west is only possible in the calm channels
  along the shores. Helle's rock splits the current mid-strait, with slack water either
  side of it. The builder proves the current never carries a surfer into rock, land or a
  swimmer.
- **The south shore** is the Troad: Cape Sigeion with the mound "of Achilles" (its stele
  scratched NOT YET; he's alive at Olympia), the beach where the ships were drawn up and
  the road south to the Skamander Plain, and Rhoiteion with Ajax's mound.
- **The set piece**: Helle's rock and its gilded ram; and on the beach, the old man who
  counts the slipway stones every morning (forty, never a thousand) and gives the Rare Bone
  he dug up by the twelfth (`FLAG_ICHOR_HELLESPONT_GOT_RARE_BONE`).

### Seams

| Edge | Neighbour | Open | Aethos-only strip | Status |
|---|---|---|---|---|
| west (x = 0) | Aethos's Route 20 (world-act2) | rows 8-21, open sea; rows 0-7 and 22-33 wood | x 0-7, every row | no connection yet (`ICHOR_STUB_AETHOS`) |
| east (x = 63) | the Bosporus (pontos-towns), `right`, offset 0 | rows 8-21, open sea; rows 0-7 and 22-33 wood and rock | x 56-63, every row | connected |
| north (y = 0) | Sestos, `up`, offset 28 | x 30-33 the road, x 37-55 the harbor mouth, x 58-60 Hero's point path | none (same tileset) | connected both ways |
| south (y = 33) | the Skamander Plain (batch 2) | x 24-27, the beach road | rows 28-33, every column | no connection yet |

### Trainers

| Id | Name | Where | Class (stand-in → intended) | Party | Sight |
|---|---|---|---|---|---|
| 680 | Glaukippos | west calm water (9,14), first, easy, in plain view | Swimmer M → Argonaut | Pelipper, Cramorant (70) | right 4 |
| 681 | Nerea | the north channel (35,8): **checkpoint** | Swimmer F → Argonaut | Tentacruel, Mantine, Pelipper (71) | down 2 |
| 682 | Euphemos | the south channel (46,19): **checkpoint** | Swimmer M → Argonaut | Clawitzer, Seadra, Wishiwashi (72) | down 3 |
| 683 | Kyane | by the sandbar (36,19) | Swimmer F → Argonaut | Cramorant, Gastrodon (72) | down 3 |
| 684 | Iphitos | the east pool where the races end (55,14) | Swimmer M → Argonaut | Tentacruel, Clawitzer, Pelipper (73) | left 2 |
| 685 | Kotys | the strip's narrows (24,2): **checkpoint** on foot | Shepherd → Shepherd of Ida | Mudsdale, Dubwool, Gogoat (71) | down 5 |
| 686 | Menestheus | Achilles's mound (12,28) | Hoplite → Trojan Hoplite | Pawmot, Medicham, Bisharp (73) | left 3 |
| 687 | Thrasios | Ajax's mound (51,27) | Hoplite → Charioteer | Arcanine, Tauros, Staraptor (74) | left 3 |

The builder proves the checkpoints: with Nerea's and Euphemos's sight cut, no swimmer gets
west past them (the races only go east), and Kotys's sight cuts the strip's road.

### Items

| Kind | Where | Item | Flag |
|---|---|---|---|
| ball | the sandbar (39,20), reached by crossing the current | Pearl String | `FLAG_ICHOR_ITEM_HELLESPONT_PEARL_STRING` (bank 0x3E4) |
| ball | the strip's west end (3,2) | Dive Ball | `FLAG_ICHOR_ITEM_HELLESPONT_DIVE_BALL` (bank 0x3E5) |
| ball | Rhoiteion's grove (58,29) | Max Revive | `FLAG_ICHOR_ITEM_HELLESPONT_MAX_REVIVE` (bank 0x3E6) |
| hidden | the end of the Abdera landing (10,9) | Pearl | `FLAG_ICHOR_HIDDEN_HELLESPONT_PEARL` (0x4C0) |
| hidden | behind Achilles's mound (10,25) | Rare Candy | `FLAG_ICHOR_HIDDEN_HELLESPONT_RARE_CANDY` (0x4C1) |
| hidden | on Helle's rock (32,13), from the slack water east of it | Nugget | `FLAG_ICHOR_HIDDEN_HELLESPONT_NUGGET` (0x4C2) |
| gift | the beach elder (26,31) | Rare Bone | `FLAG_ICHOR_HELLESPONT_GOT_RARE_BONE` (bank 0x3EB) |

**The Abdera landing:** the end of the timber stage, **(10, 9)**, is the marked landing tile
where LABORS's Abdera boat ties up (`ICHOR_STUB_LABORS` on its sign at (9,6)).

### Signs

West end (5,3), the Abdera landing (9,6), the Sestos fork (29,3), east end (58,5), Sigeion
(3,26), the beach road (23,30), Rhoiteion (54,25), Protesilaos's mound (14,3), Achilles's
mound (9,26), Ajax's mound (50,25), Helle's rock (30,14). Every open end has one within
15 cells.

### Wild tables (`src/data/wild_encounters.json`, `gHellespont_*`)

| Table | Rate | Slots | Species | How it meets BUILD §6 |
|---|---|---|---|---|
| land, Morning | 25 | 12 | Mudsdale, Exploud, Fearow, Swellow, Gumshoos, Pelipper, Farfetch'd, Cramorant, Mr. Rime (62-66) | T5's homes (Exploud, Mudsdale, Mr. Rime) and its listed shares; 9 species; band 62-66 |
| land, Day | 25 | 12 | the same nine, Gumshoos and Swellow up front | 9 species |
| land, Evening and Night | 25 | 12 | Noctowl (×3), Mudsdale, Exploud, Farfetch'd, Fearow, Mr. Rime, Pelipper, Cramorant | 8 species; the night bird replaces the day's |
| surf | 10 | 5 | Pelipper, Cramorant (T1's homes), Tentacruel, Mantine, Clawitzer (60-62) | T1 has no shares and the Troad no other water species; the strait is the Black Sea's outflow, so the rest are the Bosporus's (E1, E2) |
| fishing | 30 | 2/3/5 | Old: Wishiwashi, Tentacruel. Good: Seadra, Wishiwashi, Clawitzer. Super: Seadra, Clawitzer, Wishiwashi, Tentacruel, Seadra (60-62) | COVERAGE gives T1 no fishing; these are the Bosporus's (E2's homes Seadra and Wishiwashi, E1's Clawitzer); 4 species, none in most slots |
| Augur's Eye | — | 3 | Mr. Rime, Farfetch'd, Mantine | see "Augur's Eye" below |

Sestos's harbor is the strait's water: `gSestos_Morning` has the same surf and fishing
tables. Ilion has no water and no land table (its wheat is an impassable crop).

**Augur's Eye.** `wild_encounters.json` had no `hidden_mons` field, so no map's hidden slots
compiled. This branch adds the field (rates 50/40/10) and guards the template's hard-coded
`NUM_HIDDEN_MONS_ENCOUNTER_SLOTS` with `#ifndef`
(`src/data/wild_encounters.constants.json.txt`). Other agents adding the same field will
conflict on that one line of `fields`; keep one.

---

## Sestos

The ferry town on the European shore. The harbor opens south onto the strait; an L of
quays runs round the inner basin, where **the Euploia** lies moored north of the mole with
her gangplank down onto it. **Nausikles** stands at the gangplank's foot, **(12, 23)**, and
runs `Oik_EventScript_SailHome` (`ICHOR_STUB_SHIP`: the tile where world-postgame's
gangplank and `EventScript_IchorBoardShip` go). **Hero's tower** stands on the eastern
point with her lamp on top. The Asclepeion and the Agora face the quay street; the net-loft
(a tall white house) and the ferry house are beside them. Up the hill: the crossroads herm
(`ICHOR_STUB_HERM`), walled bean rows and a wheat plot, and the old acropolis wall with its
open gate, a tower, and a grove behind it with the Star Piece.

**Alethea's quay scene.** She waits at the mole's root, (7,22), hidden by
`FLAG_ICHOR_OIKOUMENE_ARRIVED`. Coord triggers at **(8,23) and (8,24)**, armed by
`VAR_TEMP_1 == 0` from ON_TRANSITION while the flag is clear, are the only way off the mole
(the builder proves it): she steps down beside the player, runs
`Oik_EventScript_AletheaQuay` (which sets the flag), adds a Sestos line ("Start with that
tower…"), and walks off. Talking to her first plays the same scene. Landing first at
another port hides her.

| Warp | Door | Leads to |
|---|---|---|
| 0 | (5,14) | `MAP_SESTOS_ASCLEPEION` warp 0 |
| 1 | (10,14) | `MAP_SESTOS_AGORA` warp 0 |
| 2 | (27,26), Hero's tower | `MAP_SESTOS_HEROS_TOWER` warp 0 |
| 3 | (21,14) | `MAP_SESTOS_FERRY_HOUSE` warp 0 |
| 4 | (15,14) | `MAP_SESTOS_NET_LOFT` warp 0 |

**Wings landing: (5, 15)**, the street in front of the Asclepeion's door.

**Seam:** the south edge is the Hellespont's north edge (`down`, offset -28): open at x 2-5
(the road to the Hebros strip), x 9-27 (the harbor mouth, water), x 30-32 (Hero's point's
path). Same tileset on both sides. Signs at both: (5,27) and (29,28).

**Items:** Star Piece ball in the acropolis grove (18,1) (`FLAG_ICHOR_ITEM_SESTOS_STAR_PIECE`,
bank 0x3E7); hidden Heart Scale at the mole's end (20,24) (0x4C3); hidden Ultra Ball in the
headland's trees (34,11) (0x4C4).

**People:** the quay fisher (the net-loft's rod), a sailor (the current), Demo mending nets
(Hero's lamp), a kid (Leander), the tower watcher (the windy stair: the Fire Stone hook),
Phanias at the herm (the ferry's never on time), the acropolis guard (the view of Troy), a
gardener (beans).

---

## Ilion

Troy on its hill. **The citadel (the Pergamos)** holds the top inside the great sloping walls:
the temple of Athena is the crown at the summit with its paved forecourt, Priam's megaron
with its frieze of horses beside it, Cassandra's white house, the drill yard where two
hoplites practise, and the Palladion's old pedestal stones. **The Skaian Gate** stands at the
west end of the wall, barred, a guard before it (`ICHOR_STUB_HALL`), with the oak and the twin
springs below it, where the women still do the washing. The open **ramp gate** leads up from
the main street, an avenue of cypresses. **The lower town**: the Asclepeion and the Agora
face the road in from the plain; the weaver's with her dye vats, the mason's with his
blocks and drums, the guest-room by the Ida road, the horse-breeder's walled yard with hay,
trough and chariot, a paved crossroads square, gardens, and the town's wheat fields.

| Warp | Door | Leads to |
|---|---|---|
| 0 | (10,29) | `MAP_ILION_ASCLEPEION` |
| 1 | (15,29) | `MAP_ILION_AGORA` |
| 2 | (13,8) | `MAP_ILION_PRIAMS_PALACE` |
| 3 | (31,8) | `MAP_ILION_CASSANDRAS_ROOM` |
| 4 | (34,28) | `MAP_ILION_GUEST_ROOM` |
| 5 | (10,37), the stable's double door | `MAP_ILION_HORSE_STABLE` |
| 6 | (34,20) | `MAP_ILION_MASONS_HOUSE` |
| 7 | (19,22) | `MAP_ILION_WEAVERS_HOUSE` |
| 8 | (23,5), the temple | `MAP_ILION_TEMPLE_OF_ATHENA` |

Each to its room's warp 0. **The Skaian Gate's doors** are (11,15) and (12,15): door
metatiles, impassable, no warp; batch 2's hall opens one and adds its warp after warp 8.

**Wings landing: (10, 30)**, in front of the Asclepeion's door.

**Seams, both left open for batch 2** (no connection yet):

| Edge | Neighbour | Open rows | Aethos-only strip |
|---|---|---|---|
| west (x = 0) | the Skamander Plain | 30-33 (the road on 31-32) | x 0-7, every row |
| east (x = 47) | the Ida Road | 30-33 (the road on 31-32) | x 40-47, every row |

North and south edges are shut. Signs at both gates: (4,30) and (43,33).

**Trainers:** 688 Agenor and 689 Polites in the drill yard (Hoplite → Trojan Hoplite; Lv 72,
73), 690 Hippothoos in the horse yard (Hoplite → Charioteer; Lv 74), 691 Anchises by the Ida
road (Shepherd → Shepherd of Ida; Lv 70). All optional; a city has no route checkpoints.

**Items:** Hard Stone ball in the mason's garden (36,23) (bank 0x3E8), PP Up in the
citadel's east corner (37,11) (bank 0x3E9), Elixir in the citadel's west corner behind the
palace (9,12) (bank 0x3EA); hidden Leaf Stone under the Skaian oak (15,19) (0x4C5), Revival
Herb at the citadel's east corner (39,15) (0x4C6), Star Piece in the horse yard (9,39)
(0x4C7).

**People** (the war "was a summer"; Cassandra has stopped seeing Troy burn): the washerwoman
at the springs, a grandmother (Cassandra), the crier ("the city still stands!"), a kid (the
horse was a cart of wine), a veteran ("a long summer, mind"), Theano the priestess (the
Palladion), a spinner (the weaver needs dyes: the peplos quest), a quarryman (the mason's
chisel in the undercroft: the Walls of Laomedon), a traveler (the grumbling river), the
ramp gate's guard.

---

## Flags and ids claimed

- **Bank flags** (0x3E4-0x3F3): 0x3E4-0x3EA item balls (7), 0x3EB the Rare Bone. 8 of 16 left.
- **Vanilla flags** (0x4C0-0x4C7): all eight, the hidden items (3 Hellespont, 2 Sestos, 3 Ilion).
- **Trainers** 680-691 (`TRAINERS_END_OIKOUMENE` 692). 927-934 unused.
- **Existing:** `FLAG_ICHOR_OIKOUMENE_ARRIVED` (Alethea), `VAR_TEMP_1` (Sestos's scene).

`ICHOR_STUB_HIDDEN`: none; every map has the two hidden items the standard asks for.

---

## Stand-ins

| Object | Now | Intended |
|---|---|---|
| Hellespont swimmers (Glaukippos, Euphemos, Iphitos) | `OBJ_EVENT_GFX_SWIMMER_M`, class Swimmer M | an Oikoumene swimmer sprite; class Argonaut |
| Hellespont swimmers (Nerea, Kyane) | `OBJ_EVENT_GFX_SWIMMER_F`, class Swimmer F | the same; class Argonaut |
| Kotys, Anchises | `OBJ_EVENT_GFX_ICHOR_SHEPHERD`, class Shepherd | Shepherd of Ida |
| Menestheus, Agenor, Polites, the Skaian guard, the ramp guard | `OBJ_EVENT_GFX_ICHOR_HOPLITE`, class Hoplite | `OBJ_EVENT_GFX_ICHOR_TROJAN_HOPLITE`; class Trojan Hoplite |
| Thrasios, Hippothoos | `OBJ_EVENT_GFX_ICHOR_HOPLITE`, class Hoplite | a Charioteer sprite; class Charioteer |
| Ilion's men (the crier, the quarryman) | `OBJ_EVENT_GFX_ICHOR_MAN` | `OBJ_EVENT_GFX_ICHOR_TROJAN_M` |
| Ilion's women (the washerwoman, the spinner) | `OBJ_EVENT_GFX_ICHOR_WOMAN` | `OBJ_EVENT_GFX_ICHOR_TROJAN_F` |
| Sestos's tower watcher | `OBJ_EVENT_GFX_ICHOR_ELDER_F` | stays (Hero herself, `OBJ_EVENT_GFX_ICHOR_HERO_LAMPKEEPER`, is the rooms agent's, in the tower) |
| Theano | `OBJ_EVENT_GFX_ICHOR_PRIESTESS` | stays |
| Gulls over the strait | `OBJ_EVENT_GFX_SPECIES(WINGULL)` | stays (Akti's gulls) |

Priam, Cassandra and Hektor (`_PRIAM`, `_CASSANDRA`, `_HEKTOR`) are indoors or in the hall,
so no outdoor object uses them yet. Every trainer party carries a
`/* ICHOR_STUB_CLASS: … */` comment in `src/data/trainers.party`.

**Music** (`ICHOR_STUB_MUSIC`, set in each map.json): the Hellespont plays
`MUS_ICHOR_TRIREME` for *The Wider World*; Sestos `MUS_ICHOR_AKTI` and Ilion
`MUS_ICHOR_EMPORION` for *The Plain of Troy*.

## Stubs

`grep -rn ICHOR_STUB_` finds: `ICHOR_STUB_SHIP` (Nausikles, Sestos), `ICHOR_STUB_HERM` (the
crossroads herm, Sestos), `ICHOR_STUB_HALL` (the Skaian Gate's guard and doors, Ilion),
`ICHOR_STUB_LABORS` (the Abdera landing's sign, the Hellespont), `ICHOR_STUB_SPRITE` (the
swimmers' and Trojans' objects, in the builders), `ICHOR_STUB_CLASS` (every party).

---

## Render-and-critique passes

### The Hellespont

1. **First build.** The lane worked but read as a diagram: the current a hard rectangle; the
   forests packed into rows, their leftover cells filled with rows of boulders along the
   south shore; the sandbar a broken U (a notch of sea in its top row drew wrong edges); the
   barley in plain rectangles; and the water's north-east (Sestos's mouth) empty. The checks
   also caught two things: the strip's beach row is the sand's *water-edge* row, so a surfer
   could slip west past Nerea along the beach; and an oak's east column stood in the
   Bosporus seam's aethos-only strip.
   **Changed:** the bluff at x 34-36 runs into the water as rocks; the oak became an olive.
2. **Shapes.** The current now tapers toward both ends with a ragged top and bottom (full
   height at the two checkpoint columns, so the proof still holds); the sandbar is a rounded
   island; barley comes in irregular patches with a reason each (the herdsman's nook, the
   Dive Ball's hollow); tongues of grass break the north beach; a line of dune reeds stands
   behind the south beach; sea rocks in loose clusters near the shores and in the harbor
   mouth; three gulls.
   **Changed in the wood:** trees are planted in a scrambled order (big ones first), and only
   the map's own edge is closed with cut cypresses, so a gap inside a wood stays a glade
   instead of a boulder.
3. **Purpose.** The audit found no set piece it could recognise and wanted signs at every
   open end. **Changed:** the beach elder became the beach's set piece (the forty slipway
   stones and the Rare Bone); signs checked against every end. Still to watch: the south
   beach is broad and plain at 1x; batch 2's Skamander mouth would give it a river.

### Sestos

1. **First build.** The harbor read at once (the ship, the mole, the tower), but the map's
   side edges were rows of boulders, the north edge was open at the acropolis path, and the
   mole's triggers (then at x 7) could be walked round up the west quay.
   **Changed:** wooded edges; the acropolis path stops in a grove; the triggers moved to x 8,
   the only way off the mole (proved).
2. **Edges and paths.** The quay street ran into both side edges. **Changed:** it ends in
   trees; the scrambled forests replace the regular rows; the item and the grove sit inside
   the acropolis wall.
3. **The upper town was bare grass.** **Changed:** dry-stone walls round the bean rows
   (west) and a wheat plot (east), cypresses and an olive along the lane, the ferryman's
   herb bed, stacked blocks on the quay, signs at the two seam ends. Still plain: the
   strip of grass east of the ferry house.

### Ilion

1. **First build.** The citadel and walls read well (the Skaian Gate with its shields, the
   towers, the ramp gate), but the woods were plantation rows, the lower town was wide
   empty grass with the houses far apart, both edges of the map leaked (an olive's crown at
   the top, the main street at the bottom), the stable's door faced the yard's wall, and
   wheat in town would have needed a land table.
   **Changed:** the yard's gate moved to its east side; the edges shut; the town's wheat is
   now `wheat_crop`, impassable, with no encounters.
2. **Woods.** The scrambled forests: mixed olives, pines and cypresses at irregular depth.
3. **The town.** **Changed:** the temple's forecourt and the crossroads square are paved in
   ashlar; a cypress avenue climbs the main street to the ramp gate; a walled kitchen garden
   by the springs; the mason's bean rows; the Elixir in the dead end behind the palace (the
   audit's). Still to do: the lower town's east side (between the guest-room and the wood)
   wants another yard or garden; the Trojan townsfolk's own sprites will help the streets.

---

## Tests

`tools/ichor/tests/troad_towns.sh` (with `troad_towns.lua`, `troad_towns.py` and
`troad_towns_setup.s`): see the results below.

## The audit

`map_audit.py --root . Sestos Hellespont Ilion` (the lead's script): see below.

## Open questions

- **Ilion and Lazarus's Ilios.** LAZARUS.md names its region *Ilios*. Ilion is the bible's
  name and the city's own; the director may want to confirm it's distinct enough.
- **The current runs east** as OIKOUMENE §4.1 says; the real Hellespont's surface current
  runs west, out of the Black Sea. Kept as the bible has it.
- **Fishing on T1.** COVERAGE gives the Hellespont no fishing species; the tables borrow the
  Bosporus's. A COVERAGE entry would settle it.
- **`hidden_mons`.** Adding the field to `wild_encounters.json` is shared ground; other
  Oikoumene agents will meet it too.
