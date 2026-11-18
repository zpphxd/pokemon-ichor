"""The bronze man of Kaldera (design/AWE_PASS.md C2), drawn as a classical bronze.

A 6 x 10 metatile colossus in the spirit of the Riace bronzes: about 7.5 heads
tall, in contrapposto (his weight on his right leg, the left relaxed, its heel
never cast), curled hair and beard, a smith's hammer hanging in his right hand.
His left forearm was never cast: the stump shows the clay core and an iron
armature rod, and its open mold waits on the scaffold beside him.

Process (STYLE.md §3.2-3.4):
  1. concept() sculpts him at 2x as a height field of anatomical forms (skull,
     pectorals, deltoids, the six abdominal blocks, thighs, calves...), lit from
     the top left with a specular term, so the shading follows real muscle;
  2. native() reduces that to 1x on the true grid (2x2 cells, the lighting
     re-evaluated per native pixel), maps it onto the bronze ramp (warm dark
     brown shadows, mid bronze, gold specular, verdigris in the recesses) and
     closes a selective outline;
  3. hand_fix() redraws the face, the curls, the seams and the hand at 1x.

kaldera_art.paint_giant() places the result and adds the scaffold, the mold,
the stepped plinth, the lava pit and the animated vein.
"""
from __future__ import annotations

import numpy as np

S = 2                       # concept scale
NW, NH = 96, 160            # native box (6 x 10 metatiles)
CW, CH = NW * S, NH * S

LIGHT = np.array([-0.55, -0.62, 0.56])
LIGHT = LIGHT / np.linalg.norm(LIGHT)


def _ellipsoid(h, xs, ys, cx, cy, rx, ry, rz, z=0.0):
    d = ((xs - cx) / rx) ** 2 + ((ys - cy) / ry) ** 2
    v = np.where(d < 1, np.sqrt(np.clip(1 - d, 0, 1)) * rz + z, -1)
    np.maximum(h, v, out=h)


def _capsule(h, xs, ys, a, b, ra, rb, z=0.0):
    ax, ay = a
    bx, by = b
    vx, vy = bx - ax, by - ay
    L2 = vx * vx + vy * vy
    t = np.clip(((xs - ax) * vx + (ys - ay) * vy) / L2, 0, 1)
    px, py = ax + t * vx, ay + t * vy
    r = ra + (rb - ra) * t
    d = ((xs - px) ** 2 + (ys - py) ** 2) / (r * r)
    v = np.where(d < 1, np.sqrt(np.clip(1 - d, 0, 1)) * r + z, -1)
    np.maximum(h, v, out=h)


# joints at 2x (x right, y down); the figure's own right is the viewer's left
J = {
    "head": (96, 30), "neck0": (96, 46), "neck1": (96, 60),
    "sh_r": (63, 68), "sh_l": (129, 66),
    "el_r": (50, 118), "wr_r": (52, 160), "hand_r": (53, 168),
    "el_l": (143, 112),
    "hip_r": (79, 142), "kn_r": (79, 198), "an_r": (81, 250),
    "hip_l": (113, 148), "kn_l": (119, 202), "an_l": (125, 248),
}


def concept():
    """The height field and the part map at 2x."""
    ys, xs = np.mgrid[0:CH, 0:CW].astype(float)
    h = np.full((CH, CW), -1.0)
    part = np.zeros((CH, CW), int)

    def add(fn, *args, pid=1, **kw):
        before = h.copy()
        fn(h, xs, ys, *args, **kw)
        part[h > before] = pid

    # legs first (the torso overlaps their tops)
    add(_capsule, J["hip_r"], J["kn_r"], 15, 10, pid=7)          # thigh, weight-bearing
    add(_ellipsoid, 76, 166, 13, 22, 10, z=6, pid=7)              # vastus, the thigh's swell
    add(_capsule, J["kn_r"], J["an_r"], 11, 6, pid=7)
    add(_ellipsoid, 77, 214, 12, 18, 9, z=3, pid=7)               # calf
    add(_ellipsoid, 83, 258, 12, 7, 6, pid=10)                    # foot, flat
    add(_capsule, J["hip_l"], J["kn_l"], 14, 10, pid=8)           # thigh, relaxed
    add(_ellipsoid, 116, 172, 12, 21, 9, z=5, pid=8)
    add(_capsule, J["kn_l"], J["an_l"], 10, 6, pid=8)
    add(_ellipsoid, 122, 218, 11, 17, 8, z=2, pid=8)
    add(_ellipsoid, 128, 256, 9, 6, 5, pid=11)                    # toes only: no heel
    # pelvis, tilted: the weight-side hip rides high; a smith's short wrap (perizoma)
    add(_ellipsoid, 96, 136, 27, 14, 13, z=8, pid=9)
    add(_ellipsoid, 96, 140, 29, 11, 9, z=13, pid=9)
    # torso
    add(_ellipsoid, 96, 92, 33, 34, 16, z=8, pid=4)               # ribcage
    add(_ellipsoid, 82, 77, 16, 11, 7, z=20, pid=4)               # pectorals
    add(_ellipsoid, 110, 77, 16, 11, 7, z=20, pid=4)
    for yy in (101, 113, 125):                                    # rectus abdominis
        add(_ellipsoid, 89.5, yy, 7, 5.5, 3, z=17, pid=4)
        add(_ellipsoid, 102.5, yy, 7, 5.5, 3, z=17, pid=4)
    add(_ellipsoid, 73, 114, 8, 16, 5, z=12, pid=4)               # obliques
    add(_ellipsoid, 119, 116, 8, 16, 5, z=12, pid=4)
    add(_capsule, J["neck0"], J["neck1"], 10, 12, z=6, pid=3)
    add(_ellipsoid, 96, 60, 22, 8, 6, z=12, pid=3)                # trapezius
    # arms
    add(_ellipsoid, *J["sh_r"], 12, 13, 8, z=12, pid=5)           # deltoids
    add(_ellipsoid, *J["sh_l"], 12, 13, 8, z=12, pid=6)
    add(_capsule, J["sh_r"], J["el_r"], 13, 10, z=6, pid=5)
    add(_ellipsoid, 55, 92, 11, 16, 8, z=8, pid=5)                 # biceps
    add(_capsule, J["el_r"], J["wr_r"], 10, 7, z=6, pid=5)
    add(_ellipsoid, 51, 132, 8, 12, 5, z=7, pid=5)                # forearm swell
    add(_ellipsoid, *J["hand_r"], 8, 9, 6, z=7, pid=12)           # the fist round the haft
    add(_capsule, J["sh_l"], J["el_l"], 13, 10, z=6, pid=6)
    add(_ellipsoid, 136, 88, 9, 14, 7, z=8, pid=6)
    # the head: skull, face, curls, beard
    add(_ellipsoid, 96, 30, 14, 18, 14, z=8, pid=1)
    for i, (cx, cy) in enumerate(((84, 18), (90, 13), (96, 12), (102, 13), (108, 18),
                                  (81, 27), (111, 27))):
        add(_ellipsoid, cx, cy, 6, 5, 5, z=16, pid=2)             # curls
    for cx, cy in ((86, 42), (96, 46), (106, 42), (91, 50), (101, 50)):
        add(_ellipsoid, cx, cy, 6, 6, 5, z=18, pid=2)             # beard
    add(_ellipsoid, 96, 34, 3.5, 6, 4, z=20, pid=1)               # the nose
    return h, part


def _shade(h):
    gy, gx = np.gradient(h)
    n = np.stack([-gx * 1.7, -gy * 1.7, np.ones_like(h)], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    diff = np.clip((n * LIGHT).sum(-1), 0, 1)
    refl = 2 * (n * LIGHT).sum(-1)[..., None] * n - LIGHT
    spec = np.clip(refl[..., 2], 0, 1) ** 14
    # cavity: how far a pixel sits below the average of its surroundings
    pad = np.pad(h, 4, mode="edge")
    k = sum(pad[4 + dy:4 + dy + h.shape[0], 4 + dx:4 + dx + h.shape[1]]
            for dy in (-4, 0, 4) for dx in (-4, 0, 4)) / 9
    cav = np.clip((k - h) / 3, 0, 1)
    return diff, spec, cav


def native():
    """1x pixels: a dict of (x, y) -> color name, and the native part map."""
    h, part = concept()
    diff, spec, cav = _shade(h)
    out = {}
    pmap = np.zeros((NH, NW), int)
    for y in range(NH):
        for x in range(NW):
            sl = np.s_[y * S:(y + 1) * S, x * S:(x + 1) * S]
            m = h[sl] >= 0
            if m.sum() < 2:
                continue
            d = diff[sl][m].mean()
            sp = spec[sl][m].max()
            cv_ = cav[sl][m].mean()
            pid = np.bincount(part[sl][m]).argmax()
            pmap[y, x] = pid
            if pid == 2:                       # curls and beard: darker, beaded
                d = d * 0.75
            if pid == 9:                       # the wrap: cloth, a step darker
                d = d * 0.85
            tone = 0.18 + d * 0.95 - cv_ * 0.45
            if tone < 0.36:
                name = "k_bz0"
            elif tone < 0.60:
                name = "k_bz1"
            elif tone < 0.82:
                name = "k_bz2"
            elif tone < 0.95:
                name = "k_bz3"
            else:
                name = "k_bz4"
            if sp > 0.45 and name in ("k_bz3", "k_bz4"):
                name = "k_gold"
            # patina gathers in the recesses, and runs down the legs
            if cv_ > 0.35 and name in ("k_bz1", "k_bz2") and (x * 7 + y * 3) % 5 < 2:
                name = "k_vg0" if name == "k_bz1" else "k_vg1"
            if pid in (7, 8, 10, 11) and y > 112 and (x * 5 + y * 11) % 13 == 0 and name != "k_gold":
                name = "k_vg1" if name in ("k_bz2", "k_bz3") else "k_vg0"
            out[(x, y)] = name
    hand_fix(out, pmap)
    outline(out)
    return out, pmap


def outline(out):
    """Selective outline: ink on the shadow side and the bottom, the ramp's
    darkest bronze on the lit side (STYLE §2)."""
    edge = {}
    for (x, y) in list(out):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) not in out:
                edge[(x, y)] = "ink" if (dx > 0 or dy > 0 or x > 48) else "k_bz1"
    out.update(edge)


def hand_fix(out, pmap):
    """The 1x pass: the face, the hammer, the stump, the casting seams."""
    def p(x, y, c):
        out[(x, y)] = c
    # eyes: inlaid, as the Riace bronzes' were (dark until Laurel 6)
    for x, y in ((44, 15), (45, 15), (51, 15), (52, 15)):
        p(x, y, "k_bk0")
    p(45, 14, "k_bz1"), p(52, 14, "k_bz1")
    for x in range(42, 47):
        p(x, 13, "k_bz1")                        # brows
    for x in range(50, 55):
        p(x, 13, "k_bz1")
    for y in (16, 17, 18):
        p(49, y, "k_bz1")                        # the nose's shadow side
    p(48, 19, "k_bz0"), p(49, 19, "k_bz0")
    for x in range(46, 52):
        p(x, 21, "k_bz0")                        # the mouth in the beard
    p(47, 20, "k_bz3"), p(48, 20, "k_bz3")       # the lit upper lip
    # beard curls: a dark dot in each
    for x, y in ((43, 22), (47, 24), (51, 22), (45, 25), (50, 25), (48, 23)):
        p(x, y, "k_bz0")
    # hair curls: lit crowns and dark centres
    for x, y in ((42, 8), (46, 5), (50, 5), (54, 8), (41, 12), (55, 12)):
        p(x, y, "k_bz0")
        p(x - 1, y - 1, "k_bz4")
    # the hammer: an ash haft down from the fist, a bronze head below the knee
    for y in range(87, 112):
        p(26, y, "k_bz0")
        p(27, y, "k_bz2")
        p(28, y, "k_bz1")
    for y in range(110, 120):
        for x in range(20, 35):
            k = "k_bz3" if y < 112 else "k_bz2" if x < 30 else "k_bz1"
            if x in (20, 34) or y == 119:
                k = "ink"
            p(x, y, k)
    for x in range(21, 34):
        p(x, 110, "k_bz4")
    # the stump: the forearm never cast; the clay core and an iron rod show
    for x in range(67, 78):
        for y in range(56, 60):
            if (x, y) in out:
                out[(x, y)] = "k_lv0" if (x + y) % 3 else "k_bk2"
    for y in range(58, 70):
        p(72 + (y - 58) // 6, y, "k_bk2")        # the armature rod
        p(73 + (y - 58) // 6, y, "k_bk0")
    for x in range(66, 79):
        if (x, 55) in out:
            out[(x, 55)] = "k_bz4"               # the raw cut edge, bright
    # casting seams: thin lit lines where the pieces were joined
    for x in range(36, 61):
        if pmap[30, x]:
            p(x, 30, "k_bz4")                    # neck to chest
    for x in range(34, 62):
        if pmap[63, x] and x % 2 == 0:
            p(x, 63, "k_bz1")                    # the waist joint
    # a smith's leather apron over the hips: a riveted belt, a flap to mid-thigh
    for y in range(62, 86):
        if y < 65:
            x0, x1 = 33, 63                       # the belt, round the hips
        else:
            x0 = 38 - (y - 65) // 5               # the flap widens as it falls
            x1 = 58 + (y - 65) // 5
        for x in range(x0, x1 + 1):
            if y < 65:
                k = "k_bz1" if y == 63 else "k_bz0"
            else:
                u = (x - x0) / max(1, x1 - x0)
                k = "k_bz1" if u < 0.45 else "k_bz0"
                if (x - x0) in (6, 13) and y > 67:
                    k = "k_bk0"                   # folds in the leather
                if u < 0.12:
                    k = "k_bz2"                   # the lit edge
            if x in (x0, x1) or y == 85:
                k = "ink"
            out[(x, y)] = k
            pmap[y, x] = 9
    for x in range(35, 63, 4):
        out[(x, 63)] = "k_gold"                   # bronze rivets on the belt
    for x, y in ((40, 70), (56, 70), (41, 80), (55, 80)):
        out[(x, y)] = "k_bz3"                     # and on the flap's corners
    # the heel that would not take: the left foot ends at the arch
    for y in range(124, 131):
        for x in range(56, 60):
            if (x, y) in out:
                out[(x, y)] = "k_lv0" if (x + y) % 2 else "k_bk1"
