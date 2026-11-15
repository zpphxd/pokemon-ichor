"""Haligeron (#137), the Old Man of the Sea: Proteus.

Concept A, "Elder of the Seals". A squat walrus elder sitting up among
Poseidon's herd, his head domed and heavy-browed, one sly gold eye half
shut. Ivory tusks hang over a foam beard that pours from his moustache and
curls at his feet into a Greek wave-scroll. The shapes Menelaus wrestled
out of him live in his hide as sea-glass glow: a lion's mane in a ruff of
flame-locks round his neck, a serpent coiling down his flank, and a leaf
in the hind flipper he holds up behind him. In frame 2 his eye opens wide
and the mane flares, as if the lion is about to surface.

The battle sprites are hand finished in tools/dex/sprites/art/; this file is
the draft they were planned from, and it draws the icon and follower frames.
"""
import math

from mon_lib import Mat, Mon, bez, bez3

COLORS = [
    ("ink", (32, 24, 24)),
    # Aegean hide, from the deep folds to the wet sheen on top
    ("h0", (24, 40, 96)), ("h1", (40, 80, 152)), ("h2", (72, 128, 200)), ("h3", (128, 184, 232)),
    ("sheen", (208, 240, 248)),
    # foam: blue shadow, pale, white
    ("f0", (104, 144, 208)), ("f1", (184, 216, 240)), ("foam", (248, 248, 240)),
    # ivory tusks and claws
    ("iv0", (168, 136, 96)), ("iv1", (232, 216, 168)),
    ("gold", (240, 192, 64)),
    # sea-glass: the forms he can take, glowing in his hide
    ("g0", (40, 144, 144)), ("g1", (80, 224, 184)), ("g2", (200, 248, 224)),
]
# "The hide turns marble gray like an old seal's, and the beard sun-gold."
SHINY = {
    "h0": (64, 64, 80), "h1": (112, 112, 120), "h2": (160, 160, 168), "h3": (208, 208, 208),
    "sheen": (240, 240, 240),
    "f0": (200, 136, 48), "f1": (240, 200, 88), "foam": (248, 240, 184),
}

hide = Mat(["h0", "h1", "h2", "h3"], line="h0", cuts=[0.16, 0.42, 0.7])
hide_hi = Mat(["h0", "h1", "h2", "h3", "sheen"], line="h0", cuts=[0.15, 0.38, 0.64, 0.9])
hide_d = Mat(["h0", "h1", "h2"], line="h0", cuts=[0.42, 0.74])
foam_m = Mat(["f0", "f1", "foam"], line="f0", cuts=[0.34, 0.64])
ivory = Mat(["iv0", "iv1", "foam"], line="iv0", cuts=[0.4, 0.72])
glow_m = Mat(["g0", "g1"], line="g0", cuts=[0.5])
glow_hi = Mat(["g1", "g2"], line="g1", cuts=[0.5])


def path(*segs):
    out = []
    for s in segs:
        if out and s and out[-1] == s[0]:
            s = s[1:]
        out.extend(s)
    return out


def spiral(cx, cy, th0, th1, r0, r1, n=60):
    """Points along a spiral, angles in degrees (0 right, 90 down)."""
    pts = []
    for i in range(n + 1):
        t = i / n
        th = math.radians(th0 + (th1 - th0) * t)
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(th), cy + r * math.sin(th)))
    return pts


# The ruff of flame-locks round the neck: notch, tip, notch ... (front view)
MANE_OUT = [(33, 7.5), (38.5, 7.5), (36.5, 10), (43, 10.5), (39, 13.5), (45, 15.5), (40, 18), (45, 21.5), (40, 23),
            (43.5, 27), (38, 26.5), (39, 31), (35.5, 28.5)]
MANE_IN = [(35.5, 26), (36, 22), (34.5, 17), (33.5, 13), (33, 9), (32.5, 7.5)]


# --------------------------------------------------------------------------
# Battle front: 3/4 view facing left (the art file is the finished version)
# --------------------------------------------------------------------------

def _front(p, ph):
    big = p.big
    # hind flippers: the one held up behind him is the leaf
    p.lens((52, 54), (61.6, 41), 8.5, hide_d, bend=-1.0, fat=0.6, group=3)
    p.lens((51, 49), (58.6, 15.5), 12.4, hide, bend=1.8, fat=0.52, group=4)
    p.stroke([(52, 47), (55, 32), (57.5, 19)], "g1")
    # the body: a hump of shoulder behind the head, the barrel, the haunch
    for cx, cy, rx, ry in ((36, 17, 11, 11), (39.5, 37, 14, 19), (48, 51, 9.5, 9.5), (28, 36, 9, 13.5),
                           (23, 50, 9, 11)):
        p.blob(cx, cy, rx, ry, hide_hi, group=10)
    # the lion's mane surfacing round his neck
    p.poly(MANE_OUT + MANE_IN, glow_hi if ph else glow_m, group=11, noline=True)
    # the serpent coiled down the flank
    p.limb(bez3((44.5, 25), (53, 29), (50, 36), (43, 37)), 3.2, 2.6, glow_m, group=12, noline=True)
    p.limb(bez3((43, 37), (38, 40), (42, 45), (54, 45)), 2.6, 1.6, glow_m, group=12, noline=True)
    # the head
    p.blob(22, 12.5, 10.5, 9.5, hide_hi, group=20)
    p.blob(28.5, 21, 7, 5, hide_hi, group=20)
    # the beard, pouring from under the moustache into the wave-scroll
    p.poly(path([(5, 23), (25, 23)], bez3((25, 23), (29.5, 30), (29, 40), (26, 46)),
                bez3((26, 46), (22, 48), (14, 46), (8, 44)), bez3((8, 44), (4, 41), (2.5, 32), (5, 23))),
           foam_m, group=30)
    p.limb(spiral(11.5, 52.5, 228, -150 - 30 * ph, 8.4, 3.0), 6.0, 2.4, foam_m, group=31)
    # the fore-flipper planted on the ground
    p.limb(bez((35, 44.5), (33.5, 49), (32, 55.5)), 10.5, 8.5, hide_hi, group=40)
    p.poly(path(bez3((22, 59.5), (24, 55.5), (31, 54), (37, 55)), bez3((37, 55), (41, 55.5), (43, 57.5), (42.5, 60.6)),
                [(23, 60.6)]), hide, group=41)
    # the moustache pads
    p.blob(8.5, 19.5, 6.5, 5.2, hide_hi, ang=-10, group=50)
    p.blob(17.5, 21, 7.6, 5.8, hide_hi, ang=6, group=51)
    # tusks
    p.limb(bez((10, 25), (9, 33), (10, 41)), 3.6, 1.4, ivory, group=60)
    p.limb(bez((18.5, 27), (18, 37), (19.5, 46)), 4.4, 1.6, ivory, group=61)
    if big:
        # the eye under its heavy brow, sun-gold
        rows = ["#######", "#ee##s#", ".#eee#."] if not ph else ["#######", "#ee##s#", "#ee####", ".#eee#."]
        p.patch(20, 10, rows, {"#": "ink", "e": "gold", "s": "foam"})
        p.pxs([(5, 17), (6, 17), (14, 17), (15, 17)], "ink")
    else:
        p.px(23, 11, "gold")
        p.px(24, 11, "ink")


# --------------------------------------------------------------------------
# Battle back: over the shoulder, head turned right in profile
# --------------------------------------------------------------------------

def _back(p, ph):
    p.lens((17, 56), (2.5, 36), 9.5, hide_d, bend=-1.5, fat=0.55, group=3)
    p.lens((13, 52), (6.5, 14), 13.5, hide, bend=2.2, fat=0.5, group=4)
    for cx, cy, rx, ry in ((27, 56, 25.5, 28), (38, 33, 14, 14), (44, 50, 12, 16)):
        p.blob(cx, cy, rx, ry, hide_hi, group=10)
    p.limb(bez3((37, 38), (24, 37), (20, 46), (29, 51)), 3.6, 3.0, glow_m, group=11, noline=True)
    p.limb(bez3((29, 51), (32, 57), (20, 59), (5, 62.5)), 3.0, 1.6, glow_m, group=11, noline=True)
    p.poly(path([(43, 25), (60, 25)], bez3((60, 25), (62.5, 36), (61, 50), (62.5, 64)), [(43, 64)],
                bez3((43, 64), (45, 50), (43, 36), (43, 25))), foam_m, group=30)
    p.blob(44, 15.5, 11.5, 10, hide_hi, group=20)
    p.blob(40, 24, 8, 6, hide_hi, group=20)
    p.blob(55, 21.5, 7, 5.6, hide_hi, ang=4, group=21)
    p.limb(bez((55, 27), (56, 36), (55, 44)), 4.4, 1.6, ivory, group=31)
    if p.big:
        p.patch(44, 11, ["######", "#s##ee#", ".#eee#"], {"#": "ink", "e": "gold", "s": "foam"})


# --------------------------------------------------------------------------
# Follower views
# --------------------------------------------------------------------------

def _down(p, ph):
    # walking toward the camera: the head over the beard, tusks either side,
    # the mane's ruff glowing round the neck, flippers stepping in turn
    p.lens((22, 52), (10, 60 - 2 * ph), 8, hide, bend=-1, group=3)
    p.lens((42, 52), (54, 60 - 2 * (1 - ph)), 8, hide, bend=1, group=4)
    p.blob(32, 44, 16, 15, hide_hi, group=10)
    p.blob(32, 23, 14.5, 12.5, glow_m, group=11)
    p.blob(32, 23, 11.5, 10, hide_hi, group=20)
    p.poly(path([(23, 31), (41, 31)], bez3((41, 31), (44, 42), (40, 52), (32, 58)),
                bez3((32, 58), (24, 52), (20, 42), (23, 31))), foam_m, group=30)
    p.blob(27, 29, 5.6, 4.2, hide_hi, group=31)
    p.blob(37, 29, 5.6, 4.2, hide_hi, group=32)
    p.limb([(26.5, 32), (26, 47)], 3.4, 1.4, ivory, group=40)
    p.limb([(37.5, 32), (38, 47)], 3.4, 1.4, ivory, group=41)
    p.eye(25, 20, 3, 2, shine=None, iris="gold")
    p.eye(36, 20, 3, 2, shine=None, iris="gold")


def _up(p, ph):
    # walking away: the broad back, the serpent down the spine, the leaf
    # flippers lifting in turn
    p.lens((28, 54), (18, 61 - 2 * ph), 8, hide, bend=1, group=3)
    p.lens((36, 54), (46, 61 - 2 * (1 - ph)), 8, hide, bend=-1, group=4)
    p.blob(32, 42, 17, 16, hide_hi, group=10)
    p.blob(32, 24, 13.5, 11.5, glow_m, group=11)
    p.blob(32, 24, 11, 9.5, hide_hi, group=20)
    p.limb(bez3((32, 31), (38, 36), (26, 42), (32, 50)), 3.2, 2.0, glow_m, group=12, noline=True)


def _icon(p, ph):
    """Party icon: the front pose with a bigger head and bold, flat shapes
    so the face, tusks, beard-curl, mane and leaf read at 32 px."""
    up = ph
    p.lens((47, 52), (58, 16), 15, hide, bend=2, fat=0.5, group=3)
    p.stroke([(49, 48), (53, 32), (56, 20)], "g1")
    p.blob(38, 42, 19, 17, hide_hi, group=10, flat=2)
    p.blob(32, 22 - up, 18, 16, glow_hi if ph else glow_m, group=11, flat=0)
    p.blob(26, 22 - up, 14, 13, hide_hi, group=20)
    p.poly(path([(6, 34 - up), (32, 34 - up)], bez3((32, 34 - up), (35, 44), (30, 50), (24, 52)),
                [(10, 50)], bez3((10, 50), (5, 46), (4, 40), (6, 34 - up))), foam_m, group=30, flat=2)
    p.limb(spiral(13, 54, 228, -150, 9, 3.5), 7, 3, foam_m, group=31, flat=2)
    p.blob(12, 30 - up, 8.5, 6.8, hide_hi, group=50)
    p.blob(25, 32 - up, 9.5, 7.2, hide_hi, group=51)
    p.limb([(13, 36 - up), (13, 52)], 5, 2.4, ivory, group=60, flat=1)
    p.limb([(25, 38 - up), (26, 56)], 5.6, 2.6, ivory, group=61, flat=1)
    p.rect(26, 17 - up, 32, 19 - up, Mat(["ink"]), group=70, flat=0, noline=True)
    p.rect(27, 19 - up, 30, 20 - up, Mat(["gold"]), group=71, flat=0, noline=True)


def haligeron(p, view, phase):
    if view == "icon":
        _icon(p, phase)
    elif view in ("front", "side"):
        _front(p, phase if view != "side" else 0)
    elif view == "back":
        _back(p, phase)
    elif view == "down":
        _down(p, phase)
    elif view == "up":
        _up(p, phase)


MONS = [
    # icon palette 0 keeps the blue hide, the white beard and the teal mane apart
    Mon("Haligeron", COLORS, SHINY, haligeron, foot="fin", icon_pal=0),
]
