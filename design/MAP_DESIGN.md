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
- Never use a ledge to trap a player away from an exit with no other way out.

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
