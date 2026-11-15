# Phase 3 build plan: Act II

Owner: the world-act2 session (branch `claude/world-act2-0a92e7`). This is the working plan for building `design/phase3/SCRIPT.md` as playable content. SCRIPT.md says what happens; this file says who builds which file, with which ids, and what is stubbed until another session lands.

Read first, in this order: `CLAUDE.md`, `design/MAP_DESIGN.md`, this file, the SCRIPT.md beats and Part 2 rosters for your maps, `design/TERMS.md`, `design/MUSIC.md`, then the model for your kind of work (below). world-act1's `design/phase2/BUILD.md` (on `claude/world-act1-6d11b7`) is the sister plan for Act I; where this file is silent, follow it.

## Batches

| # | Batch | Beats | Status |
|---|---|---|---|
| 1 | **The Kithairon crossing and Thyrsa:** Route 6, Mt. Kithairon (Eleutherai and the pass), Route 7 and the Kronia grounds, Thyrsa City and its interiors, the theater and skene, the Temple of Dionysus | 26–34 | built 2026-11-14 (below: what's left) |
| 2 | The road west: Route 8, Lebadeia and Trophonios's cave, Route 9, Kirrha, the Gulf ferry, Aigion | 35–37 | in progress, with batch 1's polish pass alongside |
| 3 | Arkadia: Route 11, Styx Falls, Route 12, Arkadia and its interiors, the Cypress Wood, the Pool, the Temple of Artemis | 38–44 | in progress, alongside batch 2 |
| 4 | Back to the Isthmus and the road of the Mysteries: Route 13, Nemea, Route 14, the Act II changes to Emporion, Eleusa and Akti, Route 15 with Thria, Daphni, Route 16; Aigina's interior scripted onto world-act1's maps | 45–47 | |
| 5 | Astyra: the city and its interiors, the Kerameikos and the paupers' graves, the Akropolis, Phaleron, the salt well | 48–57 | |
| 6 | The voyage and Kaldera: the *Paralos*, Delos, Route 19, Paros, the caldera road, Kaldera and its interiors, the Temple of Hephaestus, the Telchines' forge, Nea Kameni; the empty house in Elaia | 58–67 | |
| 7 | The optional lands: Euboia; Routes 17–18 with Marathon, Halai and Sounion; the open Aegean | — | |

Each batch ends with a report to the director: the branch and commit, what's playable, the map renders, the test results and the ROM delta.

## The route standard (MAP_DESIGN §8), for every batch

From 2026-11-14 every batch report passes `python3 tools/ichor/map_audit.py <its maps>` (MAP_DESIGN §8, measured on Emerald; on main 96a88cd7fe, merged here). Act II is the **middle** band. Hard minimums:

| | Land route | Sea route | Town | Dungeon |
|---|---|---|---|---|
| Grass cells per screen (15×10) | 15 | – | tables if any grass | – |
| Forced grass between any two ends | 8 cells (two 4-deep bands, or three shallower) | – | – | – |
| Trainers | 0.6 per screen, at least 6 | 0.35 per screen, at least 5 | – | 3 (1 in a one-floor cave) |
| Item balls | 0.2 per screen, at least 3 | 2 | 1 | 2 per floor, visible and hidden |
| Hidden items | 3 | 2 | 2 | 2 |
| Species per land table | 5 | – | 5 | 4 |

Also hard: a sign within 15 cells of every connected end; land tables `_Morning` and `_Night` wherever there's grass; a surf table (3 species) and a fishing table (4) wherever 12 or more water cells can be reached; a rock-smash table wherever there's marble rubble; land levels spanning no more than 5. Warnings to look at: a set piece, empty dead ends, edges that walk into a wall across a seam, item balls on solid cells. A FAIL that's right for a map (a story set piece like the Pool, a ship's deck) is explained in the report.

**More trainers than SCRIPT.md names** are needed on most routes to reach 0.6 a screen. Add them as the script's own are written: a name that fits 10 characters (Greek, not on the Lazarus avoid-list, grep `design/` for collisions), an existing class, a party at BALANCE.md's levels for the map, lines in the CLAUDE.md voice. Append each to your staged `design/phase3/parties/<agent>.party` and its name to the end of `design/phase3/parties/ORDER.txt`, then run `python3 tools/ichor/act2/fold_parties.py design/phase3/parties/*.party`. Scripts use the names, so the ids may change when this session folds every branch together at integration (Act II's ids are 160–319, then 820–849).

**Placeholders aren't maps.** Every batch 2 and 3 map was registered with a copy of Route 1, Akti Town or one of Akti's rooms so warps compile from the start; the audit flags them as copies, and they count as built only when their agent's branch is merged.

## Batch 2: the road west, and batch 1's polish

Built on the merge of main's Hoenn cut and engine batches 2–4, so **use the engine directly; batch 1's stubs for these are gone from new work**:
- **Relics** (ENGINE_API §2): obstacles are objects running `EventScript_CutTree` (thorn thicket, the Sickle), `EventScript_RockSmash` (marble rubble, the Hammer), `EventScript_StrengthBoulder` (column drum, the Girdle), `EventScript_IchorCobweb`, `EventScript_IchorGreatBoulder`; give a relic with `giveitem(ITEM_GIRDLE_OF_HERAKLES)` and the like (the item sets its `FLAG_ICHOR_GOT_*`). Dark maps: `"requires_flash": true`, braziers with `EventScript_IchorBrazier` and lit zones.
- **Rites** (§3): `EventScript_IchorAltar_<God>`, `EventScript_IchorTempleAltar_<God>`, `EventScript_IchorDesecratedAltar` (after your own guard battle), `special(Ichor_AddFavor)`. Offerings are real items: `ITEM_OLIVE_OIL`, `ITEM_BARLEY_CAKE`, `ITEM_WINE`, `ITEM_FRANKINCENSE`, `ITEM_LAUREL_SPRIG`, `ITEM_BRONZE_VOTIVE`.
- **Herms** (§4): the great herm's bg event runs `EventScript_IchorGreatHerm`. Add its row to `src/data/ichor_herms.h` and its `HEAL_LOCATION_HERM_AETHOS_ROUTE_<N>` (the landing tile south of it) to `src/data/heal_locations.json`, both appended. Ids `HERM_AETHOS_ROUTE_6` … `_9` exist.
- **Still stubbed** (keep the tags): dig spots (`ICHOR_STUB_DIG`), knucklebones, the Aethos dex, Act II's music cues, new key items and TMs, the xenia rest's clock.
- **Engine ranges, given by the ichor-engine session** (ENGINE_API §1's "Index blocks given out", 2026-11-14):
  - Braziers, `FLAG_ICHOR_BRAZIERS_START` +0x20–0x2F: +0x20 Antiope's cave, +0x21 Trophonios B1F, +0x22 the oracle's chamber; the rest for batches 3–7.
  - Desecrated altars, indices 8–15 (in `VAR_0x8005` to `EventScript_IchorDesecratedAltar`): 8 Kithairon's shrine, 9 Route 9's altar.
  - Decoys, `FLAG_ICHOR_THEOXENIA_START` +0x20–0x27: +0x20 Eleutherai's old man, +0x21 Thyrsa's blind beggar, +0x22 Route 8's traveler, +0x23 Kirrha's beggar. (Batch 1's two decoys move here from the bank flags they used.)
  - Fixed digs, `FLAG_ICHOR_DIG_FIXED_START` +0x10–0x1B: +0x10 the Treasury of Minyas, +0x11 Gla (both Route 8), +0x12 Trophonios's great boulder, +0x13 Route 9's gully.
  - **Digs aren't built**, but their names are fixed (ENGINE_API §8), so script against them behind `ICHOR_STUB_DIG`: a fixed find is `setvar(VAR_0x8004, <index>)`, `setvar(VAR_0x8005, ITEM_…)`, `goto(EventScript_IchorDigFixed)`; a daily spot is `setvar(VAR_0x8004, <spot>)`, `setvar(VAR_0x8005, ICHOR_DIG_ACT_II)`, `goto(EventScript_IchorDigSpot)` (ask this session for daily spot indices). Hide a dig-spot object with the same flag as its find.

### Who builds what

| Agent | Builds | Files it owns |
|---|---|---|
| **kopais** | The `kopais` secondary (SCRIPT.md Part 10: marsh reeds as the grass, reed-bed edges, marsh and lake water, mudflats, the Minyan dike, the Treasury of Minyas, Gla); `MAP_ROUTE8_KOPAIS` (64×26): beat 35A, Part 2's roster, Alethea's notes, the herm | `tools/ichor/art/kopais_*.py`, `data/tilesets/secondary/kopais/`, `tools/ichor/maps/kopais.py`, the map's layout and `data/maps/Route8_Kopais/`, `design/phase3/TILES_kopais.md` |
| **parnassos** | The `parnassos` secondary (grey limestone, laurels, olives, planes, the crossroads, the treasury ruin, Lebadeia's springs and precinct); `MAP_LEBADEIA` (32×28: beat 35B, Saon and the grille, the springs of Lethe and Mnemosyne) and `MAP_ROUTE9_SCHISTE` (52×44: beat 36, the three roads, the lookout, the treasury ruin, the Sphinx's ledge, the altar, the herm) | `tools/ichor/art/parnassos_*.py`, `data/tilesets/secondary/parnassos/`, `tools/ichor/maps/parnassos.py`, those two maps, `design/phase3/TILES_parnassos.md` |
| **harbors** | A `kirrha` secondary for the two harbor towns (quays, boats, nets, the gulf, the towns' houses, their own crags and olives drawn to match Parnassos's look), and the ferry from the `trireme` deck pieces (copy world-act1's art if it's on main, else draw a small deck of your own); `MAP_KIRRHA` (36×30: beat 37A, Delphoi's temple guards at the closed north road), `MAP_GULF_FERRY_DECK` (20×12: beat 37B, scripted warps quay to quay) and `MAP_AIGION` (28×24: beat 37C) | `tools/ichor/art/kirrha_*.py`, `data/tilesets/secondary/kirrha/`, `tools/ichor/maps/harbors.py`, those three maps, `design/phase3/TILES_kirrha.md` |
| **trophonios** | Trophonios's cave: a `trophonios` secondary on `aethos` (start from batch 1's `gTileset_KithaironCave` art, plus Part 10's chalk handprints, the snake cleft, the black pool, the bread offerings); `MAP_TROPHONIOS_CAVE_B1F` and `_B2F` (Part 5's descent, dark, braziers; beat 35C, the reading) | `tools/ichor/art/trophonios_*.py`, `data/tilesets/secondary/trophonios/`, `tools/ichor/maps/trophonios.py`, the two floors, `design/phase3/TILES_trophonios.md` |
| **rooms2** | The nine interiors on `oikos` (Part 10's list of new pieces; new secondaries as the art needs, grouped by shared pieces as batch 1's rooms did): Lebadeia's pilgrims' hall (heals), Herkyna's and the mason's houses; Kirrha's pilgrims' inn (heals), Agora stall (the shop), the muleteer's (a trade: Melisseer) and the old sweeper's houses; Aigion's old Achaean's and goatherd's houses | `tools/ichor/art/westrooms_*.py`, their secondaries, `tools/ichor/maps/westrooms.py`, those nine maps, `design/phase3/ROOMS_west.md`, the heal locations `HEAL_LOCATION_LEBADEIA` and `HEAL_LOCATION_KIRRHA`, the trade entry |
| **sprites2** | Part 10's batch 2 sprites: the FOWLER class (portrait, male and female; walker), Saon and the priests, pilgrims in blankets, Agamedes, Panopeus, Delphoi's temple guards, Alethea seated on a rim, Alethea's notes (object); the named folk as palette swaps | as batch 1's sprites agent, with `tools/ichor/art/sprites_act2_b2*.py` and `design/phase3/SPRITES.md` |
| **polish-kithairon** | Batch 1's crossing, made to look its best: Mt. Kithairon's climb (cliff faces, ledges, a sense of height instead of flat pine blocks and grey slabs), the maenads' drums, Route 7's empty west meadow, and anything else a fresh critique finds. Then the crossing's engine swaps: the vines and drums to the relic obstacles, the herms (and their table rows), the shrine to `EventScript_IchorDesecratedAltar`, the Barley Cake and other offerings | the kithairon, kronia and kithairon-cave art and builders, and the five crossing maps |
| **polish-thyrsa** | Thyrsa's central plaza (a wide bare cobble field), Eudora's yard, Manto's and Polos's sparse rooms, Semele's smoke (the 2-frame animation, a callback in `src/tileset_anims.c`), and anything else a fresh critique finds. Then the engine swaps on every Thyrsa map: the Neistan drum to `EventScript_StrengthBoulder`, Silenos's Girdle as `giveitem`, the temple's altar to `EventScript_IchorTempleAltar_Dionysus` with the Hierophant's gift calls, the offerings (the Agora's wine counter sells `ITEM_WINE`), the rooms' rites | the thyrsa, thyrsa_rooms, homes and stone, temple and theater art and builders, Thyrsa's 14 maps and Eleutherai's three rooms |

**New walkers are named now** in `include/constants/ichor_gfx_stubs_act2.h`'s batch 2 block, each aliased to a stand-in until sprites2 draws it: `OBJ_EVENT_GFX_ICHOR_FOWLER`, `_FOWLER_F`, `_SAON`, `_TROPHONIAN_PRIEST`, `_PILGRIM_BLANKET`, `_AGAMEDES`, `_PANOPEUS`, `_TEMPLE_GUARD`, `_ALETHEA_RIM`, `_ALETHEA_NOTE`, `_HERKYNA`, `_XENODIKE`, `_THYIA`, `_TISAMENOS`, `_HELIKE`. Classes and pics: `Class: Fowler`, `Pic: Fowler M` / `Fowler F` (folded as Shepherd until they exist).

Parties are staged in `design/phase3/parties/{kopais,trophonios,parnassos,harbors}.party`; wild tables in `design/phase3/encounters/region_b1.json` (Route 8 and 9 land, the cave's one table for both floors, fishing and the Conch's water for Route 8, Kirrha, the ferry and Aigion).

### Maps

| Map (directory) | `MAPSEC` | Type | Size | Group | Owner |
|---|---|---|---|---|---|
| `MAP_ROUTE8_KOPAIS` (`Route8_Kopais`) | `MAPSEC_AETHOS_ROUTE_8` | route | 64×26 | TownsAndRoutes | kopais |
| `MAP_LEBADEIA` (`Lebadeia`) | `MAPSEC_LEBADEIA` | town | 32×28 | TownsAndRoutes | parnassos |
| `MAP_ROUTE9_SCHISTE` (`Route9_Schiste`) | `MAPSEC_AETHOS_ROUTE_9` | route | 52×44 | TownsAndRoutes | parnassos |
| `MAP_KIRRHA` (`Kirrha`) | `MAPSEC_KIRRHA` | town | 36×30 | TownsAndRoutes | harbors |
| `MAP_GULF_FERRY_DECK` (`GulfFerry_Deck`) | `MAPSEC_AETHOS_ROUTE_10` | ocean route | 20×12 | TownsAndRoutes | harbors |
| `MAP_AIGION` (`Aigion`) | `MAPSEC_AIGION` | town | 28×24 | TownsAndRoutes | harbors |
| `MAP_TROPHONIOS_CAVE_B1F`, `_B2F` | `MAPSEC_LEBADEIA` | underground, dark | Part 5's | IndoorLebadeia | trophonios |
| `MAP_LEBADEIA_PILGRIMS_HALL`, `_HERKYNA_HOUSE`, `_MASONS_HOUSE` | `MAPSEC_LEBADEIA` | indoor | each room's own | IndoorLebadeia | rooms2 |
| `MAP_KIRRHA_INN`, `_AGORA`, `_MULETEERS_HOUSE`, `_SWEEPERS_HOUSE` | `MAPSEC_KIRRHA` | indoor | | IndoorKirrha | rooms2 |
| `MAP_AIGION_ACHAEANS_HOUSE`, `_GOATHERDS_HOUSE` | `MAPSEC_AIGION` | indoor | | IndoorAigion | rooms2 |

### Seams and warps

| Seam | Columns or rows | Owner |
|---|---|---|
| Thyrsa's Neistan Gate → Route 8's east edge | Thyrsa's west edge is open only on rows 23–24. Route 8's road meets its east edge on rows *q*…*q*+1, the kopais agent's choice, recorded here; seam strips aethos-only (8 columns, Part 10). This session adds both connections at integration (Thyrsa's map.json is the polish-thyrsa agent's builder's). | kopais |
| Route 8's west edge ↔ Lebadeia's east edge | **fixed now**: both maps' roads on rows 12–13 (verges 11 and 14), offset 0 both ways; seam strips aethos-only (different secondaries) | kopais, parnassos |
| Lebadeia's west edge ↔ Route 9's east edge | the parnassos agent's choice (one tileset, no strip) | parnassos |
| Route 9's south edge ↔ Kirrha's north edge | **fixed now**: Route 9's road at columns 8–11 (verges 8 and 11), Kirrha's at 26–29; Route 9 `down` offset −18, Kirrha `up` offset +18; seam strips aethos-only | parnassos, harbors |
| Kirrha's north road to Delphoi (Route 28, Act III) | drawn closed, with Delphoi's temple guards (beat 37A); not a connection yet | harbors |
| Aigion's south edge → Route 11 (batch 3) | draw the road's first rows; record the columns here | harbors |

**Door warps, fixed now** (outdoor warp *N* → the interior's warp 0, which leads back):

| Outdoor map | Warp | Leads to |
|---|---|---|
| `MAP_LEBADEIA` | 0, 1, 2 | `_PILGRIMS_HALL`, `_HERKYNA_HOUSE`, `_MASONS_HOUSE` |
| `MAP_LEBADEIA` | 3 | `MAP_TROPHONIOS_CAVE_B1F` (the bronze grille; closed by script until `FLAG_ICHOR_TROPHONIOS_GRILLE_OPEN`) |
| `MAP_KIRRHA` | 0, 1, 2, 3 | `_INN`, `_AGORA`, `_MULETEERS_HOUSE`, `_SWEEPERS_HOUSE` |
| `MAP_AIGION` | 0, 1 | `_ACHAEANS_HOUSE`, `_GOATHERDS_HOUSE` |
| `MAP_TROPHONIOS_CAVE_B1F` | 1 | `MAP_TROPHONIOS_CAVE_B2F`'s warp 0 (the stair down) |

The oracle's way out (beat 35C, "the hole is the way out") is a scripted warp to Lebadeia, in front of warp 3.

### Ids

**Trainers** 188–201: kopais 188–192 (Gorgidas, Ismenias, Timoxena, Perses, Euphrosyne), trophonios 193–194 (Philomelos, Melampos), parnassos 195–199 (Koretas, Onomarchos, grunt Psephos, Phayllos, Lykoreus), harbors 200–201 (Kephisios, Lamprias). Two names were over 10 characters and are renamed in SCRIPT.md: Amphilochos is now **Melampos** and Kephisodoros **Kephisios**.

**Bank flags**: this session 0x160–0x16F (already claimed, use them: `FLAG_ICHOR_VISITED_LEBADEIA`, `_TROPHONIOS_GRILLE_OPEN`, `_TROPHONIOS_READING`, `_FOUND_HERKYNAS_GOOSE`, `_VISITED_KIRRHA`, `_PYLADES_FIG`, `_XENODIKE_CAME_DOWN`, `_BOARDED_GULF_FERRY`, `_GULF_CROSSED`, `_VISITED_AIGION`); kopais 0x170–0x17F; parnassos 0x180–0x197; harbors 0x198–0x1A7; trophonios 0x1A8–0x1AF; rooms2 0x1B0–0x1BF. The polish agents use what's left of batch 1's: kithairon 0x126 and 0x129–0x12F, thyrsa 0x13C–0x13F, rooms 0x14E–0x14F, temple 0x152–0x153, scenes 0x15E–0x15F. **The second bank is in** (main a5de99c630, merged here): Act II's bank flags also include **0x500–0x63F** (320), claimed the same way (`claim.py --range 0x5xx-0x5yy bankflag …`; a worktree needs `claude/world-act2-0a92e7` from 0b2f52a09a on to claim there). Sub-ranges: heights 0x500–0x51F, arkadia 0x520–0x53F, artemis 0x540–0x54F, rooms3 0x550–0x55F; batch 2's agents, if their first ranges run out: kopais 0x560–0x567, parnassos 0x568–0x577, harbors 0x578–0x57F, trophonios 0x580–0x587, rooms2 0x588–0x58F; polish-kithairon 0x590–0x597, polish-thyrsa 0x598–0x59F; this session 0x5A0–0x5AF; batches 4–7 0x5B0–0x63F (144).

**More trainer ids:** 820–849 are Act II's too (the shared reserve, `tools/ichor/claim_ranges.md`), so 160–319 and 820–849 hold the act's 182. **Wild tables:** `_Morning` (which day and evening fall back to) plus `_Night` passes the standard; a separate `_Day` table is welcome where it adds real variety (diurnal species, a sunny meadow).

**Hidden items** are placed now, on Act II's vanilla flags 0x300–0x37F (the Hoenn cut freed them; a hidden item's flag must be a vanilla flag, not a bank flag): `python3 tools/ichor/claim.py --range LO-HI flag FLAG_ICHOR_HIDDEN_<MAP>_<ITEM> "comment"`. Sub-ranges: polish-kithairon 0x300–0x30B, polish-thyrsa 0x30C–0x313, kopais 0x314–0x31B, parnassos 0x31C–0x327, harbors 0x328–0x32F, trophonios 0x330–0x333, rooms2 0x334–0x337; 0x338–0x37F for batches 3–7.

**The user's standard for every map** (2026-11-14, through the director): "We need all these maps created. All these routes created. Thoughtfully. Engaging. Well designed. To Pokémon standards, including plenty of grass and wild encounters etc. Items etc." Forced grass bands plus plenty of optional grass with a reason to enter; land tables on every route with grass, surf and fishing on water, a rock-smash table where there's rubble; visible items as lures and hidden items where curiosity leads; trainers as checkpoints; a set piece per route; signs at each end and at forks. A measured version is coming as MAP_DESIGN §8 and `tools/ichor/map_audit.py`; every batch report will pass it.

**Names to watch:** `FLAG_ICHOR_GOT_SOOTHE_BELL` is Act I's; Aigion's Soothe Bell needs its own name (`FLAG_ICHOR_GOT_SOOTHE_BELL_AIGION`). Part 8's `FLAG_ICHOR_GOT_GIRDLE` is the engine's `FLAG_ICHOR_GOT_GIRDLE_OF_HERAKLES`. `ITEM_PYLADES_FIG` doesn't exist: use `FLAG_ICHOR_PYLADES_FIG` and a message, tagged `ICHOR_STUB_KEY_ITEMS`.

**Tests:** each map agent writes a headless test of its beats, as batch 1's did; this session writes `tools/ichor/tests/act2_batch2.sh` (the audit and the walk, extended west to Aigion) and runs both batches' suites.

## Batch 3: Arkadia (beats 38–44)

Started alongside batch 2 at the director's request ("run as many parallel map agents as your batches allow"). Everything in Batch 2's opening list holds: use the engine directly, the user's map standard, hidden items on vanilla flags, the same scope and done-means.

### Who builds what

| Agent | Builds | Files it owns |
|---|---|---|
| **heights** | The `arkadia_heights` secondary (SCRIPT.md Part 10: the gorge, the fallen Doric temple and its drums, the switchback cliff road, ledges, white water; the Styx's black cliff and still black pool; Nonakris's houses; the cypress road and its meadows); `MAP_ROUTE11_KRATHIS_GORGE` (40×56, beat 38: the drums, the Girdle's main-path gate), `MAP_STYX_FALLS` (36×30, beat 39), `MAP_ROUTE12_CYPRESS_ROAD` (56×36, beat 40) and `MAP_ROUTE12_CAVE_OF_MAIA` (Hermes's birth cave: a cave set of your own, or borrow from `kithairon_cave`'s art) | `tools/ichor/art/heights_*.py`, `data/tilesets/secondary/arkadia_heights/` (and a cave set), `tools/ichor/maps/heights.py`, those four maps, `design/phase3/TILES_heights.md` |
| **arkadia** | The `arkadia` secondary (cypresses in four shapes, lamp-trees lit and unlit, timber-and-stone houses on terraces, the outside of every building, the Cypress Wood's deep shade, the Pool); `MAP_ARKADIA` (50×44, beat 41 and the town's roster), `MAP_ARKADIA_CYPRESS_WOOD` (36×30: beat 42, Kleon's new moon, word for word from STORY.md §7.2; beat 43, the storm-hound and the vixen) and `MAP_POOL_OF_MNEMOSYNE` (24×20) | `tools/ichor/art/arkadia_*.py`, `data/tilesets/secondary/arkadia/`, `tools/ichor/maps/arkadia.py`, those three maps, `design/phase3/TILES_arkadia.md` |
| **artemis** | The `temple_artemis` secondary (the night garden: laurel walls, hunters' arches, myrtle, moonlit ground, the three clearings); `MAP_ARKADIA_TEMPLE_OF_ARTEMIS`: beat 44, Part 5's Hunt for the Hind (19193–19291), the acolytes, Hierophant Kallisto and the Moon Laurel (`FLAG_BADGE05_GET`), `EventScript_IchorTempleAltar_Artemis` and the Hierophant's gift calls | `tools/ichor/art/temple_artemis*.py`, its secondary, `tools/ichor/maps/temple_artemis.py`, the temple map, `design/phase3/TILES_temple_artemis.md` |
| **rooms3** | Nine interiors on `oikos` (Part 10's list of new pieces): Styx Falls's inn (a rest point), Horkia's house (the oaths) and Kepheus's house; Arkadia's Asclepeion (heals, the Pithos), Agora (the shop), Nyktimos's hall (the empty place set), Klymene's house, Hippothoos's charcoal hut and Krotos's house; `HEAL_LOCATION_ARKADIA`; the in-game trade (Arkoby) | `tools/ichor/art/arkrooms_*.py`, their secondaries, `tools/ichor/maps/arkrooms.py`, those nine maps, `design/phase3/ROOMS_arkadia.md` |
| **sprites3** | Part 10's batch 3 sprites: HUNTRESS and CHARCOALER (portraits, walkers), Kallisto (portrait `Hierophant Kallisto`, walker), Kleon on a stump, his row of balls, the temple hounds, the golden hind, Phylonoe, the muleteer, the lamplighter; the named folk as palette swaps | as sprites2, with `tools/ichor/art/sprites_act2_b3*.py` |

### Maps, seams and doors

All 17 maps are registered. Outdoor maps are in `gMapGroup_TownsAndRoutes`; Arkadia's rooms and the temple in `gMapGroup_IndoorArkadia`; Styx Falls's rooms and the Cave of Maia in `gMapGroup_IndoorStyx`.

| Seam | Columns or rows | Owner |
|---|---|---|
| Aigion's south edge → Route 11's north edge | the harbors agent records Aigion's columns; the heights agent draws Route 11's road and records its columns; this session sets both offsets at integration. Seam rows aethos-only. **Route 11 (heights):** the road at columns 19–20 (verges 18, 21); rows 0–5 aethos-only meadow, open along row 0 except trees at 0–1, 8–9, 28–29, 36–37. Align Aigion's road over 19–20; no `up` connection on Route 11 yet. | harbors, heights |
| Route 11 ↔ Styx Falls ↔ Route 12 | the heights agent's: three secondaries sharing a core (`TILES_heights.md`); Route 11 `down` offset 0 to Styx Falls through the cleft at 12–13 (core-only rows 50–55 and 0–5); Styx Falls `right` offset 0 to Route 12 on rows 22–23 (core-only columns 28–35 and 0–7) | heights |
| Route 12's south edge ↔ Arkadia's north edge | **fixed:** Route 12's road at columns 28–31 (verges 28, 31), Arkadia's at 22–25; Route 12 `down` offset +6, Arkadia `up` offset −6; seam rows aethos-only | heights, arkadia |
| Arkadia ↔ the Cypress Wood ↔ the Pool | the arkadia agent's | arkadia |
| Arkadia's east edge → Route 13 (batch 4) | the huntresses' cordon until `FLAG_BADGE05_GET`; record the rows | arkadia |
| Arkadia's west edge → Route 32, the Sacred Way (post-game) | **fixed with the world-postgame session:** road on rows 36–37 (verges 35, 38), 8 aethos-only columns; closed by a barrier or guard hidden by **`FLAG_ICHOR_POSTGAME`** (world-postgame's bank flag, set as the last line of Act III's epilogue; not `FLAG_SYS_GAME_CLEAR`, which the Hall of Fame sets before the epilogue). Until that flag is on main, `flags.h` ends with an `#ifndef FLAG_ICHOR_POSTGAME` alias to `FLAG_SYS_GAME_CLEAR`, and the arkadia agent's `FLAG_SYS_GAME_CLEAR` is swapped for it at integration; no connection on our side, the director joins it when the branches meet. The Cypress Wood's west-edge seam stays clear of rows 32–40. | arkadia |
| Arkadia's south road (Route 27, Act III) | drawn, closed | arkadia |

**Door warps, fixed:** `MAP_ARKADIA` warps 0–6: Asclepeion, Agora, Nyktimos's hall, Klymene's house, the charcoal hut, Krotos's house, the Temple of Artemis. `MAP_STYX_FALLS` warps 0–2: the inn, Horkia's house, Kepheus's house. `MAP_ROUTE12_CYPRESS_ROAD` warp 0: the Cave of Maia. Each interior's warp 0 (and 1) leads back.

### Ids

**Trainers** 202–216: heights 202–210 (Apheidas, Auge, Echemos, Azan; Aipytos, Laodike, Telphousa, Kypselos, grunt Basanos), arkadia 211–212 (Euadne, Agapenor), artemis 213–216 (Kyrene, Anthia, Prokris, Kallisto). Classes `Huntress`, `Charcoaler`; pic `Hierophant Kallisto`.

**Bank flags** (the last of 0x100–0x1FF until the second bank lands): this session 0x1FA–0x1FE, already claimed: `FLAG_ICHOR_VISITED_STYX_FALLS`, `_VISITED_ARKADIA`, `_KLEON_JOINED_TITANS`, `_ALETHEA_GOT_SKYLAPS`, `_HUNT_DONE`. heights 0x1C0–0x1D1, arkadia 0x1D2–0x1E3, artemis 0x1E4–0x1EB, rooms3 0x1EC–0x1F9. **Item balls and hidden items** take vanilla flags this batch, to save the bank: heights 0x338–0x34B, arkadia 0x34C–0x359, artemis 0x35A–0x35D, rooms3 0x35E–0x363 (`claim.py --range … flag`). If a range runs out, name the flag in your doc, stub its use, and say so.

**Engine indices:** decoys `FLAG_ICHOR_THEOXENIA_START` +0x24 (Route 11), +0x25 (Arkadia); desecrated altar index 10 (Route 12); herms `HERM_AETHOS_ROUTE_11` and `_12` (rows and heal locations appended by their builders); prophecy tablet 5 at `FLAG_ICHOR_PROPHECY_START` +4, read at +12; Daedalus's page IV at `FLAG_ICHOR_PAGES_START` +3; Artemis's gift I by `FLAG_ICHOR_GIFT(god, ICHOR_GIFT_I)` through the engine's Hierophant calls.

**Walkers named now** (aliased in `ichor_gfx_stubs_act2.h`'s batch 3 block): `OBJ_EVENT_GFX_ICHOR_HUNTRESS`, `_CHARCOALER`, `_KALLISTO`, `_KLEON_STUMP`, `_KLEON_BALLS`, `_TEMPLE_HOUND`, `_GOLDEN_HIND`, `_PHYLONOE`, `_LAMPLIGHTER`. `_MULETEER` is already real (batch 2's sprites2 drew Kirrha's, with a staff); Route 11's goad-carrying muleteer uses it, or a new `_MULETEER_GOAD` if sprites3 draws one. Iapetos in the Titan mask is batch 1's `_CHORUS_LEADER`; Alethea kneeling is `_ALETHEA_KNEEL`.

Parties: `design/phase3/parties/{heights,arkadia,artemis}.party`. Wild tables: `design/phase3/encounters/region_b2.json`, folded (Routes 11–12, the Wood and the Pool, morning and night; fishing for Route 11's pool and the temple's waterfall pool). Styx Falls has no wild battles and its black pool no table.

## Handovers waiting for later batches

**Batch 4, Aigina's interior** (from world-act1, 2026-11-14; maps on `claude/world-act1-6d11b7` at 1090709095, seams and spots in `design/phase2/BUILD.md`, the island stitched in `design/phase2/img/aigina_island.png`). `MAP_AEGINA_APHAIA_ROAD`, `MAP_AEGINA_TEMPLE_OF_APHAIA` and `MAP_AEGINA_MOUNT_OROS` are connected to the town and each other. The town's north gate opens on `FLAG_ICHOR_FERRY_TO_AEGINA`. Placeholders for us to replace, each with a script tagged `ICHOR_ACT2`:

| Who | Where | Notes |
|---|---|---|
| Myrmex | road (13,14), facing west | trainer, sight 3, mandatory sight line proven by world-act1's builder |
| Sostratos | road (20,6), facing east | trainer, sight 3 |
| Euthymia | road (26,3), facing east | trainer, sight 3 |
| The priestess | temple (11,9) | |

Set the three to `TRAINER_TYPE_NORMAL` once their `trainerbattle` scripts exist (the game reads the id from the script). Stubs already on their maps: the herm at road (22,3), landing (22,4), sets `FLAG_ICHOR_HERM_AEGINA` behind `ICHOR_STUB_HERM` (the engine still has to give Aigina's herm an id); altars behind `ICHOR_STUB_RITES`, Zeus on Oros (6,4) and Artemis at the temple (15,11); a dig spot at temple (18,11). The encounter tables are still Phase 2's levels 12–16: re-level them to BALANCE.md's Astyra row.

**Batch 6, Route 34 (post-game) → Kaldera's old port** (the world-postgame session, 2026-11-14): proposed and provisional, Route 34 joins `MAP_KALDERA_CALDERA_ROAD`'s east edge as open water on rows 46–51 beside the old port, with an 8-column aethos-only strip, closed until the post-game (whirlpools or a gate, the post-game session's choice). Tell that session (`local_aa883887-f146-4c32-aaad-5501bc2f5fec`) before moving it. Its post-game scenes on Act II maps (Thyrsa's vineyards and theater, Astyra's watchtower and Asclepeion) live in `design/postgame/PLACEMENTS.md`; keep any tiles it asks for free.

**Batch 7, Route 20 (the north Aegean) → the Hellespont** (agreed with the Oikoumene session, `local_6299f81d-90ba-46ac-8818-db27daa8abee`, 2026-11-14; its `MAP_HELLESPONT` is on `claude/world-oikoumene-950021`). Route 20 (about 40×88, north from Marathon, Samothrake at the top) meets the Hellespont on **Route 20's east edge, rows 8–21 open sea, offset 0** (Route 20 `right` to `MAP_HELLESPONT`; the Hellespont `left` to Route 20); every other row of that edge is shore or cliff; the 8 columns nearest the seam are aethos-only on both sides. Route 20 is open in Act II, so our side keeps the strait mouth blocked (a fog bank, or a sailor or Nausikles: "Not past Samothrake. Not yet.") until world-postgame's `FLAG_ICHOR_POSTGAME`. Neither side adds the connection until both maps exist; the director joins them.

**Batch 4, Demeter at the Maiden's Well (beat 46B).** Her disguise is **Cami**, a young woman (the user's request, SYSTEMS.md §10 on main at f6a581736e); SCRIPT.md 46B is updated to match. Her sprites are on main (af0925a436) and merged here: `OBJ_EVENT_GFX_ICHOR_CAMI` and `OBJ_EVENT_GFX_ICHOR_DEMETER`, on the new palette tag `OBJ_EVENT_PAL_TAG_ICHOR_THEOXENIA` (one more OBJ palette slot on Eleusa's map). Place Cami with `MOVEMENT_TYPE_FACE_UP` on the seat stone just south of the Kallichoron well: her north frames are the seated pose, so no `faceplayer` while she sits. At the reveal, `applymovement(… nurse_joy_bow)` plus `waitmovement` plays her rise (`ANIM_ICHOR_RISE`, 56 frames, ending facing down); then swap her for Demeter. `graphics/trainers/front_pics/cami.png` exists but isn't wired to anything. `tools/ichor/tests/theoxenia_sprites.sh` covers the animations. Check the seat stone's place against world-act1's Eleusa layout when batch 4 starts. Eleusa's sign ("An old woman sat on that bench, they say") is world-act1's and stays as written.

## Batch 1

### Result (2026-11-14)

All six agents' branches are merged (`act2-b1-sprites`, `-thyrsa`, `-temple`, `-rooms`, `-kithairon`, `-scenes`). Main's Hoenn cut and engine batches 2–4 are merged on top (2026-11-14): the real relic flags replace this session's Sickle and Girdle stand-ins, and with the cut the ROM is 22,477,208 B (67.0%); every batch 1 test still passes. `tools/ichor/tests/act2_batch1.sh --all` passes: the audit, the walk across every seam and door, and the agents' own tests (Kithairon 18 checks, Thyrsa City, the Three-Act Play 58 checks, the thirteen rooms, the Dionysia 32 checks). The ROM went from 25,544,940 B to 25,833,680 B (+282 KB, now 77.0%).

**Known failure (2026-11-14), not ours:** after merging main a5de99c630, the batch walk (`act2_batch1.sh`) stops at Thyrsa's theater gate. Main's carried-flame engine (b061bfd18a) keeps its state in `VAR_TEMP_2` and `VAR_TEMP_3` and burns `VAR_TEMP_2` down each step whenever both are nonzero; Thyrsa City's ON_TRANSITION sets both to 1 (the keeper's gate, Manto's crows), so the keeper's trigger fires. Fixed by the ichor-engine session in f3d3e16cf7 (the flame lives in engine memory; scripts read it with `Ichor_GetFlameKind` and `Ichor_GetFlameSteps`), on `claude/ichor-engine-systems-5a55eb`; the walk passes again once the director merges it to main and this branch merges main. Act II maps keep their temp vars.

Deviations the integrator accepted: the rooms' art takes three secondaries (`ThyrsaRooms`, `ThyrsaHomes`, `ThyrsaStone`) and the crossing's three (`Kithairon`, `Kronia`, `KithaironCave`), each because one set's 504 tiles couldn't hold it; the mask in the Three-Act Play is shown by the rack's empty peg, not on the player.

**Left for a polish pass** (the user's first priority is how maps look): Mt. Kithairon reads flat (pine blocks and grey rock slabs; it wants cliff faces and climb); the maenads' drums read as pale stones; Route 7's west meadow is open and empty; Thyrsa's central plaza is a wide bare cobble field; Eudora's yard is two plain walls and a tree; Manto's and Polos's rooms are sparse; Semele's smoke doesn't animate.

**Left until other work lands:** Eleusa ↔ Route 6's connection (offset 0 both ways) once Eleusa is on the same branch; hidden items (listed per map above) once the Hoenn cut is on main; the stubs by tag (`grep -rn ICHOR_STUB_`); battle backgrounds, item icons, the Mask Laurel icon and the map-name steles (Part 10); heal locations and herm landings for the fly menu (Route 6 (34,8), Route 7 (24,16)).

### Who builds what

Every agent touches only its own files. Shared registration files (`data/layouts/layouts.json`, `data/maps/map_groups.json`, `src/data/tilesets/*`, `include/constants/event_objects.h` and the sprite tables) take small appended entries; this session resolves conflicts in them.

| Agent | Builds | Files it owns |
|---|---|---|
| **kithairon** | The `kithairon` secondary (one set for all four maps of the crossing, so their shared seams need no aethos-only strip); Route 6, Eleutherai, Mt. Kithairon, Route 7 with the Kronia grounds: layouts, events, `scripts.pory` (beats 26–29 and the rosters) | `tools/ichor/art/kithairon_*.py`, `data/tilesets/secondary/kithairon/`, `tools/ichor/maps/kithairon.py`, the four maps' layouts and `data/maps/<Map>/`, `design/phase3/TILES_kithairon.md` |
| **thyrsa** | The `thyrsa` secondary (the city, its gates, its vineyards and the Kadmeia, and the theater's outer gate in the city wall); Thyrsa City (beat 30 and the roster), with a door warp into the theater | `tools/ichor/art/thyrsa_*.py`, `data/tilesets/secondary/thyrsa/`, `tools/ichor/maps/thyrsa.py`, `MAP_THYRSA_CITY`'s layout and `data/maps/ThyrsaCity/`, `design/phase3/TILES_thyrsa.md` |
| **rooms** | The `thyrsa_rooms` secondary on the `oikos` primary; every Thyrsa and Eleutherai interior except the temple and the theater: the Asclepeion, the Agora, the Kantharos, the xenia host, the seven households, Eleutherai's watch-house and homes | `tools/ichor/art/thyrsa_rooms_*.py`, `data/tilesets/secondary/thyrsa_rooms/`, `tools/ichor/maps/thyrsa_rooms.py`, those maps' layouts and `data/maps/<Map>/`, `design/phase3/ROOMS_thyrsa.md` |
| **temple** | The `temple_dionysus` secondary on the `oikos` primary; the Temple of Dionysus and the Three-Act Play (SCRIPT.md Part 5, beat 31); Thespis | `tools/ichor/art/temple_dionysus*.py`, `data/tilesets/secondary/temple_dionysus/`, `tools/ichor/maps/temple_dionysus.py`, `MAP_THYRSA_CITY_TEMPLE_OF_DIONYSUS`, `design/phase3/TILES_temple_dionysus.md` |
| **scenes** | The `theater` secondary (the cavea and its seated crowd, the orchestra, the skene's front and doors, the god-machine; backstage, the mask racks and the prop room for the skene, on `oikos`); the theater and the skene maps; the Dionysia (beat 32) with the trance effect, Kleon's third battle (beat 33), Silenos's contest (beat 34) | `tools/ichor/art/theater_*.py`, `data/tilesets/secondary/theater/` (and a `skene` secondary if the backstage rooms need their own), `tools/ichor/maps/theater.py`, `MAP_THYRSA_THEATER` and `MAP_THYRSA_THEATER_SKENE` whole, `src/ichor_act2_scene.c` and its header (the trance palette pulse and anything else these scenes need), `data/scripts/ichor_act2.pory` (shared Act II scene scripts), `design/phase3/TILES_theater.md` |
| **sprites** | Trainer portraits and overworld walkers for batch 1's new people and classes | new files under `graphics/trainers/` and `graphics/object_events/pics/`, their tables, `tools/ichor/art/sprites_act2*.py`, `design/phase3/SPRITES.md` |
| **this session** | This file, flag claims, the stub headers, trainer ids and parties, the wild encounter tables, the batch tests, integration | `design/phase3/BUILD.md`, `include/constants/flags.h` claims, `include/constants/ichor_species_stubs_act2.h`, `include/constants/opponents.h` (the world-act2 block), `src/data/trainers.party` (the world-act2 section), `src/data/wild_encounters.json`, `tools/ichor/tests/act2_*` |

**Parties and encounters are staged, then merged by this session**, so no two agents edit the same file: each agent writes its trainers' parties in `design/phase3/parties/<agent>.party` (the `.party` syntax, SCRIPT.md Part 3's blocks with the id names) and its encounter tables in `design/phase3/encounters/<agent>.json` (the `wild_encounters.json` entry for each map). This session folds them in and builds.

### Models

| Kind of work | Model to follow |
|---|---|
| An outdoor secondary tileset | `tools/ichor/art/eleusa_*.py` and `design/phase2/TILES_eleusa.md` (soft ground, borrowed ground, the catalog), and `emporion_*.py` for a city |
| A route or town builder | `tools/ichor/maps/route1.py` (ASCII grids, auto-tiling, review renders), `akti.py` |
| Interiors | `tools/ichor/art/oikia_*.py`, `civic_*.py`, `design/phase1/ROOMS_oikia.md`, `ROOMS_civic.md`; `tools/ichor/maps/akti_homes.py` |
| A temple trial | `tools/ichor/art/temple_demeter_*.py`, `temple_hermes*.py`; the slice's Hearth Trial (`data/maps/AktiTown_TempleOfHestia/scripts.pory`) |
| Sprites | `tools/ichor/art/sprites_*.py`, `design/phase1/SPRITES_classes.md`, `SPRITES_npc.md` |
| A headless test | `tools/ichor/tests/route1.sh`, `temple_trial.sh`, `slice_lib.lua` |

### Maps

This session has registered every batch 1 map with `tools/ichor/new_map.py`, so warps between agents' maps compile from the start. Each has a placeholder layout (a copy of an Act I layout, on stand-in tilesets) and stand-in music. Replace the layout, its tilesets and its size with your builder's output, and set the music when MUSIC.md's cue exists (`ICHOR_STUB_MUSIC` until then). Keep the map names, ids and groups.

| Map (directory) | `MAPSEC` | Tilesets | Type | Size (SCRIPT.md) | Group | Owner |
|---|---|---|---|---|---|---|
| `MAP_ROUTE6_ELEUTHERAI_ROAD` (`Route6_EleutheraiRoad`) | `MAPSEC_AETHOS_ROUTE_6` | aethos + kithairon | route | 56×28 | TownsAndRoutes | kithairon |
| `MAP_ROUTE6_ANTIOPES_CAVE` (`Route6_AntiopesCave`) | `MAPSEC_AETHOS_ROUTE_6` | aethos + kithairon_cave | underground (dark) | 16×12 | IndoorKithairon | kithairon |
| `MAP_ELEUTHERAI` (`Eleutherai`) | `MAPSEC_MT_KITHAIRON` | aethos + kithairon | town-like waypoint | 32×26 | TownsAndRoutes | kithairon |
| `MAP_MT_KITHAIRON` (`MtKithairon`) | `MAPSEC_MT_KITHAIRON` | aethos + kithairon | route | 40×56 | TownsAndRoutes | kithairon |
| `MAP_ROUTE7_KRONIA_GROUNDS` (`Route7_KroniaGrounds`) | `MAPSEC_AETHOS_ROUTE_7` | aethos + kronia (its core is kithairon's, at the same ids) | route | 44×40 | TownsAndRoutes | kithairon |
| `MAP_THYRSA_CITY` (`ThyrsaCity`) | `MAPSEC_THYRSA_CITY` | aethos + thyrsa | city | 56×48 | TownsAndRoutes | thyrsa |
| `MAP_THYRSA_THEATER` (`ThyrsaTheater`) | `MAPSEC_THYRSA_CITY` | aethos + theater | outdoor set piece | 40×34 | TownsAndRoutes | scenes |
| `MAP_THYRSA_THEATER_SKENE` (`ThyrsaTheater_Skene`) | `MAPSEC_THYRSA_CITY` | oikos + theater (or skene) | indoor | backstage and the prop room | IndoorThyrsa | scenes |
| `MAP_ELEUTHERAI_WATCH_HOUSE`, `_LYSIDIKE_HOUSE`, `_OINOE_HOUSE` | `MAPSEC_MT_KITHAIRON` | oikos + thyrsa_rooms | indoor | each room's own | IndoorKithairon | rooms |
| `MAP_THYRSA_CITY_ASCLEPEION`, `_AGORA`, `_TAVERN`, `_MASK_WORKSHOP`, `_ACTOR_HOUSE`, `_EUDORA_HOUSE`, `_MANTO_HOUSE`, `_PINDAROS_HOUSE`, `_SOWN_HOUSE`, `_VINTNER_HOUSE` | `MAPSEC_THYRSA_CITY` | oikos + thyrsa_rooms | indoor | each room's own | IndoorThyrsa | rooms |
| `MAP_THYRSA_CITY_TEMPLE_OF_DIONYSUS` (`ThyrsaCity_TempleOfDionysus`) | `MAPSEC_THYRSA_CITY` | oikos + temple_dionysus | indoor | the trial's | IndoorThyrsa | temple |

### Seams and warps

| Seam | Columns or rows | Agreed with |
|---|---|---|
| Eleusa's north edge → Route 6's south edge | `MAP_ELEUSA_VILLAGE` (50×40, aethos + eleusa, world-act1's commit 0284b88d32) is open at y = 0 in columns 44–47: the road is 45–46, grass verges at 44 and 47. Eleusa's six rows nearest the seam are aethos-only and have no vines; the vines are on Route 6, just past the seam. Route 6's road meets its south edge in the kithairon agent's choice of four columns *r*…*r*+3 (verge, road, road, verge), with Route 6's own seam rows aethos-only. Offsets follow from *r*: Eleusa `up` to Route 6 with offset 44 − *r*; Route 6 `down` to Eleusa with offset *r* − 44. This session adds both connections at integration, once Eleusa and Route 6 are on one branch. | world-act1 (columns), kithairon (*r*) |
| Eleusa → Route 6: *r* | **r = 44** (offset 0): Route 6's south edge has its grass verges at 44 and 47 and its road at 45–46, column for column with Eleusa. Route 6's rows 22–27 are aethos-only (path patch, grass, olives, stone pines, cypresses, the south stele); the vines are at row 21, the first non-seam row. Eleusa `up` offset 0, Route 6 `down` offset 0, both added at integration. | kithairon |
| Route 6 ↔ Eleutherai | Route 6's road leaves its north edge at 32–33 (verges 31, 34); Eleutherai's enters its south edge at 10–11 (verges 9, 12). Route 6 `up` to Eleutherai, offset 22; Eleutherai `down`, offset −22. Both on `gTileset_Kithairon`, so no seam strip. | kithairon |
| Eleutherai ↔ Mt. Kithairon | Eleutherai's road leaves its north edge at 10–11; Mt. Kithairon's enters its south edge at 18–19. Eleutherai `up`, offset −8; Mt. Kithairon `down`, offset 8. Both on `gTileset_Kithairon`. | kithairon |
| Mt. Kithairon ↔ Route 7 | Mt. Kithairon's road leaves its north edge at 20–21; Route 7's enters its south edge at 20–21. Offset 0 both ways. The maps are on different secondaries (`gTileset_Kithairon`, `gTileset_Kronia`) that share a core section at identical metatile ids (TILES_kithairon.md), so the six rows either side (Mt. Kithairon 0–5, Route 7 34–39) are core-or-aethos only, which `tools/ichor/maps/kithairon.py` enforces. | kithairon |
| Route 7's north edge → Thyrsa's Elektran Gate | Route 7's road leaves its north edge at columns 20–23; Thyrsa's Elektran Gate opens on its south edge at columns 26–29. The connection is `up` from Route 7 with offset −6 (Thyrsa's `down` with offset +6). Both rows at the seam are aethos-only. The kithairon and thyrsa agents may move it together, and record the change here. | kithairon, thyrsa |
| Thyrsa's west edge (the Neistan Gate) → Route 8 | batch 2. Thyrsa's west edge is open only at rows 23–24, where the Neistan road (aethos path) runs out through columns 0–7 (aethos-only) from the gate's one-cell passage at (8–9, 24). Every other row of the west edge is hillside (trees, rock). Route 8's east edge should open its road on two rows *q*, *q*+1; the connection is then `left` from Thyrsa with offset *q* − 23 (Route 8's `right` with offset 23 − *q*). Thyrsa adds no connection until Route 8 exists. The gate opens with the Girdle (`FLAG_ICHOR_NEISTAN_DRUM_MOVED`). | thyrsa (rows) |
| Eleusa's east edge → Route 15 | batch 4. Eleusa is open at x = 49 in rows 24–27; a wall runs down x = 48 with its gap at (48,25), where a hoplite stands in Act I. This session claimed his hide flag, `FLAG_ICHOR_HIDE_ELEUSA_EAST_HOPLITE` (bank 0x10C), and puts it on his object in batch 4, once Eleusa is on main | world-act1 |
| Thyrsa's east edge (the Proitid Gate) → Euboia | batch 7. The Proitid road runs out through columns 48–55 (aethos-only) on rows 30–31 from the gate's passage at (46–47, 31); the east edge is open only on those rows. For now its guard sits in the passage (`LOCALID_THYRSA_PROITID_GUARD`, (46,31)), so the gate is shut; batch 7 moves him aside (or gives him a hide flag) and adds the `right` connection with offset *q* − 30 for Euboia's road rows *q*, *q*+1. | thyrsa (rows) |

Record arrival tiles for scripted warps here as you choose them.

- **The Kithairon crossing** (kithairon). Doors: Route 6's warp 0 is Antiope's cave mouth at (52,7), reached from (52,8); the cave's warps 0 and 1 are its exit mat at (7,11) and (8,11), both to Route 6's warp 0. Eleutherai's warp 0 is the watch-house door in the fort's north wall at (23,3), reached from (23,4) in the court through the gate (23,8)–(23,9); warp 1 is Oinoe's door at (3,21); warp 2 is Lysidike's door at (21,19), inside the sheep pens, whose gate is at (22–24,23). Story triggers: Route 6's herald at (45,20) and (46,20) (`VAR_TEMP_1` 0); Mt. Kithairon's dancing floor at (24,38) and (25,38) (`VAR_TEMP_1` 0); Route 7's greeter at (20,16) and (21,16) (`VAR_TEMP_1` 0) and Kleon's tables across the road at row 12, columns 20–23 (`VAR_TEMP_2` 0). No scripted warps. **Hidden items**, not placed (vanilla flags): Route 6, the Wine in a forgotten jar by the broken wine-cart (27,6); Eleutherai, the Bronze Obol in the spring trough (13,15) (the trough is a sign today); Mt. Kithairon, the Pretty Feather at Aktaion's spring (38,17) and the Honey in Pentheus's fir (25,17); Route 7, the Bronze Obol in the reeds at the beach (35,16) and the Charcoal in the bread oven's ash (14,8).
- **Thyrsa City** (thyrsa): the gatekeeper's welcome fires on row 37, columns 26–29, just inside the Elektran Gate. The theater's high gate is warp 11 at (43,17), reached from (43,18); warp 12 at (28,7) is the temple's east door leaf and leads to the temple's warp 0 like warp 3. Every door is `MB_NON_ANIMATED_DOOR`. Thyrsa's **hidden items**, not placed (vanilla flags): the Cell Battery in Semele's chamber's ash (16,7), the Heart Scale in the fountain house of Dirke (22,34), the Rare Candy in the niche of the Kadmeia's bricked-up seventh gate (12,2).

**Door warp ids are fixed now**, so the outdoor and interior agents can wire both ends without waiting for each other. On an outdoor map, warp *N* is the door in this table. In every interior, warp 0 (and 1, for a two-tile doorway) is the way out, to the outdoor map's warp *N*. Add any further warps after these.

| Outdoor map | Warp | Leads to (its warp 0) |
|---|---|---|
| `MAP_ROUTE6_ELEUTHERAI_ROAD` | 0 | `MAP_ROUTE6_ANTIOPES_CAVE` |
| `MAP_ELEUTHERAI` | 0, 1, 2 | `MAP_ELEUTHERAI_WATCH_HOUSE`, `_OINOE_HOUSE`, `_LYSIDIKE_HOUSE` |
| `MAP_THYRSA_CITY` | 0, 1, 2, 3 | `MAP_THYRSA_CITY_ASCLEPEION`, `_AGORA`, `_TAVERN`, `_TEMPLE_OF_DIONYSUS` |
| `MAP_THYRSA_CITY` | 4, 5, 6, 7 | `_MASK_WORKSHOP`, `_ACTOR_HOUSE`, `_EUDORA_HOUSE`, `_MANTO_HOUSE` |
| `MAP_THYRSA_CITY` | 8, 9, 10 | `_PINDAROS_HOUSE`, `_SOWN_HOUSE`, `_VINTNER_HOUSE` |
| `MAP_THYRSA_CITY` | 11 | `MAP_THYRSA_THEATER` (the theater's outer gate in the city wall) |
| `MAP_THYRSA_THEATER` | 1 | `MAP_THYRSA_THEATER_SKENE` (the skene's back door) |

The theater's warp 0 is its gate back to the city's warp 11.

### New classes, pics and walkers

**Trainer names** fit `TRAINER_NAME_LENGTH`, 10 characters. Batch 1's three long ones are now Astylos (Route 6's runner, was Thersandros), Mynniskos and Thettalos (the temple's actors, were Kallippides and Nikostratos); SCRIPT.md is updated. Eight later trainers' names are too long too and get renamed in their batches.

**The sprites have landed** (merged from `act2-b1-sprites`; `design/phase3/SPRITES.md` is the catalog, `design/phase3/img/sprites_batch1.png` the contact sheet). Every name below is real. `include/constants/ichor_gfx_stubs_act2.h` is empty now and stays as the place for the next batch's not-yet-drawn names.

- **Classes:** `Maenad`, `Satyr`, `Actor`, `Vintner`. **Pics:** `Maenad`, `Satyr`, `Actor`, `Vintner`, `Hierophant Thespis` (Thespis stays `Class: Hierophant`), `Silenos` (`Class: Satyr`). `fold_parties.py` now folds them as written.
- **Walkers and objects** (`OBJ_EVENT_GFX_ICHOR_…`): `MAENAD`, `SATYR`, `ACTOR`, `VINTNER`, `THESPIS`, `SILENOS`, `MANTO`, `HERALD`, `KRONIST`, `CHORUS_LEADER`, `BEE_WOMAN`, `FATE_SPINNER`, `FATE_MEASURER`, `FATE_CUTTER`, `GOLD_MASK_KING`, `UNWOVEN_ACTOR`, `KLEON_SEATED`, `ALETHEA_KNEEL`, `WOODEN_IMAGE`, `MASK`, `CROWS`, and these extras:
  - `THESPIS_COMIC`: Thespis in the comic mask; his back frames match `THESPIS`, so swap while he faces away.
  - `KLEON_FEAST`: Kleon at the Kronia's bench, a loaf in each hand (bites when walking in place facing down). **Use this at the Kronia tables.** `KLEON_SEATED` is the theater pose: the stage's edge with his hat (beat 33) and the front row (beat 32).
  - `ALETHEA_SEATED`: her theater seat with the program. `ALETHEA_KNEEL` is the trowel.
  - `GOLD_MASK_KING_KNEEL`: the king on his knees.
  - `MAENAD_THYRSA`: the city maenad in wine-red (Lenaia).
  - `WOODEN_IMAGE_GARLAND`: Eleutherai's image after Oinoe's ivy garland is laid.
  - Thyrsa folk variants: `MOM_THYRSA` (Chthonia), `WOMAN_THYRSA` (Eudora), `YOUTH_F_THYRSA` (Erigone), `KID_M_THYRSA`, `MERCHANT_THYRSA` (Euthykles), `HARVESTER_THYRSA`; Staphylos is `VINTNER` and Polos is `ACTOR`.
- **There is no `setobjectgraphics` command in this tree.** To change a person's look in a scene (a mask, a pose), either keep two objects and swap their hide flags, or give the object a `OBJ_EVENT_GFX_VAR_n` graphics id, set `VAR_OBJ_GFX_ID_n`, and respawn it (`copyobjectxytoperm`, `removeobject`, `addobject`). SPRITES.md has the recipe.
- New palette tag `OBJ_EVENT_PAL_TAG_ICHOR_WINE` (0x1136) joins the folk and cast tags; a map shows at most those three.

### Ids

**Trainer ids** (`include/constants/opponents.h`, the world-act2 block, 160–319). This session defines them; agents write parties under these names.

| Ids | Agent | Trainers |
|---|---|---|
| 160–175 | kithairon | Route 6: Ikarios, Pythodoros, Botrys, Astylos. Eleutherai: Timolaos. Kithairon: Lykidas, Euia, Bromia, Arimnestos, grunt Ilys. Route 7: Komos, Hagnon; the Kronia: grunts Argillos, Keramos, Plinthos, Gypsos |
| 176–178 | thyrsa | Thyrsa City: Oinopion, Lenaia, Hegelochos |
| 179–182 | temple | Mynniskos, Thettalos, Theodoros; Thespis |
| 183–187 | scenes | Borboros (the actor); Kleon's three (`_3_KYNDER`, `_3_HIPLING`, `_3_NEBREL`); Silenos |

**Flags.** Claim only inside your sub-range, with `python3 tools/ichor/claim.py --range LO-HI bankflag FLAG_ICHOR_<NAME> "comment"`. Systems whose flags the engine reserves (herms, cleansed altars, prophecy tablets, Daedalus's pages, constellations, digs, rite gifts, theoxenia, xenia, relics) don't come from these ranges: use the engine's names (`design/ENGINE_API.md`) behind the stubs below.

| Agent | bankflag offsets | Count |
|---|---|---|
| this session (story, cross-map) | 0x100–0x10F | 16 |
| kithairon | 0x110–0x12F | 32 |
| thyrsa | 0x130–0x13F | 16 |
| rooms | 0x140–0x14F | 16 |
| temple | 0x150–0x153 | 4 |
| scenes | 0x154–0x15F | 12 |

**Bank vars** (`claim.py --range LO-HI bankvar VAR_ICHOR_<NAME> "comment"`): temple 6–7 (the Three-Act Play's state), scenes 8–9 (the Dionysia and the contest), this session 10–11.

Story flags this session has already claimed, for everyone to use: `FLAG_ICHOR_ACT2_BEGUN`, `_VISITED_ELEUTHERAI`, `_KRONIA_SEEN`, `_ARRIVED_THYRSA`, `_VISITED_THYRSA`, `_THREE_ACT_PLAY_DONE`, `_DIONYSIA_BEGUN`, `_DIONYSIA_DONE`, `_SAW_PROGRAM_HOOK`, `_KLEON_BATTLE_3_DONE` (all `FLAG_ICHOR_…`).

Daily flags (this session claims them): `FLAG_DAILY_ICHOR_KRONIST_BREAD`, `_SKENE_MASK`, `_TREADING`, from 0x4C. **Hidden items** need vanilla flags (0x1F4 or above). Act II's range is vanilla flags 0x300–0x37F, 110 of them free, from the Hoenn cut's batch 2 (commit aae327b35e on `claude/hoenn-cut-db6209`, not yet on main). Until it is on main, list each hidden item in your map's section of this file and don't place it; this session claims the flags (`claim.py --range 300-37F flag …`) and places them once the cut lands. Story state stays in the Ichor bank flags. Vars beyond the bank vars above need the director's OK. The cut removes every Hoenn and FRLG map: never use a Hoenn or FRLG `MAP_`, `LAYOUT_` or `HEAL_LOCATION_` name (warps, heal points, copied layouts), since after the cut they compile only as stubs.

Batch 1 alone wants about 80 bank flags, and Act II about 430 before item balls; the 256 in 0x100–0x1FF won't hold the act. The director has the ask.

### Stubs until other sessions land

Each stub is tagged in a comment, so it can be found with `grep -rn ICHOR_STUB_`. world-act1 uses the same tags for Act I.

- **`ICHOR_STUB_AETHOS_DEX`: species.** The Aethos dex isn't in the ROM. Write the Aethos names everywhere (`SPECIES_THYRSIVY`, `OBJ_EVENT_GFX_SPECIES(BOTRYKIT)`). `include/constants/ichor_species_stubs_act2.h` maps each Act II name to a vanilla stand-in of the same type, every one behind `#ifndef`, so world-act1's header (`ichor_species_stubs.h`, which covers Act I's species and is included first) defines the shared ones. Both headers sit inside `#ifndef ICHOR_AETHOS_DEX`, so the dex lands by defining that one macro. Write no `Ability:` lines in parties while the stand-ins are in place; note the ability in a comment for the dex.
- **`ICHOR_STUB_RELICS`: the Girdle and the obstacles.** The relics are engine batch 2. Use the engine's names: the item `ITEM_GIRDLE_OF_HERAKLES` and the flag `FLAG_ICHOR_GOT_GIRDLE_OF_HERAKLES`, behind `ICHOR_STUB_RELICS`. Until they exist, the Girdle is a story flag of this session's (`FLAG_ICHOR_ACT2_STUB_GIRDLE`, aliased), a column drum is an object whose script checks it and moves the drum by script, and the vines are a thicket object whose script checks `FLAG_ICHOR_GOT_DEMETERS_SICKLE` (world-act1's beat 23 sets it; `flags.h` aliases it to this session's `FLAG_ICHOR_ACT2_STUB_SICKLE` until the engine defines it), with the hide flag `FLAG_ICHOR_HIDE_ELEUTHERAI_VINES`, which the kithairon agent claims. Scripts check `FLAG_ICHOR_GOT_GIRDLE_OF_HERAKLES` the same way.
- **`ICHOR_STUB_RITES`, `ICHOR_STUB_HERM`, `ICHOR_STUB_DIG`.** Engine batches 3–4. An altar shows its SCRIPT.md text and says nothing about prayer mechanics; a desecrated altar's guard battles you and the cleansing line plays; a great herm offers to anoint and sets nothing; a fixed dig spot shows the turned-earth text. Each is its own small script with the tag in a comment, so it can be swapped for `EventScript_IchorAltar_<God>`, `EventScript_IchorGreatHerm` and the dig API when they land.
- **`ICHOR_STUB_OFFERINGS`.** Olive Oil, Wine, Barley Cake and the Bronze Votive are engine items. Until then, an offering given in a scene is skipped with the tag, and an offering item ball uses `ITEM_BERRY_JUICE`.
- **`ICHOR_STUB_MUSIC`.** Act II's new cues (SCRIPT.md Part 9) aren't composed yet. Use the nearest built cue and tag it: `MUS_ICHOR_ROAD` for Route 6, Kithairon and Route 7; `MUS_ICHOR_EMPORION` for Thyrsa; `MUS_ICHOR_TEMPLE_HERMES` for the Temple of Dionysus; the Titan theme for the tragedy; the rival battle for Kleon; the slice's gym battle for Thespis. Never use Elpis's lullaby (627, 628) in batch 1.
- **`ICHOR_STUB_KNUCKLEBONES`.** If the knucklebones script isn't on main when the scenes and rooms agents reach Silenos and the Kantharos, play each match as a scripted win or loss with the SCRIPT.md lines, behind the tag.
- **`ICHOR_STUB_SCENE_HOURS`.** world-act1's `Ichor_SetHoursOverride` isn't on main yet. The Dionysia holds dusk on its own map (the scenes agent draws the sky layer at dusk, SCRIPT.md beat 32), so batch 1 doesn't need it.

### Done means (per map)

- `make` is green and `tools/ichor/smoke_test.sh` passes.
- The map follows MAP_DESIGN.md: forced grass on routes, trainer checkpoints, every dead end pays, every house a home, every interior unique, seam strips from the primary only, signs at ends and forks.
- **At least three render-and-critique passes,** each written down in your TILES or ROOMS doc (what was wrong, what changed), and in-game screenshots of every scene, looked at.
- Every line of text measured with `tools/ichor/text_width.py`; the speaker's name in the name box, as in the slice.
- A 2x render in `design/phase3/img/<map>.png` for the director to forward to the user.

### Tests

This session writes `tools/ichor/tests/act2_batch1.sh` on `slice_lib.lua`: it starts a save with Act I's end flags set (`FLAG_ICHOR_ACT1_COMPLETE`, the three laurels, the Sickle), warps to Route 6's south edge and plays beats 26–34 headlessly: the vines, the Kronia, the trial, the Dionysia, Kleon and the Girdle, ending at Thyrsa's open west gate. The full-playthrough test (world-act1's) is extended through Act II once Act I's maps are on main.
