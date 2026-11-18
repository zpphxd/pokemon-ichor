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

from labyrinth_lib import PITCH, cell, gap, mid, setmetatiles

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


def remains(m, x, y, prefix, tag, text, item=None, flag=None):
    m.sign(x, y, prefix + f"Remains{tag}")
    if item:
        m.hidden(x, y, item, flag)
    s = ["", f"script {prefix}Remains{tag} {{", f"    msgbox(format(\"{text}\"), MSGBOX_SIGN)", "}"]
    m.extra_scripts = getattr(m, "extra_scripts", []) + s
    m.lost_log = getattr(m, "lost_log", [])
    m.lost_log.append((tag, (x, y), text, item))
