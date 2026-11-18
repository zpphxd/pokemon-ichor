#!/usr/bin/env python3
"""Hand-drawn Gen 3 walkers, built from layered pixel parts (STYLE.md §3.6).

Every character shares one Gen 3 build (big head about half the height, short
sturdy body, feet on the bottom row) and is drawn from parts: a face, a body
garment, hair, beard, headwear, overgarments, a cape and props. Each part is a
hand-drawn grid per view (down, up, left) and, where it moves, per walk phase.
Parts are drawn without an outline; one continuous ink outline is added round
the finished silhouette, as Gen 3 does.

Grid symbols are roles, not colors; each character maps roles to its family
palette (graphics/object_events/palettes/ichor_<family>.pal):

  S s  skin, skin shade          e   eye (ink)
  H h  hair, hair shade          W w white / linen, its shade
  C c  garment, its shade        D d overgarment (himation, peplos fold)
  A    accent (belt, armband)    F   footwear
  M m  metal (bronze), shade     R r crest / shield field, shade
  X x  cape, its shade           P p wood (staff, spear shaft), shade
  k    explicit ink line

  python3 tools/ichor/art/walker_paint.py NAME [...] [--write] [--preview DIR]
"""
import argparse
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
PALS = ROOT / "graphics/object_events/palettes"
SHEETS = ROOT / "graphics/object_events/pics/people/ichor"
VIEWS = ("down", "up", "left")


import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import walker_parts as WP  # noqa: E402
from walker_parts import T, phases  # noqa: E402


# ── faces ────────────────────────────────────────────────────────────────────
FACE = {
    "down": phases(T(13, """
....SSSSSSSS....
...SSSSSSSSSS...
..SSSSSSSSSSSS..
..SSSSSSSSSSSS..
..SSSSSSSSSSSS..
..SSSSSSSSSSSS..
...SSSeSSeSSS...
...sSSeSSeSSs...
....ssSSSSss....
""")),
    "up": phases(T(13, """
....SSSSSSSS....
...SSSSSSSSSS...
..SSSSSSSSSSSS..
..SSSSSSSSSSSS..
..SSSSSSSSSSSS..
..SSSSSSSSSSSS..
...SSSSSSSSSS...
...sSSSSSSSSs...
....ssSSSSss....
""")),
    "left": phases(T(13, """
....SSSSSSS.....
...SSSSSSSSS....
..SSSSSSSSSSS...
..SSSSSSSSSSS...
..SSSSSSSSSSS...
.SSSSSSSSSSSS...
..SSeSSSSSSSS...
..SSeSSSSSSSs...
...sSSSSSSss....
""")),
}

# Eyes drawn as short level strokes (2x1) instead of the round 1x2 ones: a
# calm, steady look. Chosen per character with face="level".
FACE_LEVEL = {
    "down": phases(T(13, """
....SSSSSSSS....
...SSSSSSSSSS...
..SSSSSSSSSSSS..
..SSSSSSSSSSSS..
..SSSSSSSSSSSS..
..SSSSSSSSSSSS..
...SSSSSSSSSS...
...sSeeSSeeSs...
....ssSSSSss....
""")),
    "up": FACE["up"],
    "left": phases(T(13, """
....SSSSSSS.....
...SSSSSSSSS....
..SSSSSSSSSSS...
..SSSSSSSSSSS...
..SSSSSSSSSSS...
.SSSSSSSSSSSS...
..SSSSSSSSSSS...
..SeeSSSSSSSs...
...sSSSSSSss....
""")),
}
# Heavy brows and a square jaw: Rhea bare-headed, and Brasidas.
FACE_STERN = {
    "down": phases(T(13, """
....SSSSSSSS....
...SSSSSSSSSS...
..SSSSSSSSSSSS..
..SSSSSSSSSSSS..
..SSSSSSSSSSSS..
..SSkkSSSSkkSS..
...SSSeSSeSSS...
..ssSSeSSeSSss..
...ssSSSSSSss...
""")),
    "up": FACE["up"],
    "left": phases(T(13, """
....SSSSSSS.....
...SSSSSSSSS....
..SSSSSSSSSSS...
..SSSSSSSSSSS...
..SSSSSSSSSSS...
.SkkSSSSSSSSS...
..SSeSSSSSSSS...
..SSeSSSSSSSs...
..ssSSSSSSss....
""")),
}

# Iapetos's white tragic mask in place of a face: brows rising to the middle,
# hollow eyes, a mouth turned down (W/w, the holes in ink).
FACE_MASK = {
    "down": phases(T(13, """
....WWWWWWWW....
...WWWWWWWWWW...
..WWWWWWWWWWWW..
..WWWWWWWWWWWW..
..WWWkWWWWkWWW..
..WWkWWWWWWkWW..
...WkkWWWWkkW...
...wWWWkkWWWw...
....wwkWWkww....
""")),
    "up": FACE["up"],
    "left": phases(T(13, """
....WWWWWWW.....
...WWWWWWWWW....
..WWWWWWWWWWS...
..WkWWWWWWWWS...
..WWkWWWWWWWS...
.WkkWWWWWWWWS...
..kkWWWWWWWWs...
..WkWWWWWWWss...
...kkwwSSSss....
""")),
}
FACES = {"round": FACE, "level": FACE_LEVEL, "stern": FACE_STERN, "mask": FACE_MASK}

# ── bodies ───────────────────────────────────────────────────────────────────
_SHORT_DOWN = T(22, """
...CCCSSSSCCC...
..SOCcCCCCcCOS..
..SOCCCCCCCCOS..
..sOAAAAAAAAOs..
...cCCCCCCCCc...
....cCCCCCCc....
....SS....SS....
....Ss....sS....
...FFF....FFF...
""")
_SHORT_DOWN_A = T(22, """
...CCCSSSSCCC...
..SOCcCCCCcCOS..
..sOCCCCCCCCOS..
...OAAAAAAAAOS..
...cCCCCCCCCs...
....cCCCCCCc....
....SS....SS....
....Ss....FFF...
...FFF..........
""")
_SHORT_SIDE = (T(22, """
.....CCCCCC.....
....CCOSSCCC....
....CCOSSCCC....
....AAOssAAA....
....cCCCCCCc....
.....cCCCCc.....
.....SSSS.......
.....SsSs.......
....FFFFF.......
"""), T(22, """
.....CCCCCC.....
....CCCCSSCC....
....CCCCSSCC....
....AAAAAssA....
....cCCCCCCc....
.....cCCCCc.....
....SS...Ss.....
...Ss.....ss....
..FFF.....FFF...
"""), T(22, """
.....CCCCCC.....
....CSSCCCCC....
....CSSCCCCC....
....AssAAAAA....
....cCCCCCCc....
.....cCCCCc.....
....sS...SS.....
...ss.....Ss....
..FFF.....FFF...
"""))

_LONG_DOWN = T(22, """
...CCCSSSSCCC...
..SOCcCCCCcCOS..
..SOCCCCCCCCOS..
..sOCCCCCCCCOs..
...CCCCCCCCCC...
..cCCCCCCCCCCc..
..cCCCCCCCCCCc..
..ccCCCCCCCCcc..
...FF......FF...
""")
_LONG_DOWN_A = T(22, """
...CCCSSSSCCC...
..SOCcCCCCcCOS..
..sOCCCCCCCCOS..
...OCCCCCCCCOs..
...CCCCCCCCCCs..
..cCCCCCCCCCCc..
..cCCCCCCCCCCc..
..ccCCCCCCCCcc..
...FF...........
""")
_LONG_SIDE = (T(22, """
.....CCCCCC.....
....CCOSSCCC....
....CCOSSCCC....
....CCOssCCC....
....CCCCCCCC....
...cCCCCCCCCc...
...cCCCCCCCCc...
...ccCCCCCCcc...
..FFF...........
"""), T(22, """
.....CCCCCC.....
....CCCCSSCC....
....CCCCSSCC....
....CCCCssCC....
....CCCCCCCC....
...cCCCCCCCCc...
...cCCCCCCCCc...
...ccCCCCCCcc...
..FFF......FF...
"""), T(22, """
.....CCCCCC.....
....CSSCCCCC....
....CSSCCCCC....
....CssCCCCC....
....CCCCCCCC....
...cCCCCCCCCc...
...cCCCCCCCCc...
...ccCCCCCCcc...
..FF............
"""))


def _up(t):
    """The back view of a down-view body: the neck is behind the hair."""
    rows = list(t.rows)
    rows[0] = rows[0].replace("SSSS", "CCCC")
    u = T.__new__(T)
    u.start, u.rows = t.start, rows
    return u


BODY = {
    "chiton": {
        "down": phases(_SHORT_DOWN, _SHORT_DOWN_A),
        "left": _SHORT_SIDE,
    },
    "robe": {
        "down": phases(_LONG_DOWN, _LONG_DOWN_A),
        "left": _LONG_SIDE,
    },
}
# A long robe cut close: Iapetos is thin, and the skirt shows it.
BODY["robe_thin"] = {
    "down": phases(T(22, """
...CCCSSSSCCC...
..SOCcCCCCcCOS..
..SOCCCCCCCCOS..
..sOCCCCCCCCOs..
....CCCCCCCC....
...cCCCCCCCCc...
...cCCCCCCCCc...
...ccCCCCCCcc...
....FF....FF....
"""), T(22, """
...CCCSSSSCCC...
..SOCcCCCCcCOS..
..sOCCCCCCCCOS..
...OCCCCCCCCOs..
....CCCCCCCCs...
...cCCCCCCCCc...
...cCCCCCCCCc...
...ccCCCCCCcc...
....FF..........
""")),
    "left": (T(22, """
.....CCCCCC.....
....CCOSSCCC....
....CCOSSCCC....
....CCOssCCC....
.....CCCCCC.....
....cCCCCCCc....
....cCCCCCCc....
....ccCCCCcc....
...FFF..........
"""), T(22, """
.....CCCCCC.....
....CCCCSSCC....
....CCCCSSCC....
....CCCCssCC....
.....CCCCCC.....
....cCCCCCCc....
....cCCCCCCc....
....ccCCCCcc....
...FF.....FF....
"""), T(22, """
.....CCCCCC.....
....CSSCCCCC....
....CSSCCCCC....
....CssCCCCC....
.....CCCCCC.....
....cCCCCCCc....
....cCCCCCCc....
....ccCCCCcc....
...FF...........
""")),
}
for _b in BODY.values():
    _b["up"] = tuple(_up(t) for t in _b["down"])

# ── hair, beards, headwear ───────────────────────────────────────────────────
HAIR = {
    "short": {
        "down": phases(T(12, """
.....HHHHHH.....
...HHGGHHHHHH...
..HHGHHHHhHHHH..
..HHHHHhHHHHhH..
..HhHHHHHHHHHH..
..HHhHhHHhHhHH..
..HH.h....h.HH..
..H..........H..
""")),
        "up": phases(T(12, """
.....HHHHHH.....
...HHGGHHHHHH...
..HHGHHHHhHHHH..
..HHHHHhHHHHhH..
..HhHHHHHHHHHH..
..HHHHhHHHHHhH..
..HhHHHHHHhHHH..
...hHHhHHHHHh...
....hhhhhhhh....
""")),
        "left": phases(T(12, """
.....HHHHHH.....
...HHGGHHHHH....
..HHGHHHhHHHH...
..HHHHhHHHHhH...
..HhHHHHHHHHH...
...hh.HHHhHHH...
.......HHHHhH...
........hHHHH...
.........hhh....
""")),
    },
    "bald_fringe": {
        "down": phases(T(13, """
.....GG.........
................
................
..W..........W..
..WW........WW..
..Ww........wW..
""")),
        "up": phases(T(13, """
.....GGG........
................
................
..WWWWWWWWWWWW..
..WWWWWWWWWWWW..
..wWWWWWWWWWWw..
...wwwwwwwwww...
""")),
        "left": phases(T(13, """
.....GG.........
................
................
.......WWWWWW...
.......WWWWWW...
........WWwWW...
.........www....
""")),
    },
}

BEARD = {
    "long_white": {
        "down": phases(T(20, """
..W..........W..
..sWWWWWWWWWWs..
...WWWWWWWWWW...
....WWWWWWWW....
.....WWWWWW.....
.....wWWWWw.....
......wwww......
""")),
        "up": phases(T(21, """
..W..........W..
""")),
        "left": phases(T(20, """
..W.............
.WWWWWW.........
.WWWWWW.........
..WWWWW.........
..wWWWw.........
...www..........
""")),
    },
}

HEADWEAR = {
    "kerchief": {
        "down": phases(T(13, """
....WWWWWWWW....
...WWWWWWWWWW...
..WWWWWWWWWWWW..
..wWWWWWWWWWWw..
..HH........HH..
..HH........HH..
..H..........H..
""")),
        "up": phases(T(13, """
....WWWWWWWW....
...WWWWWWWWWW...
..WWWWWWWWWWWW..
..WWWWWWWWWWWW..
..wWWWWWWWWWWw..
..HHHHHHHHHHHH..
..HHHHHHHHHHHH..
..hHHHHHHHHHHh..
...hHHHHHHHHh...
....hhHHHHhh....
""")),
        "left": phases(T(13, """
....WWWWWWW.....
...WWWWWWWWW....
..WWWWWWWWWWW...
..wWWWWWWWWWW...
......wWWWWWW...
.......HHHHHH...
.......HHHHHH...
........hHHHH...
.........hHHH...
""")),
    },
    "helmet_crest": {
        "down": phases(T(7, """
......RRRR......
.....RRRRRR.....
.....RrRRrR.....
......rRRr......
.....MMMMMM.....
...MMMMMMMMMM...
..MmMMMMMMMMmM..
..mm........mm..
..m..........m..
""")),
        "up": phases(T(7, """
......RRRR......
.....RRRRRR.....
.....RRRRRR.....
......rRRr......
.....MMMMMM.....
...MMMMMMMMMM...
..MMMMMMMMMMMM..
..mMMMMMMMMMMm..
..mmMMMMMMMMmm..
...mmmmmmmmmm...
""")),
        "left": phases(T(7, """
.....RRRRRR.....
...RRRRRRRRRR...
..RRrrrrrrrrRR..
...r.......rRR..
.....MMMMMM.....
...MMMMMMMMMM...
..MmMMMMMMMMM...
..m...MMMMMMM...
......mMMMMMM...
.......mmmmm....
""")),
    },
}

# ── overgarments, capes, props ───────────────────────────────────────────────
OVER = {
    "himation": {  # draped over the left shoulder, across the body
        "down": phases(T(22, """
..........DDD...
.........DDDDS..
........DDDDdS..
.......DDDDd.S..
......DDDDd..s..
.....DDDDd......
....dDDDd.......
....ddd.........
""")),
        "up": phases(T(22, """
...DDD..........
..SDDDD.........
..SdDDDD........
..S.dDDDD.......
..s..dDDDD......
......dDDDD.....
.......dDDDd....
.........ddd....
""")),
        "left": phases(T(22, """
.......DDD......
......DDDDD.....
.....DDDDDd.....
....DDDDDd......
....DDDDd.......
....dDDd........
""")),
    },
    "corselet": {
        "down": phases(T(22, """
...WWWSSSSWWW...
...WWWWWWWWWW...
...WWWWWWWWWW...
...wwwwwwwwww...
""")),
        "up": phases(T(22, """
...WWWWWWWWWW...
...WWWWWWWWWW...
...WWWWWWWWWW...
...wwwwwwwwww...
""")),
        "left": phases(T(22, """
.....WWWWWW.....
....WWWWWWWW....
....WWW..WWW....
....www..www....
""")),
    },
    "armband": {
        "down": phases(T(24, """
..A.............
""")),
        "up": phases(T(24, """
.............A..
""")),
        "left": phases(T(24, """
................
""")),
    },
    "greaves": {
        "down": phases(T(28, """
....MM....MM....
....mm....mm....
"""), T(28, """
....MM....MM....
....mm..........
""")),
        "up": phases(T(28, """
....MM....MM....
....mm....mm....
"""), T(28, """
....MM....MM....
....mm..........
""")),
        "left": phases(T(28, """
.....MMMM.......
.....mmmm.......
"""), T(28, """
....MM...mm.....
...mm.....mm....
"""), T(28, """
....mm...MM.....
...mm.....mm....
""")),
    },
}

CAPE = {  # drawn behind the body, except from behind
    "chlamys": {
        "down": phases(T(22, """
..X..........X..
.XX..........XX.
.XX..........XX.
.xX..........Xx.
..x..........x..
""")),
        "up": phases(T(22, """
..XXXXXXXXXXXX..
..XXXXXXXXXXXX..
..XXXXXXXXXXXX..
..XXXXXXXXXXXX..
..xXXXXXXXXXXx..
..xXXXXXXXXXXx..
...xxXXXXXXxx...
""")),
        "left": phases(T(22, """
..........X.....
..........XX....
..........XXX...
..........XXX...
..........XXXX..
..........xXXX..
...........xxx..
""")),
    },
}

PROP = {
    "staff": {
        "down": phases(T(16, "\n".join([".p.............."] + [".P.............."] * 17))),
        "up": phases(T(16, "\n".join(["..............p."] + ["..............P."] * 17))),
        "left": phases(T(16, "\n".join([".p.............."] + [".P.............."] * 17))),
    },
    "spear": {
        "down": phases(T(7, "\n".join(["..............M."] * 3 + ["..............p."] * 23))),
        "up": phases(T(7, "\n".join([".M.............."] * 3 + [".p.............."] * 23))),
        "left": phases(T(7, "\n".join(["...........M...."] * 3 + ["...........p...."] * 23))),
    },
    "hoplon": {
        "down": phases(T(24, """
..MMMM..........
.MRRRRM.........
MRRRRRRM........
MRRMMRRM........
MRRMMRRM........
MRRRRRRM........
.MRRRRM.........
..MMMM..........
""")),
        "up": phases(T(24, """
..........MMMM..
.........MrrrrM.
........MrrrrrrM
........MrrrrrrM
........MrrrrrrM
........MrrrrrrM
.........MrrrrM.
..........MMMM..
""")),
        "left": phases(T(24, """
...MMMMMM.......
..MRRRRRRM......
..MRRMMRRM......
..MRRMMRRM......
..MRRRRRRM......
...MMMMMM.......
""")),
    },
}

# ── the shared library: these parts plus walker_parts.py ─────────────────────
HAIR.update(WP.HAIR)
BEARD.update(WP.BEARD)
HEADWEAR.update(WP.HEADWEAR)
OVER.update(WP.OVER)
CAPE.update(WP.CAPE)
HELD = dict(WP.HELD)
HELD["hoplon"] = PROP.pop("hoplon")
PROP.update(WP.PROP)

OVER["exomis"] = {  # one shoulder bare (the wearer's right)
    "down": phases(T(22, """
...SSSS.........
..SSS...........
""")),
    "up": phases(T(22, """
.........SSSS...
...........SSS..
""")),
    "left": phases(T(22, """
................
""")),
}
OVER["belt"] = {
    "down": phases(T(25, """
...AAAAAAAAAA...
""")),
    "up": phases(T(25, """
...AAAAAAAAAA...
""")),
    "left": phases(T(25, """
....AAAAAAAA....
""")),
}
HELD["lyre_play1"] = {"down": phases(T(21, """
.....M..M.......
.....M..M.......
.....MWWM.S.....
.....MWWMS......
.....mMMm.......
"""))}
HELD["lyre_play2"] = {"down": phases(T(21, """
.....M..M.......
.....M..M.......
.....MWWM.......
.....MWWM.......
.....mMMmS......
..........S.....
"""))}
HELD["lyre_rest"] = {"down": phases(T(21, """
.....M..M.......
.....M..M.......
.....MWWM.......
.....MWWM.......
.....mMMm.......
"""))}
HELD["hands_folded"] = {"down": phases(T(26, """
.......SS.......
"""))}

FACE_CLOSED = phases(T(19, """
...SSSSSSSSSS...
...sSkkSSkkSs...
"""))


def _kilt(t, rows=3):
    """A bare-chested body from a tunic body: the top rows' cloth becomes skin."""
    u = T.__new__(T)
    u.start = t.start
    u.rows = [r.replace("C", "S").replace("c", "s") if i < rows else r for i, r in enumerate(t.rows)]
    return u


BODY["kilt"] = {v: tuple(_kilt(t) for t in BODY["chiton"][v]) for v in VIEWS}

# Running: a wider stride, the arms pumping, the body leaning into it.
_RUN_DOWN_A = T(22, """
...CCCSSSSCCC...
..SOCcCCCCcCOS..
..sOCCCCCCCCOS..
...OAAAAAAAAOs..
...cCCCCCCCCs...
....cCCCCCCc....
...SS......SS...
..FFF......Ss...
...........FFF..
""")
_RUN_LEFT_A = T(22, """
.....CCCCCC.....
....CSSOCCCC....
...SsAOAAAAA....
....cCCCCCCc....
.....cCCCCc.....
....SS...sS.....
...Ss.....Ss....
..Ss.......ss...
.FF.........FF..
""")
_RUN_LEFT_B = T(22, """
.....CCCCCC.....
....CCCCOSSC....
....AAAAOssAS...
....cCCCCCCc....
.....cCCCCc.....
....sS...SS.....
...ss.....Ss....
..ss.......Ss...
.FF.........FF..
""")
BODY["chiton_run"] = {
    "down": phases(BODY["chiton"]["down"][0], _RUN_DOWN_A),
    "up": phases(BODY["chiton"]["up"][0], _up(_RUN_DOWN_A)),
    "left": (BODY["chiton"]["left"][0], _RUN_LEFT_A, _RUN_LEFT_B),
}
BODY["child"] = {
    "down": phases(T(25, """
...SOCCCCCCOS...
...SOCCCCCCOS...
...sOCCCCCCOs...
....cCCCCCCc....
.....SS..SS.....
.....FF..FF.....
"""), T(25, """
...SOCCCCCCOS...
...sOCCCCCCOS...
....OCCCCCCOs...
....cCCCCCCc....
.....SS..FF.....
.....FF.........
""")),
    "left": (T(25, """
.....CCCCCC.....
.....COSSCC.....
.....COssCC.....
.....cCCCCc.....
......SSS.......
.....FFFF.......
"""), T(25, """
.....CCCCCC.....
.....CCOSSC.....
.....CCOssC.....
.....cCCCCc.....
.....SS..Ss.....
....FF....FF....
"""), T(25, """
.....CCCCCC.....
.....OSSCCC.....
.....OssCCC.....
.....cCCCCc.....
.....sS..SS.....
....FF....FF....
""")),
}
BODY["child"]["up"] = BODY["child"]["down"]
BODY["seated"] = {"up": phases(T(25, """
...CCCCCCCCCC...
..SOCCCCCCCCOS..
..SOCCCCCCCCOS..
..cCCCCCCCCCCc..
..cCCCCCCCCCCc..
...cccccccccc...
"""))}

# ── characters ───────────────────────────────────────────────────────────────
# Default roles per family palette (ichor_<family>.pal); each character
# overrides what it wears. Q/q: flame, coal, fruit. L/l: leaves. Y/y: hat,
# veil, hood. B: band, ribbon. N/n: net, strap, purse. O: soft outline.
CAST = dict(S=7, s=6, e=1, k=1, O=2, G=4, H=2, h=1, C=11, c=10, W=11, w=10, A=8, F=2,
            M=8, m=4, R=5, r=3, X=5, x=3, P=4, p=2, D=13, d=12, N=2, n=1, Q=9, q=5,
            L=15, l=4, Y=14, y=1, B=13)
FOLK = dict(S=7, s=6, e=1, k=1, O=2, G=6, H=2, h=1, C=12, c=11, W=9, w=8, A=4, F=2,
            M=4, m=6, R=3, r=2, X=3, x=2, P=6, p=2, D=4, d=6, N=2, n=1, Q=5, q=3,
            L=15, l=14, Y=3, y=2, B=3)
THEO = dict(S=9, s=8, e=1, k=1, O=2, G=4, H=3, h=2, C=11, c=10, W=11, w=10, A=6, F=3,
            M=6, m=5, R=5, r=3, X=3, x=2, P=4, p=2, D=12, d=13, N=2, n=1, Q=7, q=6,
            L=15, l=14, Y=12, y=13, B=6)
WINE = dict(S=7, s=6, e=1, k=1, O=2, G=6, H=2, h=1, C=8, c=10, W=9, w=8, A=5, F=2,
            M=5, m=4, R=3, r=11, X=3, x=11, P=6, p=2, D=12, d=11, N=2, n=1, Q=12, q=11,
            L=15, l=14, Y=12, y=11, B=5)
# The player's palettes (brendan.pal / may.pal) are shared by every player
# sheet (walking, running, surfing, fishing, bikes...), so they stay as they are.
THEO_PAL = dict(S=1, s=2, e=15, k=15, O=4, G=3, H=4, h=15, C=14, c=9, W=14, w=9, A=3, F=4,
                M=11, m=13, R=13, r=4, X=6, x=7, P=3, p=4, D=6, d=7, N=3, n=4, Q=10, q=13,
                L=11, l=13, Y=10, y=11, B=13)
IANTHE_PAL = dict(THEO_PAL, H=7, h=8, X=5, x=6, D=5, d=6)
PLAYER_PALS = ("brendan", "may")
FAMILY = {"cast": CAST, "folk": FOLK, "theoxenia": THEO, "wine": WINE,
          "brendan": THEO_PAL, "may": IANTHE_PAL}


def C_(family, roles=None, **parts):
    spec = dict(family=family, **parts)
    spec["roles"] = dict(FAMILY[family], **(roles or {}))
    return spec


_KLEON = dict(body="chiton", hair="short", cape="chlamys", over=["exomis", "armband"])
CHARACTERS = {
    # the named cast
    "kleon": C_("cast", dict(H=2, h=1, C=11, c=10, A=8, X=5, x=3), **_KLEON),
    "kleon_seasick": C_("cast", dict(S=10, s=15, C=11, c=10, X=5, x=3), head_dy=1,
                        held=["hand_mouth"], **_KLEON),
    "kleon_tablet": C_("cast", dict(C=11, c=10, X=5, x=3, Y=14, y=1), held=["tablet"], **_KLEON),
    "alethea": C_("cast", dict(H=2, h=1, B=13, C=8, c=4, A=2, N=2, W=11, w=10, M=10, P=4),
                  body="chiton", hair="ponytail", over=["satchel"], held=["trowel"]),
    "professor_daphne": C_("cast", dict(H=4, h=2, G=8, B=15, L=15, l=4, C=13, c=12, D=11, d=10,
                                         W=11, w=10),
                           body="robe", hair="bun", headwear=["wreath"], over=["himation"],
                           held=["scroll"]),
    "hierophant_ione": C_("cast", dict(C=4, c=3, Y=11, y=10, M=8, m=4, Q=9, q=5),
                          body="robe", hair="short", headwear=["veil_long"], held=["lamp_both"]),
    "titan_grunt": C_("cast", dict(C=14, c=1, A=9, M=8, m=4, R=5, r=3),
                      body="chiton", headwear=["helmet_closed"],
                      over=["shoulder_guards", "greaves", "emblem"]),
    "kerykos": C_("cast", dict(H=10, h=4, C=11, c=10, Y=14, y=1, X=3, x=1, M=8, L=4),
                  body="chiton", hair="short", beard="full", headwear=["petasos"],
                  cape="chlamys", props=["kerykeion"]),
    # classes (cast palette)
    "hoplite": C_("cast", dict(C=5, c=3, W=11, w=10, M=8, m=4, R=5, r=3, P=4, p=2, A=8),
                  body="chiton", hair="short", headwear=["helmet_crest"],
                  over=["corselet", "greaves"], held=["hoplon"], props=["spear"]),
    "shepherd": C_("cast", dict(H=2, C=13, c=12, Y=8, y=4, W=11, w=10, P=4, p=2),
                   body="chiton", hair="short", headwear=["pilos"], over=["sheepskin"],
                   props=["crook"]),
    "augur": C_("cast", dict(H=11, h=10, G=11, W=11, w=10, B=9, C=13, c=12, D=14, d=1, P=4, p=2),
                body="robe", hair="curly", beard="long_white", headwear=["band", "feather"],
                over=["himation"], props=["staff"]),
    "acolyte_m": C_("cast", dict(H=14, h=1, G=14, C=11, c=10, D=9, d=8, A=8, M=8, m=4, Q=5, q=3),
                    body="chiton", hair="crop", over=["waist_wrap", "soot"], held=["tongs"]),
    "acolyte_f": C_("cast", dict(H=4, h=3, G=9, B=9, C=11, c=10, P=4, p=2, Q=9, q=5),
                    body="robe", hair="bun", held=["lamp_high"]),
    # townsfolk (folk palette)
    "mom": C_("folk", dict(H=2, h=1, G=6, B=5, C=3, c=2, W=9, w=8),
              body="robe", hair="bun", over=["apron"]),
    "woman": C_("folk", dict(H=2, h=1, C=12, c=11, W=9, w=8, D=4, d=6),
                body="robe", headwear=["kerchief"], over=["himation"]),
    "man": C_("folk", dict(H=2, h=1, C=4, c=6, A=2),
              body="chiton", hair="short", beard="full", over=["exomis"]),
    "elder_m": C_("folk", dict(C=15, c=14, W=9, w=10, P=6, p=2, G=9),
                  body="robe", hair="bald_fringe", beard="long_white", props=["staff"]),
    "elder_f": C_("folk", dict(H=10, h=2, G=8, Y=2, y=1, C=8, c=10, B=3),
                  body="robe", hair="long", headwear=["hood"], over=["blush"]),
    "youth_m": C_("folk", dict(H=2, h=1, G=6, L=15, l=14, B=3, C=9, c=8, A=4),
                  body="chiton", hair="short", headwear=["wreath"]),
    "youth_f": C_("folk", dict(H=2, h=1, G=6, B=3, C=13, c=12, A=9),
                  body="robe", hair="braid", over=["belt"]),
    "kid_m": C_("folk", dict(H=2, h=1, G=6, C=3, c=2, F=6),
                body="child", hair="curly", head_dy=3),
    "kid_f": C_("folk", dict(H=2, h=1, G=6, B=3, C=5, c=4, F=6),
                body="child", hair="pigtails", head_dy=3),
    "fisher": C_("folk", dict(H=10, h=2, Y=2, y=1, C=13, c=12, A=8, N=8, n=10),
                 body="chiton", hair="short", beard="full", headwear=["pilos"], over=["net"]),
    "sailor": C_("folk", dict(H=2, h=1, G=6, B=3, C=8, c=10, A=12),
                 body="kilt", hair="short", beard="jaw", headwear=["band"]),
    "diver": C_("folk", dict(H=1, h=1, G=11, C=13, c=12, A=9, F=6, N=10, n=2, Q=5),
                body="chiton", hair="long", held=["net_bag"]),
    "healer": C_("folk", dict(H=2, h=1, G=6, B=15, A=15, C=9, c=8, P=6, p=2, L=15, l=14),
                 body="robe", hair="long", headwear=["band"], over=["sash"], props=["rod"],
                 extra=["bow"]),
    "merchant": C_("folk", dict(H=2, h=1, W=2, w=1, G=9, C=9, c=8, D=12, d=11, N=2, n=1),
                   body="robe", hair="bald_fringe", beard="full", over=["himation", "purse"]),
    "harvester": C_("folk", dict(H=2, h=1, Y=3, y=2, C=15, c=14, W=9, w=8, P=4, p=6, L=14, l=15),
                    body="robe", headwear=["scarf"], over=["apron"], held=["basket"]),
    "goatherd": C_("folk", dict(H=10, h=2, G=9, C=8, c=10, A=6, X=2, x=1, M=4, m=2, P=6, p=2),
                   body="chiton", hair="curly", beard="full", cape="cloak_long",
                   over=["bell"], held=["syrinx"]),
    "aiakides": C_("folk", dict(H=9, h=10, G=9, W=9, w=10, C=9, c=8, X=3, x=2, P=6, p=2),
                   body="robe", hair="curly", beard="long_white", cape="cloak_long",
                   props=["staff"]),
    "endeis": C_("folk", dict(H=3, h=2, G=4, C=4, c=6, W=9, w=8),
                 body="robe", hair="long", over=["apron"]),
    "kedalion": C_("folk", dict(H=2, h=1, W=2, w=1, G=9, C=10, c=2, A=2),
                   body="chiton", hair="bald_fringe", beard="full"),
    "manto": C_("folk", dict(H=9, h=10, G=9, Y=9, y=8, C=12, c=11, P=6, p=2),
                body="robe", hair="long", headwear=["veil_long"], props=["staff"]),
    "pheidon": C_("folk", dict(H=2, h=1, G=6, C=9, c=8, D=3, d=2, P=6, p=2),
                  body="chiton", hair="short", over=["himation"], props=["staff"]),
    "pilgrim": C_("folk", dict(Y=12, y=11, X=12, x=11, C=12, c=11, W=9, w=8, A=5, P=6, p=2),
                  body="robe", hair="short", headwear=["hood"], cape="cloak_long",
                  over=["front_panel"], props=["staff"]),
    "priestess": C_("folk", dict(H=10, h=2, Y=5, y=4, C=9, c=8, A=5, p=2),
                    body="robe", hair="long", headwear=["veil_long"], over=["belt"],
                    props=["spindle"]),
    # Alfred of Waltz Chariots: a wheelwright from the far east, come in by sea.
    # Black hair in a topknot tied with red, a deep-blue robe, a red sash, and a
    # leather work apron for the trade.
    "alfred": C_("folk", dict(H=1, h=2, G=11, B=3, C=12, c=11, W=6, w=2, A=3),
                 body="robe", hair="bun", over=["apron", "sash"], face="level"),
    # Knossa (design/phase4/SCRIPT.md III-3D, LABYRINTH.md §8). Ariadne, priestess of the
    # Mistress of the Labyrinth: black Minoan curls under a gold diadem, a Minoan-red
    # flounced robe banded in saffron. Sarpedon, the old bull-master: grey fringe and
    # beard, a leaper's red kilt-chiton and an ochre belt, thirty summers of scars.
    "ariadne": C_("cast", dict(H=2, h=1, B=9, C=5, c=3, A=9, D=8, d=4, W=11, w=10, M=9, m=8),
                  body="robe", hair="long", headwear=["band"], over=["stripes"]),
    "sarpedon": C_("folk", dict(H=10, h=8, W=9, w=8, C=3, c=2, A=4, P=6, p=2),
                   body="chiton", hair="bald_fringe", beard="full", over=["belt"], props=["staff"]),
    "pronomos": C_("folk", dict(H=2, h=1, G=6, C=9, c=8, A=3, P=6, p=2),
                   body="chiton", hair="curly", held=["aulos"]),
    # the Theoxenia
    "sam": C_("theoxenia", dict(H=2, h=1, G=3, C=11, c=10, A=4, X=3, x=2, M=6, m=5, W=11),
              body="chiton", hair="curly", cape="cloak_long", held=["lyre"],
              extra=["strum1", "strum2", "strum3"]),
    "apollo": C_("theoxenia", dict(H=2, h=1, G=3, C=11, c=10, A=6, L=6, l=5, M=6, m=5, W=11),
                 body="robe", hair="curly", headwear=["wreath"], held=["lyre"],
                 extra=["strum1", "strum2", "strum3"]),
    "cami": C_("theoxenia", dict(H=3, h=2, G=4, C=11, c=10, D=12, d=13),
               body="robe", hair="long", over=["himation"], extra=["sit", "rise"]),
    # the climax (design/phase4/SCRIPT.md III-9 to III-12), on the theoxenia
    # palette so they keep their color in the Frozen Hour without coloring the
    # cast and folk standing frozen round them.
    # Phaedon: the healer of Astyra in his plain white chiton, a gold sash, the
    # gold mask he no longer wears held at his side.
    "phaedon": C_("theoxenia", dict(H=13, h=2, G=12, C=11, c=10, W=11, w=10, A=6, M=6, m=5),
                  body="robe", hair="short", beard="jaw", over=["sash"], held=["mask"]),
    # Hyperion: the big bronze-breasted Titan of light, bareheaded, his eyes
    # clouded white (the eye role mapped to pale linen).
    # Kleon after he breaks his own thread (III-10G): the same boy, redrawn on the
    # theoxenia palette so his color can't spill onto the frozen Titanborn.
    "kleon_free": C_("theoxenia", dict(H=13, h=1, C=11, c=10, A=6, X=4, x=3), **_KLEON),
    "hyperion": C_("theoxenia", dict(H=3, h=2, G=12, e=10, C=13, c=2, A=6, M=6, m=5, R=6, r=5,
                                     X=3, x=2, F=2),
                   body="chiton", hair="bald_fringe", beard="full", cape="cloak_long",
                   over=["corselet", "greaves"]),
    "demeter": C_("theoxenia", dict(H=6, h=5, G=7, L=7, l=5, B=5, C=15, c=14, D=6, d=5),
                  body="robe", hair="long", headwear=["wreath"], over=["himation"]),
    # the wine palette
    "actor": C_("wine", dict(H=2, h=1, G=6, C=3, c=11, A=5, B=5, W=9, w=8),
                body="robe", hair="short", headwear=["band"], over=["stripes"], held=["mask"]),
    "vintner": C_("wine", dict(H=2, h=1, Y=12, y=11, C=8, c=10, A=2, Q=12, q=11, L=15),
                  body="chiton", hair="short", headwear=["cap"], held=["grapes"]),
    # Lakonia (Act III). Rhea, the Titan admin: a closed Corinthian helmet with
    # the sickle on its cheek-pieces, a chain round her left forearm, slate
    # robes under bronze shoulder-guards and a long cloak of Lakonian red.
    "rhea": C_("cast", dict(C=14, c=1, M=8, m=4, R=1, r=14, W=11, N=10, n=1, X=3, x=1, A=8),
               body="robe", headwear=["helmet_corinthian"], over=["shoulder_guards", "emblem", "chain"],
               cape="cloak_long"),
    # ...and the same woman with the helmet off (III-5E): gray hair pinned up,
    # Kleon's heavy brows and a square jaw.
    "rhea_unmasked": C_("cast", dict(H=10, h=14, B=10, C=14, c=1, M=8, m=4, N=10, n=1, X=3, x=1, A=8),
                        body="robe", hair="bun", face="stern",
                        over=["shoulder_guards", "emblem", "chain"], cape="cloak_long"),
    # Iapetos, the Voice: a thin man in a white tragic mask, a wax tablet on a
    # cord at his neck, his writing hand black with ink to the wrist.
    "iapetos": C_("cast", dict(H=1, h=14, C=12, c=1, W=11, w=10, P=4, p=2, Y=9, I=14),
                  body="robe_thin", hair="crop", face="mask", over=["neck_tablet", "ink_hand"]),
    # A Gigas: a giant in a closed helmet under a tall black crest, a cuirass of
    # bronze scales, guards and greaves.
    "gigas": C_("cast", dict(C=14, c=1, M=8, m=4, R=3, r=1, A=8),
                body="chiton", headwear=["helmet_gigas"], over=["scales", "shoulder_guards", "greaves"]),
    # A battle-school boy: cropped hair, a coarse tunic, bare feet and the one
    # short red cloak he gets a year.
    "cadet": C_("cast", dict(H=2, h=1, C=10, c=4, A=4, X=5, x=3, F=7),
                body="chiton", hair="crop", cape="chlamys"),
    # A Lakonian girl on her run: a short red chiton, hair tied back, bare feet.
    "cadet_f": C_("cast", dict(H=2, h=1, B=11, C=5, c=3, A=8, F=7),
                  body="chiton", hair="ponytail"),
    # Brasidas, the Polemarch: big, gray-bearded, a plain red cloak, arms folded.
    "brasidas": C_("cast", dict(H=10, h=10, C=10, c=4, X=5, x=3, A=4),
                   body="chiton", hair="short", beard="full", face="stern", cape="cloak_long",
                   held=["arms_folded"]),
}

# The player: the traveler's petasos and blue chlamys over a linen tunic, a
# satchel strap across the chest. Ianthe wears her braid down her back.
PLAYERS = {
    "theo": C_("brendan", None, body="chiton", hair="short", headwear=["petasos"],
               cape="chlamys", over=["satchel"]),
    "ianthe": C_("may", None, body="chiton", hair="long", headwear=["petasos"],
                 cape="chlamys", over=["satchel"]),
}
PLAYER_DIR = {"theo": "brendan", "ianthe": "may"}


def read_pal(family):
    path = PALS / (f"{family}.pal" if family in PLAYER_PALS else f"ichor_{family}.pal")
    v = list(map(int, path.read_text().split()[3:]))
    return np.array(v, int).reshape(-1, 3)[:16]


def stamp(grid, part, view, phase, behind=False, dy=0, dx=0):
    if not part or view not in part:
        return
    t = part[view][phase]
    if view == "left" and phase == 2:
        # same()/phases() make step B by mirroring step A, which is right seen
        # from the front or back but turns a profile round to face the other
        # way every other stride. In profile a mirrored B means "no B of its
        # own": keep A's facing. Bodies that draw a real B are untouched.
        a = part[view][1]
        if t.start == a.start and t.rows == [r[::-1] for r in a.rows] and t.rows != a.rows:
            t = a
    for i, row in enumerate(t.rows):
        y = t.start + i + dy
        if not 0 <= y < 32:
            continue
        for x, ch in enumerate(row):
            x += dx
            if ch != "." and 0 <= x < len(grid[0]) and (not behind or grid[y][x] == "."):
                grid[y][x] = ch


DARK_EDGE = set("HhGekMmRrXxPpFADYyNnQqLl")


def outline(grid):
    """One continuous outline round the silhouette (4-way), tinted like Gen 3:
    ink beside hair, metal, crests, capes, hats and wood; a dark brown ("O")
    beside skin and light cloth, so faces and linen don't sit in a black line."""
    out = [row[:] for row in grid]
    W = len(grid[0])
    for y in range(32):
        for x in range(W):
            if grid[y][x] != ".":
                continue
            near = [grid[y + dy][x + dx] for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))
                    if 0 <= y + dy < 32 and 0 <= x + dx < W and grid[y + dy][x + dx] not in ".kO"]
            if near:
                out[y][x] = "k" if any(c in DARK_EDGE for c in near) else "O"
    return out


POSES = {
    # pose: (view, phase, head offset, eyes shut, body override, held override)
    "strum1": ("down", 0, 0, False, None, ["lyre_play1"]),
    "strum2": ("down", 0, 0, False, None, ["lyre_play2"]),
    "strum3": ("down", 0, 0, True, None, ["lyre_rest"]),
    "bow": ("down", 0, 2, True, None, ["hands_folded"]),
    "sit": ("up", 0, 3, False, "seated", []),
    "rise": ("up", 0, 1, False, None, []),
}


def frame(spec, view, phase, pose=None, run=False, width=16, x0=0, body_override=None,
          head_dy=0, extra_held=(), drawings=(), thin=()):
    """One frame. width/x0 place the 16-wide figure on a wider canvas (the
    32x32 player poses); drawings(grid) run before the outline, thin(grid)
    after it (rods and sparkles, one pixel, no outline of their own)."""
    g = [["."] * width for _ in range(32)]
    dy = spec.get("head_dy", 0) + head_dy
    dx = 0
    shut = False
    body = spec["body"]
    if body_override:
        body = body_override
    if run:
        body = body + "_run"
        if phase:  # mid-stride: the head dips, and leans forward in profile
            dy += 1
            dx = -1 if view == "left" else 0
    held = [HELD[h] for h in spec.get("held", [])]
    if pose:
        view, phase, pdy, shut, pbody, pheld = POSES[pose]
        dy += pdy
        body = pbody or body
        if pheld is not None:
            held = [HELD[h] for h in pheld]
    held = held + [HELD[h] for h in extra_held]
    get = lambda table, key: table.get(key) if key else None  # noqa: E731
    X = x0  # the figure's left edge on the canvas
    cape = get(CAPE, spec.get("cape"))
    if view != "up":
        stamp(g, cape, view, phase, dx=X)
    else:
        for h in held:
            stamp(g, h, view, phase, dx=X)
    stamp(g, BODY[body], view, phase, dx=X)
    for o in spec.get("over", []):
        stamp(g, OVER[o], view, phase, dy=dy if o in ("soot", "blush") else 0, dx=X)
    stamp(g, FACES[spec.get("face", "round")], view, phase, dy=dy, dx=dx + X)
    if shut and view == "down":
        stamp(g, {"down": FACE_CLOSED}, view, 0, dy=dy, dx=dx + X)
    stamp(g, get(HAIR, spec.get("hair")), view, phase, dy=dy, dx=dx + X)
    stamp(g, get(BEARD, spec.get("beard")), view, phase, dy=dy, dx=dx + X)
    for hw in spec.get("headwear", []):
        stamp(g, HEADWEAR[hw], view, phase, dy=dy, dx=dx + X)
    if view == "up":
        stamp(g, cape, view, phase, dx=X)
    else:
        for h in held:
            stamp(g, h, view, phase, dx=X)
    for draw in drawings:
        draw(g)
    g = outline(g)
    # thin props (staff, spear, crook) go on after the outline, one pixel wide,
    # as Gen 3 draws them; from behind they only show where the body isn't
    for pr in spec.get("props", []):
        stamp(g, PROP[pr], view, phase, behind=(view == "up"), dx=X)
    for draw in thin:
        draw(g)
    return g


ORDER = [("down", 0), ("up", 0), ("left", 0), ("down", 1), ("down", 2),
         ("up", 1), ("up", 2), ("left", 1), ("left", 2)]


def build(name):
    spec = CHARACTERS[name]
    roles = spec["roles"]
    grids = [frame(spec, v, ph) for v, ph in ORDER]
    grids += [frame(spec, None, None, pose) for pose in spec.get("extra", [])]
    frames = [np.array([[0 if c == "." else roles[c] for c in row] for row in g], np.uint8)
              for g in grids]
    return np.hstack(frames), read_pal(spec["family"])


def build_player(name, sheet="walking"):
    """Theo's or Ianthe's walking or running sheet (9 frames, engine order)."""
    spec = PLAYERS[name]
    roles = spec["roles"]
    grids = [frame(spec, v, ph, run=(sheet == "running")) for v, ph in ORDER]
    frames = [np.array([[0 if c == "." else roles[c] for c in row] for row in g], np.uint8)
              for g in grids]
    return np.hstack(frames), read_pal(spec["family"])


# ── the player's 32x32 poses ─────────────────────────────────────────────────
# The seated rider for surfing: the same body folded at the knees.
BODY["surf"] = {
    "down": phases(T(25, """
...CCCSSSSCCC...
..SOCcCCCCcCOS..
..sOAAAAAAAAOs..
..cCCCCCCCCCCc..
..SSScCCCCcSSS..
...SS......SS...
""")),
    "up": phases(T(25, """
...CCCCCCCCCC...
..SOCCCCCCCCOS..
..SOAAAAAAAAOS..
..cCCCCCCCCCCc..
..cCCCCCCCCCCc..
...cccccccccc...
""")),
    "left": phases(T(25, """
.....CCCCCC.....
....CCOSSCCC....
....AAOssAAA....
...CCCCCCCCC....
..SSSCCCCCcc....
..FF............
""")),
}


def _px(g, x, y, ch):
    if 0 <= y < len(g) and 0 <= x < len(g[0]):
        g[y][x] = ch


def _line(g, x1, y1, x2, y2, ch):
    """A one-pixel line (Bresenham)."""
    dx, dy = abs(x2 - x1), -abs(y2 - y1)
    sx, sy = (1 if x1 < x2 else -1), (1 if y1 < y2 else -1)
    err = dx + dy
    while True:
        _px(g, x1, y1, ch)
        if (x1, y1) == (x2, y2):
            return
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x1 += sx
        if e2 <= dx:
            err += dx
            y1 += sy


def _ball(cx, cy):
    """A capture ball, 3x3: red top, ink band, white bottom (outlined)."""
    def draw(g):
        for x in (cx - 1, cx, cx + 1):
            _px(g, x, cy - 1, "R")
            _px(g, x, cy + 1, "W")
        _px(g, cx - 1, cy, "k"), _px(g, cx, cy, "W"), _px(g, cx + 1, cy, "k")
    return draw


def _arm_up(x, top, bottom):
    def draw(g):
        for y in range(top, bottom + 1):
            _px(g, x, y, "S")
    return draw


def _sparkle(points):
    def draw(g):
        for x, y in points:
            _px(g, x, y, "Q")
    return draw


def _rod(hand, tip, line=0):
    """A rod held at `hand`, its tip at `tip`, `line` pixels of line hanging."""
    def draw(g):
        _line(g, *hand, *tip, "p")
        for i in range(1, line + 1):
            _px(g, tip[0], tip[1] + i, "W")
    return draw


def _hands(*points):
    def draw(g):
        for x, y in points:
            _px(g, x, y, "S")
    return draw


X0 = 8  # the 16-wide figure centred on the 32-wide canvas


def _pose_frames(sheet):
    """(view, phase, frame keyword arguments) per frame, in the engine's order."""
    if sheet == "field_move":  # facing down: reach, hold, lift, raise high
        return [
            ("down", 0, {}),
            ("down", 0, {"drawings": [_ball(X0 + 13, 26)]}),
            ("down", 0, {"drawings": [_hands((X0 + 6, 24)), _hands((X0 + 10, 24)), _ball(X0 + 8, 24)]}),
            ("down", 0, {"drawings": [_hands((X0 + 6, 22)), _hands((X0 + 10, 22)), _ball(X0 + 8, 21)]}),
            ("down", 0, {"drawings": [_arm_up(X0 + 13, 16, 23), _ball(X0 + 13, 14)],
                         "thin": [_sparkle([(X0 + 10, 11), (X0 + 16, 12), (X0 + 13, 9), (X0 + 17, 15)])]}),
        ]
    if sheet == "surfing":  # seated rider and the jump on/off, per direction
        jump = lambda: [_arm_up(X0 + 1, 18, 23), _arm_up(X0 + 14, 18, 23)]  # noqa: E731
        return [
            ("down", 0, {"body_override": "surf", "head_dy": 3}),
            ("down", 0, {"drawings": jump()}),
            ("up", 0, {"body_override": "surf", "head_dy": 3}),
            ("up", 0, {"drawings": jump()}),
            ("left", 0, {"body_override": "surf", "head_dy": 3}),
            ("left", 0, {"drawings": [_arm_up(X0 + 5, 18, 23)]}),
        ]
    if sheet == "fishing":  # west 0-3, north 4-7, south 8-11: out, raise, cast, taut
        west, north, south = (X0 + 5, 24), (X0 + 12, 22), (X0 + 10, 25)
        return [
            ("left", 0, {"drawings": [_hands(west)], "thin": [_rod(west, (X0 + 10, 11))]}),
            ("left", 0, {"drawings": [_hands(west)], "thin": [_rod(west, (X0 + 2, 8))]}),
            ("left", 0, {"drawings": [_hands(west)], "thin": [_rod(west, (1, 19))]}),
            ("left", 0, {"drawings": [_hands(west)], "thin": [_rod(west, (0, 23), 3)]}),
            ("up", 0, {"thin": [_rod(north, (X0 + 16, 9))]}),
            ("up", 0, {"thin": [_rod(north, (X0 + 9, 3))]}),
            ("up", 0, {"thin": [_rod(north, (X0 + 8, 0))]}),
            ("up", 0, {"thin": [_rod(north, (X0 + 11, 1))]}),
            ("down", 0, {"drawings": [_hands(south)], "thin": [_rod(south, (X0 + 15, 13))]}),
            ("down", 0, {"drawings": [_hands(south)], "thin": [_rod(south, (X0 + 9, 5))]}),
            ("down", 0, {"drawings": [_hands(south)], "thin": [_rod(south, (X0 + 17, 31))]}),
            ("down", 0, {"drawings": [_hands(south)], "thin": [_rod(south, (X0 + 19, 29), 2)]}),
        ]
    raise KeyError(sheet)


POSE_SHEETS = ("field_move", "surfing", "fishing")


def build_player_pose(name, sheet):
    spec = PLAYERS[name]
    roles = spec["roles"]
    grids = [frame(spec, v, ph, width=32, x0=X0, **kw) for v, ph, kw in _pose_frames(sheet)]
    frames = [np.array([[0 if c == "." else roles[c] for c in row] for row in g], np.uint8)
              for g in grids]
    return np.hstack(frames), read_pal(spec["family"])


# ── the chariot: the Mach Bike's riding sheet (mach_bike.png) ─────────────────
# The player standing in a small two-wheeled racing chariot drawn by one bay
# pony, in 32x32 frames in the walking order (down, up, left, then each view's
# two trot steps). The pony and car use only the palette slots brendan.pal and
# may.pal share (browns, golds, creams, ink), so both players draw the same
# chariot. The pony trots on the step frames and the wheel's spokes turn; side
# steps keep the stand frame's facing (never mirrored).
# palette slots shared by brendan.pal and may.pal
INK, BAY, BAY_D, BAY_L = 15, 3, 4, 12
CREAM, CREAM_D = 14, 9
GOLD, GOLD_D = 10, 11
RED = 13
WOOD, WOOD_D = 3, 4


def _canvas():
    return np.zeros((32, 32), np.uint8)


def _c_outline(a):
    """Ink round a layer's own silhouette (4-way), like the walkers."""
    m = a != 0
    out = a.copy()
    near = np.zeros_like(m)
    near[1:] |= m[:-1]
    near[:-1] |= m[1:]
    near[:, 1:] |= m[:, :-1]
    near[:, :-1] |= m[:, 1:]
    out[near & ~m] = INK
    return out


def _c_over(base, top):
    out = base.copy()
    out[top != 0] = top[top != 0]
    return out


def _c_draw(a):
    im = Image.fromarray(a, 'P')
    return im, ImageDraw.Draw(im)


def _c_done(im):
    return np.array(im, np.uint8)


# The rider is drawn small for the chariot, as Gen 3 draws its cyclists: the
# same petasos, chlamys and linen chiton as the walker, at about two-thirds
# scale, so the pony, the car and its wheel all fit the 32x32 frame.
RIDER = {
    "down": """
....kkkk....
...kYYYYk...
..kBBBBBBk..
.kYYYYYYYYk.
kyyyyyyyyyyk
.kHHHGHHHHk.
.kHSSSSSSHk.
.kSeSSSSeSk.
.kSeSSSSeSk.
..ksSSSSsk..
.kXkCCCCkXk.
kXXCCNCCCXXk
kSXCCCNCCXSk
.kkCCCCNCkk.
""",
    "up": """
....kkkk....
...kYYYYk...
..kBBBBBBk..
.kYYYYYYYYk.
kyyyyyyyyyyk
.kHHHGHHHHk.
.kHHHHHHGHk.
.kHHGHHHHHk.
..khhhhhhk..
.kXXXXXXXXk.
kSXXXXXXXXSk
kSXXXXXXXXSk
.kxXXXXXXxk.
..kxxxxxxk..
..kCCkkCCk..
..kFk..kFk..
""",
    "left": """
...kkkk....
..kYYYYk...
.kBBBBBBk..
kYYYYYYYYk.
kyyyyyyyyyk
.kSHHHHHHk.
kSSSHHGHHk.
kSeSSHHHHk.
kSeSSSHHhk.
.ksSSSShk..
..kCCXXXk..
.kSSCXXXXk.
.kkCCCXXXk.
..kCCCXXk..
""",
}
# long hair falls past the hat brim: over the cape behind, beside the face in front
RIDER_LONG_HAIR = {"down": [(1, 7), (10, 7), (1, 8), (10, 8)],
                   "up": [(x, y) for y in (9, 10) for x in range(3, 9)],
                   "left": [(9, 8), (9, 9), (8, 10), (9, 10), (8, 11)]}


def _small_rider(name, view, x0, y0):
    spec = PLAYERS[name]
    roles = spec["roles"]
    grid = [list(r) for r in RIDER[view].strip("\n").splitlines()]
    if spec.get("hair") == "long":
        for x, y in RIDER_LONG_HAIR[view]:
            grid[y][x] = "H"
    a = _canvas()
    for j, row in enumerate(grid):
        for i, ch in enumerate(row):
            if ch != "." and 0 <= y0 + j < 32 and 0 <= x0 + i < 32:
                a[y0 + j, x0 + i] = roles[ch]
    return a


def wheel_side(a, cx, cy, r, spin):
    """A spoked wheel side-on, drawn over the outline (open between the spokes):
    an ink tyre, a wooden rim lit at the top left, four spokes at `spin`
    degrees, a gold hub."""
    for y in range(cy - r - 2, cy + r + 3):
        for x in range(cx - r - 2, cx + r + 3):
            if not (0 <= x < 32 and 0 <= y < 32):
                continue
            d = math.hypot(x - cx, y - cy)
            if r - 0.5 < d <= r + 0.6:
                a[y, x] = INK
            elif r - 1.6 < d <= r - 0.5:
                a[y, x] = WOOD if (x - cx) + (y - cy) < 0 else WOOD_D
            elif d <= r - 1.6 and a[y, x] in (GOLD, GOLD_D, CREAM, RED):
                pass                         # the car shows through above the axle
            elif d <= r - 1.6:
                a[y, x] = 0
    for k in range(4):
        t = math.radians(spin + 90 * k)
        for s_ in range(1, r - 1):
            x, y = round(cx + s_ * math.cos(t)), round(cy + s_ * math.sin(t))
            a[y, x] = WOOD_D
    a[cy - 1:cy + 2, cx] = INK
    a[cy, cx - 1:cx + 2] = INK
    a[cy, cx] = GOLD


PONY_LEFT = """
..k.k...........
.kBkBk..........
.kBBBkk.........
kBBBBBmk........
kBeBBBBmk.......
kBBBBBBBmk......
kLBBkkBBBmk.....
kDDk..kBBBmk....
.kk...kBBBBmk...
......kBBBBBmkkk
......kBBBBBLLLL
.....kBBBBBBBBBB
.....kBBBBBBBBBB
.....kBBBBBBBBBB
.....kDBBBBBBBBD
......kDDDDDDDDk
"""
PONY_KEY = {"k": INK, "B": BAY, "D": BAY_D, "L": BAY_L, "m": INK, "e": INK}
# x of each leg; near legs are two pixels wide (lit, shaded), far legs one, dark
PONY_LEGS = (("front", True, 6), ("front", False, 9), ("hind", False, 12), ("hind", True, 14))


def leg(a, x, front, near, lifted):
    col = (BAY, BAY_D) if near else (BAY_D,)
    if not lifted:
        cells = [(x, y) for y in range(23, 29)]
        hoof = [(x, 29)]
    else:
        d = -1 if front else 1          # the knee comes forward, the hock goes back
        cells = [(x, 23), (x, 24), (x + d, 25), (x + d, 26)]
        hoof = [(x + d, 27)]
    for cx, cy in cells:
        for i, c in enumerate(col):
            a[cy, cx + i] = c
    for cx, cy in hoof:
        for i in range(len(col)):
            a[cy, cx + i] = INK


def pony_left(phase):
    a = _canvas()
    for j, row in enumerate(PONY_LEFT.strip("\n").splitlines()):
        for i, ch in enumerate(row):
            if ch != ".":
                a[7 + j, i] = PONY_KEY[ch]
    # a trot: the diagonal pairs lift in turn (near-front with far-hind)
    lift = {0: set(), 1: {("front", True), ("hind", False)}, 2: {("front", False), ("hind", True)}}[phase]
    for kind, near, x in PONY_LEGS:
        leg(a, x, kind == "front", near, (kind, near) in lift)
    return _c_outline(a)


def car_left(phase):
    im, d = _c_draw(_canvas())
    d.polygon([(16, 18), (17, 15), (20, 15), (22, 17), (29, 18), (29, 21), (16, 21)], fill=GOLD)
    a = _c_done(im)
    for x in range(16, 30):
        col = np.nonzero(a[:, x])[0]
        if len(col):
            a[col[0], x] = CREAM                               # lit rim
        if a[21, x]:
            a[21, x] = GOLD_D
    for x in range(19, 29):
        if a[19, x]:
            a[19, x] = RED                                     # a painted band
    a = _c_outline(a)
    wheel_side(a, 23, 25, 5, {0: 0, 1: 30, 2: 60}[phase])
    return a


def frame_left(name, phase):
    a = _canvas()
    a = _c_over(a, pony_left(phase))
    a = _c_over(a, _small_rider(name, 'left', 17, 4 + (1 if phase else 0)))
    a = _c_over(a, car_left(phase))
    for x, y in ((17, 16), (16, 16), (15, 15), (14, 15), (13, 14)):   # reins to the withers
        if a[y, x] in (0, BAY, BAY_L):
            a[y, x] = INK
    out = _canvas()
    out[1:] = a[:-1]                       # stand on the bike's ground row
    return out


# ── down (facing south): the pony faces you, the rider stands behind it ──────
PONY_DOWN = """
..k......k..
.kBk....kBk.
.kBBk..kBBk.
..kBBkkBBk..
.kBBmmmmBBk.
kBBBBccBBBBk
kBeBBccBBeBk
kBBBBccBBBBk
.kBBBccBBBk.
..kBBccBBk..
..kBBccBBk..
..kDDDDDDk..
..kDkDDkDk..
...kkkkkk...
"""
PONY_KEY["c"] = CREAM


def pony_down(phase, bob):
    a = _canvas()
    for j, row in enumerate(PONY_DOWN.strip("\n").splitlines()):
        for i, ch in enumerate(row):
            if ch != ".":
                a[13 + j + bob, 10 + i] = PONY_KEY[ch]
    # forelegs under the chest; a trot lifts one, then the other
    for x, up in ((10, phase == 1), (20, phase == 2)):
        bottom = 28 if up else 30
        for y in range(22 + bob, bottom):
            a[y, x] = BAY
            a[y, x + 1] = BAY_D
        a[bottom, x] = a[bottom, x + 1] = INK
    return _c_outline(a)


def wheel_edge(a, x, top, bottom, phase):
    """A wheel seen edge-on: an upright rim with a gold hub; spokes flicker by."""
    for y in range(top, bottom + 1):
        a[y, x] = WOOD_D
        a[y, x + 1] = WOOD if (y + phase) % 3 else WOOD_D
    mid = (top + bottom) // 2
    a[mid, x] = a[mid, x + 1] = GOLD


def car_down(phase):
    im, d = _c_draw(_canvas())
    d.rectangle((8, 14, 23, 22), fill=GOLD)
    a = _c_done(im)
    a[14, 8] = a[14, 23] = 0
    for x in range(9, 23):
        a[14, x] = CREAM
        a[22, x] = GOLD_D
        a[17, x] = RED
    a = _c_outline(a)
    for x in (5, 25):                                          # the wheels, edge-on
        w = _canvas()
        wheel_edge(w, x, 14, 28, phase)
        a = _c_over(a, _c_outline(w))
    return a


def frame_down(name, phase):
    a = _canvas()
    a = _c_over(a, _small_rider(name, 'down', 10, 1 + (1 if phase else 0)))
    a = _c_over(a, car_down(phase))
    a = _c_over(a, pony_down(phase, 1 if phase else 0))
    return a


# ── up (facing north): the rider's back, the pony ahead over the hat ─────────
PONY_UP = """
.....k....k.....
....kBk..kBk....
....kBBkkBBk....
.....kBmBBk.....
.....kBmBBk.....
....kBBBmBBk....
...kBBBBmBBBk...
..kBBBBBmBBBBk..
.kLBBBBBBBBBBLk.
kLBBBBBBBBBBBBLk
kBBBBBBBBBBBBBBk
kDBBBBBBBBBBBBDk
"""


def frame_up(name, phase):
    a = _canvas()
    p = _canvas()
    bob = 1 if phase else 0
    for j, row in enumerate(PONY_UP.strip("\n").splitlines()):
        for i, ch in enumerate(row):
            if ch != ".":
                p[0 + j + bob, 8 + i] = PONY_KEY[ch]
    # under the rump: the tail, and the hind legs trotting either side of it
    for y in range(12, 15):
        p[y + bob, 15] = INK
        p[y + bob, 16] = BAY_D
    for x, up in ((9, phase == 1), (21, phase == 2)):
        bottom = 14 if up else 16
        for y in range(12 + bob, bottom):
            p[y, x] = BAY
            p[y, x + 1] = BAY_D
        p[bottom, x] = p[bottom, x + 1] = INK
    a = _c_over(a, _c_outline(p))
    w = _canvas()
    for x in (5, 25):
        wheel_edge(w, x, 17, 30, phase)
    a = _c_over(a, _c_outline(w))
    c = _canvas()
    for x in range(8, 24):                                     # the car's floor and rails
        c[29, x] = WOOD
        c[30, x] = WOOD_D
    for y in range(21, 29):
        c[y, 8] = c[y, 23] = GOLD
        c[y, 9] = c[y, 22] = GOLD_D
    a = _c_over(a, _c_outline(c))
    a = _c_over(a, _small_rider(name, 'up', 10, 13 + (1 if phase else 0)))
    return a


def chariot_frames(name):
    """The nine frames in the engine's walking order."""
    return [frame_down(name, 0), frame_up(name, 0), frame_left(name, 0),
            frame_down(name, 1), frame_down(name, 2), frame_up(name, 1), frame_up(name, 2),
            frame_left(name, 1), frame_left(name, 2)]


def build_player_chariot(name):
    return np.hstack(chariot_frames(name)), read_pal(PLAYERS[name]["family"])

def player_path(name, sheet):
    return ROOT / "graphics/object_events/pics/people" / PLAYER_DIR[name] / f"{sheet}.png"


def save(sheet, pal, path):
    im = Image.fromarray(sheet, "P")
    im.putpalette([int(v) for c in pal for v in c] + [0] * (768 - 48))
    im.save(path, bits=4, transparency=0)


def to_rgba(sheet, pal):
    a = np.zeros(sheet.shape + (4,), np.uint8)
    m = sheet != 0
    a[m, :3] = pal[sheet[m]]
    a[m, 3] = 255
    return Image.fromarray(a)


def preview(names, out, Z=4):
    """Old sheet, new sheet, Theo and an Emerald townsperson, at 4x on grass."""
    rows = []
    for n in names:
        sheet, pal = build(n)
        parts = []
        old = SHEETS / f"{n}.png"
        if old.exists():
            parts.append(Image.open(old).convert("RGBA"))
        parts.append(to_rgba(sheet, pal))
        parts.append(Image.open(ROOT / "graphics/object_events/pics/people/brendan/walking.png")
                     .convert("RGBA").crop((0, 0, 48, 32)))
        parts.append(Image.open(ROOT / "graphics/object_events/pics/people/boy_1.png")
                     .convert("RGBA").crop((0, 0, 48, 32)))
        W = sum(p.width for p in parts) + 8 * len(parts)
        row = Image.new("RGBA", (W, 32), (168, 200, 120, 255))
        x = 0
        for p in parts:
            row.alpha_composite(p, (x, 0))
            x += p.width + 8
        rows.append(row)
    W = max(r.width for r in rows)
    img = Image.new("RGBA", (W, 34 * len(rows)), (232, 226, 212, 255))
    for i, r in enumerate(rows):
        img.alpha_composite(r, (0, 34 * i))
    img.convert("RGB").resize((img.width * Z, img.height * Z), Image.NEAREST).save(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("names", nargs="*")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--preview")
    a = ap.parse_args()
    names = a.names or list(CHARACTERS) + list(PLAYERS)
    if a.write:
        for n in [n for n in names if n in PLAYERS]:
            for sheet_name in ("walking", "running"):
                sheet, pal = build_player(n, sheet_name)
                save(sheet, pal, player_path(n, sheet_name))
                print("wrote", n, sheet_name)
            for sheet_name in POSE_SHEETS:
                sheet, pal = build_player_pose(n, sheet_name)
                save(sheet, pal, player_path(n, sheet_name))
                print("wrote", n, sheet_name)
            sheet, pal = build_player_chariot(n)
            save(sheet, pal, player_path(n, "mach_bike"))
            print("wrote", n, "mach_bike (the chariot)")
    names = [n for n in names if n in CHARACTERS]
    if a.preview:
        preview(names, a.preview)
    if a.write:
        for n in names:
            sheet, pal = build(n)
            save(sheet, pal, SHEETS / f"{n}.png")
            print("wrote", n)


if __name__ == "__main__":
    main()
