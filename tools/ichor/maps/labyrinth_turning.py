"""The Turning (design/LABYRINTH.md §7): the house's shifting walls, per ring.

After Scene J (VAR_ICHOR_KNOSSA == 17) every ring the escape crosses redraws a
"turned" layout in its ON_LOAD, from the list this module plans:

- **Sealed halls.** Wall plugs across the mouths of the ring's dead-end pockets:
  a corridor cross-section, two cells deep, behind which nothing lies that any
  route needs (no warp, no trigger). A pocket only ever joins the rest of the
  ring through its mouth, so sealing it can't cut any way through the ring,
  whatever the state of its gates, dials or walls.
- **Breakthroughs.** Two or three plugs across the escape's own way (the
  shortest walk from the stair you come up by to the stair up). Each is ringed
  with triggers; the first step beside it plays Asterion smashing it open
  ("He'll clear the rest"), and VAR_TEMP_D/E/F remember it until you leave.

Ichor_DrawThread runs after the turned layout, and committed thread forces any
tile it crosses back to floor (src/ichor_labyrinth.c), so the thread holds the
house open. The plugs are autotiled walls: the ring is laid again with the plug
cells as wall, and every metatile that changes becomes a setmetatile.

  import labyrinth_turning as TURN
  TURN.lmap(m, start, end)        # the upper rings, before m.build()
  TURN.heart(m, start, end)       # the heart's rings, before m.build()
"""
from __future__ import annotations

import random
import re
from collections import deque

from kythera_maps import ROOT

BREAK_VARS = ["VAR_TEMP_D", "VAR_TEMP_E", "VAR_TEMP_F"]
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def _scripted_cells(m):
    """Every cell any script of this map setmetatiles: it may open at run time."""
    cells = set()
    p = ROOT / "data/maps" / m.name / "scripts.pory"
    text = (p.read_text() if p.exists() else "") + "\n".join(getattr(m, "gen", []))
    text = re.sub(r"script \w+_EventScript_Turning\w* \{.*?\n\}", "", text, flags=re.S)   # our own, last run
    for x, y in re.findall(r"setmetatile\((\d+),\s*(\d+),", text):
        cells.add((int(x), int(y)))
    return cells


def _events(m):
    ev = set()
    for coll in (m.objects, m.warps, m.coords, m.bgs):
        for e in coll:
            ev.add((int(e["x"]), int(e["y"])))
    return ev


class Plan:
    """The planning half, on a terrain grid: walk[y][x] (walkable, generously:
    water and anything that may open counts), wall[y][x] (plain wall terrain a
    plug can be), plain[y][x] (a plain floor cell a plug may cover)."""

    def __init__(self, w, h, walk, wall, plain, important, seed):
        self.w, self.h, self.walk, self.wall, self.plain = w, h, walk, wall, plain
        self.important = important
        self.rng = random.Random(seed)
        self.firm = lambda x, y: True
        self.spans = (1, 2)

    def ok(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def W(self, x, y):
        return self.ok(x, y) and self.walk[y][x]

    def S(self, x, y):
        return (not self.ok(x, y)) or self.wall[y][x]

    def blocks(self):
        """Corridor cross-sections two cells deep: (cells, sides) where `sides`
        are the walkable cells either end of the plug along the corridor."""
        out = []
        for y in range(self.h):
            for x in range(self.w):
                for span in self.spans:
                    # a north-south corridor `span` wide: plug rows y, y+1
                    cells = [(x + i, y + j) for i in range(span) for j in (0, 1)]
                    if all(self.ok(*c) and self.plain[c[1]][c[0]] for c in cells) \
                            and all(self.S(x - 1, y + j) and self.S(x + span, y + j) for j in (0, 1)) \
                            and all(self.W(x + i, y - 1) and self.W(x + i, y + 2) for i in range(span)):
                        out.append((cells, [(x + i, y - 1) for i in range(span)] + [(x + i, y + 2) for i in range(span)]))
                    # an east-west corridor `span` tall: plug columns x, x+1
                    cells = [(x + i, y + j) for i in (0, 1) for j in range(span)]
                    if all(self.ok(*c) and self.plain[c[1]][c[0]] for c in cells) \
                            and all(self.S(x + i, y - 1) and self.S(x + i, y + span) for i in (0, 1)) \
                            and all(self.W(x - 1, y + j) and self.W(x + 2, y + j) for j in range(span)):
                        out.append((cells, [(x - 1, y + j) for j in range(span)] + [(x + 2, y + j) for j in range(span)]))
        return out

    def components(self, blocked):
        seen, comps = {}, []
        for y in range(self.h):
            for x in range(self.w):
                if not self.walk[y][x] or (x, y) in blocked or (x, y) in seen:
                    continue
                q, comp = deque([(x, y)]), [(x, y)]
                seen[(x, y)] = len(comps)
                while q:
                    cx, cy = q.popleft()
                    for dx, dy in DIRS:
                        n = (cx + dx, cy + dy)
                        if self.W(*n) and n not in blocked and n not in seen:
                            seen[n] = len(comps)
                            comp.append(n)
                            q.append(n)
                comps.append(comp)
        return comps, seen

    def path(self, start, end, blocked=()):
        prev = {start: None}
        q = deque([start])
        while q:
            c = q.popleft()
            if c == end:
                break
            for dx, dy in DIRS:
                n = (c[0] + dx, c[1] + dy)
                if self.W(*n) and n not in blocked and n not in prev:
                    prev[n] = c
                    q.append(n)
        if end not in prev:
            return None
        out, c = [], end
        while c is not None:
            out.append(c)
            c = prev[c]
        return out[::-1]

    def choose(self, start, end, n_breaks=2, max_plugs=12):
        blocks = self.blocks()
        base, _ = self.components(set())
        # pockets: a block whose removal leaves a piece with nothing important in it
        pockets = []
        for cells, sides in blocks:
            comps, idx = self.components(set(cells))
            if len(comps) <= len(base):
                continue
            dead = [c for c in comps if not (set(c) & self.important) and len(c) >= 2]
            if not dead:
                continue
            inside = set().union(*map(set, dead))
            pockets.append((len(inside), cells, inside))
        pockets.sort(key=lambda p: -p[0])
        plugs, sealed, near = [], set(), set()
        for size, cells, inside in pockets:
            if len(plugs) >= max_plugs:
                break
            if any(c in sealed or c in near for c in cells):
                continue
            plugs.append(cells)
            sealed |= inside | set(cells)
            near |= {(x + dx, y + dy) for (x, y) in cells for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2)}
        # breakthroughs on the escape's own way
        route = self.path(start, end, sealed)
        breaks = []
        if route:
            pos = {c: i for i, c in enumerate(route)}
            cands = []
            for cells, sides in blocks:
                hit = [pos[c] for c in cells if c in pos]
                if not hit or any(c in sealed or c in near for c in cells):
                    continue
                f = min(hit) / len(route)
                if 0.1 <= f <= 0.9 and all(self.W(*s) and s not in sealed and self.firm(*s) for s in sides):
                    cands.append((f, cells, sides))
            self.rng.shuffle(cands)
            cands.sort(key=lambda c: c[0])
            for f, cells, sides in cands:
                if len(breaks) >= n_breaks:
                    break
                if any(abs(f - g) < 0.2 for g, _, _ in breaks):
                    continue
                if any(c in near for c in cells):
                    continue
                breaks.append((f, cells, sides))
                near |= {(x + dx, y + dy) for (x, y) in cells for dx in range(-3, 4) for dy in range(-3, 4)}
        return plugs, [(cells, sides) for _, cells, sides in sorted(breaks, key=lambda b: b[0])], route


# --------------------------------------------------------------------------
# The script half
# --------------------------------------------------------------------------

def _lines(cells):
    return [f"    setmetatile({x}, {y}, 0x{t:03X}, {'TRUE' if s else 'FALSE'})" for (x, y, t, s) in cells]


def scripts(name, closed, reopen):
    """ON_LOAD lines and the scripts: `closed` the turned layout's cells,
    `reopen[i]` the cells breakthrough i puts back."""
    on_load = ["if (var(VAR_ICHOR_KNOSSA) == 17) {", f"    call({name}_EventScript_TurningWalls)", "} else {"]
    on_load += [f"    setvar({v}, 1)" for v in BREAK_VARS[:len(reopen)]] + ["}"]
    s = ["", "// The Turning (LABYRINTH §7): the turned layout, from tools/ichor/maps/labyrinth_turning.py.",
         f"script {name}_EventScript_TurningWalls {{"]
    s += _lines(closed)
    for i, cells in enumerate(reopen):
        s += [f"    if (var({BREAK_VARS[i]}) != 0) {{"] + ["    " + l for l in _lines(cells)] + ["    }"]
    s.append("}")
    for i, cells in enumerate(reopen):
        v = BREAK_VARS[i]
        s += ["", f"script {name}_EventScript_TurningBreak{i} {{", "    lockall", f"    setvar({v}, 1)",
              "    playse(SE_M_EARTHQUAKE)",
              '    msgbox(format("The wall ahead grinds shut across the passage."), MSGBOX_DEFAULT)',
              "    closemessage",
              "    setvar(VAR_0x8004, 2)", "    setvar(VAR_0x8005, 2)", "    setvar(VAR_0x8006, 10)",
              "    setvar(VAR_0x8007, 3)", "    special(ShakeCamera)", "    waitstate",
              "    playse(SE_M_MEGA_KICK)"]
        s += _lines(cells)
        s += ["    special(Ichor_DrawThread)", "    special(DrawWholeMapView)",
              '    msgbox(format("Then it bursts. Horns, a tail, a cloud of dust, and Asterion is gone ahead.\\p'
              'He\'s clearing the way."), MSGBOX_DEFAULT)',
              "    closemessage", "    releaseall", "}"]
    return on_load, s


def _diff(a_mid, a_solid, b_mid, b_solid, actual):
    """Cells where layout b differs from a, or None if one of them carries a
    piece (the actual map differs from a there)."""
    out = []
    h, w = a_mid.shape
    for y in range(h):
        for x in range(w):
            if int(a_mid[y, x]) != int(b_mid[y, x]) or bool(a_solid[y, x]) != bool(b_solid[y, x]):
                if int(actual[y, x]) != int(a_mid[y, x]):
                    return None
                out.append((x, y, int(b_mid[y, x]), bool(b_solid[y, x])))
    return out


def _apply(m, plan, plugs, breaks, relay, start, end, firm):
    """Lay the turned grids, drop any plug that would disturb a piece, and wire
    the scripts and triggers into map m."""
    base_mid, base_solid = relay([])
    kept, kept_breaks = [], []
    for cells in plugs:
        a = _diff(base_mid, base_solid, *relay([cells]), m.mid)
        if a:
            kept.append(cells)
    for cells, sides in breaks:
        a = _diff(base_mid, base_solid, *relay([cells]), m.mid)
        taken = {(int(c["x"]), int(c["y"])) for c in m.coords}
        if a and not any(s in taken or not firm(*s) for s in sides):
            kept_breaks.append((cells, sides))
    allp = kept + [c for c, _ in kept_breaks]
    t_mid, t_solid = relay(allp)
    closed = _diff(base_mid, base_solid, t_mid, t_solid, m.mid) or []
    reopen = []
    for i, (cells, sides) in enumerate(kept_breaks):
        rest = kept + [c for j, (c, _) in enumerate(kept_breaks) if j != i]
        r_mid, r_solid = relay(rest)
        reopen.append(_diff(t_mid, t_solid, r_mid, r_solid, t_mid) or [])
        for (x, y) in sides:
            m.trigger(x, y, f"{m.name}_EventScript_TurningBreak{i}", var=BREAK_VARS[i], value=0)
    on_load, s = scripts(m.name, closed, reopen)
    m.turning_log = {"plugs": len(kept), "breaks": len(kept_breaks), "cells": len(closed),
                     "route": len(plan.path(start, end) or [])}
    print(f"{m.name} TURNING: {len(kept)} sealed halls, {len(kept_breaks)} breakthroughs, "
          f"{len(closed)} tiles turn")
    return on_load, s


def _important(m, start, end):
    imp = {(int(w["x"]), int(w["y"])) for w in m.warps} | {(int(c["x"]), int(c["y"])) for c in m.coords}
    return imp | {start, end}


def lmap(m, start, end, seed=7, n_breaks=2, max_plugs=12):
    """Ring I-IV (labyrinth_lib.LMap): call after the events are placed, before m.build()."""
    from labyrinth_lib import LMap, FLOORS
    ev, scripted = _events(m), _scripted_cells(m)
    keep = set(m.forced_open) | set(m.stops) | {(x, y) for x, y, _ in m.anchors} | scripted
    warps = {(int(w["x"]), int(w["y"])) for w in m.warps}
    g = m.g
    walk = [[(g[y][x] in FLOORS + "~") or (x, y) in warps or (x, y) in scripted or (x, y) in m.forced_open
             or not m.solid[y, x] for x in range(m.w)] for y in range(m.h)]
    wall = [[g[y][x] in "#%" and (x, y) not in scripted and (x, y) not in warps for x in range(m.w)] for y in range(m.h)]
    near_ev = {(x + dx, y + dy) for (x, y) in ev | keep for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    base = LMap(m.name, m.w, m.h, dict(m.header))
    base.g = [r[:] for r in g]
    base.lay()
    plain = [[g[y][x] in ".,;" and (x, y) not in near_ev and int(m.mid[y, x]) == int(base.mid[y, x])
              and not m.solid[y, x] for x in range(m.w)] for y in range(m.h)]
    plan = Plan(m.w, m.h, walk, wall, plain, _important(m, start, end), seed)
    taken = {(int(c["x"]), int(c["y"])) for c in m.coords}
    plan.firm = lambda x, y: g[y][x] in ".,;-|A" and not m.solid[y, x] and (x, y) not in taken
    plugs, breaks, route = plan.choose(start, end, n_breaks, max_plugs)

    def relay(sets):
        mm = LMap(m.name, m.w, m.h, dict(m.header))
        mm.g = [r[:] for r in g]
        for cells in sets:
            for (x, y) in cells:
                nb = [g[y + dy][x + dx] for dx, dy in DIRS if 0 <= x + dx < m.w and 0 <= y + dy < m.h]
                mm.g[y][x] = "%" if nb.count("%") > nb.count("#") else "#"
        mm.lay()
        return mm.mid, mm.solid

    on_load, s = _apply(m, plan, plugs, breaks, relay, start, end,
                        lambda x, y: g[y][x] in ".,;-|A" and not m.solid[y, x])
    m.register_extra = on_load
    m.extra_scripts = getattr(m, "extra_scripts", []) + s


def heart(m, start, end, seed=7, n_breaks=2, max_plugs=12):
    """Rings V-VII (heart_lib.HeartMap): call after the events are placed, before m.build()."""
    import heart_lib as H
    ev, scripted = _events(m), _scripted_cells(m)
    keep = {(x, y) for x, y, _ in m.anchors} | set(m.deco) | set(m.nothread) | scripted | set(m.forced_open)
    warps = {(int(w["x"]), int(w["y"])) for w in m.warps}
    cracks = {(x, y) for x, y, _ in m.cracks}
    T = m.t
    walk = [[(T[y][x] in H.FLOORS + "~") or (x, y) in warps or (x, y) in scripted or (x, y) in cracks
             for x in range(m.w)] for y in range(m.h)]
    wall = [[T[y][x] in "RM" and (x, y) not in scripted and (x, y) not in cracks and (x, y) not in warps
             for x in range(m.w)] for y in range(m.h)]
    near_ev = {(x + dx, y + dy) for (x, y) in ev | keep for dx in (-1, 0, 1) for dy in (-1, 0, 1)}

    def relay(sets):
        mm = H.HeartMap(m.name, m.ts, m.w, m.h)
        mm.t = [r[:] for r in T]
        mm.deco = dict(m.deco)
        for cells in sets:
            for (x, y) in cells:
                nb = [T[y + dy][x + dx] for dx, dy in DIRS if 0 <= x + dx < m.w and 0 <= y + dy < m.h]
                mm.t[y][x] = "M" if nb.count("M") > nb.count("R") else "R"
        mm.lay()
        return mm.mid, mm.solid

    base_mid, _ = relay([])
    plain = [[T[y][x] in ".," and (x, y) not in near_ev and int(m.mid[y, x]) == int(base_mid[y, x])
              and not m.solid[y, x] for x in range(m.w)] for y in range(m.h)]
    plan = Plan(m.w, m.h, walk, wall, plain, _important(m, start, end), seed)
    taken = {(int(c["x"]), int(c["y"])) for c in m.coords}
    plan.firm = lambda x, y: T[y][x] in ".,omx" and not m.solid[y, x] and (x, y) not in taken
    plan.spans = (1, 2, 3)      # the heart's cave passages run wider
    plugs, breaks, route = plan.choose(start, end, n_breaks, max_plugs)
    on_load, s = _apply(m, plan, plugs, breaks, relay, start, end,
                        lambda x, y: T[y][x] in ".,omx" and not m.solid[y, x])
    m.gen += on_load
    m.turning_scripts = s
