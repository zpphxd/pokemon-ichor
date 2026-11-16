import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import player_unused
import player_sources


class UnusedPlayerArtTests(unittest.TestCase):
    def test_all_sources_reproduce_native_pngs(self):
        player_unused.check(player_unused.build(), written=True)

    def test_watering_frame_order_and_all_pouring_phases(self):
        for who in player_unused.player.CHARS:
            arr = player_unused.build()[(who, "watering")]
            frames = np.hsplit(arr, 6)
            for facing in range(3):
                self.assertGreater(np.count_nonzero(frames[facing * 2]
                                                    != frames[facing * 2 + 1]), 0)
            self.assertEqual(arr.shape, (32, 192))

    def test_model_sources_preserve_frame_layout_and_original_ground_anchors(self):
        built = player_unused.build()
        for who in player_unused.player.CHARS:
            for kind in ("watering", "decorating"):
                _, contract = player_sources.asset(who, kind)
                frames = np.hsplit(built[(who, kind)], contract["source_frames"])
                canonical = np.array(player_sources.source_image(who, kind))
                self.assertTrue(np.array_equal(built[(who, kind)], canonical))
                for frame, bounds in zip(frames, contract["prior_source_frame_bounds"]):
                    self.assertGreater(np.count_nonzero(frame), 0)
                    self.assertEqual(np.nonzero(frame)[0].max() + 1, bounds[3])


if __name__ == "__main__":
    unittest.main()
