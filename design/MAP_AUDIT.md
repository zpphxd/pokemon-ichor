# Map audit: the built maps against the route standard

Every route, town and dungeon built so far, measured against MAP_DESIGN.md §8 on 2026-11-14. The tables come from:

```bash
tools/ichor/map_audit.py --ref <branch> --all-ichor --kinds route,town,dungeon --markdown --warn-only
```

The branches move quickly, so each section names the commit it measured. Run the same command to refresh a section.

- **FAIL** misses a hard minimum. **WARN** needs a look: a soft minimum or a heuristic.
- Structural warnings (reach, mixed, onsolid, edge, warp) are counted, not listed. Run the audit on a map without `--markdown` to see them.
- In the Wild column, the letters are the tables' times (Morning, Day, Evening, Night) and the numbers are each table's species. "land MN (11/12 spp)" is a morning table of 11 species and a night table of 12.
- The four slice maps come from main and appear on every branch: Elaia Village, Route 1, Kronion Hill and Akti Town.

## What's systematically weak

1. **Trainers are short on every route, on every branch.** None of the 20 distinct routes meets its trainer minimum.
   - Main's Route 1 is closest, with 5 of 6.
   - Act II's three real routes have 11 trainers between them on 37 screens: 0.3 a screen, against 0.6 required.
   - Act III's Route 22 and Route 23 have 2–3 trainers each on 16 screens of sea, against 6 required.
2. **Hidden items are missing from new work.**
   - No new map on act2 or act3 has a single hidden item: 0 across 31 routes, towns and dungeons.
   - Act I's Aegina routes have none either.
   - Act I's towns are the exception, with 2–3 each.
   - Elaia Village has 1 of 2.
3. **No dungeon has a hidden item, and most have no items or trainers.**
   - The Eleusa Sanctum, Trophonios's Cave and the Cave of Maia are empty: no items, no trainers, no hidden items.
   - Only Antiope's Cave and the Kythera Echo Caves meet 2 items a floor.
4. **Grass is thin on every new route.** Only Route 1, and the act2 placeholders copied from it, reach 15 cells a screen.
   - The real new routes have 4–13: Aphaia Road 6; Route 6 5, Kithairon 7, Kronia Grounds 9; Foam Road 4, Neraida Falls 8, Kallirhoe 13.
   - Their forced grass is short as well. Route 6 forces 5 cells, Kithairon 4, Kronia 7 and Foam Road 7, against 8. Kallirhoe forces 0.
5. **Item balls are short**, mostly on act2 and act3.
   - Act2: 8 of 11 routes and 6 of 10 towns.
   - Act3: 7 of 8 routes, and two of three Kythera towns have none.
6. **Water without water tables.**
   - Route 1's stream (43 reachable water cells) has no surf or fishing table, on every branch.
   - The same goes for Aegina's three outdoor maps (135–277 cells) and Kallirhoe's spring (83).
7. **Night tables are in; day tables aren't.**
   - Every map with grass has `_Morning` and `_Night` tables except Kronion Hill, which has no `_Night`.
   - No map anywhere has a `_Day` table. That's a note only, since day falls back to morning.
8. **Late tables are too narrow** for the late band's 7 species.
   - Route 23 has 5 species, and the night tables at Kallirhoe and Neraida Falls have 6.
   - Several fishing tables have 3 species against 4: Myrtoan Sea, the Echo Caves, Route 11 and Arkadia. Neraida Falls' surf table has 2.
9. **Placeholders are standing in as built maps on act2.**
   - Five routes are byte-for-byte copies of Route 1 with no connections, trainers, items or signs: Routes 8, 9, 11 and 12, and the Arkadia Cypress Wood. They pass the grass check only because Route 1 does.
   - Seven maps are copies of Akti Town: Lebadeia, Kirrha, Aigion, Styx Falls, Arkadia, the Pool of Mnemosyne and the Gulf ferry's deck.
   - Trophonios's two floors and the Cave of Maia copy Antiope's Cave.
   - 24 act2 interiors fail "every interior is unique" (§2). Sixteen houses, inns and halls in the new towns are copies of the Akti fisher's house. Arkadia's Asclepeion, Agora and Temple of Artemis copy Akti's, and the Gulf ferry's deck copies Akti Town. Akti's own four rooms fail alongside their copies.
   - On act1, Eleusa's six interiors and three sanctum floors are copies of the Akti fisher's house too, and nobody lives in any of them. That fails "every house a home" six times, and "every interior is unique" seven.
   - Main and act3 have no copied cells.
10. **Seams need a look.** Open cells walk into a wall across a connection in two places:
    - Act2: Eleutherai, Kithairon and Kronia Grounds. Kronia's top edge is open for 40 cells but meets Thyrsa's wall everywhere except a 4-cell gap.
    - Act3: Foam Road, Paphia and Neraida Falls.
    - Emerald does this too, so these are warnings, but check that each seam reads as a wall.
11. **Classing.** Some maps need an `"ichor_kind"` decision (MAP_DESIGN §8.6):
    - Kronion Hill is a route by its map type, and fails most route minimums as one. Either bring it up to the standard or class it as a side area: give it `"ichor_kind": "dungeon"` and its dungeon minimums.
    - Aegina's Temple of Aphaia and Mount Oros class as sea routes, being small and mostly water. Those are probably set-piece spots that want a kind of their own.

What already meets the standard: **Akti Town** on every branch, and **Emporion Harbor** on act1. Route 1 is three fixes away: one more trainer, and a surf and a fishing table for its stream.

## `main`, at `84f607e7b2`

### Routes

| Map | Stage | Screens | Grass/screen | Forced grass | Trainers | Items | Hidden | Signs | Wild | Fails | Warnings |
|---|---|---|---|---|---|---|---|---|---|---|---|
| KallisteRoute1_KronionHill | Kalliste | 9.9 | 3 | – | 0 | 1 | 2 | 7 | land M (11 spp), Lv 5–7 | 4 | 5 |
| KallisteRoute1 | Kalliste | 12.8 | 18 | 8 | 5 | 3 | 3 | 3 | land MN (11/12 spp), Lv 3–6 | 3 | 2 |

Route shortfalls, worst first:

- **KallisteRoute1_KronionHill** (4 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL grass: 3 cells per screen < 15 (29 cells in 9.9 screens; 149 needed)
  - FAIL trainers: 0 < 5 (early route of 9.9 screens)
  - FAIL item balls: 1 < 2
  - FAIL wild: no _Night land table
  - WARN forced grass: can't measure, fewer than two ends a walker can reach each other from (1 end(s))
- **KallisteRoute1** (2 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL trainers: 5 < 6 (early route of 12.8 screens)
  - FAIL wild: 43 reachable water cells but no surf table
  - FAIL wild: 43 reachable water cells but no fishing table

### Towns

| Map | Stage | Screens | Grass/screen | Forced grass | Trainers | Items | Hidden | Signs | Wild | Fails | Warnings |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ElaiaVillage | Kalliste | 7.6 | 0 | – | 0 | 1 | 1 | 22 | none | 1 | 2 |
| AktiTown | Kalliste | 5.2 | 0 | – | 0 | 2 | 3 | 9 | surf M (5 spp), fish M (9 spp) | 0 | 3 |

Town shortfalls, worst first:

- **ElaiaVillage** (2 structural warning(s))
  - FAIL hidden items: 1 < 2
- **AktiTown**: meets the standard (3 structural warning(s))

4 map(s): 8 hard shortfall(s) in 3 map(s), 12 warning(s)

## `claude/world-act1-6d11b7`, at `95ce72bd71`

### Routes

| Map | Stage | Screens | Grass/screen | Forced grass | Trainers | Items | Hidden | Signs | Wild | Fails | Warnings |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AeginaAphaiaRoad | Emporion | 6.4 | 6 | 3 | 0 | 2 | 0 | 6 | land MN (10/8 spp), Lv 12–16 | 5 | 1 |
| AeginaMountOros (sea) | Emporion | 1.7 | 6 | – | 0 | 1 | 0 | 1 | land MN (10/8 spp), Lv 12–16 | 5 | 1 |
| AeginaTempleOfAphaia (sea) | Emporion | 3.2 | 2 | – | 0 | 1 | 0 | 2 | land MN (10/8 spp), Lv 12–16 | 5 | 1 |
| KallisteRoute1_KronionHill | Kalliste | 9.9 | 3 | – | 0 | 1 | 2 | 7 | land M (11 spp), Lv 5–7 | 4 | 5 |
| KallisteRoute1 | Kalliste | 12.8 | 18 | 8 | 5 | 3 | 3 | 3 | land MN (11/12 spp), Lv 3–6 | 3 | 2 |

Route shortfalls, worst first:

- **AeginaAphaiaRoad** (notes: no _Day land table (day falls back to morning))
  - FAIL grass: 6 cells per screen < 15 (39 cells in 6.4 screens; 96 needed)
  - FAIL trainers: 0 < 3 (early route of 6.4 screens)
  - FAIL hidden items: 0 < 2
  - FAIL wild: 277 reachable water cells but no surf table
  - FAIL wild: 277 reachable water cells but no fishing table
  - WARN set piece: none found (no scene trigger, gift, trade or berry tree); check there is one
- **AeginaMountOros** (notes: no _Day land table (day falls back to morning))
  - FAIL trainers: 0 < 5 (sea route of 1.7 screens)
  - FAIL item balls: 1 < 2
  - FAIL hidden items: 0 < 2
  - FAIL wild: 135 reachable water cells but no surf table
  - FAIL wild: 135 reachable water cells but no fishing table
  - WARN set piece: none found (no scene trigger, gift, trade or berry tree); check there is one
- **AeginaTempleOfAphaia** (notes: no _Day land table (day falls back to morning))
  - FAIL trainers: 0 < 5 (sea route of 3.2 screens)
  - FAIL item balls: 1 < 2
  - FAIL hidden items: 0 < 2
  - FAIL wild: 179 reachable water cells but no surf table
  - FAIL wild: 179 reachable water cells but no fishing table
  - WARN set piece: none found (no scene trigger, gift, trade or berry tree); check there is one
- **KallisteRoute1_KronionHill** (4 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL grass: 3 cells per screen < 15 (29 cells in 9.9 screens; 149 needed)
  - FAIL trainers: 0 < 5 (early route of 9.9 screens)
  - FAIL item balls: 1 < 2
  - FAIL wild: no _Night land table
  - WARN forced grass: can't measure, fewer than two ends a walker can reach each other from (1 end(s))
- **KallisteRoute1** (2 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL trainers: 5 < 6 (early route of 12.8 screens)
  - FAIL wild: 43 reachable water cells but no surf table
  - FAIL wild: 43 reachable water cells but no fishing table

### Towns

| Map | Stage | Screens | Grass/screen | Forced grass | Trainers | Items | Hidden | Signs | Wild | Fails | Warnings |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EleusaVillage | Eleusa | 13.3 | 14 | – | 0 | 2 | 3 | 11 | land MN (11/8 spp), Lv 19–22 | 6 | 6 |
| AeginaTown | Emporion | 4.8 | 0 | – | 0 | 0 | 2 | 6 | surf M (4 spp), fish M (4 spp) | 1 | 0 |
| ElaiaVillage | Kalliste | 7.6 | 0 | – | 0 | 1 | 1 | 22 | none | 1 | 3 |
| AktiTown | Kalliste | 5.2 | 0 | – | 0 | 2 | 3 | 9 | surf M (5 spp), fish M (9 spp) | 0 | 3 |
| EmporionCity | Emporion | 14.7 | 0 | – | 0 | 2 | 2 | 22 | none | 0 | 4 |
| EmporionHarbor | Emporion | 8.3 | 0 | – | 0 | 1 | 2 | 9 | surf M (4 spp), fish M (4 spp) | 0 | 2 |

Town shortfalls, worst first:

- **EleusaVillage** (notes: no _Day land table (day falls back to morning))
  - FAIL every house a home: nobody lives in EleusaVillage_Asclepeion
  - FAIL every house a home: nobody lives in EleusaVillage_Agora
  - FAIL every house a home: nobody lives in EleusaVillage_HouseOfKeleos
  - FAIL every house a home: nobody lives in EleusaVillage_GranaryHouse
  - FAIL every house a home: nobody lives in EleusaVillage_PoetsHouse
  - FAIL every house a home: nobody lives in EleusaVillage_Farmhouse
  - WARN every house a home: nothing found happening in EleusaVillage_HouseOfKeleos (no gift, trade, battle, heal or item)
  - WARN every house a home: nothing found happening in EleusaVillage_GranaryHouse (no gift, trade, battle, heal or item)
  - WARN every house a home: nothing found happening in EleusaVillage_PoetsHouse (no gift, trade, battle, heal or item)
  - WARN every house a home: nothing found happening in EleusaVillage_Farmhouse (no gift, trade, battle, heal or item)
  - WARN dead end: 107 cells, 27 deep, ending at (18, 6), entered at (12, 18), holds nothing
  - WARN dead end: 9 cells, 6 deep, ending at (18, 16), entered at (17, 19), holds nothing
- **ElaiaVillage** (3 structural warning(s))
  - FAIL hidden items: 1 < 2
- **AeginaTown**
  - FAIL item balls: 0 < 1
- **EmporionCity** (2 structural warning(s))
  - WARN dead end: 7 cells, 7 deep, ending at (0, 15), entered at (6, 15), holds nothing
  - WARN dead end: 7 cells, 5 deep, ending at (5, 26), entered at (7, 27), holds nothing
- **AktiTown**: meets the standard (3 structural warning(s))
- **EmporionHarbor**: meets the standard (2 structural warning(s))

### Dungeons

| Map | Stage | Screens | Grass/screen | Forced grass | Trainers | Items | Hidden | Signs | Wild | Fails | Warnings |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EleusaSanctum_B1F | Eleusa | 0.5 | 0 | – | 0 | 0 | 0 | 0 | none | 1 | 1 |
| EleusaSanctum_B2F | Eleusa | 0.5 | 0 | – | 0 | 0 | 0 | 0 | none | 1 | 1 |
| EleusaSanctum_B3F | Eleusa | 0.5 | 0 | – | 0 | 0 | 0 | 0 | none | 1 | 1 |

Dungeon shortfalls, worst first:

- **EleusaSanctum_B1F**
  - FAIL items on this floor: 0 (visible and hidden) < 2
  - WARN layout: the same cells as AktiTown_FishersHouse, EleusaVillage_Asclepeion, EleusaVillage_Agora and 6 more (one of them is a placeholder copy)
- **EleusaSanctum_B2F**
  - FAIL items on this floor: 0 (visible and hidden) < 2
  - WARN layout: the same cells as AktiTown_FishersHouse, EleusaVillage_Asclepeion, EleusaVillage_Agora and 6 more (one of them is a placeholder copy)
- **EleusaSanctum_B3F**
  - FAIL items on this floor: 0 (visible and hidden) < 2
  - WARN layout: the same cells as AktiTown_FishersHouse, EleusaVillage_Asclepeion, EleusaVillage_Agora and 6 more (one of them is a placeholder copy)

Whole dungeons:

- **EleusaSanctum** (3 floor(s))
  - FAIL trainers in the whole dungeon: 0 < 3
  - FAIL hidden items in the whole dungeon: 0 < 2
  - WARN midpoint rest: no healer on any floor; check for a spring or a shortcut back

14 map(s): 35 hard shortfall(s) in 11 map(s), 31 warning(s)

## `claude/world-act2-0a92e7`, at `0204dada04`

### Routes

| Map | Stage | Screens | Grass/screen | Forced grass | Trainers | Items | Hidden | Signs | Wild | Fails | Warnings |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Route7_KroniaGrounds | Thyrsa | 11.7 | 9 | 7 | 2 | 2 | 0 | 9 | land MN (12/8 spp), surf M (5 spp), fish M (4 spp), Lv 23–27 | 5 | 4 |
| KallisteRoute1_KronionHill | Kalliste | 9.9 | 3 | – | 0 | 1 | 2 | 7 | land M (11 spp), Lv 5–7 | 4 | 5 |
| MtKithairon | Thyrsa | 14.9 | 7 | 4 | 5 | 4 | 0 | 12 | land MN (10/9 spp), Lv 22–26 | 4 | 3 |
| PoolOfMnemosyne | Arkadia | 5.2 | 0 | – | 0 | 0 | 0 | 0 | land MN (5/7 spp), Lv 31–33 | 4 | 6 |
| Route11_KrathisGorge | Arkadia | 12.8 | 18 | – | 0 | 0 | 0 | 0 | land MN (6/6 spp), fish M (3 spp), Lv 29–32 | 4 | 5 |
| Route6_EleutheraiRoad | Thyrsa | 10.5 | 5 | 5 | 4 | 3 | 0 | 7 | land MN (11/10 spp), Lv 21–24 | 4 | 0 |
| Arkadia_CypressWood | Arkadia | 12.8 | 18 | – | 0 | 0 | 0 | 0 | land MN (6/7 spp), Lv 30–33 | 3 | 5 |
| KallisteRoute1 | Kalliste | 12.8 | 18 | 8 | 5 | 3 | 3 | 3 | land MN (11/12 spp), Lv 3–6 | 3 | 3 |
| Route12_CypressRoad | Arkadia | 12.8 | 18 | – | 0 | 0 | 0 | 0 | land MN (7/8 spp), Lv 30–33 | 3 | 5 |
| Route8_Kopais | Arkadia | 12.8 | 18 | – | 0 | 0 | 0 | 0 | land MN (10/9 spp), surf M (4 spp), fish M (4 spp), Lv 27–30 | 3 | 5 |
| Route9_Schiste | Arkadia | 12.8 | 18 | – | 0 | 0 | 0 | 0 | land MN (9/8 spp), Lv 28–31 | 3 | 5 |

Route shortfalls, worst first:

- **Route7_KroniaGrounds** (4 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL grass: 9 cells per screen < 15 (104 cells in 11.7 screens; 176 needed)
  - FAIL forced grass: the ends can be walked between crossing 7 grass cell(s) < 8 (down (MT_KITHAIRON) to up (THYRSA_CITY): 7, up (THYRSA_CITY) to down (MT_KITHAIRON): 7)
  - FAIL trainers: 2 < 7 (middle route of 11.7 screens)
  - FAIL item balls: 2 < 3
  - FAIL hidden items: 0 < 3
- **PoolOfMnemosyne** (3 structural warning(s))
  - FAIL grass: 0 cells per screen < 15 (0 cells in 5.2 screens; 78 needed)
  - FAIL trainers: 0 < 6 (middle route of 5.2 screens)
  - FAIL item balls: 0 < 3
  - FAIL hidden items: 0 < 3
  - WARN layout: the same cells as AktiTown, Lebadeia, Kirrha and 4 more (one of them is a placeholder copy)
  - WARN forced grass: can't measure, fewer than two ends a walker can reach each other from (0 end(s))
  - WARN set piece: none found (no scene trigger, gift, trade or berry tree); check there is one
- **KallisteRoute1_KronionHill** (4 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL grass: 3 cells per screen < 15 (29 cells in 9.9 screens; 149 needed)
  - FAIL trainers: 0 < 5 (early route of 9.9 screens)
  - FAIL item balls: 1 < 2
  - FAIL wild: no _Night land table
  - WARN forced grass: can't measure, fewer than two ends a walker can reach each other from (1 end(s))
- **Route11_KrathisGorge** (2 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL trainers: 0 < 8 (middle route of 12.8 screens)
  - FAIL item balls: 0 < 3
  - FAIL hidden items: 0 < 3
  - FAIL wild: the Morning fishing table has 3 species < 4
  - WARN layout: the same cells as KallisteRoute1, Route8_Kopais, Route9_Schiste and 2 more (one of them is a placeholder copy)
  - WARN forced grass: can't measure, fewer than two ends a walker can reach each other from (0 end(s))
  - WARN set piece: none found (no scene trigger, gift, trade or berry tree); check there is one
- **MtKithairon** (2 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL grass: 7 cells per screen < 15 (110 cells in 14.9 screens; 224 needed)
  - FAIL forced grass: the ends can be walked between crossing 4 grass cell(s) < 8 (down (ELEUTHERAI) to up (ROUTE7_KRONIA_GROUNDS): 4, up (ROUTE7_KRONIA_GROUNDS) to down (ELEUTHERAI): 4)
  - FAIL trainers: 5 < 9 (middle route of 14.9 screens)
  - FAIL hidden items: 0 < 3
  - WARN dead end: 10 cells, 6 deep, ending at (14, 2), entered at (19, 1), holds nothing
- **Route6_EleutheraiRoad** (notes: no _Day land table (day falls back to morning))
  - FAIL grass: 5 cells per screen < 15 (56 cells in 10.5 screens; 157 needed)
  - FAIL forced grass: the ends can be walked between crossing 5 grass cell(s) < 8 (up (ELEUTHERAI) to warp to Route6_AntiopesCave: 5, warp to Route6_AntiopesCave to up (ELEUTHERAI): 5)
  - FAIL trainers: 4 < 6 (middle route of 10.5 screens)
  - FAIL hidden items: 0 < 3
- **Arkadia_CypressWood** (2 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL trainers: 0 < 8 (middle route of 12.8 screens)
  - FAIL item balls: 0 < 3
  - FAIL hidden items: 0 < 3
  - WARN layout: the same cells as KallisteRoute1, Route8_Kopais, Route9_Schiste and 2 more (one of them is a placeholder copy)
  - WARN forced grass: can't measure, fewer than two ends a walker can reach each other from (0 end(s))
  - WARN set piece: none found (no scene trigger, gift, trade or berry tree); check there is one
- **Route12_CypressRoad** (2 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL trainers: 0 < 8 (middle route of 12.8 screens)
  - FAIL item balls: 0 < 3
  - FAIL hidden items: 0 < 3
  - WARN layout: the same cells as KallisteRoute1, Route8_Kopais, Route9_Schiste and 2 more (one of them is a placeholder copy)
  - WARN forced grass: can't measure, fewer than two ends a walker can reach each other from (0 end(s))
  - WARN set piece: none found (no scene trigger, gift, trade or berry tree); check there is one
- **Route8_Kopais** (2 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL trainers: 0 < 8 (middle route of 12.8 screens)
  - FAIL item balls: 0 < 3
  - FAIL hidden items: 0 < 3
  - WARN layout: the same cells as KallisteRoute1, Route9_Schiste, Route11_KrathisGorge and 2 more (one of them is a placeholder copy)
  - WARN forced grass: can't measure, fewer than two ends a walker can reach each other from (0 end(s))
  - WARN set piece: none found (no scene trigger, gift, trade or berry tree); check there is one
- **Route9_Schiste** (2 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL trainers: 0 < 8 (middle route of 12.8 screens)
  - FAIL item balls: 0 < 3
  - FAIL hidden items: 0 < 3
  - WARN layout: the same cells as KallisteRoute1, Route8_Kopais, Route11_KrathisGorge and 2 more (one of them is a placeholder copy)
  - WARN forced grass: can't measure, fewer than two ends a walker can reach each other from (0 end(s))
  - WARN set piece: none found (no scene trigger, gift, trade or berry tree); check there is one
- **KallisteRoute1** (2 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL trainers: 5 < 6 (early route of 12.8 screens)
  - FAIL wild: 43 reachable water cells but no surf table
  - FAIL wild: 43 reachable water cells but no fishing table
  - WARN layout: the same cells as Route8_Kopais, Route9_Schiste, Route11_KrathisGorge and 2 more (one of them is a placeholder copy)

### Towns

| Map | Stage | Screens | Grass/screen | Forced grass | Trainers | Items | Hidden | Signs | Wild | Fails | Warnings |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Arkadia | Arkadia | 5.2 | 0 | – | 0 | 0 | 0 | 0 | fish M (3 spp) | 3 | 4 |
| Aigion | Arkadia | 5.2 | 0 | – | 0 | 0 | 0 | 0 | surf M (4 spp), fish M (4 spp) | 2 | 4 |
| Eleutherai | Thyrsa | 5.5 | 0 | – | 0 | 0 | 0 | 5 | none | 2 | 5 |
| Kirrha | Arkadia | 5.2 | 0 | – | 0 | 0 | 0 | 0 | surf M (4 spp), fish M (4 spp) | 2 | 4 |
| Lebadeia | Arkadia | 5.2 | 0 | – | 0 | 0 | 0 | 0 | none | 2 | 4 |
| StyxFalls | Arkadia | 5.2 | 0 | – | 0 | 0 | 0 | 0 | none | 2 | 4 |
| ElaiaVillage | Kalliste | 7.6 | 0 | – | 0 | 1 | 1 | 22 | none | 1 | 2 |
| ThyrsaCity | Thyrsa | 17.9 | 5 | – | 3 | 3 | 0 | 26 | land MN (8/6 spp), Lv 24–28 | 1 | 5 |
| ThyrsaTheater | Thyrsa | 9.1 | 0 | – | 0 | 1 | 0 | 7 | none | 1 | 2 |
| AktiTown | Kalliste | 5.2 | 0 | – | 0 | 2 | 3 | 9 | surf M (5 spp), fish M (9 spp) | 0 | 4 |

Town shortfalls, worst first:

- **Arkadia** (3 structural warning(s))
  - FAIL hidden items: 0 < 2
  - FAIL item balls: 0 < 1
  - FAIL wild: the Morning fishing table has 3 species < 4
  - WARN layout: the same cells as AktiTown, Lebadeia, Kirrha and 4 more (one of them is a placeholder copy)
- **Eleutherai** (5 structural warning(s))
  - FAIL hidden items: 0 < 2
  - FAIL item balls: 0 < 1
- **Aigion** (3 structural warning(s))
  - FAIL hidden items: 0 < 2
  - FAIL item balls: 0 < 1
  - WARN layout: the same cells as AktiTown, Lebadeia, Kirrha and 4 more (one of them is a placeholder copy)
- **Kirrha** (3 structural warning(s))
  - FAIL hidden items: 0 < 2
  - FAIL item balls: 0 < 1
  - WARN layout: the same cells as AktiTown, Lebadeia, GulfFerry_Deck and 4 more (one of them is a placeholder copy)
- **Lebadeia** (3 structural warning(s))
  - FAIL hidden items: 0 < 2
  - FAIL item balls: 0 < 1
  - WARN layout: the same cells as AktiTown, Kirrha, GulfFerry_Deck and 4 more (one of them is a placeholder copy)
- **StyxFalls** (3 structural warning(s))
  - FAIL hidden items: 0 < 2
  - FAIL item balls: 0 < 1
  - WARN layout: the same cells as AktiTown, Lebadeia, Kirrha and 4 more (one of them is a placeholder copy)
- **ThyrsaCity** (4 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL hidden items: 0 < 2
  - WARN dead end: 10 cells, 7 deep, ending at (45, 20), entered at (43, 24), holds nothing
- **ElaiaVillage** (2 structural warning(s))
  - FAIL hidden items: 1 < 2
- **ThyrsaTheater** (2 structural warning(s))
  - FAIL hidden items: 0 < 2
- **AktiTown** (3 structural warning(s))
  - WARN layout: the same cells as Lebadeia, Kirrha, GulfFerry_Deck and 4 more (one of them is a placeholder copy)

### Dungeons

| Map | Stage | Screens | Grass/screen | Forced grass | Trainers | Items | Hidden | Signs | Wild | Fails | Warnings |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Route12_CaveOfMaia | Arkadia | 1.3 | 0 | – | 0 | 0 | 0 | 0 | none | 1 | 1 |
| TrophoniosCave_B1F | Arkadia | 1.3 | 0 | – | 0 | 0 | 0 | 0 | land M (7 spp), Lv 28–31 | 1 | 1 |
| TrophoniosCave_B2F | Arkadia | 1.3 | 0 | – | 0 | 0 | 0 | 0 | land M (7 spp), Lv 28–31 | 1 | 1 |
| Route6_AntiopesCave | Thyrsa | 1.3 | 0 | – | 0 | 2 | 0 | 6 | none | 0 | 3 |

Dungeon shortfalls, worst first:

- **Route12_CaveOfMaia**
  - FAIL items on this floor: 0 (visible and hidden) < 2
  - WARN layout: the same cells as Route6_AntiopesCave, TrophoniosCave_B1F, TrophoniosCave_B2F (one of them is a placeholder copy)
- **TrophoniosCave_B1F**
  - FAIL items on this floor: 0 (visible and hidden) < 2
  - WARN layout: the same cells as Route6_AntiopesCave, TrophoniosCave_B2F, Route12_CaveOfMaia (one of them is a placeholder copy)
- **TrophoniosCave_B2F**
  - FAIL items on this floor: 0 (visible and hidden) < 2
  - WARN layout: the same cells as Route6_AntiopesCave, TrophoniosCave_B1F, Route12_CaveOfMaia (one of them is a placeholder copy)
- **Route6_AntiopesCave** (2 structural warning(s))
  - WARN layout: the same cells as TrophoniosCave_B1F, TrophoniosCave_B2F, Route12_CaveOfMaia (one of them is a placeholder copy)

Whole dungeons:

- **Route12_CaveOfMaia** (1 floor(s))
  - FAIL trainers in the whole dungeon: 0 < 1
  - FAIL hidden items in the whole dungeon: 0 < 2
- **Route6_AntiopesCave** (1 floor(s))
  - FAIL trainers in the whole dungeon: 0 < 1
  - FAIL hidden items in the whole dungeon: 0 < 2
- **TrophoniosCave** (2 floor(s))
  - FAIL trainers in the whole dungeon: 0 < 3
  - FAIL hidden items in the whole dungeon: 0 < 2

25 map(s): 65 hard shortfall(s) in 23 map(s), 90 warning(s)

## `claude/world-act3-4e546d`, at `237f76ef2b`

### Routes

| Map | Stage | Screens | Grass/screen | Forced grass | Trainers | Items | Hidden | Signs | Wild | Fails | Warnings |
|---|---|---|---|---|---|---|---|---|---|---|---|
| KytheraSpringOfKallirhoe | Kythera | 3.8 | 13 | 0 | 1 | 1 | 0 | 7 | land MN (8/6 spp), Lv 40–44 | 8 | 0 |
| KytheraNeraidaFalls | Kythera | 8.8 | 8 | – | 4 | 2 | 0 | 6 | land MN (9/6 spp), surf M (2 spp), Lv 41–45 | 6 | 8 |
| KytheraFoamRoad | Kythera | 10.2 | 4 | 7 | 4 | 3 | 0 | 12 | land MN (8/7 spp), surf M (4 spp), fish M (4 spp), Lv 39–43 | 5 | 11 |
| Route23_CretanSea (sea) | Knossa | 16.0 | 1 | – | 3 | 1 | 0 | 8 | land MN (5/5 spp), surf M (5 spp), fish M (4 spp), Lv 40–44 | 5 | 2 |
| KallisteRoute1_KronionHill | Kalliste | 9.9 | 3 | – | 0 | 1 | 2 | 7 | land M (11 spp), Lv 5–7 | 4 | 5 |
| Route22_MyrtoanSea (sea) | Kythera | 16.0 | 0 | – | 2 | 0 | 0 | 3 | surf M (5 spp), fish M (3 spp) | 4 | 1 |
| KallisteRoute1 | Kalliste | 12.8 | 18 | 8 | 5 | 3 | 3 | 3 | land MN (11/12 spp), Lv 3–6 | 3 | 2 |
| Route22_CretanSea (sea) | Kythera | 16.0 | 0 | – | 2 | 1 | 0 | 4 | surf M (5 spp), fish M (4 spp) | 3 | 1 |

Route shortfalls, worst first:

- **KytheraSpringOfKallirhoe** (notes: no _Day land table (day falls back to morning))
  - FAIL grass: 13 cells per screen < 15 (48 cells in 3.8 screens; 57 needed)
  - FAIL forced grass: the ends can be walked between crossing 0 grass cell(s) < 8 (down (KYTHERA_FOAM_ROAD) to warp to KytheraEchoCaves: 0, warp to KytheraEchoCaves to down (KYTHERA_FOAM_ROAD): 0)
  - FAIL trainers: 1 < 8 (late route of 3.8 screens)
  - FAIL item balls: 1 < 5
  - FAIL hidden items: 0 < 4
  - FAIL wild: 83 reachable water cells but no surf table
  - FAIL wild: 83 reachable water cells but no fishing table
  - FAIL wild: the Night land table has 6 species < 7
- **KytheraNeraidaFalls** (7 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL grass: 8 cells per screen < 15 (74 cells in 8.8 screens; 132 needed)
  - FAIL trainers: 4 < 8 (late route of 8.8 screens)
  - FAIL item balls: 2 < 5
  - FAIL hidden items: 0 < 4
  - FAIL wild: the Night land table has 6 species < 7
  - FAIL wild: the Morning surf table has 2 species < 3
  - WARN forced grass: can't measure, fewer than two ends a walker can reach each other from (1 end(s))
- **KytheraFoamRoad** (9 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL grass: 4 cells per screen < 15 (44 cells in 10.2 screens; 154 needed)
  - FAIL forced grass: the ends can be walked between crossing 7 grass cell(s) < 8 (up (KYTHERA_SPRING_OF_KALLIRHOE) to left (KYTHERA_PAPHIA): 7, up (KYTHERA_SPRING_OF_KALLIRHOE) to right (KYTHERA_SKANDEIA): 0, left (KYTHERA_PAPHIA) to up (KYTHERA_SPRING_OF_KALLIRHOE): 7, left (KYTHERA_PAPHIA) to right (KYTHERA_SKANDEIA): 7, right (KYTHERA_SKANDEIA) to up (KYTHERA_SPRING_OF_KALLIRHOE): 0, right (KYTHERA_SKANDEIA) to left (KYTHERA_PAPHIA): 7)
  - FAIL trainers: 4 < 9 (late route of 10.2 screens)
  - FAIL item balls: 3 < 5
  - FAIL hidden items: 0 < 4
  - WARN dead end: 22 cells, 7 deep, ending at (36, 4), entered at (33, 1), holds nothing
  - WARN dead end: 13 cells, 6 deep, ending at (58, 15), entered at (62, 17), holds nothing
- **Route23_CretanSea** (notes: no _Day land table (day falls back to morning))
  - FAIL trainers: 3 < 6 (sea route of 16.0 screens)
  - FAIL item balls: 1 < 2
  - FAIL hidden items: 0 < 2
  - FAIL wild: the Morning land table has 5 species < 7
  - FAIL wild: the Night land table has 5 species < 7
  - WARN set piece: none found (no scene trigger, gift, trade or berry tree); check there is one
  - WARN wild: land levels 40–44 sit outside Knossa's 42–48 (BALANCE.md)
- **KallisteRoute1_KronionHill** (4 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL grass: 3 cells per screen < 15 (29 cells in 9.9 screens; 149 needed)
  - FAIL trainers: 0 < 5 (early route of 9.9 screens)
  - FAIL item balls: 1 < 2
  - FAIL wild: no _Night land table
  - WARN forced grass: can't measure, fewer than two ends a walker can reach each other from (1 end(s))
- **Route22_MyrtoanSea**
  - FAIL trainers: 2 < 6 (sea route of 16.0 screens)
  - FAIL item balls: 0 < 2
  - FAIL hidden items: 0 < 2
  - FAIL wild: the Morning fishing table has 3 species < 4
  - WARN set piece: none found (no scene trigger, gift, trade or berry tree); check there is one
- **KallisteRoute1** (2 structural warning(s), notes: no _Day land table (day falls back to morning))
  - FAIL trainers: 5 < 6 (early route of 12.8 screens)
  - FAIL wild: 43 reachable water cells but no surf table
  - FAIL wild: 43 reachable water cells but no fishing table
- **Route22_CretanSea**
  - FAIL trainers: 2 < 6 (sea route of 16.0 screens)
  - FAIL item balls: 1 < 2
  - FAIL hidden items: 0 < 2
  - WARN set piece: none found (no scene trigger, gift, trade or berry tree); check there is one

### Towns

| Map | Stage | Screens | Grass/screen | Forced grass | Trainers | Items | Hidden | Signs | Wild | Fails | Warnings |
|---|---|---|---|---|---|---|---|---|---|---|---|
| KytheraPaphia | Kythera | 10.0 | 0 | – | 0 | 0 | 0 | 7 | surf M (4 spp), fish M (4 spp) | 2 | 5 |
| KytheraSkandeia | Kythera | 8.0 | 0 | – | 0 | 0 | 0 | 6 | surf M (4 spp), fish M (4 spp) | 2 | 1 |
| ElaiaVillage | Kalliste | 7.6 | 0 | – | 0 | 1 | 1 | 22 | none | 1 | 2 |
| Melos | Kythera | 7.3 | 9 | – | 2 | 1 | 0 | 9 | land MN (8/8 spp), surf M (5 spp), fish M (4 spp), Lv 38–42 | 1 | 1 |
| AktiTown | Kalliste | 5.2 | 0 | – | 0 | 2 | 3 | 9 | surf M (5 spp), fish M (9 spp) | 0 | 3 |

Town shortfalls, worst first:

- **KytheraPaphia** (3 structural warning(s))
  - FAIL hidden items: 0 < 2
  - FAIL item balls: 0 < 1
  - WARN every house a home: nothing found happening in KytheraPaphia_OrchardHouse (no gift, trade, battle, heal or item)
  - WARN dead end: 8 cells, 3 deep, ending at (27, 10), entered at (26, 11), holds nothing
- **KytheraSkandeia** (1 structural warning(s))
  - FAIL hidden items: 0 < 2
  - FAIL item balls: 0 < 1
- **ElaiaVillage** (2 structural warning(s))
  - FAIL hidden items: 1 < 2
- **Melos** (notes: no _Day land table (day falls back to morning))
  - FAIL hidden items: 0 < 2
  - WARN every house a home: nothing found happening in Melos_KnappersHouse (no gift, trade, battle, heal or item)
- **AktiTown**: meets the standard (3 structural warning(s))

### Dungeons

| Map | Stage | Screens | Grass/screen | Forced grass | Trainers | Items | Hidden | Signs | Wild | Fails | Warnings |
|---|---|---|---|---|---|---|---|---|---|---|---|
| KytheraEchoCaves | Kythera | 5.5 | 0 | – | 2 | 2 | 0 | 3 | land M (7 spp), surf M (5 spp), fish M (3 spp), Lv 40–44 | 1 | 0 |

Dungeon shortfalls, worst first:

- **KytheraEchoCaves**
  - FAIL wild: the Morning fishing table has 3 species < 4

Whole dungeons:

- **KytheraEchoCaves** (1 floor(s))
  - FAIL hidden items in the whole dungeon: 0 < 2

14 map(s): 46 hard shortfall(s) in 13 map(s), 42 warning(s)

