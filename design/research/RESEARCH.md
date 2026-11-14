# Research Summary

Compiled 2026-11-13 by the research team. Facts we could not confirm on a primary source are marked *unverified*.

## 1. Engine: pokeemerald-expansion

- **Base:** [rh-hideout/pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion). The latest release is `expansion/1.17.2` (2026-10-31), and the project is very active.
- **Species:** Gen 1–9 are all on by default (`include/config/species_enabled.h`).
  - Toggles cover Megas, Gen 9 Megas (Legends Z-A and its DLC), and the Alolan, Galarian, Hisuian and Paldean forms.
  - Single families can be turned off with `P_FAMILY_*`.
- **Battle:** Mega, Z-Moves, Dynamax/Gigantamax, Terastal, Primal and Ultra Burst are supported (`include/config/battle.h`). Mechanics default to `GEN_LATEST`.
- **Overworld features** (`include/config/overworld.h`):
  - Followers: `OW_FOLLOWERS_ENABLED`, off by default. Sprites exist for Gen 4–8 and, per `FEATURES.md`, up through Gen 9. Check each species we use.
  - NPC followers.
  - Day/night tint system: `OW_ENABLE_DNS`. Vanilla maps have no lighting set up.
  - Time-of-day encounters.
- **Also built in:**
  - DexNav (`dexnav.h`, off by default).
  - Level and EV caps (`caps.h`).
  - HGSS-style Pokédex.
  - Improved AI flags.
  - Inverse and no-whiteout battle flags.
  - Overworld debug menu (R + START).
  - Battle debug menu (SELECT).
  - Test runner: `make check`.
- **Not built in** (we must make these): difficulty modes and Nuzlocke mode.
- **Save warning:** changing the species set changes the save layout, so lock the species set before long playtests.
- **Credit:** the README asks hacks to credit RHH with the version. Clone with git, not "Download ZIP", so we can pull updates.
- **ROM size:** the hard limit is 32 MB. The size of a stock all-species build is *unverified*. We will measure it on the first build. Graphics and audio take most of the space.

## 2. Toolchain for this Mac (Apple Silicon, macOS 27)

| Tool | Version | Install | Purpose |
|---|---|---|---|
| devkitARM (`gba-dev`) | current | devkitPro pacman `.pkg`, then `sudo dkp-pacman -S gba-dev devkitarm-rules` | Compiler. This is the official macOS path; agbcc is no longer needed. |
| libpng, pkg-config | installed | brew | Build tools |
| coreutils | — | `brew install coreutils` | Needed for `make check` |
| Porymap | 6.3.1 | release zip (`porymap-macos-latest.zip`) | Map, event and encounter editor |
| Poryscript | 3.6.1 | release zip | Scripting language that compiles to event scripts |
| poryscript-pls | 1.0.14 | VS Code extension | Poryscript language server |
| Porytiles | 2.0.0 | `brew install grunt-lucas/porytiles/porytiles` | Compiles layered PNGs into tilesets |
| mGBA | 0.10.5 | installed | Emulator with Lua scripting, save states and the printf log |
| Flips | — | build from source (upstream archived) | Creates `.bps` patches |
| Aseprite | — | paid, or build from source | Pixel art, plus the Porytiles CLI pipeline |

Build: `make -j$(sysctl -n hw.ncpu)` produces `pokeemerald.gba`. Tests: `make check -j`.

**Where things live in the decomp:**

| Content | Location |
|---|---|
| Maps | `data/maps/<Map>/map.json` plus `scripts.inc` or `.pory` |
| Layouts | `data/layouts/layouts.json` |
| Wild encounters | `src/data/wild_encounters.json` |
| Tilesets | `data/tilesets/` |
| Species data | `src/data/pokemon/` |
| Config | `include/config/*.h` |

## 3. Graphics and audio constraints

**Graphics:**
- 4bpp, 16-color palettes, color 0 transparent, 15-bit color.
- **Map BG budget:** 512 primary and 512 secondary tiles, and the same for metatiles. There are 6 primary and 7 secondary palettes; palettes 13–15 are reserved for UI.
- A metatile is 16×16 with two layers of 2×2 tiles. Layer types are Normal, Covered and Split. A triple-layer patch exists.
- **Porytiles:** draw `bottom.png`, `middle.png` and `top.png` at 128 px wide (height a multiple of 16), using magenta for transparency. Porytiles deduplicates tiles and assigns palettes. Plan the 6+7 palettes before drawing.
- **Sprite sizes:**
  - Trainer front sprite: 64×64.
  - Player back sprite: 64×64 frames.
  - Overworld NPCs: 16×32 (16×16 for small objects, 32×32 for large ones).
  - Pokémon icons: 32×32.
- **On-screen sprite palettes are scarce.** About four NPC palette families should be visible at once. Followers compete for the same slots.

**Audio:**
- MIDI goes through `mid2agb` and voicegroups. Files: `sound/songs/midi/`, `songs.mk`, `include/constants/songs.h`, `song_table.inc`.
- Samples are `.aif` files in `sound/direct_sound_samples/`.
- Preview tools: agbplay, and VGMusicStudio, which exports voicegroups to `.sf2` for composing in a DAW.

**Art resources:**
- Team Aqua's Asset Repo and Eevee Expo. Check each asset's credit terms.
- Greek-themed itch.io packs need a full redraw to reach the Gen 3 style. "Land of Pixels – Ancient Greeks" is CC-BY.
- The Spriters Resource hosts ripped assets, which are not free-to-use.

## 4. Competitive landscape

- **Pokémon Glazed** (our benchmark):
  - 2012 Emerald binary hack, distributed as a UPS patch. Last listed version is 9.1 (2022).
  - Regions: Tunod, then Johto, then the Rankor Archipelago.
  - Gen 1–6 species, five starters, Delta Species, day/night, side quests, rematches, difficulty modes.
  - Post-game: legendary hunts and a World Championship.
  - Weaknesses: dated engine, no speed-up, known bugs, and its Pokémon stop at Gen 6.
- **Pokémon Lazarus (Nemo622): direct competitor.**
  - Greece-inspired Ilios region, released 1.0 in Nov 2025 and v2.0 in Feb 2026.
  - 400+ species, nine starters, mythic forms, DexNav, followers, new Megas, GBC-style art.
  - We must differentiate from it. A follow-up deep dive is in `LAZARUS.md`.
- **Other top-tier hacks in 2025–26:**
  - Unbound: new region, missions, custom OST.
  - Radical Red: difficulty, randomizer, Nuzlocke.
  - Elite Redux: ability system.
  - Emerald Imperium: level caps, Gen 9.
  - Inclement Emerald.
  - Emerald Seaglass.
- **Expected features in 2026:**
  - Physical/special split, Fairy type, modern movesets.
  - No HM slaves.
  - Run anywhere, reusable TMs.
  - EV/IV viewer, mints.
  - Portable PC and healing.
  - Difficulty modes, level caps, Megas.
- **Strong expectations:**
  - DexNav, followers, day/night.
  - Randomizer and Nuzlocke modes.
  - Quest log.
  - Speed-up and skip options.
- **What makes a hack memorable:**
  - A new region and an original story.
  - A familiar gym structure with real stakes.
  - A rich post-game.
  - Curated progression.
- **What makes a hack forgettable:**
  - Text walls.
  - Brick-wall fights.
  - Grinding.
  - Over-generous items.

## 5. Titles

| Status | Titles |
|---|---|
| Taken | Ambrosia (Crystal hack), Olympus (RPG Maker fan game), Odyssey (FireRed hack), Elysium, Marble |
| Avoid | Anything with Aegis, Ilios, Sunset or Lazarus |
| Open | Laurel, Ichor, Pantheon, Hellas |

## 6. Policy and legal

- **AI-content bans:**
  - PokéCommunity's Game Development guidelines (July 2026) and Art Studio rules (Sept 2026) ban AI-generated art and writing. This comes from search summaries because the pages returned 403. Verify before posting.
  - Eevee Expo reportedly bans AI content too (*unverified*).
  - **Impact:** release venues for an AI-built hack are limited unless humans redraw the art and rewrite the text.
- **Legal:**
  - Nintendo has taken down standalone fan games, such as Uranium in 2016 and Prism in 2016.
  - Patch-only ROM hacks have largely been tolerated.
  - **Our rules:**
    - Non-commercial.
    - Distribute only a `.bps` patch; players supply their own Emerald ROM.
    - Never ship a ROM.
