#!/usr/bin/env python3
"""Write the four Pantheon seats' scripts.pory from one Elite Four template
(design/LEAGUE.md): Emerald's EverGrandeCity_*Room, adapted. Each seat:

- ON_FRAME at its VAR_ELITE_4_STATE: the walk-in, and the way in shuts;
- ON_LOAD: a beaten member's far way stays open (and the hall stays lit), a
  walked-in seat stays shut;
- the member's scene (2026-11-17): a short set piece in the god's own key
  before the battle: Ares's braziers flare and the files stamp, Poseidon's
  basin heaves under the trireme, Athena's lamps all brighten and Hypatia
  asks her question, Hera's torches catch one by one up the aisle;
- the member's battle (trainerbattle_no_intro: a loss is a whiteout, and
  EventScript_WhiteOut resets all four seats);
- the far way opens on the win (a door warp, or a gate whose trigger warps).

The cells swapped come from the tilesets' catalogs, as tools/ichor/maps/olympus.py
lays them, so they never go stale when a tileset is rebuilt.

Usage: python3 tools/ichor/maps/league_seats.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import league_lib as L  # noqa: E402

LAB = L.catalog("labyrinth")
DEM = L.catalog("temple_demeter")


def lab(key, name):
    s = LAB[key]
    cx, cy = s["names"][name]
    return s["ids"][cy][cx]


def dem(key, name):
    s = DEM[key]
    cx, cy = s["names"][name]
    return s["ids"][cy][cx]


def h(v):
    return f"0x{v:03X}"


def quad(key, x, y, names, getter=lab):
    return [(x + dx, y + dy, h(getter(key, n))) for (dx, dy), n in zip(((0, 0), (1, 0), (0, 1), (1, 1)), names)]


LIT = ("lit_tl", "lit_tr", "lit_bl", "lit_br")
ARES_LIT = quad("brazier", 6, 3, LIT) + quad("brazier", 11, 3, LIT)
HERA_TORCHES = [(y, [(x, y, h(dem("columns", "torch_lit"))), (x, y + 1, h(dem("columns", "bottom_lit")))])
                for y in (14, 10, 6) for x in (5, 13)]
HERA_BRAZIERS = [(x, 3, h(dem("braziers", "top_lit"))) for x in (5, 13)] + \
                [(x, 4, h(dem("braziers", "summer_lit"))) for x in (5, 13)]


def shake(h_, v, n, d):
    return [f"    setvar(VAR_0x8004, {h_})", f"    setvar(VAR_0x8005, {v})", f"    setvar(VAR_0x8006, {n})",
            f"    setvar(VAR_0x8007, {d})", "    special(ShakeCamera)", "    waitstate"]


def sets(cells, indent="    "):
    return [f"{indent}setmetatile({x}, {y}, {mid}, TRUE)" for x, y, mid in cells]


def hera_scene():
    out = []
    for i in range(0, len(HERA_TORCHES), 2):
        pair = HERA_TORCHES[i][1] + HERA_TORCHES[i + 1][1]
        out += sets(pair) + ["    special(DrawWholeMapView)", "    playse(SE_M_FLAME_WHEEL)", "    delay(24)"]
    out += sets(HERA_BRAZIERS) + ["    special(DrawWholeMapView)", "    playse(SE_M_FLAMETHROWER)", "    delay(30)"]
    return out


SEATS = [
    dict(map="Olympus_SeatOfAres", member="Brasidas", flag="FLAG_ICHOR_BEAT_BRASIDAS",
         trainer="TRAINER_ICHOR_BRASIDAS", state=(0, 1, 2), next_map="MAP_OLYMPUS_SEAT_OF_POSEIDON",
         close=[(9, 19, h(lab("floor", "void"))), (10, 19, h(lab("floor", "void")))],
         open_=[(9, 2, h(lab("arcade", "door_pier")) if False else
                 h(LAB["arcade"]["ids"][2][LAB["arcade"]["names"]["door_pier"][0]]))],
         gate=False, lit=ARES_LIT,
         scene=["    msgbox(format(\"Brasidas raises his spear. Fire catches in the braziers at his side.\"), MSGBOX_DEFAULT)",
                "    closemessage"] + sets(ARES_LIT) + ["    special(DrawWholeMapView)", "    playse(SE_M_FLAMETHROWER)",
                                                         "    delay(20)"] +
               ["    playse(SE_M_STRENGTH)"] + shake(0, 2, 3, 4) + ["    delay(10)", "    playse(SE_M_STRENGTH)"] +
               shake(0, 2, 3, 4) + ["    delay(10)", "    playse(SE_M_STRENGTH)"] + shake(0, 3, 4, 4) +
               ["    msgbox(format(\"Spear on shield, three times, from every rack in the hall: the Lakonian salute.\"), MSGBOX_DEFAULT)",
                "    closemessage"],
         intro=["Lakonians never asked how long. Only how well.",
                "I've held Ares's seat for twenty winters. Kleon wrote to me once. He was nine. He asked how to be glorious.",
                "I wrote back: stand where you're put, and don't look at the end of the line.",
                "Show me well."],
         defeat="Well. That was well.",
         post=["Go on. The admiral's next. Don't let him talk you into anything.",
               "If you see Kleon, tell him the polemarch said: well."]),
    dict(map="Olympus_SeatOfPoseidon", member="Themistokles", flag="FLAG_ICHOR_BEAT_THEMISTOKLES",
         trainer="TRAINER_ICHOR_THEMISTOKLES", state=(2, 3, 4), next_map="MAP_OLYMPUS_SEAT_OF_ATHENA",
         close=[(9, 20, "0x016"), (10, 20, "0x016")], open_=[(9, 2, "0x2BC"), (10, 2, "0x2BD")], gate=True,
         lit=[],
         scene=["    msgbox(format(\"Themistokles raps his staff on the trireme's bronze ram.\"), MSGBOX_DEFAULT)",
                "    closemessage",
                "    playse(SE_M_SURF)"] + shake(3, 0, 6, 5) +
               ["    playse(SE_M_WATERFALL)", "    delay(30)",
                "    msgbox(format(\"The basin heaves. A wave rolls under the hull, and every oar along its side lifts at once.\"), MSGBOX_DEFAULT)",
                "    closemessage"],
         intro=["The oracle told Astyra to trust its wooden wall. Everyone read walls.",
                "I read ships. We won at Salamis, and I keep that ship here so nobody forgets an oracle can be read two ways.",
                "I had Aristeides exiled once. Best thing I ever did for him. Nobody's too good to be wrong.",
                "Let's see which way you read me."],
         defeat="Read me right, didn't you.",
         extra=["script Olympus_SeatOfPoseidon_EventScript_WoodenWall {",
                '    msgbox(format("TRUST THE WOODEN WALL\\nThe oracle given to Astyra before Salamis.'
                '\\pUnder it, in a newer hand: “Read it twice.”"), MSGBOX_SIGN)',
                "}", ""],
         post=["Hypatia's next. She'll ask you a question. Don't answer with your name.",
               "Tell Aristeides I said hello. He'll hate that."]),
    dict(map="Olympus_SeatOfAthena", member="Hypatia", flag="FLAG_ICHOR_BEAT_HYPATIA",
         trainer="TRAINER_ICHOR_HYPATIA", state=(4, 5, 6), next_map="MAP_OLYMPUS_SEAT_OF_HERA",
         close=[(9, 20, "0x200")], open_=[(9, 2, "0x24D")], gate=True, lit=[],
         scene=["    msgbox(format(\"Hypatia rolls up the scroll she was reading. Somewhere above, an owl wakes.\"), MSGBOX_DEFAULT)",
                "    closemessage",
                "    playmoncry(SPECIES_SOPHOWL, CRY_MODE_NORMAL)",
                "    waitmoncry",
                "    fadescreenspeed(FADE_TO_WHITE, 2)",
                "    fadescreenspeed(FADE_FROM_WHITE, 2)",
                "    msgbox(format(\"Every lamp in the library brightens at once, as if the room were listening.\"), MSGBOX_DEFAULT)",
                "    closemessage",
                "    setspeaker(Ichor_League_Text_NameHypatia)",
                "    message(format(\"A question first. The only one I ever ask. Who are you?\"))",
                "    waitmessage",
                "    dynmultichoice(15, 6, FALSE, 3, 0, DYN_MULTICHOICE_CB_NONE, Olympus_SeatOfAthena_Text_MyName, "
                "Olympus_SeatOfAthena_Text_WhatIDid, Olympus_SeatOfAthena_Text_DontKnow)",
                "    setspeaker(Ichor_League_Text_NameHypatia)",
                "    if (var(VAR_RESULT) == 0) {",
                "        msgbox(format(\"That's what they call you. I asked who you are.\"))",
                "    } elif (var(VAR_RESULT) == 1) {",
                "        msgbox(format(\"Hm. A better answer than most. Deeds can be argued with, though.\"))",
                "    } else {",
                "        msgbox(format(\"The only honest answer anyone has ever given me. Let's find out together.\"))",
                "    }"],
         intro=["Every scroll in this room was written about someone. Every one of them has an ending.",
                "Not yours. No one wrote you.",
                "So who are you? Answer in battle. It's quicker."],
         defeat="That's an answer. I'll have to think about it.",
         extra=['text Olympus_SeatOfAthena_Text_MyName { "MY NAME." }',
                'text Olympus_SeatOfAthena_Text_WhatIDid { "WHAT I'
                "'VE DONE." + '" }',
                'text Olympus_SeatOfAthena_Text_DontKnow { "I DON' + "'T KNOW YET." + '" }', ""],
         post=["Most people answer with what they were told. You answered with what you did.",
               "Olympias waits beyond. She tells stories. Be careful which ones you believe."]),
    dict(map="Olympus_SeatOfHera", member="Olympias", flag="FLAG_ICHOR_BEAT_OLYMPIAS",
         trainer="TRAINER_ICHOR_OLYMPIAS", state=(6, 7, 8), next_map="MAP_OLYMPUS_SUMMIT",
         close=[(8, 21, "0x20D"), (9, 21, "0x20D"), (10, 21, "0x20D")],
         open_=[(14, 1, "0x23E"), (14, 2, "0x247")], gate=False,
         lit=[c for _, cs in HERA_TORCHES for c in cs] + HERA_BRAZIERS,
         scene=["    msgbox(format(\"Olympias rises from Hera's throne. At the door behind you, a torch catches.\"), MSGBOX_DEFAULT)",
                "    closemessage"] + hera_scene() +
               ["    msgbox(format(\"Fire runs up the aisle, column to column, to the braziers at her feet.\\p"
                "In the pits between the columns, the serpents lift their heads to the light.\"), MSGBOX_DEFAULT)",
                "    closemessage"],
         intro=["Hera's serpents keep this hall. She raised the Hydra, you know. She loved it.",
                "I told my son a god was his father. He believed me, and he conquered the world.",
                "Was I lying?",
                "Never mind. Let's see what you believe."],
         defeat="Hm. You don't need a god for a father.",
         post=["The summit's through that door. The Archon's waiting at the altar.",
               "He's a good man who did one brave thing and has been ashamed of it ever since.",
               "Mothers notice these things."]),
]


def text(lines):
    return 'format("' + "\\p".join(lines) + '")'


def seat(s):
    P = s["map"] + "_EventScript_"
    into, walked, won = s["state"]
    out = [f"// {s['map']}: {s['member']}'s seat in the Pantheon (design/LEAGUE.md).",
           "// Generated by tools/ichor/maps/league_seats.py: edit the generator, not this file.",
           "",
           f"mapscripts {s['map']}_MapScripts {{",
           "    MAP_SCRIPT_ON_LOAD {",
           f"        if (flag({s['flag']})) {{",
           f"            call({P}SetOpen)",
           "        }",
           f"        if (var(VAR_ELITE_4_STATE) == {walked} || var(VAR_ELITE_4_STATE) == {won}) {{",
           f"            call({P}SetClosed)",
           "        }",
           "    }",
           "    MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE [",
           f"        VAR_TEMP_1, 0: {P}FaceNorth",
           "    ]",
           "    MAP_SCRIPT_ON_FRAME_TABLE [",
           f"        VAR_ELITE_4_STATE, {into}: {P}WalkIn",
           "    ]",
           "}",
           "",
           f"script {P}FaceNorth {{",
           "    turnobject(LOCALID_PLAYER, DIR_NORTH)",
           "}",
           "",
           f"script {P}WalkIn {{",
           "    lockall",
           "    call(Ichor_League_EventScript_WalkIn)",
           f"    call({P}SetClosed)",
           "    special(DrawWholeMapView)",
           f"    setvar(VAR_ELITE_4_STATE, {walked})",
           "    releaseall",
           "}",
           "",
           f"script {P}SetClosed {{"]
    out += [f"    setmetatile({x}, {y}, {mid}, TRUE)" for x, y, mid in s["close"]]
    out += ["    return", "}", "", f"script {P}SetOpen {{"]
    out += [f"    setmetatile({x}, {y}, {mid}, FALSE)" for x, y, mid in s["open_"]]
    out += sets(s["lit"])
    out += ["    return", "}", "",
            f'text {s["map"]}_Text_Defeat {{ "{s["defeat"]}" }}',
            "",
            f"script {P}{s['member']} {{",
            "    lock",
            "    faceplayer",
            f"    setspeaker(Ichor_League_Text_Name{s['member']})",
            f"    if (flag({s['flag']})) {{",
            f"        msgbox({text(s['post'])})",
            "        release",
            "        end",
            "    }",
            "    playbgm(MUS_ENCOUNTER_ELITE_FOUR, FALSE)",
            "    setspeaker(SP_NAME_NONE)"]
    out += s["scene"]
    out += [f"    setspeaker(Ichor_League_Text_Name{s['member']})",
            f"    msgbox({text(s['intro'])})",
            f"    trainerbattle_no_intro({s['trainer']}, {s['map']}_Text_Defeat)",
            f"    setflag({s['flag']})",
            f"    setvar(VAR_ELITE_4_STATE, {won})",
            f"    call({P}SetOpen)",
            "    call(Ichor_League_EventScript_DoorOpened)",
            f"    setspeaker(Ichor_League_Text_Name{s['member']})",
            f"    msgbox({text(s['post'])})",
            "    release",
            "}",
            ""]
    if s["gate"]:
        out += [f"script {P}ExitGate {{",
                "    lockall",
                f"    if (!flag({s['flag']})) {{",
                "        releaseall",
                "        end",
                "    }",
                "    playse(SE_DOOR)",
                "    waitse",
                f"    warp({s['next_map']}, 0)",
                "    waitstate",
                "    releaseall",
                "}",
                ""]
    out += s.get("extra", [])
    return "\n".join(out)


def main():
    for s in SEATS:
        (ROOT / f"data/maps/{s['map']}/scripts.pory").write_text(seat(s))


if __name__ == "__main__":
    main()
