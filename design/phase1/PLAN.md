# Phase 1: Kalliste Isle vertical slice

**Goal.** About an hour of play, from a new game to Laurel 1, built from Ichor's own maps, art, music and story.
- The user playtests it and approves the look before we scale up.
- It covers Act I, steps 1–2 of `design/PITCH.md`. Read that first.
- Where this plan and the bible disagree, the bible wins. Raise the conflict with the director.

## Story beats

| # | Where | Beat |
|---|---|---|
| 0 | Intro | Professor Daphne replaces Birch's new-game speech ("every myth is a memory of a Pokémon"). The player picks Theo or Ianthe, then a name. |
| 1 | Elaia Village, player's house | Morning of the island's coming-of-age festival. Your mother sends you to the Akademia grove. |
| 2 | Elaia, festival square | The island priestess reads each youth's thread. She cannot read yours; it is blank. Keep it subtle: foreshadowing, not exposition. |
| 3 | Akademia grove | Meet Daphne and Alethea, and choose **Snivy, Cyndaquil or Piplup**. Daphne gives you the Pokédex. |
| 4 | Elaia | Kleon is visiting with the Lakonian delegation for the festival games. He takes the starter strong against yours. First rival battle; losing does not end the game. |
| 5 | Route 1, north to Akti | Trainers and tall grass. At the hilltop ruins, Team Titan grunts are digging for a fragment of the Harpe. Alethea is there. You win two grunt battles and the grunts flee empty-handed, leaving a clue. |
| 6 | Akti Town | A fishing harbor with an Asclepeion, an Agora stall and the Temple of Hestia. |
| 7 | Temple of Hestia | The hearth trial is a short puzzle with acolyte trainers. Beat Hierophant **Ione, the Hearthkeeper** (Normal) for the **Hearth Laurel**, Laurel 1. |
| 8 | Akti harbor | The trireme to the mainland "sails when the winds turn": a clean end to the slice and a hook for Phase 2. |

## Maps

| Map | Start from | Tilesets |
|---|---|---|
| Elaia Village | Littleroot Town layout (20×20), reworked | aethos + kalliste |
| Route 1, with the hilltop ruins | Route 101 layout, lengthened, with a ruins spur | aethos + kalliste |
| Akti Town | a new harbor layout, about 28×24 | aethos + kalliste |
| Player's house 1F and 2F | Brendan's house layouts | reused for now |
| Akademia (Daphne's grove hall) | Birch's lab layout | reused for now |
| Akti Asclepeion | Pokémon Center layouts | reused for now |
| Akti Agora | Mart layout | reused for now |
| Temple of Hestia | new layout | building + temple_hestia |
| 2–3 NPC houses | Hoenn house layouts | reused for now |

Interiors marked "reused for now" get a Greek repaint after the look is approved.

New maps get their own `MAP_` names. Hoenn maps are left alone during the slice and removed later to free ROM.

## Art direction

**Master palette.** These are the RGB values for the slice. Every value is a multiple of 8 so it maps exactly to GBA BGR555. Stay within these families so all the art reads as one world.

| Family | Shades, dark → light |
|---|---|
| Aegean blue | (24,56,120) (48,104,176) (112,168,224) (176,216,240) |
| Marble | (168,160,152) (216,208,192) (248,248,240) |
| Olive | (56,72,32) (96,112,48) (144,160,72) (168,184,136) silver leaf |
| Cypress | (24,56,40) (40,88,56) |
| Terracotta | (120,48,24) (184,88,48) (224,136,88) |
| Sun-gold | (200,144,40) (240,192,64) |
| Limestone path | (176,144,96) (208,184,136) (232,216,176) |
| Black-figure ink | (32,24,24) |

**The world.**
- Kalliste is Cycladic:
  - whitewashed cube houses with Aegean-blue doors and shutters, and blue domes on sacred buildings
  - low dry-stone walls and pale limestone paths
  - gnarled olive trees (gray-brown trunks, silver-green canopy) and dark cypress spires
  - sun-bleached grass
- Sacred buildings use Doric marble columns, pediments, bronze braziers and a central hearth.

**Pixel style.**
- Gen 3 readability: 16×16 metatiles and light from the top left.
- Objects get 1 px dark outlines; terrain does not.
- Dither sparingly.
- 4bpp art, color 0 transparent, at most 15 colors per 8×8 tile.

**The pottery UI.**
- Terracotta fields with black-figure ink.
- Greek key (meander) borders on the dialogue box and menus.

## Workstreams and file ownership

Agents work in their own git worktrees and commit on their branch. The director merges. Touch only the files you own. If you need a change elsewhere, ask in your report.

| Stream | Owns | Delivers |
|---|---|---|
| Narrative | `design/phase1/SCRIPT.md` | Every scene's dialogue, NPCs per map, trainers and teams, the Route 1 encounter table, and the temple puzzle |
| Tilesets | `data/tilesets/primary/aethos/`, `data/tilesets/secondary/kalliste/` and `temple_hestia/`, the Porytiles management files, `src/data/tilesets/*`, `tools/ichor/render_map.py`, `tools/ichor/art/` | The Greek tilesets, plus a map renderer for checking art and maps |
| Music | the new `sound/songs/midi/mus_ichor_*` files and their registration, `tools/ichor/music/` | 3 songs: the Elaia Village theme, the Route 1 theme, and the battle theme for Kleon and Ione |
| UI | `graphics/text_window/` and its palettes, `tools/ichor/art/ui_*` | Pottery dialogue box and menu frames |
| Sprites | new files in `graphics/trainers/` and `graphics/object_events/pics/people/`, and their tables | The cast: Theo, Ianthe, Daphne, Alethea, Kleon, Ione and Titan grunts |
| Engine, maps and scripts | the director, then map and script agents | Starters, new-game flow, maps, events and scripts |

## Done means

- A new game plays from Daphne's intro to the Hearth Laurel without entering a Hoenn map.
- `make` is green, `tools/ichor/smoke_test.sh` passes, and the smoke test covers the slice's opening.
- Ichor's new content stays well inside the ROM's 5 MB of headroom.
- There is a screenshot gallery of every map and the key scenes for the user's look review.
