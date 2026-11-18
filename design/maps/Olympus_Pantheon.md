# The Pantheon: the Propylaia, the four seats, the Hall of Heroes

Builders: `tools/ichor/maps/olympus.py` (layouts; the four seats are in `pantheon_halls.py`), `tools/ichor/art/pantheon_build.py` (the seats' four tilesets), `tools/ichor/maps/league_seats.py` (the seats' scripts, which read the swapped cells from `pantheon_swaps.json`), `tools/ichor/maps/league_trainers.py` (the parties). The briefs are `design/LEAGUE.md`'s; the summit has its own file (`Olympus_Summit.md`).

| Map | Set piece | The scene before the battle |
|---|---|---|
| **Olympus_Propylaia** | Hestia's hearth on its raised ring, the red runner to the inner door | The priestess heals; the Archon's guard lets a challenger with eight Laurels in (`FLAG_ICHOR_PANTHEON_ENTERED`) |
| **Olympus_SeatOfAres** (Brasidas) | The war hall: a bloodred floor, tropaia of captured armor in two files with tripod braziers between, dark columns, spear racks and helmets, shields and banners on the wall, the bronze Ares on his plinth | The camera climbs the runner to him on the walk-in. He raises his spear: the great braziers and the two by the door catch, and spear strikes shield three times (three camera shakes), the Lakonian salute |
| **Olympus_SeatOfPoseidon** (Themistokles) | The sea hall: one causeway across a flooded basin, coral columns out of the water, the trireme moored against the causeway, a bronze dolphin, the colossal trident over the dais | He raps the ram; the basin heaves and every oar lifts at once |
| **Olympus_SeatOfAthena** (Hypatia) | The hall of lamps: scroll walls, lampstands down the aisle, marble owls, the owl roundel, the sacred olive over the rostrum | An owl wakes, every lamp in the hall flares (the lampstands swap to lit in the white flash), and she asks her one question (three answers, each with its own reply) |
| **Olympus_SeatOfHera** (Olympias) | The peacock hall: feather columns, torches up the aisle, gold urns of pomegranates, bronze serpents, the gold throne under a great peacock fan | She rises: the torches catch pair by pair from the door up the aisle to the braziers at her feet, and every eye on the columns catches the light |
| **Olympus_HallOfHeroes** | The cella of the Twelve, the record stone | The white flash and chime of the record (Emerald's Hall of Fame) |

The run is Emerald's: each seat's door shuts behind you, nothing heals between seats, and a whiteout resets all four. Lit braziers and torches stay lit on a beaten seat's reload (`SetOpen`).

## Hooks for later

- **Rematches:** after the first Hall of Heroes the seats can be run again with the same teams; the post-game's rematch levels and an empty-altar Archon rematch are POSTGAME work (BALANCE's Aethos post-game row).
- **Art:** a record stone for the Hall is still on LEAGUE.md's art list. Water animation in Poseidon's basin would make the heave read better.

## Renders

2026-11-18: the four seats rebuilt as set pieces, each on its own tileset (`gTileset_SeatAres`,
`SeatPoseidon`, `SeatAthena`, `SeatHera`; 167-267 of 504 tiles each), with three render, critique and
fix passes per hall. Each walk-in now runs the camera up the hall to the seat-holder and back.

| Seat | Before | After |
|---|---|---|
| Ares | `img/olympus_seat_ares_before.png` | `img/olympus_seat_ares_after.png` |
| Poseidon | `img/olympus_seat_poseidon_before.png` | `img/olympus_seat_poseidon_after.png` |
| Athena | `img/olympus_seat_athena_before.png` | `img/olympus_seat_athena_after.png` |
| Hera | `img/olympus_seat_hera_before.png` | `img/olympus_seat_hera_after.png` |

The passes (`img/olympus_seat_<god>_pass1.png`, `_pass2.png`):
- **Ares.** Pass 1: the floor read as a brick wall and the hall was a thin line of props on open red.
  Pass 2: 32 x 16 flags laid by position, a colonnade of dark columns, the armory in the bays, the
  aisle's tripods lit from the start, a glow on the flags round them, the dais in dark stone with a
  bronze grid. Pass 3: the glow cut (it drew as hard squares).
- **Poseidon.** Pass 1: a bleached floor and a gate that read as a pilaster. Pass 2: a darker sea
  marble, a wet-teal dais, a gold-framed sea gate. Pass 3: long low swells on the water.
- **Athena.** Pass 1: a flat beige hall and pigeonholes too small to read. Pass 2: larger cubbies of
  scrolls seen end-on, a darker floor so the lamps can flare. Pass 3: square slabs with gold-and-olive
  stars, an ivory-and-gold rostrum, owls at the foot of its steps.
- **Hera.** Pass 1: the floor read as brick and the fan was small. Pass 2: a plum checker with gold
  studs, a purple-and-gold dais. Pass 3: the fan widened to seven cells behind the throne, urns along
  the walls to break the long straight edge.

## Plan (2026-11-18 rework): the grand Propylaia

The Propylaia is the League's lobby, the calm before the Pantheon: grand but welcoming, like the Pokémon League's lobby with its Center and Mart before the Elite Four.

- **Bigger:** a wide columned hall on gTileset_Civic, with colonnades down both sides, statues in the side aisles, braziers either side of the inner door and the great mosaic in the floor.
- **The healer:** the standard Asclepeion station (`civic_rooms.station_cells`) with the Pithos beside it (`pithos_cells`). She sets the respawn here (`HEAL_LOCATION_OLYMPUS_PROPYLAIA`).
- **The merchant:** the Agora's stall, with the endgame stock: Full Restore, Max Potion, Hyper Potion, Revive, Max Revive, Full Heal, Max Repel, and the Herakles and Theseus Balls (BALANCE's League row, 66–75).
- **The herm:** outside by the door on 3F, as before.

## Built (2026-11-18)

- `Olympus_Propylaia` is a 27x17 hall on gTileset_Civic: the Asclepeion station and the Pithos (west), the merchant's stall (east) with the League stock (Herakles, Hermes, Chronos and Nyx Balls; Full Restore, Max and Hyper Potions, Revive, Max Revive, Full Heal, Max Repel), two colonnades, the heroes' statues, Hestia's hearth between braziers, a pilgrim resting by it, the guards at the inner door. Render `img/olympus_propylaia_after.png`.
- The Twelve's statues outside (`tools/ichor/art/statues.py`) and Zeus at the summit share one object palette (`OBJ_EVENT_PAL_TAG_ICHOR_STATUE`).
