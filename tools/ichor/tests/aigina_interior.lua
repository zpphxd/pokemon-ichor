-- Aigina's interior check, run by tools/ichor/tests/aigina_interior.sh (read it first).
--
-- Env: AIGINA_OUT is the screenshot folder; AIGINA_SYMBOLS the table the .sh wrote.
--
-- Quickstarts a new game and sets the state after the voyage with Act II's Aigina
-- stop open (FLAG_ICHOR_FERRY_TO_AEGINA), so the town's north gate stands open.
-- Then it plays the detour on foot, every step a real walk found by a search over
-- the map the game has loaded (its collision and the people standing on it):
--   1. from Aigina Town up through the gate, across the seam onto the Aphaia Road;
--   2. up the road: the south sign, the Silver Powder on the ant hills, Myrmex,
--      the band of golden grass, Sostratos, the fork sign, the great herm
--      (anointed), the Super Potion and the Oros sign;
--   3. across the seam up Mount Oros: Zeus's altar and the Wine by it;
--   4. back down, east to Euthymia, the horos and the temple sign, up the steps
--      and across the seam to the Temple of Aphaia: the priestess, the Pretty
--      Feathers, Artemis's altar and the dig spot;
--   5. home the quick way: down the east terraces, hopping each ledge, to the
--      gate and back into the town.
-- A Repel that never runs out, ahead of a lead raised to level 100, keeps wild Pokémon
-- away; the trainers are ICHOR_ACT2 placeholders and never battle.
-- Prints "AIGINA ok ..." per check and "AIGINA shot ..." per screenshot, and ends
-- with "AIGINA done"; any failure prints "AIGINA FAIL: ..." first.

local S = dofile(os.getenv("AIGINA_SYMBOLS") or "build/test_aigina_interior/symbols.lua")
local OUT = os.getenv("AIGINA_OUT") or "build/test_aigina_interior/"
local K = { A = C.GBA_KEY.A, B = C.GBA_KEY.B, START = C.GBA_KEY.START, SELECT = C.GBA_KEY.SELECT,
            UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN, LEFT = C.GBA_KEY.LEFT, RIGHT = C.GBA_KEY.RIGHT }
local DIR = { [K.DOWN] = 1, [K.UP] = 2, [K.LEFT] = 3, [K.RIGHT] = 4 }
local DELTA = { [K.DOWN] = { 0, 1 }, [K.UP] = { 0, -1 }, [K.LEFT] = { -1, 0 }, [K.RIGHT] = { 1, 0 } }

-- The test reads as straight-line code in a coroutine. mGBA only lets its own
-- functions run on the main Lua thread, so the coroutine asks the frame callback
-- to make each call (yield "call") and to advance a frame (yield "frame").
local emu = setmetatable({}, { __index = function(_, name)
  return function(_, ...) return coroutine.yield("call", name, ...) end
end })
local function log(s) coroutine.yield("log", "AIGINA " .. s) end
local function fail(s) error("AIGINA FAIL: " .. s, 0) end
local function frame() coroutine.yield("frame") end
local function wait(n) for _ = 1, n do frame() end end
local function now() return emu:currentFrame() end

-- --- Game state ------------------------------------------------------------------

local function s16(v) if v >= 0x8000 then return v - 0x10000 end return v end
local function sb1() return emu:read32(S.gSaveBlock1Ptr) end
local function getFlag(f) return (emu:read8(sb1() + S.OFF_SB1_FLAGS + (f >> 3)) >> (f & 7)) & 1 == 1 end
local function setFlag(f)
  local a = sb1() + S.OFF_SB1_FLAGS + (f >> 3)
  emu:write8(a, emu:read8(a) | (1 << (f & 7)))
end
local function setVar(v, value) emu:write16(sb1() + S.OFF_SB1_VARS + 2 * (v - S.VARS_START), value) end
local function mapId()
  local loc = sb1() + S.OFF_SB1_LOCATION
  return emu:read8(loc) * 256 + emu:read8(loc + 1)
end
local function playerObject()
  return S.gObjectEvents + emu:read8(S.gPlayerAvatar + S.OFF_AVATAR_OBJECT_EVENT_ID) * S.OBJECT_EVENT_SIZE
end
local function pos()
  local c = playerObject() + S.OFF_OBJ_CURRENT_COORDS
  return s16(emu:read16(c)) - S.MAP_OFFSET, s16(emu:read16(c + 2)) - S.MAP_OFFSET
end
local function inOverworld() return emu:read32(S.gMain + S.OFF_MAIN_CALLBACK2) == (S.CB2_Overworld | 1) end
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
    if now() - t0 > limit then
      local x, y = pos()
      shot("timeout.png")
      fail(string.format("timed out waiting for %s (on 0x%04X at (%d,%d))", what, mapId(), x, y))
    end
    frame()
  end
end

-- Press A every few frames until the player has had control for 20 frames: it
-- reads every box, answers YES, and sits through item fanfares.
local function settle(limit)
  local t0, calm = now(), 0
  while calm < 20 do
    if idle() then
      calm = calm + 1
      frame()
    else
      calm = 0
      tap(K.A)
      wait(8)
    end
    if now() - t0 > (limit or 6000) then fail("stuck: the player never got control back") end
  end
end

-- One step. "moved", or "blocked" if the player didn't leave the cell.
local function step(key)
  local x0, y0 = pos()
  local m0 = mapId()
  emu:addKey(key)
  local t0 = now()
  repeat
    frame()
    local x, y = pos()
    if x ~= x0 or y ~= y0 or mapId() ~= m0 then break end
  until now() - t0 > 40
  emu:clearKey(key)
  local x, y = pos()
  if x == x0 and y == y0 and mapId() == m0 then return "blocked" end
  waitUntil(idle, 300, "the step to settle")
  wait(2)
  return "moved"
end

-- Face a direction without moving: a short tap of a new direction turns the
-- player in place (facingDirection is the low nibble at 0x18 of their object).
local function facing() return emu:read8(playerObject() + 0x18) & 0xF end
local function face(key)
  local d = DIR[key]
  local x0, y0 = pos()
  for _ = 1, 3 do
    if facing() == d then break end
    emu:addKey(key); wait(5); emu:clearKey(key)
    waitUntil(idle, 120, "the turn")
    wait(8)
  end
  local x, y = pos()
  if x ~= x0 or y ~= y0 then fail("turning to face something walked the player off") end
  if facing() ~= d then fail(string.format("could not turn to face direction %d (facing %d)", d, facing())) end
end

-- --- The loaded map ------------------------------------------------------------------

-- The current map's size and cells, from gBackupMapLayout (the map with a
-- MAP_OFFSET margin round it). A cell can be walked on when it has no collision
-- and the land's elevation (3); ledges are solid, so walks never hop one.
local function grid()
  local bw = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_WIDTH)
  local bh = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_HEIGHT)
  local base = emu:read32(S.gBackupMapLayout + S.OFF_BACKUP_MAP_MAP)
  local w, h = bw - S.MAP_OFFSET_W, bh - S.MAP_OFFSET_H
  local open = {}
  for y = 0, h - 1 do
    for x = 0, w - 1 do
      local v = emu:read16(base + 2 * ((x + S.MAP_OFFSET) + (y + S.MAP_OFFSET) * bw))
      open[y * w + x] = (v >> 10) & 3 == 0 and (v >> 12) == 3
    end
  end
  -- people and item balls stand in the way
  local px, py = pos()
  for i = 0, S.OBJECT_EVENTS_COUNT - 1 do
    local o = S.gObjectEvents + i * S.OBJECT_EVENT_SIZE
    if emu:read8(o) & 1 == 1 then
      local c = o + S.OFF_OBJ_CURRENT_COORDS
      local x, y = s16(emu:read16(c)) - S.MAP_OFFSET, s16(emu:read16(c + 2)) - S.MAP_OFFSET
      if not (x == px and y == py) and x >= 0 and y >= 0 and x < w and y < h then
        open[y * w + x] = false
      end
    end
  end
  return { w = w, h = h, open = open }
end

local function isOpen(g, x, y)
  return x >= 0 and y >= 0 and x < g.w and y < g.h and g.open[y * g.w + x]
end

-- A breadth-first walk to any of the goal cells: the keys to press.
local function route(goals)
  local g = grid()
  local sx, sy = pos()
  local want = {}
  for _, p in ipairs(goals) do want[p[2] * g.w + p[1]] = true end
  local prev, q, head = { [sy * g.w + sx] = false }, { { sx, sy } }, 1
  while q[head] do
    local x, y = q[head][1], q[head][2]
    head = head + 1
    if want[y * g.w + x] then
      local keys, k = {}, y * g.w + x
      while prev[k] do
        table.insert(keys, 1, prev[k][2])
        k = prev[k][1]
      end
      return keys
    end
    for _, key in ipairs({ K.UP, K.DOWN, K.LEFT, K.RIGHT }) do
      local nx, ny = x + DELTA[key][1], y + DELTA[key][2]
      local nk = ny * g.w + nx
      if isOpen(g, nx, ny) and prev[nk] == nil then
        prev[nk] = { y * g.w + x, key }
        table.insert(q, { nx, ny })
      end
    end
  end
  return nil
end

local function walkTo(x, y, what)
  local keys = route({ { x, y } })
  if not keys then fail("no walk to (" .. x .. "," .. y .. ") for " .. what) end
  for _, key in ipairs(keys) do
    if step(key) ~= "moved" then
      local px, py = pos()
      fail(string.format("blocked at (%d,%d) on the walk to %s", px, py, what))
    end
  end
  local px, py = pos()
  expect(px == x and py == y, string.format("walked to (%d,%d): %s", x, y, what))
end

-- Walk to (x, y) and on across the map's edge with `key`, onto `map` at (nx, ny).
local function cross(x, y, key, map, nx, ny, what)
  walkTo(x, y, "the seam to " .. what)
  step(key)
  local px, py = pos()
  expect(mapId() == map and px == nx and py == ny,
         string.format("crossed into %s at (%d,%d) (on 0x%04X at (%d,%d))", what, nx, ny, mapId(), px, py))
end

-- Walk next to the thing at (x, y), face it, press A and read it all; a shot of
-- its first box is name.png.
local function use(x, y, name)
  local fronts = {}
  for _, key in ipairs({ K.UP, K.DOWN, K.LEFT, K.RIGHT }) do
    table.insert(fronts, { x - DELTA[key][1], y - DELTA[key][2], key })
  end
  local keys = route(fronts)
  if not keys then fail("no walk up to " .. name) end
  for _, key in ipairs(keys) do
    if step(key) ~= "moved" then fail("blocked on the walk up to " .. name) end
  end
  local px, py = pos()
  for _, f in ipairs(fronts) do
    if f[1] == px and f[2] == py then face(f[3]) end
  end
  -- (A pressed on the frame a walk settles can go unheard: press until a
  -- script takes the field)
  wait(10)
  for _ = 1, 3 do
    tap(K.A)
    wait(10)
    if not idle() then break end
  end
  if idle() then fail(string.format("pressing A at (%d,%d) facing %d started nothing for %s", px, py, facing(), name)) end
  wait(10)
  shot(name .. ".png")
  settle()
end

-- Warp, as a door does but without the fade (ichor_lib.lua's warp).
local function warp(map, x, y)
  local sb = sb1()
  emu:write16(sb + S.OFF_SB1_POS, x)
  emu:write16(sb + S.OFF_SB1_POS + 2, y)
  local loc = sb + S.OFF_SB1_LOCATION
  emu:write8(loc, map >> 8)
  emu:write8(loc + 1, map & 0xFF)
  emu:write8(loc + 2, 0xFF)
  emu:write16(loc + 4, x)
  emu:write16(loc + 6, y)
  emu:write32(S.gMain + S.OFF_MAIN_CALLBACK2, S.CB2_LoadMap | 1)
  waitUntil(function()
    local px, py = pos()
    return mapId() == map and px == x and py == y and idle()
  end, 3000, string.format("the warp to (%d,%d)", x, y))
  wait(200)  -- let the map-name popup slide away
end

-- Hop the ledge below: one step south that lands two cells down.
local function hop(what)
  local x0, y0 = pos()
  step(K.DOWN)
  waitUntil(idle, 300, "the hop to land")
  local x, y = pos()
  expect(x == x0 and y == y0 + 2, string.format("hopped %s from (%d,%d) to (%d,%d)", what, x0, y0, x, y))
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
  local opt = emu:read32(S.gSaveBlock2Ptr) + S.OFF_SB2_OPTIONS
  emu:write16(opt, (emu:read16(opt) & ~0x7) | 3)          -- instant text

  -- After the voyage, Act II's Aigina stop open; no wild Pokémon on the walk
  for _, f in ipairs({ S.FLAG_ARRIVED, S.FLAG_VISITED, S.FLAG_HIDE_CAST, S.FLAG_NIGHT,
                       S.FLAG_CROSSING_DONE, S.FLAG_AIGINA_STOP }) do setFlag(f) end
  -- (Quickstart's lead is level 14 and the island's wild ones 12-16, so the lead
  -- is raised to 100 and a Repel that never runs out turns every one away)
  emu:write8(S.gParties + S.OFF_MON_LEVEL, 100)
  setVar(S.VAR_REPEL_STEP_COUNT, 30000)

  -- 1. Aigina Town, through the open gate, onto the road
  warp(S.MAP_TOWN, 24, 6)
  shot("01_town_gate.png")
  cross(24, 0, K.UP, S.MAP_ROAD, 20, 23, "the Aphaia Road")
  wait(30)
  shot("02_road_gate.png")

  -- 2. up the road
  use(19, 20, "03_south_sign")
  walkTo(14, 17, "the lower terrace")
  shot("04_lower_terrace.png")
  use(22, 13, "05_silver_powder")
  expect(getFlag(S.FLAG_SILVER_POWDER), "the Silver Powder on the ant hills is picked up")
  use(13, 14, "06_myrmex")
  walkTo(17, 11, "the upper terrace")
  shot("07_upper_terrace.png")
  walkTo(21, 8, "the band of golden grass")
  shot("08_band.png")
  use(20, 6, "09_sostratos")
  use(20, 3, "10_fork_sign")
  use(22, 3, "11_herm")
  expect(getFlag(S.FLAG_HERM), "the great herm is anointed")
  use(12, 3, "12_super_potion")
  expect(getFlag(S.FLAG_SUPER_POTION), "the Super Potion at the Oros fork is picked up")
  use(10, 3, "13_oros_sign")

  -- 3. Mount Oros
  cross(8, 0, K.UP, S.MAP_OROS, 8, 15, "Mount Oros")
  wait(30)
  shot("14_oros_foot.png")
  walkTo(5, 10, "the golden band on Oros")
  shot("15_oros_climb.png")
  use(6, 4, "16_altar_of_zeus")
  shot("17_oros_summit.png")
  use(8, 4, "18_wine")
  expect(getFlag(S.FLAG_WINE), "the Wine (Berry Juice for now) by Zeus's altar is picked up")
  cross(8, 15, K.DOWN, S.MAP_ROAD, 8, 0, "the Aphaia Road again")

  -- 4. east to the temple
  use(26, 3, "19_euthymia")
  use(34, 4, "20_horos")
  walkTo(27, 3, "the foot of the temple steps")
  shot("21_temple_steps.png")
  use(30, 1, "22_temple_sign")
  cross(27, 0, K.UP, S.MAP_TEMPLE, 11, 19, "the Temple of Aphaia")
  wait(30)
  shot("23_temple_slope.png")
  use(11, 9, "24_priestess")
  shot("25_temple_front.png")
  use(14, 9, "26_pretty_feathers")
  expect(getFlag(S.FLAG_FEATHERS), "the Pretty Feathers on the temple steps are picked up")
  use(15, 11, "27_altar_of_artemis")
  use(18, 11, "28_dig_spot")
  shot("29_foundations.png")

  -- 5. home the quick way: down the east terraces
  cross(11, 19, K.DOWN, S.MAP_ROAD, 27, 0, "the Aphaia Road, going home")
  walkTo(29, 6, "the hill east of the steps")
  shot("30_east_hill.png")
  hop("onto the orchard terrace")
  walkTo(29, 11, "the orchard terrace's lip")
  hop("onto the meadow terrace")
  shot("31_meadow_terrace.png")
  walkTo(27, 16, "the meadow terrace's lip")
  hop("into the orchard by the gate")
  shot("32_orchard_home.png")
  cross(20, 23, K.DOWN, S.MAP_TOWN, 24, 0, "Aigina Town")
  wait(30)
  shot("33_home.png")

  expect(getFlag(S.FLAG_HERM) and getFlag(S.FLAG_SILVER_POWDER) and getFlag(S.FLAG_SUPER_POTION)
         and getFlag(S.FLAG_FEATHERS) and getFlag(S.FLAG_WINE), "every flag of the detour is set")
  log("PASS")
end

local co = coroutine.create(main)
local realEmu = _G.emu
callbacks:add("frame", function()
  if not co then return end
  local result = table.pack(coroutine.resume(co))
  while true do
    if not result[1] then
      local err = tostring(result[2])
      console:log(err:find("^AIGINA FAIL") and err or ("AIGINA FAIL: " .. err))
      console:log("AIGINA done")
      co = nil
      return
    end
    if coroutine.status(co) == "dead" then
      console:log("AIGINA done")
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
