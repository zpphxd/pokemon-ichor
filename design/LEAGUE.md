# The League: the Ascent, the Pantheon and the Archon

STORY.md's League rows L-6 to L-10 (§3), §6.15 and §7.10–7.11, built as ten maps.
The Ascent climbs Olympus through the cloud; the Pantheon is four seats in sequence;
the summit holds the Archon, Medon's Knot and the temple of the Twelve, whose cella
is the Hall of Heroes. Levels come from BALANCE.md's League row.

## The route through it

```
(Tempe, not built) ··> Ascent_1F ──> Ascent_2F ──> Ascent_Icefall ──> Ascent_Glacier ──> Ascent_3F ──> Olympus_Propylaia
   placeholder: the     the slopes   cloud ledges   ice caves, the     the Giants, the     above the     the hearth, the
   muleteer in Astyra                (camp, herm)   slide hall, seal   Gate of the Winds   cloud, keeper  healer, the door
                                                     │      │                                                  │
                                       IcefallDeep ──┘      └── CrystalVault (Labrys; Thread from the Glacier)  │
                                       (Torch, Conch, Horn)                                                     │
   Olympus_HallOfHeroes <── Olympus_Summit <── SeatOfHera <── SeatOfAthena <── SeatOfPoseidon <── SeatOfAres <──┘
   (the temple's cella)     (the altar, the Archon)
```

- **Gate.** All eight Laurels (`FLAG_BADGE01_GET`..`08`). The muleteer in Astyra checks them.
- **Placeholder.** Route 29, Thermopylai, Route 30 and the Vale of Tempe (AETHOS_MAP.md) are not
  built. Until they are, the Ascent's east road end (Ascent_1F's warp at the east edge) leads to
  Astyra's muleteer, and the muleteer walks you to the foot of the mountain. When Tempe is built,
  replace that warp with Tempe's connection and retire the muleteer (`Astyra_EventScript_Muleteer`).
- **The Pantheon run** follows Emerald's Elite Four (`EverGrandeCity_*Room`): each seat's door locks
  behind you (`VAR_ELITE_4_STATE`), each defeat flag opens the far door, nothing heals between
  seats, and a whiteout resets all four (`EventScript_WhiteOut` →
  `EverGrandeCity_HallOfFame_EventScript_ResetEliteFour`, kept). The four defeat flags are
  Emerald's `FLAG_DEFEATED_ELITE_4_*`, aliased as `FLAG_ICHOR_BEAT_<MEMBER>`.

## Map briefs (STYLE.md §4.6)

### Ascent_1F, the Pierian slopes
- **Sentence:** a mule road switchbacks up Olympus's pine-clad foot, three terraces above the sea,
  to where the first cloud sits on the mountain.
- **Land:** the mountain rises to the north-west; its foot breaks off south in a limestone sea cliff
  over the Thermaic gulf. Two cut banks step the slope into three terraces; a dry torrent bed
  (*cheimarros*) of white stones comes down from the north-west. Black pine and kermes oak hold
  every slope too steep to walk.
- **Settlement logic:** the road is the Archon's processional road, so it is paved at the bends and
  marked with milestones; the guard's beacon tower stands on the one knoll that sees the gulf, where
  fires announced a challenger; climbers who died on the road lie in stelai at the bends. The road
  enters from Tempe at the east, along the cliff.
- **Reveal:** the first leg runs the cliff edge with the open sea below; at the top of the third
  terrace the road walks into a wall of cloud (the warp to 2F, under the fog).
- **Signature:** the challengers' beacon tower on its knoll, and the stelai of the fallen at the
  bends.

### Ascent_2F, the cloud ledges
- **Sentence:** inside the cloud, a narrow road clings to bare cliff faces, ledge by ledge, past the
  camp where the Titans' lost followers wait for a master who isn't coming.
- **Land:** the timberline. Grey limestone faces in tall bands, scree fans of loose stone, a few
  wind-bent pines; the ground falls away to the south-east into cloud with the sea far below,
  glimpsed through the fog (`WEATHER_FOG_HORIZONTAL`).
- **Settlement logic:** the only flat ground is an overhang ledge with a spring; that is where the
  ex-Titanborn pitched their tents, because nobody else wanted it. The road has to go where the
  ledges go: a long traverse west, a scramble up a scree fan, a traverse back east.
- **Reveal:** the camp, firelit in the fog, halfway up; above it the cliffs end and light comes
  through the cloud (the warp to 3F).
- **Signature:** the ex-Titanborn camp (tents, cookfire, bedrolls) under the overhang: the midway
  rest, with a cook who heals you.

### Ascent_3F, the snowline and the stair
- **Sentence:** above the cloud, on the snowline, the old road becomes a processional stair that
  climbs terrace by terrace to the Pantheon's propylaia.
- **Land:** the last shoulder of the mountain under the summit cone: thin burnt grass, scree and
  snow flurries (`WEATHER_SNOW`); the cloud lies below the south edge. Three terraces, each walled,
  each reached by a stair cut in the rock.
- **Settlement logic:** this is sacred ground, so the road is built: paved terraces with tripods and
  herms, a beacon cairn, then the marble stair straight up the axis to the propylaia, the gatehouse
  of the Pantheon. The last challengers wait at the terrace stairs, where everyone must pass.
- **Reveal:** at the top of the second stair the propylaia's colonnade comes into view whole, framed
  by tripods, with the snow falling across it.
- **Signature:** the processional stair and the propylaia above the cloud.

### Olympus_Propylaia, the gatehouse of the Pantheon
- **Sentence:** a warm hall built around Hestia's hearth, the last rest before the four seats.
- **Land:** inside. A long hall, the hearth in the middle on a raised ring, the inner door behind it.
- **Settlement logic:** Hestia is counted among the Twelve and receives first; her priestess heals,
  a merchant sells for the climb, and the Archon's guard keeps the inner door.
- **Reveal:** the inner door, flanked by guards, at the end of the red runner.
- **Signature:** the League's hearth: the healer at a sacred fire.

### Olympus_SeatOfAres (Brasidas, Fighting)
- **Sentence:** a war hall on a bloodred floor, where captured armor stands in files to the bronze god.
- **Land:** inside (`gTileset_SeatAres`). Blood-red flags, an oxblood runner edged in bronze, smoke-dark
  walls hung with hoplons, crossed spears and war banners; the bronze Ares on his plinth at the head.
- **Settlement logic:** Lakonians build nothing they don't need, so nothing is painted: red stone,
  dark stone, bronze. Trophies of captured armor (tropaia) stand down the aisle the way a phalanx
  stands, tripod braziers burning between them; dark columns and the armory (spear racks, crested
  helmets) line the walls. You walk the file to reach him.
- **Reveal:** the door shuts and the camera climbs the runner to the polemarch under the god.
- **Signature:** the bronze Ares, and the two great braziers that catch when Brasidas raises his spear.

### Olympus_SeatOfPoseidon (Themistokles, Water)
- **Sentence:** a sea hall flooded to the walls, crossed by one causeway: the "wooden wall"
  Themistokles read out of the oracle rides at its mooring.
- **Land:** inside (`gTileset_SeatPoseidon`). A basin of sea water each side of a causeway laid with
  a wave-and-trident mosaic, white marble coping, coral columns standing out of the water, a
  deep-sea wall with a wave frieze and scallop niches; the colossal trident over the admiral's dais.
- **Settlement logic:** the oracle said "trust the wooden wall"; everyone read walls, Themistokles read
  ships. The Pantheon keeps his trireme as an offering, moored against the causeway, as the Greeks
  hung up the prows of Salamis; a bronze dolphin leaps in the other basin.
- **Reveal:** the causeway runs straight across the water to the trident.
- **Signature:** the trireme in the sacred basin, and the trident.

### Olympus_SeatOfAthena (Hypatia, Psychic)
- **Sentence:** a library of lamps at night, where the question is asked aloud.
- **Land:** inside (`gTileset_SeatAthena`). Ivory marble set with gold-and-olive stars, night-indigo
  walls of scroll pigeonholes, lampstands down the aisle, marble owls on pedestals, scroll cabinets,
  the owl roundel in the floor, and Athena's sacred olive growing out of the rostrum.
- **Settlement logic:** Athena's seat is a school: the shelves along the walls, the reading tables
  between them, the philosopher at the rostrum under the olive, as Athena's olive grew from the rock
  of the Akropolis. The lamps burn low until her owl wakes; then every one flares.
- **Reveal:** the aisle crosses the owl roundel to the olive and the rostrum.
- **Signature:** the sacred olive over the rostrum, and the hall of lamps.

### Olympus_SeatOfHera (Olympias, Dragon)
- **Sentence:** a royal hall in plum and gold, where every column has Argos's eyes and the queen sits
  under a peacock's fan.
- **Land:** inside (`gTileset_SeatHera`). A checker of plum marble with gold studs, a purple runner
  with peacock eyes, columns painted with peacock feathers, torches on bronze stands up the aisle,
  gold urns of pomegranates (her fruit), the gold throne under a great fanned tail on the wall.
- **Settlement logic:** Hera set the hundred eyes of Argos in the peacock's tail; she raised the Hydra
  and set Ladon on the golden apples, so bronze serpents coil either side of her throne.
- **Reveal:** Olympias rises and the torches catch pair by pair from the door to her feet.
- **Signature:** the peacock fan over the throne, and the feather columns.

### Olympus_Summit, the altar above the cloud
- **Sentence:** through a propylon onto the bare summit: the great altar of Zeus under an open sky, and
  beyond it the temple of the Twelve.
- **Land:** the summit plateau (`gTileset_Aegina`), burnt grass and rock, cloud all round below the
  map edge; a paved sacred way from the propylon to the altar, the temple facing east behind it.
- **Settlement logic:** the temple faces east and its altar stands outside in front of it, where the
  rites happen (STYLE.md §4.5). The Archon waits at the altar, not inside.
- **Reveal:** the propylon frames the altar and the temple whole as you step through.
- **Signature:** Zeus's altar with the bronze box on it, and the temple's pediment against the sky.

### Olympus_HallOfHeroes, the cella of the Twelve
- **Sentence:** the temple's inner room, where the names are kept.
- **Land:** inside. Cool white marble (`gTileset_Civic`), two rows of columns, the record stone at the
  far end.
- **Settlement logic:** a heroön: the people the age remembers are written on the wall, and you walk
  up the nave to be written too.
- **Reveal:** the record stone at the end of the nave.
- **Signature:** the record stone. (Emerald's `FLDEFF_HALL_OF_FAME_RECORD` draws Hoenn's monitors, so
  the stone's moment is a white flash and a chime instead.)

## How the maps are built

| Map | Builder | Tilesets | Size |
|---|---|---|---|
| Ascent_1F, 2F | `tools/ichor/maps/ascent.py` | aethos + Skiron | 48×40, 40×44 |
| Ascent_Icefall, IcefallDeep, CrystalVault, Glacier, 3F; Olympus_Summit | `tools/ichor/maps/ascent_snow.py` (with `ascent_glacier.py`, `ascent_summit.py`, `ascent_peak.py`) | aethos + Chion | 42×46, 34×28, 24×20, 44×58, 44×46, 28×26 |
| Olympus_* (the other six) | `tools/ichor/maps/olympus.py` | Hestia, Labyrinth, Aegina, Hermes, Demeter, Civic | 15×18 to 20×21 |

Each map has its own brief, finds and **Hooks for later** in `design/maps/<Map>.md` (2026-11-18).
After running a builder that rewrites a herm map (2F, 3F), run `tools/ichor/maps/town_herms.py`.

Both import `tools/ichor/maps/league_lib.py`: a plan of ground kinds, structures placed by catalog key
and part name, stepped Skiron banks, sea cliffs, woods and `massif()` (bare rock as one wall of
strata), the soft ground painted by shape, reachability checks and review renders (`--render DIR`:
the whole map at 2× and every 15×10 view at native size). Wild tables: `league_encounters.py`.
Parties: `league_trainers.py`. The four seats' scripts: `league_seats.py`.

Render passes are kept in `build/league/pass*/` (not committed). The critique, per map:

- **Ascent_1F.** Pass 1 had dead-straight banks, rectangles of grass and one-row strips of oak
  that read as hedges. Pass 2 stepped every bank by a row, cut the grass into organic masks and
  added the spring under the Muses' niches. Pass 3 freed the niches from a pine, broke the
  hedgerows with pine saplings and rocks, and filled the empty screens (the goatherd's fold on
  the torrent's far bank, an outcrop and a leaning pine at the bend). Pass 4/5 broke the long
  straight edges the style audit found.
- **Ascent_2F.** Pass 1 filled the bare rock with scattered boulders: polka dots, not a mountain.
  Pass 2 drew every rock mass as cliff strata (`massif()`), so the ledges cling to real faces.
  Pass 3 narrowed ledge 2, scattered scree, cut the cave-mouth variant down to a rare accent, and
  added a scree slope with a lip as the way back down.
- **Ascent_3F.** Pass 1: terraces and stairs read well; the grass blobs repeated. Pass 2 varied the
  meadows and added scree; pass 3 added cairns along every terrace edge and a lip shortcut.
- **The seats.** One pass each was enough for the composition; the Propylaia's healer moved to the
  healer walker (the bow animation needs it), Hypatia stepped off the gate's axis, and the Hall
  lost a mosaic that turned out to be the rod of Asclepius.
- **The summit.** The snow-capped crags (aethos's white-capped rock) ring the plateau; a dry-stone
  lip makes the precinct a terrace; boulders break its long edges.

## The parties

Levels from BALANCE.md's League row. Every boss has Mortal (−3 levels) and Spartan (spreads,
natures, smart AI) variants. Battle names are 10 characters at most (`TRAINER_NAME_LENGTH`), so
Themistokles fights as THEMISTOK.; his dialogue uses his full name.

Raised 2026-11-17 for always-on team-wide EXP (BALANCE.md's League row). Hero lists below;
Mortal is the same at −3 with no items, Spartan the same with 31 IVs and full spreads.

| Boss | Team |
|---|---|
| **Polydamas** (the gatekeeper, 3F) | Nemeleon 67 @Sitrus Berry, Taurivet 67 @Charcoal, Kaprodon 68 @Life Orb, Geogrip 68 @Leftovers, **Hoplektor 69** @Flame Orb (Guts) |
| **Brasidas** (Fighting) | Laolith 66 @Focus Sash, Hoplomex 66 @Life Orb, Geogrip 67 @Leftovers, Kourodin 67 @Shell Bell, Dorydrake 68 @Lum Berry (Moxie), **Hoplektor 69** @Flame Orb (Guts) |
| **Themistokles** (Water) | Dakrock 67 @Damp Rock (Drizzle), Narkeray 67 @Expert Belt, Galenyon 68 @Sharp Beak, Telkanvil 68 @Leftovers, Trybdis 69 @Rocky Helmet, **Hexylla 70** @Mystic Water |
| **Hypatia** (Psychic, Psychic Terrain) | Enigmaw 68 @Expert Belt, Mantipod 68 @Wise Glasses, Melisseer 69 @Sitrus Berry, Pithound 69 @Leftovers (Unaware), Amnoze 70 @Lum Berry, **Sophowl 71** @Twisted Spoon |
| **Olympias** (Dragon) | Pythoros 69 @Leftovers, Stachypter 69 @Miracle Seed, Persenyx 70 @Sitrus Berry, Kynoketos 70 @Dragon Fang, Melodrakon 71 @Rocky Helmet, **Lernathan 72** @Life Orb (Regenerator) |
| **Aristeides** (the Archon, Electric Terrain) | Lebetron 71 @Magnet, Krystolos 72 @Never-Melt Ice, Elektear 72 @Leftovers, Kerastorm 73 @Sitrus Berry, Sepivolt 73 @Expert Belt, **Aetarch 75** @Life Orb |

The Ascent's 23 trainers (59–67, `tools/ichor/maps/league_trainers.py`): the slopes' and ledges'
Titanborn, hoplites, augurs, acolytes and pilgrims (59–63, no items); the Icefall's Chione and
Arktos (the gut's pair) and Boreades, the Deep's Hesychios, the Vault's Argyros, the Glacier's
Niphon and Pholoe (the narrows' pair) and Nephele, and 3F's Sthenelos and Hippias, Gorgo, Melite
and Korinna (63–67, held items, smart AI, an Ice Pokémon on most teams).

## Flags, vars and trainers

- **Bank flags** 0x6C0–0x6D7 (`tools/ichor/claim_ranges.md`, the League's row):
  `FLAG_ICHOR_ACT3_COMPLETE` (set by the Act III builder at III-12; gates L-1 to L-3),
  `_LEAGUE_DECREE`, `_IAPETOS_TRIED`, `_SENTENCES_HEARD`, `_PANTHEON_ENTERED`,
  `_ARCHON_DEFEATED`, `_KNOT_UNTIED`, `_HIDE_ARCHON_SUMMIT`, `_EPILOGUE_DONE`,
  `_HIDE_DECREE_CROWD`, `_HIDE_TRIAL_STOA` (spare), seven item balls, `_GOT_ASCENT_LEFTOVERS`,
  five hidden items.
- **The seats** reuse Emerald's `FLAG_DEFEATED_ELITE_4_*` as `FLAG_ICHOR_BEAT_<MEMBER>` and
  `VAR_ELITE_4_STATE` (0–10: walked in / won, seat by seat; 8 the summit, 9 the Hall).
- **Trainers** 460–475; `TRAINERS_END_LEAGUE`.
- **Heal locations:** `HEAL_LOCATION_OLYMPUS_PROPYLAIA` (whiteouts in the Pantheon) and
  `HEAL_LOCATION_ELAIA_VILLAGE_PLAYERS_ROOM` (`GameClear`'s CONTINUE warp, for the epilogue).

## Placeholders and what later builders connect

- **The road there.** Astyra's muleteer (`Astyra_EventScript_Muleteer`, east road end) and the
  Ascent's (east road end of 1F) stand in for Route 29 → Thermopylai → Route 30 → Tempe. Tempe
  should connect to Ascent_1F's east edge (the rockfall at x 46–47, rows 23–29) and both muleteers go.
- **Act III.** `FLAG_ICHOR_ACT3_COMPLETE` is set by nothing yet. The Act III builder sets it after
  Elpis's line (III-12).
- **L-1** (Astyra): Kerykos reads the decree by the main road. **L-2** (the Stoa): the trial of
  Iapetos as a told scene; the ostraka's pile and Iapetos's walker are for Act III to stage.
  **L-3** (Akti): Ione gives the sentences. **L-4** (the olive shoot) and **L-5** (Delphoi) wait for
  their maps (the Akropolis has no stump event; Delphoi isn't built).
- **L-10.** The epilogue is a wake-up in the player's room and a told montage of §7.11. Staging it
  in place (Halia's line in the square, the footrace, Elpis at the third krater) is the
  post-game's first job.
- **Rematches.** After the first Hall of Heroes the seats can be run again (the same teams);
  BALANCE.md's post-game rematch levels and an empty-altar Archon rematch are post-game work.

## Art and music to make later

- **Tiles:** a snowfield ground and snow-capped cliff set (the snowline uses Skiron under falling
  snow); a cloud-sea for below the summit and the ledges (the ledges show the sea through fog);
  a monumental propylaia (3F uses the palaestra front); a temple of the Twelve façade (the summit
  uses Aphaia's); a record stone for the Hall. (The four seats have their own tilesets since
  2026-11-18: `tools/ichor/art/pantheon_build.py`.)
- **Objects:** Medon's Knot as an item icon with three looser frames and the gold thread (§6.15);
  the gold thread drifting south; the bronze box on the altar.
- **Portraits:** Brasidas, Themistokles, Hypatia, Olympias and Aristeides use Hoplite, Ichor
  Sailor, Augur, Acolyte F and Pilgrim. Walkers likewise (HOPLITE, SAILOR, AUGUR, PRIESTESS,
  ELDER_M).
- **Music:** the Ascent uses `MUS_VICTORY_ROAD`, the seats `MUS_ENCOUNTER_ELITE_FOUR` /
  `MUS_VS_ELITE_FOUR`, the Archon `MUS_ENCOUNTER_CHAMPION` / `MUS_VS_CHAMPION`; MUSIC.md's Archon
  theme (Mixolydian, kithara and drum, stopping on "Gods help you") is still to write.
- **Credits:** `CB2_StartIchorCredits` (src/intro.c) pans the intro's frieze back from Olympus to
  Elaia under the names. The Star Chart's Unwoven patch is placed in the Hall; showing it filling
  on screen at the end of the credits is still to do.
