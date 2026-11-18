# Ichor systems: relics, fire, rites and the specialty features

- **Owner:** Systems and level design.
- **Status:** a proposal for the user's approval. Nothing here is built yet.
- **Companion:** `design/LABYRINTH.md` covers the Knossa dungeon and its storyline, which is where most of these systems pay off.
- **Sources:** `design/PITCH.md` (the bible), `design/MAP_DESIGN.md` (the map rulebook), `design/research/RESEARCH.md`, `design/research/LAZARUS.md`, `design/phase1/SCRIPT.md` Part 5 (the Hearth Trial), `design/art/INVENTORY.md`, and the engine source as cited.
- **Authority.** This file is the source of truth for the relics' powers and upgrades (§1), fire and light (§2), the rites (§3: Favor, blessings and gifts), and the theoxenia gifts (§10).
  - The post-game docs, `LABORS.md`, `UNDERWORLD.md`, `ODYSSEY.md` and `POSTGAME.md`, are by another designer and reference these definitions.
  - Where this file places something in the post-game, such as the Nereid Pearl, Aeolus's Bag, Triton's Conch, the Helm of Hades, Hades's rite or the post-game theoxenia visits, it is a **hook**. Those docs own the arcs; this file owns the rules.
- **Maps.** Every map named here follows `design/MAP_DESIGN.md`. Where a feature adds rules for maps, they are written as additions to that rulebook, never exceptions.

Where this file disagrees with the bible, the change is listed in §16 and waits for approval. The user's open decisions are at the very end.

## How to read this file

Every feature has the same seven parts:

- **Play:** what the player does and feels.
- **Rules:** the numbers.
- **Myth and story:** the hook, and why it belongs in Aethos.
- **Where:** the acts and maps.
- **Engine:** the approach, the files it touches, the effort (Low, Medium or High) and the risk. Every engine claim names the code it rests on.
- **Cost:** ROM and art.
- **Flags and vars.**

Three conventions hold throughout.

- **New code is isolated.** Ichor's C goes in `src/ichor_*.c`, with headers in `include/ichor_*.h`. Hooks into vanilla files are one-line calls, so upstream merges stay easy (CLAUDE.md).
- **New state lives in one save struct.** Only **20 `VAR_UNUSED_*` lines remain** in `include/constants/vars.h`, against **332 unused flags** and **52 unused daily flags**. So new state goes into `struct IchorSave` inside SaveBlock3 (§14) or into flags, almost never into vars.
- **Species are placeholders.** Names come from PITCH §4. The Aethos dex (`design/dex/`, Aethos-only) will replace them. Where a mechanic depends on a species, this file specifies the role, and the dex fills it.

---

## 0. Summary

### Design principles

1. **No Pokémon ever needs a field move.** Relics are key items, used from the field.
2. **The main path never needs a time of day, a calendar date, luck or a grind.** Time, festivals, Favor and collections pay out in optional content and in power, never in progress.
3. **Teach in a temple, test in the Labyrinth.** Each temple trial introduces one puzzle verb. Knossa's seven rings combine the seven you have learned by then (LABYRINTH.md).
4. **Every system feeds another.**
   - Rites upgrade relics.
   - Digging fills amphorae, which point to rare Pokémon and place constellations.
   - Every town's herm carries you between towns from the start; herms you anoint on the routes join the Wings' fly map in Act II.
   - Daedalus's pages, found across Acts I–III, unlock the Labyrinth's secrets.
5. **Myth as rule, not lecture.** Hestia takes a share of every offering, because she took the first and last of every feast. Demeter refuses pomegranates. Nobody explains either.
6. **One blessing at a time, counted in steps,** like a Repel.
7. **Small engine edits, heavy data.** Most features are scripts and tables on top of systems the expansion already has.
8. **The map rulebook governs.**
   - Every relic opens something in a place the player has already been (§1, "Relic gates").
   - Every temple trial teaches its puzzle in the first room, tests it in the middle and masters it at the end (§12).
   - Every dungeon here teaches, tests and combines its mechanics, and every dead end pays (MAP_DESIGN §1, §3 and §4).

### The features at a glance

| # | Feature | In one line | Scope |
|---|---|---|---|
| 1 | Relics | 13 relics replace every HM and add four new verbs | 1.0 (2 are post-game) |
| 2 | Fire and light | Hecate's Torch, darkness, braziers you light for good, carried flames | 1.0 (halos stretch) |
| 3 | Rites | Pray or offer at about 60 altars; Favor with 15 gods; timed blessings; 3 gifts per god | 1.0 (tier III stretch) |
| 4 | Herm waystones | A travel herm at every town's gate, registered by its Asclepeion or a touch; route herms anointed for Hermes become Wings landing points | 1.0 |
| 5 | Excavation | Alethea's Trowel: coins, fossils, ostraka, 12 amphorae of myth, prophecy fragments, Daedalus's pages | 1.0 (paintings stretch) |
| 6 | Omens | One augury a day: a swarm, a rare visitor, the weather or a lucky sign | 1.0 |
| 7 | Festival calendar | 11 festivals on a 36-day Aethos year | 4 in 1.0, rest stretch |
| 8 | Katasterismoi | A star chart that fills with 24 constellations as you finish myths | stretch |
| 9 | Knucklebones | A tavern dice game with a real choice in it, and Mom at 212–0 | 1.0 |
| 10 | Xenia and theoxenia | Hosts who feed you, let you rest until dusk, and send you down token chains. Gods in disguise test your kindness and give you the old starters. | Xenia stretch. Theoxenia: core 1.0, extended a user choice (D8). |
| 11 | "Know thyself" | After prophecy ends, the Pythia hyper-trains instead of foretelling | 1.0 |
| 12 | Temple trials | One puzzle verb per Olympian, written as a family | 1.0 |

---

## 1. Relics

### Play

You never open the party menu to cut a bush. You walk up to a thorn thicket, press A, and your character raises Demeter's Sickle. One stroke, and the thicket falls. The relics are named things with stories, won on quests at the right point in the myth. Some of them grow: the Talaria sprout real wings once Hermes favors you.

Free-use relics (the Wings, the Torch, the Helm, the Thread) sit on a small **Relic Ring** under SELECT, so the common action is two presses.

### The relic table, in acquisition order

Main-path relics are in bold.

| # | Relic | Field power | When | Where, and from whom | What it opens on the main path | Upgrade |
|---|---|---|---|---|---|---|
| 1 | **Talaria** | Run (hold B) | Act I, before Laurel 1 | Elaia, Melitta (built in the slice) | — | Winged Talaria, at Hermes Favor 60: leap one-tile gaps |
| 2 | **Bronze Hammer** | Rock Smash | Act I, after Laurel 1 | Emporion, Kedalion at the Hephaisteion | The rockslide on the road to Eleusa | Hephaestus's Hammer, at Hephaestus Favor 60: great 2×2 boulders |
| 3 | **Hecate's Torch** | Flash; light braziers; burn webs; douse to see glow-paint | Act I, after Laurel 2 | Hecate's Hollow, a cave crossroads on the Eleusa road | Eleusa's trial and the Mystery sanctum | Three-Flamed Torch, at Hecate Favor 60: bigger radius, burns thornwebs |
| 4 | **Demeter's Sickle** | Cut (thickets, vines, reeds) | End of Act I, after Laurel 3 | Eleusa, Chloe, after the theft | The vine-choked road to Thyrsa | — |
| 5 | **Girdle of Herakles** | Strength (column drums) | Act II, after Laurel 4 | Thyrsa, Silenos the old actor | The drum-blocked pass to Arkadia | — |
| 6 | **Poseidon's Conch** | Surf, riding a dolphin | Act II, after the Akropolis battle | Astyra, the salt well under the Akropolis | Open sea; your own route to Thera | Triton's Conch, at Poseidon Favor 60: calm whirlpools (post-game Odyssey) |
| 7 | **Daedalus's Wings** | Fly | End of Act II, after Laurel 6 | Kaldera, Talos the Bronzesmith | Fly from anywhere, not only from a herm (herm travel between towns works from the start, §4). Every route herm you anointed goes live on the fly map. | — |
| 8 | **Horn of Achelous** | Waterfall | Act III, after Laurel 7 | Kythera, the Naiads of the Neraida falls | The Kastalian falls up to Delphoi, then the Ascent | — |
| 9 | **Ariadne's Thread** | Marks your path; ties anchors; escape | Act III, Knossa | Ariadne, at the Grand Staircase | The Labyrinth | Post-game: a longer spool |
| 10 | **Labrys** | Turns Daedalus's dials; cleaves labrys seals and bronze chains | Act III, Labyrinth Ring III | Daedalus | Labyrinth Rings IV–VII, then Minoan vaults | — |
| 11 | **Helm of Darkness** | Unseen in the dark | Act III, Labyrinth Ring V | King Minos's tomb | Rings V–VI | Helm of Hades, from Hades in the post-game: works in shadow by day |
| 12 | Nereid Pearl | Dive | Post-game | Atlantis | Atlantis | — |
| 13 | Aeolus's Bag | Defog; sail the fog banks | Post-game | The Odyssey | The Odyssey's islands | — |

Two **tools** sit beside the relics. They are key items, not relics.
- **Alethea's Trowel** (dig) comes from Alethea on arrival at Emporion, at the start of Act I proper (§5).
- **The Star Chart** comes from Daphne at the end of Act I (§8).

**Gating, act by act.**
- **Act I.** The Hammer clears the road to Eleusa. The Torch opens the trial and the sanctum. The Sickle ends Act I by opening the road to Thyrsa.
- **Act II.**
  - The Girdle opens Arkadia.
  - The Conch opens the sea. Thera is also reachable by the story trireme, so Surf never blocks the story.
  - The Wings arrive at Laurel 6, the same badge count at which Emerald gives Fly.
- **Act III.** The Horn opens Delphoi. The three Knossa relics are found inside their dungeon, Zelda-style.

### Relic gates: shown early, opened later

MAP_DESIGN §1 says every relic must open something in an area the player has already visited, with what lies behind it visible or hinted. Each relic does, besides its main-path gate.
- Several of these gates are **additions to maps already built or scripted** (Kalliste, Akti). Those are proposals for the map team, marked "slice map".
- Every gate below is optional. The main path never waits on a return trip.

| Relic | The gate the player sees first | Where, and when they first pass it | What's visible behind it | The return pays |
|---|---|---|---|---|
| Bronze Hammer | Marble rubble choking a sea-grotto mouth on Akti's tide rocks | Akti, the slice (slice map) | A glint of a sealed jar in the grotto's dark | The grotto: a Kalliste amphora sherd spot, a Pearl, and a rare shore Pokémon |
| Hecate's Torch | A black cistern mouth under Emporion's Agora steps, with a sign: "No light, no entry" | Emporion, Act I before the Torch | Dripping water; something's eyes catch light | Emporion's cistern: a small dark cave that teaches lit zones, with a TM, a sealed jar and a Ghost-type |
| Hecate's Torch, second gate | The dig pit on Kronion Hill now drops into a dark stair (the Titanborn dug deeper after the slice) | Kronion Hill, on any return to Kalliste | "It still feels like something's looking up" (the slice's own line) | The Kronion crypt: the Kronos-and-the-stone amphora's sherds, and an old altar to Kronos with Rhea carved weeping beside it (a seed for Delphoi's Omphalos) |
| Demeter's Sickle | A thorn thicket closing a terrace path above the Emporion road | The Emporion–Eleusa road, Act I | A sealed jar on the terrace above | A terrace orchard: a berry grove (first fruits for the rites) and a hidden item |
| Girdle of Herakles | Column drums blocking the Hephaisteion's back stair | Emporion, Act I | The stair rising to the roof | Kedalion's roof forge: a TM and Hephaestus Favor +5 |
| Poseidon's Conch | An islet with a white shrine off Akti's quay, seen from the slice's harbor | Akti, the slice (already on the slice's battle background and harbor views) | The shrine, and gulls circling | The islet: a Poseidon altar, a Water-type rare, and a hidden Big Pearl |
| Daedalus's Wings | Every herm anointed since Act I (§4) | Every route | — | Fast travel |
| Horn of Achelous | A waterfall beside Arkadia's temple with a cave mouth halfway up | Arkadia, Act II | The cave mouth, and a glint | The upper pool: the Orpheus amphora's sherds and the Meloetta lead (§5) |
| Ariadne's Thread | **The Wandering Halls,** a side tunnel in Hecate's Hollow. A sign: "Whoever goes in comes out where they went in." | Hecate's Hollow, Act I | A tunnel that loops you back to its mouth, whichever way you turn | With the thread laid, the loop breaks: its warps let a threaded walker through. The Hollow's deep shrine: Hecate Favor +10 and a Max Revive. |
| Labrys | A door in Kaldera's ash cliff with no handle, only a hollow shaped like a double axe | Kaldera, Act II | Painted plaster round the door: Minoan, under the ash | The first Minoan vault: Kaldera's buried town (LABYRINTH.md §9) |
| Helm of Darkness | Stone sentinels in the Mystery sanctum's crypt. They turn back anyone they see: "The uninitiated may not pass." | Eleusa, Act I | A dark stair past them | The crypt of the Mysteries: the last secret (lore), Demeter Favor +10 and an item |
| Alethea's Trowel | Turned earth appears on Kalliste after the slice | Kalliste, Route 1 and Kronion Hill | — | Kalliste's dig spots |
| Winged Talaria (upgrade) | One-tile gaps: a broken bridge, a split terrace | Routes in Acts I–II | An item ball across the gap | Shortcuts and items |
| Hephaestus's Hammer (upgrade) | Great 2×2 boulders | Caves in Acts I–II | A tunnel past them | Side caves |
| Three-Flamed Torch (upgrade) | Thornwebs, too thick for the plain torch | Hecate's Hollow, Ring III | The far side, dimly | Item pockets |

**Map notes for the relic-quest maps.** Each follows MAP_DESIGN §3.

| Map | Teach | Test | Combine | Every dead end pays | Payoff, then the way out |
|---|---|---|---|---|---|
| **Hecate's Hollow** (Act I) | The first fork. The bark comes clearly from one side. Both wrong branches are short and end in visible items: a Potion and a Barley Cake. | The second fork, darker and longer. One wrong branch has an optional trainer, a torch-less Augur. | The third fork. The bark echoes, so you must listen twice. A draught from one branch is a second clue, and it previews the wind verb. | Yes: items or a trainer at every branch end | The Hekataion and the Torch. Then the lit shrine passage is a short exit back to the road. |
| **The salt well** (Act II, 2 floors) | Tide pools by the stair: a shallow pool you can wade, with an item | A floor where the tide line has stranded a trainer on a rock (mandatory, easy) and a fork | The lower floor: wading plus a dark grotto, so the Torch and the tide work together | Each side grotto holds a sea gift or a trainer | The dolphin and the Conch. Then a sea-door opens to the harbor, and you ride out on the dolphin. |
| **The Neraida falls** (Act III) | Route rules (MAP_DESIGN §1): forced grass below the falls | — | — | The pool above the falls holds Daedalus's page VII | The Horn. Then climb out to the Kythera road. |

### Changes from the bible, and why

- **Cut is Demeter's Sickle, not the Labrys.** Cut has to arrive by the end of Act I, but the Labrys belongs to Knossa in Act III. The myth fits too.
  - Apollonius (*Argonautica* 4) says the island of Drepane hides a sickle. It is either the one Kronos used on his father, or the one Demeter used to teach the Titans to reap.
  - So at Eleusa the Titanborn dig for one sickle and walk straight past the other. The player carries the sickle that feeds people, against the one that cut a father.
- **The Labrys becomes the Labyrinth's dungeon tool.**
  - *Labyrinthos* likely means "house of the double axe", from *labrys*.
  - It is found mid-dungeon and solves the second half: the dials, the seals and Asterion's chains. Afterwards it opens optional Minoan vaults.
  - Attic vase-painters also gave Hephaestus a double axe for splitting Zeus's brow at Athena's birth. It is the axe that opens what was sealed.
- **Waterfall is the Horn of Achelous (new).**
  - Achelous, a river god, wrestled Herakles in the shape of a bull. Herakles broke off a horn, and the Naiads filled it with fruit: the cornucopia.
  - A horn that climbs rivers is the river god's own, and a bull's horn rhymes with the Labyrinth.
  - Kythera has a real waterfall named for the nymphs (Neraida).
- **New: Ariadne's Thread.** It is the game's theme in one object. The hero is "the Unwoven", and this is the thread they hold.
- **New: the Helm of Darkness.**
  - The Cyclopes forged it for Hades to fight the Titans (Apollodorus 1.2.1). It is the anti-Titan relic, and you wear it into Team Titan's headquarters.
  - Minos, Knossa's dead king, became a judge of the dead. The Helm lies in his tomb, and the post-game Underworld asks for it back.
- **The Girdle of Herakles stays, with one flag.**
  - The post-game's ninth Labor is "the Girdle of Hippolyta", so the game would have two girdles.
  - I recommend renaming the Labor's prize **Hippolyta's War-Belt**. This is decision D2.
- **Athena's polished shield is not a relic in 1.0** (§13).
- **Aeolus's Bag stays in the post-game,** as the bible has it.

### The myth-quests

Each relic is a short quest of 5 to 20 minutes. None needs a time of day.

**1. Talaria.** Built in the slice: Mom's gift. The cobbler stitched wings on them for luck.

**2. Bronze Hammer: "The Cold Forge" (Emporion).**
1. A small Hephaisteion stands above the Agora, as Hephaestus's temple overlooks Athens's Agora.
   - Its forge went cold during the halcyon calm. This is the same calm that holds the trireme at Akti.
   - The keeper, **Kedalion**, can't relight it with ordinary fire. In myth, Kedalion was Hephaestus's servant, who carried blind Orion on his shoulders.
2. He explains the colonists' custom, which is real: a new hearth is lit from the mother city's hearth, which never goes out.
3. The player shows the **Charcoal** from Hestia's hearth, the slice's trial reward. Kedalion takes a sliver and leaves the item.
   - If the player no longer has it, Euboulos in Akti gives another on request.
   - Emporion's Agora stocks Charcoal from then on.
4. The forge roars. Kedalion hands over the Bronze Hammer, which hung over the forge as a votive. Hephaestus Favor +5.

**3. Hecate's Torch: "The Three Roads" (Hecate's Hollow, on the Eleusa road).**
1. A cave junction where three tunnels meet is pitch dark, even at noon. The player has no light yet, so the flash radius is 24 px, about one and a half tiles.
2. A dog barks somewhere ahead. It is Hecate's black hound, a Houndour as placeholder.
   - At each three-way fork the bark comes from the correct branch, through left, right or centre audio panning. A text cue also says "The barking comes from your left," for players without sound.
   - Three forks lead to the **Hekataion**, a three-faced pillar.
3. The altar of Hecate gives the rites tutorial (§3) if the player hasn't had it yet: "Leave her supper at the crossroads." It takes any offering, and a Barley Cake sits ready on the pillar's ledge.
4. The three faces' torches kindle one by one. The player receives the Torch.
5. **Optional, at night:** come back after 20:00 and the hound appears with two more. It is a static encounter, a Dark-type at Lv 22, and catchable.

**4. Demeter's Sickle: "The Other Sickle" (Eleusa, Act I climax).**
1. The trial (§12) ends with Chloe's reveal in the dark: a single ear of grain, reaped in silence. This is the Eleusinian Mysteries' secret, as the sources hint.
2. The Titans then rob the Mystery sanctum of the first Harpe fragment (PITCH Act I step 4).
3. In the wreck of the sanctum, Chloe finds the bronze harvest sickle that the Titanborn tossed aside.
4. CHLOE: "They came for a sickle. They didn't know there were two."
5. She gives it to the player for the road. It is the sickle Demeter used to teach the reaping, in Aethos's telling.

**5. Girdle of Herakles: "Herakles Lost a Drinking Game" (Thyrsa).**
1. Herakles once lost a drinking contest to Dionysus. Antioch's mosaics show it.
2. In Aethos the stake was Herakles's girdle, and the theater's prop master **Silenos** keeps it. In myth Silenus was Dionysus's tutor, an old drunk.
3. Silenos gives it to anyone who beats him at two of three contests.
   - **Knucklebones** (§9). Silenos's bones are loaded. Call "Loaded!" after he throws two sixes twice running, and you win that contest.
   - **A riddle.** You get three tries, and a new riddle after each miss.
   - **A battle,** with Silenos's team at Lv 33–35.
4. Losing simply lets you try again. The Girdle pushes **column drums**, which replace Emerald's boulders (INVENTORY §1).

**6. Poseidon's Conch: "The Salt Well" (Astyra).**
1. After the Akropolis battle, the Akropolis's caretaker shows the trident marks in the rock. Poseidon struck the rock when he and Athena contested the city, and a salt spring welled up: the "sea of Erechtheus".
2. The well roars when the south wind blows. Below it is a short sea-cave dungeon of tide pools, 2 floors, with Water-type encounters at Lv 36–39.
3. At the bottom a dolphin surfaces with a conch in its mouth.
   - In myth, Poseidon's dolphin found Amphitrite for him and was set among the stars.
   - DOLPHIN: no words. It nudges the shell into your hands.
4. Blowing the Conch at the shore calls the dolphin, and you ride it. This is the Surf sprite (art in §1 Cost).
5. The **Delphinus** constellation is placed (§8).

**7. Daedalus's Wings: "What the Fire Gave Back" (Kaldera).**
1. After Laurel 6, Talos takes you into the back of the forge.
2. Years ago an old man threw a pair of wax-and-feather wings into this fire. Talos pulled them out.
3. TALOS: "He said not too high, not too low. Then he threw them in my forge."
4. TALOS: "They aren't mine to give. Take them back to him. He's under Knossa. He'll want to know they still fly."
5. This sets up Knossa: you meet Daedalus wearing his own wings (LABYRINTH.md, the workshop scene).
6. Talos is Daedalus's former apprentice. This is new backstory, decision D8 (LABYRINTH.md).

**8. Horn of Achelous: "The Silent Falls" (Kythera).**
1. Kythera's Neraida falls have gone silent. The water still falls but makes no sound: the calm again.
2. The Naiads' spring-shrine at the foot keeps a horn wreathed in dead flowers.
3. A Naiad priestess tells the myth in two lines: the river god wrestled a hero as a bull, lost a horn, and the nymphs filled it with fruit.
4. Fill it again. Offer **First Fruits**, any 3 berries, at the spring altar (§3).
5. The horn fills, the falls roar, and the priestess gives it to you: "It climbs water the way he did."
6. Aphrodite Favor +5.

**9–11. Ariadne's Thread, the Labrys and the Helm** are in LABYRINTH.md.

**12–13. The Nereid Pearl and Aeolus's Bag** are post-game, designed with the Atlantis and Odyssey arcs. Their engines are Dive (vanilla) and Defog (`OW_DEFOG_FIELD_MOVE` already exists in `include/config/overworld.h`).

### Using relics: the prompt and the Relic Ring

**Contextual relics.** These are the Hammer, Sickle, Girdle, Conch, Horn, Labrys, Trowel, and the Torch when used on braziers and webs. Face the obstacle and press A.

- **Option "Relic prompts": ASK (default) or AUTO.**
  - ASK:
    ```text
    A thorn thicket.

    Cut it with Demeter's Sickle?
    ```
    ?? YES/NO
  - AUTO shows one box and no question:
    ```text
    {PLAYER} cut the thicket with Demeter's Sickle.
    ```
- **Surf and Waterfall** always need the A press, even on AUTO, so the player never rides off a pier by accident.
- **Without the relic,** the text describes the obstacle and hints at a tool. It never mentions a Pokémon:
  ```text
  A thorn thicket. A good blade would clear it.
  ```

**Free relics.** These are the Wings, the Torch (light or douse), the Helm (on or off), the Thread, the Star Chart, and Hestia's stored heal while you hold her blessing.

- **SELECT opens the Relic Ring,** a menu in the top-right corner with up to 6 entries.
  - The first entry is the item registered in the bag, if there is one (for example the Old Rod). The owned free relics follow, in a fixed order.
- **The cursor starts on the last entry you used,** so SELECT then A repeats your last action. B closes the ring.
- Entries that can't be used here are greyed out with a reason ("No sky to fly in").

**The pose.**
- The player raises the relic, using the field-move pose sheet, which is already Greek (INVENTORY §2).
- The relic's icon flashes above their head and a short relic chime plays. No Pokémon cut-in appears.
- If a follower is out, it hops beside you, as the expansion's follower field-move code already does (`EventScript_FollowerFieldMove` in `data/scripts/field_move_scripts.inc`).

**Obstacle art.** INVENTORY §1 lists three swaps:
- the cut tree becomes a thorn thicket;
- the breakable rock becomes marble rubble;
- the boulder becomes a column drum.

New obstacles: a cobweb (Torch), a labrys seal (Labrys), a dig spot (Trowel), a great boulder (Hephaestus's Hammer) and a whirlpool (Triton's Conch, post-game).

**Where relics don't work.**
- In the Endless Labyrinth, which keeps the Battle Pyramid's bag rules.
- Inside a temple trial that forbids outside tools. Hestia's house says so, for example.

### Engine

| Change | Where | Effort |
|---|---|---|
| 13 key items with `fieldUseFunc`s, sorted first in Key Items | `src/data/items.h`, `include/constants/items.h` | Low |
| Obstacle scripts check the bag instead of the party. Replace `checkfieldmove FIELD_MOVE_CUT, TRUE` with `checkitem ITEM_DEMETERS_SICKLE`, drop `bufferpartymonnick`, and rewrite the text. The same applies to Rock Smash and Strength. | `data/scripts/field_move_scripts.inc` | Low |
| Water checks. `GetInteractedWaterScript` tests `IsFieldMoveUnlocked(FIELD_MOVE_SURF) && PartyHasMonWithSurf()`; make it test for the Conch. Waterfall gets the same treatment, as do the Dive checks in `TrySetupDiveDownScript` and `TrySetupDiveEmergeScript`. | `src/field_control_avatar.c` (around line 643) | Low |
| Hide field moves in the party menu: set each `unlockType` to `CANT_UNLOCK` with `hideIfLocked`, so no Pokémon offers to cut | `src/field_move.c` (`gFieldMoveInfo`) | Low |
| Fly from the Wings. The expansion's `OW_FLAG_POKE_RIDER` already lets the Town Map fly with R (`src/field_region_map.c` lines 191 and 245). Point it at `FLAG_ICHOR_GOT_WINGS` and open the fly map from the Wings item. | `include/config/overworld.h`, `src/item_use.c` | Low |
| The Relic Ring. `UseRegisteredKeyItemOnField` (`src/item_menu.c`, around line 2160) runs one registered item or falls back to `EventScript_SelectWithoutRegisteredItem`. Replace the fallback, and the registered path once the player owns a free relic, with a script that builds a `dynmultichoice` (`asm/macros/event.inc`, around line 1950). | `src/item_menu.c`, a new `data/scripts/ichor_relics.pory` | Low–Medium |
| The "Relic prompts" option: one row, stored in a spare options bit | `src/option_menu.c` | Low |
| The relic pose. The field-move effect shows a Pokémon cut-in; add a relic variant that skips the cut-in and shows the item icon (`AddItemIconSprite`) over the player. | `src/field_effect.c` | Medium |
| The Winged Talaria gap leap. Add a metatile behavior `MB_ICHOR_GAP`. With the upgrade flag set and the player running, walking into a gap plays the two-tile jump that ledges already use. | `src/field_player_avatar.c`, `src/metatile_behavior.c` | Medium |

**Risk: low.**
- The follower field-move code (`isfollowerfieldmoveuser`) expects a party slot argument. Pass "none" and keep the hop.
- Nothing here touches battle code.

### Cost

| Item | Size |
|---|---|
| 13 relic icons and 2 tool icons (24×24) | ~5 KiB |
| Obstacle sprites: cobweb, labrys seal, dig spot, great boulder | ~3 KiB |
| Surf on a dolphin: 2 player sheets, which replace the "surfing" row in INVENTORY §2 | ~4 KiB |
| Fly: the player on wax wings replaces the Fly bird field effect | ~2 KiB |
| Text | ~8 KiB |
| **Total** | **~22 KiB** |

### Flags and vars

- `FLAG_ICHOR_GOT_<RELIC>`, one for each of the 13 relics. Scripts and the Scroll of Deeds read these, not the bag.
- Upgrade flags: `FLAG_ICHOR_WINGED_TALARIA`, `_THREE_FLAMED_TORCH`, `_HEPHAESTUS_HAMMER`, `_TRITON_CONCH` and `_HELM_OF_HADES`.
- State flags: `FLAG_ICHOR_TORCH_DOUSED` and `FLAG_ICHOR_HELM_ON`.
- `OW_FLAG_POKE_RIDER` is set to `FLAG_ICHOR_GOT_WINGS`.
- **No vars.**

---

## 2. Fire and light

### Play

- **Darkness is real.** Some caves are dark, as are the Mystery sanctum, Hecate's Hollow and the Labyrinth. Without a light you see a tile and a half around you. Hecate's Torch pushes that to three and a half.
- **Braziers stay lit.** Light a bronze brazier and its room or zone becomes fully lit, permanently. Coming back to a cave you have lit up feels like coming home, and the braziers are your own landmarks.
- **Webs burn.** Ariados country is full of them.
- **Douse to see.** Some paint glows only in full darkness: Hecate's chalk, and Daedalus's own trail marks.
  - Douse your torch from the Relic Ring. The walls vanish, and the glowing marks show across the whole screen.
  - Relight to see where the walls are. Walking a route by alternating the two is the Mysteries' puzzle (§12).
- **Carried flames are a language.** Some braziers take only a named fire: the hearth's, the sanctum's, the threshold's. Your torch can carry that fire, but only for a set number of steps.

### Rules

**Light radius.** These are the expansion's flash levels; `sFlashLevelToRadius` is 200, 72, 64, 56, 48, 40, 32, 24 and 0 px, in `src/field_screen_effect.c`.

| State | Flash level | Radius |
|---|---|---|
| Dark map, no torch | 7 | 24 px (1.5 tiles) |
| Hecate's Torch | 3 | 56 px (3.5 tiles) |
| Three-Flamed Torch, or Hecate's blessing | 2 | 64 px (4 tiles) |
| Both | 1 | 72 px (4.5 tiles) |
| Inside a lit zone | 0 | full light |
| Torch doused | 8, with the glow palette | glow-paint only |

**The carried-flame grammar.** Six verbs, which temples and dungeons combine:

1. **Order.** Light braziers in a sequence (Hestia's hymn).
2. **Relay.** A named fire lasts N steps on your torch, then turns ordinary. Any brazier already lit with that fire relights it. Puzzles become routes where each hop is shorter than N.
3. **Return.** The last flame goes back to its source (Hestia).
4. **Wind.** Draughty doorways, marked by fluttering ribbons, blow out a carried flame. This shapes the route.
5. **Water.** Surfing, falling into water or climbing a waterfall puts out a carried flame.
6. **Reveal.** Some things exist only in a brazier's light: an inscription, a hidden stair or a doorway in the fresco.

**Fairness rules.**
- Losing a carried flame resets only the current puzzle. Braziers you have already lit stay lit.
- The step count left shows in the start-menu info panel ("Hearth fire: 12 steps").
- At 5 steps left: "The flame gutters."

### Myth and story

- Hecate lit Demeter's search for Persephone with torches (the Homeric *Hymn to Demeter*).
- Athens ran torch-relay races (the *lampadedromia*) at the Panathenaia (§7).
- Colonists carried hearth fire from the mother city.
- Prometheus stole fire, and Hestia never let hers go out.

The slice already taught the grammar's first and third verbs.

### Where

- About 10 dark caves across Acts I–III, starting with Hecate's Hollow.
- The Mystery sanctum (Act I).
- The Labyrinth (Act III).
- Tartarus (post-game).
- Carried-flame puzzles: the Hearth Trial (done), the Demeter trial, the Panathenaia torch race, and Labyrinth Rings I and III.

### Readable darkness: map rules

These add to MAP_DESIGN §3 ("dark areas should still be readable; lit braziers become landmarks") and §6 (the 15×10 test).

1. **Teach light first.** Every dark map has a lit brazier, a skylight or a glow-mark within its first screen, so the player sees what light does before they need it.
2. **Rim-lit walls.** Dark tilesets give walls a lighter top edge, so the wall line reads clearly inside a 3.5-tile torch radius.
3. **A landmark every screen, even in the dark.** A brazier, glow-paint, a skylight, a fresco catching the torch: no screen of pitch dark is empty. A pitch-dark corridor runs at most 2 screens (30 tiles) before the next landmark.
4. **Lit zones repay the lighting.** Every brazier you light reveals something worth seeing: a fresco, an item, a shortcut or a hidden door.
5. **Checkpoints stay readable.** Never put a mandatory trainer's sight line in pitch dark. A lamp or brazier marks every mandatory trainer, so the checkpoint is visible before it is crossed.
6. **Ordinary caves** (not the Labyrinth) get a lit exit passage once their payoff is reached, the "shortcut back out" MAP_DESIGN §3 asks for.

### Engine

- **Darkness.** A map's header `cave` flag drives `SetDefaultFlashLevel` (`src/overworld.c`, around line 1105), which checks `FLAG_SYS_USE_FLASH`. Replace that check with `Ichor_GetTorchFlashLevel()`, which returns 7, 3, 2 or 1 from the relic, its upgrade and the blessing. **Low.**
- **Lit zones (1.0).**
  - Coord events on a zone's thresholds run `animateflash 0` going in and `animateflash <torch level>` going out (macros in `asm/macros/event.inc`).
  - The zone's state is one bit in `IchorSave.litBraziers` (128 bits, §14). `ON_TRANSITION` restores it. **Low.**
- **Brazier halos (stretch).** In open caves, a lit brazier could carve a permanent pool of light even outside the torch radius.
  - Method: a 64×64 circle sprite with `copyToObjWin` at each lit brazier, plus `WINOUT_WINOBJ_BG_ALL | WINOUT_WINOBJ_OBJ`, so the map shows through the object window.
  - Precedent: `ShowItemIconSprite` (`src/overworld.c`, around line 3776) already sets `DISPCNT_OBJWIN_ON` and `WINOUT_WINOBJ_OBJ` so an item icon shows in darkness.
  - The halos must follow the camera like field-effect sprites. **Medium.**
  - Risk: sprite count, and interplay with the day/night tint. Test in mGBA before committing to it.
- **Douse.**
  - Load a "glow" copy of the map's palettes, with every slot black except the glow index, and set flash level 0. Relighting restores both.
  - Each dark tileset needs one extra palette set, planned in Porytiles. **Low–Medium.**
- **Webs.** Object events with a script and a hide flag, like cuttable trees. **Low.**
- **Carried flames.** The map's `VAR_TEMP_2` holds steps left and `VAR_TEMP_3` holds the flame's kind. Both reset on a map change, which also matches the rule "the flame dies when you leave".
  - A tiny step hook in `Ichor_OnStep` decrements the count. The Hearth Trial's scripts (SCRIPT.md Part 5) are the template. **Low.**

### Cost

- Brazier metatiles (2×2, lit and unlit) in each dark tileset, counted in the biome tilesets.
- Glow palettes: 32 bytes each.
- Halo sprite: 2 KiB (stretch).
- Web sprite: 0.5 KiB.

### Flags and vars

- `IchorSave.litBraziers` (128 bits; every brazier in the game has an index).
- `VAR_TEMP_2` and `VAR_TEMP_3` (per map).
- `FLAG_ICHOR_TORCH_DOUSED`.

---

## 3. Rites: worship as a living system

### Play

Aethos is full of altars.

- **In towns:** every town has an altar of its temple's god, and every home has a hearth, Hestia's altar. The slice's tilesets already include the household altar of Hestia and the harbor shrine to Poseidon.
- **On the roads:**
  - herms for Hermes;
  - Hekataia at crossroads for Hecate;
  - laurel shrines on hills for Apollo, ivy shrines in vineyards for Dionysus, grain shrines in fields for Demeter;
  - forest shrines for Artemis and owl stelai in cities for Athena;
  - battle trophies (*tropaia*) for Ares and myrtle shrines at springs for Aphrodite;
  - wellheads for Hera and oaks on the peaks for Zeus.

There are about 60 altars in all. Walk up to one and press A:

```text
An altar of Apollo, crowned with laurel.
```
?? PRAY / MAKE AN OFFERING / FAVOR / LEAVE

- **PRAY.** Free.
  - "You pray to Apollo." Then one line in the god's manner: a laurel leaf turns in a windless air, or an owl calls once.
  - You get the god's **minor blessing**. Once a day per god, a prayer also earns +1 Favor.
- **MAKE AN OFFERING.**
  - The bag opens, showing only offerings. Pick one, and the god reacts by preference.
  - You get the god's **major blessing** and some Favor.
- **FAVOR.**
  - "Apollo knows your name." Then your rank, and how far it is to the next gift.
- **Replacing a blessing.** If another god's blessing is active, the altar asks first:
  ```text
  Artemis's blessing is still on you. Pray anyway?
  ```
  ?? YES/NO

Your follower faces the altar and shows a small emote. Small, but it makes the act feel shared.

### Rules: Favor

Each god has Favor from 0 to 100. It **never decreases.**

| Deed | Favor |
|---|---|
| Pray: the first prayer each day to that god | +1 |
| Offering the god loves, likes, or merely accepts | +5, +3, +1 |
| …made at that god's own temple altar | ×2 |
| Win that god's laurel or Pantheon seat | +15 |
| Finish that god's myth-quest | +10 |
| Take part in that god's festival (§7) | +5 |
| Cleanse a desecrated altar (below) | +3 |
| **Any** offering, to any god | **Hestia +1.** She takes the first share of every feast. |

**Ranks:** 10 **Known**, 30 **Favored** (gift I), 60 **Beloved** (gift II) and 100 **Chosen** (gift III).

**Pacing.**
- Winning a temple plus three loved offerings at its altar is 15 + 30 = 45 Favor. So gift I usually lands right after each temple.
- Beloved costs about 8 more loved offerings.
- Chosen costs about 20 more, roughly 6,000–12,000 money at Agora prices. That puts it in the late game and post-game, where it belongs.

**One wrong offering.** Demeter turns away from a pomegranate (the Pomeg Berry): +0 Favor, and the line "Demeter looks at the fruit for a long time. She does not take it." Every other offering is at least accepted. The game never punishes generosity.

**Desecrated altars.**
- In Acts I–III, Team Titan has scratched sickles into about 12 roadside altars, and a Titanborn guards each one.
- Beat the guard, then pray to cleanse the altar: +3 Favor to its god, and the altar works again.
- This side activity shows the Titans' contempt for the gods without a speech.

### Rules: blessings

- **Only one is active at a time.** It is stored as a god and a step count.
- **Duration:**

  | Source | Steps |
  |---|---|
  | Prayer | 100 (150 once you are Known) |
  | Liked offering | 300 |
  | Loved offering | 500 |
  | At Beloved rank | ×1.5 |
  | Cap | 4,095 (12 bits) |

- **Expiry:** "Apollo's light fades from you." This works like Emerald's Repel message.
- **Display:** the start-menu info panel shows "Blessing: Apollo (412)".
- **Difficulty:**
  - Blessings work on every difficulty.
  - On Spartan, EXP boosts still respect level caps.
  - Under the Oath of the Styx, Hestia's stored heal never revives a fainted Pokémon.

**Gift III species.** Under dex decision D5 (a), only Aethos species appear before the League. So each god's sacred animal is cast from the Aethos dex. The bible's old vanilla picks (Magearna, Zapdos) stay in the post-game national dex, not here.

### The gods

There are 15 gods: the Twelve, plus Zeus, Hecate and, in the post-game, Hades. Under "Gifts", **I** is Favor 30 (a TM, named by its move; Balance assigns the numbers), **II** is Favor 60 (a tool or relic upgrade), and **III** is Favor 100 (the god's sacred animal as a unique static encounter, with a strong nature, 3 perfect IVs and a rare move; species pending the dex).

| God | Loves / likes | Major blessing | Gifts |
|---|---|---|---|
| **Hestia** | Olive Oil / Barley Cake, Honey | **Hearthfire.** Stores one full party heal. Use it from the Relic Ring anywhere outside battle; the blessing ends when used. The minor version heals HP only. | **I** Wish (tutor)<br>**II** **Ever-Ember**: Hearthfire no longer counts down, and you can heal at any home's hearth<br>**III** the hearth donkey: Kanthos's foal, Akti's temple donkey from the slice |
| **Hermes** | Honey / Frankincense, Olive Oil | **Swift Trade.** Agora prices −20% when buying and +20% when selling; trainer prize money +20%. | **I** U-turn<br>**II** **Winged Talaria**: gap leaps<br>**III** the lyre-tortoise |
| **Demeter** | Barley Cake / First Fruits (any berry except Pomeg) | **Harvest.** Wild Pokémon carry held items twice as often; berry trees give +1; each dig rolls twice and keeps the rarer result. | **I** Leech Seed<br>**II** **Harvest Basket**: berry trees always give +1<br>**III** her chariot-serpent |
| **Dionysus** | Wine / Figy and Grepa Berries (fig and grape) | **Revel.** Gives a random other god's major blessing at 1.5× duration (never Zeus or Hades). One time in eight it is **Frenzy** instead: wild encounters ×2, wild levels +3, EXP ×1.5. | **I** Swagger<br>**II** **Thyrsus**: climb marked ivy walls (the expansion's Rock Climb), opening optional ledges<br>**III** the panther |
| **Artemis** | Any feather (the first of the hunt) / Barley Cake (her moon-cakes) | **Moonlit Hunt.** At night, a route's three rarest land slots are 3× as likely; wild encounter rate −25% at all times; the Augur's Eye sneaking range +2 tiles. | **I** Night Slash<br>**II** **Hunter's Moon**: the Augur's Eye lists each map's rare-slot species<br>**III** the golden-horned deer |
| **Hephaestus** | Bronze Votive / Wine (he came home to Olympus drunk) | **Forge-sight.** Hidden items within 6 tiles glint every 2 seconds; smashed rocks drop items 3× as often. | **I** Flash Cannon<br>**II** **Hephaestus's Hammer**: great boulders<br>**III** the golden automaton |
| **Aphrodite** | Frankincense / Pretty Feather (her doves), sea gifts | **Charm.** Friendship gains ×2; wild Pokémon are the opposite gender of your lead two times in three. | **I** Draining Kiss<br>**II** **Myrtle Wreath**: a held item; friendship can't drop<br>**III** the swan |
| **Apollo** | Laurel Sprig / Frankincense, Honey | **Daylight.** EXP +20%. | **I** Solar Beam<br>**II** **Lyre of Apollo**: plays a tune that wakes sleeping blockers (Emerald's Poké Flute)<br>**III** the raven |
| **Ares** | No item: a fight. "Offer a battle" at his trophy and a daily war-acolyte, levelled to your party, battles you. | **War-lust.** Wild Pokémon 5+ levels below your lead don't appear; wild levels +2; EXP +10%. | **I** Bulk Up<br>**II** **War Horn**: the expansion's VS Seeker, to rematch beaten trainers<br>**III** the war-dogs |
| **Poseidon** | Sea gifts (Pearl, Big Pearl, Shoal Salt, Shoal Shell, Heart Scale) / Wine, Barley Cake (sailors' barley) | **Calm Seas.** Every cast gets a bite at once; surfing encounters −50%; the rods' rare slots ×2. | **I** Scald<br>**II** **Triton's Conch**: calms whirlpools<br>**III** the hippocampus |
| **Athena** | Olive Oil / Frankincense, Honey | **Owl's Eye.** The Augur's Eye finds hidden Pokémon twice as often (+10% hidden-ability chance); escape from wild battles always succeeds. | **I** Calm Mind<br>**II** **Athena's Stylus**: the Scroll of Deeds shows a hint for every open quest<br>**III** the owl |
| **Hera** | Pomeg Berry (the pomegranate) / Pretty Feather (the peacock), Honey | **Queen's Care.** Eggs hatch twice as fast; the day care finds eggs twice as often. | **I** Protect<br>**II** **Eyes of Argus**: the Augur's Eye detector runs constantly and shows shiny sparkles from 8 tiles<br>**III** the white cow of Argos |
| **Zeus** | Wine (the first libation of every feast) / Frankincense, Honey; also +3 Favor per completed xenia link (§10) | **Thunderhead.** +1 shiny reroll, as a Lure gives; Electric and Flying types ×2. | **I** Thunderbolt<br>**II** **Acorn of Dodona**: the Shiny Charm<br>**III** the oak-dove of Dodona, whose doves gave Zeus's oracles. The thunder-eagle is now the Archon's ace (STORY §2). |
| **Hecate** | Barley Cake (her crossroads supper) / Honey, sea gifts | **Crossroads.** Torch radius one level larger; at night, Ghost, Dark and Psychic types ×2. | **I** Hex<br>**II** **Three-Flamed Torch**<br>**III** her polecat |
| **Hades** (post-game) | A Bronze Obol / Pomeg Berry (Persephone's fruit) | **Wealth Below.** Dig spots and smashed rocks give two items; coins sell for +50%. | **I** Shadow Ball<br>**II** **Helm of Hades**<br>**III** the black horse |

**Two Favor features use no altar.**
- **Hestia** gains from every offering anywhere.
- **Ares** takes battles, not things.

Both are myth turned into rules.

### Offerings

Six items are new. The rest reuse items the expansion already has.

| Offering | Source | Price |
|---|---|---|
| Olive Oil (new; also used to anoint herms, §4) | Every Agora | 200 |
| Barley Cake (new) | Every Agora | 150 |
| Wine (new) | Emporion, then Thyrsa onward | 300 |
| Frankincense (new) | Emporion, Kythera | 500 |
| Laurel Sprig (new) | Apollo's shrines and Delphoi; also picked free from laurel trees, one per tree per day | 100 |
| Bronze Votive (new) | Emporion and Kaldera smiths | 400 |
| Honey (existing) | The expansion's item; also Melitta's hives | 900 at Gen 8 prices; Ichor sets 300 |
| First Fruits | Any berry | — |
| Feathers | The expansion's 7 wing items, found on routes | — |
| Sea gifts | Pearl, Big Pearl, Shoal Salt, Shoal Shell, Heart Scale | — |

Using berries as first fruits also settles the berry question that INVENTORY §1 left open: **keep the berry system**, restyled as Greek fruit and herbs, because the rites give berries a purpose (decision D6).

### Myth and story

- The gods never appear in person in 1.0. They answer through small signs: a flame leans, an owl calls, a laurel leaf turns.
- **Phaedon.** In Astyra, the healer's Asclepeion has a hearth, and Phaedon never prays at it. If asked, he says "I've stopped asking." It is a one-line seed for the unmasking (LABYRINTH.md).
- **After the climax,** when prophecy ends, the rites go on. The gods were never the Fates.
- Altars give the world a pulse between towns, and give money a long-term use.

### Temples and Hierophants

1. **The temple altar is the god's great altar,** where offerings count double.
2. **The Hierophant teaches their god's rite** on your first visit: one line, plus one free loved offering.
3. **The system's tutorial is in Emporion,** with Kerykos, the Herald of Hermes.
   - Ione told the player he will "talk your ear off" (SCRIPT.md beat 7).
   - He teaches praying at herms and gives 3 Olive Oil.
   - The slice is not changed.
4. **The Hierophant hands over gift I in person:** "Hermes is pleased with you. He asked me to give you this."
5. **The post-game Arena of Champions** (PITCH §6.3) opens each Hierophant's rematch once you are Beloved of their god. It is optional content behind an optional system.

### Engine

**The core.** `src/ichor_rites.c` holds:
- `Ichor_GetFavor` and `Ichor_AddFavor`;
- `Ichor_SetBlessing` and `Ichor_BlessingTick`;
- `Ichor_IsBlessed(enum IchorGod)`, a single inline check every hook calls.

**The step tick.** Call `Ichor_OnStep()` from `TryStartStepCountScript` (`src/field_control_avatar.c`, around line 746). Model it on `UpdateRepelCounter` (`src/wild_encounter.c`, around line 1033), which already packs two meanings into one var with `REPEL_LURE_MASK`.

**The hooks,** each about 5 lines behind `Ichor_IsBlessed`:

| God | Hook |
|---|---|
| Hestia | A Relic Ring entry that calls `HealPlayerParty` |
| Hermes | The price calculation in `src/shop.c`; trainer prize money in the battle money command |
| Demeter | Wild held-item roll (`src/wild_encounter.c`, `src/pokemon.c`); berry yield (`src/berry.c`); the dig roll (`src/ichor_dig.c`) |
| Dionysus | Rolls at the moment the blessing starts |
| Artemis | Slot choice in `ChooseWildMonIndex_Land` when `GetTimeOfDay() == TIME_NIGHT`; a rate change beside `ApplyCleanseTagEncounterRateMod`; the Augur's Eye `SNEAKING_PROXIMITY` (`include/config/dexnav.h`) |
| Hephaestus | Glints: call `ItemfinderCheckForHiddenItems` (`src/item_use.c`) on a timer and spawn sparkles; the Rock Smash item roll |
| Aphrodite | Friendship (`UpdateFriendshipStepCounter`, `src/field_control_avatar.c` around line 833, and the battle friendship gains); gender skew where wild Pokémon are created |
| Apollo | The EXP command in battle |
| Ares | Beside `IsWildLevelAllowedByRepel` (`src/wild_encounter.c`, around line 1070) |
| Poseidon | `CalculateFishingBiteOdds` in `src/fishing.c` returns 100 |
| Athena | The DexNav hidden-Pokémon rate (`HIDDEN_MON_SEARCH_RATE`); flee chance |
| Hera | Egg cycles and egg finding (`src/daycare.c`) |
| Zeus | The shiny-reroll loop (`src/pokemon.c`, around line 886, next to the Lure's reroll) |
| Hecate | `Ichor_GetTorchFlashLevel`; type weights |
| Hades | `src/ichor_dig.c` and the Rock Smash roll |

**The altar script.** One shared Poryscript file, `data/scripts/ichor_rites.pory`, with an entry point per god that sets `VAR_0x8004` to that god.
- The offering picker reuses the bag's choose-an-item mode, the one berry planting uses, filtered by a new `offering` field in the item data. **Low–Medium.**

**The info panel.** One line in the start-menu info window (`src/start_menu.c`). **Low.**

**Risk: low.**
- The hooks touch many files, battle code included, but each is one guarded line.
- A future expansion merge conflicts on single lines, never on logic.

### Cost

| Item | Size |
|---|---|
| 6 offering icons | ~2 KiB |
| About 13 altar styles, 4–6 metatiles each, inside the biome tilesets they belong to | — |
| Text: 15 gods × about 12 lines, plus offering reactions | ~18 KiB |
| 15 sacred-animal encounters | Data only |

### Flags and vars

- `IchorSave.favor[16]` and `IchorSave.blessing`. The blessing is a u16: 4 bits of god, 12 bits of steps.
- 15 daily flags, `FLAG_DAILY_ICHOR_PRAYED_<GOD>` (52 daily flags are unused).
- 45 gift flags, `FLAG_ICHOR_GIFT_<GOD>_I`, `_II` and `_III`.
- About 12 flags `FLAG_ICHOR_ALTAR_CLEANSED_<n>`.

---

## 4. Herm waystones

### Play

Herms do two jobs: **travel** between towns from the very start, and **anointing**, a Favor rite for Hermes on the routes.

**Travel herms** (user, 2026-11-17). Every town, hamlet and major rest stop has a great herm right at its main entrance, a step or two from where you arrive: Hermes's head in a bright winged cap, a laurel garland, a bronze caduceus down the pillar. A small plaque beside it reads:

```text
The herm of Akti.
Touch it to travel between herms.
```

The town's herm becomes a destination the first time you rest at its Asclepeion (or its healer, or the inn where there is no Asclepeion), or touch the herm. The healer says so the first time:

```text
Go in health.

Our town's great herm knows you now.
Touch any herm, and Hermes will bring you back to us.
```

Touch any town's herm and it offers to carry you:

```text
The great herm of Emporion.
Travel to another herm?
```
?? YES/NO, then a list of every town whose herm knows you, in story order, and "Stay here". Pick one and the screen flashes white: you stand beside that town's herm. No Olive Oil and no relic are needed. Daedalus's Wings, at Laurel 6, add flying from anywhere through the Fly map.

**Route herms.** Every route has one great herm too: a garlanded pillar with Hermes's head, darker than the others where hands have touched it. Talk to it while you carry oil:

```text
A great herm, hung with old garlands. Hermes's face, worn smooth.

Anoint it with olive oil? (You have 4.)
```
?? YES/NO
```text
The oil runs down the old stone face.

Somewhere, Hermes makes a note.
```

From Act I you can anoint herms, and Kerykos tells you why: Hermes remembers every traveler who honors his stones. Each anointing is Favor for Hermes. At Laurel 6 you get Daedalus's Wings, and every route herm you anointed appears on the Fly map at once, so you can land in the middle of a route as well as in a town.

### Rules

- **Travel herms.**
  - One per town, hamlet and major rest stop, at the main entrance (MAP_DESIGN §2), with its plaque. 19 in the current build, from Elaia to Olympus's Propylaia.
  - Registered by the town's first heal (Asclepeion, healer, Mom at home, or the inn in Aigina and Styx Falls) or by touching the herm. Registering costs nothing and gives no Favor.
  - Every travel herm offers TRAVEL once another town is registered. The list shows registered towns only, never the one you stand in. Route herms stay with anointing: the Wings fly from them, and from anywhere.
  - You land on the tile beside the town's herm, on the main path.
  - Travel herms are not anointed. Emporion keeps its anointing herm at the crossroads beside its new gate herm.
- **Route herms.** There is one great herm per route map section; about 22 in 1.0.
  - Other herms stay signposts, like the slice's three on Route 1.
  - Route 1's spur-fork herm becomes Kalliste's great herm.
- Anointing costs 1 Olive Oil and gives Hermes +1 Favor, once per herm.
- With the Wings, you land on the tile south of the herm.
- Anointing all of them gives Hermes +10 Favor, and Kerykos adds a herald's-staff stamp to your trainer card (the kylix).
- The Scroll of Deeds counts them: "Herms anointed: 7 of 22."
- **Placement** follows MAP_DESIGN §1 and §7.
  - The great herm stands at the route's main fork or beside its set piece, never in a dead end.
  - It doubles as the fork's sign ("East: Kronion Hill. North: Akti Town.") and as one of the route's "myth in the land" landmarks.
  - Its landing tile must be on the main path, with a clear way on in both directions.

### Myth and story

- Herms were waymarkers and boundary stones of Hermes, god of travelers, and travelers did anoint them with oil.
- The herald god who "remembers you passed" is the god of roads keeping a ledger.

### Where

- Herm travel between towns from Elaia onward: the first trip is possible once a second town is registered (Akti).
- Anointing from Act I (Emporion) onward.
- Flying to anointed route herms, and from anywhere, from Act II's end.

### Engine

- **Travel herms** (built; ENGINE_API §4). The herm and plaque are object events (`OBJ_EVENT_GFX_ICHOR_GREAT_HERM`, `_HERM_PLAQUE`), so they look the same on every tileset and need no new metatiles. `tools/ichor/maps/town_herms.py` places them; `src/data/ichor_town_herms.h` holds each town's landing tile, healer and name; the travel menu is a `dynmultistack` list; the trip is `SetWarpDestination` plus the white-flash warp.
- **Route herms** (built). Fly works per map section. `GetMapsecType` in `src/region_map.c` returns the can-fly type for a route whose herm is anointed, the fly map draws a dot for it, and each route herm has a heal location at its landing tile.

### Cost

- Two field objects (a 16x32 herm, a 16x16 plaque) in the cast palette: under 1 KiB.
- A herm-dot icon on the fly map; one heal location per route herm.
- Text: ~2 KiB.

### Flags and vars

- 32 flags, `FLAG_ICHOR_TOWN_HERM_<TOWN>` (`FLAG_ICHOR_TOWN_HERMS_START` + `TOWN_HERM_*`; 13 spares for new towns).
- 32 flags for route herms, `FLAG_ICHOR_HERMS_START` + `HERM_*`.
- No vars.

---

## 5. Excavation: Alethea's Trowel

### Play

Turned earth with a glint of pottery means a dig spot. Kneel, scrape, and see what Aethos buried. Most finds are small: a coin, a shard, a fossil. Some are pieces of something bigger:

- **Potsherds** reassemble into **12 amphorae**. Each is painted with a myth, and each myth points to a rare Pokémon somewhere in Aethos.
- **Ostraka**, the clay voting shards Athenians used to exile people, are a running joke with a payoff.
- **Prophecy fragments** reveal Iapetos's forgeries before Lakonia does.
- **Daedalus's pages** carry the Labyrinth's secrets (LABYRINTH.md).

### Rules

**The Trowel.** Alethea gives it on arrival at Emporion:
```text
ALETHEA: Here. I brought two trowels. I always bring two.

ALETHEA: Truthfully, I bring three.
```

**Spots.**
- There are about 45 **daily spots**. Each can be dug once a day and looks flattened until the next day.
- About 25 **fixed finds**, plus 7 pages and 8 prophecy fragments, can each be dug once.
- **Placement** follows MAP_DESIGN §1, "every dead end pays".
  - Dig spots go where curiosity takes people: the end of a side path, the tip of a peninsula, behind a statue, inside optional grass, beside a ruin.
  - **Never on the main path.** A dig spot is a reason to leave the road.
  - Daily spots favor dead ends that otherwise hold a one-time item, so those dead ends keep paying after the first visit.

**Digging.** Press A. The field-move pose plays, with a dust puff, for one second, then the item.

**The loot tables** are percentages. A spot uses the table for its act.

| Find | Act I | Act II | Act III and post-game |
|---|---|---|---|
| Potsherd | 22 | 20 | 16 |
| Bronze Obol (Relic Copper) | 18 | 12 | — |
| Silver Owl (Relic Silver) | — | 8 | 10 |
| Gold Stater (Relic Gold) | — | — | 4 |
| Ostrakon | 10 | 10 | 8 |
| Evolution shard (red, blue, yellow or green) | 10 | 8 | 10 |
| Stardust or Star Piece | 12 | 6 | 8 |
| Hard Stone | 10 | 6 | — |
| Heart Scale | 8 | 8 | 6 |
| Fossil | 6 | 8 | 10 |
| Pearl | 4 | — | — |
| Evolution stone | — | 8 | 10 |
| Rare Bone | — | 6 | 6 |
| PP Up | — | — | 6 |
| Comet Shard | — | — | 3 |
| Bottle Cap (the "Pythian Laurel", §11) | — | — | 2 |
| Ichor Stone | — | — | 1 |

- If you have every sherd from a region, or every ostrakon, a roll for those rerolls.
- Demeter's blessing rolls twice and keeps the rarer result. Hades's gives two items.
- Rolls are seeded by the daily seed and the spot, so reloading a save gives the same result. There is no save-scumming.

**The coins** are renamed and get a new description. "A copper coin used by a civilization 3,000 years ago" makes no sense in an age where it is pocket change.
- Relic Copper becomes the **Bronze Obol**.
- Relic Silver becomes the **Silver Owl**, after Athens's owl coin.
- Relic Gold becomes the **Gold Stater**.
- They are sell-only treasure. The slice's hidden Relic Copper in Elaia's well, "a coin someone wished on", is an obol. **Charon accepts it** in the post-game (PITCH §6.2, "pay Charon an obol").

**Fossils.** Daphne revives them at the Akademia. The species wait for the dex.

### The 12 amphorae

Each amphora has 4 sherds, all from one region; that region's dig spots are the only source.
- A completed amphora goes on Daphne's shelf at the Akademia.
- Reading it shows the black-figure painting, at 64×64 in a pottery frame, with three or four boxes of Daphne's notes.
- It also adds a **lead** to the Scroll of Deeds.

| # | Myth | Sherds from | The painting | The lead |
|---|---|---|---|---|
| 1 | Kronos swallows the stone | Kalliste | Rhea hands Kronos a swaddled stone | At night the broken altar on Kronion Hill hums: a rare Rock-type. It also seeds the Omphalos, the swallowed stone at Delphoi. |
| 2 | Persephone's six seeds | Eleusa | A girl with a pomegranate, half in shadow | Eleusa's fields at dusk: a rare Grass/Ghost type |
| 3 | Arachne at the loom | Emporion | A weaver and a spider, both at work | The web cave on the Eleusa road: a web-spinner with its hidden ability |
| 4 | Hermes steals the cattle | Emporion's coast | A baby leading cattle backward | Backward hoofprints on a beach lead to a hidden grotto |
| 5 | The return of Hephaestus | Kaldera | A god on a donkey, led home drunk | Hephaestus Favor +5; a forge-side rare |
| 6 | Icarus | The Ikarian coasts | A boy falling, feathers loose | A sea-bird's dawn roost, and a seed for Daedalus |
| 7 | Pandora's jar | Astyra | A lid lifted; one small thing left inside | Elpis (*Hope*). Post-game: the Treasures of Ruin, the jar's evils (PITCH §4) |
| 8 | Orpheus sings | Arkadia | A singer, animals listening | Arkadia's grove at night: the Meloetta lead (PITCH §4) |
| 9 | Atalanta's race | Arkadia | A runner stooping for a golden apple | A fast Pokémon's hidden path; seeds the Olympiad's Atalanta |
| 10 | Phaethon's chariot | Kaldera | A boy, a chariot of fire, a fall | The caldera rim: a rare Fire-type. A hubris echo. |
| 11 | The judgement of Paris | Kythera | Three goddesses and one apple | Aphrodite Favor +5; a golden-apple tree (seeds Ladon, the eleventh Labor) |
| 12 | Theseus and the Minotaur | Knossa | A youth, a bull-headed man, a thread | Ariadne reads it: "That's not how it went." Seeds the Endless Labyrinth. |

**All 12** give Daphne's last lecture ("every myth is a memory of a Pokémon, and now you've seen twelve") and an Ability Patch.

### Ostraka

There are 30, each a scratched name and a grudge. An old voter in Astyra's Agora collects them: **Lysimachos**, which was the real name of Aristeides the Just's father. So the Archon's old dad collects the votes to exile his son.

```text
LYSIMACHOS: Nine of these have my boy's name on them.

LYSIMACHOS: I keep those on top.
```

**Rewards:** 10 ostraka, a TM; 20, an Ability Capsule; 30, three Pythian Laurels and the last ostrakon.

**Sample ostraka:**
- "ARISTEIDES. Sick of hearing him called the Just." This is the farmer's vote in Plutarch.
- "THEMISTOKLES. Talks about boats at dinner." He is the Pantheon's Poseidon seat.
- "HYPERION. Burned my fence."
- "THE GOAT. You know which goat."
- **The 30th:** "{PLAYER}. Never met them. Just a feeling." The handwriting looks a lot like Kleon's.

### Prophecy fragments

There are 8 lead tablets, the kind pilgrims scratched questions on at Dodona. They are fixed finds in Acts II–III.

- Alethea "reads" each one. Under the visible prophecy lies an older one, scraped away and written over in a neat hand with a little hook on every sign-off. That is Iapetos.
- Each tablet is a small story of one person Iapetos used.
- **They are optional.** The main-path proof is the Knossa archive: Kleon's draft and Elpis's sealed tablet (LABYRINTH.md scene H).

The eight are STORY §4's table:

| # | Whose | The forgery | The original, as Alethea reads it | Where it lands |
|---|---|---|---|---|
| 1 | A quarryman of Emporion | "The quarry closes. You'll starve." | "The quarry closes. You'll find other work." | Petros's father. The first grunts were hired off this lie. |
| 2 | The harbor-master of Emporion | "Close the port to the Archon's ships." | "Keep the port open." | The archive's "Revised." line (LABYRINTH scene H) |
| 3 | A soldier of Thyrsa | "You'll die in the next war." | "You'll come home from the next war." | A Titanborn grunt type (STORY §5) |
| 4 | A bride of Eleusa | "Your husband will leave you." | "Your husband will be late." | A comic one |
| 5 | Kallisto of Arkadia | "Show no mercy at the new moon." | "Show mercy at the new moon." | Kleon's loss |
| 6 | A farmer of Kalliste | "Your olives will fail." | "Your olives will come in silver." | The slice's silver olives |
| 7 | **Hyperion** | "You'll end your days in the dark." | "You'll end your days in the dark, and be glad of it." | His epilogue. With this one found, Alethea reads it to him at Talos's forge. |
| 8 | **A widow of Lakonia** | "Your last child will die young." | "Your last child will be glorious young." | Rhea's. **Not a forgery** but her own misreading: the lead is unchanged, and only her fear changed the words. Alethea: "Nobody scraped this one. She just read it wrong." |

- **With all 8,** Alethea gets an extra line at Lakonia and reads the full pattern at the trial (STORY L-2), and the vote becomes unanimous.
- **Placement** follows the dig-spot rules above. Each tablet lies near the person it concerns: tablet 6 on Kalliste, tablet 8 in Lakonia, and so on.

### Engine

- **Dig spots** are bg events with a script `Ichor_Dig` and a spot id. Daily state is 64 bits in `IchorSave.digDaily`, cleared in `DoDailyEvents` (`src/clock.c`).
- **Rolls** use a local random seeded with `gSaveBlock1Ptr->dailySeed ^ spotId`. The pattern already exists: `src/lottery_corner.c` uses `LocalRandomSeed(dailySeed ^ salt)`. **Low.**
- **The amphora shelf** is objects with flags. The painting is a small picture window, the same way the expansion shows a Pokémon picture in a box. **Low–Medium.**

### Cost

| Item | Size |
|---|---|
| 12 paintings, 64×64 at 4bpp | 24 KiB (stretch; text-only first) |
| Item icons: Trowel, Potsherd, Ostrakon, lead tablet, page | ~2 KiB |
| Dig-spot object | 0.25 KiB |
| Text | ~10 KiB |

### Flags and vars

- About 40 fixed-find flags.
- `IchorSave.sherds` (48 bits), `.ostraka` (32 bits) and `.digDaily` (64 bits).

---

## 6. Omens and augury

### Play

Each town has an augur on the wall, watching birds. Ask, and you get the day's omen for all of Aethos. Townsfolk repeat it ("They say the birds went left over Route 4"), so the world feels like it read the same sky.

### Rules

There is one omen per day, drawn from five kinds:

| Kind | Weight | What happens today |
|---|---|---|
| Swarm | 35% (45% before the Stranger kind opens) | One route's swarm species makes up half its encounters |
| Rare visitor | 25% | A rare Pokémon waits at a fixed spot on one map. Catch or defeat it and it's gone until another omen sends one. |
| Weather | 20% | One map's weather is set, and the augur says what likes it |
| Good sign | 10% | A free minor blessing from the augur, or a lucky number: "Today, threes are lucky." In knucklebones, the 3-face counts as a 4 today. |
| Stranger | 10%, only after the core theoxenia (§10) | A disguised god walks somewhere today: "An eagle sat on a beggar's shoulder in Astyra and didn't fly off." |

- **Entries are filtered by story progress,** so only places you can reach are named.
- **Entries from the dex team's late-area habitats** (2026-11-14, `design/dex/DECISIONS.md`):
  - **Swarm:** Sporadon. "A crop springs up overnight." Level 38.
  - **Rare visitor:** Hymnet. One cygnet waits at the Kastalian spring at dawn. Level 33.
  - **Weather:** Kryopuff. Snow falls on the lowest slopes of the Ascent. Level 38.
- **There are about 30 entries in 1.0:** 12 swarms, 12 visitors and 6 weather spots.
- **After the climax,** when prophecy has ended, the augurs keep working:
  ```text
  AUGUR: Birds don't read threads. They read weather.
  ```

### Myth and story

- Augury, reading the flight of birds, sat alongside oracles in Greek divination. The slice already has an Augur trainer (Polyeidos) and the Augur's Eye.
- An augur who reads nature rather than fate survives the end of prophecy, and that is the point.

### Where

From Emporion onward. The first augur sits on Emporion's harbor wall.

### Engine

- `src/ichor_omen.c` picks the day's omen in `DoDailyEvents` (`src/clock.c`), from `dailySeed ^ ICHOR_OMEN_SALT`.
- **Swarms** call `StartMassOutbreak` (`src/mass_outbreak.c`), whose struct holds a species, moves, level, probability, duration and location.
  - INVENTORY §10 proposes cutting mass outbreaks along with the TV. **Keep `mass_outbreak.c`**; it is small. The TV can go (decision D7).
- **Visitors** use one hide flag per entry, set or cleared daily.
- **Weather** comes from the affected map's `ON_TRANSITION`, which calls `setweather` from the omen.
- **Low.**

### Cost

About 4 KiB of text and 1 KiB of data.

### Flags and vars

- `IchorSave.omen` (u16).
- 12 visitor hide flags.

---

## 7. The festival calendar

### Play

Aethos keeps the old Attic year. On a festival day the town is hung with garlands, the Agora stocks festival goods, special Pokémon appear, and there is something to do: a torch race, a play, a night when the dead walk. The Scroll of Deeds has a calendar page: "Hekatombaion. The Panathenaia is in 4 days."

### Rules

**An Aethos year is 36 real days:** 12 months of 3 days each, counted on the RTC day counter (`gLocalTime.days`, which `VAR_DAYS` tracks).
- The month is (days ÷ 3) mod 12, and the festival falls on each month's middle day.
- So a festival comes every 3–4 days. A player sees most of them in a normal playthrough.

**Why not real dates.**
- A 30-hour story played over a few weeks would meet a real-date festival once or never.
- Emulator clocks are unreliable.
- A real calendar would lock content to seasons.
- The expansion does convert to real dates (`ConvertTimeToDateTime` in `src/datetime.c`), but the 36-day year is the better design (decision D4).

| Month | Festival | God | Where | The day's event | Agora stock | Encounters |
|---|---|---|---|---|---|---|
| Hekatombaion | **Panathenaia** | Athena | Astyra | A **torch relay race**: carry a flame from the Akademia altar to the Akropolis altar inside the step limit (§2 verbs 2 and 4). Winners get oil-amphorae (Olive Oil ×10). | Olive Oil at half price | Owl-types at night |
| Metageitnion | Karneia | Apollo | Lakonia | Chase the garland-runner through the streets | Laurel Sprig | — |
| Boedromion | The Mysteries | Demeter | Eleusa | The procession; the sanctum's lower hall opens to initiates | Barley Cake | Grass and Ghost types at the sanctum |
| Pyanepsion | Pyanopsia | Apollo | Every port | Bean soup, and sailors' tales of Knossa (a Labyrinth seed). The *eiresione* branch is an offering every god likes. | Eiresione | — |
| Maimakterion | — (the month of storms) | — | — | Weather omens twice as likely | — | — |
| Poseideon | Poseidea | Poseidon | Every harbor | Fishing contest: three different species in 50 steps | Sea gifts | Water swarm |
| Gamelion | Theogamia | Hera and Zeus | Astyra | Wedding feast: eggs found twice as fast today | Pomeg Berry | — |
| Anthesterion | **Anthesteria** | Dionysus | Everywhere | The jars are opened and the dead walk. Doors are smeared with pitch. | Wine | Ghost-types ×3 on every route at night |
| Elaphebolion | **City Dionysia** | Dionysus | Thyrsa | The story event in Act II. Afterwards, the yearly theater tournament. | Masks (cosmetic) | — |
| Mounichion | Mounichia | Artemis | Arkadia | Moon-cakes with candles on the altar | Barley Cake | Full-moon encounters |
| Thargelion | Thargelia | Apollo and Artemis | Delphoi, Arkadia | The twins' birthday: first fruits | Laurel, berries | — |
| Skirophorion | **Kronia** | Kronos | Kronion Hill and Titan sites | Before the climax, the Titanborn's golden-age feasts: grunt battles and speeches. After it, Time Fractures are twice as common (PITCH Act III). | — | Paradox Pokémon at fractures |

- **The main path never needs a festival.** The Act II Dionysia is scripted on story time, whatever the calendar says.
- **Joining a festival** gives that god +5 Favor, once per festival day.

**1.0 set:** the Panathenaia (it reuses carried flames), the Anthesteria (only an encounter change), the Kronia (story flavor, then fractures) and the story Dionysia. The rest are stretch or post-1.0.

### Myth and story

- These are real Attic festivals. The Kronia was a real festival of Kronos at which masters served their slaves, and Team Titan keeps it.
- The Pyanopsia remembered Theseus's crew coming home from Crete with only beans left.

### Engine

- `src/ichor_calendar.c` provides `Ichor_GetMonth`, `Ichor_GetFestival` and `Ichor_DaysToFestival`.
- Town `ON_TRANSITION` scripts set decoration hide flags, switch the music to a festival variant, and pick an alternate Agora list.
- Encounter changes hook `src/wild_encounter.c`.
- **Low–Medium,** and heavy on text.

### Cost

- Garland and banner objects: ~1 KiB.
- One festival music variant: ~4 KiB.
- Text: ~10 KiB for the 1.0 set.

### Flags and vars

- One decoration hide flag per town.
- A daily flag "joined the festival".
- `IchorSave.festivalsSeen` (16 bits).

---

## 8. Katasterismoi: the star chart

### Play

Daphne gives you the **Star Chart** at the end of Act I, after she tells you what you are:

```text
DAPHNE: When people were sure of a story, they put it in the sky.

DAPHNE: You're not in the sky yet. Neither am I.
```

- **From the bag,** the chart shows a parchment sky with the constellations you have placed.
- **At night outdoors,** at a stargazing seat on a hilltop, at Delphoi or on the Akademia roof, you see the live sky. The constellations you placed twinkle into place.
- Each one goes up when you finish its myth. The last patch of sky stays empty until the very end.

### Rules: the 24 constellations

| # | Constellation | Myth | Placed when |
|---|---|---|---|
| 1 | Delphinus | Poseidon's dolphin | You get Poseidon's Conch |
| 2 | Crater | Dionysus's cup | Laurel 4 |
| 3 | Ursa Major | Kallisto | Laurel 5 |
| 4 | Orion | Artemis's hunter | Artemis Favor 30 |
| 5 | Sagitta | The arrow | The Artemis trial |
| 6 | Cygnus | Aphrodite's swan | Laurel 7 |
| 7 | Taurus | Asterion | You free Asterion (LABYRINTH.md) |
| 8 | Corona Borealis | Ariadne's crown | The crane dance (LABYRINTH.md) |
| 9 | Pleiades | The seven sisters | All 7 of Daedalus's pages |
| 10 | Corvus | Apollo's raven | Laurel 8 |
| 11 | Lyra | Orpheus's lyre | The Orpheus amphora's lead |
| 12 | Capricornus | Amalthea, Zeus's nurse-goat on Crete | Knossa's Idaean cave (optional) |
| 13 | Cancer | Hera's crab | Hera Favor 30 |
| 14 | Aries | The Golden Fleece | The Mega Ampharos quest (PITCH §4) |
| 15 | Gemini | The Dioskouroi | The Latias and Latios quest (PITCH §4) |
| 16 | Aquila | Zeus's eagle | You beat the Archon, whose ace is the thunder-eagle (STORY §2) |
| 17 | Ophiuchus | Asclepius, the healer Zeus struck down for cheating death | The climax's resolution (Phaedon and Elpis) |
| 18 | Leo | The Nemean Lion | Labor 1 |
| 19 | Hydra | The Hydra | Labor 2 |
| 20 | Draco | Ladon | Labor 11 |
| 21 | Hercules | Herakles | All 12 Labors |
| 22 | Centaurus | Chiron, teacher of heroes | The Olympiad's Achilles, gold |
| 23 | Cetus | The sea-monster | The Atlantis arc |
| 24 | **The Unwoven** | Your own | The credits. The empty patch fills with your shape. |

**Rewards:**
- **6 placed:** on clear nights, a moon-dance of small star Pokémon on Kronion Hill.
- **12:** TM Cosmic Power.
- **18:** 3 Star Pieces.
- **All 24:** a special encounter, a star-born mythical whose species comes with the dex.

### Myth and story

- *Katasterismoi*, "placings among the stars", is the name of the ancient book of constellation myths.
- The Unwoven's empty patch of sky is the theme made visible. Everyone else's story is already up there.

### Engine

- The Bag screen is built in `src/ichor_star_chart.c`:
  - BG2 is the sky;
  - BG1 holds the constellation line tilemaps, copied in when a constellation's bit is set;
  - BG0 is text;
  - the twinkle is a palette cycle, like the title screen's.
- The portable parchment view uses 24 distinct original line patterns.
  Kronion Hill's eastern shrine steps are the first outdoor seat: the real
  Chart and night are required, and the same placed patterns twinkle against
  a midnight-blue sky. B returns to the steps, not the Bag. The view preserves
  map music and saved placements. Other seats and milestone-reward world
  callers remain to integrate.
- Its setup follows the small-screen lifecycle of `src/diploma.c`, with
  explicit resource cleanup and return to the Bag or the seat's waiting script.

### Cost

- Sky background: ~5 KiB compressed.
- Line tiles: ~4 KiB.
- Text: ~2 KiB.

### Flags and vars

Production uses the existing 32-bit allocation at
`FLAG_ICHOR_CONSTELLATIONS_START`: 24 saved flags in table order, with eight
spare bits. It has the same persistent placement semantics without changing
the current save layout. See ENGINE_API §10.

---

## 9. Knucklebones (astragaloi)

### Play

The player's room has a knucklebones set: "Record against Mom: 0 wins, 212 losses" (SCRIPT.md, the 2F roster). Now you can actually play. Taverns across Aethos have regulars and a champion, and the game has a real choice in it.

### Rules

**The bones.** Four knucklebones, each landing on one of four sides worth 1, 3, 4 or 6, as real astragali do.
- The broad sides are likelier: 3 and 4 come up 40% each, 1 and 6 just 10%.

**A throw.**
1. Throw all four.
2. You may rethrow any of them **once**, choosing which to keep.
3. Score the sum, from 4 to 24.

**Named throws:**
- **Aphrodite** is all four sides different (1, 3, 4, 6). It beats everything, and comes up about 3.8% of the time.
- **The Dog** is four 1s. It loses to everything, and comes up 0.01% of the time.
- Otherwise the higher sum wins, and a tie is rethrown.

**The choice.** Keep your 6s and rethrow the 1s, or chase Aphrodite when you already hold three different sides.

**A match** is best of 5 throws.

**Opponents:**

| Personality | Plays like |
|---|---|
| Cautious | Rethrows only 1s |
| Bold | Chases Aphrodite whenever it holds three different sides |
| Silenos | His bones are loaded (6 comes up 30% of the time). Call "Loaded!" after two straight throws with two 6s each, and you win the match. |
| **Mom, until Delphoi** | House rules: she gets **two** rethrows. And her throws lean lucky, because her bee, Melisseer, hums the throws before they land (STORY §2). Her faces come up 5/30/30/35 instead of 10/40/40/10. In a simulation of 40,000 best-of-5 matches with sensible play on both sides, you win about **5.5%** of matches. That is why she is 212–0. |
| **Mom, after Delphoi** | Fair bones and one rethrow, like anyone, so about **50%**. At her first game after Delphoi: "I gave the bee the day off." |

**Taverns and prizes.**
- There are 6 taverns: Emporion, Thyrsa, Astyra, Kaldera, Amnisos and Lakonia. Each has two regulars and a champion.
- A champion's first loss gives a TM and a line for your trainer card. Regulars give Olive Oil and Wine.
- **No money wagers.** It stays a friendly game.

**Mom.**
- She plays at home after the slice, except while she is gone. She leaves the night before the helmets come, at Act II's low point in Kaldera (STORY II-14), and doesn't come back until Delphoi (STORY III-7).
- The 2F text shows the live record: "Record against Mom: {wins} wins, {losses} losses."
- **The confession.** At the Kastalian spring she admits it: "The knucklebones. I cheated. The bee hums the throws. All two hundred and twelve." (STORY §7.5). From then on she plays fair.
- **Your first win,** whenever it comes:
  ```text
  MOM: …Well.

  MOM: Two hundred and twelve, and then one.

  MOM: Here. My lucky bone. Your grandmother threw Aphrodite with it twice in one night.

  MOM: She never told me how. I suspect cheating.
  ```
- She gives the **Aphrodite Bone**, a key item that grants one extra rethrow per match.
- A win before Delphoi is rare but possible: a 1-in-18 match against a bee. It plays the same lines. The bee sulks.

### Engine

- **1.0 is a script version.**
  - `random` weighted 10/40/40/10, or 5/30/30/35 for Mom before `FLAG_ICHOR_MOM_CONFESSED`.
  - A `dynmultichoice` with four bone toggles plus THROW.
  - A small text window that draws the faces.
  - **Low.**
- **Stretch:** a little C screen with four bone sprites that tumble. **Medium.**

### Cost

- Text: ~3 KiB.
- Stretch screen: ~2 KiB of sprites.

### Flags and vars

- `IchorSave.momWins` and `.momLosses`. `momLosses` starts at **212** in a new game.
- 6 champion flags.
- `FLAG_ICHOR_MOM_CONFESSED`, set at the Kastalian spring (STORY III-7). It ends the bee's help.

---

## 10. Xenia and theoxenia: guest-friendship, and gods at the door

### Play

In every town, one household keeps the old law of hospitality. Knock, and you're fed before anyone asks your name, as Homer's hosts do:

```text
HOST: Sit. Eat first.

HOST: Then tell me who you are. Not before.
```

- **A host's table heals your party.**
- **A host offers a bed until a time you choose:** dawn, noon, dusk or night.
- **A host may hand you half of a broken token** (a *symbolon*) to carry to their guest-friend in another town. That friend matches the halves, gives a gift, and maybe hands you the next half.

### Rules

**Resting** moves the clock **forward only, and never past midnight.** Each option appears only if that time is still ahead today.
- Dawn is 06:00, noon is 12:00, dusk is 19:00 and night is 20:30. These follow the expansion's Gen 8+ hours in `include/constants/rtc.h`: morning 6–10, day 10–19, evening 19–20, night 20–6.
- So players who only play in daytime can still see the night, and nobody can farm daily resets.

**Token chains.** Three in the stretch set, four links each:

| Chain | Path | Final gift |
|---|---|---|
| **The Potter's Knucklebone** | Diktys (Akti) → a potter (Emporion) → an actor (Thyrsa) → a scribe (Astyra) | A traded Pokémon with its hidden ability and a rare held item |
| **The Split Coin** | Emporion → Eleusa → Arkadia → Kaldera | 2 Pythian Laurels |
| **The Broken Ring** | Kythera → Amnisos → Lakonia → Delphoi | An Ichor Stone |

Each link gives Zeus Xenios +3 Favor.

**Bad guests.** In Kythera, Titanborn abuse a host's table. Drive them off for Zeus +5. The Odyssey's suitors (post-game) are the ultimate bad guests.

### Engine

- Scripts and flags.
- Resting changes `localTimeOffset` (`src/rtc.c`, around line 320), with a same-day check.
- **Medium–Low.** Risk: the day/night tint and berry timers jump forward, which is acceptable.

### Cost

About 6 KiB of text. Hosts reuse the townsfolk walkers.

### Flags and vars

About 12 chain flags. Resting stores nothing.

### Theoxenia: gods in disguise, and the old starters

> **User direction (2026-11-14):** "we need to make it later game to be able to receive the old starters as blessings from gods in disguise." The slice's starters (Snivy, Cyndaquil and Piplup) give way to the Aethos dex's own starters, decision D1 in `design/dex/DECISIONS.md`. The old three come back here.

**Play.**
- Sometimes a stranger in Aethos is a god, testing whether the old law of hospitality still holds. This is *theoxenia*, the myth behind xenia. Zeus and Hermes once walked Phrygia as beggars. Only old Baucis and Philemon let them in, and their wine jug never emptied.
- You meet:
  - an old woman grieving by a well;
  - a lame tinker on a mountain road;
  - an old fisherman who fishes up three rods.
- You aren't told who they are. You're asked for something small, a little kindness or the truth.
- Pass, and the stranger stands up taller than they were. You get a blessing you can hold: a starter Pokémon, chosen by the god for their domain.

**Two tiers,** so the user can choose (decision D8):

| Tier | What it covers | Gifts | Where |
|---|---|---|---|
| **Core** | The three old slice starters, from three gods | 3 | Mid to late game: after Laurels 5, 6 and 7 |
| **Extended** | The core, then a recurring chain of 13 more visits and a finale at your own home | 3 + 15 | From Act III's end through the post-game |

#### Rules shared by both tiers

**One god, one gift.** Each god gives one fixed species, picked for the god's domain; the myth-fit is the point, and a choice would blur it. The one exception is the finale, where two gods give one each.

**Every gift** is the base form, the iconic starter, with these touches:

| Touch | Detail |
|---|---|
| Level | Past both evolution levels, so the next two level-ups bring the final form: the blessing unfolds. A player who wants the little one can give it an Everstone. |
| Ball | A Cherish Ball, the gift ball, already in the expansion |
| Nature | Chosen by the god |
| Ability | Its hidden ability, where that suits the god |
| IVs | 3 perfect IVs, in the stats the god favors |
| Move | One "god-taught" move it couldn't otherwise know yet |
| Fateful encounter | The flag is set (`MON_DATA_MODERN_FATEFUL_ENCOUNTER`) |
| Met location | "a guest-gift of Demeter", and so on |
| The **Xenia Ribbon** | One of the Gen 3 event ribbons (`MON_DATA_WORLD_RIBBON`) renamed, with the text "A guest-gift from a god. Hospitality, returned." This depends on INVENTORY §11's ribbon re-theme. |
| Favor | The god's Favor +15 (§3) |

**No permanent failure.** A failed test ends the visit kindly ("Never mind, child") and the stranger comes back another day with the same test. Nothing is lost except your Old Rod for a moment (Poseidon) and your sandals for a walk (Hermes), and both come back.

**The tells.** Players learn to recognize a god:
1. **No shadow.** Ichor gives every object a shadow (`OW_OBJECT_VANILLA_SHADOWS` is FALSE), so the one figure without one stands out. Hermes points this out at his reveal.
2. **Your follower bows** when within 3 tiles of a disguised god.
3. **A detail that doesn't fit:** an ear of grain in a beggar's shawl, gold under a tinker's soot, a fisherman who stays dry in the rain.
4. **The Augur's Eye.** On a map with a disguised god, its screen adds: "Something here is watching you."
5. **Omens** (§6). After the core three, a fifth omen kind, **Stranger**, names a place: "An eagle sat on a beggar's shoulder in Astyra and didn't fly off."

**Decoys.** About 10 ordinary strangers make the same kinds of request: water, directions, a coin.
- They have shadows, and your follower ignores them.
- Kindness to them earns Zeus Xenios +1 Favor and a small item.
- So the tells tell you **who** the gods are, but kindness is always the right answer. That is the moral of the myth, played rather than preached: treat every stranger as if they might be a god.

#### The core tier: the old three

| God | Disguise | The test | When and where | Gift |
|---|---|---|---|---|
| **Demeter** | **Cami, a young woman by the Maiden's Well** (named and drawn by the user's request, from a photo they gave; 2026-11-14). In the Homeric *Hymn to Demeter*, the grieving goddess sat by the Maiden's Well at Eleusis as an old woman, until the king's daughters took her in. The song remembered her wrong, and her reveal says so. | **Share food and comfort her.** Offer her a drink from the bag. She refuses Wine (she did in the *Hymn*). Water is accepted. Water plus a Barley Cake is her *kykeon*, barley water with mint, and is loved. Then she asks for a joke: three choices, two that land. Old Iambe made the goddess laugh with a crude joke, the first laugh of her grief. | **After Laurel 5.** Eleusa's well, on any return visit. An omen points there. | **Snivy** (Grass), whose line ends in Serperior. Demeter's chariot was drawn by serpents. |
| **Hephaestus** | **A lame tinker,** his cart broken on the caldera switchbacks, with a toolbag too heavy for him. | **Walk at his pace.** You carry the bag, and can't run while you do. Halfway up, a goat-path scramble cuts the corner, and he can't take it with his leg. Take it and you arrive alone; he sits down: "Go on. Everyone does." Climb back down to him and walk the long way together. The scramble is two-way, so no ledge strands anyone (MAP_DESIGN §1). Reach the rim forge together. | **After Laurel 6.** Kaldera's caldera road. | **Cyndaquil** (Fire), evolving to **Hisuian Typhlosion** (Fire/Ghost). In myth Typhon is buried under the volcano, his breath feeding Hephaestus's forge. PITCH §4 ties Typhlosion to Typhon and puts Hisuian forms in Aethos. |
| **Poseidon** | **An old fisherman** on a sea-rock below a cape shrine, dry in the spray. | **Answer truthfully,** after Aesop's honest woodcutter. Your Old Rod slips into the sea. The old man dives, then holds up a gold rod, a silver rod, and your salt-cracked one: "This one yours?" Choose your own. Claiming gold or silver gets your old rod back with a sigh: "Come back when the tide's honest." | **After Laurel 7,** before Knossa. A cape near Astyra, reached with the Conch. | **Piplup** (Water), whose line ends in Empoleon with its trident crest |

| Gift | Lv | Held | Nature | Ability | God-taught move | Perfect IVs |
|---|---|---|---|---|---|---|
| Snivy | 35 | Miracle Seed | Timid | Contrary (hidden). Demeter turned the world to winter when crossed. | Leaf Storm | HP, Sp. Atk, Speed |
| Cyndaquil | 40 | Spell Tag ("soot from the forge's oldest wall") | Modest | Blaze | Eruption ("the mountain's breath") | HP, Sp. Atk, Speed |
| Piplup | 45 | Shell Bell | Modest | Competitive (hidden). Poseidon never got over losing Astyra to Athena. | Hydro Pump | HP, Sp. Atk, Sp. Def |

Winning the Poseidon test also gives the **Good Rod**, the "silver" one, if you don't have it.

**The reveals.** These are drafts in the CLAUDE.md voice; each line is one box.

**Demeter, at the Maiden's Well.**

[Cami laughs, a cracked sound, then a real one.]
```text
CAMI: Ha. Oh, that's terrible. Tell it again.

CAMI: I haven't laughed since my daughter went away.
```
[She stands, and she is taller than she was. Gold light fills the well-yard. The dry stalks around the well turn green and heavy.]
```text
DEMETER: I sat at this well once before. The song says I was an old woman.

DEMETER: People remember what they expect. Nobody expects a god.

DEMETER: A girl brought me water. Another made me laugh. I never forgot them.

DEMETER: You did both. Hold out your hands.

{PLAYER} received a Snivy from Demeter!

DEMETER: It grows where it's tended. So do you.

DEMETER: Don't tell anyone Cami was me. They'll feed every stranger in Eleusa.

DEMETER: …Actually. Tell everyone.
```

**Hephaestus, at the rim forge.**

[The tinker sets down the bag and wipes his face. The soot comes away, and under it his skin shines like bronze in a fire.]
```text
TINKER: Everyone takes the goat path. Every single one.

TINKER: My mother threw me off a mountain for limping. Did you know?

TINKER: I fell a whole day. Two sea-nymphs caught me. Nobody else came down.

HEPHAESTUS: You came back down.

HEPHAESTUS: I keep the hot ones under the mountain. This one's small yet.

{PLAYER} received a Cyndaquil from Hephaestus!

HEPHAESTUS: Something huge sleeps under every volcano. This one'll wake slow.

HEPHAESTUS: Feed it coal. Not your fingers.
```

**Poseidon, on the sea-rock.**
```text
OLD MAN: This one yours? The gold? …The silver? …This old thing?
```
[The player chooses the Old Rod.]
```text
OLD MAN: Glaukos's old rod. He fished too, before the sea kept him.
```
[He laughs. Behind him the sea stands up in a wall, and holds still.]
```text
POSEIDON: Everyone picks the gold. Then I keep all three. That's the joke.

POSEIDON: You'd make a bad merchant and a good sailor.

POSEIDON: Take the silver too. And this one. He's got my crest coming in.

{PLAYER} received a Piplup from Poseidon!

POSEIDON: If my niece asks, the salt spring was better than her olive tree.
```

Glaukos, the slice's old fisher who gave you the Old Rod, is named for the fisherman who became a sea-god. Poseidon's "niece" is Athena.

#### The extended tier: the strangers' chain

**The chain.**
- It opens after the core three, so the player already knows what a god in disguise looks like.
- Hermes's visit always comes first, because he teaches the tells.
- After that, visits come in any order as their conditions are met. A Stranger omen names the next one. If no Stranger omen falls for 5 days, one is forced.

**The 15 lines** are every other starter line **except Lazarus's nine.** Lazarus unlocks Rowlet, Litten, Popplio, Chespin, Fennekin, Froakie, Sprigatito, Fuecoco and Quaxly in tiers, and LAZARUS.md tells us to avoid its nine starters. So this chain never offers them, and its gifts come from gods' tests, not a tier menu.

| # | God | Disguise | The test | When and where | Gift |
|---|---|---|---|---|---|
| E1 | **Hermes** | A barefoot messenger with bleeding feet, at a great herm | **Lend him your Talaria.** No running until the next town's great herm, where he waits, wearing them. Then the reveal, and the tells lesson. | End of Act III, the Kythera road | **Squirtle.** Hermes made the first lyre from a tortoise shell. |
| E2 | **Hestia** | A woman shivering at a cold hearth in a roofless farmhouse, in the rain | **Rekindle her hearth.** Carry fire from the nearest altar, 40 tiles off. Rain shortens a carried flame to 20 steps; roadside shrines relight it (§2, relay and water). | End of Act III, the Lakonia road | **Charmander.** Its tail flame must never go out, like Hestia's hearth. |
| E3 | **Athena** | An old weaver at a loom below the Akropolis. As an old woman, Athena warned Arachne. | **Humility.** "Are you the greatest trainer in Aethos?" "Not yet" and "I don't know" pass. "Yes" fails: "A girl here said that about weaving once." This is the game's hubris theme in one question. | Act III, Astyra | **Turtwig.** Torterra carries a tree on its back, as Athena's olive grows on the Akropolis. |
| E4 | **Ares** | A grizzled veteran with a cockerel on his shoulder, ambushed by Titanborn | **Stand beside him.** A double battle with him as your partner. | Act III, Lakonia (Sparta worshipped Ares) | **Torchic.** Ares turned his sleepy sentry Alektryon into a rooster to wake the sun. |
| E5 | **Dionysus** | A drowsy youth with ivy in his hair, tied to a trireme's mast by sailors (the Homeric *Hymn to Dionysus*) | **Speak up.** The sailors ask you: "Ransom him, or sell him?" Pass with "Let him go." A fourth choice, "He's a god," appears only if you spotted a tell; it passes too, with a better line. As in the *Hymn*, vines climb the mast, and the sailors leap overboard as dolphins. | Post-climax, the crossing to Delphoi | **Grookey.** Rillaboom drums, and the maenads danced to drums. |
| E6 | **Artemis** | A girl with a bow, watching a harvest feast at a vineyard | **Find the forgotten altar.** Every altar at the feast has offerings but one small shrine at the edge, hers. Make an offering there. King Oeneus forgot Artemis at his harvest, and she sent the Calydonian Boar. | Post-game, Thyrsa's vineyards | **Tepig.** "The boar I sent was its great-grandmother. This one's tamer." |
| E7 | **Aphrodite** | An old woman collecting shells on Kythera's foam beach | **Discretion.** Carry a love letter between two shy villagers. The bag lets you read it, but don't. | Post-game, Kythera | **Oshawott**, evolving to **Hisuian Samurott.** Its scalchop is a scallop shell, and Aphrodite came ashore on one. |
| E8 | **Apollo** | **Sam,** a hired herdsman who lost his master's cattle, playing a lyre far too fine for a herdsman (named and drawn by the user's request, from a photo they gave; 2026-11-14). Apollo served King Admetus as a herdsman for a year, and the lyre is the one Hermes gave him to settle the stolen cattle (Homeric *Hymn to Hermes*). In the cave: "A baby stole these from me once. Walked them backwards. Then he paid me with this." | **Track them.** Follow backward hoofprints: Hermes stole Apollo's cattle walking them backward. Walk against the prints to a cave. This pays off the Hermes amphora (§5). | Post-game, near Arkadia | **Chimchar.** Infernape's crown of fire is the sun's. |
| E9 | **Hera** | An old woman stranded at a flooded ford. Hera tested Jason this way at the river Anauros. | **Carry her across.** Twelve tiles of ford, with no running. Mid-river you lose a sandal, as Jason did; she gives it back on the far bank. | Post-game, the river below Arkadia | **Chikorita.** Meganium's flower collar; lilies sprang from Hera's milk. |
| E10 | **Hecate** | A hooded old woman at a three-way crossroads, **at night only.** This is the one test that needs a time, and a xenia rest (§10) can reach it. | **Don't look back.** Leave her supper, a Barley Cake, at the stone, then walk 8 steps without turning toward her. Turning ends the visit. | Post-game, the mouth of Hecate's Hollow | **Mudkip.** A creature of thresholds, half water and half earth. |
| E11 | **Hades** | A grey, ragged shade on a riverbank, buried without the ferryman's fare | **Give your obol.** The Bronze Obol, your Elaia well coin. | Post-game, before the Katabasis, the river near Cape Tainaron | **Totodile.** "The river's jaws. He'll mind you." |
| E12 | **Persephone** | A pale girl gathering narcissus at dusk, lost. She was picking flowers when she was taken. | **Guide her home.** Walk her to Demeter's altar in Eleusa. | Post-game, after the Katabasis, when spring returns | **Bulbasaur.** The bulb that blooms when she comes home. |
| E13 | **Proteus**, the Old Man of the Sea | An old seal-herder asleep among his seals on a beach | **Hold fast.** Four wild battles in a row against his shapes: a lion, a serpent, a leopard, a wave. No healing between, and fleeing ends the test. Menelaus held on to Proteus this way (*Odyssey* 4). | Post-game, the Odyssey's islet | **Sobble.** It vanishes and changes, like him. |
| Finale | **Zeus and Hermes** | Two ragged travelers in a storm, at **your own home** | **Host them,** with Mom. This is Baucis and Philemon. Mom takes down the honey jar labelled "NOT FOR {PLAYER}" (SCRIPT.md, 1F roster). The wine jug never empties. | Post-game, after E1–E13. It plays as the Odyssey's homecoming night if that arc is done (PITCH §6.4 ends at Elaia). | **Treecko,** from Hermes: Baucis and Philemon became an oak and a linden, woven together. **Scorbunny,** from Zeus: Olympia's games were his. |

| Gift | Lv | Held | Nature | Ability | God-taught move |
|---|---|---|---|---|---|
| Squirtle | 45 | White Herb | Modest | Rain Dish | Shell Smash |
| Charmander | 45 | Charcoal | Timid | Solar Power | Dragon Dance |
| Turtwig | 50 | Leftovers | Impish | Shell Armor | Wood Hammer |
| Torchic | 50 | Expert Belt | Adamant | Speed Boost | Swords Dance |
| Grookey | 50 | Grassy Seed | Adamant | Grassy Surge | Drum Beating |
| Tepig | 55 | Assault Vest | Brave | Reckless | Head Smash |
| Oshawott | 55 | Mystic Water | Jolly | Shell Armor | Razor Shell |
| Chimchar | 55 | Choice Scarf | Naive | Iron Fist | Mach Punch |
| Chikorita | 55 | Light Clay | Bold | Leaf Guard | Aromatherapy |
| Mudkip | 55 | Sitrus Berry | Relaxed | Damp | Stealth Rock |
| Totodile | 55 | Life Orb | Adamant | Sheer Force | Aqua Jet |
| Bulbasaur | 60 | A Pomeg Berry ("six seeds are missing") | Modest | Chlorophyll | Giga Drain |
| Sobble | 60 | Scope Lens | Timid | Sniper | Snipe Shot |
| Treecko | 60 | Miracle Seed | Timid | Unburden | Leaf Blade |
| Scorbunny | 60 | Choice Band | Jolly | Libero | Pyro Ball |

All of these carry the shared touches: a Cherish Ball, 3 perfect IVs, the Xenia Ribbon, the fateful flag and the met string.

**Three more reveals.**

**Hermes (E1), at the next town's herm.**

[He sits on the herm's base, swinging his feet, wearing your Talaria.]
```text
MESSENGER: There you are. Fine sandals. Whoever made these knew feet.

MESSENGER: Most people say no. Some say yes, then chase me for them.

MESSENGER: You just walked. The whole way. Without much whining.
```
[He stands. There is no shadow under him. There never was.]
```text
HERMES: Look at my feet, {PLAYER}. No shadow. Bad habit of ours, pretending.

HERMES: Remember it. We're about. More than you'd think.

HERMES: Your sandals. I loosened the left strap. You're welcome.

HERMES: And this. A tortoise. My first lyre was a tortoise shell. Don't tell him.

{PLAYER} received a Squirtle from Hermes!
```

**Athena (E3), at the loom.**
```text
OLD WEAVER: Are you the greatest trainer in Aethos?
```
?? YES / NOT YET / I DON'T KNOW
```text
> YES:
OLD WEAVER: Hm. A girl in Astyra said that about weaving once.
```
[She turns back to her loom. The visit ends.]
```text
> NOT YET / I DON'T KNOW:
OLD WEAVER: Good answer. The best never know. The worst always do.
```
[The shuttle flies across the loom by itself. An owl lands on the beam.]
```text
ATHENA: I warned a weaver once. She said she was better than the gods.

ATHENA: She was very good. She's a spider now.

ATHENA: Take this one. It carries an olive tree. Mine, from the Akropolis.

{PLAYER} received a Turtwig from Athena!
```

**Hecate (E10), at the crossroads.**
```text
HOODED WOMAN: Leave my supper at the stone. Then walk away.

HOODED WOMAN: Don't look back. People always look back.
```
If the player turns toward her:
```text
The footsteps behind you stop. When you look, the crossroads is empty.
```
After eight steps without turning:
```text
Behind you, three dogs bay at once. Three torches catch. You don't turn around.

VOICE: Good. Most people can't do that. Orpheus couldn't.

HECATE: Hold your hand out behind you. Don't turn.

{PLAYER} received a Mudkip from Hecate!

HECATE: A doorway creature. Half water, half earth. Like me.
```

**The finale: Baucis and Philemon, at home.**

[A storm night in Elaia. Knocking. Two ragged travelers stand in the doorway: a big old man with a heavy beard, and a young one in muddy sandals.]
```text
MOM: In, in, before you drown. {PLAYER}, the stools.

MOM: There's bread. There's… hm. There's honey.
```
[She takes down the new jar, labelled NOT FOR {PLAYER} again. She gave the old one away at Delphoi (STORY §7.5).]
```text
MOM: Habit.

MOM: Don't look at me like that. They're guests.
```
[The player pours wine for the guests. The jug stays full.]
```text
MOM: …{PLAYER}. The jug.

MOM: I've poured from it six times.

YOUNG TRAVELER: Told you they'd notice. They always notice at the jug.
```
[Thunder with no rain. The old man stands, and the ceiling seems very far away.]
```text
ZEUS: Melitta of Elaia. Your only honey, on a night like this, for strangers.

ZEUS: Ask for something.

MOM: …

MOM: Bring my child home. That's all. Every time.

ZEUS: Done. Though from what I hear, your child decides that now.

HERMES: Feet, {PLAYER}. Always check the feet.

HERMES: This one's for the old couple who turned into trees. Long story.

{PLAYER} received a Treecko from Hermes!

ZEUS: And this one runs like my games did.

{PLAYER} received a Scorbunny from Zeus!
```
From then on, Mom's new honey jar never empties. She gives you one Honey a day.

STORY §4 reads Zeus's line in hindsight: feeding strangers before asking their names is Mom's habit, and the reason the hero is alive.

#### Engine

| Piece | How | Effort |
|---|---|---|
| Gifts | `givemon` already takes species, level, held item, ball, nature, ability number, IVs and four moves (`asm/macros/event.inc`, around line 1056). Then `setmondata` sets the fateful flag and the ribbon. | Low |
| Met string | A new met-location value, shown on the summary screen as "a guest-gift of …" | Low–Medium |
| Hisuian evolutions | Quilava and Dewott evolve into their Hisuian forms in Aethos. The expansion gates this on `IF_REGION, REGION_HISUI` (`src/data/pokemon/species_info/gen_2_families.h`, line 431). Ichor makes the condition true: PITCH §4 puts Hisuian forms in Aethos. | Low, a dex-team change |
| Strangers | Objects with hide flags. They appear by story flag, or by the day's Stranger omen (`src/ichor_omen.c`). | Low |
| No shadow | A per-object opt-out from the shadow every object now gets (`OW_OBJECT_VANILLA_SHADOWS` FALSE) | Low–Medium |
| The follower bows | A new condition in the follower reaction table (`src/follower_helper.c`): "near a theoxenia object" | Low–Medium |
| Augur's Eye line | One line on its screen (`src/dexnav.c`) | Low |
| Tests | All scripts, using systems already specified: the bag picker (§3), carried flames (§2), a "don't run" flag (Hephaestus, Hera), clearing `FLAG_SYS_B_DASH` for a walk (Hermes), a facing check on each step (Hecate), four `setwildbattle`s in a row (Proteus), a partner double battle (Ares), a letter item with a "read" option (Aphrodite), footprint metatiles (Apollo) | Low each |
| Escorts | Walk-with tests use scripted movement, not the expansion's NPC followers (`FNPC_ENABLE_NPC_FOLLOWERS`, FALSE in `include/config/follower_npc.h`), which would cost SaveBlock3 space | Low |

#### ROM: a note for the dex team

The Aethos dex is Aethos-only (D5), but **these species must stay in the ROM.**

INVENTORY puts species art and data at about 3.7 KiB per form, and cries at about 8 KiB each. So each kept species costs about 11.7 KiB.

| Tier | Species kept | Cost |
|---|---|---|
| Core | 3 lines × 3 = 9 species, plus Hisuian Typhlosion | ~110 KiB |
| Extended | 15 lines × 3 = 45 species; Hisuian Samurott; the classic Megas of these lines (Venusaur, Charizard X and Y, Blastoise, Sceptile, Blaziken, Swampert), since Apotheosis is on | ~560 KiB more |
| **Both** | 54 species, 2 Hisuian forms, 7 Megas | **~670 KiB (0.65 MiB)** |

Cries are most of it.

Two more notes for the dex team:
- **The Pokédex needs a place for them.** I propose a short **"Visitors"** page after the Aethos list, recording the gift lines.
- **Their follower sprites** come with the kept species data (INVENTORY §3).

#### Flags and vars

- 16 visit flags, `FLAG_ICHOR_THEOXENIA_<GOD>`: 3 core and 13 extended.
- 1 finale flag.
- About 17 hide flags.
- About 10 decoy flags.
- The Stranger omen uses `IchorSave.omen`.
- No vars.

---

## 11. "Know thyself" at Delphoi

**Pushback.** The bible's modern features already include an EV/IV viewer on the summary screen (PITCH §5). An Oracle who judges IVs would duplicate it. So the Oracle does something only she can do, and it changes with the story.

### Play and rules

**Before the climax.**
- Phemonoe, the Pythia and eighth Hierophant, answers everyone in single words. The slice already seeds this: "the Pythia answering in single words".
- To you she says nothing at all:
  ```text
  PYTHIA: …

  PYTHIA: I can't see you.
  ```

**After the climax,** when prophecy is over, she offers **"Know thyself"** (*gnōthi seauton*, carved over the real temple's door):
- a **Pythian Laurel** perfects one IV;
- a **Golden Pythian Laurel** perfects all six.
- These are the Bottle Caps, renamed. Hyper training is the service.

She can also change a Pokémon's nature, as the mints do.
```text
PYTHIA: For a thousand years they asked me who they'd be.

PYTHIA: Ask me who you want to be. That one I can help with.
```

### Engine

- A script and a special that sets `MON_DATA_HYPER_TRAINED_*` (`include/pokemon.h`, line 117 onward).
- Rename `ITEM_BOTTLE_CAP` and its gold version.
- **Low.**

### Flags and vars

`FLAG_ICHOR_PYTHIA_KNOW_THYSELF`.

---

## 12. Temple trials as a design language

Each Olympian's temple teaches **one puzzle verb**. The Labyrinth's seven rings test them again, combined (LABYRINTH.md).

Every trial follows MAP_DESIGN §4. The Hearth Trial is the model.
- **Taught in the first room, tested in the middle, mastered at the end.**
- **Acolytes are checkpoints** between the stages. At least one is optional.
- **The Hierophant waits at the climax of the architecture.**
- **After the laurel,** the room stays solved and the acolytes stay beaten.

Every trial also has:
- a safety valve: an acolyte who will show you, or a reset with no penalty;
- no time-of-day requirement.

| # | Temple | Verb | The trial | Engine | Tested again in |
|---|---|---|---|---|---|
| 1 | Hestia (Akti) | **Carry the flame**: order and return | The Hearth Trial. Built: SCRIPT.md Part 5. | Script | Ring I |
| 2 | Hermes (Emporion) | **Race and route** | The Herald's Run | Step hook, `VAR_TEMP` · Low | Ring II |
| 3 | Demeter (Eleusa) | **Dark and light**: torch, braziers, dousing | The Lesser Mysteries | Glow palette · Low–Medium | Ring III |
| 4 | Dionysus (Thyrsa) | **Masks and roles** | The Three-Act Play | Mask var · Low | Ring IV |
| 5 | Artemis (Arkadia) | **Stealth** | The Hunt for the Hind | Non-battle sight objects · Low–Medium | Ring V |
| 6 | Hephaestus (Kaldera) | **Automata and gears** | The Bronze Servants | Movement swaps, an "object on tile" special · Medium | Ring VI |
| 7 | Aphrodite (Kythera) | **Marble and mirrors** | Galatea's Gallery | A custom "watched" movement type · Medium | Ring VII |
| 8 | Apollo (Delphoi) | **Beams** | The Pythian Light | A beam-trace special shared with Ring VII · Medium | — (the Labyrinth's Starry Chamber previews it) |

**2. Hermes: the Herald's Run.**
- **The task:** Kerykos hands you sealed scrolls to deliver to herald-herms inside a switchback stoa, within a step-glass. Steps don't count during battles, and a failure simply returns the scrolls to Kerykos.
- **Teach** (the entry porch): one scroll, one herm 20 steps away, a glass of 40 steps. One herm head swivels to point the way once you anoint it (a second use of oil).
- **Test** (the main stoa): three scrolls and three herms inside one glass of 120 steps on Hero (150 Mortal, 100 Spartan). Hermes's turnstiles are one-way, and the wrong one loops you back.
- Kerykos names the selected budget in both explanations; the glass's halfway warning follows it (60 steps remaining on Hero, 75 Mortal, 50 Spartan). Its low warning remains at 30.
- **Master** (the upper colonnade): the herms point the way only when anointed, and each turnstile reverses after you pass a herm.
- **Acolytes:**
  - one mandatory, easy and in plain view at the porch's narrow exit;
  - one **optional**, facing away in a side colonnade, guarding a shortcut turnstile;
  - one mandatory before the rostrum.
- **Kerykos** waits on the herald's rostrum at the head of the stoa's steps.

**3. Demeter: the Lesser Mysteries.**
- **Teach** (the vestibule): one brazier is already lit. Douse the torch, and a single glowing pomegranate seed shows by your feet. Relight.
- **Test** (the Telesterion's hall): four seeds across a pitch-dark hall, Persephone's trail.
  - Each seed is seen doused and reached lit.
  - Each seed is beside a season's brazier, and lighting it brightens a quarter of the hall for good.
- **Master** (the anaktoron, the inner shrine): the seeds show only when doused, the walls only when lit, and the path between them crosses a draught that blows out a carried flame. This combines dousing with Hestia's wind verb, so you must relight from the season braziers on the way.
- **Acolytes:** three *mystai*; one **optional**, beside a side seed.
- **Chloe** waits in the anaktoron. Her reveal is a single reaped ear of grain.

**4. Dionysus: the Three-Act Play.** Built: `data/maps/ThyrsaCity_TempleOfDionysus/scripts.pory`, map from `tools/ichor/maps/thyrsa.py`.
- **The play** is *The Vintner's Gift*. Three painted scenery walls stand between the green room (backstage, by the entrance) and the stage-building's roof, one wall per act, each with a left, middle and right door. Each act is one entrance: the right door in the right mask walks you onto the next stage, and that door stays open.
- **The rules**, chalked in the green room: come on through the door painted with where you've just been; wear the face your part would wear; miss your cue and the floor will find you. The doors are painted with vines on a hillside (left), a house's lit gate (middle) and a ship with ivy up its mast (right). Masks hang on a rack in the green room only, so you dress before you go up.
- **Teach** (Act I): the script says the stranger steps off a ship, laughing. Comedy, right door. The prompter catches a wrong try for free.
- **Test** (Act II): "Enter the one they blame." The vintner poured, then went in to bed: he comes from the house (middle). His mask takes two clues: the comic acolyte says nobody laughs in Act II, and a fresco says the goat-men always come last. Tragedy, middle door.
- **Master** (Act III): the page is torn off. A tragedy is followed by the satyr play (the fresco, the chorus leader), and the goat-men follow their god in by his door (a second fresco, the tragic acolyte). The comic acolyte lets slip that the stranger is the god, so the god's door is the ship's. Satyr, right door. Myth-savvy players spot Dionysus in the ivy-masted ship.
- **Costs:** in Acts II and III a wrong door is a trapdoor back to the green room, and the right door in the wrong mask is a battle with the chorus (`TRAINER_ICHOR_THYRSA_CHORUS`, fought again every time).
- **Acolytes:** the comic actor guards the one gap in Act I's footlights; the tragic actor on Act II's stage is **optional** and gives a clue; the satyr actor guards the crane.
- **Safety valve:** the prompter in the green room gives a nudge for the act you're on.
- **Thespis** waits on the stage-building's roof. The mechane (crane) lifts you there once Act III is played, and lowers you again.
- **The Dionysia** reuses the painted doors. Thespis's cues name no doors ("a fool drunk in the vineyards", "someone from the king's own house", "the goat-men, the way they come in"), and a wrong cue undoes the entrances made so far.

**5. Artemis: the Hunt for the Hind.**
- **The grove** is a temple garden under endless night. A hound that sees you sends you back to the start of the current stage, not the whole trial.
- **Teach:** one hound walks a short line across a glade, with an obvious bush to wait behind.
- **Test:** three hounds and two moonlit clearings, where sight range doubles.
- **Master:** the golden hind bolts to another clearing each time you touch her antler, three times, while the hounds patrol.
- **Acolytes:** huntresses, one per stage; one **optional**.
- **Kallisto** waits on a moonlit rock above the last clearing.

**6. Hephaestus: the Bronze Servants.**
- **Teach:** one automaton walking a loop, one plate and one dial.
- **Test:** two automata, two plates, two dials.
- **Master:** three automata on three plates at once. One loop can only be cut with a column drum pushed by the Girdle, which combines this verb with Strength.
- **Acolytes:** smiths; one **optional**.
- **Talos** waits at the great anvil on the forge's raised floor.

**7. Aphrodite: Galatea's Gallery.**
- **The rule:** marble statues step toward you only while you face away from them. A statue you can see in a bronze mirror can't move. A touch sends you back to the stage's start. Pygmalion's statue was the original marble that came alive.
- **Teach:** one statue in a short corridor, and one mirror.
- **Test:** three statues and two fixed mirrors.
- **Master:** statues and mirrors you can turn. It is the first rotating mirror in the game, and it previews Apollo's beams.
- **Acolytes:** two; one **optional**.
- **Galatea** waits on her dais.

**8. Apollo: the Pythian Light.**
- **Teach:** one mirror, one sunbeam, one target, in the pronaos.
- **Test:** carry the beam from the oculus through four chambers. By night it is a moonbeam on the same path.
- **Master:** focus the beam onto a brazier to light it, then carry that firelight on to the Omphalos's tripod. This combines beams with Hestia's flame.
- **Acolytes:** three; one **optional**.
- **Phemonoe** waits on the tripod in the adyton, the temple's innermost room.

**Engine notes.**

- **Non-battle sight (Artemis, and the Labyrinth's Asterion).** The expansion already supports trainer-sight objects whose scripts aren't battles.
  - `CheckForTrainersWantingBattle` (`src/trainer_see.c`, around line 436) sends a non-`trainerbattle` script through `EventScript_ObjectApproachPlayer`.
  - It runs every frame the player has control, so a patrol walking into you while you stand still still spots you.
  - Sight is a straight line in the facing direction, blocked by walls (`CheckPathBetweenTrainerAndPlayer`).
  - `OW_FLAG_NO_TRAINER_SEE` switches all sight off; the Helm of Darkness uses it (LABYRINTH.md).
- **Statues (Aphrodite).**
  - A new movement type checks on each player step whether the player is facing the statue, or facing a mirror that reflects it. If neither, the statue steps toward the player.
  - The vanilla copy-the-player movement types (`MOVEMENT_TYPE_COPY_PLAYER*` in `include/constants/event_object_movement.h`) are the nearest model.
- **Beams (Apollo, Ring VII).** A C special walks a grid from the source, turns at mirror objects by their facing, and swaps beam metatiles along the path.

---

## 13. Cut, replaced or deferred

| Idea | Decision | Why |
|---|---|---|
| Athena's polished shield, a beam relic | **Deferred** | A carried mirror has one verb. Fixed bronze mirrors in Aphrodite's and Apollo's temples and Ring VII give the beam puzzles without a relic. If wanted later: a post-game **Perseus's Shield** for a Gorgon's-isle quest. Avoid "Medusa" in any name (LAZARUS.md). |
| "Know thyself" as an IV judge | **Replaced** by post-climax hyper training (§11) | The summary screen already has the viewer |
| A Pokémon's first-caught feather as an offering | **Replaced** by the 7 existing feather items, as Artemis's "first of the hunt" | No new tracking needed |
| Festivals on real dates | **Replaced** by the 36-day Aethos year | Players would rarely see them |
| Knucklebones for money | **Cut** | It stays a friendly game |
| Overworld wild encounters (`WE_OW_ENCOUNTERS`) | **Not proposed** | The config warns about VRAM with compressed followers on |
| Rock Climb as a main-path relic | **Optional only:** Dionysus's Thyrsus, gift II | The expansion has it (`OW_ROCK_CLIMB_FIELD_MOVE`), but the main path doesn't need another verb |
| Brazier halos in open caves | **Stretch** | Lit zones do the job in 1.0 |

---

## 14. Save data

The new state lives in one struct in SaveBlock3.
- The block can hold **1,624 bytes** (a `STATIC_ASSERT` in `src/save.c`).
- Today it holds only `dexNavChain` (1 byte). `USE_DEXNAV_SEARCH_LEVELS` is FALSE, and the fake RTC, NPC followers and item-description flags are off.

```c
struct IchorSave              // in SaveBlock3; ~760 bytes of 1,624
{
    u8  version;
    u8  favor[16];            // §3, one per god
    u16 blessing;             // §3, 4-bit god + 12-bit steps
    u32 litBraziers[4];       // §2, 128 braziers
    u32 digDaily[2];          // §5, cleared daily
    u8  sherds[6];            // §5, 48 bits
    u32 ostraka;              // §5
    u32 constellations;       // §8
    u32 herms;                // §4, mirrors the flags for the fly map
    u16 momWins, momLosses;   // §9, momLosses starts at 212
    u16 omen;                 // §6
    u16 festivalsSeen;        // §7
    u8  xenia[4];             // §10
    struct IchorThread thread;// LABYRINTH.md: ~660 bytes
};
```

- **Saves break when this is added.** RESEARCH §1 warns that changing the save layout breaks saves, so add it once, early in Phase 2, before long playtests.
- **Keep a `version` byte** so later additions can migrate saves.
- **Flags:** about 250 new flags across all systems, out of 332 unused, plus the Hoenn story flags that free up as their maps go (INVENTORY §9). The 52 unused daily flags cover prayers and festivals.

---

## 15. Recommended scope

| Feature | Essential for 1.0 | Stretch, if time allows | Post-1.0 |
|---|---|---|---|
| Relics | Relics 1–11, contextual prompts, the Relic Ring, the option | The relic-icon pose | The Pearl, the Bag, Triton's Conch, the Helm of Hades |
| Fire and light | Torch levels, lit zones, webs, douse, the carried-flame grammar | Brazier halos | — |
| Rites | Altars, prayer, offerings, Favor, all 15 blessings, gifts I and II, Hierophant links, desecrated altars | Gift III (sacred animals) | Hades's row |
| Herm waystones | All | — | — |
| Excavation | Trowel, daily spots, coins, fossils, sherds with text-only amphorae, ostraka, prophecy fragments, pages | Amphora paintings | — |
| Omens | All four kinds | More entries | — |
| Festivals | Panathenaia, Anthesteria, Kronia, the story Dionysia | Mysteries, Pyanopsia, Poseidea | The rest, the yearly Klotheia epilogue |
| Katasterismoi | Constellation bits recorded (data only) | The chart screen | Labor and Atlantis constellations |
| Knucklebones | Script version, 6 taverns, Mom | The bone-sprite screen | — |
| Xenia | Hosts' tables and rest | The 3 token chains | More chains |
| Theoxenia | The core tier: Demeter, Hephaestus and Poseidon; the tells; the decoys | The extended chain's Act III visits (E1–E5), if D8 picks extended | The post-game visits (E6–E13) and the finale, if D8 picks extended |
| "Know thyself" | All | — | — |
| Temple trials | All 8 | — | — |

**By roadmap phase** (PITCH §8):

| Phase | What lands |
|---|---|
| 2 (Act I) | `IchorSave`; relics 2–4; the Relic Ring; darkness; rites core with Kerykos's tutorial; herm anointing; Trowel and digs; omens; knucklebones; the Hermes and Demeter trials |
| 3 (Act II) | Relics 5–7; herm flight; the Dionysus, Artemis and Hephaestus trials; the Panathenaia, Dionysia and Anthesteria; prophecy fragments |
| 4 (Act III) | Relic 8; the Labyrinth with relics 9–11; the Aphrodite and Apollo trials; "Know thyself"; the Kronia |
| 5 (post-game) | The Endless Labyrinth; relics 12–13 and the upgrades; post-game constellations; Hades; the remaining festivals and chains |

**The slice (Phase 1) is not changed,** apart from the optional two-line seed in LABYRINTH.md.

---

## 16. Proposed changes to PITCH.md

1. **§5, the relic table.** Replace it with §1's table.
   - Cut moves from the Labrys to **Demeter's Sickle**.
   - The **Labrys** becomes the Labyrinth's tool (dials, seals, chains).
   - Waterfall gets the **Horn of Achelous**.
   - Add **Ariadne's Thread** and the **Helm of Darkness**.
   - List **Alethea's Trowel** and the **Star Chart** as tools.
   - State when each relic arrives.
2. **§5, Systems.** Add the Rites (Favor, blessings, gifts), herm waystones, excavation, omens, the festival calendar, the Katasterismoi, knucklebones, xenia and "Know thyself". Add the design principle: **the main path never needs a time of day, a date, luck or a grind.**
3. **§1, the re-skin table.** Add three rows:
   - Escape Rope → Ariadne's Thread, inside the Labyrinth; the rope still works elsewhere.
   - VS Seeker → Ares's War Horn.
   - Shiny Charm → the Acorn of Dodona.
4. **§6.1, the Labors.** If the Girdle of Herakles stays as the Strength relic, rename the ninth Labor's prize **Hippolyta's War-Belt** (D2).
5. **§6.2, Katabasis.**
   - Hades, or Minos as judge of the dead, asks for the Helm of Darkness back, then upgrades it.
   - The slice's well coin is Charon's obol.
6. **Item renames.**
   - Relic Copper, Silver and Gold become the Bronze Obol, Silver Owl and Gold Stater, with new descriptions.
   - The Bottle Caps become Pythian Laurels.
7. **Berries.** Keep the berry system, restyled, as first-fruits offerings (D6). This resolves INVENTORY §1's open berry row.
8. **Mass outbreaks.** Keep `src/mass_outbreak.c` for omens, even though the TV is cut (D7). This amends INVENTORY §10's proposal.
9. **§4, the starters, and the Sanctuary of Firsts.**
   - Today PITCH §4 says "A post-game Sanctuary of Firsts offers every other starter."
   - Replace it with **theoxenia** (§10): gods in disguise give the old starters as guest-gifts.
     - The core tier is Snivy from Demeter, Cyndaquil (into Hisuian Typhlosion) from Hephaestus, and Piplup from Poseidon, after Laurels 5, 6 and 7.
     - The extended tier, if chosen, adds the 15 other starter lines that are not among Lazarus's nine.
   - **Lazarus's nine starters are offered nowhere** (D9).
10. **§4, ROM.** Record that the gift species stay in the ROM despite the Aethos-only dex: about 110 KiB for the core tier and about 670 KiB for both (§10).
11. **The slice's maps (not PITCH).** Add three relic gates to Kalliste for the map team, so Act III has old places to reopen (§1, "Relic gates"; MAP_DESIGN §1 and §5):
    - marble rubble at a grotto on Akti's tide rocks (the Bronze Hammer);
    - a dark stair at the bottom of Kronion Hill's dig pit (the Torch);
    - a shrine on the islet off Akti's quay (the Conch).

    None changes the slice's path or script (D10).

---

## Decisions for the user

> **Approved by the user, 2026-11-14:** D1 (the relic re-mapping), D3 (all 15 gods), D8 (core plus extended theoxenia) and L10 (seven rings). Every other decision here and in the other doc follows the designer's recommendation. PITCH.md has been updated to match. D10 (the three Kalliste relic gates) was approved by the director under the user's map rules.

These are the ones this file raises. LABYRINTH.md adds its own.

- **D1. The relic re-mapping.**
  - Cut becomes Demeter's Sickle.
  - The Labrys becomes the Labyrinth's tool.
  - Waterfall becomes the Horn of Achelous.
  - The Thread and the Helm are added.
  - Athena's shield is deferred.
- **D2. Two girdles.** Keep the Girdle of Herakles and rename the ninth Labor's prize (recommended), or rename the Strength relic.
- **D3. How big the rites are in 1.0.** All 15 gods with gifts I and II (recommended), or only the 8 temple gods plus Hecate, with the Pantheon gods added at Phase 4.
- **D4. Festivals** on the 36-day Aethos year (recommended), or on real calendar dates.
- **D5. The relic prompt's default:** ASK (recommended for a first playthrough) or AUTO.
- **D6. Keep berries** as first-fruits offerings.
- **D7. Keep `mass_outbreak.c`** for omens.
- **D8. The theoxenia tier.**
  - **Core only:** 3 gifts, about 110 KiB of ROM.
  - **Core plus extended:** 18 gifts, the chain of strangers and the finale at home; about 670 KiB of ROM.
  - I recommend core plus extended. It is the post-game's best recurring thread, and it ends at Mom's table.
- **D9. Lazarus's nine starters.** Never offered (recommended), or offered elsewhere despite the avoid-list.
- **D10. Three relic gates added to the slice's maps** (Akti's rubble grotto, the stair under Kronion Hill's pit, Akti's islet shrine), so the rulebook's "every relic opens something already visited" holds from Kalliste on.
