#!/usr/bin/env python3
"""Naukratis's and Memphis's interiors, on the per tileset.

Every house is a home and every interior is unique (design/MAP_DESIGN.md
section 2); public buildings share their counter but not their plan. Who
lives in each room and what happens there is in design/OIKOUMENE.md section
4.5 and design/oikoumene/ROOMS_egypt.md, which also records the
render-and-critique passes.

Room format (world-act1's aegina_homes.py, with the events kept here too):
  grid    one string per row: '.' the room's floor, 'W' its wall, '#' void;
          `floors` and `walls` map more characters to other floors and walls
  stamps  (stamp, x, y), the stamp's top-left cell (tools/ichor/art/per_*.py)
  rugs    (design, x, y, w, h)
  exit    the door mat's two tiles: warp 0, back to the town's warp `door`
  people  object events: id (a LOCALID_ name or None), gfx, at, face, script,
          flag (hide flag, or "0"), perch (the tile to talk from, when they
          stand on furniture), move (a movement type), label
  signs   bg events: script, at, read (x, y, facing), label
  layout  the data/layouts/ folder; render: the 2x image in design/oikoumene/img/

per_build.py composes and checks the rooms (every warp, person and readable
thing walkable and reachable from the door) and writes their layouts; this
module then writes each map.json's events from the same data, so the two
never disagree.

  /usr/bin/python3 tools/ichor/maps/egypt_rooms.py   # builds per, the rooms and the maps
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

G = "OBJ_EVENT_GFX_ICHOR_"
# Stand-ins until the sprites agent's Egyptians land (ICHOR_STUB_SPRITE; the
# table is in design/oikoumene/ROOMS_egypt.md).
EGYPTIAN_M = G + "MAN"
EGYPTIAN_F = G + "WOMAN"
SCRIBE = G + "AUGUR"
EMBALMER = G + "ACOLYTE_M"
PHOENICIAN = G + "MERCHANT"
GREEK_M = G + "SAILOR"
DAPHNE = G + "PROFESSOR_DAPHNE"


def mon(species):
    return f"OBJ_EVENT_GFX_SPECIES({species})"


def _grid(w, h, rows=None):
    """A room w wide and h tall: two rows of wall, then floor. `rows` swaps
    whole rows by index (for voids and odd corners)."""
    g = ["W" * w, "W" * w] + ["." * w for _ in range(h - 2)]
    for y, row in (rows or {}).items():
        g[y] = row
    return g


ROOMS = {
    # ==================================================================
    # NAUKRATIS
    # ==================================================================
    # The Asclepeion. The Greeks of the Hellenion built it of the town's
    # mud brick and kept their god: Asclepius's rod is painted over the
    # counter. A window looks over the river harbor. The patients' beds stand
    # on a reed mat on the west side, a lamp between them; the east side is
    # a waiting corner by the Pithos, and an ear stele by it asks the god to
    # listen, the Egyptian way. Papyrus grows in pots either side of the door.
    "naukratis_asclepeion": {
        "title": "The Asclepeion, Naukratis",
        "map": "MAP_NAUKRATIS_ASCLEPEION",
        "town": "MAP_NAUKRATIS", "door": 0,
        "layout": "Naukratis_Asclepeion",
        "render": "egypt_naukratis_asclepeion.png",
        "music": "MUS_ICHOR_ASCLEPEION",
        "floor": "flags",
        "wall": "plaster",
        "grid": _grid(13, 9),
        "rugs": [("mat", 0, 4, 3, 4), ("mat", 9, 5, 4, 2)],
        "stamps": [
            ("window_river", 1, 0),
            ("relief_rod", 6, 0),
            ("basin_naukratis", 4, 1),
            ("counter_heal_l", 3, 2),
            ("counter_heal_front", 4, 3),
            ("counter_heal_front", 5, 3),
            ("counter_heal_staff", 6, 2),
            ("counter_heal_m", 7, 2),
            ("counter_heal_r", 8, 2),
            ("pithos", 10, 1),
            ("ear_stele", 12, 0),
            ("lamp", 2, 7),
            ("bed", 0, 4),
            ("bed", 0, 6),
            ("chair", 9, 5),
            ("table", 10, 5),
            ("chair", 11, 5),
            ("papyrus_pot", 4, 7),
            ("papyrus_pot", 9, 7),
            ("jar", 12, 8),
            ("mat", 6, 8),
        ],
        "exit": [(6, 8), (7, 8)],
        "people": [
            dict(id="LOCALID_NAUKRATIS_HEALER", gfx=G + "HEALER", at=(6, 2), face="south", counter=True,
                 script="Naukratis_Asclepeion_EventScript_Healer", label="the healer"),
            dict(gfx=GREEK_M, at=(2, 6), face="west",
                 script="Naukratis_Asclepeion_EventScript_Sailor", label="a Samian sailor by the beds, his hand bound up"),
            dict(gfx=EGYPTIAN_F, at=(12, 6), face="west",
                 script="Naukratis_Asclepeion_EventScript_CatWoman", label="an Egyptian woman, waiting with her Espurr"),
            dict(gfx=mon("ESPURR"), at=(10, 6), face="east",
                 script="Naukratis_Asclepeion_EventScript_Espurr", label="her Espurr, Miu"),
        ],
        "signs": [
            dict(script="Naukratis_Asclepeion_EventScript_Pithos", at=(10, 2), read=(10, 3, "north"),
                 label="the Pithos"),
            dict(script="Naukratis_Asclepeion_EventScript_Pithos", at=(11, 2), read=(11, 3, "north"),
                 label="the Pithos"),
            dict(script="Naukratis_Asclepeion_EventScript_EarStele", at=(12, 1), read=(12, 2, "north"),
                 label="the ear stele"),
            dict(script="Naukratis_Asclepeion_EventScript_Window", at=(1, 1), read=(1, 2, "north"),
                 label="the window on the harbor"),
        ],
    },
    # ------------------------------------------------------------------
    # The Agora: the emporion's hall. Naukratis is where Greece's wine and
    # oil come in and Egypt's grain and linen go out, so the stall stands
    # between the two trades: Greek amphorae racked against the west wall
    # beside the oil shelf, and on the east, by the window on the quay, sacks
    # of emmer and crates for the outbound ships.
    "naukratis_agora": {
        "title": "The Agora, Naukratis",
        "map": "MAP_NAUKRATIS_AGORA",
        "town": "MAP_NAUKRATIS", "door": 1,
        "layout": "Naukratis_Agora",
        "render": "egypt_naukratis_agora.png",
        "music": "MUS_ICHOR_AGORA",
        "floor": "earth",
        "wall": "plaster",
        "grid": _grid(12, 8),
        "rugs": [("mat", 3, 5, 5, 2)],
        "stamps": [
            ("amphora_rack", 0, 1),
            ("jar_shelf", 2, 1),
            ("counter_stall_l_scale", 4, 2),
            ("counter_stall_m", 5, 2),
            ("counter_stall_staff", 6, 2),
            ("counter_stall_r_bread", 7, 2),
            ("window_river", 9, 0),
            ("crate_stack", 10, 1),
            ("crate_shut", 11, 2),
            ("sacks_grain", 10, 4),
            ("sacks_grain", 11, 4),
            ("sacks_grain", 11, 5),
            ("jars", 0, 4),
            ("amphora_rack", 0, 5),
            ("crate_shut", 11, 7),
            ("mat", 5, 7),
        ],
        "exit": [(5, 7), (6, 7)],
        "people": [
            dict(gfx=G + "MERCHANT", at=(6, 2), face="south", counter=True,
                 script="Naukratis_Agora_EventScript_Stallkeeper", label="Charaxos, the stallkeeper"),
            dict(gfx=PHOENICIAN, at=(2, 5), face="west",
                 script="Naukratis_Agora_EventScript_Trader", label="a Chian wine trader, by the amphorae"),
            dict(gfx=EGYPTIAN_M, at=(9, 5), face="east",
                 script="Naukratis_Agora_EventScript_Porter", label="a porter by the grain sacks"),
        ],
        "signs": [
            dict(script="Naukratis_Agora_EventScript_Amphorae", at=(1, 2), read=(1, 3, "north"),
                 label="the amphora rack"),
        ],
    },
    # ------------------------------------------------------------------
    # Daphne's field station. She has rented a little mud-brick house off
    # the quay: her chart of the Oikoumene pinned over her work table, crates
    # of fossils from every dig stacked in the east corner, her camp cot on a
    # mat, and in the middle of the floor the trough of black Nile silt where
    # she wakes them.
    "naukratis_field_station": {
        "title": "Daphne's field station, Naukratis",
        "map": "MAP_NAUKRATIS_FIELD_STATION",
        "town": "MAP_NAUKRATIS", "door": 2,
        "layout": "Naukratis_FieldStation",
        "render": "egypt_naukratis_field_station.png",
        "floor": "earth",
        "wall": "plaster",
        "grid": _grid(11, 8),
        "rugs": [("mat", 7, 5, 4, 2)],
        "stamps": [
            ("lamp", 0, 1),
            ("chart", 1, 0),
            ("desk_notes", 1, 2),
            ("stool", 2, 3),
            ("papyrus_pot", 4, 1),
            ("crate_stack", 8, 1),
            ("crate_fossils", 9, 2),
            ("crate_fossils", 10, 2),
            ("crate_shut", 10, 3),
            ("silt_trough", 4, 4),
            ("cot", 7, 5),
            ("chest", 10, 5),
            ("dig_tools", 0, 5),
            ("jar", 0, 6),
            ("mat", 5, 7),
        ],
        "exit": [(5, 7), (6, 7)],
        "people": [
            dict(id="LOCALID_NAUKRATIS_DAPHNE", gfx=DAPHNE, at=(6, 4), face="south",
                 script="Naukratis_FieldStation_EventScript_Daphne", label="Daphne, by her silt trough"),
        ],
        "signs": [
            dict(script="Naukratis_FieldStation_EventScript_Trough", at=(4, 4), read=(4, 5, "north"),
                 label="the silt trough"),
            dict(script="Naukratis_FieldStation_EventScript_Notes", at=(1, 2), read=(1, 3, "north"),
                 label="her notes, and the chart over them"),
            dict(script="Naukratis_FieldStation_EventScript_Crates", at=(9, 2), read=(9, 3, "north"),
                 label="the fossil crates"),
        ],
    },
    # ------------------------------------------------------------------
    # The egg-ovens: the Oikoumene's day care. A long mud-brick hall, warm
    # as a bath: four vaulted ovens along the back wall, the fire troughs
    # glowing between them, eggs in baskets turning on a bed of straw in the
    # middle, dung-cake fuel stacked by the east wall. Neferu keeps the fires
    # and minds the eggs; his wife Tiy takes in the Pokémon.
    "naukratis_egg_ovens": {
        "title": "The egg-ovens, Naukratis",
        "map": "MAP_NAUKRATIS_EGG_OVENS",
        "town": "MAP_NAUKRATIS", "door": 3,
        "layout": "Naukratis_EggOvens",
        "render": "egypt_naukratis_egg_ovens.png",
        "floor": "earth",
        "wall": "brick",
        "grid": _grid(13, 9),
        "rugs": [("straw", 3, 4, 6, 3)],
        "stamps": [
            ("egg_oven", 0, 1),
            ("fire_trough", 2, 2),
            ("egg_oven", 3, 1),
            ("fire_trough", 5, 2),
            ("egg_oven", 6, 1),
            ("fire_trough", 8, 2),
            ("egg_oven", 9, 1),
            ("jars", 11, 2),
            ("jar", 12, 2),
            ("basket_eggs", 4, 5),
            ("basket_eggs", 6, 5),
            ("basket_eggs", 7, 4),
            ("fuel", 12, 4),
            ("fuel", 12, 5),
            ("fire_trough", 11, 7),
            ("stool", 1, 5),
            ("basket_eggs", 0, 7),
            ("mat", 6, 8),
        ],
        "exit": [(6, 8), (7, 8)],
        "people": [
            dict(id="LOCALID_EGG_OVENS_NEFERU", gfx=EGYPTIAN_M, at=(2, 4), face="east",
                 script="Naukratis_EggOvens_EventScript_Neferu", label="Neferu, the oven-keeper, turning eggs"),
            dict(id="LOCALID_EGG_OVENS_TIY", gfx=EGYPTIAN_F, at=(10, 5), face="west",
                 script="Naukratis_EggOvens_EventScript_Tiy", label="Tiy, who takes in the Pokémon"),
        ],
        "signs": [
            dict(script="Naukratis_EggOvens_EventScript_Oven", at=(4, 2), read=(4, 3, "north"),
                 label="an oven"),
            dict(script="Naukratis_EggOvens_EventScript_Oven", at=(10, 2), read=(10, 3, "north"),
                 label="an oven"),
        ],
    },
    # ------------------------------------------------------------------
    # The incense merchant from Arabia. A narrow shop thick with smoke: his
    # own rug from home on the floor, his low table and balance across it,
    # jars of oils on the shelves behind him, sacks of frankincense and myrrh
    # along the walls, and two censers going all day.
    "naukratis_incense_shop": {
        "title": "The incense merchant's, Naukratis",
        "map": "MAP_NAUKRATIS_INCENSE_SHOP",
        "town": "MAP_NAUKRATIS", "door": 4,
        "layout": "Naukratis_IncenseShop",
        "render": "egypt_naukratis_incense_shop.png",
        "floor": "earth",
        "wall": "plaster",
        "grid": _grid(10, 8),
        "rugs": [("arabian", 2, 2, 6, 3)],
        "stamps": [
            ("censer", 0, 1),
            ("sacks_frank", 1, 2),
            ("jar_shelf", 2, 1),
            ("jar_shelf", 6, 1),
            ("sacks_myrrh", 8, 2),
            ("censer", 9, 1),
            ("incense_table", 4, 3),
            ("sacks_frank", 0, 5),
            ("sacks_myrrh", 9, 4),
            ("jars", 9, 5),
            ("mat", 4, 7),
        ],
        "exit": [(4, 7), (5, 7)],
        "people": [
            dict(gfx=PHOENICIAN, at=(5, 2), face="south", counter=True,
                 script="Naukratis_IncenseShop_EventScript_Merchant", label="Yada'il, the incense merchant from Saba"),
            dict(gfx=G + "ELDER_F", at=(1, 4), face="east",
                 script="Naukratis_IncenseShop_EventScript_Customer", label="a Greek widow buying for a funeral"),
        ],
        "signs": [
            dict(script="Naukratis_IncenseShop_EventScript_Frankincense", at=(1, 2), read=(1, 3, "north"),
                 label="the frankincense"),
            dict(script="Naukratis_IncenseShop_EventScript_Myrrh", at=(8, 2), read=(8, 3, "north"),
                 label="the myrrh"),
        ],
    },
    # ------------------------------------------------------------------
    # The potter's house. Naukratis's Greek potters throw white-slipped
    # chalices for the temples. Lykos works at his turntable in the middle of
    # the floor by the clay trough; his finished pots fill the shelves,
    # greenware dries along the wall and by the kiln in the east corner. His
    # Kecleon sits among the drying pots and turns their colour.
    "naukratis_potters_house": {
        "title": "The potter's house, Naukratis",
        "map": "MAP_NAUKRATIS_POTTERS_HOUSE",
        "town": "MAP_NAUKRATIS", "door": 5,
        "layout": "Naukratis_PottersHouse",
        "render": "egypt_naukratis_potters_house.png",
        "floor": "earth",
        "wall": "brick",
        "grid": _grid(11, 8),
        "rugs": [],
        "stamps": [
            ("pot_shelf", 0, 1),
            ("greenware", 2, 2),
            ("greenware", 3, 2),
            ("jars", 4, 2),
            ("kiln", 8, 1),
            ("fuel", 10, 2),
            ("greenware", 7, 3),
            ("wheel", 5, 4),
            ("clay_tub", 4, 5),
            ("jar", 0, 4),
            ("jars", 0, 5),
            ("table", 9, 5),
            ("stool", 10, 5),
            ("mat", 5, 7),
        ],
        "exit": [(5, 7), (6, 7)],
        "people": [
            dict(id="LOCALID_POTTER_LYKOS", gfx=GREEK_M, at=(6, 4), face="west",
                 script="Naukratis_PottersHouse_EventScript_Lykos", label="Lykos the potter, at his wheel"),
            dict(id="LOCALID_POTTER_KECLEON", gfx=mon("KECLEON"), at=(3, 3), face="south",
                 flag="FLAG_ICHOR_TRADED_KECLEON",
                 script="Naukratis_PottersHouse_EventScript_Kecleon", label="Lykos's Kecleon, among the drying pots"),
            dict(id="LOCALID_POTTER_SMEARGLE", gfx=mon("SMEARGLE"), at=(3, 3), face="north",
                 flag="FLAG_TEMP_1",
                 script="Naukratis_PottersHouse_EventScript_Smeargle", label="the Smeargle, painting, after the trade"),
        ],
        "signs": [
            dict(script="Naukratis_PottersHouse_EventScript_Shelf", at=(1, 2), read=(1, 3, "north"),
                 label="the pot shelf"),
            dict(script="Naukratis_PottersHouse_EventScript_Kiln", at=(9, 2), read=(9, 3, "north"),
                 label="the kiln"),
        ],
    },
    # ------------------------------------------------------------------
    # The net-loft. Ipy the fisher and his wife Merit: his nets drying on
    # their poles, a papyrus skiff waiting for its new bindings, baskets of
    # the morning's perch by his corner; her flax in sheaves under the window
    # and her ground loom pegged to the floor, a length of linen half woven.
    # Merit's brother is the embalmer in Memphis.
    "naukratis_net_loft": {
        "title": "The net-loft, Naukratis",
        "map": "MAP_NAUKRATIS_NET_LOFT",
        "town": "MAP_NAUKRATIS", "door": 6,
        "layout": "Naukratis_NetLoft",
        "render": "egypt_naukratis_net_loft.png",
        "floor": "mat",
        "wall": "brick",
        "grid": _grid(12, 8),
        "rugs": [],
        "stamps": [
            ("net_rack", 0, 1),
            ("window_river", 3, 0),
            ("flax", 3, 2),
            ("flax", 4, 2),
            ("spindles", 5, 2),
            ("net_rack", 9, 1),
            ("basket_fish", 11, 3),
            ("basket_fish", 11, 4),
            ("ground_loom", 3, 4),
            ("skiff", 8, 6),
            ("jar", 0, 5),
            ("stool", 1, 6),
            ("mat", 5, 7),
        ],
        "exit": [(5, 7), (6, 7)],
        "people": [
            dict(gfx=G + "FISHER", at=(10, 4), face="west",
                 script="Naukratis_NetLoft_EventScript_Ipy", label="Ipy the fisher, mending a net"),
            dict(gfx=EGYPTIAN_F, at=(5, 5), face="west",
                 script="Naukratis_NetLoft_EventScript_Merit", label="Merit, at her loom"),
        ],
        "signs": [
            dict(script="Naukratis_NetLoft_EventScript_Loom", at=(4, 4), read=(4, 3, "south"),
                 label="the ground loom"),
            dict(script="Naukratis_NetLoft_EventScript_Skiff", at=(8, 6), read=(8, 5, "south"),
                 label="the papyrus skiff"),
        ],
    },
    # ==================================================================
    # MEMPHIS
    # ==================================================================
    # The Asclepeion: the shrine of Imhotep, the old king's architect and
    # healer, whom the Greeks call Asclepius. Painted limestone under a
    # starry ceiling; two papyrus columns; Imhotep himself seated with his
    # papyrus between two lamps, a scribe at his feet; the same healer's
    # counter as every Asclepeion, with an offering table for a basin; a
    # reed mat before it for the sick to wait on, and a bed in each corner.
    "memphis_asclepeion": {
        "title": "The Asclepeion, Memphis",
        "map": "MAP_MEMPHIS_ASCLEPEION",
        "town": "MAP_MEMPHIS", "door": 0,
        "layout": "Memphis_Asclepeion",
        "render": "egypt_memphis_asclepeion.png",
        "music": "MUS_ICHOR_ASCLEPEION",
        "floor": "flags",
        "wall": "temple",
        "grid": _grid(15, 10),
        "rugs": [("mat", 5, 5, 5, 3)],
        "stamps": [
            ("lamp", 1, 1),
            ("imhotep", 2, 1),
            ("lamp", 3, 1),
            ("basin_memphis", 5, 1),
            ("counter_heal_l", 4, 2),
            ("counter_heal_front", 5, 3),
            ("counter_heal_front", 6, 3),
            ("counter_heal_staff", 7, 2),
            ("counter_heal_m", 8, 2),
            ("counter_heal_r", 9, 2),
            ("censer", 10, 1),
            ("pithos", 12, 1),
            ("ear_stele", 14, 0),
            ("papyrus_column", 3, 5),
            ("papyrus_column", 11, 5),
            ("bed", 0, 5),
            ("bed", 0, 8),
            ("bed", 13, 5),
            ("bed", 13, 8),
            ("jar", 0, 7),
            ("chest", 14, 7),
            ("mat", 7, 9),
        ],
        "exit": [(7, 9), (8, 9)],
        "people": [
            dict(id="LOCALID_MEMPHIS_HEALER", gfx=G + "HEALER", at=(7, 2), face="south", counter=True,
                 script="Memphis_Asclepeion_EventScript_Healer", label="the healer"),
            dict(gfx=G + "PRIESTESS", at=(6, 6), face="south",
                 script="Memphis_Asclepeion_EventScript_Lector", label="a lector-priestess of Imhotep, on the mat"),
            dict(gfx=SCRIBE, at=(2, 3), face="north",
                 script="Memphis_Asclepeion_EventScript_Scribe", label="a scribe, praying to his patron"),
            dict(gfx=G + "KID_M", at=(12, 8), face="west",
                 script="Memphis_Asclepeion_EventScript_Boy", label="a boy with a scorpion sting, by his bed"),
        ],
        "signs": [
            dict(script="Memphis_Asclepeion_EventScript_Pithos", at=(12, 2), read=(12, 3, "north"),
                 label="the Pithos"),
            dict(script="Memphis_Asclepeion_EventScript_Pithos", at=(13, 2), read=(13, 3, "north"),
                 label="the Pithos"),
            dict(script="Memphis_Asclepeion_EventScript_Imhotep", at=(2, 2), read=(2, 3, "north"),
                 label="the statue of Imhotep"),
            dict(script="Memphis_Asclepeion_EventScript_EarStele", at=(14, 1), read=(14, 2, "north"),
                 label="the ear stele"),
        ],
    },
    # ------------------------------------------------------------------
    # The Agora: Memphis's market hall, Egyptian through and through. Onions
    # and garlic hang on the walls; beer and bread by the stall; dates for
    # the children to stare at; on the east side a linen-seller's bolts and
    # an amulet-maker's tray. The stall's counter is every Agora's.
    "memphis_agora": {
        "title": "The Agora, Memphis",
        "map": "MAP_MEMPHIS_AGORA",
        "town": "MAP_MEMPHIS", "door": 1,
        "layout": "Memphis_Agora",
        "render": "egypt_memphis_agora.png",
        "music": "MUS_ICHOR_AGORA",
        "floor": "mat",
        "wall": "plaster",
        "grid": _grid(12, 8),
        "rugs": [],
        "stamps": [
            ("onions", 1, 0),
            ("onions", 2, 0),
            ("jars", 0, 2),
            ("basket_bread", 1, 2),
            ("counter_stall_l_scale", 4, 2),
            ("counter_stall_m", 5, 2),
            ("counter_stall_staff", 6, 2),
            ("counter_stall_r_bread", 7, 2),
            ("onions", 9, 0),
            ("onions", 10, 0),
            ("sacks_grain", 10, 2),
            ("jar", 11, 2),
            ("basket_dates", 0, 4),
            ("basket_dates", 0, 5),
            ("linen_bolts", 10, 5),
            ("linen_bolts", 11, 5),
            ("amulets", 11, 6),
            ("jar", 0, 7),
            ("mat", 5, 7),
        ],
        "exit": [(5, 7), (6, 7)],
        "people": [
            dict(gfx=EGYPTIAN_M, at=(6, 2), face="south", counter=True,
                 script="Memphis_Agora_EventScript_Stallkeeper", label="Senbi, the stallkeeper"),
            dict(gfx=EGYPTIAN_F, at=(10, 6), face="west",
                 script="Memphis_Agora_EventScript_LinenSeller", label="the linen-seller"),
            dict(gfx=G + "KID_F", at=(1, 5), face="west",
                 script="Memphis_Agora_EventScript_Girl", label="a girl eyeing the dates"),
        ],
        "signs": [
            dict(script="Memphis_Agora_EventScript_Amulets", at=(11, 6), read=(11, 7, "north"),
                 label="the amulet tray"),
        ],
    },
    # ------------------------------------------------------------------
    # The Apis keepers'. The sacred herd's stable in the Apieion: painted
    # limestone, an earth floor deep in straw, the window of appearances in
    # the back wall where the true Apis is shown to the people. Four stalls
    # along the back, the water trough and fodder between them; in the pen
    # in front, two more of the herd and Hesat, the cow who bore the last
    # Apis. Which of them is the god?
    "memphis_apis_stable": {
        "title": "The Apis keepers', Memphis",
        "map": "MAP_MEMPHIS_APIS_STABLE",
        "town": "MAP_MEMPHIS", "door": 2,
        "layout": "Memphis_ApisStable",
        "render": "egypt_memphis_apis_stable.png",
        "floor": "earth",
        "wall": "temple",
        "grid": _grid(16, 10),
        "rugs": [("straw", 0, 2, 2, 3), ("straw", 3, 2, 2, 3), ("straw", 11, 2, 2, 3), ("straw", 14, 2, 2, 3),
                 ("straw", 10, 6, 6, 3)],
        "stamps": [
            ("manger", 0, 2),
            ("stall_wall", 2, 2),
            ("manger", 4, 2),
            ("stall_wall", 5, 2),
            ("hay", 6, 2),
            ("window_apis", 7, 0),
            ("hay", 9, 2),
            ("stall_wall", 10, 2),
            ("manger", 11, 2),
            ("stall_wall", 13, 2),
            ("manger", 15, 2),
            ("water_trough", 7, 4),
            ("water_trough", 12, 5),
            ("hay", 15, 8),
            ("stool", 1, 7),
            ("jar", 0, 8),
            ("mat", 7, 9),
        ],
        "exit": [(7, 9), (8, 9)],
        "people": [
            dict(gfx=G + "ELDER_M", at=(8, 6), face="south",
                 script="Memphis_ApisStable_EventScript_Keeper", label="Pakhom, the chief keeper"),
            dict(gfx=G + "GOATHERD", at=(3, 7), face="east",
                 script="Memphis_ApisStable_EventScript_Herdsman", label="a herdsman with a broom"),
            dict(id="LOCALID_APIS_BULL_1", gfx=mon("TAUROS_PALDEA_COMBAT"), at=(1, 3), face="south",
                 script="Memphis_ApisStable_EventScript_Bull1", label="a black bull: a star on the brow"),
            dict(id="LOCALID_APIS_BULL_2", gfx=mon("TAUROS_PALDEA_COMBAT"), at=(3, 3), face="south",
                 script="Memphis_ApisStable_EventScript_Bull2", label="a black bull: single tail hairs"),
            dict(id="LOCALID_APIS_BULL_3", gfx=mon("TAUROS_PALDEA_COMBAT"), at=(11, 3), face="south",
                 flag="FLAG_ICHOR_FOUND_APIS",
                 script="Memphis_ApisStable_EventScript_Bull3", label="the true Apis"),
            dict(id="LOCALID_APIS_BULL_4", gfx=mon("TAUROS"), at=(14, 3), face="south",
                 script="Memphis_ApisStable_EventScript_Bull4", label="a brown bull with every other mark"),
            dict(id="LOCALID_APIS_BULL_5", gfx=mon("TAUROS_PALDEA_COMBAT"), at=(11, 7), face="west",
                 script="Memphis_ApisStable_EventScript_Bull5", label="a black bull: a plain back"),
            dict(id="LOCALID_APIS_BULL_6", gfx=mon("TAUROS_PALDEA_COMBAT"), at=(13, 7), face="west",
                 script="Memphis_ApisStable_EventScript_Bull6", label="a black bull: a crescent on the brow"),
            dict(gfx=mon("MILTANK"), at=(14, 8), face="west",
                 script="Memphis_ApisStable_EventScript_Hesat", label="Hesat, mother of the last Apis"),
        ],
        "signs": [
            dict(script="Memphis_ApisStable_EventScript_Window", at=(7, 1), read=(7, 2, "north"),
                 label="the window of appearances"),
            dict(script="Memphis_ApisStable_EventScript_Window", at=(8, 1), read=(8, 2, "north"),
                 label="the window of appearances"),
        ],
    },
    # ------------------------------------------------------------------
    # The scribe of Thoth. A house of books on a reed-mat floor: niches of
    # papyrus rolls, the painted panel he sets his riddles from, Thoth as an
    # ibis and as a baboon keeping watch, and his low writing table, where
    # his apprentice copies. The riddles lead to the chambers where the Unown
    # sleep.
    "memphis_scribes_house": {
        "title": "The scribe of Thoth's house, Memphis",
        "map": "MAP_MEMPHIS_SCRIBES_HOUSE",
        "town": "MAP_MEMPHIS", "door": 3,
        "layout": "Memphis_ScribesHouse",
        "render": "egypt_memphis_scribes_house.png",
        "floor": "mat",
        "wall": "plaster",
        "grid": _grid(11, 8),
        "rugs": [],
        "stamps": [
            ("niches", 0, 1),
            ("niches", 2, 1),
            ("glyphs", 5, 0),
            ("ibis", 8, 1),
            ("baboon", 9, 2),
            ("papyrus_pot", 10, 1),
            ("scribe_desk", 4, 4),
            ("lamp", 7, 3),
            ("chest", 10, 5),
            ("jar", 0, 5),
            ("stool", 1, 6),
            ("mat", 5, 7),
        ],
        "exit": [(5, 7), (6, 7)],
        "people": [
            dict(gfx=SCRIBE, at=(5, 3), face="south",
                 script="Memphis_ScribesHouse_EventScript_Scribe", label="Amenemope, scribe of Thoth"),
            dict(gfx=G + "KID_M", at=(3, 4), face="east",
                 script="Memphis_ScribesHouse_EventScript_Apprentice", label="his apprentice, copying"),
        ],
        "signs": [
            dict(script="Memphis_ScribesHouse_EventScript_Glyphs", at=(5, 1), read=(5, 2, "north"),
                 label="the hieroglyph panel"),
            dict(script="Memphis_ScribesHouse_EventScript_Glyphs", at=(6, 1), read=(6, 2, "north"),
                 label="the hieroglyph panel"),
            dict(script="Memphis_ScribesHouse_EventScript_Ibis", at=(8, 2), read=(8, 3, "north"),
                 label="the ibis of Thoth"),
            dict(script="Memphis_ScribesHouse_EventScript_Niches", at=(1, 2), read=(1, 3, "north"),
                 label="the papyrus niches"),
        ],
    },
    # ------------------------------------------------------------------
    # The embalmer's. Khay's workshop on a limestone floor: two stone beds,
    # one with a small wrapped bundle on it, heaps of natron drying salt
    # along the back wall, the canopic jars waiting, the jackal mask on its
    # stand for the rites, resin warming over coals, and a basket of linen
    # rolls running low. His sister Merit weaves his linen in Naukratis.
    "memphis_embalmers_house": {
        "title": "The embalmer's house, Memphis",
        "map": "MAP_MEMPHIS_EMBALMERS_HOUSE",
        "town": "MAP_MEMPHIS", "door": 4,
        "layout": "Memphis_EmbalmersHouse",
        "render": "egypt_memphis_embalmers_house.png",
        "floor": "flags",
        "wall": "brick",
        "grid": _grid(11, 8),
        "rugs": [],
        "stamps": [
            ("jars", 0, 2),
            ("natron", 1, 2),
            ("natron", 2, 2),
            ("canopic", 4, 2),
            ("canopic", 5, 2),
            ("anubis", 7, 1),
            ("lamp", 8, 1),
            ("resin_pot", 10, 2),
            ("natron_table", 1, 4),
            ("natron_table", 6, 4),
            ("linen_rolls", 0, 6),
            ("jar", 10, 5),
            ("chest", 10, 6),
            ("mat", 5, 7),
        ],
        "exit": [(5, 7), (6, 7)],
        "people": [
            dict(id="LOCALID_EMBALMER_KHAY", gfx=EMBALMER, at=(4, 5), face="south",
                 script="Memphis_EmbalmersHouse_EventScript_Khay", label="Khay the embalmer"),
        ],
        "signs": [
            dict(script="Memphis_EmbalmersHouse_EventScript_Bundle", at=(2, 4), read=(2, 5, "north"),
                 label="the wrapped bundle"),
            dict(script="Memphis_EmbalmersHouse_EventScript_Canopic", at=(4, 2), read=(4, 3, "north"),
                 label="the canopic jars"),
            dict(script="Memphis_EmbalmersHouse_EventScript_Anubis", at=(7, 2), read=(7, 3, "north"),
                 label="the jackal mask"),
            dict(script="Memphis_EmbalmersHouse_EventScript_Linen", at=(0, 6), read=(1, 6, "west"),
                 label="the linen basket"),
        ],
    },
}

FACE = {"south": "MOVEMENT_TYPE_FACE_DOWN", "north": "MOVEMENT_TYPE_FACE_UP",
        "west": "MOVEMENT_TYPE_FACE_LEFT", "east": "MOVEMENT_TYPE_FACE_RIGHT"}
PLAYER_FACING = {"north": "BG_EVENT_PLAYER_FACING_NORTH", "south": "BG_EVENT_PLAYER_FACING_SOUTH",
                 "east": "BG_EVENT_PLAYER_FACING_EAST", "west": "BG_EVENT_PLAYER_FACING_WEST"}


def _spots(spec):
    spots = [("warp", f"door mat back to {spec['town']} (warp {spec['door']})", list(spec["exit"]))]
    for p in spec["people"]:
        if p.get("perch"):
            spots.append(("perch", p["label"], p["at"], p["perch"]))
        elif p.get("counter"):
            spots.append(("counter", p["label"], p["at"]))
        else:
            spots.append(("npc", p["label"], p["at"], p["face"]))
    for s in spec["signs"]:
        spots.append(("bg", s["label"], s["at"], s["read"]))
    return spots


for _spec in ROOMS.values():
    _spec["spots"] = _spots(_spec)


def write_maps():
    """Write each room's map.json events (and music) from ROOMS."""
    for name, spec in ROOMS.items():
        folder = spec["map"].replace("MAP_", "")
        path = ROOT / "data/maps" / spec["layout"] / "map.json"
        data = json.loads(path.read_text())
        assert data["id"] == spec["map"], f"{path}: id {data['id']} != {spec['map']}"
        if spec.get("music"):
            data["music"] = spec["music"]
        objs = []
        for p in spec["people"]:
            o = {}
            if p.get("id"):
                o["local_id"] = p["id"]
            o.update({
                "graphics_id": p["gfx"],
                "x": p["at"][0],
                "y": p["at"][1],
                "elevation": 3,
                "movement_type": p.get("move", FACE[p["face"]]),
                "movement_range_x": p.get("range", (0, 0))[0],
                "movement_range_y": p.get("range", (0, 0))[1],
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": "0",
                "script": p["script"],
                "flag": p.get("flag", "0"),
            })
            objs.append(o)
        data["object_events"] = objs
        data["warp_events"] = [{"x": x, "y": y, "elevation": 0, "dest_map": spec["town"],
                                "dest_warp_id": str(spec["door"])} for (x, y) in spec["exit"]]
        data["coord_events"] = []
        data["bg_events"] = [{"type": "sign", "x": s["at"][0], "y": s["at"][1], "elevation": 0,
                              "player_facing_dir": PLAYER_FACING[s["read"][2]], "script": s["script"]}
                             for s in spec["signs"]]
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        print(f"egypt_rooms: {spec['layout']}/map.json: {len(objs)} people, {len(spec['signs'])} signs")


def main(argv=None):
    sys.path.insert(0, str(ROOT / "tools/ichor/art"))
    import per_build
    per_build.main(argv)
    if not (argv and "--no-compile" in argv):
        write_maps()


if __name__ == "__main__":
    main(sys.argv[1:])
