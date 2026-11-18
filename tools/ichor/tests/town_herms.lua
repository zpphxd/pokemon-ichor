-- Travel herms check, run by tools/ichor/tests/town_herms.sh (read it first).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, tap = L.log, L.expect, L.wait, L.shot, L.tap

-- The landing tiles beside each herm (src/data/ichor_town_herms.h)
local AKTI_X, AKTI_Y = 13, 26          -- the herm is east, at (14,26)
local EMP_X, EMP_Y = 19, 41            -- the herm is south, at (19,42)
local MAPCURSOR_X_MIN, MAPCURSOR_Y_MIN = 1, 2   -- region_map.c: section cell (0,0)'s screen tile

local function registered(t) return L.getFlag(S.FLAG_ICHOR_TOWN_HERMS_START + t) end
local function registeredList()
  local out = {}
  for t = 0, S.TOWN_HERM_COUNT - 1 do if registered(t) then out[#out + 1] = t end end
  return table.concat(out, ",")
end

local function yesNo() return L.taskRunning("Task_HandleYesNoInput") end

-- Press A through a running script's messages until `cond` holds (never on a
-- question, and never once the player is free: A would touch the herm again).
local function pressUntil(cond, limit, what)
  local t0 = L.now()
  while not cond() do
    if L.now() - t0 > (limit or 1500) then shot("stuck"); L.fail("never reached " .. what) end
    if L.idle() or yesNo() or L.on("CB2_FlyMap") then
      wait(2)
    else
      wait(12)
      if not (cond() or L.idle() or yesNo() or L.on("CB2_FlyMap")) then tap(K.A) end
    end
  end
end

-- The travel map's state: the chosen herm, the cursor's cell, the lit herms.
local function flyMap() return emu:read32(S.sFlyMap) end
local function dest() return emu:read8(flyMap() + S.OFF_FLYMAP_HERMDEST) end
local function cursorCell()
  local rm = flyMap() + S.OFF_FLYMAP_REGIONMAP
  return emu:read16(rm + S.OFF_RM_CURSOR_X) - MAPCURSOR_X_MIN, emu:read16(rm + S.OFF_RM_CURSOR_Y) - MAPCURSOR_Y_MIN
end
local function hermCell(t)
  local row = S.gIchorTownHerms + t * S.TOWN_HERM_ROW_SIZE
  return emu:read8(row + S.OFF_TH_MAPX), emu:read8(row + S.OFF_TH_MAPY)
end
local function litHerms()
  local lit = {}
  for i = 0, S.MAX_SPRITES - 1 do
    local sp = S.gSprites + i * S.SPRITE_SIZE
    if emu:read32(sp + S.OFF_SPRITE_CALLBACK) & ~1 == S.SpriteCB_FlyDestIcon then  -- Thumb bit off
      lit[#lit + 1] = emu:read16(sp + S.OFF_SPRITE_DATA0 + 4)                       -- data[2], the herm
    end
  end
  table.sort(lit)
  return table.concat(lit, ",")
end
local function ids(list) table.sort(list); return table.concat(list, ",") end

-- Touch the herm in direction `key`; YES opens the travel map, NO lets go.
local function touchHerm(key, travel)
  L.face(key)
  tap(K.A)
  pressUntil(function() return yesNo() or L.idle() end, 1500, "the herm's question")
  if not yesNo() then return false end
  wait(10)
  if not travel then
    tap(K.DOWN); tap(K.A)
    pressUntil(L.idle, 600, "the herm to let go")
    return false
  end
  tap(K.A)                                         -- YES
  L.waitUntil(function() return L.on("CB2_FlyMap") end, 900, "the herm travel map")
  wait(40)                                         -- its fade in
  return true
end

-- On the open map: check the cursor sits on its herm's own cell, press the
-- d-pad around and collect every herm the cursor reaches, then steer to `goal`.
local DIRS = { K.RIGHT, K.UP, K.LEFT, K.DOWN, K.DOWN, K.RIGHT, K.UP, K.UP, K.LEFT, K.LEFT, K.DOWN, K.RIGHT }
local function exploreTo(goal, where)
  local seen, order, off = {}, {}, nil
  local function note()
    local d = dest()
    local cx, cy = cursorCell()
    local hx, hy = hermCell(d)
    if (cx ~= hx or cy ~= hy) and not off then off = string.format("herm %d, cursor (%d,%d)", d, cx, cy) end
    if not seen[d] then seen[d] = true; order[#order + 1] = d end
  end
  note()
  for _, key in ipairs(DIRS) do tap(key); wait(4); note() end
  expect(not off, where .. ": the cursor always sits on its herm's own cell (" .. (off or "") .. ")")
  for _ = 1, 20 do
    if dest() == goal then break end
    for _, key in ipairs({ K.RIGHT, K.UP, K.LEFT, K.DOWN }) do
      if dest() == goal then break end
      tap(key); wait(4)
    end
  end
  return ids(order)
end

L.start(function()
  L.quickstart()
  L.runHeader("TownHermTest_SetupHeader", { limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_AKTI_ASCLEPEION and L.idle() end, 3000, "Akti's Asclepeion")
  wait(30)
  expect(registeredList() == "", "a new game has no travel herm registered (" .. registeredList() .. ")")

  -- Town A: rest at Akti's Asclepeion
  L.runHeader("TownHermTest_HealHeader", { limit = 4000 })
  expect(registered(S.TOWN_HERM_AKTI), "resting at Akti's Asclepeion registers Akti's herm")
  expect(registeredList() == tostring(S.TOWN_HERM_AKTI), "and only Akti's (" .. registeredList() .. ")")

  -- Town B: walk up to Emporion's entrance herm and touch it
  L.setVar(S.VAR_0x8008, EMP_X); L.setVar(S.VAR_0x8009, EMP_Y)
  L.runHeader("TownHermTest_EmporionHeader", { limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_EMPORION and L.idle() end, 3000, "Emporion")
  wait(60)
  shot("emporion_entrance_herm")
  expect(not registered(S.TOWN_HERM_EMPORION), "Emporion's herm waits for a touch")
  touchHerm(K.DOWN, false)
  expect(registered(S.TOWN_HERM_EMPORION), "touching Emporion's herm registers it")
  expect(not registered(S.TOWN_HERM_ELAIA) and not registered(S.TOWN_HERM_THYRSA),
         "towns never visited stay unregistered (" .. registeredList() .. ")")

  -- An unregistered town is neither counted nor reachable
  L.setVar(S.VAR_0x8004, S.TOWN_HERM_THYRSA)
  L.runHeader("TownHermTest_ProbeHeader", { limit = 600 })
  expect(L.getVar(S.VAR_0x8005) == 1, string.format("Emporion's herm offers 1 other town (%d)", L.getVar(S.VAR_0x8005)))
  expect(L.getVar(S.VAR_0x8006) == 0 and L.mapId() == S.MAP_EMPORION,
         "travel to unregistered Thyrsa is refused")

  -- Two more towns known (Elaia and Eleusa); Thyrsa stays unknown
  L.setFlag(S.FLAG_ICHOR_TOWN_HERMS_START + S.TOWN_HERM_ELAIA, true)
  L.setFlag(S.FLAG_ICHOR_TOWN_HERMS_START + S.TOWN_HERM_ELEUSA, true)
  local others = ids({ S.TOWN_HERM_ELAIA, S.TOWN_HERM_AKTI, S.TOWN_HERM_ELEUSA })

  -- B -> A on the map: only registered herms other than Emporion are lit or reachable
  expect(touchHerm(K.DOWN, true), "YES at Emporion's herm opens the travel map")
  shot("herm_map_emporion")
  expect(litHerms() == others, "Emporion's travel map lights Elaia, Akti and Eleusa only (" .. litHerms() .. ")")
  local reached = exploreTo(S.TOWN_HERM_AKTI, "Emporion's map")
  expect(reached == others, "the cursor snaps between those three herms and no others (" .. reached .. ")")
  expect(dest() == S.TOWN_HERM_AKTI, "the cursor can be steered to Akti")
  wait(20)
  shot("herm_map_cursor_akti")
  tap(K.A)
  L.waitUntil(function() return L.mapId() == S.MAP_AKTI and L.idle() end, 3000, "the travel to Akti")
  wait(40)
  shot("arrived_akti")
  local x, y = L.pos()
  expect(x == AKTI_X and y == AKTI_Y, string.format("Hermes sets the player beside Akti's herm (%d,%d)", x, y))

  -- B on the map: back to the field, standing where the player was
  expect(touchHerm(K.RIGHT, true), "YES at Akti's herm opens the travel map")
  shot("herm_map_akti")
  others = ids({ S.TOWN_HERM_ELAIA, S.TOWN_HERM_EMPORION, S.TOWN_HERM_ELEUSA })
  expect(litHerms() == others, "Akti's travel map lights Elaia, Emporion and Eleusa, not Akti (" .. litHerms() .. ")")
  tap(K.B)
  L.waitUntil(function() return L.idle() end, 1500, "the field after B")
  wait(30)
  shot("cancelled_akti")
  x, y = L.pos()
  expect(L.mapId() == S.MAP_AKTI and x == AKTI_X and y == AKTI_Y, "B on the travel map stays put")

  -- A -> B on the map
  expect(touchHerm(K.RIGHT, true), "Akti's herm opens the travel map again")
  reached = exploreTo(S.TOWN_HERM_EMPORION, "Akti's map")
  expect(reached == others, "Akti's map reaches the same three herms (" .. reached .. ")")
  wait(20)
  shot("herm_map_cursor_emporion")
  tap(K.A)
  L.waitUntil(function() return L.mapId() == S.MAP_EMPORION and L.idle() end, 3000, "the travel to Emporion")
  wait(40)
  shot("arrived_emporion")
  x, y = L.pos()
  expect(x == EMP_X and y == EMP_Y, string.format("Hermes sets the player beside Emporion's herm (%d,%d)", x, y))

  -- Every herm known: all 24 others lit, and Kythera's two towns each have a cell
  for t = 0, S.TOWN_HERM_COUNT - 1 do L.setFlag(S.FLAG_ICHOR_TOWN_HERMS_START + t, true) end
  expect(touchHerm(K.DOWN, true), "Emporion's herm opens the travel map with every herm known")
  local n = 0
  for _ in litHerms():gmatch("%d+") do n = n + 1 end
  expect(n == S.TOWN_HERM_COUNT - 1, string.format("every herm but Emporion's is lit (%d)", n))
  shot("herm_map_all")
  local function steer(goal)
    for _ = 1, 40 do
      if dest() == goal then return true end
      local cx, cy = hermCell(dest())
      local gx, gy = hermCell(goal)
      local before = dest()
      local keys = math.abs(gx - cx) >= math.abs(gy - cy)
                   and { gx > cx and K.RIGHT or K.LEFT, gy > cy and K.DOWN or K.UP }
                   or { gy > cy and K.DOWN or K.UP, gx > cx and K.RIGHT or K.LEFT }
      tap(keys[1]); wait(4)
      if dest() == before and keys[2] then tap(keys[2]); wait(4) end
    end
    return dest() == goal
  end
  expect(steer(S.TOWN_HERM_SKANDEIA), "the cursor reaches Skandeia")
  wait(20); shot("herm_map_skandeia")
  tap(K.DOWN); wait(20)
  expect(dest() == S.TOWN_HERM_PAPHIA, "and Paphia, its own cell just south on Kythera")
  shot("herm_map_paphia")
  expect(steer(S.TOWN_HERM_OLYMPUS), "the cursor reaches Olympus")
  wait(20); shot("herm_map_olympus")
  tap(K.B)
  L.waitUntil(function() return L.idle() end, 1500, "the field after B")
  x, y = L.pos()
  expect(L.mapId() == S.MAP_EMPORION and x == EMP_X and y == EMP_Y, "B stays put at Emporion")
end)
