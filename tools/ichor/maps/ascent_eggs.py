#!/usr/bin/env python3
"""The gods' small easter eggs on the Ascent's older floors (design/maps/Ascent_*.md):
inspects and hidden finds added after each floor's own builder has run, so the
builders stay as they are. Each egg names a spot near where it belongs; this file
finds the nearest cell that fits (a sign goes on a blocked cell beside one you
can walk to, a hidden find on a cell you can walk to) and writes its event and
its line. Run it after the builders (tools/ichor/maps/olympus_all.sh does);
it is idempotent.

The outdoor floors' eggs are in their own builders (oros_maps.py, propylon.py).
"""
from __future__ import annotations

import json
import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
MARK = "// --- the gods' easter eggs (tools/ichor/maps/ascent_eggs.py) ---"

# map: (start cell for reachability, [(kind, x, y, name, payload)])
#   kind "sign": payload is the line; kind "hidden": payload is (item, flag, line or None)
EGGS = {
    "Ascent_1F": ((44, 26), [
        ("sign", 23, 24, "PanPipes", "A set of reed pipes left on the guard's seat, seven reeds bound with wax.\\p"
                                     "The wind plays the eighth. Pan never could sit still for long."),
        ("hidden", 24, 25, "PanBell", ("ITEM_SOOTHE_BELL", "FLAG_ICHOR_HIDDEN_ITEM_ASCENT1_SOOTHE_BELL", None)),
        ("sign", 29, 25, "HermWreath", "Someone keeps a fresh wreath on this herm, even this far up.\\p"
                                       "The god of travellers is owed that much by anyone climbing."),
    ]),
    "Ascent_2F": ((5, 43), [
        ("sign", 8, 25, "Fennel", "A fennel stalk propped by the cookfire, and in its pith a coal, still glowing.\\p"
                                  "It's been burning longer than the camp has. Longer than the mountain's had a name."),
        ("hidden", 9, 27, "FennelCharcoal", ("ITEM_CHARCOAL", "FLAG_ICHOR_HIDDEN_ITEM_ASCENT2_CHARCOAL", None)),
        ("sign", 15, 25, "Jar", "A big jar, sealed with pitch. Scratched on the lid: DON'T.\\p"
                                "The cook says it's Pandora's, and it's full of olives. He won't open it to prove it."),
    ]),
    "Ascent_Icefall": ((20, 44), [
        ("sign", 13, 12, "Hammer", "A smith's hammer is frozen into the ice here, haft up.\\p"
                                   "The haft is warm. It shouldn't be. Hephaestus never could keep track of his tools."),
        ("hidden", 14, 13, "HammerStone", ("ITEM_HARD_STONE", "FLAG_ICHOR_HIDDEN_ITEM_ICEFALL_HARD_STONE", None)),
        ("sign", 22, 2, "Boreas", "The frost on the wall has made a face: cheeks puffed out, mid-blow.\\p"
                                  "The north wind came through here once and left his likeness behind."),
    ]),
    "Ascent_IcefallDeep": ((8, 5), [
        ("sign", 12, 3, "Owl", "Two round eyes shine back at you from a ledge above the tarn.\\p"
                               "An owl, Athena's kind. It has watched everything you did in the dark, and it isn't telling."),
        ("hidden", 17, 9, "Obol", ("ITEM_RELIC_COPPER", "FLAG_ICHOR_HIDDEN_ITEM_DEEP_RELIC_COPPER", None)),
        ("sign", 10, 22, "Ferry", "A coin lies on the tarn's shore, set there on purpose: a fare for a ferryman.\\p"
                                  "Charon never comes this far up. Somebody hoped anyway."),
    ]),
    "Ascent_CrystalVault": ((11, 18), [
        ("hidden", 19, 13, "Apple", ("ITEM_SWEET_APPLE", "FLAG_ICHOR_HIDDEN_ITEM_VAULT_SWEET_APPLE",
                                     "Something gold is wedged between two crystals: an apple, scratched FOR THE FAIREST.\\p"
                                     "Eris threw one of these once and started a war. Best not to toss it to anyone.")),
        ("sign", 5, 12, "Wheel", "Deep inside one crystal, a gold wheel turns, very slowly.\\p"
                                 "The crystal hasn't moved in an age. The wheel has never stopped."),
    ]),
    "Olympus_Summit": ((13, 25), [
        ("sign", 12, 12, "Cup", "A gold cup has been left on the altar's step, still half full.\\p"
                                "Ganymede poured for the gods up here. Of what, you'd rather not ask."),
        ("sign", 8, 9, "Feather", "An eagle's feather, long as your arm, caught in the crag's foot.\\p"
                                  "Gold at the quill. Something up the cone keeps shedding them."),
        ("script", 0, 0, "StatueZeus", "ZEUS, FATHER OF GODS AND MEN. Painted marble: the thunderbolt raised, the eagle on his arm.\\p"
                                       "Whoever carved him gave him the Archon's eyes. Or the other way round."),
    ]),
}


def blocks(name):
    lay = json.loads((ROOT / f"data/maps/{name}/map.json").read_text())["layout"]
    data = json.loads((ROOT / "data/layouts/layouts.json").read_text())
    L = next(l for l in data["layouts"] if l.get("id") == lay)
    raw = np.fromfile(ROOT / L["blockdata_filepath"], "<u2").reshape(L["height"], L["width"])
    return raw


def walk_set(name, start):
    raw = blocks(name)
    H, W = raw.shape
    m = json.loads((ROOT / f"data/maps/{name}/map.json").read_text())
    solid = (raw >> 10) & 3 != 0
    for o in m.get("object_events", []):
        if 0 <= o["x"] < W and 0 <= o["y"] < H:
            solid[o["y"], o["x"]] = True
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            X, Y = x + dx, y + dy
            if 0 <= X < W and 0 <= Y < H and (X, Y) not in seen and not solid[Y, X]:
                seen.add((X, Y))
                q.append((X, Y))
    return seen, solid, W, H


def nearest(x, y, ok, W, H):
    best = None
    for Y in range(H):
        for X in range(W):
            if ok(X, Y):
                d = abs(X - x) + abs(Y - y)
                if best is None or d < best[0]:
                    best = (d, X, Y)
    if best is None:
        raise SystemExit(f"no spot near {x},{y}")
    return best[1], best[2]


def apply(name, start, eggs):
    seen, solid, W, H = walk_set(name, start)
    used = set()
    mpath = ROOT / f"data/maps/{name}/map.json"
    m = json.loads(mpath.read_text())
    prefix = f"{name}_EventScript_Egg"
    m["bg_events"] = [b for b in m["bg_events"] if not str(b.get("script", "")).startswith(prefix)
                      and not (b.get("type") == "hidden_item" and any(e[0] == "hidden" and e[4][1] == b.get("flag")
                                                                      for e in eggs))]
    taken = {(b["x"], b["y"]) for b in m["bg_events"]}
    text = [MARK]
    for kind, x, y, nm, payload in eggs:
        if kind == "script":
            text.append(f'script {name}_EventScript_{nm} {{\n    msgbox(format("{payload}"), MSGBOX_SIGN)\n}}\n')
            continue
        if kind == "sign":
            X, Y = nearest(x, y, lambda X, Y: solid[Y, X] and (X, Y) not in taken | used and any(
                (X + dx, Y + dy) in seen for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))), W, H)
            m["bg_events"].append(dict(type="sign", x=X, y=Y, elevation=0, player_facing_dir="BG_EVENT_PLAYER_FACING_ANY",
                                       script=f"{prefix}{nm}"))
            text.append(f'script {prefix}{nm} {{\n    msgbox(format("{payload}"), MSGBOX_SIGN)\n}}\n')
        else:
            item, flag, line = payload
            X, Y = nearest(x, y, lambda X, Y: (X, Y) in seen and (X, Y) not in taken | used and (X, Y) != start, W, H)
            m["bg_events"].append(dict(type="hidden_item", x=X, y=Y, elevation=3, item=item, flag=flag, quantity=1,
                                       underfoot=False))
            if line:
                SX, SY = nearest(X, Y, lambda A, B: solid[B, A] and (A, B) not in taken | used and abs(A - X) + abs(B - Y) == 1
                                 and any((A + dx, B + dy) in seen for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))), W, H)
                m["bg_events"].append(dict(type="sign", x=SX, y=SY, elevation=0,
                                           player_facing_dir="BG_EVENT_PLAYER_FACING_ANY", script=f"{prefix}{nm}"))
                text.append(f'script {prefix}{nm} {{\n    msgbox(format("{line}"), MSGBOX_SIGN)\n}}\n')
                used.add((SX, SY))
        used.add((X, Y))
    mpath.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    spath = ROOT / f"data/maps/{name}/scripts.pory"
    s = spath.read_text()
    if MARK in s:
        s = s[:s.index(MARK)].rstrip("\n") + "\n"
    spath.write_text(s + "\n" + "\n".join(text))
    print(f"{name}: {len(eggs)} eggs")


def main():
    for name, (start, eggs) in EGGS.items():
        apply(name, start, eggs)


if __name__ == "__main__":
    main()
