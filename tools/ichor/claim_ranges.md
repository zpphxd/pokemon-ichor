# Claim ranges

Every build session claims flags only inside its own range, so parallel work never collides when the director merges it:

```bash
python3 tools/ichor/claim.py --range LO-HI flag NAME "comment"
```

The director assigns the ranges. Ask in your report if your range runs low.

| Owner | Flags (hex) | Free now | Notes |
|---|---|---|---|
| The slice (director and area agents: Elaia, Route 1, Akti, the temple) | 0x020–0x1FF | 197 | 9 of them can hold a hidden item: 0x1F7–0x1FF |
| **world-act1** (Phase 2: the crossing, Aegina, Emporion, the Sacred Way, Eleusa) | 0x200–0x2FF | 214 | |
| **world-act2** | 0x300–0x37F | 110 | |
| **world-act3** | 0x380–0x3FF | 121 | |
| **ichor-engine** (relics, rites, herms, save state) | 0x400–0x47F | 128 | Prefer the Ichor SaveBlock3 struct for bulk state |
| **the post-game** | 0x480–0x4BF | 64 | |
| **the Oikoumene** | 0x4C0–0x4FF | 49 | |

The Hoenn cut freed 700 vanilla flags: every Hoenn story, item and hide flag that nothing left in the build names. The "Free now" counts are the `FLAG_UNUSED_0x…` lines in each range.

- **Hidden items can use bank flags.** `bg_hidden_item_event` (asm/macros/map.inc) takes a vanilla flag at 0x1F4 or above, or any Ichor bank flag (both general banks, 0x2000–0x2EFF). Claim one from your bank range with `python3 tools/ichor/claim.py --range LO-HI hiddenitem FLAG_ICHOR_HIDDEN_ITEM_<NAME> "comment"`. It takes a flag from the same lines as `bankflag`, so it counts against your bank range. Vanilla flags still work for hidden items that already use them.
- Hoenn flags that upstream C or a kept script still names stay defined until batch 3 cuts those systems: the decorations (0x0AE–0x0BB, reached by arithmetic), the Battle Frontier's, and a few dozen story flags.

## Ichor bank flags and vars (in IchorSave)

The ichor-engine session's IchorSave holds 0xAE0 bank flags (the first bank's 0x500 plus a second bank of 0x5E0, added 2026-11-14 as IchorSave v4), 0x70 daily flags and 32 bank vars. Offsets run on as one number line: 0x500 and up land in the second bank (`FLAG_ICHOR_GENERAL2_START + n`), and claim.py handles both. These are the main pool for new content, so claim from them first. The `--range` LO-HI value is an offset into each bank:

```bash
python3 tools/ichor/claim.py --range 0x000-0x0FF bankflag FLAG_ICHOR_... "comment"
```

| Owner | bankflag offsets | dailyflag offsets | bankvar offsets |
|---|---|---|---|
| **world-act1** | 0x000–0x0FF | 0x40–0x4B | 0–5 |
| **world-act2** | 0x100–0x1FF, and 0x500–0x63F | 0x4C–0x57 | 6–11 |
| **world-act3** | 0x200–0x2FF, 0x4C0–0x4FF, and 0x640–0x6BF | 0x58–0x63 | 12–17 |
| **world-act3, the League** (the Ascent, Olympus, L-1 to L-10; `design/LEAGUE.md`) | 0x6C0–0x6FF (24 used: 0x6C0–0x6D7) | — | — |
| **the post-game** | 0x300–0x3BF, and 0x700–0x7FF | 0x64–0x6F | 18–23 |
| **the Oikoumene** | 0x3C0–0x47F, and 0x800–0x8FF | — | 24–27 |
| **ichor-engine** | 0x480–0x4BF (0x4A0–0x4BF are the travel herms, `FLAG_ICHOR_TOWN_HERM_*`: rename a spare for a new town) | 0x00–0x3F | 28–31 |
| Reserve | 0x900–0xADF (480); ask the director. The second bank's last 32 flags sit outside these offsets as `FLAG_ICHOR_WAYSTONES_START`, for the Oikoumene's herm run | — | — |

Hidden items can take these bank flags too (`claim.py hiddenitem`; see `asm/macros/map.inc`), so the vanilla range is no longer the limit on them.

### Act I dig indices

These indices are inside the engine's reserved dig ranges, not the general bank
offsets above. Do not assign them to another find.

General bank offset 0x02E is `FLAG_ICHOR_GOT_AMPHORA_PATCH`, the one-time
Ability Patch on Daphne's shelf after all twelve amphorae are restored.
It is independent of sherd collection and the reserved restored-amphora bank.

| Kind | Index | Location | Find |
|---|---|---|---|
| Fixed (`FLAG_ICHOR_DIG_FIXED_START`) | 0 | Emporion Harbor's quay planter | First available Arachne sherd |
| Daily (`FLAG_DAILY_ICHOR_DIG_START`) | 0 | Emporion Harbor's ship sheds | Act I loot, including Arachne sherds |
| Daily (`FLAG_DAILY_ICHOR_DIG_START`) | 1 | Emporion's Hephaisteion garden | Act I loot, including Arachne sherds |
| Daily (`FLAG_DAILY_ICHOR_DIG_START`) | 2 | Eleusa's west field | Act I loot, including Persephone sherds |
| Daily (`FLAG_DAILY_ICHOR_DIG_START`) | 3 | Eleusa's east meadow | Act I loot, including Persephone sherds |
| Daily (`FLAG_DAILY_ICHOR_DIG_START`) | 6 | Kronion Hill's pried-up slabs (8,6) | Act I loot, including Kronos sherds |
| Daily (`FLAG_DAILY_ICHOR_DIG_START`) | 7 | Route 1's bee terraces (23,26) | Act I loot, including Kronos sherds |
| Daily (`FLAG_DAILY_ICHOR_DIG_START`) | 8 | Akti's beach shells (25,9) | Act I loot, including Kronos sherds |

Herm id 25 is Emporion's crossroads town anchor. It uses the reserved Aethos
herm bank but does not count toward the 23-route completion reward. Its Wings
landing is (26,32); the Asclepeion's existing respawn location is unchanged.
`FLAG_ICHOR_HERM_EMPORION` is retained as a legacy mirror.

Daily general offset 0x40 is `FLAG_DAILY_ICHOR_AUGURY_READ`: one shared
reading/blessing entitlement per day, retained across map changes.

General bank offset 0x08E is `FLAG_ICHOR_HIDE_OMEN_KORANTHA`, Eleusa's rare
visitor at (17,35), in the reachable wheat rather than the sealed Rharian field.
Visitor id 2 preserves the reserved Act II visitor ids 0/1.
The daily omen clears this hide flag only for a matching visit; capture/defeat
sets it again, while escape/loss leaves it available.
General bank offset 0x08F is `FLAG_ICHOR_HIDE_OMEN_PITHOUND`, visitor id 3.
It records consumption of Emporion's marked-jar visitor at (10,24), without
hiding the jar. Only its matching later omen clears it for another visit.
General bank offset 0x01E is `FLAG_ICHOR_HIDE_OMEN_NEMECUB`, visitor id 4,
for the cleared Isthmus hill spur at (28,3). Its capture/defeat state resets
only with another matching omen, like the Eleusa visitor.
General offset 0x01F is `FLAG_ICHOR_DIFFICULTY_CHOSEN`; bank var offset 0 is
`VAR_ICHOR_DIFFICULTY`. An unset confirmation flag means Hero, preserving old
saves whose new var is zero. The bedroom's confirmed selection is save-fixed.
General offset 0x02C is `FLAG_ICHOR_GOT_MOMS_HONEY`, the one-time three-Honey
return-home gift after the Act I ending and letter. It is set only after the
whole gift fits; `FLAG_ICHOR_WROTE_TO_MOM` independently records the sent letter.
General offset 0x02D is `FLAG_ICHOR_HIDE_DAPHNE_AKADEMIA`. The Akademia transition
sets it after `FLAG_ICHOR_MYSTERIES_NIGHT`, preventing duplicate home/mainland
appearances; earlier visits clear it.
General offsets 0x02F/0x030 are `FLAG_ICHOR_KRONION_ALTAR_STONE` and
`FLAG_ICHOR_ELEUSA_PERSENYX`, permanent capture/victory receipts for the
restored-amphora encounters. Offset 0x031 is
`FLAG_ICHOR_HIDE_AMPHORA_PERSENYX`, derived from restoration, the receipt and
dusk; it is not the encounter's completion state or a daily omen flag.
Isthmus excavation uses daily dig indices 4 (kilns) and 5 (hill spur), and fixed
find index 1 (family tomb, Girdle-gated). All belong to the Arachne amphora.
These are offsets in the reserved dig ranges, not the general flag range.
Fixed dig index 2 is sanctum B1F's Persephone sherd (bay B's great jar).
Fixed dig index 3 is sanctum B3F's Daedalus page II, exposed after the cave-in;
it grants canonical page offset 1 (`FLAG_ICHOR_PAGES_START + 1`).

### Act I technique scrolls

TM51, TM52 and TM53 activate existing reserved item IDs as Fling, Bulldoze
and Round. Myrtale awards Fling; Emporion sells Bulldoze and Round. Existing
TM01–50 and HM item IDs are unchanged. The fixed 64-slot TM/HM pocket still
holds all 53 TMs and eight HMs without a save-layout change.

## Vars

115 vars are free now that the Hoenn cut has run (`VAR_UNUSED_0x…` in `include/constants/vars.h`; 0x4010–0x401F are the object-graphics vars and stay). Use `VAR_TEMP_*` for state within a single scene, and the Ichor SaveBlock3 struct (`design/ENGINE_API.md`, by ichor-engine) for anything lasting. Claim a real var only with the director's OK.

## Trainers

Emerald's Hoenn trainers are gone. `MAX_TRAINERS_COUNT_EMERALD` is 1,536 (raised from upstream's 864: to 1,024 for the Oikoumene, PG-38 in `design/OIKOUMENE.md`, then to 1,536 for Emerald's trainer density, `design/MAP_DESIGN.md` §8), so trainer ids run 1–1535, each with its own defeated flag at `TRAINER_FLAGS_START + id`. System flags start at 0xB00: always use their names, never numbers.

| Owner | Trainer ids | Notes |
|---|---|---|
| The slice | 1–14 | Full |
| The slice, from the reserve | 22–25 | Route 1's Thestylis and Kronion Hill's three herders (MAP_DESIGN §8; director's go-ahead, 2026-11-14). Full |
| The Frontier engine | 15–21 | The seven Hoenn Brains (`TRAINER_ANABEL` … `TRAINER_BRANDON`), kept because `gFrontierBrainInfo` reads their pic, class and name. The post-game re-themes them as the Olympiad's Brains. |
| Reserve | 26–39 | Ask the director |
| **world-act1** | 40–159 | |
| **world-act2** | 160–319, 820–849 and 1344–1403 | 820–849 added from the shared reserve (2026-11-14): Act II's script needs 182. 1344–1403 added with the 1,536 raise |
| **world-act3** | 320–459 and 1404–1503 | Kythera to the Stair. 1404–1503 added with the 1,536 raise |
| **world-act3, the League** | 460–499 | 460–475 used: the Ascent's eleven, the Pantheon's four, the Archon. Its own `TRAINERS_END_LEAGUE` line, so it never shares a line with Act III's |
| **the post-game** | 500–679 and 1024–1223 | Rematches (the War Horn, the Arena of Champions) need ids of their own |
| **the Oikoumene** | 680–819, 864–1023 and 1224–1343 | 420 in all, for its ten champion halls and its routes |
| Reserve | 850–863 and 1504–1535 | Shared; ask the director |

To add a trainer:

1. In `include/constants/opponents.h`, add `#define TRAINER_ICHOR_<NAME> <id>` inside your own block only, at the next free id in your range.
2. Set your block's `TRAINERS_END_<OWNER>` line to your highest id + 1. `TRAINERS_COUNT_EMERALD` is the largest of these lines, so `gTrainers` grows only as far as real trainers, and no two sessions edit the same line.
3. Put the party in `src/data/trainers.party` under your section's `/* Ichor: <owner> */` comment. Order there doesn't matter: trainerproc writes designated initializers.

Never use a Hoenn trainer name. Until batch 3 cuts the rematch table's and Match Call's Hoenn entries, `include/constants/opponents_hoenn_stub.h` defines every removed one as `TRAINER_NONE`.

Battle partners (`include/constants/battle_partner.h`, `src/data/battle_partners.party`) have no ranges yet. Add yours after the last `PARTNER_*` line and bump `PARTNER_COUNT`; there are few enough that the director resolves merges by hand.

## Removed maps

Never use a Hoenn or FRLG `MAP_*`, `LAYOUT_*` or `HEAL_LOCATION_*` name. They're deleted, but `include/constants/maps_removed_stub.h` keeps each one defined, with an id no real map has, so upstream code still compiles. Only the Ichor maps are real, plus the few Frontier maps whose layouts the engine loads at runtime: the Battle Pyramid floor, top and squares, the Pike rooms and the Trainer Hill floors.

## Map sections

The Hoenn cut freed Hoenn's map-section ids 0–57 and 59–85 for the Oikoumene. No `MAPSEC_*` that Ichor uses was renumbered.

- Each freed slot is `MAPSEC_OIKOUMENE_<id>` in `src/data/region_map/region_map_sections.json`, with no name or region-map position.
- The Hoenn names stay defined as aliases in `include/constants/region_map_sections_hoenn.h`, so upstream code still compiles. When you give a slot a real name, rename it in the json and change its alias line.
- 58 is `MAPSEC_BATTLE_FRONTIER`, which the kept Pyramid and Pike maps still use. It frees once the Olympiad replaces them.
- 86 (`MAPSEC_SECRET_BASE`) and 87 (`MAPSEC_DYNAMIC`) are engine sections and stay.
- Every slot appears in `map_name_popup.c`'s theme table and most in `region_map.c`. A few have more upstream behavior behind their Hoenn name, so check before reusing them:
  - 2 (Dewford): weather
  - 8 (Slateport): the battle tent
  - 59 (Petalburg Woods), 65 (Mt. Pyre) and 85 (Sky Pillar): follower messages
  - 68 (Seafloor Cavern) and 85: the Pokédex area screen
  - 16–49 (routes): `landmark.c`
  - 0–15 (towns): `event_object_movement.c`

## Act III's chapter builds (2026-11-17)

The director split the rest of Act III across parallel builders. Each claims
only inside its own bank-flag and trainer-ID range, from the reserve:

| Builder | Beats (`design/phase4/SCRIPT.md`) | bankflag offsets | trainer ids |
|---|---|---|---|
| Knossa above ground (Amnisos, the Bull Road, the palace, the court) | III-3A–3E, III-3O, III-4 | 0x900–0x94F | 345–364 |
| The Labyrinth I (Rings I–IV, Daedalus's workshop, Minos's tomb) | III-3F–3I | 0x950–0x99F | 365–389 |
| The Labyrinth II (Rings V–VII, the forge, the Starry Chamber, the Turning, the Icarus Shaft) | III-3J–3N, III-3P | 0x9A0–0x9EF | 390–409 |
| Lakonia (Malea, Gytheion, the Eurotas, Lakonia) | III-5A–5J | 0x9F0–0xA3F | 410–424 |
| Delphoi (Kirrha's olives, the Kastalian Gorge, Delphoi, the Temple of Apollo, the Omphalos) | III-6A–III-8 | 0xA40–0xA8F | 425–444 |
| The climax (the Loom, the Frozen Hour, the Stair of Hours, Elpis's line) | III-9–III-12 | 0xA90–0xADF | 445–459 |

Shared state: `VAR_ICHOR_ACT3` (bankvar 0xC) with the values SCRIPT.md fixes,
and Knossa's `VAR_ICHOR_KNOSSA` (0xD) and `VAR_ICHOR_LABYRINTH` (0xE), claimed
by the director. Trainer ids 300–327 are the director's reserve.

Lakonia (2026-11-17): bank flags used 0x9F0-0xA1A and 0xA20-0xA33 (the
rooms' households 0xA20-0xA2A); trainer ids 410-424 all used; fixed dig
index 0x30 is fragment 8 in Lampito's burial plot.

The road north from Lakonia (2026-11-18, `tools/ichor/maps/stymphalia.py`:
Route 26, Lake Stymphalia, Route 27 and the Skiritai cave) claims from
world-act3's own blocks: bankflag offsets 0x640-0x67F (0x640-0x670 used; the
generator claims each flag it names with `claim.py --range 0x640-0x6BF`, so
reruns are no-ops), trainer ids 1404-1443 (1404-1434 used; `TRAINERS_END_ACT3`
follows the highest), brazier `FLAG_ICHOR_BRAZIERS_START + 0x60` (the cave),
and travel herm 24 (`TOWN_HERM_STYMPHALIA`, the old `FLAG_ICHOR_TOWN_HERM_SPARE_24`).

The Erymanthian Preserve (2026-11-18, `tools/ichor/maps/erymanthos.py`) claims its items' and hidden items' flags from world-act2's bankflag offsets with `claim.py --range 0x500-0x63F` (0x577-0x58A), and the Labor 4 hook `FLAG_ICHOR_ERYMANTHIAN_BOAR` from the post-game's 0x700-0x7FF (0x700). Reruns are no-ops.

The Sacred Way (2026-11-18, `tools/ichor/maps/sacredway.py`: Route 15, Daphni and its
three rooms, Route 16) claims from world-act2's own blocks: bankflag offsets
0x590-0x5AF (0x590-0x5AC used; the generator claims each flag it names with
`claim.py --range 0x590-0x5AF`, so reruns are no-ops) and trainer ids 1344-1363
(1344-1352 used; `TRAINERS_END_ACT2` follows the highest). The old road's item,
hidden-item and trainer flags (FLAG_ICHOR_ITEM_R15_*, R16_*, ids 223-234) are kept.
