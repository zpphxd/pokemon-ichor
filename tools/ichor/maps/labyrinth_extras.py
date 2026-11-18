"""What every upper ring adds on top of its maze (design/maps/Labyrinth_System.md):

- **relic obstacles** on the passages every route must cross (labyrinth_lib's
  maze bridges) and on side loops: marble rubble for the Bronze Hammer in the
  masonry, roots for Demeter's Sickle in the cave, bronze chains for the Labrys,
  column drums for the Girdle. They are the expansion's field obstacles
  (ENGINE_API §2), so they come back when the map reloads, as in Emerald;
- **Daedalus's floor seals:** Strength puzzles. Column drums pushed onto bronze
  plates (the herald plate's metatile) open a grate or a door. The check runs
  from coord events on the cells a player stands on after a push; leaving the
  map, or the reset lever, puts the drums back (FLAG_TEMP_* hold the open
  state, so nothing can be locked);
- **cellars:** a stair down in one dead end to a sealed cell elsewhere in the
  ring, with treasure and a stair back up;
- **the lost:** remains of the Athenian tribute and of explorers since, read as
  signs, some holding an item.
"""
from __future__ import annotations

from labyrinth_lib import PITCH, ST, cell, gap, mid, setmetatiles

KINDS = {
    "rubble": ("BREAKABLE_ROCK", "EventScript_RockSmash", "Bronze Hammer"),
    "roots": ("CUTTABLE_TREE", "EventScript_CutTree", "Demeter's Sickle"),
    "drum": ("PUSHABLE_BOULDER", "EventScript_StrengthBoulder", "Girdle of Herakles"),
    "chain": ("BREAKABLE_ROCK", "EventScript_IchorLabrysSeal", "Labrys"),
    "web": ("CUTTABLE_TREE", "EventScript_IchorCobweb", "Hecate's Torch"),
    "thornweb": ("CUTTABLE_TREE", "EventScript_IchorThornweb", "the Three-Flamed Torch (post-game)"),
    "boulder": ("PUSHABLE_BOULDER", "EventScript_IchorGreatBoulder", "Hephaestus's Hammer (post-game)"),
}


def log(m, what):
    m.relic_log = getattr(m, "relic_log", [])
    m.relic_log.append(what)


def obstacle(m, x, y, kind, flag=None, why=""):
    """A field obstacle. It hides on a temp flag (FLAG_TEMP_10 up, one per
    obstacle on the map): cleared on every map load, so the obstacle comes
    back when the player leaves, as in Emerald."""
    gfx, script, relic = KINDS[kind]
    if flag is None:
        m.temp_next = getattr(m, "temp_next", 0x10)
        assert m.temp_next <= 0x1F, "out of temp flags for obstacles"
        flag = f"FLAG_TEMP_{m.temp_next:X}"
        m.temp_next += 1
    m.obj(gfx, x, y, script, flag=flag)
    log(m, f"{relic}: {kind} at ({x},{y}){' — ' + why if why else ''}")


def block_gap(m, a, b, kind, why=""):
    """Both lanes of the passage between nodes a and b, on the side nearer a."""
    cells = gap(a, b)
    (ax, ay) = a
    if a[1] == b[1]:
        xs = sorted({c[0] for c in cells})
        x = xs[0] if b[0] > a[0] else xs[-1]
        lanes = [(x, c[1]) for c in cells if c[0] == x]
    else:
        ys = sorted({c[1] for c in cells})
        y = ys[0] if b[1] > a[1] else ys[-1]
        lanes = [(c[0], y) for c in cells if c[1] == y]
    for (x, y) in lanes:
        obstacle(m, x, y, kind, why=why)


def plate_puzzle(m, tag, drums, plates, opens, temp_flag, check_cells, reset, prefix, why):
    """drums: [(x, y)]; plates: [(x, y)] (laid as bronze plates); opens: [(x, y,
    open metatile, open solid, shut metatile, shut solid)]; check_cells: where a
    player stands after a push; reset: (x, y) of the lever, warping back to
    (rx, ry)."""
    pm = mid("plate", "plate")
    for (x, y) in plates:
        m.set(x, y, pm, False)
        m.floors_used.add("plate")
    ids = []
    for i, (x, y) in enumerate(drums):
        lid = f"LOCALID_{m.name.upper()}_{tag}_DRUM{i}"
        m.obj("PUSHABLE_BOULDER", x, y, "EventScript_StrengthBoulder", local_id=lid)
        ids.append(lid)
    op = [(x, y, t, s) for (x, y, t, s, _, _) in opens]
    sh = [(x, y, t, s) for (x, y, _, _, t, s) in opens]
    m.gen += [f"if (flag({temp_flag})) {{"] + setmetatiles(op, "    ") + ["} else {"] + setmetatiles(sh, "    ") + ["}"]
    for (x, y) in check_cells:
        m.trigger(x, y, prefix + f"Plates{tag}")
    lx, ly, rx, ry = reset
    m.sign(lx, ly, prefix + f"Lever{tag}")
    s = ["", f"// Daedalus's floor seal {tag}: {why}",
         f"script {prefix}Plates{tag} {{", f"    if (flag({temp_flag})) {{", "        end", "    }",
         "    setvar(VAR_TEMP_9, 0)"]
    for lid in ids:
        s.append(f"    getobjectxy({lid}, CURRENT_POSITION, VAR_0x8007, VAR_0x8008)")
        for (px, py) in plates:
            s += [f"    if (var(VAR_0x8007) == {px} && var(VAR_0x8008) == {py}) {{", "        addvar(VAR_TEMP_9, 1)", "    }"]
    s += [f"    if (var(VAR_TEMP_9) == {len(plates)}) {{", "        lockall", f"        setflag({temp_flag})",
          f"        call({m.name}_EventScript_DrawState)", "        special(DrawWholeMapView)", "        playse(SE_DOOR)",
          '        msgbox(format("Bronze clanks deep in the wall. Something has opened."), MSGBOX_DEFAULT)',
          "        releaseall", "    }", "}", "",
          f"script {prefix}Lever{tag} {{", "    lockall",
          '    msgbox(format("A bronze lever with a double axe for a handle: Daedalus\'s reset.\\pPull it?"), MSGBOX_YESNO)',
          "    if (var(VAR_RESULT) == YES) {", "        closemessage", "        playse(SE_CLICK)",
          f"        warpsilent({map_id(m)}, {rx}, {ry})", "        waitstate", "    }", "    releaseall", "}"]
    m.extra_scripts = getattr(m, "extra_scripts", []) + s
    log(m, f"Girdle of Herakles: floor seal {tag}, {len(drums)} drums onto {len(plates)} plates — {why}")


def map_id(m):
    import re
    return "MAP_" + re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", m.name).upper()


def cellar(m, d1, d2, item, flag, prefix, tag, story):
    """A stair down in dead-end node d1's north face to the sealed node d2 (its
    passage walled off), holding `item`, with a stair back up in d2's face."""
    x1, y1 = cell(d1)
    x2, y2 = cell(d2)
    m.stairs(x1, y1 - 1, "down")
    m.stairs(x2, y2 - 1, "up")
    a = len(m.warps)
    m.warp(x1, y1 - 1, map_id(m), a + 2)
    m.warp(x1 + 1, y1 - 1, map_id(m), a + 2)
    m.arrival(x2, y2)
    m.warp(x2, y2 - 1, map_id(m), a + 5)
    m.warp(x2 + 1, y2 - 1, map_id(m), a + 5)
    m.arrival(x1, y1)
    m.item(x2 + 1, y2 + 1, item, flag)
    m.sign(x2 + 1, y2 - 2 if False else y2 - 1, prefix + f"Cellar{tag}") if False else None
    log(m, f"cellar {tag}: stairs at node {d1} down to the sealed cell {d2}: {item} — {story}")


def free_dead_ends(m, mz):
    """Dead-end nodes with nothing in them yet, and a passage cell leading in."""
    busy = {(o["x"], o["y"]) for o in m.objects} | {(b["x"], b["y"]) for b in m.bgs} | \
        {(c["x"], c["y"]) for c in m.coords} | {(w["x"], w["y"]) for w in m.warps} | {(a[0], a[1]) for a in m.anchors}
    out = []
    for n in mz.metrics()["dead"]:
        if len(n) != 2:
            continue
        cells = [cell(n, i, j) for i in range(2) for j in range(2)]
        if any(c in busy for c in cells) or not all(m.walkable(*c) for c in cells):
            continue
        nb = [b for b in mz.nbrs(n) if frozenset({n, b}) in mz.edges]
        if len(nb) == 1:
            out.append((n, nb[0]))
    return out


def later_gate(m, slot, kind, hide_flag, prefix, tag, species, level, static_flag, item, item_flag, story):
    """A gate for a relic the player gets later: the obstacle across the dead
    end's mouth (hidden for good by hide_flag), and behind it a stronger
    Pokémon (a scripted encounter on the dead end's back wall) and an item."""
    n, mouth = slot
    lanes = []
    cells = gap(n, mouth)
    if n[1] == mouth[1]:
        x = sorted({c[0] for c in cells})[0 if mouth[0] < n[0] else -1]
        x = max(c[0] for c in cells) if mouth[0] < n[0] else min(c[0] for c in cells)
        lanes = [(x, c[1]) for c in cells if c[0] == x]
    else:
        y = max(c[1] for c in cells) if mouth[1] < n[1] else min(c[1] for c in cells)
        lanes = [(c[0], y) for c in cells if c[1] == y]
    gfx, script, relic = KINDS[kind]
    m.obj(gfx, lanes[0][0], lanes[0][1], script, flag=hide_flag)
    for (x, y) in lanes[1:]:
        m.obj(gfx, x, y, script, flag=hide_flag)
    x0, y0 = cell(n)
    m.item(x0, y0, item, item_flag)
    m.sign(x0 + 1, y0 + 1, prefix + f"Lair{tag}")
    s = ["", f"// Hook for later ({relic}): {story}",
         f"script {prefix}Lair{tag} {{", "    lockall", f"    if (!flag({static_flag})) {{",
         '        msgbox(format("Something shifts in the dark at the end of the passage."), MSGBOX_DEFAULT)',
         "        closemessage", f"        setwildbattle(SPECIES_{species.upper()}, {level})", "        dowildbattle",
         f"        setflag({static_flag})", "    } else {",
         '        msgbox(format("Old scratches on the rock. Whatever lived here has gone."), MSGBOX_DEFAULT)',
         "    }", "    releaseall", "}"]
    m.extra_scripts = getattr(m, "extra_scripts", []) + s
    log(m, f"{relic} (later): {kind} across dead end {n}: {species} Lv {level} and {item} — {story}")


REGISTRY = None


def cellar_entries(m, mz, rooms, prefix):
    """Stairs down into the Labyrinth's cellars (MAP_LABYRINTH_CELLARS) from
    dead ends whose north wall is a plain face: each `rooms` entry is the cellar
    room it leads to. Records each ring arrival for the cellars' stairs back up
    in tools/ichor/maps/labyrinth_cellars.json."""
    import json
    from pathlib import Path
    reg_p = Path(__file__).resolve().parent / "labyrinth_cellars.json"
    reg = json.loads(reg_p.read_text()) if reg_p.exists() else {}
    faces = {mid("walls", n) for n in ("face_cc", "face_ci", "face_ic", "face_ii", "face_oo", "face_oc", "face_co", "face_io", "face_oi")} | {mid("niche", n) for n in ("back", "shrine", "lamp_out")}
    faces |= {ST["cave_rock"]["ids"][xy[1]][xy[0]] for k, xy in ST["cave_rock"]["names"].items() if k.startswith("fb")}
    busy = {(b["x"], b["y"]) for b in m.bgs} | {(o["x"], o["y"]) for o in m.objects} | \
        {(w["x"], w["y"]) for w in m.warps} | {(c["x"], c["y"]) for c in m.coords}
    slots = []
    for n in mz.metrics()["dead"]:
        if len(n) != 2:
            continue
        x, y = cell(n)
        f = [(x, y - 1), (x + 1, y - 1)]
        if all(int(m.mid[fy, fx]) in faces and (fx, fy) not in busy for fx, fy in f) and m.walkable(x, y + 1) \
                and (x, y + 1) not in busy and (x + 1, y) not in busy:
            slots.append(n)
    for room, n in zip(rooms, slots):
        x, y = cell(n)
        m.stairs(x, y - 1, "down")
        m.warp(x, y - 1, "MAP_LABYRINTH_CELLARS", 3 * room)
        m.warp(x + 1, y - 1, "MAP_LABYRINTH_CELLARS", 3 * room)
        reg[str(room)] = [map_id(m), len(m.warps)]
        m.arrival(x, y + 1)
        log(m, f"stairs down at dead end {n} to cellar room {room}")
    # any room left over gets a hole in the floor of a free dead end instead
    left = rooms[len(slots):]
    used = set(slots)
    for room in left:
        cands = []
        for n in mz.metrics()["dead"]:
            if len(n) != 2 or n in used:
                continue
            free = [c for c in [cell(n, i, j) for i in range(2) for j in range(2)] if c not in busy and m.walkable(*c)]
            if len(free) >= 2:
                cands.append((-len(free), n, free))
        if not cands:
            break
        _, n, free = sorted(cands)[0]
        used.add(n)
        (hx, hy), (ax, ay) = free[-1], free[0]
        m.put("hole", hx, hy)
        m.stops.add((hx, hy))
        m.trigger(hx, hy, prefix + f"CellarHole{room}")
        reg[str(room)] = [map_id(m), len(m.warps)]
        m.arrival(ax, ay)
        m.extra_scripts = getattr(m, "extra_scripts", []) + [
            "", f"script {prefix}CellarHole{room} {{", "    lockall",
            '    msgbox(format("The floor here is only rubble over a hole. It gives!"), MSGBOX_DEFAULT)',
            "    closemessage", "    playse(SE_FALL)", f"    warp(MAP_LABYRINTH_CELLARS, {3 * room})", "    waitstate", "}"]
        log(m, f"a hole in dead end {n} down to cellar room {room}")
    reg_p.write_text(json.dumps(reg, indent=1, sort_keys=True) + "\n")
    return slots[:len(rooms)]


def remains(m, x, y, prefix, tag, text, item=None, flag=None):
    m.sign(x, y, prefix + f"Remains{tag}")
    if item:
        m.hidden(x, y, item, flag)
    s = ["", f"script {prefix}Remains{tag} {{", f"    msgbox(format(\"{text}\"), MSGBOX_SIGN)", "}"]
    m.extra_scripts = getattr(m, "extra_scripts", []) + s
    m.lost_log = getattr(m, "lost_log", [])
    m.lost_log.append((tag, (x, y), text, item))
