#!/usr/bin/env python3
"""Write the native-scale concept prompts for every species (design/STYLE.md §3.2).

Reads design/dex/species/*.yaml and writes, in dex order, one front prompt and
one back prompt per species to design/dex/CONCEPT_PROMPTS.md, plus a JSON copy
for tools. Each prompt carries the style rules that make the converter
(tools/ichor/art/concept_to_native.py) lossless: a true 64x64 grid at 8x,
at most 15 colors, a flat magenta backdrop and the species' own size.

  python3 tools/dex/concept_prompts.py
"""
import glob
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
OUT_MD = ROOT / "design/dex/CONCEPT_PROMPTS.md"
OUT_JSON = ROOT / "design/dex/concept_prompts.json"

STYLE = (
    "Gen 3 (Game Boy Advance) Pokémon battle sprite. True pixel art on a 64×64 pixel grid, "
    "rendered at 512×512 so every pixel is an exact 8×8 square: no anti-aliasing, no blur, "
    "no gradients, no half-pixels. At most 15 colors. Solid flat magenta background "
    "(#F800F8) everywhere outside the creature: no ground, no shadow, no text, no frame. "
    "1-pixel dark selective outline, light from the top left, hue-shifted cluster shading, "
    "no noise. Expressive face: eyes at least 2×2 pixels with a 1-pixel white shine. "
    "Match the style of the attached Ichor starter reference sheet."
)

SIZE_RE = re.compile(r"(?:fills|fill|about|is)\s+(?:about\s+)?(\d+)\s*[×x]\s*(\d+)\s*px", re.I)
FULL_RE = re.compile(r"fills (?:the whole |the )?64\s*[×x]\s*64 box", re.I)
# Smallest subject per stage, so every sprite keeps enough pixels for detail
# (STYLE.md §3.1). The dex's own size wins when it is larger.
STAGE_MIN = {"basic": 48, "middle": 54, "final": 60, "single": 54}


def clauses(text):
    text = " ".join(text.split())
    parts = re.split(r"(?<=[.;])\s+", text)
    return [p.strip().rstrip(";").strip() for p in parts if p.strip()]


def split_art(art):
    front, back, size = [], [], None
    for c in clauses(art):
        m = SIZE_RE.search(c)
        if m and size is None:
            size = (int(m.group(1)), int(m.group(2)))
        if FULL_RE.search(c) and size is None:
            size = (62, 62)
        low = c.lower()
        if "back sprite" in low or "back pic" in low:
            for piece in re.split(r",?\s+and the follower|\s*;\s*", c):
                if "back" in piece.lower():
                    back.append(piece.strip())
            continue
        if low.startswith("frame 2") or "follower" in low:
            continue
        # drop the bare size note ("Small: it fills about 41×39 px.")
        c = re.sub(r"^[A-Z][A-Za-z -]{0,20}:\s*", "", c)
        if re.match(r"it (?:fills|is about)", c, re.I):
            continue
        front.append(c)
    return " ".join(front), " ".join(back), size


def back_view(text):
    text = re.sub(r"^the back sprite\s+", "", text.strip(), flags=re.I).rstrip(".")
    if not text:
        return "Its signature features stay visible from behind."
    return f"From behind it {text}." if not text[0].isupper() else f"{text}."


def stage_size(size, stage):
    w, h = size or (56, 56)
    need = STAGE_MIN[stage]
    if max(w, h) < need:
        k = need / max(w, h)
        w, h = round(w * k), round(h * k)
    return min(w, 62), min(h, 62)


def size_text(size):
    w, h = size
    return f"The creature fills about {w}×{h} pixels of the 64×64 grid"


def build():
    species = []
    for f in sorted(glob.glob(str(ROOT / "design/dex/species/*.yaml"))):
        line = yaml.safe_load(open(f))["species"]
        for i, s in enumerate(line):
            s["_stage"] = ("single" if len(line) == 1 else "basic" if i == 0
                           else "final" if i == len(line) - 1 else "middle")
            species.append(s)
    species.sort(key=lambda s: s["dex"])
    rows = []
    for s in species:
        front_art, back_art, size = split_art(s["art"])
        size = stage_size(size, s["_stage"])
        types = "/".join(s["types"])
        who = f"{s['name']}, the {s['category']} Pokémon ({types})"
        expr = " ".join(s.get("expression", "").split())
        front = (f"{STYLE} {size_text(size)}, centered, its lowest point 2 pixels above the "
                 f"bottom edge. Three-quarter view facing left. Creature: {who}. {front_art} "
                 f"Personality: {expr}")
        back = (f"{STYLE} Back sprite: the same creature seen from behind and slightly above, "
                f"three-quarter rear view facing up and to the right, as the player's own "
                f"Pokémon in battle. It fills the lower two-thirds of the 64×64 grid and may "
                f"touch the bottom edge. Same colors and outline as its front sprite. "
                f"Creature: {who}. {back_view(back_art)}")
        rows.append({
            "dex": s["dex"], "name": s["name"], "types": types,
            "size": list(size), "stage": s["_stage"], "shiny": s.get("shiny", ""),
            "front_file": f"{s['dex']:03d}_{s['name'].lower()}_front.png",
            "back_file": f"{s['dex']:03d}_{s['name'].lower()}_back.png",
            "front_prompt": front, "back_prompt": back,
        })
    return rows


def write(rows):
    OUT_JSON.write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n")
    lines = [
        "# Concept prompts for the whole Aethos dex",
        "",
        "Generated by `tools/dex/concept_prompts.py` from `design/dex/species/`. "
        "Don't edit by hand; rerun the script after a species changes.",
        "",
        "These prompts make concepts the converter can use without losing detail "
        "(`design/STYLE.md` §3.2).",
        "",
        "1. Attach a reference sheet from `design/art/img/style/` (the starters) to every request, so the style stays consistent.",
        "2. Generate the **front** and the **back** for each species. Pick the best take of each.",
        "3. Save each image as a PNG with the file name given (e.g. `004_kynder_front.png`). Keep it at the 512×512 size it was generated at, without cropping or resizing.",
        "4. Put them all in one folder and hand the folder back. Partial batches by evolution line are fine.",
        "",
        "**Checklist for each image before keeping it:**",
        "- The background is flat magenta all the way round.",
        "- The pixels are hard squares.",
        "- The creature isn't cut off.",
        "- It faces left on the front and away on the back.",
        "- The eyes read clearly.",
        "",
    ]
    for r in rows:
        size = f"{r['size'][0]}×{r['size'][1]} px" if r["size"] else "~56 px"
        lines += [
            f"## #{r['dex']:03d} {r['name']} ({r['types']}, {size})",
            "",
            f"**Front** → `{r['front_file']}`",
            "",
            "```text", r["front_prompt"], "```",
            "",
            f"**Back** → `{r['back_file']}`",
            "",
            "```text", r["back_prompt"], "```",
            "",
            f"*Shiny (for reference, not generated): {' '.join(r['shiny'].split())}*",
            "",
        ]
    OUT_MD.write_text("\n".join(lines))


if __name__ == "__main__":
    rows = build()
    write(rows)
    print(f"{len(rows)} species -> {OUT_MD.relative_to(ROOT)}")
