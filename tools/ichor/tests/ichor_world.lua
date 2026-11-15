-- The world's small systems, run by tools/ichor/tests/ichor_world.sh (read it first).

local L = dofile("tools/ichor/tests/engine_lib.lua")
local S, K, emu = L.S, L.K, L.emu
local log, expect, wait, shot, tap, settle = L.log, L.expect, L.wait, L.shot, L.tap, L.settle

local function clock(h, m)
  L.setVar(S.VAR_0x8004, h); L.setVar(S.VAR_0x8005, m)
  L.runHeader("WorldTest_ClockHeader")
end
local function hours() return emu:read8(S.gLocalTime + S.OFF_TIME_HOURS) end
local function minutes() return emu:read8(S.gLocalTime + S.OFF_TIME_MINUTES) end
local function menuUp()
  return L.taskRunning("Task_HandleScrollingMultichoiceInput") or L.taskRunning("Task_HandleMultichoiceInput")
end

L.start(function()
  L.quickstart()
  L.setVar(S.VAR_0x8008, 14); L.setVar(S.VAR_0x8009, 22)
  L.runHeader("WorldTest_SetupHeader", { limit = 4000 })
  L.waitUntil(function() return L.mapId() == S.MAP_ROUTE1 and L.idle() end, 3000, "Route 1")
  wait(40)

  -- The rest at 08:00: NOON, DUSK, NIGHT and NOT NOW. The second is DUSK.
  clock(8, 0)
  wait(10)
  expect(hours() == 8, string.format("the clock is set to 08:%02d (%d)", minutes(), hours()))
  L.runHeader("WorldTest_RestHeader", { noSettle = true })
  L.waitUntil(menuUp, 600, "the rest menu")
  wait(20); shot("rest_menu_morning")
  tap(K.DOWN); wait(8); tap(K.A)
  settle()
  wait(30)
  expect(L.getVar(S.VAR_0x8009) == 1 and hours() == 19 and minutes() <= 1,
         string.format("resting until dusk moves the clock to 19:00 (%02d:%02d, answer %d)", hours(), minutes(), L.getVar(S.VAR_0x8009)))
  shot("after_rest_dusk")

  -- NOT NOW leaves the clock alone
  L.runHeader("WorldTest_RestHeader", { noSettle = true })
  L.waitUntil(menuUp, 600, "the rest menu")
  wait(20); shot("rest_menu_dusk")
  tap(K.DOWN); wait(8); tap(K.A)   -- NIGHT, NOT NOW: the second
  settle()
  expect(L.getVar(S.VAR_0x8009) == 0 and hours() == 19, "NOT NOW leaves the clock at dusk")

  -- After 20:30 no hour is left: no menu, and FALSE
  clock(20, 45)
  L.runHeader("WorldTest_RestHeader")
  expect(L.getVar(S.VAR_0x8009) == 0 and hours() == 20, "after 20:30 the rest offers nothing and the clock stays")

  -- The party's highest level (the setup's Piplup is level 20)
  L.runHeader("WorldTest_LevelHeader")
  expect(L.getVar(S.VAR_0x8009) == 20, string.format("Ichor_GetHighestPartyLevel reads the party (%d)", L.getVar(S.VAR_0x8009)))
end)
