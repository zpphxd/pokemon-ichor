# Pokémon Ichor

A fan ROM hack set in the ancient-era Aethos region. It is non-commercial and distributed only as a `.bps` patch for your own Pokémon Emerald ROM.

Based off RHH's pokeemerald-expansion 1.17.2 https://github.com/rh-hideout/pokeemerald-expansion/

## Layout

| Path | What it is |
|---|---|
| `design/PITCH.md` | The pitch and design bible. It is the source of truth for story, world and systems. |
| `design/research/` | Research on the toolchain, competitors and assets |
| `design/pitch/` | Source of the published pitch page |
| everything else | The pokeemerald-expansion engine plus our changes. See the expansion's [FEATURES.md](FEATURES.md) and [INSTALL.md](INSTALL.md). |

## Build

Requires devkitARM, installed through devkitPro pacman (`gba-dev`).

```bash
make -j$(sysctl -n hw.ncpu)          # produces pokeemerald.gba
make check -j$(sysctl -n hw.ncpu)    # runs the expansion test suite
```

## Branches and remotes

- `main` holds Ichor's work.
- `upstream` points to rh-hideout/pokeemerald-expansion. To take an engine update, run `git fetch upstream --tags` and merge the next `expansion/x.y.z` release tag.

## Credits

- Engine: pokeemerald-expansion by RHH (ROM Hacking Hideout) and [its contributors](CREDITS.md).
- Decompilation: pret/pokeemerald.
- Pokémon is © Nintendo, Game Freak and The Pokémon Company. This project is unaffiliated and non-commercial.
