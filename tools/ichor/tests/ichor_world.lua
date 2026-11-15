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

  -- Knucklebones: mark a bone, roll it, then stand on every throw after
  local function playBones(opponent, name)
    L.setVar(S.VAR_0x8004, opponent)
    L.runHeader("WorldTest_BonesHeader", { noSettle = true })
    local menus, first = 0, true
    L.waitUntil(function()
      if menuUp() then
        menus = menus + 1
        wait(12)
        if first then
          shot(name .. "_menu")
          tap(K.A); wait(12)                         -- the first bone: KEEP -> ROLL
          L.waitUntil(menuUp, 120, "the menu again")
          wait(12); shot(name .. "_marked")
          for _ = 1, 4 do tap(K.DOWN); wait(6) end   -- ROLL THEM
          tap(K.A)
          first = false

        else
          tap(K.B)                                   -- STAND
        end
        wait(10)
      elseif not L.idle() then
        tap(K.A); wait(6)                            -- through the messages
      end
      return L.idle() and L.getVar(S.VAR_0x8009) ~= 0xFF
    end, 20000, "the match to end")
    return L.getVar(S.VAR_0x8009), menus
  end
  local result, menus = playBones(S.ICHOR_BONES_CAUTIOUS, "bones")
  expect((result == 0 or result == 1) and menus >= 3,
         string.format("a match against a cautious regular plays to its end (%s after %d menus)", result == 1 and "won" or "lost", menus))

  local function record() return emu:read16(L.ichor() + S.OFF_ICHOR_MOM_WINS), emu:read16(L.ichor() + S.OFF_ICHOR_MOM_LOSSES) end
  local w0, l0 = record()
  result = playBones(S.ICHOR_BONES_MOM, "mom")
  local w1, l1 = record()
  expect(l0 == 212 and w1 + l1 == w0 + l0 + 1 and (result == 1) == (w1 == w0 + 1),
         string.format("a match against Mom goes on her record (%d-%d -> %d-%d)", w0, l0, w1, l1))

  -- The party's highest level (the setup's Piplup is level 20)
  L.runHeader("WorldTest_LevelHeader")
  expect(L.getVar(S.VAR_0x8009) == 20, string.format("Ichor_GetHighestPartyLevel reads the party (%d)", L.getVar(S.VAR_0x8009)))
end)
