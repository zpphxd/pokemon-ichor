#!/usr/bin/env python3
"""Ascent 3F on gTileset_Chion: above the cloud line (design/maps/Ascent_3F.md).

The old road out of the glacier's cloud becomes a processional stair that
climbs three terraces of the mountain's shoulder, with nothing round it but
sky and the sea of cloud, to the Pantheon's propylaia. A pair of trainers waits
at the foot of each stair; the gatekeeper stands in the last one. Run it with
ascent_snow.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ascent_lib as A  # noqa: E402
from ascent_lib import Snow, blob, carve, plan  # noqa: E402
from ascent_glacier import sign_script, trainer_script, write_scripts  # noqa: E402
from league_lib import A_STEPS  # noqa: E402

TW, TH = 44, 46
STAIR1, STAIR2, STAIR3 = 31, 18, 6        # the bands' top rows (each band is two rows)
KEEPER = (21, 8)                          # the gatekeeper, in front of the last stair
DOOR = (21, 4)


def summit_mask(x, y):
    """The shoulder of the mountain above the cloud: True where there's rock or
    snow, False where the cloud sea shows. Its edges step, never run straight."""
    if y >= TH - 6:
        half = 9
    elif y >= 20:
        half = 13 + (2 if (y // 3) % 2 else 0) + (1 if y in (24, 25, 33) else 0)
    elif y >= 8:
        half = 11 + (1 if (y // 2) % 3 == 0 else 0)
    else:
        half = 9 + (1 if y % 3 == 0 else 0)
    return abs(x - 21.5) <= half


def plan_3f():
    r = plan(TW, TH)
    carve(r, ".", 18, TH - 6, 26, TH - 1)        # the way up out of the cloud (the glacier's seam)
    carve(r, ".", 12, 33, 31, TH - 7)            # terrace 1
    blob(r, ".", 21, 37, 11, 4, salt=51)
    carve(r, ".", 10, 20, 33, 30)                # terrace 2
    blob(r, ".", 21, 25, 13, 4, salt=52)
    carve(r, ".", 13, 8, 30, 17)                 # terrace 3, the processional way
    carve(r, ".", 14, 5, 27, 5)                  # the platform before the propylaia
    carve(r, ".", 14, 4, 17, 5)                  # its west bay (the travel herm)
    carve(r, ".", 25, 4, 27, 5)                  # its east bay
    for top in (STAIR1, STAIR2, STAIR3):         # the bands between the terraces
        for x in range(TW):
            r[top][x] = "#"
            r[top + 1][x] = "#"
    carve(r, ".", 11, 21, 13, 23)                # the sealed stair's foot (Arceus's hook)
    # the Archon's watch-post (2026-11-18): a walled store off terrace 3 with one way
    # in, kept by a watchman nobody gets past seen (the Helm of Darkness)
    carve(r, ".", 11, 10, 12, 14)
    for y in (10, 11, 13, 14):
        r[y][13] = "#"
    for y in range(TH):
        for x in range(TW):
            if not summit_mask(x, y):
                r[y][x] = "#"
    return r


def build_3f(PLANS):
    r = plan_3f()
    g = Snow("Ascent_3F", r, style="glacier")
    P = "Ascent_3F_EventScript_"
    # the propylaia first: its door is warp 0 (the Propylaia's way out returns here)
    g.put("propylaia", 18, 0)
    g.warp(DOOR[0], DOOR[1], "Olympus_Propylaia", 0)

    def steps(x0, x1, top):
        for x in range(x0, x1 + 1):
            for j in (0, 1):
                g.set(x, top + j, A_STEPS[j], False, "steps")
    steps(20, 22, STAIR1)
    steps(20, 22, STAIR2)
    steps(21, 21, STAIR3)
    # the processional way: paving up the axis, tripods both sides, braziers at the platform
    for y in range(8, 17):
        for x in range(19, 24):
            if not g.fixed[y, x]:
                g.set(x, y, g.pid("paving" if (x + y) % 2 else "paving_b"), False, "paving")
    for x in range(14, 28):
        if not g.fixed[5, x]:
            g.set(x, 5, g.pid("paving" if x % 2 else "paving_b"), False, "paving")
    for y in (10, 13):
        g.put("tripod", 17, y)
        g.put("tripod", 25, y)
    g.put("brazier", 14, 4)
    g.put("brazier", 27, 4)
    # the cloud sea round the shoulder
    cloud = A.PIECES["cloud"]
    for y in range(TH):
        for x in range(TW):
            if not summit_mask(x, y):
                g.set(x, y, cloud["ids"][y % 2][x % 4], True, "cloud")
    # the Arceus hook: four empty sockets before a sealed stair into the cone
    for (x, y) in ((14, 24), (16, 24), (14, 26), (16, 26)):
        g.put("plate_down", x, y)
    g.set(12, 21, A_STEPS[0], True, "steps")
    g.set(12, 22, A_STEPS[1], True, "steps")
    g.put("grate", 12, 23)
    g.sign(15, 25, P + "Sockets")
    # the D11 hook: the cloud bank that never clears, rolling onto terrace 2's east end
    for (x, y) in ((33, 23), (32, 24), (33, 24), (33, 25), (32, 25), (31, 25)):
        g.set(x, y, cloud["ids"][y % 2][x % 4], True, "cloud")
    g.sign(30, 24, P + "CloudBank")
    # the shrine, the finds
    g.put("shrine", 28, 35)
    g.sign(28, 36, P + "Shrine")
    g.item("ITEM_PP_UP", 31, 21, "FLAG_ICHOR_ITEM_ASCENT3_PP_UP")
    g.item("ITEM_FULL_HEAL", 14, 34, "FLAG_ICHOR_ITEM_ASCENT3_FULL_HEAL")
    g.item("ITEM_RARE_CANDY", 26, 4, "FLAG_ICHOR_ITEM_ASCENT3_RARE_CANDY")
    g.hidden("ITEM_COMET_SHARD", 30, 38, "FLAG_ICHOR_HIDDEN_ITEM_ASCENT3_COMET_SHARD")
    g.hidden("ITEM_STAR_PIECE", 28, 12, "FLAG_ICHOR_HIDDEN_ITEM_ASCENT3_STAR_PIECE")
    for key, x, y in (("ice_boulders", 12, 38), ("ice_rock", 25, 40), ("crystal_s", 30, 33), ("ice_rock", 27, 28),
                      ("ice_boulders", 29, 21), ("crystal_tall", 14, 15), ("ice_rock", 29, 15)):
        g.put(key, x, y)
    # the watch-post: its watchman faces the one way in; the stores behind him
    g.person("WATCHMAN", "HOPLITE", 11, 12, "WatchMan", facing="RIGHT")
    g.item("ITEM_CHOICE_BAND", 11, 14, "FLAG_ICHOR_ITEM_ASCENT3_CHOICE_BAND")
    g.item("ITEM_WEAKNESS_POLICY", 12, 10, "FLAG_ICHOR_ITEM_ASCENT3_WEAKNESS_POLICY")
    g.trigger(13, 12, "WatchPost")
    # the trainers: a pair at each stair's foot, then the gatekeeper in the last
    g.person("STHENELOS", "HOPLITE", 18, 33, "Sthenelos", facing="RIGHT", sight=4)
    g.person("HIPPIAS", "HOPLITE", 24, 33, "Hippias", facing="LEFT", sight=4)
    g.person("GORGO", "TITAN_GRUNT", 22, 24, "Gorgo", facing="DOWN", sight=4)
    g.person("MELITE", "ACOLYTE_F", 18, 12, "Melite", facing="RIGHT", sight=4)
    g.person("KORINNA", "PRIESTESS", 24, 14, "Korinna", facing="LEFT", sight=4)
    g.person("POLYDAMAS", "GIGAS", KEEPER[0], KEEPER[1], "Polydamas", facing="DOWN", sight=3)
    # the awe scenes: out of the cloud, and the first sight of the Pantheon
    for x in range(18, 27):
        g.trigger(x, TH - 3, "CloudBreak")
    for x in (20, 21, 22):
        g.trigger(x, STAIR2 - 1, "Pantheon")
    g.sign(17, 41, P + "SnowSign")
    g.accents(salt=53, rate=6)
    cl = cloud["ids"]
    g.save([cl[0][0] | (1 << 10), cl[0][1] | (1 << 10), cl[1][0] | (1 << 10), cl[1][1] | (1 << 10)],
           dict(map_type="MAP_TYPE_ROUTE", weather="WEATHER_SUNNY", show_map_name=False,
                allow_cycling=False, allow_escaping=False, requires_flash=False,
                music="MUS_VICTORY_ROAD", ichor_kind="dungeon"),
           connections=[dict(map="MAP_ASCENT_GLACIER", offset=0, direction="down")])
    entry = (21, TH - 1)
    must = [("door", (DOOR[0], DOOR[1] + 1)), ("sockets", (15, 25)), ("cloud bank", (30, 24)),
            ("full heal", (14, 34)), ("candy", (26, 4)), ("pp up", (31, 21)), ("shrine", (28, 36))]
    # the keeper steps aside once beaten
    g.events["object_events"][-1]["x"] = KEEPER[0] - 1
    seen = g.check(entry, must)
    g.events["object_events"][-1]["x"] = KEEPER[0]
    g.check(entry, [("keeper", KEEPER)])
    kx, ky = KEEPER
    s = f"""// Ascent 3F (design/maps/Ascent_3F.md): above the cloud line, the processional stair
// climbs three terraces to the Pantheon's propylaia. Generated by
// tools/ichor/maps/ascent_summit.py: edit the builder, not this file.

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
movement Ascent_3F_Movement_CameraToGate {{ walk_slow_up * 3 walk_up * 9 }}
movement Ascent_3F_Movement_CameraFromGate {{ walk_faster_down * 12 }}
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

script Ascent_3F_EventScript_Pantheon {{
    if (flag(FLAG_ICHOR_SEEN_PANTHEON)) {{
        end
    }}
    lockall
    setflag(FLAG_ICHOR_SEEN_PANTHEON)
    special(SpawnCameraObject)
    applymovement(OBJ_EVENT_ID_CAMERA, Ascent_3F_Movement_CameraToGate)
    waitmovement(0)
    delay(60)
    msgbox(format("At the top of the way, white against the blue: the Propylaia of the Pantheon.\\p"
                  "Six columns. Gold on the pediment: Zeus, with the thunderbolt in his fist.\\p"
                  "Behind it, the four seats of the Twelve. And above them all, the Archon."), MSGBOX_DEFAULT)
    closemessage
    delay(20)
    applymovement(OBJ_EVENT_ID_CAMERA, Ascent_3F_Movement_CameraFromGate)
    waitmovement(0)
    special(RemoveCameraObject)
    releaseall
}}

script Ascent_3F_EventScript_Polydamas {{
    trainerbattle_single(TRAINER_ICHOR_ASCENT_POLYDAMAS,
        format("Polydamas of Skotoussa. I won the pankration at Olympia barehanded.\\p"
               "The Archon set me on this stair. Nobody goes up who can't go through me."),
        format("…Through me. Go up, then."), Ascent_3F_EventScript_PolydamasAside)
    msgbox(format("The doors are just there. Hestia's fire is lit inside.\\p"
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
                  "Nobody comes in here that I can see. Back to the stair."), MSGBOX_DEFAULT)
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
"""
    s += sign_script(P, "Shrine",
                     "A stele of Zeus Ombrios, the rain-giver. Fragment V of the Olympian hymn:\\p"
                     "“From this height he saw every field below the cloud,\\p"
                     "and gave rain to the just and the unjust, since from up here he couldn't tell them apart.”")
    s += sign_script(P, "Sockets",
                     "Four sockets cut in a square in the stone, each the shape of a different key.\\p"
                     "Behind them a stair climbs into the summit cone, barred with bronze.\\p"
                     "Carved over it: STAND STILL.")
    s += sign_script(P, "CloudBank",
                     "Here the cloud never clears. It rolls up over the terrace's edge and won't go back down.\\p"
                     "Inside it, something whinnies. The wind itself would have to be told to move it.")
    s += sign_script(P, "SnowSign",
                     "THE PROCESSIONAL WAY\\nThree terraces, three stairs, the Propylaia.\\p"
                     "Above the cloud, the mountain belongs to the Twelve.")
    write_scripts("Ascent_3F", s)
    return g, seen, [("arrival", 21, 41), ("terrace1", 21, 36), ("stair1", 21, 30), ("sockets", 15, 24),
                     ("cloud_bank", 29, 24), ("stair2", 21, 17), ("procession", 21, 12), ("keeper", 21, 7),
                     ("propylaia", 21, 4)]
