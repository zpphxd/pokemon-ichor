# Emporion: the city and its harbor district

Built by `tools/ichor/maps/emporion.py` (`MAP_EMPORION_CITY`, 48×46, aethos + emporion) and `tools/ichor/maps/emporion_harbor.py` (`MAP_EMPORION_HARBOR`, 48×26, aethos + isthmos). Run either with `--render DIR` for a 2x render, a collision overlay with the events, and screen-sized crops along the player's route. Both builders check their map on every run: warps on doors and every door warped, people and triggers on open ground, every sign and person reachable past the people who stand still, the scenes' walking paths open, the seam rows aethos only, and the seams open exactly at their roads.

The scripts are in `data/maps/EmporionCity/scripts.pory` and `data/maps/EmporionHarbor/scripts.pory`; `design/phase2/BUILD.md` has the connections, warp ids, arrival tile, flags and stubs. `tools/ichor/tests/emporion.sh` plays it all.

| Image | Shows |
|---|---|
| `img/emporion_city.png`, `img/emporion_harbor.png` | The final layouts, 2x |
| `img/emporion_city_walk.png`, `img/emporion_harbor_walk.png` | The same with impassable cells red, water blue, people (yellow rings), warps (cyan), triggers (magenta), signs (white crosses) and hidden items (green crosses) |
| `img/emporion_city_screens.png`, `img/emporion_harbor_screens.png` | 15×10 views along the route (the map's border shows past its edges; in game the neighbour map draws there) |
| `img/emporion_*_pass1.png`, `_pass2.png` | The first two render passes |
| `img/emporion_ingame.png` | In-game frames from the headless check: beat 11 on the quay, the harbor's people, the Agora, Number Nine, Acrocorinth's stair, beat 14 and beat 16 |

## How the two maps fit

Emporion is Corinth on its Isthmus. The *Euploia* comes up the Saronic Gulf into the eastern harbor, a district outside the walls on `isthmos`; the city stands above it on `emporion`. They join by a **map connection**: the harbor road runs north from the quay straight up the city's main street to the Temple of Hermes, so the crown is framed by the street from the quay. The connection costs a band of aethos-only ground on each side (MAP_DESIGN §5: the two maps have different secondaries), twelve rows in all, which is drawn as what lay between Corinth and its harbors: a road lined with cypresses through olive gardens, a fork sign, and the Nemea road branching west. A gate warp would have saved the band, but neither tileset has a city gateway, and the street would no longer run unbroken from the quay to the temple.

The city's other edges: the **Isthmus Gate** on the north seam at x = 7..9 (Route 4, batch 3), in the city wall across the crag's wooded slope; its rows 0–5 are aethos only, so Route 4 can join whatever its secondary. The **Nemea gate** (Route 14, Act II) is a gap in the west wall at row 41, shut by a hoplite; columns 0–7 below row 32 are kept aethos for the day it becomes a connection.

## The city (`MAP_EMPORION_CITY`)

South to north, as SCRIPT.md's "Layout" has it:
- **The harbor road** (rows 40–45, aethos): cypresses along the road, olive gardens, the fork stele, the Nemea gate with its hoplite and stele.
- **The harbor quarter:** the **Asclepeion** on its steps just inside the city, west of the main street, the first building on the way in; the **Deigma** (a stoa with a door bay) across the street; the metic at its end, the Repel behind it; a herb garden and Asclepius's tripod among olives to the west; a cypress court to the east.
- **The Agora:** the long stoa on the square's north-west side, with the spice and scroll counters (sellers behind them), the potter's bay and its stylobate; the six empty pithoi in front of it; Pegasus on his column; two rows of stalls (the general stall facing the main street, the offerings stall, Pasion's table, Kydon's bull-leaper awning; Sykeas's figs with the snatcher on his awning, the fishmonger, cloth and wine); Number Nine on his plinth; the notice board (the Agora's sign); the crossroads great herm; exedra benches; and the Dolphin on the north-east side. The main street through it is an avenue of laurels in great pots, and so is the Isthmus road down the west side.
- **The grid east of the Agora:** Philoxenos's three-storey house and his walled garden, the widow's house, and a walled neighbourhood garden with a tripod, under the crag of **Acrocorinth**, whose rock-cut stair climbs to a hidden Stardust.
- **The Hephaisteion** on its hill above the Agora's west side, its garden (a dig spot) beside it, its terrace wall over **the potters' lane**: Euphronios's narrow house between two kilns, his pots drying in the yard.
- **The temple terrace:** the **Temple of Hermes** at the top of the main street, on a marble terrace up a broad stair (beat 14's trigger is its bottom tread), laurels flanking it, the **Peirene** fountain house beside it, and the cistern's black arch in the terrace wall (Hecate's Torch, later).
- **The north-west:** the runners' house beside the Isthmus Gate, and the gate itself: the city wall across the slope, a hoplite on each post, the road out between them.

Every door has a household or a public building behind it, and no other house is drawn: the rest of the grid is the stoas, the stalls, gardens, walls, shrines and trees (SCRIPT.md, "Houses").

### Passes

**Pass 1** (`img/emporion_city_pass1.png`).
- The city read as monuments floating on a sea of white marble. The Agora was a vast blank square with eleven stalls scattered over it. The east grid was open paving with two houses in it. Nothing said "the harbor of the whole world".
- Bronze drain grates were scattered every few cells and read as holes.
- The orchards at the edges were olives in rows, and the south band was a single straight row of them.
- The temple read well as the crown: framed by the stair, the terrace and the slope behind it.

**Pass 2** (`img/emporion_city_pass2.png`).
- The stalls went into two aisles on each side of the main street. The main street became an avenue of laurels in great pots from the harbor quarter to the temple stair, so the axis reads from the quay.
- Acrocorinth's crag went in over the east grid, the landmark that screen lacked. Drains came down to one cell in sixty. Pines and cypresses broke up the olive rows.
- The Peirene was in the city twice (the terrace and the east grid); the second became a walled garden with a tripod.
- The seam rows were open grass: a player could cross into the harbor or Route 4 anywhere. A tree line (olives, pines and cypresses by turns) now closes both seams except at their roads, so each exit is a road through a gap.
- In game the pithoi sat on the stoa's front row and made it a one-tile corridor; the man with a lamp, pacing it, kept standing in front of the scroll counter. The pithoi moved down a row, so the stoa front is two tiles wide, and he paces the outer row.

**Pass 3** (this render).
- The Isthmus road down the Agora's west side was a long empty strip: it got its own laurels.
- The south-west garden was olives and nothing else: Asclepius's tripod went in below the Asclepeion.
- In game every screen along the route shows a landmark: the harbor road's cypresses, the Asclepeion and the Deigma, Pegasus and the stalls, the tavern and the notice board, the temple on its terrace, the Hephaisteion and the kilns, Acrocorinth, the gate and its hoplites.

## The harbor district (`MAP_EMPORION_HARBOR`)

- **The road down** from the city (rows 0–5, aethos): cypresses and olive gardens behind dry-stone walls, the harbor road's stele, the coast curving in at the east.
- **The forum,** a marble square where the road meets the quay: Glykera's fish stall and the wine-seller's.
- **The west yard:** the Titans' **hiring hall** (the warehouse with the chalked board, its cart-door the door) with the crates of shovels and bronze helmets in front, a bonded store beside it, amphorae stacked like firewood, the dockhand; below it the **ship sheds**, six sterns hauled up on their slipways onto a beach (the Super Potion, the daily dig spot, the mother and son, the sailor), and a hull half built on the stocks.
- **The quay:** the customs post (goods off the ships and the customs man), the crane over the water, bollards, landing steps (the hidden Heart Scale), two merchantmen at their berths, and the *Euploia*'s berth at (30, 16) with Nausikles. **The quay herm** at the head of the quay in a bed of anemones, with the city's stele and the planter Alethea digs.
- **Poseidon's sanctuary** at the root of the mole: his altar and a victor's pine crown from his Isthmian games, under a cypress.
- **The mole,** the harbor wall, running out east and south into the gulf, with the hidden Bronze Obol in a crack, gulls, and Halitherses at its end.

### Passes

**Pass 1** (`img/emporion_harbor_pass1.png`).
- The quay was a vast tan expanse with a few goods on it, and the forum was too big and empty.
- The landing steps stood half over the water.
- The beach under the ship sheds was one row: the sand's water-edge pieces are surf, not sand, so only one row was walkable.

**Pass 2** (`img/emporion_harbor_pass2.png`).
- The harbor came down from 30 rows to 26, the quay from nine rows to seven, and the goods went into clusters (the customs post, the crane, the yard), so each screen has something on it.
- The steps moved onto the berth's edge. The beach got a second walkable row.
- The headless check found the hull on the stocks cutting the warehouses, and so the hiring hall, off from the quay: you could only reach them round through the olive gardens. The hull moved beside the sheds and the yard opened onto the quay.
- The road's sign stood behind the cypresses that line it, where nobody could read it; it moved to the road's edge. The seam row got its closing tree line.

**Pass 3** (this render).
- The quay's east end, on the way to the mole, was empty: Poseidon's sanctuary went in there.
- The coast's corner of the seam row was a straight line of cypress tops, because the sand came up to row 1 and no tree had room. The coast now starts at row 2, so the tree line there mixes olives and pines like the rest.

## Not drawn, and asks

- **The *Euploia* at her berth.** `isthmos` has no trireme and no gangplank (Akti's trireme is in `akti`), so the berth at (30, 16) is open water with bollards, and beat 11 starts with the party on the quay. A trireme and a gangplank in `isthmos`, copied from `tools/ichor/art/akti_harbor.py`, would put her there (isthmos has 174 tiles free).
- **The Deigma's door.** `stoa_bay_door` and `stoa_agora` are `D` in their walk grids, but `tools/ichor/art/emporion_agora.py` never gives the door cell `MB_NON_ANIMATED_DOOR`, so a warp on it never fires. The Deigma's door is a coord trigger that warps (`EmporionCity_EventScript_DeigmaDoor`). The fix is two lines in `stoa_pieces()` and a recompile; then the trigger can go.
- **A pithos.** Emporion has no great storage jar, so the six empty pithoi are three vase racks.
- **Number Nine** stands in as the youth walker (`ICHOR_STUB_SPRITE`); he wants a wooden-statue walker. Kerykos's walker is the temple agent's.
- **The quay herm** is aethos's roadside herm: `great_herm` is in `emporion` only. It is the altar of beat 11's rites tutorial, so a plain herm is right; the great herm (anointing) is the Agora's.
