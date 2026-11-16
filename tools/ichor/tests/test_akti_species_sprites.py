import re
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/dex/rom"))
import gen
sys.path.insert(0, str(ROOT / "tools/dex/sprites"))
import build


NAMES = (
    "Eopeep", "Alekrow", "Hoplektor", "Harpeck", "Harpelle",
    "Epopoi", "Lophops", "Basilops", "Gelasable", "Kerazap", "Kerastorm",
)


class AktiSpeciesSpriteTests(unittest.TestCase):
    def test_all_views_reproduce_and_keep_distinct_animation_states(self):
        mons = build.load_mons()
        for name in (*NAMES, "Galekit", "Eripip"):
            with self.subTest(species=name):
                errors, warnings = [], []
                built = build.build_mon(mons[name], errors, warnings)
                self.assertEqual(errors, [])
                self.assertEqual(warnings, [])
                expected = {
                    "anim_front.png": np.vstack(built.front),
                    "back.png": built.back,
                    "icon.png": np.vstack(built.icon),
                    "overworld.png": np.hstack(built.follow),
                    "footprint.png": built.foot,
                }
                source = ROOT / "design/dex/sprites" / name.lower()
                target = ROOT / "graphics/pokemon" / name.lower()
                for file, pixels in expected.items():
                    with Image.open(source / file) as image:
                        self.assertEqual(image.mode, "P")
                        np.testing.assert_array_equal(np.asarray(image), pixels)
                        self.assertEqual((source / file).read_bytes()[24], 1 if file == "footprint.png" else 4)
                        if file != "footprint.png":
                            self.assertEqual(image.info.get("transparency"), 0)
                        if file == "icon.png":
                            colors = build.read_jasc(Path(build.ICON_PALS) / f"pal{built.icon_pal}.pal")
                        elif file != "footprint.png":
                            colors = built.pal.colors
                        else:
                            colors = None
                        if colors is not None:
                            self.assertEqual(image.getpalette()[:48], [v for color in colors for v in color])
                    self.assertEqual((source / file).read_bytes(), (target / file).read_bytes())
                for file, colors in (
                    ("normal.pal", built.pal.colors), ("shiny.pal", built.pal_shiny.colors),
                    ("overworld_normal.pal", built.pal.colors),
                    ("overworld_shiny.pal", built.pal_shiny.colors),
                ):
                    self.assertEqual(build.read_jasc(source / file), colors)
                    self.assertEqual((source / file).read_bytes(), (target / file).read_bytes())
                for normal, shiny in zip(built.follow, built.follow_shiny):
                    np.testing.assert_array_equal(normal, shiny)
                for first, second in (
                    built.front, built.icon,
                    *[built.follow[i:i + 2] for i in (0, 2, 4)],
                ):
                    self.assertFalse(np.array_equal(first, second))
                entry = (
                    (ROOT / "src/data/pokemon/species_info/aethos_families.h").read_text()
                    .split("[SPECIES_" + name.upper() + "]", 1)[1]
                    .split("[SPECIES_", 1)[0]
                )
                self.assertEqual(int(re.search(r"\.iconPalIndex = (\d+)", entry)[1]), built.icon_pal)

    def test_goat_miniatures_are_native_and_battle_grids_hand_finished(self):
        mons = build.load_mons()
        for name in ("Kerazap", "Kerastorm"):
            for view in ("down", "up", "side", "icon"):
                for phase in (0, 1):
                    with self.subTest(species=name, view=view, phase=phase):
                        first = build.render(mons[name], view, phase, W=32, H=32, s=0.2)
                        second = build.render(mons[name], view, phase, W=32, H=32, s=0.7)
                        np.testing.assert_array_equal(first, second)
                        x0, y0, x1, y1 = build.bbox(first)
                        self.assertGreater(x0, 0)
                        self.assertGreater(y0, 0)
                        self.assertLess(x1, 31)
                        self.assertEqual(y1, 30)
                        if name == "Kerastorm":
                            self.assertEqual(np.count_nonzero(first == 15), 1)
            for view, phase in (("front", 0), ("front", 1), ("back", 0)):
                with self.subTest(species=name, view=view, phase=phase):
                    finished = build.render(mons[name], view, phase)
                    draft = build.render(mons[name], view, phase, art=False)
                    self.assertGreater(np.count_nonzero(finished != draft), 20)
                    if name == "Kerastorm":
                        self.assertEqual(np.count_nonzero(finished == 15), 1)

    def test_geometry_matches_authoritative_sprite_generator(self):
        entries = {
            species["name"]: species
            for path in (ROOT / "design/dex/species").glob("*.yaml")
            for species in yaml.safe_load(path.read_text())["species"]
        }
        source = (ROOT / "src/data/pokemon/species_info/aethos_families.h").read_text()
        for name in NAMES:
            with self.subTest(species=name):
                measured = gen.pics(
                    SimpleNamespace(e=entries[name]),
                    ROOT / "design/dex/sprites" / name.lower(),
                )
                fw, fh, fy = measured["front"]
                bw, bh, by = measured["back"]
                ps, po, ts, to = measured["scale"]
                expected = {
                    "frontPicSize": f"MON_COORDS_SIZE({fw}, {fh})",
                    "frontPicYOffset": str(fy),
                    "backPicSize": f"MON_COORDS_SIZE({bw}, {bh})",
                    "backPicYOffset": str(by),
                    "pokemonScale": str(ps), "pokemonOffset": str(po),
                    "trainerScale": str(ts), "trainerOffset": str(to),
                }
                entry = source.split("[SPECIES_" + name.upper() + "]", 1)[1].split("[SPECIES_", 1)[0]
                for field, value in expected.items():
                    self.assertEqual(re.search(r"\." + field + r" = (.+),", entry)[1], value)
                sx, sy, size = measured["shadow"]
                self.assertIn(f"SHADOW({sx}, {sy}, {size})", entry)


if __name__ == "__main__":
    unittest.main()
