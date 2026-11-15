#!/usr/bin/env python3
"""Mock scenes for the Knossa tilesets, rendered with render_map.py.

These are review scenes, not maps: they show how each kit's pieces fit
together. Pieces are placed by key and name from build/<dir>/catalog.json
(run knossa_build.py first), exactly as a map builder would place them.

Usage: /usr/bin/python3 tools/ichor/art/knossa_scene.py [scene ...] [--pass N]
Scenes: amnisos_quay (240x160: the quay, the Titan ships at the mole, hives on
every roof), amnisos_town (the town on its slope), bull_road (240x160: the
terraces, the vineyard and the herd crossing), bull_road_wide, bronze_heel,
palace_court (240x160: the Central Court and the bull-leaping lane),
palace_hill (the palace on its hill from the Bull Road's end), palace_rooms,
ida_path, idaean_cave, eileithyia.
--pass N also writes <name>_passN.png, for the render-and-critique record.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kythera_scene as KS  # noqa: E402
from kythera_scene import (AGORA, ASCLEPEION, CYP_BOT, CYP_TOP, GRASS, OLIVE_BOT,  # noqa: E402,F401
                           OLIVE_TIP, OLIVE_TOP, PATCH, PATH, SAND, SEA, STELE, TALL)

ROOT = KS.ROOT
IMG = ROOT / "design/phase4/img"
LEDGE = KS.LEDGE


class Scene(KS.Scene):
    def __init__(self, tileset, w, h, fill=GRASS, primary="aethos"):
        super().__init__(tileset, w, h, fill)
        self.primary = primary
        self.sprites = []

    def sprite(self, mon, frame, x, y, flip=False):
        """Stand a Pokémon's overworld sprite (32 x 32, frames: 0-1 down, 2-3
        up, 4-5 left) on cell (x, y), as the map's objects would."""
        self.sprites.append((mon, frame, x, y, flip))

    def render(self, out, scale=2):
        blk = ROOT / f"build/{self.dir}/scene.bin"
        blk.parent.mkdir(parents=True, exist_ok=True)
        self.m.astype("<u2").tofile(blk)
        subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata",
                        str(blk), "--width", str(self.W), "--primary", self.primary,
                        "--secondary", self.symbol, "--scale", str(scale), "-o", str(out)],
                       check=True)
        if self.sprites:
            from PIL import Image
            img = Image.open(out).convert("RGB")
            for (mon, frame, x, y, flip) in self.sprites:
                src = Image.open(ROOT / f"graphics/pokemon/{mon}/overworld.png")
                fr = src.crop((frame * 32, 0, frame * 32 + 32, 32))
                a = np.array(fr)
                rgba = np.array(fr.convert("RGBA"))
                rgba[..., 3] = np.where(a == 0, 0, 255)
                sp = Image.fromarray(rgba, "RGBA")
                if flip:
                    sp = sp.transpose(Image.FLIP_LEFT_RIGHT)
                sp = sp.resize((32 * scale, 32 * scale), Image.NEAREST)
                img.paste(sp, ((x * 16 - 8) * scale, (y * 16 - 16) * scale), sp)
            img.save(out)
        print(Path(out).relative_to(ROOT))

    def front(self, key, x, y):
        for j, row in enumerate(self.fronts[key]["ids"]):
            for i, mid in enumerate(row):
                if mid is not None and self.ok(x + i, y + j):
                    self.m[y + j, x + i] = mid

    def block(self, rows, x, y):
        for j, row in enumerate(rows):
            for i, mid in enumerate(row):
                if mid is not None and self.ok(x + i, y + j):
                    self.m[y + j, x + i] = mid

    def run(self, key, names, x0, y):
        """Lay a west-east run: names[0] at x0, then names[1:] in turn."""
        for i, n in enumerate(names):
            self.piece(key, n, x0 + i, y)

    def wall_run(self, key, x0, x1, y, top=True):
        for x in range(x0, x1 + 1):
            n = "L" if x == x0 else ("R" if x == x1 else ("M2" if (x - x0) % 4 == 2 else "M"))
            self.piece(key, n, x, y)
            if top:
                self.piece(key, "top" + ("_L" if n == "L" else "_R" if n == "R" else
                                         "_M2" if n == "M2" else ""), x, y - 1)


# --------------------------------------------------------------------------
# Amnisos
# --------------------------------------------------------------------------

def pave(s, x0, x1, y0, y1):
    """Pave with the quay's flagstones in a staggered mix, a worn slab here and there."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            k = (x * 7 + y * 3) % 11
            n = "worn" if k == 0 else ("A", "B", "C")[(x + 2 * y) % 3]
            s.piece("flags", n, x, y)


def quay_row(s, x0, x1, y, side="N"):
    for x in range(x0, x1 + 1):
        s.piece("quay", side, x, y)


def amnisos_quay():
    """One screen (15 x 10) of Amnisos's quay: a Titan trireme at the mole,
    the Asclepeion and the Agora by the quay, houses with hives behind."""
    s = Scene("amnisos", 15, 10, fill=PATH)
    s.rect(0, 0, 14, 2, SEA)
    s.put("titan_trireme", 7, 0)
    # the quay's sea edge; the mole bends out north-east
    quay_row(s, 0, 14, 3, "N")
    s.piece("quay", "N_plank", 10, 3)
    # flagstones and gear on the quay
    pave(s, 0, 14, 4, 5)
    s.piece("flags", "drain", 13, 5)
    s.piece("flags", "ring", 2, 5)
    s.piece("gear", "amphorae", 1, 4)
    s.piece("gear", "nets", 4, 4)
    s.piece("gear", "bollard", 6, 4)
    s.piece("gear", "rope", 9, 4)
    s.piece("gear", "crate", 14, 4)
    s.piece("shrine", "top", 12, 4)
    s.piece("shrine", "base", 12, 5)
    # the Asclepeion and the Agora face the quay across the lane
    s.block(ASCLEPEION, 0, 6)
    s.front("honey_house", 5, 7)
    s.block(AGORA, 10, 6)
    return s


def amnisos_town():
    """A 30 x 20 stretch of Amnisos: the quay and the mole with the four
    Titan ships, the houses climbing the slope in terraces, the cliff and the
    Cave of Eileithyia's mouth up the goat path, the south gap in the wall."""
    W, H = 30, 22
    s = Scene("amnisos", W, H, fill=GRASS)
    # sea and quay
    s.rect(0, 0, W - 1, 4, SEA)
    s.put("titan_trireme", 13, 0)
    s.put("titan_trireme", 21, 0)
    quay_row(s, 0, 21, 5, "N")
    s.piece("quay", "N_plank", 8, 5)
    pave(s, 0, 21, 6, 7)
    # the mole: out east along the ships, two cells wide
    quay_row(s, 22, 28, 3, "N")
    quay_row(s, 22, 28, 4, "S")
    s.piece("quay", "out_NE", 29, 3)
    s.piece("quay", "out_SE", 29, 4)
    s.piece("quay", "in_SW", 22, 5)
    s.rect(23, 5, 29, 7, SEA)
    s.piece("quay", "S", 22, 6)
    s.rect(22, 6, 22, 7, PATH)
    for x in range(23, 30):
        s.piece("surf", "S", x, 6)
    s.rect(23, 7, 29, 7, SAND)
    s.piece("sand_decor", "sherd_dig", 25, 7)
    s.piece("sand_decor", "shells", 27, 7)
    s.piece("shrine", "top", 21, 6)
    s.piece("shrine", "base", 21, 7)
    s.piece("gear", "amphorae", 2, 6)
    s.piece("gear", "nets", 5, 6)
    s.piece("gear", "bollard", 11, 6)
    # first terrace: Asclepeion and Agora by the quay, a lane between
    s.block(ASCLEPEION, 1, 8)
    s.block(AGORA, 14, 8)
    s.front("tavern", 7, 9)
    s.rect(0, 12, W - 1, 12, PATH)
    s.rect(5, 8, 6, 12, PATH)
    s.rect(12, 8, 13, 12, PATH)
    s.rect(18, 8, 19, 12, PATH)
    s.rect(20, 8, 29, 11, GRASS)
    s.front("fisher_hut", 23, 9)
    s.piece("sand_decor", "footprints", 21, 12)
    # second terrace: a terrace wall, then the houses climbing
    s.wall_run("wall", 0, 10, 14)
    s.piece("wall", "steps", 6, 14)
    s.piece("wall", "top_steps", 6, 13)
    s.wall_run("wall", 14, 20, 14)
    s.piece("wall", "spout", 17, 14)
    s.piece("wall", "top_spout", 17, 13)
    s.rect(11, 13, 13, 14, PATH)
    s.front("xenia_house", 1, 15)
    s.front("leaper_house", 8, 15)
    s.front("honey_house", 15, 15)
    s.rect(0, 18, W - 1, 18, PATH)
    # the cliff at the town's west end, the cave up the goat path
    s.rect(20, 15, 29, 17, GRASS)
    s.piece("cliff", "lip_L", 21, 14)
    for x in range(22, 29):
        s.piece("cliff", "lip", x, 14)
    s.piece("cliff", "lip_R", 29, 14)
    for y in (15, 16):
        s.piece("cliff", "face_L", 21, y)
        for x in range(22, 29):
            s.piece("cliff", "face" if x % 3 else "face_b", x, y)
        s.piece("cliff", "face_R", 29, y)
    s.put("cave_mouth", 23, 14)
    s.piece("cliff", "foot_grass", 22, 17)
    s.piece("cliff", "foot_grass", 28, 17)
    # the south gap in the town wall, a sign beside it
    s.wall_run("wall", 0, 12, 20)
    s.wall_run("wall", 16, 29, 20)
    s.rect(13, 19, 15, 21, PATH)
    s.m[19, 16] = STELE
    for (x, y) in ((0, 21), (4, 21), (20, 21), (26, 21)):
        s.olive(x, y) if y + 1 < H else None
    s.cypress(19, 16)
    s.cypress(21, 16)
    return s


# --------------------------------------------------------------------------
# The Bull Road
# --------------------------------------------------------------------------

def brow_run(s, x0, x1, y, stairs=()):
    for x in range(x0, x1 + 1):
        n = "L" if x == x0 else ("R" if x == x1 else ("M2" if (x - x0) % 3 == 2 else "M"))
        s.piece("brow", "stair" if x in stairs else n, x, y)


def vine_patch(s, x0, y0, w, h, grapes=(), dig=None):
    for j in range(h):
        for i in range(w):
            v = "N" if j == 0 else ("S" if j == h - 1 else "")
            hh = "W" if i == 0 else ("E" if i == w - 1 else "")
            n = (v + hh) or ("C_b" if (i + j) % 3 == 1 else "C")
            if (i, j) in grapes:
                n = "C_grapes"
            if dig == (i, j):
                n = "C_dig"
            s.piece("vines", n, x0 + i, y0 + j)


def vine_row(s, x0, x1, y):
    for x in range(x0, x1 + 1):
        n = "row_L" if x == x0 else ("row_R" if x == x1 else
                                     ("row_grapes" if (x - x0) % 3 == 1 else
                                      ("row_post" if (x - x0) % 3 == 2 else "row")))
        s.piece("vines", n, x, y)


def bull_road():
    """One screen (15 x 10) of the Bull Road: the vineyard's rows, a terrace
    brow to hop down toward Amnisos, the palace herd crossing the road, the
    first forced grass band."""
    s = Scene("bull_road", 15, 10)
    s.path_patch(6, 0, 8, 9)
    vine_row(s, 0, 4, 0)
    vine_patch(s, 0, 1, 5, 2, grapes={(2, 0)})
    s.olive(10, 0)
    s.olive(12, 1)
    s.cypress(14, 0)
    s.piece("phrygana", "thyme", 9, 2)
    brow_run(s, 0, 14, 3, stairs=(7,))
    s.piece("phrygana", "thyme", 1, 5)
    s.piece("phrygana", "asphodel", 13, 4)
    s.piece("phrygana", "sage", 0, 6)
    s.piece("phrygana", "burnet", 14, 6)
    s.piece("phrygana", "thyme_b", 11, 6)
    s.m[4, 5] = STELE
    # the first forced grass band, walled by olives
    s.rect(2, 7, 12, 9, TALL)
    s.olive(0, 8)
    s.olive(13, 8)
    # the palace herd crossing
    s.sprite("tauros", 5, 3, 5, flip=True)
    s.sprite("tauros", 4, 10, 4)
    s.sprite("tauros", 0, 12, 6)
    return s


def bull_road_wide():
    """A 30 x 22 stretch: the fork and the great herm, the way east to the
    Bronze Heel, the cutting with the labrys door in its east cliff, the
    beekeeper's hut and its spring, Ida's gate, the vineyard."""
    W, H = 30, 22
    s = Scene("bull_road", W, H)
    s.path_patch(12, 0, 14, H - 1)
    # north: a brow, the vineyard to the west with its sign, olives east
    brow_run(s, 0, 11, 2)
    brow_run(s, 15, 29, 2)
    s.piece("brow", "stair", 13, 2)
    s.piece("brow", "M", 12, 2)
    s.piece("brow", "M", 14, 2)
    vine_row(s, 1, 9, 0)
    vine_patch(s, 1, 1, 9, 1) if False else None
    for x in range(1, 10):
        s.piece("vines", "S" if 1 < x < 9 else ("SW" if x == 1 else "SE"), x, 1)
    s.piece("vines", "sign", 10, 1)
    for x in (17, 21, 25):
        s.olive(x, 0)
    # the fork: the herm, the road east to the Bronze Heel
    s.path_patch(15, 6, 29, 7)
    s.put("herm", 15, 4)
    s.piece("phrygana", "thyme", 17, 4)
    s.piece("phrygana", "asphodel", 20, 5)
    s.piece("phrygana", "sage", 27, 4)
    # the west: vineyard terraces with low vines (optional grass)
    vine_row(s, 1, 9, 4)
    vine_patch(s, 1, 5, 9, 3, grapes={(4, 1)}, dig=(7, 1))
    vine_row(s, 1, 9, 8)
    # the cutting: limestone cliffs close in either side, the labrys door east
    for (x0, x1) in ((6, 11), (15, 22)):
        s.piece("cliff", "lip_L", x0, 10)
        for x in range(x0 + 1, x1):
            s.piece("cliff", "lip", x, 10)
        s.piece("cliff", "lip_R", x1, 10)
        for y in (11, 12):
            s.piece("cliff", "face_L", x0, y)
            for x in range(x0 + 1, x1):
                s.piece("cliff", "face" if x % 3 else "face_b", x, y)
            s.piece("cliff", "face_R", x1, y)
        for x in range(x0 + 1, x1):
            s.piece("cliff", "foot_grass", x, 13)
    s.part("labrys_door", "top_L", 17, 11, 3, 2)
    s.rect(12, 10, 14, 13, PATH)
    # the beekeeper's hut and its spring, south-west
    s.put("mitato", 3, 15)
    s.m[15, 6] = s.m[15, 6]
    s.piece("mitato", "runnel", 4, 18)
    s.piece("mitato", "runnel", 4, 19)
    s.piece("mitato", "hives", 7, 16)
    s.piece("mitato", "skeps", 8, 16)
    s.piece("phrygana", "thyme", 1, 17)
    s.piece("phrygana", "thyme_b", 8, 18)
    # Ida's gate in a terrace wall to the south-west
    s.wall_run("terrace", 0, 10, 21, top=True)
    s.part("ida_gate", "pillar_L_top", 6, 20, 3, 2)
    # east: the band of olives and the forced grass band 2, after the cutting
    s.rect(15, 15, 27, 18, TALL)
    s.rect(15, 14, 27, 14, GRASS)
    for x in (16, 20, 24):
        s.olive(x, 19) if x + 1 < W else None
    s.cypress(28, 15)
    s.cypress(29, 17)
    s.olive(27, 9)
    s.sprite("tauros", 4, 22, 8)
    return s


def bronze_heel():
    """The Bronze Heel, 20 x 13: Talos's foot on the beach, the tide pools,
    the fossil ledge at the tide line, the reef spit out to its tip."""
    W, H = 20, 13
    s = Scene("bull_road", W, H, fill=SAND)
    s.rect(0, 0, W - 1, 1, GRASS)
    s.path_patch(0, 0, 3, 1)
    for x in (5, 9, 14, 18):
        s.piece("phrygana", "thyme" if x % 2 else "sage", x, 0)
    s.piece("phrygana", "asphodel", 11, 1)
    s.piece("phrygana", "burnet", 16, 1)
    # the brow down onto the beach
    brow_run(s, 4, 19, 2)
    s.put("talos_foot", 6, 3)
    s.piece("tide_pools", "pool", 13, 6)
    s.piece("tide_pools", "pool_b", 15, 7)
    s.piece("tide_pools", "urchins", 17, 6)
    s.piece("tide_pools", "pool_dig", 14, 8)
    s.piece("sand_decor", "shells", 3, 6)
    s.piece("sand_decor", "footprints", 4, 8)
    s.piece("tide_pools", "ledge_skull", 2, 9)
    s.piece("tide_pools", "ledge_dart", 3, 9)
    s.shore(["####################",
             "~~~~~~~~~~~~~~~~#~~~",
             "~~~~~~~~~~~~~~~~#~~~",
             ], 0, 10)
    s.piece("rocks", "spit_V", 16, 11)
    s.piece("rocks", "spit_head", 16, 12)
    s.piece("rocks", "spit_M", 16, 10)
    s.piece("rocks", "tide_rock", 9, 12)
    s.piece("rocks", "rocks_sand", 12, 9)
    s.piece("sand_decor", "lace", 7, 9)
    s.piece("sand_decor", "wrack", 10, 9)
    return s


# --------------------------------------------------------------------------
# The Palace of Minos
# --------------------------------------------------------------------------

def court_pave(s, x0, y0, x1, y1, seed=0):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            k = (x * 5 + y * 3 + seed) % 13
            n = "ABCD"[(x + 2 * y + seed) % 4]
            if k == 0:
                n = "cracked"
            elif k == 7:
                n = "weeds"
            s.piece("paving", n, x, y)


def wall_row(s, x0, x1, y, faces=None, tops=None):
    """A west-east wall: tops on row y, faces on row y+1 (and more rows in
    `faces`, a list of per-row name lists or None for plain)."""
    for x in range(x0, x1 + 1):
        t = "top_L" if x == x0 else ("top_R" if x == x1 else "top")
        if tops and x in tops:
            t = tops[x]
        s.piece("walls", t, x, y)
    for r, row in enumerate(faces or [None]):
        for x in range(x0, x1 + 1):
            f = "face_L" if x == x0 else ("face_R" if x == x1 else "face")
            if row and x in row:
                f = row[x]
            if f:
                s.piece("walls", f, x, y + 1 + r)


def palace_court():
    """One screen (15 x 10) of the Central Court: the north wing's wall with
    the Throne Room's door and the bull-leapers fresco, the bull-leaping
    lane with its painted line, the Gentle Bull at its far end, his pen, a
    colonnade."""
    s = Scene("palace_minos", 15, 10)
    court_pave(s, 0, 0, 14, 9)
    wall_row(s, 0, 14, 0,
             faces=[{3: "face_frieze", 4: "face_frieze", 5: "face_frieze", 6: "face_frieze",
                     7: "face_frieze", 8: "face_frieze", 1: "face_window", 13: "face_labrys"},
                    {3: "door", 1: "face_labrys", 6: "face_window"}],
             tops={5: "top_horns", 7: "top_broken", 12: "top_horns", 2: "top_horns"})
    s.part("frescoes", "leap_TL", 9, 1, 3, 2)
    # the lane: nine cells west to east, the line in front of the leaper
    s.piece("paving", "lane_W", 2, 5)
    for x in range(3, 10):
        s.piece("paving", "lane_h_line" if x == 3 else "lane_h", x, 5)
    s.piece("paving", "lane_E", 10, 5)
    # the pen, south-east
    s.piece("court_works", "fence_L", 11, 7)
    s.piece("court_works", "fence_gate", 12, 7)
    s.piece("court_works", "fence", 13, 7)
    s.piece("court_works", "fence_R", 14, 7)
    s.piece("court_works", "trough", 12, 8)
    s.piece("court_works", "hay", 14, 8)
    # a colonnade along the south
    for x in (1, 3, 5, 7):
        s.piece("columns", "col_top", x, 8)
        s.piece("columns", "col", x, 9)
    s.piece("columns", "pithos_top", 9, 8)
    s.piece("columns", "pithos", 9, 9)
    # the Gentle Bull pawing at the far end
    s.sprite("tauros", 4, 10, 5)
    return s


def palace_hill():
    """The palace on its hill (24 x 16), from the south: the limestone face
    of Kephala with a broad stair up it; on the plateau the North Entrance's
    portico and charging bull, the West Court's kouloura, the Theatral
    Area's steps."""
    W, H = 24, 16
    s = Scene("palace_minos", W, H)
    court_pave(s, 0, 0, W - 1, 9, seed=3)
    # the entrance wing: a wall two faces tall with the charging bull
    wall_row(s, 7, 17, 0, faces=[{8: "face_frieze", 9: "face_frieze", 15: "face_frieze",
                                    16: "face_frieze"},
                                   {12: "door"}],
             tops={9: "top_horns", 15: "top_horns", 12: "top_horns"})
    s.part("frescoes", "bull_TL", 9, 1, 3, 2)
    # a portico in front of the door
    s.piece("columns", "beam_L", 11, 3)
    s.piece("columns", "beam_col", 12, 3) if False else s.piece("columns", "beam_horns", 12, 3)
    s.piece("columns", "beam_R", 13, 3)
    s.piece("columns", "under_col", 11, 4)
    s.piece("columns", "under", 12, 4)
    s.piece("columns", "under_col", 13, 4)
    # the West Court: a kouloura; the Theatral Area's steps, east
    s.part("court_works", "pit_TL", 2, 2, 2, 2)
    s.run("court_works", ["steps_L", "steps", "steps", "steps", "steps_R"], 18, 4)
    s.run("court_works", ["steps_L", "steps", "steps", "steps", "steps_R"], 18, 5)
    for x in range(18, 23):
        s.piece("paving", "dance" if x % 2 else "dance_b", x, 6)
        s.piece("paving", "dance_b" if x % 2 else "dance", x, 7)
    for (x, y) in ((5, 6), (14, 7)):
        s.piece("columns", "col_top", x, y)
        s.piece("columns", "col", x, y + 1)
    s.piece("columns", "stump", 7, 7)
    s.piece("walls", "horns", 16, 7)
    s.piece("walls", "rubble", 1, 7)
    # the plateau's edge and the hill's face, the stair cut up it
    for x in range(W):
        s.piece("paving", "edge_S", x, 9)
    s.rect(0, 10, W - 1, 10, GRASS)
    s.piece("cliff", "lip_L", 0, 10)
    for x in range(1, W - 1):
        s.piece("cliff", "lip_b" if x % 4 == 1 else "lip", x, 10)
    s.piece("cliff", "lip_R", W - 1, 10)
    for y in (11, 12):
        s.piece("cliff", "face_L", 0, y)
        for x in range(1, W - 1):
            s.piece("cliff", "face_b" if (x + y) % 4 == 0 else "face", x, y)
        s.piece("cliff", "face_R", W - 1, y)
    for x in range(1, W - 1):
        s.piece("cliff", "foot_grass", x, 13)
    s.part("court_works", "stair_L", 11, 11, 2, 2)
    s.rect(11, 9, 12, 10, s.s["paving"]["ids"][0][0])
    s.rect(11, 13, 12, 15, PATH)
    for x in (3, 7, 16, 20):
        s.olive(x, 15)
    s.cypress(1, 14)
    s.cypress(22, 14)
    return s


SCENES = {
    "amnisos_quay": (amnisos_quay, "knossa_amnisos_quay.png", 3),
    "amnisos_town": (amnisos_town, "knossa_amnisos_town.png", 2),
    "bull_road": (bull_road, "knossa_bull_road.png", 3),
    "bull_road_wide": (bull_road_wide, "knossa_bull_road_wide.png", 2),
    "bronze_heel": (bronze_heel, "knossa_bronze_heel.png", 2),
    "palace_court": (palace_court, "knossa_palace_court.png", 3),
    "palace_hill": (palace_hill, "knossa_palace_hill.png", 2),
}
ONE_X = {"amnisos_quay", "bull_road", "palace_court"}


def main(argv):
    names = [a for a in argv if not a.startswith("--")]
    pas = None
    if "--pass" in argv:
        pas = argv[argv.index("--pass") + 1]
        names = [n for n in names if n != pas]
    IMG.mkdir(parents=True, exist_ok=True)
    for n in names or list(SCENES):
        fn, out, sc = SCENES[n]
        s = fn()
        s.render(IMG / out, scale=sc)
        if n in ONE_X:
            s.render(IMG / out.replace(".png", "_1x.png"), scale=1)
        if pas:
            s.render(IMG / out.replace(".png", f"_pass{pas}.png"), scale=sc)


if __name__ == "__main__":
    main(sys.argv[1:])
