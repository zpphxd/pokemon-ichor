-- Travel herms check, run by tools/ichor/tests/town_herms.sh (read it first).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, tap = L.log, L.expect, L.wait, L.shot, L.tap

-- The landing tiles beside each herm (src/data/ichor_town_herms.h)
local AKTI_X, AKTI_Y = 13, 26          -- the herm is east, at (14,26)
local EMP_X, EMP_Y = 19, 41            -- the herm is south, at (19,42)

local function registered(t) return L.getFlag(S.FLAG_ICHOR_TOWN_HERMS_START + t) end
local function registeredList()
  local out = {}
  for t = 0, S.TOWN_HERM_COUNT - 1 do if registered(t) then out[#out + 1] = t end end
  return table.concat(out, ",")
end

local function yesNo() return L.taskRunning("Task_HandleYesNoInput") end
local function menu() return L.taskRunning("Task_HandleScrollingMultichoiceInput")
                           or L.taskRunning("Task_HandleMultichoiceInput") end

-- Press A through a running script's messages until `cond` holds (never on a
-- question or a menu, and never once the player is free: A would touch the herm again).
local function pressUntil(cond, limit, what)
  local t0 = L.now()
  while not cond() do
    if L.now() - t0 > (limit or 1500) then shot("stuck"); L.fail("never reached " .. what) end
    if L.idle() or yesNo() or menu() then
      wait(2)
    else
      wait(12)
      if not (cond() or L.idle() or yesNo() or menu()) then tap(K.A) end
    end
  end
end

-- The travel menu's entries, as TOWN_HERM_* ids.
local function menuIds()
  local t = S.gMultiuseListMenuTemplate
  local items = emu:read32(t + S.OFF_LMT_ITEMS)
  local n = emu:read32(t + S.OFF_LMT_ITEMS + 12) & 0xFFF   -- totalItems, after three pointers
  local ids = {}
  for i = 0, n - 1 do ids[#ids + 1] = emu:read32(items + i * S.LIST_MENU_ITEM_SIZE + S.OFF_LMI_ID) end
  return ids
end

-- Touch the herm in direction `key`, answer the travel question, and in the
-- menu pick `pick` (an index) or leave. Returns the menu's ids.
local function touchHerm(key, travel, pick, menuShot)
  L.face(key)
  tap(K.A)
  pressUntil(function() return yesNo() or L.idle() end, 1500, "the herm's question")
  if not yesNo() then return nil end
  wait(10)
  if not travel then
    tap(K.DOWN); tap(K.A)
    pressUntil(L.idle, 600, "the herm to let go")
    return nil
  end
  tap(K.A)                                         -- YES
  pressUntil(menu, 600, "the travel menu")
  wait(20)
  local ids = menuIds()
  if menuShot then shot(menuShot) end
  for _ = 1, pick do tap(K.DOWN) end
  tap(K.A)
  return ids
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

  -- B -> A
  local ids = touchHerm(K.DOWN, true, 0, "travel_menu_emporion")
  expect(ids and #ids == 2 and ids[1] == S.TOWN_HERM_AKTI and ids[2] == S.TOWN_HERM_STAY,
         "Emporion's travel menu: Akti, then Stay here (" .. table.concat(ids or {}, ",") .. ")")
  L.waitUntil(function() return L.mapId() == S.MAP_AKTI and L.idle() end, 3000, "the travel to Akti")
  wait(40)
  shot("arrived_akti")
  local x, y = L.pos()
  expect(x == AKTI_X and y == AKTI_Y, string.format("Hermes sets the player beside Akti's herm (%d,%d)", x, y))

  -- A -> B
  ids = touchHerm(K.RIGHT, true, 0, "travel_menu_akti")
  expect(ids and #ids == 2 and ids[1] == S.TOWN_HERM_EMPORION and ids[2] == S.TOWN_HERM_STAY,
         "Akti's travel menu: Emporion, then Stay here; no unregistered town (" .. table.concat(ids or {}, ",") .. ")")
  L.waitUntil(function() return L.mapId() == S.MAP_EMPORION and L.idle() end, 3000, "the travel to Emporion")
  wait(40)
  shot("arrived_emporion")
  x, y = L.pos()
  expect(x == EMP_X and y == EMP_Y, string.format("Hermes sets the player beside Emporion's herm (%d,%d)", x, y))

  -- Stay here: the menu's last entry leaves the player where they are
  touchHerm(K.DOWN, true, 1)
  pressUntil(L.idle, 600, "the herm to let go")
  wait(30)
  x, y = L.pos()
  expect(L.mapId() == S.MAP_EMPORION and x == EMP_X and y == EMP_Y, "STAY HERE stays")
end)
