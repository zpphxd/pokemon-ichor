# Ascent_Snowfield, the Leuke snowfield

Builder: `tools/ichor/maps/oros_maps.py` (`build_snowfield`, aethos + gTileset_Oros, outdoor, `WEATHER_SNOW`).
New on 2026-11-18: the climb's first outdoor snow floor, between the cloud ledges (2F) and the Icefall.

- **Sentence:** above the cloud ledges the trees give up one by one; the old road wades through deep snow past snow-laden firs to a frozen tarn under the Icefall's cliff.
- **Land:** three snow levels. The lower meadow (firs, drifts, a forced band of deep snow), a cliff with a stair cut into it, the tarn's shelf, then the high cliff where the Icefall's mouth opens.
- **Settlement logic:** muleteers stop at the treeline; the Archon's road-builders cut the stair and roped off the cave they couldn't make safe.
- **Reveal:** at the top of the cut stair the whole tarn opens out, flat and shining, the Icefall's cliff behind it.
- **Signature:** the Mirror Tarn, its rocks standing up through the ice.

## Plan (2026-11-18)

- **Puzzle: the Mirror Tarn** (ice slide). The only way from the stair to the Icefall's mouth is across the frozen tarn; rocks poke through the ice, and you must stop on the right one. The builder proves the answer (`slide_plan`) and that the ice can never strand you (`check_no_strand`). A second slide reaches the islet's find.
- **Shortcut back down:** past the tarn, a snow cornice ledge drops one way to the arrival meadow, so a defeat never means re-crossing the ice.
- **Trainers:** a pair on the deep-snow band below the cut stair (no way round); wild 56–60 in the deep snow.
- **Post-game gates:**
  - **The roped cave**, an icy mouth in the west cliff: "CLOSED BY ORDER OF THE ARCHON." After the credits the rope is gone, but the way stays dark (a road for later).
  - **The bronze door of the Twelve**, set in the east cliff: twelve marks round a keyhole. It doesn't move now.
- **Easter eggs:** Artemis's silver arrow in a fir (a Scope Lens at its foot); Demeter's poppy blooming in the snow; Sisyphus's boulder at the meadow's foot, which rolls back whenever you push it.

## What's here (built 2026-11-18)

- **The Mirror Tarn**, the warm-up ice puzzle: one way onto the ice from the south shore (x 20), three cells of landing under the Icefall's mouth, ice boulders placed by a search for a 4–6-slide answer with dead ends (`oros_maps.search_ice`, proven by `ice_report`: the fewest slides, the dead ends, and that no resting place strands you). Walking off the ice onto the shore is the reset.
- **The cornice:** from the mouth's path east, a snow cornice drops one way into the east corridor and the meadow (the builder asserts it is one way).
- **Trainers:** Leukippos and Theonoe at the cut stair's foot (62–63). Wild 56–60 in the deep snow.
- **Finds:** Max Elixir (the mouth's path), a Herakles Ball (the east corridor), hidden Never-Melt Ice and the Scope Lens at Artemis's fir.
- **Easter eggs:** Artemis's silver arrow in a fir; Demeter's poppy in the snow; Dionysus's wine-stained drift; Sisyphus's boulder at the meadow's foot ("It goes up a step, and another, and then it rolls right back").
- **Mixed by altitude:** alpine grass and wildflowers show through patchy snow on the meadow's foot, thinning as you climb; the cloud sea falls away to the east, with Olympus's summit cone far off in it.

## Hooks for later

- **The roped cave** (6,40) in the knoll: "CLOSED BY ORDER OF THE ARCHON"; after the credits the rope is gone (`FLAG_SYS_GAME_CLEAR`), the cave still dark: a post-game road.
- **The bronze door of the Twelve** (12,31) in the shelf's cliff: twelve marks round a keyhole; after the credits Hestia's mark warms (the post-game's twelve keys).

## Renders

- `img/ascent_snowfield_after.png`, 15x10 screens `img/ascent_snowfield_after_screens.png`. New map, no before.
- Pass 1: the cliffs read as fences (regular vertical strata) and the deep snow as cobbles; the faces were redrawn as craggy masses lit from the upper left and the deep snow as soft white heaps. Pass 2: one-level drops looked like walls, so every cliff became a two-level, four-row face; the tarn's north shore was closed with rocks so a straight slide can't solve it. Pass 3: packed-snow paths with soft fringes, alpine grass at the foot, the cloud edges roughened so no edge runs straight.
