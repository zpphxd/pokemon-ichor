#!/usr/bin/env python3
"""Build the approved Arkadia--Nemea--Emporion return loop."""
from thyrsa import Map, const, obj, read, write, ROOT

ROADS = [
    ("Route13_HighlandRoad", "R13", 30,
     ["POLYDOROS", "ANTHE", "LYKON", "THEANO", "KALLIAS", "AGLAON"]),
    ("Route14_NemeaRoad", "R14", 31,
     ["ISON", "PHILOMELE", "NEOKLES", "ERATO", "DEMADES", "KLEARCHOS"]),
]


def roads():
    for name, tag, base, names in ROADS:
        m = Map(name, 48, 24)
        m.json["music"] = "MUS_ICHOR_ROAD"
        if tag == "R13":
            m.rect(0, 0, 47, 23, 0x0E1, True)
        m.rect(0, 10, 47, 13, 0x1D9)
        for x0, x1 in ((4, 11), (23, 31), (39, 43)):
            m.rect(x0, 4, x1, 19, 0x001)
            m.rect(x0, 5, x1 - 1, 7, 0x00D)
            m.rect(x0 + 1, 16, x1, 18, 0x00D)
        for x in (16, 34):
            m.rect(x, 10, x + 3, 13, 0x00D)
        if tag == "R14":
            # Emporion's established Nemea gate is one tile wide, at city y=41.
            m.rect(44, 0, 47, 23, 0x0E1, True)
            m.rect(44, 11, 47, 11, 0x1D9)
        m.connection("left", "Arkadia" if tag == "R13" else "Nemea")
        m.connection("right", "Nemea" if tag == "R13" else "EmporionCity",
                     0 if tag == "R13" else -30)
        scripts = [f"mapscripts {name}_MapScripts {{}}"]
        positions = [(14, 10, "DOWN", 3), (6, 6, "RIGHT", 1), (26, 6, "DOWN", 1),
                     (32, 10, "DOWN", 3), (29, 18, "LEFT", 1), (41, 18, "UP", 1)]
        for i, (trainer, (x, y, facing, sight)) in enumerate(zip(names, positions)):
            m.person(trainer, x, y, gfx=("HOPLITE", "HARVESTER", "PILGRIM",
                                       "ACOLYTE_F", "SHEPHERD", "AUGUR")[i],
                     facing=facing, sight=sight)
            scripts.append(f'''script {m.prefix}{trainer} {{
    trainerbattle_single(TRAINER_ICHOR_{tag}_{trainer},
        format("The Isthmus is below us. One more battle before the descent?"),
        format("You kept your footing."))
    msgbox(format("Nemea's healer keeps a lamp burning by the road."), MSGBOX_AUTOCLOSE)
    end
}}''')
        for (x, y), suffix, item in zip(((4, 4), (23, 19), (42, 4)),
                ("HEAL", "BALL", "ETHER"), ("HYPER_POTION", "ULTRA_BALL", "ETHER")):
            e = obj("", x, y, "Common_EventScript_FindItem",
                    flag=f"FLAG_ICHOR_ITEM_{tag}_{suffix}")
            e.pop("local_id")
            e.update(graphics_id="OBJ_EVENT_GFX_ITEM_BALL",
                     trainer_sight_or_berry_tree_id="ITEM_" + item)
            m.json["object_events"].append(e)
        for (x, y), suffix, item in zip(((10, 5), (30, 18), (42, 19)),
                ("HONEY", "REVIVE", "REPEL"), ("HONEY", "REVIVE", "SUPER_REPEL")):
            m.json["bg_events"].append(dict(type="hidden_item", x=x, y=y, elevation=3,
                item="ITEM_" + item, flag=f"FLAG_ICHOR_HIDDEN_ITEM_{tag}_{suffix}",
                quantity=1, underfoot=False))
        directions = ("West: Arkadia. East: Nemea, then Emporion." if tag == "R13"
                      else "West: Nemea and Arkadia. East: Emporion's Nemea Gate.")
        for i, x in enumerate((2, 45)):
            m.sign("Sign" + str(i), x, 10 if tag == "R14" and i == 1 else 9)
            scripts.append(f'''script {m.prefix}Sign{i} {{
    msgbox(format("{directions}"), MSGBOX_SIGN)
    end
}}''')
        m.rect(26, 8, 28, 9, 0x001)
        m.sign("Herm", 27, 8, tile=0x01B)
        scripts.append(f'''script {m.prefix}Herm {{
    goto(EventScript_IchorGreatHerm)
}}''')
        (ROOT / f"data/maps/{name}/scripts.pory").write_text("\n\n".join(scripts) + "\n")
        m.save()


def nemea():
    m = Map("Nemea", 28, 32)
    m.json["music"] = "MUS_ICHOR_ROAD"
    m.rect(2, 2, 25, 29, 0x001)
    m.rect(0, 10, 27, 13, 0x1D9)
    m.rect(10, 6, 13, 27, 0x1D9)
    m.connection("left", "Route13_HighlandRoad")
    m.connection("right", "Route14_NemeaRoad")
    m.person("Healer", 18, 10, gfx="HEALER")
    m.rect(17, 11, 19, 11, 0x149, True)
    m.person("Merchant", 19, 18, gfx="MERCHANT")
    m.rect(17, 17, 21, 17, 0x149, True)
    m.person("Guide", 6, 13, gfx="SHEPHERD")
    m.sign("Sign", 14, 14)
    for x in (8, 12, 16):
        m.put(x, 3, 0x060, True)
        m.put(x, 4, 0x068, True)
    m.sign("Zeus", 12, 6)
    m.rect(4, 23, 8, 25, 0x0E1, True)
    m.sign("LionCave", 6, 26, tile=0x0E0)
    m.save()


def old_connections():
    path = "data/maps/EmporionCity/map.json"
    m = read(path)
    m["connections"] = [c for c in m["connections"] if c["map"] != "MAP_ROUTE14_NEMEA_ROAD"]
    m["connections"].append(dict(direction="left", map="MAP_ROUTE14_NEMEA_ROAD", offset=30))
    guard = next(e for e in m["object_events"] if e.get("local_id") == "LOCALID_EMPORION_HOPLITE_NEMEA")
    guard["flag"] = "FLAG_ICHOR_ARKADIA_NORTH_OPEN"
    write(path, m)


def encounters_and_teams():
    wild = read("src/data/wild_encounters.json")
    group = next(g for g in wild["wild_encounter_groups"] if g.get("for_maps"))
    ids = {"MAP_" + const(r[0]) for r in ROADS}
    group["encounters"] = [e for e in group["encounters"] if e.get("map") not in ids]
    for name, tag, level, _ in ROADS:
        for time in ("Morning", "Day", "Evening", "Night"):
            species = ["KLADOE", "GALENYON", "CAIRNOLITH", "ELAPLING", "KERAZAP", "NEMELEON"]
            if tag == "R14":
                species[3:5] = ["HOPLOMEX", "MELISSEER"]
            if time == "Night":
                species[0:2] = ["LYKANAX", "HARPELLE"]
            group["encounters"].append(dict(map="MAP_" + const(name),
                base_label=f"g{name}_{time}", land_mons=dict(encounter_rate=15,
                    mons=[dict(min_level=level, max_level=level + 2,
                               species="SPECIES_" + species[i % 6]) for i in range(12)])))
    write("src/data/wild_encounters.json", wild)
    path = ROOT / "src/data/trainers.party"
    start, end = "/* Nemea return teams. */", "/* End Nemea return teams. */"
    before, _, old = path.read_text().partition(start)
    after = old.partition(end)[2]
    text = before.rstrip() + "\n\n" + start + "\n"
    pairs = [("Galenyon", "Hoplomex"), ("Thyrsivy", "Elapling"),
             ("Cairnolith", "Kerazap"), ("Harpelle", "Prosomime"),
             ("Nemeleon", "Kladoe"), ("Lykanax", "Melisseer")]
    for _, tag, base, names in ROADS:
        for i, name in enumerate(names):
            cls, pic = [("Hoplite", "Hoplite"), ("Harvester", "Harvester"),
                        ("Pilgrim", "Pilgrim"), ("Acolyte", "Acolyte F"),
                        ("Shepherd", "Shepherd"), ("Augur", "Augur")][i]
            text += f"\n=== TRAINER_ICHOR_{tag}_{name} ===\nName: {name}\nClass: {cls}\nPic: {pic}\n"
            text += ("Gender: Female\n" if i in (1, 3) else "Gender: Male\n")
            text += "Music: Male\nAI: Basic Trainer\n"
            for j, species in enumerate(pairs[i]):
                text += f"\n{species}\nLevel: {base + 3 + i // 3 + j}\n"
                text += "IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe\n"
    path.write_text(text + "\n" + end + after + ("" if after else "\n"))


if __name__ == "__main__":
    roads()
    nemea()
    old_connections()
    encounters_and_teams()
