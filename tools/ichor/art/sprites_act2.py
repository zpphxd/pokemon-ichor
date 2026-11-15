"""Overworld walkers and field objects for Act II, batch 1 (beats 26-34).

Usage:
    python3 tools/ichor/art/sprites_act2.py [NAME ...] [--write] [--preview DIR] [--grids DIR]

--write    writes graphics/object_events/pics/people/ichor/<name>.png (walkers),
           graphics/object_events/pics/misc/ichor/<name>.png (objects) and the
           new wine palette graphics/object_events/palettes/ichor_wine.pal
--preview  writes DIR/sprites_act2_sheets.png (every frame at 4x, labelled)
--grids    writes DIR/<name>_grid.png, 8x pixel grids for editing

The house style is the slice's (sprites_folk.py, sprites_npc.py): 16x32 frames,
nine to a sheet, feet on row 30, a 1 px step bob, right = left mirrored. Most
walkers are built the sprites_folk way (a body archetype in role letters, a
head per direction, overlays per pose). The seated and kneeling poses are drawn
frame by frame (POSES below).

Three palette families, so a map shows at most three Ichor OBJ palette slots:

* folk (OBJ_EVENT_PAL_TAG_ICHOR_FOLK): the mountain and the road. The Maenad,
  the Satyr, Silenos, Manto, the Kronists, the herald, the crows.
* cast (OBJ_EVENT_PAL_TAG_ICHOR_CAST): the Dionysia's players (the chorus
  leader, the bee-woman, the three Fates, the gold-masked king, the Unwoven)
  and Kleon's and Alethea's poses.
* wine (new, OBJ_EVENT_PAL_TAG_ICHOR_WINE): Thyrsa. The folk palette with its
  three blues turned to grape purples and its terracotta to wine red, index for
  index, so any folk sheet shown under the wine tag is a Thyrsa palette swap.
  The Vintner, the Actor, Thespis (both masks), the god's wooden image and the
  floating mask.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, Palette, save_indexed, to_rgba, upscale, grid_preview  # noqa: E402
from sprites_npc import checker_bg, ref_rgba  # noqa: E402
from sprites_folk import (FOLK_COLORS, ARCHETYPES, PALETTES, pole, _with, build_frame,  # noqa: E402
                          build_sheet as folk_build_sheet)
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

W, H = 16, 32
FEET_ROW = 30
PEOPLE_DIR = os.path.join(ROOT, "graphics/object_events/pics/people/ichor")
MISC_DIR = os.path.join(ROOT, "graphics/object_events/pics/misc/ichor")
WINE_PAL_PATH = os.path.join(ROOT, "graphics/object_events/palettes/ichor_wine.pal")

# --------------------------------------------------------------------------
# The wine palette: the folk palette, index for index, with the blues turned
# to grape and the terracotta to wine. Letters keep their folk roles.
# --------------------------------------------------------------------------

_WINE_SWAP = {
    "u": ("wine", (160, 40, 72)),       # wine red: the Actor's robe, Thyrsa's scarves
    "n": ("grape_d", (56, 32, 80)),     # grape shadow, stained feet, eye holes
    "B": ("grape", (112, 56, 136)),     # grape purple: Thespis's robe, stained shins
    "a": ("lilac", (184, 136, 208)),    # bloom on the grapes, mask ribbons
}
WINE_COLORS = [(ch, *_WINE_SWAP[ch]) if ch in _WINE_SWAP else (ch, name, rgb)
               for ch, name, rgb in FOLK_COLORS]
WINE_PAL = Palette([(name, rgb) for _, name, rgb in WINE_COLORS])
WINE_LEGEND = {ch: name for ch, name, _ in WINE_COLORS}
PALETTES["wine"] = (WINE_PAL, WINE_LEGEND)

_BLANK3 = ["................"] * 3


def _flip(cells):
    """Mirror a list of prop cells (for the other hand in the back view)."""
    width = max(len(c) for c in cells)
    return [c.ljust(width, "_")[::-1] for c in cells]


# --------------------------------------------------------------------------
# Extra body archetypes (role letters, as in sprites_folk)
# --------------------------------------------------------------------------

_HANDS_W0 = {5: "..kSSCCCCCQkk...", 6: "..kkCCCCCCCQk..."}
_HANDS_W1 = {5: "...kkCCCCCQSSk..", 6: "...kCCCCCCCQkk.."}
_ARM_BACK = {2: "....kCCSsCQk....", 3: "....kCCSsCQk....",
             4: "....kTTSsTTk....", 5: "....kCCSSCQk...."}
_ARM_FWD = {2: "....kSsCCCQk....", 3: "....kSsCCCQk....",
            4: "....kSsTTTTk....", 5: "....kSSCCCQk...."}

# A floor-length robe one row longer, for tall people (Thespis, the chorus
# leader, the king): the hem falls straight, then flares.
_TALL_DOWN = [
    "...kCCSSSSCQk...",
    "..kCCCCCCCCCQk..",
    "..kSSCCCCCQSsk..",
    "..kSsCCCCCQSsk..",
    "..kSsTTTTTTSsk..",
    "..kSSCCCCCQSSk..",
    "..kkCCCCCCCQkk..",
    "...kCCCCCCCQk...",
    "...kCCCCCCCQk...",
    "..kCCCCCCCCCQk..",
    "..kkkFFkkFFkkk..",
]
_TALL_UP = _with(_TALL_DOWN, {0: "...kCCCCCCCQk..."})
_TALL_LEFT = [
    ".....kSSCQk.....",
    "....kCCCCCQk....",
    "....kCSsCCQk....",
    "....kCSsCCQk....",
    "....kTSsTTTk....",
    "....kCSSCCQk....",
    "....kCCCCCQk....",
    "...kCCCCCCQk....",
    "...kCCCCCCQk....",
    "...kCCCCCCCQk...",
    "...kFFkkkkkkk...",
]


def _front_tall(stand):
    return dict(stand=stand,
                walk0=_with(stand, {**_HANDS_W0, 10: "..kkkFFkkkkkkk.."}),
                walk1=_with(stand, {**_HANDS_W1, 10: "..kkkkkkkFFkkk.."}))


ARCHETYPES["robe_tall"] = dict(
    down=_front_tall(_TALL_DOWN),
    up=_front_tall(_TALL_UP),
    left=dict(stand=_TALL_LEFT,
              walk0=_with(_TALL_LEFT, {**_ARM_BACK, 8: "..kCCCCCCCQk....",
                                       9: "..kCCCCCCCCQk...", 10: "..kFFkkkkkkFFk.."}),
              walk1=_with(_TALL_LEFT, {**_ARM_FWD, 10: "....kFFkkkkkk..."})),
)

# Tragic boots (kothornoi): the tall robe over thick soles, a row taller still.
_SOLE_DOWN = _TALL_DOWN + ["...kbbkkkbbk...."]
_SOLE_DOWN[10] = "..kkkFFkkFFkkk.."
_SOLE_DOWN[11] = "...kbbbkkbbbk..."
_SOLE_UP = _with(_SOLE_DOWN, {0: "...kCCCCCCCQk..."})
_SOLE_LEFT = _TALL_LEFT + ["...kbbbk........"]
_SOLE_LEFT[10] = "...kFFFkkkkkk..."


def _front_sole(stand):
    return dict(stand=stand,
                walk0=_with(stand, {**_HANDS_W0, 10: "..kkkFFkkkkkkk..", 11: "...kbbbk........"}),
                walk1=_with(stand, {**_HANDS_W1, 10: "..kkkkkkkFFkkk..", 11: "........kbbbk..."}))


ARCHETYPES["robe_soles"] = dict(
    down=_front_sole(_SOLE_DOWN),
    up=_front_sole(_SOLE_UP),
    left=dict(stand=_SOLE_LEFT,
              walk0=_with(_SOLE_LEFT, {**_ARM_BACK, 8: "..kCCCCCCCQk....", 9: "..kCCCCCCCCQk...",
                                       10: "..kFFkkkkkFFk...", 11: ".kbbbk...kbbbk.."}),
              walk1=_with(_SOLE_LEFT, {**_ARM_FWD, 10: "....kFFkkkkkk...",
                                       11: "....kbbbk......."})),
)

# A tiny old woman's robe: eight rows, narrow shoulders (Manto).
_SMALL_DOWN = [
    "....kCSSSSCk....",
    "...kCCCCCCCQk...",
    "...kSCCCCCQSk...",
    "...kSCCCCCQSk...",
    "...kSTTTTTQSk...",
    "...kkCCCCCQkk...",
    "...kCCCCCCCQk...",
    "...kkFFkkFFkk...",
]
_SMALL_UP = _with(_SMALL_DOWN, {0: "....kCCCCCCk...."})
_SMALL_LEFT = [
    ".....kSCQk......",
    "....kCCCCQk.....",
    "....kCSsCQk.....",
    "....kCSsCQk.....",
    "....kTSsTTk.....",
    "....kCCCCQk.....",
    "...kCCCCCCQk....",
    "...kFFkkkkk.....",
]
ARCHETYPES["robe_small"] = dict(
    down=dict(stand=_SMALL_DOWN,
              walk0=_with(_SMALL_DOWN, {4: "...kSTTTTTQkk...", 5: "...kkCCCCCQk....",
                                        7: "...kkFFkkkkkk..."}),
              walk1=_with(_SMALL_DOWN, {4: "...kkTTTTTQSk...", 5: "....kCCCCCQkk...",
                                        7: "...kkkkkkFFkk..."})),
    up=dict(stand=_SMALL_UP,
            walk0=_with(_SMALL_UP, {4: "...kSTTTTTQkk...", 5: "...kkCCCCCQk....",
                                    7: "...kkFFkkkkkk..."}),
            walk1=_with(_SMALL_UP, {4: "...kkTTTTTQSk...", 5: "....kCCCCCQkk...",
                                    7: "...kkkkkkFFkk..."})),
    left=dict(stand=_SMALL_LEFT,
              walk0=_with(_SMALL_LEFT, {2: "....kCCSsk......", 3: "....kCCSsk......",
                                        7: "..kFFkkkkFFk...."}),
              walk1=_with(_SMALL_LEFT, {2: "....kSsCQk......", 3: "....kSsCQk......",
                                        7: "....kFFkkkk....."})),
)

# A round old man (Silenos): a belly that bulges past his arms, short legs.
_ROUND_DOWN = [
    "...kCCSSSSCQk...",
    "..kCCCCCCCCCQk..",
    ".kSkCCCCCCCCQsk.",
    ".kSkCCCCCCCCCQk.",
    ".kSkTTTTTTTTTQk.",
    ".kSSkCCCCCCCQkk.",
    "..kkkCCCCCCQkk..",
    "....kkXYkkXYk...",
    "....kXYkkXYk....",
    "....kFFkkFFk....",
]
_ROUND_UP = _with(_ROUND_DOWN, {0: "...kCCCCCCCQk...",
                                2: ".ksQCCCCCCCCkSk.", 3: ".kQCCCCCCCCCkSk.",
                                4: ".kQTTTTTTTTTkSk.", 5: ".kkQCCCCCCCkSSk."})
_ROUND_LEFT = [
    ".....kSSCQk.....",
    "....kCCCCCQk....",
    "...kCCSsCCCQk...",
    "...kCCSsCCCQk...",
    "...kTTSsTTTTQk..",
    "...kCCSSCCCQk...",
    "....kCCCCCQk....",
    ".....kXYkkk.....",
    ".....kXYk.......",
    "....kFFFk.......",
]
ARCHETYPES["round"] = dict(
    down=dict(stand=_ROUND_DOWN,
              walk0=_with(_ROUND_DOWN, {8: "....kXYkkFFk....", 9: "....kFFk........"}),
              walk1=_with(_ROUND_DOWN, {8: "....kFFkkXYk....", 9: "........kFFk...."})),
    up=dict(stand=_ROUND_UP,
            walk0=_with(_ROUND_UP, {8: "....kXYkkFFk....", 9: "....kFFk........"}),
            walk1=_with(_ROUND_UP, {8: "....kFFkkXYk....", 9: "........kFFk...."})),
    left=dict(stand=_ROUND_LEFT,
              walk0=_with(_ROUND_LEFT, {2: "...kCCCSsCCQk...", 3: "...kCCCSsCCQk...",
                                        5: "...kCCCSSCCQk...",
                                        7: "....kXYkkYYk....", 8: "...kXYk..kYYk...",
                                        9: "...kFFk...kFFk.."}),
              walk1=_with(_ROUND_LEFT, {2: "...kSsCCCCCQk...", 3: "...kSsCCCCCQk...",
                                        5: "...kSSCCCCCQk...",
                                        7: "....kYYkkXYk....", 8: "...kYYk..kXYk...",
                                        9: "...kFFk...kFFk.."})),
)

# A big man's tunic, a size too large (the Unwoven): broad shoulders and an
# extra row of leg.
_BIG_DOWN = [
    "..kCCCSSSSCQQk..",
    ".kCCCCCCCCCCCQk.",
    ".kSSCCCCCCCQSsk.",
    ".kSsCCCCCCCQSsk.",
    ".kSsTTTTTTTTSsk.",
    ".kSSCCCCCCCQSSk.",
    ".kkCCCCCCCCCQkk.",
    "...kkXYkkXYkk...",
    "....kXYkkXYk....",
    "....kXYkkXYk....",
    "...kFFFkkFFFk...",
]
_BIG_UP = _with(_BIG_DOWN, {0: "..kCCCCCCCCQQk.."})
_BIG_LEFT = [
    ".....kSSCCQk....",
    "....kCCCCCCQk...",
    "....kCSsCCCQk...",
    "....kCSsCCCQk...",
    "....kTSsTTTTk...",
    "....kCSSCCCQk...",
    "....kCCCCCCQk...",
    "....kkXYkkkk....",
    ".....kXYk.......",
    ".....kXYk.......",
    "....kFFFFk......",
]
ARCHETYPES["big"] = dict(
    down=dict(stand=_BIG_DOWN,
              walk0=_with(_BIG_DOWN, {5: ".kSSCCCCCCCQkk..", 6: ".kkCCCCCCCCCQk..",
                                      9: "....kXYkkFFFk...", 10: "...kFFFk........"}),
              walk1=_with(_BIG_DOWN, {5: "..kkCCCCCCCQSSk.", 6: "..kCCCCCCCCCQkk.",
                                      9: "...kFFFkkXYk....", 10: "........kFFFk..."})),
    up=dict(stand=_BIG_UP,
            walk0=_with(_BIG_UP, {5: ".kSSCCCCCCCQkk..", 6: ".kkCCCCCCCCCQk..",
                                  9: "....kXYkkFFFk...", 10: "...kFFFk........"}),
            walk1=_with(_BIG_UP, {5: "..kkCCCCCCCQSSk.", 6: "..kCCCCCCCCCQkk.",
                                  9: "...kFFFkkXYk....", 10: "........kFFFk..."})),
    left=dict(stand=_BIG_LEFT,
              walk0=_with(_BIG_LEFT, {2: "....kCCSsCCQk...", 3: "....kCCSsCCQk...",
                                      4: "....kTTSsTTTk...", 5: "....kCCSSCCQk...",
                                      7: "...kXYkkkYYk....", 8: "..kXYk...kYYk...",
                                      9: "..kXYk...kYYk...", 10: ".kFFFk...kFFFk.."}),
              walk1=_with(_BIG_LEFT, {2: "....kSsCCCCQk...", 3: "....kSsCCCCQk...",
                                      4: "....kSsTTTTTk...", 5: "....kSSCCCCQk...",
                                      7: "...kYYkkkXYk....", 8: "..kYYk...kXYk...",
                                      9: "..kYYk...kXYk...", 10: ".kFFFk...kFFFk.."})),
)


# ==========================================================================
# Folk palette: the mountain and the road
# ==========================================================================

# The thyrsus: a fennel staff wound with ivy and tipped with a pine cone.
_THYRSUS = ["_kk_", "kOok", "kobk", "kbok", "kobk", "_kk_", "gvg"] + ["kg", "gk", "kg", "kv", "kg", "gk",
                                                                       "kg", "kv", "kg", "kg", "kg", "kg",
                                                                       "kg", "kb"]

# Euia, Bromia and Kithairon's bacchants: loose dark hair crowned with ivy, a
# fawnskin knotted over the left shoulder on a saffron chiton to mid-calf,
# bare feet, and the thyrsus held high in her right hand.
MAENAD = dict(
    name="maenad", pal="folk", arch="midi",
    roles=dict(C="O", Q="o", T="g", F="s"),
    head=dict(
        down=_BLANK3 + [
            "......kkkk......",
            "....kkbbbbkk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..vgvggvggvgvg..",
            "..kbSbbSbbSbbk..",
            ".kbbSkSSSSkSbbk.",
            ".kbbSkSSSSkSbbk.",
            ".kbbsSSSSSSsbbk.",
            ".kbbbssSSssbbbk.",
            ".kbbk.kssk.kbbk.",
        ],
        up=_BLANK3 + [
            "......kkkk......",
            "....kkbbbbkk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            ".gvgvggvggvgvg..",
            "..kbbbbbbbbbbk..",
            ".kbbbbubbbbbbbk.",
            ".kbbbbbubbbbbbk.",
            ".kbbbbubbbbbbbk.",
            ".kbbbbbubbbbbbk.",
            ".kbbbbubbbbbbbk.",
        ],
        left=_BLANK3 + [
            "......kkkkk.....",
            "....kkbbbbbk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..vgvggvggvgvgk.",
            "..kbSbbbbbbbbbk.",
            "..kSSSSSbsbbbbbk",
            "..kSkSSSssbbbbbk",
            "..kSkSSSSbbubbbk",
            "..kSSSSSsbbbubk.",
            "...kbsSssbkbbbk.",
        ],
    ),
    over=dict(
        down={"all": [("b0", [".kbk__________kb", ".kbk________ob__", "..k_______oLb___",
                              "________oob_____", "_______oLb______", "______oob_______"]),
                      pole(0, 0, _THYRSUS), ("b5", ["__S_____________"])],
              "walk1": [("b5", ["..SSSCCCCCQSSk..", "..kkCCCCCCCQkk.."])]},
        up={"all": [("b0", ["..kbbbbbbbbbbk..", "..kbbbubbbbbbk..", "..kbobubbbbbbk..",
                            "...kLoobbbbbk...", "_____kooLo______", "_______ooLo_____"]),
                    pole(12, 0, _flip(_THYRSUS)), ("b5", ["_____________S__"])],
            "walk0": [("b5", ["..kSSCCCCCQSSS..", "..kkCCCCCCCQkk.."])]},
        left={"all": [("b0", ["_________kbbk___", "_________kbbk___", "________oobk____",
                              "_______oLob_____"]),
                      pole(0, 0, _THYRSUS), ("b4", ["__Ss____________"])]},
    ),
)

# Lenaia and Thyrsa's vineyard dancers: the same maenad in the city's colors, a
# wine-red chiton shaded grape (wine palette).
MAENAD_THYRSA = dict(MAENAD, name="maenad_thyrsa", pal="wine", roles=dict(C="u", Q="n", T="g", F="s"))

# Komos and the comic chorus men: a snub-nosed satyr mask pushed up on dark
# curls, a grin and a beard, bare chest, a goat-hair costume to the hooves with
# a tail behind, and a wineskin under his left arm.
_WINESKIN = ["_kbk_", "kbuuk", "kuuuk", "kbuuk", "_kkk_"]
SATYR = dict(
    name="satyr", pal="folk", arch="tunic",
    roles=dict(C="S", Q="s", T="b", F="k", X="y", Y="b"),
    head=dict(
        down=[
            "..kk.k....k.kk..",
            "..kLklkkkklkLk..",
            "...kLLLLLLLLk...",
            "...kLkkLLkkLk...",
            "..kbLLLuuLLLbk..",
            "..kbbkLLLLkbbk..",
            "..kbSbbSbbSbbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "..kbsLLLLLLsbk..",
            "...kbbkkkkbbk...",
            "....kbbbbbbk....",
        ],
        up=[
            "..kk.k....k.kk..",
            "..kLklkkkklkLk..",
            "...kllllllllk...",
            "...kllllllllk...",
            "..kbkllllllkbk..",
            "..kbbkkkkkkbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbubbbbbbk..",
            "..kbbbbbbubbbk..",
            "..kbbbbbbbbbbk..",
            "...kbbbbbbbbk...",
            "....kbSSSSbk....",
        ],
        left=[
            ".....k..kk......",
            "....klkkkLk.....",
            "...kLLLLLkk.....",
            "..kLkkLLLLk.....",
            ".kuLLLLLLLlk....",
            "..kkkLLLLlkbk...",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSLLSSSbbbbk..",
            "...kbbbbbbbbk...",
            "....kbbbbbbk....",
        ],
    ),
    over=dict(
        down={"all": [("b5", ["_____ybyybyb____", "____kyybyybyk___"]),
                      pole(10, "b1", _WINESKIN)]},
        up={"all": [("b5", ["_____ybyybyb____", "____kyybyybyk___", "_______kyk______",
                            "_______kbk______"]),
                    pole(1, "b1", _flip(_WINESKIN))]},
        left={"all": [("b5", ["_____yybyyk_____", "_____ybyybk_____"]),
                      ("b4", ["___________kyk__", "___________kbyk_", "____________kk__"]),
                      pole(7, "b1", _WINESKIN)]},
    ),
)

# Silenos, the god's old tutor: bald and round and red-nosed, satyr ears, a
# long white beard over his chest, a goatskin slung over his left shoulder, a
# linen loincloth, and the wineskin he never puts down.
SILENOS = dict(
    name="silenos", pal="folk", arch="round",
    roles=dict(C="S", Q="s", T="u", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kSSSSSSk....",
            ".k.kSSSSSSSsk.k.",
            ".kSkSSSSSSSSkSk.",
            "..kkLSSSSSSLkk..",
            "..kLLSkSSkSLLk..",
            "..kLSSSuuSSSLk..",
            "..kLLLsuusLLLk..",
            "..kLLLLkkLLLLk..",
            "...kLLLLLLLLk...",
        ],
        up=[
            ".....kkkkkk.....",
            "....kSSSSSSk....",
            ".k.kSSSSSSSsk.k.",
            ".kSkSSSSSSSskSk.",
            "..kkSSSSSSSskk..",
            "..kLSSSSSSSsLk..",
            "..kLLLSSSSLLLk..",
            "..kLLLLLLLLLLk..",
            "...kLLLLLLLLk...",
            "....kLLLLLLk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkSSSSSk....",
            "...kSSSSSSSsk...",
            "..kSSSSSSSSskSk.",
            "..kSSSSSSSSSkSk.",
            "..kSkSSSLLLskk..",
            ".kuuSSSLLLLLk...",
            ".kuSSSLLLLLLk...",
            "..kkLLLLLLLk....",
            "...kLLLLLLk.....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["_________yyk____", "_________yybyk__", "_________ybyyk__",
                              "__________yybk__", "___________yyk__"]),
                      ("b0", ["____kLLLLLLk____", "____kLLLLLLk____", "_____kLLLLk_____",
                              "______kLLk______"]),
                      ("b4", ["____ss____ss____"]),
                      ("b6", ["_____llllll_____"]),
                      pole(11, "b2", _WINESKIN)]},
        up={"all": [("b0", ["___kyyyk________", "__kyybyyk_______", "__kybyyyyk______",
                            "__kyybyyybk_____", "__kyyyk_ybyk____"]),
                    ("b6", ["_____llllll_____"]),
                    pole(0, "b2", _flip(_WINESKIN))]},
        left={"all": [("b0", ["______yyk_______", "_____yybyk______", "_____ybyyyk_____"]),
                      ("b0", ["_____kLLk_______", "____kLLLk_______", "____kLLk________"]),
                      ("b6", ["_____lllll______"]),
                      pole(8, "b2", _WINESKIN)]},
    ),
)

# Manto, Thyrsa's blind augur: tiny and very old, white hair in a knot, white
# eyes in a face tilted up to the sky, a dark robe, and a black cornel staff.
_CORNEL = ["kk", "kb"] * 7
MANTO = dict(
    name="manto", pal="folk", arch="robe_small",
    roles=dict(C="n", Q="k", T="b", F="b"),
    head=dict(
        down=[
            "......kkkk......",
            ".....kLLLyk.....",
            "....kkLLLykk....",
            "...kLLLLLLLyk...",
            "...kLSSSSSSyk...",
            "...kSLkSSkLSk...",
            "...kSyLSSLySk...",
            "...kSSSssSSSk...",
            "....kSSkkSSk....",
            ".....kssssk.....",
        ],
        up=[
            "......kkkk......",
            ".....kLLLyk.....",
            "....kkLLLykk....",
            "...kLLLLLLLyk...",
            "...kLLLLLLLyk...",
            "...kyLLLLLLyk...",
            "...knyLLLLynk...",
            "...knnyyyynnk...",
            "....knnnnnnk....",
            ".....kSSSSk.....",
        ],
        left=[
            "......kkkk......",
            ".....kyLLLk.....",
            "....kkyLLLkk....",
            "...kLLLLLLLLk...",
            "..kSSSSLLLLyk...",
            "..kLySSSLLLyk...",
            ".kSSSSSSyLLyk...",
            "..kkSSSSsnnnk...",
            "...kSSssnnnk....",
            "....kssknnk.....",
        ],
    ),
    over=dict(
        down={"all": [pole(1, 4, _CORNEL), ("b3", ["___S____________"])]},
        up={"all": [pole(13, 4, _flip(_CORNEL)), ("b3", ["____________S___"])]},
        left={"all": [pole(1, 4, _CORNEL), ("b3", ["___S____________"])]},
    ),
)

# The Kronia's readers and greeter: a plain undyed tunic with a gold sickle pin
# at the shoulder, and a smiling clay half-mask over the eyes.
KRONIST = dict(
    name="kronist", pal="folk", arch="tunic",
    roles=dict(C="l", Q="y", T="b", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kooooooooouk..",
            "..kookooookouk..",
            "..kokokookokuk..",
            "..kbooooooouuk..",
            "...kSkSSSSkSk...",
            "....kskkkksk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kubbbbbbbbuk..",
            "..kbuuuuuuuubk..",
            "..kbbbbbbbbbbk..",
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
            ".koooooubbbbbk..",
            ".kokoooubsbbbk..",
            ".kkokouubsbbbk..",
            "..kSSSSSsbbbk...",
            "..kkSSSSbbbk....",
            "...ksSSsbbk.....",
        ],
    ),
    over=dict(
        down={"all": [("b1", ["_________Ok_____"])]},
        left={"all": [("b1", ["______Ok________"])]},
    ),
)

# The herald on the Eleutherai road (and in the orchestra): a runner's short
# linen chiton girt high with red, a red fillet, an ox-horn on a cord across
# his chest, and the barrier pole he shoulders like an oar.
_POLE = ["kk", "Lk", "uk", "uk", "Lk", "Lk", "uk", "uk", "Lk", "Lk", "uk", "uk", "Lk", "Lk", "uk",
         "uk", "Lk", "Lk", "uk", "kk"]
HERALD = dict(
    name="herald", pal="folk", arch="tunic",
    roles=dict(C="L", Q="l", T="u", F="b"),
    head=dict(
        down=_BLANK3 + [
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kuuuuuuuuuuk..",
            "..kbSbbSbbSbbk..",
            "..bsSkSSSSkSsb..",
            "..bsSkSSSSkSsb..",
            "...bSSSSSSSSb...",
            "....bssSSssb....",
        ],
        up=_BLANK3 + [
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kuuuuuuuuuuk..",
            "..kbbbbbbbbubk..",
            "..bsbbbbbbbbub..",
            "..bsbbbbbbbbsb..",
            "...bbbbbbbbbb...",
            "....bbSSSSbb....",
        ],
        left=_BLANK3 + [
            "......kkkkk.....",
            "....kkbbbbbk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kuuuuuuuuuuk..",
            "..kbSbSbbbbbbuk.",
            "..kSSSSSbsbbbuk.",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbk...",
            "...bsSSSsbbk....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["_____b__________", "______b_________", "_______b________",
                              "________b_kk____", "_________kLlk___", "__________kLok__",
                              "___________kk___"]),
                      pole(0, 0, _POLE), ("b2", ["__S_____________"])],
              "walk1": [("b5", ["..SSSCCCCCQSSk..", "..kkCCCCCCCQkk.."])]},
        up={"all": [("b0", ["__________b_____", "_________b______", "________b_______",
                            "_______b________"]),
                    pole(14, 0, _flip(_POLE)), ("b2", ["_____________S__"])],
            "walk0": [("b5", ["..kSSCCCCCQSSS..", "..kkCCCCCCCQkk.."])]},
        left={"all": [("b3", ["______kk________", "_____kLlk_______", "______kok_______",
                              "_______k________"]),
                      pole(1, 0, _POLE), ("b2", ["___S____________"])]},
    ),
)


# ==========================================================================
# Wine palette: Thyrsa
# ==========================================================================

# A basket of black grapes (lilac bloom on grape purple) in an ochre basket.
_GRAPES = ["_kkk_", "kaBak", "kBnBk", "knBnk", "kOoOk", "_kkk_"]
# A vine-pruner's billhook, blade curled at the top.
_HOOK = ["kk_", "kLk", "_kb", "__b", "__b"]

# Ikarios, Oinopion and the vineyard men: a wine-red headscarf, a short beard,
# an undyed exomis off the right shoulder, legs stained purple to the knee from
# the treading floor, a basket of black grapes on his left shoulder and a
# pruning hook in his right hand.
VINTNER = dict(
    name="vintner", pal="wine", arch="tunic",
    roles=dict(C="l", Q="y", T="b", F="n", X="B", Y="n"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kuuuuuuk....",
            "...kuuuuuuuuk...",
            ".kkuuuuuuuuuuk..",
            "kukbuuuuuuuubk..",
            "kukbbbbbbbbbbk..",
            ".kkbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "..kbbSSSSSSbbk..",
            "...kbbbssbbbk...",
        ],
        up=[
            ".....kkkkkk.....",
            "....kuuuuuuk....",
            "...kuuuuuuuuk...",
            "..kuuuuuuuuuukk.",
            "..kbuuuuuuuubkuk",
            "..kbbuuuuuubbkuk",
            "..kbbbbbbbbbbkk.",
            "..kbbbbbbbbbbk..",
            "..ksbbbbbbbbsk..",
            "...kbbbbbbbbk...",
            "....kbSSSSbk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkuuuuuk....",
            "...kuuuuuuuuk...",
            "..kuuuuuuuuuuk..",
            "..kbuuuuuuuuukk.",
            "..kbbbbuuuuubkuk",
            "..kSSSSbkuubkkuk",
            "..kSkSSSbkkbbkk.",
            "..kSkSSbbbbbbk..",
            "...kbbbbbbbbk...",
            "....kbbbbbbk....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["____SS__________", "___SSs__________"]),
                      pole(11, 6, _GRAPES), ("b1", ["___________kSk__"]),
                      pole(0, "b2", _HOOK), ("b5", ["__S_____________"])],
              "walk1": [("b5", ["..SSSCCCCCQSSk..", "..kkCCCCCCCQkk.."])]},
        up={"all": [("b0", ["__________SS____", "__________sSS___"]),
                    pole(0, 6, _flip(_GRAPES)), ("b1", ["__kSk___________"])]},
        left={"all": [pole(7, 6, _GRAPES), ("b1", ["________kSk_____"]),
                      pole(0, "b2", _HOOK), ("b4", ["__Ss____________"])]},
    ),
)

# A tragic actor's mask carried in the hand: white, open-mouthed.
_HAND_MASK = ["_kkk_", "kLLLk", "kkLkk", "kLLLk", "kLkLk", "_kkk_"]

# Hegelochos, Mynniskos, Thettalos, Theodoros: Dionysus's actors. Dark curls
# under a gold fillet and a short beard, a long-sleeved wine-red robe patterned
# in gold and white, tragic boots with thick soles, his mask in his left hand
# and his right hand raised to declaim.
ACTOR = dict(
    name="actor", pal="wine", arch="robe_soles",
    roles=dict(C="u", Q="n", T="O", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbbkbbkbbk...",
            "..kbbbbbbbbbbk..",
            "..kOOOOOOOOOOk..",
            "..kbSbbSbbSbbk..",
            "..bsSkSSSSkSsb..",
            "..bsSkSSSSkSsb..",
            "..kbbSSSSSSbbk..",
            "...kbbbssbbbk...",
            "....kbbbbbbk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbbkbbkbbk...",
            "..kbbbbbbbbbbk..",
            "..kOOOOOOOOOOk..",
            "..kbbkbbbkbbbk..",
            "..kbbbbbbbbbbk..",
            "..ksbbkbbbkbsk..",
            "..ksbbbbbbbbsk..",
            "...kbbbbbbbbk...",
            "....kbSSSSbk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkbbbbbk....",
            "...kbbkbbkbbk...",
            "..kbbbbbbbbbbk..",
            "..kOOOOOOOOOOk..",
            "..kbSbSbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSbbbbbk...",
            "...kbbbbbbbk....",
            "....kbbbbk......",
        ],
    ),
    over=dict(
        down={"all": [(6, ["_k______________", "kSk_____________", "kSk_____________",
                           "kuk_____________", "kuuk____________", "_kuk____________"]),
                      ("b2", ["__kuu___________", "__kuu___________", "__kOO___________",
                              "__kuu___________"]),
                      ("b1", ["____OoOoOoOo____"]), ("b7", ["____LuLuLuLu____"]),
                      ("b9", ["___OOOOOOOOOO___"]),
                      pole(11, "b3", _HAND_MASK)],
              "walk0": [("b5", ["__kuu___________"])]},
        up={"all": [(6, ["______________k_", "_____________kSk", "_____________kSk",
                         "_____________kuk", "____________kuuk", "____________kuk_"]),
                    ("b2", ["___________uuk__", "___________uuk__", "___________OOk__",
                            "___________uuk__"]),
                    ("b1", ["____OoOoOoOo____"]), ("b7", ["____LuLuLuLu____"]),
                    ("b9", ["___OOOOOOOOOO___"]),
                    pole(0, "b3", _flip(_HAND_MASK))],
            "walk1": [("b5", ["___________uuk__"])]},
        left={"all": [(5, ["_k______________", "kSk_____________", "kSk_____________",
                           "kuk_____________", "_kuk____________"]),
                      ("b1", ["_____OoOoO______"]), ("b7", ["____LuLuLu______"]),
                      ("b9", ["____OOOOOOOO____"]),
                      pole(6, "b4", _HAND_MASK)]},
    ),
)

# Thespis, the Masked Player: tall, with a long grape-purple robe patterned in
# ivy and hemmed in gold, tragic boots, gray-streaked hair under an ivy crown,
# and a mask always on his face, tied behind with lilac ribbons. The mask is
# his oldest Prosomime: her eye holes hold its violet haze. Two sheets share
# everything but the face: the tragic mask and the comic one. From behind they
# are the same, so a script can swap them while he has his back turned.
_THESPIS_UP = [
    ".....kkkkkk.....",
    "...kkbbybbbkk...",
    "..kgvbbbbbbvgk..",
    "..kbgvgvgvgvbk..",
    "..kbbbbybbbbbk..",
    "..kbybbbbbybbk..",
    "..kbbbaaabbbbk..",
    "..kbbbabbabbbk..",
    "..kbbbabbabbbk..",
    "...kbbbbbbbbk...",
    "....kbSSSSbk....",
]
_THESPIS_IVY_DOWN = [("b1", ["____gv____vg____"]), ("b3", ["______gv________"]),
                     ("b5", ["_____vg___gv____"]), ("b7", ["____gv__vg__gv__"]),
                     ("b9", ["___OOOOOOOOOO___"])]
_THESPIS_IVY_UP = [("b1", ["____gv____vg____"]), ("b3", ["________vg______"]),
                   ("b5", ["____gv___vg_____"]), ("b7", ["___gv__vg__gv___"]),
                   ("b9", ["___OOOOOOOOOO___"])]
_THESPIS_IVY_LEFT = [("b1", ["_____vg_________"]), ("b5", ["_____gv_________"]),
                     ("b7", ["____gv__vg______"]), ("b9", ["____OOOOOOOO____"])]


def _thespis(name, down_face, left_face):
    return dict(
        name=name, pal="wine", arch="robe_soles",
        roles=dict(C="B", Q="n", T="O", F="b"),
        head=dict(down=down_face, up=_THESPIS_UP, left=left_face),
        over=dict(
            down={"all": list(_THESPIS_IVY_DOWN)},
            up={"all": list(_THESPIS_IVY_UP)},
            left={"all": list(_THESPIS_IVY_LEFT)},
        ),
    )


THESPIS = _thespis(
    "thespis",
    [
        ".....kkkkkk.....",
        "...kkbbybbbkk...",
        "..kgvbbbbbbvgk..",
        "..kbgvgvgvgvbk..",
        "..kbLLLLLLLLbk..",
        "..kbLLkLLkLLbk..",
        "..kbLnkLLknLbk..",
        "..kbLLLlLLLLbk..",
        "..kblLLkkLLlbk..",
        "..kbllkLLkllbk..",
        "...kbllllllbk...",
    ],
    [
        "......kkkkk.....",
        "....kkbbbybk....",
        "...kgvbbbbbbk...",
        "..kbgvgvgvgvbk..",
        "..kLLLLLbbbbbk..",
        "..kLLkLlbybbbk..",
        ".kLLnkLlbbbbbk..",
        ".kLLLLlbbbabk...",
        "..kkkLlbbbabk...",
        "..kLkLlbbbbk....",
        "...kllkbbbk.....",
    ],
)
THESPIS_COMIC = _thespis(
    "thespis_comic",
    [
        ".....kkkkkk.....",
        "...kkbbybbbkk...",
        "..kgvbbbbbbvgk..",
        "..kbgvgvgvgvbk..",
        "..kbLkLLLLkLbk..",
        "..kbkLLLLLLkbk..",
        "..kbLnkLLknLbk..",
        "..kbLLLlLLLLbk..",
        "..kbkLLLLLLkbk..",
        "..kblkkkkkklbk..",
        "...kbluuuulbk...",
    ],
    [
        "......kkkkk.....",
        "....kkbbbybk....",
        "...kgvbbbbbbk...",
        "..kbgvgvgvgvbk..",
        "..kLkLLLbbbbbk..",
        "..kkLLLlbybbbk..",
        ".kLLnkLlbbbbbk..",
        ".kLLLLlbbbabk...",
        "..kLLLlbbbabk...",
        "..kkkklbbbbk....",
        "...kuukbbbk.....",
    ],
)


# ==========================================================================
# Cast palette: the Dionysia's players (beat 32)
# ==========================================================================

# The CHORUS LEADER (and region B2's masked Iapetos): a thin man in a long
# white chorus robe and a white tragic mask framed by black hair. His right
# hand is black with ink to the wrist.
CHORUS_LEADER = dict(
    name="chorus_leader", pal="cast", arch="robe_tall",
    roles=dict(C="L", Q="l", T="l", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kkkkkkkk....",
            "...kkkktkkkkk...",
            "..kktkkkkkkkkk..",
            "..kkLLLLLLLLkk..",
            "..kkLLkLLkLLkk..",
            "..kkLkkLLkkLkk..",
            "..kkLLLlLLLLkk..",
            "..kkLLLkkLLLkk..",
            "..kkLLkLLkLLkk..",
            "...kkLLLLLLkk...",
        ],
        up=[
            ".....kkkkkk.....",
            "....kkkkkkkk....",
            "...kkkktkkkkk...",
            "..kktkkkkkkkkk..",
            "..kkkkkkkkkkkk..",
            "..kkkkktkkkkkk..",
            "..kkLLLLLLLLkk..",
            "..kkkkkkkkkkkk..",
            "..kkkkkkkkkkkk..",
            "...kkkkkkkkkk...",
            "....kkSSSSkk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkkkkkkk....",
            "...kkkktkkkkk...",
            "..kktkkkkkkkkk..",
            "..kLLLLLkkkkkk..",
            "..kLLkLlkkkkkk..",
            ".kLkkLLlkkkkkk..",
            ".kLLLLlkkkkkk...",
            "..kkkLlkkkkkk...",
            "..kLkLlkkkkk....",
            "...kllkkkkk.....",
        ],
    ),
    over=dict(
        down={"all": [("b3", ["___k____________", "___kk___________", "__kkk___________"])],
              "walk0": [("b5", ["__kkk___________"])]},
        up={"all": [("b3", ["____________k___", "___________kk___", "___________kkk__"])],
            "walk1": [("b5", ["___________kkk__"])]},
    ),
)

# A small clay jar of honey, held in both hands.
_JAR = ["_kkk_", "kOOOk", "_kuk_", "kuuuk", "kuurk", "_kkk_"]

# The bee-woman: an actor in a long pale veil with a honeycomb hem over a
# honey-colored robe, a white woman's mask, and a clay jar held before her.
BEE_WOMAN = dict(
    name="bee_woman", pal="cast", arch="robe",
    roles=dict(C="o", Q="u", T="O", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kllllllk....",
            "...klllllllLk...",
            "..klllllllllLk..",
            "..klkkkkkkkklk..",
            "..klkLLLLLLklk..",
            "..klLkLLLLkLlk..",
            "..klLkLLLLkLlk..",
            "..klLLLrrLLLlk..",
            "..kllkLLLLkllk..",
            "..klllkkkkllLk..",
        ],
        up=[
            ".....kkkkkk.....",
            "....kllLlllk....",
            "...kllLllLlLk...",
            "..klllLllLllLk..",
            "..kllLlllLllLk..",
            "..kllLllllLlLk..",
            "..kllLllllLlLk..",
            "..klLlllllLllk..",
            "..klLllllllLlk..",
            "..klLllllllLlk..",
            "..klLllllllLlk..",
        ],
        left=[
            "......kkkkk.....",
            "....kklllllk....",
            "...klllllllLk...",
            "..klllllllllLk..",
            "..kkkkklllllLk..",
            "..kLLLklllllLk..",
            ".kLkLLklllllLk..",
            ".kLkLLklllllLk..",
            "..kLrLklllllLk..",
            "..kLLklllllLk...",
            "...kkllllllLk...",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["..klk______kLk..", "..kl________Lk..", "..kl________Lk..",
                              "..kk________kk.."]),
                      pole(5, "b2", _JAR), ("b4", ["____S_____S_____"]),
                      ("b7", ["___OkOOkOOkO____"]), ("b8", ["__kOOkOOkOOkOk__"])]},
        up={"all": [("b0", ["..kLllllllllLk..", "..kLlllllllLlk..", "..kLlllllllLlk..",
                            "..kOkOOkOOkOOk..", "..kkOkkOkkOkkk.."]),
                    ("b7", ["____OkOOkOOkO___"]), ("b8", ["__kOkOOkOOkOOk__"])]},
        left={"all": [("b0", ["_______klllk____", "________llLk____", "________llLk____",
                              "________kkkk____"]),
                      pole(2, "b2", _JAR), ("b4", ["______S_________"]),
                      ("b7", ["____OkOOkO______"]), ("b8", ["___kOOkOOkOk____"])]},
    ),
)


# The three Fates, as the Dionysia plays them: black-figure costumes, robes of
# glossy black with incised folds and a meander hem, white masks (black-figure
# women are painted white) under black hair. Each has her own incision color
# and her own tool: the Spinner's distaff (linen), the Measurer's rod
# (bronze), the Cutter's shears (crimson). One palette for all three.
def _fate(name, a, over_down, over_up, over_left):
    head_down = [
        ".....kkkkkk.....",
        "....kkkkkkkk....",
        "...kkkkkkkkkk...",
        "..kkkkkkkkkkkk..",
        "..k" + a * 10 + "k..",
        "..kkLLLLLLLLkk..",
        "..kkLkLLLLkLkk..",
        "..kkLkLLLLkLkk..",
        "..kkLLLLLLLLkk..",
        "..kkkLLkkLLkkk..",
        "...kkLLLLLLkk...",
    ]
    head_up = [
        ".....kkkkkk.....",
        "....kkkkkkkk....",
        "...kkkkkkkkkk...",
        "..kkkkkkkkkkkk..",
        "..k" + a * 10 + "k..",
        "..kkkkkkkkkkkk..",
        "..kkkkkttkkkkk..",
        "..kkkkkkkkkkkk..",
        "..kkkkkkkkkkkk..",
        "...kkkkkkkkkk...",
        "....kkSSSSkk....",
    ]
    head_left = [
        "......kkkkk.....",
        "....kkkkkkkk....",
        "...kkkkkkkkkk...",
        "..kkkkkkkkkkkk..",
        "..k" + a * 7 + "kkkk..",
        "..kLLLLLkkkkkk..",
        "..kLkLLLkkkkkk..",
        "..kLkLLLk" + a + "kkkk..",
        "..kLLLLLkkkkk...",
        "..kkLLLkkkkk....",
        "...kLLLkkkk.....",
    ]
    hem = "__k" + (a + "k") * 5 + "k__"
    return dict(
        name=name, pal="cast", arch="robe",
        roles=dict(C="k", Q="k", T=a, F="b"),
        head=dict(down=head_down, up=head_up, left=head_left),
        over=dict(
            down={"all": [("b1", ["______" + a + "__" + a + "______"]),
                          ("b2", ["______" + a + "__" + a + "______"]),
                          ("b6", ["_____" + a + "____" + a + "_____"]),
                          ("b7", ["____" + a + "__" + a + "__" + a + "_____"]),
                          ("b8", [hem])] + over_down},
            up={"all": [("b1", ["_______" + a + a + "_______"]),
                        ("b6", ["_____" + a + "____" + a + "_____"]),
                        ("b7", ["____" + a + "__" + a + "__" + a + "_____"]),
                        ("b8", [hem])] + over_up},
            left={"all": [("b6", ["______" + a + "_" + a + "_______"]),
                          ("b8", ["___k" + (a + "k") * 4 + "____"])] + over_left},
        ),
    )


_DISTAFF = ["_kk_", "kLlk", "klLk", "kLlk", "_kk_", "_ok", "_ok", "_ok", "_ok", "_ok", "_ok", "_ok",
            "_ok", "_ok", "_ok", "_ok", "_kk"]
_ROD = ["kk", "Ok", "kk", "ok", "ok", "kk", "ok", "ok", "kk", "ok", "ok", "kk", "ok", "ok", "kk", "kk"]
_SHEARS = ["L___L", "kL_Lk", "_kLk_", "_ckc_", "c_k_c", "c___c"]

FATE_SPINNER = _fate(
    "fate_spinner", "L",
    [pole(0, 1, _DISTAFF), ("b5", ["__S_____________"]),
     ("b6", ["___________k____", "___________L____", "__________kLk___"])],
    [pole(12, 1, _flip(_DISTAFF)), ("b5", ["_____________S__"])],
    [pole(0, 1, _DISTAFF), ("b4", ["__Ss____________"])],
)
FATE_MEASURER = _fate(
    "fate_measurer", "o",
    [pole(0, 4, _ROD), ("b5", ["__S_____________"])],
    [pole(14, 4, _ROD), ("b5", ["_____________S__"])],
    [pole(0, 4, _ROD), ("b4", ["__Ss____________"])],
)
FATE_CUTTER = _fate(
    "fate_cutter", "c",
    [pole(5, "b0", _SHEARS), ("b4", ["____S_____S_____"])],
    [("b4", ["___S________S___"])],
    [pole(1, "b0", _SHEARS), ("b4", ["___S____________"])],
)

# The gold-masked king: a tall actor in a crimson royal robe hemmed in bronze,
# a gold crown, and a smooth gold mask with closed eyes. His kneeling frames
# are their own sheet (POSES, gold_mask_king_kneel).
_KING_DOWN = [
    "....kk.kk.kk....",
    "....kOkOOkOk....",
    "...kOOOOOOOok...",
    "..kkkkkkkkkkkk..",
    "..kkOOOOOOOokk..",
    "..kkOOOOOOOokk..",
    "..kkouuOOuuokk..",
    "..kkOOOOOOOokk..",
    "..kkOOOooOOokk..",
    "..kkOOuuuuOokk..",
    "...kkoOOOOokk...",
]
_KING_UP = [
    "....kk.kk.kk....",
    "....kOkOOkOk....",
    "...kOOOOOOOok...",
    "..kkkkkkkkkkkk..",
    "..kkkkkkkkkkkk..",
    "..kkkkkkktkkkk..",
    "..kkktkkkkkkkk..",
    "..kkkkkkkkkkkk..",
    "..kkkkkkktkkkk..",
    "...kkkkkkkkkk...",
    "....kkSSSSkk....",
]
_KING_LEFT = [
    ".....kk.kk.k....",
    ".....kOkOOkOk...",
    "....kOOOOOOOok..",
    "...kkkkkkkkkkk..",
    "..kOOOOOokkkkk..",
    "..kOOOOOokkkkk..",
    ".kOuuOOOokkktk..",
    ".kOOOOOOokkkkk..",
    "..kOOooOokkkk...",
    "..kOuuOOokkk....",
    "...kOOOokkk.....",
]
GOLD_MASK_KING = dict(
    name="gold_mask_king", pal="cast", arch="robe_tall",
    roles=dict(C="c", Q="r", T="o", F="b"),
    head=dict(down=_KING_DOWN, up=_KING_UP, left=_KING_LEFT),
    over=dict(
        down={"all": [("b0", ["____o______o____", "___o________o___"]), ("b9", ["__kooooooooook__"])]},
        up={"all": [("b9", ["__kooooooooook__"])]},
        left={"all": [("b9", ["___kooooooook___"])]},
    ),
)

# A sickle for the Unwoven: a bronze crescent blade on a short handle.
_SICKLE = ["_kk_", "kOok", "k_kO", "___k", "__kb", "__kb", "___k"]

# The Unwoven: Borboros playing the cursed child, a deliberate echo of the
# player a size too big. A wide straw petasos, a blank pale mask, an
# Aegean-blue chlamys pinned with gold over a cream chiton, a terracotta
# satchel at his hip, sandals, and the old sickle in his right hand.
UNWOVEN_ACTOR = dict(
    name="unwoven_actor", pal="cast", arch="big",
    roles=dict(C="L", Q="l", T="u", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kOOOOOok....",
            "...kOOOOOOOok...",
            ".kkkbbbbbbbbkkk.",
            "kOOOOOOOOOOOOOok",
            ".kkoooooooooookk",
            "..kbLLLLLLLLbk..",
            "..kbLkkLLkkLbk..",
            "..kbLLLLLLLLbk..",
            "..kbLLLllLLLbk..",
            "...kLLLLLLLLk...",
        ],
        up=[
            ".....kkkkkk.....",
            "....kOOOOOok....",
            "...kOOOOOOOok...",
            ".kkkbbbbbbbbkkk.",
            "kOOOOOOOOOOOOOok",
            ".kkoooooooooookk",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..ksbbbbbbbbsk..",
            "...kbbSSSSbbk...",
        ],
        left=[
            "......kkkkk.....",
            ".....kOOOOOok...",
            "....kOOOOOOOok..",
            "..kkkbbbbbbbkk..",
            "kOOOOOOOOOOOOOok",
            ".kkoooooooooookk",
            "..kLLLLLbbbbbk..",
            "..kLkkLLbbbbbk..",
            "..kLLLLLbbbbbk..",
            "..kLLLllbbbbk...",
            "...kLLLLbbbk....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["__kBB______nBk__", ".kBBn_______nBk.", ".kB__________Bk.",
                              ".kB__________nk.", ".kn__________nk.", ".kn__________nk.",
                              ".kk__________kk."]),
                      ("b0", ["___O____________"]),
                      ("b4", ["___________uu___", "__________kuuk__"]),
                      pole(0, "b2", _SICKLE)]},
        up={"all": [("b0", ["..kBBBBBBBBBBk..", ".kBBBBBBBBBBnBk.", ".kBBBBBBBBBBnBk.",
                            ".kBBBBBBBBBnBBk.", ".knBBBBBBBBnBnk.", ".knBBBBBBBnBBnk.",
                            ".kknnnnnnnnnnkk."])]},
        left={"all": [("b0", ["_________BBk____", "________BBBnk___", "________BBBnk___",
                              "________BBnnk___", "________BnBnk___", "________nBnnk___",
                              "________kkkk____"]),
                      ("b4", ["______kuuk______"]),
                      pole(0, "b2", _SICKLE)]},
    ),
)


# ==========================================================================
# Output
# ==========================================================================

WALKERS = [MAENAD, SATYR, SILENOS, MANTO, KRONIST, HERALD,
           VINTNER, ACTOR, THESPIS, THESPIS_COMIC, MAENAD_THYRSA,
           CHORUS_LEADER, BEE_WOMAN, FATE_SPINNER, FATE_MEASURER, FATE_CUTTER,
           GOLD_MASK_KING, UNWOVEN_ACTOR]
OBJECTS = []
POSES = []


# ==========================================================================
# Poses: seated and kneeling frames, drawn frame by frame (cast palette)
# ==========================================================================
#
# A pose sheet is nine 16x32 frames in the standard order, played by
# sAnimTable_Standard, so the facing picks the pose's direction and
# walk_in_place_* loops stand -> frame A -> stand -> frame B. Nothing here
# bobs: the "walk" frames are the pose's own small motions (a hat turning, a
# trowel striking, a sob). Each frame is a list of rows standing on row 30
# unless it names another bottom row.

from sprites_npc import KLEON, ALETHEA  # noqa: E402

_KLEON_TOP = {d: KLEON[d]["top"] for d in ("down", "up", "left")}
_ALETHEA_TOP = {d: ALETHEA[d]["top"] for d in ("down", "up", "left")}


def _frame(rows, bottom=FEET_ROW):
    return (list(rows), bottom)


def _same(frame):
    return dict(stand=frame, walk0=frame, walk1=frame)


# Kleon's back, sitting: the crimson chlamys spread on the bench, his legs out
# of sight in front of him. Shared by both of his seated sheets.
_KLEON_SEAT_UP = _frame(_KLEON_TOP["up"] + [
    "..kccrkSSkrcck..",
    ".kccccrccrccrrk.",
    ".kcccccrcccrrrk.",
    ".kcccccrccrrrrk.",
    ".kccccrcccrrrrk.",
    ".krcccrccrrrrrk.",
    ".kkrrrrrrrrrrkk.",
    "..kkkkkkkkkkkk..",
], bottom=29)

# Seated in profile, hands on his knees, legs hanging from the seat's edge.
_KLEON_SEAT_LEFT = _frame(_KLEON_TOP["left"] + [
    ".....kSSkcck....",
    "....kLLLLkccrk..",
    "....kLoOlkccrk..",
    "....kLSslkcrrk..",
    "....kbSsbkcrrrk.",
    "..kkkLSSLkcrrrk.",
    ".kLLLLLLlkrrrk..",
    ".kSSkkkkkkkkk...",
    ".kSsk...........",
    "kbbbk...........",
])

_KLEON_SEAT_TORSO = [
    "..kcrkLSSLkrck..",
    ".kcSSLLLLLLSsrk.",
    ".kcoOLLLLLlSsrk.",
]
_KLEON_SEAT_LEGS = [
    "...kSsk..kSsk...",
    "...kbbk..kbbk...",
]

# OBJ_EVENT_GFX_ICHOR_KLEON_SEATED: on the stage's edge after the play, turning
# the petasos actor's hat in his lap (face down; walk in place to turn it), and
# in the front row (face up to watch the stage, left or right to turn to the
# player).
KLEON_SEATED = dict(
    name="kleon_seated", pal="cast", kind="pose",
    frames=dict(
        down=dict(
            stand=_frame(_KLEON_TOP["down"] + _KLEON_SEAT_TORSO + [
                ".kcSsLbbobbSsrk.",
                ".kcSkoOOOOOkSrk.",
                ".kckOObbbbOOkrk.",
                ".kcrkooooookrrk.",
                "..kkkkkkkkkkkk..",
            ] + _KLEON_SEAT_LEGS),
            walk0=_frame(_KLEON_TOP["down"] + _KLEON_SEAT_TORSO + [
                ".kcSsLkkkkLSsrk.",
                ".kcSkkOOOOkkSrk.",
                ".kckOOObbOOOkrk.",
                ".kcrkkoooookkrk.",
                "..kkkkkkkkkkkk..",
            ] + _KLEON_SEAT_LEGS),
            walk1=_frame(_KLEON_TOP["down"] + _KLEON_SEAT_TORSO + [
                ".kcSsLbbobbSsrk.",
                ".kcSkLLLLLLkSrk.",
                ".kckOOOOOOOOkrk.",
                ".kcrkkkkkkkkrrk.",
                "..kkkkkkkkkkkk..",
            ] + _KLEON_SEAT_LEGS),
        ),
        up=_same(_KLEON_SEAT_UP),
        left=_same(_KLEON_SEAT_LEFT),
    ),
)

# OBJ_EVENT_GFX_ICHOR_KLEON_FEAST: at the Kronia's long tables (beat 29), a
# loaf in each fist at his chest. Walking in place facing down, he bites one
# loaf, then the other.
_KLEON_FEAST_BODY = [
    "..kcrkLSSLkrck..",
    ".kcSSLLLLLLSsrk.",
    ".kkkkkLLLLkkkkk.",
    ".kuuokLLLlkuuok.",
    ".kuoukbbobkuouk.",
    ".kkSkkLLLlkkSkk.",
    ".kcrkLLLLLlkrrk.",
    "..kkkkkkkkkkkk..",
] + _KLEON_SEAT_LEGS


def _bite(side):
    """Kleon with one loaf up at his mouth: side 0 his right (viewer's left)."""
    head = list(_KLEON_TOP["down"])
    body = list(_KLEON_FEAST_BODY)
    x = 4 if side == 0 else 8
    for j, cells in enumerate(["kkkk", "kuok", "kuuk", "kkkk"]):
        line = list(head[6 + j])
        line[x:x + 4] = list(cells)
        head[6 + j] = "".join(line)
    # the loaf left his fist: an empty sleeve and forearm below
    for j, cells in enumerate(["kSSk", "kSsk"]):
        line = list(body[2 + j])
        bx = 1 if side == 0 else 11
        line[bx:bx + 4] = list(cells)
        body[2 + j] = "".join(line)
    return head + body


KLEON_FEAST = dict(
    name="kleon_feast", pal="cast", kind="pose",
    frames=dict(
        down=dict(
            stand=_frame(_KLEON_TOP["down"] + _KLEON_FEAST_BODY),
            walk0=_frame(_bite(0)),
            walk1=_frame(_bite(1)),
        ),
        up=_same(_KLEON_SEAT_UP),
        left=dict(
            stand=_frame(_KLEON_TOP["left"][:7] + [
                "..kSkSSSssbbbk..",
                "..kSkSSSSbbbk...",
                "...bsSSSsbbk....",
            ] + _KLEON_SEAT_LEFT[0][10:]),
            walk0=_frame(_KLEON_TOP["left"][:7] + [
                "kkkSkSSSssbbbk..",
                "kuokSSSSSbbbk...",
                "kuukSSSSsbbk....",
            ] + [".kk" + r[3:] if i == 0 else r for i, r in enumerate(_KLEON_SEAT_LEFT[0][10:])]),
            walk1=_frame(_KLEON_TOP["left"][:7] + [
                "..kSkSSSssbbbk..",
                "..kSkSSSSbbbk...",
                "...bsSSSsbbk....",
            ] + _KLEON_SEAT_LEFT[0][10:]),
        ),
    ),
)

# Alethea's back, kneeling or sitting: the sun-gold chiton spread, her
# satchel strap, the ponytail down her back.
_ALETHEA_BACK = [
    "..kokSSkbkSkok..",
    ".kSooooooobooSk.",
    ".kSoooooobooo" "Sk.",
    ".kbbuooobooooSk.",
    ".kbububooooooSk.",
]

# OBJ_EVENT_GFX_ICHOR_ALETHEA_KNEEL: kneeling at a dig with her trowel. Face
# down, left or right to dig toward the viewer or sideways, up from behind;
# walking in place, the trowel rises and strikes.
ALETHEA_KNEEL = dict(
    name="alethea_kneel", pal="cast", kind="pose",
    frames=dict(
        down=dict(
            stand=_frame(_ALETHEA_TOP["down"] + [
                "..kokSSSSSSkok..",
                ".kSobooooooooSk.",
                ".kSoobooookLlkk.",
                ".kSkoobookbbubk.",
                "kSskuoobokbuubk.",
                "kSkooooooooooook",
                "kLlkkkkkkkkkkkk.",
            ]),
            walk0=_frame(_ALETHEA_TOP["down"] + [
                "kkkokSSSSSSkok..",
                "kLlkbooooooooSk.",
                "kSSoobooookLlkk.",
                ".kSkoobookbbubk.",
                "..kkuoobokbuubk.",
                ".kooooooooooooook"[:16],
                ".kkkkkkkkkkkkkk.",
            ]),
            walk1=_frame(_ALETHEA_TOP["down"] + [
                "..kokSSSSSSkok..",
                ".kSobooooooooSk.",
                ".kSoobooookLlkk.",
                ".kSkoobookbbubk.",
                "kSskuoobokbuubk.",
                "kSkooooooooooook",
                "bkLkkkkkkkkkkkk.",
            ]),
        ),
        up=_same(_frame(_ALETHEA_TOP["up"] + _ALETHEA_BACK + [
            ".koooooooooooook",
            ".kkbbkkkkkkbbkk.",
        ])),
        left=dict(
            stand=_frame(_ALETHEA_TOP["left"] + [
                "....koSSkok.....",
                "...kooooobok....",
                "..kSooSSobuk....",
                ".kSkoSsLbbuk....",
                "kSk.kooobuubk...",
                "Lk.kooooooobbk..",
                "lkkkkkkkkkbbbk..",
            ]),
            walk0=_frame(_ALETHEA_TOP["left"] + [
                "....koSSkok.....",
                "kk.kooooobok....",
                "LkkSooSSobuk....",
                "kSSkoSsLbbuk....",
                "...kkooobuubk...",
                "...kooooooobbk..",
                "...kkkkkkkkbbbk.",
            ]),
            walk1=_frame(_ALETHEA_TOP["left"] + [
                "....koSSkok.....",
                "...kooooobok....",
                "..kSooSSobuk....",
                ".kSkoSsLbbuk....",
                "kSk.kooobuubk...",
                "kLkkooooooobbk..",
                "bLbkkkkkkkbbbk..",
            ]),
        ),
    ),
)

# OBJ_EVENT_GFX_ICHOR_ALETHEA_SEATED: in her seat at the Dionysia. Face down,
# she holds the program up to show it (walking in place, she waves it); left
# or right, it lies open in her lap and she reads; up, she watches the stage.
_PROGRAM_DOWN = [
    "..kokSSSSSSkok..",
    ".kSokkkkkkkkoSk.",
    ".kSkLLLLLLLLkSk.",
    ".kSkLlllLlLLkSk.",
    ".kSSLLLLLLLLSSk.",
    ".kokLlLLlllLkok.",
    ".kookkkkkkkkook.",
    "..kkoooooooookk.",
    "...kSsk..kSsk...",
    "...kbbk..kbbk...",
]
ALETHEA_SEATED = dict(
    name="alethea_seated", pal="cast", kind="pose",
    frames=dict(
        down=dict(
            stand=_frame(_ALETHEA_TOP["down"] + _PROGRAM_DOWN),
            walk0=_frame(_ALETHEA_TOP["down"][:9] + _PROGRAM_DOWN[1:7] + [
                "..kokSSSSSSkok..",
                "..kkoooooooookk.",
            ] + _PROGRAM_DOWN[8:]),
            walk1=_frame(_ALETHEA_TOP["down"] + _PROGRAM_DOWN),
        ),
        up=_same(_frame(_ALETHEA_TOP["up"] + _ALETHEA_BACK + [
            ".kbbbuuoooooobk.",
            "..kkkkkkkkkkkk..",
        ], bottom=29)),
        left=dict(
            stand=_frame(_ALETHEA_TOP["left"] + [
                "....koSSkok.....",
                "...kooooobok....",
                "...kooSSobuk....",
                "..kLLLSsLbbuk...",
                ".kLlLlSkbuubk...",
                ".kkkkkkoooobk...",
                ".kSSoooooobk....",
                ".kSskkkkkkk.....",
                ".kSsk...........",
                "kbbbk...........",
            ]),
            walk0=_frame(_ALETHEA_TOP["left"] + [
                "....koSSkok.....",
                "...kooooobok....",
                "..kLLkSSobuk....",
                ".kLlLSsoobuk....",
                ".kLLLkSkbuubk...",
                ".kkkkkkoooobk...",
                ".kSSoooooobk....",
                ".kSskkkkkkk.....",
                ".kSsk...........",
                "kbbbk...........",
            ]),
            walk1=_frame(_ALETHEA_TOP["left"] + [
                "....koSSkok.....",
                "...kooooobok....",
                "...kooSSobuk....",
                "..kLLLSsLbbuk...",
                ".kLlLlSkbuubk...",
                ".kkkkkkoooobk...",
                ".kSSoooooobk....",
                ".kSskkkkkkk.....",
                ".kSsk...........",
                "kbbbk...........",
            ]),
        ),
    ),
)

# OBJ_EVENT_GFX_ICHOR_GOLD_MASK_KING_KNEEL: the gold-masked king on his knees,
# his face in his hands, his crimson robe pooled round him. Walking in place,
# his shoulders heave.
_KING_HANDS = [
    "....kk.kk.kk....",
    "....kOkOOkOk....",
    "...kOOOOOOOok...",
    "..kkkkkkkkkkkk..",
    "..kkOOOOOOOokk..",
    "..kkSkkOOkkSkk..",
    "..kSsSkOOkSsSk..",
    "..kSssSkkSssSk..",
    "..kcSsskksSsck..",
    "..kcckOOOOkcck..",
    "...kckOooOkck...",
]
_KING_KNEEL_BODY = [
    "..kcrrcccrrcck..",
    ".kcrcccccccrrck.",
    ".kccrcccccrcrrk.",
    ".kcccrcccrccrrk.",
    "kccccoooooocrrrk",
    "kcccccccccccrrrk",
    "kooooooooooooook",
    ".kkkkkkkkkkkkkk.",
]
GOLD_MASK_KING_KNEEL = dict(
    name="gold_mask_king_kneel", pal="cast", kind="pose",
    frames=dict(
        down=dict(
            stand=_frame(_KING_HANDS + _KING_KNEEL_BODY),
            walk0=_frame(["." * 16] + _KING_HANDS + _KING_KNEEL_BODY[:3] + _KING_KNEEL_BODY[4:]),
            walk1=_frame(_KING_HANDS + _KING_KNEEL_BODY),
        ),
        up=_same(_frame(_KING_UP + [
            "..kccrrSSrrcck..",
            ".kccccrccrccrrk.",
            ".kcccccrcccrrrk.",
            ".kcccccrccrrrrk.",
            "kccccooooooorrrk",
            "kcccccrcccrrrrrk",
            "kooooooooooooook",
            ".kkbbkkkkkkbbkk.",
        ])),
        left=_same(_frame(_KING_LEFT[:4] + [
            "..kOOOOOOkkkkk..",
            "..kSSSSOOkkkkk..",
            ".kSSsSSOOkkktk..",
            ".kSSSSOOOkkkkk..",
            "..ksSSooOkkkk...",
            "..kkSOuuOkkk....",
            "...kOOOOOkk.....",
            "....kcccSkcck...",
            "...kccccSkccrk..",
            "...kcccSskcrrk..",
            "...kcccSkkcrrk..",
            "..kcccccccrrrk..",
            "..kccccccrrrrrk.",
            "..kooooooooooook",
            "...kkkkkkkkkkkk.",
        ])),
    ),
)

POSES = [KLEON_SEATED, KLEON_FEAST, ALETHEA_KNEEL, ALETHEA_SEATED, GOLD_MASK_KING_KNEEL]


# ==========================================================================
# Field objects
# ==========================================================================
#
# An object spec gives its frame size (fw x fh) and its frames in sheet order.
# One frame is inanimate (sAnimTable_Inanimate); nine frames play through
# sAnimTable_Standard like a walker.

# The god's wooden image, inside the Temple of Dionysus's door: an old xoanon,
# a post of olive wood worn smooth by hands, on a small stone base. Its face
# has worn into something cheerful and dog-like: a round muzzle, a black nose,
# a grin, locks of hair hanging like soft ears. Drawn only in colors the folk
# and wine palettes share, so it reads the same under either tag.
_WOODEN_IMAGE = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "......kkkk......",
    "....kkllllkk....",
    "...kllylllssbk..",
    "..kllllllssssbk.",
    "..kllklllskssbk.",
    ".ksslllllsssbbbk",
    ".ksllLLLLLlssbbk",
    ".ksLLLLkkLLLsbbk",
    ".kskLLLLLLLLksbk",
    ".ksk.kkuukkk.kbk",
    ".kk...kkkk....kk",
    ".....kllsbk.....",
    "....klllssbk....",
    "....klklssbk....",
    "....klklskbk....",
    "....kyllsssbk...",
    ".....kllssbk....",
    ".....kllssbk....",
    ".....kylssbk....",
    "...kkkkkkkkkk...",
    "..kLLLLLLLLLlk..",
    "..klllllllllyk..",
    "...kkkkkkkkkk...",
    "................",
]
# The same, wearing Oinoe's ivy garland (beat 30's errand).
_WOODEN_IMAGE_GARLAND = list(_WOODEN_IMAGE)
_WOODEN_IMAGE_GARLAND[18] = ".kkgvgkkkkgvgkk."
_WOODEN_IMAGE_GARLAND[19] = "...kgvgssgvgk..."
_WOODEN_IMAGE_GARLAND[20] = "....kgvggvgk...."

WOODEN_IMAGE = dict(name="wooden_image", pal="wine", kind="object", fw=16, fh=32,
                    frames=[_WOODEN_IMAGE])
WOODEN_IMAGE_GARLAND = dict(name="wooden_image_garland", pal="wine", kind="object", fw=16, fh=32,
                            frames=[_WOODEN_IMAGE_GARLAND])

# A Prosomime adrift as a mask (beat 32: the masks lift off the actors' faces
# and float into the skene). Its dex colors: marble white, wine-red lips and
# cheek, the violet haze leaking from its eyes, lilac ribbons. Face down it is
# split down the middle, the comic half grinning and the tragic half weeping;
# face up it is the mask's hollow back; face left, its profile. The walk
# frames bob a pixel, so it floats.
_MASK_DOWN = [
    "................",
    "..a..........a..",
    "..akkkkkkkkkka..",
    ".akLLLLLLLLLlka.",
    ".kLLLLLLLLLLLlk.",
    ".kLknkLLLLknkLk.",
    ".kLLLLLLLLnnLlk.",
    ".kLuLLLlLLaLLlk.",
    ".kLkLLLLLLLLkLk.",
    "..kLkkkkkkkkLk..",
    "..kLLknnnkLLlk..",
    "...kLLkkkkLlk...",
    "....kkllllkk....",
    ".....kBnnBk.....",
    "......kBBk......",
    ".......kk.......",
]
_MASK_UP = [
    "................",
    "..a..........a..",
    "..akkkkkkkkkka..",
    ".akllllllllllka.",
    ".klBBBBBBBBBBlk.",
    ".klBnnnnnnnnBlk.",
    ".klBnaaaaaanBlk.",
    ".klBnnnnnnnnBlk.",
    ".klBBnnnnnnBBlk.",
    "..klBBBBBBBBlk..",
    "..kllBBBBBBllk..",
    "...kllBBBBllk...",
    "....kkllllkk....",
    ".....kBnnBk.....",
    "......kBBk......",
    ".......kk.......",
]
_MASK_LEFT = [
    "................",
    "........a.......",
    "......kka.......",
    ".....kLLkaa.....",
    "....kLLLLkka....",
    "...kLnkLLlk.a...",
    "..kLLLLLLlk.....",
    ".kLLLLLLLlk.....",
    "..kkLLLLllk.....",
    "..knkLLLlk......",
    "..kLLLLllk......",
    "...kkLllk.......",
    ".....kBBk.......",
    "......kBnk......",
    ".......kk.......",
    "................",
]


def _bob(rows):
    return ["." * 16] + rows[:-1] if rows[-1] == "." * 16 else rows[1:] + ["." * 16]


MASK = dict(name="mask", pal="wine", kind="object", fw=16, fh=16, anim=True,
            frames=[_MASK_DOWN, _MASK_UP, _MASK_LEFT,
                    _bob(_MASK_DOWN), _MASK_DOWN, _bob(_MASK_UP), _MASK_UP,
                    _bob(_MASK_LEFT), _MASK_LEFT])

# Crows over the Kronia (Manto's errand): four birds wheeling on a 32x32
# frame. Each frame turns the ring a little and moves the wings, so walking in
# place wheels them over one spot and any walk carries them off.
_CROW = {
    "up": ["k.....k", "kk...kk", ".kkykk.", "..kkk..", "...k..."],
    "mid": [".......", ".......", "kkkykkk", ".kkkkk.", "...k..."],
    "down": [".......", ".......", "..kyk..", ".kkkkk.", "kk.k.kk"],
}
_WINGS = ["up", "mid", "down", "mid"]


def _crows(turn, start):
    """Five crows on a tilted ring, turned `turn` radians, wings from `start`."""
    import math
    grid = [["."] * 32 for _ in range(32)]
    for i in range(5):
        ang = turn + i * (2 * math.pi / 5)
        cx = 16 + round(10 * math.cos(ang))
        cy = 15 + round(7 * math.sin(ang))
        for j, row in enumerate(_CROW[_WINGS[(start + i) % 4]]):
            for k, ch in enumerate(row):
                if ch != ".":
                    grid[cy - 3 + j][cx - 3 + k] = ch
    return ["".join(r) for r in grid]


CROWS = dict(name="crows", pal="folk", kind="object", fw=32, fh=32, anim=True,
             frames=[_crows(0.25 * n, n) for n in range(9)])

OBJECTS = [WOODEN_IMAGE, WOODEN_IMAGE_GARLAND, MASK, CROWS]


def all_specs():
    return WALKERS + POSES + OBJECTS


def build(spec):
    if spec.get("kind") == "pose":
        return build_pose_sheet(spec)
    if spec.get("kind") == "object":
        return build_object_sheet(spec)
    return folk_build_sheet(spec)


ORDER = [("down", "stand"), ("up", "stand"), ("left", "stand"),
         ("down", "walk0"), ("down", "walk1"), ("up", "walk0"), ("up", "walk1"),
         ("left", "walk0"), ("left", "walk1")]


def build_pose_sheet(spec):
    pal, legend = PALETTES[spec["pal"]]
    frames = []
    for d, pose in ORDER:
        rows, bottom = spec["frames"][d][pose]
        frames.append(build_frame(rows, bottom + 1 - len(rows), legend, pal, f"{spec['name']} {d} {pose}"))
    return np.hstack(frames)


def build_object_sheet(spec):
    pal, legend = PALETTES[spec["pal"]]
    fw, fh = spec["fw"], spec["fh"]
    out = []
    for n, rows in enumerate(spec["frames"]):
        assert len(rows) == fh, f"{spec['name']} frame {n}: {len(rows)} rows, not {fh}"
        frame = np.zeros((fh, fw), np.int32)
        for y, row in enumerate(rows):
            assert len(row) == fw, f"{spec['name']} frame {n} row {y}: {len(row)} px: {row!r}"
            for x, ch in enumerate(row):
                if ch not in ". ":
                    frame[y, x] = pal[legend[ch]]
        out.append(frame)
    return np.hstack(out)


def palette_of(spec):
    return PALETTES[spec["pal"]][0]


def label_font(size):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow < 10.1
        return ImageFont.load_default()


CONTACT_SHEET = os.path.join(ROOT, "design/phase3/img/sprites_batch1.png")
# The slice's walkers the batch is drawn to match, shown first for scale.
ACT1_REFS = ["kleon", "alethea", "goatherd", "harvester", "elder_f", "acolyte_m"]


def sheet_preview(sheets, specs, k=4, refs=("prof_birch",), lw=40, font_size=18):
    """Every sheet's frames on a grass checker, one row per sheet, the
    reference sheets first for scale, each row labelled with name and palette."""
    rows = []
    for ref in refs:
        if ref == "prof_birch":
            rows.append(("prof_birch", "vanilla", ref_rgba(), W, H))
        else:
            rows.append((ref, "Act I", ref_rgba(os.path.join(PEOPLE_DIR, ref + ".png")), W, H))
    for spec in specs:
        arr = sheets[spec["name"]]
        fw, fh = spec.get("fw", W), spec.get("fh", H)
        rows.append((spec["name"], spec["pal"], to_rgba(arr, palette_of(spec)), fw, fh))
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
    """design/phase3/img/sprites_batch1.png: everything at 2x, after the
    slice's walkers it is drawn to match."""
    return sheet_preview(sheets, all_specs(), k=2, refs=ACT1_REFS, lw=84, font_size=12)


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
        WINE_PAL.write_jasc(WINE_PAL_PATH)
        if not only:
            os.makedirs(os.path.dirname(CONTACT_SHEET), exist_ok=True)
            contact_sheet(sheets).save(CONTACT_SHEET)
    if pv:
        os.makedirs(pv, exist_ok=True)
        sheet_preview(sheets, specs).save(os.path.join(pv, "sprites_act2_sheets.png"))
    if grids:
        os.makedirs(grids, exist_ok=True)
        for spec in specs:
            grid_preview(to_rgba(sheets[spec["name"]], palette_of(spec)), 8).save(
                os.path.join(grids, spec["name"] + "_grid.png"))


if __name__ == "__main__":
    main()
