"""Pixel art for the civic tileset: the Asclepeion, the Agora and the Akademia.

Every piece is drawn by hand below as a character grid, one character per
pixel. LEGEND maps each character to a color; '.' is transparent. Pieces are
whole objects (a column, a basin, a shelf) at their real size in pixels, always
a multiple of 16 wide and tall; civic_tiles.py cuts them into 16x16 metatile
layers.

Light comes from the top left. Objects carry a 1 px dark outline; floors and
walls do not. Colors stay in the families of the master palette in
design/phase1/PLAN.md, but no value repeats a color the aethos primary uses:
Porytiles compiles civic against aethos and would otherwise park civic tiles in
aethos palettes, which break on any other primary.
"""

# --- Legend ----------------------------------------------------------------

LEGEND = {
    "#": (40, 24, 24),     # black-figure ink
    # marble and stone, dark to light
    "1": (72, 64, 64),
    "2": (112, 104, 96),
    "3": (152, 144, 136),
    "4": (184, 176, 160),
    "5": (208, 200, 184),
    "6": (224, 224, 208),
    "7": (240, 240, 232),
    "8": (248, 248, 248),
    # Aegean blue
    "N": (24, 40, 88),
    "B": (24, 48, 112),
    "b": (48, 96, 168),
    "c": (104, 160, 216),
    "C": (168, 208, 240),
    "F": (208, 232, 248),
    # bronze and gold
    "z": (72, 40, 16),
    "Z": (128, 80, 24),
    "x": (176, 112, 32),
    "G": (208, 152, 48),
    "g": (240, 200, 80),
    "h": (248, 232, 152),
    # terracotta
    "R": (88, 32, 16),
    "T": (128, 48, 24),
    "t": (176, 80, 40),
    "u": (216, 128, 80),
    "U": (240, 176, 128),
    "r": (216, 56, 40),
    # wood
    "D": (56, 40, 32),
    "d": (96, 64, 40),
    "w": (136, 96, 56),
    "W": (176, 128, 80),
    "v": (208, 168, 112),
    # limestone and parchment
    "p": (184, 152, 104),
    "L": (208, 184, 136),
    "P": (232, 216, 168),
    "Q": (248, 240, 208),
    # greens: cypress, olive, laurel, grass
    "e": (16, 40, 24),
    "E": (24, 64, 40),
    "y": (40, 88, 48),
    "Y": (64, 80, 32),
    "o": (96, 120, 48),
    "O": (144, 168, 72),
    "i": (184, 200, 112),
    "I": (216, 224, 152),
    # bark
    "k": (72, 56, 40),
    "K": (112, 88, 64),
    "j": (152, 128, 96),
    # dyes
    "m": (72, 32, 80),
    "M": (120, 64, 136),
    "n": (176, 120, 184),
    "a": (128, 32, 32),
    "A": (184, 56, 48),
    # flame
    "X": (240, 128, 40),
    "V": (248, 216, 96),
}

ART = {}


def art(name, rows):
    """Registers a piece. Rows must all be the same width, multiples of 16."""
    w = len(rows[0])
    for i, r in enumerate(rows):
        if len(r) != w:
            raise ValueError(f"{name}: row {i} is {len(r)} wide, expected {w}: {r!r}")
        for ch in r:
            if ch != "." and ch not in LEGEND:
                raise ValueError(f"{name}: row {i} has unknown char {ch!r}")
    if w % 16 or len(rows) % 16:
        raise ValueError(f"{name}: {w}x{len(rows)} is not a multiple of 16")
    ART[name] = rows
    return rows


def rep(motif, width):
    """Repeats a hand-drawn motif row out to a width."""
    return (motif * (width // len(motif) + 1))[:width]


def paste(rows, piece, x, y, remap=None):
    """Lays a small hand-drawn piece over rows at (x, y); '.' stays clear."""
    out = [list(r) for r in rows]
    for j, line in enumerate(piece):
        for i, ch in enumerate(line):
            if ch != ".":
                out[y + j][x + i] = (remap or {}).get(ch, ch)
    return ["".join(r) for r in out]


# =============================================================================
# Shared: marble floor, Doric column, doormats, stairs, bench, brazier
# =============================================================================

# White marble slabs with a soft bevel; A and B alternate as a checker.
art("floor_marble_a", [
    "5555555555555555",
    "5888888888888887",
    "5877777777777776",
    "5877777777777776",
    "5877777777777776",
    "5877777777777776",
    "5877777777777776",
    "5877777777777776",
    "5877777777777776",
    "5877777777777776",
    "5877777777777776",
    "5877777777777676",
    "5877777777776776",
    "5877777777777776",
    "5877777777777776",
    "5766666666666666",
])

art("floor_marble_b", [
    "5555555555555555",
    "5777777777777776",
    "5766666666666665",
    "5766666666666665",
    "5766666666666665",
    "5766666666666665",
    "5766666666666665",
    "5766666666666665",
    "5766666666666665",
    "5766666666666665",
    "5766666666666665",
    "5766666666666665",
    "5766666666666665",
    "5766566666666665",
    "5766656666666665",
    "5655555555555555",
])

# A free-standing Doric column: capital, fluted shaft, plinth.
_SHAFT = ".18768657546431."
art("column", [
    "................",
    "................",
    "1111111111111111",
    "1888888888888871",
    "1666666666666551",
    "1111111111111111",
    "1788888877766541",
    ".17877776665431.",
    ".11111111111111.",
    ".12222222222221.",
] + [_SHAFT] * 30 + [
    ".17656546435321.",
    "1111111111111111",
    "1888888888887661",
    "1666666666665541",
    "1444444444443331",
    "1333333333332221",
    "1111111111111111",
    "................",
])

# Threshold mats: a terracotta mosaic with a cream field and a black key.
art("mat_single", [
    "................",
    ".TTTTTTTTTTTTTT.",
    ".TuuuuuuuuuuuuT.",
    ".TuPPPPPPPPPPtT.",
    ".TuP#P##P##P#tT.",
    ".TuP#PPPPPPP#tT.",
    ".TuP#P####P##tT.",
    ".TuPPP#PP#PPPtT.",
    ".TuP##P##P###tT.",
    ".TuP#PPPPPPP#tT.",
    ".TuP#P##P##P#tT.",
    ".TuPPPPPPPPPPtT.",
    ".TutttttttttttT.",
    ".TTTTTTTTTTTTTT.",
    "..RRRRRRRRRRRR..",
    "................",
])

# Marble stairs climbing into a doorway in the back wall (2 wide x 3 tall).
# The bottom row holds the lowest steps, on the floor: the warp tiles.
_STEPS = ["#", "#", "2", "1", "1", "3", "2", "2", "4", "4", "3", "3", "5", "5",
          "4", "4", "6", "6", "4", "4", "7", "7", "5", "5", "8", "6"]
art("stairs_up", [
    "1" * 32,
    "1" + "8" * 30 + "1",
    "1" + "7" * 30 + "1",
    "1" + "6" * 29 + "51",
    "1" + "4" * 30 + "1",
    "1" * 32,
] + ["1875" + "1" + s * 22 + "2" + "6531" for s in _STEPS] + [
    "1" + "8" * 30 + "1",
    "1" + "7" * 30 + "1",
    "1" + "6" * 30 + "1",
    "1" + "4" * 30 + "1",
    "1" + "3" * 30 + "1",
    "1" + "8" * 30 + "1",
    "1" + "7" * 30 + "1",
    "1" + "6" * 30 + "1",
    "1" + "4" * 30 + "1",
    "1" + "3" * 30 + "1",
    "1" * 32,
    "." * 32,
    "." * 32,
    "." * 32,
    "." * 32,
    "." * 32,
])

# A marble bench with lion-paw feet.
art("bench", [
    "................................",
    "................................",
    "................................",
    ".111111111111111111111111111111.",
    "18888888888888888888888888888761",
    "17777777777777777777777777777651",
    "17777777777777777777777777776551",
    "16666666666666666666666666665541",
    "11111111111111111111111111111111",
    ".155541..................155541.",
    ".165441..................165441.",
    ".175431..................175431.",
    ".175431..................175431.",
    "1785431..................1785431",
    "1111111..................1111111",
    "................................",
])

# A bronze tripod brazier with a live flame (flame row, then legs).
art("brazier", [
    "................",
    "................",
    ".......V........",
    "......VV........",
    "......VXV.......",
    ".....VXV..V.....",
    ".....VXXV.VV....",
    "....VXrXV.VXV...",
    "....VXrXXVXXV...",
    "...VXrrXXXrXV...",
    "...VXrrrXrrXV...",
    "..VXXrrrrrrXXV..",
    ".ZZZZZZZZZZZZZZ.",
    ".ZhgggggggggGxZ.",
    "..ZxGGGGGGGGxZ..",
    "...ZZxxxxxxZZ...",
    ".....ZZxxZZ.....",
    "......ZxZ.......",
    ".....Z.x.Z......",
    ".....Z.x.Z......",
    "....Z..x..Z.....",
    "....Z..x..Z.....",
    "...Z...x...Z....",
    "...Z...x...Z....",
    "..Z...ZxZ...Z...",
    ".ZxZ...Z...ZxZ..",
    ".ZZZ.......ZZZ..",
    "................",
    "................",
    "................",
    "................",
    "................",
])


# =============================================================================
# The Asclepeion: white marble, a blue wave frieze, the spring, the serpent
# =============================================================================

# Back wall, top row: cornice and a running-wave frieze between gold fillets.
art("wall_asc_top", [
    "1111111111111111",
    "5555555555555555",
    "8888888888888888",
    "6666666666666666",
    "3333333333333333",
    "GGGGGGGGGGGGGGGG",
    "bbbbbbbbbbbbbbbb",
    "bbb88bbbbbb88bbb",
    "bb8bb8bbbb8bb8bb",
    "b8bb88bbb8bb88bb",
    "8bbbbbb88bbbbbb8",
    "8888888888888888",
    "GGGGGGGGGGGGGGGG",
    "2222222222222222",
    "7777777777777777",
    "6666666666666666",
])

# Back wall, lower row: marble ashlar over a blue dado.
art("wall_asc_body", [
    "5888888888888888",
    "5777777777777777",
    "5777777777777777",
    "5777777777777777",
    "5777777777777777",
    "5777777777777777",
    "5666666666666666",
    "5555555555555555",
    "8888888588888888",
    "7777777577777777",
    "7777777577777777",
    "6666666566666666",
    "3333333333333333",
    "bbbbbbbbbbbbbbbb",
    "BBBBBBBBBBBBBBBB",
    "1111111111111111",
])

# The healer's counter, an altar of marble. Top row: left end, middle, right
# end. The slab fills the lower ten rows; above it is the floor behind.
art("counter_asc_top", [
    "." * 48,
    "." * 48,
    "." * 48,
    "." * 48,
    "." * 48,
    "." * 48,
    "." + "1" * 46 + ".",
    "18" + "8" * 44 + "71",
    "18" + "7" * 44 + "61",
    "18" + "7" * 44 + "61",
    "18" + "7" * 44 + "61",
    "18" + "7" * 44 + "61",
    "18" + "6" * 44 + "51",
    "18" + "8" * 44 + "51",
    "15" + "5" * 44 + "41",
    "13" + "3" * 44 + "31",
])

# Its front: a triglyph frieze with blue metopes and gold rosettes.
_TRI = ["353bbbbb", "353bbbbb", "353bbgbb", "353bgGgb", "353bbgbb", "353bbbbb"]
art("counter_asc_front", [
    "1" + "4" * 46 + "1",
    "1" + "2" * 46 + "1",
    "17" + "6" * 44 + "51",
    "17" + "1" * 44 + "31",
] + ["17" + rep(m, 44) + "31" for m in _TRI] + [
    "17" + "1" * 44 + "31",
    "17" + "7" * 44 + "41",
    "17" + "6" * 44 + "41",
    "18" + "8" * 44 + "51",
    "14" + "4" * 44 + "31",
    "1" * 48,
])

# The sacred spring, where the healing machine stood (2x2: the wall row, then
# the counter row). A bronze serpent spouts into a marble basin; the heal
# animation drops the party's balls at x 9-23, y 8-24 of this piece, on the
# water.
art("basin", [
    "................................",
    "............11111111............",
    "............18gggg71............",
    "............17#gg#61............",
    "............16gGGg51............",
    ".............1GccG1.............",
    ".......11111111cF11111111.......",
    "....11188888888cF88888877111....",
    "..11877BBBBBBBBcFBBBBBBBB77611..",
    ".187B" + "bbbbbbbbbbCFbbbbbbbbbb" + "B761.",
    ".187b" + "bbbbbbbbbcFFcbbbbbbbbb" + "b761.",
    ".187b" + "bbbbbbbcbbbbbbcbbbbbbb" + "b761.",
    ".177b" + "bbbbbbcbbbbbbbbcbbbbbb" + "b651.",
    ".177b" + "bbbbbbbccccccccbbbbbbb" + "b651.",
    ".177b" + "bbbbbbbbbbbbbbbbbbbbbb" + "b651.",
    ".176b" + "bbbbbbbbbbbbbbbbbbbbbb" + "b651.",
    # the counter row
    ".176c" + "cbbbbbbbbbbbbbbbbbbbbc" + "c551.",
    ".176c" + "ccbbbbbbbbbbbbbbbbbbcc" + "c551.",
    ".166c" + "cccccccccccccccccccccc" + "c541.",
    ".1" + "8" * 28 + "1.",
    "..1" + "7" * 6 + "6" * 20 + "1..",
    "...1" + "5" * 24 + "1...",
    "11111" + "4" * 22 + "11111",
    "888881" + "3" * 20 + "188888",
    "7777777" + "1" * 18 + "7777777",
    "77777777" + "5" * 18 + "777777",
    "7" * 32,
    "7" * 32,
    "6" * 32,
    "8" * 32,
    "5" * 32,
    "3" * 32,
])

# The rod of Asclepius: a painted relief on the wall above the healer. Only
# the top row shows over her head, so the serpent's head is there.
_ROD = [
    "BbbbbbbbbB",
    "Bbbbhhbbbb",
    "BbbbxZbggb",
    "BbbbxZg#gb",
    "BbbbxZGgbb",
    "BbbbgGbbbb",
    "BbbgxZbbbb",
    "BbgGxZbbbb",
    "BbbgxZbbbb",
    "BbbbgGbbbb",
    "BbbbxZgbbb",
    "BbbbxZgGbb",
    "BbbbxZgbbb",
    "BbbbgGbbbb",
    "BbbgxZbbbb",
    "BbgGxZbbbb",
    "BbbgxZbbbb",
    "BbbbgGbbbb",
    "BbbbxZgbbb",
    "BbbbxZbgbb",
    "BbbbxZbbbb",
    "BBBBZZBBBB",
]
# The staff is painted wood-brown, which keeps it in the marble palette.
WOOD_STAFF = str.maketrans("xZh", "tTg")
_ROD = [r.translate(WOOD_STAFF) for r in _ROD]
art("relief", [
    "................",
    "................",
    "......1111......",
    "....11777711....",
    "..117777777611..",
    ".1" + "7" * 11 + "61.",
    ".1" + "5" * 11 + "41.",
    ".17" + "1" * 10 + "41.",
] + [".17" + r + "41." for r in _ROD] + [
    ".17" + "1" * 10 + "41.",
    ".1" + "3" * 12 + "1.",
])

# Votive tablets hung on the wall: a patient on a couch, an eye, a serpent.
art("votive_wall", [
    "................................",
    "......1" + "." * 10 + "1" + "." * 9 + "1....",
    ".....1.1" + "." * 8 + "1.1" + "." * 7 + "1.1...",
    "....1...1" + "." * 6 + "1...1" + "." * 5 + "1...1..",
    ".." + "R" * 9 + "..." + "R" * 7 + "..." + "R" * 7 + ".",
    ".." + "RUuuuuuuR" + "..." + "RUuuutR" + "..." + "RUu##uR" + ".",
    ".." + "Ru#uuuuuR" + "..." + "Ru###tR" + "..." + "Ru#uuuR" + ".",
    ".." + "Ru####uuR" + "..." + "R#u#u#R" + "..." + "Ruu#uuR" + ".",
    ".." + "Ru#####uR" + "..." + "Ru###tR" + "..." + "Ruuu#uR" + ".",
    ".." + "Ru#uuu#uR" + "..." + "RuuuutR" + "..." + "Ruu#uuR" + ".",
    ".." + "RuuuuuuuR" + "..." + "RRRRRRR" + "..." + "Ru#uutR" + ".",
    ".." + "RttttttTR" + "..." + "......." + "..." + "RtttttR" + ".",
    ".." + "RRRRRRRRR" + "..." + "......." + "..." + "RRRRRRR" + ".",
    "................................",
    "................................",
    "................................",
])

# Clay votives on the counter: a leg, an arm, an eye plaque.
art("votive_counter", [
    "................................",
    "...RRRR" + "." * 25,
    "...RUtR" + "." * 25,
    "...RutR" + "." * 14 + "RRRRRR" + ".....",
    "...RutR" + "." * 14 + "RUuuuR" + ".....",
    "...RutR" + "." * 14 + "Ru##uR" + ".....",
    "111RutR" + "1" * 14 + "R#uu#R" + "11111",
    "888RuttRR" + "8" * 7 + "RRR" + "88" + "Ru##uR" + "88888",
    "777RutttuR" + "7" + "RRRRRuUuR" + "7" + "RuuutR" + "77777",
    "777RRRRRRR" + "7" + "RUuuuttuR" + "7" + "RRRRRR" + "77777",
    "7777555555" + "7" + "RRRRRRRRR" + "77" + "55555" + "77777",
    "7" * 12 + "5" * 9 + "7" * 11,
    "6" * 32,
    "8" * 32,
    "5" * 32,
    "3" * 32,
])

# The Pithos: a great storage jar, rope bands, its lid sealed with wax.
art("pithos_big", [
    "." * 32,
    "." * 14 + "RXrR" + "." * 14,
    "." * 11 + "RTTrXrrTTR" + "." * 11,
    "." * 10 + "RUuttrrttTTR" + "." * 10,
    "." * 8 + "R" * 16 + "." * 8,
    "." * 8 + "RUUuuuuuuuuuutTR" + "." * 8,
    "." * 8 + "RuttttttttttttTR" + "." * 8,
    "." * 8 + "R" * 16 + "." * 8,
    "." * 10 + "RtttttttttTR" + "." * 10,
    "." * 8 + "RRutttttttttTTRR" + "." * 8,
    "." * 6 + "RRUuuuttttttttttTTRR" + "." * 6,
    "." * 5 + "RUUuuuuttttttttttttTTR" + "." * 5,
    "." * 4 + "R" + "TU" * 11 + "R" + "." * 4,
    "." * 3 + "R" + "UT" * 12 + "R" + "." * 3,
    "." * 3 + "RUUuuuuuttttttttttttttTTTR" + "." * 3,
    "." * 2 + "RUUuuuuuuttttttttttttttTTTTR" + "." * 2,
    "..RuUUuuuu" + "t" * 15 + "TTTTR..",
    "..RuUUuuuu" + "t" * 15 + "TTTTR..",
    "..RuUUuuuu" + "t" * 15 + "TTTTR..",
    "..RuUUuuuu" + "tTUttTUttTUttTt" + "TTTTR..",
    "..RuUUuuuu" + "t" * 15 + "TTTTR..",
    "..RuUUuuuu" + "t" * 15 + "TTTTR..",
    "..RuUUuuuu" + "t" * 15 + "TTTTR..",
    "..RuUUuuuu" + "t" * 15 + "TTTTR..",
    "..R" + "TU" * 13 + "R..",
    "..R" + "UT" * 13 + "R..",
    "..RuuUuuu" + "t" * 16 + "TTTTR..",
    "..RuuUuuu" + "t" * 16 + "TTTTR..",
    "..RuuUuuu" + "t" * 16 + "TTTTR..",
    "...Ruuuuu" + "t" * 14 + "TTTTTR...",
    "...Ruuuuu" + "t" * 14 + "TTTTTR...",
    "....Ruuuu" + "t" * 14 + "TTTTR....",
    "....Ruuuu" + "t" * 14 + "TTTTR....",
    ".....Ruuu" + "t" * 13 + "TTTTR.....",
    ".....Ruuu" + "t" * 13 + "TTTTR.....",
    "......Ruu" + "t" * 12 + "TTTTR......",
    "......Ruu" + "t" * 12 + "TTTTR......",
    ".......Ru" + "t" * 12 + "TTTR.......",
    ".......R" + "t" * 13 + "TTTR.......",
    "........RT" + "t" * 10 + "TTTR........",
    ".........RT" + "t" * 8 + "TTTR.........",
    ".........." + "RTTttttTTTTR" + "..........",
    ".........." + "R" + "T" * 10 + "R" + "..........",
    "........." + "Ru" + "t" * 10 + "TR" + ".........",
    "........." + "R" + "T" * 12 + "R" + ".........",
    "........." + "#" * 14 + ".........",
    "." * 32,
    "." * 32,
])

# A smaller lidded storage jar for the Pithos corner.
art("pithos_small", [
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    ".....RRRRRR.....",
    ".....RUuttR.....",
    "....RRRRRRRR....",
    "....RUuuttTR....",
    "....RRRRRRRR....",
    ".....RttttR.....",
    "...RRuttttTRR...",
    "..RUUuttttttTR..",
    ".RUUuuttttttTTR.",
    ".R" + "TU" * 6 + "R.",
    ".R" + "UT" * 6 + "R.",
    ".RuUuuttttttTTR.",
    ".RuUuuttttttTTR.",
    ".RuUuuttttttTTR.",
    ".RuUuuttttttTTR.",
    ".RuUuuttttttTTR.",
    ".RuUuuttttttTTR.",
    ".RuuuttttttTTTR.",
    "..RuuttttttTTR..",
    "..RuttttttTTTR..",
    "...RutttttTTR...",
    "....RttttTTR....",
    "....RTTTTTTR....",
    ".....RttttR.....",
    ".....######.....",
    "." * 16,
])

# Asclepius in a wall niche, leaning on his serpent staff, on a plinth.
_STATUE = [
    "3333566333",
    "3335788633",
    "3335878633",
    "3335777533",
    "3333576533",
    "3333565333",
    "3h33676543",
    "3x57887652",
    "gZg7887652",
    "3Z57877652",
    "3Zg7787652",
    "gZ37876552",
    "3Z37787652",
    "3Zg7778652",
    "gZ37787552",
    "3Z37877652",
    "3Zg7787652",
    "gZ37778552",
    "3Z37787652",
    "3Zg7877652",
    "3Z37787552",
    "3Z37778652",
    "3Z37787652",
    "3Z37877552",
    "3Z37787652",
    "3Z37778652",
]
# The niche is painted Aegean blue so the white marble stands out.
_STATUE = [r.replace("3", "b").replace("2", "B").translate(WOOD_STAFF) for r in _STATUE]
art("statue", [
    "." * 16,
    "." * 16,
    ".....111111.....",
    "...1144444411...",
    "..14BBBBBBBB41..",
    ".14" + "BBbbbbbbBB" + "41.",
] + [".14" + r + "41." for r in _STATUE] + [
    "....T.677755....",
    "....T.676655....",
    "....T.655554....",
    "....T5444443....",
    ".11111111111111.",
    ".1" + "8" * 11 + "71.",
    ".1" + "7" * 11 + "61.",
    ".1" + "6" * 11 + "51.",
    ".11111111111111.",
    ".17" + "5" * 10 + "41.",
    ".17" + "5353535353" + "41.",
    ".17" + "5" * 10 + "41.",
    ".16" + "4" * 10 + "31.",
    ".11111111111111.",
    "." * 16,
    "." * 16,
])

# A healing couch (kline) of stone: headrest, linen mattress, blue blanket.
_STONE_FRAME = str.maketrans("DWwdvN", "14335B")
art("kline", [r.translate(_STONE_FRAME) for r in [
    "." * 32,
    "." * 32,
    "." * 32,
    "." * 32,
    "..DDDD" + "." * 26,
    ".DWvvWD" + "." * 25,
    ".DWvWwD" + "." * 25,
    ".DWwwwD" + "D" * 24 + ".",
    ".DWwwwD" + "888886" + "777777" + "Cccccccccbb" + "D.",
    ".DWwwwD" + "888876" + "777777" + "cccccccccbb" + "D.",
    ".DWwwwD" + "877765" + "777777" + "cccbcccccbb" + "D.",
    ".DWwwwD" + "766655" + "777777" + "ccbbbcccbbb" + "D.",
    ".DWwwwD" + "666655" + "666666" + "bbbbbbbbbbB" + "D.",
    ".DwwwdD" + "4" * 12 + "B" * 11 + "D.",
    ".DwwwdD" + "3" * 12 + "N" * 11 + "D.",
    ".DdddDD" + "D" * 24 + ".",
    ".D" + "W" * 28 + "D.",
    ".D" + "w" * 28 + "D.",
    ".D" + "D" * 28 + "D.",
    "..DWwD........DWwD........DWwD..",
    "..DwwD........DwwD........DwwD..",
    "...DwD.........DwD.........DwD..",
    "..DWwD........DWwD........DWwD..",
    "..DwdD........DwdD........DwdD..",
    "...DwD.........DwD.........DwD..",
    "...DdD.........DdD.........DdD..",
    "..DDDD........DDDD........DDDD..",
    "." * 32,
    "." * 32,
    "." * 32,
    "." * 32,
    "." * 32,
]])

# One of the god's harmless snakes, loose on the floor.
art("snake", [
    "................",
    "................",
    "................",
    "................",
    "...........kk...",
    "..........koOk..",
    "..........ko#k..",
    "...........kok..",
    "....kkk.....kok.",
    "...koOok...kok..",
    "..kok.kok.kok...",
    "..kok..koOok....",
    "...kok..kkk.....",
    "....kk..........",
    "................",
    "................",
])

# The floor mosaic: a serpent rod in a terracotta ring, framed in blue.
_MOSAIC = [
    "555555555555555555555555555555555555555555555555",
    "577777777777777777777777777777777777777777777776",
    "577777777777777777777777777777777777777777777776",
    "577BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB776",
    "577BbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbB776",
    "577BbBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBbB776",
    "577BbB77777777777777TTTTTTTT77777777777777BbB776",
    "577BbB77777777777TTTTTTTTTTTTTT77777777777BbB776",
    "577BbB777777777TTTttttttttttttTTT777777777BbB776",
    "577BbB7777777TTTtttt88888888ttttTTT7777777BbB776",
    "577BbB777777TTTtt88888888888888ttTTT777777BbB776",
    "577BbB77777TTttt8888888888888888tttTT77777BbB776",
    "577BbB7777TTtt88888888888888888888ttTT7777BbB776",
    "577BbB777TTtt8888888888888888888888ttTT777BbB776",
    "577BbB777TTt888888888888888888888888tTT777BbB776",
    "577BbB77TTtt888888888888888888888888ttTT77BbB776",
    "577BbB77Ttt88888888888888888888888888ttT77BbB776",
    "577BbB7TTt8888888888888888888888888888tTT7BbB776",
    "577BbB7Ttt8888888888888888888888888888ttT7BbB776",
    "577BbB7Ttt8888888888888888888888888888ttT7BbB776",
    "577BbBTTt888888888888888888888888888888tTTBbB776",
    "577BbBTTt888888888888888888888888888888tTTBbB776",
    "577BbBTTt888888888888888888888888888888tTTBbB776",
    "577BbBTTt888888888888888888888888888888tTTBbB776",
    "577BbBTTt888888888888888888888888888888tTTBbB776",
    "577BbBTTt888888888888888888888888888888tTTBbB776",
    "577BbBTTt888888888888888888888888888888tTTBbB776",
    "577BbBTTt888888888888888888888888888888tTTBbB776",
    "577BbB7Ttt8888888888888888888888888888ttT7BbB776",
    "577BbB7Ttt8888888888888888888888888888ttT7BbB776",
    "577BbB7TTt8888888888888888888888888888tTT7BbB776",
    "577BbB77Ttt88888888888888888888888888ttT77BbB776",
    "577BbB77TTtt888888888888888888888888ttTT77BbB776",
    "577BbB777TTt888888888888888888888888tTT777BbB776",
    "577BbB777TTtt8888888888888888888888ttTT777BbB776",
    "577BbB7777TTtt88888888888888888888ttTT7777BbB776",
    "577BbB77777TTttt8888888888888888tttTT77777BbB776",
    "577BbB777777TTTtt88888888888888ttTTT777777BbB776",
    "577BbB7777777TTTtttt88888888ttttTTT7777777BbB776",
    "577BbB777777777TTTttttttttttttTTT777777777BbB776",
    "577BbB77777777777TTTTTTTTTTTTTT77777777777BbB776",
    "577BbB77777777777777TTTTTTTT77777777777777BbB776",
    "577BbBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBbB776",
    "577BbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbB776",
    "577BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB776",
    "577777777777777777777777777777777777777777777776",
    "577777777777777777777777777777777777777777777776",
    "566666666666666666666666666666666666666666666666",
]
_CORNER = [".b.", "bBb", ".b."]
_MOSAIC = paste(_MOSAIC, _ROD[1:21], 19, 14, {"B": "8", "b": "8", "t": "3", "T": "2"})
for _cx, _cy in ((8, 8), (37, 8), (8, 37), (37, 37)):
    _MOSAIC = paste(_MOSAIC, _CORNER, _cx, _cy)
art("mosaic", _MOSAIC)


# =============================================================================
# The Agora: terracotta tiles, a timber beam, dyed cloth, the merchant's stall
# =============================================================================

# Large pale fired-clay tiles with a soft bevel, so clay pots stand out.
art("floor_tc", [
    "tttttttttttttttt",
    "tPUUUUUUUUUUUUUU",
    "tUUUUUUUUUUUUUUu",
    "tUUUUUUUUUUUUUUu",
    "tUUUUUUUUUUUUUUu",
    "tUUUUUUUUUUUUUUu",
    "tUUUUUUUUUUUUUUu",
    "tUUUUUUUUUUUUUUu",
    "tUUUUUUUUUUUUUUu",
    "tUUUUUUUUUUUUUUu",
    "tUUUUUUUUUUuUUUu",
    "tUUUUUUUUUUUuUUu",
    "tUUUUUUUUUUUUUUu",
    "tUUUUUUUUUUUUUUu",
    "tUUUUUUUUUUUUUUu",
    "tuuuuuuuuuuuuuuu",
])

# Back wall: a timber beam over limewashed plaster, a red dado below.
art("wall_ago_top", [
    "DDDDDDDDDDDDDDDD",
    "vvvvvvvvvvvvvvvv",
    "WWWWWWWWWWWWWWWW",
    "WWwWWWWWWWWWwWWW",
    "wwwwwwwwwwwwwwww",
    "dddddddddddddddd",
    "DDDDDDDDDDDDDDDD",
    "pppppppppppppppp",
    "LLLLLLLLLLLLLLLL",
    "PPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPP",
    "PPPPLPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPLPP",
    "PPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPP",
])

art("wall_ago_body", [
    "PPPPPPPPPPPPPPPP",
    "PPPPPPPPPLPPPPPP",
    "PPPPPPPPPPPPPPPP",
    "PPLPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPLPPP",
    "PPPPPPPPPPPPPPPP",
    "LLLLLLLLLLLLLLLL",
    "TTTTTTTTTTTTTTTT",
    "uuuuuuuuuuuuuuuu",
    "tttttttttttttttt",
    "tttttttttttttttt",
    "tttttttttttttttt",
    "TTTTTTTTTTTTTTTT",
    "RRRRRRRRRRRRRRRR",
])

# Dyed cloth hung from a rod under the beam (purple; blue and saffron are
# recolors in civic_tiles.py).
art("cloth", [
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    ".DDDDDDDDDDDDDD.",
    "..nMMmnMMmnMMm..",
    "..nMMmnMMmnMMm..",
    "..nMMMmMMmnMMm..",
    "..nnMMmMMmnnMm..",
    "..nMMmnMMmnMMm..",
    "..nMMmnMMMmMMm..",
    "..nMMmnnMMmMMm..",
    "..nMMmnMMmnMMm..",
    "..nMMmnMMmnMMm..",
    "..gggggggggggG..",
    "..GGGGGGGGGGGG..",
    "..nMMmnMMmnMMm..",
    "..nMMmnMMmnMMm..",
    "..mmmmmmmmmmmm..",
    "..m.m.m.m.m.m...",
    "..m.m.m.m.m.m...",
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
])

# Herbs and a garlic braid drying from the beam.
art("herbs", [
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "..k....k....k...",
    "..k....k....k...",
    ".kkk..kkk..kkk..",
    ".yOy..I88I.oio..",
    "yOOoy.8IIjoiiOy.",
    "yOoOy.I88IiOiOy.",
    "oyOyo.jIIjOiOiy.",
    "yoOoy.I88I.yOy..",
    ".yoy..8IIj.yoy..",
    "o.y.o.I88I..y...",
    "..y...jIIj......",
    ".......II.......",
    ".......jj.......",
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
])

# A narrow shelf unit of pottery: oil flasks, an amphora, two jars.
_SHELF_IN = [
    "DDDDDDDDDDDD",
    "dddddddddddd",
    "dddRddddRRdd",
    "ddRuRdddRRdd",
    "dRUutRdRuuRd",
    "dRuttRdR##Rd",
    "dRuttRdRutRd",
    "ddRTRdddRRdd",
    "dddddddddddd",
    "dddddddddddd",
    None,
    "DDDDDDDDDDDD",
    "ddddRRRRdddd",
    "dddRRuRRRddd",
    "dddRRUutRRdd",
    "dddRUuuttRdd",
    "dddRuuuttRdd",
    "dddR#u#u#Rdd",
    "dddRuuuttRdd",
    "ddddRuutRddd",
    "ddddRuttRddd",
    "dddddRtRdddd",
    "dddddRRddddd",
    None,
    "DDDDDDDDDDDD",
    "dddddddddddd",
    "ddRRRdddRRRd",
    "dRUutRdRUutR",
    "dRuutRdRuutR",
    "dR#u#RdR#u#R",
    "dRuttRdRuttR",
    "ddRTRdddRTRd",
    "dddddddddddd",
    "dddddddddddd",
]
_SHELF_BOARD = ["D" + "v" * 14 + "D", "D" + "w" * 14 + "D", "D" * 16]
_shelf = ["." * 16] * 3 + ["D" * 16, "D" + "v" * 14 + "D", "D" + "w" * 14 + "D", "D" * 16]
for _r in _SHELF_IN:
    _shelf += _SHELF_BOARD if _r is None else ["DW" + _r + "wD"]
_shelf += ["D" + "v" * 14 + "D", "D" + "w" * 14 + "D", "D" * 16]
art("shelf_pots", _shelf)

# The merchant's counter. Top row: the slab, with the awning's poles at the
# ends; the balance scale and the goods are laid on it below.
art("counter_ago_top", [
    "DWD" + "." * 42 + "DWD",
    "DWD" + "." * 42 + "DWD",
    "DWD" + "." * 42 + "DWD",
    "DWD" + "." * 42 + "DWD",
    "DWD" + "." * 42 + "DWD",
    "DWD" + "." * 42 + "DWD",
    "D" * 48,
    "Dv" + "v" * 44 + "wD",
    "DW" + rep("WWWWWWWw", 44) + "wD",
    "DW" + "W" * 44 + "wD",
    "DW" + rep("wWWWWWWW", 44) + "dD",
    "Dw" + "w" * 44 + "dD",
    "Dw" + "w" * 44 + "dD",
    "Dv" + "v" * 44 + "wD",
    "Dd" + "d" * 44 + "dD",
    "D" * 48,
])

# The stall's cloth is drawn as blue-and-white stripes, then dyed madder red
# on cream so the whole stall sits in the warm wood palette.
WARM = str.maketrans("BbcC678", "TtuuLPQ")

# Its front: a striped cloth over plank boards.
art("counter_ago_front", [r.translate(WARM) for r in [
    "D" + rep("BBBB6666", 46) + "D",
    "D" + rep("cbbb7888", 46) + "D",
    "D" + rep("cbbb7888", 46) + "D",
    "D" + rep("cbbb7888", 46) + "D",
    "D" + rep("cbbb7888", 46) + "D",
    "D" + rep("cbbb7888", 46) + "D",
    "D" + rep("cbbb7888", 46) + "D",
    "D" + rep("bbbb8888", 46) + "D",
    "D" + rep("BbbB6886", 46) + "D",
    "D" + rep("wBBdw66d", 46) + "D",
    "D" + rep("WWwd", 46) + "D",
    "D" + rep("WWwd", 46) + "D",
    "D" + rep("WWwd", 46) + "D",
    "D" + rep("WWwd", 46) + "D",
    "D" + rep("wwdd", 46) + "D",
    "D" * 48,
]])

# A bronze balance scale, laid on the counter's left end.
SCALE = [
    ".....hg.....",
    "zgggggggggxz",
    "x....Zx....x",
    "x....Zx....x",
    "x....Zx....x",
    "GggG.Zx.GggG",
    ".GG..Zx..GG.",
    ".....Zx.....",
    ".....Zx.....",
    "....ZZxZ....",
    "....zzzz....",
]

# A round loaf and an oil flask, laid on the counter's right end.
GOODS = [
    "...........",
    "........RR.",
    "........RR.",
    ".DDDD..RUtR",
    "DvvWWD.RutR",
    "DvWWwD.RutR",
    "DWwwdD.RttR",
    ".DDDD...RR.",
]

# The stall's striped awning, hung under the beam on two poles (3x2).
art("awning", [r.translate(WARM) for r in [
    "." * 48,
    "." * 48,
    "." * 48,
    "." * 48,
    "." * 48,
    "." * 48,
    "." * 48,
    "D" * 48,
    "D" + rep("BBBB6666", 46) + "D",
    "D" + rep("BBBB6666", 46) + "D",
    "D" + rep("bbbb7777", 46) + "D",
    "D" + rep("cbbb7888", 46) + "D",
    "D" + rep("cbbb7888", 46) + "D",
    "D" + rep("cbbb7888", 46) + "D",
    "D" + rep("cbbb7888", 46) + "D",
    "D" + rep("cbbb7888", 46) + "D",
    "D" + rep("cbbb7888", 46) + "D",
    "D" + rep("bbbb8888", 46) + "D",
    "D" + rep("BBBB6666", 46) + "D",
    "D" * 48,
    "D" + rep("cbbb7888", 46) + "D",
    "D" + rep("bbbb8888", 46) + "D",
    "D" + rep("bbbb8888", 46) + "D",
    "D" + rep("BbbB6886", 46) + "D",
    "D" + rep(".BB..66.", 46) + "D",
    "DWD" + "." * 42 + "DWD",
    "DWD" + "." * 42 + "DWD",
    "DWD" + "." * 42 + "DWD",
    "DWD" + "." * 42 + "DWD",
    "DWD" + "." * 42 + "DWD",
    "DWD" + "." * 42 + "DWD",
    "DWD" + "." * 42 + "DWD",
]])

# A wicker basket. The mound uses 1-3 (light to dark), recolored per good.
BASKET = [
    "................",
    "......1221......",
    "....13213231....",
    "..123212321232..",
    ".D312321232123D.",
    "DvvvvvvvvvvvvvwD",
    "DWWWWWWWWWWWWWdD",
    "DWwWwWwWwWwWwWdD",
    "DwWwWwWwWwWwWwdD",
    "DWwWwWwWwWwWwWdD",
    "DwWwWwWwWwWwWwdD",
    ".DWwWwWwWwWwWdD.",
    ".DwWwWwWwWwWwdD.",
    "..DWwWwWwWwWdD..",
    "..DDDDDDDDDDDD..",
    "................",
]
for _name, _cols in (("grain", "hgG"), ("olives", "oYE"), ("figs", "nMm"), ("pomegranates", "rAa")):
    _rows = [r.replace("1", _cols[0]).replace("2", _cols[1]).replace("3", _cols[2]) for r in BASKET]
    if _name == "olives":
        # Green olives in a rush basket, all in the grove palette.
        _rows = [r.translate(str.maketrans("DdwWv", "#kKjI")) for r in _rows]
    art(f"basket_{_name}", _rows)

# A plain wooden table (2x2). The money-changer's trapeza, Daphne's writing
# desk and Alethea's worktable are this table with different things on it,
# so their legs share tiles.
TABLE = [
    "." * 32,
    "." * 32,
    "." * 32,
    "." * 32,
    "." * 32,
    "." * 32,
    "." + "D" * 30 + ".",
    "D" + "v" * 30 + "D",
] + ["DW" + rep("WWWWWWWWWWWwWWWW", 28) + "wD"] * 9 + [
    "D" + "v" * 30 + "D",
    "D" + "w" * 30 + "D",
    "D" + "d" * 30 + "D",
    "D" * 32,
    "..DWwD" + "." * 20 + "DWwD..",
    "..DwdD" + "." * 20 + "DwdD..",
    "..DwdD" + "." * 20 + "DwdD..",
    "..DWwD" + "." * 20 + "DWwD..",
    "..DwdD" + "." * 20 + "DwdD..",
    "..DDDD" + "." * 20 + "DDDD..",
    "." * 32,
    "." * 32,
    "." * 32,
    "." * 32,
    "." * 32,
]

# The money-changer's table (trapeza): coin stacks, loose coins, a purse.
_TRAPEZA = TABLE
_SILVER = [".gg.", "ghhg", "xggx", "ZxxZ", "xZZx", "ZxxZ", ".ZZ."]  # bronze obols
_GOLD = [".gg.", "ghhg", "GggG", "xGGx", "GxxG", "xGGx", ".xx."]
_PURSE = ["..D.D..", "..DwD..", ".DWWwD.", "DWWwwdD", "DWwwddD", ".DdddD."]
_TRAPEZA = paste(_TRAPEZA, _SILVER, 4, 7)
_TRAPEZA = paste(_TRAPEZA, _GOLD, 9, 8)
_TRAPEZA = paste(_TRAPEZA, _PURSE, 20, 9)
for _x, _y, _c in ((15, 12, "gG"), (26, 10, "hg"), (13, 15, "gx"), (6, 15, "Gx")):
    _TRAPEZA = paste(_TRAPEZA, [_c], _x, _y)
art("trapeza", _TRAPEZA)

# A black-figure amphora in a ring stand.
art("amphora", [
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "......RRRR......",
    ".......RuR......",
    "....RR.RuR.RR...",
    "...R..RRutRR.R..",
    "...R.RUuuttR.R..",
    "...RRUuuuttTRR..",
    "....RUuuuttTR...",
    "...RUuuuuttTTR..",
    "...R#########R..",
    "...R#uu#uu#u#R..",
    "...R#########R..",
    "...RuuuuutttTR..",
    "...RUuuuttttTR..",
    "....RuuuttttR...",
    "....RuutttTTR...",
    ".....RutttTR....",
    ".....RuttTTR....",
    "......RttTR.....",
    "......RtTTR.....",
    ".......RTR......",
    ".......RTR......",
    "....DDDRTDDD....",
    "....DWWRRWwD....",
    "....DddddddD....",
    ".....D....D.....",
    ".....D....D.....",
    "....DD....DD....",
    "." * 16,
])


# =============================================================================
# The Akademia: limestone, a meander frieze, scrolls, the grove and its laurel
# =============================================================================

# Limestone flagstones, laid in courses of uneven length.
art("floor_flags", [
    "pppppppppppppppp",
    "pQQQQQQQpQQQQQQQ",
    "pQPPPPPPpQPPPPPP",
    "pQPPPPPPpQPPPLPP",
    "pQPPLPPPpQPPPPPP",
    "pQPPPPPPpQPPPPPP",
    "pQPPPPPPpQPPPPPP",
    "pppppppppQPPPPPP",
    "pQQQQQQQpQPPPPPP",
    "pQPPPPPPpQPPPPPP",
    "pQPPPPPPpQPLPPPP",
    "pQPPPPLPpppppppp",
    "pQPPPPPPpQQQQQQQ",
    "pQPPPPPPpQPPPPPP",
    "pQPLPPPPpQPPPPLP",
    "pQPPPPPPpQPPPPPP",
])

# Back wall, top row: a cornice and a cream meander on a terracotta frieze.
_KEY = ["tttttttt", "PPPPPtPP", "ttttPtPt", "tPPPPtPt", "tPttttPt", "tPPPPPPt"]
art("wall_aka_top", [
    "DDDDDDDDDDDDDDDD",
    "LLLLLLLLLLLLLLLL",
    "QQQQQQQQQQQQQQQQ",
    "PPPPPPPPPPPPPPPP",
    "pppppppppppppppp",
    "RRRRRRRRRRRRRRRR",
] + [k * 2 for k in _KEY] + [
    "RRRRRRRRRRRRRRRR",
    "pppppppppppppppp",
    "QQQQQQQQQQQQQQQQ",
    "PPPPPPPPPPPPPPPP",
])

# Back wall, lower row: limestone ashlar over a darker plinth course.
art("wall_aka_body", [
    "pQQQQQQQQQQQQQQQ",
    "pQPPPPPPPPPPPPPP",
    "pQPPPPPPPPPPPPPP",
    "pPPPPPPPPPPPPPPP",
    "pPPPPPPPPPPPPPPP",
    "pLLLLLLLLLLLLLLL",
    "pppppppppppppppp",
    "QQQQQQQpQQQQQQQQ",
    "PPPPPPPpQPPPPPPP",
    "PPPPPPPpQPPPPPPP",
    "PPPPPPPpQPPPPPPP",
    "LLLLLLLpLLLLLLLL",
    "TTTTTTTTTTTTTTTT",
    "LLLLLLLLLLLLLLLL",
    "pppppppppppppppp",
    "DDDDDDDDDDDDDDDD",
])

# The grove's back: a clipped cypress hedge, two rows tall.
art("hedge", [
    "eeeeeeeeeeeeeeee",
    "eeeyyyeeeeeyyyee",
    "eeyOOyyeeeyOOyye",
    "eyOiOyyyeyOiOyyy",
    "yOiOyyyEyOiOyyyE",
    "yOOyyEyEyOOyyEyE",
    "yyyyEyEEyyyyEyEE",
    "EyyEyyEEEyyEyyEE",
    "yyOyyEEyyyOyyEEy",
    "yOiOyyEyyOiOyyEy",
    "yOOyyEyEyOOyyEyE",
    "EyyyEyEEEyyyEyEE",
    "yEEyyEEyyEEyyEEy",
    "yyOyEyyyyyOyEyyy",
    "yOiOyyEyyOiOyyEy",
    "EyOyyEEyEyOyyEEy",
    # lower row
    "yyOyyEEyyyOyyEEy",
    "yOiOyyEyyOiOyyEy",
    "yOOyyEyEyOOyyEyE",
    "EyyyEyEEEyyyEyEE",
    "yEEyyEEyyEEyyEEy",
    "yyOyEyyyyyOyEyyy",
    "yOiOyyEyyOiOyyEy",
    "EyOyyEEyEyOyyEEy",
    "yyyEyyEEyyyEyyEE",
    "EyEEyEEEEyEEyEEE",
    "EEEEEEEEEEEEEEEE",
    "EeEEEeEEEeEEEeEE",
    "eeEeeeeEeeEeeeeE",
    "eeeeeeeeeeeeeeee",
    "eeeeeeeeeeeeeeee",
    "eeeeeeeeeeeeeeee",
])

# Sun-bleached grass, plain and with wildflowers.
art("grass_a", [
    "iiiiiiiiiiiiiiii",
    "iiiiiiiiiiiiiiii",
    "iiiIiiiiiiiiiiii",
    "iiOiOiiiiiiiiiii",
    "iiiOiiiiiiiiIiii",
    "iiiiiiiiiiiOiOii",
    "iiiiiiiiiiiiOiii",
    "iiiiiiiiiiiiiiii",
    "iiiiiiiiiiiiiiii",
    "iiiiiiIiiiiiiiii",
    "iiiiiOiOiiiiiiii",
    "iiiiiiOiiiiiiiIi",
    "iiiiiiiiiiiiiOiO",
    "iiIiiiiiiiiiiiOi",
    "iOiOiiiiiiiiiiii",
    "iiOiiiiiiiiiiiii",
])

art("grass_b", [
    "iiiiiiiiiiiiiiii",
    "iiiiiiiiiii8iiii",
    "iiiIiiiiii8g8iii",
    "iiOiOiiiiii8iiii",
    "iiiOiiiiiiiOiiii",
    "iiiiiiiiiiiiiiii",
    "iiiiiAiiiiiiiiii",
    "iiiiAgAiiiiiIiii",
    "iiiiiAiiiiiOiOii",
    "iiiiiOiiiiiiOiii",
    "iiiiiiiiiiiiiiii",
    "iiIiiiiiiiiiiiii",
    "iOiOiiiiii8iiiii",
    "iiOiiiiii8g8iiii",
    "iiiiiiiiii8iiiii",
    "iiiiiiiiiiOiiiii",
])

# The stylobate: the raised marble strip the colonnade stands on.
art("stylobate", [
    "2455555555555555",
    "2487777777777776",
] + ["2477777777777776"] * 13 + [
    "2466666666666666",
])

# A laurel, Daphne's tree: canopy (drawn over walkers) and trunk.
_LAUREL = [
    "...............eee..............",
    "..........ee.eeeeeeeee..........",
    "........eeyyeyyyyeeyyeeee.......",
    "........eyyyyyyyyyyyyeeeee......",
    "....eeeeyyyyyyyyyyyyyyyyee......",
    "...eeeyyyyyyyyyyyyyyyyyyyeee....",
    "...eeeyyyyyyyyyyyyyyyyyyyyyye...",
    "..eeeeyyyyyyyyyyyyyyyyyyyyyye...",
    "..eyyyyyyyyyyyyyyyyyyyyyyyyye...",
    ".eeeyyyyyyyyyyyyyyyyyyyyyyyyee..",
    ".eeeyyyyyyyyyyyyyyyyyyyyyyyyyye.",
    "eeeyyyyyyyyyyyyyyyyyyyyyyyyyyye.",
    "eeyyyyyyyyyyyyyyyyyyyyyyyyyyyye.",
    ".eeyyyyyyyyyyyyyyyyyyyyyyyyyyye.",
    ".eyyyyyyyyyyyyyyyyyyyyyyyyyyEEee",
    ".eyyyyyyyyyyyyyyyyyyyyyyyyyEEEee",
    ".eyyyyyyyyyyyyyyyyyyyyyyyEEEEeee",
    ".eyyyyyyyyyyyyyyyyyyyyyyEEEEEee.",
    ".eyyyyyyyyyyyyyyyyyyyyyEEEEEEEee",
    ".eyyyyyyyyyyyyyyyyyyyEEEEEEEEee.",
    "..eeyyyyyyyyyyyyyyyyEEEEEEEEee..",
    "...eyyyyyyyyyyyyyyEEEEEEEEEEEe..",
    "...eyyyyyyyyyyyyyEEEEEEEEEEEee..",
    "...eyyyyyyyyyyyyEEEEEEEEEEeee...",
    "....eeyyyyyyyyEEEEEEEEEEEEee....",
    "......eyyyyyyEEEEEEEEEEEeeee....",
    "......eeeeyEEEEEEEEEEEEe........",
    ".......e.eeEeeeEEEEEEEe.........",
    ".........eeeeeeeeeeeee..........",
    "..............kKjKk.............",
    "..............kjKKk.............",
    "..............kKjjk.............",
    # trunk
    "..............kKjKk.............",
    "..............kjKKk.............",
    "..............kKjjk.............",
    "..............kKjKk.............",
    "..............kjKKk.............",
    "..............kKjjk.............",
    "..............kKjKk.............",
    "..............kjKKk.............",
    ".............kKKjKKk............",
    "............kKkjjKkKk...........",
    "...........kk.kKjKk.kk..........",
    "..........EEEEEEEEEEEEE.........",
    "." * 32,
    "." * 32,
    "." * 32,
    "." * 32,
]
_LEAF_LIT = [".oO.", "oOiO", "yoOy", ".yy."]
_LEAF_MID = [".oo.", "oOoy", "yoyE"]
_LEAF_DARK = [".yy.", "yoyE", "EyEE"]
for _x, _y in ((12, 2), (7, 4), (17, 5), (3, 9), (10, 8), (15, 11), (6, 14), (21, 8)):
    _LAUREL = paste(_LAUREL, _LEAF_LIT, _x, _y)
for _x, _y in ((24, 11), (19, 15), (11, 17), (4, 18), (14, 21), (8, 22)):
    _LAUREL = paste(_LAUREL, _LEAF_MID, _x, _y)
for _x, _y in ((24, 17), (19, 21), (14, 25)):
    _LAUREL = paste(_LAUREL, _LEAF_DARK, _x, _y)
art("laurel", _LAUREL)

# A tall cabinet of scrolls in cubbyholes, red tags hanging (2x3).
_CUB_A = ["dddddd", "QPdQPd", "PpdPpd", "ddQPdd", "ddPpdd", "QPdQPd", "PpdPpd", "tddudd"]
_CUB_B = ["dddddd", "dQPdQP", "dPpdPp", "QPdQPd", "PpdPpd", "dQPddd", "dPpddd", "ddtddu"]


def _cubbies(a, b):
    return ["Dw" + w + "D" + x + "D" + y + "D" + z + "wdD" for w, x, y, z in zip(a, b, a, b)]


art("scroll_shelf", ["." * 32] * 4 + [
    "D" * 32,
    "Dv" + "v" * 27 + "wdD",
    "DW" + "W" * 27 + "wdD",
    "D" * 32,
] + _cubbies(_CUB_A, _CUB_B) + ["Dw" + "v" * 27 + "wdD"]
  + _cubbies(_CUB_B, _CUB_A) + ["Dw" + "v" * 27 + "wdD"]
  + _cubbies(_CUB_A, _CUB_B) + ["Dw" + "v" * 27 + "wdD"]
  + _cubbies(_CUB_B, _CUB_A) + [
    "D" * 32,
    "Dv" + "v" * 27 + "wdD",
    "Dw" + "w" * 27 + "wdD",
    "D" * 32,
    "." * 32,
])

# Daphne's writing desk: a scroll unrolled, ink, a reed pen, a wax tablet.
_DESK = TABLE
_DESK = paste(_DESK, ["LQQQQQQQQQQQL", "LQpppQppQpQQL", "LQQQQQQQQQQQL",
                      "LQppQpppQppQL", "LQQQQQQQQQQQL", "pLLLLLLLLLLLp"], 3, 9)
_DESK = paste(_DESK, [".D.", "D#D", "DDD"], 17, 9)
_DESK = paste(_DESK, ["v....", ".v...", "..v..", "...v."], 18, 12)
_DESK = paste(_DESK, ["wwwwwww", "wDdDdDw", "wDDDDDw", "wDdDdDw", "wDDDDDw", "wwwwwww"], 22, 9)
art("desk", _DESK)

# A plain four-legged stool (diphros).
art("stool", [
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
    "...DDDDDDDDDD...",
    "..DvvvvvvvvvvD..",
    "..DWWWWWWWWWwD..",
    "..DwwwwwwwwwdD..",
    "..DDDDDDDDDDDD..",
    "...DwD....DwD...",
    "...DwD....DwD...",
    "...DdD....DdD...",
    "..DDD......DDD..",
    "." * 16,
    "." * 16,
])

# Specimen jars on a marble shelf: a shell, a starfish, a beetle.
art("specimens", [
    "." * 16,
    "." * 16,
    "1" * 16,
    "1" + "8" * 13 + "61",
    "1" + "5" * 13 + "41",
    "1" * 16,
    "14" + "333333333333" + "31",
    "14" + "3bbbb33bbbb3" + "31",
    "14" + "3bFCb33bFCb3" + "31",
    "14" + "3bC7b33bCgb3" + "31",
    "14" + "3bc5b33bgGb3" + "31",
    "14" + "3bCcb33bccb3" + "31",
    "14" + "33bb3333bb33" + "31",
    "14" + "333333333333" + "31",
    "1" + "8" * 13 + "61",
    "1" + "5" * 13 + "41",
    "1" * 16,
    "14" + "333333333333" + "31",
    "14" + "3bbbbbb3bbb3" + "31",
    "14" + "3bFCCCb3bFb3" + "31",
    "14" + "3bC#CCb3bCb3" + "31",
    "14" + "3bCC#Cb3bcb3" + "31",
    "14" + "3bCCCcb3bcb3" + "31",
    "14" + "3bcccbb3bbb3" + "31",
    "14" + "33bbbb333333" + "31",
    "14" + "333333333333" + "31",
    "1" + "8" * 13 + "61",
    "1" + "5" * 13 + "41",
    "1" + "4" * 13 + "31",
    "1" * 16,
    "." * 16,
    "." * 16,
])

# A bronze armillary sphere on a tripod stand.
art("armillary", [
    "................",
    "......gggg......",
    "....gg.Zx.Gg....",
    "...g...Zx...G...",
    "..g....Zx....G..",
    "..gGGGGzzGGGGx..",
    ".g....zxxz....G.",
    ".g..ggzxxzGG..G.",
    ".gggg..zz...GGx.",
    "..g....Zx....G..",
    "..g....Zx....x..",
    "...g...Zx...x...",
    "....Gx.Zx.xZ....",
    "......GxxZ......",
    ".......Zx.......",
    ".......Zx.......",
    ".......Zx.......",
    "......ZgxZ......",
    ".......Zx.......",
    ".......Zx.......",
    ".......Zx.......",
    ".......Zx.......",
    "......ZZxZ......",
    ".....ZxZZxZ.....",
    "....Zx.Zx.xZ....",
    "...Zx..Zx..xZ...",
    "..Zx...Zx...xZ..",
    ".ZZ...ZZxZ...ZZ.",
    "." * 16,
    "." * 16,
    "." * 16,
    "." * 16,
])

# A painted map of Aethos. Kalliste is the speck by the arrow, bottom left.
_MAP = [
    "cccccccccccc777777777777",
    "ccccccCcccc7777777777777",
    "cccccccccc77777777777757",
    "cccCccccc777777777777757",
    "ccccccccc777777557777777",
    "cccccc7cc7777775cc577777",
    "ccccc777cc77777cccc57777",
    "cccccc75cccc777cccc77777",
    "ccCccccccccccc77ccc77777",
    "ccccccccc77ccccccc777757",
    "cccccccc7775cccccc777777",
    "ccccccccc75cccCccc777777",
    "cccCccccccccccccc7777777",
    "cccccccccccc77ccc7777757",
    "ccccccccccc7775cccc77777",
    "ccccCcccccc7775ccccc7777",
    "cccccccccccc75ccCcccc777",
    "c##ccccccccccccccccccc77",
    "cc##c77cccccccCcccccccc7",
    "ccc#7G75cccccccccccccccc",
    "cccc7775cccccccccccccccc",
    "ccccc55ccccccCcccccccccc",
]
art("wall_map", ["." * 32] * 2 + [
    "." + "1" * 30 + ".",
    ".15" + "5" * 26 + "31.",
    ".15" + "1" * 26 + "31.",
] + [".151" + r + "131." for r in _MAP] + [
    ".15" + "1" * 26 + "31.",
    ".13" + "3" * 26 + "31.",
    "." + "1" * 30 + ".",
    "." * 32,
    "." * 32,
])

# The starters' kraters: painted black-figure bowls, one per starter. Each
# is laid on a middle cell of the long marble table.
KRATER = [
    "..RRRRRRRRRR..",
    ".RU########tR.",
    "RUu########tTR",
    "RUuuuuuuuuttTR",
    ".RRRRRRRRRRRR.",
    "..RuuuuuuttR..",
    "RRR########RRR",
    "R.R@@@@@@@@R.R",
    "RRR%%%%%%%%RRR",
    "..R########R..",
    "...RuuuttTR...",
    "....RttTTR....",
    "...RRRRRRRR...",
    "...RUuuttTR...",
]
# The band's two motif rows, and a recolor: a cream serpent on black for
# Snivy (it grows into Delphoi's python), flames for Cyndaquil, and for Piplup
# a white-ground krater with blue water inside and waves round the band.
KRATER_MOTIFS = {
    "snivy": ("#PP##PP#", "P##PP##P", {}),
    "cyndaquil": ("#rX##Xr#", "rXXrrXXr", {}),
    "piplup": ("##88##88", "#8##8##8",
               {"R": "1", "T": "3", "t": "4", "u": "6", "U": "7", "#": "B"}),
}

# The long table's front: a marble apron on two lion-paw legs (3 cells).
art("table_front", [
    "1" + "4" * 46 + "1",
    "1" + "2" * 46 + "1",
    "17" + "6" * 44 + "51",
    "17" + "5" * 44 + "41",
    "1" * 48,
] + [".17541" + "." * 36 + ".17541"] * 7 + [
    "117541" + "." * 36 + "117541",
    "177641" + "." * 36 + "177641",
    "111111" + "." * 36 + "111111",
    "." * 48,
])

# Alethea's worktable: potsherds laid out, a brush, a trowel, her notes.
_WORK = TABLE
for _piece, _x, _y in (
        (["RRR.", "RutR", ".RtR"], 4, 9),
        ([".RR", "RuR", "RtR", "RR."], 9, 10),
        (["RRRR", "R##R", "RuuR", ".RR."], 14, 9),
        (["RRR", "RUR", "RRR"], 6, 14),
        (["wvvvvDD"], 19, 15),
        (["wwwdDD", "...DDd"], 18, 10),
        (["QQQQ", "QppQ", "QQQQ"], 25, 9)):
    _WORK = paste(_WORK, _piece, _x, _y)
art("worktable", _WORK)

# A crate of finds with potsherds sticking out.
art("crate", [
    "................",
    "......Rt........",
    "....RuuR.Ru.....",
    "...RutRRRtuR....",
    "..DDDDDDDDDDDD..",
    "..DvvvvvvvvvwD..",
    "..DWWWWWWWWWwD..",
    "..DwwwwwwwwwdD..",
    "..DDDDDDDDDDDD..",
    "..DWWWWWWWWWwD..",
    "..DwwwwwwwwwdD..",
    "..DDDDDDDDDDDD..",
    "..DWWWWWWWWWwD..",
    "..DwwwwwwwwwdD..",
    "..DDDDDDDDDDDD..",
    "................",
])

# A marble head, broken from its statue, face up on the floor.
art("marble_head", [
    "................",
    "................",
    "................",
    "......1111......",
    "....11333311....",
    "...1353353531...",
    "...1335353331...",
    "..13577777531...",
    "..15717717751...",
    "..15777577751...",
    "..13777577631...",
    "...157117651....",
    "...135776531....",
    "....135531......",
    "....131131......",
    "...33333333.....",
])

# A pick and a brush, laid down for the day.
art("dig_tools", [
    "................",
    "................",
    "........DDD.....",
    ".......DddDDD...",
    "......DdDD..DD..",
    ".....DWD......D.",
    "....DWD.........",
    "...DWD..........",
    "..DWD...........",
    ".DWD......DDDDD.",
    ".DD......DvvvwD.",
    ".........DDDDDD.",
    "................",
    "................",
    "................",
    "................",
])
