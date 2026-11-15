-- The Akti / Route 1 seam, seen from Route 1's side.
--
--   mkdir -p build/akti_seam && build/tools/ichor-mgba-headless \
--       --script tools/ichor/tests/akti_seam.lua --frames 4000 --until "SEAM done" pokeemerald.gba
--
-- Env: SEAM_OUT is the screenshot folder (default build/akti_seam/, which must exist).
-- The engine draws a connected map with the tilesets of the map the player stands
-- on, so from Route 1 (aethos + agros) Akti's bottom rows must use only aethos
-- metatiles (MAP_DESIGN.md §5; akti.py checks it). This walks the seam from Route
-- 1's side, then north across it, with screenshots, for a person to look at:
--   1. three spots on Route 1 just below the seam, west, middle and east;
--   2. the walk north up the road into Akti, screenshots mid-step and after each step.
-- Passes when the walk ends in Akti.

local L = dofile("tools/ichor/tests/ichor_lib.lua")
local K = L.K
local OUT = os.getenv("SEAM_OUT") or "build/akti_seam/"

local TOWNS, MAP_ROUTE1 = L.map("MAP_KALLISTE_ROUTE1")
local _, MAP_AKTI = L.map("MAP_AKTI_TOWN")

local function spot(name, x, y)
  return { { warp = { TOWNS, MAP_ROUTE1, -1, x, y }, wait = 240 },
           { shot = "route1_" .. name .. ".png", wait = 2 } }
end

-- north up the road from (12,3): a step is 16 frames; a screenshot mid-step and
-- at the end of each, six steps in all (the fourth crosses into Akti)
local walk = {}
for k = 0, 5 do
  table.insert(walk, { hold = K.UP, frames = 16, wait = 8 })
  table.insert(walk, { shot = string.format("walk_%02d_mid.png", k), wait = 8 })
  table.insert(walk, { shot = string.format("walk_%02d.png", k) })
end

local steps = L.seq(
  L.quickstart(),
  spot("west", 7, 2), spot("middle", 12, 0), spot("east", 17, 2), spot("road", 12, 3),
  walk,
  { { wait = 60 },
    { check = function()
        local sb = L.sb1()                   -- SaveBlock1.location: group, then number
        local g, n = emu:read8(sb + 4), emu:read8(sb + 5)
        return g == TOWNS and n == MAP_AKTI,
               string.format("the walk north ended on map %d.%d, not Akti", g, n)
      end } }
)

L.run("SEAM", OUT, steps)
