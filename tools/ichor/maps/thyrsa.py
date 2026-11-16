#!/usr/bin/env python3
"""Build the connected Eleusa--Kithairon--Thyrsa chapter using existing Greek art."""
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


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
    def __init__(self, name, w, h, indoor=False):
        self.name, self.w, self.h = name, w, h
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
        border = 0x3400 | (0x205 if self.indoor else 0x0E0)
        (path / "border.bin").write_bytes(struct.pack("<4H", *([border] * 4)))
        layouts = read("data/layouts/layouts.json")
        layout = next(l for l in layouts["layouts"] if l.get("id") == self.json["layout"])
        layout.update(width=self.w, height=self.h, primary_tileset="gTileset_Aethos",
                      secondary_tileset="gTileset_Civic" if self.indoor else "gTileset_Kalliste")
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


def hall(name, w, h):
    m = Map(name, w, h, True)
    m.rect(1, 2, w - 2, h - 1, 0x201)
    m.rect(0, 0, w - 1, 0, 0x205, True)
    m.rect(0, 1, w - 1, 1, 0x208, True)
    m.put(w // 2, h - 1, 0x242)
    return m


def main():
    roads = [road(*r) for r in ROADS]
    roads[0].connection("down", "EleusaVillage", -34)
    roads[0].connection("up", "MtKithairon")
    roads[1].connection("down", roads[0].name)
    roads[1].connection("up", roads[2].name)
    roads[1].json["music"] = "MUS_ICHOR_ROAD"
    roads[2].connection("down", roads[1].name)
    roads[2].connection("up", "ThyrsaCity")
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
    town.connection("down", roads[2].name)
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
    clinic.rect(4, 4, 10, 4, 0x213, True)
    clinic.rect(4, 3, 10, 3, 0x211)
    clinic.person("Healer", 7, 3, gfx="HEALER")
    clinic.stamp(11, 2, [[0x21F, 0x220], [0x221, 0x222], [0x223, 0x224]])
    clinic.json["bg_events"].append(bg(11, 4, clinic.prefix + "Pithos"))
    clinic.json["bg_events"].append(bg(12, 4, clinic.prefix + "Pithos"))
    clinic.stamp(2, 6, [[0x21B, 0x21C], [0x21D, 0x21E]])
    clinic.json["warp_events"] = [warp(7, 11, "ThyrsaCity", 0)]
    clinic.save()
    shop = hall("ThyrsaCity_Agora", 12, 10)
    shop.rect(3, 4, 8, 4, 0x213, True)
    shop.person("Merchant", 5, 3, gfx="WOMAN")
    shop.stamp(9, 2, [[0x21F, 0x220], [0x221, 0x222], [0x223, 0x224]])
    shop.json["warp_events"] = [warp(6, 9, "ThyrsaCity", 1)]
    shop.save()

    for name in ("TempleOfDionysus", "Amphitheater"):
        m = Map("ThyrsaCity_" + name, 25, 27, True)
        m.rect(1, 2, 23, 26, 0x250)
        m.rect(0, 0, 24, 0, 0x205, True)
        m.rect(0, 1, 24, 1, 0x208, True)
        m.put(12, 26, 0x242)
        m.json["warp_events"] = [warp(12, 26, "ThyrsaCity", 2 if name == "TempleOfDionysus" else 3)]
        for x in (2, 22):
            for y in (5, 11, 17, 23):
                m.stamp(x, y, [[0x20B], [0x20C], [0x20D]])
        for x, door in ((6, "Comedy"), (12, "Tragedy"), (18, "Satyr")):
            m.put(x, 8, 0x208, True)
            m.json["bg_events"].append(bg(x, 8, m.prefix + door))
        m.sign("Masks", 4, 21, 0x003)
        m.sign("Program", 20, 21, 0x003)
        if name == "TempleOfDionysus":
            m.person("Thespis", 12, 3, gfx="ACOLYTE_M")
            for person, x, y in (("Comic", 6, 18), ("Tragic", 18, 18), ("SatyrActor", 12, 12)):
                m.person(person, x, y, gfx="ACOLYTE_M")
            for x in range(1, 24):
                m.put(x, 5, 0x149, True)
        else:
            for y in (12, 16, 20):
                for x in (6, 8, 14, 16):
                    m.stamp(x, y, [[0x240, 0x241]])
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

    wild = read("src/data/wild_encounters.json")
    group = next(g for g in wild["wild_encounter_groups"] if g.get("for_maps"))
    ids = {"MAP_" + const(r[0]) for r in ROADS}
    group["encounters"] = [e for e in group["encounters"] if e.get("map") not in ids]
    for name, _, level, _ in ROADS:
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
            text += "IVs: 18 HP / 18 Atk / 18 Def / 18 SpA / 18 SpD / 18 Spe\n"
            if difficulty == "Hard":
                text += "EVs: 252 HP / 128 SpA / 128 Spe\nModest Nature\n"
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
    main()
