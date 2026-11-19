#!/usr/bin/env python3
"""Build Poseidon's two-floor tide-pool quest and the capital's sea exit."""
import struct
import sys

from thyrsa import ROOT, Map, bg, const, obj, read, warp, write

sys.path.insert(0, str(ROOT / "tools/ichor/art"))
import cave_dark_kit as kit
import plan_hook  # noqa: E402  (tools/ichor/wild_plan.py)

CAT = read("data/tilesets/secondary/cave_dark/catalog.json")
PIECES = {p["key"]: p["ids"] for p in CAT["pieces"]}


def item(m, x, y, item, flag):
    e = obj("", x, y, "Common_EventScript_FindItem", flag="FLAG_ICHOR_" + flag)
    e.pop("local_id")
    e.update(graphics_id="OBJ_EVENT_GFX_ITEM_BALL", trainer_sight_or_berry_tree_id="ITEM_" + item)
    m.json["object_events"].append(e)


def hidden(m, x, y, item, flag):
    m.json["bg_events"].append(dict(type="hidden_item", x=x, y=y, elevation=0,
        item="ITEM_" + item, flag="FLAG_ICHOR_" + flag, quantity=1, underfoot=False))


def cave(name, lower=False):
    m = Map(name, 30, 30)
    grid = [["#"] * m.w for _ in range(m.h)]

    def rect(x0, y0, x1, y1, ch="."):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                grid[y][x] = ch

    if lower:
        for r in ((3, 4, 8, 9), (6, 5, 19, 8), (16, 7, 19, 19),
                  (11, 12, 24, 16), (4, 12, 8, 17), (7, 14, 16, 16),
                  (14, 18, 26, 26)):
            rect(*r)
        rect(13, 18, 26, 22, "~")
        rect(15, 17, 18, 17)
        rect(15, 23, 24, 26)
        rect(19, 23, 27, 24, "~")
        rect(17, 23, 19, 25)
    else:
        for r in ((3, 4, 8, 10), (6, 9, 21, 12), (18, 5, 25, 10),
                  (11, 11, 17, 13), (13, 12, 15, 23), (10, 19, 24, 26),
                  (5, 21, 12, 25)):
            rect(*r)
        rect(9, 14, 19, 17, "~")
        rect(12, 16, 12, 16)
    tiles = kit.autotile(["".join(r) for r in grid], CAT, "wet")
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            m.put(x, y, tile, grid[y][x] == "#")
            if grid[y][x] == "~":
                m.cells[y * m.w + x] = tile | 0x1000
    m.put(5, 5, PIECES["hole_down"][0][0])
    m.json.update(allow_cycling=False, allow_escaping=True, requires_flash=lower)
    m.json["warp_events"] = [warp(5, 5, "SaltWell_B1F" if lower else "Astyra_Akropolis", 1)]
    if not lower:
        m.put(21, 24, PIECES["hole_down"][0][0])
        m.json["warp_events"].append(warp(21, 24, "SaltWell_B2F", 0))
        m.rect(5, 8, 7, 9, 0x157)
        item(m, 7, 9, "HYPER_POTION", "ITEM_SALT_WELL_HEAL")
        item(m, 24, 6, "BIG_PEARL", "ITEM_SALT_WELL_PEARL")
        hidden(m, 6, 24, "SHOAL_SALT", "HIDDEN_SALT_WELL_SALT")
        hidden(m, 23, 25, "HEART_SCALE", "HIDDEN_SALT_WELL_SCALE")
        m.person("Glaukos", 12, 16, gfx="PILGRIM", facing="RIGHT", sight=3)
        m.person("Kymothoe", 22, 7, gfx="ACOLYTE_F", facing="LEFT", sight=1)
        m.json["bg_events"] += [bg(12, 13, m.prefix + "Tide"),
                                bg(4, 7, m.prefix + "Shallows")]
        m.put(12, 13, PIECES["stele"][0][0], True)
        m.person("Rest", 8, 22, gfx="ELDER_M")
    else:
        m.json["bg_events"] += [bg(15, 17, m.prefix + "Tide"),
                                bg(14, 8, m.prefix + "Brazier")]
        # the tide stele marks the shore, and stepping onto the shore offers the backwash too
        m.put(15, 17, PIECES["stele"][0][0], True)
        for x in (16, 17):
            m.json["coord_events"].append(dict(type="trigger", x=x, y=17, elevation=0,
                var="VAR_TEMP_2", var_value="0", script=m.prefix + "TideStep"))
        m.stamp(14, 8, PIECES["brazier_cold"])
        m.person("Halia", 5, 14, gfx="ACOLYTE_F", facing="RIGHT", sight=1)
        item(m, 5, 16, "ETHER", "ITEM_SALT_WELL_ETHER")
        item(m, 23, 14, "SHOAL_SHELL", "ITEM_SALT_WELL_SHELL")
        hidden(m, 12, 12, "PEARL", "HIDDEN_SALT_WELL_PEARL")
        hidden(m, 24, 25, "REVIVE", "HIDDEN_SALT_WELL_REVIVE")
        m.put(18, 22, 0x157)
        m.person("Dolphin", 18, 22, flag="FLAG_ICHOR_GOT_POSEIDONS_CONCH")
        m.json["object_events"][-1]["graphics_id"] = "OBJ_EVENT_GFX_SPECIES(FINIZEN)"
        m.person("Alethea", 19, 25, gfx="ALETHEA", flag="FLAG_ICHOR_HIDE_ALETHEA_SALT_WELL")
        m.put(25, 23, 0x0E0, True)
        m.json["coord_events"].append(dict(type="trigger", x=26, y=23, elevation=0,
            var="VAR_TEMP_1", var_value="0", script=m.prefix + "SeaDoor"))
    m.save()
    layouts = read("data/layouts/layouts.json")
    layout = next(l for l in layouts["layouts"] if l.get("id") == m.json["layout"])
    layout["secondary_tileset"] = "gTileset_CaveDark"
    write("data/layouts/layouts.json", layouts)
    border = kit.kit_id(CAT, "T|...", "wet") | 0x3400
    (ROOT / f"data/layouts/{name}/border.bin").write_bytes(struct.pack("<4H", *([border] * 4)))


def harbor():
    m = Map("Astyra_Harbor", 32, 24)
    m.cells = [0x1170] * (m.w * m.h)
    m.rect(0, 0, 7, 23, 0x0E0, True)
    m.rect(18, 0, 31, 10, 0x1D9)
    m.rect(20, 10, 29, 17, 0x1D9)
    m.rect(16, 12, 25, 14, 0x1D9)
    m.put(26, 3, 0x1DB)
    m.json["warp_events"] = [warp(26, 3, "Astyra", 5)]
    m.sign("SeaDoor", 7, 12, tile=0x0E0)
    m.sign("Sign", 27, 4)
    m.person("Mariner", 25, 12, gfx="PILGRIM")
    item(m, 28, 16, "ULTRA_BALL", "ITEM_ASTYRA_HARBOR")
    hidden(m, 19, 9, "SHOAL_SALT", "HIDDEN_ASTYRA_HARBOR_SALT")
    hidden(m, 20, 17, "HEART_SCALE", "HIDDEN_ASTYRA_HARBOR_SCALE")
    m.save()


def encounters_and_teams():
    wild = read("src/data/wild_encounters.json")
    group = next(g for g in wild["wild_encounter_groups"] if g.get("for_maps"))
    names = ("SaltWell_B1F", "SaltWell_B2F", "Astyra_Harbor")
    group["encounters"] = [e for e in group["encounters"] if e.get("map") not in
                           {"MAP_" + const(n) for n in names}]
    species = ("GALENYON", "KARKITOX", "NARKERAY", "SEISMARE")
    for name in names:
        level = 34 if name == "Astyra_Harbor" else (36 if name.endswith("B1F") else 37)
        entry = dict(map="MAP_" + const(name), base_label="g" + name)
        for field, count in (("land_mons", 12), ("water_mons", 5), ("fishing_mons", 10)):
            if field == "land_mons" and name == "Astyra_Harbor":
                continue
            entry[field] = dict(encounter_rate=10 if field == "land_mons" else 6,
                mons=[dict(min_level=level, max_level=min(39, level + 2),
                           species="SPECIES_" + species[i % 4]) for i in range(count)])
        group["encounters"].append(entry)
    plan_hook.apply(group["encounters"])  # the distribution pass has the last word (design/DISTRIBUTION.md)
    write("src/data/wild_encounters.json", wild)
    path = ROOT / "src/data/trainers.party"
    start, end = "/* Salt Well teams. */", "/* End Salt Well teams. */"
    before, _, old = path.read_text().partition(start)
    after = old.partition(end)[2]
    text = before.rstrip() + "\n\n" + start + "\n"
    for name, party in (("GLAUKOS", [("Galenyon", 36)]),
                        ("KYMOTHOE", [("Narkeray", 37), ("Karkitox", 37)]),
                        ("HALIA", [("Karkitox", 38), ("Galenyon", 38)])):
        pic = "Pilgrim" if name == "GLAUKOS" else "Acolyte F"
        gender = "Male" if name == "GLAUKOS" else "Female"
        text += (f"\n=== TRAINER_ICHOR_SALT_WELL_{name} ===\nName: {name}\n"
                 f"Class: Pilgrim\nPic: {pic}\nGender: {gender}\nMusic: Male\nAI: Basic Trainer\n")
        for species, level in party:
            text += (f"\n{species}\nLevel: {level}\n"
                     "IVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe\n")
    path.write_text(text + "\n" + end + after + ("" if after else "\n"))


if __name__ == "__main__":
    cave("SaltWell_B1F")
    cave("SaltWell_B2F", True)
    harbor()
    encounters_and_teams()
