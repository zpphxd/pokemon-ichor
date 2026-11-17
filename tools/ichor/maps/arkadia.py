#!/usr/bin/env python3
"""Build the approved Kopais--Gulf--Styx approach to Arkadia."""
import water_tables
from thyrsa import Map, bg, const, obj, read, warp, write, ROOT

ROUTES = [
    ("Route8_KopaisRoad", "R8", 26, ["PANOS", "AMPELIS", "KEPHALOS", "MEDA", "MELAS", "THYONE"]),
    ("Route9_ParnassosCrossroads", "R9", 27, ["POLYON", "MNASON", "AKESON", "ERYX", "PHILTA", "DEINON"]),
    ("Route11_DrumPass", "R11", 28, ["DORYS", "LACHON", "THRASEAS", "MYRINE", "PHERON", "XANTHE"]),
    ("Route12_CypressRoad", "R12", 29, ["STHENON", "BRISEIS", "OPHION", "DAMO", "PHANES", "KALLIN"]),
]
HEALERS = ("Lebadeia", "Kirrha", "Aigion", "Arkadia")
# Owned by tools/ichor/maps/gulf.py (layouts, events, scripts, wild tables): skipped here.
GULF = {"Route9_ParnassosCrossroads", "Kirrha", "Aigion", "Route11_DrumPass"}


def routes():
    for name, tag, base, names in ROUTES:
        if name in GULF:  # gulf.py builds it
            continue
        horizontal = tag == "R8"
        m = Map(name, 48 if horizontal else 24, 24 if horizontal else 40)
        if horizontal:
            m.rect(0, 0, 47, 23, 0x170, True)
            m.rect(0, 10, 47, 13, 0x1D9)
            for x0, x1 in ((4, 11), (24, 31), (42, 45)):
                m.rect(x0, 4, x1, 19, 0x001)
                m.rect(x0, 4, x1 - 2, 7, 0x00D)
                m.rect(x0, 16, x1 - 2, 19, 0x00D)
            for x in (16, 36):
                m.rect(x, 10, x + 3, 13, 0x00D)
            positions = [(8, 10, "DOWN", 3), (6, 6, "RIGHT", 1), (26, 6, "DOWN", 1),
                         (30, 10, "DOWN", 3), (29, 18, "LEFT", 1), (44, 18, "UP", 1)]
            rewards = [(4, 4), (24, 19), (44, 4)]
            hidden = [(10, 5), (30, 18), (44, 19)]
            signs = [(2, 9), (45, 9)]
            m.connection("right", "ThyrsaCity", -8)
            m.connection("left", "Lebadeia")
        else:
            if tag in ("R9", "R11"):
                m.rect(0, 0, 23, 39, 0x0E1, True)
            else:
                for y in range(40):
                    m.rect(0, y, 23, y, 0x00E if y % 2 == 0 else 0x016, True)
            m.rect(10, 0, 13, 39, 0x1D9)
            for y0, y1 in ((4, 9), (16, 21), (30, 35)):
                m.rect(4, y0, 19, y1, 0x001)
                m.rect(4, y0, 7, y1, 0x00D)
                m.rect(16, y0, 19, y1, 0x00D)
            for y in (10, 26):
                m.rect(10, y, 13, y + 3, 0x00D)
            m.rect(8, 12, 9, 15, 0x001)
            m.put(9, 14, 0x087)
            m.put(10, 15, 0x001)
            positions = [(10, 8, "RIGHT", 3), (5, 6, "DOWN", 1), (18, 19, "UP", 1),
                         (10, 22, "RIGHT", 3), (5, 32, "UP", 1), (18, 33, "LEFT", 1)]
            rewards = [(4, 4), (19, 17), (4, 34)]
            hidden = [(7, 4), (19, 21), (7, 34)]
            signs = [(14, 2), (14, 37)]
            north, south = {"R9": ("Lebadeia", "Kirrha"), "R11": ("Aigion", "StyxFalls"),
                            "R12": ("StyxFalls", "Arkadia")}[tag]
            m.connection("up", north)
            m.connection("down", south)
        if tag == "R11":
            m.rect(10, 23, 13, 25, 0x0E1, True)
            m.rect(11, 23, 11, 25, 0x1D9)
            drum = obj("LOCALID_ROUTE11_DRUM", 11, 24, "EventScript_StrengthBoulder")
            drum["graphics_id"] = "OBJ_EVENT_GFX_PUSHABLE_BOULDER"
            m.json["object_events"].append(drum)
        if tag == "R9":
            m.rect(18, 14, 21, 17, 0x1D9)
            m.sign("Delphoi", 21, 14)
        scripts = [f"mapscripts {name}_MapScripts {{}}"]
        for i, (trainer, (x, y, facing, sight)) in enumerate(zip(names, positions)):
            m.person(trainer, x, y, gfx=("HOPLITE", "HARVESTER", "PILGRIM", "ACOLYTE_F",
                                       "SHEPHERD", "AUGUR")[i], facing=facing, sight=sight)
            scripts.append(f'''script {m.prefix}{trainer} {{
    trainerbattle_single(TRAINER_ICHOR_{tag}_{trainer},
        format("A long road. Let's make it worth remembering."),
        format("Worth the walk."))
    msgbox(format("There's a healer at the next hamlet."), MSGBOX_AUTOCLOSE)
    end
}}''')
        for (x, y), suffix, item in zip(rewards, ("HEAL", "BALL", "ETHER"),
                                         ("HYPER_POTION", "ULTRA_BALL", "ETHER")):
            e = obj("", x, y, "Common_EventScript_FindItem", flag=f"FLAG_ICHOR_ITEM_{tag}_{suffix}")
            e.pop("local_id")
            e["graphics_id"] = "OBJ_EVENT_GFX_ITEM_BALL"
            e["trainer_sight_or_berry_tree_id"] = "ITEM_" + item
            m.json["object_events"].append(e)
        for (x, y), suffix, item in zip(hidden, ("HONEY", "REVIVE", "REPEL"),
                                         ("HONEY", "REVIVE", "SUPER_REPEL")):
            m.json["bg_events"].append(dict(type="hidden_item", x=x, y=y, elevation=3,
                item="ITEM_" + item, flag=f"FLAG_ICHOR_HIDDEN_ITEM_{tag}_{suffix}",
                quantity=1, underfoot=False))
        directions = {"R8": "East: Thyrsa. West: Lebadeia, along Lake Kopais.",
                      "R9": "North: Lebadeia. South: Kirrha and the Gulf trireme.",
                      "R11": "North: Aigion. South: Styx Falls. Column drums block the pass.",
                      "R12": "North: Styx Falls. South: Arkadia and the temple of Artemis."}
        for i, (x, y) in enumerate(signs):
            m.sign("Sign" + str(i), x, y)
            scripts.append(f'''script {m.prefix}Sign{i} {{
    msgbox(format("{directions[tag]}"), MSGBOX_SIGN)
    end
}}''')
        if tag == "R9":
            scripts.append(f'''script {m.prefix}Delphoi {{
    msgbox(format("Delphoi is above the falls. The water has taken the stair.\\p"
                  "The road continues south to Kirrha."), MSGBOX_SIGN)
    end
}}''')
        (ROOT / f"data/maps/{name}/scripts.pory").write_text("\n\n".join(scripts) + "\n")
        m.save()


def hubs():
    links = {"Lebadeia": [("right", "Route8_KopaisRoad"), ("down", "Route9_ParnassosCrossroads")],
             "Kirrha": [("up", "Route9_ParnassosCrossroads")],
             "Aigion": [("down", "Route11_DrumPass")],
             "StyxFalls": [("up", "Route11_DrumPass"), ("down", "Route12_CypressRoad")],
             "Arkadia": [("up", "Route12_CypressRoad"), ("right", "Route13_HighlandRoad")]}
    for name, connections in links.items():
        if name in GULF:  # gulf.py builds it
            continue
        m = Map(name, 28, 32)
        m.rect(2, 2, 25, 29, 0x001)
        m.rect(10, 2, 13, 29, 0x1D9)
        m.rect(5, 12, 23, 15, 0x1D9)
        for direction, dest in connections:
            m.connection(direction, dest)
            if direction == "up":
                m.rect(10, 0, 13, 2, 0x1D9)
            elif direction == "down":
                m.rect(10, 29, 13, 31, 0x1D9)
            elif direction == "right":
                m.rect(23, 10, 27, 13, 0x1D9)
        if name in HEALERS:
            m.person("Healer", 18, 10, gfx="HEALER")
            m.rect(17, 11, 19, 11, 0x149, True)
            m.person("Merchant", 19, 18, gfx="MERCHANT")
            for x in range(17, 22):
                m.put(x, 17, 0x149, True)
        m.person("Guide", 6, 13, gfx="ELDER_F")
        m.sign("Sign", 14, 14)
        if name in ("Kirrha", "Aigion"):
            m.rect(2, 23, 25, 31, 0x170, True)
            if name == "Aigion":
                m.rect(10, 23, 13, 31, 0x1D9)
            m.rect(19, 21, 20, 27, 0x1D9)
            m.person("Captain", 19, 26, gfx="SAILOR")
        if name == "StyxFalls":
            m.rect(21, 2, 24, 28, 0x147, True)
            m.rect(22, 3, 23, 16, 0x0B3, True)
            m.put(20, 18, 0x01B, True)
        if name == "Arkadia":
            for y in range(10, 14):
                m.json["coord_events"].append(dict(type="trigger", x=26, y=y, elevation=3,
                    var="VAR_TEMP_4", var_value="0", script="Arkadia_EventScript_NemeaRoad"))
            m.stamp(17, 2, [
                [0x1AA, 0x1AB, 0x1AB, 0x1AB, 0x1AB, 0x1AC],
                [0x1B2, 0x1B3, 0x1B3, 0x1B3, 0x1B3, 0x1B4],
                [0x1B8, 0x1B9, 0x1BA, 0x1B3, 0x1BB, 0x1BC],
                [0x1C0, 0x1C1, 0x1C2, 0x1C5, 0x1C3, 0x1C4],
                [0x1C8, 0x1C9, 0x1CA, 0x1CD, 0x1CB, 0x1CC]])
            m.rect(14, 7, 20, 8, 0x1D9)
            m.json["warp_events"] = [warp(20, 6, "Arkadia_TempleOfArtemis", 0)]
            m.person("Kleon", 7, 22, gfx="KLEON", flag="FLAG_ICHOR_KLEON_JOINED_TITANS")
            m.person("Alethea", 15, 22, gfx="ALETHEA", flag="FLAG_ICHOR_VISITED_ASTYRA")
            m.person("Iapetos", 5, 22, gfx="TITAN_GRUNT", flag="FLAG_ICHOR_HIDE_IAPETOS_ARKADIA")
            for x in range(10, 14):
                m.json["coord_events"].append(dict(type="trigger", x=x, y=23, elevation=3,
                    var="VAR_TEMP_1", var_value="0", script="Arkadia_EventScript_Recruitment"))
        m.save()


def grove():
    m = Map("Arkadia_TempleOfArtemis", 28, 72)
    m.json.update(allow_fly=False, allow_escape_rope=False)
    m.rect(12, 2, 13, 71, 0x1D9)
    for y0, y1 in ((50, 68), (28, 47), (6, 25)):
        m.rect(7, y0, 21, y1, 0x001)
    for x0, y0, x1, y1 in ((8, 39, 13, 43), (14, 31, 19, 35),
                           (17, 19, 21, 23), (6, 13, 10, 17), (17, 7, 21, 11)):
        m.rect(x0, y0, x1, y1, 0x1D9)
    for x, y in ((11, 60), (15, 44), (11, 38), (15, 32),
                 (15, 22), (11, 16), (15, 10)):
        m.put(x, y, 0x00E, True)
        m.put(x, y + 1, 0x016, True)
    hounds = [("HoundTeach", 12, 58, 4), ("HoundTest1", 12, 44, 4),
              ("HoundTest2", 16, 38, 4), ("HoundTest3", 12, 32, 4),
              ("HoundMaster1", 12, 20, 4), ("HoundMaster2", 16, 14, 4),
              ("HoundMaster3", 12, 8, 4)]
    for name, x, y, radius in hounds:
        m.person(name, x, y, script=m.prefix + "Hound")
        e = m.json["object_events"][-1]
        e.update(graphics_id="OBJ_EVENT_GFX_SPECIES(LYKOPUP)",
                 movement_type="MOVEMENT_TYPE_WALK_LEFT_AND_RIGHT",
                 movement_range_x=radius, movement_range_y=0)
    m.person("Hind", 20, 21, flag="FLAG_ICHOR_KALLISTO_TRIAL")
    m.json["object_events"][-1]["graphics_id"] = "OBJ_EVENT_GFX_SPECIES(KERAZAP)"
    for name, x, y in (("Teach", 10, 52), ("Test", 19, 36), ("Master", 10, 6)):
        m.person(name, x, y, gfx="ACOLYTE_F", facing="RIGHT", sight=3 if name != "Test" else 0)
    m.rect(10, 1, 15, 4, 0x1D9)
    m.person("Kallisto", 12, 2, gfx="ACOLYTE_F")
    m.sign("Altar", 15, 2, tile=0x01B)
    m.sign("Instructions", 16, 67)
    m.put(12, 71, 0x024)
    m.json["warp_events"] = [warp(12, 71, "Arkadia", 0)]
    for y, script in ((49, "TeachExit"), (27, "TestExit"), (5, "Dais")):
        for x in (12, 13):
            m.json["coord_events"].append(dict(type="trigger", x=x, y=y, elevation=3,
                var="VAR_TEMP_4", var_value="0", script=m.prefix + script))
    m.save()


def ferry():
    m = read("data/maps/GulfTrireme/map.json")
    m.update(connections=None, object_events=[
        obj("LOCALID_GULF_CAPTAIN", 19, 7, "GulfTrireme_EventScript_Captain", gfx="SAILOR"),
        obj("LOCALID_GULF_PASSENGER", 8, 7, "GulfTrireme_EventScript_Passenger", gfx="PILGRIM")],
        warp_events=[], coord_events=[], bg_events=[])
    write("data/maps/GulfTrireme/map.json", m)


def encounters_and_teams():
    wild = read("src/data/wild_encounters.json")
    g = next(g for g in wild["wild_encounter_groups"] if g.get("for_maps"))
    ids = {"MAP_" + const(r[0]) for r in ROUTES if r[0] not in GULF}  # gulf.py writes the Gulf's
    g["encounters"] = [e for e in g["encounters"] if e.get("map") not in ids]
    for name, tag, level, _ in ROUTES:
        if name in GULF:
            continue
        for time in ("Morning", "Day", "Evening", "Night"):
            species = ["NEBREL", "AMPELIX", "ERIPIP", "GALEKIT", "PEBBLITH", "MELIBEE"]
            if time == "Night":
                species[2:4] = ["LYKOPUP", "PROSOMIME"]
            g["encounters"].append(dict(map="MAP_" + const(name), base_label=f"g{name}_{time}",
                land_mons=dict(encounter_rate=15, mons=[dict(min_level=level, max_level=level + 2,
                    species="SPECIES_" + species[i % 6]) for i in range(12)])))
    water_tables.apply(g["encounters"], {"MAP_ROUTE8_KOPAIS_ROAD", "MAP_ROUTE12_CYPRESS_ROAD"})
    write("src/data/wild_encounters.json", wild)
    path = ROOT / "src/data/trainers.party"
    start, end = "/* Arkadia approach teams. */", "/* End Arkadia approach teams. */"
    before, _, old = path.read_text().partition(start)
    after = old.partition(end)[2]
    text = before.rstrip() + "\n\n" + start + "\n"
    pairs = [("Galekit", "Ampelix"), ("Ergant", "Elapling"), ("Spalunk", "Pebblith"),
             ("Raknit", "Prosomime"), ("Eripip", "Chelonet"), ("Lykopup", "Melibee")]
    for _, tag, base, names in ROUTES:
        for i, name in enumerate(names):
            cls, pic = [("Hoplite", "Hoplite"), ("Harvester", "Harvester"), ("Pilgrim", "Pilgrim"),
                        ("Acolyte", "Acolyte F"), ("Shepherd", "Shepherd"), ("Augur", "Augur")][i]
            text += f"\n=== TRAINER_ICHOR_{tag}_{name} ===\nName: {name}\nClass: {cls}\nPic: {pic}\n"
            text += ("Gender: Female\n" if i == 3 else "Gender: Male\n") + "Music: Male\nAI: Basic Trainer\n"
            for j, species in enumerate(pairs[i]):
                text += f"\n{species}\nLevel: {base + 4 + (i // 3) + j}\n"
                text += "IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe\n"
    path.write_text(text + "\n" + end + after + ("" if after else "\n"))


def hunt_teams():
    path = ROOT / "src/data/trainers.party"
    start, end = "/* Artemis hunt teams. */", "/* End Artemis hunt teams. */"
    before, _, old = path.read_text().partition(start)
    after = old.partition(end)[2]
    text = before.rstrip() + "\n\n" + start + "\n"
    for tag, team in (("TEACH", [("Lykopup", 32), ("Harpelle", 33)]),
                      ("TEST", [("Botrykit", 33), ("Lykanax", 34)]),
                      ("MASTER", [("Harpelle", 34), ("Lykanax", 35), ("Arkoby", 35)])):
        text += f"\n=== TRAINER_ICHOR_ARTEMIS_{tag} ===\nName: HUNTRESS\nClass: Acolyte\n"
        text += "Pic: Acolyte F\nGender: Female\nMusic: Female\nAI: Basic Trainer\n"
        for species, level in team:
            text += f"\n{species}\nLevel: {level}\n"
            text += "IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe\n"
    team = [
        ("Lykanax", 35, "Adamant", "4 HP / 252 Atk / 252 Spe", ["Crunch", "Ice Fang", "Howl", "Roar"]),
        ("Harpelle", 35, "Jolly", "4 HP / 252 Atk / 252 Spe", ["Night Slash", "Wing Attack", "Quick Attack", "Taunt"]),
        ("Oinopard", 36, "Jolly", "4 HP / 252 Atk / 252 Spe", ["Poison Jab", "Night Slash", "Fake Out", "Hone Claws"]),
        ("Starkos", 37, "Adamant", "252 HP / 252 Atk / 4 SpD", ["Crunch", "Play Rough", "Bulk Up", "Protect"]),
    ]
    for difficulty in ("Normal", "Easy", "Hard"):
        hard = difficulty == "Hard"
        text += "\n=== TRAINER_ICHOR_KALLISTO ===\nName: KALLISTO\nClass: Hierophant\nPic: Acolyte F\nGender: Female\nMusic: Female\n"
        if difficulty != "Normal":
            text += f"Difficulty: {difficulty}\n"
        text += "AI: " + ("Smart Trainer" if hard else "Basic Trainer") + "\n"
        for species, level, nature, evs, moves in team:
            text += f"\n{species}" + (" @ Sitrus Berry" if hard else "") + "\n"
            text += f"Level: {level - (3 if difficulty == 'Easy' else 0)}\n"
            iv = 31 if hard else 20
            text += f"IVs: {iv} HP / {iv} Atk / {iv} Def / {iv} SpA / {iv} SpD / {iv} Spe\n"
            if hard:
                text += f"EVs: {evs}\n{nature} Nature\n"
            text += "".join("- " + move + "\n" for move in moves)
    path.write_text(text + "\n" + end + after + ("" if after else "\n"))


def main():
    routes()
    hubs()
    grove()
    ferry()
    encounters_and_teams()
    hunt_teams()


if __name__ == "__main__":
    main()
