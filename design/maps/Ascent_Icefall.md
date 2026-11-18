# Ascent_Icefall, the ice caves behind the frozen fall

Builder: `tools/ichor/maps/ascent_snow.py` (gTileset_Chion, cave style, 42×46).

- **Sentence:** the mule road goes into the mountain behind a waterfall that froze, and the floor turns to ice.
- **Land:** blue ice caves: a great slide hall of slick ice (`MB_ICE`), a guarded gut, a drum room, a crystal garden off to the east.
- **Settlement logic:** the road's builders cut steps where they could and set a bronze grate where they couldn't; Hestia's stele stands by the way in, the first warm thing on the floor.
- **Reveal:** the slide hall opens wide and white the moment you step on it, and you don't stop till something stops you.
- **Signature:** the slide hall, with crystals and pillars as its only brakes.

## What's here

- **Ice sliding:** the slide hall carries the player to the gut (the builder proves the slide and refuses a field that can strand anyone; `slide_plan()`).
- **The gut's pair:** Chione and Arktos, on a chokepoint you can't walk round; Boreades in the upper hall. Wild 57–61: Borapteryx, Chionyad, Krystolos, Niflake, Kryopuff, Stygiad at night; Pagoshard and Krystolos in the rocks.
- **The Girdle seal:** one drum onto one plate raises the grate (`FLAG_ICHOR_ICEFALL_GRATE_OPEN`), with a reset lever.
- **Relics:** the Girdle (the drum), the Bronze Hammer (rubble), the Labrys (the chained door to the Crystal Vault), Hecate's Torch (the ladder down into the dark Deep).
- **Finds:** TM Blizzard (crystal garden), Never-Melt Ice, Max Elixir, hidden Ice Stone and Nugget.
- **Shrine:** Hestia's stele, fragment III of the hymn.

## Hooks for later

- **The frozen fall** at (23,36): "something glints behind the ice, high up." It thaws for the post-game (with the Glacier's fall), opening the ledge above.

## Renders

No changes in the 2026-11-18 pass; `img/ascent_icefall_after.png`.

## Plan (2026-11-18 rework)

- **Puzzle:** the slide hall and the one-drum seal, as before (the second step up in difficulty). The way in is now from the snowfield's cliff mouth.
- **Easter eggs:** **Hephaestus's forgotten hammer** stuck in the ice of the drum room (a hidden Hard Stone: "the haft is warm. It shouldn't be"); **Boreas's breath** frozen in the upper hall's frost (an inspect: the frost on the wall has the shape of a face, cheeks puffed).
- **Post-game gate:** the frozen fall at (23,36). After the credits its line changes: water can be heard running behind the ice.
