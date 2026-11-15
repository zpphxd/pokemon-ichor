"""Search Galatea's Gallery for safe routes (gallery_sim's model): the shortest
route from a room's door to its goal on which no statue ever touches the player,
and whether the plain shortest walk (statues ignored) gets the player touched."""
from __future__ import annotations

from collections import deque

from gallery_sim import DIRS, Sim


def state_key(sim, px, py):
    return (px, py) + tuple((s.x, s.y) for s in sim.statues)


def load(sim, key):
    for i, s in enumerate(sim.statues):
        s.x, s.y = key[2 + i]


def safe_route(sim, start, goals, limit=200000):
    """Shortest safe route (a string of N/E/S/W) from start to any goal tile, or None."""
    sim.reset()
    k0 = state_key(sim, *start)
    prev = {k0: None}
    q = deque([k0])
    while q and len(prev) < limit:
        k = q.popleft()
        if (k[0], k[1]) in goals:
            route = ""
            while prev[k]:
                k, d = prev[k]
                route = d + route
            sim.reset()
            return route
        for d in "NESW":
            load(sim, k)
            nx, ny, touched, _ = sim.step_player(d, k[0], k[1])
            if (nx, ny) == (k[0], k[1]) or touched:
                continue
            nk = state_key(sim, nx, ny)
            if nk not in prev:
                prev[nk] = (k, d)
                q.append(nk)
    sim.reset()
    return None


CLOCKWISE = {"N": "E", "E": "S", "S": "W", "W": "N"}


def safe_route_turning(sim, start, goals, turnable, limit=400000):
    """As safe_route, with the turnable mirrors (names in `turnable`) in the state:
    standing next to one, 'tNAME' turns it 90 degrees clockwise (no step, so no
    statue moves). Returns the action list, or None."""
    sim.reset()
    names = list(turnable)
    home = {n: sim.mirrors[n][2] for n in names}

    def key(px, py):
        return (px, py) + tuple((s.x, s.y) for s in sim.statues) + tuple(sim.mirrors[n][2] for n in names)

    def load_all(k):
        load(sim, k)
        for i, n in enumerate(names):
            sim.mirrors[n][2] = k[2 + len(sim.statues) + i]

    k0 = key(*start)
    prev = {k0: None}
    q = deque([k0])
    found = None
    while q and len(prev) < limit:
        k = q.popleft()
        if (k[0], k[1]) in goals:
            found = k
            break
        for d in "NESW":
            load_all(k)
            nx, ny, touched, _ = sim.step_player(d, k[0], k[1])
            if (nx, ny) == (k[0], k[1]) or touched:
                continue
            nk = key(nx, ny)
            if nk not in prev:
                prev[nk] = (k, d)
                q.append(nk)
        for n in names:
            load_all(k)
            mx, my, f = sim.mirrors[n]
            if abs(mx - k[0]) + abs(my - k[1]) != 1:
                continue
            sim.mirrors[n][2] = CLOCKWISE[f]
            nk = key(k[0], k[1])
            if nk not in prev:
                prev[nk] = (k, "t" + n)
                q.append(nk)
    for n in names:
        sim.mirrors[n][2] = home[n]
    sim.reset()
    if not found:
        return None
    route, k = [], found
    while prev[k]:
        k, a = prev[k]
        route.insert(0, a)
    return route


def plain_route(sim, start, goal):
    """The shortest walk with the statues standing on their plinths as obstacles."""
    sim.reset()
    q, prev = deque([start]), {start: None}
    while q:
        p = q.popleft()
        if p == goal:
            break
        for d, (dx, dy) in DIRS.items():
            n = (p[0] + dx, p[1] + dy)
            if n not in prev and sim.walkable(*n) and not sim.object_at(*n):
                prev[n] = (p, d)
                q.append(n)
    route, p = "", goal
    while prev.get(p):
        p, d = prev[p]
        route = d + route
    return route
