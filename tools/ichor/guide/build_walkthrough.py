#!/usr/bin/env python3
"""Build the Ichor player's walkthrough: one self-contained HTML page.

Writes build/guide/ichor_walkthrough.html from the game's own data:
  data/maps/*/map.json           items, hidden items, trainers, NPC positions
  data/maps/*/scripts.pory       which trainer each script battles, NPC gifts
  src/data/wild_encounters.json  wild tables, by time of day
  src/data/trainers.party        trainer parties (Hero, Mortal, Spartan)
  src/battle_main.c              trainer class names and prize money
  species, item and move data    names, types, sprites and icons
  data/layouts + tilesets        map renders (tools/ichor/render_map.py)

The prose (walkthrough steps, tips, puzzles, spoilers, Hierophant strategy)
lives in tools/ichor/guide/content/*.json, written from the scripts. Every
numbered callout on a map is placed from the event coordinates (16 px a tile).

Usage: tools/ichor/guide/build_walkthrough.py [-o OUT]
Needs Pillow and numpy (macOS's /usr/bin/python3 has both).
"""
import argparse
import base64
import html
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools/ichor"))
import render_map  # noqa: E402

TILE = 16

# Chapters in story order: (id, tab label, title, content file, intro)
CHAPTERS = [
    ("ch1", "I", "Kalliste Isle", "kalliste.json",
     "Your home island. Pick your first partner, follow the Klotheia, and win the Hearth Laurel at Akti."),
    ("ch2", "II", "The Voyage and Emporion", "voyage.json",
     "The trireme Euploia carries you to the mainland by way of Aegina. In Emporion, Hermes's Herald waits."),
    ("ch3", "III", "The Isthmus to Eleusa", "eleusa.json",
     "Through Hecate's dark Hollow and along the Skironian cliffs to Demeter's village and the Mysteries."),
    ("ch4", "IV", "Act II: The Road to Thyrsa", "thyrsa.json",
     "North over Mt. Kithairon to Dionysus's city, the Dionysia and the Mask Laurel."),
]
# Content-file areas that are built but not reachable yet: moved to "Coming up".
NOT_YET = {"aegina-aphaia-road", "aegina-temple-of-aphaia", "aegina-mount-oros"}
# Next connected stretch past Thyrsa: shown from data alone.
COMING_UP = [
    ("route-8", "Route 8: the Kopais Road", ["Route8_KopaisRoad"], "route",
     "West from Thyrsa along the shore of Lake Kopais. Its sign reads: East: Thyrsa. West: Lebadeia."),
    ("lebadeia", "Lebadeia", ["Lebadeia"], "town",
     "The town of Trophonios's oracle cave, where the road turns south toward Kirrha."),
    ("route-9", "Route 9: the Parnassos Crossroads", ["Route9_ParnassosCrossroads"], "route",
     "South from Lebadeia under Parnassos. Its sign reads: South: Kirrha and the Gulf trireme."),
    ("kirrha", "Kirrha", ["Kirrha"], "town",
     "The port below Delphoi, where the Euploia crosses the Gulf of Korinthos to Aigion."),
]

TIMES = [("Morning", "Morn", "6–10"), ("Day", "Day", "10–19"), ("Evening", "Eve", "19–20"), ("Night", "Night", "20–6")]
DIFF_NAME = {None: "Hero", "Normal": "Hero", "Easy": "Mortal", "Hard": "Spartan"}

TYPE_COLORS = {
    "NORMAL": "#9a9478", "FIRE": "#d4683a", "WATER": "#4f7fc4", "GRASS": "#5f9a46", "ELECTRIC": "#c9a227",
    "ICE": "#6fb6b8", "FIGHTING": "#a8432f", "POISON": "#8a4f93", "GROUND": "#b08a4c", "FLYING": "#8a8fc8",
    "PSYCHIC": "#c8557a", "BUG": "#8a9a2c", "ROCK": "#a08c4a", "GHOST": "#5f5285", "DRAGON": "#5b4fb8",
    "DARK": "#5a4a40", "STEEL": "#8c8fa0", "FAIRY": "#c27fa8",
}


def esc(s):
    return html.escape(str(s), quote=True)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def title_const(c, prefix):
    s = c.removeprefix(prefix).replace("_", " ").title()
    return s


# --- game data --------------------------------------------------------------

class Game:
    def __init__(self):
        self.maps = {}
        for p in sorted((ROOT / "data/maps").glob("*/map.json")):
            m = json.loads(p.read_text())
            self.maps[m["name"]] = m
        self.map_by_id = {m["id"]: m for m in self.maps.values()}
        self.scripts = {}
        for name in self.maps:
            sp = ROOT / "data/maps" / name / "scripts.pory"
            self.scripts[name] = sp.read_text() if sp.exists() else ""
        self.load_species()
        self.load_moves()
        self.load_items()
        self.load_classes()
        self.load_trainers()
        self.load_wild()
        layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
        self.layouts = {l["id"]: l for l in layouts if "id" in l}

    # species: name, types, front sprite
    def load_species(self):
        gfx = {}
        for p in (ROOT / "src/data/graphics").glob("pokemon*.h"):
            for sym, path in re.findall(r'(gMonFrontPic_\w+)\[\]\s*=\s*INCGFX_U32\("([^"]+)"', p.read_text()):
                gfx[sym] = path
        self.species = {}
        for p in (ROOT / "src/data/pokemon/species_info").glob("*.h"):
            text = p.read_text()
            for m in re.finditer(r"\[(SPECIES_\w+)\]\s*=\s*\{", text):
                body = text[m.end():m.end() + 6000]
                nm = re.search(r'\.speciesName\s*=\s*_\("([^"]+)"\)', body)
                ty = re.search(r"\.types\s*=\s*MON_TYPES\((TYPE_\w+)(?:,\s*(TYPE_\w+))?\)", body)
                fp = re.search(r"\.frontPic\s*=\s*(gMonFrontPic_\w+)", body)
                if not nm or m.group(1) in self.species:
                    continue
                types = []
                if ty:
                    types = [t.removeprefix("TYPE_") for t in ty.groups() if t]
                    types = list(dict.fromkeys(types))
                self.species[m.group(1)] = {
                    "name": nm.group(1), "types": types,
                    "front": gfx.get(fp.group(1)) if fp else None,
                }
        self.species_by_name = {}
        for k, v in self.species.items():
            self.species_by_name.setdefault(v["name"].lower(), k)

    def load_moves(self):
        text = (ROOT / "src/data/moves_info.h").read_text()
        self.moves = {}
        for m in re.finditer(r"\[(MOVE_\w+)\]\s*=\s*\{", text):
            body = text[m.end():m.end() + 1500]
            nm = re.search(r'\.name\s*=\s*COMPOUND_STRING\("([^"]+)"\)', body)
            ty = re.search(r"\.type\s*=\s*(TYPE_\w+)", body)
            if nm:
                self.moves[m.group(1)] = {"name": nm.group(1), "type": ty.group(1)[5:] if ty else "NORMAL"}
        tms = (ROOT / "include/constants/tms_hms.h").read_text()
        block = re.search(r"#define FOREACH_TM\(F\)(.*?)\n\n", tms, re.S).group(1)
        self.tm_moves = re.findall(r"F\((\w+)\)", block)

    def load_items(self):
        gfx = {}
        for sym, path in re.findall(r'(gItemIcon\w+)\[\]\s*=\s*INCGFX_U(?:32|16)\("([^"]+)"',
                                    (ROOT / "src/data/graphics/items.h").read_text()):
            gfx[sym] = path
        text = (ROOT / "src/data/items.h").read_text()
        self.items = {}
        for m in re.finditer(r"\[(ITEM_\w+)\]\s*=\s*\{", text):
            body = text[m.end():m.end() + 2500]
            body = body[:body.find("\n    },")] if "\n    }," in body else body
            nm = re.search(r'\.name\s*=\s*ITEM_NAME\("([^"]+)"\)', body)
            ic = re.search(r"\.iconPic\s*=\s*(\w+)", body)
            pal = re.search(r"\.iconPalette\s*=\s*(\w+)", body)
            self.items[m.group(1)] = {
                "name": nm.group(1) if nm else title_const(m.group(1), "ITEM_"),
                "icon": gfx.get(ic.group(1)) if ic else None,
                "pal": gfx.get(pal.group(1)) if pal else None,
            }

    def item_name(self, const):
        tm = re.fullmatch(r"ITEM_TM(\d+)", const)
        if tm:
            n = int(tm.group(1))
            mv = self.tm_moves[n - 1] if n <= len(self.tm_moves) else None
            mname = self.moves.get("MOVE_" + mv, {}).get("name", "") if mv else ""
            return f"TM{n:02d} {mname}".strip()
        tm = re.fullmatch(r"ITEM_TM_(\w+)", const)
        if tm and tm.group(1) in self.tm_moves:
            n = self.tm_moves.index(tm.group(1)) + 1
            return f"TM{n:02d} {self.moves.get('MOVE_' + tm.group(1), {}).get('name', '')}".strip()
        it = self.items.get(const)
        return it["name"] if it else title_const(const, "ITEM_")

    def tm_type(self, const):
        tm = re.fullmatch(r"ITEM_TM(\d+)", const)
        mv = None
        if tm:
            n = int(tm.group(1))
            mv = self.tm_moves[n - 1] if n <= len(self.tm_moves) else None
        tm2 = re.fullmatch(r"ITEM_TM_(\w+)", const)
        if tm2:
            mv = tm2.group(1)
        if not mv:
            return None
        return self.moves.get("MOVE_" + mv, {}).get("type", "NORMAL")

    def load_classes(self):
        text = (ROOT / "src/battle_main.c").read_text()
        self.classes = {}
        for c, name, money in re.findall(r'\[(TRAINER_CLASS_\w+)\]\s*=\s*\{\s*_\("([^"]*)"\)(?:,\s*(\d+))?', text):
            self.classes[c] = {"name": name.replace("{PKMN}", "Pokémon").title() if name.isupper() else name,
                               "money": int(money) if money else 5}

    def load_trainers(self):
        text = (ROOT / "src/data/trainers.party").read_text()
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        self.trainers = {}
        for blk in re.split(r"(?m)^(?==== )", text):
            m = re.match(r"=== (TRAINER_\w+) ===\n", blk)
            if not m:
                continue
            tid = m.group(1)
            parts = re.split(r"\n\s*\n", blk[m.end():].strip())
            head = {}
            for line in parts[0].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    head[k.strip()] = v.strip()
            mons = []
            for p in parts[1:]:
                lines = [l.strip() for l in p.strip().splitlines() if l.strip()]
                if not lines or ":" in lines[0] and not re.search(r"@|\(", lines[0]) and not lines[0][0].isupper():
                    continue
                first = lines[0]
                item = None
                if "@" in first:
                    first, item = [s.strip() for s in first.split("@", 1)]
                first = re.sub(r"\((M|F)\)", "", first).strip()
                nick = re.search(r"\(([^)]+)\)", first)
                sp = nick.group(1) if nick else first
                mon = {"species": sp.strip(), "item": item, "moves": [], "level": None}
                for l in lines[1:]:
                    if l.startswith("- "):
                        mon["moves"].append(l[2:].strip())
                    elif l.startswith("Level:"):
                        mon["level"] = int(l.split(":")[1])
                    elif l.startswith("Ability:"):
                        mon["ability"] = l.split(":", 1)[1].strip()
                    elif l.startswith("Nature:"):
                        mon["nature"] = l.split(":", 1)[1].strip()
                    elif l.endswith(" Nature"):
                        mon["nature"] = l[:-7].strip()
                if mon["level"] is None:
                    continue
                mons.append(mon)
            diff = head.get("Difficulty")
            entry = {"head": head, "mons": mons, "diff": DIFF_NAME.get(diff, diff)}
            self.trainers.setdefault(tid, {})[entry["diff"]] = entry

    def trainer(self, tid, diff="Hero"):
        v = self.trainers.get(tid)
        if not v:
            return None
        return v.get(diff) or v.get("Hero") or next(iter(v.values()))

    def prize(self, t):
        if not t or not t["mons"]:
            return None
        cls = "TRAINER_CLASS_" + re.sub(r"[^A-Z0-9]+", "_", t["head"].get("Class", "").upper()).strip("_")
        money = self.classes.get(cls, {}).get("money", 5)
        mult = 2 if t["head"].get("Battle Type", "").lower().startswith("double") else 1
        return 4 * t["mons"][-1]["level"] * money * mult

    def class_name(self, t):
        cls = "TRAINER_CLASS_" + re.sub(r"[^A-Z0-9]+", "_", t["head"].get("Class", "").upper()).strip("_")
        return self.classes.get(cls, {}).get("name") or t["head"].get("Class", "")

    def load_wild(self):
        d = json.loads((ROOT / "src/data/wild_encounters.json").read_text())
        g = d["wild_encounter_groups"][0]
        self.wild_rates = {f["type"]: f for f in g["fields"]}
        self.wild = {}
        for e in g["encounters"]:
            lab = e["base_label"]
            tod = "Morning"
            for t, _, _ in TIMES:
                if lab.endswith("_" + t):
                    tod = t
            self.wild.setdefault(e["map"], {})[tod] = e

    # scripts
    def script_body(self, mapname, script):
        text = self.scripts.get(mapname, "")
        m = re.search(r"(?m)^script\s+" + re.escape(script) + r"\b[^{]*\{", text)
        if not m:
            return ""
        nxt = re.search(r"(?m)^(script|text|movement|mart|mapscripts)\s", text[m.end():])
        return text[m.end():m.end() + nxt.start()] if nxt else text[m.end():]


# --- images -----------------------------------------------------------------

class Images:
    def __init__(self, game):
        self.g = game
        self.css = {}        # class -> data uri
        render_map.read_fieldmap_constants()
        self.symbols = render_map.scan_tileset_symbols()
        self.tilesets = {}

    @staticmethod
    def png_uri(img, colors=256):
        buf = io.BytesIO()
        if img.mode == "RGBA":
            img.save(buf, "PNG", optimize=True)
        else:
            q = img.convert("RGB")
            if len(q.getcolors(1 << 16) or []) <= 256 and q.getcolors(1 << 16) is not None:
                q = q.quantize(colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
            q.save(buf, "PNG", optimize=True)
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

    def tileset(self, name):
        if name not in self.tilesets:
            self.tilesets[name] = render_map.Tileset(render_map.resolve_tileset(name, self.symbols))
        return self.tilesets[name]

    def render(self, mapname):
        m = self.g.maps[mapname]
        lay = self.g.layouts.get(m["layout"])
        if not lay:
            return None
        import numpy as np
        r = render_map.Renderer(self.tileset(lay["primary_tileset"]), self.tileset(lay["secondary_tileset"]))
        blocks = np.fromfile(ROOT / lay["blockdata_filepath"], "<u2")
        return render_map.render_blocks(r, blocks, lay["width"])

    def sprite_class(self, species_const):
        sp = self.g.species.get(species_const)
        if not sp or not sp["front"]:
            return None
        cls = "sp-" + slug(species_const.removeprefix("SPECIES_"))
        if cls in self.css:
            return cls
        p = ROOT / sp["front"]
        if not p.exists():
            return None
        im = Image.open(p)
        pal = im.getpalette() if im.mode == "P" else None
        im = im.convert("RGBA") if im.mode != "P" else im
        if pal is not None:
            idx = im
            im = im.convert("RGBA")
            a = [0 if v == 0 else 255 for v in idx.getdata()]
            alpha = Image.new("L", idx.size)
            alpha.putdata(a)
            im.putalpha(alpha)
        w = im.width
        im = im.crop((0, 0, w, min(w, im.height)))
        bbox = im.getbbox()
        self.css[cls] = (self.png_uri(im), im.width, im.height)
        return cls

    @staticmethod
    def read_jasc(path):
        lines = Path(path).read_text().split()
        vals = [int(v) for v in lines[3:3 + 48]]
        return [tuple(vals[i:i + 3]) for i in range(0, len(vals), 3)]

    def icon_class(self, item_const):
        cls = "ic-" + slug(item_const.removeprefix("ITEM_"))
        if cls in self.css:
            return cls
        it = self.g.items.get(item_const, {})
        icon, pal = it.get("icon"), it.get("pal")
        ttype = self.g.tm_type(item_const)
        if ttype:
            icon = "graphics/items/icons/tm.png"
            pal = f"graphics/items/icon_palettes/{ttype.lower()}_tm_hm.pal"
        if not icon:
            return None
        ip = ROOT / icon
        pp = ROOT / re.sub(r"\.gbapal$", ".pal", pal) if pal else None
        if not ip.exists():
            return None
        im = Image.open(ip)
        if im.mode == "P":
            idx = list(im.getdata())
            colors = self.read_jasc(pp) if pp and pp.exists() else [tuple(im.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
            out = Image.new("RGBA", im.size)
            out.putdata([(0, 0, 0, 0) if v % 16 == 0 else (*colors[v % 16], 255) for v in idx])
            im = out
        else:
            im = im.convert("RGBA")
        self.css[cls] = (self.png_uri(im), im.width, im.height)
        return cls

    def stylesheet(self):
        out = []
        for cls, (uri, w, h) in self.css.items():
            out.append(f".{cls}{{background-image:url({uri})}}")
        return "\n".join(out)


# --- area model ---------------------------------------------------------------

def collect_map(game, mapname):
    """Items, hidden items, trainers and gifts on one map, from its events."""
    m = game.maps[mapname]
    pts = []
    for o in m.get("object_events", []):
        gid = o["graphics_id"]
        if gid == "OBJ_EVENT_GFX_ITEM_BALL":
            pts.append({"kind": "item", "x": o["x"], "y": o["y"], "item": o["trainer_sight_or_berry_tree_id"],
                        "flag": o.get("flag", "")})
    for b in m.get("bg_events", []):
        if b["type"] == "hidden_item":
            pts.append({"kind": "hidden", "x": b["x"], "y": b["y"], "item": b["item"],
                        "qty": b.get("quantity", 1), "flag": b.get("flag", "")})
    # trainers: every trainerbattle in the map's scripts, located by object script if any
    text = game.scripts.get(mapname, "")
    obj_by_script = {}
    for o in m.get("object_events", []):
        obj_by_script.setdefault(o["script"], o)
    order = []
    for sm in re.finditer(r"(?m)^script\s+(\w+)", text):
        body = game.script_body(mapname, sm.group(1))
        for tid in re.findall(r"trainerbattle_\w+\((TRAINER_\w+)", body):
            order.append((tid, sm.group(1)))
    seen = set()
    trainers = []
    for tid, script in order:
        if tid in seen:
            continue
        seen.add(tid)
        o = obj_by_script.get(script)
        trainers.append({"kind": "trainer", "tid": tid, "script": script,
                         "x": o["x"] if o else None, "y": o["y"] if o else None})
    return pts, trainers


def find_event(game, mapname, script):
    m = game.maps.get(mapname)
    if not m:
        return None
    for o in m.get("object_events", []):
        if o.get("script") == script:
            return o["x"], o["y"]
    for b in m.get("bg_events", []):
        if b.get("script") == script:
            return b["x"], b["y"]
    for c in m.get("coord_events", []):
        if c.get("script") == script:
            return c["x"], c["y"]
    return None


def gifts_of(game, mapname, script):
    body = game.script_body(mapname, script)
    out = []
    for item, qty in re.findall(r"giveitem\((ITEM_\w+)(?:,\s*(\d+))?\)", body):
        out.append((item, int(qty) if qty else 1))
    return out


# --- HTML -----------------------------------------------------------------------

class Page:
    def __init__(self, game, images):
        self.g = game
        self.im = images
        self.parts = []
        self.toc = []
        self.missing = []
        self.counts = {"areas": 0, "items": 0, "trainers": 0, "maps": 0}

    def w(self, s):
        self.parts.append(s)

    # small pieces
    def species_chip(self, name_or_const, level=None, big=False):
        const = name_or_const if name_or_const.startswith("SPECIES_") else \
            self.g.species_by_name.get(name_or_const.lower())
        sp = self.g.species.get(const) if const else None
        name = sp["name"] if sp else name_or_const
        cls = self.im.sprite_class(const) if const else None
        types = "".join(f'<i class="ty" style="--t:{TYPE_COLORS.get(t, "#888")}">{t.title()}</i>'
                        for t in (sp["types"] if sp else []))
        spr = f'<span class="spr {cls}{" big" if big else ""}" role="img" aria-label="{esc(name)}"></span>' if cls else \
            f'<span class="spr none{" big" if big else ""}"></span>'
        return spr, name, types

    def item_chip(self, const, qty=1):
        cls = self.im.icon_class(const)
        name = self.g.item_name(const)
        q = f" ×{qty}" if qty and qty > 1 else ""
        ic = f'<span class="ico {cls}" aria-hidden="true"></span>' if cls else '<span class="ico none"></span>'
        return f'<span class="itm">{ic}<span>{esc(name)}{q}</span></span>'

    # ----- sections
    def area(self, ch_id, a, coming=False):
        aid = slug(a["id"])
        self.counts["areas"] += 1
        self.toc[-1][2].append((aid, a["title"], a.get("kind", "")))
        kind = a.get("kind", "route")
        label = {"town": "Town", "route": "Route", "dungeon": "Dungeon", "temple": "Temple"}.get(kind, kind.title())
        self.w(f'<section class="area k-{esc(kind)}" id="{aid}">')
        self.w('<header class="area-head">')
        self.w(f'<p class="kicker"><span>{esc(label)}</span>{"<span class=soon>Coming up</span>" if coming else ""}</p>')
        self.w(f'<h3>{esc(a["title"])}</h3>')
        if a.get("blurb"):
            self.w(f'<p class="blurb">{esc(a["blurb"])}</p>')
        self.w('</header>')

        maps = [m for m in a["maps"] if m in self.g.maps]
        for m in a["maps"]:
            if m not in self.g.maps:
                self.missing.append(f"{a['id']}: map {m} not found")
        # Towns show their outdoor map; interiors are listed below it. Routes,
        # dungeons and temples show every map (sanctum floors, the trireme's hold).
        main = maps[:1] if kind == "town" else [m for m in maps if not m.endswith("RestHouse")]
        if a.get("walkthrough"):
            self.w('<div class="steps">')
            for i, p in enumerate(a["walkthrough"], 1):
                self.w(f'<p><b class="stepn">{i}</b>{esc(p)}</p>')
            self.w('</div>')

        # gather all callout data
        all_items = []
        all_trainers = []
        for mn in maps:
            pts, trs = collect_map(self.g, mn)
            for p in pts:
                p["map"] = mn
            for t in trs:
                t["map"] = mn
            all_items += pts
            all_trainers += trs
        npcs = []
        for n in a.get("key_npcs", []) or []:
            pos = find_event(self.g, n.get("map"), n.get("script", ""))
            npcs.append({**n, "pos": pos})
            if pos is None:
                self.missing.append(f"{a['id']}: NPC script {n.get('script')} not found on {n.get('map')}")

        # number callouts per rendered map
        numbering = {}
        for mn in maps:
            k = 0
            for p in all_items:
                if p["map"] == mn:
                    k += 1
                    numbering[id(p)] = k
            for t in all_trainers:
                if t["map"] == mn and t["x"] is not None:
                    k += 1
                    numbering[id(t)] = k
            tpos = {(t["x"], t["y"]): t for t in all_trainers if t["map"] == mn and t["x"] is not None}
            for n in npcs:
                if n.get("map") == mn and n["pos"]:
                    if tuple(n["pos"]) in tpos:      # a trainer already marks this spot
                        tpos[tuple(n["pos"])]["note"] = n.get("note", "")
                        n["merged"] = True
                        continue
                    k += 1
                    numbering[id(n)] = k

        for mn in maps:
            render = mn in main
            if not render:
                continue
            self.map_block(a, mn, all_items, all_trainers, npcs, numbering, multi=len(main) > 1)

        # interiors with things in them, listed without renders
        others = [mn for mn in maps if mn not in main]
        oth = [n for n in npcs if n.get("map") in others]
        oth_items = [p for p in all_items if p["map"] in others]
        if oth or oth_items:
            self.w('<div class="indoors"><h4>Indoors</h4><ul class="keylist">')
            for mn in others:
                rows = [n for n in oth if n["map"] == mn]
                its = [p for p in oth_items if p["map"] == mn]
                if not rows and not its:
                    continue
                for n in rows:
                    gl = gifts_of(self.g, mn, n.get("script", ""))
                    gift = "".join(self.item_chip(i, q) for i, q in gl)
                    self.w(f'<li><span class="mk npc sm">•</span><div><b>{esc(n.get("label", ""))}</b>'
                           f' <span class="where">{esc(self.map_title(mn))}</span><br>{esc(n.get("note", ""))}'
                           f'{"<div class=gifts>" + gift + "</div>" if gift else ""}</div></li>')
                for p in its:
                    self.w(f'<li><span class="mk {"hid" if p["kind"] == "hidden" else "item"} sm">•</span><div>'
                           f'{self.item_chip(p["item"], p.get("qty", 1))} <span class="where">{esc(self.map_title(mn))}'
                           f'{" (hidden)" if p["kind"] == "hidden" else ""}</span></div></li>')
            self.w('</ul></div>')

        self.wild_block(a, maps)
        self.statics_block(a)
        self.trainer_block(a, all_trainers, numbering)
        if a.get("hierophant"):
            self.hierophant(a)
        self.checklist(aid, a, all_items, npcs)
        self.shops_block(a)
        self.tips_block(a)
        self.puzzles_block(a)
        self.spoilers_block(a)
        self.w('</section>')

    def map_title(self, mn):
        s = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", mn.split("_", 1)[1] if "_" in mn else mn)
        s = re.sub(r"(?<=[a-z])(?=\d)", " ", s)
        return s.replace("Of ", "of ")

    def map_block(self, a, mn, items, trainers, npcs, numbering, multi):
        img = self.im.render(mn)
        if img is None:
            self.missing.append(f"{a['id']}: no render for {mn}")
            return
        self.counts["maps"] += 1
        W, H = img.size
        uri = Images.png_uri(img)
        marks = []
        keyrows = []
        for p in items:
            if p["map"] != mn:
                continue
            n = numbering[id(p)]
            hid = p["kind"] == "hidden"
            marks.append((n, p["x"], p["y"], "hid" if hid else "item"))
            keyrows.append((n, "hid" if hid else "item",
                            self.item_chip(p["item"], p.get("qty", 1)) + (' <span class="tag">Hidden</span>' if hid else "")))
        for t in trainers:
            if t["map"] != mn or t["x"] is None:
                continue
            n = numbering[id(t)]
            tr = self.g.trainer(t["tid"])
            nm = f'{self.g.class_name(tr)} {tr["head"].get("Name", "").title()}' if tr else t["tid"]
            marks.append((n, t["x"], t["y"], "trn"))
            hier = (a.get("hierophant") or {}).get("trainer", "")
            anchor = f'{slug(a["id"])}-hierophant' if t["tid"] in (hier, re.sub(r"_DAY$", "_NIGHT", hier)) \
                else f't-{slug(t["tid"])}'
            note = f' {esc(t["note"])}' if t.get("note") else ""
            keyrows.append((n, "trn", f'<a href="#{anchor}">{esc(nm)}</a>{note}'))
        for nn in npcs:
            if nn.get("map") != mn or not nn["pos"] or nn.get("merged"):
                continue
            n = numbering[id(nn)]
            marks.append((n, nn["pos"][0], nn["pos"][1], "npc"))
            gl = gifts_of(self.g, mn, nn.get("script", ""))
            gift = "".join(self.item_chip(i, q) for i, q in gl)
            keyrows.append((n, "npc", f'<b>{esc(nn.get("label", ""))}</b> {esc(nn.get("note", ""))}'
                                      f'{"<span class=gifts>" + gift + "</span>" if gift else ""}'))
        cap = self.map_title(mn) if multi else a["title"]
        self.w('<figure class="mapfig">')
        self.w(f'<figcaption><span>{esc(cap)}</span><span class="dim">{W // TILE}×{H // TILE} tiles</span></figcaption>')
        self.w('<div class="mapgrid"><div class="mapscroll"' + (' data-tall' if H > 900 else '') + '>')
        zoom = 2 if W <= 480 and H <= 640 else 1   # small rooms read better at 2x
        self.w(f'<div class="mapwrap" style="width:{W * zoom}px;aspect-ratio:{W}/{H}">')
        self.w(f'<img src="{uri}" width="{W}" height="{H}" alt="Overhead map of {esc(cap)}" loading="lazy">')
        for n, x, y, k in marks:
            left = (x + 0.5) * TILE / W * 100
            top = (y + 0.5) * TILE / H * 100
            self.w(f'<span class="mk {k}" style="left:{left:.3f}%;top:{top:.3f}%">{n}</span>')
        self.w('</div></div>')
        if keyrows:
            self.w('<ol class="keylist">')
            for n, k, body in keyrows:
                self.w(f'<li><span class="mk {k} sm">{n}</span><div>{body}</div></li>')
            self.w('</ol>')
        self.w('</div></figure>')

    def wild_block(self, a, maps):
        tables = []
        for mn in maps:
            mid = self.g.maps[mn]["id"]
            w = self.g.wild.get(mid)
            if not w:
                continue
            for field, label in (("land_mons", "Tall grass"), ("water_mons", "Surfing"),
                                 ("rock_smash_mons", "Smashed rocks"), ("fishing_mons", "Fishing")):
                per = {}
                for t, _, _ in TIMES:
                    e = w.get(t) or w.get("Morning")
                    per[t] = e.get(field) if e else None
                if not any(per.values()):
                    continue
                rates = self.g.wild_rates[field]["encounter_rates"]
                groups = self.g.wild_rates[field].get("groups") or {"": list(range(len(rates)))}
                for gname, idxs in groups.items():
                    rows = {}
                    for t, _, _ in TIMES:
                        tab = per[t]
                        if not tab:
                            continue
                        tot = sum(rates[i] for i in idxs)
                        for i in idxs:
                            if i >= len(tab["mons"]):
                                continue
                            mon = tab["mons"][i]
                            r = rows.setdefault(mon["species"], {"min": 99, "max": 0, "t": {}})
                            r["min"] = min(r["min"], mon["min_level"])
                            r["max"] = max(r["max"], mon["max_level"])
                            r["t"][t] = r["t"].get(t, 0) + rates[i] * 100 / tot
                    if not rows:
                        continue
                    sub = {"old_rod": "Old Rod", "good_rod": "Good Rod", "super_rod": "Super Rod"}.get(gname, "")
                    tables.append((mn, label + (f": {sub}" if sub else ""), rows,
                                   per["Morning"]["encounter_rate"] if per["Morning"] else None))
        if not tables:
            return
        self.w('<div class="block wild"><h4>Wild Pokémon</h4>')
        for mn, label, rows, er in tables:
            same = all(abs(r["t"].get(t, 0) - r["t"].get("Morning", 0)) < 0.01 for r in rows.values() for t, _, _ in TIMES)
            cap = label + (f" — {self.map_title(mn)}" if len(set(x[0] for x in tables)) > 1 else "")
            self.w(f'<div class="tblscroll"><table class="wildt"><caption>{esc(cap)}</caption><thead><tr><th>Pokémon</th><th>Lv.</th>')
            if same:
                self.w('<th class="num">Rate</th>')
            else:
                for t, short, hrs in TIMES:
                    self.w(f'<th class="num">{short}<small>{hrs}</small></th>')
            self.w('</tr></thead><tbody>')
            def key(item):
                sp, r = item
                return -sum(r["t"].values())
            for sp, r in sorted(rows.items(), key=key):
                spr, name, types = self.species_chip(sp)
                lv = f'{r["min"]}' if r["min"] == r["max"] else f'{r["min"]}–{r["max"]}'
                self.w(f'<tr><td><span class="mon">{spr}<span><b>{esc(name)}</b>{types}</span></span></td><td class="num">{lv}</td>')
                if same:
                    self.w(f'<td class="num">{self.pct(r["t"].get("Morning", 0))}</td>')
                else:
                    for t, _, _ in TIMES:
                        v = r["t"].get(t, 0)
                        self.w(f'<td class="num{" zero" if not v else ""}">{self.pct(v) if v else "—"}</td>')
                self.w('</tr>')
            self.w('</tbody></table></div>')
        self.w('<p class="fine">Times are the in-game clock: morning 6–10, day 10–19, evening 19–20, night 20–6.</p></div>')

    @staticmethod
    def pct(v):
        return f"{v:.0f}%" if v >= 1 else f"{v:.1f}%"

    def statics_block(self, a):
        st = a.get("statics") or []
        if not st:
            return
        self.w('<div class="block statics"><h4>Special encounters and trades</h4><ul class="statlist">')
        for s in st:
            spr, name, types = self.species_chip(s.get("species", ""), big=False)
            lv = f'Lv. {s["level"]}' if s.get("level") else ""
            self.w(f'<li>{spr}<div><b>{esc(name)}</b> <span class="lv">{lv}</span>{types}<br>'
                   f'<span class="where">{esc(s.get("where", ""))}</span><br>{esc(s.get("condition", ""))}</div></li>')
        self.w('</ul></div>')

    def party_html(self, t, show_moves=False):
        out = ['<ul class="party">']
        for mon in t["mons"]:
            spr, name, types = self.species_chip(mon["species"])
            extra = ""
            if mon.get("item"):
                extra += f'<span class="held">{esc(mon["item"])}</span>'
            moves = ""
            if show_moves and mon["moves"]:
                moves = '<span class="moves">' + " · ".join(esc(m) for m in mon["moves"]) + "</span>"
            out.append(f'<li>{spr}<span class="pm"><b>{esc(name)}</b><span class="lv">Lv. {mon["level"]}</span>'
                       f'{types}{extra}{moves}</span></li>')
        out.append("</ul>")
        return "".join(out)

    def trainer_block(self, a, trainers, numbering):
        hier = (a.get("hierophant") or {}).get("trainer")
        hier_ids = {hier, re.sub(r"_DAY$", "_NIGHT", hier or "")}
        rows = [t for t in trainers if t["tid"] not in hier_ids]
        # rival/admin variants: collapse starter variants into one card
        if not rows:
            return
        self.w('<div class="block"><h4>Trainers</h4><div class="cards">')
        groups = {}
        for t in rows:
            key = re.sub(r"_(KYNDER|HIPLING|NEBREL)$", "", t["tid"])
            groups.setdefault(key, []).append(t)
        for key, ts in groups.items():
            t0 = ts[0]
            tr = self.g.trainer(t0["tid"])
            if not tr:
                self.missing.append(f"{a['id']}: trainer {t0['tid']} has no party")
                continue
            self.counts["trainers"] += 1
            n = numbering.get(id(t0))
            prize = self.g.prize(tr)
            name = tr["head"].get("Name", "").title()
            cls = self.g.class_name(tr)
            self.w(f'<article class="tcard" id="t-{slug(t0["tid"])}">')
            for extra in ts[1:]:
                self.w(f'<span id="t-{slug(extra["tid"])}"></span>')
            self.w('<header>')
            self.w(f'<span class="mk trn sm">{n if n else "★"}</span>')
            self.w(f'<span class="tn"><small>{esc(cls)}</small><b>{esc(name)}</b></span>')
            if prize:
                self.w(f'<span class="prize">¥{prize:,}</span>')
            self.w('</header>')
            if len(ts) > 1:
                for t in ts:
                    st = t["tid"].rsplit("_", 1)[1].title()
                    trv = self.g.trainer(t["tid"])
                    self.w(f'<p class="variant">If you chose <b>{esc(st)}</b>:</p>')
                    self.w(self.party_html(trv))
            else:
                self.w(self.party_html(tr))
            if len(self.g.trainers.get(t0["tid"], {})) > 1:
                self.w('<p class="fine">Hero difficulty shown. Mortal is 3 levels lower; Spartan has trained sets.</p>')
            if not n:
                self.w('<p class="fine">No fixed spot: battled during an event.</p>')
            self.w('</article>')
        self.w('</div></div>')

    def hierophant(self, a):
        h = a["hierophant"]
        tr = self.g.trainer(h["trainer"])
        variants = self.g.trainers.get(h["trainer"], {})
        self.w(f'<div class="hiero" id="{slug(a["id"])}-hierophant">')
        self.w('<div class="hiero-band"><span>Hierophant</span><span>' + esc(h.get("laurel", "")) + '</span></div>')
        self.w('<div class="hiero-body">')
        self.w(f'<h4><small>{esc(h.get("title", ""))}</small>{esc(h.get("name", ""))}</h4>')
        ty = h.get("type", "")
        self.w(f'<p class="hmeta"><i class="ty" style="--t:{TYPE_COLORS.get(ty.upper(), "#888")}">{esc(ty)}</i>'
               f' {("<span>Prize ¥" + format(self.g.prize(tr), ",") + "</span>") if tr else ""}</p>')
        if h.get("before"):
            self.w(f'<p class="before"><b>Before the battle.</b> {esc(h["before"])}</p>')
        teams = []
        if h["trainer"].endswith("_DAY") and h["trainer"][:-4] + "_NIGHT" in self.g.trainers:
            teams = [("Day team", h["trainer"]), ("Night team", h["trainer"][:-4] + "_NIGHT")]
        else:
            teams = [("Team", h["trainer"])]
        for lab, tid in teams:
            t = self.g.trainer(tid)
            if not t:
                continue
            self.w(f'<h5>{esc(lab)} <small>Hero</small></h5>')
            self.w(self.party_html(t, show_moves=True))
            for dn in ("Mortal", "Spartan"):
                tv = self.g.trainers.get(tid, {}).get(dn)
                if tv:
                    lv = "/".join(str(m["level"]) for m in tv["mons"])
                    self.w(f'<p class="fine"><b>{dn}:</b> levels {lv}'
                           f'{"; held items " + ", ".join(sorted(set(m["item"] for m in tv["mons"] if m.get("item")))) if any(m.get("item") for m in tv["mons"]) else ""}'
                           f'{"; natures " + ", ".join(m["nature"] for m in tv["mons"] if m.get("nature")) if any(m.get("nature") for m in tv["mons"]) else ""}.</p>')
        if h.get("strategy"):
            self.w('<div class="strat"><h5>Strategy</h5>')
            for p in h["strategy"]:
                self.w(f'<p>{esc(p)}</p>')
            self.w('</div>')
        rw = h.get("rewards") or []
        self.w('<div class="rewards"><h5>Rewards</h5><p>')
        self.w(f'<span class="laurel">{esc(h.get("laurel", ""))}</span>')
        for r in rw:
            self.w(self.item_chip(r))
        self.w('</p>')
        if h.get("unlocks"):
            self.w(f'<p class="fine">{esc(h["unlocks"])}</p>')
        self.w('</div></div></div>')

    def checklist(self, aid, a, items, npcs):
        rows = []
        for p in items:
            rows.append((f'{p["map"]}:{p["x"]},{p["y"]}', self.item_chip(p["item"], p.get("qty", 1)),
                         ("Hidden" if p["kind"] == "hidden" else "Item ball") +
                         (f' · {self.map_title(p["map"])}' if p["map"] != a["maps"][0] else "")))
        for n in npcs:
            for i, q in gifts_of(self.g, n.get("map"), n.get("script", "")):
                rows.append((f'{n.get("map")}:{n.get("script")}:{i}', self.item_chip(i, q),
                             f'From {n.get("label", "")}'))
        if not rows:
            return
        self.counts["items"] += len(rows)
        self.w(f'<details class="block check" open><summary><h4>Item checklist</h4>'
               f'<span class="count" data-count="{aid}">0/{len(rows)}</span></summary><ul class="checks" data-area="{aid}">')
        for key, chip, src in rows:
            k = esc(key)
            self.w(f'<li><label><input type="checkbox" data-k="{k}"><span>{chip}<small>{esc(src)}</small></span></label></li>')
        self.w('</ul></details>')

    def shops_block(self, a):
        shops = a.get("shops") or []
        if not shops:
            return
        self.w('<div class="block"><h4>Agora stalls</h4>')
        for s in shops:
            items = "".join(f'<li>{self.item_chip(i)}<span class="num">{self.price(i)}</span></li>' for i in s.get("items", []))
            when = f' <span class="dim">{esc(s.get("when", ""))}</span>' if s.get("when") else ""
            self.w(f'<div class="shop"><h5>{esc(s.get("where", ""))}{when}</h5><ul class="shoplist">{items}</ul></div>')
        self.w('</div>')

    def price(self, const):
        text = self.g.items.get(const)
        p = self._prices.get(const) if hasattr(self, "_prices") else None
        return f"¥{p:,}" if p else ""

    def tips_block(self, a):
        tips = a.get("tips") or []
        if not tips:
            return
        self.w('<div class="tips">')
        for t in tips:
            k = t.get("kind", "Hot Tip")
            cls = {"Hot Tip": "hot", "Pro Tip": "pro", "Lore": "lore"}.get(k, "hot")
            self.w(f'<aside class="tip {cls}"><b>{esc(k)}</b><p>{esc(t.get("text", ""))}</p></aside>')
        self.w('</div>')

    def puzzles_block(self, a):
        for pz in a.get("puzzles") or []:
            self.w(f'<div class="puzzle"><h4><span>Puzzle</span>{esc(pz.get("title", ""))}</h4>')
            self.w(f'<details><summary>Show a hint</summary><p>{esc(pz.get("hint", ""))}</p>'
                   f'<details class="inner"><summary>Show the full solution</summary><p>{esc(pz.get("solution", ""))}</p></details></details></div>')

    def spoilers_block(self, a):
        sps = a.get("spoilers") or []
        if not sps:
            return
        self.w('<div class="spoilers"><h4>Story notes <small>spoilers inside</small></h4>')
        for s in sps:
            self.w(f'<details class="spoiler"><summary>{esc(s.get("title", "Spoiler"))}</summary><p>{esc(s.get("text", ""))}</p></details>')
        self.w('</div>')


# --- build ---------------------------------------------------------------------

CSS = r"""
:root{
  --paper:#f1ece2; --paper2:#e7dfd0; --ink:#1d1814; --ink2:#4a4038; --mute:#7a6d60;
  --clay:#b4532a; --clay2:#d9774a; --clayink:#ffffff; --black:#1b1612; --blackfg:#e9a273;
  --sea:#1f5672; --seabg:#dfe9ee; --gold:#a8781c; --rule:#cdbfa8; --card:#fbf8f2;
  --hot:#b4532a; --hotbg:#f6e3d6; --pro:#1f5672; --probg:#dde8ee; --lore:#6b5a2a; --lorebg:#efe8d2;
  --mk-item:#b4532a; --mk-trn:#1b1612; --mk-npc:#1f5672; --shadow:0 1px 0 rgba(0,0,0,.06);
  color-scheme:light;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#171310; --paper2:#211b16; --ink:#efe3cf; --ink2:#cdbca3; --mute:#9b8b77;
    --clay:#d9774a; --clay2:#e9935f; --clayink:#1b1612; --black:#0d0a08; --blackfg:#e9935f;
    --sea:#7fb2cf; --seabg:#16232b; --gold:#d6a84a; --rule:#3a3028; --card:#1f1914;
    --hot:#e9935f; --hotbg:#2b1d15; --pro:#7fb2cf; --probg:#15212a; --lore:#d6bf7a; --lorebg:#26211a;
    --mk-item:#d9774a; --mk-trn:#efe3cf; --mk-npc:#7fb2cf; color-scheme:dark;
  }
}
:root[data-theme="dark"]{
    --paper:#171310; --paper2:#211b16; --ink:#efe3cf; --ink2:#cdbca3; --mute:#9b8b77;
    --clay:#d9774a; --clay2:#e9935f; --clayink:#1b1612; --black:#0d0a08; --blackfg:#e9935f;
    --sea:#7fb2cf; --seabg:#16232b; --gold:#d6a84a; --rule:#3a3028; --card:#1f1914;
    --hot:#e9935f; --hotbg:#2b1d15; --pro:#7fb2cf; --probg:#15212a; --lore:#d6bf7a; --lorebg:#26211a;
    --mk-item:#d9774a; --mk-trn:#efe3cf; --mk-npc:#7fb2cf; color-scheme:dark;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:64px}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 "Barlow","Helvetica Neue",Arial,sans-serif;
  font-variant-numeric:tabular-nums;-webkit-text-size-adjust:100%}
.wrap{max-width:1080px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-bottom:64px}
h1,h2,h3,h4,h5,.kicker,.tabs a,figcaption,summary,.mk,.prize,.tn small,.hiero-band,th{font-family:"Barlow Condensed","Arial Narrow",Arial,sans-serif}
a{color:var(--clay)}
.key{height:14px;margin:0 -16px;background:
 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='14' viewBox='0 0 28 14'%3E%3Cpath d='M0 13h14V3H6v6h4V7H8V5h4v6H2V1h18v12h8' fill='none' stroke='%23b4532a' stroke-width='2'/%3E%3C/svg%3E") repeat-x center/28px 14px}
/* cover */
.cover{background:var(--black);color:#efe3cf;margin:0 calc(-1 * max(16px,env(safe-area-inset-left,0px)));padding:28px max(16px,env(safe-area-inset-left,0px)) 22px;position:relative;overflow:hidden}
.cover .eyebrow{font:600 13px/1 "Barlow Condensed",sans-serif;letter-spacing:.22em;text-transform:uppercase;color:var(--blackfg)}
.cover h1{font-size:clamp(44px,11vw,92px);line-height:.88;margin:10px 0 6px;letter-spacing:-.01em;text-transform:uppercase;font-weight:800;color:#e9935f}
.cover h1 span{display:block;color:#efe3cf;font-size:.42em;letter-spacing:.06em;font-weight:600;margin-top:8px}
.cover p{max-width:56ch;color:#cdbca3;margin:12px 0 0}
.cover .meta{display:flex;gap:18px;flex-wrap:wrap;margin-top:18px;font:600 14px "Barlow Condensed",sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#9b8b77}
.cover .meta b{color:#efe3cf;font-size:20px;display:block}
/* tabs */
.tabs{position:sticky;top:0;z-index:20;background:var(--paper);border-bottom:2px solid var(--ink);margin:0 calc(-1 * max(16px,env(safe-area-inset-left,0px)));padding:0 max(16px,env(safe-area-inset-left,0px));display:flex;gap:2px;overflow-x:auto;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tabs a{flex:none;display:flex;align-items:baseline;gap:6px;padding:10px 12px 8px;text-decoration:none;color:var(--ink2);font-weight:600;font-size:15px;letter-spacing:.04em;text-transform:uppercase;border-bottom:4px solid transparent;margin-bottom:-2px}
.tabs a b{font-size:20px;color:var(--clay)}
.tabs a.on{color:var(--ink);border-color:var(--clay)}
.tabs .theme{margin-left:auto;background:none;border:0;color:var(--ink2);font:600 14px "Barlow Condensed",sans-serif;text-transform:uppercase;letter-spacing:.06em;padding:10px 6px;cursor:pointer}
/* toc */
.toc{margin:26px 0 8px;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px 28px}
.toc h2{grid-column:1/-1;font-size:30px;text-transform:uppercase;margin:0;letter-spacing:.02em}
.toc section h3{margin:0 0 6px;font-size:18px;text-transform:uppercase;letter-spacing:.05em;border-bottom:2px solid var(--ink);padding-bottom:3px;display:flex;gap:8px;align-items:baseline}
.toc section h3 b{color:var(--clay);font-size:22px}
.toc ol{list-style:none;margin:0;padding:0}
.toc li{display:flex;justify-content:space-between;gap:8px;border-bottom:1px dotted var(--rule);padding:4px 0}
.toc li a{color:var(--ink);text-decoration:none}
.toc li a:hover{color:var(--clay)}
.toc li span{color:var(--mute);font:600 12px "Barlow Condensed",sans-serif;text-transform:uppercase;letter-spacing:.08em}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;margin:18px 0 0;padding:12px 14px;border:2px solid var(--ink);background:var(--card);font-size:14px}
.legend b{font-family:"Barlow Condensed",sans-serif;text-transform:uppercase;letter-spacing:.08em;width:100%}
.legend span{display:inline-flex;align-items:center;gap:6px}
/* chapter */
.chapter{margin-top:44px}
.ch-head{background:var(--black);color:#efe3cf;padding:22px 18px 18px;position:relative}
.ch-head .no{font:800 64px/0.8 "Barlow Condensed",sans-serif;color:#e9935f;float:left;margin:0 16px 0 0}
.ch-head h2{margin:0;font-size:clamp(26px,6vw,40px);line-height:1;text-transform:uppercase;letter-spacing:.01em}
.ch-head p{margin:6px 0 0;color:#cdbca3;max-width:60ch}
.ch-head::after{content:"";display:block;clear:both}
/* area */
.area{margin-top:34px;padding-top:4px;border-top:6px solid var(--ink)}
.area-head .kicker{margin:10px 0 0;display:flex;gap:8px;font-size:13px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:var(--clay)}
.area-head .soon{color:var(--sea)}
.area h3{font:800 clamp(30px,7vw,46px)/0.95 "Barlow Condensed",sans-serif;margin:4px 0 6px;text-transform:uppercase;letter-spacing:-.005em}
.blurb{margin:0 0 10px;color:var(--ink2);font-size:17px;max-width:62ch}
.steps p{margin:0 0 10px;padding-left:34px;position:relative;max-width:70ch}
.stepn{position:absolute;left:0;top:1px;width:24px;height:24px;background:var(--ink);color:var(--paper);font:700 14px/24px "Barlow Condensed",sans-serif;text-align:center}
h4{font-size:22px;text-transform:uppercase;letter-spacing:.03em;margin:22px 0 8px;line-height:1.1}
h5{font-size:17px;text-transform:uppercase;letter-spacing:.05em;margin:14px 0 6px}
.block{margin-top:6px}
/* maps */
.mapfig{margin:18px 0 10px;border:2px solid var(--ink);background:var(--card)}
.mapfig figcaption{display:flex;justify-content:space-between;gap:8px;background:var(--ink);color:var(--paper);padding:5px 10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;font-size:15px}
.mapfig .dim{opacity:.7;font-weight:500}
.mapgrid{display:grid;grid-template-columns:minmax(0,max-content) minmax(220px,1fr);align-items:start}
.mapgrid>*{min-width:0}
.mapfig,.area,.chapter,.block,.tips,.cards{min-width:0;max-width:100%}
.mapscroll{overflow:auto;max-height:640px;background:var(--paper2);border-right:2px solid var(--ink);-webkit-overflow-scrolling:touch}
.mapwrap{position:relative;max-width:none}
.mapwrap img{display:block;width:100%;height:100%;image-rendering:pixelated;image-rendering:crisp-edges}
.mk{display:inline-flex;align-items:center;justify-content:center;min-width:20px;height:20px;padding:0 4px;font:700 13px/1 "Barlow Condensed",sans-serif;color:#fff;background:var(--mk-item);border:2px solid #fff;border-radius:50%;box-shadow:0 1px 2px rgba(0,0,0,.45)}
.mapwrap .mk{position:absolute;transform:translate(-50%,-50%);z-index:2}
.mk.hid{background:#fff;color:#b4532a;border:2px dashed #b4532a}
.mk.trn{background:#1b1612;border-radius:2px;color:#fff}
.mk.npc{background:#1f5672;border-radius:3px;transform-origin:center}
.mapwrap .mk.npc{transform:translate(-50%,-50%)}
.mk.sm{flex:none}
.keylist{list-style:none;margin:0;padding:8px 10px;max-height:640px;overflow:auto;font-size:14.5px}
.keylist li{display:flex;gap:8px;align-items:flex-start;padding:5px 0;border-bottom:1px dotted var(--rule)}
.keylist li:last-child{border-bottom:0}
.keylist li>div{min-width:0}
.keylist a{color:var(--ink);font-weight:600}
.tag{font:700 11px "Barlow Condensed",sans-serif;text-transform:uppercase;letter-spacing:.1em;color:#b4532a;border:1px solid currentColor;padding:0 4px;margin-left:2px}
.gifts{display:flex;flex-wrap:wrap;gap:4px 10px;margin-top:2px}
.where{color:var(--mute);font-size:13px}
.indoors{margin-top:8px}
.indoors .keylist{max-height:none;border:2px solid var(--ink);background:var(--card)}
/* chips */
.itm{display:inline-flex;align-items:center;gap:4px;font-weight:600;white-space:nowrap}
.ico{width:24px;height:24px;flex:none;background:no-repeat center/24px 24px;image-rendering:pixelated}
.ico.none{background:var(--rule);border-radius:50%;width:10px;height:10px;margin:7px}
.spr{width:48px;height:48px;flex:none;background:no-repeat center/contain;image-rendering:pixelated}
.spr.big{width:64px;height:64px}
.spr.none{background:var(--paper2);border-radius:50%}
.ty{display:inline-block;font:700 10.5px/1.5 "Barlow Condensed",sans-serif;font-style:normal;text-transform:uppercase;letter-spacing:.08em;color:#fff;background:var(--t);padding:0 5px;margin:0 3px 0 0;border-radius:2px}
.mon{display:flex;align-items:center;gap:6px}
.mon b{display:block;font-weight:600}
/* tables */
.tblscroll{overflow-x:auto;margin:8px 0 12px;border:2px solid var(--ink);background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:14.5px}
caption{caption-side:top;text-align:left;font:700 15px "Barlow Condensed",sans-serif;text-transform:uppercase;letter-spacing:.08em;padding:6px 10px;background:var(--clay);color:var(--clayink)}
th{font-weight:700;text-transform:uppercase;letter-spacing:.06em;font-size:13px;text-align:left;padding:5px 8px;border-bottom:2px solid var(--ink);white-space:nowrap}
th small{display:block;font-weight:500;color:var(--mute);letter-spacing:.02em}
td{padding:3px 8px;border-bottom:1px solid var(--rule)}
tr:last-child td{border-bottom:0}
.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.zero{color:var(--mute)}
.fine{font-size:13px;color:var(--mute);margin:4px 0}
/* trainer cards */
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.tcard{border:2px solid var(--ink);background:var(--card);padding:0 0 6px}
.tcard header{display:flex;align-items:center;gap:8px;padding:6px 8px;border-bottom:2px solid var(--ink);background:var(--paper2)}
.tn{display:flex;flex-direction:column;line-height:1.05;min-width:0}
.tn small{font-size:12px;text-transform:uppercase;letter-spacing:.12em;color:var(--clay);font-weight:700}
.tn b{font:800 20px "Barlow Condensed",sans-serif;text-transform:uppercase;letter-spacing:.02em}
.prize{margin-left:auto;font-weight:700;font-size:17px;color:var(--gold)}
.party{list-style:none;margin:0;padding:4px 8px}
.party li{display:flex;align-items:center;gap:6px;padding:2px 0}
.pm{display:flex;flex-wrap:wrap;align-items:baseline;gap:2px 8px;min-width:0}
.pm b{font-weight:600}
.lv{font-weight:700;font-size:13px;color:var(--ink2)}
.held{font-size:12.5px;color:var(--mute)}
.held::before{content:"@ "}
.moves{flex-basis:100%;font-size:12.5px;color:var(--ink2)}
.variant{margin:6px 8px 0;font-size:13px;color:var(--ink2)}
.tcard .fine{padding:0 8px}
/* hierophant spread */
.hiero{margin:24px 0 10px;border:3px solid var(--ink);background:var(--card)}
.hiero-band{display:flex;justify-content:space-between;gap:8px;background:var(--black);color:#e9935f;padding:8px 14px;font-weight:800;font-size:16px;text-transform:uppercase;letter-spacing:.22em;border-bottom:4px solid #b4532a}
.hiero-band span+span{color:#efe3cf;letter-spacing:.08em}
.hiero-body{padding:4px 16px 14px}
.hiero h4{font-size:clamp(34px,8vw,54px);line-height:.9;margin:12px 0 4px}
.hiero h4 small{display:block;font-size:15px;letter-spacing:.16em;color:var(--clay);margin-bottom:6px}
.hmeta{display:flex;gap:12px;align-items:center;margin:0 0 6px;font:700 15px "Barlow Condensed",sans-serif;color:var(--gold)}
.hmeta .ty{font-size:13px;padding:1px 8px}
.before{border-left:4px solid var(--clay);padding-left:10px}
.hiero .party{border:2px solid var(--ink);padding:6px 10px;background:var(--paper)}
.hiero .party .spr{width:64px;height:64px}
.strat p{max-width:70ch}
.laurel{display:inline-flex;align-items:center;gap:6px;font:800 16px "Barlow Condensed",sans-serif;text-transform:uppercase;letter-spacing:.08em;color:var(--clay);margin-right:14px}
.laurel::before{content:"";width:22px;height:14px;background:
 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 22 14'%3E%3Cg fill='%235f9a46'%3E%3Cellipse cx='4' cy='9' rx='3' ry='1.6' transform='rotate(-35 4 9)'/%3E%3Cellipse cx='7' cy='5' rx='3' ry='1.6' transform='rotate(-55 7 5)'/%3E%3Cellipse cx='18' cy='9' rx='3' ry='1.6' transform='rotate(35 18 9)'/%3E%3Cellipse cx='15' cy='5' rx='3' ry='1.6' transform='rotate(55 15 5)'/%3E%3C/g%3E%3C/svg%3E") no-repeat center/contain}
.rewards p{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:center}
/* checklist */
.check{border:2px solid var(--ink);background:var(--card);margin-top:16px}
.check summary{display:flex;align-items:center;gap:10px;padding:4px 10px;cursor:pointer;list-style:none;background:var(--paper2)}
.check summary::-webkit-details-marker{display:none}
.check summary h4{margin:4px 0;font-size:19px}
.count{margin-left:auto;font:700 16px "Barlow Condensed",sans-serif;color:var(--clay)}
.checks{list-style:none;margin:0;padding:6px 10px;columns:2 240px;column-gap:18px}
.checks li{break-inside:avoid;padding:3px 0}
.checks label{display:flex;gap:8px;align-items:flex-start;cursor:pointer}
.checks input{margin-top:5px;accent-color:var(--clay);width:17px;height:17px;flex:none}
.checks label>span{display:flex;flex-direction:column}
.checks small{color:var(--mute);font-size:12.5px;padding-left:28px;margin-top:-2px}
.checks input:checked+span .itm{text-decoration:line-through;opacity:.55}
/* shops */
.shop h5{margin:10px 0 4px}
.shop h5 .dim{color:var(--mute);font-weight:500;letter-spacing:.02em;text-transform:none;font-family:"Barlow",sans-serif;font-size:14px}
.shoplist{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:4px 18px}
/* tips */
.tips{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin-top:18px}
.tip{padding:10px 12px 8px;border-left:6px solid var(--hot);background:var(--hotbg)}
.tip b{font:800 15px "Barlow Condensed",sans-serif;text-transform:uppercase;letter-spacing:.14em;color:var(--hot)}
.tip p{margin:2px 0 0;font-size:15px}
.tip.pro{border-color:var(--pro);background:var(--probg)}
.tip.pro b{color:var(--pro)}
.tip.lore{border-color:var(--lore);background:var(--lorebg)}
.tip.lore b{color:var(--lore)}
/* puzzles and spoilers */
.puzzle{margin-top:16px;border:2px dashed var(--ink);padding:2px 12px 8px}
.puzzle h4{display:flex;gap:10px;align-items:baseline;font-size:20px;margin:10px 0 6px}
.puzzle h4 span{font-size:13px;letter-spacing:.16em;background:var(--ink);color:var(--paper);padding:2px 6px}
details summary{cursor:pointer;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--clay);font-size:15px}
details p{margin:6px 0}
details.inner{margin-top:6px}
details.inner summary{color:var(--sea)}
.spoilers{margin-top:16px}
.spoilers h4 small{font-size:13px;letter-spacing:.12em;color:var(--mute);margin-left:6px}
.spoiler{border:2px solid var(--ink);background:var(--card);padding:6px 12px;margin:6px 0}
.statlist{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px}
.statlist li{display:flex;gap:8px;border:2px solid var(--ink);background:var(--card);padding:6px 8px;font-size:14.5px}
footer.colophon{margin-top:56px;padding-top:14px;border-top:2px solid var(--ink);color:var(--mute);font-size:13px}
.totop{position:fixed;right:max(14px,env(safe-area-inset-right,0px));bottom:max(14px,env(safe-area-inset-bottom,0px));z-index:30;background:var(--ink);color:var(--paper);text-decoration:none;font:700 14px "Barlow Condensed",sans-serif;text-transform:uppercase;letter-spacing:.1em;padding:8px 12px}
@media (max-width:720px){
  .mapgrid{grid-template-columns:minmax(0,1fr)}
  .mapscroll{border-right:0;border-bottom:2px solid var(--ink);max-height:70vh}
  .keylist{max-height:none}
  .ch-head .no{font-size:48px}
}
"""

JS = r"""
(function(){
  var root=document.documentElement;
  function get(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function set(k,v){try{if(v===null)localStorage.removeItem(k);else localStorage.setItem(k,v)}catch(e){}}
  var th=get('ichor-guide:theme'); if(th) root.setAttribute('data-theme',th);
  var btn=document.querySelector('.theme');
  if(btn){btn.addEventListener('click',function(){
    var cur=root.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
    var nx=cur==='dark'?'light':'dark'; root.setAttribute('data-theme',nx); set('ichor-guide:theme',nx);});}
  function recount(ul){
    var a=ul.getAttribute('data-area'); var bx=ul.querySelectorAll('input'); var n=0;
    bx.forEach(function(b){if(b.checked)n++});
    var c=document.querySelector('[data-count="'+a+'"]'); if(c)c.textContent=n+'/'+bx.length;
  }
  document.querySelectorAll('.checks').forEach(function(ul){
    ul.querySelectorAll('input').forEach(function(b){
      var k='ichor-guide:got:'+b.getAttribute('data-k'); if(get(k)==='1') b.checked=true;
      b.addEventListener('change',function(){set(k,b.checked?'1':null);recount(ul);});
    });
    recount(ul);
  });
  var tabs=[].slice.call(document.querySelectorAll('.tabs a[href^="#ch"]'));
  var chs=tabs.map(function(a){return document.getElementById(a.getAttribute('href').slice(1))});
  function onScroll(){var y=window.scrollY+90,on=-1;chs.forEach(function(c,i){if(c&&c.offsetTop<=y)on=i});
    tabs.forEach(function(t,i){t.classList.toggle('on',i===on)});}
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();
})();
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("-o", "--out", default=str(ROOT / "build/guide/ichor_walkthrough.html"))
    args = ap.parse_args()

    g = Game()
    ims = Images(g)
    page = Page(g, ims)
    page._prices = {}
    text = (ROOT / "src/data/items.h").read_text()
    for m in re.finditer(r"\[(ITEM_\w+)\]\s*=\s*\{", text):
        pr = re.search(r"\.price\s*=\s*(\d+)", text[m.end():m.end() + 400])
        if pr:
            page._prices[m.group(1)] = int(pr.group(1))

    chapters = []
    later = []
    for cid, tab, title, fname, intro in CHAPTERS:
        data = json.loads((HERE / "content" / fname).read_text())
        areas = []
        for a in data["areas"]:
            (later if a["id"] in NOT_YET else areas).append(a)
        chapters.append((cid, tab, title, intro, areas, False))
    coming = []
    for aid, title, maps, kind, blurb in COMING_UP:
        coming.append({"id": aid, "title": title, "maps": maps, "kind": kind, "blurb": blurb})
    for a in later:
        a = dict(a)
        a["blurb"] = (a.get("blurb", "") + " Built, but not reachable in the current version.").strip()
        coming.append(a)
    chapters.append(("ch5", "→", "Coming Up", "The next stretch past Thyrsa, from the game data alone. "
                     "Prose for these areas comes when they are fully connected.", coming, True))

    for cid, tab, title, intro, areas, soon in chapters:
        page.toc.append((cid, title, []))
        page.w(f'<div class="chapter" id="{cid}"><div class="ch-head"><span class="no">{esc(tab)}</span>'
               f'<h2>{esc(title)}</h2><p>{esc(intro)}</p></div><div class="key"></div>')
        for a in areas:
            page.area(cid, a, coming=soon)
        page.w('</div>')

    body = "\n".join(page.parts)
    toc = ['<nav class="toc" aria-label="Contents"><h2>Contents</h2>']
    for (cid, title, items), (_, tab, *_r) in zip(page.toc, chapters):
        toc.append(f'<section><h3><b>{esc(tab)}</b><a href="#{cid}" style="color:inherit;text-decoration:none">{esc(title)}</a></h3><ol>')
        for aid, t, kind in items:
            toc.append(f'<li><a href="#{aid}">{esc(t)}</a><span>{esc(kind)}</span></li>')
        toc.append('</ol></section>')
    toc.append('</nav>')
    legend = ('<div class="legend"><b>Map key</b>'
              '<span><span class="mk item">1</span>Item ball</span>'
              '<span><span class="mk hid">2</span>Hidden item</span>'
              '<span><span class="mk trn">3</span>Trainer</span>'
              '<span><span class="mk npc">4</span>Key person or place</span></div>')
    tabs = ['<nav class="tabs" aria-label="Chapters">']
    for cid, tab, title, *_ in chapters:
        short = title.split(":")[-1].strip()
        tabs.append(f'<a href="#{cid}"><b>{esc(tab)}</b>{esc(short)}</a>')
    tabs.append('<a href="#contents" style="display:none"></a><button class="theme" type="button">Light / Dark</button></nav>')

    cover = ('<header class="cover"><div class="eyebrow">Pokémon Ichor · Official-style Player\'s Guide</div>'
             '<h1>Field Guide<span>Kalliste to the Mask Laurel</span></h1>'
             '<p>Every map, item, trainer and wild Pokémon from the start of your journey to Thyrsa, area by area, '
             'in story order. Puzzle answers and story twists stay folded away until you ask for them.</p>'
             f'<div class="meta"><span><b>4</b>Laurels</span><span><b>{page.counts["areas"]}</b>Areas</span>'
             f'<span><b>{page.counts["trainers"]}</b>Trainers</span><span><b>{page.counts["items"]}</b>Items to find</span></div>'
             '</header>')

    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,400;0,600;0,700;1,400&'
             'family=Barlow+Condensed:wght@500;600;700;800&display=swap" rel="stylesheet">')
    out = "\n".join([
        "<title>Ichor Field Guide</title>",
        '<meta name="claude:viewport-fit-sides" content="cover">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        fonts,
        "<style>" + CSS + "\n" + ims.stylesheet() + "</style>",
        '<div class="wrap" id="contents">',
        cover,
        "".join(tabs),
        "".join(toc),
        legend,
        body,
        '<footer class="colophon">Built from the game files by tools/ichor/guide/build_walkthrough.py. '
        'Trainer parties show Hero difficulty unless marked. Prize money is the base amount before any money-boosting item.</footer>',
        '</div><a class="totop" href="#contents">Contents</a>',
        "<script>" + JS + "</script>",
    ])
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(out)
    size = outp.stat().st_size
    print(f"{outp}  {size / 1e6:.2f} MB  areas={page.counts['areas']} maps={page.counts['maps']} "
          f"trainers={page.counts['trainers']} items={page.counts['items']}")
    for m in page.missing:
        print("missing:", m)


if __name__ == "__main__":
    main()
