"""Layout diagrams of three designed-but-unbuilt areas, drawn from the design docs.

    /usr/bin/python3 tools/ichor/art/plan_diagrams.py

Writes design/art/img/plan_labyrinth.png, plan_underworld.png and plan_atlantis.png.
They are plans (LABYRINTH.md §4, UNDERWORLD.md §3, POSTGAME.md §3.2), not game maps:
redraw them from real map renders once the areas are built.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "design/art/img"
W = 1080
SERIF = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SERIF_B = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
SANS = "/System/Library/Fonts/Avenir Next.ttc"


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


F_TITLE = font(SERIF_B, 64)
F_SUB = font(SANS, 30)
F_CARD = font(SERIF_B, 38)
F_BODY = font(SANS, 29)
F_SMALL = font(SANS, 25)
F_TAG = font(SANS, 24, index=5)  # Avenir Next Demi Bold


def text_w(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, s, f, width):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(d, t, f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def header(d, pal, title, sub, status):
    d.text((60, 56), title, font=F_TITLE, fill=pal["ink"])
    y = 140
    for line in wrap(d, sub, F_SUB, W - 120):
        d.text((60, y), line, font=F_SUB, fill=pal["muted"])
        y += 40
    tw = text_w(d, status, F_TAG)
    d.rounded_rectangle((60, y + 14, 60 + tw + 36, y + 60), 23, fill=pal["accent"])
    d.text((78, y + 24), status, font=F_TAG, fill=pal["on_accent"])
    return y + 100


def card(d, pal, x, y, w, title, lines, fill=None, edge=None, title_fill=None):
    body = []
    for s in lines:
        body += wrap(d, s, F_BODY, w - 48)
    heads = wrap(d, title, F_CARD, w - 48)
    h = 30 + 46 * len(heads) + len(body) * 38 + 24
    d.rounded_rectangle((x, y, x + w, y + h), 18, fill=fill or pal["card"], outline=edge or pal["edge"], width=3)
    for k, line in enumerate(heads):
        d.text((x + 24, y + 22 + 46 * k), line, font=F_CARD, fill=title_fill or pal["ink"])
    ty = y + 30 + 46 * len(heads)
    for s in body:
        d.text((x + 24, ty), s, font=F_BODY, fill=pal["body"])
        ty += 38
    return h


def arrow(d, pal, x, y0, y1, label=None):
    d.line((x, y0, x, y1 - 14), fill=pal["thread"], width=5)
    d.polygon([(x - 12, y1 - 16), (x + 12, y1 - 16), (x, y1)], fill=pal["thread"])
    if label:
        d.text((x + 20, (y0 + y1) / 2 - 16), label, font=F_SMALL, fill=pal["muted"])


def finish(img, d, pal, y, note, name):
    for line in wrap(d, note, F_SMALL, W - 120):
        d.text((60, y), line, font=F_SMALL, fill=pal["muted"])
        y += 34
    img = img.crop((0, 0, W, y + 50))
    OUT.mkdir(parents=True, exist_ok=True)
    img.save(OUT / name)
    print("wrote", OUT / name, img.size)


def labyrinth():
    pal = dict(bg="#1d1b1a", card="#2c2826", edge="#5a4a3e", ink="#f1e6d2", body="#d8cbb6", muted="#a8998a",
               accent="#b5352b", on_accent="#fbefe0", thread="#c23a2e", side="#3a2f22", side_edge="#c9a23a")
    img = Image.new("RGB", (W, 4200), pal["bg"])
    d = ImageDraw.Draw(img)
    y = header(d, pal, "The Labyrinth",
               "Under the ruined palace of Knossa, Act III. Seven rings, each smaller and deeper than the last; "
               "each tests one temple's lesson. Ariadne's red thread marks your way. About 2 hours.",
               "DESIGNED  ·  ART BEGUN: DAEDALUS'S WORKSHOP")
    rings = [
        ("The Grand Staircase", ["The palace's way down. Ariadne gives you her thread here."], None),
        ("Ring I · The Threshold", ["Hestia's lesson: carry the flame through the dark. 44×32."], None),
        ("Ring II · The Runner's Ring", ["Hermes's lesson: the race, sun and moon gates. First sight of Asterion. 56×40."], None),
        ("Ring III · The Mysteries", ["Demeter's lesson: pitch dark and webs. Douse your torch to follow Daedalus's glowing marks. 56×48."],
         ("Daedalus's workshop", ["Heal, save, the Pithos. Automata, the music box, the Master Ball, the Icarus Shaft. 24×18."])),
        ("Ring IV · The Masks", ["Dionysus's lesson, in the Titans' lamplit halls. 48×40."], None),
        ("Ring V · The Hunt", ["Artemis's lesson: four skylight pools in the dark. 56×48."],
         ("Minos's tomb", ["The Helm of Darkness. 16×12."])),
        ("Ring VI · The Forge", ["Hephaestus's lesson, firelit. Team Titan's headquarters. 48×48."],
         ("Archive, vault, Mistress's shrine", ["The forged prophecy; the vault; a heal before the heart."])),
        ("Ring VII · The Choros", ["Aphrodite's lesson: the crane dance on the dancing floor. Starlit. 32×32."], None),
        ("The Starry Chamber", ["The heart. A black pool of reflected stars, and the unmasking. 20×20."], None),
    ]
    indent = 0
    for i, (title, lines, side) in enumerate(rings):
        x = 60 + indent
        w = (W - 120 - indent) if not side else 560 - indent // 2
        heart = i == len(rings) - 1
        h = card(d, pal, x, y, w, title, lines,
                 fill="#1b2240" if heart else None, edge="#c9a23a" if heart else None)
        if side:
            sx = x + w + 30
            sh = card(d, pal, sx, y, W - 60 - sx, side[0], side[1], fill=pal["side"], edge=pal["side_edge"])
            d.line((x + w, y + 50, sx, y + 50), fill=pal["side_edge"], width=4)
            main_h, h = h, max(h, sh)
        else:
            main_h = h
        if i < len(rings) - 1:
            arrow(d, pal, x + 60, y + main_h, y + h + 54)
        y += h + 54
        indent += 26
    return finish(img, d, pal, y + 10,
                  "A plan from design/LABYRINTH.md §4, not a game map. The lit room is the only part drawn so far; "
                  "after the Labyrinth, the Endless Labyrinth rebuilds itself on every visit.", "plan_labyrinth.png")


def underworld():
    pal = dict(bg="#e9e6e1", card="#f7f5f2", edge="#9aa0a6", ink="#1f2329", body="#3c424a", muted="#6b717a",
               accent="#2d3440", on_accent="#f2efe9", thread="#55606e", side="#ece6d4", side_edge="#b59a4a")
    img = Image.new("RGB", (W, 5200), pal["bg"])
    d = ImageDraw.Draw(img)
    y = header(d, pal, "The Underworld",
               "The Katabasis, post-game. Down through a cave at Cape Tainaron with Thanira, the Fate who cuts the thread, "
               "as your guide. 27 maps, about 4 hours, Lv 60–80.",
               "DESIGNED  ·  NOT BUILT YET")
    steps = [
        ("The Mani Road and Cape Tainaron", ["South from Lakonia to the cave mouth and its bronze gate."], None),
        ("The Descent", ["Two dark cave floors. Hecate's Torch lights the way."], None),
        ("The Acheron and the Styx", ["Charon's landing, then his boat across the Styx. The Oath of the Styx is sworn here."],
         ("Riverside of the Oath", ["Only on an Oath run: say goodbye to your fallen."])),
        ("The Gate", ["Kerberos. Optional boss."], None),
        ("The Meadows of Asphodel", ["The hub: the shades, the Danaids' jar, Kleon's siblings."], None),
        ("The Crossroads of Judgment", ["Three roads and the three Judges."],
         ("Elysium and Elysium's Shore", ["Gold fields; across the water, the Isles of the Blessed. Opens at the end."])),
        ("The Plain of Lethe", ["Fog that forgets your path."], None),
        ("The Lake of Mnemosyne", ["The guards and the password."], None),
        ("The House of Hades", ["Hades and Persephone, Lv 78–80."], ("The Vault", ["After the story: Nekranax."])),
        ("The Bronze Gates and the Fall", ["Nine days falling."], None),
        ("Tartarus", ["Five cells, five Titans to free. Briareus at the inner gate."],
         ("The House of Night", ["Cresselia and Darkrai. Built for 1.0, by your choice."])),
        ("The Chasm", ["Giratina, upside down, as Tartaros itself. Lv 80."], None),
        ("The Ascent of Tainaron", ["You lead Persephone up the stair and spring follows you into the world."], None),
    ]
    for i, (title, lines, side) in enumerate(steps):
        x = 60
        w = W - 120 if not side else 560
        last = i == len(steps) - 1
        h = card(d, pal, x, y, w, title, lines, fill="#f4ecd2" if last else None, edge=pal["side_edge"] if last else None)
        if side:
            sx = x + w + 30
            sh = card(d, pal, sx, y, W - 60 - sx, side[0], side[1], fill=pal["side"], edge=pal["side_edge"])
            d.line((x + w, y + 50, sx, y + 50), fill=pal["side_edge"], width=4)
            main_h, h = h, max(h, sh)
        else:
            main_h = h
        if not last:
            arrow(d, pal, x + 60, y + main_h, y + h + 54)
        y += h + 54
    return finish(img, d, pal, y + 10,
                  "A plan from design/UNDERWORLD.md §3, not a game map. Nobody returns from the dead in Ichor: "
                  "the Orpheus moment is Persephone's return.", "plan_underworld.png")


def atlantis():
    pal = dict(bg="#0f2236", card="#16324d", edge="#2e5a80", ink="#eaf3f8", body="#c8dbe6", muted="#8fb1c6",
               accent="#c8743a", on_accent="#fff3e6", thread="#5fa8d3", side="#2a2418", side_edge="#c8743a")
    img = Image.new("RGB", (W, 4600), pal["bg"])
    d = ImageDraw.Draw(img)
    y = header(d, pal, "Atlantis",
               "Daphne's arc, post-game: the one myth she never believed. Plato's city of rings of land and sea, "
               "beyond the Pillars. About 12 maps, about 3 hours, Lv 65–80.",
               "DESIGNED  ·  NOT BUILT YET")
    # Plato's rings: concentric land (orichalcum) and water
    cx, cy, R = W // 2, y + 360, 340
    rings = [(R, "#1d4a72"), (R - 50, "#a8683a"), (R - 95, "#1d4a72"), (R - 140, "#b97a46"),
             (R - 185, "#1d4a72"), (R - 230, "#c98a52"), (R - 270, "#1d4a72")]
    for r, c in rings:
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c, outline="#0f2236", width=3)
    d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill="#d9a35a", outline="#fff1d6", width=4)
    d.text((cx, cy - 16), "Temple", font=F_BODY, fill="#2a1a0c", anchor="mm")
    d.text((cx, cy + 22), "of Poseidon", font=F_SMALL, fill="#2a1a0c", anchor="mm")
    for r, label in [(R - 25, "1  Outer ring"), (R - 118, "2  Middle ring"), (R - 208, "3  Inner ring")]:
        d.text((cx, cy - r), label, font=F_TAG, fill="#fff3e6", anchor="mm")
    y = cy + R + 50
    steps = [
        ("Beyond the Pillars", ["The largest sea map: open ocean, no islands. Aeolus's Bag parts the fog."]),
        ("The Nereids' circle", ["Thetis gives you the Nereid Pearl, to dive. Underwater you have 60 steps of breath; air pockets refill it."]),
        ("1  The outer ring", ["The harbor, full of orichalcum wrecks."]),
        ("2  The middle ring", ["Palaces and Plato's racecourse; the museum hall where your other fossil waits."]),
        ("3  The inner ring", ["The citadel and the kings' orichalcum pillar. The Telchines still work its forges."]),
        ("The temple", ["Pontanax, the sea colossus, behind a seal only the trident lot opens."]),
        ("The coral nursery", ["A single Manaphy egg."]),
        ("The abyss", ["Leukothea, the Odyssey's white bird, is Lugia. Lv 80."]),
        ("The edge of the world", ["The river Oceanus, running forever in a circle: Kyogre, the first Primordial. Lv 88."]),
    ]
    for i, (title, lines) in enumerate(steps):
        h = card(d, pal, 60, y, W - 120, title, lines)
        if i < len(steps) - 1:
            arrow(d, pal, 120, y + h, y + h + 46)
        y += h + 46
    return finish(img, d, pal, y + 10,
                  "A plan from design/POSTGAME.md §3.2, not a game map. Daphne, after: \"So Plato was remembering "
                  "something too.\"", "plan_atlantis.png")


if __name__ == "__main__":
    labyrinth()
    underworld()
    atlantis()
