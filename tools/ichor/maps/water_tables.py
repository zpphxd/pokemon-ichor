#!/usr/bin/env python3
"""Surf and fishing tables for the maps whose water was solid until the
fishing audit (tools/ichor/fishing_audit.py) opened it. The map builders call
tables(); run this to write them into src/data/wild_encounters.json without
rerunning the builders:

  /usr/bin/python3 tools/ichor/maps/water_tables.py

Every map's entries keep their land tables; this adds water_mons and
fishing_mons to the _Morning one (the engine falls back to it at any hour, per
area). A fishing table is Emerald's ten slots: 0-1 Old Rod, 2-4 Good Rod, 5-9
Super Rod. Species follow design/dex/species habitats; levels follow each
map's land band (BALANCE.md), the Old Rod a little under it.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / "src/data/wild_encounters.json"


def _mons(rows):
    return [{"min_level": lo, "max_level": hi, "species": "SPECIES_" + s} for s, lo, hi in rows]


def _table(surf, fish, surf_rate=4, fish_rate=30):
    out = {}
    if surf:
        assert len(surf) == 5
        out["water_mons"] = {"encounter_rate": surf_rate, "mons": _mons(surf)}
    assert len(fish) == 10
    out["fishing_mons"] = {"encounter_rate": fish_rate, "mons": _mons(fish)}
    return out


def sea(L, surf=True):
    """Mainland coast and the Gulf: Ketofry in any water, Karkipool off the rocks,
    Narkeray on the trireme crossings, Kynoketos off the headlands."""
    return _table(
        [("HALCYLING", L, L + 2), ("KETOFRY", L, L + 2), ("GALENYON", L + 1, L + 3),
         ("NARKERAY", L + 1, L + 3), ("GALENYON", L + 3, L + 4)] if surf else None,
        [("KETOFRY", L - 8, L - 6), ("KARKIPOOL", L - 8, L - 6),
         ("KETOFRY", L - 3, L - 1), ("KARKIPOOL", L - 3, L - 1), ("NARKERAY", L - 2, L),
         ("KYNOKETOS", L, L + 3), ("NARKERAY", L, L + 3), ("KARKIPOOL", L, L + 2),
         ("KYNOKETOS", L + 3, L + 5), ("NARKERAY", L + 3, L + 5)])


def lake(L):
    """Lake Kopais: Ketofry, the shore's Halcyling and Galenyon, and Karkitox in the
    reed marshes, as at Lake Stymphalia."""
    return _table(
        [("HALCYLING", L, L + 2), ("KETOFRY", L, L + 2), ("GALENYON", L + 1, L + 3),
         ("HALCYLING", L + 2, L + 3), ("GALENYON", L + 3, L + 4)],
        [("KETOFRY", L - 6, L - 4), ("KETOFRY", L - 4, L - 2),
         ("KETOFRY", L - 1, L + 1), ("HALCYLING", L - 1, L + 1), ("KARKITOX", L, L + 2),
         ("GALENYON", L + 1, L + 4), ("KARKITOX", L + 2, L + 4), ("KETOFRY", L + 2, L + 4),
         ("GALENYON", L + 3, L + 5), ("KARKITOX", L + 4, L + 5)])


def pond(L):
    """Inland pools and streams: Ketofry, Galenyon fishing the banks, Halcyling,
    and Kynoketos with the Super Rod."""
    return _table(
        [("KETOFRY", L, L + 2), ("HALCYLING", L, L + 2), ("GALENYON", L + 1, L + 3),
         ("KETOFRY", L + 2, L + 3), ("GALENYON", L + 3, L + 4)],
        [("KETOFRY", L - 6, L - 4), ("HALCYLING", L - 6, L - 4),
         ("KETOFRY", L - 1, L + 1), ("HALCYLING", L - 1, L + 1), ("GALENYON", L, L + 2),
         ("KYNOKETOS", L + 1, L + 3), ("GALENYON", L + 1, L + 3), ("KETOFRY", L + 1, L + 3),
         ("KYNOKETOS", L + 3, L + 4), ("GALENYON", L + 3, L + 4)])


def forge(L):
    """The Telchines' forge pool: Telpup fishing the shallows and Telkanvil in the
    deep, as in Kaldera's sea caves."""
    return _table(
        [("TELPUP", L - 2, L), ("TELKANVIL", L, L + 2), ("KARKITOX", L, L + 2),
         ("TELPUP", L, L + 2), ("TELKANVIL", L + 2, L + 3)],
        [("KETOFRY", L - 8, L - 6), ("TELPUP", L - 6, L - 4),
         ("TELPUP", L - 3, L - 1), ("KETOFRY", L - 3, L - 1), ("KARKITOX", L - 2, L),
         ("TELKANVIL", L, L + 2), ("TELPUP", L, L + 2), ("KARKITOX", L, L + 2),
         ("TELKANVIL", L + 2, L + 3), ("TELKANVIL", L + 3, L + 3)], surf_rate=6, fish_rate=20)


def falls(L):
    """Neraida Falls' river: Aphrell washed down from the foam, Galenyon, Ketofry."""
    return _table(None,
        [("KETOFRY", L - 7, L - 5), ("APHRELL", L - 7, L - 5),
         ("KETOFRY", L - 1, L + 1), ("APHRELL", L - 1, L + 1), ("GALENYON", L, L + 2),
         ("KYNOKETOS", L + 1, L + 3), ("GALENYON", L + 2, L + 4), ("APHRELL", L + 2, L + 4),
         ("KYNOKETOS", L + 3, L + 4), ("GALENYON", L + 4, L + 4)])


def spring(L):
    """The Ascent's springs: cold water under the weeping cliff, final forms only
    (BALANCE.md from Astyra on). Dakrock is the rare one at the foot of the cliff."""
    return _table(None,
        [("KYNOKETOS", L - 2, L), ("GALENYON", L - 2, L),
         ("KYNOKETOS", L, L + 2), ("GALENYON", L, L + 2), ("STYGIAD", L, L + 2),
         ("KYNOKETOS", L + 2, L + 4), ("GALENYON", L + 2, L + 4), ("STYGIAD", L + 2, L + 4),
         ("DAKROCK", L + 3, L + 4), ("DAKROCK", L + 4, L + 4)], fish_rate=20)


# map -> (base label of the entry to add to, its tables)
TABLES = {
    "MAP_ROUTE8_KOPAIS_ROAD": ("gRoute8_KopaisRoad_Morning", lake(27)),
    "MAP_KIRRHA": ("gKirrha_Morning", sea(27)),
    "MAP_GULF_TRIREME": ("gGulfTrireme_Morning", sea(28, surf=False)),
    "MAP_AIGION": ("gAigion_Morning", sea(28)),
    "MAP_ROUTE12_CYPRESS_ROAD": ("gRoute12_CypressRoad_Morning", pond(30)),
    "MAP_ROUTE15_MYSTERY_ROAD": ("gRoute15_MysteryRoad_Morning", sea(33)),
    "MAP_KALDERA_TELCHINES_FORGE": ("gKaldera_TelchinesForge_Morning", forge(37)),
    "MAP_KYTHERA_NERAIDA_FALLS": ("gKytheraNeraidaFalls_Morning", falls(42)),
    "MAP_ASCENT_1F": ("gAscent_1F_Morning", spring(53)),
    "MAP_ASCENT_2F": ("gAscent_2F_Morning", spring(55)),
}


def apply(entries, maps=None):
    """Add the water tables to the matching entries (creating the entry if needed)."""
    for mapid, (label, t) in TABLES.items():
        if maps and mapid not in maps:
            continue
        e = next((e for e in entries if e.get("base_label") == label), None)
        if e is None:
            e = {"map": mapid, "base_label": label}
            entries.append(e)
        e.update(json.loads(json.dumps(t)))


def main():
    data = json.loads(PATH.read_text())
    group = next(g for g in data["wild_encounter_groups"] if g.get("for_maps"))
    apply(group["encounters"])
    PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
