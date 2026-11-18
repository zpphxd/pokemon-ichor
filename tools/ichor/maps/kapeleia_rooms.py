#!/usr/bin/env python3
"""The Great Deigma (gTileset_Kapeleia) and the Nursery of Nysa (gTileset_Nysa).

Every interior is unique (design/MAP_DESIGN.md section 2). The briefs are
design/IDEAS.md's "Grand bazaar: the Great Deigma" and "Day care: the Nursery
of Nysa"; the render-and-critique passes are in design/maps/GreatDeigma.md and
design/maps/NurseryOfNysa.md.

Room format: aegina_homes.py's (grid, floors, walls, stamps, rugs, spots), as
emporion_rooms.py uses it. A stall is four stamps: an awning (3x2), its goods
(3x1, the seller standing in the middle cell) and the shared counter (3x1)
the player talks across. Spots of kind "across" are people behind a counter:
(label, their cell, (x, y, facing) the player reads them from).

  /usr/bin/python3 tools/ichor/maps/kapeleia_rooms.py      # tileset, layouts, events
  /usr/bin/python3 tools/ichor/maps/kapeleia_rooms.py --no-compile --preview DIR

Each room's exit is warp 0, the door mat: the Great Deigma back to
MAP_EMPORION_CITY (its warp 11, the stoa's east door), the nursery back to
MAP_ROUTE7_KRONIA_GROUNDS (its warp 0, the farmhouse door).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROOMS_DOC = ROOT / "design/maps/Kapeleia_rooms.md"


def stall(awning, goods, x, y):
    """A stall's stamps with its awning's top-left at (x, y): the seller
    stands at (x + 1, y + 2), the player reads them from (x + 1, y + 4)."""
    return [(f"awning_{awning}", x, y), (f"goods_{goods}", x, y + 2), ("stall_counter", x, y + 3)]


DEIGMA_STALLS = {
    # name: (awning, goods, awning's top-left)
    "Phoenician": ("purple", "phoenician", (1, 1)),
    "Egyptian": ("blue", "egyptian", (5, 1)),
    "Scythian": ("red", "scythian", (9, 1)),
    "Stones": ("green", "stones", (18, 1)),
    "Tablets": ("saffron", "tablets", (22, 1)),
    "Berries": ("red", "berries", (26, 1)),
    "Curios": ("purple", "curios", (3, 7)),
    "Spices": ("saffron", "spices", (5, 11)),
    "Pottery": ("blue", "pottery", (25, 11)),
}


def _deigma_stamps():
    s = []
    for awning, goods, (x, y) in DEIGMA_STALLS.values():
        s += stall(awning, goods, x, y)
    s += [
        # the north wall between the stalls: banners, windows, the market's law
        ("banner_purple", 4, 0), ("banner_blue", 8, 0), ("banner_green", 21, 0), ("banner_red", 25, 0),
        ("window", 0, 0), ("window", 29, 0),
        ("notice_board", 12, 0), ("window", 13, 0), ("window", 16, 0), ("notice_board", 17, 0),
        ("scales", 14, 1), ("scales", 15, 1),
        # between the stalls, goods waiting
        ("amphora", 4, 3), ("amphora_plain", 8, 3), ("sack", 21, 4), ("amphora", 25, 3),
        ("crate_stack", 0, 3), ("pithos", 29, 3),
        # the crossing: the fountain under the lantern, columns down the nave
        ("fountain", 13, 7), ("dolphin_mosaic", 13, 9),
        ("lampstand", 10, 7), ("lampstand", 19, 7),
        ("column", 11, 6), ("column", 18, 6), ("column", 11, 11), ("column", 18, 11),
        # the money-changer's trapeza, east of the fountain
        ("trapeza", 22, 8), ("amphora_rack", 26, 8), ("scales", 21, 8),
        # the west side: wool bales, carpets
        ("carpets_rolled", 0, 7), ("bales", 0, 12), ("baskets_floor", 2, 14),
        ("amphora_plain", 8, 13),
        # the east side: oil samples, crates, sacks
        ("trestle_oil", 21, 12), ("crate_stack", 29, 12), ("sack", 28, 14), ("amphora", 24, 13),
        ("trestle_grain", 18, 14), ("baskets_floor", 10, 14),
        ("mat", 14, 15),
    ]
    return s


ROOMS = {
    # ------------------------------------------------------------------
    # The Great Deigma: Emporion's covered market, through the stoa's east
    # door. A long timber-roofed hall: the sellers' stalls under striped
    # awnings along the north wall (the Phoenician's purple and glass, the
    # Egyptian's papyrus and alabaster, the Scythian's furs and gold, the
    # stones, the techniques, the berries), the market's official measures
    # and its notice boards between them; the fountain at the crossing under
    # the lantern; the curio-seller's stall west of it and the money-changer's
    # trapeza east; bales, oil and carpets down the sides; a runner from the
    # door.
    "great_deigma": {
        "set": "kapeleia",
        "title": "The Great Deigma, Emporion",
        "map": "MAP_EMPORION_CITY_GREAT_DEIGMA",
        "layout": "EmporionCity_GreatDeigma",
        "render": "emporion_great_deigma.png",
        "floor": "flags",
        "wall": "stone",
        "grid": ["W" * 30] * 2 + ["." * 30] * 14,
        "rugs": [("red", 14, 11, 2, 4)],
        "stamps": _deigma_stamps(),
        "spots": [
            ("warp", "door to Emporion (south-arrow mat)", [(14, 15), (15, 15)]),
        ] + [("across", f"the {n} stall's seller", (x + 1, y + 2), (x + 1, y + 4, "north"))
             for n, (_, _, (x, y)) in DEIGMA_STALLS.items()] + [
            ("across", "the money-changer at the trapeza", (23, 8), (23, 10, "north")),
            ("bg", "the market's notice board (west)", (12, 1), (12, 2, "north")),
            ("bg", "the market's notice board (east)", (17, 1), (17, 2, "north")),
            ("bg", "the official measures", (14, 2), (14, 3, "north")),
            ("bg", "the fountain", (14, 8), (14, 9, "north")),
        ],
    },
    # ------------------------------------------------------------------
    # The Nursery of Nysa: a farmhouse at the edge of the Kronia grounds where
    # the nymphs of Nysa, who raised the infant Dionysus, raise travelers'
    # Pokémon. Ivy along the beams; the keeper's plank counter with the loom
    # behind her; the liknon cradle with an Egg in it and baskets of Eggs
    # waiting; a hearth, the honey shelf and a krater of watered wine; a fawn
    # skin on the floor and thyrsoi stacked by the door.
    "nursery": {
        "set": "nysa",
        "title": "The Nursery of Nysa, Route 7",
        "map": "MAP_ROUTE7_NURSERY_OF_NYSA",
        "layout": "Route7_NurseryOfNysa",
        "render": "route7_nursery_of_nysa.png",
        "floor": "terracotta",
        "wall": "red",
        "grid": ["W" * 14] * 2 + ["." * 14] * 7,
        "rugs": [("blue", 0, 4, 4, 2)],
        "stamps": [
            ("window", 2, 0), ("herbs", 3, 0), ("jar_shelf", 4, 0), ("window", 6, 0), ("jar_shelf", 7, 0),
            ("ivy", 9, 0), ("window", 11, 0), ("soot", 12, 0),
            ("stall_counter", 5, 3), ("myrtle", 9, 2),
            ("hearth", 12, 2), ("krater", 11, 2),
            ("liknon", 1, 4), ("nest_basket", 0, 3), ("nest_basket", 3, 4), ("nest_basket", 0, 5),
            ("loom", 0, 0),
            ("kline", 0, 6), ("thyrsoi", 13, 5), ("water_jar", 12, 6), ("kalathos", 11, 7),
            ("nebris", 3, 6), ("table", 8, 6), ("stool", 10, 6), ("pots", 8, 5),
            ("mat", 6, 8),
        ],
        "spots": [
            ("warp", "door to Route 7 (south-arrow mat)", [(6, 8), (7, 8)]),
            ("across", "the keeper, behind her counter", (6, 2), (6, 4, "north")),
            ("npc", "the second nymph, by the cradle", (2, 5), "north"),
            ("npc", "the nymph's Pokémon by the hearth", (10, 4), "west"),
            ("bg", "the liknon", (1, 4), (1, 5, "north")),
        ],
    },
}


# ===========================================================================
# Events: map.json and scripts.pory, written from the spots above
# ===========================================================================

import json  # noqa: E402

GFX = "OBJ_EVENT_GFX_ICHOR_"
DEIGMA = "EmporionCity_GreatDeigma"
NURSERY = "Route7_NurseryOfNysa"
CITY_WARP = 11          # data/maps/EmporionCity/map.json: the stoa's east door
ROUTE7_WARP = 0         # kopais.py: Route 7's warp 0, the farmhouse door


def _obj(lid, gfx, x, y, facing, script, flag="0", wander=False):
    return {"local_id": lid, "graphics_id": gfx if gfx.startswith("OBJ_") else GFX + gfx,
            "x": x, "y": y, "elevation": 3,
            "movement_type": "MOVEMENT_TYPE_WANDER_AROUND" if wander else f"MOVEMENT_TYPE_FACE_{facing}",
            "movement_range_x": 1 if wander else 0, "movement_range_y": 1 if wander else 0,
            "trainer_type": "TRAINER_TYPE_NONE", "trainer_sight_or_berry_tree_id": "0",
            "script": script, "flag": flag}


def _write_map(name, spec, objects, bgs, scripts, header, music, dest_map, dest_warp):
    path = ROOT / f"data/maps/{name}/map.json"
    m = json.loads(path.read_text())
    m.update(music=music, map_type="MAP_TYPE_INDOOR", weather="WEATHER_NONE", show_map_name=False,
             allow_cycling=False, connections=None)
    m["object_events"] = objects
    warp = next(s for s in spec["spots"] if s[0] == "warp")
    m["warp_events"] = [{"x": x, "y": y, "elevation": 0, "dest_map": dest_map, "dest_warp_id": str(dest_warp)}
                        for x, y in warp[2]]
    m["coord_events"] = []
    m["bg_events"] = [{"type": "sign", "x": x, "y": y, "elevation": 0,
                       "player_facing_dir": f"BG_EVENT_PLAYER_FACING_{f.upper()}", "script": s}
                      for (x, y), f, s in bgs]
    path.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    text = [header, f"// Generated by tools/ichor/maps/kapeleia_rooms.py; edit the builder, not this file."]
    (ROOT / f"data/maps/{name}/scripts.pory").write_text("\n\n".join(text + scripts) + "\n")


def _speaker(px, key, name):
    return f'text {px}Text_Name{key} {{ "{name}" }}'


def _mart(label, items):
    return f"mart {label} {{\n" + "".join(f"    {i}\n" for i in items) + "}"


# --- the Great Deigma's sellers ------------------------------------------------
# Each seller's stock grows with the Laurels: a second tier after the fourth
# (Act II's first, won far from Emporion: a reason to sail back), a third
# after the seventh. (stall, speaker key, NAME, sprite, lines, tiers)
SELLERS = [
    ("Phoenician", "Hiram", "HIRAM", "SAILOR",
     ("Hiram of Sidon. Purple from Tyre, glass from the furnaces of Sidon,\\n"
      "and the sea's own goods for your Pokémon.",
      "New cargo came in on the last ship. Have a look.",
      "Fair winds. My ship sails when the hold is light."),
     [["ITEM_NET_BALL", "ITEM_DIVE_BALL", "ITEM_MYSTIC_WATER", "ITEM_WAVE_INCENSE"],
      ["ITEM_LUXURY_BALL", "ITEM_DEEP_SEA_SCALE", "ITEM_DEEP_SEA_TOOTH"],
      ["ITEM_PRISM_SCALE", "ITEM_SHELL_BELL"]]),
    ("Egyptian", "Amasis", "AMASIS", "ACOLYTE_M",
     ("Amasis, of Naukratis on the Nile. Frankincense, herbs of the Black Land,\\n"
      "and sand from the desert, which your Ground Pokémon will love.",
      "The Nile flooded well this year. More herbs, finer incense.",
      "Go in health. The gods of my country keep accounts, too."),
     [["ITEM_FRANKINCENSE", "ITEM_HEAL_POWDER", "ITEM_ENERGY_POWDER", "ITEM_ENERGY_ROOT", "ITEM_SOFT_SAND"],
      ["ITEM_REVIVAL_HERB", "ITEM_ODD_INCENSE", "ITEM_ROSE_INCENSE", "ITEM_SMOOTH_ROCK"],
      ["ITEM_LIGHT_CLAY", "ITEM_PURE_INCENSE"]]),
    ("Scythian", "Skyles", "SKYLES", "HARVESTER",
     ("Skyles. My people live on horseback past the Euxine, where the rivers\\n"
      "freeze. Furs, gold, and the things an archer needs.",
      "The caravans came down from the steppe. Better lenses this time.",
      "When you see the grass sea, say Skyles sent you."),
     [["ITEM_SHARP_BEAK", "ITEM_NEVER_MELT_ICE", "ITEM_BLACK_BELT", "ITEM_QUICK_CLAW"],
      ["ITEM_ICY_ROCK", "ITEM_SCOPE_LENS"],
      ["ITEM_WIDE_LENS", "ITEM_POWER_BRACER", "ITEM_POWER_WEIGHT"]]),
    ("Stones", "Petraios", "PETRAIOS", "MERCHANT",
     ("Stones that change a Pokémon. Fire, water, thunder, leaf.\\n"
      "And an Everstone, for one you'd rather keep as it is.",
      "Quarrymen up north found more kinds. Moon, sun and ice.",
      "Mind your toes. They're heavier than they look."),
     [["ITEM_FIRE_STONE", "ITEM_WATER_STONE", "ITEM_THUNDER_STONE", "ITEM_LEAF_STONE", "ITEM_EVERSTONE"],
      ["ITEM_MOON_STONE", "ITEM_SUN_STONE", "ITEM_ICE_STONE"],
      ["ITEM_SHINY_STONE", "ITEM_DUSK_STONE", "ITEM_DAWN_STONE"]]),
    ("Tablets", "Sophron", "SOPHRON", "ELDER_M",
     ("Techniques, written on wax. Teach them to your Pokémon as often as you like.\\n"
      "I wrote them all myself. My hand aches.",
      "I've been writing all season. Weather, and calmer minds.",
      "A technique learned is never lost. Unlike my stylus."),
     [["ITEM_TM_WATER_PULSE", "ITEM_TM_SECRET_POWER", "ITEM_TM_LIGHT_SCREEN", "ITEM_TM_REFLECT",
       "ITEM_TM_SAFEGUARD"],
      ["ITEM_TM_SUNNY_DAY", "ITEM_TM_RAIN_DANCE", "ITEM_TM_SANDSTORM", "ITEM_TM_HAIL", "ITEM_TM_CALM_MIND",
       "ITEM_TM_DOUBLE_TEAM"],
      ["ITEM_TM_THUNDERBOLT", "ITEM_TM_DRAGON_CLAW", "ITEM_TM_FOCUS_PUNCH", "ITEM_TM_SLUDGE_BOMB"]]),
    ("Berries", "Melia", "MELIA", "WOMAN",
     ("Fruit from every orchard on the gulf! Oran, Pecha, Cheri...\\n"
      "Good for Pokémon, and good for the altars.",
      "The southern orchards sent Sitrus and Lum. Get them while they last!",
      "Eat some, offer some. The gods like ripe ones."),
     [["ITEM_ORAN_BERRY", "ITEM_PECHA_BERRY", "ITEM_CHERI_BERRY", "ITEM_CHESTO_BERRY", "ITEM_RAWST_BERRY",
       "ITEM_ASPEAR_BERRY", "ITEM_PERSIM_BERRY"],
      ["ITEM_SITRUS_BERRY", "ITEM_LUM_BERRY"],
      ["ITEM_OCCA_BERRY", "ITEM_PASSHO_BERRY", "ITEM_WACAN_BERRY", "ITEM_RINDO_BERRY", "ITEM_YACHE_BERRY"]]),
]
LAUREL_TIERS = ("FLAG_BADGE04_GET", "FLAG_BADGE07_GET")

# The curio stall: two rare things a day, drawn fresh each morning
# (VAR_ICHOR_DEIGMA_RARE, FLAG_DAILY_ICHOR_DEIGMA_RARE); after the seventh
# Laurel each day's pair has a third.
CURIOS = [
    (["ITEM_LUCKY_EGG", "ITEM_PP_UP"], "ITEM_CHOICE_BAND",
     "An egg of beaten gold, they swear, laid by a goose in Lydia."),
    (["ITEM_AMULET_COIN", "ITEM_BOTTLE_CAP"], "ITEM_CHOICE_SPECS",
     "A coin from Croesus's own treasury. Probably."),
    (["ITEM_LEFTOVERS", "ITEM_DESTINY_KNOT"], "ITEM_CHOICE_SCARF",
     "A red thread from Aphrodite's sanctuary on Kythera. It ties two together."),
    (["ITEM_FOCUS_SASH", "ITEM_RARE_CANDY"], "ITEM_CHOICE_BAND",
     "A sash a wrestler wore at Olympia. He never fell."),
    (["ITEM_LIFE_ORB", "ITEM_PP_MAX"], "ITEM_CHOICE_SPECS",
     "A glass orb from Sidon with a light inside. It hums. Don't ask."),
    (["ITEM_EVIOLITE", "ITEM_ABILITY_CAPSULE"], "ITEM_CHOICE_SCARF",
     "A capsule from the far east. It changes a Pokémon's nature. Well, its gift."),
]

# Shoppers and the market's people: (key, sprite, x, y, facing, wander, line)
DEIGMA_PEOPLE = [
    ("Agoranomos", "HOPLITE", 16, 3, "DOWN", False,
     "I'm the agoranomos. I check the weights against the city's measures.\\p"
     "Short a sixth of an obol on a scale of figs? I'll know."),
    ("Haggler", "WOMAN", 8, 5, "DOWN", True,
     "Two obols for that? At home I'd pay half! ...At home they don't have it."),
    ("Sailor", "SAILOR", 13, 5, "DOWN", True,
     "Four months at sea, and the first thing I buy is figs. Every time."),
    ("Child", "KID_F", 12, 9, "DOWN", True,
     "The Scythian has a gold deer! A real gold deer! Mama says it's not for children."),
    ("Elder", "ELDER_F", 20, 11, "LEFT", True,
     "I come every day to see what the curio-seller has. Kallias never has the same thing twice."),
    ("Student", "YOUTH_F", 8, 11, "UP", True,
     "Sophron's tablets taught my Pokémon a new move. And then another. I'm broke."),
    ("Pilgrim", "PILGRIM", 20, 13, "DOWN", True,
     "I came for the Isthmian Games and stayed for the market. Don't tell my wife."),
    ("Porter", "MAN", 1, 10, "RIGHT", False,
     "Bales up from the harbor all day. The Scythian's furs weigh the most. And smell the most."),
    ("Donkey", "OBJ_EVENT_GFX_SPECIES(ONOTIS)", 2, 10, "LEFT", False, None),
    ("Spicer", "MERCHANT", 6, 13, "DOWN", False,
     "Saffron from Lydia, cumin from Kypros, salt from the pans at Megara.\\p"
     "I sell to cooks, not to Trainers. But smell this. Go on."),
    ("Potter", "MAN", 26, 13, "DOWN", False,
     "Real Athenian ware, black-figure and red. The owl on the bottom says so.\\p"
     "Euphronios up the hill paints better. Don't tell him I said that."),
    ("Mother", "WOMAN", 12, 12, "DOWN", True,
     "Stay where I can see you! ...Has anyone seen a small boy with a fig?"),
    ("Boy", "KID_M", 17, 12, "DOWN", True,
     "Mmf. I'm not lost. I'm eating a fig."),
    ("Taster", "YOUTH_M", 20, 5, "DOWN", True,
     "Melia lets you taste a berry if you smile. I've smiled nine times."),
]


def write_deigma():
    spec = ROOMS["great_deigma"]
    px = DEIGMA + "_EventScript_"
    lid = "LOCALID_EMPORION_GREAT_DEIGMA_"
    objs, bgs, scripts = [], [], []
    for stall, key, name, gfx, (hello, restock, bye), tiers in SELLERS:
        _, _, (sx, sy) = DEIGMA_STALLS[stall]
        objs.append(_obj(lid + key.upper(), gfx, sx + 1, sy + 2, "DOWN", px + key))
        scripts.append(_speaker(px, key, name))
        marts = [f"{DEIGMA}_Mart_{key}{n}" for n in (1, 2, 3)]
        for i, label in enumerate(marts):
            scripts.append(_mart(label, sum(tiers[:i + 1], [])))
        scripts.append(f'''script {px}{key} {{
    lock
    faceplayer
    setspeaker({px}Text_Name{key})
    if (flag({LAUREL_TIERS[0]})) {{
        msgbox(format("{restock}"))
    }} else {{
        msgbox(format("{hello}"))
    }}
    message(format("Take your time."))
    waitmessage
    if (flag({LAUREL_TIERS[1]})) {{
        pokemart({marts[2]})
    }} elif (flag({LAUREL_TIERS[0]})) {{
        pokemart({marts[1]})
    }} else {{
        pokemart({marts[0]})
    }}
    setspeaker({px}Text_Name{key})
    msgbox(format("{bye}"))
    release
}}''')
    # the curio stall
    _, _, (cx, cy) = DEIGMA_STALLS["Curios"]
    objs.append(_obj(lid + "KALLIAS", "MERCHANT_THYRSA", cx + 1, cy + 2, "DOWN", px + "Kallias"))
    scripts.append(_speaker(px, "Kallias", "KALLIAS"))
    cases_lines, cases_mart = [], []
    for i, (items, late, line) in enumerate(CURIOS):
        scripts.append(_mart(f"{DEIGMA}_Mart_Curios{i}", items))
        scripts.append(_mart(f"{DEIGMA}_Mart_CuriosLate{i}", items + [late]))
        cases_lines.append(f'''        case {i}:
            msgbox(format("{line}"))''')
        cases_mart.append(f'''        case {i}:
            if (flag({LAUREL_TIERS[1]})) {{
                pokemart({DEIGMA}_Mart_CuriosLate{i})
            }} else {{
                pokemart({DEIGMA}_Mart_Curios{i})
            }}''')
    nl = "\n"
    scripts.append(f'''script {px}Kallias {{
    lock
    faceplayer
    setspeaker({px}Text_NameKallias)
    msgbox(format("Kallias, curios and rarities. Never the same two days running.\\p"
                  "Today, look at this!"))
    setspeaker({px}Text_NameKallias)
    switch (var(VAR_ICHOR_DEIGMA_RARE)) {{
{nl.join(cases_lines)}
    }}
    message(format("Buy it today. Tomorrow it's gone."))
    waitmessage
    switch (var(VAR_ICHOR_DEIGMA_RARE)) {{
{nl.join(cases_mart)}
    }}
    setspeaker({px}Text_NameKallias)
    msgbox(format("Come back tomorrow. I'll have something else. I always do."))
    release
}}''')
    # the money-changer: the Deigma's trapeza pays more than the Agora, and
    # more again as your name grows (VAR_0x8005: percent over the market)
    objs.append(_obj(lid + "PHORMION", "ELDER_M", 23, 8, "DOWN", px + "Phormion"))
    scripts.append(_speaker(px, "Phormion", "PHORMION"))
    scripts.append(f'''script {px}Phormion {{
    lock
    faceplayer
    setspeaker({px}Text_NamePhormion)
    msgbox(format("Phormion, at the trapeza. I learned the trade from old Pasion out in the Agora.\\p"
                  "He gives a fifth over the market for old coins. I give more, and more\\n"
                  "again for a Trainer the temples know."))
    goto({px}PhormionWeigh)
}}''')
    scripts.append(f'''script {px}PhormionWeigh {{
    setspeaker({px}Text_NamePhormion)
    message(format("Which coin shall I weigh?"))
    waitmessage
    multichoice(0, 0, MULTI_ICHOR_COINS, FALSE)
    if (var(VAR_RESULT) == 0) {{
        setvar(VAR_0x8004, ITEM_RELIC_COPPER)
    }} elif (var(VAR_RESULT) == 1) {{
        setvar(VAR_0x8004, ITEM_RELIC_SILVER)
    }} elif (var(VAR_RESULT) == 2) {{
        setvar(VAR_0x8004, ITEM_RELIC_GOLD)
    }} else {{
        setspeaker({px}Text_NamePhormion)
        msgbox(format("Another day, then. The trapeza is always here."))
        release
        end
    }}
    checkitem(VAR_0x8004)
    if (var(VAR_RESULT) == FALSE) {{
        setspeaker({px}Text_NamePhormion)
        msgbox(format("You don't have one of those. Find an old coin and come back."))
        goto({px}PhormionWeigh)
    }}
    if (flag({LAUREL_TIERS[1]})) {{
        setvar(VAR_0x8005, 60)
    }} elif (flag({LAUREL_TIERS[0]})) {{
        setvar(VAR_0x8005, 40)
    }} else {{
        setvar(VAR_0x8005, 25)
    }}
    specialvar(VAR_RESULT, Ichor_QuoteToMoneychanger)
    if (var(VAR_RESULT) == FALSE) {{
        setspeaker({px}Text_NamePhormion)
        msgbox(format("Your purse can't hold the price. Spend some first."))
        release
        end
    }}
    bufferitemname(STR_VAR_2, VAR_0x8004)
    msgbox("Sell the {{STR_VAR_2}}\\nfor ¥{{STR_VAR_1}}?", MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        specialvar(VAR_RESULT, Ichor_SellToMoneychanger)
        if (var(VAR_RESULT) == TRUE) {{
            playse(SE_SHOP)
            msgbox(format("Phormion rings it on the stone.\\nHe pays you ¥{{STR_VAR_1}}."))
        }}
    }}
    goto({px}PhormionWeigh)
}}''')
    for key, gfx, x, y, facing, wander, line in DEIGMA_PEOPLE:
        objs.append(_obj(lid + key.upper(), gfx, x, y, facing, px + key, wander=wander))
        if line is None:
            scripts.append(f'''script {px}{key} {{
    lock
    faceplayer
    msgbox(format("The donkey is loaded with a bale of wool. It flicks an ear at you."))
    release
}}''')
        else:
            scripts.append(f'''script {px}{key} {{
    lock
    faceplayer
    msgbox(format("{line}"))
    release
}}''')
    notices = {
        "the market's notice board (west)": ("NoticeWest", "THE GREAT DEIGMA. Every trader from every sea, under one roof.\\p"
                                             "Weights checked by the agoranomoi. Old coins at Phormion's trapeza."),
        "the market's notice board (east)": ("NoticeEast", "Notice: Kallias's curio stall changes its wares each day.\\p"
                                             "Ships in from Sidon, Naukratis and the Euxine. More goods after the season."),
        "the official measures": ("Measures", "The city's measures in bronze: a balance, a set of weights,\\n"
                                  "a measure of grain. Stamped with Hermes of the Agora."),
        "the fountain": ("Fountain", "A lion's head spills cold water into the basin.\\p"
                         "Someone has dropped an obol in it for luck."),
    }
    for s in spec["spots"]:
        if s[0] != "bg":
            continue
        key, text = notices[s[1]]
        bgs.append((s[2], s[3][2], px + key))
        scripts.append(f'''script {px}{key} {{
    msgbox(format("{text}"), MSGBOX_SIGN)
    end
}}''')
    # the daily draw: a new stock every morning, never the same as yesterday's
    n = len(CURIOS)
    draw = []
    for old in range(n):
        draw.append(f'''            case {old}:
                random({n - 1})
                if (var(VAR_RESULT) >= {old}) {{
                    addvar(VAR_RESULT, 1)
                }}''')
    header = f'''mapscripts {DEIGMA}_MapScripts {{
    MAP_SCRIPT_ON_TRANSITION {{
        if (!flag(FLAG_DAILY_ICHOR_DEIGMA_RARE)) {{
            setflag(FLAG_DAILY_ICHOR_DEIGMA_RARE)
            switch (var(VAR_ICHOR_DEIGMA_RARE)) {{
{nl.join(draw)}
                default:
                    random({n})
            }}
            copyvar(VAR_ICHOR_DEIGMA_RARE, VAR_RESULT)
        }}
    }}
}}'''
    _write_map(DEIGMA, spec, objs, bgs, scripts, header, "MUS_ICHOR_EMPORION", "MAP_EMPORION_CITY", CITY_WARP)


# --- the Nursery of Nysa ---------------------------------------------------------
# Makris (the nymph who fed the infant Dionysus honey) takes the deposits: the
# day-care woman's script (data/scripts/day_care.inc's
# Route117_PokemonDayCare_EventScript_DaycareWoman) in Ichor's words.

def write_nursery():
    spec = ROOMS["nursery"]
    px = NURSERY + "_EventScript_"
    lid = "LOCALID_NURSERY_OF_NYSA_"
    objs = [
        _obj(lid + "MAKRIS", "PRIESTESS", 6, 2, "DOWN", px + "Makris"),
        _obj(lid + "BROMIE", "YOUTH_F", 2, 5, "UP", px + "Bromie"),
        _obj(lid + "KID", "OBJ_EVENT_GFX_SPECIES(MELIBEE)", 10, 4, "LEFT", px + "Melibee"),
    ]
    bgs = [((1, 4), "north", px + "Liknon")]
    S = "setspeaker({px}Text_NameMakris)".format(px=px)
    scripts = [_speaker(px, "Makris", "MAKRIS"), f'''script {px}Makris {{
    lock
    faceplayer
    specialvar(VAR_RESULT, GetDaycareState)
    if (var(VAR_RESULT) == DAYCARE_EGG_WAITING) {{
        {S}
        msgbox(format("Aristaios has been looking for you. Something was laid in the glade.\\n"
                      "Go and see him by the wall."))
        release
        end
    }}
    if (var(VAR_RESULT) == DAYCARE_ONE_MON) {{
        {S}
        msgbox(format("Welcome back. Your Pokémon is well. Aristaios walks it in the glade."))
        setvar(VAR_0x8004, 0)
        call({px}LevelsGained)
        {S}
        msgbox(format("I could raise one more beside it. Shall I?"), MSGBOX_YESNO)
        if (var(VAR_RESULT) == YES) {{
            goto({px}GiveMon)
        }}
        goto({px}AskTakeBack)
    }}
    if (var(VAR_RESULT) == DAYCARE_TWO_MONS) {{
        {S}
        msgbox(format("Welcome back. Both of yours are well."))
        setvar(VAR_0x8004, 0)
        call({px}LevelsGained)
        setvar(VAR_0x8004, 1)
        call({px}LevelsGained)
        goto({px}AskTakeBack)
    }}
    {S}
    msgbox(format("This is the Nursery of Nysa. We nymphs raised a god here once,\\n"
                  "in a winnowing basket, on milk and honey.\\p"
                  "Now we raise travelers' Pokémon. Leave one or two with me and they'll grow\\n"
                  "while you're on the road. It costs a little to take them back.\\p"
                  "Shall I raise one for you?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        goto({px}GiveMon)
    }}
    {S}
    msgbox(format("Come back whenever you like. The door is always open."))
    release
}}''', f'''script {px}GiveMon {{
    specialvar(VAR_RESULT, CountPartyNonEggMons)
    if (var(VAR_RESULT) == 1) {{
        {S}
        msgbox(format("You have only one Pokémon with you. Who would walk the road with you?"))
        release
        end
    }}
    specialvar(VAR_RESULT, CountPartyAliveNonEggMons)
    if (var(VAR_RESULT) == 2) {{
        {S}
        msgbox(format("If I take one, you'll have only one left to fight with. Heal them first."))
        release
        end
    }}
    {S}
    msgbox(format("Which one shall I raise?"))
    chooseboxmon(SELECT_PC_MON_DAYCARE)
    waitstate
    if (var(VAR_0x8004) == PARTY_NOTHING_CHOSEN) {{
        goto({px}ComeAgain)
    }}
    specialvar(VAR_RESULT, CountPartyAliveNonEggMons_IgnoreVar0x8004Slot)
    if (var(VAR_RESULT) == 0) {{
        {S}
        msgbox(format("Then you'd have nothing to battle with. Choose another."))
        release
        end
    }}
    specialvar(VAR_0x8005, GetSelectedMonNicknameAndSpecies)
    waitse
    playmoncry(VAR_0x8005, CRY_MODE_NORMAL)
    {S}
    msgbox(format("I'll raise your {{STR_VAR_1}} as if it were my own."))
    waitmoncry
    special(StoreSelectedPokemonInDaycare)
    callnative(UpdateFollowingPokemon)
    incrementgamestat(GAME_STAT_USED_DAYCARE)
    specialvar(VAR_RESULT, GetDaycareState)
    if (var(VAR_RESULT) == DAYCARE_ONE_MON) {{
        {S}
        msgbox(format("I could raise one more beside it. Shall I?"), MSGBOX_YESNO)
        if (var(VAR_RESULT) == YES) {{
            goto({px}GiveMon)
        }}
        goto({px}ComeAgain)
    }}
    {S}
    msgbox(format("Two together. If they get along, Aristaios may find an Egg in the glade."))
    release
}}''', f'''script {px}ComeAgain {{
    {S}
    msgbox(format("Come back whenever you like. The door is always open."))
    release
}}''', f'''script {px}LevelsGained {{
    specialvar(VAR_RESULT, GetNumLevelsGainedFromDaycare)
    if (var(VAR_RESULT) != 0) {{
        {S}
        msgbox(format("Your {{STR_VAR_1}} has grown by {{STR_VAR_2}} level(s)."))
    }}
    return
}}''', f'''script {px}AskTakeBack {{
    {S}
    msgbox(format("Would you like one back?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == NO) {{
        goto({px}ComeAgain)
    }}
    goto({px}TryTakeBack)
}}''', f'''script {px}TryTakeBack {{
    specialvar(VAR_RESULT, CalculatePlayerPartyCount)
    if (var(VAR_RESULT) == PARTY_SIZE) {{
        {S}
        msgbox(format("Your party is full. Make room, then come back for it."))
        release
        end
    }}
    specialvar(VAR_RESULT, GetDaycareState)
    setvar(VAR_0x8004, 0)
    if (var(VAR_RESULT) != DAYCARE_ONE_MON) {{
        special(ShowDaycareLevelMenu)
        copyvar(VAR_0x8004, VAR_RESULT)
        if (var(VAR_RESULT) == DAYCARE_EXITED_LEVEL_MENU) {{
            goto({px}ComeAgain)
        }}
    }}
    special(GetDaycareCostAndPrepareString)
    {S}
    msgbox(format("Raising it cost ¥{{STR_VAR_2}}. Will you pay?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == NO) {{
        goto({px}ComeAgain)
    }}
    specialvar(VAR_RESULT, IsEnoughForCostInVar0x8005)
    if (var(VAR_RESULT) == FALSE) {{
        {S}
        msgbox(format("You haven't enough money. The honey isn't free, I'm afraid."))
        release
        end
    }}
    applymovement({lid}MAKRIS, {px}Movement_Fetch)
    waitmovement(0)
    specialvar(VAR_RESULT, TakePokemonFromDaycare)
    special(SubtractMoneyFromVar0x8005)
    playse(SE_SHOP)
    {S}
    msgbox(format("Here's your {{STR_VAR_1}}. It missed you."))
    waitse
    playmoncry(VAR_RESULT, CRY_MODE_NORMAL)
    msgbox(format("{{PLAYER}} took back {{STR_VAR_1}}."))
    waitmoncry
    callnative(UpdateFollowingPokemon)
    specialvar(VAR_RESULT, GetDaycareState)
    if (var(VAR_RESULT) == DAYCARE_ONE_MON) {{
        {S}
        msgbox(format("Will you take the other one too?"), MSGBOX_YESNO)
        if (var(VAR_RESULT) == YES) {{
            goto({px}TryTakeBack)
        }}
    }}
    goto({px}ComeAgain)
}}''', f'''movement {px}Movement_Fetch {{
    delay_16 * 2
    face_left
    delay_16 * 2
    face_right
    delay_16 * 2
    face_down
}}''', _speaker(px, "Bromie", "BROMIE"), f'''script {px}Bromie {{
    lock
    faceplayer
    setspeaker({px}Text_NameBromie)
    msgbox(format("We keep the Eggs here until Aristaios finds their Trainers.\\p"
                  "An Egg wants walking. Carry one in your party and keep moving,\\n"
                  "and it'll hatch on the road."))
    release
}}''', f'''script {px}Melibee {{
    lock
    faceplayer
    msgbox(format("A Melibee hums by the honey jars. Makris says it was the first\\n"
                  "Pokémon they ever raised here."))
    release
}}''', f'''script {px}Liknon {{
    msgbox(format("A liknon, a winnowing basket. The nymphs laid the infant god in one.\\p"
                  "Today it holds an Egg, wrapped in fleece."), MSGBOX_SIGN)
    end
}}''']
    header = f"mapscripts {NURSERY}_MapScripts {{}}"
    _write_map(NURSERY, spec, objs, bgs, scripts, header, "MUS_ICHOR_ELEUSA", "MAP_ROUTE7_KRONIA_GROUNDS",
               ROUTE7_WARP)


def check_across(name, layouts):
    """Each "across" spot: the cell between the player and the person is a
    counter, and the player's cell is open."""
    cells = layouts[name]
    for s in ROOMS[name]["spots"]:
        if s[0] != "across":
            continue
        (px_, py_), (fx, fy, _) = s[2], s[3]
        mid = cells[(py_ + fy) // 2][px_]
        assert mid.behavior == "MB_COUNTER", f"{name}: {s[1]}: no counter at ({px_},{(py_ + fy) // 2})"
        assert cells[fy][fx].block != 0x0C00, f"{name}: {s[1]} is read from a blocked cell"


def render_people(name, png, out):
    """The room's 2x render with its people and Pokémon drawn in (for review)."""
    from PIL import Image
    sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
    import route5 as R5
    im = Image.open(png).convert("RGBA")
    s = im.width // len(ROOMS[name]["grid"][0]) // 16
    flat = im.resize((im.width // s, im.height // s), Image.NEAREST)
    m = json.loads((ROOT / f"data/maps/{ROOMS[name]['layout']}/map.json").read_text())
    for o in sorted(m["object_events"], key=lambda o: o["y"]):
        facing = o["movement_type"].rsplit("_", 1)[-1] if "FACE" in o["movement_type"] else "DOWN"
        try:
            spr, fw, fh = R5.sprite(o["graphics_id"], facing)
        except Exception:
            continue
        flat.alpha_composite(spr, (o["x"] * 16 + 8 - fw // 2, max(0, o["y"] * 16 + 16 - fh)))
    flat.resize(im.size, Image.NEAREST).convert("RGB").save(out)


def build(args=None):
    sys.path.insert(0, str(ROOT / "tools/ichor/art"))
    import ergasteria_build as EB
    import kapeleia_build as KB
    args = args or EB.parse_args()
    _, deigma = EB.build(KB.KAPELEIA, args)
    _, nursery = EB.build(KB.NYSA, args)
    check_across("great_deigma", deigma)
    check_across("nursery", nursery)
    write_deigma()
    write_nursery()


if __name__ == "__main__":
    build()
