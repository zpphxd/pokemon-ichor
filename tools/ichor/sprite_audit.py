#!/usr/bin/env python3
"""Inventory sprite sources and check native Aethos sprite batches.

python3 tools/ichor/sprite_audit.py inventory --output build/sprite_inventory.json
python3 tools/ichor/sprite_audit.py changes --baseline build/sprite_inventory.json
python3 tools/ichor/sprite_audit.py provenance --reference <commit> --output build/sprite_provenance.json
python3 tools/ichor/sprite_audit.py check --pokemon Nebrel Kynder Hipling
python3 tools/ichor/sprite_audit.py check --image graphics/trainers/front_pics/kleon.png

Inventory hashes are coverage evidence, not artistic approval. Checks do not
replace reviewing native-size sprites or running the ROM's visual tests.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
MON_SIZES = {
    "anim_front.png": (64, 128),
    "back.png": (64, 64),
    "icon.png": (32, 64),
    "footprint.png": (16, 16),
    "overworld.png": (192, 32),
}
MON_PALETTES = ("normal.pal", "shiny.pal", "overworld_normal.pal", "overworld_shiny.pal")


def inside(root, name):
    path = (root / name).resolve()
    path.relative_to(root.resolve())
    return path


def palette(path, native=True):
    lines = path.read_text().splitlines()
    if lines[:3] != ["JASC-PAL", "0100", "16"] or len(lines) != 19:
        raise ValueError(f"{path}: expected a 16-color JASC palette")
    colors = [tuple(map(int, line.split())) for line in lines[3:]]
    if any(len(color) != 3 or any(channel < 0 or channel > 255 for channel in color)
           for color in colors):
        raise ValueError(f"{path}: palette channels must be RGB bytes in 0..255")
    if native and any(channel % 8 for color in colors for channel in color):
        raise ValueError(f"{path}: new palette channels must be multiples of 8 in 0..248")
    return colors


def check_image(path, size=None, footprint=False, native=True):
    with Image.open(path) as image:
        image.load()
        if size is not None and image.size != size:
            raise ValueError(f"{path}: expected {size}, got {image.size}")
        if footprint:
            if image.mode not in ("1", "P") or (image.mode == "P" and max(image.getdata()) > 1):
                raise ValueError(f"{path}: footprint must use only 1-bit indices")
            return
        if image.mode != "P":
            raise ValueError(f"{path}: expected indexed PNG, got {image.mode}")
        used = set(image.getdata())
        if not used - {0}:
            raise ValueError(f"{path}: sprite is empty")
        if max(used) > 15:
            raise ValueError(f"{path}: 4bpp sprites must use only indices 0..15")
        if image.info.get("transparency", 0) != 0:
            raise ValueError(f"{path}: transparency must be palette index 0")
        colors = image.getpalette()
        if colors is None or len(colors) < 48:
            raise ValueError(f"{path}: expected at least 16 RGB palette entries")
        colors = [tuple(colors[i:i + 3]) for i in range(0, 48, 3)]
        if native and any(channel % 8 for index in used for channel in colors[index]):
            raise ValueError(f"{path}: new sprite colors must be multiples of 8 in 0..248")
        return colors, used


def check_mon(root, name):
    if not re.fullmatch(r"[A-Za-z0-9_]+", name):
        raise ValueError(f"invalid species folder: {name!r}")
    folder = root / "graphics/pokemon" / name.lower()
    palettes = {filename: palette(folder / filename) for filename in MON_PALETTES}
    images = {
        filename: check_image(folder / filename, size, footprint=filename == "footprint.png",
                              native=filename != "icon.png")
        for filename, size in MON_SIZES.items()
    }
    for filename, size in (("anim_front.png", (64, 64)), ("back.png", (64, 64)),
                            ("icon.png", (32, 32)), ("overworld.png", (32, 32))):
        with Image.open(folder / filename) as image:
            for y in range(0, image.height, size[1]):
                for x in range(0, image.width, size[0]):
                    frame = image.crop((x, y, x + size[0], y + size[1]))
                    if not set(frame.getdata()) - {0}:
                        raise ValueError(f"{folder / filename}: empty frame at ({x}, {y})")
    for filename, palname in (("anim_front.png", "normal.pal"), ("back.png", "normal.pal"),
                              ("overworld.png", "overworld_normal.pal")):
        colors, used = images[filename]
        if any(colors[index] != palettes[palname][index] for index in used):
            raise ValueError(f"{folder / filename}: embedded colors differ from {palname}")
    info = (root / "src/data/pokemon/species_info/aethos_families.h").read_text()
    match = re.search(r"\.iconSprite\s*=\s*gMonIcon_" + re.escape(name)
                      + r",\s*\.iconPalIndex\s*=\s*(\d+)", info, re.IGNORECASE)
    if match is None:
        raise ValueError(f"{name}: missing icon palette index in Aethos species info")
    icon_palette = palette(root / f"graphics/pokemon/icon_palettes/pal{match[1]}.pal", native=False)
    colors, used = images["icon.png"]
    if any(colors[index] != icon_palette[index] for index in used):
        raise ValueError(f"{folder / 'icon.png'}: embedded colors differ from engine icon palette")
    source = root / "design/dex/sprites" / name.lower()
    for filename in (*MON_SIZES, *MON_PALETTES):
        if (source / filename).read_bytes() != (folder / filename).read_bytes():
            raise ValueError(f"{name}/{filename}: design sprite and ROM source differ; regenerate ROM data")
    return motion(folder / "anim_front.png", (64, 64)), motion(folder / "overworld.png", (32, 32))


def motion(path, frame_size):
    with Image.open(path) as image:
        width, height = frame_size
        if image.width % width or image.height % height:
            raise ValueError(f"{path}: frame size {frame_size} does not divide sheet {image.size}")
        frames = [
            image.crop((x, y, x + width, y + height)).tobytes()
            for y in range(0, image.height, height)
            for x in range(0, image.width, width)
        ]
    return [sum(a != b for a, b in zip(frames[i], frames[i + 1]))
            for i in range(0, len(frames) - 1, 2)]


def inventory(root):
    assets = []
    for path in sorted((root / "graphics").rglob("*")):
        if path.is_file() and path.suffix in (".png", ".pal"):
            relative = path.relative_to(root)
            assets.append({
                "path": relative.as_posix(),
                "group": relative.parts[1],
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
    maps = []
    groups = json.loads((root / "data/maps/map_groups.json").read_text())
    for group in groups["group_order"]:
        for name in groups[group]:
            folder = root / "data/maps" / name
            if (folder / "scripts.pory").exists():
                data = json.loads((folder / "map.json").read_text())
                maps.append({
                    "name": name,
                    "type": data["map_type"],
                    "graphics_ids": sorted({event["graphics_id"] for event in data.get("object_events", [])}),
                })
    return {
        "schema_version": 1,
        "groups": dict(sorted(Counter(asset["group"] for asset in assets).items())),
        "assets": assets,
        "maps": maps,
    }


def inventory_changes(before, after):
    snapshots = []
    for snapshot in (before, after):
        if (not isinstance(snapshot, dict) or snapshot.get("schema_version") != 1
                or not isinstance(snapshot.get("assets"), list)):
            raise ValueError("expected a schema_version 1 sprite inventory")
        assets = {}
        for asset in snapshot["assets"]:
            if (not isinstance(asset, dict) or not isinstance(asset.get("path"), str)
                    or not isinstance(asset.get("sha256"), str)
                    or not re.fullmatch(r"[0-9a-f]{64}", asset["sha256"])):
                raise ValueError("inventory assets require a path and SHA-256 digest")
            if asset["path"] in assets:
                raise ValueError(f"duplicate inventory asset: {asset['path']}")
            assets[asset["path"]] = asset["sha256"]
        snapshots.append(assets)
    old, new = snapshots
    common = old.keys() & new.keys()
    return {
        "schema_version": 1,
        "added": sorted(new.keys() - old.keys()),
        "removed": sorted(old.keys() - new.keys()),
        "changed": sorted(path for path in common if old[path] != new[path]),
        "unchanged_count": sum(old[path] == new[path] for path in common),
    }


def provenance(root, reference):
    def git(*args):
        try:
            return subprocess.check_output(
                ["git", "-C", str(root), *args], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as error:
            raise ValueError(error.output.decode(errors="replace").strip()) from error

    commit = git("rev-parse", "--verify", "--end-of-options",
                 f"{reference}^{{commit}}").decode().strip()
    algorithm = git("rev-parse", "--show-object-format").decode().strip()
    originals = {}
    for entry in git("ls-tree", "-r", "-z", commit, "--", "graphics").split(b"\0"):
        if not entry:
            continue
        metadata, path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.decode().split()
        name = path.decode()
        if Path(name).suffix in (".png", ".pal"):
            if kind != "blob" or mode not in ("100644", "100755"):
                raise ValueError(f"{name}: reference source is not a regular file")
            originals[name] = oid
    if not originals:
        raise ValueError(f"{commit}: no graphics PNG/palette reference sources")
    snapshot = inventory(root)
    for asset in snapshot["assets"]:
        path = inside(root, asset["path"])
        if path.is_symlink() or (root / asset["path"]).is_symlink():
            raise ValueError(f"{asset['path']}: source must be a regular file")
        content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != asset["sha256"]:
            raise ValueError(f"{asset['path']}: source changed during inventory")
        # Match the repository's *.pal text filter without modifying checkout bytes.
        if path.suffix == ".pal":
            content = content.replace(b"\r\n", b"\n")
        oid = hashlib.new(algorithm, b"blob " + str(len(content)).encode()
                          + b"\0" + content).hexdigest()
        original = originals.get(asset["path"])
        asset.update({
            "source_git_oid": oid,
            "reference_git_oid": original,
            "relation": ("current_only" if original is None else
                         "reference_identical" if oid == original else "source_different"),
        })
    current = {asset["path"] for asset in snapshot["assets"]}
    snapshot.update({
        "reference_commit": commit,
        "git_object_format": algorithm,
        "palette_comparison": "Git-canonical LF; working SHA-256 remains byte-exact",
        "relations": dict(sorted(Counter(asset["relation"] for asset in snapshot["assets"]).items())),
        "reference_only": sorted(originals.keys() - current),
        "scope": "Source provenance only; not artistic approval, runtime binding or redraw coverage.",
    })
    return snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("inventory")
    listing.add_argument("--output", type=Path)
    changes = commands.add_parser("changes")
    changes.add_argument("--baseline", type=Path, required=True)
    changes.add_argument("--output", type=Path)
    ancestry = commands.add_parser("provenance")
    ancestry.add_argument("--reference", required=True)
    ancestry.add_argument("--output", type=Path)
    checking = commands.add_parser("check")
    checking.add_argument("--pokemon", nargs="+", default=[])
    checking.add_argument("--image", nargs="+", default=[])
    args = parser.parse_args()
    try:
        if args.command in ("inventory", "changes", "provenance"):
            result = (provenance(args.root, args.reference) if args.command == "provenance"
                      else inventory(args.root))
            if args.command == "changes":
                result = inventory_changes(json.loads(args.baseline.read_text()), result)
            content = json.dumps(result, indent=2) + "\n"
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(content)
                print(f"SPRITE {args.command.upper()}: {args.output}")
            else:
                print(content, end="")
        else:
            if not args.pokemon and not args.image:
                parser.error("check requires --pokemon or --image")
            for name in args.pokemon:
                front, follower = check_mon(args.root, name)
                print(f"SPRITE PASS {name}: front changed pixels {front}; follower pairs {follower}")
                if 0 in front + follower:
                    print(f"SPRITE NOTE {name}: identical frame pair; confirm intentional static motion")
            for name in args.image:
                path = inside(args.root, name)
                relative = path.relative_to(args.root.resolve())
                size = (64, 64) if relative.parts[:3] == ("graphics", "trainers", "front_pics") else None
                check_image(path, size=size)
                print(f"SPRITE PASS {name}")
    except (OSError, ValueError) as error:
        print(f"SPRITE FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
