#!/usr/bin/env python3
"""Knossa's rooms above ground, every one its own shape (MAP_DESIGN.md §2): the
seven Amnisos houses, Bombylia's hut on the Bull Road, and the palace's four
(design/maps/Knossa*.md; SCRIPT.md Part 2, III-3D, III-3E, III-3O).

All draw on gTileset_PalaceRooms (Minoan rooms: frieze, red or gypsum field,
dado, gypsum floor; frescoes; furniture). Its two table pieces are counters
(MB_COUNTER), so the healer and the stallkeeper serve across them.

    python3 tools/ichor/maps/knossa_rooms.py [NAME ...] [--pass N]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from knossa_maps import Map, ensure_map  # noqa: E402

AMNISOS_WARPS = {"Asclepeion": 0, "Agora": 1, "Tavern": 2, "FishersHut": 3, "XeniaHouse": 4,
                 "LeapersHouse": 5, "KydonsHouse": 6}
PALACE_WARPS = {"ThroneRoom": 0, "WestMagazines": 1, "QueensMegaron": 2, "GrandStaircase": 3}


class Room(Map):
    def __init__(self, name, w, h):
        super().__init__(name, "palace_rooms", w, h, fill=0, primary="oikos")
        void = self.id("house", "void")
        self.mid[:] = void
        self.solid[:] = True
        self.border = [void] * 4

    def shell(self, x0, x1, y0, y1, exit_x, field="field", fields=None):
        """North wall three rows from y0 (frieze, field, dado), floor to y1-1,
        the south wall on y1 with the exit mat at exit_x."""
        for x in range(x0, x1 + 1):
            e = "_L" if x == x0 else ("_R" if x == x1 else "")
            f = (fields or {}).get(x, field)
            self.piece("house", "frieze" + e, x, y0)
            self.piece("house", ("field" + e) if e else f, x, y0 + 1)
            self.piece("house", ("dado" + e) if e else ("dado_b" if x % 5 == 2 else "dado"), x, y0 + 2)
        for y in range(y0 + 3, y1):
            self.piece("house", "side_W", x0, y)
            self.piece("house", "side_E", x1, y)
            for x in range(x0 + 1, x1):
                if y == y0 + 3:
                    self.piece("house", "shade" if x % 2 else "shade_b", x, y)
                else:
                    self.piece("house", "floor_" + "ABCD"[(x * 3 + y * 5 + x // 3) % 4], x, y)
        for x in range(x0, x1 + 1):
            self.piece("house", "south_W" if x == x0 else ("south_E" if x == x1 else "south"), x, y1)
        self.piece("house", "exit", exit_x, y1)

    def f(self, name, x, y):
        self.piece("furniture", name, x, y)

    def run(self, key, names, x, y):
        for i, n in enumerate(names):
            self.piece(key, n, x + i, y)

    def tall(self, top, bottom, x, y):
        self.f(top, x, y)
        self.f(bottom, x, y + 1)

    def panel(self, name, x, y, w, h):
        self.part("frescoes", name, x, y, w, h)


def _out(m, exit_x, exit_y, dest, warp):
    m.warp(exit_x, exit_y, dest, warp)


# --------------------------------------------------------------------------------------------
def asclepeion(stem):
    """A harbor Asclepeion lit from above: the counter, the honey-salve shelves
    (the healer's basin at its left for the heal), the light well's sunken pool
    where the Panacoil coils, the painted Pithos jar, benches for the waiting."""
    name, P = "KnossaAmnisos_Asclepeion", "KnossaAmnisos_Asclepeion_EventScript_"
    ensure_map(name, 13, 10, "palace_rooms", "MAP_TYPE_INDOOR", "MAPSEC_AMNISOS", "MUS_ICHOR_ASCLEPEION",
               primary="oikos")
    m = Room(name, 13, 10)
    m.shell(0, 12, 0, 9, 6, fields={2: "lilies", 4: "lilies", 8: "lilies", 10: "lilies"})
    m.panel("saffron", 6, 1, 1, 1)
    m.piece("house", "niche", 1, 1)
    m.piece("house", "niche", 11, 1)
    m.part("furniture", "basin_TL", 4, 3, 2, 1)
    m.part("furniture", "basin_BL", 4, 4, 2, 1)
    m.run("furniture", ["table_L", "table_R"], 6, 5)
    m.f("bowl", 8, 5)
    m.tall("pithos_top", "pithos", 11, 3)
    m.part("furniture", "well_TL", 1, 7, 2, 1)
    m.run("furniture", ["bench_L", "bench", "bench_R"], 8, 8)
    m.f("stand", 1, 4)
    m.piece("house", "rug", 6, 7)
    m.piece("house", "rug", 6, 8)
    m.obj("ICHOR_HEALER", 6, 4, P + "Akestor", local_id="LOCALID_AMNISOS_HEALER")
    m.obj("SPECIES(PANACOIL)", 2, 6, P + "Panacoil", "MOVEMENT_TYPE_FACE_RIGHT")
    m.obj("ICHOR_SAILOR", 10, 7, P + "Patient", "MOVEMENT_TYPE_FACE_LEFT")
    m.sign(11, 4, P + "Pithos")
    m.sign(11, 3, P + "Pithos")
    m.sign(1, 7, P + "Pool")
    _out(m, 6, 9, "MAP_KNOSSA_AMNISOS", AMNISOS_WARPS["Asclepeion"])
    return m.build(stem, starts=[(6, 9)], must_reach=[(6, 6, "the counter")], views=[(6, 5)])


def agora(stem):
    """Anthousa's saffron hall: pithoi of oil along the back wall, the loom-weight
    scale, baskets of crocus on the counter, crates of thyme."""
    name, P = "KnossaAmnisos_Agora", "KnossaAmnisos_Agora_EventScript_"
    ensure_map(name, 12, 8, "palace_rooms", "MAP_TYPE_INDOOR", "MAPSEC_AMNISOS", "MUS_ICHOR_AGORA",
               primary="oikos")
    m = Room(name, 12, 8)
    m.shell(0, 11, 0, 7, 5, field="field_red", fields={3: "lilies_red", 8: "lilies_red"})
    m.panel("monkey", 6, 1, 1, 1)
    for x in (1, 2, 9, 10):
        m.tall("pithoi_top", "pithoi", x, 3)
    m.run("furniture", ["table_L", "table_R"], 4, 4)
    m.f("stand", 7, 3)
    m.f("crate", 10, 6)
    m.f("crate", 1, 6)
    m.f("bowl", 6, 4)
    m.obj("ICHOR_MERCHANT", 4, 3, P + "Anthousa", local_id="LOCALID_AMNISOS_CLERK")
    m.obj("ICHOR_ELDER_M", 8, 5, P + "Customer", "MOVEMENT_TYPE_FACE_LEFT")
    _out(m, 5, 7, "MAP_KNOSSA_AMNISOS", AMNISOS_WARPS["Agora"])
    return m.build(stem, starts=[(5, 7)], must_reach=[(4, 5, "the counter")], views=[(5, 4)])


def kydons_house(stem):
    """A narrow house whose back wall is the hillside: hive tubes in the rock
    (niches), the wax press and its drip tray, the folded awning, the gulls' perch."""
    name, P = "KnossaAmnisos_KydonsHouse", "KnossaAmnisos_KydonsHouse_EventScript_"
    ensure_map(name, 9, 8, "palace_rooms", "MAP_TYPE_INDOOR", "MAPSEC_AMNISOS", "MUS_ICHOR_AKTI",
               primary="oikos")
    m = Room(name, 9, 8)
    m.shell(0, 8, 0, 7, 4, fields={1: "niche", 2: "corbel", 3: "niche", 5: "niche", 6: "corbel", 7: "niche"})
    m.f("crate", 6, 3)
    m.f("bowl", 7, 3)
    m.f("banner", 1, 3)
    m.f("bedroll", 1, 5)
    m.f("stand", 7, 5)
    m.f("chest", 7, 6)
    m.tall("pithos_top", "pithos", 2, 3)
    m.obj("ICHOR_MERCHANT", 4, 4, P + "Kydon", "MOVEMENT_TYPE_FACE_DOWN", local_id="LOCALID_AMNISOS_KYDON")
    m.sign(6, 3, P + "WaxPress")
    _out(m, 4, 7, "MAP_KNOSSA_AMNISOS", AMNISOS_WARPS["KydonsHouse"])
    return m.build(stem, starts=[(4, 7)], views=[(4, 4)])


def tavern(stem):
    """The Double Axe: a long low room, a rack of bulls' horns over the door, a
    long bench under half-flaked dolphins, the gypsum knucklebones table."""
    name, P = "KnossaAmnisos_Tavern", "KnossaAmnisos_Tavern_EventScript_"
    ensure_map(name, 14, 8, "palace_rooms", "MAP_TYPE_INDOOR", "MAPSEC_AMNISOS", "MUS_ICHOR_AGORA",
               primary="oikos")
    m = Room(name, 14, 8)
    m.shell(0, 13, 0, 7, 7)
    m.panel("dolphins_TL", 8, 0, 3, 2)
    m.piece("furniture", "wall_spears", 3, 1)
    m.piece("house", "lamp", 5, 1)
    m.run("furniture", ["bench_L", "bench", "bench", "bench_R"], 1, 3)
    m.run("furniture", ["table_L", "table_R"], 6, 4)
    m.f("brazier", 12, 3)
    m.tall("pithoi_top", "pithoi", 12, 5)
    m.f("crate", 1, 6)
    m.piece("house", "rug", 7, 5)
    m.piece("house", "rug", 7, 6)
    m.obj("ICHOR_ELDER_M", 6, 3, P + "Lykastos", local_id="LOCALID_AMNISOS_LYKASTOS")
    m.obj("ICHOR_WOMAN", 9, 4, P + "Kressa", "MOVEMENT_TYPE_FACE_LEFT", local_id="LOCALID_AMNISOS_KRESSA")
    m.obj("ICHOR_YOUTH_M", 10, 6, P + "Dorion", "MOVEMENT_TYPE_FACE_UP", local_id="LOCALID_AMNISOS_DORION")
    _out(m, 7, 7, "MAP_KNOSSA_AMNISOS", AMNISOS_WARPS["Tavern"])
    return m.build(stem, starts=[(7, 7)], must_reach=[(6, 5, "the bones table")], views=[(7, 4)])


def xenia_house(stem):
    """Aithon's courtyard house: the lustral basin with steps down, guest couches,
    a ship painted on the wall, a table set for more than live here, the lamp."""
    name, P = "KnossaAmnisos_XeniaHouse", "KnossaAmnisos_XeniaHouse_EventScript_"
    ensure_map(name, 12, 9, "palace_rooms", "MAP_TYPE_INDOOR", "MAPSEC_AMNISOS", "MUS_ICHOR_AKTI",
               primary="oikos")
    m = Room(name, 12, 9)
    m.shell(0, 11, 0, 8, 6, field="field")
    m.panel("dolphins_TL", 6, 0, 3, 2)
    m.piece("house", "lamp", 2, 1)
    m.part("furniture", "basin_TL", 1, 4, 2, 1)
    m.part("furniture", "basin_BL", 1, 5, 2, 1)
    m.run("furniture", ["bench_L", "bench", "bench_R"], 8, 3)
    m.run("furniture", ["table_L", "table_R"], 5, 5)
    m.f("bowl", 7, 5)
    m.f("bed_top", 10, 5)
    m.f("bed", 10, 6)
    m.obj("ICHOR_ELDER_M", 5, 4, P + "Aithon", local_id="LOCALID_AMNISOS_AITHON")
    _out(m, 6, 8, "MAP_KNOSSA_AMNISOS", AMNISOS_WARPS["XeniaHouse"])
    return m.build(stem, starts=[(6, 8)], views=[(6, 4)])


def leapers_house(stem):
    """Euanthe's two rooms in one: the shelf of little bronze bulls, a prize a
    summer; the splint and linen on a peg; the loom in the back with the cat."""
    name, P = "KnossaAmnisos_LeapersHouse", "KnossaAmnisos_LeapersHouse_EventScript_"
    ensure_map(name, 11, 8, "palace_rooms", "MAP_TYPE_INDOOR", "MAPSEC_AMNISOS", "MUS_ICHOR_AKTI",
               primary="oikos")
    m = Room(name, 11, 8)
    m.shell(0, 10, 0, 7, 5, field="field_red")
    m.panel("griffin_TL", 7, 0, 2, 2)
    m.piece("furniture", "banner", 2, 1)
    m.f("stand", 3, 3)
    m.f("stand", 4, 3)
    m.piece("furniture", "wall_spears", 5, 1)
    m.f("loom", 8, 3)
    m.f("bedroll", 9, 5)
    m.f("chest", 1, 3)
    m.piece("house", "rug", 5, 5)
    m.piece("house", "rug", 5, 6)
    m.f("bowl", 1, 6)
    m.obj("ICHOR_ELDER_F", 4, 5, P + "Euanthe", local_id="LOCALID_AMNISOS_EUANTHE")
    m.obj("SPECIES(GELASABLE)", 8, 4, P + "Cat", "MOVEMENT_TYPE_FACE_DOWN")
    m.sign(3, 3, P + "Bulls")
    m.sign(4, 3, P + "Bulls")
    _out(m, 5, 7, "MAP_KNOSSA_AMNISOS", AMNISOS_WARPS["LeapersHouse"])
    return m.build(stem, starts=[(5, 7)], views=[(5, 4)])


def fishers_hut(stem):
    """Polypos's hut under an upturned hull: octopus pots stacked by the door,
    two octopuses drying, the bean pot always on the fire."""
    name, P = "KnossaAmnisos_FishersHut", "KnossaAmnisos_FishersHut_EventScript_"
    ensure_map(name, 8, 7, "palace_rooms", "MAP_TYPE_INDOOR", "MAPSEC_AMNISOS", "MUS_ICHOR_AKTI",
               primary="oikos")
    m = Room(name, 8, 7)
    m.shell(0, 7, 0, 6, 2, fields={4: "corbel", 5: "corbel"})
    m.f("crate", 1, 3)
    m.f("crate", 1, 4)
    m.f("brazier", 6, 3)
    m.f("bedroll", 6, 5)
    m.f("spears", 5, 3)
    m.f("bowl", 1, 5)
    m.obj("ICHOR_FISHER", 4, 3, P + "Polypos", local_id="LOCALID_AMNISOS_POLYPOS")
    m.sign(6, 3, P + "BeanPot")
    _out(m, 2, 6, "MAP_KNOSSA_AMNISOS", AMNISOS_WARPS["FishersHut"])
    return m.build(stem, starts=[(2, 6)], views=[(3, 3)])


def bull_road_hut(stem):
    """Bombylia's round hut over a spring: the stone basin in the floor where the
    spring rises, skeps on shelves, the smoker, the narrow cot."""
    name, P = "KnossaBullRoad_Hut", "KnossaBullRoad_Hut_EventScript_"
    ensure_map(name, 9, 7, "palace_rooms", "MAP_TYPE_INDOOR", "MAPSEC_BULL_ROAD", "MUS_ICHOR_AKTI",
               primary="oikos")
    m = Room(name, 9, 7)
    m.shell(0, 8, 0, 6, 4, fields={2: "niche", 6: "niche"})
    m.part("furniture", "basin_TL", 3, 3, 2, 1)
    m.part("furniture", "basin_BL", 3, 4, 2, 1)
    m.tall("pithoi_top", "pithoi", 1, 3)
    m.f("bed_top", 7, 3)
    m.f("bed", 7, 4)
    m.f("brazier", 1, 5)
    m.f("chest", 7, 5)
    m.f("stand", 6, 3)
    m.obj("ICHOR_ELDER_F", 5, 3, P + "Bombylia", local_id="LOCALID_HUT_BOMBYLIA")
    m.sign(3, 4, P + "Spring")
    m.sign(4, 4, P + "Spring")
    _out(m, 4, 6, "MAP_KNOSSA_BULL_ROAD", 0)
    return m.build(stem, starts=[(4, 6)], views=[(4, 3)])


def throne_room(stem):
    """The Throne Room: the gypsum throne against the north wall between its
    wingless griffins in lilies, the benches of the council either side, the
    porphyry bowl, the lustral basin, the way out to the court."""
    name, P = "KnossaPalace_ThroneRoom", "KnossaPalace_ThroneRoom_EventScript_"
    ensure_map(name, 13, 9, "palace_rooms", "MAP_TYPE_INDOOR", "MAPSEC_PALACE_OF_MINOS", "MUS_ICHOR_TEMPLE",
               primary="oikos")
    m = Room(name, 13, 9)
    m.shell(0, 12, 0, 8, 6, field="field_red")
    m.panel("griffin_TL", 3, 0, 2, 2)
    m.panel("griffin2_TL", 8, 0, 2, 2)
    m.f("throne_back", 6, 2)
    m.f("throne", 6, 3)
    m.run("furniture", ["bench_L", "bench", "bench", "bench_R"], 1, 3)
    m.run("furniture", ["bench_L", "bench", "bench", "bench_R"], 8, 3)
    m.f("bowl", 9, 5)
    m.part("furniture", "basin_TL", 1, 5, 2, 1)
    m.part("furniture", "basin_BL", 1, 6, 2, 1)
    m.piece("house", "rug", 6, 6)
    m.piece("house", "rug", 6, 7)
    m.f("stand", 11, 5)
    m.obj("ICHOR_ARIADNE", 5, 4, P + "Ariadne", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_HIDE_ARIADNE_THRONE", local_id="LOCALID_THRONE_ARIADNE")
    m.obj("ICHOR_TITAN_GRUNT", 5, 7, P + "Guard", "MOVEMENT_TYPE_FACE_RIGHT",
          flag="FLAG_ICHOR_HIDE_PALACE_GRUNTS", local_id="LOCALID_THRONE_GUARD_1")
    m.obj("ICHOR_TITAN_GRUNT", 7, 7, P + "Guard", "MOVEMENT_TYPE_FACE_LEFT",
          flag="FLAG_ICHOR_HIDE_PALACE_GRUNTS", local_id="LOCALID_THRONE_GUARD_2")
    m.hidden(2, 3, "ITEM_RELIC_SILVER", "FLAG_ICHOR_HIDDEN_ITEM_PALACE_SILVER_OWL")
    m.sign(6, 3, P + "Throne")
    _out(m, 6, 8, "MAP_KNOSSA_PALACE", PALACE_WARPS["ThroneRoom"])
    return m.build(stem, starts=[(6, 8)], must_reach=[(5, 5, "Ariadne")], views=[(6, 4)])


def west_magazines(stem):
    """The West Magazines: long rows of pithoi taller than you down narrow aisles,
    and the Titans' camp among them: bedrolls, a brazier, their shovels."""
    name, P = "KnossaPalace_WestMagazines", "KnossaPalace_WestMagazines_EventScript_"
    ensure_map(name, 15, 11, "palace_rooms", "MAP_TYPE_INDOOR", "MAPSEC_PALACE_OF_MINOS", "MUS_ICHOR_TITAN",
               primary="oikos")
    m = Room(name, 15, 11)
    m.shell(0, 14, 0, 10, 11, fields={3: "niche", 7: "niche"})
    m.piece("furniture", "banner", 5, 1)
    m.piece("furniture", "wall_spears", 9, 1)
    m.panel("monkey", 12, 1, 1, 1)
    for x in (1, 2, 4, 5):
        m.tall("pithoi_top", "pithoi", x, 3)
        m.tall("pithoi_top", "pithoi", x, 6)
    for x in (12, 13):
        m.tall("pithoi_top", "pithoi", x, 3)
    m.tall("pithos_top", "pithos", 13, 6)
    m.f("cist_open", 12, 8)
    m.f("bedroll", 8, 4)
    m.f("bedroll", 9, 5)
    m.f("brazier", 8, 7)
    m.f("crate", 1, 9)
    m.f("spears", 13, 9)
    m.obj("ICHOR_TITAN_GRUNT", 7, 4, P + "Grunt1", "MOVEMENT_TYPE_FACE_RIGHT", flag="FLAG_ICHOR_HIDE_PALACE_GRUNTS")
    m.obj("ICHOR_TITAN_GRUNT", 10, 4, P + "Grunt2", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_ICHOR_HIDE_PALACE_GRUNTS")
    m.obj("ICHOR_TITAN_GRUNT", 9, 7, P + "Grunt3", "MOVEMENT_TYPE_FACE_LEFT", flag="FLAG_ICHOR_HIDE_PALACE_GRUNTS")
    m.obj("ICHOR_TITAN_GRUNT", 3, 9, P + "Doubter", "MOVEMENT_TYPE_FACE_RIGHT", flag="FLAG_ICHOR_HIDE_PALACE_GRUNTS")
    m.item_ball(11, 8, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_PALACE_HYPER_POTION")
    m.sign(12, 8, P + "OpenPithos")
    _out(m, 11, 10, "MAP_KNOSSA_PALACE", PALACE_WARPS["WestMagazines"])
    return m.build(stem, starts=[(11, 10)], must_reach=[(11, 9, "the open pithos")], views=[(7, 5)])


def queens_megaron(stem):
    """The Queen's Megaron, Ariadne's rooms: the dolphin fresco, the saffron
    gatherer, her bed and bath, a loom, a light well over the pool."""
    name, P = "KnossaPalace_QueensMegaron", "KnossaPalace_QueensMegaron_EventScript_"
    ensure_map(name, 12, 10, "palace_rooms", "MAP_TYPE_INDOOR", "MAPSEC_PALACE_OF_MINOS", "MUS_ICHOR_TEMPLE",
               primary="oikos")
    m = Room(name, 12, 10)
    m.shell(0, 11, 0, 9, 6)
    m.panel("dolphins_TL", 2, 0, 3, 2)
    m.panel("saffron", 8, 1, 1, 1)
    m.piece("house", "lamp", 6, 1)
    m.f("bath", 1, 3)
    m.f("loom", 6, 3)
    m.f("bed_top", 9, 3)
    m.f("bed", 9, 4)
    m.f("chest", 10, 3)
    m.part("furniture", "well_TL", 2, 6, 2, 1)
    m.f("stand", 10, 7)
    m.piece("house", "rug", 6, 6)
    m.piece("house", "rug", 6, 7)
    m.obj("ICHOR_ALETHEA", 3, 3, P + "Alethea", "MOVEMENT_TYPE_FACE_UP",
          flag="FLAG_ICHOR_HIDE_ALETHEA_MEGARON", local_id="LOCALID_MEGARON_ALETHEA")
    m.sign(2, 2, P + "Dolphins")
    m.sign(3, 2, P + "Dolphins")
    m.sign(8, 2, P + "Leaper")
    _out(m, 6, 9, "MAP_KNOSSA_PALACE", PALACE_WARPS["QueensMegaron"])
    return m.build(stem, starts=[(6, 9)], must_reach=[(3, 4, "Alethea")], views=[(6, 5)])


def grand_staircase(stem):
    """The Grand Staircase: a flight going down under its balustrade into the
    dark, a light well beside it; below the dressed gypsum, the stair's last
    steps are cut into the living rock (LABYRINTH_MAZE.md §1)."""
    name, P = "KnossaPalace_GrandStaircase", "KnossaPalace_GrandStaircase_EventScript_"
    ensure_map(name, 11, 10, "palace_rooms", "MAP_TYPE_INDOOR", "MAPSEC_PALACE_OF_MINOS", "MUS_ICHOR_TEMPLE",
               primary="oikos")
    m = Room(name, 11, 10)
    m.shell(0, 10, 0, 9, 5)
    m.panel("monkey", 8, 1, 1, 1)
    for y, row in ((3, "deep"), (4, "flight"), (5, "flight"), (6, "head")):
        m.run("staircase", [row + "_L", row, row + "_R"], 1, y)
        m.piece("staircase", "balustrade_col" if y in (4, 6) else "balustrade", 4, y)
    m.piece("staircase", "dark", 2, 2)
    m.part("furniture", "well_TL", 6, 4, 2, 1)
    m.f("brazier", 9, 3)
    m.obj("ICHOR_ARIADNE", 6, 6, P + "Ariadne", "MOVEMENT_TYPE_FACE_DOWN",
          flag="FLAG_ICHOR_HIDE_ARIADNE_STAIR", local_id="LOCALID_STAIR_ARIADNE")
    m.sign(6, 4, P + "LightWell")
    m.sign(7, 4, P + "LightWell")
    m.coords.append({"type": "trigger", "x": 2, "y": 3, "elevation": 3, "var": "VAR_TEMP_0",
                     "var_value": "0", "script": P + "StairDown"})
    _out(m, 5, 9, "MAP_KNOSSA_PALACE", PALACE_WARPS["GrandStaircase"])
    # warp 1, the dark at the stair's foot: Ring I's way back up lands here. The
    # trigger on the step below (2,3) checks for the Thread before you reach it.
    m.warp(2, 2, "MAP_LABYRINTH_RING1", 0)
    return m.build(stem, starts=[(5, 9)], must_reach=[(2, 3, "the stair down")], views=[(5, 5)])


ROOMS = {f.__name__: f for f in (asclepeion, agora, kydons_house, tavern, xenia_house, leapers_house,
                                 fishers_hut, bull_road_hut, throne_room, west_magazines, queens_megaron,
                                 grand_staircase)}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--pass", dest="n", default="1")
    a = ap.parse_args()
    for n in a.names or ROOMS:
        ROOMS[n](f"knossa_room_{n}_pass{a.n}")
