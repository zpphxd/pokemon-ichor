# Post-game placements on other branches' maps

The post-game's scenes for towns that live on other branches are written as scripts on the post-game branch. This file says where each one's object or event goes, so the map's owner or the director can drop it in when the branches meet (BUILD.md §1, "Maps that live on other branches").

- **Gate.** Everything waits for `FLAG_ICHOR_POSTGAME`. A person who appears only in the post-game hides behind a `FLAG_TEMP_*` flag, set in the map's `ON_TRANSITION` while the post-game is off (or once they've gone). No permanent hide flag is spent. Each table names a free temp flag for its map; pick another if the map has taken it since.
- **The snippet.** For a new person with hide flag `F` and a condition `C` under which they're gone:
  ```
  // in the map's MAP_SCRIPT_ON_TRANSITION
  if (!flag(FLAG_ICHOR_POSTGAME) || C) {
      setflag(F)
  }
  ```
- **A branch** in an existing person's script goes at its very top, except in a trainer's script, which must open with its `trainerbattle`; there the branch goes right after it.
- **Sprites.** The heralds wear `OBJ_EVENT_GFX_ICHOR_HERALD`, and Phemios, Lynkeus and Nolan their own sprites, once the sprites agent's work merges. Until then, use the stand-in named in the table (`ICHOR_STUB_PG_SPRITES`). Phaedon and Elpis have no sprites anywhere yet.
- **Scripts** are in `data/scripts/ichor_postgame_opening.pory` (the heralds, Elaia, Akti) and `data/scripts/ichor_postgame_crew.pory` (the crew).
- **Coordinates.** Where a town is built, x and y were checked against its map on the named branch: walkable, clear of its people, warps and triggers. Where it isn't built yet, the place is described from AETHOS_MAP and the act's script, and the owner picks the tile.

Each section in this file belongs to the agent who added it. The westsea agent's Route 33 section is its own.

---

## Akti's opening: what is already placed on main's maps

These are placed on this branch, for reference when another branch merges over the same maps. World-act1 also adds to Elaia and Akti (Phase 2 beats 9A and 9B). Its quay scene uses `VAR_TEMP_4` on the same x = 10 line, so the post-game takes `VAR_TEMP_5` and `VAR_TEMP_6` there. Its Lakonian rower hides once you board in Act I.

| Map | x, y | Graphics | Movement | Flag | Script | What |
|---|---|---|---|---|---|---|
| `MAP_ELAIA_VILLAGE` | 24, 18 | `KLEON` | face down | `FLAG_TEMP_18` (until his scene) | `EventScript_IchorPg_KleonWell` | Kleon on the well's edge with Daphne's scroll (LABORS scene 0). act2's `KLEON_SEATED` would sit him down. |
| `MAP_ELAIA_VILLAGE` | 15, 23 | `AUGUR` (herald stand-in) | face down | `FLAG_TEMP_19` | `EventScript_IchorHerald_Elaia` | The herald in the square |
| `MAP_AKTI_TOWN` | 14, 20 | `AUGUR` (herald stand-in) | face down | `FLAG_TEMP_18` | `EventScript_IchorHerald_Akti` | The herald in the plaza |
| `MAP_AKTI_TOWN` | 6, 8 | `ALETHEA` | face down | `FLAG_TEMP_19` (until the ship is yours) | `EventScript_IchorPg_AletheaOnDeck` | Alethea on the Euploia's deck |
| `MAP_AKTI_TOWN` | 8, 10 | `ACOLYTE_M` | face right | `FLAG_TEMP_1A` (only while the fire is coming) | `EventScript_IchorPgCrew_LamponQuayTalk` | Lampon waiting for Hestia's fire |
| `MAP_AKTI_TOWN` | 5, 9 | (Nausikles, moved) | face right | — | `EventScript_IchorPg_Nausikles` | Nausikles on the bollard: `setobjectxyperm` in the post-game |
| `MAP_AKTI_TOWN` | 10, 9–11 | coord, `VAR_TEMP_5` = 1 | | | `EventScript_IchorPg_AktiShipRow9`… | ODYSSEY scene 1 |
| `MAP_AKTI_TOWN` | 10, 9–11 | coord, `VAR_TEMP_6` = 1 | | | `EventScript_IchorPgCrew_LamponQuayRow9`… | Hestia's fire reaches the quay (`ICHOR_STUB_CARRIED_FLAME`) |
| `MAP_AKTI_TOWN` | 7, 9 | coord, `VAR_TEMP_5` = 2 | | | `EventScript_IchorPg_AktiGangplank` | The gangplank: `EventScript_IchorBoardShip`, `VOYAGE_AKTI` |
| `MAP_AKTI_TOWN` | 9, 25 | (Diktys) | | `FLAG_TEMP_1B` (once crew) | branch to `EventScript_IchorPgCrew_Diktys` | Diktys and his boat |
| `MAP_AKTI_TOWN_ASCLEPEION` | 7, 2 | `ELDER_M` (Phaedon stand-in) | face down | `FLAG_TEMP_18` | `EventScript_IchorPg_Phaedon` | Phaedon at the counter. The healer moves to (11, 3) and still answers a whiteout. |
| `MAP_AKTI_TOWN_ASCLEPEION` | 0, 9 | `KID_F` (Elpis stand-in) | face right | `FLAG_TEMP_19` | `EventScript_IchorPg_Elpis` | Elpis by the cots |
| `MAP_AKTI_TOWN_FISHERS_HOUSE` | 3, 2 / 6, 6 | (Glaukos / Glaukias) | | `FLAG_TEMP_18` / `FLAG_TEMP_19` | branch to `EventScript_IchorPgCrew_Glaukias` | The sea has kept Glaukos; Glaukias begs to sail |
| `MAP_AKTI_TOWN_TEMPLE_OF_HESTIA` | 8, 15 | (Lampon) | | `FLAG_TEMP_18` (once crew) | branch after his `trainerbattle` | Lampon asks for the fire; the great hearth lights his pot |
| `MAP_AKTI_TOWN_AGORA` | 3, 2 | (Demeas) | | | branch to `EventScript_IchorPgCrew_DemeasRope` | A coil of rope, on Diktys's tab |
| `MAP_KALLISTE_ROUTE1` | 7, 25 | (the olive farmer) | | | branch to `EventScript_IchorPgCrew_OliveFarmerRoot` | The Big Root for Diktys's boat |

Elaia's people (Mom, Kydippe, Glykera, Kimon, Halia, Korinna, Philon, Gylippos, the festival pair, Daphne and the kraters) and Akti's (the healer, Hydna, the islet fisher, the fishwife, the pilgrim, the quay and Fisher's house signs) have one-line branches into `ichor_postgame_opening.pory`.

---

## The heralds of the truce

POSTGAME §1: "The truce is declared. Every road to Olympia is safe." One herald (a *spondophoros*) per town in AETHOS_MAP's list. Each runs its town's wrapper, which sets `VAR_0x8004` to an `ICHOR_HERALD_*` id (`include/constants/ichor_postgame.h`) and goes to `EventScript_IchorHerald`, so each tells the road to Olympia from where you stand.

All: graphics `OBJ_EVENT_GFX_ICHOR_HERALD` (until the sprites merge, `OBJ_EVENT_GFX_ICHOR_AUGUR` stands in), face down, no movement, hidden while `FLAG_ICHOR_POSTGAME` is clear.

| Town | Map (branch) | x, y | Flag | Script | Where, and why |
|---|---|---|---|---|---|
| Elaia | `MAP_ELAIA_VILLAGE` (main) | 15, 23 | `FLAG_TEMP_19` | `EventScript_IchorHerald_Elaia` | **Placed.** The square's south end, by the finish line |
| Akti | `MAP_AKTI_TOWN` (main) | 14, 20 | `FLAG_TEMP_18` | `EventScript_IchorHerald_Akti` | **Placed.** The plaza, seen from the road up from Route 1 |
| Emporion | `MAP_EMPORION_CITY` (world-act1) | 26, 39 | `FLAG_TEMP_18` | `EventScript_IchorHerald_Emporion` | Beside the harbor road where it enters the city (x 21–25), the way in from the Euploia |
| Eleusa | `MAP_ELEUSA_VILLAGE` (world-act1) | 20, 25 | `FLAG_TEMP_18` | `EventScript_IchorHerald_Eleusa` | The main street, between the Agora (17, 23) and the Telesterion road |
| Thyrsa | `MAP_THYRSA_CITY` (world-act2) | 28, 18 | `FLAG_TEMP_18` | `EventScript_IchorHerald_Thyrsa` | Where the Dionysia's herald stood. His own object hides on `FLAG_ICHOR_DIONYSIA_DONE`, so this is a new object on the same tile. Thyrsa uses `FLAG_TEMP_11`–`13`. |
| Arkadia | `MAP_ARKADIA` (world-act2; not built yet) | — | — | `EventScript_IchorHerald_Arkadia` | **Not built** (the branch's `MAP_ARKADIA` is a stand-in layout). At the west gate, where the road leaves for Route 32 down the Alpheios |
| Astyra | `MAP_ASTYRA` (world-act2; not built yet) | — | — | `EventScript_IchorHerald_Astyra` | **Not built.** In the Agora, beside the herald's stone where Kerykos read the Archon's word (phase3 SCRIPT beat 48) |
| Kaldera | `MAP_KALDERA` (not built yet) | — | — | `EventScript_IchorHerald_Kaldera` | **Not built.** By the harbor, where ships leave west for Kythera |
| Kythera | `MAP_KYTHERA_PAPHIA` (world-act3) | 36, 19 | `FLAG_TEMP_18` | `EventScript_IchorHerald_Kythera` | Between the Agora (33, 16) and the Asclepeion (38, 16), clear of the girl (34, 20) and Hermes (41, 18) |
| Amnisos | `MAP_AMNISOS` (not built yet) | — | — | `EventScript_IchorHerald_Amnisos` | **Not built.** On the quay, where ships leave for Kythera |
| Lakonia | `MAP_LAKONIA` (world-act3; not built yet) | — | — | `EventScript_IchorHerald_Lakonia` | **Not built.** The agora in the middle of town, by the chained statue of Enyalios (phase4 SCRIPT's Lakonia layout) |
| Delphoi | `MAP_DELPHOI` (not built yet) | — | — | `EventScript_IchorHerald_Delphoi` | **Not built.** At the foot of the Sacred Way up to the temple |
| Mt. Olympus | `MAP_MOUNT_OLYMPUS` (not built yet) | — | — | `EventScript_IchorHerald_Olympus` | **Not built.** Outside the Pantheon's gate |
| Cape Tainaron | `MAP_CAPE_TAINARON` (batch 3) | — | — | `EventScript_IchorHerald_Tainaron` | Where Route 31 reaches the cape, before the cave gate |
| Olympia | the Altis (batch 2) | — | — | `EventScript_IchorHerald_Olympia` | At the entrance to the Altis, greeting arrivals |
| Atlantis | — | — | — | — | None: the city is under the sea |

---

## The crew who join elsewhere

ODYSSEY §3. Every scene waits for the ship (`FLAG_ICHOR_GOT_EUPLOIA`). Before it, each person has a line that points west. Once a crew flag is set, the euploia agent shows that person aboard, so their town copy should hide (the condition `C` in the snippet above).

### Kydon, quartermaster: Emporion's Agora

Buy one jar of Knossan honey (¥300, the Honey item); he decides he likes you.

| Map (branch) | x, y | Graphics | Movement | Flag | Script |
|---|---|---|---|---|---|
| `MAP_EMPORION_CITY` (world-act1) | 18, 29 | his own object, `LOCALID_EMPORION_KYDON` | face down | add `FLAG_TEMP_18`, set once `FLAG_ICHOR_CREW_KYDON` (he's aboard) | at the top of `EmporionCity_EventScript_Kydon`: `if (flag(FLAG_ICHOR_POSTGAME) && flag(FLAG_ICHOR_GOT_EUPLOIA) && !flag(FLAG_ICHOR_CREW_KYDON)) { goto(EventScript_IchorPgCrew_Kydon) }` |

**Rope for Diktys.** Diktys's coil of rope comes from Demeas at Akti's Agora, as a line and a flag (`FLAG_ICHOR_PG_GOT_ROPE`). ODYSSEY has it from Emporion's Agora; the general stallkeeper there (`LOCALID_EMPORION_GENERAL_STALLKEEPER`, 19, 26) could also hand it over later, with the same condition and a script like `EventScript_IchorPgCrew_DemeasRope`.

### Phemios, bard: Thyrsa's theater

Sit through his rehearsal of *The Return of Odysseus* and tell him the truth (three choices; "TOO MANY SHIPS" wins).

| Map (branch) | x, y | Graphics | Movement | Flag | Script |
|---|---|---|---|---|---|
| `MAP_THYRSA_THEATER` (world-act2) | 22, 12 | `OBJ_EVENT_GFX_ICHOR_PHEMIOS` (stand-in `YOUTH_M`) | face down | `FLAG_TEMP_1C` (the theater uses `_11`–`_1B`); `C` = `FLAG_ICHOR_CREW_PHEMIOS` | `EventScript_IchorPgCrew_Phemios` |

The orchestra, east of the thymele, clear of the Dionysia's cast (who hide after it).

### Lynkeus, lookout: Astyra's harbor (Phaleron)

He names three things in the harbor he can see and you can't. **Not built yet:** `MAP_ASTYRA_PHALERON` (36×24, phase3 SCRIPT). ODYSSEY puts him on the harbor watchtower; Phaleron's plan has none, so the tower is a small piece for the map's owner at the root of the stone quay, or Lynkeus stands on the quay's end.

| Map | Where | Kind | Flag | Script |
|---|---|---|---|---|
| `MAP_ASTYRA_PHALERON` | the watchtower at the quay's root (or the quay's end) | object, `OBJ_EVENT_GFX_ICHOR_LYNKEUS` (stand-in `SAILOR`), face down | `C` = `FLAG_ICHOR_CREW_LYNKEUS` | `EventScript_IchorPgCrew_Lynkeus` |
| `MAP_ASTYRA_PHALERON` | the dune grass where the beach bends | bg event (sign) | — | `EventScript_IchorPgCrew_LynkeusCoin` (a Relic Copper) |
| `MAP_ASTYRA_PHALERON` | the harbor shrine of Poseidon, hung with shells | bg event: branch the shrine's own sign script into it | — | `EventScript_IchorPgCrew_LynkeusPearl` (a Big Pearl) |
| `MAP_ASTYRA_PHALERON` | the quay stones under the *Paralos*'s gangplank | bg event (sign) | — | `EventScript_IchorPgCrew_LynkeusRing` (a Nugget) |

Each thing keeps a plain line until he has asked (`FLAG_ICHOR_PG_LYNKEUS_ASKED`) and after it's found (`_FOUND_1`–`_3`).

### Iaso, healer: Astyra's Asclepeion

She's the young healer who worked under Phaedon in Act II ("He never takes a fee from children"). Phaedon recommends her if the Katabasis is done (`VAR_ICHOR_KATABASIS >= ICHOR_PG_KATABASIS_DONE`, tagged `ICHOR_STUB_PG_FLAGS` for batch 3); otherwise help her with three patients. **Not built yet:** `MAP_ASTYRA_ASCLEPEION` (phase3 SCRIPT, Part 2: the counter faces the door; the incubation stoa's pallets run down the east side).

| Map | Where | Graphics | Flag | Script |
|---|---|---|---|---|
| `MAP_ASTYRA_ASCLEPEION` | behind the counter, Phaedon's old place | `HEALER` | `C` = `FLAG_ICHOR_CREW_IASO` (a healer from Astyra takes the counter then) | `EventScript_IchorPgCrew_Iaso` |
| `MAP_ASTYRA_ASCLEPEION` | the first pallet of the stoa | `HOPLITE` | post-game only | `EventScript_IchorPgCrew_IasoPatient1` (wants a Paralyze Heal) |
| `MAP_ASTYRA_ASCLEPEION` | the second pallet | `FISHER` or `WOMAN` | post-game only | `EventScript_IchorPgCrew_IasoPatient2` (an Antidote) |
| `MAP_ASTYRA_ASCLEPEION` | the third pallet | `KID_M` | post-game only | `EventScript_IchorPgCrew_IasoPatient3` (an Awakening) |

Act II's own pallet patient, old soldier and young healer can stay or step aside, as the owner prefers.

### Christopher Nolan, dramatist: Lechaion, beside the Diolkos

ODYSSEY §3's scene, word for word; he joins once the *Euploia* is moored at Lechaion (`Ichor_GetShipPort` = `VOYAGE_LECHAION`; until the sail engine merges, a stub that always answers `VOYAGE_AKTI`, tagged `ICHOR_STUB_SAILING`). World-act1's harbor district, `MAP_EMPORION_HARBOR`, is Lechaion: its `isthmos` tileset holds the port and the Diolkos, and the *Euploia* berths at (30, 16).

| Map (branch) | x, y | Graphics | Movement | Flag | Script |
|---|---|---|---|---|---|
| `MAP_EMPORION_HARBOR` (world-act1) | 20, 12 | `OBJ_EVENT_GFX_ICHOR_NOLAN` (stand-in `MAN`) | face left, watching the hauled ship | `FLAG_TEMP_18`; `C` = `FLAG_ICHOR_CREW_NOLAN` | `EventScript_IchorPgCrew_Nolan` |

The Diolkos track and the ship on its cradle are the isthmos pieces at (15–19, 11–12); he stands at their east end. The stevedore at (21, 11) wanders; give him a fixed facing if he crowds Nolan.

### The twelve Lakonian oarsmen: Lakonia's battle school

Kleon lends them: "They row better than they fight. Don't tell them." **Not built yet:** `MAP_LAKONIA` (52×42, phase4 SCRIPT): the battle-school ring is the round sand floor in the agoge's yard, north-west of town.

| Map | Where | Graphics | Flag | Script |
|---|---|---|---|---|
| `MAP_LAKONIA` | inside the battle-school ring, visiting his mother | `KLEON` | post-game only | `EventScript_IchorPgCrew_Oarsmen` (sets `FLAG_ICHOR_CREW_OARSMEN`) |
| `MAP_LAKONIA` | two or three oarsmen on the ring's low wall | `HOPLITE` or the act's `CADET` | `C` = `FLAG_ICHOR_CREW_OARSMEN` | a one-line script of the owner's; one of them is the "OARSMAN: We heard that." voice |

---

## Shades on the roads

POSTGAME §1's shades are small gray Obolorn in every route's night table. They come from the sail-engine agent's post-game encounter overlay, so they need no placements here.
