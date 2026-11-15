"""Overworld walkers for the Theoxenia's two gods drawn from life: Sam and
Apollo, Cami and Demeter (design/SYSTEMS.md §10).

Usage:
    python3 tools/ichor/art/sprites_npc_theoxenia.py [NAME ...] [--write] [--preview DIR]

--write    writes graphics/object_events/pics/people/ichor/<name>.png (4bpp
           indexed, 16x32 frames side by side) and the palette
           graphics/object_events/palettes/ichor_theoxenia.pal
--preview  writes DIR/<name>_grid.png, 8x pixel grids for editing

All four share one palette, THEOX_PAL, loaded under
OBJ_EVENT_PAL_TAG_ICHOR_THEOXENIA. The cast palette has one bronze ramp and
sun-browned hair; these four need a true gold, white and gold, two greens, a
grey-brown shawl, and two distinct hair browns for the people they're drawn
after.

Frames 0-8 are the standard Emerald layout (sprites_npc.py). The extra frames
are played by the animation tables in src/data/object_events/object_event_anims.h:

    sam, apollo   9-11  the lyre strum, facing down (sAnimTable_IchorLyre)
    cami          9     sitting on the well's bench, facing up
                  10    rising from the bench (sAnimTable_IchorCami)
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sprites_lib import ROOT, Palette, save_indexed, to_rgba, grid_preview  # noqa: E402
from sprites_npc import mirror, build_frame  # noqa: E402

OUT_DIR = os.path.join(ROOT, "graphics/object_events/pics/people/ichor")
PAL_PATH = os.path.join(ROOT, "graphics/object_events/palettes/ichor_theoxenia.pal")

THEOX_COLORS = [
    # char, name, rgb                       used for
    ("k", "ink", (32, 24, 24)),            # outlines, eyes
    ("h", "hair_d", (80, 48, 40)),         # Sam's hair, tortoiseshell, sandals
    ("H", "hair_m", (128, 80, 48)),        # Sam's hair light, Cami's hair shadow, leather
    ("c", "chestnut", (168, 104, 64)),      # Cami's hair, tortoiseshell mottle
    ("y", "amber", (208, 144, 56)),        # gold shadow, chestnut in the light
    ("o", "gold", (232, 184, 56)),         # gold, ripe wheat
    ("O", "gold_l", (248, 232, 144)),      # gold highlight
    ("s", "skin_d", (224, 152, 112)),      # skin shadow
    ("S", "skin_l", (248, 208, 176)),      # skin
    ("w", "linen_d", (200, 192, 168)),     # undyed wool and linen, white's shadow
    ("W", "linen_l", (248, 248, 232)),     # the god's white, lyre strings
    ("g", "wool", (136, 120, 104)),        # the grey-brown shawl, cloth shadow, stubble
    ("d", "wool_d", (88, 72, 64)),         # shawl shadow
    ("v", "green_d", (56, 104, 56)),       # Demeter's green, shadow
    ("V", "green", (104, 160, 72)),        # Demeter's green
]
PAL = Palette([(name, rgb) for _, name, rgb in THEOX_COLORS])
LEGEND = {ch: name for ch, name, _ in THEOX_COLORS}


def ov(rows, patch, at=0):
    """Overlay patch rows onto rows from row `at`: '_' keeps, '.' clears."""
    out = list(rows)
    for j, p in enumerate(patch):
        r = list(out[at + j])
        for i, ch in enumerate(p):
            if ch != "_":
                r[i] = ch
        out[at + j] = "".join(r)
    return out


def build(spec):
    """The sheet: the standard nine frames, then spec['extra'] in order."""
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
        frames[d] = build_frame(part["top"], part["stand"], y0, LEGEND, PAL, f"{name} {d} stand")
        for i in (0, 1):
            frames[f"{d}{i}"] = build_frame(part["top"], walk[i], y0 + 1, LEGEND, PAL,
                                            f"{name} {d} walk {i}")
    order = ["down", "up", "left", "down0", "down1", "up0", "up1", "left0", "left1"]
    out = [frames[k] for k in order]
    for i, ex in enumerate(spec.get("extra", [])):
        out.append(build_frame(ex["top"], ex["body"], ex["y0"], LEGEND, PAL,
                               f"{spec['name']} extra {i}"))
    return np.hstack(out)


# ==========================================================================
# Sam: Apollo as a hired herdsman. Short dark-brown hair, full and wavy on
# top, short at the sides; dark brows; a big open grin and light stubble.
# An undyed wool tunic under a short brown cloak, sandals, and in his left
# arm a lyre far too fine for him: a tortoiseshell bowl and gold arms.
# ==========================================================================

SAM_DOWN_TOP = [
    "......kkkkk.....",
    "....kkhHHhhkk...",
    "...khhhhhHHhhk..",
    "..khHHhhhhhHhk..",
    "..khhhhHHhhhhk..",
    "..khhhhhhhhhhk..",
    "..khShhShhShhk..",
    "..sSSkSSSSkSSs..",
    "..sSSkSSSSkSSs..",
    "...gSSkWWkSSg...",
    "....kgsSSsgk....",
]

# the lyre in his left arm (the viewer's right), his right hand at the strings
SAM_DOWN_STAND = [
    "...kdwSSSoSodk..",
    "..kgdwwwwyoOoyk.",
    "..kSdwwwSywWwyk.",
    "..kSswwwSywWwyk.",
    "..kSsHHHHkhchSk.",
    "..kSSwwwwkchckk.",
    "..kkwwwwwwkkkk..",
    "...kkSskkSskk...",
    "....kSskkSsk....",
    "....khhkkhhk....",
]
_DOWN_LEGS_W0 = ["...kkSskkSskk...", "....kSskkhhk....", "....khhk........"]
_DOWN_LEGS_W1 = ["...kkSskkSskk...", "....khhkkSsk....", "........khhk...."]


def legs(body, rows):
    return body[:len(body) - 3] + rows


SAM_UP_TOP = [
    ".....kkkkk......",
    "...kkhhHHhkk....",
    "..khhHHhhhhhk...",
    "..khHhhhhHHhhk..",
    "..khhhhHHhhhhk..",
    "..khhHhhhhhHhk..",
    "..khhhhhhhhhhk..",
    "..shhhhhhhhhhs..",
    "..shhhhhhhhhhs..",
    "...khhhhhhhhk...",
    "....ksSSSSsk....",
]
# the cloak over his back; the lyre's gold horns show past his left shoulder
SAM_UP_STAND = [
    "..okggggggggk...",
    "..kgggggggggdk..",
    "..kSgggggggdSk..",
    "..kSsgggggddsk..",
    "..kSsHHHHHHHsk..",
    "..kSSwwwwwwgSk..",
    "..kkwwwwwwwgkk..",
    "...kkSskkSskk...",
    "....kSskkSsk....",
    "....khhkkhhk....",
]

SAM_LEFT_TOP = [
    "......kkkkk.....",
    "....kkhHHhhkk...",
    "...khhhhhHHhhk..",
    "..khHHhhhhhHhk..",
    "..khhhhHHhhhhk..",
    "..khhhhhhhhhhk..",
    "..kShShhshhhhk..",
    "..kSkSSSshShhk..",
    "..kSkSSSSshhhk..",
    "..kWSSSSShhhk...",
    "...kgsSSsghk....",
]
SAM_LEFT_STAND = [
    ".....kSSkggk....",
    "..o.kwwwwkgdk...",
    "..yOkwwwwkgdk...",
    "..yWySswwkgdk...",
    "..khcSswwkgdk...",
    "..kchkHHHkddk...",
    "...kkwwwwgkk....",
    ".....kSskk......",
    ".....kSsk.......",
    "....khhhk.......",
]
SAM_LEFT_W0 = legs(SAM_LEFT_STAND, ["...kSskkSsk.....", "..kSsk..kSsk....", "..khhk...khhk..."])
SAM_LEFT_W1 = legs(SAM_LEFT_STAND, [".....kSskk......", ".....kSsk.......", "....khhhk......."])

# the strum, facing down: right hand high, low, and high with his eyes shut
# (the hand sweeps from the yoke to the bowl; on the down-stroke the strings
# catch the light)
SAM_STRUM_HIGH = ov(SAM_DOWN_STAND, ["_________Ss_____", "________S_______", "________w_______"], at=1)
SAM_STRUM_LOW = ov(SAM_DOWN_STAND, ["________w__O____", "________SSsO____"], at=2)
SAM_TOP_JOY = ov(SAM_DOWN_TOP, ["_____S____S_____"], at=7)

SAM = dict(
    name="sam",
    y0=10,
    down=dict(top=SAM_DOWN_TOP, stand=SAM_DOWN_STAND,
              walk=[legs(SAM_DOWN_STAND, _DOWN_LEGS_W0), legs(SAM_DOWN_STAND, _DOWN_LEGS_W1)]),
    up=dict(top=SAM_UP_TOP, stand=SAM_UP_STAND,
            walk=[legs(SAM_UP_STAND, _DOWN_LEGS_W0), legs(SAM_UP_STAND, _DOWN_LEGS_W1)]),
    left=dict(top=SAM_LEFT_TOP, stand=SAM_LEFT_STAND, walk=[SAM_LEFT_W0, SAM_LEFT_W1]),
    extra=[
        dict(top=SAM_DOWN_TOP, body=SAM_STRUM_HIGH, y0=10),
        dict(top=SAM_DOWN_TOP, body=SAM_STRUM_LOW, y0=10),
        dict(top=SAM_TOP_JOY, body=SAM_STRUM_HIGH, y0=10),
    ],
)

# ==========================================================================
# Apollo: Sam revealed. The same face and hair under a gold laurel wreath,
# a long white chiton with gold borders, and the lyre all gold. He stands a
# pixel taller than he did.
# ==========================================================================

_WREATH_DOWN = [".o____________o.", ".yo__________oy.", ".oyoOoyoOoyoOoy."]
APOLLO_DOWN_TOP = ov(SAM_DOWN_TOP, _WREATH_DOWN, at=3)
APOLLO_DOWN_STAND = [
    "...kWWSSSSoWok..",
    "..kWWWWWWyoOoyk.",
    "..kSWWWWSyOWOyk.",
    "..kSsWWWSyOWOyk.",
    "..kSsoOookyoySk.",
    "..kSSWWWWkoyokk.",
    "..kkWWWWWWkkkk..",
    "...kWWWWWWWWwk..",
    "...kWWWWWWWwwk..",
    "...kOoooooooyk..",
    "....kyykkyyk....",
]
_ROBE_W0 = ["..kkOoooooooykk.", ".....kyyk......."]
_ROBE_W1 = ["..kkOoooooooykk.", "........kyyk...."]


def hem(body, rows):
    return body[:len(body) - 2] + rows


_WREATH_UP = [".o____________o.", ".yo__________oy.", ".oyoOoyoOoyoOoy."]
APOLLO_UP_TOP = ov(SAM_UP_TOP, _WREATH_UP, at=3)
APOLLO_UP_STAND = [
    "..oOkWWWWWWWWk..",
    "..kWWWWWWWWWWwk.",
    "..kSWWWWWWWWwSk.",
    "..kSsWWWWWWwwsk.",
    "..kSsoOooooooyk.",
    "..kSSWWWWWWWwSk.",
    "..kkWWWWWWWWwkk.",
    "...kWWWWWWWWwk..",
    "...kWWWWWWWwwk..",
    "...kOoooooooyk..",
    "....kyykkyyk....",
]

_WREATH_LEFT = ["______________o.", "_____________oy.", "___oyoOoyoOoyOy."]
APOLLO_LEFT_TOP = ov(SAM_LEFT_TOP, _WREATH_LEFT, at=3)
APOLLO_LEFT_STAND = [
    ".....kSSkWWk....",
    "..o.kWWWWWWwk...",
    "..oOkWWWWWWwk...",
    "..oWOSsWWWWwk...",
    "..kyoSsWWWwwk...",
    "..koykOoyoOyk...",
    "...kkWWWWWWwk...",
    "....kWWWWWWwk...",
    "....kWWWWWwwk...",
    "....kOoooooyk...",
    ".....kyyk.......",
]
APOLLO_LEFT_W0 = hem(APOLLO_LEFT_STAND, ["...kOooooooyk...", "...kyyk.kyyk...."])
APOLLO_LEFT_W1 = hem(APOLLO_LEFT_STAND, ["....kOoooooyk...", ".....kyyk......."])

APOLLO_STRUM_HIGH = ov(APOLLO_DOWN_STAND, ["_________Ss_____", "________S_______", "________W_______"],
                       at=1)
APOLLO_STRUM_LOW = ov(APOLLO_DOWN_STAND, ["________W__O____", "________SSsO____"], at=2)
APOLLO_TOP_JOY = ov(APOLLO_DOWN_TOP, ["_____S____S_____"], at=7)

APOLLO = dict(
    name="apollo",
    y0=9,
    down=dict(top=APOLLO_DOWN_TOP, stand=APOLLO_DOWN_STAND,
              walk=[hem(APOLLO_DOWN_STAND, _ROBE_W0), hem(APOLLO_DOWN_STAND, _ROBE_W1)]),
    up=dict(top=APOLLO_UP_TOP, stand=APOLLO_UP_STAND,
            walk=[hem(APOLLO_UP_STAND, _ROBE_W0), hem(APOLLO_UP_STAND, _ROBE_W1)]),
    left=dict(top=APOLLO_LEFT_TOP, stand=APOLLO_LEFT_STAND, walk=[APOLLO_LEFT_W0, APOLLO_LEFT_W1]),
    extra=[
        dict(top=APOLLO_DOWN_TOP, body=APOLLO_STRUM_HIGH, y0=9),
        dict(top=APOLLO_DOWN_TOP, body=APOLLO_STRUM_LOW, y0=9),
        dict(top=APOLLO_TOP_JOY, body=APOLLO_STRUM_HIGH, y0=9),
    ],
)


# ==========================================================================
# Cami: Demeter as a young woman by the Maiden's Well. A chin-length
# chestnut bob with full blunt bangs to the brows, a slim face and a soft
# smile. A plain undyed peplos, a grey-brown shawl, and caught in the
# shawl's fringe a single ear of ripe wheat.
# ==========================================================================

CAMI_DOWN_TOP = [
    ".....kkkkkk.....",
    "....kcyyccck....",
    "...kcycccccck...",
    "..kcycccccccck..",
    "..kcccccccccck..",
    "..kcccccccccck..",
    "..kcHHHHHHHHck..",
    "..kcSkSSSSkSck..",
    "..kcSkSSSSkSck..",
    "..kcSSSssSSSck..",
    "..kHHsSSSSsHHk..",
]
# the shawl over her shoulders, fringed at the elbow; the peplos to the ankle
CAMI_DOWN_STAND = [
    "...kddSSSSddk...",
    "..kdggdSSdggdk..",
    "..kdgggddgggdk..",
    "..kSdggggggdSk..",
    "..kSkgdgdgdkSk..",
    "..kkwwwwwwwwkk..",
    "..kwwwwwwwwwwk..",
    "..kwwwwwwwwwgk..",
    "...kwwwwwwwgk...",
    "....khhkkhhk....",
]
_PEPLOS_W0 = ["..kkwwwwwwwgkk..", ".....khhk......."]
_PEPLOS_W1 = ["..kkwwwwwwwgkk..", "........khhk...."]

CAMI_UP_TOP = [
    ".....kkkkkk.....",
    "....kcyyccck....",
    "...kcycccccck...",
    "..kcycccccccck..",
    "..kcccccccccck..",
    "..kcccccccccck..",
    "..kcccccccccck..",
    "..kcccccccccck..",
    "..kcccccccccck..",
    "..kHccccccccHk..",
    "..kHHHHHHHHHHk..",
]
# from behind: the shawl over her back, the wheat ear caught in its fringe
CAMI_UP_STAND = [
    "...kddddddddk...",
    "..kdggggggggdk..",
    "..kdggggggggdk..",
    "..kSdggggggdSk..",
    "..kSkgdgOgdkSk..",
    "..kkwwwwywwwkk..",
    "..kwwwwwwwwwwk..",
    "..kwwwwwwwwwgk..",
    "...kwwwwwwwgk...",
    "....khhkkhhk....",
]

CAMI_LEFT_TOP = [
    "......kkkkk.....",
    "....kkcyycck....",
    "...kcycccccck...",
    "..kcycccccccck..",
    "..kcccccccccck..",
    "..kcccccccccck..",
    "..kcHHHcccccck..",
    "..kSkSScccccck..",
    "..kSkSSSccccck..",
    "..kSSsSSccccck..",
    "...kssSkHHHHHk..",
]
CAMI_LEFT_STAND = [
    "....kSSkddk.....",
    "...kddggggdk....",
    "...kSggggggk....",
    "...kSsgggddk....",
    "...kkdgdOdgk....",
    "...kwwwwwwwk....",
    "...kwwwwwwwgk...",
    "...kwwwwwwggk...",
    "....kwwwwwgk....",
    "....kkhhhkk.....",
]
CAMI_LEFT_W0 = ov(CAMI_LEFT_STAND, ["...kwwwwwwggk...", "..kkwwwwwwgkk...", "..khhk..khhk...."], at=7)
CAMI_LEFT_W1 = ov(CAMI_LEFT_STAND, ["...kwwwwwwwgk...", "....kkwwwwkk....", ".....khhhk......"], at=7)

# Sitting on the well's bench with her back to us, facing the well: three
# rows lower than standing, her skirt spread over the seat.
CAMI_SIT_BODY = [
    "...kddddddddk...",
    "..kSdggggggdSk..",
    "..kSkgdgOgdkSk..",
    "..kwwwwwywwwwk..",
    "...kkkwwwwkkk...",
]
# Rising from the bench, turning toward you, halfway up
CAMI_RISE_BODY = [
    "....kSSkddk.....",
    "...kddggggdk....",
    "...kSggggggk....",
    "..kkSsgdOdgk....",
    "..kwwwwwwwwk....",
    ".kwwwwwwwwgk....",
    ".kkwwwkwwwgk....",
    "..khhk.kwgk.....",
    "........khk.....",
]

CAMI = dict(
    name="cami",
    y0=10,
    down=dict(top=CAMI_DOWN_TOP, stand=CAMI_DOWN_STAND,
              walk=[hem(CAMI_DOWN_STAND, _PEPLOS_W0), hem(CAMI_DOWN_STAND, _PEPLOS_W1)]),
    up=dict(top=CAMI_UP_TOP, stand=CAMI_UP_STAND,
            walk=[hem(CAMI_UP_STAND, _PEPLOS_W0), hem(CAMI_UP_STAND, _PEPLOS_W1)]),
    left=dict(top=CAMI_LEFT_TOP, stand=CAMI_LEFT_STAND, walk=[CAMI_LEFT_W0, CAMI_LEFT_W1]),
    extra=[
        dict(top=CAMI_UP_TOP, body=CAMI_SIT_BODY, y0=10),
        dict(top=CAMI_LEFT_TOP, body=CAMI_RISE_BODY, y0=11),
    ],
)


# ==========================================================================
# Demeter: Cami revealed. The same face and bob under a crown of ripe wheat,
# a green peplos under a gold himation, and a sheaf of wheat in her left arm.
# She stands a pixel taller than she did.
# ==========================================================================

# the crown: four ripe ears standing on a gold band
_EARS = ["....O.O..O.O....", "....o.o..o.o...."]
_BAND = ["....kyoyyoyk....", "....kOoyyoOk...."]
DEMETER_DOWN_TOP = _EARS + ov(CAMI_DOWN_TOP, _BAND)
DEMETER_UP_TOP = _EARS + ov(CAMI_UP_TOP, _BAND)
DEMETER_LEFT_TOP = (["......O.O.O.....", "......o.o.o....."]
                    + ov(CAMI_LEFT_TOP, ["_____kyoyoyk____", "____kOoyyoOk____"]))

# a green peplos with a gold overfold, girdle and hem; the sheaf in her left arm
DEMETER_DOWN_STAND = [
    "...kVVSSSSVVkO.O",
    "..kVVVVSSVVVkoOy",
    "..kVOooOOooVSyoy",
    "..kSVVVVVVVSkHHk",
    "..kSkyoOOoykyoyk",
    "..kSkVVVVVVkyky.",
    "..kkVVVVVVVVkk..",
    "..kVVVVVVVVVvk..",
    "..kVVVVVVVVvvk..",
    "..kOooooooooyk..",
    "....kyykkyyk....",
]
DEMETER_UP_STAND = ov(mirror(DEMETER_DOWN_STAND), ["___kVVVVVVVVk___", "___VVVVVVVVVk___"], at=0)
DEMETER_LEFT_STAND = [
    "....kSSkOkOk....",
    "...kVVVkoOok....",
    "...kVVSyoyVk....",
    "...kVVSHHHVk....",
    "...kyoOyoyok....",
    "...kVVVkyykk....",
    "...kVVVVVVVk....",
    "...kVVVVVVvk....",
    "...kVVVVVvvk....",
    "...kOoooooyk....",
    "....kyyyk.......",
]
DEMETER_LEFT_W0 = hem(DEMETER_LEFT_STAND, ["..kOooooooyk....", "..kyyk.kyyk....."])
DEMETER_LEFT_W1 = hem(DEMETER_LEFT_STAND, ["...kOoooooyk....", "....kyyyk......."])

DEMETER = dict(
    name="demeter",
    y0=7,
    down=dict(top=DEMETER_DOWN_TOP, stand=DEMETER_DOWN_STAND,
              walk=[hem(DEMETER_DOWN_STAND, _ROBE_W0), hem(DEMETER_DOWN_STAND, _ROBE_W1)]),
    up=dict(top=DEMETER_UP_TOP, stand=DEMETER_UP_STAND,
            walk=[hem(DEMETER_UP_STAND, _ROBE_W0), hem(DEMETER_UP_STAND, _ROBE_W1)]),
    left=dict(top=DEMETER_LEFT_TOP, stand=DEMETER_LEFT_STAND,
              walk=[DEMETER_LEFT_W0, DEMETER_LEFT_W1]),
)

SPECS = {"sam": SAM, "apollo": APOLLO, "cami": CAMI, "demeter": DEMETER}


def main():
    args = sys.argv[1:]
    pv = args[args.index("--preview") + 1] if "--preview" in args else None
    write = "--write" in args
    only = [a for a in args if a in SPECS]
    sheets = {n: build(s) for n, s in SPECS.items() if not only or n in only}
    if write:
        for name, arr in sheets.items():
            save_indexed(arr, PAL, os.path.join(OUT_DIR, name + ".png"))
        PAL.write_jasc(PAL_PATH)
    if pv:
        os.makedirs(pv, exist_ok=True)
        for name, arr in sheets.items():
            grid_preview(to_rgba(arr, PAL), 8).save(os.path.join(pv, name + "_grid.png"))


if __name__ == "__main__":
    main()
