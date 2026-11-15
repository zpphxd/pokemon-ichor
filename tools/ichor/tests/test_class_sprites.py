import sys
import unittest
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import sprites_classes as classes


class ClassSpriteTests(unittest.TestCase):
    def test_native_sources_and_palettes_reproduce(self):
        for name, painter in classes.CLASSES.items():
            with self.subTest(portrait=name):
                figure, palette = painter()
                path = Path(classes.FRONT) / (name + ".png")
                with Image.open(path) as image:
                    self.assertEqual(image.mode, "P")
                    self.assertEqual(image.size, (64, 64))
                    self.assertEqual(image.info.get("transparency"), 0)
                    self.assertEqual(image.getpalette(), palette.flat())
                    np.testing.assert_array_equal(np.array(image), classes.render(figure))
                self.assertEqual(path.read_bytes()[24], 4)

    def test_lamp_and_raised_arm_are_connected(self):
        figure, _ = classes.acolyte_f()
        pixels = classes.render(figure)
        start = (14, 15)
        self.assertNotEqual(pixels[start[1], start[0]], 0)
        visited = {start}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if (0 <= nx < 64 and 0 <= ny < 64
                        and pixels[ny, nx] != 0 and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        self.assertIn((34, 30), visited)


if __name__ == "__main__":
    unittest.main()
