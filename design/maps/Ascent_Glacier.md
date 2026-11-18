# Ascent_Glacier, the river of ice

Builder: `tools/ichor/maps/ascent_glacier.py` (`build_glacier`, gTileset_Chion glacier style, 44×58, `WEATHER_SNOW`).

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
