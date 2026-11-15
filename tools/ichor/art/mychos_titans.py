"""The Titan wing, for gTileset_Mychos (LABYRINTH.md §6, Rings IV and VI).

  Ring IV   Team Titan's barracks and mess hall, lit by their oil lamps: bunks,
            the helmet locker (the disguise), a weapon rack, mess tables, the
            sickle banners, bronze grates, the lamps on their stands
  Ring VI   the forge (scene G): the furnace, Hyperion's anvil, bellows, the
            quench trough, the molten runnel, slag; the Hall of Dials: Daedalus's
            dials and the wall segments they swing; the archive (scene H): shelves
            of wax tablets, the forged tablet on its desk; the vault; the
            Mistress's shrine on the landing below
  both      the fresco of the dance's steps 1-3 (Ring IV) and 7-9 (Ring VI), the
            doorways and labrys seals

Everything stands on the rings' dark floor (labyrinth_kit), so each floor piece
comes as twins: `<key>` where its top-left cell has x + y even, `<key>_odd` where
odd.
"""
from __future__ import annotations

import copy
import math

import labyrinth_art as A
import labyrinth_kit as KIT
import labyrinth_rings as R
import labyrinth_workshop as WS
from labyrinth_art import Struct, blit

BZ = {"k": "ink", "0": "bz0", "1": "bz1", "2": "bz2", "3": "bz3", "4": "bz4", "w": "bw",
      "e": "be", "v": "bv0", "V": "bv1", "i": "bi0", "I": "bi1", "s": "ts0", "S": "ts1",
      "r": "brp"}
TM = WS.TM
FI = R.FI
MN = {"k": "ink", "R": "mr0", "r": "mr1", "e": "mr2", "E": "mr3", "o": "mo0", "O": "mo1",
      "y": "mo2", "g": "mg0", "G": "mg1", "W": "mg2", "b": "mb", "0": "mt0", "1": "mt1",
      "2": "mt2"}


def on_dark(s):
    """Re-lay a workshop piece's floor cells with the rings' dark floor."""
    KIT.on_ring_floor(s, s.floor_cells, odd=getattr(s, "parity", None) == "odd")
    return s


def rekey(pair, key, title, notes):
    """A workshop piece and its odd twin, renamed and set on the dark floor."""
    out = []
    for s in pair:
        t = copy.deepcopy(s)
        odd = t.key.endswith("_odd")
        t.key = key + ("_odd" if odd else "")
        t.title = title + (" (odd cells)" if odd else "")
        if odd:
            t.twin_of = (key, t.twin_of[1])
            t.notes = t.notes.replace(f"`{s.key[:-4]}`", f"`{key}`")
        else:
            t.notes = notes
        on_dark(t)
        out.append(t)
    return out


# --------------------------------------------------------------------------
# Ring IV: the barracks and the mess hall
# --------------------------------------------------------------------------

def bunk():
    """A Titan's cot: the workshop's kline with a grey army blanket."""
    pair = WS.kline()
    for s in pair:
        for ln in ("bottom", "middle"):
            L = s.layers[ln]
            for y in range(L.h):
                for x in range(L.w):
                    c = L.get(x, y)
                    if c in ("tb0", "tb1"):
                        L.px(x, y, {"tb0": "tg", "tb1": "tq"}[c])
    return rekey(pair, "bunk", "Barracks: a Titan's bunk",
                 "A plain timber cot with a grey wool blanket and a fleece, two cells wide: the "
                 "barracks' bunks (Ring IV). Blocks.")


def mess_table():
    """A long trestle table laid for the mess: bowls of barley, bread, a jug."""
    s = Struct("mess_table", "Mess hall: a trestle table, laid", 3, 2, walk=["XXX", "XXX"],
               notes="A mess-hall table three cells long, laid with bowls of barley, flat "
                     "loaves, cups and a wine jug (Ring IV; the grunts talk across it). Top row "
                     "the board, bottom row its front and trestles. `mess_table_odd` holds its "
                     "bottom row on the odd parity.")
    s.floor_cells = [(x, 1) for x in range(3)]
    R.lay(s)
    B, M = s.B, s.M
    # the board fills the top row (bottom layer, so what's on it can be clay);
    # its front edge hangs into the bottom row (middle layer, over the floor)
    for y in range(0, 22):
        for x in range(0, 48):
            if y < 16:
                if y == 0:
                    c = "tw3"
                elif x in (0, 47):
                    c = "ink"
                else:
                    c = "tw2" if (y - 1) % 4 else "tw1"
                B.px(x, y, c)
            else:
                if x in (0, 47) or y == 21:
                    c = "ink"
                else:
                    c = "tw2" if y < 18 else "tw1"
                M.px(x, y, c)
    # trestle legs under it (middle layer, timber, over the floor)
    for lx in (4, 42):
        blit(M, ["k11k", ".k1k.", "k1k1k", "k1..1k", "kk..kk"], TM, lx - 1, 22)
    for x in range(6, 42):
        M.px(x, 25, "tw0")
    # bowls of barley, loaves, cups, a jug
    for bx in (5, 19, 33):
        blit(M, [".kkkk.", "kbbbbk", "k0000k", ".kkkk."], {**MN, "b": "mo2", "0": "mt1"}, bx, 9)
    for bx in (12, 27):
        blit(M, [".kkk.", "kyyyk", "kOOOk", ".kkk."], MN, bx, 13)
    for bx in (16, 38):
        blit(M, ["kk", "21"], MN, bx, 14)
    blit(M, [".kk.", "k21k", "k11k", "k10k", ".kk."], MN, 41, 8)
    s.names = {"top_l": (0, 0), "top_m": (1, 0), "top_r": (2, 0),
               "front_l": (0, 1), "front_m": (1, 1), "front_r": (2, 1)}
    return R.twins(s)


def helmet_rack():
    """The helmet locker in the barracks: bronze Corinthian helmets on pegs, one
    spare (the disguise, LABYRINTH.md §5.6)."""
    s = Struct("helmets", "Barracks: the helmet locker", 2, 2, walk=["XX", "XX"],
               notes="The barracks' helmet locker, two cells: an open timber press with three "
                     "bronze Corinthian helmets on its shelves, crested, and a gap where the "
                     "spare was. The disguise's bg event goes on its bottom row (Ring IV). "
                     "`helmets_odd` on the odd parity.")
    R.lay(s)
    M = s.M
    # the press: dark oak (the bronze palette's browns), back in shadow, a shelf
    for y in range(1, 30):
        for x in range(1, 31):
            if x in (1, 30) or y in (1, 29):
                c = "ink"
            elif x in (2, 29) or y in (2, 15, 28):
                c = "bz1" if x == 2 or y == 2 else "bz0"
            elif y == 16:
                c = "bz1"
            else:
                c = "ts0"
            M.px(x, y, c)
    helmet = [".kkkkk..",
              "k34433k.",
              "k3kk32k.",
              "k3.k31k.",
              "k32k21k.",
              ".kk.kk.."]
    crest = ["..SSSS..", ".SseesS."]
    for (hx, hy) in ((4, 7), (17, 7), (4, 21)):
        blit(M, crest, BZ, hx, hy - 2)
        blit(M, helmet, BZ, hx, hy)
    # the spare's peg, empty, a tuft of its crest left behind
    M.px(21, 23, "bz3")
    M.px(22, 25, "ts1")
    M.px(23, 26, "ts1")
    s.names = {"tl": (0, 0), "tr": (1, 0), "bl": (0, 1), "br": (1, 1)}
    return R.twins(s)


def weapon_rack():
    """Spears and round shields: the armory."""
    s = Struct("armory", "Barracks: spears and shields", 2, 2, walk=["XX", "XX"],
               notes="An armory rack: spears upright in a timber stand, two round bronze shields "
                     "with the sickle blazon leaning against it (Ring IV's armory dead end). "
                     "`armory_odd` on the odd parity.")
    R.lay(s)
    M = s.M
    # ash spear-shafts (the bronze palette's pale rope color) with iron heads,
    # in a dark oak stand
    for sx in (5, 10, 15, 20, 25):
        for y in range(3, 28):
            M.px(sx, y, "brp" if y > 6 else "bi1")
        blit(M, [".k.", "kIk", "kIk", ".k."], BZ, sx - 1, 0)
    for x in range(2, 30):
        M.px(x, 20, "ink")
        M.px(x, 21, "bz1")
        M.px(x, 22, "bz0")
        M.px(x, 23, "ink")
    for (cx, cy) in ((9, 22), (22, 23)):
        for y in range(cy - 7, cy + 8):
            for x in range(cx - 7, cx + 8):
                d = math.hypot(x - cx, y - cy)
                if d <= 7.4:
                    c = "ink" if d > 6.5 else "bz3" if (x - cx) + (y - cy) < -3 else "bz2"
                    if d <= 2.2:
                        c = "be"
                    M.px(x, y, c)
        # the sickle blazon
        blit(M, ["..kk", ".k..", "k...", "k...", ".kk."], BZ, cx - 2, cy - 2)
    s.names = {"tl": (0, 0), "tr": (1, 0), "bl": (0, 1), "br": (1, 1)}
    return R.twins(s)


def banners():
    """The sickle banners: Kronos's sign, gold on Titan slate, hung on the walls."""
    s = Struct("banners", "Sickle banners on the walls", 3, 1, walk=["XXX"],
               notes="Team Titan's banners hung on a face: slate cloth, a gold sickle, gold "
                     "fringe. (0) `face`: on a face that runs on; (1) `torn`: one slashed and "
                     "hanging in tatters; (2) `top_n`: a banner pole bracket on a wall top's north "
                     "rim (for the far side of a hall). All block.")
    L, M = s.B, s.M
    for i in range(2):
        R.face(L, i * 16, 0)
        x0 = i * 16
        # the bracket and pole
        for x in range(2, 14):
            M.px(x0 + x, 3, "bz3")
            M.px(x0 + x, 4, "bz1")
        M.px(x0 + 1, 3, "ink")
        M.px(x0 + 14, 3, "ink")
        # the sickle: a hooked blade on a short haft
        cloth = ["kSSSSSSSSk",
                 "kSss444ssk",
                 "kss4sss4sk",
                 "ks4ssssssk",
                 "ks4ssssssk",
                 "kss4sssssk",
                 "ksss44sssk",
                 "kssss1sssk",
                 "kssss1sssk",
                 "kekekekekk"]
        if i == 1:
            cloth = ["kSSSSSSSSk",
                     "kSssssssSk",
                     "ksss44sssk",
                     "kss4ks4ssk",
                     "ks4sk.sssk",
                     "ks4sk.ssk.",
                     "kss4k.ssk.",
                     "ksssk..sk.",
                     "kssk...kk.",
                     "kek......."]
        blit(M, cloth, BZ, x0 + 3, 5)
    R.top(L, 32, 0, n=True)
    blit(M, ["kkkkkkkkkk", "k32222221k", "kkkkkkkkkk"], BZ, 35, 6)
    blit(M, ["k4k", "kek"], BZ, 34, 5)
    s.names = {"face": (0, 0), "torn": (1, 0), "top_n": (2, 0)}
    return s


def titan_lamp():
    """A Titan oil lamp on an iron stand: Ring IV's sentry posts are lit by them."""
    s = Struct("lamp_stand", "A Titan oil lamp on its stand", 1, 2, walk=["X", "X"],
               notes="A tall iron lamp-stand with a bronze oil lamp burning on it (its flame "
                     "animated): the Titans' light in Ring IV, beside each sentry post (a lamp "
                     "marks every mandatory trainer in a dark ring). `lamp_stand_odd` on the "
                     "odd parity.")
    R.lay(s)
    M = s.M
    blit(M, ["....k1k.....",
             "...k1Ii1k...",
             ".....i......",
             ".....I......",
             ".....i......",
             ".....I......",
             ".....i......",
             ".....I......",
             ".....i......",
             ".....I......",
             ".....i......",
             ".....I......",
             "....kIk.....",
             "...kIiik....",
             "..kIk.kik...",
             ".kIk...kik..",
             "kkk.....kkk."], FI, 2, 14)
    # the lamp's bowl and flame (top cell)
    blit(M, ["..kkkkkk...", ".k333221k..", "kk2222111kk", ".kkkkkkkk.."], FI, 2, 10)
    frames = A.anim_layer(s, "flame", 3)
    lit = [["....c....", "...cyc...", "...cwc...", "..cywyc..", "..cywyc..", "...ccc..."],
           ["...c.....", "...cc....", "..cyyc...", "..cywyc..", "..cywyc..", "...ccc..."],
           [".....c...", "....cc...", "...cyyc..", "..cywyc..", "..cywyc..", "...ccc..."]]
    blit(M, lit[0], FI, 3, 4)
    for i, f in enumerate(frames, 1):
        blit(f, lit[i], FI, 3, 4)
    s.names = {"top": (0, 0), "base": (0, 1)}
    return R.twins(s)


def grates():
    """Bronze grates: over a shaft in the floor, and a vent in a wall."""
    s = Struct("grates", "Bronze grates: in the floor and in a wall", 3, 1, walk=["XXX"],
               notes="(0) `floor`: a bronze grate over a shaft in the floor, the forge's glow "
                     "far below (blocks; it takes no thread); (1) `vent`: a face with a bronze "
                     "vent grille, warm air from the forge; (2) `gallery`: a wall top's north "
                     "rim with a bronze railing along it, for Ring V's grated gallery seen from "
                     "below or a balcony's edge. All block.")
    L, M = s.B, s.M
    # the shaft below: black, a glint of the forge far down (symmetric, so its
    # four tiles are one, flipped)
    for y in range(16):
        for x in range(16):
            L.px(x, y, "ls1" if min(x, y, 15 - x, 15 - y) == 0 else "lk")
    for y in range(16):
        for x in range(16):
            e = min(x, y, 15 - x, 15 - y)
            if e == 1:
                M.px(x, y, "bz3")
            elif e == 2:
                M.px(x, y, "bz1")
            elif e > 2 and (x - 3) % 3 and (y - 3) % 3:
                continue        # a hole: nine of them, the grate symmetric
            elif e > 2:
                M.px(x, y, "bz2" if (x - 3) % 3 == 0 and (y - 3) % 3 == 0 else "bz1")
    R.face(L, 16, 0)
    L.rect(19, 6, 10, 7, "lk")
    for y in range(6, 13):
        for x in range(19, 29):
            if (x - 19) % 2 == 0:
                M.px(x, y, "bz2" if y < 9 else "bz1")
    for x in range(18, 30):
        M.px(x, 5, "bz3")
        M.px(x, 13, "bz1")
    R.top(L, 32, 0, n=True)
    for x in range(32, 48):
        M.px(x, 1, "bz3")
        M.px(x, 2, "bz1")
        if (x - 32) % 4 == 1:
            for y in range(3, 8):
                M.px(x, y, "bz2")
            M.px(x, 8, "bz1")
    s.names = {"floor": (0, 0), "vent": (1, 0), "gallery": (2, 0)}
    return s


# --------------------------------------------------------------------------
# Ring VI: the forge
# --------------------------------------------------------------------------

def forge():
    """Hephaestus's forge, the Titans' now: a great furnace in a north wall, its
    mouth roaring (animated), bellows, coal."""
    s = Struct("forge", "The forge: the furnace in its wall", 3, 3, walk=["XXX", "XXX", "XXX"],
               notes="The forge's furnace (Ring VI, scene G), built into a north wall three "
                     "cells wide and three tall (as a bay of the arcade): a domed brick furnace, "
                     "its mouth full of fire (animated), a hood over it and a chimney into the "
                     "vault, coal heaped at its foot. Blocks; lay floor in front of it.")
    L, M = s.B, s.M
    # the vault and the wall behind, soot-black, in firelight (all fire palette)
    for x in range(48):
        for y, c in enumerate(("ink", "fi0", "fi0", "fi1")):
            L.px(x, y, c)
    for y in range(4, 48):
        for x in range(48):
            L.px(x, y, "fi1" if (y + (x // 8) * 3) % 9 else "fi0")
    # the brick furnace (fire palette clay and iron)
    for y in range(6, 47):
        for x in range(3, 45):
            dx = (x - 23.5) / 21.0
            dome = y > 6 + 14 * (dx * dx) ** 1.2
            if not dome:
                continue
            # brick courses, lit from the west
            c = "fc0" if (y - 6) % 3 == 0 or (x + ((y - 6) // 3) * 3) % 6 == 0 else "fc1"
            if x < 7:
                c = "fc1"
            if x > 40:
                c = "fc0"
            L.px(x, y, c)
    for y in range(6, 47):
        for x in range(3, 45):
            dx = (x - 23.5) / 21.0
            if abs(y - (6 + 14 * (dx * dx) ** 1.2)) < 1.0:
                L.px(x, y, "ink")
    # the hood and chimney
    for y in range(0, 8):
        for x in range(18, 30):
            L.px(x, y, "fi0" if x in (18, 29) else "fi1")
    # the mouth: an arch of fire
    for y in range(22, 42):
        for x in range(11, 37):
            dx = (x - 23.5) / 12.5
            if y >= 22 + 9 * (dx * dx) ** 1.0 and y < 42:
                M.px(x, y, "fe0")
    for y in range(20, 43):
        for x in range(10, 38):
            dx = (x - 23.5) / 13.5
            edge = abs(y - (21 + 9 * dx * dx)) < 1.0 and y < 41
            if edge:
                L.px(x, y, "fi0")
    frames = A.anim_layer(s, "forge", 3)
    for f, fr in [(M, 0)] + [(f, i) for i, f in enumerate(frames, 1)]:
        for y in range(22, 42):
            for x in range(11, 37):
                dx = (x - 23.5) / 12.5
                if y >= 22 + 9 * dx * dx:
                    t = (y - 22) / 19
                    cx = abs(x - 23.5) / 12.5
                    wob = math.sin(x * 1.3 + fr * 2.2) * 0.2 + math.sin(y * 0.9 - fr * 1.7) * 0.1
                    heat = t * 1.2 - cx * 0.5 + wob
                    c = ("ff3" if heat > 0.95 else "ff2" if heat > 0.72 else "ff1" if heat > 0.5
                         else "ff0" if heat > 0.28 else "fe1" if heat > 0.08 else "fe0")
                    f.px(x, y, c)
    # the sill and coal at its foot
    for x in range(8, 40):
        L.px(x, 42, "fi2")
        L.px(x, 43, "fi1")
        for y in (44, 45, 46, 47):
            L.px(x, y, "fi0" if (x + y) % 3 else "ink")
    s.names = {f"{c}{r}": (i, r) for r in range(3) for i, c in enumerate("lmr")}
    return s


def anvil():
    """Hyperion's anvil: a great bronze-age anvil on an oak stump, a bar on it
    glowing from the fire, his hammer against it."""
    s = Struct("anvil", "The forge: Hyperion's anvil", 2, 2, walk=["XX", "XX"],
               notes="Hyperion's anvil (scene G): a great anvil of dark iron on an oak stump, a "
                     "bar glowing orange on its face and his long-handled hammer leaning on it. "
                     "Stand Hyperion north of it. `anvil_odd` on the odd parity.")
    R.lay(s)
    M = s.M
    # everything here is in the fire palette: iron (fi), oak (clay browns), heat
    # the stump, bottom row
    blit(M, ["....kkkkkkkkkkkkkkkkkkk....",
             "...kbbbbbbbbbbbbbbbbbbak...",
             "...kaaaaaaaaaaaaaaaaaaik...",
             "...kaiaiaiaiaiaiaiaiaaik...",
             "...kaaaaaaaaaaaaaaaaaiik...",
             "...kiaiaiaiaiaiaiaiaiiik...",
             "....kkkkkkkkkkkkkkkkkkk...."], FI, 2, 23)
    # the anvil: horn to the west, heel to the east
    blit(M, [".kkkkkkkkkkkkkkkkkkkkkk.....",
             "kJJJJJJJJJJJJJJJJJJJJJJkk...",
             ".kkIIIIIIIIIIIIIIIIIIIIIIk..",
             "...kkkkIIIIIIIIIIIIIIIIk....",
             "......kIiiiiiiiiiiiik.......",
             "......kkIiiiiiiiiiikk.......",
             ".......kIiiiiiiiiik.........",
             "......kIiiiiiiiiiiik........",
             ".....kIIiiiiiiiiiiiik.......",
             ".....kkkkkkkkkkkkkkkk......."], FI, 1, 13)
    # the hot bar on its face
    blit(M, ["kkkkkkkkkkkk", "kcyywwwyyccf", "kfccccccffek", "kkkkkkkkkkkk"], FI, 8, 10)
    # the hammer leaning against the heel, its oak handle
    for i in range(12):
        M.px(28 - i // 3, 4 + i, "fc1")
    blit(M, ["kkkk", "kJJk", "kIIk", "kkkk"], FI, 26, 1)
    s.names = {"tl": (0, 0), "tr": (1, 0), "bl": (0, 1), "br": (1, 1)}
    return R.twins(s)


def forge_kit():
    """The rest of the forge: bellows, quench trough, the molten runnel, slag."""
    s = Struct("forge_kit", "The forge: bellows, tub, runnel, mold, slag", 7, 1,
               walk=["XXXXXXX"],
               notes="(0, 1) `bellows_l`, `bellows_r`: a great leather bellows, its nozzle west "
                     "(the bellows room; lay it against the furnace's flank); (2) `trough`: an "
                     "oak quench tub of black water, steaming; (3) `runnel_h` and (4) "
                     "`runnel_v`: a stone-lipped channel in the floor running with molten "
                     "bronze, east-west and north-south: run it straight from the furnace's "
                     "foot; (6) `mold`: where a north-south runnel ends, the bronze pouring "
                     "into an ingot mold; (5) `slag`: a heap of slag and clinker (the slag "
                     "heap's dead end). All block. `forge_kit_odd` on the odd parity.")
    R.lay(s)
    M = s.M
    # bellows, seen from above: an oak board widening to two handles at the east,
    # leather pleats showing beneath its edge, an iron nozzle to the west
    blit(M, ["....................kkkkkkkkkk..",
             "...........kkkkkkkkkbbbbbbbbbbk.",
             "......kkkkkbbbbbbbbbbbbbbbbbbbbk",
             "kkkkkkJJkbbbbbbbbbbbbbbbbbbbbbbk",
             "kIIIIIJJkbbbbbbbbbbbbkkbbbbbbbbk",
             "kkkkkkJJkbbbbbbbbbbbbkkbbbbbbbak",
             "......kkkkkaaaaaaaaaaaaaaaaaaaak",
             "...........kkEeEeEeEeEeEeEeEeEek",
             "..............kkEeEeEeEeEeEeEek.",
             ".................kkkkkkkkkkkkk.."], {**FI, "a": "fc0", "b": "fc1"}, 0, 3)
    # the handles
    blit(M, ["kk", "ak", "kk", "..", "kk", "ak", "kk"], {**FI, "a": "fc0"}, 30, 2)
    # the quench tub: oak staves bound in iron, black water, a hiss of steam
    blit(M, ["....kkkkkkkk....",
             "..kkbabababakk..",
             ".kbkkkkkkkkkkbk.",
             "kbkiiJJJJiiiikak",
             "kaiJIiiiiIJiiiak",
             "kJkiiiiiiiiiikJk",
             "kaiiiiIIIiiiiiak",
             "kbkiiiiiiiiIikbk",
             ".kakiiiiiiiikak.",
             "..kkbJbbbbJbkk..",
             "....kkkkkkkk...."], {**FI, "a": "fc0", "b": "fc1", "J": "fi2"}, 32, 4)
    for (x, y) in ((38, 1), (39, 2), (41, 0), (40, 3), (42, 2)):
        M.px(x, y, "fi2")
    # the runnels: a stone-lipped channel running with molten bronze
    def runnel(x0, horiz):
        for a in range(16):
            for b in range(4, 12):
                c = {4: "ink", 5: "fi1", 6: "ff1", 7: "ff2", 8: "ff3", 9: "ff1", 10: "fi1",
                     11: "ink"}[b]
                if b in (6, 9) and a % 5 == 2:
                    c = "fe1"           # a crust cooling on it
                M.px(x0 + (a if horiz else b), (b if horiz else a), c)
    runnel(48, True)
    runnel(64, False)
    # slag
    blit(M, ["......kkk.......",
             "....kkIiIkk.....",
             "...kIiiJiiIk....",
             "..kiIiieiIiik...",
             ".kiiJiIiiiJiik..",
             "kIiiiiiEiiiiiik.",
             "kiJiiIiiiJiiiIk.",
             ".kkkkkkkkkkkkk.."], {**FI, "J": "fi2"}, 80, 6)
    # the mold: the runnel comes in from the north and fills a clay ingot mold
    runnel_v_end = 7
    for a in range(runnel_v_end):
        for b in range(4, 12):
            c = {4: "ink", 5: "fi1", 6: "ff1", 7: "ff2", 8: "ff3", 9: "ff1", 10: "fi1",
                 11: "ink"}[b]
            M.px(96 + b, a, c)
    blit(M, ["kkkkkkkkkkkkkkkk",
             "kbbbbbbbbbbbbbbk",
             "kbkkkkkkkkkkkkbk",
             "kbkcyyywwyyyckbk",
             "kbkyywwwwwwyykbk",
             "kbkcyyywwyyyckbk",
             "kbkkkkkkkkkkkkbk",
             "kaaaaaaaaaaaaaak",
             "kkkkkkkkkkkkkkkk"], FI, 96, 6)
    s.names = {"bellows_l": (0, 0), "bellows_r": (1, 0), "trough": (2, 0), "runnel_h": (3, 0),
               "runnel_v": (4, 0), "slag": (5, 0), "mold": (6, 0)}
    return R.twins(s)


# --------------------------------------------------------------------------
# Ring VI: the Hall of Dials
# --------------------------------------------------------------------------

def _dial(M, x0, pos):
    """A bronze wheel with a labrys-shaped socket and a pointer at A or B."""
    for y in range(16):
        for x in range(16):
            d = math.hypot(x - 7.5, y - 8.5)
            if d <= 6.8:
                c = "bz3" if (x - 7.5) + (y - 8.5) < -2 else "bz2"
                if d > 5.9:
                    c = "ink"
                elif d > 4.8:
                    c = "bz1" if int(math.degrees(math.atan2(y - 8.5, x - 7.5)) // 30) % 2 else "bz3"
                M.px(x0 + x, y, c)
    blit(M, ["k...k", "kk.kk", "kkkkk", "kk.kk", "k...k"], BZ, x0 + 6, 6)
    # the pointer
    if pos == "a":
        for i in range(5):
            M.px(x0 + 7, 1 + i, "bz4")
    else:
        for i in range(5):
            M.px(x0 + 13 - i, 8, "bz4")


def dials():
    """Daedalus's dials and the wall segments they swing (LABYRINTH.md §5.5)."""
    s = Struct("dials", "The Hall of Dials: dials, swinging walls, the reset lever", 8, 1,
               walk=["XXXXXXXX"],
               notes="Ring VI's dials (EventScript_IchorDial). (0) `dial_a`, (1) `dial_b`: a "
                     "bronze wheel with a labrys socket on a face, its pointer up (position A) "
                     "or across (B): swap with the wall it turns. The swinging walls are "
                     "bronze-bound stone on a pivot: (2) `pivot`, the post they turn on (always "
                     "there); (3) `face_seg`, a segment seen from the south (a horizontal run, "
                     "blocking a north-south way) and (4) `face_end`, its free end; (5) "
                     "`top_seg`, a segment seen from above (a vertical run, blocking an "
                     "east-west way) and (6) `top_end`, its free end at the south. A segment's "
                     "cells, when it swings away, are ring floor for their parity. (7) `lever`: "
                     "the reset lever by the entrance, on a face. All block.")
    L, M = s.B, s.M
    for i in (0, 1):
        R.face(L, i * 16, 0)
        _dial(M, i * 16, "ab"[i])
    # the pivot: a squat bronze-capped post
    KIT.dark_slab(L, 32, 0, "l")
    blit(M, ["................",
             "....kkkkkkkk....",
             "...k44333322k...",
             "...k43222211k...",
             "...kkkkkkkkkk...",
             "....k333221k....",
             "....k322211k....",
             "....k322211k....",
             "....k322211k....",
             "....k322210k....",
             "...kk322210kk...",
             "..k4332221100k..",
             "..kkkkkkkkkkkk..",
             "................"], BZ, 32, 1)
    # segments: faces bound with bronze straps
    for i, end in ((3, False), (4, True)):
        R.face(L, i * 16, 0, "cont", "open" if end else "cont")
        for y in range(2, 15):
            for x in (2, 9):
                M.px(i * 16 + x, y, "bz2")
                M.px(i * 16 + x + 1, y, "bz1")
        for x in range(16 if not end else 14):
            M.px(i * 16 + x, 2, "bz3")
            M.px(i * 16 + x, 14, "bz1")
    for i, end in ((5, False), (6, True)):
        R.top(L, i * 16, 0, w=True, e=True)
        if end:
            R.face(L, i * 16, 0, "open", "open")
            for y in range(0, 5):
                for d, c in enumerate(KIT.RIM):
                    L.px(i * 16 + d, y, c)
                    L.px(i * 16 + 15 - d, y, c)
        for y in range(0, 16 if not end else 15):
            if y % 7 == 3:
                for x in range(5, 11):
                    M.px(i * 16 + x, y, "bz3" if x < 8 else "bz1")
    # the reset lever on a face
    R.face(L, 112, 0)
    blit(M, ["...kk...", "..k44k..", "...kk...", "...k3k..", "...k2k..", "...k2k..",
             "..kk1kk.", ".k33221k", ".kkkkkkk"], BZ, 116, 2)
    s.names = {"dial_a": (0, 0), "dial_b": (1, 0), "pivot": (2, 0), "face_seg": (3, 0),
               "face_end": (4, 0), "top_seg": (5, 0), "top_end": (6, 0), "lever": (7, 0)}
    return s


# --------------------------------------------------------------------------
# The archive and the vault
# --------------------------------------------------------------------------

def _tablet(M, x, y, seal=False, label=True):
    """A wax tablet on edge: a wooden frame, dark wax, a little label."""
    blit(M, ["kkkk", "k0gk", "k0gk", "k0gk", "kkkk"], {**TM, "g": "tg"}, x, y)
    if label:
        M.px(x + 1, y + 1, "tp2")
    if seal:
        M.px(x + 2, y + 3, "tr")


def archive():
    """Iapetos's archive (scene H): shelves of wax tablets labelled in a neat hand,
    the scraped tablet on its desk."""
    s = Struct("archive", "The archive: shelves of tablets", 3, 3, walk=["XXX"] * 3,
               notes="Iapetos's archive (scene H): a bay of the arcade fitted with pigeonholes, "
                     "each holding wax tablets on edge, each labelled. Lay it between piers as "
                     "`arcade`'s bay. The bottom shelf's middle holds the one tablet sealed shut "
                     "with a blob of wax (put the sealed tablet's bg event on the bay's bottom "
                     "row).")
    L, M = s.B, s.M
    ins = A.arch(L, 0, 48)
    A.recess(L, 0, 48, ins)
    # pigeonholes filling the recess (timber, middle layer over the stone), on
    # the eight-pixel grid so the shelving repeats tile for tile
    for y in range(18, 46):
        for x in range(1, 47):
            if not ins(x, y):
                continue
            if (y - 18) % 8 == 0 or y == 45 or x % 8 == 0:
                c = "tw2" if y != 45 else "tw1"
            elif (y - 18) % 8 == 1 or x % 8 == 1:
                c = "tw1"
            else:
                c = "tw0"
            M.px(x, y, c)
    for ty in (19, 27, 35):
        for hole in range(6):
            _tablet(M, hole * 8 + 2, ty + 2)
    # on the bottom shelf, the one tablet sealed shut with a blob of wax
    M.px(18 + 2, 37 + 3, "tr")
    M.px(18 + 3, 37 + 3, "tr")
    s.names = {f"{c}{r}": (i, r) for r in range(3) for i, c in enumerate("lmr")}
    t = Struct("archive_desk", "The archive: the desk and the scraped tablet", 2, 2,
               walk=["XX", "XX"],
               notes="A scribe's desk with the tablet that lies by itself, scraped and rewritten "
                     "many times (Kleon's prophecy, scene H): put its bg event on the desk. A "
                     "stylus, a lamp, the hook-mark of Iapetos's signature. `archive_desk_odd` "
                     "on the odd parity.")
    t.floor_cells = [(0, 1), (1, 1)]
    R.lay(t)
    for y in range(0, 20):
        for x in range(0, 32):
            if y < 16:
                c = "ink" if x in (0, 31) else "tw3" if y < 2 else "tw2" if (y - 2) % 5 else "tw1"
                t.B.px(x, y, c)
            else:
                c = "ink" if y == 19 or x in (0, 31) else "tw1"
                t.M.px(x, y, c)
    for lx in (3, 27):
        for y in range(20, 30):
            t.M.px(lx, y, "tw1")
            t.M.px(lx + 1, y, "tw0")
    for x in range(3, 29):
        t.M.px(x, 20, "ink")
        t.M.px(x, 21, "tw1")
    # the tablet, open on the desk, scored through
    blit(t.M, ["kkkkkkkkkkk", "k0g0g0g0g0k", "kgkkkkk0g0k", "k0g0g0gkkgk", "kgkkk0g0g0k",
               "kkkkkkkkkkk"], {**TM, "g": "tg"}, 6, 9)
    blit(t.M, ["k", "x", "x"], TM, 20, 9)
    blit(t.M, [".kk.", "k21k", "kkkk"], {**TM, "2": "tw3", "1": "tw2"}, 23, 11)
    t.names = {"tl": (0, 0), "tr": (1, 0), "bl": (0, 1), "br": (1, 1)}
    return [s, *R.twins(t)]


def vault():
    """The vault: copper oxhide ingots, a bronze-bound chest, gold."""
    s = Struct("vault", "The vault: chests, ingots, gold", 4, 1, walk=["XXXX"],
               notes="The vault's treasure (Ring VI): (0, 1) `chest_l`, `chest_r`: a cedar "
                     "chest bound in bronze, two cells; (2) `ingots`: a stack of copper oxhide "
                     "ingots; (3) `gold`: gold cups and staters heaped in a basket. All block; put "
                     "the items on the floor in front. `vault_odd` on the odd parity.")
    R.lay(s)
    M = s.M
    for y in range(3, 15):
        for x in range(1, 31):
            if y in (3, 14) or x in (1, 30):
                c = "ink"
            elif y < 7:
                c = "tw3" if y == 4 else "tw2"
            elif y == 7:
                c = "ink"
            else:
                c = "tw1" if (y - 8) % 3 else "tw0"
            M.px(x, y, c)
    for bx in (5, 15, 25):
        for y in range(4, 14):
            M.px(bx, y, "tx")
    M.px(15, 9, "ink")
    M.px(16, 9, "tx")
    # oxhide ingots: copper cast like a stretched hide, stacked
    hide = ["kk.......kk",
            "kokkkkkkkok",
            ".kocooooock.",
            ".kooooooook.",
            "kokkkkkkkok",
            "kk.......kk"]
    for k, (hx, hy) in enumerate(((35, 9), (36, 6), (35, 3))):
        blit(M, hide, {"k": "ink", "o": "fc0", "c": "fc1"}, hx, hy)
    # gold in a basket
    blit(M, ["....kk.kk.....",
             "...k44k44kk...",
             "..k4ee44e44k..",
             ".k4e44e44e44k.",
             "kkkkkkkkkkkkkk",
             "k3232323232321",
             ".k1212121212k.",
             "..kkkkkkkkkk.."], BZ, 49, 6)
    s.names = {"chest_l": (0, 0), "chest_r": (1, 0), "ingots": (2, 0), "gold": (3, 0)}
    return R.twins(s)


# --------------------------------------------------------------------------
# The Mistress's shrine (the heal below Ring VI)
# --------------------------------------------------------------------------

def shrine():
    """The Mistress's shrine on the landing below Ring VI: a gypsum altar with
    horns of consecration, a faience snake goddess, honey in a jar."""
    s = Struct("shrine", "The Mistress's shrine", 2, 2, walk=["XX", "XX"],
               notes="The second heal (LABYRINTH.md §6, Ring VI): a gypsum altar, horns of "
                     "consecration on it, between them a little faience goddess holding up two "
                     "snakes, a honey jar and a lamp before her. The priestess stands beside "
                     "it; put the heal's bg event on its bottom row. `shrine_odd` on the odd "
                     "parity.")
    R.lay(s)
    M = s.M
    # the altar (gypsum block with a red band)
    for y in range(12, 30):
        for x in range(3, 29):
            if y in (12, 29) or x in (3, 28):
                c = "ink"
            elif y < 16:
                c = "mg2" if y == 13 else "mg1"
            elif y in (19, 20):
                c = "mr1"
            else:
                c = "mg1" if x > 5 else "mg2"
            M.px(x, y, c)
    for x in range(6, 26, 4):
        M.px(x, 19, "mo1")
        M.px(x + 1, 20, "mo1")
    # horns of consecration on it
    blit(M, ["kk..........kk",
             "kWk........kWk",
             "kWGk......kGWk",
             ".kWGk....kGWk.",
             "..kWWkkkkWWk..",
             "...kGGGGGGk...",
             "...kkkkkkkk..."], MN, 9, 6)
    # the goddess between them (faience: white, black, ochre)
    blit(M, ["..k.k..", ".kOkOk.", "kO.k.Ok", "..kOk..", ".kbbbk.", "kbOObbk", "kkkkkkk"],
         MN, 12, 4)
    s.names = {"tl": (0, 0), "tr": (1, 0), "bl": (0, 1), "br": (1, 1)}
    return R.twins(s)


# --------------------------------------------------------------------------
# Frescoes and doorways (as in labyrinth)
# --------------------------------------------------------------------------

def frescoes():
    out = [R.fresco_bay("fresco_iv", "Fresco: the dance's steps 1-3 (Ring IV)", "XWL",
                        "Ring IV's fresco alcove (LABYRINTH.md §5.7): dancers holding up the "
                        "dance's steps 1-3, double axe, wave, lily, in a bay of the arcade.",
                        section="titans"),
           R.fresco_bay("fresco_vi", "Fresco: the dance's steps 7-9 (Ring VI)", "RWS",
                        "Ring VI's fresco corridor (LABYRINTH.md §5.7): the dance's steps 7-9, "
                        "rosette, wave, star.", section="titans")]
    return out


def build():
    out = []
    out.append(forge())
    out += archive()
    out += frescoes()
    out += bunk()
    out += mess_table()
    out += helmet_rack()
    out += weapon_rack()
    out += anvil()
    out += shrine()
    out += titan_lamp()
    out += forge_kit()
    out += vault()
    out.append(dials())
    out.append(banners())
    out.append(grates())
    out += R.doorways(gates=False)
    return A.order_for_packing(out)
