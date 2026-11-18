#!/usr/bin/env python3
"""The distribution pass's wild tables (design/DISTRIBUTION.md), applied on top of
what each map's builder writes.

  /usr/bin/python3 tools/ichor/wild_plan.py          apply the plan to src/data/wild_encounters.json
  /usr/bin/python3 tools/ichor/wild_plan.py --check  exit 1 if the json and the plan disagree

Every builder that writes wild tables (kopais.py, gulf.py, nemea.py, the *_encounters.py
scripts, water_tables.py and the rest) calls apply() on its entries just before it
writes the json, so rerunning any builder keeps the distribution. The builders' own
species lists for these maps are the pre-pass tables; this module is where a planned
table is changed.

Four kinds of change, applied in this order:
  TABLES  a whole table (land 12 slots, water 5, rock smash 5, fishing 10) for a map and
          time of day; new maps' entries (the Erymanthian Preserve) are created.
  SWAPS   one species for another in some of a map's tables (a starter out, a signature in).
  SLOTS   one slot of one table.
  then    no early evolved forms (BALANCE.md): any evolved form left below the level it
          evolves at becomes its earlier stage, in every Ichor table.
Rows are written "Species lo-hi" (or "Species lv").
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "src/data/wild_encounters.json"
TIMES = ("Morning", "Day", "Evening", "Night")
COUNTS = {"land_mons": 12, "water_mons": 5, "rock_smash_mons": 5, "fishing_mons": 10}


def rows(*specs):
    out = []
    for s in specs:
        name, lv = s.rsplit(" ", 1)
        lo, _, hi = lv.partition("-")
        out.append((name.upper(), int(lo), int(hi or lo)))
    return out


L, W, R, F = "land_mons", "water_mons", "rock_smash_mons", "fishing_mons"

# --------------------------------------------------------------------------------------
# Whole tables: (map, label stem, time) -> {method: (rate or None to keep, rows)}
# --------------------------------------------------------------------------------------
TABLES = {}


def table(mapid, stem, times, **methods):
    for t in times:
        entry = TABLES.setdefault((mapid, stem, t), {})
        for meth, val in methods.items():
            rate, rs = val if isinstance(val, tuple) else (None, val)
            entry[{"land": L, "water": W, "rock": R, "fish": F}[meth]] = (rate, rs)


# Aegina (Emporion stage, 12-16): three roads with their own wildlife. The island of the
# Myrmidons (Ergant everywhere), of the first coins (Onotis and Obolorn, the obol, at
# night) and of the sea turtle on those coins (Chelonet, the Aphaia road's own).
table("MAP_AEGINA_APHAIA_ROAD", "gAeginaAphaiaRoad", ["Morning"], land=rows(
    "Ergant 12-14", "Chelonet 12-14", "Epopoi 12-14", "Onotis 13-15", "Halcyling 12-14", "Ergant 14-15",
    "Karkipool 13-15", "Chelonet 14-16", "Galekit 12-14", "Lophops 14-15", "Onotis 16", "Chelonet 16"))
table("MAP_AEGINA_APHAIA_ROAD", "gAeginaAphaiaRoad", ["Night"], land=rows(
    "Galekit 12-14", "Ergant 12-14", "Chelonet 12-14", "Onotis 12-14", "Karkipool 12-14", "Pebblith 13-15",
    "Galekit 14-15", "Obolorn 14-15", "Ergant 14-15", "Onotis 15-16", "Obolorn 16", "Chelonet 16"))
# The temple of Aphaia, the nymph who vanished: the veiled butterfly by day.
table("MAP_AEGINA_TEMPLE_OF_APHAIA", "gAeginaTempleOfAphaia", ["Morning"], land=rows(
    "Ergant 12-14", "Psychora 12-14", "Epopoi 12-14", "Lophops 14-15", "Galekit 12-14", "Psychora 14-15",
    "Chelonet 13-15", "Ergant 14-15", "Halcyling 12-14", "Kerazap 13-15", "Psychora 16", "Lophops 16"))
table("MAP_AEGINA_TEMPLE_OF_APHAIA", "gAeginaTempleOfAphaia", ["Night"], land=rows(
    "Galekit 12-14", "Ergant 12-14", "Pebblith 13-15", "Onotis 12-14", "Galekit 14-15", "Ergant 14-15",
    "Obolorn 14-15", "Pebblith 15-16", "Chelonet 12-14", "Onotis 15-16", "Obolorn 16", "Galekit 16"))
# Mount Oros: the island's goat crags and the harpies' sea cliffs.
table("MAP_AEGINA_MOUNT_OROS", "gAeginaMountOros", ["Morning"], land=rows(
    "Kerazap 13-15", "Ergant 12-14", "Harpeck 13-15", "Epopoi 12-14", "Lophops 14-15", "Kerazap 14-16",
    "Pebblith 13-15", "Harpeck 15-16", "Chelonet 12-14", "Ergant 15-16", "Kerazap 16", "Harpeck 16"))
table("MAP_AEGINA_MOUNT_OROS", "gAeginaMountOros", ["Night"], land=rows(
    "Galekit 12-14", "Pebblith 12-14", "Kerazap 13-15", "Ergant 12-14", "Galekit 14-15", "Pebblith 14-16",
    "Harpeck 13-15", "Obolorn 14-15", "Kerazap 15-16", "Ergant 15-16", "Narthip 15", "Pebblith 16"))

# Hecate's Hollow by night: Gelasable is Galanthis, the weasel Hecate took in, and the
# shades' Obolorn come up out of the dark. (The day tables stay the builder's.)
table("MAP_HECATES_HOLLOW", "gHecatesHollow", ["Night"], land=rows(
    "Galekit 17-19", "Pebblith 17-19", "Galekit 18-20", "Spalunk 17-19", "Obolorn 17-19", "Ergant 17-19",
    "Gelasable 20", "Obolorn 18-20", "Spalunk 19-20", "Pebblith 19-20", "Gelasable 20", "Obolorn 20"))

# Route 4 and Route 5's rubble: broken amphorae, and the jar-dog that lives in them.
table("MAP_ROUTE4_ISTHMUS", "gRoute4Isthmus", ["Morning"], rock=rows(
    "Pebblith 16-19", "Spalunk 16-18", "Pithound 17-19", "Chelonet 17-19", "Pithound 19"))
table("MAP_ROUTE5_SKIRONIAN_CLIFFS", "gRoute5SkironianCliffs", ["Morning"], rock=rows(
    "Pebblith 18-21", "Spalunk 18-20", "Pithound 19-21", "Chelonet 19-21", "Pithound 21-22"))

# Eleusa (19-22): Demeter's fields. Wheat-ear Stachyss, bees, piglets, and the farmyard
# cocks (Alekrow) by day; the field mice of the night are the weasels.
table("MAP_ELEUSA_VILLAGE", "gEleusaVillage", ["Morning"], land=rows(
    "Stachyss 19-21", "Melibee 19-21", "Kaplet 19-21", "Stachyss 20-22", "Spalunk 19-21", "Alekrow 19-21",
    "Melibee 21-22", "Elaleaf 19-21", "Kaplet 21-22", "Alekrow 21-22", "Rhoaril 22", "Stachyss 22"))
table("MAP_ELEUSA_VILLAGE", "gEleusaVillage", ["Night"], land=rows(
    "Galekit 19-21", "Kaplet 19-21", "Spalunk 19-21", "Gelasable 20-22", "Stachyss 19-21", "Kaplet 20-22",
    "Spalunk 21-22", "Galekit 21-22", "Elaleaf 20-22", "Gelasable 21-22", "Rhoaril 22", "Kaplet 22"))

# Route 9, the Parnassos crossroads (27-31): the Schiste crossroads, where Oedipus met his
# father on the road to Delphoi, and the Sphinx's road. Enigmaw at dusk and after dark.
table("MAP_ROUTE9_PARNASSOS_CROSSROADS", "gRoute9_ParnassosCrossroads", ["Morning", "Day"], land=rows(
    "Eripip 27-30", "Ampelix 27-31", "Lophops 27-31", "Harpelle 27-31", "Melibee 27-31", "Onotis 27-30",
    "Eripip 29-31", "Cairnolith 28-31", "Midonos 27-31", "Kerazap 28-31", "Enigmaw 30-31", "Midonos 31"))
table("MAP_ROUTE9_PARNASSOS_CROSSROADS", "gRoute9_ParnassosCrossroads", ["Evening"], land=rows(
    "Ampelix 27-30", "Gelasable 27-31", "Botrykit 27-31", "Lophops 27-30", "Lykopup 27-31", "Prosomime 27-31",
    "Enigmaw 28-31", "Eripip 27-31", "Harpelle 27-31", "Cairnolith 27-30", "Enigmaw 30-31", "Kerazap 31"))
table("MAP_ROUTE9_PARNASSOS_CROSSROADS", "gRoute9_ParnassosCrossroads", ["Night"], land=rows(
    "Gelasable 27-30", "Lykopup 27-31", "Prosomime 27-31", "Botrykit 27-30", "Raknit 27-31", "Spalunk 27-31",
    "Enigmaw 28-31", "Ampelix 27-30", "Galekit 27-31", "Cairnolith 27-30", "Enigmaw 30-31", "Midonos 31"))

# Route 12, the cypress road down to Arkadia (29-31): Arkadia's own wildlife starts here.
table("MAP_ROUTE12_CYPRESS_ROAD", "gRoute12_CypressRoad", ["Morning", "Day"], land=rows(
    "Raknit 29-31", "Eripip 29-31", "Ampelix 29-31", "Melibee 29-31", "Arkoby 29-31", "Kaplet 29-31",
    "Raknit 30-31", "Eripip 30-31", "Galekit 29-31", "Arkoby 30-31", "Skylaps 31", "Melibee 31"))
table("MAP_ROUTE12_CYPRESS_ROAD", "gRoute12_CypressRoad", ["Evening"], land=rows(
    "Raknit 29-31", "Lykopup 29-31", "Arkoby 29-31", "Eripip 29-31", "Ampelix 29-31", "Kaplet 29-31",
    "Lykopup 30-31", "Raknit 30-31", "Prosomime 29-31", "Arkoby 30-31", "Skylaps 31", "Amnoze 31"))
table("MAP_ROUTE12_CYPRESS_ROAD", "gRoute12_CypressRoad", ["Night"], land=rows(
    "Lykopup 29-31", "Raknit 29-31", "Prosomime 29-31", "Arkoby 29-31", "Kaplet 29-31", "Amnoze 29-31",
    "Lykopup 30-31", "Raknit 30-31", "Galekit 29-31", "Prosomime 30-31", "Amnoze 31", "Lykanax 31"))

# Arkadia's cypress wood (30-33): the bear cubs of Kallisto's glades and the webs by day,
# the wolves of Lykaon and the boar by night. Skylaps, Artemis's hound, runs here rarely.
table("MAP_ARKADIA_CYPRESS_WOOD", "gArkadiaCypressWood", ["Morning"], land=rows(
    "Raknit 30-32", "Arkoby 30-32", "Raknit 31-33", "Lophops 30-32", "Arkoby 31-33", "Kaplet 30-32",
    "Arkoby 32-33", "Raknit 32-33", "Kaplet 32-33", "Lophops 32-33", "Skylaps 32-33", "Arkoby 33"))
table("MAP_ARKADIA_CYPRESS_WOOD", "gArkadiaCypressWood", ["Night"], land=rows(
    "Lykopup 30-32", "Raknit 30-32", "Arkoby 30-32", "Lykopup 31-33", "Amnoze 30-32", "Raknit 31-33",
    "Arkoby 32-33", "Kaprodon 31-33", "Lykopup 32-33", "Amnoze 31-33", "Lykanax 33", "Kaprodon 33"))

# Route 8, Lake Kopais (27-31): the reed marsh. Chalkip, the Stymphalian chicks, and the
# swans' cygnets (Hymnet) on the open water.
table("MAP_ROUTE8_KOPAIS_ROAD", "gRoute8_KopaisRoad", TIMES, water=rows(
    "Hymnet 27-29", "Ketofry 27-29", "Galenyon 28-30", "Hymnet 29-30", "Galenyon 30-31"), fish=rows(
    "Ketofry 21-23", "Ketofry 23-25", "Ketofry 26-28", "Hymnet 26-28", "Karkitox 28-29",
    "Galenyon 28-31", "Karkitox 29-31", "Hymnet 29-31", "Galenyon 30-32", "Karkitox 31-32"))

# Route 13, the highland road to Nemea (30-32): eagle chicks over the uplands by day,
# Athena's owlets at dusk. (The night table stays the builder's.)
table("MAP_ROUTE13_HIGHLAND_ROAD", "gRoute13_HighlandRoad", ["Morning", "Day"], land=rows(
    "Elapling 30-32", "Arkoby 30-32", "Kerazap 30-32", "Melisseer 30-32", "Nemeleon 30-32", "Cairnolith 30-32",
    "Aetling 30-32", "Arkoby 31-32", "Nemeleon 31-32", "Elapling 31-32", "Aetling 32", "Kerazap 32"))
table("MAP_ROUTE13_HIGHLAND_ROAD", "gRoute13_HighlandRoad", ["Evening"], land=rows(
    "Elapling 30-32", "Harpelle 30-32", "Kerazap 30-32", "Glaukoin 30-32", "Nemeleon 30-32", "Lykanax 31-32",
    "Arkoby 30-32", "Harpelle 31-32", "Prosomime 30-32", "Cairnolith 30-32", "Glaukoin 32", "Nemeleon 32"))

# Route 16, the capital pass (34-36): Athena's owls come out to meet the road to Astyra,
# and the Asklepian snakes sun on its walls.
table("MAP_ROUTE16_CAPITAL_PASS", "gRoute16_CapitalPass", ["Morning", "Day", "Evening"], land=rows(
    "Sophowl 34-36", "Hoplomex 34-36", "Cairnolith 34-36", "Thyrsivy 34-36", "Nemeleon 34-36", "Elapling 34-36",
    "Ophidrop 34-36", "Sophowl 35-36", "Thyrsivy 35-36", "Hoplomex 35-36", "Ophidrop 36", "Aetling 34-35"))
table("MAP_ROUTE16_CAPITAL_PASS", "gRoute16_CapitalPass", ["Night"], land=rows(
    "Sophowl 34-36", "Lykanax 34-36", "Harpelle 34-36", "Cairnolith 34-36", "Thyrsivy 34-36", "Nemeleon 34-36",
    "Sophowl 35-36", "Lykanax 35-36", "Persenyx 34-36", "Hoplomex 34-36", "Ophidrop 36", "Persenyx 36"))

# Kaldera (the caldera floor, 32-36): the bronze bulls' calves and the forge tripods as
# young things on the warm slopes, the Gigantes' Kapnub on the caldera floor.
for t in ("Morning", "Night"):
    table("MAP_KALDERA", "gKaldera", [t], land=rows(
        "Taurivet 34-36", "Laolith 33-36", "Kapnub 33-34", "Taurivet 33-35", "Narthip 33-35", "Laolith 34-36",
        "Kaminoo 32", "Pyrapod 32-33", "Kapnub 34", "Taurivet 36", "Kaminoo 32", "Pyrapod 33"))

# Route 25, the Eurotas (46-50): Leda's swans on Sparta's river.
table("MAP_ROUTE25_EUROTAS", "gRoute25_Eurotas", ["Morning", "Night"], water=rows(
    "Hymnaria 46-48", "Karkitox 46-48", "Hymnaria 47-49", "Kynoketos 48-50", "Hymnaria 49-50"))

# --------------------------------------------------------------------------------------
# The Erymanthian Preserve (Artemis's hunting park, a Safari Zone beside Arkadia, 28-32).
# Pan Balls only; what's rare elsewhere, or missing from the wild, lives here by the hour.
# --------------------------------------------------------------------------------------
PRESERVE = "MAP_ERYMANTHOS_PRESERVE_"
PRESERVE_BAND = (28, 32)           # BALANCE's Arkadia stage, five levels wide (MAP_DESIGN, map_audit)


def band(*specs):
    lo, hi = PRESERVE_BAND
    return [(s, min(max(a, lo), hi), min(max(b, lo), hi)) for s, a, b in rows(*specs)]


table(PRESERVE + "OAKWOOD", "gErymanthosPreserve_Oakwood", ["Morning", "Day", "Evening"], land=(20, band(
    "Kaplet 27-30", "Arkoby 27-30", "Skylaps 28-31", "Melibee 27-30", "Raknit 28-31", "Lophops 28-31",
    "Kaplet 30-32", "Skylaps 30-32", "Eripip 28-31", "Arkoby 31-32", "Kerdovix 31-33", "Kaprodon 33")))
table(PRESERVE + "OAKWOOD", "gErymanthosPreserve_Oakwood", ["Night"], land=(20, band(
    "Glaukoin 27-30", "Lykopup 27-30", "Kaplet 27-30", "Raknit 28-31", "Glaukoin 29-32", "Amnoze 28-31",
    "Lykopup 30-32", "Kerdovix 29-32", "Arkoby 28-31", "Amnoze 31-32", "Kerdovix 32-33", "Lykanax 32-33")))
table(PRESERVE + "MEADOW", "gErymanthosPreserve_Meadow", ["Morning", "Day", "Evening"], land=(20, band(
    "Eripip 27-30", "Chelonet 27-30", "Aetling 27-30", "Kryopuff 28-31", "Melibee 28-31", "Arkoby 28-31",
    "Aetling 30-32", "Kryopuff 30-32", "Eripip 31-32", "Chelonet 31-32", "Kerazap 32-33", "Skylaps 33")))
table(PRESERVE + "MEADOW", "gErymanthosPreserve_Meadow", ["Night"], land=(20, band(
    "Amnoze 27-30", "Kryopuff 27-30", "Lykopup 27-30", "Amnoze 29-32", "Chelonet 27-30", "Kryopuff 29-32",
    "Arkoby 28-31", "Lykopup 30-32", "Amnoze 31-32", "Kerdovix 31-32", "Glaukoin 32", "Lykanax 33")))
table(PRESERVE + "RIVER", "gErymanthosPreserve_River", ["Morning", "Day", "Evening"], land=(20, band(
    "Chalkip 27-30", "Melibee 27-30", "Hymnet 28-31", "Kaplet 27-30", "Chalkip 29-32", "Arkoby 28-31",
    "Halcyling 27-30", "Hymnet 30-32", "Raknit 28-31", "Chalkip 31-32", "Skylaps 32-33", "Hymnet 33")))
table(PRESERVE + "RIVER", "gErymanthosPreserve_River", ["Morning"], water=(4, band("Ketofry 27-30", "Hymnet 28-31", "Galenyon 30-32", "Hymnet 31-33", "Lernip 29")),
    fish=(30, band("Ketofry 27-29", "Karkipool 26-27", "Hymnet 28-30", "Ketofry 29-31", "Karkitox 28-30",
                   "Kynoketos 29-32", "Hymnet 30-32", "Karkitox 30-32", "Kynoketos 32-33", "Lernip 29")))
table(PRESERVE + "RIVER", "gErymanthosPreserve_River", ["Night"], land=(20, band(
    "Chalkip 27-30", "Lykopup 27-30", "Amnoze 28-31", "Raknit 27-30", "Kaplet 28-31", "Lykopup 29-32",
    "Chalkip 30-32", "Amnoze 30-32", "Glaukoin 29-32", "Raknit 31-32", "Kerdovix 32-33", "Lykanax 33")))
table(PRESERVE + "CAVE", "gErymanthosPreserve_Cave", ["Morning", "Night"], land=(10, band(
    "Pagoshard 27-30", "Spalunk 27-30", "Pebblith 27-30", "Raknit 28-31", "Pagoshard 29-32", "Obolorn 28-31",
    "Cairnolith 28-31", "Spalunk 30-32", "Pagoshard 31-33", "Kryopuff 30-32", "Obolorn 32-33", "Pagoshard 33")))
# The cold cave's seep pool (rods from its shore; the Conch onto it).
table(PRESERVE + "CAVE", "gErymanthosPreserve_Cave", ["Morning"], water=(4, band(
    "Ketofry 28-30", "Karkipool 28", "Ketofry 30-32", "Kynoketos 30-32", "Karkitox 32")), fish=(20, band(
    "Ketofry 28-29", "Karkipool 28", "Ketofry 29-31", "Karkitox 28-30", "Hymnet 28-30",
    "Kynoketos 29-31", "Karkitox 30-32", "Ketofry 31-32", "Kynoketos 31-32", "Karkitox 32")))
# The boar's thicket, sealed until the Erymanthian Boar's Labor (post-game, LABORS's 57-64).
table(PRESERVE + "THICKET", "gErymanthosPreserve_Thicket", ["Morning", "Night"], land=(20, rows(
    "Kaprodon 58-61", "Kaplet 58-60", "Borapteryx 58-61", "Lykanax 58-61", "Kaprodon 60-62", "Krystolos 59-62",
    "Chionyad 59-62", "Starkos 59-62", "Kaprodon 62", "Borapteryx 61-62", "Skylaps 62", "Kerdovix 62")))

# --------------------------------------------------------------------------------------
# Swaps: (map, times or None, methods or None) -> {old: new}
# --------------------------------------------------------------------------------------
SWAPS = [
    # Thyrsa (21-28). Route 6 loses the stone filler to its vines; Route 7's Kronia grounds
    # grow the Spartoi, Thebes's sown men (Kadmos sowed the dragon's teeth by Thyrsa).
    ("MAP_ROUTE6_ELEUTHERAI_ROAD", None, [L], {"PEBBLITH": "BOTRYKIT"}),
    ("MAP_ROUTE7_KRONIA_GROUNDS", None, [L], {"PEBBLITH": "SPORADON", "CAIRNOLITH": "SPORADON"}),
    ("MAP_ROUTE7_KRONIA_GROUNDS", ["Morning", "Day"], [L], {"GELASABLE": "AMPELIX"}),
    ("MAP_ROUTE7_KRONIA_GROUNDS", ["Evening", "Night"], [L], {"GELASABLE": "BOTRYKIT"}),
    # Lake Kopais's banks: Stymphalian chicks in the reeds instead of the coast's birds.
    ("MAP_ROUTE8_KOPAIS_ROAD", None, [L], {"KARKIPOOL": "CHALKIP", "GALENYON": "CHALKIP"}),
    # The Korykian cave, Pan's cave on Parnassos and the Python's: the young serpent.
    ("MAP_ROUTE9_KORYKIAN_CAVE", ["Morning"], [L], {"SPALUNK": "PELYTHON", "GALEKIT": "PELYTHON"}),
    ("MAP_ROUTE9_KORYKIAN_CAVE", ["Night"], [L], {"SPALUNK": "PELYTHON", "GELASABLE": "PELYTHON"}),
    # The Drum Pass: the Kouretes' cymbal-clashers among the column drums.
    ("MAP_ROUTE11_DRUM_PASS", None, [L], {"NEBREL": "KYMBASH", "PEBBLITH": "KYMBASH"}),
    # The Astyra road (30-36). No starter in the wild: Kladoe's slots go to the highland
    # eagles, Nemea's lion and wrestler, the Mystery road's Kore, and the owls at dusk.
    ("MAP_NEMEA", ["Morning", "Day"], [L], {"KLADOE": "HOPLOMEX", "GALENYON": "ELAPLING"}),
    ("MAP_NEMEA", ["Evening"], [L], {"KLADOE": "GLAUKOIN"}),
    ("MAP_ROUTE14_NEMEA_ROAD", None, [L], {"KLADOE": "HOPLOMEX", "GALENYON": "ELAPLING",
                                           "CAIRNOLITH": "ELAPLING", "HARPELLE": "GLAUKOIN"}),
    # Inland, the sea cliffs' harpies give way to the owlets of the Nemean hills.
    ("MAP_NEMEA", None, [L], {"HARPELLE": "GLAUKOIN"}),
    ("MAP_ROUTE14_TRETOS", None, [L], {"HARPELLE": "GLAUKOIN"}),
    # The Mystery road's bees: the Melissai were Demeter's priestesses.
    ("MAP_ROUTE15_MYSTERY_ROAD", None, [L], {"CAIRNOLITH": "MELISSEER"}),
    ("MAP_ROUTE15_MYSTERY_ROAD", ["Morning", "Day"], [L], {"KLADOE": "KORANTHA"}),
    ("MAP_ROUTE15_MYSTERY_ROAD", ["Evening"], [L], {"KLADOE": "GLAUKOIN"}),
    ("MAP_ROUTE15_MYSTERY_ROAD", ["Night"], [L], {"HARPELLE": "PERSENYX"}),
    # The Salt Well and the harbor: no starter; the sea's own Kynoketos instead.
    ("MAP_SALT_WELL_B1F", None, None, {"SEISMARE": "KYNOKETOS"}),
    ("MAP_SALT_WELL_B2F", None, None, {"SEISMARE": "KYNOKETOS"}),
    ("MAP_ASTYRA_HARBOR", None, None, {"SEISMARE": "KYNOKETOS"}),
    ("MAP_KALDERA", None, [W, F], {"SEISMARE": "KYNOKETOS"}),
    # Kythera after dark: the echoes instead of the mainland weasels.
    ("MAP_KYTHERA_FOAM_ROAD", None, [L], {"GELASABLE": "ECHOLALI"}),
    ("MAP_KYTHERA_SPRING_OF_KALLIRHOE", None, [L], {"GELASABLE": "ECHOLALI"}),
    ("MAP_KYTHERA_NERAIDA_FALLS", None, [L], {"GELASABLE": "NARCIBULB"}),
    # Knossa: the bull's road keeps its bulls, not the mainland goats.
    ("MAP_KNOSSA_BULL_ROAD", None, [L], {"KERAZAP": "TAURIVET", "GALENYON": "KOLOSSETTE"}),
    ("MAP_KNOSSA_BULL_ROAD_VINEYARD", None, [L], {"KERAZAP": "OINOPARD"}),
    # Lakonia (46-50): the Stymphalian birds grown, Sparta's swans and lions.
    ("MAP_ROUTE25_EUROTAS", None, [L], {"GELASABLE": "BELORNIS", "CHELONET": "STACHYPTER",
                                        "KERAZAP": "HYMNARIA", "CAIRNOLITH": "DORYDRAKE"}),
    ("MAP_LAKONIA", None, [L], {"KERAZAP": "BELORNIS", "GELASABLE": "NEMELEON", "CHELONET": "HOPLEKTOR"}),
    # Delphoi: the Kastalian swans where the coast's birds were.
    ("MAP_ROUTE28_SACRED_OLIVES", None, [L], {"GALENYON": "ELAPLING", "CAIRNOLITH": "HIEROLIVE",
                                              "GELASABLE": "LYKANAX"}),
    ("MAP_ROUTE28_KASTALIAN_GORGE", None, [L], {"GALENYON": "HYMNARIA"}),
    ("MAP_DELPHOI", None, [L], {"GALENYON": "HYMNARIA"}),
    # The Ascent: Stygiad only in the coldest dark (the Deep and the Crystal Vault).
    ("MAP_ASCENT_1F", None, None, {"STYGIAD": "KYNOKETOS"}),
    ("MAP_ASCENT_2F", None, [F], {"STYGIAD": "KYNOKETOS"}),
    ("MAP_ASCENT_2F", None, [L], {"STYGIAD": "CHIONYAD"}),
    ("MAP_ASCENT_ICEFALL", None, [W, F], {"STYGIAD": "KYNOKETOS"}),
    ("MAP_ASCENT_ICEFALL", None, [L], {"STYGIAD": "KRYSTOLOS"}),
    ("MAP_ASCENT_GLACIER", None, [W, F], {"STYGIAD": "KYNOKETOS"}),
    ("MAP_ASCENT_GLACIER", None, [L], {"STYGIAD": "KRYSTOLOS"}),
    ("MAP_ASCENT_3F", None, [L], {"STYGIAD": "KRYSTOLOS"}),
]
# Starters never live in the wild (Nebrel's old slots on Routes 9 and 12 are rewritten above).

# --------------------------------------------------------------------------------------
# Single slots: (map, time, method, index, row)
# --------------------------------------------------------------------------------------
SLOTS = [
    # Mt Kithairon after dark: the Teumessian vixen that plagued Thebes, very rarely.
    ("MAP_MT_KITHAIRON", "Evening", L, 10, "Kerdovix 26-27"),
    ("MAP_MT_KITHAIRON", "Night", L, 11, "Kerdovix 27"),
    # Nemea's palaestra: Antaeus's wrestler, in the rarest slot.
    ("MAP_NEMEA", "Morning", L, 11, "Geogrip 33"),
    ("MAP_NEMEA", "Day", L, 11, "Geogrip 33"),
    # The Tretos pass's rubble hides a wrestler too.
    ("MAP_ROUTE14_TRETOS", "Morning", R, 4, "Geogrip 34"),
    # Salmoneus's bronze-cauldron thunderer, in the Ascent's foothills.
    ("MAP_ASCENT_1F", "Morning", L, 11, "Lebetron 56-58"),
    ("MAP_ASCENT_1F", "Night", L, 11, "Lebetron 56-58"),
]


def _mons(rs):
    return [{"min_level": lo, "max_level": hi, "species": "SPECIES_" + s} for s, lo, hi in rs]


def _entry(entries, mapid, label, create=False):
    e = next((e for e in entries if e.get("base_label") == label), None)
    if e is None and create:
        e = {"map": mapid, "base_label": label}
        entries.append(e)
    return e


def _time(e):
    t = e["base_label"].rsplit("_", 1)[-1]
    return t if t in TIMES else "Morning"


def _evolutions():
    """const -> (previous stage const, level it evolves at) from the Aethos families."""
    text = (ROOT / "src/data/pokemon/species_info/aethos_families.h").read_text()
    prev = {}
    for m in re.finditer(r"\[SPECIES_(\w+)\] =\s*\{(.*?)\n    \},", text, re.S):
        for e in re.finditer(r"\{EVO_LEVEL, (\d+), SPECIES_(\w+)", m.group(2)):
            if int(e.group(1)):
                prev[e.group(2)] = (m.group(1), int(e.group(1)))
    return prev


def _map_ids():
    ids = set()
    for p in (ROOT / "data/maps").glob("*/map.json"):
        m = re.search(r'"id": "(MAP_\w+)"', p.read_text())
        if m:
            ids.add(m.group(1))
    return ids


def apply(entries):
    """Rewrite the planned tables in a wild_encounters.json encounter list, in place."""
    ids = _map_ids()
    for (mapid, stem, t), methods in TABLES.items():
        if mapid not in ids:  # a planned map not built yet
            continue
        e = _entry(entries, mapid, f"{stem}_{t}", create=True)
        for meth, (rate, rs) in methods.items():
            assert len(rs) == COUNTS[meth], (mapid, t, meth, len(rs))
            old = e.get(meth, {}).get("encounter_rate")
            if rate is None and old is None:
                raise ValueError(f"{mapid} {t} {meth}: a new table needs its encounter rate")
            e[meth] = {"encounter_rate": rate if rate is not None else old, "mons": _mons(rs)}
    for mapid, times, methods, swap in SWAPS:
        for e in entries:
            if e.get("map") != mapid or (times and _time(e) not in times):
                continue
            for meth in methods or COUNTS:
                for mon in e.get(meth, {}).get("mons", []):
                    s = mon["species"].removeprefix("SPECIES_")
                    if s in swap:
                        mon["species"] = "SPECIES_" + swap[s]
    for mapid, t, meth, i, row in SLOTS:
        e = next((e for e in entries if e.get("map") == mapid and _time(e) == t and meth in e), None)
        if e is None:
            raise ValueError(f"{mapid} {t} {meth}: no table for slot {i}")
        e[meth]["mons"][i] = _mons(rows(row))[0]
    prev = _evolutions()
    for e in entries:
        for meth in COUNTS:
            for mon in e.get(meth, {}).get("mons", []):
                s = mon["species"].removeprefix("SPECIES_")
                while s in prev and mon["min_level"] < prev[s][1]:
                    s = prev[s][0]
                mon["species"] = "SPECIES_" + s
    return entries


def ichor_entries(data):
    return next(g for g in data["wild_encounter_groups"] if g.get("for_maps"))["encounters"]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="exit 1 if the json doesn't match the plan")
    args = ap.parse_args()
    text = PATH.read_text()
    data = json.loads(text)
    apply(ichor_entries(data))
    new = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if json.loads(new) != json.loads(text):
            print("wild_plan: src/data/wild_encounters.json disagrees with tools/ichor/wild_plan.py; run it")
            return 1
        print("wild_plan: ok")
        return 0
    PATH.write_text(new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
