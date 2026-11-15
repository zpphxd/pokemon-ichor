"""Overworld walkers for Phase 2's first batch: the voyage and Aegina.

Usage:
    python3 tools/ichor/art/sprites_phase2_walkers.py [NAME ...] [--write] [--preview DIR] [--grids DIR]

--write    writes graphics/object_events/pics/people/ichor/<name>.png (144x32,
           4bpp indexed) for every walker here and, when no NAME is given, the
           contact sheet design/phase2/img/sprites_walkers.png
--preview  writes DIR/sprites_walkers.png: every frame at 4x, the slice walker
           each one was edited from in the row above it
--grids    writes DIR/<name>_grid.png, 8x pixel grids for editing

No new palettes. The townsfolk here use the slice's folk palette
(OBJ_EVENT_PAL_TAG_ICHOR_FOLK) and Kleon's poses the cast palette
(OBJ_EVENT_PAL_TAG_ICHOR_CAST), so a map that shows them needs no OBJ palette
slot the slice's walkers didn't already take.

* pilgrim, pronomos, endeis, pheidon, aiakides: built like sprites_folk.py's
  walkers, from its body archetypes, with their own heads and overlays.
* kleon_seasick, kleon_tablet: Kleon's pose sheets. Every frame is drawn
  whole here (the poses don't fit an archetype). The facing picks the pose's
  direction and walking in place plays the two walk frames as a loop; see
  design/phase2/SPRITES.md for how a script shows them.

The frame layout, the step bob and feet on row 30 match sprites_npc.py.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import to_rgba, upscale, grid_preview, save_indexed  # noqa: E402
from sprites_npc import CAST_PAL, CAST_LEGEND, checker_bg  # noqa: E402
import sprites_npc  # noqa: E402
import sprites_folk as F  # noqa: E402
from sprites_folk import pole, W, H, OUT_DIR, PALETTES  # noqa: E402
from sprites_lib import ROOT  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

SHEET = os.path.join(ROOT, "design/phase2/img/sprites_walkers.png")

# --------------------------------------------------------------------------
# Pilgrim (female; Euthymia on the Aphaia Road). The initiate's body, a white
# chiton to mid-calf with a saffron cord, under a dark hooded cloak; a staff
# in her right hand and a covered dish of Hecate's supper in her left.
# An initiate walker can reuse PILGRIM_BODY's chiton without the cloak.
# --------------------------------------------------------------------------

_PILGRIM_STAFF = ["_k", "ku", "kb"] + ["ku"] * 17 + ["kb"]
PILGRIM = dict(
    name="pilgrim", pal="folk", arch="midi",
    roles=dict(C="L", Q="l", T="O", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....knnnnnnk....",
            "...knBBnnnnnk...",
            "..knBnnnnnnnnk..",
            "..kBnkbbbbknnk..",
            "..kBbbSbbSbbnk..",
            "..kBSSSSSSSSnk..",
            "..kBSkSSSSkSnk..",
            "..knSkSSSSkSnk..",
            "..knsSSSSSSsnk..",
            "..knnksSSsknnk..",
        ],
        up=[
            ".....kkkkkk.....",
            "....knnnnnnk....",
            "...knBBnnnnnk...",
            "..knBnnnnnnnnk..",
            "..kBnnnnnnnnnk..",
            "..kBnnnnnnnnnk..",
            "..kBnnnnknnnnk..",
            "..kBnnnnknnnnk..",
            "..knnnnnknnnnk..",
            "..knnnnnnnnnnk..",
            "..knnnnnnnnnnk..",
        ],
        left=[
            "......kkkkk.....",
            "....kknnnnnk....",
            "...knBBnnnnnk...",
            "..knBnnnnnnnnk..",
            "..kbbbbknnnnnk..",
            "..kbSbbbknnnnk..",
            "..kSSSSSknnnnk..",
            "..kSkSSSknnnnk..",
            "..kSkSSSSknnnk..",
            "..ksSSSSknnnnk..",
            "...kssssknnnk...",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["..knnnLSSLnnnk..",
                              "..kBnnLLLLlnnk..",
                              "..kBnkLLLLlknk..",
                              "..kBnkLLLLlknk..",
                              "..kBnkOOOOOknk..",
                              "..kBnkLLLLlknk..",
                              "..kBnkLLLLlknk..",
                              "...knkLLLLlkk..."]),
                      # the covered dish, held at her waist: a linen cloth
                      # knotted with saffron over a terracotta bowl
                      ("b2", ["__________kOk___",
                              "_________kLLlk__",
                              "________kLLLllk_",
                              "________SkuuukS_",
                              "_________kkkkk__"]),
                      pole(0, 0, _PILGRIM_STAFF), ("b5", ["__S_____________"])]},
        up={"all": [("b0", ["..knnnnnnnnnnk..",
                            "..kBnnnnnnnnnk..",
                            "..kBnnnnnnnnnk..",
                            "..kBnnnnnnnnnk..",
                            "..kBnnnnnnnnnk..",
                            "..kBnnnnnnnnnk..",
                            "..kBnnnnnnnnkk..",
                            "...klLLLLLLlk..."]),
                    pole(14, 0, [c[::-1] for c in _PILGRIM_STAFF]), ("b5", ["_____________S__"])]},
        left={"all": [("b0", [".....kSSknnk....",
                              "....kLLLknnnk...",
                              "....kLLLknnnk...",
                              "....kLLLknnnk...",
                              "....kOOOknnnk...",
                              "....kLLLknnnk...",
                              "....kLLLknnnk...",
                              "....kLLLlknnk..."]),
                      ("b1", ["__kOk___________",
                              "_kLLlk__________",
                              "kLLLllk_________",
                              "kkuuukS_________",
                              "_kkkkk__________"]),
                      pole(12, 0, ["kk", "uk", "bk"] + ["uk"] * 3)]},
    ),
)

# --------------------------------------------------------------------------
# Pronomos, the Euploia's piper: the slice's sailor, with his curls bound by
# the aulete's leather strap (the phorbeia) and the double pipes at his lips.
# His sash is terracotta, so he stands out among the rowers. His hands stay
# on the pipes when he walks.
# --------------------------------------------------------------------------

PRONOMOS = dict(
    name="pronomos", pal="folk", arch="tunic",
    roles=dict(C="l", Q="y", T="u", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbkbbkbk....",
            "...kbbbkbbbbk...",
            "..kbkbbbbbkbbk..",
            "..kbbbbbbbbbbk..",
            "..kbSbbSbbSbbk..",
            "..bsSkSSSSkSsb..",
            "..bsSkSSSSkSsb..",
            "..bbbbbkObbbbb..",
            "....bSSSOkSb....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbkbbkbk....",
            "...kbbbkbbbbk...",
            "..kbkbbbbbkbbk..",
            "..kbbbkbbbbbbk..",
            "..kbbbbbbkbbbk..",
            "..bsbbbbbbbbsb..",
            "..bbbbbbbbbbbb..",
            "..bbbbbbbbbbbb..",
            "....bbSSSSbb....",
        ],
        left=[
            "......kkkkk.....",
            "....kkbkbbbk....",
            "...kbbbbkbbbk...",
            "..kbkbbbbbbkbk..",
            "..kbbbbbbbbbbk..",
            "..kbSbSbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..bbbbbbbbbbk...",
            "...bbbbbbbbk....",
        ],
    ),
    over=dict(
        # the pipes slant from his lips across to his left side, a hand high
        # on them and a hand low
        down={"all": [("b0", ["...kSSSSSOkSk...",
                              "..kSsssskOOsSk..",
                              "..kSkSSSkkOOkk..",
                              "..kSsSSsSkSSOk..",
                              "..kSsTTTTkSSOOk.",
                              "..kSSCCCCCkkkk..",
                              "..kkCCCCCCCQkk.."])]},
        up={"all": [("b0", ["...kSSSSSSSsk...", "..kSSSSsSSSSsk..", "..kSSsSsSSsSsk..",
                            "..kSsSSsSSsSsk..", "..kssTTTTTTssk..", "..kkCCCCCCCQkk..",
                            "..kkCCCCCCCQkk.."])]},
        left={"all": [("b0", [".....kSSssk.....", "....ksSSsssk....", "....ksSSsssk....",
                              "....ksSSsssk....", "....kTTTTTTk....", "....kCCCCCQk...."]),
                      (8, ["..Obbbbbbbbbk...",
                           "..Ok____________",
                           "__Ok____________",
                           "_kSSk___________",
                           "__kOSk__________",
                           "___kOk__________",
                           "____kk__________"])]},
    ),
)

# --------------------------------------------------------------------------
# Endeis, Aegina's innkeeper: dark hair streaked gray under a terracotta
# kerchief, an ochre peplos, a linen apron, and a wine jug in her right hand.
# Edited from the slice's island woman and Melitta's apron.
# --------------------------------------------------------------------------

_JUG = ["_kk_", "kuuk", "kkkk", "kuuk", "_kk_"]
ENDEIS = dict(
    name="endeis", pal="folk", arch="robe",
    roles=dict(C="o", Q="u", T="b", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kuuuuuuk....",
            "...kuuuuuuubk...",
            "..kuuuuuuuuubk..",
            "..kbbbbbbbbbbk..",
            "..kbyySbbSbbbk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "..kbsSSSSSSsbk..",
            "...kbssSSssbk...",
        ],
        up=[
            ".....kkkkkk.....",
            "....kuuuuuuk....",
            "...kuuuuuuubk...",
            "..kuuuuuuuuubk..",
            "..kbuuuuuuubbk..",
            "..kbbbkuukbbbk..",
            "..kbybbuubbbbk..",
            "..kbybbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "...kbbbbbbbbk...",
            "....kbSSSSbk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkuuuuuk....",
            "...kuuuuuuuuk...",
            "..kuuuuuuuuubk..",
            "..kbbbbbbbbubk..",
            "..kbSbbbbyybubk.",
            "..kSSSSSbsbbkuk.",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbbk..",
            "..kSSSSSsbbbbk..",
            "...kbsSssbbbk...",
        ],
    ),
    over=dict(
        down={"all": [("b5", ["_____LLLLLl_____", "_____LLLLLl_____",
                              "_____LLLLLl_____", "_____lLLLLl_____"]),
                      pole(0, "b4", _JUG), ("b4", ["__S_____________"])]},
        up={"all": [("b5", ["______Ll________"]), pole(12, "b4", _JUG), ("b4", ["_____________S__"])]},
        left={"all": [("b6", ["_____L__________", "____LL__________", "____Ll__________"]),
                      pole(3, "b4", _JUG), ("b4", ["______S_________"])]},
    ),
)

# --------------------------------------------------------------------------
# Pheidon, Aegina's moneyer: dark curls going gray at the temples, a short
# beard, an undyed exomis under a leather smith's apron, and the striking
# hammer in his right hand.
# --------------------------------------------------------------------------

_HAMMER = ["kkkkk", "kLyyk", "kkbkk", "_kbk_", "_kSk_"]
PHEIDON = dict(
    name="pheidon", pal="folk", arch="tunic",
    roles=dict(C="l", Q="y", T="b", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbkbbkbk....",
            "...kbbbbbbbbk...",
            "..kbkbbbbbbkbk..",
            "..kybbbbbbbbyk..",
            "..kySbbSSbbSyk..",
            "..kbSkSSSSkSbk..",
            "..kSSkSSSSkSSk..",
            "..kbSSsSSsSSbk..",
            "...kbbSSSSbbk...",
            "....kbbbbbbk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbkbbkbk....",
            "...kbbbbbbbbk...",
            "..kbkbbbbbbkbk..",
            "..kybbbkbbbbyk..",
            "..kybbbbbbbbyk..",
            "..kbbbbbbbbbbk..",
            "..ksbbbbbbbbsk..",
            "..ksbbbbbbbbsk..",
            "...kbbSSSSbbk...",
            "....kbSSSSbk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkbkbbbk....",
            "...kbbbbbbbbk...",
            "..kbbbbbbkbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbSbbbyybbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSbbbbbk...",
            "...kbbbbbbbk....",
            "....kbbbbk......",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["______b__b______", "_____buuuub_____", "_____buuuub_____",
                              "_____buuuub_____", "_____bbbbbb_____", "_____buuuub_____",
                              "_____kbuubk_____"]),
                      pole(0, "b1", _HAMMER)]},
        up={"all": [("b0", ["______b__b______"]), ("b4", ["____bbbbbbb_____"]),
                    pole(11, "b1", [c[::-1] for c in _HAMMER])]},
        left={"all": [("b0", ["______bb________"]),
                      ("b1", ["____kuu_________", "____kuu_________", "____kuu_________",
                              "____kbb_________", "____kuu_________", "____kuuk________"]),
                      pole(3, "b1", _HAMMER)]},
    ),
)

# --------------------------------------------------------------------------
# Aiakides, an old soldier of Aegina: close-cropped white hair, a short white
# beard and stern brows, a white chiton with a black belt (the one he gives
# away), a faded terracotta soldier's cloak, and a stick.
# --------------------------------------------------------------------------

_STICK = ["_k", "kb"] + ["ku"] * 17 + ["kb"]
AIAKIDES = dict(
    name="aiakides", pal="folk", arch="tunic",
    roles=dict(C="L", Q="l", T="k", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kLLLLLLk....",
            "...kLLyLLLLyk...",
            "..kLLLLLLLLLyk..",
            "..kySSSSSSSSyk..",
            "..kySkkSSkkSyk..",
            "..kySkSSSSkSyk..",
            "..kLSkSSSSkSLk..",
            "..kLLsSSSSsLLk..",
            "...kLLLssLLLk...",
            "....kLLLLLLk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kLLLLLLk....",
            "...kLLyLLLLyk...",
            "..kLLLLLLLLLyk..",
            "..kLLLLyLLLLyk..",
            "..kyLLLLLLLLyk..",
            "..kyLLLLLLLLyk..",
            "..ksyLLLLLLysk..",
            "..ksyyLLLLyysk..",
            "...kyySSSSyyk...",
            "....kSSSSSSk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkLLLLLk....",
            "...kLLLLLyLLk...",
            "..kLLLLLLLLyLk..",
            "..kSSSSyLLLLyk..",
            "..kkkSSsLLLLyk..",
            "..kSSSSSsLLLyk..",
            "..kSkSSSsyLLyk..",
            "..kLkSSLLLyyk...",
            "..kLLLLLLyk.....",
            "...kLLLLyk......",
        ],
    ),
    over=dict(
        down={"all": [("b0", [".ku___________bk", ".kuu_________ubk", ".kub_________ubk",
                              ".kub_________bbk", ".kub_________bbk", ".kub_________bbk",
                              ".kbb_________bbk"]),
                      ("b0", ["_____ou_________"]),
                      pole(0, 1, _STICK), ("b5", ["__S_____________"])],
              "walk1": [("b5", ["..SSSCCCCCQSSk..", "..kkCCCCCCCQkk.."])]},
        up={"all": [("b0", ["..kuuuuSSuuubk..", ".kuuuuubuuuubbk.", ".kuuuuubuuuubbk.",
                            ".kuuuuubuuuubbk.", ".kuuuuubuuuubbk.", ".kuuuuubuuubbbk.",
                            ".kbuuubbuubbbbk.", "..kkbbbbbbbbkk.."]),
                    pole(14, 1, [c[::-1] for c in _STICK])]},
        left={"all": [("b0", ["_________kuk____", "_________kuuk___", "_________kuubk__",
                              "_________kuubk__", "_________kubbk__", "_________kubbk__",
                              "_________kbbk___"]),
                      pole(0, 1, _STICK), ("b4", ["__Ss____________"])]},
    ),
)

# --------------------------------------------------------------------------
# Kedalion, the smith of Emporion's Hephaisteion (batch 2): a short, broad man,
# bald on top with a black fringe and a great black beard, soot on his brow, a
# sooty gray exomis under a black leather apron, and his tongs. He once
# carried a blind giant to the sunrise on his shoulders.
# --------------------------------------------------------------------------

_TONGS_K = ["k_k", "kyk", "_y_", "_y_", "_k_"]
KEDALION = dict(
    name="kedalion", pal="folk", arch="tunic",
    roles=dict(C="y", Q="l", T="k", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kSSSSSSk....",
            "...kSSyySSSSk...",
            "..kSSSSySSSSSk..",
            "..kkSSSSSSSSkk..",
            "..kkkkSSSSkkkk..",
            "..kbSkSSSSkSbk..",
            "..kbSSSssSSSbk..",
            "..kkkkkkkkkkkk..",
            "..kkkbkkkkbkkk..",
            "...kkkkbbkkkk...",
        ],
        up=[
            ".....kkkkkk.....",
            "....kSSSSSSk....",
            "...kSSSSSSSSk...",
            "..kSSSSSSSSSSk..",
            "..kSSSSSSSSSsk..",
            "..kkSSSSSSSSkk..",
            "..kkkkkkkkkkkk..",
            "..kkkkbkkbkkkk..",
            "..kskkkkkkkksk..",
            "...kkkkkkkkkk...",
            "....kssSSssk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkSSSSSk....",
            "...kSyySSSSSk...",
            "..kSSSSSSSSSSk..",
            "..kSSSSSSSSSsk..",
            "..kkkSSSSSkkkk..",
            "..kSkSSSSskkkk..",
            "..kSSSSSSskkbk..",
            "..kkkkkkkkkkk...",
            "..kkbkkkbkkk....",
            "...kkkkkkk......",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["_____kbbbbk_____", "_____kbbbbk_____", "_____kbbbbk_____",
                              "_____kbbbbk_____", "_____kkkkkk_____", "_____kbbbbk_____",
                              "_____kkbbkk_____"]),
                      pole(0, "b1", _TONGS_K)]},
        up={"all": [("b0", ["______k__k______"]), ("b4", ["____kkkkkkk_____"]),
                    pole(13, "b1", [c[::-1] for c in _TONGS_K])]},
        left={"all": [("b0", ["______kk________"]),
                      ("b1", ["____kbb_________", "____kbb_________", "____kbb_________",
                              "____kkk_________", "____kbb_________", "____kbbk________"]),
                      pole(2, "b1", _TONGS_K)]},
    ),
)

FOLK_WALKERS = [PILGRIM, PRONOMOS, ENDEIS, PHEIDON, AIAKIDES, KEDALION]

# --------------------------------------------------------------------------
# Kleon's poses (cast palette). Each frame is whole: (y0, rows), the rows
# placed from y0 down. Facing picks the pose's direction (right is left
# mirrored); walking in place loops stand, walk A, stand, walk B.
# --------------------------------------------------------------------------

# Seasick (beat 10, the starboard rail). Facing down: doubled over a rail in
# front of him. Up: from behind, his arms out to the rail and his head hung
# between his shoulders. Left: bent over a rail at his left. The walk frames
# are the heave: he sags a pixel lower and gulps.
SEASICK = {
    "down": (11, [
        ".....kkkkkk.....",
        "....kbbbbbbk....",
        "...kbuubbbbbk...",
        "..kbubbbbbbbbk..",
        "..kbbbbbbbbbbk..",
        "..kbbbbbbbbbbk..",
        "..kbSbbSbbSbbk..",
        "..bgllllllllgb..",
        "..bglkkllkklgb..",
        "...bgllkkllgb...",
        "..kcrkLllLkrck..",
        ".kcSSLLLLLLSsrk.",
        ".kcoOLLLLLlSsrk.",
        ".kcSskSSSSkSsrk.",
        ".kcrkSSbbSSkrrk.",
        ".kcrkLLLLLlkrrk.",
        ".kcrklLLLLlkrrk.",
        "..kkkSskkSskkk..",
        "....kSskkSsk....",
        "....kbbkkbbk....",
    ]),
    "down_heave": (12, [
        ".....kkkkkk.....",
        "....kbbbbbbk....",
        "...kbuubbbbbk...",
        "..kbubbbbbbbbk..",
        "..kbbbbbbbbbbk..",
        "..kbbbbbbbbbbk..",
        "..kbSbbSbbSbbk..",
        "..bgllllllllgb..",
        "..bglkkllkklgb..",
        "...bgkSSSSkgb...",
        "..kcrkSssSkrck..",
        ".kcSSkSskLLSsrk.",
        ".kcoOSskLLlSsrk.",
        ".kcSskLLSSkSsrk.",
        ".kcrkbbbSSkkrrk.",
        ".kcrkLLLLLlkrrk.",
        ".kcrklLLLLlkrrk.",
        "..kkkSskkSskkk..",
        "....kSskkSsk....",
        "....kbbkkbbk....",
    ]),
    "up": (15, [
        "....kk....kk....",
        "...kSSk..kSSk...",
        "...kSskkkkSsk...",
        "..kSskbbbbkSsk..",
        ".kSskbuubbbkSsk.",
        ".kSkcbbbbbbckSk.",
        ".kkcccbbbbcccrk.",
        ".kccccrkkrccrrk.",
        ".kccccrccrccrrk.",
        ".kcccccrcccrrrk.",
        ".kcccccrccrrrrk.",
        ".kccccrcccrrrrk.",
        ".krcccrccrrrrrk.",
        "..kkrrrrrrrrkk..",
        "....kSskkSsk....",
        "....kbbkkbbk....",
    ]),
    "up_heave": (16, [
        "....kk....kk....",
        "...kSSk..kSSk...",
        "...kSskkkkSsk...",
        "..kSskbbbbkSsk..",
        ".kSskbbbbbbkSsk.",
        ".kSkccbbbbcckSk.",
        ".kkcccckkcccrrk.",
        ".kccccrccrccrrk.",
        ".kcccccrcccrrrk.",
        ".kcccccrccrrrrk.",
        ".kccccrcccrrrrk.",
        ".krcccrccrrrrrk.",
        "..kkrrrrrrrrkk..",
        "....kSskkSsk....",
        "....kbbkkbbk....",
    ]),
    "left": (15, [
        "....kkkkk.......",
        "...kbbbbbkkkk...",
        "..kbubbbbbkccck.",
        ".kbubbbbbbbkccrk",
        ".kbbbbbbbLLkcrrk",
        ".kbbbsbbLLLLkrrk",
        ".kglkbbkLLLLkrrk",
        "..kllkkSsLLlkrk.",
        "..kSSk.kSsLLkrk.",
        "..kSSk..kbobbk..",
        "...kk...kLLLlk..",
        "........kLLLlk..",
        "........kkSskk..",
        ".........kSsk...",
        ".........kSsk...",
        "........kbbbk...",
    ]),
    "left_heave": (16, [
        "....kkkkk.......",
        "...kbbbbbkkkk...",
        "..kbubbbbbkccck.",
        ".kbubbbbbbbkccrk",
        ".kbbbbbbbLLkcrrk",
        ".kbbbsbbLLLLkrrk",
        ".kglkkbkLLLLkrrk",
        "..kgkkSsLLLlkrk.",
        "..kSSk.kSLLlkrk.",
        "..kSSk..kbobbk..",
        "...kk...kLLLlk..",
        "........kkSskk..",
        ".........kSsk...",
        ".........kSsk...",
        "........kbbbk...",
    ]),
}

# Reading (beat 10's night leg: his mother's letter). A small wax diptych
# open in both hands, his head bowed over it. He can walk while he reads: the
# legs step and the tablet stays put.
_TAB_HEAD_DOWN = [
    ".....kkkkkk.....",
    "....kbbbbbbk....",
    "...kbuubbbbbk...",
    "..kbubbbbbbbbk..",
    "..kbbbbbbbbbbk..",
    "..kbSbbSbbSbbk..",
    "..bsSSSSSSSSsb..",
    "..bsSkkSSkkSsb..",
    "...bSSSSSSSSb...",
    "....bssSSssb....",
]
_TAB_BODY_DOWN = [
    "..kcrkLSSLkrck..",
    ".kcSkkkkkkkkSrk.",
    ".kcoSubbubbuSrk.",
    ".kcSSulbublSSrk.",
    ".kcrkkkkkkkkrrk.",
    ".kcrkLLLLLlkrrk.",
    ".kcrklLLLLlkrrk.",
    "..kkklLLLLlkkk..",
]
_TAB_LEGS_DOWN = (["....kSskkSsk....", "....kbbkkbbk...."],
                  ["....kSskkbbk....", "....kbbk........"],
                  ["....kbbkkSsk....", "........kbbk...."])
_TAB_HEAD_UP = sprites_npc.KLEON["up"]["top"]
_TAB_BODY_UP = [
    "..kccrkSSkrcck..",
    ".kccccrccrccrrk.",
    ".kcccccrcccrrrk.",
    ".kcccccrccrrrrk.",
    ".kccccrcccrrrrk.",
    ".kccccrcccrrrrk.",
    ".krcccrccrrrrrk.",
    "..kkrrrrrrrrkk..",
]
_TAB_LEGS_UP = _TAB_LEGS_DOWN
_TAB_HEAD_LEFT = [
    "......kkkkk.....",
    "....kkbbbbbk....",
    "...kbuubbbbbk...",
    "..kbubbbbbbbbk..",
    "..kbbbbbbbbbbk..",
    "..kbSbSbbbbbbk..",
    "..kSSSSSbsbbbk..",
    "..kSSSSSssbbbk..",
    "..kkkSSSSbbbk...",
    "...bsSSSsbbk....",
]
_TAB_BODY_LEFT = [
    "..kk.kSSkcck....",
    ".kubkLLLLkccrk..",
    ".kbbSSoOlkccrk..",
    ".kubkSsLlkcrrk..",
    "..kkkbbbbkcrrrk.",
    "....kLLLlkcrrrk.",
    "....kLLLlkrrrrk.",
    ".....kSskkrrrk..",
]
_TAB_LEGS_LEFT = ([".....kSsk.kkk...", "....kbbbk......."],
                  ["...kSskkSskrrk..", "..kSsk..kSsk....", "..kbbk...kbbk..."],
                  ["....kSskrrrrk...", "....kSskkkk.....", "...kbbbk........"])


def _tablet_pose():
    out = {}
    for d, head, body, legs in (("down", _TAB_HEAD_DOWN, _TAB_BODY_DOWN, _TAB_LEGS_DOWN),
                                ("up", _TAB_HEAD_UP, _TAB_BODY_UP, _TAB_LEGS_UP),
                                ("left", _TAB_HEAD_LEFT, _TAB_BODY_LEFT, _TAB_LEGS_LEFT)):
        for i, pose in enumerate(("stand", "walk0", "walk1")):
            rows = list(head) + list(body)
            leg = legs[i]
            if len(leg) == 3:          # the side stride replaces the last body row too
                rows = rows[:-1] + leg
            else:
                rows = rows + leg
            y0 = F.FEET_ROW + 1 - len(rows) + (0 if pose == "stand" else 1)
            out[(d, pose)] = (y0, rows)
    return out


def _seasick_pose():
    out = {}
    for d in ("down", "up", "left"):
        out[(d, "stand")] = SEASICK[d]
        out[(d, "walk0")] = SEASICK[d + "_heave"]
        out[(d, "walk1")] = SEASICK[d + "_heave"]
    return out


KLEON_POSES = {
    "kleon_seasick": _seasick_pose,
    "kleon_tablet": _tablet_pose,
}

ORDER = [("down", "stand"), ("up", "stand"), ("left", "stand"),
         ("down", "walk0"), ("down", "walk1"), ("up", "walk0"), ("up", "walk1"),
         ("left", "walk0"), ("left", "walk1")]


def build_pose_sheet(name):
    frames = KLEON_POSES[name]()
    out = []
    for key in ORDER:
        y0, rows = frames[key]
        frame = np.zeros((H, W), np.int32)
        sprites_npc._place(frame, rows, y0, CAST_LEGEND, CAST_PAL, f"{name} {key}")
        out.append(frame)
    return np.hstack(out)


def build_all(only=()):
    sheets = {}
    for spec in FOLK_WALKERS:
        if not only or spec["name"] in only:
            sheets[spec["name"]] = (F.build_sheet(spec), "folk")
    for name in KLEON_POSES:
        if not only or name in only:
            sheets[name] = (build_pose_sheet(name), "cast")
    return sheets


# --------------------------------------------------------------------------
# Previews
# --------------------------------------------------------------------------

# The slice walker each new one was made from, shown above it for comparison.
BASES = {
    "pilgrim": ("priestess", "folk"),
    "pronomos": ("sailor", "folk"),
    "endeis": ("woman", "folk"),
    "pheidon": ("merchant", "folk"),
    "aiakides": ("elder_m", "folk"),
    "kedalion": ("pheidon", "folk"),
    "kleon_seasick": ("kleon", "cast"),
    "kleon_tablet": ("kleon", "cast"),
}


def _base_sheet(name, pal):
    path = os.path.join(OUT_DIR, name + ".png")
    im = Image.open(path)
    return np.array(im).astype(np.int32)


def sheet_preview(sheets, k=4):
    rows = []
    for name, (arr, pal) in sheets.items():
        base, bpal = BASES[name]
        rows.append((base + " (slice)", bpal, _base_sheet(base, bpal)))
        rows.append((name, pal, arr))
    pad, lw = 4, 44
    cw = lw + W * 9 + pad * 8
    out = Image.new("RGBA", (cw, (H + pad) * len(rows) - pad), (232, 224, 200, 255))
    for i, (_, pal, arr) in enumerate(rows):
        im = to_rgba(arr, PALETTES[pal][0])
        for f in range(9):
            tile = checker_bg(W, H)
            tile.alpha_composite(im.crop((f * W, 0, (f + 1) * W, H)))
            out.alpha_composite(tile, (lw + f * (W + pad), i * (H + pad)))
    big = upscale(out, k)
    d = ImageDraw.Draw(big)
    try:
        font = ImageFont.load_default(size=16)
    except TypeError:  # Pillow < 10.1
        font = ImageFont.load_default()
    for i, (label, pal, _) in enumerate(rows):
        y = i * (H + pad) * k + 40
        d.text((4, y), label, fill=(32, 24, 24, 255), font=font)
        d.text((4, y + 20), pal, fill=(112, 96, 80, 255), font=font)
    return big


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    grids = args[args.index("--grids") + 1] if "--grids" in args else None
    write = "--write" in args
    names = [w["name"] for w in FOLK_WALKERS] + list(KLEON_POSES)
    only = [a for a in args if a in names]
    sheets = build_all(only)
    if write:
        for name, (arr, pal) in sheets.items():
            save_indexed(arr, PALETTES[pal][0], os.path.join(OUT_DIR, name + ".png"))
        if not only:
            os.makedirs(os.path.dirname(SHEET), exist_ok=True)
            sheet_preview(sheets).save(SHEET)
    if pv:
        os.makedirs(pv, exist_ok=True)
        sheet_preview(sheets).save(os.path.join(pv, "sprites_walkers.png"))
    if grids:
        os.makedirs(grids, exist_ok=True)
        for name, (arr, pal) in sheets.items():
            grid_preview(to_rgba(arr, PALETTES[pal][0]), 8).save(os.path.join(grids, name + "_grid.png"))


if __name__ == "__main__":
    main()
