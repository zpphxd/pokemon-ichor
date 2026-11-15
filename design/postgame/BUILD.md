# The Aethos post-game: build plan

- **Owner:** the world-postgame session, branch `claude/world-postgame-9fad0c`. The director merges this branch into main; this session never merges into main.
- **What it builds:** the Aethos post-game, from the epilogue's last fade to the Prime Mover: the opening hooks, Olympia and the Olympiad, the sailing layer, the Labors, the Katabasis, the Odyssey, Atlantis, the summit and its Primordials, the theoxenia's extended tier (E6–E13 and the finale), the Aethos-side legendary quests, and the music cue lists.
- **Every post-game place on the Aethos chart is ours** (the director, 2026-11-14): Routes 31 (the Mani, Lakonia to Tainaron), 32 (the Sacred Way, Arkadia to Olympia), 33 (the western sea to Atlantis, Ithaka and Kerkyra) and 34 (Kaldera's sea to Rhodos), and Cape Tainaron, Olympia, Atlantis, Rhodos, Ithaka and Kerkyra.
- **What it doesn't:** the League, the credits and the epilogue itself (world-act3), the Oikoumene's chart and its ten lands (world-oikoumene), the shared engine systems (ichor-engine), the dex (aethos-dex).

**Read first, in this order:** `CLAUDE.md`, `design/MAP_DESIGN.md`, this file, `design/POSTGAME.md` (the frame), your epic's doc (`design/LABORS.md`, `design/UNDERWORLD.md` or `design/ODYSSEY.md`), `design/BALANCE.md` (the Aethos post-game row is wild 55–70, trainers 65–75, bosses 70–80; the Odyssey uses the Oikoumene row), `design/TERMS.md`, `design/ENGINE_API.md`, `design/postgame/ENGINE.md` (this branch's engine pieces), `design/MUSIC.md`, `tools/ichor/claim_ranges.md`. Then the model for your kind of work: world-act2's `design/phase3/BUILD.md` and its builders (`git show claude/world-act2-0a92e7:<path>`), world-act1's `design/phase2/BUILD.md`.

**Every decision in the post-game docs is settled** (the user, 2026-11-14): see the "Settled by the user" note at the top of each doc's decisions, and `design/OIKOUMENE.md` §13 (PG-1 to PG-41). In short: Persephone's return is the Orpheus moment and nobody returns from the dead; the five Titans and Briareus are freed; the suitors stay, comic, with Mom in control; Argos lives and joins you; the House of Night is built for 1.0; the legend castings are approved as a set; everything else takes its recommendation. **Christopher Nolan** is Odyssey crew (ODYSSEY §3). **Sam** (Apollo's disguise, E8) and **Cami** (Demeter's) are real people the user knows: keep their names exactly; their sprites are `OBJ_EVENT_GFX_ICHOR_SAM`, `_APOLLO`, `_CAMI` and `_DEMETER`.

---

## 1. The rules every agent follows

**The quality bar is the best ROM hacks.** The user's first priority for maps is that they look great. In their words (via the director, 2026-11-14): "We need all these maps created. All these routes created. Thoughtfully. Engaging. Well designed. To Pokémon standards, including plenty of grass and wild encounters etc. Items etc." So, on every map:
- **Grass:** forced bands across the path, plus plenty of optional grass with a reason to go in.
- **Wild tables by time of day:** `_Morning`, `_Day` and `_Night` land tables (`wild_encounters.json` supports them; see `gKallisteRoute1_Morning`), surf and fishing on water, rock smash at breakable rocks, all in BALANCE.md's band.
- **Items:** visible and hidden; every dead end pays.
- **Trainers** are checkpoints. **Every route** has a set piece and signs at its ends and forks.
- **The audit:** `tools/ichor/map_audit.py` and MAP_DESIGN §8 ("The route standard, in numbers") are coming to main. Every batch report must pass it on its maps.
- **Renders** of every map go to the director.
- **Every house is enterable,** with someone living there and something that happens: a gift, a trade, a quest, a minigame, a rematch, or lore that leads to a reward (MAP_DESIGN §2). Spread the rewards; open some after a later beat.
- **Every interior is a unique layout.** No room is copied from another, here or on any other branch.
- **Routes force you into grass,** with trainers as checkpoints, ledges toward the previous town, and an item in every dead end (MAP_DESIGN §1).
- **The seam rule:** the 6 rows (up/down) or 8 columns (left/right) nearest a connection with a different secondary tileset use only `aethos` metatiles, enforced in your builder's code (MAP_DESIGN §5).
- **Three render-and-critique passes** before you hand a map over. Render with `tools/ichor/render_map.py`, look at the PNG, fix what reads badly, and repeat. Commit the final render to `design/postgame/img/<map>.png`.
- **Text fits the box.** Two lines per box; check widths with `tools/ichor/text_width.py`. People sound like people. Use TERMS.md's words (Asclepeion, Agora, Pithos, Laurel, the Archon) and TERMS.md's casing.
- **Levels come from BALANCE.md.** Aethos post-game wild tables use **Aethos species only** (POSTGAME §4), except the myth-cast single encounters POSTGAME §4 lists. Trainers may field existing species. The Odyssey's sea and islands are at the Oikoumene's levels and may use any species.
- **No stone unturned.** Hidden items where curiosity goes, a set piece on every route, a myth in the land.

**Files and ownership.**
- Each agent works in its own worktree off this branch, on its own branch (`pg-b<batch>-<name>`), and touches only the files its row names.
- Shared registration files (`data/layouts/layouts.json`, `data/maps/map_groups.json`, `src/data/tilesets/*`, `include/constants/event_objects.h`, the sprite tables, `src/data/heal_locations.json`, `include/constants/opponents.h`'s post-game block) take small appended entries; this session resolves conflicts in them.
- **Parties and encounters are staged:** write your trainers' parties in `design/postgame/parties/<agent>.party` (the `.party` syntax, with the `TRAINER_ICHOR_*` names) and your wild tables in `design/postgame/encounters/<agent>.json` (each map's `wild_encounters.json` entry). This session folds them in. You may fold them in yourself on your branch to test, as long as you keep the staged copy as the source.
- **Flags:** claim only inside your sub-range (§3), with `python3 tools/ichor/claim.py --range LO-HI bankflag FLAG_ICHOR_<NAME> "comment"`. Hidden items take vanilla flags from 0x480–0x4BF (the sub-ranges in §3), because `bg_hidden_item_event` needs a vanilla flag at or above 0x1F4.
- **Trainer ids:** only your block (§3). Add `#define TRAINER_ICHOR_<NAME> <id>` in the post-game block of `opponents.h`; this session sets `TRAINERS_END_POSTGAME`.
- **Scripts** are Poryscript, `data/maps/<Map>/scripts.pory`. Shared post-game scripts go in `data/scripts/ichor_postgame_<topic>.pory`.
- **Maps that live on other branches** (Thyrsa, Astyra, Lakonia, Arkadia, Eleusa, Emporion, Kythera, Delphoi, Olympus): don't edit them. Write the scene as a script in `data/scripts/ichor_postgame_<topic>.pory`, with its object or coord event described in `design/postgame/PLACEMENTS.md` (map, x, y, graphics, flag, script), so the owner or the director can drop it in when the branches meet. On main's own maps (Elaia, Route 1, Akti and their interiors) edit directly, behind `FLAG_ICHOR_POSTGAME`.

**Gates and tests.**
- **Everything is gated on `FLAG_ICHOR_POSTGAME`,** which world-act3's epilogue sets as its last line. No post-game object, warp or encounter appears without it.
- **Tests don't need the story.** `tools/ichor/tests/pg_lib.lua` (batch 1) sets the post-game flag, builds a Lv 70 party, gives the relics and warps anywhere. Every map agent writes a headless Lua test of its beats (`tools/ichor/tests/pg_<area>.sh`), as the act batches do, and each epic gets one playthrough test (`pg_<epic>_playthrough.sh`).
- **Green after every merge:** `make -j$(sysctl -n hw.ncpu)`, `tools/ichor/smoke_test.sh < /dev/null` and `tools/ichor/tests/slice_playthrough.sh < /dev/null`, plus every `pg_*.sh`.
- **ROM:** note `make`'s memory line before and after your batch. Main is at about 66%; the post-game's whole budget is about 2 MiB (POSTGAME §7).
- **Stubs** for systems that haven't landed carry a grep-able tag, `ICHOR_STUB_<SYSTEM>`, with the fallback the doc gives.

---

## 2. Batches

PG-2's order: the sailing layer first, then Olympia, the Katabasis, the Labors, the Odyssey, Atlantis and the summit. The theoxenia and the legends ride along with the epics whose maps they use.

| # | Batch | Maps | Engine it needs | Status |
|---|---|---|---|---|
| 1 | **Set sail:** the post-game's opening hooks; the *Euploia* refitted (deck and below deck, every service aboard); the ship at sea, wind, stars and the helm's voyages; Route 33, the western sea; the crew who join at Akti; the music cue lists | 4 | IchorEpics; the sailing layer (this branch) | **in progress** |
| 2 | **Olympia, and the far lands' tilesets:** the Sacred Way (Route 32), the Altis, the Temple of Zeus, the Leonidaion, the Echo Stoa (Arena of Champions), Phidias's workshop, the Heraion; the Stadion, the Horse, the Palaestra and the Apple Course with their Brains; the Moment and Nike; E8 (Sam) and E9 (Hera's ford) on the Sacred Way; the `steppe` and `far_west` tilesets, early, for the Oikoumene | ~16 | The Frontier re-skin (this branch); the bull-leap timing (ichor-engine, E7) | |
| 3 | **The Katabasis:** the Mani Road (Route 31), Cape Tainaron, the Descent, the Acheron, the Styx, the Gate, the Meadows, the Crossroads, Lethe, Mnemosyne, the House of Hades and its Vault, the Bronze Gates, Tartarus and its five cells, Sisyphus's Hill, the Chasm, Elysium and its shore, the Ascent, the House of Night; the messages home; E11 (Hades) and E12 (Persephone) | 28 | The judgment, the don't-look-back rule, Lethe's fog (this branch); carried flame (ichor-engine) | |
| 4 | **The Labors, pairs 1–3:** Scene 0, the Heraion and Olympias; Nemea Glen and the Lion's Den; Lerna; the Ladon Ford; Erymanthos and the Snowfield; Augeas's farm and the Stable Yard; the Stymphalian Reeds | 10 | Flee-from-player movement, roamer flee, krotala (this branch); Asterion's charge and drifts, beam trace (ichor-engine) | |
| 5 | **The Labors, pairs 4–6, and the Kotinos:** the Bull's Shore and Crossing; Abdera and the Bistonian Plain; the Thermodon Road, Themiskyra, Hippolyta's Hall; the Western Cape, the Ocean Stream, the Strait of the Pillars, Erytheia, Geryon's Pasture; the Caucasus Crag, the Garden, Atlas's Ridge; Kerberos; the finale | 18 | Bull ride, cup ride, holding the sky (this branch); bull-leap, the no-shadow tell (ichor-engine) | |
| 6 | **The Odyssey:** the wine-dark sea (three sea maps), the Lotus Isle, the Cyclops's island and cave, Aiolia and its hall, Aiaia and Circe's hall, the Sirens' Strait, the Strait and Scylla's cave, Thrinakia, Proteus's islet (E13), Scheria, the Mist Beach, the homecoming in Elaia, and the theoxenia finale at home | 27 | Tornadus's storm, the Cyclops's eye, the Sirens' wax (this branch); the disguise state for Circe's forms and the beggar (ichor-engine) | |
| 7 | **Atlantis and the summit:** beyond the Pillars, the Nereids, the three rings (surface and underwater), the temple, the nursery, the abyss, the edge of the world (Kyogre); the Korykian cave (Groudon); the cloud meadows and Ouranos's sky (Rayquaza, Pegaunos); the summit path and the unmoved mover (Arceus); the colossi; Ichorin; the Loom and the Kleos page | 20 | Breath, the unmoved mover (this branch); the Scroll of Deeds' Kleos page (ichor-engine) | |
| 8 | **The rest of the theoxenia and the legends:** E6, E7, E10 as placements on the act maps; LEGENDS §7's Aethos post-game quests (Celebi, Heatran, Type: Null, Magearna, Marshadow, the satyr play); POSTGAME §3.4's Aethos homes; Time Fractures; Route 34 and Rhodos; Ithaka | ~8 | Time Fractures overlay (this branch) | |

The order inside a batch is parallel. Each batch ends with an integration pass here, a full green run, a push, and a report with renders to the director (§6).

---

## 3. Ranges and how they're split

From `tools/ichor/claim_ranges.md`: trainer ids **500–679**; bank flags **0x300–0x3BF** (192); daily flags **0x64–0x6F** (12); bank vars **18–23** (6; decimal, so `claim.py --range 0x12-0x17 bankvar …`); vanilla flags **0x480–0x4BF** (64, for hidden items). `claim.py`'s `--range` is always hex.

**Already claimed by this session** (use them; don't claim them again):

| Name | What |
|---|---|
| `FLAG_ICHOR_POSTGAME` | The post-game is live. world-act3's epilogue sets it last. Every post-game gate reads it. |
| `FLAG_ICHOR_GOT_EUPLOIA` | Nausikles has given you the ship (ODYSSEY scene 1) |
| `FLAG_ICHOR_ON_SHIP` | You're sailing the *Euploia*: the ship avatar is on (ENGINE.md) |
| `FLAG_ICHOR_AT_SEA` | You've rounded Maleia: the Wings don't work until you're home (ODYSSEY O1) |
| `FLAG_ICHOR_CREW_LAMPON`, `_DIKTYS`, `_KYDON`, `_PHEMIOS`, `_LYNKEUS`, `_IASO`, `_GLAUKIAS`, `_NOLAN`, `_OARSMEN` | The crew aboard (ODYSSEY §3). Nausikles and Alethea come with the ship. |
| `FLAG_ICHOR_SHIP_RAM`, `_SHIP_SAIL`, `_SHIP_KEEL` | The ship's upgrades (ODYSSEY §2): the bronze ram breaks sea rocks; the new sail adds a step downwind; the Phaeacian keel stops the Outer Sea's loop. Flags, not `IchorEpics.shipUpgrades` bits. |
| `FLAG_DAILY_ICHOR_SHIP_HEARTHFIRE`, `FLAG_DAILY_ICHOR_SHIP_NETS` | Lampon's daily Hearthfire, Diktys's daily haul |
| `VAR_ICHOR_POSTGAME` | The frame's state, 0–20: the opening, Atlantis, the summit (POSTGAME §6) |
| `VAR_ICHOR_ODYSSEY` | The Odyssey, 0–30 (ODYSSEY §15) |
| `VAR_ICHOR_KATABASIS` | The Katabasis (UNDERWORLD §13) |

**Sub-ranges.** Bank flag offsets, vanilla flags and trainer ids per batch; each batch's agents get theirs in the batch's section. Bank vars 21–23 are held back for the epics that ask.

| Batch | Bank flag offsets | Vanilla flags (hidden items) | Trainer ids |
|---|---|---|---|
| 1 | 0x300–0x32F | 0x480–0x487 | 500–509 |
| 2 | 0x330–0x34F | 0x488–0x48F | 510–539 |
| 3 | 0x350–0x36F | 0x490–0x49B | 540–569 |
| 4–5 | 0x370–0x39F | 0x49C–0x4AB | 570–629 |
| 6 | 0x3A0–0x3B3 | 0x4AC–0x4B5 | 630–664 |
| 7–8 | 0x3B4–0x3BF | 0x4B6–0x4BF | 665–679 |

**The range is short, and the director has the ask** (2026-11-14). The epics' own counts are about 140 story flags (LABORS ~40, UNDERWORLD ~30, ODYSSEY ~35, POSTGAME ~35), about 60 hide flags, and an item ball or two on each of about 130 maps, against 192 bank flags and 64 vanilla flags. Until it's answered:
- Per-epic state goes in `struct IchorEpics` (POSTGAME §6, ENGINE.md), not in flags.
- Hide flags for people who come and go on one map use `FLAG_TEMP_*`, set in `ON_TRANSITION` from the real state (temp flags clear on every map load).
- Item balls on batches 1–3 take bank flags from the batch's range; later batches wait for the answer.

---

## 4. Engine: what this branch builds, and what it asks for

New post-game systems are built here, in the conventions of ENGINE_API.md, documented in `design/postgame/ENGINE.md`, with `// Ichor postgame:` comments at every upstream hook. Shared systems that other sessions need too go to the ichor-engine session as asks. Each stubbed use is tagged `ICHOR_STUB_<NAME>` and uses the doc's fallback until the system lands.

**Built on this branch:**

| System | Batch | Needed by | Doc |
|---|---|---|---|
| `struct IchorEpics` in IchorSave (64 bytes from `reserved`, version 3) | 1 | Everything | POSTGAME §6 |
| The ship at sea: the *Euploia*'s 64×64 avatar in the surf state, boarding and landing, going below deck and back | 1 | Labors 8–11, the Odyssey, Atlantis, Route 33 | ODYSSEY §2, §4, §14 |
| Wind: the daily wind, speed by heading, the encounter rate, the sail's frames, the start menu's line | 1 | The same | ODYSSEY §4 |
| The at-sea lock on the Wings | 1 | The Odyssey | ODYSSEY O1 |
| The Great Bear at night on sea maps | 1 | The Outer Sea | ODYSSEY §4 |
| The helm's voyages: Nausikles's list of ports, each behind its flag, with a short crossing | 1 | Every far land; the Oikoumene adds its ports | §5 below |
| Post-game encounter overlays: shades on the roads at night (then Time Fractures, batch 8) | 1 | POSTGAME §1 | POSTGAME §1, §3.4 |
| The Olympiad: the Frontier engine re-skinned (Tower → Stadion, Factory → Horse, Arena → Palaestra, Pike → Apple Course), the Brains re-themed on ids 15–21, Aethos data tables, symbols and the prize exchange | 2 | Olympia | POSTGAME §3.1 |
| The judgment (reading the save), the don't-look-back rule, Lethe's forgetting fog, obols | 3 | The Katabasis | UNDERWORLD §5 |
| Flee-from-player movement, the roamer-style flee, the krotala's radius | 4 | Labors 1, 3, 6, 10 | LABORS §11 |
| The bull ride, the cup ride, holding the sky, light shafts | 5 | Labors 7, 10, 11, 12 | LABORS §11 |
| Tornadus's storm, the Cyclops's eye, the Sirens' wax, the Lotus's frozen clock | 6 | The Odyssey | ODYSSEY §14 |
| Breath underwater; the unmoved mover | 7 | Atlantis, the summit | POSTGAME §3.2, §3.3 |

**Asked of the other sessions** (sent 2026-11-14; each also serves another session). The answers so far:

| Ask | Who builds it | Needed by here | The name, once it lands | Fallback until then |
|---|---|---|---|---|
| **E7, the bull-leap timing** | world-act3: **built**, on origin/claude/world-act3-4e546d (`src/ichor_bull_leap.c`, API in its `design/phase4/ENGINE_ACT3.md`), not on main yet | The Moment (batch 2), Labor 7 (batch 5), Charybdis's fig tree (batch 6) | `special(Ichor_BullLeap)`: `VAR_0x8004` the moving object's local id, `0x8005` the line's tile `ICHOR_TILE(x, y)`, `0x8006` the window in frames (0 = 10), `0x8007` frames per tile (0 = 6); waits by itself; `VAR_RESULT` `ICHOR_LEAP_EARLY`/`_CLEAN`/`_LATE` (0/1/2, `include/constants/ichor_act3.h`). One call is one pass: for fail-forward, move the object back and call again with a wider window. | A YES/NO on the beat |
| **The carried flame** | ichor-engine, building now | Lampon (batch 1), Labor 2 (batch 4) | `setvar(VAR_0x8004, FLAME_x)`, `setvar(VAR_0x8005, <dry steps>)`, `special(Ichor_TakeFlame)`; `VAR_TEMP_2` steps left, `VAR_TEMP_3` the kind; `call(EventScript_IchorDraught)` puts it out. Asked for: in rain each step costs 2 (scripts give the dry budget); a lit brazier refills a flame; kinds `FLAME_HESTIA_SHIP` and `FLAME_LERNA` | A line of dialogue |
| **The disguise sprite** | with the director | Circe's forms, the beggar (batch 6) | `setvar(VAR_0x8004, OBJ_EVENT_GFX_…)`, `special(Ichor_SetPlayerGraphics)`, 0 to clear | An icon over the player |
| **E9, the beam trace** | world-act3: **built**, already generic | Labor 5 (batch 4) | `special(Ichor_TraceBeam)`: `VAR_0x8004` the source object (the beam leaves the way it faces), `0x8005` the first of six metatiles in a row (E–W, N–S, NE, NW, SE, SW): pass six water-channel metatiles. Turns are E8 mirror objects (`MOVEMENT_TYPE_ICHOR_MIRROR*`), so the sluice dials are mirror objects. `VAR_RESULT` the object it ends on or 0, end tile in `0x8006`/`0x8007`. At most 2 beams at once, 128 tiles, 16 turns, no crossing. | Fixed states per sluice |
| **Asterion's charge for the boar** | ichor-engine (built; asked for a hit script, `Ichor_AddDrift`, and a no-hearing bit) | Labor 4 (batch 4) | `special(Ichor_StartAsterion)` on any object | Scripted lanes |
| **The no-shadow opt-out, the follower's bow** | with the director (theoxenia is unassigned) | E6–E13, Labor 9 | — | Dialogue tells |
| **The Scroll of Deeds' pages** | with the director (unassigned) | Batches 5–7 | — | Flags only |
| **Digs** | with the director (excavation is unassigned) | Batch 3 | `EventScript_IchorDigSpot`, `EventScript_IchorDigFixed` (ENGINE_API §8); ask ichor-engine for index blocks | `ICHOR_STUB_DIG` |
| **The star chart** | ichor-engine | Cetus, Centaurus, Cancer | `setvar(VAR_0x8004, <index>)`, `special(Ichor_PlaceConstellation)` (sets `FLAG_ICHOR_CONSTELLATIONS_START + index`) | Set that flag |

**IchorEpics takes no version bump** (ichor-engine has version 3 for the forced omen and the held time of day): all its defaults are zero-valid, and `reserved` has always been zero-filled.

---

## 4a. Seams with the act sessions

| Seam | Agreed | Notes |
|---|---|---|
| **Route 32 ↔ Arkadia** (world-act2) | Arkadia (50×44) west edge; its road on rows 36–37, verges 35 and 38; 8 aethos-only columns each side. Our `right` connection to `MAP_ARKADIA` has offset *r* − 36, where *r* is the Sacred Way's road row on its east edge. | Their barrier hides on `FLAG_SYS_GAME_CLEAR`; we ask them to swap it for `FLAG_ICHOR_POSTGAME` at integration. We add our connection; the director joins them. |
| **Route 34 ↔ Kaldera** (world-act2, provisional) | `MAP_KALDERA_CALDERA_ROAD` (32×56)'s east edge, open water on rows 46–51 by the old port; 8 aethos-only columns. Closed until the post-game by whirlpools (Triton's Conch). | Their batch 6 hasn't started; they'll warn us if the rows move. |
| **Route 31 ↔ Lakonia** (world-act3) | Lakonia's south edge, roped off until the post-game. They send the columns and their 6 primary-only rows when Lakonia is built. | Route 25 enters Lakonia on the east; Route 26 leaves north. |
| **Lake Stymphalia** (Labor 6's reeds) | It's world-act3's Route 27, not world-act2's. | Ask world-act3 when batch 4 starts. |

## 5. Shared work with world-oikoumene

LABORS's far lands (Thrace, Themiskyra, the Caucasus, Erytheia and the Pillars, the Garden, Atlas's Ridge) and ODYSSEY's wine-dark sea are **this branch's maps** on the **Oikoumene's chart and map sections**. Agreed with world-oikoumene before each is built, and recorded here:

**Their map sections, adopted** (claude/world-oikoumene-950021 at 86f9c74609; `python3 tools/ichor/oikoumene_sections.py --list`; interiors share their parent's):
- **The Labors:** `MAPSEC_ABDERA`, `_BISTONIAN_PLAIN`, `_THEMISKYRA`, `_THERMODON_ROAD`, `_CAUCASUS` (our crag, their caves below it), `_PILLARS` (our Strait of the Pillars, their waters round it), `_OCEAN_STREAM`, `_ERYTHEIA`, `_HESPERIDES`, `_ATLAS_RIDGE`.
- **The Odyssey:** `MAPSEC_WINE_DARK_SEA` (both halves), `_OUTER_SEA` (with Proteus's islet), `_LOTUS_ISLE`, `_CYCLOPS_ISLE`, `_AIOLIA`, `_AIAIA`, `_SIRENS_ROCKS`, `_SCYLLA_STRAIT`, `_THRINAKIA`.
- **On Aethos sections:** the Western Cape, Maleia's waters, Scheria (Kerkyra) and the Mist Beach.

**Travel:** sea lanes on either chart are real `MAP_TYPE_OCEAN_ROUTE` maps sailed in the ship (their Hellespont and Pontic lanes connect to Route 20 and Route 34). The helm's SET A COURSE is fast travel between ports already reached, so every port has a gangplank and a voyage row. Until our table is on main their ports have a SAIL HOME Nausikles, tagged `ICHOR_STUB_SHIP`.

**Tilesets we share:** LABORS's `steppe` (Thrace, Themiskyra; their Scythia) and `far_west` (Erytheia, the Garden; their Far West) are drawn in **our batch 2**, ahead of their batch 4.

**Seams and warps still to fix** (each when its map is built): their Hellespont lane's landing → Abdera's harbor; their Pontic Coast → Themiskyra's harbor; a cave-mouth tile on our Caucasus crag for their caves; Gadeira and their Atlantic Shore → our Strait of the Pillars; our Atlas's Ridge → their Atlas foothills; quays on our wine-dark sea for their Kroton, Cumae and Ogygia; Route 34's edge → their Pharos waters (primary-only).

| What | Ours | Theirs |
|---|---|---|
| Map sections for the far lands and the sea | We use them | They name and place them on the chart |
| The helm's ports (`src/data/ichor_voyages.h`) | The table, the menu and the Aethos-side ports | Their ports, appended as rows |
| Wings crossing targets (THE OIKOUMENE, AETHOS) | — | Theirs (OIKOUMENE §2) |
| Abdera, Themiskyra as Wings landings | Their heal locations | The chart cells |
| Seams where our maps meet theirs (the Strait of the Pillars ↔ the waters of the Strait; Themiskyra ↔ the Black Sea) | Agreed per seam, recorded in that batch | |

---

## 6. Reports

At the end of every batch, this session:
1. merges the agents' branches here and runs the full green set;
2. pushes the branch to origin;
3. writes the batch's result in its section below (what's built, deviations, what's left, the ROM line);
4. puts the renders in `design/postgame/img/`, sends them to the user, and leaves the report in the shared notes folder (`world-postgame.md`) for the director.

---

## Batch 1: set sail

### Who builds what

| Agent | Builds | Files it owns |
|---|---|---|
| **sail-engine** | `struct IchorEpics` (POSTGAME §6, version 3); the ship at sea; wind; the at-sea lock; the Great Bear; going below deck and back; the helm's voyages (the table and `EventScript_IchorHelm`); the post-game encounter overlay (shades at night); `tools/ichor/tests/pg_lib.lua` and `pg_sailing.sh`; `design/postgame/ENGINE.md` | `include/ichor_save.h` and `src/ichor_save.c` (the epics field only), `src/ichor_sailing.c`, `include/ichor_sailing.h`, `include/constants/ichor_sailing.h`, `src/data/ichor_voyages.h`, `data/scripts/ichor_postgame_sailing.pory`, the `// Ichor postgame:` hooks in upstream files, `tools/ichor/tests/pg_lib.lua`, `pg_sailing*` |
| **euploia** | The `euploia` secondary on `oikos` or `aethos` (world-act1's `trireme` art as its base, `git show claude/world-act1-6d11b7:tools/ichor/art/...`; add the bunk, hearth, stall, Pithos, Poseidon's altar, trophy shelf, chart table, nets, rail); `MAP_EUPLOIA_DECK` (24×12) and `MAP_EUPLOIA_BELOW` (20×10) with every service in ODYSSEY §2 (crew appear only when aboard); the trophy shelf's seven keepsakes as `FLAG_TEMP` displays over the Odyssey's flags (stubbed until batch 6) | `tools/ichor/art/euploia_*.py`, `data/tilesets/secondary/euploia/`, `tools/ichor/maps/euploia.py`, the two maps, `design/postgame/TILES_euploia.md` |
| **akti** | The post-game's opening on main's maps: Kleon at Elaia's well (LABORS scene 0's first line), the heralds of the truce (`EventScript_IchorHerald`, a line per town), Nausikles and Alethea on Akti's quay (ODYSSEY scene 1; the gangplank boards the ship), Lampon (carried flame from Hestia's hearth to the quay, stubbed), Diktys (his boat), Glaukias (the Fisher's house); the other crew's recruitment scenes as scripts with placements (Kydon at Emporion, Phemios at Thyrsa, Lynkeus and Iaso at Astyra, Nolan at Lechaion, the oarsmen at Lakonia); the heralds' and the shades' placements for the act maps | the post-game objects and scripts on `ElaiaVillage*`, `KallisteRoute1`, `AktiTown*` (behind `FLAG_ICHOR_POSTGAME`), `data/scripts/ichor_postgame_opening.pory`, `data/scripts/ichor_postgame_crew.pory`, `design/postgame/PLACEMENTS.md` |
| **westsea** | Route 33, the western sea (AETHOS_MAP: Tainaron to Atlantis, Ithaka and Kerkyra), as one or two sea maps up to 80×80 on `aethos` (or a small `westsea` secondary if the rocks and wrecks need one): free sailing with currents, sea rocks for the bronze ram, whirlpools for Triton's Conch, floating items in the lee of rocks, the fog bank south-west toward the Pillars (batch 7), the landings for Cape Tainaron (batch 3), Ithaka and Kerkyra (batch 6) as warps to stub rooms; its trainers (sailors and divers at sea, on rafts and rocks); its encounters | `tools/ichor/maps/westsea.py` (and `tools/ichor/art/westsea_*.py` if it draws), the Route 33 maps, `design/postgame/parties/westsea.party`, `design/postgame/encounters/westsea.json` |
| **sprites** | The *Euploia* at sea (64×64, four directions, two frames, sail full and slack); the Great Bear's stars (a small sprite); Christopher Nolan, Phemios and Lynkeus (16×32); a herald of the truce (16×32); and, ahead of batch 2, Olympia's cast: Achilles, Odysseus, Hippolyta, Atalanta, Ariadne, Olympias, Paionios (walkers; the five Brains' portraits) | `graphics/object_events/pics/ichor/pg_*`, `graphics/trainers/front_pics/ichor_pg_*`, their table entries, `tools/ichor/art/sprites_pg*.py`, `design/postgame/SPRITES.md` |
| **this session** | This file, the claims, the music cue lists (`design/postgame/MUSIC_CUES.md`), the integration, the batch test | `design/postgame/*.md`, `design/postgame/parties/`, `design/postgame/encounters/` |

### Ids

**Species:** until the dex is on main, `include/constants/ichor_species_stubs_postgame.h` defines every Aethos species by its dex name (`SPECIES_OBOLORN` and the rest) as a same-type vanilla stand-in, so parties and tables use the real names now.

**Bank flags:** this session 0x300–0x30F (claimed above); akti 0x310–0x31F; euploia 0x320–0x324; westsea 0x325–0x32D; sail-engine 0x32E–0x32F. **Vanilla flags (hidden items):** westsea 0x480–0x485, akti 0x486–0x487. **Trainer ids:** westsea 500–505; 506–509 spare. **Daily flags:** the two above; akti may take one more.

### Interfaces fixed now

So the five agents can build at once:

| Name | Owner | What |
|---|---|---|
| `MAP_EUPLOIA_DECK`, `MAP_EUPLOIA_BELOW` | euploia | Deck warp 0 is the hatch down (below's warp 0 is the ladder up). The deck's steering oars at the stern, Nausikles beside them, run `EventScript_IchorHelm`. |
| `EventScript_IchorBoardShip` | sail-engine | A landing's gangplank (a coord or bg event on the quay tile). Asks "Board the Euploia?"; YES puts you on the sea map named by the landing's row in `src/data/ichor_voyages.h`, in the ship, or onto the deck when the landing has no sea map. |
| `EventScript_IchorLand` | sail-engine | A bg event on a sea map's landing tile, `VAR_0x8004` = the port: "Go ashore at …?", then the port's quay, ship mode off |
| `EventScript_IchorLeaveShip` | sail-engine | The deck's gangplank: back to the quay of the port where she's moored |
| `EventScript_IchorHelm` | sail-engine | Nausikles at the helm: "TAKE HER OUT" (back to the sea where you went below), "CAST OFF" (moored at a port with a sea map), "SET A COURSE" (the ports list), "THE WIND?" and "STAY". |
| `specialvar(VAR_RESULT, Ichor_IsStarsOut)` | sail-engine | Night, at sea, in the ship: the Great Bear is up |
| `ICHOR_SHIP_GFX`, `ICHOR_SHIP_GFX_SLACK` | sail-engine | The avatar's graphics, defined to a stand-in until the sprites agent's `OBJ_EVENT_GFX_ICHOR_EUPLOIA`/`_SLACK` merge |
| `special(Ichor_GoBelowDeck)`, `special(Ichor_ReturnToSea)` | sail-engine | At sea, the Relic Ring's DECK entry saves your position and warps to `MAP_EUPLOIA_DECK`; the helm's TAKE HER OUT brings you back. |
| `specialvar(VAR_RESULT, Ichor_GetWind)`, `special(Ichor_SetWind)` | sail-engine | Wind as `ICHOR_WIND_*` direction and strength (`include/constants/ichor_sailing.h`) |
| `VOYAGE_*` ids | sail-engine | One per port: `VOYAGE_AKTI`, `VOYAGE_ROUTE33`, `VOYAGE_CAPE_TAINARON`, `VOYAGE_KNOSSA`, `VOYAGE_LECHAION`, `VOYAGE_KALDERA`, then the Labors' and the Oikoumene's as they're built |
| `MAP_ROUTE33_WESTERN_SEA` (and `_SOUTH` if two maps) | westsea | `MAPSEC_AETHOS_ROUTE_33`, `MAP_TYPE_OCEAN_ROUTE`; its landing rows in `ichor_voyages.h` are the westsea agent's to add |
| `OBJ_EVENT_GFX_ICHOR_EUPLOIA`, `_NOLAN`, `_PHEMIOS`, `_LYNKEUS`, `_HERALD`, `_ACHILLES`, `_ODYSSEUS`, `_HIPPOLYTA`, `_ATALANTA`, `_ARIADNE`, `_OLYMPIAS`, `_PAIONIOS` | sprites | Until they land, use any existing walker and the `ICHOR_STUB_PG_SPRITES` tag |
| `EventScript_IchorHerald` | akti | `VAR_0x8004` = the town (`ICHOR_HERALD_*`), so each town's herald has its own line |

### Result

*(written when the batch is merged)*
