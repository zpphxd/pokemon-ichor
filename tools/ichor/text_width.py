#!/usr/bin/env python3
"""Measure Gen 3 text in pixels, with the game's own proportional font widths.

The widths come from src/fonts.c (gFont*LatinGlyphWidths) and the encoding from
charmap.txt, so the numbers match GetStringWidth for plain text. Line breaks are
\\n, \\l and \\p. Placeholders take sample text (--var); other {CODES} are taken
as zero width, except key and symbol icons, which are estimated.

  tools/ichor/text_width.py "Welcome to the Asclepeion."
  tools/ichor/text_width.py --font short --max 120 "AUGUR'S EYE"
  tools/ichor/text_width.py --var STR_VAR_1=POTION "{STR_VAR_1} is selected."
  tools/ichor/text_width.py --scan data/text/save.inc --max 216

--scan lists every string in a .c or .inc file and flags lines wider than --max.
The default --max, 216, is the field message box (27 tiles). Battle messages
wrap themselves at 208 (BATTLE_MSG_MAX_WIDTH).
"""
import argparse
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
FONTS = {
    "normal": "gFontNormalLatinGlyphWidths",
    "short": "gFontShortLatinGlyphWidths",
    "small": "gFontSmallLatinGlyphWidths",
    "narrow": "gFontNarrowLatinGlyphWidths",
    "small_narrow": "gFontSmallNarrowLatinGlyphWidths",
    "narrower": "gFontNarrowerLatinGlyphWidths",
}
# Worst-case-ish samples: names are up to 7 characters (PLAYER_NAME_LENGTH).
DEFAULT_VARS = {
    "PLAYER": "IANTHEX",
    "RIVAL": "KLEON",
    "STR_VAR_1": "XXXXXXXXXX",
    "STR_VAR_2": "XXXXXXXXXX",
    "STR_VAR_3": "XXXXXXXXXX",
    "KUN": "",
    "PKMN": None,  # real glyphs, measured from the charmap
}
ICON_WIDTH = {"F8": 12, "F9": 9}  # keypad icons and extra symbols, estimated


def load_charmap():
    chars, codes = {}, {}
    with open(os.path.join(ROOT, "charmap.txt"), encoding="utf-8") as f:
        for line in f:
            line = line.split("@")[0].rstrip()
            m = re.match(r"^'(\\?.)'\s*=\s*([0-9A-Fa-f ]+)$", line)
            if m:
                ch = m.group(1).replace("\\'", "'")
                chars.setdefault(ch, m.group(2).split())
                continue
            m = re.match(r"^([A-Z0-9_]+)\s*=\s*([0-9A-Fa-f ]+)$", line)
            if m:
                codes[m.group(1)] = m.group(2).split()
    return chars, codes


def load_widths(array):
    src = open(os.path.join(ROOT, "src", "fonts.c"), encoding="utf-8").read()
    m = re.search(re.escape(array) + r"\[\]\s*=\s*\{(.*?)\};", src, re.S)
    if not m:
        sys.exit(f"{array} not found in src/fonts.c")
    return [int(x) for x in re.findall(r"\d+", m.group(1))]


def measure_lines(text, font, chars, codes, variables):
    """Return [(line_text, width)] for each line of a game string."""
    widths = load_widths(FONTS[font])
    lines, cur, w = [], [], 0

    def add_text(s):
        nonlocal w
        for ch in s:
            b = chars.get(ch)
            if b is None:
                print(f"  warning: no glyph for {ch!r}", file=sys.stderr)
                continue
            w += widths[int(b[0], 16)]

    i = 0
    while i < len(text):
        c = text[i]
        if c == "\\" and i + 1 < len(text) and text[i + 1] in "nlp":
            lines.append(("".join(cur), w))
            cur, w = [], 0
            i += 2
            continue
        if c == "{":
            j = text.index("}", i)
            code = text[i + 1:j].split()[0]
            cur.append(text[i:j + 1])
            if code in variables and variables[code] is not None:
                add_text(variables[code])
            elif code in codes:
                b = codes[code]
                if b[0] in ICON_WIDTH:
                    w += ICON_WIDTH[b[0]]
                elif b[0] not in ("FC", "FD"):
                    for byte in b:
                        w += widths[int(byte, 16)]
            i = j + 1
            continue
        cur.append(c)
        add_text(c)
        i += 1
    lines.append(("".join(cur), w))
    return lines


STRING_RE = re.compile(r'(?:_\(|COMPOUND_STRING\(|\.string\s)\s*"((?:[^"\\]|\\.)*)"')


def scan(path, font, maxw, chars, codes, variables):
    bad = 0
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            for m in STRING_RE.finditer(line):
                for text, w in measure_lines(m.group(1), font, chars, codes, variables):
                    if w > maxw:
                        bad += 1
                        print(f"{path}:{n}: {w}px > {maxw}: {text}")
    print(f"{bad} line(s) wider than {maxw}px")
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("text", nargs="*")
    ap.add_argument("--font", default="normal", choices=sorted(FONTS))
    ap.add_argument("--max", type=int, default=216)
    ap.add_argument("--var", action="append", default=[], help="NAME=sample text")
    ap.add_argument("--scan", help="a .c or .inc file to check")
    a = ap.parse_args()
    chars, codes = load_charmap()
    variables = dict(DEFAULT_VARS)
    for v in a.var:
        k, _, val = v.partition("=")
        variables[k] = val
    if a.scan:
        sys.exit(1 if scan(a.scan, a.font, a.max, chars, codes, variables) else 0)
    over = False
    for text in a.text:
        for line, w in measure_lines(text, a.font, chars, codes, variables):
            flag = "  TOO WIDE" if w > a.max else ""
            over |= w > a.max
            print(f"{w:4d}px  {line}{flag}")
    sys.exit(1 if over else 0)


if __name__ == "__main__":
    main()
