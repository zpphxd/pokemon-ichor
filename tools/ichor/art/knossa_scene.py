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

    def render(self, out, scale=2):
        blk = ROOT / f"build/{self.dir}/scene.bin"
        blk.parent.mkdir(parents=True, exist_ok=True)
        self.m.astype("<u2").tofile(blk)
        subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--blockdata",
                        str(blk), "--width", str(self.W), "--primary", self.primary,
                        "--secondary", self.symbol, "--scale", str(scale), "-o", str(out)],
                       check=True)
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


SCENES = {
    "amnisos_quay": (amnisos_quay, "knossa_amnisos_quay.png", 3),
    "amnisos_town": (amnisos_town, "knossa_amnisos_town.png", 2),
}
ONE_X = {"amnisos_quay"}


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
