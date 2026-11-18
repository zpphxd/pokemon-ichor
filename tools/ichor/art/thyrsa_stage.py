#!/usr/bin/env python3
"""Draw the Temple of Dionysus's stage pieces into the ThyrsaRooms tileset.

The Three-Act Play (tools/ichor/maps/thyrsa.py) needs art the room tileset
never had: the painted door panels the puzzle reads from, a trapdoor, the
mechane crane, the ekkyklema, an open doorway, Dionysus's statue, footlights,
painted backdrops, floorcloths for each act's scene, goat-men props, a ship
cutout and a dressing-room mirror.

Every new metatile is appended after the hand-drawn ones (from 0x298), in
porytiles_src/{bottom,middle,top}.png. Each 8x8 tile of each layer is snapped
to whichever of the tileset's own seven palettes fits it best, so the new art
never adds a color. Objects come in "twins": the same middle layer over each
floor they stand on, which costs metatiles but no tiles. The ids are written
to thyrsa_stage_ids.json for the map builder.

  /usr/bin/python3 tools/ichor/art/thyrsa_stage.py          # draw, then compile
  /usr/bin/python3 tools/ichor/art/thyrsa_stage.py --sheet  # also a review sheet
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
TS = ROOT / "data/tilesets/secondary/thyrsa_rooms"
SRC = TS / "porytiles_src"
IDS = Path(__file__).with_name("thyrsa_stage_ids.json")
FIRST = 0x298           # the first metatile after the hand-drawn set
HAND_DRAWN = FIRST - 0x200
MAGENTA = (255, 0, 255)
TILE_BUDGET = 496       # CLAUDE.md: 504 at most; keep the door-animation tiles free

# Color keys. Each picture keeps to one palette's colors per 8x8 tile.
KEY = {
    "k": (40, 24, 24),
    # palette 06: sky, sea, gold, brass, white
    "w": (240, 240, 232), "l": (208, 200, 192), "x": (160, 152, 144), "G": (232, 184, 88),
    "o": (176, 128, 48), "n": (112, 72, 32), "r": (184, 56, 40), "R": (216, 64, 32),
    "O": (248, 144, 48), "y": (248, 224, 104), "c": (248, 232, 168), "s": (120, 176, 224),
    "B": (56, 112, 184), "g": (72, 120, 56),
    # palette 09: vines, grapes, hills
    "D": (40, 72, 48), "V": (120, 168, 80), "h": (184, 216, 128), "P": (56, 24, 64),
    "p": (96, 56, 104), "u": (136, 80, 144), "L": (184, 136, 192), "W": (248, 248, 232),
    "e": (120, 88, 48), "t": (176, 136, 72), "q": (224, 192, 128), "Q": (208, 184, 144),
    # palette 10: the walls' own colors, and the sea backdrop
    "b": (56, 96, 160), "a": (104, 152, 208), "i": (200, 224, 240), "m": (80, 48, 32),
    "M": (160, 104, 56), "z": (232, 224, 208), "Z": (248, 240, 232), "T": (224, 176, 96),
    # palette 08: stage wood and sand
    "1": (112, 64, 56), "2": (128, 80, 64), "3": (152, 96, 72), "4": (168, 104, 80),
    "5": (176, 136, 96), "6": (192, 176, 144), "7": (208, 192, 160), "8": (232, 224, 192),
}


def grid(text):
    rows = [r for r in text.strip("\n").split("\n")]
    rows = [r.strip() for r in rows]
    assert len(rows) == 16, (len(rows), rows)
    for r in rows:
        assert len(r) == 16, (len(r), r)
    out = np.zeros((16, 16, 4), np.uint8)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != ".":
                out[y, x, :3] = KEY[ch]
                out[y, x, 3] = 255
    return out


# --- The art ------------------------------------------------------------------------------

# Door panels, each a framed picture on the dado. The puzzle reads from these.
PANEL_VINES = grid("""
................
.kkkkkkkkkkkkkk.
.kqqqqqqqqqqqqk.
.kqpppppppWWpqk.
.kqppppppWWWWqk.
.kqpppppppWWpqk.
.kqpppppppppppk.
.kqppVVVVppppqk.
.kqVVVVVVVVVpqk.
.kqVDuDVDuDVVqk.
.kqgDPDgDPDgDqk.
.kqgDuDgDuDgDqk.
.kqggggggggggqk.
.kqqqqqqqqqqqqk.
.kkkkkkkkkkkkkk.
................
""")
PANEL_HOUSE = grid("""
................
.kkkkkkkkkkkkkk.
.kGGGGGGGGGGGGk.
.kGssssssssssGk.
.kGsssrrrrsssGk.
.kGssrrrrrrssGk.
.kGsrrrrrrrrsGk.
.kGcccckkccccGk.
.kGccckOOkcccGk.
.kGcckOyyOkccGk.
.kGcckOyyOkccGk.
.kGcckOOOOkccGk.
.kGnnnnnnnnnnGk.
.kGGGGGGGGGGGGk.
.kkkkkkkkkkkkkk.
................
""")
PANEL_SHIP = grid("""
................
.kkkkkkkkkkkkkk.
.kGGGGGGGGGGGGk.
.kGssssgsssssGk.
.kGsssgnwwsssGk.
.kGssssgwwwssGk.
.kGsssgnwwwwsGk.
.kGssssnsssssGk.
.kGnnnnnnnnnkGk.
.kGkwnnnnnnkBGk.
.kGBknnnnnkBBGk.
.kGBBBsBBBBsBGk.
.kGBBBBBBBBBBGk.
.kGGGGGGGGGGGGk.
.kkkkkkkkkkkkkk.
................
""")

# A trapdoor let into the stage planks.
TRAPDOOR = grid("""
................
.11111111111111.
.13333333333331.
.13444444444431.
.13333333333331.
.13444444444431.
.13333311333331.
.13444133144431.
.13333133133331.
.13444411444431.
.13333333333331.
.13444444444431.
.13333333333331.
.13444444444431.
.11111111111111.
................
""")

# The mechane: a beam out over the stage, its pulley, and the hook on its ropes.
CRANE_BEAM = grid("""
................
................
................
................
................
................
....kkkkkkkkkkkk
...knooooooooooo
...knnnnnnnnnnnn
....kkkkkkkkkkkk
........kon.....
.......kon......
......kon.......
.....kon........
....kon.........
....kk..........
""")
CRANE_PULLEY = grid("""
................
................
................
................
................
................
kkkkkkkkkkk.....
ooooooooook.....
nnnnnnnnnnk.....
kkkkkkkkkkk.....
.....kGGk.......
....kGkkGk......
....kGkkGk......
.....kGGk.......
.....o..o.......
.....o..o.......
""")
CRANE_HOOK = grid("""
.....o..o.......
.....o..o.......
.....o..o.......
.....o..o.......
.....o..o.......
.....o..o.......
.....o..o.......
.....o..o.......
.....kkkkk......
.....kxxxk......
.......kx.......
.....kx.kx......
.....kx.kx......
......kxxk......
................
................
""")

# The ekkyklema, the rolling stage, in two halves (the right is the left mirrored).
EKKYKLEMA_L = grid("""
................
................
................
................
..kkkkkkkkkkkkkk
.kGGGGGGGGGGGGGG
.koooooooooooooo
.knnnnnnnnnnnnnn
.koooooooooooooo
.knnnnnnnnnnnnnn
.kkkkkkkkkkkkkkk
..kxxxk.........
.kxkkkxk........
.kxkGkxk........
.kxkkkxk........
..kxxxk.........
""")
EKKYKLEMA_R = EKKYKLEMA_L[:, ::-1].copy()

# Dionysus: ivy-crowned, his thyrsus (a fennel staff tipped with a pine cone) in hand.
STATUE_TOP = grid("""
................
..........kk....
....kkkk.kGGk...
...kgygggkGoGk..
..kgwwwwgkGGk...
..kwwlwwwk.kok..
..kwkwwkwk.kok..
..kwwwwwwk.kok..
...kwlwwk..kok..
....kwwk...kok..
..kkwwwwkk.kok..
.kwwwwwwwwkkok..
kwwlwwwwlwwkwk..
kwlwwwwwwlwkwk..
kwlwwwwwwlwkok..
kwlwwwwwwlwkok..
""")
STATUE_BASE = grid("""
kwlwwwwwwlwkok..
kwlwwwwwwlwkok..
.kwlwwwwlwkkok..
.kwlwwwwlwk.kok.
.kwlwwwwlwk.kok.
..kwlwwlwk..kok.
..kwlwwlwk..kok.
.kkkkkkkkkkkkkk.
.kGGGGGGGGGGGGk.
..kllllllllllk..
..klxxxxxxxxlk..
..klxlllllxxlk..
..klxxxxxxxxlk..
.kkkkkkkkkkkkkk.
.kxxxxxxxxxxxxk.
.kkkkkkkkkkkkkk.
""")

# Footlights: oil lamps along the stage's edge.
FOOTLIGHTS = grid("""
................
................
................
................
................
...y.......y....
..yOy.....yOy...
..yOy.....yOy...
...k.......k....
.kkkkk...kkkkk..
koooonk.koooonk.
knnnnnk.knnnnnk.
GGGGGGGGGGGGGGGG
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
kkkkkkkkkkkkkkkk
""")

# A goat-man's mask on a pole, for the satyr play's hillside.
GOAT_POLE = grid("""
................
..kk........kk..
.kMk........kMk.
.kMMk......kMMk.
..kTkkkkkkkkTk..
..kTTTTTTTTTTk..
.kTTkkTTTTkkTTk.
.kTTkiTTTTikTTk.
.kTTTTTmmTTTTTk.
..kTTTmmmmTTTk..
...kTTTzzTTTk...
....kmTTTTmk....
.....kkMMkk.....
.......mm.......
.......mm.......
......kmmk......
""")

# A painted ship cutout: hull and mast, then the prow with its eye.
SHIP_L = grid("""
..........k.....
.........kwk....
........kwwwk...
.......kwwrwwk..
.......kwwrwwk..
........kwwwk...
.k.......knk....
kok......knk....
kokkkkkkkknkkkkk
.koooooooooooooo
.knnnnnnnnnnnnnn
..kooooooooooooo
...knnnnnnnnnnnn
....kkkkkkkkkkkk
................
................
""")
SHIP_R = grid("""
................
................
................
................
................
................
..............k.
.............kok
kkkkkkkkkkkkkkok
oooooooooooook.k
nnnnnwwknnnnk...
oooooowkkoook...
nnnnnnnnnnkk....
kkkkkkkkkk......
................
................
""")

# A dressing-room mirror of polished bronze on a stand.
MIRROR = grid("""
................
.....mmmmmm.....
....mTTTTTTm....
...mTaiiiiaTm...
...mTiiZiiaTm...
...mTiZiiaaTm...
...mTiiiaaaTm...
...mTiiaaabTm...
...mTiaaabbTm...
....mTaabbTm....
.....mTTTTm.....
.......mm.......
.......MM.......
.......MM.......
.....mMMMMm.....
....mmmmmmmm....
""")


def seamless(pattern):
    """A 16x16 floor from one 8x8 pattern repeated, so it costs one tile."""
    rows = [r.strip() for r in pattern.strip("\n").split("\n")]
    assert len(rows) == 8 and all(len(r) == 8 for r in rows), rows
    return grid("\n".join(r + r for r in rows + rows))


SAND = """
77777777
76677777
77777787
77778877
77777777
77777767
88777777
77777777
"""
SAND_SHELL = grid("""
7777777777777777
7667777776677777
7777778777777787
7777887777778877
7777777777777777
7777776777777767
8877777788777777
7777777777777777
7777777777777777
7667777776677777
77777787777k7787
777788777kOOk877
7777777777kk7777
7777776777777767
8877777788777777
7777777777777777
""")
GRASS = """
VVVVVVVV
VhVVVVVV
VhhVVVgV
VVVVVggV
VVVVVVVV
VVgVVVVV
VggVVhVV
VVVVVhhV
"""
GRASS_FLOWERS = grid("""
VVVVVVVVVVVVVVVV
VhVVVVVVVhVVVVVV
VhhVVVgVVhhVVVgV
VVVVVggVVVVLLggV
VVVVVVVVVVLWLVVV
VVgVVVVVVVgLVVVV
VggVVhVVVggVVhVV
VVVVVhhVVVVVVhhV
VVVVVVVVVVVVVVVV
VhVLLVVVVhVVVVVV
VhLWLVgVVhhVVVgV
VVgLVggVVVVVVggV
VVVVVVVVVVVVVVVV
VVgVVVVVVVgVVVVV
VggVVhVVVggVVhVV
VVVVVhhVVVVVVhhV
""")

# Backdrops: painted below the cornice (rows 8-15) of the plain upper wall, so
# the cornice tiles stay the hand-drawn ones.
SEA_SKY = ["iiiiiiiiiiiiiiii", "iiiiiZZiiiiiiiii", "iiiZZZZZiiiiiiii", "iiiiiiiiiiiiiiii",
           "aaaaaaaaaaaaaaaa", "aaZaaaaaaaaaZaaa", "bbbbbbbbbbbbbbbb", "babbbbbbbabbbbbb"]
SEA_SAIL = ["iiiiiiiiiiiiiiii", "iiiiiiiiiiZiiiii", "iiiiiiiiiZZmiiii", "iiiiiiiiZZZmiiii",
            "aaaaaaaaammmmaaa", "aaZaaaaaaaaaaaaa", "bbbbbbbbbbbbbbbb", "babbbbbbbabbbbbb"]
HILL_SKY = ["WWWWWWWWWWWWWWWW", "WWWWWWWWWWWWWWWW", "WWWWVVVWWWWWWWWW", "WWVVVVVVVWWWWWWW",
            "VVVVVVVVVVVVWWWW", "VVVgVVVVVVVVVVVV", "gggggVVVgggVVVgg", "gggggggggggggggg"]
HILL_TREE = ["WWWWWWWWWWWWWWWW", "WWWWWWWWWDDWWWWW", "WWWWWWWWDgDDWWWW", "WWWWWWWDgDgDWWWW",
             "VVVVVVVVDDDDVVVW", "VVVgVVVVVeVVVVVV", "gggggVVVVeVVVVgg", "gggggggggggggggg"]
# The sea runs on into the top of the dado (rows 0-4), above the frieze.
SEA_DADO = ["bbbbbbbbbbbbbbbb", "bbabbbbbbbbabbbb", "bbbbbbbbbbbbbbbb", "zzzzzzzzzzzzzzzz",
            "zzzzzzzzzzzzzzzz"]

# Each new metatile: (name, bottom, middle). A bottom is an existing metatile id
# (its bottom layer is copied), a 16x16 grid, or ("paint", base id, rows from, rows).
OBJECTS = {
    "PANEL_VINES": PANEL_VINES, "PANEL_HOUSE": PANEL_HOUSE, "PANEL_SHIP": PANEL_SHIP,
    "CRANE_BEAM": CRANE_BEAM, "CRANE_PULLEY": CRANE_PULLEY, "CRANE_HOOK": CRANE_HOOK,
    "EKKYKLEMA_L": EKKYKLEMA_L, "EKKYKLEMA_R": EKKYKLEMA_R,
    "STATUE_TOP": STATUE_TOP, "STATUE_BASE": STATUE_BASE, "FOOTLIGHTS": FOOTLIGHTS,
    "GOAT_POLE": GOAT_POLE, "SHIP_L": SHIP_L, "SHIP_R": SHIP_R, "MIRROR": MIRROR,
}
WALL_TOP, WALL_BOTTOM, WOOD, WOOD_SHADOW, STONE = 0x25E, 0x204, 0x26D, 0x267, 0x21A
# Existing props reused on the new floors (their middle layer over a new bottom).
REUSED = {"KRATER": 0x265, "AMPHORA": 0x278, "URN": 0x27B, "TORCH": 0x28F, "STOOL": 0x284,
          "CRATE_L": 0x24B, "CRATE_R": 0x24C, "TABLE_L": 0x275, "TABLE_R": 0x276,
          "VINES_L": 0x21C, "VINES_R": 0x21D, "RACK": 0x28A, "SHELVES": 0x288,
          "BENCH": 0x269, "LECTERN": 0x287}


class Sheet:
    def __init__(self):
        self.layers = {l: np.array(Image.open(SRC / f"{l}.png").convert("RGBA"))
                       for l in ("bottom", "middle", "top")}
        for l, a in self.layers.items():   # forget earlier runs' output
            self.layers[l] = a[:(HAND_DRAWN // 8 + 1) * 16].copy()
            self.layers[l][(HAND_DRAWN // 8) * 16:, (HAND_DRAWN % 8) * 16:] = (
                (40, 24, 24, 255) if l == "bottom" else (*MAGENTA, 255))
        self.pals = []
        for i in range(6, 13):
            lines = (TS / f"porytiles_bin/palettes/{i:02d}.pal").read_text().split()[3:]
            cols = [tuple(int(v) for v in lines[j:j + 3]) for j in range(0, len(lines), 3)]
            self.pals.append(np.array([c for c in cols[1:] if c != (0, 0, 0) or i != 12], float))
        self.ids = {}
        self.next = HAND_DRAWN

    def cell(self, layer, mid):
        i = mid - 0x200
        return self.layers[layer][(i // 8) * 16:(i // 8) * 16 + 16, (i % 8) * 16:(i % 8) * 16 + 16]

    def snap(self, art, opaque):
        """Each 8x8 tile to the closest of the tileset's palettes."""
        out = art.copy()
        for ty in (0, 8):
            for tx in (0, 8):
                t = art[ty:ty + 8, tx:tx + 8]
                solid = t[..., 3] > 0
                if not solid.any():
                    continue
                px = t[..., :3][solid].astype(float)
                best = None
                for pal in self.pals:
                    d = ((px[:, None, :] - pal[None, :, :]) ** 2).sum(-1)
                    err = d.min(1).sum()
                    if best is None or err < best[0]:
                        best = (err, pal[d.argmin(1)])
                block = out[ty:ty + 8, tx:tx + 8]
                block[..., :3][solid] = best[1].astype(np.uint8)
                if not opaque:
                    block[~solid] = (*MAGENTA, 255)
        if not opaque:
            out[out[..., 3] == 0] = (*MAGENTA, 255)
        return out

    def add(self, name, bottom, middle=None):
        n = self.next
        self.next += 1
        rows = (n // 8 + 1) * 16
        for l, a in self.layers.items():
            if a.shape[0] < rows:
                pad = np.zeros((rows - a.shape[0], 128, 4), np.uint8)
                pad[...] = (40, 24, 24, 255) if l == "bottom" else (*MAGENTA, 255)
                self.layers[l] = np.vstack([a, pad])
        if isinstance(bottom, int):
            b = self.cell("bottom", bottom).copy()
        else:
            b = self.snap(bottom, True)
        x, y = (n % 8) * 16, (n // 8) * 16
        self.layers["bottom"][y:y + 16, x:x + 16] = b
        if middle is not None:
            self.layers["middle"][y:y + 16, x:x + 16] = self.snap(middle, False)
        self.ids[name] = 0x200 + n
        return 0x200 + n

    def middle_of(self, mid):
        art = self.cell("middle", mid).copy()
        art[(art[..., :3] == MAGENTA).all(-1), 3] = 0
        return art

    def painted(self, base, start, rows):
        assert all(len(r) == 16 for r in rows), rows
        full = ["." * 16] * start + rows + ["." * 16] * (16 - start - len(rows))
        return self.overlay(base, grid("\n".join(full)))

    def overlay(self, base, art):
        out = self.cell("bottom", base).copy()
        solid = art[..., 3] > 0
        out[solid] = art[solid]
        return out

    def save(self):
        for l, a in self.layers.items():
            Image.fromarray(a).save(SRC / f"{l}.png")


def build():
    s = Sheet()
    sand = seamless(SAND)
    grass = seamless(GRASS)
    floors = {"WOOD": WOOD, "SHADOW": WOOD_SHADOW, "STONE": STONE}
    floors["SAND"] = s.add("SAND", sand)
    s.add("SAND_SHELL", SAND_SHELL)
    floors["GRASS"] = s.add("GRASS", grass)
    s.add("GRASS_FLOWERS", GRASS_FLOWERS)
    s.add("TRAPDOOR", s.overlay(WOOD, TRAPDOOR))
    # An open doorway: the leaf swung back against the left jamb, the dark of the
    # wings inside, and stage light on the boards at the threshold.
    def way(inside):
        return "zzk" + "MT" + inside + "kzz"
    s.add("DOORWAY_TOP", s.painted(WALL_TOP, 4, [
        "kkk" + "m" * 10 + "kkk", way("kkkkkkkk"), way("kkkkkkkk"), way("kkkkkkkk"),
        way("kkkkkkkk"), way("kmmkkmmk"), way("kkkkkkkk"), way("kmkkkkmk"),
        way("kkkkkkkk"), way("mkkmmkkm"), way("kkkkkkkk"), way("mmkmmkmm")]))
    s.add("DOORWAY_BOTTOM", s.painted(WALL_BOTTOM, 0, [
        way("mmmmmmmm"), way("1m11m11m"), way("12112112"), way("12212212"),
        way("22322322"), way("23323323"), way("23323323"), way("33433433"),
        way("33433433"), way("34434434"), way("34434434"), way("44544544"),
        way("44544544"), way("45545545"), way("45545545"), way("55555555")]))
    s.add("BACKDROP_SEA", s.painted(WALL_TOP, 8, SEA_SKY))
    s.add("BACKDROP_SEA_SAIL", s.painted(WALL_TOP, 8, SEA_SAIL))
    s.add("DADO_SEA", s.painted(WALL_BOTTOM, 0, SEA_DADO))
    s.add("BACKDROP_HILL", s.painted(WALL_TOP, 8, HILL_SKY))
    s.add("BACKDROP_HILL_TREE", s.painted(WALL_TOP, 8, HILL_TREE))
    # Objects: wall pieces over the wall, floor pieces over each floor they need.
    for name in ("PANEL_VINES", "PANEL_HOUSE", "PANEL_SHIP", "CRANE_HOOK"):
        s.add(name, WALL_BOTTOM, OBJECTS[name])
    for name in ("CRANE_BEAM", "CRANE_PULLEY"):
        s.add(name, WALL_TOP, OBJECTS[name])
    placements = {
        "CRANE_HOOK": ["WOOD"], "EKKYKLEMA_L": ["WOOD"], "EKKYKLEMA_R": ["WOOD"],
        "STATUE_TOP": ["SHADOW"], "STATUE_BASE": ["WOOD"], "FOOTLIGHTS": ["WOOD"],
        "GOAT_POLE": ["GRASS"], "SHIP_L": ["SAND"], "SHIP_R": ["SAND"],
        "MIRROR": ["SHADOW", "WOOD"],
    }
    for name, where in placements.items():
        for floor in where:
            s.add(f"{name}_{floor}", floors[floor], OBJECTS[name])
    reused = {"KRATER": ["GRASS"], "AMPHORA": ["SAND", "GRASS", "STONE"], "URN": ["SAND"],
              "TORCH": ["GRASS", "SAND"], "CRATE_L": ["WOOD"], "CRATE_R": ["WOOD"],
              "TABLE_L": ["STONE"], "TABLE_R": ["STONE"], "RACK": ["SHADOW", "STONE"],
              "SHELVES": ["SHADOW"], "STOOL": ["WOOD"],
              # the Amphitheater's seats and stands, on its stone orchestra
              "BENCH": ["STONE"], "LECTERN": ["STONE"]}
    for name, where in reused.items():
        for floor in where:
            s.add(f"{name}_{floor}", floors[floor], s.middle_of(REUSED[name]))
    assert s.next <= 512 - 0, s.next
    s.save()
    IDS.write_text(json.dumps({k: f"0x{v:03X}" for k, v in s.ids.items()}, indent=2) + "\n")
    subprocess.run([str(Path.home() / ".local/bin/porytiles"), "compile-tileset",
                    "gTileset_ThyrsaRooms"], cwd=ROOT, check=True)
    tiles = Image.open(TS / "porytiles_bin/tiles.png")
    count = tiles.size[0] // 8 * tiles.size[1] // 8
    print(f"thyrsa_rooms: {s.next} metatiles, {count} tiles (budget {TILE_BUDGET})")
    assert count <= TILE_BUDGET, count
    return s


if __name__ == "__main__":
    build()
    if "--sheet" in sys.argv:
        subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), "--sheet",
                        "thyrsa_rooms", "--primary", "aethos", "--scale", "4", "--range",
                        f"0x{FIRST:03X}-0x2FF", "-o", str(ROOT / "build/render/thyrsa_stage_sheet.png")],
                       check=True)
