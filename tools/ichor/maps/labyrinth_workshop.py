"""Daedalus's workshop (design/LABYRINTH.md §6 Ring III and scene D,
design/maps/LabyrinthWorkshop.md): the hub at the end of Ring III, on the
`daidaleion` tileset. The room is the approved scene-D mock-up
(tools/ichor/art/labyrinth_scene.workshop), laid as the real map, plus its ways:
the back door in the arcade (Ring III's glow trail), the threshold to the front
way, the stair down to Ring IV in the shelves' bay, and the lift.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import labyrinth_tiles as LT  # noqa: E402
from kythera_maps import Map, _attrs, ROOT  # noqa: E402
import numpy as np  # noqa: E402

NAME = "LabyrinthWorkshop"
TS = "daidaleion"
W, H = 24, 18
P = NAME + "_EventScript_"


def room():
    import labyrinth_scene as S
    S.CATS["daidaleion"] = LT.TILESETS[TS]["structures"]
    orig = S.Room

    class R(orig):
        def __init__(self, w=W, h=H, tileset="daidaleion", fill=("floor", 1, 0)):
            orig.__init__(self, w, h, tileset, fill)
    S.Room = R
    try:
        r = S.workshop("lit")
    finally:
        S.Room = orig
    return r


class WMap(Map):
    def __init__(self):
        self.name, self.ts, self.w, self.h, self.primary = NAME, TS, W, H, "oikos"
        self.cat = LT.TILESETS[TS]
        self.mid = np.zeros((H, W), np.uint16)
        self.solid = np.ones((H, W), bool)
        self.pattr = _attrs("data/tilesets/primary/oikos/porytiles_bin/metatile_attributes.bin")
        self.sattr = _attrs(f"data/tilesets/secondary/{TS}/porytiles_bin/metatile_attributes.bin")
        self.objects, self.warps, self.coords, self.bgs, self.connections = [], [], [], [], []
        self.seams = []
        void = LT.mid(TS, "floor", "void")
        self.border = [void] * 4
        self.header = {"requires_flash": False, "map_type": "MAP_TYPE_INDOOR", "show_map_name": True,
                       "music": "MUS_ICHOR_ELPIS_LULLABY_BOX", "region_map_section": "MAPSEC_WATER_LABYRINTH",
                       "allow_running": True, "allow_cycling": False, "allow_escaping": False}
        self.forced_open = set()

    def cellp(self, key, cx, cy, x, y, solid=None):
        s = self.cat["structures"][key]
        self.set(x, y, s["ids"][cy][cx], (s["walk"][cy][cx] == "X") if solid is None else solid)


def build(render=True):
    r = room()
    m = WMap()
    for y in range(H):
        for x in range(W):
            key, cx, cy = r.g[y][x]
            m.cellp(key, cx, cy, x, y)
    # the stair down to Ring IV, in the shelves' bay (its lowest shelf taken out)
    m.cellp("stairs", 0, 0, 6, 2, False)
    m.cellp("stairs", 1, 0, 7, 2, False)
    # --- events ------------------------------------------------------------------------------
    m.warp(11, 17, "MAP_LABYRINTH_RING3", 6)       # 0: the threshold, the front way
    m.warp(1, 2, "MAP_LABYRINTH_RING3", 7)         # 1: the back door
    m.warp(6, 2, "MAP_LABYRINTH_RING4", 0)         # 2, 3: the stair down
    m.warp(7, 2, "MAP_LABYRINTH_RING4", 0)
    m.warps.append({"x": 6, "y": 3, "elevation": 0, "dest_map": "MAP_LABYRINTH_WORKSHOP", "dest_warp_id": "4"})
    m.warps.append({"x": 20, "y": 3, "elevation": 0, "dest_map": "MAP_LABYRINTH_WORKSHOP", "dest_warp_id": "5"})
    m.warp(12, 17, "MAP_LABYRINTH_RING3", 6)       # 6: the threshold's other half
    m.obj("ICHOR_ELDER_M", 12, 7, P + "Daedalus", move="MOVEMENT_TYPE_FACE_DOWN",
          local_id="LOCALID_WORKSHOP_DAEDALUS")
    m.sign(21, 7, P + "HealBed")
    m.sign(22, 7, P + "HealBed")
    m.sign(15, 9, P + "MusicBox")
    m.sign(5, 5, P + "NumberFour")
    m.sign(5, 6, P + "NumberFour")
    m.sign(20, 2, P + "Lift")
    m.sign(11, 2, P + "Shaft")
    m.sign(12, 2, P + "Shaft")
    for x in (2, 3, 4):
        m.sign(x, 2, P + "WingsPlan")
    for x in (15, 16, 17):
        m.sign(x, 2, P + "LabyrinthPlan")
    errs, reach = Map.check(m, [(11, 16)])
    Map.write(m)
    if render:
        m.render("labyrinth_workshop", [(11, 8)])
    for e in errs:
        print("CHECK:", e)
    print(f"{NAME}: {len(m.objects)} objects, {len(m.warps)} warps, {len(m.bgs)} bg events")


if __name__ == "__main__":
    build(render="--no-render" not in sys.argv)
