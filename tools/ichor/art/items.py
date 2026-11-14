"""Ichor's item icons (24x24, graphics/items/icons) and their palettes.

Usage:
    /usr/bin/python3 tools/ichor/art/items.py [--write] [--preview DIR]

--write    rewrites the icon PNGs and palettes this file owns, keeping every
           item that shares a pic or a palette consistent
--preview  writes DIR/items_icons.png (before and after at 4x and 1x, on the
           bag's parchment plate and on clay) and DIR/items_icons_tm.png (the
           sealed scroll and the tablet in all 19 type colors)

The look (design/phase1/PLAN.md's master palette; the Aethos style):
  * medicines are clay flasks, alabastra and herb bundles tied with wool;
    the flask's ware gives the strength, the wool's color the status cured
  * Escape Rope is a coil of linen cord, Repel an incense cone
  * TMs are sealed scrolls, the seal and cord in the move's type color
  * berries are Aegean fruit: the Oran Berry a fig, the Sitrus Berry a golden
    quince, the "golden apple" of the Hesperides
  * Poke Balls keep their name and look (director's ruling), so the ball
    icons are not touched

Some pics are shared by several items, each with its own palette (the Potion
pic serves Potion, Super Potion and Hyper Potion), and some palettes color
two pics (star.pal: Stardust and Star Piece). Each is drawn over one fixed
role order and every sharing palette is rewritten, so no item that shares a
file is left with scrambled colors. The sharing is read from
src/data/items.h at run time and checked before anything is written.

The four flag-only key items of the slice (Talaria, Augur's Eye, Pokedex,
Hearth Laurel) are not items in the engine. Their icons are drawn as
ichor_*.png assets, ready for when they become items; nothing builds them yet.
"""
from __future__ import annotations

import argparse
import io
import math
import os
import re
import subprocess
import sys
from collections import defaultdict

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from items_lib import (C, Icon, ROOT, mix, palette_colors, ramp4,  # noqa: E402
                       save_indexed, to_rgb, upscale, write_jasc)

ICONS = os.path.join(ROOT, "graphics/items/icons")
PALS = os.path.join(ROOT, "graphics/items/icon_palettes")
BASE_REV = "963009665e"     # main when this file was written: the "before" art

PICS = {}        # pic stem -> Icon
PIC_PALS = {}    # pic stem -> [palette stems that color it]
PALETTES = {}    # palette stem -> (roles, {role: color})
LABELS = {}      # palette stem -> what the sheet calls it
ORDER = []       # (pic, palette) in sheet order
ASSETS = set()   # pics not referenced by the game yet


def icon(pic, palettes=None, uses=(), labels=None, asset=False):
    """Register an icon. palettes: {stem: colors} defined here; uses:
    palette stems defined by another pic that also color this one."""
    def deco(fn):
        ic = fn()
        PICS[pic] = ic
        PIC_PALS[pic] = []
        for stem, cols in (palettes or {}).items():
            missing = [r for r in ic.roles if r not in cols]
            assert not missing, (pic, stem, missing)
            PALETTES[stem] = (tuple(ic.roles), cols)
            PIC_PALS[pic].append(stem)
            ORDER.append((pic, stem))
        for stem in uses:
            PIC_PALS[pic].append(stem)
            ORDER.append((pic, stem))
        for k, v in (labels or {}).items():
            LABELS[k] = v
        if asset:
            ASSETS.add(pic)
        return fn
    return deco


INK = C["ink"]


def pal(roles_colors, **kw):
    d = dict(K=INK)
    d.update(roles_colors)
    d.update(kw)
    return d


def ramp_roles(prefix, colors):
    return {f"{prefix}{i + 1}": c for i, c in enumerate(colors)}


# ==========================================================================
# Clay flasks: Potion, Super Potion, Hyper Potion (potion.png)
# An aryballos: a round oil flask with a disc lip, a strap handle and a wax
# plug. Plain red clay, then black glaze with red figures, then Aegean
# faience: the tier reads by the ware, as Emerald's colors did.
# ==========================================================================
@icon("potion", {
    "potion": pal(ramp_roles("c", [C["tc_d"], C["tc_m"], C["tc_l"], C["tc_p"]]),
                  b=INK, f=C["tc_p"], s1=C["ol_m"], s2=C["ol_l"]),
    "super_potion": pal(ramp_roles("c", [(40, 32, 40), (72, 64, 72), (112, 104, 112), (176, 168, 168)]),
                        b=C["tc_m"], f=C["tc_p"], s1=C["sg_d"], s2=C["sg_l"]),
    "hyper_potion": pal(ramp_roles("c", [C["ae_d"], C["ae_m"], C["ae_l"], C["ae_p"]]),
                        b=C["sg_d"], f=C["sg_p"], s1=C["tc_m"], s2=C["tc_l"]),
}, labels={"potion": "Potion", "super_potion": "Super Potion", "hyper_potion": "Hyper Potion"})
def _potion():
    ic = Icon("K c1 c2 c3 c4 b f s1 s2")
    body = ic.ellipse(12, 15.5, 7.6, 7.2)
    ic.shade(body, ["c1", "c2", "c3", "c4"])
    ic.outline(body)
    # plug, disc lip, neck and strap handle, by hand
    ic.patch(5, 0, [
        "....KKKK........",
        "...KSSssK.......",
        "...KSsssK.......",
        ".KKKKKKKKKKKK...",
        ".K44333332211K..",
        ".KKK1222211KKKK.",
        "....K3221K..K2K.",
        "....K3221K..K1K.",
        "....K3221K.K1K..",
    ], {"K": "K", "S": "s2", "s": "s1", "4": "c4", "3": "c3", "2": "c2", "1": "c1"})
    # black-figure band: two rules and a row of dots
    for x in range(5, 20):
        for y, role in ((13, "b"), (14, "b"), (16, "b"), (17, "b")):
            if body[y, x] and ic.a[y, x] != ic.idx["K"]:
                ic.px(x, y, role)
        if body[15, x] and ic.a[15, x] != ic.idx["K"]:
            ic.px(x, 15, "f" if x % 2 == 0 else "b")
    ic.pxs([(8, 10), (9, 10), (7, 11)], "c4")     # glint on the shoulder
    return ic


# ==========================================================================
# Alabastron: Max Potion, Full Restore (large_potion.png). A tall alabaster
# flask with a disc lip and a wool fillet tied at the neck. Full Restore's
# gold bands and red fillet mark that it cures status as well.
# ==========================================================================
@icon("large_potion", {
    "max_potion": pal(ramp_roles("a", [(160, 152, 136), (208, 200, 184), (240, 232, 216), (248, 248, 240)]),
                      b1=C["ae_d"], b2=C["ae_m"], r1=C["ae_m"], r2=C["ae_l"], s1=C["tc_d"], s2=C["tc_m"]),
    "full_restore": pal(ramp_roles("a", [(160, 152, 136), (208, 200, 184), (240, 232, 216), (248, 248, 240)]),
                        b1=C["sg_d"], b2=C["sg_l"], r1=(160, 32, 32), r2=(216, 72, 56),
                        s1=C["sg_d"], s2=C["sg_l"]),
}, labels={"max_potion": "Max Potion", "full_restore": "Full Restore"})
def _large_potion():
    ic = Icon("K a1 a2 a3 a4 b1 b2 r1 r2 s1 s2")
    upper = ic.ellipse(12, 11.5, 4.6, 5.5)
    lower = ic.ellipse(12, 16.5, 6.3, 6.3)
    body = upper | lower | ic.poly([(7.5, 13), (16.5, 13), (17.5, 17), (6.5, 17)])
    neck = ic.rect(10, 4, 13, 7)
    lip = ic.rect(8, 3, 15, 3)
    plug = ic.rect(10, 0, 13, 2)
    ic.shade(body, ["a1", "a2", "a3", "a4"])
    ic.shade(neck, ["a1", "a2", "a3"], kind="cyl")
    ic.shade(lip, ["a2", "a3"], kind="flat")
    ic.shade(plug, ["s1", "s2"], kind="cyl")
    sil = body | neck | lip | plug
    ic.outline(sil)
    # alabaster veining
    ic.pxs([(9, 15), (10, 16), (10, 17), (14, 10), (15, 11), (13, 19), (14, 20)], "a2")
    # two painted bands
    for y, r in ((10, "b1"), (11, "b2"), (17, "b2"), (18, "b1")):
        for x in range(5, 20):
            if body[y, x] and ic.a[y, x] != ic.idx["K"]:
                ic.px(x, y, r)
    # the fillet at the neck, its ends hanging to the left
    ic.patch(9, 5, ["KrRRRK", ".KRRK."], {"r": "r2", "R": "r1"})
    ic.patch(6, 6, ["KK", "Kr", "KrK", ".Kr", ".KK"], {"r": "r2"})
    ic.pxs([(9, 8), (8, 9)], "a4")
    return ic


# ==========================================================================
# Herb bundles tied with wool: Antidote, Paralyze Heal, Burn Heal, Ice Heal,
# Awakening (status_heal.png). The wool is dyed the status's color, so the
# five read apart at a glance: purple poison, gold paralysis, red burn, ice
# white, sea-blue sleep.
# ==========================================================================
HERB_ROLES = "K l1 l2 l3 t1 t2 w1 w2 w3 fl1 fl2"
STEM = ((88, 72, 40), (144, 120, 64))
RUE = [(40, 80, 64), (80, 128, 96), (136, 176, 128)]
SAGE = [(72, 96, 72), (120, 144, 112), (176, 192, 160)]
MINT = [(32, 88, 48), (64, 136, 72), (128, 184, 104)]
THYME = [(56, 80, 40), (96, 128, 56), (152, 176, 88)]
WOOL = dict(
    purple=[(80, 32, 104), (144, 72, 168), (200, 144, 216)],
    gold=[(176, 112, 24), (232, 176, 48), (248, 224, 128)],
    red=[(136, 24, 24), (208, 56, 40), (248, 128, 96)],
    ice=[(88, 136, 184), (168, 208, 240), (240, 248, 248)],
    sea=[(24, 48, 128), (48, 104, 184), (120, 168, 232)],
)


def _herb(leaf, wool, flower):
    d = pal(ramp_roles("l", leaf), t1=STEM[0], t2=STEM[1], fl1=flower[0], fl2=flower[1])
    d.update(ramp_roles("w", wool))
    return d


WRAP_A, WRAP_B = (6.6, 17.4), (10.9, 13.1)    # the tie's axis, stems to leaves


def herb_bundle(ic, wrap):
    """A bundle lying on the diagonal: cut stems at the lower left, a fan of
    leaves at the upper right, tied in the middle. wrap(ic) paints the tie
    and returns its mask. Each leaf is outlined on its own, back to front,
    so the sprigs stay apart at 1x."""
    stems = ic.tube((2.6, 21.4), (8.5, 15.5), 2.5, ["t1", "t2", "t2"], caps=True)
    ic.outline(stems)
    ic.line(3, 20, 7, 16, "t1")
    ic.pxs([(2, 20), (3, 21), (2, 21)], "t2")      # the cut ends
    leaves = [((11, 12), (12, 1), 2.9), ((12, 12), (22, 3), 2.9), ((11, 12), (4, 4), 2.6),
              ((12, 13), (22, 13), 2.5)]
    for base, tip, w in leaves:
        m = ic.leaf(base, tip, w, ["l2", "l3"], rib="l1")
        ic.outline(m)
        # a dark vein tip and a lit edge near the base
        ic.px(int(round(base[0] + (tip[0] - base[0]) * 0.3)), int(round(base[1] + (tip[1] - base[1]) * 0.3)), "l1")
    wrap(ic)


def wool_wrap(ic):
    """Turns of dyed wool: cylinder-shaded, a dark line between turns, and a
    loose end with a tuft hanging to the right."""
    t, s, ln = ic.tube_coords(WRAP_A, WRAP_B)
    m = ic.tube(WRAP_A, WRAP_B, 3.1, ["w1", "w2", "w3"], caps=False)
    turns = m & (np.abs(((t * ln) % 2.0) - 1.0) < 0.35)
    ic.recolor(turns, {"w3": "w2", "w2": "w1"})
    tail = ic.tube((10.5, 16.5), (14.5, 20.5), 0.9, ["w1", "w2", "w3"], caps=True)
    tuft = ic.ellipse(15.2, 21.2, 1.8, 1.6)
    ic.shade(tuft, ["w1", "w2", "w3"])
    ic.outline(m)
    ic.outline(tail | tuft)
    return m | tail | tuft


@icon("status_heal", {
    "antidote": _herb(RUE, WOOL["purple"], (C["sg_d"], C["sg_l"])),
    "paralyze_heal": _herb(THYME, WOOL["gold"], ((200, 120, 24), (248, 208, 72))),
    "burn_heal": _herb(SAGE, WOOL["red"], ((200, 192, 184), (248, 248, 240))),
    "ice_heal": _herb(THYME, WOOL["ice"], ((160, 64, 112), (224, 136, 184))),
    "awakening": _herb(MINT, WOOL["sea"], ((128, 96, 184), (200, 168, 232))),
}, labels={"antidote": "Antidote", "paralyze_heal": "Paralyze Heal", "burn_heal": "Burn Heal",
           "ice_heal": "Ice Heal", "awakening": "Awakening"})
def _status_heal():
    ic = Icon(HERB_ROLES)
    herb_bundle(ic, wool_wrap)
    # flower heads on the sprig tips
    for x, y in ((12, 0), (21, 2), (3, 3)):
        ic.patch(x - 1, y, ["KFK", "FfF", ".F."], {"F": "fl1", "f": "fl2"})
    return ic


# ==========================================================================
# Full Heal (full_heal.png): the panacea bundle, named for Panakeia, daughter
# of Asclepius. The same herbs, tied with all five wools.
# ==========================================================================
@icon("full_heal", {
    "full_heal": pal(ramp_roles("l", RUE), t1=STEM[0], t2=STEM[1],
                     p1=WOOL["purple"][1], p2=WOOL["purple"][2], g1=WOOL["gold"][1], g2=WOOL["gold"][2],
                     r1=WOOL["red"][1], r2=WOOL["red"][2], b1=WOOL["sea"][1], b2=WOOL["sea"][2],
                     fl=C["mb_l"]),
}, labels={"full_heal": "Full Heal"})
def _full_heal():
    ic = Icon("K l1 l2 l3 t1 t2 p1 p2 g1 g2 r1 r2 b1 b2 fl")

    def wrap(ic):
        # one turn of each wool, lit side light, shaded side dark
        t, s, ln = ic.tube_coords(WRAP_A, WRAP_B)
        m = ic.tube(WRAP_A, WRAP_B, 3.1)
        bands = ["p", "g", "r", "b"]
        for yy, xx in zip(*np.nonzero(m)):
            k = min(int(t[yy, xx] * len(bands)), len(bands) - 1)
            ic.a[yy, xx] = ic.idx[bands[k] + ("2" if s[yy, xx] < 0.8 else "1")]
        tail = ic.tube((10.5, 16.5), (14.5, 20.5), 0.9, ["g1", "g2"], caps=True)
        tuft = ic.ellipse(15.2, 21.2, 1.8, 1.6)
        ic.shade(tuft, ["r1", "r2"])
        ic.outline(m)
        ic.outline(tail | tuft)
        return m
    herb_bundle(ic, wrap)
    for x, y in ((12, 0), (21, 2), (3, 3)):
        ic.patch(x - 1, y, ["KFK", "FFF", ".F."], {"F": "fl"})
    return ic


# ==========================================================================
# Revive and Max Revive (revive.png, max_revive.png; both revive.pal):
# amber, the tears of the Heliades, set in gold. A drop of sun to wake a
# fainted Pokemon; the larger stone in its gold frame for Max Revive.
# ==========================================================================
REVIVE_ROLES = "K a1 a2 a3 a4 g1 g2 g3 c s"


@icon("revive", {
    "revive": pal(ramp_roles("a", [(160, 72, 16), (216, 128, 24), (248, 184, 56), (248, 232, 152)]),
                  g1=C["br_m"], g2=C["sg_d"], g3=C["sg_l"], c=C["tc_d"], s=C["mb_l"]),
}, labels={"revive": "Revive"})
def _revive():
    ic = Icon(REVIVE_ROLES)
    drop = ic.ellipse(12, 15.5, 5.2, 5.6) | ic.poly([(7.2, 14), (12, 5.5), (16.8, 14)])
    ic.shade(drop, ["a1", "a2", "a3", "a4"])
    cap = ic.rect(10, 5, 13, 7)
    ic.shade(cap, ["g1", "g2", "g3"], kind="cyl")
    loop = ic.spans(2, [(11, 12), [(10, 10), (13, 13)], [(10, 10), (13, 13)]])
    ic.fill(loop, "g2")
    ic.outline(drop | cap | loop)
    ic.pxs([(11, 3), (12, 3), (11, 4), (12, 4)], "_")
    ic.outline(loop | cap)
    # cord to the right
    for x, y in ((14, 2), (15, 1), (16, 1), (17, 2), (18, 2), (19, 3)):
        ic.px(x, y, "c")
    # inner glow and a glint
    ic.pxs([(10, 12), (10, 13), (11, 11)], "a4")
    ic.pxs([(9, 13), (9, 14)], "s")
    ic.pxs([(14, 18), (13, 19), (15, 17)], "a1")
    return ic


@icon("max_revive", uses=["revive"], labels={("max_revive", "revive"): "Max Revive"})
def _max_revive():
    ic = Icon(REVIVE_ROLES)
    drop = ic.ellipse(12, 15, 7.4, 7.4) | ic.poly([(5, 13), (12, 2.5), (19, 13)])
    frame = drop.copy()
    ic.fill(frame, "g2")
    inner = ic.ellipse(12, 15, 5.6, 5.6) | ic.poly([(6.8, 13.5), (12, 5), (17.2, 13.5)])
    ic.shade(frame, ["g1", "g2", "g3"])
    ic.shade(inner, ["a1", "a2", "a3", "a4"])
    ic.outline(drop)
    ic.outline(inner)
    loop = ic.spans(0, [(11, 12), [(10, 10), (13, 13)]])
    ic.fill(loop, "g3")
    ic.pxs([(10, 1), (13, 1), (11, 0), (12, 0)], "K")
    ic.pxs([(11, 1), (12, 1)], "_")
    # rays: the sun inside
    ic.pxs([(10, 12), (10, 13), (11, 11), (11, 10)], "a4")
    ic.pxs([(9, 14), (9, 15)], "s")
    ic.pxs([(15, 18), (14, 19), (16, 17)], "a1")
    # gold studs on the frame
    ic.pxs([(5, 15), (19, 15), (12, 21)], "g3")
    return ic


# ==========================================================================
# Ether family (ether.png): Ether, Max Ether, Elixir, Max Elixir. A little
# two-handled amphoriskos of nectar, the gods' drink: it restores PP.
# ==========================================================================
@icon("ether", {
    "ether": pal(ramp_roles("e", [C["ae_d"], C["ae_m"], C["ae_l"], C["ae_p"]]), b1=INK, b2=C["mb_l"]),
    "max_ether": pal(ramp_roles("e", [(16, 32, 88), C["ae_d"], C["ae_m"], C["ae_l"]]), b1=C["sg_d"], b2=C["sg_l"]),
    "elixir": pal(ramp_roles("e", [(168, 96, 16), C["sg_d"], C["sg_l"], C["sg_p"]]), b1=INK, b2=C["tc_l"]),
    "max_elixir": pal(ramp_roles("e", [(168, 96, 16), C["sg_d"], C["sg_l"], C["sg_p"]]),
                      b1=(144, 24, 32), b2=(224, 80, 64)),
}, labels={"ether": "Ether", "max_ether": "Max Ether", "elixir": "Elixir", "max_elixir": "Max Elixir"})
def _ether():
    ic = Icon("K e1 e2 e3 e4 b1 b2")
    body = ic.ellipse(12, 13.5, 6.2, 6.3) | ic.poly([(7, 16), (17, 16), (12.5, 22.5), (11.5, 22.5)])
    neck = ic.rect(10, 4, 13, 8)
    lip = ic.rect(9, 2, 14, 3)
    foot = ic.rect(10, 21, 13, 22)
    hl = ic.spans(4, [(7, 9), [(6, 6), (9, 9)], [(6, 6)], [(6, 7)], [(7, 8)]])
    hr = ic.spans(4, [(14, 16), [(14, 14), (17, 17)], [(17, 17)], [(16, 17)], [(15, 16)]])
    ic.shade(body, ["e1", "e2", "e3", "e4"])
    ic.shade(neck, ["e1", "e2", "e3"], kind="cyl")
    ic.shade(lip, ["e2", "e3"], kind="flat")
    ic.shade(foot, ["e1", "e2"], kind="cyl")
    ic.fill(hl, "e2")
    ic.fill(hr, "e1")
    ic.outline(body | neck | lip | foot | hl | hr)
    for x in range(5, 20):
        for y, r in ((12, "b1"), (13, "b2"), (14, "b1")):
            if body[y, x] and ic.a[y, x] != ic.idx["K"]:
                ic.px(x, y, r if not (y == 13 and x % 2) else "b1")
    ic.pxs([(8, 9), (8, 10), (9, 9)], "e4")
    return ic


# ==========================================================================
# Repel family (repel.png): an incense cone smoldering on a clay saucer.
# Frankincense for Repel, myrrh for Super Repel, cypress resin for Max Repel.
# ==========================================================================
@icon("repel", {
    "repel": pal(ramp_roles("i", [(144, 96, 40), (200, 152, 72), (240, 208, 128)]),
                 e1=(208, 64, 32), e2=(248, 176, 64), d1=C["tc_d"], d2=C["tc_m"], d3=C["tc_l"],
                 s1=(144, 136, 136), s2=(200, 192, 192)),
    "super_repel": pal(ramp_roles("i", [(104, 32, 32), (160, 64, 48), (208, 112, 80)]),
                       e1=(208, 64, 32), e2=(248, 176, 64), d1=C["tc_d"], d2=C["tc_m"], d3=C["tc_l"],
                       s1=(144, 136, 136), s2=(200, 192, 192)),
    "max_repel": pal(ramp_roles("i", [(32, 64, 48), (64, 104, 72), (112, 152, 104)]),
                     e1=(208, 64, 32), e2=(248, 176, 64), d1=C["tc_d"], d2=C["tc_m"], d3=C["tc_l"],
                     s1=(144, 136, 136), s2=(200, 192, 192)),
}, labels={"repel": "Repel", "super_repel": "Super Repel", "max_repel": "Max Repel"})
def _repel():
    ic = Icon("K i1 i2 i3 e1 e2 d1 d2 d3 s1 s2")
    cone = ic.poly([(12, 7), (6.5, 18), (17.5, 18)])
    dish = ic.ellipse(12, 19, 9.5, 3.4)
    ic.shade(dish, ["d1", "d2", "d3"], kind="flat", light=(0, -1))
    ic.shade(cone, ["i1", "i2", "i3"], kind="cyl")
    ic.outline(dish)
    ic.outline(cone)
    # the saucer's rim and well
    ic.patch(5, 18, ["KddddddddddddK"], {"d": "d1"})
    ic.pxs([(4, 19), (19, 19)], "d3")
    # ember at the tip
    ic.patch(11, 6, ["KeK", "KEeK"], {"e": "e2", "E": "e1"})
    ic.pxs([(12, 6)], "e2")
    # smoke: two soft curls, no outline
    ic.pxs([(12, 5), (13, 4), (13, 3), (12, 2), (11, 1), (12, 0)], "s1")
    ic.pxs([(14, 4), (15, 3), (15, 2), (16, 1)], "s2")
    ic.pxs([(10, 3), (9, 2), (10, 1)], "s2")
    return ic


# ==========================================================================
# Escape Rope (escape_rope.png): a coil of linen cord with a knotted end,
# Ariadne's thread for finding the way out.
# ==========================================================================
@icon("escape_rope", {
    "escape_rope": pal(ramp_roles("r", [(112, 80, 40), (160, 120, 64), (200, 168, 104), (232, 208, 152)])),
}, labels={"escape_rope": "Escape Rope"})
def _escape_rope():
    ic = Icon("K r1 r2 r3 r4")
    sil = np.zeros((24, 24), bool)
    y, x = np.mgrid[0:24, 0:24]
    # two thick turns of twisted cord. Each pixel of a turn knows its angle
    # round the coil and its depth across the cord: the strands are slanted
    # stripes, lit where the cord's round face meets the light.
    for cx, cy, rx, ry, w, twists in ((12, 11.6, 10.3, 7.2, 3.5, 13), (12, 13.0, 6.8, 4.4, 3.3, 9)):
        ring = ic.ellipse(cx, cy, rx, ry) & ~ic.ellipse(cx, cy, rx - w, ry - w)
        u, v = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
        theta = np.arctan2(v, u)
        depth = (1 - np.sqrt(u * u + v * v)) * min(rx, ry) / w        # 0 outside .. 1 inside
        strand = ((theta / (2 * math.pi)) * twists + depth * 0.9) % 1.0
        lit = (-np.cos(theta) * 0.6 - np.sin(theta) * 0.8) * (0.5 - depth)  # outer top-left lit
        for yy, xx in zip(*np.nonzero(ring)):
            if strand[yy, xx] < 0.28:
                role = "r1"
            else:
                b = 0.55 - abs(depth[yy, xx] - 0.4) + lit[yy, xx] * 0.6
                role = "r4" if b > 0.55 else "r3" if b > 0.3 else "r2"
            ic.a[yy, xx] = ic.idx[role]
        ic.outline(ring)
        sil |= ring
    # the free end runs down to a knot
    end = ic.tube((15, 17), (19.5, 21.5), 1.2, ["r1", "r2", "r3"])
    knot = ic.ellipse(20, 21.5, 2.2, 1.8)
    ic.shade(knot, ["r1", "r2", "r3"])
    ic.outline(end | knot)
    ic.pxs([(22, 22), (23, 23), (21, 23)], "r2")
    return ic


# ==========================================================================
# Oran Berry (oran_berry.png): a ripe black fig with a fig leaf. Oran's blue
# is kept in the fig's skin.
# ==========================================================================
@icon("oran_berry", {
    "oran_berry": pal(ramp_roles("f", [(40, 32, 88), (72, 64, 144), (112, 104, 192), (176, 168, 224)]),
                      o=(200, 104, 128), st=C["ol_d"], **ramp_roles("lf", [C["ol_d"], C["ol_m"], C["ol_l"]])),
}, labels={"oran_berry": "Oran Berry"})
def _oran():
    ic = Icon("K f1 f2 f3 f4 o st lf1 lf2 lf3")
    leaf = ic.leaf((12, 7), (21, 1), 3.2, ["lf1", "lf2"], rib="lf1")
    leaf |= ic.leaf((13, 7), (21, 9), 2.4, ["lf1", "lf2"], rib="lf1")
    ic.outline(leaf)
    ic.pxs([(16, 3), (15, 4)], "lf3")
    body = ic.ellipse(11.5, 15.5, 7.2, 6.6) | ic.poly([(6, 13), (10, 6.5), (13, 6.5), (17, 13)])
    ic.shade(body, ["f1", "f2", "f3", "f4"])
    stem = ic.rect(10, 4, 12, 6)
    ic.fill(stem, "st")
    ic.outline(body | stem)
    ic.pxs([(11, 4), (11, 5)], "lf2")
    # the eye at the base, and faint ribs
    ic.pxs([(11, 21), (12, 21)], "o")
    ic.pxs([(14, 12), (15, 14), (15, 16), (9, 17), (8, 15)], "f2")
    ic.pxs([(8, 11), (8, 12), (9, 10)], "f4")
    return ic


# ==========================================================================
# Sitrus Berry (sitrus_berry.png): a golden quince with its leaf, the
# "golden apple" of the Hesperides.
# ==========================================================================
@icon("sitrus_berry", {
    "sitrus_berry": pal(ramp_roles("q", [(168, 104, 24), (216, 160, 40), (240, 208, 80), (248, 240, 168)]),
                        st=C["wd_d"], b=(120, 72, 24), **ramp_roles("lf", [C["ol_d"], C["ol_m"], C["ol_l"]])),
}, labels={"sitrus_berry": "Sitrus Berry"})
def _sitrus():
    ic = Icon("K q1 q2 q3 q4 st b lf1 lf2 lf3")
    leaf = ic.leaf((13, 6), (22, 2), 3.0, ["lf1", "lf2"], rib="lf1")
    ic.outline(leaf)
    ic.pxs([(17, 3), (16, 4)], "lf3")
    body = (ic.ellipse(12, 15, 8.0, 7.2) | ic.ellipse(10, 9.5, 4.5, 3.8) | ic.ellipse(14, 9.8, 4.2, 3.6))
    ic.shade(body, ["q1", "q2", "q3", "q4"])
    stem = ic.rect(11, 3, 12, 6)
    ic.fill(stem, "st")
    ic.outline(body | stem)
    # the dimple at the stalk, the lobes, the blossom end
    ic.pxs([(11, 7), (13, 7)], "q1")
    ic.pxs([(16, 12), (17, 14), (12, 11)], "q2")
    ic.patch(11, 20, ["bKb"], {"b": "b"})
    ic.pxs([(7, 11), (7, 12), (8, 10), (8, 9)], "q4")
    return ic


# ==========================================================================
# Honey (honey.png): Melitta's honey pot, a dipper standing in it.
# ==========================================================================
@icon("honey", {
    "honey": pal(ramp_roles("c", [C["tc_d"], C["tc_m"], C["tc_l"]]),
                 **ramp_roles("h", [(184, 104, 16), (232, 160, 32), (248, 208, 88)]),
                 w1=C["wd_m"], w2=C["wd_l"], b=INK),
}, labels={"honey": "Honey"})
def _honey():
    ic = Icon("K c1 c2 c3 h1 h2 h3 w1 w2 b")
    dip = ic.tube((13, 11), (19.5, 1.5), 1.1, ["w1", "w2"])
    head = ic.ellipse(19.5, 2.5, 1.8, 2.4)
    ic.shade(head, ["w1", "w2"])
    ic.outline(dip | head)
    pot = ic.ellipse(12, 16.5, 8, 6.3)
    rim = ic.ellipse(12, 10.5, 7, 2.2)
    neck = ic.rect(6, 10, 17, 12)
    ic.shade(pot | neck, ["c1", "c2", "c3"])
    ic.fill(rim, "h2")
    ic.shade(ic.ellipse(12, 10.5, 5.6, 1.4), ["h1", "h2", "h3"], kind="flat", light=(0, 1))
    ic.outline(pot | neck | rim)
    ic.outline(rim)
    # the dipper goes in under the rim
    ic.pxs([(13, 10), (14, 9)], "w1")
    # a drip down the side
    ic.patch(6, 11, ["h", "hH", "Hh", ".H", ".h"], {"h": "h2", "H": "h3"})
    # a band of bees, black-figure
    for x in range(5, 20):
        if pot[17, x] and ic.a[17, x] != ic.idx["K"]:
            ic.px(x, 17, "b")
    ic.pxs([(8, 16), (11, 16), (14, 16), (17, 16)], "b")
    ic.pxs([(8, 14), (7, 15)], "c3")
    return ic


# ==========================================================================
# Moomoo Milk (moomoo_milk.png): a clay jug of fresh milk.
# ==========================================================================
@icon("moomoo_milk", {
    "moomoo_milk": pal(ramp_roles("c", [C["tc_d"], C["tc_m"], C["tc_l"], C["tc_p"]]),
                       m1=(208, 200, 192), m2=C["mb_l"], b=INK),
}, labels={"moomoo_milk": "Moomoo Milk"})
def _moomoo():
    ic = Icon("K c1 c2 c3 c4 m1 m2 b")
    body = ic.ellipse(11, 15.5, 7, 6.8)
    neck = ic.poly([(7, 4), (15, 4), (14, 10), (8, 10)])
    foot = ic.rect(8, 21, 14, 22)
    handle = ic.spans(4, [(15, 18), [(15, 15), (18, 19)], [(19, 19)], [(19, 19)], [(18, 19)], [(17, 18)], [(16, 17)]])
    ic.shade(body | neck, ["c1", "c2", "c3", "c4"])
    ic.shade(foot, ["c1", "c2"], kind="cyl")
    ic.fill(handle, "c2")
    mouth = ic.ellipse(11, 4.5, 4.6, 1.7)
    ic.fill(mouth, "m2")
    ic.outline(body | neck | foot | handle | mouth)
    ic.outline(mouth)
    ic.pxs([(9, 4), (10, 4), (11, 4), (12, 4)], "m2")
    ic.pxs([(13, 4)], "m1")
    # a drip of milk on the lip
    ic.patch(7, 5, ["m", "m", "M"], {"m": "m2", "M": "m1"})
    # a black band with a cow's head? keep it plain: two rules and dots
    for x in range(4, 19):
        for y in (14, 16):
            if body[y, x] and ic.a[y, x] != ic.idx["K"]:
                ic.px(x, y, "b")
        if body[15, x] and ic.a[15, x] != ic.idx["K"] and x % 3 == 0:
            ic.px(x, 15, "b")
    ic.pxs([(7, 11), (6, 12), (7, 12)], "c4")
    return ic


# ==========================================================================
# Miracle Seed (miracle_seed.png): an olive pit putting out its first leaves.
# ==========================================================================
@icon("miracle_seed", {
    "miracle_seed": pal(ramp_roles("p", [(112, 72, 40), (168, 120, 72), (208, 168, 112), (232, 208, 160)]),
                        **ramp_roles("g", [C["ol_d"], (96, 144, 48), (152, 200, 80)])),
}, labels={"miracle_seed": "Miracle Seed"})
def _miracle_seed():
    ic = Icon("K p1 p2 p3 p4 g1 g2 g3")
    sprout = ic.tube((12, 13), (12, 7), 0.8, ["g1", "g2"])
    l1 = ic.leaf((12, 7), (5, 2), 2.4, ["g1", "g2"], rib="g1")
    l2 = ic.leaf((12, 7), (19, 3), 2.2, ["g1", "g2"], rib="g1")
    ic.outline(sprout | l1 | l2)
    ic.pxs([(8, 4), (9, 4), (15, 4)], "g3")
    pit = ic.ellipse(12, 16.5, 7.2, 5.0)
    ic.shade(pit, ["p1", "p2", "p3", "p4"])
    ic.outline(pit)
    # pointed ends and the long ridges of an olive stone
    ic.pxs([(4, 16), (20, 17)], "K")
    for x0, y0, x1, y1 in ((7, 14, 16, 13), (6, 17, 17, 16), (8, 19, 16, 20)):
        ic.line(x0, y0, x1, y1, "p2")
    ic.pxs([(8, 13), (9, 13), (7, 14)], "p4")
    return ic


# ==========================================================================
# Hard Stone (hard_stone.png): a quarried block of hard gray stone.
# ==========================================================================
@icon("hard_stone", {
    "hard_stone": pal(ramp_roles("s", [(72, 72, 80), (112, 112, 120), (160, 160, 160), (208, 208, 200)]),
                      v=C["mb_l"]),
}, labels={"hard_stone": "Hard Stone"})
def _hard_stone():
    ic = Icon("K s1 s2 s3 s4 v")
    top = ic.poly([(4, 9), (10, 4), (19, 5), (13, 10)])
    left = ic.poly([(4, 9), (13, 10), (13, 21), (5, 18)])
    right = ic.poly([(13, 10), (19, 5), (20, 15), (13, 21)])
    ic.fill(top, "s4")
    ic.fill(left & ~top, "s3")
    ic.fill(right & ~top & ~left, "s2")
    sil = top | left | right
    ic.outline(sil)
    # facet edges and chisel marks
    ic.line(4, 9, 13, 10, "s2")
    ic.line(13, 10, 19, 5, "s3")
    ic.line(13, 10, 13, 20, "s1")
    ic.pxs([(7, 12), (8, 13), (7, 15), (9, 16), (15, 12), (17, 11), (16, 15), (18, 14)], "s1")
    ic.pxs([(9, 6), (11, 6), (14, 6), (12, 7)], "s3")
    # a white vein
    ic.line(6, 17, 11, 13, "v")
    ic.pxs([(15, 17), (16, 16)], "s3")
    return ic


# ==========================================================================
# Stardust and Soft Sand (sand.png), and Star Piece (star_piece.png), which
# shares Stardust's star.pal: dust heaped on a potsherd; a star-shaped shard.
# ==========================================================================
DUST_ROLES = "K d1 d2 d3 s h1 h2 h3 b"
SHERD = dict(h1=C["tc_d"], h2=C["tc_m"], h3=C["tc_l"], b=INK)


@icon("sand", {
    "star": pal(ramp_roles("d", [(160, 48, 72), (216, 104, 120), (248, 168, 168)]), s=(248, 248, 240), **SHERD),
    "soft_sand": pal(ramp_roles("d", [(176, 136, 80), (216, 184, 120), (240, 224, 168)]), s=(248, 240, 216), **SHERD),
}, labels={"star": "Stardust", "soft_sand": "Soft Sand"})
def _sand():
    ic = Icon(DUST_ROLES)
    sherd = ic.ellipse(12, 18, 10.5, 4.2) & ~ic.ellipse(12, 15.6, 9.6, 3.2)
    ic.shade(sherd, ["h1", "h2", "h3"], kind="cyl")
    heap = ic.ellipse(12, 16, 8.5, 7.5) & ic.rect(0, 0, 23, 16)
    ic.shade(heap, ["d1", "d2", "d3"])
    ic.outline(sherd | heap)
    for x in range(3, 22):
        if sherd[19, x] and ic.a[19, x] != ic.idx["K"]:
            ic.px(x, 19, "b")
    # glints in the dust
    ic.pxs([(9, 10), (13, 12), (7, 14), (15, 15), (11, 15), (16, 11), (10, 13)], "s")
    ic.pxs([(12, 9), (8, 12), (14, 10)], "d3")
    return ic


@icon("star_piece", {
    "comet_shard": pal(ramp_roles("d", [(48, 64, 136), (96, 128, 200), (168, 200, 240)]), s=(248, 248, 240), **SHERD),
}, uses=["star"], labels={"comet_shard": "Comet Shard", ("star_piece", "star"): "Star Piece"})
def _star_piece():
    ic = Icon(DUST_ROLES)
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        r = 10.5 if i % 2 == 0 else 4.6
        pts.append((12 + r * math.cos(a), 12.8 + r * math.sin(a)))
    star = ic.poly(pts)
    ic.fill(star, "d2")
    # facets: each point lit on its upper-left side
    for i in range(0, 10, 2):
        a = -math.pi / 2 + i * math.pi / 5
        tip = (12 + 10.5 * math.cos(a), 12.8 + 10.5 * math.sin(a))
        left = (12 + 4.6 * math.cos(a - math.pi / 5), 12.8 + 4.6 * math.sin(a - math.pi / 5))
        facet = ic.poly([(12, 12.8), left, tip]) & star
        lit = (math.cos(a - math.pi / 10) * -0.75 + math.sin(a - math.pi / 10) * -0.65) > -0.2
        ic.fill(facet, "d3" if lit else "d1")
    ic.outline(star)
    ic.pxs([(11, 6), (11, 7), (8, 11), (12, 12)], "s")
    return ic


# ==========================================================================
# Pearl and Big Pearl (pearl.png, big_pearl.png; both pearl.pal): a pearl in
# its opened shell.
# ==========================================================================
PEARL_ROLES = "K p1 p2 p3 p4 s1 s2 s3 n"


@icon("pearl", {
    "pearl": pal(ramp_roles("p", [(168, 160, 176), (208, 208, 216), (240, 240, 240), (248, 248, 248)]),
                 s1=(136, 96, 80), s2=(192, 144, 120), s3=(232, 200, 176), n=(184, 200, 216)),
}, labels={"pearl": "Pearl"})
def _pearl():
    ic = Icon(PEARL_ROLES)
    shell = ic.ellipse(12, 17, 10, 4.6) & ic.rect(0, 15, 23, 23)
    lip = ic.ellipse(12, 16, 9, 2.2)
    ic.shade(shell, ["s1", "s2", "s3"], kind="cyl")
    y, x = np.mgrid[0:24, 0:24]
    ic.recolor(shell & ((x % 3) == 0), {"s3": "s2", "s2": "s1"})
    ic.fill(lip, "n")
    ic.shade(ic.ellipse(12, 16.4, 7.6, 1.4), ["n", "s3"], kind="flat")
    pearl = ic.ellipse(12, 12, 5, 5)
    ic.shade(pearl, ["p1", "p2", "p3", "p4"])
    ic.outline(shell | lip | pearl)
    ic.outline(pearl)
    ic.pxs([(10, 9), (10, 10)], "p4")
    ic.pxs([(14, 14), (15, 13)], "n")
    return ic


@icon("big_pearl", uses=["pearl"], labels={("big_pearl", "pearl"): "Big Pearl"})
def _big_pearl():
    ic = Icon(PEARL_ROLES)
    shell = ic.ellipse(12, 18, 11, 5.0) & ic.rect(0, 17, 23, 23)
    lip = ic.ellipse(12, 17.5, 10, 2.4)
    ic.shade(shell, ["s1", "s2", "s3"], kind="cyl")
    y, x = np.mgrid[0:24, 0:24]
    ic.recolor(shell & ((x % 3) == 0), {"s3": "s2", "s2": "s1"})
    ic.fill(lip, "n")
    pearl = ic.ellipse(12, 11, 7.2, 7.2)
    ic.shade(pearl, ["p1", "p2", "p3", "p4"])
    ic.outline(shell | lip | pearl)
    ic.outline(pearl)
    ic.pxs([(9, 7), (9, 8), (10, 7)], "p4")
    ic.pxs([(15, 14), (16, 13), (17, 12)], "n")
    return ic


# ==========================================================================
# Heart Scale (heart_scale.png): a heart-shaped scale with growth rings and
# a mother-of-pearl sheen.
# ==========================================================================
@icon("heart_scale", {
    "heart_scale": pal(ramp_roles("h", [(176, 88, 120), (224, 136, 160), (240, 184, 200), (248, 232, 232)]),
                       i1=(136, 184, 216), i2=(176, 224, 200)),
}, labels={"heart_scale": "Heart Scale"})
def _heart_scale():
    ic = Icon("K h1 h2 h3 h4 i1 i2")
    heart = ic.ellipse(8.2, 9.5, 5.2, 5) | ic.ellipse(15.8, 9.5, 5.2, 5) | ic.poly([(3.2, 11), (20.8, 11), (12, 21.5)])
    ic.shade(heart, ["h1", "h2", "h3", "h4"])
    ic.outline(heart)
    # growth rings
    ring = ic.ellipse(12, 15, 6.5, 5.5) & ~ic.ellipse(12, 15, 5.5, 4.5) & ic.rect(0, 9, 23, 23)
    ring2 = ic.ellipse(12, 17, 3.6, 3) & ~ic.ellipse(12, 17, 2.6, 2) & ic.rect(0, 13, 23, 23)
    ic.recolor(ring | ring2, {"h4": "h2", "h3": "h2", "h2": "h1"})
    # sheen
    ic.pxs([(6, 8), (7, 7), (8, 7)], "i2")
    ic.pxs([(15, 7), (16, 7), (14, 8)], "i1")
    ic.pxs([(6, 9), (7, 8)], "h4")
    return ic


# ==========================================================================
# Relic Copper, Silver and Gold (relic_coin.png): an archaic coin of the
# Titans' age, struck with a sickle, the Harpe.
# ==========================================================================
@icon("relic_coin", {
    "relic_copper": pal(ramp_roles("m", [(96, 48, 32), (152, 88, 56), (200, 128, 88), (232, 176, 136)]), x=(64, 32, 24)),
    "relic_silver": pal(ramp_roles("m", [(96, 96, 112), (152, 152, 168), (200, 200, 208), (240, 240, 240)]), x=(64, 64, 80)),
    "relic_gold": pal(ramp_roles("m", [(152, 96, 24), (200, 144, 40), (240, 192, 64), (248, 232, 152)]), x=(104, 64, 16)),
}, labels={"relic_copper": "Relic Copper", "relic_silver": "Relic Silver", "relic_gold": "Relic Gold"})
def _relic_coin():
    ic = Icon("K m1 m2 m3 m4 x")
    edge = ic.ellipse(12.8, 13, 9, 8.6)
    face = ic.ellipse(11.8, 12, 9, 8.6)
    ic.fill(edge, "m1")
    ic.shade(face, ["m1", "m2", "m3", "m4"])
    ic.outline(edge | face)
    # dotted border
    for i in range(20):
        a = i * 2 * math.pi / 20
        ic.px(int(round(11.8 + 6.9 * math.cos(a) - 0.5)), int(round(12 + 6.6 * math.sin(a) - 0.5)), "m1")
    # the Harpe in relief: a hooked blade on a handle, struck deep (x) with
    # its upper-left edges catching the light (h)
    ic.patch(6, 5, [
        "...hhhh...",
        ".hhxxxxh..",
        "hxxx..xxh.",
        "xx.....xx.",
        "x......xx.",
        "........xx",
        ".......xx.",
        "......xx..",
        ".....xx...",
        "....xx....",
        "...xx.....",
    ], {"x": "x", "h": "m4"})
    return ic


# ==========================================================================
# Charcoal (charcoal.png): lumps from the hearth, one still glowing.
# ==========================================================================
@icon("charcoal", {
    "charcoal": pal(ramp_roles("c", [(40, 32, 32), (72, 64, 64), (112, 104, 104), (152, 144, 144)]),
                    e1=(160, 32, 16), e2=(232, 104, 32), e3=(248, 200, 72)),
}, labels={"charcoal": "Charcoal"})
def _charcoal():
    ic = Icon("K c1 c2 c3 c4 e1 e2 e3")
    a = ic.tube((4, 15), (14, 9), 3.6, ["c1", "c2", "c3", "c4"], caps=True)
    b = ic.tube((11, 18), (20, 15), 3.2, ["c1", "c2", "c3"], caps=True)
    ic.outline(a)
    ic.outline(b)
    ic.recolor(a & b, {})
    # grain lines along each lump
    for x0, y0, x1, y1 in ((4, 14, 13, 9), (5, 17, 14, 12)):
        ic.line(x0, y0, x1, y1, "c1")
    ic.line(11, 18, 19, 15, "c1")
    # embers in the cracks of the lower lump
    ic.patch(12, 16, ["eEe..", ".eEEe", "..ee."], {"e": "e1", "E": "e2"})
    ic.pxs([(14, 17), (15, 17)], "e3")
    ic.pxs([(16, 12), (17, 11), (18, 10), (15, 10)], "e2")
    return ic


# ==========================================================================
# Old Rod (old_rod.png): a cane rod with a linen line and a bronze hook.
# ==========================================================================
@icon("old_rod", {
    "old_rod": pal(ramp_roles("w", [(120, 88, 40), (176, 136, 72), (216, 184, 112)]),
                   n=(88, 56, 32), l=(208, 200, 184), h1=C["br_m"], h2=C["sg_l"], f1=C["tc_m"], f2=C["mb_l"]),
}, labels={"old_rod": "Old Rod"})
def _old_rod():
    ic = Icon("K w1 w2 w3 n l h1 h2 f1 f2")
    rod = ic.tube((2.5, 21.5), (20.5, 2.5), 1.35, ["w1", "w2", "w3"])
    ic.outline(rod)
    for t in (0.2, 0.42, 0.64, 0.84):
        x = 2.5 + (20.5 - 2.5) * t
        y = 21.5 + (2.5 - 21.5) * t
        ic.pxs([(int(x), int(y)), (int(x) + 1, int(y))], "n")
    # grip wrapped in cord
    ic.pxs([(4, 19), (5, 18), (3, 20)], "n")
    # the line: from the tip, hanging down to the hook
    line = [(21, 3), (21, 4), (22, 5), (22, 6), (22, 7), (22, 8), (21, 9), (21, 10), (21, 11),
            (20, 12), (20, 13), (20, 14), (20, 15)]
    for x, y in line:
        ic.px(x, y, "l")
    # a cork float
    ic.patch(19, 9, ["KfK", "KFK"], {"f": "f2", "F": "f1"})
    # the hook
    ic.patch(17, 15, ["...hK", "K..hK", "KhhhK", ".KKK."], {"h": "h1"})
    ic.pxs([(20, 16)], "h2")
    return ic


# ==========================================================================
# Mystic Water (mystic_water.png): a white-ground lekythos of seawater with a
# running-wave band.
# ==========================================================================
@icon("mystic_water", {
    "mystic_water": pal(ramp_roles("m", [(176, 168, 160), (216, 208, 192), (248, 248, 240)]),
                        b=INK, **ramp_roles("w", [C["ae_d"], C["ae_m"], C["ae_l"]]), d=C["ae_p"]),
}, labels={"mystic_water": "Mystic Water"})
def _mystic_water():
    ic = Icon("K m1 m2 m3 b w1 w2 w3 d")
    # white ground body, black-glazed neck, mouth, handle and foot
    ic.art([
        "........................",
        ".......KKKKKKKK.........",
        ".......KddddddK.........",
        "......dKwbbbbbK.........",
        "......dKKbbbbKK.........",
        "......w.KbbbbK..........",
        ".........KbbKKKK........",
        ".........KbbKbbbK.......",
        "........KKbbKK.KbK......",
        "......KKmmmmmmKKbK......",
        ".....KmmmmmmmmmmKK......",
        "....KmMMMMMMMMMmmmK.....",
        "....KbbbbbbbbbbbbbK.....",
        "....KvwwWwvwwWwvwwK.....",
        "....KwWvvwWwWvvwWwK.....",
        "....KWWWWWWWWWWWWWK.....",
        "....KbbbbbbbbbbbbbK.....",
        "....KMMMMMmmmmmmmlK.....",
        "....KMMMMmmmmmmmllK.....",
        ".....KMMMmmmmmmllK......",
        "......KKmmmmmmlKK.......",
        "........KbbbbbK.........",
        ".......KbbbbbbbK........",
        "........KKKKKKK.........",
    ], {"K": "K", "b": "b", "M": "m3", "m": "m2", "l": "m1", "d": "d",
        "w": "w2", "W": "w1", "v": "w3"})
    return ic


# ==========================================================================
# Fresh Water (fresh_water.png): a hydria from the spring.
# ==========================================================================
@icon("fresh_water", {
    "fresh_water": pal(ramp_roles("c", [C["tc_d"], C["tc_m"], C["tc_l"], C["tc_p"]]),
                       b=INK, w1=C["ae_m"], w2=C["ae_p"]),
}, labels={"fresh_water": "Fresh Water"})
def _fresh_water():
    ic = Icon("K c1 c2 c3 c4 b w1 w2")
    body = ic.ellipse(12, 15, 7.5, 7) | ic.ellipse(12, 10, 6, 3)
    neck = ic.rect(9, 4, 14, 7)
    lip = ic.rect(8, 3, 15, 4)
    hl = ic.spans(12, [(3, 5), [(3, 3)], (3, 5)])
    hr = ic.spans(12, [(18, 20), [(20, 20)], (18, 20)])
    hb = ic.spans(5, [(15, 17), [(17, 17)], [(17, 18)], [(18, 18)]])
    ic.shade(body, ["c1", "c2", "c3", "c4"])
    ic.shade(neck | lip, ["c1", "c2", "c3"], kind="cyl")
    ic.fill(hl, "c2")
    ic.fill(hr | hb, "c1")
    water = ic.ellipse(11.5, 3.5, 3.2, 0.9)
    ic.fill(water, "w1")
    ic.outline(body | neck | lip | hl | hr | hb)
    ic.pxs([(10, 3), (11, 3), (12, 3), (13, 3)], "w1")
    ic.pxs([(10, 3), (11, 3)], "w2")
    for x in range(4, 21):
        for y in (14, 15):
            if body[y, x] and ic.a[y, x] != ic.idx["K"]:
                ic.px(x, y, "b")
    ic.pxs([(8, 9), (7, 10), (8, 10)], "c4")
    return ic


# ==========================================================================
# Energy Powder, Heal Powder, Shoal Salt (powder.png): a heap of ground herb
# (or salt) on an opened papyrus packet.
# ==========================================================================
@icon("powder", {
    "energy_powder": pal(ramp_roles("d", [(120, 152, 40), (176, 200, 72), (224, 232, 136)]),
                         **ramp_roles("p", [C["lp_d"], C["lp_m"], C["ln_l"]])),
    "heal_powder": pal(ramp_roles("d", [(136, 152, 120), (192, 208, 176), (240, 248, 232)]),
                       **ramp_roles("p", [C["lp_d"], C["lp_m"], C["ln_l"]])),
    "shoal_salt": pal(ramp_roles("d", [(152, 168, 192), (208, 216, 232), (248, 248, 248)]),
                      **ramp_roles("p", [C["lp_d"], C["lp_m"], C["ln_l"]])),
}, labels={"energy_powder": "Energy Powder", "heal_powder": "Heal Powder", "shoal_salt": "Shoal Salt"})
def _powder():
    ic = Icon("K d1 d2 d3 p1 p2 p3")
    paper = ic.poly([(1, 17), (8, 10), (22, 12), (16, 21)])
    ic.fill(paper, "p2")
    ic.fill(ic.poly([(1, 17), (8, 10), (9, 13), (4, 18)]), "p3")
    ic.fill(ic.poly([(16, 21), (22, 12), (20, 18)]), "p1")
    heap = ic.ellipse(12, 15.5, 7, 6) & ic.rect(0, 0, 23, 16)
    ic.shade(heap, ["d1", "d2", "d3"])
    ic.outline(paper | heap)
    ic.outline(heap)
    ic.pxs([(8, 16), (13, 16), (16, 16), (10, 17), (15, 17)], "d1")
    ic.pxs([(10, 11), (9, 12)], "d3")
    return ic


# ==========================================================================
# Energy Root (energy_root.png): a forked mandrake root.
# ==========================================================================
@icon("energy_root", {
    "energy_root": pal(ramp_roles("r", [(112, 72, 40), (168, 120, 72), (208, 168, 112), (232, 208, 160)]),
                       **ramp_roles("g", [C["ol_d"], C["ol_m"], C["ol_l"]])),
}, labels={"energy_root": "Energy Root"})
def _energy_root():
    ic = Icon("K r1 r2 r3 r4 g1 g2 g3")
    lv = ic.leaf((9, 6), (3, 1), 2.0, ["g1", "g2"], rib="g1") | ic.leaf((10, 6), (13, 0), 1.8, ["g1", "g2"], rib="g1")
    lv |= ic.leaf((10, 6), (16, 3), 1.8, ["g1", "g2"], rib="g1")
    ic.outline(lv)
    root = ic.tube((9.5, 7.5), (12.5, 15), 3.4, ["r1", "r2", "r3", "r4"], caps=True)
    leg1 = ic.tube((11, 15), (7.5, 22), 1.6, ["r1", "r2", "r3"], caps=True)
    leg2 = ic.tube((13, 15), (18.5, 21), 1.6, ["r1", "r2", "r3"], caps=True)
    arm = ic.tube((13.5, 10), (19, 8), 1.1, ["r1", "r2", "r3"], caps=True)
    ic.outline(root | leg1 | leg2 | arm)
    ic.pxs([(9, 11), (11, 13), (10, 9)], "r2")
    ic.pxs([(5, 23), (20, 22), (21, 22), (20, 7)], "r1")
    return ic


# ==========================================================================
# Revival Herb (revival_herb.png): the herb Polyidos used to bring Glaukos
# back: a sprig with gold star flowers.
# ==========================================================================
@icon("revival_herb", {
    "revival_herb": pal(ramp_roles("l", [C["cy_d"], C["cy_m"], (88, 152, 88)]), st=(88, 72, 40),
                        **ramp_roles("fl", [C["sg_d"], C["sg_l"], C["sg_p"]])),
}, labels={"revival_herb": "Revival Herb"})
def _revival_herb():
    ic = Icon("K l1 l2 l3 st fl1 fl2 fl3")
    stem = ic.tube((5, 22), (14, 6), 0.9, ["st", "l1"])
    sil = stem
    for base, tip, w in (((7, 18), (2, 13), 2.0), ((8, 17), (14, 16), 1.9), ((10, 13), (5, 8), 1.9),
                         ((11, 12), (18, 11), 1.9), ((13, 9), (9, 3), 1.7)):
        sil |= ic.leaf(base, tip, w, ["l1", "l2"], rib="l1")
    ic.outline(sil)
    for cx, cy in ((15, 4), (19, 7), (17, 1)):
        ic.patch(cx - 2, cy - 2, [".K.K.", "KfFfK", ".FgF.", "KfFfK", ".K.K."],
                 {"f": "fl1", "F": "fl2", "g": "fl3"})
    return ic


# ==========================================================================
# TMs (tm.png) and HMs (hm.png), colored by gTypesInfo[].paletteTMHM: a
# papyrus scroll tied with a cord and sealed, the cord and wax in the move's
# type color; an HM is a hinged wax tablet tied the same way.
# ==========================================================================
SCROLL_ROLES = "K p1 p2 p3 p4 r1 r2 w1 w2 w3 w4"

TYPE_COLORS = {
    "normal": (176, 168, 144), "fighting": (184, 56, 40), "flying": (136, 144, 216),
    "poison": (152, 72, 168), "ground": (208, 160, 72), "rock": (168, 144, 64),
    "bug": (144, 176, 32), "ghost": (104, 88, 160), "steel": (168, 168, 192),
    "mystery": (96, 160, 144), "fire": (232, 96, 40), "water": (64, 120, 224),
    "grass": (96, 176, 64), "electric": (240, 192, 48), "psychic": (232, 88, 136),
    "ice": (120, 200, 216), "dragon": (104, 64, 216), "dark": (96, 72, 64),
    "fairy": (232, 144, 200),
}


def _scroll_pal(base):
    r = ramp4(base)
    return pal(dict(p1=(160, 128, 80), p2=C["lp_m"], p3=C["lp_l"], p4=C["ln_l"],
                    r1=C["wd_d"], r2=C["wd_l"], w1=r[0], w2=r[1], w3=r[2], w4=r[3]))


@icon("tm", {f"{t}_tm_hm": _scroll_pal(c) for t, c in TYPE_COLORS.items()},
      labels={f"{t}_tm_hm": f"TM ({t})" for t in TYPE_COLORS})
def _tm():
    ic = Icon(SCROLL_ROLES)
    a, b = (5.2, 18.8), (18.8, 5.2)
    roll = ic.tube(a, b, 3.9, ["p1", "p2", "p3", "p4"], caps=False)
    ic.outline(roll)
    # the rod's knobs stand out of both ends
    for x, y in ((2, 18), (18, 2)):
        ic.patch(x, y, [".KK.", "KrRK", "KRRK", ".KK."], {"r": "r2", "R": "r1"})
    # the rolled edge: a spiral line near the upper end
    t, s, ln = ic.tube_coords(a, b)
    edge = roll & (np.abs(t * ln - (ln - 2.2)) < 0.6) & (s > -2.5)
    ic.fill(edge, "p1")
    # the cord: one turn round the middle, in the type color
    cord = roll & (np.abs(t - 0.5) * ln < 1.1)
    ic.fill(cord, "w2")
    ic.recolor(cord & (s > 1.2), {"w2": "w1"})
    # the seal: a disc of wax, lit at the top left, stamped
    ic.patch(8, 9, [
        "..KKKK..",
        ".KwVvwK.",
        "KwVvwwAK",
        "KvwAwwAK",
        "KwwwwAAK",
        "KwwAAAAK",
        ".KAAAAK.",
        "..KKKK..",
    ], {"V": "w4", "v": "w3", "w": "w2", "A": "w1"})
    # cord tails below the seal
    ic.patch(12, 17, ["Kw", ".Kw", "..K"], {"w": "w2"})
    ic.patch(9, 17, ["wK", "w.", "K."], {"w": "w1"})
    return ic


@icon("hm", uses=list(f"{t}_tm_hm" for t in TYPE_COLORS), labels={})
def _hm():
    ic = Icon(SCROLL_ROLES)
    back = ic.poly([(4, 4), (18, 3), (19, 17), (5, 18)])
    front = ic.poly([(6, 7), (20, 6), (21, 21), (7, 21)])
    ic.fill(back, "r1")
    ic.fill(front, "r2")
    wax = ic.poly([(8.5, 9), (18.5, 8.5), (19, 19), (9, 19)])
    ic.fill(wax, "p1")
    ic.outline(back)
    ic.outline(front)
    ic.outline(wax)
    # lines written in the wax
    for y in (11, 13, 15, 17):
        ic.line(10, y, 17, y, "p2")
    # the tie and its seal
    ic.line(5, 13, 21, 13, "w2")
    ic.line(5, 14, 21, 14, "w1")
    seal = ic.ellipse(13.5, 13.5, 3.4, 3.4)
    ic.shade(seal, ["w1", "w2", "w3", "w4"])
    ic.outline(seal)
    ic.pxs([(12, 12)], "w4")
    return ic


# ==========================================================================
# Flag-only key items of the slice, drawn for when they become items.
# ==========================================================================
@icon("ichor_talaria", {
    "ichor_talaria": pal(ramp_roles("le", [(104, 56, 32), (160, 96, 56), (208, 144, 96)]),
                         **ramp_roles("f", [C["mb_d"], C["mb_m"], C["mb_l"]]), g1=C["sg_d"], g2=C["sg_l"]),
}, labels={"ichor_talaria": "Talaria (asset)"}, asset=True)
def _talaria():
    ic = Icon("K le1 le2 le3 f1 f2 f3 g1 g2")
    # a laced sandal-boot in profile, toe to the left, a wing at the ankle
    ic.art([
        "........................",
        "....................KK..",
        "................KK.KFFK.",
        "...............KFFKKFfFK",
        "..............KKFfFKFfK.",
        "...........KKKKKFfFfffK.",
        "..........KooooooKFffK..",
        "..........KLlLlLlKKKK...",
        "..........KlLlLlLlK.....",
        "..........KLlLlLlLK.....",
        "..........KlLlLlLlK.....",
        ".........KLlLlLlLlK.....",
        "........KLlLlLlLlLK.....",
        "......KKLlLlLlLlLlK.....",
        "....KKLlLlLlLlLlLlK.....",
        "...KLlLlLlLlLlLlLlK.....",
        "..KLlLlLlLlLlLlLlLK.....",
        "..KLLLLLLLLLLLLLLLLK....",
        "..KsssssssssssssssssK...",
        "...KKKKKKKKKKKKKKKKK....",
        "........................",
        "........................",
        "........................",
        "........................",
    ], {"K": "K", "f": "f2", "F": "f3", "l": "le2", "L": "le3", "s": "le1", "o": "le1"})
    # quills, and a gold buckle at the ankle
    ic.pxs([(21, 4), (20, 5), (18, 3)], "f1")
    ic.patch(15, 8, ["gG"], {"g": "g1", "G": "g2"})
    ic.pxs([(16, 15), (17, 16), (16, 16)], "le1")
    return ic


@icon("ichor_augurs_eye", {
    "ichor_augurs_eye": pal(ramp_roles("b", [(88, 48, 24), C["br_m"], (200, 144, 72), (240, 200, 128)]),
                            e1=C["mb_l"], e2=C["ae_m"], p=C["ae_d"], c=C["tc_d"]),
}, labels={"ichor_augurs_eye": "Augur's Eye (asset)"}, asset=True)
def _augurs_eye():
    ic = Icon("K b1 b2 b3 b4 e1 e2 p c")
    disc = ic.ellipse(12, 13, 7.5, 7.5)
    wl = ic.poly([(5, 10), (0, 8), (1, 12), (0, 15), (5, 16)])
    wr = ic.poly([(19, 10), (24, 8), (23, 12), (24, 15), (19, 16)])
    ic.shade(wl | wr, ["b1", "b2", "b3"])
    ic.shade(disc, ["b1", "b2", "b3", "b4"])
    ic.outline(disc | wl | wr)
    for y in (10, 12, 14):
        ic.line(1, y, 4, y + 1, "b1")
        ic.line(19, y + 1, 22, y, "b1")
    eye = ic.ellipse(12, 13, 4.6, 2.6)
    ic.fill(eye, "e1")
    ic.outline(eye)
    iris = ic.ellipse(12, 13, 2.0, 2.0)
    ic.fill(iris, "e2")
    ic.pxs([(12, 13), (11, 13)], "p")
    ic.px(11, 12, "e1")
    # the loop and its cord
    ic.patch(10, 2, [".KKK.", "K...K", "KbbbK"], {"b": "b2"})
    ic.pxs([(9, 1), (8, 0), (15, 1), (16, 0)], "c")
    return ic


@icon("ichor_codex", {
    "ichor_codex": pal(ramp_roles("w", [C["wd_d"], C["wd_m"], C["wd_l"]]),
                       x1=(40, 32, 24), x2=(88, 72, 48), c=C["tc_m"], g=C["sg_l"], ln=C["lp_l"]),
}, labels={"ichor_codex": "Pokedex codex (asset)"}, asset=True)
def _codex():
    ic = Icon("K w1 w2 w3 x1 x2 c g ln")
    lb = ic.poly([(1, 6), (11, 4), (12, 20), (2, 21)])
    rb = ic.poly([(12, 4), (22, 6), (21, 21), (12, 20)])
    ic.fill(lb, "w2")
    ic.fill(rb, "w1")
    ic.outline(lb | rb)
    wl = ic.poly([(3, 8), (10, 6.5), (10.5, 18), (3.5, 19)])
    wr = ic.poly([(13.5, 6.5), (20, 8), (19.5, 19), (13, 18)])
    ic.fill(wl | wr, "x2")
    ic.outline(wl)
    ic.outline(wr)
    # a sketch of a Pokemon scratched in the wax, and lines of notes
    ic.patch(4, 9, [".ln.", "lnnl", ".ll.", "l..l"], {"l": "ln", "n": "x2"})
    for y in (9, 11, 13, 15, 17):
        ic.line(14, y, 18, y, "ln")
    ic.pxs([(5, 15), (6, 16), (7, 15), (8, 16)], "ln")
    # binding cords and a gold clasp
    for y in (8, 16):
        ic.pxs([(11, y), (12, y)], "c")
    ic.pxs([(21, 13), (22, 13)], "g")
    ic.pxs([(2, 7), (3, 6)], "w3")
    return ic


@icon("ichor_hearth_laurel", {
    "ichor_hearth_laurel": pal(ramp_roles("l", [C["cy_d"], (64, 120, 64), (128, 176, 96)]),
                               g1=C["sg_d"], g2=C["sg_l"], f1=(216, 72, 32), f2=(248, 176, 64), r=C["tc_m"]),
}, labels={"ichor_hearth_laurel": "Hearth Laurel (asset)"}, asset=True)
def _hearth_laurel():
    ic = Icon("K l1 l2 l3 g1 g2 f1 f2 r")
    stem = ic.tube((4, 21), (17, 5), 0.8, ["g1", "g2"])
    sil = stem
    for base, tip, w in (((6, 18), (2, 12), 2.2), ((7, 17), (13, 18), 2.1), ((9, 14), (5, 8), 2.1),
                         ((10, 13), (17, 13), 2.0), ((12, 10), (9, 3), 2.0), ((14, 9), (20, 8), 1.9)):
        sil |= ic.leaf(base, tip, w, ["l1", "l2"], rib="l1")
    ic.outline(sil)
    for base, tip, w in (((9, 14), (5, 8), 2.1), ((12, 10), (9, 3), 2.0)):
        ic.pxs([(int((base[0] + tip[0]) / 2) - 1, int((base[1] + tip[1]) / 2))], "l3")
    # gilded tips, and the hearth's flame at the top
    ic.pxs([(2, 12), (13, 18), (5, 8), (17, 13), (9, 3), (20, 8)], "g2")
    ic.patch(16, 0, [".f..", "fFf.", "fFFf", ".ff."], {"f": "f1", "F": "f2"})
    ic.patch(3, 20, ["rr", ".rr", "..r"], {"r": "r"})
    return ic


# ==========================================================================
# The ground item (OBJ_EVENT_GFX_ITEM_BALL): a small clay jar sealed with
# beeswax and tied with twine, in the townsfolk palette (ichor_folk.pal), so a
# map that shows folk spends no extra palette slot on it. 16x16, one frame.
# ==========================================================================
JAR_PATH = os.path.join(ROOT, "graphics/object_events/pics/misc/ichor_item_jar.png")
FOLK_PAL = os.path.join(ROOT, "graphics/object_events/palettes/ichor_folk.pal")
# folk palette letters (SPRITES_folk.md): k ink, b brown, u terra, o ochre,
# O gold, s skin_d (light clay), S skin_l (clay highlight), l/L linen
FOLK_INDEX = {"k": 1, "b": 2, "u": 3, "o": 4, "O": 5, "s": 6, "S": 7, "l": 8, "L": 9}
JAR = [
    "................",
    "................",
    "......kkkk......",
    ".....kOOook.....",
    ".....kLLllk.....",
    "......ksuk......",
    "....kSsuuubk....",
    "...kSSsuuuubk...",
    "..kkkkkkkkkkkk..",
    "..kLkLkLkLkLkk..",
    "..kSsuuuuuubbk..",
    "..kSsuuuuuubbk..",
    "...ksuuuuubbk...",
    "....ksuuubbk....",
    ".....kbbbbk.....",
    "......kkkk......",
]


def jar_array():
    assert len(JAR) == 16 and all(len(r) == 16 for r in JAR), [len(r) for r in JAR]
    a = np.zeros((16, 16), np.int32)
    for y, row in enumerate(JAR):
        for x, ch in enumerate(row):
            if ch != ".":
                a[y, x] = FOLK_INDEX[ch]
    return a


def folk_colors():
    vals = open(FOLK_PAL).read().split()[3:]
    return [tuple(int(v) for v in vals[i * 3:i * 3 + 3]) for i in range(16)]


def write_jar():
    save_indexed(jar_array(), folk_colors(), JAR_PATH)
    print(f"items.py: wrote {os.path.relpath(JAR_PATH, ROOT)}")


# ==========================================================================
# Checks, files and sheets
# ==========================================================================

def items_sharing():
    """pic stem -> {palette stem: [items]}, from src/data/items.h."""
    src = open(os.path.join(ROOT, "src/data/items.h")).read()
    gfx = open(os.path.join(ROOT, "src/data/graphics/items.h")).read()
    pic_file = dict(re.findall(r'const u32 (gItemIcon_\w+)\[\] = INCGFX_U32\("graphics/items/icons/(\w+)\.png"', gfx))
    pal_file = dict(re.findall(r'const u16 (gItemIconPalette_\w+)\[\] = INCGFX_U16\("graphics/items/icon_palettes/(\w+)\.pal"', gfx))
    out = defaultdict(lambda: defaultdict(list))
    for m in re.finditer(r'\[(ITEM_\w+)\]\s*=\s*\{(.*?)\n    \},', src, re.S):
        pic = re.search(r'\.iconPic\s*=\s*(\w+)', m.group(2))
        pal_ = re.search(r'\.iconPalette\s*=\s*(\w+)', m.group(2))
        if pic and pal_ and pic.group(1) in pic_file and pal_.group(1) in pal_file:
            out[pic_file[pic.group(1)]][pal_file[pal_.group(1)]].append(m.group(1))
    return out


def check_sharing():
    """Every palette that colors one of our pics must be one we write, and
    every palette we write must color only pics we draw, over the same roles."""
    share = items_sharing()
    pics_of_pal = defaultdict(set)
    for pic, pals in share.items():
        for p in pals:
            pics_of_pal[p].add(pic)
    ok = True
    for pic in PICS:
        if pic in ("tm", "hm") or pic in ASSETS:
            continue  # TM/HM colors come from gTypesInfo[].paletteTMHM
        for p in share.get(pic, {}):
            if p not in PIC_PALS[pic]:
                print(f"items.py: {pic}.png is also colored by {p}.pal {share[pic][p]}, which this file does not write")
                ok = False
        for p in PIC_PALS[pic]:
            for other in pics_of_pal.get(p, ()):
                if other not in PICS:
                    print(f"items.py: {p}.pal also colors {other}.png, which this file does not draw")
                    ok = False
    for pic, stems in PIC_PALS.items():
        for p in stems:
            if tuple(PICS[pic].roles) != PALETTES[p][0]:
                print(f"items.py: {pic}.png and {p}.pal disagree on roles")
                ok = False
    return ok


def write_all():
    for pic, ic in PICS.items():
        first = PALETTES[PIC_PALS[pic][0]][1]
        save_indexed(ic.a, palette_colors(ic.roles, first), os.path.join(ICONS, pic + ".png"))
    for stem, (roles, cols) in PALETTES.items():
        write_jasc(os.path.join(PALS, stem + ".pal"), palette_colors(roles, cols))
    print(f"items.py: wrote {len(PICS)} pics and {len(PALETTES)} palettes")


def git_original(path):
    rel = os.path.relpath(path, ROOT)
    try:
        return subprocess.run(["git", "-C", ROOT, "show", f"{BASE_REV}:{rel}"],
                              capture_output=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None


def original_rgb(pic, stem, bg):
    p = git_original(os.path.join(ICONS, pic + ".png"))
    q = git_original(os.path.join(PALS, stem + ".pal"))
    if not p or not q:
        return None
    a = np.array(Image.open(io.BytesIO(p))) % 16
    vals = q.decode().split()[3:]
    cols = [tuple(int(v) for v in vals[i * 3:i * 3 + 3]) for i in range(16)]
    return to_rgb(a, cols, bg)


PARCH = (232, 216, 176)     # the bag's icon plate
CLAY_BG = (184, 88, 48)     # the bag's field


def new_rgb(pic, stem, bg):
    ic = PICS[pic]
    return to_rgb(ic.a, palette_colors(ic.roles, PALETTES[stem][1]), bg)


def preview(outdir):
    os.makedirs(outdir, exist_ok=True)
    entries = [(pic, stem) for pic, stem in ORDER if pic not in ("tm", "hm")]
    k = 4
    cell_w, cell_h = 2 * 24 * k + 3 * 8 + 2 * 26 + 8, 24 * k + 30
    cols_n = 4
    rows_n = (len(entries) + cols_n - 1) // cols_n
    sheet = Image.new("RGB", (cols_n * cell_w, rows_n * cell_h + 20), (64, 40, 32))
    d = ImageDraw.Draw(sheet)
    d.text((6, 4), "before (main) | after, 4x on the bag's parchment plate | after and before at 1x, "
                   "on parchment and on clay", fill=(248, 224, 136))
    for i, (pic, stem) in enumerate(entries):
        r, c = divmod(i, cols_n)
        x0, y0 = c * cell_w + 6, r * cell_h + 24
        old = original_rgb(pic, stem, PARCH)
        new = new_rgb(pic, stem, PARCH)
        d.text((x0, y0), LABELS.get((pic, stem), LABELS.get(stem, stem)) + ("" if pic == stem else f"  [{pic}]"),
               fill=(248, 240, 216))
        y = y0 + 13
        if old is not None:
            sheet.paste(Image.fromarray(upscale(old, k)), (x0, y))
        else:
            d.text((x0 + 8, y + 40), "(new)", fill=(200, 192, 184))
        sheet.paste(Image.fromarray(upscale(new, k)), (x0 + 24 * k + 8, y))
        xs = x0 + 2 * (24 * k + 8)
        sheet.paste(Image.fromarray(new), (xs, y))
        sheet.paste(Image.fromarray(new_rgb(pic, stem, CLAY_BG)), (xs + 26, y))
        if old is not None:
            sheet.paste(Image.fromarray(old), (xs, y + 28))
            sheet.paste(Image.fromarray(original_rgb(pic, stem, CLAY_BG)), (xs + 26, y + 28))
    sheet.save(os.path.join(outdir, "items_icons.png"))

    # TMs and HMs in every type color
    stems = PIC_PALS["tm"]
    sheet = Image.new("RGB", (len(stems) * (24 * 3 + 6) + 6, 2 * (24 * 3 + 6) + 40), (64, 40, 32))
    d = ImageDraw.Draw(sheet)
    for i, stem in enumerate(stems):
        x = 6 + i * (24 * 3 + 6)
        d.text((x, 4), stem.replace("_tm_hm", ""), fill=(248, 240, 216))
        sheet.paste(Image.fromarray(upscale(new_rgb("tm", stem, PARCH), 3)), (x, 18))
        sheet.paste(Image.fromarray(upscale(new_rgb("hm", stem, PARCH), 3)), (x, 18 + 24 * 3 + 6))
    sheet.save(os.path.join(outdir, "items_icons_tm.png"))
    print(f"items.py: preview in {outdir}")


def preview_jar(outdir):
    """The jar where the slice places it (every item object on the Ichor
    maps), and on a floor or ground of every slice tileset, at 3x."""
    import json
    sys.path.insert(0, os.path.join(ROOT, "tools/ichor"))
    import render_map as R
    R.read_fieldmap_constants()
    syms = R.scan_tileset_symbols()
    jar = to_rgb(jar_array(), folk_colors())

    def put(img, x, y):
        a = jar[..., 3:4] / 255.0
        sub = img[y:y + 16, x:x + 16]
        sub[...] = (jar[..., :3] * a + sub * (1 - a)).astype(np.uint8)

    layouts = {l["id"]: l for l in json.load(open(os.path.join(ROOT, "data/layouts/layouts.json")))["layouts"] if "id" in l}
    shots = []
    for m in ("KallisteRoute1", "KallisteRoute1_KronionHill", "AktiTown"):
        mj = json.load(open(os.path.join(ROOT, f"data/maps/{m}/map.json")))
        lay = layouts[mj["layout"]]
        r = R.Renderer(R.Tileset(R.resolve_tileset(lay["primary_tileset"], syms)),
                       R.Tileset(R.resolve_tileset(lay["secondary_tileset"], syms)))
        blocks = np.fromfile(os.path.join(ROOT, lay["blockdata_filepath"]), "<u2").reshape(lay["height"], lay["width"])
        for o in mj.get("object_events", []):
            if o.get("graphics_id") != "OBJ_EVENT_GFX_ITEM_BALL":
                continue
            ox, oy = o["x"], o["y"]
            img = np.zeros((48, 80, 3), np.uint8)
            for dy in range(-1, 2):
                for dx in range(-2, 3):
                    x, y = ox + dx, oy + dy
                    if 0 <= x < lay["width"] and 0 <= y < lay["height"]:
                        img[(dy + 1) * 16:(dy + 2) * 16, (dx + 2) * 16:(dx + 3) * 16] = r.metatile(int(blocks[y, x]) & 0x3FF)[0]
            put(img, 32, 16)
            shots.append((f"{m} ({ox},{oy}) {o.get('flag', '').replace('FLAG_ICHOR_', '')}", img))
    # one ground of each slice tileset pairing
    grounds = [("aethos grass", "aethos", "kalliste", 0x001), ("aethos barley", "aethos", "kalliste", 0x00D),
               ("aethos path", "aethos", "kalliste", 0x1D9), ("aethos sand", "aethos", "kalliste", 0x124),
               ("aethos rock floor", "aethos", "kalliste", 0x0E9), ("kalliste paving", "aethos", "kalliste", 0x26B),
               ("oikos terracotta", "oikos", "oikia", 0x008), ("oikos marble", "oikos", "civic", 0x00B),
               ("temple floor", "oikos", "temple_hestia", 0x201)]
    for name, p, s, mid in grounds:
        r = R.Renderer(R.Tileset(R.resolve_tileset(p, syms)), R.Tileset(R.resolve_tileset(s, syms)))
        img = np.zeros((48, 80, 3), np.uint8)
        for yy in range(3):
            for xx in range(5):
                img[yy * 16:(yy + 1) * 16, xx * 16:(xx + 1) * 16] = r.metatile(mid)[0]
        put(img, 32, 16)
        shots.append((name, img))
    k = 3
    cols = 4
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (80 * k + 10) + 10, rows * (48 * k + 20) + 10), (64, 40, 32))
    d = ImageDraw.Draw(sheet)
    for i, (name, img) in enumerate(shots):
        r_, c = divmod(i, cols)
        x, y = 10 + c * (80 * k + 10), 10 + r_ * (48 * k + 20)
        d.text((x, y), name, fill=(248, 240, 216))
        sheet.paste(Image.fromarray(upscale(img, k)), (x, y + 12))
    sheet.save(os.path.join(outdir, "items_ground_jar.png"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--preview")
    args = ap.parse_args()
    if not check_sharing():
        sys.exit(1)
    if args.write:
        write_all()
        write_jar()
    if args.preview:
        preview(args.preview)
        preview_jar(args.preview)


if __name__ == "__main__":
    main()
