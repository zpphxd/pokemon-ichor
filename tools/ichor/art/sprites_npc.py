"""Overworld walking sprites for Ichor's NPCs (16x32, 9 frames).

Usage:
    python3 tools/ichor/art/sprites_npc.py [NAME ...] [--write] [--preview DIR]

--write    writes graphics/object_events/pics/people/ichor/<name>.png (144x32,
           4bpp indexed) and the shared palette
           graphics/object_events/palettes/ichor_cast.pal
--preview  writes DIR/sprites_npc_sheets.png (4x, vanilla Birch first for
           scale) and 8x pixel grids for editing

Every sprite in this file shares ONE 16-color palette, CAST_PAL, loaded in
game under OBJ_EVENT_PAL_TAG_ICHOR_CAST. A sheet that needs other colors goes
in its own sprites_npc_<batch>.py with its own palette and tag (see
design/phase1/SPRITES_npc.md).

Sheet layout (same as every Emerald NPC, e.g. prof_birch.png):

    0 face down   1 face up   2 face left
    3 walk down A 4 walk down B
    5 walk up A   6 walk up B
    7 walk left A 8 walk left B

Right-facing frames are the left frames flipped in game.

Each character is drawn as ASCII, one char per pixel. A direction has a `top`
block (head, shared by all its frames) and a `stand` block plus two `walk`
blocks for the body. The stand frame puts `top` at row y0; the walk frames
drop `top` one pixel (the Gen 3 step bob) and use their own body block.
A walk block given as "mirror" is the other walk block flipped.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, Palette, save_indexed, to_rgba, upscale, grid_preview  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

W, H = 16, 32
OUT_DIR = os.path.join(ROOT, "graphics/object_events/pics/people/ichor")
PAL_PATH = os.path.join(ROOT, "graphics/object_events/palettes/ichor_cast.pal")

# --------------------------------------------------------------------------
# The shared "Ichor cast" palette. Ramps are merged across the five cast
# members, so each color is used by several of them. Colors are drawn from
# the trainer portraits (sprites_trainers.py) and the master palette.
# sprites_folk.py draws five trainer-class walkers in this palette too, so a
# change here means re-running sprites_folk.py --write as well.
# --------------------------------------------------------------------------

CAST_COLORS = [
    # char, name, rgb                     used for
    ("k", "ink", (32, 24, 24)),         # outlines, eyes
    ("b", "brown", (88, 48, 32)),       # dark hair, leather, sandals
    ("r", "red_d", (120, 32, 40)),      # crimson / terracotta shadow
    ("u", "umber", (168, 88, 48)),      # terracotta robe, chestnut hair, bronze shadow
    ("c", "crimson", (216, 64, 56)),    # Kleon's cloak, helmet crest
    ("s", "skin_d", (224, 152, 104)),   # skin shadow, terracotta light
    ("S", "skin_l", (248, 208, 168)),   # skin
    ("o", "bronze", (216, 160, 64)),    # bronze, gold, ochre cloth
    ("O", "bronze_l", (248, 216, 112)), # bronze highlight, lamp flame
    ("l", "linen_d", (200, 176, 144)),  # linen shadow, parchment
    ("L", "linen_l", (248, 240, 216)),  # linen, veil, himation
    ("n", "blue_d", (24, 56, 120)),     # Aegean blue shadow
    ("B", "blue", (48, 104, 176)),      # Aegean blue
    ("t", "slate", (72, 64, 96)),       # Titanborn tunic
    ("g", "leaf", (120, 144, 56)),      # laurel
]
CAST_PAL = Palette([(name, rgb) for _, name, rgb in CAST_COLORS])
CAST_LEGEND = {ch: name for ch, name, _ in CAST_COLORS}


# --------------------------------------------------------------------------
# Sheet assembly
# --------------------------------------------------------------------------

def mirror(rows):
    return [r[::-1] for r in rows]


def _place(frame, rows, y, legend, pal, where):
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


def build_frame(top, body, y0, legend, pal, where):
    frame = np.zeros((H, W), np.int32)
    _place(frame, top, y0, legend, pal, where + " top")
    _place(frame, body, y0 + len(top), legend, pal, where + " body")
    return frame


def build_sheet(spec, legend=CAST_LEGEND, pal=CAST_PAL):
    """spec: dict(y0=, down=, up=, left=), each direction a dict(top, stand, walk)."""
    frames = {}
    y0 = spec["y0"]
    for d in ("down", "up", "left"):
        part = spec[d]
        walk = list(part["walk"])
        if walk[1] == "mirror":
            walk[1] = mirror(walk[0])
        if walk[0] == "mirror":
            walk[0] = mirror(walk[1])
        name = spec["name"]
        frames[d] = build_frame(part["top"], part["stand"], y0, legend, pal, f"{name} {d} stand")
        for i in (0, 1):
            frames[f"{d}{i}"] = build_frame(part["top"], walk[i], y0 + 1, legend, pal, f"{name} {d} walk {i}")
    order = ["down", "up", "left", "down0", "down1", "up0", "up1", "left0", "left1"]
    return np.hstack([frames[k] for k in order])


# --------------------------------------------------------------------------
# Kleon: the rival from Lakonia. Crimson chlamys over a linen exomis,
# bronze armband on his right arm, short-cropped dark hair.
# --------------------------------------------------------------------------

KLEON = dict(
    name="kleon",
    y0=11,
    down=dict(
        top=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbSbbSbbSbbk..",
            "..bsSkSSSSkSsb..",
            "..bsSkSSSSkSsb..",
            "...bSSSSSSSSb...",
            "....bssSSssb....",
        ],
        stand=[
            "..kcrkLSSLkrck..",
            ".kcSSLLLLLLSsrk.",
            ".kcoOLLLLLlSsrk.",
            ".kcSsLLLLLlSsrk.",
            ".kcSsbbobbbSsrk.",
            ".kcSSLLLLLlSSrk.",
            ".kcrklLLLLlkrrk.",
            "..kkkSskkSskkk..",
            "....kSskkSsk....",
            "....kbbkkbbk....",
        ],
        walk=[
            [
                "..kcrkLSSLkrck..",
                ".kcSSLLLLLLSsrk.",
                ".kcoOLLLLLlSsrk.",
                ".kcSsLLLLLlSsrk.",
                ".kcSsbbobbbkrrk.",
                ".kcSSLLLLLlkrrk.",
                ".kcrklLLLLlkrrk.",
                "..kkkSskkSskkk..",
                "....kSskkbbk....",
                "....kbbk........",
            ],
            [
                "..kcrkLSSLkrck..",
                ".kcSSLLLLLLSsrk.",
                ".kcoOLLLLLlSsrk.",
                ".kcrkLLLLLlSsrk.",
                ".kcrkbbobbbSsrk.",
                ".kcrkLLLLLlSSrk.",
                ".kcrklLLLLlkrrk.",
                "..kkkSskkSskkk..",
                "....kbbkkSsk....",
                "........kbbk....",
            ],
        ],
    ),
    up=dict(
        top=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..bsbbbbbbbbsb..",
            "..bsbbbbbbbbsb..",
            "...bbbbbbbbbb...",
            "....bbSSSSbb....",
        ],
        stand=[
            "..kccrkSSkrcck..",
            ".kccccrccrccrrk.",
            ".kcccccrcccrrrk.",
            ".kcccccrccrrrrk.",
            ".kccccrcccrrrrk.",
            ".kScccrcccrrrsk.",
            ".krcccrccrrrrrk.",
            "..kkrrrrrrrrkk..",
            "....kSskkSsk....",
            "....kbbkkbbk....",
        ],
        walk=[
            [
                "..kccrkSSkrcck..",
                ".kccccrccrccrrk.",
                ".kcccccrcccrrrk.",
                ".kcccccrccrrrrk.",
                ".kccccrcccrrrrk.",
                ".kScccrcccrrrrk.",
                ".krcccrccrrrrrk.",
                "..kkrrrrrrrrkk..",
                "....kSskkbbk....",
                "....kbbk........",
            ],
            [
                "..kccrkSSkrcck..",
                ".kccccrccrccrrk.",
                ".kcccccrcccrrrk.",
                ".kcccccrccrrrrk.",
                ".kccccrcccrrrrk.",
                ".krcccrcccrrrsk.",
                ".krcccrccrrrrrk.",
                "..kkrrrrrrrrkk..",
                "....kbbkkSsk....",
                "........kbbk....",
            ],
        ],
    ),
    left=dict(
        top=[
            "......kkkkk.....",
            "....kkbbbbbk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbSbSbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbk...",
            "...bsSSSsbbk....",
        ],
        stand=[
            ".....kSSkcck....",
            "....kLLLLkccrk..",
            "....kLoOlkccrk..",
            "....kLSslkcrrk..",
            "....kbSsbkcrrrk.",
            "....kLSSlkcrrrk.",
            "....kLLLlkrrrrk.",
            ".....kSskkrrrk..",
            ".....kSsk.kkk...",
            "....kbbbk.......",
        ],
        walk=[
            [
                ".....kSSkcck....",
                "....kLLLLkccrk..",
                "....kLoOlkccrk..",
                "....kLSslkcrrk..",
                "....kbSsbkcrrrk.",
                "....kLSSlkcrrrk.",
                "....kLLLLlkrrrk.",
                "...kSskkSskrrk..",
                "..kSsk..kSsk....",
                "..kbbk...kbbk...",
            ],
            [
                ".....kSSkcck....",
                "....kLLLLkccrk..",
                "....kLoOlkccrk..",
                "....kLlSskcrrk..",
                "....kbbSskcrrrk.",
                "....kLlSSkcrrrk.",
                "....kLLLlkrrrrk.",
                ".....kSskrrrrk..",
                ".....kSskkkk....",
                "....kbbbk.......",
            ],
        ],
    ),
)

# --------------------------------------------------------------------------
# Professor Daphne: chestnut hair in a bun under a laurel wreath, a floor-
# length Aegean-blue chiton with a white himation over her left shoulder,
# and a scroll in the crook of her left arm.
# --------------------------------------------------------------------------

DAPHNE = dict(
    name="professor_daphne",
    y0=10,
    down=dict(
        top=[
            "......kkkk......",
            ".....kubbuk.....",
            "....kkuuuukk....",
            "...kuuuuuuuuk...",
            "..kguuuuuuuugk..",
            "..kggguuuugggk..",
            "..kugbSSSSbguk..",
            "..kuuSSSSSSuuk..",
            "..kuSkSSSSkSuk..",
            "..kbSkSSSSkSbk..",
            "..kbsSSSSSSsbk..",
            "...kbssSSssbk...",
        ],
        stand=[
            "..kBBBkSSkLLLk..",
            ".kBBBBBBBLLLLlk.",
            ".knBBBBBLLLLlkuk",
            ".kSnBBBLLLLlkLlk",
            ".kSnBBLLLLlSkLlk",
            "..knBLLLlnnkkuk.",
            "..knBBBBnnBnk...",
            "..knBBBBBnBnk...",
            "...kkbbkkbbkk...",
        ],
        walk=[
            [
                "..kBBBkSSkLLLk..",
                ".kBBBBBBBLLLLlk.",
                ".knBBBBBLLLLlkuk",
                ".kSnBBBLLLLlkLlk",
                ".kSnBBLLLLlSkLlk",
                "..knBLLLlnnkkuk.",
                "..knBBBBnnBnk...",
                "..kknBBBnnBnkk..",
                ".....kbbk.......",
            ],
            [
                "..kBBBkSSkLLLk..",
                ".kBBBBBBBLLLLlk.",
                ".knBBBBBLLLLlkuk",
                ".kSnBBBLLLLlkLlk",
                ".kSnBBLLLLlSkLlk",
                "..knBLLLlnnkkuk.",
                "..knBBBBnnBnk...",
                "..kknBBBnnBnkk..",
                "........kbbk....",
            ],
        ],
    ),
    up=dict(
        top=[
            "......kkkk......",
            ".....kuuuuk.....",
            "....kkbuubkk....",
            "...kuuuuuuuuk...",
            "..kguuuuuuuugk..",
            "..kugggggggguk..",
            "..kuuuuuuuuuuk..",
            "..kuuubuuuuuuk..",
            "..kuubuuuubuuk..",
            "..kbuuuuuuuubk..",
            "..kbbuuuuuubbk..",
            "...kbbSSSSbbk...",
        ],
        stand=[
            "..kLLLkSSkBBBk..",
            ".klLLLLBBBBBBnk.",
            ".kLlLLLLBBBBBnk.",
            ".kSlLLLLLBBBnSk.",
            ".kSBlLLLLLBBnSk.",
            "..knBllLLLlBnk..",
            "..knBBBlllBBnk..",
            "..knBBBBBBBBnk..",
            "...kkkkkkkkkk...",
        ],
        walk=[
            [
                "..kLLLkSSkBBBk..",
                ".klLLLLBBBBBBnk.",
                ".kLlLLLLBBBBBnk.",
                ".kSlLLLLLBBBnSk.",
                ".kSBlLLLLLBBnSk.",
                "..knBllLLLlBnk..",
                "..knBBBlllBBnk..",
                "..kknBBBBBBnkk..",
                ".....kbbk.......",
            ],
            [
                "..kLLLkSSkBBBk..",
                ".klLLLLBBBBBBnk.",
                ".kLlLLLLBBBBBnk.",
                ".kSlLLLLLBBBnSk.",
                ".kSBlLLLLLBBnSk.",
                "..knBllLLLlBnk..",
                "..knBBBlllBBnk..",
                "..kknBBBBBBnkk..",
                "........kbbk....",
            ],
        ],
    ),
    left=dict(
        top=[
            "..........kkk...",
            "......kkkkuuuk..",
            "....kkuuuuubbuk.",
            "...kuuuuuuuukk..",
            "..kguuuuuuuuk...",
            "..kggguuuuuuk...",
            "..kSSgguuuuuk...",
            "..kSSSSguuuuk...",
            "..kSkSSSsuuuk...",
            "..kSkSSSSbuk....",
            "..kSSSSSsbuk....",
            "...kbsSssbk.....",
        ],
        stand=[
            "....kBSSkLk.....",
            "...kBBBLLLLk....",
            "..kuLLlkLLlk....",
            "..kullSkLlnk....",
            "...kkkBLLlnk....",
            "...knBBBlnnk....",
            "...knBBBBnBnk...",
            "...knBBBBBnBk...",
            "....kkkbbbkkk...",
        ],
        walk=[
            [
                "....kBSSkLk.....",
                "...kBBBLLLLk....",
                "..kuLLlkLLlk....",
                "..kullSkLlnk....",
                "...kkkBLLlnk....",
                "...knBBBlnnk....",
                "..knBBBBBnBnk...",
                "..kkkBBBBnnBk...",
                "..kbbk..kkkk....",
            ],
            [
                "....kBSSkLk.....",
                "...kBBBLLLLk....",
                "..kuLLlkLLlk....",
                "..kullSkLlnk....",
                "...kkkBLLlnk....",
                "...knBBBlnnk....",
                "...knBBBBnBnk...",
                "...kkBBBBBnkk...",
                "......kkbbbk....",
            ],
        ],
    ),
)


# --------------------------------------------------------------------------
# Alethea: Daphne's apprentice and a digger of ruins. Dark ponytail under a
# blue headband, a sun-gold chiton to the knee, a leather satchel of scrolls
# on her left hip and a small trowel in her right hand.
# --------------------------------------------------------------------------

ALETHEA = dict(
    name="alethea",
    y0=11,
    down=dict(
        top=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbk...",
            "..kBBBBBBBBnnk..",
            "..kbbbbbbbbbbk..",
            "..kbbSSbbSSbbk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "..kbsSSSSSSsbk..",
            "...kbssSSssbk...",
        ],
        stand=[
            "..kokSSSSSSkok..",
            ".kSobooooooooSk.",
            ".kSoobooookLlkk.",
            ".kSooobookbbubk.",
            ".kSkuoobokbuubk.",
            ".kLkuuooobkbbk..",
            ".klkkkkkkkkkkk..",
            "..k.kSskkSsk....",
            "....kbbkkbbk....",
        ],
        walk=[
            [
                "..kokSSSSSSkok..",
                ".kSobooooooooSk.",
                ".kSoobooookLlkk.",
                ".kSooobookbbubk.",
                ".kSkuoobokbuubk.",
                ".kLkuuooobkbbk..",
                ".klkkkkkkkkkkk..",
                "..k.kSskkbbk....",
                "....kbbk........",
            ],
            [
                "..kokSSSSSSkok..",
                ".kSobooooooooSk.",
                ".kSoobooookLlkk.",
                ".kSooobookbbubk.",
                ".kSkuoobokbuubk.",
                ".kLkuuooobkbbk..",
                ".klkkkkkkkkkkk..",
                "..k.kbbkkSsk....",
                "........kbbk....",
            ],
        ],
    ),
    up=dict(
        top=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbuubbbbbk...",
            "..kBBBBBBBBnnk..",
            "..kbbbbBnbbbbk..",
            "..kbbbbuubbbbk..",
            "..kbbbbuubbbbk..",
            "..kbbbbuubbbbk..",
            "..kbbbbuubbbbk..",
            "..kbbbkuubkbbk..",
            "...kSSkuukSSk...",
        ],
        stand=[
            "..kokSSkbkSkok..",
            ".kSooooooobooSk.",
            ".kSoooooobooo" "Sk.",
            ".kbbuooobooooSk.",
            ".kbububooooooSk.",
            ".kbbbuuoooooobk.",
            "..kkkkkkkkkkkk..",
            "....kSskkSsk....",
            "....kbbkkbbk....",
        ],
        walk=[
            [
                "..kokSSkbkSkok..",
                ".kSooooooobooSk.",
                ".kSoooooobooo" "Sk.",
                ".kbbuooobooooSk.",
                ".kbububooooooSk.",
                ".kbbbuuoooooobk.",
                "..kkkkkkkkkkkk..",
                "....kSskkbbk....",
                "....kbbk........",
            ],
            [
                "..kokSSkbkSkok..",
                ".kSooooooobooSk.",
                ".kSoooooobooo" "Sk.",
                ".kbbuooobooooSk.",
                ".kbububooooooSk.",
                ".kbbbuuoooooobk.",
                "..kkkkkkkkkkkk..",
                "....kbbkkSsk....",
                "........kbbk....",
            ],
        ],
    ),
    left=dict(
        top=[
            "......kkkkk.....",
            "....kkbbbbbk....",
            "...kbuubbbbbk...",
            "..kBBBBBBBBBnk..",
            "..kbbbbbbbbbbkk.",
            "..kbSbbbbbbbbbuk",
            "..kSSSSSbbbbkubk",
            "..kSkSSSsbbbkbbk",
            "..kSkSSSSbbbkbk.",
            "..kSSSSSsbbk.kk.",
            "...kbsSssbk.....",
        ],
        stand=[
            "....koSSkok.....",
            "...kooooobok....",
            "...kooSSobuk....",
            "...kLoSsLbbuk...",
            "...kkkSsbuubk...",
            "...kuoooobbk....",
            "....kkkkkkk.....",
            ".....kSskk......",
            "....kbbbk.......",
        ],
        walk=[
            [
                "....koSSkok.....",
                "...kooooobok....",
                "...kooSSobuk....",
                "...kLoSsLbbuk...",
                "...kkkSsbuubk...",
                "...kuoooobbk....",
                "...kkkkkkkk.....",
                "..kSsk.kSsk.....",
                "..kbbk..kbbk....",
            ],
            [
                "....koSSkok.....",
                "...kooooobok....",
                "...koooSSbuk....",
                "...koooSsbbuk...",
                "...koookSsuubk..",
                "...kuooolSbk....",
                "....kkkkkkk.....",
                ".....kSsk.......",
                "....kbbbk.......",
            ],
        ],
    ),
)


# --------------------------------------------------------------------------
# Hierophant Ione, the Hearthkeeper: a cream veil over dark hair, a floor-
# length terracotta robe with a gold hem, and a bronze oil lamp held before
# her in both hands.
# --------------------------------------------------------------------------

IONE = dict(
    name="hierophant_ione",
    y0=10,
    down=dict(
        top=[
            ".....kkkkkk.....",
            "....kLLLLLLk....",
            "...kLLLLLLLlk...",
            "..kLLLLLLLLLlk..",
            "..kLLLLLLLLLlk..",
            "..kLLbbbbbblLk..",
            "..kLbSSSSSSblk..",
            "..kLSSSSSSSSlk..",
            "..kLSkSSSSkSlk..",
            "..kLSkSSSSkSlk..",
            ".kLlsSSSSSSslk..",
            ".kLLlkssssklllk.",
        ],
        stand=[
            ".kLLlsuuuuslllk.",
            ".klLsuuOcuuslk..",
            ".kSSkuoOOokSSk..",
            "..kSkkuoouukSk..",
            "..kusuukkuuurk..",
            "..kssuuuuuurrk..",
            "..ksuuuuuuurrk..",
            "..kooooooooook..",
            "...kkbbkkbbkk...",
        ],
        walk=[
            [
                ".kLLlsuuuuslllk.",
                ".klLsuuOcuuslk..",
                ".kSSkuoOOokSSk..",
                "..kSkkuoouukSk..",
                "..kusuukkuuurk..",
                "..kssuuuuuurrk..",
                "..ksuuuuuuurrk..",
                "..kooooooooook..",
                ".....kbbk.......",
            ],
            [
                ".kLLlsuuuuslllk.",
                ".klLsuuOcuuslk..",
                ".kSSkuoOOokSSk..",
                "..kSkkuoouukSk..",
                "..kusuukkuuurk..",
                "..kssuuuuuurrk..",
                "..ksuuuuuuurrk..",
                "..kooooooooook..",
                "........kbbk....",
            ],
        ],
    ),
    up=dict(
        top=[
            ".....kkkkkk.....",
            "....kLLLLLLk....",
            "...kLLLLLLLlk...",
            "..kLLLLLLLLLlk..",
            "..kLLLLLLLLLlk..",
            "..kLLLLLLLLLlk..",
            "..kLLLLlLLLLlk..",
            "..kLLLLlLLLLlk..",
            "..kLLLLlLLLllk..",
            "..kLLLLlLLLllk..",
            ".kLLLLlLLLLlllk.",
            ".kLLLLlLLLLlllk.",
        ],
        stand=[
            ".ksLLLlLLLlllsk.",
            ".ksuLLlLLlllurk.",
            ".ksukLlLLllkurk.",
            "..ksukLLllkurk..",
            "..ksuukllkuurk..",
            "..ksuuukkuurrk..",
            "..ksuuuuuuurrk..",
            "..kooooooooook..",
            "...kkkkkkkkkk...",
        ],
        walk=[
            [
                ".ksLLLlLLLlllsk.",
                ".ksuLLlLLlllurk.",
                ".ksukLlLLllkurk.",
                "..ksukLLllkurk..",
                "..ksuukllkuurk..",
                "..ksuuukkuurrk..",
                "..ksuuuuuuurrk..",
                "..kooooooooook..",
                ".....kbbk.......",
            ],
            [
                ".ksLLLlLLLlllsk.",
                ".ksuLLlLLlllurk.",
                ".ksukLlLLllkurk.",
                "..ksukLLllkurk..",
                "..ksuukllkuurk..",
                "..ksuuukkuurrk..",
                "..ksuuuuuuurrk..",
                "..kooooooooook..",
                "........kbbk....",
            ],
        ],
    ),
    left=dict(
        top=[
            "......kkkkk.....",
            ".....kLLLLLk....",
            "....kLLLLLLlk...",
            "...kLLLLLLLLlk..",
            "...kLLLLLLLLlk..",
            "..kbbbbLLLLLlk..",
            "..kSSSbLLLLLlk..",
            "..kSSSSbLLLLlk..",
            "..kSkSSbLLLllk..",
            "..kSkSSbLLLllk..",
            "..kSSSsbLLllllk.",
            "...kssbLLLlllk..",
        ],
        stand=[
            "...kOk.kLLlllk..",
            "..kocok.kLlllk..",
            ".kuoOokSSkllk...",
            "..kuookSsuurk...",
            "...kkkuuuuurk...",
            "...ksuuuuuurrk..",
            "...ksuuuuuuurk..",
            "...koooooooook..",
            "....kkkkbbbk....",
        ],
        walk=[
            [
                "...kOk.kLLlllk..",
                "..kocok.kLlllk..",
                ".kuoOokSSkllk...",
                "..kuookSsuurk...",
                "...kkkuuuuurk...",
                "...ksuuuuuurrk..",
                "..ksuuuuuuuurk..",
                "..kkoooooooook..",
                "..kbbk..kkkk....",
            ],
            [
                "...kOk.kLLlllk..",
                "..kocok.kLlllk..",
                ".kuoOokSSkllk...",
                "..kuookSsuurk...",
                "...kkkuuuuurk...",
                "...ksuuuuuurrk..",
                "...ksuuuuuuurk..",
                "...kkoooooooook.",
                "......kkkbbbk...",
            ],
        ],
    ),
)


# --------------------------------------------------------------------------
# Titanborn grunt: a bronze Corinthian helmet with a crimson crest and a
# T-shaped face opening, a dark slate tunic with a bronze sickle emblem,
# bronze greaves.
# --------------------------------------------------------------------------

GRUNT = dict(
    name="titan_grunt",
    y0=10,
    down=dict(
        top=[
            "......kkkk......",
            ".....kccrrk.....",
            "....kccccrrk....",
            "...kkkrrrrkkk...",
            "..kOOOoooooouk..",
            "..kOoooooooouk..",
            "..koooooooooouk.",
            "..kokckookckuk..",
            "..kooookkooouk..",
            "..kooookkooouk..",
            "...kuookkouuk...",
            "....kkkkkkkk....",
        ],
        stand=[
            "..kotkSSSSktok..",
            ".kSoottttttoosk.",
            ".kSkttttOtttksk.",
            ".kSkttOOttttksk.",
            ".kSkbbbobbbbksk.",
            ".kSktttttttttkk.",
            "..kkttttttttkk..",
            "....kookkouk....",
            "....kbbkkbbk....",
        ],
        walk=[
            [
                "..kotkSSSSktok..",
                ".kSoottttttoosk.",
                ".kSkttttOtttksk.",
                ".kSkttOOttttksk.",
                ".kSkbbbobbbbkkk.",
                ".kSkttttttttkk..",
                "..kkttttttttkk..",
                "....kookkbbk....",
                "....kbbk........",
            ],
            [
                "..kotkSSSSktok..",
                ".kSoottttttoosk.",
                ".kSkttttOtttksk.",
                ".kSkttOOttttksk.",
                ".kkkbbbobbbbksk.",
                "..kkttttttttksk.",
                "..kkttttttttkk..",
                "....kbbkkouk....",
                "........kbbk....",
            ],
        ],
    ),
    up=dict(
        top=[
            "......kkkk......",
            ".....kccrrk.....",
            "....kccccrrk....",
            "...kkcccrrrkk...",
            "..kOOkccrrkouk..",
            "..kOoookrkooouk.",
            "..koooooooooouk.",
            "..koooooooooouk.",
            "..koooooooooouk.",
            "..kuooooooooouk.",
            "...kuuuuuuuuk...",
            "....kkSSSSkk....",
        ],
        stand=[
            "..kotkkkkkktok..",
            ".kSoottttttoosk.",
            ".kSkttttttttksk.",
            ".kSkttttttttksk.",
            ".kSkbbbbbbbbksk.",
            ".kSkttttttttkkk.",
            "..kkttttttttkk..",
            "....kookkouk....",
            "....kbbkkbbk....",
        ],
        walk=[
            [
                "..kotkkkkkktok..",
                ".kSoottttttoosk.",
                ".kSkttttttttksk.",
                ".kSkttttttttksk.",
                ".kSkbbbbbbbbkkk.",
                ".kSkttttttttkk..",
                "..kkttttttttkk..",
                "....kookkbbk....",
                "....kbbk........",
            ],
            [
                "..kotkkkkkktok..",
                ".kSoottttttoosk.",
                ".kSkttttttttksk.",
                ".kSkttttttttksk.",
                ".kkkbbbbbbbbksk.",
                "..kkttttttttksk.",
                "..kkttttttttkk..",
                "....kbbkkouk....",
                "........kbbk....",
            ],
        ],
    ),
    left=dict(
        top=[
            "......kkkk......",
            ".....kccrrk.....",
            "....kccccrrk....",
            "...kkcccrrrrk...",
            "..kOOkkkkkkkuk..",
            "..kOOooooooouuk.",
            "..kOooooooooouk.",
            "..kokckooooooouk",
            "..kokkooooooouk.",
            "..kokoooooooukk.",
            "...kkoooooouuk..",
            "....kkkkkkkkk...",
        ],
        stand=[
            ".....kSSkotk....",
            "....kttttook....",
            "....kSSOttok....",
            "....kSsttttk....",
            "....kbSsbbbk....",
            "....ktttttttk...",
            ".....ktttttk....",
            ".....kookk......",
            "....kbbbk.......",
        ],
        walk=[
            [
                ".....kSSkotk....",
                "....kttttook....",
                "....kSSOttok....",
                "....kSsttttk....",
                "....kbSsbbbk....",
                "....ktttttttk...",
                "....kttttttk....",
                "...kook.kouk....",
                "..kbbk...kbbk...",
            ],
            [
                ".....kSSkotk....",
                "....kttttook....",
                "....ktSSOtok....",
                "....kttSsttk....",
                "....kbbSsbbk....",
                "....ktttttttk...",
                ".....ktttttk....",
                ".....kookk......",
                "....kbbbk.......",
            ],
        ],
    ),
)


CAST = {
    "kleon": KLEON,
    "professor_daphne": DAPHNE,
    "alethea": ALETHEA,
    "hierophant_ione": IONE,
    "titan_grunt": GRUNT,
}


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def checker_bg(w, h, a=(176, 200, 152), b=(168, 192, 144)):
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(0, h, 8):
        for x in range(0, w, 8):
            d.rectangle([x, y, x + 7, y + 7], fill=(a if (x // 8 + y // 8) % 2 == 0 else b) + (255,))
    return im


REF_SHEET = os.path.join(ROOT, "graphics/object_events/pics/people/prof_birch.png")


def ref_rgba(path=REF_SHEET):
    """A vanilla sheet as RGBA with color 0 cleared, shown first for scale."""
    im = Image.open(path)
    idx = np.array(im)
    rgba = np.array(im.convert("RGBA"))
    rgba[idx == 0, 3] = 0
    return Image.fromarray(rgba, "RGBA")


def sheet_preview(sheets, pal=CAST_PAL, k=4, ref=True):
    """All sheets stacked (vanilla Birch first, for scale), each frame on a
    grass checker, upscaled k times."""
    rows = ([ref_rgba()] if ref else []) + [to_rgba(arr, pal) for arr in sheets.values()]
    pad = 4
    w = W * 9 + pad * 8
    h = (H + pad) * len(rows) - pad
    out = Image.new("RGBA", (w, h), (232, 224, 200, 255))
    for i, im in enumerate(rows):
        for f in range(9):
            tile = checker_bg(W, H)
            tile.alpha_composite(im.crop((f * W, 0, (f + 1) * W, H)))
            out.alpha_composite(tile, (f * (W + pad), i * (H + pad)))
    return upscale(out, k)


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    write = "--write" in args
    only = [a for a in args if a in CAST]
    sheets = {}
    for name, spec in CAST.items():
        if only and name not in only:
            continue
        sheets[name] = build_sheet(spec)
    if write:
        os.makedirs(OUT_DIR, exist_ok=True)
        for name, arr in sheets.items():
            save_indexed(arr, CAST_PAL, os.path.join(OUT_DIR, name + ".png"))
        CAST_PAL.write_jasc(PAL_PATH)
    if pv:
        os.makedirs(pv, exist_ok=True)
        sheet_preview(sheets).save(os.path.join(pv, "sprites_npc_sheets.png"))
        for name, arr in sheets.items():
            grid_preview(to_rgba(arr, CAST_PAL), 8).save(os.path.join(pv, name + "_grid.png"))


if __name__ == "__main__":
    main()
