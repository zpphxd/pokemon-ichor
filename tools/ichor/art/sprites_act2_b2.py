"""Overworld walkers, poses and field objects for Act II, batch 2 (beats 35-37).

The road west: Route 8 (the Kopais), Lebadeia and Trophonios's cave, Route 9,
Kirrha, the Gulf ferry and Aigion. See design/phase3/SPRITES.md (batch 2).

Usage:
    python3 tools/ichor/art/sprites_act2_b2.py [NAME ...] [--write] [--preview DIR] [--grids DIR]

--write    writes graphics/object_events/pics/people/ichor/<name>.png (walkers and
           poses) and graphics/object_events/pics/misc/ichor/<name>.png (objects);
           with no NAME, also the contact sheet design/phase3/img/sprites_batch2.png
--preview  writes DIR/sprites_act2_b2_sheets.png (every frame at 4x, labelled)
--grids    writes DIR/<name>_grid.png, 8x pixel grids for editing

The house style is the slice's and batch 1's (sprites_folk.py, sprites_act2.py):
16x32 frames, nine to a sheet, feet on row 30, a 1 px step bob, right = left
mirrored. Walkers are a body archetype in role letters, a head per direction and
overlays per pose; poses are drawn frame by frame; objects are plain frames.

No new palette. Everyone on the road west fits the two families the slice
already loads, so a map here shows at most two Ichor OBJ palette slots:

* folk (OBJ_EVENT_PAL_TAG_ICHOR_FOLK): the Fowlers, Saon and the priest of
  Trophonios, the pilgrims in blankets, Agamedes, Panopeus, Alethea's notes and
  the named townsfolk.
* cast (OBJ_EVENT_PAL_TAG_ICHOR_CAST): Delphoi's temple guard (the Hoplite's
  palette) and Alethea on the spring's rim (her own).
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, save_indexed, to_rgba, upscale, grid_preview  # noqa: E402
from sprites_npc import checker_bg  # noqa: E402
from sprites_folk import (ARCHETYPES, PALETTES, DIRS, POSES, pole, _with, _paint, _resolve,  # noqa: E402
                          build_frame, GOATHERD, HOPLITE, SAILOR, ELDER_M, _STAFF, _SPEAR)
import sprites_act2 as b1  # noqa: E402  (registers the wine palette and batch 1's archetypes)
from sprites_act2 import (_flip, _frame, _same, _ALETHEA_TOP, _ALETHEA_BACK, ORDER,  # noqa: E402
                          build_pose_sheet, build_object_sheet, palette_of, label_font)
from PIL import Image, ImageDraw  # noqa: E402

W, H = 16, 32
FEET_ROW = 30
PEOPLE_DIR = b1.PEOPLE_DIR
MISC_DIR = b1.MISC_DIR

# ==========================================================================
# Building, with one extra hook over sprites_folk's: a spec may give
# `post(rows, d, pose, head_len)` to recolor the composed figure (Agamedes's
# stone-gray hands). Everything else is sprites_folk.build_sheet.
# ==========================================================================


def figure(spec, d, pose):
    head = spec["head"][d]
    body = ARCHETYPES[spec["arch"]][d][pose]
    fig = list(head) + list(body)
    over = spec.get("over", {}).get(d, {})
    keys = ["all", pose] if pose == "stand" else ["all", "walk", pose]
    for key in keys:
        for start, rows in over.get(key, []):
            _paint(fig, start, rows, len(head), f"{spec['name']} {d} {pose} [{key}]")
    fig = _resolve(fig, spec.get("roles", {}))
    if "post" in spec:
        fig = spec["post"](fig, d, pose, len(head))
    return fig


def build_walker(spec):
    pal, legend = PALETTES[spec["pal"]]
    heights = {len(spec["head"][d]) for d in DIRS}
    if len(heights) != 1:
        raise ValueError(f"{spec['name']}: head heights differ by direction: {heights}")
    frames = {}
    for d in DIRS:
        for pose in POSES:
            rows = figure(spec, d, pose)
            y0 = FEET_ROW + 1 - len(rows) + (0 if pose == "stand" else 1)
            frames[(d, pose)] = build_frame(rows, y0, legend, pal, f"{spec['name']} {d} {pose}")
    return np.hstack([frames[k] for k in ORDER])


def _recolor(rows, y0, y1, x0, x1, swap):
    """Swap palette letters inside a box of resolved figure rows."""
    out = list(rows)
    for y in range(max(0, y0), min(len(out), y1 + 1)):
        line = list(out[y])
        for x in range(x0, x1 + 1):
            line[x] = swap.get(line[x], line[x])
        out[y] = "".join(line)
    return out


def _remap(frames, swap):
    """A pose's frames with role letters swapped (palette swaps of one body)."""
    def one(fr):
        rows, bottom = fr
        return (["".join(swap.get(c, c) for c in r) for r in rows], bottom)
    return {d: {p: one(fr) for p, fr in poses.items()} for d, poses in frames.items()}


# Hand fixes for prop carriers: the stand rows that keep a hand on its prop in
# the walk frame that would swing it away (as sprites_folk's staff carriers).
_KEEP_HAND = {"tunic": ("b5", ["..kSSCCCCCQSSk..", "..kkCCCCCCCQkk.."]),
              "midi": ("b5", ["..kSSCCCCCQSSk..", "..kkCCCCCCCQkk.."]),
              "robe": ("b5", ["..kSSCCCCCQSSk..", "..kkCCCCCCCQkk.."])}


# ==========================================================================
# FOWLER: the bird-catchers of the Kopais (folk)
# ==========================================================================
#
# A lean man or woman in a short undyed tunic and a broad straw hat, a folded
# net over the left shoulder, a reed decoy-pipe at the lips and a little wicker
# quail cage hanging at the right hip. The hat is the walkers' read: a gold
# brim the full width of the frame, a terracotta band.

_STRAW_DOWN = [
    "......kkkk......",
    "....kkOOOOkk....",
    "...kOOOOOOOok...",
    "...kuuuuuuuuk...",
    ".kkOOOOOOOOOOkk.",
    "kOOOOOOOOOOOOOok",
    ".kkooooooooookk.",
]
_STRAW_LEFT = [
    ".......kkkk.....",
    ".....kkOOOOkk...",
    "....kOOOOOOOok..",
    "....kuuuuuuuuk..",
    "..kkOOOOOOOOOOkk",
    "kOOOOOOOOOOOOOok",
    ".kkooooooooookk.",
]

# the cage: a wicker dome with gold ribs and a dark inside, a loop on top
_CAGE = ["_kOk_", "kOOOk", "kbObk", "kbObk", "kOOOk", "_kkk_"]
_NET_DOWN = ["__________lyk___", "__________ylyk__", "___________lyk__", "___________kk___"]
_NET_UP = ["___klylyk_______", "___kylylk_______", "___klylyk_______", "___kylylk_______",
           "___klylyk_______", "____kkkk________"]
_NET_LEFT = ["_________lylk___", "_________ylylk__", "__________lylk__", "__________ylyk__",
             "__________lylk__", "__________kkk___"]


def _fowler_over(arch, braid=()):
    keep = _KEEP_HAND[arch]
    cage_d = pole(0, "b4", _CAGE)
    cage_u = pole(11, "b4", _CAGE)
    return dict(
        down={"all": [("b0", _NET_DOWN)],
              "stand": [cage_d], "walk0": [cage_d], "walk1": [keep, cage_d]},
        up={"all": [("b0", _NET_UP)] + list(braid),
            "stand": [cage_u], "walk0": [keep, cage_u], "walk1": [cage_u]},
        left={"all": [("b0", _NET_LEFT)]},
    )


# Gorgidas and the marsh's bird-catchers: short dark hair, clean-shaven, the
# decoy pipe at the corner of his mouth.
FOWLER = dict(
    name="fowler", pal="folk", arch="tunic",
    roles=dict(C="l", Q="y", T="u", F="b"),
    head=dict(
        down=_STRAW_DOWN + [
            "..kbbSSSSSSbbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "...bsSSSSoSsb...",
            "....bssSSsOb....",
        ],
        up=_STRAW_DOWN[:6] + [
            ".kkbbbbbbbbbbkk.",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..ksbbbbbbbbsk..",
            "...kbbbbbbbbk...",
            "....kbSSSSbk....",
        ],
        left=_STRAW_LEFT + [
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbk...",
            ".oOSSSSSsbbk....",
            "o..kbsSssbk.....",
        ],
    ),
    over=_fowler_over("tunic"),
)

# Timoxena and the women who net the reed beds: the same hat with a sky-blue
# band, hair falling past her jaw into a long braid down her back, a paler
# linen tunic to mid-calf with a sky-blue girdle.
_STRAW_DOWN_F = [r.replace("u", "a") for r in _STRAW_DOWN]
_STRAW_LEFT_F = [r.replace("u", "a") for r in _STRAW_LEFT]
_BRAID_UP = [("b0", ["_______kbbk_____", "_______kbbk_____", "_______kbbk_____",
                     "________kuk_____", "________kbk_____", "_________k______"])]
FOWLER_F = dict(
    name="fowler_f", pal="folk", arch="midi",
    roles=dict(C="L", Q="l", T="a", F="b"),
    head=dict(
        down=_STRAW_DOWN_F + [
            "..kbbSSSSSSbbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "..kbsSSSSoSsbk..",
            "..kbkssSSsOkbk..",
        ],
        up=_STRAW_DOWN_F[:6] + [
            ".kkbbbbbbbbbbkk.",
            "..kbbbbbbbbbbk..",
            "..kbbbbubbbbbk..",
            "..kbbbbbubbbbk..",
            "..kbbbbubbbbbk..",
            "...kbbbbubbbk...",
        ],
        left=_STRAW_LEFT_F + [
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbbk..",
            ".oOSSSSSsbbubk..",
            "o..kbsSssbkbbk..",
        ],
    ),
    over=_fowler_over("midi", _BRAID_UP),
)


# ==========================================================================
# Lebadeia: the priests of Trophonios and the pilgrims (folk)
# ==========================================================================

# A wax tablet held up at the chest in both hands: a wooden frame, dark wax,
# a line scratched across it.
_TABLET_HELD = [
    "___kkkkkkkkkk___",
    "__kSkooooooks___",
    "__kSkobbbbokSk__",
    "__ksSoblllobSk__",
    "___kkobbbbokk___",
    "_____kkkkkk_____",
]
_TABLET_SIDE = ["kkk", "kok", "kok", "kok", "kSk", "kkk"]


def _robe_hands_still():
    return ("b5", ["..kSSCCCCCQSSk..", "..kkCCCCCCCQkk.."])


# Saon, the eldest priest: bald under a terracotta fillet whose ends hang behind
# his ears, a white fringe and a long white beard, a white robe to the floor,
# and the wax tablet the priests write every answer on.
SAON = dict(
    name="saon", pal="folk", arch="robe",
    roles=dict(C="L", Q="l", T="u", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kSSSSSSk....",
            "...kSSSSSSSsk...",
            "..kuuuuuuuuuuk..",
            "..kLSSSSSSSSlk..",
            "..kLSyySSyySlk..",
            "..kLSkSSSSkSlk..",
            "..kuLkSSSSkLuk..",
            "..kulLLsSsLLuk..",
            "...kLLLLLLLLk...",
            "....kyLLLLyk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kSSSSSSk....",
            "...kSSSSSSSsk...",
            "..kuuuuuuuuuuk..",
            "..kSSSSuuSSSsk..",
            "..kLSSSSSSSSlk..",
            "..kLLSSSSSSLlk..",
            "..kLLLLLLLLLlk..",
            "..kyLLLLLLLLyk..",
            "...kyLLLLLLyk...",
            "....ksSSSSsk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkSSSSSk....",
            "...kSSSSSSSsk...",
            "..kuuuuuuuuuuk..",
            "..kSSSSSSuLLlk..",
            "..kyySSSSuLLlk..",
            "..kSkSSSsuLLlk..",
            "..kSkSSLLuuLk...",
            "..kLLSLLLLuuk...",
            "..kLLLLLLLyuk...",
            "...kLLLLLyk.....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["______LLLy______"])],
              "stand": [("b1", _TABLET_HELD)],
              "walk": [_robe_hands_still(), ("b1", _TABLET_HELD)]},
        left={"all": [("b0", ["____LLLy________"]), pole(2, "b1", _TABLET_SIDE)]},
    ),
)

# The priest of Trophonios: dark hair going gray and a short gray beard under
# the same fillet, the same white robe, and a clay lamp held out before him
# for the descent.
_LAMP_HELD = [
    "_______O________",
    "______kOk_______",
    "___kSkuuukSk____",
    "___kSkbuukSk____",
    "____kkkkkkk_____",
]
PRIEST = dict(
    name="trophonian_priest", pal="folk", arch="robe",
    roles=dict(C="L", Q="l", T="u", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbbybbbk....",
            "...kbybbbybbk...",
            "..kbbbbybbbbbk..",
            "..kuuuuuuuuuuk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kySkSSSSkSyk..",
            "..kyyySSSSyyyk..",
            "...kyyyssyyyk...",
            "....kyyyyyyk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbbybbbk....",
            "...kbybbbybbk...",
            "..kbbbbybbbbbk..",
            "..kuuuuuuuuuuk..",
            "..kbbbbuubbbbk..",
            "..kbbybbbbybbk..",
            "..ksbbbbbbbbsk..",
            "..ksybbbbbbysk..",
            "...kyySSSSyyk...",
            "....kySSSSyk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkbbybbk....",
            "...kbybbbbybk...",
            "..kbbbbybbbbbk..",
            "..kuuuuuuuuuuk..",
            "..kSSSSSSubbbk..",
            "..kSkSSSsubybk..",
            "..kSkSSSSuubk...",
            "..kSSyyyyyyk....",
            "...kyyyyyyk.....",
            "....kyyyk.......",
        ],
    ),
    over=dict(
        down={"stand": [("b1", _LAMP_HELD)],
              "walk": [_robe_hands_still(), ("b1", _LAMP_HELD)]},
        left={"all": [("b1", ["_O______________", "kOk_____________", "kuuk____________",
                              "kbukS___________", "_kkk____________"])]},
    ),
)


# The pilgrims on the steps: three palette swaps of one seated body, wrapped in
# a blanket to the chin over a white chiton, bare feet on the step below. Role
# letters: C/Q the blanket, H/h the hair. Walking in place facing down they
# shiver (the shoulders hunch and the head ducks into the blanket).
_PILGRIM_HEAD_DOWN = [
    ".....kkkkkk.....",
    "....kHHHHHHk....",
    "...kHHHHHHHhk...",
    "..kHHHHHHHHHhk..",
    "..kHHSSHHSSHhk..",
    "..kHSSSSSSSShk..",
    "..kHSkSSSSkShk..",
    "..kHSkSSSSkShk..",
    "..kHsSSSSSSshk..",
    "...khssSSsshk...",
]
_PILGRIM_WRAP_DOWN = [
    "..kCCkksskkCQk..",
    ".kCCCCCkkCCCQQk.",
    ".kCCCCCCCCCCQQk.",
    ".kCCQCCCCCCQCQk.",
    ".kCCCQCSSCQCCQk.",
    ".kCCCCCSskCCCQk.",
    ".kQCCCCCCCCCQQk.",
    "..kkLLLLLLLLkk..",
    "...kSskkkkSsk...",
    "...kbbk..kbbk...",
]
_PILGRIM_SHIVER_DOWN = [
    ".....kkkkkk.....",
    "....kHHHHHHk....",
    "...kHHHHHHHhk...",
    "..kHHHHHHHHHhk..",
    "..kHHSSHHSSHhk..",
    "..kHSSSSSSSShk..",
    "..kHSkSSSSkShk..",
    "..kHSkSSSSkShk..",
    ".kCCkSSSSSSkCQk.",
    ".kCCCkkkkkkCCQk.",
    ".kCCCCCkkCCCQQk.",
    ".kCCCCCCCCCCQQk.",
    ".kCCQCCCCCCQCQk.",
    ".kCCCQCSSCQCCQk.",
    ".kCCCCCSskCCCQk.",
    ".kQCCCCCCCCCQQk.",
    "..kkLLLLLLLLkk..",
    "...kSskkkkSsk...",
    "...kbbk..kbbk...",
]
_PILGRIM_UP = [
    ".....kkkkkk.....",
    "....kHHHHHHk....",
    "...kHHHHHHHhk...",
    "..kHHHHHHHHHhk..",
    "..kHHHHHHHHHhk..",
    "..kHHHHHHHHHhk..",
    "..kHHHHHHHHHhk..",
    "..khHHHHHHHHhk..",
    "..khhHHHHHHhhk..",
    "...khhHHHHhhk...",
    "..kCCksssskCQk..",
    ".kCCCCCCCCCCQQk.",
    ".kCCCCCCCCCCQQk.",
    ".kCCCQCCCCCQCQk.",
    ".kCCCCQCCCQCCQk.",
    ".kCCCCCQCQCCCQk.",
    ".kQCCCCCCCCCQQk.",
    ".kQQCCCCCCCQQQk.",
    "..kkkkkkkkkkkk..",
]
_PILGRIM_LEFT = [
    "......kkkkk.....",
    "....kkHHHHHk....",
    "...kHHHHHHHHk...",
    "..kHHHHHHHHHhk..",
    "..kHSHHHHHHHhk..",
    "..kSSSSSHsHHhk..",
    "..kSkSSSssHHhk..",
    "..kSkSSSSHHhk...",
    "..kSSSSSsHhk....",
    "...kssSsshk.....",
    "...kCCkkCCCk....",
    "..kCCCCCCCCQk...",
    ".kCCCCCCCCCQQk..",
    ".kSSCCCCCCCQQk..",
    ".kSsCCCCCCCQQk..",
    "kCCCCCCCCCCQQk..",
    "kQCCCCCCCCQQQk..",
    ".kkkkLLLLLLLkk..",
    ".kSskkkkkkkk....",
    ".kSsk...........",
    "kbbbk...........",
]
_PILGRIM_LEFT_SHIVER = [
    "................",
    "......kkkkk.....",
    "....kkHHHHHk....",
    "...kHHHHHHHHk...",
    "..kHHHHHHHHHhk..",
    "..kHSHHHHHHHhk..",
    "..kSSSSSHsHHhk..",
    "..kSkSSSssHHhk..",
    "..kSkSSSSHHhk...",
    "..kCCSSSsHhCk...",
    "..kCCCkkkkCCQk..",
    ".kCCCCCCCCCCQk..",
    ".kSSCCCCCCCQQk..",
    ".kSsCCCCCCCQQk..",
    "kCCCCCCCCCCQQk..",
    "kQCCCCCCCCQQQk..",
    ".kkkkLLLLLLLkk..",
    ".kSskkkkkkkk....",
    ".kSsk...........",
    "kbbbk...........",
]
_PILGRIM_FRAMES = dict(
    down=dict(stand=_frame(_PILGRIM_HEAD_DOWN + _PILGRIM_WRAP_DOWN),
              walk0=_frame(_PILGRIM_SHIVER_DOWN),
              walk1=_frame(_PILGRIM_HEAD_DOWN + _PILGRIM_WRAP_DOWN)),
    up=_same(_frame(_PILGRIM_UP, bottom=29)),
    left=dict(stand=_frame(_PILGRIM_LEFT), walk0=_frame(_PILGRIM_LEFT_SHIVER),
              walk1=_frame(_PILGRIM_LEFT)),
)
PILGRIM_BLANKET = dict(name="pilgrim_blanket", pal="folk", kind="pose",
                       frames=_remap(_PILGRIM_FRAMES, {"C": "u", "Q": "b", "H": "b", "h": "k"}))
PILGRIM_BLANKET_2 = dict(name="pilgrim_blanket_2", pal="folk", kind="pose",
                         frames=_remap(_PILGRIM_FRAMES, {"C": "B", "Q": "n", "H": "y", "h": "b"}))
PILGRIM_BLANKET_3 = dict(name="pilgrim_blanket_3", pal="folk", kind="pose",
                         frames=_remap(_PILGRIM_FRAMES, {"C": "g", "Q": "v", "H": "u", "h": "b"}))


# Agamedes the mason: dark curls under a terracotta sweatband, a short beard, a
# terracotta exomis under a stone-dusted linen apron, hands and forearms gray
# with stone dust, and a wooden mallet in his right hand.
_MALLET = ["kkkk_", "koobk", "kobbk", "kkkk_", "_kb__", "_kb__"]


def _stone_hands(rows, d, pose, head_len):
    """Gray the forearms and hands: skin below the shoulder rows, outside the legs."""
    b = head_len
    rows = _recolor(rows, b + 3, b + 6, 0, 4, {"S": "y", "s": "y"})
    rows = _recolor(rows, b + 3, b + 6, 11, 15, {"S": "y", "s": "y"})
    if d == "left":
        rows = _recolor(rows, b + 2, b + 6, 0, 15, {"S": "y", "s": "y"})
    return rows


AGAMEDES = dict(
    name="agamedes", pal="folk", arch="tunic",
    roles=dict(C="u", Q="b", T="b", F="b"),
    post=_stone_hands,
    head=dict(
        down=[
            "....kk.kk.kk....",
            "...kbbkbbkbbk...",
            "..kbbbbbbbbbbk..",
            "..kuuuuuuuuuuk..",
            "..kbbbbbbbbbbk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kSSkSSSSkSSk..",
            "..kbbSyyyySbbk..",
            "...kbbbssbbbk...",
            "....kbbbbbbk....",
        ],
        up=[
            "....kk.kk.kk....",
            "...kbbkbbkbbk...",
            "..kbbbbbbbbbbk..",
            "..kuuuuuuuuuuk..",
            "..kbbbbuubbbbk..",
            "..kbbbbbubbbbk..",
            "..kbbbbbbbbbbk..",
            "..ksbbbbbbbbsk..",
            "..ksbbbbbbbbsk..",
            "...kbbSSSSbbk...",
            "....kbSSSSbk....",
        ],
        left=[
            ".....kk.kk.k....",
            "....kbbkbbkbk...",
            "...kbbbbbbbbbk..",
            "..kuuuuuuuuuuk..",
            "..kbbbbbbbbbubk.",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSbbbbbk...",
            "...kbbbbbbbk....",
            "....kbbbbk......",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["____SS__________", "___SSs__________"]),
                      ("b2", ["_____lLLLLl_____", "_____lLyLLl_____", "_____lLLLLl_____",
                              "_____lLLLyl_____", "_____lylll______"])],
              "stand": [pole(0, "b0", _MALLET)], "walk0": [pole(0, "b0", _MALLET)],
              "walk1": [_KEEP_HAND["tunic"], pole(0, "b0", _MALLET)]},
        up={"all": [("b0", ["__________SS____", "__________sSS___"]), ("b4", ["___kbbbbbbbbk___"])],
            "stand": [pole(11, "b0", _flip(_MALLET))], "walk1": [pole(11, "b0", _flip(_MALLET))],
            "walk0": [_KEEP_HAND["tunic"], pole(11, "b0", _flip(_MALLET))]},
        left={"all": [("b2", ["___lLLl_________", "___lLLl_________", "___lLyl_________",
                              "___lLLl_________", "____ll__________"]),
                      pole(0, "b0", _MALLET)]},
    ),
)


# ==========================================================================
# Kirrha and the ferry
# ==========================================================================

# Panopeus, the ferry's captain: the sailor's bare chest, linen kilt and blue
# sash, a tall blue felt pilos with a terracotta band (the captain's hat; the
# fisher's is brown), and a full black beard going gray.
PANOPEUS = dict(
    SAILOR, name="panopeus",
    head=dict(
        down=[
            "......kkkk......",
            ".....kBBBnk.....",
            "....kBBBBBnk....",
            "...kBBBBBBBnk...",
            "..kuuuuuuuuuuk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "..kbbbSssSbbbk..",
            "..kbbybbbbybbk..",
            "...kbbbybbbbk...",
            "....kbbbbbbk....",
        ],
        up=[
            "......kkkk......",
            ".....kBBBnk.....",
            "....kBBBBBnk....",
            "...kBBBBBBBnk...",
            "..kuuuuuuuuuuk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..ksbbbbbbbbsk..",
            "..ksbbbbbbbbsk..",
            "...kbbSSSSbbk...",
            "....kbSSSSbk....",
        ],
        left=[
            ".......kkkk.....",
            "......kBBBnk....",
            ".....kBBBBBnk...",
            "....kBBBBBBBnk..",
            "..kkuuuuuuuuuk..",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSbbbbbbbk..",
            "..kbbbybbbbbk...",
            "...kbbbbybbk....",
            "....kbbbbk......",
        ],
    ),
)

# Delphoi's temple guards at the pilgrims' gate: the Hoplite with a white
# horsehair crest, a white cloak behind, a blue chiton under the linen
# corselet, and a white shield with Apollo's laurel wreath (cast palette).
_LAUREL_SHIELD = ["__kkkk__", "_kooook_", "koLLLLok", "kogLLgok", "kogLLgok", "koLggLok",
                  "_kooook_", "__kkkk__"]
_LAUREL_SHIELD_BACK = ["__kkkk__", "_kooook_", "kobbbbok", "kobuubok", "kobbbbok", "kobbbbok",
                       "_kooook_", "__kkkk__"]
_WHITE_CLOAK_DOWN = ["__kL________lk__", ".kLL________lLk.", ".kL__________Lk.", ".kL__________lk.",
                     ".kl__________lk.", ".kl__________lk.", ".kk__________kk."]
TEMPLE_GUARD = dict(
    HOPLITE, name="temple_guard",
    roles=dict(C="B", Q="n", T="o", F="b", X="O", Y="o"),
    head=dict(
        down=[r.replace("c", "L").replace("r", "l") for r in HOPLITE["head"]["down"]],
        up=[r.replace("c", "L").replace("r", "l") for r in HOPLITE["head"]["up"]],
        left=[r.replace("c", "L").replace("r", "l") for r in HOPLITE["head"]["left"]],
    ),
    over=dict(
        down={"all": [("b0", _WHITE_CLOAK_DOWN),
                      ("b0", ["____LL____Ll____", "___LLLLLLLLLl___", "_____LLLLLl_____",
                              "_____LLLLLl_____"]),
                      ("b5", ["_____LBLBLn_____", "____BLBLBLBn____"]),
                      pole(8, "b0", _LAUREL_SHIELD), pole(0, 0, _SPEAR), ("b5", ["__S_____________"])],
              "walk1": [("b5", ["..SSSLBLBLnSSk..", "..kkBLBLBLBnkk.."])]},
        up={"all": [("b0", ["..kLLLLLLLLLLk..", ".kLLLLLLLLLLlLk.", ".kLLLLLLLLLLlLk.",
                            ".kLLLLLLLLLlLLk.", ".klLLLLLLLLlLlk.", ".klLLLLLLLlLLlk.",
                            ".kklllllllllllkk"[:16]]),
                    pole(0, "b0", _LAUREL_SHIELD_BACK), pole(13, 0, [c[::-1] for c in _SPEAR]),
                    ("b5", ["_____________S__"])],
            "walk0": [("b5", ["..kSSBLBLBLSSS..", "..kkBLBLBLBnkk.."])]},
        left={"all": [("b0", ["_________LLk____", "________LLLlk___", "________LLLlk___",
                              "________LLllk___", "________LlLlk___", "________lLllk___",
                              "________kkkk____"]),
                      ("b5", ["_____LBLBLn_____"]), pole(4, "b0", _LAUREL_SHIELD),
                      pole(0, 0, _SPEAR), ("b4", ["__Ss____________"])]},
    ),
)


# Alethea on the rim of the bright spring (beat 35B), her satchel open beside
# her and a wax tablet on her knee: she's writing it all down. Face down she
# writes (walking in place, the stylus scratches); left or right, in profile,
# the tablet on her knee; up, from behind (the seated back of ALETHEA_SEATED).
_RIM_DOWN = [
    "..kokSSSSSSkok..",
    ".kSobooooooooSk.",
    ".kSoobooookbbkk.",
    ".kSkkkkkkkkbuubk",
    ".kSkobbbbokbLLbk",
    ".kSSobllbokbuubk",
    ".kookkkkkkkkbbk.",
    "..kkoooooooookk.",
    "...kSsk..kSsk...",
    "...kbbk..kbbk...",
]
_RIM_WRITE = list(_RIM_DOWN)
_RIM_WRITE[4] = ".kSkobbbbokbLLbk"
_RIM_WRITE[5] = ".kSSobbllokbuubk"
_RIM_LIFT = list(_RIM_DOWN)
_RIM_LIFT[2] = ".kSSobooookbbkk."
_RIM_LIFT[3] = ".kkLkkkkkkkbuubk"
_RIM_LIFT[5] = ".kSkobbbbokbuubk"
_RIM_LEFT = [
    "....koSSkok.....",
    "...kooooobok....",
    "...kooSSobuk....",
    "..kkkkSsLbbuk...",
    ".kobblSkbuubk...",
    ".kkkkkkoooobk...",
    ".kSSoooooobk....",
    ".kSskkkkkkk.....",
    ".kSsk...........",
    "kbbbk...........",
]
_RIM_LEFT_WRITE = list(_RIM_LEFT)
_RIM_LEFT_WRITE[3] = "..kkkkSLkbbuk..."
_RIM_LEFT_WRITE[4] = ".kobbbSkbuubk..."
ALETHEA_RIM = dict(
    name="alethea_rim", pal="cast", kind="pose",
    frames=dict(
        down=dict(stand=_frame(_ALETHEA_TOP["down"] + _RIM_DOWN),
                  walk0=_frame(_ALETHEA_TOP["down"] + _RIM_LIFT),
                  walk1=_frame(_ALETHEA_TOP["down"] + _RIM_WRITE)),
        up=_same(_frame(_ALETHEA_TOP["up"] + _ALETHEA_BACK + [
            ".kbbbuuoooooobk.",
            "..kkkkkkkkkkkk..",
        ], bottom=29)),
        left=dict(stand=_frame(_ALETHEA_TOP["left"] + _RIM_LEFT),
                  walk0=_frame(_ALETHEA_TOP["left"] + _RIM_LEFT_WRITE),
                  walk1=_frame(_ALETHEA_TOP["left"] + _RIM_LEFT)),
    ),
)


# ==========================================================================
# The named townsfolk (folk)
# ==========================================================================

# Herkyna, Lebadeia's river girl of about nine: dark hair loose to her
# shoulders with a white flower over one ear, a sky-blue tunic, barefoot.
HERKYNA = dict(
    name="herkyna", pal="folk", arch="kid",
    roles=dict(C="a", Q="B", T="a", F="s"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbLk...",
            "..kbbbbbbbbLLk..",
            "..kbbSbbbbSbbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "..kbbsSSSSsbbk..",
            "..kbk.kssk.kbk..",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kLbbbbbuubk..",
            "..kLLbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbkSSSSkbbk..",
        ],
        left=[
            "......kkkk......",
            "....kkbbbbk.....",
            "...kbuubbbbk....",
            "...kbbbbbbbbk...",
            "...kbSbbbbLLbk..",
            "...kSSSSbsLbbk..",
            "...kSkSSssbbbk..",
            "...ksSSSsbbbk...",
            "....kssssbbk....",
        ],
    ),
)

# Xenodike, the traveler girl at the lookout: dark hair in a knot, a linen
# chiton to mid-calf, a terracotta traveling cloak pinned at the right
# shoulder, and a sky-blue cloth bundle under her left arm.
_BUNDLE = ["_kLk_", "kaLak", "kaaBk", "kaaBk", "_kkk_"]
XENODIKE = dict(
    name="xenodike", pal="folk", arch="midi",
    roles=dict(C="L", Q="l", T="u", F="b"),
    head=dict(
        down=[
            "......kkkk......",
            ".....kbbbbk.....",
            "....kkbbbbkk....",
            "...kbbbbbbbbk...",
            "..kbbbbbbbbbbk..",
            "..kbbSSbbSSbbk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "..kbsSSSSSSsbk..",
            "...kbssSSssbk...",
        ],
        up=[
            "......kkkk......",
            ".....kbuubk.....",
            "....kkbbbbkk....",
            "...kbbbbbbbbk...",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..ksbbbbbbbbsk..",
            "...kbbSSSSbbk...",
        ],
        left=[
            "......kkkk......",
            ".....kbbbbkk....",
            "....kkbbbbbuk...",
            "...kbbbbbbbbk...",
            "..kbbbbbbbbbbk..",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbbk..",
            "..kSSSSSsbbbk...",
            "...kbsSssbbk....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["___kuu__________", "__kuuuu_________", "__kuubuu________",
                              "__kubuuuu_______", "__kubbuuuu______", "__kbbbbuuuk_____"]),
                      ("b0", ["___O____________"]),
                      pole(11, "b3", _BUNDLE)]},
        up={"all": [("b0", ["..kuuuuuuuuuk...", ".kuuuuuuuuuubk..", ".kuuuuuuuuubuk..",
                            ".kuuuuuuuubuuk..", ".kbuuuuuubuuuk..", ".kbbuuuubuuubk..",
                            "..kbbbbbbbbbk..."]),
                    pole(0, "b3", _flip(_BUNDLE))]},
        left={"all": [("b0", ["_________uk_____", "________uuuk____", "________uuubk___",
                              "________uubuk___", "________ubuuk___", "________kkkk____"]),
                      pole(6, "b3", _BUNDLE)]},
    ),
)

# Thyia, who swept Apollo's floor for forty years: white hair pulled back into
# a bun on the crown, a kind old face with smiling eyes, a blue peplos and a
# linen apron, and a broom (a twig besom bound to a stick) in her right hand.
_BROOM = ["_k"] + ["kb"] * 11 + ["kuk", "kuk", "kook", "koOk", "kOoOk", "koOok", "kkkkk"]
THYIA = dict(
    name="thyia", pal="folk", arch="robe",
    roles=dict(C="B", Q="n", T="L", F="b"),
    head=dict(
        down=[
            "......kkkk......",
            ".....kLLLyk.....",
            "....kkyLyykk....",
            "...kLLLLLLLyk...",
            "..kLLLyLLyLLyk..",
            "..kLLSSSSSSLyk..",
            "..kLSkkSSkkSyk..",
            "..kySuSSSSuSyk..",
            "..kySSSsSsSSyk..",
            "...ksSSSSSSsk...",
            "....kssSSssk....",
        ],
        up=[
            "......kkkk......",
            ".....kLLLyk.....",
            "....kkyLyykk....",
            "...kLLLLLLLyk...",
            "..kLLLlLLLLLyk..",
            "..kLLLLlLLLLyk..",
            "..kLLLLLlLLLyk..",
            "..kyLLLLLLLLyk..",
            "..kyyLLLLLLyyk..",
            "...kyyLLLLyyk...",
            "....kySSSSyk....",
        ],
        left=[
            "........kkkk....",
            ".......kLLLyk...",
            ".....kkkyLyyk...",
            "...kkLLLLLLLyk..",
            "..kLLLLLLLLLyk..",
            "..kSSLLLLyLLyk..",
            "..kSSSSSsLLLyk..",
            "..kSkkSSsLLyk...",
            "..kSSuSSSyLyk...",
            "..ksSSSsLLyk....",
            "...ksssk.yk.....",
        ],
    ),
    over=dict(
        down={"all": [("b5", ["_____LLLLLl_____", "_____LLLLLl_____", "_____LLLLLl_____",
                              "_____lLLLLl_____"])],
              "stand": [pole(0, 2, _BROOM)], "walk0": [pole(0, 2, _BROOM)],
              "walk1": [_KEEP_HAND["robe"], pole(0, 2, _BROOM)]},
        up={"all": [("b5", ["______Ll________"])],
            "stand": [pole(11, 2, _flip(_BROOM))], "walk1": [pole(11, 2, _flip(_BROOM))],
            "walk0": [_KEEP_HAND["robe"], pole(11, 2, _flip(_BROOM))]},
        left={"all": [("b6", ["_____L__________", "____LL__________", "____Ll__________"]),
                      pole(0, 2, _BROOM)]},
    ),
)

# Tisamenos, Aigion's keeper of the ship-list: a full head of white hair and a
# long white beard (the elder walker, who is bald), a sea-blue himation for the
# Achaean fleet, and the walking staff.
TISAMENOS = dict(
    ELDER_M, name="tisamenos",
    roles=dict(C="B", Q="n", T="B", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kLLLLLLk....",
            "...kLLlLLlLLk...",
            "..kLLLLLLLLLlk..",
            "..kLLSSSSSSLlk..",
            "..kLSyySSyySlk..",
            "..kLSkSSSSkSlk..",
            "..klSkSSSSkSlk..",
            "..klLLsSSsLLlk..",
            "...kLLLLLLLLk...",
            "....klLLLLlk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kLLLLLLk....",
            "...kLLLlLLLLk...",
            "..kLLlLLLLlLLk..",
            "..kLLlLLLLlLlk..",
            "..kLlLLLLlLLlk..",
            "..kLlLLLLlLLlk..",
            "..klLLLLlLLllk..",
            "..kllLLlLLlllk..",
            "...kllLlLlllk...",
            "....ksSSSSsk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkLLLLLk....",
            "...kLLLLlLLLk...",
            "..kLLLLLLlLLlk..",
            "..kSSLLLLLlLlk..",
            "..kyySSSSLlLlk..",
            "..kSSSSSsLLLlk..",
            "..kSkSSSsLLLlk..",
            "..kLkSSLLLLLk...",
            "..kLLLLLLLlk....",
            "...kLLLLLlk.....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["______LLLl______", "______lLl_______"]),
                      ("b2", ["_______n________", "________n_______", "_________n______"]),
                      pole(0, 1, _STAFF), ("b5", ["__S_____________"])],
              "walk1": [("b5", ["..SSSCCCCCQSSk..", "..kkCCCCCCCQkk.."])]},
        up=ELDER_M["over"]["up"],
        left=ELDER_M["over"]["left"],
    ),
)

# Helike, Aigion's goatherd: the goatherd's palette and shaggy goat-hair
# cloak, a terracotta kerchief over dark hair worn long in a braid, an undyed
# dress to mid-calf, a bronze goat bell at her belt and a crook.
_CROOK = ["_kkk_", "kuouk", "kukuk", "ku_k_"] + ["ku"] * 19 + ["kb"]
_CROOK_UP = [c.rjust(5, "_")[::-1] for c in _CROOK]
HELIKE = dict(
    name="helike", pal="folk", arch="midi",
    roles=dict(C="l", Q="y", T="u", F="b"),
    head=dict(
        down=[
            "................",
            "................",
            "................",
            ".....kkkkkk.....",
            "....kuuuuuubk...",
            "...kuuuuuuubbk..",
            "..kbbbbbbbbbbk..",
            "..kbbSSbbSSbbk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "..kbsSSSSSSsbk..",
            "..kbbssSSssbbk..",
            "...kbk.kk.kbk...",
        ],
        up=[
            "................",
            "................",
            "................",
            ".....kkkkkk.....",
            "....kuuuuuuk....",
            "...kuuuuuuuuk...",
            "..kbbbuuuubbbk..",
            "..kbbbbuubbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbubbbbbk..",
            "..kbbbbbubbbbk..",
            "..kbbbbubbbbbk..",
            "...kbbbbubbbk...",
            "....kbSubSbk....",
        ],
        left=[
            "................",
            "................",
            "................",
            "......kkkkk.....",
            "....kkuuuuuk....",
            "...kuuuuuuuuk...",
            "..kbbbbbbuuuuk..",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbbk..",
            "..kSSSSSsbbubk..",
            "...kbsSssbkbk...",
            "....kkkkk.kk....",
        ],
    ),
    over=dict(
        down={"all": [GOATHERD["over"]["down"]["all"][0], ("b5", ["_______Oo_______", "_______kk_______"])],
              "stand": [pole(0, 0, _CROOK)], "walk0": [pole(0, 0, _CROOK)],
              "walk1": [_KEEP_HAND["midi"], pole(0, 0, _CROOK)]},
        up={"all": [GOATHERD["over"]["up"]["all"][0]],
            "stand": [pole(11, 0, _CROOK_UP)], "walk1": [pole(11, 0, _CROOK_UP)],
            "walk0": [_KEEP_HAND["midi"], pole(11, 0, _CROOK_UP)]},
        left={"all": [GOATHERD["over"]["left"]["all"][0], ("b4", ["_________o______"]),
                      pole(0, 0, _CROOK)]},
    ),
)


# ==========================================================================
# Field objects
# ==========================================================================

# One of Alethea's notes on Route 8: a slip of wax tablet tied to a reed stuck
# in the mud, five of them along the road. A green reed with a brown plume, the
# slip's wooden frame and dark wax with her scratched lines, a twist of twine.
_NOTE = [
    "................",
    "................",
    "........k.......",
    ".......kok......",
    ".......kbok.....",
    "......kobok.....",
    ".......kbok.....",
    ".......kok......",
    "........kgk.....",
    "........kgk.....",
    "........kvk.....",
    "....kkkkkkkkk...",
    "....kooooooook..",
    "....kobbbbbbok..",
    "....kobLLlbbok..",
    "....kobbLlLbok..",
    "....kobLlbbbok..",
    "....kooooooook..",
    "....kkkkkkkkkk..",
    "........kgk.....",
    ".....kk.kgk.....",
    ".....kgkkvk.....",
    "......kgkgk.....",
    "......kvkgk.....",
    ".......kkgk.....",
    "........kvk..kk.",
    "...kk...kgk.kgk.",
    "...kgk..kgkkgk..",
    "....kgk.kvkgk...",
    "...kbbbkkbbbbk..",
    "..kbbbbbbbbbbbk.",
    "................",
]
ALETHEA_NOTE = dict(name="alethea_note", pal="folk", kind="object", fw=16, fh=32, frames=[_NOTE])


# ==========================================================================
# Output
# ==========================================================================

WALKERS = [FOWLER, FOWLER_F, SAON, PRIEST, AGAMEDES, PANOPEUS, TEMPLE_GUARD,
           HERKYNA, XENODIKE, THYIA, TISAMENOS, HELIKE]
POSE_SPECS = [PILGRIM_BLANKET, PILGRIM_BLANKET_2, PILGRIM_BLANKET_3, ALETHEA_RIM]
OBJECTS = [ALETHEA_NOTE]


def all_specs():
    return WALKERS + POSE_SPECS + OBJECTS


def build(spec):
    if spec.get("kind") == "pose":
        return build_pose_sheet(spec)
    if spec.get("kind") == "object":
        return build_object_sheet(spec)
    return build_walker(spec)


CONTACT_SHEET = os.path.join(ROOT, "design/phase3/img/sprites_batch2.png")
# The walkers the batch is drawn to match, first for scale: the slice's
# fisher, sailor, elder, goatherd and hoplite, and batch 1's Kronist.
REFS = ["fisher", "sailor", "elder_m", "goatherd", "hoplite", "alethea", "kronist"]


def sheet_preview(sheets, specs, k=4, refs=(), lw=40, font_size=18):
    rows = []
    for ref in refs:
        im = Image.open(os.path.join(PEOPLE_DIR, ref + ".png")).convert("RGBA")
        rows.append((ref, "ref", im, W, H))
    for spec in specs:
        fw, fh = spec.get("fw", W), spec.get("fh", H)
        rows.append((spec["name"], spec["pal"], to_rgba(sheets[spec["name"]], palette_of(spec)), fw, fh))
    pad = 4
    width = lw + max((im.width // fw) * (fw + pad) for _, _, im, fw, fh in rows)
    height = sum(fh + pad for *_, fh in rows)
    out = Image.new("RGBA", (width, height), (232, 224, 200, 255))
    y = 0
    for _, _, im, fw, fh in rows:
        for f in range(im.width // fw):
            tile = checker_bg(fw, fh)
            tile.alpha_composite(im.crop((f * fw, 0, (f + 1) * fw, fh)))
            out.alpha_composite(tile, (lw + f * (fw + pad), y))
        y += fh + pad
    big = upscale(out, k)
    d = ImageDraw.Draw(big)
    font = label_font(font_size)
    y = 0
    for name, pal, _, _, fh in rows:
        d.text((4, y * k + 6), name, fill=(32, 24, 24, 255), font=font)
        d.text((4, y * k + 8 + font_size), pal, fill=(112, 96, 80, 255), font=font)
        y += fh + pad
    return big


def contact_sheet(sheets):
    """design/phase3/img/sprites_batch2.png: everything at 2x, after the
    walkers it is drawn to match."""
    return sheet_preview(sheets, all_specs(), k=2, refs=REFS, lw=96, font_size=12)


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    grids = args[args.index("--grids") + 1] if "--grids" in args else None
    write = "--write" in args
    names = {s["name"] for s in all_specs()}
    only = [a for a in args if a in names]
    specs = [s for s in all_specs() if not only or s["name"] in only]
    sheets = {s["name"]: build(s) for s in specs}
    if write:
        for spec in specs:
            out = MISC_DIR if spec.get("kind") == "object" else PEOPLE_DIR
            save_indexed(sheets[spec["name"]], palette_of(spec), os.path.join(out, spec["name"] + ".png"))
        if not only:
            os.makedirs(os.path.dirname(CONTACT_SHEET), exist_ok=True)
            contact_sheet(sheets).save(CONTACT_SHEET)
    if pv:
        os.makedirs(pv, exist_ok=True)
        sheet_preview(sheets, specs, refs=REFS if not only else ()).save(
            os.path.join(pv, "sprites_act2_b2_sheets.png"))
    if grids:
        os.makedirs(grids, exist_ok=True)
        for spec in specs:
            grid_preview(to_rgba(sheets[spec["name"]], palette_of(spec)), 8).save(
                os.path.join(grids, spec["name"] + "_grid.png"))


if __name__ == "__main__":
    main()
