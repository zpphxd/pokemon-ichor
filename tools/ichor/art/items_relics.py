"""The relics' item icons (design/SYSTEMS.md §1), registered into items.py.

items.py calls register() with its own icon decorator and palette helpers, so
these icons are written, previewed and checked exactly like the others. Each is
a 24x24 icon in the master palette with an ink outline and light from the top
left. Ariadne's Thread reuses the Escape Rope's coil (escape_rope.png) in red;
its palette is defined beside the coil in items.py.

    /usr/bin/python3 tools/ichor/art/items.py --write --preview design/phase1/img
    /usr/bin/python3 tools/ichor/art/items_relics.py DIR   # relics alone, at 4x and 1x
"""
from __future__ import annotations

import numpy as np

RELIC_PICS = [
    "ichor_talaria", "bronze_hammer", "hecates_torch", "demeters_sickle", "girdle_of_herakles",
    "poseidons_conch", "daedalus_wings", "horn_of_achelous", "labrys", "helm_of_darkness",
    "nereid_pearl", "aeolus_bag", "aletheas_trowel", "aphrodite_bone",
]


def register(icon, pal, ramp_roles, C, Icon):
    WOOD = [C["wd_d"], C["wd_m"], C["wd_l"]]
    BRONZE = [C["br_d"], C["br_m"], C["sg_d"], C["sg_l"]]

    # ----------------------------------------------------------------------
    # The Bronze Hammer: Kedalion's votive smithing hammer, the haft on the
    # diagonal and the bronze head across its top.
    @icon("bronze_hammer", {
        "bronze_hammer": pal(ramp_roles("w", WOOD), **ramp_roles("b", BRONZE), c=C["tc_m"]),
    }, labels={"bronze_hammer": "Bronze Hammer"})
    def _hammer():
        ic = Icon("K w1 w2 w3 b1 b2 b3 b4 c")
        haft = ic.tube((4, 21), (15, 8), 1.6, ["w1", "w2", "w3"], caps=True)
        head = ic.poly([(9, 5), (15, 0.5), (22.5, 8), (17, 13)])
        ic.shade(head, ["b1", "b2", "b3", "b4"])
        ic.outline(haft | head)
        # the striking face, bright, and the peen, dark
        ic.line(17, 2, 21, 6, "b4")
        ic.pxs([(10, 6), (11, 7)], "b1")
        # a cord binding the haft below the head, and a ring at the butt
        for i in range(3):
            ic.px(12 + i, 12 - i, "c")
        ic.pxs([(4, 21), (5, 20)], "b2")
        return ic

    # ----------------------------------------------------------------------
    # Hecate's Torch: a pine torch bound with bronze, the flame streaming to
    # the top right.
    @icon("hecates_torch", {
        "hecates_torch": pal(ramp_roles("w", WOOD), **ramp_roles("b", BRONZE[:3]),
                             e1=(176, 40, 16), e2=(232, 112, 32), e3=(248, 200, 72), e4=(248, 240, 192)),
    }, labels={"hecates_torch": "Hecate's Torch"})
    def _torch():
        ic = Icon("K w1 w2 w3 b1 b2 b3 e1 e2 e3 e4")
        stick = ic.tube((5, 22), (13, 11), 1.8, ["w1", "w2", "w3"], caps=True)
        cup = ic.tube((11.5, 13), (15.5, 7.5), 3.0, ["b1", "b2", "b3"], caps=True)
        ic.outline(stick | cup)
        ic.line(11, 14, 16, 9, "b1")
        flame = ic.poly([(12, 6), (14, 1), (17, 4), (20, 0), (21, 5), (23, 4), (21, 10), (16, 11)])
        ic.fill(flame, "e2")
        inner = ic.poly([(14, 7), (16, 4), (18, 6), (20, 3), (20, 8), (16, 9)])
        ic.fill(inner, "e3")
        ic.pxs([(17, 7), (18, 7), (17, 6)], "e4")
        ic.outline(flame, "e1")
        return ic

    # ----------------------------------------------------------------------
    # Demeter's Sickle: a bronze harvest blade on an olive-wood grip, with a
    # single ear of grain tied to it.
    @icon("demeters_sickle", {
        "demeters_sickle": pal(ramp_roles("w", WOOD), **ramp_roles("b", BRONZE),
                               g1=C["sg_d"], g2=C["sg_p"], t=C["tc_m"]),
    }, labels={"demeters_sickle": "Demeter's Sickle"})
    def _sickle():
        ic = Icon("K w1 w2 w3 b1 b2 b3 b4 g1 g2 t")
        y, x = np.mgrid[0:24, 0:24]
        outer = ic.ellipse(12, 12.5, 10.5, 10)
        inner = ic.ellipse(14.5, 15, 9, 9)
        blade = outer & ~inner & ((x + y) < 30)
        ic.shade(blade, ["b1", "b2", "b3", "b4"])
        grip = ic.tube((19, 14), (21.5, 22), 2.0, ["w1", "w2", "w3"], caps=True)
        ic.outline(blade | grip)
        # the edge, honed bright on the inside of the curve
        inner2 = ic.ellipse(14.5, 15, 10.2, 10.2)
        edge = blade & inner2
        ic.recolor(edge, {"b1": "b4", "b2": "b3", "b3": "b4"})
        ic.pxs([(18, 14), (19, 13), (20, 13)], "t")
        # the ear of grain tied to the grip
        for k, (gx, gy) in enumerate([(16, 15), (15, 16), (16, 17), (15, 18), (16, 19)]):
            ic.px(gx, gy, "g2" if k % 2 == 0 else "g1")
        ic.line(17, 20, 19, 21, "g1")
        return ic

    # ----------------------------------------------------------------------
    # The Girdle of Herakles: a broad lion-hide belt, looped, closed by a
    # gold lion-head buckle.
    @icon("girdle_of_herakles", {
        "girdle_of_herakles": pal(ramp_roles("l", [(104, 56, 32), (152, 96, 48), (200, 144, 88)]),
                                  **ramp_roles("g", [C["sg_d"], C["sg_l"], C["sg_p"]]), m=(96, 64, 32)),
    }, labels={"girdle_of_herakles": "Girdle of Herakles"})
    def _girdle():
        ic = Icon("K l1 l2 l3 g1 g2 g3 m")
        outer = ic.ellipse(12, 12.5, 11, 8.5)
        inner = ic.ellipse(12, 12.5, 7.2, 4.6)
        band = outer & ~inner
        ic.shade(band, ["l1", "l2", "l3"])
        ic.outline(band)
        # stitching along the band
        y, x = np.mgrid[0:24, 0:24]
        mid = (((x + 0.5 - 12) / 9.1) ** 2 + ((y + 0.5 - 12.5) / 6.6) ** 2)
        stitch = band & (np.abs(mid - 1) < 0.07) & ((x + y) % 3 == 0)
        ic.fill(stitch, "m")
        # the buckle, a lion's face in gold at the front
        buckle = ic.ellipse(12, 19.5, 4.2, 3.6)
        ic.shade(buckle, ["g1", "g2", "g3"])
        ic.outline(buckle)
        ic.patch(10, 18, ["K.K", ".g.", "KKK"], {"g": "g1"})
        ic.pxs([(9, 17), (15, 17)], "g1")
        return ic

    # ----------------------------------------------------------------------
    # Poseidon's Conch: a spiral triton shell, cream with a rose mouth.
    @icon("poseidons_conch", {
        "poseidons_conch": pal(ramp_roles("s", [(184, 152, 120), (224, 200, 160), (248, 232, 200)]),
                               **ramp_roles("p", [(200, 104, 104), (240, 160, 152)]),
                               a1=C["ae_m"], a2=C["ae_l"]),
    }, labels={"poseidons_conch": "Poseidon's Conch"})
    def _conch():
        ic = Icon("K s1 s2 s3 p1 p2 a1 a2")
        body = ic.ellipse(10.5, 14, 8.5, 7.5)
        spire = ic.poly([(11, 8), (16, 4), (22, 1), (21, 6), (18, 12)])
        ic.shade(body | spire, ["s1", "s2", "s3"])
        ic.outline(body | spire)
        # the whorls, banded in Aegean blue
        ic.line(13, 9, 19, 4, "a1")
        ic.line(15, 11, 20, 7, "a1")
        ic.line(5, 10, 12, 8, "a1")
        ic.line(4, 13, 13, 11, "a2")
        # the flared mouth, rose inside
        mouth = ic.ellipse(8, 16.5, 4.8, 3.6)
        ic.fill(mouth & body, "p1")
        ic.outline(mouth & body)
        ic.pxs([(6, 16), (7, 15), (8, 15), (6, 17)], "p2")
        # knobs on the shoulder
        for (kx, ky) in [(9, 7), (13, 7), (17, 9)]:
            ic.patch(kx, ky - 1, ["K", "s"], {"s": "s3"})
        return ic

    # ----------------------------------------------------------------------
    # Daedalus's Wings: one wing of feathers set in wax, the wax band gold.
    @icon("daedalus_wings", {
        "daedalus_wings": pal(ramp_roles("f", [C["mb_d"], C["mb_m"], C["mb_l"]]),
                              **ramp_roles("x", [(200, 160, 72), (240, 208, 120)]), c=C["br_m"]),
    }, labels={"daedalus_wings": "Daedalus's Wings"})
    def _wings():
        ic = Icon("K f1 f2 f3 x1 x2 c")
        arm = ic.tube((22, 3), (3, 7), 1.6, caps=True)
        lengths = [15, 14, 13, 11, 9, 7, 5]
        xs = [4, 7, 10, 13, 16, 19, 21]
        feathers = []
        for bx, ln in zip(xs, lengths):
            by = 7 - (bx - 3) * 4 / 19 + 0.5
            f = ic.tube((bx, by), (bx - 2.5, by + ln), 1.9, caps=True)
            feathers.append(f)
        allf = np.zeros((24, 24), bool)
        for f in reversed(feathers):
            ic.shade(f, ["f1", "f2", "f3"], kind="cyl")
            ic.outline(f)
            allf |= f
        ic.fill(arm, "x1")
        ic.line(21, 3, 4, 6, "x2")
        ic.outline(arm | allf)
        ic.outline(arm)
        ic.pxs([(22, 3), (21, 2)], "c")
        return ic

    # ----------------------------------------------------------------------
    # The Horn of Achelous: the river-bull's horn, ivory, its mouth filled
    # with fruit and flowers (the cornucopia).
    @icon("horn_of_achelous", {
        "horn_of_achelous": pal(ramp_roles("h", [(152, 128, 96), (208, 184, 144), (240, 224, 192)]),
                                d=(88, 64, 40), r1=C["tc_m"], r2=C["tc_l"], g1=C["ol_m"], g2=C["ol_l"], y=C["sg_l"]),
    }, labels={"horn_of_achelous": "Horn of Achelous"})
    def _horn():
        ic = Icon("K h1 h2 h3 d r1 r2 g1 g2 y")
        y, x = np.mgrid[0:24, 0:24]
        # a curve from the tip (bottom left) to the mouth (top right), widening
        horn = np.zeros((24, 24), bool)
        for t in np.linspace(0, 1, 60):
            cx = 3 + 14 * t + 2 * np.sin(t * 3.1)
            cy = 21 - 13 * t - 3 * np.sin(t * 3.1)
            horn |= ((x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2) <= (0.8 + 4.2 * t) ** 2
        ic.shade(horn, ["h1", "h2", "h3"])
        ic.outline(horn)
        # rings around the horn
        for t in (0.35, 0.55, 0.75):
            cx = 3 + 14 * t + 2 * np.sin(t * 3.1)
            cy = 21 - 13 * t - 3 * np.sin(t * 3.1)
            ic.line(int(cx - 2), int(cy - 2), int(cx + 2), int(cy + 2), "d")
        # the fruit at the mouth
        for (fx, fy, rr, ramp) in [(18, 5, 2.6, ["r1", "r2"]), (21.5, 8, 2.2, ["g1", "g2"]), (15, 3, 1.8, ["g1", "g2"])]:
            m = ic.ellipse(fx, fy, rr, rr)
            ic.shade(m, ramp)
            ic.outline(m)
        ic.pxs([(20, 2), (21, 3), (22, 2)], "y")
        return ic

    # ----------------------------------------------------------------------
    # The Labrys: the double axe of Knossa, two crescent blades on a haft.
    @icon("labrys", {
        "labrys": pal(ramp_roles("b", BRONZE), **ramp_roles("w", WOOD), r=C["tc_m"]),
    }, labels={"labrys": "Labrys"})
    def _labrys():
        ic = Icon("K b1 b2 b3 b4 w1 w2 w3 r")
        haft = ic.rect(11, 2, 12, 22)
        ic.shade(haft, ["w1", "w2", "w3"], kind="cyl")
        left = ic.poly([(11, 6), (2, 2), (4, 8), (3, 13), (2, 18), (11, 13)])
        right = ic.poly([(12, 6), (21, 2), (19, 8), (20, 13), (21, 18), (12, 13)])
        ic.shade(left | right, ["b1", "b2", "b3", "b4"])
        ic.outline(haft | left | right)
        # the honed edges and the binding at the eye
        ic.line(3, 3, 3, 17, "b4")
        ic.line(20, 3, 20, 17, "b2")
        ic.pxs([(11, 8), (12, 8), (11, 11), (12, 11)], "r")
        return ic

    # ----------------------------------------------------------------------
    # The Helm of Darkness: a Corinthian helm in black bronze, a dark crest,
    # the eye slits empty.
    @icon("helm_of_darkness", {
        "helm_of_darkness": pal(ramp_roles("m", [(32, 32, 48), (64, 56, 80), (104, 96, 128), (152, 144, 176)]),
                                c1=(56, 24, 40), c2=(104, 40, 64), v=(16, 16, 24)),
    }, labels={"helm_of_darkness": "Helm of Darkness"})
    def _helm():
        ic = Icon("K m1 m2 m3 m4 c1 c2 v")
        dome = ic.ellipse(12, 11, 7.5, 7.5)
        cheeks = ic.poly([(4.5, 11), (19.5, 11), (18, 21), (14, 22), (13, 15), (11, 15), (10, 22), (6, 21)])
        helm = dome | cheeks
        ic.shade(helm, ["m1", "m2", "m3", "m4"])
        crest = ic.poly([(4, 4), (9, 1), (16, 1), (21, 4), (19, 6), (12, 3.5), (6, 6)])
        ic.shade(crest, ["c1", "c2"])
        ic.outline(helm | crest)
        # the eye slits and the gap down the face
        ic.patch(7, 11, ["vvv....vvv", ".vvv..vvv."], {"v": "v"})
        ic.line(12, 13, 12, 21, "v")
        ic.line(11, 15, 11, 21, "v")
        return ic

    # ----------------------------------------------------------------------
    # The Nereid Pearl: a great pearl in an opened scallop.
    @icon("nereid_pearl", {
        "nereid_pearl": pal(ramp_roles("s", [(192, 136, 120), (232, 184, 160), (248, 224, 208)]),
                            **ramp_roles("p", [(160, 168, 192), (208, 216, 232), (248, 248, 248)]), a=C["ae_l"]),
    }, labels={"nereid_pearl": "Nereid Pearl"})
    def _pearl():
        ic = Icon("K s1 s2 s3 p1 p2 p3 a")
        shell = ic.poly([(1, 14), (4, 7), (12, 4), (20, 7), (23, 14), (16, 22), (8, 22)])
        ic.shade(shell, ["s1", "s2", "s3"])
        ic.outline(shell)
        for x0 in (4, 8, 12, 16, 20):
            ic.line(12, 21, x0, 7 if 6 < x0 < 18 else 10, "s1")
        pearl = ic.ellipse(12, 13, 4.6, 4.6)
        ic.shade(pearl, ["p1", "p2", "p3"])
        ic.outline(pearl)
        ic.pxs([(10, 11), (11, 11), (10, 12)], "p3")
        ic.pxs([(15, 16), (14, 17)], "a")
        return ic

    # ----------------------------------------------------------------------
    # Aeolus's Bag: an ox-hide bag tied with a silver cord, the winds curling
    # out of its neck.
    @icon("aeolus_bag", {
        "aeolus_bag": pal(ramp_roles("l", [(112, 72, 40), (160, 112, 64), (208, 160, 104)]),
                          c=C["mb_l"], **ramp_roles("w", [C["ae_l"], C["ae_p"]]), d=(80, 48, 32)),
    }, labels={"aeolus_bag": "Aeolus's Bag"})
    def _bag():
        ic = Icon("K l1 l2 l3 c w1 w2 d")
        body = ic.ellipse(11, 16, 8.5, 7)
        neck = ic.poly([(8, 10), (14, 10), (13, 6), (9, 6)])
        ic.shade(body | neck, ["l1", "l2", "l3"])
        ic.outline(body | neck)
        ic.line(7, 9, 15, 9, "c")
        ic.line(8, 10, 14, 10, "K")
        ic.pxs([(16, 9), (17, 10)], "c")
        # hide seams, and the winds
        ic.line(6, 15, 9, 21, "d")
        ic.line(15, 13, 16, 20, "d")
        ic.patch(12, 0, [
            ".wwW.....",
            "w...W.ww.",
            "....WW..W",
            "..WW...W.",
        ], {"w": "w1", "W": "w2"})
        return ic


    # ----------------------------------------------------------------------
    # Alethea's Trowel (§5, a tool beside the relics): a pointed bronze blade,
    # worn bright at the tip, on a short olive-wood handle, held on the diagonal.
    @icon("aletheas_trowel", {
        "aletheas_trowel": pal(ramp_roles("b", BRONZE), **ramp_roles("w", WOOD), e=C["tc_l"]),
    }, labels={"aletheas_trowel": "Alethea's Trowel"})
    def _trowel():
        ic = Icon("K b1 b2 b3 b4 w1 w2 w3 e")
        handle = ic.tube((15, 9), (21, 3), 1.8, ["w1", "w2", "w3"], caps=True)
        tang = ic.tube((12, 12), (15.5, 8.5), 0.7)
        blade = ic.poly([(13, 10.5), (9, 7), (2.5, 21.5), (16.5, 15)])
        ic.shade(tang, ["b1", "b2"])
        ic.shade(blade, ["b1", "b2", "b3", "b4"])
        ic.outline(handle | tang | blade)
        # the spine down the blade, the worn tip and a smear of earth
        ic.line(12, 11, 5, 19, "b4")
        ic.pxs([(3, 21), (4, 20)], "b4")
        ic.pxs([(13, 15), (14, 14), (12, 16)], "e")
        return ic

    # ----------------------------------------------------------------------
    # The Aphrodite Bone (§9): Mom's lucky knucklebone, an astragalus worn
    # smooth and ivory, its four sides marked, with a rose-gold thread.
    @icon("aphrodite_bone", {
        "aphrodite_bone": pal(ramp_roles("i", [C["lp_d"], C["lp_m"], C["lp_l"], C["ln_l"]]),
                              d=C["br_d"], r=(216, 120, 136)),
    }, labels={"aphrodite_bone": "Aphrodite Bone"})
    def _bone():
        ic = Icon("K i1 i2 i3 i4 d r")
        # the knuckle: a waisted block, wider at the ends
        body = ic.poly([(4, 8), (8, 5), (12, 7), (16, 5), (20, 8), (19, 13),
                        (20, 18), (16, 20), (12, 18), (8, 20), (4, 18), (5, 13)])
        ic.shade(body, ["i1", "i2", "i3", "i4"])
        ic.outline(body)
        # the hollow on its face and the pips of the side up
        ic.line(9, 12, 15, 12, "i1")
        ic.pxs([(8, 9), (16, 9), (8, 16), (16, 16)], "d")
        # a thread tied round its waist
        ic.line(12, 7, 12, 18, "r")
        ic.pxs([(13, 19), (14, 20), (14, 21)], "r")
        return ic

def preview(outdir):
    """The relics alone, at 4x on the bag's parchment and at 1x on clay."""
    import os
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    import items  # noqa: E402  (registers everything, these included)
    from items_lib import palette_colors, to_rgb, upscale
    from PIL import Image
    pics = RELIC_PICS + ["escape_rope"]
    stems = {p: items.PIC_PALS[p][0] for p in RELIC_PICS}
    stems["escape_rope"] = "ariadnes_thread"
    k = 4
    sheet = Image.new("RGB", (len(pics) * (24 * k + 8) + 8, 24 * k + 48), (184, 88, 48))
    for i, p in enumerate(pics):
        ic = items.PICS[p]
        cols = palette_colors(ic.roles, items.PALETTES[stems[p]][1])
        big = Image.fromarray(upscale(to_rgb(ic.a, cols, (232, 216, 176)), k)).convert("RGB")
        sheet.paste(big, (8 + i * (24 * k + 8), 8))
        small = Image.fromarray(to_rgb(ic.a, cols, (184, 88, 48))).convert("RGB")
        sheet.paste(small, (8 + i * (24 * k + 8), 24 * k + 16))
    path = os.path.join(outdir, "items_relics.png")
    sheet.save(path)
    print(f"items_relics.py: wrote {path}")


if __name__ == "__main__":
    import sys
    preview(sys.argv[1] if len(sys.argv) > 1 else ".")
