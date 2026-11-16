import hashlib
import io
from pathlib import Path
import re
import sys
import unittest

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import export_route4_characters as portraits


class Route4CharacterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = Image.open(portraits.SOURCE).convert("RGBA")
        cls.figures = portraits.split_figures(source)

    def test_generated_source_is_preserved(self):
        self.assertEqual(
            hashlib.sha256(portraits.SOURCE.read_bytes()).hexdigest(),
            portraits.SOURCE_SHA256,
        )

    def test_native_exports_reproduce(self):
        for (name, _, _), (_, figure) in zip(portraits.PORTRAITS, self.figures):
            with self.subTest(portrait=name):
                expected = portraits.encode(figure)
                path = portraits.ROOT / f"graphics/trainers/front_pics/{name}.png"
                encoded = io.BytesIO()
                expected.save(encoded, format="PNG", bits=4, transparency=0)
                self.assertEqual(path.read_bytes(), encoded.getvalue())
                with Image.open(path) as image:
                    self.assertEqual(image.mode, "P")
                    self.assertEqual(image.size, (64, 64))
                    self.assertEqual(image.info["transparency"], 0)
                    self.assertLessEqual(len(set(image.getdata()) - {0}), 15)
                    self.assertTrue(all(value % 8 == 0 for value in image.getpalette()))
                    x0, y0, x1, y1 = image.convert("RGBA").getbbox()
                    self.assertGreaterEqual(min(x0, y0), 2)
                    self.assertLessEqual(max(x1, y1), 62)
                self.assertEqual(path.read_bytes()[24], 4)

    def test_linen_and_identity_accents_survive_reduction(self):
        images = {
            name: portraits.encode(figure).convert("RGBA")
            for (name, _, _), (_, figure) in zip(portraits.PORTRAITS, self.figures)
        }
        linen = sum(
            a and r > 200 and g > 190 and b > 160
            for r, g, b, a in images["potter"].getdata()
        )
        leaves = sum(
            a and g > r * 1.05 and b < g * 0.85
            for r, g, b, a in images["initiate_f"].getdata()
        )
        ochre = sum(
            a and r > 140 and g > 90 and r > g * 1.1 and g > b * 1.5
            for r, g, b, a in images["runner"].getdata()
        )
        self.assertGreaterEqual(linen, 10)
        self.assertGreaterEqual(leaves, 4)
        self.assertGreaterEqual(ochre, 20)

    def test_original_imported_portraits_are_unchanged(self):
        expected = {
            "hiker": "5f27a6416e5bd2f5c27fc9b8c3297ccaa2d7a3d59f27ec3a9116e4aefbac3097",
            "psychic_f": "90018e603e63e6122999ea8af5de72dc9bc0e49e30d215728c207b847c2e8204",
            "running_triathlete_m": "38d3457c4974ea56edc027e6c8a03f493499a4fd03770689f02c9bf92b8a37ef",
        }
        for name, digest in expected.items():
            path = portraits.ROOT / f"graphics/trainers/front_pics/{name}.png"
            with self.subTest(original=name):
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)

    def test_existing_trainers_use_their_own_portrait_bindings(self):
        source = (portraits.ROOT / "src/data/trainers.party").read_text()
        for trainer, picture in (
            ("EXEKIAS", "Potter"),
            ("MYRRHINE", "Initiate F"),
            ("PHEIDIPPOS", "Runner"),
        ):
            with self.subTest(trainer=trainer):
                block = re.search(
                    rf"^=== TRAINER_ICHOR_{trainer} ===\n(.*?)(?=^===|\Z)",
                    source,
                    re.MULTILINE | re.DOTALL,
                )
                self.assertIsNotNone(block)
                self.assertIn(f"\nPic: {picture}\n", "\n" + block.group(1))


if __name__ == "__main__":
    unittest.main()
