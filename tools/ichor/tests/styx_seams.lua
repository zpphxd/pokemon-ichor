-- Styx Falls' two seams, Route 11 above and Route 12 below, crossed both ways.
--
--   mkdir -p build/styx_seams && build/tools/ichor-mgba-headless \
--       --script tools/ichor/tests/styx_seams.lua --frames 9000 --until "STYXSEAM done" pokeemerald.gba
--
-- Env: SEAM_OUT is the screenshot folder (default build/styx_seams/, which must exist).
-- A connected map draws with the tilesets of the map the player stands on, so the
-- strip seen across each seam must be Aethos only (tools/ichor/seam_audit.py). For
-- a person to look at, each crossing takes a shot two steps short of the border,
-- then mid-step and after each step across it and one beyond:
--   r11_down_*   Route 11's road (11,49) south into Styx Falls
--   styx_up_*    Styx Falls' road (12,2) north into Route 11
--   styx_down_*  Styx Falls' south road (30,27) down into Route 12
--   r12_up_*     Route 12's trail (6,2) north into Styx Falls
-- Passes when each walk ends on the map across its seam.

local L = dofile("tools/ichor/tests/ichor_lib.lua")
local K = L.K
local OUT = os.getenv("SEAM_OUT") or "build/styx_seams/"

local G11, R11 = L.map("MAP_ROUTE11_DRUM_PASS")
local GS, STYX = L.map("MAP_STYX_FALLS")
local G12, R12 = L.map("MAP_ROUTE12_CYPRESS_ROAD")

local function on(group, num, what)
  return { wait = 30, check = function()
    local sb = L.sb1()
    local g, n = emu:read8(sb + 4), emu:read8(sb + 5)
    return g == group and n == num, string.format("%s ended on map %d.%d", what, g, n)
  end }
end

local function crossing(name, group, num, x, y, key, toGroup, toNum)
  local s = { { warp = { group, num, -1, x, y }, wait = 240 },
              { shot = name .. "_0_start.png", wait = 2 } }
  for k = 1, 4 do                        -- two steps to the border, one across, one beyond
    table.insert(s, { hold = key, frames = 16, wait = 8 })
    table.insert(s, { shot = string.format("%s_%d_mid.png", name, k), wait = 8 })
    table.insert(s, { shot = string.format("%s_%d.png", name, k) })
  end
  table.insert(s, on(toGroup, toNum, name))
  return s
end

local steps = L.seq(
  L.quickstart(),
  crossing("r11_down", G11, R11, 11, 49, K.DOWN, GS, STYX),
  crossing("styx_up", GS, STYX, 12, 2, K.UP, G11, R11),
  crossing("styx_down", GS, STYX, 30, 27, K.DOWN, G12, R12),
  crossing("r12_up", G12, R12, 6, 2, K.UP, GS, STYX)
)

L.run("STYXSEAM", OUT, steps)
