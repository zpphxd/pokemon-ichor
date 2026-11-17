# The Labyrinth as a maze and a cave system

A director's addendum to `design/LABYRINTH.md` (2026-11-17), from the user's direction: **"make the Labyrinth awesome and a maze. A very good cave system."** LABYRINTH.md still holds the story, the cast, the scenes, each ring's god and mechanic (§5–§6), the state (§13) and the sizes (§4). This document decides how the rings are laid out. Where the two differ on layout, this one wins.

## 1. The idea

Daedalus didn't dig the Labyrinth from nothing. He built it **into the karst caves under Knossos**: the real Crete is riddled with them (the Idaean Cave, Skotino, the Cave of Eileithyia, the quarry-maze at Gortyn that travelers called "the Labyrinth"). So the house is two things at once:

- **The built maze:** Minoan corridors of ashlar and gypsum, red-and-black painted columns, light wells, frescoes, double-axe mason's marks, pithoi magazines.
- **The cave it was cut into:** limestone caverns, stalactites and flowstone, underground streams and a lake, chasms crossed on beams, rooms where the masonry has collapsed and the cave shows through.

**The deeper you go, the more the cave wins.** Rings I–II are mostly built, with breaches into raw cave. Rings III–V are half and half: corridors that open into caverns and back. Ring VI's forge sits in a magma-lit cavern. Ring VII's dancing floor lies under a vast natural dome, and the Starry Chamber's "stars" are crystals in a cave ceiling. The Icarus Shaft is a natural chimney to the sky. A player should feel the house getting older, wilder and less human as they descend.

## 2. Every ring is a real maze

These are hard rules. Measure them on the render, and give the counts in the ring's `design/maps/<Map>.md`.

| Rule | Minimum per ring |
|---|---|
| Junctions (3- or 4-way) | 3 per 15×10 screen, on average |
| Loops (two different routes between the same two points) | 3 |
| Dead ends | 4. **Each holds something**: an item or hidden item, a trainer, a fresco or inscription that tells part of the story, a Thread anchor, or a view into a place you can't reach yet |
| Longest straight run without a turn, junction or feature | 8 cells |
| Corridor width | 1–2 cells. Chambers of 4×4 or more are the landmarks and rest points, about one per two screens |
| Wrong turns that cost real time | At least 2 per ring that lead a long way before they dead-end or loop back |

**A maze, not a corridor with side rooms.** Draw the ring's graph first: nodes for junctions and chambers, edges for passages. Check it has the loops and dead ends above *before* placing tiles. Keep the graph sketch in the brief. The critical path should be no more than about a third of the ring's walkable area.

**It must stay readable.** A maze that is only confusing is a bad maze. Each ring gets:

- **A landmark set** of its own, so a player always knows which ring and which part of it they're in: a color and a fresco motif per ring (bulls, dolphins, lilies, griffins, octopus and argonauts, double axes, stars), plus one big unmistakable feature per screen (a fallen column, a cave pool, a giant pithos, a stalagmite cluster, a light well).
- **Sight lines** that show a goal before the route to it is open (a lit chamber across a chasm, a stair seen through bars), so the player has something to aim for.
- **The Thread** (LABYRINTH §5.1) as the player's own map. Place Thread anchors at junctions where a player would want to mark their way.

## 3. A connected cave system, in three dimensions

The rings are stacked floors (LABYRINTH §4), but **they are not a straight line of stairs.** They are one cave system:

- **Drops and climbs.** Every ring has at least one hole or chute that drops to the ring below (one-way: a shortcut forward, or a trap that lands you in a part you haven't reached) and at least one ladder, root or flowstone climb back up. A player should sometimes reach a new ring by falling into it.
- **Shortcuts back.** When a player reaches the far side of a ring, they open a way back to the ring's entrance or to Daedalus's workshop (a bronze door that only opens from beyond, a beam to push across a chasm, a rope to drop). Backtracking to heal or restock is then short. The workshop is the hub (LABYRINTH §4).
- **The underground water.** One stream runs down through the whole house: it appears in Ring II as a trickle in a cleft, becomes a stream in Ring III, a lake in Ring V (the skylight pools), and falls past the forge in Ring VI. Following the water downstream is always a way deeper. Use it for Surf and Waterfall with the relics the player has by now (the Horn of Achelous is Waterfall, SYSTEMS §1), and for fishing.
- **Relic and Labrys gates** that invite a return: cracked walls Asterion can break, Labrys dials, column drums for the Girdle of Herakles, webs or myrtle the Sickle cuts. Some open now; some only after the heart, for the post-game's Endless Labyrinth (LABYRINTH §10).
- **One map of the whole system.** Keep `design/maps/Labyrinth_System.md` with a connection diagram of every ring, drop, climb, shortcut and the stream. Keep it current as rings land, so the two Labyrinth builders' halves fit together.

## 4. The cave as art

The `labyrinth` tileset (Rings I–IV, owned by the Labyrinth I builder) and the `mychos` tileset (the heart, Rings V–VII and the chambers below, owned by the Labyrinth II builder) both need **natural cave pieces**, not just masonry. Draw them; don't work around them:

- **Limestone walls:** rough cave rock in 3/4 view, with a top edge, cliff faces and outer and inner corners in all directions.
- **Cave floor:** packed earth, wet rock, gravel and scree.
- **Formations:** stalactites hanging from the top edge, stalagmites and columns on the floor, flowstone curtains.
- **Water and chasms:** underground water (still pool, flowing stream, falls) and a chasm or pit edge with a beam bridge.
- **The breach:** where masonry meets cave, dressed blocks breaking into rough rock, and a collapsed wall with rubble and a gap. This is the house's signature piece.
- **Light:** glowing crystals for the Starry Chamber, and magma glow for the forge cavern.

The `cave` and `maia_cave` tilesets on `zach-main` (the Cave of Maia off Route 12) show how Ichor draws cave rock. Match their 3/4 perspective and edge logic, in the Labyrinth's own palette. Gen 3 references for cave craft: Granite Cave, Seafloor Cavern, Victory Road, and Mt. Moon's ladders and holes.

## 5. Encounters and life

- **Wild encounters in every cave part.** Land tables in the cave sections, water and fishing tables on the stream and lake, all full and varied from the Aethos dex at `design/BALANCE.md`'s Act III levels. Include a few species found only here: cave dwellers, bats, the Labyrinth's serpents and the like (check the dex yamls' habitats).
- **The built corridors stay encounter-free**, as LABYRINTH says. The caves are where the wild things live. That contrast is part of the mood.
- **Asterion** (LABYRINTH §5.3) roams Ring V as the maze's living danger. Its layout must give him real hunting room: long loops he can patrol and side passages to hide in.

## 6. The review gate

A ring lands only when the director has seen:

1. its graph sketch with the counts from §2;
2. three render → critique → fix passes, kept as images, at full size and at 15×10;
3. `tools/ichor/map_audit.py` and `tools/ichor/map_style_audit.py` with no FAILs;
4. a headless test that walks the critical path, and one wrong turn and back.
