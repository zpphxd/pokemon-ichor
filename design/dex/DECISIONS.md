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
| D2 | Kronos and the Moirai replace Dialga and the lake trio in the story | Yes | Open |
| D3 | Add Kairos as a post-game legendary at Olympia | Yes | Open |
| D4 | Two mythicals, Hope and Ichor | Yes | Changed: "mythicals should be like a zeus pokemon, a posiden pokemon, and a hades pokemon. as like regis giant types ... with good names." Three Regi-style colossi, the cult statues of the brothers who drew lots for the world, replace Hope: Olympanax (Zeus, Electric), Pontanax (Poseidon, Water) and Nekranax (Hades, Ghost). Ichorin, the title Pokémon, stays as a fourth mythical at #152: "Keep it as #152". The dex is 152. |
| D5 | How the regional dex mixes with the existing 1,025 species | (a) Aethos-only through the League | (b) mixed: "while we add in the other pokemon into the region too". Then changed to (a): "(a). It makes Aethos feel like a real new region and keeps the bible's post-game promise. lets switch it to this". Only Aethos's own species appear until the League is beaten; existing species arrive in the post-game. |
| D6 | Post-game Labors use regional species where one exists | Yes | Open |

D2, D3 and D6 don't block Gate 2. The entries for those species are written either way, and the open questions are about where they go in the story.

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
