# Claim ranges

Every build session claims flags only inside its own range, so parallel work never collides when the director merges it:

```bash
python3 tools/ichor/claim.py --range LO-HI flag NAME "comment"
```

The director assigns the ranges. Ask in your report if your range runs low.

| Owner | Flags (hex) | Free now | Notes |
|---|---|---|---|
| The slice (director and area agents: Elaia, Route 1, Akti, the temple) | 0x020–0x1FF | 201 | |
| **world-act1** (Phase 2: the crossing, Aegina, Emporion, the Sacred Way, Eleusa) | 0x200–0x2FF | 214 | |
| **world-act2** | 0x300–0x37F | 110 | |
| **world-act3** | 0x380–0x3FF | 121 | |
| **ichor-engine** (relics, rites, herms, save state) | 0x400–0x47F | 128 | Prefer the Ichor SaveBlock3 struct for bulk state |
| **the post-game** | 0x480–0x4BF | 64 | |
| **the Oikoumene** | 0x4C0–0x4FF | 49 | |

The Hoenn cut freed 700 vanilla flags: every Hoenn story, item and hide flag that nothing left in the build names. The "Free now" counts are the `FLAG_UNUSED_0x…` lines in each range.

- **Hidden items need these vanilla flags.** `bg_hidden_item_event` (asm/macros/map.inc) stores the flag as an offset from `FLAG_HIDDEN_ITEMS_START` (0x1F4), so a hidden item's flag must be a vanilla flag at 0x1F4 or above. Spend your range's flags from 0x1F4 up on hidden items. Put story and other state in the Ichor bank flags (`claim.py bankflag`) instead.
- Hoenn flags that upstream C or a kept script still names stay defined until batch 3 cuts those systems: the decorations (0x0AE–0x0BB, reached by arithmetic), the Battle Frontier's, and a few dozen story flags.

## Ichor bank flags and vars (in IchorSave)

The ichor-engine session's IchorSave holds 0x500 bank flags, 0x70 daily flags and 32 bank vars. These are the main pool for new content, so claim from them first. The `--range` LO-HI value is an offset into each bank:

```bash
python3 tools/ichor/claim.py --range 0x000-0x0FF bankflag FLAG_ICHOR_... "comment"
```

| Owner | bankflag offsets | dailyflag offsets | bankvar offsets |
|---|---|---|---|
| **world-act1** | 0x000–0x0FF | 0x40–0x4B | 0–5 |
| **world-act2** | 0x100–0x1FF | 0x4C–0x57 | 6–11 |
| **world-act3** | 0x200–0x2FF, and 0x4C0–0x4FF | 0x58–0x63 | 12–17 |
| **the post-game** | 0x300–0x3BF | 0x64–0x6F | 18–23 |
| **the Oikoumene** | 0x3C0–0x47F | — | 24–27 |
| **ichor-engine** | 0x480–0x4BF | 0x00–0x3F | 28–31 |
| Reserve | (given to world-act3) | — | — |

Hidden items still need vanilla flags at or above `FLAG_HIDDEN_ITEMS_START` (see `asm/macros/map.inc`), so claim those from your vanilla flag range.

## Vars

115 vars are free now that the Hoenn cut has run (`VAR_UNUSED_0x…` in `include/constants/vars.h`; 0x4010–0x401F are the object-graphics vars and stay). Use `VAR_TEMP_*` for state within a single scene, and the Ichor SaveBlock3 struct (`design/ENGINE_API.md`, by ichor-engine) for anything lasting. Claim a real var only with the director's OK.

## Trainers

Emerald's Hoenn trainers are gone. `MAX_TRAINERS_COUNT_EMERALD` is 1,024 (raised from upstream's 864 for the Oikoumene, PG-38 in `design/OIKOUMENE.md`), so trainer ids run 1–1023, each with its own defeated flag at `TRAINER_FLAGS_START + id`. System flags start at 0x900: always use their names, never numbers.

| Owner | Trainer ids | Notes |
|---|---|---|
| The slice | 1–14 | Full |
| The Frontier engine | 15–21 | The seven Hoenn Brains (`TRAINER_ANABEL` … `TRAINER_BRANDON`), kept because `gFrontierBrainInfo` reads their pic, class and name. The post-game re-themes them as the Olympiad's Brains. |
| Reserve | 22–39 | Ask the director |
| **world-act1** | 40–159 | |
| **world-act2** | 160–319 | |
| **world-act3** | 320–499 | Includes the League |
| **the post-game** | 500–679 | Rematches (the War Horn, the Arena of Champions) need ids of their own |
| **the Oikoumene** | 680–819 and 864–1023 | 300 in all, for its ten champion halls |
| Reserve | 820–863 | Shared; ask the director |

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
