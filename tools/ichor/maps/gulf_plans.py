"""The Gulf maps' plans, one character per cell (tools/ichor/maps/gulf.py
reads them; the characters are explained there and in kithairon.py).

Rows are built from runs so the columns stay honest; a comment gives the
landmarks on each row. Pieces placed on 'k' and 'h' cells are named in
gulf.py's props_* functions.
"""

# ---------------------------------------------------------------------------
# Route 9, the Schiste (32x58). North: Lebadeia (x 10-13). South: Kirrha (x 14-17).
# ---------------------------------------------------------------------------
ROUTE9 = [
    # 0         1         2         3
    # 01234567890123456789012345678901
    "##########pppp##################",  # 0  Lebadeia's road comes down
    "#########.pppp.#################",  # 1
    "########..pppp..################",  # 2
    "#######..,pppp,..###############",  # 3
    "#######.,,..pp,k.###############",  # 4  the north sign (15,4)
    "######^.,,..pp.,..^#############",  # 5
    "#####^^^,,..pp.,...^bbbbbbbbbbbb",  # 6  the Korykian crag
    "####^^^^.,..pp.,,...uuuuuuuuuuuu",  # 7  the cave mouth (29,7)/(29,8)
    "###^^^^^.,..pp.,,...ffffffffffff",  # 8
    "##^^.k^^^...pp.,,,,,,...,,,..pp^",  # 9  the Daulis milestone (5,9)
    "#^^..^^^^..ppppppppppppppppppp.^",  # 10 the goat path east
    "#^.,.p.pppppppp..,,,.....,,,,.^^",  # 11 the Daulis road west: the thicket (5,11)
    "#^.,.^^^^^^.pp.^^,,,,..,,,,,,.^^",  # 12
    "#^^..^^^^^^.pp.kkk.,,,,,,,,..^^#",  # 13 Laius's tomb (15..17,13..14)
    "##^^^^#####.pp.kkkk^^^^^^^^^^###",  # 14 its stele (18,14)
    "###########^pp^^################",  # 15
    "###########^pp.#################",  # 16 Polyon's niche (14,16)
    "##########^,,,^#################",  # 17 band 1
    "##########^,,,^#################",  # 18
    "##########^,,,^#################",  # 19
    "b" * 12 + "pp" + "b" * 18,           # 20 tier 1's brink: the cut stair (12-13)
    "u" * 12 + "ss" + "u" * 18,           # 21
    "f" * 12 + "pp" + "f" * 18,           # 22
    "##^" + "p" * 11 + ".." + "," * 10 + "....." + "#",            # 23 tier 2
    "#^.pp,,..^^^^^.,,,,.kk..k...kk.#",                            # 24 the camp: tents (20,24) (28,24), fire (24,24)
    "#^^pp.^^^^####^.,,..kk......kk.#",                            # 25
    "#^^pp.^#######^..,..,,~~....,,.#",                            # 26 the spring (22-23, 26-27)
    "#^^pp.^#######^^,,,.,,~~..,,,^^#",                            # 27 Mnason's niche (5,27)
    "#^,,,^^" + "#" * 8 + "^^,,,." + ",,,," + "^" * 6 + "#",       # 28 band 2
    "#^,,,^" + "#" * 11 + "^" * 7 + "." + "......" + "#",          # 29 the scree gate (24,29)
    "#^,,,^" + "#" * 12 + "^" * 7 + "......" + "#",                # 30 the scree pocket
    "#^.pp^" + "#" * 13 + "^" * 6 + "..,,.." + "#",                # 31
    "bbbppbbbbbbbbbbbbbbbbbbbbbbbbbbb",                            # 32 tier 2's brink: the stair (3-4)
    "uuussuuuuuuuuuuuuuuuuuuuuuuuuuuu",                            # 33 (ivy face x 20-25: the climbing relic)
    "fffppfffffffffffffffffffffffffff",                            # 34
    "^.," + "p" * 15 + ",,,," + "p" * 7 + "..^",                   # 35 tier 3: the long traverse
    "^.," + "p" * 15 + ",,,," + "p" * 7 + ".k^",                   # 36 the Delphoi sign (30,36)
    "^^.^^^^^^^^^^^^.^^^^^^^^^^pp^..^",                            # 37 Akeson's niche (15,37); the ravine's mouth (2,37)
    "^.,^#####^^^^^^^^^^^#####^pp^..^",                            # 38 the ravine (1-2, 38-40); Theano (29,38)
    "^,.^######^^^^^^^^^^^####^pp^^.^",                            # 39 the lookout's goat track (30, 39-41)
    "^.,^#######^^^^^^^^^^####,,,,^,^",                            # 40 band 3
    "^^^^" + "#" * 21 + ",,,," + "^.^",                            # 41
    "b" * 26 + "pp" + "b" * 4,                                     # 42 tier 3's brink: the stair (26-27)
    "u" * 26 + "ss" + "u" * 4,                                     # 43
    "f" * 26 + "pp" + "f" * 4,                                     # 44
    "o" * 12 + ".,,,,,,,,." + ",,,," + "pp" + ".." + "oo",      # 45 the olive sea
    "o" * 12 + ".,,,,,,,.." + ",," + "pppp" + ".." + "oo",        # 46
    "o" * 12 + ",,,,,," + ".." + "pppppp" + ",," + ".." + "oo",   # 47
    "o" * 12 + ",,,,,," + "." + "pppp" + "." + ",,," + "..." + "oo",  # 48
    "o" * 12 + ".,,," + "pppppp" + ",,," + "." + "o" * 6,         # 49
    "o" * 12 + ".." + "pppp" + ".." + "o" * 12,                   # 50
    "o" * 14 + "pp" + "." + "o" * 15,                             # 51 Eryx's niche (16,51)
    "o" * 13 + ",,,," + "o" * 15,                                 # 52 band 4
    "o" * 13 + ",,,," + "o" * 15,                                 # 53
    "o" * 13 + ",pp," + "o" * 15,                                 # 54
    "o" * 12 + ".." + "pppp" + "." + "k" + "o" * 12,             # 55 the south sign (19,55)
    "o" * 12 + ".." + "pppp" + ".." + "o" * 12,                   # 56
    "o" * 14 + "pppp" + "o" * 14,                                 # 57 Kirrha's road
]

# ---------------------------------------------------------------------------
# Kirrha (28x32). North: Route 9 (x 14-17). The ferry's quay south.
# ---------------------------------------------------------------------------
KIRRHA = [
    "^" * 10 + "oooo" + "pppp" + "o" * 10,                        # 0  from the olive sea
    "^bbbWWbbbb" + "oo.." + "pppp" + "..oooooooo",                # 1  the Kastalian falls (4-5, 1-3)
    "^uuuWWuuus" + "...." + "pppp" + "...ooooooo",                # 2  the Sacred Way's stair, washed out (9, 2-3)
    "^lllWWllls" + "...." + "pppp" + "...ooooooo",                # 3
    "^d~~~~~~d." + "kk.." + "pppp" + "....oooooo",                # 4  the falls' pool; the pilgrims' tents (10,4)
    "^d~~~~~~d." + "kk.k" + "pppp" + ".hhhhh.ooo",                # 5  their fire (13,5); the hostel (19..23, 5..8)
    "^.dddddd.." + "...." + "pppp" + ".hhhhh.ooo",                # 6
    "^^......k." + "...." + "pppp" + ".hhhhh..oo",                # 7  the Sacred Way's stele (8,7)
    "^^........" + "...." + "pppp" + ".hhhhh..oo",                # 8  the hostel's door (21,8)
    "^^....pppp" + "pppp" + "pppp" + "pppppp..oo",                # 9  the plaza
    "^^oo.ppppp" + "pppp" + "pppp" + "ppppppp.oo",                # 10 a few olives west of the plaza
    "^^oo.ppp.." + ".k.." + "pppp" + "...kkk.^^^",                # 11 the herm (11,11); Apollo's shrine (21..23, 11..13)
    "^^oooopp.." + "...." + "pppp" + "...kkk.^^^",                # 12
    "^^oooopp.." + ".k.." + "pppp" + "...kkk..^^",                # 13 the merchant's jars (11,13)
    "^^....pp.." + "...." + "pppp" + "....k...^^",                # 14 the dolphin altar (22, 14..15)
    "^^....pp.." + "...." + "pppp" + "....k..bbb",                # 15 the headland
    "^ddddddddd" + "dddd" + "dqqd" + "ddddddd" + "uuu",           # 16 the beach; the quay (15-16)
    "^ddddddddd" + "dddd" + "dqqd" + "ddddddd" + "FFF",           # 17
    "^~~ddddddd" + "dddd" + "dqqd" + "dddd~~~" + "~~~",           # 18
    "^~~~~ddddd" + "dddd" + "~qq~" + "~~~~~~~" + "~~~",           # 19
    "^" + "~" * 14 + "qq" + "~" * 11,                              # 20
    "^" + "~" * 14 + "qq" + "~" * 11,                              # 21
    "^" + "~" * 14 + "qq" + "~" * 11,                              # 22
    "^~~dd" + "~" * 10 + "qq" + "~" * 11,                          # 23 the islet (3-4, 23-24): the Conch
    "^~~dd" + "~" * 10 + "qq" + "~" * 11,                          # 24
    "^" + "~" * 14 + "qq" + "~" * 11,                              # 25
    "^" + "~" * 14 + "qq" + "~" * 11,                              # 26
    "^" + "~" * 14 + "qq" + "~" * 11,                              # 27 the captain (15,27)
    "^" + "~" * 27,                                               # 28
    "^" + "~" * 27,                                               # 29
    "^" + "~" * 27,                                               # 30
    "^" + "~" * 27,                                               # 31
]

# ---------------------------------------------------------------------------
# Aigion (28x32). The ferry's quay north. South: Route 11 (x 13-16).
# ---------------------------------------------------------------------------
AIGION = [
    "~" * 28,                                                     # 0
    "~" * 28,                                                     # 1
    "~" * 28,                                                     # 2
    "~~~k~~~~~~" + "~" * 18,                                      # 3  Helike's drowned columns (3,3) (6,4) (1,6) (8,6)
    "~~~~~~k~~~" + "~" * 5 + "qq" + "~" * 11,                     # 4  the quay (15-16, 4-12); the captain (15,4)
    "~~~ddd~~~~" + "~" * 5 + "qq" + "~" * 11,                     # 5  the islet (3-5, 5-6): the Conch
    "~k~ddd~~k~" + "~" * 5 + "qq" + "~" * 11,                     # 6
    "~" * 15 + "qq" + "~" * 11,                                   # 7
    "~" * 15 + "qq" + "~" * 11,                                   # 8
    "~" * 15 + "qq" + "~" * 11,                                   # 9
    "^ddd~~~~~~" + "~~~~d" + "qq" + "d~~~~~~~~~~",                # 10 the beach
    "^ddddddd~~" + "ddddd" + "qq" + "dddd~~~~~~~",                # 11
    "^ddddddddd" + "ddddd" + "qq" + "ddddddd~~~~",                # 12
    "^ddddddddd" + "ddd" + "pppp" + "ddddddddd^~",                # 13
    "^kk.k.kk.." + "..." + "pppp" + "..........^",                # 14 the fishers' camp: tents (1,14) (6,14), fire (4,14)
    "^kk...kk.." + "..." + "pppp" + "....k.k...^",                # 15 the merchant's jars (21,15), a herm (23,15)
    "^...k....." + "..." + "pppp" + "..........^",                # 16 baskets (2,16), firewood (4,16)
    "#oooooo##." + "..." + "pppp" + "..ooooooooo",                # 17
    "##.hhhhhh#" + "..." + "pppp" + "..ooooooooo",                # 18 the Homarion (3..8, 18..22)
    "##.hhhhhh#" + "..." + "pppp" + "..ooooooooo",                # 19
    "##.hhhhhh#" + "..." + "pppp" + "..ooooooooo",                # 20
    "##.hhhhhh#" + "..." + "pppp" + "..ooooooooo",                # 21
    "##.hhhhhh#" + "..." + "pppp" + "...oooooooo",                # 22 its door (6,22)
    "##....p.k#" + "..." + "pppp" + "...oooooooo",                # 23 the oath altar (8, 23..24)
    "##....p.k#" + "..." + "pppp" + ".k.oooooooo",                # 24 the Zeus oak (18,24)
    "#wwwwwswww" + "..." + "pppp" + "...oooooooo",                # 25 the terrace wall; its steps (6,25)
    "#....ppppp" + "ppp" + "pppp" + "..........#",                # 26
    "#....ppppp" + "ppp" + "pppp" + "..........#",                # 27
    "oooooooo.." + "..." + "pppp" + "...oooooooo",                # 28
    "oooooooo.." + "..." + "pppp" + "...oooooooo",                # 29 the south sign (11,29)? see props
    "oooooooooo" + "o.." + "pppp" + "..ooooooooo",                # 30
    "oooooooooo" + "ooo" + "pppp" + "ooooooooooo",                # 31 Route 11's road
]

# ---------------------------------------------------------------------------
# Route 11, the drum pass (30x52). North: Aigion (x 13-16). South: Styx Falls (x 11-12).
# ---------------------------------------------------------------------------
_W = "^" * 12
ROUTE11 = [
    "o" * 13 + "pppp" + "o" * 13,                                 # 0  Aigion's road
    "o" * 12 + "," + "pppp" + "," + "o" * 12,                     # 1
    "o" * 10 + ",,," + "pppp" + ",,," + "o" * 10,                 # 2
    "o" * 10 + ",,," + "pppp" + ",k," + "o" * 10,                 # 3  the north sign (18,3)
    "##########" + ",,," + ",pp," + ",,," + "##########",         # 4
    "^^" + ",,,,,," + "^^" + "^^^" + ".pp." + "..^" + "^" * 10,   # 5  the pool above the falls (2-7, 5-8)
    "^^" + ",,~~,," + "^^" + "^^^" + "^pp." + "^^^" + "^" * 10,   # 6  Dorys (16,6)
    "^^" + "..~~.." + "^^" + "^^^" + ",,,," + "^^^" + "#" * 10,   # 7  band 1
    "^^" + "..~~.," + "^^" + "^^^" + ",,,," + "^^^" + "#" * 10,   # 8
    "bb" + "bb" + "WW" + "b" * 8 + "pp" + "b" * 14,               # 9  the gorge's lip; the falls (4-5); the stair (14-15)
    "uu" + "uu" + "WW" + "u" * 8 + "ss" + "u" * 14,               # 10
    "ff" + "ff" + "WW" + "f" * 8 + "pp" + "f" * 14,               # 11
    "^^" + "~~~~~~" + ".,,,,," + "pp" + "^^^^" + "^" * 10,        # 12 the falls' pool
    "^^" + "~~~~~~" + ",,,,,," + "pp" + ".^^^" + "^" * 10,        # 13
    "^^^" + "~~~~" + ".," + "pppppp" + "," + "^^^" + "^" * 11,    # 14 the Selinous
    "^^^" + "~~~~" + ".," + "pp" + ",,.," + "^^^" + _W,           # 15
    "^,," + "~~~~" + ".." + "pp" + ".^^^" + "^^^" + _W,           # 16 Thraseas (11,16)
    "^.." + "qqqq" + "pp" + "pp" + ",,,," + "^^^" + _W,           # 17 the ford to the west bank
    "^.," + "~~~~" + ".." + "pp" + ",,.." + "kkk" + _W,           # 18 the nymphs' niches (15..17, 18..20)
    "^,," + "~~~~" + ".." + "pp" + ",,.." + "kkk" + _W,           # 19
    "^,," + "~~~~" + ".." + "pp" + ",,,." + "kkk" + _W,           # 20 Xanthe (2,20)
    "^,," + "~~~~" + ".," + "pp" + ".,,," + "^^^" + _W,           # 21 Lachon (11,21)
    "^,," + "~~~~" + ",,,," + "^^^^" + "^^^" + _W,                # 22 band 2
    "^,," + "~~~~" + ",,,," + "^^^^" + "^^^" + _W,                # 23
    "^,." + "~~~~" + ",,,," + "^^^^" + "^^^" + _W,                # 24
    "^^^" + "~~~~" + ".." + "pp" + ",,,," + "^.." + _W,           # 25 the rubble pocket (16-17, 25-27)
    "^^~" + "~~~~" + ".." + "pp" + "...." + "..." + _W,           # 26 its gate (15,26)
    "^~~" + "~~~~" + ".." + "pp" + ",,,," + "^,," + _W,           # 27
    "^~~" + "~dd~" + "~." + "pp" + ",,,," + "^^^" + _W,           # 28 the islet (4-5, 28-29): the Conch
    "^~~" + "~dd~" + "~." + "pp" + ",,,," + "^^^" + _W,           # 29
    "^~~" + "~~~~" + "~." + "pp" + ",,,," + "^^^" + _W,           # 30
    "^^^" + "^^~~" + "^." + "pp" + ",,,," + "^^^" + _W,           # 31
    "b" * 9 + "pp" + "b" * 19,                                    # 32 the pass's brink: the stair (9-10)
    "u" * 9 + "ss" + "u" * 19,                                    # 33 (ivy face x 20-24: the climbing relic)
    "f" * 9 + "pp" + "f" * 19,                                    # 34
    "^^^" + "^^" + ",,,," + "pppp" + "..^^" + "^^^^^" + "^" * 8,  # 35 Myrine (14,35)
    "^^^" + "^^" + "^^^^" + "^^^" + "p" + "^^^^" + "^^^^^" + "^" * 8,  # 36 the cutting
    "^^^" + "^^" + "^^^^" + "^^^" + "p" + "^^^^" + "^^^^^" + "^" * 8,  # 37 the column drum (12,37)
    "^^^" + "^^" + "^^^^" + "^^^" + "p" + "^^^^" + "^^^^^" + "^" * 8,  # 38
    "^" * 10 + ".,p,." + "^" * 15,                                # 39 out of the cutting: the drum rolls clear
    "^" * 9 + ",..p..," + "^" * 14,                               # 40
    "^" * 8 + ",,..p..,," + "^" * 13,                             # 41
    "^^^^" + "^^" + ",,,," + "..p..." + ",,^^" + "^" * 10,        # 42 the fallen temple's floor
    "^^^^" + "^," + ",,,," + "..p..." + ",,^^" + "^" * 10,        # 43
    "^^^^" + "^^" + ",,,," + ".pp..." + ",,^^" + "^" * 10,        # 44
    "^^^^" + "^^" + "^^^^^" + "pp" + ".." + "^^^" + "^" * 12,     # 45 Pheron (14,45)
    "#" * 8 + ",,,,,,,," + "#" * 14,                              # 46 band 3 (aethos only from here)
    "#" * 8 + ",,,,,,,," + "#" * 14,                              # 47
    "#" * 9 + ",,,,,," + "#" * 15,                                # 48
    "#" * 10 + ".pp.k" + "#" * 15,                                # 49 the south sign (14,49)
    "#" * 10 + ".pp." + "#" * 16,                                 # 50
    "#" * 11 + "pp" + "#" * 17,                                   # 51 Styx Falls's road
]

# ---------------------------------------------------------------------------
# The Korykian Cave (34x26): cave_dark kit characters. '#' rock, '.' floor,
# ',' daylight at the mouth, '~' still water.
# ---------------------------------------------------------------------------
CAVE = [
    "#" * 34,                                                     # 0
    "#" * 14 + "." * 5 + "#" * 15,                                # 1  the nymphs' inner grotto (14-18, 1-3)
    "#" * 13 + "." * 7 + "#" * 14,                                # 2
    "#" * 14 + "." * 5 + "#" * 15,                                # 3
    "#" * 17 + "." + "#" * 16,                                    # 4  the thornweb (17, 4-5)
    "#" * 17 + "." + "#" * 16,                                    # 5
    "#" * 10 + "." * 13 + "#" + "." * 2 + "#" * 8,                # 6  the great hall
    "#" * 8 + "." * 19 + "." + "#" * 6,                           # 7
    "#" * 3 + "~" * 5 + "." * 20 + "#" * 6,                       # 8  the pool (2-8, 8-14)
    "#" * 2 + "~" * 7 + "." * 19 + "#" * 6,                       # 9
    "#" * 2 + "~~..~~~" + "." * 19 + "#" * 6,                     # 10 its islet (4-5, 10-11): the Conch
    "#" * 2 + "~~..~~~" + "." * 19 + "#" * 6,                     # 11
    "#" * 2 + "~" * 7 + "." * 24 + "#",                           # 12 the drum's passage east (28-32)
    "#" * 3 + "~" * 5 + "." * 20 + "#" * 3 + "." + "#" * 2,       # 13
    "#" * 4 + "~" * 3 + "." * 20 + "#" * 4 + "." + "#" * 2,       # 14
    "#" * 5 + "." * 21 + "#" * 5 + "." + "#" * 2,                 # 15
    "#" * 5 + "." * 21 + "#" * 5 + "." + "#" * 2,                 # 16 the cobweb (5, 16-17)
    "#" * 5 + "." + "#" * 2 + "." * 16 + "#" * 6 + ".." + "#" * 2,  # 17
    "#" * 2 + "." * 4 + "#" * 2 + "." * 14 + "#" * 4 + "." * 6 + "#" * 2,  # 18 the side chamber; the east grotto
    "#" * 2 + "." * 4 + "#" * 3 + "." * 12 + "." + "#" * 3 + "." * 7 + "#" * 2,  # 19
    "#" * 2 + "." * 4 + "#" * 4 + "." * 10 + "#" * 4 + "." * 8 + "#" * 2,  # 20
    "#" * 3 + "." * 3 + "#" * 6 + "," * 6 + "#" * 6 + "." * 7 + "#" * 3,   # 21 daylight from the mouth
    "#" * 13 + "," * 4 + "#" * 17,                                # 22
    "#" * 14 + "," * 3 + "#" * 17,                                # 23
    "#" * 15 + "," * 2 + "#" * 17,                                # 24
    "#" * 15 + "," * 2 + "#" * 17,                                # 25 the mouth (15-16, 25)
]


def _shift_band(rows, y0, x0, x1, dy, fill):
    """Step a 3-row cliff band (rows y0..y0+2) by dy rows over columns x0..x1,
    so a long cliff breaks into two runs with a step between (STYLE.md 4.2).
    The row it leaves becomes `fill`."""
    rows = [list(r) for r in rows]
    band = [rows[y0 + j][x0:x1 + 1] for j in range(3)]
    for j in range(3):
        rows[y0 + j][x0:x1 + 1] = fill * (x1 - x0 + 1)
    for j in range(3):
        rows[y0 + dy + j][x0:x1 + 1] = band[j]
    return ["".join(r) for r in rows]


ROUTE9 = _shift_band(ROUTE9, 20, 20, 31, 1, "#")     # tier 1's cliff steps down east of the stair
ROUTE9 = _shift_band(ROUTE9, 32, 12, 31, -1, "^")    # tier 2's steps up east of the traverse's start
ROUTE9 = _shift_band(ROUTE9, 42, 0, 12, -1, "#")     # tier 3's steps up west of the olive sea


def _put(rows, cells):
    rows = [list(r) for r in rows]
    for (x, y), ch in cells.items():
        rows[y][x] = ch
    return ["".join(r) for r in rows]


# The lookout's goat track: down the brink by a ledge (one way, into the olive sea)
ROUTE9 = _put(ROUTE9, {(30, 42): "v", (30, 43): ".", (30, 44): ".", (30, 45): ".", (31, 45): "."})
