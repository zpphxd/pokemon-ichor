#!/usr/bin/env python3
"""Build the connected Eleusa--Kithairon--Thyrsa chapter using existing Greek art.

Route 6 and Mt. Kithairon's layouts, events, scripts and wild tables now come
from tools/ichor/maps/kithairon.py; this script still writes their trainers'
parties (trainers()) and builds Route 7.
"""
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OPEN_WATER = {0x170}  # aethos's sea


def read(path):
    return json.loads((ROOT / path).read_text())


def write(path, value):
    (ROOT / path).write_text(json.dumps(value, indent=2) + "\n")


def const(name):
    import re
    return re.sub(r"(?<=[a-z])(?=[A-Z])", "_", name).upper()


def obj(name, x, y, script, gfx="PILGRIM", facing="DOWN", sight=0, flag="0"):
    return dict(local_id=name, graphics_id="OBJ_EVENT_GFX_ICHOR_" + gfx,
                x=x, y=y, elevation=3, movement_type="MOVEMENT_TYPE_FACE_" + facing,
                movement_range_x=0, movement_range_y=0,
                trainer_type="TRAINER_TYPE_NORMAL" if sight else "TRAINER_TYPE_NONE",
                trainer_sight_or_berry_tree_id=str(sight), script=script, flag=flag)


def bg(x, y, script):
    return dict(type="sign", x=x, y=y, elevation=0,
                player_facing_dir="BG_EVENT_PLAYER_FACING_ANY", script=script)


def warp(x, y, dest, index):
    return dict(x=x, y=y, elevation=0, dest_map="MAP_" + const(dest), dest_warp_id=str(index))


class Map:
    def __init__(self, name, w, h, indoor=False, secondary=None):
        self.name, self.w, self.h = name, w, h
        self.secondary = secondary
        self.json = read(f"data/maps/{name}/map.json")
        self.json.update(object_events=[], bg_events=[], warp_events=[], coord_events=[], connections=None)
        self.cells = [0x3400 | (0x205 if indoor else 0x001)] * (w * h)
        if not indoor:
            for y in range(h):
                for x in range(w):
                    self.cells[y * w + x] = 0x3400 | (
                        ((0x01E, 0x01F), (0x026, 0x027))[y % 2][x % 2])
        self.indoor = indoor
        self.prefix = name + "_EventScript_"

    def put(self, x, y, tile, solid=False):
        assert 0 <= x < self.w and 0 <= y < self.h, (self.name, x, y)
        if tile in OPEN_WATER:
            # Open water sits at elevation 1 with no collision, below the land's 3: the
            # elevation step keeps walkers out, and the rod and Surf work from the shore
            # (tools/ichor/fishing_audit.py). Solid water at 3 can't be fished.
            self.cells[y * self.w + x] = 0x1000 | tile
            return
        self.cells[y * self.w + x] = 0x3000 | (0x400 if solid else 0) | tile

    def rect(self, x0, y0, x1, y1, tile, solid=False):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, tile, solid)

    def stamp(self, x, y, rows):
        for dy, row in enumerate(rows):
            for dx, tile in enumerate(row):
                self.put(x + dx, y + dy, tile, True)

    def person(self, name, x, y, script=None, **kwargs):
        event = obj("LOCALID_" + const(self.name) + "_" + name.upper(), x, y,
                    script or self.prefix + name, **kwargs)
        self.json["object_events"].append(event)

    def sign(self, name, x, y, tile=0x003):
        self.put(x, y, tile, True)
        self.json["bg_events"].append(bg(x, y, self.prefix + name))

    def connection(self, direction, dest, offset=0):
        if self.json["connections"] is None:
            self.json["connections"] = []
        self.json["connections"].append(dict(direction=direction, map="MAP_" + const(dest), offset=offset))

    def save(self):
        path = ROOT / f"data/layouts/{self.name}"
        (path / "map.bin").write_bytes(struct.pack("<" + "H" * len(self.cells), *self.cells))
        border = 0x3400 | (0x200 if self.secondary == "gTileset_ThyrsaRooms" else
                           0x205 if self.indoor else 0x0E0)
        (path / "border.bin").write_bytes(struct.pack("<4H", *([border] * 4)))
        layouts = read("data/layouts/layouts.json")
        layout = next(l for l in layouts["layouts"] if l.get("id") == self.json["layout"])
        layout.update(width=self.w, height=self.h, primary_tileset="gTileset_Aethos",
                      secondary_tileset=self.secondary or ("gTileset_Civic" if self.indoor else "gTileset_Kalliste"))
        write("data/layouts/layouts.json", layouts)
        write(f"data/maps/{self.name}/map.json", self.json)


ROADS = [
    ("Route6_EleutheraiRoad", "Eleutherai", 21, [
        ("DAMON", "HOPLITE", "The road goes up. Your guard must too.", "Good. Keep your footing."),
        ("PHANO", "HARVESTER", "The vines have ears. Mine have partners.", "All right. You can pass the grapes."),
        ("LYSIS", "PILGRIM", "Do you trust the next step?", "That one, apparently."),
        ("MELANIPPE", "ACOLYTE_F", "The mountain is the god's other theater.", "A very steep stage."),
        ("SOSTRATOS", "SHEPHERD", "My flock won't climb without an audience.", "They liked that."),
        ("THEOGNIS", "AUGUR", "My reading promised a quiet walk.", "It left that part out."),
    ]),
    ("MtKithairon", "Kithairon", 23, [
        ("AKTAIOS", "HOPLITE", "At the pass, even a whisper carries.", "So does a defeat."),
        ("NYSA", "ACOLYTE_F", "Don't pick the ivy. It picks back.", "You've met it before."),
        ("BROMIOS", "ACOLYTE_M", "The mountain answers a shout.", "It answered yours."),
        ("CHARINOS", "PILGRIM", "The god came here dressed as a stranger.", "I'd have offered him a seat."),
        ("KLEITO", "HARVESTER", "Up here the wine needs no water.", "I need some, though."),
        ("EUPHRON", "SHEPHERD", "Thyrsa's just beyond the next ridge.", "A ridge and a battle."),
    ]),
    ("Route7_KroniaGrounds", "Kronia", 25, [
        ("HAGES", "TITAN_GRUNT", "No toll. Battle for fun?", "Still no toll."),
        ("MYRTON", "HARVESTER", "They fed me. Nobody asked my name.", "Funny thing to be grateful for."),
        ("DORIS", "PILGRIM", "A better reading. Free bread. What's the catch?", "I keep asking."),
        ("PHILISKOS", "ACOLYTE_M", "Even masters serve at the Kronia.", "Your turn to sit."),
        ("EUXENOS", "HOPLITE", "They said I'd come home from the war.", "That's all I wanted."),
        ("MANTO", "AUGUR", "A true reading doesn't need a sales pitch.", "Remember that."),
    ]),
]


def road(name, label, base, trainers):
    m = Map(name, 24, 40)
    if name == "MtKithairon":
        m.rect(0, 0, 23, 39, 0x0E1, True)
    m.rect(10, 0, 13, 39, 0x1D9)
    for y0, y1 in ((4, 9), (18, 21), (30, 35)):
        m.rect(4, y0, 19, y1, 0x001)
        m.rect(4, y0, 7, y1, 0x00D)
        m.rect(16, y0, 19, y1, 0x00D)
    for y in (10, 24):
        m.rect(10, y, 13, y + 3, 0x00D)
    # A southward hop is a return shortcut, not a bypass around either grass band.
    m.rect(8, 16, 9, 23, 0x001)
    m.put(9, 22, 0x087)
    m.put(9, 23, 0x001)
    m.put(10, 23, 0x001)
    if name == "MtKithairon":
        m.rect(10, 14, 17, 15, 0x1D9)
        m.rect(14, 14, 17, 19, 0x1D9)
        m.rect(10, 16, 13, 17, 0x0E1, True)
    for y in range(2, 39, 4):
        for x in (1, 22):
            m.put(x, y, 0x00E, True)
            m.put(x, y + 1, 0x016, True)
    positions = [(10, 8, "RIGHT", 3), (6, 6, "DOWN", 1), (18, 19, "UP", 1),
                 (10, 22, "RIGHT", 3), (5, 32, "UP", 1), (18, 33, "LEFT", 1)]
    for (trainer, gfx, _, _), (x, y, facing, sight) in zip(trainers, positions):
        m.person(trainer, x, y, gfx=gfx, facing=facing, sight=sight)
    tag = "KITHAIRON" if name == "MtKithairon" else ("R6" if name.startswith("Route6") else "R7")
    for i, (x, y, item, suffix) in enumerate(((4, 4, "SUPER_POTION", "HEAL"),
                                              (19, 18, "GREAT_BALL", "BALL"),
                                              (4, 34, "ETHER", "ETHER"))):
        flag = "FLAG_ICHOR_ITEM_" + (tag if tag == "KITHAIRON" and i == 0 else tag + "_" + suffix)
        e = obj("", x, y, "Common_EventScript_FindItem", flag=flag)
        e.pop("local_id")
        e["graphics_id"] = "OBJ_EVENT_GFX_ITEM_BALL"
        e["trainer_sight_or_berry_tree_id"] = "ITEM_" + item
        m.json["object_events"].append(e)
    m.sign("SouthSign", 14, 37)
    m.sign("NorthSign", 14, 2)
    for x, y, suffix, item in ((7, 4, "HONEY", "HONEY"), (19, 21, "REVIVE", "REVIVE"),
                               (7, 34, "REPEL", "SUPER_REPEL")):
        m.json["bg_events"].append(dict(type="hidden_item", x=x, y=y, elevation=3,
            item="ITEM_" + item, flag=f"FLAG_ICHOR_HIDDEN_ITEM_{tag}_{suffix}",
            quantity=1, underfoot=False))
    scripts = [f"mapscripts {name}_MapScripts {{}}"]
    for trainer, _, intro, defeat in trainers:
        scripts.append(f'''script {m.prefix}{trainer} {{
    trainerbattle_single(TRAINER_ICHOR_{trainer}, format("{intro}"), format("{defeat}"))
    msgbox(format("{defeat}"), MSGBOX_AUTOCLOSE)
    end
}}''')
    south, north = {"Eleutherai": ("Eleusa", "Mt. Kithairon"),
                    "Kithairon": ("Eleutherai road", "Kronia grounds"),
                    "Kronia": ("Mt. Kithairon", "Thyrsa")}[label]
    for key in ("SouthSign", "NorthSign"):
        scripts.append(f'''script {m.prefix}{key} {{
    msgbox(format("South: {south}.\\nNorth: {north}."), MSGBOX_SIGN)
    end
}}''')
    if name == "Route7_KroniaGrounds":
        m.rect(14, 5, 20, 8, 0x1D9)
        for x in range(15, 20):
            m.put(x, 6, 0x149, True)
        m.person("Baker", 18, 8, gfx="WOMAN")
        m.person("Kronist", 17, 5, gfx="PILGRIM")
        scripts.append(f'''script {m.prefix}Baker {{
    lock
    faceplayer
    msgbox(format("Sit. Masters carry the bread today. Hungry people eat it."))
    special(HealPlayerParty)
    if (!flag(FLAG_ICHOR_KRONIA_BREAD)) {{
        giveitem(ITEM_BARLEY_CAKE, 2)
        if (var(VAR_RESULT) == TRUE) {{
            setflag(FLAG_ICHOR_KRONIA_BREAD)
        }}
    }}
    msgbox(format("No oath. No payment. Take your time."))
    release
}}
script {m.prefix}Kronist {{
    lock
    faceplayer
    msgbox(format("The old readers sell you an ending. We offer a beginning.\\p"
                  "May your thread never be cut."))
    release
}}''')
    if name == "MtKithairon":
        m.person("Spring", 13, 18, gfx="ELDER_F")
        scripts.append(f'''script {m.prefix}Spring {{
    lock
    faceplayer
    msgbox(format("Water first. The god can wait."))
    special(HealPlayerParty)
    release
}}''')
    (ROOT / f"data/maps/{name}/scripts.pory").write_text("\n\n".join(scripts) + "\n")
    return m


def asclepeion(m, hx, pithos_x):
    """The standard Asclepeion pieces from civic_rooms.py, the same in every
    town: the healer's station with her at (hx, 2), and the Pithos against
    the back wall at columns pithos_x, pithos_x + 1 (bg events on its foot).
    Adds the healer; the caller names her."""
    import sys
    sys.path.insert(0, str(ROOT / "tools/ichor/art"))
    import civic_tiles as ct
    import civic_rooms as CR
    ct.define()
    for x, y, n in CR.station_cells(hx, 2) + CR.pithos_cells(pithos_x):
        m.cells[y * m.w + x] = CR.block_of(n)
    for x in (pithos_x, pithos_x + 1):
        m.json["bg_events"].append(bg(x, 2, m.prefix + "Pithos"))


def hall(name, w, h):
    m = Map(name, w, h, True)
    m.rect(1, 2, w - 2, h - 1, 0x201)
    m.rect(0, 0, w - 1, 0, 0x205, True)
    m.rect(0, 1, w - 1, 1, 0x208, True)
    m.put(w // 2, h - 1, 0x242)
    return m


KITHAIRON_MAPS = ("Route6_EleutheraiRoad", "MtKithairon")   # built by kithairon.py
# Route 7 is built by kopais.py (layout, events, scripts, wild tables); trainers() still
# writes its parties. Both lists are skipped below.
BUILT_ELSEWHERE = KITHAIRON_MAPS + ("Route7_KroniaGrounds",)

# The Temple of Dionysus: Thespis's Three-Act Play (SYSTEMS §12, redesigned).
# Backstage (the green room) is at the south door. Three painted scenery walls
# stand between it and the roof, one per act, each with a left, middle and right
# door. The right door with the right mask walks you onto the next stage; the
# wrong door drops you through the trapdoor back to the green room. Each stage is
# dressed as its act's scene: the harbor (Act I), the vintner's courtyard (Act II)
# and the god's hillside (Act III). The stage art is tools/ichor/art/thyrsa_stage.py.
VOID, WTOP, WBOT = 0x200, 0x25E, 0x204
FLOOR, FLOOR_SHADOW, FLOOR_EDGE = 0x26D, 0x267, 0x26C
STONES = (0x21A, 0x21A, 0x21A, 0x214, 0x21A, 0x21B, 0x21A, 0x21A)
DOOR = 0x238
DOOR_X = (6, 12, 18)
# (wall top row, act index) for each scenery wall, south to north.
FACADES = ((31, 0), (23, 1), (15, 2))


def stage_ids():
    path = ROOT / "tools/ichor/art/thyrsa_stage_ids.json"
    return {k: int(v, 16) for k, v in json.loads(path.read_text()).items()}


def scatter(x, y, seed=0):
    """A fixed, irregular pick for ground variants (no visible grid)."""
    return (x * 7 + y * 13 + seed * 5 + (x * y) % 3) % 8


def temple():
    A = stage_ids()
    panels = ((7, A["PANEL_VINES"], "PanelLeft"), (13, A["PANEL_HOUSE"], "PanelMiddle"),
              (19, A["PANEL_SHIP"], "PanelRight"))
    m = Map("ThyrsaCity_TempleOfDionysus", 25, 41, True, "gTileset_ThyrsaRooms")
    m.rect(0, 0, 24, 40, VOID, True)

    def room(x0, y0, x1, y1):
        """Boards with a shadow under the wall above and a shaded left edge."""
        m.rect(x0, y0, x1, y1, FLOOR)
        m.rect(x0, y0, x1, y0, FLOOR_SHADOW)
        m.rect(x0, y0 + 1, x0, y1, FLOOR_EDGE)

    def wall(x0, x1, y):
        m.rect(x0, y, x1, y, WTOP, True)
        m.rect(x0, y + 1, x1, y + 1, WBOT, True)

    # --- The roof of the stage building: Dionysus's statue, and Thespis ---------------
    wall(7, 17, 1)
    for x, mask in zip(range(8, 17, 2), (0x233, 0x234, 0x236, 0x235, 0x27E)):
        m.put(x, 1, mask, True)
    room(7, 3, 17, 6)
    m.put(7, 3, 0x28F, True)
    m.put(17, 3, 0x28F, True)
    m.put(15, 3, A["STATUE_TOP_SHADOW"], True)
    m.sign("Altar", 15, 4, A["STATUE_BASE_WOOD"])
    m.put(16, 4, 0x265, True)
    m.put(14, 4, 0x264, True)
    m.person("Thespis", 12, 4, gfx="ACOLYTE_M")
    m.sign("MechaneDown", 9, 5, A["CRANE_HOOK_WOOD"])
    m.put(12, 6, 0x291)
    m.put(13, 6, 0x292)

    # --- Act III: the god's hillside, with the crane at the back -------------------
    wall(1, 23, 7)
    for x in range(1, 24):
        if x not in (10, 11, 12, 13):
            m.put(x, 7, A["BACKDROP_HILL_TREE"] if x in (4, 17, 21) else A["BACKDROP_HILL"], True)
    m.put(11, 7, A["CRANE_BEAM"], True)
    m.put(12, 7, A["CRANE_PULLEY"], True)
    m.sign("MechaneUp", 12, 8, A["CRANE_HOOK"])
    room(1, 9, 23, 14)
    m.rect(2, 10, 22, 14, A["GRASS"])
    for x, y in ((3, 13), (4, 14), (16, 12), (17, 12), (20, 13), (8, 14), (6, 10)):
        m.put(x, y, A["GRASS_FLOWERS"])
    # The corridor to the crane, lined with the satyr play's props.
    for y, left, right in ((9, 0x28F, 0x28F), (10, A["KRATER_GRASS"], A["GOAT_POLE_GRASS"]),
                           (11, None, A["AMPHORA_GRASS"]), (12, A["GOAT_POLE_GRASS"], A["TORCH_GRASS"])):
        if left:
            m.put(11, y, left, True)
        m.put(13, y, right, True)
    m.person("SatyrActor", 11, 11, gfx="ACOLYTE_M", facing="RIGHT", sight=1)
    for x, y in ((4, 11), (7, 12), (16, 10), (21, 11)):
        m.put(x, y, A["GOAT_POLE_GRASS"], True)
    m.put(5, 11, A["KRATER_GRASS"], True)
    m.put(20, 11, A["AMPHORA_GRASS"], True)
    m.put(9, 13, A["KRATER_GRASS"], True)
    m.put(19, 12, A["GOAT_POLE_GRASS"], True)
    m.put(2, 13, A["TORCH_GRASS"], True)
    m.put(22, 13, A["TORCH_GRASS"], True)

    # --- Act II: the vintner's courtyard, his house behind it ------------------------
    room(1, 17, 23, 22)
    for y in range(19, 23):
        for x in range(2, 23):
            m.put(x, y, STONES[scatter(x, y)])
    m.put(9, 18, A["EKKYKLEMA_L_WOOD"], True)   # the rolling stage, parked
    m.put(10, 18, A["EKKYKLEMA_R_WOOD"], True)
    for x, y in ((2, 19), (7, 19), (16, 19), (21, 19)):   # the vintner's vines
        m.put(x, y, 0x21C, True)
        m.put(x + 1, y, 0x21D, True)
    m.put(5, 19, 0x209, True)          # a tall wine jar
    m.put(5, 20, 0x211, True)
    m.put(15, 21, A["TABLE_L_STONE"], True)
    m.put(16, 21, A["TABLE_R_STONE"], True)
    m.put(17, 21, A["AMPHORA_STONE"], True)
    m.put(18, 22, A["AMPHORA_STONE"], True)
    m.put(8, 21, A["AMPHORA_STONE"], True)
    m.put(9, 21, A["AMPHORA_STONE"], True)
    m.put(2, 22, 0x212, True)
    m.put(22, 22, 0x212, True)
    m.person("Koryphaios", 4, 21, gfx="ACTOR")
    m.person("Tragic", 20, 20, gfx="ACOLYTE_M", facing="UP")

    # --- Act I: the harbor, behind a row of footlights with one gap ---------------------
    room(1, 25, 23, 30)
    m.rect(2, 27, 22, 27, A["SAND"])
    m.rect(2, 29, 22, 30, A["SAND"])
    for x, y in ((4, 29), (15, 30), (21, 30), (8, 27), (17, 29)):
        m.put(x, y, A["SAND_SHELL"])
    for x in range(1, 24):
        if x != 21:
            m.put(x, 28, A["FOOTLIGHTS_WOOD"], True)
    for x in (3, 13):
        m.put(x, 27, A["SHIP_L_SAND"], True)
        m.put(x + 1, 27, A["SHIP_R_SAND"], True)
    m.put(2, 30, A["AMPHORA_SAND"], True)
    m.put(3, 30, A["URN_SAND"], True)
    m.put(10, 30, A["TORCH_SAND"], True)
    m.put(14, 30, A["AMPHORA_SAND"], True)
    m.put(6, 30, A["URN_SAND"], True)
    m.put(7, 30, A["AMPHORA_SAND"], True)
    m.put(22, 29, A["TORCH_SAND"], True)
    # He faces the row behind the gap, so once beaten he never blocks it.
    m.person("Comic", 18, 27, gfx="ACOLYTE_M", facing="RIGHT", sight=3)

    # --- The scenery walls --------------------------------------------------------------
    for y, act in FACADES:
        wall(1, 23, y)
        m.put(1, y, 0x233, True)  # laughing and weeping, the theater's sign
        m.put(23, y, 0x234, True)
        for i, x in enumerate(DOOR_X):
            m.put(x, y + 1, DOOR, True)
            m.json["bg_events"].append(bg(x, y + 1, m.prefix + f"Door{act + 1}{'LMR'[i]}"))
        for x, tile, name in panels:
            m.sign(name, x, y + 1, tile)
    # Act I's harbor is painted on the wall behind it; Act II's house wears vines.
    for x in range(2, 23):
        m.put(x, 23, A["BACKDROP_SEA_SAIL"] if x in (5, 15) else A["BACKDROP_SEA"], True)
        if x not in DOOR_X and x not in (3, 7, 13, 19):
            m.put(x, 24, A["DADO_SEA"], True)
        m.put(x, 15, 0x201 if x % 2 else 0x202, True)
    m.sign("FrescoLast", 3, 24, 0x203)
    m.sign("FrescoFollow", 3, 16, 0x203)
    for y in (18, 26):   # trapdoors in front of every door the acts can drop you from
        for x in DOOR_X:
            m.put(x, y, A["TRAPDOOR"])

    # --- The green room, backstage -------------------------------------------------------
    room(1, 33, 23, 40)
    for x, mask, shelf in ((2, 0x233, 0x280), (3, 0x27E, 0x281), (4, 0x235, 0x282)):
        m.put(x, 31, mask, True)
        m.sign("Masks", x, 32, shelf)
    m.sign("Rules", 22, 32, 0x241)
    for x in (7, 9):     # two dressing places: a bronze mirror and a stool
        m.put(x, 33, A["MIRROR_SHADOW"], True)
        m.put(x, 34, A["STOOL_WOOD"], True)
    m.sign("Costumes", 15, 33, A["RACK_SHADOW"])
    m.put(14, 33, A["SHELVES_SHADOW"], True)
    m.put(16, 33, A["RACK_SHADOW"], True)
    m.put(17, 33, A["SHELVES_SHADOW"], True)
    m.sign("Script", 11, 35, 0x287)
    m.put(10, 35, 0x268, True)
    m.put(12, 36, 0x28D)  # the trapdoor drops you onto this rug
    m.put(13, 36, 0x28E)
    m.person("Prompter", 20, 36, gfx="ELDER_F", facing="LEFT")
    m.put(2, 38, A["CRATE_L_WOOD"], True)
    m.put(3, 38, A["CRATE_R_WOOD"], True)
    m.put(2, 37, 0x278, True)
    m.put(5, 38, 0x27B, True)
    m.put(16, 37, 0x285, True)
    m.put(17, 37, 0x286, True)
    m.put(21, 39, 0x278, True)
    m.put(22, 39, 0x27B, True)
    for x in (6, 7):     # spare costumes waiting on their rails
        m.put(x, 37, 0x28A, True)
    m.put(8, 38, 0x275, True)   # a prop table with a stool
    m.put(9, 38, 0x276, True)
    m.put(10, 38, 0x284, True)
    m.put(15, 39, 0x27B, True)
    m.put(19, 34, 0x288, True)
    for x, y in ((1, 35), (23, 35)):
        m.put(x, y, 0x28F, True)
    m.put(12, 40, 0x295)
    m.put(13, 40, 0x296)
    m.json["warp_events"] = [warp(12, 40, "ThyrsaCity", 2), warp(13, 40, "ThyrsaCity", 2)]
    m.save()


def amphitheater():
    """The Dionysia's theater, on the room tileset so its doors wear the temple's panels."""
    A = stage_ids()
    m = Map("ThyrsaCity_Amphitheater", 25, 27, True, "gTileset_ThyrsaRooms")
    m.rect(0, 0, 24, 26, VOID, True)
    m.rect(1, 0, 23, 0, WTOP, True)
    m.rect(1, 1, 23, 1, WBOT, True)
    for x, mask in zip(range(3, 23, 3), (0x233, 0x234, 0x236, 0x235, 0x27E, 0x233, 0x234)):
        m.put(x, 0, mask, True)
    # The stage, and the skene's front with its three doors.
    m.rect(1, 2, 23, 8, FLOOR)
    m.rect(1, 2, 23, 2, FLOOR_SHADOW)
    m.rect(4, 7, 20, 7, WTOP, True)
    m.rect(4, 8, 20, 8, WBOT, True)
    for x in range(5, 20):
        if x not in (6, 7, 12, 13, 18, 19):
            m.put(x, 7, 0x201 if x % 2 else 0x202, True)
    for x, door in ((6, "DoorLeft"), (12, "DoorMiddle"), (18, "DoorRight")):
        m.put(x, 8, DOOR, True)
        m.json["bg_events"].append(bg(x, 8, m.prefix + door))
    for x, name, tile in ((7, "PanelLeft", A["PANEL_VINES"]), (13, "PanelMiddle", A["PANEL_HOUSE"]),
                          (19, "PanelRight", A["PANEL_SHIP"])):
        m.put(x, 8, tile, True)
        m.json["bg_events"].append(bg(x, 8, "ThyrsaCity_TempleOfDionysus_EventScript_" + name))
    for x in (2, 22):
        m.put(x, 3, 0x28F, True)
    for x, tile in ((3, 0x265), (4, 0x278), (20, 0x278), (21, 0x265)):
        m.put(x, 5, tile, True)   # the festival's kraters and jars, set out on the stage
    # The orchestra and the seats, in stone.
    for y in range(9, 27):
        for x in range(1, 24):
            m.put(x, y, STONES[scatter(x, y, 1)])
    for y in (12, 16, 20):
        for x in (3, 4, 5, 6, 7, 8, 9, 10, 14, 15, 16, 17, 18, 19, 20, 21):
            m.put(x, y, A["BENCH_STONE"], True)
    m.put(12, 11, 0x219, True)   # the thymele, the god's altar in the orchestra
    for x in (2, 22):
        for y in (11, 17, 23):
            m.put(x, y, 0x212, True)
    m.sign("Masks", 4, 21, A["RACK_STONE"])
    m.sign("Program", 20, 21, A["LECTERN_STONE"])
    m.put(12, 26, 0x295)
    m.put(13, 26, 0x296)
    m.json["warp_events"] = [warp(12, 26, "ThyrsaCity", 3), warp(13, 26, "ThyrsaCity", 3)]
    m.person("Thespis", 4, 18, gfx="ACOLYTE_M")
    m.person("Chorus", 12, 4, gfx="TITAN_GRUNT", flag="FLAG_ICHOR_DIONYSIA_BROKEN")
    m.person("Actor", 6, 4, gfx="YOUTH_M")
    m.person("BeeWoman", 18, 4, gfx="WOMAN")
    m.person("Kleon", 7, 15, gfx="KLEON")
    m.person("Alethea", 17, 15, gfx="ALETHEA")
    for x in (10, 12, 14):
        m.person("Fate" + str(x), x, 2, script=m.prefix + "Actor", gfx="ELDER_F")
    for block, y in enumerate((13, 17, 21)):
        for x in (8, 16):
            m.person(f"Audience{block}_{x}", x, y, script=m.prefix + "Audience",
                     gfx="PILGRIM", facing="UP")
    m.json["coord_events"] = [dict(type="trigger", x=x, y=23, elevation=0,
        var="VAR_TEMP_1", var_value="0", script=m.prefix + "Performance") for x in range(10, 15)]
    m.save()



def main():
    roads = [road(*r) for r in ROADS if r[0] not in BUILT_ELSEWHERE]
    for m in roads:
        m.save()
    eleusa = read("data/maps/EleusaVillage/map.json")
    eleusa["connections"] = [c for c in eleusa["connections"] if c["direction"] != "up"]
    eleusa["connections"].append(dict(direction="up", map="MAP_ROUTE6_ELEUTHERAI_ROAD", offset=34))
    eleusa["coord_events"] = [e for e in eleusa["coord_events"]
                              if e["script"] != "EleusaVillage_EventScript_NorthRoadBarrier"]
    eleusa["coord_events"] += [dict(type="trigger", x=x, y=6, elevation=0,
        var="VAR_TEMP_4", var_value="0", script="EleusaVillage_EventScript_NorthRoadBarrier")
        for x in range(44, 48)]
    write("data/maps/EleusaVillage/map.json", eleusa)

    town = Map("ThyrsaCity", 36, 32)
    town.rect(2, 2, 33, 29, 0x001)
    town.rect(10, 7, 13, 31, 0x1D9)
    town.rect(5, 17, 30, 21, 0x1D9)
    town.rect(10, 7, 29, 12, 0x1D9)
    town.connection("down", "Route7_KroniaGrounds")
    town.connection("left", "Route8_KopaisRoad", 8)
    town.rect(0, 18, 5, 21, 0x1D9)
    clinic = [[0x048, 0x049, 0x04A, 0x04B], [0x050, 0x051, 0x052, 0x053],
              [0x058, 0x059, 0x05A, 0x05B], [0x060, 0x061, 0x062, 0x063]]
    shop = [[0x028, 0x029, 0x029, 0x02B], [0x030, 0x031, 0x032, 0x033],
            [0x038, 0x039, 0x03A, 0x03B], [0x060, 0x041, 0x042, 0x043]]
    temple = [[0x1AA, 0x1AB, 0x1AB, 0x1AB, 0x1AB, 0x1AC],
              [0x1B2, 0x1B3, 0x1B3, 0x1B3, 0x1B3, 0x1B4],
              [0x1B8, 0x1B9, 0x1BA, 0x1B3, 0x1BB, 0x1BC],
              [0x1C0, 0x1C1, 0x1C2, 0x1C5, 0x1C3, 0x1C4],
              [0x1C8, 0x1C9, 0x1CA, 0x1CD, 0x1CB, 0x1CC]]
    town.stamp(5, 22, clinic)
    town.stamp(16, 22, shop)
    town.stamp(8, 2, temple)
    town.stamp(25, 12, temple)
    town.put(28, 16, 0x1DB)
    for x, y, dest in ((6, 25, "Asclepeion"), (17, 25, "Agora"),
                       (11, 6, "TempleOfDionysus"), (28, 16, "Amphitheater")):
        town.json["warp_events"].append(warp(x, y, "ThyrsaCity_" + dest, 0))
    town.person("Silenos", 23, 18, gfx="ELDER_M")
    town.person("Alethea", 14, 20, gfx="ALETHEA")
    town.person("Kleon", 26, 18, gfx="KLEON")
    town.person("Herald", 31, 8, gfx="PILGRIM")
    town.sign("CitySign", 14, 28)
    town.sign("TempleSign", 8, 7)
    town.sign("TheaterSign", 30, 17)
    town.save()

    clinic = hall("ThyrsaCity_Asclepeion", 15, 12)
    asclepeion(clinic, 7, 11)
    clinic.person("Healer", 7, 2, gfx="HEALER")
    clinic.stamp(2, 6, [[0x21B, 0x21C], [0x21D, 0x21E]])
    clinic.json["warp_events"] = [warp(7, 11, "ThyrsaCity", 0)]
    clinic.save()
    shop = hall("ThyrsaCity_Agora", 12, 10)
    shop.rect(3, 4, 8, 4, 0x213, True)
    shop.person("Merchant", 5, 3, gfx="WOMAN")
    shop.stamp(9, 2, [[0x21F, 0x220], [0x221, 0x222], [0x223, 0x224]])
    shop.json["warp_events"] = [warp(6, 9, "ThyrsaCity", 1)]
    shop.save()

    temple()
    amphitheater()

    wild = read("src/data/wild_encounters.json")
    group = next(g for g in wild["wild_encounter_groups"] if g.get("for_maps"))
    ids = {"MAP_" + const(r[0]) for r in ROADS if r[0] not in BUILT_ELSEWHERE}
    group["encounters"] = [e for e in group["encounters"] if e.get("map") not in ids]
    for name, _, level, _ in ROADS:
        if name in BUILT_ELSEWHERE:
            continue
        for time in ("Morning", "Day", "Evening", "Night"):
            species = ["AMPELIX", "GALEKIT", "NEBREL", "SPALUNK", "MELIBEE", "PEBBLITH"]
            if time == "Night":
                species[1:3] = ["LYKOPUP", "PROSOMIME"]
            group["encounters"].append(dict(map="MAP_" + const(name),
                base_label="g" + name + "_" + time,
                land_mons=dict(encounter_rate=15, mons=[
                    dict(min_level=level, max_level=level + 3, species="SPECIES_" + species[i % 6])
                    for i in range(12)])))
    write("src/data/wild_encounters.json", wild)
    trainers()


def trainers():
    path = ROOT / "src/data/trainers.party"
    marker = "/* Connected Thyrsa chapter: generated by tools/ichor/maps/thyrsa.py. */"
    end = "/* End connected Thyrsa chapter. */"
    before, _, generated = path.read_text().partition(marker)
    after = generated.partition(end)[2]
    text = before.rstrip() + "\n\n" + marker + "\n"
    classes = {"HOPLITE": ("Hoplite", "Hoplite"), "HARVESTER": ("Harvester", "Harvester"),
               "PILGRIM": ("Pilgrim", "Pilgrim"), "ACOLYTE_F": ("Acolyte", "Acolyte F"),
               "ACOLYTE_M": ("Acolyte", "Acolyte M"), "SHEPHERD": ("Shepherd", "Shepherd"),
               "AUGUR": ("Augur", "Augur"), "TITAN_GRUNT": ("Titanborn", "Titan Grunt")}
    def party(name, display, cls, pic, mons, difficulty=None):
        nonlocal text
        text += f"\n=== TRAINER_ICHOR_{name} ===\nName: {display}\nClass: {cls}\nPic: {pic}\nGender: Male\nMusic: Male\n"
        if difficulty:
            text += "Difficulty: " + difficulty + "\n"
        text += "AI: " + ("Smart Trainer" if difficulty == "Hard" else "Basic Trainer") + "\n"
        for i, (species, level, moves) in enumerate(mons):
            held = " @ Sitrus Berry" if difficulty == "Hard" else ""
            text += f"\n{species}{held}\nLevel: {level}\n"
            iv = 31 if difficulty == "Hard" else 18
            text += f"IVs: {iv} HP / {iv} Atk / {iv} Def / {iv} SpA / {iv} SpD / {iv} Spe\n"
            if difficulty == "Hard":
                if species == "Raknit":
                    text += "EVs: 4 HP / 252 Atk / 252 Spe\nAdamant Nature\n"
                elif species == "Prosomime":
                    text += "EVs: 4 HP / 252 SpA / 252 Spe\nTimid Nature\n"
                else:
                    text += "EVs: 252 HP / 128 Def / 128 SpA\nBold Nature\n"
            if moves:
                text += "".join("- " + move + "\n" for move in moves)
    for _, _, base, roster in ROADS:
        pairs = [("Galekit", "Ampelix"), ("Ergant", "Elapling"), ("Spalunk", "Pebblith"),
                 ("Botrykit", "Prosomime"), ("Eripip", "Chelonet"), ("Lykopup", "Melibee")]
        for i, ((name, gfx, _, _), pair) in enumerate(zip(roster, pairs)):
            cls, pic = classes[gfx]
            level = base + 3 + (i // 3)
            party(name, name, cls, pic, [(s, min(30, level + j), None) for j, s in enumerate(pair)])
    for name, species in (("COMIC", "Botrykit"), ("TRAGIC", "Prosomime"), ("SATYR", "Ampelix")):
        party("THYRSA_" + name, name, "Acolyte", "Acolyte M", [(species, 28, None), ("Raknit", 29, None)])
    # The chorus that shoves a wrongly masked actor back offstage, every time.
    party("THYRSA_CHORUS", "CHORUS", "Acolyte", "Acolyte M", [("Elapling", 28, None), ("Botrykit", 28, None)])
    sets = [
        ("Prosomime", 30, ["Psybeam", "Clear Smog", "Hypnosis", "Encore"]),
        ("Raknit", 30, ["Poison Jab", "Bite", "String Shot", "Protect"]),
        ("Ampelix", 31, ["Venoshock", "Giga Drain", "Leech Seed", "Toxic"]),
        ("Thyrsivy", 32, ["Venoshock", "Giga Drain", "Toxic", "Protect"]),
    ]
    for difficulty, delta in ((None, 0), ("Easy", -3), ("Hard", 0)):
        party("THESPIS", "THESPIS", "Hierophant", "Acolyte M",
              [(s, level + delta, moves) for s, level, moves in sets], difficulty)
    party("SILENOS", "SILENOS", "Acolyte", "Acolyte M",
          [("Midonos", 33, None), ("Botrykit", 34, None), ("Thyrsivy", 35, None)])
    path.write_text(text + "\n" + end + after)


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["theater"]:
        # Only the temple, the amphitheater and the trainers: main() would also
        # rebuild the city and roads, which have since been restored by hand.
        temple()
        amphitheater()
        trainers()
    else:
        main()
