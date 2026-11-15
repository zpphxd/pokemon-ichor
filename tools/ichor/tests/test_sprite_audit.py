"""Regression tests for the redraw rollout's native asset gate."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

SPEC = importlib.util.spec_from_file_location("sprite_audit", Path(__file__).parents[1] / "sprite_audit.py")
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class SpriteAuditTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.colors = [(112, 192, 160)] + [(i * 8, i * 8, i * 8) for i in range(1, 16)]

    def image(self, name, size=(64, 64)):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        image = Image.new("P", size, 0)
        image.putpalette([channel for color in self.colors for channel in color])
        image.putpixel((1, 1), 1)
        image.save(path, transparency=0)
        return path

    def pal(self, name):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("JASC-PAL\n0100\n16\n"
                        + "".join(" ".join(map(str, color)) + "\n" for color in self.colors))
        return path

    def mon(self):
        folder = "graphics/pokemon/testmon"
        for name, size in audit.MON_SIZES.items():
            path = self.image(f"{folder}/{name}", size)
            if name != "footprint.png":
                frame_width = 32 if name in ("icon.png", "overworld.png") else 64
                frame_height = 32 if name in ("icon.png", "overworld.png") else 64
                with Image.open(path) as image:
                    for y in range(0, size[1], frame_height):
                        for x in range(0, size[0], frame_width):
                            image.putpixel((x + 1, y + 1), 1)
                    image.save(path, transparency=0)
            source = self.root / "design/dex/sprites/testmon" / name
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_bytes(path.read_bytes())
        for name in audit.MON_PALETTES:
            path = self.pal(f"{folder}/{name}")
            (self.root / "design/dex/sprites/testmon" / name).write_bytes(path.read_bytes())
        self.pal("graphics/pokemon/icon_palettes/pal0.pal")
        info = self.root / "src/data/pokemon/species_info/aethos_families.h"
        info.parent.mkdir(parents=True)
        info.write_text(".iconSprite = gMonIcon_Testmon,\n.iconPalIndex = 0,")

    def test_valid_mon_checks_all_views(self):
        self.mon()
        front, follower = audit.check_mon(self.root, "Testmon")
        self.assertEqual(front, [0])
        self.assertEqual(follower, [0, 0, 0])

    def test_rgb_concept_is_not_native_sprite(self):
        path = self.root / "concept.png"
        Image.new("RGB", (64, 64)).save(path)
        with self.assertRaisesRegex(ValueError, "indexed PNG"):
            audit.check_image(path)

    def test_wrong_dimensions_fail(self):
        path = self.image("wrong.png", (128, 128))
        with self.assertRaisesRegex(ValueError, "expected"):
            audit.check_image(path, (64, 64))

    def test_empty_sprite_fails(self):
        path = self.image("empty.png")
        with Image.open(path) as image:
            image.putpixel((1, 1), 0)
            image.save(path, transparency=0)
        with self.assertRaisesRegex(ValueError, "empty"):
            audit.check_image(path)

    def test_high_palette_index_fails(self):
        path = self.image("index.png")
        with Image.open(path) as image:
            image.putpalette(image.getpalette() + [0] * (768 - len(image.getpalette())))
            image.putpixel((1, 1), 16)
            image.save(path, bits=8)
        with self.assertRaisesRegex(ValueError, "indices 0..15"):
            audit.check_image(path)

    def test_wrong_transparency_fails(self):
        path = self.image("alpha.png")
        with Image.open(path) as image:
            image.save(path, transparency=1)
        with self.assertRaisesRegex(ValueError, "transparency"):
            audit.check_image(path)

    def test_non_gba_palette_fails(self):
        path = self.pal("wrong.pal")
        path.write_text(path.read_text().replace("8 8 8", "9 8 8"))
        with self.assertRaisesRegex(ValueError, "multiples of 8"):
            audit.palette(path)

    def test_existing_icon_palettes_allow_eight_bit_channels(self):
        path = self.pal("icon.pal")
        path.write_text(path.read_text().replace("8 8 8", "255 123 74"))
        self.assertEqual(audit.palette(path, native=False)[1], (255, 123, 74))

    def test_desynchronized_source_fails(self):
        self.mon()
        path = self.root / "design/dex/sprites/testmon/back.png"
        path.write_bytes(b"old source")
        with self.assertRaisesRegex(ValueError, "design sprite and ROM source differ"):
            audit.check_mon(self.root, "Testmon")

    def test_icon_engine_palette_mismatch_fails(self):
        self.mon()
        path = self.root / "graphics/pokemon/icon_palettes/pal0.pal"
        path.write_text(path.read_text().replace("8 8 8", "16 8 8"))
        with self.assertRaisesRegex(ValueError, "engine icon palette"):
            audit.check_mon(self.root, "Testmon")

    def test_frame_geometry_fails(self):
        path = self.image("motion.png", (65, 64))
        with self.assertRaisesRegex(ValueError, "does not divide"):
            audit.motion(path, (64, 64))

    def test_missing_animation_frame_fails(self):
        self.mon()
        path = self.root / "graphics/pokemon/testmon/anim_front.png"
        with Image.open(path) as image:
            image.putpixel((1, 65), 0)
            image.save(path, transparency=0)
        with self.assertRaisesRegex(ValueError, "empty frame"):
            audit.check_mon(self.root, "Testmon")

    def test_path_escape_fails(self):
        with self.assertRaises(ValueError):
            audit.inside(self.root, "../outside.png")

    def test_inventory_accounts_for_unplaced_assets(self):
        self.image("graphics/pokemon/unplaced/anim_front.png")
        self.pal("graphics/items/icon_palettes/jar.pal")
        self.image("graphics/trainers/front_pics/unused.png")
        maps = self.root / "data/maps"
        maps.mkdir(parents=True)
        (maps / "map_groups.json").write_text(json.dumps({"group_order": ["towns"], "towns": []}))
        result = audit.inventory(self.root)
        self.assertEqual(len(result["assets"]), 3)
        self.assertEqual(result["groups"], {"items": 1, "pokemon": 1, "trainers": 1})
        self.assertTrue(all(len(asset["sha256"]) == 64 for asset in result["assets"]))

    def test_changes_accounts_for_each_asset_once(self):
        before = {"schema_version": 1, "assets": [
            {"path": "graphics/unchanged.png", "sha256": "a" * 64},
            {"path": "graphics/changed.png", "sha256": "a" * 64},
            {"path": "graphics/removed.png", "sha256": "a" * 64},
        ]}
        after = {"schema_version": 1, "assets": [
            {"path": "graphics/changed.png", "sha256": "b" * 64},
            {"path": "graphics/unchanged.png", "sha256": "a" * 64},
            {"path": "graphics/added.png", "sha256": "c" * 64},
        ]}
        self.assertEqual(audit.inventory_changes(before, after), {
            "schema_version": 1,
            "added": ["graphics/added.png"],
            "removed": ["graphics/removed.png"],
            "changed": ["graphics/changed.png"],
            "unchanged_count": 1,
        })

    def test_changes_rejects_wrong_schema(self):
        with self.assertRaisesRegex(ValueError, "schema_version 1"):
            audit.inventory_changes({"schema_version": 2, "assets": []}, {})

    def test_changes_rejects_invalid_digest(self):
        snapshot = {"schema_version": 1, "assets": [
            {"path": "graphics/invalid.png", "sha256": "not a digest"},
        ]}
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            audit.inventory_changes(snapshot, snapshot)

    def test_changes_rejects_duplicate_assets(self):
        asset = {"path": "graphics/duplicate.png", "sha256": "a" * 64}
        snapshot = {"schema_version": 1, "assets": [asset, asset]}
        with self.assertRaisesRegex(ValueError, "duplicate inventory asset"):
            audit.inventory_changes(snapshot, snapshot)


if __name__ == "__main__":
    unittest.main()
