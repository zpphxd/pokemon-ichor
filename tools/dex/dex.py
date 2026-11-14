#!/usr/bin/env python3
"""Build the Aethos Pokédex review page from the full species entries.

  python3 tools/dex/dex.py --html OUT.html   write the page (template: tools/dex/dex_page.html)
  python3 tools/dex/dex.py --json OUT.json   write the entries as one JSON file

Run tools/dex/validate.py first; this script assumes the entries are valid.
"""
import argparse
import base64
import io
import json
import pathlib
import sys

import numpy as np
import yaml
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/dex"))
import plan as planlib  # noqa: E402

SPECIES_DIR = ROOT / "design/dex/species"
SPRITE_DIR = ROOT / "design/dex/sprites"
TEMPLATE = ROOT / "tools/dex/dex_page.html"
STATS = ["hp", "atk", "def", "spa", "spd", "spe"]


def _jasc(path):
    rows = [ln.split() for ln in path.read_text().splitlines()[3:19]]
    return [tuple(int(v) for v in r[:3]) for r in rows]


def _uri(idx, colors):
    """An indexed array and its palette as a transparent PNG data URI."""
    rgba = np.zeros(idx.shape + (4,), np.uint8)
    for i, c in enumerate(colors):
        if i:
            rgba[idx == i] = (*c, 255)
    buf = io.BytesIO()
    Image.fromarray(rgba, "RGBA").save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def sprite_data(name):
    """Every finished sprite of a species, as data URIs, or None."""
    d = SPRITE_DIR / name.lower()
    if not (d / "anim_front.png").exists():
        return None
    normal, shiny = _jasc(d / "normal.pal"), _jasc(d / "shiny.pal")
    front = np.array(Image.open(d / "anim_front.png"))
    back = np.array(Image.open(d / "back.png"))
    ow = np.array(Image.open(d / "overworld.png"))
    icon_im = Image.open(d / "icon.png")
    flat = icon_im.getpalette()[:48]
    icon_pal = [tuple(flat[i:i + 3]) for i in range(0, 48, 3)]
    icon = np.array(icon_im)
    foot = np.array(Image.open(d / "footprint.png"))
    out = {}
    for key, pal in (("normal", normal), ("shiny", shiny)):
        out[key] = {
            "front": [_uri(front[:64], pal), _uri(front[64:], pal)],
            "back": _uri(back, pal),
            "follow": [_uri(ow[:, i * 32:(i + 1) * 32], pal) for i in range(6)],
        }
    out["icon"] = [_uri(icon[:32], icon_pal), _uri(icon[32:], icon_pal)]
    out["foot"] = _uri(foot, [(0, 0, 0), (98, 98, 98)])
    return out


def collect():
    data = planlib.load()
    plan_species, errors = planlib.build(data)
    if errors:
        sys.exit("plan.yaml has errors; run tools/dex/plan.py")
    lines = {l["id"]: l for l in data["lines"]}
    written = {}
    for path in sorted(SPECIES_DIR.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text())
        for sp in doc.get("species") or []:
            written[sp["dex"]] = sp

    out = []
    for p in plan_species:
        line = lines[p["line"]]
        sp = written.get(p["dex"])
        members = [s for s in plan_species if s["line"] == p["line"]]
        chain = []
        for m in members:
            w = written.get(m["dex"])
            chain.append({
                "dex": m["dex"],
                "name": (w or {}).get("name") or m["concept"],
                "evos": [{"to": members[e.get("to", m["index"] + 1)]["dex"], "how": planlib.describe(e)} for e in m["evos"]],
            })
        entry = {
            "dex": p["dex"],
            "line": p["line"],
            "section": line["section"],
            "roles": line["roles"],
            "group": bool(line.get("group")),
            "concept": p["concept"],
            "types": p["types"],
            "baby": p["baby"],
            "chain": chain,
            "written": bool(sp),
        }
        if sp:
            bs = sp["base_stats"]
            entry.update({k: sp.get(k) for k in (
                "name", "etymology", "category", "abilities", "hidden_ability", "ev_yield", "exp_yield",
                "catch_rate", "gender", "egg_groups", "egg_cycles", "growth_rate", "height_m", "weight_kg",
                "myth", "expression", "art", "shiny", "dex_entry", "habitat", "learnset", "signature", "new_move")})
            entry["base_stats"] = [bs[k] for k in STATS]
            entry["bst"] = sum(entry["base_stats"])
            entry["base_friendship"] = sp.get("base_friendship", 50)
            entry["sprite"] = sprite_data(sp["name"])
        out.append(entry)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--html", type=pathlib.Path)
    ap.add_argument("--json", type=pathlib.Path)
    ap.add_argument("--summary", action="store_true", help="print one review line per species")
    args = ap.parse_args()
    entries = collect()
    if args.summary:
        for e in entries:
            if not e["written"]:
                print(f"{e['dex']:03d} -- {e['concept']} (not written)")
                continue
            bs = "/".join(str(v) for v in e["base_stats"])
            abil = "/".join(e["abilities"]) + (f" [{e['hidden_ability']}]" if e["hidden_ability"] else "")
            print(f"{e['dex']:03d} {e['name']:<12} {'/'.join(e['types']):<17} {e['bst']:>3} {bs:<23} "
                  f"{e['category']:<12} {abil}")
    payload = {"species": entries, "types": planlib.TYPES}
    if args.json:
        args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=1))
    if args.html:
        args.html.write_text(TEMPLATE.read_text().replace("/*DEX_DATA*/null", json.dumps(payload, ensure_ascii=False)))
    written = sum(e["written"] for e in entries)
    drawn = sum(bool(e.get("sprite")) for e in entries)
    print(f"{written} of {len(entries)} entries written, {drawn} drawn", *(p for p in (args.html, args.json) if p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
