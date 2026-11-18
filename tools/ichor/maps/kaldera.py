#!/usr/bin/env python3
"""Build Thera's crescent harbor, the Bronze Servants and the Telchines forge."""
import struct
import sys

import water_tables
from thyrsa import ROOT, Map, asclepeion, bg, const, hall, read, warp, write
from astyra import CLINIC, HOUSE, LIBRARY
from salt_well import hidden, item

sys.path.insert(0, str(ROOT / "tools/ichor/art"))
import cave_dark_kit as kit
import plan_hook  # noqa: E402  (tools/ichor/wild_plan.py)

CAT = read("data/tilesets/secondary/cave_dark/catalog.json")
PIECES = {p["key"]: p["ids"] for p in CAT["pieces"]}


def town():
    m = Map("Kaldera", 40, 40)
    m.cells = [0x1170] * (m.w * m.h)
    land = set()
    for y in range(2, 38):
        for x in range(4, 39):
            outer = ((x - 22) / 17) ** 2 + ((y - 20) / 18) ** 2 < 1
            inner = ((x - 12) / 15) ** 2 + ((y - 20) / 10) ** 2 < 1
            if outer and not inner:
                land.add((x, y))
    for x0, y0, x1, y1 in ((26, 3, 36, 12), (26, 13, 37, 28),
                           (18, 29, 33, 36)):
        land.update((x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1))
    for x, y in land:
        n, s = (x, y - 1) not in land, (x, y + 1) not in land
        w, e = (x - 1, y) not in land, (x + 1, y) not in land
        row, col = (0 if n else 2 if s else 1), (0 if w else 2 if e else 1)
        m.put(x, y, ((0x11B, 0x11C, 0x11D), (0x123, 0x124, 0x125),
                     (0x12B, 0x12C, 0x12D))[row][col])
        if not (n or s or w or e) and (x + 2 * y) % 11 < 2:
            m.put(x, y, 0x109)
    m.rect(29, 9, 32, 30, 0x1D9)
    m.rect(20, 32, 31, 35, 0x1D9)
    m.rect(28, 19, 35, 21, 0x1D9)
    m.rect(28, 26, 35, 28, 0x1D9)
    m.rect(27, 9, 36, 9, 0x08F)
    m.rect(30, 9, 31, 10, 0x0CF)
    m.stamp(28, 3, LIBRARY)
    m.put(31, 7, 0x1CD)
    m.stamp(26, 14, CLINIC)
    m.put(27, 17, 0x061)
    m.stamp(33, 21, HOUSE)
    m.put(34, 24, 0x041)
    m.stamp(23, 29, [[0x008, 0x009, 0x00A], [0x010, 0x011, 0x012],
                     [0x018, 0x019, 0x01A], [0x020, 0x021, 0x022]])
    m.put(24, 32, 0x021)
    m.rect(26, 12, 29, 13, 0x1D9)
    m.put(26, 12, 0x1DB)
    m.json["warp_events"] = [
        warp(27, 17, "Kaldera_Asclepeion", 0),
        warp(34, 24, "Kaldera_Agora", 0),
        warp(24, 32, "Kaldera_SmithsHouse", 0),
        warp(31, 7, "Kaldera_TempleOfHephaestus", 0),
        warp(26, 12, "Kaldera_TelchinesForge", 0)]
    m.person("Nausikles", 19, 33, gfx="PILGRIM")
    m.person("Daphne", 22, 34, gfx="PROFESSOR_DAPHNE")
    m.person("HarborGuide", 28, 28, gfx="PILGRIM")
    m.person("AshWorker", 34, 13, gfx="KEDALION")
    m.sign("Sign", 21, 33)
    m.sign("ForgeSign", 25, 13)
    m.sign("TempleSign", 34, 9, tile=0x130)
    item(m, 30, 35, "ULTRA_BALL", "ITEM_KALDERA_BALL")
    hidden(m, 36, 27, "SHOAL_SALT", "HIDDEN_ITEM_KALDERA_SALT")
    hidden(m, 26, 34, "HEART_SCALE", "HIDDEN_ITEM_KALDERA_SCALE")
    m.json["coord_events"] = [dict(type="trigger", x=x, y=34, elevation=0,
        var="VAR_TEMP_1", var_value="0", script=m.prefix + "Letter") for x in (19, 20)]
    m.json["allow_cycling"] = False
    m.save()
    (ROOT / "data/layouts/Kaldera/border.bin").write_bytes(struct.pack("<4H", *([0x1170] * 4)))


def rooms():
    m = hall("Kaldera_Asclepeion", 18, 12)
    m.json["music"] = read("data/maps/ThyrsaCity_Asclepeion/map.json")["music"]
    asclepeion(m, 8, 2)
    m.person("Healer", 8, 2, gfx="HEALER")
    m.json["warp_events"] = [warp(9, 11, "Kaldera", 0)]
    m.save()
    m = hall("Kaldera_Agora", 16, 12)
    m.rect(3, 3, 11, 3, 0x20C, True)
    m.rect(12, 5, 13, 8, 0x20C, True)
    m.person("Merchant", 7, 4, gfx="MERCHANT")
    m.person("Customer", 4, 8, gfx="PILGRIM")
    m.json["warp_events"] = [warp(8, 11, "Kaldera", 1)]
    m.save()
    m = hall("Kaldera_SmithsHouse", 16, 14)
    m.rect(2, 3, 5, 3, 0x20C, True)
    m.rect(11, 4, 13, 6, 0x20C, True)
    m.rect(3, 8, 5, 9, 0x20C, True)
    m.person("Smith", 8, 5, gfx="KEDALION")
    m.person("Apprentice", 10, 9, gfx="ACOLYTE_M")
    m.json["warp_events"] = [warp(8, 13, "Kaldera", 2)]
    m.save()


SERVANTS = [
    ("Teach", 10, 38, "FLAG_TEMP_1"),
    ("TestOne", 9, 24, "FLAG_TEMP_2"),
    ("TestTwo", 18, 24, "FLAG_TEMP_3"),
    ("MasterOne", 8, 10, "FLAG_TEMP_4"),
    ("MasterTwo", 14, 10, "FLAG_TEMP_5"),
    ("MasterThree", 20, 10, "FLAG_TEMP_6"),
]


def temple():
    m = hall("Kaldera_TempleOfHephaestus", 28, 46)
    m.rect(0, 2, 2, 44, 0x205, True)
    m.rect(25, 2, 27, 44, 0x205, True)
    for y in (5, 18, 32):
        m.rect(3, y, 24, y, 0x205, True)
    for name, x, y, _ in SERVANTS:
        m.person(name, x, y, script=m.prefix + "Servant")
        actor = m.json["object_events"][-1]
        actor.update(graphics_id="OBJ_EVENT_GFX_SPECIES(KOLOSSARD)",
            movement_type="MOVEMENT_TYPE_WALK_SEQUENCE_DOWN_RIGHT_UP_LEFT",
            movement_range_x=1, movement_range_y=2 if name == "MasterThree" else 1)
        m.put(x, y + 1, 0x131)
        m.sign("Dial" + name, x - 2, y + 1, tile=0x20C)
    m.person("Drum", 20, 13, script="EventScript_StrengthBoulder")
    m.json["object_events"][-1]["graphics_id"] = "OBJ_EVENT_GFX_PUSHABLE_BOULDER"
    m.person("SmithOne", 21, 40, gfx="ACOLYTE_M", facing="LEFT", sight=3)
    m.person("SmithTwo", 5, 29, gfx="ACOLYTE_M", facing="RIGHT", sight=1)
    m.person("SmithThree", 22, 16, gfx="ACOLYTE_M", facing="LEFT", sight=3)
    m.person("Talos", 14, 3, gfx="KEDALION")
    m.sign("Rule", 16, 43)
    m.json["warp_events"] = [warp(14, 45, "Kaldera", 3)]
    m.json["allow_cycling"] = False
    m.save()
    path = ROOT / "data/maps/Kaldera_TempleOfHephaestus/scripts.pory"
    start, end = "// Generated servant dials.", "// End servant dials."
    before, _, old = path.read_text().partition(start)
    after = old.partition(end)[2]
    text = before.rstrip() + "\n\n" + start + "\n"
    for i, (name, x, y, flag) in enumerate(SERVANTS):
        stage = "TEACH" if i == 0 else "TEST" if i < 3 else "MASTER"
        local_id = "LOCALID_KALDERA_TEMPLE_OF_HEPHAESTUS_" + name.upper()
        text += f"""
script Kaldera_TempleOfHephaestus_EventScript_Dial{name} {{
    lockall
    if (flag(FLAG_ICHOR_FORGE_{stage}) || flag({flag})) {{
        msgbox(format("The bronze feet are settled. The dial rests."))
        releaseall
        end
    }}
    setvar(VAR_0x8004, {local_id})
    setvar(VAR_0x8005, {x})
    setvar(VAR_0x8006, {y + 1})
    setvar(VAR_0x800B, {flag})
    setvar(VAR_0x8009, {1 if name == "MasterThree" else 0})
    call(KalderaTemple_EventScript_Dial)
    call(KalderaTemple_EventScript_Check)
    releaseall
}}
"""
    text += "\nscript KalderaTemple_EventScript_Reset {\n"
    for name, x, y, _ in SERVANTS:
        local_id = "LOCALID_KALDERA_TEMPLE_OF_HEPHAESTUS_" + name.upper()
        text += (f"    setobjectxyperm({local_id}, {x}, {y})\n"
                 f"    setobjectmovementtype({local_id}, MOVEMENT_TYPE_WALK_SEQUENCE_DOWN_RIGHT_UP_LEFT)\n")
    text += "    setobjectxyperm(LOCALID_KALDERA_TEMPLE_OF_HEPHAESTUS_DRUM, 20, 13)\n    return\n}\n"
    path.write_text(text + end + after + ("" if after else "\n"))


def forge():
    m = Map("Kaldera_TelchinesForge", 34, 30)
    grid = [["#"] * m.w for _ in range(m.h)]
    for x0, y0, x1, y1 in ((3, 22, 9, 27), (7, 18, 16, 24),
                           (12, 8, 17, 22), (5, 12, 13, 16),
                           (16, 15, 28, 20), (12, 4, 29, 10),
                           (24, 8, 29, 16)):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                grid[y][x] = "."
    for y in range(18, 22):
        for x in range(18, 25):
            grid[y][x] = "~"
    tiles = kit.autotile(["".join(r) for r in grid], CAT, "wet")
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            m.put(x, y, tile, grid[y][x] == "#")
            if grid[y][x] == "~":  # the pool: elevation 1, open, so it can be fished (as in the Salt Well)
                m.cells[y * m.w + x] = tile | 0x1000
    m.put(6, 25, PIECES["hole_down"][0][0])
    m.stamp(23, 5, [[0x2FA, 0x2FB], [0x302, 0x303]])
    m.rect(7, 20, 17, 20, 0x2C1, True)
    m.person("Talos", 21, 8, gfx="KEDALION")
    m.person("Hyperion", 24, 8, gfx="TITAN_GRUNT", flag="FLAG_ICHOR_HIDE_KALDERA_HYPERION")
    for name, x, y in (("Petros", 10, 22), ("Amathos", 14, 13), ("Phlogios", 27, 13)):
        m.person(name, x, y, gfx="TITAN_GRUNT", facing="DOWN", sight=2)
    item(m, 6, 13, "ETHER", "ITEM_KALDERA_FORGE_ETHER")
    item(m, 27, 18, "REVIVE", "ITEM_KALDERA_FORGE_REVIVE")
    hidden(m, 8, 26, "RED_SHARD", "HIDDEN_ITEM_KALDERA_FORGE_SHARD")
    hidden(m, 28, 6, "NUGGET", "HIDDEN_ITEM_KALDERA_FORGE_NUGGET")
    m.json["warp_events"] = [warp(6, 25, "Kaldera", 4)]
    m.sign("Rest", 8, 23, tile=PIECES["stele"][0][0])
    m.sign("Rest", 20, 6, tile=PIECES["dish_covered"][0][0])
    m.sign("Gate", 13, 21, tile=PIECES["stele"][0][0])
    m.json["allow_escaping"] = True
    m.save()
    layouts = read("data/layouts/layouts.json")
    next(l for l in layouts["layouts"] if l.get("id") == m.json["layout"])["secondary_tileset"] = "gTileset_CaveDark"
    write("data/layouts/layouts.json", layouts)
    border = kit.kit_id(CAT, "T|...", "wet") | 0x3400
    (ROOT / "data/layouts/Kaldera_TelchinesForge/border.bin").write_bytes(struct.pack("<4H", *([border] * 4)))


def encounters_and_teams():
    wild = read("src/data/wild_encounters.json")
    group = next(g for g in wild["wild_encounter_groups"] if g.get("for_maps"))
    names = {"MAP_KALDERA", "MAP_KALDERA_TELCHINES_FORGE"}
    group["encounters"] = [e for e in group["encounters"] if e.get("map") not in names]
    for name, level, species in (
            ("Kaldera", 34, ("TAURIVET", "LAOLITH", "PYRAPOD", "KAMINOO")),
            ("Kaldera_TelchinesForge", 36, ("TAURIVET", "LAOLITH", "PYRAPOD", "PLOUTERAS"))):
        for time in ("Morning", "Night"):
            entry = dict(map="MAP_" + const(name), base_label="g" + name + "_" + time)
            entry["land_mons"] = dict(encounter_rate=4 if name == "Kaldera" else 10,
                mons=[dict(min_level=level, max_level=level + 3,
                    species="SPECIES_" + species[i % 4]) for i in range(12)])
            if name == "Kaldera":
                for field, count in (("water_mons", 5), ("fishing_mons", 10)):
                    sea = ("GALENYON", "KARKITOX", "NARKERAY", "SEISMARE")
                    entry[field] = dict(encounter_rate=6, mons=[
                        dict(min_level=34, max_level=37, species="SPECIES_" + sea[i % 4])
                        for i in range(count)])
            group["encounters"].append(entry)
    water_tables.apply(group["encounters"], {"MAP_KALDERA_TELCHINES_FORGE"})
    plan_hook.apply(group["encounters"])  # the distribution pass has the last word (design/DISTRIBUTION.md)
    write("src/data/wild_encounters.json", wild)
    teams = [
        ("SMITH_ONE", "ALKIMOS", [("Taurivet", 38), ("Karkitox", 38)]),
        ("SMITH_TWO", "CHALKE", [("Kolossard", 39), ("Taurivet", 39)]),
        ("SMITH_THREE", "PYRAICHMES", [("Kolossard", 40), ("Karkitox", 40)]),
        ("PETROS", "PETROS", [("Laolith", 40), ("Taurivet", 40)]),
        ("AMATHOS", "AMATHOS", [("Plouteras", 40), ("Pyrapod", 41)]),
        ("PHLOGIOS", "PHLOGIOS", [("Laolith", 41), ("Pyrapod", 42)]),
        ("TALOS", "TALOS", [("Taurivet", 41), ("Karkitox", 41), ("Kolossard", 42), ("Kolossard", 43)]),
        ("HYPERION", "HYPERION", [("Taurivet", 41), ("Laolith", 42), ("Pyrapod", 43), ("Gigantomb", 44)]),
    ]
    moves = {
        "Taurivet": ("Iron Head", "Heat Crash", "Work Up", "Protect"),
        "Karkitox": ("Crabhammer", "Poison Jab", "Swords Dance", "Protect"),
        "Kolossard": ("Iron Head", "Bulldoze", "Rock Slide", "Iron Defense"),
        "Laolith": ("Rock Slide", "Bulldoze", "Brick Break", "Iron Defense"),
        "Pyrapod": ("Flamethrower", "Psybeam", "Will-O-Wisp", "Calm Mind"),
        "Gigantomb": ("Heat Crash", "Rock Slide", "Stealth Rock", "Yawn"),
    }
    path = ROOT / "src/data/trainers.party"
    start, end = "/* Kaldera teams. */", "/* End Kaldera teams. */"
    before, _, old = path.read_text().partition(start)
    after = old.partition(end)[2]
    text = before.rstrip() + "\n\n" + start + "\n"
    for key, name, party in teams:
        boss = key in ("TALOS", "HYPERION")
        for difficulty in (("", 0), ("Easy", -3), ("Hard", 0)) if boss else (("", 0),):
            mode, offset = difficulty
            titan = key in ("PETROS", "AMATHOS", "PHLOGIOS", "HYPERION")
            klass = "Titan Admin" if key == "HYPERION" else "Titanborn" if titan else "Hierophant" if boss else "Acolyte"
            pic = "Titan Grunt" if titan else "Acolyte M"
            text += (f"\n=== TRAINER_ICHOR_KALDERA_{key} ===\nName: {name}\n"
                     f"Class: {klass}\nPic: {pic}\nGender: Male\nMusic: Male\n")
            if mode:
                text += f"Difficulty: {mode}\n"
            text += "AI: Smart Trainer\n" if mode == "Hard" else "AI: Basic Trainer\n"
            for species, level in party:
                item_name = " @ Sitrus Berry" if mode == "Hard" else ""
                iv = 31 if mode == "Hard" else 20
                text += (f"\n{species}{item_name}\nLevel: {level + offset}\n"
                         f"IVs: {iv} HP / {iv} Atk / {iv} Def / {iv} SpA / {iv} SpD / {iv} Spe\n")
                if mode == "Hard":
                    special = species == "Pyrapod"
                    text += "EVs: 252 HP / 252 " + ("SpA" if special else "Atk") + " / 4 SpD\n"
                    text += "Modest Nature\n" if special else "Adamant Nature\n"
                if boss:
                    text += "".join("- " + move + "\n" for move in moves[species])
    path.write_text(text + "\n" + end + after + ("" if after else "\n"))


if __name__ == "__main__":
    town()
    rooms()
    temple()
    forge()
    encounters_and_teams()
