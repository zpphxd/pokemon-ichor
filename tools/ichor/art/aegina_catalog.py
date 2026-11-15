#!/usr/bin/env python3
"""Rewrite the generated part of design/phase2/TILES_aegina.md from
build/aegina/catalog.json.

aegina_build.py runs this after a build. Only the text between the
"catalog:start" and "catalog:end" markers is replaced; the rest of the file (the
palette plan, the detour notes, the render-and-critique log) is written by hand
and kept.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/aegina/catalog.json"
DOC = ROOT / "design/phase2/TILES_aegina.md"
START, END = "<!-- catalog:start -->", "<!-- catalog:end -->"

# (title, blurb, keys) in catalog order
SECTIONS = [
    ("The harbor", "Akti's harbor pieces, copied pixel for pixel, and the round harbor: "
     "four rounded basin corners and the two mole heads with their beacons.",
     ["quay", "quay_gangplank", "quay_edges", "trireme", "boat_kaiki", "boat_kaiki_left",
      "bollard_line", "rope_coil", "amphora_stack", "sea_rocks", "boat_beached",
      "basin_nw", "basin_ne", "basin_sw", "basin_se", "mole_head_w", "mole_head_e"]),
    ("The town", "The three doors (the inn, the mint, Aiakides's house), the north gate "
     "and its shut leaves, and the turtle mosaic.",
     ["inn", "mint", "house_aiakides", "gate", "gate_shut", "turtle_mosaic"]),
    ("Dry ground and ants", "The dry grass, its golden tall grass, and the ant hills.",
     ["dry_grass", "dry_tall_grass", "anthills"]),
    ("Landmarks and growth", "Kolona and its fallen temple, the island's trees and scrub, "
     "and the detour's two monuments.",
     ["kolona", "kolona_ruins", "pistachio", "pine", "scrub", "temple_aphaia", "altar_zeus"]),
]


def grid(ids, skip):
    return [" ".join("  -  " if f"{x},{y}" in skip else f"0x{v:03X}" for x, v in enumerate(r))
            for y, r in enumerate(ids)]


def section(tiles_used, counts, detour_tiles, detour_only):
    data = {s["key"]: s for s in json.loads(CAT.read_text())}
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from aegina_art import DETOUR, DETOUR_SHARED
    out = [START, "",
           f"**Tile count.** {tiles_used} of 504 tiles are used. The pieces drawn for the "
           f"detour ({', '.join(f'`{k}`' for k in DETOUR)}) use {detour_tiles} of them. The "
           f"town plants the {', '.join(f'`{k}`' for k in DETOUR_SHARED)} too, so "
           f"{detour_only} tiles belong to the detour alone.", "",
           "| Structure | Size | Tiles it draws | New tiles |", "|---|---|---|---|"]
    for key, n, new in counts:
        s = data[key]
        mark = " (detour)" if key in DETOUR else ""
        out.append(f"| `{key}`{mark} | {s['w']}×{s['h']} | {n} | {new} |")
    out.append("")
    out.append("New tiles are counted before Porytiles merges flips and the build merges "
               "near-duplicates, so they add up to a little more than the total.")
    out.append("")
    listed = set()
    for title, blurb, keys in SECTIONS:
        out.append(f"## {title}\n\n{blurb}\n")
        for k in keys:
            s = data.get(k)
            if not s:
                continue
            listed.add(k)
            out.append(f"### {s['title']}\n")
            tag = " **Detour piece.**" if k in DETOUR else ""
            out.append(f"`{s['key']}`, {s['w']} wide by {s['h']} tall.{tag} {s['notes']}\n")
            rows = grid(s["ids"], set(s.get("skip", [])))
            out.append("```text")
            out.append("ids".ljust(len(rows[0])) + "   walk")
            for r, w in zip(rows, s["walk"]):
                out.append(r + "   " + " ".join(w))
            out.append("```\n")
            ground = s.get("ground", {})
            if ground:
                kinds = sorted(set(ground.values()))
                if len(ground) == s["w"] * s["h"] and len(kinds) == 1:
                    out.append(f"Ground: all on aethos {kinds[0]}.\n")
                else:
                    parts = []
                    for kind in kinds:
                        cells = sorted(c for c, g in ground.items() if g == kind)
                        parts.append(f"{kind} at " + ", ".join(f"({c})" for c in cells))
                    out.append("Ground: " + "; ".join(parts) + ".\n")
            doors = [f"0x{s['ids'][int(c.split(',')[1])][int(c.split(',')[0])]:03X}"
                     for c, mb in s["behaviors"].items() if mb == "MB_NON_ANIMATED_DOOR"]
            if doors:
                out.append(f"Door metatile: {', '.join(doors)}.\n")
    missing = set(data) - listed
    assert not missing, f"aegina_catalog: no section lists {sorted(missing)}"
    out.append(END)
    return "\n".join(out)


def main(tiles_used, counts, detour_tiles, detour_only):
    text = DOC.read_text() if DOC.exists() else f"# Aegina tileset catalog\n\n{START}\n{END}\n"
    if START not in text:
        text = text.rstrip() + f"\n\n{START}\n{END}\n"
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    DOC.write_text(head + section(tiles_used, counts, detour_tiles, detour_only) + tail)
    print(DOC)
