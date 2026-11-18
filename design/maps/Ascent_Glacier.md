# Ascent_Glacier, the river of ice

Builder: `tools/ichor/maps/oros_maps.py` (`build_glacier`, aethos + gTileset_Oros, outdoor, 44×62, `WEATHER_SNOW`). The cave-walled build on Chion (`ascent_glacier.py`) was retired on 2026-11-18.

- **Sentence:** out of the Icefall onto a river of ice with the Giants of the Gigantomachy frozen in it, climbing to the cloud line.
- **Land:** the foot and its narrows, a frozen lake, the court of the Gate of the Winds, the upper glacier under the storm face, a couloir, a frozen fall on the lip.
- **Settlement logic:** the road's builders sealed the way up with Herakles's kind of lock (drums on plates); shepherds and acolytes come up as far as the ice lets them.
- **Reveal:** two frozen Giants either side of the Gate, hands still raised; above them the white of the cloud.
- **Signature:** the Giants in the ice.

## What's here

- **The narrows' pair** (Niphon and Pholoe, no way round); Nephele waits on the upper glacier. Wild 58–62: Pagoshard's first wild home, with Chionyad, Borapteryx, Krystolos, Stygiad at night.
- **The frozen lake:** an ice slide to the way up, and a second slide to TM Ice Beam's pocket.
- **The Gate of the Winds:** three drums onto three plates (`push_plan()` proves it, 21 pushes), a reset lever that puts all three back (the test pushes one wrong first, then resets).
- **New relic puzzles (2026-11-18), on the upper glacier:**
  - **Daedalus's Wings:** an updraft at the west edge carries the player over a gap of wind to the eyrie (Choice Scarf, hidden Comet Shard) and back.
  - **Ariadne's Thread:** a crevasse mouth to tie off and climb down into the Crystal Vault's crack ledge.
- Finds: TM Ice Beam, Focus Sash, Max Revive, hidden Big Nugget and Star Piece. **Shrine:** Hephaestus's stele, fragment IV.

## Hooks for later

- **The storm face** (8,20): handholds too far apart for hands, thunder before the light: Pan's Crook up to Olympus's storm terrace (the colossi, POSTGAME §3.4).
- **The couloir's great boulder** (35,23): Hephaestus's Hammer; bronze glints beyond.
- **The frozen fall** (33,4): "runs again once the mountain has a new master": the post-game thaw.
- **The cloud line** at the top edge leads on to 3F and, beyond it, Pegaunos's meadows (D11).

## Renders

- Before: `img/ascent_glacier_before.png`. After: `img/ascent_glacier_after.png`.
- Pass 1 stepped the court's north wall (the 21-cell straight edge was `map_style_audit`'s only FAIL). Pass 2 cut the eyrie off the west edge and placed the crevasse by the Focus Sash's corner, so both read from the main path. Pass 3 checked the gate's push answer is unchanged and the eyrie can't be walked to.

## Plan (2026-11-18 rework, outdoor on gTileset_Oros)

Rebuilt as an outdoor glacier valley: snow levels and real cliffs instead of cave walls, firs on the foot, the lake a frozen tarn under the cliffs, the court on its own shelf behind the Gate of the Winds, snowfall.

- **Puzzles (the third step):** the frozen lake (two slides: the way up and the TM's pocket); the Gate of the Winds, three drums onto three plates, with its reset lever; the Wings' updraft to the eyrie; Ariadne's Thread down the crevasse into the Crystal Vault. All kept, on the new layout, with every answer re-proved by the builder.
- **Shortcut back down:** past the Gate, a snow chute (a one-way ledge) drops back to the foot by the Icefall's mouth.
- **Post-game gates:** the storm face (Pan's Crook), the couloir's great boulder (Hephaestus's Hammer), the frozen fall (thaws after the credits; its line changes).
- **Easter eggs:** **Hera's peacock feather** in the snow (a hidden Pretty Feather: "one eye on it, watching"); **Ares's broken shield** half-buried at the narrows ("the boar on it is the one he lost to Herakles; he never came back for it"); **Poseidon's trident mark**, three prongs split into a boulder ("someone lost his temper with the mountain").

## Built (2026-11-18)

- **Outdoors on gTileset_Oros:** four-row cliffs with stairs cut into them between the foot, the lake's shelf, the court and the upper glacier; firs on the foot, snowfall, the cloud sea either side.
- **The main ice puzzle, the frozen lake** (medium-hard): one way onto the ice (x 21), the stair to the court the only landing, snow patches and ice boulders as stops. The builder's solver (`oros_maps.ice_report`) proves a 6-slide answer (8 key presses), 16 dead ends (resting places further from the stair than the shore is, so you must come back), the TM Ice Beam's islet as a 4-slide side answer, and that nothing strands you. The shore is the reset. `ascent.sh` slides into a dead end, back to the shore, then solves it.
- **The Gate of the Winds** (18 pushes), the reset lever, the Wings' eyrie (west, across the gap of wind), Ariadne's Thread down the crevasse, as before.
- **The chute:** a cornice from the upper glacier's east end drops one way down the east corridor to the foot.
- **Eggs:** Hera's peacock feather (hidden Pretty Feather), Ares's broken shield (hidden Hard Stone), Poseidon's trident rock, the Giants in the ice.
- **Post-game:** the storm face, the couloir's boulder and the frozen fall each change their line after the credits.
- Renders: before `img/ascent_glacier_before.png` (the cave-walled build), after `img/ascent_glacier_after.png`, screens `img/ascent_glacier_after_screens.png`. Pass 1 laid the levels and the lake; pass 2 moved the narrows' pair onto the stair's row so they can't be walked past, and the updraft off the storm crag's face; pass 3 Gen 3 ice (bold light bands, ice boulders) after Emerald's Shoal Cave (`img/oros_vs_shoal.png`) and roughened edges.
