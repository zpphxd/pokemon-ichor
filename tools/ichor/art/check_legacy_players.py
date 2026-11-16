#!/usr/bin/env python3
"""Offline read-only checks for accepted genuine Gen 3 legacy player sprites.

python3 tools/ichor/art/check_legacy_players.py --rom pokeemerald.gba

Checks never rewrite art, palettes or manifests. The ROM and its matching ELF
are required; missing current link symbols fail rather than skipping coverage.
This checks compiled source fidelity, not live peer-link/controller gameplay.
"""
import argparse
import hashlib
import json
import shutil
import struct
import subprocess
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = Path(__file__).with_name("legacy_players.json")
PEOPLE = Path("graphics/object_events/pics/people")
PALETTES = Path("graphics/object_events/palettes")
PARTITIONS = {
    "compiled-link": (4, 36),
    "rs-running-gc": (2, 18),
    "orphan-frlg-rs": (2, 18),
    "frlg-gated": (14, 136),
}
LINK_SYMBOLS = {
    "gObjectEventPic_Red", "gObjectEventPic_Leaf",
    "gObjectEventPic_RubySapphireBrendanNormal", "gObjectEventPic_RubySapphireMayNormal",
}
PALETTE_SYMBOLS = {
    "gObjectEventPal_RedLeaf",
    "gObjectEventPal_RubySapphireBrendan", "gObjectEventPal_RubySapphireMay",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_manifest(path=MANIFEST):
    manifest = json.loads(path.read_text())
    require(manifest["schema"] == 1, "unsupported legacy manifest schema")
    files = manifest["files"]
    require(len(files) == 22 and len({row["path"] for row in files}) == 22,
            "manifest must preserve all 22 unique sources")
    counts, frames = Counter(), Counter()
    for row in files:
        require(row["partition"] in PARTITIONS, f"{row['path']}: unknown partition")
        layout = manifest["layouts"][row["layout"]]
        counts[row["partition"]] += 1
        frames[row["partition"]] += layout["frames"]
        require(layout["dimensions"] == [layout["frame_width"] * layout["frames"], 32],
                f"{row['path']}: invalid native frame layout")
        require(row["original"] in manifest["originals"], f"{row['path']}: missing provenance")
        require(("symbol" in row) == (row["partition"] == "compiled-link"),
                f"{row['path']}: compiled/dormant partition mismatch")
    require({key: (counts[key], frames[key]) for key in counts} == PARTITIONS,
            "manifest must preserve the 36/18/18/136 source-frame partitions")
    require({row["symbol"] for row in files if "symbol" in row} == LINK_SYMBOLS,
            "manifest must preserve all four required current link symbols")
    require({row["symbol"] for row in manifest["palettes"].values() if row["symbol"]}
            == PALETTE_SYMBOLS, "manifest must preserve all three required palette arrays")
    require(not (set(manifest["absent_symbols"]) & (LINK_SYMBOLS | PALETTE_SYMBOLS)),
            "required current symbols cannot be classified as absent")
    for provenance in [manifest["expansion"], *manifest["originals"].values()]:
        revision = provenance["revision"]
        require(len(revision) == 40 and all(c in "0123456789abcdef" for c in revision),
                "original revision provenance must be pinned")
    return manifest


def inside(root, path):
    result = (root / path).resolve()
    require(result.is_relative_to(root.resolve()), f"path outside repository: {path}")
    return result


def hardware_palette(colors):
    require(len(colors) == 16 and all(len(c) == 3 for c in colors),
            "expected sixteen RGB palette entries")
    require(all(isinstance(v, int) and 0 <= v <= 255 for c in colors for v in c),
            "palette channels must be RGB bytes")
    return b"".join(struct.pack("<H", (r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10))
                    for r, g, b in colors)


def palette_bytes(path):
    lines = path.read_text().splitlines()
    require(lines[:3] == ["JASC-PAL", "0100", "16"] and len(lines) == 19,
            f"{path}: expected a sixteen-color JASC palette")
    return hardware_palette([list(map(int, line.split())) for line in lines[3:]])


def native_tiles(indices, width, height, frame_width):
    """gbagfx's -mwidth/-mheight frame-major 4bpp tile order, without writes."""
    require(width % frame_width == 0 and frame_width % 8 == 0 and height % 8 == 0,
            "invalid tile/frame dimensions")
    require(len(indices) == width * height and max(indices) <= 15,
            "invalid indexed native pixels")
    result = bytearray()
    for frame_x in range(0, width, frame_width):
        for tile_y in range(0, height, 8):
            for tile_x in range(frame_x, frame_x + frame_width, 8):
                for y in range(tile_y, tile_y + 8):
                    for x in range(tile_x, tile_x + 8, 2):
                        offset = y * width + x
                        result.append(indices[offset] | (indices[offset + 1] << 4))
    return bytes(result)


def check_sources(root, manifest):
    root = root.resolve()
    expected = {row["path"] for row in manifest["files"]}
    actual = set()
    for folder in ("ruby_sapphire_brendan", "ruby_sapphire_may", "red", "leaf"):
        actual.update(str(p.relative_to(root / PEOPLE))
                      for p in (root / PEOPLE / folder).glob("*.png"))
    for filename in ("rs_brendan.png", "rs_may.png", "red.png", "leaf.png"):
        if (root / PEOPLE / filename).is_file():
            actual.add(filename)
    require(actual == expected,
            f"legacy source inventory differs: missing {sorted(expected - actual)}, "
            f"added {sorted(actual - expected)}")
    compiled, colors = {}, {}
    for name, row in manifest["palettes"].items():
        data = palette_bytes(inside(root, PALETTES / f"{name}.pal"))
        require(digest(data) == row["hardware_sha256"], f"{name}: hardware palette hash changed")
        colors[name] = data
        if row["symbol"]:
            compiled[row["symbol"]] = data
    for row in manifest["files"]:
        path = inside(root, PEOPLE / row["path"])
        layout = manifest["layouts"][row["layout"]]
        with Image.open(path) as image:
            image.load()
            require(image.mode == "P", f"{row['path']}: expected indexed PNG")
            require(list(image.size) == layout["dimensions"], f"{row['path']}: dimensions changed")
            require(digest(struct.pack("<II", *image.size)) == layout["dimension_sha256"],
                    f"{row['path']}: dimension hash changed")
            require(image.info.get("transparency", 0) == 0, f"{row['path']}: index0 transparency")
            indices = image.tobytes()
            require(digest(indices) == row["index_sha256"], f"{row['path']}: native index hash changed")
            require(max(indices) <= 15, f"{row['path']}: invalid 4bpp indices")
            palette = image.getpalette()
            require(palette is not None and len(palette) >= 48, f"{row['path']}: missing palette")
            embedded = hardware_palette([palette[i:i + 3] for i in range(0, 48, 3)])
            require(embedded == colors[row["palette"]], f"{row['path']}: embedded hardware palette")
            if "symbol" in row:
                compiled[row["symbol"]] = native_tiles(indices, *image.size, layout["frame_width"])
        data = path.read_bytes()
        require(data[24] == 4, f"{row['path']}: expected 4bpp PNG depth")
        require(digest(data) == row["source_sha256"], f"{row['path']}: source byte hash changed")
    return compiled


def resolve_symbols(elf, nm=None):
    require(elf.is_file(), f"matching ELF missing: {elf}")
    tool = nm or shutil.which("arm-none-eabi-nm")
    require(tool is not None, "arm-none-eabi-nm missing; load the native build environment")
    result = subprocess.run([tool, "--defined-only", "--print-size", str(elf)],
                            check=True, capture_output=True, text=True)
    symbols = {}
    for line in result.stdout.splitlines():
        fields = line.split()
        if len(fields) == 4:
            address, size, kind, name = fields
            size = int(size, 16)
        elif len(fields) == 3:
            address, kind, name = fields
            size = None  # Absolute constants have no size but are still defined.
        else:
            continue
        if name in LINK_SYMBOLS | PALETTE_SYMBOLS:
            require(name not in symbols, f"ambiguous ELF symbol: {name}")
        symbols[name] = (int(address, 16), size, kind)
    return symbols


def check_rom(rom, symbols, compiled, manifest):
    require(set(compiled) == LINK_SYMBOLS | PALETTE_SYMBOLS,
            "source gate did not produce all seven required arrays")
    for name, expected in compiled.items():
        require(name in symbols, f"required current symbol missing: {name}")
        address, size, kind = symbols[name]
        require(kind.upper() == "R" and size == len(expected), f"{name}: ROM array size/type changed")
        # Architectural GBA ROM base, not an asset address. Every asset's address
        # and size come from the selected matching ELF.
        offset = address - 0x08000000
        require(0 <= offset and offset + size <= len(rom), f"{name}: outside selected ROM")
        require(rom[offset:offset + size] == expected, f"{name}: selected ROM bytes differ from source")
    unexpected = sorted(set(manifest["absent_symbols"]) & set(symbols))
    require(not unexpected, f"GC/orphan/IS_FRLG partition changed: {unexpected}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--rom", type=Path)
    parser.add_argument("--elf", type=Path, help="defaults to the selected ROM's adjacent .elf")
    parser.add_argument("--nm", help="explicit arm-none-eabi-nm executable")
    args = parser.parse_args()
    try:
        manifest = load_manifest()
        compiled = check_sources(args.root, manifest)
        rom = args.rom if args.rom is not None else args.root / "pokeemerald.gba"
        elf = args.elf if args.elf is not None else rom.with_suffix(".elf")
        require(rom.is_file(), f"selected ROM missing: {rom}")
        check_rom(rom.read_bytes(), resolve_symbols(elf, args.nm), compiled, manifest)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f"LEGACY_PLAYER FAIL: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError) and error.stderr:
            print(error.stderr.rstrip(), file=sys.stderr)
        return 1
    print("LEGACY_PLAYER PASS: 22 sources / 208 frames / 5 hardware palettes; "
          "4 compiled link atlases / 36 frames / 3 palette arrays; dormant partitions retained")
    print("LEGACY_PLAYER NOTE: offline compiled-source fidelity, not live link/controller gameplay")
    return 0


if __name__ == "__main__":
    sys.exit(main())
