#!/usr/bin/env python3
"""Ascent 3F on gTileset_Propylon: the terraces above the cloud and the grand entrance
(design/maps/Ascent_3F.md).

Out of Boreas's ridge the processional way climbs three snow terraces, each stepped
up by a cliff with a stair cut into it, to the cliff top. There the Propylaia
stands across the whole width of the mountain's top: a pediment with Zeus and the
eagle in gold, a painted frieze, ten Ionic columns you walk behind, bronze doors,
the statues of the Twelve before it and two great braziers. The first time you
come up the last stair the camera climbs the facade.

Usage: /usr/bin/python3 tools/ichor/maps/propylon.py [--render DIR] [--tag T] [--walk]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ascent_lib as A  # noqa: E402
from ascent_glacier import sign_script, trainer_script, write_scripts  # noqa: E402
from oros_lib import Oros, roughen, seam_check  # noqa: E402
from oros_maps import area, lv_plan, rows_of  # noqa: E402

TW, TH = 44, 62
DOOR = (21, 9)                    # the bronze doors (cells 21-22 on row 9): warp 0
KEEPER = (21, 27)                 # Polydamas, at the foot of the last stair
STAIRS = {"s1": 47, "s2": 35, "s3": 23}   # each stair's top row (four rows, x 21-22)
HERM = (19, 16)                   # the travel herm (an object: tools/ichor/maps/town_herms.py)
SEAM = range(TH - 8, TH)          # the bottom rows that show from Boreas's ridge
TWELVE_L = ["hestia", "hermes", "demeter", "dionysus", "artemis", "hephaestus"]
TWELVE_R = ["aphrodite", "apollo", "ares", "poseidon", "athena", "hera"]
STATUE_X_L = [2, 5, 8, 11, 14, 17]
STATUE_X_R = [26, 29, 32, 35, 38, 41]
STATUE_Y = 16
WATCH = (11, 30)                  # the watchman of the Archon's stores
CHAMPION = (0, 16)


def levels():
    a = lv_plan(TW, TH, -1)
    area(a, 6, 0, 0, TW - 1, 22)                         # the cliff top: the facade and the Twelve
    area(a, 4, 8, 23, 35, 34)                            # terrace 3, the processional way
    area(a, 2, 4, 35, 39, 46)                            # terrace 2
    area(a, 4, 4, 35, 9, 39)                             # the summit cone's foot (the sealed stair)
    area(a, 0, 10, 47, 33, TH - 1)                       # terrace 1, out of the cloud
    return a


def build_3f():
    a = levels()
    # the terraces' edges break against the cloud: no straight runs
    keep = {(x, y) for x in range(0, 44) for y in range(0, 23)} | {(x, y) for x in range(16, 28) for y in range(23, 62)} | {(x, y) for x in range(4, 13) for y in range(35, 47)} | {(x, y) for x in range(33, 41) for y in range(39, 47)}
    roughen(a, -1, 65, rate=38, keep=keep)
    g = Oros("Ascent_3F", rows_of(a), tileset="gTileset_Propylon")
    P = "Ascent_3F_EventScript_"
    for top in STAIRS.values():                     # broad marble steps, four wide
        g.stairs({(x, y) for x in range(20, 24) for y in range(top, top + 4)}, marble=True)
    g.stairs({(7, y) for y in range(40, 44)})
    way = {(x, y) for x in range(20, 24) for y in list(range(16, 23)) + list(range(27, 35)) + list(range(39, 47))
           + list(range(51, TH))}
    g.path(way)
    g.paint()
    # the grand entrance
    g.put("facade", 0, 0)
    for x in (21, 22):
        g.warp(x, DOOR[1], "Olympus_Propylaia", 0)
    # the statues of the Twelve: painted marble on teal plinths (tools/ichor/art/statues.py),
    # 32x64 objects standing on the row's base cell, so they cost the facade no tiles
    for god, x in zip(TWELVE_L + TWELVE_R, STATUE_X_L + STATUE_X_R):
        g.person("STATUE_" + god.upper(), "OBJ_EVENT_GFX_ICHOR_STATUE_" + god.upper(), x, STATUE_Y + 2,
                 "Statue_" + god.title(), movement="MOVEMENT_TYPE_NONE")
    g.put("statue_champion", *CHAMPION)
    g.sign(CHAMPION[0], CHAMPION[1] + 3, P + "ChampionStatue", facing="NORTH")
    g.hidden("ITEM_LAUREL_SPRIG", STATUE_X_L[0] + 1, STATUE_Y + 3, "FLAG_ICHOR_HIDDEN_ITEM_ASCENT3_LAUREL_SPRIG")
    # every stair lined with lit braziers, top and foot; the kit's Ionic columns
    # flanking the processional way on the upper terraces
    for top in STAIRS.values():
        for x in (18, 25) if top != STAIRS["s3"] else (17, 26):
            g.put("brazier", x, top - 2)
            if top + 5 < TH - 8:
                g.put("brazier", x, top + 4)
    for (x, y) in ((16, 29), (27, 29), (16, 32), (27, 32), (14, 40), (29, 40), (14, 43), (29, 43)):
        g.put("kcol", x, y)
    g.put("basin", 24, 16)
    g.sign(24, 16, P + "Basin")
    g.sign(25, 16, P + "Basin")
    # the processional way: tripods of every Archon, both sides
    for y in (28, 31):
        g.put("tripod", 19, y + 1)
        g.put("tripod", 24, y + 1)
    # the Archon's watch-post: a walled store off terrace 3 with one way in
    for y in range(28, 34):
        if y != WATCH[1]:
            g.put("rock" if y % 2 else "rock_b", 13, y)
    for x in range(9, 13):
        g.put("rock" if x % 2 else "rock_b", x, 28)
        g.put("rock_b" if x % 2 else "rock", x, 33)
    g.person("WATCHMAN", "HOPLITE", WATCH[0], WATCH[1], "WatchMan", facing="RIGHT")
    g.item("ITEM_CHOICE_BAND", 10, 32, "FLAG_ICHOR_ITEM_ASCENT3_CHOICE_BAND")
    g.item("ITEM_WEAKNESS_POLICY", 12, 29, "FLAG_ICHOR_ITEM_ASCENT3_WEAKNESS_POLICY")
    g.trigger(13, WATCH[1], "WatchPost")
    # the Arceus hook: four empty sockets before the sealed stair into the cone
    for (x, y) in ((6, 44), (8, 44), (6, 46), (8, 46)):
        g.put("plate_down", x, y)
    g.put("grate", 7, 43)
    g.sign(7, 45, P + "Sockets", facing="NORTH")
    # the D11 hook: the cloud bank that never clears, rolling onto terrace 2's east end
    for (x, y) in ((38, 41), (37, 42), (38, 42), (39, 42), (36, 43), (37, 43), (38, 43), (39, 43)):
        g.set(x, y, g.pid(f"cloud_{(x % 2) + 2 * (y % 2)}"), True, "cloud")
    g.sign(35, 43, P + "CloudBank", facing="EAST")
    # the shrine, the finds, the props
    g.put("stele", 28, 51)
    g.sign(28, 53, P + "Shrine", facing="NORTH")
    g.put("sign", 16, 52)
    g.sign(16, 52, P + "SnowSign")
    g.item("ITEM_PP_UP", 33, 40, "FLAG_ICHOR_ITEM_ASCENT3_PP_UP")
    g.item("ITEM_FULL_HEAL", 12, 51, "FLAG_ICHOR_ITEM_ASCENT3_FULL_HEAL")
    g.item("ITEM_RARE_CANDY", 34, 27, "FLAG_ICHOR_ITEM_ASCENT3_RARE_CANDY")
    g.hidden("ITEM_COMET_SHARD", 31, 52, "FLAG_ICHOR_HIDDEN_ITEM_ASCENT3_COMET_SHARD")
    g.hidden("ITEM_STAR_PIECE", 30, 33, "FLAG_ICHOR_HIDDEN_ITEM_ASCENT3_STAR_PIECE")
    for (key, x, y) in (("rock", 13, 40), ("rock", 28, 45), ("rock_b", 31, 28), ("rock_b", 15, 45),
                        ("rock", 11, 52), ("rock", 26, 40), ("rock_b", 33, 32)):
        g.put(key, x, y)
    # the trainers: a pair at the first stair's foot, Gorgo on terrace 2, a pair on
    # the processional way, then the gatekeeper at the foot of the last stair
    g.person("STHENELOS", "HOPLITE", 19, 52, "Sthenelos", facing="RIGHT", sight=4)
    g.person("HIPPIAS", "HOPLITE", 24, 52, "Hippias", facing="LEFT", sight=4)
    g.person("GORGO", "TITAN_GRUNT", 22, 42, "Gorgo", facing="DOWN", sight=4)
    g.person("MELITE", "ACOLYTE_F", 19, 31, "Melite", facing="RIGHT", sight=4)
    g.person("KORINNA", "PRIESTESS", 24, 31, "Korinna", facing="LEFT", sight=4)
    g.person("POLYDAMAS", "GIGAS", KEEPER[0], KEEPER[1], "Polydamas", facing="DOWN", sight=3)
    for x in (20, 22, 23):
        g.trigger(x, KEEPER[1], "KeeperBlocks")
    # the awe scenes: out of the cloud, and the facade's first sight
    for x in range(19, 26):
        g.trigger(x, TH - 3, "CloudBreak")
    for x in range(20, 24):
        g.trigger(x, 34, "Pantheon")
    seam_check(g, SEAM)
    g.save(g.border(), dict(map_type="MAP_TYPE_ROUTE", weather="WEATHER_SUNNY", show_map_name=False,
                            allow_cycling=False, allow_escaping=False, requires_flash=False,
                            music="MUS_VICTORY_ROAD", ichor_kind="dungeon"),
           connections=[dict(map="MAP_ASCENT_WIND_RIDGE", offset=0, direction="down")])
    entry = (22, TH - 1)
    must = [("door", (21, 10)), ("sockets", (7, 45)), ("cloud bank", (35, 43)), ("full heal", (12, 51)),
            ("candy", (34, 27)), ("pp up", (33, 40)), ("shrine", (28, 53)), ("herm", (HERM[0] + 1, HERM[1])),
            ("champion", (0, 19)), ("hera", (41, 19))]
    keeper = g.events["object_events"][-1] if False else None
    kp = next(o for o in g.events["object_events"] if o.get("local_id", "").endswith("_POLYDAMAS"))
    kp["x"] = KEEPER[0] - 1
    seen = g.check(entry, must)
    kp["x"] = KEEPER[0]
    g.check(entry, [("keeper", KEEPER)])
    assert (11, 30) not in g.reach((14, 30), blocked=[(13, 30)]), "the stores have one way in"
    write_scripts("Ascent_3F", script(g, P))
    return g, seen, [("arrival", 22, 57), ("terrace1", 22, 53), ("stair1", 22, 48), ("sockets", 8, 43),
                     ("cloud_bank", 35, 42), ("stair2", 22, 37), ("procession", 22, 30), ("watch", 12, 30),
                     ("keeper", 22, 26), ("twelve_w", 9, 18), ("twelve_e", 34, 18), ("facade", 22, 10),
                     ("pediment", 22, 4)]


STATUE_LINES = {
    "Hestia": "HESTIA OF THE HEARTH. Her hand is cupped round a flame of gold leaf.\\pThe eldest of them, and the first one given every offering.",
    "Hermes": "HERMES OF THE ROADS. Wings at his heels; the staff with two snakes.\\pSomeone has left a coin on the plinth for the road down.",
    "Demeter": "DEMETER OF THE GRAIN. A sheaf of wheat in her arms, carved so fine the ears look ripe.\\pThere's snow on the sheaf. She doesn't look pleased about it.",
    "Dionysus": "DIONYSUS, TWICE-BORN. A fennel staff with a pine cone on top.\\pThe sculptor gave him a smile you can't quite trust.",
    "Artemis": "ARTEMIS OF THE WILDS. A bow, a crescent in her hair.\\pHer quiver's one arrow short.",
    "Hephaestus": "HEPHAESTUS THE SMITH. The hammer, the tongs, a crutch he made himself.\\pThe only statue here that looks like it could fix the others.",
    "Aphrodite": "APHRODITE, FOAM-BORN. A scallop shell at her feet, a dove on her wrist.\\pThe sculptor signed this one twice.",
    "Apollo": "APOLLO OF THE LYRE. The lyre, the laurel, the far-shooting bow.\\pThe wind makes his marble strings hum.",
    "Ares": "ARES OF THE SPEAR. Helmet, spear, a shield with a boar on it.\\pSomeone has polished his spearpoint very recently.",
    "Poseidon": "POSEIDON, EARTH-SHAKER. The trident. Salt crusted at the base, this far from any sea.",
    "Athena": "ATHENA OF THE CITY. Helm, aegis, the owl on her shoulder.\\pThe owl is the only one here that looks back at you.",
    "Hera": "HERA, QUEEN OF HEAVEN. A crown, a sceptre with a cuckoo on it,\\pand a peacock's eye cut into the hem of her robe.",
}


def script(g, P):
    kx, ky = KEEPER
    s = f"""// Ascent 3F (design/maps/Ascent_3F.md): the terraces above the cloud, and the
// Propylaia's facade across the cliff top. Generated by tools/ichor/maps/propylon.py:
// edit the builder, not this file.

mapscripts Ascent_3F_MapScripts {{
    MAP_SCRIPT_ON_TRANSITION: Ascent_3F_EventScript_Keeper
}}

// Polydamas stands aside once beaten.
script Ascent_3F_EventScript_Keeper {{
    if (defeated(TRAINER_ICHOR_ASCENT_POLYDAMAS)) {{
        setobjectxyperm(LOCALID_ASCENT_3F_POLYDAMAS, {kx - 1}, {ky})
        setobjectmovementtype(LOCALID_ASCENT_3F_POLYDAMAS, MOVEMENT_TYPE_FACE_RIGHT)
    }}
}}

movement Ascent_3F_Movement_CameraUp {{ walk_slow_up * 4 }}
movement Ascent_3F_Movement_CameraDown {{ walk_down * 4 }}
movement Ascent_3F_Movement_CameraUpFacade {{ walk_up * 8 walk_slow_up * 14 }}
movement Ascent_3F_Movement_CameraPediment {{ walk_slow_left * 3 walk_slow_right * 6 walk_slow_left * 3 }}
movement Ascent_3F_Movement_CameraFromFacade {{ walk_faster_down * 22 }}
movement Ascent_3F_Movement_KeeperAside {{ walk_left face_right }}

script Ascent_3F_EventScript_CloudBreak {{
    if (flag(FLAG_ICHOR_SEEN_CLOUD_BREAK)) {{
        end
    }}
    lockall
    setflag(FLAG_ICHOR_SEEN_CLOUD_BREAK)
    fadescreenspeed(FADE_TO_WHITE, 4)
    playse(SE_M_GUST)
    delay(20)
    fadescreenspeed(FADE_FROM_WHITE, 2)
    msgbox(format("The white thins, and thins, and then there isn't any.\\p"
                  "The cloud lies below you like a sea, all the way to the edge of the world.\\p"
                  "For the first time since the foothills, there is sun."), MSGBOX_DEFAULT)
    closemessage
    special(SpawnCameraObject)
    applymovement(OBJ_EVENT_ID_CAMERA, Ascent_3F_Movement_CameraUp)
    waitmovement(0)
    delay(40)
    applymovement(OBJ_EVENT_ID_CAMERA, Ascent_3F_Movement_CameraDown)
    waitmovement(0)
    special(RemoveCameraObject)
    releaseall
}}

// The first sight of the grand entrance: the camera climbs the facade to the pediment.
script Ascent_3F_EventScript_Pantheon {{
    if (flag(FLAG_ICHOR_SEEN_PANTHEON)) {{
        end
    }}
    lockall
    setflag(FLAG_ICHOR_SEEN_PANTHEON)
    special(SpawnCameraObject)
    applymovement(OBJ_EVENT_ID_CAMERA, Ascent_3F_Movement_CameraUpFacade)
    waitmovement(0)
    playse(SE_M_GUST)
    applymovement(OBJ_EVENT_ID_CAMERA, Ascent_3F_Movement_CameraPediment)
    waitmovement(0)
    delay(30)
    msgbox(format("At the top of the last stair, across the whole of the mountain's top:\\p"
                  "the Propylaia. Column after column of white marble, bronze doors taller than a house,\\p"
                  "and the Twelve in stone before it. Gold on the pediment: Zeus, with the thunderbolt in his fist.\\p"
                  "Behind it, the four seats of the Pantheon. And above them all, the Archon."), MSGBOX_DEFAULT)
    closemessage
    delay(20)
    applymovement(OBJ_EVENT_ID_CAMERA, Ascent_3F_Movement_CameraFromFacade)
    waitmovement(0)
    special(RemoveCameraObject)
    releaseall
}}

// Polydamas holds the last stair: step past him unbeaten and he steps across.
script Ascent_3F_EventScript_KeeperBlocks {{
    if (defeated(TRAINER_ICHOR_ASCENT_POLYDAMAS)) {{
        end
    }}
    lockall
    applymovement(LOCALID_ASCENT_3F_POLYDAMAS, Common_Movement_FaceRight)
    waitmovement(0)
    msgbox(format("POLYDAMAS: The stair's mine. Nobody goes up who can't go through me."), MSGBOX_DEFAULT)
    closemessage
    applymovement(LOCALID_PLAYER, Common_Movement_WalkDown)
    waitmovement(0)
    applymovement(LOCALID_ASCENT_3F_POLYDAMAS, Common_Movement_FaceDown)
    waitmovement(0)
    releaseall
}}

script Ascent_3F_EventScript_Polydamas {{
    trainerbattle_single(TRAINER_ICHOR_ASCENT_POLYDAMAS,
        format("Polydamas of Skotoussa. I won the pankration at Olympia barehanded.\\p"
               "The Archon set me on this stair. Nobody goes up who can't go through me."),
        format("…Through me. Go up, then."), Ascent_3F_EventScript_PolydamasAside)
    msgbox(format("The doors are just there. The hearth's lit inside, and the healer keeps it.\\p"
                  "Warm your hands. You'll want them steady."), MSGBOX_AUTOCLOSE)
}}

script Ascent_3F_EventScript_PolydamasAside {{
    msgbox(format("I held up a cave roof once, so my friends could run.\\p"
                  "You're heavier than a mountain. Go on."), MSGBOX_DEFAULT)
    closemessage
    applymovement(LOCALID_ASCENT_3F_POLYDAMAS, Ascent_3F_Movement_KeeperAside)
    waitmovement(0)
    setobjectxyperm(LOCALID_ASCENT_3F_POLYDAMAS, {kx - 1}, {ky})
    release
    end
}}
"""
    s += trainer_script(P, "Sthenelos", "ASCENT_STHENELOS",
                        "The stair begins here. So does the Archon's peace.\\pDraw, challenger.",
                        "Peace kept. Barely.",
                        "Three terraces, three stairs. Then the doors.\\p"
                        "Don't stop at the top to look at the view. Everyone does.")
    s += trainer_script(P, "Hippias", "ASCENT_HIPPIAS",
                        "Sthenelos takes the left of the stair. I take the right.\\pBetween us there's no way round.",
                        "We'll widen the stair, then.",
                        "I've stood guard up here three winters. The cloud has never once been the same shape.")
    s += trainer_script(P, "Gorgo", "ASCENT_GORGO",
                        "I held a rank in Team Titan. I had a tablet with my name on it.\\p"
                        "The last draft. My draft. Do you know what it said?",
                        "…It didn't say this.",
                        "It said I'd stand at the master's right hand when the hours stopped.\\p"
                        "The hours stopped. I was in a ditch outside Delphoi.\\pFunny. I feel lighter.")
    s += trainer_script(P, "Melite", "ASCENT_MELITE",
                        "Snow on the Twelve's own stair. Isn't it lovely?\\pLet's see if you are.",
                        "Lovelier than I thought.",
                        "Hypatia taught me once. She asked me who I was.\\pI said my name. She said, “That's what they call you.”")
    s += trainer_script(P, "Korinna", "ASCENT_KORINNA",
                        "I sing the hymns on the processional way. Every pilgrim walks between Melite and me,\\p"
                        "and every pilgrim pays in a battle.",
                        "Paid in full.",
                        "The tripods are offerings from every Archon there's been. Count them. One is missing.\\p"
                        "Nobody knows whose.")
    s += """
// The watch-post: seen, you're sent back; under the Helm of Darkness, his eyes slide past.
script Ascent_3F_EventScript_WatchPost {
    if (flag(FLAG_ICHOR_HELM_ON)) {
        end
    }
    lockall
    playse(SE_PIN)
    msgbox(format("WATCHMAN: Halt. These are the Archon's stores.\\p"
                  "Nobody comes in here that I can see. Back to the way."), MSGBOX_DEFAULT)
    closemessage
    applymovement(LOCALID_PLAYER, Common_Movement_WalkRight)
    waitmovement(0)
    releaseall
}

script Ascent_3F_EventScript_WatchMan {
    lock
    if (flag(FLAG_ICHOR_HELM_ON)) {
        msgbox(format("The watchman stares straight through you, at the stair.\\p"
                      "“…Wind,” he mutters. “Only the wind.”"), MSGBOX_DEFAULT)
    } else {
        faceplayer
        msgbox(format("Twenty winters on this post. I've never once let in anyone I could see."), MSGBOX_DEFAULT)
    }
    release
}

// The empty plinth among the Twelve: after the credits it bears the champion's name.
script Ascent_3F_EventScript_ChampionStatue {
    lockall
    if (flag(FLAG_SYS_GAME_CLEAR)) {
        msgbox(format("An empty plinth at the end of the Twelve, and new letters cut in it, still sharp:\\p"
                      "{PLAYER}, WHO CLIMBED THE MOUNTAIN AND KEPT THE BOX.\\p"
                      "There's no statue on it. Whoever cut the letters said you'd want to stand there yourself."), MSGBOX_DEFAULT)
    } else {
        msgbox(format("An empty plinth at the end of the Twelve. The stone's been dressed, ready for letters.\\p"
                      "Nobody's cut any yet."), MSGBOX_DEFAULT)
    }
    releaseall
}
"""
    for god, line in STATUE_LINES.items():
        s += sign_script(P, "Statue_" + god, line)
    s += sign_script(P, "Basin",
                     "The lustral basin by the doors, frozen over. A white dove drinks at a hole in the ice,\\p"
                     "and a scallop shell lies on the rim, pink inside. Someone always leaves one. Aphrodite's.")
    s += sign_script(P, "Shrine",
                     "A stele of Zeus Ombrios, the rain-giver. Fragment V of the Olympian hymn:\\p"
                     "“From this height he saw every field below the cloud,\\p"
                     "and gave rain to the just and the unjust, since from up here he couldn't tell them apart.”")
    s += """
script Ascent_3F_EventScript_Sockets {
    lockall
    if (flag(FLAG_SYS_GAME_CLEAR)) {
        msgbox(format("Four sockets in a square, each the shape of a different key. Behind them, the barred stair.\\p"
                      "Since the summit, the bronze hums when you come near, very low. Still barred.\\p"
                      "Carved over it: STAND STILL."), MSGBOX_DEFAULT)
    } else {
        msgbox(format("Four sockets cut in a square in the stone, each the shape of a different key.\\p"
                      "Behind them a stair climbs into the summit cone, barred with bronze.\\p"
                      "Carved over it: STAND STILL."), MSGBOX_DEFAULT)
    }
    releaseall
}
"""
    s += sign_script(P, "CloudBank",
                     "Here the cloud never clears. It rolls up over the terrace's edge and won't go back down.\\p"
                     "Inside it, something whinnies. The wind itself would have to be told to move it.")
    s += sign_script(P, "SnowSign",
                     "THE PROCESSIONAL WAY\\nThree terraces, three stairs, the Propylaia.\\p"
                     "Above the cloud, the mountain belongs to the Twelve.")
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--render")
    ap.add_argument("--tag", default="")
    ap.add_argument("--walk", action="store_true")
    args = ap.parse_args()
    g, seen, views = build_3f()
    if args.walk:
        print(g.walk_text(seen))
    if args.render:
        print(A.render(g, args.render, A.views_of(g, views), args.tag))


if __name__ == "__main__":
    main()
