-- Route 1 and Kronion Hill check, run by tools/ichor/tests/route1.sh (read it first).
--
-- Setup touches no ROM data. After Quickstart the test copies route1_setup.s's
-- assembled blob into spare EWRAM and points the current map header's script
-- table at one of its ON_FRAME headers; the game runs it on the next frame. The
-- first one gives a starter and the flags Elaia leaves set after beat 4, then
-- warps to Route 1. The others warp to (VAR_0x8008, VAR_0x8009) on either map.
-- Options are set to fast text, Set battle style and no battle animations.
--
-- Then, as a player: walk north into Tityros's sight and win the battle; tour
-- the route with a screenshot per stop; check the flock blocks the road; climb
-- Kronion Hill into the summit scene and play it out (two grunt battles, the
-- tablet, the Augur's Eye); check the story flags; and check the road is open.
--
-- Prints "ROUTE1 ok ..." per check and "ROUTE1 shot ..." per screenshot, and
-- ends with "ROUTE1 done"; any failure prints "ROUTE1 FAIL: ..." first.
-- SPRITE_REVIEW=1 also captures the trainer/send-out sequence every 60 frames.

local S = dofile("build/test_route1/symbols.lua")
local OUT = os.getenv("ROUTE1_OUT") or "build/test_route1/"
local BLOB_ADDR = tonumber(os.getenv("ROUTE1_BLOB_ADDR") or "0x0203F000")
local K = { A = C.GBA_KEY.A, B = C.GBA_KEY.B, START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT,
            UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN, LEFT = C.GBA_KEY.LEFT, RIGHT = C.GBA_KEY.RIGHT }

-- The test reads as straight-line code in a coroutine. mGBA only lets its own
-- functions run on the main Lua thread, so the coroutine asks the frame callback
-- to make each call (yield "call") and to advance a frame (yield "frame").
local emu = setmetatable({}, { __index = function(_, name)
  return function(_, ...) return coroutine.yield("call", name, ...) end
end })
local function log(s) coroutine.yield("log", "ROUTE1 " .. s) end
local function fail(s) error("ROUTE1 FAIL: " .. s, 0) end
local function frame() coroutine.yield("frame") end
local function wait(n) for _ = 1, n do frame() end end
local function now() return emu:currentFrame() end

-- --- Game state ------------------------------------------------------------------

local function sb1() return emu:read32(S.gSaveBlock1Ptr) end
local function sb2() return emu:read32(S.gSaveBlock2Ptr) end
local function getFlag(f) return (emu:read8(sb1() + S.OFF_SB1_FLAGS + (f >> 3)) >> (f & 7)) & 1 == 1 end
local function defeated(t) return getFlag(S.TRAINER_FLAGS_START + t) end
local function mapId()
  local loc = sb1() + S.OFF_SB1_LOCATION
  return emu:read8(loc) * 256 + emu:read8(loc + 1)
end
local function playerObject()
  return S.gObjectEvents + emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_OBJECT_EVENT_ID) * S.OBJECT_EVENT_SIZE
end
local function pos()
  local c = playerObject() + S.OFF_OBJ_CURRENT_COORDS
  return emu:read16(c) - S.MAP_OFFSET, emu:read16(c + 2) - S.MAP_OFFSET
end
local function callback2() return emu:read32(S.gMain + S.OFF_MAIN_CALLBACK2) end
local function inOverworld() return callback2() == (S.CB2_Overworld | 1) end
local function inBattle() return callback2() == (S.BattleMainCB2 | 1) end
local CONTEXT_SHUTDOWN = 2
local function idle()
  return inOverworld()
     and emu:read8(S.sLockFieldControls) == 0
     and emu:read8(S.sGlobalScriptContextStatus) == CONTEXT_SHUTDOWN
     and emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_TILE_TRANSITION) == 0
end

local function expect(cond, what)
  if not cond then fail(what) end
  log("ok " .. what)
end

-- --- Input -----------------------------------------------------------------------

local function tap(key, hold)
  emu:addKey(key); wait(hold or 3); emu:clearKey(key); wait(3)
end
local function shot(name)
  emu:screenshot(OUT .. name)
  log("shot " .. name)
end
local function waitUntil(cond, limit, what)
  local t0 = now()
  while not cond() do
    if now() - t0 > limit then fail("timed out waiting for " .. what) end
    frame()
  end
end

-- Press A every 12 frames until the player is free again for 20 frames. A on a
-- YES/NO prompt answers YES.
local function settle(limit)
  local t0, calm = now(), 0
  while calm < 20 do
    if idle() then
      calm = calm + 1
      frame()
    else
      calm = 0
      tap(K.A)
      wait(6)
    end
    if now() - t0 > (limit or 20000) then fail("stuck: the player never got control back") end
  end
end

-- One step. Returns "moved", "blocked", or "taken" (the game took control: a
-- trainer saw the player, or a trigger fired).
local function step(key)
  local x0, y0 = pos()
  emu:addKey(key)
  local t0 = now()
  repeat
    frame()
    local x, y = pos()
    if x ~= x0 or y ~= y0 then break end
  until now() - t0 > 40
  emu:clearKey(key)
  local x, y = pos()
  if x == x0 and y == y0 then return "blocked" end
  t0 = now()
  local calm = 0
  while calm < 4 do
    if idle() then calm = calm + 1 else calm = 0 end
    if now() - t0 > 60 then return "taken" end
    frame()
  end
  return "moved"
end
local function walkTo(points)
  for _, p in ipairs(points) do
    while true do
      local x, y = pos()
      if x == p[1] and y == p[2] then break end
      local key
      if x < p[1] then key = K.RIGHT elseif x > p[1] then key = K.LEFT
      elseif y < p[2] then key = K.DOWN else key = K.UP end
      local r = step(key)
      if r ~= "moved" then return r end
    end
  end
  return "moved"
end

-- A trainer battle that starts from the current script. Screenshots the action menu.
local function battle(name, trainer)
  local t0 = now()
  while not inBattle() do
    tap(K.A); wait(9)
    if now() - t0 > 4000 then fail("no battle for " .. name) end
  end
  if os.getenv("SPRITE_REVIEW") == "1" then
    for i = 1, 8 do
      wait(60)
      shot(string.format("%s_intro_%02d.png", name, i))
    end
  else
    wait(480)
  end
  shot(name .. ".png")
  t0 = now()
  while not inOverworld() do
    tap(K.A); wait(6)
    if now() - t0 > 20000 then fail("battle never ended: " .. name) end
  end
  expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_WON, "won " .. name)
  expect(defeated(trainer), "trainer flag set after " .. name)
end

-- --- The injected scripts ----------------------------------------------------------

local blob = {}
do
  local f = assert(io.open("build/test_route1/setup.bin", "rb"))
  local data = f:read("a")
  f:close()
  for i = 1, #data do blob[i] = data:byte(i) end
  local syms = {}
  for line in io.lines("build/test_route1/setup.syms") do
    local name, hex = line:match("^(%S+) (%x+)$")
    if name then syms[name] = tonumber(hex, 16) end
  end
  S.blob = syms
end
local function loadBlob()
  for i, b in ipairs(blob) do emu:write8(BLOB_ADDR + i - 1, b) end
end
local function run(header, x, y)
  emu:write16(S.gSpecialVar_0x8008, x)
  emu:write16(S.gSpecialVar_0x8009, y)
  emu:write32(S.gMapHeader + S.OFF_MAPHEADER_MAPSCRIPTS, S.blob[header])
end
local function warpTo(header, map, x, y)
  run(header, x, y)
  waitUntil(function()
    local px, py = pos()
    return mapId() == map and px == x and py == y and idle()
  end, 3000, string.format("the warp to (%d,%d)", x, y))
  wait(200)  -- let the map-name popup slide away before any screenshot
end
local function tour(name, x, y)
  warpTo("Route1Test_WarpRoute1Header", S.MAP_ROUTE1, x, y)
  shot(name)
end

-- --- The test ---------------------------------------------------------------------

local function main()
  -- Boot, skip the intro, Quickstart (the smoke test's timing).
  waitUntil(function() return now() >= 500 end, 600, "frame 500")
  tap(K.START)
  waitUntil(function() return now() >= 1020 end, 600, "frame 1020")
  tap(K.SELECT)
  waitUntil(idle, 4000, "the new game")
  wait(30)
  local opt = sb2() + S.OFF_SB2_OPTIONS
  emu:write16(opt, (emu:read16(opt) & ~0x7) | 2 | (1 << 9) | (1 << 10))

  -- The state after beat 4, arriving on Route 1 south of Tityros's meadow.
  loadBlob()
  warpTo("Route1Test_SetupHeader", S.MAP_ROUTE1, 10, 52)
  shot("01_route1_meadow.png")

  -- Tityros, at the meadow wall's only gap, sees the player step through it.
  local r = walkTo({ { 10, 47 } })
  expect(r == "taken", "Tityros stops the player at the wall gap")
  battle("02_battle_tityros", S.TRAINER_TITYROS)
  settle()
  wait(60)
  shot("03_after_tityros.png")

  -- The route, south to north.
  -- The route, south to north (each stop is outside every trainer's line).
  tour("04_south_entrance.png", 11, 60)
  tour("05_carter.png", 13, 55)
  tour("06_meadow.png", 13, 47)
  tour("07_grove_narrows.png", 12, 37)
  tour("08_grove_lane.png", 21, 33)
  tour("09_big_olive.png", 9, 25)
  tour("10_bee_terraces.png", 13, 25)
  tour("11_fork.png", 13, 20)
  tour("12_spur.png", 23, 19)
  tour("13_cove.png", 7, 12)
  tour("14_north_road.png", 11, 3)

  -- The flock blocks the road north of the fork.
  tour("15_flock_before.png", 12, 16)
  expect(step(K.UP) == "moved" and step(K.UP) == "blocked", "the flock blocks the gap in the wall")
  expect(not getFlag(S.FLAG_HIDE_FLOCK), "flock shown before the ruins are cleared")

  -- Kronion Hill: the hill foot from the spur, then the summit scene.
  warpTo("Route1Test_WarpRoute1Header", S.MAP_ROUTE1, 26, 19)
  r = walkTo({ { 29, 19 } })
  expect(r == "moved", "the spur walks east")
  step(K.RIGHT)
  waitUntil(function() return mapId() == S.MAP_KRONION and idle() end, 600, "Kronion Hill by the connection")
  local kx, ky = pos()
  expect(kx == 0 and ky == 17, string.format("the spur meets the hill foot (at %d,%d)", kx, ky))
  shot("16_hill_foot.png")
  -- Along the path to the lower stair (6,15), east along the shelf, up the
  -- upper stair (13,11). The path keeps out of the tall grass.
  r = walkTo({ { 0, 16 }, { 6, 16 }, { 6, 13 }, { 13, 13 }, { 13, 11 } })
  expect(r == "moved", "the stairs climb to the summit")
  shot("17_summit_before.png")
  r = walkTo({ { 13, 10 } })
  expect(r == "taken", "the summit scene starts at the top of the stair")

  -- The scene: screenshots along the way; battles are fought as they come.
  local t0, n, nextShot = now(), 0, now() + 40
  local fights = { { "19_battle_petros", S.TRAINER_PETROS }, { "21_battle_amathos", S.TRAINER_AMATHOS } }
  local fought = 0
  while not (getFlag(S.FLAG_RUINS_CLEARED) and idle()) do
    if now() - t0 > 30000 then fail("the summit scene never finished") end
    if inBattle() then
      fought = fought + 1
      local f = fights[fought] or { "battle_extra", S.TRAINER_AMATHOS }
      battle(f[1], f[2])
    else
      if now() >= nextShot then
        n = n + 1
        shot(string.format("18_scene_%02d.png", n))
        nextShot = now() + 150
      end
      tap(K.A)
      wait(9)
    end
  end
  settle()
  expect(fought == 2, "two grunt battles in the scene")
  expect(getFlag(S.FLAG_FOUND_TABLET), "the tablet is found")
  expect(getFlag(S.FLAG_DEXNAV_GET), "the Augur's Eye is given")
  expect(getFlag(S.FLAG_HIDE_ALETHEA_RUINS) and getFlag(S.FLAG_HIDE_RUINS_GRUNTS), "Alethea and the grunts are gone")
  expect(getFlag(S.FLAG_HIDE_FLOCK), "the flock is told to move")
  shot("22_summit_after.png")

  -- Back on Route 1 the road north is open, and Agis holds the pass past the gap.
  tour("23_flock_after.png", 12, 16)
  r = walkTo({ { 12, 13 } })
  expect(r == "taken", "Agis stops the player in the pass")
  battle("24_battle_agis", S.TRAINER_AGIS)
  settle()
  r = walkTo({ { 12, 12 } })
  expect(r == "moved", "the road north is open")
  shot("25_road_open.png")

  -- Regression (QA, Route 1 softlock): the goat path's last lip drops onto row
  -- 13 east of the gap, and that pocket's only way out is west along row 13.
  -- Agis once stood in it at (14,13) and, beaten, walled the player in. Hop the
  -- lip at (17,11) and walk back out, west to the road and south through the gap.
  tour("26_goat_path.png", 17, 10)
  r = walkTo({ { 17, 11 } })
  expect(r == "moved", "down the goat path to its last lip")
  r = step(K.DOWN)
  local hx, hy = pos()
  expect(r == "moved" and hx == 17 and hy == 13, string.format("hopped the lip from (17,11) to (17,13), at (%d,%d)", hx, hy))
  r = walkTo({ { 12, 13 }, { 12, 16 } })
  local ox, oy = pos()
  expect(r == "moved" and ox == 12 and oy == 16,
         string.format("walked out of the lip's pocket past the beaten Agis, at (%d,%d)", ox, oy))
  shot("27_out_of_the_pocket.png")
end

local co = coroutine.create(main)
local realEmu = _G.emu
callbacks:add("frame", function()
  if not co then return end
  local result = table.pack(coroutine.resume(co))
  while true do
    if not result[1] then
      local err = tostring(result[2])
      console:log(err:find("^ROUTE1 FAIL") and err or ("ROUTE1 FAIL: " .. err))
      console:log("ROUTE1 done")
      co = nil
      return
    end
    if coroutine.status(co) == "dead" then
      console:log("ROUTE1 done")
      co = nil
      return
    end
    local kind = result[2]
    if kind == "frame" then return end
    if kind == "log" then
      console:log(result[3])
      result = table.pack(coroutine.resume(co))
    else -- "call"
      local fn = realEmu[result[3]]
      result = table.pack(coroutine.resume(co, fn(realEmu, table.unpack(result, 4, result.n))))
    end
  end
end)
