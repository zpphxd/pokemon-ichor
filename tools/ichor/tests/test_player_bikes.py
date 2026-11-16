import sys
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import player_bikes as bikes
import player_sources


class RetainedBikeArtTests(unittest.TestCase):
    def test_complete_written_sources(self):
        bikes.check()

    def test_all_native_pedal_phases_are_distinct(self):
        for who in bikes.FOLDERS:
            for kind in ("mach_bike", "acro_bike"):
                frames = bikes.frames(who, kind)
                for first, second in ((3, 4), (5, 6), (7, 8)):
                    self.assertFalse(np.array_equal(frames[first], frames[second]))
                if kind == "acro_bike":
                    for first, second in ((21, 22), (23, 24), (25, 26)):
                        self.assertFalse(np.array_equal(frames[first], frames[second]))

    def test_bicycle_contact_planes_are_unchanged_in_every_source_frame(self):
        for who in bikes.FOLDERS:
            for kind, specs in (("mach_bike", bikes.NORMAL), ("acro_bike", bikes.ACRO)):
                original = np.array(Image.open(bikes.BASE / f"{who}_{kind}.png"))
                actual = np.hsplit(np.array(Image.open(bikes.path(who, kind))), len(specs))
                for index, (frame, (_, plane, _, _)) in enumerate(zip(actual, specs)):
                    retained = original[:, index * 32:(index + 1) * 32]
                    self.assertTrue(np.array_equal(frame[plane:],
                                                   retained[plane:]))
                    for x0, y0, x1, y1 in bikes.VEHICLE_EXTRAS.get(index, []):
                        with self.subTest(who=who, kind=kind, source=index, rectangle=(x0, y0, x1, y1)):
                            self.assertTrue(np.array_equal(frame[y0:y1, x0:x1],
                                                           retained[y0:y1, x0:x1]))

    def test_all_frames_match_canonical_model_source_identity(self):
        for who in bikes.FOLDERS:
            for kind in ("mach_bike", "acro_bike"):
                name, row = player_sources.asset(who, kind)
                self.assertEqual(player_sources.digest(player_sources.ROOT / name), row["sha256"])
                self.assertTrue(np.array_equal(np.hstack(bikes.frames(who, kind)),
                                               np.array(player_sources.source_image(who, kind))))


if __name__ == "__main__":
    unittest.main()
