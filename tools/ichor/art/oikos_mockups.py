#!/usr/bin/env python3
"""Render the slice's interiors on oikos for the look review.

Two kinds of image go to design/phase1/img/:
  oikos_slice_<layout>.png   the real Hoenn layouts with --primary oikos: how
                             far the primary alone takes them (their
                             secondaries are still Hoenn)
  oikos_mock_<room>.png      the same rooms rebuilt from oikos kit metatiles
                             only, to show what Greek interiors will look like
                             once the layouts use the kit
  oikos_sheet.png            the numbered metatile sheet

The mock rooms are throwaway block data (not maps); the map batch builds the
real layouts. Usage: /usr/bin/python3 tools/ichor/art/oikos_mockups.py
"""
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
IMG = ROOT / "design/phase1/img"
TMP = ROOT / "build/oikos_mock"
RENDER = ROOT / "tools/ichor/render_map.py"
PY = sys.executable

SLICE = [
    "LAYOUT_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F",
    "LAYOUT_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F",
    "LAYOUT_LITTLEROOT_TOWN_MAYS_HOUSE_1F",
    "LAYOUT_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB",
    "LAYOUT_POKEMON_CENTER_1F",
    "LAYOUT_MART",
    "LAYOUT_HOUSE1",
]

# Two-letter codes for kit metatiles (see design/phase1/TILES_oikos.md).
CODES = {
    "..": 0x000, "TV": 0x002, "PC": 0x004, "x1": 0x006, "x2": 0x007,
    "F_": 0x008, "Fw": 0x009, "Fs": 0x00A, "M_": 0x00B, "Mi": 0x00C, "Ms": 0x00D,
    "Mm": 0x00E, "Ru": 0x00F,
    "Wb": 0x010, "Wu": 0x011, "Wf": 0x012, "Wn": 0x013, "Ws": 0x014, "Wo": 0x015,
    "Dt": 0x016, "Ut": 0x017,
    "Wl": 0x018, "Wd": 0x019, "Pu": 0x01A, "Pl": 0x01B, "Th": 0x01C, "Sd": 0x01D,
    "Db": 0x01E, "Ub": 0x01F,
    "K1": 0x020, "K2": 0x021, "K3": 0x028, "K4": 0x029,
    "S1": 0x022, "S2": 0x023, "S3": 0x02A, "S4": 0x02B,
    "R1": 0x024, "R2": 0x025, "R3": 0x02C, "R4": 0x02D,
    "O1": 0x026, "O2": 0x02E, "L1": 0x027, "L2": 0x02F,
    "H1": 0x030, "H2": 0x031, "H3": 0x038, "H4": 0x039,
    "C1": 0x032, "C2": 0x03A, "C3": 0x042,
    "A1": 0x033, "A2": 0x03B, "P1": 0x034, "P2": 0x03C, "Y1": 0x035, "Y2": 0x03D,
    "Kf": 0x036, "Kr": 0x037, "Kl": 0x03E, "Tb": 0x03F,
    "Sx": 0x040, "Ch": 0x041, "Am": 0x043, "Kt": 0x044, "Bz": 0x045, "Kc": 0x046,
    "Kn": 0x047, "c1": 0x048, "c2": 0x049, "c3": 0x04A, "m1": 0x04B, "m2": 0x04C,
    "s1": 0x04D, "s2": 0x04E, "Hb": 0x04F, "t1": 0x050, "t2": 0x051,
}

ROOMS = {
    # Beat 1B: Mom at the family hearth; her loom, honey jars, the stairs up.
    "players_house_1f": """
        Wb Ws Wb R1 R2 Wb Wn Wb Y1 Ut Wb
        Wl Wl Wl R3 R4 Wl Wl Wl Y2 Ub Wl
        Fs O1 Fs Fs Fs Fs Fs Fs Fs F_ Fs
        F_ O2 F_ F_ F_ F_ F_ F_ F_ F_ F_
        F_ F_ F_ F_ H1 H2 F_ F_ F_ F_ Am
        F_ F_ F_ F_ H3 H4 F_ F_ Ru Ru F_
        F_ Kr Tb Kl F_ F_ F_ F_ Ru Ru F_
        F_ F_ Fw F_ F_ F_ F_ F_ F_ F_ Hb
        F_ F_ F_ F_ F_ F_ F_ F_ x1 x2 F_
    """,
    # Beat 1A: the player's room: kline, klepsydra, kibotos, knucklebones.
    "players_room_2f": """
        Wb Ws Wb Kc S1 S2 Wb Wo Wb
        Wl Wl Wl Wl S3 S4 Wl Wl Wl
        Fs Fs Fs Fs Fs Fs Fs Fs Sd
        K1 K2 F_ F_ F_ F_ F_ F_ F_
        K3 K4 F_ Kn F_ F_ Ru Ru F_
        F_ F_ F_ F_ F_ F_ Ru Ru F_
        Ch F_ F_ F_ F_ F_ F_ F_ Hb
        F_ F_ F_ Fw F_ F_ F_ F_ F_
    """,
    # Beat 3: Daphne's hall: scroll shelves, the map of Aethos, three kraters.
    "akademia": """
        Wb Wb S1 S2 Wb m1 m2 Wb S1 S2 Wb Wo Wb
        Wl Wl S3 S4 Wl Wl Wl Wl S3 S4 Wl Wl Wl
        Ms Ms Ms Ms Ms Ms Ms Ms Ms Ms Ms Ms Ms
        M_ C1 M_ M_ M_ M_ M_ M_ M_ M_ M_ C1 M_
        M_ C2 M_ M_ Kt Kt Kt M_ M_ A1 M_ C2 M_
        M_ C3 M_ M_ M_ M_ M_ M_ M_ A2 M_ C3 M_
        M_ M_ M_ M_ M_ M_ M_ M_ M_ M_ M_ M_ M_
        M_ M_ t1+ t2+ M_ M_ Mi M_ M_ t1+ t2+ M_ M_
        M_ M_ Kf+ Kf+ M_ M_ M_ M_ M_ Kf+ Kf+ M_ M_
        Mm Mm Mm Mm Mm Mm Mm Mm Mm Mm Mm Mm Mm
        M_ M_ M_ M_ M_ M_ x1 x2 M_ M_ M_ M_ M_
    """,
    # Akti Asclepeion: the healer's counter, the sacred spring, the Pithos.
    "asclepeion": """
        Wb Wf Wf Wb Wb Wn Wb Wn Wb P1 Wb Wf Wf Wb
        Wl Wl Wl Wl Wl Wl Wl Wl Wl P2 Wl Wl Wl Wl
        Ms Ms Ms Ms Ms Ms Ms Ms Ms Ms Ms Ms Ms Ms
        M_ O1+ M_ M_ c1+ c2+ c3+ M_ s1 s2 M_ M_ A1 M_
        M_ O2+ M_ M_ M_ M_ M_ M_ M_ M_ M_ M_ A2 M_
        Mm Mm Mm Mm Mm Mm Mm Mm Mm Mm Mm Mm Mm Mm
        M_ Bz M_ M_ M_ M_ Mi M_ M_ M_ M_ M_ Bz M_
        M_ Kf+ Kf+ M_ M_ M_ M_ M_ M_ M_ M_ Kf+ Kf+ M_
        M_ M_ M_ M_ M_ M_ x1 x2 M_ M_ M_ M_ M_ M_
    """,
    # Akti Agora: Demeas's stall among wine racks and jars.
    "agora": """
        Wb R1 R2 Wb Ws Wb R1 R2 Wb S1 S2
        Wl R3 R4 Wl Wl Wl R3 R4 Wl S3 S4
        Fs Fs Fs Fs Fs Fs Fs Fs Fs Fs Fs
        F_ F_ c1 c2 c3 F_ F_ Am Am Am F_
        F_ F_ F_ F_ F_ F_ F_ F_ F_ F_ F_
        L1 F_ F_ F_ Fw F_ F_ F_ F_ F_ L1
        L2 F_ Ru Ru F_ F_ F_ Ch Ch F_ L2
        F_ F_ F_ F_ x1 x2 F_ F_ F_ F_ F_
    """,
}


def run(*args):
    subprocess.run([PY, str(RENDER), *map(str, args)], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL)


def main():
    IMG.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    run("--sheet", "oikos", "--scale", 3, "-o", IMG / "oikos_sheet.png")
    for lay in SLICE:
        name = lay.lower().removeprefix("layout_littleroot_town_").removeprefix("layout_")
        run(lay, "--primary", "oikos", "--scale", 3, "-o", IMG / f"oikos_slice_{name}.png")
    for name, text in ROOMS.items():
        rows = [r.split() for r in text.strip().splitlines()]
        width = len(rows[0])
        assert all(len(r) == width for r in rows), name
        # A trailing "+" picks the piece on the other floor (id + 0x40).
        blocks = np.array([CODES[c.rstrip("+")] + (0x40 if c.endswith("+") else 0)
                           for r in rows for c in r], "<u2")
        path = TMP / f"{name}.bin"
        blocks.tofile(path)
        run("--blockdata", path, "--width", width, "--primary", "oikos",
            "--secondary", "gTileset_GenericBuilding", "--scale", 3,
            "-o", IMG / f"oikos_mock_{name}.png")
    print("wrote", IMG)


if __name__ == "__main__":
    main()
