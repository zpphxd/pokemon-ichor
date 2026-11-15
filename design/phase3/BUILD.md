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

**Order, by the main story's critical path** (the director, 2026-11-14; the user: "I want to get to full 8 gyms + elite 4"): Thyrsa for Laurel 4 (batch 1, built) → Arkadia and the Temple of Artemis for Laurel 5 (batch 3, running) → **Astyra**, the midpoint (batch 5, next) → **Kaldera and the Temple of Hephaestus** for Laurel 6 (batch 6) → the routes connecting them (batch 4: Routes 13–16, Nemea, Daphni, the Act II changes to Emporion and Eleusa). The optional lands (batch 7: Euboia, Marathon, Sounion, Paros, the open Aegean; and Trophonios's cave, already under way in batch 2) come after a playable path through Laurel 6. Every map is built to §8 as it goes.

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
| Thyrsa's Neistan Gate → Route 8's east edge | Thyrsa's west edge is open only on rows 23–24. Route 8's road meets its east edge on rows *q*…*q*+1, the kopais agent's choice, recorded here; seam strips aethos-only (8 columns, Part 10). This session adds both connections at integration (Thyrsa's map.json is the polish-thyrsa agent's builder's). **q = 14** (kopais, 2026-11-14): Route 8's road reaches its east edge on rows 14–15, with grass verges on 13 and 16, and columns 56–63 are aethos only (Thyrsa's olive grove runs on into them: olives, cypresses, boulders, the road on aethos's limestone patch). Connections: Route 8 `right` to Thyrsa with offset −9 (in Route 8's map.json now); Thyrsa `left` to Route 8 with offset +9, to add at integration. The game reads a neighbor's row as this map's row minus the offset (as Route 7's `up` −6 to Thyrsa does), so the "*q* − 23 / 23 − *q*" in the batch 1 row below is the wrong way round; `map_audit.py`'s seam check agrees with these. | kopais |
| Route 8's west edge ↔ Lebadeia's east edge | **fixed now**: both maps' roads on rows 12–13 (verges 11 and 14), offset 0 both ways; seam strips aethos-only (different secondaries) | kopais, parnassos |
| Lebadeia's west edge ↔ Route 9's east edge | **chosen:** Lebadeia's road on rows 12-13 (verges 11, 14), Route 9's on rows 20-21 (verges 19, 22). Lebadeia `left` offset −8, Route 9 `right` offset +8. Both on `gTileset_Parnassos`, so no strip | parnassos |
| Route 9's south edge ↔ Kirrha's north edge | **fixed now**: Route 9's road at columns 8–11 (verges 8 and 11), Kirrha's at 26–29; Route 9 `down` offset −18, Kirrha `up` offset +18; seam strips aethos-only | parnassos, harbors |
| Kirrha's north road to Delphoi (Route 28, Act III) | drawn closed, with Delphoi's temple guards (beat 37A); not a connection yet | harbors |
| Aigion's south edge → Route 11 (batch 3) | **drawn**: Aigion's road leaves its south edge at columns 13–14, verges 12 and 15 (columns 12–15 walkable at row 23, nothing else). Its six southern rows (18–23) are aethos-only (path, olives, pines, cypresses, rocks, the stele at (16,19)). For Route 11's road at its north edge on columns *s*…*s*+3 (verge, road, road, verge): Aigion `down` offset *s* − 12, Route 11 `up` offset 12 − *s*. Alethea waits on the road at (14,22) (`FLAG_ICHOR_HIDE_ALETHEA_AIGION`: batch 3 sets it when she goes on with the player). | harbors |

**Door warps, fixed now** (outdoor warp *N* → the interior's warp 0, which leads back):

| Outdoor map | Warp | Leads to |
|---|---|---|
| `MAP_LEBADEIA` | 0, 1, 2 | `_PILGRIMS_HALL`, `_HERKYNA_HOUSE`, `_MASONS_HOUSE` |
| `MAP_LEBADEIA` | 3 | `MAP_TROPHONIOS_CAVE_B1F` (the bronze grille; closed by script until `FLAG_ICHOR_TROPHONIOS_GRILLE_OPEN`) |
| `MAP_KIRRHA` | 0, 1, 2, 3 | `_INN`, `_AGORA`, `_MULETEERS_HOUSE`, `_SWEEPERS_HOUSE` |
| `MAP_AIGION` | 0, 1 | `_ACHAEANS_HOUSE`, `_GOATHERDS_HOUSE` |
| `MAP_TROPHONIOS_CAVE_B1F` | 1 | `MAP_TROPHONIOS_CAVE_B2F`'s warp 0 (the stair down) |

The oracle's way out (beat 35C, "the hole is the way out") is a scripted warp to Lebadeia, in front of warp 3.

**The Gulf crossing, as built** (harbors, `tools/ichor/maps/harbors*.py`):
- Kirrha's doors: warp 0, the inn, at (23,9), its doorstep (23,10) on the road (the spot for `HEAL_LOCATION_KIRRHA`, rooms2's); warp 1, the Agora's shed, at (21,20) onto the quay (21,21); warp 2, the muleteer's, at (15,15), doorstep (15,16); warp 3, the old sweeper's, at (21,15), doorstep (21,16). Kirrha `up` to Route 9 with offset +18 is in its map.json.
- Aigion's doors: warp 0, the old Achaean's, at (8,8), doorstep (8,9); warp 1, the goatherd's, at (19,8), doorstep (19,9). `HEAL_LOCATION_AIGION` (added): Aigion (12,13), in front of the grove-keeper (12,12), who heals.
- The ferry is scripted warps only: Kirrha's quay (Panopeus at (23,23)) → the deck at (11,6); the deck → Aigion's quay at (17,4) (beat 37C the first time); Aigion's quay (Panopeus at (18,3)) → the deck, `FLAG_ICHOR_FERRY_TO_KIRRHA` set; the deck → Kirrha's quay at (22,23).
- Tilesets: three, not one. A single `kirrha` set for both towns came to some 610 tiles against the 504 the door animations leave, so Aigion has `gTileset_Aigion` and the deck `gTileset_GulfFerry`, all drawn by the same painters (`tools/ichor/art/kirrha_*.py`, catalog `design/phase3/TILES_kirrha.md`).

### Ids

**Trainers** 188–201: kopais 188–192 (Gorgidas, Ismenias, Timoxena, Perses, Euphrosyne), trophonios 193–194 (Philomelos, Melampos), parnassos 195–199 (Koretas, Onomarchos, grunt Psephos, Phayllos, Lykoreus), harbors 200–201 (Kephisios, Lamprias). Two names were over 10 characters and are renamed in SCRIPT.md: Amphilochos is now **Melampos** and Kephisodoros **Kephisios**.

**Bank flags**: this session 0x160–0x16F (already claimed, use them: `FLAG_ICHOR_VISITED_LEBADEIA`, `_TROPHONIOS_GRILLE_OPEN`, `_TROPHONIOS_READING`, `_FOUND_HERKYNAS_GOOSE`, `_VISITED_KIRRHA`, `_PYLADES_FIG`, `_XENODIKE_CAME_DOWN`, `_BOARDED_GULF_FERRY`, `_GULF_CROSSED`, `_VISITED_AIGION`); kopais 0x170–0x17F; parnassos 0x180–0x197; harbors 0x198–0x1A7; trophonios 0x1A8–0x1AF; rooms2 0x1B0–0x1BF. The polish agents use what's left of batch 1's: kithairon 0x126 and 0x129–0x12F, thyrsa 0x13C–0x13F, rooms 0x14E–0x14F, temple 0x152–0x153, scenes 0x15E–0x15F. **The second bank is in** (main a5de99c630, merged here): Act II's bank flags also include **0x500–0x63F** (320), claimed the same way (`claim.py --range 0x5xx-0x5yy bankflag …`; a worktree needs `claude/world-act2-0a92e7` from 0b2f52a09a on to claim there). Sub-ranges: heights 0x500–0x51F, arkadia 0x520–0x53F, artemis 0x540–0x54F, rooms3 0x550–0x55F; batch 2's agents, if their first ranges run out: kopais 0x560–0x567, parnassos 0x568–0x577, harbors 0x578–0x57F, trophonios 0x580–0x587, rooms2 0x588–0x58F; polish-kithairon 0x590–0x597, polish-thyrsa 0x598–0x59F; this session 0x5A0–0x5AF; batches 4–7 0x5B0–0x63F (144).

**More trainer ids:** 820–849 are Act II's too (the shared reserve, `tools/ichor/claim_ranges.md`), and **1344–1403** (60) from the block that opens when hoenn-cut raises the trainer limit to 1,536; use that block from batch 4 on, once the raise is on main. `fold_parties.py` runs through 160–319, then 820–849, then 1344–1403. **Wild tables:** `_Morning` (which day and evening fall back to) plus `_Night` passes the standard; a separate `_Day` table is welcome where it adds real variety (diurnal species, a sunny meadow).

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
| Arkadia ↔ the Cypress Wood ↔ the Pool | **fixed:** Arkadia → the Wood by a gate warp, not an edge: `MAP_ARKADIA` warp 7, the Wood's gate in the square's west wall (9,17), ↔ the Wood's warps 0–1, exit mats at (32,29) and (33,29) on its bottom edge. The Wood's west edge rows 13–15 ↔ the Pool's east edge rows 9–11: the Wood `left` offset +4, the Pool `right` offset −4; both maps are on `gTileset_ArkadiaWood`, so no seam strip. The Wood's west edge is closed on every other row (clear of rows 32–40). | arkadia |
| Arkadia's east edge → Route 13 (batch 4) | **fixed:** road on rows 23–24 (verges 22 and 25), columns 42–49 aethos-only. Two huntresses stand on the road at (43,23) and (43,24), hidden by `FLAG_BADGE05_GET`; boulders on the verges at (43,22) and (43,25) keep the cordon from being walked round. No connection yet; batch 4's Route 13 meets rows 23–24. | arkadia |
| Arkadia's west edge → Route 32, the Sacred Way (post-game) | **fixed with the world-postgame session:** road on rows 36–37 (verges 35, 38), 8 aethos-only columns; closed by a barrier or guard hidden by **`FLAG_ICHOR_POSTGAME`** (world-postgame's bank flag, set as the last line of Act III's epilogue; not `FLAG_SYS_GAME_CLEAR`, which the Hall of Fame sets before the epilogue). Until that flag is on main, `flags.h` ends with an `#ifndef FLAG_ICHOR_POSTGAME` alias to `FLAG_SYS_GAME_CLEAR`, and the arkadia agent uses `FLAG_ICHOR_POSTGAME` through that alias (two Elean guards at (5,36) and (5,37), verge stones at (5,35) and (5,38)); no connection on our side, the director joins it when the branches meet. The Cypress Wood's west-edge seam stays clear of rows 32–40. | arkadia |
| Arkadia's south road (Route 27, Act III) | drawn, closed: road at columns 13–14 (verges 12 and 15), rows 38–43 aethos-only. The Lakonian hoplite at (13,40) (no hide flag yet: Act III's builder gives him one) and a herm at (14,40); verge stones at (12,40) and (15,40). | arkadia |

**Door warps, fixed:** `MAP_ARKADIA` warps 0–6: Asclepeion, Agora, Nyktimos's hall, Klymene's house, the charcoal hut, Krotos's house, the Temple of Artemis. Warp 7 is the Cypress Wood's gate. `HEAL_LOCATION_ARKADIA`: (15,12), in front of the Asclepeion's door. `MAP_STYX_FALLS` warps 0–2: the inn, Horkia's house, Kepheus's house. `MAP_ROUTE12_CYPRESS_ROAD` warp 0: the Cave of Maia. Each interior's warp 0 (and 1) leads back.

### Ids

**Trainers** 202–216: heights 202–210 (Apheidas, Auge, Echemos, Azan; Aipytos, Laodike, Telphousa, Kypselos, grunt Basanos), arkadia 211–212 (Euadne, Agapenor), artemis 213–216 (Kyrene, Anthia, Prokris, Kallisto); after trophonios's Mnesarete (217), arkadia's four for the route standard 218–221 (Hekaerge, Mainalos, Lysippe, Melanippe; `ORDER.txt`). Classes `Huntress`, `Charcoaler`; pic `Hierophant Kallisto`.

**Bank flags** (the last of 0x100–0x1FF until the second bank lands): this session 0x1FA–0x1FE, already claimed: `FLAG_ICHOR_VISITED_STYX_FALLS`, `_VISITED_ARKADIA`, `_KLEON_JOINED_TITANS`, `_ALETHEA_GOT_SKYLAPS`, `_HUNT_DONE`. heights 0x1C0–0x1D1, arkadia 0x1D2–0x1E3, artemis 0x1E4–0x1EB, rooms3 0x1EC–0x1F9. **Item balls and hidden items** take vanilla flags this batch, to save the bank: heights 0x338–0x34B, arkadia 0x34C–0x359, artemis 0x35A–0x35D, rooms3 0x35E–0x363 (`claim.py --range … flag`). If a range runs out, name the flag in your doc, stub its use, and say so.

**Engine indices:** decoys `FLAG_ICHOR_THEOXENIA_START` +0x24 (Route 11), +0x25 (Arkadia); desecrated altar index 10 (Route 12); herms `HERM_AETHOS_ROUTE_11` and `_12` (rows and heal locations appended by their builders); prophecy tablet 5 at `FLAG_ICHOR_PROPHECY_START` +4, read at +12; Daedalus's page IV at `FLAG_ICHOR_PAGES_START` +3; Artemis's gift I by `FLAG_ICHOR_GIFT(god, ICHOR_GIFT_I)` through the engine's Hierophant calls.

**Walkers named now** (aliased in `ichor_gfx_stubs_act2.h`'s batch 3 block): `OBJ_EVENT_GFX_ICHOR_HUNTRESS`, `_CHARCOALER`, `_KALLISTO`, `_KLEON_STUMP`, `_KLEON_BALLS`, `_TEMPLE_HOUND`, `_GOLDEN_HIND`, `_PHYLONOE`, `_LAMPLIGHTER`. `_MULETEER` is already real (batch 2's sprites2 drew Kirrha's, with a staff); Route 11's goad-carrying muleteer uses it, or a new `_MULETEER_GOAD` if sprites3 draws one. Iapetos in the Titan mask is batch 1's `_CHORUS_LEADER`; Alethea kneeling is `_ALETHEA_KNEEL`.

Parties: `design/phase3/parties/{heights,arkadia,artemis}.party`. Wild tables: `design/phase3/encounters/region_b2.json`, folded (Routes 11–12, the Wood and the Pool, morning and night; fishing for Route 11's pool and the temple's waterfall pool). Styx Falls has no wild battles and its black pool no table.

## Batch 5: Astyra (beats 48–57)

The midpoint, and the next batch on the critical path (Arkadia → **Astyra** → Kaldera). It builds on main fe2234a4ac merged here: the real Aethos dex (`ICHOR_AETHOS_DEX` is defined, so species are real, follower sprites included) and hidden items on bank flags. Everything in Batch 2's opening list holds: use the engine directly, the route standard, every house a home, every interior unique, three render-and-critique passes, a 2x render per map in `design/phase3/img/`, and batch 1's done-means.

Six map agents and a sprites agent, each on its own branch (`act2-b5-<agent>`) in its own worktree, each pushing as it goes. Batch 2 ran seven. The raid and the salt well are each a dungeon-sized job, so they go to two agents; one agent holding both would be the batch's long pole. If only five can run, fold `sea` into `akropolis` and move Phaleron and its net-loft to `outskirts`.

### Before the agents start (this session)

1. **Register all 23 maps** with `tools/ichor/new_map.py`: placeholder layouts copied from Act I maps, stand-in music, the map ids and groups below, so every warp compiles from the start. The five outdoor maps go in `gMapGroup_TownsAndRoutes`. The 16 rooms and the two salt-well floors go in a new `gMapGroup_IndoorAstyra`, appended to `group_order`.
2. **Claim the cross-map story flags** (the hand-off table below) in 0x5B0–0x5C5. Then delete the `#ifndef FLAG_ICHOR_AKROPOLIS_RAID … 0` stub at the end of `flags.h`, which Lebadeia's scripts read.
3. **Claim three daily flags**: `FLAG_DAILY_ICHOR_ASTYRA_JAR` and `_ASTYRA_CHIPS` (the city's) and `_PANATHENAIA` (civic's, stretch). They take the next free offsets, 0x4F–0x51 today. `FLAG_DAILY_ICHOR_KRONIST_BREAD` already exists and is shared.
4. **Append batch 5's 23 trainer names to `parties/ORDER.txt`** in the order of the Ids table, so agents never touch that file. Stage `design/phase3/encounters/region_c2.json` from SCRIPT.md Part 4: every table is already written there. Batch 4 takes `region_c1.json`.
5. **Generalize the picture window.** Turn `Ichor_ShowProgram`/`Ichor_HideProgram` (`src/ichor_act2_scene.c`, the Dionysia's program close-up) into `special(Ichor_ShowPicture)` with `VAR_0x8004` = `ICHOR_PICTURE_PROGRAM`, `_DECREE`, `_FORGED_ORDER` or `_PRACTICE_TABLETS`, and `special(Ichor_HidePicture)`. The program stays a wrapper. The three new 64×64 images start as copies of the program, and sprites5 draws them.
6. **Add batch 5's block to `include/constants/ichor_gfx_stubs_act2.h`**: every walker in "Stand-ins" below, aliased to its stand-in. Also give `fold_parties.py` stand-ins for the new pics (Archer, Philosopher, Athlete, Potter, Pilgrim, Kleon Titan, Admin Rhea). With the dex in, stop dropping `Ability:` lines.
7. **Update `map_audit.py`.** Add `"SaltWell"` to the Astyra prefixes in `STAGES`.
8. **Rename the three trainers** whose names are longer than `TRAINER_NAME_LENGTH` (10) in SCRIPT.md: Theophrastos becomes **Tyrtamos** (his birth name; Aristotle renamed him), Antisthenes becomes **Krates** (Diogenes's pupil, which keeps the jar), and Aristoxenos becomes **Archytas** (the harmonist). None of the three appears in `design/` or on the Lazarus list.

### Maps

All are in `MAPSEC_ASTYRA`. Kinds are what `map_audit.py` judges them as. Interior sizes are a guide; the room's owner decides.

| Map (directory) | Kind | `map_type` | Size | Tilesets | Beats | Owner |
|---|---|---|---|---|---|---|
| `MAP_ASTYRA` (`Astyra`) | town | CITY | 64×56 | aethos + `astyra` | 48 (the Dipylon, the Agora), 52 (Kerykos's run), 53 | city |
| `MAP_ASTYRA_KERAMEIKOS` (`Astyra_Kerameikos`) | town | TOWN | 40×30 | aethos + `kerameikos` | 48 (first step: walls and rock, no text), 54 | outskirts |
| `MAP_ASTYRA_PAUPERS_GRAVES` (`Astyra_PaupersGraves`) | town (`"ichor_kind": "town"`) | ROUTE | 16×12 | aethos + `kerameikos` | — | outskirts |
| `MAP_ASTYRA_AKROPOLIS` (`Astyra_Akropolis`) | town | TOWN | 44×36 | aethos + `akropolis` | 55, 57 (Boutes, the grate) | akropolis |
| `MAP_ASTYRA_PHALERON` (`Astyra_Phaleron`) | town | TOWN | 36×24 | aethos + `phaleron` | 57 (the landing); batch 6's 58 starts here | sea |
| `MAP_SALT_WELL_1F` (`SaltWell_1F`) | dungeon | UNDERGROUND, lit from above | 30×24 | aethos + `salt_well` | 57 | sea |
| `MAP_SALT_WELL_B1F` (`SaltWell_B1F`) | dungeon | UNDERGROUND, `"cave": true` | 30×24 | aethos + `salt_well` | 57 | sea |
| `MAP_ASTYRA_ASCLEPEION` | interior | INDOOR | ~20×14 | oikos + civic's | 49, 56 (the pallets) | civic |
| `MAP_ASTYRA_AGORA` (the market hall) | interior | INDOOR | ~18×10 | oikos + civic's | shops | civic |
| `MAP_ASTYRA_STOA_OF_THE_ARCHON` | interior | INDOOR | ~22×12 | oikos + civic's | 52 | civic |
| `MAP_ASTYRA_LIBRARY` | interior | INDOOR | ~24×12 + courtyard | oikos + civic's | 51 | civic |
| `MAP_ASTYRA_LYCEUM` | interior | INDOOR | ~24×20 | oikos + civic's | the walk (4 trainers) | civic |
| `MAP_ASTYRA_TAVERN` (the Glaux) | interior | INDOOR | ~14×10 | oikos + homes's | knucklebones | homes |
| `MAP_ASTYRA_PHAEDONS_HOUSE` | interior | INDOOR | ~14×9, two rooms | oikos + homes's | 50, 56 (Elpis, "Morning.") | homes |
| `MAP_ASTYRA_KEPHALOS_HOUSE` | interior | INDOOR | ~18×12 | oikos + homes's | xenia host, the cloak | homes |
| `MAP_ASTYRA_LYSIMACHOS_HOUSE` | interior | INDOOR | ~7×6 | oikos + homes's | ostraka | homes |
| `MAP_ASTYRA_SCRIBES_HOUSE` (Eukleides) | interior | INDOOR | ~10×7 | oikos + homes's | the census errand | homes |
| `MAP_ASTYRA_PRAXAGORAS_HOUSE` | interior | INDOOR | ~12×9 | oikos + homes's | oil, Sideros | homes |
| `MAP_ASTYRA_SCULPTORS_WORKSHOP` (Kritios) | interior | INDOOR | ~16×12 | oikos + `astyra_crafts` | Scope Lens, the static Glyphlet | outskirts |
| `MAP_ASTYRA_WEAVERS_HOUSE` | interior | INDOOR | ~12×12, loft in-map | oikos + `astyra_crafts` | the Hyphantis trade | outskirts |
| `MAP_ASTYRA_KERAMEIKOS_POTTERY` (Brygos) | interior | INDOOR | ~12×9 | oikos + `astyra_crafts` | Spell Tag | outskirts |
| `MAP_ASTYRA_KERAMEIKOS_LODGE` (Manes) | interior | INDOOR | ~8×7 | oikos + `astyra_crafts` | lore, the obol | outskirts |
| `MAP_ASTYRA_PHALERON_NET_LOFT` (Hipponikos) | interior | INDOOR | ~12×10, loft in-map | oikos + `astyra_crafts` | Damp Rock | outskirts |

Every outdoor map's `ON_TRANSITION` holds its people's story hides: `FLAG_TEMP_11`–`_17`, set from the story flags. The bank pays only for state nothing else records, so SCRIPT.md Part 8's named hide flags (Alethea's six, Daphne's three, the Keeper, the Archon, Kerykos, the raid, the vote, the dolphin) are temp flags under those names' comments. Leave `FLAG_TEMP_18`–`_1F` to world-postgame's placements. Each map takes at most 64 object templates with 16 live at once, so hide the regulars around a scene while it plays.

### Who builds what

| Agent | Builds | Files it owns |
|---|---|---|
| **city** | The `astyra` secondary (SCRIPT.md Part 10, minus Phaleron): marble houses, the Agora's paving, the herald's stone, the urn's fence, the crowd metatiles (busy, quiet, the fenced vote), stoas, the Painted Stoa, the statue plinths (Kairos scratched), the pithoi, the Kronist's cart, the old spring house, fountains, four gate styles, the Akropolis cliff from below with the ramp's foot, the Asclepeion against the cliff, the herb garden, the theater seats, the drying lines, the chip heaps, the open orchard. `MAP_ASTYRA` with its roster: the archer, Hierokles, the wardens, Euthyphron, Diopeithes, the woman and child, Kerykos, the stall, Toxaris, Anacharsis, Zenon, Krates, the ramp guard, the citizens, the kid. Beat 48 (the Dipylon trigger, the proclamation, the statues), beat 52's run, beat 53 (the urn). The two decoys, the jars, the chips, the Perdix plaque, the Kronists' stall and its fixed dig, two daily digs, Kephalos's berry tree, the signs, and every door and gate below. | `tools/ichor/art/astyra_*.py`, `data/tilesets/secondary/astyra/`, `tools/ichor/maps/astyra.py`, `data/maps/Astyra/` and its layout, `design/phase3/TILES_astyra.md`, `parties/city.party`, `tests/act2_astyra.*` |
| **civic** | Five public rooms on its own room secondaries (`astyra_civic`, plus `_civic2` if the 504 tiles don't hold them). The Asclepeion: Phaedon, Panacoil, the Pithos, the cold hearth, beat 49, and beat 56's half (Chalkos and the pallets). The market hall: three counters and the moneychanger. The Stoa: beat 52 with `ICHOR_PICTURE_PRACTICE_TABLETS`; the clerk and the desk afterwards. The Library: beat 51, page V, the amphora. The Lyceum: the walk. `HEAL_LOCATION_ASTYRA`. | `tools/ichor/art/astyra_civic_*.py`, its secondaries, `tools/ichor/maps/astyra_civic.py`, those five maps, `design/phase3/ROOMS_astyra_civic.md`, the heal-location row, `parties/civic.party`, `tests/act2_astyra_civic.*` |
| **homes** | Six rooms on an `astyra_homes` secondary. Phaedon's house: beat 50; beat 56's half with Elpis, Daphne and "Morning." (sets `FLAG_ICHOR_RAID_MORNING`, holds `TIME_MORNING`); the music box; the Destiny Knot; Elpis and the conch. Kephalos's house: the xenia heal and rest, the cloak, the incense. Lysimachos's house: the ostraka, and his end of the errand. Eukleides's house: the errand, PP Up, the curl, the knucklebone link (stretch). Praxagora's house: before the raid and after it (Sideros, Olive Oil ×5). The Glaux: Dikaiopolis, Philokleon and Xanthippe. | `tools/ichor/art/astyra_homes_*.py`, its secondary, `tools/ichor/maps/astyra_homes.py`, those six maps, `design/phase3/ROOMS_astyra_homes.md` |
| **outskirts** | The `kerameikos` secondary (SCRIPT.md Part 10: stelai, lekythoi, the bull's plot, Hegeso, Dexileos, the Eridanos in its channel, cypresses, kilns, clay pits, cemetery grass, the mounds, the coin stones, the wild fig). `MAP_ASTYRA_KERAMEIKOS`: beat 48's first sight, Brygos, Proxenos, the drum, beat 54 (dusk; warps to the Akropolis). `MAP_ASTYRA_PAUPERS_GRAVES`. Five craftsmen's rooms on an `astyra_crafts` secondary: Brygos's workshop, the gravedigger's lodge, Kritios's workshop, the weavers' house, and Hipponikos's net-loft (its door is on the sea agent's Phaleron). The trade entry. | `tools/ichor/art/kerameikos_*.py`, `astyra_crafts_*.py`, both secondaries, `tools/ichor/maps/kerameikos.py`, `astyra_crafts.py`, those seven maps, `TILES_kerameikos.md`, `ROOMS_astyra_crafts.md`, the `src/data/trade.h` entry, `parties/outskirts.party`, `tests/act2_kerameikos.*` |
| **akropolis** | The `akropolis` secondary (Part 10: the rock's paving, the Propylaia, the bronze Athena's base, the Parthenon from outside, the Erechtheion and both porches, the trident marks under the roof hole, the grate, the Pandroseion; **the olive**, 2×3, with its falling frame and a fallen trunk; the split and its rubble rows; the stump, the drums, the weeds, the parapet; lit and unlit torch stands). `MAP_ASTYRA_AKROPOLIS`: beat 55 whole (four stops, two multi battles, Kleon, Rhea, the olive, `ICHOR_PICTURE_FORGED_ORDER`), the rock after the raid (Pandrosa, the guard, the stump, the parapet), beat 57's top half (Boutes, the grate, the Leaf Stone), Athena's great altar, the drum's ledge, a daily dig, the stargazing seat (stub). `PARTNER_ICHOR_ALETHEA_AKROPOLIS`. | `tools/ichor/art/akropolis_*.py`, `data/tilesets/secondary/akropolis/`, `tools/ichor/maps/akropolis.py`, the map, `TILES_akropolis.md`, `parties/akropolis.party`, the partner in `src/data/battle_partners.party` and `include/constants/battle_partner.h`, `tests/act2_akropolis.*` |
| **sea** | The `salt_well` secondary on aethos: salt-white rock, terraced tide pools (deep, drained, wadeable), two-frame sluice wheels, the great sluice, the shelf and its lip, wet sand, blowholes (dark, and lit), the fresh trickle, the sea arch, light shafts, two braziers. Start from `trophonios_*`/`kithairon_cave_*` rock. The `phaleron` secondary: coarse sand, dune grass, the quay and its bollards, fishers' huts, the harbor shrine, the cliff and its sea arch, the bay, the moored *Paralos*, and a small watchtower. Start from `kirrha_*` and the slice's trireme. Both well floors, with beat 57's well half (the sluices, the tide, the braziers, the blowholes, Asbestos, Nauson, Lepis, Alethea's three points, the dolphin, the Conch, Delphinus, the goodbye and the cloak, the ride out). `MAP_ASTYRA_PHALERON`: Euangelos, Konon, the shrine and its seller, the islet, Daphne from the morning after the raid, the *Paralos*'s hoplite and Peisias as one-line stubs for batch 6, and Hipponikos's door. | `tools/ichor/art/salt_well_*.py`, `phaleron_*.py`, both secondaries, `tools/ichor/maps/salt_well.py`, `phaleron.py`, those three maps, `TILES_salt_well.md`, `TILES_phaleron.md`, `parties/sea.party`, `tests/act2_salt_well.*` |
| **sprites5** | Every walker, object, class and pic in "Stand-ins" below, plus the three 64×64 picture-window images | as sprites2 and sprites3, with `tools/ichor/art/sprites_act2_b5*.py`, `design/phase3/SPRITES.md`, deleting each stub line as its sprite lands |

The homes agent stages no `.party` file because nobody in its rooms battles. Its test is `tests/act2_astyra_homes.*`.

**Shared files** take small appended entries, and this session resolves conflicts in them:
- `flags.h`: through `claim.py` only, inside your range.
- `layouts.json` and `map_groups.json`: this session registers every map; agents change only their own layout entries.
- `src/data/tilesets/{headers,graphics,metatiles}.h`: one appended block per new secondary.
- `heal_locations.json`: civic's.
- `trade.h`: outskirts's.
- `battle_partners.party` and `battle_partner.h`: akropolis's.
- The sprite tables: sprites5's.

**Tile budget.** A secondary holds at most 504 tiles. Keep 496–511 free on any map with wide doors. `astyra` is the fullest: one secondary has to draw a whole 64×56 city. Lean on aethos for roads, grass, trees and plain walls, and cut variety before the cliff or the Agora. Thyrsa City (56×48) fit in one set.

### Cross-map scenes and hand-offs

Each scene is owned by the agent whose map it plays on. Agents meet only through these flags and the fixed warp ids. Every cross-agent scripted warp is `warp(MAP_…, <warp id>)`, which the macro accepts, so no agent waits for another's coordinates.

| Flag (claimed by this session, 0x5B0–0x5C5) | Set by | Read by |
|---|---|---|
| `FLAG_ICHOR_ARRIVED_ASTYRA`, `_VISITED_ASTYRA` | city (the first step through the Dipylon) | everyone (rooms' occupants appear) |
| `FLAG_ICHOR_HEARD_PROCLAMATION` | city (beat 48) | civic (Alethea shows in the Stoa) |
| `FLAG_ICHOR_MET_PHAEDON` | civic (first heal), or homes (beat 50, if the heal was skipped) | both |
| `FLAG_ICHOR_MET_ELPIS` | homes (beat 50) | civic (Daphne in the Library; the Asclepeion's music) |
| `FLAG_ICHOR_LIBRARY_DAPHNE` | civic (beat 51) | city (Kerykos's run) |
| `FLAG_ICHOR_STOA_HEARING` | civic (beat 52) | city (the urn; the after-the-hearing lines), every room's lines |
| `FLAG_ICHOR_OSTRACISM_DONE`, `FLAG_ICHOR_WROTE_OWN_NAME` | city (beat 53) | outskirts (beat 54; the farmer box), everyone's after-lines |
| `FLAG_ICHOR_ALETHEA_CONFESSED` | outskirts (beat 54) | akropolis (beat 55 starts on arrival) |
| `FLAG_ICHOR_AKROPOLIS_RAID`, `_PROPYLAIA_PASSED`, `_KLEON_AKROPOLIS_DONE` | akropolis | city (the ramp guard hides from `_RAID`, so a whiteout can walk back up), akropolis (resume) |
| `FLAG_ICHOR_SECOND_FRAGMENT_STOLEN` (with `#define`s `FLAG_ICHOR_OLIVE_FELL` and `_RHEA_AKROPOLIS_DONE` aliased to it: always set together) | akropolis (end of 55) | civic (beat 56), everyone's after-raid lines |
| `FLAG_ICHOR_AFTER_RAID` | civic (beat 56, the Asclepeion) | homes (beat 56's house half, Sideros, the cloak), city lines |
| `FLAG_ICHOR_RAID_MORNING` (**new**) | homes ("Morning." in Phaedon's house) | akropolis (beat 57), sea (Daphne on the quay), city (the stall is empty) |
| `FLAG_ICHOR_SALT_WELL_OPEN` | akropolis (beat 57) | akropolis (the grate), sea |
| `FLAG_ICHOR_GOT_KEPHALOS_CLOAK` | homes | sea (the goodbye's cloak box) |
| `FLAG_ICHOR_DELIVERED_CLOAK`, `FLAG_ICHOR_ALETHEA_LEFT` | sea (beat 57) | homes (Kephalos's incense), akropolis, city |
| `FLAG_ICHOR_GOT_POSEIDONS_CONCH` (the engine's relic flag) | sea | homes (Elpis's conch), sea (the islet), everyone |

**The held tint chain** (`Ichor_HoldTimeOfDay`, ENGINE_API §7; the hold survives warps and saves):
1. city: beat 53 holds `TIME_DAY` for the urn and releases it at the end.
2. outskirts: the Kerameikos's `ON_TRANSITION` holds `TIME_EVENING` when `OSTRACISM_DONE` is set and `ALETHEA_CONFESSED` is not. After beat 54 it holds `TIME_NIGHT`, then `warp(MAP_ASTYRA_AKROPOLIS, 0)`.
3. akropolis and civic keep the night held.
4. homes' "Morning." holds `TIME_MORNING`.
5. sea releases the hold when the ride lands at Phaleron, and also on `FLAG_ICHOR_ALETHEA_LEFT` as a safety.

**Readings picked where the script is open:**
- **Beats 48 and 53 play in the outdoor Agora** on `MAP_ASTYRA`, so they are the city agent's. `MAP_ASTYRA_AGORA` is the market hall. **Beat 54 plays in the Kerameikos**, so it is outskirts's.
- **Beat 52's run** fires on a load of `MAP_ASTYRA` with the player on the Library's doorstep, `LIBRARY_DAPHNE` set and `STOA_HEARING` clear. It ends `warp(MAP_ASTYRA_STOA_OF_THE_ARCHON, 0)`. The Stoa plays the hearing on *any* entry in that state.
- **Beat 53's "next time"** is the first load of `MAP_ASTYRA` after the hearing where the player isn't standing on the Stoa's doorstep (`getplayerxy` in an `ON_FRAME`). Stepping out of the Stoa leaves the evening free; the next door or gate brings noon.
- **Beat 57's "by day"** means `RAID_MORNING`, not the clock. The morning stays held until Phaleron.
- **Pandrosa's "TM Calm Mind"** is the engine's gift I, a lesson (ENGINE_API §3). Use `EventScript_IchorHierophantRite` (one free loved offering: Olive Oil) and `EventScript_IchorHierophantGift`, with `VAR_0x8004 = ICHOR_GOD_ATHENA`.
- **No wild battles during the raid.** No engine flag turns encounters off, so keep the north wall's grass off the raid's path behind Alethea's turn-back triggers ("Not now. Up.").
- **The salt well's 1F basins** are non-surfable deep-water metatiles (draining is the only way), and so is B1F's flooded floor. Only B1F's deep pool and the arch are surfable. The audit then wants water tables on B1F alone, as Part 4 has them.
- **Alethea's and the dolphin's positions** in the well are derived from W1–W3, Asbestos's trainer flag and the Conch. That costs no flags.
- **The paupers' graves** are 16×12, the front matter's size.
- **The Phaleric Gate** is on the south edge, centre-west.
- **The Glaux** is homes's, to balance the load.

### Seams and warps

Offsets follow batch 2's rule: the game reads a neighbor's row (or column) as this map's minus the offset. On left and right connections the 8 columns nearest the seam are aethos-only; on up and down connections, the 6 rows (MAP_DESIGN §5). This applies across the overlap, unless the two maps share a secondary.

| Seam | Fixed now | Connection | Owner |
|---|---|---|---|
| Route 16 (batch 4) → the Kerameikos's west edge | The Kerameikos's road meets x = 0 on rows 14–15, with verges on 13 and 16; every other row of the west edge is blocked. Columns 0–7 are aethos-only (road, verges, cypresses, rocks). For Route 16's road on rows *q*, *q*+1: Kerameikos `left` offset 14 − *q*, Route 16 `right` offset *q* − 14. Added at integration once Route 16 exists. | none yet | outskirts |
| The Kerameikos ↔ Astyra (the Dipylon) | The Kerameikos's road meets x = 39 on rows 14–15 (verges 13, 16), and columns 32–39 are aethos-only. Astyra's Dipylon road meets x = 0 on rows 28–29 (verges 27, 30), and columns 0–7 are aethos-only outside the west wall. **The Dipylon's towers stand on Astyra's map at columns 8–11**, its passage on rows 28–29, as Thyrsa's gates do. | Kerameikos `right` −14; Astyra `left` +14 | outskirts, city |
| The Kerameikos ↔ the paupers' graves | The gap in the cemetery's south wall meets y = 29 at columns 24–27 (path 25–26). The graves' path meets y = 0 at columns 6–9 (path 7–8). Same secondary, so there's no strip. | Kerameikos `down` +18; graves `up` −18 | outskirts |
| Astyra ↔ Phaleron (the Phaleric Gate) | Astyra's road meets y = 55 at columns 28–31 (road 29–30), the gate in the south wall above it, and rows 50–55 are aethos-only. Phaleron's road meets y = 0 at columns 10–13 (road 11–12), and rows 0–5 are aethos-only. | Astyra `down` +18; Phaleron `up` −18 | city, sea |
| Astyra → Route 17 (batch 7), the Diochares Gate | Astyra's road meets y = 0 at columns 50–53 (road 51–52), by the Lyceum; rows 0–5 are aethos-only. For Route 17's road at columns *c*…*c*+3: Astyra `up` 50 − *c*, Route 17 `down` *c* − 50. Until then the warden stands in the passage, with his SCRIPT.md lines; batch 7 moves him aside. | none yet | city |
| Astyra → Route 18 (batch 7), the Itonian Gate | Astyra's road meets x = 63 on rows 44–45 (verges 43, 46); columns 56–63 are aethos-only. For Route 18's road on rows *r*, *r*+1: Astyra `right` 44 − *r*, Route 18 `left` *r* − 44. The warden stands in the passage the same way. | none yet | city |
| Phaleron's south edge → the sea (Route 3, world-act1, or batch 7's open sea) | Open water across the whole edge, rows 18–23, aethos water only, so it can join at any offset later | none yet | sea |

If the city and outskirts agents want the walls to continue across the Dipylon seam, they may share a walls-and-gate core at identical metatile ids in both secondaries, the kithairon/kronia trick. The seam then becomes core-or-aethos. They agree it together and record it here; the default is the aethos strip.

**Door warps, fixed now.** Outdoor warp *N* leads to the room's warp 0 (and 1, for a two-wide door), which leads back to *N*. The outdoor map's owner places the door; the room's owner wires the way back.

| Outdoor map | Warp | Leads to |
|---|---|---|
| `MAP_ASTYRA` | 0–5 | `_ASCLEPEION`, `_AGORA`, `_STOA_OF_THE_ARCHON`, `_LIBRARY`, `_LYCEUM`, `_TAVERN` |
| `MAP_ASTYRA` | 6–12 | `_PHAEDONS_HOUSE` (next door to the Asclepeion), `_KEPHALOS_HOUSE`, `_LYSIMACHOS_HOUSE`, `_SCULPTORS_WORKSHOP`, `_WEAVERS_HOUSE`, `_SCRIBES_HOUSE`, `_PRAXAGORAS_HOUSE` |
| `MAP_ASTYRA` | 13 | The ramp's top step, to `MAP_ASTYRA_AKROPOLIS`'s warp 0 (the west foot). The ramp guard stands in front of it until `AKROPOLIS_RAID`. |
| `MAP_ASTYRA_KERAMEIKOS` | 0, 1 | `_KERAMEIKOS_POTTERY`, `_KERAMEIKOS_LODGE` |
| `MAP_ASTYRA_PHALERON` | 0 | `_PHALERON_NET_LOFT` |
| `MAP_ASTYRA_AKROPOLIS` | 0 | The west foot of the ramp, back to `MAP_ASTYRA`'s warp 13. During the raid, a trigger turns the player back ("ALETHEA: Not now. Up."). Beat 54's warp lands here. |
| `MAP_ASTYRA_AKROPOLIS` | 1 | The north porch's grate, to `MAP_SALT_WELL_1F`'s warp 0. It is shut by metatile until `SALT_WELL_OPEN`: "A bronze grate in the floor… locked from below." |
| `MAP_SALT_WELL_1F` | 1 | The stair down, to `MAP_SALT_WELL_B1F`'s warp 0 |

**Scripted warps:**
- Beat 52: `MAP_ASTYRA` → the Stoa's warp 0.
- Beat 54: the Kerameikos → the Akropolis's warp 0, at night.
- The blowholes: B1F coord events land the player in 1F's P1, wet. Nothing else changes.
- The sea-door: coord triggers on the arch's water at B1F and at Phaleron. The player is surfing on the Conch, which the engine's Surf prompt allows. A warp onto water keeps the player surfing; the sea agent's test proves it. Both ends are the sea agent's.
- The first ride lands surfing in Phaleron's bay, under the arch.

**Keep these tiles free** for world-postgame's `PLACEMENTS.md`:
- **City:** a walkable tile beside the herald's stone (the truce herald, `FLAG_TEMP_18`).
- **Asclepeion:** the counter tile, and the first three pallets of the incubation stoa. Iaso takes Phaedon's place in the post-game, so his object hides on `FLAG_ICHOR_POSTGAME` until Act III names its unmasking flag.
- **Phaleron:** a watchtower at the quay's root (Lynkeus, facing down), plus open bg spots at the dune grass where the beach bends, at the harbor shrine (whose script the post-game branches) and on the quay stones under the *Paralos*'s gangplank.

### Heal locations and herms

- **`HEAL_LOCATION_ASTYRA`** (civic adds the row): map `MAP_ASTYRA`, at the Asclepeion's doorstep (the city agent records the tile here), `respawn_map` `MAP_ASTYRA_ASCLEPEION`, `respawn_npc` `LOCALID_ASTYRA_HEALER` (Phaedon's counter object).
- A whiteout mid-raid respawns here at night, and the raid resumes at its first undone stop.
- Kephalos's xenia heal and the salt well's spring (`special HealPlayerParty`) aren't heal locations.
- **No herms.** Routes 13–16 are batch 4's; Routes 17–18 are batch 7's.
- Fly: when the fly wiring lands, `MAPSEC_ASTYRA` reads `FLAG_ICHOR_VISITED_ASTYRA` like the other towns (`src/region_map.c`, this session).

### Ids

**Trainers** (23). Stage parties in `design/phase3/parties/<agent>.party`, copied from SCRIPT.md Part 3 (14830–15513) with the renames. Agents don't pick numbers: this session folds (`fold_parties.py`; today's next free id is 232). Classes and pics that don't exist yet fold as stand-ins. The Fisher class is the existing `Class: Fisherman`.

| Agent | Trainers, in `ORDER.txt` order |
|---|---|
| city | `TRAINER_ICHOR_TOXARIS`, `_ANACHARSIS` (Archers), `_ZENON`, `_KRATES` (Philosophers) |
| civic | `TRAINER_ICHOR_AUTOLYKOS`, `_ARCHYTAS`, `_PHRYNON`, `_TYRTAMOS` (the walk; `cleartrainerflag` all four to walk again after a loss) |
| outskirts | `TRAINER_ICHOR_BRYGOS` (Potter), `_PROXENOS` (Pilgrim) |
| akropolis | `TRAINER_ICHOR_GRUNT_AKROPOLIS_LITHOS`, `_KONIORTOS`, `_SIDEROS`, `_CHALKOS`; `TRAINER_ICHOR_KLEON_AKROPOLIS_KYNDER`, `_HIPLING`, `_NEBREL` (aces Seismare, Daphnyad, Pylakyon); `TRAINER_ICHOR_RHEA_AKROPOLIS`. Also `PARTNER_ICHOR_ALETHEA_AKROPOLIS` (Plouteras, Sophowl, Skylaps), written straight into `battle_partners.party`, not folded; `PARTNER_COUNT` goes to 3. |
| sea | `TRAINER_ICHOR_EUANGELOS`, `_NAUSON` (Fisherman), `_KONON` (Sailor), `TRAINER_ICHOR_GRUNT_SALT_WELL_ASBESTOS`, `_LEPIS` |

The towns need no route-standard trainers. The salt well's three meet the dungeon's three. Aigina's eight Astyra-level placeholders stay batch 4's (Handovers above).

**Bank flags and hidden items.** Both come from the second bank (`claim.py --range LO-HI bankflag FLAG_ICHOR_<NAME>` and `claim.py --range LO-HI hiddenitem FLAG_ICHOR_HIDDEN_ITEM_<MAP>_<ITEM>`; the tool requires that `_HIDDEN_ITEM_` prefix). Visible items are `FLAG_ICHOR_ITEM_<MAP>_<ITEM>` bank flags. **Batch 5 has 0x5B0–0x60F (96).** Each agent claims inside its "Range at 96" row; "Min" is the least it needs.

| Range at 96 | Owner | What | Min | Range at 72 |
|---|---|---|---|---|
| 0x5B0–0x5C5 | this session | the 20 hand-off flags above, and 2 spare | 20 | 0x5B0–0x5C3 |
| 0x5C6–0x5CF | city | Hyper Potion, Max Repel, Ultra Ball ×2 (balls); hidden Silver Owl (`ITEM_RELIC_SILVER`, the drain grate), Rare Candy (Kodros's heel), Heart Scale (the weaving court) | 6 | 0x5C4–0x5C9 |
| 0x5D0–0x5D9 | civic | `GOT_CHOICE_SPECS` (alias `LYCEUM_WALK_DONE`); room hidden items, optional | 1 | 0x5CA |
| 0x5DA–0x5E7 | homes | `GOT_DESTINY_KNOT`, `ELPIS_HEARD_CONCH`, `GOT_PURE_INCENSE`, `EUKLEIDES_ERRAND`, `_ERRAND_DONE`, `GOT_EUKLEIDES_PP_UP`, `GOT_PRAXAGORAS_OIL`, `OSTRAKA_10`, `_20`, `_30`, `KNUCKLEBONES_ASTYRA` (Xanthippe), `_DIKAIOPOLIS`, `_PHILOKLEON`; room hidden items, optional | 13 | 0x5CB–0x5D7 |
| 0x5E8–0x5F7 | outskirts | `GOT_SPELL_TAG`, `GOT_SCOPE_LENS`, `STATIC_KRITIOS_GLYPHLET`, `TRADED_HYPHANTIS`, `GOT_DAMP_ROCK`, `HIDE_KERAMEIKOS_DRUM`; Revive, X Defend, one ball on the graves (balls); hidden Bronze Obol ×2 (`ITEM_RELIC_COPPER`: the grave-jar, the flat stone), plus one more on each map to reach the town minimum of 2 | 13 | 0x5D8–0x5E4 |
| 0x5F8–0x600 | akropolis | `GOT_LEAF_STONE`, `HIDE_AKROPOLIS_DRUM`; Full Heal, Star Piece (balls); hidden Stardust, plus one more | 6 | 0x5E5–0x5EA |
| 0x601–0x60F | sea | `SALT_WELL_W1`, `_W2`, `_W3`, `_LOW_TIDE`; Phaleron's Big Pearl (the islet), 1F's Pearl, Heart Scale and Shoal Salt, B1F's Mystic Water (balls); hidden B1F Big Pearl, B1F Shoal Salt ×2, Phaleron Shoal Shell ×2, plus one more on Phaleron | 13 | 0x5EB–0x5F7 |

The Glaux's three flags are counted with homes. If a range runs out, name the flag in your doc, stub its use, and say so.

**Engine indices** (ENGINE_API §1's blocks):
- **Decoys:** `FLAG_ICHOR_THEOXENIA_START` +0x26 is the old man at the crossing (`FLAG_ICHOR_DECOY_ASTYRA_1`, a `#define`); +0x27 is the thirsty girl (`_2`). That fills world-act2's block, so batch 4's two decoys need a new one.
- **Braziers:** `FLAG_ICHOR_BRAZIERS_START` +0x23 and +0x24 are B1F's shelf braziers B1 and B2.
- **Fixed dig:** `FLAG_ICHOR_DIG_FIXED_START` +0x16 is the old spring house's threshold (a Hard Stone; the Titan's sickle pin doesn't exist yet).
- **Desecrated altars:** none in Astyra. Indices 11–13 stay for batch 4's Route 13, 15 and 16.
- **Daily digs:** seven spots, but no block has been given out yet. Each stays on `EventScript_IchorAct2_DigStub`, with its spot named in a comment.
- **Other ranges:** Delphinus is `FLAG_ICHOR_CONSTELLATIONS_START` +0 (SYSTEMS §8 #1). Page V is `FLAG_ICHOR_PAGES_START` +4, given as page III was (`ichor_act2.pory`'s pattern, in the Library's own script). Tablets are found at `FLAG_ICHOR_PROPHECY_START` +*n* and read at +8+*n*. Ostraka are `FLAG_ICHOR_OSTRAKA_START` +0…29, counted with `Ichor_CountFlagRange`. Athena's rite and gift come from the engine's gift range. The knucklebone link (stretch) is `FLAG_ICHOR_XENIA_START`, and its index needs the engine session.

**Vars:** none permanent (SCRIPT.md Part 8). The Lyceum's walk is `VAR_TEMP_1`; scene gates are `VAR_TEMP_*`. **Daily flags:** the three in step 3 above. Nothing here needs the director's OK beyond the block's width.

### Encounters and parties

BALANCE.md's Astyra row is wild 30–36 and trainers 33–38. SCRIPT.md Part 4 has every slot. This session stages them as `design/phase3/encounters/region_c2.json` (labels below). Agents only report a change, such as a table their encounter cells don't need. The two small spots sit below 30 on purpose (the dex's first stages). The audit WARNs about them; explain that in the report.

| Map | Labels | Land rate, band | Water and fishing |
|---|---|---|---|
| `MAP_ASTYRA` (the herb garden, the weaving court) | `gAstyra_Morning`, `_Night` | 15, 29–33 | — |
| `MAP_ASTYRA_PAUPERS_GRAVES` | `gAstyraPaupersGraves_Morning`, `_Night` | 20, 27–31 (Obolorn at night, 28) | — |
| `MAP_ASTYRA_KERAMEIKOS` | `gAstyraKerameikos_Morning`, `_Night` | 20, 32–36 (Kalyptor at night) | none: the Eridanos is an impassable channel |
| `MAP_ASTYRA_AKROPOLIS` | `gAstyraAkropolis_Morning`, `_Night` | 15, 31–34 (Glaukoin, Sophowl from 33, Hierolive 2%) | — |
| `MAP_ASTYRA_PHALERON` | `gAstyraPhaleron_Morning`, `_Night` | 20, 33–36 | in `_Morning`: water rate 4 (Galenyon, Narkeray, Kynoketos); fishing rate 30 |
| `MAP_SALT_WELL_1F` | `gSaltWell1F_Morning` (one table at all hours) | 10, 34–37 | — |
| `MAP_SALT_WELL_B1F` | `gSaltWellB1F_Morning` | 10, 34–37 | in `_Morning`: the deep pools' water and fishing |

**Statics** (scripted `setwildbattle`):
- Pithound 32–34 in the day's jar, `FLAG_DAILY_ICHOR_ASTYRA_JAR`; the jar is `RetrieveLotteryNumber` mod 5 (check that it re-rolls daily).
- Glyphlet 31–33 in the day's chip heap, `_ASTYRA_CHIPS`.
- Kritios's Glyphlet holding a Hard Stone, 34, once.
- The omen's Hierolive, 35: stub.

Party levels:
- The city's four: 35–36.
- The Lyceum: 35–37.
- The Kerameikos: 34–35.
- Phaleron: 35–36.
- The salt well: 35–37.
- The raid pairs: 36–37.
- Kleon: 35–39, ace 39.
- Rhea: 38–40.
- Alethea's partner team: 34–36.

Species are checked against `design/dex/species/*.yaml`: every species above and in Part 3's blocks is in the dex (152 names), so nothing is a stand-in. With the dex real, parties may carry their `Ability:` lines.

### Stand-ins (sprites5's scope)

Each name goes into the batch 5 block of `ichor_gfx_stubs_act2.h` as `OBJ_EVENT_GFX_ICHOR_<NAME>` → its stand-in, and its line is deleted when the sprite lands. Palette families follow SPRITES.md; one map shows at most three tags, so plan the Agora's crowd scenes around that.

**Classes** (portrait, plus a walker for each), folded as stand-ins until they land:
- `Archer` (→ Hoplite)
- `Philosopher` (→ Augur)
- `Athlete` (→ Hoplite; batch 4's Agias needs it too)
- `Potter` (→ Shepherd)
- `Pilgrim` (→ Shepherd)
- `Titan Admin` (→ Titanborn)

**Pics:** `Archer`, `Philosopher`, `Athlete`, `Potter`, `Pilgrim`, `Kleon Titan` (→ Kleon; the helmet pushed back like a cap), `Admin Rhea` (→ the grunt).

The partner's `Class: Scholar` is written as Augur until a Scholar class exists. HEALER (class, pic and walker) is batch 4's Epione: an optional extra.

**Story walkers**, with stand-ins:
- `PHAEDON` (→ `HEALER`), with `PHAEDON_KNEEL` for the pallet and the bed's end
- `ELPIS_BED`, sitting up and lying down (→ `KID_F`)
- `KEEPER`: Lykophron, with an ink-dark right hand readable at walker size (→ `AUGUR`)
- `ARCHON` (→ `ELDER_M`)
- `RHEA` (→ `TITAN_GRUNT`)
- `KLEON_TITAN` (→ `KLEON`)
- `ALETHEA_SATCHEL`, sitting on her satchel (→ `ALETHEA_SEATED`)
- `ALETHEA_CLIMB`, the goat path; optional (→ `ALETHEA`)
- `DAPHNE_SEATED`, on a stool with a scroll (→ `PROFESSOR_DAPHNE`)
- `KERYKOS` (→ `HERALD`; it's world-act1's real walker, so delete this line when their branch merges)
- `KERYKOS_STAFF`, on the stone with the staff raised (→ `HERALD`)
- `EUTHYPHRON` (→ `KRONIST`)
- `FARMER`, in a straw hat (→ `ELDER_M`)
- `XANTHIPPE` (→ `WOMAN`)
- `SIDEROS_BANDAGED` (→ `YOUTH_M`)
- `CHALKOS_BANDAGED` (→ `TITAN_GRUNT`)
- `TITAN_DIGGER`, with a shovel (→ `TITAN_GRUNT`)

**Townsfolk by palette swap:**
- `BOUTES` (sea-blue; → `ELDER_M`)
- `PANDROSA` (white, olive sprig; → `PRIESTESS`)
- `APELLIKON` (→ `ELDER_M`)
- `TYRTAMOS` (→ `AUGUR`)
- `KEPHALOS` (garland; → `ELDER_M`)
- `LYSIMACHOS` (patched; → `ELDER_M`)
- `KRITIOS` (→ `MAN`)
- `KALONIKE` (→ `WOMAN`)
- `WEAVER_GIRL` (→ `YOUTH_F`)
- `EUKLEIDES` (→ `MAN`)
- `PRAXAGORA` (→ `MOM`)
- `KLEITOS` (→ `KID_M`)
- `MANES` (→ `ELDER_M`)
- `HIPPONIKOS` (→ `FISHER`)
- `DIOPEITHES` (→ `AUGUR`)
- `HIEROKLES` (crow feather; → `AUGUR`)

The six voters' shard-drop frame is optional; a face-up and a sound effect do the job.

**Objects:**
- `KRONIST_CART`, 2×1 (→ `UPTURNED_BOAT_L`)
- `URN`, in its fence (→ `TABLET`); or metatiles plus a tipping object
- `DOLPHIN`, with the conch in its mouth (→ a water follower)
- `STARRY`, the clay bull (→ `TABLET`)
- `MUSIC_BOX`, with a two-frame tick (→ `TABLET`)
- `FRAGMENT_GLINT` (→ the item-ball sprite)

Ophidrop, Panacoil, Plouteras ×2, Pithound and Glyphlet are `OBJ_EVENT_GFX_SPECIES(...)`, and real now.

**Screens:** the three 64×64 picture images (`ICHOR_PICTURE_DECREE`, `_FORGED_ORDER`, `_PRACTICE_TABLETS`).

**Later, not batch 5:**
- the dolphin as the surf sprite (stub: the normal surf blob)
- the two new battle backgrounds (stub: the dark temple and the cave)
- the map-name stele

### What the script needs from the engine

**Built** (use directly):
- **Multi battles:** `setmultitrainerbattle` (`asm/macros/event.inc`, 2665) with a partner from `battle_partners.party`.
- **The held tint:** `Ichor_HoldTimeOfDay` and `Ichor_ReleaseTimeOfDay`. This is SCRIPT.md Part 8's "hold the tint" ask, already done.
- **Scene staging:** `special ShakeCamera`; `setmetatile` plus `DrawWholeMapView` (the olive, the split, the sluices, the tide, the crowd); `FLAG_ICHOR_NO_WHITEOUT` (`B_FLAG_NO_WHITEOUT`) for Kleon.
- **Braziers and darkness:** `EventScript_IchorBrazier` and the lit zones.
- **Rites:** `EventScript_IchorHearth` (the Asclepeion's hearth, after Phaedon's lines); `EventScript_IchorAltar_Poseidon` (Phaleron); `EventScript_IchorTempleAltar_Athena` (the rock's great altar; offerings count double, as SCRIPT.md wants); the Hierophant calls for Pandrosa.
- **Favor:** `Ichor_AddFavor` for the decoys (Zeus +1).
- **The Conch:** the engine's Surf checks `ITEM_POSEIDONS_CONCH`.
- **The pictures:** `Ichor_ShowPicture`, once step 5 is done.

**Script-only, no engine work:**
- **The ostracism:** scripted walks to the urn, a clink sound effect per shard, the count board as three sign boxes, the decree as a picture. The farmer's three-way multichoice sets `WROTE_OWN_NAME`.
- **The raid:** four stops shown by flags in turn, with 14 objects at most.
- **The Lyceum's no-heal walk:** a coord-triggered sequence on `VAR_TEMP_1`.
- **The tide puzzle:** metatile swaps from flags in `ON_LOAD`, with blowholes as coord warps.
- **The ride out:** the Surf prompt, then a coord warp while surfing.
- **The daily jar:** `RetrieveLotteryNumber`.
- **Kritios's and the painter's type checks:** loop over the party's species and compare their types.

**Stubbed by tag** (the engine isn't there yet):
- `ICHOR_STUB_DIG`: the seven daily digs, the fixed dig, and the ostraka's only source.
- `ICHOR_STUB_KNUCKLEBONES`: the Glaux, as scripted wins and losses, as Thyrsa's Kantharos did.
- `ICHOR_STUB_XENIA_REST`: Kephalos's rest menu. The heal itself works.
- `ICHOR_STUB_KEY_ITEMS`: Kephalos's Cloak (a flag carries it, as Pylades's fig does), the Ostrakon, the Half Knucklebone, the Titan's sickle pin, the Pythian Laurel.
- `ICHOR_STUB_TMS`: TMs Payback, Taunt and the scroll stall's five.
- `ICHOR_STUB_OMENS`: Hierokles reads `Ichor_GetOmen` with a fallback line. The three Astyra omen entries (the Glaukoin swarm, the Hierolive visitor, fog over the Kerameikos) go to the engine session to append to `ichor.h`.
- `ICHOR_STUB_STARS`: Delphinus's line and the parapet's seat. The flag is set for real.
- `ICHOR_STUB_MUSIC`:

  | SCRIPT.md's cue | Stand-in |
  |---|---|
  | `MUS_ICHOR_ASTYRA` | `MUS_ICHOR_EMPORION` |
  | `MUS_ICHOR_OSTRACISM` | silence |
  | `MUS_ICHOR_PHAEDON` | `MUS_ICHOR_ASCLEPEION` |
  | `MUS_ICHOR_ALETHEA` | skipped |
  | `MUS_ICHOR_BATTLE_RIVAL_TITAN` | `MUS_ICHOR_BATTLE_RIVAL` |
  | `MUS_ICHOR_BATTLE_ADMIN_RHEA` | `MUS_ICHOR_BATTLE_ADMIN` |
  | `MUS_ICHOR_SURF` | the map's music |

  The salt well's `MUS_ICHOR_HOLLOW`, `MUS_ICHOR_TITAN` and the lullaby (627, 628) are built and real. The new sound effects stand in with stock ones.

**Needs another session:**
- **The engine session:** a daily-dig block for Astyra's seven spots; a new theoxenia decoy block for batch 4; the knucklebone link's xenia index; the moneychanger's +20% on the Silver Owl (a sell-price hook; until then he only talks).
- **The Panathenaia's torch race:** it needs a festival-day check and a new flame kind (`FLAME_PANATHENAIA` in `src/ichor_relics.c`). It's deferred: civic writes only the athlete's "No race this year" line.

**The engine's answers (ichor-engine, 2026-11-14).** They're on `claude/ichor-engine-systems-5a55eb` through 4c11c5e57f, not on main yet; ENGINE_API §1, §7 and §8 have the details. Until the director merges that branch into main and main is merged here, write each call below as a stub, with the exact call in a comment and its tag. This session swaps the stubs for the real calls after that merge.
- **Daily digs:** world-act2 has `FLAG_DAILY_ICHOR_DIG_START` +0x20–0x3F (32). Batch 5 takes +0x20–0x26 (city +0x20–0x21, akropolis +0x22, outskirts +0x23–0x24, sea +0x25–0x26). Batches 1–3's stubs take +0x27 on later. Call: `setvar(VAR_0x8004, <spot>); setvar(VAR_0x8005, ICHOR_DIG_ACT_II | ICHOR_DIG_SHERDS(ICHOR_AMPHORA_PANDORA)); goto(EventScript_IchorDigSpot)`. Fixed finds: `setvar(VAR_0x8004, <index>); setvar(VAR_0x8005, <item or ICHOR_FIND_PROPHECY(n) / _PAGE(n) / _SHERD(a) / ICHOR_FIND_OSTRAKON>); call(EventScript_IchorDigFixed)`; VAR_RESULT is TRUE if it was dug just now. The Kronists' stall's fixed dig is +0x16.
- **Decoys:** batch 5 keeps +0x26 and +0x27. Batch 4 gets the new block +0x28–0x2F. A god in disguise is an object with trainer type `TRAINER_TYPE_ICHOR_GOD`.
- **Xenia:** Eukleides's knucklebone link is `FLAG_ICHOR_XENIA_START + 0x03`. Kephalos's rest is `call(EventScript_IchorXeniaRest)`, which sets VAR_RESULT TRUE if the player rested, so `ICHOR_STUB_XENIA_REST` goes.
- **Knucklebones (the Glaux):** `bufferstring(STR_VAR_3, <prose name>); setvar(VAR_0x8004, ICHOR_BONES_CAUTIOUS / _BOLD / _SILENOS / _MOM); call(EventScript_IchorKnucklebones)`. It plays best of five; VAR_RESULT is TRUE if the player won.
- **The moneychanger:** `setvar(VAR_0x8004, ITEM_RELIC_SILVER); setvar(VAR_0x8005, 20); specialvar(VAR_RESULT, Ichor_SellToMoneychanger)`. TRUE means sold, with the price in STR_VAR_1.
- **Omens:** the numbers are in ichor.h: `OMEN_SWARM_GLAUKOIN`, `OMEN_VISITOR_HIEROLIVE`, `OMEN_WEATHER_KERAMEIKOS_FOG`. Rows go in `src/data/ichor_omens.h` (examples in ENGINE_API §7). A weather omen runs in the map's ON_TRANSITION with `Ichor_CheckOmen`.
- **Level check:** `specialvar(VAR_RESULT, Ichor_GetHighestPartyLevel)`.
- **Still deferred:** the Panathenaia's festival day and `FLAME_PANATHENAIA`.

### Tests

Each agent writes `tools/ichor/tests/act2_<name>.sh`, `.lua` and `_consts.c` on `slice_lib.lua`, as `act2_harbors.sh` does: Quickstart, then an EWRAM setup script gives a level-36 team (Hecate's Torch and the Girdle in the bag) and batch 4's end flags (the five laurels, `FLAG_ICHOR_ROUTE15_OPEN`, `_SAW_ASTYRA`, `_ALETHEA_GOT_SKYLAPS`, `_KLEON_JOINED_TITANS`). It seeds the hand-off flags its scenes need, warps in, plays by key presses, checks flags (bank ones through IchorSave), and saves screenshots to `build/test_<name>/shots/`. It fails on any failed check, a crash or a timeout.

| Test | Agent | Checks |
|---|---|---|
| `act2_astyra.sh` | city | The Dipylon trigger; the proclamation (Alethea hidden, `HEARD_PROCLAMATION`); the statues, Kerykos and the stall; both decoys (+0x26, +0x27, Zeus Favor +1); the jar and the chips; the ramp guard blocks; every door 0–13 lands on its room's warp 0, and back; the wardens; the Phaleric seam; signs and hidden items. Seed `LIBRARY_DAPHNE` and load on the Library's doorstep: the run lands in the Stoa. Seed `STOA_HEARING`: step out of the Stoa (no urn), then the Glaux and back out (the urn, each farmer branch in turn, `OSTRACISM_DONE`, tint released). |
| `act2_astyra_civic.sh` | civic | The first heal (`MET_PHAEDON`, the lead's nickname) and a rotated closing; the Pithos and the hearth; the shops open. Seed `MET_ELPIS`: Daphne, page V (only A PARTRIDGE sets +4), the amphora. The hearing with 0 and with 5 tablets, the practice-tablet picture, `STOA_HEARING`. The walk won (Choice Specs) and lost (retry). Seed `SECOND_FRAGMENT_STOLEN`: Chalkos, the heal, `AFTER_RAID`. A forced whiteout respawns at the counter. |
| `act2_astyra_homes.sh` | homes | Beat 50, both choices (`MET_ELPIS`, Daphne hidden, the music box). Seed `AFTER_RAID`: the house half, `RAID_MORNING`, `TIME_MORNING` held; the Destiny Knot. Kephalos's heal; the cloak, then both incense branches. The errand round trip (PP Up). The ostraka lines. Praxagora before and after (Olive Oil ×5). The Glaux's three tables. Every occupant answers. |
| `act2_kerameikos.sh` | outskirts | In from the west edge; Brygos and Proxenos; the drum and the X Defend; hidden items; the graves seam; Manes. Each craft room's quest with the right Pokémon given: the Spell Tag, the Scope Lens and the static, the PEPLOS trade, the Damp Rock. Seed `OSTRACISM_DONE`: evening held, both forms of beat 54, `CONFESSED`, arriving on the Akropolis's warp 0 with night held. |
| `act2_akropolis.sh` | akropolis | Seed `CONFESSED`: the Propylaia and its picture; no going back; both multi battles with Alethea; one forced loss, whiteout and resume; the heal at 2b; Kleon for each starter, and a loss (`NO_WHITEOUT` cleared after); Rhea; the olive's metatiles read fallen; `SECOND_FRAGMENT_STOLEN`; the ramp opens. Seed `RAID_MORNING`: Boutes, `SALT_WELL_OPEN`, the Leaf Stone; Pandrosa's rite and her gift at Favor 30; the drum's ledge; the day table. |
| `act2_salt_well.sh` | sea | Seed `SALT_WELL_OPEN`: wading; W1 both ways; W3 and the side grotto; W2 and Asbestos; the spring heals; HIGH, the shelf, both braziers (+0x23, +0x24), Nauson; LOW, a blowhole (state kept), Lepis and the Mystic Water; the Conch, Delphinus (+0), the goodbye with and without the cloak, `ALETHEA_LEFT`; surfing through the arch lands at Phaleron surfing, tint released. On Phaleron: both trainers, the shrine and its shop, the islet by surf, Daphne on the quay, the net-loft door, the north seam. |

**This session's `act2_batch5.sh`:**
1. `map_audit.py` on all 23 maps. Every FAIL that's right for a map (a small spot's levels) is explained in the report.
2. The walk across every seam, door, stair, grate and the sea-door.
3. The story from the Kerameikos's west edge (Route 16 isn't built yet), headless: 48 → 57 in order, ending surfing at Phaleron with the Conch, Alethea gone and Daphne at the gangplank.
4. `--all` runs every agent's test and batches 1–3's suites. Then `make check`.

The report gives the ROM delta. Batch 5 is five outdoor sets, three or four room sets and about 50 sprites, so expect 0.6–0.9 MB; check `make`'s memory line.

### Decisions (2026-11-14)

- **Bank block:** 0x5B0–0x60F (96). Batches 4, 6 and 7 keep 0x610–0x63F and the 89 free first-bank flags in 0x100–0x1FF.
- **Engine asks:** answered above.
- **Renames:** Tyrtamos, Krates and Archytas are approved.
- **Phaleron's south edge:** open water with no connection for now. Batch 7 (the open Aegean) or world-act1 joins it later; leave the 8-column aethos-only strip clear.

## Handovers waiting for later batches

**Batch 4, Aigina's interior** (from world-act1, 2026-11-14; maps on `claude/world-act1-6d11b7` at 1090709095, seams and spots in `design/phase2/BUILD.md`, the island stitched in `design/phase2/img/aigina_island.png`). `MAP_AEGINA_APHAIA_ROAD`, `MAP_AEGINA_TEMPLE_OF_APHAIA` and `MAP_AEGINA_MOUNT_OROS` are connected to the town and each other. The town's north gate opens on `FLAG_ICHOR_FERRY_TO_AEGINA`. Placeholders for us to replace, each with a script tagged `ICHOR_ACT2`:

| Who | Where | Notes |
|---|---|---|
| Myrmex | road (13,14), facing west | trainer, sight 3, mandatory sight line proven by world-act1's builder |
| Sostratos | road (20,6), facing east | trainer, sight 3 |
| Euthymia | road (26,3), facing east | trainer, sight 3 |
| The priestess | temple (11,9) | |

Set the three to `TRAINER_TYPE_NORMAL` once their `trainerbattle` scripts exist (the game reads the id from the script). Stubs already on their maps: the herm at road (22,3), landing (22,4), sets `FLAG_ICHOR_HERM_AEGINA` behind `ICHOR_STUB_HERM` (the engine still has to give Aigina's herm an id); altars behind `ICHOR_STUB_RITES`, Zeus on Oros (6,4) and Artemis at the temple (15,11); a dig spot at temple (18,11). The encounter tables are still Phase 2's levels 12–16: re-level them to BALANCE.md's Astyra row. **Update (world-act1, for the route standard):** world-act1 is adding grass, items, hidden items, surf and fishing tables at Astyra levels (32–35) and `"ichor_kind": "dungeon"` on the temple and Oros, and moving the three to the Astyra stage in `map_audit.py`'s `STAGES`. It is also placing **five more placeholder trainers** the same way as the first three (three more on the road, one at the temple, one on Oros; `TRAINER_TYPE_NONE`, one line, an `ICHOR_ACT2` comment with a suggested party). Batch 4 registers all **eight** at Astyra levels in Act II's ids and sets them to `TRAINER_TYPE_NORMAL`; the people, ant hills, altars, dig, gatekeeper lines and land-table levels stay Act II's.

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
