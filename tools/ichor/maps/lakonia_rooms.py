#!/usr/bin/env python3
"""Lakonia's fifteen rooms: Gytheion's five and Lakonia's ten (Act III).

Every house is a home and every interior is unique (design/MAP_DESIGN.md §2).
Who is in each room and what happens there is in design/phase4/SCRIPT.md,
Part 2 (Gytheion, Lakonia); the plans and the render-critique passes are in
design/phase4/ROOMS_lakonia.md.

The rooms are composed with ergasteria_build.py's machinery from
tools/ichor/art/lakonia_rooms_art.py (oikia's palettes, oikia's and limen's
furniture, and the pieces these rooms needed drawn) into three secondaries:
  oikia_gytheion  Gytheion's five rooms
  oikia_lakonia   Lampito's, Gylippos's, Chilon's and Lichas's houses, the syssition
  civic_lakonia   Lakonia's Asclepeion and Agora, the agoge, the palaestra, Orthia

Room format: aegina_homes.py's (grid, floor, wall, stamps, rugs, spots) plus
"set", "floors", "walls", "blocked" and "variants" (ergasteria_build.py).
Each room's warps 0 and 1 are its door mat, back to the outdoor warp in DOORS.
The builder also writes the metatile labels scripts swap (LABELS) to
include/constants/metatile_labels.h, and each room's warps to its map.json.

  /usr/bin/python3 tools/ichor/maps/lakonia_rooms.py [--no-compile] [--preview DIR]
"""
import json
import re
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
ROOMS_DOC = ROOT / "design/phase4/ROOMS_lakonia.md"
IMG = ROOT / "design/phase4/img/rooms_lakonia"

# the outdoor warp each room's mat returns to (the outdoor builder lays the doors)
DOORS = {
    "Gytheion_Asclepeion": ("MAP_GYTHEION", 0), "Gytheion_Dyeworks": ("MAP_GYTHEION", 1),
    "Gytheion_LysandrosHouse": ("MAP_GYTHEION", 2), "Gytheion_TimaiaHouse": ("MAP_GYTHEION", 3),
    "Gytheion_KranaiShrine": ("MAP_GYTHEION", 4),
    "Lakonia_Asclepeion": ("MAP_LAKONIA", 0), "Lakonia_Agora": ("MAP_LAKONIA", 1),
    "Lakonia_LampitosHouse": ("MAP_LAKONIA", 2), "Lakonia_GylipposHouse": ("MAP_LAKONIA", 3),
    "Lakonia_Syssition": ("MAP_LAKONIA", 4), "Lakonia_Agoge": ("MAP_LAKONIA", 5),
    "Lakonia_Palaestra": ("MAP_LAKONIA", 6), "Lakonia_Orthia": ("MAP_LAKONIA", 7),
    "Lakonia_ChilonHouse": ("MAP_LAKONIA", 8), "Lakonia_LichasHouse": ("MAP_LAKONIA", 9),
}


def room(layout, title, set_, floor, wall, grid, stamps, spots, **kw):
    spec = {"set": set_, "title": title,
            "map": "MAP_" + re.sub(r"(?<=[a-z])(?=[A-Z])", "_", layout).upper(),
            "layout": layout, "render": f"{layout}.png", "floor": floor, "wall": wall, "grid": grid,
            "rugs": kw.pop("rugs", []), "stamps": stamps, "spots": spots}
    spec.update(kw)
    return spec


def box(w, h, wall_rows=2):
    return ["W" * w] * wall_rows + ["." * w for _ in range(h - wall_rows)]


ROOMS = {}

# ======================================================================
# Gytheion (oikia_gytheion)
# ======================================================================

# The Asclepeion, built into the little theater's stage-building: a long narrow
# hall. Painted scenery flats still lean on the back wall (a palace, a sea); the
# healer stands at the old ticket counter with the spring basin at her right
# hand; two windows look out over the front rows, where patients sit in the
# sun. The Pithos stands at the far end.
ROOMS["Gytheion_Asclepeion"] = room(
    "Gytheion_Asclepeion", "The Asclepeion, Gytheion (the stage-building)", "oikia_gytheion",
    "flags", "stone", box(16, 7),
    [("flat_palace", 0, 0), ("flat_sea", 2, 0), ("lampstand", 4, 1),
     ("basin_stone", 5, 1), ("mask_pegs", 7, 1), ("tickets_L", 6, 3), ("tickets_M", 7, 3), ("tickets_R", 8, 3),
     ("theater_window", 10, 0), ("theater_window", 12, 0), ("pithos", 15, 1),
     ("bench", 10, 4), ("bench", 12, 4), ("myrtle", 0, 4), ("amphora", 15, 4),
     ("mat", 7, 6)],
    [("warp", "the door to the quay (south-arrow mat)", [(7, 6), (8, 6)]),
     ("npc", "the healer, at the old ticket counter", (7, 2), "south"),
     ("npc", "a fisherman with his arm in a sling, on the front bench", (11, 5), "north"),
     ("bg", "the scenery flat: a palace", (1, 1), (1, 2, "north")),
     ("bg", "the scenery flat: the sea", (3, 1), (3, 2, "north")),
     ("bg", "the window over the front rows", (11, 1), (11, 2, "north")),
     ("bg", "the Pithos", (15, 2), (15, 3, "north"))])

# The dye-works: a stone shed open to the sea at its east end. Lead vats steam
# over low fires; crushed murex is heaped in the corner; wool hangs from the
# rafters in every shade from pink to near-black, and one finished hank of true
# purple waits on a stool under a cloth.
ROOMS["Gytheion_Dyeworks"] = room(
    "Gytheion_Dyeworks", "The dye-works, Gytheion", "oikia_gytheion",
    "flags", "stone",
    ["WWWWWWWWWWW~~", "WWWWWWWWWWW~~"] + ["...........~~"] * 6,
    [("skeins", 0, 0), ("skeins", 4, 0), ("skeins", 8, 0),
     ("vat", 1, 2), ("vat", 5, 2), ("vat", 1, 5),
     ("shell_heap", 9, 2), ("hank_stool", 9, 6), ("amphora_plain", 10, 5),
     ("mat", 5, 7)],
    [("warp", "the door to the beach (south-arrow mat)", [(5, 7), (6, 7)]),
     ("npc", "Porphyris, purple to the elbows", (4, 5), "east"),
     ("bg", "a lead vat", (5, 3), (5, 4, "north")),
     ("bg", "the shell heap", (9, 3), (8, 3, "east")),
     ("bg", "the hank under a cloth", (9, 6), (8, 6, "east"))],
    floors={"~": "sea"}, blocked="~")

# Lysandros's house on the harbor wall: a window that's mostly sea, the gulf
# scratched into the plaster with every rock and current, three model triremes
# on a shelf, and a bronze ram for a doorstop.
ROOMS["Gytheion_LysandrosHouse"] = room(
    "Gytheion_LysandrosHouse", "Lysandros's house, Gytheion", "oikia_gytheion",
    "boards", "blue", box(10, 8),
    [("gulf_map", 0, 0), ("sea_window", 4, 0), ("trireme_shelf", 7, 0),
     ("kline", 8, 3), ("table", 4, 3), ("klismos_r", 3, 3), ("oars", 0, 3),
     ("water_jar", 9, 5), ("ram", 6, 7), ("mat", 4, 7)],
    [("warp", "the door to the quay (south-arrow mat)", [(4, 7), (5, 7)]),
     ("npc", "Lysandros, the old harbor-master", (6, 3), "west"),
     ("bg", "the gulf scratched into the plaster", (1, 1), (1, 2, "north")),
     ("bg", "the window that's mostly sea", (4, 1), (4, 2, "north")),
     ("bg", "the model triremes", (7, 1), (7, 2, "north")),
     ("bg", "the bronze ram doorstop", (6, 7), (6, 6, "south"))])

# Timaia's house smells of bread: the oven built into the corner, nets mended
# and folded on a bench, a child's wooden spear behind the door, and on the
# table a cloth over something fig-shaped.
ROOMS["Gytheion_TimaiaHouse"] = room(
    "Gytheion_TimaiaHouse", "Timaia's house, Gytheion", "oikia_gytheion",
    "terracotta", "red", box(9, 7),
    [("bread_oven", 0, 1), ("window", 3, 0), ("bench_nets", 5, 2), ("jar_shelf", 7, 0),
     ("cake_table", 3, 4), ("stool", 2, 4), ("pithos", 8, 4), ("toy_spear", 6, 5),
     ("mat", 4, 6)],
    [("warp", "the door to the lane (south-arrow mat)", [(4, 6), (5, 6)]),
     ("npc", "Timaia, by her table", (5, 4), "west"),
     ("bg", "the bread oven", (1, 2), (1, 3, "north")),
     ("bg", "the fig cake under its cloth", (4, 4), (4, 5, "north")),
     ("bg", "the child's wooden spear", (6, 5), (7, 5, "west")),
     ("bg", "the folded nets", (6, 2), (6, 3, "north"))])

# The shrine on Kranai: one whitewashed room. Two clay doves in the niche, a
# hundred tiny votive sandals on strings, and a bench under the window that
# faces Kythera.
ROOMS["Gytheion_KranaiShrine"] = room(
    "Gytheion_KranaiShrine", "The shrine on Kranai, Gytheion", "oikia_gytheion",
    "flags", "white", box(9, 7),
    [("sandals_a", 0, 0), ("window", 2, 0), ("dove_niche", 4, 0), ("window", 6, 0),
     ("sandals_b", 7, 0), ("bench", 6, 2), ("myrtle", 0, 2), ("myrtle", 8, 4),
     ("mat", 3, 6)],
    [("warp", "the door to the islet (south-arrow mat)", [(3, 6), (4, 6)]),
     ("npc", "Klymene, the shrine-keeper", (2, 3), "south"),
     ("bg", "the doves in the niche", (4, 1), (4, 2, "north")),
     ("bg", "the votive sandals", (1, 1), (1, 2, "north")),
     ("bg", "the bench under the window, toward Kythera", (6, 2), (5, 2, "east"))])

# ======================================================================
# Lakonia's homes (oikia_lakonia)
# ======================================================================

# Lampito's kitchen: a cold hearth, a loom with a small red cloak, a plain table
# and two stools, a chest under the loom, and two grave-stelai painted on the
# plaster. Kleon sits at the table. The hearth is lit in III-5E (variant "lit").
ROOMS["Lakonia_LampitosHouse"] = room(
    "Lakonia_LampitosHouse", "Lampito's house, Lakonia", "oikia_lakonia",
    "earth", "lakon", box(11, 9),
    [("loom_cloak", 0, 0), ("chest", 0, 3), ("soot", 4, 0), ("hearth_cold", 4, 2),
     ("stele_agis", 7, 0), ("stele_swallow", 9, 0), ("amphora_plain", 10, 2),
     ("wall_worn", 3, 1), ("wall_worn", 10, 0), ("pots", 6, 2),
     ("stool_seat", 5, 5), ("table", 6, 5), ("stool_seat", 8, 5),
     ("water_jar", 10, 6), ("mat", 5, 8)],
    [("warp", "the door to the yard (south-arrow mat)", [(5, 8), (6, 8)]),
     ("npc", "Kleon, at the table", (5, 5), "east"),
     ("npc", "Rhea, just inside the door", (5, 7), "north"),
     ("npc", "Alethea, by the door", (8, 7), "north"),
     ("bg", "the loom", (1, 2), (2, 2, "west")),
     ("bg", "the chest under the loom", (1, 4), (2, 4, "west")),
     ("bg", "the hearth", (4, 3), (4, 4, "north")),
     ("bg", "the stele: AGIS", (7, 1), (7, 2, "north")),
     ("bg", "the stele: a swallow", (9, 1), (9, 2, "north"))],
    variants={"lit": {"swap": {"hearth_cold": "hearth_lit"},
                      "script": "LakoniaLampito_EventScript_SetHearthLit"}})

# Gylippos's house: almost empty. A sleeping mat, a stool with a leather strap
# coiled on it, a water jar, and on the wall a dozen identical scytale staffs.
ROOMS["Lakonia_GylipposHouse"] = room(
    "Lakonia_GylipposHouse", "Gylippos's house, Lakonia", "oikia_lakonia",
    "earth", "lakon", box(7, 7),
    [("staff_rack", 2, 0), ("sleeping_mat", 0, 3), ("stool_strap", 5, 3),
     ("water_jar", 6, 4), ("wall_worn", 0, 1), ("wall_worn", 6, 0), ("mat", 3, 6)],
    [("warp", "the door to the lane (south-arrow mat)", [(3, 6), (4, 6)]),
     ("npc", "Gylippos, standing (the stool is his)", (4, 3), "south"),
     ("bg", "the elders' staffs", (3, 1), (3, 2, "north")),
     ("bg", "the stool and the strap", (5, 3), (5, 4, "north"))])

# Chilon's house: every wall scratched with sayings, one or two words each, in
# a hundred hands, floor to ceiling; one shard on a shelf that says IF.
ROOMS["Lakonia_ChilonHouse"] = room(
    "Lakonia_ChilonHouse", "Chilon's house, Lakonia", "oikia_lakonia",
    "earth", "sayings", box(8, 7),
    [("pallet", 0, 2), ("if_shelf", 5, 0), ("stool", 3, 3), ("table_round", 4, 3),
     ("kalathos", 7, 4), ("lampstand", 7, 2), ("mat", 3, 6)],
    [("warp", "the door to the lane (south-arrow mat)", [(3, 6), (4, 6)]),
     ("npc", "Chilon, a very old man", (2, 3), "south"),
     ("bg", "the shard that says IF", (5, 1), (5, 2, "north")),
     ("bg", "the sayings on the wall", (2, 1), (2, 2, "north"))])

# Lichas's house: the only house in Lakonia with cushions. A hearth, a guest bed
# behind a curtain, a bronze tripod from Olympia with someone else's name on it,
# and a basket of figs.
ROOMS["Lakonia_LichasHouse"] = room(
    "Lakonia_LichasHouse", "Lichas's house, Lakonia", "oikia_lakonia",
    "earth", "lakon", box(10, 8),
    [("soot", 0, 0), ("hearth_lit", 0, 2), ("tripod", 3, 0),
     ("curtain_bed", 8, 1), ("cushions", 4, 5), ("cushions", 6, 5), ("wall_worn", 6, 1), ("table_round", 5, 3),
     ("figs", 6, 3), ("amphora", 9, 4), ("mat", 4, 7)],
    [("warp", "the door to the lane (south-arrow mat)", [(4, 7), (5, 7)]),
     ("npc", "Lichas, the host", (4, 2), "south"),
     ("bg", "the tripod with someone else's name on it", (3, 1), (3, 2, "north")),
     ("bg", "the guest bed behind its curtain", (8, 2), (7, 2, "east")),
     ("bg", "the figs", (6, 3), (6, 2, "south"))],
    rugs=[("red", 3, 5, 5, 2)])

# The syssition: one long low room, a plank table for fifteen men with each
# man's clay cup on a peg above his place, and the black cauldron over a fire at
# the far end. A barrel of barley in the corner. No windows.
ROOMS["Lakonia_Syssition"] = room(
    "Lakonia_Syssition", "The syssition, Lakonia", "oikia_lakonia",
    "earth", "smoke", box(15, 7),
    [("barley", 0, 1), ("cup_pegs", 1, 1), ("cup_pegs", 3, 1), ("cup_pegs", 5, 1),
     ("cup_pegs", 7, 1), ("cup_pegs", 9, 1), ("cauldron", 12, 2),
     ("stool", 2, 3), ("stool", 4, 3), ("stool", 6, 3), ("stool", 8, 3),
     ("plank_L", 1, 4), ("plank_M", 2, 4), ("plank_M", 3, 4), ("plank_M", 4, 4),
     ("plank_M", 5, 4), ("plank_M", 6, 4), ("plank_M", 7, 4), ("plank_M", 8, 4),
     ("plank_R", 9, 4), ("stool", 3, 5), ("stool", 5, 5), ("stool", 7, 5),
     ("amphora_plain", 14, 2), ("mat", 6, 6)],
    [("warp", "the door to the agora (south-arrow mat)", [(6, 6), (7, 6)]),
     ("npc", "Dexippos, the cook", (11, 3), "south"),
     ("bg", "the black cauldron", (12, 3), (12, 4, "north")),
     ("bg", "the cups on their pegs", (4, 1), (4, 2, "north"))])

# ======================================================================
# Lakonia's public rooms (civic_lakonia)
# ======================================================================

# The Asclepeion: a bare stone room with one long bench and nothing on the
# walls. The counter is a plank on two stones; a bowl of cold water on it.
ROOMS["Lakonia_Asclepeion"] = room(
    "Lakonia_Asclepeion", "The Asclepeion, Lakonia", "civic_lakonia",
    "flags", "stone", box(9, 7),
    [("basin_stone", 2, 1), ("stone_counter_L", 3, 3), ("stone_counter_M", 4, 3),
     ("stone_counter_R", 5, 3), ("pithos", 8, 1), ("bench", 6, 5), ("mat", 3, 6)],
    [("warp", "the door to the road (south-arrow mat)", [(3, 6), (4, 6)]),
     ("npc", "the healer, a Lakonian woman of very few words", (4, 2), "south"),
     ("bg", "the Pithos", (8, 2), (8, 3, "north")),
     ("bg", "the spring basin", (2, 2), (1, 2, "east"))])

# The Agora: a stall with a set of great scales, because Lakonia pays in iron
# bars, and a pile of them stacked by the door like firewood.
ROOMS["Lakonia_Agora"] = room(
    "Lakonia_Agora", "The Agora, Lakonia", "civic_lakonia",
    "earth", "lakon", box(9, 7),
    [("great_scales", 5, 0), ("stall_L", 2, 3), ("stall_M", 3, 3), ("stall_R", 4, 3),
     ("sack", 1, 2), ("amphora_plain", 0, 1), ("iron_bars", 6, 5), ("wall_worn", 8, 1), ("mat", 3, 6)],
    [("warp", "the door to the road (south-arrow mat)", [(3, 6), (4, 6)]),
     ("npc", "the stallkeeper, who weighs everything", (3, 2), "south"),
     ("bg", "the great scales", (5, 1), (5, 2, "north")),
     ("bg", "the iron bars", (6, 5), (6, 4, "south"))])

# The agoge's barracks: thirty reed mats in rows on a beaten floor, a rack of
# practice spears, red cloaks on pegs, and at the far end Archidamos's stool
# under the herd's names, some struck through.
_mats = [("reed_mat" if (x + y // 2) % 3 else "reed_mat_b", x, y) for y in (4, 6, 8) for x in range(2, 12)]
ROOMS["Lakonia_Agoge"] = room(
    "Lakonia_Agoge", "The agoge, Lakonia", "civic_lakonia",
    "earth", "lakon", box(16, 10),
    [("cloak_pegs", 0, 0), ("cloak_pegs", 2, 0), ("cloak_pegs", 4, 0), ("cloak_pegs", 6, 0),
     ("cloak_pegs", 8, 0), ("cloak_pegs", 10, 0), ("names_list", 13, 0), ("spear_rack", 14, 4),
     ("stool", 13, 3)] + _mats + [("mat", 7, 9)],
    [("warp", "the door to the yard (south-arrow mat)", [(7, 9), (8, 9)]),
     ("npc", "Archidamos, the boys' master, by his stool", (12, 3), "south"),
     ("npc", "a cadet, sitting on his mat", (5, 6), "south"),
     ("bg", "the herd's names", (14, 1), (14, 2, "north")),
     ("bg", "the practice spears", (14, 5), (13, 5, "east")),
     ("bg", "the red cloaks", (3, 1), (3, 2, "north"))])

# The palaestra: an open court with a stone porch, oil flasks and scrapers on
# hooks, a sandpit for wrestling, a bench of folded cloaks, and six olive
# crowns, dried brown, nailed above the door.
ROOMS["Lakonia_Palaestra"] = room(
    "Lakonia_Palaestra", "The palaestra, Lakonia", "civic_lakonia",
    "flags", "stone",
    ["WWWWWWWWWWWWW", "WWWWWWWWWWWWW", ".............", ".SSSSSSS.....", ".SSSSSSS.....",
     ".SSSSSSS.....", ".SSSSSSS.....", ".............", "............."],
    [("oil_hooks", 0, 1), ("crowns", 4, 0), ("oil_hooks", 7, 1),
     ("column", 9, 2), ("column", 12, 2), ("cloak_bench", 10, 5), ("louterion", 10, 2),
     ("mat", 5, 8)],
    [("warp", "the door to the sands (south-arrow mat)", [(5, 8), (6, 8)]),
     ("npc", "Hipposthenes, six times crowned", (4, 4), "south"),
     ("bg", "the six olive crowns", (5, 1), (5, 2, "north")),
     ("bg", "the oil flasks and scrapers", (1, 1), (1, 2, "north")),
     ("bg", "the bench of folded cloaks", (10, 5), (10, 6, "north"))],
    floors={"S": "sand"})

# The sanctuary of Artemis Orthia: a small court on the marshy bank, willows
# growing right up to the steps, the long stone altar set with round cheeses,
# the goddess's wooden image bound upright, low benches for watchers. The
# cheese game: two cadets watch the court (coord triggers on their lines).
ROOMS["Lakonia_Orthia"] = room(
    "Lakonia_Orthia", "The sanctuary of Artemis Orthia, Lakonia", "civic_lakonia",
    "court", "stone", box(15, 11),
    [("willow", 0, 0), ("xoanon", 7, 0), ("willow", 13, 0),
     ("altar_cheese_L", 5, 3), ("altar_M", 6, 3), ("altar_cheese_M", 7, 3), ("altar_M", 8, 3),
     ("altar_cheese_R", 9, 3),
     ("bench", 1, 8), ("bench", 12, 8), ("myrtle", 0, 6), ("myrtle", 14, 6),
     ("reeds", 0, 4), ("reeds", 14, 4), ("reeds", 0, 9), ("reeds", 14, 9), ("reeds", 0, 3), ("mat", 7, 10)],
    [("warp", "the gate to the river bank (south-arrow mat)", [(7, 10), (8, 10)]),
     ("npc", "Kleta, the priestess", (9, 8), "west"),
     ("npc", "a watching cadet (west)", (2, 4), "east"),
     ("npc", "a watching cadet (east)", (12, 6), "west"),
     ("bg", "the goddess's wooden image", (7, 1), (7, 2, "north")),
     ("bg", "the cheese, west end", (5, 3), (5, 2, "south")),
     ("bg", "the cheese, middle", (7, 3), (7, 2, "south")),
     ("bg", "the cheese, east end", (9, 3), (9, 2, "south"))],
    variants={"bare": {"swap": {"altar_cheese_L": "altar_L", "altar_cheese_M": "altar_M",
                                "altar_cheese_R": "altar_R"},
                       "script": "LakoniaOrthia_EventScript_AltarBare"}})

# Metatile labels for scripts: (label, room, x, y[, variant]).
LABELS = [
    ("METATILE_OikiaLakonia_Hearth_Cold_TL", "Lakonia_LampitosHouse", 4, 2, None),
    ("METATILE_OikiaLakonia_Hearth_Cold_TR", "Lakonia_LampitosHouse", 5, 2, None),
    ("METATILE_OikiaLakonia_Hearth_Cold_BL", "Lakonia_LampitosHouse", 4, 3, None),
    ("METATILE_OikiaLakonia_Hearth_Cold_BR", "Lakonia_LampitosHouse", 5, 3, None),
    ("METATILE_OikiaLakonia_Hearth_Lit_TL", "Lakonia_LampitosHouse", 4, 2, "lit"),
    ("METATILE_OikiaLakonia_Hearth_Lit_TR", "Lakonia_LampitosHouse", 5, 2, "lit"),
    ("METATILE_OikiaLakonia_Hearth_Lit_BL", "Lakonia_LampitosHouse", 4, 3, "lit"),
    ("METATILE_OikiaLakonia_Hearth_Lit_BR", "Lakonia_LampitosHouse", 5, 3, "lit"),
    ("METATILE_CivicLakonia_Altar_West", "Lakonia_Orthia", 5, 3, "bare"),
    ("METATILE_CivicLakonia_Altar_Middle", "Lakonia_Orthia", 7, 3, "bare"),
    ("METATILE_CivicLakonia_Altar_East", "Lakonia_Orthia", 9, 3, "bare"),
    ("METATILE_CivicLakonia_Altar_Cheese_West", "Lakonia_Orthia", 5, 3, None),
    ("METATILE_CivicLakonia_Altar_Cheese_Middle", "Lakonia_Orthia", 7, 3, None),
    ("METATILE_CivicLakonia_Altar_Cheese_East", "Lakonia_Orthia", 9, 3, None),
]


# ======================================================================
# The build
# ======================================================================

SETS = {
    "oikia_gytheion": ("gTileset_OikiaGytheion", ("flags", "boards", "terracotta", "sea"),
                       ("stone", "blue", "red", "white")),
    "oikia_lakonia": ("gTileset_OikiaLakonia", ("earth",), ("lakon", "smoke", "sayings")),
    "civic_lakonia": ("gTileset_CivicLakonia", ("flags", "earth", "sand", "court"), ("stone", "lakon")),
}


def art_for(A, floors, walls):
    """The art module as one set sees it: only the floors and walls its rooms
    use, so the bare pieces don't spend tiles another set needs."""
    return types.SimpleNamespace(PALETTES=A.PALETTES, FLOORS={k: A.FLOORS[k] for k in floors},
                                 WALLS={k: A.WALLS[k] for k in walls}, VOID=A.VOID,
                                 RUGS=A.RUGS, STAMPS=A.STAMPS)


# ----------------------------------------------------------------------
# Events: people, signs and triggers, at the spots above.
# ----------------------------------------------------------------------

FACE = {"south": "MOVEMENT_TYPE_FACE_DOWN", "north": "MOVEMENT_TYPE_FACE_UP",
        "west": "MOVEMENT_TYPE_FACE_LEFT", "east": "MOVEMENT_TYPE_FACE_RIGHT"}


def o(gfx, x, y, script, face="south", local_id=None, flag="0", move=None):
    if not gfx.startswith("OBJ_EVENT_GFX_"):
        gfx = "OBJ_EVENT_GFX_" + gfx
    e = {"graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": move or FACE[face],
         "movement_range_x": 0, "movement_range_y": 0, "trainer_type": "TRAINER_TYPE_NONE",
         "trainer_sight_or_berry_tree_id": "0", "script": script, "flag": flag}
    return {"local_id": local_id, **e} if local_id else e


def b(x, y, script):
    return {"type": "sign", "x": x, "y": y, "elevation": 0,
            "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY", "script": script}


def t(x, y, script, var="VAR_TEMP_1", value=1):
    return {"type": "trigger", "x": x, "y": y, "elevation": 3, "var": var, "var_value": str(value),
            "script": script}


def _events():
    G, L = "Gytheion", "Lakonia"
    E = {}
    p = "Gytheion_Asclepeion_EventScript_"
    E["Gytheion_Asclepeion"] = (
        [o("ICHOR_HEALER", 7, 2, p + "Healer", local_id="LOCALID_GYTHEION_HEALER"),
         o("SPECIES(PANACOIL)", 8, 2, p + "Panacoil"),
         o("ICHOR_FISHER", 11, 5, p + "Fisherman", "north")],
        [b(1, 1, p + "FlatPalace"), b(3, 1, p + "FlatSea"), b(11, 1, p + "Window"),
         b(13, 1, p + "Window"), b(15, 2, p + "Pithos")], [])
    p = "Gytheion_Dyeworks_EventScript_"
    E["Gytheion_Dyeworks"] = (
        [o("ICHOR_WOMAN", 4, 5, p + "Porphyris", "east", local_id="LOCALID_DYEWORKS_PORPHYRIS")],
        [b(5, 3, p + "Vat"), b(1, 3, p + "Vat"), b(1, 6, p + "Vat"), b(9, 3, p + "Shells"),
         b(9, 6, p + "Hank"), b(4, 1, p + "Skeins")], [])
    p = "Gytheion_LysandrosHouse_EventScript_"
    E["Gytheion_LysandrosHouse"] = (
        [o("ICHOR_ELDER_M", 6, 3, p + "Lysandros", "west", local_id="LOCALID_LYSANDROS")],
        [b(1, 1, p + "GulfMap"), b(0, 1, p + "GulfMap"), b(2, 1, p + "GulfMap"), b(4, 1, p + "Window"),
         b(5, 1, p + "Window"), b(7, 1, p + "Triremes"), b(8, 1, p + "Triremes"), b(6, 7, p + "Ram")], [])
    p = "Gytheion_TimaiaHouse_EventScript_"
    E["Gytheion_TimaiaHouse"] = (
        [o("ICHOR_MOM", 5, 4, p + "Timaia", "west", local_id="LOCALID_TIMAIA")],
        [b(1, 2, p + "Oven"), b(0, 2, p + "Oven"), b(4, 4, p + "Cake"), b(3, 4, p + "Cake"),
         b(6, 5, p + "Spear"), b(6, 2, p + "Nets"), b(5, 2, p + "Nets")], [])
    p = "Gytheion_KranaiShrine_EventScript_"
    E["Gytheion_KranaiShrine"] = (
        [o("ICHOR_PRIESTESS", 2, 3, p + "Klymene", local_id="LOCALID_KLYMENE")],
        [b(4, 1, p + "Doves"), b(1, 1, p + "Sandals"), b(8, 1, p + "Sandals"),
         b(6, 2, p + "Bench"), b(7, 2, p + "Bench")], [])
    p = "LakoniaLampito_EventScript_"
    E["Lakonia_LampitosHouse"] = (
        [o("ICHOR_KLEON", 5, 5, p + "Kleon", "east", local_id="LOCALID_LAMPITO_KLEON"),
         o("VAR_1", 5, 7, p + "Rhea", "north", local_id="LOCALID_LAMPITO_RHEA"),
         o("ICHOR_ALETHEA", 8, 7, p + "Alethea", "north", local_id="LOCALID_LAMPITO_ALETHEA"),
         o("ICHOR_TABLET", 6, 5, p + "Helmet", local_id="LOCALID_LAMPITO_HELMET"),
         o("ICHOR_TABLET", 7, 5, p + "Tablet", local_id="LOCALID_LAMPITO_TABLET")],
        [b(7, 1, p + "Stelai"), b(9, 1, p + "Stelai"), b(1, 2, p + "Loom"), b(1, 4, p + "Chest"),
         b(0, 4, p + "Chest"), b(4, 3, p + "Hearth"), b(5, 3, p + "Hearth")], [])
    p = "Lakonia_GylipposHouse_EventScript_"
    E["Lakonia_GylipposHouse"] = (
        [o("ICHOR_ELDER_M", 4, 3, p + "Gylippos", local_id="LOCALID_GYLIPPOS_HOME")],
        [b(2, 1, p + "Staffs"), b(3, 1, p + "Staffs"), b(4, 1, p + "Staffs"), b(5, 3, p + "Stool")], [])
    p = "Lakonia_ChilonHouse_EventScript_"
    E["Lakonia_ChilonHouse"] = (
        [o("ICHOR_AIAKIDES", 2, 3, p + "Chilon", local_id="LOCALID_CHILON")],
        [b(5, 1, p + "Shard"), b(1, 1, p + "Sayings"), b(2, 1, p + "Sayings"), b(3, 1, p + "Sayings"),
         b(6, 1, p + "Sayings")], [])
    p = "Lakonia_LichasHouse_EventScript_"
    E["Lakonia_LichasHouse"] = (
        [o("ICHOR_MAN", 4, 2, p + "Lichas", local_id="LOCALID_LICHAS")],
        [b(3, 1, p + "Tripod"), b(8, 2, p + "Bed"), b(9, 2, p + "Bed"), b(6, 3, p + "Figs")], [])
    p = "Lakonia_Syssition_EventScript_"
    E["Lakonia_Syssition"] = (
        [o("ICHOR_MAN", 11, 3, p + "Dexippos", local_id="LOCALID_DEXIPPOS"),
         o("ICHOR_HOPLITE", 4, 5, p + "Soldier", "north")],
        [b(12, 3, p + "Cauldron"), b(13, 3, p + "Cauldron"), b(4, 1, p + "Cups"), b(2, 1, p + "Cups"),
         b(6, 1, p + "Cups"), b(8, 1, p + "Cups")], [])
    p = "Lakonia_Asclepeion_EventScript_"
    E["Lakonia_Asclepeion"] = (
        [o("ICHOR_HEALER", 4, 2, p + "Healer", local_id="LOCALID_LAKONIA_HEALER"),
         o("SPECIES(PANACOIL)", 5, 2, p + "Panacoil")],
        [b(8, 2, p + "Pithos"), b(2, 2, p + "Basin")], [])
    p = "Lakonia_Agora_EventScript_"
    E["Lakonia_Agora"] = (
        [o("ICHOR_MERCHANT", 3, 2, p + "Clerk", local_id="LOCALID_LAKONIA_CLERK")],
        [b(5, 1, p + "Scales"), b(6, 1, p + "Scales"), b(6, 5, p + "Bars"), b(7, 5, p + "Bars")], [])
    p = "Lakonia_Agoge_EventScript_"
    E["Lakonia_Agoge"] = (
        [o("ICHOR_HOPLITE", 12, 3, p + "Archidamos", local_id="LOCALID_ARCHIDAMOS"),
         o("ICHOR_YOUTH_M", 5, 6, p + "Cadet"),
         o("ICHOR_YOUTH_M", 9, 8, p + "CadetSleeping", "west")],
        [b(13, 1, p + "Names"), b(14, 1, p + "Names"), b(14, 5, p + "Spears"), b(1, 1, p + "Cloaks"),
         b(3, 1, p + "Cloaks"), b(5, 1, p + "Cloaks"), b(7, 1, p + "Cloaks"), b(9, 1, p + "Cloaks")], [])
    p = "Lakonia_Palaestra_EventScript_"
    E["Lakonia_Palaestra"] = (
        [o("ICHOR_MAN", 4, 4, p + "Hipposthenes", local_id="LOCALID_HIPPOSTHENES")],
        [b(5, 1, p + "Crowns"), b(4, 1, p + "Crowns"), b(6, 1, p + "Crowns"), b(1, 1, p + "Oil"),
         b(8, 1, p + "Oil"), b(10, 5, p + "Cloaks")], [])
    p = "LakoniaOrthia_EventScript_"
    E["Lakonia_Orthia"] = (
        [o("ICHOR_PRIESTESS", 9, 8, p + "Kleta", "west", local_id="LOCALID_KLETA"),
         o("ICHOR_YOUTH_M", 2, 4, p + "WatcherWest", "east", local_id="LOCALID_ORTHIA_WATCHER_W"),
         o("ICHOR_YOUTH_M", 12, 6, p + "WatcherEast", "west", local_id="LOCALID_ORTHIA_WATCHER_E")],
        [b(7, 1, p + "Image"), b(5, 3, p + "CheeseWest"), b(7, 3, p + "CheeseMiddle"),
         b(9, 3, p + "CheeseEast")],
        [t(x, 4, p + "SeenWest") for x in range(3, 11)] + [t(x, 6, p + "SeenEast") for x in range(4, 12)])
    return E


EVENTS = _events()


def write_events(spec):
    """Warps 0 and 1 (the mat) back outside, and the room's people, signs and
    triggers from EVENTS."""
    name = spec["layout"]
    mp = ROOT / "data/maps" / name / "map.json"
    mj = json.loads(mp.read_text())
    dest, wid = DOORS[name]
    mats = [s for s in spec["spots"] if s[0] == "warp"][0][2]
    mj["warp_events"] = [{"x": x, "y": y, "elevation": 0, "dest_map": dest, "dest_warp_id": str(wid)}
                         for (x, y) in mats]
    objs, bgs, coords = EVENTS[name]
    mj["object_events"], mj["bg_events"], mj["coord_events"] = objs, bgs, coords
    mp.write_text(json.dumps(mj, indent=2, ensure_ascii=False) + "\n")


def write_labels(entries):
    p = ROOT / "include/constants/metatile_labels.h"
    t = p.read_text()
    begin, end = "// Lakonia's rooms (Ichor), written by tools/ichor/maps/lakonia_rooms.py", "// end Lakonia's rooms"
    block = begin + "\n" + "".join(f"#define {n:<44} 0x{v:03X}\n" for n, v in entries) + end + "\n"
    if begin in t:
        a, b = t.index(begin), t.index(end) + len(end) + 1
        t = t[:a] + block + t[b:]
    else:
        i = t.rindex("#endif")
        t = t[:i] + block + "\n" + t[i:]
    p.write_text(t)


def main():
    import ergasteria_build as EB
    import lakonia_rooms_art as A
    this = sys.modules[__name__]
    EB.room_modules = lambda: [this]
    EB.IMG = IMG
    IMG.mkdir(parents=True, exist_ok=True)
    args = EB.parse_args()
    labels = []
    for name, (tileset, floors, walls) in SETS.items():
        rs = EB.RoomSet(name, tileset, art_for(A, floors, walls),
                        tiles_doc=ROOT / "design/phase4/TILES_lakonia_rooms.md",
                        default_rooms_doc=ROOMS_DOC)
        rooms, layouts = EB.build(rs, args)
        if args.no_compile:
            continue
        _, ids = EB.collect(rs, layouts)
        for (label, rname, x, y, var) in LABELS:
            if ROOMS[rname]["set"] == name:
                key = rname if var is None else f"{rname}@{var}"
                labels.append((label, ids[key][y][x]))
        for n in rooms:
            write_events(ROOMS[n])
    if labels:
        write_labels(labels)


if __name__ == "__main__":
    main()
