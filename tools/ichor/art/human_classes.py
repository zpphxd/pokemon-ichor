#!/usr/bin/env python3
"""Reproduce the 32 image-model-led human class assets from authored native PNGs.

The indexed exports are the canonical inputs, not the legacy shape painters.
Their larger model sources and conversion/continuity evidence live in the
matching review archive. This producer only validates and copies native art.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
SOURCES = Path(__file__).resolve().parent / "sources/human_classes"
MANIFEST = json.loads((SOURCES / "manifest.json").read_text())
ASSETS = MANIFEST["assets"]
BY_KEY = {(entry["kind"], entry["name"]): entry for entry in ASSETS}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_image(kind, name):
    with Image.open(SOURCES / BY_KEY[kind, name]["source"]) as image:
        return image.copy()


def validate():
    if len(ASSETS) != 32 or len(BY_KEY) != 32:
        raise ValueError("human class source union must contain exactly 32 distinct assets")
    for relative, expected in MANIFEST["shared_palettes"].items():
        if digest(ROOT / relative) != expected:
            raise ValueError(f"{relative}: shared palette changed; coordinated review required")
    for entry in ASSETS:
        kind, name = entry["kind"], entry["name"]
        prefix = {"walkers": "graphics/object_events/pics/people/ichor",
                  "portraits": "graphics/trainers/front_pics"}[kind]
        if entry["target"] != f"{prefix}/{name}.png" or entry["source"] != f"{kind}/{name}.png":
            raise ValueError(f"{name}: unexpected source or production path")
        path = SOURCES / entry["source"]
        if digest(path) != entry["sha256"]:
            raise ValueError(f"{path}: authored source hash differs from manifest")
        with source_image(kind, name) as image:
            frames = (10 if name == "healer" else 9) if kind == "walkers" else 1
            expected_size = (frames * 16, 32) if kind == "walkers" else (64, 64)
            if (image.mode != "P" or image.size != expected_size
                    or image.info.get("transparency") != 0 or path.read_bytes()[24] != 4
                    or len(image.getpalette()) != 48 or max(image.getdata()) > 15):
                raise ValueError(f"{name}: invalid native dimensions, palette or 4bpp PNG")
            if kind == "walkers":
                palette = [int(value) for line in (ROOT / entry["palette"]).read_text().splitlines()[3:]
                           for value in line.split()]
                if image.getpalette() != palette:
                    raise ValueError(f"{name}: PNG palette does not match the engine-loaded shared palette")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="copy only the 32 authored native exports")
    mode.add_argument("--check", action="store_true", help="verify sources and production reproduction")
    mode.add_argument("--list", action="store_true", help="print the exact legacy-write protected paths")
    args = parser.parse_args()
    validate()
    if args.list:
        print("\n".join(entry["target"] for entry in ASSETS))
        return
    for entry in ASSETS:
        source, target = SOURCES / entry["source"], ROOT / entry["target"]
        if args.write:
            shutil.copyfile(source, target)
        if digest(target) != entry["sha256"]:
            raise ValueError(f"{target}: differs from authored source; run human_classes.py --write")
    print("PASS: 32 authored human assets reproduce; shared palettes unchanged")


if __name__ == "__main__":
    main()
