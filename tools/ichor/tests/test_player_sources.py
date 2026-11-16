import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import player_sources as sources


class PlayerCanonicalSourceTests(unittest.TestCase):
    def test_complete_native_coverage_and_palettes(self):
        self.assertEqual(sources.check(), {
            "pngs": 24, "source_frames": 186, "trainer_palettes": 2,
            "read_only_shared_palettes": 3,
        })

    def test_all_high_level_source_readers_use_pinned_native_pngs(self):
        for name, row in sources.manifest()["assets"].items():
            if not name.endswith(".png"):
                continue
            with self.subTest(path=name), Image.open(sources.ROOT / name) as image:
                actual = sources.source_image(row["identity"], row["state"])
                self.assertEqual(actual.tobytes(), image.tobytes())
                self.assertEqual(actual.getpalette(), image.getpalette())

    def test_legacy_writers_reject_exact_player_paths_and_shared_palettes(self):
        manifest = sources.manifest()
        for name in [*manifest["assets"], *manifest["read_only_shared_palettes"]]:
            with self.subTest(path=name), self.assertRaisesRegex(ValueError, "Legacy repainting is retired"):
                sources.reject_legacy_write(sources.ROOT / name)
        sources.reject_legacy_write(sources.ROOT / "graphics/trainers/front_pics/kleon.png")
        sources.reject_legacy_write(sources.ROOT / "graphics/object_events/palettes/npc_1.pal")

    def test_rejects_source_or_shared_palette_tampering(self):
        manifest = sources.manifest()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in [*manifest["assets"], *manifest["read_only_shared_palettes"]]:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(sources.ROOT / name, target)
            sources.check(root)
            for name in (next(iter(manifest["assets"])),
                         next(iter(manifest["read_only_shared_palettes"]))):
                with self.subTest(path=name):
                    target = root / name
                    saved = target.read_bytes()
                    target.write_bytes(saved + b"\n")
                    with self.assertRaisesRegex(ValueError, "differs|changed|Invalid"):
                        sources.check(root)
                    target.write_bytes(saved)

    def test_no_native_output_copy_writer_is_exposed(self):
        self.assertFalse(hasattr(sources, "write"))

    def test_selected_rom_arrays_require_symbols_sizes_bounds_and_exact_bytes(self):
        expected = {"required": b"\x12\x34\x56\x78"}
        symbols = {"required": (0x08000000, 4, "R")}
        sources.check_compiled_arrays(expected["required"], symbols, expected)
        for rom, actual in (
                (expected["required"], {}),
                (expected["required"], {"required": (0x08000000, 2, "R")}),
                (expected["required"], {"required": (0x08000000, 4, "B")}),
                (expected["required"], {"required": (0x08000004, 4, "R")}),
                (b"\x00" * 4, symbols)):
            with self.subTest(symbols=actual, rom=rom), self.assertRaises(ValueError):
                sources.check_compiled_arrays(rom, actual, expected)


if __name__ == "__main__":
    unittest.main()
