"""Read-only integrity gate for image-led Theo/Ianthe canonical PNG sources.

    python3 tools/ichor/art/player_sources.py --check

The production PNGs are the sole native build inputs. Source reconstruction is
separate: the frozen generated-image/crop/export bundle rebuilds these assets
offline without a live image model. This module never writes art or palettes.
"""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ART = Path(__file__).resolve().parent
ROOT = ART.parents[2]
MANIFEST = ART / "player_sources.json"
FOLDERS = {"theo": "brendan", "ianthe": "may"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest():
    data = json.loads(MANIFEST.read_text())
    if data["schema"] != 2:
        raise ValueError("Unsupported authored-player manifest")
    for path in [*data["assets"], *data["read_only_shared_palettes"]]:
        if Path(path).is_absolute() or ".." in Path(path).parts:
            raise ValueError(f"Invalid repository-relative player asset: {path}")
    return data


def read_palette(path):
    lines = path.read_text().splitlines()
    if lines[:3] != ["JASC-PAL", "0100", "16"] or len(lines) != 19:
        raise ValueError(f"Invalid sixteen-color JASC palette: {path}")
    rows = [tuple(map(int, row.split())) for row in lines[3:]]
    if any(len(row) != 3 or any(v < 0 or v > 255 for v in row) for row in rows):
        raise ValueError(f"Invalid palette RGB channels: {path}")
    return rows


def asset(who, state):
    rows = [(path, row) for path, row in manifest()["assets"].items()
            if row["identity"] == who and row.get("state") == state]
    if len(rows) != 1:
        raise ValueError(f"Expected exactly one player source for {who}/{state}")
    return rows[0]


def source_image(who, state):
    name, row = asset(who, state)
    path = ROOT / name
    if digest(path) != row["sha256"]:
        raise ValueError(f"Canonical player source differs from pinned manifest: {path}")
    with Image.open(path) as image:
        return image.copy()


def reject_legacy_write(path, root=ROOT):
    root = Path(root).resolve()
    target = Path(path).resolve()
    data = manifest()
    protected = {root / p for p in [*data["assets"], *data["read_only_shared_palettes"]]}
    if target in protected:
        raise ValueError(
            f"{target.relative_to(root)} is a canonical player source or "
            "read-only shared palette. Legacy repainting is retired; reproduce it with "
            "the frozen image-source replay bundle, and verify with "
            "`python3 tools/ichor/art/player_sources.py --check`.")


def check(root=ROOT):
    root = Path(root).resolve()
    data = manifest()
    pngs = frames = palettes = 0
    for name, row in data["assets"].items():
        source = root / name
        if digest(source) != row["sha256"]:
            raise ValueError(f"Canonical player source differs from pinned manifest: {source}")
        if source.suffix == ".pal":
            colors = read_palette(source)
            if any(channel & 7 for color in colors for channel in color):
                raise ValueError(f"Trainer palette is not hardware precise: {source}")
            palettes += 1
            continue
        with Image.open(source) as image:
            image.load()
            if (image.mode != "P" or list(image.size) != row["size"]
                    or source.read_bytes()[24] != 4
                    or image.info.get("transparency") != 0
                    or max(image.tobytes()) > 15):
                raise ValueError(f"Invalid native indexed player source: {source}")
            if hashlib.sha256(image.tobytes()).hexdigest() != row["indices_sha256"]:
                raise ValueError(f"Reviewed player pixel indices differ: {source}")
            width, height = row["frame_size"]
            if (image.width % width or image.height % height
                    or image.width // width * (image.height // height) != row["source_frames"]):
                raise ValueError(f"Invalid player source-frame layout: {source}")
            role = row["palette_role"]
            colors = [tuple(image.getpalette()[i:i + 3]) for i in range(0, 48, 3)]
            if role.startswith("trainer-local-"):
                folder = FOLDERS[row["identity"]]
                expected = read_palette(root / f"graphics/trainers/palettes/{folder}.pal")
            else:
                shared = read_palette(root / f"graphics/object_events/palettes/{role}.pal")
                expected = [tuple(c & 248 for c in color) for color in shared]
            if colors != expected:
                raise ValueError(f"Player hardware palette binding differs: {source}")
            pngs += 1
            frames += row["source_frames"]
    for name, expected in data["read_only_shared_palettes"].items():
        if digest(root / name) != expected:
            raise ValueError(f"Read-only shared player palette changed: {name}")
    if (pngs, frames, palettes) != (24, 186, 2):
        raise ValueError(f"Incomplete player source coverage: {(pngs, frames, palettes)}")
    return {"pngs": pngs, "source_frames": frames, "trainer_palettes": palettes,
            "read_only_shared_palettes": 3}


def check_replay(directory):
    directory = Path(directory)
    for name, row in manifest()["assets"].items():
        folder = FOLDERS[row["identity"]]
        filename = row["state"] + ".png" if name.endswith(".png") else "battle.pal"
        reconstructed = directory / folder / filename
        if digest(reconstructed) != row["sha256"]:
            raise ValueError(f"Portable image-source reconstruction differs: {reconstructed}")


def check_compiled_arrays(rom, symbols, expected):
    for name, data in expected.items():
        if name not in symbols:
            raise ValueError(f"Required player ROM symbol missing: {name}")
        address, size, kind = symbols[name]
        if size != len(data) or kind.upper() != "R":
            raise ValueError(f"Player ROM symbol size/type differs: {name}")
        offset = address - 0x08000000
        if offset < 0 or offset + size > len(rom):
            raise ValueError(f"Player symbol outside selected ROM: {name}")
        if rom[offset:offset + size] != data:
            raise ValueError(f"Player ROM bytes differ from canonical source: {name}")


def check_rom(rom, elf):
    import check_legacy_players as legacy

    check()
    expected = {}
    suffixes = {
        "field_move": "FieldMove", "fishing": "Fishing", "surfing": "Surfing",
        "underwater": "Underwater", "mach_bike": "MachBike", "acro_bike": "AcroBike",
        "watering": "Watering", "decorating": "Decorating",
    }

    def tiles(who, state):
        image = source_image(who, state)
        _, row = asset(who, state)
        return legacy.native_tiles(image.tobytes(), *image.size, row["frame_size"][0])

    with tempfile.TemporaryDirectory() as directory:
        for who, folder in FOLDERS.items():
            name = "Brendan" if who == "theo" else "May"
            prefix = "gObjectEventPic_" + name
            expected[prefix + "NormalRunning"] = tiles(who, "walking") + tiles(who, "running")
            for state, suffix in suffixes.items():
                expected[prefix + suffix] = tiles(who, state)
            expected["gTrainerBackPic_" + name] = tiles(who, "battle_back")
            raw = Path(directory) / (folder + ".4bpp")
            compressed = Path(directory) / (folder + ".smol")
            raw.write_bytes(tiles(who, "battle_front"))
            subprocess.run([str(ROOT / "tools/compresSmol/compresSmol"), "-w",
                            str(raw), str(compressed)], check=True, capture_output=True)
            expected["gTrainerFrontPic_" + name] = compressed.read_bytes()
            expected["gTrainerPalette_" + name] = legacy.palette_bytes(
                ROOT / f"graphics/trainers/palettes/{folder}.pal")
            expected["gObjectEventPal_" + name] = legacy.palette_bytes(
                ROOT / f"graphics/object_events/palettes/{folder}.pal")
        expected["gObjectEventPal_PlayerUnderwater"] = legacy.palette_bytes(
            ROOT / "graphics/object_events/palettes/player_underwater.pal")
    if len(expected) != 27:
        raise ValueError("Incomplete player compiled-array coverage")
    check_compiled_arrays(Path(rom).read_bytes(), legacy.resolve_symbols(Path(elf)), expected)
    return len(expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--rom", type=Path)
    parser.add_argument("--elf", type=Path, help="Defaults to the selected ROM's adjacent ELF")
    parser.add_argument("--replay-dir", type=Path, help="Independently reconstructed native/ directory")
    parser.add_argument("--source-bundle", type=Path, help="Verify the frozen source archive hash")
    args = parser.parse_args()
    if args.elf and not args.rom:
        parser.error("--elf requires --rom")
    try:
        result = check()
        if args.replay_dir:
            check_replay(args.replay_dir)
        if args.source_bundle:
            if digest(args.source_bundle) != manifest()["reproduction_bundle"]["sha256"]:
                raise ValueError("Frozen image-source bundle hash differs")
        if args.rom:
            arrays = check_rom(args.rom, args.elf or args.rom.with_suffix(".elf"))
            print(f"PASS: {arrays} ELF-resolved ROM image/palette arrays match all24 canonical PNGs")
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"PLAYER_SOURCE FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {result['pngs']} canonical player PNGs/"
          f"{result['source_frames']} source frames, two local trainer palettes; "
          "three shared palettes unchanged; integrity/format only, not artistic approval")
    return 0


if __name__ == "__main__":
    sys.exit(main())
