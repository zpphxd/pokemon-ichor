# The Oikoumene chart

- **Owner:** the chart agent, batch 1 (`design/oikoumene/BUILD.md` §5).
- **What this is:** how the Oikoumene's region map, its sections, its fly targets and the engine around them were built, the hidden-section audit, and the chart's critique passes.
- **Renders:** `img/chart.png` (2x), `img/chart_grid.png` (every section code on its cell), `img/popups.png` (the three new map-name stones).

## Stopped at

Work stopped on 2026-11-14 at the coordinator's request (usage limit; the main story comes first). Last commit: the WIP commit on this branch, `feat(engine): WIP the Oikoumene chart…`.

**Done, and tested in game** (`tools/ichor/tests/oikoumene_chart.sh`: 23 checks, all passing on the build before the WIP commit):
- `REGION_OIKOUMENE` is `REGION_KANTO`; `IsOikoumeneMapSec` / `GetRegionForSectionId` read ids 0–85 (less the kept Battle Frontier, 58) and the Kanto tail (`MAPSEC_CATARACTS`–`MAPSEC_SELVAGE`) as the Oikoumene. `GetKantoSubregion` returns the main subregion outside FRLG, so nothing lands on a Sevii chart. The FRLG branch is intact.
- The Fly map, wall map and Pokédex area view load the Oikoumene art in the Oikoumene (`gRegionMapInfos[REGION_MAP_KANTO]`, `sRegionMapSections_Kanto`). The wall map's title reads OIKOUMENE there.
- Crossing targets: AETHOS (the inlay, cells 9–11 × 6–8) flies to Akti; THE OIKOUMENE (Aethos chart, cell 27,5, in a painted fog bank with a sail) flies to the last Oikoumene port. Both stay unnamed, with no target icon, until `FLAG_ICHOR_OIKOUMENE_ARRIVED`.
- Last port and visited towns live in one bank var, `VAR_ICHOR_OIK_CHART` (offset 24): bits 0–1 the port (Sestos, Naukratis, Kroton, Themiskyra; Kroton and Themiskyra fall back to Sestos until they have heal locations), bits 2–15 the towns visited. `Ichor_TrackOikoumene` keeps it on every map load (overworld.c), so the towns' scripts set no visited flag. No bank flags were claimed.
- Fly targets and heal locations for Sestos, Ilion, Naukratis, Memphis, Salmydessos and Aia. Every heal location is a placeholder at (3,23) on the placeholder layout: the lead moves each to its town's Wings landing after merge.
- Popups: three new stones (TROAD limestone walls, PAPYRUS, PONTOS bronze; `tools/ichor/art/ui_oikoumene_popups.py`), and a theme for all 107 sections, including a tail table for the Kanto-tail ids.
- Battle music: trainers in the Oikoumene play `MUS_ICHOR_BATTLE_OIKOUMENE`, which is `#define`d to `MUS_ICHOR_BATTLE_TRAINER` until the music agent's song lands (`ICHOR_STUB_MUSIC` in `src/pokemon.c`; it falls away by itself once songs.h defines it). Wild battles keep Ichor's wild theme, not FRLG's.
- The audit (below) and its guards; the magnetic-field slot pin (Gargaros Peak takes id 62).
- Nursery hook in `src/wild_encounter.c` (`sIchorNurseryMaps`, `Ichor_GetAethosMonth`, `Ichor_GetNurseryHeaderOffset`, `Ichor_IsWildHeaderCurrent`), with the Pokédex area view showing only this month's table.

**Partial:**
- *The chart art.* `tools/ichor/art/ui_oikoumene_map.py` paints a working chart: the disc with Okeanos as a block-drawn ellipse, polygon coastlines for the Mediterranean (Italy, the Adriatic), the Hellespont, Propontis, Bosporus and the Black Sea, a glyph for every place, roads, the Nile, sea lanes, the meander border. Fly map 241 tiles (of 256); the Pokédex view drops the landscape stamps to fit 229 (of 232). The script stops if either is over. Still to do: one critique pass is written (below), not three; the Aethos inlay's miniature is a muddy blob and wants a hand-drawn Greece; the land is cluttered with glyphs and needs a hierarchy (towns bright, ways quiet); the in-game screenshot shown here predates the polygon coasts.
- *The Nursery test.* `test/ichor_nursery.c` is written (month, twelve-table offset, wrap, non-Nursery maps) but was never run: the `make check` build was stopped. With the table empty the ROM's compiler drops the Nursery path, so an in-game check waits for batch 2's first Nursery map.
- *BUILD.md* has no §5 subsection yet; the Nursery convention is below, ready to move there.

**Not started:** the slice playthrough at the end; a second and third critique pass; the in-game screenshot of the final art.

**`make`:** green at the WIP commit (fe6a756908): ROM 22,204,208 B (66.17%), up from 22,191,564 B. The smoke and slice tests weren't run after the polygon-coast regeneration.

## The Nurseries' monthly tables (for BUILD.md §5)

- A Nursery is its own small map (not a corner of a route), because a wild table is per map.
- In `src/data/wild_encounters.json`, its block holds **twelve consecutive entries with the same `map`**, in month order: entry 0 is Hekatombaion (days 0–2 of the 36-day year), entry 11 Skirophorion. `base_label`s must differ (e.g. `gNursery_LambingMeadows_M00` … `_M11`).
- Add the map to `sIchorNurseryMaps` in `src/wild_encounter.c`, above `MAP_UNDEFINED`.
- The month is `(VAR_DAYS / 3) % 12` (SYSTEMS §7). A Nursery with fewer than twelve entries wraps the month over what it has.

## The audit

Every upstream use of the Hoenn block's old names and the Kanto tail's old names, and what was done.

| Where | What it does | Fires on an Oikoumene place? | Done |
|---|---|---|---|
| `src/region_map.c` | heal locations, fly targets, map types, Ever Grande's two names, Southern Island, Littleroot's fly, bent-route cursor cases (114, 121, 126), special-place redirects (Kyrene, Lake Maeotis), red outlines | yes | rewritten for the Oikoumene; Hoenn entries removed; FRLG targets under `#if IS_FRLG`; redirects skip Oikoumene ids; a general cursor snap replaces the bent-route cases |
| `src/map_name_popup.c` | theme per section | yes | Oikoumene themes; tail table added |
| `src/regions.c` | Sevii sub-charts by Kanto-tail name | yes (Mount Nysa, Pillars, …) | `!IS_FRLG` returns the main subregion |
| `src/pokemon.c` | Kanto battle music | yes (region is Kanto's slot) | FRLG-only; Oikoumene branch added |
| species `IF_IN_MAPSEC MAPSEC_NEW_MAUVILLE` | Magnezone, Probopass, Vikavolt by level | yes (was Silphium Plateau) | `oikoumene_sections.py` `PINNED` puts Gargaros Peak (Ida's summit, Pliny's lodestone) on id 62. **Open question for the director.** |
| `src/event_object_movement.c` | gym-type follower emotes under `MUS_GYM` | only with gym music | guarded: not in the Oikoumene |
| `src/field_region_map.c` | wall map title | yes | OIKOUMENE in the Oikoumene |
| `src/pokedex_area_screen.c` | Sky Pillar, Seafloor Cavern landmarks | no (skipped slots 85, 68) | Nursery off-months filtered |
| `src/match_call.c`, `pokenav_match_call_data.c`, `landmark.c`, `city_map_entries.h` | Pokénav | no: the Pokénav and Match Call are never given | none |
| `src/map_preview_screen.c` | FRLG dungeon previews | no: `MPS_ENABLE_MAP_PREVIEWS` is `IS_FRLG` | none |
| `battle_message.c`, `battle_util2.c`, `battle_controller_opponent.c` | Trainer Tower (Isles of the Blessed's old id) | no: needs `BATTLE_TYPE_TRAINER_TOWER`, FRLG maps only | none |
| `follower_helper.c`, `battle_tent.c`, `field_weather_effect.c` | Sky Pillar, Mt. Pyre, Petalburg Woods, Slateport, Dewford | no: skipped slots | none; `SKIP_HOENN` kept as is |

**Renumbering:** Gargaros Peak and the Silphium Plateau swapped ids (7 ↔ 62). Nothing else moved. `oikoumene_sections.py` now accepts any of its own names in a slot, keeps each section's chart position across a renumbering, and rewrites the Hoenn aliases by slot.

**Names:** every Oikoumene name fits the Fly map's 96-pixel name box in the normal font (widest: ARIMASPI HEIGHTS and SILPHIUM PLATEAU, 93 px). Thirteen are over the popup's 80 px and print in the narrow font, as long Aethos names do; none needed shortening.

## Critique passes

**Pass 1** (the first full render, cell-built coasts): the disc read as a round shield only once the rim was drawn in 4-pixel blocks; a smooth ellipse cost about 120 tiles on its own, a ring following the cells looked like an octagonal UI frame. The inner seas were boxes, Italy invisible, the Mediterranean a cross of channels. Fixes made: polygon coastlines for every inner sea; Thrinakia drawn as an island; the Nile a river through land; the Pokédex view allowed to drop decoration to fit its 232 tiles. Still to fix: glyph clutter, the inlay's miniature, a visual hierarchy between towns and minor places.

