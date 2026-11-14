#!/usr/bin/env python3
"""Show Ichor's battle backgrounds in the real ROM, headlessly.

For each environment this boots pokeemerald.gba in the Lua-capable runner
(build/tools/ichor-mgba-headless, built by tools/ichor/smoke_test.sh), takes
Quickstart to the player's room, opens the expansion's debug menu (hold R,
press START) and picks Party > Start Debug Battle. While the battle loads, the
script keeps writing the environment id to gBattleEnvironment (its address
comes from pokeemerald.map); debug battles never recompute it, so the battle
draws that environment, its entry overlay and its intro slide. Screenshots of
the slide, the trainers on the platforms and the battlers on the platforms go
to build/battle_bg/<env>/.

Then it lays the key frames side by side at 3x into
design/phase1/img/battle_bg_<env>.png.

Usage: python3 tools/ichor/art/battle_bg_check.py [env ...]
       envs: grass plain sand water building gym leader (default: all)
Run `make` and tools/ichor/smoke_test.sh first.
"""
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
RUNNER = ROOT / "build/tools/ichor-mgba-headless"
ROM = ROOT / "pokeemerald.gba"
IMG = ROOT / "design/phase1/img"

# BATTLE_ENVIRONMENT_* values (include/constants/battle.h).
ENVS = {
    "grass": 0,      # BATTLE_ENVIRONMENT_GRASS
    "sand": 2,       # BATTLE_ENVIRONMENT_SAND
    "water": 4,      # BATTLE_ENVIRONMENT_WATER
    "building": 8,   # BATTLE_ENVIRONMENT_BUILDING
    "plain": 9,      # BATTLE_ENVIRONMENT_PLAIN
    "gym": 11,       # BATTLE_ENVIRONMENT_GYM
    "leader": 12,    # BATTLE_ENVIRONMENT_LEADER
}

# Frames (stable for a given ROM; re-probe if the opening changes).
F_DEBUG = 2600       # hold R, press START: debug menu
F_BATTLE = 2980      # A on "Start Debug Battle"
SHOTS = {            # offset from F_BATTLE -> name
    205: "1_entry",      # the entry overlay sweeping in
    222: "2_slide",      # the scene sliding in: both halves of the strip
    240: "3_slide",
    300: "4_trainers",   # trainers on the platforms
    1000: "5_battlers",  # both Pokemon out
    1100: "6_menu",      # with the HP boxes and the action menu
}
PRESS_A = (420, 620, 820, 1020)  # advance the intro messages

LUA = r"""
local K = C.GBA_KEY
local OUT = "%(out)s"
local ENV_ADDR = %(addr)d
local ENV = %(env)d
local schedule = {
  [500]  = { press = {K.START} },            -- skip the intro
  [1020] = { press = {K.SELECT} },           -- Quickstart
  [%(dbg)d] = { press = {K.R}, hold = 24 },  -- hold R...
  [%(dbg)d + 8] = { press = {K.START} },     -- ...and press START: debug menu
  [%(dbg)d + 60] = { press = {K.DOWN} },
  [%(dbg)d + 80] = { press = {K.DOWN} },     -- Party...
  [%(dbg)d + 50] = { shot = "0_debug_menu" },
  [%(dbg)d + 100] = { press = {K.A} },
%(downs)s
  [%(bat)d - 10] = { shot = "0_party_menu" },
  [%(bat)d] = { press = {K.A}, poke = true },  -- Start Debug Battle
%(shots)s
  [%(done)d] = { done = true },
}
local release, poking = {}, false
callbacks:add("frame", function()
  local f = emu:currentFrame()
  for k, at in pairs(release) do
    if f >= at then emu:clearKey(k); release[k] = nil end
  end
  if poking and f < %(bat)d + 400 then emu:write8(ENV_ADDR, ENV) end
  local s = schedule[f]
  if not s then return end
  if s.press then
    for _, k in ipairs(s.press) do emu:addKey(k); release[k] = f + (s.hold or 6) end
  end
  if s.poke then poking = true end
  if s.shot then emu:screenshot(OUT .. s.shot .. ".png"); console:log("BG shot " .. s.shot .. " at " .. f) end
  if s.done then console:log("BG done at " .. f) end
end)
"""


def symbol(name):
    for line in (ROOT / "pokeemerald.map").read_text().splitlines():
        p = line.split()
        if len(p) == 2 and p[1] == name and p[0].startswith("0x"):
            return int(p[0], 16)
    raise SystemExit(f"{name} not in pokeemerald.map")


def capture(env):
    out = ROOT / "build/battle_bg" / env
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("*.png"):
        f.unlink()
    downs = "\n".join(f"  [{F_DEBUG + 130 + 20 * i}] = {{ press = {{K.DOWN}} }},"
                      for i in range(10))           # to "Start Debug Battle"
    shots = "\n".join(f'  [{F_BATTLE + o}] = {{ shot = "{n}" }},' for o, n in SHOTS.items())
    shots += "\n" + "\n".join(f"  [{F_BATTLE + o}] = {{ press = {{K.A}} }}," for o in PRESS_A)
    lua = LUA % dict(out=str(out) + "/", addr=symbol("gBattleEnvironment"), env=ENVS[env],
                     dbg=F_DEBUG, bat=F_BATTLE, downs=downs, shots=shots,
                     done=F_BATTLE + max(SHOTS) + 10)
    script = out / "check.lua"
    script.write_text(lua)
    timeout = "gtimeout" if subprocess.run(["which", "gtimeout"], capture_output=True).returncode == 0 else "timeout"
    r = subprocess.run([timeout, "180", str(RUNNER), "--script", str(script), "--frames", "6000",
                        "--until", "BG done", str(ROM)], cwd=ROOT, capture_output=True, text=True)
    (out / "mgba.log").write_text(r.stdout + r.stderr)
    if "BG done" not in r.stdout + r.stderr:
        raise SystemExit(f"{env}: run did not finish, see {out / 'mgba.log'}")
    print(f"{env}: {len(list(out.glob('*.png')))} screenshots in {out.relative_to(ROOT)}")
    return out


def sheet(env, out, frames=("2_slide", "4_trainers", "6_menu"), scale=3):
    ims = [Image.open(out / f"{f}.png").convert("RGB") for f in frames]
    pad = 6 * scale
    w = sum(im.width * scale for im in ims) + pad * (len(ims) + 1)
    h = ims[0].height * scale + pad * 2
    sh = Image.new("RGB", (w, h), (32, 24, 24))
    x = pad
    for im in ims:
        sh.paste(im.resize((im.width * scale, im.height * scale), Image.NEAREST), (x, pad))
        x += im.width * scale + pad
    path = IMG / f"battle_bg_{env}_ingame.png"
    sh.save(path)
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    envs = sys.argv[1:] or list(ENVS)
    for e in envs:
        o = capture(e)
        sheet(e, o)
