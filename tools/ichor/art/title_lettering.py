"""Lettering for the title screen, as character grids.

ICHOR is cut like a gilded inscription in black stone: each stroke is a V-groove.
Light comes from the top left, so the groove's left/top wall is in shadow and
its right/bottom wall catches the light. The letterforms are Greek lapidary
capitals with small wedge apices at the stroke ends; C is the lunate sigma.

ICHOR legend (shaded by hand, one char per pixel):
  .  background (transparent)
  d  deep edge of the shadow wall
  s  shadow wall
  m  where the two walls turn (curves and diagonals)
  l  lit wall
  g  glint on the lit edge

The smaller lines (POKEMON, PRESS START) are masks ('#'); title_screen.py cuts
the same V into them with shade_thin(): left/top pixels shadow, the rest lit.
The creator credit is a plain painted mask.
"""

ICHOR = {
    "I": [
        "ddddddddmg",
        ".sssssmlg.",
        "..dssmlg..",
    ] + ["..dssllg.."] * 26 + [
        "..dsmllg..",
        ".dsmlllll.",
        "dmgggggggg",
    ],
    "C": [
        "...........ddddddd.........",
        "........dddsssssssddm......",
        ".......dsssssssssssmmm.....",
        ".....ddssssllllllmmmmmmm...",
        "....dssssllllgggmmmmmmmmm..",
        "....dssslllgg...mmmmmmmlg..",
        "...dsssllgg.......mmmmlllg.",
        "..dsssllg...........mmllg..",
        "..dsslllg...........mmlg...",
        ".dsssllg.............gg....",
        ".dssllg....................",
        ".dssllg....................",
        "dssllg.....................",
        "dssllg.....................",
        "dssllg.....................",
        "dssllg.....................",
        "dssllg.....................",
        "dssllg.....................",
        "dssllg.....................",
        "dsmllg.....................",
        ".dsmmmm....................",
        ".dsmmmm....................",
        ".dmmmmmm.............dd....",
        "..mmmmmmm...........dssm...",
        "..mmmmmmm...........dssmm..",
        "...mmmmmmmm.......ddssmllg.",
        "....mmmmmmmmm...ddssssllg..",
        "....mmmmmmmmmdddssssllllg..",
        ".....mmmmmmmssssssllllgg...",
        ".......mmmlllllllllllg.....",
        "........mgglllllllggg......",
        "...........ggggggg.........",
    ],
    "H": [
        "ddddddddmg..........ddddddddmg",
        ".sssssmlg............sssssmlg.",
        "..dssmlg..............dssmlg..",
    ] + ["..dssllg..............dssllg.."] * 10 + [
        "..dssmmmddddddddddddddsssllg..",
        "..dsssmmsssssssssssssssssllg..",
        "..dsssmmsssssssssssssssssllg..",
        "..dssmllllllllllllllllmmlllg..",
        "..dsslllllllllllllllllmmlllg..",
        "..dsslllggggggggggggggmmmllg..",
    ] + ["..dssllg..............dssllg.."] * 10 + [
        "..dsmllg..............dsmllg..",
        ".dsmlllll............dsmlllll.",
        "dmgggggggg..........dmgggggggg",
    ],
    "O": [
        "...........dddddddd...........",
        ".........ddsssssssmmm.........",
        ".......ddsssssssssmmmmm.......",
        "......dssssllllllllmmmmm......",
        ".....dssslllllgglllmmmmmm.....",
        "....dssslllggg..ggmmmmmmmm....",
        "...dssslllg........mmmmmmmm...",
        "..dssslllg..........mmmmmmmm..",
        "..dsslllg............mmmmmmm..",
        ".dsssllg..............mmmmmmg.",
        ".dssllg................mssmlg.",
        ".dssllg................dssllg.",
        "dsssllg................dsssllg",
        "dssllg..................dssllg",
        "dssllg..................dssllg",
        "dssllg..................dssllg",
        "dssllg..................dssllg",
        "dssllg..................dssllg",
        "dssllg..................dssllg",
        "dsslllg................dsslllg",
        ".dssllg................dssllg.",
        ".dsmllm................dssllg.",
        ".dmmmmmm..............dsslllg.",
        "..mmmmmmm............dsssllg..",
        "..mmmmmmmm..........dssslllg..",
        "...mmmmmmmm........dssslllg...",
        "....mmmmmmmmdd..dddssslllg....",
        ".....mmmmmmsssddssssslllg.....",
        "......mmmmmssssssssllllg......",
        ".......mmmmmlllllllllgg.......",
        ".........mmmlllllllgg.........",
        "...........gggggggg...........",
    ],
    "R": [
        "ddddddddddddddd..........",
        ".ssssssssssssssddm.......",
        "..dssssssssmmmsssmm......",
        "..dsssmlllllllmmmmmm.....",
        "..dssmllllllggmmmmmmm....",
        "..dsslllgggg..mmmmmmmm...",
        "..dssllg.......mmssmlg...",
        "..dssllg........dssllg...",
        "..dssllg........dssllg...",
        "..dssllg........dsslllg..",
        "..dssllg........dssllg...",
        "..dssllg........dssllg...",
        "..dssmmm.......dsslllg...",
        "..dssmmmmddddddsslllg....",
        "..dsssmmmsssssssllllg....",
        "..dsssmmmsssssmlllgg.....",
        "..dssmllllmssmlllg.......",
        "..dsslllllmmmlllg........",
        "..dsslllggmmmlllg........",
        "..dssllg..mmmmllg........",
        "..dssllg...mmmmlmm.......",
        "..dssllg...mmmmmmmm......",
        "..dssllg....mmmmmmmm.....",
        "..dssllg.....mmmmmmm.....",
        "..dssllg......mmmmmmm....",
        "..dssllg......mmmmmmmm...",
        "..dssllg.......mmmmmmm...",
        "..dssllg........mmmmmmm..",
        "..dsmllg........mmmmmmmm.",
        "..dsmllg.........dmmllllg",
        ".dmmlllll........mmlllllg",
        "dmgggggggg......mmggggggg",
    ],
}

# POKEMON, 9 px capitals with 2 px strokes. The acute sits over the E.
POKEMON = {
    "P": [
        "######.",
        "##..###",
        "##...##",
        "##..###",
        "######.",
        "##.....",
        "##.....",
        "##.....",
        "##.....",
    ],
    "O": [
        ".######.",
        "###..###",
        "##....##",
        "##....##",
        "##....##",
        "##....##",
        "##....##",
        "###..###",
        ".######.",
    ],
    "K": [
        "##...###",
        "##..###.",
        "##.###..",
        "#####...",
        "####....",
        "#####...",
        "##.###..",
        "##..###.",
        "##...###",
    ],
    "E": [
        "######",
        "##....",
        "##....",
        "##....",
        "#####.",
        "##....",
        "##....",
        "##....",
        "######",
    ],
    "M": [
        "##......##",
        "###....###",
        "####..####",
        "##.####.##",
        "##..##..##",
        "##......##",
        "##......##",
        "##......##",
        "##......##",
    ],
    "N": [
        "##....##",
        "###...##",
        "####..##",
        "##.##.##",
        "##..####",
        "##...###",
        "##....##",
        "##....##",
        "##....##",
    ],
}
ACUTE = [
    "..##",
    ".##.",
]

# PRESS START, 7 px capitals with 2 px stems, and the interpunct inscriptions
# used between words.
PRESS = {
    "P": ["#####.", "##..##", "##..##", "#####.", "##....", "##....", "##...."],
    "R": ["#####.", "##..##", "##..##", "#####.", "##.##.", "##..##", "##..##"],
    "E": ["#####", "##...", "##...", "####.", "##...", "##...", "#####"],
    "S": [".####.", "##..##", "##....", ".####.", "....##", "##..##", ".####."],
    "T": ["######", "..##..", "..##..", "..##..", "..##..", "..##..", "..##.."],
    "A": ["..##..", ".####.", "##..##", "##..##", "######", "##..##", "##..##"],
    "·": ["..", "..", "##", "##", "..", "..", ".."],
    " ": ["...", "...", "...", "...", "...", "...", "..."],
}

# Painted name labels in the field, as on the Francois Vase: KLOTHO, LACHESIS
# and ATROPOS in 5 px Greek capitals ('#' is black gloss).
GREEK = {
    "Α": [".#.", "#.#", "###", "#.#", "#.#"],
    "Ε": ["###", "#..", "##.", "#..", "###"],
    "Θ": [".###.", "#...#", "#.#.#", "#...#", ".###."],
    "Ι": ["#", "#", "#", "#", "#"],
    "Κ": ["#..#", "#.#.", "##..", "#.#.", "#..#"],
    "Λ": ["..#..", ".#.#.", ".#.#.", "#...#", "#...#"],
    "Ο": [".##.", "#..#", "#..#", "#..#", ".##."],
    "Π": ["####", "#..#", "#..#", "#..#", "#..#"],
    "Ρ": ["###.", "#..#", "###.", "#...", "#..."],
    "Σ": ["####", ".#..", "..#.", ".#..", "####"],
    "Τ": ["###", ".#.", ".#.", ".#.", ".#."],
    "Χ": ["#...#", ".#.#.", "..#..", ".#.#.", "#...#"],
    "Ω": [".###.", "#...#", "#...#", ".#.#.", "##.##"],
}

# The creator credit, 5 px capitals, 1 px strokes.
SMALL = {
    "A": [".#.", "#.#", "###", "#.#", "#.#"],
    "B": ["###.", "#..#", "###.", "#..#", "###."],
    "C": [".##", "#..", "#..", "#..", ".##"],
    "D": ["###.", "#..#", "#..#", "#..#", "###."],
    "E": ["###", "#..", "##.", "#..", "###"],
    "F": ["###", "#..", "##.", "#..", "#.."],
    "G": [".###", "#...", "#.##", "#..#", ".###"],
    "H": ["#..#", "#..#", "####", "#..#", "#..#"],
    "I": ["###", ".#.", ".#.", ".#.", "###"],
    "L": ["#..", "#..", "#..", "#..", "###"],
    "M": ["#...#", "##.##", "#.#.#", "#...#", "#...#"],
    "N": ["#..#", "##.#", "#.##", "#..#", "#..#"],
    "W": ["#...#", "#...#", "#.#.#", "#.#.#", ".#.#."],
    "O": [".##.", "#..#", "#..#", "#..#", ".##."],
    "P": ["###.", "#..#", "###.", "#...", "#..."],
    "R": ["###.", "#..#", "###.", "#.#.", "#..#"],
    "S": [".##", "#..", ".#.", "..#", "##."],
    "U": ["#..#", "#..#", "#..#", "#..#", ".##."],
    "Y": ["#.#", "#.#", ".#.", ".#.", ".#."],
    "Z": ["###", "..#", ".#.", "#..", "###"],
    "K": ["#..#", "#.#.", "##..", "#.#.", "#..#"],
    "2": ["###.", "...#", ".##.", "#...", "####"],
    "0": [".##.", "#..#", "#..#", "#..#", ".##."],
    "6": [".##.", "#...", "###.", "#..#", ".##."],
    "·": [".", ".", "#", ".", "."],
    " ": ["..", "..", "..", "..", ".."],
}
