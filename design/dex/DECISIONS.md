# Aethos dex: decisions

Every decision the user makes about the regional dex, newest gate last. Dates are when the user decided.

## Before Gate 1

| Date | Decision | Source |
|---|---|---|
| 2026-11-14 | Design a new Aethos regional dex of about 150 species inspired by Greek myth, following a traditional region's structure. This replaces the bible's earlier "no new species". | The user, in the main session: "full 150 greek myth inspireed that follows the traditional pokemon guidelihes of a region" |
| 2026-11-14 | The user sees the complete dex, with art, before anything is implemented in the ROM. | Same message: "I want to see all of them made the full dex before we impliment them" |
| 2026-11-14 | Ichor is a private project and won't be released, so AI-art and AI-writing bans on release sites don't apply. | The user, relayed by the main session: "this is just a fun project for us, so we can make them. not being sent to anyone." |
| 2026-11-14 | Every species gets Gen 3 pixel sprites: front, back, shiny palette, icon, footprint and follower overworld. This settles the art question, so Gate 3 no longer asks how to visualize. | The user, relayed: "yes we want pixel sprites." |
| 2026-11-14 | Every entry has full data: EV yields, complete learnsets (level-up, TM and tutor, egg) using existing moves, and evolutions. | The user, relayed: "make sure you handle all the EVs, the moves, evolutions etc. this will be a full game." |
| 2026-11-14 | Total conversion: every sprite is Greek-myth inspired and nothing on screen stays Hoenn. See `design/ART_PLAN.md`. | The user, relayed: "every sprite needs to be greek myth inspired. we dont want to leave anything really unchanged" |

## Gate 1: the dex plan

Plan: `design/dex/PLAN.md` (generated from `plan.yaml`). Review page: https://claude.ai/artifact/RqaQokm636va9rD6qDGyDg

| # | Question | Recommendation | Answer (2026-11-14) |
|---|---|---|---|
| — | Approve the 150-slot plan | — | Approved: "these will replace the starters and the be the regions pokemon" |
| D1 | Regional starters replace Snivy, Cyndaquil and Piplup | Yes, once the species exist in the ROM | Yes |
| D2 | Kronos and the Moirai replace Dialga and the lake trio in the story | Yes | **Yes**, confirmed by the user-approved master story, `design/STORY.md` S19 on main: the Lord of Time (Kronolith) and the three Fates replace Dialga and the lake trio. In scenes, the name boxes call the Fates SPINNER, MEASURER and CUTTER (S10). |
| D3 | Add Kairos as a post-game legendary at Olympia | Yes | **Yes**, per `design/STORY.md` S11: the Moment (Kairazor) restarts time on the Stair of Hours, where you seize it as it runs down the falling sickle. It can only be caught in the post-game, at Olympia. |
| D4 | Two mythicals, Hope and Ichor | Yes | Changed: "mythicals should be like a zeus pokemon, a posiden pokemon, and a hades pokemon. as like regis giant types ... with good names." Three Regi-style colossi, the cult statues of the brothers who drew lots for the world, replace Hope: Olympanax (Zeus, Electric), Pontanax (Poseidon, Water) and Nekranax (Hades, Ghost). Ichorin, the title Pokémon, stays as a fourth mythical at #152: "Keep it as #152". The dex is 152. |
| D5 | How the regional dex mixes with the existing 1,025 species | (a) Aethos-only through the League | (b) mixed: "while we add in the other pokemon into the region too". Then changed to (a): "(a). It makes Aethos feel like a real new region and keeps the bible's post-game promise. lets switch it to this". Only Aethos's own species appear until the League is beaten; existing species arrive in the post-game. |
| D6 | Post-game Labors use regional species where one exists | Yes | Open |

**D1 follow-up (2026-11-14): the old starters return as gifts from the gods.** The user, relayed by the main session: "we need to make it later game to be able to receive the old starters as blessings from gods in disguise."
- The Snivy, Cyndaquil and Piplup lines don't leave the game when the Aethos starters replace them. They return mid-to-late game as gifts from gods in disguise (theoxenia, in the spirit of Baucis and Philemon).
- The main session's systems designer is specifying it, with an optional extended tier in which other generations' starters also come as gifts.

**Theoxenia tier (2026-11-14): core plus extended.** The user picked both tiers, relayed by the main session. The spec is `design/SYSTEMS.md` §10 on main. There are 18 gift lines; Lazarus's nine starters are offered nowhere.
- **Core:** Snivy from Demeter, Cyndaquil from Hephaestus (evolving into Hisuian Typhlosion), Piplup from Poseidon.
- **Extended:**
  - Squirtle (Hermes), Charmander (Hestia), Turtwig (Athena), Torchic (Ares)
  - Grookey (Dionysus), Tepig (Artemis), Oshawott (Aphrodite), Chimchar (Apollo)
  - Chikorita (Hera), Mudkip (Hecate), Totodile (Hades), Bulbasaur (Persephone)
  - Sobble (Proteus)
  - The finale: Treecko and Scorbunny from Zeus and Hermes
- **The Pokédex's "Visitors" page.** The gift species get their own page after the Aethos dex's #1–152. It's unnumbered, grouped by the god who gave each one, and each entry notes the guest-gift. It's to be specified here before implementation.

**Asterion is Asterlorn (#98, Fighting/Dark).** The Labyrinth's Minotaur gets this dex's own species, not the placeholder Paldean Tauros. The entry already makes him the one-of-a-kind Minotaur chained at the Labyrinth's heart, catchable after the raid, which fits `design/LABYRINTH.md`'s idea of him joining the player.

**Story traits the time pair's design must keep** (`design/STORY.md` S20):
- The Lord of Time carries the Harpe and a stopped hourglass, and is big enough to fill the sky.
- The Moment has a razor's edge, and a forelock with nothing behind it.
- Both have to be built in as anatomy, not props (the cohesion rule).

D6 doesn't block Gate 2. The entries for those species are written either way, and the open questions are about where they go in the story.

## Gate 2: the full entries

All 152 entries are in `design/dex/species/*.yaml`, and `tools/dex/validate.py --complete` passes them with no errors or warnings. Gate 2 reviewed 150; afterwards the three colossi replaced Hope and Ichorin moved to #152 (D4). Review page: https://claude.ai/artifact/D4PXiuRijZf2Sdubr9QADh

Choices made in review, which the user can overrule:
- **Borrowed signature moves.** Existing species arrive in Aethos in the post-game, so other Pokémon's signature moves were swapped for generic ones to avoid clashes there. Five were kept because the myth depends on them:
  - Kronolith: Roar of Time, and Mighty Cleave as a stand-in until Harpe exists.
  - Kairazor: Esper Wing.
  - Hoplektor: No Retreat.
  - Geogrip: Shore Up.
- **Stat and ability changes.**
  - The Archon's ace, Aetarch, got its own stat band and went up to 530 BST.
  - The Midas donkey's Nugget evolution needs level 25 or above.
  - The theater mask's hidden ability went from Moody to Cursed Body.

Waiting on the user:

| # | Question | Recommendation | Answer |
|---|---|---|---|
| — | Approve the 150 entries, or name the ones to change | — | pending |
| D7 | New move **Harpe** for Kronolith: Ground, physical, 100 power, hits through Protect and Substitute. It costs one new move and an animation. | Yes: the story spends two acts rebuilding the Harpe | pending |
| D8 | New move **Shield Clash** for the Kouretes line: Steel, special sound move, 80 power, stops the target using sound moves for two turns. It costs one new move and an animation. | Optional: Steel moves already cover the role | pending |
| D9 | Call the title mythical **Ichorin** (coined) or plain **Ichor** | Ichorin, matching the other coined names | Ichorin (2026-11-14): kept under that name as #152, from the user's "Keep it as #152" reply to a question that named it Ichorin. |

## Gate 3: sprites

| Date | Decision | Source |
|---|---|---|
| 2026-11-14 | The 150 entries are approved. Sprites start. | The user: "Approve, start sprites" |
| 2026-11-14 | Every sprite must be as detailed and well designed as an official Pokémon's: hand-finished battle sprites, not just code-drawn ones. | The user: "make sure they are as detailed and designed well as any normal pokemon. spend time" |
| 2026-11-14 | Legendaries, mythicals, the Olympian colossi and the Astral constellations form a top tier: concepts first for the user to pick, then one artist per species. See "The legendary tier" in `design/dex/SPRITES.md`. | The user: "all legendaries and mythical olympians constilations etc need to be fucking awesome. powerful. mysterical. the best pokemon ever designed" |
| 2026-11-14 | Time pair: **round 2, pair A, "Adamant"**.<br>**Kronolith** is a four-legged Devourer behemoth on column legs: a bronze helm grown into its skull, a starry-void maw and broken-column fangs. One dorsal line runs from crest to spine to the Harpe arched over its back, and the stopped hourglass glows between its chest plates.<br>**Kairazor** is Lugia meets Dialga: razor-fingered wing-hands, Aegean plates with violet lines, a diamond chest gem, a psychic third eye, a gold forelock curling forward over a bare crown, and balance-pan tail fins.<br>They share the hourglass and diamond gem. The pair is to be rendered well beyond the concepts. See `design/dex/concepts/time_r2.md`. | The user: "A is the best" |
| 2026-11-14 | Fates direction: **A, Daughters of Night**. Three great birds sharing swan necks, crests and raised wings with black-figure flight feathers, a bronze whorl in the breast, and the golden thread as a glowing seam down the spine. The tail is each one's instrument: Nemira's twists into a spindle, Lotira's is a banded measuring plume, Thanira's splits into crossed shear-blades. It is to be rendered well beyond the rough concept. See `design/dex/concepts/moirai.md`. | The user: "A" |
| 2026-11-14 | Colossi direction: **B, The Elemental Titans**. All three brothers wear one Cyclops-forged Corinthian helm and cuirass over their element: a thunderhead with cloud-eagle wings and a lightning crest (Olympanax), a curling wave with a water trident arm (Pontanax), a plume of shadow with bident talons and a ghost tail (Nekranax). The species' art briefs are to be rewritten to match once the renders pass review. See `design/dex/concepts/colossi.md`. | The user: "B, Elemental Titans" |
| 2026-11-14 | The Fire starter line (Kynder, Dikyon, Pylakyon) gets a concept round like the legendaries. Four rendering passes didn't reach the bar; three heads on a small pup get cluttered at Gen 3 size. Three line-wide directions, for the user to pick. | The user: "Yes, concepts first" |
| 2026-11-14 | Time pair concepts. **Kronolith: B, The Devourer** is the best of the set, to be developed into one cohesive creature. **Kairazor: none of the three.** A new direction instead: Lugia meets Dialga, with a Psychic twist. All three concepts felt disjointed, so cohesion is now part of the legendary-tier bar in `design/dex/SPRITES.md`. | The user: "i dont like any of these they all feel disjointed. the devourer is the best one of 146 and 147 i dont like any of them. i think lugia meets dialga with a twist for psychic st is the best" |
| 2026-11-14 | Legendary concepts picked. **Pegaunos: A**, Thunderhead Rampant: a white stallion rearing, with a lightning mane and thunderhead wings. **Ichorin: B**, The Marble Child: a living marble child with a vein of ichor. Both are to be improved well beyond the concepts. See `design/dex/concepts/`. | The user: "I like A and B tho obviously need to be improved", then "1A 2B" |
| 2026-11-14 | The user likes the starters' look. Final evolutions must feel grand and powerful: large in the frame, commanding poses, richer detail and effects. See "Evolutions must feel grand" in `design/dex/SPRITES.md`. | The user: "i like them. we just want to make sure these look amazing. and evolutions are truly grand and powerful etc" |

## Next, after the sprites: the Astral type

| Date | Decision | Source |
|---|---|---|
| 2026-11-14 | Add a new 19th type, **Astral**, a star type. Its Pokémon are the constellations: one for each major constellation, none of them evolving. They are a new category to be mixed into Aethos. | The user: "i also want a new type made once this is done called Astral, which is like a star type. that will be constellations. each maojr constillation will have a pokemon. no evolutions. this will be a new catagory we will want to mix in somehow." |

Questions for when this starts:
- **Which constellations count as major?** The 12 zodiac signs, Ptolemy's 48 (most are Greek myths), or a shortlist of about 20 of the best-known Greek ones.
- **Type matchups.** How Astral fits the type chart.
- **How they appear.** For example only at night, at observatories or high peaks, or as a star-chart side quest.
- **The engine cost.** A new type touches the type chart, type icons, move data and the Pokédex, so it is an engine change for the main session.

Map and encounter notes for whoever builds the areas:
- The Spring of Kallirhoe drains into Echo's sea caves.
- Relic Copper must be obtainable somewhere for Charonaut to evolve.
- Victory Road's wild levels should stay under 40, or the wild eagle, north-wind and ice lines will evolve on their first level-up.
- The Hydra's line is named from Lerna, though it lives at Lake Stymphalia as the plan says.

ROM budget notes for whoever implements the dex. These come from the main session's inventory (`design/art/INVENTORY.md` on main), measured from `pokeemerald.map` on 2026-11-14:
- Pokémon cries take 9.4 MB (35% of the ROM), and species art and data take 5.9 MB (22%). The ROM is about 80% full, with about 6.3 MB free. Cutting Hoenn-only systems frees only about 2.2 MB more.
- Under D5 (a), removing the vanilla species Aethos doesn't use is the single biggest space lever, worth several times all the other cuts combined. Plan the implementation around two questions:
  - Which vanilla species stay, if any. The post-game national dex is the main reason to keep some.
  - How the new species' cries are made. Full-length cries are the expensive part, so the choice is between new short cries and reused, pitch-shifted vanilla cries.
- The dex's own sprites, at about 152 species, should come to roughly 1.2–1.5 MB.
- 2026-11-14: The user said: "we dont have a specific ROM MB cap because this is just playing on the laptop". There's no physical cartridge to fit. The 32 MB ceiling still applies, though, because it's the GBA's address space for game data (0x08000000–0x09FFFFFF), and emulators such as mGBA reproduce it, so a larger ROM won't load. The notes above stand, with 32 MB as the hard limit.
- 2026-11-14: **Cries are reused.** The user: "just reuse criess then". Each Aethos species gets an existing vanilla cry, and the engine's cry modes can pitch it up or down. No new cries are recorded.
  - Implementation catch: `sound/cry_tables.inc` and the cry data wrap every cry in its family's `P_FAMILY_*` switch, so switching a vanilla family off also removes its cry. Donor cries must stay compiled in, for example behind their own switch, even when their species are disabled.
  - Picking a donor for each species (a fitting size and temper, and not the same donor twice within a line) is a small job for when the species are implemented.
- 2026-11-14: **Protected from the vanilla-species cut** (see the D1 follow-up above):
  - **Must stay:** the Snivy, Cyndaquil and Piplup lines, with art, cries and data.
  - **May stay:** every generation's starter lines (27 lines), until the user picks a tier for the gods' gifts.
- 2026-11-14: **Eventually every Pokémon can be obtained.** The user: "eventualy you should be able to get every pokemon". This fits D5 (a): the national dex opens in the post-game. It also **supersedes the vanilla-species cut above**: all 1,025 vanilla species stay in the ROM, and the protected-starters list is moot. The budget without that lever:
  - The ROM is about 80% full today (about 6.3 MB free). Cutting Hoenn-only systems adds about 2.2 MB, so all of Ichor's new content shares about 8.5 MB.
  - The Aethos dex is about 1.2–1.5 MB of sprites and data. Its cries are reused, so they cost almost nothing. That leaves roughly 7 MB for maps, tilesets, music, trainer art and the Astral constellations.
  - Levers that keep every species, if space gets tight:
    - Share one cry across each Mega Evolution (`P_MODIFIED_MEGA_CRIES`, about 3% of the ROM, roughly 1 MB).
    - Trim alternate forms that aren't separate species.
    - Watch the build's memory line after each asset batch.
- 2026-11-14: **Mega Evolutions reuse their base form's cry**, which frees about 1 MB. The user: "Give each Mega Evolution the same cry as its base form, which frees about 1 MB." It's an engine config change for the main session to make (the dex branch doesn't edit `include/`). In `include/config/pokemon.h`:
  - `#define P_MODIFIED_MEGA_CRIES FALSE` drops the separate Mega cry samples.
  - `#define P_MODIFIED_MEGA_CRY_MODE CRY_MODE_NORMAL` plays the base cry unchanged, which is what the user asked for. The default, `CRY_MODE_HIGH_PITCH`, plays it pitched up instead, also at no cost.
- 2026-11-14: **Checked against the whole-game level curve** (`design/BALANCE.md` on main).
  - **Fits:** everything through Arkadia. The starters evolve at 16 and then 34–36, and the other main finals at 30–36, inside the curve's Laurels 4–6 window (levels 30–43).
  - **Static encounters raised to fit:** the Fates to level 60, matching the Lord of Time they're freed after, and Ichorin to 70, with the other post-game legendaries.
  - **Conflicts reported to the main session.** From Astyra on, lines first met in an area evolve below that area's wild band:
    - Obolorn (30) in Astyra (30–36)
    - Kaminoo (33) in Kaldera (34–40)
    - Kymbash (35), Monophant (39) and Sepidart (39) in Knossa (42–48)
    - Chalkip (35) and Sporadon (40) in Lakonia (46–50)
    - Pelython (36), Pyrapod (34) and Hymnet (35) in Delphoi (48–52)
    - Aetling (40), Kryopuff (40) and Pagoshard (42) on the Ascent (52–58)
    - Elegull (42) in the post-game (55–70)
  - **Decided (2026-11-14, by the main session, now in `design/BALANCE.md`): keep the evolution levels.** From Astyra on, late areas' wild tables carry the evolved forms at the band's levels. First stages appear only in rare lower-level spots, in swarms or omens, or by breeding. Lernip is the exception: a rare rain-only hunt at Lake Stymphalia at about level 30. The species' habitat text follows this.
  - **Superseded:** the earlier "keep Victory Road under 40" note above.
  - **Habitats rewritten to the ruling (2026-11-14), 18 species.**
    - Late areas now carry the evolved forms at band levels. First stages appear rarely at lower levels, in special spots or omens. Lernip is the exception: rain-only, levels 28–30.
    - The fossil lines (Monophant, Sepidart) stay revive-only, at level 35, so the fossil choice still means something.
    - Lines at the edge of their band (Glaukoin, Telpup, Kapnub) are capped instead of reworked.
    - The species YAML habitats are now the source of truth. `plan.yaml`'s one-line habitats are older summaries.
    - For the main session:
      - New omen entries for SYSTEMS.md §6: Sporadon (swarm), Hymnet (rare visitor), Kryopuff (weather).
      - New small map spots: the paupers' graves (Astyra), the warm hollow (Kaldera), the cradle shrine (Knossa), the reed-bed nests (Lakonia), the oldest altar (Delphoi), the ice-cave side grotto (the Ascent), the Sirens' cliff nests (post-game).
      - Aetarch, the Archon's ace, is now uncommon wild on the Ascent.
