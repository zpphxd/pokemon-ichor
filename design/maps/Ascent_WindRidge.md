# Ascent_WindRidge, Boreas's ridge

Builder: `tools/ichor/maps/oros_maps.py` (`build_windridge`, aethos + gTileset_Oros, outdoor, `WEATHER_SNOW`).
New on 2026-11-18: the second outdoor snow floor, between the Glacier and the terraces above the cloud (3F).

- **Sentence:** out of the Glacier the mountain narrows to a wind-scoured ridge with cloud on both sides, climbing north in steps of bare rock and snow.
- **Land:** a spine over the cloud sea, cliffs with stairs cut into them, rocks poking through the scoured snow, a cloud span off the east flank.
- **Settlement logic:** the road-builders barred the ridge's last stair with bronze, worked by Herakles's kind of lock; storm rubble buried the drums.
- **Reveal:** the summit cone of Olympus rises out of the cloud to the north-east, white against the blue: the first time you see where you're going.
- **Signature:** the ridge itself, and the far peak.

## Plan (2026-11-18)

- **Puzzle: the Bellows of Boreas** (two relics, several steps). Storm rubble buries two drums (the Bronze Hammer breaks it); the drums go onto two plates on the ridge (the Girdle) to lift the bronze bar off the last stair. A lever by the bar resets the drums. The builder proves the pushes (`push_plan`); the test plays a wrong push and the reset first.
- **Shortcut back down:** above the bar, a snow ledge drops straight back to the ridge's foot.
- **Trainers:** Nephele (moved up from the Glacier) and a new pair on the narrow spine.
- **Post-game gate: the cloud bridge.** A span of cloud off the east flank toward Pegaunos's meadows (D11): "It looks solid. It isn't. Not yet." After the credits it firms a little, and hoofprints show.
- **Easter eggs:** Zeus's eagle on a crag, which flies off when you come close; Apollo's lyre humming in the wind through a split rock; Hermes's winged sandals left on a ledge (a Quick Claw).

## What's here (built 2026-11-18)

- **The Bellows of Boreas:** four storm rubble (the Bronze Hammer; each keeps a temp flag, so broken rubble stays broken until you leave), then two drums onto two plates (the Girdle; `push_plan` proves 19 pushes) lift the bronze bar off the last stair (`FLAG_ICHOR_WINDRIDGE_BAR_UP`). The lever rolls the drums back without reloading the map.
- **The cornice:** from the upper ridge a cornice drops one way down the east flank to the ridge's foot.
- **Trainers:** Nephele (moved up from the Glacier), Oreithyia and Kalais on the narrow spine (65–66). Wild 59–63.
- **Finds:** Full Restore, Hermes's sandals (a Quick Claw) on the east flank, hidden Comet Shard by the eagle's crag and Star Piece by the lyre rock.
- **Easter eggs:** Zeus's eagle on its crag, which flies off toward the summit when you come close; Apollo's lyre rock humming in the wind.
- **The far peak:** the summit cone of Olympus rises out of the cloud to the east.

## Hooks for later

- **The cloud bridge** (35,12) east toward Pegaunos's meadows (D11): "It looks solid. It isn't. Not yet." After the credits hoofprints show in it.

## Renders

- `img/ascent_windridge_after.png`, `img/ascent_windridge_after_screens.png`. New map, no before.
- Pass 1: the spine's face rows ate the plates' rows (the drums couldn't reach them), so the spine was raised under the upper ridge's face. Pass 2: inner-corner rims blocked the narrows; they are walkable now, and the drums start where they can be pushed. Pass 3: the cloud edges roughened, the seam rows to 3F kept to the two tilesets' shared terrain (`oros_lib.seam_check`).
