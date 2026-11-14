#!/usr/bin/env python3
"""Decode and check every field message a slice run saw.

The playthrough logs each message as it appears (gStringVar4, after the game
expanded {PLAYER} and the like, so this is exactly what was on screen):

  SLICE TEXT <mapId> <x>,<y> <hex bytes in the game's charset>

This prints each one decoded, then flags:
  WIDE   a line wider than the field message box (216 px in the normal font)
  TALL   a page with more than two lines before a \\p (the box shows two)
  HOENN  a Hoenn-era word left in the text
  WORD?  words not in the system dictionary or Ichor's own names, for a typo read

  tools/ichor/tests/slice_text_report.py build/slice/run.log > build/slice/text.txt
"""
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "ichor"))
import text_width  # noqa: E402

MAX_WIDTH = 216
HOENN = [r"\bHOENN\b", r"\bHoenn\b", r"\bBIRCH\b", r"\bBirch\b", r"LITTLEROOT", r"Littleroot", r"OLDALE",
         r"Oldale", r"PETALBURG", r"Petalburg", r"RUSTBORO", r"Rustboro", r"BRENDAN", r"Brendan", r"\bWALLY\b",
         r"\bWally\b", r"POKéMON CENTER", r"Pokémon Center", r"POKé MART", r"Poké Mart", r"\bGYM\b",
         r"\bGym\b", r"\bBADGE", r"\bBadge", r"\bPC\b", r"\bPROF\. BIRCH", r"Team Aqua", r"Team Magma",
         r"\bAQUA\b", r"\bMAGMA\b", r"\bROUTE 10\d", r"Route 10\d", r"POKéNAV", r"PokéNav", r"\bLEADER\b",
         r"Gym Leader", r"\bChampion\b", r"\bCHAMPION\b", r"Elite Four", r"ELITE FOUR"]
# Ichor's own words (names, places, Greek terms) that no English dictionary has.
ICHOR_WORDS = """
aethos akademia akti alethea amaryllis amathos aithra agis agora apollo asclepeion asclepius athena augur
augurs augury daphne delphoi demeas diktys elaia eleusa emporion euboulos euploia glaukos gylippos halia harpe
hestia hierophant hyperion hydna ianthe ione kalliste kanthos kerykos kibotos klepsydra kleon klotheia
kline komatas korinna kronion kronos krater kraters kydippe lakonia lakonian lakonians lampon melitta nausikles
oikos olympus pithos philon phyllis polyeidos petros pyrrha pythia talaria theo titanborn tityros typhon
zeus aeolus mudbray wooloo smoliv snivy cyndaquil piplup chansey skiddo combee mareep pidove nincada ekans
tandemaus ponyta hoothoot spinarak murkrow cleffa nickit roggenrola baltoy timburr diglett rockruff bronzor
growlithe geodude drilbur nosepass silicobra machop minccino fletchling lillipup munchlax litleo magikarp
horsea krabby finizen corsola wailmer pokédex pokémon poké moomoo hrrrnk baaa baa chaaan whumpf kalliste's
herm herms halcyon facade tm42 ichor mom hearthkeeper woodsmoke seabed mainland sitrus stardust louder safer
ooh hm kingfishers healers has
""".split()


def load_dictionary():
    words = set(w.lower() for w in ICHOR_WORDS)
    try:
        with open("/usr/share/dict/words", encoding="utf-8") as f:
            words.update(w.strip().lower() for w in f)
    except OSError:
        pass
    return words


def decoder():
    chars, codes = text_width.load_charmap()
    byte_char = {}
    for ch, bs in chars.items():
        if len(bs) == 1:
            byte_char.setdefault(int(bs[0], 16), ch)
    widths = text_width.load_widths(text_width.FONTS["normal"])
    # arguments after FC <code> (src/string_util.c, StringExpandPlaceholders)
    no_args = {0x07, 0x09, 0x0F, 0x15, 0x16, 0x17, 0x18}
    three = {0x04, 0x1C}

    def decode(data):
        """Return (text, [(line, width, page, line_no)])."""
        out, lines, cur, w, page, line_no = [], [], [], 0, 0, 0
        i = 0
        while i < len(data):
            b = data[i]
            if b in (0xFE, 0xFA, 0xFB):
                lines.append(("".join(cur), w, page, line_no))
                cur, w = [], 0
                if b == 0xFB:
                    page, line_no = page + 1, 0
                    out.append("\\p")
                elif b == 0xFA:
                    line_no += 1
                    out.append("\\l")
                else:
                    line_no += 1
                    out.append("\\n")
                i += 1
            elif b == 0xFC:
                code = data[i + 1] if i + 1 < len(data) else 0
                n = 0 if code in no_args else 3 if code in three else 2 if code == 0x0B else 1
                i += 2 + n
            elif b in (0xF8, 0xF9):
                w += text_width.ICON_WIDTH.get("%02X" % b, 10)
                cur.append("{%02X %02X}" % (b, data[i + 1] if i + 1 < len(data) else 0))
                i += 2
            elif b == 0xFD:
                cur.append("{?}")
                i += 2
            else:
                ch = byte_char.get(b, "{%02X}" % b)
                cur.append(ch)
                out.append(ch)
                w += widths[b] if b < len(widths) else 0
                i += 1
        lines.append(("".join(cur), w, page, line_no))
        return "".join(out), lines

    return decode


def main():
    log = sys.argv[1] if len(sys.argv) > 1 else "build/slice/run.log"
    decode = decoder()
    words = load_dictionary()
    seen, wide, tall, hoenn, unknown = set(), 0, 0, 0, {}
    pat = re.compile(r" TEXT (\d+) (-?\d+,-?\d+) ([0-9A-F]+)")
    with open(log, encoding="utf-8", errors="replace") as f:
        for raw in f:
            m = pat.search(raw)
            if not m:
                continue
            mapid, where, hexs = m.groups()
            data = bytes.fromhex(hexs)
            if data in seen:
                continue
            seen.add(data)
            text, lines = decode(data)
            group, num = int(mapid) >> 8, int(mapid) & 0xFF
            print(f"[map {group}.{num} at {where}] {text}")
            for line, w, _, _ in lines:
                if w > MAX_WIDTH:
                    wide += 1
                    print(f"WIDE {w}px > {MAX_WIDTH}: {line}")
            # \l scrolls the box up a line, so only \n stacks a third line in a page
            for n, page in enumerate(text.split("\\p"), 1):
                stacked = page.count("\\n") + 1
                if stacked > 2:
                    tall += 1
                    print(f"TALL page {n} has {stacked} lines: {page}")
            for h in HOENN:
                if re.search(h, text):
                    hoenn += 1
                    print(f"HOENN {h}: {text}")
            plain = re.sub(r"\\[nlp]", " ", text).replace("’", "'")
            for word in re.findall(r"[A-Za-zéÉ']+", plain):
                wl = word.lower().strip("'")
                for tail in ("'s", "n't", "'ll", "'re", "'ve", "'d", "'m"):
                    if wl.endswith(tail):
                        wl = wl[:-len(tail)]
                stems = {wl, wl[:-1], wl[:-2], wl[:-3], wl[:-3] + "y", wl[:-2] + "e", wl[:-3] + "e", wl[:-4]}
                if len(wl) < 3 or any(s in words for s in stems if len(s) > 2):
                    continue
                unknown.setdefault(wl, plain[:60])
    for wl in sorted(unknown):
        print(f"WORD? {wl}  ({unknown[wl]}...)")
    print(f"SUMMARY {len(seen)} messages, {wide} wide lines, {tall} tall pages, {hoenn} Hoenn words, "
          f"{len(unknown)} words to read")


if __name__ == "__main__":
    main()
