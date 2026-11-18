#!/usr/bin/env python3
"""The reference sheet for STYLE.md §4.8 (Architecture: Gen 3 craft and Greek
forms): Ichor's own art, labelled with the parts and the measurements the
rules give. design/art/architecture_reference.png.

    /usr/bin/python3 tools/ichor/art/architecture_sheet.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import astyra_art as AA  # noqa: E402
import astyra_city_art as CA  # noqa: E402
import astyra_statues as ST  # noqa: E402
import columns as CK  # noqa: E402
import kythera_lib as K  # noqa: E402

S = 3
INK = (240, 230, 200)
LINE = (255, 200, 80)


def img(s):
    im = Image.fromarray(K.composite(s))
    return im.resize((im.width * S, im.height * S), Image.NEAREST)


def label(d, x, y, tx, ty, text):
    d.line([(x, y), (tx, ty)], fill=LINE, width=1)
    d.text((tx + 3, ty - 6), text, fill=INK)


def main():
    out = K.ROOT / "design/art/architecture_reference.png"
    W, H = 1900, 1150
    sheet = Image.new("RGB", (W, H), (28, 28, 36))
    d = ImageDraw.Draw(sheet)
    d.text((12, 8), "Ichor architecture reference (STYLE.md 4.8). 3x; 1 metatile = 48 px here. "
           "Light from the upper left; shadows fall down and right.", fill=INK)
    # 1. the Parthenon, its parts labelled
    p = img(AA.parthenon())
    ox, oy = 12, 40
    sheet.paste(p, (ox, oy))
    for (py, text) in ((18, "pediment: rises 1 px in 4, blue tympanum, figures, gold akroteria"),
                       (40, "frieze: triglyphs (blue) over every column and gap, metopes"),
                       (51, "architrave: gold shields; a 1 px shadow under every member"),
                       (60, "Doric capital (poly): abacus 3, echinus 3, annulets 2"),
                       (80, "shaft 10 px, flutes as stripes; pitch 28 px (octastyle)"),
                       (112, "krepis: 3 steps (tread, riser, shadow); top step = stylobate")):
        label(d, ox + p.width - 20, oy + py * S, ox + p.width + 20, oy + py * S, text)
    d.text((ox, oy + p.height + 4), "The Parthenon, 14 x 8: a landmark is >= 2.5x a house's footprint",
           fill=INK)
    # 2. the orders, side by side, 4 tall
    ox2, oy2 = 12, oy + p.height + 40
    x = ox2
    for o in CK.ORDERS:
        c = img(CK.free_column(o, "marble", 4, "path"))
        sheet.paste(c, (x, oy2))
        d.text((x, oy2 + c.height + 4), o, fill=INK)
        x += c.width + 30
    label(d, x - 30, oy2 + 10 * S, x, oy2 + 10 * S, "capital on the top layer (walk behind)")
    label(d, x - 30, oy2 + 58 * S, x, oy2 + 58 * S, "base solid; cast shadow down-right")
    d.text((x, oy2 + 80), "Doric: no base, 10 px shaft", fill=INK)
    d.text((x, oy2 + 96), "Ionic: volutes, Attic base, 8 px", fill=INK)
    d.text((x, oy2 + 112), "Corinthian: acanthus bell; one per city", fill=INK)
    # 3. a house beside the stoa's bay: roof to wall
    ox3 = 12
    oy3 = oy2 + 64 * S + 40
    hk = CA.house_kit()
    house = K.pick(hk, ["RT_L", "RT_M", "RT_R", "RB_L", "RB_M", "RB_R", "W_L", "door", "W_R"], w=3, key="h")
    hi = img(house)
    sheet.paste(hi, (ox3, oy3))
    d.text((ox3, oy3 + hi.height + 4), "house: roof 2 rows over wall 1; one door, high windows", fill=INK)
    st = CA.stoa()
    bay = K.pick(st, ["RT_L", "RT_M", "RT_M", "RT_R", "RB_L", "RB_M", "RB_M", "RB_R", "C_L", "C_M", "C_door",
                      "C_R", "B_L", "B_M", "B_door", "B_R", "S_L", "S_M", "S_M2", "S_R"], w=4, key="bay")
    bi = img(bay)
    sheet.paste(bi, (ox3 + hi.width + 40, oy3))
    d.text((ox3 + hi.width + 40, oy3 + bi.height + 4), "stoa: roof 2, colonnade 2 (pitch 16), step 1",
           fill=INK)
    # 4. the statue, its plinth and shadow
    ox4 = 1250
    pr = img(ST.promachos())
    sheet.paste(pr, (ox4, oy))
    for (py, text) in ((24, "a head that reads at 1x"), (58, "attribute: owl shield, spear"),
                       (90, "folds: 5 value steps"), (122, "plinth in 3/4: lit top, front, dark side"),
                       (141, "cast shadow down-right")):
        label(d, ox4 + pr.width - 10, oy + py * S, ox4 + pr.width + 20, oy + py * S, text)
    for i, (name, fig) in enumerate((("Kodros", ST.KODROS), ("Kairos", ST.KAIROS))):
        hs = img(ST.hero_statue(name.lower(), fig, name))
        sheet.paste(hs, (ox4 + i * (hs.width + 20), oy + pr.height + 30))
        d.text((ox4 + i * (hs.width + 20), oy + pr.height + 34 + hs.height), f"{name}, 2 x 3", fill=INK)
    # 5. the rock: lip, face, foot
    cl = img(K.pick(AA.cliff("path"), ["lip_W", "lip", "lip_b", "lip_E", "face_W", "face", "face_b", "face_E",
                                      "foot_W", "foot", "foot_b", "foot_E"], w=4, key="c"))
    ox5, oy5 = ox3 + hi.width + bi.width + 100, oy3
    sheet.paste(cl, (ox5, oy5))
    d.text((ox5, oy5 + cl.height + 4), "rock: lit lip, faceted face, foot + shadow", fill=INK)
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
