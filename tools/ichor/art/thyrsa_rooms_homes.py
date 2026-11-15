#!/usr/bin/env python3
"""Thyrsa's seven households: Pindaros the poet, Manto the seer, Staphylos the
vintner, Polos the actor, Eudora the soldier's mother, Euthykles the
mask-maker and Chthonia of the Sown Men. Registered into
thyrsa_rooms_art.STAMPS on import."""
import math

from thyrsa_rooms_art import stamp, grid, blank, over, hflip, STAMPS, recolor, OA  # noqa: F401
import thyrsa_rooms_civic as CIV  # noqa: F401  (the masks)


def _canvas(w, h):
    return [["."] * w for _ in range(h)]


def _put(g, x, y, c):
    if 0 <= y < len(g) and 0 <= x < len(g[0]):
        g[y][x] = c


def _text(g):
    return "\n".join("".join(r) for r in g)


def _paste(g, art, ox, oy):
    for dy, row in enumerate(art):
        for dx, c in enumerate(row):
            if c != ".":
                _put(g, ox + dx, oy + dy, c)


# ---- Pindaros: the poet's upper room -------------------------------------

def _pigeonholes(gap=False):
    """Scroll pigeonholes, 2x2 on the wall: each scroll end tagged with a
    victor's name in red."""
    g = _canvas(32, 32)
    for y in range(1, 32):
        for x in range(0, 32):
            if x in (0, 31) or y in (1, 31):
                c = "k"
            elif x in (1, 30) or y == 2:
                c = "m" if x in (1, 30) else "h"
            elif (y - 3) % 7 == 6 or (x - 2) % 7 == 6:
                c = "d"
            else:
                c = "k"                         # the dark of the cubby
            g[y][x] = c
    holes = [(2 + i * 7, 3 + j * 7) for j in range(4) for i in range(4)]
    for n, (hx, hy) in enumerate(holes):
        if gap and n in (5, 14):
            continue
        # three scroll ends stacked, cream with a dark core
        for (dx, dy) in ((0, 1), (3, 1), (1, 3)):
            _paste(g, [".cc.", "cCdc", "cCCc", ".cc."][:3], hx + dx - 0, hy + dy - 1)
        if n % 3 != 1:
            _put(g, hx + 2, hy + 5, "r")       # a red tag hanging
            _put(g, hx + 2, hy + 4, "R")
    return _text(g)


stamp("pigeonholes", 2, 2, art=[("wood", _pigeonholes())],
      note="pigeonholes full of scrolls, each tagged with a victor's name and the year")

stamp("lyre_peg", 1, 2, art=[("wood", """
................
................
................
................
................
................
.......kk.......
.......kk.......
....kk.kk.kk....
...khk....khk...
...khk....khk...
...kmkkkkkkmk...
...kmhhhhhhmk...
...kmkkkkkkmk...
....kmcccccmk...
....kmcccccmk...
....kmcccccmk...
....kmcccccmk...
...kkmcccccmkk..
..kddmcccccmddk.
..kdldkcccckldk.
..kdllldkkdllldk
..kdldlllllldldk
..kddlldllldlddk
...kddlllllddk..
....kkddddddk...
......kkkkk.....
................
................
................
................
................
""")], note="a lyre of tortoiseshell and horn on a peg")


def _kline_v(guest=False):
    """A dining couch seen end on, head to the north: 1x2."""
    cover = "c" if guest else "u"
    cover2 = "C" if guest else "U"
    rows = [
        "................",
        "..kkkkkkkkkkkk..",
        ".khhhhhhhhhhhhk.",
        ".kmkkkkkkkkkkmk.",
        ".kmkccccccCCkmk.",
        ".kmkcccccCCCkmk.",
        ".kmkkCCCCCCkkmk.",
    ]
    for y in range(7, 25):
        c = cover if y % 4 else cover2
        if guest and y in (9, 10):
            rows.append(".kmkrrrrrrrrkmk.")       # a folded red cloak for the guest
            continue
        rows.append(f".km{cover}{c * 8}{cover}mk.")
    rows += [
        ".kmkkkkkkkkkkmk.",
        ".khhhhhhhhhhhhk.",
        ".kdmmmmmmmmmmdk.",
        ".kkkkkkkkkkkkkk.",
        ".kdk........kdk.",
        ".kkk........kkk.",
        "................",
    ]
    return "\n".join(rows)


stamp("kline_v", 1, 2, art=[("wood", _kline_v())], note="a dining couch, end on, a blue coverlet")
stamp("kline_v_guest", 1, 2, art=[("wood", _kline_v(True))],
      note="the guest's couch, always made up: fresh linen and a folded red cloak")


def _tripod():
    g = _canvas(16, 32)
    # the cauldron
    _paste(g, ["..kkkkkkkkkkkk..", ".kyYYYYYYYYYYyk.", "kyYYyyyyyyyyyYbk", "kbyyyyyyyyyyyybk",
               ".kbyyyyyyyyybbk.", ".kzbbbbbbbbbbzk.", "..kzzbbbbbbzzk..", "...kkzzzzzzkk..."], 0, 2)
    # ring handles
    _paste(g, ["kk", "ky", "kk"], 0, 0)
    _paste(g, ["kk", "yk", "kk"], 14, 0)
    for x in (2, 3, 12, 13):
        _put(g, x, 1, "k")
    # three legs, splayed, lion's feet
    for y in range(10, 30):
        t = (y - 10) / 20
        for (x0, dx) in ((5, -3), (8, 0), (11, 3)):
            x = int(round(x0 + dx * t))
            _put(g, x - 1, y, "k")
            _put(g, x, y, "y" if dx <= 0 else "b")
            _put(g, x + 1, y, "k")
    for (x, y) in ((1, 30), (2, 30), (3, 30), (7, 30), (8, 30), (9, 30), (13, 30), (14, 30), (15, 30)):
        _put(g, x, y, "k")
    return _text(g)


stamp("victor_tripod", 1, 2, art=[("bronze", _tripod())],
      note="a bronze victor's tripod, won long ago for a song")


def _stairs_down_s():
    """Stairs going down south to the courtyard: 2x1, both cells the exit."""
    g = _canvas(32, 16)
    for y in range(16):
        for x in range(32):
            if x in (0, 31):
                c = "k"
            elif x in (1, 30):
                c = "m"
            else:
                step = y // 4
                c = ["h", "l", "m", "d"][step] if y % 4 else "k"
            g[y][x] = c
    return _text(g)


stamp("stairs_down_s", 2, 1, flat=[("wood", _stairs_down_s())], walk={(0, 0), (1, 0)},
      behavior={(0, 0): "MB_SOUTH_ARROW_WARP", (1, 0): "MB_SOUTH_ARROW_WARP"},
      note="the stair down to the courtyard; both cells are the exit")

# ---- Manto: the seer's room on the Kadmeia wall ---------------------------


def _cage(bird):
    """A wicker birdcage hanging from the beam on a cord, its door open: top layer."""
    g = _canvas(16, 16)
    for y in range(0, 4):
        _put(g, 8, y, "K")
    _paste(g, ["....kkkkkk....", "..kkJjJjJJkk..", ".kJ.j..j..jJk.", ".kj.j..j..jjk.", ".kJ.j..j..j.k.",
               ".kj.j..j..j.k.", ".kJ.j..j..j.k.", ".kkkkkkkkkkkk.", "..kKKKKKKKKk.."], 1, 4)
    # the open door, swung aside
    _paste(g, ["k", "J", "j", "J", "k"], 13, 7)
    for (x, y) in ((11, 7), (11, 8), (11, 9), (11, 10)):
        _put(g, x, y, ".")
    if bird == "inside":
        _paste(g, [".kk.", "kSSk", "kSSSk", ".kkk"], 5, 8)
        _put(g, 5, 9, "J")
    elif bird == "roof":
        _paste(g, ["..kk...", ".kwwk..", "kwwwwkk", ".kkkk.."], 4, 1)
        _put(g, 3, 2, "J")
    return _text(g)


stamp("cage_a", 1, 1, top=[("nature", _cage("inside"))], walk={(0, 0)},
      note="a birdcage hung from the beam, door open, a dark bird inside by choice")
stamp("cage_b", 1, 1, top=[("nature", _cage("roof"))], walk={(0, 0)},
      note="a birdcage, door open, a white dove sitting on its roof")
stamp("cage_c", 1, 1, top=[("nature", _cage(None))], walk={(0, 0)},
      note="an empty birdcage, door open: its bird is out")

def _tripod_cold():
    g = _canvas(16, 32)
    _paste(g, ["..kkkkkkkkkkkk..", ".knnmnnnmnnnnnk.", "kynnmnkknnmnnnzk", "kbyMnnnnnmnnnbzk",
               ".kbbyyyyyyyybzk.", "..kzbbbbbbbbzk..", "...kkzzzzzzkk..."], 0, 8)
    for y in range(15, 28):
        t = (y - 15) / 12
        for (x0, dx) in ((4, -3), (8, 0), (11, 3)):
            x = int(round(x0 + dx * t))
            _put(g, x - 1, y, "k")
            _put(g, x, y, "y" if dx < 0 else "b")
            _put(g, x + 1, y, "k")
    for x in (0, 1, 2, 7, 8, 9, 13, 14, 15):
        _put(g, x, 28, "k")
    return _text(g)


stamp("tripod_cold", 1, 2, art=[("bronze", _tripod_cold())],
      note="a bronze tripod over a cold brazier: the ash is old")

stamp("cornel_staff", 1, 2, art=[("bronze", """
................
................
................
...........kk...
..........kyzk..
..........kzzk..
.........kzzk...
.........kzk....
.........kzk....
........kzzk....
........kzk.....
........kzk.....
.......kzzk.....
.......kyzk.....
.......kzk......
......kzzk......
......kyzk......
......kzk.......
......kzk.......
.....kzzk.......
.....kzk........
.....kzk........
....kzzk........
....kyzk........
....kzk.........
...kzzk.........
...kzk..........
...kkk..........
................
................
................
................
""")], note="a staff of cornel wood leaning on the wall, worn black where hands held it")

stamp("feather_pots", 2, 1, art=[("clay", """
....k.....k..........k...k......
...kak...kck........kFk.kSk.....
...kak...kck........kFk.kSk.....
..kaak..kcck.......kFFk.ktSk....
..kak....kck..ka...kFk...kSk....
..kak...kcck.kaak..kYk...ktk....
...kak...kck..kak...kFk.kSk.....
....kak.kck....kak..kFkkSk......
..kkkkkkkkkk....kkkkkkkkkkkk....
.kdmmlllllmdk..kdmmllllllmdk....
.kmlhhllllmdk..kmlhhlllllmdk....
.kmllllllmmdk..kmlllllllmmdk....
..kdmmmmmmdk....kdmmmmmmmdk.....
...kkkkkkkk......kkkkkkkkk......
................................
................................
""")], note="feathers sorted into pots by color: crow, dove, kite, owl")

stamp("sky_window", 1, 2, art=[("wall", """
................
................
................
................
................
................
kkkkkkkkkkkkkkkk
k2222222222222k.
k2aaaaaaaaaaa2k.
k2aaaawaaaaaa2k.
k2aaawwwaaaaa2k.
k2aaaaaaaaaaa2k.
k2aakaaaakaaa2k.
k2akakaakakaa2k.
k2aaaaaaaaaaa2k.
k2aaaaaaaaaaa2k.
k2aaaaaaaaaaa2k.
k2aaaaaaaaaaa2k.
k2aaaaaaaaaaa2k.
k2aaaaaaaaaaa2k.
kwwwwkkwwwwwwwk.
kpppkkkkppppppk.
.ssskkksssssss..
................
""")], note="Manto's one window, open to the sky, a crow on the sill and birds far off")

# ---- Staphylos: the vintner's press-house --------------------------------


def _tread_floor():
    """The treading floor, 4x3: a stone basin raised waist-high, heaped with
    grapes (rows 0-1, walkable), and its front face with the spout (row 2)."""
    W, H = 64, 48
    flat = _canvas(W, H)
    mid = _canvas(W, H)
    for y in range(H):
        for x in range(W):
            if y < 32:
                ox, oy = min(x, W - 1 - x), y
                if ox == 0 or oy == 0:
                    c = "k"
                elif ox < 3 or oy < 3:
                    c = "5" if (ox == 1 or oy == 1) else "4"
                else:
                    c = "2"
                flat[y][x] = c
            else:
                # the front face: coursed stone, the spout in the middle
                yy = y - 32
                if x in (0, W - 1) or yy == 15:
                    c = "k"
                elif yy == 0:
                    c = "5"
                elif yy % 5 == 0 or (x + (yy // 5) * 4) % 8 == 0:
                    c = "1"
                else:
                    c = "3"
                flat[y][x] = c
    # grapes heaped inside: an 8x8 cluster of berries, repeated so it costs few tiles
    G8 = ["pPPpSpPs",
          "PsPPpPPP",
          "PPPpSpPp",
          "pPpSSSpS",
          "SpPsPpSp",
          "pPPPPPpP",
          "SpPPPpSp",
          "SSpppSSS"]
    for y in range(3, 32):
        for x in range(3, W - 3):
            mid[y][x] = G8[y % 8][x % 8]
    for (x, y) in [(5, 4), (6, 4), (58, 29), (57, 29), (4, 28)]:   # a leaf or two at the rim
        _put(mid, x, y, "g")
    # the spout: a stone lip and a thin stream of must into the vat below
    for y in range(36, 48):
        for x in (30, 31, 32, 33):
            if y < 40:
                c = "k" if x in (30, 33) else "p"
                _put(mid, x, y, c)
            else:
                _put(mid, x, y, "S" if x in (31, 32) else ".")
    return _text(flat), _text(mid)


_f, _m = _tread_floor()
stamp("tread_floor", 4, 3, flat=[("stone", _f)], art=[("nature", _m)],
      walk={(x, y) for x in range(4) for y in range(2)},
      note="the treading floor: a stone basin raised waist-high, heaped with grapes; a spout to the vat")

stamp("sunk_vat", 2, 1, flat=[("stone", """
44444444444444444444444444444444
4kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk4
k555555555555555555555555555555k
k544444444444444444444444444445k
k441111111111111111111111111144k
k441222222222222222222222222144k
k441222222222222222222222222144k
k441222222222222222222222222144k
k441222222222222222222222222144k
k441222222222222222222222222144k
k441111111111111111111111111144k
k544444444444444444444444444445k
k555555555555555555555555555555k
4kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk4
44444444444444444444444444444444
33333333333333333333333333333333
""")], art=[("nature", """
................................
................................
................................
................................
....SSSSSSSSSSSSSSSSSSSSSSSS....
....SppSSSSSSSSSSpSSSSSSSSSS....
....SSSSSSpSSSSSSSSSSSSpSSSS....
....SSSSSSSSSSSSsSSSSSSSSSSS....
....SSpSSSSSSSSSSSSSSSSSSpSS....
....SSSSSSSSSSSSSSSSSSSSSSSS....
................................
................................
................................
................................
................................
................................
""")], note="the vat sunk in the floor before the spout, dark with new must")


def _beam_press():
    """The great beam press against the back wall: 3x2 at y=1 (row 0 on the
    wall's lower course, row 1 on the floor). A lever beam pinned in the wall,
    a press bed of grape cake, a stone weight hung at its free end."""
    g = _canvas(48, 32)
    # the beam, slanting from the wall down to the right
    for x in range(2, 44):
        y0 = 5 + (x - 2) * 8 // 42
        for dy, c in enumerate("khlmdk"):
            _put(g, x, y0 + dy, c)
    # the wall socket
    _paste(g, ["kkkk", "kddk", "kmdk", "kddk", "kkkk"], 0, 4)
    # the press bed: a wide wooden trough of crushed grape cake
    for y in range(18, 30):
        for x in range(6, 30):
            if x in (6, 29) or y in (18, 29):
                c = "k"
            elif y == 19:
                c = "h"
            elif y > 26:
                c = "m"
            else:
                c = "R" if (x + y) % 4 else "r"
            _put(g, x, y, c)
    for x in range(10, 26):                     # the press board on top
        _put(g, x, 14, "k")
        _put(g, x, 15, "h")
        _put(g, x, 16, "l")
        _put(g, x, 17, "k")
    # the rope and weight at the beam's end
    for y in range(13, 20):
        _put(g, 42, y, "C")
    _paste(g, [".kkkkk.", "kmlllmk", "kllhllk", "kmlllmk", "kdmmmdk", ".kkkkk."], 39, 20)
    return _text(g)


stamp("beam_press", 3, 2, art=[("wood", _beam_press())],
      note="the beam press: a great lever pinned in the wall, the press bed, a weight on its rope")



def _pitch_jar():
    img = OA.STAMPS["amphora_plain"]["img"].copy()
    # seal the mouth with black pitch: the top rows of the jar go to soot
    from thyrsa_rooms_art import PALETTES
    k = PALETTES["clay"]["k"]
    a = PALETTES["clay"]["a"]
    m = img[..., 3] > 0
    ys, xs = m.nonzero()
    top = ys.min()
    for y in range(top, top + 5):
        for x in range(16):
            if m[y, x] and tuple(img[y, x, :3]) != k:
                img[y, x, :3] = a if y > top + 1 else k
    return img


stamp("pitch_jar", 1, 2, art=_pitch_jar(), note="a wine jar sealed with pitch")

stamp("grape_mats", 2, 1, art=[("nature", """
................................
................................
.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.
.kJjJpPpJjJjPpJjJjJpPJjJjPPpJjk.
.kjJpPsPpjJpPspjJjpPsPpjJpsPpJk.
.kJjpPPpJjJpPPpJjJjpPPJjJpPPpjk.
.kjJjppjJjJjppjJjJjjppjJjJjpjJk.
.kJjJjJjJjpPpJjJjJjJjJpPpjJjJjk.
.kjJjJpPpjpsPpJjpPpJjpPsPpjJjJk.
.kJjJpPsPjpPPpJjpsPpJjpPPpjJjJk.
.kjJjjPPpjjppjJjpPPpJjjpppJjJjk.
.kKKKKKKKKKKKKKKKKKKKKKKKKKKKKk.
.kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.
................................
................................
................................
""")], note="grapes drying to raisins on reed mats")

stamp("panther_shrine", 1, 2, art=[("bronze", """
................
................
................
................
................
................
................
.....kk.........
....kyyk..kk....
...kyYybkkyk....
..kyybbbbbybk...
..kybkkkkbbzk...
..kzk.k.kzk.k...
..kk..k..kk.....
..kkkkkkkkkkkk..
.kMMMMMMMMMMMMk.
.kmmmmmmmmmmmnk.
.kkkkkkkkkkkkkk.
..kMMMMMMMMMMk..
..kMnrrrrrrnMk..
..kMMMMMMMMMMk..
..kMnrrrrrrnMk..
..kMMMMMMMMMMk..
..kmmmmmmmmmnk..
..kmmmmmmmmmnk..
..knnnnnnnnnnk..
..kkkkkkkkkkkk..
................
................
................
................
................
""")], note="the family shrine of Dionysus: a little bronze panther on a marble altar")

# ---- Polos: the actor's narrow house --------------------------------------

stamp("costume_trunk", 2, 1, art=[("wood", """
................................
.....rr.................uU......
....rRRr...cc.....yy...uUUu.....
..kkkRRkkkkcckkkkkyykkkuUkkkk...
.kRrrrRRrcCCcccyyyyuuUUuuuUUk...
.krRRrrrrccCCcyyybyuuuUUuuuUkk..
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.
khhhhhhhhhhhhhhhhhhhhhhhhhhhhhk.
klllbllllllllllllllllllllblllldk
klllllllllkkkkkkkkllllllllllldk.
klllllllllkyybbyykllllllllllldk.
klllllllllkkkkkkkklllllllllldk..
klllbllllllllllllllllllllblllldk
kmmmmmmmmmmmmmmmmmmmmmmmmmmmmmdk
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk.
.kdk......................kdk...
""")], note="the costume trunk under the window, a king's purple and a chorus-cloak spilling out")

stamp("boot_shelf", 2, 1, art=[("wood", """
................................
................................
...kkk.....kkk......kkk.....kkk.
..krrrk...krrrk....kuuuk...kuuuk
..krRrk...krRrk....kuUuk...kuUuk
..krrrk...krrrk....kuuuk...kuuuk
..krrrkkk.krrrkkk..kuuukkk.kuuuk
..krrrrrk.krrrrrk..kuuuuuk.kuuuk
.kkdddddkkkdddddk.kkdddddkkkdddk
.khhhhhhhkkhhhhhhkkhhhhhhkkhhhhk
.kddddddddddddddddddddddddddddk.
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
khhhhhhhhhhhhhhhhhhhhhhhhhhhhhhk
kmmmmmmmmmmmmmmmmmmmmmmmmmmmmmdk
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
...kdk....................kdk...
""")], note="high-soled tragic boots, kothornoi, on a shelf: red pairs for kings, blue for gods")

stamp("bronze_mirror", 1, 2, art=[("bronze", """
................
................
.....kkkkkk.....
....kYYYYyyk....
...kYMYYyyybk...
...kYYYyyyybk...
...kYYyyyyybk...
...kyyyyyybbk...
...kyyyyybbzk...
....kyybbbzk....
.....kkkkkk.....
.......kk.......
......kyyk......
......kbbk......
.......kk.......
......kybk......
......kybk......
......kybk......
.......kk.......
......kybk......
......kybk......
.....kyybbk.....
....kyybbbzk....
...kkkkkkkkkk...
................
................
................
................
................
................
................
................
""")], note="a mirror of polished bronze on a stand: a woman-shaped handle, the face worn bright")

stamp("urn_table", 1, 1, art=[("wood", """
................
.......o.o......
......oo.o......
.......ooo......
.......kok......
......klhlk.....
.....klhhhlk....
.....klhhhlk....
.....kmlllmk....
......kmmmk.....
...kkkkkkkkkk...
..khhhhhhhhhhk..
..kmmmmmmmmmmk..
..kkkkkkkkkkkk..
...kdk....kdk...
...kkk....kkk...
""")], note="a plain clay urn on a little table by itself, a sprig of ivy on it")

# ---- Eudora: the soldier's mother -----------------------------------------


def _fig(part):
    """The old fig in Eudora's courtyard: canopy 3x2 (top layer, walkers pass
    under), trunk at the middle of the third row."""
    W, H = 48, 48
    top = _canvas(W, H)
    mid = _canvas(W, H)
    # canopy: broad fig leaves in clumps
    cx, cy = 24, 15
    for y in range(0, 32):
        for x in range(0, W):
            dx, dy = (x - cx) / 23.0, (y - cy) / 15.0
            d = dx * dx + dy * dy
            wob = 0.12 * math.sin(x * 0.9) + 0.1 * math.cos(y * 1.3)
            if d > 1.0 + wob:
                continue
            n = (x * 13 + y * 7) % 10
            lit = dx < 0.1 and dy < 0.1
            if d > 0.86 + wob:
                c = "k" if n < 7 else "G"
            elif n < 2:
                c = "G"
            elif n < 6:
                c = "g"
            else:
                c = "v" if lit else "g"
            if lit and n == 9:
                c = "V"
            top[y][x] = c
    for (x, y) in [(12, 10), (30, 8), (20, 20), (36, 18), (16, 24), (28, 26), (8, 18)]:
        _paste(top, [".kk.", "kpPk", "kPsk", ".kk."], x, y)
    # the trunk, gnarled, and the roots in the bare earth
    for y in range(24, 44):
        for x in range(19, 29):
            edge = x in (19, 28)
            c = "k" if edge else ("j" if x < 23 else "K")
            if (x + y) % 5 == 0 and not edge:
                c = "K"
            if y < 32:
                top[y][x] = c if top[y][x] == "." else top[y][x]
            else:
                mid[y][x] = c
    for (x, y) in [(16, 42), (17, 42), (18, 41), (29, 41), (30, 42), (31, 42)]:
        _put(mid, x, y, "K")
        _put(mid, x, y + 1, "k")
    return _text(top), _text(mid)


_t, _m = _fig(None)
stamp("fig_tree", 3, 3, top=[("nature", _t)], art=[("nature", _m)],
      walk={(x, y) for x in range(3) for y in range(2)} | {(0, 2), (2, 2)},
      note="the old fig in the courtyard, figs ripening purple")

stamp("turned_earth", 1, 1, flat=[("floor", """
................
................
................
....jjjjjjj.....
..jjnmnnmnnjj...
.jnmWmnnmWnmnj..
.jnnmnjmnnmnnj..
.jmnWnnmnjnmnj..
.jnmnnmnWnnmj...
..jjnmnnmnnjj...
....jjjjjjjj....
................
................
................
................
................
""")], walk={(0, 0)}, note="a patch of turned earth under the fig")

stamp("loom_cloak", 2, 3, art=recolor(OA.STAMPS["loom"]["img"], "wood", {"u": "R", "U": "r"}),
      note="Eudora's loom, a soldier's red cloak half-mended on it")

stamp("helmet_peg", 1, 1, art=[("bronze", """
.......kk.......
.......kk.......
.....kkkkkk.....
....kyYYYyyk....
...kyYyyyyybk...
...kyyyyyyybk...
..kyyyykkkbbzk..
..kyyyk...kbzk..
..kybbk..kbbzk..
..kybbk..kbzk...
...kbbzk.kbzk...
...kzzzk..kk....
....kkk.........
................
................
................
""")], note="a bronze helmet of the city's levy on a peg by the door: his father's, dusted daily")


stamp("lintel", 1, 1, top=[("wall", """
k11111111111111k
k22222222222222k
k33333333333333k
k22222222222222k
k11111111111111k
kSk..........kSk
kSk..........kSk
kSk..........kSk
kSk..........kSk
kSk..........kSk
kSk..........kSk
kSk..........kSk
kSk..........kSk
kSk..........kSk
kSk..........kSk
kSk..........kSk
""")], walk={(0, 0)}, note="the lintel and jambs of a doorway through a partition wall, over walkers")



# ---- Euthykles: the mask-maker's workshop ----------------------------------


def _heads():
    """A bench of wooden heads, each wearing a blank linen mask to dry: 2x1."""
    g = _canvas(32, 16)
    for (hx) in (2, 12, 22):
        _paste(g, ["..kkkk..", ".kcccck.", "kccccCck", "kckcckCk", "kcccccCk", "kccCcCck", ".kcCCCk.",
                   "..kccck.", "..kmmk..", ".kkmmkk."], hx, 0)
    for x in range(1, 31):
        _put(g, x, 10, "k")
        _put(g, x, 11, "h")
        _put(g, x, 12, "m")
        _put(g, x, 13, "k")
    for (x) in (2, 3, 28, 29):
        _put(g, x, 14, "d")
        _put(g, x, 15, "k")
    return _text(g)


stamp("mask_heads", 2, 1, art=[("wood", _heads())],
      note="blank linen masks drying on wooden heads")

stamp("paint_pots", 1, 1, art=[("clay", """
................
................
................
..kkkk...kkkk...
.kffffk.kYYYYk..
.kdmmdk.kdmmdk..
.kmllmk.kmllmk..
.kdmmdk.kdmmdk..
..kkkk...kkkk...
....kkkk..kkkk..
...kaaaak.kcck..
...kdmmdk.kdmk..
...kmllmk.kmlk..
...kdmmdk.kddk..
....kkkk...kk...
................
""")], note="pots of paint: red, saffron, black and white")

stamp("plaster_vat", 1, 1, art=[("clay", """
................
................
..........kk....
.........kdk....
....kkkkkdkkk...
..kkcccckdcckk..
.kcccccckdcccck.
.kccctcccdccctk.
.ktcccccccccctk.
.kdkkkkkkkkkkdk.
.kmlhhlllllmmdk.
.kmlhllllllmmdk.
.kdmllllllmmddk.
..kdmmmmmmmddk..
...kkkkkkkkkk...
................
""")], note="a pot of wet plaster with its paddle")

stamp("cutting_bench", 2, 1, art=[("wood", """
................................
................................
................................
..ccccccc......kk...............
.cCcCcCcCc....kyyk...kkkkkk.....
..ccccccc.....kbyk..kccccck.....
..........kk..kbbk..kcCCcck.....
.........kyyk..kk...kckkcck.....
kkkkkkkkkkbbkkkkkkkkkcCCCCkkkkkk
khhhhhhhhhhhhhhhhhhhhhhhhhhhhhhk
klllllllllllllllllllllllllllllmk
kmmmmmmmmmmmmmmmmmmmmmmmmmmmmmdk
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
.kdk........................kdk.
.kdk........................kdk.
.kkk........................kkk.
""")], note="the cutting bench: linen strips, bronze shears, a mask half cut")

stamp("wig_pegs", 1, 2, art=[("wood", """
................
................
................
................
................
................
.k....k....k....
.kk...kk...kk...
kddk.kcck.kRRk..
kdddkcccckRRRk..
kdkdkcCcckRkRk..
kdddkccCckRRRk..
kdkdkcccckRkRk..
kdddkcCcckRRRk..
kdk.kccCk.kRRk..
kd..kcCk...kRk..
.k...kck....kk..
......ck........
......k.........
................
................
................
................
................
................
................
................
................
................
................
................
................
""")], note="wigs on pegs: a black one, an old man's white beard, a red one for a satyr")

stamp("high_shelf", 1, 1, art=[("wood", """
................
................
................
................
................
................
................
................
................
................
................
kkkkkkkkkkkkkkkk
khhhhhhhhhhhhhhk
kmmmmmmmmmmmmmdk
.kkdk......kdkk.
...kk......kk...
""")], note="a high shelf by itself; the mask on it is a walker of its own")

# ---- Chthonia: the house of the Sown Men -----------------------------------

stamp("dragon_tooth", 2, 1, art=[("bronze", """
................................
..kk........................kk..
.kbbk......................kbbk.
.kbzkkkkkkkkkkkkkkkkkkkkkkkkzbk.
..kkMMMMMMMMMMMMMMMmmmmnnkkkkk..
...kMMMMMMMMMMMMMMmmmmmnnnk.....
....kkMMMMMMMMMMMmmmmnnnk.......
......kkMMMMMMMMmmmnnnk.........
........kkMMMMMmmmnnk...........
..........kkMMmmnnk.............
............kkmnk...............
..............kk................
................................
................................
................................
................................
""")], note="a dragon's tooth, or something very like one, as long as a forearm, over the hearth")

stamp("clay_men", 2, 1, art=[("clay", """
................................
..kk....kk....kk....kk....kk....
.kmmk..kmmk..kmmk..kmmk..kmmk...
.kmlk..kmlk..kmlk..kmlk..kmlk...
dkmmkk.kmmkkkkmmkk.kmmkkkkmmk...
dkmlmmkkmlmmkkmlmmkkmlmmkkmlmmk.
dkmmmdkkmmmdkkmmmdkkmmmdkkmmmdk.
dkmlmdkkmlmdkkmlmdkkmlmdkkmlmdk.
.kmmdk.kmmdk.kmmdk.kmmdk.kmmdk..
.kmkmk.kmkmk.kmkmk.kmkmk.kmkmk..
.kkkkk.kkkkk.kkkkk.kkkkk.kkkkk..
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
ksssssssssssssssssssssssssssssss
kSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSk
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
................................
""")], note="five little clay men, armed, on a stone shelf: the five who were left standing")
