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
| **Kaldera** (Laurel 6) | 34–40 | 37–42 | Talos 41–43 | The low point |
| **Kythera** (Laurel 7) | 38–45 | 42–47 | Galatea 46–48 | Act III |
| **Knossa**, the Labyrinth | 42–48 | 45–50 | Hyperion 50–53, Kleon 51–54 | LABYRINTH.md's levels |
| **Lakonia** | 46–50 | 49–53 | Rhea 52–54 | |
| **Delphoi** (Laurel 8) | 48–52 | 52–56 | Phemonoe 55–57 | |
| **The Loom, the Frozen Hour, the Stair of Hours** | — | 55–58 | Kronos 58–60, the Lord of Time 60 | The climax |
| **The Ascent and the Pantheon** | 52–58 | 56–62 | Pantheon 60–64, the Archon 65–67 | The League |
| **Aethos post-game**: the Labors, Katabasis, the Olympiad, Atlantis | 55–70 | 65–75 | 70–80 | Rematches scale here |
| **The Oikoumene**, the second map | 60–80 | 70–85 | Legendaries 70–80; the strongest up to 90–100 | Every non-Aethos National Dex Pokémon lives here |

## Rules

- **Wild levels** at a stage start near the previous boss's ace minus 4 and rise along the stage's routes. A route's level band is never wider than 5.
- **Evolved forms in late areas** (director's ruling, 2026-11-14, with the dex team): from Astyra on, a line whose evolution level sits below the area's wild band appears in the wild as its evolved form, at the band's levels. Its first stage shows up only in rare lower-level spots, in swarms or omens, or by breeding, the way Victory Road works. The rare exception is the pseudo-legendary Lernip (evolving at 30 and 55): a rain-only hunt at Lake Stymphalia at about level 30, in the tradition of Bagon. The full list is in `design/dex/DECISIONS.md` (07dd37483b).
- **Evolution timing:** the Aethos dex sets evolution levels so the main fully-evolved forms arrive around Laurels 4–6. The dex team owns this; keep this curve and their levels in step.
- **Spartan difficulty:** the level cap at each stage is that stage's boss ace. Bosses use competitive sets.
- **Mortal difficulty:** bosses at −3 levels.
- **Gifts:** theoxenia starters follow SYSTEMS.md §10's levels, which must sit inside the band of the stage where they're given.
- **Rematches** (the Olympiad's Arena, the Hierophants) scale to the Aethos post-game row.
