#!/usr/bin/env python3
"""Build the Sacred Way: Route 15 (the road of the Mysteries, Eleusa's east gate
to Daphni), Daphni, and Route 16 (the capital pass, Daphni to Astyra's gate),
with their events, scripts, wild tables, new trainers' parties, herms, Daphni's
three rooms, checks and review renders. This file owns those three maps and
Daphni's rooms; nemea.roads() and astyra.py's daphni() no longer write them.

Design: AETHOS_MAP.md (Routes 15-16, Daphni), PITCH.md Act II (the Astyra
arrival), WORLD_EXPLORATION.md §5.5 (A1 the jesters' bridge, A2 the Aigaleo
lookout, A8 the pass gap), DISTRIBUTION.md (Korantha, Persenyx, Melisseer on
Route 15; Sophowl and Ophidrop on Route 16). Each map's finds and its hooks
for later are in design/maps/<Map>.md.

Route 15, the road of the Mysteries (80x34). *The procession's road from
Eleusis to the city, walked backwards.* Eleusa's gate and the Thriasian
olives (Timon in plain view), the Rheitoi: two salt lakes with the causeway
between them (band 1 after Hegeso), the priest-fishers' beach, the jesters'
broken bridge and the jester on his islet (the Conch). Then the Aigaleo pass:
the stair up the scarp (Polemon at its head), the terrace road (band 2,
Phila), the herm and the pilgrims' spring (the rest), Aphrodite's niches in the
rock, the shrine court where two column drums seat on two plates and open a
stair down to Kore's hollow (the Girdle; a TM), the ledge back down, the foot
meadow and the old quarry under it (Pan's Crook). Down the east side: the
gully to the Iakchos glade and its cold torch-stand (the Hammer, then Hecate's
Torch), the thicket over Demeter's wayside altar (the Sickle), Agis, band 3,
Praxon, and Daphni's laurels.

Daphni (40x34). *Apollo's laurels at the top of the pass.* The sanctuary of
Apollo Daphnaios on its paving inside the laurel grove (a room), the prayer
laurel whose cord cuts its bark (the Sickle), the Aigaleo lookout up the rock
behind the grove (Pan's Crook; the traveler from the east, A2), the pilgrims'
rest with the healer and the merchant on its porch (a room), the laurel-cutter's
cottage (a room), and the travel herm at the west road.

Route 16, the capital pass (72x36). *Down to the Kephisos, through the
potters' graves, up to the city's gate.* Nikias at Daphni's foot, Timarete, the
Kephisos ford (band 1) and its islet (the Conch), the Kerameikos: grave plots
along the road, a drum in a plot gap (the Girdle), a rubble-filled plot (the
Hammer) and a tomb behind a double-axe seal (the Labrys); the Akademia's olives
behind a thicket (the Sickle) and Aristokles in his grove. Then the climb: the
scarp stair (Ariston), the terrace (band 2, Straton), the Nymphs' shrine up
the rock (Pan's Crook), the lookout seat where the Akropolis comes into view
the first time (a scene), the ditch and the fallen span (Daedalus's Wings),
Eubios at the gate, and Astyra.

Pieces come from build/skiron/catalog.json (make it with
/usr/bin/python3 tools/ichor/art/skiron_build.py --no-compile).

Usage: /usr/bin/python3 tools/ichor/maps/sacredway.py [--render DIR] [--stem-suffix S] [--walk] [--no-rooms]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools/ichor"))
sys.path.insert(0, str(ROOT / "tools/ichor/maps"))
sys.path.insert(0, str(ROOT / "tools/ichor/art"))
import kithairon as K  # noqa: E402  (the Skiron grid, painters and walks)
import nemea as N  # noqa: E402  (water, massif, seam columns, events, checks, renders)
import route5 as R5  # noqa: E402
import water_tables  # noqa: E402
import plan_hook  # noqa: E402  (tools/ichor/wild_plan.py)

def ellipse(g, ch, cx, cy, rx, ry, only=None):
    """A smooth ellipse (a lake's shore wants no jitter)."""
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if 0 <= x < g.w and 0 <= y < g.h and ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1 \
                    and (only is None or g.g[y][x] in only):
                g.g[y][x] = ch


blob, stamp, trainer, sign, talker, item, hidden, gift = (N.blob, N.stamp, N.trainer, N.sign, N.talker,
                                                         N.item, N.hidden, N.gift)
GFX = "OBJ_EVENT_GFX_ICHOR_"
R15, DAPHNI, R16 = "Route15_MysteryRoad", "Daphni", "Route16_CapitalPass"
SANCTUARY, REST, COTTAGE_ROOM = "Daphni_Sanctuary", "Daphni_PilgrimsRest", "Daphni_LaurelHouse"
MAP_ID = {R15: "MAP_ROUTE15_MYSTERY_ROAD", DAPHNI: "MAP_DAPHNI", R16: "MAP_ROUTE16_CAPITAL_PASS"}
HERM, SIGN = R5.HERM, R5.SIGN
TRIPOD, ALTAR = 0x130, 0x131

# --- the seams ---------------------------------------------------------------------------
# Eleusa's east gate is its x 49, rows 24-27 (Route 15 sits at offset 14: our rows 10-13).
ELEUSA_OFFSET = 14
# Route 15's east road (rows 16-19) runs straight on through Daphni into Route 16.
# Astyra's west road is its rows 32-35; Route 16's east road is rows 10-13 (offset -22).
ASTYRA_OFFSET = -22

# ---------------------------------------------------------------------------
# Flags: every new name this file uses, claimed from world-act2's bank range
# (tools/ichor/claim_ranges.md, "The Sacred Way"). The old road's flags
# (FLAG_ICHOR_ITEM_R15_*, FLAG_ICHOR_HIDDEN_ITEM_R15_* and R16's) are kept.
# ---------------------------------------------------------------------------
BANK_RANGE = "0x590-0x5AF"
FLAG_NOTES = {}


def flag(name, note):
    FLAG_NOTES[name] = note
    return name


def claim_flags():
    """Claim each flag this file names that flags.h doesn't define yet (reruns are no-ops)."""
    text = (ROOT / "include/constants/flags.h").read_text()
    for name, note in FLAG_NOTES.items():
        if re.search(rf"#define {name}\b", text):
            continue
        kind = "hiddenitem" if name.startswith("FLAG_ICHOR_HIDDEN_ITEM_") else "bankflag"
        subprocess.run([sys.executable, str(ROOT / "tools/ichor/claim.py"), "--range", BANK_RANGE, kind, name,
                        "Sacred Way: " + note], check=True, capture_output=True)
        text = (ROOT / "include/constants/flags.h").read_text()


F = {
    "r15_islet": flag("FLAG_ICHOR_ITEM_R15_ISLET", "Route 15: the jester's islet jar (the Conch)"),
    "r15_quarry": flag("FLAG_ICHOR_ITEM_R15_QUARRY", "Route 15: the Aigaleo quarry jar (Pan's Crook)"),
    "r15_hollow": flag("FLAG_ICHOR_ITEM_R15_HOLLOW", "Route 15: Kore's hollow jar, under the shrine court's stair"),
    "r15_altar": flag("FLAG_ICHOR_ITEM_R15_ALTAR", "Route 15: Demeter's wayside altar jar (the Sickle)"),
    "r15_h_niches": flag("FLAG_ICHOR_HIDDEN_ITEM_R15_NICHES", "Route 15: in Aphrodite's rock niches"),
    "r15_h_quarry": flag("FLAG_ICHOR_HIDDEN_ITEM_R15_QUARRY", "Route 15: in the quarry's spoil"),
    "r15_priest": flag("FLAG_ICHOR_R15_PRIEST_GIFT", "Route 15: the Rheitoi priest-fisher's gift"),
    "r15_seal": flag("FLAG_ICHOR_R15_SHRINE_STAIR", "Route 15: both drums on the shrine court's plates; the stair down is open"),
    "r15_torch": flag("FLAG_ICHOR_R15_IAKCHOS_LIT", "Route 15: Iakchos's torch-stand lit with Hecate's Torch"),
    "r15_torch_gift": flag("FLAG_ICHOR_R15_IAKCHOS_GIFT", "Route 15: the torchbearer's thanks for the lit stand"),
    "d_cord": flag("FLAG_ICHOR_DAPHNI_CORD_CUT", "Daphni: the cord cut from the prayer laurel (the Sickle)"),
    "d_priestess": flag("FLAG_ICHOR_DAPHNI_PRIESTESS_GIFT", "Daphni: the priestess's laurel crown"),
    "d_kykeon": flag("FLAG_ICHOR_DAPHNI_KYKEON_GIFT", "Daphni: Iambe's kykeon at the pilgrims' rest"),
    "d_trade": flag("FLAG_ICHOR_DAPHNI_HONEY_TRADE", "Daphni: the initiate's berries for a Honey"),
    "d_weaver": flag("FLAG_ICHOR_DAPHNI_WEAVER_GIFT", "Daphni: the laurel-cutter's gift, after the capital"),
    "d_lookout": flag("FLAG_ICHOR_ITEM_DAPHNI_LOOKOUT", "Daphni: the Aigaleo lookout's jar (Pan's Crook)"),
    "d_h_laurel": flag("FLAG_ICHOR_HIDDEN_ITEM_DAPHNI_LAUREL", "Daphni: among the laurel roots"),
    "d_h_rest": flag("FLAG_ICHOR_HIDDEN_ITEM_DAPHNI_REST", "Daphni: behind the pilgrims' rest"),
    "d_h_seat": flag("FLAG_ICHOR_HIDDEN_ITEM_DAPHNI_SEAT", "Daphni: under the stone seat on the lookout"),
    "d_traveler": flag("FLAG_ICHOR_DAPHNI_TRAVELER_TOLD", "Daphni: the traveler from the east told of the Troad"),
    "r16_islet": flag("FLAG_ICHOR_ITEM_R16_ISLET", "Route 16: the Kephisos islet jar (the Conch)"),
    "r16_tomb": flag("FLAG_ICHOR_ITEM_R16_TOMB", "Route 16: the sealed tomb's jar (the Labrys)"),
    "r16_span": flag("FLAG_ICHOR_ITEM_R16_SPAN", "Route 16: the fallen span's pier jar (Daedalus's Wings)"),
    "r16_grove": flag("FLAG_ICHOR_ITEM_R16_GROVE", "Route 16: the Akademia grove's jar (the Sickle)"),
    "r16_h_plot": flag("FLAG_ICHOR_HIDDEN_ITEM_R16_PLOT", "Route 16: in the rubble-filled grave plot (the Hammer)"),
    "r16_h_drum": flag("FLAG_ICHOR_HIDDEN_ITEM_R16_DRUM", "Route 16: in the plot behind the fallen drum (the Girdle)"),
    "r16_h_shrine": flag("FLAG_ICHOR_HIDDEN_ITEM_R16_SHRINE", "Route 16: at the Nymphs' shrine (Pan's Crook)"),
    "r16_view": flag("FLAG_ICHOR_R16_AKROPOLIS_SEEN", "Route 16: the first sight of the Akropolis from the lookout"),
    "r16_sage": flag("FLAG_ICHOR_R16_AKADEMIA_GIFT", "Route 16: Aristokles's gift in the Akademia's grove"),
}
OLD = {"r15_heal": "FLAG_ICHOR_ITEM_R15_HEAL", "r15_ball": "FLAG_ICHOR_ITEM_R15_BALL",
       "r15_ether": "FLAG_ICHOR_ITEM_R15_ETHER", "r16_heal": "FLAG_ICHOR_ITEM_R16_HEAL",
       "r16_ball": "FLAG_ICHOR_ITEM_R16_BALL", "r16_ether": "FLAG_ICHOR_ITEM_R16_ETHER"}

# --- trainers: the old road's twelve keep their ids; the new ones are world-act2's
# 1344-1352 (claim_ranges.md, "The Sacred Way").
NEW_TRAINERS = {
    "R15_KERKOPS": 1344, "R15_SIMMIAS": 1345, "R15_THEOXENOS": 1346, "R15_LAMPON": 1347,
    "R15_KALLIDIKE": 1348, "R16_EXEKIAS": 1349, "R16_SPEUSIPPOS": 1350, "R16_MENEXENOS": 1351,
    "R16_STRATON": 1352,
}


class Spec(N.Spec):
    """nemea's Spec, with coord triggers and scripts written in place."""

    def trigger(self, x, y, script, var="VAR_TEMP_1", value="0"):
        self.coords.append(dict(type="trigger", x=x, y=y, elevation=0, var=var, var_value=value,
                                script=self.px + script))

    def script(self, name, body):
        self.scripts.append(f"script {self.px}{name} {{\n{body}\n}}")

    def person(self, name, gfx, x, y, facing="DOWN", flag="0"):
        self.people.append((name, gfx, x, y, facing, flag))


def write_events(spec, music="MUS_ICHOR_ROAD", kind="MAP_TYPE_ROUTE", mapscripts=None, extra=None):
    path = ROOT / f"data/maps/{spec.name}/map.json"
    m = json.loads(path.read_text())
    m.update(music=music, map_type=kind, connections=spec.connections or None,
             object_events=spec.objects(), warp_events=spec.warps, coord_events=spec.coords,
             bg_events=spec.bgs())
    if extra:
        m.update(extra)
    path.write_text(json.dumps(m, indent=2) + "\n")
    scripts = [mapscripts or f"mapscripts {spec.name}_MapScripts {{}}",
               "// Generated by tools/ichor/maps/sacredway.py; edit the builder, not this file."]
    for t in spec.trainers:
        tid = t.get("id", f"TRAINER_ICHOR_{spec.tag}_{t['name']}")
        scripts.append(f'''script {spec.px}{t["name"]} {{
    trainerbattle_single({tid}, format("{t["intro"]}"), format("{t["defeat"]}"))
    msgbox(format("{t["after"]}"), MSGBOX_AUTOCLOSE)
    end
}}''')
    scripts += spec.scripts
    (ROOT / f"data/maps/{spec.name}/scripts.pory").write_text("\n\n".join(scripts) + "\n")


def laurels(g, ch="L"):
    """Daphni's laurel grove: bay laurels (the Skiron myrtle) among cypresses,
    stone pines and a few oaks; every cell of it solid and looking it."""
    def free(x, y):
        return 0 <= x < g.w and 0 <= y < g.h and g.g[y][x] == ch and not g.fixed[y, x]
    for y in range(g.h):
        for x in range(g.w):
            if not free(x, y):
                continue
            n = K.noise(x, y, 91)
            seam = g.seam(x, y) or x in g.cols
            if n < 10 and all(free(x + i, y + j) for i in range(2) for j in range(2)) and \
                    (not seam or (x + 1) in g.cols):
                for j in range(2):
                    for i in range(2):
                        g.set(x + i, y + j, R5.STONE_PINE[j][i], True, "laurel")
            elif n < 30 and free(x, y + 1):
                g.set(x, y, R5.CYPRESS_TOP, True, "laurel")
                g.set(x, y + 1, R5.CYPRESS_BOT, True, "laurel")
            elif seam:
                g.set(x, y, R5.BOULDER, True, "laurel")
            elif n < 80:
                g.piece("myrtle", x, y, kind="laurel")
            elif n < 92:
                g.piece("oak", x, y, kind="laurel")
            else:
                g.piece("rock", x, y, kind="laurel")


# ---------------------------------------------------------------------------
# Route 15, the road of the Mysteries (80x34)
# ---------------------------------------------------------------------------
R15_W, R15_H = 80, 34
R15_DRUMS, R15_PLATES = [(49, 9), (51, 9)], [(47, 9), (53, 9)]
R15_STAIR_X = 50                    # the shrine court's stair down to Kore's hollow (closed until the seal)
R15_TORCH = (65, 3)
R15_HERM = (48, 4)


def plan_r15():
    W, H = R15_W, R15_H
    g = N.Grid(R15, W, H, west=True, east=True)
    r = g.rect
    r("#", 0, 0, W - 1, H - 1)
    # --- Eleusa's gate and the Thriasian plain (aethos strip x 0-7) ---------------
    r("o", 0, 0, 11, 8)
    r("o", 0, 15, 11, H - 1)
    r(".", 1, 9, 9, 14)
    r("p", 0, 10, 9, 13)
    g.put("k", (3, 9))                         # the west sign
    r(".", 2, 2, 8, 7)                         # the north field among the olives
    blob(g, ",", 5, 4.5, 3, 2.2, 1, only=".")
    r(".", 6, 8, 7, 8)
    r(".", 2, 19, 9, 25)                       # the south field
    blob(g, ",", 5.5, 22, 3.4, 2.6, 3, only=".")
    r(".", 4, 15, 5, 18)
    g.put(".", (9, 9))                         # Timon's post
    r(".", 10, 11, 11, 17)                     # the road bends down to the causeway
    r("p", 10, 13, 11, 16)
    r("p", 8, 12, 11, 13)
    # --- the Rheitoi: two salt lakes, the causeway between them -----------------
    # the north lake: the causeway's embankment is straight, the far shores are not
    ellipse(g, "~", 22, 5, 9.2, 7.5)
    r("~", 14, 9, 30, 13)
    r("_", 12, 1, 13, 13)                      # the priest-fishers' beach
    r("k", 12, 1, 13, 2)                       # their hut
    for y in range(0, 13):                     # a sandy lip on the beach side only
        if g.g[y][14] == "~" and y < 9:
            g.put("_", (14, y))
    # the south lake, its islet, and the jesters' broken bridge
    r("~", 13, 18, 30, 21)
    ellipse(g, "~", 21.5, 25, 9.2, 8)
    r(".", 12, 14, 31, 17)                     # the causeway
    r("p", 12, 15, 31, 16)
    r(",", 17, 14, 20, 17)                     # band 1, walled by the lakes
    g.put(".", (22, 14))                       # Hegeso's spot
    r("A", 24, 18, 25, 20)                     # the bridge's stub, its span gone
    g.put("k", (23, 18))                       # its sign
    ellipse(g, "_", 24.5, 24.8, 3.9, 2.6, only="~")   # the islet across the gap (the Conch)
    ellipse(g, ".", 24.5, 24.9, 2.7, 1.5, only="_")
    r("A", 24, 22, 25, 22)                     # the span's far stub
    g.put(",", (23, 25), (22, 25))
    N.round_pools(g)
    # --- the Aigaleo pass: the scarp, its two stairs and the ledge --------------
    r(".", 32, 14, 35, 17)
    r("p", 32, 15, 35, 16)
    r("p", 34, 13, 35, 14)
    for y, ch in ((11, "b"), (12, "u"), (13, "f")):
        r(ch, 32, y, 59, y)
        r("s" if ch == "u" else "p", 34, y, 35, y)      # the west stair
        r("s" if ch == "u" else "p", 55, y, 56, y)      # the east stair
        r("v" if ch == "u" else ".", 44, y, 46, y)      # the ledge back down
        r("s" if ch == "u" else "p", R15_STAIR_X, y, R15_STAIR_X, y)   # the hollow's stair (shut)
    # the upper terrace: the stair head, band 2, the clearing
    r(".", 33, 2, 57, 10)
    r("^", 33, 2, 38, 4)
    r("^", 33, 5, 33, 10)
    r("^", 36, 8, 38, 10)
    g.put(".", (36, 9))                        # Polemon's niche
    r("p", 34, 6, 35, 10)
    r("p", 34, 6, 56, 7)
    r("p", 55, 8, 56, 10)
    r("^", 39, 2, 44, 5)
    r("^", 39, 8, 44, 10)
    r(",", 40, 6, 43, 7)                       # band 2
    r("^", 45, 2, 45, 5)
    r("^", 45, 9, 46, 10)
    g.put(".", (45, 8))                        # Phila's niche
    r("#", 33, 0, 60, 1)
    r("#", 58, 2, 60, 10)
    g.put("k", R15_HERM)                       # the herm
    r("k", 50, 2, 52, 4)                       # the pilgrims' spring
    r("k", 54, 1, 56, 3)                       # Aphrodite's niches
    blob(g, ",", 54, 5, 1.5, .6, 7, only=".")
    # the shrine court above the hollow's stair: two drums, two plates
    r(".", 47, 8, 54, 10)
    for x, y in R15_PLATES:
        g.put("A", (x, y))
    g.put("k", (54, 8))                        # the reset post
    # the foot meadow under the scarp (the ledge lands here) and Kore's hollow
    r("^", 36, 14, 57, H - 1)
    r(".", 36, 14, 48, 15)
    blob(g, ",", 41.5, 14.5, 5, 1.4, 4, only=".")
    r(".", 49, 14, 52, 16)                     # Kore's hollow, under the court
    # the quarry below the meadow (Pan's Crook down the face)
    for y, ch in ((16, "b"), (17, "u"), (18, "f")):
        r(ch, 37, y, 48, y)
    r("_", 37, 19, 48, 25)                     # the quarry floor: marble dust
    blob(g, ".", 41, 22.5, 4.5, 2.4, 25, only="_")
    blob(g, ",", 42, 22.5, 3.2, 1.6, 5, only=".")
    r("k", 46, 19, 47, 20)                     # cut blocks waiting for a cart
    # Aigaleo's south spur: bare rock under the pass
    for x in range(32, 71):
        r("M", x, 28 + K.noise(x // 2, 3, 41) % 3 + (1 if 52 <= x <= 58 else 0), x, H - 1)
    # --- the descent to Daphni ---------------------------------------------------
    r(".", 53, 14, 61, 19)
    r("p", 55, 14, 56, 18)
    r("p", 55, 17, W - 1, 18)
    r("#", 53, 14, 54, 16)
    r("#", 57, 14, 61, 16)
    r("#", 57, 19, 61, 19)
    g.put(".", (59, 16))                       # Agis's niche
    r(".", 62, 16, 67, 19)
    r(",", 63, 16, 66, 19)                     # band 3, right after Agis
    r(".", 68, 16, W - 1, 19)
    r("#", 68, 20, 71, 21)
    g.put("k", (64, 15), (66, 15), (70, 15), (70, 20), (71, 20))   # graves along the Sacred Way
    g.put(".", (69, 20))                       # Praxon's niche
    g.put("k", (73, 15))                       # the east sign
    # the Iakchos glade north of the road, up a rubble-choked gully (the Hammer)
    r(".", 62, 12, 62, 15)
    r(".", 61, 2, 70, 11)
    blob(g, ",", 66, 7, 4.6, 3.8, 8, only=".")
    r("#", 61, 2, 62, 4)
    r("#", 69, 9, 70, 11)
    g.put("k", R15_TORCH, (R15_TORCH[0], R15_TORCH[1] + 1))
    # Demeter's wayside altar south of the road, behind a thicket (the Sickle)
    r("#", 53, 19, 56, 19)
    g.put(".", (58, 19), (58, 20))
    r(".", 56, 21, 66, 28)
    blob(g, ",", 62, 25, 4.5, 2.6, 9, only=".")
    r("k", 59, 22, 59, 23)                     # the altar
    r("#", 56, 27, 58, 28)
    return g


def props_r15(g):
    g.set(3, 9, SIGN, True, "sign")
    g.set(73, 15, SIGN, True, "sign")
    g.set(23, 18, SIGN, True, "sign")
    g.set(*R15_HERM, HERM, True, "herm")
    stamp(g, N.SPRING, 50, 2, kind="spring")
    g.piece("niches", 54, 1)
    g.piece("tent", 12, 1)
    g.piece("stele_low", 54, 8)
    g.set(R15_TORCH[0], R15_TORCH[1], TRIPOD, True, "torch")
    g.set(R15_TORCH[0], R15_TORCH[1] + 1, ALTAR, True, "torch")
    g.set(59, 22, TRIPOD, True, "altar")
    g.set(59, 23, ALTAR, True, "altar")
    # the crook's face down to the quarry (WORLD_EXPLORATION §2)
    g.named("crook", "brink", 43, 16)
    g.named("crook", "face_u", 43, 17)
    g.named("crook", "foot", 43, 18)
    # the procession's litter: sherds and offerings along the road, spoil in the quarry
    g.piece("rubble", 46, 19)
    for x, key in ((64, "stele_low"), (66, "stele_family"), (70, "stele_low")):
        g.piece("stele_low" if key == "stele_family" else key, x, 15)
    g.piece("sarcophagus", 70, 20) if not g.seam(70, 20) else None
    for key, x, y in (("sherds", 31, 14), ("milestone", 9, 14), ("rock", 38, 22), ("rubble_small", 45, 21),
                      ("boulders", 39, 24), ("stele_palmette", 68, 2), ("pebbles", 57, 8), ("baskets", 13, 3),
                      ("amphorae", 65, 21), ("milestone", 60, 18), ("rock_path", 44, 24), ("sherds", 40, 20)):
        if key == "milestone" and g.g[y][x] == "p":
            key = "milestone_path"
        if key in ("sherds", "pebbles", "milestone_path") or not g.fixed[y, x]:
            g.piece(key, x, y)


def spec_r15():
    s = Spec(R15, MAP_ID[R15], "R15")
    s.connections = [{"direction": "left", "map": "MAP_ELEUSA_VILLAGE", "offset": -ELEUSA_OFFSET},
                     {"direction": "right", "map": "MAP_DAPHNI", "offset": 0}]
    trainer(s, "TIMON", "HOPLITE", 9, 9, "DOWN", 4,
            "Eleusa's east watch. Everyone on the Mysteries' road gets one look from me.",
            "Go on, then. The lakes are just past the olives.",
            "Daphni's healer tends travelers at the top of the pass.")
    trainer(s, "HEGESO", "HARVESTER", 22, 14, "DOWN", 3,
            "Salt on the wind, salt in the grass. My Pokémon love it out here.", "Ugh. Briny luck.",
            "Only the priests may fish the Rheitoi. The fish are the goddesses'.")
    trainer(s, "POLEMON", "PILGRIM", 36, 9, "LEFT", 2,
            "The procession climbs this stair every autumn. Show me you can climb it.", "You'll do.",
            "Up top there's a spring. Drink before you pray.")
    trainer(s, "PHILA", "ACOLYTE_F", 45, 8, "UP", 2,
            "Aphrodite's niches are just ahead. No rushing past the goddess.", "...Fine. Rush.",
            "People leave little clay doves in the rock up there.")
    trainer(s, "AGIS", "SHEPHERD", 59, 16, "DOWN", 2,
            "My sheep graze the pass and I graze on challengers.", "Shorn!",
            "Daphni's just down the hill. Smell the laurel?")
    trainer(s, "PRAXON", "AUGUR", 69, 20, "UP", 4,
            "The birds over Daphni fly east today. Toward the city. Toward trouble.", "The birds were right.",
            "Apollo's laurels. Go and see the god's house.")
    trainer(s, "KERKOPS", "YOUTH_M", 24, 23, "UP", 2,
            "Hey, pilgrim! Your hat's a disgrace and your Pokémon smell of goat!\\pThat's the custom. Insult me back!",
            "Ha! That stung. The goddess laughed, at least.",
            "When Demeter grieved, old Iambe made her laugh with filth. So we jest at the bridge.",
            mandatory=False)
    trainer(s, "SIMMIAS", "GOATHERD", 40, 21, "RIGHT", 3,
            "This marble built half the city. The other half's in my boots.", "Cracked like a bad block.",
            "The good stone's deep. Mind the face on your way up.", mandatory=False)
    trainer(s, "THEOXENOS", "PILGRIM", 39, 15, "UP", 1,
            "I hopped the ledge to skip the climb. Don't tell the procession.", "Caught out.",
            "The ledge is a shortcut home. Not a shortcut up.", mandatory=False)
    trainer(s, "LAMPON", "ACOLYTE_M", 64, 9, "LEFT", 3,
            "In the Mysteries we carry Iakchos by torchlight. Carry this battle!", "My torch is out.",
            "That stand held Iakchos's torch. It's gone cold since the Titans came.", mandatory=False)
    trainer(s, "KALLIDIKE", "HARVESTER", 63, 23, "LEFT", 3,
            "King Keleos's daughters met Demeter at a well. I met you at an altar.",
            "Mother will hear of this.", "Leave a little barley at the altar. She notices.",
            mandatory=False)
    for t in s.trainers:
        if "R15_" + t["name"] in NEW_TRAINERS:
            t["id"] = "TRAINER_ICHOR_R15_" + t["name"]
    s.people += [("Priest", "FISHER", 13, 6, "LEFT", "0"),
                 ("SpringKeeper", "WOMAN", 51, 5, "DOWN", "0")]
    s.thickets += [("AltarThicket", 58, 19, "0")]
    s.gate("GullyRubble", "BREAKABLE_ROCK", 62, 14, "EventScript_RockSmash", "0")
    for i, (x, y) in enumerate(R15_DRUMS):
        s.gate(f"Drum{i + 1}", "PUSHABLE_BOULDER", x, y, "EventScript_StrengthBoulder")
    item(s, "HYPER_POTION", 3, 4, "ITEM_R15_HEAL")
    item(s, "ULTRA_BALL", 8, 23, "ITEM_R15_BALL")
    item(s, "ETHER", 68, 4, "ITEM_R15_ETHER")
    s.items += [("ITEM_BIG_PEARL", 27, 24, F["r15_islet"]), ("ITEM_HARD_STONE", 47, 24, F["r15_quarry"]),
                ("ITEM_TM22", 51, 15, F["r15_hollow"]), ("ITEM_BIG_ROOT", 65, 27, F["r15_altar"])]
    hidden(s, "HONEY", 9, 19, "HIDDEN_ITEM_R15_HONEY")          # the south field's corner hive
    hidden(s, "REVIVE", 13, 12, "HIDDEN_ITEM_R15_REVIVE")       # the priests' beach
    hidden(s, "SUPER_REPEL", 70, 2, "HIDDEN_ITEM_R15_REPEL")    # the Iakchos glade's far corner
    s.hidden += [("ITEM_HEART_SCALE", 55, 3, F["r15_h_niches"]), ("ITEM_STAR_PIECE", 38, 25, F["r15_h_quarry"])]
    sign(s, "Sign0", 3, 9, "Route 15, the road of the Mysteries.\\nWest: Eleusa. East: the salt lakes, the pass and Daphni.")
    sign(s, "Sign1", 73, 15, "Route 15.\\nEast: Daphni. West: over the Aigaleo pass, the salt lakes and Eleusa.")
    sign(s, "Bridge", 23, 18, "The procession's bridge. Its middle span lies in the lake.\\p"
         "On the islet across the gap, a masked man is shouting at everyone who passes.\\p"
         "With a way over the water, you could shout back.")
    s.signs.append((R15_HERM[0], R15_HERM[1], "ANY", "Herm"))
    s.script("Herm", "    goto(EventScript_IchorGreatHerm)")
    sign(s, "Niches", 55, 3, "Niches cut in the living rock, full of clay doves and little offerings.\\p"
         "Aphrodite's shrine on the Sacred Way. The procession stops here to rest.", "NORTH")
    sign(s, "Altar", 59, 23, "A wayside altar of Demeter and Kore, sheaves carved on its sides.\\p"
         "Someone has kept it swept, even here.")
    s.signs += [(R15_TORCH[0], R15_TORCH[1] + 1, "ANY", "Torch"), (54, 8, "ANY", "ResetPost")]
    s.script("Torch", f'''    setvar(VAR_0x8004, {F["r15_torch"]})
    setvar(VAR_0x8005, FALSE)
    call(EventScript_IchorBrazier)
    if (var(VAR_RESULT) == TRUE) {{
        msgbox(format("The old stand catches. Iakchos's torch burns over the glade again,\\p"
                      "the way it burned every autumn when the procession sang its way to Eleusis."), MSGBOX_DEFAULT)
    }}
    if (flag({F["r15_torch"]}) && !flag({F["r15_torch_gift"]})) {{
        msgbox(format("Under the flame, in the stand's bronze cup, a stone has warmed red.\\pYou take it."), MSGBOX_DEFAULT)
        giveitem(ITEM_FIRE_STONE)
        if (var(VAR_RESULT) == TRUE) {{
            setflag({F["r15_torch_gift"]})
        }}
    }}
    releaseall''')
    gift(s, "Priest", F["r15_priest"],
         "The Rheitoi's fish belong to Demeter and Kore. Only we priests may take them.\\p"
         "You walk the goddesses' road, though. Take this. The lake gives it up now and then.",
         "ITEM_DIVE_BALL", "Salt water and sweet water meet under the causeway. The fish like it there.")
    s.script("SpringKeeper", '''    lock
    faceplayer
    msgbox(format("Rest a while. The procession always drinks here before it goes down.\\pWater first. The god can wait."))
    special(HealPlayerParty)
    msgbox(format("There. Daphni's laurels are an hour down the far side."))
    release''')
    # --- the shrine court's seal: both drums on both plates open the stair down ----------
    for (px, py) in R15_PLATES:
        for dx, dy in K.FACE.values():
            c = (px + dx, py + dy)
            if c not in R15_PLATES and 47 <= c[0] <= 53 and 8 <= c[1] <= 10:
                s.trigger(*c, "Plates", "VAR_TEMP_2", "0")
    return s


def seal_scripts_r15(s, g, open_ids):
    """The seal's scripts, written once the layout's open and shut ids are known."""
    seal = F["r15_seal"]
    lid = "LOCALID_ROUTE15_MYSTERY_ROAD_"
    stair = "\n".join(f"    setmetatile({R15_STAIR_X}, {y}, 0x{mid:03X}, FALSE)" for y, mid in open_ids)
    (p1x, p1y), (p2x, p2y) = R15_PLATES
    s.script("Stair", stair + "\n    return")
    s.script("DrawSeal", f'''    if (flag({seal})) {{
        call({s.px}Stair)
        setobjectxyperm({lid}DRUM1, {p1x}, {p1y})
        setobjectxyperm({lid}DRUM2, {p2x}, {p2y})
    }}
    return''')
    s.script("Plates", f'''    if (flag({seal})) {{
        end
    }}
    getobjectxy({lid}DRUM1, CURRENT_POSITION, VAR_0x8007, VAR_0x8008)
    getobjectxy({lid}DRUM2, CURRENT_POSITION, VAR_0x8009, VAR_0x800A)
    if (var(VAR_0x8007) == {p1x} && var(VAR_0x8008) == {p1y} && var(VAR_0x8009) == {p2x} && var(VAR_0x800A) == {p2y}) {{
        lockall
        setflag({seal})
        playse(SE_DOOR)
        delay(20)
        call({s.px}Stair)
        special(DrawWholeMapView)
        playse(SE_M_STRENGTH)
        msgbox(format("Both drums sit true on their plates. Under the court, stone grinds on stone,\\p"
                      "and steps open down the scarp to a hollow in the rock."), MSGBOX_DEFAULT)
        releaseall
    }} elif (var(VAR_0x8007) == {p1x} && var(VAR_0x8008) == {p1y}) {{
        msgbox(format("The drum settles on a worn plate with a click. One plate to go."), MSGBOX_AUTOCLOSE)
    }} elif (var(VAR_0x8009) == {p2x} && var(VAR_0x800A) == {p2y}) {{
        msgbox(format("The drum settles on a worn plate with a click. One plate to go."), MSGBOX_AUTOCLOSE)
    }}''')
    s.script("ResetPost", f'''    lockall
    if (flag({seal})) {{
        msgbox(format("A post with the Girdle's knot carved in it. The stair below is open."), MSGBOX_DEFAULT)
        releaseall
        end
    }}
    msgbox(format("A post with the Girdle's knot carved in it. Two plates, two drums.\\p"
                  "Roll the drums back where they lay?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_CLICK)
        warpsilent({MAP_ID[R15]}, 50, 8)
        waitstate
    }}
    releaseall''')


R15_SCRIPTS = f'''mapscripts {R15}_MapScripts {{
    MAP_SCRIPT_ON_LOAD {{
        call({R15}_EventScript_DrawSeal)
    }}
    MAP_SCRIPT_ON_TRANSITION {{
        special(Ichor_ReleaseTimeOfDay)
    }}
}}'''


# ---------------------------------------------------------------------------
# Daphni (40x34)
# ---------------------------------------------------------------------------
D_W, D_H = 40, 34
TEMPLE = (17, 2)          # the PALAESTRA columns stamp (6x5), its door at (+3, +4)
REST_AT, REST_DOOR = (9, 21), (2, 3)      # route5's INN stamp (5x4)
COT_AT = (25, 21)                          # the cottage stamp (3x4), its door at (+1, +3)
HEALER = (16, 21)
D_HERM, D_PLAQUE, D_LANDING = (4, 15), (5, 15), (4, 16)


def plan_daphni():
    W, H = D_W, D_H
    g = N.Grid(DAPHNI, W, H, west=True, east=True)
    r = g.rect
    r("#", 0, 0, W - 1, H - 1)
    # --- the Sacred Way through the village -----------------------------------
    r(".", 0, 15, W - 1, 20)
    r("p", 0, 17, W - 1, 18)
    for x in (0, W - 1):                       # the seams are four wide, like the roads either side
        g.put("L", (x, 15), (x, 20))
    for x in (14, 15, 25, 26, 27, 34, 35):      # the grove's edge, broken along the road
        g.put("L", (x, 15))
    g.put("k", (11, 15))                        # the town sign
    # --- the sanctuary of Apollo Daphnaios in its laurel grove -------------------
    r("L", 8, 0, 31, 14)
    r("A", 14, 7, 26, 13)                      # the temenos's paving
    r("k", TEMPLE[0], TEMPLE[1], TEMPLE[0] + 5, TEMPLE[1] + 4)
    r("A", 19, 14, 21, 14)
    r("p", 20, 14, 20, 16)
    r("A", 15, 6, 25, 6)
    g.put("k", (23, 10), (23, 11))              # the altar
    g.put("L", (14, 7), (26, 7), (14, 13), (26, 13))
    g.put("k", (16, 9))                         # the prayer laurel
    r(".", 9, 10, 9, 14)                       # a laurel walk into the grove (a saved game stands at 9,10)
    # the Aigaleo lookout up the rock behind the grove (Pan's Crook)
    for y, ch in ((3, "b"), (4, "u"), (5, "f")):
        r(ch, 24, y, 31, y)
    r(".", 24, 0, 31, 2)
    r("#", 24, 0, 31, 0)
    r("k", 26, 1, 27, 2)                       # the stone seat
    r("A", 26, 6, 26, 6)
    # --- south of the road: the pilgrims' rest and its porch, the laurel-cutter ----
    r(".", 6, 20, 32, 27)
    r("k", REST_AT[0], REST_AT[1], REST_AT[0] + 4, REST_AT[1] + 3)
    r("k", HEALER[0] - 1, HEALER[1] + 1, HEALER[0] + 3, HEALER[1] + 1)   # the porch counter
    r("k", COT_AT[0], COT_AT[1], COT_AT[0] + 2, COT_AT[1] + 3)
    r("O", 29, 21, 31, 24)                     # the laurel-cutter's bay saplings
    r("p", REST_AT[0] + REST_DOOR[0], REST_AT[1] + 4, REST_AT[0] + REST_DOOR[0], 25)
    r("p", COT_AT[0] + 1, COT_AT[1] + 4, COT_AT[0] + 1, 25)
    r("p", 11, 25, 26, 25)
    r("p", 18, 19, 19, 25)
    r("L", 6, 26, 33, 29)
    r(".", 7, 25, 8, 25)
    g.put(".", (8, 26), (15, 26), (16, 26), (23, 26))   # bays in the south laurels
    for x in (6, 7, 23, 24, 32, 33, 37, 38):    # the south verge
        g.put("L", (x, 20))
    r("k", 21, 22, 23, 24)                     # the pilgrims' fountain
    return g


def props_daphni(g):
    g.set(11, 15, SIGN, True, "sign")
    stamp(g, N.PALAESTRA, TEMPLE[0], TEMPLE[1], door=(3, 4))
    stamp(g, R5.INN, REST_AT[0], REST_AT[1], door=REST_DOOR)
    stamp(g, N.COTTAGE, COT_AT[0], COT_AT[1], door=(1, 3))
    stamp(g, N.SPRING, 21, 22, kind="fountain")
    g.set(23, 10, TRIPOD, True, "altar")
    g.set(23, 11, ALTAR, True, "altar")
    g.piece("myrtle", 16, 9)
    g.piece("rock_seat", 26, 1)
    g.named("crook", "brink", 25, 3)
    g.named("crook", "face_u", 25, 4)
    g.named("crook", "foot", 25, 5)
    for x in range(HEALER[0] - 1, HEALER[0] + 4):
        g.set(x, HEALER[1] + 1, 0x149, True, "counter")
    for key, x, y in (("baskets", 28, 21), ("firewood", 28, 25), ("amphorae", 14, 21), ("pot_rack", 20, 21),
                      ("stele_low", 15, 12), ("lekythos", 25, 12)):
        if not g.fixed[y, x]:
            g.piece(key, x, y)
    laurels(g)


def spec_daphni():
    s = Spec(DAPHNI, MAP_ID[DAPHNI], "DAPHNI")
    s.connections = [{"direction": "left", "map": "MAP_ROUTE15_MYSTERY_ROAD", "offset": 0},
                     {"direction": "right", "map": "MAP_ROUTE16_CAPITAL_PASS", "offset": 0}]
    tx, ty = TEMPLE[0] + 3, TEMPLE[1] + 4
    s.warps = [dict(x=tx, y=ty, elevation=0, dest_map="MAP_DAPHNI_SANCTUARY", dest_warp_id="0"),
               dict(x=REST_AT[0] + REST_DOOR[0], y=REST_AT[1] + REST_DOOR[1], elevation=0,
                    dest_map="MAP_DAPHNI_PILGRIMS_REST", dest_warp_id="0"),
               dict(x=COT_AT[0] + 1, y=COT_AT[1] + 3, elevation=0, dest_map="MAP_DAPHNI_LAUREL_HOUSE",
                    dest_warp_id="0")]
    s.person("Healer", "HEALER", HEALER[0], HEALER[1], "DOWN")
    s.person("Merchant", "MERCHANT", HEALER[0] + 2, HEALER[1], "DOWN")
    s.person("Guide", "PILGRIM", 12, 15, "DOWN")
    s.person("Traveler", "MAN", 28, 2, "LEFT")
    s.person("Daphne", "KID_F", 30, 25, "LEFT")
    s.scripts.append(f'''script {s.px}Healer {{
    setvar(VAR_0x800B, LOCALID_DAPHNI_HEALER)
    call(Ichor_EventScript_AsclepeionHealer)
    waitmessage
    waitbuttonpress
    release
}}''')
    s.script("Merchant", "    goto(ArkadiaApproach_EventScript_Merchant)")
    talker(s, "Guide", "The pass opens onto Astyra.\\p"
           "The city's full of people who know exactly when the world ends. None of them agree what to do until then.")
    talker(s, "Daphne", "I'm Daphne. Like the laurel! Like the lady who ran from Apollo and turned into a tree.\\p"
           "Papa cuts the laurel for the god's crowns. He says I'm not allowed to turn into one.")
    s.script("Traveler", f'''    lock
    faceplayer
    msgbox(format("A Persian king sat on this rock once, they say, to watch his ships win at Salamis.\\p"
                  "He watched them sink instead. Kings should sit lower.\\p"
                  "Me? I came from the east, across the water. Past the Troad, where a city burned for a woman.\\p"
                  "There's a whole world out there your herms don't reach. Not yet."))
    setflag({F["d_traveler"]})
    release''')
    s.signs += [(16, 9, "ANY", "Laurel"), (23, 11, "ANY", "Altar")]
    sign(s, "Sign", 11, 15, "DAPHNI\\nApollo's laurels at the top of the Sacred Way.\\p"
         "West: the pass and Eleusa. East: the Kephisos and Astyra.")
    s.script("Altar", '''    msgbox(format("Apollo Daphnaios's altar. A laurel crown lies on it, still green."), MSGBOX_SIGN)
    end''')
    s.script("Laurel", f'''    lockall
    if (flag({F["d_cord"]})) {{
        msgbox(format("The prayer laurel. Where the cord was, the bark is healing over."), MSGBOX_DEFAULT)
        releaseall
        end
    }}
    msgbox(format("Someone tied a little prayer to the laurel.\\pThe string has cut into its bark."), MSGBOX_DEFAULT)
    checkitem(ITEM_DEMETERS_SICKLE)
    if (var(VAR_RESULT) == FALSE) {{
        releaseall
        end
    }}
    msgbox(format("Cut the cord free with Demeter's Sickle? The prayer stays on the branch."), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        setvar(VAR_0x8004, ITEM_DEMETERS_SICKLE)
        call(EventScript_IchorRelicPose)
        playse(SE_M_CUT)
        setflag({F["d_cord"]})
        msgbox(format("The cord falls away. The little prayer stays tucked in the leaves."), MSGBOX_DEFAULT)
    }}
    releaseall''')
    s.items += [("ITEM_STAR_PIECE", 30, 1, F["d_lookout"])]
    s.hidden += [("ITEM_HEART_SCALE", 9, 9, F["d_h_laurel"]), ("ITEM_BIG_ROOT", 8, 25, F["d_h_rest"]),
                 ("ITEM_NUGGET", 24, 1, F["d_h_seat"])]
    sign(s, "Fountain", 22, 24, "The pilgrims' fountain. Everyone on the Sacred Way washes the road off here,\p"
         "going out to the Mysteries and coming home from them.")
    sign(s, "Seat", 27, 2, "A stone seat cut in the rock, looking south over the gulf to Salamis.")
    return s


DAPHNI_SCRIPTS = f'''mapscripts {DAPHNI}_MapScripts {{
    MAP_SCRIPT_ON_TRANSITION {{
        special(Ichor_ReleaseTimeOfDay)
        setrespawn(HEAL_LOCATION_DAPHNI)
    }}
}}'''


# ---------------------------------------------------------------------------
# Route 16, the capital pass (72x36)
# ---------------------------------------------------------------------------
R16_W, R16_H = 72, 36
R16_SEAT = (60, 9)          # the rock seat (2x2); the route herm stands west of it
R16_HERM = (57, 9)
R16_VIEW = [(58, y) for y in range(9, 14)]
R16_SPAN_LINK = ((57, 19), (61, 23))        # the ditch's broken pier -> the far pier (the Wings)


def kephisos(y):
    """The river's swing east or west of its ford columns at row y."""
    import math
    return 0 if 13 <= y <= 22 else int(round(1.4 * math.sin((y - 17) / 3.2)))


def plan_r16():
    W, H = R16_W, R16_H
    g = N.Grid(R16, W, H, west=True, east=True)
    r = g.rect
    r("#", 0, 0, W - 1, H - 1)
    # --- Daphni's foot: Nikias, Timarete, the Kephisos ford -------------------------
    r(".", 0, 16, 15, 19)
    r("p", 0, 17, 15, 18)
    r("#", 8, 15, 10, 15)
    g.put(".", (9, 15))                        # Nikias's niche
    g.put(".", (13, 15))                       # Timarete's niche
    g.put("k", (3, 15))                        # the west sign
    r(".", 3, 4, 13, 13)                       # the oak wood's meadow above the road
    blob(g, ",", 8, 8.5, 5, 4.2, 16, only=".")
    r(".", 6, 14, 6, 15)
    for x, y in ((3, 4), (4, 4), (13, 4), (13, 5), (3, 13), (12, 13), (13, 13)):
        g.put("#", (x, y))
    r("o", 0, 20, 14, H - 1)
    r(".", 2, 22, 9, 28)                       # the vine-dresser's olives, a little meadow
    blob(g, ",", 5.5, 25, 3.2, 2.4, 11, only=".")
    r(".", 5, 20, 6, 21)
    # the Kephisos, north to south, with its ford and an islet
    for y in range(H):
        o = kephisos(y)
        r("~", 17 + o, y, 20 + o, y)
    r("_", 16, 14, 16, 21)
    r("_", 21, 14, 21, 21)
    r("x", 17, 17, 20, 18)
    r(".", 16, 16, 16, 19)
    r(".", 21, 16, 21, 19)
    for y in range(27, 30):                    # the islet (the Conch)
        r("_", 18 + kephisos(y), y, 19 + kephisos(y), y)
    r(".", 22, 16, 26, 19)
    r("p", 22, 17, 47, 18)
    r(",", 22, 16, 25, 19)                     # band 1, on the far bank
    # --- the Kerameikos: grave plots along the road ----------------------------------
    r(".", 27, 15, 44, 16)
    r(".", 27, 2, 44, 9)
    r("p", 30, 9, 31, 16)
    r("p", 28, 7, 43, 8)
    r("k", 27, 2, 44, 5)                       # the plots (props)
    r(".", 32, 2, 34, 4)                       # the drum's plot (the Girdle)
    r(".", 39, 3, 41, 4)                       # the rubble plot (the Hammer)
    r(".", 28, 3, 30, 4)                       # the sealed tomb's chamber (the Labrys)
    for x in (29, 33, 40):                     # the plots' gates
        g.put(".", (x, 5))
    blob(g, ",", 37, 12.5, 4.5, 1.6, 12, only="#")
    r(".", 33, 10, 43, 14)
    blob(g, ",", 38, 12, 5, 2.2, 13, only=".")
    r("#", 27, 10, 29, 14)
    g.put(".", (36, 9))                        # Exekias's spot
    # --- the Akademia's olives south of the road, behind a thicket (the Sickle) --------
    r("o", 27, 20, 44, H - 1)
    g.put(".", (35, 19), (35, 20))
    g.put(".", (35, 21))
    blob(g, ".", 35.5, 25.5, 6.5, 4.8, 15, only="o")
    blob(g, ",", 35.5, 26, 4.5, 3, 14, only=".")
    r("#", 37, 15, 44, 16)
    g.put(".", (40, 16))                       # Diotima's niche
    # --- the climb: the scarp, the terrace, the lookout -------------------------------
    r(".", 45, 17, 63, 20)
    blob(g, ",", 50, 19, 3.5, 1.4, 17, only=".")
    r("p", 45, 17, 47, 18)
    r("p", 46, 13, 47, 18)
    for y, ch in ((14, "b"), (15, "u"), (16, "f")):
        r(ch, 44, y, 63, y)
        r("s" if ch == "u" else "p", 46, y, 47, y)      # the scarp stair
        r("v" if ch == "u" else ".", 52, y, 54, y)      # the ledge back down to the ditch
    r(".", 44, 9, 63, 13)
    r("p", 46, 11, 47, 13)
    r("p", 46, 11, W - 1, 12)
    r("^", 44, 9, 45, 13)
    r("^", 48, 13, 49, 13)
    g.put(".", (48, 13))                       # Ariston's niche
    r(",", 50, 10, 53, 13)                     # band 2, right after Ariston
    r("^", 50, 9, 53, 9)
    g.put(".", (55, 9))                        # Straton's niche
    r("^", 54, 9, 54, 9)
    r("^", 56, 9, 57, 9)
    r("k", R16_SEAT[0], R16_SEAT[1], R16_SEAT[0] + 1, R16_SEAT[1] + 1)   # the lookout seat
    g.put("k", R16_HERM)                       # the herm
    # the Nymphs' shrine up the rock (Pan's Crook)
    for y, ch in ((6, "b"), (7, "u"), (8, "f")):
        r(ch, 44, y, 49, y)
    r(".", 44, 2, 49, 5)
    r("k", 45, 2, 47, 4)
    # the Akropolis across the walls: the rock and the temple on it (never reached)
    r("M", 48, 4, 52, 8)
    r("M", 59, 4, 63, 8)
    r("M", 53, 5, 58, 8)
    r("k", 53, 0, 58, 4)
    # the ditch under the walls and the fallen span (the Wings)
    r("^", 45, 21, 63, H - 1)
    r(",", 55, 19, 57, 20)
    r("^", 59, 17, 63, 20)
    g.put("A", (58, 19))
    g.put("k", (59, 19))                       # the broken pier's stump (the span sign)
    r("_", 59, 21, 63, 25)                     # the far pier, across the gap
    r(".", 60, 22, 62, 24)
    g.put("k", (62, 22))
    # the hill's bare flank under the ditch: rock in strata down to the Akademia's edge
    for x in range(45, 64):
        top = (23 if x < 58 else 26) + K.noise(x // 2, 5, 43) % 3
        r("M", x, top, x, H - 1)
    # --- the gate road (aethos strip x 64-71) ----------------------------------------
    r(".", 64, 9, W - 1, 13)
    r("p", 64, 10, W - 1, 13)
    g.put("k", (68, 9))                        # the east sign
    r("#", 64, 9, 65, 9)
    r("#", 66, 9, W - 1, 9)
    g.put(".", (69, 9))                        # Eubios's nook by the gate, out of the stream of travelers
    return g


def props_r16(g):
    g.set(3, 15, SIGN, True, "sign")
    g.set(68, 9, SIGN, True, "sign")
    g.set(*R16_HERM, HERM, True, "herm")
    # the Kerameikos's plots: walls, stelai, sarcophagi, lekythoi, the sealed tomb
    for x in range(27, 45):
        if x not in (29, 33, 40):              # the three plot gates (the Labrys, the Girdle, the Hammer)
            g.named("plot_wall", "EW" if x % 3 else "EW2", x, 5)
    for y in (2, 3, 4):
        for x in (31, 38):
            g.named("plot_wall", "NS", x, y)
    g.set(28, 2, R5.CAVE_TOP, True, "tomb")
    g.set(29, 2, R5.CAVE_TOP, True, "tomb")
    for key, x, y in (("stele_family", 27, 2), ("stele_low", 30, 2), ("lekythos", 34, 2),
                      ("stele_palmette", 35, 2), ("lekythos", 36, 2), ("stele_family", 37, 2),
                      ("stele_low", 41, 2), ("mound", 42, 2), ("sarcophagus", 42, 4)):
        g.piece(key, x, y)
    for y in range(2, 6):
        for x in range(27, 45):
            if g.g[y][x] == "k" and not g.fixed[y, x]:
                g.piece("rock", x, y)
    for key, x, y in (("milestone", 29, 15), ("sherds", 33, 16), ("stele_low", 43, 9), ("lekythos", 27, 7)):
        g.piece(key if g.g[y][x] != "p" else key + "_path" if key == "milestone" else key, x, y)
    # the Nymphs' shrine, the lookout seat, the crook's face
    g.piece("niches", 45, 2)
    g.piece("rock_seat", *R16_SEAT)
    g.named("crook", "brink", 48, 6)
    g.named("crook", "face_u", 48, 7)
    g.named("crook", "foot", 48, 8)
    # the Akropolis: the temple's columns on the rock
    stamp(g, N.PALAESTRA, 53, 0, kind="akropolis")
    g.piece("stele_palmette", 44, 2)
    g.piece("stele_low", 59, 19)
    g.piece("stele_low", 62, 22)


def spec_r16():
    s = Spec(R16, MAP_ID[R16], "R16")
    s.connections = [{"direction": "left", "map": "MAP_DAPHNI", "offset": 0},
                     {"direction": "right", "map": "MAP_ASTYRA", "offset": ASTYRA_OFFSET}]
    trainer(s, "NIKIAS", "HOPLITE", 9, 15, "DOWN", 4,
            "The capital road starts here. So does the capital's watch.", "You'll get through the gate.",
            "Astyra's over the hill. Follow the river, then climb.")
    trainer(s, "TIMARETE", "HARVESTER", 13, 15, "DOWN", 4,
            "The Kephisos waters every olive from here to the walls. Don't trample them!", "You stepped lightly.",
            "Hop the stones at the ford. The river's colder than it looks.")
    trainer(s, "KLEOBIS", "PILGRIM", 41, 8, "LEFT", 3,
            "My mother asked the goddess for the best gift for her sons. We fell asleep and never woke.\\p"
            "...That's my namesake's story, anyway. Battle?", "A deep sleep, that.",
            "The graves along here are the city's oldest. Walk softly.", mandatory=False)
    trainer(s, "DIOTIMA", "ACOLYTE_F", 40, 16, "DOWN", 2,
            "Love climbs from one beautiful thing to the next. Battles climb too.", "A lovely climb.",
            "The philosophers walk in the olives south of here. Ask one anything. Bring lunch.")
    trainer(s, "ARISTON", "SHEPHERD", 48, 13, "LEFT", 2,
            "Last flock before the walls. Show me your shepherding!", "Well herded.",
            "Up top you'll see it. The rock, and the god's house on it.")
    trainer(s, "EUBIOS", "AUGUR", 69, 9, "DOWN", 0,
            "The Dipylon's ahead. I read anyone who asks. You're asking.", "A bright omen.",
            "Astyra. Mind your purse, your manners and your future.", mandatory=False)
    trainer(s, "EXEKIAS", "MAN", 36, 9, "UP", 3,
            "I paint the jars they bury with the dead. Black figures. Want to be one?", "You'd fire well.",
            "Potters' quarter, potters' graves. We keep each other company.", mandatory=False)
    trainer(s, "SPEUSIPPOS", "YOUTH_M", 33, 23, "RIGHT", 3,
            "My uncle teaches under these olives. I'm supposed to be learning. Battle instead!",
            "Uncle will hear of this.", "Talk to Aristokles. He loves a question. Hates an answer.",
            mandatory=False)
    trainer(s, "MENEXENOS", "HOPLITE", 51, 19, "RIGHT", 3,
            "Nobody uses the ditch road since the span fell. Nobody but me.", "Ditch duty, done.",
            "The old border road crossed to that pier. Now only birds do.", mandatory=False)
    trainer(s, "STRATON", "HOPLITE", 55, 9, "DOWN", 4,
            "The city's walls start at the lookout. So does my patrol.", "Patrol relieved.",
            "Take a moment at the seat. Everyone does, the first time.")
    for t in s.trainers:
        if "R16_" + t["name"] in NEW_TRAINERS:
            t["id"] = "TRAINER_ICHOR_R16_" + t["name"]
    s.extra.append(K.obj("LOCALID_ROUTE16_CAPITAL_PASS_ALETHEA", GFX + "ALETHEA", 62, 13, "LEFT",
                         "Astyra_EventScript_RoadAlethea", "FLAG_ICHOR_HIDE_ALETHEA_R16"))
    s.people += [("Aristokles", "ELDER_M", 37, 22, "DOWN", "0")]
    s.thickets += [("GroveThicket", 35, 20, "0")]
    s.gate("PlotRubble", "BREAKABLE_ROCK", 40, 5, "EventScript_RockSmash", "0")
    s.gate("PlotDrum", "PUSHABLE_BOULDER", 33, 5, "EventScript_StrengthBoulder")
    s.gate("TombSeal", "BREAKABLE_ROCK", 29, 5, "EventScript_IchorLabrysSeal")
    item(s, "HYPER_POTION", 5, 23, "ITEM_R16_HEAL")
    item(s, "ULTRA_BALL", 12, 5, "ITEM_R16_BALL")
    item(s, "ETHER", 49, 3, "ITEM_R16_ETHER")
    s.items += [("ITEM_BIG_PEARL", 18 + kephisos(28), 28, F["r16_islet"]), ("ITEM_COMET_SHARD", 28, 3, F["r16_tomb"]),
                ("ITEM_TM38", 61, 23, F["r16_span"]), ("ITEM_LEAF_STONE", 40, 29, F["r16_grove"])]
    hidden(s, "HONEY", 9, 22, "HIDDEN_ITEM_R16_HONEY")          # the vine-dresser's olives
    hidden(s, "REVIVE", 63, 13, "HIDDEN_ITEM_R16_REVIVE")       # under the walls at the gate
    hidden(s, "SUPER_REPEL", 26, 19, "HIDDEN_ITEM_R16_REPEL")   # the ford's far bank
    s.hidden += [("ITEM_STAR_PIECE", 41, 3, F["r16_h_plot"]), ("ITEM_NUGGET", 33, 3, F["r16_h_drum"]),
                 ("ITEM_PRETTY_FEATHER", 46, 5, F["r16_h_shrine"])]
    sign(s, "Sign0", 3, 15, "Route 16, the capital pass.\\nWest: Daphni. East: the Kephisos, then Astyra.")
    sign(s, "Sign1", 68, 9, "Route 16.\\nEast: Astyra's Dipylon gate. West: the Kerameikos, the Kephisos and Daphni.")
    s.signs.append((R16_HERM[0], R16_HERM[1], "ANY", "Herm"))
    s.script("Herm", "    goto(EventScript_IchorGreatHerm)")
    sign(s, "Tomb", 28, 5, "A family tomb, its door sealed with bronze stamped with a double axe.\\p"
         "Old Knossian work. Whatever's inside was meant to stay there.")
    sign(s, "Plots", 36, 5, "Grave stelai of the city's dead: a girl with her doves, a rider, an old man and his dog.\\p"
         "A row of little oil jars stands in front of each.")
    sign(s, "Shrine", 46, 4, "Niches cut for the Nymphs of the hill, with clay figures and a dried garland.", "NORTH")
    s.script("Aristokles", f'''    lock
    faceplayer
    if (!flag({F["r16_sage"]})) {{
        msgbox(format("A visitor! Sit. I'm Aristokles, though my students call me the broad one.\\p"
                      "Tell me: is a thing good because the gods love it, or do they love it because it's good?\\p"
                      "...You don't know. Excellent. Neither do I. Take this, for the walk."))
        giveitem(ITEM_WISE_GLASSES)
        if (var(VAR_RESULT) == TRUE) {{
            setflag({F["r16_sage"]})
        }}
        release
        end
    }}
    msgbox(format("Prometheus's altar is in this grove. The torch race starts there and runs to the city.\\p"
                  "Whoever keeps the flame alight wins. Not whoever's fastest. Think about that."))
    release''')
    # the lookout: the seat, and the first sight of the Akropolis
    s.signs += [(R16_SEAT[0], R16_SEAT[1] + 1, "ANY", "Seat"), (R16_SEAT[0] + 1, R16_SEAT[1] + 1, "ANY", "Seat")]
    s.script("Seat", '''    msgbox(format("A stone seat at the top of the climb. From here: the walls, the city's roofs,\\p"
                  "and over them the rock, with the goddess's house on it, white as salt."), MSGBOX_SIGN)
    end''')
    for x, y in R16_VIEW:
        s.trigger(x, y, "View")
    s.script("View", f'''    lockall
    if (flag({F["r16_view"]})) {{
        releaseall
        end
    }}
    setflag({F["r16_view"]})
    applymovement(OBJ_EVENT_ID_PLAYER, Common_Movement_FaceUp)
    waitmovement(0)
    special(SpawnCameraObject)
    applymovement(OBJ_EVENT_ID_CAMERA, {s.px}Movement_CameraToRock)
    waitmovement(0)
    msgbox(format("Over the walls, the rock of the Akropolis rises out of the city.\\p"
                  "On top, the columns of the goddess's house catch the light.\\p"
                  "Astyra. The capital."), MSGBOX_DEFAULT)
    closemessage
    applymovement(OBJ_EVENT_ID_CAMERA, {s.px}Movement_CameraBack)
    waitmovement(0)
    special(RemoveCameraObject)
    releaseall''')
    s.scripts.append(f'''movement {s.px}Movement_CameraToRock {{
    walk_slow_up * 5
}}''')
    s.scripts.append(f'''movement {s.px}Movement_CameraBack {{
    walk_slow_down * 5
}}''')
    # the fallen span: Daedalus's Wings over the gap to the far pier
    (ax, ay), (bx, by) = R16_SPAN_LINK
    s.signs.append((ax + 2, ay, "ANY", "Span"))
    s.script("Span", f'''    lockall
    if (!flag(FLAG_ICHOR_GOT_DAEDALUS_WINGS)) {{
        msgbox(format("The old border road's span lies in pieces in the ditch.\\p"
                      "On the far pier something glints. Only something with wings could reach it."), MSGBOX_DEFAULT)
        releaseall
        end
    }}
    msgbox(format("The fallen span. The far pier is a short glide away.\\pSpread Daedalus's Wings?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_M_FLY)
        fadescreen(FADE_TO_WHITE)
        warpsilent({MAP_ID[R16]}, {bx}, {by})
        waitstate
    }}
    releaseall''')
    s.signs.append((62, 22, "ANY", "SpanBack"))
    s.script("SpanBack", f'''    lockall
    msgbox(format("The far pier of the fallen span. Glide back across?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == YES) {{
        closemessage
        playse(SE_M_FLY)
        fadescreen(FADE_TO_WHITE)
        warpsilent({MAP_ID[R16]}, {ax}, {ay})
        waitstate
    }}
    releaseall''')
    return s


R16_SCRIPTS = f'''mapscripts {R16}_MapScripts {{
    MAP_SCRIPT_ON_TRANSITION {{
        special(Ichor_ReleaseTimeOfDay)
        call(Astyra_EventScript_PlaceRoadAlethea)
    }}
}}'''


# ---------------------------------------------------------------------------
# Daphni's rooms (gTileset_Oikia; every interior unique, MAP_DESIGN §2)
# ---------------------------------------------------------------------------
ROOMS = {
    # The sanctuary of Apollo Daphnaios: the god in his niche, the altar before
    # him, potted laurels, lampstands, two columns, the priestess at the altar.
    SANCTUARY: {
        "title": "The sanctuary of Apollo Daphnaios, Daphni", "map": "MAP_DAPHNI_SANCTUARY", "layout": SANCTUARY,
        "floor": "flags", "wall": "red",
        "grid": ["WWWWWWWWWWWWWW", "WWWWWWWWWWWWWW"] + ["." * 14] * 8,
        "rugs": [],
        "stamps": [("window", 2, 0), ("niche", 6, 0), ("niche_horse", 7, 0), ("window", 11, 0),
                   ("altar", 5, 1), ("chest", 12, 1), ("myrtle", 0, 3), ("myrtle", 13, 4),
                   ("lampstand", 4, 3), ("lampstand", 9, 3), ("column", 2, 5), ("column", 11, 5),
                   ("kalathos", 8, 4), ("amphora", 13, 7), ("mat", 6, 9)],
        "spots": [("warp", "door to Daphni (south-arrow mat)", [(6, 9), (7, 9)]),
                  ("npc", "the priestess, by the altar", (6, 3), "south")],
    },
    # The pilgrims' rest: Iambe's hearth, couches for the initiates walking
    # to Eleusis, the long table, the kykeon jars.
    REST: {
        "title": "The pilgrims' rest, Daphni", "map": "MAP_DAPHNI_PILGRIMS_REST", "layout": REST,
        "floor": "terracotta", "wall": "red",
        "grid": ["WWWWWWWWWWWW", "WWWWWWWWWWWW"] + ["." * 12] * 7,
        "rugs": [],
        "stamps": [("soot", 1, 0), ("hearth", 1, 2), ("window", 3, 0), ("jar_shelf", 5, 0), ("window", 8, 0),
                   ("herbs", 10, 0), ("pithos", 11, 3), ("table", 4, 4), ("stool", 3, 4), ("stool", 6, 4),
                   ("kline", 8, 4), ("kline", 10, 6), ("pots", 1, 5), ("mat", 5, 8)],
        "spots": [("warp", "door to Daphni (south-arrow mat)", [(5, 8), (6, 8)]),
                  ("npc", "Iambe, at her hearth", (2, 4), "east"),
                  ("npc", "an initiate by the couches", (8, 6), "north")],
    },
    # The laurel-cutter's cottage: the loom where the crowns are woven, cut
    # laurel drying, the work table, the child's knucklebones.
    COTTAGE_ROOM: {
        "title": "The laurel-cutter's cottage, Daphni", "map": "MAP_DAPHNI_LAUREL_HOUSE", "layout": COTTAGE_ROOM,
        "floor": "boards", "wall": "blue",
        "grid": ["WWWWWWWWWW", "WWWWWWWWWW"] + ["." * 10] * 6,
        "rugs": [],
        "stamps": [("loom", 1, 0), ("herbs", 3, 0), ("window", 5, 0), ("myrtle", 7, 3), ("myrtle", 8, 3),
                   ("table", 4, 4), ("stool", 3, 4), ("knucklebones", 1, 6), ("kalathos", 9, 5), ("mat", 4, 7)],
        "spots": [("warp", "door to Daphni (south-arrow mat)", [(4, 7), (5, 7)]),
                  ("npc", "Dryas the laurel-cutter, at his table", (5, 3), "south")],
    },
}
ROOM_SIZE = {SANCTUARY: (14, 10), REST: (12, 9), COTTAGE_ROOM: (10, 8)}
IGNORE_FILE = ROOT / (".g" + "itignore")


def ensure_room_map(name, w, h):
    """Register a Daphni room map (its layout, map.json, scripts.pory, Daphni's map
    group, ichor_maps.inc, the ignore file) if it isn't yet."""
    lid = "LAYOUT_" + N.const(name)
    lp = ROOT / "data/layouts/layouts.json"
    lay = json.loads(lp.read_text())
    if not any(l.get("id") == lid for l in lay["layouts"]):
        d = ROOT / "data/layouts" / name
        d.mkdir(parents=True, exist_ok=True)
        np.full(w * h, 0x210 | (1 << 10), np.uint16).astype("<u2").tofile(d / "map.bin")
        np.full(4, 0x210, np.uint16).astype("<u2").tofile(d / "border.bin")
        lay["layouts"].append({"id": lid, "name": f"{name}_Layout", "width": w, "height": h,
                               "primary_tileset": "gTileset_Aethos", "secondary_tileset": "gTileset_Oikia",
                               "border_filepath": f"data/layouts/{name}/border.bin",
                               "blockdata_filepath": f"data/layouts/{name}/map.bin", "layout_version": "emerald"})
        lp.write_text(json.dumps(lay, indent=2) + "\n")
    md = ROOT / "data/maps" / name
    if (md / "map.json").exists():
        return
    md.mkdir(parents=True, exist_ok=True)
    (md / "map.json").write_text(json.dumps({
        "id": "MAP_" + N.const(name), "name": name, "layout": lid, "music": "MUS_ICHOR_ROAD",
        "region": "REGION_HOENN", "region_map_section": "MAPSEC_DAPHNI", "requires_flash": False,
        "weather": "WEATHER_NONE", "map_type": "MAP_TYPE_INDOOR", "allow_cycling": False,
        "allow_escaping": False, "allow_running": True, "show_map_name": False,
        "battle_scene": "MAP_BATTLE_SCENE_NORMAL", "connections": None, "object_events": [],
        "warp_events": [], "coord_events": [], "bg_events": []}, indent=2) + "\n")
    (md / "scripts.pory").write_text(f"mapscripts {name}_MapScripts {{}}\n")
    line = f"data/maps/{name}/scripts.inc"
    if line not in IGNORE_FILE.read_text().split("\n"):
        with IGNORE_FILE.open("a") as f:
            f.write(line + "\n")
    gp = ROOT / "data/maps/map_groups.json"
    groups = json.loads(gp.read_text())
    group = next(k for k, v in groups.items() if isinstance(v, list) and DAPHNI in v)
    if name not in groups[group]:
        groups[group].append(name)
    gp.write_text(json.dumps(groups, indent=2, ensure_ascii=False) + "\n")
    inc = ROOT / "data/ichor_maps.inc"
    if name not in inc.read_text():
        with inc.open("a") as f:
            f.write(f'\t.include "data/maps/{name}/scripts.inc"\n')


def build_rooms():
    import oikia_art as A
    import oikia_build as B
    import oikia_rooms as RR
    import kopais as KP
    base = dict(RR.ROOMS)
    base.update(RR.catalog(A.STAMPS))
    composed = {n: B.compose(sp) for n, sp in base.items()}
    order0, _ = B.collect(composed)
    for name, spec in ROOMS.items():
        composed[name] = B.compose(spec)
    order, ids = B.collect(composed)
    if len(order) != len(order0):
        raise SystemExit(f"sacredway: Daphni's rooms need {len(order) - len(order0)} cells gTileset_Oikia doesn't have")
    for name, spec in ROOMS.items():
        ensure_room_map(name, *ROOM_SIZE[name])
        B.check_spots(name, spec, composed[name])
        cells = composed[name]
        h, w = len(cells), len(cells[0])
        blocks = B.blockdata(cells, ids[name]).reshape(h, w)
        KP.write_layout(name, blocks, [0x0210] * 4, "gTileset_Aethos", "gTileset_Oikia")


def room_specs():
    import kopais as KP
    specs = []
    mats = {SANCTUARY: (6, 9), REST: (5, 8), COTTAGE_ROOM: (4, 7)}
    for door, name in enumerate((SANCTUARY, REST, COTTAGE_ROOM)):
        s = KP.Spec(name)
        mx, my = mats[name]
        s.warps = [KP.warp(mx, my, DAPHNI, door), KP.warp(mx + 1, my, DAPHNI, door)]
        specs.append(s)
    sanc, rest, cot = specs
    sanc.person("Priestess", "PRIESTESS", 6, 3, "DOWN")
    sanc.person("Acolyte", "ACOLYTE_M", 10, 7, "LEFT")
    sanc.scripts.append(f'''script {sanc.px}Priestess {{
    lock
    faceplayer
    if (flag({F["d_priestess"]})) {{
        msgbox(format("Apollo chased Daphne to the river, and her father made her a laurel.\\p"
                      "So the god wears her leaves. Love that can't hold on, kept anyway."))
        release
        end
    }}
    if (flag({F["d_cord"]})) {{
        msgbox(format("You freed the prayer laurel. I saw the cord on the ground.\\p"
                      "Somebody tied their wish too tight. People do.\\p"
                      "Take this. We weave them for the victors at the Pythian Games."))
        giveitem(ITEM_KINGS_ROCK)
        if (var(VAR_RESULT) == TRUE) {{
            setflag({F["d_priestess"]})
        }}
        release
        end
    }}
    msgbox(format("Welcome to Apollo Daphnaios's house. The laurels outside are his.\\p"
                  "One of them has a cord cutting into it. Someone's prayer.\\p"
                  "I can't bring myself to cut a prayer. Perhaps a harvester's blade would know how."))
    release
}}''')
    sanc.scripts.append(f'''script {sanc.px}Acolyte {{
    lock
    faceplayer
    msgbox(format("Pilgrims stop here on the way to Eleusis, then again on the way home.\\p"
                  "Going out, they're scared. Coming home, they won't say a word about what they saw."))
    release
}}''')
    rest.person("Iambe", "ELDER_F", 2, 4, "RIGHT")
    rest.person("Initiate", "PILGRIM", 8, 6, "UP")
    rest.scripts.append(f'''script {rest.px}Iambe {{
    lock
    faceplayer
    if (!flag({F["d_kykeon"]})) {{
        msgbox(format("Sit, sit. I'm Iambe. My great-great-whatever made the goddess laugh when she grieved.\\p"
                      "Rude jokes, mostly. It worked.\\p"
                      "Here: kykeon, barley and mint, what the initiates drink. Good for the road."))
        giveitem(ITEM_MOOMOO_MILK, 2)
        if (var(VAR_RESULT) == TRUE) {{
            setflag({F["d_kykeon"]})
        }}
        release
        end
    }}
    msgbox(format("The healer's on my porch, the merchant too. I just keep the fire going.\\p"
                  "And the jokes. Want one? ...No? Your loss."))
    release
}}''')
    rest.scripts.append(f'''script {rest.px}Initiate {{
    lock
    faceplayer
    if (flag({F["d_trade"]})) {{
        msgbox(format("The honey's for the cakes we carry at the Mysteries. I can't say more. I mean it."))
        release
        end
    }}
    msgbox(format("I'm walking to Eleusis for the Mysteries, and I've lost my honey for the cakes.\\p"
                  "I'd trade you two Lum Berries for a Honey. Fair?"))
    checkitem(ITEM_HONEY)
    if (var(VAR_RESULT) == FALSE) {{
        msgbox(format("No honey? The bees on the salt-lake road have plenty. If you're quick."))
        release
        end
    }}
    msgbox(format("Trade one Honey for two Lum Berries?"), MSGBOX_YESNO)
    if (var(VAR_RESULT) == NO) {{
        release
        end
    }}
    removeitem(ITEM_HONEY)
    giveitem(ITEM_LUM_BERRY, 2)
    if (var(VAR_RESULT) == TRUE) {{
        setflag({F["d_trade"]})
    }} else {{
        additem(ITEM_HONEY)
    }}
    msgbox(format("Thank you. The goddesses notice who shares on the road."))
    release
}}''')
    cot.person("Dryas", "MAN", 5, 3, "DOWN")
    cot.scripts.append(f'''script {cot.px}Dryas {{
    lock
    faceplayer
    if (flag({F["d_weaver"]})) {{
        msgbox(format("The crowns go to the city now, for the Archon's guests. My girl weaves faster than I cut."))
        release
        end
    }}
    if (flag(FLAG_ICHOR_ASTYRA_OSTRACISM_DONE)) {{
        msgbox(format("You came back from the city. You've the look of someone who watched the Assembly vote.\\p"
                      "They say the laurel keeps off lightning. It didn't help that girl, did it?\\p"
                      "Here. Seeds from the god's own trees. Plant them somewhere kinder."))
        giveitem(ITEM_MIRACLE_SEED)
        if (var(VAR_RESULT) == TRUE) {{
            setflag({F["d_weaver"]})
        }}
        release
        end
    }}
    msgbox(format("I cut the laurel for the god's crowns. Only the dead branches, mind. Apollo's jealous.\\p"
                  "Come back after you've seen the capital. I'll want to hear how they're spending my crowns."))
    release
}}''')
    return specs


# ---------------------------------------------------------------------------
# Wild tables, the new trainers, heal locations, herms
# ---------------------------------------------------------------------------
LAND = {
    R15: (32, 34, {
        "Morning": ["KORANTHA", "MELISSEER", "GALENYON", "THYRSIVY", "HOPLOMEX", "KORANTHA",
                    "MELISSEER", "NEMELEON", "THYRSIVY", "GALENYON", "HOPLOMEX", "NEMELEON"],
        "Day": ["MELISSEER", "KORANTHA", "THYRSIVY", "GALENYON", "KORANTHA", "HOPLOMEX",
                "MELISSEER", "NEMELEON", "GALENYON", "THYRSIVY", "NEMELEON", "HOPLOMEX"],
        "Evening": ["GLAUKOIN", "MELISSEER", "GALENYON", "THYRSIVY", "HOPLOMEX", "GLAUKOIN",
                    "MELISSEER", "NEMELEON", "THYRSIVY", "GALENYON", "HOPLOMEX", "NEMELEON"],
        "Night": ["PERSENYX", "LYKANAX", "MELISSEER", "THYRSIVY", "PERSENYX", "LYKANAX",
                  "HOPLOMEX", "NEMELEON", "MELISSEER", "THYRSIVY", "NEMELEON", "HOPLOMEX"],
    }),
    # wild_plan.py's tables have the last word on Route 16's land (Sophowl, Ophidrop)
    R16: (34, 36, {t: ["SOPHOWL", "HOPLOMEX", "CAIRNOLITH", "THYRSIVY", "NEMELEON", "ELAPLING",
                       "OPHIDROP", "SOPHOWL", "THYRSIVY", "HOPLOMEX", "OPHIDROP", "AETLING"]
                   for t in ("Morning", "Day", "Evening", "Night")}),
}


ROCK = ("CAIRNOLITH", "KERAZAP", "CAIRNOLITH", "HOPLOMEX", "CAIRNOLITH")


def write_wild():
    path = ROOT / "src/data/wild_encounters.json"
    data = json.loads(path.read_text())
    group = next(gr for gr in data["wild_encounter_groups"] if gr.get("for_maps"))
    ids = {MAP_ID[R15], MAP_ID[R16]}
    at = next((i for i, e in enumerate(group["encounters"]) if e.get("map") in ids), len(group["encounters"]))
    before = [e for e in group["encounters"][:at] if e.get("map") not in ids]
    after = [e for e in group["encounters"][at:] if e.get("map") not in ids]
    new = []
    for name, (lo, hi, tables) in LAND.items():
        for time, species in tables.items():
            mons = [{"min_level": lo if i % 3 else lo + 1, "max_level": hi, "species": "SPECIES_" + sp}
                    for i, sp in enumerate(species)]
            new.append({"map": MAP_ID[name], "base_label": f"g{name}_{time}",
                        "land_mons": {"encounter_rate": 25, "mons": mons}})
    for e in new:
        if e["base_label"].endswith("_Morning"):
            lo, hi = LAND[R15 if e["map"] == MAP_ID[R15] else R16][:2]
            e["rock_smash_mons"] = {"encounter_rate": 20, "mons": [
                {"min_level": lo, "max_level": hi, "species": "SPECIES_" + sp} for sp in ROCK]}
    group["encounters"] = before + new + after
    water_tables.apply(group["encounters"], ids)          # the Rheitoi and the Kephisos (water_tables.py)
    plan_hook.apply(group["encounters"])                  # the distribution pass has the last word
    path.write_text(json.dumps(data, indent=2) + "\n")


NEW_TEAMS = [
    ("R15_KERKOPS", "KERKOPS", "Pilgrim", "Pilgrim", "Male", [("Gelasable", 36), ("Prosomime", 37)]),
    ("R15_SIMMIAS", "SIMMIAS", "Sculptor", "Sculptor", "Male",
     [("Cairnolith", 35), ("Hoplomex", 36), ("Cairnolith", 36)]),
    ("R15_THEOXENOS", "THEOXENOS", "Pilgrim", "Pilgrim", "Male", [("Melisseer", 35), ("Thyrsivy", 36)]),
    ("R15_LAMPON", "LAMPON", "Acolyte", "Acolyte M", "Male", [("Lykanax", 36), ("Harpelle", 36), ("Persenyx", 37)]),
    ("R15_KALLIDIKE", "KALLIDIKE", "Harvester", "Harvester", "Female", [("Korantha", 36), ("Melisseer", 37)]),
    ("R16_EXEKIAS", "EXEKIAS", "Potter", "Potter", "Male", [("Cairnolith", 37), ("Kerazap", 37), ("Hoplomex", 38)]),
    ("R16_SPEUSIPPOS", "SPEUSIPPOS", "Acolyte", "Acolyte M", "Male", [("Sophowl", 37), ("Elapling", 38)]),
    ("R16_MENEXENOS", "MENEXENOS", "Hoplite", "Hoplite", "Male", [("Hoplomex", 37), ("Nemeleon", 38)]),
    ("R16_STRATON", "STRATON", "Hoplite", "Hoplite", "Male",
     [("Nemeleon", 37), ("Ophidrop", 38), ("Hoplomex", 38)]),
]


def write_trainers():
    """The new trainers' ids (world-act2's 1344-1352) and their parties. The old
    road's twelve keep their ids and astyra.py's parties."""
    path = ROOT / "include/constants/opponents.h"
    text = path.read_text()
    start, end = "// The Sacred Way (tools/ichor/maps/sacredway.py): world-act2's 1344-1352.", "// End the Sacred Way."
    block = start + "\n" + "".join(f"#define TRAINER_ICHOR_{k:<24} {v}\n" for k, v in NEW_TRAINERS.items()) + end + "\n"
    if start in text:
        a, b = text.index(start), text.index(end) + len(end) + 1
        text = text[:a] + block + text[b:]
    else:
        anchor = "#define TRAINERS_END_ACT2"
        text = text.replace(anchor, block + anchor, 1)
    top = max(NEW_TRAINERS.values()) + 1
    text = re.sub(r"#define TRAINERS_END_ACT2[^\n]*",
                  f"#define TRAINERS_END_ACT2                   {top} // the highest Act II id is the Sacred Way's {top - 1}",
                  text)
    path.write_text(text)
    path = ROOT / "src/data/trainers.party"
    text = path.read_text()
    start, end = "/* Sacred Way teams (tools/ichor/maps/sacredway.py). */", "/* End Sacred Way teams. */"
    block = start + "\n"
    for key, name, cls, pic, gender, mons in NEW_TEAMS:
        block += (f"\n=== TRAINER_ICHOR_{key} ===\nName: {name}\nClass: {cls}\nPic: {pic}\nGender: {gender}\n"
                  f"Music: {'Female' if gender == 'Female' else 'Male'}\nAI: Basic Trainer\n")
        for sp, lv in mons:
            block += f"\n{sp}\nLevel: {lv}\nIVs: 20 HP / 20 Atk / 20 Def / 20 SpA / 20 SpD / 20 Spe\n"
    block += "\n" + end
    if start in text:
        a, b = text.index(start), text.index(end) + len(end)
        text = text[:a] + block + text[b:]
    else:
        anchor = "/* End Astyra approach teams. */"
        a = text.index(anchor) + len(anchor)
        text = text[:a] + "\n\n" + block + text[a:]
    path.write_text(text)


def write_heal_locations():
    path = ROOT / "src/data/heal_locations.json"
    data = json.loads(path.read_text())
    for h in data["heal_locations"]:
        if h["id"] == "HEAL_LOCATION_DAPHNI":
            h.update(x=HEALER[0], y=HEALER[1] + 2, respawn_x=HEALER[0], respawn_y=HEALER[1] + 2)
        elif h["id"] == "HEAL_LOCATION_HERM_AETHOS_ROUTE_15":
            h.update(x=R15_HERM[0], y=R15_HERM[1] + 1)
        elif h["id"] == "HEAL_LOCATION_HERM_AETHOS_ROUTE_16":
            h.update(x=R16_HERM[0], y=R16_HERM[1] + 1)
    path.write_text(json.dumps(data, indent=2) + "\n")


def place_town_herm():
    """Daphni's travel herm: town_herms.py's row (the source of truth) and the
    landing in src/data/ichor_town_herms.h, then its two objects."""
    import town_herms as TH
    src_path = ROOT / "tools/ichor/maps/town_herms.py"
    src = src_path.read_text()
    old = re.search(r'    \("Daphni",[^\n]*\n', src).group(0)
    new = (f'    ("Daphni",            {str(D_HERM) + ",":<10} {str(D_PLAQUE) + ",":<10} {str(D_LANDING) + ",":<10} '
           f'"the west road, from Route 15"),\n')
    if old != new:
        src_path.write_text(src.replace(old, new))
    TH.apply((DAPHNI, D_HERM, D_PLAQUE, D_LANDING, "the west road, from Route 15"))
    h = ROOT / "src/data/ichor_town_herms.h"
    text = h.read_text()
    text = re.sub(r"(\[TOWN_HERM_DAPHNI\]\s*=\s*\{ MAP_DAPHNI,\s+)\d+,\s*\d+,",
                  lambda m: f"{m.group(1)}{D_LANDING[0]}, {D_LANDING[1]:>2},", text)
    h.write_text(text)


# ---------------------------------------------------------------------------
# Building, checking, rendering
# ---------------------------------------------------------------------------
VIEWS = {
    R15: [("1 Eleusa's gate, Timon", 7, 11), ("2 the causeway, band 1", 20, 15), ("3 the jesters' bridge", 24, 21),
          ("4 the scarp stair", 35, 10), ("5 the terrace, band 2", 42, 6), ("6 the herm and spring", 50, 5),
          ("7 the shrine court", 50, 9), ("8 the foot meadow", 42, 14), ("9 the quarry", 43, 21),
          ("10 the Iakchos glade", 65, 6), ("11 Demeter's altar", 61, 23), ("12 band 3, Praxon", 66, 18)],
    DAPHNI: [("1 the west road, the herm", 7, 17), ("2 the sanctuary", 20, 7), ("3 the lookout", 27, 3),
             ("4 the rest and its porch", 14, 23), ("5 the laurel-cutter's", 27, 23), ("6 the east road", 34, 17)],
    R16: [("1 Daphni's foot", 8, 17), ("2 the Kephisos ford", 19, 17), ("3 the Kerameikos", 34, 6),
          ("4 the Akademia", 35, 25), ("5 the scarp stair", 47, 13), ("6 the terrace, band 2", 52, 11),
          ("7 the lookout", 58, 8), ("8 the ditch and span", 57, 20), ("9 the Dipylon road", 66, 11)],
}
STEMS = {R15: "route15", DAPHNI: "daphni", R16: "route16"}
# objects reachable only with a relic the walk doesn't use (the Conch, Pan's Crook)
LATER = {R15: {"KERKOPS", "SIMMIAS"}, DAPHNI: {"TRAVELER", "SEAT"}, R16: {"SHRINE", "SPANBACK", "TOMB"}}


def build_r15():
    g, s, b = N.build(plan_r15, props_r15, spec_r15)
    # the hollow's stair stays shut until the seal: the band's own pieces over it
    open_ids = [(y, int(g.mt[y, R15_STAIR_X])) for y in (11, 12, 13)]
    for y in (11, 12, 13):
        g.mt[y, R15_STAIR_X] = g.mt[y, R15_STAIR_X + 2]
        g.solid[y, R15_STAIR_X] = True
    b = N.write_layout(g)
    seal_scripts_r15(s, g, open_ids)
    return g, s, b


def check_seal():
    import ascent_lib
    yard = {(x, y) for x in range(47, 54) for y in range(8, 11)}
    plan = ascent_lib.push_plan(yard, R15_DRUMS, R15_PLATES, (50, 8))
    if not plan:
        raise SystemExit("Route 15: the shrine court's seal can't be solved")
    return plan


def filtered(problems, name):
    return [p for p in problems
            if not (("can't be reached" in p or "can't be read" in p) and any(n in p.upper() for n in LATER[name]))]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--render", metavar="DIR")
    ap.add_argument("--stem-suffix", default="")
    ap.add_argument("--walk", action="store_true")
    ap.add_argument("--no-rooms", action="store_true", help="skip Daphni's room layouts")
    args = ap.parse_args()
    if not K.CAT.exists():
        sys.exit(f"{K.CAT} is missing; run /usr/bin/python3 tools/ichor/art/skiron_build.py --no-compile first")
    claim_flags()
    g15, s15, b15 = build_r15()
    gd, sd, bd = N.build(plan_daphni, props_daphni, spec_daphni, notch=False)
    g16, s16, b16 = N.build(plan_r16, props_r16, spec_r16)
    write_events(s15, mapscripts=R15_SCRIPTS)
    write_events(sd, kind="MAP_TYPE_TOWN", mapscripts=DAPHNI_SCRIPTS)
    write_events(s16, mapscripts=R16_SCRIPTS)
    if not args.no_rooms:
        import kopais as KP
        build_rooms()
        for spec in room_specs():
            KP.write_events(spec, "MUS_ICHOR_ROAD", "MAP_TYPE_INDOOR",
                            extra={"allow_cycling": False, "show_map_name": False, "weather": "WEATHER_NONE"})
    place_town_herm()
    write_heal_locations()
    write_wild()
    write_trainers()
    print(f"the shrine court's seal: {len(check_seal())} pushes")
    bad = 0
    for g, s, b, pairs in (
            (g15, s15, b15, [(("Eleusa", N.edge_cells(g15, "left")), ("Daphni", N.edge_cells(g15, "right")))]),
            (gd, sd, bd, [(("Route 15", N.edge_cells(gd, "left")), ("Route 16", N.edge_cells(gd, "right")))]),
            (g16, s16, b16, [(("Daphni", N.edge_cells(g16, "left")), ("Astyra", N.edge_cells(g16, "right")))])):
        problems, mand, forced = N.check(g, s, pairs)
        problems = filtered(problems, g.name)
        if args.walk:
            print(N.walk_text(g, s))
        if args.render:
            N.render(g.name, g.w, g.h, b, s.objects(), args.render, STEMS[g.name] + args.stem_suffix,
                     views=VIEWS[g.name], walk=(g, s))
        for p in problems:
            print(f"PROBLEM {s.name}: {p}")
        print(f"{s.name}: {g.w}x{g.h}, forced grass {forced}, {len(s.trainers)} trainers, "
              f"on the only road: {', '.join(mand) or 'none'}, {len(problems)} problems")
        bad += len(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
