"""MAP_TRIREME_EUPLOIA_DECK_SOUTH: the Euploia's deck for Act III's southern
voyages (design/phase4/SCRIPT.md, Open questions 1 and Part 2).

The same ship as Phase 2's MAP_TRIREME_EUPLOIA_DECK: its layout is that deck's
map.bin cell for cell (copied from world-act1, with gTileset_Trireme), so this
module only adds Act III's people and things and closes the hatch (there is no
hold on this voyage's map: the rowers are asleep below). The deck is rows 4-9,
x 2-19; the bow is west, the helm east at x = 20; the rail's gaps at (7,3),
(13,3) and (15,10) are sea to fish into.

Used by: III-1A (boarding, moored at Kaldera), III-1B (Route 22 by night),
III-1B3 (Cape Malea), III-1I (Route 23 to Amnisos). scripts.pory picks the
scene from VAR_ICHOR_ACT3 and the voyage flags.
"""
import numpy as np

import kythera_outdoor as K
from kythera_outdoor import obj, item_ball, sign, trigger

NAME = "TriremeEuploia_DeckSouth"
P = "TriremeEuploia_DeckSouth_EventScript_"
HIDE = "FLAG_ICHOR_HIDE_DECK_ACT3"
HATCH = (14, 7)


def specs():
    path = K.ROOT / "data/layouts" / NAME / "map.bin"
    blocks = np.fromfile(path, "<u2").reshape(16, 24)
    blocks = blocks.copy()
    blocks[HATCH[1], HATCH[0]] |= K.SOLID          # the hatch (idempotent): no hold on this voyage
    g = K.Grid(24, 16, "trireme")
    g.mid[:] = blocks & 0x3FF
    g.solid[:] = (blocks & K.SOLID) != 0

    objects = [
        obj("ICHOR_SAILOR", 19, 7, "right", P + "Nausikles", "LOCALID_DECKS_NAUSIKLES"),
        obj("ICHOR_YOUTH_M", 2, 6, "left", P + "Lookout", "LOCALID_DECKS_LOOKOUT"),
        obj("ICHOR_MAN", 12, 8, "down", P + "Oarsman", "LOCALID_DECKS_OARSMAN", HIDE),
        obj("ICHOR_WOMAN", 15, 5, "up", P + "Passenger", "LOCALID_DECKS_PASSENGER", HIDE),
        obj("ICHOR_ELDER_M", 8, 6, "left", P + "OldSailor", "LOCALID_DECKS_OLD_SAILOR", HIDE),
        obj("ICHOR_SAILOR", 10, 4, "up", P + "Eudoros", "LOCALID_DECKS_EUDOROS", HIDE, trainer=1),
        obj("ICHOR_MERCHANT", 5, 5, "up", P + "Kerdon", "LOCALID_DECKS_KERDON", HIDE, trainer=1),
        obj("ICHOR_PROFESSOR_DAPHNE", 12, 5, "down", P + "Daphne", "LOCALID_DECKS_DAPHNE",
            "FLAG_ICHOR_DAPHNE_SAILED_ASTYRA"),
        item_ball(3, 5, "ITEM_HYPER_POTION", "FLAG_ICHOR_ITEM_DECK_SOUTH_HYPER_POTION"),
    ]
    bgs = [
        sign(5, 4, P + "Cargo", "north"), sign(6, 4, P + "Cargo", "north"),
        sign(19, 4, P + "Klepsydra"),
        sign(HATCH[0], HATCH[1], P + "Hatch"),
    ]
    # The lookout's shout: two tiles from the bow (beat III-1B), armed by
    # VAR_TEMP_1 on the night crossing only.
    coords = [trigger(4, y, P + "TitanFleet", "VAR_TEMP_1", 1) for y in (5, 6, 7, 8)]
    spec = K.Spec(NAME, g, music="MUS_ICHOR_TRIREME", mapsec="MAPSEC_AETHOS_ROUTE_22",
                  map_type="MAP_TYPE_OCEAN_ROUTE", show_name=False, allow_cycling=False,
                  border=[0x170] * 4, objects=objects, bgs=bgs, coords=coords, start=(12, 7),
                  screens={"1_bow": (5, 6), "2_midships": (12, 6), "3_stern": (17, 6)},
                  blocks=blocks)
    return [spec]
