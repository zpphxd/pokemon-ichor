#!/usr/bin/env python3
"""Register the Oikoumene's maps for a batch (design/oikoumene/BUILD.md §5).

  python3 tools/ichor/oikoumene_register.py 1     # register batch 1's maps

Runs tools/ichor/new_map.py once per map not yet registered, so the parallel agents
never edit map_groups.json, ichor_maps.inc or .gitignore themselves. Layouts are
placeholders copied from Akti's; each owner rewrites its own.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

OUT = "gMapGroup_Oikoumene"
TOWN, CITY, ROUTE, SEA, IN = ("MAP_TYPE_TOWN", "MAP_TYPE_CITY", "MAP_TYPE_ROUTE",
                              "MAP_TYPE_OCEAN_ROUTE", "MAP_TYPE_INDOOR")
OUTDOOR_FROM = "LAYOUT_AKTI_TOWN"
ROOM_FROM = "LAYOUT_AKTI_TOWN_FISHERS_HOUSE"
CIVIC_FROM = "LAYOUT_AKTI_TOWN_ASCLEPEION"

# name, group, type, mapsec, music (stand-ins until the music agent's songs land)
BATCHES = {
    1: [
        # The Troad
        ("Sestos", OUT, TOWN, "MAPSEC_SESTOS", "MUS_ICHOR_AKTI"),
        ("Hellespont", OUT, SEA, "MAPSEC_HELLESPONT", "MUS_ICHOR_TRIREME"),
        ("Ilion", OUT, CITY, "MAPSEC_ILION", "MUS_ICHOR_EMPORION"),
        ("Sestos_Asclepeion", "gMapGroup_IndoorTroad", IN, "MAPSEC_SESTOS", "MUS_ICHOR_ASCLEPEION"),
        ("Sestos_Agora", "gMapGroup_IndoorTroad", IN, "MAPSEC_SESTOS", "MUS_ICHOR_AGORA"),
        ("Sestos_HerosTower", "gMapGroup_IndoorTroad", IN, "MAPSEC_SESTOS", "MUS_ICHOR_AKTI"),
        ("Sestos_FerryHouse", "gMapGroup_IndoorTroad", IN, "MAPSEC_SESTOS", "MUS_ICHOR_AKTI"),
        ("Sestos_NetLoft", "gMapGroup_IndoorTroad", IN, "MAPSEC_SESTOS", "MUS_ICHOR_AKTI"),
        ("Ilion_Asclepeion", "gMapGroup_IndoorTroad", IN, "MAPSEC_ILION", "MUS_ICHOR_ASCLEPEION"),
        ("Ilion_Agora", "gMapGroup_IndoorTroad", IN, "MAPSEC_ILION", "MUS_ICHOR_AGORA"),
        ("Ilion_PriamsPalace", "gMapGroup_IndoorTroad", IN, "MAPSEC_ILION", "MUS_ICHOR_EMPORION"),
        ("Ilion_CassandrasRoom", "gMapGroup_IndoorTroad", IN, "MAPSEC_ILION", "MUS_ICHOR_EMPORION"),
        ("Ilion_GuestRoom", "gMapGroup_IndoorTroad", IN, "MAPSEC_ILION", "MUS_ICHOR_EMPORION"),
        ("Ilion_HorseStable", "gMapGroup_IndoorTroad", IN, "MAPSEC_ILION", "MUS_ICHOR_EMPORION"),
        ("Ilion_MasonsHouse", "gMapGroup_IndoorTroad", IN, "MAPSEC_ILION", "MUS_ICHOR_EMPORION"),
        ("Ilion_WeaversHouse", "gMapGroup_IndoorTroad", IN, "MAPSEC_ILION", "MUS_ICHOR_EMPORION"),
        ("Ilion_TempleOfAthena", "gMapGroup_IndoorTroad", IN, "MAPSEC_ILION", "MUS_ICHOR_TEMPLE"),
        # Egypt
        ("Naukratis", OUT, TOWN, "MAPSEC_NAUKRATIS", "MUS_ICHOR_AKTI"),
        ("Pharos", OUT, ROUTE, "MAPSEC_PHAROS", "MUS_ICHOR_ROAD"),
        ("DeltaReeds", OUT, ROUTE, "MAPSEC_DELTA_REEDS", "MUS_ICHOR_ROAD"),
        ("Memphis", OUT, CITY, "MAPSEC_MEMPHIS", "MUS_ICHOR_EMPORION"),
        ("Naukratis_Asclepeion", "gMapGroup_IndoorEgypt", IN, "MAPSEC_NAUKRATIS", "MUS_ICHOR_ASCLEPEION"),
        ("Naukratis_Agora", "gMapGroup_IndoorEgypt", IN, "MAPSEC_NAUKRATIS", "MUS_ICHOR_AGORA"),
        ("Naukratis_FieldStation", "gMapGroup_IndoorEgypt", IN, "MAPSEC_NAUKRATIS", "MUS_ICHOR_AKTI"),
        ("Naukratis_EggOvens", "gMapGroup_IndoorEgypt", IN, "MAPSEC_NAUKRATIS", "MUS_ICHOR_AKTI"),
        ("Naukratis_IncenseShop", "gMapGroup_IndoorEgypt", IN, "MAPSEC_NAUKRATIS", "MUS_ICHOR_AGORA"),
        ("Naukratis_PottersHouse", "gMapGroup_IndoorEgypt", IN, "MAPSEC_NAUKRATIS", "MUS_ICHOR_AKTI"),
        ("Naukratis_NetLoft", "gMapGroup_IndoorEgypt", IN, "MAPSEC_NAUKRATIS", "MUS_ICHOR_AKTI"),
        ("Memphis_Asclepeion", "gMapGroup_IndoorEgypt", IN, "MAPSEC_MEMPHIS", "MUS_ICHOR_ASCLEPEION"),
        ("Memphis_Agora", "gMapGroup_IndoorEgypt", IN, "MAPSEC_MEMPHIS", "MUS_ICHOR_AGORA"),
        ("Memphis_ApisStable", "gMapGroup_IndoorEgypt", IN, "MAPSEC_MEMPHIS", "MUS_ICHOR_EMPORION"),
        ("Memphis_ScribesHouse", "gMapGroup_IndoorEgypt", IN, "MAPSEC_MEMPHIS", "MUS_ICHOR_EMPORION"),
        ("Memphis_EmbalmersHouse", "gMapGroup_IndoorEgypt", IN, "MAPSEC_MEMPHIS", "MUS_ICHOR_EMPORION"),
        # The Black Sea
        ("Bosporus", OUT, SEA, "MAPSEC_BOSPORUS", "MUS_ICHOR_TRIREME"),
        ("Salmydessos", OUT, TOWN, "MAPSEC_SALMYDESSOS", "MUS_ICHOR_AKTI"),
        ("PonticCoast", OUT, SEA, "MAPSEC_PONTIC_COAST", "MUS_ICHOR_TRIREME"),
        ("Aia", OUT, CITY, "MAPSEC_AIA", "MUS_ICHOR_EMPORION"),
        ("Salmydessos_PhineussHouse", "gMapGroup_IndoorPontos", IN, "MAPSEC_SALMYDESSOS", "MUS_ICHOR_AKTI"),
        ("Salmydessos_BirdCatchersHouse", "gMapGroup_IndoorPontos", IN, "MAPSEC_SALMYDESSOS", "MUS_ICHOR_AKTI"),
        ("Aia_Asclepeion", "gMapGroup_IndoorPontos", IN, "MAPSEC_AIA", "MUS_ICHOR_ASCLEPEION"),
        ("Aia_Agora", "gMapGroup_IndoorPontos", IN, "MAPSEC_AIA", "MUS_ICHOR_AGORA"),
        ("Aia_PhrixosSonsHouse", "gMapGroup_IndoorPontos", IN, "MAPSEC_AIA", "MUS_ICHOR_EMPORION"),
        ("Aia_LinenWeaversHouse", "gMapGroup_IndoorPontos", IN, "MAPSEC_AIA", "MUS_ICHOR_EMPORION"),
        ("Aia_PalaceWorkshop", "gMapGroup_IndoorPontos", IN, "MAPSEC_AIA", "MUS_ICHOR_EMPORION"),
    ],
}


def registered(name):
    return (ROOT / "data/maps" / name / "map.json").exists()


def main():
    batch = int(sys.argv[1])
    for name, group, mtype, mapsec, music in BATCHES[batch]:
        if registered(name):
            continue
        civic = name.endswith(("_Asclepeion", "_Agora"))
        src = OUTDOOR_FROM if mtype != IN else (CIVIC_FROM if civic else ROOM_FROM)
        cmd = [sys.executable, str(ROOT / "tools/ichor/new_map.py"), name, "--group", group,
               "--layout-from", src, "--mapsec", mapsec, "--music", music, "--type", mtype]
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
