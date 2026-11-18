# The Pantheon: the Propylaia, the four seats, the Hall of Heroes

Builders: `tools/ichor/maps/olympus.py` (layouts), `tools/ichor/maps/league_seats.py` (the seats' scripts), `tools/ichor/maps/league_trainers.py` (the parties). The briefs are `design/LEAGUE.md`'s; the summit has its own file (`Olympus_Summit.md`).

| Map | Set piece | The scene before the battle |
|---|---|---|
| **Olympus_Propylaia** | Hestia's hearth on its raised ring, the red runner to the inner door | The priestess heals; the Archon's guard lets a challenger with eight Laurels in (`FLAG_ICHOR_PANTHEON_ENTERED`) |
| **Olympus_SeatOfAres** (Brasidas) | Two files of arms racks and helmets as a phalanx, the bronze way up the middle, cold braziers by the polemarch | He raises his spear: both braziers catch, and spear strikes shield three times from every rack (three camera shakes), the Lakonian salute |
| **Olympus_SeatOfPoseidon** (Themistokles) | The trireme in its sacred basin, open to the sky | He raps the ram; the basin heaves and every oar lifts at once |
| **Olympus_SeatOfAthena** (Hypatia) | Scroll walls and reading tables in a grid, the rostrum | An owl wakes, every lamp brightens, and she asks her one question (three answers, each with its own reply) |
| **Olympus_SeatOfHera** (Olympias) | A forest of dark columns over the serpent pits, the throne on its dais | She rises: Hera's torches catch pair by pair up the aisle to the braziers at her feet, and the serpents lift their heads |
| **Olympus_HallOfHeroes** | The cella of the Twelve, the record stone | The white flash and chime of the record (Emerald's Hall of Fame) |

The run is Emerald's: each seat's door shuts behind you, nothing heals between seats, and a whiteout resets all four. Lit braziers and torches stay lit on a beaten seat's reload (`SetOpen`).

## Hooks for later

- **Rematches:** after the first Hall of Heroes the seats can be run again with the same teams; the post-game's rematch levels and an empty-altar Archon rematch are POSTGAME work (BALANCE's Aethos post-game row).
- **Art:** an Ares frieze or shield wall, a Hera frieze (peacock, Hydra, Ladon, the pomegranate) and a record stone are still on LEAGUE.md's art list.

## Renders

No layout changes on 2026-11-18 beyond marking the six interiors `"ichor_kind": "interior"` (the Labyrinth columns in Ares's seat carry `MB_CAVE`, which made `map_audit` read the seat as a dungeon and fail it). Current renders: `img/olympus_seats_after.png`.
