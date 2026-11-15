# The Black Sea's outdoor maps: the Bosporus, Salmydessos, the Pontic Coast, Aia

The pontos-towns agent's maps (BUILD.md §5, batch 1). Tileset: `gTileset_Pontos` on `aethos`
([TILES_pontos.md](TILES_pontos.md)). Builders: `tools/ichor/maps/bosporus.py`,
`salmydessos.py`, `pontic_coast.py`, `aia.py`, sharing `pontos_map.py`.

**Rebuild order.** A coast piece's id depends on every map's coastline, so after any plan
change: `rm tools/ichor/art/pontos_shapes.json`, run each builder with `--shapes`, then
`/usr/bin/python3 tools/ichor/art/pontos_build.py`, then each builder again (with
`--render DIR` for review images).

## Stopped at (2026-11-14: the Oikoumene paused)

**`make` at the last commit: red.** It stops in `data/map_events.o`
(`data/maps/Aia/events.inc:40: invalid operands`): the maps' events name item and hidden-item
flags that aren't claimed yet (see Partial). The tileset and layouts themselves assemble.
Smoke and slice tests were not run.

### Done
- **`gTileset_Pontos`**, compiled and registered (`src/data/tilesets/{headers,graphics,metatiles}.h`):
  397 of 504 tiles; sheet rows 50-63 left for batch 2 (107 tiles free).
  - Palettes: six packed groups in slots 6-11 (chalk, kyanean, bronze, timber, flora, accent) and
    **slot 12, the Pontic sea**: aethos's sea palette with its blues turned dark green. Pontos
    metatiles point at aethos's animated water tiles with palette 12, so the Black Sea is dark
    green and still moves, for no tiles.
  - Coast autotiles (`pontos_coast.py`): white chalk cliffs with a face standing about a cell
    tall on south-facing coasts, the Clashing Rocks' blue-black kyanean rock, dressed-stone quays.
    One piece per 3x3 neighbourhood the maps use (`pontos_shapes.json`).
  - Props: chalk and kyanean crags, a sea stack, whirlpool, sea-marks (the lanes' signs), the
    dove's feathers in the Clashing Rocks, the Acherusian cave, a colony lighthouse; the Isle of
    Ares's black stone, feathers in the turf, shield post, roost, dead perch; oak, hazel, reeds;
    the thatch roof kit, Thracian daub walls, Colchian log walls (Vitruvius's towers), Phineus's
    raked roof and table, the dovecote and cages, pier, boat, nets, wreck and boundary stones;
    Aietes's bronze palace, Hephaestus's four fountains (milk, wine, oil, water), vine posts, the
    ram post (Aia's waystone), the Euploia moored stern-to with her gangplank.
- **Layouts, borders, connections and events written by code** for all four maps; each builder's
  checks pass (surf-aware reachability, doors warped, people on open ground, signs and people
  readable, seam rules, the narrows checkpoint proven, the whirlpool jar locked).
  - **The Bosporus** (56x34, sea lane): west edge rows 8-21 open sea to the Hellespont, every other
    row shore; columns 0-7 aethos only. The Propontis basin with an islet, the European ridge with
    the Hieron (Zeus of the Fair Wind's altar) and its landing stage, the narrows (Euphemos's
    checkpoint), the strait, the Clashing Rocks standing open across the mouth, the side channel
    visible but shut (`ICHOR_STUB_STRETCH`). 4 trainers placed (the audit wants 5).
  - **Salmydessos** (28x24, village): Phineus's house (door warp 0) and the bird-catcher's (warp 1),
    the beach with the wreck and boundary stones, a pier, a small stone mole with the Euploia and
    Nausikles (`ICHOR_STUB_SHIP`). **Wings landing tile (5, 7).**
  - **The Pontic Coast** (80x40, sea lane): the Bosporus's mouth, Herakleia with the Acherusian
    cave, Sinope with its lighthouse and quay, the whirlpool cove (`ICHOR_STUB_RELIC`: Triton's
    Conch; its jar locked), the Isle of Ares with grass, the black stone, perches and the roost
    crag (`ICHOR_STUB_LEGEND`: Yveltal), the north-west reach open for Leuke (west edge rows 0-15),
    the Phasis mouth to Aia (east edge rows 22-30). **Themiskyra landing tile (65, 30)**
    (`ICHOR_STUB_PG_LANDING` sign at (64, 28)). 8 trainers placed (the audit wants 7).
  - **Aia** (44x36, city): harbor at the Phasis mouth (west edge rows 18-26), quay and mole with the
    Euploia and Nausikles, the Asclepeion (warp 0) and Agora (warp 1) on the harbor plaza, Phrixos's
    sons' log tower (warp 2), the linen-weaver's (warp 3), the palace workshop (warp 4), Aietes's
    bronze palace and the four fountains (palace door guarded, `ICHOR_STUB_HALL`), the reeds and
    pheasants, the east gate road left open for the Phasis (east edge rows 18-19). **Wings landing
    tile (18, 15).**
  - Connections: Bosporus left Hellespont 0, up Salmydessos 0, up Pontic Coast 28; Salmydessos down
    Bosporus 0, right Pontic Coast -16; Pontic Coast down Bosporus -28, left Salmydessos 16, right
    Aia 4; Aia left Pontic Coast -4.
- 2x renders: `img/bosporus.png`, `img/salmydessos.png`, `img/pontic_coast.png`, `img/aia.png`.

### Partial
- **Events reference scripts and flags that don't exist yet.** The four maps' `scripts.pory` are
  still the registration placeholders, and the item and hidden-item flags named in `map.json`
  (`FLAG_ICHOR_ITEM_*`, `FLAG_ICHOR_HIDDEN_*`) are unclaimed. This is why `make` fails if it does.
  To finish: write the four `scripts.pory` (every sign, person, trainer and stub named in the
  builders' `EVENTS`), claim bank flags 0x424-0x433 for item balls and put the eight hidden items
  on vanilla 0x4D0-0x4D7 (two per map; the audit's further ones go under ICHOR_STUB_HIDDEN).
- **Render-and-critique passes:** the Bosporus had three (below); Salmydessos two; the Pontic
  Coast and Aia one each (built and checked, not yet reviewed against their renders).
- Music stand-ins: lanes `MUS_ICHOR_TRIREME`, Salmydessos `MUS_ICHOR_AKTI`, Aia
  `MUS_ICHOR_EMPORION` (intended: *The Black Sea*; tag `ICHOR_STUB_MUSIC` in the scripts).

### Not started
- Trainers 720-733 (and 943-950 if needed): `opponents.h` Oikoumene block and parties under
  `/* Ichor: the Oikoumene, Black Sea */`; the placed trainer objects use swimmer stand-ins
  (`ICHOR_STUB_SPRITE`, intended `_ARGONAUT`) and need classes with `# ICHOR_STUB_CLASS` comments.
- Wild tables in `src/data/wild_encounters.json`: the Bosporus (E1, 67-69), the Pontic Coast
  (E2, 68-70, plus the Isle of Ares's land tables, _Morning/_Day/_Evening/_Night), town water for
  Salmydessos and Aia. Rates: surf 10, fishing 30, land 25. Augur's Eye hidden slots need a
  `hidden_mons` field in the JSON's group (and its template), which no map has yet.
- Text measured with `text_width.py`; the Lua test `tools/ichor/tests/pontos_towns.*`; the
  smoke test; `map_audit.py`; the fifth Bosporus trainer.

### Open questions
- **Tile budget:** 397 of 504 leaves 107 for batch 2 (the Phasis, the Field of Ares, the Grove
  of Ares, Leuke, the Caucasus caves). Leuke can reuse the chalk coast; the rest is tight.
- The audit's "every house a home" fails on the towns until pontos-rooms' interiors merge.
- The Hellespont seam is built to BUILD.md §5 but only tested against the placeholder.

## Render-and-critique passes

**The Bosporus.**
1. Cliffs read as thin curbs; the Clashing Rocks were rectangles; the blue-to-green staircase
   at the seam looked artificial; the shores were empty grass. *Changed:* faces raised to about a
   cell (9 px inside the land, 9 below), rims thickened, rocks given an outline, the seam made a
   straight line marked by a current, the shores filled with Pontic woods.
2. The narrows trainer stood on a face cell; the side channel's sign sat in a sealed pocket; the
   jetty-style landing produced broken beach corners. *Changed:* checkpoint moved, sign moved to
   the channel's north rocks, the Hieron reached by a stone landing stage instead of a beach.
3. Both rocks share one rounded shape (fewer pieces), the west rock's face carries the dove's
   feathers. The mouth now reads as two dark rocks standing open with the passage between.
   *Still to do:* taller rock tops, more life on the water (rocks, items).

**Salmydessos.**
1. The stone jetty dominated a Thracian fishing village. *Changed:* a beach at the bay's head, a
   wooden pier, and a small mole for the Euploia.
2. Reads as a village: thatch, Phineus's raked roof and table, dovecote, wreck stones. *Still to
   do:* the green between the houses is bare.

**The Pontic Coast** and **Aia**: built and checked; no review pass yet.
