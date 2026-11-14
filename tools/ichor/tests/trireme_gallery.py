#!/usr/bin/env python3
"""Copy the Euploia's renders and the key frames of its headless run into
design/phase2/img at 2x, for the director to forward.

  /usr/bin/python3 tools/ichor/maps/trireme.py --render build/trireme/maps
  tools/ichor/tests/trireme.sh
  /usr/bin/python3 tools/ichor/tests/trireme_gallery.py

The run is deterministic, so the frame names below pick the same moments each
time; if the scenes' timing changes, look at build/test_trireme/ and update them.
"""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "build/test_trireme"
MAPS = ROOT / "build/trireme/maps"
IMG = ROOT / "design/phase2/img"

RENDERS = ["trireme_deck.png", "trireme_hold.png", "trireme_deck_calm.png", "trireme_deck_cast_off.png",
           "trireme_deck_last_leg.png", "trireme_screens.png"]

SCENES = [
    ("01_cast_off", "02_cast_off_02", "Boarding: \"Cast off!\" The sail half full, filling"),
    ("02_calm", "20_calm_11", "The halcyon calm: the sail sags, the camera looks forward"),
    ("03_stroke", "20_calm_27", "Kleon keeps the stroke from the hatch, the oars out"),
    ("04_nest", "30_nest_06", "The nest drifts at the ram; two snatchers circle"),
    ("05_snatcher", "30_nest_battle_4", "A snatcher (Harpeck, a stand-in sprite) at the nest"),
    ("06_spalunk", "30_nest_20", "There's a third! Alethea's Spalunk"),
    ("07_hatching", "30_nest_32", "The Galenyon on the ram; the eggs hatch"),
    ("08_chick", "30_nest_41", "A halcyon chick on the player's petasos"),
    ("09_letter", "30_nest_61", "The night leg: Kleon's letter from his mother"),
    ("10_dark_trireme", "30_nest_77", "The trireme with no lamps, a sickle on its furled sail"),
    ("11_last_leg", "51_last_leg_06", "Beat 10C: the mainland ahead of the bow"),
    ("12_hold", "10_hold", "The hold: three banks of benches, oars in their ports"),
]


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    for name in RENDERS:
        src = MAPS / name
        if src.exists():
            Image.open(src).save(IMG / name)
            print(IMG / name)
    tiles = []
    for out, frame, caption in SCENES:
        src = RUN / f"{frame}.png"
        if not src.exists():
            print("missing", src)
            continue
        im = Image.open(src).convert("RGB").resize((480, 320), Image.NEAREST)
        im.save(IMG / f"trireme_scene_{out}.png")
        tiles.append((im, caption))
    cols, pad, cap = 3, 8, 16
    rows = -(-len(tiles) // cols)
    sheet = Image.new("RGB", (cols * (480 + pad) + pad, rows * (320 + pad + cap) + pad), (24, 24, 32))
    d = ImageDraw.Draw(sheet)
    for i, (im, caption) in enumerate(tiles):
        x = pad + (i % cols) * (480 + pad)
        y = pad + (i // cols) * (320 + pad + cap)
        d.text((x, y), caption, fill=(230, 230, 200))
        sheet.paste(im, (x, y + cap))
    sheet.save(IMG / "trireme_scenes.png")
    print(IMG / "trireme_scenes.png")


if __name__ == "__main__":
    main()
