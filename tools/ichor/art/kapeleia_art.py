"""Art for gTileset_Kapeleia: the Great Deigma's stalls and the Nursery of Nysa.

kapeleia ("the shops") is limen's art and palettes (limen_art.py), plus:
  - the market stall: a striped awning on two posts (3x2, one per colorway),
    the goods laid out under it (3x1, one per stall, the seller's middle cell
    in the top layer so the goods stand in front of the seller's legs), and
    the plank counter shared by every stall (3x1, MB_COUNTER, talked across);
  - the money-changer's trapeza, the fountain at the market's crossing, hung
    banners and heaped goods for the aisles;
  - the nursery's cradle (a liknon, the winnowing basket the nymphs laid the
    infant Dionysus in), a nest basket of Eggs, ivy hung on the wall, a fawn
    skin on the floor, a vine krater.

Each 8x8 tile takes all its colors from one of limen's seven palettes, which
ergasteria_build.py checks; pieces are drawn per palette on Canvases and laid
over each other (comp below). The palettes are all full, so every new piece
draws from the colors already there.
"""
import copy

import numpy as np

import limen_art as LA
from char_canvas import Canvas

PALETTES = copy.deepcopy(LA.PALETTES)
PALETTE_ORDER = LA.PALETTE_ORDER
FLOORS = LA.FLOORS
WALLS = LA.WALLS
VOID = LA.VOID
RUGS = LA.RUGS
grid = LA.grid
hflip = LA.hflip

# limen's pieces the market and the nursery reuse.
SHARED = ["window", "column", "amphora", "amphora_plain", "pithos", "sack", "crate", "crate_stack",
          "scales", "notice_board", "mat", "bench", "stool", "table", "kline", "loom", "hearth", "soot",
          "honey_shelf", "jar_shelf", "herbs", "myrtle", "kalathos", "krater", "water_jar", "lampstand",
          "trestle_wool", "trestle_oil", "trestle_grain", "trestle_lamps", "amphora_rack", "chest",
          "counter_plank", "dolphin_mosaic", "pots", "klismos_l", "klismos_r", "table_round"]
STAMPS = {k: dict(LA.STAMPS[k], source="limen") for k in SHARED}


def comp(w, h, *layers):
    """Lay (palette, Canvas or text) layers over each other into one RGBA image."""
    out = np.zeros((h, w, 4), np.uint8)
    for pal, art in layers:
        img = grid(pal, art.text() if isinstance(art, Canvas) else art, w, h)
        m = img[..., 3] > 0
        out[m] = img[m]
    return out


def stamp(name, img, w, h, pal="wood", top=None, walk=(), behavior=None, flatten=False, note=""):
    """oikia's stamp contract: img and top are RGBA (h*16, w*16)."""
    assert img.shape[:2] == (h * 16, w * 16), f"{name}: art is {img.shape[:2]}, want {(h * 16, w * 16)}"
    if top is not None:
        assert top.shape[:2] == img.shape[:2], f"{name}: top is {top.shape[:2]}"
    STAMPS[name] = {"pal": pal, "img": img, "top": top, "w": w, "h": h, "walk": set(walk),
                    "behavior": dict(behavior or {}), "flatten": flatten, "note": note, "source": "kapeleia"}


def split_cell(img, cx, cy):
    """img with one cell cut out, and that cell alone (for the top layer)."""
    a, b = img.copy(), np.zeros_like(img)
    sl = (slice(cy * 16, cy * 16 + 16), slice(cx * 16, cx * 16 + 16))
    b[sl] = a[sl]
    a[sl] = 0
    return a, b


# ===========================================================================
# The market stall
# ===========================================================================
# Three cells wide. The awning (rows 0-1) is a striped canopy on two posts; the
# goods row stands on the counter's slab; the counter (MB_COUNTER) is the same
# planks for every stall, so a player talks across it to the seller standing
# in the goods row's middle cell. Colorways: (main, dark, lit, white, shade).

COLORWAYS = {
    "red": ("r", "R", "o", "c", "C"),
    "blue": ("u", "i", "U", "c", "C"),
    "purple": ("P", "p", "q", "c", "C"),
    "saffron": ("y", "o", "c", "c", "C"),
    "green": ("g", "n", "g", "c", "C"),
}


def _awning(colorway):
    main, dark, lit, white, shade = COLORWAYS[colorway]
    cl = Canvas(48, 32)            # cloth: the canopy and the valance (rows 0-23)
    wd = Canvas(48, 32)            # wood: the posts under it (rows 24-31)

    def stripe(x):
        return (x % 8) in (2, 3, 4, 5)
    # the canopy, seen from the front and a little above: a lit top edge,
    # stripes, a shaded belly, then the valance with its scalloped hem
    for y in range(3, 13):
        for x in range(1, 47):
            if stripe(x):
                ch = lit if y == 3 else dark if y >= 11 else main
            else:
                ch = white if y < 11 else shade
            cl.put(x, y, ch)
    cl.hline(2, 45, 2, "k")
    cl.put(1, 3, "k")
    cl.put(46, 3, "k")
    cl.vline(0, 4, 12, "k")
    cl.vline(47, 4, 12, "k")
    cl.hline(0, 47, 13, "k")
    # the valance: deeper color, a hem of tabs every 4 px
    for y in range(14, 20):
        for x in range(1, 47):
            cl.put(x, y, dark if stripe(x) else shade)
    cl.hline(1, 46, 14, "k" if colorway in ("saffron",) else dark)
    for x in range(1, 47):
        if stripe(x):
            cl.put(x, 15, main)
    cl.vline(0, 14, 19, "k")
    cl.vline(47, 14, 19, "k")
    for x in range(0, 48):
        tab = (x // 4) % 2 == 0
        if tab:
            cl.put(x, 20, dark if stripe(x) else shade)
            cl.put(x, 21, "k")
        else:
            cl.put(x, 20, "k")
    for x in (0, 47):
        cl.put(x, 20, "k")
        cl.put(x, 21, ".")
    # the posts: turned wood, a bronze ring under the valance
    for px in (2, 44):
        wd.vline(px - 1, 24, 31, "k")
        wd.vline(px + 2, 24, 31, "k")
        wd.vline(px, 24, 31, "m")
        wd.vline(px + 1, 24, 31, "d")
        wd.hline(px, px + 1, 24, "b")
        wd.hline(px, px + 1, 25, "z")
    return comp(48, 32, ("cloth", cl), ("wood", wd))


def _posts(c):
    """The two posts down the goods row (wood), at the row's outer tiles."""
    for px in (2, 44):
        c.vline(px - 1, 0, 15, "k")
        c.vline(px + 2, 0, 15, "k")
        c.vline(px, 0, 15, "m")
        c.vline(px + 1, 0, 15, "d")


COUNTER = """
kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
khhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhk
kllllllllllllllllllllllllllllllllllllllllllllllk
kdddddddddddddddddddddddddddddddddddddddddddddddk
kmmlmmmmmmmmdmmmmmmmmmmmdmmmmmmmmmmmdmmmmmmmlmmk
kmmlmmmmmmmmdmmmmmmmmmmmdmmmmmmmmmmmdmmmmmmmlmmk
kmmlmmmmmmmmdmmmmmmmmmmmdmmmmmmmmmmmdmmmmmmmlmmk
kmmlmmmmmmmmdmmmmmmmmmmmdmmmmmmmmmmmdmmmmmmmlmmk
kddlddddddddkddddddddddddddddddddddkddddddddlddk
kmmlmmmmmmmmdmmmmmmmmmmmdmmmmmmmmmmmdmmmmmmmlmmk
kmmlmmmmmmmmdmmmmmmmmmmmdmmmmmmmmmmmdmmmmmmmlmmk
kmmlmmmmmmmmdmmmmmmmmmmmdmmmmmmmmmmmdmmmmmmmlmmk
kmmlmmmmmmmmdmmmmmmmmmmmdmmmmmmmmmmmdmmmmmmmlmmk
kdddddddddddddddddddddddddddddddddddddddddddddddk
kdkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkdk
.kk............................................kk.
"""


def _counter():
    rows = [r[:48] for r in COUNTER.strip("\n").split("\n")]
    return comp(48, 16, ("wood", "\n".join(rows)))


for _cw in COLORWAYS:
    stamp(f"awning_{_cw}", _awning(_cw), 3, 2, pal="cloth",
          note=f"a stall's awning, {_cw} and white stripes on two posts")
stamp("stall_counter", _counter(), 3, 1,
      behavior={(0, 0): "MB_COUNTER", (1, 0): "MB_COUNTER", (2, 0): "MB_COUNTER"},
      note="a stall's plank counter, talked across to the seller behind it")


def goods(name, layers, note):
    """A stall's goods row (3x1): the posts, and the goods in x 8-39 of 48
    (one palette per 8x8 tile). The middle cell goes in the top layer, over
    the seller's legs; the seller stands there (walkable)."""
    wd = Canvas(48, 16)
    _posts(wd)
    img = comp(48, 16, ("wood", wd), *layers)
    side, mid = split_cell(img, 1, 0)
    stamp(name, side, 3, 1, top=mid, walk=[(1, 0)], note=note)


# --- the goods, drawn on 48x16 (x 8-39 used) --------------------------------

def _phoenician():
    """Tyrian purple folded in bolts, murex shells, blown glass, a cedar log."""
    cl = Canvas(48, 16)
    for (y, a, b, d) in ((10, "P", "q", "p"), (5, "p", "P", "p")):
        cl.box(8, y, 15, y + 5, a)
        cl.hline(9, 14, y + 1, b)
        cl.hline(9, 14, y + 4, d)
    cl.paste(["kqqk", "kPPk", "kPPk", "kppk", ".kk."], 11, 0)        # a hank of purple yarn on top
    # murex shells (x 16-23), spiny, the dye's source
    for (x, y) in ((16, 9), (19, 4), (19, 10)):
        cl.paste(["..k...",
                  ".kckk.",
                  "kcCcck",
                  "kCcCck",
                  ".kcCk.",
                  "..kk.."], x, y)
    br = Canvas(48, 16)
    # Sidonian glass (x 24-31): a tall flask and a little aryballos
    br.paste(["..kk..",
              "..ka..",
              "..kU..",
              ".kUak.",
              "kUuUak",
              "kUuuUk",
              "kuuuUk",
              "kuuuuk",
              ".kuuk.",
              "..kk.."], 24, 5)
    br.paste([".kk.",
              "kaUk",
              "kUuk",
              ".kk."], 29, 11)
    br.paste([".kk.", "kMak", ".kk."], 29, 6)
    wd = Canvas(48, 16)
    # Lebanese cedar (x 32-39): two logs, end on
    for (x, y) in ((32, 9), (35, 4)):
        wd.paste([".kkkk.",
                  "khlhlk",
                  "klhmlk",
                  "khmhlk",
                  ".kkkk."], x, y)
    wd.paste(["kk", "kd", "kk"], 38, 10)
    return [("cloth", cl), ("bronze", br), ("wood", wd)]


def _egyptian():
    """Papyrus rolls, a blue faience scarab and amulets, alabaster jars."""
    wd = Canvas(48, 16)
    # papyrus (x 8-15): rolls tied with red cord, one opened
    for (y,) in ((10,), (5,)):
        wd.paste(["kkkkkkkk",
                  "kccccCck",
                  "kcCcrcCk",
                  "kccccCck",
                  "kkkkkkkk"], 8, y)
    wd.paste(["..kk....", ".kCck...", "kccCk..."], 8, 0)
    cl = Canvas(48, 16)
    # faience (x 16-23): a scarab, blue-green, and a strand of beads
    cl.paste(["..kkkk..",
              ".kUuuUk.",
              "kuUUUuuk",
              "kuiUUiuk",
              "kuUuuUuk",
              ".kuiiuk.",
              "k.kkkk.k"], 16, 8)
    cl.paste(["kUkukUku", ".k.k.k.k"], 16, 4)
    br = Canvas(48, 16)
    # alabaster (x 24-39): a tall alabastron and a wide jar of kohl, a lid
    br.paste(["..kkk..",
              ".kMMMk.",
              "..kmk..",
              ".kMMmk.",
              "kMMmmnk",
              "kMMmmnk",
              "kMMmmnk",
              "kMMmmnk",
              "kMmmmnk",
              ".kMmnk.",
              "..kkk.."], 24, 4)
    br.paste([".kkkkkk.",
              "kMMMMmnk",
              "kkkkkkkk",
              "kMmmmmnk",
              "kMmmmmnk",
              ".kmmmnk."], 31, 9)
    br.paste(["kYk", ".k."], 34, 7)
    return [("wood", wd), ("cloth", cl), ("bronze", br)]


def _scythian():
    """Furs from the steppe, a gold stag plaque, a bow case of red leather."""
    cl = Canvas(48, 16)
    # furs (x 8-23): a white fox pelt over a brown bear's
    cl.paste(["..kkkkkkkkkkkk..",
              ".knnCnnnnnCnnnk.",
              "knnnnnnCnnnnnnnk",
              "knCnnnnnnnnCnnnk",
              "knnnnnCnnnnnnnnk",
              ".kknnnnnnnnnnkk.",
              "...kkkkkkkkkk..."], 8, 9)
    cl.paste(["..kkkkkkkk......",
              ".kccCccccCkk....",
              "kccccCccccccCk..",
              "kCccccccCccccck.",
              ".kkcccccccccckk.",
              "...kkkkkkkkkkk.."], 8, 4)
    cl.paste(["kk", "kc"], 22, 4)
    br = Canvas(48, 16)
    # Scythian gold (x 24-31): a curled stag plaque on a stand
    br.paste(["k..k.k..",
              ".kykyk..",
              "..kYk...",
              ".kyyyk..",
              "kyYyybk.",
              "kybyyybk",
              ".kbk.kbk",
              "..k...k.",
              "..kkkk..",
              ".kzbbzk.",
              ".kkkkkk."], 24, 3)
    wd = Canvas(48, 16)
    # the gorytos (x 32-39): a bow case with arrows, studded with bronze
    wd.paste([".k.k.k..",
              "kckckck.",
              ".kRkRk..",
              "kkkkkkk.",
              "krrbrrk.",
              "krRrRrk.",
              "krrbrrk.",
              "krRrRrk.",
              "krrbrrk.",
              ".krrrk..",
              "..kkk..."], 32, 3)
    return [("cloth", cl), ("bronze", br), ("wood", wd)]


def _stones():
    """Evolution stones on a cloth: Fire, Sun, Water, Thunder, Leaf, Moon."""
    cy = Canvas(48, 16)
    cy.paste(["..kk..",
              ".kFYk.",
              "kfFFFk",
              "kffFfk",
              ".kffk.",
              "..kk.."], 9, 9)                     # Fire
    cy.paste([".k..k.",
              "..kk..",
              ".knnk.",
              "knFnnk",
              ".knnk.",
              "..kk.."], 9, 2)                     # Sun
    br = Canvas(48, 16)
    br.paste(["..kk..",
              ".kaUk.",
              "kUUuuk",
              "kUuuuk",
              ".kuuk.",
              "..kk.."], 17, 9)                    # Water
    br.paste(["..kkk.",
              ".keek.",
              "keyk..",
              ".kyyk.",
              "..kyk.",
              "...k.."], 18, 2)                    # Thunder
    nt = Canvas(48, 16)
    nt.paste(["...kk.",
              "..kVgk",
              ".kVgGk",
              "kvgGk.",
              "kgGk..",
              ".kk..."], 25, 9)                    # Leaf
    br.paste(["..kk..",
              ".kMmk.",
              "kMmmnk",
              "kmmnnk",
              ".knnk.",
              "..kk.."], 33, 9)                    # Moon
    br.paste([".kkk..",
              "kmMmk.",
              "kmmnk.",
              ".kkk.."], 33, 3)                    # a dull Everstone
    nt.paste(["kk..", "kJk.", ".kk."], 26, 3)
    return [("clay", cy), ("bronze", br), ("nature", nt)]


def _tablets():
    """The techniques seller's goods: wax tablets written over, a stylus,
    a scroll case, and a little bronze sphere for teaching the stars."""
    wd = Canvas(48, 16)
    for (x, y) in ((8, 8), (12, 3), (24, 8)):
        wd.paste(["kkkkkkkk",
                  "kdmmmmdk",
                  "kmkkkkmk",
                  "kmmmmmmk",
                  "kmkkkmmk",
                  "kdmmmmdk",
                  "kkkkkkkk"], x, y)
    wd.paste(["k", "y", "b", "z", "k"], 22, 9)          # the stylus
    wd.paste(["..kkkk..",
              ".kRrrRk.",
              ".krrrrk.",
              ".kbbbbk.",
              ".krrrrk.",
              ".kRrrRk.",
              "..kkkk.."], 32, 8)                       # a scroll case
    br = Canvas(48, 16)
    br.paste(["..kkk...",
              ".kyYbk..",
              "kyzbybk.",
              "kbybzbk.",
              ".kbbbk..",
              "..kzk...",
              ".kkkkk.."], 32, 0)                       # the sphere on its stand
    return [("wood", wd), ("bronze", br)]


def _berries():
    """Baskets heaped with berries: Oran blue, Pecha pink, Cheri red, Sitrus."""
    nt = Canvas(48, 16)
    cl = Canvas(48, 16)
    cy = Canvas(48, 16)
    for x in (8, 16, 24, 32):
        nt.paste(["kkkkkkkk",
                  "kJjJjJjk",
                  "kjKjKjKk",
                  "kjjjjjjk",
                  ".kjKjjk.",
                  ".kkkkkk."], x, 8)
    # the heaps sit in the upper tile row, one palette per basket
    cl.paste(["...kk...", "..kUUk..", ".kUuUuk.", "kuUuuUuk", "kuuiuuik", ".kuuuuk."], 8, 2)   # Oran
    cl.paste(["...kk...", "..kqqk..", ".kqPqPk.", "kPqPPqPk", "kPPpPPpk", ".kPPPPk."], 16, 2)  # Pecha
    cy.paste(["...kk...", "..kFFk..", ".kfFfFk.", "kfFffFfk", "kffdffdk", ".kffffk."], 24, 2)  # Cheri
    cy.paste(["...kk...", "..kYYk..", ".kYnYnk.", "knYnnYnk", "knnFnnFk", ".knnnnk."], 32, 2)  # Sitrus
    return [("nature", nt), ("cloth", cl), ("clay", cy)]


def _curios():
    """The rare stall: an open chest of gold, a blue glass egg on a cushion,
    a peacock's feather (Hera's bird), and a sealed little jar."""
    wd = Canvas(48, 16)
    wd.paste(["kkkkkkkkkkkkkkkk",
              "kmmmmmmbbmmmmmmk",
              "kmllllmbbmlllllk",
              "kmmmmmmbbmmmmmmk",
              "kmmmmmmyymmmmmmk",
              "kdmmmmmbbmmmmmdk",
              "kddddddddddddddk",
              "kkkkkkkkkkkkkkkk"], 8, 8)              # the chest
    br = Canvas(48, 16)
    br.paste(["...kk.kk.kk.kk..",
              "..kYykYykyYkYyk.",
              ".kyyykyykyyykyyk",
              "kybyybyybyybyybk",
              "kbbbbbbbbbbbbbbk"], 8, 3)              # gold heaped in it
    br.paste(["..kk..",
              ".kaUk.",
              "kUaUuk",
              "kUUuuk",
              "kuUuuk",
              ".kuuk."], 25, 2)                       # a glass egg
    cl = Canvas(48, 16)
    cl.paste(["kkkkkkkk", "krrorrrk", "kRRRRRRk", "kRrrrrRk", ".kkkkkk."], 24, 8)   # its cushion
    cl.paste(["..kk....",
              ".kgUk...",
              "kgUiuk..",
              "kgiugk..",
              ".kgUgk..",
              "..kggk..",
              "...kgk..",
              "....kgk.",
              ".....kk."], 32, 0)                      # the feather
    cl.paste(["..kk", ".kCk", "kcCk", "kcck", ".kk."], 35, 10)
    return [("wood", wd), ("bronze", br), ("cloth", cl)]


goods("goods_phoenician", _phoenician(), "Tyrian purple, murex shells, Sidonian glass, cedar")
goods("goods_egyptian", _egyptian(), "papyrus, a faience scarab and beads, alabaster jars")
goods("goods_scythian", _scythian(), "furs, a gold stag plaque, a red bow case")
goods("goods_stones", _stones(), "evolution stones laid out: Fire, Sun, Water, Thunder, Leaf, Moon")
goods("goods_tablets", _tablets(), "wax tablets, a stylus, a scroll case, a bronze star sphere")
goods("goods_berries", _berries(), "baskets of Oran, Pecha, Cheri and Sitrus berries")
goods("goods_curios", _curios(), "an open chest of gold, a glass egg, a peacock feather, a jar")


def _spices():
    """Spices from Lydia and Arabia heaped in shallow bowls: saffron, sumac,
    cumin, salt, and a sack of peppercorns."""
    cl = Canvas(48, 16)
    cy = Canvas(48, 16)
    nt = Canvas(48, 16)
    heaps = ((8, cl, "y", "o"), (16, cl, "r", "R"), (24, cy, "l", "m"), (32, cy, "c", "t"))
    for x, c, a, b in heaps:
        c.paste(["..kkkk..",
                 ".k" + a * 4 + "k.",
                 "k" + a + b + a * 3 + b + "k",
                 "k" + b + a * 4 + b + "k"], x, 4)
    for x in (8, 16, 24, 32):
        nt.paste(["kkkkkkkk", "kJjJjJjk", "kjKjjKjk", ".kkkkkk."], x, 8)
    nt.paste(["k.k", ".k."], 11, 12)
    return [("cloth", cl), ("clay", cy), ("nature", nt)]


def _pottery():
    """Athenian pots for sale: a black-figure amphora, a red-figure cup,
    a lekythos and a stack of plates."""
    cy = Canvas(48, 16)
    cy.paste(["..k.k..",
              ".kakak.",
              "..kak..",
              ".kaaak.",
              "kammlak",
              "kamllak",
              "kaamaak",
              ".kaaak.",
              "..kak..",
              ".kkkkk."], 8, 5)
    cy.paste(["kkkkkkkk", "kaammaak", ".kaaaak.", "..kaak..", "..kkkk.."], 16, 10)
    cy.paste(["..kk..", ".kmmk.", ".kllk.", ".kmmk.", "kmmmmk", "kmllmk", "kmmmmk", ".kmmk.", ".kkkk."],
             17, 1)
    cy.paste(["..k..", ".kck.", ".kak.", "kaaak", "kacak", "kaaak", ".kak.", ".kkk."], 26, 7)
    for y in (13, 11, 9, 7):
        cy.paste(["kkkkkkk", "kmlllmk"], 32, y)
    return [("clay", cy)]


goods("goods_spices", _spices(), "saffron, sumac, cumin and salt heaped in bowls")
goods("goods_pottery", _pottery(), "Athenian pots: a black-figure amphora, a cup, a lekythos, plates")


# ===========================================================================
# The money-changer's trapeza: the bench every Greek bank was named for. Its
# top carries the coin stacks and the touchstone (top layer over the
# changer's legs in the middle), its front is the counter.
# ===========================================================================

def _trapeza():
    wd = Canvas(48, 32)
    rows = [r[:48] for r in COUNTER.strip("\n").split("\n")]
    wd.paste(rows, 0, 16)
    _posts_short = None  # noqa: F841
    br = Canvas(48, 32)
    # stacks of coins: bronze obols, silver owls, gold staters (x 8-39, y 4-15)
    for (x, h, a, b) in ((8, 4, "z", "b"), (12, 6, "z", "b"), (17, 5, "n", "m"), (21, 7, "n", "M"),
                         (26, 3, "b", "y"), (30, 6, "b", "Y")):
        for i in range(h):
            y = 15 - i * 2
            br.paste(["kkkk", "k" + a + b + "k"], x, y - 1)
        br.paste([".kk.", "k" + b + b + "k"], x, 15 - h * 2 - 1)
    # the touchstone and a heap of loose coins
    br.paste(["..kk...", ".kYyk..", "kyybyk.", "kkkkkkk"], 33, 12)
    cy = Canvas(48, 32)
    cy.paste(["kkkkkk", "kssSsk", "ksSssk", "kkkkkk"], 41, 11)  # the touchstone, black basanite
    img = comp(48, 32, ("wood", wd), ("bronze", br), ("clay", cy))
    side, mid = split_cell(img, 1, 0)
    return side, mid


_tz, _tz_top = _trapeza()
stamp("trapeza", _tz, 3, 2, top=_tz_top, walk=[(1, 0)],
      behavior={(0, 1): "MB_COUNTER", (1, 1): "MB_COUNTER", (2, 1): "MB_COUNTER"},
      note="the money-changer's trapeza: coin stacks of bronze, silver and gold, a touchstone")


# ===========================================================================
# The fountain at the market's crossing (3x2): a marble basin, a lion's
# head spout on a pillar, the water falling.
# ===========================================================================

def _fountain():
    br = Canvas(48, 32)
    # the basin, an oval seen from above and in front
    br.ellipse(24, 19, 23, 10, "m")
    br.ellipse(24, 18.5, 21, 8, "M")
    br.ellipse(24, 19, 18, 6, "u")
    br.ellipse(24, 18.5, 16, 4.5, "U")
    br.fill_where(lambda x, y: br.get(x, y) == "U" and (x * 3 + y * 5) % 11 == 0, "a")
    br.fill_where(lambda x, y: br.get(x, y) == "m" and y > 24, "n")
    br.outline("k", solid=lambda ch: ch != ".")
    # the pillar and its lion head
    br.rect(21, 2, 26, 15, "M")
    br.vline(25, 2, 15, "m")
    br.vline(26, 2, 15, "n")
    br.vline(20, 1, 15, "k")
    br.vline(27, 1, 15, "k")
    br.hline(20, 27, 1, "k")
    br.paste(["kyyyyk", "kybbyk", "kzkkzk", ".kyyk.", "..kk.."], 21, 3)
    # the jet, falling into the basin
    br.vline(23, 8, 15, "a")
    br.vline(24, 8, 15, "U")
    br.paste(["a.a", ".a."], 22, 16)
    return comp(48, 32, ("bronze", br))


stamp("fountain", _fountain(), 3, 2, pal="bronze",
      note="the market's fountain: a marble basin under a lion's head spout")


# ===========================================================================
# Banners on the wall (1x2), one per stall's colorway, with a sign of its goods
# ===========================================================================

BANNER_SIGNS = {
    "purple": ["..kk..", ".kcck.", "kccCck", ".kCCk.", "..kk.."],         # a murex
    "blue": ["..kk..", ".kcck.", "kcckck", "kcckck", ".kcck.", "..kk.."],  # an eye
    "red": ["k....k", ".k..k.", "..kk..", ".kcck.", "kcccck"],              # a stag's antlers
    "saffron": ["..kk..", ".kcck.", "kcckck", ".kcck.", "..kk.."],         # a stone
    "green": [".kk.kk", "kcckcc", "kcccck", ".kcck.", "..kk.."],            # a leaf pair
}


def _banner(cw):
    main, dark, lit, white, shade = COLORWAYS[cw]
    cl = Canvas(16, 32)
    cl.hline(2, 13, 2, "k")                                   # the rod
    cl.box(3, 3, 12, 24, main)
    cl.vline(11, 4, 23, dark)
    cl.vline(4, 4, 23, lit)
    for x in range(3, 13):
        cl.put(x, 25 + (x % 2), main if x % 2 == 0 else dark)
    cl.outline("k", solid=lambda ch: ch != "." and ch != "k")
    cl.paste(BANNER_SIGNS[cw], 5, 10)
    cl.hline(1, 14, 2, "n")
    cl.hline(1, 14, 1, "k")
    cl.put(1, 3, "k")
    cl.put(14, 3, "k")
    return comp(16, 32, ("cloth", cl))


for _cw in COLORWAYS:
    stamp(f"banner_{_cw}", _banner(_cw), 1, 2, pal="cloth", note=f"a {_cw} banner hung on the wall")


# ===========================================================================
# Goods heaped in the aisles
# ===========================================================================

def _baskets_floor():
    """Two wicker baskets on the floor, one of figs, one of onions."""
    nt = Canvas(32, 16)
    for x in (1, 17):
        nt.paste(["kkkkkkkkkkkkk",
                  "kJjJjJjJjJjJk",
                  "kjKjKjKjKjKjk",
                  ".kjjjjjjjjjk.",
                  ".kKjjjjjjjKk.",
                  "..kkkkkkkkk.."], x, 10)
    nt.paste(["..kpkpk..", ".kpppppk.", "kpGpppGpk"], 3, 7)        # figs
    nt.paste(["..kwkwk..", ".kwwVwwk.", "kwVwwwVwk"], 19, 7)       # onions
    return comp(32, 16, ("nature", nt))


stamp("baskets_floor", _baskets_floor(), 2, 1, pal="nature", note="baskets of figs and onions on the floor")


def _bales():
    """Wool bales roped up, a sack on top (2x2)."""
    cl = Canvas(32, 32)
    for (x, y) in ((1, 16), (16, 16), (8, 4)):
        cl.box(x, y, x + 14, y + 13, "c")
        cl.vline(x + 13, y + 1, y + 12, "C")
        cl.hline(x + 1, x + 12, y + 12, "C")
        cl.vline(x + 5, y + 1, y + 12, "n")
        cl.hline(x + 1, x + 12, y + 6, "n")
    return comp(32, 32, ("cloth", cl))


stamp("bales", _bales(), 2, 2, pal="cloth", note="bales of raw wool, roped")


def _carpet_roll():
    """Rolled carpets stood on end against the wall, and one unrolled (1x2)."""
    cl = Canvas(16, 32)
    for (x, a, b) in ((1, "r", "o"), (6, "u", "y"), (11, "P", "c")):
        cl.box(x, 4 + (x % 3), x + 4, 30, a)
        for y in range(6 + (x % 3), 30, 4):
            cl.hline(x + 1, x + 3, y, b)
        cl.paste(["kkkkk", "k" + b + "k" + b + "k"], x, 3 + (x % 3))
    return comp(16, 32, ("cloth", cl))


stamp("carpets_rolled", _carpet_roll(), 1, 2, pal="cloth", note="rolled carpets stood on end")


# ===========================================================================
# The Nursery of Nysa
# ===========================================================================

def _liknon():
    """The liknon: a winnowing basket, the cradle the nymphs laid the infant
    god in. Here it holds a swaddled Egg (2x1)."""
    nt = Canvas(32, 16)
    nt.paste(["......kkkkkkkkkkkkkkkkk.......",
              "...kkkJjJjJjJjJjJjJjJjJkkk....",
              ".kkJjJjjjjjjjjjjjjjjjjjjJjJkk.",
              "kJjjKjjjjjjjjjjjjjjjjjjjjKjjJk",
              "kjjKjjjjjjjjjjjjjjjjjjjjjjKjjk",
              "kJjKjjjjjjjjjjjjjjjjjjjjjjjKjk",
              ".kjjKKjjjjjjjjjjjjjjjjjjjKKjk.",
              "..kkjjKKKKKKKKKKKKKKKKKKKjjkk.",
              "....kkkkkkkkkkkkkkkkkkkkkkk..."], 1, 6)
    nt.paste(["..kkkkkk..",
              ".kwwwwwwk.",
              "kwwVwwwVwk",
              "kwwwwVwwwk",
              ".kwwwwwwk."], 10, 4)                     # the Egg, swaddled in fleece
    return comp(32, 16, ("nature", nt))


stamp("liknon", _liknon(), 2, 1, pal="nature", note="the liknon: a winnowing-basket cradle with an Egg in it")


def _nest_basket():
    """A low basket of straw with Eggs in it, waiting for their trainers (1x1)."""
    nt = Canvas(16, 16)
    nt.paste(["..kk..kk..kk..",
              ".kwwkkwVkkwwk.",
              "kwVwwkwwkwwVwk",
              "kJjJjJjJjJjJjk",
              "kjKjjjKjjjKjjk",
              ".kjjjjjjjjjjk.",
              "..kkkkkkkkkk.."], 1, 7)
    return comp(16, 16, ("nature", nt))


stamp("nest_basket", _nest_basket(), 1, 1, pal="nature", note="a straw basket of Eggs")


def _ivy():
    """Ivy hung along the wall in a swag, Dionysus's plant (2x1, nature)."""
    nt = Canvas(32, 16)
    for x in range(0, 32):
        y = 3 + int(3 * abs(((x / 31.0) - 0.5) * 2) ** 0 * (1 - abs((x - 15.5) / 15.5)))
        nt.put(x, y, "K")
    for (x, y, big) in ((1, 2, 1), (5, 4, 0), (9, 5, 1), (14, 6, 0), (18, 6, 1), (23, 5, 0),
                        (27, 4, 1), (30, 2, 0)):
        if big:
            nt.paste([".kk.", "kvgk", "kgGk", ".kk."], x - 1, y)
        else:
            nt.paste([".k.", "kgk", ".k."], x - 1, y + 1)
    nt.paste([".k.", "kpk", "kpk", ".k."], 15, 9)              # a hanging bunch
    nt.paste([".k.", "kpk", ".k."], 16, 12)
    return comp(32, 16, ("nature", nt))


stamp("ivy", _ivy(), 2, 1, pal="nature", note="a swag of ivy along the wall, a bunch of grapes")


def _nebris():
    """A fawn skin spread on the floor, the maenads' cloak (2x2, flattened)."""
    cl = Canvas(32, 32)
    cl.ellipse(16, 16.5, 10, 12, "C")
    for (x0, y0, x1, y1) in ((8, 8, 3, 3), (24, 8, 29, 3), (8, 25, 3, 30), (24, 25, 29, 30)):
        cl.line(x0, y0, x1, y1, "C")
        cl.line(x0 + 1, y0, x1 + 1, y1, "C")
    cl.ellipse(16, 4, 3, 2.5, "C")                             # the head, flat
    cl.vline(16, 6, 27, "o")                                   # the dark stripe down the back
    for (x, y) in ((11, 10), (20, 9), (13, 15), (21, 16), (11, 21), (19, 22), (16, 12), (15, 19)):
        cl.put(x, y, "c")
        cl.put(x + 1, y, "c")
    cl.outline("n", solid=lambda ch: ch in "Cco")
    return comp(32, 32, ("cloth", cl))


stamp("nebris", _nebris(), 2, 2, pal="cloth", walk=[(0, 0), (1, 0), (0, 1), (1, 1)],
      note="a dappled fawn skin on the floor")


def _thyrsos_rack():
    """Thyrsoi against the wall: fennel staffs tipped with pine cones (1x2)."""
    nt = Canvas(16, 32)
    for x in (3, 8, 12):
        nt.vline(x, 9, 30, "J")
        nt.vline(x + 1, 9, 30, "K")
        nt.paste([".k.", "kJk", "kjk", "kKk", ".k."], x - 1, 3 + (x % 3))
        nt.paste(["kgk", ".v."], x - 1, 8 + (x % 3))
    return comp(16, 32, ("nature", nt))


stamp("thyrsoi", _thyrsos_rack(), 1, 2, pal="nature", note="thyrsoi, ivy-wound staffs tipped with pine cones")
