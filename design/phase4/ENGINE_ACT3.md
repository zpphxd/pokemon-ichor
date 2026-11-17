# Act III engine: what's built

The engine pieces SCRIPT.md Part 11 asks for that are built so far, with their exact contracts. Map and script writers build against these. Every engine edit outside the new files is a few lines marked `// Ichor:`.

| Need | API | Files | Check |
|---|---|---|---|
| — | Aethos species stand-ins | `include/constants/ichor_species_stubs_act3.h` | the build |
| E7 | `special Ichor_BullLeap` | `src/ichor_bull_leap.c` | `tools/ichor/tests/ichor_bull_leap.sh` |
| E8 | `MOVEMENT_TYPE_ICHOR_STATUE`, `_ROOTED`, `MOVEMENT_TYPE_ICHOR_MIRROR` | `src/ichor_statue.c` | `tools/ichor/tests/ichor_statues.sh` |
| E9 | `special Ichor_TraceBeam` | `src/ichor_beam.c` | `tools/ichor/tests/ichor_beam.sh` |

## Aethos species stand-ins

`include/constants/ichor_species_stubs_act3.h` gives every one of the 152 Aethos species a `SPECIES_<NAME>` constant, so `trainers.party` (`Aphrell` becomes `SPECIES_APHRELL`), the wild tables, `givemon` and `OBJ_EVENT_GFX_SPECIES()` build today.

- Each name maps to a vanilla species of the same or the closest types, with a similar stage and base-stat total. Each line's comment gives the Aethos species' own types and myth. No vanilla species stands in for two Aethos ones.
- The 43 species that world-act1's `constants/ichor_species_stubs.h` covers use its exact stand-ins. Every name is guarded on its own, so the two files coexist in either include order.
- The legendaries are vanilla legendaries: the Fates are the lake trio (Nemira the Spinner is Mesprit, Lotira the Measurer is Uxie, Thanira the Cutter is Azelf), Kronolith is Dialga, Kairazor (the Moment) is Lugia, Pegaunos is Zapdos, and the three brothers are Raikou, Suicune and Spectrier.
- When the dex lands, define `ICHOR_AETHOS_DEX` or delete the file and its include at the end of `include/constants/species.h`.

## E8: marble statues and bronze mirrors

**Movement types.** Each comes in four facings; the suffix is the starting facing, and no suffix is down. All of them hold still like `MOVEMENT_TYPE_FACE_*`, and Porymap lists them with the rest.

| Type | What it is |
|---|---|
| `MOVEMENT_TYPE_ICHOR_STATUE` (`_UP`, `_LEFT`, `_RIGHT`) | A statue that walks while unwatched (Galatea's Gallery). |
| `MOVEMENT_TYPE_ICHOR_STATUE_ROOTED` (`_UP`, `_LEFT`, `_RIGHT`) | A statue that only turns (Melos). |
| `MOVEMENT_TYPE_ICHOR_MIRROR` (`_UP`, `_LEFT`, `_RIGHT`) | A bronze mirror. Its facing is its angle. A wall mirror and a mirror on a stand are the same thing. |

**On each step.** On each step the player takes under their own control, every statue on screen that the player can't see does this:
- A **walking statue** steps one tile toward the player. It goes along the longer axis, or along the other axis if that tile is blocked; on a diagonal tie it goes east or west first. It doesn't walk: it is simply one tile nearer, with `SE_M_STRENGTH` once per step however many statues move. The usual collision rules apply, and the template's movement range, if set, keeps a statue within that many tiles of its plinth.
- A **rooted statue** never moves.
- Either kind then turns to face the player.

Statues don't move when the player turns on the spot, during scripts (a trainer walking up, `applymovement`), on forced-movement tiles, or in battle. Statues off screen aren't spawned, so they don't move. A statue that leaves the screen respawns on its plinth.

**Watched.** The player watches every statue on the line of tiles straight ahead, from the tile next to them. Statues on the line don't block it. The line:
- turns at a **mirror's face**: it leaves the mirror going the way the mirror faces. A mirror facing the player head-on sends it straight back past them, so a wall mirror shows what's behind you. A mirror seen from the side sends it round the corner;
- stops at a **mirror's back** (the line travelling the way the mirror faces);
- stops at anyone else (a person, any other object), at an impassable tile, and at the map's edge;
- runs at most 32 tiles and turns at most 4 times.

The player and any follower don't block it. Off-screen mirrors count, at their templates' places and facings.

**The touch.** A walking statue that is unwatched and ends the step on a tile next to the player turns to face them and touches them: **its own object script runs**. The script runs with `VAR_LAST_TALKED` set to the statue's local id and `VAR_FACING` set to `DIR_NONE`. A talk always sets a real direction, so the same script can tell a touch from the player pressing A on the statue:

```
script Gallery_EventScript_Statue {
    if (var(VAR_FACING) == DIR_NONE) {          // a touch
        lockall
        msgbox(format("A cold marble hand rests on your shoulder.\p…You're back at the door."))
        warpsilent(MAP_GALLERY, 12, 30)         // the room's door (an example): statues respawn on their plinths
        waitstate
    } else {
        msgbox(format("A marble youth. His eyes are blank, and on you."), MSGBOX_SIGN)
    }
}
```

A warp, even to the same map, respawns every statue from its template. To reset only one room, use `setobjectxy` on that room's statues.

**Turning a mirror.** It's a script: `turnobject LOCALID, DIR_*`. That turn lasts while the mirror is on screen. To make it survive the mirror leaving the screen, also run `setobjectmovementtype LOCALID, MOVEMENT_TYPE_ICHOR_MIRROR_<DIR>`. To keep it across visits (Galatea's P2 and P3), set the movement type from your saved facing in `ON_TRANSITION`.

**After the Laurel,** give the statues a plain `MOVEMENT_TYPE_FACE_*` with `setobjectmovementtype` in `ON_TRANSITION`.

**Not in the engine:** the BGM's one-beat stop when a statue moves (SCRIPT.md Part 5), the stone SE choice beyond `SE_M_STRENGTH`, and the statues' art.

**Files:**
- `src/ichor_statue.c`, `include/ichor_statue.h`.
- The step hook in `ProcessPlayerFieldInput` (`src/field_control_avatar.c`), after trainers' sight and before coord triggers.
- The types in `include/constants/event_object_movement.h` and `src/event_object_movement.c`'s two tables.

## E7: the bull-leap timing special

```
setvar VAR_0x8004, LOCALID_GENTLE_BULL     // the object that charges, on this map
setvar VAR_0x8005, ICHOR_TILE(10, 6)       // the line's tile: x | (y << 8), map coordinates
setvar VAR_0x8006, 10                      // the window in frames (0: 10, Hero)
setvar VAR_0x8007, 6                       // frames per tile (0: 6, Hero)
special Ichor_BullLeap                     // waits by itself (no waitstate needed)
// VAR_RESULT: ICHOR_LEAP_EARLY 0, ICHOR_LEAP_CLEAN 1, ICHOR_LEAP_LATE 2
```

**Behavior:**
- The object charges one tile per `VAR_0x8007` frames toward the line's tile, along the longer axis first, and stops on the line. Nothing it crosses is checked for collision; the lane is the map's job.
- The **window** opens on the frame the object's step onto the line's tile begins, as its head crosses the line. It lasts `VAR_0x8006` frames. On a lane of N tiles that is frame (N − 1) × speed of the special.
- **A** before the window opens is early. A inside the window is clean. No A by the end of the window is late.
- Once the result is known, the object finishes the tile it is crossing, so an early leap leaves it mid-lane and the others leave it on the line. Then the script goes on.

It never moves the player. The vault (the player's `jump_2` with four facings mid-air), the knock-down fade and the bull trotting back are the script's.

There is no difficulty setting in the engine yet, so the speed and window are parameters. LABYRINTH §3's table:

| | Mortal | Hero | Spartan |
|---|---|---|---|
| `VAR_0x8007` (frames per tile) | 8 | 6 | 5 |
| `VAR_0x8006` (window) | 14 | 10 | 6 |

"After each miss the window grows by 2 frames, up to double" is the script's: keep the window in a temp var and pass it each try. The Moment on the Stair of Hours uses the same special: the object is the Moment and the line is the painted line.

**Files:** `src/ichor_bull_leap.c`, `include/ichor_bull_leap.h`, `include/constants/ichor_act3.h` (included in `data/event_scripts.s`), and `data/specials.inc`.

## E9: the beam trace

```
setvar VAR_0x8004, LOCALID_APOLLO_M2       // the source: the object the light comes from
setvar VAR_0x8005, METATILE_Delphoi_BeamEW // the first of the six beam metatiles
special Ichor_TraceBeam
// VAR_RESULT: the local id of the object the beam ended on, or 0
// VAR_0x8006, VAR_0x8007: the tile it ended on (map coordinates)
```

**Sources and targets are object events:**
- The **source** is any object on the map, named by its local id. The beam leaves the source's tile going the way the source faces. Usually it is the mirror the shaft of light falls on, so turning that mirror aims the beam. A fixed light (a window, a lamp) is any object facing the way the light goes.
- **Mirrors** are `MOVEMENT_TYPE_ICHOR_MIRROR*` objects, as for the statues.
- A **target** is whatever object the beam ends on: a crystal, a brazier, or an invisible marker object on a disc's tile in the wall. The script compares `VAR_RESULT` with the target's `LOCALID_*`. A disc that is only a metatile can be checked by `VAR_0x8006`/`VAR_0x8007` instead.

**The path:**
- The beam runs tile by tile from the source.
- At a mirror it turns the way the mirror faces. A mirror facing it head-on, or showing it its back, ends it there, with `VAR_RESULT` the mirror's id.
- Any other object ends it on that object.
- An impassable tile (a wall, a shut door, a screen, the serpent pillar) or the map's edge ends it with `VAR_RESULT` 0.
- The player and followers don't block it.
- At most 128 tiles and 16 mirrors.
- Off-screen objects count, at their templates' places and facings.

**The metatiles.** The floor it crosses becomes beam metatiles. Each keeps its tile's collision and elevation. They are six consecutive metatiles from `VAR_0x8005`:

| + | Piece |
|---|---|
| 0 | east–west |
| 1 | north–south |
| 2 | corner joining the tile's north and east sides |
| 3 | corner, north and west |
| 4 | corner, south and east |
| 5 | corner, south and west |

The corner goes under the mirror the beam turns at; the source's own tile is left alone. The delphoi tileset isn't drawn yet, so pass placeholder ids until it is. The special redraws the map itself (`DrawWholeMapView`).

**Re-tracing.** Tracing a source again first puts back the floor its last beam covered: turn a mirror, then trace. It restores only tiles that still show a beam metatile, so a map that was left and entered again is safe. The engine remembers two beams at once (two sources per map). Beams shouldn't cross each other.

Night's moonbeam is a palette swap of the same metatiles (the map's). Discs, doors and their flags are the script's, after the trace.

**Files:** `src/ichor_beam.c`, `include/ichor_beam.h`, `data/specials.inc`.

## Tests

Each check runs on the Lua headless runner, in the Akti Agora. It rebuilds the map's three objects from rewritten templates and lays a plain floor in the live map grid (`tools/ichor/tests/act3_lib.lua`, `act3_setup.s`, `act3_consts.c`), so nothing in the ROM is patched and no debug content ships.

```bash
tools/ichor/tests/ichor_statues.sh     # a wall mirror watching, a mirror's back, facing directly,
                                       # a rooted statue, a person blocking, the touch script
tools/ichor/tests/ichor_bull_leap.sh   # A at fixed frames: early, just early, clean, late, Mortal, defaults
tools/ichor/tests/ichor_beam.sh        # trace, turn, re-trace: target, edge, back, head-on, the old path restored
```
