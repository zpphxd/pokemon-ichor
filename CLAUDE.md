# Pokémon Ichor: team handbook

This repo is a fan ROM hack built on **pokeemerald-expansion 1.17.2**, the Emerald decompilation. Every agent working here reads this file first.

The model-neutral entry point is [AGENTS.md](AGENTS.md). Shared task contracts,
regression selection and evidence requirements live in
[design/ENGINEERING.md](design/ENGINEERING.md).

## Sources of truth

- **`design/PITCH.md`** is the design bible: story, world, characters, the Twelve, Pokémon, systems and roadmap. Read the relevant section before any content work. If a change contradicts the bible, raise it with the creative director (the main session) instead of improvising.
- **`design/BALANCE.md`** is the level curve for the whole game; every encounter table and trainer party takes its levels from it.
- **`design/MAP_DESIGN.md`** is the map design rulebook every map follows: forced grass, trainer checkpoints, ledges, rewards, relic gates, town and dungeon structure.
- **`design/TERMS.md`** gives the Ichor word for every Pokémon-system term (Asclepeion, Pithos, Laurel and the rest) and how to case it. `tools/ichor/text_width.py` measures a line against the game font.
- **`design/research/RESEARCH.md`** covers engine facts, tool versions and GBA constraints.
- **`design/research/LAZARUS.md`** is the list of things we must not copy from Pokémon Lazarus, an existing Greek-themed hack.
- Expansion docs live in `docs/` (upstream), `FEATURES.md` and `INSTALL.md`. Config switches live in `include/config/*.h`.

## Build and test

```bash
make -j$(sysctl -n hw.ncpu)            # builds pokeemerald.gba (~1 min clean)
tools/ichor/smoke_test.sh              # boots it headlessly, screenshots to build/smoke/
make check -j$(sysctl -n hw.ncpu)      # expansion test suite (needs: brew install coreutils)
mgba pokeemerald.gba                   # play it
```

- The toolchain is devkitARM (gcc 16.1) in `/opt/devkitpro`. `DEVKITPRO` and `DEVKITARM` come from the devkitPro launch agent. If they are missing, export `DEVKITPRO=/opt/devkitpro` and `DEVKITARM=/opt/devkitpro/devkitARM`.
- Every change must leave `make` green and `tools/ichor/smoke_test.sh` passing. Run both before reporting work as done, and look at the screenshots when the change is visible.
- **Headless runs.**
  - `tools/ichor/mgba_headless.c` is our Lua-capable headless mGBA, built on demand against Homebrew's libmgba. The bundled `tools/mgba` runner has no Lua.
  - Write new automated checks as Lua scripts that run on it. `console:log` and the ROM's mgba printf go to stdout, and the run stops on the `--until` text.
- **ROM budget.** The stock expansion build already uses 26.7 MB of the 32 MB limit (80%). That leaves about 5 MB for all of Ichor's maps, art and music. Check `make`'s memory usage line after adding assets, and cut upstream content before cutting ours.
- Patches: `flips --create --bps <clean emerald.gba> pokeemerald.gba ichor.bps`. ROMs, saves and patches are never committed.

## Tools

| Tool | Version | Use |
|---|---|---|
| Porymap | 6.3.1, at `~/Applications/porymap.app` | Maps, events, encounters |
| poryscript | 3.6.1, in `~/.local/bin` | Event scripts |
| porytiles | 2.0.0, in `~/.local/bin` | Tileset compiler |
| flips | in `~/.local/bin` | `.bps` patches |
| mGBA | 0.10.5, Homebrew | Playing. Its libmgba powers the headless test runner. |

## Conventions

- **Scripts.**
  - Write new map scripts in Poryscript as `data/maps/<Map>/scripts.pory`. The build compiles it to `scripts.inc` through `poryscript_rules.mk`.
  - When converting an existing map, `git rm` its `scripts.inc` and add that path to `.gitignore`.
- **Flags and vars.**
  - Claim an unused one by renaming its `FLAG_UNUSED_0x…` or `VAR_UNUSED_0x…` line in `include/constants/flags.h` or `vars.h` to `FLAG_ICHOR_<NAME>` or `VAR_ICHOR_<NAME>`, with a comment.
  - Never reuse an `ICHOR_` one. `grep -n ICHOR_ include/constants/` lists what is taken.
  - Prefer Ichor's own banks, saved in IchorSave: `tools/ichor/claim.py bankflag`, `dailyflag` or `bankvar` (3,584 flags in two banks, 256 daily flags, 32 vars). They work with every flag and var command. See `design/ENGINE_API.md` §1.
- **Config changes** go in `include/config/*.h`. Note why in the commit message.
- **Naming.**
  - Place, character and item names come from the bible.
  - New in-game names must be Greek-rooted and must not collide with the Lazarus avoid-list.
- **In-game text.**
  - Short lines, written so they still fit the Gen 3 text box (Poryscript's `format()` wraps text).
  - Characters sound like people, not encyclopedias. Myth references are woven into play, never lectured.
- **Graphics.**
  - 4bpp, 16-color palettes, color 0 transparent.
  - Tilesets: draw `bottom/middle/top.png` at 128 px wide and compile with Porytiles. Plan palettes first: 6 primary and 7 secondary.
  - A secondary tileset may use at most 504 tiles. Door animations copy their frames over tiles 504–511 (`DOOR_TILE_START_SIZE1` in `src/field_door.c`), so anything there glitches while a door opens. Leave 496–511 free if a map uses wide doors.
  - Overworld NPCs share palette families.
- **Upstream.**
  - `upstream` is rh-hideout/pokeemerald-expansion.
  - Engine updates arrive by merging a release tag, never by cherry-picking.
  - Keep engine edits small and well-commented so merges stay easy.

## Git

- Work in the assigned checkout and branch (an isolated feature worktree when provided).
  Never edit the main checkout from another worktree. `main` is the integration
  branch; `origin` is the private repo `zpphxd/pokemon-ichor`.
- Commit format:

  ```
  type(scope): brief description

  Why this change was made (not what).

  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
  ```

  Types: feat, fix, refactor, docs, test, chore, perf. Scopes: engine, map, script, art, audio, balance, design, tools.

## Roadmap status

| Phase | Status |
|---|---|
| 0. Foundation (toolchain, first build, feature config, pipelines) | Done 2026-11-14: builds green, smoke test and `make check` pass |
| 1. Vertical slice: Kalliste Isle, Temple of Hestia | Playable; current natural-level balance and user look/fun approval still gate completion |
| 2. Act I: voyage, Emporion, Eleusa | Playable through Laurel 3 and the sanctum; closing scenes and complete integrations remain |
| 3–4. Act II, Act III and League | Next connected chapter builds; story-complete milestone is **0.9** |
| 5–6. Core post-game and release | **1.0** includes approved core post-game, ten Oikoumene lands and full Periodos halls |

The current status and acceptance matrix is in `design/PITCH.md` §8. Approved
`design/OIKOUMENE.md` §13 decisions supersede older conflicting release labels.
