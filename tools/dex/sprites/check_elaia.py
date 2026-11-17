"""Validate the eleven Elaia dex redraws, optionally importing only those assets.

Run after build.py with the eleven species names. --import-rom uses the existing
dex importer without regenerating unrelated species, constants or game data.
"""
import argparse
import importlib.util
import json
import re
import struct
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

import build


NAMES = (
    "Nebrel", "Kladoe", "Daphnyad", "Kynder", "Dikyon", "Pylakyon",
    "Hipling", "Thalamare", "Seismare", "Eripip", "Galekit",
)
ROOT = Path(build.ROOT)


def importer():
    spec = importlib.util.spec_from_file_location("dex_rom_gen", ROOT / "tools/dex/rom/gen.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def concept_builder():
    spec = importlib.util.spec_from_file_location("mon_from_concept", ROOT / "tools/ichor/art/mon_from_concept.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(names=NAMES):
    mons = build.load_mons()
    engine = (ROOT / "src/data/pokemon/species_info/aethos_families.h").read_text()
    report = {}
    sizes = {"anim_front.png": (64, 128), "back.png": (64, 64),
             "icon.png": (32, 64), "overworld.png": (192, 32), "footprint.png": (16, 16)}
    for name in names:
        errors, warnings = [], []
        b = build.build_mon(mons[name], errors, warnings)
        assert not errors and not warnings, (name, errors, warnings)
        source = ROOT / "design/dex/sprites" / name.lower()
        dest = ROOT / "graphics/pokemon" / name.lower()
        arrays = {}
        for file, size in sizes.items():
            path = source / file
            with Image.open(path) as im:
                assert im.mode == "P" and im.size == size, (name, file, im.mode, im.size)
                assert path.read_bytes()[24] == (1 if file == "footprint.png" else 4), (name, file, "bit depth")
                arr = np.array(im)
                assert arr.max() <= (1 if file == "footprint.png" else 15), (name, file, "index")
                if file != "footprint.png":
                    assert im.info.get("transparency") == 0 and np.any(arr == 0), (name, file, "transparency")
                if file == "icon.png":
                    expected = build.read_jasc(Path(build.ICON_PALS) / f"pal{b.icon_pal}.pal")
                    assert im.getpalette()[:48] == [v for c in expected for v in c], (name, "shared icon palette")
                elif file != "footprint.png":
                    expected = build.read_jasc(source / "normal.pal")
                    assert im.getpalette()[:48] == [v for c in expected for v in c], (name, file, "battle palette")
                arrays[file] = arr
            assert path.read_bytes() == (dest / file).read_bytes(), (name, file, "ROM import")
        for file in ("normal.pal", "shiny.pal", "overworld_normal.pal", "overworld_shiny.pal"):
            colors = build.read_jasc(source / file)
            assert len(colors) == 16 and all(0 <= v <= 248 and v % 8 == 0 for c in colors for v in c), (name, file, "BGR555")
            assert (source / file).read_bytes() == (dest / file).read_bytes(), (name, file, "ROM import")
        assert (source / "normal.pal").read_bytes() == (source / "overworld_normal.pal").read_bytes(), name
        assert (source / "shiny.pal").read_bytes() == (source / "overworld_shiny.pal").read_bytes(), name
        assert (source / "normal.pal").read_bytes() != (source / "shiny.pal").read_bytes(), name
        if name.lower() in build.concept_sourced():
            # built from an approved concept (design/STYLE.md §3), not the painter
            c = concept_builder().build(name.lower(), concept_builder().config(name.lower()))
            for file, want in (("anim_front.png", c["front"]), ("back.png", c["back"]),
                               ("overworld.png", c["follow"]), ("icon.png", c["icon"])):
                assert np.array_equal(arrays[file], want), (name, file, "concept reproducibility")
            report[name] = {"source": "concept"}
            continue
        assert np.array_equal(arrays["anim_front.png"], np.vstack(b.front)), (name, "front reproducibility")
        assert np.array_equal(arrays["back.png"], b.back), (name, "back reproducibility")
        assert np.array_equal(arrays["overworld.png"], np.hstack(b.follow)), (name, "follower reproducibility")
        assert np.array_equal(arrays["icon.png"], np.vstack(b.icon)), (name, "icon reproducibility")
        for view, phase in (("front", 0), ("front", 1), ("back", 0)):
            path = Path(build.art_path(mons[name], view, phase))
            rows = [line for line in path.read_text().splitlines() if line[:3].strip().isdigit()]
            assert len(rows) == 64 and all(len(row[4:]) == 64 for row in rows), (name, view, phase, "editable grid")
            assert np.count_nonzero(build.render(mons[name], view, phase) !=
                                    build.render(mons[name], view, phase, art=False)), (name, view, phase, "hand finish")
        battle_motion = int(np.count_nonzero(b.front[0] != b.front[1]))
        icon_motion = int(np.count_nonzero(b.icon[0] != b.icon[1]))
        walk_motion = [int(np.count_nonzero(b.follow[i] != b.follow[i + 1])) for i in (0, 2, 4)]
        assert battle_motion and icon_motion and all(walk_motion), (name, "duplicate motion", walk_motion)
        entry = engine.split("[SPECIES_" + name.upper() + "]", 1)[1].split("[SPECIES_", 1)[0]
        assert int(re.search(r"\.iconPalIndex = (\d+)", entry)[1]) == b.icon_pal, (name, "engine icon selector")
        report[name] = {"battle_changed_pixels": battle_motion, "icon_changed_pixels": icon_motion,
                        "walk_changed_pixels_down_up_side": walk_motion, "icon_palette": b.icon_pal,
                        "front_bbox": b.front_bbox, "status": "technical checks passed"}
    return report


def native_check(name):
    dest = ROOT / "graphics/pokemon" / name.lower()
    out = ROOT / "build/elaia-sprite-native" / name.lower()
    out.mkdir(parents=True, exist_ok=True)
    conversions = (
        ("anim_front.png", "front.4bpp", 4096, ("-mwidth", "8", "-mheight", "8")),
        ("back.png", "back.4bpp", 2048, ("-mwidth", "8", "-mheight", "8")),
        ("icon.png", "icon.4bpp", 1024, ("-mwidth", "4", "-mheight", "4")),
        ("overworld.png", "overworld.4bpp", 3072, ("-mwidth", "4", "-mheight", "4")),
        ("footprint.png", "footprint.1bpp", 32, ()),
        ("normal.pal", "normal.gbapal", 32, ()),
        ("shiny.pal", "shiny.gbapal", 32, ()),
    )
    for source, target, size, options in conversions:
        subprocess.run([str(ROOT / "tools/gbagfx/gbagfx"), str(dest / source),
                        str(out / target), *options], check=True)
        assert (out / target).stat().st_size == size, (name, target, "native size")
    for pal in ("normal", "shiny"):
        colors = build.read_jasc(dest / (pal + ".pal"))
        expected = [r // 8 | (g // 8) << 5 | (b // 8) << 10 for r, g, b in colors]
        actual = struct.unpack("<16H", (out / (pal + ".gbapal")).read_bytes())
        assert list(actual) == expected, (name, pal, "native BGR555 words")
    return "passed"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("names", nargs="*", metavar="NAME", help="validate/import only these Elaia species")
    ap.add_argument("--import-rom", action="store_true")
    ap.add_argument("--native-check", action="store_true", help="verify real gbagfx conversion sizes and palette words")
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    names = args.names or NAMES
    if any(name not in NAMES for name in names):
        ap.error("names must be Elaia species: " + ", ".join(NAMES))
    if args.import_rom:
        gen = importer()
        for mon in gen.load_species():
            if mon.name in names:
                gen.copy_sprites(mon)
    report = check(names)
    if args.native_check:
        for name in names:
            report[name]["native_gbagfx_sizes_and_bgr555"] = native_check(name)
    print(json.dumps(report, indent=2))
    print(f"{len(names)} species: native files, matching ROM imports, palettes and unique motion verified.")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
