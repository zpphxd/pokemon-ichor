#!/usr/bin/env python3
"""Build the before-and-after sheets for design/phase1/UI_world.md from in-game
screenshots: the "before" from main before this batch, the "after" from this
branch, both captured with the temporary harness described in UI_world.md.

Usage: python3 tools/ichor/art/ui_world_review.py BEFORE_DIR AFTER_DIR [SHEET]
(SHEET, such as aethos_map_revision.png, builds just that one.)
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
IMG = ROOT / "design/phase1/img"
INK, PARCH, CLAY = (32, 24, 24), (232, 216, 176), (184, 88, 48)

SHEETS = {
    "ui_world_compare_map.png": [
        ("Fly map", "fly_fly.png", "fly_fly.png"),
        ("Fly map, cursor on Astyra", None, "fly_fly_astyra.png"),
        ("Wall map", "wallmap_wallmap.png", "wallmap_wallmap.png"),
        ("Pokedex area: Smoliv on Route 1, morning", None, "dex_dex_area_b.png"),
        ("Fly map before the game is cleared: Olympia unnamed", None, "fly_fly_olympia.png"),
        ("... and after: OLYMPIA", None, "flyclear_fly_olympia.png"),
    ],
    # The map revision (design/AETHOS_MAP.md): before is the first Aethos map
    "aethos_map_revision.png": [
        ("Fly map, from Elaia", "fly_fly.png", "fly_fly.png"),
        ("Astyra", "fly_fly_astyra.png", "fly_fly_astyra.png"),
        ("Delphoi", "fly_fly_delphoi.png", "fly_fly_delphoi.png"),
        ("Knossa: the island, then Amnisos on it", "fly_fly_knossa.png", "fly_fly_amnisos.png"),
        ("A waypoint: Hecate's Hollow", None, "fly_fly_hollow.png"),
        ("An island: Lesbos", None, "fly_fly_lesbos.png"),
        ("Wall map", "wallmap_wallmap.png", "wallmap_wallmap.png"),
        ("Pokedex area: Smoliv on Route 1, morning", "dex_dex_area_b.png", "dex_dex_area_b.png"),
    ],
    "ui_world_compare_card.png": [
        ("Front, Theo, no stars", "card_theo_0_front.png", "card_theo_0_front.png"),
        ("Back, the Hearth Laurel", "card_theo_1_back.png", "card_theo_1_back.png"),
        ("Front, Ianthe", "card_ianthe_3_front.png", "card_ianthe_3_front.png"),
        ("Back, Ianthe, three Laurels", "card_ianthe_3_back.png", "card_ianthe_3_back.png"),
        ("Front, one star: the bronze lip", "card_theo_8_front.png", "card_theo_8_front.png"),
        ("Back, eight Laurels and the Hall of Heroes", "card_theo_8_back.png", "card_theo_8_back.png"),
    ],
    "ui_world_compare_starter.png": [
        ("Cyndaquil's krater", "starter_pick.png", "starter_pick.png"),
        ("Snivy's krater", "starter_pick_left.png", "starter_pick_left.png"),
        ("Piplup's krater", "starter_pick_right.png", "starter_pick_right.png"),
        ("The choice, on a cup's tondo", "starter_confirm.png", "starter_confirm.png"),
    ],
    "ui_world_compare_clock.png": [
        ("Setting the klepsydra (Theo)", "clock_theo_set.png", "clock_theo_set.png"),
        ("Two hours later: the water has risen", "clock_theo_set_later.png", "clock_theo_set_later.png"),
        ("Ianthe's", "clock_ianthe_set_much_later.png", "clock_ianthe_set_much_later.png"),
        ("Is this the correct time?", "clock_theo_confirm.png", "clock_theo_confirm.png"),
        ("Viewing it later", "viewclock_view.png", "viewclock_view.png"),
    ],
    "ui_world_compare_evolution.png": [
        ("The radiance begins", "evo_evo_2.png", "evo_evo_2.png"),
        ("The wave runs out", "evo_evo_3.png", "evo_evo_3.png"),
        ("... and back", "evo_evo_4.png", "evo_evo_4.png"),
        ("Full light", "evo_evo_5.png", "evo_evo_5.png"),
    ],
    "ui_world_compare_speech.png": [
        ("Daphne", "02_daphne.png", "02_daphne.png"),
        ("Smoliv", "03_smoliv.png", "03_smoliv.png"),
        ("Which of these two is you?", "05_theo_or_ianthe.png", "05_theo_or_ianthe.png"),
    ],
}


def sheet(name, rows, before, after):
    scale, pad, cap = 2, 6, 14
    w, h = 240 * scale, 160 * scale
    out = Image.new("RGB", (pad + 2 * (w + pad), pad + len(rows) * (h + cap + pad) + cap), INK)
    d = ImageDraw.Draw(out)
    d.text((pad, 2), "before (main)", fill=CLAY)
    d.text((pad * 2 + w, 2), "after (this branch)", fill=CLAY)
    for i, (caption, b, a) in enumerate(rows):
        y = cap + pad + i * (h + cap + pad)
        d.text((pad, y), caption, fill=PARCH)
        for j, (folder, fname) in enumerate([(before, b), (after, a)]):
            x = pad + j * (w + pad)
            if fname and (folder / fname).exists():
                im = Image.open(folder / fname).convert("RGB").resize((w, h), Image.NEAREST)
                out.paste(im, (x, y + cap))
            else:
                d.rectangle([x, y + cap, x + w - 1, y + cap + h - 1], outline=(72, 56, 56))
                d.text((x + 8, y + cap + 8), "(no before shot: a new screen state)", fill=(120, 104, 96))
    out.save(IMG / name)
    print(f"wrote design/phase1/img/{name}")


if __name__ == "__main__":
    before, after = Path(sys.argv[1]), Path(sys.argv[2])
    only = sys.argv[3] if len(sys.argv) > 3 else None
    for name, rows in SHEETS.items():
        if only is None or name == only:
            sheet(name, rows, before, after)
