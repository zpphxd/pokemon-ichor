# The Labyrinth as one cave system

The connection diagram LABYRINTH_MAZE.md §3 asks for: every ring, stair, drop, climb, shortcut and the stream, and the warp ids each side promises the other. **Keep it current.** Labyrinth I (Rings I–IV, the workshop, Minos's tomb; tileset `labyrinth`, the workshop on `daidaleion`) and Labyrinth II (Rings V–VII, the forge, the chambers, the Icarus Shaft; tileset `mychos`) both edit it.

```text
                    PALACE: the Grand Staircase (Knossa above ground)
                               | stair             ^ Daedalus's lift (after scene D)
                               v                   |
   +---------------- RING I, the Threshold -------------------+
   |  hall/hearth --- maze --- fresco door --- gate room      |
   |  east cleft (cave) ... HOLE (9,0) ......................+-----+ drop
   |  cleft anchor  <------------------------- flowstone climb |     |
   +-----------------------------+-----------------------------+     |
                                 | stair (G lit)                     |
   +---------------- RING II, the Runner's Ring --------------+     |
   |  sun gate | moon gate --- Long Hall (scene C) --- heralds |<----+ the grotto
   |  Moon Room ... SUNKEN FLOOR ............................+-----+ drop
   |  ~ the trickle in the cleft (the stream begins) ~         |     |
   +-----------------------------+-----------------------------+     |
                                 | stair                             |
   +---------------- RING III, the Mysteries -----------------+     |
   |  webs (front way) | glow-marks (back way, doused)        |<----+ the web pocket
   |  ~~ the stream, surfable, north to south ~~               |
   |  front door --+   back door --+    HOLE in the webs ......+-----+ drop
   +---------------|---------------|---------------------------+     |
                   v               v                                 |
            DAEDALUS'S WORKSHOP (heal, Pithos, lift up)              |
                   | stair                                           |
   +---------------v-- RING IV, the Masks ---------------------+     |
   |  barracks, mess hall, posts --- Enkelados's checkpoint    |<----+ the Titans' dig
   |  the Titans' dig (cave) ~~ the stream ~~ CHUTE ...........+-----+ surf drop
   +-----------------------------+-----------------------------+     |
                                 | stair                             |
   +---------------- RING V, the Hunt (Labyrinth II) ----------+     |
   |  gallery --- Asterion's loop --- the LAKE (skylight pools)|<----+
   |  %1 ---> MINOS'S TOMB (the Helm)                          |
   +-----------------------------------------------------------+
           ... Ring VI (the forge; the stream falls past it), Ring VII, the heart
```

## The seams (warp ids)

Warp ids are each map's `warp_events` index. "Arrival" warps sit on a floor or a bronze ring: they are only landing spots (landing on a ring ties the thread, LABYRINTH §5.1).

| From | Cell | Goes to | Status |
|---|---|---|---|
| Grand Staircase (Knossa builder) | its way down | Ring I warp 0 (arrival on the threshold ring, (21,2)) | **Knossa builder:** please aim it here |
| Ring I warps 1-2 | the stair up (21-22,1) | `MAP_KNOSSA_PALACE_GRAND_STAIRCASE` warp 0 | falls back to Ring I warp 0 until the palace lands (`labyrinth_lib.dest`) |
| Ring I warp 3 | arrival on the gate ring (30,26) | — | Ring II's stair up lands here |
| Ring I warps 4-5 | the stair down (30-31,25), grated until G burns | Ring II warp 0 | |
| Ring I warp 6 | arrival on the cleft ring (38,6) | — | Ring II's flowstone climb lands here |
| Ring I hole (38,3) | coord event | Ring II warp 3 (the grotto) | one way |
| Ring II warp 0 | arrival on its entrance ring | — | |
| Ring II warps 1-2 | the stair up | Ring I warp 3 | |
| Ring II warp 3 | arrival in the grotto | — | from Ring I's hole |
| Ring II flowstone climb | coord event in the grotto | Ring I warp 6 | |
| Ring II warps 4-5 | the stair down | Ring III warp 0 | |
| Ring II warp 6 | arrival by its stair down | — | Ring III's stair up lands here |
| Ring II sunken floor | coord event in the Moon Room | Ring III warp 3 (the web pocket) | one way |
| Ring III warp 0 | arrival on its entrance ring | — | |
| Ring III warps 1-2 | the stair up | Ring II warp 6 | |
| Ring III warp 3 | arrival in the sealed web pocket | — | burn out from inside |
| Ring III front door / back door | warps | Workshop warps 0 / 1 | |
| Ring III warps (arrivals) | outside each door | — | the workshop's doors land here |
| Ring III hole | coord event in the webs | Ring IV warp 3 (the Titans' dig) | one way |
| Workshop warps 0 / 1 | front door / back door | Ring III's arrivals | |
| Workshop warps 2-3 | the stair down | Ring IV warp 0 | |
| Workshop lift | script, after scene D | Grand Staircase (Knossa builder: a landing warp by its stair) | falls back as above |
| Ring IV warps 4-5 | the stair down at Enkelados's checkpoint | **Ring V warp 0** (Labyrinth II: arrival on the gallery) | Labyrinth II to provide |
| Ring IV warp 6 | arrival by its stair down | — | **Ring V's stair up should land here** |
| Ring IV stream chute | coord event on the water | **Ring V warp 2** (Labyrinth II: arrival in the lake) | Labyrinth II to provide |
| Ring V's %1 breach (Labyrinth II) | warp | Minos's tomb warp 0 | Labyrinth II |
| Minos's tomb warp 0 | the door back | **Ring V warp 1** (arrival outside %1) | Labyrinth II to provide |

## Shared ids

- **Thread anchor names:** Labyrinth I uses `THREAD_ANCHOR_*` 10-29 (`include/constants/ichor.h`); Labyrinth II, please take 30 and up.
- **Braziers:** Labyrinth I uses `FLAG_ICHOR_BRAZIERS_START + 0x30`-`0x3F`.
- **Map section:** the rings show `MAPSEC_WATER_LABYRINTH`, renamed "LABYRINTH" (the FRLG section, unused by Ichor).
- **Map group:** `gMapGroup_Labyrinth`; add Labyrinth II's maps to it.
- **Tilesets:** `labyrinth` and `mychos` share the house (rows 0-12) and the rings' floor (rows 36-38) at the same metatile ids. `labyrinth` keeps its cave at rows 13-35; Rings I-IV, the tomb. `daidaleion` holds the workshop and **the Icarus Shaft** (the `dawn/` set), so Labyrinth II's `MAP_LABYRINTH_ICARUS_SHAFT` should use `gTileset_Daidaleion`.
- **The thread's floors:** the engine now takes eight (`MAX_FLOORS`), so a ring can register its slabs, cave earth, gravel, beams and plates together.

## The stream

A trickle in Ring II's cleft, a surfable stream across Ring III, a channel through Ring IV's dig that ends in a chute down to Ring V's lake, then falls past Ring VI's forge. Downstream is always a way deeper. The upper rings' water tables are in `tools/ichor/maps/labyrinth_encounters.py`.
