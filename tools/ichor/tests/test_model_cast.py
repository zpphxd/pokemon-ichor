import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import model_cast as cast
import walker_paint as hand_drawn  # owns the hand-drawn Gen 3 walkers (STYLE.md §3.6)
from sprites_lib import Palette, save_indexed


class ModelCastTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs = cast.build()

    def test_selected_model_sources_match_manifest(self):
        manifest = json.loads((cast.BASE / "manifest.json").read_text())
        self.assertEqual(len(manifest["source_files"]), 49)
        self.assertEqual(set(manifest["source_files"]),
                         {p.name for p in cast.BASE.glob("*.png")})
        for name, spec in manifest["source_files"].items():
            with self.subTest(source=name):
                path = cast.BASE / name
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), spec["sha256"])
                with Image.open(path) as image:
                    self.assertEqual(image.mode, "RGBA")

    def test_exact_owned_scope_and_native_frame_counts(self):
        self.assertEqual(set(self.outputs), cast.OWNED)
        self.assertEqual(len(self.outputs), 29)
        for path, image in self.outputs.items():
            with self.subTest(path=path):
                if path.parent == cast.PEOPLE:
                    count = 12 if path.stem in ("sam", "apollo") else 11 if path.stem == "cami" else 9
                    self.assertEqual(image.size, (16 * count, 32))
                    a = np.array(image)
                    self.assertEqual(len({a[:, i * 16:(i + 1) * 16].tobytes()
                                          for i in range(count)}), count)
                    for first, second in ((3, 4), (5, 6), (7, 8)):
                        self.assertGreater(np.count_nonzero(
                            a[:, first * 16:(first + 1) * 16]
                            != a[:, second * 16:(second + 1) * 16]), 8)
                else:
                    self.assertEqual(image.size, (64, 256) if path.parent == cast.BACK else (64, 64))

    def test_native_pngs_reproduce_production(self):
        for path, expected in self.outputs.items():
            with self.subTest(path=path):
                if path.parent == cast.PEOPLE and path.stem in hand_drawn.CHARACTERS:
                    # walkers are redrawn by hand now; the model output is history
                    with Image.open(cast.ROOT / path) as image:
                        np.testing.assert_array_equal(np.array(image), hand_drawn.build(path.stem)[0])
                    continue
                data = io.BytesIO()
                expected.save(data, format="PNG", bits=4, transparency=0)
                self.assertEqual((cast.ROOT / path).read_bytes(), data.getvalue())
                with Image.open(cast.ROOT / path) as image:
                    self.assertEqual(image.mode, "P")
                    self.assertEqual(image.info["transparency"], 0)
                    self.assertLessEqual(max(image.getdata()), 15)
                self.assertEqual(data.getvalue()[24], 4)

    def test_shared_walker_palettes_and_gba_precision(self):
        manifest = json.loads((cast.BASE / "manifest.json").read_text())
        for path, digest in manifest["shared_palette_sha256"].items():
            self.assertEqual(hashlib.sha256((cast.ROOT / path).read_bytes()).hexdigest(), digest)
        for path, image in self.outputs.items():
            with self.subTest(path=path):
                colors = np.array(image.getpalette()[:48]).reshape(16, 3)
                self.assertTrue(np.all(colors % 8 == 0))
                if path.parent == cast.PEOPLE:
                    np.testing.assert_array_equal(colors, cast.shared_palette(path.stem))

    def test_joint_back_palettes_and_intro_duplicate(self):
        for name in ("kleon", "alethea"):
            self.assertEqual(self.outputs[cast.FRONT / f"{name}.png"].getpalette(),
                             self.outputs[cast.BACK / f"{name}.png"].getpalette())
        front = self.outputs[cast.FRONT / "professor_daphne.png"]
        intro = self.outputs[cast.INTRO]
        self.assertEqual(front.tobytes(), intro.tobytes())
        self.assertEqual(front.getpalette(), intro.getpalette())

    def test_opposite_contacts_preserve_every_pixel_outside_the_legs(self):
        for name in cast.WALKERS:
            if name in ("kleon_seasick", "kleon_tablet"):
                continue
            image = np.array(self.outputs[cast.PEOPLE / f"{name}.png"])
            y = 27 if name in cast.ROBES else 24
            boxes = cast.LEG_BOXES.get(name, ((3, y, 13, 32), (3, y, 13, 32)))
            for first, box in zip((3, 5), boxes):
                outside = np.ones((32, 16), dtype=bool)
                x0, y0, x1, y1 = box
                outside[y0:y1, x0:x1] = False
                a, b = image[:, first * 16:(first + 1) * 16], image[:, (first + 1) * 16:(first + 2) * 16]
                np.testing.assert_array_equal(a[outside], b[outside],
                                              err_msg=f"{name}: staff/cape/tool/body moved outside leg selection")

    def test_blue_headband_survives_source_sampling_and_joint_palette(self):
        images = [cast.fit(cast.source("alethea", "front"))] + cast.backs("alethea")
        for image in images:
            a = np.array(image).astype(int)
            self.assertGreater(np.count_nonzero((a[:, :, 2] > a[:, :, 0] * 1.3)
                                                & (a[:, :, 2] > a[:, :, 1] * 1.3)
                                                & (a[:, :, 3] != 0)), 0)
        for path in (cast.FRONT / "alethea.png", cast.BACK / "alethea.png"):
            a = np.array(self.outputs[path].convert("RGBA")).astype(int)
            self.assertGreater(np.count_nonzero((a[:, :, 2] > a[:, :, 0] * 1.3)
                                                & (a[:, :, 2] > a[:, :, 1] * 1.3)
                                                & (a[:, :, 3] != 0)), 0)

    def test_back_heads_are_fixed_and_contacts_are_occupied(self):
        for name in ("kleon", "alethea"):
            frames = cast.backs(name)
            for frame in frames[:3]:
                np.testing.assert_array_equal(np.array(frame)[0:31, 18:53],
                                              np.array(frames[3])[0:31, 18:53])
            for frame, point in zip(frames, ((8, 38), (9, 18), (56, 38))):
                self.assertEqual(frame.getpixel(point)[3], 255)
            for frame in frames:
                # Whole hands/forearms fit; only the waist reaches the bottom.
                self.assertIsNone(frame.crop((0, 0, 1, 63)).getbbox())
                self.assertIsNone(frame.crop((63, 0, 64, 63)).getbbox())
        self.assertEqual(cast.backs("alethea")[1].getpixel((1, 30))[3], 0,
                         "the upper-arm selection must not retain detached spill")

    def test_existing_model_orb_caps_and_lights_survive_quantization(self):
        for name in ("kleon", "alethea"):
            sheet = self.outputs[cast.BACK / f"{name}.png"].convert("RGBA")
            for frame, (x, y) in enumerate(((8, 38), (9, 18))):
                a = np.array(sheet.crop((x - 4, frame * 64 + y - 5,
                                         x + 5, frame * 64 + y + 5))).astype(int)
                opaque = a[:, :, 3] != 0
                self.assertTrue(np.any(opaque & (a[:, :, 0] > a[:, :, 1] * 2)
                                       & (a[:, :, 0] > a[:, :, 2] * 2)),
                                f"{name} frame{frame} model-red cap")
                self.assertTrue(np.any(opaque & (a[:, :, :3].min(axis=2) >= 168)
                                       & (np.ptp(a[:, :, :3], axis=2) < 48)),
                                f"{name} frame{frame} model-light orb")

    def test_piece_registration_copies_source_pixels_without_mirroring(self):
        image = Image.new("RGBA", (16, 16))
        image.putpixel((3, 3), (248, 160, 112, 255))
        image.putpixel((5, 4), (112, 64, 40, 255))
        piece = cast.place_piece(image, [(0, 0), (15, 0), (15, 15), (0, 15)],
                                 ((2, 2), (6, 2)), ((20, 20), (24, 20)))
        self.assertEqual(piece.getpixel((21, 21)), image.getpixel((3, 3)))
        self.assertEqual(piece.getpixel((23, 22)), image.getpixel((5, 4)))

    def test_broad_red_does_not_consume_linen_or_ochre(self):
        image = Image.new("RGBA", (40, 40), (176, 48, 32, 255))
        image.paste((248, 232, 200, 255), (0, 0, 12, 40))
        image.paste((208, 144, 48, 255), (12, 0, 24, 40))
        result = cast.indexed(image, cast.palette([image])).convert("RGBA")
        for point, expected in (((4, 4), (248, 232, 200)),
                                ((16, 4), (208, 144, 48)),
                                ((30, 4), (176, 48, 32))):
            self.assertEqual(result.getpixel(point)[:3], expected)

    def test_cami_wheat_is_on_shawl_without_repainting_or_moving_the_figure(self):
        original = np.array(cast.opaque(cast.source("cami", "front")))
        assembled = np.array(cast.cami_front())
        np.testing.assert_array_equal(original[:, :, 3], assembled[:, :, 3])
        np.testing.assert_array_equal(original[140:650, 100:480],
                                      assembled[140:650, 100:480])
        source_colors = {tuple(p) for p in original.reshape(-1, 4)}
        self.assertTrue(all(tuple(p) in source_colors
                            for p in assembled.reshape(-1, 4)))

        def gold(image):
            a = np.array(image).astype(int)
            return ((a[:, :, 1] > a[:, :, 2] * 1.8)
                    & (a[:, :, 1] >= 100) & (a[:, :, 0] > a[:, :, 1])
                    & (a[:, :, 3] != 0))

        self.assertGreater(np.count_nonzero(gold(cast.source("cami", "front"))[316:569, 490:615]), 0)
        self.assertEqual(np.count_nonzero(gold(cast.cami_front())[316:569, 490:615]), 0)
        for image in (cast.fit(cast.cami_front()),
                      self.outputs[cast.FRONT / "cami.png"].convert("RGBA")):
            self.assertGreater(np.count_nonzero(gold(image)[46:62, 8:25]), 0)
            self.assertEqual(np.count_nonzero(gold(image)[8:43, 40:57]), 0)

    def test_legacy_guard_is_exact_and_explicit(self):
        for path in cast.OWNED:
            target = cast.ROOT / path
            with self.subTest(path=path):
                self.assertTrue(cast.is_owned(target))
                before = target.read_bytes()
                with self.assertRaisesRegex(RuntimeError, r"model_cast\.py --write"):
                    save_indexed(np.zeros((1, 1), dtype=np.uint8), None, target)
                self.assertEqual(target.read_bytes(), before)
        for path in (cast.PEOPLE / "fisher.png", cast.PEOPLE / "halia.png",
                     cast.FRONT / "brendan.png"):
            self.assertFalse(cast.is_owned(cast.ROOT / path))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "unowned.png"
            save_indexed(np.zeros((8, 8)), Palette([]), path)
            self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
