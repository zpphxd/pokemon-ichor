#!/usr/bin/env python3
"""Name the Oikoumene's map sections (design/oikoumene/BUILD.md, "Sections").

The Hoenn cut left ids 0-85 as MAPSEC_OIKOUMENE_<id>. This gives each usable slot
its place, and puts the lands that don't fit into the Kanto block's spare tail
(after MAPSEC_RHODOS), which a second range check reads as the Oikoumene too.

  python3 tools/ichor/oikoumene_sections.py          # apply (idempotent)
  python3 tools/ichor/oikoumene_sections.py --list   # print id, name

It rewrites the slot ids and names in src/data/region_map/region_map_sections.json,
the Hoenn alias lines in include/constants/region_map_sections_hoenn.h, and writes
include/constants/region_map_sections_oikoumene.h (the Kanto tail's aliases and the
two range markers). Positions on the chart are tools/ichor/art/ui_oikoumene_map.py's;
this keeps each section's position with it when the tables move it to another id.
Everything names sections, never numbers, so renumbering before release is safe.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON = ROOT / "src/data/region_map/region_map_sections.json"
HOENN = ROOT / "include/constants/region_map_sections_hoenn.h"
OIK_H = ROOT / "include/constants/region_map_sections_oikoumene.h"

# Hoenn slots upstream code still treats specially (weather, battle tent, Safari
# Zone, underwater and dive, follower messages, the dex area screen, Mirage
# Island, the truck). The chart's audit (design/oikoumene/MAPS_chart.md) kept
# them unnamed: there's room without them, and 58 is the kept Battle Frontier.
SKIP_HOENN = {2, 8, 50, 51, 52, 53, 54, 57, 58, 59, 65, 66, 68, 69, 71, 79, 84, 85}

# Sections pinned to a particular slot, swapped with whoever would have had it.
# 62 was New Mauville: the expansion evolves Magneton, Nosepass and Charjabug
# by level in MAPSEC_NEW_MAUVILLE (IF_IN_MAPSEC, gen_1/3/7_families.h), so that
# slot is the Oikoumene's magnetic place. Gargaros, Ida's summit, where Pliny's
# shepherd Magnes found the lodestone held his iron-nailed sandals (NH 36.127).
PINNED = {"GARGAROS_PEAK": 62}

# (constant suffix, display name). Grouped by land, in OIKOUMENE.md's order.
# (L) = LABORS's map and (O) = ODYSSEY's, built by world-postgame on this chart.
HOENN_BLOCK = [
    ("AETHOS", "AETHOS"),                       # the crossing target at the center
    # 4.1 Thrace and the Troad
    ("SESTOS", "SESTOS"),
    ("HELLESPONT", "THE HELLESPONT"),
    ("ILION", "ILION"),
    ("SKAMANDER_PLAIN", "SKAMANDER PLAIN"),
    ("IDA_ROAD", "THE IDA ROAD"),
    ("GARGAROS_PEAK", "GARGAROS PEAK"),
    ("WALLS_OF_LAOMEDON", "LAOMEDON'S WALLS"),
    ("CHRYSE", "CHRYSE"),
    ("HEBROS_SHORE", "HEBROS SHORE"),
    ("ABDERA", "ABDERA"),                       # (L) Labor 8
    ("BISTONIAN_PLAIN", "BISTONIAN PLAIN"),     # (L) Labor 8
    # 4.5 Egypt
    ("NAUKRATIS", "NAUKRATIS"),
    ("DELTA_REEDS", "THE DELTA REEDS"),
    ("PHAROS", "PHAROS"),
    ("MEMPHIS", "MEMPHIS"),
    ("PYRAMID_FIELD", "PYRAMID FIELD"),
    ("GREAT_PYRAMID", "GREAT PYRAMID"),
    ("NILE", "THE NILE"),
    ("HELIOPOLIS", "HELIOPOLIS"),
    ("LAKE_MOERIS", "LAKE MOERIS"),
    ("VALLEY_OF_TOMBS", "VALLEY OF TOMBS"),
    ("HEKATOMPYLOS", "HEKATOMPYLOS"),
    ("ELEPHANTINE", "ELEPHANTINE"),
    ("ABYDOS", "ABYDOS"),
    # 4.3 The Black Sea
    ("BOSPORUS", "THE BOSPORUS"),
    ("SALMYDESSOS", "SALMYDESSOS"),
    ("PONTIC_COAST", "PONTIC COAST"),
    ("THEMISKYRA", "THEMISKYRA"),               # (L) Labor 9
    ("THERMODON_ROAD", "THERMODON ROAD"),       # (L) Labor 9
    ("AIA", "AIA"),
    ("PHASIS", "THE PHASIS"),
    ("FIELD_OF_ARES", "FIELD OF ARES"),
    ("GROVE_OF_ARES", "GROVE OF ARES"),
    ("LEUKE", "LEUKE"),
    ("ISLE_OF_ARES", "ISLE OF ARES"),
    ("CAUCASUS", "THE CAUCASUS"),               # (L) the crag; this file's caves below
    ("CHALYBIA", "CHALYBIA"),
    # 4.2 Lydia and Phrygia
    ("ROYAL_ROAD", "THE ROYAL ROAD"),
    ("SARDIS", "SARDIS"),
    ("PACTOLUS_SANDS", "PACTOLUS SANDS"),
    ("MOUNT_TMOLUS", "MOUNT TMOLUS"),
    ("HYPAIPA", "HYPAIPA"),
    ("MAEANDER", "THE MAEANDER"),
    ("MILETOS", "MILETOS"),
    ("MOUNT_LATMOS", "MOUNT LATMOS"),
    ("CHASM_OF_GYGES", "CHASM OF GYGES"),
    ("GORDION", "GORDION"),
    ("MOUNT_SIPYLOS", "MOUNT SIPYLOS"),
    # 4.7 Libya
    ("AMMONION", "AMMONION"),
    ("SAND_SEA", "GREAT SAND SEA"),
    ("KYRENE", "KYRENE"),
    ("SILPHIUM_PLATEAU", "SILPHIUM PLATEAU"),
    ("TRITONIS", "TRITONIS"),
    ("SYRTIS", "SYRTIS SHALLOWS"),
    ("SALT_RIDGE", "THE SALT RIDGE"),
    ("ANTAEUS_RING", "ANTAEUS'S RING"),
    ("GARAMANTES_TUNNELS", "GARAMANTES"),
    ("GLASS_CRATER", "GLASS CRATER"),
    # 4.4 Scythia and Hyperborea
    ("OLBIA", "OLBIA"),
    ("STEPPE_ROAD", "THE STEPPE ROAD"),
    ("LAKE_MAEOTIS", "LAKE MAEOTIS"),
    ("FEATHER_WASTES", "FEATHER WASTES"),
    ("ARIMASPIAN_HEIGHTS", "ARIMASPI HEIGHTS"),
    ("RHIPAEAN_PASS", "RHIPAEAN PASS"),
    ("CAVE_OF_BOREAS", "CAVE OF BOREAS"),
    ("HYPERBOREA", "HYPERBOREA"),
]

# The Aethos chart's crossing target: on the Aethos chart, so outside both ranges.
AETHOS_CHART = [("THE_OIKOUMENE", "THE OIKOUMENE")]

KANTO_TAIL = [
    # 4.6 Aithiopia
    ("CATARACTS", "THE CATARACTS"),
    ("MEROE", "MEROE"),
    ("TABLE_OF_THE_SUN", "TABLE OF THE SUN"),
    ("MOUNT_NYSA", "MOUNT NYSA"),
    ("MOUNTAINS_OF_THE_MOON", "MOON MOUNTAINS"),
    ("PYGMY_MARSHES", "PYGMY MARSHES"),
    ("GATE_OF_DAWN", "GATE OF DAWN"),
    # 4.8 The Far West
    ("PILLARS", "THE PILLARS"),                 # (L) the Strait of the Pillars; this file's waters
    ("OCEAN_STREAM", "OCEAN STREAM"),           # (L) Labor 10
    ("ERYTHEIA", "ERYTHEIA"),                   # (L) Labor 10
    ("HESPERIDES", "THE HESPERIDES"),           # (L) Labor 11
    ("ATLAS_RIDGE", "ATLAS'S RIDGE"),           # (L) Labor 11
    ("GADEIRA", "GADEIRA"),
    ("TARTESSOS", "TARTESSOS"),
    ("ATARANTES", "THE ATARANTES"),
    ("ATLANTIC_SHORE", "ATLANTIC SHORE"),
    ("ATLAS_RANGE", "ATLAS RANGE"),
    # 4.9 The Western Sea
    ("WINE_DARK_SEA", "WINE-DARK SEA"),         # (O) east and west halves
    ("OUTER_SEA", "THE OUTER SEA"),             # (O) with Proteus's islet
    ("LOTUS_ISLE", "LOTUS ISLE"),               # (O)
    ("CYCLOPS_ISLE", "CYCLOPS ISLE"),           # (O)
    ("AIOLIA", "AIOLIA"),                       # (O)
    ("AIAIA", "AIAIA"),                         # (O)
    ("SIRENS_ROCKS", "SIRENS' ROCKS"),          # (O)
    ("SCYLLA_STRAIT", "THE STRAIT"),            # (O) Scylla and Charybdis
    ("THRINAKIA", "THRINAKIA"),                 # (O)
    ("KROTON", "KROTON"),
    ("CUMAE", "CUMAE"),
    ("ELEA", "ELEA"),
    ("PHLEGRAEAN_FIELDS", "BURNING FIELDS"),
    ("OGYGIA", "OGYGIA"),
    # 4.10 The Ring of Okeanos
    ("OKEANOS", "OKEANOS"),
    ("CIMMERIAN_SHORE", "CIMMERIAN SHORE"),
    ("LAND_OF_DREAMS", "LAND OF DREAMS"),
    ("GATES_OF_THE_SUN", "GATES OF THE SUN"),
    ("ISLES_OF_THE_BLESSED", "BLESSED ISLES"),
    ("GORGONS_ISLE", "GORGONS' ISLE"),
    ("GRAIAI", "CAVE OF GRAIAI"),
    ("SPRINGS_OF_OKEANOS", "OKEANOS SPRINGS"),
    ("SELVAGE", "THE SELVAGE"),
]


# The Kanto block's spare tail as upstream named it, in id order (FRLG only).
KANTO_TAIL_UPSTREAM = """SEAFOAM_ISLANDS POKEMON_TOWER CERULEAN_CAVE POWER_PLANT ONE_ISLAND TWO_ISLAND
THREE_ISLAND FOUR_ISLAND FIVE_ISLAND SEVEN_ISLAND SIX_ISLAND KINDLE_ROAD TREASURE_BEACH
CAPE_BRINK BOND_BRIDGE THREE_ISLE_PORT RESORT_GORGEOUS WATER_LABYRINTH FIVE_ISLE_MEADOW
MEMORIAL_PILLAR OUTCAST_ISLAND GREEN_PATH WATER_PATH RUIN_VALLEY TRAINER_TOWER
CANYON_ENTRANCE SEVAULT_CANYON TANOBY_RUINS SEVII_ISLE_22 SEVII_ISLE_23 SEVII_ISLE_24
NAVEL_ROCK_FRLG MT_EMBER BERRY_FOREST ICEFALL_CAVE ROCKET_WAREHOUSE TRAINER_TOWER_2
DOTTED_HOLE LOST_CAVE PATTERN_BUSH ALTERING_CAVE_FRLG TANOBY_CHAMBERS THREE_ISLE_PATH
TANOBY_KEY BIRTH_ISLAND_FRLG MONEAN_CHAMBER LIPTOO_CHAMBER WEEPTH_CHAMBER DILFORD_CHAMBER
SCUFIB_CHAMBER RIXY_CHAMBER VIAPOIS_CHAMBER EMBER_SPA""".split()
KANTO_TAIL_UPSTREAM = ["MAPSEC_" + n for n in KANTO_TAIL_UPSTREAM]


POSITION_KEYS = ("x", "y", "width", "height")


def hoenn_slots():
    """{slot: (suffix, display)} for the Hoenn block: the names in order over
    the usable slots, then PINNED swaps."""
    usable = [i for i in range(86) if i not in SKIP_HOENN]
    if len(HOENN_BLOCK) > len(usable):
        raise SystemExit(f"{len(HOENN_BLOCK)} names for {len(usable)} Hoenn slots")
    slots = dict(zip(usable, HOENN_BLOCK))
    for suffix, want in PINNED.items():
        have = next(s for s, (n, _) in slots.items() if n == suffix)
        if want not in slots:
            raise SystemExit(f"PINNED {suffix} to {want}, which is skipped or unused")
        slots[have], slots[want] = slots[want], slots[have]
    return slots


def main():
    data = json.loads(JSON.read_text())
    secs = data["map_sections"]
    ids = [s["id"] for s in secs]
    # the chart builder's positions, kept with their section across a renumbering
    positions = {s["id"]: {k: s[k] for k in POSITION_KEYS if k in s} for s in secs}

    # Hoenn block: slots 0-85 in json order are ids 0-85. A slot may hold its
    # MAPSEC_OIKOUMENE_<id> placeholder or any Oikoumene name (renumbering).
    ours = {"MAPSEC_" + n for n, _ in HOENN_BLOCK} | {f"MAPSEC_OIKOUMENE_{i:02d}" for i in range(86)}
    slots = hoenn_slots()
    slot_of = {}  # current id string -> slot
    for slot in range(86):
        cur = secs[slot]["id"]
        if slot in SKIP_HOENN and cur == "MAPSEC_BATTLE_FRONTIER":
            continue
        if cur not in ours:
            raise SystemExit(f"slot {slot} is {cur}, which isn't the Oikoumene's")
        slot_of[cur] = slot
    for slot in range(86):
        if secs[slot]["id"] == "MAPSEC_BATTLE_FRONTIER":
            continue
        if slot in slots:
            suffix, display = slots[slot]
            new = "MAPSEC_" + suffix
            secs[slot] = {"id": new, "name": display, **positions.get(new, {})}
        else:
            secs[slot] = {"id": f"MAPSEC_OIKOUMENE_{slot:02d}"}
    new_at = {slot: secs[slot]["id"] for slot in range(86)}

    # Kanto tail: the spare ids after MAPSEC_RHODOS, before MAPSEC_SPECIAL_AREA.
    start = ids.index("MAPSEC_RHODOS") + 1
    tail_names = AETHOS_CHART + KANTO_TAIL
    if len(tail_names) > len(KANTO_TAIL_UPSTREAM):
        raise SystemExit("too many names for the Kanto tail")
    kanto_aliases = []  # (upstream name, new constant)
    for k, (suffix, display) in enumerate(tail_names):
        slot = start + k
        new = "MAPSEC_" + suffix
        upstream = KANTO_TAIL_UPSTREAM[k]
        if secs[slot]["id"] not in (upstream, new):
            raise SystemExit(f"tail slot {slot} is {secs[slot]['id']}, expected {upstream}")
        kanto_aliases.append((upstream, new))
        secs[slot] = {"id": new, "name": display, **positions.get(new, {})}

    if "--list" in sys.argv:
        for i, s in enumerate(secs):
            if i < 86 or start <= i < start + len(tail_names):
                print(i, s["id"], s.get("name", ""))
        return

    JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    # each Hoenn alias points at whatever its slot holds now
    lines = HOENN.read_text().split("\n")
    for k, line in enumerate(lines):
        m = re.match(r"^#define (MAPSEC_\w+) (MAPSEC_\w+)$", line)
        if m and m.group(2) in slot_of:
            lines[k] = f"#define {m.group(1)} {new_at[slot_of[m.group(2)]]}"
    HOENN.write_text("\n".join(lines))

    first_tail = "MAPSEC_" + KANTO_TAIL[0][0]
    last_tail = "MAPSEC_" + KANTO_TAIL[-1][0]
    lines = [
        "// Ichor: the Oikoumene's map sections (design/oikoumene/BUILD.md, \"Sections\").",
        "// Generated by tools/ichor/oikoumene_sections.py; edit that script, not this file.",
        "// Most of the Oikoumene sits in the Hoenn block (ids 0-85, aliased in",
        "// region_map_sections_hoenn.h). The lands that don't fit use the Kanto block's",
        "// spare tail; these lines keep the FRLG names those slots replaced compiling.",
        "#ifndef GUARD_CONSTANTS_REGION_MAP_SECTIONS_OIKOUMENE_H",
        "#define GUARD_CONSTANTS_REGION_MAP_SECTIONS_OIKOUMENE_H",
        "",
        "// The two ranges GetRegionForSectionId reads as the Oikoumene chart.",
        "#define MAPSEC_OIKOUMENE_FIRST   0",
        "#define MAPSEC_OIKOUMENE_LAST    85",
        f"#define MAPSEC_OIKOUMENE2_FIRST  {first_tail}",
        f"#define MAPSEC_OIKOUMENE2_LAST   {last_tail}",
        "",
    ]
    for upstream, new in kanto_aliases:
        if upstream:
            lines.append(f"#define {upstream} {new}")
    lines += ["", "#endif // GUARD_CONSTANTS_REGION_MAP_SECTIONS_OIKOUMENE_H", ""]
    OIK_H.write_text("\n".join(lines))
    print(f"named {len(slots)} Hoenn slots and {len(tail_names)} Kanto-tail slots")


if __name__ == "__main__":
    main()
