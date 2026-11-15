import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import player_unused


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

    def test_existing_faces_and_feet_are_not_clipped(self):
        for who, (_, _, roles) in player_unused.player.CHARS.items():
            sources = player_unused.watering(who) + player_unused.decorating(who)
            for index, source in enumerate(sources):
                frame = player_unused.player.to_index([source], roles)
                self.assertTrue(np.any(frame[30] == roles["b"]))
                self.assertFalse(np.any(frame[:10]))
                facing = ("down", "up", "left")[index // 2] if index < 6 else "down"
                face = player_unused.player.parse(player_unused.player.FACES[who][facing])
                x, y = (8, 16) if index < 6 else (0, 19)
                for dy, row in enumerate(face):
                    for dx, role in enumerate(row):
                        if role != ".":
                            self.assertEqual(frame[y + dy, x + dx], roles[role])


if __name__ == "__main__":
    unittest.main()
