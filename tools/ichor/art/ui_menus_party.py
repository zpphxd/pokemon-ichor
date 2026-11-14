#!/usr/bin/env python3
"""Draw Ichor's party menu: clay plaques on a terracotta field.

Each party slot is a parchment plaque set in a clay rim with an ink outline,
like the panels of the dialogue box. The highlighted slot glows sun-gold, a
fainted one goes ashen, and a slot picked to switch takes an Aegean rim. HP
bars keep the battle meaning: olive green, sun-gold, then red.

How the engine paints the slots (src/party_menu.c, src/data/party_menu.h):
  - Slot frames are tiles of bg.png, blitted into each slot's window by the
    byte maps slot_*.bin (no flips). Every slot window starts as a copy of BG
    palette 3; state changes then load single colors from the 11 palettes of
    bg.png into window colors 1, 4-8 (frame and face), 9-10 (HP fill) and
    11-12 (gender). Text is color 3 with shadow 2; the empty part of the HP
    bar is 13 over 2.
  - The Cancel button is BG tiles drawn in palette 1, swapped to palette 2
    while selected. An empty slot loads colors 1, 11 and 12 from palette 1.

Writes, in graphics/party_menu/:
  bg.png, bg.bin            tiles (<= 62, see graphics.c), 11 palettes, BG1 map
  slot_*.bin                slot frames
  cancel_button.bin, confirm_button.bin
  pokeball.png, pokeball_small.png   the slot's ball, painted black-figure
  hold_icons.png            held item and mail badges

Usage: python3 tools/ichor/art/ui_menus_party.py
"""
import numpy as np

from ui_menus_lib import *

OUT = ROOT / "graphics/party_menu"
IMG = ROOT / "design/phase1/img"

RING = (160, 72, 40)
FACE_LIGHT = (248, 240, 208)

# --- Palettes ---------------------------------------------------------------
# Slot window colors, as LoadPartyBoxPalette and friends use them.
S_OUT, S_SHADOW, S_TEXT, S_FACE_HI, S_FACE, S_FACE_LO, S_INCISE, S_RIM = 1, 2, 3, 4, 5, 6, 7, 8
S_HP, S_HP_HI, S_G1, S_G2, S_EMPTY_HI, S_GOLD, S_GOLD_DARK = 9, 10, 11, 12, 13, 14, 15

SLOT = [
    TRANSPARENT,   # 0
    INK,           # 1  outline (state)
    PARCH_SHADE,   # 2  text shadow, empty HP bar
    INK_TEXT,      # 3  text, HP label, bar frame
    FACE_LIGHT,    # 4  face, lit (state)
    PARCHMENT,     # 5  face (state)
    PARCH_SHADE,   # 6  face, shade (state)
    CLAY_DARK,     # 7  incised line (state)
    CLAY,          # 8  rim (state)
    (96, 168, 56), # 9  HP fill, healthy
    (176, 216, 104),  # 10 HP fill, healthy, lit
    AEGEAN,        # 11 male symbol
    AEGEAN_PALE,   # 12 male symbol shadow
    PARCH_DARK,    # 13 empty HP bar, top row
    GOLD,          # 14 HP letters
    GOLD_DARK,     # 15
]


def with_(base, **kw):
    p = list(base)
    for k, v in kw.items():
        p[int(k[1:])] = v
    return p


GOLD_RIM = dict(c1=GOLD, c7=GOLD_DARK, c8=GOLD_PALE)
AEGEAN_RIM = dict(c1=AEGEAN_DARK, c7=AEGEAN, c8=AEGEAN_LIGHT)

# Palette 1: the field, the Cancel plaque (1, 7-10), and the empty slot
# socket (1, 11, 12). Palette 2 is the same with the Cancel plaque lit.
BGP1 = [
    CLAY,          # 0
    INK,           # 1  Cancel outline / unused by the socket
    CLAY,          # 2  field
    RING,          # 3  throwing rings
    CLAY_DARK,     # 4
    CLAY_LIGHT,    # 5
    INK,           # 6  friezes
    CLAY,          # 7  Cancel rim
    PARCH_SHADE,   # 8  Cancel face, shade
    PARCHMENT,     # 9  Cancel face
    FACE_LIGHT,    # 10 Cancel face, lit
    CLAY_DARK,     # 11 empty socket, incised outline
    RING,          # 12 empty socket, inner shade
    GOLD,          # 13
    INK_TEXT,      # 14
    GOLD_DARK,     # 15
]
BGP2 = with_(BGP1, c1=GOLD, c7=GOLD_PALE, c8=(232, 200, 104), c9=GOLD_PALE, c10=(248, 240, 192))

PALETTES = [
    BGP1,                                                            # 0 backdrop
    BGP1,                                                            # 1
    BGP2,                                                            # 2
    SLOT,                                                            # 3 normal, healthy HP, male
    with_(SLOT, c1=INK, c4=(232, 240, 200), c5=(208, 216, 168), c6=SILVER_LEAF,
          c7=OLIVE_DARK, c8=OLIVE,                                   # 4 partner's slot
          c9=(232, 168, 32), c10=(248, 224, 112),                    #   caution HP
          c11=(192, 48, 32), c12=(240, 168, 136)),                   #   female symbol
    with_(SLOT, c1=INK, c4=(216, 208, 200), c5=(184, 176, 168), c6=(152, 144, 136),
          c7=(80, 72, 72), c8=(120, 112, 104),                       # 5 fainted, ashen
          c9=(208, 56, 32), c10=(240, 136, 104)),                    #   danger HP
    with_(SLOT, c4=(232, 240, 240), c5=(208, 224, 232), c6=(168, 200, 216),
          **GOLD_RIM),                                               # 6 picked face; lit rim
    with_(SLOT, c4=(248, 248, 216), c5=(248, 232, 168), c6=(232, 200, 112)),   # 7 lit face
    with_(SLOT, c4=(248, 248, 208), c5=(232, 232, 168), c6=(208, 208, 128)),   # 8 lit partner face
    with_(SLOT, c4=(240, 232, 216), c5=(224, 216, 200), c6=(192, 184, 168)),   # 9 lit fainted face
    with_(SLOT, **AEGEAN_RIM),                                       # 10 picked rim
]
for p in PALETTES:
    for c in p:
        assert all(v % 8 == 0 for v in c), c


# --- Slot frames -------------------------------------------------------------
def plaque(w, h, outline=S_OUT, rim=S_RIM, incise=S_INCISE, face=(S_FACE_HI, S_FACE, S_FACE_LO)):
    """A rounded plaque: ink outline, clay rim, incised line, then the face,
    lit along its top and left and shaded along its bottom and right."""
    m = np.ones((h, w), bool)
    for (x, y) in [(0, 0), (1, 0), (0, 1)]:
        for xx, yy in [(x, y), (w - 1 - x, y), (x, h - 1 - y), (w - 1 - x, h - 1 - y)]:
            m[yy, xx] = False
    depth = np.zeros((h, w), int)
    cur = m.copy()
    d = 0
    while cur.any():
        d += 1
        pad = np.pad(cur, 1, constant_values=False)
        inner = cur & pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:]
        depth[cur & ~inner] = d
        cur = inner
    a = np.zeros((h, w), np.uint8)
    a[depth == 1] = outline
    a[depth == 2] = rim
    a[depth == 3] = incise
    f = depth >= 4
    a[f] = face[1]
    pad = np.pad(f, 1, constant_values=False)
    lit = f & (~pad[:-2, 1:-1] | ~pad[1:-1, :-2])
    dark = f & (~pad[2:, 1:-1] | ~pad[1:-1, 2:])
    a[dark] = face[2]
    a[lit] = face[0]
    return a


HP_LETTERS = [
    "1111111111111",
    "1e1e11ee11111",
    "1e1e11e1e1111",
    "1eee11ee11111",
    "1e1e11e111111",
    "1e1e11e111111",
    "1111111111111",
]


def hp_bar(a, label_x, bar_x, bar_y):
    """The HP label (gold letters on an ink tablet) and the bar's ink frame.
    bar_x, bar_y: top-left of the 48x3 fill the code paints."""
    for j, row in enumerate(HP_LETTERS):
        for i, ch in enumerate(row):
            a[bar_y - 2 + j, label_x + i] = S_TEXT if ch == "1" else S_GOLD
    # round the tablet's corners into the face
    for (x, y) in [(label_x, bar_y - 2), (label_x, bar_y + 4), (label_x + 12, bar_y - 2), (label_x + 12, bar_y + 4)]:
        a[y, x] = S_FACE
    # the bar: ink frame, empty groove
    a[bar_y - 1, bar_x - 1:bar_x + 49] = S_TEXT
    a[bar_y + 3, bar_x - 1:bar_x + 49] = S_TEXT
    a[bar_y:bar_y + 3, bar_x - 1] = S_TEXT
    a[bar_y:bar_y + 3, bar_x + 48] = S_TEXT
    a[bar_y, bar_x:bar_x + 48] = S_EMPTY_HI
    a[bar_y + 1:bar_y + 3, bar_x:bar_x + 48] = S_SHADOW
    # soften the frame's corners
    a[bar_y - 1, bar_x - 1] = S_FACE
    a[bar_y + 3, bar_x - 1] = S_FACE
    a[bar_y - 1, bar_x + 48] = S_FACE
    a[bar_y + 3, bar_x + 48] = S_FACE


def slot_main(hp=True):
    a = plaque(80, 56)
    if hp:
        hp_bar(a, 9, 24, 35)       # sPartyBoxInfoRects: bar at 24,35 in the window
    return a


def slot_wide(hp=True):
    a = plaque(144, 24)
    if hp:
        hp_bar(a, 73, 88, 10)      # bar at 88,10
    return a


def slot_empty():
    """An empty socket in the field: an incised outline, its inside clear.
    Drawn only in colors 1, 11 and 12, which come from BG palette 1."""
    a = plaque(144, 24, outline=S_G1, rim=S_G2, incise=0, face=(0, 0, 0))
    return a


# --- Tiles -------------------------------------------------------------------
class SlotTiles:
    """Unflipped tiles for the slot frames, which are blitted by number."""

    def __init__(self):
        self.tiles = [np.zeros((8, 8), np.uint8)]
        self.lookup = {self.tiles[0].tobytes(): 0}

    def add(self, t):
        k = np.asarray(t, np.uint8).tobytes()
        if k not in self.lookup:
            self.lookup[k] = len(self.tiles)
            self.tiles.append(np.asarray(t, np.uint8).copy())
        return self.lookup[k]

    def cut(self, a):
        h, w = a.shape
        return np.array([[self.add(a[y:y + 8, x:x + 8]) for x in range(0, w, 8)] for y in range(0, h, 8)], np.uint8)


# --- The field ----------------------------------------------------------------
def paint_field():
    """BG1 in palette 1: terracotta with throwing rings, a meander frieze at
    the top, a row of rays at the foot, and the Cancel plaque."""
    c = Canvas(240, 160, 2)
    for y in range(160):
        if y % 8 == 7:
            c.hline(0, y, 240, 3)
    c.hline(0, 0, 240, 4)
    c.hline(0, 1, 240, 6)
    c.rect(0, 2, 240, 5, 2)
    c.meander(0, 2, 240, 6)
    c.hline(0, 7, 240, 6)
    # foot rays
    c.rect(0, 152, 240, 8, 2)
    c.hline(0, 152, 240, 6)
    for x0 in range(0, 240, 8):
        for j, half in enumerate([0, 0, 1, 1, 2, 3]):
            c.hline(x0 + 4 - half, 154 + j, 2 * half + 1, 6)
    c.hline(0, 159, 240, 6)
    return c


def cancel_plaque():
    """The Cancel/Confirm plaque, 56x16, in palette 1 colors (the code swaps
    in palette 2 to light it)."""
    p = plaque(56, 16, outline=1, rim=7, incise=7, face=(10, 9, 8))
    return p


def build():
    st = SlotTiles()
    maps = {
        "slot_main": st.cut(slot_main(True)),
        "slot_main_no_hp": st.cut(slot_main(False)),
        "slot_wide": st.cut(slot_wide(True)),
        "slot_wide_no_hp": st.cut(slot_wide(False)),
        "slot_wide_empty": st.cut(slot_empty()),
    }
    n_slot = len(st.tiles)

    # BG1: field tiles (flips allowed), then the Cancel plaque.
    field = paint_field()
    plaque_px = cancel_plaque()
    ts = TileSet()
    ts.tiles = list(st.tiles)
    ts.lookup = {}
    for i, t in enumerate(ts.tiles):
        ts._index(t, i)
    entries = np.zeros((32, 32), np.uint16)
    for ty in range(20):
        for tx in range(30):
            cell = field.a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            i, f = ts.add(cell)
            entries[ty, tx] = i | f | (1 << 12)

    def plaque_map(ty0, field_rows):
        """Map for the 7x2 plaque at cols 23-29, composited on the field."""
        comp = field.a[ty0 * 8:ty0 * 8 + 16, 184:240].copy()
        m = plaque_px != 0
        comp[m] = plaque_px[m]
        out = []
        for j in range(2):
            for i in range(7):
                k, f = ts.add(comp[j * 8:j * 8 + 8, i * 8:i * 8 + 8])
                out.append(k | f | (1 << 12))
        return out

    cancel = plaque_map(17, None)
    for j in range(2):
        for i in range(7):
            entries[17 + j, 23 + i] = cancel[j * 7 + i]
    # In choose-half mode Confirm sits at rows 16-17 and Cancel at 18-19.
    confirm_bin = plaque_map(16, None)
    cancel_bin = plaque_map(18, None)
    n = len(ts.tiles)
    assert n <= 62, f"party bg uses {n} tiles; graphics.c loads -num_tiles 62"
    return st, maps, ts, entries, confirm_bin, cancel_bin, n_slot


def write():
    st, maps, ts, entries, confirm_bin, cancel_bin, n_slot = build()
    # bg.png: 8-bit, 11 palettes; slot tiles preview in palette 3, field in 1.
    write_tiles_png(OUT / "bg.png", ts.tiles, PALETTES, tiles_wide=8, min_tiles=64,
                    pal_of_tile=lambda i: 3 if i < n_slot else 1)
    write_tilemap(OUT / "bg.bin", entries)
    for name, m in maps.items():
        (OUT / f"{name}.bin").write_bytes(m.tobytes())
        print(f"wrote graphics/party_menu/{name}.bin")
    (OUT / "confirm_button.bin").write_bytes(np.array(confirm_bin, "<u2").tobytes())
    (OUT / "cancel_button.bin").write_bytes(np.array(cancel_bin, "<u2").tobytes())
    print(f"party bg: {len(ts.tiles)} tiles ({n_slot} for the slots)")
    write_balls()
    write_hold_icons()
    preview(st, maps, ts, entries)


# --- Sprites -------------------------------------------------------------------
BALL_PAL = pal16([
    TRANSPARENT, INK, (72, 56, 48), CLAY_DARK, CLAY, CLAY_LIGHT,
    PARCHMENT, PARCH_SHADE, PARCH_DARK, GOLD, GOLD_DARK, GOLD_PALE,
])

# A Poke Ball painted black-figure: a glazed ink cap with a clay highlight,
# a buff lower half, a clay seam and a gold button. 20x20, top left of the
# 32x32 frame like the Hoenn ball.
BALL_CLOSED = [
    "       111111       ",
    "     1122222211     ",
    "    125522222221    ",
    "   12552222222221   ",
    "  1255222222222221  ",
    "  1252222222222221  ",
    " 125222222111222221 ",
    " 122222221999122221 ",
    " 111111119bb91111111",
    " 133333319ba91333331",
    " 166666661991666661 ",
    " 166666666116666671 ",
    " 166666666666666771 ",
    "  1666666666666771  ",
    "  1666666666667781  ",
    "   16666666677781   ",
    "    167777777781    ",
    "     1188888811     ",
    "       111111       ",
    "                    ",
]
BALL_OPEN = [
    "       111111       ",
    "     1122222211     ",
    "    125522222221    ",
    "   12552222222221   ",
    "  1255222222222221  ",
    "  1111111111111111  ",
    "   1333333333331    ",
    "    bbbbbbbbbbbb    ",
    "   bbbbbbbbbbbbbb   ",
    " 111111119bb91111111",
    " 133333319ba91333331",
    " 166666661991666661 ",
    " 166666666116666671 ",
    " 166666666666666771 ",
    "  1666666666666771  ",
    "  1666666666667781  ",
    "   16666666677781   ",
    "    167777777781    ",
    "     1188888811     ",
    "       111111       ",
]
BALL_KEY = {"1": 1, "2": 2, "5": 5, "3": 3, "6": 6, "7": 7, "8": 8, "9": 9, "a": 10, "b": 11}


def grid_array(rows, w, h, x0=0, y0=0):
    a = np.zeros((h, w), np.uint8)
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != " ":
                a[y0 + j, x0 + i] = BALL_KEY[ch]
    return a


def write_balls():
    big = np.vstack([grid_array(BALL_CLOSED, 32, 32, 2, 3), grid_array(BALL_OPEN, 32, 32, 2, 2)])
    write_indexed_png(OUT / "pokeball.png", big, [BALL_PAL])
    # The small ball (Cancel/Confirm in choose-half mode): 16x16, 2 frames
    # used, 4 blank.
    small_closed = [
        "    111111    ",
        "  1122222211  ",
        " 125222222221 ",
        " 122222111221 ",
        "11111119b91111",
        "13333319a91331",
        " 166666616661 ",
        " 166666666671 ",
        "  1677777781  ",
        "   11888811   ",
        "     1111     ",
    ]
    small_open = [
        "    111111    ",
        "  1122222211  ",
        " 111111111111 ",
        "  bbbbbbbbbb  ",
        "11111119b91111",
        "13333319a91331",
        " 166666616661 ",
        " 166666666671 ",
        "  1677777781  ",
        "   11888811   ",
        "     1111     ",
    ]
    frames = [grid_array(small_closed, 16, 16, 1, 3), grid_array(small_open, 16, 16, 1, 3)]
    frames += [np.zeros((16, 16), np.uint8)] * 4
    write_indexed_png(OUT / "pokeball_small.png", np.vstack(frames), [BALL_PAL])


def write_hold_icons():
    # 8x8 badges beside a held item's icon: a gold-tied pouch for an item, a
    # sealed scroll for mail. Palette gHeldItemPalette (this PNG's).
    pal = pal16([TRANSPARENT, INK, PARCHMENT, PARCH_SHADE, GOLD, GOLD_DARK, CLAY, CLAY_LIGHT])
    item = [
        "  1111  ",
        " 145541 ",
        "  1441  ",
        " 166661 ",
        "17766661",
        "17666661",
        " 166661 ",
        "  1111  ",
    ]
    mail = [
        "11111111",
        "12222221",
        "13333331",
        "12221221",
        "12216122",
        "13333331",
        "11111111",
        "        ",
    ]
    key = {str(i): i for i in range(8)}
    a = np.zeros((16, 8), np.uint8)
    for j, row in enumerate(item + mail):
        for i, ch in enumerate(row):
            if ch != " ":
                a[j, i] = key[ch]
    write_indexed_png(OUT / "hold_icons.png", a, [pal])


# --- Preview --------------------------------------------------------------------
def preview(st, maps, ts, entries):
    """A mock of the single-battle layout in each slot state, for review."""
    rgb = render_map(entries, ts.tiles, PALETTES, 30, 20)

    def put(m, w, tx, ty, pal):
        for j in range(m.shape[0]):
            for i in range(m.shape[1]):
                t = st.tiles[m[j, i]]
                block = np.array(pal, np.uint8)[t]
                region = rgb[(ty + j) * 8:(ty + j) * 8 + 8, (tx + i) * 8:(tx + i) * 8 + 8]
                region[t != 0] = block[t != 0]

    def state(face_pal, rim_pal, hp_pal=3):
        p = list(SLOT)
        for k in (4, 5, 6):
            p[k] = PALETTES[face_pal][k]
        for k in (1, 7, 8):
            p[k] = PALETTES[rim_pal][k]
        for k in (9, 10):
            p[k] = PALETTES[hp_pal][k]
        return p

    def fill_hp(tx, ty, x, y, frac, hp_pal):
        x0, y0 = tx * 8 + x, ty * 8 + y
        n = int(48 * frac)
        rgb[y0, x0:x0 + n] = PALETTES[hp_pal][10]
        rgb[y0 + 1:y0 + 3, x0:x0 + n] = PALETTES[hp_pal][9]

    put(maps["slot_main"], 10, 1, 3, state(7, 6))
    fill_hp(1, 3, 24, 35, 1.0, 3)
    rows = [(1, (3, 3), 0.7, 3), (4, (6, 10), 0.35, 4), (7, (3, 3), 0.12, 5), (10, (5, 5), 0.0, 5)]
    for ty, (fp, rp), frac, hpp in rows:
        put(maps["slot_wide"], 18, 12, ty, state(fp, rp))
        fill_hp(12, ty, 88, 10, frac, hpp)
    empty = list(SLOT)
    for k in (1, 11, 12):
        empty[k] = BGP1[k]
    put(maps["slot_wide_empty"], 18, 12, 13, empty)
    save_rgb(IMG / "ui_party_bg.png", rgb, 2)


if __name__ == "__main__":
    write()
