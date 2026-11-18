#!/usr/bin/env python3
"""Rough placement mockups for design/AWE_PASS.md: paint colossi, zones and
sight lines over the current renders, at true metatile scale.

  /usr/bin/python3 tools/ichor/art/awe_pass_mockups.py

Reads build/render/awe/<Map>.png (render each with tools/ichor/render_map.py
first) and writes design/art/awe_pass/*.png. The figures are blocking shapes
for size and position, not tile art.
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "build/render/awe"
OUT = ROOT / "design/art/awe_pass"
M = 16  # px per metatile at render scale 1

BRONZE = (178, 116, 58)
BRONZE_D = (112, 68, 36)
BRONZE_L = (230, 176, 102)
MARBLE = (238, 234, 222)
MARBLE_D = (176, 170, 160)
GOLD = (236, 196, 76)
GOLD_D = (168, 126, 40)
INK = (34, 24, 18)
LIME = (214, 204, 178)
LIME_D = (150, 140, 118)
BASALT = (58, 52, 56)
BASALT_L = (96, 88, 92)
LAVA = (250, 110, 30)
WHITE = (250, 250, 246)
RED = (196, 60, 40)
NOTE = (255, 236, 90)


def font(size):
    for p in ("/System/Library/Fonts/HelveticaNeue.ttc", "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()


def render(map_name):
    p = SRC / f"{map_name}.png"
    if not p.exists():
        lay = __import__("json").loads((ROOT / f"data/maps/{map_name}/map.json").read_text())["layout"]
        subprocess.run([sys.executable, str(ROOT / "tools/ichor/render_map.py"), lay, "-o", str(p)], check=True)
    return Image.open(p).convert("RGBA")


class Canvas:
    """Draw in metatile coordinates on a 1x render, then upscale for labels."""

    def __init__(self, base, top_pad=0):
        w, h = base.size
        self.img = Image.new("RGB", (w, h + top_pad * M), (150, 186, 220))
        self.img.paste(base.convert("RGB"), (0, top_pad * M))
        self.oy = top_pad
        self.d = ImageDraw.Draw(self.img, "RGBA")
        self.labels = []  # drawn after upscale

    def p(self, x, y):
        return (round(x * M), round((y + self.oy) * M))

    def rect(self, x0, y0, x1, y1, fill, outline=INK, width=1):
        self.d.rectangle([*self.p(x0, y0), self.p(x1, y1)[0] - 1, self.p(x1, y1)[1] - 1], fill=fill, outline=outline, width=width)

    def poly(self, pts, fill, outline=INK):
        self.d.polygon([self.p(x, y) for x, y in pts], fill=fill, outline=outline)

    def ellipse(self, x0, y0, x1, y1, fill, outline=INK):
        self.d.ellipse([*self.p(x0, y0), *self.p(x1, y1)], fill=fill, outline=outline)

    def line(self, pts, fill, width=2):
        self.d.line([self.p(x, y) for x, y in pts], fill=fill, width=width)

    def zone(self, x0, y0, x1, y1, color, label=None):
        self.rect(x0, y0, x1, y1, (*color, 70), outline=(*color, 255), width=2)
        if label:
            self.labels.append((x0 + 0.2, y0 + 0.15, label, color))

    def screen(self, x, y, label):
        """The 15x10 play screen with its top-left at metatile (x, y)."""
        for i in range(0, 3):
            self.d.rectangle([self.p(x, y)[0] - i, self.p(x, y)[1] - i, self.p(x + 15, y + 10)[0] + i, self.p(x + 15, y + 10)[1] + i], outline=(255, 255, 255, 230))
        self.labels.append((x + 0.2, y + 10 - 0.9, label, (255, 255, 255)))

    def arrow(self, pts, color=(255, 255, 255), label=None):
        for a, b in zip(pts, pts[1:]):
            n = 24
            for i in range(0, n, 2):
                t0, t1 = i / n, (i + 1) / n
                self.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], (*color, 255), 3)
        (ax, ay), (bx, by) = pts[-2], pts[-1]
        import math
        ang = math.atan2(by - ay, bx - ax)
        tip = (bx, by)
        l, s = 0.8, 0.45
        self.poly([tip, (bx - l * math.cos(ang) + s * math.sin(ang), by - l * math.sin(ang) - s * math.cos(ang)),
                   (bx - l * math.cos(ang) - s * math.sin(ang), by - l * math.sin(ang) + s * math.cos(ang))], (*color, 255), outline=INK)
        if label:
            self.labels.append((pts[0][0] + 0.3, pts[0][1] - 0.9, label, color))

    def note(self, x, y, text, color=NOTE):
        self.labels.append((x, y, text, color))

    def grid(self, x0, y0, x1, y1):
        for x in range(x0, x1 + 1):
            self.line([(x, y0), (x, y1)], (255, 255, 255, 60), 1)
        for y in range(y0, y1 + 1):
            self.line([(x0, y), (x1, y)], (255, 255, 255, 60), 1)

    def save(self, name, title, scale=2):
        big = self.img.resize((self.img.width * scale, self.img.height * scale), Image.NEAREST)
        bar = 54
        out = Image.new("RGB", (big.width, big.height + bar), (20, 22, 32))
        out.paste(big, (0, bar))
        d = ImageDraw.Draw(out, "RGBA")
        d.text((12, 10), title, font=font(26), fill=WHITE)
        f = font(17)
        for x, y, text, color in self.labels:
            px, py = round(x * M * scale), round((y + self.oy) * M * scale) + bar
            for i, line in enumerate(text.split("\n")):
                bb = d.textbbox((px, py + i * 21), line, font=f)
                d.rectangle([bb[0] - 4, bb[1] - 2, bb[2] + 4, bb[3] + 2], fill=(10, 10, 16, 200))
                d.text((px, py + i * 21), line, font=f, fill=color)
        OUT.mkdir(parents=True, exist_ok=True)
        out.convert("RGB").save(OUT / name)
        print(OUT / name, out.size)


# --- figures ---------------------------------------------------------------

def promachos(c, x, y, metal=BRONZE, dark=BRONZE_D, light=BRONZE_L):
    """Athena Promachos, 4 wide x 9 tall metatiles; (x, y) is the plinth's top-left."""
    c.rect(x + 0.5, y + 7.6, x + 3.5, y + 9, LIME, outline=INK)          # plinth
    c.rect(x + 0.5, y + 7.6, x + 3.5, y + 7.9, LIME_D, outline=None)
    c.poly([(x + 1.2, y + 7.6), (x + 1.5, y + 4.6), (x + 2.5, y + 4.6), (x + 2.8, y + 7.6)], metal)  # peplos
    c.poly([(x + 1.95, y + 4.8), (x + 2.05, y + 4.8), (x + 2.25, y + 7.6), (x + 1.75, y + 7.6)], dark, outline=None)
    c.rect(x + 1.45, y + 3.2, x + 2.55, y + 4.8, metal)                    # torso
    c.rect(x + 1.55, y + 3.3, x + 1.8, y + 4.7, light, outline=None)
    c.ellipse(x + 1.55, y + 2.35, x + 2.45, y + 3.3, metal)                 # head
    c.poly([(x + 1.5, y + 2.6), (x + 2.0, y + 1.7), (x + 2.6, y + 2.0), (x + 2.5, y + 2.6)], light)  # helmet + crest
    c.ellipse(x + 0.3, y + 3.6, x + 1.6, y + 5.6, dark)                     # shield
    c.ellipse(x + 0.65, y + 4.1, x + 1.25, y + 5.1, light, outline=None)
    c.poly([(x + 2.5, y + 3.4), (x + 3.3, y + 2.9), (x + 3.45, y + 3.15), (x + 2.6, y + 3.8)], metal)  # spear arm
    c.line([(x + 3.35, y + 8.0), (x + 3.35, y - 0.2)], INK, 3)              # spear
    c.poly([(x + 3.2, y - 0.2), (x + 3.35, y - 1.0), (x + 3.5, y - 0.2)], GOLD)  # the gleaming tip


def parthenon(c, x, y, w=12, h=7):
    c.rect(x, y + h - 1, x + w, y + h, LIME_D)                              # krepis
    c.rect(x + 0.3, y + h - 1.5, x + w - 0.3, y + h - 1, LIME)
    c.rect(x + 0.5, y + 1.6, x + w - 0.5, y + h - 1.5, MARBLE)
    for i in range(int((w - 1) / 0.75)):
        cx = x + 0.8 + i * 0.75
        c.rect(cx, y + 2.0, cx + 0.32, y + h - 1.6, MARBLE_D, outline=None)
    c.poly([(x + 0.2, y + 1.7), (x + w / 2, y + 0.2), (x + w - 0.2, y + 1.7)], MARBLE)  # pediment
    c.poly([(x + 1.4, y + 1.5), (x + w / 2, y + 0.55), (x + w - 1.4, y + 1.5)], (80, 112, 170), outline=None)
    c.rect(x + 0.2, y + 1.6, x + w - 0.2, y + 2.0, (196, 72, 52))           # painted frieze


def hermes(c, x, y):
    """Hermes Limenios striding on the mole, 5 wide x 9 tall; beacon fire in the caduceus."""
    c.rect(x, y + 7.4, x + 5, y + 9, LIME, outline=INK)                    # square plinth on the mole head
    c.rect(x, y + 7.4, x + 5, y + 7.8, LIME_D, outline=None)
    c.poly([(x + 1.4, y + 7.4), (x + 1.9, y + 5.2), (x + 2.4, y + 5.2), (x + 2.1, y + 7.4)], BRONZE)   # left leg
    c.poly([(x + 2.6, y + 5.2), (x + 3.1, y + 5.2), (x + 3.8, y + 7.4), (x + 3.2, y + 7.4)], BRONZE_D)  # right leg striding
    c.rect(x + 1.8, y + 3.4, x + 3.2, y + 5.3, BRONZE)                     # torso
    c.rect(x + 1.9, y + 3.5, x + 2.2, y + 5.2, BRONZE_L, outline=None)
    c.poly([(x + 1.6, y + 3.4), (x + 3.4, y + 3.4), (x + 3.6, y + 4.6), (x + 1.4, y + 4.4)], (60, 96, 150))  # chlamys
    c.ellipse(x + 2.05, y + 2.5, x + 2.95, y + 3.45, BRONZE)               # head
    c.poly([(x + 1.8, y + 2.75), (x + 3.2, y + 2.75), (x + 2.5, y + 2.25)], BRONZE_D)  # petasos
    c.poly([(x + 1.75, y + 2.6), (x + 1.3, y + 2.2), (x + 1.8, y + 2.45)], GOLD)       # wing
    c.poly([(x + 3.2, y + 3.6), (x + 4.0, y + 2.4), (x + 4.25, y + 2.6), (x + 3.4, y + 3.95)], BRONZE)  # raised arm
    c.line([(x + 4.15, y + 2.5), (x + 4.15, y + 0.6)], GOLD_D, 3)          # caduceus staff
    c.ellipse(x + 3.7, y - 0.4, x + 4.6, y + 0.8, LAVA, outline=GOLD)      # beacon fire
    c.ellipse(x + 3.95, y - 0.05, x + 4.35, y + 0.5, NOTE, outline=None)
    c.poly([(x + 1.8, y + 4.0), (x + 1.0, y + 5.2), (x + 1.25, y + 5.35), (x + 1.95, y + 4.4)], BRONZE)  # lowered arm, purse


def bronze_giant(c, x, y):
    """Kaldera's unfinished bronze man: 6 wide x 10 tall, scaffold on one side, a heel missing."""
    c.rect(x, y + 8.8, x + 6, y + 10, BASALT_L)                             # casting pit rim
    c.rect(x + 0.3, y + 9.1, x + 5.7, y + 10, LAVA, outline=None)
    c.poly([(x + 1.8, y + 8.9), (x + 2.2, y + 6.0), (x + 2.9, y + 6.0), (x + 2.7, y + 8.9)], BRONZE)
    c.poly([(x + 3.1, y + 6.0), (x + 3.8, y + 6.0), (x + 4.2, y + 8.3), (x + 3.5, y + 8.3)], BRONZE_D)  # the leg without a heel
    c.rect(x + 1.9, y + 3.2, x + 4.1, y + 6.1, BRONZE)
    c.line([(x + 3.0, y + 3.3), (x + 3.0, y + 8.6)], LAVA, 2)              # the one vein, neck to heel
    c.ellipse(x + 2.4, y + 1.9, x + 3.6, y + 3.3, BRONZE)
    c.rect(x + 2.6, y + 2.4, x + 3.4, y + 2.6, LAVA, outline=None)          # the eyes, not yet lit
    c.poly([(x + 1.9, y + 3.4), (x + 1.2, y + 5.8), (x + 1.6, y + 5.9), (x + 2.2, y + 4.0)], BRONZE)
    c.poly([(x + 4.1, y + 3.4), (x + 4.8, y + 5.8), (x + 4.4, y + 5.9), (x + 3.8, y + 4.0)], BRONZE_D)
    for i in range(6):                                                       # timber scaffold
        c.line([(x + 4.7, y + 1.5 + i * 1.5), (x + 6.0, y + 1.5 + i * 1.5)], (130, 92, 52), 2)
    c.line([(x + 4.8, y + 1.2), (x + 4.8, y + 9.0)], (130, 92, 52), 2)
    c.line([(x + 5.9, y + 1.2), (x + 5.9, y + 9.0)], (130, 92, 52), 2)


def seated_zeus(c, x, y):
    """Enthroned Zeus, gold and ivory, 10 wide x 11 tall metatiles."""
    c.rect(x, y + 9.6, x + 10, y + 11, MARBLE_D)                            # base
    c.rect(x + 0.4, y + 9.2, x + 9.6, y + 9.6, MARBLE)
    c.rect(x + 0.8, y + 1.0, x + 9.2, y + 9.2, (88, 58, 44))                # ebony throne back
    c.rect(x + 1.0, y + 1.2, x + 9.0, y + 1.7, GOLD, outline=None)
    c.rect(x + 0.6, y + 5.5, x + 1.8, y + 9.2, (88, 58, 44))                # arms of the throne
    c.rect(x + 8.2, y + 5.5, x + 9.4, y + 9.2, (88, 58, 44))
    c.poly([(x + 2.6, y + 6.0), (x + 7.4, y + 6.0), (x + 7.8, y + 9.2), (x + 2.2, y + 9.2)], GOLD)   # gold robe over the knees
    c.poly([(x + 3.0, y + 6.3), (x + 4.8, y + 6.3), (x + 4.6, y + 9.0), (x + 2.8, y + 9.0)], GOLD_D, outline=None)
    c.rect(x + 3.5, y + 3.2, x + 6.5, y + 6.2, MARBLE)                      # ivory torso
    c.rect(x + 3.7, y + 3.3, x + 4.2, y + 6.1, WHITE, outline=None)
    c.ellipse(x + 4.2, y + 1.6, x + 5.8, y + 3.4, MARBLE)                   # head
    c.poly([(x + 4.3, y + 2.6), (x + 5.7, y + 2.6), (x + 5.0, y + 3.9)], (232, 232, 236))  # beard
    c.poly([(x + 4.1, y + 1.9), (x + 5.0, y + 1.3), (x + 5.9, y + 1.9)], (90, 150, 70))    # olive wreath
    c.line([(x + 7.2, y + 0.4), (x + 7.2, y + 9.2)], GOLD_D, 3)            # sceptre
    c.ellipse(x + 6.9, y + 0.0, x + 7.5, y + 0.6, GOLD)
    c.ellipse(x + 2.3, y + 4.3, x + 3.5, y + 5.5, GOLD)                     # Nike in the right hand
    c.poly([(x + 6.5, y + 3.4), (x + 7.3, y + 4.6), (x + 7.0, y + 4.9), (x + 6.4, y + 4.0)], MARBLE)
    c.poly([(x + 3.5, y + 3.5), (x + 2.8, y + 4.8), (x + 3.1, y + 5.0), (x + 3.6, y + 4.1)], MARBLE)


def courtyard_block(c, x, y, w, h):
    c.rect(x, y, x + w, y + h, (226, 206, 170))
    c.rect(x + 0.6, y + 0.6, x + w - 0.6, y + h - 0.6, (196, 92, 56), outline=None)
    c.rect(x + w / 2 - 0.6, y + h / 2 - 0.6, x + w / 2 + 0.6, y + h / 2 + 0.6, (180, 176, 150), outline=None)


def stoa(c, x, y, w, h=2):
    c.rect(x, y, x + w, y + h, (190, 84, 52))
    c.rect(x, y + h - 0.7, x + w, y + h, MARBLE)
    for i in range(int(w / 0.8)):
        c.rect(x + 0.3 + i * 0.8, y + h - 0.65, x + 0.5 + i * 0.8, y + h - 0.05, MARBLE_D, outline=None)


# --- the five mockups --------------------------------------------------------

def mock_astyra():
    c = Canvas(render("Astyra"))
    c.img.paste((214, 196, 150), [0, 0, c.img.width, c.img.height])   # clear the placeholder grass to a plan
    # the Akropolis rock: a limestone mass across the north
    c.poly([(9, 1), (40, 1), (42, 6), (39, 13), (30, 15), (18, 15), (11, 12), (8, 7)], LIME, outline=INK)
    c.poly([(11, 12), (18, 15), (30, 15), (39, 13), (39, 14), (30, 16.2), (18, 16.2), (11, 13)], LIME_D, outline=None)
    parthenon(c, 24, 3, 12, 6)
    promachos(c, 17, 2)
    c.zone(12, 9, 17, 15.5, (255, 255, 255), "Propylaia ramp")
    # the agora, framed by stoas
    c.zone(13, 21, 35, 33, (236, 196, 76), "Agora (open; Panathenaic Way crosses it)")
    stoa(c, 13, 19, 22)
    stoa(c, 36, 21, 2, 12)
    c.note(13, 18.2, "Stoa of the Archon (north side)")
    c.rect(22, 26, 24, 28, (110, 150, 200))                                  # fountain house
    c.note(24.3, 26.4, "fountain house + herms")
    # asty blocks on the slopes
    for bx, by in [(2, 18), (2, 24), (2, 30), (8, 36), (14, 36), (40, 18), (40, 24), (40, 36), (34, 38), (28, 38)]:
        courtyard_block(c, bx, by, 5, 4)
    c.note(2, 17.2, "courtyard houses (asty)")
    c.zone(38, 26, 47, 34, (150, 200, 120), "Pnyx hill")
    c.zone(0, 38, 7, 48, (160, 130, 170), "Dipylon gate +\nKerameikos graves")
    c.zone(20, 40, 30, 48, (110, 150, 200), "harbor road\n(to Phaleron)")
    c.arrow([(4, 44), (12, 33), (16, 25), (15, 14)], (255, 255, 255), "Panathenaic Way")
    c.screen(17, 0, "reveal screen: spear tip over the rock")
    c.arrow([(25, 46), (25, 36), (24, 12)], NOTE, "first entry: camera pans up the Way")
    c.save("1_astyra_city.png", "AWE 1 - Astyra: the Akropolis and Athena Promachos over the capital (48x48, plan)")


def mock_akropolis():
    c = Canvas(render("Astyra_Akropolis"))
    c.img.paste((60, 92, 58), [0, 0, c.img.width, c.img.height])
    # the rock: top plateau and cliff skirts
    c.poly([(3, 2), (31, 2), (32, 26), (27, 30), (7, 30), (2, 26)], LIME, outline=INK)
    c.poly([(2, 26), (7, 30), (27, 30), (32, 26), (32, 28), (27, 33), (7, 33), (2, 28)], LIME_D, outline=None)
    parthenon(c, 16, 4, 14, 8)
    c.note(16, 12.2, "Parthenon: 14x8, krepis of 3 steps")
    promachos(c, 9, 13)
    c.note(5, 22.4, "Athena Promachos 4x9\n(bronze; spear tip gleams)")
    c.rect(4, 4, 10, 9, MARBLE)                                              # Erechtheion
    for i in range(3):
        c.rect(4.4 + i * 0.9, 7.5, 4.9 + i * 0.9, 9, (220, 200, 170), outline=INK)
    c.note(3, 3.1, "Erechtheion + Karyatid porch")
    c.ellipse(10.5, 5.5, 13, 8, (90, 140, 70))
    c.note(10.2, 8.3, "Athena's olive")
    c.zone(18, 16, 30, 24, (150, 140, 118), "Old Temple foundations\n(ruins kit)")
    c.rect(10, 26, 24, 30, MARBLE)                                           # Propylaia
    for i in range(6):
        c.rect(11 + i * 2.2, 27, 11.6 + i * 2.2, 30, MARBLE_D, outline=None)
    c.note(10.2, 30.3, "Propylaia (5 doors, 2 wings)")
    # the ramp, switchbacks below the rock
    c.zone(4, 34, 30, 51, (200, 170, 120), None)
    c.arrow([(17, 51), (27, 47), (8, 42), (26, 37), (17, 31)], (255, 255, 255), "ramp: 3 switchbacks = Titan checkpoints")
    c.screen(6, 16, "reveal: through the Propylaia")
    c.save("2_astyra_akropolis.png", "AWE 2 - The Akropolis: Propylaia, Promachos, Parthenon (34x52, plan)")


def mock_kaldera():
    c = Canvas(render("Kaldera"))
    c.img.paste((40, 96, 160), [0, 0, c.img.width, c.img.height])      # the flooded caldera
    # the ring of cliffs, open to the west
    ring = [(14, 0), (40, 0), (40, 40), (14, 40), (14, 34), (24, 33), (31, 28), (33, 20), (31, 12), (24, 7), (14, 6)]
    c.poly(ring, BASALT, outline=INK)
    c.poly([(14, 6), (24, 7), (31, 12), (33, 20), (31, 28), (24, 33), (14, 34), (14, 32), (23, 31), (29, 27), (31, 20), (29, 13), (23, 9), (14, 8)], (180, 90, 60), outline=None)  # red-and-white bands
    c.poly([(0, 0), (12, 0), (12, 4), (3, 7), (0, 6)], BASALT)
    c.poly([(0, 40), (12, 40), (12, 36), (3, 33), (0, 34)], BASALT)
    # the white town on the rim
    for i, (bx, by) in enumerate([(33, 2), (36, 4), (34, 7), (37, 10), (35, 14), (38, 17), (36, 23), (38, 27), (35, 31), (37, 35)]):
        c.rect(bx, by, bx + 2.4, by + 2, WHITE)
        if i % 3 == 0:
            c.ellipse(bx + 0.6, by - 0.6, bx + 1.8, by + 0.6, (60, 100, 200))
    c.note(32.5, 0.2, "white town on the rim")
    c.arrow([(33, 30), (30, 31.5), (32, 33), (28, 35)], (255, 255, 255), None)
    c.note(25.5, 35.3, "switchback stair to the port")
    c.zone(22, 34, 30, 39, (220, 220, 220), "black-sand port")
    # Nea Kameni: the islet with the casting pit
    c.poly([(8, 13), (16, 11), (21, 15), (21, 25), (16, 29), (8, 27), (5, 20)], BASALT_L, outline=INK)
    bronze_giant(c, 10, 13)
    c.note(5.2, 28.4, "the islet: casting pit + bronze giant 6x10\n(seams and eyes animate)")
    c.rect(14, 23, 16, 25, (20, 14, 12))
    c.note(16.3, 23.6, "forge mouth")
    c.arrow([(0.5, 20), (4.5, 20)], NOTE, "trireme in")
    c.screen(1, 13, "reveal: sailing in, giant against the cliff")
    c.save("3_kaldera.png", "AWE 3 - Kaldera: the caldera, the rim town and the bronze giant (40x40, plan)")


def mock_emporion_harbor():
    c = Canvas(render("EmporionHarbor"))
    c.rect(40.5, 15, 47.5, 25.5, LIME)                               # widen the mole head into a platform
    hermes(c, 41.5, 15.6)
    c.note(31.0, 13.6, "Hermes Limenios 5x9\non the mole head; beacon\nfire in the caduceus (anim)")
    c.arrow([(23, 1), (23, 6), (38, 12)], NOTE, "from the city road: pan east")
    c.arrow([(17, 24.5), (30, 21)], (255, 255, 255), "trireme berth")
    c.screen(29, 14, "dock screen: the statue fills the right third")
    c.zone(0.5, 10.8, 15.5, 14.2, (110, 150, 200), "ship sheds (keep)")
    c.save("4_emporion_harbor.png", "AWE 4 - Emporion Harbor: the harbor colossus on the mole (48x26)")


def mock_summit():
    pad = 12
    c = Canvas(render("Olympus_Summit"), top_pad=pad)
    c.img.paste((150, 186, 228), [0, 0, c.img.width, pad * M])
    for i in range(0, 28, 3):                                                # cloud bank behind
        c.ellipse(i - 1, -2.8, i + 4, -0.4, (240, 244, 250))
    c.poly([(4, 0.2), (8, -9), (20, -9), (24, 0.2)], (200, 210, 226), outline=INK)  # the summit cone cut as a niche
    seated_zeus(c, 9, -10.6)
    c.note(0.3, -11.6, "proposal: +12 rows north. Enthroned Zeus 10x11\n(gold and ivory), cut into the summit cone")
    c.note(0.3, -6.0, "post-game: the throne\nempties (Olympanax wakes)")
    c.arrow([(14, 25), (14, 12), (14, 1)], NOTE, "the climb up the stair")
    c.screen(6, 2 - pad + 4, "reveal: the stair crest frames him over the temple")
    c.save("5_olympus_summit.png", "AWE 5 - Olympus Summit: Zeus enthroned (28x38 proposed)")


if __name__ == "__main__":
    mock_astyra()
    mock_akropolis()
    mock_kaldera()
    mock_emporion_harbor()
    mock_summit()
