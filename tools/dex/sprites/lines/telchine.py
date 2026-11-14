"""Telchine line: Telpup, Telkanvil (Water, then Water/Steel). The Telchines,
flippered sea-smiths of Rhodes who forged Poseidon's trident and the adamant
sickle (the Harpe) that Kronos used on Ouranos."""
import math

from mon_lib import C, Mat, Mon, bez

INK = C.ink

# --------------------------------------------------------------------------
# Telpup, the smith pup
# --------------------------------------------------------------------------

TELPUP_COLORS = [
    ("ink", INK),
    # Aegean-blue coat with a wet sheen
    ("aeg0", (24, 56, 120)), ("aeg1", (48, 104, 176)), ("aeg2", (112, 168, 224)), ("aeg3", (184, 224, 248)),
    # marble belly and muzzle
    ("marb0", (160, 152, 152)), ("marb1", (216, 208, 192)), ("white", C.white),
    # the limestone hammerhead on a driftwood haft
    ("lime0", (144, 112, 72)), ("lime1", (200, 168, 112)), ("lime2", (232, 216, 176)),
    ("wood", (104, 72, 48)),
    # black-sand soot, the obsidian pebble, the pink of the mouth
    ("soot", (72, 64, 80)), ("glass", (128, 120, 144)), ("pink", (224, 128, 136)),
]
TELPUP_SHINY = {
    "aeg0": (64, 64, 80), "aeg1": (112, 112, 128), "aeg2": (168, 168, 184), "aeg3": (224, 224, 232),
    "lime0": (168, 104, 24), "lime1": (224, 168, 48), "lime2": (248, 224, 120),
}

coat = Mat(["aeg0", "aeg1", "aeg2", "aeg3"], line="aeg0", cuts=[0.16, 0.5, 0.84])
belly = Mat(["marb0", "marb1", "white"], line="marb0", cuts=[0.4, 0.7])
stone = Mat(["lime0", "lime1", "lime2"], line="lime0", cuts=[0.36, 0.7])
haft = Mat(["wood", "lime0"], cuts=[0.55])
glass = Mat(["soot", "glass"], line="soot", cuts=[0.5])


def _hammer(p, grip, head, w=4.6, h=3.4):
    """A tiny stone hammer: a haft from the grip up to a lashed stone head
    lying across its top."""
    p.limb([grip, head], 1.6, 1.4, haft)
    dx, dy = head[0] - grip[0], head[1] - grip[1]
    d = math.hypot(dx, dy) or 1
    nx, ny = -dy / d, dx / d
    a = (head[0] + nx * w / 2, head[1] + ny * w / 2)
    b = (head[0] - nx * w / 2, head[1] - ny * w / 2)
    return p.limb([a, b], h, h * 0.9, stone)


def _crescent(p, cx, cy, r=2.8, flip=False):
    """The obsidian pebble Telpup knaps: a little curved blade, the shape
    its kind beat out without knowing why (the Harpe)."""
    s = -1 if flip else 1
    return p.lens((cx - s * r, cy + 0.8), (cx + s * r, cy - 0.4), r * 1.15, glass, bend=-s * 1.1, fat=0.45)


def telpup(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0        # head lifts
        wind = phase == 1 and view == "front"                   # hammer cocked back

        # hind flippers fanned up behind the rump
        p.lens((45.5, 56.5), (52.5, 49 + L), 5.0, coat, bend=-0.7, bias=0.22, group=10)
        p.lens((46.5, 58.5), (54.5, 57), 4.6, coat, bend=0.6, bias=0.1, group=11)

        # the obsidian pebble, held down by the far fore-flipper
        _crescent(p, 14.2, 59, r=2.8)
        p.lens((26, 52.5), (17.6, 59.3), 4.6, coat, bend=0.9, bias=0.3, group=12)

        # body: a round pup sitting up, its rump trailing back
        body = p.blob(34.5, 51.5, 10, 8.8, coat, group=1)
        p.blob(42, 57, 6.4, 3.4, coat, group=1)
        p.blob(30, 53.5, 6.4, 6.6, belly, clip=[body], group=2)

        # head: big and round, a short marble muzzle
        p.blob(27.5, 38.6 - L, 10.8, 9.4, coat, group=3)
        p.blob(20, 44.2 - L, 5.8, 3.8, belly, ang=-4, group=4)

        # near fore-flipper raising the hammer beside the head
        if wind:
            _hammer(p, (40.5, 46), (46.5, 37), w=6, h=4)
        else:
            _hammer(p, (40.5, 46), (43.5, 34.5), w=6, h=4)
        p.lens((33, 51), (41, 45), 5.2, coat, bend=-0.7, group=13)

        if p.big:
            p.eye(25, 34 - L, 5, 6, shine="white", shine_at=(1, 1))
            p.eye(19, 35 - L, 3, 5, shine="white", shine_at=(1, 1))
            p.pxs([(15, 42 - L), (16, 42 - L), (16, 43 - L)], "ink")      # nose
            p.pxs([(18, 41 - L), (19, 41 - L), (18, 42 - L)], "soot")     # soot smudge
            p.stroke([(18, 46 - L), (21, 46 - L)], "marb0")              # mouth
            if wind:
                p.pxs([(19, 46 - L), (20, 46 - L)], "pink")
        else:
            p.px(27, 37 - L, "ink")
            p.px(20, 38 - L, "ink")
        return

    if view == "back":
        # over the shoulder at about 1.2x: the round back cropped by the
        # frame, the head turned right in profile, the hammer held up
        p.blob(30, 65, 26, 22.5, coat, group=1)
        p.blob(41, 44, 11, 8, coat, group=1)
        p.blob(44, 30.5, 11, 9.8, coat, group=3)
        p.blob(53.5, 35.5, 6, 4, belly, ang=6, group=4)
        _hammer(p, (17, 45), (12.5, 31.5), w=7, h=4.6)
        p.lens((28, 51), (16.5, 44.5), 6.6, coat, bend=0.8, group=13)
        if p.big:
            p.eye(47, 26, 4, 6, shine="white", shine_at=(1, 1))
            p.pxs([(58, 33), (58, 34), (57, 33)], "ink")
            p.pxs([(55, 32), (56, 32)], "soot")
        return

    if view == "down":
        # follower toward the camera: round pup, both flippers, hammer up
        step = phase
        p.lens((27, 57), (19, 60 - step), 5, coat, bend=-0.4, group=12)
        p.lens((37, 57), (45, 60 - (1 - step)), 5, coat, bend=0.4, group=13)
        p.blob(32, 50, 9, 8, coat, group=1)
        p.blob(32, 52, 6, 5.6, belly, group=2)
        p.blob(32, 38, 8.6, 7.6, coat, group=3)
        p.blob(32, 42.5, 4.4, 2.8, belly, group=4)
        _hammer(p, (42, 48), (44, 39 + step), w=5, h=3.4)
        p.lens((37, 50), (42, 47), 4.4, coat, group=20)
        _crescent(p, 25, 58)
        p.eye(27, 36, 3, 4, shine="white")
        p.eye(34, 36, 3, 4, shine="white")
        p.pxs([(31, 41), (32, 41)], "ink")
        p.px(32, 40, "soot")
        p.px(32, 44, "pink")
        return

    if view == "up":
        step = phase
        p.lens((27, 56), (20, 61 - step), 5, coat, bend=-0.4, group=12)
        p.lens((37, 56), (44, 61 - (1 - step)), 5, coat, bend=0.4, group=13)
        p.blob(32, 50, 9, 8.4, coat, group=1)
        p.blob(32, 38, 8.4, 7.4, coat, group=3)
        _hammer(p, (42, 47), (44, 38 + step), w=5, h=3.4)
        p.lens((37, 49), (42, 46), 4.4, coat, group=20)
        return


# --------------------------------------------------------------------------
# Telkanvil, the sea smith
# --------------------------------------------------------------------------

TELKANVIL_COLORS = [
    ("ink", INK),
    ("aeg0", (24, 48, 104)), ("aeg1", (40, 96, 168)), ("aeg2", (96, 152, 216)), ("aeg3", (168, 208, 240)),
    ("marb0", (160, 152, 152)), ("marb1", (216, 208, 192)), ("white", C.white),
    # the anvil shell: iron black to marble gray
    ("iron0", (48, 48, 64)), ("iron1", (88, 88, 104)), ("iron2", (144, 144, 160)),
    # leather apron, and the hot blank: red heat to sun-gold to white heat
    ("terra0", (120, 48, 24)), ("terra1", (184, 88, 48)),
    ("gold", (240, 192, 64)), ("hot", (248, 240, 176)),
]
TELKANVIL_SHINY = {
    "aeg0": (56, 56, 72), "aeg1": (104, 104, 120), "aeg2": (160, 160, 176), "aeg3": (216, 216, 224),
    "iron0": (96, 56, 24), "iron1": (160, 104, 48), "iron2": (216, 168, 88),
}

k_coat = Mat(["aeg0", "aeg1", "aeg2", "aeg3"], line="aeg0", cuts=[0.18, 0.44, 0.72])
k_belly = Mat(["marb0", "marb1", "white"], line="marb0", cuts=[0.42, 0.72])
k_iron = Mat(["iron0", "iron1", "iron2"], line="iron0", cuts=[0.4, 0.7])
k_apron = Mat(["terra0", "terra1"], line="terra0", cuts=[0.5])
k_hot = Mat(["terra1", "gold", "hot"], line="terra1", outline="terra0", cuts=[0.34, 0.62])
k_whisk = Mat(["marb0", "marb1", "white"], line="marb0", cuts=[0.3, 0.62])


def _anvil(p, x0, y0, w, h, horn, d=2.0, flip=False, **kw):
    """The anvil shell: a flat face x0..x0+w on row y0 seen a little from
    above (a top band d deep), a horn tapering off the right end (the left
    when flip), a waisted body and a broad foot h below. Returns the body
    part's id; the top band is drawn over it."""
    def X(x):
        return 2 * x0 + w - x if flip else x
    body = [(x0, y0), (x0 + w, y0), (x0 + w + horn * 0.45, y0 + 0.6), (x0 + w + horn, y0 + d + 1.6),
            (x0 + w + horn * 0.5, y0 + d + 2.6), (x0 + w - 0.5, y0 + h * 0.36),
            (x0 + w - h * 0.16, y0 + h * 0.58), (x0 + w + h * 0.06, y0 + h), (x0 - h * 0.06, y0 + h),
            (x0 + h * 0.16, y0 + h * 0.58), (x0, y0 + h * 0.36)]
    pid = p.poly([(X(x), y) for x, y in body], k_iron, **kw)
    kw.pop("group", None)
    top = [(x0 + 0.5, y0 + 0.3), (x0 + w, y0 + 0.3), (x0 + w + horn * 0.45, y0 + 0.9),
           (x0 + w + horn * 0.8, y0 + d + 1.2), (x0 + w, y0 + d), (x0 + 0.5, y0 + d)]
    p.poly([(X(x), y) for x, y in top], k_iron, clip=[pid], flat=2, noline=True, **kw)
    return pid


def _harpe(p, tang, tip, w=3.4, **kw):
    """The glowing blank in the tongs: a sickle blade from its tang, curving
    out and hooking at the tip like the Harpe. Red heat at the edges, sun-gold
    through the blade, white heat along the spine."""
    pid = p.lens(tang, tip, w, k_hot, bend=-3.2, fat=0.62, **kw)
    kw.pop("group", None)
    p.lens(tang, tip, w * 0.45, k_hot, bend=-2.9, fat=0.6, clip=[pid], flat=2, noline=True, **kw)
    return pid


def telkanvil(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0      # hammer cocks back, head lifts
        # the anvil shell on its back, the horn sweeping back past the shoulder
        _anvil(p, 29, 9, 22, 25, 10, d=2.4, group=30)

        # near arm raised, the hammer cocked back over the shoulder
        p.limb([(45, 17 - L), (51 + L, 7.5 - L)], 2.4, 2.2, k_apron)                  # haft
        p.limb([(47.5 + L, 4.4 - L), (56 + L, 10.4 - L)], 6.4, 6.0, k_iron, group=31)  # head
        p.limb([(40, 31), (49.5, 24.5)], 9.4, 7.8, k_coat, group=20)
        p.limb([(49.5, 24.5), (45.5, 17 - L)], 7.6, 6.2, k_coat, bias=-0.05, group=20)
        p.blob(45.2, 16 - L, 3.8, 3.4, k_coat, group=20)

        # hind flippers splayed like broad feet
        p.lens((44, 57), (56, 60), 6.4, k_coat, bend=0.8, bias=0.3, group=10)
        p.lens((24, 57), (11, 60.4), 6.4, k_coat, bend=-0.6, bias=0.05, group=11)
        p.lens((35, 58), (26, 61), 6.4, k_coat, bend=-0.5, group=12)

        # body: a massive upright seal, broad in the shoulder and the base
        body = p.blob(32.5, 43, 15, 16, k_coat, group=1)
        p.blob(34.5, 52.5, 14, 7.4, k_coat, group=1)
        p.blob(34.5, 31, 12.6, 7.4, k_coat, group=1)
        p.blob(26, 41, 9, 12, k_belly, clip=[body], group=2)
        # the leather apron, flaring to the knees, a strap round the neck
        p.poly(bez((20, 35), (27.5, 32.5), (36, 35), n=8) + bez((38, 44), (41.5, 52), (41.5, 58), n=6)
               + bez((41.5, 58), (29, 61), (15.5, 57.5), n=8) + bez((15.5, 57.5), (17, 46), (20, 35), n=6),
               k_apron, group=5)

        # head: a heavy brow ridge over a broad whiskered muzzle
        p.blob(22, 19 - L, 10.6, 9.6, k_coat, group=3)
        p.blob(19.5, 14.5 - L, 8.6, 3.8, k_coat, ang=-8, group=3)
        p.blob(13.5, 25 - L, 8, 5.4, k_belly, ang=-6, group=4)
        # whiskers drooping like a smith's beard
        p.poly(bez((6, 26.5 - L), (14, 31 - L), (24, 27.5 - L), n=8) + [(25.5, 31), (23.5, 37), (20.5, 35),
               (18.5, 40), (15.5, 36), (12.5, 40.5), (10.5, 35.5), (7, 38), (6, 32)], k_whisk, group=6)

        # far arm reaching forward, the tongs gripping the glowing blank
        p.limb([(21, 40), (15, 45.5)], 6.4, 5.4, k_coat, group=21)
        p.limb([(14, 46), (8.5, 48)], 1.8, 1.6, k_iron)
        _harpe(p, (9, 49.5), (7.5, 34.5), w=5.4)

        if p.big:
            p.eye(21, 17 - L, 4, 4, shine="white", shine_at=(1, 1))
            p.eye(14, 17 - L, 2, 4, shine="white", shine_at=(0, 1))
            p.pxs([(6, 22 - L), (7, 22 - L), (6, 23 - L), (7, 23 - L)], "ink")      # nose
        else:
            p.px(21, 18 - L, "ink")
        return

    if view == "back":
        # over the shoulder: the anvil shell across the back, its horn
        # pointing back past the shoulder blade, the head turned right in
        # profile, the hammer raised over the near shoulder
        p.blob(32, 67, 28.5, 24, k_coat, group=1)
        p.blob(46, 47, 13, 12, k_coat, group=1)
        _anvil(p, 15, 27, 27, 36, 11.5, d=3.6, flip=True, group=30)
        p.blob(47, 29.5, 11.5, 10.5, k_coat, group=3)
        p.blob(46, 22.5, 9.4, 4.4, k_coat, ang=4, group=3)
        p.blob(55.5, 34.5, 6.6, 5.2, k_belly, ang=6, group=4)
        p.poly(bez((50, 37.5), (56, 41), (62, 37), n=8) + [(62, 42), (61, 48), (59, 45), (57, 51), (55, 46),
               (53, 50), (51.5, 44), (49.5, 46)], k_whisk, group=6)
        p.limb([(25, 25), (15.5, 14)], 2.8, 2.6, k_apron)
        p.limb([(9, 18), (19.5, 8.5)], 8, 7.4, k_iron, group=31)
        p.limb([(37, 45), (28.5, 36.5)], 10.4, 9, k_coat, group=20)
        p.limb([(28.5, 36.5), (25, 26)], 9, 7.4, k_coat, group=20)
        p.blob(25, 25, 4.4, 4, k_coat, group=20)
        if p.big:
            p.eye(50, 25, 4, 4, shine="white", shine_at=(1, 1))
            p.pxs([(61, 31), (61, 32), (62, 31)], "ink")
        return

    if view in ("down", "up"):
        step = phase
        p.lens((26, 58), (18, 61 - step), 6, k_coat, bend=-0.4, group=12)
        p.lens((38, 58), (46, 61 - (1 - step)), 6, k_coat, bend=0.4, group=13)
        if view == "up":
            p.blob(32, 46, 13, 14, k_coat, group=1)
            _anvil(p, 23, 30, 18, 18, 6, group=30)
            p.blob(32, 26, 9, 8, k_coat, group=3)
            p.limb([(44, 15), (44, 25)], 2, 2, k_apron)
            p.limb([(40, 14), (48, 14)], 5, 5, k_iron)
            p.limb([(42, 40), (47, 32), (45, 25)], 5, 4, k_coat, group=20)
            return
        p.limb([(44, 15), (44, 25)], 2, 2, k_apron)
        p.limb([(40, 14), (48, 14)], 5, 5, k_iron)
        p.limb([(42, 40), (47, 32), (45, 25)], 5, 4, k_coat, group=20)
        p.blob(32, 46, 13, 14, k_coat, group=1)
        p.blob(32, 46, 8, 11, k_belly, group=2)
        p.poly(bez((24, 39), (32, 37), (40, 39), n=6) + [(41, 56), (23, 56)], k_apron, group=5)
        p.blob(32, 26, 9.4, 8.2, k_coat, group=3)
        p.blob(32, 31, 6, 3.6, k_belly, group=4)
        p.lens((28, 33), (25, 42), 3.6, k_whisk, bend=0.6)
        p.lens((36, 33), (39, 42), 3.6, k_whisk, bend=-0.6)
        p.limb([(22, 42), (17, 45)], 5, 4, k_coat, group=21)
        _harpe(p, (16, 47), (13, 37), w=3.6)
        p.eye(27, 22, 3, 4, shine="white")
        p.eye(34, 22, 3, 4, shine="white")
        return


MONS = [
    Mon("Telpup", TELPUP_COLORS, TELPUP_SHINY, telpup, foot="fin"),
    Mon("Telkanvil", TELKANVIL_COLORS, TELKANVIL_SHINY, telkanvil, foot="fin"),
]
