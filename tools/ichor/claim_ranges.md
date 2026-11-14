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

## Vars

Only 20 vars are free. Use `VAR_TEMP_*` for state within a single scene, and the Ichor SaveBlock3 struct (`design/ENGINE_API.md`, by ichor-engine) for anything lasting. Claim a real var only with the director's OK.

## Trainers

Until the Hoenn cut lands, only 11 trainer ids are free (MAX_TRAINERS_COUNT_EMERALD is 880). The hoenn-cut session removes Hoenn's 855 trainers first, renumbers Ichor's own from 1, and then hands out trainer id ranges here.
