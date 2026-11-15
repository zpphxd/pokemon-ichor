#!/usr/bin/env python3
"""Audit maps against the route standard: MAP_DESIGN.md §8, "The route standard, in numbers".

  tools/ichor/map_audit.py KallisteRoute1 AktiTown     maps, or name prefixes
  tools/ichor/map_audit.py Route6 Eleutherai           (a prefix takes every map that starts with it)
  tools/ichor/map_audit.py --all-ichor                 every Ichor map in map_groups.json
  tools/ichor/map_audit.py --all-ichor --warn-only     report, but exit 0
  tools/ichor/map_audit.py --ref BRANCH --all-ichor    audit another branch, read with git archive
  tools/ichor/map_audit.py --root DIR ...              audit another tree laid out like this repo
  tools/ichor/map_audit.py --markdown ...              tables for design/MAP_AUDIT.md
  tools/ichor/map_audit.py --kinds route,town ...      report only these classes
  tools/ichor/map_audit.py --benchmark                 Emerald's numbers (MAP_DESIGN.md's Appendix A),
                                                       from upstream's merge-base

Each map is classed as a route, town, interior or dungeon: by an "ichor_kind"
key in its map.json if it has one, otherwise by its map type (see classify()).
It then gets its numbers and one line per shortfall:

  FAIL   misses a hard minimum of §8 (exit 1, unless --warn-only)
  WARN   misses a soft one, or a heuristic thinks something is off: look at it
  NOTE   encouraged, not required

It also runs the slice audit's structural checks (tools/ichor/mapdata.py): a
broken WARP or EDGE fails, REACH, MIXED and ONSOLID warn.

Python 3 stdlib only. A full --all-ichor run takes a few seconds.
"""
import argparse
import hashlib
import re
import statistics
import subprocess
import sys
import tarfile
import tempfile
from collections import defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mapdata import (GRASS, OTHER_LAND_ENCOUNTER, REPO, SCREEN_H, SCREEN_W, TIMES, UPSTREAM_PREFIXES,  # noqa: E402
                     WATER, Repo, Walker, bfs, entries, is_berry_tree, is_item_ball, is_obstacle, is_trainer,
                     reverse, structural_checks)

UPSTREAM_BASE = "79dd436920845ebc145577649de624f65298c209"  # pokeemerald-expansion 1.17.2, before the Hoenn cut

# ---------------------------------------------------------------------------
# The standard (MAP_DESIGN.md §8). Keep these numbers and §8's tables in step.
# ---------------------------------------------------------------------------

# A screen is 15x10 cells of map area. Counts "per screen" scale with the map: the
# minimum is the per-screen rate times the map's screens, rounded, or the floor if higher.
LAND_ROUTE = {  # per band, hard
    "grass_per_screen": {"early": 15, "middle": 15, "late": 15},
    "forced_grass": {"early": 2, "middle": 8, "late": 8},       # grass cells no walker can avoid
    "trainers_per_screen": {"early": 0.5, "middle": 0.6, "late": 0.9},
    "trainers_floor": {"early": 3, "middle": 6, "late": 8},
    "items_per_screen": {"early": 0.2, "middle": 0.2, "late": 0.3},  # visible item balls
    "items_floor": {"early": 2, "middle": 3, "late": 5},
    "hidden": {"early": 2, "middle": 3, "late": 4},
    "land_species": {"early": 4, "middle": 5, "late": 7},       # distinct species in each land table
}
SEA_ROUTE = {"trainers_per_screen": 0.35, "trainers_floor": 5, "items": 2, "hidden": 2}  # hard
SURF_SPECIES, FISHING_SPECIES = 3, 4  # per table, any map with them
WATER_TABLE_CELLS = 12    # reachable water from this many cells up needs surf and fishing tables
LEVEL_BAND_MAX = 5        # BALANCE.md: a route's level band is never wider than 5
SIGN_REACH = 15           # a sign within a screen's width of an end is that end's sign
TOWN = {"hidden": 2, "items": 1}
DUNGEON = {"items_per_floor": 2, "hidden": 2, "trainers": 3, "trainers_one_floor": 1, "land_species": 4,
           "rest_floors": 3}  # a dungeon of rest_floors+ floors needs a midpoint rest
DEADEND_CELLS = 7         # a cul-de-sac of this many cells or more...
DEADEND_MOUTH = 3         # ...entered through at most this many cells...
DEADEND_DEPTH = 3         # ...and at least this deep is a dead end, and must hold something
SEA_WATER_SHARE = 0.5     # a route whose open ground is mostly water is a sea route

# Where each place sits on BALANCE.md's curve (the stage's name as BALANCE.md bolds it), and its band.
# Routes go by number (AETHOS_MAP.md's story order); other places by name prefix. Add places as they're built.
STAGES = [  # (stage, band, route numbers, place prefixes)
    ("Kalliste", "early", (1,), ("Elaia", "Kalliste", "Akti")),
    ("Emporion", "early", (2, 3), ("TriremeEuploia", "Aegina", "Emporion")),
    ("Eleusa", "early", (4, 5), ("HecatesHollow", "Eleusa")),
    ("Thyrsa", "middle", (6, 7), ("MtKithairon", "Kithairon", "Eleutherai", "Thyrsa", "Kronia")),
    ("Arkadia", "middle", (8, 9, 10, 11, 12),
     ("Lebadeia", "Trophonios", "Kopais", "Kirrha", "GulfFerry", "Aigion", "StyxFalls", "Arkadia",
      "PoolOfMnemosyne")),
    ("Astyra", "middle", (13, 14, 15, 16, 17, 18),
     ("Nemea", "Daphni", "Astyra", "Marathon", "CapeSounion", "Sounion")),
    ("Kaldera", "middle", (19, 20, 21), ("Kaldera", "Paros", "Delos", "Skyros", "Lemnos", "Samothrake", "Ikaria",
                                         "Samos", "Chios", "Lesbos")),
    ("Kythera", "late", (22,), ("Melos", "Kythera")),
    ("Knossa", "late", (23,), ("Knossa", "Amnisos", "Labyrinth")),
    ("Lakonia", "late", (24, 25, 26, 27), ("Gytheion", "Lakonia", "Stymphalia")),
    ("Delphoi", "late", (28,), ("Delphoi",)),
    ("Ascent", "late", (29, 30), ("Thermopylai", "Tempe", "Ascent", "Olympus", "Pantheon")),
    ("post-game", "late", (31, 32, 33, 34), ("Tainaron", "Olympia", "Atlantis", "Rhodos", "Ithaka", "Kerkyra")),
]


def stage_of(name):
    m = re.match(r"Route(\d+)(?!\d)", name)
    for stage, band, routes, prefixes in STAGES:
        if (m and int(m.group(1)) in routes) or (not m and name.startswith(prefixes)):
            return stage, band
    return None, "early"


def balance_bands(root):
    """BALANCE.md's wild level range per stage: {first bold words: (lo, hi)}."""
    p = Path(root) / "design/BALANCE.md"
    if not p.exists():
        p = REPO / "design/BALANCE.md"
    out = {}
    for line in p.read_text().splitlines():
        m = re.match(r"\|\s*\*\*([^*]+)\*\*[^|]*\|\s*(\d+)\s*[–-]\s*(\d+)\s*\|", line)
        if m:
            out[m.group(1).strip()] = (int(m.group(2)), int(m.group(3)))
    return out


def wild_range(bands, stage):
    for key, rng in bands.items():
        if stage and stage.lower() in key.lower():
            return rng
    return None


# ---------------------------------------------------------------------------
# Classing and measuring a map
# ---------------------------------------------------------------------------

def classify(repo, name):
    """route, town, interior or dungeon.

    An "ichor_kind" key in map.json wins. Otherwise: a ship's deck or hold is an
    interior; MAP_TYPE_ROUTE and MAP_TYPE_OCEAN_ROUTE are routes; TOWN and CITY
    are towns; UNDERGROUND and UNDERWATER are dungeons; an INDOOR map is a
    dungeon if it has wild encounters (a land table or encounter cells), else an
    interior."""
    j = repo.map_json(name)
    if j.get("ichor_kind"):
        return j["ichor_kind"]
    t = j.get("map_type", "")
    if re.search(r"_(Deck|Hold)", name):
        return "interior"
    if t in ("MAP_TYPE_ROUTE", "MAP_TYPE_OCEAN_ROUTE"):
        return "route"
    if t in ("MAP_TYPE_TOWN", "MAP_TYPE_CITY"):
        return "town"
    if t in ("MAP_TYPE_UNDERGROUND", "MAP_TYPE_UNDERWATER"):
        return "dungeon"
    if t == "MAP_TYPE_INDOOR":
        m = repo.map(name)
        if repo.wild().get(j["id"], {}).get("Morning", {}).get("land_mons"):
            return "dungeon"
        if any(m.behavior(c & 0x3FF) in (OTHER_LAND_ENCOUNTER | GRASS) for c in m.cells):
            return "dungeon"
    return "interior"


def dungeon_group(name):
    """A dungeon's floors share a name up to the floor: EleusaSanctum_B1F -> EleusaSanctum."""
    return re.sub(r"_(B?\d+F|\d+R|Entrance|Room\d*|Top|End|Summit|Back|Inner\w*|Outer\w*)(_.*)?$", "", name)


HEAL = re.compile(r"HealPlayerParty|PartyHeal")


class Measure:
    """Everything the standard looks at, for one map."""

    def __init__(self, repo, name):
        self.repo, self.name = repo, name
        m = self.m = repo.map(name)
        self.kind = classify(repo, name)
        self.stage, self.band = stage_of(name)
        self.cells = m.w * m.h
        self.screens = self.cells / (SCREEN_W * SCREEN_H)
        grass = water = other = land = 0
        for y in range(m.h):
            for x in range(m.w):
                mid, col, _ = m.cell(x, y)
                b = m.behavior(mid)
                if b in WATER:
                    water += 1
                elif not col:
                    land += 1
                    grass += b in GRASS
                    other += b in OTHER_LAND_ENCOUNTER
        self.grass, self.water, self.other_enc = grass, water, other
        self._water_major = water > SEA_WATER_SHARE * (water + land)
        objs = m.objects
        self.trainers = [o for o in objs if is_trainer(o)]
        self.items = [o for o in objs if is_item_ball(o)]
        self.berries = [o for o in objs if is_berry_tree(o)]
        self.rocks = [o for o in objs if is_obstacle(o) and "ROCK" in o.get("graphics_id", "")]
        self.obstacles = [o for o in objs if is_obstacle(o)]
        self.npcs = [o for o in objs if o not in self.trainers and o not in self.items and o not in self.berries
                     and not is_obstacle(o)]
        self.hidden = [b for b in m.bgs if b.get("type") == "hidden_item"]
        self.signs = [b for b in m.bgs if b.get("type") == "sign"]
        self.scenes = len(m.coords)
        script = repo.script_text(name)
        self.gifts = len(re.findall(r"\b(giveitem|givemon|giveegg|ScriptGiveMon)\b", script))
        self.trades = len(re.findall(r"InGameTrade", script))
        self.heals = bool(HEAL.search(script))
        self.wild = repo.wild().get(m.json["id"], {})
        # walking: the whole reach (surf and relics), and the first visit's (no surf, no relics)
        full = Walker(m, surf=True, relics=True)
        self.reach_states = full.reach(full.starts([t for _, ts in entries(m) for t in ts]))
        self.reach = {s[:2] for s in self.reach_states}
        self.reach_water = sum(1 for t in self.reach if m.is_water(*t))
        self._forced = self._ends = self._dead = self._sea = None

    @property
    def sea(self):
        """A sea route: an ocean route, or a route whose open ground is mostly
        water and none of whose connected edges a walker can join without surfing."""
        if self.kind != "route":
            return False
        if self.m.json.get("map_type") == "MAP_TYPE_OCEAN_ROUTE":
            return True
        if self._sea is None:
            self._sea = self._water_major and not self._grass_pairs(self.main_exits(False))
        return self._sea

    # -- wild tables --------------------------------------------------------
    def tables(self, area):
        return [t for t in TIMES if area in self.wild.get(t, {})]

    def species(self, area, time):
        mons = self.wild.get(time, {}).get(area) or []
        return len({mon["species"] for mon in mons})

    def levels(self, area):
        lv = [(mon["min_level"], mon["max_level"]) for t in TIMES for mon in self.wild.get(t, {}).get(area) or []]
        return (min(a for a, _ in lv), max(b for _, b in lv)) if lv else None

    # -- the route's ends ---------------------------------------------------
    def main_exits(self, warps=False):
        """The ends a route is walked between: its connected edges, and with
        warps=True its warps to other outdoor maps (a cave mouth, the woods)."""
        m, w = self.m, Walker(self.m)
        out = []
        for c in m.connections:
            tiles = m.edge_tiles(c)
            s = w.starts(tiles)
            if s:
                out.append((f"{c['direction']} ({c['map'].replace('MAP_', '')})", s, tiles))
        if warps:
            for w_ in m.warps:
                dname = self.repo.name_of(w_.get("dest_map"))
                if dname and classify(self.repo, dname) != "interior":
                    tiles = [(w_["x"], w_["y"]), (w_["x"], w_["y"] + 1)]
                    s = w.starts(tiles)
                    if s:
                        out.append((f"warp to {dname}", s, tiles))
        return out

    def forced_grass(self):
        """Fewest grass cells a first-visit walker (no surf, no relics) must cross
        between two ends, taking the highest over the ordered pairs of ends it
        can walk between, so a band crossed one way counts. Pairs of connected
        edges come first; warps to outdoor maps join in only when no two edges
        are joined by land (Route 104, split by Petalburg Woods)."""
        if self._forced is None:
            self._forced = (None, [])
            for use_warps in (False, True):
                pairs = self._grass_pairs(self.main_exits(use_warps))
                if pairs:
                    self._forced = (max(p[0] for p in pairs), pairs)
                    break
        return self._forced

    def _grass_pairs(self, ex):
        if len(ex) < 2:
            return []
        w = Walker(self.m)
        grass = {(x, y) for y in range(self.m.h) for x in range(self.m.w) if self.m.behavior_at(x, y) in GRASS}
        pairs = []
        for i, (la, sa, _) in enumerate(ex):
            cost = {s: (1 if s[:2] in grass else 0) for s in sa}
            dq = deque(sorted(cost, key=cost.get))
            while dq:  # 0-1 breadth-first search: stepping into grass costs 1
                s = dq.popleft()
                for t in w.steps(*s):
                    c = cost[s] + (1 if t[:2] in grass else 0)
                    if c < cost.get(t, 1 << 30):
                        cost[t] = c
                        (dq.append if c > cost[s] else dq.appendleft)(t)
            for j, (lb, sb, _) in enumerate(ex):
                if i != j:
                    got = [cost[s] for s in sb if s in cost]
                    if got:
                        pairs.append((min(got), la, lb))
        return pairs

    def unsigned_ends(self):
        """Connected ends with no sign within SIGN_REACH cells."""
        if self._ends is None:
            self._ends = []
            signs = [(b["x"], b["y"]) for b in self.signs]
            for label, _, tiles in self.main_exits():
                if not any(max(abs(sx - x), abs(sy - y)) <= SIGN_REACH for sx, sy in signs for x, y in tiles
                           if self.m.cell(x, y) and not self.m.cell(x, y)[1]):
                    self._ends.append(label)
        return self._ends

    # -- dead ends ----------------------------------------------------------
    def dead_ends(self):
        """Empty cul-de-sacs: walkable pockets off every shortest path between the
        map's entrances, bigger than DEADEND_CELLS, entered through at most
        DEADEND_MOUTH cells, at least DEADEND_DEPTH deep, with no object, sign,
        hidden item or warp in or beside them. A heuristic."""
        if self._dead is not None:
            return self._dead
        m = self.m
        w = Walker(m, relics=True)
        ex = [s for s in (w.starts(t) for _, t in entries(m)) if s]
        self._dead = []
        if not ex:
            return self._dead
        adj = w.graph([s for ss in ex for s in ss])
        radj = reverse(adj)
        fwd = [bfs(adj, ss) for ss in ex]
        bwd = [bfs(radj, ss) for ss in ex]
        trunk = {s[:2] for ss in ex for s in ss}
        for i in range(len(ex)):
            for j in range(len(ex)):
                if i == j:
                    continue
                dij = min((fwd[i][s] for s in ex[j] if s in fwd[i]), default=None)
                if dij is None:
                    continue
                bj = bwd[j]
                trunk.update(s[:2] for s, d in fwd[i].items() if bj.get(s, -10 ** 9) + d == dij)
        tadj = defaultdict(set)
        for s, nb in adj.items():
            for t in nb:
                if s[:2] != t[:2]:
                    tadj[s[:2]].add(t[:2])
                    tadj[t[:2]].add(s[:2])
        content = ({(o["x"], o["y"]) for o in m.objects} | {(b["x"], b["y"]) for b in m.bgs}
                   | {(x["x"], x["y"]) for x in m.warps})
        off = {s[:2] for s in adj} - trunk
        done = set()
        for t0 in sorted(off):
            if t0 in done:
                continue
            comp, q = {t0}, deque([t0])
            while q:
                t = q.popleft()
                for n in tadj[t]:
                    if n in off and n not in comp:
                        comp.add(n)
                        q.append(n)
            done |= comp
            if len(comp) < DEADEND_CELLS:
                continue
            mouth = [t for t in comp if any(n in trunk for n in tadj[t])]
            if len(mouth) > DEADEND_MOUTH:
                continue
            depth = {t: 1 for t in mouth}
            q = deque(mouth)
            while q:
                t = q.popleft()
                for n in tadj[t]:
                    if n in comp and n not in depth:
                        depth[n] = depth[t] + 1
                        q.append(n)
            deep = max(depth.values(), default=0)
            if deep < DEADEND_DEPTH:
                continue
            near = comp | {(x + dx, y + dy) for x, y in comp for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))}
            if near & content:
                continue
            end = max(depth, key=depth.get)
            self._dead.append((len(comp), deep, end, mouth[0] if mouth else None))
        return self._dead


# ---------------------------------------------------------------------------
# Judging against §8
# ---------------------------------------------------------------------------

def judge(ms, bands, by_name):
    """[(level, message)] for one map. by_name holds every measured map (for houses and dungeon floors)."""
    out = []

    def need(ok, level, msg):
        if not ok:
            out.append((level, msg))

    for kind, msg in structural_checks(ms.m):
        # A warp or connection to nowhere is broken. An open cell facing a wall across
        # a seam is often deliberate (Emerald has 57 on its routes and towns): a warning.
        broken = (kind in ("WARP", "EDGE") and ("isn't in map_groups" in msg or "which has" in msg)) or kind == "TRAP"
        out.append(("FAIL" if broken else "WARN", f"{kind.lower()}: {msg}"))
    if getattr(ms, "twins", None):
        # §2: every interior is unique. Elsewhere a shared layout is a placeholder.
        twins = ", ".join(ms.twins[:3]) + (f" and {len(ms.twins) - 3} more" if len(ms.twins) > 3 else "")
        out.append(("FAIL" if ms.kind == "interior" else "WARN", f"layout: the same cells as {twins}"
                    + (" (every interior is unique)" if ms.kind == "interior" else
                       " (one of them is a placeholder copy)")))

    if ms.kind == "route":
        judge_route(ms, bands, need)
    elif ms.kind == "town":
        judge_town(ms, need, by_name)
    elif ms.kind == "dungeon":
        judge_dungeon(ms, need)
    for size, deep, end, mouth in ms.dead_ends() if ms.kind in ("route", "town", "dungeon") else []:
        out.append(("WARN", f"dead end: {size} cells, {deep} deep, ending at {end}, entered at {mouth}, "
                            "holds nothing"))
    judge_wild(ms, bands, need)
    order = {"FAIL": 0, "WARN": 1, "NOTE": 2}
    return sorted(out, key=lambda r: order[r[0]])


def scaled(rate, floor, screens):
    """A per-screen minimum: the rate times the map's screens, rounded, or the floor if higher."""
    return max(floor, round(rate * screens))


def judge_route(ms, bands, need):
    b, t, it, hid = ms.band, len(ms.trainers), len(ms.items), len(ms.hidden)
    if ms.sea:
        want = scaled(SEA_ROUTE["trainers_per_screen"], SEA_ROUTE["trainers_floor"], ms.screens)
        need(t >= want, "FAIL", f"trainers: {t} < {want} (sea route of {ms.screens:.1f} screens)")
        need(it >= SEA_ROUTE["items"], "FAIL", f"item balls: {it} < {SEA_ROUTE['items']}")
        need(hid >= SEA_ROUTE["hidden"], "FAIL", f"hidden items: {hid} < {SEA_ROUTE['hidden']}")
    else:
        gps, want_g = ms.grass / ms.screens, LAND_ROUTE["grass_per_screen"][b]
        need(gps >= want_g, "FAIL", f"grass: {gps:.0f} cells per screen < {want_g} "
                                    f"({ms.grass} cells in {ms.screens:.1f} screens; {round(want_g * ms.screens)} needed)")
        forced, pairs = ms.forced_grass()
        want_f = LAND_ROUTE["forced_grass"][b]
        if forced is None:
            need(False, "WARN", f"forced grass: can't measure, fewer than two ends a walker can reach each other from "
                                f"({len(ms.main_exits(True))} end(s))")
        else:
            need(forced >= want_f, "FAIL",
                 f"forced grass: the ends can be walked between crossing {forced} grass cell(s) < {want_f} ("
                 + ", ".join(f"{a} to {c}: {g}" for g, a, c in pairs) + ")")
        want = scaled(LAND_ROUTE["trainers_per_screen"][b], LAND_ROUTE["trainers_floor"][b], ms.screens)
        need(t >= want, "FAIL", f"trainers: {t} < {want} ({b} route of {ms.screens:.1f} screens)")
        want = scaled(LAND_ROUTE["items_per_screen"][b], LAND_ROUTE["items_floor"][b], ms.screens)
        need(it >= want, "FAIL", f"item balls: {it} < {want}")
        need(hid >= LAND_ROUTE["hidden"][b], "FAIL", f"hidden items: {hid} < {LAND_ROUTE['hidden'][b]}")
    ends = ms.unsigned_ends()
    need(not ends, "FAIL", f"signs: no sign within {SIGN_REACH} cells of the {', '.join(ends)} end")
    need(ms.scenes or ms.gifts or ms.trades or ms.berries, "WARN",
         "set piece: none found (no scene trigger, gift, trade or berry tree); check there is one")


HAPPENS = re.compile(r"giveitem|givemon|giveegg|ScriptGiveMon|trainerbattle|InGameTrade|HealPlayerParty|PartyHeal|"
                     r"addmoney|NameReceivedPartyMon")
PUBLIC = re.compile(r"Asclepeion|Agora|Temple|Mart|PokemonCenter|Theater|Skene|Hall|Deigma|Akademia|Lab")


def judge_town(ms, need, by_name):
    need(len(ms.hidden) >= TOWN["hidden"], "FAIL", f"hidden items: {len(ms.hidden)} < {TOWN['hidden']}")
    need(len(ms.items) >= TOWN["items"], "FAIL", f"item balls: {len(ms.items)} < {TOWN['items']}")
    repo, seen = ms.repo, set()
    for w in ms.m.warps:
        dname = repo.name_of(w.get("dest_map"))
        if not dname or dname in seen or classify(repo, dname) != "interior":
            continue
        house, people, happens, q = {dname}, 0, 0, deque([dname])
        while q:  # the house and its other floors
            n = q.popleft()
            h = repo.map(n)
            people += sum(1 for o in h.objects if o.get("script") not in (None, "", "0") and not is_item_ball(o))
            happens += len(HAPPENS.findall(repo.script_text(n))) + sum(1 for o in h.objects if is_item_ball(o))
            happens += sum(1 for b in h.bgs if b.get("type") == "hidden_item")
            for w2 in h.warps:
                n2 = repo.name_of(w2.get("dest_map"))
                if n2 and n2 not in house and classify(repo, n2) == "interior":
                    house.add(n2)
                    q.append(n2)
        seen |= house
        need(people, "FAIL", f"every house a home: nobody lives in {dname}")
        need(happens or PUBLIC.search(dname), "WARN",
             f"every house a home: nothing found happening in {dname} (no gift, trade, battle, heal or item)")


def judge_dungeon(ms, need):
    n = len(ms.items) + len(ms.hidden)
    need(n >= DUNGEON["items_per_floor"], "FAIL",
         f"items on this floor: {n} (visible and hidden) < {DUNGEON['items_per_floor']}")


def judge_dungeon_group(group, floors):
    """Whole-dungeon minimums, summed over its floors."""
    out = []
    t, h = sum(len(f.trainers) for f in floors), sum(len(f.hidden) for f in floors)
    want = DUNGEON["trainers"] if len(floors) > 1 else DUNGEON["trainers_one_floor"]
    if t < want:
        out.append(("FAIL", f"trainers in the whole dungeon: {t} < {want}"))
    if h < DUNGEON["hidden"]:
        out.append(("FAIL", f"hidden items in the whole dungeon: {h} < {DUNGEON['hidden']}"))
    if len(floors) >= DUNGEON["rest_floors"] and not any(f.heals for f in floors):
        out.append(("WARN", "midpoint rest: no healer on any floor; check for a spring or a shortcut back"))
    return out


def judge_wild(ms, bands, need):
    """Wild tables. Ichor's engine falls back to the _Morning table for day and
    evening (OW_TIME_OF_DAY_FALLBACK), so a map with grass needs a _Morning (or
    unsuffixed) land table and a _Night one; _Day is encouraged, not required.
    Water and fishing tables follow the same rule once they're split by time."""
    land = ms.tables("land_mons")
    if ms.grass:
        need("Morning" in land, "FAIL", f"wild: {ms.grass} grass cells but no land table (_Morning or unsuffixed)")
        need("Night" in land, "FAIL", "wild: no _Night land table")
        need("Day" in land, "NOTE", "wild: no _Day land table (day falls back to morning)")
    elif ms.other_enc and ms.kind in ("route", "dungeon"):
        need("Morning" in land, "FAIL", f"wild: {ms.other_enc} cave or sand cells but no land table")
        need("Night" in land or not land, "NOTE", "wild: no _Night land table")
    if ms.reach_water >= WATER_TABLE_CELLS and ms.kind in ("route", "town", "dungeon"):
        for area, what in (("water_mons", "surf"), ("fishing_mons", "fishing")):
            have = ms.tables(area)
            need("Morning" in have, "FAIL", f"wild: {ms.reach_water} reachable water cells but no {what} table")
            if have and have != ["Morning"]:
                need("Night" in have, "FAIL", f"wild: the {what} tables are split by time but have no _Night one")
                need("Day" in have, "NOTE", f"wild: the {what} tables are split by time but have no _Day one")
    if ms.rocks:
        need(ms.tables("rock_smash_mons"), "FAIL", f"wild: {len(ms.rocks)} breakable rocks but no rock-smash table")
    want = LAND_ROUTE["land_species"][ms.band] if ms.kind == "route" else DUNGEON["land_species"]
    for t in land:
        n = ms.species("land_mons", t)
        need(n >= want, "FAIL", f"wild: the {t} land table has {n} species < {want}")
    for area, what, want in (("water_mons", "surf", SURF_SPECIES), ("fishing_mons", "fishing", FISHING_SPECIES)):
        for t in ms.tables(area):
            n = ms.species(area, t)
            need(n >= want, "FAIL", f"wild: the {t} {what} table has {n} species < {want}")
    lv = ms.levels("land_mons")
    if lv:
        need(lv[1] - lv[0] <= LEVEL_BAND_MAX, "FAIL",
             f"wild: land levels span {lv[0]}–{lv[1]}, wider than BALANCE.md's {LEVEL_BAND_MAX}")
        rng = wild_range(bands, ms.stage)
        if rng:
            need(rng[0] <= lv[0] and lv[1] <= rng[1], "WARN",
                 f"wild: land levels {lv[0]}–{lv[1]} sit outside {ms.stage}'s {rng[0]}–{rng[1]} (BALANCE.md)")
        elif ms.stage is None:
            need(False, "NOTE", "wild: no BALANCE.md stage for this map (add its place to map_audit.STAGES)")


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def wild_summary(ms):
    parts = []
    for area, short in (("land_mons", "land"), ("water_mons", "surf"), ("fishing_mons", "fish"),
                        ("rock_smash_mons", "rock")):
        ts = ms.tables(area)
        if ts:
            sp = "/".join(str(ms.species(area, t)) for t in ts)
            parts.append(f"{short} {''.join(t[0] for t in ts)} ({sp} spp)")
    lv = ms.levels("land_mons")
    if lv:
        parts.append(f"Lv {lv[0]}–{lv[1]}")
    return ", ".join(parts) or "none"


def numbers(ms):
    s = (f"{ms.m.w}x{ms.m.h} = {ms.screens:.1f} screens; grass {ms.grass} ({ms.grass / ms.screens:.0f}/screen, "
         f"{100 * ms.grass / ms.cells:.0f}%)")
    if ms.water:
        s += f"; water {100 * ms.water / ms.cells:.0f}%"
    if ms.kind == "route" and not ms.sea:
        f = ms.forced_grass()[0]
        s += f"; forced grass {f if f is not None else '?'}"
    s += (f"; trainers {len(ms.trainers)}; items {len(ms.items)} + {len(ms.hidden)} hidden; signs {len(ms.signs)}; "
          f"NPCs {len(ms.npcs)}")
    if ms.berries:
        s += f"; berry trees {len(ms.berries)}"
    return s + f"; wild: {wild_summary(ms)}"


def ichor_names(repo):
    return [n for n in repo.names if not n.startswith(UPSTREAM_PREFIXES)]


def select(repo, args):
    if args.all_ichor:
        return ichor_names(repo)
    out = []
    for a in args.maps:
        hit = [n for n in repo.names if n == a] or [n for n in repo.names if n.startswith(a)]
        if not hit:
            sys.exit(f"map_audit: no map named or starting with {a}")
        out += [n for n in hit if n not in out]
    return out


def audit(repo, names, show_kinds=("route", "town", "dungeon", "interior")):
    """Measure and judge. Returns [(Measure, [(level, msg)])] and the dungeon groups' results."""
    bands = balance_bands(repo.root)
    ms = {n: Measure(repo, n) for n in names}
    # maps drawn on the same layout, or on a byte-for-byte copy of another map's
    users, key = defaultdict(list), {}
    for n in ichor_names(repo):
        lay = repo.layouts[repo.map_json(n)["layout"]]
        key[n] = hashlib.sha1((repo.root / lay["blockdata_filepath"]).read_bytes()).hexdigest()
        users[key[n]].append(n)
    for m in ms.values():
        m.twins = [n for n in users[key[m.name]] if n != m.name]
    results = [(m, judge(m, bands, ms)) for m in ms.values() if m.kind in show_kinds]
    groups = defaultdict(list)
    for m in ms.values():
        if m.kind == "dungeon" and "dungeon" in show_kinds:
            groups[dungeon_group(m.name)].append(m)
    return results, {g: (fl, judge_dungeon_group(g, fl)) for g, fl in groups.items()}


def print_text(results, groups):
    for ms, rows in results:
        print(f"{ms.name}  [{ms.kind}{', sea' if ms.sea else ''}, {ms.stage or 'no stage'}, {ms.band}]")
        print(f"  {numbers(ms)}")
        for level, msg in rows:
            print(f"  {level:4s}  {msg}")
    for g, (floors, rows) in sorted(groups.items()):
        if rows:
            print(f"{g}  [whole dungeon, {len(floors)} floor(s)]")
            for level, msg in rows:
                print(f"  {level:4s}  {msg}")


STRUCTURAL = ("reach:", "mixed:", "onsolid:", "edge:", "warp:")


def print_markdown(results, groups):
    """Tables and shortfall lists for design/MAP_AUDIT.md. Structural warnings
    (reach, mixed, onsolid, edge, warp) and notes are counted, not listed."""
    def count(r, level):
        return sum(1 for lv, _ in r if lv == level)

    for kind in ("route", "town", "dungeon"):
        rows = sorted([(m, r) for m, r in results if m.kind == kind], key=lambda x: (-count(x[1], "FAIL"), x[0].name))
        if not rows:
            continue
        print(f"\n#### {kind.capitalize()}s\n")
        print("| Map | Stage | Screens | Grass/screen | Forced grass | Trainers | Items | Hidden | Signs | Wild | "
              "Fails | Warnings |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for m, r in rows:
            forced = m.forced_grass()[0] if kind == "route" and not m.sea else None
            print(f"| {m.name}{' (sea)' if m.sea else ''} | {m.stage or '?'} | {m.screens:.1f} | "
                  f"{m.grass / m.screens:.0f} | {'–' if forced is None else forced} | {len(m.trainers)} | "
                  f"{len(m.items)} | {len(m.hidden)} | {len(m.signs)} | {wild_summary(m)} | "
                  f"{count(r, 'FAIL')} | {count(r, 'WARN')} |")
        print(f"\n{kind.capitalize()} shortfalls, worst first:\n")
        for m, r in sorted(rows, key=lambda x: (-count(x[1], "FAIL"), -count(x[1], "WARN"), x[0].name)):
            design = [(lv, msg) for lv, msg in r if lv == "FAIL" or (lv == "WARN" and not msg.startswith(STRUCTURAL))]
            structural = sum(1 for lv, msg in r if lv == "WARN" and msg.startswith(STRUCTURAL))
            notes = [msg.replace("wild: ", "") for lv, msg in r if lv == "NOTE"]
            tail = []
            if structural:
                tail.append(f"{structural} structural warning(s)")
            if notes:
                tail.append("notes: " + "; ".join(notes))
            print(f"- **{m.name}**" + (": meets the standard" if not design else "")
                  + (f" ({', '.join(tail)})" if tail else ""))
            for level, msg in design:
                print(f"  - {level} {msg}")
    gl = [(g, fl, r) for g, (fl, r) in sorted(groups.items()) if r]
    if gl:
        print("\nWhole dungeons:\n")
        for g, fl, r in gl:
            print(f"- **{g}** ({len(fl)} floor(s))")
            for level, msg in r:
                print(f"  - {level} {msg}")


# ---------------------------------------------------------------------------
# The Emerald benchmark (MAP_DESIGN.md §8's appendix)
# ---------------------------------------------------------------------------

EMERALD_TOWNS = ["LittlerootTown", "OldaleTown", "PetalburgCity", "RustboroCity", "DewfordTown", "SlateportCity",
                 "MauvilleCity", "VerdanturfTown", "FallarborTown", "LavaridgeTown", "FortreeCity", "LilycoveCity",
                 "MossdeepCity", "SootopolisCity", "PacifidlogTown", "EverGrandeCity"]
EMERALD_DUNGEONS = {  # for interest: Petalburg Woods, Granite Cave and the other main caves, floor by floor
    "Petalburg Woods": ["PetalburgWoods"],
    "Granite Cave": ["GraniteCave_1F", "GraniteCave_B1F", "GraniteCave_B2F", "GraniteCave_StevensRoom"],
    "Rusturf Tunnel": ["RusturfTunnel"],
    "Meteor Falls": ["MeteorFalls_1F_1R", "MeteorFalls_1F_2R", "MeteorFalls_B1F_1R", "MeteorFalls_B1F_2R"],
    "Fiery Path": ["FieryPath"],
    "Mt. Pyre": [f"MtPyre_{i}F" for i in range(1, 7)],
    "Shoal Cave": ["ShoalCave_LowTideEntranceRoom", "ShoalCave_LowTideInnerRoom", "ShoalCave_LowTideStairsRoom",
                   "ShoalCave_LowTideLowerRoom", "ShoalCave_LowTideIceRoom"],
    "Seafloor Cavern": ["SeafloorCavern_Entrance"] + [f"SeafloorCavern_Room{i}" for i in range(1, 10)],
    "Victory Road": ["VictoryRoad_1F", "VictoryRoad_B1F", "VictoryRoad_B2F"],
}


def export_tree(ref, dest):
    """The map data of a git ref, read into dest with git archive (nothing is checked out)."""
    git = ["git", "-C", str(REPO)]
    listed = subprocess.run(git + ["ls-tree", "-r", "--name-only", ref, "data/tilesets", "design/BALANCE.md"],
                            check=True, capture_output=True, text=True).stdout.split("\n")
    paths = ["data/maps", "data/layouts", "src/data/wild_encounters.json", "include/constants/metatile_behaviors.h",
             "src/data/tilesets/headers.h", "src/data/tilesets/metatiles.h"]
    paths += [p for p in listed if p.endswith("metatile_attributes.bin") or p == "design/BALANCE.md"]
    proc = subprocess.Popen(git + ["archive", ref] + paths, stdout=subprocess.PIPE)
    with tarfile.open(fileobj=proc.stdout, mode="r|") as tar:
        for member in tar:
            if hasattr(tarfile, "data_filter"):
                tar.extract(member, dest, filter="data")
            else:
                tar.extract(member, dest)
    if proc.wait():
        sys.exit(f"map_audit: git archive of {ref} failed")


def quart(xs):
    xs = sorted(xs)
    if len(xs) < 2:
        return (xs[0],) * 3 if xs else (0, 0, 0)
    q = statistics.quantiles(xs, n=4, method="inclusive")
    return q[0], statistics.median(xs), q[2]


def benchmark(repo):
    """Print the appendix's tables: every route 101-134, the towns, Petalburg Woods and the main caves."""
    rows = {f"Route{n}": Measure(repo, f"Route{n}") for n in range(101, 135)}
    towns = [Measure(repo, n) for n in EMERALD_TOWNS]
    dungeons = {g: [Measure(repo, n) for n in names] for g, names in EMERALD_DUNGEONS.items()}

    def sp(m, area):
        return m.species(area, "Morning") if m.tables(area) else None

    def length(m):
        return max(m.m.w / SCREEN_W, m.m.h / SCREEN_H)

    def q(ms, f, digits=None):
        xs = [x for x in (f(m) for m in ms) if x is not None]
        if not xs:
            return "–"
        a, b, c = quart(xs)
        d = digits if digits is not None else (1 if max(a, b, c) < 10 else 0)
        return f"{a:.{d}f} / **{b:.{d}f}** / {c:.{d}f}"

    print("#### Every route\n")
    print("| Route | Size | Screens | Long side | Grass | Grass/screen | Grass % | Water % | Forced grass | "
          "Trainers | Items | Hidden | Signs | NPCs | Berry trees | Rocks | Tables | Species: land / surf / fish |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for n, m in rows.items():
        f = m.forced_grass()[0] if not m.sea else None
        tabs = "+".join(short for a, short in (("land_mons", "land"), ("water_mons", "surf"),
                                               ("fishing_mons", "fish"), ("rock_smash_mons", "rock")) if m.tables(a))
        spp = " / ".join("–" if x is None else str(x) for x in
                         (sp(m, "land_mons"), sp(m, "water_mons"), sp(m, "fishing_mons")))
        print(f"| {n[5:]}{' (sea)' if m.sea else ''} | {m.m.w}×{m.m.h} | {m.screens:.1f} | {length(m):.1f} | "
              f"{m.grass} | {m.grass / m.screens:.0f} | {100 * m.grass / m.cells:.0f} | "
              f"{100 * m.water / m.cells:.0f} | {'–' if f is None else f} | {len(m.trainers)} | {len(m.items)} | "
              f"{len(m.hidden)} | {len(m.signs)} | {len(m.npcs)} | {len(m.berries)} | {len(m.rocks)} | "
              f"{tabs or '–'} | {spp} |")

    def band_of(n):
        k = int(n[5:])
        return "early" if k <= 104 else "middle" if 110 <= k <= 119 else "late" if k >= 120 else "105–109"

    print("\n#### Routes by band\n\nEach cell is the 25th percentile / **median** / 75th percentile.\n")
    print("| Band | Routes | Screens | Long side | Grass/screen | Grass % | Forced grass | Trainers | "
          "Trainers/screen | Items | Items/screen | Hidden | Signs | Ends signed | Land species | Surf species | "
          "Fish species |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    bands = [("early (101–104)", lambda n, m: band_of(n) == "early"),
             ("middle (110–119)", lambda n, m: band_of(n) == "middle"),
             ("late (120–134)", lambda n, m: band_of(n) == "late"),
             ("late, land only (120, 121, 123)", lambda n, m: band_of(n) == "late" and not m.sea),
             ("all land routes", lambda n, m: not m.sea),
             ("all sea routes", lambda n, m: m.sea),
             ("all of 101–134", lambda n, m: True)]
    for label, pick in bands:
        ms = [m for n, m in rows.items() if pick(n, m)]
        ends = sum(len(m.main_exits()) for m in ms)
        signed = ends - sum(len(m.unsigned_ends()) for m in ms)
        print(f"| {label} | {len(ms)} | {q(ms, lambda m: m.screens)} | {q(ms, length)} | "
              f"{q(ms, lambda m: m.grass / m.screens)} | {q(ms, lambda m: 100 * m.grass / m.cells)} | "
              f"{q([m for m in ms if not m.sea], lambda m: m.forced_grass()[0], 0)} | "
              f"{q(ms, lambda m: len(m.trainers))} | {q(ms, lambda m: len(m.trainers) / m.screens, 2)} | "
              f"{q(ms, lambda m: len(m.items))} | {q(ms, lambda m: len(m.items) / m.screens, 2)} | "
              f"{q(ms, lambda m: len(m.hidden))} | {q(ms, lambda m: len(m.signs))} | {signed} of {ends} | "
              f"{q(ms, lambda m: sp(m, 'land_mons'), 0)} | {q(ms, lambda m: sp(m, 'water_mons'), 0)} | "
              f"{q(ms, lambda m: sp(m, 'fishing_mons'), 0)} |")

    print("\n#### Towns\n")
    print("| Town | Size | Screens | Items | Hidden | Signs | NPCs | Doors | Tables |")
    print("|---|---|---|---|---|---|---|---|---|")
    for m in towns:
        doors = sum(1 for w in m.m.warps if repo.name_of(w.get("dest_map"))
                    and classify(repo, repo.name_of(w.get("dest_map"))) == "interior")
        tabs = "+".join(short for a, short in (("land_mons", "land"), ("water_mons", "surf"), ("fishing_mons", "fish"))
                        if m.tables(a))
        print(f"| {m.name} | {m.m.w}×{m.m.h} | {m.screens:.1f} | {len(m.items)} | {len(m.hidden)} | "
              f"{len(m.signs)} | {len(m.npcs)} | {doors} | {tabs or '–'} |")
    print(f"| **25th / median / 75th** | | {q(towns, lambda m: m.screens)} | {q(towns, lambda m: len(m.items))} | "
          f"{q(towns, lambda m: len(m.hidden))} | {q(towns, lambda m: len(m.signs))} | "
          f"{q(towns, lambda m: len(m.npcs))} | | |")

    print("\n#### Petalburg Woods and the main caves\n")
    print("| Dungeon | Floors | Trainers | Items + hidden | Per floor | Healer | Land species, by floor |")
    print("|---|---|---|---|---|---|---|")
    per_floor = []
    for g, fl in dungeons.items():
        per_floor += [len(f.items) + len(f.hidden) for f in fl]
        items = sum(len(f.items) + len(f.hidden) for f in fl)
        spp = ", ".join(str(sp(f, "land_mons")) for f in fl if sp(f, "land_mons"))
        print(f"| {g} | {len(fl)} | {sum(len(f.trainers) for f in fl)} | {sum(len(f.items) for f in fl)} + "
              f"{sum(len(f.hidden) for f in fl)} | {items / len(fl):.1f} | "
              f"{'yes' if any(f.heals for f in fl) else 'no'} | {spp or '–'} |")
    fl_all = list(dungeons.values())
    print(f"| **25th / median / 75th** | {q(fl_all, len)} | "
          f"{q(fl_all, lambda fl: sum(len(f.trainers) for f in fl))} | "
          f"hidden {q(fl_all, lambda fl: sum(len(f.hidden) for f in fl))} | "
          f"{q(per_floor, lambda x: x)} | | |")

    land = [m for m in rows.values() if not m.sea]
    dead = [(m.name, d) for m in land for d in m.dead_ends()]
    print(f"\nThe dead-end heuristic flags {len(dead)} empty pocket(s) on Emerald's {len(land)} land routes: "
          + "; ".join(f"{n} at {d[2]} ({d[0]} cells)" for n, d in dead) + ".")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("maps", nargs="*", help="map names or name prefixes")
    ap.add_argument("--all-ichor", action="store_true", help="every Ichor map in map_groups.json")
    ap.add_argument("--warn-only", action="store_true", help="report shortfalls but exit 0")
    ap.add_argument("--root", help="tree to audit (default: this repo)")
    ap.add_argument("--ref", help="audit a git ref (a branch) instead; its maps are read with git archive")
    ap.add_argument("--markdown", action="store_true", help="print tables for design/MAP_AUDIT.md")
    ap.add_argument("--benchmark", action="store_true",
                    help="measure Emerald's routes at the upstream merge-base (or at --root)")
    ap.add_argument("--kinds", default="route,town,dungeon,interior", help="classes to report (comma-separated)")
    args = ap.parse_args()
    if not args.benchmark and not args.maps and not args.all_ichor:
        ap.error("name some maps or prefixes, or pass --all-ichor")
    ref = args.ref or (UPSTREAM_BASE if args.benchmark and not args.root else None)
    if ref:
        sha = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", ref], check=True,
                             capture_output=True, text=True).stdout.strip()
        print(f"{ref} at {sha}\n" if args.ref else f"upstream merge-base {sha}\n")
        with tempfile.TemporaryDirectory() as tmp:
            export_tree(ref, tmp)
            return run(Repo(tmp), args)
    return run(Repo(args.root or REPO), args)


def run(repo, args):
    if args.benchmark:
        benchmark(repo)
        return 0
    results, groups = audit(repo, select(repo, args), tuple(args.kinds.split(",")))
    (print_markdown if args.markdown else print_text)(results, groups)
    fails = sum(1 for _, r in results for lv, _ in r if lv == "FAIL")
    fails += sum(1 for _, r in groups.values() for lv, _ in r if lv == "FAIL")
    warns = sum(1 for _, r in results for lv, _ in r if lv == "WARN")
    failing = sorted({m.name for m, r in results if any(lv == "FAIL" for lv, _ in r)})
    print(f"\n{len(results)} map(s): {fails} hard shortfall(s) in {len(failing)} map(s), {warns} warning(s)")
    return 1 if fails and not args.warn_only else 0


if __name__ == "__main__":
    sys.exit(main())
