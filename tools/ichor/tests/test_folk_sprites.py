import sys
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import sprites_folk as folk
import human_classes as humans


class FolkSpriteTests(unittest.TestCase):
    def test_all_sources_reproduce_pngs(self):
        for spec in folk.WALKERS:
            with self.subTest(walker=spec["name"]):
                path = Path(folk.OUT_DIR) / (spec["name"] + ".png")
                with Image.open(path) as image:
                    if ("walkers", spec["name"]) in humans.BY_KEY:
                        with humans.source_image("walkers", spec["name"]) as authored:
                            expected = np.array(authored)
                    else:
                        expected = folk.build_sheet(spec)
                    np.testing.assert_array_equal(expected, np.array(image))

    def test_akti_states_are_complete_and_distinct(self):
        for name in ("sailor", "diver", "healer", "kid_f", "augur", "acolyte_m",
                     "acolyte_f", "merchant", "goatherd", "hoplite"):
            with self.subTest(walker=name):
                count = 10 if name == "healer" else 9
                sheet = folk.build_sheet(folk.BY_NAME[name])
                self.assertEqual(sheet.shape, (32, count * 16))
                frames = {sheet[:, i * 16:(i + 1) * 16].tobytes() for i in range(count)}
                self.assertEqual(len(frames), count)

    def test_bow_keeps_the_rod_planted(self):
        sheet = folk.build_sheet(folk.HEALER)
        np.testing.assert_array_equal(sheet[:, :3], sheet[:, 144:147])

    def test_preview_includes_the_entire_tenth_frame(self):
        sheets = {
            "kid_f": folk.build_sheet(folk.KID_F),
            "healer": folk.build_sheet(folk.HEALER),
        }
        preview = folk.sheet_preview(sheets, cols=1)
        self.assertEqual(preview.size, (904, 416))
        bow = folk.to_rgba(sheets["healer"][:, 144:160], folk.FOLK_PAL)
        tile = folk.checker_bg(16, 32)
        tile.alpha_composite(bow)
        np.testing.assert_array_equal(
            np.array(preview.crop((840, 288, 904, 416))),
            np.array(folk.upscale(tile, 4)),
        )


if __name__ == "__main__":
    unittest.main()
