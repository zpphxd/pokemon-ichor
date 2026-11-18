# Olympus_Summit, the altar above the cloud

Builder: `tools/ichor/maps/ascent_peak.py` (gTileset_Chion, 28×26), run by `ascent_snow.py --only summit`. Scripts are hand-written (`data/maps/Olympus_Summit/scripts.pory`). Moved off Aegina on 2026-11-18: the old build drew the top of the world as a green meadow, which the cloud-break and summit-view scenes contradicted.

- **Sentence:** up the last stair out of the Pantheon onto the bare summit: Zeus's great ash altar under an open sky, the temple of the Twelve behind it, and the sea of cloud on every side.
- **Land:** a snowfield plateau, its rim stepping down to cloud; the cone's last crag in the north-west; a strait of cloud to the east with a meadow floating beyond it.
- **Settlement logic:** the temple faces east with its altar in front, where the rites happen (STYLE §4.5); the Archon waits at the altar, not inside; every Archon since Medon has a stele on the west terrace.
- **Reveal:** the stair ends on the sacred way, and the altar and the temple stand whole above it (the summit-view camera pans west, east and back).
- **Signature:** the altar with the bronze box, and the temple of the Twelve against the sky.

## What's here

- New Chion pieces (`tools/ichor/art/chion_props.py`, `summit_props()`): **`altar_zeus`** (4×2: horned corners, ash, the box) and **`temple_twelve`** (7×5: an Ionic porch, a red frieze of the Twelve enthroned in gold, an eagle with the thunderbolt in the pediment, fire in the cella). They pack into Chion's empty rows 28–37, so no earlier metatile moved (493 of 504 tiles).
- **The Archon** at (13,13): the story's peak (the box, the confession, thunder out of a clear sky, `MUS_VS_CHAMPION`), then Medon's Knot and the Hall of Heroes. Coordinates kept from the old build, so the scripts and `league.sh` are unchanged.
- **The Archons' stelai:** Aristeides's name is the last cut; the next stone is blank, "waiting for yours" once he's beaten.

## Hooks for later

- **The crag** (7,6): Pan's Crook handholds up the cone's true top, a throne-shaped stone against the sky: the way to the Prime Mover's summit (Arceus).
- **Pegaunos's meadow** (east, across the strait of cloud): a winged thing grazing; no stair reaches it (D11, OIKOUMENE_GUIDE §15).

## Renders

- Before (Aegina): `img/olympus_summit_before.png`. Passes: `img/olympus_summit_pass1.png`, `img/olympus_summit_pass2.png`. After: `img/olympus_summit_after.png`.
- Pass 1: the temple and altar read at once, but the crag was a ragged patch, the meadow merged into the plateau, and the top edge ran straight to the map's rim. Pass 2 stepped the rim, cut a strait of cloud so the meadow floats, and made the crag a stepped mass with a face for the handholds. Pass 3 filled the empty west terrace with the Archons' stelai.

## Plan (2026-11-18 rework)

- **Easter eggs:** **Ganymede's cup** left on the altar step ("still half full. Of what, you'd rather not ask"); **the eagle's feather** on the crag's foot, the Pegaunos and Prime Mover hooks as before.
