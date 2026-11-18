"""The heart's share of the Labyrinth's extras (design/maps/Labyrinth_System.md; the upper
rings' are tools/ichor/maps/labyrinth_extras.py, whose relic obstacles and remains these
reuse): relic obstacles the player must clear, Daedalus's floor seal (drums onto bronze
plates), stairs and holes down to sealed treasure pockets, and the remains of the lost.
Everything is placed by the ring builders in labyrinth_heart.py, so reruns keep it, and
the scripts land between the EXTRAS markers in each map's scripts.pory."""
from __future__ import annotations

import re

from labyrinth_extras import log, obstacle, remains  # noqa: F401  (re-exported)

ROOT = None
BEGIN, END = "// ---- BEGIN GENERATED EXTRAS ----", "// ---- END GENERATED EXTRAS ----"


def map_id(m):
    return "MAP_" + re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", m.name).upper()


def busy(m):
    return ({(o["x"], o["y"]) for o in m.objects} | {(b["x"], b["y"]) for b in m.bgs}
            | {(c["x"], c["y"]) for c in m.coords} | {(w["x"], w["y"]) for w in m.warps}
            | {(a[0], a[1]) for a in m.anchors} | set(m.deco))


def rock_rect(m, w, h, avoid=(), near=None, margin=1):
    """The top-left of a w x h block of solid cave rock (with a rock margin), nearest
    `near` if given."""
    best = None
    for y0 in range(1, m.h - h):
        for x0 in range(1, m.w - w):
            ok = all(m.T(x, y) == "R" and (x, y) not in avoid and (x, y) not in m.deco
                     for y in range(y0 - margin, y0 + h + margin) for x in range(x0 - margin, x0 + w + margin))
            if ok:
                d = 0 if near is None else abs(x0 - near[0]) + abs(y0 - near[1])
                if best is None or d < best[0]:
                    best = (d, (x0, y0))
    return best[1] if best else None


def arrival(m, x, y):
    m.warp(x, y, map_id(m), 0)
    m.warps[-1].update({"_scripted": True, "unreached_ok": True})
    return len(m.warps) - 1


def stair_entry(m, avoid=(), far_from=None):
    """A floor cell (x, y) with (x+1, y) floor and both cells north of them solid wall,
    nothing on them: where a stair down can be cut. Farthest from `far_from`."""
    b = busy(m) | set(avoid)
    cands = []
    for y in range(2, m.h - 1):
        for x in range(1, m.w - 2):
            if all(m.T(cx, cy) in ".," and (cx, cy) not in b for cx, cy in ((x, y), (x + 1, y))) \
                    and all(m.T(cx, y - 1) in "RM" and (cx, y - 1) not in m.deco for cx in (x, x + 1)) \
                    and all(m.T(cx, y - 2) in "RM" for cx in (x, x + 1)):
                d = 0 if far_from is None else abs(x - far_from[0]) + abs(y - far_from[1])
                cands.append((-d, (x, y)))
    return sorted(cands)[0][1] if cands else None


def treasure_stair(m, prefix, tag, item, flag, story, avoid=(), far_from=None):
    """Stairs down from a passage to a sealed pocket in the rock, with treasure and a
    stair back up (LABYRINTH_MAZE §3; the user's 'stairs and ladders to treasure')."""
    e = stair_entry(m, avoid, far_from)
    p = rock_rect(m, 4, 4, avoid=avoid, near=e) or rock_rect(m, 4, 3, avoid=avoid, near=e, margin=0)
    if not e or not p:
        log(m, f"treasure stair {tag}: no room")
        return
    x, y = e
    px, py = p
    deep = 3 if all(m.T(x_, py + 3) == "R" for x_ in range(px, px + 4)) else 2
    m.carve(px, py + 1, px + 3, py + deep, ".")        # the pocket; its north row stays rock (the stair up)
    for cx in (x, x + 1):
        m.cell(cx, y - 1, "M")
    for cx in (px + 1, px + 2):
        m.cell(cx, py, "M")
    m.place(x, y - 1, "stairs", "down_l", solid=False)
    m.place(x + 1, y - 1, "stairs", "down_r", solid=False)
    m.place(px + 1, py, "stairs", "up_l", solid=False)
    m.place(px + 2, py, "stairs", "up_r", solid=False)
    a = len(m.warps)
    m.warp(x, y - 1, map_id(m), a + 2)
    m.warp(x + 1, y - 1, map_id(m), a + 2)
    arrival(m, px + 1, py + 1)
    m.warp(px + 1, py, map_id(m), a + 5)
    m.warp(px + 2, py, map_id(m), a + 5)
    arrival(m, x, y)
    for w in m.warps[a:]:
        w["unreached_ok"] = True
    m.item_ball(px + 3, py + deep, item, flag)
    m.notes[(x, y)] = "stair"
    log(m, f"stairs down at ({x},{y}) to a sealed pocket at ({px},{py}): {item} — {story}")


def treasure_hole(m, prefix, tag, item, flag, story, avoid=(), far_from=None):
    """A hole in a dead end's floor drops into a sealed pocket; a rope climbs back out."""
    from labyrinth_heart import dead_ends
    b = busy(m) | set(avoid)
    m.lay()
    reach = m.reach([(m.warps[0]["x"], m.warps[0]["y"] + 1)])
    ends = [c for c in dead_ends(m) if m.T(*c) == "." and c not in b and c in reach]
    if far_from:
        ends.sort(key=lambda c: -(abs(c[0] - far_from[0]) + abs(c[1] - far_from[1])))
    if not ends:   # no free dead end: cut a one-cell alcove off a cave passage instead
        for y in range(2, m.h - 2):
            for x in range(2, m.w - 2):
                if m.T(x, y) != "." or (x, y) in b or (x, y) not in reach:
                    continue
                for dx, dy in ((0, -1), (1, 0), (-1, 0), (0, 1)):
                    sx, sy = x + dx, y + dy
                    if m.T(sx, sy) == "R" and (sx, sy) not in m.deco and all(
                            m.T(sx + ex, sy + ey) == "R" for ex, ey in ((0, -1), (1, 0), (-1, 0), (0, 1)) if (ex, ey) != (-dx, -dy)):
                        ends.append((sx, sy))
        if far_from:
            ends.sort(key=lambda c: -(abs(c[0] - far_from[0]) + abs(c[1] - far_from[1])))
        if not ends:
            log(m, f"treasure hole {tag}: no room")
            return
        m.cell(*ends[0], ".")
    hx, hy = ends[0]
    p, rows = rock_rect(m, 3, 4, avoid=avoid, near=(hx, hy)), 2
    if not p:
        p, rows = rock_rect(m, 3, 3, avoid=avoid, near=(hx, hy), margin=0), 1
    if not p:
        log(m, f"treasure hole {tag}: no room")
        return
    px, py = p
    m.carve(px, py + 2, px + 2, py + 1 + rows, ".")            # the pocket; rows py, py+1: the rope's face
    m.place(hx, hy, "formations", "hole", solid=False)
    m.place(px + 1, py + 1, "formations", "climb", solid=False)
    m.place(px + 1, py, "formations", "climb_top", solid=True)
    a = len(m.warps)
    arrival(m, px + 1, py + 2)                            # a: under the rope, where the fall lands
    m.warp(px + 1, py + 1, map_id(m), a + 2)              # a+1: the rope up
    m.warps[-1]["unreached_ok"] = True
    nb = [(hx + dx, hy + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if m.walkable_t(hx + dx, hy + dy)]
    arrival(m, *nb[0])                                    # a+2: back up beside the hole
    m.trigger(hx, hy, prefix + f"Hole{tag}", var="VAR_TEMP_0", value=0)
    m.item_ball(px + 2, py + 1 + rows, item, flag)
    m.extra_scripts = getattr(m, "extra_scripts", []) + [
        "", f"script {prefix}Hole{tag} {{", "    lockall",
        '    msgbox(format("The floor is only a crust of flowstone over a hole. It gives!"), MSGBOX_DEFAULT)',
        "    closemessage", "    playse(SE_FALL)", f"    warp({map_id(m)}, {a})", "    waitstate", "    releaseall", "}"]
    log(m, f"a hole at ({hx},{hy}) down to a sealed pocket, a rope back up: {item} — {story}")


def floor_seal(m, prefix, tag, temp_flag, item, flag, why, avoid=(), near=None, at=None):
    """Daedalus's floor seal: a small room off a passage with two column drums to push
    onto two bronze plates (the Girdle of Herakles); both pressed, a grate opens on an
    alcove with treasure. A lever in the north wall resets it (a quiet warp back)."""
    b = busy(m) | set(avoid)
    best = None
    for y0 in range(2, m.h - 7):
        for x0 in range(2, m.w - 9):
            room = [(x, y) for x in range(x0, x0 + 5) for y in range(y0 + 1, y0 + 5)]
            if any(c in b or c in m.deco or m.T(*c) not in "R.," for c in room):
                continue
            if not any(m.walkable_t(*c) for c in room) and not m.walkable_t(x0 - 1, y0 + 2):
                continue
            if not all(m.T(x, y) == "R" and (x, y) not in m.deco for x in (x0 + 5, x0 + 6)
                       for y in range(y0 + 2, y0 + 5)):
                continue
            if not all(m.T(x, y) in "RM" for (x, y) in [(x0 + 7, y) for y in range(y0 + 1, y0 + 6)]
                       + [(x0 + 5, y0 + 1), (x0 + 6, y0 + 1), (x0 + 5, y0 + 5), (x0 + 6, y0 + 5)]):
                continue
            if m.T(x0 + 2, y0) not in "RM" or (x0 + 2, y0) in m.deco:
                continue
            if any(m.T(x, y0) not in "RM" for x in range(x0, x0 + 5)):
                continue
            d = 0 if near is None else abs(x0 - near[0]) + abs(y0 - near[1])
            if best is None or d < best[0]:
                best = (d, (x0, y0))
    if at:
        best = (0, at)
    if not best:
        log(m, f"floor seal {tag}: no room")
        return
    x0, y0 = best[1]
    m.carve(x0, y0 + 1, x0 + 4, y0 + 4, ".")
    m.carve(x0 + 6, y0 + 2, x0 + 6, y0 + 4, ".")          # the alcove behind the grate
    m.cell(x0 + 5, y0 + 3, "M")
    m.place(x0 + 5, y0 + 3, "doorways", "grate", solid=True)
    m.cell(x0 + 2, y0, "M")
    m.place(x0 + 2, y0, "dials", "lever", solid=True)
    drums = [(x0 + 1, y0 + 2), (x0 + 3, y0 + 2)]
    plates = [(x0 + 1, y0 + 4), (x0 + 3, y0 + 4)]
    for (x, y) in plates:
        m.place(x, y, "plate", "plate", solid=False)
        m.nothread.add((x, y))
    ids = []
    for i, (x, y) in enumerate(drums):
        lid = f"LOCALID_{m.name.upper()}_{tag}_DRUM{i}"
        m.obj("PUSHABLE_BOULDER", x, y, "EventScript_StrengthBoulder", local_id=lid)
        ids.append(lid)
    m.item_ball(x0 + 6, y0 + 3, item, flag)
    for x in range(x0, x0 + 5):
        for y in range(y0 + 1, y0 + 4):
            if (x, y) not in drums:
                m.trigger(x, y, prefix + f"Plates{tag}", var="VAR_TEMP_0", value=0)
    cave = "METATILE_Mychos_CaveFloor"
    m.gen += [f"if (flag({temp_flag})) {{", f"    setmetatile({x0 + 5}, {y0 + 3}, {cave}, FALSE)",
              "} else {", f"    setmetatile({x0 + 5}, {y0 + 3}, METATILE_Mychos_Grate, TRUE)", "}"]
    m.sign(x0 + 2, y0, prefix + f"Lever{tag}")
    s = ["", f"// Daedalus's floor seal {tag}: {why}", f"script {prefix}Plates{tag} {{",
         f"    if (flag({temp_flag})) {{", "        end", "    }", "    setvar(VAR_TEMP_9, 0)"]
    for lid in ids:
        s.append(f"    getobjectxy({lid}, CURRENT_POSITION, VAR_0x8007, VAR_0x8008)")
        for (px, py) in plates:
            s += [f"    if (var(VAR_0x8007) == {px} && var(VAR_0x8008) == {py}) {{", "        addvar(VAR_TEMP_9, 1)", "    }"]
    s += ["    if (var(VAR_TEMP_9) == 2) {", "        lockall", f"        setflag({temp_flag})",
          f"        setmetatile({x0 + 5}, {y0 + 3}, {cave}, FALSE)", "        special(DrawWholeMapView)",
          "        playse(SE_DOOR)",
          '        msgbox(format("Both plates sink. Bronze clanks deep in the wall, and the grate swings up."), MSGBOX_DEFAULT)',
          "        releaseall", "    }", "}", "", f"script {prefix}Lever{tag} {{", "    lockall",
          '    msgbox(format("A bronze lever with a double axe for a handle: Daedalus\'s reset.\\pPull it?"), MSGBOX_YESNO)',
          "    if (var(VAR_RESULT) == YES) {", "        closemessage", "        playse(SE_CLICK)",
          f"        warpsilent({map_id(m)}, {x0 + 2}, {y0 + 1})", "        waitstate", "    }", "    releaseall", "}"]
    m.extra_scripts = getattr(m, "extra_scripts", []) + s
    m.notes[(x0 - 1, y0 + 2)] = "seal"
    log(m, f"Girdle of Herakles: floor seal {tag} at ({x0},{y0}), two drums onto two plates — {why}")


def write_extras(m, root):
    p = root / "data/maps" / m.name / "scripts.pory"
    text = p.read_text()
    block = "\n".join(getattr(m, "extra_scripts", []))
    if BEGIN not in text:
        text = text.rstrip("\n") + f"\n\n{BEGIN}\n{END}\n"
    a, b = text.index(BEGIN) + len(BEGIN), text.index(END)
    p.write_text(text[:a] + "\n" + block + "\n" + text[b:])


def report(m, root):
    """The ring's extras, for its brief (design/maps/<Map>.md)."""
    lines = [f"- {x}" for x in getattr(m, "relic_log", [])]
    lines += [f"- the lost, {t} at {xy}: “{txt}”" + (f" ({it})" if it else "") for t, xy, txt, it in getattr(m, "lost_log", [])]
    out = root / "build" / f"{m.name}_extras.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines) + "\n")
    return lines
