import copy
import shutil
import struct
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "art"))
import check_legacy_players as legacy


class LegacyPlayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = legacy.load_manifest()
        cls.compiled = legacy.check_sources(legacy.ROOT, cls.manifest)

    def copied_sources(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        paths = [legacy.PEOPLE / row["path"] for row in self.manifest["files"]]
        paths += [legacy.PALETTES / f"{name}.pal" for name in self.manifest["palettes"]]
        for path in paths:
            (root / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(legacy.ROOT / path, root / path)
        return root

    def synthetic_rom(self, start=0x100):
        rom, symbols = bytearray(start), {}
        for name, data in self.compiled.items():
            symbols[name] = (0x08000000 + len(rom), len(data), "R")
            rom.extend(data)
        return rom, symbols

    def test_all_sources_and_required_arrays(self):
        self.assertEqual(len(self.manifest["files"]), 22)
        self.assertEqual(set(self.compiled), legacy.LINK_SYMBOLS | legacy.PALETTE_SYMBOLS)
        self.assertEqual(sum(len(self.compiled[name]) for name in legacy.LINK_SYMBOLS), 4 * 2304)
        self.assertEqual(sum(len(self.compiled[name]) for name in legacy.PALETTE_SYMBOLS), 3 * 32)

    def test_no_network_used_for_source_check(self):
        with patch("socket.socket", side_effect=AssertionError("network forbidden")):
            self.assertEqual(legacy.check_sources(legacy.ROOT, self.manifest), self.compiled)

    def test_source_check_never_writes_files(self):
        root = self.copied_sources()
        before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
        with patch.object(Image.Image, "save", side_effect=AssertionError("art write forbidden")):
            legacy.check_sources(root, self.manifest)
        after = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_every_partition_and_provenance_is_pinned(self):
        counts, frames = {}, {}
        for row in self.manifest["files"]:
            part = row["partition"]
            counts[part] = counts.get(part, 0) + 1
            frames[part] = frames.get(part, 0) + self.manifest["layouts"][row["layout"]]["frames"]
            self.assertIn(row["original"], self.manifest["originals"])
            self.assertTrue(row["original_path"].endswith(".png"))
        self.assertEqual({key: (counts[key], frames[key]) for key in counts}, legacy.PARTITIONS)
        self.assertEqual(sum(frames.values()), 208)
        self.assertEqual(self.manifest["expansion"]["revision"],
                         "79dd436920845ebc145577649de624f65298c209")

    def test_orphans_keep_original_npc_white_roles(self):
        for row in self.manifest["files"]:
            if row["partition"] == "orphan-frlg-rs":
                self.assertEqual(row["palette"], "npc_white")
                self.assertEqual(row["original"], "frlg")
                self.assertNotIn("symbol", row)

    def test_relocated_rom_arrays_use_resolved_symbols(self):
        for start in (0x80, 0x1900):
            rom, symbols = self.synthetic_rom(start)
            legacy.check_rom(rom, symbols, self.compiled, self.manifest)

    def test_each_missing_required_current_symbol_fails(self):
        rom, symbols = self.synthetic_rom()
        for name in self.compiled:
            with self.subTest(name=name):
                missing = symbols.copy()
                del missing[name]
                with self.assertRaisesRegex(ValueError, "required current symbol missing"):
                    legacy.check_rom(rom, missing, self.compiled, self.manifest)

    def test_each_changed_rom_array_fails(self):
        rom, symbols = self.synthetic_rom()
        for name in self.compiled:
            with self.subTest(name=name):
                changed = rom.copy()
                changed[symbols[name][0] - 0x08000000] ^= 1
                with self.assertRaisesRegex(ValueError, "ROM bytes differ"):
                    legacy.check_rom(changed, symbols, self.compiled, self.manifest)

    def test_wrong_symbol_size_type_and_rom_bounds_fail(self):
        rom, symbols = self.synthetic_rom()
        name = next(iter(self.compiled))
        address, size, _ = symbols[name]
        for value, message in (((address, size - 1, "R"), "size/type"),
                               ((address, size, "T"), "size/type"),
                               ((0x02000000, size, "R"), "outside selected ROM"),
                               ((0x08000000 + len(rom), size, "R"), "outside selected ROM")):
            with self.subTest(value=value):
                wrong = dict(symbols, **{name: value})
                with self.assertRaisesRegex(ValueError, message):
                    legacy.check_rom(rom, wrong, self.compiled, self.manifest)

    def test_each_unexpected_dormant_symbol_fails(self):
        rom, symbols = self.synthetic_rom()
        for name in self.manifest["absent_symbols"]:
            with self.subTest(name=name):
                wrong = dict(symbols, **{name: (0x08000000, 32, "R")})
                with self.assertRaisesRegex(ValueError, "partition changed"):
                    legacy.check_rom(rom, wrong, self.compiled, self.manifest)

    def test_missing_or_added_source_fails(self):
        root = self.copied_sources()
        path = root / legacy.PEOPLE / "rs_may.png"
        path.rename(path.with_name("unassigned.png"))
        with self.assertRaisesRegex(ValueError, "source inventory differs"):
            legacy.check_sources(root, self.manifest)

    def test_modified_source_indices_fail(self):
        root = self.copied_sources()
        path = root / legacy.PEOPLE / "rs_may.png"
        with Image.open(path) as image:
            image.putpixel((8, 16), image.getpixel((8, 16)) ^ 1)
            image.save(path, bits=4, transparency=0)
        with self.assertRaisesRegex(ValueError, "native index hash changed"):
            legacy.check_sources(root, self.manifest)

    def test_modified_dimensions_fail(self):
        root = self.copied_sources()
        path = root / legacy.PEOPLE / "rs_may.png"
        with Image.open(path) as image:
            image.crop((0, 0, 128, 32)).save(path, bits=4, transparency=0)
        with self.assertRaisesRegex(ValueError, "dimensions changed"):
            legacy.check_sources(root, self.manifest)

    def test_modified_hardware_palette_fails(self):
        root = self.copied_sources()
        path = root / legacy.PALETTES / "npc_white.pal"
        lines = path.read_text().splitlines()
        lines[4] = "0 0 0"
        path.write_text("\n".join(lines) + "\n")
        with self.assertRaisesRegex(ValueError, "hardware palette hash changed"):
            legacy.check_sources(root, self.manifest)

    def test_modified_embedded_palette_fails(self):
        root = self.copied_sources()
        path = root / legacy.PEOPLE / "rs_may.png"
        with Image.open(path) as image:
            palette = image.getpalette()
            palette[3:6] = [0, 0, 0]
            image.putpalette(palette)
            image.save(path, bits=4, transparency=0)
        with self.assertRaisesRegex(ValueError, "embedded hardware palette"):
            legacy.check_sources(root, self.manifest)

    def test_dimension_hash_is_checked_separately(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["layouts"]["walker"]["dimension_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "dimension hash changed"):
            legacy.check_sources(legacy.ROOT, manifest)

    def test_modified_png_metadata_fails_source_hash(self):
        root = self.copied_sources()
        path = root / legacy.PEOPLE / "rs_may.png"
        # Trailing bytes leave decoded dimensions/indices/colors unchanged.
        with path.open("ab") as file:
            file.write(b"changed metadata")
        with self.assertRaisesRegex(ValueError, "source byte hash changed"):
            legacy.check_sources(root, self.manifest)

    def test_truncated_rom_fails(self):
        rom, symbols = self.synthetic_rom()
        with self.assertRaisesRegex(ValueError, "outside selected ROM"):
            legacy.check_rom(rom[:128], symbols, self.compiled, self.manifest)

    def test_missing_elf_is_not_success_skipped(self):
        with self.assertRaisesRegex(ValueError, "matching ELF missing"):
            legacy.resolve_symbols(Path("/nonexistent/legacy-test.elf"))

    def test_missing_nm_is_actionable_failure(self):
        with tempfile.NamedTemporaryFile() as elf:
            with patch.object(legacy.shutil, "which", return_value=None):
                with self.assertRaisesRegex(ValueError, "arm-none-eabi-nm missing"):
                    legacy.resolve_symbols(Path(elf.name))

    def test_symbol_resolution_rejects_ambiguous_required_arrays(self):
        name = next(iter(legacy.LINK_SYMBOLS))
        result = type("Result", (), {"stdout": f"08001000 00000900 R {name}\n"
                                              f"08002000 00000900 R {name}\n"})()
        with tempfile.NamedTemporaryFile() as elf:
            with patch.object(legacy.subprocess, "run", return_value=result):
                with self.assertRaisesRegex(ValueError, "ambiguous ELF symbol"):
                    legacy.resolve_symbols(Path(elf.name), "arm-none-eabi-nm")

    def test_size_less_defined_symbols_remain_visible(self):
        name = self.manifest["absent_symbols"][0]
        result = type("Result", (), {"stdout": f"08001000 A {name}\n"})()
        with tempfile.NamedTemporaryFile() as elf:
            with patch.object(legacy.subprocess, "run", return_value=result):
                symbols = legacy.resolve_symbols(Path(elf.name), "arm-none-eabi-nm")
        self.assertIn(name, symbols)
        self.assertIsNone(symbols[name][1])

    def test_native_tile_order_and_nibbles(self):
        pixels = bytes(x % 16 for y in range(32) for x in range(32))
        result = legacy.native_tiles(pixels, 32, 32, 16)
        self.assertEqual(len(result), 512)
        self.assertEqual(result[:4], bytes([0x10, 0x32, 0x54, 0x76]))
        self.assertEqual(result[32:36], bytes([0x98, 0xBA, 0xDC, 0xFE]))
        # A distinctive second source frame must follow all eight first-frame tiles.
        pixels = bytes(1 if x < 16 else 2 for y in range(32) for x in range(32))
        self.assertEqual(legacy.native_tiles(pixels, 32, 32, 16),
                         bytes([0x11]) * 256 + bytes([0x22]) * 256)

    def test_original_expanded_channels_truncate_without_rewriting(self):
        colors = [[255, 197, 148]] * 16
        expected = struct.pack("<H", 31 | (24 << 5) | (18 << 10)) * 16
        self.assertEqual(legacy.hardware_palette(colors), expected)

    def test_manifest_cannot_omit_required_arrays(self):
        manifest = copy.deepcopy(self.manifest)
        del manifest["files"][0]
        with patch.object(legacy.json, "loads", return_value=manifest):
            with self.assertRaisesRegex(ValueError, "all 22 unique sources"):
                legacy.load_manifest()


if __name__ == "__main__":
    unittest.main()
