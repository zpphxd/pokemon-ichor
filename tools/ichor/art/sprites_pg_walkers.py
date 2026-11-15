#!/usr/bin/env python3
"""Overworld walkers for the post-game's first cast: the Euploia's three new
crew, the herald of the Olympic truce, and Olympia's people ahead of batch 2
(design/postgame/SPRITES.md).

Usage:
    python3 tools/ichor/art/sprites_pg_walkers.py [NAME ...] [--write] [--preview DIR] [--grids DIR]

--write    writes graphics/object_events/pics/ichor/pg_<name>.png (144x32,
           4bpp indexed, nine 16x32 frames) for every walker here, and the
           Olympia palette graphics/object_events/palettes/ichor_olympia.pal
--preview  writes DIR/pg_walkers_sheets.png (4x, vanilla Birch first for scale)
--grids    writes DIR/pg_<name>_grid.png, 8x pixel grids for editing

Two palettes, so neither the ship nor Olympia costs more than one Ichor OBJ
palette slot of its own:

* CAST_PAL (sprites_npc.py, OBJ_EVENT_PAL_TAG_ICHOR_CAST): Nolan, Phemios and
  Lynkeus, who stand below deck beside Alethea and the cast-palette crew, and
  the herald, who stands in every town beside the townsfolk.
* OLYMPIA_PAL (new, OBJ_EVENT_PAL_TAG_ICHOR_OLYMPIA): the five Brains,
  Olympias and Paionios. The cast's ramps and letters, with a gold that is
  brighter than the cast's bronze, an ash gray for beards and marble dust, two
  greens for serpents, wreaths and Achilles's cloak, and Olympias's purple
  shading into wine.

Walkers are built on sprites_folk.py's body archetypes (tunic, midi, robe),
so proportions, the step bob and feet on row 30 match every Ichor walker. Each
walker draws its own head per direction and paints its costume and props with
overlays; see sprites_folk.py's docstring for the overlay format.
"""
import os
import sys


sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, Palette, save_indexed, to_rgba, upscale, grid_preview  # noqa: E402
from sprites_npc import checker_bg, ref_rgba  # noqa: E402
import sprites_folk as F  # noqa: E402
from sprites_folk import pole, W, H  # noqa: E402
from PIL import Image  # noqa: E402

OUT_DIR = os.path.join(ROOT, "graphics/object_events/pics/ichor")
OLY_PAL_PATH = os.path.join(ROOT, "graphics/object_events/palettes/ichor_olympia.pal")

# --------------------------------------------------------------------------
# The Olympia palette. Letters follow the cast palette where the role
# matches (k ink, b brown, r wine/red_d, u umber, c crimson, s/S skin,
# o/O bronze-gold, l/L linen).
# --------------------------------------------------------------------------

OLY_COLORS = [
    # char, name, rgb                       used for
    ("k", "ink", (32, 24, 24)),            # outlines, eyes, black hair
    ("b", "brown", (88, 48, 32)),          # hair, leather, boots, the bearskin
    ("r", "wine", (120, 32, 56)),          # crimson's and purple's shade
    ("u", "umber", (168, 96, 56)),         # auburn hair, wood, felt, the apron
    ("c", "crimson", (216, 64, 56)),       # Hippolyta's tunic, Ariadne's thread
    ("s", "skin_d", (224, 152, 104)),      # skin shadow
    ("S", "skin_l", (248, 208, 168)),      # skin
    ("o", "bronze", (208, 144, 48)),       # bronze, gold's shade, Achilles's hair
    ("O", "gold", (248, 216, 96)),         # gold: crowns, belts, Achilles's hair
    ("l", "linen_d", (200, 184, 152)),     # linen shade, dusty wool
    ("L", "linen_l", (248, 240, 216)),     # linen, marble dust, beard highlights
    ("a", "ash", (136, 136, 144)),         # gray beards, iron, marble dust in shade
    ("v", "green_d", (48, 96, 64)),        # serpents' and the cloak's shade
    ("g", "green", (112, 168, 80)),        # serpents, wreaths, Achilles's cloak
    ("p", "purple", (152, 80, 152)),       # Olympias's peplos
]
OLY_PAL = Palette([(name, rgb) for _, name, rgb in OLY_COLORS])
OLY_LEGEND = {ch: name for ch, name, _ in OLY_COLORS}

# sprites_folk builds sheets by palette name
F.PALETTES["olympia"] = (OLY_PAL, OLY_LEGEND)

_BLANK1 = ["................"]
_BLANK3 = ["................"] * 3


def _rev(cells):
    return [c[::-1] for c in cells]


# ==========================================================================
# The Euploia's crew (cast palette)
# ==========================================================================

# Christopher Nolan, the dramatist: light-brown hair swept back from a high
# forehead, a steady unblinking stare, a dark slate himation pinned neatly at
# the left shoulder with a bronze pin and wrapped over a pale chiton that
# shows at his right shoulder and arm and at the hem.
NOLAN = dict(
    name="nolan", pal="cast", arch="midi",
    roles=dict(C="t", Q="n", T="t", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kuulluuk....",
            "...kulluuuubk...",
            "..kullluuuuubk..",
            "..kuuSSSSSSubk..",
            "..kuSSSSSSSSuk..",
            "..kuSbbSSbbSuk..",
            "..kuSkSSSSkSuk..",
            "..kbSkSSSSkSbk..",
            "...kSSSSSSSSk...",
            "....kssSSssk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kuulluuk....",
            "...kulluuuubk...",
            "..kullluuuuubk..",
            "..kuluuuuuubuk..",
            "..kuuluuuuuubk..",
            "..kuuuuuuuubbk..",
            "..kSuuuuuuubSk..",
            "..ksuuuuuuubsk..",
            "...ksuuuuubsk...",
            "....kSSSSSSk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkuulluk....",
            "...kulluuuuubk..",
            "..kulluuuuuubk..",
            "..kSSuuuuuuubk..",
            "..kSSSSuuuuubk..",
            "..kbSSSSuuuubk..",
            "..kSkSSSsuuubk..",
            "..kSkSSSSuubk...",
            "..kSSSSSsubk....",
            "...ksSSssk......",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["____LL____O_____"]),
                      ("b1", ["___LLl___n______"]),
                      ("b2", ["___Ll___n__tn___"]),
                      ("b3", ["___Ll__n___tn___"]),
                      ("b4", ["______n____tn___"]),
                      ("b7", ["____LLLLLLLl____"])]},
        up={"all": [("b0", ["__________LL____"]),
                    ("b1", ["_____n__________"]),
                    ("b2", ["___tn_n____Ll___"]),
                    ("b3", ["___tn__n___Ll___"]),
                    ("b4", ["___tn___n_______"]),
                    ("b7", ["____LLLLLLLl____"])]},
        left={"all": [("b0", ["________O_______"]),
                      ("b7", ["_____LLLLLl_____"])]},
    ),
)

# Phemios, Odysseus's old bard: dark curls and a short beard under a laurel
# wreath, a long linen robe girt with blue, a blue mantle over his shoulders,
# and a bronze lyre with a tortoiseshell sound box in his left arm.
PHEMIOS = dict(
    name="phemios", pal="cast", arch="robe",
    roles=dict(C="L", Q="l", T="B", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbbubbbk....",
            "...kbubbbubbk...",
            ".gkbubbbbbubbkg.",
            "..kggggggggggk..",
            "..kbSbbSbbSbbk..",
            "..bsSSSSSSSSsb..",
            "..bsSkSSSSkSsb..",
            "..bbSkSSSSkSbb..",
            "...bbSbSSbSbb...",
            "....bbbbbbbb....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbbubbbk....",
            "...kbubbbubbk...",
            ".gkbbbubbbbbbkg.",
            "..kggggggggggk..",
            "..kbbubbbbubbk..",
            "..bsbbbubbbbsb..",
            "..bsbbbbbubbsb..",
            "...bbbubbbbbb...",
            "....bbbbbbbb....",
            "....kbSSSSbk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkbbubbk....",
            "...kbubbbubbk.g.",
            "..kbbbbbbbubbkg.",
            "..kggggggggggk..",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbbk..",
            "..kbSSSSsbbbk...",
            "...kbbbbbbbk....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["____BB____Bn____"]),
                      ("b1", ["___BB______Bn___"]),
                      ("b2", ["_kB__________nk_"]),
                      ("b3", ["_kB__________nk_"]),
                      ("b4", ["_kB__________nk_"]),
                      ("b5", ["_kn__________nk_"]),
                      (10, ["_________k___k__"]),
                      ("b0", ["_________O___O__"]),
                      ("b1", ["_________OOOOO__"]),
                      ("b2", ["_________oLLLo__"]),
                      ("b3", ["_________oLLLo__"]),
                      ("b4", ["_________kuuuk__"]),
                      ("b5", ["__________kuk___"])]},
        up={"all": [("b0", ["____BBBBBBBn____"]),
                    ("b1", ["___BBBBBBBBBn___"]),
                    ("b2", ["_____BBBBBn_____"]),
                    ("b3", ["_____BBBBBn_____"]),
                    ("b4", ["_____BBBBBn_____"]),
                    ("b5", ["_____nBBBnn_____"]),
                    (10, ["_k___k__________"]),
                    ("b0", ["_O___O__________"]),
                    ("b1", ["_OOOOO__________"])]},
        left={"all": [("b0", ["_________Bn_____"]),
                      ("b1", ["_________BBn____"]),
                      ("b2", ["__________Bnk___"]),
                      ("b3", ["__________Bnk___"]),
                      ("b4", ["__________nnk___"]),
                      (10, ["_k__k___________"]),
                      ("b0", ["_O__O___________"]),
                      ("b1", ["_OOOO___________"]),
                      ("b2", ["_oLLo___________"]),
                      ("b3", ["_kuuk___________"]),
                      ("b4", ["__kk____________"])]},
    ),
)

# Lynkeus the lookout, lynx-eyed: black hair under a crimson headband, its
# tails flying at the back, a short blue exomis, and a spotted lynx pelt
# slung from his left shoulder to his right hip.
LYNKEUS = dict(
    name="lynkeus", pal="cast", arch="tunic",
    roles=dict(C="B", Q="n", T="b", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbbbbbbbbk...",
            "..kbbbbbbbbbbk..",
            "..kcccccccccrk..",
            "..kbSbbSbbSbbk..",
            "..bsSSSSSSSSsb..",
            "..bsLkSSSSkLsb..",
            "..bsSkSSSSkSsb..",
            "...bSSSSSSSSb...",
            "....bssSSssb....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbbbbbbbbk...",
            "..kbbbbbbbbbbk..",
            "..kcccccccccrk..",
            "..kbbbbbbbbccrk.",
            "..bsbbbbbbbbcr..",
            "..bsbbbbbbbbsb..",
            "...bbbbbbbbbb...",
            "....bbbbbbbb....",
            "....bbSSSSbb....",
        ],
        left=[
            "......kkkkk.....",
            "....kkbbbbbk....",
            "...kbbbbbbbbk...",
            "..kbbbbbbbbbbk..",
            "..kcccccccccrkk.",
            "..kbSbbbbbbbbck.",
            "..kSSSSSbsbbbkc.",
            "..kSLkSSssbbbk..",
            "..kSkSSSSbbbbk..",
            "...bsSSSsbbbk...",
            "....bssSSbbk....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["__________ub____"]),
                      ("b1", ["_________ubu____"]),
                      ("b2", ["________uub_____"]),
                      ("b3", ["_______ubu______"]),
                      ("b4", ["______uub_______"]),
                      ("b5", ["_____kub________"])]},
        up={"all": [("b0", ["____bu__________"]),
                    ("b1", ["____ubu_________"]),
                    ("b2", ["_____buu________"]),
                    ("b3", ["______ubu_______"]),
                    ("b4", ["_______buu______"]),
                    ("b5", ["________buk_____"])]},
        left={"all": [("b0", ["______ubu_______"]),
                      ("b1", ["_____uubu_______"])]},
    ),
)

# A herald of the Olympic truce, a spondophoros: auburn hair under the olive
# wreath, a long white robe with a crimson girdle and hem, and the bronze
# kerykeion, the herald's staff with its two serpents knotted at the top.
_KERYKEION = ["_k_", "kOk", "O_O", "kOk", "O_O", "kok"] + ["ko"] * 14 + ["kb"]
HERALD = dict(
    name="truce_herald", pal="cast", arch="robe",
    roles=dict(C="L", Q="l", T="c", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kuuuuuuk....",
            "...kuOuuuuubk...",
            ".gkuuuuuuuuubkg.",
            "..kggggggggggk..",
            "..kuSuuSuuSubk..",
            "..usSSSSSSSSsu..",
            "..usSkSSSSkSsu..",
            "..usSkSSSSkSsu..",
            "...uSSSSSSSSu...",
            "....ussSSssu....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kuuuuuuk....",
            "...kuOuuuuubk...",
            ".gkuuuuuuuuubkg.",
            "..kggggggggggk..",
            "..kuuuuuuuuubk..",
            "..usuuuuuuuusu..",
            "..usuuuuuuubsu..",
            "...uuuuuuuubu...",
            "....uuuuuubu....",
            "....kuSSSSuk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkuuuuuk....",
            "...kuOuuuuubk.g.",
            "..kuuuuuuuuubkg.",
            "..kggggggggggkg.",
            "..kuSuuuuuuubk..",
            "..kSSSSSusuubk..",
            "..kSkSSSssuubk..",
            "..kSkSSSSuuubk..",
            "...kSSSSsuubk...",
            "....kssSSuuk....",
        ],
    ),
    over=dict(
        down={"all": [("b8", ["___cccccccccr___"]), pole(0, 0, _KERYKEION),
                      ("b5", ["__S_____________"])],
              "walk1": [("b5", ["..SSSCCCCCQSSk.."]), ("b6", ["..kkCCCCCCCQkk.."])]},
        up={"all": [("b8", ["___cccccccccr___"]), pole(13, 0, _rev(_KERYKEION)),
                    ("b5", ["_____________S__"])],
            "walk0": [("b5", ["..kSSCCCCCQSSS.."]), ("b6", ["..kkCCCCCCCQkk.."])]},
        left={"all": [("b8", ["___ccccccccr____"]), pole(0, 0, _KERYKEION),
                      ("b4", ["__Ss____________"])]},
    ),
)


# ==========================================================================
# Olympia (Olympia palette)
# ==========================================================================

# Achilles, swift-footed and restless: long bronze hair loose to the jaw, no
# beard, a short white chiton girt with gold, a sea-green chlamys (Thetis's
# color) pinned at his right shoulder and falling down his left side, and his
# ash spear.
_SPEAR = ["_k_", "kOk", "kok", "_u_"] + ["ku"] * 19 + ["kb"]
ACHILLES = dict(
    name="achilles", pal="olympia", arch="tunic",
    roles=dict(C="L", Q="l", T="O", F="b"),
    head=dict(
        down=_BLANK3 + [
            ".....kkkkkk.....",
            "....kOOOOook....",
            "...kOOoooOook...",
            "..kOoooooooouk..",
            "..kOoOooOooOuk..",
            "..koSSoSSoSSuk..",
            "..koSSSSSSSSuk..",
            "..koSkSSSSkSuk..",
            "..koSkSSSSkSuk..",
            "..kosSSSSSSsuk..",
            "..kuoksSSskouk..",
        ],
        up=_BLANK3 + [
            ".....kkkkkk.....",
            "....kOOOOook....",
            "...kOOoooOook...",
            "..kOoooooooouk..",
            "..kOoooOoooouk..",
            "..kOooooOooouk..",
            "..kOooOoooOouk..",
            "..kOoooooOoouk..",
            "..kooOooooOouk..",
            "..kuooooooooukk.",
            "...kuoSSSSouk...",
        ],
        left=_BLANK3 + [
            "......kkkkk.....",
            "....kkOOOOok....",
            "...kOOooooOok...",
            "..kOoooooooouk..",
            "..kOoOoooooouk..",
            "..kSoSoooOoouk..",
            "..kSSSSSoooouk..",
            "..kSkSSSSooouk..",
            "..kSkSSSSoOouk..",
            "..kSSSSSsooouk..",
            "...ksSSskuoouk..",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["____O_____gv____"]),
                      ("b1", ["__________ggvk__"]),
                      ("b2", ["___________gvk__"]),
                      ("b3", ["___________gvk__"]),
                      ("b4", ["___________gvk__"]),
                      ("b5", ["____________vk__"]),
                      pole(0, 0, _SPEAR), ("b5", ["__S_____________"])],
              "walk1": [("b5", ["..SSSCCCCCQSSk.."]), ("b6", ["..kkCCCCCCCQkk.."])]},
        up={"all": [("b0", ["____ggggggv_____"]),
                    ("b1", ["___gggggggggv___"]),
                    ("b2", ["_____gggggv_____"]),
                    ("b3", ["_____gggggv_____"]),
                    ("b4", ["_____ggggvv_____"]),
                    ("b5", ["_____vgggvv_____"]),
                    pole(13, 0, _rev(_SPEAR)), ("b5", ["_____________S__"])],
            "walk0": [("b5", ["..kSSCCCCCQSSS.."]), ("b6", ["..kkCCCCCCCQkk.."])]},
        left={"all": [("b0", ["______gv________"]),
                      ("b1", ["_____ggvk_______"]),
                      pole(0, 0, _SPEAR), ("b4", ["__Ss____________"])]},
    ),
)

# Odysseus, the man of many turns: broad, a gray beard and gray at the
# temples, one brow up, a traveler's felt pilos, a linen tunic under a brown
# cloak over both shoulders, and an oar on his left shoulder (Teiresias told
# him to carry one inland).
_OAR = ["_kkk", "kLLk", "kLlk", "kLlk", "_kk_"] + ["_ku"] * 12 + ["_kb"]
ODYSSEUS = dict(
    name="odysseus", pal="olympia", arch="tunic",
    roles=dict(C="L", Q="l", T="b", F="b"),
    head=dict(
        down=_BLANK1 + [
            "......kkkk......",
            ".....kuuubk.....",
            "....kuuuuubk....",
            "...kuuuuuuubk...",
            "..kbbbbbbbbbbk..",
            "..kaSSSSSbbSak..",
            "..kaSbbSSSSSak..",
            "..kaSkSSSSkSak..",
            "..kaaSSssSSaak..",
            "...aLaaaaaaLa...",
            "....kaaLLaak....",
        ],
        up=_BLANK1 + [
            "......kkkk......",
            ".....kuuubk.....",
            "....kuuuuubk....",
            "...kuuuuuuubk...",
            "..kbbbbbbbbbbk..",
            "..kaaaaaaaaaak..",
            "..saaLaaaaaaas..",
            "..saaaaaaaaaas..",
            "...aaaaaaaaaa...",
            "....aaaaaaaa....",
            "....kaSSSSak....",
        ],
        left=_BLANK1 + [
            ".......kkkk.....",
            "......kuuubk....",
            ".....kuuuuubk...",
            "...kkuuuuuuubk..",
            "..kbbbbbbbbbbbk.",
            "..kSSSSaaaaaak..",
            "..kSbbSSaaaaak..",
            "..kSkSSSsaaaak..",
            "..kSSSSsaaaak...",
            "..kaLaaaaaaak...",
            "...kaaaLaak.....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["..kuuuSSSSuubk.."]),
                      ("b1", [".kuuLLLLLLLLubk."]),
                      ("b2", ["_ku__________bk_"]),
                      ("b3", ["_ku__________bk_"]),
                      ("b4", ["_ku__________bk_"]),
                      pole(12, 0, _OAR)]},
        up={"all": [("b0", ["..kuuuuuuuuubk.."]),
                    ("b1", [".kuuuuuuuuuubbk."]),
                    ("b2", ["_ku__uuuuub__bk_"]),
                    ("b3", ["_ku__uuuuub__bk_"]),
                    ("b4", ["_ku__uuuubb__bk_"]),
                    ("b5", ["_____buuubb_____"]),
                    pole(0, 0, _rev(_OAR))]},
        left={"all": [("b0", ["_____kuuubk_____"]),
                      ("b1", ["____kuuuubbk____"]),
                      ("b2", ["_________ubk____"]),
                      ("b3", ["_________ubk____"]),
                      pole(9, 0, _OAR)]},
    ),
)

# Hippolyta, queen of the Amazons, daughter of Ares: black hair in a long
# braid under a gold diadem, a crimson tunic, the gold war-belt (two rows of
# plaques), patterned leggings, high boots, and a bronze pelta, the Amazons'
# crescent shield, on her left arm.
_PELTA = ["k___k", "Ok_kO", "OOkOO", "oOOOo", "koOok", "_kkk_"]
HIPPOLYTA = dict(
    name="hippolyta", pal="olympia", arch="tunic",
    roles=dict(C="c", Q="r", T="O", F="b", X="L", Y="p"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbbbbbbk....",
            "...kbbbbbbbbk...",
            "..kbbbbbbbbbbk..",
            "..kOOoOOoOOOok..",
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
            "...kbbbbbbbbk...",
            "..kbbbbbbbbbbk..",
            "..kOOoOOoOOOok..",
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
            "...kbbbbbbbbk...",
            "..kbbbbbbbbbbk..",
            "..kOOoOOoOOOok..",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbbk..",
            "..kSSSSSsbbubk..",
            "...kbsSssbkbbk..",
        ],
    ),
    over=dict(
        down={"all": [("b4", ["_____OoOOoO_____"]),
                      ("b5", ["_____oOoOo______"]),
                      pole(11, "b1", _PELTA)]},
        up={"all": [("b0", ["_______ub_______", "_______bu_______", "_______ub_______",
                            "______kOOk______", "_______kk_______"]),
                    ("b4", ["_____OoOOoO_____"]),
                    pole(0, "b1", ["k___k", "ok_ko", "oukuo", "ouuuo", "kouok", "_kkk_"])]},
        left={"all": [("b0", ["__________ubk___", "__________buk___", "__________kOk___",
                              "___________k____"]),
                      ("b4", ["____OoOOo_______"]),
                      pole(3, "b1", ["kkk", "kOo", "OOo", "OOo", "kOo", "kkk"])]},
    ),
)

# Atalanta the huntress, raised by a bear: auburn hair tied high, a short
# linen chiton, the bearskin over her shoulders with its paws knotted at her
# chest, tall hunting boots, and her bow in her left hand.
_BOW = ["_k_", "kuk", "Luk", "Lbk", "Luk", "Lbk", "Luk", "Lbk", "Luk", "kuk", "_k_"]
ATALANTA = dict(
    name="atalanta", pal="olympia", arch="tunic",
    roles=dict(C="L", Q="l", T="b", F="b", X="u", Y="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kuuuuurk....",
            "...kuouuuuurk...",
            "..kuuuuuuuuurk..",
            "..kuuuuuuuuurk..",
            "..kuSuuuuuuSrk..",
            "..kuSSSSSSSSrk..",
            "..kuSkSSSSkSrk..",
            "..kuSkSSSSkSrk..",
            "..krsSSSSSSsrk..",
            "...krssSSssrk...",
        ],
        up=[
            ".....kkkkkk.....",
            "....kuuuuurk....",
            "...kuouuuuurk...",
            "..kuuuuuuuuurk..",
            "..kuuuuuouuurk..",
            "..kuuuuubbuurk..",
            "..kuuuuuouuurk..",
            "..kuuuuuuuuurk..",
            "..kruuuuuuuurk..",
            "..kSruuuuuurSk..",
            "...kSSkurkkSSk..",
        ],
        left=[
            "......kkkkk.....",
            "....kkuuuuuk....",
            "...kuouuuuurk...",
            "..kuuuuuuuuurkk.",
            "..kuuuuuuubbuuk.",
            "..kuSuuuuuuurrk.",
            "..kSSSSSurrurk..",
            "..kSkSSSssuurk..",
            "..kSkSSSSuuurk..",
            "..kSSSSSsuurk...",
            "...ksSSsskrk....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["___kbbSSSSbbk___"]),
                      ("b1", ["___bu__bb__ub___"]),
                      ("b2", ["_kb__________bk_"]),
                      ("b3", ["_kb__________bk_"]),
                      ("b4", ["_kb__________bk_"]),
                      ("b5", ["_kb__________bk_"]),
                      pole(13, 6, _BOW)]},
        up={"all": [("b0", ["____bbbbbbb_____", "___bbuuubbbb____", "_____buubb______",
                            "_____bbubb______", "_____bbbbb______", "_____kbkbk______"]),
                    ("b0", ["_______ur_______"]), ("b1", ["_______ru_______"]),
                    pole(0, 6, _rev(_BOW))]},
        left={"all": [("b0", ["_______bbk______"]),
                      ("b1", ["_______bbbk_____"]),
                      ("b2", ["_________bk_____"]),
                      pole(2, 6, ["k", "u", "u", "u", "u", "u", "u", "u", "u", "u", "k"])]},
    ),
)

# Ariadne, mistress of the Labyrinth: long black curls bound with a gold band,
# a Minoan gold bodice, a flounced skirt in linen and crimson bands, and the
# red spool of her thread in her right hand.
ARIADNE = dict(
    name="ariadne", pal="olympia", arch="robe",
    roles=dict(C="O", Q="o", T="c", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbkbbkbk....",
            "...kbbkbbkbbk...",
            "..kbkbbkbbkbbk..",
            "..kOOOOOOOOOok..",
            "..kbSbSbbSbSbk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "..kbsSSSSSSsbk..",
            "..kbkssSSsskbk..",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbkbbkbk....",
            "...kbbkbbkbbk...",
            "..kbkbbkbbkbbk..",
            "..kOOOOOOOOOok..",
            "..kbbkbbkbbbbk..",
            "..kbkbbbbkbbbk..",
            "..kbbbkbbbbkbk..",
            "..kbkbbbkbbbbk..",
            "..kbbkbbbbkbbk..",
            "..kbbbbkbbbbbk..",
        ],
        left=[
            "......kkkkk.....",
            "....kkbkbbkk....",
            "...kbbkbbkbbk...",
            "..kbkbbkbbkbbk..",
            "..kOOOOOOOOOok..",
            "..kbSbbkbbkbbk..",
            "..kSSSSSbkbbbk..",
            "..kSkSSSsbkbbk..",
            "..kSkSSSSbbkbk..",
            "..kSSSSSsbkbbk..",
            "...ksSssbkbbbk..",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["__kb________bk__", "__kb________bk__"]),
                      ("b6", ["____LLLLLLLl____"]),
                      ("b7", ["____cccccccr____"]),
                      ("b8", ["___LcLcLcLcLl___"]),
                      ("b4", ["kk______________"]),
                      ("b5", ["kcrk____________"]),
                      ("b6", ["krrk____________"]),
                      ("b7", ["_kc_____________"]),
                      ("b8", ["__c_____________"])]},
        up={"all": [("b0", ["____bkbbkbb_____", "___bbkbbbkbb____", "_____bkbbk______",
                            "______kbbk______"]),
                    ("b6", ["____LLLLLLLl____"]),
                    ("b7", ["____cccccccr____"]),
                    ("b8", ["___LcLcLcLcLl___"])]},
        left={"all": [("b0", ["_________bkbk___", "_________kbbk___", "__________kk____"]),
                      ("b6", ["____LLLLLLl_____"]),
                      ("b7", ["____ccccccr_____"]),
                      ("b8", ["___LcLcLcLcl____"]),
                      ("b4", ["__kk____________"]),
                      ("b5", ["_kcrk___________"]),
                      ("b6", ["__kk____________"])]},
    ),
)

# Olympias, the Serpent Queen, Hera's seat: a tall gold polos over black
# hair, gold earrings, stern brows, a purple peplos with a gold girdle and
# hem, green serpents coiled about both forearms, and one risen over her
# right shoulder.
OLYMPIAS = dict(
    name="olympias", pal="olympia", arch="robe",
    roles=dict(C="p", Q="r", T="O", F="b"),
    head=dict(
        down=[
            "....kkkkkkkk....",
            "....kOOOOOok....",
            "....kOoOoOok....",
            "...kooooooook...",
            "..kbbbbbbbbbbk..",
            "..kbSbbbbbbSbk..",
            "..kbkkSSSSkkbk..",
            "..kbSkSSSSkSbk..",
            "..kbSkSSSSkSbk..",
            "..kOsSSSSSSsOk..",
            "...kbssSSssbk...",
        ],
        up=[
            "....kkkkkkkk....",
            "....kOOOOOok....",
            "....kOoOoOok....",
            "...kooooooook...",
            "..kbbbbbbbbbbk..",
            "..kbbbbubbbbbk..",
            "..kbbbbbubbbbk..",
            "..kbbbbubbbbbk..",
            "..kbbbkbbbbbbk..",
            "..kObbbbbbbbOk..",
            "...kbbkSSkbbk...",
        ],
        left=[
            ".....kkkkkkkk...",
            ".....kOOOOOok...",
            ".....kOoOoOok...",
            "....kooooooook..",
            "..kbbbbbbbbbbk..",
            "..kbSbbbbbbbbk..",
            "..kSkkSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSObbbk..",
            "..kSSSSSsbbbbk..",
            "...kssSssbkbbk..",
        ],
    ),
    over=dict(
        down={"all": [("b2", ["___gS______gS___"]),
                      ("b3", ["___Sv______Sv___"]),
                      ("b4", ["___gv______gv___"]),
                      ("b8", ["___OOOOOOOOOo___"]),
                      (8, [".kg_____________", "_gv_____________", "_vg_____________"]),
                      ("b0", ["__g_____________"])]},
        up={"all": [("b2", ["___Sg______Sg___"]),
                    ("b3", ["___vS______vS___"]),
                    ("b4", ["___vg______vg___"]),
                    ("b8", ["___OOOOOOOOOo___"]),
                    (8, ["_____________gk.", "_____________vg_", "_____________gv_"]),
                    ("b0", ["_____________g__"])]},
        left={"all": [("b8", ["___OOOOOOOOo____"]),
                      ("b2", ["_____gv_________"]),
                      ("b3", ["_____vg_________"])]},
    ),
)

# Paionios the sculptor, slightly behind schedule: dark curls and beard
# whitened with marble dust, mouth open mid-story, a dusty exomis off his
# right shoulder under a leather apron, a chisel in his right hand and a
# mallet in his left.
PAIONIOS = dict(
    name="paionios", pal="olympia", arch="tunic",
    roles=dict(C="l", Q="a", T="b", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbbabbbk....",
            "...kbabbbbabk...",
            "..kbbbbLbbbbbk..",
            "..kbabbbbbabbk..",
            "..kbSbbSbbSbbk..",
            "..bsSSSSSSSSsb..",
            "..bsSkSSSSkSsb..",
            "..bbSkSSSSkSbb..",
            "...bbSbkkbSbb...",
            "....bbbabbbb....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbbabbbk....",
            "...kbabbbbabk...",
            "..kbbbbLbbbbbk..",
            "..kbabbbbbabbk..",
            "..kbbbbabbbbbk..",
            "..bsbbbbbbabsb..",
            "..bsbabbbbbbsb..",
            "...bbbbbbabbb...",
            "....bbbbbbbb....",
            "....kbSSSSbk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkbbabbk....",
            "...kbabbbbabk...",
            "..kbbbbLbbbbbk..",
            "..kbabbbbbabbk..",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbabk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbbk..",
            "..kkSSSSsbbbk...",
            "...kbbbabbbk....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["____SS__________"]),
                      ("b1", ["____L_____L_____"]),
                      ("b2", ["_____uuuub______"]),
                      ("b3", ["_____uuuub______"]),
                      ("b4", ["_____uuuub______"]),
                      ("b5", ["_____uuuub______"]),
                      ("b6", ["_____uuub_______"]),
                      ("b4", [".k______________"]),
                      ("b5", ["ka______________"]),
                      ("b6", [".a______________"]),
                      ("b4", ["_____________kk_"]),
                      ("b5", ["____________kuuk"]),
                      ("b6", ["_____________ku_"])]},
        up={"all": [("b1", ["______L____L____"]),
                    ("b4", ["_kk_____________"]),
                    ("b5", ["kuuk____________"]),
                    ("b6", ["_uk_____________"]),
                    ("b4", ["______________k."]),
                    ("b5", ["______________ak"]),
                    ("b6", ["______________a."])]},
        left={"all": [("b0", ["______SS________"]),
                      ("b1", ["_____L__________"]),
                      ("b1", ["____uu__________"]),
                      ("b2", ["___kuuk_________"]),
                      ("b3", ["____ku__________"])]},
    ),
)

WALKERS = [NOLAN, PHEMIOS, LYNKEUS, HERALD, ACHILLES, ODYSSEUS, HIPPOLYTA, ATALANTA,
           ARIADNE, OLYMPIAS, PAIONIOS]
BY_NAME = {w["name"]: w for w in WALKERS}


def sheets(names=None):
    out = {}
    for w in WALKERS:
        if names and w["name"] not in names:
            continue
        out[w["name"]] = F.build_sheet(w)
    return out


def pal_of(name):
    return F.PALETTES[BY_NAME[name]["pal"]][0]


def sheet_preview(sh, k=4):
    """Every sheet at k times on a grass checker, vanilla Birch first."""
    items = [("prof_birch", ref_rgba())] + [(n, to_rgba(a, pal_of(n))) for n, a in sh.items()]
    pad = 4
    out = Image.new("RGBA", (W * 9 + pad * 8, (H + pad) * len(items) - pad), (232, 224, 200, 255))
    for i, (n, im) in enumerate(items):
        for f in range(9):
            tile = checker_bg(W, H)
            tile.alpha_composite(im.crop((f * W, 0, (f + 1) * W, H)))
            out.alpha_composite(tile, (f * (W + pad), i * (H + pad)))
    return upscale(out, k)


def main(argv):
    names = [a for a in argv if not a.startswith("--") and a in BY_NAME]
    sh = sheets(names)
    if "--write" in argv:
        os.makedirs(OUT_DIR, exist_ok=True)
        for n, a in sh.items():
            save_indexed(a, pal_of(n), os.path.join(OUT_DIR, f"pg_{n}.png"))
        OLY_PAL.write_jasc(OLY_PAL_PATH)
        print("wrote", len(sh), "sheets and", os.path.relpath(OLY_PAL_PATH, ROOT))
    if "--preview" in argv:
        d = argv[argv.index("--preview") + 1]
        os.makedirs(d, exist_ok=True)
        sheet_preview(sh).save(os.path.join(d, "pg_walkers_sheets.png"))
        print("preview in", d)
    if "--grids" in argv:
        d = argv[argv.index("--grids") + 1]
        os.makedirs(d, exist_ok=True)
        for n, a in sh.items():
            grid_preview(to_rgba(a, pal_of(n)), k=8).save(os.path.join(d, f"pg_{n}_grid.png"))


if __name__ == "__main__":
    main(sys.argv[1:])
