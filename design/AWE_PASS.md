# The awe pass: colossi, grand temples, great cities and ruins

An art-director review of every great city, temple and ruin, written as a plan
that can be built. It was written on 2026-11-18 against zach-main `3b3c0aca7f`.
The north star is the user's: *grand and amazing, a new world never explored.*

Nothing here has been built yet. Every map and tileset named below is as it
stands today. The mockups in `design/art/awe_pass/` are blocking sketches,
painted to scale over the current renders, that show where things go and how
big they are. They are not tile art. To regenerate them, render each map with
`tools/ichor/render_map.py` and run `tools/ichor/art/awe_pass_mockups.py`.

The Ascent and Olympus's Propylaia are being rebuilt by another helper, so
this plan notes them but doesn't plan them. Proposals that touch the story are
marked **(story: director)**. They need the creative director's yes before
anyone builds them.

---

## 0. What the renders say

These findings come from the stitched overworld (`tools/ichor/world_render.py
--labels`) and a fresh render of every map named here.

1. **Two of the four great cities are placeholders.**
   - **Astyra**, the capital where the story turns, is open grass with sand
     crosses, four buildings and a forest wall (`build/render/awe/Astyra.png`).
   - Its **Akropolis** is a sand corridor through a tree grid.
   - **Astyra_Harbor** is a sand strip.
   - **Kaldera** is a sand crescent in the sea with four stock buildings.
   - Kaldera's **Temple of Hephaestus** is a Civic sample hall (striped walls
     and pedestals in rows), and the **Telchines Forge** is a bare cave room.
   - All four exteriors still borrow **gTileset_Kalliste**, the home-island
     set that Elaia, Route 15, Daphni and Route 16 also use.
   - No amount of polish fixes this. They need their own tilesets and a full
     rebuild. That is the biggest gap in the game's grandeur.
2. **The built cities are good maps but small pictures.** Emporion, Thyrsa,
   Eleusa, Delphoi, Knossa Palace, Arkadia and Paphia all follow STYLE §4.
   None of them has a thing that is *bigger than the screen*. Every landmark
   fits inside 8×6 metatiles, so nothing makes the player stop. Gen 3's own
   awe moments (Sootopolis's crater, Sky Pillar, the Groudon/Kyogre reveal)
   come from scale and from the camera, not from detail.
3. **There is no colossal figure anywhere in the main game.** The only giant
   statue is the Bronze Heel on Knossa's shore, a 3×4 foot. It's a fine seed
   with nothing to pay it off.
4. **Ruins look tidy.** Route 4's tombs, Nemea's columns, Kronion Hill's
   shrine and Hecate's Hollow use whole columns, whole stelai and clean
   rectangles. Nothing is fallen, half-buried or overgrown. There is no
   shared ruins vocabulary, so each tileset improvises its own.
5. **Tile budgets are the hard constraint.** Almost every secondary tileset is
   full:

   | Tileset | Tiles used (cap 504; 496 with wide doors) | Maps on it |
   |---|---|---|
   | aethos (primary) | 492 / 512 | all exteriors |
   | kalliste | 491 | 8, including Astyra ×3 and Kaldera |
   | skiron | 496 | 14 (Route 4, Nemea, Aigion, Route 11 and the others) |
   | agros | 496 | Route 1, Kronion Hill |
   | chion | 492 | 6 (the Ascent's snow floors, Olympus Summit) |
   | civic | **503** | 17 interiors. It is already past the 496 door-safe line. |
   | thyrsa | **506** | Thyrsa. It is over the 504 cap in CLAUDE.md. |
   | delphoi | 475 | Delphoi |
   | isthmos | 329 | EmporionHarbor only |
   | stair_of_hours | 416 | StairOfHours only |

   **Rule that follows:** each colossus gets either a tileset no one else
   shares (isthmos, stair_of_hours) or a new secondary for its map. No
   colossus can be squeezed into a shared, full set.
6. **Neighbors can't show each other's landmarks.** A connected map is drawn
   with the tilesets of the map the player is standing on (MAP_DESIGN §5), so
   a statue on one map turns to garbage when seen from across the seam.
   Sight lines have three options:
   - stay inside one map
   - put both maps on one shared secondary
   - draw a separate "distant view" of the landmark in the neighbor's own set

---

## 1. Colossi

### How a colossus is built on a GBA

- **Scale.** The play screen is 15×10 metatiles. A figure 8–11 metatiles tall
  fills the screen's height, and that is the threshold for awe. Anything
  under 5 tall reads as "a statue", not "a colossus".
- **Walk behind it.**
  - Collide only on the plinth.
  - Draw the figure's body above the plinth on the metatile **top layer**, so
    the player walks *behind* its shins and torso.
  - Being hidden by the statue is what sells its size.
- **Tile cost.** Count about 4 unique tiles per covered metatile, times the
  fill (0.5–0.8 for a figure). Mirror symmetric parts with h-flip (a throne,
  a pediment, a shield), which cuts their cost by about 40%.
- **One palette per colossus** (of the 7 secondary slots):
  - bronze: a 5-step ramp plus verdigris and a gold highlight
  - chryselephantine: an ivory ramp plus gold
  - weathered marble
- **Life.** One animated element per colossus makes it feel alive at little
  cost. Use the existing tileset animation hooks:
  - a beacon fire
  - lava seams
  - a gleam that travels down a spear
- **The reveal.** The camera pans with `special(SpawnCameraObject)` and
  `applymovement(OBJ_EVENT_ID_CAMERA, …)`. Delphoi and the Temple of Hestia
  already use this. Each colossus below names its approach and its pan.
- **Moving parts.** Use a 64×64 object sprite (`gObjectEventBaseOam_64x64`, as
  Kyogre/Groudon use) only for a part that must move, such as an eye or an
  arm in a post-game wake. Everything else stays in tiles.

### Ranked

| # | Colossus | Map | Size (metatiles) | Est. tiles | Tileset plan |
|---|---|---|---|---|---|
| C1 | **Athena Promachos** | Astyra_Akropolis, plus a "spear over the rock" view in Astyra | 4×9 | ~90, plus ~20 for the city view | new `akropolis` secondary (0 → ~330 with the Parthenon and Propylaia); the city view goes in the new `astyra` |
| C2 | **The bronze man of Kaldera** | Kaldera | 6×10 | ~120 | new `kaldera` secondary |
| C3 | **Hermes Empolaios on the mole** | EmporionHarbor | 5×9 | ~100 | isthmos: 329 used, 167 free. It fits with no new set. |
| C4 | **Zeus enthroned** | Olympus_Summit | 10×11 | ~250 | new `olympus_summit` secondary. Chion is full and shared by 6 maps. |
| C5 | **The Sleeping Titan** carved in Kronion Hill | KallisteRoute1_KronionHill | 18×6 relief | ~140 | new `kronion` secondary. Agros is full. |
| C6 | **The Horai and the great water-clock**, the Lord of Time's hall | StairOfHours (summit) | 12 statues of 2×5 and one clepsydra of 6×8 | ~200 | stair_of_hours has 80 free: mirror the Horai in pairs, or split off a `stair_summit` set |
| C7 | The Naxian Sphinx on its column (a cheap win) | Delphoi | 2×6 | ~30 | delphoi has 21 free; dedupe or trim to fit |
| C8 | The fallen Colossus of Rhodos (already planned) | Rhodos, post-game | — | — | out of scope. It must not look like C3: Rhodos is fallen, Helios and broken; Emporion is standing, Hermes and lit. |

#### C1. Athena Promachos over Astyra (mockups 1 and 2)
- **Where.**
  - Astyra_Akropolis, on the plateau between the Propylaia and the
    Parthenon, at about (9, 13).
  - It faces the Propylaia, so the player meets it head-on through the gate.
- **What the player sees.**
  - **From the city:** Astyra's north edge shows the Akropolis's south
    cliff. Above it rise the helmet crest and the spear, with a gold tip.
    This is the "distant view": 3×4 metatiles drawn into `astyra`.
  - **On first entry:** the camera pans up the Panathenaic Way from the
    Dipylon gate to the rock and holds on the spear tip for one beat (§3,
    Astyra).
  - **Through the Propylaia:** the first plateau screen frames Promachos at
    left-centre and the Parthenon's whole front at right.
- **Story.**
  - The midpoint: Team Titan storms the Akropolis for the second fragment,
    and you fight up the ramp beside Alethea, then face Kleon.
  - **(story: director)** The fragment was hidden in plain sight: the spear's
    gold tip, the gleam that sailors saw from Sounion (Pausanias 1.28),
    which is the Harpe's adamant.
  - The Titans' grunts climb the statue's scaffolding, and you watch the
    gleam go out.
  - After the midpoint the spear stays dark. It's a scar that everyone in the
    city can see.
- **Tiles.** Promachos is ~90 tiles. The Parthenon is ~60, because its columns
  repeat. The Propylaia and the Erechtheion are ~80 together, and the ruins
  kit adds ~60. That puts `akropolis` at about 330, leaving headroom.

#### C2. The bronze man of Kaldera (mockup 3)
- **Where.**
  - On the caldera's central islet (Nea Kameni), at about (10, 13).
  - He stands in a casting pit, with timber scaffold up one side.
  - The Telchines Forge's mouth opens at his feet.
- **What the player sees.**
  - The trireme sails in through the ring's western gap.
  - The first screen inside shows him dark against the red-and-white banded
    cliffs.
  - Lava glows in the pit, and a single orange seam runs neck to heel. That
    seam is "one vein, stoppered with a bronze nail", as Alethea says at the
    Bronze Heel.
- **Story (story: director).**
  - In Ichor, Talos is the Hierophant, the smith who was once Perdix. This
    proposal adds that he took his name from this unfinished second bronze
    man.
  - He is casting it to replace the first one, whose ruined heel lies on
    Knossa's shore (LABYRINTH seed 16).
  - Its heel is the one piece he has never been able to cast.
  - This pays off the Bronze Heel, gives Kaldera's low point a silent witness,
    and sets up the post-game S2 "Forge Under the Forge".
  - **Payoff:** after Laurel 6 its eyes light, as one animated tile pair.
- **Tiles.** ~120 for the figure and scaffold. The `kaldera` set also needs
  ~200 for the town: basalt cliffs with red pumice bands, whitewashed rim
  houses, blue domes (islands only, STYLE §4.5), black sand and the
  switchback stair. That is about 350 in total.

#### C3. Hermes Empolaios on Emporion's mole (mockup 4)
- **Where.**
  - EmporionHarbor, on the mole head at the map's south-east (x 41–46,
    y 15–24).
  - Widen the mole's end into a 7×10 platform.
  - He strides, chlamys blowing, petasos winged.
  - His raised hand holds a caduceus that burns as the harbor's beacon. The
    fire is a 3-frame animation.
- **What the player sees.**
  - If the Act I trireme berths here, this is the first sight of the
    mainland. The berth screen has the statue filling its right third.
  - Coming down from the city, the camera pans east along the quay to the
    mole.
- **Story.** Hermes is Emporion's god (Laurel 2), and *Empolaios* ("of
  commerce") is his real epithet. He is the first proof that the mainland is
  bigger than home, and an Act I lesson in scale before the player's first
  big city.
- **Tiles.** ~100 tiles plus 1 palette. Isthmos has 167 free and no other map
  uses it, so this is the cheapest colossus in the plan.

#### C4. Zeus enthroned at the Summit (mockup 5)
- **Where.**
  - Extend Olympus_Summit 12 rows north.
  - Cut a niche into the summit cone behind the temple of the Twelve.
  - Zeus sits in it, gold robe over ivory, with the sceptre in his left hand
    and Nike in his right: Phidias's Olympia figure, at 10×11.
- **What the player sees.**
  - Climbing the stair, the temple's pediment rises first.
  - At the stair's crest the camera tilts up past the roof to his face.
  - He is the only thing on the map bigger than the temple.
- **Story.** POSTGAME §3.4 and OIKOUMENE_GUIDE say Phidias's empty throne at
  Olympia "stood up and walked to Olympus". This is where it sat down.
  - **Post-game (story: director):** setting the thunderbolt lot wakes the
    Olympanax, and the niche is left empty: the same tiles without the figure.
- **Tiles.**
  - ~250 for the figure. The throne back and arms are mirrored.
  - Give the Summit its own `olympus_summit` set with the temple and altar
    moved into it.
  - Chion stays with the Ascent's floors.
  - LEAGUE.md names the summit plateau as aethos plus Aegina, but the layout
    uses Chion. Settle that first.
- **Timing.** Build only after the Ascent/Propylaia helper lands, because
  `tools/ichor/maps/ascent_summit.py` owns this layout.

#### C5. The Sleeping Titan (Kronion Hill)
- **Where.**
  - The Hill of Kronos's crest.
  - A reclining giant is worn into the limestone along 18 metatiles: brow,
    closed eye, beard, a chest that is the hilltop, and a hand that is the
    dig site.
  - Ivy and wild olive grow in the folds.
- **What the player sees.**
  - From Route 1 below, it reads as a hill.
  - Halfway up, a lookout turn shows it as a face: one camera pan along the
    profile.
- **Story.**
  - Act I beat 2: the grunts are digging at the giant's hand for the Harpe
    fragment.
  - Plutarch's Kronos sleeps bound on a western island. **(story: director)**
    The islanders' joke is that the hill is him.
  - This is the game's first grand image, in the prologue. It foreshadows the
    Titans and tells the player this land is older than its people.
- **Tiles.** ~140 for the relief. A new `kronion` secondary also takes
  Kronion Hill's existing shrine pieces and the ruins kit. Route 1 keeps
  agros, and the seam strip stays on aethos.

#### C6. The Lord of Time's hall
- **Where.** The top of StairOfHours, a 24×110 sky column.
  - Widen the last 30 rows into a round platform.
  - Twelve standing Horai (the Hours) ring it, 2×5 each, frozen mid-step.
  - At the centre is a 6×8 bronze water-clock (clepsydra) whose falling
    water, an animation, stops at the Frozen Hour.
- **The reveal.** The stair spirals up past the statues one by one, so the
  player counts the hours. The camera holds on the clock as it stops.
- **Story.** The Frozen Hour, and the Stair of Hours fight against Kronos and
  Hyperion. The stopped clock is the image of the whole act.
- **Tiles.** stair_of_hours has 80 free. The Horai pair as mirror images (6
  designs, h-flipped) at ~25 tiles each, which comes to ~150, plus ~50 for
  the clock. Either trim the stair's sky set or split off `stair_summit`.

#### C7. Cheap wins: under 40 tiles each, no new set
- **Delphoi:** the Naxian Sphinx on its Ionic column beside the Sacred Way,
  2×6.
- **Thyrsa:** the Sphinx crouched on a rock column outside the south gate,
  where she asked her riddle. It's one 3×4 block, about 30 tiles.
  - thyrsa is already at **506 tiles**, past CLAUDE.md's 504 cap.
  - Free its tiles first, by deduping or moving the field and vineyard
    pieces to thyrsa_stone, and then place the Sphinx.
- **Knossa Palace:** giant horns of consecration (3×2) over the south
  entrance, as at Knossos. They are palace_minos's signature, and that set
  has 167 free.
- **Paphia:** the foam rock where Aphrodite rose, a sea stack offshore with
  an animated foam ring. Use paphia's last ~9 tiles, or move it into kythera
  (40 free).

---

## 2. Grand temples

A temple reads as grand from five things:
- a **stepped platform** (krepis, 3 steps)
- **column depth** (two rows, or a pronaos shadow)
- a **pediment** with sculpture or color
- a **precinct** (a temenos wall and a propylon)
- an **approach axis**: the altar outside in front, then the facade, and the
  temple raised above the player

Every temple below is graded on those, exterior first, then interior.

| Laurel | Today | Missing | Fix |
|---|---|---|---|
| 1 Hestia (Akti) | Exterior on a rise above the harbor. The interior has a strong hearth axis and red carpet to the fire. The best interior in the game. | Precinct; the altar outside | A 1-tile temenos wall with a propylon at the stair foot, and a round hearth-altar (*eschara*) in front of the doors. |
| 2 Hermes (Emporion) | A small 3-column front at the plaza's south edge; a white puzzle interior | Scale and a platform. It's lower than the Deigma next to it. | Raise it on a 5-step podium. Line the approach with an avenue of herms, so the town's crossroads herms lead to it. Add a gold pediment (AETHOS_MAP names "a temple front with a gold pediment"). Pair it with C3. |
| 3 Demeter (Eleusa) | The Telesterion exterior is a long hall. The interior is a dark grid of columns. | The Telesterion is a **forest of columns** (STYLE §4.6). The interior grid is right but unlit and flat. | Interior: 7×6 columns with torch pools of light between them (the darkness rule, MAP_DESIGN §3), the Anaktoron as a lit stone room at the centre, and rock-cut stepped seating along two walls. Exterior: a Great Propylaia gate and the Kallichoron well on the approach. |
| 4 Dionysus (Thyrsa) | The Kadmeia temple is on the citadel with stairs and a painted pediment. The interior is theatrical bands. | The theater is invisible from the overworld. | Cut the theater cavea into the hillside outside the north-east wall, on the Thyrsa exterior: 12×8 of stepped seats facing the vineyards. It is the town's grand skyline object. |
| 5 Artemis (Arkadia) | A temple on a plinth with stairs and a waterfall pool. The interior is moonlit pools. | Height. The temple sits in the town instead of above it. | A Bassae-style approach. Move the temple's *read* up the mountain by adding a 2-level terrace behind it, and frame it in cypress masses instead of the tree grid. Reveal it around a bend. |
| 6 Hephaestus (Kaldera) | **Placeholder** (a Civic sample hall) | Everything | A new `temple_hephaestus` set. A Doric temple on the rim's highest terrace above the caldera, looking at C2. Interior: a forge-temple with an anvil altar, bellows-puzzle braziers, bronze tripods (Iliad 18), and the Hierophant on a dais over a lava channel. |
| 7 Aphrodite (Kythera) | A pink sanctuary on an axis at Paphia. The interior is a rose maze, then a white hall. | Precinct depth; the sacred stone | Paphos's real cult object was an aniconic conical stone, not a statue. Put a dark baetyl stone under a columned shrine at the hall's head, add rose-garden terraces in two levels, and add a foam rock offshore (C7). |
| 8 Apollo (Delphoi) | The exterior is strong: a temple on its terrace above the treasuries. **The interior is bare**: a gray floor and repeated statues. | The adyton | Rebuild the interior as cella columns in two rows → the adyton down 3 steps → the omphalos, the laurel and the tripod over a steam vent (animated). Carve the E and "Know thyself" on the pronaos. Outside, make the temple wider and raise it on the famous **polygonal retaining wall**, 2 metatiles high, the same height as the Sacred Way. |

Major sanctuaries beyond the Laurels:
- **The Parthenon** (C1): 14×8 on a 3-step krepis, the frieze painted. It's
  the only Doric octastyle in the game; keep it unique.
- **Aegina's Temple of Aphaia** is already good: a temple on a pine ridge
  over the sea. Add one fallen column drum on its terrace as ruins-kit
  practice.
- **The temple of the Twelve** (Olympus Summit) gets its scale from C4
  behind it.
- **Lakonia's Orthia** stays austere by design. Add only the altar and the
  running track in front.

---

## 3. The great cities

### Astyra (rebuild): the capital (mockup 1)
- **Weaknesses.**
  - A placeholder on borrowed tiles.
  - Grass fills over 80% of the map.
  - There is no wall, no agora, no hill and no skyline.
  - The Akropolis is a separate corridor with no view of it from the city.
- **Fixes.**
  1. **The Akropolis rock across the north,** a limestone mass 30 metatiles
     wide with a cast-shadow cliff. Promachos's spear and the Parthenon's
     pediment show above it (C1). That is the skyline.
  2. **The Panathenaic Way.** It runs diagonally from the Dipylon gate in the
     south-west, through the agora, to the Propylaia ramp. It's the one road
     that isn't on the grid, and it's the camera pan's path.
  3. **The agora,** open on the flattest ground. The Stoa of the Archon runs
     along its north side and a long stoa down its east side. A fountain
     house and herms stand in it. Keep it open; let the stoas frame it.
  4. **The asty:** courtyard-house blocks on the slopes. Blank walls, one
     door each and red-tile roofs, in 3 heights and 2 roof pitches so no two
     blocks repeat.
  5. **Outside the gate:** the Kerameikos, grave stelai and cypress along
     the road, where the ruins kit's broken stelai belong. The Pnyx is a
     terraced hill to the east; it becomes the vista point.
- **Tileset.** A new `astyra` secondary, shared by Astyra and Astyra_Harbor.
  Route 16's seam stays aethos-only.

### Kaldera (rebuild) (mockup 3)
- **Weaknesses.** A sand crescent with no cliffs, no town and no forge. The
  STYLE §4.7 brief ("caldera cliffs with white towns on the rim, black-sand
  beaches, a buried Bronze Age town in the ash") is entirely unbuilt.
- **Fixes.**
  1. **A ring of cliffs** open to the west, banded red and white pumice over
     black basalt.
  2. **A white town on the eastern rim,** stepped down the cliff, with blue
     domes on the shrines only.
  3. **A switchback donkey stair** from the rim to the black-sand port. It's
     the map's compression-and-release moment.
  4. **The islet** with C2 and the Forge mouth.
  5. **The ash cliff** with the buried town's door: a fresco wall showing
     through the ash, and the Labrys gate (AETHOS_MAP).

### Emporion (mockup 4 for the harbor)
- **Weaknesses.**
  - One pale plaza paves about 55% of the city in a single metatile, which
    fails STYLE §4.2's ground rule.
  - Buildings ring it symmetrically.
  - Potted plants and stalls sit in a grid.
  - There is no skyline.
  - The Long Walls aren't drawn.
  - The temple is lower than the Deigma.
- **Fixes.**
  1. **Break the plaza into a Hippodamian grid** (STYLE: Emporion is
     planned). Use 3-wide streets and blocks of shops and houses, with the
     agora as a single open block.
  2. **The Long Walls** leave the north edge as two parallel towered walls
     running inland. That's an instant sense of a great city.
  3. **Raise the Temple of Hermes on its podium** (§2) and add the
     Hephaisteion on a small hill (Kolonos) in the west. That gives two
     heights on the skyline.
  4. **The harbor scene:** C3 on the mole, the ship sheds kept, and a long
     two-storey market stoa on the quay instead of loose crates.
  5. **Market life:** stalls in irregular clusters near the harbor gate,
     amphora stacks and a fish market. Move the potted plants to doors.

### Thyrsa
- **Weaknesses.**
  - The walls are one straight height with no towers between the corners.
  - The citadel's cobble is one metatile everywhere.
  - Fields are rectangles.
  - The theater can't be seen from the overworld.
- **Fixes.**
  1. Make the walls step up the Kadmeia hill. Add towers at gates, with at
     least 3 of Thebes's 7 gates readable.
  2. The theater cavea in the hillside (§2).
  3. Turn the vineyard terraces into stepped *pezoules* instead of flat
     plots.
  4. The Dirce spring gets a fountain house.
  5. The Sphinx column outside the south gate (C7).

### Eleusa
- **Weaknesses.**
  - The village is lovely but low.
  - The sanctuary is a hall beside the houses.
  - The Sacred Way's start is just a road.
- **Fixes.**
  1. A Great Propylaia gateway and an inner propylon make a sanctuary
     precinct with a wall.
  2. Raise the Telesterion on a rock-cut terrace with stepped seating on its
     flank.
  3. Put the Kallichoron well on the approach.
  4. Give the Sacred Way's first 10 metatiles roadside tombs and shrines
     (ruins kit).

### Arkadia
- **Weaknesses.**
  - Cypress stand in one-by-one columns (STYLE §4.1's forest-grid flaw).
  - The town is flat.
- **Fixes.**
  1. Interlocking cypress masses.
  2. The temple raised a terrace higher (§2).
  3. Pan's grotto drawn as a cave mouth in a crag with votive reliefs.
  4. A shepherds' fold.

### Kythera's towns (Paphia, Skandeia)
- **Weaknesses.**
  - Strong axes, but the white boxes repeat: the same cube in 6 places.
  - Paphia's plaza is pink paving with nothing in it.
- **Fixes.**
  1. Vary the cubes in 2 heights, with flat roofs, outside stairs and a
     pergola.
  2. The foam rock (C7).
  3. Rose-garden terraces up to the sanctuary.
  4. In Skandeia, a shipwright's slip with a half-built hull: a harbor scene
     that is unique to Kythera.

### Knossa Palace
- **Weaknesses.**
  - The central court is excellent.
  - The wings repeat one long-building strip 8 times.
  - The palace is one storey everywhere.
- **Fixes.**
  1. Vary the wing heights to 1, 2 and 3 storeys, with light-well openings.
  2. Put the horns of consecration on the roofline (C7).
  3. Show the Grand Staircase as an exterior light well with red columns.
  4. Show one fresco wall (the griffins) through an open portico.

### Lakonia (Sparta)
- **Weaknesses.**
  - Austere is right, but it's flat dirt.
  - The stadium oval reads as Roman.
  - The Menelaion across the river is just a pickup.
- **Fixes.**
  1. Make the stadium a straight Greek track with one turning post.
  2. Build the Menelaion as a Mycenaean ruin on its ridge: a stepped
     platform of cyclopean blocks with the ruins kit, a shrine of Helen and
     Menelaos.
  3. Give Taygetos's wall a single dark ravine (the Kaiadas) as a vista.

### Delphoi
- **Weaknesses.**
  - The layout is strong, but the temple (7 columns) is small for its
    terrace.
  - The treasuries look alike.
  - The Phaedriades are flat brown bands.
- **Fixes.**
  1. Widen the temple and raise it on the polygonal wall (§2).
  2. The Naxian Sphinx (C7).
  3. The bronze Charioteer on a base by the Sacred Way's turn.
  4. Give each treasury its own front: Doric, Ionic, and one with
     Karyatids, like the Siphnian.
  5. Make the Phaedriades "shining": a two-tone cliff with a highlight band
     and the Castalia ravine cut between them.

---

## 4. Ruins style guide (proposed STYLE.md §4.8)

> Ichor's ruins are **an older world lying down in a living one**. They're
> what makes Aethos feel ancient and unexplored. A ruin is mostly horizontal,
> partly buried and overgrown, and always tells you what it used to be.

### 4.8.1 How Ichor ruins look
- **Fallen beats standing, about 3 to 1.**
  - Columns lie as **separated drums** (3–4 discs in a line, slightly
    offset), not as whole shafts.
  - Columns still standing come in groups of 2 or 3 of **uneven height**,
    sometimes carrying one architrave block between them.
- **The plan shows through.** A stylobate outline (a line of foundation
  blocks) traces the lost building's footprint, so the player reads "a
  temple stood here".
- **Pieces.**
  - **Capitals:** Doric echinus or Ionic volute, lying where they fell.
  - **Pediment fragments:** a triangle corner, lying face-up.
  - **Statues:** a statue fallen on its back, and a **plinth with only the
    feet left**, which is the most evocative piece in the kit.
  - **Steps:** half-buried, with the top 1–2 steps showing and grass on the
    treads.
- **Nature wins at the edges.**
  - ivy over walls and stubs, on the top layer
  - wild olive grown out of a cella floor
  - poppies and thistle in the cracks
  - acanthus beside capitals, a nod to the origin of the Corinthian capital
  - moss on north faces, which on our top-down maps means the bottom edges
- **Palette (one ruins palette):**
  - weathered marble: warmer and darker than living-temple marble
  - limestone gray: 3 steps
  - moss green: 2 steps
  - ivy: 2 steps
  - poppy red
  - soil
  - **Rule:** ruins are never as bright as a working temple, so the eye knows
    which one is alive.
- **Collision.**
  - Stubs, drums and statues block.
  - Stylobates and buried steps are walkable.
  - A fallen column can be a **ledge-like wall that makes a little maze**.
    Make it the dungeon's teaching mechanic for darkness or pushing, where it
    fits.

### 4.8.2 The kit
Draw it once as a Porytiles source sheet, about 36 metatiles and 80–110
tiles, in `tools/ichor/art/ruins_kit/`. Copy only the subset each map uses
into its secondary.

| Group | Pieces (metatiles) |
|---|---|
| Columns | drum (1×1, two variants); standing stub, short and tall (1×1, 1×2); fallen line of drums (3×1, and 1×3 vertical); a column with ivy (1×2) |
| Entablature | Doric capital (1×1); Ionic volute capital (1×1); architrave block with triglyphs (2×1); pediment corner (2×1) |
| Platforms | stylobate edge set (straight, outer corner, inner corner); cracked floor (3 variants with grass in the joints); half-buried steps (left, middle, right) |
| Statuary | fallen torso (2×1); head (1×1); plinth with feet (1×1); toppled stele (1×1); broken pithos (1×1) |
| Walls | ashlar wall stub edge set; cyclopean block (Mycenaean: Lakonia, Knossa); dry-stone wall broken end |
| Nature | ivy curtain overlays (top layer, 3); wild olive in a ruin (2×2); poppy clump; thistle and acanthus; moss overlay; rubble ground variant (2) |

**A micro-kit in the primary.** Aethos has 20 free tiles. Spend them on 4
seam-safe pieces usable on every exterior:
- a single drum
- a fallen drum pair
- a capital
- a rubble ground variant

Then any route can scatter a ruin without touching its secondary.

### 4.8.3 Where to apply it
| Place | Use |
|---|---|
| **Kronion Hill's shrine** | The shrine around C5's dig: a stylobate outline and a plinth-with-feet where the Kronos statue stood |
| **Route 4's tombs** | Toppled stelai, a broken pithos, family plots with half-buried steps; the Titans' rock as a fallen pediment |
| **Hecate's Hollow** | A ruined crossroads shrine (three herm-stubs facing three ways, Hecate's form); ivy and moss in the dark palette |
| **The Labyrinth** | Not ruins-kit marble. The palace's red-and-ochre fallen columns, which taper downward, belong only to Knossa. |
| **The Korykian Cave** | Votive clutter: small broken figurines and fallen offering stones near the Pan and nymph altar |
| **Aigion: drowned Helike** | Column tops in the shallows: the kit's drums drawn as water-edge tiles; the bronze Poseidon below (WORLD_EXPLORATION G1/G2) |
| **Nemea** | The model ruin: the Temple of Zeus with **three standing columns** and its drums fallen in a line, as the real Nemea stood for centuries. That's Nemea's signature. |
| **Route 11's fallen temple** | Drums strewn down the gorge slope, as if an earthquake rolled them. It makes the "drum pass" literal. |
| **Lakonia's Menelaion** | A cyclopean platform (§3) |
| **The Akropolis** | The Old Temple's foundations beside the Parthenon: ruin and living temple side by side, the clearest teaching image |
| **Eleusa's Sacred Way, Astyra's Kerameikos** | Roadside tombs and broken stelai |

Skiron is full and carries Route 4, Nemea, Aigion and Route 11. Move **Nemea
and Aigion** to a new `nemea` secondary that takes the full kit, and use the
primary micro-kit on Route 4 and Route 11.

---

## 5. Build order: the top 10

Each item is one helper task. **Files** lists what it owns. Items in the same
wave share no files and can run in parallel. Run 2–3 helpers at a time (the
standing usage rule).

| # | Task | Files it owns | Wave |
|---|---|---|---|
| 1 | **Astyra rebuild:** a new `astyra` secondary; the city per §3 with the Panathenaic Way pan and the Promachos distant view; Astyra_Harbor re-laid on it | `data/tilesets/secondary/astyra/`, `data/layouts/Astyra*`, `data/maps/Astyra/`, `data/maps/Astyra_Harbor/`, tileset headers | A |
| 2 | **The Akropolis and Athena Promachos (C1):** a new `akropolis` secondary; ramp, Propylaia, Promachos, Parthenon, Erechtheion and the Old Temple ruins; the midpoint script's positions kept | `data/tilesets/secondary/akropolis/`, `data/layouts/Astyra_Akropolis/`, `data/maps/Astyra_Akropolis/` | A |
| 3 | **Kaldera rebuild and the bronze man (C2):** a new `kaldera` secondary; ring cliffs, rim town, stair, islet and giant, the ash-cliff door | `data/tilesets/secondary/kaldera/`, `data/layouts/Kaldera/`, `data/maps/Kaldera/` | A |
| 4 | **Hermes Empolaios on the mole (C3),** plus the Emporion temple podium and the Long Walls | `data/tilesets/secondary/isthmos/`, `emporion/`; `EmporionHarbor`, `EmporionCity` layouts and maps | B |
| 5 | **Zeus enthroned at the Summit (C4):** a new `olympus_summit` set; the map extended 12 rows | `olympus_summit/` set, the `Olympus_Summit` layout and map, `tools/ichor/maps/ascent_summit.py` | **After the Ascent helper lands** |
| 6 | **The ruins kit:** the source sheet, the 4-piece primary micro-kit, and STYLE.md §4.8 from §4 above | `tools/ichor/art/ruins_kit/`, `data/tilesets/primary/aethos/` (only the 20 free tiles), `design/STYLE.md` | B |
| 7 | **Delphoi grandeur:** the polygonal wall and a wider temple, the Naxian Sphinx, the Charioteer, distinct treasuries; the Temple of Apollo interior rebuilt around the adyton | `delphoi/`, `temple_apollo/`, the `Delphoi` and `Delphoi_TempleOfApollo` layouts and maps | B |
| 8 | **Kaldera's interiors:** a new `temple_hephaestus` set and the forge-temple (Laurel 6 puzzle kept); the Telchines Forge as a forge cave with anvils and lava channels | `temple_hephaestus/`, `Kaldera_TempleOfHephaestus`, `Kaldera_TelchinesForge` | C (after 3, for a matching look) |
| 9 | **The Lord of Time's hall (C6):** the summit platform, 12 Horai, the clepsydra that stops | `stair_of_hours/` (or a new `stair_summit/`), `StairOfHours` | C |
| 10 | **Kronion Hill: the Sleeping Titan (C5)** and its shrine ruins on a new `kronion` set | `kronion/`, `KallisteRoute1_KronionHill` | C (after 6, for the kit) |

**Next after the top 10:**
- the ruins application pass: the `nemea` split; Route 4, Route 11, Hecate's
  Hollow, Lakonia's Menelaion
- Thyrsa's theater and walls
- Eleusa's precinct and Telesterion lighting
- the Knossa wing heights and horns
- Kythera's foam rock and varied cubes
- Arkadia's canopy masses

**Waves.**
- **A:** 1, 2 and 3. Each is a new tileset and its own maps, so they have no
  overlap. They are the biggest gap, so they go first.
- **B:** 4, 6 and 7. Item 6 edits the primary's free tiles only, and the
  others don't touch the primary.
- **C:** 8, 9 and 10.
- **Item 5** waits on the Ascent/Propylaia helper.

**Shared files.** Every item that adds a tileset edits the shared tileset
registration files (`src/data/tilesets/headers.h`, `graphics.h`,
`metatiles.h`). Keep each addition a self-contained block so parallel merges
resolve cleanly. Every item must leave `make` green, `smoke_test.sh` passing,
and the ROM-budget line checked.

**Per-task gate** (STYLE §4.4):
- a beauty shot of the reveal screen before cutting tiles
- three render-and-critique passes
- `map_style_audit.py`
- a walk in game, including the camera pan
- the before and after renders sent to the user, per the "show map images"
  rule

---

## 6. Mockups

| # | File | Shows |
|---|---|---|
| 1 | `design/art/awe_pass/1_astyra_city.png` | Astyra's plan: the Akropolis rock with Promachos and the Parthenon over the city, the agora and stoas, the Panathenaic Way, the reveal screen and the entry pan |
| 2 | `design/art/awe_pass/2_astyra_akropolis.png` | The Akropolis: the switchback ramp, the Propylaia, Promachos at 4×9 in the first plateau screen, the Parthenon at 14×8, the Erechtheion and the Old Temple ruins |
| 3 | `design/art/awe_pass/3_kaldera.png` | The caldera ring, the rim town, the switchback stair, the islet with the bronze man at 6×10, and the trireme's reveal screen |
| 4 | `design/art/awe_pass/4_emporion_harbor.png` | Hermes Empolaios at 5×9 on the widened mole head over the current harbor render, with the berth screen and the pan from the city road |
| 5 | `design/art/awe_pass/5_olympus_summit.png` | The Summit extended 12 rows north, with Zeus enthroned at 10×11 behind the temple of the Twelve over the current render |

The white frames are the 15×10 play screen. Yellow arrows are camera pans
and white arrows are walking routes. Figures are at true metatile scale.
