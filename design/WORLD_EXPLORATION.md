# World exploration: what to find, and what to come back for

This file plans the whole of Aethos as one explorable world: what each region shows on the first visit, what it keeps closed, which relic opens it, and what waits behind. It extends `SYSTEMS.md` §1 ("Relic gates: shown early, opened later") from one gate per relic to a full set per region, and it proposes the missing climbing relic.

- **The user's direction (2026-11-17):** "We need to think about the map and land as a whole: what will be there to explore, hidden parts you need to come back to later. Almost every cave needs more that you can go back to with rock climb, surf, etc." And: "where there is more story and adventures, better Pokémon and stronger too."
- **Earlier direction** (`IDEAS.md`): every route longer and more engaging, varied terrain, much more relic use; bare stops become temples, shrines or outcamps that can carry later quests.
- **Sources this file follows:** `PITCH.md` (story and post-game), `AETHOS_MAP.md` (every place), `SYSTEMS.md` §1 (relics), `MAP_DESIGN.md` §1 and §3, `BALANCE.md` (levels), `LABYRINTH.md` §9 (the Minoan vaults), `LEGENDS.md` (post-game legends), `OIKOUMENE.md` §2, `design/phase2/SCRIPT.md` ("Return to Kalliste"), the dex yamls in `design/dex/species/`, and `research/LAZARUS.md`.
- **Status words.** **Built**: in the game now. **Gate built**: the obstacle or its tease is on a built map, but the place behind it isn't. **Designed**: written up in another doc, not built. **In progress**: on a map being rebuilt now (Routes 7–14, Lebadeia, Kirrha, Aigion, Nemea). **Proposed**: new in this file, for the director and map builders to accept or cut.

## Contents

1. The principle
2. A climbing relic: Pan's Crook (proposal)
3. The gate vocabulary
4. Levels behind a gate
5. Region by region
6. The matrix
7. Return loops
8. Build order
9. Decisions for the director and the user

---

## 1. The principle

- **Every region rewards a return.** No region is finished on the first visit.
- **Almost every cave has a back section** the player can see but not enter: a ledge above, a pool below, a sealed door, a dark side passage. A later relic opens it.
- **Every route hides one or two such places,** off the main line: a cliff with handholds, an islet, a boulder over a cave mouth.
- **The player sees or hears what's behind first.** A glint, an item ball, a sign, an NPC who wonders aloud, a sound. MAP_DESIGN §1: "What's behind should be visible, or hinted at."
- **Returns pay out,** and the significant ones carry more than an item:
  - **a small story or adventure:** a side quest, a myth episode, an NPC with a thread, or lore that deepens the main plot;
  - **better, stronger Pokémon:** rarer species, evolved forms, higher levels than the area around them, and the place's own encounters (legend leads, rare Aethos species);
  - and also items, a shortcut, Favor, or a quest start.
- **Levels follow the relic, not the region.** A gate opens at the levels of the act in which its relic arrives (§4), so a Conch return to Kalliste is an Act II fight, not a Prologue one.
- **The main path never waits on a return.** Every gate in this file is optional unless `SYSTEMS.md` already makes it the main path.

---

## 2. A climbing relic: Pan's Crook (built 2026-11-18)

> **Built:** the item, the faces (Skiron's limestone and Arkadia's grey crag), "Noon in Arkadia", and the faces on Route 13 and Route 9 (ENGINE_API §2). The other hooks stay later; see "Faces placed" at the end of this section. The original proposal follows.
>
> **Proposal for the director and the user to approve.** It adds a 14th relic and reverses `SYSTEMS.md` §13's ruling that Rock Climb stays optional-only as Dionysus's gift II. The user's new direction ("rock climb, surf, etc.") asks for climbing gates across the world, which a Favor gift can't carry: a gate has to open for every player at a known point in the story.

### The pick

**Pan's Crook** (`ITEM_PANS_CROOK`). The shepherd's crook (the *kalaurops*) Pan carries on vases and reliefs, given by Pan himself in Arkadia.

| Candidate | For | Against | Verdict |
|---|---|---|---|
| **Pan's Crook** | Pan is Arkadia's god, goat-footed, at home on crags. Arkadia already has **Pan's grotto** scripted with its "sudden, total panic" tease (`data/maps/Arkadia/scripts.pory`), and a goatherd's house (`Arkadia_GoatherdHouse`). Pan recurs across the map (his caves under the Akropolis and on Parnassos, his meeting with the runner before Marathon), so the relic seeds a quest chain. Goats are the climbing animal of Greece, and the Amalthea line (Eripip, Kerazap, Kerastorm) is a cliff goat. | Pan is not one of the Twelve with a rite, so there's no Favor tie. | **Chosen** |
| Dionysus's Thyrsus (SYSTEMS §3, gift II) | Already designed; ivy walls | Favor-gated, so it can't be a world gate; Dionysus already gives the Girdle quest's setting at Thyrsa | Keep the ivy look, drop the gift (§9, Q1) |
| Atalanta's grip | Arkadian huntress | She is an Olympiad Frontier Brain (PITCH §6); a relic named for her muddles that | No |
| Arachne's grip | Spider-climb | Ariadne's Thread is already the thread relic, and the names are one letter apart | No |
| Amalthea's horn | Goat | The Horn of Achelous is already the cornucopia | No |

- **The avoid-list.** LAZARUS lists "Satyr's Lair", so no relic, place or quest here uses the word *satyr*. "Pan" and "Crook" are clear.
- **The name fits `TERMS.md`'s pattern:** a god's possessive plus a plain object, like Hecate's Torch and Demeter's Sickle.

### The myth

- Pan was born in Arkadia, on Mount Kyllene or Lykaion, goat-legged from birth (Homeric *Hymn to Pan*). He roams "the snowy crests and the mountain peaks and rocky crags."
- **Pan sleeps at noon,** and shepherds dared not pipe then for fear of waking him (Theocritus, *Idyll* 1.15–18). Woken, he sends **panic**.
- **The syrinx.** The nymph Syrinx fled him to the river Ladon, in Arkadia, and became reeds. He cut them and made the pipes (Ovid, *Metamorphoses* 1.689–712).
- **Marathon.** The runner Philippides met Pan on the mountain road and was promised help; afterwards Athens gave Pan a cave under the Akropolis (Herodotus 6.105). That cave is a gate in §5.5.

### The quest: "Noon in Arkadia" (5–15 minutes)

When: Act II, after Laurel 5 (Kallisto), before the player leaves Arkadia by Route 13. Where: Arkadia, Pan's grotto, and the goatherd's house.

1. **The goats.** The goatherd's flock is stuck on the cliff above the grotto, frozen in a panic. "Nobody's piped since noon yesterday. Nobody dares. He's asleep in there."
2. **The grotto.** Inside, Pan sleeps behind a curtain of dead reeds. The syrinx carved over the mouth is cracked.
3. **New reeds.** Go to the Ladon reed bed at the edge of Arkadia (the Sickle cuts them, a relic the player already has) and bring three reeds.
4. **Wake him.** Pipe at the grotto mouth. The screen shakes (the scripted panic already in the map). A battle with a panicked wild **Kaprodon, Lv 36** (the boar, Arkadia's own) bursts out.
5. **Pan.** No sprite needed: a voice in the dark and a hoof-print in the dust.
   ```text
   VOICE: Who pipes at noon?

   VOICE: …Not badly. Not badly at all.

   VOICE: My goats are on the cliff. Fetch them down. Here. Goats don't fall.
   ```
6. **The Crook.** The player climbs the first marked cliff to fetch the kid down: the teach. Then the goatherd thanks them with **Kerazap, Lv 34** as a gift (the Amalthea line's cliff goat; it evolves by friendship, so a gift is the right way to give it before the wild bands allow it).

### The field mechanic

- **Engine:** the expansion's Rock Climb, `OW_ROCK_CLIMB_FIELD_MOVE` in `include/config/overworld.h` (now FALSE), on `MB_ROCK_CLIMB` metatiles. It runs as a contextual relic, like the Hammer and the Horn: face the wall and press A ("Climb with Pan's Crook?"). It goes on the Relic Ring's contextual list in SYSTEMS §1.
- **How a climbable face looks** (one look, every tileset): a vertical strip of cliff with **worn handholds cut in pairs** up its face and **ivy hanging over the top edge**, and a **small goat-hoof votive** scratched at the foot. Plain cliff never has handholds. Ivy alone, without handholds, is decoration.
- **Up and down.** Climbing works both ways; a climbed face is never a one-way trap (MAP_DESIGN §1, ledges).
- **Art cost:** one handhold face (3 metatiles: top, middle, foot) for each cliff family: limestone, ivy over limestone, basalt (Kaldera), marble (Paros, the Akropolis) and snow rock (the Ascent). About 15 metatiles, plus the expansion's climbing frames on the player sprites.
- **Myth-safe dialogue:** the prompt never mentions goats or Pan again; the Crook is just a tool after the quest.

### Where it sits in the order

Talaria, Bronze Hammer, Hecate's Torch, Demeter's Sickle, Girdle of Herakles, **Pan's Crook**, Poseidon's Conch, Daedalus's Wings, Horn of Achelous, Ariadne's Thread, Labrys, Helm of Darkness, then the post-game's Nereid Pearl and Aeolus's Bag.

- **Nothing on the main path needs it.** Arkadia's exits (Route 12 back to Styx Falls, Route 13 on to Nemea) are untouched.
- **It lands before the Conch,** so for one stretch of Act II the player can climb but not swim: the Act I regions they walk back through on Routes 13–14 and the capital road (Isthmus, Eleusa) are the first payoffs.
- **Its upgrade:** none. Pan's caves quest (§7, loop 4) gives a key item, not a stronger crook.

### As built (2026-11-18)

- **The quest:** Krotos (`Arkadia_GoatherdHouse`) tells of his kid on the crag over the grotto; the reed bed by Arkadia's falls pool, where the water runs off toward the Ladon, takes the Sickle; piping at the grotto shakes the screen and a panicked Kaprodon (Lv 36) bursts out; Pan's voice gives the Crook; the player climbs the crag (x9, rows 10-12) to the kid; Krotos gives Kerazap Lv 34. Flags `FLAG_ICHOR_NOON_*`. The crag is `tools/ichor/maps/polish/arkadia_crook.py`.
- **Faces placed:** Arkadia's crag (the teach); Route 13's scarp at (47, 14-16) to the crag pocket's PP Up (`nemea.py`); Route 9's tier 2 cliff at (27, 31-33), a shortcut between the tier 3 traverse and the scree pocket under the camp (`gulf.py`).
- **Later, and why:** Nemea's den (the upper chamber isn't built); Route 7's scree pocket (no cliff or ledge there yet: a new terrace over the camp is needed, through `kopais.py`); Route 8's Katavothres shaft and Route 11's rim and watchtower (not built); Route 28's Hyampeia face, the Ascent's storm face, the Crystal Vault's crack and Olympus's crag (post-game; Chion would need its prop packing kept stable before a climbable copy can be added); the Labyrinth's Ring II and IV faces (its tileset has 3 tiles free). The cave's flowstone family is not drawn yet: no cave hook has its reward built.

---

## 3. The gate vocabulary

One look per relic, so every map builder draws the same obstacle and every player reads it at once. Rows are in acquisition order. "Object or metatile" says how it's built.

| # | Relic | The obstacle on a map | Object or metatile | What says "come back" | Never use it for |
|---|---|---|---|---|---|
| 1 | **Talaria** (run) | — | — | — | It opens nothing |
| 2 | **Bronze Hammer** | **Marble rubble:** a heap of broken column and cornice, white with gray shadow, one tile | `BREAKABLE_ROCK` object (Route 4 is the model) | "Marble rubble. A good hammer would break it." | Natural rock (that's the 2×2 boulder) |
| 3 | **Hecate's Torch** | **A black cave mouth** with a cold brazier beside it, or a dark room; **spider webs** (thin, gray) across a passage | Dark map (`"cave": true`); web objects (`ICHOR_HIDE_HOLLOW_WEB_*`) | A sign or a voice: "No light, no entry." Eyes that catch light. | Thornwebs (thicker, see row 9) |
| 4 | **Demeter's Sickle** | **Thorn thicket** (dry, dark green, red berries); **vines** across a road; **tall reeds** in a marsh | `CUTTABLE_TREE` object; reed metatile swaps | Fruit or a jar visible past it | Trees (a tree is a wall) |
| 5 | **Girdle of Herakles** | **Fallen column drums:** a fluted marble drum on its side, one tile, that rolls one tile when pushed | `PUSHABLE_BOULDER` object, drawn as a drum (Kythera's Foam Road quarry is the model) | A stair, a door or a path visibly continuing past the drums | Boulders of raw rock |
| 6 | Winged Talaria (Hermes Favor 60) | **A one-tile gap:** a broken bridge, a split terrace, a missing aqueduct span, with the same ground on both sides | Metatile with a jump behavior; a sign ("Hermes's runners leap this.") at the first one | An item ball on the far side | Gaps of two tiles or more |
| 7 | **Pan's Crook** (proposed) | **A climbable face:** paired handholds cut up a cliff, ivy over the top edge, a goat-hoof votive at the foot | `MB_ROCK_CLIMB` metatiles (§2) | A ledge with an item, a cave mouth, or a person on top | Ledges (one-way down) |
| 8 | **Poseidon's Conch** | **Open water** reaching an islet, a sea-door, a cove, or a flooded tunnel | Water metatiles; a sea-door script (`Astyra_Harbor` is the model) | A shrine, a glint or gulls past the water | The Styx: "Nothing floats on the Styx" (`StyxFalls`) |
| 9 | Three-Flamed Torch (Hecate Favor 60) | **Thornwebs:** webs threaded with black thorns, wall to wall, glinting purple | A second web object, darker palette | "The plain torch only singes them." | Plain webs |
| 10 | **Daedalus's Wings** | **An eyrie:** a peak, mesa or sea stack with no path, and a **sighting stone** below it the player can read. Reading the stone adds the eyrie as a Wings landing. | A fly target behind a flag set by the sighting stone | The stone: "No path goes up. Something nests there." | Any place reachable on foot |
| 11 | Hephaestus's Hammer (Hephaestus Favor 60) | **A great boulder:** raw basalt or limestone, 2×2, cracked, with a bronze glint in the crack | 2×2 object or metatile block (Route 12 is the model) | "A smith's hammer would crack it. Nothing less." | Marble rubble (row 2) |
| 12 | **Horn of Achelous** | **A waterfall** with something at the top: a cave mouth, a ledge, a pool | Waterfall metatiles | A glint halfway up (Arkadia is the model) | A cascade with nothing above it |
| 13 | **Ariadne's Thread** | **A looping passage** whose exits return you to its mouth, or **a shaft** with an anchor ring at its lip | Loop warps; an anchor-ring object | A sign: "Whoever goes in comes out where they went in." | Ordinary mazes |
| 14 | **Labrys** | **A door with no handle, only a double-axe hollow;** bronze chains across a passage | Door metatile and script (the Bull Road's door is the model) | Painted Minoan plaster round the door | Greek doors (they have handles) |
| 15 | **Helm of Darkness** | **Stone sentinels** or watchers whose sight lines turn anyone back; a precinct where the seen may not pass | Sight-line triggers | "The uninitiated may not pass." | Trainers (they battle, not block) |
| 16 | Triton's Conch (Poseidon Favor 60, post-game) | **A whirlpool** in open sea or a strait | Whirlpool metatiles | An islet or a cove past it | Main-path sea routes before the post-game |
| 17 | Nereid Pearl (post-game) | **Deep water:** a darker blue patch with drowned columns showing through | Vanilla Dive tiles | Columns, a statue or a wreck visible under the surface | Shallow water |
| 18 | Aeolus's Bag (post-game) | **A fog bank:** a white wall of mist over sea, marsh or cloud | `OW_DEFOG_FIELD_MOVE` | Shapes in the fog: a mast, a roof, a peak | Weather (rain and fog weather stay weather) |
| 19 | Helm of Hades (post-game upgrade) | **A shadow door:** a dark doorway that opens only in shadow, now by day too | Time-of-day check | "It opens at night. Only at night." | — |

Two tools sit beside the relics and get no row: **Alethea's Trowel** (turned earth, SYSTEMS §5) and the **Star Chart** (§8).

---

## 4. Levels behind a gate

A gate's content uses **the band of the moment the player can first get in**: the stage in which its relic arrives, or the region's own stage if that comes later (BALANCE.md). Statics and leads sit up to 4 levels above the band, as "something stronger than around it". BALANCE's evolution rules hold: no wild evolved form below its evolution level; early evolved forms only as one-off statics or gifts; from Astyra on, evolved forms replace first stages in the wild.

| Relic | First in hand | BALANCE stage | Wild band behind its gates | Statics and leads up to |
|---|---|---|---|---|
| Bronze Hammer | Emporion, after Laurel 1 | Emporion | 16–19 | 21 |
| Hecate's Torch | Hecate's Hollow, after Laurel 2 | Eleusa | 19–22 | 24 |
| Demeter's Sickle | Eleusa, after Laurel 3 | Eleusa → Thyrsa | 22–25 | 27 |
| Girdle of Herakles | Thyrsa, after Laurel 4 | Thyrsa → Arkadia | 28–31 | 33 |
| Winged Talaria | Hermes Favor 60, typically mid Act II | Thyrsa → Arkadia | 30–33 | 35 |
| Pan's Crook | Arkadia, after Laurel 5 | Arkadia → Astyra | 33–36 | 38 |
| Poseidon's Conch | The salt well, after the Akropolis | Salt Well | 36–39 | 42 |
| Three-Flamed Torch | Hecate Favor 60, typically by Kaldera | Kaldera | 37–40 | 43 |
| Daedalus's Wings | Kaldera, after Laurel 6 | Kaldera → Kythera | 40–43 | 46 |
| Hephaestus's Hammer | Hephaestus Favor 60, typically after Kaldera | Kythera | 42–45 | 48 |
| Horn of Achelous | Kythera, after Laurel 7 | Knossa | 45–48 | 50 |
| Ariadne's Thread, Labrys, Helm | Knossa, the Labyrinth | Knossa → Lakonia | 47–51 | 54 |
| Triton's Conch, Helm of Hades | Post-game | Aethos post-game | 58–65 | 70 |
| Nereid Pearl | Atlantis | Aethos post-game | 62–68 | 72 |
| Aeolus's Bag | The Odyssey | Post-game top | 68–75 | 80 |

**Example.** The Akti islet (Conch) is on the Prologue island, but the player first sets foot on it after the salt well, so its table is 36–39 and its static is ~40.

**Kalliste in Act I.** The ferry runs between Emporion and Akti from the first arrival (`phase2/SCRIPT.md`, "Return to Kalliste"), so Kalliste's Hammer, Torch and Sickle gates open in Act I at Act I levels. Phase 2's tables already do this.

---

## 5. Region by region

Each region has: what's open on the first visit; a table of every hidden or closed part; which caves get back sections; and which routes to lengthen.

- **ID** is stable for cross-reference (K1, I3…).
- **Relic** is the name the matrix counts (§6).
- **Story** is the adventure, quest or lore behind the gate. **Pokémon** is what lives there, with levels by §4. **Also** is items, shortcuts and Favor.
- Species come from `design/dex/species/*.yaml` and `design/dex/plan.yaml`'s habitats unless marked as a National Dex legend from `LEGENDS.md`.

### 5.1 Kalliste (Prologue)

**Maps:** `ElaiaVillage`, `KallisteRoute1`, `KallisteRoute1_KronionHill`, `AktiTown`.

**First visit.** The olive groves and Route 1's terraces, Kronion Hill's ruin and dig pit, Akti's harbor and the Temple of Hestia. The Trowel later adds dig spots.

| ID | Where | Relic | Seen first | Story | Pokémon | Also | Status |
|---|---|---|---|---|---|---|---|
| K1 | Kronion Hill: the dig pit's **dark stair** → **the Kronion Crypt** | Torch | The pit, in the slice: "It still feels like something's looking up" | The carved relief of Kronos and the stone, Rhea weeping beside it: the seed for Delphoi's Omphalos | Pebblith, Cairnolith 19–22 (Phase 2's table, raised to the Torch's band); **Cairnolith Lv 20** static at the altar after the Kronos amphora (BALANCE) | Kronos sherd, Hard Stone | Gate built (`KallisteRoute1_KronionHill` dark stair); crypt designed (`phase2/SCRIPT.md`) |
| K2 | Akti's tide rocks: **marble rubble** → **Akti's Sea Grotto** | Hammer | Rubble choking the grotto mouth; Hydna's "too still" water; a glint of a sealed jar | A fisherman's shrine; the diver Hydna's lost lamp | Karkipool, Halcyling 16–19; **Galenyon** 1% | Big Pearl, Kronos sherd | Gate built (`AktiTown` grotto rubble); grotto designed |
| K3 | Route 1 terraces → **the old grove** | Sickle | Thorn thicket off the olive terraces | Elaia's oldest olives, older than the village; Halia's first spindle-whorl in a root | Elapling 4%, Psychora 1% (20–24) | Leaf Stone, Oran Berry | Designed |
| K4 | Kronion Hill: **the toppled stylobate** | Girdle | Drums lying across the temple's back steps; a herm behind them | The Titanborn's first camp: a dropped work-list in Iapetos's hand that names "the girl's mother" (a beat of foreshadowing for Delphoi) | Cairnolith 28–30 at night, rare **Laolith** static Lv 32 (a one-off; it evolves by trade otherwise) | TM, Titan lore | Proposed |
| K5 | Kronion Hill's **north face** | Crook | A goat on an impossible ledge, seen from the summit | A goatherd's kid stranded since the slice; on the ledge, a cleft altar to Rhea: "Here she swaddled the stone." | **Kerazap Lv 35** static (Amalthea line), Eripip 33–35 | Shortcut down to Elaia's beach | Proposed |
| K6 | Off Akti's quay: **the islet shrine** | Conch | The white shrine on the slice's harbor views; the fisher who points at it | The Poseidon altar's keeper tells of a city under the sea that drowned for pride: the **Pontanax lead's first step** (Atlantis, post-game) | Galenyon, Narkeray, Karkitox 36–39; **Narkeray Lv 41** static on the altar steps | Big Pearl, Poseidon Favor +5 | Gate built (tease in `AktiTown`) |
| K7 | Route 1: **the split terrace** above the groves | Winged Talaria | An item ball across a one-tile gap | — (minor) | — | PP Up; a shortcut from Elaia to Kronion | Proposed |
| K8 | **Mount Zas eyrie**, Kalliste's peak (Naxos's real Mount Zas) | Wings | A sighting stone on Route 1: "Eagles nest on Zas. No path goes up." | Naxians say Zeus was hidden here too. A lightning-split altar, and an old eagle that watches the sea: the **Olympanax lead** (post-game storm terrace) | **Aetling Lv 44** static; Lophops, Basilops 40–43 | Kalliste's second Wings landing | Proposed |
| K9 | Akti's other islet, under the great marble door frame (Naxos's real Portara) → **Ariadne's door** | Labrys | A door frame with no wall, and below it a handle-less door with a double-axe hollow | **Ariadne's return.** After Knossa she sails to Kalliste: "Someone once told me I'd be left on an island. I'd like to see which one." Behind the door, a Minoan shrine to her. She leaves her crown, which becomes the **Corona Borealis** constellation (SYSTEMS §8) | **Mitoclew Lv 52** static (the Ariadne line) | Dionysus Favor +10; a Phaistos Disc (LEGENDS §7.3) | Proposed |
| K10 | The Kronion Crypt's **inner door** | Labrys | A second door in the crypt's back wall, behind the relief | The Titanborn's first dig reached a Minoan seal and stopped. Inside, the **"house of the double axe"** inscription's other half (Kronion Hill already has its first line) | Cairnolith, Laolith 48–51 | Ichor Stone | Proposed |
| K11 | The Sea Grotto's **drowned back pool** | Pearl | Columns under the pool's still water | The colonists' first ship, sunk on arrival: a votive from Elaia's founders to Hestia | **Haligeron Lv 68** static (the Proteus line: "it changes shape when you look away"); Charonaut 62–66 | Elaia's founding story; a Hestia relic for the Odyssey's homecoming | Proposed |

- **Caves with back sections:** the Kronion Crypt (K10, Labrys), Akti's Sea Grotto (K11, Pearl).
- **Routes to lengthen:** Route 1 gets the old grove (K3), the split terrace (K7) and the Zas sighting stone (K8), and its west edge becomes a shore walk round to the Portara islet (K9) seen from the land.

### 5.2 The Isthmus and Eleusa (Act I)

**Maps:** `EmporionCity` and its interiors, `EmporionHarbor`, `Route4_Isthmus`, `HecatesHollow`, `Route5_SkironianCliffs`, `Route5_RestHouse`, `EleusaVillage`, `EleusaSanctum_B1F`–`B3F`, `Route6_EleutheraiRoad` (with Mt. Kithairon).

**First visit.** The Agora, the Deigma and the Hephaisteion; Route 4's slide (the Hammer, main path); the Hollow's three roads and web chamber (the Torch); the Skironian cliffs; Eleusa's fields and the sanctum (the Torch, main path); the vines on Route 6 (the Sickle, end of Act I).

| ID | Where | Relic | Seen first | Story | Pokémon | Also | Status |
|---|---|---|---|---|---|---|---|
| I1 | Under the Agora steps → **Emporion's cistern** | Torch | The black mouth and its sign: "No light, no entry." Dripping water; eyes in the dark | **The man in the jar.** A philosopher lives in an empty pithos at the bottom. Shine the torch at him: "Stand out of my light." He trades riddles for the cistern's sealed jar | **Pithound Lv 22** static (the Diogenes line, "empty jars in Emporion's Agora"); Galekit, Harpeck 19–22 | TM, sealed jar | Gate built (`EmporionCity` cistern script) |
| I2 | The cistern's **flooded far tunnel** → **the spring of Peirene** | Conch | The tunnel ends in black water with a draught and daylight beyond | **Bellerophon's spring, part 1.** Peirene wept herself into a spring for her son. A golden bridle lies in the basin, where Bellerophon caught the winged horse. It starts the **Pegaunos chain** (§7, loop 6) | Ketofry, Kynoketos, Karkitox 36–39; **Galenyon Lv 41** | The Golden Bridle (key item) | Proposed |
| I3 | **Akrokorinthos eyrie,** the rock over Emporion | Wings | A sighting stone on Route 4: "The old fort on the rock. The stair fell a century ago." | **Bellerophon's spring, part 2.** The upper spring where the horse drank. With the bridle, a hoof-print in the rock glows: the next step is Helikon (T9) | Harpelle, Basilops 40–43 | Aphrodite's ruined shrine; Aphrodite Favor +5 | Proposed |
| I4 | **The Hephaisteion's back stair** | Girdle | Drums blocking the stair to the roof | **Kedalion's roof forge.** He carried blind Orion on his shoulders, in myth. He tells it, and gives the **Orion lead** (SYSTEMS §8) | **Kaminoo Lv 31** gift (the bronze bull calf) | TM, Hephaestus Favor +5 | Designed (SYSTEMS §1) |
| I5 | Route 4: **the terrace orchard** | Sickle | Thicket below a sealed jar | The Isthmian beekeeper's abandoned hives; finish her harvest for her | **Melisseer Lv 25** static on the hives; Melibee 22–24 | Sitrus Berry, a Figy tree | Gate built (`ICHOR_HIDE_THICKET_ROUTE`) |
| I6 | Route 4: **the ship-track** (the real *diolkos*) | Winged Talaria | Broken slipway sections in the ship-track | A Hermes runner races you over the track (SYSTEMS's Talaria races) | — | Shortcut Emporion ↔ the Hollow; Hermes Favor +5 | Proposed |
| I7 | Route 4: **the drum pocket** | Girdle | A drum in the scrub with a pine wreath on the far side | The Isthmian Games were Poseidon's, crowned with pine. A retired victor's training ground | **Nemecub** swarm 28–30, **Nemeleon Lv 33** static | Pine wreath (a Poseidon offering) | Gate built (Route 4 `PUSHABLE_BOULDER`) |
| I8 | Hecate's Hollow: **the Wandering Halls** | Thread | "Whoever goes in comes out where they went in." | **What Hecate saw.** At the loop's heart, Hecate's own shrine; she tells you she lit Demeter's way when Kore was taken, and what Kore said going down. It deepens Eleusa's Mysteries and seeds the Underworld | **Lykanax Lv 50** static (Hecate's hound, grown); Hyphantis, Lykanax 47–50 | Hecate Favor +10, Max Revive | Designed (SYSTEMS §1) |
| I9 | Hecate's Hollow: **Hecate's garden** past the thornwebs | Three-Flamed Torch | "The plain torch only singes them." | Aconite grew where Kerberos's slaver fell. A witch-gardener tends it, and names Colchis, where her sister grows the same (the Oikoumene's Medea) | **Hyphantis Lv 42** static; Panacoil, Ophidrop 37–40 | TM Toxic | Proposed |
| I10 | Route 5: **Skiron's cove** under the cliffs | Conch | From the cliff path, a giant shell on the beach below | **Skiron's turtle.** The bandit kicked travelers off this cliff to a turtle; Theseus kicked him to it. The turtle is still here, old and gentle | **Chelyra Lv 40** static (the tortoise line, final form); Galenyon 36–39 | Big Pearl | Proposed |
| I11 | Route 5: **Skiron's lookout** above the cove | Crook | Handholds up from the cove, and a rope end at the top | The bandit's hoard, and the stone where he sat. Optional trainer: a "Skironian" highwayman (Lv 38) | — | Nugget ×2 | Proposed |
| I12 | **The crypt of the Mysteries** under Eleusa's sanctum | Helm | Stone sentinels on B3F: "The uninitiated may not pass." A dark stair past them | **The last secret.** Kore's descent, told in the dark; then Persephone's empty throne. It deepens Act I's trial and seeds the Underworld | **Persenyx Lv 53** static (the pomegranate line, Persephone below by night); Korantha 50–52 | Demeter Favor +10, an item | Designed (SYSTEMS §1) |
| I13 | Eleusa: **the Ploutonion's bronze gate** | Helm of Hades | The cave of Hades beside the sanctum, its gate shut | A side door into the Katabasis: the way Persephone comes up each spring | Underworld table, 62–66 | A shortcut into `UNDERWORLD.md`'s Asphodel | Gate built (`EleusaVillage`) |
| I14 | Eleusa's bay: **the snake-king's islet** (Salamis's Kychreus) | Conch | An islet with a serpent carved on its stele, seen from Route 5 | Kychreus, half snake, served Demeter at Eleusis. His cave keeps her oldest offerings | **Panacoil Lv 40**; Ophidrop 36–39 | Demeter Favor +5 | Proposed |
| I15 | Mt. Kithairon: **Pentheus's pine** | Crook | An ivy face to a pine on the crag, ribbons tied to it | **The Bacchae.** The pine where Pentheus spied on the maenads. A Thyrsa actor rehearses the scene up there and asks you to play Pentheus | **Oinopard Lv 36** at night; Botrykit 33–35 | Dionysus Favor +5; Dionysus's theoxenia start (AETHOS_MAP proposal) | Proposed |
| I16 | Route 5: **rubble on the cliff stair** → the cliff-top pasture | Hammer | A sealed jar on the pasture above the rubble | A shepherd who grazes where nobody can reach him; he trades | Epopoi, Lophops 16–19; **Kerazap** 1% | Sealed jar | Gate built (`Route5_SkironianCliffs` rock) |
| I17 | Route 5: **the pine hollow** | Sickle | A thicket under the pines, sap smell | Skiron's victims' grave stelai; a mourner who wants a name read | Kampillar, Nymveil 22–25 | Revive | Gate built (`Route5_SkironianCliffs` thicket) |

- **Caves with back sections:** Emporion's cistern (I2, Conch), Hecate's Hollow (I8 Thread, I9 Three-Flamed Torch), Eleusa's sanctum (I12 Helm, I13 Helm of Hades).
- **Routes to lengthen:** Route 4 (the ship-track and drum pocket); Route 5 (a beach level under the cliffs with the cove and lookout, so the cliff route gets a second tier); Route 6 (the Kithairon crag, I15). `Route5_SkironianCliffs` and `Route6_EleutheraiRoad` already carry rock, thicket and drum objects: each must lead somewhere that pays.

### 5.3 Thyrsa, Kopais and Parnassos (Act II)

**Maps:** `Route7_KroniaGrounds`, `ThyrsaCity` and interiors, `Route8_KopaisRoad`, `Lebadeia`, `Route9_ParnassosCrossroads`, `Kirrha`. Euboia is unbuilt. Routes 7–9, Lebadeia and Kirrha are **in progress**.

**First visit.** The Kronia feast camp, the Dionysia, the vineyards, the Kopais reeds, Lebadeia's new temple rest stop, the crossroads under Parnassos, Kirrha's harbor with Delphoi shut above.

| ID | Where | Relic | Seen first | Story | Pokémon | Also | Status |
|---|---|---|---|---|---|---|---|
| T1 | Route 7: **the Titans' cache** behind the feast camp | Hephaestus's Hammer | A great boulder rolled over a pit; Titanborn bootprints round it | Iapetos's discarded script pages for *The Unwoven*: a scene he cut, where the hero's mother speaks (lore toward Delphoi) | **Gigantomb Lv 46** static (the Titans' Pokémon); Kapnub 42–45 | Rare Candy | In progress (Route 7) |
| T2 | Thyrsa: **Silenos's winepress cellar** past the Proitid gate | Girdle | Drums blocking the cellar ramp in the vineyard | Opens as soon as the Girdle is won. Silenos's hidden amphora and his one true story about Dionysus | **Thyrsivy Lv 33** static; Ampelix 28–31 | Wine (an offering) ×3 | Proposed |
| T3 | Thyrsa: **the spring of Ares** under the Kadmeia | Labrys | Bronze chains across a cave mouth by the spring | **Kadmos's dragon.** He killed it here and sowed its teeth; armed men sprang up. Its last teeth are still chained in. Harmonia's necklace story, cursed by its maker | **Dorydrake Lv 51** static; Sporadon, Dorydrake 47–51 | Dragon Fang | Proposed |
| T4 | Route 8: **the Sphinx's rock** (Mount Phikion) | Sickle | A rock above the reeds with a winged shape on it | Three riddles, the Sphinx's own trial, on the road to Thebes. Sickle-time, so it opens on the first visit | **Enigmaw Lv 31** static after the riddles | — | In progress (Route 8) |
| T5 | Route 8: **the Kopais sinkholes** | Conch | Whirling water in the lake's reed edge; a domed tomb on the far shore | **Herakles drowned Orchomenos** by blocking the sinkholes. Surf to the drowned Minyan treasury; roll a drum out of a sinkhole (the Girdle) to drain one chamber | Kynoketos, Karkitox, Narkeray 36–39; **Kynoketos Lv 41** | Gold Stater ×2 (the Treasury of Minyas) | In progress (Route 8) |
| T6 | Route 8: **the Kopais marsh mist** | Bag | A fog bank over the north marsh that never lifts | The marsh's far side, where the reed people live outside time: post-game | Stachypter, Narcisheen 70–74 | Post-game fishing table | Proposed |
| T7 | Lebadeia: **the oracle of Trophonios** | Thread | The sealed descent behind the new temple (IDEAS.md) | **Feet first.** Tie the Thread to the anchor ring and go down. Drink from Lethe, then Mnemosyne. At the bottom, a votive tablet from **Phaedon**, years old, asking whether his daughter will live. (The player finds it before Knossa's reveal) | **Amnoze Lv 50** static at Lethe; Sophowl, Amnoze 47–50 | Move Relearner at Mnemosyne's spring; "forget" at Lethe's | In progress (temple); descent proposed |
| T8 | Lebadeia: **the Herkyna cascade** | Horn | A waterfall in the gorge behind the hamlet, a goose carved over a pool at the top | The nymph Herkyna and Kore played here with a goose that ran off into a cave (Pausanias 9.39) | **Hymnaria Lv 49**; Hymnet 45–47 | Persephone lore; Demeter Favor +5 | Proposed |
| T9 | **Helikon's horse-spring** (Hippokrene) | Wings | A sighting stone on Route 8: "The horse-spring. Struck by a hoof. No road." | **Bellerophon's spring, part 3.** The spring the winged horse struck. The bridle fits a hoof-print. Last step before Olympus (post-game, Bag) | Basilops, Harpelle 41–44 | A Pegaunos feather (key) | Proposed |
| T10 | Route 9: **the Korykian approach** | Crook | Handholds up the crossroads' north cliff to a plateau | The upper road toward Pan's cave on Parnassos, closed at the top until the League (D8). Pan's caves quest step | **Pythoros Lv 37** (python line); Pelython 33–35 | Shortcut over the crossroads | In progress (Route 9) |
| T11 | Kirrha: **Apollo's dolphin cove** | Conch | A cove under the harbor wall with a dolphin carved on its rock | **The Cretan priests.** Apollo, as a dolphin, steered a Knossian ship here and made its sailors his first priests (*Homeric Hymn to Apollo*). Their wrecked ship's log points to Delphoi (D7) | Galenyon, Narkeray 36–39 | Apollo Favor +5 | In progress (Kirrha) |
| T12 | Euboia: **the Euripus race** | Triton's Conch | The strait's current reversing; a cove at Aulis past it | Aulis, where the fleet waited for wind. A post-game episode with Agamemnon's stranded priest | Trybdis 62–65 | — | Proposed |
| T13 | Euboia: **the Chalkis copper mine** | Hephaestus's Hammer | Boulders in a mine adit marked with bronze-green stains | Chalkis is named for bronze. The Kouretes' bronze came from here | **Kourodin Lv 47**; Kymbash 42–45 | Metal Coat | Proposed |
| T14 | Route 8: **Orchomenos's rubble** on the shore road | Hammer | A collapsed tomb porch beside the road | Opens on the first visit: the treasury's outer room and a sign pointing to the sinkholes (T5) | Pebblith, Cairnolith 24–27 | Hard Stone | In progress (Route 8) |

- **Caves with back sections:** Trophonios (T7), the Kopais treasury (T5), the spring of Ares (T3), the Chalkis mine (T13).
- **Routes to lengthen:** Route 7 (the cache behind the camp); Route 8 (a lake shore level with the reeds, the Sphinx's rock and the sinkholes: two of the best gates in the game sit here); Route 9 (the north cliff tier).

### 5.4 The Gulf, Arkadia and Nemea (Act II)

**Maps:** `GulfTrireme` (Route 10), `Aigion`, Route 11, `StyxFalls` and interiors, `Route12_CypressRoad`, `Arkadia` and interiors (`Arkadia_CypressWood`, `Arkadia_NyktimosHall`, `Arkadia_GoatherdHouse`), Route 13, `Nemea`, `Route14_NemeaRoad`. Route 11, Route 13, Aigion and Nemea are **in progress**.

**First visit.** The ferry, Aigion, the drum pass (the Girdle, main path), the black falls, the cypress road, Arkadia and the Temple of Artemis, the road down to Nemea's columns.

| ID | Where | Relic | Seen first | Story | Pokémon | Also | Status |
|---|---|---|---|---|---|---|---|
| G1 | Off Aigion: **the Helike reef** | Conch | Column tops in the shallows off the landing, seen from the ferry | **Helike**, Poseidon's city that sank in one night. A fisher who lost his grandfather there | Narkeray, Galenyon 37–40 | Pontanax lead, step 2 | In progress (Aigion's shore) |
| G2 | Off Aigion: **drowned Helike** | Pearl | The reef's dark-blue hollow, a bronze Poseidon on his back below | The city's temple, still standing under the sea: the Pontanax lead's last step before Atlantis | **Charonaut Lv 68** static; Kynoketos 62–66 | Poseidon Favor +10 | Proposed |
| G3 | Route 10: **the Rhion whirlpool** | Triton's Conch | A whirlpool in the strait the ferry steers round | A sea cave in the narrows | Kynoketos, Trybdis 60–64 | Big Pearl | Proposed |
| G4 | Aigion: **the goat's cave** above the town | Crook | Handholds up the bluff, a goat skull over a cave | Aigion was named for the goat who nursed Zeus. Its cave holds a shepherds' shrine and a seed for Knossa's Diktaean cave (C5) | **Kerazap Lv 37**; Eripip 33–36 | Amalthea's milk (a held item: Leftovers) | In progress (Aigion) |
| G5 | Route 11: **the Cave of the Lakes** (the Vouraikos gorge) | Horn | A waterfall beside the drum pass with a cave mouth at its top | Thirteen stepped lakes in the dark, where Melampous cured the Proitid daughters' madness. Ties to Thyrsa's Proitid gate | **Dakrock Lv 49** (the weeping rock); Lykanax, Karkitox 45–48 | Thyrsa's Proitid gatekeeper's quest ends here | In progress (Route 11) |
| G6 | Styx Falls: **the source ledge** | Crook | Handholds beside the black falls, ribbons on a ledge | **The hoof cup.** The Styx breaks every vessel but a horse's hoof (Pausanias 8.18). The Oath House's keeper wants water from the source for a true oath; the girl's grandmother already says "Except hooves." | Obolorn 33–36 at night; **Kalyptor Lv 38** | The Hoof Cup (key: Charon recognizes it in the Katabasis) | Proposed (`StyxFalls_OathHouse` is built) |
| G7 | Route 12: **the bear's den** | Hephaestus's Hammer | The 2×2 boulder in the rock, and its sign | **Kallisto and Arkas.** Kallisto, turned into a bear, nearly killed by her own son: Zeus set them in the sky. The den's mother bear | **Starkos Lv 47** static (the Kallisto line, final form); Arkoby 42–45 | **Ursa Major** constellation (SYSTEMS §8) | Gate built (Route 12) |
| G8 | Arkadia: **the waterfall cave** | Horn | "Halfway up, there's a cave mouth. Something glints in it." | The upper pool: the Orpheus amphora's sherds and the **Meloetta lead** (LEGENDS §4.7) | Psychora, Lykanax 45–48; **Amnoze Lv 50** at night | — | Gate built (`Arkadia`) |
| G9 | Arkadia: **Pan's grotto**, upper meadow | Crook | The panic, scripted; goats on the cliff | **The Crook's own quest** (§2), then a high meadow on Kyllene where Hermes made the first lyre from a tortoise | **Chelyra Lv 38** static; Chelonet 33–36 | Hermes Favor +5 | Gate built (grotto tease); quest proposed |
| G10 | Arkadia: **the cypress thornwebs** in `Arkadia_CypressWood` | Three-Flamed Torch | Webs between cypresses, too thick to burn | Arachne's grove: a weaver who challenged a goddess, and her last web (the Arachne line's home) | **Hyphantis Lv 43** static; Raknit, Hyphantis 37–40 | Silk Scarf | Proposed |
| G11 | Mount Lykaion: **the shadowless precinct** off `Arkadia_NyktimosHall` | Helm | A walled precinct whose sentinels turn you back. Inside, nobody casts a shadow (Pausanias 8.38) | **Lykaon's ash altar.** The king who served Zeus human flesh, made a wolf. His son Nyktimos (whose hall stands) tells it. The wolf-king is still there | **Lykanax Lv 54** static (the alpha); Lykanax 50–52 | Dark-type TM | Proposed |
| G12 | Arkadia: **the Pool of Mnemosyne**, deep | Pearl | The pool's bottom shows stars in daylight | The Frozen Hour's sanctuary has a floor nobody has seen. **Ichorin** waits there with Mnemosyne's Water (LEGENDS: Lv 70) | **Ichorin Lv 70** | — | Designed (LEGENDS, POSTGAME) |
| G13 | Mount Kyllene: **the cave of Maia** | Wings | A sighting stone on Route 13: "Hermes was born up there. No road." | Hermes's birth cave and the first theft (Apollo's cattle). A runner's shrine | **Skylaps Lv 44** static (the Laelaps line, which roams) | Hermes Favor +10 (a step toward the Winged Talaria) | Proposed |
| G14 | Route 13: **the terrace gaps** | Winged Talaria | Split shepherd terraces down the highlands | — (minor) | — | Shortcut and items | In progress (Route 13) |
| G15 | Nemea: **the Lion's cave**, second mouth | Girdle | Drums jammed in a cleft behind Zeus's columns | Herakles blocked one mouth of the Lion's cave. Before Labor 1 the inner cave stays sealed (story); this is the outer chamber | **Nemeleon Lv 34** static; Nemecub 30–32 | Labor 1's lead | In progress (Nemea) |
| G16 | Route 14: **the broken aqueduct** | Winged Talaria | A missing span across a gully | Kleonai's channel: a shortcut back to Emporion | — | Shortcut | In progress (Route 14) |
| G17 | Nemea: **the temple crypt** under Zeus's columns | Hammer | Rubble in the crypt stair | Opens on the first visit: the Nemean Games' victor lists, and a priest who tracks the Lion (Labor 1's first lead) | Nemecub 29–31 | Nemean wreath (celery, a Zeus offering) | In progress (Nemea) |

- **Caves with back sections:** Arkadia's waterfall cave (G8), the Cave of the Lakes (G5), the goat's cave (G4), Pan's grotto (G9), the bear's den (G7), the Lion's cave (G15), Lykaion (G11).
- **Routes to lengthen:** Route 11 (the gorge with its cascade and cave, not a straight drum pass); Route 12 (the den pocket); Route 13 (terraces, the Kyllene sighting stone); Route 14 (the aqueduct gully).

### 5.5 Astyra and the Akropolis (Act II)

**Maps:** `Route15_MysteryRoad`, `Daphni`, `Route16_CapitalPass`, `Astyra`, `Astyra_Akropolis`, `Astyra_Harbor`, `Astyra_Library`, `Astyra_Stoa`, `SaltWell_B1F`, `SaltWell_B2F`, Aegina (`AeginaTown`, `AeginaAphaiaRoad`, `AeginaMountOros`, `AeginaTempleOfAphaia`). Routes 17 and 18 are unbuilt.

**First visit.** The road of the Mysteries, Daphni's laurels, the capital, the Akropolis battle, the salt well (the Conch), Aegina by ferry.

| ID | Where | Relic | Seen first | Story | Pokémon | Also | Status |
|---|---|---|---|---|---|---|---|
| A1 | Route 15: **the jesters' bridge** over the Kephisos | Winged Talaria | A broken bridge; a masked jester on the far side shouting insults | The procession's bridge-jesting (*gephyrismos*). Out-insult him for a prize | — | Hermes Favor +5 | Proposed |
| A2 | Daphni: **the Aigaleo lookout** | Crook | An ivy face behind the laurel grove | A stone seat where a Persian king watched his fleet lose at Salamis. A traveler from the east waits there: the Oikoumene's first rumor | **Daphnyad Lv 37** static (BALANCE: Daphnyad is already wild here) | Lore toward the Troad | Proposed |
| A3 | The Akropolis: **the cave of Pan** on the north slope | Crook | Handholds up the Long Rocks from the Agora side | **The runner.** Pan met Philippides before Marathon; Athens gave him this cave. Pan's caves quest, step 2; starts the Marathon race (A9) | Sophowl, Glaukoin 34–37 | The runner's sandal (a key for A9) | Proposed |
| A4 | The Akropolis: **the Arrephoroi stair** | Helm | A sealed stair the night-girls used, sentinels at its head | Girls carried a covered chest down it unseen. Erichthonios, the snake-child Athena raised: the sisters who looked went mad. You may look | **Panacoil Lv 54** static | Athena lore; a TM | Proposed |
| A5 | The salt well: **the trident's root** | Pearl | B2F's deepest pool, three marks scored into its floor | Where Poseidon struck the rock. The sea under the city: a passage toward Atlantis | **Kynoketos Lv 66** static; Charonaut 62–65 | Poseidon Favor +10 | Proposed |
| A6 | Astyra: **the weavers' loft** over the weaving quarter | Three-Flamed Torch | Thornwebs in the loft door | The Arachne line's city home; a weaver unpicking a tapestry of the Titans' war | **Hyphantis Lv 41**; Raknit 37–39 | — | Proposed |
| A7 | **Lykabettos eyrie,** the hill over Astyra | Wings | A sighting stone in the Stoa's square: "Athena dropped that hill when the crow told her the news. No path." | The crow who carried bad news and was turned black; it's still up there, still gossiping | **Harpelle Lv 44**; Glaukoin 40–43 | Lore: the Akropolis's founding | Proposed |
| A8 | Route 16: **the pass gaps** | Winged Talaria | A collapsed span of the old border road | — (minor) | — | Shortcut | Proposed |
| A9 | Route 17: **the runner's road** to Marathon | (Talaria race) | — | Philippides's run, timed, with the sandal from A3 | — | Hermes Favor | Proposed (not a gate) |
| A10 | Marathon: **the phantom battle** | Helm | The mound; at night, sounds of fighting (Pausanias 1.32) | Unseen, you watch the night battle; a phantom hoplite notices you and fights | **Kalyptor Lv 54** static; phantom hoplite trainer Lv 54 | Charon line lead | Proposed |
| A11 | Route 18: **the Laurion silver galleries** | Hephaestus's Hammer | Great boulders in a mine adit, lamp soot on the stone | A miner's son lost in the galleries; the dark (the Torch) and the boulders combine | **Plouteras Lv 46**, Midonos 43–45 | Nugget, Gold Stater | Proposed |
| A12 | Cape Sounion: **Aegeus's cove** | Conch | Under the cliff where Aegeus leapt, a black sail in a cave | Theseus forgot to change the sail; his father leapt. The sail, kept by fishermen. Lore that reaches Knossa | Galenyon, Karkitox 36–39 | Poseidon Favor +5 | Proposed |
| A13 | Aegina: **Aphaia's net-room** under her temple | Labrys | A double-axe door in `AeginaTempleOfAphaia`'s crypt | Aphaia (Britomartis) fled Minos, leapt into the sea and was caught in fishers' nets. A Minoan shrine of hers: a sixth vault (Q2) | **Hoplomex Lv 50** (the Myrmidon line); Ergant, Hoplomex 47–50 | A Phaistos Disc | Proposed |
| A14 | Aegina: **Mount Oros's rain ridge** | Crook | Handholds above the summit altar | Zeus's rain altar's high stone, where Aiakos prayed the drought away; an ant colony's queen chamber | **Hoplomex Lv 38** static | Zeus lore | Proposed |

- **Caves with back sections:** the salt well (A5, Pearl; its dark grotto is already Torch), the Akropolis caves (A3, A4), Laurion (A11), Sounion's cove (A12), Aphaia's crypt (A13).
- **Routes to lengthen:** Route 15 (the bridge and the salt lakes' shore); Route 16 (gaps); Routes 17 and 18 when built, each with a cave.

### 5.6 The sea and the Kyklades (Act II–III)

**Maps:** `Kaldera` and interiors (`Kaldera_TelchinesForge`, `Kaldera_TempleOfHephaestus`), the Kythera set (`KytheraPaphia`, `KytheraSkandeia`, `KytheraFoamRoad`, `KytheraNeraidaFalls`, `KytheraNeraidaFalls_Mill`, `KytheraSpringOfKallirhoe`, `KytheraEchoCaves`, `KytheraTempleOfAphrodite`), `TriremeEuploia_Deck`, `TriremeEuploia_Hold`. Routes 19–24 and the ten Conch islands are unbuilt.

**First visit.** Kaldera's forge and Laurel 6, the Wings; Kythera's beaches, the Spring of Kallirhoe and Laurel 7, the Horn.

| ID | Where | Relic | Seen first | Story | Pokémon | Also | Status |
|---|---|---|---|---|---|---|---|
| S1 | Kaldera: **the ash-cliff door** → Akrotiri, the town under the ash | Labrys | "A door in Kaldera's ash cliff with no handle" | The first Minoan vault: a whole street of a town buried by the volcano (LABYRINTH §9) | **Sepivolt Lv 51**; Kolossette 48–50 | Phaistos Discs, coins | Designed (LABYRINTH §9) |
| S2 | Kaldera's caldera floor: **the vent boulder** | Hephaestus's Hammer | A boulder that's warm to the touch | **The Forge Under the Forge** (LEGENDS §7.2): Talos and blind Hyperion guide you down. Before the post-game, the first chamber opens: lava tubes, Hyperion's directions | **Taurivet Lv 46**, Gigantomb 43–45; Heatran (post-game, Lv 72) at the bottom | Fire Stone | Designed (LEGENDS) |
| S3 | Kaldera: **the burnt islet** in the caldera | Conch | A smoking islet in the bay, seen from the harbor | Where Hyperion's eruption broke through; a crater with a Titan's dropped helm | **Promethex Lv 44** static; Kapnub 37–40 | Charcoal ×3 | Proposed |
| S4 | Kaldera: **the Telchines' sea forge** past the forge's back | Crook | Handholds down the basalt from the forge yard to a sea-cave | The first smiths of Rhodos, the sea-dog Telchines: a post-game Rhodos hook | **Telkanvil Lv 39** static; Telpup 35–37 | Rhodos lead | Proposed |
| S5 | Kythera: **the Neraida upper pool** | Horn | The silent falls | Daedalus's page VII, the vault door and Thestylis | per `MAPS_kythera.md` | Page VII | Built (`KytheraNeraidaFalls`) |
| S6 | Kythera: **the upper pool's vault door** | Labrys | The double-axe door in the pool's cliff | A Minoan vault on Kythera (LABYRINTH §9) | **Kalliglyph Lv 52** static; Glyphlet 47–50 | Phaistos Disc | Gate built (TODO in script) |
| S7 | Kythera: **the Echo Caves' sea mouth** | Conch | The rock in the water past the arch | Echo's last word | Echolali, Narcisheen (cave table) | TM Hyper Voice (pending) | Built |
| S8 | Kythera: **the Foam Road quarry** | Girdle | Drums across the quarry path | Galatea's unfinished statues | quarry table | — | Built |
| S9 | Kythera: **the headland cascade** | Horn | A cascade off the Foam Road headland | Clifftop meadow | meadow table | — | Built |
| S10 | Kythera: **the myrtle thicket** at Kallirhoe | Sickle | Thicket on the spring's back path | Narcissus's other pool | Narcibulb 38–42 | — | Gate built (TODO in script) |
| S11 | Kythera: **the foam rock** (Aphrodite's birthplace) | Pearl | A sea stack off Paphia ringed with white foam | **The first cut.** Aphrodite rose from the foam where Ouranos's blood fell, cut by Kronos's sickle: the Harpe's first stroke. Lore at the heart of the main plot | **Aphrogene Lv 68** static | Enamorus lead (LEGENDS: the Spring of Kallirhoe) | Proposed |
| S12 | Delos: **Kynthos grotto** | Crook | A cave mouth above the island's lake, handholds to it | Leto's labour: Artemis, born first, helped deliver Apollo. A midwife's shrine | **Hymnaria Lv 44** | Apollo and Artemis Favor +5 each | Proposed |
| S13 | Paros: **the lamplit quarry**, deep seam | Hephaestus's Hammer | The dark quarry (the Torch) ends at a boulder with marble glinting through | The seam Galatea was carved from; a sculptor who knew her (AETHOS_MAP) | **Kalliglyph Lv 47**; Glyphlet 42–45 | Galatea lore before Laurel 7 | Proposed |
| S14 | Lemnos: **Hephaestus's landing** | Hephaestus's Hammer | A crater where something fell from Olympus | Hephaestus fell here and was nursed by Thetis; his first forge. Philoctetes's cave (the Torch) beside it | **Kolossette Lv 46** static; Kaminoo, Taurivet 42–45 | Hephaestus Favor +10; Herakles's bow lead (Labors) | Proposed |
| S15 | Samothrake: **the Hall of the Great Gods** | Helm | Initiates only; sentinels at the inner door | The sailors' Mysteries; the inner rite grants the sailor's blessing at full strength | **Galenyon Lv 52** static; Narkeray 47–50 | Poseidon Favor +10 | Proposed |
| S16 | Samos: **Eupalinos's tunnel** | Thread | A tunnel with two mouths; inside, it loops | Dug from both ends to meet in the middle. Tie the Thread at one mouth, walk out the other; Hera's Heraion vault | **Basilops Lv 50** static (the hoopoe king, Hera's bird stand-in); Lophops 46–49 | Hera's rite (Cancer at Favor 30) | Proposed |
| S17 | Ikaria: **Icarus's rock** | Wings | A sighting stone on the shore: "He fell there. Nobody goes up." | A wax-sealed letter from Daedalus to his son, never sent. Daedalus's arc, before or after Knossa | **Ikaroth Lv 46** on sunny days | The Icarus amphora's last sherd | Proposed |
| S18 | Skyros: **Lykomedes's cliff** | Crook | Handholds up the cliff behind the palace | Theseus was pushed off it. His bones are still there; an Athenian wants them home (a fetch quest to Astyra) | Hoplektor 44–46 | Rare Candy | Proposed |
| S19 | Route 21: **the Icarian whirlpool** | Triton's Conch | A whirlpool where Icarus's sea is deepest | A sea cave with a drowned feathered harness | Trybdis 62–65 | — | Proposed |
| S20 | Cape Malea (Route 22–24): **the fog bank** | Bag | Fog off the cape that the trireme always steers round | The Odyssey's storm starts here; after the Bag, a hidden cove of wrecks | Seirenade, Elegull 70–74 | Wreck salvage | Proposed |
| S21 | Kythera: **the Echo Caves' dark gallery** | Torch | A cold brazier at the gallery's mouth | Kolymbos by the lamp; the gallery's far end | cave table 40–44 | Heart Scale | Gate built (brazier TODO in script) |
| S22 | Paros: **the lamplit quarry** | Torch | A black quarry mouth with lamp niches | Marble cut by lamplight (AETHOS_MAP); leads to S13 | Glyphlet 38–41 | — | Proposed |
| S23 | Melos: **the obsidian face** | Hammer | Rubble over a black-glass seam | The obsidian dig site (AETHOS_MAP) | Sepidart 40–43 | Obsidian (a Trowel find) | Proposed |

- **Caves with back sections:** the Telchines forge (S2, S4), Akrotiri (S1), the Echo Caves (S7), the Neraida pool (S6), the Paros quarry (S13), Philoctetes's cave (S14), the Kynthos grotto (S12), Eupalinos's tunnel (S16).
- **Sea routes:** every sea route gets one islet or reef with a Conch payoff and a deep patch for the Pearl, so the sea isn't empty water (MAP_DESIGN §6).

### 5.7 Crete and the Labyrinth (Act III)

**Maps:** `KnossaAmnisos` and interiors, `KnossaBullRoad` (+`_Hut`, `_Vineyard`), `KnossaBronzeHeel`, `KnossaPalace` and rooms, `LabyrinthRing1`–`7`, `LabyrinthWorkshop`, `LabyrinthMinosTomb`, `LabyrinthStarryChamber`, `LabyrinthIcarusShaft`. Mt. Ida, the Idaean and Diktaean caves and the Cave of Eileithyia are unbuilt.

**First visit.** Amnisos, the Bull Road, the palace, the seven rings with the Thread, Labrys and Helm found inside.

| ID | Where | Relic | Seen first | Story | Pokémon | Also | Status |
|---|---|---|---|---|---|---|---|
| C1 | The Bull Road: **the labrys door** | Labrys | The door in the east cliff | The Bull Road vault | Kymbash, Kourodin 47–50 | Ichor Stone | Gate built (`KnossaBullRoad`) |
| C2 | **Mt. Ida and the Idaean cave** | Labrys | The seal on the Ida path | Where Rhea hid Zeus: the Kouretes' shields; Capricornus | **Kourodin Lv 52** | Capricornus; a vault | Designed (LABYRINTH §2) |
| C3 | Amnisos: **the Cave of Eileithyia** | Labrys | A stalagmite cave above the harbor, its inner door sealed | The birth goddess's cave; women's votives; a vault | Melisseer, Amnoze 47–50 | Phaistos Disc | Designed (LABYRINTH §9) |
| C4 | Amnisos: **Dia islet** | Conch | The islet across the bay | Ariadne's first night after the escape; a fisher's chapel | Galenyon, Kynoketos 45–48 | — | Proposed |
| C5 | **The Diktaean cave** | Crook | A cave mouth halfway down a gorge wall | **Rhea's turn** (LABYRINTH "hooks"): Rhea comes here after her mercy at the heart, to the cave where she bore Zeus. A scene with her, and Amalthea's storm-goat | **Kerastorm Lv 54** static (dex habitat: "the Diktaean cave") | Rhea's arc; Electric TM | Proposed |
| C6 | The palace: **the Temple Repositories** under the West Magazines | Hephaestus's Hammer | A boulder fallen through the magazines' floor | The snake-goddess figurines in their stone cists | Kymbash 45–48 | Phaistos Disc | Proposed |
| C7 | The Icarus Shaft: **the side ledges** | Winged Talaria | Ledges across one-tile gaps in the shaft | Icarus's practice perches | — | Daedalus's spare feathers (a Wings flavor item) | Proposed |
| C8 | Ring V's lake: **the drowned archive** | Pearl | The lake's floor, shelves of tablets below | Minos's laws, the judge's own, carried down when the ring flooded | Charonaut 64–68 | Linear tablets (lore) | Proposed |
| C9 | **Dikte eyrie**, Knossa's highest crag | Wings | A sighting stone on the Bull Road | Talos's lookout: the bronze giant's footprints, post-game | **Kolossard Lv 50** static | Talos lore | Proposed |

- **Caves with back sections:** the Idaean cave (C2), Eileithyia (C3), the Diktaean cave (C5), the Labyrinth (C8; the Endless Labyrinth in the post-game).
- **Routes to lengthen:** the Bull Road already has its door; Mt. Ida's path should be a full route (3–4 screens) with the Labrys seal at its top, not its foot.

### 5.8 Lakonia, Delphoi and the League (Act III)

**Maps:** `Ascent_1F`–`3F`, `Olympus_*`. Gytheion, Routes 24–30, Lakonia, Lake Stymphalia, Delphoi, Thermopylai and Tempe are unbuilt.

**First visit.** Gytheion, the Eurotas, Lakonia and the battle school, Stymphalia's marsh, Route 28 up the Kastalian falls (the Horn, main path), Delphoi, then the League road.

| ID | Where | Relic | Seen first | Story | Pokémon | Also | Status |
|---|---|---|---|---|---|---|---|
| D1 | Gytheion: **Kranai islet** | Conch | An islet with a ruined shrine, off the harbor | Paris and Helen's first night. A note that Helen never reached Troy: the **Haligeron/Proteus lead** into Egypt (OIKOUMENE) | Galenyon 46–48 | Oikoumene lore | Proposed |
| D2 | Route 25: **the Eurotas terraces** | Winged Talaria | Split banks along the river | — (minor) | — | Shortcut | Proposed |
| D3 | Lakonia: **the beehive tomb** (Vapheio) | Labrys | A domed tomb with a sealed inner door | The gold cups that show bull-catching: Asterion's people. A vault | Kourodin, Dorydrake 48–51 | Phaistos Disc | Designed (LABYRINTH §9) |
| D4 | Lake Stymphalia: **the reeds** | Sickle | Reed walls in the marsh | Open now: the Lernip rain hunt's best water | **Lernip** rain-only (BALANCE) | — | Proposed |
| D5 | Lake Stymphalia: **the roost in the mist** | Bag | A fog bank over the north marsh | Labor 6's birds before the Labor: a lone **Belornis** that won't leave | **Belornis Lv 72** | — | Proposed |
| D6 | Route 28: **the Hyampeia rock** | Crook | Handholds up the Phaedriades from the falls road | Delphi threw Aesop off this rock. A fox at the top tells fables, one per day | **Kerdovix Lv 50** static (the vixen) | A fable a day (a daily item) | Proposed |
| D7 | Delphoi: **the Cretan priests' shrine** | Labrys | A double-axe door in the temple terrace | Ends T11's thread: the Knossian sailors Apollo made his priests. Their shrine ties Delphoi to Knossa | **Mantipod Lv 54** static | Apollo Favor +10 | Proposed |
| D8 | Route 29: **the Korykian cave** | Crook | The plateau from T10, now reachable from above | **Pan's caves, the last.** The cave of Pan and the nymphs on Parnassos. Pan's syrinx (the quest's reward, §7) | **Pythoros Lv 56**; Pelython, Pythoros 52–55 | Pan's Syrinx (key) | Proposed |
| D9 | Thermopylai: **the Anopaia path** | Crook | A goat track up the cliff above the hot gates | The path the traitor showed. A Lakonian veteran guards the top and asks why you climbed | **Dorydrake Lv 58**; Hoplektor 54–56 | Shortcut round the pass | Proposed |
| D10 | Tempe: **Cheiron's cave** on Pelion | Wings | A sighting stone on Route 30: "The old centaur's cave. Nobody's been asked up." | Cheiron taught Asclepius, Jason and Achilles. He teaches you: a move tutor | — | Move tutor | Proposed |
| D11 | The Ascent: **the cloud bank** | Bag | Cloud that never clears off the 3F terrace | Olympus's cloud meadows, where **Pegaunos** grazes (LEGENDS: Lv 80). Bellerophon's chain ends here | **Pegaunos Lv 80** | — | Designed (POSTGAME §3.4) |
| D12 | The Ascent: **the storm face** | Crook | Handholds up a snow cliff off 2F | A storm terrace below the summit: **Olympanax**'s (LEGENDS: Lv 80) | Borapteryx, Aetarch 55–58 | — | Proposed |
| D13 | The Ascent: **rubble and drums** on 2F and 3F | Hammer | On the main line | Built side pockets: keep each paying | Ascent table 52–58 | Items | Built (`Ascent_2F`, `Ascent_3F`) |

- **Caves with back sections:** Vapheio (D3), the Korykian cave (D8), the Ascent floors (D11, D12; `Ascent_1F`–`3F` already have rubble and drum gates on the main line).
- **Routes to lengthen:** Route 28 (the Phaedriades tier above the falls), Route 29 (the Korykian plateau), Route 30 (a Pelion foothill strip).

### 5.9 The post-game lands

**Places:** Cape Tainaron and the Underworld, Olympia, Atlantis, Rhodos, the Odyssey's islands, Ithaka and Kerkyra; then the Oikoumene (`OIKOUMENE.md`).

| ID | Where | Relic | Seen first | Story | Pokémon | Also | Status |
|---|---|---|---|---|---|---|---|
| P1 | Routes 33 and 34: **the whirlpools** | Triton's Conch | Whirlpools in the post-game sea lanes | The way to Atlantis's waters and Rhodos | sea tables 60–66 | — | Designed (AETHOS_MAP) |
| P2 | **Atlantis** | Pearl | Plato's rings under the sea | POSTGAME's arc; Pontanax's temple ends the lead from K6, G1, G2 and A5 | Pontanax Lv 80 | — | Designed (POSTGAME) |
| P3 | **The Odyssey's fog** | Bag | The fog banks of the wine-dark sea | ODYSSEY | — | — | Designed (ODYSSEY) |
| P4 | Route 31, the Mani: **the tower cliffs** | Crook | Handholds up a sea cliff under a tower village | A Maniot family's tower and their feud | Hoplektor, Kaprodon 60–64 | — | Proposed |
| P5 | Tainaron: **the shadow door** | Helm of Hades | The cave gate opens only at night | By day too, after Hades returns the Helm (UNDERWORLD) | Underworld tables | — | Designed (SYSTEMS §1) |
| P6 | Rhodos: **the Colossus's vault** | Labrys | A sealed door in the fallen Colossus's base | The Telchines' last forge (S4's lead); a vault | Telkanvil, Kolossard 64–68 | Phaistos Disc | Proposed |
| P7 | Olympia: **the Alpheios crossing** | Horn | The river's cascade by the stadium | Alpheios chased the nymph Arethusa under the sea; a spring that comes up in Sicily, in the Oikoumene | Hymnaria 62–64 | Oikoumene lore | Proposed |
| P8 | The Oikoumene | all | — | `OIKOUMENE.md` §2 already gates its lands with the Conch (Scythia), the Torch (Hyperborea), the Horn (Aithiopia) and the Bag (Okeanos). Add the Crook to its mountain routes (Atlas's foothills, Mount Sipylos) | — | — | Designed, plus a proposal |

---

## 6. The matrix

Gates per region and relic, counted from the tables in §5 (A9 is a race, not a gate). Columns are in acquisition order: Ham(mer), Tor(ch), Sic(kle), Gir(dle), WTa (Winged Talaria), Crk (Pan's Crook), Con(ch), 3FT (Three-Flamed Torch), Wng (Wings), HHa (Hephaestus's Hammer), Hrn (Horn), Thr(ead), Lab(rys), Hlm (Helm), TCo (Triton's Conch), Prl (Pearl), Bag, HoH (Helm of Hades).

| Region | Ham | Tor | Sic | Gir | WTa | Crk | Con | 3FT | Wng | HHa | Hrn | Thr | Lab | Hlm | TCo | Prl | Bag | HoH | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Kalliste | 1 | 1 | 1 | 1 | 1 | 1 | 1 | · | 1 | · | · | · | 2 | · | · | 1 | · | · | **11** |
| Isthmus and Eleusa | 1 | 1 | 2 | 2 | 1 | 2 | 3 | 1 | 1 | · | · | 1 | · | 1 | · | · | · | 1 | **17** |
| Thyrsa, Kopais, Parnassos | 1 | · | 1 | 1 | · | 1 | 2 | · | 1 | 2 | 1 | 1 | 1 | · | 1 | · | 1 | · | **14** |
| Gulf, Arkadia, Nemea | 1 | · | · | 1 | 2 | 3 | 1 | 1 | 1 | 1 | 2 | · | · | 1 | 1 | 2 | · | · | **17** |
| Astyra and the Akropolis | · | · | · | · | 2 | 3 | 1 | 1 | 1 | 1 | · | · | 1 | 2 | · | 1 | · | · | **13** |
| Sea and the Kyklades | 1 | 2 | 1 | 1 | · | 3 | 2 | · | 1 | 3 | 2 | 1 | 2 | 1 | 1 | 1 | 1 | · | **23** |
| Crete and the Labyrinth | · | · | · | · | 1 | 1 | 1 | · | 1 | 1 | · | · | 3 | · | · | 1 | · | · | **9** |
| Lakonia, Delphoi, League | 1 | · | 1 | · | 1 | 4 | 1 | · | 1 | · | · | · | 2 | · | · | · | 2 | · | **13** |
| Post-game lands | · | · | · | · | · | 1 | · | · | · | · | 1 | · | 1 | · | 1 | 1 | 1 | 1 | **7** |
| **All regions** | **6** | **4** | **6** | **6** | **8** | **19** | **12** | **3** | **8** | **8** | **6** | **3** | **12** | **5** | **4** | **7** | **5** | **2** | **124** |
| **Regions reached** | 6 | 3 | 5 | 5 | 6 | 9 | 8 | 3 | 8 | 5 | 4 | 3 | 7 | 4 | 4 | 6 | 4 | 2 | |

**What the gates carry,** by region, counted from the Story and Pokémon columns (a "minor" gate is a shortcut or items only):

| Region | Gates | With a story or quest | With Pokémon | With a static, gift or lead above the area | Built, gate built or designed |
|---|---:|---:|---:|---:|---:|
| Kalliste | 11 | 10 | 10 | 7 | 4 |
| Isthmus and Eleusa | 17 | 17 | 15 | 11 | 9 |
| Thyrsa, Kopais, Parnassos | 14 | 14 | 14 | 9 | 0 |
| Gulf, Arkadia, Nemea | 17 | 16 | 15 | 12 | 4 |
| Astyra and the Akropolis | 13 | 12 | 11 | 9 | 0 |
| Sea and the Kyklades | 23 | 23 | 23 | 12 | 9 |
| Crete and the Labyrinth | 9 | 9 | 8 | 3 | 3 |
| Lakonia, Delphoi, League | 13 | 12 | 11 | 6 | 3 |
| Post-game lands | 7 | 7 | 6 | 0 | 4 |
| **All** | **124** | **120** | **113** | **69** | **36** |

**What the matrix shows:**
- **No region is gate-free.** The smallest, the post-game lands, still has 7 gates of 7 kinds, and its `OIKOUMENE.md` lands add more.
- **Every relic from the Girdle on opens things in several earlier regions.** The Crook reaches all nine regions; the Conch reaches all eight Aethos regions; the Wings reach eight; the Labrys seven; the Winged Talaria and the Pearl six; the Hephaestus's Hammer five.
- **The Act I relics** (Hammer, Torch, Sickle) have only Kalliste behind them, so they earn their counts the other way: as **first-visit gates** in later regions (T14, G17, S21–S23, D4, D13, S10). The player opens them on the spot, which teaches that old relics stay useful.
- **The thinnest columns** are the Three-Flamed Torch and the Thread (3 regions each) and the Helm of Hades (2). They are Favor- or post-game-gated, so that is by design; add a thornweb pocket to Crete or Lakonia if the director wants more.
- **Over half the gates carry a static, gift or legend lead** above the area's level (69 of 124), and nearly all carry a story (120 of 124). The four without one are the minor Talaria shortcuts.

---

## 7. Return loops

The natural points where the player gains a relic and has a reason to go back, and what pulls them.

| # | When | The player gains | Where it pays (gates) | What pulls them back |
|---|---|---|---|---|
| 1 | Act I, Emporion | Hammer, then Torch | K1, K2, I1, I16 | **The ferry to Akti** runs from the first arrival. Mom's scene, Euboulos's Charcoal, Hydna's "too still" water, and the Trowel's Kronos sherds (a dex-free collection pull) |
| 2 | End of Act I, Eleusa | Sickle | K3, I5, I17, T4 | Chloe's parting line about first fruits; the rites need berries, and the orchard and old grove have them |
| 3 | Act II, Thyrsa | Girdle | I4, I7, K4, T2 | **A letter from Kedalion:** "Somebody rolled drums up my back stair. Bring that girdle." Kalliste's drums are on the way home on the ferry |
| 4 | Act II, Arkadia | **Pan's Crook** | K5, I11, I15, T10, G4, G6, G9, A2, A3, A14 | **Pan's caves quest:** Pan says "I have three caves. Find the other two." (the Akropolis, A3; Parnassos, D8). An **omen** (SYSTEMS §6): a goat on a cliff, seen at dawn, marks a climbable face on the next route. Routes 13–14 and the capital road walk you past I11, I15 and A2 |
| 5 | Act II, Astyra | **Conch** | K6, I2, I10, I14, T5, T11, G1, A12, S3, plus the ten islands | **The sea opens.** The dolphin rides you out of the salt well into the harbor. Fishers name islands; the **Pontanax lead** (K6 → G1 → A5 → G2 → Atlantis) starts at home; the dex shows Water-type gaps on every coast |
| 6 | Act II end, Kaldera | **Wings** | K8, I3, T9, G13, A7, S17, C9, D10 | **Every herm goes live**, and every sighting stone read becomes a landing. **Bellerophon's chain** (I2 → I3 → T9 → D11) pulls across three regions |
| 7 | Hermes, Hecate, Hephaestus Favor 60 | Winged Talaria, Three-Flamed Torch, Hephaestus's Hammer | K7, I6, G14, G16, A1 · I9, G10, A6 · T1, T13, G7, A11, S2, S13, S14, C6 | **The god's priest writes** when Favor reaches 60, naming one gate the player has already seen: "There's a boulder on the cypress road. You know the one." |
| 8 | Act III, Kythera | **Horn** | T8, G5, G8, S5, S9 | The Naiad priestess names three silent falls on the mainland. The **Meloetta lead** sits behind G8 |
| 9 | Act III, Knossa | **Thread, Labrys, Helm** | I8, T7, S16 · K9, K10, T3, A13, S1, S6, C1–C3, C6, D3, D7 · I12, G11, A4, A10, S15 | **Daedalus's ledger:** "I sealed doors all over Aethos. Here's my list. Some of them I've forgotten." It marks the Labrys doors on the Fly map. **Ariadne** asks to visit Kalliste (K9). **Phaedon's tablet** at Trophonios (T7) pays off the reveal |
| 10 | Act III, Lakonia → Kirrha | All of the above | Every Act II region | **The main path walks back** through Arkadia, Styx Falls, Aigion and the ferry to Kirrha (AETHOS_MAP, Act III step 7). Put a gate the player can now open within sight of that road on each map: G4, G5, G6, G8, G11, T11 |
| 11 | Post-game | Triton's Conch, Pearl, Bag, Helm of Hades | K11, G2, G3, G12, A5, S11, S19, S20, T6, T12, D5, D11, I13, P1–P7 | **Legend leads** (LEGENDS: Pegaunos, Olympanax, Pontanax, Ichorin, Heatran), **Golden fractures** at Kronion, Eleusa, Kaldera and Delphoi (LEGENDS §7), **Phaistos Discs** for Silvally in every vault, and the Labors revisiting Nemea and Stymphalia |

**Two cross-region quests carry the loops:**
- **Bellerophon's spring** (Conch → Wings → Wings → Bag): Peirene (I2), Akrokorinthos (I3), Hippokrene (T9), then Pegaunos above the Ascent's clouds (D11). Each step's NPC names the next place.
- **Pan's caves** (Crook): Arkadia's grotto (G9), the Akropolis (A3), the Korykian cave (D8). Reward: **Pan's Syrinx**, a key item. Played in tall grass at noon, it makes the next encounter the area's rarest slot (once a day).

---

## 8. Build order

Most payoff first: finish gates that are already built or designed, then put new gates into the maps being rebuilt now, then the shared engine work that unlocks many gates at once.

| # | Build | Why first | Maps |
|---|---|---|---|
| 1 | **The Kalliste return pack:** the Kronion Crypt, Akti's Sea Grotto and the old grove (K1–K3) | Designed in `phase2/SCRIPT.md` with tables; the gates and teases are built; it's the first return every player makes | new `KallisteRoute1_KronionCrypt`, `AktiTown_SeaGrotto`, `KallisteRoute1_OldGrove` |
| 2 | **Emporion's cistern and the man in the jar** (I1) | Its gate script is built and promises a cave that doesn't exist | new `EmporionCity_Cistern` |
| 3 | **Gates in the Routes 7–14 rebuild** while those maps are open: T1, T4, T5, T7's anchor ring, T10, T11, G1, G4, G5, G14, G15, G16 | Cheapest moment: the maps are being redrawn now. Leave the space, the obstacle and the tease even where the place behind waits | `Route7_KroniaGrounds`, `Route8_KopaisRoad`, `Lebadeia`, `Route9_ParnassosCrossroads`, `Kirrha`, `Aigion`, Route 11, Route 13, `Nemea`, `Route14_NemeaRoad` |
| 4 | **Pan's Crook:** approve (Q1), turn on `OW_ROCK_CLIMB_FIELD_MOVE`, draw the handhold faces, script "Noon in Arkadia" | Unlocks ten Act I–II gates and the user's "rock climb" ask; the grotto and goatherd's house are built | `Arkadia`, `Arkadia_GoatherdHouse`, the Ladon reed bed |
| 5 | **The Akti islet** (K6) | Its tease is built and on every harbor view; first sea payoff; starts the Pontanax lead | new `AktiTown_Islet` |
| 6 | **Arkadia's waterfall cave** (G8) | Its tease is built; carries the Meloetta lead and the Orpheus sherds | new `Arkadia_UpperPool` |
| 7 | **The Route 12 bear's den** (G7) | Its boulder and sign are built; a strong static and a constellation | new `Route12_BearsDen` |
| 8 | **The Hephaisteion roof forge** (I4) and the Route 4 drum pocket (I7) | Designed; the Act II letter loop (§7, loop 3) needs a destination | `EmporionCity_Hephaisteion`, `Route4_Isthmus` |
| 9 | **Kaldera's two returns:** the Akrotiri door (S1) and the vent boulder's first chamber (S2) | Both designed (LABYRINTH §9, LEGENDS §7.2); Kaldera is the Wings hub | `Kaldera`, new `Kaldera_Akrotiri`, `Kaldera_LavaTubes` |
| 10 | **The eyrie template and three eyries:** Zas (K8), Akrokorinthos (I3), Kyllene (G13), with sighting stones | One small reusable map plus a fly-target flag; makes the Wings an exploration relic, not only fast travel | one eyrie layout, three section entries |

**Next after the ten:** the Kythera Labrys and Sickle gates whose scripts are TODO (S6, S10); Ariadne's door on Kalliste (K9); the Eleusa crypt (I12); Trophonios's descent (T7); Lykaion (G11); then the island set with the Conch (§5.6).

**Budget note.** Most gates are small pocket maps (one or two screens) reusing a region's tileset. The new art is the handhold faces (~15 metatiles), the thornweb and great-boulder objects, the eyrie layout and the deep-water patch: well inside the ~5 MB budget in `CLAUDE.md`.

---

## 9. Decisions for the director and the user

| # | Decision | Recommendation |
|---|---|---|
| Q1 | **Add Pan's Crook as relic 6** (Arkadia, after Laurel 5), reversing SYSTEMS §13's "Rock Climb optional only" | Yes. Dionysus's gift II then needs a new power; suggestion: the panther (gift III) arrives at II, and III becomes "Frenzy on demand" |
| Q2 | **A sixth Minoan vault on Aegina** (A13) and one on Rhodos (P6), beyond LABYRINTH §9's five | Yes for Aegina (Aphaia's flight from Minos is the link); Rhodos is optional |
| Q3 | **Ariadne's door on Kalliste** (K9): Ariadne visits the home island after Knossa | Yes; it pays off Naxos (Kalliste) being Ariadne's island in myth, and gives the Corona Borealis |
| Q4 | **Eyries as Wings-only landings** set by sighting stones | Yes; cost is one flag and one fly target each |
| Q5 | **Favor-60 letters** naming a seen gate (loop 7) | Yes; one text per god |
| Q6 | **Starter lines stay out of every gated table** (Hipling's, Kynder's and Nebrel's lines), except Daphnyad where BALANCE already places it | Yes |
| Q7 | **Pan's Syrinx** (rarest slot once a day) as the Pan's caves reward | Yes, if `ENGINE_API` can force a slot cheaply; otherwise a held item |
| Q8 | **The Korykian approach (T10) opens at the top only in the League** | Yes: T10 pays its own pocket in Act II, and D8 completes it from Route 29 |
| Q9 | **Kalliste's first two gates follow the built maps:** the Akti grotto is the Hammer's (rubble) and the Kronion Crypt is the Torch's (the dark stair), as SYSTEMS §1 and the built scripts have them. `phase2/SCRIPT.md`'s "Return to Kalliste" table has them the other way round | Follow the built maps; swap Phase 2's two encounter tables' level bands when the maps are built |
