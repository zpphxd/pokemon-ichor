#!/usr/bin/env python3
"""Helpers for tools/ichor/tests/oikoumene_trainer_pics.sh.

  oikoumene_trainer_pics.py expect OUT.lua   the cases, with each pic's palette from its PNG
  oikoumene_trainer_pics.py sheet DIR        a contact sheet of DIR/shots/*.png at DIR/intros.png

CASES is the test's list: one battle per new class, with the label it must show
and a sample trainer name (from PERIODOS.md where the halls name one). KING has
no pic of its own in batch 1, so its battle borrows Hektor's.
"""
import glob
import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
FRONT = os.path.join(ROOT, "graphics/trainers/front_pics")

CASES = [
    ("TROJAN_HOPLITE", "TROJAN_HOPLITE", "HOPLITE", "AGENOR"),
    ("CHARIOTEER", "CHARIOTEER", "CHARIOTEER", "KEBRIONES"),
    ("SHEPHERD_OF_IDA", "SHEPHERD_OF_IDA", "SHEPHERD", "PARIS"),
    ("ARGONAUT", "ARGONAUT", "ARGONAUT", "EUPHEMOS"),
    ("COLCHIAN_SORCERESS", "COLCHIAN_SORCERESS", "SORCERESS", "KYTAIA"),
    ("CHALYBES_SMITH", "CHALYBES_SMITH", "SMITH", "AKMON"),
    ("PRIEST_OF_THE_SUN", "PRIEST_OF_THE_SUN", "SUN PRIEST", "MANETHO"),
    ("SCRIBE_OF_THOTH", "SCRIBE_OF_THOTH", "SCRIBE", "IMOUTHES"),
    ("EMBALMER", "EMBALMER", "EMBALMER", "PETOSIRIS"),
    ("NILE_BOATMAN", "NILE_BOATMAN", "BOATMAN", "THONIS"),
    ("PHOENICIAN_TRADER", "PHOENICIAN_TRADER", "TRADER", "ITHOBAL"),
    ("PRINCE", "PRINCE_HEKTOR", "PRINCE", "HEKTOR"),
    ("PHARAOH", "PHARAOH_PROTEUS", "PHARAOH", "PROTEUS"),
    ("PRIESTESS", "PRIESTESS_MEDEA", "PRIESTESS", "MEDEA"),
    ("QUEEN", "QUEEN_HELEN", "QUEEN", "HELEN"),
    ("KING", "PRINCE_HEKTOR", "KING", "PRIAM"),
]


def bgr555(r, g, b):
    return (r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10)


def expect(path):
    lines = ["return {"]
    for cls, pic, label, name in CASES:
        png = os.path.join(FRONT, pic.lower() + ".png")
        im = Image.open(png)
        if im.mode != "P":
            sys.exit(f"{png} is not an indexed PNG")
        raw = im.getpalette()[:48]
        cols = [bgr555(*raw[i * 3:i * 3 + 3]) for i in range(16)]
        lines.append('  { class = "TRAINER_CLASS_%s", pic = "TRAINER_PIC_%s", label = "%s", name = "%s", '
                     'file = "%s", pal = { %s } },' % (cls, pic, label, name, pic.lower(),
                                                        ", ".join(str(c) for c in cols[1:])))
    lines.append("}")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def sheet(out):
    shots = sorted(glob.glob(os.path.join(out, "shots", "*.png")))
    if not shots:
        print("no screenshots in", out)
        return
    cols, pad = 4, 14
    rows = (len(shots) + cols - 1) // cols
    big = Image.new("RGB", (240 * cols, (160 + pad) * rows), (248, 240, 224))
    d = ImageDraw.Draw(big)
    for i, p in enumerate(shots):
        x, y = 240 * (i % cols), (160 + pad) * (i // cols)
        big.paste(Image.open(p).convert("RGB").resize((240, 160)), (x, y))
        d.text((x + 3, y + 161), os.path.basename(p)[5:-4], fill=(64, 40, 32))
    dest = os.path.join(out, "intros.png")
    big.save(dest)
    print("sheet:", dest)


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("expect", "sheet"):
        sys.exit(__doc__)
    (expect if sys.argv[1] == "expect" else sheet)(sys.argv[2])
