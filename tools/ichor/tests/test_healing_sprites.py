import sys
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import field_effects as effects


class HealingSpriteTests(unittest.TestCase):
    def test_selected_sources_and_palettes_reproduce(self):
        bright, dim = effects.monitor_frames()
        for name, pixels, palette, size in (
            ("pokecenter_monitor/0.png", bright, effects.GENERAL_0, (24, 16)),
            ("pokecenter_monitor/1.png", dim, effects.GENERAL_0, (24, 16)),
            ("pokeball_glow.png", effects.ball_frame(), effects.BALL, (8, 8)),
        ):
            with self.subTest(effect=name):
                path = Path(effects.PICS) / name
                with Image.open(path) as image:
                    self.assertEqual(image.mode, "P")
                    self.assertEqual(image.size, size)
                    self.assertEqual(image.info.get("transparency"), 0)
                    self.assertEqual(image.getpalette(), palette.flat())
                    np.testing.assert_array_equal(np.array(image), pixels)
                self.assertEqual(path.read_bytes()[24], 4)

    def test_relief_pulse_remains_registered_and_connected(self):
        bright, dim = effects.monitor_frames()
        np.testing.assert_array_equal(bright != 0, dim != 0)
        self.assertFalse(np.array_equal(bright, dim))
        ys, xs = np.nonzero(bright)
        self.assertEqual((xs.min(), xs.max(), ys.min(), ys.max()), (5, 11, 1, 15))
        pending = [(7, 1)]
        visited = set()
        while pending:
            x, y = pending.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            pending.extend(
                (nx, ny)
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
                if 0 <= nx < 24 and 0 <= ny < 16 and bright[ny, nx] != 0
            )
        self.assertEqual(len(visited), len(xs))

    def test_orb_flash_and_unflashed_waterline_roles(self):
        pixels = effects.ball_frame()
        self.assertTrue({2, 3, 5, 6, 8}.issubset(set(pixels.flat)))
        self.assertEqual(set(pixels[5:7].flat), {0, 12, 13})
        self.assertTrue(np.all(pixels[[0, 7]] == 0))


if __name__ == "__main__":
    unittest.main()
