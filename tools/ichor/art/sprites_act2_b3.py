"""Overworld walkers, poses and field objects for Act II, batch 3 (Arkadia).

Usage:
    python3 tools/ichor/art/sprites_act2_b3.py [NAME ...] [--write] [--preview DIR] [--grids DIR]

--write    writes graphics/object_events/pics/people/ichor/<name>.png (people)
           and graphics/object_events/pics/misc/ichor/<name>.png (objects)
--preview  writes DIR/sprites_act2_b3_sheets.png (every frame at 4x, labelled)
--grids    writes DIR/<name>_grid.png, 8x pixel grids for editing

The house style is the slice's and batch 1's (sprites_folk.py,
sprites_act2.py): 16x32 frames, nine to a sheet, feet on row 30, a 1 px step
bob, right = left mirrored. See design/phase3/SPRITES.md, "Batch 3".

No new palette tag. Every sheet uses one of three existing families:

* folk (OBJ_EVENT_PAL_TAG_ICHOR_FOLK): the Huntress, the Charcoaler, Kallisto,
  Phylonoe, the muleteer with the goad, the lamplighter and the temple hounds.
* cast (OBJ_EVENT_PAL_TAG_ICHOR_CAST): Kleon on his stump and his row of balls.
* theoxenia (OBJ_EVENT_PAL_TAG_ICHOR_THEOXENIA): the golden hind, for the
  palette's true gold and chestnut. It is the goddess's own animal.

Some sheets carry frames past the standard nine, played by their own
animation tables in src/data/object_events/object_event_anims.h:

* kallisto: 9 seated on the rock looking at the sky, 10 looking down.
* kleon_stump: 9 rising, 10 standing (facing down).
* temple_hound: 9 asleep, curled; 10 the same with an ear up.
* golden_hind: 9-11 grazing (down, up, left); 0-2 her head up.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, to_rgba, save_indexed, grid_preview  # noqa: E402
from sprites_folk import ARCHETYPES, PALETTES, pole, _with, build_frame  # noqa: E402
from sprites_folk import build_sheet as folk_build_sheet  # noqa: E402
import sprites_act2 as b1  # noqa: E402  (registers batch 1's archetypes and the wine palette)
from sprites_act2 import _BLANK3, _flip, sheet_preview  # noqa: E402
from sprites_npc import KLEON  # noqa: E402
import sprites_npc_theoxenia as theox  # noqa: E402

W, H = 16, 32
FEET_ROW = 30
PEOPLE_DIR = os.path.join(ROOT, "graphics/object_events/pics/people/ichor")
MISC_DIR = os.path.join(ROOT, "graphics/object_events/pics/misc/ichor")
CONTACT_SHEET = os.path.join(ROOT, "design/phase3/img/sprites_batch3.png")
# The slice's and batch 1's walkers the batch is drawn to match, for scale.
REFS = ["kleon", "youth_f", "harvester", "kid_f", "maenad", "herald"]

PALETTES["theoxenia"] = (theox.PAL, theox.LEGEND)

# --------------------------------------------------------------------------
# A tall tunic: the slice's tunic with one more row of shin (Kallisto).
# --------------------------------------------------------------------------

_T = ARCHETYPES["tunic"]
_TT_DOWN = _T["down"]["stand"][:9] + ["....kXYkkXYk....", "....kFFkkFFk...."]
_TT_UP = _with(_TT_DOWN, {0: "...kCCCCCCCQk..."})
_TT_LEFT = _T["left"]["stand"][:9] + [".....kXYk.......", "....kFFFk......."]
_TT_HANDS_W0 = {5: "..kSSCCCCCQkk...", 6: "..kkCCCCCCCQk..."}
_TT_HANDS_W1 = {5: "...kkCCCCCQSSk..", 6: "...kCCCCCCCQkk.."}


def _front_tt(stand):
    return dict(stand=stand,
                walk0=_with(stand, {**_TT_HANDS_W0, 9: "....kXYkkFFk....", 10: "....kFFk........"}),
                walk1=_with(stand, {**_TT_HANDS_W1, 9: "....kFFkkXYk....", 10: "........kFFk...."}))


ARCHETYPES["tunic_tall"] = dict(
    down=_front_tt(_TT_DOWN),
    up=_front_tt(_TT_UP),
    left=dict(stand=_TT_LEFT,
              walk0=_with(_TT_LEFT, {2: "....kCCSsCQk....", 3: "....kCCSsCQk....",
                                     4: "....kTTSsTTk....", 5: "....kCCSSCQk....",
                                     7: "...kXYkkkYYk....", 8: "..kXYk...kYYk...",
                                     9: "..kXYk...kYYk...", 10: "..kFFk....kFFk.."}),
              walk1=_with(_TT_LEFT, {2: "....kSsCCCQk....", 3: "....kSsCCCQk....",
                                     4: "....kSsTTTTk....", 5: "....kSSCCCQk....",
                                     7: "...kYYkkkXYk....", 8: "..kYYk...kXYk...",
                                     9: "..kYYk...kXYk...", 10: "..kFFk....kFFk.."})),
)

# A child's robe to the ankles (Phylonoe's krokotos).
_KR_DOWN = _with(ARCHETYPES["kid"]["down"]["stand"], {5: "...kCCCCCCCQk...", 6: "...kkFFkkFFkk..."})
_KR_UP = _with(_KR_DOWN, {0: "....kkCCCCkk...."})
_KR_LEFT = _with(ARCHETYPES["kid"]["left"]["stand"], {5: "...kCCCCCQk.....", 6: "...kFFkkkk......"})


def _front_kr(stand):
    return dict(stand=stand,
                walk0=_with(stand, {6: "...kkFFkkkkkk..."}),
                walk1=_with(stand, {6: "...kkkkkkFFkk..."}))


ARCHETYPES["kid_robe"] = dict(
    down=_front_kr(_KR_DOWN),
    up=_front_kr(_KR_UP),
    left=dict(stand=_KR_LEFT,
              walk0=_with(_KR_LEFT, {2: "....kCCSsQk.....", 3: "....kCCSsQk.....",
                                     5: "..kCCCCCCQk.....", 6: "..kFFkkkFFk....."}),
              walk1=_with(_KR_LEFT, {2: "....kSsCCQk.....", 3: "....kSsCCQk.....",
                                     6: "...kFFkkkk......"})),
)


# ==========================================================================
# Folk palette: Arkadia's people
# ==========================================================================

# HUNTRESS (Euadne, Auge, Artemis's acolytes): a short saffron chiton girt
# high, knee boots for the hill paths, hair bound up in a knot, a fawnskin
# over her left shoulder, the quiver on her back and her bow held low in her
# left hand.
_BOW_R = ["_k_", "_bk", "__b", "__b", "__b", "__b", "__b", "__b", "_bk", "_k_"]
HUNTRESS = dict(
    name="huntress", pal="folk", arch="tunic",
    roles=dict(C="O", Q="o", T="u", F="b", X="u", Y="b"),
    head=dict(
        down=[
            "......kkkk......",
            ".....kbuubk.....",
            "....kkbbbbkk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbSbbSbbSbbk..",
            "..bsSkSSSSkSsb..",
            "..bsSkSSSSkSsb..",
            "...bSSSSSSSSb...",
            "....bssSSssb....",
        ],
        up=[
            "......kkkk......",
            ".....kbuubk.....",
            "....kkbbbbkk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk.k",
            "..ksbbbbbbbbskLk",
            "...kbbbbbbbbkLuk",
            "....kbSSSSbkkuk.",
        ],
        left=[
            ".......kkkk.....",
            "......kbuubk....",
            "....kkkbbbbk....",
            "...kbuubbbbbk...",
            "..kbubbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbbbkk.",
            "..kSkSSSssbbbkLk",
            "..kSkSSSSbbbkLuk",
            "...bsSSSsbbkkuk.",
        ],
    ),
    over=dict(
        down={"all": [(9, ["_k______________", "kLk_____________"]),
                      ("b0", ["kuk______lll____", "_k______lLll____", "_______llLl_____",
                              "______lLll______", "_____bllb_______"]),
                      pole(13, "b0", _BOW_R)]},
        up={"all": [("b0", ["____lll_____kuk_", "_____ll____kuuk_", "__________kuuk__",
                            "_________kuuk___", "________kubk____", "_________kk_____"]),
                    pole(0, "b0", _flip(_BOW_R))]},
        left={"all": [("b0", ["__________kuk___", "___________uuk__", "__________kuuk__",
                              "__________kubk__", "___________kk___"]),
                      ("b0", ["_____lLl________", "____llLl________", "_____lll________"]),
                      pole(2, "b1", ["_k_", "kbk", "kb_", "kb_", "kb_", "kb_", "kb_", "kbk", "_k_"])]},
    ),
)

# CHARCOALER (Hippothoos, Agapenor, the kiln men): a stocky man in a soot-gray
# tunic and a sooty felt cap, a tan leather apron, arms black to the elbows, a
# short beard, and the long iron rake over his shoulder.
_RAKE_DOWN = (0, ["_________kkkkkkk", "_________kykykyk", "_________k_k_kyk"] + ["_____________kyk"] * 15
              + ["_____________kkk"])
CHARCOALER = dict(
    name="charcoaler", pal="folk", arch="tunic",
    roles=dict(C="y", Q="b", T="b", F="b"),
    head=dict(
        down=_BLANK3 + [
            ".....kkkkkk.....",
            "....kyyyyyyk....",
            "...kyyyyyybyk...",
            "..kyyyyyyyyyyk..",
            "..kyyyyyyyyyyk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kbSSSSSSySbk..",
            "..kbbbSSSSbbbk..",
            "...kbbbbbbbbk...",
            "....kbbbbbbk....",
        ],
        up=_BLANK3 + [
            ".....kkkkkk.....",
            "....kyyyyyyk....",
            "...kybyyyyyyk...",
            "..kyyyyyyyyyyk..",
            "..kyyyyyyyyyyk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..ksbbbbbbbbsk..",
            "..ksbbbbbbbbsk..",
            "...kbbSSSSbbk...",
            "....kbSSSSbk....",
        ],
        left=_BLANK3 + [
            "......kkkkk.....",
            "....kkyyyyyk....",
            "...kyyyyyyyyk...",
            "..kyyyyyyyyyyk..",
            "..kyyyyyyyyyyk..",
            "..kSSSSSbbbbbk..",
            "..kSkSSSbsbbbk..",
            "..kSSSySbbbbbk..",
            "..kbbbSbbbbbk...",
            "...kbbbbbbbk....",
            "....kbbbbbk.....",
        ],
    ),
    over=dict(
        down={"all": [_RAKE_DOWN,
                      ("b1", ["______llll______", "_____llllly_____", "_____llllly_____",
                              "_____llllly_____", "_____llllly_____", "_____llllly_____"]),
                      ("b3", ["___bb______bb___", "___kk______kk___"])],
              "stand": [("b5", ["___kk______kk___"])],
              "walk0": [("b5", ["___kk___________"])],
              "walk1": [("b5", ["___________kk___"])]},
        up={"all": [(0, [r[::-1] for r in _RAKE_DOWN[1]]),
                    ("b3", ["___bb______bb___", "___kk______kk___"])],
            "stand": [("b5", ["___kk______kk___"])],
            "walk0": [("b5", ["___kk___________"])],
            "walk1": [("b5", ["___________kk___"])]},
        left={"all": [_RAKE_DOWN,
                      ("b1", ["____kll_________", "___kll__________", "___kll__________",
                              "___kll__________", "___kll__________", "____kl__________"])],
              "stand": [("b4", ["______kk________", "______kk________"])],
              "walk0": [("b4", ["_______kk_______", "_______kk_______"])],
              "walk1": [("b4", ["_____kk_________", "_____kk_________"])]},
    ),
)

# MULETEER_GOAD, the muleteer of Nonakris (Route 11, Styx Falls; batch 2's
# MULETEER is Kirrha's): a lean mountain man in a peaked felt pilos, a dusty
# russet tunic under a short goat-hair cape, wrapped shins, and the long goad
# he walks his mules with (a cornel stick with an iron prick).
_GOAD = ["_k", "ky", "_k"] + ["kb"] * 21
_PILOS = [
    ".......kk.......",
    "......kobk......",
    ".....koobbk.....",
    "....koooobbk....",
    "...koooooobbk...",
]
MULETEER_GOAD = dict(
    name="muleteer_goad", pal="folk", arch="tunic",
    roles=dict(C="u", Q="b", T="b", F="b", X="l", Y="y"),
    head=dict(
        down=_BLANK3 + _PILOS + [
            "..kbboooooobbk..",
            "...kSSSSSSSSk...",
            "...kSkSSSSkSk...",
            "...kSkSSSSkSk...",
            "...kbSSssSSbk...",
            "....kbbbbbbk....",
        ],
        up=_BLANK3 + _PILOS + [
            "..kbboooooobbk..",
            "...kbbbbbbbbk...",
            "...kbbbbbbbbk...",
            "...kbbbbbbbbk...",
            "...kbbSSSSbbk...",
            "....kbSSSSbk....",
        ],
        left=_BLANK3 + [r[1:] + "." for r in _PILOS] + [
            "..kbooooobbbk...",
            "..kSSSSSbsbbk...",
            "..kSkSSSsbbbk...",
            "..kSkSSSSbbk....",
            "..kbSSssbbk.....",
            "...kbbbbbk......",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["..kyyy____yyyk..", ".kyyby____ybyyk.", ".kybyk____kbyyk.",
                              "..kk________kk.."]),
                      pole(0, 0, _GOAD)]},
        up={"all": [("b0", ["..kyyyyyyyyyyk..", ".kyybyyybyyybyk.", ".kybyyybyyybyyk.",
                            "..kkykkykkykkk.."]),
                    pole(14, 0, _flip(_GOAD))]},
        left={"all": [("b0", ["_______kyyk_____", "______kyybyk____", "______kybyyk____",
                              "_______kkkk_____"]),
                      pole(1, 0, _GOAD)]},
    ),
)

# The LAMPLIGHTER of Arkadia: dark curls, an olive tunic, a clay oil flask at
# his belt, and a long pole with a lit taper at its head. The lamp-trees light
# as he passes.
_TAPER = ["_k_", "kOk", "kuk", "_k_", "_bk"] + ["_bk"] * 17
LAMPLIGHTER = dict(
    name="lamplighter", pal="folk", arch="tunic",
    roles=dict(C="g", Q="v", T="b", F="b"),
    head=dict(
        down=_BLANK3 + [
            "....kk.kk.kk....",
            "...kbbkbbkbbk...",
            "..kbubbbbbbbbk..",
            "..kbbbbbubbbbk..",
            "..kbSbbSbbSbbk..",
            "..bsSkSSSSkSsb..",
            "..bsSkSSSSkSsb..",
            "...bSSSSSSSSb...",
            "....bssSSssb....",
        ],
        up=_BLANK3 + [
            "....kk.kk.kk....",
            "...kbbkbbkbbk...",
            "..kbubbbbbbbbk..",
            "..kbbbbbubbbbk..",
            "..kbbbbbbbbbbk..",
            "..bsbbbbbbbbsb..",
            "..bsbbbbbbbbsb..",
            "...bbbbbbbbbb...",
            "....bbSSSSbb....",
        ],
        left=_BLANK3 + [
            ".....kk.kk.kk...",
            "....kbbkbbkbbk..",
            "...kbubbbbbbbbk.",
            "..kbbbbbbubbbbk.",
            "..kbSbbbbbbbbbk.",
            "..kSSSSSbsbbbbk.",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbk...",
            "...bsSSSsbbk....",
        ],
    ),
    over=dict(
        down={"all": [pole(12, 0, _TAPER), ("b4", ["____kuk_________", "____kuk_________",
                                                    "_____k__________"])]},
        up={"all": [pole(1, 0, _flip(_TAPER))]},
        left={"all": [pole(1, 0, _TAPER), ("b4", ["_________kuk____", "_________kuk____",
                                                   "__________k_____"])]},
    ),
)

# PHYLONOE, the temple's guide: a girl of nine, one of Artemis's little bears.
# A saffron robe to her ankles and a little bear-ear cap of brown fur over
# auburn hair.
PHYLONOE = dict(
    name="phylonoe", pal="folk", arch="kid_robe",
    roles=dict(C="O", Q="o", T="O", F="s"),
    head=dict(
        down=[
            "..kkk......kkk..",
            ".kbubk....kbubk.",
            ".kbbbkkkkkkbbbk.",
            "..kkbbbbbbbbkk..",
            "..kbbbbbbbbbbk..",
            ".kuuuSuuuuSuuuk.",
            ".kuSSkSSSSkSSuk.",
            "..kSSkSSSSkSSk..",
            "...kusSSSSsuk...",
            "....kussssuk....",
        ],
        up=[
            "..kkk......kkk..",
            ".kbbbk....kbbbk.",
            ".kbbbkkkkkkbbbk.",
            "..kkbbbbbbbbkk..",
            "..kbbbbbbbbbbk..",
            ".kubbbbbbbbbbuk.",
            ".kuuuuuuuuuuuuk.",
            "..kuuuuuuuuuuk..",
            "...kuuuuuuuuk...",
            "....kuSSSSuk....",
        ],
        left=[
            "....kkk...kkk...",
            "...kbubk.kbbbk..",
            "...kbbbkkkbbbk..",
            "...kkbbbbbbbkk..",
            "...kbbbbbbbbbk..",
            "...kuuSuuuuuuuk.",
            "...kSSSSuuuuuuk.",
            "...kSkSSSuuuuk..",
            "...ksSSSsuuuk...",
            "....kssssuuk....",
        ],
    ),
)


# ==========================================================================
# Kallisto (theoxenia palette): the Hierophant of Artemis
# ==========================================================================
#
# Tall and very still: a short silver-gray chiton girt for running, a dark
# bearskin over her left shoulder pinned with a silver crescent, dark hair in
# one long braid over her right shoulder, and the bow she never draws slung
# across her back. Drawn in the theoxenia palette (true linen gray, dark wool
# for the bearskin), like the golden hind she keeps.
#
# Frames 9 and 10 sit her on the moonlit rock, knees drawn up and her arms
# round them (sAnimTable_IchorKallisto): 9, face tipped up to the sky; 10,
# looking down at you.

KALLISTO = dict(
    name="kallisto", pal="theoxenia", arch="tunic_tall",
    roles=dict(C="w", Q="g", T="h", F="h"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....khhhhhhk....",
            "...khHHhhhhhk...",
            "..khHhhhhhhhhk..",
            "..khhhhhhhhhhk..",
            "..khShhhhhhShk..",
            "..khSSSSSSSShk..",
            "..khSkSSSSkShk..",
            "..khSkSSSSkShk.k",
            "..khsSSSSSSshkk.",
            "...khhsSSsshkHk.",
        ],
        up=[
            ".....kkkkkk.....",
            "....khhhhhhk....",
            "...khHHhhhhhk...",
            "..khHhhhhhhhhk..",
            "..khhhhhhhhhhk..",
            "..khhhhhhhhhhk..",
            "..khhhhhhhhhhk..",
            "..khhhhhhhhhhk..",
            "..kShhhhhhhhhk..",
            "...kShhhhhHhk...",
            "....kSSShHhk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkhhhhhk....",
            "...khHHhhhhhk...",
            "..khHhhhhhhhhk..",
            "..khhhhhhhhhhk..",
            "..khShhhhhhhhk..",
            "..kSSSSShshhhk..",
            "..kSkSSSShhhhk..",
            "..kSkSSSShhhhk..",
            "..kSSSSSshhHhk..",
            "...ksSSsshHhk...",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["__khH_____Wddk__", "__kHh_____dkddk_", "__khH_____ddkdk_",
                              "__kHh_____dkddk_", "__kWk_____ddddk_", "___________kdk__",
                              "kH______________", "_k______________"])]},
        up={"all": [("b0", ["__kddd____Hh____", "_kdkdd__________", "_kddkdH_________",
                            "_kdkdd_H________", "__kddd__H_______", "___kk____H______",
                            "__________H_____", "___________k____"])]},
        left={"all": [("b0", ["______Wddk__hH__", "_____kdkddk_____", "_____kddkdk_____",
                              "_____kdkddk_____", "______kddk______"]),
                      ("b0", ["___________kH___", "___________kH___", "____________H___",
                              "____________Hk__", "____________k___"])]},
    ),
)

# Seated on the rock: shoulders, the knees drawn up with her arms round her
# shins, the chiton's hem and the bearskin spread on the stone either side.
_KALLISTO_SEAT_BODY = [
    "..kddkSSSSkddk..",
    ".kdSkkwwkkwwkdk.",
    ".kdSkwwwkkwwgkdk",
    ".kdSkwwgkkwggkdk",
    ".kdSSkkkkkkkSSdk",
    ".kdkSSSSSSSSSSdk",
    "kddkkSskkSskkkdk",
    "kdddkhhkkhhkdddk",
    ".kkkkkkkkkkkkkk.",
]
_KALLISTO_SKY = [
    ".....kkkkkk.....",
    "....khhhhhhk....",
    "...khHHhhhhhk...",
    "..khHhhhhhhhhk..",
    "..khSkSSSSkShk..",
    "..khSSSSSSSShk..",
    "..khSSSSSSSShk..",
    "..khsSSssSSshk..",
    "...khSSSSSShk...",
    "....kksSSskk....",
]
_KALLISTO_LOOK = [
    ".....kkkkkk.....",
    "....khhhhhhk....",
    "...khHHhhhhhk...",
    "..khHhhhhhhhhk..",
    "..khhhhhhhhhhk..",
    "..khShhhhhhShk..",
    "..khSSSSSSSShk..",
    "..khSkSSSSkShk..",
    "...khsSSSSshk...",
    "....kksSSskk....",
]
KALLISTO["extra"] = [(_KALLISTO_SKY + _KALLISTO_SEAT_BODY, FEET_ROW),
                     (_KALLISTO_LOOK + _KALLISTO_SEAT_BODY, FEET_ROW)]

# Part 10's named folk, as recolors of the slice's walkers (no new shapes).
# MNASEAS, keeper of the Pool of Mnemosyne: the elder man in a himation of
# poplar white (linen shaded gray, so his white hair and beard still read).
from sprites_folk import ELDER_M  # noqa: E402
MNASEAS = dict(ELDER_M, name="mnaseas", roles=dict(C="l", Q="y", T="l", F="b"))

WALKERS = [HUNTRESS, CHARCOALER, KALLISTO, PHYLONOE, MULETEER_GOAD, LAMPLIGHTER, MNASEAS]


# ==========================================================================
# Kleon on the stump (cast palette): a pose sheet
# ==========================================================================
#
# Beat 42: Kleon sits low on a cypress stump in the Cypress Wood, elbows on his
# knees, head down. The stump is the map's (a metatile); his seat is about
# 5 px above the tile's bottom. Facing picks the view (down: his front, head
# bowed; up: his back; left/right: profile). Walking in place he hangs his
# head lower and lifts it. Frames 9 and 10 are his rise, played by
# nurse_joy_bow (sAnimTable_IchorStump): half up, then standing facing down in
# his ordinary look. After it, swap him to OBJ_EVENT_GFX_ICHOR_KLEON.

_KLEON_TOP = {d: KLEON[d]["top"] for d in ("down", "up", "left")}

_STUMP_HEAD_DOWN = [
    ".....kkkkkk.....",
    "....kbbbbbbk....",
    "...kbuubbbbbk...",
    "..kbubbbbbbbbk..",
    "..kbbbbbbbbbbk..",
    "..kbbbbbbbbbbk..",
    "..kbSbbSbbSbbk..",
    "..bsSsSSSSsSsb..",
    "...bSSSSSSSSb...",
]
_STUMP_BODY_DOWN = [
    "..kcrkLSSLkrck..",
    ".kcSSkLLLLkSSck.",
    ".kcSskLLLLkSsck.",
    ".kkSSSkLLkSSSkk.",
    ".kLLkSSkkSSkLLk.",
    ".kLLLkSSSSkLLLk.",
    "..kSskkkkkkkSsk.",
    "..kSsk....kSsk..",
    "..kbbk....kbbk..",
]
_STUMP_SAG_DOWN = ["................"] + _STUMP_HEAD_DOWN + _STUMP_BODY_DOWN[1:]
_STUMP_UP = [
    ".....kkkkkk.....",
    "....kbbbbbbk....",
    "...kbuubbbbbk...",
    "..kbubbbbbbbbk..",
    "..kbbbbbbbbbbk..",
    "..kbbbbbbbbbbk..",
    "..kbbbbbbbbbbk..",
    "..kkbbbbbbbbkk..",
    ".kccrkSSSSkrcck.",
    ".kcccrccccrrrck.",
    ".kccccrccrrrrrk.",
    ".kScccrccrrrrsk.",
    ".kkccrccrrrrrkk.",
    "..kkrrrrrrrrkk..",
    "...kbbk..kbbk...",
]
_STUMP_SAG_UP = ["................"] + _STUMP_UP[:8] + _STUMP_UP[9:]
_STUMP_LEFT = [
    "......kkkkk.....",
    "....kkbbbbbk....",
    "...kbuubbbbbk...",
    "..kbubbbbbbbbk..",
    "..kbbbbbbbbbbk..",
    "..kSbbbbbbbbbk..",
    "..kSSSbsbbbbk...",
    "...kSSssbbbkck..",
    "....kkLLLkccrk..",
    "..kkSSSkLkcrrk..",
    ".kSSkLLLLLkrrk..",
    ".kLLLLLLLLkrk...",
    ".kSskkkkkkkk....",
    ".kSsk...........",
    "kbbbk...........",
]
_STUMP_SAG_LEFT = ["................"] + _STUMP_LEFT[:8] + _STUMP_LEFT[9:]
# Frame 9: half up, hands on his knees, head lifting to the player.
_STUMP_RISE = _KLEON_TOP["down"] + [
    "..kcrkLSSLkrck..",
    ".kcSSLLLLLLSsrk.",
    ".kcSkLLLLLLkSrk.",
    ".kckSSLLLLSSkrk.",
    ".kcrkSSkkSSkrrk.",
    ".kkkLLLkkLLLkkk.",
    "...kSsk..kSsk...",
    "...kbbk..kbbk...",
]


def _kleon_frame0():
    """Kleon's own standing frame, facing down, for the end of his rise."""
    from sprites_npc import build_sheet as npc_build_sheet
    return npc_build_sheet(KLEON)[:, :W]


KLEON_STUMP = dict(
    name="kleon_stump", pal="cast", kind="pose",
    frames=dict(
        down=dict(stand=(_STUMP_HEAD_DOWN + _STUMP_BODY_DOWN, FEET_ROW),
                  walk0=(_STUMP_SAG_DOWN, FEET_ROW), walk1=(_STUMP_SAG_DOWN, FEET_ROW)),
        up=dict(stand=(_STUMP_UP, FEET_ROW), walk0=(_STUMP_SAG_UP, FEET_ROW),
                walk1=(_STUMP_SAG_UP, FEET_ROW)),
        left=dict(stand=(_STUMP_LEFT, FEET_ROW), walk0=(_STUMP_SAG_LEFT, FEET_ROW),
                  walk1=(_STUMP_SAG_LEFT, FEET_ROW)),
    ),
    extra=[(_STUMP_RISE, FEET_ROW), "kleon_frame0"],
)

POSES = [KLEON_STUMP]


# ==========================================================================
# Field objects (32x32)
# ==========================================================================

def _obj(rows, top, w=32, h=32):
    """A frame from rows placed with its first row at `top`, padded to w x h."""
    out = ["." * w] * top + [r.ljust(w, ".") for r in rows]
    out += ["." * w] * (h - len(out))
    assert len(out) == h, (len(out), h)
    for r in out:
        assert len(r) == w, r
    return out


def _paste(base, rows, x0, y0):
    """base with rows painted over it at (x0, y0); '.' in rows keeps base."""
    out = [list(r) for r in base]
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch != ".":
                out[y0 + j][x0 + i] = ch
    return ["".join(r) for r in out]


def _cut(rows, y0, y1):
    """rows with lines y0..y1-1 blanked."""
    return [("." * len(r) if y0 <= j < y1 else r) for j, r in enumerate(rows)]


# His six Poke Balls in a row on the stump's edge (beat 42), none of them
# twitching. Face down: centered on the tile. Face left: the row runs out to
# the left from the tile's right edge; face right (mirrored) out to the right
# from the tile's left edge, so it sits beside Kleon on either side.
_BALL = [".kkk.", "kcckk", "kkLkk", "klLLk", ".kkk."]


def _ball_row(x0):
    rows = [list("." * 32) for _ in range(32)]
    for i in range(6):
        for j, line in enumerate(_BALL):
            for k, ch in enumerate(line):
                if ch != ".":
                    rows[21 + j][x0 + i * 4 + k] = ch
    return ["".join(r) for r in rows]


_BALLS_CENTER = _ball_row(3)
_BALLS_LEFT = _ball_row(0)
KLEON_BALLS = dict(name="kleon_balls", pal="cast", kind="object", fw=32, fh=32,
                   frames=[_BALLS_CENTER, _BALLS_CENTER, _BALLS_LEFT])

# --------------------------------------------------------------------------
# The temple hounds: lean white sighthounds in bronze collars (folk palette:
# linen white and shade, the gray for the far legs, the bronze ochre and
# gold). Nine walking frames in the standard order; walking, the legs swing
# and the head turns. Frames 9 and 10 are a sleeping curl (an ear lifts in
# 10), shown by OBJ_EVENT_GFX_ICHOR_TEMPLE_HOUND_SLEEP.
# --------------------------------------------------------------------------

#         0         1         2         3
#         01234567890123456789012345678901
_HOUND_L_TOP = [
    ".........k......................",
    "........kLk.....................",
    "......kkLulk....................",
    "....kkLLLLLlk...................",
    "..kkLLkLLLLlk...................",
    "kkLLLLLLLLLlk...................",
    "kLLLLLLLLLLlk...................",
    ".kkkkkkLLLLlk...................",
    ".......kLLLLOk..................",
    "........kLLLook.................",
    "........kLLLLLkkkkkkkkkkk.......",
    "........kLLLLLLLLLLLLLLLLkk.....",
    "........klLLLLLLLLLLLLLLLLlk....",
    ".........kLLLLLLLLLLLLLLLlllk...",
    ".........kllLLLLlkkkkkkLllllkk..",
]
# legs: (near front, far front, near hind, far hind) drawn below the body
_HOUND_L_LEGS_STAND = [
    "..........klllk......kllllk..kLk",
    "..........kLLk.kk.....kllk....kk",
    "..........kLLk.kyk....kLk.kk....",
    "..........kLk..kyk....kLk.kyk...",
    "..........kLk..kyk....kLk.kyk...",
    ".........kLLk..kyk...kLLk.kyk...",
    ".........kkkk.kkk....kkkk.kkk...",
]
_HOUND_L_LEGS_W0 = [
    ".........kLllk.......kllllk..kLk",
    "........kLLk..kk......kllk....kk",
    ".......kLLk...kyk......kLk..kk..",
    "......kLLk.....kyk......kLk.kyk.",
    "......kLk......kyk.......kLkkyk.",
    ".....kLLk.....kyyk.......kLLkyk.",
    ".....kkkk.....kkk........kkkkkk.",
]
_HOUND_L_LEGS_W1 = [
    "..........klllk.....kllllk...kLk",
    "...........kLLk.kk...kllk.....kk",
    "............kLLkkyk..kLk.kk.....",
    ".............kLk.kyk.kLk..kyk...",
    "............kLLk..kyk.kLk..kyk..",
    "...........kLLk...kyyk.kLk..kyk.",
    "...........kkkk...kkk..kkkk.kkk.",
]
#         0         1         2         3
#         01234567890123456789012345678901
_HOUND_D_HEAD = [
    "............k......k............",
    "...........kLk....kLk...........",
    "...........kuLkkkkLuk...........",
    "............kLLLLLLk............",
    "............kLkLLkLk............",
    ".............kLLLLk.............",
    "..............kLLk..............",
    "..............kLlk..............",
    "..............kkkk..............",
]
_HOUND_D_BODY = [
    ".............kOooOk.............",
    "............kLLLLLLk............",
    "...........klLLLLLLlk...........",
    "...........klLLLLLLlk...........",
    "...........kllLLLLllk...........",
    "............kLkllkLk............",
]
_HOUND_D_LEGS_STAND = [
    "............kLk..kLk............",
    "............kLk..kLk............",
    "............kLk..kLk............",
    "...........kLLk..kLLk...........",
    "...........kkkk..kkkk...........",
]
_HOUND_D_LEGS_W0 = [
    "............kLk..kLk............",
    "............kLk..kLk............",
    "...........kLLk..kLk............",
    "...........kkkk..kLk............",
    ".................kkk............",
]
_HOUND_D_LEGS_W1 = [
    "............kLk..kLk............",
    "............kLk..kLk............",
    "............kLk..kLLk...........",
    "............kLk..kkkk...........",
    "............kkk.................",
]
_HOUND_U_TOP = [
    "............k......k............",
    "...........kLk....kLk...........",
    "...........kLLkkkkLLk...........",
    "............kLLLLLLk............",
    "............kLLLLLLk............",
    "............kOooooOk............",
    "............kLLLLLLk............",
    "...........kLLLLLLLLk...........",
    "...........kLLLLLLLLk...........",
    "...........klLLLLLLlk...........",
    "..........kllLLkkLLllk..........",
    "..........kllLkLLkLllk..........",
    "...........kllkLLkllk...........",
]
_HOUND_U_LEGS_STAND = [
    "...........kLLkLkkLLk...........",
    "............kLkkkkLk............",
    "............kLk..kLk............",
    "............kLk..kLk............",
    "............kLk..kLk............",
    "............kLLk.kLLk...........",
    "............kkkk.kkkk...........",
]
_HOUND_U_LEGS_W0 = [
    "...........kLLkLkkLLk...........",
    "............kLkkkkLk............",
    "............kLk..kLk............",
    "............kLk..kLk............",
    "............kLLk.kLk............",
    "............kkkk.kLLk...........",
    ".................kkkk...........",
]
_HOUND_U_LEGS_W1 = [
    "...........kLLkLkkLLk...........",
    "............kLkkkkLk............",
    "............kLk..kLk............",
    "............kLk..kLk............",
    "............kLk..kLLk...........",
    "............kLLk.kkkk...........",
    "............kkkk................",
]
_HOUND_SLEEP = [
    "............kkkkkkkk............",
    "....k.....kkLLLLLLLLkk..........",
    "...kLk...kLLLLLLLLLLLLk.........",
    "...kuLkkkLLLLLLLLLLLLLlk........",
    "..kLLLLLkLLLLLLLLkkLLLlk........",
    ".kLLLLLLkLLLLLLLkLLlLllk........",
    ".kLkkLLLLkLLLLLLkLLllllk........",
    "kLLLLLLLLkOoLLkkLlllllk.........",
    "kkkkkkLLLLkkkkkLLLLkkLLk........",
    "......kLLLLLLLLLLkk..kLk........",
    ".......kkkkkkkkkkk...kk.........",
]
_HOUND_SLEEP_EAR = _paste(_HOUND_SLEEP, ["kk...", "kLk..", "kLLk."], 2, 1)


def _hound_frames():
    # Standing frames have the paws on row 30; walking frames bob a pixel
    # lower, as the walkers do.
    def left(legs, top):
        return _obj(_HOUND_L_TOP + legs, top)

    def down(legs, top, turn=0):
        head = [r[1:] + "." if turn > 0 else ("." + r[:-1] if turn < 0 else r) for r in _HOUND_D_HEAD]
        return _obj(head + _HOUND_D_BODY + legs, top)

    def up(legs, top):
        return _obj(_HOUND_U_TOP + legs, top)

    return [down(_HOUND_D_LEGS_STAND, 11), up(_HOUND_U_LEGS_STAND, 11), left(_HOUND_L_LEGS_STAND, 9),
            down(_HOUND_D_LEGS_W0, 12, -1), down(_HOUND_D_LEGS_W1, 12, 1),
            up(_HOUND_U_LEGS_W0, 12), up(_HOUND_U_LEGS_W1, 12),
            left(_HOUND_L_LEGS_W0, 10), left(_HOUND_L_LEGS_W1, 10),
            _obj(_HOUND_SLEEP, 20), _obj(_HOUND_SLEEP_EAR, 20)]


TEMPLE_HOUND = dict(name="temple_hound", pal="folk", kind="object", fw=32, fh=32,
                    frames=_hound_frames())

# --------------------------------------------------------------------------
# The golden hind (theoxenia palette): a doe with gold antlers. Frames 0-2
# head up, 3-8 the bolt, 9-11 grazing (down, up, left), played by
# sAnimTable_IchorHind: placed or turned, she grazes; running, she bolts head
# up and stands alert where the run ends; nurse_joy_bow throws her head up.
# --------------------------------------------------------------------------

#         0         1         2         3
#         01234567890123456789012345678901
_HIND_L_HEAD = [
    "..........k.....................",
    ".....k...kOk....................",
    "....kyk.kOk.k...................",
    ".....kyk.kOkOk..................",
    "..k...kykkOOk...................",
    ".kyk..kykOOk....................",
    "..kykkyykOk.....................",
    "...kkyyOOk.kk...................",
    "....kkcck.kcck..................",
    "...kcccckcck....................",
    "..kccccccck.....................",
    ".kcckccccHk.....................",
    "kccccccccHk.....................",
    "kWwcccccHk......................",
    ".kkkwcccHk......................",
    ".....kwccHk.....................",
    ".....kwcccHk....................",
]
_HIND_L_BODY = [
    ".....kwccccHkkkkkkkkkkk.........",
    ".....kwccccccccccccccccHk.......",
    "......kwcccccccccccccccHHk......",
    "......kwcccccccccccccccHHWk.....",
    "......kWwcccccccccccccHHHWk.....",
    ".......kWwwccccccccccHHHk.......",
    "........kkwWWwkkkkkwwHHk........",
]
_HIND_L_LEGS = [
    ".........kcHk.kHk..kHHk.kHk.....",
    ".........kcHk.kHk..kcHk.kHk.....",
    ".........kcHk.khk...kHk.khk.....",
    ".........kcHk.khk...kHk.khk.....",
    ".........kkk..kkk...kkk.kkk.....",
]
# The bolt: stretched out (legs flung fore and aft), then gathered.
_HIND_L_LEGS_STRETCH = [
    "........kcHk.kHk.....kHHk.kHk...",
    ".......kcHk..khk......kHHk.kHk..",
    "......kcHk..khk........kHk..khk.",
    ".....kcHk..khk..........kHk..kk.",
    ".....kkk...kk............kk.....",
]
_HIND_L_LEGS_GATHER = [
    "........kcHkkHk....kHHk.kHk.....",
    ".......kcHk.khk.....kHHk.kHk....",
    ".......kHHk.kk.......kHk..khk...",
    "........kk............kHk..khk..",
    ".......................kkk..kk..",
]
#         0         1         2         3
#         01234567890123456789012345678901
_HIND_D_HEAD = [
    "..........k.k......k.k..........",
    "..........kOk.k..k.kOk..........",
    "...........kOkOk.kOkOk..........",
    "............kOOk..kOOk..........",
    ".............kyOkkOyk...........",
    "..........kk..kkkkkk..kk........",
    "..........kcck.kcck.kcck........",
    "...........kckcccccckck.........",
    "............kcccccccck..........",
    "............kckccccckck.........",
    "............kccccccccck.........",
    ".............kcccccck...........",
    "..............kkWWkk............",
]
_HIND_D_BODY = [
    "..............kWwwck............",
    ".............kcWwwcck...........",
    "............kccWwwccck..........",
    "...........kcccWwwcccHk.........",
    "...........kccccwccccHk.........",
    "...........kHcccccccHHk.........",
    "...........kHHccccccHHk.........",
    "............kHHkkkkHHk..........",
]
_HIND_D_LEGS = [
    "............kcHk..kcHk..........",
    "............kcHk..kcHk..........",
    "............kcHk..kcHk..........",
    "............kcHk..kcHk..........",
    "............kcHk..kcHk..........",
    "............kkkk..kkkk..........",
]
_HIND_D_LEGS_W0 = [
    "............kcHk..kcHk..........",
    "............kcHk..kcHk..........",
    "............kcHk..kcHk..........",
    "............kkkk..kcHk..........",
    "..................kcHk..........",
    "..................kkkk..........",
]
_HIND_D_LEGS_W1 = [
    "............kcHk..kcHk..........",
    "............kcHk..kcHk..........",
    "............kcHk..kcHk..........",
    "............kcHk..kkkk..........",
    "............kcHk................",
    "............kkkk................",
]
_HIND_U_HEAD = [
    "..........k.k......k.k..........",
    "..........kOk.k..k.kOk..........",
    "...........kOkOk.kOkOk..........",
    "............kOOk..kOOk..........",
    ".............kyOkkOyk...........",
    "..........kk..kkkkkk..kk........",
    "..........kcck.kcck.kcck........",
    "...........kckcccccckck.........",
    "............kcccccccck..........",
    "............kccccccccck.........",
    "............kHcccccccHk.........",
    ".............kHcccccHk..........",
    "..............kccccck...........",
]
_HIND_U_BODY = [
    ".............kcccccccck.........",
    "............kcccccccccck........",
    "...........kccccccccccccHk......",
    "...........kcccccWWccccHk.......",
    "...........kcccWWWWWWccHk.......",
    "...........kccWWWwwWWcHHk.......",
    "...........kHccWWwwWWcHHk.......",
    "............kHcWwkkwWcHk........",
]
_HIND_U_LEGS = [
    "............kcHk....kcHk........",
    "............kcHk....kcHk........",
    "............kchk....kchk........",
    "............kchk....kchk........",
    "............kchk....kchk........",
    "............kkkk....kkkk........",
]
_HIND_U_LEGS_W0 = [
    "............kcHk....kcHk........",
    "............kcHk....kcHk........",
    "............kchk....kchk........",
    "............kkkk....kchk........",
    "....................kchk........",
    "....................kkkk........",
]
_HIND_U_LEGS_W1 = [
    "............kcHk....kcHk........",
    "............kcHk....kcHk........",
    "............kchk....kchk........",
    "............kchk....kkkk........",
    "............kchk................",
    "............kkkk................",
]
# Grazing: the head down at the grass, antlers forward.
_HIND_GRAZE_L_FRONT = [
    ".....kk..........",
    "...kkOOk.........",
    "..kOkOkkkk.......",
    ".kOk.kOkcck......",
    "..kOOkcccHk......",
    "...kkcckcHk......",
    "...kccccHk.......",
    "..kcccccHk.......",
    "..kccccHk........",
    "..kWwccHk........",
    "...kkkkk.........",
]
_HIND_GRAZE_D_HALF = [
    "..........k.....",
    ".........kOk....",
    "..........kOk.k.",
    "...........kOkOk",
    ".........kckkyOO",
    "..........kckccc",
    ".............kcc",
    ".............kcc",
    "..............kc",
    "..............kW",
    "...............k",
]
_HIND_GRAZE_D_HEAD = [r + r[::-1].replace("W", "w") for r in _HIND_GRAZE_D_HALF]
_HIND_GRAZE_D_LEGS = [
    "...........kcHk....kcHk.........",
    "..........kcHk......kcHk........",
    "..........kcHk......kcHk........",
    "..........kcHk......kcHk........",
    "..........kcHk......kcHk........",
    "..........kkkk......kkkk........",
]

_HIND_U_GRAZE_BACK = [
    ".............kkkkkkkk...........",
    "............kccccccccHk.........",
    "...........kccccccccccHk........",
]
_HIND_GRAZE_D_BODY = [
    ".............kkkkkkkk...........",
    "............kccccccccHk.........",
    "...........kccccccccccHk........",
    "...........kccccccccccHk........",
    "...........kHcccccccccHk........",
    "...........kHHcccccccHHk........",
    "............kHHkkkkkkHHk........",
]


def _hind_frames():
    def left(legs, top):
        return _obj(_HIND_L_HEAD + _HIND_L_BODY + legs, top)

    def down(legs, top):
        return _obj(_HIND_D_HEAD + _HIND_D_BODY + legs, top)

    def up(legs, top):
        return _obj(_HIND_U_HEAD + _HIND_U_BODY + legs, top)

    blank = ["." * 32]
    # Grazing: the body as it stands, the head lowered to the grass in front.
    graze_left = _paste(_obj(blank * 17 + _HIND_L_BODY + _HIND_L_LEGS, 2), _HIND_GRAZE_L_FRONT, 0, 20)
    graze_down = _paste(_obj(blank * 15 + _HIND_GRAZE_D_BODY + _HIND_GRAZE_D_LEGS, 3), _HIND_GRAZE_D_HEAD, 0, 20)
    graze_up = _obj(blank * 12 + _HIND_U_GRAZE_BACK + _HIND_U_BODY[2:] + _HIND_U_LEGS, 4)
    return [down(_HIND_D_LEGS, 4), up(_HIND_U_LEGS, 4), left(_HIND_L_LEGS, 2),
            down(_HIND_D_LEGS_W0, 5), down(_HIND_D_LEGS_W1, 5),
            up(_HIND_U_LEGS_W0, 5), up(_HIND_U_LEGS_W1, 5),
            left(_HIND_L_LEGS_STRETCH, 1), left(_HIND_L_LEGS_GATHER, 2),
            graze_down, graze_up, graze_left]


GOLDEN_HIND = dict(name="golden_hind", pal="theoxenia", kind="object", fw=32, fh=32,
                   frames=_hind_frames())

OBJECTS = [KLEON_BALLS, TEMPLE_HOUND, GOLDEN_HIND]



# ==========================================================================
# Output
# ==========================================================================

def all_specs():
    return WALKERS + POSES + OBJECTS


def _extra_frames(spec):
    pal, legend = PALETTES[spec["pal"]]
    out = []
    for item in spec.get("extra", []):
        if item == "kleon_frame0":
            out.append(_kleon_frame0())
            continue
        rows, bottom = item
        out.append(build_frame(rows, bottom + 1 - len(rows), legend, pal, f"{spec['name']} extra"))
    return out


def build(spec):
    if spec.get("kind") == "pose":
        sheet = b1.build_pose_sheet(spec)
    elif spec.get("kind") == "object":
        sheet = b1.build_object_sheet(spec)
    else:
        sheet = folk_build_sheet(spec)
    extra = _extra_frames(spec)
    return np.hstack([sheet] + extra) if extra else sheet


def palette_of(spec):
    return PALETTES[spec["pal"]][0]


def contact_sheet(sheets):
    """design/phase3/img/sprites_batch3.png: everything at 2x, after the
    walkers it is drawn to match (the slice's and batch 1's, labelled)."""
    big = sheet_preview(sheets, all_specs(), k=2, refs=REFS, lw=84, font_size=12)
    # sheet_preview labels every reference "Act I"; batch 1's are Act II's.
    from PIL import ImageDraw
    d = ImageDraw.Draw(big)
    font = b1.label_font(12)
    for i, ref in enumerate(REFS):
        if ref in ("maenad", "herald"):
            y = i * (H + 4) * 2
            d.rectangle([4, y + 8 + 12, 80, y + 8 + 26], fill=(232, 224, 200, 255))
            d.text((4, y + 8 + 12), "Act II b1", fill=(112, 96, 80, 255), font=font)
    return big


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
        sheet_preview(sheets, specs, refs=REFS).save(os.path.join(pv, "sprites_act2_b3_sheets.png"))
    if grids:
        os.makedirs(grids, exist_ok=True)
        for spec in specs:
            grid_preview(to_rgba(sheets[spec["name"]], palette_of(spec)), 8).save(
                os.path.join(grids, spec["name"] + "_grid.png"))


if __name__ == "__main__":
    main()
