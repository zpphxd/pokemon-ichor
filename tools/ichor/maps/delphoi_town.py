#!/usr/bin/env python3
"""Delphoi (design/maps/Delphoi.md; SCRIPT.md III-6C to III-8, Part 2). 52 x 46,
on delphoi.

Bottom to top, the way a pilgrim climbs it: up from the gorge at the south-east
onto the little square (the Asclepeion and the Agora), the lower town's lane of
houses running west under the sanctuary's wall, the Kastalian spring in the
cleft of the Phaedriades to the east; through the sanctuary's gate onto the
Sacred Way, which switches back three times past the Siphnians' treasury,
Kleobis and Biton, the Rock of the Sibyl with the oldest altar and the
Naxians' sphinx, Astyra's treasury and the Lesche; up the stair in the
polygonal wall to the Omphalos court before the Temple of Apollo, with the
altar of the Chians; the theatre cut into the slope above to the west, the
god's laurel grove to the east; and at the top, the stadium, with the
north-west gate onto Route 29.

The bottom six rows meet the gorge (another secondary) and use only aethos.

  /usr/bin/python3 tools/ichor/maps/delphoi_town.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from delphoi_maps import POND, A, DMap, Plan, _hash, npc, paint, trainer  # noqa: E402

W, H = 52, 46
NAME = "Delphoi"
S = "Delphoi_EventScript_"

# where things stand (top-left cells)
TEMPLE = (20, 8)            # 7 x 5; door (23, 12)
OMPHALOS = (22, 14)         # 2 x 2
ALTAR = (27, 14)            # 3 x 2
SIPHNOS = (30, 26)          # 3 x 4; door (31, 29)
ASTYRA = (12, 20)           # 3 x 4; door (13, 23)
LESCHE = (36, 21)           # 5 x 3; door (39, 23)
KASTALIA = (43, 29)         # 5 x 3
ASCLEPEION = (31, 33)       # aethos 4 x 4; door (32, 36)
AGORA = (36, 33)            # aethos 4 x 4; door (37, 36)
HOUSES = [("house_melissai", 3, 34, "MAP_DELPHOI_HOUSE_OF_THE_MELISSAI"),
          ("house_pilgrims", 9, 34, "MAP_DELPHOI_PILGRIMS_HOUSE"),
          ("house_koretas", 15, 34, "MAP_DELPHOI_KORETAS_HOUSE"),
          ("house_a", 20, 34, "MAP_DELPHOI_THEOKLES_HOUSE"),
          ("house_b", 25, 34, "MAP_DELPHOI_KITHARODE_HOUSE")]


def plan():
    P = Plan(W, H, fill="T")
    # the Phaedriades along the east, and the rock above everything
    P.box(43, 0, 51, 39, "#")
    P.box(0, 0, 51, 0, "#")
    # the stadium on the top terrace, the north-west gate
    P.box(1, 1, 33, 1, "U")
    P.box(1, 2, 33, 3, "s")           # the track (sand)
    P.box(0, 2, 0, 3, "p")
    # the theatre, cut into the slope west of the temple
    for i, y in enumerate(range(4, 9)):
        P.box(3 + i, y, 18 - i, y, "U")
    P.box(10, 4, 11, 8, "A")          # the aisle up the middle
    P.box(4, 9, 17, 10, "v")          # the orchestra's floor
    # the temple terrace and the Omphalos court
    P.box(19, 8, 33, 16, "v")
    P.box(18, 11, 18, 16, "v")
    P.box(14, 11, 17, 12, "v")
    P.box(34, 11, 35, 16, "v")
    # the god's laurel grove, east of the temple
    P.box(34, 2, 42, 10, "L")
    P.box(35, 3, 41, 9, "G")
    P.box(34, 10, 37, 10, ".")
    P.box(34, 1, 42, 1, "U")
    # the polygonal wall under the terrace, its stair
    P.box(8, 17, 41, 17, "W")
    P.box(23, 17, 23, 17, "S")
    # the Sacred Way: three switchbacks
    P.box(2, 18, 42, 31, ".")
    P.box(23, 18, 34, 19, "v")        # leg C, from the stair east
    P.box(33, 18, 34, 25, "v")        # down to leg B
    P.box(9, 24, 41, 25, "v")         # leg B, west
    P.box(9, 24, 10, 31, "v")         # down to leg A
    P.box(9, 30, 29, 31, "v")         # leg A, east to the gate
    # the sanctuary's wall and gate
    P.box(2, 32, 42, 32, "W")
    P.box(28, 32, 29, 32, "v")
    P.box(27, 32, 27, 32, "P")
    P.box(30, 32, 30, 32, "P")
    # the lower town: the lane, the square, the houses
    P.box(2, 33, 42, 39, ".")
    P.box(2, 37, 30, 38, "v")         # the lane
    P.box(26, 33, 41, 39, "v")        # the square
    P.box(30, 33, 41, 36, " ")
    # the spring in the cleft
    P.box(41, 28, 48, 39, ".")
    P.box(41, 28, 42, 39, "v")
    P.box(44, 32, 48, 36, "~")        # the Kastalian pools
    P.box(43, 32, 43, 37, "v")        # the walk beside them
    P.box(49, 28, 51, 39, "#")
    P.box(43, 28, 48, 28, "#")
    # the way down to the gorge (aethos only from row 40)
    P.box(0, 40, 51, 45, "T")
    P.road([(38, 39), (38, 45)], width=3, salt=21, bulge=False)
    P.box(37, 40, 41, 41, ".")
    P.box(41, 40, 41, 41, ".")
    # people's spots on the slope between the legs
    for (x, y, w, h) in ((2, 18, 6, 6), (36, 18, 6, 2)):
        P.box(x, y, x + w - 1, y + h - 1, ".")
    # bushes and terraces of grass between the legs
    P.box(12, 26, 27, 29, "o")
    P.box(14, 19, 22, 23, ".")
    P.box(2, 26, 8, 29, "o")
    # terrace lips between the legs: the slope steps down to the south
    P.box(11, 27, 29, 27, "J")
    P.box(24, 21, 31, 21, "J")
    P.box(3, 24, 7, 24, "J")
    return P


def way_kit(m):
    s = m.s("way")
    return {n: s["ids"][s["names"][n][1]][s["names"][n][0]] for n in ("TL", "T", "TR", "L", "C", "R", "BL", "B", "BR")}


def build():
    rows = plan().rows()
    m = DMap(NAME, "delphoi", W, H)
    m.seam("down")
    get = paint(m, rows, salt=60)
    kit = way_kit(m)
    m.path(get("v") | get("S") | get(" "), kit=kit)
    # plain flags in the middle of broad paving, with the odd cracked flag
    for (x, y) in get("v"):
        if int(m.mid[y, x]) == kit["C"] and _hash(x, y, 71) < 90:
            m.piece("way", "flag2" if _hash(x, y, 72) % 2 else "flag4", x, y, solid=False)
    for (x, y) in get("s"):
        m.set(x, y, A.SAND, False)
    for (x, y) in get("U") | get("A"):
        w, e = (x - 1, y) in get("U") | get("A"), (x + 1, y) in get("U") | get("A")
        name = "aisle" if (x, y) in get("A") else "W" if not w else "E" if not e else ("M" if x % 2 else "M2")
        m.piece("tiers", name, x, y, solid=False)
    for (x, y) in get("W"):
        w, e = (x - 1, y) in get("W"), (x + 1, y) in get("W")
        m.piece("polywall", "W" if not w else "E" if not e else ("M" if x % 3 else "M2"), x, y, solid=True)
    for (x, y) in get("S"):
        m.piece("polywall", "stair", x, y, solid=False)
    for (x, y) in get("P"):
        m.piece("polywall", "pier", x, y, solid=True)
    m.grove(get("L"), salt=61)
    m.scatter(get(".") - {c for c in get(".") if c[1] >= 40}, "ground",
              ["tuft", "pebbles", "thyme", "stones"], rate=140, salt=62)
    # the monuments
    m.put("temple_apollo", *TEMPLE)
    m.put("omphalos", *OMPHALOS)
    m.put("altar_chians", *ALTAR)
    m.put("treasury_siphnos", *SIPHNOS)
    m.put("treasury_astyra", *ASTYRA)
    m.put("lesche", *LESCHE)
    m.put("kastalia", *KASTALIA)
    m.put("kleobis_biton", 17, 28)
    m.put("sibyl_rock", 19, 21)
    m.put("oldest_altar", 21, 22)
    m.put("sphinx_column", 17, 20)
    m.put("great_laurel", 37, 4)
    m.piece("balbis", "sill", 3, 2)
    m.piece("balbis", "sill", 3, 3)
    m.piece("balbis", "post", 32, 2)
    for (x, y) in ((22, 19), (28, 19), (32, 24), (20, 25), (11, 26), (16, 30), (24, 30)):
        m.piece("torch", "cold", x, y, solid=True)
    # the lower town
    for (k, x, y, _dest) in HOUSES:
        m.put(k, x, y)
    m.block(A.ASCLEPEION, *ASCLEPEION)
    m.block(A.AGORA, *AGORA)
    m.set(ASCLEPEION[0] + 1, ASCLEPEION[1] + 3, A.ASCLEPEION[3][1], False)
    m.set(AGORA[0] + 1, AGORA[1] + 3, A.AGORA[3][1], False)
    m.border = [m.s("phaedriades")["ids"][1][1], m.s("phaedriades")["ids"][1][2],
                m.s("phaedriades")["ids"][2][1], m.s("phaedriades")["ids"][2][2]]
    m.border = [A.PINE_TOP[0], A.PINE_TOP[1], A.PINE_BOT[0], A.PINE_BOT[1]]
    events(m)
    way = m.s("way")
    allow = {A.GRASS, A.TALL, way_kit(m)["C"], way_kit(m)["T"], way_kit(m)["B"], way_kit(m)["L"], way_kit(m)["R"]}
    allow |= {m.s("tiers")["ids"][0][i] for i in (1, 2)}
    m.break_runs(keep=get("p") | {(23, y) for y in range(13, 20)}, allow=allow, longest=9,
                 props=[("torch", "cold"), (None, A.STELE), ("bush", "laurel")])
    m.connect("down", 26, "MAP_ROUTE28_KASTALIAN_GORGE")
    m.header = {"ichor_kind": "town"}
    return m, rows


def events(m):
    # warps
    m.warp(TEMPLE[0] + 3, TEMPLE[1] + 4, "MAP_DELPHOI_TEMPLE_OF_APOLLO", 0)
    m.warp(SIPHNOS[0] + 1, SIPHNOS[1] + 3, "MAP_DELPHOI_SIPHNIAN_TREASURY", 0)
    m.warp(ASTYRA[0] + 1, ASTYRA[1] + 3, "MAP_DELPHOI_ASTYRAN_TREASURY", 0)
    m.warp(LESCHE[0] + 3, LESCHE[1] + 2, "MAP_DELPHOI_LESCHE", 0)
    m.warp(ASCLEPEION[0] + 1, ASCLEPEION[1] + 3, "MAP_DELPHOI_ASCLEPEION", 0)
    m.warp(AGORA[0] + 1, AGORA[1] + 3, "MAP_DELPHOI_AGORA", 0)
    for (k, x, y, dest) in HOUSES:
        dx, dy = m.s(k)["names"]["door"]
        m.warp(x + dx, y + dy, dest, 0)
    # signs and things to read
    m.set(36, 39, A.STELE, True)
    m.sign(36, 39, S + "SignTown")
    m.set(1, 4, A.STELE, True)
    m.sign(1, 4, S + "SignNorthWest")
    m.sign(TEMPLE[0] + 3, TEMPLE[1] + 3, S + "Inscription", facing="BG_EVENT_PLAYER_FACING_NORTH")
    m.sign(OMPHALOS[0], OMPHALOS[1] + 1, S + "Omphalos")
    m.sign(OMPHALOS[0] + 1, OMPHALOS[1] + 1, S + "Omphalos")
    m.sign(17, 29, S + "KleobisBiton")
    m.sign(18, 29, S + "KleobisBiton")
    m.sign(19, 22, S + "SibylRock")
    m.sign(21, 22, S + "OldestAltar")
    m.sign(17, 22, S + "Sphinx")
    m.sign(ALTAR[0] + 1, ALTAR[1] + 1, S + "AltarChians")
    m.sign(KASTALIA[0], KASTALIA[1] + 2, S + "Spring")
    m.sign(38, 6, S + "GreatLaurel")
    # III-6C: arrival and the Pythia's procession
    for x in (38, 39, 40):
        m.trigger(x, 39, S + "Arrival", "VAR_TEMP_1", 1)
    npc(m, "ICHOR_PRIESTESS", 41, 30, S + "Pythia", face="left", flag="FLAG_ICHOR_HIDE_PYTHIA_PROCESSION",
        local_id="LOCALID_DELPHOI_PYTHIA")
    npc(m, "ICHOR_ACOLYTE_F", 41, 29, S + "Melissa", face="left", flag="FLAG_ICHOR_HIDE_PYTHIA_PROCESSION",
        local_id="LOCALID_DELPHOI_MELISSA_1")
    npc(m, "ICHOR_ACOLYTE_F", 41, 31, S + "Melissa", face="left", flag="FLAG_ICHOR_HIDE_PYTHIA_PROCESSION",
        local_id="LOCALID_DELPHOI_MELISSA_2")
    npc(m, "ICHOR_ALETHEA", 28, 31, S + "AletheaArrival", face="down", flag="FLAG_ICHOR_HIDE_ALETHEA_DELPHOI_STEPS",
        local_id="LOCALID_DELPHOI_ALETHEA")
    # the queue of pilgrims on the first switchback
    npc(m, "ICHOR_PILGRIM", 19, 31, S + "Pilgrim1", face="up", local_id="LOCALID_DELPHOI_PILGRIM_1")
    npc(m, "ICHOR_WOMAN", 20, 31, S + "Pilgrim2", face="up")
    npc(m, "ICHOR_ELDER_M", 21, 31, S + "Pilgrim3", face="up", local_id="LOCALID_DELPHOI_OLD_PILGRIM")
    npc(m, "ICHOR_MAN", 22, 31, S + "Pilgrim4", face="up")
    # the town's people
    npc(m, "ICHOR_ACOLYTE_F", 5, 37, S + "MelissaHives", face="up")
    npc(m, "ICHOR_ELDER_M", 41, 33, S + "DozingPilgrim", face="right")
    npc(m, "ICHOR_HOPLITE", 0, 2, S + "GateGuard", face="right")
    npc(m, "ICHOR_AUGUR", 9, 4, S + "Iamos", face="up")
    npc(m, "ICHOR_YOUTH_M", 18, 2, S + "Orsippos", face="left", wander=False)
    # Kleon and Rhea: the stadium (11-13), then the court's gate (13)
    npc(m, "ICHOR_KLEON", 24, 3, S + "KleonStadium", face="left", flag="FLAG_ICHOR_HIDE_KLEON_DELPHOI_STADIUM",
        local_id="LOCALID_DELPHOI_KLEON_STADIUM")
    npc(m, "ICHOR_WOMAN", 26, 1, S + "RheaStadium", face="down", flag="FLAG_ICHOR_HIDE_RHEA_DELPHOI_STADIUM",
        local_id="LOCALID_DELPHOI_RHEA_STADIUM")
    m.trigger(13, 2, S + "StadiumScene", "VAR_TEMP_2", 1)
    m.trigger(13, 3, S + "StadiumScene", "VAR_TEMP_2", 1)
    # Mom at the spring (III-7)
    npc(m, "ICHOR_MOM", 43, 32, S + "Mom", face="up", flag="FLAG_ICHOR_HIDE_MOM_DELPHOI_SPRING",
        local_id="LOCALID_DELPHOI_MOM")
    for x in (41, 42):
        m.trigger(x, 35, S + "MomScene", "VAR_TEMP_3", 1)
    # III-8: the night at the gate of the Omphalos court
    m.trigger(23, 18, S + "OmphalosNight", "VAR_TEMP_4", 1)
    npc(m, "ICHOR_KLEON", 22, 18, S + "KleonGate", face="up", flag="FLAG_ICHOR_HIDE_KLEON_DELPHOI_GATE",
        local_id="LOCALID_DELPHOI_KLEON_GATE")
    npc(m, "ICHOR_WOMAN", 24, 18, S + "RheaGate", face="up", flag="FLAG_ICHOR_HIDE_RHEA_DELPHOI_GATE",
        local_id="LOCALID_DELPHOI_RHEA_GATE")
    for i, (x, y) in enumerate(((19, 15), (19, 16))):
        npc(m, "ICHOR_TITAN_GRUNT", x, y, S + "Gigas", face="down", flag="FLAG_ICHOR_HIDE_OMPHALOS_GIGAS",
            local_id=f"LOCALID_DELPHOI_GIGAS_{i + 1}")
    npc(m, "ICHOR_HOPLITE", 22, 16, S + "Hyperion", face="up", flag="FLAG_ICHOR_HIDE_OMPHALOS_HYPERION",
        local_id="LOCALID_DELPHOI_HYPERION")
    npc(m, "ICHOR_HEALER", 21, 15, S + "Phaedon", face="up", flag="FLAG_ICHOR_HIDE_OMPHALOS_PHAEDON",
        local_id="LOCALID_DELPHOI_PHAEDON")
    npc(m, "ICHOR_ELDER_M", 28, 31, S + "Aristeides", face="up", flag="FLAG_ICHOR_HIDE_OMPHALOS_ARCHON",
        local_id="LOCALID_DELPHOI_ARCHON")
    npc(m, "ICHOR_MOM", 21, 14, S + "MomStair", face="right", flag="FLAG_ICHOR_HIDE_MOM_STAIRHEAD",
        local_id="LOCALID_DELPHOI_MOM_STAIR")
    npc(m, "ICHOR_ALETHEA", 24, 14, S + "AletheaStair", face="left", flag="FLAG_ICHOR_HIDE_MOM_STAIRHEAD",
        local_id="LOCALID_DELPHOI_ALETHEA_STAIR")
    for i, (x, y) in enumerate(((22, 20), (24, 21), (34, 22), (12, 25))):
        npc(m, "ICHOR_TITAN_GRUNT", x, y, S + "Titanborn", face="up", flag="FLAG_ICHOR_HIDE_OMPHALOS_MUSTER",
            local_id=f"LOCALID_DELPHOI_MUSTER_{i + 1}")
    # the entrance herm, beside the arrival from the falls (fast travel)
    m.set(37, 41, A.HERM, True)
    m.sign(37, 41, S + "EntranceHerm")
    # items
    m.item_ball(2, 18, "ITEM_ULTRA_BALL", "FLAG_ICHOR_ITEM_DELPHOI_ULTRA_BALL")
    m.hidden(KASTALIA[0] + 1, KASTALIA[1] + 2, "ITEM_PEARL", "FLAG_ICHOR_HIDDEN_ITEM_DELPHOI_PEARL")
    m.hidden(3, 4, "ITEM_STARDUST", "FLAG_ICHOR_HIDDEN_ITEM_DELPHOI_STARDUST")
    m.hidden(22, 21, "ITEM_RELIC_COPPER", "FLAG_ICHOR_HIDDEN_ITEM_DELPHOI_BRONZE_OBOL")


def splice_consts(m):
    """The metatile ids the scripts swap (torches, the Omphalos's three states),
    written into the map's scripts.pory between markers."""
    import re
    s = m.s
    lines = ["// delphoi_town: begin generated (tools/ichor/maps/delphoi_town.py; don't edit)"]
    lines.append(f"const METATILE_DELPHOI_TORCH_COLD = 0x{s('torch')['ids'][0][0]:03X}")
    lines.append(f"const METATILE_DELPHOI_TORCH_LIT = 0x{s('torch')['ids'][0][1]:03X}")
    for key, tag in (("omphalos", "WHOLE"), ("omphalos_burning", "BURNING"), ("omphalos_open", "OPEN")):
        ids = s(key)["ids"]
        for (dx, dy, n) in ((0, 0, "TL"), (1, 0, "TR"), (0, 1, "BL"), (1, 1, "BR")):
            lines.append(f"const METATILE_DELPHOI_OMPHALOS_{tag}_{n} = 0x{ids[dy][dx]:03X}")
    lines.append("// delphoi_town: end generated")
    p = Path(__file__).resolve().parents[3] / "data/maps/Delphoi/scripts.pory"
    t = p.read_text()
    block = chr(10).join(lines)
    if "delphoi_town: begin generated" in t:
        t = re.sub(r"// delphoi_town: begin generated.*?// delphoi_town: end generated", lambda _m: block, t,
                   flags=re.S)
    else:
        t = block + chr(10) + chr(10) + t
    p.write_text(t)


if __name__ == "__main__":
    m, rows = build()
    splice_consts(m)
    print("\n".join(rows))
    m.build(NAME.lower(), starts=[(39, 45)],
            views=[(38, 38), (15, 36), (20, 28), (22, 18), (10, 6), (38, 6), (45, 32), (14, 22), (24, 12)])
