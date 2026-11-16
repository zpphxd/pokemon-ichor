#!/usr/bin/env bash
# Complete TEST-ONLY native/ROM/OBJ gallery. Story scenes stay separate.
set -eu
cd "$(dirname "$0")/../../.."
ROM="${1:-pokeemerald.gba}"
. tools/ichor/tests/engine_build.sh
OUT=build/test_human_classes
engine_prepare HUMANS "$OUT" tools/ichor/tests/human_classes_consts.c tools/ichor/tests/human_classes_setup.s
python3 - "$OUT" "${HUMAN_NATIVE_SOURCE:-}" "$ROM" <<'PY'
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, "tools/ichor/art")
import human_classes as humans

out, reference, rom = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
(out / "native").mkdir(exist_ok=True)
hashes = {}
for entry in humans.ASSETS:
    source = (Path(reference) / entry["source"]) if reference else humans.ROOT / entry["target"]
    stem = out / "native" / (entry["kind"] + "_" + entry["name"])
    width, height = (2, 4) if entry["kind"] == "walkers" else (8, 8)
    subprocess.run(["tools/gbagfx/gbagfx", str(source), str(stem) + ".4bpp",
                    "-mwidth", str(width), "-mheight", str(height)], check=True)
    subprocess.run(["tools/gbagfx/gbagfx", str(source), str(stem) + ".gbapal"], check=True)
    hashes[entry["target"]] = hashlib.sha256(source.read_bytes()).hexdigest()
(out / "evidence.json").write_text(json.dumps({
    "kind": "TEST-ONLY fixture; not story footage", "native_sources": hashes,
    "rom_sha256": hashlib.sha256(rom.read_bytes()).hexdigest(),
    "elf_sha256": hashlib.sha256(rom.with_suffix(".elf").read_bytes()).hexdigest(),
    "map_sha256": hashlib.sha256(rom.with_suffix(".map").read_bytes()).hexdigest(),
}, indent=2) + "\n")
PY
engine_run HUMANS "$OUT" tools/ichor/tests/human_classes.lua 200000 900
python3 tools/ichor/tests/human_classes_render.py "$OUT" "${HUMAN_NATIVE_SOURCE:-}"
