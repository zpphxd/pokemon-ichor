"""A model of the marble statues and bronze mirrors (engine need E8,
src/ichor_statue.c, design/phase4/ENGINE_ACT3.md), for designing Galatea's
Gallery and checking it in kythera_temple.py without the ROM.

It follows the engine step for step: on each step the player takes, every live
statue the player can't see steps one tile toward them (the longer axis first,
east or west on a tie, the other axis if that tile is blocked, never outside
its movement range), then turns to face them; one that ends next to the player
touches them. The player sees along the line of tiles straight ahead from the
tile next to them: statues don't block it, a mirror's face turns it the way the
mirror faces, a mirror's back, anyone else or a wall stops it, at most 32 tiles
and 4 mirrors.
"""
from __future__ import annotations

DIRS = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}


class Statue:
    def __init__(self, name, x, y, rng=None, live=True):
        self.name, self.home, self.x, self.y = name, (x, y), x, y
        self.rng = rng                  # (rx, ry), 0 = no limit on that axis, as the engine
        self.live = live


class Sim:
    def __init__(self, walkable, statues, mirrors, people=()):
        """walkable(x, y) -> bool; mirrors {name: [x, y, facing]}; people [(x, y)]."""
        self.walkable = walkable
        self.statues = statues
        self.mirrors = mirrors
        self.people = set(people)
        # Tiles where a trainer sees the player: the engine checks trainers' sight
        # before the statues, and a trainer who spots you skips that step's statues.
        # A trainer only does it once (then they're beaten).
        self.sight = set()

    def object_at(self, x, y):
        for s in self.statues:
            if (s.x, s.y) == (x, y):
                return ("statue", s)
        for n, (mx, my, f) in self.mirrors.items():
            if (mx, my) == (x, y):
                return ("mirror", f)
        if (x, y) in self.people:
            return ("person", None)
        return None

    def watched(self, px, py, facing):
        seen, d, x, y, mirrors = set(), facing, px, py, 0
        for _ in range(32):
            dx, dy = DIRS[d]
            x, y = x + dx, y + dy
            o = self.object_at(x, y)
            if o:
                if o[0] == "statue":
                    seen.add(o[1].name)
                    continue
                if o[0] == "mirror":
                    mirrors += 1
                    if mirrors > 4 or o[1] == d:
                        break
                    d = o[1]
                    continue
                break
            if not self.walkable(x, y):
                break
        return seen

    def blocked(self, x, y, px, py, me):
        if not self.walkable(x, y) or (x, y) == (px, py):
            return True
        o = self.object_at(x, y)
        return o is not None and not (o[0] == "statue" and o[1] is me)

    def toward(self, s, px, py, other):
        dx, dy = px - s.x, py - s.y
        across = (abs(dx) >= abs(dy)) != other
        if across:
            return None if dx == 0 else ("E" if dx > 0 else "W")
        return None if dy == 0 else ("S" if dy > 0 else "N")

    def step_player(self, d, px, py):
        """Move the player one tile (d), run the statues, and return
        (new x, new y, touched statue name or None, moved names)."""
        dx, dy = DIRS[d]
        nx, ny = px + dx, py + dy
        if not self.walkable(nx, ny) or self.object_at(nx, ny):
            return px, py, None, []          # a bump: no step, nothing moves
        px, py = nx, ny
        if (px, py) in self.sight:
            self.sight.discard((px, py))
            return px, py, None, []
        seen = self.watched(px, py, d)
        moved = []
        for s in self.statues:
            if not s.live or s.name in seen:
                continue
            if abs(s.x - px) + abs(s.y - py) != 1:
                for attempt in (False, True):
                    t = self.toward(s, px, py, attempt)
                    if t is None:
                        continue
                    tx, ty = s.x + DIRS[t][0], s.y + DIRS[t][1]
                    if self.blocked(tx, ty, px, py, s):
                        continue
                    if s.rng:
                        rx, ry = s.rng
                        if (rx and abs(tx - s.home[0]) > rx) or (ry and abs(ty - s.home[1]) > ry):
                            continue
                    s.x, s.y = tx, ty
                    moved.append(s.name)
                    break
            if abs(s.x - px) + abs(s.y - py) == 1:
                return px, py, s.name, moved
        return px, py, None, moved

    def walk(self, start, route, log=False):
        """Walk a route ('NNEE...'); returns (touched name or None, step index, end)."""
        px, py = start
        for i, d in enumerate(route):
            nx, ny, touched, moved = self.step_player(d, px, py)
            if (nx, ny) == (px, py):
                return ("bump", i, (px, py))
            px, py = nx, ny
            if log:
                print(i, d, (px, py), "moved", moved, {s.name: (s.x, s.y) for s in self.statues})
            if touched:
                return (touched, i, (px, py))
        return (None, len(route), (px, py))

    def play(self, start, actions, log=False):
        """As walk, with 'tNAME' actions that turn mirror NAME 90 degrees clockwise."""
        cw = {"N": "E", "E": "S", "S": "W", "W": "N"}
        px, py = start
        for i, a in enumerate(actions):
            if a.startswith("t"):
                self.mirrors[a[1:]][2] = cw[self.mirrors[a[1:]][2]]
                continue
            nx, ny, touched, moved = self.step_player(a, px, py)
            if (nx, ny) == (px, py):
                return ("bump", i, (px, py))
            px, py = nx, ny
            if log:
                print(i, a, (px, py), "moved", moved, {s.name: (s.x, s.y) for s in self.statues})
            if touched:
                return (touched, i, (px, py))
        return (None, len(actions), (px, py))

    def reset(self):
        for s in self.statues:
            s.x, s.y = s.home
