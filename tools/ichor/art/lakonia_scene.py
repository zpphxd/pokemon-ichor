#!/usr/bin/env python3
"""Mock scenes for the Lakonia-family tilesets, rendered with render_map.py.

These are review scenes, not maps: they show how each kit's pieces fit
together. Pieces are placed by key and name from build/<dir>/catalog.json
(run lakonia_build.py first), exactly as a map builder would place them, and
soft ground takes its shape keys from blob_key.

Usage: /usr/bin/python3 tools/ichor/art/lakonia_scene.py [scene ...]
Scenes: agoge (a 240x160 screen of the agoge's yard, the ring, Taygetos
behind), town (the agora and the river), quay (a 240x160 screen of Gytheion's
quay), gytheion, boardwalk (a 240x160 screen of Lake Stymphalia's boardwalk
through the reeds), stymphalia, eurotas (Route 25 at Amyklai), hills (Route
27), platanistas (Route 26).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kythera_lib as K  # noqa: E402
from kythera_scene import (GRASS, PATH, SAND, SEA, SHALLOW, TALL, PATCH, STELE,  # noqa: E402,F401
                           HERM, ASCLEPEION, AGORA, Scene)

ROOT = K.ROOT
IMG = ROOT / "design/phase4/img"


class LScene(Scene):
    """kythera_scene.Scene with Lakonia's helpers."""

    def region(self, key, rows, ox, oy, ch="#"):
        """Lay a soft-edged autotile from a mask of `ch` cells."""
        self.blob(key, rows, ox, oy, ch=ch)

    def mass(self, x0, y0, x1, y1, key="taygetos"):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if self.ok(x, y):
                    self.piece(key, f"mass_{x % 2}{y % 2}", x, y)

    def wall_run(self, x0, x1, y, key="taygetos", variants=True, faces=1):
        """A south-facing rock wall: lip row y, `faces` rows of face, then the foot."""
        for x in range(x0, x1 + 1):
            b = "_b" if variants and x % 2 else ""
            self.piece(key, "lip" + b, x, y)
            for f in range(faces):
                self.piece(key, "face" + b, x, y + 1 + f)
            self.piece(key, "foot" + b, x, y + 1 + faces)

    def plane(self, x, y, key="plane"):
        self.put(key, x, y)

    def river_v(self, x0, x1, y0, y1, key="river"):
        """A north-south river between columns x0..x1 (inclusive)."""
        rows = []
        for y in range(y0, y1 + 1):
            rows.append("".join("#" if x0 <= x <= x1 else "." for x in range(self.W)))
        self.region(key, rows, 0, y0)


# --------------------------------------------------------------------------
# lakonia: the agoge's yard (240 x 160) and the town
# --------------------------------------------------------------------------

def agoge():
    s = LScene("lakonia", 15, 10)
    s.wall_run(0, 14, 0, faces=2)
    s.piece("taygetos", "pine_face", 4, 2)
    s.piece("taygetos", "pine_face", 11, 1)
    # the yard: beaten sand from below the mountain's foot
    yard = ["...............",
            "...............",
            "...............",
            "...............",
            "##############.",
            "###############",
            "###############",
            "....###########",
            "....###########",
            "....###########"]
    s.region("yard", yard, 0, 0)
    # the barracks, west; the ring, east, cut by the screen's bottom edge
    s.front("barracks", 0, 4)
    s.put("ring", 6, 4)
    s.plane(0, 7)
    return s


def town():
    W, H = 40, 30
    s = LScene("lakonia", W, H)
    # Taygetos: its flank down the west edge, its south face behind the agoge
    s.mass(0, 0, 2, H - 1)
    for y in range(1, H):
        s.piece("taygetos", "side_E", 3, y)
    s.mass(3, 0, 22, 0)
    s.wall_run(4, 22, 1, faces=1)
    s.piece("taygetos", "pine_face", 9, 2)
    s.piece("taygetos", "pine_face", 17, 2)
    s.piece("taygetos", "in_E", 3, 1)
    for y in (2, 3):
        s.piece("taygetos", "side_E", 3, y)
    # the agoge: its yard, barracks and ring; the training fields
    yard = ["." * W] * 4 + [
        "....####################................",
        "....####################................",
        "....####################................",
        "....###################.................",
        "....###################.................",
        "....###################.................",
        "......################..................",
        "........#############...................",
        "..........##########....................",
    ]
    s.region("yard", yard, 0, 0)
    s.front("barracks", 4, 4)
    s.put("ring", 12, 4)
    s.plane(5, 8)
    s.rect(4, 12, 9, 15, TALL)
    s.rect(4, 11, 7, 11, TALL)
    s.put("sown", 5, 13)
    # the palaestra: its porch on the wrestling sands
    s.put("colonnade", 12, 14)
    for j, row in enumerate((("TL", "T", "T", "T", "TR"), ("L", "C", "C_b", "C", "R"),
                             ("BL", "B", "B", "B", "BR"))):
        for i, nm in enumerate(row):
            s.piece("sands", nm, 12 + i, 17 + j)
    # the agora: Lesche, syssition, the stoa, Enyalios, paving
    s.path_patch(21, 15, 33, 22)
    s.path_patch(24, 23, 26, H - 1)
    s.front("syssition", 22, 5)
    s.front("lesche", 21, 11)
    s.put("stoa", 26, 9)
    s.put("enyalios", 27, 17)
    s.put("rope", 24, 27)
    s.m[27, 23] = STELE
    # houses round their yards
    village = ["." * W] * 20 + [
        "....#######.............................",
        "....#########...........................",
        "..............######....................",
        "..............######.......#######......",
        "...........................########.....",
        "........................................",
    ] + ["." * W] * 4
    s.region("yard", village, 0, 0)
    s.put("well", 11, 21)
    s.front("lampito", 4, 17)
    s.put("burial", 8, 18)
    s.front("house", 4, 22)
    s.front("house_wide", 8, 22)
    s.front("low_house", 15, 24)
    s.front("house", 28, 24)
    s.front("house_wide", 31, 24)
    s.plane(17, 21)
    s.plane(32, 21)
    # the Eurotas, its bridge east to Route 25, Orthia among willows
    s.river_v(36, 39, 0, H - 1)
    s.piece("bridge", "deck_W", 35, 18)
    for x in (36, 37, 38):
        s.piece("bridge", "deck", x, 18)
    s.piece("bridge", "deck_E", 39, 18)
    s.piece("bridge", "face_W", 35, 19)
    for x in (36, 37, 38):
        s.piece("bridge", "arch", x, 19)
    s.piece("bridge", "face_E", 39, 19)
    s.path_patch(33, 17, 34, 19)
    s.put("orthia", 31, 3)
    s.put("willow", 29, 2)
    s.put("willow", 34, 1)
    s.piece("oleander", "bush", 35, 8)
    s.part("oleander", "thicket_L", 34, 13, 2, 1)
    return s


# --------------------------------------------------------------------------
# gytheion: the quay (240 x 160) and the hamlet
# --------------------------------------------------------------------------

def quay():
    s = LScene("gytheion", 15, 10, fill=PATH)
    # behind the dye-works, the shell heaps on the hillside grass
    s.rect(0, 0, 14, 0, GRASS)
    s.put("quayside", 0, 0, cells=[(0, 1), (1, 1), (0, 2), (1, 2)])
    s.part("quayside", "heap_TL", 0, 0, 2, 2)
    s.piece("quayside", "heap_small", 2, 0)
    s.front("house", 11, 0)
    s.piece("quayside", "shells", 2, 1)
    s.put("dyeworks", 3, 1)
    s.piece("vats", "vat", 8, 2)
    s.piece("vats", "skein_rack", 9, 2)
    s.piece("vats", "vat_b", 2, 3)
    # the quay: stains spreading from the dye-works to the steps
    for (x, y, nm) in ((4, 3, "stain"), (5, 4, "stain_b"), (6, 5, "stain"), (3, 5, "shells")):
        s.piece("quayside", nm, x, y)
    s.put("stall", 10, 3)
    s.piece("vats", "nets_L", 13, 3)
    s.piece("vats", "nets_R", 14, 3)
    s.piece("quayside", "basket", 9, 4)
    s.piece("quayside", "bucket", 8, 6)
    s.piece("quayside", "mooring", 11, 6)
    # the quay's edge, the purple steps, the sea and a boat
    for x in range(15):
        s.piece("quay", "S" if x % 4 else "S_b", x, 7)
    s.piece("quay", "ring_S", 11, 7)
    s.piece("quayside", "steps_SL", 6, 7)
    s.piece("quayside", "steps_SR", 7, 7)
    s.piece("quayside", "stain_b", 6, 6)
    s.piece("quayside", "stain", 7, 6)
    s.piece("quayside", "amphorae", 1, 4)
    s.piece("quayside", "mooring", 2, 6)
    s.rect(0, 8, 14, 9, SEA)
    s.put("kaiki", 9, 8, cells=[(i, j) for i in range(3) for j in range(2)])
    return s


def gytheion():
    W, H = 36, 26
    s = LScene("gytheion", W, H, fill=GRASS)
    # the hill and the theater, its stage-building facing the town
    s.put("theater", 3, 1)
    s.put("skene", 3, 5)
    s.front("house", 11, 4)
    s.front("low_house", 15, 5)
    s.front("house", 20, 3)
    s.path_patch(0, 7, 27, 15)
    s.put("dyeworks", 18, 8)
    s.put("quayside", 22, 6, cells=[(0, 1), (1, 1), (0, 2), (1, 2)])
    s.part("quayside", "heap_TL", 23, 6, 2, 2)
    s.piece("vats", "vat", 17, 10)
    s.piece("vats", "vat_b", 23, 10)
    s.put("stall", 7, 9)
    s.piece("vats", "nets_L", 10, 9)
    s.piece("vats", "nets_R", 11, 9)
    for (x, y, nm) in ((19, 11, "stain"), (20, 12, "stain_b"), (21, 13, "stain"), (12, 13, "shells")):
        s.piece("quayside", nm, x, y)
    s.piece("quayside", "bucket", 15, 14)
    # the quay along the south and east, the sea beyond
    for x in range(0, 28):
        s.piece("quay", "S" if x % 5 else "S_b", x, 16)
    s.piece("quay", "out_SE", 27, 16)
    for y in range(7, 16):
        s.piece("quay", "E", 28, y)
    s.piece("quay", "in_SE", 28, 16)
    s.piece("quayside", "steps_SL", 20, 16)
    s.piece("quayside", "steps_SR", 21, 16)
    s.rect(0, 17, W - 1, H - 1, SEA)
    s.rect(29, 0, W - 1, H - 1, SEA)
    s.put("kaiki", 12, 18, cells=[(i, j) for i in range(3) for j in range(2)])
    s.put("kaiki", 30, 9, cells=[(i, j) for i in range(3) for j in range(2)])
    # the shingle beach, stained, and the causeway out to Kranai
    s.rect(0, 20, 9, H - 1, SAND)
    for (x, y) in ((2, 21), (5, 22), (7, 21)):
        s.piece("quayside", "pebbles" if x % 2 else "pebbles_b", x, y)
    for y in range(20, H):
        s.piece("surf", "W", 10, y)
    for x in range(11, 24):
        s.piece("kranai_way", "H" if x % 2 else "H_b", x, 23)
    s.piece("kranai_way", "H_W", 10, 23)
    s.rect(24, 21, 28, 25, SAND)
    s.put("kranai_shrine", 25, 21)
    for y in range(21, 26):
        s.piece("surf", "E", 23, y) if y != 23 else None
    for x in range(24, 29):
        s.piece("surf", "N", x, 20)
    for y in range(21, 26):
        s.piece("surf", "W", 29, y)
    s.put("drowned", 31, 18)
    for x in range(30, 36):
        s.piece("current", "current" if x % 2 else "current_b", x, 2)
    return s


# --------------------------------------------------------------------------
# stymphalia: the boardwalk (240 x 160), the lake, the Platanistas
# --------------------------------------------------------------------------

def boardwalk():
    s = LScene("stymphalia", 15, 10)
    water = ["###############"] * 10
    s.region("marsh", water, 0, 0)
    # reed islets and the curtain behind them
    curtain = ["##########.....",
               "########.......",
               "#####..........",
               "...............",
               "...............",
               "...............",
               "...............",
               "...............",
               "...............",
               "..............."]
    s.region("curtain", curtain, 0, 0)
    reeds = ["...............",
             "...............",
             "...............",
             "..####.........",
             ".######..####..",
             ".######.######.",
             "..####..######.",
             "........#####..",
             "...............",
             "..............."]
    # the forced band: the middle islet's reeds fill the walk's whole width
    reeds = [r if j not in (4, 5, 6) else r[:7] + "#" + r[8:] for j, r in enumerate(reeds)]
    s.region("marsh_reeds", reeds, 0, 0)
    # the boardwalk threading the islets, the causeway from the south
    for y in (3, 7):
        s.piece("boardwalk", "V", 7, y)
    s.piece("boardwalk", "end_N", 7, 2)
    s.piece("boardwalk", "V_sit", 7, 3)
    s.piece("boardwalk", "T_W", 7, 8)
    for x in range(2, 7):
        s.piece("boardwalk", "H", x, 8)
    s.piece("boardwalk", "end_W", 1, 8)
    for y in (9,):
        s.piece("causeway", "V", 7, y)
    s.put("stilt_hut", 10, 0)
    s.piece("boardwalk", "V", 11, 3)
    s.piece("boardwalk", "SW", 11, 4)
    s.piece("marsh", "rock", 13, 8)
    s.piece("marsh", "stump", 4, 2)
    return s


def lake():
    W, H = 34, 24
    s = LScene("stymphalia", W, H)
    water = [("." * 2 + "#" * (W - 4) + "." * 2) if 1 < y < H - 3 else "." * W for y in range(H)]
    water = [list(r) for r in water]
    for y in range(H):
        for x in range(W):
            if (x < 5 and y > 15) or (x > 27 and y < 5):
                water[y][x] = "."
    water = ["".join(r) for r in water]
    s.region("marsh", water, 0, 0)
    roost = ["." * W] * 2 + ["...." + "#" * 14 + "." * (W - 18)] + ["." * W] * (H - 3)
    s.region("curtain", ["." * W, "." * W, "...." + "#" * 14 + "." * (W - 18),
                         "...." + "#" * 13 + "." * (W - 17)] + ["." * W] * (H - 4), 0, 0)
    for x in range(5, 17):
        s.piece("roost", "M" if x % 3 else "M_b", x, 3)
    s.piece("roost", "L", 4, 3)
    s.piece("roost", "R", 17, 3)
    isle = ["." * W] * H
    isle = [list(r) for r in isle]
    for (cx, cy, rx, ry) in ((9, 14, 3, 2), (17, 10, 4, 2), (25, 15, 3, 2)):
        for y in range(H):
            for x in range(W):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.1:
                    isle[y][x] = "#"
    s.region("marsh_reeds", ["".join(r) for r in isle], 0, 0)
    for y in range(18, 21):
        s.piece("causeway", "V", 16, y)
    s.piece("causeway", "V_S", 16, 21)
    for y in range(12, 18):
        s.piece("boardwalk", "V", 16, y)
    s.piece("boardwalk", "T_W", 16, 11)
    for x in range(10, 16):
        s.piece("boardwalk", "H", x, 11)
    s.piece("boardwalk", "NE", 9, 11)
    for y in range(6, 11):
        s.piece("boardwalk", "V", 9, y)
    s.put("stilt_hut", 18, 15)
    for x in range(17, 26):
        s.piece("boardwalk", "H", x, 11) if x > 20 else None
    s.piece("boardwalk", "end_E", 26, 11)
    for x in range(27, 32):
        s.piece("regrow", "wall" if x % 2 else "wall_b", x, 19)
    s.piece("regrow", "cut", 29, 19)
    s.piece("marsh", "rock", 22, 7)
    s.piece("marsh", "stump", 6, 8)
    return s


def platanistas():
    W, H = 26, 18
    s = LScene("stymphalia", W, H)
    moat = [list("." * W) for _ in range(H)]
    for y in range(H):
        for x in range(W):
            r = ((x - 12.5) / 9.5) ** 2 + ((y - 8.5) / 6.5) ** 2
            if 0.55 <= r <= 1.0:
                moat[y][x] = "#"
    s.region("river", ["".join(r) for r in moat], 0, 0)
    for (x, y) in ((8, 5), (14, 4), (10, 8), (15, 9)):
        s.plane(x, y)
    for y in range(1, 4):
        s.piece("bridge", "foot_V", 12, y)
    s.piece("bridge", "foot_V_N", 12, 1)
    s.piece("bridge", "foot_V_S", 12, 3)
    for y in range(13, 17):
        s.piece("bridge", "foot_V", 12, y)
    s.piece("bridge", "foot_V_S", 12, 16)
    s.part("statues", "herakles", 13, 0, 1, 2)
    s.part("statues", "lykourgos", 11, 16, 1, 2)
    s.put("trees", 20, 13, cells=[(0, 0), (1, 0), (0, 1), (1, 1)])
    s.put("trees", 22, 1, cells=[(i, j) for i in range(2, 4) for j in range(3)])
    s.put("phoibaion", 2, 14)
    return s


# --------------------------------------------------------------------------
# eurotas: Route 25 at Amyklai
# --------------------------------------------------------------------------

def eurotas():
    W, H = 32, 22
    s = LScene("eurotas", W, H)
    # the foot of Taygetos in the north-west, the beehive tomb in it
    s.mass(0, 0, 11, 1)
    s.piece("taygetos", "mass_pine", 4, 0)
    s.wall_run(0, 10, 2, faces=1)
    s.piece("taygetos", "lip_R", 11, 2)
    s.piece("taygetos", "face_R", 11, 3)
    s.piece("taygetos", "foot_R", 11, 4)
    s.put("vapheio", 3, 3, cells=[(i, j) for i in range(4) for j in range(3)])
    s.piece("taygetos", "boulder", 9, 6)
    s.piece("taygetos", "scree", 1, 5)
    # the road north through the plain
    s.path_patch(17, 0, 19, H - 1)
    # Amyklai on its low hill: the throne on the tomb, the altar, the spring
    s.put("throne", 12, 1)
    s.put("altar", 12, 6, cells=[(0, 0), (1, 0)])
    s.put("spring", 14, 5)
    s.piece("flowers", "hyacinths", 11, 4)
    s.piece("flowers", "hyacinths_b", 15, 4)
    s.piece("flowers", "hyacinths", 11, 5)
    s.m[7, 16] = HERM
    # the farmhouse in the west fields, the herm-shrines on the way to it
    s.rect(0, 12, 9, 21, TALL)
    s.rect(1, 13, 6, 17, GRASS)
    s.put("farmhouse", 1, 13, cells=[(i, j) for i in range(4) for j in range(3)])
    s.path_patch(4, 16, 16, 17)
    s.put("herm_shrine", 10, 14, cells=[(0, 0), (0, 1)])
    s.put("herm_shrine", 14, 14, cells=[(1, 0), (1, 1)])
    # the Eurotas on the east, in reeds and oleander, a plank bridge over a side stream
    river = [("." * 16 + "#" * 16) if y in (17, 18) else ("." * 23 + "#" * 9) for y in range(H)]
    s.region("river", river, 0, 0)
    reeds = ["." * W] * 6 + ["." * 25 + "####" + "..."] + ["." * 24 + "######.."] * 3 + \
        ["." * 25 + "####" + "..."] + ["." * W] * (H - 11)
    s.region("reeds", reeds, 0, 0)
    s.piece("bridge", "foot_V_N", 18, 16)
    s.piece("bridge", "foot_V", 18, 17)
    s.piece("bridge", "foot_V", 18, 18)
    s.piece("bridge", "foot_V_S", 18, 19)
    for (x, y) in ((22, 2), (22, 9), (21, 13)):
        s.piece("oleander", "bush", x, y)
    s.part("oleander", "thicket_L", 21, 5, 2, 1)
    s.piece("river", "rock", 26, 14)
    s.piece("river", "tuft", 27, 3)
    return s


SCENES = {
    "agoge": (agoge, "lakonia_agoge.png", 3),
    "town": (town, "lakonia_town.png", 2),
    "quay": (quay, "gytheion_quay.png", 3),
    "gytheion": (gytheion, "gytheion_town.png", 2),
    "boardwalk": (boardwalk, "stymphalia_boardwalk.png", 3),
    "lake": (lake, "stymphalia_lake.png", 2),
    "platanistas": (platanistas, "stymphalia_platanistas.png", 2),
    "eurotas": (eurotas, "eurotas_amyklai.png", 2),
}
ONE_X = {"agoge", "quay", "boardwalk"}


def main(names):
    IMG.mkdir(parents=True, exist_ok=True)
    for n in names or list(SCENES):
        fn, out, sc = SCENES[n]
        s = fn()
        s.render(IMG / out, scale=sc)
        if n in ONE_X:
            s.render(IMG / out.replace(".png", "_1x.png"), scale=1)


if __name__ == "__main__":
    main(sys.argv[1:])
