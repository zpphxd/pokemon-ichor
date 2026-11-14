"""Echo line: Echolali (Kythera Isle). The nymph Echo, cursed by Hera to repeat
only the last words she heard, pined for Narcissus until nothing was left of
her but her voice (Ovid, Metamorphoses 3)."""
import math

from mon_lib import Mat, Mon, bez, bez3

INK = (32, 24, 24)

ECHOLALI_COLORS = [
    ("ink", INK),
    # only marble-white and the two lightest Aegean blues: half there
    ("white", (248, 248, 240)), ("pale", (224, 232, 232)),
    ("ae3", (176, 216, 240)), ("ae2", (112, 168, 224)),
    # her eyes, the one solid thing about her
    ("eye", (40, 72, 128)),
]
ECHOLALI_SHINY = {
    # the pale blues turn a faint lilac, the color of dusk in the caves
    "ae3": (216, 200, 240), "ae2": (168, 144, 216), "eye": (88, 64, 136),
}

e_body = Mat(["ae2", "ae3", "pale", "white"], line="ae2", cuts=[0.18, 0.42, 0.7])
e_skin = Mat(["ae3", "pale", "white"], line="ae3", cuts=[0.36, 0.68])
e_hair = Mat(["ae2", "ae3", "pale"], line="ae2", cuts=[0.3, 0.64])


def _arc(cx, cy, rx, ry, a0, a1, n=10):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def _rings(p, cx, cy, side=-1, n=3, r0=2.0, dr=2.6, span=55, color="ae2", grow=1.0):
    """Thin arcs of sound rippling out from (cx, cy) toward side (-1 left,
    +1 right, 2 down)."""
    for k in range(n):
        r = r0 + dr * k
        if side == 2:
            pts = _arc(cx, cy, r * 1.6 * grow, r * 0.5, 20, 160, n=14)
        else:
            mid = 180 if side < 0 else 0
            pts = _arc(cx, cy, r * 0.7, r, mid - span, mid + span, n=10)
        p.stroke(pts, color if k < n - 1 else "ae3")


def echolali(p, view, phase):
    if view in ("front", "side", "icon"):
        L = 1 if (phase == 1 and view == "front") else 0
        # long hair streaming back, parting into locks that fade to rings
        p.lens((28, 8 - L), (46, 22 + L), 9.0, e_hair, bend=-2.4, fat=0.32, group=10)
        p.lens((29, 13 - L), (44, 34), 8.0, e_hair, bend=-2.2, fat=0.32, group=11, bias=0.08)
        p.lens((30, 18 - L), (38, 42), 6.0, e_hair, bend=-1.2, fat=0.32, group=12, bias=0.16)
        # the far arm trailing back
        p.limb([(31, 25), (35, 30), (38, 33)], 2.6, 2.0, e_skin, group=19, bias=0.2)
        # the dress, flaring from the waist and thinning into rings at the hem
        p.poly([(24.5, 29), (31.5, 29), (34, 36), (38, 44), (40, 50), (33, 51.5), (26, 52), (19, 51), (15, 49.5),
                (19, 42), (22, 35)], e_body, group=20)
        # torso, neck, head
        p.limb([(27.5, 21.5), (28, 30)], 6.0, 5.0, e_body, group=21)
        p.limb([(26.5, 17 - L), (27, 22)], 2.8, 3.2, e_skin, group=22)
        p.blob(25, 12 - L, 6.8, 7.0, e_skin, group=30, bias=-0.12)
        # the near arm raised, a hand cupped by where her mouth would be
        p.limb([(25, 22.5), (20, 24), (17.5, 19.5 - L)], 2.6, 2.2, e_skin, group=24)
        p.blob(17.2, 18.4 - L, 1.6, 1.8, e_skin, group=25)
        # hair over the brow
        p.lens((32, 5 - L), (19, 10 - L), 5.0, e_hair, bend=1.6, group=31)
        if p.big:
            # large eyes, no mouth: thin rings ripple out where it would be
            p.eye(19, 11 - L, 2, 6, pupil="eye", shine="white", shine_at=(1, 1))
            p.eye(22, 11 - L, 4, 6, pupil="eye", shine="white")
            _rings(p, 15, 17 - L, -1, n=3, r0=1.6 + 0.5 * L, dr=2.2)
            _rings(p, 46, 22 + L, +1, n=2, r0=1.8, dr=2.4, span=50)
            _rings(p, 44, 35, +1, n=2, r0=1.8 + L, dr=2.4, span=50)
            _rings(p, 28, 53, 2, n=3, r0=2.6, dr=1.4, grow=1.0 + 0.1 * L)
        else:
            p.px(20, 13 - L, "eye")
            p.px(23, 13 - L, "eye")
        return

    if view == "back":
        # over the shoulder: hair dissolving into rings, her face turned
        # right in profile, rings rippling out ahead of her
        p.lens((36, 18), (12, 50), 14, e_hair, bend=3.0, fat=0.35, group=10)
        p.poly([(18, 64), (22, 40), (30, 30), (44, 30), (50, 42), (52, 64)], e_body, group=20)
        p.limb([(40, 30), (41, 24)], 4.4, 4.0, e_skin, group=22)
        p.blob(42, 17, 8, 8.4, e_skin, group=30, bias=-0.1)
        p.lens((34, 10), (50, 10), 6, e_hair, bend=-1.0, group=31)
        p.blob(37, 15, 7.6, 7.2, e_hair, group=32)
        if p.big:
            p.eye(46, 15, 3, 6, pupil="eye", shine="white", shine_at=(1, 1))
            _rings(p, 50.5, 22, +1, n=3, r0=1.6, dr=2.4)
        return

    if view in ("down", "up"):
        # the follower walks a step behind, copying the player
        st = phase
        p.poly([(27, 30), (37, 30), (40, 42), (36, 50), (28, 50), (24, 42)], e_body, group=20)
        p.lens((26, 14), (20, 38 + st), 6, e_hair, bend=1.2, group=10)
        p.lens((38, 14), (44, 38 + 1 - st), 6, e_hair, bend=-1.2, group=11)
        p.limb([(32, 22), (32, 31)], 6, 5.6, e_body, group=21)
        p.blob(32, 16, 6.6, 7, e_skin, group=30, bias=-0.1)
        p.blob(32, 11.5, 7, 4, e_hair, group=31)
        if view == "down":
            p.eye(27.5, 15, 3, 5, pupil="eye", shine="white")
            p.eye(33.5, 15, 3, 5, pupil="eye", shine="white")
            if p.big:
                _rings(p, 32, 22, 2, n=2, r0=1.2, dr=1.4)
        else:
            p.lens((32, 12), (32, 40), 9, e_hair, group=12)
        if p.big:
            _rings(p, 32, 51, 2, n=2, r0=2.6 + st * 0.6, dr=1.8)
        return


MONS = [
    Mon("Echolali", ECHOLALI_COLORS, ECHOLALI_SHINY, echolali, foot="blank"),
]
