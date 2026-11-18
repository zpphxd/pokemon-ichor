# The Nursery of Nysa (Route 7)

The day care. The nymphs of Nysa raised the infant Dionysus; Aristaios carried him to them. Built by `tools/ichor/maps/kopais.py` (the farmhouse and glade on Route 7) and `tools/ichor/maps/kapeleia_rooms.py` (the room, `MAP_ROUTE7_NURSERY_OF_NYSA`, 14x9, on `gTileset_Nysa`). Brief: design/IDEAS.md, "Day care: the Nursery of Nysa".

## Where

Route 7 is 14 columns wider (44x36). East of Thyrsa's south gate a lane runs under the olives to a whitewashed farmhouse (aethos's farmhouse, widened to seven; door (35,3), Route 7's warp 0) with its sign. Below the field wall, through steps at (37,6), is the glade: flowers, the beekeeper's hives, and the two Pokémon left at the nursery roaming it. Below the glade, long grass (Route 7's wild table) keeps the route at 16 grass cells a screen.

## How it works

- **Makris** (the nymph who fed the god honey) behind her counter takes one or two Pokémon (`chooseboxmon`), reports levels gained, and returns them for the usual fee: Emerald's day-care woman's script, in Ichor's words. The expansion's `src/daycare.c` does the rest (EXP per step, Eggs), with Hera's hooks untouched: Queen's Care doubles the egg chance (`Ichor_ModifyEggChance`) and hatches faster (`Ichor_ExtraEggCycles`).
- **Aristaios**, at the end of the lane over the glade, hands over Eggs (the day-care man's script).
- **The glade.** Route 7's `ON_TRANSITION` calls `Ichor_SetNurseryYardMons` (`src/ichor_nursery.c`): each deposited Pokémon's overworld sprite, shiny and female forms kept, goes in `VAR_OBJ_GFX_ID_0/1`, which the two wandering yard objects use; an empty slot's object hides on `FLAG_TEMP_1/2`. Talking to one names it.
- Inside: Bromie explains Eggs, a Melibee hums by the honey, the liknon (the god's winnowing-basket cradle) holds an Egg.

## Passes

Renders: `img/route7_nursery_before.png`, `img/route7_nursery_after.png` (with `_walk`, `_views`); the room `img/nursery_of_nysa_pass1.png`, `_pass2.png`, `_after.png`; in game, `img/nysa_deigma_ingame.png`.

1. **Pass 1.** The farmhouse one row down in the olives, the lane to x 41, the glade bare. Critique: a row of boulders above the roof and a single column of them beside it (olive leftovers), the lane cut off behind Aristaios, the glade indistinguishable from the woods round it. In the room, the keeper's counter floated mid-floor with nothing behind her, and the walls were bare.
2. **Pass 2.** Farmhouse to the top row and one column west, cypresses at its east side, the lane ends at Aristaios, flowers and hives in the glade. The room: the keeper's counter against the wall between jar shelves and a window, the loom, herbs, ivy, the cradle corner. Critique: Route 7's widened screens fell to 11 grass cells a screen (map_audit FAIL), the field wall now ran 24 cells unbroken (map_style_audit FAIL); in the room the cradle corner and the middle floor were still empty.
3. **Pass 3.** A pine breaks the wall where the old field ends; the long grass below the glade. The room: a blue rug under the cradle corner, a table with pots, a stool. After: map_audit 16 grass/screen; map_style_audit WARN (17-cell edge, as before the change).
