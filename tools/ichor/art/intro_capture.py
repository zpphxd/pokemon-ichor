"""Capture Ichor's boot sequence from the built ROM, headlessly.

Used by intro_screen.py --capture, or on its own:
  python3 tools/ichor/art/intro_capture.py           # contact sheets + stills
  python3 tools/ichor/art/intro_capture.py --skip    # check skipping mid-sequence

It boots pokeemerald.gba in build/tools/ichor-mgba-headless (built by
tools/ichor/smoke_test.sh), screenshots every 30 frames from power-on until
the title is up, plus each scene's key frame by the intro's own clock
(gIntroFrameCounter, read from RAM), and writes:
  design/phase1/img/intro_sheet_*.png   contact sheets, a frame per 30
  design/phase1/img/intro_keys.png      the key frames, labeled
  design/phase1/img/intro_<n>_*.png     stills of the key frames
"""
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
RUNNER = ROOT / "build/tools/ichor-mgba-headless"
OUT = ROOT / "build/intro_capture"
IMG = ROOT / "design/phase1/img"
W, H = 240, 160

# Key frames on the intro's clock (frames since the studio card began), named
# for the stills. INTRO.md's timing sheet lists the same moments.
KEYS = [
    (40, "3_studio_bead"),
    (100, "4_studio_fall"),
    (200, "5_studio_mark"),
    (560, "6_clotho"),
    (1060, "7_grove"),
    (1360, "8_sea"),
    (1640, "9_temple"),
    (1898, "10_olympus"),
    (2100, "11_measure"),
    (2210, "12_cut"),
    (2290, "13_hesitate"),
]
BOOT_STILLS = {"1_copyright": 90, "2_powered_by": 330}
SHEET_STEP = 30
LAST_FRAME = 3420        # the amphora title is up by then


def map_address(symbol):
    text = (ROOT / "pokeemerald.map").read_text(errors="replace")
    m = re.search(r"^\s+(0x[0-9a-f]+)\s+" + re.escape(symbol) + r"\s*$", text, re.M)
    assert m, f"{symbol} not in pokeemerald.map"
    return int(m.group(1), 16)


LUA = """-- Written by tools/ichor/art/intro_capture.py
local COUNTER = %(counter)d
local OUT = "%(out)s"
local KEYS = {%(keys)s}
local PRESS = {%(press)s}
local LAST = %(last)d
local STEP = %(step)d
local K = C.GBA_KEY
local want, taken, held, releaseAt = {}, {}, nil, 0
for _, t in ipairs(KEYS) do want[t] = true end
local started = false
callbacks:add("frame", function()
  local f = emu:currentFrame()
  if held and f >= releaseAt then emu:clearKey(held); held = nil end
  local t = emu:read32(COUNTER)
  if t > 0 then started = true end
  if PRESS[f] then emu:addKey(K.START); held = K.START; releaseAt = f + 6
    console:log(string.format("press at boot %%d, intro t %%d", f, t)) end
  if f %% STEP == 0 then emu:screenshot(string.format("%%s/boot_%%05d.png", OUT, f)) end
  if started and want[t] and not taken[t] then
    taken[t] = true
    emu:screenshot(string.format("%%s/key_%%05d.png", OUT, t))
    console:log(string.format("key %%d at boot %%d", t, f))
  end
  if f == LAST then console:log("INTRO done") end
end)
"""


def run_lua(press=(), last=LAST_FRAME, keys=None):
    assert RUNNER.exists(), "run tools/ichor/smoke_test.sh once to build the headless runner"
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.png"):
        old.unlink()
    keys = [k for k, _ in KEYS] if keys is None else keys
    lua = OUT / "capture.lua"
    lua.write_text(LUA % {
        "counter": map_address("gIntroFrameCounter"), "out": OUT,
        "keys": ", ".join(map(str, keys)),
        "press": ", ".join(f"[{f}] = true" for f in press),
        "last": last, "step": SHEET_STEP})
    res = subprocess.run([str(RUNNER), "--script", str(lua), "--frames", str(last + 20), "--until", "INTRO done",
                          str(ROOT / "pokeemerald.gba")], capture_output=True, text=True, cwd=ROOT, check=True)
    return [line for line in res.stdout.splitlines() if "[Scripting]" in line]


def contact(paths, path, cols=6, labels=None):
    rows = (len(paths) + cols - 1) // cols
    lab = 11 if labels else 0
    sheet = Image.new("RGB", (cols * (W + 4) + 4, rows * (H + lab + 4) + 4), (24, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, p in enumerate(paths):
        x = 4 + (i % cols) * (W + 4)
        y = 4 + (i // cols) * (H + lab + 4)
        sheet.paste(Image.open(p).convert("RGB"), (x, y + lab))
        if labels:
            d.text((x + 1, y - 1), labels[i], fill=(232, 216, 176))
    sheet.save(path)


def capture():
    log = run_lua()
    starts = []
    for line in log:
        m = re.search(r"key (\d+) at boot (\d+)", line)
        if m:
            starts.append(int(m.group(2)) - int(m.group(1)))
    start = min(starts) if starts else 0
    boots = sorted(OUT.glob("boot_*.png"))
    # contact sheets: the cards, the studio, the frieze, the loom and the title
    def frames_between(a, b):
        return [p for p in boots if a <= int(p.stem[5:]) < b]
    sections = [
        ("cards", 0, start),
        ("studio", start, start + 410),
        ("frieze", start + 410, start + 2048),
        ("loom", start + 2048, LAST_FRAME + 1),
    ]
    for name, a, b in sections:
        ps = frames_between(a, b)
        labels = [f"boot {int(p.stem[5:])}" + (f" / t {int(p.stem[5:]) - start}" if int(p.stem[5:]) >= start else "")
                  for p in ps]
        contact(ps, IMG / f"intro_sheet_{name}.png", cols=6, labels=labels)
    keys = sorted(OUT.glob("key_*.png"))
    names = dict(KEYS)
    contact(keys, IMG / "intro_keys.png", cols=4, labels=[f"t {int(p.stem[4:])}: {names[int(p.stem[4:])]}" for p in keys])
    for p in keys:
        Image.open(p).save(IMG / f"intro_{names[int(p.stem[4:])]}.png")
    for name, f in BOOT_STILLS.items():
        src = OUT / f"boot_{f:05d}.png"
        if src.exists():
            Image.open(src).save(IMG / f"intro_{name}.png")
    title = OUT / f"boot_{LAST_FRAME - LAST_FRAME % SHEET_STEP:05d}.png"
    Image.open(title).save(IMG / "intro_14_title.png")
    print(f"studio card starts at boot frame {start}; sheets and stills in {IMG}")
    return start


def skip_check():
    """Press START at several points and screenshot 300 frames later: in the
    powered-by card (which, as upstream's, skips to the studio card), the
    studio card, the frieze and the loom (which skip to the title)."""
    results = []
    for press in (300, 520, 1700, 2560):
        log = run_lua(press=(press,), last=press + 300, keys=[])
        f = press + 300
        shot = ROOT / f"build/intro_skip_{press}.png"
        Image.open(OUT / f"boot_{f - f % SHEET_STEP:05d}.png").save(shot)
        results.append((press, [l for l in log if "press" in l], shot))
    contact([r[2] for r in results], IMG / "intro_skip.png", cols=4,
            labels=[f"START at boot {p}, shot 300 frames later" for p, _, _ in results])
    return results


if __name__ == "__main__":
    if "--skip" in sys.argv:
        for press, log, shot in skip_check():
            print(press, log, shot)
    else:
        capture()
