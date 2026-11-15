"""Overworld walkers for the Oikoumene's batch 1: the Troad, Egypt and the
Black Sea (design/OIKOUMENE.md §4.1, §4.3, §4.5, §6, §7; design/oikoumene/SPRITES.md).

Usage:
    python3 tools/ichor/art/sprites_oikoumene_ow.py [NAME ...] [--write] [--preview DIR]
        [--sheet PNG] [--grids DIR]

--write    writes graphics/object_events/pics/people/ichor/oik/<name>.png
           (144x32, 4bpp indexed) for every walker here, and the three land
           palettes graphics/object_events/palettes/ichor_{troad,kemet,pontos}.pal
--preview  writes DIR/oikoumene_ow_<land>.png, each land's sheets at 4x on
           grass, vanilla Birch first for scale
--sheet    writes every sheet at 2x, one column per land, to PNG (the batch's
           review sheet is design/oikoumene/img/overworld_batch1.png)
--grids    writes DIR/<name>_grid.png, 8x pixel grids for editing

Three palettes, one per land, so a land's map spends one Ichor OBJ palette
slot on all its people:

* TROAD_PAL (OBJ_EVENT_PAL_TAG_ICHOR_TROAD): wheat gold, river blue, Trojan
  red and royal purple, limestone linen. Hero, Priam, Cassandra, Hektor and
  Odysseus, the Trojan townsfolk, and the Hoplite, Charioteer and Shepherd of Ida.
* KEMET_PAL (OBJ_EVENT_PAL_TAG_ICHOR_KEMET): white linen, gold, lapis,
  malachite and carnelian, as on the tomb walls. Three skin tones in one
  chain: men red-brown (s/S), women and Helen lighter (S/w), the way Egyptian
  painters told them apart. Proteus, Helen, the Egyptian townsfolk, and the
  Priest of the Sun, Scribe of Thoth, Embalmer, Nile Boatman and Phoenician.
* PONTOS_PAL (OBJ_EVENT_PAL_TAG_ICHOR_PONTOS): dark sea green, bronze, gold,
  iron and Hecate's night. Colchians are darker-skinned with tight curls
  (Herodotus 2.104) on s/S; the Greeks among them (the Argonaut, Phineus) take
  S/w. Aietes, Medea, Phineus, the Colchian townsfolk, and the Argonaut,
  Sorceress and Chalybes Smith.

The bodies are sprites_folk.py's archetypes, so these foreigners keep the
islanders' proportions, outline and step bob: drawn by the same painter. Two
role pairs are added to them here: the arms (body rows b2-b4) become A/Z and
every other skin pixel G/J, so sleeves and a land's skin tone are a role
mapping, not a redraw. X/Y (shins) default to G/J, so trousers and greaves
are roles too.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, Palette, save_indexed, to_rgba, upscale, grid_preview  # noqa: E402
from sprites_folk import ARCHETYPES as FOLK_ARCH, W, H, FEET_ROW, _paint, build_frame  # noqa: E402
from sprites_npc import checker_bg, ref_rgba  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

OUT_DIR = os.path.join(ROOT, "graphics/object_events/pics/people/ichor/oik")
PAL_DIR = os.path.join(ROOT, "graphics/object_events/palettes")

# --------------------------------------------------------------------------
# Palettes. Letters follow the cast and folk palettes where the role matches
# (k ink, b brown, s/S skin, l/L linen, o/O bronze and gold, n/B blue, y gray).
# None of them is a role letter (A Z C Q T F X Y).
# --------------------------------------------------------------------------

TROAD_COLORS = [
    # char, name, rgb                       used for
    ("k", "ink", (32, 24, 24)),            # outlines, eyes, black hair
    ("b", "brown", (96, 56, 32)),          # hair, beards, leather, wood
    ("s", "skin_d", (208, 136, 88)),       # skin shadow
    ("S", "skin_l", (240, 192, 144)),      # skin
    ("l", "linen_d", (200, 184, 152)),     # linen and fleece shadow
    ("L", "linen_l", (248, 240, 216)),     # linen, white hair, limestone
    ("y", "gray", (144, 144, 152)),        # gray hair, beard shadow, iron
    ("o", "bronze", (192, 128, 48)),       # bronze, wheat shadow, felt
    ("O", "gold", (240, 200, 88)),         # gold, wheat, lamp flame
    ("r", "red_d", (136, 32, 40)),         # Trojan red shadow
    ("c", "red", (216, 72, 48)),           # Phrygian caps, crests, veils
    ("n", "blue_d", (32, 64, 136)),        # river blue shadow, night
    ("B", "blue", (72, 128, 200)),         # river blue
    ("p", "purple_d", (88, 40, 104)),      # royal purple shadow, hair sheen
    ("P", "purple", (144, 80, 160)),       # royal purple
]

KEMET_COLORS = [
    ("k", "ink", (32, 24, 24)),            # outlines, kohl, wigs
    ("b", "brown", (96, 56, 32)),          # wood, leather, Nile mud
    ("s", "skin_d", (144, 72, 40)),        # men's skin shadow
    ("S", "skin_m", (192, 112, 64)),       # men's skin; women's shadow
    ("w", "skin_l", (232, 168, 104)),      # women's skin, Helen's
    ("l", "linen_d", (200, 192, 168)),     # linen shadow
    ("L", "linen_l", (248, 248, 232)),     # bleached linen
    ("o", "gold_d", (200, 136, 32)),       # gold shadow, leopard
    ("O", "gold", (248, 208, 80)),         # gold, Helen's hair
    ("n", "lapis_d", (32, 48, 136)),       # lapis shadow, wig sheen
    ("B", "lapis", (72, 112, 200)),        # lapis
    ("v", "mal_d", (24, 112, 96)),         # malachite shadow
    ("g", "malachite", (88, 176, 136)),    # malachite
    ("u", "carnelian", (192, 72, 40)),     # carnelian, sun disc, phoinix red
    ("p", "purple", (112, 40, 96)),        # Tyrian purple
]

PONTOS_COLORS = [
    ("k", "ink", (32, 24, 24)),            # outlines, curls
    ("b", "brown", (88, 56, 40)),          # leather, wood, curl sheen
    ("s", "skin_d", (120, 72, 48)),        # Colchian skin shadow
    ("S", "skin_m", (168, 112, 72)),       # Colchian skin; Greek shadow
    ("w", "skin_l", (232, 176, 128)),      # Greek skin (Argonaut, Phineus)
    ("l", "linen_d", (200, 184, 152)),     # linen shadow
    ("L", "linen_l", (248, 240, 216)),     # Colchian linen, white hair, the dove
    ("o", "bronze", (184, 120, 40)),       # Aia's bronze
    ("O", "gold", (248, 200, 80)),         # Helios's gold
    ("y", "iron", (128, 128, 136)),        # Chalybes iron, gray hair
    ("e", "sea_d", (24, 72, 72)),          # Black Sea shadow
    ("E", "sea", (56, 136, 120)),          # Black Sea green
    ("r", "wine", (128, 32, 48)),          # Medea's crimson
    ("c", "flame", (224, 88, 40)),         # torch, forge
    ("p", "night", (72, 40, 96)),          # Hecate's night
]


def _pal(colors):
    return Palette([(name, rgb) for _, name, rgb in colors]), {ch: name for ch, name, _ in colors}


PALETTES = {
    "troad": _pal(TROAD_COLORS),
    "kemet": _pal(KEMET_COLORS),
    "pontos": _pal(PONTOS_COLORS),
}
PAL_FILES = {"troad": "ichor_troad.pal", "kemet": "ichor_kemet.pal", "pontos": "ichor_pontos.pal"}

# --------------------------------------------------------------------------
# Archetypes: sprites_folk's, with the body's skin turned into roles A and Z.
# --------------------------------------------------------------------------

def _skin_roles(rows):
    """Body rows 2-4 are the arms (A light, Z shade: sleeves or bare skin);
    every other skin pixel (neck, hands) is G/J, bare skin."""
    out = []
    for i, r in enumerate(rows):
        m = {"S": "A", "s": "Z"} if 2 <= i <= 4 else {"S": "G", "s": "J"}
        out.append("".join(m.get(ch, ch) for ch in r))
    return out


ARCH = {name: {d: {p: _skin_roles(rows) for p, rows in poses.items()}
               for d, poses in dirs.items()}
        for name, dirs in FOLK_ARCH.items()}
POSES = ("stand", "walk0", "walk1")
DIRS = ("down", "up", "left")


def _resolve(rows, roles):
    """Map role letters to palette letters. G/J (bare skin) default to S/s;
    A/Z (arms) and X/Y (shins) default to the skin, so a spec only names the
    roles it changes."""
    g, j = roles.get("G", "S"), roles.get("J", "s")
    m = {"G": g, "J": j, "A": g, "Z": j, "X": g, "Y": j}
    m.update(roles)
    return ["".join(m.get(ch, ch) for ch in r) for r in rows]


def pole(x, start, cells):
    """An overlay of short cell strings placed at column x, one per row, for
    staffs, spears and other props that run down the figure."""
    rows = []
    for c in cells:
        r = ["_"] * W
        for i, ch in enumerate(c):
            if ch != "_" and 0 <= x + i < W:
                r[x + i] = ch
        rows.append("".join(r))
    return (start, rows)


def flip_cells(cells, width):
    """Mirror pole cells left to right inside `width` columns."""
    return [c.ljust(width, "_")[::-1] for c in cells]


def figure(spec, d, pose):
    """The figure for one direction and pose as resolved palette rows. A
    spec's `recolor` swaps palette letters in its head and overlays (not its
    body roles), to reuse a drawing in other colours."""
    rc = spec.get("recolor", {})

    def swap(rows):
        return ["".join(rc.get(ch, ch) for ch in r) for r in rows]

    head = swap(spec["head"][d])
    body = ARCH[spec["arch"]][d][pose]
    fig = list(head) + list(body)
    over = spec.get("over", {}).get(d, {})
    keys = ["all", "stand"] if pose == "stand" else ["all", "walk", pose]
    for key in keys:
        for start, rows in over.get(key, []):
            _paint(fig, start, swap(rows), len(head), f"{spec['name']} {d} {pose} [{key}]")
    return _resolve(fig, spec.get("roles", {}))


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
    return np.hstack([frames[k] for k in order])


_B3 = ["................"] * 3
_B2 = ["................"] * 2


# ==========================================================================
# Props, in pole cells (column 0 is the outline side)
# ==========================================================================

def spear(head="O", shaft="o"):
    return ["_k_", "k" + head + "k", "kok", "_" + shaft + "_"] + ["k" + shaft] * 19 + ["kk"]


def staff(top="o", wood="b", n=17):
    return ["_k", "k" + top] + ["k" + wood] * n + ["kk"]


def crook(wood="b", hi="o"):
    return ["_kkk_", "k" + wood + hi + wood + "k", "k" + wood + "k" + wood + "k",
            "k" + wood + "_k_"] + ["k" + wood] * 18 + ["kk"]


def round_shield(rim, field, shade, boss):
    """An 8x8 round shield seen from the front: rim, field, a boss."""
    R, F, D, X = rim, field, shade, boss
    return ["__kkkk__",
            "_k" + R + R + R + R + "k_",
            "k" + R + F + F + F + D + R + "k",
            "k" + R + F + X + X + D + R + "k",
            "k" + R + F + X + X + D + R + "k",
            "k" + R + D + D + D + D + R + "k",
            "_k" + R + R + R + R + "k_",
            "__kkkk__"]


def shield_back(rim, inner, strap):
    R, I, T = rim, inner, strap
    return ["__kkkk__",
            "_k" + R + R + R + R + "k_",
            "k" + R + I + I + I + I + R + "k",
            "k" + R + I + T + T + I + R + "k",
            "k" + R + I + I + I + I + R + "k",
            "k" + R + I + I + I + I + R + "k",
            "_k" + R + R + R + R + "k_",
            "__kkkk__"]


# A hand gripping a pole: on the viewer's left facing down, on the viewer's
# right facing up, in front facing left. The walk frame that would swing
# that hand keeps it on the pole.
GRIP_DOWN = {"all": [("b5", ["__G_____________"])],
             "walk1": [("b5", ["..GGGCCCCCQGGk..", "..kkCCCCCCCQkk.."])]}
GRIP_UP = {"all": [("b5", ["_____________G__"])],
           "walk0": [("b5", ["..kGGCCCCCQGGG..", "..kkCCCCCCCQkk.."])]}
GRIP_LEFT = {"all": [("b4", ["__GJ____________"])]}


def merge(*overs):
    """Merge overlay dicts {pose: [entries]} in order."""
    out = {}
    for o in overs:
        for k, v in o.items():
            out.setdefault(k, []).extend(v)
    return out


# ==========================================================================
# THE TROAD (troad palette)
# ==========================================================================

# Hero of Sestos, Aphrodite's priestess on the Hellespont, who keeps a lamp
# burning every night for a swimmer: golden hair blown out by the strait's
# wind, a night-blue peplos with a gold girdle, and a clay lamp cupped in both
# hands at her waist.
HERO_LAMPKEEPER = dict(
    name="hero_lampkeeper", pal="troad", arch="robe",
    roles=dict(C="B", Q="n", T="L", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kOOOoook....",
            "...kOOoooooook..",
            "..kOooooooooook.",
            "..koooooooooOook",
            "..kooSSooSSoooOk",
            "..koSSSSSSSSoook",
            "..koSkSSSSkSooOk",
            "..koSkSSSSkSook.",
            "..kosSSSSSSsok..",
            "...kossSSssok...",
        ],
        up=[
            ".....kkkkkk.....",
            "....kOOOoook....",
            "...kOOoooooook..",
            "..kOooooooooook.",
            "..kOoooooooOoook",
            "..koOooooooooOok",
            "..kooOooooooooOk",
            "..koooOooooooook",
            "..kooooOoooook..",
            "..koooooooook...",
            "...kooSSSSok....",
        ],
        left=[
            "......kkkkk.....",
            "....kkOOoook....",
            "...kOOoooooook..",
            "..kOooooooooook.",
            "..koooooooooOook",
            "..koSoooooooooOk",
            "..kSSSSSoSoooook",
            "..kSkSSSssoooOok",
            "..kSkSSSSoooook.",
            "..kSSSSSsoook...",
            "...kssSssok.....",
        ],
    ),
    over=dict(
        down={"all": [("b2", ["________O_______", "_______cOc______", "_______cOc______",
                              "..kGGkooookGGk.."])]},
        left={"all": [("b2", ["__O_kAZCCCQk....", "_cOckAZCCCQk....", "_cOckAZTTTTk...."]),
                      ("b5", [".kooooGGCCQk...."])]},
    ),
)

# King Priam, who would rather talk about horses than the war: white hair and
# a long white beard under a gold band, a royal purple robe with a gold key
# hem, and a gold-headed sceptre.
_SCEPTRE = ["_k", "kO", "kO", "kk"] + ["ko"] * 15 + ["kb"]
PRIAM = dict(
    name="priam", pal="troad", arch="robe",
    roles=dict(C="P", Q="p", T="O", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kLLLLLLk....",
            "...kLLLLLLLlk...",
            "..kOOOOOOOOOOk..",
            "..kLLLLLLLLLlk..",
            "..kLSyySSyySyk..",
            "..kLSkSSSSkSyk..",
            "..kySkSSSSkSyk..",
            "..kyLLsSSsLLyk..",
            "...kLLLLLLLLk...",
            "....kyLLLLyk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kLLLLLLk....",
            "...kLLLLLLLlk...",
            "..kOOOOOOOOOOk..",
            "..kLLLLLLLLLlk..",
            "..kLLLLLLLLLlk..",
            "..kLLLLLLLLLyk..",
            "..kyLLLLLLLLyk..",
            "..kyLLLLLLLyyk..",
            "...kyLLLLLLyk...",
            "....ksSSSSsk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkLLLLLk....",
            "...kLLLLLLLLk...",
            "..kOOOOOOOOOOk..",
            "..kLLLLLLLLLlk..",
            "..kyySSSSLLLyk..",
            "..kSSSSSsLLLyk..",
            "..kSkSSSsLLLyk..",
            "..kLkSSLLLLLk...",
            "..kLLLLLLLyk....",
            "...kLLLLLyk.....",
        ],
    ),
    over=dict(
        down=merge({"all": [("b0", ["______LLLy______", "______yLy_______"]),
                            ("b8", ["___OoOoOoOoOo___"]),
                            pole(0, 1, _SCEPTRE)]}, GRIP_DOWN),
        up=merge({"all": [("b8", ["___OoOoOoOoOo___"]),
                          pole(14, 1, flip_cells(_SCEPTRE, 2))]}, GRIP_UP),
        left=merge({"all": [("b8", ["____OoOoOoOo____"]), pole(0, 1, _SCEPTRE)]}, GRIP_LEFT),
    ),
)

# Cassandra, Apollo's seer, freed of her curse and delighted to be wrong:
# loose black hair with a purple sheen under a gold fillet, wide bright eyes,
# a white peplos with a red girdle and a red himation over one shoulder.
CASSANDRA = dict(
    name="cassandra", pal="troad", arch="robe",
    roles=dict(C="L", Q="l", T="c", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kkppkkkk....",
            "...kkpkkkkpkk...",
            "..kOOOOOOOOOOk..",
            "..kkpkkkkkkpkk..",
            "..kkkSSkkSSkkk..",
            "..kkSSSSSSSSkk..",
            "..kkSkSSSSkSkk..",
            "..kkSBSSSSBSkk..",
            "..kpsSSSSSSspk..",
            "..kpksSSSSskpk..",
        ],
        up=[
            ".....kkkkkk.....",
            "....kkppkkkk....",
            "...kkpkkkkpkk...",
            "..kOOOOOOOOOOk..",
            "..kkpkkkkkpkkk..",
            "..kkpkkkkkpkkk..",
            "..kkkpkkkkkpkk..",
            "..kkkpkkkkkpkk..",
            "..kkpkkkkkpkkk..",
            "..kkpkkkkkpkkk..",
            "..kkkpkkkkkpkk..",
        ],
        left=[
            "......kkkkk.....",
            "....kkppkkkk....",
            "...kkpkkkkkpk...",
            "..kOOOOOOOOOOk..",
            "..kkkkkkkpkkkk..",
            "..kkSkkkkkkpkk..",
            "..kSSSSkkkkkkk..",
            "..kSkSSSkkpkkk..",
            "..kSBSSSSkkkkk..",
            "..ksSSSSkkpkkk..",
            "...kssskkkkkpk..",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["..kp______cc_pk.", "..kk_____cccrkk.", "________cccr____",
                              "_______cccr_____", "______cccr______", "_____cccr_______",
                              "____rccr________", "___krr__________"])]},
        up={"all": [("b0", ["..kkpkkkkkpkkk..", "..kkpkkkkkpkkk..", "...kkpkkkkpkk...",
                            "....kkpkkpkk....", ".....kkkkkk.....", "______cccr______",
                            "_______rccr_____", "__________rrk___"])]},
        left={"all": [("b0", ["_________kpk____", "_________kkpk___", "__________kpk___",
                              "__________kk____"]),
                      ("b2", ["_____ccr________", "____cccr________", "_____rr_________"])]},
    ),
)

# Prince Hektor of the shining helm, the Troad's champion: a bronze helmet with
# cheek-pieces and a tall red horsehair crest, a bronze cuirass over a royal
# purple chiton, bronze greaves, a spear, and a purple shield with a gold boss.
_HEK_SHIELD = round_shield("o", "P", "p", "O")
HEKTOR = dict(
    name="hektor", pal="troad", arch="tunic",
    roles=dict(C="P", Q="p", T="o", F="b", X="O", Y="o"),
    head=dict(
        down=[
            "......kkkk......",
            ".....kcccrk.....",
            ".....kcccrk.....",
            ".....kccrrk.....",
            "....kkccrrkk....",
            "...kOOOoooobk...",
            "..kOOoooooobbk..",
            "..kOoooooooobk..",
            "..kkkkkkkkkkkk..",
            "..koSSSSSSSSbk..",
            "..koSkSSSSkSbk..",
            "..koSkSSSSkSbk..",
            "..kosSSSSSSsbk..",
            "...kokSSSSkbk...",
            "....kksssskk....",
        ],
        up=[
            "......kkkk......",
            ".....kcccrk.....",
            ".....kcccrk.....",
            ".....kccrrk.....",
            "....kkccrrkk....",
            "...kOOOcroobk...",
            "..kOOoocroobbk..",
            "..kOooocrooobk..",
            "..kOoooorooobk..",
            "..koooooooobbk..",
            "..koooooooobbk..",
            "..koooooooobbk..",
            "..kooooooooobk..",
            "...kooooooobk...",
            "....kksSSskk....",
        ],
        left=[
            "........kkk.....",
            "......kkccck....",
            ".....kcccccrk...",
            "....kccccrrrrk..",
            "....kkkkkkkrrrk.",
            "...kOOOoooookrrk",
            "..kOOoooooobbkrk",
            "..kOoooooooobk..",
            "..kkkkkkoooobk..",
            "..kSSSSkoooobk..",
            "..kSkSSkooobk...",
            "..kSkSSSoooobk..",
            "..kSSSSSooobk...",
            "...kssSSsobk....",
            "....kksssk......",
        ],
    ),
    over=dict(
        down=merge({"all": [("b0", ["____oO____Oo____", "___oOOOOOOOOo___", "_____OOooOo_____",
                                    "_____oOOOOo_____"]),
                            ("b5", ["_____bPbPbp_____", "____PbPbPbPp____"]),
                            pole(8, "b0", _HEK_SHIELD), pole(0, 0, spear())]}, GRIP_DOWN,
                   {"walk1": [("b5", ["..GGGbPbPbpGGk..", "..kkPbPbPbPpkk.."])]}),
        up=merge({"all": [("b0", ["___________O____", "___oOOOOOOOOo___", "_____oOOOOo_____",
                                  "_____oOOOOo_____"]),
                          ("b5", ["_____PbPbPb_____", "____PbPbPbPp____"]),
                          pole(0, "b0", shield_back("o", "b", "k")),
                          pole(13, 0, flip_cells(spear(), 3))]}, GRIP_UP,
                 {"walk0": [("b5", ["..kGGPbPbPbGGG..", "..kkPbPbPbPpkk.."])]}),
        left=merge({"all": [("b0", ["_____oOOo_______", "____oOOOOo______"]),
                            ("b5", ["_____bPbPp______"]), pole(4, "b0", _HEK_SHIELD),
                            pole(0, 0, spear())]}, GRIP_LEFT),
    ),
)

# Odysseus, visiting the plain as he does every year to see how wrong the
# songs were: a felt pilos, a dark beard, a white chiton and a blue chlamys
# pinned at the right shoulder with a gold brooch.
ODYSSEUS = dict(
    name="odysseus", pal="troad", arch="tunic",
    roles=dict(C="L", Q="l", T="b", F="b"),
    head=dict(
        down=[
            "......kkkk......",
            ".....kOoobk.....",
            "....kOooobbk....",
            "...kOoooobbbk...",
            "..kkbbbbbbbbkk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kSSkSSSSkSSk..",
            "..kbbSSSSSSbbk..",
            "...kbbbssbbbk...",
            "....kbbbbbbk....",
        ],
        up=[
            "......kkkk......",
            ".....kOoobk.....",
            "....kOooobbk....",
            "...kOoooobbbk...",
            "..kkbbbbbbbbkk..",
            "..kbbbbbbbbbbk..",
            "..kbbbbbbbbbbk..",
            "..ksbbbbbbbbsk..",
            "..ksbbbbbbbbsk..",
            "...kbbSSSSbbk...",
            "....kbSSSSbk....",
        ],
        left=[
            ".......kkkk.....",
            "......kOoobk....",
            ".....kOooobbk...",
            "....kOooooobbk..",
            "..kkbbbbbbbbbk..",
            "..kbSbbbbbbbbk..",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSbbbbbk...",
            "...kbbbbbbbk....",
            "....kbbbbk......",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["____O___________", "..kBBn__________", "..kBBn__________",
                              "..kBnn__________", "..kBBn__________", "..kBnn__________",
                              "..knn___________"])]},
        up={"all": [("b0", ["...kBBBBBBBnk...", "..kBBBBBBBBBnk..", "..kBBBBBBBBBnk..",
                            "..kBBBBBBBBBnk..", "..kBBBBBBBBBnk..", "..kBBBBBBBBBnk..",
                            "..kknBBnBBnnkk.."])]},
        left={"all": [("b0", ["_________Bnk____", "_________Bnk____", "_________BBnk___",
                              "_________BBnk___", "_________BBnk___", "_________Bnnk___",
                              "__________kk____"])]},
    ),
)

# The Phrygian cap with lappets that Greek painters gave every Trojan, in
# cap colours (light, shade) and hair colour.
def phrygian_cap(c, r, hair="b"):
    h = hair
    return dict(
        down=[
            "......kkkk......",
            "....kkcccckk....",
            "...kcccccccrk...",
            "..kccrrrrrrcrk..",
            "..kcccccccccrk..",
            "..kchhShhShhrk..",
            "..kcSkSSSSkSrk..",
            "..kcSkSSSSkSrk..",
            "..kcsSSSSSSsrk..",
            "..kcrsSSSSsrrk..",
            "...kkksssskkk...",
        ],
        up=[
            "......kkkk......",
            "....kkcccckk....",
            "...kcccccccrk...",
            "..kcccccccccrk..",
            "..kcccccccccrk..",
            "..kccccrcccrrk..",
            "..kcccccccccrk..",
            "..kchhhhhhhhrk..",
            "..kcshhhhhhsrk..",
            "..kcrhhhhhhrrk..",
            "...kkkSSSSkkk...",
        ],
        left=[
            "....kkkkk.......",
            "...kcccccrk.....",
            "..kccrrkkcccrk..",
            "..kcrkkcccccrk..",
            "..kkkcccccccrk..",
            "..khShhhhhcrrk..",
            "..kSSSSShcccrk..",
            "..kSkSSSscccrk..",
            "..kSkSSSScrrk...",
            "..kSSSSSscrk....",
            "...kssSsskk.....",
        ],
    ), {"c": c, "r": r, "h": h}


def recolor(rows_by_dir, m):
    return {d: ["".join(m.get(ch, ch) for ch in r) for r in rows] for d, rows in rows_by_dir.items()}


def cap_head(c, r, hair="b", top=()):
    rows, m = phrygian_cap(c, r, hair)
    out = recolor(rows, m)
    return {d: list(top) + v for d, v in out.items()}


# A Trojan townsman: a red Phrygian cap with its lappets, a wheat-gold tunic
# with a red belt, and blue sleeves and trousers, as Greek painters drew
# Trojans.
TROJAN_M = dict(
    name="trojan_m", pal="troad", arch="tunic",
    roles=dict(C="O", Q="o", T="c", F="b", A="B", Z="n", X="B", Y="n"),
    head=cap_head("c", "r"),
    over=dict(
        down={"all": [("b6", ["____ocococoo____"])]},
        up={"all": [("b6", ["____ocococoo____"])]},
        left={"all": [("b6", ["_____ocoo_______"])]},
    ),
)

# A Trojan woman: a red veil over her hair and down to her shoulders, a blue
# sleeved dress to the floor with a gold girdle and a gold hem.
TROJAN_F = dict(
    name="trojan_f", pal="troad", arch="robe",
    roles=dict(C="B", Q="n", T="O", F="b", A="B", Z="n"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kcccccck....",
            "...kcccccccrk...",
            "..kccccccccrrk..",
            "..kccbbbbbbcrk..",
            "..kcbSSbbSSbrk..",
            "..kcSSSSSSSSrk..",
            "..kcSkSSSSkSrk..",
            "..kOSkSSSSkSOk..",
            "..kcsSSSSSSsrk..",
            "..kcrsSSSSsrrk..",
        ],
        up=[
            ".....kkkkkk.....",
            "....kcccccck....",
            "...kcccccccrk...",
            "..kccccccccrrk..",
            "..kccccccccrrk..",
            "..kcccccrcccrk..",
            "..kccccccrccrk..",
            "..kcccccrcccrk..",
            "..kccccccrccrk..",
            "..kcccccrccrrk..",
            "..kOoOoOoOoOok..",
        ],
        left=[
            "......kkkkk.....",
            "....kkcccccck...",
            "...kcccccccrk...",
            "..kcccccccccrk..",
            "..kcbbbbbcccrk..",
            "..kbSbbbbcccrk..",
            "..kSSSSSbccrrk..",
            "..kSkSSSOccrrk..",
            "..kSkSSSSccrk...",
            "..kSSSSSsccrk...",
            "...kbsSssccrk...",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["..kcr______rck..", "..kcr______rck..", "___k________k___"]),
                      ("b8", ["___OoOoOoOoOo___"])]},
        up={"all": [("b8", ["___OoOoOoOoOo___"])]},
        left={"all": [("b0", ["________ccrk____", "________ccrk____", "________OOk_____"]),
                      ("b8", ["____OoOoOoOo____"])]},
    ),
)

# A Trojan hoplite, the plain's checkpoint guard: a bronze helmet with
# cheek-pieces and a short white crest, a linen corselet over a river-blue
# chiton, greaves, a spear and a blue shield with a bronze rim.
_TRO_SHIELD = round_shield("o", "B", "n", "O")
TROJAN_HOPLITE = dict(
    name="trojan_hoplite", pal="troad", arch="tunic",
    roles=dict(C="B", Q="n", T="o", F="b", X="O", Y="o"),
    head=dict(
        down=_B2 + [
            "......kkkk......",
            ".....kLLLlk.....",
            "....kkLLllkk....",
            "...kOOOoooobk...",
            "..kOOoooooobbk..",
            "..kOoooooooobk..",
            "..kkkkkkkkkkkk..",
            "..koSSSSSSSSbk..",
            "..koSkSSSSkSbk..",
            "..koSkSSSSkSbk..",
            "..kosSSSSSSsbk..",
            "...kokSSSSkbk...",
            "....kksssskk....",
        ],
        up=_B2 + [
            "......kkkk......",
            ".....kLLLlk.....",
            "....kkLLllkk....",
            "...kOOLlooobk...",
            "..kOOooLlooobk..",
            "..kOooooloobbk..",
            "..koooooooobbk..",
            "..koooooooobbk..",
            "..koooooooobbk..",
            "..koooooooobbk..",
            "..kooooooooobk..",
            "...kooooooobk...",
            "....kksSSskk....",
        ],
        left=_B2 + [
            "......kkkk......",
            ".....kLLLLlk....",
            "....kkLLllllk...",
            "...kOOOoooookk..",
            "..kOOoooooobbk..",
            "..kOoooooooobk..",
            "..kkkkkkoooobk..",
            "..kSSSSkoooobk..",
            "..kSkSSkooobk...",
            "..kSkSSSoooobk..",
            "..kSSSSSooobk...",
            "...kssSSsobk....",
            "....kksssk......",
        ],
    ),
    over=dict(
        down=merge({"all": [("b0", ["____LL____Ll____", "___LLLLLLLLLl___", "_____LLLLLl_____",
                                    "_____LLLLLl_____"]),
                            ("b5", ["_____LBLBLn_____", "____BLBLBLBn____"]),
                            pole(8, "b0", _TRO_SHIELD), pole(0, 0, spear())]}, GRIP_DOWN,
                   {"walk1": [("b5", ["..GGGLBLBLnGGk..", "..kkBLBLBLBnkk.."])]}),
        up=merge({"all": [("b0", ["___________L____", "___LLLLLLLLLl___", "_____LLLLLl_____",
                                  "_____LLLLLl_____"]),
                          ("b5", ["_____BLBLBL_____", "____BLBLBLBn____"]),
                          pole(0, "b0", shield_back("o", "b", "k")),
                          pole(13, 0, flip_cells(spear(), 3))]}, GRIP_UP,
                 {"walk0": [("b5", ["..kGGBLBLBLGGG..", "..kkBLBLBLBnkk.."])]}),
        left=merge({"all": [("b5", ["_____LBLBn______"]), pole(4, "b0", _TRO_SHIELD),
                            pole(0, 0, spear())]}, GRIP_LEFT),
    ),
)

# A charioteer, as the bronze one at Delphi stands: short curls under a red
# fillet whose ends fly behind, a long white xystis held by red straps that
# cross over the chest, and a goad with a red tassel.
_GOAD = ["_k", "kc", "kc"] + ["ko"] * 15 + ["kk"]
CHARIOTEER = dict(
    name="charioteer", pal="troad", arch="robe",
    roles=dict(C="L", Q="l", T="c", F="b"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kbobobbk....",
            "...kbobbobbbk...",
            "..kbobbbobbbbk..",
            "..kccccccccccrk.",
            "..kbbSbbSbbSbk.c",
            "..kbSkSSSSkSbk..",
            "..kSSkSSSSkSSk..",
            "..kbsSSSSSSsbk..",
            "...kbssSSssbk...",
            "....kssssssk....",
        ],
        up=[
            ".....kkkkkk.....",
            "....kbobobbk....",
            "...kbobbobbbk...",
            "..kbobbbobbbbk..",
            "..kccccccccccrk.",
            "..kbbbbcrbbbbk..",
            "..kbobbcrbobbk..",
            "..ksbbbcrbbbsk..",
            "..ksbbbbcrbbsk..",
            "...kbbbbcrbbk...",
            "....kbSSScrk....",
        ],
        left=[
            "......kkkkk.....",
            "....kkbobobk....",
            "...kbobbobbbk...",
            "..kbobbbobbbbk..",
            "..kcccccccccrrcc",
            "..kbSbbbbbbbbkrc",
            "..kSSSSSbsbbbk..",
            "..kSkSSSssbbbk..",
            "..kSkSSSSbbbk...",
            "..kSSSSSsbbk....",
            "...kssSssbk.....",
        ],
    ),
    over=dict(
        down=merge({"all": [("b1", ["____c______c____", "_____c____c_____", "______c__c______"]),
                            pole(0, 2, _GOAD)]}, GRIP_DOWN),
        up=merge({"all": [("b1", ["____c______c____", "_____c____c_____", "______cccc______"]),
                          pole(14, 2, flip_cells(_GOAD, 2))]}, GRIP_UP),
        left=merge({"all": [("b1", ["_____cc_________", "______c_________"]),
                            pole(0, 2, _GOAD)]}, GRIP_LEFT),
    ),
)

# A shepherd of Ida, where Paris the prince kept his flocks: a purple
# Phrygian cap, a white fleece over his shoulders, a bronze-brown tunic and a
# crook.
_IDA_CROOK = crook("b", "o")
SHEPHERD_IDA = dict(
    name="shepherd_ida", pal="troad", arch="tunic",
    roles=dict(C="o", Q="b", T="b", F="b"),
    head=cap_head("P", "p", top=_B3),
    over=dict(
        down=merge({"all": [("b0", ["..kLLLkGGkLLlk..", "..kLlLLLLLLlLk..", "______lLLl______"]),
                            pole(0, 0, _IDA_CROOK)]}, GRIP_DOWN),
        up=merge({"all": [("b0", ["..kLLLLLLLLLlk..", "..kLlLLlLLlLlk..", "_____LLlLLl_____",
                                  "_____lLLlLl_____", "______lkll______"]),
                          pole(11, 0, flip_cells(_IDA_CROOK, 5))]}, GRIP_UP),
        left=merge({"all": [("b0", [".....kGGLLLk....", "....kLLLLLLlk...", "________LLlk____",
                                    "________lLlk____", "_________lk_____"]),
                            pole(0, 0, _IDA_CROOK)]}, GRIP_LEFT),
    ),
)

TROAD = [HERO_LAMPKEEPER, PRIAM, CASSANDRA, HEKTOR, ODYSSEUS, TROJAN_M, TROJAN_F,
         TROJAN_HOPLITE, CHARIOTEER, SHEPHERD_IDA]

# ==========================================================================
# EGYPT (kemet palette). Men take skin s/S, women and Helen S/w.
# ==========================================================================

# A black bob wig with a lapis sheen, cut straight at the jaw, and eyes
# lined with kohl.
_WIG_BOB = dict(
    down=[
        ".....kkkkkk.....",
        "....kknnnkkk....",
        "...kknkkkknkk...",
        "..kknkkkkkknkk..",
        "..kkkkkkkkkkkk..",
        "..kkSSSSSSSSkk..",
        "..kkSkkSSkkSkk..",
        "..kkSkSSSSkSkk..",
        "..kksSSSSSSskk..",
        "..knksSSSSsknk..",
        "..kkkkssssskkk..",
    ],
    up=[
        ".....kkkkkk.....",
        "....kknnnkkk....",
        "...kknkkkknkk...",
        "..kknkkkkkknkk..",
        "..kkkkkkkkkkkk..",
        "..kknkkkkkknkk..",
        "..kkkkkkkkkkkk..",
        "..kknkkkkkknkk..",
        "..kkkkkkkkkkkk..",
        "..knkkkkkkkknk..",
        "..kkkkSSSSkkkk..",
    ],
    left=[
        "......kkkkk.....",
        "....kknnnkkk....",
        "...kknkkkknkk...",
        "..kknkkkkkkknk..",
        "..kkkkkkkkkkkk..",
        "..kkSkkkkkknkk..",
        "..kSSSSkkkkkkk..",
        "..kSkkSSkknkkk..",
        "..kSSSSSkkkkkk..",
        "..ksSSSSkknkkk..",
        "...kssssskkkkk..",
    ],
)

# The broad collar, malachite, gold and lapis, and a bare chest (body rows
# b0-b3), facing down.
_COLLAR_DOWN = [("b0", ["...kJgOBBOgJk...", "..kGGgvOOvgGJk..", "..kAZGGGGGJAZk..",
                        "..kAZGGGGGJAZk.."])]
_COLLAR_UP = [("b0", ["...kJgggggJJk...", "..kGGGGGGGGGJk..", "..kAZGGGGGJAZk..",
                      "..kAZGGGGGJAZk.."])]
_COLLAR_LEFT = [("b0", [".....kgOBk......", "....kGGgOJk.....", "....kGAZGJk.....",
                        "....kGAZGJk....."])]

# An Egyptian townsman: a black bob wig, a broad collar, a bare chest and a
# white linen kilt with a pleated apron.
EGYPTIAN_M = dict(
    name="egyptian_m", pal="kemet", arch="tunic",
    roles=dict(C="L", Q="l", T="o", F="b"),
    head=_WIG_BOB,
    over=dict(
        down={"all": _COLLAR_DOWN + [("b5", ["_______ll_______", "______llll______"])]},
        up={"all": _COLLAR_UP},
        left={"all": _COLLAR_LEFT},
    ),
)

# An Egyptian townswoman, lighter-skinned as the tomb painters drew women: a
# long black wig to the chest with a lapis band and a lotus, a broad collar,
# and a white sheath dress to the ankles with a lapis sash.
EGYPTIAN_F = dict(
    name="egyptian_f", pal="kemet", arch="robe",
    roles=dict(C="L", Q="l", T="B", F="b", G="w", J="S"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kknnnkkk....",
            "...kknkkLLnkk...",
            "..kBBBBgLgBBBk..",
            "..kknkkkkkknkk..",
            "..kkkwwkkwwkkk..",
            "..kkwwwwwwwwkk..",
            "..kkwkkwwkkwkk..",
            "..kkwkwwwwkwkk..",
            "..kkSwwwwwwSkk..",
            "..knkSwwwwSknk..",
        ],
        up=[
            ".....kkkkkk.....",
            "....kknnnkkk....",
            "...kknkkkknkk...",
            "..kBBBBBBBBBBk..",
            "..kknkkkkkknkk..",
            "..kkkkkkkkkkkk..",
            "..kknkkkkkknkk..",
            "..kkkkkkkkkkkk..",
            "..kknkkkkkknkk..",
            "..kkkkkkkkkkkk..",
            "..kknkkkkkknkk..",
        ],
        left=[
            "......kkkkk.....",
            "....kknnnkkk....",
            "...kLLkkkknkk...",
            "..kgLgBBBBBBBk..",
            "..kkkkkkkkknkk..",
            "..kkwkkkkkkkkk..",
            "..kwwwwkkkknkk..",
            "..kwkkwwkkkkkk..",
            "..kwwwwwkknkkk..",
            "..kSwwwwkkkkkk..",
            "...kSSSSkknkkk..",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["..knkgOBBOgknk..", "..kkGgvOOvgGkk..", "___k________k___"])]},
        up={"all": [("b0", ["..kknkkkkknkkk..", "..kkkkkkkkkkkk..", "...knkkkkkknk...",
                            "....kkkkkkkk...."])]},
        left={"all": [("b0", [".....kgOBkknk...", "....kGGgOkkkk...", "_________kkk____",
                              "__________k_____"])]},
    ),
)

# Pharaoh Proteus of Memphis, who kept Helen through the war: the striped
# nemes with the uraeus, a false beard, a broad collar, a bare chest, a white
# kilt with a gold apron, and the striped crook.
_HEKA = ["_kkk_", "kOBOk", "kBkOk", "kO_k_"] + ["kB", "kO"] * 7 + ["kk"]
PROTEUS = dict(
    name="proteus", pal="kemet", arch="tunic",
    roles=dict(C="L", Q="l", T="O", F="b"),
    head=dict(
        down=_B2 + [
            ".....kkkkkk.....",
            "....kOOOuOOk....",
            "...kBBBBuBBBk...",
            "..kOOOOOOOOOOk..",
            "..kBBBBBBBBBBk..",
            "..kOkOOOOOOkOk..",
            "..kBkSSSSSSkBk..",
            "..kOSkkSSkkSOk..",
            "..kBSkSSSSkSBk..",
            "..kOsSSSSSSsOk..",
            "..kBksSkkSskBk..",
        ],
        up=_B2 + [
            ".....kkkkkk.....",
            "....kOOOOOOk....",
            "...kBBBBBBBBk...",
            "..kOOOOOOOOOOk..",
            "..kBBBBBBBBBBk..",
            "..kOOOOOOOOOOk..",
            "..kBBBBBBBBBBk..",
            "..kOOOOOOOOOOk..",
            "...kBBBBBBBBk...",
            "....kOOOOOOk....",
            "....kSBOBOSk....",
        ],
        left=_B2 + [
            "......kkkkk.....",
            "....kkOOOOOk....",
            "...kuBBBBBBBk...",
            "..kOOOOOOOOOOk..",
            "..kBBBBBBBBBBk..",
            "..kOkOOOOOOOOk..",
            "..kSSSSkBBBBBk..",
            "..kSkkSkOOOOOk..",
            "..kSSSSkBBBBk...",
            "..kkSSSkOOOk....",
            "...kkksSkBk.....",
        ],
    ),
    over=dict(
        down=merge({"all": [("b0", ["...kOgOkkOgOk...", "..kGBGgOOgGBJk..", "..kAZGGGGGJAZk..",
                                    "..kAZGGGGGJAZk.."]),
                            ("b5", ["_______OO_______", "______oOOo______"]),
                            pole(0, 0, _HEKA)]}, GRIP_DOWN),
        up=merge({"all": [("b0", ["...kJGOBOGJk....", "..kGGGBOGGGGJk..", "..kAZGGGGGJAZk..",
                                  "..kAZGGGGGJAZk.."]),
                          pole(11, 0, flip_cells(_HEKA, 5))]}, GRIP_UP),
        left=merge({"all": [("b0", [".....kgOBk......", "....kGGgOJk.....", "....kGAZGJk.....",
                                    "....kGAZGJk....."]),
                            ("b5", ["_____OOo________"]), pole(0, 0, _HEKA)]}, GRIP_LEFT),
    ),
)

# Helen of Sparta, the Stranger in Proteus's temple, who never left: golden
# hair in a knot with a lapis ribbon, a white peplos, a lapis himation over
# one shoulder and a gold girdle. Greek dress among the Egyptians.
def _recolor_rows(rows, m):
    return ["".join(m.get(ch, ch) for ch in r) for r in rows]


_HELEN_MAP = {"b": "o", "u": "O", "O": "B", "S": "w", "s": "S"}
HELEN = dict(
    name="helen", pal="kemet", arch="robe",
    roles=dict(C="L", Q="l", T="O", F="b", G="w", J="S"),
    head=dict(
        down=_recolor_rows([
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
        ], _HELEN_MAP),
        up=_recolor_rows([
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
        ], _HELEN_MAP),
        left=_recolor_rows([
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
        ], _HELEN_MAP),
    ),
    over=dict(
        down={"all": [("b0", ["__________BB____", "_________BBBn___", "________BBBn____",
                              "_______BBBn_____", "______BBBn______", "_____BBBn_______",
                              "____nBBn________", "___knn__________"])]},
        up={"all": [("b0", ["____BB__________", "___nBBB_________", "____nBBB________",
                            "_____nBBB_______", "______nBBB______", "_______nBBB_____",
                            "________nBBn____", "__________nnk___"])]},
        left={"all": [("b0", ["_____BBB________", "____kBBBn_______"]),
                      ("b2", ["_________Bn_____", "_________Bn_____", "_________nn_____",
                              "_________nk_____"])]},
    ),
)

# A priest of the Sun at Heliopolis: a shaved head, eyes lined with kohl, a
# leopard skin over a long white robe, and a staff crowned with the red disc.
_SUN_STAFF = ["_kkk_", "kuuuk", "kuOuk", "kuuuk", "_kkk_"] + ["_kb"] * 18 + ["_kk"]
PRIEST_SUN = dict(
    name="sun_priest", pal="kemet", arch="robe",
    roles=dict(C="L", Q="l", T="o", F="b"),
    head=dict(
        down=_B3 + [
            ".....kkkkkk.....",
            "....kSwwSSSk....",
            "...kSwwSSSSsk...",
            "..kSwSSSSSSSsk..",
            "..kSSSSSSSSSsk..",
            "..kSkkkSSkkksk..",
            "..kSSkSSSSkSsk..",
            ".ksSSkSSSSkSSsk.",
            "..ksSSSSSSSSsk..",
            "...ksSSssSSsk...",
            "....kssSSssk....",
        ],
        up=_B3 + [
            ".....kkkkkk.....",
            "....kSwwSSSk....",
            "...kSwwSSSSsk...",
            "..kSwSSSSSSSsk..",
            "..kSSSSSSSSSsk..",
            "..kSSSSSSSSSsk..",
            "..kSSSSSSSSSsk..",
            ".ksSSSSSSSSSssk.",
            "..ksSSSSSSSSsk..",
            "...ksSSSSSSsk...",
            "....ksSSSSsk....",
        ],
        left=_B3 + [
            "......kkkkk.....",
            "....kkSwwSSk....",
            "...kSwwSSSSsk...",
            "..kSwSSSSSSSsk..",
            "..kSSSSSSSSSsk..",
            "..kkkSSSSSSSsk..",
            "..kSkSSSSSsSsk..",
            "..kSkSSSSsssk...",
            "..kSSSSSSSsSsk..",
            "..ksSSSSSSssk...",
            "...kssSSSssk....",
        ],
    ),
    over=dict(
        down=merge({"all": [("b0", ["__________Oo____", "_________OkOo___", "________OOOko___",
                                    "_______kOOOo____", "______OOkOo_____", "_____OOOOko_____",
                                    "____oOkOo_______", "___koo__________"]),
                            pole(0, 0, _SUN_STAFF)]}, GRIP_DOWN),
        up=merge({"all": [("b0", ["____oO__________", "___oOkO_________", "___okOOO________",
                                  "____oOOOk_______", "_____oOkOO______", "_____okOOOO_____",
                                  "_______oOkOo____", "__________ook___"]),
                          pole(11, 0, flip_cells(_SUN_STAFF, 5))]}, GRIP_UP),
        left=merge({"all": [("b0", ["_____OOk________", "____kOOOo_______"]),
                            ("b2", ["_________Oo_____", "_________ko_____", "_________Ok_____",
                                    "_________ok_____"]),
                            pole(0, 0, _SUN_STAFF)]}, GRIP_LEFT),
    ),
)

# A scribe of Thoth: a black wig with a reed pen behind the ear, a white
# sleeved shirt and a kilt to mid-calf with a lapis sash, a papyrus roll in
# his arms, and his palette of red and black ink at his belt.
SCRIBE = dict(
    name="scribe", pal="kemet", arch="midi",
    roles=dict(C="L", Q="l", T="B", F="b", A="L", Z="l"),
    head=dict(
        down=[r[:13] + ("O" if i in (3, 4, 5) else r[13]) + r[14:] for i, r in enumerate(_WIG_BOB["down"])],
        up=_WIG_BOB["up"],
        left=_WIG_BOB["left"],
    ),
    over=dict(
        down={"all": [("b2", ["______kOOOOOk___", "_____kOoooook___", "______kkkkkk____"]),
                      ("b5", ["____kkuk________"])]},
        up={"all": [("b4", ["____kkuk________"])]},
        left={"all": [("b2", ["..kOOOk_________", "..kooOk_________"]),
                      ("b5", ["______kkuk______"])]},
    ),
)

# An embalmer in the jackal mask of Anpu: black, with tall ears, gold eyes and
# the striped headcloth behind, over a long white robe; a roll of linen
# bandage in his hands.
EMBALMER = dict(
    name="embalmer", pal="kemet", arch="robe",
    roles=dict(C="L", Q="l", T="o", F="b"),
    head=dict(
        down=[
            "...kk......kk...",
            "...knk....knk...",
            "...knnk..knnk...",
            "...knnkkkknnk...",
            "..kknnnnnnnnkk..",
            "..kBkknkknkkBk..",
            "..kOkOkkkkOkOk..",
            "..kBkkknnkkkBk..",
            "..kOkkknnkkkOk..",
            "..kBkkknnkkkBk..",
            "..kOkkkkkkkkOk..",
            "..kBk.kkkk.kBk..",
            "...k........k...",
        ],
        up=[
            "...kk......kk...",
            "...knk....knk...",
            "...knnk..knnk...",
            "...knnkkkknnk...",
            "..kkkkkkkkkkkk..",
            "..kkknkkkknkkk..",
            "..kOOOOOOOOOOk..",
            "..kBBBBBBBBBBk..",
            "..kOOOOOOOOOOk..",
            "..kBBBBBBBBBBk..",
            "...kOOOOOOOOk...",
            "....kBBBBBBk....",
            ".....kkSSkk.....",
        ],
        left=[
            ".......kk.......",
            "......knk.......",
            "......knnk......",
            ".....kknnkk.....",
            "....kkkkkkkkk...",
            "...kkknkkkBOBk..",
            "kkkkkOkkkkOBOk..",
            "knkkkkkkkkBOBk..",
            ".kkkkkkkkkOBOk..",
            "....kkkkkBOBk...",
            "....kkkkkOBOk...",
            ".....kkkkBOk....",
            "......kk.kk.....",
        ],
    ),
    over=dict(
        down={"all": [("b4", ["______kLLk______", "..kGGkLllkGGk..."]),
                      ("b0", ["...kBk____kBk...", "..kOk______kOk.."])]},
        up={"all": [("b0", ["....kOBOBOBk....", "....kBOBOBOk....", ".....kkkkkk....."])]},
        left={"all": [("b4", ["__kLk___________", "_kLlGG__________"])]},
    ),
)

# A Nile boatman: a linen headcloth tied with a malachite band, a bare
# sun-darkened chest, a short white kilt, bare feet, and a punting pole taller
# than he is.
_PUNT = ["_k", "ko"] + ["ko"] * 20 + ["kk"]
NILE_BOATMAN = dict(
    name="nile_boatman", pal="kemet", arch="tunic",
    roles=dict(C="L", Q="l", T="g", F="s"),
    head=dict(
        down=_B3 + [
            ".....kkkkkk.....",
            "....kLLLLLLk....",
            "...kLLLLLLLlk...",
            "..kLLLLLLLLLlk..",
            "..kggggggggvvk..",
            "..kLSSSSSSSSlk..",
            "..kLSkSSSSkSlk..",
            "..kSSkSSSSkSSk..",
            "..kssSSSSSSssk..",
            "...ksSSSSSSsk...",
            "....kssSSssk....",
        ],
        up=_B3 + [
            ".....kkkkkk.....",
            "....kLLLLLLk....",
            "...kLLLLLLLlk...",
            "..kLLLLLLLLLlk..",
            "..kggggggggvvk..",
            "..kLLLLLLLLLlk..",
            "..kLLLLLLLLLlk..",
            "..ksLLLLLLLlsk..",
            "..ksllllllllsk..",
            "...kkkSSSSkkk...",
            "....ksSSSSsk....",
        ],
        left=_B3 + [
            "......kkkkk.....",
            "....kkLLLLLk....",
            "...kLLLLLLLlk...",
            "..kLLLLLLLLLlk..",
            "..kgggggggggvk..",
            "..kSSSSSLLLLlk..",
            "..kSSSSSsLLLlk..",
            "..kSkSSSsLLLlk..",
            "..kSkSSSSlllk...",
            "..kSSSSSsssk....",
            "...kssSssk......",
        ],
    ),
    over=dict(
        down=merge({"all": [("b0", ["...kGGGGGGGJk...", "..kGGGGGGGGGJk..", "..kAZGJGGJGAZk..",
                                    "..kAZGGJJGGAZk.."]),
                            pole(0, 0, _PUNT)]}, GRIP_DOWN),
        up=merge({"all": [("b0", ["...kGGGGGGGJk...", "..kGGGGJGGGGJk..", "..kAZGGJGGGAZk..",
                                  "..kAZGGJGGGAZk.."]),
                          pole(14, 0, flip_cells(_PUNT, 2))]}, GRIP_UP),
        left=merge({"all": [("b0", [".....kGGJk......", "....kGGJJJk.....", "....kGAZJJk.....",
                                    "....kGAZJJk....."]),
                            pole(0, 0, _PUNT)]}, GRIP_LEFT),
    ),
)

# A Phoenician trader out of Tyre, whose name is the colour he sells
# (phoinix, purple-red): a tall purple cone of a cap, black curls and a curled
# beard, a long phoinix-red robe with a gold hem, and a jar on his hip.
_JAR = ["_kk_", "kbbk", "kbOk", "kbbk", "_kk_"]
PHOENICIAN = dict(
    name="phoenician", pal="kemet", arch="robe",
    roles=dict(C="u", Q="p", T="O", F="b"),
    head=dict(
        down=_B2 + [
            ".......kk.......",
            "......kupk......",
            ".....kuuppk.....",
            "....kuuuppk.....",
            "...kkkkkkkkkk...",
            "..kkbkbkkbkbkk..",
            "..kbSSSSSSSSbk..",
            "..kbSkSSSSkSbk..",
            "..kSSkSSSSkSSk..",
            "..kkbSSSSSSbkk..",
            "...kkbkbbkbkk...",
        ],
        up=_B2 + [
            ".......kk.......",
            "......kupk......",
            ".....kuuppk.....",
            "....kuuuppk.....",
            "...kkkkkkkkkk...",
            "..kkbkbkkbkbkk..",
            "..kbkbkbbkbkbk..",
            "..kkbkbkkbkbkk..",
            "..ksbkbkkbkbsk..",
            "...kkbkkbkbkk...",
            "....kkSSSSkk....",
        ],
        left=_B2 + [
            "........kk......",
            ".......kupk.....",
            "......kuuppk....",
            ".....kuuuppk....",
            "...kkkkkkkkkk...",
            "..kbbkbkkbkbk...",
            "..kbSbkbkbkbbk..",
            "..kSSSSSbkbkbk..",
            "..kSkSSSskbkbk..",
            "..kSkSSbbkbkk...",
            "...kbkbbkbk.....",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["______kbbk______", "_______kk_______"]),
                      ("b8", ["___OoOoOoOoOo___"]), pole(11, "b3", _JAR)]},
        up={"all": [("b8", ["___OoOoOoOoOo___"]), pole(1, "b3", _JAR)]},
        left={"all": [("b8", ["____OoOoOoOo____"]), pole(7, "b3", _JAR)]},
    ),
)

EGYPT = [PROTEUS, HELEN, EGYPTIAN_M, EGYPTIAN_F, PRIEST_SUN, SCRIBE, EMBALMER,
         NILE_BOATMAN, PHOENICIAN]

# ==========================================================================
# THE BLACK SEA (pontos palette). Colchians take skin s/S, Greeks S/w.
# ==========================================================================

# Tight black curls (Herodotus 2.104: the Colchians are dark and woolly-haired)
# and a short curled beard.
_CURLS = dict(
    down=[
        "....kk.kk.kk....",
        "...kbkkbkkbkk...",
        "..kkbkkbkkbkkk..",
        "..kbkkbkkbkkbk..",
        "..kkkbkkbkkbkk..",
        "..kkSSkSSkSSkk..",
        "..kkSkSSSSkSkk..",
        "..kSSkSSSSkSSk..",
        "..kkbSSSSSSbkk..",
        "...kkbkbbkbkk...",
        "....kkbbbbkk....",
    ],
    up=[
        "....kk.kk.kk....",
        "...kbkkbkkbkk...",
        "..kkbkkbkkbkkk..",
        "..kbkkbkkbkkbk..",
        "..kkkbkkbkkbkk..",
        "..kbkkbkkbkkbk..",
        "..kkbkkbkkbkkk..",
        "..ksbkkbkkbksk..",
        "..kskbkkbkkbsk..",
        "...kkbkkbkkk....",
        "....kkSSSSkk....",
    ],
    left=[
        ".....kk.kk.kk...",
        "....kbkkbkkbkk..",
        "...kkbkkbkkbkk..",
        "..kbkkbkkbkkbk..",
        "..kkkbkkbkkbkk..",
        "..kbSkkbkkbkbk..",
        "..kSSSSSbkkbkk..",
        "..kSkSSSskbkbk..",
        "..kSkSSbbkbkk...",
        "...kbkbkbkbk....",
        "....kkbkbk......",
    ],
)

# A Colchian townsman: black curls and beard, a sea-green tunic with sleeves
# of Colchian linen and a bronze belt, and brown leggings.
COLCHIAN_M = dict(
    name="colchian_m", pal="pontos", arch="tunic",
    roles=dict(C="E", Q="e", T="o", F="b", A="L", Z="l", X="b", Y="k"),
    head=_CURLS,
    over=dict(
        down={"all": [("b6", ["____LeLeLeLe____"])]},
        up={"all": [("b6", ["____LeLeLeLe____"])]},
        left={"all": [("b6", ["_____LeLe_______"])]},
    ),
)

# A Colchian townswoman: a veil of Colchian linen over black curls, bronze
# earrings, and a sea-green dress to the floor with a wine-red sash and hem.
_LINEN_VEIL = {"E": "L", "e": "l"}
COLCHIAN_F = dict(
    name="colchian_f", pal="pontos", arch="robe",
    roles=dict(C="E", Q="e", T="r", F="b"),
    recolor=_LINEN_VEIL,
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kEEEEEEk....",
            "...kEEEEEEEek...",
            "..kEEEEEEEEEek..",
            "..kEkbkkbkkbek..",
            "..kEkSSkkSSkek..",
            "..kEkSSSSSSkek..",
            "..kEkSkSSkSkek..",
            "..kEoSkSSkSoek..",
            "..kEksSSSSskek..",
            "..kEekssssskek..",
        ],
        up=[
            ".....kkkkkk.....",
            "....kEEEEEEk....",
            "...kEEEEEEEek...",
            "..kEEEEEEEEEek..",
            "..kEEEEEEEEEek..",
            "..kEEEEeEEEEek..",
            "..kEEEEEeEEEek..",
            "..kEEEEeEEEEek..",
            "..kEEEEEeEEEek..",
            "..kEEEEeEEEEek..",
            "..keeEEEEEeeek..",
        ],
        left=[
            "......kkkkk.....",
            "....kkEEEEEk....",
            "...kEEEEEEEek...",
            "..kEEEEEEEEEek..",
            "..kkbkbEEEEEek..",
            "..kbSkbEEEEEek..",
            "..kSSSSkEEEEek..",
            "..kSkSSoEEEEek..",
            "..kSkSSSkEEEek..",
            "..kSSSSSkEEeek..",
            "...kssskEEeek...",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["..kEe______eEk..", "..kEe______eEk..", "___kk______kk___"]),
                      ("b8", ["___rrrrrrrrrr___"])]},
        up={"all": [("b0", ["..kEEEEeEEEEek..", "..kEEEEEeEEEek..", "..keEEEeEEEeek..",
                            "...kkkkkkkkkk..."]),
                    ("b8", ["___rrrrrrrrrr___"])]},
        left={"all": [("b0", ["_______EEek_____", "_______EEek_____", "________kk______"]),
                      ("b8", ["____rrrrrrrr____"])]},
    ),
)

# King Aietes of Colchis, son of Helios, keeper of the Fleece: a crown of
# gold rays, black curls and beard, a long robe of gold and bronze with a
# wine-red belt and hem, a wine-red cloak, and a gold sceptre.
_AIETES_SCEPTRE = ["_k", "kO", "kO", "kO", "kk"] + ["ko"] * 14 + ["kb"]
AIETES = dict(
    name="aietes", pal="pontos", arch="robe",
    roles=dict(C="O", Q="o", T="r", F="b"),
    head=dict(
        down=[
            "...k..k..k..k...",
            "..kOkkOkkOkkOk..",
            "..kOOOOOOOOOOk..",
            "..kooooooooook..",
        ] + _CURLS["down"][4:],
        up=[
            "...k..k..k..k...",
            "..kOkkOkkOkkOk..",
            "..kOOOOOOOOOOk..",
            "..kooooooooook..",
        ] + _CURLS["up"][4:],
        left=[
            "....k..k..k.....",
            "...kOkkOkkOk....",
            "..kOOOOOOOOOk...",
            "..kooooooooook..",
        ] + _CURLS["left"][4:],
    ),
    over=dict(
        down=merge({"all": [("b0", ["..kr________rk..", "..kr________rk..", "..kr________rk..",
                                    "..kr________rk..", "..kr________rk..", "..kr________rk.."]),
                            ("b8", ["___rrrrrrrrrr___"]),
                            pole(0, 1, _AIETES_SCEPTRE)]}, GRIP_DOWN),
        up=merge({"all": [("b0", ["...krrrrrrrrk...", "..krrrrrrrrrrk..", "..krrrrrrrrrrk..",
                                  "..krrrrrrrrrrk..", "..krrrrrrrrrrk..", "..krrrrrrrrrrk..",
                                  "..kkrrrrrrrrkk.."]),
                          ("b8", ["___rrrrrrrrrr___"]),
                          pole(14, 1, flip_cells(_AIETES_SCEPTRE, 2))]}, GRIP_UP),
        left=merge({"all": [("b0", ["_________rrk____", "_________rrk____", "_________rrrk___",
                                    "_________rrrk___", "_________rrrk___", "_________rrrk___"]),
                            ("b8", ["____rrrrrrrr____"]), pole(0, 1, _AIETES_SCEPTRE)]}, GRIP_LEFT),
    ),
)

# Medea, Hecate's priestess and the Black Sea's champion, the moon to her
# father's sun: a gold crescent on the brow of a night-purple veil over black
# curls, a long-sleeved wine-red robe with a gold girdle and hem, and
# Hecate's torch.
_TORCH = ["_O_", "cOc", "kck"] + ["_ko"] * 9 + ["_kk"]
MEDEA = dict(
    name="medea", pal="pontos", arch="robe",
    roles=dict(C="r", Q="p", T="O", F="b", A="r", Z="p"),
    head=dict(
        down=[
            ".....kkkkkk.....",
            "....kppppppk....",
            "...kppOppOppk...",
            "..kpppOOOOpppk..",
            "..kpkbkkkkbkpk..",
            "..kpkSSkkSSkpk..",
            "..kpSSSSSSSSpk..",
            "..kpSkSSSSkSpk..",
            "..kpSkSSSSkSpk..",
            "..kpksSSSSskpk..",
            "..kppkssssskpk..",
        ],
        up=[
            ".....kkkkkk.....",
            "....kppppppk....",
            "...kppppppppk...",
            "..kppppppppppk..",
            "..kppppkpppppk..",
            "..kpppppkppppk..",
            "..kppppkpppppk..",
            "..kpppppkppppk..",
            "..kppppkpppppk..",
            "..kpppppkppppk..",
            "..kppppkppppppk.",
        ],
        left=[
            "......kkkkk.....",
            "....kkppppppk...",
            "...kOkpppppppk..",
            "..kOOkppppppppk.",
            "..kkbkkppppppk..",
            "..kbSkbkppppppk.",
            "..kSSSSkpppppk..",
            "..kSkSSkpppppk..",
            "..kSkSSSkppppk..",
            "..kSSSSkpppppk..",
            "...kssskppppk...",
        ],
    ),
    over=dict(
        down=merge({"all": [("b0", ["..kp________pk..", "..kp________pk..", "___k________k___"]),
                            ("b8", ["___OoOoOoOoOo___"]),
                            pole(-1, 4, _TORCH)]}, GRIP_DOWN),
        up=merge({"all": [("b0", ["..kppppkppppk...", "..kpppppkpppk...", "...kppppkppk....",
                                  "....kkkkkkkk...."]),
                          ("b8", ["___OoOoOoOoOo___"]),
                          pole(12, 4, flip_cells(_TORCH, 3))]}, GRIP_UP),
        left=merge({"all": [("b0", ["________ppk_____", "________pppk____", "_________ppk____",
                                    "_________kk_____"]),
                            ("b8", ["____OoOoOoOo____"]), pole(-1, 4, _TORCH)]}, GRIP_LEFT),
    ),
)

# Phineus, the blind seer of Salmydessos, who can't see the future any more
# and misses the Harpies: wild white hair and beard, closed eyes, a worn linen
# robe under a night-purple mantle, a staff, and the dove on his hand.
PHINEUS = dict(
    name="phineus", pal="pontos", arch="robe",
    roles=dict(C="l", Q="y", T="p", F="b", G="w", J="S"),
    head=dict(
        down=[
            "....kk.kk.kk....",
            "...kLLkLLkLLk...",
            "..kLLLLLLLLLLk..",
            ".kLLlLLLLLLLllk.",
            ".klLLLLLLLLLLyk.",
            "..kLyyLLLLyyLyk.",
            "..kLwwwwwwwwyk..",
            "..kywkkwwkkwyk..",
            "..kyLLSwwSLLyk..",
            "...kLLLLLLLLk...",
            "....kyLLLLyk....",
        ],
        up=[
            "....kk.kk.kk....",
            "...kLLkLLkLLk...",
            "..kLLLLLLLLLLk..",
            ".kLLlLLLLLLLllk.",
            ".klLLLLLLLLLLyk.",
            ".klLLLLLLLLLLyk.",
            "..kLLLLlLLLLyk..",
            "..kyLLLLLLLLyk..",
            "..kyLLlLLLLyyk..",
            "...kyLLLLLLyk...",
            "....kSwwwwSk....",
        ],
        left=[
            ".....kk.kk.kk...",
            "....kLLkLLkLLk..",
            "...kLLLLLLLLLk..",
            "..kLLLLLLLLLLlk.",
            "..kyyLLLLLLLLyk.",
            "..kwwwwwLLLLLyk.",
            "..kwwwwwSLLLLyk.",
            "..kwkkwwSLLLyk..",
            "..kLLwwLLLLLk...",
            "..kLLLLLLLyk....",
            "...kLLLLLyk.....",
        ],
    ),
    over=dict(
        down=merge({"all": [("b0", ["______LLLy______", "______yLy_______"]),
                            ("b1", ["...pp______pp___", "...pp______pp___", "...pp______pp___",
                                    "...ppp____ppp___"]),
                            ("b2", ["___________kk___", "__________oLLk__", "__________kLLLkk",
                                    "_________kGkLlLk", "__________kkkkk_"]),
                            pole(0, 1, staff("o", "b", 17))]}, GRIP_DOWN),
        up=merge({"all": [("b0", ["...kppppppppk...", "..kppppppppppk..", "..kppppppppppk..",
                                  "..kppppppppppk..", "..kppppppppppk..", "..kkppppppppkk.."]),
                          pole(14, 1, flip_cells(staff("o", "b", 17), 2))]}, GRIP_UP),
        left=merge({"all": [("b0", ["_________ppk____", "_________ppk____", "_________pppk___",
                                    "_________pppk___"]),
                            ("b3", ["__kLk___________", "_kLLyk__________"]),
                            pole(0, 1, staff("o", "b", 17))]}, GRIP_LEFT),
    ),
)

# An Argonaut, a veteran of the Argo's bench: brown curls and a short beard,
# a white exomis, a red chlamys, and an oar with its blade up.
_OAR = ["_kk_", "kOok", "kOok", "kOob", "kOob", "koob", "_kbk"] + ["_ko"] * 16 + ["_kk"]
ARGONAUT = dict(
    name="argonaut", pal="pontos", arch="tunic",
    roles=dict(C="L", Q="l", T="b", F="b", G="w", J="S"),
    head=dict(
        down=_B3 + [
            ".....kkkkkk.....",
            "....kbobbobk....",
            "...kbobbbobbk...",
            "..kbobbobbbobk..",
            "..kbbbbbbbbbbk..",
            "..kbwwbwwbwwbk..",
            "..kbwkwwwwkwbk..",
            "..kwwkwwwwkwwk..",
            "..kbbwwwwwwbbk..",
            "...kbbbSSbbbk...",
            "....kbbbbbbk....",
        ],
        up=_B3 + [
            ".....kkkkkk.....",
            "....kbobbobk....",
            "...kbobbbobbk...",
            "..kbobbobbbobk..",
            "..kbbbbbbbbbbk..",
            "..kbobbbobbbbk..",
            "..kbbbbbbbbbbk..",
            "..kSbbbbbbbbSk..",
            "..kSbbbbbbbbSk..",
            "...kbbwwwwbbk...",
            "....kbwwwwbk....",
        ],
        left=_B3 + [
            "......kkkkk.....",
            "....kkbobobk....",
            "...kbobbbobbk...",
            "..kbobbobbbobk..",
            "..kbbbbbbbbbbk..",
            "..kbwbbbbbbbbk..",
            "..kwwwwwbSbbbk..",
            "..kwkwwwSSbbbk..",
            "..kwkwwbbbbbk...",
            "...kbbbbbbbk....",
            "....kbbbbk......",
        ],
    ),
    over=dict(
        down=merge({"all": [("b0", ["____O___________", "..kcc___________", "..kcr___________",
                                    "..kcr___________", "..kcc___________", "..kcr___________",
                                    "..krr___________"]),
                            pole(11, 0, _OAR)]},
                   {"all": [("b5", ["___________G____"])],
                    "walk0": [("b5", ["..kcrCCCCCQGGG..", "..kkCCCCCCCQkk.."])]}),
        up=merge({"all": [("b0", ["...kcccccccrk...", "..kcccccccccrk..", "..kcccccccccrk..",
                                  "..kcccccccccrk..", "..kcccccccccrk..", "..kcccccccccrk..",
                                  "..kkrccrccrrkk.."]),
                          pole(1, 0, _OAR)]},
                 {"all": [("b5", ["__G_____________"])]}),
        left=merge({"all": [("b0", ["_________crk____", "_________crk____", "_________ccrk___",
                                    "_________ccrk___", "_________ccrk___", "_________crrk___",
                                    "__________kk____"]),
                            pole(1, 0, _OAR)]}, GRIP_LEFT),
    ),
)

# A Colchian sorceress, Medea's acolyte: a sea-green hood and mantle with
# gold eyes glinting in its shadow, a night-purple dress, and a bronze phial
# of something she brewed.
SORCERESS = dict(
    name="sorceress", pal="pontos", arch="robe",
    roles=dict(C="p", Q="k", T="E", F="b", A="E", Z="e"),
    head=dict(
        down=[
            "......kkkk......",
            ".....kEEEek.....",
            "....kEEEEEek....",
            "...kEEEEEEEek...",
            "..kEEEEEEEEEek..",
            "..kEEkkkkkkEek..",
            "..kEkkSSSSkkek..",
            "..kEkOkSSkOkek..",
            "..kEkSSSSSSkek..",
            "..kEekSSSSkeek..",
            "..kEEekkkkeeek..",
        ],
        up=[
            "......kkkk......",
            ".....kEEEek.....",
            "....kEEEEEek....",
            "...kEEEEEEEek...",
            "..kEEEEEEEEEek..",
            "..kEEEEEEEEEek..",
            "..kEEEEeEEEEek..",
            "..kEEEEeEEEEek..",
            "..kEEEEEeEEEek..",
            "..kEEEEeEEEEek..",
            "..keEEEEEEEeek..",
        ],
        left=[
            "......kkkk......",
            ".....kEEEEk.....",
            "....kEEEEEEk....",
            "...kEEEEEEEek...",
            "..kEEEEEEEEEek..",
            "..kkkkkEEEEEek..",
            "..kSSSkEEEEEek..",
            "..kOkSkEEEEEek..",
            "..kSSSkEEEEEek..",
            "..kSSkEEEEEeek..",
            "...kkEEEEEeek...",
        ],
    ),
    over=dict(
        down={"all": [("b0", ["..kEEe____eEEk..", "..kEEe____eEEk..", "..kEe______eEk..",
                              "..kEe______eEk..", "..kEe______eEk..", "..keek____keek..",
                              "..kkk______kkk.."]),
                      ("b4", ["______kOk_______", "______kok_______"])]},
        up={"all": [("b0", ["...kEEEEEEEek...", "..kEEEEeEEEEek..", "..kEEEEeEEEEek..",
                            "..kEEEEEeEEEek..", "..kEEEEeEEEEek..", "..kEEEEEeEEEek..",
                            "..keEEEeEEEeek..", "...kkkkkkkkkk..."])]},
        left={"all": [("b0", ["_______EEek_____", "______EEEek_____", "______EEEek_____",
                              "______EEEeek____", "______EEEeek____", "______EEEeek____",
                              "______eeeeek____", "_______kkkk_____"]),
                      ("b4", ["__kOk___________", "__kok___________"])]},
    ),
)

# A smith of the Chalybes, who worked iron before anyone: a brown felt pilos,
# black curls and beard, a sooty linen exomis under a leather apron, and an
# iron hammer.
_HAMMER = ["kkkkk", "kLyyk", "kyyyk", "kkkkk", "_ko", "_ko", "_ko", "_ko"]
SMITH = dict(
    name="chalybes_smith", pal="pontos", arch="tunic",
    roles=dict(C="l", Q="y", T="b", F="b"),
    head=dict(
        down=[
            "......kkkk......",
            ".....kOoobk.....",
            "....kOooobbk....",
            "...kOoooobbbk...",
            "..kkkbkkbkkbkk..",
        ] + _CURLS["down"][5:],
        up=[
            "......kkkk......",
            ".....kOoobk.....",
            "....kOooobbk....",
            "...kOoooobbbk...",
            "..kkkbkkbkkbkk..",
        ] + _CURLS["up"][5:],
        left=[
            ".......kkkk.....",
            "......kOoobk....",
            ".....kOooobbk...",
            "....kOoooobbbk..",
            "..kkkkbkkbkkbk..",
        ] + _CURLS["left"][5:],
    ),
    over=dict(
        down=merge({"all": [("b0", ["____GG__________", "___GGJ__________"]),
                            ("b3", ["_____bbbbbb_____", "_____bbbbbb_____", "_____bbbbbb_____",
                                    "_____kbbbbk_____"]),
                            pole(0, 9, _HAMMER)]}, GRIP_DOWN),
        up=merge({"all": [("b0", ["__________GG____", "__________JGG___"]),
                          pole(12, 9, flip_cells(_HAMMER, 4))]}, GRIP_UP),
        left=merge({"all": [("b3", ["___bbb__________", "___bbb__________", "___bbb__________",
                                    "___kbb__________"]),
                            pole(0, 9, _HAMMER)]}, GRIP_LEFT),
    ),
)

PONTOS = [AIETES, MEDEA, PHINEUS, COLCHIAN_M, COLCHIAN_F, ARGONAUT, SORCERESS, SMITH]


# ==========================================================================
# Output
# ==========================================================================

LANDS = {"troad": TROAD, "kemet": EGYPT, "pontos": PONTOS}
WALKERS = [w for land in LANDS.values() for w in land]
BY_NAME = {w["name"]: w for w in WALKERS}


def _font(size):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # Pillow < 10.1
        return ImageFont.load_default()


def sheet_preview(sheets, k=4, cols=2, groups=None, bg=None):
    """Sheets at k times, each frame on a grass checker (or `bg`, an RGBA tile
    16x32 cut from a town), in `cols` columns headed by vanilla Birch, or one
    column per list of names in `groups`."""
    items = [(name, BY_NAME[name]["pal"], to_rgba(arr, PALETTES[BY_NAME[name]["pal"]][0]))
             for name, arr in sheets.items()]
    if groups:
        cols = len(groups)
        chunks = [[it for it in items if it[0] in g] for g in groups]
    else:
        per = -(-len(items) // cols)
        chunks = [items[c * per:(c + 1) * per] for c in range(cols)]
    columns = [[("prof_birch", "vanilla", ref_rgba())] + chunk for chunk in chunks]
    pad, lw, gap = 4, 48, 8
    cw = lw + W * 9 + pad * 8
    rows = max(len(c) for c in columns)
    out = Image.new("RGBA", (cols * cw + (cols - 1) * gap, (H + pad) * rows - pad), (232, 224, 200, 255))
    for c, column in enumerate(columns):
        x0 = c * (cw + gap)
        for i, (_, _, im) in enumerate(column):
            for f in range(9):
                tile = (bg(f, i) if bg else checker_bg(W, H)).copy()
                tile.alpha_composite(im.crop((f * W, 0, (f + 1) * W, H)))
                out.alpha_composite(tile, (x0 + lw + f * (W + pad), i * (H + pad)))
    big = upscale(out, k)
    d = ImageDraw.Draw(big)
    font = _font(4 * k + 2)
    for c, column in enumerate(columns):
        for i, (name, pal, _) in enumerate(column):
            x, y = c * (cw + gap) * k + 4, i * (H + pad) * k + 11 * k
            d.text((x, y), name.replace("_", " "), fill=(32, 24, 24, 255), font=font)
            d.text((x, y + 5 * k), pal, fill=(112, 96, 80, 255), font=font)
    return big


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    grids = args[args.index("--grids") + 1] if "--grids" in args else None
    batch = args[args.index("--sheet") + 1] if "--sheet" in args else None
    write = "--write" in args
    only = [a for a in args if a in BY_NAME]
    sheets = {spec["name"]: build_sheet(spec) for spec in WALKERS if not only or spec["name"] in only}
    if write:
        os.makedirs(OUT_DIR, exist_ok=True)
        for name, arr in sheets.items():
            save_indexed(arr, PALETTES[BY_NAME[name]["pal"]][0], os.path.join(OUT_DIR, name + ".png"))
        for land, (pal, _) in PALETTES.items():
            pal.write_jasc(os.path.join(PAL_DIR, PAL_FILES[land]))
    if pv:
        os.makedirs(pv, exist_ok=True)
        for land, specs in LANDS.items():
            mine = {s["name"]: sheets[s["name"]] for s in specs if s["name"] in sheets}
            if mine:
                sheet_preview(mine).save(os.path.join(pv, f"oikoumene_ow_{land}.png"))
    if batch:
        groups = [[s["name"] for s in specs] for specs in LANDS.values()]
        sheet_preview(sheets, k=2, groups=groups).save(batch)
    if grids:
        os.makedirs(grids, exist_ok=True)
        for name, arr in sheets.items():
            pal = PALETTES[BY_NAME[name]["pal"]][0]
            grid_preview(to_rgba(arr, pal), 8).save(os.path.join(grids, name + "_grid.png"))


if __name__ == "__main__":
    main()
