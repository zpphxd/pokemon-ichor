#!/usr/bin/env python3
"""Write the catalog section of design/phase2/TILES_skiron.md from
build/skiron/catalog.json.

skiron_build.py runs this after a build. Everything between the
`<!-- catalog -->` and `<!-- /catalog -->` markers is regenerated, so the ids
in the document always match the compiled tileset; the rest of the document
(palettes, how to use it, the critique passes) is written by hand.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAT = ROOT / "build/skiron/catalog.json"
DOC = ROOT / "design/phase2/TILES_skiron.md"
START, END = "<!-- catalog -->", "<!-- /catalog -->"


def grid(ids):
    return "\n".join(" ".join(f"0x{v:03X}" for v in r) for r in ids)


def ground_note(s):
    g = s.get("ground") or {}
    kinds = sorted(set(g.values()))
    if not kinds:
        return ""
    if len(g) == s["w"] * s["h"] and len(kinds) == 1:
        return f" Every cell sits on borrowed aethos {kinds[0]}."
    return " Cells on borrowed aethos ground: " + ", ".join(
        f"{k} ({', '.join(c for c, v in g.items() if v == k)})" for k in kinds) + "."


def render(tiles_used=None):
    import skiron_build as B
    data = json.loads(CAT.read_text())
    out = [START, ""]
    if tiles_used is not None:
        out.append(f"**Tile budget.** {tiles_used} of 504 tiles are used (tiles 504-511 belong to "
                   f"the door animations). The build fails past 504.\n")
    for key, (title, blurb) in B.SECTION_TITLES.items():
        items = [s for s in data if s["section"] == key]
        if not items:
            continue
        first = min(s["ids"][0][0] for s in items)
        out.append(f"## {title} (from 0x{first:03X})\n\n{blurb}\n")
        for s in items:
            out.append(f"### {s['title']}\n")
            out.append(f"`{s['key']}`, {s['w']} wide by {s['h']} tall. {s['notes']}{ground_note(s)}\n")
            if key == "ground":
                out.append("| Piece | Id | Walk |\n|---|---|---|")
                for name, (cx, cy) in s["names"].items():
                    out.append(f"| `{name}` | 0x{s['ids'][cy][cx]:03X} | {s['walk'][cy][cx]} |")
                out.append("")
                continue
            out.append("```text")
            g = grid(s["ids"]).split("\n")
            out.append("ids".ljust(len(g[0])) + "   walk")
            for row_ids, row_walk in zip(g, s["walk"]):
                out.append(row_ids + "   " + " ".join(row_walk))
            out.append("```\n")
            beh = {k: v for k, v in s["behaviors"].items() if v not in ("MB_TALL_GRASS",)}
            if beh:
                out.append("Behaviors: " + ", ".join(
                    f"0x{s['ids'][int(k.split(',')[1])][int(k.split(',')[0])]:03X} `{v}`"
                    for k, v in beh.items()) + ".\n")
            if s["names"]:
                named = ", ".join(f"`{n}` 0x{s['ids'][c[1]][c[0]]:03X}" for n, c in s["names"].items())
                out.append(f"Pieces: {named}.\n")
    out.append(END)
    return "\n".join(out)


def main(tiles_used=None):
    block = render(tiles_used)
    text = DOC.read_text() if DOC.exists() else f"# Skiron tileset catalog\n\n{START}\n{END}\n"
    if START not in text:
        text = text.rstrip() + "\n\n" + START + "\n" + END + "\n"
    text = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block, text, flags=re.S)
    DOC.write_text(text)
    print(DOC)


if __name__ == "__main__":
    main()
