#!/usr/bin/env python3
"""The before/after sheet for Thyrsa's polish pass (Act II batch 2):
design/phase3/img/thyrsa_polish_before_after.png.

  /usr/bin/python3 tools/ichor/art/thyrsa_polish_sheet.py BEFORE_DIR [SMOKE_A SMOKE_B]

BEFORE_DIR holds batch 1's renders (ThyrsaCity.png, ThyrsaCity_MantoHouse.png,
ThyrsaCity_ActorHouse.png, all 2x), e.g. from `git show 07dddca155:design/phase3/img/...`.
The after side is design/phase3/img's current renders. SMOKE_A and SMOKE_B are two
in-game screenshots of Semele's chamber a smoke frame apart (thyrsa_city.sh's
semele.png and semele_smoke_b.png); the sheet crops the chamber out of each.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
IMG = ROOT / "design/phase3/img"
BG = (236, 228, 208)
INK = (40, 32, 32)
C = 32          # one map cell at 2x


def font(size):
    for f in ("/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf"):
        if Path(f).exists():
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def crop(im, x0, y0, x1, y1):
    return im.crop((x0 * C, y0 * C, x1 * C, y1 * C))


def pair(title, before, after, scale=1.0, note=""):
    if scale != 1.0:
        before = before.resize((int(before.width * scale), int(before.height * scale)), Image.NEAREST)
        after = after.resize((int(after.width * scale), int(after.height * scale)), Image.NEAREST)
    gap, head = 24, 44
    w = max(before.width + after.width + gap, int(font(22).getlength(title)) + 8)
    h = max(before.height, after.height) + head + (24 if note else 0)
    out = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(out)
    d.text((0, 4), title, fill=INK, font=font(22))
    d.text((0, head - 18), "batch 1", fill=(120, 96, 80), font=font(15))
    d.text((before.width + gap, head - 18), "polish pass", fill=(120, 96, 80), font=font(15))
    out.paste(before, (0, head))
    out.paste(after, (before.width + gap, head))
    if note:
        d.text((0, h - 20), note, fill=INK, font=font(15))
    return out


def stack(parts, pad=36):
    w = max(p.width for p in parts) + 2 * pad
    h = sum(p.height for p in parts) + pad * (len(parts) + 1)
    out = Image.new("RGB", (w, h), BG)
    y = pad
    for p in parts:
        out.paste(p, (pad, y))
        y += p.height + pad
    return out


ROOMS = [
    ("Eleutherai_WatchHouse", "Eleutherai: the watch-house"), ("Eleutherai_OinoeHouse", "Eleutherai: Oinoe's house"),
    ("Eleutherai_LysidikeHouse", "Eleutherai: Lysidike's house"), ("ThyrsaCity_Asclepeion", "Thyrsa: Asclepeion"),
    ("ThyrsaCity_Agora", "Thyrsa: Agora"), ("ThyrsaCity_Tavern", "Thyrsa: the Kantharos"),
    ("ThyrsaCity_PindarosHouse", "Thyrsa: Pindaros (xenia host)"), ("ThyrsaCity_MantoHouse", "Thyrsa: Manto the seer"),
    ("ThyrsaCity_VintnerHouse", "Thyrsa: Staphylos the vintner"), ("ThyrsaCity_ActorHouse", "Thyrsa: Polos the actor"),
    ("ThyrsaCity_EudoraHouse", "Thyrsa: Eudora"), ("ThyrsaCity_MaskWorkshop", "Thyrsa: Euthykles's masks"),
    ("ThyrsaCity_SownHouse", "Thyrsa: Chthonia (the Sown)"),
]


def overview():
    """design/phase3/img/thyrsa_interiors_overview.png: every room's 2x render, four to a row."""
    ims = [(Image.open(IMG / f"{n}.png").convert("RGB"), label) for n, label in ROOMS]
    cw = max(im.width for im, _ in ims) + 24
    rows = [ims[i:i + 4] for i in range(0, len(ims), 4)]
    heights = [max(im.height for im, _ in r) + 30 for r in rows]
    out = Image.new("RGB", (cw * 4, sum(heights) + 12), BG)
    d = ImageDraw.Draw(out)
    y = 6
    for r, h in zip(rows, heights):
        for i, (im, label) in enumerate(r):
            x = i * cw + 12
            d.text((x, y), label, fill=INK, font=font(14))
            out.paste(im, (x + (cw - 24 - im.width) // 2, y + 20))
        y += h
    out.save(IMG / "thyrsa_interiors_overview.png")
    print(IMG / "thyrsa_interiors_overview.png", out.size)


INGAME = ["arrival_after_the_welcome", "tour_the_square", "tour_wine_seller",
          "tour_fountain_court", "tour_the_gods_fountain", "tour_semele",
          "tour_theater_terrace", "tour_eudora", "tour_eudora_yard_gate",
          "west_gate_drum_brace", "west_gate_drum_pushed", "west_gate_alethea_west"]


def ingame(shots):
    """design/phase3/img/ThyrsaCity_ingame.png: a dozen of thyrsa_city.sh's screenshots, 2x."""
    def find(name):        # shots are numbered in order: match the name after the number
        hits = sorted(Path(shots).glob(f"[0-9][0-9][0-9][0-9]_{name}.png"))
        assert hits, f"no screenshot named {name} in {shots}"
        return hits[0]
    ims = [Image.open(find(n)).convert("RGB") for n in INGAME]
    w, h = ims[0].size
    out = Image.new("RGB", (3 * w + 2 * 8, 4 * h + 3 * 8), (24, 24, 32))
    for i, im in enumerate(ims):
        out.paste(im, ((i % 3) * (w + 8), (i // 3) * (h + 8)))
    out = out.resize((out.width * 2, out.height * 2), Image.NEAREST)
    out.save(IMG / "ThyrsaCity_ingame.png")
    print(IMG / "ThyrsaCity_ingame.png", out.size)


def main():
    if sys.argv[1] == "--overview":
        overview()
        return
    if sys.argv[1] == "--ingame":
        ingame(sys.argv[2])
        return
    before = Path(sys.argv[1])
    city_b = Image.open(before / "ThyrsaCity.png").convert("RGB")
    city_a = Image.open(IMG / "ThyrsaCity.png").convert("RGB")
    parts = [
        pair("Thyrsa City", city_b, city_a, scale=0.5,
             note="The square, the street of tripods, Eudora's yard, the bed inside the gate, "
                  "the Kadmeia's groves."),
        pair("The square: the god's fountain, the market, garlands across the processional way",
             crop(city_b, 20, 13, 36, 28), crop(city_a, 20, 13, 36, 28)),
        pair("Eudora's yard: a household's court, with its gate",
             crop(city_b, 36, 31, 47, 37), crop(city_a, 36, 31, 47, 37)),
        pair("Manto's house: cages from every beam",
             Image.open(before / "ThyrsaCity_MantoHouse.png").convert("RGB"),
             Image.open(IMG / "ThyrsaCity_MantoHouse.png").convert("RGB")),
        pair("Polos's house: robes, his lines, his crown, the rug he paces",
             Image.open(before / "ThyrsaCity_ActorHouse.png").convert("RGB"),
             Image.open(IMG / "ThyrsaCity_ActorHouse.png").convert("RGB")),
    ]
    if len(sys.argv) >= 4:
        a = Image.open(sys.argv[2]).convert("RGB")
        b = Image.open(sys.argv[3]).convert("RGB")
        # the chamber sits just left of the screen's centre in the player's view
        box = (80, 16, 160, 80)
        fa, fb = a.crop(box), b.crop(box)
        fa = fa.resize((fa.width * 3, fa.height * 3), Image.NEAREST)
        fb = fb.resize((fb.width * 3, fb.height * 3), Image.NEAREST)
        p = pair("Semele's smoke, in game: its two frames", fa, fb)
        d = ImageDraw.Draw(p)
        d.rectangle([0, 26, p.width, 44], fill=BG)
        d.text((0, 26), "frame 0", fill=(120, 96, 80), font=font(15))
        d.text((fa.width + 24, 26), "frame 1", fill=(120, 96, 80), font=font(15))
        parts.append(p)
    out = stack(parts)
    out.save(IMG / "thyrsa_polish_before_after.png")
    print(IMG / "thyrsa_polish_before_after.png", out.size)


if __name__ == "__main__":
    main()
