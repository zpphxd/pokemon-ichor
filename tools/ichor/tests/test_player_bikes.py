import sys
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import player_bikes as bikes


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
                for index, (frame, (_, plane, _, _)) in enumerate(zip(bikes.frames(who, kind), specs)):
                    self.assertTrue(np.array_equal(frame[plane:],
                                                   original[plane:, index * 32:(index + 1) * 32]))

    def test_all_existing_identity_faces_are_present(self):
        for who in bikes.FOLDERS:
            roles = bikes.player.CHARS[who][2]
            for frame, (facing, plane, _, lean) in zip(bikes.frames(who, "acro_bike"), bikes.ACRO):
                x = 8 + (lean if facing == "left" else 0)
                y = max(0, plane - 19) + 6
                for dy, row in enumerate(bikes.player.parse(bikes.player.FACES[who][facing])):
                    for dx, role in enumerate(row):
                        if role != ".":
                            self.assertEqual(frame[y + dy, x + dx], roles[role])


if __name__ == "__main__":
    unittest.main()
