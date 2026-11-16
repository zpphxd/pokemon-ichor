import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import human_classes as humans
import human_classes_render as rendered


class HumanClassTests(unittest.TestCase):
    def test_rendered_pixel_gate_rejects_even_one_obscured_pixel(self):
        pixels = np.arange(18, dtype=np.uint8).reshape((3, 2, 3)) + 10
        mask = np.ones((3, 2), dtype=bool)
        screen = np.zeros((8, 8, 3), dtype=np.uint8)
        screen[2:5, 3:5] = pixels
        self.assertEqual(rendered.locate(screen, pixels, mask), [3, 2, 5, 5])
        screen[3, 4, 0] += 1
        with self.assertRaisesRegex(ValueError, "expected one complete, unobscured"):
            rendered.locate(screen, pixels, mask)

    def test_exact_native_source_union_reproduces(self):
        humans.validate()
        self.assertEqual(len([a for a in humans.ASSETS if a["kind"] == "walkers"]), 22)
        self.assertEqual(len([a for a in humans.ASSETS if a["kind"] == "portraits"]), 10)
        for entry in humans.ASSETS:
            with self.subTest(asset=entry["target"]):
                self.assertEqual(humans.digest(humans.ROOT / entry["target"]), entry["sha256"])

    def test_all_199_field_frames_are_complete_distinct_and_anchored(self):
        total = 0
        for entry in humans.ASSETS:
            if entry["kind"] != "walkers":
                continue
            with humans.source_image("walkers", entry["name"]) as image:
                sheet = np.array(image)
                frames = [sheet[:, x:x + 16] for x in range(0, image.width, 16)]
                self.assertEqual(len({frame.tobytes() for frame in frames}), len(frames))
                for i, frame in enumerate(frames):
                    ys, xs = np.nonzero(frame)
                    self.assertGreater(xs.min(), 0)
                    self.assertLess(xs.max(), 15)
                    self.assertEqual(ys.max(), 30 if i in (0, 1, 2, 9) else 31)
                    if 3 <= i <= 8:
                        idle_y = np.nonzero(frames[(i - 3) // 2])[0]
                        self.assertLessEqual(abs((ys.max() - ys.min()) - (idle_y.max() - idle_y.min())), 1)
                total += len(frames)
        self.assertEqual(total, 199)

    def test_corrected_upper_bodies_and_props_are_model_pixel_exact(self):
        for name, source, destination, rows, columns in (
                ("elder_m", 3, 4, 26, 3), ("shepherd", 7, 8, 28, 4), ("woman", 5, 6, 29, 0)):
            with humans.source_image("walkers", name) as image:
                sheet = np.array(image)
            a, b = [sheet[:, i * 16:(i + 1) * 16] for i in (source, destination)]
            np.testing.assert_array_equal(a[:rows], b[:rows])
            np.testing.assert_array_equal(a[:, :columns], b[:, :columns])
            self.assertFalse(np.array_equal(a[rows:], b[rows:]))

    def test_healer_bow_lowers_head_but_keeps_rod_and_feet(self):
        with humans.source_image("walkers", "healer") as image:
            sheet = np.array(image)
        stand, bow = sheet[:, :16], sheet[:, 144:160]
        np.testing.assert_array_equal(stand[30] > 0, bow[30] > 0)
        self.assertTrue(np.all(stand[15:31, 3] > 0))
        self.assertTrue(np.all(bow[15:31, 3] > 0))
        self.assertGreater(np.nonzero(bow[:, 7:13])[0].min(), np.nonzero(stand[:, 7:13])[0].min())

    def test_goatherd_uses_existing_gray_and_legacy_fronts_stay_unchanged(self):
        with humans.source_image("walkers", "goatherd") as image:
            sheet = np.array(image)
        for i in range(9):
            self.assertGreater(np.count_nonzero(sheet[:, i * 16:(i + 1) * 16] == 10), 8)
        for relative, expected in humans.MANIFEST["retained_legacy"].items():
            self.assertEqual(humans.digest(humans.ROOT / relative), expected)


if __name__ == "__main__":
    unittest.main()
