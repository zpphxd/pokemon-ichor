#!/usr/bin/env python3
"""Build the Eleusa--Daphni--Astyra road and the capital's first story rooms."""
from thyrsa import ROOT, Map, bg, hall, obj, read, warp, write
from nemea import roads, encounters_and_teams

ROADS = [
    ("Route15_MysteryRoad", "R15", 32,
     ["TIMON", "HEGESO", "POLEMON", "PHILA", "AGIS", "PRAXON"]),
    ("Route16_CapitalPass", "R16", 34,
     ["NIKIAS", "TIMARETE", "KLEOBIS", "DIOTIMA", "ARISTON", "EUBIOS"]),
]
CLINIC = [[0x048, 0x049, 0x04A, 0x04B], [0x050, 0x051, 0x052, 0x053],
          [0x058, 0x059, 0x05A, 0x05B], [0x060, 0x061, 0x062, 0x063]]
HOUSE = [[0x028, 0x029, 0x029, 0x02B], [0x030, 0x031, 0x032, 0x033],
         [0x038, 0x039, 0x03A, 0x03B], [0x060, 0x041, 0x042, 0x043]]
LIBRARY = [[0x1AA, 0x1AB, 0x1AB, 0x1AB, 0x1AB, 0x1AC],
           [0x1B2, 0x1B3, 0x1B3, 0x1B3, 0x1B3, 0x1B4],
           [0x1B8, 0x1B9, 0x1BA, 0x1B3, 0x1BB, 0x1BC],
           [0x1C0, 0x1C1, 0x1C2, 0x1C5, 0x1C3, 0x1C4],
           [0x1C8, 0x1C9, 0x1CA, 0x1CD, 0x1CB, 0x1CC]]


def daphni():
    m = Map("Daphni", 28, 32)
    m.rect(2, 2, 25, 29, 0x001)
    m.rect(0, 10, 27, 13, 0x1D9)
    m.rect(10, 4, 13, 27, 0x1D9)
    m.connection("left", "Route15_MysteryRoad")
    m.connection("right", "Route16_CapitalPass")
    m.person("Healer", 18, 10, gfx="HEALER")
    m.rect(17, 11, 19, 11, 0x149, True)
    m.person("Merchant", 19, 18, gfx="MERCHANT")
    m.rect(17, 17, 21, 17, 0x149, True)
    m.person("Guide", 6, 13, gfx="PILGRIM")
    m.sign("Sign", 14, 14)
    m.sign("Laurel", 11, 5, tile=0x01B)
    m.save()


def city():
    m = Map("Astyra", 48, 48)
    m.rect(8, 8, 43, 43, 0x001)
    m.rect(0, 32, 43, 35, 0x1D9)
    m.rect(24, 9, 27, 43, 0x1D9)
    m.rect(9, 20, 39, 23, 0x1D9)
    m.connection("left", "Route16_CapitalPass", 22)
    m.stamp(8, 28, CLINIC)
    m.stamp(35, 28, HOUSE)
    m.stamp(7, 15, LIBRARY)
    m.rect(9, 32, 10, 33, 0x1D9)
    m.rect(36, 32, 37, 33, 0x1D9)
    m.rect(10, 20, 10, 23, 0x1D9)
    m.json["warp_events"] = [
        warp(9, 31, "Astyra_Asclepeion", 0),
        warp(36, 31, "Astyra_PhaedonsHouse", 0),
        warp(10, 19, "Astyra_Library", 0),
        warp(35, 18, "Astyra_Stoa", 0)]
    m.person("Preacher", 17, 34, gfx="AUGUR")
    m.person("Herald", 29, 34, gfx="PILGRIM")
    m.person("Merchant", 37, 36, gfx="MERCHANT")
    m.person("Alethea", 31, 23, gfx="ALETHEA", flag="FLAG_ICHOR_HIDE_ALETHEA_ASTYRA")
    m.person("Clerk", 37, 19, gfx="ELDER_M")
    m.rect(34, 17, 40, 18, 0x149, True)
    m.put(35, 18, 0x1DB)
    m.rect(21, 8, 30, 11, 0x0E1, True)
    m.person("Guard", 25, 12, gfx="HOPLITE")
    for name, x, y in (("Sign", 8, 36), ("ClinicSign", 12, 32),
                        ("HouseSign", 39, 32), ("LibrarySign", 13, 20),
                        ("Kodros", 18, 26), ("Kairos", 29, 26), ("Perdix", 27, 13)):
        m.sign(name, x, y)
    m.save()


def rooms():
    m = hall("Astyra_Asclepeion", 18, 12)
    m.json["music"] = "MUS_ICHOR_ASCLEPEION"
    m.rect(4, 4, 11, 4, 0x213, True)
    m.person("Phaedon", 8, 3, gfx="MAN")
    m.person("Panacoil", 12, 7)
    m.json["object_events"][-1]["graphics_id"] = "OBJ_EVENT_GFX_SPECIES(PANACOIL)"
    m.stamp(14, 2, [[0x21F, 0x220], [0x221, 0x222], [0x223, 0x224]])
    m.json["bg_events"].append(bg(14, 4, m.prefix + "Pithos"))
    m.sign("Hearth", 3, 7, tile=0x21B)
    m.json["warp_events"] = [warp(9, 11, "Astyra", 0)]
    m.save()
    m = hall("Astyra_PhaedonsHouse", 16, 14)
    m.json["music"] = "MUS_ICHOR_ELPIS_LULLABY"
    m.stamp(11, 2, [[0x21B, 0x21C], [0x21D, 0x21E]])
    m.rect(3, 7, 6, 8, 0x213, True)
    m.person("Elpis", 10, 4, gfx="KID_F")
    m.person("Phaedon", 8, 5, gfx="MAN", script="Astyra_PhaedonsHouse_EventScript_Visitor",
             flag="FLAG_ICHOR_HIDE_PHAEDON_HOUSE")
    m.person("Daphne", 6, 5, gfx="PROFESSOR_DAPHNE", script="Astyra_PhaedonsHouse_EventScript_Visitor",
             flag="FLAG_ICHOR_HIDE_DAPHNE_HOUSE")
    m.sign("Starry", 12, 5, tile=0x003)
    m.sign("MusicBox", 7, 3, tile=0x003)
    m.json["warp_events"] = [warp(8, 13, "Astyra", 1)]
    m.save()
    m = hall("Astyra_Library", 22, 16)
    m.json["music"] = "MUS_ICHOR_AKADEMIA"
    for x in (3, 7, 15, 18):
        m.stamp(x, 2, [[0x20B], [0x20C], [0x20D]])
    m.rect(3, 8, 7, 8, 0x213, True)
    m.rect(14, 10, 18, 10, 0x213, True)
    m.person("Daphne", 5, 7, gfx="PROFESSOR_DAPHNE")
    m.person("Librarian", 16, 9, gfx="ELDER_F")
    m.sign("Book", 6, 6, tile=0x003)
    m.json["warp_events"] = [warp(11, 15, "Astyra", 2)]
    m.save()


def stoa():
    m = hall("Astyra_Stoa", 36, 32)
    m.person("Archon", 17, 13, gfx="ELDER_M")
    m.person("Keeper", 21, 13, gfx="ELDER_M")
    m.person("Alethea", 19, 14, gfx="ALETHEA", flag="FLAG_ICHOR_HIDE_ALETHEA_ASTYRA")
    for name, x, gfx in (("Nikomache", 12, "MERCHANT"), ("Euphranor", 13, "PILGRIM"),
                          ("Kallippos", 14, "MAN"), ("Mnesippe", 22, "HARVESTER"),
                          ("Philinos", 23, "HOPLITE"), ("Theano", 24, "WOMAN")):
        m.person(name, x, 18, gfx=gfx, script="Astyra_Stoa_EventScript_Citizen")
    m.stamp(17, 14, [[0x21F, 0x220], [0x221, 0x222], [0x223, 0x224]])
    for x in (4, 29):
        m.stamp(x, 3, [[0x20B], [0x20C], [0x20D]])
    m.sign("Count", 23, 14, tile=0x003)
    m.json["warp_events"] = [warp(18, 31, "Astyra", 3)]
    m.save()


def roadside_cast():
    path = "data/maps/Route16_CapitalPass/map.json"
    m = read(path)
    m["object_events"].append(obj("LOCALID_ROUTE16_CAPITAL_PASS_ALETHEA", 43, 15,
        "Astyra_EventScript_RoadAlethea", gfx="ALETHEA", flag="FLAG_ICHOR_HIDE_ALETHEA_R16"))
    write(path, m)
    path = ROOT / "data/maps/Route16_CapitalPass/scripts.pory"
    path.write_text(path.read_text().replace("mapscripts Route16_CapitalPass_MapScripts {}",
        """mapscripts Route16_CapitalPass_MapScripts {
    MAP_SCRIPT_ON_TRANSITION {
        special(Ichor_ReleaseTimeOfDay)
        call(Astyra_EventScript_PlaceRoadAlethea)
    }
}""", 1))


def eleusa_connection():
    path = "data/maps/EleusaVillage/map.json"
    m = read(path)
    m["connections"] = [c for c in m["connections"] if c["direction"] != "right"]
    m["connections"].append(dict(direction="right", map="MAP_ROUTE15_MYSTERY_ROAD", offset=14))
    guard = next(e for e in m["object_events"] if e.get("local_id") == "LOCALID_ELEUSA_HOPLITE")
    guard["flag"] = "FLAG_ICHOR_ELEUSA_CAPITAL_OPEN"
    m["coord_events"] = [e for e in m["coord_events"] if e["script"] != "EleusaVillage_EventScript_RoadShut"]
    m["coord_events"] += [dict(type="trigger", x=49, y=y, elevation=0,
        var="VAR_TEMP_1", var_value="0", script="EleusaVillage_EventScript_RoadShut")
        for y in range(24, 28)]
    write(path, m)


if __name__ == "__main__":
    roads(ROADS)
    daphni()
    city()
    rooms()
    stoa()
    roadside_cast()
    eleusa_connection()
    encounters_and_teams(ROADS, "Astyra approach")
