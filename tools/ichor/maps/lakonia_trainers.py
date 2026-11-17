#!/usr/bin/env python3
"""Put Lakonia's trainers (ids 410-424) into src/data/trainers.party.

The parties are lakonia_trainers.party (SCRIPT.md Part 3) plus Kleon's three
clean-battle teams, which share five Pokémon and differ in his starter's
final stage (the one that beats the player's). Rerunning replaces the block.

    python3 tools/ichor/maps/lakonia_trainers.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BEGIN, END = "/* Ichor: Lakonia begin */\n", "/* Ichor: Lakonia end */\n"
IV24 = "IVs: 24 HP / 24 Atk / 24 Def / 24 SpA / 24 SpD / 24 Spe"
IV31 = "IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe"
FIVE = [("Hoplomex", 53, ["Close Combat", "X-Scissor", "Crunch", "Bulk Up"]),
        ("Nemeleon", 53, ["Double-Edge", "Crunch", "Bulk Up", "Crush Claw"]),
        ("Dorydrake", 54, ["Dragon Dance", "Dragon Rush", "Brick Break", "Crunch"]),
        ("Hoplektor", 54, ["Brave Bird", "Close Combat", "Drill Peck", "Bulk Up"]),
        ("Kourodin", 54, ["Sacred Sword", "Heavy Slam", "Teeter Dance", "Swords Dance"])]
ACES = {"NEBREL": ("Pylakyon", "Charcoal", ["Phantom Force", "Temper Flare", "Crunch", "Will-O-Wisp"]),
        "KYNDER": ("Seismare", "Mystic Water", ["Wave Crash", "Earthquake", "Liquidation", "Agility"]),
        "HIPLING": ("Daphnyad", "Miracle Seed", ["Petal Blizzard", "Dazzling Gleam", "Energy Ball", "Synthesis"])}


def mon(species, level, ivs, moves, item=None):
    head = species + (f" @ {item}" if item else "")
    return f"{head}\nLevel: {level}\n{ivs}\n" + "".join(f"- {m}\n" for m in moves) + "\n"


def kleon():
    out = []
    for key, (sp, item, moves) in ACES.items():
        out.append(f"=== TRAINER_ICHOR_KLEON_LAKONIA_{key} ===\nName: KLEON\nClass: Lakonian\nPic: Kleon\n"
                   "Gender: Male\nMusic: Rival\nItems: Full Restore / Full Restore\n"
                   "AI: Basic Trainer / Check Bad Move\n\n")
        out += [mon(s, lv, IV24, mv) for (s, lv, mv) in FIVE]
        out.append(mon(sp, 55, IV31, moves, item))
    return "".join(out)


def main():
    body = BEGIN + (HERE / "lakonia_trainers.party").read_text() + "\n" + kleon() + END
    p = ROOT / "src/data/trainers.party"
    t = p.read_text()
    if BEGIN in t:
        t = t[:t.index(BEGIN)] + body + t[t.index(END) + len(END):]
    else:
        anchor = "/* Ichor: world-act3 (ids 320-499) */\n"
        t = t.replace(anchor, anchor + "\n" + body, 1)
    p.write_text(t)
    print("trainers.party: Lakonia's block written")


if __name__ == "__main__":
    main()
