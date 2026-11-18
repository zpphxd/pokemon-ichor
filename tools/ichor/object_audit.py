#!/usr/bin/env python3
"""Audit where people stand: no object event inside a wall, a tree or a column.

  tools/ichor/object_audit.py               every Ichor map (exit 1 on any hit)
  tools/ichor/object_audit.py Arkadia ...   these maps, or name prefixes
  tools/ichor/object_audit.py --crops DIR   also write a render of each hit (red: the object)

An overworld person is a 16x32 sprite: its feet are on its cell and its head on
the cell above. It fails when

  SOLID   its own cell has collision, or a behavior nobody stands on (water,
          a ledge, a waterfall): it was placed inside a wall, a tree or a rock
  COVERED its own cell's top layer covers its chest (a tree's crown, an arch):
          a counter in front may hide the legs, but no more
  HEAD    the cell above draws top-layer art over its head

Skipped, because they stand there on purpose:
  - props, not people (PROPS: item balls, cut trees, herms, plaques, statues...)
  - staging spots: an object hidden by a flag that its map's script moves
    (setobjectxy or applymovement) before it is seen
  - *_PERCH local ids, which emporion.py perches on counters and gate posts
  - ALLOWED below: each one looked at in a render, with the reason

Fix a hit where its generator places it (tools/ichor/maps/*.py, or map.json for
hand-placed people); add to ALLOWED only what a render shows is meant.

Reads map.json, each layout's map.bin and each tileset's metatiles,
attributes and tiles (tools/ichor/render_map.py's loader). Run by
tools/ichor/smoke_test.sh.
"""
import argparse
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mapdata import NEVER_STAND, NUM_PRIMARY, UPSTREAM_PREFIXES, WATER, Repo, is_berry_tree, is_item_ball, is_obstacle  # noqa: E402
import render_map  # noqa: E402

LAYER_NORMAL, LAYER_COVERED, LAYER_SPLIT = 0, 1, 2
COVER_PIXELS = 16  # top-layer pixels over the head or chest before it counts

# Deliberate placements on solid cells, each looked at in a render: (map, local id or script).
ALLOWED = {
    ("KallisteRoute1", "KallisteRoute1_EventScript_WallYouth"): "sits on the field wall",
    ("TriremeEuploia_Deck", "LOCALID_DECK_NEST_HATCHING"): "the halcyon nest floats on the sea",
    ("TriremeEuploia_Deck", "LOCALID_DECK_NEST_EGGS"): "the halcyon nest floats on the sea",
    ("TriremeEuploia_Deck", "LOCALID_DECK_NEST_EMPTY"): "the halcyon nest floats on the sea",
    ("TriremeEuploia_Hold", "LOCALID_HOLD_LAKONIAN"): "seated at an oar bench",
    ("TriremeEuploia_Hold", "LOCALID_HOLD_ROWER_1"): "seated at an oar bench",
    ("TriremeEuploia_Hold", "LOCALID_HOLD_ROWER_2"): "seated at an oar bench",
    ("TriremeEuploia_Hold", "LOCALID_HOLD_ROWER_3"): "seated at an oar bench",
    ("StyxFalls_Inn", "LOCALID_STYX_INN_GRYLLOS"): "a gift Pokemon among the jars",
    ("AeginaTown_Mint", "LOCALID_AEGINA_MINT_CHELONET"): "a trade Pokemon on the counter",
    ("EmporionCity_Deigma", "LOCALID_EMPORION_DEIGMA_NARKERAY"): "a trade Pokemon in the tank",
    ("EmporionCity_Hephaisteion", "LOCALID_EMPORION_HEPHAISTEION_KEDALION"): "at the forge",
    ("ThyrsaCity_MaskWorkshop", "LOCALID_MASK_WORKSHOP_MASK"): "a mask Pokemon on the wall rack",
    ("KytheraSkandeia_DiversHouse", "LOCALID_SKANDEIA_ANKYRA"): "a trade Pokemon in the tank",
    ("KytheraSkandeia_Asclepeion", "KytheraSkandeia_Asclepeion_EventScript_Panacoil"): "the staff's snake on the counter",
    ("KytheraPaphia_PottersHouse", "LOCALID_PAPHIA_POTHOS"): "a trade Pokemon by the kiln",
    ("KytheraPaphia_PottersHouse", "LOCALID_PAPHIA_GALENYON"): "a trade Pokemon by the kiln",
    ("Delphoi_TempleOfApollo", "LOCALID_APOLLO_PYTHIA"): "the Pythia on her tripod",
    ("EleusaVillage_Farmhouse", "LOCALID_ELEUSA_FARMHOUSE_GALEKIT"): "a pet among the grain jars",
    ("EleusaVillage_Asclepeion", "LOCALID_ELEUSA_ASCLEPEION_PANACOIL"): "coiled round the garden's gate post (eleusa_rooms.py)",
    ("Lakonia", "Lakonia_EventScript_Augur"): "reads the birds from a roof (lakonia_town.py marks it _floats)",
    ("ThyrsaCity", "LOCALID_THYRSA_PROITID_GUARD"): "stands in the Proitid Gate under its lintel",
    ("Gytheion", "LOCALID_GYTHEION_STALLKEEPER"): "inside the stall, under its awning",
    ("Arkadia_TempleOfArtemis", "LOCALID_ARKADIA_TEMPLE_OF_ARTEMIS_HOUNDMASTER2"): "a hound patrolling under the grove's crowns",
    **{("Lakonia", f"LOCALID_LAKONIA_RING_CADET_{i}"): "the cadets on the ring's wall (III-5I)"
       for i in range(1, 6)},
    **{("LakeStymphalia", f"LOCALID_LAKE_STYMPHALIA_BIRD{i}"): "the birds roost in the reeds"
       for i in range(1, 7)},
    **{("EmporionCity_GreatDeigma", f"LOCALID_EMPORION_GREAT_DEIGMA_{n}"): "a keeper behind the stall's wares"
       for n in ("AMASIS", "SKYLES", "PETRAIOS", "MELIA", "KALLIAS", "PHORMION", "SPICER", "POTTER")},
}
# Graphics that are props, not people: they stand on solid cells by design.
PROPS = ("ITEM_BALL", "BERRY_TREE", "CUTTABLE_TREE", "BREAKABLE_ROCK", "PUSHABLE_BOULDER",
         "HERM", "PLAQUE", "STATUE", "PILLAR", "STELE", "ALTAR", "BRAZIER", "SIGN", "TRUCK",
         "BOAT", "SHIP", "TRIREME", "INVISIBLE", "LIGHT", "DOOR", "CHEST", "URN", "KRATER",
         "BIRTH_ISLAND_STONE", "MOVING_BOX", "CUSHION", "DOLL", "FOSSIL", "BALL_", "_ROCK",
         "APRICORN", "SHRINE", "LOOM", "MIRROR", "TABLET", "CRACK")


class Tiles:
    """Per tileset pair: a 16x16 mask of the pixels each metatile draws above objects."""

    def __init__(self, repo):
        render_map.read_fieldmap_constants()
        self.repo = repo
        self.symbols = render_map.scan_tileset_symbols()
        self.sets, self.masks = {}, {}

    def tileset(self, sym):
        if sym not in self.sets:
            self.sets[sym] = render_map.Tileset(render_map.resolve_tileset(sym, self.symbols))
        return self.sets[sym]

    def top_mask(self, layout, m, mid):
        key = (layout["primary_tileset"], layout["secondary_tileset"], mid)
        if key in self.masks:
            return self.masks[key]
        attrs = m.prim if mid < NUM_PRIMARY else m.sec
        i = mid if mid < NUM_PRIMARY else mid - NUM_PRIMARY
        mask = np.zeros((16, 16), bool)
        if i < len(attrs) and (attrs[i] >> 12) in (LAYER_NORMAL, LAYER_SPLIT):
            prim = self.tileset(layout["primary_tileset"])
            sec = self.tileset(layout["secondary_tileset"])
            table = prim.metatiles if mid < NUM_PRIMARY else sec.metatiles
            if i < len(table):
                entries = table[i]
                top = (render_map.TILES_PER_METATILE // 4 - 1) * 4
                for k in range(4):
                    e = int(entries[top + k])
                    idx, hflip, vflip = e & 0x3FF, e >> 10 & 1, e >> 11 & 1
                    if idx < render_map.NUM_TILES_IN_PRIMARY:
                        src = prim.tiles[idx] if idx < len(prim.tiles) else None
                    else:
                        j = idx - render_map.NUM_TILES_IN_PRIMARY
                        src = sec.tiles[j] if j < len(sec.tiles) else None
                    if src is None:
                        continue
                    if hflip:
                        src = src[:, ::-1]
                    if vflip:
                        src = src[::-1, :]
                    y, x = (k // 2) * 8, (k % 2) * 8
                    mask[y:y + 8, x:x + 8] |= src != 0
        self.masks[key] = mask
        return mask


def is_prop(o):
    g = o.get("graphics_id", "")
    return (is_item_ball(o) or is_berry_tree(o) or is_obstacle(o)
            or any(p in g for p in PROPS))


def staged(repo, name, o):
    """Hidden by a flag until its map's script moves it into place: a staging spot."""
    lid = o.get("local_id")
    if not lid or o.get("flag") in (None, "", "0", 0):
        return False
    return re.search(rf"(setobjectxy|setobjectxyperm|applymovement)\s*\(?\s*{lid}\b",
                     repo.script_text(name)) is not None


def audit_map(repo, tiles, name):
    m = repo.map(name)
    layout = repo.layouts[m.json["layout"]]
    hits = []
    for n, o in enumerate(m.objects, 1):
        ident = o.get("local_id") or o.get("script")
        # *_PERCH objects are perched on purpose by their generator (emporion.py's
        # stall keepers and gate hoplites, the harbor herald).
        if (is_prop(o) or (name, ident) in ALLOWED or str(ident).endswith("_PERCH")
                or staged(repo, name, o)):
            continue
        x, y = int(o["x"]), int(o["y"])
        who = f"{name} #{n} {o.get('local_id') or o.get('script')} ({o['graphics_id']}) at ({x},{y})"
        c = m.cell(x, y)
        if c is None:
            continue  # off-map placeholders are moved by scripts before they show
        b = m.behavior(c[0])
        if c[1] or b in NEVER_STAND or (b in WATER and "SURF" not in o.get("graphics_id", "")
                                         and "SPECIES" not in o.get("graphics_id", "")):
            hits.append(("SOLID", who, f"metatile 0x{c[0]:03X} collision {c[1]} {b}"))
        # A counter in front may hide the legs (the lower rows of its own cell);
        # art over the chest or the head is a placement mistake.
        if tiles.top_mask(layout, m, c[0])[:6].sum() >= COVER_PIXELS:
            hits.append(("COVERED", who, f"metatile 0x{c[0]:03X} draws over its body"))
        above = m.cell(x, y - 1)
        if above and tiles.top_mask(layout, m, above[0])[6:].sum() >= COVER_PIXELS:
            hits.append(("HEAD", who, f"metatile 0x{above[0]:03X} above draws over its head"))
    return hits


def crop(repo, tiles, name, x0, y0, path, rad=4):
    """The cells around an object: lower layers, then the map's people as bars
    (red for this one), then the top layer over them, as the game draws it."""
    from PIL import Image
    m = repo.map(name)
    layout = repo.layouts[m.json["layout"]]
    r = render_map.Renderer(tiles.tileset(layout["primary_tileset"]), tiles.tileset(layout["secondary_tileset"]))
    w = 2 * rad + 1
    img = np.zeros((w * 16, w * 16, 3), np.uint8)
    img[:] = r.backdrop
    tops = []
    for j in range(w):
        for i in range(w):
            c = m.cell(x0 - rad + i, y0 - rad + j)
            if not c:
                continue
            prim = c[0] < NUM_PRIMARY
            table = (r.p if prim else r.s).metatiles
            k = c[0] if prim else c[0] - NUM_PRIMARY
            attrs = m.prim if prim else m.sec
            if k >= len(table):
                continue
            over = k < len(attrs) and (attrs[k] >> 12) in (LAYER_NORMAL, LAYER_SPLIT)
            for layer in range(render_map.TILES_PER_METATILE // 4):
                for q in range(4):
                    t = r.tile(int(table[k][layer * 4 + q]))
                    at = (j * 16 + (q // 2) * 8, i * 16 + (q % 2) * 8, t)
                    if over and layer == render_map.TILES_PER_METATILE // 4 - 1:
                        tops.append(at)
                    else:
                        _blit(img, *at)
    for o in m.objects:
        ox, oy = int(o["x"]) - x0 + rad, int(o["y"]) - y0 + rad
        if 0 <= ox < w and 0 <= oy < w:
            img[max(0, oy * 16 - 12):oy * 16 + 16, ox * 16 + 3:ox * 16 + 13] = \
                (255, 0, 0) if (ox, oy) == (rad, rad) else (255, 0, 255)
    for at in tops:
        _blit(img, *at)
    Image.fromarray(img).resize((w * 32, w * 32), Image.NEAREST).save(path)


def _blit(img, y, x, t):
    region = img[y:y + 8, x:x + 8]
    region[:] = np.where(t[..., 3:] > 0, t[..., :3], region)


def ichor_maps(repo):
    return [n for n in repo.names if not n.startswith(UPSTREAM_PREFIXES)
            and (repo.root / f"data/maps/{n}/scripts.pory").exists()]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("maps", nargs="*")
    ap.add_argument("--crops", help="write a render around each hit to this directory")
    args = ap.parse_args()
    repo = Repo()
    tiles = Tiles(repo)
    names = ichor_maps(repo)
    if args.maps:
        names = [n for n in repo.names if any(n == p or n.startswith(p) for p in args.maps)]
    hits = []
    for name in names:
        hits += audit_map(repo, tiles, name)
    for kind, who, why in hits:
        print(f"{kind:8} {who}: {why}")
    if args.crops:
        Path(args.crops).mkdir(parents=True, exist_ok=True)
        for kind, who, why in hits:
            name, xy = who.split(" ")[0], re.search(r"at \((\d+),(\d+)\)", who)
            crop(repo, tiles, name, int(xy.group(1)), int(xy.group(2)),
                 Path(args.crops) / f"{kind}_{name}_{xy.group(1)}_{xy.group(2)}.png")
    print(f"object_audit: {len(names)} maps, {len(hits)} hits")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
