"""Build/check only the native Smoliv opening assets, without editing dex data.

python3 tools/dex/sprites/smoliv.py --native-check --preview build/smoliv-review --report build/smoliv-check.json
"""
import argparse
import json
from pathlib import Path
import shutil
import struct
import subprocess

import numpy as np
from PIL import Image

import build
from lines.smoliv import SMOLIV


ROOT = Path(build.ROOT)
FILES = {
    "anim_front.png": "front.png", "back.png": "back.png", "icon.png": "icon.png",
    "normal.pal": "normal.pal", "shiny.pal": "shiny.pal",
    "overworld.png": "overworld.png", "overworld_normal.pal": "overworld_normal.pal",
    "overworld_shiny.pal": "overworld_shiny.pal", "footprint.png": "footprint.png",
}


def check(b):
    source = ROOT / "design/dex/sprites/smoliv"
    dest = ROOT / "graphics/pokemon/smoliv"
    arrays = {"anim_front.png": np.vstack(b.front), "back.png": b.back,
              "icon.png": np.vstack(b.icon), "overworld.png": np.hstack(b.follow),
              "footprint.png": b.foot}
    for file, arr in arrays.items():
        path = source / file
        with Image.open(path) as im:
            assert im.mode == "P" and im.size == (arr.shape[1], arr.shape[0]), file
            assert np.array_equal(np.array(im), arr), (file, "reproducibility")
            assert path.read_bytes()[24] == (1 if file == "footprint.png" else 4), (file, "bit depth")
            assert arr.max() <= (1 if file == "footprint.png" else 15), (file, "indices")
            if file != "footprint.png":
                assert im.info.get("transparency") == 0 and np.any(arr == 0), (file, "transparent index")
                colors = (build.read_jasc(Path(build.ICON_PALS) / "pal1.pal") if file == "icon.png"
                          else build.read_jasc(source / "normal.pal"))
                assert im.getpalette()[:48] == [v for c in colors for v in c], (file, "palette identity")
    for file, target in FILES.items():
        assert (source / file).read_bytes() == (dest / target).read_bytes(), (file, "ROM copy")
        if file.endswith(".pal"):
            colors = build.read_jasc(source / file)
            assert len(colors) == 16 and all(0 <= v <= 248 and v % 8 == 0 for c in colors for v in c), (file, "BGR555")
    assert (source / "normal.pal").read_bytes() == (source / "overworld_normal.pal").read_bytes()
    assert (source / "shiny.pal").read_bytes() == (source / "overworld_shiny.pal").read_bytes()
    assert (source / "normal.pal").read_bytes() != (source / "shiny.pal").read_bytes()
    for view, phase in (("front", 0), ("front", 1), ("back", 0)):
        path = Path(build.art_path(SMOLIV, view, phase))
        rows = [line for line in path.read_text().splitlines() if line[:3].strip().isdigit()]
        assert len(rows) == 64 and all(len(row[4:]) == 64 for row in rows), (view, phase, "editable grid")
        assert np.count_nonzero(build.render(SMOLIV, view, phase) !=
                                build.render(SMOLIV, view, phase, art=False)), (view, phase, "hand finish")
    motion = [int(np.count_nonzero(b.follow[i] != b.follow[i + 1])) for i in (0, 2, 4)]
    battle_motion = int(np.count_nonzero(b.front[0] != b.front[1]))
    icon_motion = int(np.count_nonzero(b.icon[0] != b.icon[1]))
    assert battle_motion and icon_motion and all(motion), ("unique frames", motion)
    entry = (ROOT / "src/data/pokemon/species_info/gen_9_families.h").read_text().split(
        "[SPECIES_SMOLIV]", 1)[1].split("[SPECIES_DOLLIV]", 1)[0]
    assert ".iconPalIndex = 1," in entry
    assert ".frontAnimFrames = sAnims_TwoFramePlaceHolder," in entry
    graphics = (ROOT / "src/data/graphics/pokemon.h").read_text()
    assert 'gMonFrontPic_Smoliv[] = INCGFX_U32("graphics/pokemon/smoliv/front.png"' in graphics
    return {"species": "Smoliv", "icon_palette": 1, "battle_changed_pixels": battle_motion,
            "icon_changed_pixels": icon_motion, "walk_changed_pixels_down_up_side": motion,
            "front_bbox": b.front_bbox, "status": "technical checks passed"}


def native_check():
    out = ROOT / "build/smoliv-native"
    out.mkdir(parents=True, exist_ok=True)
    conversions = (
        ("front.png", "front.4bpp", 4096, ("-mwidth", "8", "-mheight", "8")),
        ("back.png", "back.4bpp", 2048, ("-mwidth", "8", "-mheight", "8")),
        ("icon.png", "icon.4bpp", 1024, ("-mwidth", "4", "-mheight", "4")),
        ("overworld.png", "overworld.4bpp", 3072, ("-mwidth", "4", "-mheight", "4")),
        ("footprint.png", "footprint.1bpp", 32, ()),
        ("normal.pal", "normal.gbapal", 32, ()),
        ("shiny.pal", "shiny.gbapal", 32, ()),
    )
    for source, target, size, options in conversions:
        subprocess.run([str(ROOT / "tools/gbagfx/gbagfx"),
                        str(ROOT / "graphics/pokemon/smoliv" / source),
                        str(out / target), *options], check=True)
        assert (out / target).stat().st_size == size, (target, "native size")
    for name in ("normal", "shiny"):
        colors = build.read_jasc(ROOT / "graphics/pokemon/smoliv" / (name + ".pal"))
        expected = [r // 8 | (g // 8) << 5 | (b // 8) << 10 for r, g, b in colors]
        actual = struct.unpack("<16H", (out / (name + ".gbapal")).read_bytes())
        assert list(actual) == expected, (name, "native BGR555 words")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--preview", type=Path)
    ap.add_argument("--report", type=Path)
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--native-check", action="store_true")
    args = ap.parse_args()
    errors, warnings = [], []
    b = build.build_mon(SMOLIV, errors, warnings)
    assert not errors and not warnings, (errors, warnings)
    if not args.check_only:
        source = Path(build.write_mon(b))
        dest = ROOT / "graphics/pokemon/smoliv"
        for file, target in FILES.items():
            shutil.copyfile(source / file, dest / target)
    report = check(b)
    if args.native_check:
        native_check()
        report["native_gbagfx_sizes_and_bgr555"] = "passed"
    if args.preview:
        args.preview.mkdir(parents=True, exist_ok=True)
        build.card(b).save(args.preview / "smoliv.png")
        build.grid(b.front[0], b.pal).save(args.preview / "smoliv-front-grid.png")
        build.grid(b.back, b.pal).save(args.preview / "smoliv-back-grid.png")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    print("Smoliv: native assets and ROM copies verified; 0 errors, 0 warnings.")


if __name__ == "__main__":
    main()
