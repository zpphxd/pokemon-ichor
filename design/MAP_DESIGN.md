# Ichor map design: the fundamentals

Every Ichor map follows these rules. They come from how Game Freak builds Gen 3 maps, tuned for Aethos. A map that looks beautiful but breaks them plays badly. A map that follows them but looks flat isn't done either; see the "great" checklist at the end.

## 1. Routes

### Grass is the route's heartbeat
- **Forced grass.** Every route has at least one band of tall grass across the main path that the player can't walk around. Make it 2–4 tiles deep, as wide as the path, and walled in by trees, ledges, water or rock so there's no detour. Longer routes have two or three of these bands.
  - **Early routes** (Act I) have short forced bands. The first band on Route 1 is 2 deep.
  - **Later routes** have longer bands, or a forced band right after a trainer, so the player can't heal between them.
- **Optional grass.** Put more grass off the path, with a reason to go in: an item, a rarer encounter table, or a shortcut. Optional grass is never just filler.
- **Shape.** Grass patches follow the land: meadows in hollows, verges along walls, clearings in groves. Never draw plain rectangles; use the soft-edge pieces.
- **The encounter table matches what the player sees.** Shore grass holds sea-side species, olive groves hold grove species, and night tables apply after dark.

### Trainers are checkpoints
- **The first trainer on a route is easy** and stands in plain view, so the player learns where trainers wait.
- **Mandatory trainers.** Put their sight lines across the only path. Their facing and range (usually 3–5) must cover the full width of a narrow point.
- **Optional trainers** sit off the path or face away. Battling them is the player's choice.
- **Spacing.** Leave room between trainers to breathe; that's a good place for a forced grass band. Don't stack three sight lines on one tile.
- **Themes.** Trainer classes fit the place: shepherds in meadows, harvesters in groves, hoplites at narrow passes, augurs on hilltops.

### Ledges are one-way shortcuts
- Ledges drop toward the previous town, so the trip back is quick and the trip forward takes work.
- Use them to make loops. The way out goes up the long side; the way back hops down.
- Never use a ledge to trap a player away from an exit with no other way out. A person who never moves counts as a wall here: a beaten trainer stays on his tile, so never stand one in a ledge pocket's only way out.

### Every dead end pays
- **Visible items** (sealed jars) are lures. Put them where the player can see them but has to work to reach them: up a side path, past optional grass, behind a trainer.
- **Hidden items** go where curiosity takes people: the end of a pier, behind a statue, the corner of a walled garden, the tip of a peninsula.
- A dead end with nothing in it is a bug.

### Relic gates invite a return
- Show the player locked places early: brambles that need the Labrys (or whatever cuts), boulders that need the Girdle, water that needs Poseidon's Conch, a dark cave mouth that needs Hecate's Torch.
- What's behind should be visible, or hinted at, so they remember to come back.
- Every relic must open something in an area the player has already visited.

### Pacing and size
- **Size.** A route is 2–5 GBA screens long. One screen is 15×10 tiles.
- **Width.** Vary it: narrow passes force encounters and battles; open meadows let players explore.
- **Rhythm.** A good route follows a beat: a calm stretch, grass, a trainer, a reward, grass, a landmark, then the next town in view.
- **A set piece.** Give each route one moment: a gift NPC, a scene, a view, or a small puzzle.
- **A rest point** on long routes: a house, a spring, a berry tree or a friendly healer.
- **Signs.** Put a sign at each end of a route, and at forks.

## 2. Towns

- **First things first.** The Asclepeion and the Agora should be visible from the main entrance, or very close to it. A tired player shouldn't have to search for healing.
- **The temple is the crown.** It is the town's landmark: elevated, at the far end, or framed by the main street. If the story needs it closed, it stays shut until the right beat.
- **Every house is a home** (user, 2026-11-14). Every house in a town has a door, an interior and someone living there, and something happens inside. That means a gift, a trade (an in-game Pokémon trade or an item swap), a small quest, a minigame, a rematch, or lore that leads to a reward. Flavour text alone isn't enough. There are no scenery-only houses with barred or shuttered doors.
  - Give each household a story in a line or two: who lives there, and what they want or offer.
  - Spread the rewards across a town: not five gifts of the same item, and not all of them available on the first visit. Some open after a Laurel or a story beat, so returning to a town pays.
  - **Every interior is unique** (user, 2026-11-14). No layout is reused or copied between buildings. Each room has its own shape, size and furniture, chosen for whoever lives or works there: a potter's wheel and kiln, a weaver's loom, a fisher's nets and drying racks, a philosopher's scroll niches, a shepherd's fold. Rooms follow the room catalogs (`ROOMS_oikia.md`, `ROOMS_civic.md`). When a catalog lacks a piece a room needs, ask for it to be drawn.
  - Public buildings of the same kind (each town's Asclepeion or Agora) share their function and service counter, but each town's version differs in layout, size and local character: a harbor Asclepeion with a sea window, a mountain one with a cave spring.
- **Exits.** Make every exit easy to read: a road, a sign and a gap in the edge. No hidden exits on the main path.
- **Identity.** Each town has one signature feature or mechanic the player remembers. Akti has its harbor and trireme. Elaia has its festival square and the old olive.
- **Hidden items.** Towns have them too, a couple per town.

## 3. Caves, ruins and dungeons

- **Shape.** The main line has branches and loops. Branches end in items or trainers. Floors are connected by stairs and holes.
- **Mechanics: teach, then test, then combine.** Introduce a mechanic safely: a dark room with one brazier, a single boulder. Then test it. Then combine it with another mechanic.
- **A midpoint rest:** a spring, a friendly NPC, or a shortcut that opens back to the entrance.
- **A payoff at the end:** a boss, a legendary, a relic or a story scene. Once the dungeon is cleared, a shortcut leads back out.
- **Darkness** (Hecate's Torch): dark areas should still be readable. Lit braziers become landmarks.

## 4. Temples (gyms)

- **One rite-puzzle,** in the god's theme, taught in the first room, tested in the middle and mastered at the end. The Hearth Trial is the model.
- **Acolytes** are checkpoints between stages, and at least one is optional.
- **The Hierophant** waits at the climax of the architecture: the dais or the inner sanctum.
- **After the Laurel,** the room stays solved and the acolytes are marked as beaten.

## 5. The world's shape

- **Act I is a corridor:** island, crossing, mainland road. The player learns the rules.
- **Act II opens into hubs:** a capital with spokes, side regions and optional areas.
- **Act III and the post-game** reward backtracking. New relics open old places, old routes gain post-game encounters, and rematches appear.
- **Connections.** Neighbouring maps connect on matching seams. Agree the seam columns before building either side.
- **Seam strips use only the primary tileset.** The game draws a connected neighbour using the tilesets of the map the player is standing on. A neighbour's secondary-tileset pieces (kalliste, akti, agros) near the seam therefore draw as garbage from across it.
  - On an up or down connection, the 6 rows nearest the seam may use only aethos metatiles.
  - On a left or right connection, the 8 columns nearest the seam may use only aethos metatiles.
  - Every map builder enforces this in code.
  - Two neighbours that share the same secondary tileset are exempt.

## 6. Readability on a GBA screen

- **The 15×10 test.** Crop along the player's route. Every view should show where to go, what's blocked, and something worth looking at.
- **Walkable versus blocked must be obvious.** Walls look like walls, ledges look like ledges, and grass looks like grass.
- **No long empty stretches.** If a screen has nothing on it, cut it or give it purpose.
- **Borders.** The map's border tiles match its edge, so the camera never shows nonsense past the edge.

## 7. The "great" checklist, on top of the rules

- **A landmark on every screen.**
- **Natural edges.** Tree lines staggered 2–4 deep, mixed species, irregular silhouettes, never straight walls of one tree.
- **Varied ground.** Grass variants, flowers, bare earth, and worn paths that curve and widen at junctions.
- **Believable places.** Details cluster around a purpose. Leave breathing room.
- **Myth in the land.** Every route tells a small story: a herm, a shrine, a ruin, a grave stele, a place a myth happened.
- **At least three render-and-critique passes** before a map is handed over.

## 8. The route standard, in numbers

§§1–7 say what a good map does. This section says how much of it a map needs. The numbers come from measuring Game Freak's own Emerald maps (Appendix A), and each one matches Emerald's median or beats it: Ichor is generous, not sparse. `tools/ichor/map_audit.py` checks them (§8.6).

### 8.1 How things are counted

- **A screen** is 15×10 cells of map area: width × height ÷ 150, borders included. Kalliste Route 1 (30×64) is 12.8 screens. A per-screen minimum is the rate times the map's screens, rounded, or the floor if that's higher.
- **Grass** is a walkable cell whose metatile behavior is tall grass or long grass. Ash grass counts too.
- **Forced grass** is the fewest grass cells a first-time walker must cross between two of a route's ends: no surf, no relics, and NPCs and trainers who stand still are in the way. A 3-deep band across the only path is 3. A route counts its worst pair of ends, so a band crossed in one direction counts.
- **Items** are item balls you can see. **Hidden items** are `hidden_item` bg events, **signs** are `sign` bg events, and **trainers** are objects with a trainer type.
- **Bands** follow BALANCE.md's stages. **Early** is the Prologue and Act I (Kalliste, Emporion, Eleusa). **Middle** is Act II (Thyrsa to Kaldera). **Late** is Act III, the League and the post-game. `STAGES` in `map_audit.py` says which place belongs to which stage.
- **A sea route** is an ocean route, or a route whose open ground is mostly water and whose connected ends can't be joined on foot. Every other route is a land route.

### 8.2 Routes

Hard minimums for a land route. Emerald's median is beside each one: early routes 101–104 / middle 110–119 / late land routes 120, 121 and 123.

| | Early | Middle | Late | Emerald median |
|---|---|---|---|---|
| Grass cells per screen | 15 | 15 | 15 | 15 / 8 / 13 |
| Forced grass, in cells | 2 | 8 | 8 | 2 / 8 / 1 |
| Trainers per screen (floor) | 0.5 (3) | 0.6 (6) | 0.9 (8) | 0.49 / 0.57 / 0.86 |
| Item balls per screen (floor) | 0.2 (2) | 0.2 (3) | 0.3 (5) | 0.16 / 0.18 / 0.27 |
| Hidden items | 2 | 3 | 4 | 0 / 2 / 4 |
| Species in each land table | 4 | 5 | 7 | 4 / 5 / 7 |

- **Grass.** 15 a screen is about a tenth of a route's area, Emerald's early-route median. Game Freak thins the grass after the first routes. Ichor keeps it ("plenty of grass", user, 2026-11-14).
- **Forced grass.** Early 2 is Route 1's first band (§1). Middle and late 8 is two 4-deep bands, or three shallower ones: §1's "longer routes have two or three". Four of Emerald's ten middle routes force no grass at all. Ichor allows none.
- **What that comes to.** A 12.8-screen early route needs 6 trainers and 3 item balls. A 12-screen middle route needs 7 and 3; a 12-screen late route, 11 and 5.
- **Length.** Emerald's routes run longer than §1's 2–5 screens (the long side's median is 4.3, 7.3 and 9.3 screens). Because §8 counts per screen, a longer route simply needs more.

Every route also needs, as hard minimums:

- **A sign within 15 cells of every connected end.** Emerald signs 25 of its 36 land-route ends. Forks need one too, but the audit can't find forks, so check them by eye.
- **Its wild tables** (§8.5).

The audit also flags these by heuristic, as warnings. Look at each one:

- **A set piece.** It looks for a scene trigger, a gift, a trade or a berry tree. A view or a puzzle counts just as well, but the audit can't see those.
- **No empty dead end.** It looks for a pocket of 7 or more walkable cells off every shortest path between the entrances, entered through 3 cells or fewer, at least 3 deep, with nothing in it or beside it: no object, sign, hidden item or warp. On Emerald's 17 land routes it finds 6.

Hard minimums for a sea route, beside the median of Emerald's 17 sea routes:

| | Ichor | Emerald median |
|---|---|---|
| Trainers per screen (floor) | 0.35 (5) | 0.33 |
| Item balls | 2 | 1 |
| Hidden items | 2 | 0 |

Sea routes also need surf and fishing tables (§8.5). The grass rules don't apply, but an island with grass needs land tables like any other map.

### 8.3 Towns

| | Ichor | Emerald median (16 towns) |
|---|---|---|
| Hidden items | 2 | 0 |
| Item balls | 1 | 0 |

- **Every house is a home** (§2), as a hard minimum: every door leads to an interior with someone in it. Something should happen in each house as well: a gift, a trade, a battle, a heal or an item. The audit looks for those in the house's scripts and warns when it finds none. A quest or a minigame it can't see is fine.
- **Every interior is unique** (§2), as a hard minimum: no interior uses another map's cells. A route or town that is a byte-for-byte copy of another map's cells gets a warning, since it's a placeholder.
- **Grass in a town** needs the same land tables as a route.

### 8.4 Dungeons

A dungeon's floors are the maps that share a name before `_B1F`, `_1F`, `_Room2` and the like: `EleusaSanctum_B1F` to `_B3F` are one dungeon. Hard minimums:

| | Ichor | Emerald median (9 dungeons, 35 floors) |
|---|---|---|
| Items on each floor, visible and hidden | 2 | 1.0 |
| Trainers in the dungeon | 3, or 1 in a one-floor cave | 2 |
| Hidden items in the dungeon | 2 | 0 |
| Species in each land table | 4 | 4–5 in Granite Cave |

- **The midpoint rest** (§3). A dungeon of 3 or more floors has a healer, a spring or a shortcut back. Emerald has none; Ichor does. The audit looks for a healing script and warns when it finds none, since a spring or a shortcut doesn't show in the data.

### 8.5 Wild tables

Ichor's engine falls back to the `_Morning` table for day and evening (`OW_TIME_OF_DAY_FALLBACK` in `include/config/overworld.h`). So:

- **A map with grass** needs a `_Morning` (or unsuffixed) land table and a `_Night` one. Both are hard. A `_Day` table is encouraged, not required.
- **Cave or sand encounter cells** need a land table. A night table is optional.
- **12 or more reachable water cells** need a surf table and a fishing table. If either is split by time, it needs a `_Night` table too, and a `_Day` one is encouraged.
- **Breakable rocks** (the Hammer's) need a rock-smash table.
- **Species.** Each land table needs the number in §8.2, or 4 in a dungeon. Each surf table needs 3, Emerald's median. Each fishing table needs 4, Emerald's sea-route median and one more than its land routes'.
- **Levels.** A map's land levels span no more than 5, BALANCE.md's rule; this one is hard. They also sit inside the stage's wild range in BALANCE.md; that one is a warning, since `STAGES` is kept by hand.

### 8.6 Running the audit

Every session runs `map_audit.py` on the maps it built or changed before it reports a batch, and puts the result in the report.

```bash
tools/ichor/map_audit.py Route6 Eleutherai MtKithairon               # map names or prefixes
tools/ichor/map_audit.py --all-ichor                                  # every Ichor map
tools/ichor/map_audit.py --ref claude/world-act2-0a92e7 --all-ichor   # another branch, read from git
```

- **Reading it.** Each map gets its numbers, then one line per shortfall. **FAIL** misses a hard minimum, and any FAIL makes the audit exit 1. **WARN** is a soft minimum, a heuristic or a structural check that needs a look. **NOTE** is encouraged, not required.
- **When it's done.** A batch isn't done while its maps FAIL. If a FAIL is right for a map (a story beat, a ship's deck), say why in the report. `--warn-only` reports without failing.
- **Structural checks.** It also runs the slice audit's REACH, WARP, EDGE, MIXED, ONSOLID and TRAP checks, from `tools/ichor/mapdata.py`. TRAP finds cells a player can walk to but never walk back out of, with every person who never moves counted as a wall. A trap, or a warp or connection to a map that doesn't exist, fails. The rest warn: Emerald's routes and towns have 57 stretches of open cells that face a wall across a seam.
- **Classing.** A map is a route, town, interior or dungeon by its map type, and a ship's deck or hold is an interior. To override, put `"ichor_kind": "dungeon"` (or `route`, `town` or `interior`) in its map.json, for example on a side area like Kronion Hill. mapjson ignores the key.
- **New places.** Add the place's name to `STAGES` in `map_audit.py`, so its levels are checked against BALANCE.md.
- **Changing a number** here means changing the constants at the top of `map_audit.py` in the same commit.
- **Other output.** `--markdown` prints the tables in `design/MAP_AUDIT.md`. `--benchmark` re-measures Emerald and prints Appendix A.

## Appendix A: the Emerald benchmark

Measured by `tools/ichor/map_audit.py --benchmark` from upstream's Emerald maps at the merge-base, `79dd436920` (pokeemerald-expansion 1.17.2), read with `git archive`. Each map's cells come from its layout's `map.bin` and each behavior from its tilesets' `metatile_attributes.bin`, the same way the audit reads Ichor's maps.

- **Screens** count the map's whole area. The long side is the longer of width ÷ 15 and height ÷ 10.
- **Wild tables** are Emerald's single tables. Species counts are the distinct species in the land, surf and fishing tables.
- **Route 111** shows no grass because its encounters are desert sand. Routes 103 and 104 force none: 103's halves join only by Surf, and 104's only through Petalburg Woods, so each is measured between the ends of one half.
- **The late band** (120–134) is mostly sea, so its land routes get their own row.

### Every route

| Route | Size | Screens | Long side | Grass | Grass/screen | Grass % | Water % | Forced grass | Trainers | Items | Hidden | Signs | NPCs | Berry trees | Rocks | Tables | Species: land / surf / fish |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 101 | 20×20 | 2.7 | 2.0 | 91 | 34 | 23 | 0 | 10 | 0 | 0 | 0 | 1 | 6 | 0 | 0 | land | 3 / – / – |
| 102 | 50×20 | 6.7 | 3.3 | 143 | 21 | 14 | 3 | 4 | 4 | 1 | 0 | 2 | 2 | 2 | 0 | land+surf+fish | 6 / 2 / 3 |
| 103 | 80×22 | 11.7 | 5.3 | 92 | 8 | 5 | 19 | 0 | 9 | 2 | 0 | 1 | 4 | 3 | 0 | land+surf+fish | 3 / 3 / 4 |
| 104 | 40×80 | 21.3 | 8.0 | 126 | 6 | 4 | 24 | 0 | 8 | 4 | 5 | 5 | 11 | 10 | 0 | land+surf+fish | 5 / 2 / 1 |
| 105 (sea) | 40×80 | 21.3 | 8.0 | 0 | 0 | 0 | 72 | – | 7 | 1 | 2 | 0 | 0 | 0 | 0 | surf+fish | – / 3 / 3 |
| 106 (sea) | 80×20 | 10.7 | 5.3 | 0 | 0 | 0 | 65 | – | 4 | 1 | 3 | 1 | 0 | 0 | 0 | surf+fish | – / 3 / 3 |
| 107 (sea) | 60×20 | 8.0 | 4.0 | 0 | 0 | 0 | 68 | – | 7 | 0 | 0 | 0 | 0 | 0 | 0 | surf+fish | – / 3 / 3 |
| 108 (sea) | 60×20 | 8.0 | 4.0 | 0 | 0 | 0 | 70 | – | 6 | 1 | 1 | 0 | 0 | 0 | 0 | surf+fish | – / 3 / 3 |
| 109 (sea) | 40×63 | 16.8 | 6.3 | 0 | 0 | 0 | 62 | – | 14 | 2 | 6 | 2 | 8 | 0 | 0 | surf+fish | – / 3 / 3 |
| 110 | 40×100 | 26.7 | 10.0 | 212 | 8 | 5 | 31 | 38 | 14 | 3 | 4 | 11 | 16 | 3 | 0 | land+surf+fish | 7 / 3 / 3 |
| 111 | 40×140 | 37.3 | 14.0 | 0 | 0 | 0 | 2 | 0 | 17 | 4 | 3 | 7 | 18 | 4 | 2 | land+surf+fish+rock | 4 / 2 / 3 |
| 112 | 40×60 | 16.0 | 6.0 | 59 | 4 | 2 | 0 | 0 | 6 | 1 | 0 | 3 | 3 | 4 | 0 | land | 2 / – / – |
| 113 | 100×20 | 13.3 | 6.7 | 270 | 20 | 14 | 0 | 27 | 11 | 3 | 3 | 4 | 2 | 0 | 0 | land | 3 / – / – |
| 114 | 40×80 | 21.3 | 8.0 | 88 | 4 | 3 | 12 | 13 | 13 | 3 | 2 | 3 | 3 | 3 | 5 | land+surf+fish+rock | 5 / 2 / 3 |
| 115 | 40×80 | 21.3 | 8.0 | 20 | 1 | 1 | 16 | 0 | 10 | 6 | 1 | 2 | 1 | 5 | 1 | land+surf+fish | 5 / 3 / 3 |
| 116 | 100×20 | 13.3 | 6.7 | 138 | 10 | 7 | 0 | 12 | 10 | 5 | 2 | 5 | 4 | 4 | 0 | land | 6 / – / – |
| 117 | 60×20 | 8.0 | 4.0 | 65 | 8 | 5 | 8 | 0 | 10 | 2 | 1 | 3 | 10 | 3 | 0 | land+surf+fish | 6 / 2 / 3 |
| 118 | 80×20 | 10.7 | 5.3 | 110 | 10 | 7 | 18 | 5 | 7 | 1 | 2 | 2 | 9 | 3 | 0 | land+surf+fish | 6 / 3 / 4 |
| 119 | 40×140 | 37.3 | 14.0 | 765 | 20 | 14 | 8 | 13 | 17 | 9 | 4 | 3 | 10 | 7 | 0 | land+surf+fish | 5 / 3 / 3 |
| 120 | 40×100 | 26.7 | 10.0 | 436 | 16 | 11 | 10 | 1 | 13 | 5 | 4 | 2 | 13 | 10 | 0 | land+surf+fish | 7 / 2 / 3 |
| 121 | 80×20 | 10.7 | 5.3 | 140 | 13 | 9 | 16 | 12 | 11 | 3 | 4 | 2 | 4 | 8 | 0 | land+surf+fish | 7 / 3 / 3 |
| 122 (sea) | 40×40 | 10.7 | 4.0 | 0 | 0 | 0 | 50 | – | 0 | 0 | 0 | 0 | 0 | 0 | 0 | surf+fish | – / 3 / 4 |
| 123 | 140×20 | 18.7 | 9.3 | 164 | 9 | 6 | 13 | 0 | 16 | 5 | 5 | 3 | 1 | 18 | 0 | land+surf+fish | 7 / 3 / 3 |
| 124 (sea) | 80×80 | 42.7 | 8.0 | 0 | 0 | 0 | 72 | – | 9 | 3 | 0 | 1 | 0 | 0 | 0 | surf+fish | – / 3 / 4 |
| 125 (sea) | 80×40 | 21.3 | 5.3 | 0 | 0 | 0 | 68 | – | 9 | 1 | 0 | 0 | 0 | 0 | 0 | surf+fish | – / 3 / 4 |
| 126 (sea) | 80×80 | 42.7 | 8.0 | 0 | 0 | 0 | 68 | – | 8 | 1 | 0 | 0 | 0 | 0 | 0 | surf+fish | – / 3 / 4 |
| 127 (sea) | 80×80 | 42.7 | 8.0 | 0 | 0 | 0 | 65 | – | 8 | 3 | 0 | 0 | 0 | 0 | 0 | surf+fish | – / 3 / 4 |
| 128 (sea) | 120×40 | 32.0 | 8.0 | 0 | 0 | 0 | 78 | – | 7 | 0 | 3 | 0 | 3 | 0 | 0 | surf+fish | – / 3 / 5 |
| 129 (sea) | 80×40 | 21.3 | 5.3 | 0 | 0 | 0 | 83 | – | 5 | 0 | 0 | 0 | 0 | 0 | 0 | surf+fish | – / 4 / 4 |
| 130 (sea) | 80×40 | 21.3 | 5.3 | 0 | 0 | 0 | 78 | – | 3 | 0 | 0 | 0 | 0 | 1 | 0 | land+surf+fish | 1 / 3 / 4 |
| 131 (sea) | 60×40 | 16.0 | 4.0 | 0 | 0 | 0 | 70 | – | 8 | 0 | 0 | 0 | 0 | 0 | 0 | surf+fish | – / 3 / 4 |
| 132 (sea) | 80×40 | 21.3 | 5.3 | 0 | 0 | 0 | 68 | – | 8 | 2 | 0 | 0 | 0 | 0 | 0 | surf+fish | – / 3 / 5 |
| 133 (sea) | 80×40 | 21.3 | 5.3 | 0 | 0 | 0 | 65 | – | 7 | 3 | 0 | 0 | 0 | 0 | 0 | surf+fish | – / 3 / 5 |
| 134 (sea) | 80×40 | 21.3 | 5.3 | 0 | 0 | 0 | 70 | – | 9 | 2 | 0 | 0 | 0 | 0 | 0 | surf+fish | – / 3 / 5 |

### Routes by band

Each cell is the 25th percentile / **median** / 75th percentile.

| Band | Routes | Screens | Long side | Grass/screen | Grass % | Forced grass | Trainers | Trainers/screen | Items | Items/screen | Hidden | Signs | Ends signed | Land species | Surf species | Fish species |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| early (101–104) | 4 | 6 / **9** / 14 | 3.0 / **4.3** / 6.0 | 7 / **15** / 25 | 5 / **10** / 16 | 0 / **2** / 6 | 3.0 / **6.0** / 8.2 | 0.28 / **0.49** / 0.64 | 0.8 / **1.5** / 2.5 | 0.11 / **0.16** / 0.17 | 0.0 / **0.0** / 1.2 | 1.0 / **1.5** / 2.8 | 6 of 8 | 3 / **4** / 5 | 2 / **2** / 2 | 2 / **3** / 4 |
| middle (110–119) | 10 | 13 / **19** / 25 | 6.2 / **7.3** / 9.5 | 4 / **8** / 10 | 2.5 / **5.4** / 6.9 | 0 / **8** / 13 | 10 / **10** / 14 | 0.46 / **0.57** / 0.73 | 2.2 / **3.0** / 4.8 | 0.11 / **0.18** / 0.25 | 1.2 / **2.0** / 3.0 | 3.0 / **3.0** / 4.8 | 16 of 22 | 4 / **5** / 6 | 2 / **3** / 3 | 3 / **3** / 3 |
| late (120–134) | 15 | 20 / **21** / 29 | 5.3 / **5.3** / 8.0 | 0.0 / **0.0** / 0.0 | 0.0 / **0.0** / 0.0 | 0 / **1** / 6 | 7.0 / **8.0** / 9.0 | 0.20 / **0.33** / 0.45 | 0.0 / **2.0** / 3.0 | 0.00 / **0.07** / 0.12 | 0.0 / **0.0** / 1.5 | 0.0 / **0.0** / 0.5 | 3 of 21 | 6 / **7** / 7 | 3 / **3** / 3 | 4 / **4** / 4 |
| late, land only (120, 121, 123) | 3 | 15 / **19** / 23 | 7.3 / **9.3** / 9.7 | 11 / **13** / 15 | 7.3 / **8.8** / 9.8 | 0 / **1** / 6 | 12 / **13** / 14 | 0.67 / **0.86** / 0.94 | 4.0 / **5.0** / 5.0 | 0.23 / **0.27** / 0.27 | 4.0 / **4.0** / 4.5 | 2.0 / **2.0** / 2.5 | 3 of 6 | 7 / **7** / 7 | 2 / **3** / 3 | 3 / **3** / 3 |
| all land routes | 17 | 11 / **16** / 21 | 5.3 / **6.7** / 9.3 | 6 / **9** / 16 | 4 / **6** / 11 | 0 / **4** / 12 | 8 / **10** / 13 | 0.46 / **0.60** / 0.77 | 2.0 / **3.0** / 5.0 | 0.11 / **0.19** / 0.25 | 1.0 / **2.0** / 4.0 | 2.0 / **3.0** / 4.0 | 25 of 36 | 4 / **5** / 6 | 2 / **3** / 3 | 3 / **3** / 3 |
| all sea routes | 17 | 16 / **21** / 21 | 5.3 / **5.3** / 8.0 | 0.0 / **0.0** / 0.0 | 0.0 / **0.0** / 0.0 | – | 6.0 / **7.0** / 8.0 | 0.21 / **0.33** / 0.42 | 0.0 / **1.0** / 2.0 | 0.00 / **0.05** / 0.09 | 0.0 / **0.0** / 1.0 | 0.0 / **0.0** / 0.0 | 2 of 18 | 1 / **1** / 1 | 3 / **3** / 3 | 3 / **4** / 4 |
| all of 101–134 | 34 | 11 / **21** / 21 | 5.3 / **5.7** / 8.0 | 0.0 / **0.0** / 8.6 | 0.0 / **0.0** / 5.7 | 0 / **4** / 12 | 7 / **8** / 11 | 0.33 / **0.46** / 0.73 | 1.0 / **2.0** / 3.0 | 0.05 / **0.10** / 0.18 | 0.0 / **1.0** / 3.0 | 0.0 / **1.0** / 3.0 | 27 of 54 | 3 / **5** / 6 | 3 / **3** / 3 | 3 / **3** / 4 |

### Towns

| Town | Size | Screens | Items | Hidden | Signs | NPCs | Doors | Tables |
|---|---|---|---|---|---|---|---|---|
| LittlerootTown | 20×20 | 2.7 | 0 | 0 | 4 | 8 | 3 | – |
| OldaleTown | 20×20 | 2.7 | 0 | 0 | 5 | 4 | 4 | – |
| PetalburgCity | 30×30 | 6.0 | 2 | 1 | 7 | 7 | 6 | surf+fish |
| RustboroCity | 40×60 | 16.0 | 1 | 0 | 10 | 15 | 12 | – |
| DewfordTown | 20×20 | 2.7 | 0 | 0 | 5 | 5 | 5 | surf+fish |
| SlateportCity | 40×60 | 16.0 | 0 | 0 | 13 | 35 | 11 | surf+fish |
| MauvilleCity | 40×20 | 5.3 | 1 | 0 | 8 | 10 | 6 | – |
| VerdanturfTown | 20×20 | 2.7 | 0 | 0 | 8 | 4 | 6 | – |
| FallarborTown | 20×20 | 2.7 | 0 | 1 | 7 | 4 | 5 | – |
| LavaridgeTown | 20×20 | 2.7 | 0 | 1 | 7 | 9 | 6 | – |
| FortreeCity | 40×20 | 5.3 | 0 | 0 | 6 | 7 | 9 | – |
| LilycoveCity | 80×40 | 21.3 | 1 | 3 | 10 | 21 | 14 | surf+fish |
| MossdeepCity | 80×40 | 21.3 | 1 | 0 | 8 | 16 | 10 | surf+fish |
| SootopolisCity | 60×60 | 24.0 | 0 | 0 | 6 | 18 | 12 | surf+fish |
| PacifidlogTown | 20×40 | 5.3 | 0 | 0 | 3 | 3 | 6 | surf+fish |
| EverGrandeCity | 40×80 | 21.3 | 0 | 0 | 5 | 0 | 2 | surf+fish |
| **25th / median / 75th** | | 3 / **5** / 17 | 0.0 / **0.0** / 1.0 | 0.0 / **0.0** / 0.2 | 5.0 / **7.0** / 8.0 | 4 / **8** / 15 | | |

### Petalburg Woods and the main caves

| Dungeon | Floors | Trainers | Items + hidden | Per floor | Healer | Land species, by floor |
|---|---|---|---|---|---|---|
| Petalburg Woods | 1 | 2 | 4 + 4 | 8.0 | no | 7 |
| Granite Cave | 4 | 0 | 4 + 2 | 1.5 | no | 4, 5, 4, 4 |
| Rusturf Tunnel | 1 | 1 | 2 + 0 | 2.0 | no | 1 |
| Meteor Falls | 4 | 3 | 5 + 0 | 1.2 | no | 2, 2, 2, 3 |
| Fiery Path | 1 | 0 | 2 + 0 | 2.0 | no | 6 |
| Mt. Pyre | 6 | 12 | 5 + 0 | 0.8 | no | 1, 1, 1, 2, 2, 2 |
| Shoal Cave | 5 | 0 | 5 + 0 | 1.0 | no | 3, 3, 3, 3, 4 |
| Seafloor Cavern | 10 | 6 | 1 + 0 | 0.1 | no | 2, 2, 2, 2, 2, 2, 2, 2 |
| Victory Road | 3 | 16 | 5 + 3 | 2.7 | no | 8, 4, 4 |
| **25th / median / 75th** | 1.0 / **4.0** / 5.0 | 0.0 / **2.0** / 6.0 | hidden 0.0 / **0.0** / 2.0 | 0.0 / **1.0** / 1.5 | | |

The dead-end heuristic flags 6 empty pocket(s) on Emerald's 17 land routes: Route110 at (33, 28) (10 cells); Route113 at (11, 0) (13 cells); Route114 at (13, 16) (13 cells); Route114 at (25, 0) (14 cells); Route116 at (60, 16) (8 cells); Route123 at (23, 18) (14 cells).
