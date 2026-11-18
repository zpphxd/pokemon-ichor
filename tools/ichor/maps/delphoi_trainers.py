#!/usr/bin/env python3
"""Splice Delphoi's trainer parties (delphoi_trainers.party, ids 425-444) into
src/data/trainers.party, between its own markers, replacing any earlier copy.
Rhea's partner party goes into src/data/battle_partners.party the same way.

  /usr/bin/python3 tools/ichor/maps/delphoi_trainers.py
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

PARTNER = """
/* Delphoi: Rhea beside you at the Omphalos (phase4 SCRIPT.md Part 3). She
 * never uses a move that hits her partner. */
=== PARTNER_ICHOR_RHEA_DELPHOI ===
Name: RHEA
Class: Titan Admin
Pic: Rhea Partner
Gender: Female
Music: Female
AI: Basic Trainer

Laolith
Level: 57
Ability: Iron Fist
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
- Stone Edge
- Hammer Arm
- Rock Slide
- Stealth Rock

Geogrip
Level: 57
Ability: Earth Eater
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
- High Horsepower
- Superpower
- Circle Throw
- Bulk Up

Plouteras
Level: 57
Ability: Thick Fat
IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe
- High Horsepower
- Wish
- Body Slam
- Helping Hand

/* End Delphoi partner. */
"""


def splice(path, text, start, end):
    t = path.read_text()
    t = re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\n?", "", t, flags=re.S)
    path.write_text(t.rstrip("\n") + "\n" + text)


def main():
    party = (HERE / "delphoi_trainers.party").read_text()
    splice(ROOT / "src/data/trainers.party", party,
           "\n/* Delphoi and Laurel 8 (ids 425-444;", "/* End Delphoi teams. */")
    splice(ROOT / "src/data/battle_partners.party", PARTNER,
           "\n/* Delphoi: Rhea beside you", "/* End Delphoi partner. */")


if __name__ == "__main__":
    main()
