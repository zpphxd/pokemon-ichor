# Claim ranges

Every build session claims flags only inside its own range, so parallel work never collides when the director merges it:

```bash
python3 tools/ichor/claim.py --range LO-HI flag NAME "comment"
```

The director assigns the ranges. Ask in your report if your range runs low.

| Owner | Flags (hex) | Notes |
|---|---|---|
| The slice (director and area agents: Elaia, Route 1, Akti, the temple) | 0x020–0x1FF | Mostly claimed already |
| **world-act1** (Phase 2: the crossing, Aegina, Emporion, the Sacred Way, Eleusa) | 0x200–0x2FF | |
| **ichor-engine** (relics, rites, herms, save state) | 0x400–0x47F | Prefer the Ichor SaveBlock3 struct for bulk state |
| Reserve | 0x480–0x4FF | Ask the director |
| world-act2, world-act3, the post-game, the Oikoumene | from the flags the Hoenn cut frees | The hoenn-cut session adds their ranges here |

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

Only 20 vars are free. Use `VAR_TEMP_*` for state within a single scene, and the Ichor SaveBlock3 struct (`design/ENGINE_API.md`, by ichor-engine) for anything lasting. Claim a real var only with the director's OK.

## Trainers

Emerald's Hoenn trainers are gone. `MAX_TRAINERS_COUNT_EMERALD` is 864 (upstream's value), so trainer ids run 1–863, each with its own defeated flag at `TRAINER_FLAGS_START + id`.

| Owner | Trainer ids | Notes |
|---|---|---|
| The slice | 1–14 | Full |
| The Frontier engine | 15–21 | The seven Hoenn Brains (`TRAINER_ANABEL` … `TRAINER_BRANDON`), kept because `gFrontierBrainInfo` reads their pic, class and name. The post-game re-themes them as the Olympiad's Brains. |
| Reserve | 22–39 | Ask the director |
| **world-act1** | 40–159 | |
| **world-act2** | 160–319 | |
| **world-act3** | 320–499 | Includes the League |
| **the post-game** | 500–679 | Rematches (the War Horn, the Arena of Champions) need ids of their own |
| **the Oikoumene** | 680–819 | |
| Reserve | 820–863 | Ask the director |

To add a trainer:

1. In `include/constants/opponents.h`, add `#define TRAINER_ICHOR_<NAME> <id>` inside your own block only, at the next free id in your range.
2. Set your block's `TRAINERS_END_<OWNER>` line to your highest id + 1. `TRAINERS_COUNT_EMERALD` is the largest of these lines, so `gTrainers` grows only as far as real trainers, and no two sessions edit the same line.
3. Put the party in `src/data/trainers.party` under your section's `/* Ichor: <owner> */` comment. Order there doesn't matter: trainerproc writes designated initializers.

Never use a Hoenn trainer name. Until batch 2 deletes the Hoenn maps, `include/constants/opponents_hoenn_stub.h` defines every removed one as `TRAINER_NONE`, so those scripts still assemble.

Battle partners (`include/constants/battle_partner.h`, `src/data/battle_partners.party`) have no ranges yet. Add yours after the last `PARTNER_*` line and bump `PARTNER_COUNT`; there are few enough that the director resolves merges by hand.
