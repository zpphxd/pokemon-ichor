#!/usr/bin/env python3
"""Checks and review renders for Route 33 (tools/ichor/maps/westsea.py).

check() reads the layout and map.json as written and proves:
  - every object, warp and sign sits where it can be used, and every bg event
    can be read from water or ground next to it;
  - the sea as the player sails it (surfing, currents carrying you, landing on
    walkable ground) under each state of the gates: no relics; Triton's Conch;
    the bronze ram; both. The Ithaka and Kerkyra landings, the north basin and
    the lagoon need the Conch; the cove and the current's run through the reef
    need the ram; the way through the fog stays shut in every state;
  - the mandatory divers' lines close their crossings (Pontia and Aktaios the
    reef fence, Nerites the Echinades' gap);
  - the hut's door warps into the hut, and its mat back out.

render(dir) writes route33.png (2x), route33_walk.png (collision red, water
blue, currents marked, events drawn) and screen-sized crops (15x10) along the
sailing lines, tiled into route33_screens.png.
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import deque
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import westsea as WS  # noqa: E402

ROOT = WS.ROOT
W, H = WS.W, WS.H


def load():
    blocks = np.fromfile(ROOT / "data/layouts" / WS.NAME / "map.bin", "<u2").reshape(H, W)
    ev = json.loads((ROOT / "data/maps" / WS.NAME / "map.json").read_text())
    return blocks, ev


def beh(blocks, x, y):
    return WS.behavior(int(blocks[y, x]) & 0x3FF)


def solid(blocks, x, y):
    return bool(blocks[y, x] >> 10 & 3)


def elev(blocks, x, y):
    return int(blocks[y, x]) >> 12


def is_water(blocks, x, y):
    return beh(blocks, x, y) in WS.SURF_BEHAVIORS and elev(blocks, x, y) == 1


# Which object cells block, by state: (conch, ram)
def blockers(ev, conch, ram):
    out = set()
    for o in ev["object_events"]:
        f = o["flag"]
        if f in ("FLAG_ICHOR_R33_WHIRLPOOL_ECHINADES", "FLAG_ICHOR_R33_WHIRLPOOL_LAGOON") and conch:
            continue
        if f in ("FLAG_ICHOR_R33_ROCKS_COVE", "FLAG_ICHOR_R33_ROCKS_CHANNEL") and ram:
            continue
        if o["graphics_id"] == "OBJ_EVENT_GFX_ITEM_BALL" and o["script"] == "Common_EventScript_FindItem":
            continue                                    # items get picked up; they don't wall anything
        if f == "FLAG_ICHOR_R33_KYMON_HOME":
            pass
        out.add((o["x"], o["y"]))
    return out


def sail(blocks, ev, start, conch, ram, avoid=frozenset()):
    """Every cell the player can reach from `start`: surfing, walking on land,
    stepping between them, carried by currents (which only let you go their way
    unless the next cell is blocked)."""
    stop = blockers(ev, conch, ram)

    def passable(x, y):
        return (0 <= x < W and 0 <= y < H and not solid(blocks, x, y) and (x, y) not in stop
                and (x, y) not in avoid)

    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        b = beh(blocks, x, y)
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if b in WS.CURRENTS:
            dx, dy = WS.CURRENTS[b]
            if passable(x + dx, y + dy):
                moves = [(dx, dy)]
        for dx, dy in moves:
            n = (x + dx, y + dy)
            if n not in seen and passable(*n):
                seen.add(n)
                q.append(n)
    return seen


def fronts(x, y):
    return [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]


def check():
    blocks, ev = load()
    errors = []
    start = WS.LANDINGS["TAINARON"][0]
    states = {(c, r): sail(blocks, ev, start, c, r) for c in (False, True) for r in (False, True)}
    base, conch, ram, both = states[(False, False)], states[(True, False)], states[(False, True)], states[(True, True)]

    def reach_front(cells, x, y):
        return any(p in cells for p in fronts(x, y))

    # ---- every landing is water next to the land it serves, and its reach ------------
    for name, ((x, y), port, what) in WS.LANDINGS.items():
        if not is_water(blocks, x, y):
            errors.append(f"landing {name} at ({x},{y}) is not water")
        need = both if name in ("ITHAKA", "KERKYRA") else base
        if (x, y) not in need and not reach_front(need, x, y):
            errors.append(f"landing {name} at ({x},{y}) can't be reached")
        if name in ("ITHAKA", "KERKYRA") and ((x, y) in base or reach_front(base, x, y)):
            errors.append(f"landing {name} is reachable without Triton's Conch")
    # ---- gates ---------------------------------------------------------------------
    lagoon = (WS.LAGOON[0] + 1, WS.LAGOON[1])
    if reach_front(base, *lagoon) or reach_front(ram, *lagoon):
        errors.append("the lagoon's amphora is reachable without the Conch")
    if not reach_front(conch, *lagoon):
        errors.append("the lagoon's amphora can't be reached with the Conch")
    cove = WS.COVE
    if reach_front(base, *cove) or reach_front(conch, *cove):
        errors.append("the cove's find is reachable without the ram")
    if not reach_front(ram, *cove):
        errors.append("the cove's find can't be reached with the ram")
    beyond_fog = (0, WS.FOG_GATE[0][1])
    for st, cells in states.items():
        if beyond_fog in cells or any((x, y) in cells for (x, y) in WS.FOG_GATE):
            errors.append(f"the way through the fog is open in state conch={st[0]} ram={st[1]}")
    # the current's run: with the ram, from the cape you're carried through the reef fence
    east_of = (WS.BARRIER_X + 2, WS.CURRENT_ROWS[0])
    ride = sail(blocks, ev, east_of, False, True)
    west_end = (16, WS.CURRENT_ROWS[0])
    if west_end not in ride:
        errors.append("with the ram, the westward current doesn't carry you to the fog's approach")
    # ---- mandatory lines: Pontia and Aktaios close the reef fence; Nerites the gap ---
    sights = {}
    for name, (x, y, facing, sight, gfx, crossing) in WS.TRAINERS.items():
        dx, dy = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}[facing]
        sights[name] = {(x + dx * k, y + dy * k) for k in range(1, sight + 1)}
        for (sx, sy) in sights[name]:
            if solid(blocks, sx, sy):
                errors.append(f"{name}'s line crosses solid ({sx},{sy})")
    west_cell = WS.LANDINGS["ROUTE33"][0]
    fence_avoid = frozenset(sights["Pontia"] | sights["Aktaios"])
    if west_cell in sail(blocks, ev, start, False, False, fence_avoid):
        errors.append("the reef fence can be crossed without passing Pontia or Aktaios")
    if west_cell not in base:
        errors.append("Halia's jetty can't be reached from Tainaron")
    north = WS.LANDINGS["ITHAKA"][0]
    if north in sail(blocks, ev, start, True, False, frozenset(sights["Nerites"])):
        errors.append("the Echinades' gap can be crossed without passing Nerites")
    # ---- objects --------------------------------------------------------------------
    for o in ev["object_events"]:
        x, y, what = o["x"], o["y"], o.get("local_id") or o["script"]
        if o["movement_type"] == "MOVEMENT_TYPE_INVISIBLE":
            if solid(blocks, x, y):
                errors.append(f"{what} at ({x},{y}) holds a solid cell: it must be passable once removed")
            continue
        cells = both
        if o["trainer_type"] != "TRAINER_TYPE_NONE" or "Kymon" in o["script"] or "FindItem" in o["script"]:
            if not ((x, y) in cells or reach_front(cells, x, y)):
                errors.append(f"{what} at ({x},{y}) can't be reached")
    for name in ("Glaukon", "Pontia", "Aktaios", "Halieus"):
        x, y = WS.TRAINERS[name][:2]
        if not reach_front(base, x, y):
            errors.append(f"{name} can't be reached without relics")
    # ---- bg events -------------------------------------------------------------------
    for b in ev["bg_events"]:
        x, y = b["x"], b["y"]
        if b.get("script", "").endswith(("LandIthaka", "LandKerkyra")):
            continue
        cells = both
        if not reach_front(cells, x, y):
            errors.append(f"bg event {b.get('script') or b.get('item')} at ({x},{y}) can't be read")
    # ---- the hut ---------------------------------------------------------------------
    wx, wy = WS.HUT_DOOR
    if beh(blocks, wx, wy) not in WS.DOOR_BEHAVIORS:
        errors.append(f"the hut's door at ({wx},{wy}) is {beh(blocks, wx, wy)}")
    if (wx, wy + 1) not in base:
        errors.append("the hut's door can't be walked up to")
    if elev(blocks, wx, wy + 1) != 3:
        errors.append("the ground before the hut's door isn't land")
    # on foot: from the jetty's end (the ship's quay) to the hut's door
    def on_foot(x, y):
        return (0 <= x < W and 0 <= y < H and not solid(blocks, x, y) and elev(blocks, x, y) == 3
                and beh(blocks, x, y) not in WS.SURF_BEHAVIORS)
    quay = WS.JETTY[-1]
    seen, q = {quay}, deque([quay])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in seen and (on_foot(*n) or n == (wx, wy)):
                seen.add(n)
                q.append(n)
    if (wx, wy) not in seen:
        errors.append("the hut's door can't be walked to from the jetty's end")
    tx, ty = WS.LANDINGS["ROUTE33"][0]
    if not is_water(blocks, tx, ty) or abs(tx - quay[0]) + abs(ty - quay[1]) != 1:
        errors.append("the jetty's landing isn't the water beside its end")
    return errors


# ---------------------------------------------------------------------------
# Renders
# ---------------------------------------------------------------------------

# Where the player is for each review crop, along the sailing lines.
SCREENS = {
    "01_tainaron": (55, 64), "02_kymon": (46, 58), "03_fence_north": (39, 56), "04_cove": (43, 53),
    "05_current": (30, 64), "06_wreck": (31, 72), "07_fog": (14, 66), "08_corner": (22, 52),
    "09_islet": (17, 47), "10_altar": (8, 44), "11_echinades": (14, 39), "12_ithaka": (8, 25),
    "13_birds_rock": (25, 17), "14_lagoon": (33, 12), "15_kerkyra": (10, 6), "16_stone_ship": (12, 12),
}


def render(out_dir):
    from PIL import Image, ImageDraw
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    rm = [sys.executable, str(ROOT / "tools/ichor/render_map.py")]
    png = out / "route33.png"
    subprocess.run(rm + [WS.LAYOUT_ID, "--scale", "2", "-o", str(png)], check=True, stdout=subprocess.DEVNULL)
    blocks, ev = load()
    # the walk overlay
    im = Image.open(png).convert("RGBA")
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = 32
    for y in range(H):
        for x in range(W):
            if solid(blocks, x, y):
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 0, 0, 60))
            elif beh(blocks, x, y) in WS.CURRENTS:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(255, 255, 0, 50))
            elif elev(blocks, x, y) == 3:
                d.rectangle([x * c, y * c, x * c + c - 1, y * c + c - 1], fill=(0, 255, 0, 40))
    for o in ev["object_events"]:
        col = (255, 0, 255, 255) if o["movement_type"] == "MOVEMENT_TYPE_INVISIBLE" else (255, 255, 0, 255)
        d.ellipse([o["x"] * c + 6, o["y"] * c + 6, o["x"] * c + c - 7, o["y"] * c + c - 7], outline=col, width=3)
    for w_ in ev["warp_events"]:
        d.rectangle([w_["x"] * c + 2, w_["y"] * c + 2, w_["x"] * c + c - 3, w_["y"] * c + c - 3],
                    outline=(0, 255, 255, 255), width=3)
    for b in ev["bg_events"]:
        col = (255, 255, 255, 255) if b["type"] == "sign" else (0, 255, 0, 255)
        d.line([b["x"] * c + 4, b["y"] * c + 4, b["x"] * c + c - 5, b["y"] * c + c - 5], fill=col, width=3)
        d.line([b["x"] * c + c - 5, b["y"] * c + 4, b["x"] * c + 4, b["y"] * c + c - 5], fill=col, width=3)
    Image.alpha_composite(im, lay).save(out / "route33_walk.png")
    # screen crops from the map padded with its border (open sea)
    margin = 8
    big = np.full((H + 2 * margin, W + 2 * margin), WS.SEA, np.uint16)
    big[margin:margin + H, margin:margin + W] = blocks
    tmp = out / "padded.bin"
    big.astype("<u2").tofile(tmp)
    padded = out / "padded.png"
    subprocess.run(rm + ["--blockdata", str(tmp), "--width", str(big.shape[1]), "--primary", "aethos",
                         "--secondary", "westsea", "--scale", "2", "-o", str(padded)],
                   check=True, stdout=subprocess.DEVNULL)
    pim = Image.open(padded)
    crops = []
    for name, (px, py) in SCREENS.items():
        x0, y0 = (px - 7 + margin) * c, (py - 4 + margin) * c
        crop = pim.crop((x0, y0, x0 + 15 * c, y0 + 10 * c))
        crop.save(out / f"screen_{name}.png")
        crops.append(crop)
    cols = 4
    sheet = Image.new("RGB", (cols * 15 * c + (cols - 1) * 8, -(-len(crops) // cols) * (10 * c + 8) - 8),
                      (24, 24, 32))
    for i, crop in enumerate(crops):
        sheet.paste(crop, ((i % cols) * (15 * c + 8), (i // cols) * (10 * c + 8)))
    sheet.save(out / "route33_screens.png")
    tmp.unlink()
    padded.unlink()
    print(f"westsea_review: renders in {out}")


if __name__ == "__main__":
    errs = check()
    for e in errs:
        print("CHECK:", e)
    sys.exit(1 if errs else 0)
