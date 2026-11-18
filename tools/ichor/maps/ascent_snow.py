#!/usr/bin/env python3
"""Build the Ascent's snow floors on gTileset_Chion (design/LEAGUE.md,
design/maps/Ascent_*.md):

  Ascent_Icefall       the ice caves behind a waterfall that froze: the slide
                       hall, the guarded gut, the drum seal, the crystal garden
  Ascent_IcefallDeep   the coldest dark under it (Hecate's Torch): the black
                       tarn (Poseidon's Conch), Stygiad's home
  Ascent_CrystalVault  a hall of frozen ichor behind a bronze chain (the Labrys)
  Ascent_Glacier       the river of ice with the Giants frozen in it: the ice
                       field, the Gate of the Winds (three drums, three plates)
  Ascent_3F            above the cloud line: the processional stair, the
                       gatekeeper and the Pantheon's propylaia
  Olympus_Summit       the altar of Zeus above the cloud, the temple of the
                       Twelve (ascent_peak.py; its scripts are hand-written)

Each map writes its layout, map.json and scripts.pory. Usage:
  /usr/bin/python3 tools/ichor/maps/ascent_snow.py [--render DIR] [--tag T] [--only A,B] [--walk]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ascent_lib as A  # noqa: E402
import league_lib as L  # noqa: E402
from ascent_lib import Snow, blob, carve, plan, push_plan  # noqa: E402
from league_lib import ROOT, A_STEPS, noise  # noqa: E402

PLANS = {}   # puzzle answers for the headless test: name -> data


def write_scripts(name, text):
    (ROOT / f"data/maps/{name}/scripts.pory").write_text(text.lstrip("\n"))


def trainer_script(prefix, lid, const, intro, defeat, after):
    return f'''
script {prefix}{lid} {{
    trainerbattle_single(TRAINER_ICHOR_{const},
        format("{intro}"),
        format("{defeat}"))
    msgbox(format("{after}"), MSGBOX_AUTOCLOSE)
}}
'''


def sign_script(prefix, name, text):
    return f'''
script {prefix}{name} {{
    msgbox(format("{text}"), MSGBOX_SIGN)
}}
'''


def setmetas(cells, indent="    "):
    """setmetatile lines for [(x, y, metatile id, impassable)]."""
    return "\n".join(f"{indent}setmetatile({x}, {y}, 0x{mid:03X}, {'TRUE' if s else 'FALSE'})"
                     for x, y, mid, s in cells)


# ---------------------------------------------------------------------------
# The Icefall
# ---------------------------------------------------------------------------
IW, IH = 42, 46


# The slide hall's stoppers, found by a search for a field whose way to the gut
# takes ten slides and to the garden seven, and which can never strand you
# (Snow.check_no_strand proves the last on every build).
ICE_STOPS = [(5, 23), (8, 29), (9, 25), (10, 23), (13, 24), (18, 33), (20, 29), (21, 31), (23, 30),
             (28, 25), (31, 28), (32, 27), (33, 29), (33, 33), (34, 32)]
ICE_CRYSTALS = [(8, 29), (20, 29), (23, 30), (31, 28), (33, 33), (13, 24), (28, 25)]


def icefall_plan():
    r = plan(IW, IH)
    # the entry hall, where 2F's tunnel comes in (south edge)
    blob(r, ".", 20, 40, 10, 3, salt=1)
    carve(r, ".", 19, 41, 21, IH - 1)
    # the slide hall: a frozen lake in a long chamber, a floor rim on its south side
    carve(r, ".", 5, 34, 36, 35)
    carve(r, ",", 5, 23, 36, 33)
    blob(r, ",", 9, 26, 4, 3, salt=2)
    blob(r, ",", 32, 26, 4, 3, salt=3)
    carve(r, ".", 17, 36, 23, 37)
    # the stoppers on the ice: crystals grown up through it, and rock pillars
    # the hall's walls bite into the ice here and there (the field's corners)
    for (x, y) in ((5, 33), (36, 33), (36, 23), (6, 23)):
        r[y][x] = "#"
    # the gaps out of the hall: the gut (north, x 21) and the crystal garden (north-east, x 34)
    r[22][21] = "."
    r[22][34] = "."
    # the gut: a narrow way north with two alcoves (the pair)
    carve(r, ".", 20, 15, 22, 21)
    carve(r, ".", 18, 18, 19, 18)
    carve(r, ".", 23, 16, 24, 16)
    # the drum room
    blob(r, ".", 16, 11, 8, 3, salt=4)
    carve(r, ".", 12, 10, 24, 14)
    # the grate's gap in the north wall, then the upper hall to the mouth
    carve(r, ".", 19, 6, 19, 8)
    blob(r, ".", 19, 4, 7, 2, salt=5)
    carve(r, ".", 18, 0, 20, 3)
    # the west alcove with the ladder down (behind ice-rubble)
    carve(r, ".", 6, 3, 11, 5)
    carve(r, ".", 12, 4, 13, 4)
    # the crystal garden (north-east), reached off the ice
    blob(r, ".", 34, 14, 5, 6, salt=6)
    carve(r, ".", 34, 20, 34, 21)
    carve(r, ".", 31, 5, 37, 9)
    carve(r, ".", 33, 3, 35, 4)
    # a frozen pool in the entry hall
    blob(r, "~", 28, 40, 2, 1, salt=8, rough=0.0)
    return r


def build_icefall():
    r = icefall_plan()
    g = Snow("Ascent_Icefall", r)
    P = "Ascent_Icefall_EventScript_"
    # the way in from 2F: daylight at the tunnel's foot
    for x in (19, 20, 21):
        g.put("exit_s", x, IH - 1)
        g.warp(x, IH - 1, "Ascent_2F", 0)
    # the way out to the glacier
    for x in (18, 19, 20):
        g.put("exit_n", x, 0)
        g.warp(x, 0, "Ascent_Glacier", 0)
    # stoppers: crystals where the plan put rock pillars in the ice
    for (x, y) in ICE_STOPS:
        g.put("crystal_s_ice" if (x, y) in ICE_CRYSTALS else "ice_rock_ice", x, y)
    # the entry hall: the shrine (fragment III) and the Icefall's lore
    g.put("shrine", 12, 38)
    g.sign(12, 39, P + "Shrine")
    g.put("crystal_tall", 29, 37)
    g.put("crystal_s", 11, 41)
    g.put("ice_rock", 26, 42)
    g.put("frozen_fall", 23, 36)
    g.sign(23, 38, P + "FrozenFall")
    g.hidden("ITEM_ICE_STONE", 30, 41, "FLAG_ICHOR_HIDDEN_ITEM_ICEFALL_ICE_STONE")
    g.put("snow_glitter", 30, 41)
    # the slide hall's prize: Never-Melt Ice at the far east wall, reached by sliding
    g.item("ITEM_NEVER_MELT_ICE", 36, 28, "FLAG_ICHOR_ITEM_ICEFALL_NEVER_MELT_ICE")
    g.sign(15, 35, P + "IceSign")
    for (x, y) in ((8, 35), (30, 35), (35, 34)):
        g.put("crystal_s", x, y)
    # the gut: the pair in their alcoves, facing across
    g.person("CHIONE", "PRIESTESS", 18, 18, "Chione", facing="RIGHT", sight=4)
    g.person("ARKTOS", "HOPLITE", 24, 16, "Arktos", facing="LEFT", sight=4)
    # the drum room: one drum, one plate, the grate in the north wall
    drum, plate_c, grate_c = (16, 13), (16, 11), (19, 8)
    g.put("plate", *plate_c)
    g.put("grate", *grate_c)
    g.obstacle("DRUM", "drum", *drum)
    g.put("crystal_l", 22, 10)
    g.put("crystal_s", 12, 13)
    g.sign(13, 9, P + "Lever")
    g.trigger(plate_c[0], plate_c[1] + 1, "Plates", var="VAR_TEMP_1", value="0")
    g.trigger(plate_c[0] - 1, plate_c[1], "Plates", var="VAR_TEMP_1", value="0")
    g.trigger(plate_c[0] + 1, plate_c[1], "Plates", var="VAR_TEMP_1", value="0")
    g.trigger(plate_c[0], plate_c[1] - 1, "Plates", var="VAR_TEMP_1", value="0")
    # the upper hall: the last guard, the mouth, the west alcove and its ladder
    g.person("BOREAS", "AUGUR", 22, 3, "Boreades", facing="LEFT", sight=4)
    g.item("ITEM_MAX_ELIXIR", 25, 5, "FLAG_ICHOR_ITEM_ICEFALL_MAX_ELIXIR")
    g.obstacle("RUBBLE", "rubble", 12, 4)
    g.put("ladder_down", 7, 4)
    g.warp(7, 4, "Ascent_IcefallDeep", 0)
    g.put("crystal_s", 6, 3)
    g.put("ice_rock", 10, 5)
    # the crystal garden
    g.put("crystal_l", 36, 11)
    g.put("crystal_l", 31, 15)
    g.put("crystal_tall", 37, 16)
    g.put("crystal_tall", 32, 9)
    g.put("crystal_s", 30, 12)
    g.put("crystal_s", 38, 14)
    g.item("ITEM_TM_BLIZZARD", 35, 17, "FLAG_ICHOR_ITEM_ICEFALL_TM_BLIZZARD")
    g.hidden("ITEM_NUGGET", 38, 8, "FLAG_ICHOR_HIDDEN_ITEM_ICEFALL_NUGGET")
    g.put("mouth", 33, 3)
    g.warp(34, 4, "Ascent_CrystalVault", 0)
    g.solid[4, 33] = True
    g.person("CHAIN", "OBJ_EVENT_GFX_BREAKABLE_ROCK", 34, 4, "EventScript_IchorLabrysSeal",
             movement="MOVEMENT_TYPE_NONE", flag="FLAG_ICHOR_HIDE_VAULT_CHAIN")
    g.sign(35, 5, P + "VaultDoor")
    g.sign(32, 13, P + "Ichor")
    g.accents()

    g.save([CHION_WALL()] * 4,
           dict(map_type="MAP_TYPE_UNDERGROUND", weather="WEATHER_NONE", show_map_name=True,
                allow_cycling=False, allow_escaping=True, requires_flash=False,
                music="MUS_VICTORY_ROAD", ichor_kind="dungeon"))
    # checks: the drum seal's answer, the slide answers, and reachability
    walk = g.walkable()
    open_cells = {(x, y) for y in range(g.H) for x in range(g.W)
                  if walk[y, x] or (x, y) == drum} - {grate_c}
    room = {(x, y) for (x, y) in open_cells if 9 <= y <= 15 and 10 <= x <= 25}
    pushes = push_plan(room, [drum], [plate_c], (21, 15))
    if not pushes:
        raise SystemExit("Ascent_Icefall: the drum seal can't be solved")
    entry = (20, IH - 2)
    g.check_no_strand(entry, blocked=[grate_c])
    gut = g.slide_plan((21, 34), (21, 22))
    garden = g.slide_plan((21, 34), (34, 22))
    prize = g.slide_plan((21, 34), (35, 28))
    PLANS["icefall"] = dict(gut=gut, garden=garden, prize=prize, pushes=pushes, drum=drum, plate=plate_c)
    must = [("gut", (21, 21)), ("garden", (34, 20)), ("prize", (36, 28)), ("drum", drum),
            ("shrine", (12, 39))]
    seen = g.check(entry, must, blocked=[grate_c])
    must_up = [("exit", (19, 0)), ("ladder", (7, 4)), ("elixir", (25, 5))]
    g.solid[grate_c[1], grate_c[0]] = False          # the seal solved
    g.check(entry, must_up)
    g.solid[grate_c[1], grate_c[0]] = True
    print(f"Icefall: gut {gut}, garden {garden}, prize {prize}, pushes {pushes}")

    # scripts
    gx, gy = grate_c
    px, py = plate_c
    s = f'''// The Icefall (design/maps/Ascent_Icefall.md): ice caves behind a waterfall that
// froze. Generated by tools/ichor/maps/ascent_snow.py: edit the builder, not this file.

mapscripts Ascent_Icefall_MapScripts {{
    MAP_SCRIPT_ON_LOAD: Ascent_Icefall_EventScript_DrawState
    MAP_SCRIPT_ON_TRANSITION {{
        setflag(FLAG_SYS_USE_STRENGTH) if (false) {{}}
    }}
}}

// The grate stays up once the drum has sat on its plate; the drum stays on it.
script Ascent_Icefall_EventScript_DrawState {{
    if (flag(FLAG_ICHOR_ICEFALL_GRATE_OPEN)) {{
        setmetatile({gx}, {gy}, 0x{g.pid("grate_up"):03X}, FALSE)
        setmetatile({px}, {py}, 0x{g.pid("plate_down"):03X}, FALSE)
        setobjectxyperm(LOCALID_ASCENT_ICEFALL_DRUM, {px}, {py})
    }}
}}

// Herakles's floor seal: one drum onto one plate raises the grate (the teach).
script Ascent_Icefall_EventScript_Plates {{
    if (flag(FLAG_ICHOR_ICEFALL_GRATE_OPEN)) {{
        end
    }}
    getobjectxy(LOCALID_ASCENT_ICEFALL_DRUM, CURRENT_POSITION, VAR_0x8007, VAR_0x8008)
    if (var(VAR_0x8007) == {px} && var(VAR_0x8008) == {py}) {{
        lockall
        setflag(FLAG_ICHOR_ICEFALL_GRATE_OPEN)
        setmetatile({px}, {py}, 0x{g.pid("plate_down"):03X}, FALSE)
        playse(SE_DOOR)
        delay(20)
        setmetatile({gx}, {gy}, 0x{g.pid("grate_up"):03X}, FALSE)
        special(DrawWholeMapView)
        msgbox(format("The plate sinks under the drum. Somewhere a chain runs, and the bronze grate rises."), MSGBOX_DEFAULT)
        releaseall
    }}
}}

script Ascent_Icefall_EventScript_Lever {{
    lockall
    if (flag(FLAG_ICHOR_ICEFALL_GRATE_OPEN)) {{
        msgbox(format("A bronze lever, frozen in the up position. The grate is open."), MSGBOX_DEFAULT)
        releaseall
        end
    }}
    msgbox(format("A bronze lever by the plate, the Girdle's knot cast in its handle: the seal's reset.\\pPull it and put the drum back?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_CLICK)
        warpsilent(MAP_ASCENT_ICEFALL, 13, 10)
        waitstate
    }}
    releaseall
}}
'''
    s = s.replace('''    MAP_SCRIPT_ON_TRANSITION {
        setflag(FLAG_SYS_USE_STRENGTH) if (false) {}
    }
''', "")
    s += trainer_script(P, "Chione", "ICEFALL_CHIONE",
                        "The snow nymph keeps this gut. I keep it for her.\\pYou'll have to come through both of us.",
                        "Melted.",
                        "Chione was Boreas's daughter. The north wind's.\\pHer children are still in the walls here, if you listen.")
    s += trainer_script(P, "Arktos", "ICEFALL_ARKTOS",
                        "The Archon's guard holds the Icefall. Nobody slips past.",
                        "…Nobody but you, then.",
                        "Up past the grate there's a drum and a plate. Herakles's sort of lock.\\pPut the weight where the weight goes.")
    s += trainer_script(P, "Boreades", "ICEFALL_BOREADES",
                        "I read the wind for omens. It stopped telling me anything.\\pSo now I just fight in it.",
                        "Cold comfort.",
                        "The glacier's up through that mouth. Mind the ice field.\\pA wrong push and it carries you right across.")
    s += sign_script(P, "Shrine",
                     "A stele of Hestia, cut into the ice. Fragment III of the Olympian hymn:\\p"
                     "“Hestia took the first seat at the hearth and the last at the feast.\\p"
                     "When the Twelve were too many by one, she gave her throne away, and kept the fire.”")
    s += sign_script(P, "FrozenFall",
                     "A waterfall frozen solid in mid-pour. It hasn't moved in a thousand years.\\p"
                     "Something glints behind the ice, high up. No way to reach it.")
    s += sign_script(P, "IceSign",
                     "THE ICEFALL\\nThe floor is ice. You won't stop till something stops you.\\p"
                     "Crystals and pillars will. Plan the slide before you take it.")
    s += sign_script(P, "VaultDoor",
                     "A door of black ice, bound with a bronze chain thick as an arm.\\p"
                     "Cut into the lintel: ICHOR, WHAT THE GODS BLED.")
    s += sign_script(P, "Ichor",
                     "The crystals here are full of light, gold at the heart.\\p"
                     "Old climbers said the gods bled here in the war with the Giants,\\p"
                     "and the blood froze where it fell.")
    write_scripts("Ascent_Icefall", s)
    return g, seen, [("entry", 20, 41), ("shrine", 13, 37), ("slide_hall", 20, 30), ("slide_east", 31, 27),
                     ("gut", 21, 18), ("drum_room", 17, 11), ("upper", 19, 4), ("alcove", 9, 4),
                     ("garden", 34, 13), ("vault", 34, 6)]


def CHION_WALL():
    return A.CHION["kit"]["T|..."] | (1 << 10)


# ---------------------------------------------------------------------------

import ascent_glacier as AG  # noqa: E402
import ascent_summit as AS  # noqa: E402
import ascent_peak as AP  # noqa: E402

BUILDERS = {"icefall": build_icefall, "deep": lambda: AG.build_deep(PLANS), "vault": lambda: AG.build_vault(PLANS),
            "glacier": lambda: AG.build_glacier(PLANS), "3f": lambda: AS.build_3f(PLANS),
            "summit": lambda: AP.build_summit(PLANS)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render")
    ap.add_argument("--tag", default="")
    ap.add_argument("--only", default=",".join(BUILDERS))
    ap.add_argument("--walk", action="store_true")
    args = ap.parse_args()
    for key in args.only.split(","):
        g, seen, views = BUILDERS[key]()
        if args.walk:
            print(g.walk_text(seen))
        if args.render:
            print(A.render(g, args.render, A.views_of(g, views), args.tag))
    if set(PLANS) >= {"icefall", "glacier"}:
        write_plans(PLANS)


def lua(v):
    if isinstance(v, str):
        return '"' + v + '"'
    if isinstance(v, (list, tuple)):
        return "{" + ", ".join(lua(x) for x in v) + "}"
    if isinstance(v, dict):
        return "{" + ", ".join(f"{k} = {lua(x)}" for k, x in v.items()) + "}"
    return str(v)


def write_plans(plans):
    """The puzzles' answers, for tools/ichor/tests/ascent.lua to replay (the build
    proves them; the test plays them in the game)."""
    lines = ["-- Generated by tools/ichor/maps/ascent_snow.py with the maps: the Ascent's",
             "-- puzzle answers (ice slides as key strings, drum pushes as {stand x, stand y, key}).",
             "return {"]
    for k in ("icefall", "glacier"):
        lines.append(f"  {k} = {lua(plans[k])},")
    lines.append("}")
    (ROOT / "tools/ichor/tests/ascent_plans.lua").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
