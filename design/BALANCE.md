# Ichor balance: the level curve

The single source for levels across the whole game. Every script, encounter table and trainer party takes its levels from here. When a stage's content is written, record its actual numbers in this table.

**The principle (user, 2026-11-14):** levels rise steadily through the game. The post-game is higher than the League, and the Oikoumene higher still.

## The curve (Hero difficulty)

| Stage | Wild | Route trainers | Boss (ace) | Notes |
|---|---|---|---|---|
| **Kalliste** (slice, Laurel 1) | 2–9 | 3–11 | Ione 12–14 | Built. Kleon Lv 5 |
| **Emporion** (Laurel 2) | 9–16 | 12–18 | Kerykos 18–20 | Act I. The crossing and the first mainland routes |
| **Eleusa** (Laurel 3) | 15–22 | 18–24 | Chloe 24–26 | The sanctum theft; Kleon ~23 |
| **Thyrsa** (Laurel 4) | 21–28 | 24–30 | Thespis 30–32 | Act II. The Dionysia |
| **Arkadia** (Laurel 5) | 26–33 | 30–35 | Kallisto 35–37 | Kleon joins the Titans |
| **Astyra** (midpoint) | 30–36 | 33–38 | Kleon 38–40 | The Akropolis double battle |
| **Salt Well** (Conch quest) | 36–39 | 36–38 | — | Two floors after the Akropolis raid, SYSTEMS §1 |
| **Kaldera** (Laurel 6) | 34–40 | 37–42 | Talos 41–43; Hyperion 41–44 | The low point |
| **Kythera** (Laurel 7) | 38–45 | 42–47 | Galatea 46–48 | Act III |
| **Knossa**, the Labyrinth | 42–48 | 45–50 | Hyperion 50–53, Kleon 51–54 | LABYRINTH.md's levels |
| **Lakonia** | 46–50 | 49–53 | Rhea 52–54 | |
| **Delphoi** (Laurel 8) | 48–52 | 52–56 | Phemonoe 55–57 | |
| **The Loom, the Frozen Hour, the Stair of Hours** | — | 55–58 | Kronos 58–60, the Lord of Time 60 | The climax |
| **The Ascent and the Pantheon** | 54–64 | 59–69 | Pantheon 66–72, the Archon 71–75 | The League; raised for team-wide EXP (2026-11-17) |
| **Aethos post-game**: the Labors, Katabasis, the Olympiad, Atlantis | 55–70 | 65–75 | 70–80 | Rematches scale here |
| **The Oikoumene**, the second map | 60–80 | 70–85 | Legendaries 70–80; the strongest up to 90–100 | Every non-Aethos National Dex Pokémon lives here |

## Rules

- **Wild levels** at a stage start near the previous boss's ace minus 4 and rise along the stage's routes. A route's level band is never wider than 5.
- **Evolved forms in late areas** (director's ruling, 2026-11-14, with the dex team): from Astyra on, a line whose evolution level sits below the area's wild band appears in the wild as its evolved form, at the band's levels. Its first stage shows up only in rare lower-level spots, in swarms or omens, or by breeding, the way Victory Road works. The rare exception is the pseudo-legendary Lernip (evolving at 30 and 55): a rain-only hunt at Lake Stymphalia at about level 30, in the tradition of Bagon. The full list is in `design/dex/DECISIONS.md` (07dd37483b).
- **No early evolved forms in the wild** (director's ruling, 2026-11-14, from Phase 2's open question 22). A wild Pokémon never appears in an evolved form earlier than its evolution level allows. A few early evolved forms may appear only as one-off story rewards: augury statics such as Harpelle at 17 and Korantha or Persenyx at 22, and trainer teams such as Aiakides's Hoplomex on Aegina.
- **Evolution timing:** the Aethos dex sets evolution levels so the main fully-evolved forms arrive around Laurels 4–6. The dex team owns this; keep this curve and their levels in step.
- **Implemented return loop:** Route 13 uses wild 30–32 and trainers 33–35;
  Route 14 uses wild 31–33 and trainers 34–36. The rebuild (design/maps/Nemea.md)
  adds Nemea's wild 31–33, the Tretos's 32–34, and four trainers at 35–37. These begin the Astyra stage
  after the Moon Laurel. Their evolved encounters respect evolution timing;
  assisted native travel is not natural-level balance approval.
- **Implemented capital approach:** Route 15 uses wild 32–34 and trainers 35–37;
  Route 16 uses wild 34–36 and trainers 36–38. The distribution pass (design/DISTRIBUTION.md, 2026-11-18) took the
  starters out of the wild: Route 16 now has Sophowl and Ophidrop in their slots;
  Daphnyad stays in both roads' late trainer parties. These are implemented bands, not
  natural-level approval.
  The Sacred Way rebuild (sacredway.py, 2026-11-18) adds nine trainers on the same
  bands: Route 15's five at 35-37, Route 16's four at 37-38.
- **Spartan difficulty:** the level cap at each stage is that stage's boss ace. Bosses use competitive sets.
- **Mortal difficulty:** bosses at −3 levels.
- **Current connected implementation:** Mortal variants cover Ione, Kerykos,
  both Chloe parties, Thespis, Kallisto, all three Akropolis Kleon parties and
  Akropolis Rhea, Kaldera Talos, Kaldera Hyperion and Galatea, retaining Hero's species
  and moves at three levels lower.
  Spartan uses those species and levels with trained EV spreads, natures,
  held items and smart AI. Its EXP/candy caps are 14, 20, 26, 32 and 37, advancing when
  each Laurel is won; after Laurel 5 the next cap is Astyra's 40, followed by
  Kaldera's 43 after the saved Akropolis raid victory, Hyperion's 44 after
  Laurel 6, Kythera's 48 after the saved third-fragment aftermath, and Knossa's
  Hyperion cap of 53 after Laurel 7. Extend the
  milestone mapping as later chapters are connected. Hero's existing parties
  and uncapped EXP are unchanged. These integrations are not natural-level
  balance approval.
- **Implemented Akropolis:** the first Titanborn pair uses 36–37 and the second
  37–38. Alethea's partner Plouteras/Harpelle are 38/37. Kleon's three
  starter-counter variants use 38, 38, 39, 40; Rhea uses 38, 39, 40.
  These parties and their difficulty variants are implemented, not
  natural-level pacing approval.
- **Implemented League** (design/LEAGUE.md, the endgame upgrade of 2026-11-17/18,
  raised for always-on team-wide EXP): the Ascent's wild bands climb with the
  mountain, 54–58 (1F), 55–59 (2F), 57–61 (the Icefall), 58–62 (the Glacier),
  59–63 (the Deep), 60–63 (the Crystal Vault) and 60–64 (3F); its 23 trainers run
  59–67 (held items and the smart AI from the Icefall up), the gatekeeper
  Polydamas 67–69. The Pantheon's teams run 66–72 (aces 69, 70, 71, 72); the
  Archon has 71/72/72/73/73/75. All six bosses (with the gatekeeper) have Mortal
  (−3, no items) and Spartan (full spreads, natures, smart AI) variants, and Hero
  bosses carry natures, held items and lighter spreads. These are implemented
  parties, not natural-level balance approval.
- **Salt Well quest band:** its two floors use Water-type encounters at
  36–39 (SYSTEMS §1), following the raid rather than the earlier capital road.
  The stranded Glaukos has one 36; optional grotto trainers use 37–38.
- **Implemented Kaldera:** harbor encounters are 32–36 (the distribution pass, 2026-11-18:
  rare young Kaminoo at 32 and Pyrapod at 32–33, BALANCE's lower-level spots, so both
  lines are caught before they evolve) and forge encounters
  36–39. Three smiths use 38–40; three Titanborn use 40–42. Talos has
  41/41/42/43 and eruption Hyperion has 41/42/43/44, matching STORY's
  approximately level-44 ace. Both bosses have explicit four-move sets and
  Mortal/Spartan variants; Pyrapod's Spartan training is special, not physical.
  These are implemented parties, not natural-level balance approval.
- **Aethos's trainers use Aethos's Pokémon** (user, 2026-11-14). Before the post-game, trainer parties and wild tables draw on the 152-species Aethos dex for the most part. A non-Aethos species is the exception and needs a reason: a story gift such as the theoxenia starters, a foreigner's signature Pokémon, or a deliberate rarity. The National Dex's other species belong to the Oikoumene and the post-game.
- **Implemented Galatea:** Hero uses 46/46/47/47/48, Mortal uses
  43/43/44/44/45, and Spartan retains Hero's levels with trained EVs, natures,
  held items and smart AI. Himerow remains itemless for Acrobatics. These
  concrete teams and the post-Laurel cap are not natural-level approval.
- **Gifts:** theoxenia starters follow SYSTEMS.md §10's levels, which must sit inside the band of the stage where they're given.
- **Act I amphora returns:** explicit shelf restoration unlocks the one-off
  Cairnolith Lv20 at Kronion's altar (night, Sand Force, Hard Stone), Raknit
  Lv20 in the Hollow's web chamber (Defiant), and Persenyx Lv22 in Eleusa's
  fields (dusk). These are the scripted return prizes from Phase 2, not
  additions to Kalliste's early wild band. Cairnolith and Persenyx are deliberate
  early-evolved static exceptions, like the fields' existing augury rewards.
- **The Erymanthian Preserve** (the Safari Zone beside Arkadia, design/maps/ErymanthosPreserve.md):
  wild 28–32 in its four story areas, Arkadia's stage; the post-game Boar's Thicket 58–62.
  Lernip's catch point is its river's 1% surf and Super Rod slot at 29 (the "about level
  30" above) until Lake Stymphalia's rain hunt is built; the lake itself sits at 46–50.
- **Rematches** (the Olympiad's Arena, the Hierophants) scale to the Aethos post-game row.
