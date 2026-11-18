#!/usr/bin/env python3
"""The Temple of Apollo: the Pythian Light (design/maps/Delphoi_TempleOfApollo.md;
SCRIPT.md III-6D and Part 5). 19 x 47, on oikos + temple_apollo; and the
Omphalos stair (III-8), 14 x 40.

South to north: the pronaos (teach: M1 sends the window's sun onto disc 0);
four chambers behind bronze screens, one beam from the smoke-hole passed on
(test: chamber 1, M2 to disc 1 then through door 1; chamber 2, M3 to disc 2
on the east wall, then west to M3b and through door 2; chamber 3, round the
serpent pillar with M4 and M5 to disc 3 in the screen, then through door 3;
chamber 4, M6 to disc 4 at the stair head, then up the stair); the adyton
(master: M7 and M8 focus the beam on the brazier, and its fire is carried
round the vents to the tripod).

Mirror facings are in the clockwise order down, left, up, right (a turn is
one step). The puzzle's geometry is here; the scripts are
data/maps/Delphoi_TempleOfApollo/scripts.pory.

  /usr/bin/python3 tools/ichor/maps/delphoi_temple.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from delphoi_maps import DMap, npc, trainer  # noqa: E402

NAME = "Delphoi_TempleOfApollo"
S = "Delphoi_TempleOfApollo_EventScript_"
W, H = 19, 47
MAT = (0x006, 0x007)

# (local id, x, y, initial facing)
MIRRORS = [("M1", 4, 43, "up"), ("M2", 9, 37, "down"), ("M3", 9, 30, "up"), ("M3B", 5, 30, "left"),
           ("M4", 5, 24, "down"), ("M5", 2, 24, "left"), ("M6", 2, 15, "down"), ("M7", 12, 15, "down"),
           ("M8", 12, 8, "up")]
# where each mirror ends once the rite is solved (and stays, bolted, after the Laurel)
SOLVED = {"M1": "right", "M2": "up", "M3": "left", "M3B": "up", "M4": "left", "M5": "up", "M6": "right",
          "M7": "up", "M8": "right"}
# disc markers: invisible objects the beam ends on. Disc 4 sits on the stair's
# gate itself, so its marker is hidden (its flag) once lit and the gate opens.
DISCS = [("DISC_0", 18, 43), ("DISC_1", 0, 37), ("DISC_2", 18, 30), ("DISC_3", 2, 26), ("DISC_4", 12, 11)]
# which gate each disc opens
DISC_GATE = {"DISC_0": "inner", "DISC_1": "door1", "DISC_2": "door2", "DISC_3": "door3", "DISC_4": "stair"}
GATES = {"inner": (9, 40), "door1": (9, 33), "door2": (5, 26), "door3": (2, 18), "stair": (12, 11)}
SCREEN_ROWS = (11, 18, 26, 33, 40)
VENTS = [(x, 7) for x in range(5, 14)] + [(x, 5) for x in range(1, 18) if x != 7]
BRAZIER = (16, 8)
CLOCKWISE = ["down", "left", "up", "right"]
TRIPOD = (7, 2)            # 3 x 2


def build():
    m = DMap(NAME, "temple_apollo", W, H, fill=0, primary="oikos")
    T = lambda key, name, x, y, solid=None: m.piece(key, name, x, y, solid)  # noqa: E731
    for y in range(H):
        for x in range(1, W - 1):
            T("floor", "floor" if (x + y) % 5 else "floor2", x, y, False)
        T("wall", "side_W", 0, y, True)
        T("wall", "side_E", W - 1, y, True)
    # the adyton's back wall, rock floor, tripod, brazier and vents
    for x in range(1, W - 1):
        T("wall", "top" if x % 3 else "top2", x, 0, True)
        T("wall", "wall" if x % 4 else "pilaster", x, 1, True)
    for y in range(2, 11):
        for x in range(1, W - 1):
            T("adyton", ("rock", "rock2", "rock3", "rock4")[(x * 3 + y * 5) % 4], x, y, False)
    m.part("adyton", "tripod_TL", TRIPOD[0], TRIPOD[1], 3, 2)
    for x in range(TRIPOD[0], TRIPOD[0] + 3):
        for y in (TRIPOD[1], TRIPOD[1] + 1):
            m.solid[y, x] = True
    T("props", "chasm", 6, 2, True)
    T("props", "chasm", 10, 3, True)
    T("props", "brazier", *BRAZIER, True)
    for (x, y) in VENTS:
        T("props", "vent", x, y, False)
    # the screens between the chambers, their gates and discs
    for y in SCREEN_ROWS:
        for x in range(1, W - 1):
            T("screen", "grille", x, y, True)
    for (x, y) in GATES.values():
        T("screen", "shut", x, y, True)
    T("screen", "disc", 2, 26, True)
    # the side walls' discs, the window, the inscription
    for (_k, x, y) in DISCS:
        if x in (0, W - 1):
            T("wall", "disc", x, y, True)
    T("wall", "window", 0, 43, True)
    # the steps from the stair head down into the adyton
    T("props", "steps", 12, 10, False)
    # chamber 1 (rows 34-39): tripods of old victories down both sides, the smoke-hole's light
    for (x, y) in ((3, 35), (15, 35), (3, 39), (15, 39), (6, 35), (12, 35)):
        T("props", "tripod_top", x, y - 1, False)
        T("props", "tripod", x, y, True)
    T("floor", "light", 9, 37, False)
    # chamber 2 (rows 27-32): lyres and kitharas; Pherenike's aisle behind a screen
    for y in range(27, 32):
        T("screen", "grille", 3, y, True)
    for (x, y) in ((15, 28), (17, 28), (15, 32), (17, 32), (12, 32)):
        T("props", "lyre" if (x + y) % 2 else "kithara", x, y, True)
    # chamber 3 (rows 19-25): the bronze serpent round its pillar
    m.part("props", "serpent_TL", 5, 20, 2, 2)
    for (x, y) in ((5, 20), (6, 20), (5, 21), (6, 21)):
        m.solid[y, x] = True
    for (x, y) in ((11, 20), (15, 20), (11, 23), (15, 23)):
        T("props", "tripod_top", x, y - 1, False)
        T("props", "tripod", x, y, True)
    # chamber 4 (rows 12-17): laurels in rows
    for (x, y) in ((7, 14), (10, 14), (13, 14), (16, 14), (7, 17), (10, 17), (13, 17), (16, 17)):
        T("props", "laurel_top", x, y - 1, False)
        T("props", "laurel", x, y, True)
    # the pronaos: the exit mat
    m.set(9, 46, MAT[0], False)
    events(m)
    m.border = [0, 0, 0, 0]
    m.header = {"ichor_kind": "dungeon"}
    return m


def facing(f):
    return {"down": "MOVEMENT_TYPE_ICHOR_MIRROR", "up": "MOVEMENT_TYPE_ICHOR_MIRROR_UP",
            "left": "MOVEMENT_TYPE_ICHOR_MIRROR_LEFT", "right": "MOVEMENT_TYPE_ICHOR_MIRROR_RIGHT"}[f]


def events(m):
    m.warp(9, 46, "MAP_DELPHOI", 0)
    for (k, x, y, f) in MIRRORS:
        e = m.obj("ICHOR_MIRROR", x, y, S + "Mirror", move=facing(f), local_id=f"LOCALID_APOLLO_{k}")
        e["_floats"] = False
    for (k, x, y) in DISCS:
        e = m.obj("ICHOR_MIRROR_MARK", x, y, "0x0", move="MOVEMENT_TYPE_INVISIBLE",
                  local_id=f"LOCALID_APOLLO_{k}",
                  flag="FLAG_ICHOR_APOLLO_DISC_4" if k == "DISC_4" else "0")
        e["_floats"] = True
    e = m.obj("ICHOR_MIRROR_MARK", BRAZIER[0], BRAZIER[1], "0x0", move="MOVEMENT_TYPE_INVISIBLE",
              local_id="LOCALID_APOLLO_BRAZIER")
    e["_floats"] = True
    # the people
    npc(m, "ICHOR_KID_M", 13, 45, S + "Eudoros", face="left", local_id="LOCALID_APOLLO_EUDOROS")
    trainer(m, "ICHOR_ACOLYTE_M", 10, 41, S + "Onomakritos", "left", 3)
    trainer(m, "ICHOR_PRIESTESS", 1, 28, S + "Pherenike", "up", 1, local_id="LOCALID_APOLLO_PHERENIKE")
    trainer(m, "ICHOR_PRIESTESS", 4, 12, S + "Bremousa", "left", 3)
    e = npc(m, "ICHOR_PRIESTESS", 8, 3, S + "Pythia", face="down", flag="FLAG_ICHOR_HIDE_PHEMONOE_TRIPOD",
            local_id="LOCALID_APOLLO_PYTHIA")
    e["_floats"] = True
    # things to read: the brazier, the tripod, the vents (coord events that douse)
    m.sign(BRAZIER[0], BRAZIER[1], S + "Brazier")
    m.sign(TRIPOD[0] + 1, TRIPOD[1] + 1, S + "Tripod")
    for (x, y) in VENTS:
        m.trigger(x, y, S + "Vent", "VAR_TEMP_9", 1)
    for (k, (x, y)) in GATES.items():
        m.sign(x, y, S + "Gate")
    m.item_ball(17, 3, "ITEM_FULL_RESTORE", "FLAG_ICHOR_ITEM_APOLLO_FULL_RESTORE")
    m.hidden(1, 10, "ITEM_HEAL_POWDER", "FLAG_ICHOR_HIDDEN_ITEM_APOLLO_HEAL_POWDER")
    m.hidden(17, 25, "ITEM_STARDUST", "FLAG_ICHOR_HIDDEN_ITEM_APOLLO_STARDUST")


# ==========================================================================
# The Omphalos stair (III-8): 14 x 40, down from the cracked stone to the Loom
# ==========================================================================

STAIR = "Delphoi_OmphalosStair"
LOOM = ("MAP_THE_LOOM", 0)     # the Loom's east door (tools/ichor/maps/climax.py)


def build_stair():
    w, h = 14, 40
    m = DMap(STAIR, "temple_apollo", w, h, fill=0, primary="oikos")
    import random
    rnd = random.Random(28)
    for y in range(h):
        for x in range(w):
            r = rnd.random()
            m.piece("stair", "rock_crack" if r < 0.06 else "roots" if r < 0.10 else "rock", x, y, True)
    # It switchbacks: five flights and four landings, each landing a little
    # wider than the last, the way cut more roughly as it goes down.
    flights = [((3, 4), 1, 7), ((8, 9), 10, 15), ((3, 4), 18, 21), ((9, 10), 25, 30), ((9, 10), 33, 38)]
    landings = [(3, 9, 8, 9), (3, 9, 16, 17), (3, 11, 22, 24), (5, 11, 31, 32)]
    for (xs, y0, y1) in flights:
        for y in range(y0, y1 + 1):
            for x in xs:
                worn = (y + x) % 5 == 0 and y > 9
                m.piece("stair", "steps_worn" if worn else "steps", x, y, False)
    for (x0, x1, y0, y1) in landings:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                m.piece("stair", "landing", x, y, False)
    # the rock's lip over every landing, so the walls read as walls
    for (x0, x1, y0, y1) in landings:
        for x in range(x0, x1 + 1):
            if m.solid[y0 - 1, x]:
                m.piece("stair", "rock_lip", x, y0 - 1, True)
    # side niches: a lamp niche on each landing, offering pots, old bones
    m.piece("stair", "niche", 6, 7, True)
    m.piece("stair", "pots", 10, 15, True)
    m.piece("stair", "niche", 5, 21, True)
    m.piece("stair", "pots", 11, 21, True)
    m.piece("stair", "niche", 8, 30, True)
    m.piece("stair", "bones", 3, 24, False)
    m.piece("stair", "bones", 6, 32, False)
    # the gold thread, picked up on the second landing, runs down to the bottom
    for (x, y) in ((8, 16), (8, 17)):
        m.piece("stair", "thread", x, y, False)
    for y in range(18, 22):
        m.piece("stair", "thread", 4, y, False)
    for y in range(25, 31):
        m.piece("stair", "thread", 10, y, False)
    for y in range(33, 38):
        m.piece("stair", "thread", 10, y, False)
    m.piece("stair", "torch", 8, 12, False)
    m.piece("stair", "knot", 9, 28, False)
    m.piece("stair", "carving", 11, 36, True)
    for x in (3, 4):
        m.piece("stair", "way_up", x, 1, False)
        m.warp(x, 1, "MAP_DELPHOI", 0)   # back up: out by the temple door, over the court
    # The Loom is the climax chapter's map (III-9). Until it lands, the bottom
    # step is a dark way down that brings you back up (LOOM below).
    for x in (9, 10):
        m.piece("stair", "way_down", x, 38, False)
        m.warp(x, 38, LOOM[0], LOOM[1])
    # the music box's tick: every third step near the top, every second lower down
    ticks = [(x, y) for (xs, y0, y1) in flights[:3] for y in range(y0 + 2, y1 + 1, 3) for x in xs]
    ticks += [(x, y) for (xs, y0, y1) in flights[3:] for y in range(y0, y1, 2) for x in xs]
    for (x, y) in ticks:
        if (x, y) not in ((8, 12), (9, 28)):
            m.trigger(x, y, STAIR + "_EventScript_Tick", "VAR_TEMP_0", 0)
    m.sign(8, 12, STAIR + "_EventScript_Torch")
    m.sign(9, 28, STAIR + "_EventScript_Knot")
    m.sign(11, 36, STAIR + "_EventScript_Carving")
    m.sign(5, 21, STAIR + "_EventScript_Niche")
    m.sign(10, 15, STAIR + "_EventScript_Pots")
    # what pilgrims and Hyperion left on the way down
    m.item_ball(9, 8, "ITEM_MAX_ETHER", "FLAG_ICHOR_ITEM_OMPHALOS_STAIR")
    m.hidden(3, 8, "ITEM_REVIVE", "FLAG_ICHOR_HIDDEN_ITEM_OMPHALOS_STAIR_1")
    m.hidden(5, 32, "ITEM_HYPER_POTION", "FLAG_ICHOR_HIDDEN_ITEM_OMPHALOS_STAIR_2")
    m.border = [0, 0, 0, 0]
    # A scripted descent with no encounters and no fights (the Gigas are
    # beaten at the top): measured as a passage, not a dungeon floor. The
    # Loom below it is the dungeon (the climax chapter's).
    m.header = {"ichor_kind": "interior"}
    return m


def gen_scripts(m):
    """The generated half of the temple's scripts.pory: metatile ids, each
    mirror's turn, the trace after it, and the restore on load. The rite's own
    words and people are the hand-written half."""
    s = m.s
    mid = lambda key, name: s(key)["ids"][s(key)["names"][name][1]][s(key)["names"][name][0]]  # noqa: E731
    L = ["// delphoi_temple: begin generated (tools/ichor/maps/delphoi_temple.py; don't edit)", ""]
    L.append(f"const METATILE_APOLLO_BEAM_EW = 0x{mid('beam', 'EW'):03X}")
    L.append(f"const METATILE_APOLLO_MOONBEAM_EW = 0x{mid('moonbeam', 'EW'):03X}")
    L.append(f"const METATILE_APOLLO_WALL_DISC_LIT = 0x{mid('wall', 'disc_lit'):03X}")
    L.append(f"const METATILE_APOLLO_SCREEN_DISC_LIT = 0x{mid('screen', 'disc_lit'):03X}")
    L.append(f"const METATILE_APOLLO_GATE_OPEN = 0x{mid('screen', 'open'):03X}")
    L.append(f"const METATILE_APOLLO_BRAZIER_LIT = 0x{mid('props', 'brazier_lit'):03X}")
    for n in ("TL", "TC", "TR", "BL", "BC", "BR"):
        L.append(f"const METATILE_APOLLO_TRIPOD_LIT_{n} = 0x{mid('adyton', 'tripod_lit_' + n):03X}")
    L.append("")
    temps = {k: f"VAR_TEMP_{i + 1}" for i, (k, *_r) in enumerate(MIRRORS)}
    # the beam's metatiles: gold by day, silver by night
    L += ["script Delphoi_TempleOfApollo_EventScript_BeamKind {",
          "    specialvar(VAR_RESULT, Ichor_GetTimeOfDay)",
          "    if (var(VAR_RESULT) == TIME_NIGHT) {",
          "        setvar(VAR_0x8005, METATILE_APOLLO_MOONBEAM_EW)",
          "    } else {",
          "        setvar(VAR_0x8005, METATILE_APOLLO_BEAM_EW)",
          "    }",
          "    return", "}", ""]
    # set every mirror's facing from its var (after a load, a reset, or the Laurel)
    L.append("script Delphoi_TempleOfApollo_EventScript_ApplyFacings {")
    for (k, x, y, f) in MIRRORS:
        L.append(f"    call(Delphoi_TempleOfApollo_EventScript_Face{k})")
    L += ["    return", "}", ""]
    for (k, x, y, f) in MIRRORS:
        var, lid = temps[k], f"LOCALID_APOLLO_{k}"
        L.append(f"script Delphoi_TempleOfApollo_EventScript_Face{k} {{")
        L.append(f"    switch (var({var})) {{")
        for i, d in enumerate(CLOCKWISE):
            dirc = {"down": "DIR_SOUTH", "left": "DIR_WEST", "up": "DIR_NORTH", "right": "DIR_EAST"}[d]
            mt = {"down": "MOVEMENT_TYPE_ICHOR_MIRROR", "left": "MOVEMENT_TYPE_ICHOR_MIRROR_LEFT",
                  "up": "MOVEMENT_TYPE_ICHOR_MIRROR_UP", "right": "MOVEMENT_TYPE_ICHOR_MIRROR_RIGHT"}[d]
            L += [f"        case {i}:", f"            turnobject({lid}, {dirc})",
                  f"            setobjectmovementtype({lid}, {mt})"]
        L += ["    }", "    return", "}", ""]
    # the initial and solved facings
    L.append("script Delphoi_TempleOfApollo_EventScript_InitialFacings {")
    for (k, x, y, f) in MIRRORS:
        L.append(f"    setvar({temps[k]}, {CLOCKWISE.index(f)})")
    L += ["    return", "}", ""]
    L.append("script Delphoi_TempleOfApollo_EventScript_SolvedFacings {")
    for (k, x, y, f) in MIRRORS:
        L.append(f"    setvar({temps[k]}, {CLOCKWISE.index(SOLVED[k])})")
    L += ["    return", "}", ""]
    # a mirror's turn: one step clockwise, then trace its beam
    L.append("script Delphoi_TempleOfApollo_EventScript_TurnTalked {")
    L.append("    switch (var(VAR_LAST_TALKED)) {")
    for (k, x, y, f) in MIRRORS:
        var = temps[k]
        L += [f"        case LOCALID_APOLLO_{k}:", f"            addvar({var}, 1)",
              f"            if (var({var}) >= 4) {{", f"                setvar({var}, 0)", "            }",
              f"            call(Delphoi_TempleOfApollo_EventScript_Face{k})"]
    L += ["    }", "    if (var(VAR_LAST_TALKED) == LOCALID_APOLLO_M1) {",
          "        call(Delphoi_TempleOfApollo_EventScript_TracePronaos)",
          "    } else {", "        call(Delphoi_TempleOfApollo_EventScript_TraceCella)", "    }",
          "    return", "}", ""]
    # what lights when the beam ends on a disc or the brazier; restoring on load
    L.append("script Delphoi_TempleOfApollo_EventScript_LightTiles {")
    for (k, x, y) in DISCS:
        gx, gy = GATES[DISC_GATE[k]]
        tile = ("METATILE_APOLLO_WALL_DISC_LIT" if x in (0, W - 1) else
                "METATILE_APOLLO_SCREEN_DISC_LIT" if (x, y) != (gx, gy) else None)
        L.append(f"    if (flag(FLAG_ICHOR_APOLLO_{k})) {{")
        if tile:
            L.append(f"        setmetatile({x}, {y}, {tile}, TRUE)")
        L.append(f"        setmetatile({gx}, {gy}, METATILE_APOLLO_GATE_OPEN, FALSE)")
        L.append("    }")
    bx, by = BRAZIER
    L += ["    if (flag(FLAG_ICHOR_APOLLO_BRAZIER)) {", f"        setmetatile({bx}, {by}, METATILE_APOLLO_BRAZIER_LIT, TRUE)",
          "    }", "    if (flag(FLAG_ICHOR_PYTHIAN_LIGHT_DONE)) {"]
    tx, ty = TRIPOD
    for (dx, dy, n) in ((0, 0, "TL"), (1, 0, "TC"), (2, 0, "TR"), (0, 1, "BL"), (1, 1, "BC"), (2, 1, "BR")):
        L.append(f"        setmetatile({tx + dx}, {ty + dy}, METATILE_APOLLO_TRIPOD_LIT_{n}, TRUE)")
    L += ["    }", "    return", "}", ""]
    # after a trace from the cella's source: did it end on something that lights?
    L.append("script Delphoi_TempleOfApollo_EventScript_CheckCella {")
    L.append("    switch (var(VAR_RESULT)) {")
    for (k, x, y) in DISCS[1:]:
        L += [f"        case LOCALID_APOLLO_{k}:", f"            if (!flag(FLAG_ICHOR_APOLLO_{k})) {{",
              f"                setflag(FLAG_ICHOR_APOLLO_{k})",
              "                call(Delphoi_TempleOfApollo_EventScript_DiscBlazes)"]
        if k == "DISC_4":
            L.append(f"                removeobject(LOCALID_APOLLO_{k})")
        L += ["            }"]
    L += ["        case LOCALID_APOLLO_BRAZIER:", "            if (!flag(FLAG_ICHOR_APOLLO_BRAZIER)) {",
          "                setflag(FLAG_ICHOR_APOLLO_BRAZIER)",
          "                call(Delphoi_TempleOfApollo_EventScript_BrazierCatches)", "            }",
          "    }", "    return", "}", ""]
    L.append("// delphoi_temple: end generated")
    return "\n".join(L)


def splice_scripts(m):
    import re
    p = Path(__file__).resolve().parents[3] / "data/maps" / NAME / "scripts.pory"
    t = p.read_text()
    block = gen_scripts(m)
    if "delphoi_temple: begin generated" in t:
        t = re.sub(r"// delphoi_temple: begin generated.*?// delphoi_temple: end generated", lambda _m: block, t,
                   flags=re.S)
    else:
        t = t.rstrip("\n") + "\n\n" + block + "\n"
    p.write_text(t)


if __name__ == "__main__":
    m = build()
    splice_scripts(m)
    m.build("delphoi_templeofapollo", starts=[(9, 45)],
            extra={(x, y) for (x, y) in GATES.values()},
            views=[(9, 43), (9, 36), (9, 29), (6, 22), (6, 14), (9, 6)])
    s = build_stair()
    s.build("delphoi_omphalosstair", starts=[(3, 2)], views=[(4, 6), (7, 22), (9, 34)])
