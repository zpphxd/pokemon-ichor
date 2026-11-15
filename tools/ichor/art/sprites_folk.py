"""Overworld walkers for Kalliste's townsfolk and the slice's trainer classes.

Usage:
    python3 tools/ichor/art/sprites_folk.py [NAME ...] [--write] [--preview DIR] [--grids DIR]

--write    writes graphics/object_events/pics/people/ichor/<name>.png (144x32,
           4bpp indexed) for every walker here, and the folk palette
           graphics/object_events/palettes/ichor_folk.pal
--preview  writes DIR/sprites_folk_sheets.png (4x, vanilla Birch first for
           scale, each walker labelled with its sheet name)
--grids    writes DIR/<name>_grid.png, 8x pixel grids for editing

Two palettes, so a crowded map needs at most two Ichor OBJ palette slots:

* FOLK_PAL (new, OBJ_EVENT_PAL_TAG_ICHOR_FOLK): sun-browned islanders in linen,
  wool, terracotta, olive, Aegean blue and saffron. The fifteen townsfolk plus
  the Harvester and the Goatherd, whose portraits use the same sun-browned skin.
* CAST_PAL (sprites_npc.py, OBJ_EVENT_PAL_TAG_ICHOR_CAST): the Shepherd, the
  Hoplite, the Augur and both Acolytes, whose portraits share the cast's fairer
  skin, crimson, bronze, linen and blue.

The frame layout, the 1 px step bob and feet on row 30 match sprites_npc.py.

How a walker is built here:

* A body ARCHETYPE (tunic, midi, robe, kid) gives the torso, arms and legs for
  all nine frames, drawn once in ROLE letters: C cloth, Q cloth shade, T belt,
  F feet, X/Y shins (light, shade). Each walker maps the roles to its palette.
* Each walker draws its own head per direction (`head`), the same height in
  all three directions.
* Overlays (`over`) paint props and costume over the composed figure:
  {direction: {pose: [(start, rows), ...]}}, pose one of all/stand/walk/walk0/
  walk1. `start` is a figure row (0 = top of the head) or "bN" for body row N.
  In overlay rows "_" keeps the pixel underneath and "." clears it.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, Palette, save_indexed, to_rgba, upscale, grid_preview  # noqa: E402
from sprites_npc import CAST_PAL, CAST_LEGEND, checker_bg, ref_rgba  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

W, H = 16, 32
FEET_ROW = 30
OUT_DIR = os.path.join(ROOT, "graphics/object_events/pics/people/ichor")
FOLK_PAL_PATH = os.path.join(ROOT, "graphics/object_events/palettes/ichor_folk.pal")

# --------------------------------------------------------------------------
# The folk palette. Letters follow the cast palette where the role matches
# (k ink, b brown, o/O ochre-gold, s/S skin, l/L linen, n/B blue, g green).
# --------------------------------------------------------------------------

FOLK_COLORS = [
    # char, name, rgb                       used for
    ("k", "ink", (32, 24, 24)),            # outlines, eyes, wet hair
    ("b", "brown", (88, 48, 32)),          # hair, sandals, leather, terracotta shadow
    ("u", "terra", (184, 72, 48)),         # terracotta cloth, ribbons, hair highlight
    ("o", "ochre", (200, 144, 40)),        # saffron and ochre shadow, wicker, bronze
    ("O", "gold", (240, 192, 64)),         # saffron, honey, gold, sponges
    ("s", "skin_d", (192, 120, 72)),       # sun-browned skin shadow
    ("S", "skin_l", (232, 176, 120)),      # sun-browned skin
    ("l", "linen_d", (200, 184, 152)),     # linen and wool shadow, net twine
    ("L", "linen_l", (248, 240, 216)),     # linen, white hair
    ("y", "gray", (152, 144, 136)),        # gray hair, goat hair, net knots
    ("n", "blue_d", (24, 56, 120)),        # Aegean blue shadow, wet-hair sheen
    ("B", "blue", (48, 104, 176)),         # Aegean blue
    ("a", "sky", (112, 168, 224)),         # faded sea-blue
    ("v", "olive_d", (64, 80, 32)),        # olive shadow, olives
    ("g", "olive", (120, 136, 56)),        # olive cloth, wreath leaves
]
FOLK_PAL = Palette([(name, rgb) for _, name, rgb in FOLK_COLORS])
FOLK_LEGEND = {ch: name for ch, name, _ in FOLK_COLORS}

PALETTES = {
    "folk": (FOLK_PAL, FOLK_LEGEND),
    "cast": (CAST_PAL, CAST_LEGEND),
}

ROLES = "CQTFXY"
DEFAULT_ROLES = {"X": "S", "Y": "s"}

# --------------------------------------------------------------------------
# Body archetypes, in role letters. Each direction has stand, walk0, walk1.
# Front and back walks lift one leg (walk0 the right one as seen, walk1 the
# left) and swing that side's hand back. Side walks stride: walk0 the near
# leg forward and the arm back, walk1 the far leg forward and the arm forward.
# --------------------------------------------------------------------------


def _with(rows, changes):
    out = list(rows)
    for i, r in changes.items():
        out[i] = r
    return out


_TUNIC_DOWN = [
    "...kCCSSSSCQk...",
    "..kCCCCCCCCCQk..",
    "..kSSCCCCCQSsk..",
    "..kSsCCCCCQSsk..",
    "..kSsTTTTTTSsk..",
    "..kSSCCCCCQSSk..",
    "..kkCCCCCCCQkk..",
    "...kkXYkkXYkk...",
    "....kXYkkXYk....",
    "....kFFkkFFk....",
]
_TUNIC_UP = _with(_TUNIC_DOWN, {0: "...kCCCCCCCQk..."})
_HANDS_W0 = {5: "..kSSCCCCCQkk...", 6: "..kkCCCCCCCQk..."}
_HANDS_W1 = {5: "...kkCCCCCQSSk..", 6: "...kCCCCCCCQkk.."}
_LEGS_W0 = {8: "....kXYkkFFk....", 9: "....kFFk........"}
_LEGS_W1 = {8: "....kFFkkXYk....", 9: "........kFFk...."}

_TUNIC_LEFT = [
    ".....kSSCQk.....",
    "....kCCCCCQk....",
    "....kCSsCCQk....",
    "....kCSsCCQk....",
    "....kTSsTTTk....",
    "....kCSSCCQk....",
    "....kCCCCCQk....",
    "....kkXYkkkk....",
    ".....kXYk.......",
    "....kFFFk.......",
]
_ARM_BACK = {2: "....kCCSsCQk....", 3: "....kCCSsCQk....",
             4: "....kTTSsTTk....", 5: "....kCCSSCQk...."}
_ARM_FWD = {2: "....kSsCCCQk....", 3: "....kSsCCCQk....",
            4: "....kSsTTTTk....", 5: "....kSSCCCQk...."}
_STRIDE_W0 = {7: "...kXYkkkYYk....", 8: "..kXYk...kYYk...", 9: "..kFFk....kFFk.."}
_STRIDE_W1 = {7: "...kYYkkkXYk....", 8: "..kYYk...kXYk...", 9: "..kFFk....kFFk.."}


def _dirs(down, up, left):
    return {"down": down, "up": up, "left": left}


def _front(stand):
    return dict(stand=stand,
                walk0=_with(stand, {**_HANDS_W0, **{k: v for k, v in _LEGS_W0.items()}}),
                walk1=_with(stand, {**_HANDS_W1, **{k: v for k, v in _LEGS_W1.items()}}))


TUNIC = _dirs(
    _front(_TUNIC_DOWN),
    _front(_TUNIC_UP),
    dict(stand=_TUNIC_LEFT,
         walk0=_with(_TUNIC_LEFT, {**_ARM_BACK, **_STRIDE_W0}),
         walk1=_with(_TUNIC_LEFT, {**_ARM_FWD, **_STRIDE_W1})),
)

# Mid-calf: the skirt runs one row longer and only the ankles show.
_MIDI_DOWN = _with(_TUNIC_DOWN, {7: "...kCCCCCCCQk...", 8: "...kkXYkkXYkk..."})
_MIDI_UP = _with(_MIDI_DOWN, {0: "...kCCCCCCCQk..."})
_MIDI_LEGS_W0 = {8: "...kkXYkkFFkk...", 9: "....kFFk........"}
_MIDI_LEGS_W1 = {8: "...kkFFkkXYkk...", 9: "........kFFk...."}
_MIDI_LEFT = _with(_TUNIC_LEFT, {7: "....kCCCCCQk....", 8: "....kkXYkkkk...."})


def _front_midi(stand):
    return dict(stand=stand,
                walk0=_with(stand, {**_HANDS_W0, **_MIDI_LEGS_W0}),
                walk1=_with(stand, {**_HANDS_W1, **_MIDI_LEGS_W1}))


MIDI = _dirs(
    _front_midi(_MIDI_DOWN),
    _front_midi(_MIDI_UP),
    dict(stand=_MIDI_LEFT,
         walk0=_with(_MIDI_LEFT, {**_ARM_BACK, 8: "...kXYkkkYYk....", 9: "..kFFk...kFFk..."}),
         walk1=_with(_MIDI_LEFT, {**_ARM_FWD, 8: "...kYYkkkXYk....", 9: "..kFFk...kFFk..."})),
)

# Floor-length: the hem flares a little and only the toes show.
_ROBE_DOWN = _with(_TUNIC_DOWN, {
    7: "...kCCCCCCCQk...",
    8: "..kCCCCCCCCCQk..",
    9: "..kkkFFkkFFkkk..",
})
_ROBE_UP = _with(_ROBE_DOWN, {0: "...kCCCCCCCQk..."})
_ROBE_FEET_W0 = {9: "..kkkFFkkkkkkk.."}
_ROBE_FEET_W1 = {9: "..kkkkkkkFFkkk.."}
_ROBE_LEFT = _with(_TUNIC_LEFT, {
    7: "...kCCCCCCQk....",
    8: "...kCCCCCCCQk...",
    9: "...kFFkkkkkkk...",
})


def _front_robe(stand):
    return dict(stand=stand,
                walk0=_with(stand, {**_HANDS_W0, **_ROBE_FEET_W0}),
                walk1=_with(stand, {**_HANDS_W1, **_ROBE_FEET_W1}))


ROBE = _dirs(
    _front_robe(_ROBE_DOWN),
    _front_robe(_ROBE_UP),
    dict(stand=_ROBE_LEFT,
         walk0=_with(_ROBE_LEFT, {**_ARM_BACK, 7: "..kCCCCCCCQk....",
                                  8: "..kCCCCCCCCQk...", 9: "..kFFkkkkkkFFk.."}),
         walk1=_with(_ROBE_LEFT, {**_ARM_FWD, 9: "....kFFkkkkkk..."})),
)

# Children: a 7-row body under a 9-row head, barefoot as a rule.
_KID_DOWN = [
    "....kkCSSCkk....",
    "...kCCCCCCCQk...",
    "...kSCCCCCQSk...",
    "...kSCCCCCQSk...",
    "...kSCCCCCQSk...",
    "...kkXYkkXYkk...",
    "....kFFkkFFk....",
]
_KID_UP = _with(_KID_DOWN, {0: "....kkCCCCkk...."})
_KID_LEFT = [
    ".....kSSCk......",
    "....kCCCCQk.....",
    "....kCSsCQk.....",
    "....kCSsCQk.....",
    "....kCSSCQk.....",
    "....kkXYkk......",
    "....kFFFk.......",
]


def _front_kid(stand):
    return dict(stand=stand,
                walk0=_with(stand, {5: "...kkXYkkFFkk...", 6: "....kFFk........"}),
                walk1=_with(stand, {5: "...kkFFkkXYkk...", 6: "........kFFk...."}))


KID = _dirs(
    _front_kid(_KID_DOWN),
    _front_kid(_KID_UP),
    dict(stand=_KID_LEFT,
         walk0=_with(_KID_LEFT, {2: "....kCCSsQk.....", 3: "....kCCSsQk.....", 4: "....kCCSSQk.....",
                                 5: "...kXYkYYk......", 6: "..kFFk.kFFk....."}),
         walk1=_with(_KID_LEFT, {2: "....kSsCCQk.....", 3: "....kSsCCQk.....", 4: "....kSSCCQk.....",
                                 5: "...kYYkXYk......", 6: "..kFFk.kFFk....."})),
)

ARCHETYPES = {"tunic": TUNIC, "midi": MIDI, "robe": ROBE, "kid": KID}

# Elaia's shared cloth construction: a folded shoulder, bloused waist and
# separated ankles. Keep the other towns' source bodies until their batch.
_ELAIA_DOWN = [
    "...kCCSSSCQk....",
    "..kCCCCCCCQQk...",
    "..kSCCQCCCQSsk..",
    "..kSsCCQCCQSsk..",
    "..kSsTTTTTTSsk..",
    "..kSSCCCCCQSSk..",
    "...kCCCQCCQQk...",
    "....kXYkkXYk....",
    "....kXYkkXYk....",
    "...kFFFkkFFk....",
]
_ELAIA_UP = _with(_ELAIA_DOWN, {0: "...kCCCCCCQk....", 2: "..kSCCQCCCQSsk..",
                               3: "..kSsCQCCCQSsk..", 6: "...kCCQCCCQQk..."})
_ELAIA_LEFT = [
    ".....kSSCQk.....",
    "....kCCCCQQk....",
    "....kCSsCQk.....",
    "....kCSsCQQk....",
    "....kTSsTTk.....",
    "....kCSSCQQk....",
    "....kCCQCCQk....",
    "....kkXYkkkk....",
    ".....kXYk.......",
    "....kFFFk.......",
]
ARCHETYPES["elaia_tunic"] = _dirs(
    _front(_ELAIA_DOWN), _front(_ELAIA_UP),
    dict(stand=_ELAIA_LEFT, walk0=_with(_ELAIA_LEFT, {**_ARM_BACK, **_STRIDE_W0}),
         walk1=_with(_ELAIA_LEFT, {**_ARM_FWD, **_STRIDE_W1})),
)
_ELAIA_MIDI_DOWN = _with(_ELAIA_DOWN, {7: "...kCCCQCCQQk...", 8: "...kkXYkkXYkk..."})
_ELAIA_MIDI_UP = _with(_ELAIA_UP, {7: "...kCCQCCCQQk...", 8: "...kkXYkkXYkk..."})
_ELAIA_MIDI_LEFT = _with(_ELAIA_LEFT, {7: "....kCCQCCQk....", 8: "....kkXYkkkk...."})
ARCHETYPES["elaia_midi"] = _dirs(
    _front_midi(_ELAIA_MIDI_DOWN), _front_midi(_ELAIA_MIDI_UP),
    dict(stand=_ELAIA_MIDI_LEFT,
         walk0=_with(_ELAIA_MIDI_LEFT, {**_ARM_BACK, 8: "...kXYkkkYYk....", 9: "..kFFk...kFFk..."}),
         walk1=_with(_ELAIA_MIDI_LEFT, {**_ARM_FWD, 8: "...kYYkkkXYk....", 9: "..kFFk...kFFk..."})),
)
_ELAIA_ROBE_DOWN = _with(_ELAIA_DOWN, {7: "...kCCCQCCCQk...", 8: "..kCCCCQCCCCQk..",
                                     9: "..kkkFFkkFFkkk.."})
_ELAIA_ROBE_UP = _with(_ELAIA_UP, {7: "...kCCQCCCCQk...", 8: "..kCCCQCCCCCQk..",
                                 9: "..kkkFFkkFFkkk.."})
_ELAIA_ROBE_LEFT = _with(_ELAIA_LEFT, {7: "...kCCQCCCQk....", 8: "...kCCCQCCCQk...",
                                     9: "...kFFkkkkkkk..."})
ARCHETYPES["elaia_robe"] = _dirs(
    _front_robe(_ELAIA_ROBE_DOWN), _front_robe(_ELAIA_ROBE_UP),
    dict(stand=_ELAIA_ROBE_LEFT,
         walk0=_with(_ELAIA_ROBE_LEFT, {**_ARM_BACK, 7: "..kCCQCCCCQk....",
                                       8: "..kCCCQCCCCQk...", 9: "..kFFkkkkkkFFk.."}),
         walk1=_with(_ELAIA_ROBE_LEFT, {**_ARM_FWD, 9: "....kFFkkkkkk..."})),
)
_ELAIA_KID_DOWN = _with(_KID_DOWN, {1: "...kCCCCCCQQk...", 3: "...kSCQCCCQSk...",
                                  4: "...kSCCQCCQSk..."})
_ELAIA_KID_UP = _with(_ELAIA_KID_DOWN, {0: "....kkCCCCkk....", 3: "...kSCCQCCQSk..."})
_ELAIA_KID_LEFT = _with(_KID_LEFT, {1: "....kCCCCQQk....", 3: "....kCSsCQQk...."})
ARCHETYPES["elaia_kid"] = _dirs(
    _front_kid(_ELAIA_KID_DOWN), _front_kid(_ELAIA_KID_UP),
    dict(stand=_ELAIA_KID_LEFT,
         walk0=_with(_ELAIA_KID_LEFT, {2: "....kCCSsQk.....", 3: "....kCCSsQk.....",
                                      4: "....kCCSSQk.....", 5: "...kXYkYYk......", 6: "..kFFk.kFFk....."}),
         walk1=_with(_ELAIA_KID_LEFT, {2: "....kSsCCQk.....", 3: "....kSsCCQk.....",
                                      4: "....kSSCCQk.....", 5: "...kYYkXYk......", 6: "..kFFk.kFFk....."})),
)

# Eight-row harbor heads keep room for a longer torso and a complete stride.
_AKTI_DOWN = [
    "...kCCSSSCQk....",
    "..kCCCCCCCQQk...",
    "..kSCCQCCCQSsk..",
    "..kSsCCQCCQSsk..",
    "..kSsTTTTTTSsk..",
    "..kSSCCCCCQSSk..",
    "...kCCCQCCQQk...",
    "....kXYkkXYk....",
    "....kXYkkXYk....",
    "....kXYkkXYk....",
    "....kXYkkXYk....",
    "....kXYkkXYk....",
    "....kXYkkXYk....",
    "...kFFFkkFFk....",
]
_AKTI_UP = _with(_AKTI_DOWN, {0: "...kCCCCCCQk....", 3: "..kSsCQCCCQSsk.."})
_AKTI_LEFT = [
    ".....kSSCQk.....",
    "....kCCCCQQk....",
    "....kCSsCQk.....",
    "....kCSsCQQk....",
    "....kTSsTTk.....",
    "....kCSSCQQk....",
    "....kCCQCCQk....",
    "....kkXYkkkk....",
    ".....kXYk.......",
    ".....kXYk.......",
    ".....kXYk.......",
    ".....kXYk.......",
    ".....kXYk.......",
    "....kFFFk.......",
]
_AKTI_STEP0 = {
    11: "....kXYkkFFk....", 12: "....kXYk........", 13: "...kFFFk........",
}
_AKTI_STEP1 = {
    11: "....kFFkkXYk....", 12: "........kXYk....", 13: "........kFFk....",
}


def _akti_front(rows):
    return dict(stand=rows,
                walk0=_with(rows, {**_HANDS_W0, **_AKTI_STEP0}),
                walk1=_with(rows, {**_HANDS_W1, **_AKTI_STEP1}))


ARCHETYPES["akti_tunic"] = _dirs(
    _akti_front(_AKTI_DOWN), _akti_front(_AKTI_UP),
    dict(
        stand=_AKTI_LEFT,
        walk0=_with(_AKTI_LEFT, {
            **_ARM_BACK,
            8: "....kXYkkYYk....", 9: "....kXYkkkYYk...", 10: "...kXYk..kYYk...",
            11: "..kXYk....kYYk..", 12: "..kXYk....kYYk..",
            13: ".kFFFk....kFFk..",
        }),
        walk1=_with(_AKTI_LEFT, {
            **_ARM_FWD,
            8: "....kYYkkXYk....", 9: "....kYYkkkXYk...", 10: "...kYYk..kXYk...",
            11: "..kYYk....kXYk..", 12: "..kYYk....kXYk..",
            13: ".kFFk.....kFFFk.",
        }),
    ),
)
POSES = ("stand", "walk0", "walk1")
DIRS = ("down", "up", "left")


# --------------------------------------------------------------------------
# Composition
# --------------------------------------------------------------------------

def _resolve(rows, roles):
    m = {**DEFAULT_ROLES, **roles}
    return ["".join(m.get(ch, ch) for ch in r) for r in rows]


def _paint(fig, start, rows, head_len, where):
    if isinstance(start, str):
        start = head_len + int(start[1:])
    for j, r in enumerate(rows):
        y = start + j
        if len(r) != W:
            raise ValueError(f"{where}: overlay row {j} is {len(r)} px wide: {r!r}")
        if not 0 <= y < len(fig):
            raise ValueError(f"{where}: overlay row {j} lands at figure row {y}, outside the figure")
        line = list(fig[y])
        for x, ch in enumerate(r):
            if ch != "_":
                line[x] = ch
        fig[y] = "".join(line)


def pole(x, start, cells):
    """An overlay of short cell strings placed at column x, one per row, for
    staffs, spears and other props that run down the figure."""
    rows = []
    for c in cells:
        r = ["_"] * W
        for i, ch in enumerate(c):
            if ch != "_":
                r[x + i] = ch
        rows.append("".join(r))
    return (start, rows)


def figure(spec, d, pose):
    """The figure for one direction and pose as resolved palette rows.

    The "bow" pose is the down-facing stand with the spec's "bow" overlays
    painted on top. Only walkers that play Movement_PkmnCenterNurse_Bow have
    one; see build_sheet."""
    head = spec["head"][d]
    base = "stand" if pose == "bow" else pose
    body = ARCHETYPES[spec["arch"]][d][base]
    fig = list(head) + list(body)
    over = spec.get("over", {}).get(d, {})
    keys = ["all", base] if base == "stand" else ["all", "walk", pose]
    if pose == "bow":
        keys.append("bow")
    for key in keys:
        for start, rows in over.get(key, []):
            _paint(fig, start, rows, len(head), f"{spec['name']} {d} {pose} [{key}]")
    return _resolve(fig, spec.get("roles", {}))


def build_frame(rows, y, legend, pal, where):
    frame = np.zeros((H, W), np.int32)
    for j, row in enumerate(rows):
        if len(row) != W:
            raise ValueError(f"{where}: row {j} is {len(row)} px wide: {row!r}")
        yy = y + j
        if not 0 <= yy < H:
            raise ValueError(f"{where}: row {j} lands at y={yy}, outside the frame")
        for x, ch in enumerate(row):
            if ch in ". ":
                continue
            if ch not in legend:
                raise ValueError(f"{where}: unknown char {ch!r} at row {j} col {x}")
            frame[yy, x] = pal[legend[ch]]
    return frame


def build_sheet(spec):
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
    order = [("down", "stand"), ("up", "stand"), ("left", "stand"),
             ("down", "walk0"), ("down", "walk1"), ("up", "walk0"), ("up", "walk1"),
             ("left", "walk0"), ("left", "walk1")]
    # Frame 9 is the bow that sAnimTable_Nurse's ANIM_NURSE_BOW plays. A walker
    # whose scripts run Movement_PkmnCenterNurse_Bow needs it, or waitmovement
    # never returns.
    if "bow" in spec.get("over", {}).get("down", {}):
        rows = figure(spec, "down", "bow")
        frames[("down", "bow")] = build_frame(rows, FEET_ROW + 1 - len(rows), legend, pal,
                                              f"{spec['name']} down bow")
        order.append(("down", "bow"))
    return np.hstack([frames[k] for k in order])


# --------------------------------------------------------------------------
# Townsfolk (folk palette)
# --------------------------------------------------------------------------

# Melitta, the player's mother and Elaia's beekeeper: hair up in a bun tied
# with a honey-gold ribbon, a terracotta peplos and a linen apron.
MOM = dict(
    name="mom", pal="folk", arch="elaia_robe",
    roles=dict(C="u", Q="b", T="L", F="b"),
    head=dict(
        down=[
            "......kkkk......",
            ".....kbuubk.....",
            ".....kOOOOk.....",
            "...kkbbbbbbkk...",
            "..kbuubbbbbbbk..",
            "..kbubbbbbbbbk..",
            "..kbbSSbbSSbbk..",
            "..kbSkSSSSkSbk..",
            "..bSSkSSSSkSSb..",
            "...bSSSSSSSSb...",
            "....bssSSssb....",
        ],
        up=[
            "......kkkk......",
            ".....kbuubk.....",
            ".....kOOOOk.....",
            "...kkbbbbbbkk...",
            "..kbuubbbbbbbk..",
            "..kbubbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..bsbbbbbbbbsb..",
            "...bsbbbbbbsb...",
            "....bsSSSSsb....",
        ],
        left=[
            "..........kkk...",
            ".........kbuuk..",
            "......kkkkOObk..",
            "....kkbbbbkkk...",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbk...",
            "..kSkSSSSbbk....",
            "...bsSSSsbk.....",
        ],
    ),
    over=dict(
        down={"all": [("b5", ["_____LLLLLl_____", "_____LLLLLl_____",
                              "_____LLLLLl_____", "_____lLLLLl_____"])]},
        up={"all": [("b5", ["______Ll________"])]},
        left={"all": [("b6", ["_____L__________", "____LL__________", "____Ll__________"])]},
    ),
)

# Halia, the old island priestess who reads each youth's thread: a saffron
# veil over gray hair, a white peplos, and a drop spindle in her left hand.
PRIESTESS = dict(
    name="priestess", pal="folk", arch="elaia_robe",
    roles=dict(C="L", Q="l", T="O", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kOOooook....",
            "...kOOooooouk...",
            "..kOoooooooouk..",
            "..kOoooooooouk..",
            "..kouuuuuuuuuk..",
            "..koyLLLLLLyuk..",
            "..koSkSSSSkSuk..",
            "..koSkSSSSkSuk..",
            "..kosSSSSSSsuk..",
            "..kouksSSskuuk..",
        ],
        up=[
            ".....kkkkkk.....",
            "....kOOooook....",
            "...kOOooooouk...",
            "..kOoooooooouk..",
            "..kOoooooooouk..",
            "..kOooouoooouk..",
            "..kOooouooouuk..",
            "..kOooouooouuk..",
            "..kOooouooouuk..",
            "..kOooouooouuk..",
            "..kOooouooouuk..",
        ],
        left=[
            ".....kkkkkk.....",
            "....kOOooook....",
            "...kOOooooouk...",
            "..kOoooooooouk..",
            "..kOoooooooouk..",
            "..kuuuuooooouk..",
            "..kyLLyuoooouk..",
            "..kSSSSuoooouk..",
            "..kSkSSSuooouk..",
            "..kSkSSSuooouk..",
            "...kssskuooouk..",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["..koukLSSLkuuk..", "___ou_______u___"]),
                      ("b6", ["____________u___", "___________kOk__", "____________b___"])],
              "walk0": [("b5", ["..kSSCCCCCQSSk..", "..kkCCCCCCCQuk.."])]},
        up={"all": [("b0", ["..kOooouooouuk..", "..kOooouooouuk..",
                            "_____oouoou_____", "_____oouoou_____", "____kuuuuuuk____"]),
                    ("b6", ["___u____________", "__kOk___________", "___b____________"])],
            "walk1": [("b5", ["..kSSCCCCCQSSk..", "..kuCCCCCCCQkk.."])]},
        left={"all": [("b0", ["__________oouk__", "__________oouk__",
                              "__________ouuk__", "__________kuuk__"])],
              "stand": [("b6", ["______u_________", "_____kOk________", "______b_________"])],
              "walk0": [("b6", ["_______u________", "______kOk_______", "_______b________"])],
              "walk1": [("b6", ["_____u__________", "____kOk_________", "_____b__________"])]},
    ),
)

# Philon, a nervous festival youth: a short linen chiton and the festival's
# olive wreath, its leaves sprigging past his brown hair, tied behind with
# terracotta ribbons.
YOUTH_M = dict(
    name="youth_m", pal="folk", arch="elaia_tunic",
    roles=dict(C="L", Q="l", T="b", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            ".g.kbuubbbbbk.g.",
            ".gkbubbbbbbbbkg.",
            ".vgvggvggvggvgv.",
            "..kbSbbSbbSbbk..",
            "..bsSkSSSSkSsb..",
            "..bsSkSSSSkSsb..",
            "...bSSSSSSSSb...",
            "....bssSSssb....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            ".g.kbuubbbbbk.g.",
            ".gkbubbbbbbbbkg.",
            ".vgvggvggvggvgv.",
            "..kbbbbuubbbbk..",
            "..bsbbbuubbbsb..",
            "..bsbbbbubbbsb..",
            "...bbbbbubbbb...",
            "....bbSSSSbb....",
        ],
        left=[
            "......kkkkk.....",
            "....kkbbbbbk....",
            "...kbuubbbbbk.g.",
            "..kbubbbbbbbbkg.",
            ".gvgggvgggvggvg.",
            "..kbSbSbbbbbbuk.",
            "..kSSSSSbsbbbuk.",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbk...",
            "...bsSSSsbbk....",
        ],
    ),
)

# Korinna, a sharp-tongued festival youth: a sky-blue chiton to mid-calf with
# a linen girdle, and a long braid tied with a terracotta ribbon.
YOUTH_F = dict(
    name="youth_f", pal="folk", arch="elaia_midi",
    roles=dict(C="a", Q="B", T="L", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbkk..",
            "..kbubbbbbbbkuk.",
            "..kbbbbbbbbbkuk.",
            "..kbSbbbbbbSbk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "..kbsSSSSSSsbk..",
            "...kbssSSssbk...",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbkk..",
            "..kbubbbbbbbkuk.",
            "..kbbbbbbbbbkuk.",
            "..kbbbbubbbbbk..",
            "..kbbbbbubbbbk..",
            "..kbbbbubbbbbk..",
            "..kbbbbbubbbbk..",
            "..kSbbbubbbbSk..",
            "...kSSkbukSSk...",
        ],
        left=[
            "......kkkkk.....",
            "....kkbbbbbk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbbk..",
            "..kSSSSSsbbubk..",
            "...kbsSssbkbbk..",
        ],
    ),
    over=dict(
        up={"all": [("b0", ["_______ub_______", "_______bu_______", "_______ub_______",
                            "______kuuk______", "_______kk_______"])]},
        left={"all": [("b0", ["__________ubk___", "__________buk___", "__________kuk___",
                              "___________k____"])]},
    ),
)

# An island man: a knee-length ochre exomis off his right shoulder, a brown
# beard and sandals.
MAN = dict(
    name="man", pal="folk", arch="elaia_tunic",
    roles=dict(C="o", Q="u", T="b", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kSSkSSSSkSSk..",
            "..kbbSSSSSSbbk..",
            "...kbbbssbbbk...",
            "....kbbbbbbk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..ksbbbbbbbbsk..",
            "..ksbbbbbbbbsk..",
            "...kbbSSSSbbk...",
            "....kbSSSSbk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkbbbbbk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSbbbbbk...",
            "...kbbbbbbbk....",
            "....kbbbbk......",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["____SS__________", "___SSs__________"])]},
        up={"all": [("b0", ["__________SS____", "__________sSS___"])]},
    ),
)

# An island woman: a blue peplos, an ochre himation over her left shoulder and
# a linen kerchief over her hair.
WOMAN = dict(
    name="woman", pal="folk", arch="elaia_robe",
    roles=dict(C="B", Q="n", T="n", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kLLLLLLk....",
            "...kLLLLLLLlk...",
            "..kLLLLLLLLLlk..",
            "..kbbbbbbbbbbk..",
            "..kbbSSbbSSbbk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "..kbsSSSSSSsbk..",
            "...kbssSSssbk...",
        ],
        up=[
            ".....kkkkkk.....",
            "....kLLLLLLk....",
            "...kLLLLLLLlk...",
            "..kLLLLLLLLLlk..",
            "..kbbbbLLbbbbk..",
            "..kbbbkllkbbbk..",
            "..kbbbbllbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "...kbbbbbbbbk...",
            "....kbSSSSbk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkLLLLLk....",
            "...kLLLLLLLLk...",
            "..kLLLLLLLLLlk..",
            "..kbbbbbbbbLlk..",
            "..kbSbbbbbbblLk.",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbbk..",
            "..kSSSSSsbbbbk..",
            "...kbsSssbbbk...",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["__________oo____", "_________ooou___", "________ooou____",
                              "_______ooou_____", "______ooou______", "_____ooou_______",
                              "____uoou________", "___kuu__________"])]},
        up={"all": [("b0", ["____oo__________", "___uooo_________", "____uooo________",
                            "_____uooo_______", "______uooo______", "_______uooo_____",
                            "________uoou____", "__________uuk___"])]},
        left={"all": [("b0", ["_____ooo________", "____kooou_______"]),
                      ("b2", ["_________ou_____", "_________ou_____", "_________uu_____",
                              "_________uk_____"])]},
    ),
)

# An old man of the island (farmers, shepherds, the Lakonian elder): bald with
# a white fringe and a long white beard, an olive-wool himation to mid-calf and
# a walking staff in his right hand.
_STAFF = ["_k", "ko"] + ["ku"] * 17 + ["kb"]
ELDER_M = dict(
    name="elder_m", pal="folk", arch="elaia_midi",
    roles=dict(C="g", Q="v", T="g", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kSSSSSSk....",
            "...kSSSSSSSsk...",
            "..kSSSSSSSSSsk..",
            "..kLSSSSSSSSyk..",
            "..kLSyySSyySyk..",
            "..kLSkSSSSkSyk..",
            "..kySkSSSSkSyk..",
            "..kyLLsSSsLLyk..",
            "...kLLLLLLLLk...",
            "....kyLLLLyk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kSSSSSSk....",
            "...kSSSSSSSsk...",
            "..kSSSSSSSSSsk..",
            "..kSSSSSSSSSsk..",
            "..kLSSSSSSSSyk..",
            "..kLLSSSSSSLyk..",
            "..kLLLLLLLLLyk..",
            "..kyLLLLLLLLyk..",
            "...kyLLLLLLyk...",
            "....ksSSSSsk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkSSSSSk....",
            "...kSSSSSSSsk...",
            "..kSSSSSSSSSsk..",
            "..kSSSSSSSSSsk..",
            "..kyySSSSLLLyk..",
            "..kSSSSSsLLLyk..",
            "..kSkSSSsLLLyk..",
            "..kLkSSLLLLLk...",
            "..kLLLLLLLyk....",
            "...kLLLLLyk.....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["______LLLy______", "______yLy_______"]),
                      ("b2", ["_______v________", "________v_______", "_________v______"]),
                      pole(0, 1, _STAFF), ("b5", ["__S_____________"])],
              "walk1": [("b5", ["..SSSCCCCCQSSk..", "..kkCCCCCCCQkk.."])]},
        up={"all": [pole(14, 1, [c[::-1] for c in _STAFF]), ("b5", ["_____________S__"])],
            "walk0": [("b5", ["..kSSCCCCCQSSS..", "..kkCCCCCCCQkk.."])]},
        left={"all": [pole(0, 1, _STAFF), ("b4", ["__Ss____________"])]},
    ),
)

# Kydippe, the old midwife: a dark wool himation drawn over her gray hair and
# wrapped round her, her hands folded in front, a linen chiton below.
_KYDIPPE_FRONT = [
    "..kubbubbbbbkk..",
    "..kubbbubbbbkk..",
    "..kubbbbubbbkk..",
    "..kubbbbbubbkk..",
    "..kubbbSSbbbkk..",
    "..kubbbbbbbbkk..",
    "..kkuubuuuuukk..",
    "...klllllllyk...",
    "..klllllllllyk..",
]
ELDER_F = dict(
    name="elder_f", pal="folk", arch="elaia_robe",
    roles=dict(C="b", Q="k", T="b", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbuubbbk....",
            "...kbLLLyyybk...",
            "..kbyLLyyLLybk..",
            "..kbyyLSSLyybk..",
            "..kbySSSSSSybk..",
            "..kbSkkSSkkSbk..",
            "..kbuSSSSSSubk..",
            "..kbSSsSSsSSbk..",
            "..kbbsSssSsbbk..",
            "..kbbkSSSSkbbk..",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbuubbbk....",
            "...kbLLLyyybk...",
            "..kbyLLyyyyybk..",
            "..kbyyyLLyyybk..",
            "..kbyykLLkyybk..",
            "..kbuuukkuuubk..",
            "..kbbbbbbbbbkk..",
            "..kbubbbbbbbkk..",
            "..kbubbbbbbbkk..",
            "..kbbbbbbbbbkk..",
        ],
        left=[
            ".....kkkkkk.....",
            "....kbuubbbk....",
            "...kLLLLybbbk...",
            "..kLLyyyyubbbk..",
            "..kyyyyyyubbbk..",
            "..kSSSyyyubbbk..",
            "..kSkkSSyubbbk..",
            "..kSSuSSyubbbk..",
            "..ksSSSSyubbbk..",
            "..ksSSSsbubbbk..",
            "...kssskbubbkk..",
        ],
    ),
    over=dict(
        down={"all": [("b0", _KYDIPPE_FRONT),
                      ("b0", ["_______LL_______", "_______Ll_______"])]},
        up={"all": [("b0", ["..kubbbbbbbbkk..", "..kubbbbbbbbkk..", "..kubbbbbbbbkk..",
                            "..kubbbbbbbbkk..", "..kluubbbbuuyk..", "..kLllkuukllyk..",
                            "..kkLllkklllkk..", "...kLllllllyk...", "..kLllllllllyk.."])]},
        left={"all": [("b0", [".....kbbbbk.....", "....kubbbbbk....", "....kubbbbbk....",
                              "....kubbbbbk....", "...kSSbbbbbk....", "....kubbbbbk....",
                              "....kuuuuuuk....", "...kllllllyk....", "...klllllllyk..."])]},
    ),
)

# A barefoot island boy: a short terracotta tunic and a mop of dark hair.
KID_M = dict(
    name="kid_m", pal="folk", arch="elaia_kid",
    roles=dict(C="u", Q="b", T="u", F="s"),
    head=dict(
        down=[
            ".....kkkkk......",
            "....kbbbbbkk....",
            "...kbuubbbbbk...",
            "...kbbbbbbbbk...",
            "...kbSbbSbbbk...",
            "...bSkSSSSkSb...",
            "...bSkSSSSkSb...",
            "....bsSSSSsb....",
            ".....bssssb.....",
        ],
        up=[
            ".....kkkkk......",
            "....kbbbbbkk....",
            "...kbuubbbbbk...",
            "...kbbbbbbbbk...",
            "...kbbbbbbbbk...",
            "...bsbbbbbbsb...",
            "...bsbbbbbbsb...",
            "....bbbbbbbb....",
            ".....bSSSSb.....",
        ],
        left=[
            "......kkkk......",
            "....kkbbbbk.....",
            "...kbuubbbbk....",
            "...kbbbbbbbbk...",
            "...kbSbbbbbbk...",
            "...kSSSSbsbbk...",
            "...kSkSSssbk....",
            "...ksSSSsbk.....",
            "....kssssk......",
        ],
    ),
)

# A barefoot island girl: a short saffron tunic and two short pigtails tied
# with terracotta.
KID_F = dict(
    name="kid_f", pal="folk", arch="kid",
    roles=dict(C="O", Q="o", T="O", F="s"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbk...",
            "..kubbbbbbbbuk..",
            ".kbkbSbbbbSbkbk.",
            ".kbkSkSSSSkSkbk.",
            "..kkSkSSSSkSkk..",
            "...kbsSSSSsbk...",
            "....kbssssbk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbk...",
            "..kubbbbbbbbuk..",
            ".kbkbbbbbbbbkbk.",
            ".kbkbbbbbbbbkbk.",
            "..kkbbbbbbbbkk..",
            "...kbbbbbbbbk...",
            "....kbSSSSbk....",
        ],
        left=[
            "......kkkk......",
            "....kkbbbbk.....",
            "...kbuubbbbk....",
            "...kbbbbbbbukk..",
            "...kbSbbbbbkbbk.",
            "...kSSSSbsbkbbk.",
            "...kSkSSssbkkk..",
            "...ksSSSsbk.....",
            "....kssssk......",
        ],
    ),
)

# A net-mender (Diktys, Glaukos and the harbor's fishers): a brown felt pilos,
# a gray beard, a faded sea-blue tunic with a rope belt, and a net slung over
# his shoulder.
FISHER = dict(
    name="fisher", pal="folk", arch="elaia_tunic",
    roles=dict(C="a", Q="B", T="u", F="b"),
    head=dict(
        down=[
            "......kkkk......",
            ".....kbuubk.....",
            "....kbuubbbk....",
            "...kbuubbbbbk...",
            "..kkbbbbbbbbkk..",
            "..kyySSSSSSyyk..",
            "..kySkSSSSkSyk..",
            "..kySkSSSSkSyk..",
            "..kyyLSSSSLyyk..",
            "...kyyLssLyyk...",
            "....kyyLLyyk....",
        ],
        up=[
            "......kkkk......",
            ".....kbuubk.....",
            "....kbuubbbk....",
            "...kbuubbbbbk...",
            "..kkbbbbbbbbkk..",
            "..kyyyyyyyyyyk..",
            "..kyyyyyyyyyyk..",
            "..ksyyyyyyyysk..",
            "...ksyyyyyysk...",
            "....kyySSyyk....",
            "....ksSSSSsk....",
        ],
        left=[
            ".......kkkk.....",
            "......kbuubk....",
            ".....kbuubbbk...",
            "....kbuubbbbbk..",
            "..kkbbbbbbbbbk..",
            "..kSSSSyysyyyk..",
            "..kSkSSSssyyyk..",
            "..kSkSSSSyyyk...",
            "..kLyLSyyyyk....",
            "...kyLyyyyk.....",
            "....kyyyk.......",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["____yl__________", "___lyly_________", "____lyly________",
                              "_____lyly_______", "______lyly______", "_______lyly_____",
                              "________lyl_____"])]},
        up={"all": [("b0", ["____klylylk_____", "___klylylylk____", "_____lylyly_____",
                            "_____ylylyl_____", "_____lylyly_____", "______kylyk_____"])]},
        left={"all": [("b0", ["_________lylk___", "_________ylylk__", "__________lylk__",
                              "__________ylyk__", "__________lylk__", "__________kkk___"])]},
    ),
)

# A rower or deckhand (the Lakonian rower too): tousled hair under a
# terracotta headband, a short jaw beard, bare-chested above an undyed linen
# kilt with a blue sash.
_SAILOR_CHEST = ["...kSSSSSSsk....", "..kSSSSSSSSssk..",
                 "..kSSSSsSSSSsk..", "..kSSssSSSSSsk.."]
_SAILOR_ROPE_DOWN = ["__________lL____", "_________l__L___",
                     "_________l__L___", "__________lL____"]
_SAILOR_ROPE_UP = ["____Ll__________", "___L__l_________",
                   "___L__l_________", "____Ll__________"]
_SAILOR_ROPE_LEFT = ["________lL______", "_______l__L_____",
                     "_______l__L_____", "________lL______"]
SAILOR = dict(
    name="sailor", pal="folk", arch="akti_tunic",
    roles=dict(C="l", Q="y", T="n", F="b"),
    head=dict(
        down=[
            ".....bbbbbb.....",
            "....bubbbbub....",
            "...buuuuuuubb...",
            "...bSSbSSbSSb...",
            "...bSkSSSSkSb...",
            "...bSSSSSSssb...",
            "....bSSSsssbb...",
            ".....bbsssbb....",
        ],
        up=[
            ".....bbbbbb.....",
            "....bubbbbub....",
            "...buuuuuuubb...",
            "...bbbbbbbbbb...",
            "...bsbbbbbbSb...",
            "...bsbbbbbbSb...",
            "....bbbbbbbb....",
            ".....bSSssb.....",
        ],
        left=[
            ".....bbbbbb.....",
            "....bubbbbb.....",
            "...buuuuuuuub...",
            "...bSbbbbbbbub..",
            "...bSSSSbsbbub..",
            "..bSkSSSssbbb...",
            "...bSSSsbbbbb...",
            "....bssbbbb.....",
        ],
    ),
    over=dict(
        down={"all": [("b0", _SAILOR_CHEST), ("b0", _SAILOR_ROPE_DOWN)]},
        up={"all": [("b0", ["...kSSSSSSsk....", "..kSSSSsSSSSsk..", "..kSSSSsSSSSsk..",
                            "..kSSssSSSSSsk.."]), ("b0", _SAILOR_ROPE_UP)]},
        left={"stand": [("b0", [".....kSSssk.....", "....ksSSsssk....", "....ksSSsssk....",
                                "....ksSSsssk...."]), ("b0", _SAILOR_ROPE_LEFT)],
              "walk0": [("b0", [".....kSSssk.....", "....kssSSssk....", "....kssSSssk....",
                                "....kssSSssk...."]), ("b0", _SAILOR_ROPE_LEFT)],
              "walk1": [("b0", [".....kSSssk.....", "....kSSssssk....", "....kSSssssk....",
                                "....kSSssssk...."]), ("b0", _SAILOR_ROPE_LEFT)]},
    ),
)

# Hydna, the sponge diver: wet black hair to her shoulders, a short sea-blue
# wrap tied with linen, bare feet, and a net bag of sponges at her hip.
DIVER = dict(
    name="diver", pal="folk", arch="akti_tunic",
    roles=dict(C="a", Q="B", T="L", F="s"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kBnkkkkk....",
            "...kBnkkknnkk...",
            "...kkSSkkSSkk...",
            "...kSkSSSSkSk...",
            "...knSSSSSsnk...",
            "...knsSSSssnk...",
            "...knksSssknk...",
        ],
        up=[
            ".....kkkkkk.....",
            "....kBnkkkkk....",
            "...kBnkkkkkkk...",
            "...kknkkkkkkk...",
            "...kknkkkkkkk...",
            "...kknkkkkkkk...",
            "...knkkkkkknk...",
            "...knkkkkkknk...",
        ],
        left=[
            ".....kkkkkk.....",
            "....kBnnkkkk....",
            "...kBnkkkkkkk...",
            "...kSkkkkknkk...",
            "..kSSSSSknkkk...",
            "..kSkSSSsknkk...",
            "...ksSSSSkkkk...",
            "....kssskknkk...",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["..kn________nk..", "___SS______Ss___"]),
                      ("b6", ["___________kOyOk", "___________kyOyk", "____________kkk_"])]},
        up={"all": [("b0", ["..kkkknnkkkkk...", "___SS______Ss___"]),
                    ("b6", ["kOyOk___________", "kyOyk___________", "_kkk____________"])]},
        left={"all": [("b0", ["_________knk____", "______SS________"]),
                      ("b6", ["_____kOyOk______", "_____kyOyk______", "______kkk_______"])]},
    ),
)

# An Asclepeion healer, where the Nurse stood: a white chiton to the floor, an
# olive-green sash and fillet, and a gold serpent armlet on her left arm.
_ROD = ["_k_", "kgk", "kbg", "gbk", "kbg", "gbk", "kbg", "gbk"] + ["kb"] * 10 + ["kb"]
HEALER = dict(
    name="healer", pal="folk", arch="robe",
    roles=dict(C="L", Q="l", T="g", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbk...",
            "..kgggggggggvk..",
            "..kbubbbbbbbbk..",
            "..kbbbSbbSbbbk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "..kbsSSSSSSsbk..",
            "..kbbssSSssbbk..",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbk...",
            "..kgggggggggvk..",
            "..kbubbbbbbbbk..",
            "..kbbbubbbubbk..",
            "..kbbbubbbubbk..",
            "..kbbbubbbubbk..",
            "..kbbbubbbubbk..",
            "..kbbbubbbubbk..",
            "..kbbbubbbubbk..",
        ],
        left=[
            "......kkkkk.....",
            "....kkbbbbbk....",
            "...kbuubbbbbk...",
            "..kgggggggggvk..",
            "..kbubbbbbbbbk..",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbbk..",
            "..ksSSSSsbbbbk..",
            "...kssssbbbbk...",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["..kbb______bbk..", "___b________b___"]),
                      ("b2", ["___________Oo___"]),
                      pole(0, 2, _ROD), ("b5", ["__S_____________"])],
              "walk1": [("b5", ["..SSSCCCCCQSSk..", "..kkCCCCCCCQkk.."])],
              # The bow: the crown tips toward the viewer, so the top of the
              # head drops a pixel, the fillet two, the eyes close and the neck
              # disappears. Her left hand comes up over her heart; the rod
              # stays planted.
              "bow": [(0, ["___.............",
                           "___..kkkkkk.....",
                           "___.kbbbbbbk....",
                           "___kbuubbbbbk...",
                           "___bubbbbbbbbk..",
                           "___gggggggggvk..",
                           "___bbbbbbbbbbk..",
                           "___bbSSSSSSbbk..",
                           "___bSkkSSkkSbk..",
                           "___bsSSSSSSsbk..",
                           "___bbssSSssbbk..",
                           "___bbLLLLLLbbk.."]),
                      ("b2", ["___SSLLLLSSSOk..",
                              "___SsLLLLLLsSk..",
                              "___SsggggggSSk..",
                              "___SSLLLLLLLlk.."])]},
        up={"all": [("b0", ["...kbbubbbubk...", "____kbubbbuk____", "_____kubbuk_____",
                            "______kkkk______"]),
                    ("b2", ["___Oo___________"]),
                    pole(13, 2, [c[::-1].rjust(3, "_") for c in _ROD]), ("b5", ["_____________S__"])],
            "walk0": [("b5", ["..kSSCCCCCQSSS..", "..kkCCCCCCCQkk.."])]},
        left={"all": [("b0", ["_________bbk____", "_________bk_____"]),
                      pole(0, 2, _ROD), ("b4", ["__Ss____________"])],
              "stand": [("b2", ["______Oo________"])],
              "walk0": [("b2", ["_______Oo_______"])],
              "walk1": [("b2", ["_____Oo_________"])]},
    ),
)

# Demeas and the Agora's stall-keepers: balding, bearded, a blue chiton with a
# leather belt, a linen apron and a coin purse.
MERCHANT = dict(
    name="merchant", pal="folk", arch="tunic",
    roles=dict(C="B", Q="n", T="b", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kSSSSSSk....",
            "...kSSSSSSSsk...",
            "..kbSSSSSSSSbk..",
            "..kbbSSSSSSbbk..",
            "..kbSbbSSbbSbk..",
            "..kbSkSSSSkSbk..",
            "..kSSkSSSSkSSk..",
            "..kbbbsSSsbbbk..",
            "...kbbbbbbbbk...",
            "....kbbbbbbk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kSSSSSSk....",
            "...kbSSSSSSbk...",
            "..kbbbSSSSbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..ksbbbbbbbbsk..",
            "..ksbbbbbbbbsk..",
            "...kbbSSSSbbk...",
            "....kbSSSSbk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkSSSSbk....",
            "...kSSSSSbbbk...",
            "..kSSSSSbbbbbk..",
            "..kSSSSbbbbbbk..",
            "..kbbSSbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSbbbbbk...",
            "...kbbbbbbbk....",
            "....kbbbbk......",
        ],
    ),
    over=dict(
        down={"all": [("b5", ["_____LLLLbO_____", "_____lLLLbb_____"])]},
        up={"all": [("b5", ["______LL________"])]},
        left={"all": [("b5", ["_____L__bO______", "_____L__bb______"])]},
    ),
)

# Phyllis and the olive-pickers: a terracotta headscarf knotted at the side,
# an olive-green dress to the floor, a linen apron and a wicker basket of
# olives on her left hip.
_BASKET = ["_kkk_", "kvgvk", "kOOOk", "kOoOk", "_kkk_"]
HARVESTER = dict(
    name="harvester", pal="folk", arch="elaia_robe",
    roles=dict(C="g", Q="v", T="b", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kuuuuuuk....",
            "...kuuuuuuubk...",
            "..kuuuuuuuuubkk.",
            "..kbuuuuuuuubkuk",
            "..kbbbbbbbbbbkuk",
            "..kbSSSSSSSSbkk.",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "...bsSSSSSSsb...",
            "....bssSSssb....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kuuuuuuk....",
            "...kuuuuuuubk...",
            ".kkuuuuuuuuubk..",
            "kukuuuuuuuuubk..",
            "kukbuuuuuuuubk..",
            ".kkbbuuuuuubbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "...kbbbbbbbbk...",
            "....kbSSSSbk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkuuuuuk....",
            "...kuuuuuuuuk...",
            "..kuuuuuuuuubk..",
            "..kbuuuuuuuubk..",
            "..kbbbbuuuuubk..",
            "..kSSSSbkuukbk..",
            "..kSkSSSkuukbk..",
            "..kSkSSSSkkbbk..",
            "..kSSSSSsbbbk...",
            "...kbsSssbbk....",
        ],
    ),
    over=dict(
        down={"all": [("b5", ["_____LLLLLl_____", "_____LLLLLl_____",
                              "_____LLLLLl_____", "_____lLLLLl_____"]),
                      pole(11, "b3", _BASKET)]},
        up={"all": [("b5", ["______Ll________"]), pole(0, "b3", _BASKET)]},
        left={"all": [("b6", ["_____L__________", "____LL__________", "____Ll__________"]),
                      pole(8, "b3", _BASKET)]},
    ),
)

# Komatas and the hill goatherds: wild graying curls and beard, a syrinx at
# his lips, a shaggy goat-hair cloak over a coarse undyed tunic, a bronze
# goat-bell on his rope belt, and leg thongs.
GOATHERD = dict(
    name="goatherd", pal="folk", arch="tunic",
    roles=dict(C="l", Q="y", T="u", F="b"),
    head=dict(
        down=[
            "....kk.kk.kk....",
            "...kbbkbbkbbk...",
            "..kbybbbbbbbbk..",
            ".kbybbbbbbbbbbk.",
            ".kbbbbbbbbbbybk.",
            ".kybbSSbbSSbbyk.",
            "..kySkSSSSkSyk..",
            "..kbSkSSSSkSbk..",
            "..kbySSSSSSybk..",
            "..kbbboOoObbbk..",
            "...kbybbbbybk...",
        ],
        up=[
            "....kk.kk.kk....",
            "...kbbkbbkbbk...",
            "..kbybbbbbbbbk..",
            ".kbbbbbbbybbbbk.",
            ".kbybbbbbbbbbbk.",
            ".kbbbbbybbbbbbk.",
            "..kbbbbbbbbybk..",
            "..kbybbbbbbbbk..",
            "..kbbbbbbybbbk..",
            "...kbbbbbbbbk...",
            "....kbSSSSbk....",
        ],
        left=[
            ".....kk.kk.kk...",
            "....kbbkbbkbbk..",
            "...kbybbbbbbbbk.",
            "..kbybbbbbbbbbk.",
            "..kbSbbbbbbbybk.",
            "..kSSSSSbsbbbbk.",
            "..kSkSSSssbbybk.",
            "..kSkSSybbbbbk..",
            "..kbSbbbybbbk...",
            "..ooOkbbbbbk....",
            "...kbybbbk......",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["..ky________yk..", ".ky__________yk.", ".ky__________bk.",
                              ".kb__________bk.", ".ky__________yk.", ".kb__________bk.",
                              ".kyk________kbk.", "..k__________k.."]),
                      ("b5", ["_______Oo_______", "_______kk_______", "_____b___b______"])]},
        up={"all": [("b0", ["..kyyyyyyyyyyk..", ".kyybyyybyyybyk.", ".kyybyyybyyybyk.",
                            ".kybyyybyyybyyk.", ".kybyyybyyybyyk.", ".kyybyyybyyybyk.",
                            ".kbyykbyykbyykk.", "..kk.k.kk.k.kk.."]),
                    ("b7", ["_____b___b______"])]},
        left={"all": [("b0", ["_________kyk____", "_________yybk___", "_________yybk___",
                              "_________ybyyk__", "_________ybyyk__", "_________yybyk__",
                              "_________kybkk__", "__________k_k___"]),
                      ("b4", ["_________o______"])]},
    ),
)


# --------------------------------------------------------------------------
# Trainer classes in the cast palette (sprites_npc.py): fairer skin, crimson,
# bronze, linen and blue, as in their battle portraits (sprites_classes.py).
# --------------------------------------------------------------------------

_CROOK = ["_kkk_", "kuouk", "kukuk", "ku_k_"] + ["ku"] * 18 + ["kb"]
_BLANK3 = ["................"] * 3

# Tityros and the island shepherds: a bronze felt pilos, a sheepskin mantle
# over a blue tunic, sandals, and a crook in his right hand.
SHEPHERD = dict(
    name="shepherd", pal="cast", arch="elaia_tunic",
    roles=dict(C="B", Q="n", T="b", F="b"),
    head=dict(
        down=_BLANK3 + [
            "......kkkk......",
            ".....kOoouk.....",
            "....kOoooouk....",
            "...kOoooooouk...",
            "..kuuuuuuuuuuk..",
            "..kbbSSSSSSbbk..",
            "..kbSkSSSSkSbk..",
            "..bSSkSSSSkSSb..",
            "...bSSSSSSSSb...",
            "....bssSSssb....",
        ],
        up=_BLANK3 + [
            "......kkkk......",
            ".....kOoouk.....",
            "....kOoooouk....",
            "...kOoooooouk...",
            "..kuuuuuuuuuuk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..bsbbbbbbbbsb..",
            "...bbbbbbbbbb...",
            "....bbSSSSbb....",
        ],
        left=_BLANK3 + [
            ".......kkkk.....",
            "......kOoouk....",
            ".....kOoooouk...",
            "....kOoooooouk..",
            "..kkuuuuuuuuuk..",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbk...",
            "...bsSSSsbbk....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["..kLLLkSSkLLlk..", "..kLlLLLLLLlLk..", "______lLLl______"]),
                      pole(0, 0, _CROOK), ("b5", ["__S_____________"])],
              "walk1": [("b5", ["..SSSCCCCCQSSk..", "..kkCCCCCCCQkk.."])]},
        up={"all": [("b0", ["..kLLLLLLLLLlk..", "..kLlLLlLLlLlk..", "_____LLlLLl_____",
                            "_____lLLlLl_____", "______lkll______"]),
                    pole(11, 0, [c.rjust(5, "_")[::-1] for c in _CROOK]), ("b5", ["_____________S__"])],
            "walk0": [("b5", ["..kSSCCCCCQSSS..", "..kkCCCCCCCQkk.."])]},
        left={"all": [("b0", [".....kSSLLLk....", "....kLLLLLLlk...", "________LLlk____",
                              "________lLlk____", "_________lk_____"]),
                      pole(0, 0, _CROOK), ("b4", ["__Ss____________"])]},
    ),
)

_SPEAR = ["_k_", "kOk", "kok", "_u_"] + ["ku"] * 19 + ["kb"]
_HOPLON = ["__kkkk__", "_kooook_", "kocOOcok", "koOccOok", "koOcrOok", "kocrrrok",
           "_kooook_", "__kkkk__"]
_HOPLON_BACK = ["__kkkk__", "_kooook_", "kouuuuok", "koubbuok", "kouuuuok", "kouuuuok",
                "_kooook_", "__kkkk__"]

# Agis and the Lakonian youths: a Corinthian helmet pushed up with a crimson
# crest, a linen corselet over a crimson chiton, bronze greaves, a spear, and a
# crimson hoplon with a bronze rim and Lakonia's lambda.
HOPLITE = dict(
    name="hoplite", pal="cast", arch="tunic",
    roles=dict(C="c", Q="r", T="o", F="b", X="O", Y="o"),
    head=dict(
        down=_BLANK3 + [
            "......kkkk......",
            ".....kcccrk.....",
            "....kkccrrkk....",
            "...kOOooooouk...",
            "..kOokkookkouk..",
            "..kooooooooouk..",
            "..kbSbbSbbSbbk..",
            "..bsSkSSSSkSsb..",
            "..bsSkSSSSkSsb..",
            "...bSSSSSSSSb...",
            "....bssSSssb....",
        ],
        up=_BLANK3 + [
            "......kkkk......",
            ".....kcccrk.....",
            "....kkccrrkk....",
            "...kOoocroouk...",
            "..kOoooroooouk..",
            "..kooooooooouk..",
            "..kbbbbbbbbbbk..",
            "..bsbbbbbbbbsb..",
            "..bsbbbbbbbbsb..",
            "...bbbbbbbbbb...",
            "....bbSSSSbb....",
        ],
        left=_BLANK3 + [
            ".......kkkk.....",
            "....kkcccrrk....",
            "...kccccrrrrk...",
            "...kOOoooooouk..",
            "..kOkkooooooouk.",
            "..koooooooooouk.",
            "..kbSbSbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbk...",
            "...bsSSSsbbk....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["____LL____Ll____", "___LLLLLLLLLl___", "_____LLLLLl_____",
                              "_____LLLLLl_____"]),
                      ("b5", ["_____LcLcLr_____", "____cLcLcLcr____"]),
                      pole(8, "b0", _HOPLON), pole(0, 0, _SPEAR), ("b5", ["__S_____________"])],
              "walk1": [("b5", ["..SSSLcLcLrSSk..", "..kkcLcLcLcrkk.."])]},
        up={"all": [("b0", ["___________L____", "___LLLLLLLLLl___", "_____LLLLLl_____",
                            "_____LLLLLl_____"]),
                    ("b5", ["_____cLcLcL_____", "____cLcLcLcr____"]),
                    pole(0, "b0", _HOPLON_BACK), pole(13, 0, [c[::-1] for c in _SPEAR]),
                    ("b5", ["_____________S__"])],
            "walk0": [("b5", ["..kSScLcLcLSSS..", "..kkcLcLcLcrkk.."])]},
        left={"all": [("b5", ["_____LcLcLr_____"]), pole(4, "b0", _HOPLON),
                      pole(0, 0, _SPEAR), ("b4", ["__Ss____________"])]},
    ),
)

# Polyeidos and the bird-watching seers: white hair and beard, a gold fillet
# with a black crow feather, an indigo robe under a slate himation, a hem
# frieze of black birds on terracotta, and a staff in his left hand.
_AUGUR_HEM = "___ukukukukuk___"
AUGUR = dict(
    name="augur", pal="cast", arch="robe",
    roles=dict(C="n", Q="k", T="t", F="b"),
    head=dict(
        down=[
            "............k...",
            ".....kkkkkk.k...",
            "....kLLLLLLkk...",
            "...kLLLLLLLlk...",
            "..kLLLLLLLLLlk..",
            "..kooooooooOok..",
            "..kLSSSSSSSSlk..",
            "..kLSkSSSSkSlk..",
            "..kLSkSSSSkSlk..",
            "..kLLLsSSsLLlk..",
            "...kLLLLLLLlk...",
            "....kLLLLLlk....",
        ],
        up=[
            "............k...",
            ".....kkkkkk.k...",
            "....kLLLLLLkk...",
            "...kLLLLLLLlk...",
            "..kLLLLLLLLLlk..",
            "..kooooooooOok..",
            "..kLLLLLLLLLlk..",
            "..kLLLLLLLLLlk..",
            "..kLLLLLLLLLlk..",
            "..klLLLLLLLLlk..",
            "...klLLLLLLlk...",
            "....kSSSSSSk....",
        ],
        left=[
            "...........k....",
            "......kkkkkk....",
            "....kkLLLLLkk...",
            "...kLLLLLLLLlk..",
            "..kLLLLLLLLLlk..",
            "..koooooooOook..",
            "..kSSSSSlLLLlk..",
            "..kSkSSSlLLLlk..",
            "..kSkSSSSLLLlk..",
            "..kLLLLLLLLlk...",
            "...kLLLLLLlk....",
            "....kLLLLk......",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["______LLLl______", "_______Ll_______"]),
                      ("b1", ["_________ttt____", "________ttt_____", "_______ttt______",
                              "______ttt_______", "_____ttt________", "____ttt_________"]),
                      ("b8", [_AUGUR_HEM]),
                      pole(14, 2, ["kk", "uk"] + ["uk"] * 17 + ["bk"]), ("b5", ["_____________S__"])],
              "walk0": [("b5", ["..kSSCCCCCQSSS..", "..kkCCCCCCCQkk.."])]},
        up={"all": [("b1", ["____ttt_________", "_____ttt________", "______ttt_______",
                            "_______ttt______", "________ttt_____", "_________ttt____"]),
                    ("b8", [_AUGUR_HEM]),
                    pole(0, 2, ["kk", "ku"] + ["ku"] * 17 + ["kb"]), ("b5", ["__S_____________"])],
            "walk1": [("b5", ["..SSSCCCCCQSSk..", "..kkCCCCCCCQkk.."])]},
        left={"all": [("b1", ["______tttk______", "_______ttk______"]),
                      ("b8", ["____ukukukuk____"]),
                      pole(0, 2, ["kk", "ku"] + ["ku"] * 17 + ["kb"]), ("b4", ["__Ss____________"])]},
    ),
)

# Lampon, Hestia's temple servant: close-cropped black hair, a smear of hearth
# soot across his cheek, a white chiton to the floor under a broad saffron
# himation, a saffron hem, and bronze tongs holding a glowing coal.
_TONGS = ["__ok", "_ok_", "kOck", "kcrk"]


def _side_tongs(x):
    """Tongs held out ahead in the side view, the coal at column x."""
    return pole(x, "b6", ["__oo", "kOck", "kcrk"])


ACOLYTE_M = dict(
    name="acolyte_m", pal="cast", arch="robe",
    roles=dict(C="L", Q="l", T="o", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kkttkkkk....",
            "...kktkkkkkkk...",
            "..kktkkkkkkkkk..",
            "..kkkkkkkkkkkk..",
            "..kkSkkSkkSkkk..",
            "..ksSkSSSSkSsk..",
            "..ksSkSSSSkSsk..",
            "...kSSSSSttSk...",
            "....kssSSssk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kkttkkkk....",
            "...kktkkkkkkk...",
            "..kktkkkkkkkkk..",
            "..kkkkkkkkkkkk..",
            "..kkkkktkkkkkk..",
            "..ksktkkkkkksk..",
            "..kskkkkkkkksk..",
            "...kkkkkkkkkk...",
            "....kkSSSSkk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkkttkkk....",
            "...kktkkkkkkk...",
            "..kktkkkkkkkkk..",
            "..kkkkkkkkkkkk..",
            "..kkSkSkkkkkkk..",
            "..kSSSSSksktkk..",
            "..kSkSSSsskkkk..",
            "..kSkttSSkkkk...",
            "...ksSSSskkk....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["_________OOO____", "________OOOoo___", "_______OOOoo____",
                              "______OOOoo_____", "_____OOooooo____", "_____oOoo_______"]),
                      ("b8", ["___oooooooooo___"]), pole(0, "b6", _TONGS)],
              "walk1": [("b5", ["..kSSoOooCQSSk..", "..okCCCCCCCQkk.."])]},
        up={"all": [("b0", ["___OOO__________", "___oOOOO________", "____oOOOO_______",
                            "_____oOOOO______", "____ooooooOO____", "_______ooOo_____"]),
                    ("b8", ["___oooooooooo___"])]},
        left={"all": [("b0", ["_____OOO________", "____kOOOo_______"]),
                      ("b2", ["_________OOo____", "_________OOo____", "_________ooo____",
                              "_________oOk____", "_________ook____"]),
                      ("b8", ["____ooooooo_____"])],
              "stand": [_side_tongs(1)],
              "walk0": [_side_tongs(2)],
              "walk1": [_side_tongs(0)]},
    ),
)

# Pyrrha and Aithra, Hestia's temple servants: auburn hair in a bun tied with
# saffron, a white peplos with a saffron girdle and hem, and a clay oil lamp
# held high.
_LAMP = ["_c_", "kOk", "kuk", "kSk", "kS", "kS", "kS", "kS", "kSS"]
ACOLYTE_F = dict(
    name="acolyte_f", pal="cast", arch="robe",
    roles=dict(C="L", Q="l", T="o", F="b"),
    head=dict(
        down=[
            "......kkkk......",
            ".....kuuurk.....",
            ".....kOOOOk.....",
            "...kkuuuuuukk...",
            "..kuuuuuuuuurk..",
            "..kuuuuuuuuurk..",
            "..kuuSSuuSSurk..",
            "..kuSkSSSSkSrk..",
            "..rSSkSSSSkSSr..",
            "...rSSSSSSSSr...",
            "....rssSSssr....",
        ],
        up=[
            "......kkkk......",
            ".....kuuurk.....",
            ".....kOOOOk.....",
            "...kkuuuuuukk...",
            "..kuuuuuuuuurk..",
            "..kuuuuuuuuurk..",
            "..kuuuuuuuuurk..",
            "..kuuuuuuuuurk..",
            "..rsuuuuuuuusr..",
            "...rsuuuuuusr...",
            "....rsSSSSsr....",
        ],
        left=[
            "..........kkk...",
            ".........kuurk..",
            "......kkkkOOrk..",
            "....kkuuuukkk...",
            "...kuuuuuuuuk...",
            "..kuuuuuuuuurk..",
            "..kuSuuuuuuurk..",
            "..kSSSSSuruurk..",
            "..kSkSSSrruuk...",
            "..kSkSSSSuuk....",
            "...rsSSSsrk.....",
        ],
    ),
    over=dict(
        down={"all": [pole(0, 3, _LAMP), ("b2", ["___LL___________", "___LL___________",
                                                 "___oo___________"]),
                      ("b8", ["___oooooooooo___"])],
              "stand": [("b5", ["..kLLCCCCCQSSk..", "..kkCCCCCCCQkk.."])],
              "walk0": [("b5", ["..kLLCCCCCQkk...", "..kkCCCCCCCQk..."])],
              "walk1": [("b5", ["..kLLCCCCCQSSk..", "..kkCCCCCCCQkk.."])]},
        up={"all": [pole(13, 3, [c[::-1].rjust(3, "_") for c in _LAMP]),
                    ("b2", ["___________SL___", "___________LL___", "___________oo___"]),
                    ("b8", ["___oooooooooo___"])],
            "stand": [("b5", ["..kSSCCCCCQLLk..", "..kkCCCCCCCQkk.."])],
            "walk0": [("b5", ["..kSSCCCCCQLLk..", "..kkCCCCCCCQkk.."])],
            "walk1": [("b5", ["...kkCCCCCQLLk..", "...kCCCCCCCQkk.."])]},
        left={"all": [pole(0, 4, ["_c", "kO", "ku", "kS"]), ("b8", ["____ooooooo_____"])]},
    ),
)


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

WALKERS = [MOM, PRIESTESS, YOUTH_M, YOUTH_F, MAN, WOMAN, ELDER_M, ELDER_F, KID_M, KID_F,
           FISHER, SAILOR, DIVER, HEALER, MERCHANT, HARVESTER, GOATHERD,
           SHEPHERD, HOPLITE, AUGUR, ACOLYTE_M, ACOLYTE_F]
BY_NAME = {w["name"]: w for w in WALKERS}


def sheet_preview(sheets, k=4, cols=2):
    """Every sheet at k times on a grass checker, in `cols` columns, each
    column headed by vanilla Birch for scale and each walker labelled with
    its sheet name and palette."""
    items = [(name, BY_NAME[name]["pal"], to_rgba(arr, PALETTES[BY_NAME[name]["pal"]][0]))
             for name, arr in sheets.items()]
    per = -(-len(items) // cols)
    columns = [[("prof_birch", "vanilla", ref_rgba())] + items[c * per:(c + 1) * per] for c in range(cols)]
    pad, lw, gap = 4, 30, 8
    cw = lw + W * 9 + pad * 8
    rows = max(len(c) for c in columns)
    out = Image.new("RGBA", (cols * cw + (cols - 1) * gap, (H + pad) * rows - pad), (232, 224, 200, 255))
    for c, column in enumerate(columns):
        x0 = c * (cw + gap)
        for i, (_, _, im) in enumerate(column):
            for f in range(9):
                tile = checker_bg(W, H)
                tile.alpha_composite(im.crop((f * W, 0, (f + 1) * W, H)))
                out.alpha_composite(tile, (x0 + lw + f * (W + pad), i * (H + pad)))
    big = upscale(out, k)
    d = ImageDraw.Draw(big)
    try:
        font = ImageFont.load_default(size=18)
    except TypeError:  # Pillow < 10.1
        font = ImageFont.load_default()
    for c, column in enumerate(columns):
        for i, (name, pal, _) in enumerate(column):
            x, y = c * (cw + gap) * k + 4, i * (H + pad) * k + 44
            d.text((x, y), name, fill=(32, 24, 24, 255), font=font)
            d.text((x, y + 22), pal, fill=(112, 96, 80, 255), font=font)
    return big


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    grids = args[args.index("--grids") + 1] if "--grids" in args else None
    write = "--write" in args
    only = [a for a in args if a in BY_NAME]
    sheets = {}
    for spec in WALKERS:
        if only and spec["name"] not in only:
            continue
        sheets[spec["name"]] = build_sheet(spec)
    if write:
        os.makedirs(OUT_DIR, exist_ok=True)
        for name, arr in sheets.items():
            save_indexed(arr, PALETTES[BY_NAME[name]["pal"]][0], os.path.join(OUT_DIR, name + ".png"))
        FOLK_PAL.write_jasc(FOLK_PAL_PATH)
    if pv:
        os.makedirs(pv, exist_ok=True)
        sheet_preview(sheets).save(os.path.join(pv, "sprites_folk_sheets.png"))
    if grids:
        os.makedirs(grids, exist_ok=True)
        for name, arr in sheets.items():
            pal = PALETTES[BY_NAME[name]["pal"]][0]
            grid_preview(to_rgba(arr, pal), 8).save(os.path.join(grids, name + "_grid.png"))


if __name__ == "__main__":
    main()
