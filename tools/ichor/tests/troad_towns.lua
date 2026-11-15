-- The Troad's towns and lane, run by tools/ichor/tests/troad_towns.sh (read it first).
--
-- Setup touches no ROM data: after Quickstart the test copies troad_towns_setup.s's
-- blob into spare EWRAM and points the current map header's script table at one of
-- its ON_FRAME headers. The doors, signs, hidden items and people come from the
-- maps' own map.json (troad_towns.py), so the test follows the builders.
--
-- Prints "TROAD ok ..." per check and "TROAD shot ..." per screenshot, and ends
-- with "TROAD done"; any failure prints "TROAD FAIL: ..." first.

local S = dofile("build/test_troad_towns/symbols.lua")
local G = dofile("build/test_troad_towns/grids.lua")
local OUT = os.getenv("TROAD_OUT") or "build/test_troad_towns/"
local BLOB_ADDR = tonumber(os.getenv("TROAD_BLOB_ADDR") or "0x0203F000")
local K = { A = C.GBA_KEY.A, B = C.GBA_KEY.B, START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT,
            UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN, LEFT = C.GBA_KEY.LEFT, RIGHT = C.GBA_KEY.RIGHT }

local emu = setmetatable({}, { __index = function(_, name)
  return function(_, ...) return coroutine.yield("call", name, ...) end
end })
local function log(s) coroutine.yield("log", "TROAD " .. s) end
local function fail(s) error("TROAD FAIL: " .. s, 0) end
local function frame() coroutine.yield("frame") end
local function wait(n) for _ = 1, n do frame() end end
local function now() return emu:currentFrame() end

-- --- Game state ------------------------------------------------------------------

local function sb1() return emu:read32(S.gSaveBlock1Ptr) end
local function sb2() return emu:read32(S.gSaveBlock2Ptr) end
local function getFlag(f)
  if f >= S.ICHOR_FLAGS_START then
    local base = emu:read32(S.gSaveBlock3Ptr) + S.OFF_SB3_ICHOR + S.OFF_ICHOR_FLAGS
    local i = f - S.ICHOR_FLAGS_START
    return (emu:read8(base + (i >> 3)) >> (i & 7)) & 1 == 1
  end
  return (emu:read8(sb1() + S.OFF_SB1_FLAGS + (f >> 3)) >> (f & 7)) & 1 == 1
end
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

local checks = 0
local function expect(cond, what)
  if not cond then fail(what) end
  checks = checks + 1
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
    if now() - t0 > 90 then return "taken" end
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

-- --- The injected scripts ----------------------------------------------------------

local blob = {}
do
  local f = assert(io.open(OUT .. "setup.bin", "rb"))
  local data = f:read("a")
  f:close()
  for i = 1, #data do blob[i] = data:byte(i) end
  local syms = {}
  for line in io.lines(OUT .. "setup.syms") do
    local name, hex = line:match("^(%S+) (%x+)$")
    if name then syms[name] = tonumber(hex, 16) end
  end
  S.blob = syms
end
local function loadBlob()
  for i, b in ipairs(blob) do emu:write8(BLOB_ADDR + i - 1, b) end
end
local HEADERS = { Sestos = "TroadTest_WarpSestosHeader", Hellespont = "TroadTest_WarpHellespontHeader",
                  Ilion = "TroadTest_WarpIlionHeader" }
local MAPS = { Sestos = "MAP_SESTOS", Hellespont = "MAP_HELLESPONT", Ilion = "MAP_ILION" }
local function warpTo(m, x, y, header)
  emu:write16(S.gSpecialVar_0x8008, x)
  emu:write16(S.gSpecialVar_0x8009, y)
  emu:write32(S.gMapHeader + S.OFF_MAPHEADER_MAPSCRIPTS, S.blob[header or HEADERS[m]])
  waitUntil(function()
    local px, py = pos()
    return mapId() == S[MAPS[m]] and px == x and py == y and idle()
  end, 3000, string.format("the warp to %s (%d,%d)", m, x, y))
  wait(20)
end

-- Face a direction from a fresh warp (which leaves the player facing south): a
-- short press of another direction only turns the player.
local function face(dir)
  if dir ~= "DOWN" then tap(K[dir], 2) end
  wait(4)
end

-- Press A and expect a script to start (a text box), then play it out.
local function interact(what)
  tap(K.A)
  local t0, started = now(), false
  while now() - t0 < 60 do
    if not idle() then started = true break end
    frame()
  end
  expect(started, what .. " answers")
  settle()
end

local function battle(name, trainer)
  local t0 = now()
  while not inBattle() do
    tap(K.A); wait(9)
    if now() - t0 > 4000 then fail("no battle for " .. name) end
  end
  wait(480)
  shot(name .. ".png")
  t0 = now()
  while not inOverworld() do
    tap(K.A); wait(6)
    if now() - t0 > 30000 then fail("battle never ended: " .. name) end
  end
  expect(emu:read8(S.gBattleOutcome) == S.B_OUTCOME_WON, "won " .. name)
  expect(defeated(trainer), "trainer flag set after " .. name)
end

local function doors(m)
  for i, d in ipairs(G[m].doors) do
    warpTo(m, d.x, d.y)
    face("UP")
    tap(K.UP, 10)
    waitUntil(function() return mapId() == S[d.dest] and idle() end, 600,
              string.format("%s door %d to %s", m, i - 1, d.dest))
    expect(true, string.format("%s door %d leads to %s", m, i - 1, d.dest))
    wait(30)
    shot(string.format("%s_door_%d.png", m:lower(), i - 1))
  end
end

local function reads(m)
  for _, r in ipairs(G[m].reads) do
    warpTo(m, r.x, r.y)
    face(r.face)
    interact(m .. " " .. r.what)
    if r.flag then expect(getFlag(S[r.flag]), m .. " " .. r.what .. " is taken") end
  end
end

local function talks(m)
  for _, t in ipairs(G[m].talks) do
    warpTo(m, t.x, t.y)
    face(t.face)
    interact(m .. " " .. t.what)
  end
end

-- --- The test ---------------------------------------------------------------------

local function main()
  waitUntil(function() return now() >= 500 end, 600, "frame 500")
  tap(K.START)
  waitUntil(function() return now() >= 1020 end, 600, "frame 1020")
  tap(K.SELECT)
  waitUntil(idle, 4000, "the new game")
  wait(30)
  local opt = sb2() + S.OFF_SB2_OPTIONS
  emu:write16(opt, (emu:read16(opt) & ~0x7) | 2 | (1 << 9) | (1 << 10))

  -- Landing at Sestos: on the mole, south of Nausikles at the gangplank's foot.
  loadBlob()
  warpTo("Sestos", 12, 24, "TroadTest_SetupHeader")
  shot("01_sestos_landing.png")
  expect(not getFlag(S.FLAG_ICHOR_OIKOUMENE_ARRIVED), "nobody has landed in the Oikoumene yet")

  -- Alethea's quay scene: walking off the mole meets her, once.
  local r = walkTo({ { 8, 24 } })
  expect(r == "taken", "Alethea stops the player at the root of the mole")
  wait(40)
  shot("02_alethea.png")
  settle()
  expect(getFlag(S.FLAG_ICHOR_OIKOUMENE_ARRIVED), "Alethea's scene sets FLAG_ICHOR_OIKOUMENE_ARRIVED")
  warpTo("Sestos", 12, 24)
  r = walkTo({ { 8, 24 }, { 6, 24 } })
  expect(r == "moved", "the scene plays only once")

  -- Sestos: every door, sign, hidden item and person.
  doors("Sestos")
  reads("Sestos")
  talks("Sestos")
  shot("03_sestos_quay.png")

  -- The Hellespont: signs and hidden items (Helle's rock from the water), people.
  reads("Hellespont")
  talks("Hellespont")
  warpTo("Hellespont", 31, 13)
  shot("04_helles_rock.png")

  -- Kotys holds the strip's narrows.
  warpTo("Hellespont", 31, 4)
  r = walkTo({ { 20, 4 } })
  expect(r == "taken", "Kotys sees the player in the strip's narrows")
  battle("05_battle_kotys", S.TRAINER_KOTYS)
  settle()

  -- The beach's set piece: the old man's bone, once.
  warpTo("Hellespont", 26, 32)
  face("UP")
  interact("the beach elder")
  expect(getFlag(S.FLAG_ICHOR_HELLESPONT_GOT_RARE_BONE), "the beach elder gives his Rare Bone")

  -- The current carries a surfer east.
  local c = G.current
  warpTo("Hellespont", c.x, c.y)
  emu:addKey(K.DOWN); wait(10); emu:clearKey(K.DOWN)
  waitUntil(idle, 1200, "the current to let go")
  wait(20)
  local x, y = pos()
  expect(y == c.y + 1 and x > c.x, string.format("the current carries the surfer east from (%d,%d) to (%d,%d)",
                                                    c.x, c.y + 1, x, y))
  shot("06_current.png")

  -- Surf east along the north channel to the Bosporus seam, and back.
  warpTo("Hellespont", 55, 9)
  r = walkTo({ { 63, 9 } })
  x, y = pos()
  expect(r == "moved" and x == 63 and y == 9, "surfed east to the seam column at (63,9)")
  shot("07_east_seam.png")
  r = walkTo({ { 56, 9 } })
  x, y = pos()
  expect(r == "moved" and x == 56, "and back west from the seam")

  -- Ilion: every door, sign, hidden item and person.
  doors("Ilion")
  reads("Ilion")
  talks("Ilion")
  warpTo("Ilion", 27, 18)
  shot("08_ilion_ramp_gate.png")
  warpTo("Ilion", 12, 18)
  shot("09_ilion_skaian_gate.png")

  -- Home with Nausikles.
  warpTo("Sestos", 12, 24)
  face("UP")
  local t0 = now()
  while not (mapId() == S.MAP_AKTI_TOWN and idle()) do
    if now() - t0 > 3000 then fail("Nausikles never sailed home") end
    if mapId() ~= S.MAP_AKTI_TOWN then tap(K.A) end
    wait(10)
  end
  expect(true, "Nausikles sails the player home to Akti")
  wait(30)
  shot("10_home_at_akti.png")
  log("ok " .. checks .. " checks")
end

local co = coroutine.create(main)
local realEmu = _G.emu
callbacks:add("frame", function()
  if not co then return end
  local result = table.pack(coroutine.resume(co))
  while true do
    if not result[1] then
      local err = tostring(result[2])
      console:log(err:find("^TROAD FAIL") and err or ("TROAD FAIL: " .. err))
      console:log("TROAD done")
      co = nil
      return
    end
    if coroutine.status(co) == "dead" then
      console:log("TROAD done")
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
