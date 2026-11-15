-- The Route 1 / Elaia seam, seen from both sides, run by tools/ichor/tests/elaia_seam.sh.
--
-- The engine draws a connected map with the tilesets of the map the player stands
-- on, so from Route 1 (aethos + agros) Elaia's top rows must be aethos-only, and
-- from Elaia (aethos + kalliste) Route 1's bottom rows must be. This Quickstarts,
-- warps to Route 1's south edge and screenshots the seam at three points along
-- it, then crosses into Elaia and does the same looking north.
--
-- Env: SEAM_OUT, the screenshot folder; SEAM_SYMBOLS, the table elaia_symbols.sh wrote.
-- Prints "SEAM shot ..." per screenshot and ends with "SEAM done"; a failure
-- prints "SEAM FAIL: ..." first.

local S = dofile(os.getenv("SEAM_SYMBOLS") or "build/elaia_seam/symbols.lua")
local OUT = os.getenv("SEAM_OUT") or "build/elaia_seam/"
local K = { A = C.GBA_KEY.A, START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT,
            UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN, LEFT = C.GBA_KEY.LEFT, RIGHT = C.GBA_KEY.RIGHT }
local SCRATCH = 0x0203F000

local emu = setmetatable({}, { __index = function(_, name)
  return function(_, ...) return coroutine.yield("call", name, ...) end
end })
local function log(s) coroutine.yield("log", "SEAM " .. s) end
local function fail(s) error("SEAM FAIL: " .. s, 0) end
local function frame() coroutine.yield("frame") end
local function wait(n) for _ = 1, n do frame() end end

local function sb1() return emu:read32(S.gSaveBlock1Ptr) end
local function mapId()
  local loc = sb1() + S.OFF_SB1_LOCATION
  return emu:read8(loc) * 256 + emu:read8(loc + 1)
end
local function callback2() return emu:read32(S.gMain + S.OFF_MAIN_CALLBACK2) end
local function idle()
  return callback2() == (S.CB2_Overworld | 1) and emu:read8(S.sLockFieldControls) == 0
     and emu:read8(S.sGlobalScriptContextStatus) == 2
     and emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_TILE_TRANSITION) == 0
end
local function pos()
  local o = S.gObjectEvents + emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_OBJECT_EVENT_ID) * S.OBJECT_EVENT_SIZE
  local c = o + S.OFF_OBJ_CURRENT_COORDS
  return emu:read16(c) - S.MAP_OFFSET, emu:read16(c + 2) - S.MAP_OFFSET
end
local function tap(key, hold) emu:addKey(key); wait(hold or 4); emu:clearKey(key); wait(4) end
local function waitFor(cond, limit, what)
  for _ = 1, limit do
    if cond() then return end
    frame()
  end
  fail("timed out waiting for " .. what)
end
local function shot(name) emu:screenshot(OUT .. name); log("shot " .. name) end

local function bytes(t)
  local out = {}
  for _, v in ipairs(t) do
    if type(v) == "table" then
      for i = 0, v[2] - 1 do out[#out + 1] = (v[1] >> (8 * i)) & 0xFF end
    else
      out[#out + 1] = v
    end
  end
  return out
end
local function poke(addr, t)
  for i, b in ipairs(bytes(t)) do emu:write8(addr + i - 1, b) end
end
-- Warp to (x, y) on `map` from an ON_FRAME script written into spare EWRAM.
local function warpTo(map, x, y)
  local tableAddr, frameTable, code = SCRATCH, SCRATCH + 0x20, SCRATCH + 0x40
  poke(code, { S.SCR_OP_SETVAR, { S.VAR_TEMP_0, 2 }, { 1, 2 },
               S.SCR_OP_WARP, map >> 8, map & 0xFF, 0xFF, { x, 2 }, { y, 2 }, S.SCR_OP_WAITSTATE, S.SCR_OP_END })
  poke(frameTable, { { S.VAR_TEMP_0, 2 }, { 0, 2 }, { code, 4 }, { 0, 2 } })
  poke(tableAddr, { S.MAP_SCRIPT_ON_FRAME_TABLE, { frameTable, 4 }, 0 })
  emu:write32(S.gMapHeader + S.OFF_MAPHEADER_MAPSCRIPTS, tableAddr)
  waitFor(function() return mapId() == map and idle() end, 2000, "the warp")
  wait(40)
end

-- Walk straight along a row or column to (x, y): the seam's road and verges are open.
local function walkTo(x, y)
  for _ = 1, 60 do
    local px, py = pos()
    if px == x and py == y then return end
    local key = px < x and K.RIGHT or px > x and K.LEFT or py < y and K.DOWN or K.UP
    emu:addKey(key)                            -- hold only until the step starts
    waitFor(function() local qx, qy = pos(); return qx ~= px or qy ~= py end, 60, "a step")
    emu:clearKey(key)
    waitFor(idle, 300, "control while walking")
  end
  fail(string.format("never reached (%d,%d)", x, y))
end
local function face(key) tap(key, 2); wait(20) end

local function main()
  wait(500); tap(K.START)
  wait(500); tap(K.SELECT)                     -- Quickstart
  waitFor(idle, 3000, "the new game")
  wait(30)
  -- From Route 1's south edge, looking south into Elaia.
  warpTo(S.MAP_ROUTE1, 11, 62)
  face(K.DOWN); shot("01_route1_road.png")
  walkTo(11, 63); face(K.DOWN); shot("02_route1_road_edge.png")
  -- Along the edge the road is the only open ground, so warp to the verges' views.
  warpTo(S.MAP_ROUTE1, 11, 63); walkTo(13, 63); face(K.DOWN); shot("03_route1_road_east.png")
  warpTo(S.MAP_ROUTE1, 10, 63); face(K.DOWN); shot("04_route1_road_west.png")
  -- Into Elaia, looking north into Route 1.
  emu:addKey(K.DOWN)                           -- one step south crosses the seam
  waitFor(function() return mapId() == S.MAP_ELAIA end, 120, "Elaia")
  emu:clearKey(K.DOWN)
  waitFor(idle, 300, "control in Elaia")
  wait(30)
  local x, y = pos()
  log(string.format("ok crossed into Elaia at (%d,%d)", x, y))
  -- (row 2 is the shepherd's gate, so stay on row 1)
  walkTo(10, 1); face(K.UP); shot("05_elaia_looking_north.png")
  walkTo(11, 1); face(K.UP); shot("06_elaia_looking_north_east.png")
end

local co = coroutine.create(main)
local realEmu = _G.emu
callbacks:add("frame", function()
  if not co then return end
  local result = table.pack(coroutine.resume(co))
  while true do
    if not result[1] then
      local err = tostring(result[2])
      console:log(err:find("^SEAM FAIL") and err or ("SEAM FAIL: " .. err))
      console:log("SEAM done")
      co = nil
      return
    end
    if coroutine.status(co) == "dead" then
      console:log("SEAM done")
      co = nil
      return
    end
    local kind = result[2]
    if kind == "frame" then return end
    if kind == "log" then
      console:log(result[3])
      result = table.pack(coroutine.resume(co))
    else
      local fn = realEmu[result[3]]
      result = table.pack(coroutine.resume(co, fn(realEmu, table.unpack(result, 4, result.n))))
    end
  end
end)
